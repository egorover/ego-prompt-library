"""Metrics thresholds — from config with shared.py fallback."""

try:
    from ..config import config
except ImportError:
    from config import config

from ._imports import METRICS_THRESHOLDS


def get_metrics_thresholds() -> dict[str, dict]:
    """Return quality gate thresholds (config overrides defaults)."""
    t = config.metrics_thresholds
    return {
        "test_pass_rate": {
            "warning": t.test_pass_rate_warning,
            "critical": t.test_pass_rate_critical,
        },
        "latency_p50": {
            "warning": t.latency_p50_warning,
            "critical": t.latency_p50_critical,
        },
        "quality_avg": {
            "warning": t.quality_avg_warning,
            "critical": t.quality_avg_critical,
        },
        "changes_per_month": {
            "warning": t.changes_per_month_warning,
        },
    }


# Backward-compatible alias for code that still imports METRICS_THRESHOLDS
DEFAULT_METRICS_THRESHOLDS = METRICS_THRESHOLDS
