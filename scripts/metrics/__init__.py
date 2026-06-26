#!/usr/bin/env python3
"""Metrics subpackage for prompt library.

Provides:
- collect_metrics: collect all metrics for a single prompt
- check_quality_gate: run quality gate checks
"""

try:
    from .collector import collect_metrics
    from .quality_gate import check_quality_gate
except ImportError:
    from scripts.metrics.collector import collect_metrics
    from scripts.metrics.quality_gate import check_quality_gate

__all__ = [
    "collect_metrics",
    "check_quality_gate",
]
