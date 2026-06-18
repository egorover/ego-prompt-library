#!/usr/bin/env python3
"""
Metrics Collector — сбор метрик для prompt library.

Собирает:
- Usage count (по changelog entries)
- Test pass rate (по test-cases.md Status)
- Latency (по latency.md)
- Quality rating (по quality.md)
- Change frequency (по changelog.md)
- Open issues (по card.md status)

Использование:
    python scripts/metrics-collector.py                     # собрать для всех промптов
    python scripts/metrics-collector.py prompts/python-architect  # конкретный
    python scripts/metrics-collector.py --all               # явный сбор всех
    python scripts/metrics-collector.py --json              # JSON-вывод
    python scripts/metrics-collector.py --dashboard         # обновить dashboard
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# Fix console encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


@dataclass
class PromptMetrics:
    name: str
    usage_count: int = 0
    test_pass_rate: float = 100.0
    test_total: int = 0
    test_passed: int = 0
    latency_p50: float = 0.0
    latency_p95: float = 0.0
    latency_p99: float = 0.0
    quality_avg: float = 0.0
    quality_count: int = 0
    changes_this_month: int = 0
    open_issues: int = 0
    version: str = ""
    status: str = ""
    trend: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "usage_count": self.usage_count,
            "test_pass_rate": self.test_pass_rate,
            "latency_p50": self.latency_p50,
            "latency_p95": self.latency_p95,
            "latency_p99": self.latency_p99,
            "quality_avg": self.quality_avg,
            "changes_this_month": self.changes_this_month,
            "open_issues": self.open_issues,
            "version": self.version,
            "status": self.status,
        }


def discover_prompts(library_root: Path) -> list[Path]:
    """Находит все директории промптов."""
    prompts_dir = library_root / "prompts"
    if not prompts_dir.exists():
        return []
    return [d for d in prompts_dir.iterdir() if d.is_dir()]


def read_file(path: Path) -> str:
    """Читает файл и возвращает содержимое."""
    return path.read_text(encoding="utf-8")


def parse_metadata(card_content: str) -> dict:
    """Извлекает метаданные из card.md."""
    metadata = {}
    in_metadata = False

    for line in card_content.split('\n'):
        if '## Metadata' in line or '## Metadata' in line:
            in_metadata = True
            continue

        if in_metadata and line.startswith('##'):
            break

        if in_metadata:
            match = re.match(r'\|\s*(\w+)\s*\|\s*([^|]+?)\s*\|', line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                if key in ("Name", "Version", "Status", "Updated", "Author", "Category"):
                    metadata[key] = value

    return metadata


def count_usage(card_content: str, changelog_content: str) -> int:
    """Считает количество использований по changelog."""
    # Каждый changelog entry — это одно изменение/использование
    versions = re.findall(r"## \[v?\d+\.\d+\.\d+\]", changelog_content)
    return len(versions)


def parse_test_results(test_content: str) -> tuple[int, int]:
    """Извлекает пройденные/общее количество тестов."""
    passed = len(re.findall(r"\*\*?Status:\*\*?\s*✅", test_content))
    failed = len(re.findall(r"\*\*?Status:\*\*?\s*❌", test_content))
    pending = len(re.findall(r"\*\*?Status:\*\*?\s*⏳", test_content))
    total = passed + failed + pending
    return passed, total


def parse_latency(latency_content: str) -> tuple[float, float, float]:
    """Извлекает P50, P95, P99 из latency.md."""
    p50_values = []
    p95_values = []
    p99_values = []

    # Ищем паттерн: <число>s ... <число>s ... <число>s
    for line in latency_content.split('\n'):
        if '|' not in line:
            continue
        # Ищем 3+ значения типа "5s" в строке
        time_values = re.findall(r'(\d+)s', line)
        if len(time_values) >= 3:
            p50_values.append(int(time_values[0]))
            p95_values.append(int(time_values[1]))
            p99_values.append(int(time_values[2]))

    def percentile(values: list[int], p: float) -> float:
        if not values:
            return 0.0
        sorted_v = sorted(values)
        k = (len(sorted_v) - 1) * (p / 100)
        f = int(k)
        c = f + 1 if f + 1 < len(sorted_v) else f
        d = k - f
        return round(sorted_v[f] + d * (sorted_v[c] - sorted_v[f]), 1)

    return (
        percentile(p50_values, 50),
        percentile(p95_values, 95),
        percentile(p99_values, 99),
    )


def parse_quality(quality_content: str) -> tuple[float, int]:
    """Извлекает средний рейтинг качества."""
    ratings = []
    for line in quality_content.split('\n'):
        # Формат: | 2026-06-18 | 5 | admin | ... | ...
        match = re.match(r'\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*(\d+)\s*\|', line)
        if match:
            rating = int(match.group(1))
            if 1 <= rating <= 5:
                ratings.append(rating)
    if not ratings:
        return 0.0, 0
    return round(sum(ratings) / len(ratings), 1), len(ratings)


def count_changes_this_month(changelog_content: str) -> int:
    """Считает количество изменений за текущий месяц."""
    now = date.today()
    current_month = now.strftime("%Y-%m")
    count = 0
    for line in changelog_content.split('\n'):
        if current_month in line or now.strftime("%B") in line or now.strftime("%b") in line:
            count += 1
    # Альтернатива: считаем по версиям с датами
    versions = re.findall(r"## \[v?\d+\.\d+\.\d+\].*?(\d{4}-\d{2}-\d{2})", changelog_content, re.DOTALL)
    for v_date in versions:
        if v_date.startswith(current_month):
            count += 1
    return max(count, len(versions) if not count else count)


def parse_status(card_content: str) -> str:
    """Извлекает статус промпта."""
    for status in ("draft", "testing", "validated", "deprecated"):
        if f"| {status} " in card_content or f"| {status}$" in card_content:
            return status
    return "unknown"


def collect_metrics(prompt_dir: Path) -> PromptMetrics:
    """Собирает все метрики для одного промпта."""
    name = prompt_dir.name
    metrics = PromptMetrics(name=name)

    # Card
    card_path = prompt_dir / "card.md"
    if card_path.exists():
        card_content = read_file(card_path)
        metadata = parse_metadata(card_content)
        metrics.version = metadata.get("Version", "")
        metrics.status = parse_status(card_content)

    # Changelog
    changelog_path = prompt_dir / "changelog.md"
    if changelog_path.exists():
        changelog_content = read_file(changelog_path)
        metrics.usage_count = count_usage(card_content if card_path.exists() else "", changelog_content)
        metrics.changes_this_month = count_changes_this_month(changelog_content)

    # Test cases
    test_path = prompt_dir / "test-cases.md"
    if test_path.exists():
        test_content = read_file(test_path)
        passed, total = parse_test_results(test_content)
        metrics.test_passed = passed
        metrics.test_total = total
        metrics.test_pass_rate = round((passed / total * 100), 1) if total > 0 else 100.0

    # Latency
    latency_path = prompt_dir / "metrics" / "latency.md"
    if latency_path.exists():
        latency_content = read_file(latency_path)
        metrics.latency_p50, metrics.latency_p95, metrics.latency_p99 = parse_latency(latency_content)

    # Quality
    quality_path = prompt_dir / "metrics" / "quality.md"
    if quality_path.exists():
        quality_content = read_file(quality_path)
        metrics.quality_avg, metrics.quality_count = parse_quality(quality_content)

    return metrics


def update_dashboard(metrics: PromptMetrics, prompt_dir: Path) -> None:
    """Обновляет dashboard.md для промпта."""
    dashboard_path = prompt_dir / "metrics" / "dashboard.md"
    if not dashboard_path.exists():
        return

    now = date.today().strftime("%Y-%m-%d")

    # Определяем статусы
    test_status = "🟢" if metrics.test_pass_rate >= 95 else ("🟡" if metrics.test_pass_rate >= 80 else "🔴")
    latency_status = "🟢" if metrics.latency_p50 < 15 else ("🟡" if metrics.latency_p50 < 30 else "🔴")
    usage_trend = "→ рост" if metrics.usage_count > 0 else "⚪"
    quality_status = "🟢" if metrics.quality_avg >= 4.0 else ("🟡" if metrics.quality_avg >= 3.0 else "🔴")

    content = f"""# Dashboard: {metrics.name}

## Summary ({now})

| Метрика            | Значение | Статус | Тренд  |
|--------------------|----------|--------|--------|
| Usage count        | {metrics.usage_count}        | ⚪     | {usage_trend}      |
| Test pass rate     | {metrics.test_pass_rate}%     | {test_status}     | {'→ стаб' if metrics.test_pass_rate == 100 else '→ ' + ('рост' if metrics.test_pass_rate > 95 else 'падение')} |
| Latency P50        | {int(metrics.latency_p50)}s       | {latency_status}     | —      |
| Quality Avg        | {metrics.quality_avg if metrics.quality_count > 0 else '—'}        | {quality_status if metrics.quality_count > 0 else '⚪'}     | —      |
| Changes (this mo)  | {metrics.changes_this_month}        | {'🟢' if metrics.changes_this_month <= 2 else '🟡'}     | —      |
| Open issues        | {metrics.open_issues}        | {'🟢' if metrics.open_issues < 3 else '🟡'}     | —      |

## Trend (последние 3 месяца)

| Месяц    | Usage | Test% | Latency | Quality | Issues |
|----------|-------|-------|---------|---------|--------|
| {now[:7]}  | {metrics.usage_count}     | {metrics.test_pass_rate}   | {int(metrics.latency_p50)}s      | {metrics.quality_avg if metrics.quality_count > 0 else '—'}       | {metrics.open_issues}      |

> 📌 Дашборд обновляется автоматически через CI.
"""

    dashboard_path.write_text(content, encoding="utf-8")


def generate_summary(metrics_list: list[PromptMetrics]) -> str:
    """Генерирует сводный отчёт по всем промптам."""
    total = len(metrics_list)
    passed = sum(1 for m in metrics_list if m.test_pass_rate >= 95)
    avg_latency = sum(m.latency_p50 for m in metrics_list) / total if total > 0 else 0
    avg_quality = sum(m.quality_avg for m in metrics_list if m.quality_count > 0) / max(1, sum(1 for m in metrics_list if m.quality_count > 0))

    now = date.today().strftime("%Y-%m-%d")

    report = f"""# Prompt Library Metrics Report

**Date:** {now}
**Prompts:** {total} | **Healthy:** {passed} | **Avg Latency:** {avg_latency:.0f}s | **Avg Quality:** {avg_quality:.1f}

---

## Summary

| Метрика | Значение | Статус |
|---------|----------|--------|
| Total prompts | {total} | — |
| Pass rate ≥ 95% | {passed}/{total} | {'🟢' if passed == total else '🟡'} |
| Avg latency P50 | {avg_latency:.0f}s | {'🟢' if avg_latency < 15 else '🟡'} |
| Avg quality | {avg_quality:.1f} | {'🟢' if avg_quality >= 4.0 else '🟡'} |

---

## Per-Prompt Metrics

"""

    for m in metrics_list:
        status_icon = "🟢" if m.test_pass_rate >= 95 and m.latency_p50 < 15 else "🟡"
        report += f"""### {m.name} {status_icon}

| Метрика | Значение |
|---------|----------|
| Version | {m.version} |
| Status | {m.status} |
| Usage count | {m.usage_count} |
| Test pass rate | {m.test_pass_rate}% |
| Latency P50 | {m.latency_p50}s |
| Latency P95 | {m.latency_p95}s |
| Latency P99 | {m.latency_p99}s |
| Quality Avg | {m.quality_avg if m.quality_count > 0 else '—'} |
| Changes (this mo) | {m.changes_this_month} |

---

"""

    return report


def main():
    parser = argparse.ArgumentParser(description="Collect metrics for prompt library")
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Path to prompt directory or library root",
    )
    parser.add_argument("--all", action="store_true", help="Collect metrics for all prompts")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--dashboard", action="store_true", help="Update dashboard files")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    args = parser.parse_args()

    target = Path(args.target).resolve()

    # Определяем корень библиотеки
    is_prompt_dir = "prompts" in str(target) and target.is_dir()
    library_root = target.parent.parent if is_prompt_dir else target

    # Находим промпты
    if is_prompt_dir:
        prompts = [target]
    else:
        prompts = discover_prompts(library_root)

    if not prompts:
        print("[WARN] No prompts found.")
        sys.exit(0)

    # Собираем метрики
    metrics_list = [collect_metrics(p) for p in prompts]

    # Обновляем dashboards
    if args.dashboard:
        for m in metrics_list:
            prompt_dir = library_root / "prompts" / m.name
            update_dashboard(m, prompt_dir)
        print(f"[OK] Updated dashboards for {len(metrics_list)} prompt(s)")

    # JSON-вывод
    if args.json:
        output = {
            "collected_at": datetime.now().isoformat(),
            "prompts": [m.to_dict() for m in metrics_list],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    # Ручной вывод
    print(f"\n{'='*60}")
    print(f"Metrics Collection — {len(metrics_list)} prompt(s)")
    print(f"{'='*60}")

    for m in metrics_list:
        print(f"\n[METRICS] {m.name} ({m.version}, {m.status})")
        print(f"   Usage: {m.usage_count} | Tests: {m.test_pass_rate}% ({m.test_passed}/{m.test_total})")
        print(f"   Latency P50: {m.latency_p50}s | Quality: {m.quality_avg if m.quality_count > 0 else '—'}")
        print(f"   Changes this month: {m.changes_this_month}")

    # Генерация отчёта
    if args.report:
        report = generate_summary(metrics_list)
        Path("report.md").write_text(report, encoding="utf-8")
        print(f"\n[OK] Report written to report.md")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
