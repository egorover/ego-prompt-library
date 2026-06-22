#!/usr/bin/env python3
"""JSON report generator for prompt library.

Generates structured JSON output with metrics, issues, and summary.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List

try:
    from ..metrics.models import PromptMetrics, Issue
except ImportError:
    from scripts.metrics.models import PromptMetrics, Issue
from .utils import compute_summary


def generate_json_report(
    metrics_list: List[PromptMetrics],
    issues: List[Issue],
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
                "prompt": i.prompt_name,
                "metric": i.metric,
                "message": i.message,
                "recommendation": i.recommendation,
            }
            for i in issues
        ],
        "summary": summary,
    }

    return json.dumps(output, indent=2, ensure_ascii=False)


def write_json_report(
    metrics_list: List[PromptMetrics],
    issues: List[Issue],
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
    Path(output_path).write_text(report, encoding="utf-8")
