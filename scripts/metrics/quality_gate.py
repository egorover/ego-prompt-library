#!/usr/bin/env python3
"""Quality gate orchestrator.

Runs all individual metric checks and aggregates results.

Uses:
- models.PromptMetrics, models.Issue
- gate_checks (individual checkers)
"""

from ._imports import get_logger
from .models import PromptMetrics, Issue
from .gate_checks import (
    check_test_pass_rate,
    check_latency,
    check_quality,
    check_changes_frequency,
    check_status,
)

logger = get_logger(__name__)


def check_quality_gate(metrics: PromptMetrics) -> list[Issue]:
    """Проверяет промпт по quality gate критериям.

    Args:
        metrics: Объект с метриками промпта.

    Returns:
        Список найденных проблем (Issue).
    """
    issues: list[Issue] = []

    # Run all individual checkers
    issues.extend(check_test_pass_rate(metrics))
    issues.extend(check_latency(metrics))
    issues.extend(check_quality(metrics))
    issues.extend(check_changes_frequency(metrics))
    issues.extend(check_status(metrics))

    if issues:
        logger.debug(
            "Quality gate issues for %s: %d critical, %d warning, %d info",
            metrics.name,
            sum(1 for i in issues if i.severity == "critical"),
            sum(1 for i in issues if i.severity == "warning"),
            sum(1 for i in issues if i.severity == "info"),
        )

    return issues
