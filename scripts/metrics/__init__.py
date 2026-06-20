#!/usr/bin/env python3
"""Metrics subpackage for prompt library.

Provides:
- models.PromptMetrics, models.Issue
- parsers for test results, latency, quality
- collector for metric collection
- quality_gate for threshold checks
- dashboard updater
"""

from metrics.models import PromptMetrics, Issue
from metrics.parsers import parse_latency, parse_quality, parse_test_results
from metrics.collector import collect_metrics
from metrics.quality_gate import check_quality_gate
from metrics.dashboard import update_dashboard

__all__ = [
    "PromptMetrics",
    "Issue",
    "parse_latency",
    "parse_quality",
    "parse_test_results",
    "collect_metrics",
    "check_quality_gate",
    "update_dashboard",
]
