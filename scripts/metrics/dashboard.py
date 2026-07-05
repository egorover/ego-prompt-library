#!/usr/bin/env python3
"""Dashboard updater — генерация и запись dashboard.md для промптов.

Uses PromptMetrics dataclass to generate markdown dashboard files.
"""

import sys
from datetime import date
from pathlib import Path

from ._imports import get_logger
from .models import PromptMetrics

try:
    from ..report.sanitize import sanitize
except ImportError:
    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from scripts.report.sanitize import sanitize  # type: ignore[import]

logger = get_logger(__name__)


def _get_month_names() -> list[str]:
    """Return last 3 month keys as 'YYYY-MM' strings."""
    now = date.today()
    months = []
    for i in range(2, -1, -1):
        month_num = (now.month - 1 - i) % 12 + 1
        year = now.year if month_num <= now.month else now.year - 1
        months.append(f"{year}-{month_num:02d}")
    return months


def _build_trend_rows(metrics: PromptMetrics, months: list[str]) -> list[str]:
    """Build trend rows for dashboard. Uses current metrics for current month,
    and placeholder data for previous months (historical data would require
    storing past snapshots)."""
    rows = []
    for i, month_key in enumerate(reversed(months)):
        year, month = map(int, month_key.split("-"))
        month_name = [
            "январь",
            "февраль",
            "март",
            "апрель",
            "май",
            "июнь",
            "июль",
            "август",
            "сентябрь",
            "октябрь",
            "ноябрь",
            "декабрь",
        ][month - 1]

        if i == 2:  # Current month
            rows.append(
                f"| {month_name} ({year})  | {metrics.usage_count}     | {metrics.test_pass_rate}   | {int(metrics.latency_p50)}s      | {metrics.quality_avg if metrics.quality_count > 0 else '—'}       | {metrics.open_issues}      |"
            )
        else:
            rows.append(f"| {month_name} ({year})  | —     | —   | —      | —       | —      |")
    return rows


def update_dashboard(metrics: PromptMetrics, prompt_dir: Path) -> None:
    """Обновляет dashboard.md для промпта.

    Args:
        metrics: Объект с метриками промпта (PromptMetrics).
        prompt_dir: Путь к директории промпта.
    """
    dashboard_path = prompt_dir / "metrics" / "dashboard.md"
    if not dashboard_path.exists():
        logger.debug("Dashboard not found for %s, skipping", prompt_dir.name)
        return

    now = date.today()
    now_str = now.strftime("%Y-%m-%d")
    months = _get_month_names()
    trend_rows = _build_trend_rows(metrics, months)

    test_status = "🟢" if metrics.test_pass_rate >= 95 else ("🟡" if metrics.test_pass_rate >= 80 else "🔴")
    latency_status = "🟢" if metrics.latency_p50 < 15 else ("🟡" if metrics.latency_p50 < 30 else "🔴")
    quality_status = "🟢" if metrics.quality_avg >= 4.0 else ("🟡" if metrics.quality_avg >= 3.0 else "🔴")

    trend_body = "\n".join(trend_rows)

    content = f"""# Dashboard: {metrics.name}

## Summary ({now_str})

| Метрика            | Значение | Статус | Тренд  |
|--------------------|----------|--------|--------|
| Usage count        | {metrics.usage_count}        | ⚪     | {"→ рост" if metrics.usage_count > 0 else "⚪"}      |
| Test pass rate     | {metrics.test_pass_rate}%     | {test_status}     | {"→ стаб" if metrics.test_pass_rate == 100 else "→ " + ("рост" if metrics.test_pass_rate > 95 else "падение")} |
| Latency P50        | {int(metrics.latency_p50)}s       | {latency_status}     | —      |
| Quality Avg        | {metrics.quality_avg if metrics.quality_count > 0 else "—"}        | {quality_status if metrics.quality_count > 0 else "⚪"}     | —      |
| Changes (this mo)  | {metrics.changes_this_month}        | {"🟢" if metrics.changes_this_month <= 2 else "🟡"}     | —      |
| Open issues        | {metrics.open_issues}        | {"🟢" if metrics.open_issues < 3 else "🟡"}     | —      |

## Trend (последние 3 месяца)

| Месяц    | Usage | Test% | Latency | Quality | Issues |
|----------|-------|-------|---------|---------|--------|
{trend_body}

> 📌 Дашборд обновляется автоматически через CI.
"""

    try:
        dashboard_path.write_text(sanitize(content), encoding="utf-8")
        logger.debug("Dashboard updated for %s", prompt_dir.name)
    except OSError as e:
        logger.error("Failed to write dashboard for %s: %s", prompt_dir.name, e)
