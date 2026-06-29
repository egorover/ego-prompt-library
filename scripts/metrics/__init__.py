#!/usr/bin/env python3
"""Metrics subpackage for prompt library.

Provides:
- collect_metrics: collect all metrics for a single prompt
- check_quality_gate: run quality gate checks
- check_lifecycle_gate: run lifecycle status checks (draft/deprecated)
"""

import sys
from pathlib import Path

try:
    from .collector import collect_metrics
    from .quality_gate import check_quality_gate, check_lifecycle_gate
except ImportError:
    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from scripts.metrics.collector import collect_metrics  # type: ignore[import]
    from scripts.metrics.quality_gate import check_quality_gate, check_lifecycle_gate  # type: ignore[import]

__all__ = [
    "collect_metrics",
    "check_quality_gate",
    "check_lifecycle_gate",
]
