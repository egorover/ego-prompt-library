#!/usr/bin/env python3
"""Quality gate checks for prompt metrics.

Defines thresholds and checks against them, returning issues.

Uses:
- models.PromptMetrics, models.Issue
- shared.METRICS_THRESHOLDS
"""

from shared import METRICS_THRESHOLDS
from metrics.models import PromptMetrics, Issue


def check_quality_gate(metrics: PromptMetrics) -> list[Issue]:
    """Проверяет промпт по quality gate критериям.

    Args:
        metrics: Объект с метриками промпта.

    Returns:
        Список найденных проблем (Issue).
    """
    issues = []
    thresholds = METRICS_THRESHOLDS

    # Test pass rate
    if metrics.test_pass_rate < thresholds["test_pass_rate"]["critical"]:
        issues.append(Issue(
            severity="critical",
            prompt_name=metrics.name,
            metric="test_pass_rate",
            message=f"Test pass rate {metrics.test_pass_rate}% is below {thresholds['test_pass_rate']['critical']}%",
            recommendation="Run all test cases and fix failures immediately",
        ))
    elif metrics.test_pass_rate < thresholds["test_pass_rate"]["warning"]:
        issues.append(Issue(
            severity="warning",
            prompt_name=metrics.name,
            metric="test_pass_rate",
            message=f"Test pass rate {metrics.test_pass_rate}% is below {thresholds['test_pass_rate']['warning']}%",
            recommendation="Review and fix failing test cases",
        ))

    # Latency
    if metrics.latency_p50 > thresholds["latency_p50"]["critical"]:
        issues.append(Issue(
            severity="critical",
            prompt_name=metrics.name,
            metric="latency_p50",
            message=f"P50 latency {metrics.latency_p50}s exceeds {thresholds['latency_p50']['critical']}s",
            recommendation="Optimize prompt: reduce verbosity, simplify logic",
        ))
    elif metrics.latency_p50 > thresholds["latency_p50"]["warning"]:
        issues.append(Issue(
            severity="warning",
            prompt_name=metrics.name,
            metric="latency_p50",
            message=f"P50 latency {metrics.latency_p50}s exceeds {thresholds['latency_p50']['warning']}s",
            recommendation="Consider simplifying prompt sections",
        ))

    # Quality
    if metrics.quality_count > 0 and metrics.quality_avg < thresholds["quality_avg"]["critical"]:
        issues.append(Issue(
            severity="critical",
            prompt_name=metrics.name,
            metric="quality_avg",
            message=f"Quality average {metrics.quality_avg} is below {thresholds['quality_avg']['critical']}",
            recommendation="Major review needed — prompt may be producing poor outputs",
        ))
    elif metrics.quality_count > 0 and metrics.quality_avg < thresholds["quality_avg"]["warning"]:
        issues.append(Issue(
            severity="warning",
            prompt_name=metrics.name,
            metric="quality_avg",
            message=f"Quality average {metrics.quality_avg} is below {thresholds['quality_avg']['warning']}",
            recommendation="Review user feedback and adjust prompt",
        ))

    # Changes frequency
    if metrics.changes_this_month > thresholds["changes_per_month"]["warning"]:
        issues.append(Issue(
            severity="info",
            prompt_name=metrics.name,
            metric="changes_this_month",
            message=f"{metrics.changes_this_month} changes this month (recommended: ≤ {thresholds['changes_per_month']['warning']})",
            recommendation="Consider batching changes to reduce instability",
        ))

    # Status
    if metrics.status == "deprecated":
        issues.append(Issue(
            severity="info",
            prompt_name=metrics.name,
            metric="status",
            message="Prompt is deprecated",
            recommendation="Plan migration to new version or remove",
        ))
    elif metrics.status == "draft":
        issues.append(Issue(
            severity="warning",
            prompt_name=metrics.name,
            metric="status",
            message="Prompt is in draft status",
            recommendation="Complete validation and move to testing/validated",
        ))

    return issues
