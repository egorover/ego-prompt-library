#!/usr/bin/env python3
"""JSON report generator for prompt library.

Generates structured JSON output with metrics, issues, and summary.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from ..metrics.models import PromptMetrics, Issue
except ImportError:
    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from scripts.metrics.models import PromptMetrics, Issue  # type: ignore[import]

from .sanitize import sanitize
from .utils import compute_summary


def generate_json_report(
    metrics_list: list[PromptMetrics],
    issues: list[Issue],
    strict: bool = False,
) -> str:
    """Generate JSON report string.

    Args:
        metrics_list: List of collected prompt metrics.
        issues: List of quality gate issues.
        strict: If True, filter to critical/warning only.

    Returns:
        JSON-formatted string.
    """
    if strict:
        issues = [i for i in issues if i.severity in ("critical", "warning")]

    summary = compute_summary(metrics_list, issues)

    output = {
        "generated_at": datetime.now().isoformat(),
        "prompts": [m.to_dict() for m in metrics_list],
        "issues": [
            {
                "severity": i.severity,
                "prompt": sanitize(i.prompt_name),
                "metric": sanitize(i.metric),
                "message": sanitize(i.message),
                "recommendation": sanitize(i.recommendation),
            }
            for i in issues
        ],
        "summary": summary,
    }

    return json.dumps(output, indent=2, ensure_ascii=False)


def write_json_report(
    metrics_list: list[PromptMetrics],
    issues: list[Issue],
    output_path: str,
    strict: bool = False,
) -> None:
    """Generate JSON report and write to file.

    Args:
        metrics_list: List of collected prompt metrics.
        issues: List of quality gate issues.
        output_path: File path to write report.
        strict: If True, filter to critical/warning only.
    """
    report = generate_json_report(metrics_list, issues, strict)
    Path(output_path).write_text(sanitize(report), encoding="utf-8")
