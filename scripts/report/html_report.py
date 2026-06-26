#!/usr/bin/env python3
"""HTML report generator for prompt library.

Generates a styled HTML dashboard with metrics summary,
per-prompt table, and issues section.
"""

from datetime import date
from pathlib import Path

try:
    from ..metrics.models import PromptMetrics, Issue
except ImportError:
    try:
        from metrics.models import PromptMetrics, Issue
    except ImportError:
        from scripts.metrics.models import PromptMetrics, Issue

from .utils import compute_summary


def generate_html_report(metrics_list: list[PromptMetrics], issues: list[Issue]) -> str:
    """Generate HTML report string.

    Args:
        metrics_list: List of collected prompt metrics.
        issues: List of quality gate issues.

    Returns:
        HTML-formatted string.
    """
    now = date.today().strftime("%Y-%m-%d %H:%M")
    summary = compute_summary(metrics_list, issues)

    critical_count = summary["critical_issues"]
    warning_count = summary["warning_issues"]
    healthy_count = summary["healthy"]

    rows = []
    for m in metrics_list:
        test_class = "green" if m.test_pass_rate >= 95 else ("yellow" if m.test_pass_rate >= 80 else "red")
        status_class = "green" if m.status == "validated" else ("yellow" if m.status == "testing" else "red")
        quality_display = m.quality_avg if m.quality_count > 0 else "\u2014"
        rows.append(
            f"""                <tr>
                    <td><strong>{m.name}</strong></td>
                    <td>{m.version}</td>
                    <td><span class="badge badge-{status_class}">{m.status}</span></td>
                    <td><span class="badge badge-{test_class}">{m.test_pass_rate}%</span></td>
                    <td>{m.latency_p50}s</td>
                    <td>{quality_display}</td>
                    <td>{m.usage_count}</td>
                </tr>"""
        )

    issues_html = ""
    if issues:
        issues_items = []
        for issue in sorted(issues, key=lambda x: {"critical": 0, "warning": 1, "info": 2}[x.severity]):
            issues_items.append(
                f"""            <div class="issue issue-{issue.severity}">
                <strong>[{issue.severity.upper()}]</strong> {issue.prompt_name} \u2014 {issue.metric}<br>
                {issue.message}<br>
                <em>\u2192 {issue.recommendation}</em>
            </div>"""
            )
        issues_html = f"""        <h2>\u26a0\ufe0f Issues</h2>
        <div class="issues">
{chr(10).join(issues_items)}
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prompt Library Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 20px 0; }}
        .card {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .card h3 {{ margin: 0 0 8px 0; color: #666; font-size: 14px; text-transform: uppercase; }}
        .card .value {{ font-size: 32px; font-weight: bold; }}
        .card .value.green {{ color: #28a745; }}
        .card .value.yellow {{ color: #ffc107; }}
        .card .value.red {{ color: #dc3545; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 20px 0; }}
        th {{ background: #007bff; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9fa; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
        .badge-green {{ background: #d4edda; color: #155724; }}
        .badge-yellow {{ background: #fff3cd; color: #856404; }}
        .badge-red {{ background: #f8d7da; color: #721c24; }}
        .issues {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 20px 0; }}
        .issue {{ padding: 12px; margin: 8px 0; border-left: 4px solid #ccc; background: #f8f9fa; }}
        .issue-critical {{ border-left-color: #dc3545; }}
        .issue-warning {{ border-left-color: #ffc107; }}
        .issue-info {{ border-left-color: #17a2b8; }}
        .timestamp {{ color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>\ud83d\udee0\ufe0f Prompt Library Dashboard</h1>
        <p class="timestamp">Generated: {now}</p>

        <div class="summary">
            <div class="card">
                <h3>Prompts</h3>
                <div class="value">{len(metrics_list)}</div>
            </div>
            <div class="card">
                <h3>Healthy</h3>
                <div class="value green">{healthy_count}/{len(metrics_list)}</div>
            </div>
            <div class="card">
                <h3>Critical Issues</h3>
                <div class="value {"red" if critical_count > 0 else "green"}">{critical_count}</div>
            </div>
            <div class="card">
                <h3>Warnings</h3>
                <div class="value {"yellow" if warning_count > 0 else "green"}">{warning_count}</div>
            </div>
        </div>

        <h2>Per-Prompt Metrics</h2>
        <table>
            <thead>
                <tr>
                    <th>Prompt</th>
                    <th>Version</th>
                    <th>Status</th>
                    <th>Tests</th>
                    <th>Latency P50</th>
                    <th>Quality</th>
                    <th>Usage</th>
                </tr>
            </thead>
            <tbody>
{chr(10)}{chr(10).join(rows)}
            </tbody>
        </table>

{issues_html}
    </div>
</body>
</html>"""

    return html


def write_html_report(metrics_list: list[PromptMetrics], issues: list[Issue], output_path: str) -> None:
    """Generate HTML report and write to file.

    Args:
        metrics_list: List of collected prompt metrics.
        issues: List of quality gate issues.
        output_path: File path to write report.
    """
    report = generate_html_report(metrics_list, issues)
    Path(output_path).write_text(report, encoding="utf-8")
