#!/usr/bin/env python3
"""Individual quality gate checkers for each metric.

Each function checks one metric and returns a list of issues.

Uses:
- models.PromptMetrics, models.Issue
- thresholds passed from quality_gate.py (single source call)
"""

from ._imports import get_logger
from .models import PromptMetrics, Issue

logger = get_logger(__name__)

Thresholds = dict[str, dict[str, float | int]]


def check_test_pass_rate(metrics: PromptMetrics, thresholds: Thresholds) -> list[Issue]:
    """Проверяет процент пройденных тестов.

    Args:
        metrics: Объект с метриками промпта.
        thresholds: Пороги quality gate (кэшированные).

    Returns:
        Список проблем (Issue).
    """
    issues: list[Issue] = []
    t = thresholds["test_pass_rate"]

    if metrics.test_pass_rate < t["critical"]:
        issues.append(
            Issue(
                severity="critical",
                prompt_name=metrics.name,
                metric="test_pass_rate",
                message=f"Test pass rate {metrics.test_pass_rate}% is below {t['critical']}%",
                recommendation="Run all test cases and fix failures immediately",
            )
        )
        logger.warning("Critical: test_pass_rate for %s is %.1f%%", metrics.name, metrics.test_pass_rate)
    elif metrics.test_pass_rate < t["warning"]:
        issues.append(
            Issue(
                severity="warning",
                prompt_name=metrics.name,
                metric="test_pass_rate",
                message=f"Test pass rate {metrics.test_pass_rate}% is below {t['warning']}%",
                recommendation="Review and fix failing test cases",
            )
        )

    return issues


def check_latency(metrics: PromptMetrics, thresholds: Thresholds) -> list[Issue]:
    """Проверяет задержку генерации (P50).

    Args:
        metrics: Объект с метриками промпта.
        thresholds: Пороги quality gate (кэшированные).

    Returns:
        Список проблем (Issue).
    """
    issues: list[Issue] = []
    t = thresholds["latency_p50"]

    if metrics.latency_p50 > t["critical"]:
        issues.append(
            Issue(
                severity="critical",
                prompt_name=metrics.name,
                metric="latency_p50",
                message=f"P50 latency {metrics.latency_p50}s exceeds {t['critical']}s",
                recommendation="Optimize prompt: reduce verbosity, simplify logic",
            )
        )
        logger.warning("Critical: latency_p50 for %s is %.1fs", metrics.name, metrics.latency_p50)
    elif metrics.latency_p50 > t["warning"]:
        issues.append(
            Issue(
                severity="warning",
                prompt_name=metrics.name,
                metric="latency_p50",
                message=f"P50 latency {metrics.latency_p50}s exceeds {t['warning']}s",
                recommendation="Consider simplifying prompt sections",
            )
        )

    return issues


def check_quality(metrics: PromptMetrics, thresholds: Thresholds) -> list[Issue]:
    """Проверяет средний рейтинг качества.

    Args:
        metrics: Объект с метриками промпта.
        thresholds: Пороги quality gate (кэшированные).

    Returns:
        Список проблем (Issue).
    """
    issues: list[Issue] = []
    t = thresholds["quality_avg"]

    if metrics.quality_count > 0 and metrics.quality_avg < t["critical"]:
        issues.append(
            Issue(
                severity="critical",
                prompt_name=metrics.name,
                metric="quality_avg",
                message=f"Quality average {metrics.quality_avg} is below {t['critical']}",
                recommendation="Major review needed — prompt may be producing poor outputs",
            )
        )
        logger.warning("Critical: quality_avg for %s is %.1f", metrics.name, metrics.quality_avg)
    elif metrics.quality_count > 0 and metrics.quality_avg < t["warning"]:
        issues.append(
            Issue(
                severity="warning",
                prompt_name=metrics.name,
                metric="quality_avg",
                message=f"Quality average {metrics.quality_avg} is below {t['warning']}",
                recommendation="Review user feedback and adjust prompt",
            )
        )

    return issues


def check_changes_frequency(metrics: PromptMetrics, thresholds: Thresholds) -> list[Issue]:
    """Проверяет частоту изменений.

    Args:
        metrics: Объект с метриками промпта.
        thresholds: Пороги quality gate (кэшированные).

    Returns:
        Список проблем (Issue).
    """
    issues: list[Issue] = []
    t = thresholds["changes_per_month"]

    if metrics.changes_this_month > t["warning"]:
        issues.append(
            Issue(
                severity="info",
                prompt_name=metrics.name,
                metric="changes_this_month",
                message=f"{metrics.changes_this_month} changes this month (recommended: ≤ {t['warning']})",
                recommendation="Consider batching changes to reduce instability",
            )
        )

    return issues


def check_status(metrics: PromptMetrics) -> list[Issue]:
    """Проверяет статус промпта (lifecycle check, not quality).

    Args:
        metrics: Объект с метриками промпта.

    Returns:
        Список проблем (Issue).
    """
    issues: list[Issue] = []

    if metrics.status == "deprecated":
        issues.append(
            Issue(
                severity="info",
                prompt_name=metrics.name,
                metric="status",
                message="Prompt is deprecated",
                recommendation="Plan migration to new version or remove",
            )
        )
    elif metrics.status == "draft":
        issues.append(
            Issue(
                severity="warning",
                prompt_name=metrics.name,
                metric="status",
                message="Prompt is in draft status",
                recommendation="Complete validation and move to testing/validated",
            )
        )

    return issues
