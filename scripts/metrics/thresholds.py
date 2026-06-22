"""Metrics thresholds — defaults from shared.py (config.py fallback removed)."""

from ._imports import METRICS_THRESHOLDS

# Use shared.py thresholds directly — avoids circular import with config.py
DEFAULT_METRICS_THRESHOLDS = METRICS_THRESHOLDS


def get_metrics_thresholds() -> dict[str, dict]:
    """Return quality gate thresholds from shared.py.

    Returns:
        Dictionary with threshold values for each metric.
    """
    t = METRICS_THRESHOLDS
    return {
        "test_pass_rate": {
            "warning": t["test_pass_rate"]["warning"],
            "critical": t["test_pass_rate"]["critical"],
        },
        "latency_p50": {
            "warning": t["latency_p50"]["warning"],
            "critical": t["latency_p50"]["critical"],
        },
        "quality_avg": {
            "warning": t["quality_avg"]["warning"],
            "critical": t["quality_avg"]["critical"],
        },
        "changes_per_month": {
            "warning": t["changes_per_month"]["warning"],
        },
    }
