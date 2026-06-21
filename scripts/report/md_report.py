#!/usr/bin/env python3
"""Markdown report generator for prompt library.

Generates a structured Markdown report with summary,
per-prompt metrics, and issues section.
"""

from datetime import date
from pathlib import Path
from typing import List

from metrics.models import PromptMetrics, Issue


def generate_md_report(metrics_list: List[PromptMetrics], issues: List[Issue]) -> str:
    """Generate Markdown report string.

    Args:
        metrics_list: List of collected prompt metrics.
        issues: List of quality gate issues.

    Returns:
        Markdown-formatted string.
    """
    now = date.today().strftime("%Y-%m-%d")
    critical_count = sum(1 for i in issues if i.severity == "critical")
    warning_count = sum(1 for i in issues if i.severity == "warning")
    info_count = sum(1 for i in issues if i.severity == "info")
    healthy_count = sum(1 for m in metrics_list if m.test_pass_rate >= 95 and m.latency_p50 < 15)

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
        "| Метрика | Значение |",
        "|---------|----------|",
        f"| Total prompts | {len(metrics_list)} |",
        f"| Healthy (tests ≥ 95%, latency < 15s) | {healthy_count}/{len(metrics_list)} |",
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
            "| Метрика | Значение |",
            "|---------|----------|",
            f"| Test pass rate | {m.test_pass_rate}% |",
            f"| Latency P50 | {m.latency_p50}s |",
            f"| Latency P95 | {m.latency_p95}s |",
            f"| Quality Avg | {m.quality_avg if m.quality_count > 0 else '—'} |",
            f"| Usage count | {m.usage_count} |",
            f"| Changes this month | {m.changes_this_month} |",
            "",
        ])

    if issues:
        lines.extend(["---", "", "## Issues", ""])
        for issue in sorted(issues, key=lambda x: {"critical": 0, "warning": 1, "info": 2}[x.severity]):
            lines.extend([
                f"- **[{issue.severity.upper()}]** {issue.prompt_name} — {issue.metric}: {issue.message}",
                f"  → {issue.recommendation}",
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
