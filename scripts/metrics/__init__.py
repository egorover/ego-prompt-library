#!/usr/bin/env python3
"""Metrics subpackage for prompt library.

Provides:
- Parsers for test results, latency, quality
- Dashboard updater
"""

from metrics.parsers import parse_latency, parse_quality, parse_test_results
from metrics.dashboard import update_dashboard

__all__ = [
    "parse_latency",
    "parse_quality",
    "parse_test_results",
    "update_dashboard",
]
