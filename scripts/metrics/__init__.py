#!/usr/bin/env python3
"""Metrics subpackage for prompt library.

Provides:
- models.PromptMetrics, models.Issue
- parsers for test results, latency, quality
- collector for metric collection
- quality_gate for threshold checks
- gate_checks for individual metric checkers
- dashboard updater
"""

from .models import PromptMetrics, Issue
from .parsers import parse_latency, parse_quality, parse_test_results
from .collector import collect_metrics
from .quality_gate import check_quality_gate
from .gate_checks import (
    check_test_pass_rate,
    check_latency,
    check_quality,
    check_changes_frequency,
    check_status,
)
from .dashboard import update_dashboard

__all__ = [
    "PromptMetrics",
    "Issue",
    "parse_latency",
    "parse_quality",
    "parse_test_results",
    "collect_metrics",
    "check_quality_gate",
    "check_test_pass_rate",
    "check_latency",
    "check_quality",
    "check_changes_frequency",
    "check_status",
    "update_dashboard",
]
