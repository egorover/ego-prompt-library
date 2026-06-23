#!/usr/bin/env python3
"""Markdown report generator for prompt library.

Generates a structured Markdown report with summary,
per-prompt metrics, and issues section.
"""

from datetime import date
from pathlib import Path
from typing import List

try:
    from ..metrics.models import PromptMetrics, Issue
except ImportError:
    try:
        from metrics.models import PromptMetrics, Issue
    except ImportError:
        from scripts.metrics.models import PromptMetrics, Issue

from .utils import compute_summary


def generate_md_report(metrics_list: List[PromptMetrics], issues: List[Issue]) -> str:
    """Generate Markdown report string.

    Args:
        metrics_list: List of collected prompt metrics.
        issues: List of quality gate issues.

    Returns:
        Markdown-formatted string.
    """
    now = date.today().strftime("%Y-%m-%d")
    summary = compute_summary(metrics_list, issues)

    critical_count = summary["critical_issues"]
    warning_count = summary["warning_issues"]
    info_count = summary["info_issues"]
    healthy_count = summary["healthy"]

    lines = [
        "# Prompt Library Report",
        "",
        f"**Date:** {now}",
        f"**Prompts:** {len(metrics_list)} | **Healthy:** {healthy_count} | **Issues:** {critical_count} critical, {warning_count} warnings, {info_count} info",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| \u041c\u0435\u0442\u0440\u0438\u043a\u0430 | \u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 |",
        "|---------|----------|",
        f"| Total prompts | {len(metrics_list)} |",
        f"| Healthy (tests \u2265 95%, latency < 15s) | {healthy_count}/{len(metrics_list)} |",
        f"| Critical issues | {critical_count} |",
        f"| Warnings | {warning_count} |",
        f"| Info | {info_count} |",
        "",
        "---",
        "",
        "## Per-Prompt",
        "",
    ]

    for m in metrics_list:
        lines.extend([
            f"### {m.name} ({m.version}, {m.status})",
            "",
            "| \u041c\u0435\u0442\u0440\u0438\u043a\u0430 | \u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 |",
            "|---------|----------|",
            f"| Test pass rate | {m.test_pass_rate}% |",
            f"| Latency P50 | {m.latency_p50}s |",
            f"| Latency P95 | {m.latency_p95}s |",
            f"| Quality Avg | {m.quality_avg if m.quality_count > 0 else '\u2014'} |",
            f"| Usage count | {m.usage_count} |",
            f"| Changes this month | {m.changes_this_month} |",
            "",
        ])

    if issues:
        lines.extend(["---", "", "## Issues", ""])
        for issue in sorted(issues, key=lambda x: {"critical": 0, "warning": 1, "info": 2}[x.severity]):
            lines.extend([
                f"- **[{issue.severity.upper()}]** {issue.prompt_name} \u2014 {issue.metric}: {issue.message}",
                f"  \u2192 {issue.recommendation}",
            ])
        lines.append("")

    return "\n".join(lines)


def write_md_report(metrics_list: List[PromptMetrics], issues: List[Issue], output_path: str) -> None:
    """Generate Markdown report and write to file.

    Args:
        metrics_list: List of collected prompt metrics.
        issues: List of quality gate issues.
        output_path: File path to write report.
    """
    report = generate_md_report(metrics_list, issues)
    Path(output_path).write_text(report, encoding="utf-8")