"""Metrics thresholds — loaded from config.py (single source of truth)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config import Config

# Lazy import — avoids circular import and side effects
_config: Config | None = None


def _get_config() -> Config | None:
    """Ленивый геттер для конфига (избегает side effects при импорте)."""
    global _config
    if _config is None:
        try:
            from config import _get_config as _cfg  # type: ignore[import-not-found]

            _config = _cfg()
        except ImportError:
            _config = None
    return _config


def get_metrics_thresholds() -> dict:
    """Return quality gate thresholds from config.py.

    Returns:
        Dictionary with threshold values for each metric.
    """
    try:
        cfg = _get_config()
        if cfg is not None:
            try:
                t = cfg.metrics_thresholds
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
            except Exception:
                pass
    except Exception:
        pass

    # Fallback defaults
    return {
        "test_pass_rate": {"warning": 95, "critical": 80},
        "latency_p50": {"warning": 15, "critical": 30},
        "quality_avg": {"warning": 4.0, "critical": 3.0},
        "changes_per_month": {"warning": 2},
    }
