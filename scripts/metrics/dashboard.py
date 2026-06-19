#!/usr/bin/env python3
"""
Dashboard updater — генерация и запись dashboard.md для промптов.

Использует attrs-based подход: принимает любой объект с нужными полями.
"""

from datetime import date
from pathlib import Path


def update_dashboard(metrics: object, prompt_dir: Path) -> None:
    """Обновляет dashboard.md для промпта.

    Args:
        metrics: Объект с атрибутами (name, usage_count, test_pass_rate,
                 latency_p50, quality_avg, quality_count, changes_this_month,
                 open_issues).
        prompt_dir: Путь к директории промпта.
    """
    dashboard_path = prompt_dir / "metrics" / "dashboard.md"
    if not dashboard_path.exists():
        return

    now = date.today().strftime("%Y-%m-%d")

    test_status = "🟢" if metrics.test_pass_rate >= 95 else ("🟡" if metrics.test_pass_rate >= 80 else "🔴")
    latency_status = "🟢" if metrics.latency_p50 < 15 else ("🟡" if metrics.latency_p50 < 30 else "🔴")
    quality_status = "🟢" if metrics.quality_avg >= 4.0 else ("🟡" if metrics.quality_avg >= 3.0 else "🔴")

    content = f"""# Dashboard: {metrics.name}

## Summary ({now})

| Метрика            | Значение | Статус | Тренд  |
|--------------------|----------|--------|--------|
| Usage count        | {metrics.usage_count}        | ⚪     | {'→ рост' if metrics.usage_count > 0 else '⚪'}      |
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
