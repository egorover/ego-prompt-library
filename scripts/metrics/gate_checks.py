#!/usr/bin/env python3
"""Individual quality gate checkers for each metric.

Each function checks one metric and returns a list of issues.

Uses:
- models.PromptMetrics, models.Issue
- shared.METRICS_THRESHOLDS
"""

from ._imports import get_logger
from .models import PromptMetrics, Issue
from .thresholds import get_metrics_thresholds

logger = get_logger(__name__)


def check_test_pass_rate(metrics: PromptMetrics) -> list[Issue]:
    """Проверяет процент пройденных тестов.

    Args:
        metrics: Объект с метриками промпта.

    Returns:
        Список проблем (Issue).
    """
    issues: list[Issue] = []
    thresholds = get_metrics_thresholds()

    if metrics.test_pass_rate < thresholds["test_pass_rate"]["critical"]:
        issues.append(
            Issue(
                severity="critical",
                prompt_name=metrics.name,
                metric="test_pass_rate",
                message=f"Test pass rate {metrics.test_pass_rate}% is below {thresholds['test_pass_rate']['critical']}%",
                recommendation="Run all test cases and fix failures immediately",
            )
        )
        logger.warning("Critical: test_pass_rate for %s is %.1f%%", metrics.name, metrics.test_pass_rate)
    elif metrics.test_pass_rate < thresholds["test_pass_rate"]["warning"]:
        issues.append(
            Issue(
                severity="warning",
                prompt_name=metrics.name,
                metric="test_pass_rate",
                message=f"Test pass rate {metrics.test_pass_rate}% is below {thresholds['test_pass_rate']['warning']}%",
                recommendation="Review and fix failing test cases",
            )
        )

    return issues


def check_latency(metrics: PromptMetrics) -> list[Issue]:
    """Проверяет задержку генерации (P50).

    Args:
        metrics: Объект с метриками промпта.

    Returns:
        Список проблем (Issue).
    """
    issues: list[Issue] = []
    thresholds = get_metrics_thresholds()

    if metrics.latency_p50 > thresholds["latency_p50"]["critical"]:
        issues.append(
            Issue(
                severity="critical",
                prompt_name=metrics.name,
                metric="latency_p50",
                message=f"P50 latency {metrics.latency_p50}s exceeds {thresholds['latency_p50']['critical']}s",
                recommendation="Optimize prompt: reduce verbosity, simplify logic",
            )
        )
        logger.warning("Critical: latency_p50 for %s is %.1fs", metrics.name, metrics.latency_p50)
    elif metrics.latency_p50 > thresholds["latency_p50"]["warning"]:
        issues.append(
            Issue(
                severity="warning",
                prompt_name=metrics.name,
                metric="latency_p50",
                message=f"P50 latency {metrics.latency_p50}s exceeds {thresholds['latency_p50']['warning']}s",
                recommendation="Consider simplifying prompt sections",
            )
        )

    return issues


def check_quality(metrics: PromptMetrics) -> list[Issue]:
    """Проверяет средний рейтинг качества.

    Args:
        metrics: Объект с метриками промпта.

    Returns:
        Список проблем (Issue).
    """
    issues: list[Issue] = []
    thresholds = get_metrics_thresholds()

    if metrics.quality_count > 0 and metrics.quality_avg < thresholds["quality_avg"]["critical"]:
        issues.append(
            Issue(
                severity="critical",
                prompt_name=metrics.name,
                metric="quality_avg",
                message=f"Quality average {metrics.quality_avg} is below {thresholds['quality_avg']['critical']}",
                recommendation="Major review needed — prompt may be producing poor outputs",
            )
        )
        logger.warning("Critical: quality_avg for %s is %.1f", metrics.name, metrics.quality_avg)
    elif metrics.quality_count > 0 and metrics.quality_avg < thresholds["quality_avg"]["warning"]:
        issues.append(
            Issue(
                severity="warning",
                prompt_name=metrics.name,
                metric="quality_avg",
                message=f"Quality average {metrics.quality_avg} is below {thresholds['quality_avg']['warning']}",
                recommendation="Review user feedback and adjust prompt",
            )
        )

    return issues


def check_changes_frequency(metrics: PromptMetrics) -> list[Issue]:
    """Проверяет частоту изменений.

    Args:
        metrics: Объект с метриками промпта.

    Returns:
        Список проблем (Issue).
    """
    issues: list[Issue] = []
    thresholds = get_metrics_thresholds()

    if metrics.changes_this_month > thresholds["changes_per_month"]["warning"]:
        issues.append(
            Issue(
                severity="info",
                prompt_name=metrics.name,
                metric="changes_this_month",
                message=f"{metrics.changes_this_month} changes this month (recommended: ≤ {thresholds['changes_per_month']['warning']})",
                recommendation="Consider batching changes to reduce instability",
            )
        )

    return issues


def check_status(metrics: PromptMetrics) -> list[Issue]:
    """Проверяет статус промпта.

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
