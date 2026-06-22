#!/usr/bin/env python3
"""Report utilities — shared logic for report generators.

Provides:
- compute_summary: calculates summary statistics from metrics and issues
"""

from typing import List

try:
    from ..metrics.models import PromptMetrics, Issue
except ImportError:
    from scripts.metrics.models import PromptMetrics, Issue
except ImportError:
    from scripts.metrics.models import PromptMetrics, Issue
except ImportError:
    from scripts.metrics.models import PromptMetrics, Issue
except ImportError:
    from scripts.metrics.models import PromptMetrics, Issue
except ImportError:
    from scripts.metrics.models import PromptMetrics, Issue
except ImportError:
    from scripts.metrics.models import PromptMetrics, Issue
except ImportError:
    from scripts.metrics.models import PromptMetrics, Issue


def compute_summary(
    metrics_list: List[PromptMetrics],
    issues: List[Issue],
) -> dict:
    """Вычисляет сводную статистику для отчёта.

    Args:
        metrics_list: Список метрик промптов.
        issues: Список проблем quality gate.

    Returns:
        Словарь с суммарной статистикой.
    """
    critical_count = sum(1 for i in issues if i.severity == "critical")
    warning_count = sum(1 for i in issues if i.severity == "warning")
    info_count = sum(1 for i in issues if i.severity == "info")
    healthy_count = sum(
        1 for m in metrics_list
        if m.test_pass_rate >= 95 and m.latency_p50 < 15
    )

    return {
        "total_prompts": len(metrics_list),
        "healthy": healthy_count,
        "critical_issues": critical_count,
        "warning_issues": warning_count,
        "info_issues": info_count,
    }
