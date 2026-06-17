#!/usr/bin/env python3
"""
Report Generator — генерация отчётов для prompt library.

Генерирует:
- Сводный отчёт по всем промптам
- Анализ трендов
- Выявление проблемных зон
- Recommendations

Использование:
    python scripts/report.py                          # стандартный отчёт
    python scripts/report.py --output report.md       # в файл
    python scripts/report.py --json                   # JSON-формат
    python scripts/report.py --strict                 # только проблемы
"""

import argparse
import json
import sys
import importlib.util
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# Fix console encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Загружаем metrics_collector динамически
_scripts_dir = Path(__file__).parent.resolve()
_spec = importlib.util.spec_from_file_location("metrics_collector", _scripts_dir / "metrics-collector.py")
_metrics_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_metrics_module)

collect_metrics = _metrics_module.collect_metrics
discover_prompts = _metrics_module.discover_prompts
PromptMetrics = _metrics_module.PromptMetrics


@dataclass
class Issue:
    severity: str  # critical, warning, info
    prompt_name: str
    metric: str
    message: str
    recommendation: str


def check_quality_gate(metrics: PromptMetrics) -> list[Issue]:
    """Проверяет промпт по quality gate критериям."""
    issues = []

    # Test pass rate
    if metrics.test_pass_rate < 80:
        issues.append(Issue(
            severity="critical",
            prompt_name=metrics.name,
            metric="test_pass_rate",
            message=f"Test pass rate {metrics.test_pass_rate}% is below 80%",
            recommendation="Run all test cases and fix failures immediately",
        ))
    elif metrics.test_pass_rate < 95:
        issues.append(Issue(
            severity="warning",
            prompt_name=metrics.name,
            metric="test_pass_rate",
            message=f"Test pass rate {metrics.test_pass_rate}% is below 95%",
            recommendation="Review and fix failing test cases",
        ))

    # Latency
    if metrics.latency_p50 > 30:
        issues.append(Issue(
            severity="critical",
            prompt_name=metrics.name,
            metric="latency_p50",
            message=f"P50 latency {metrics.latency_p50}s exceeds 30s",
            recommendation="Optimize prompt: reduce verbosity, simplify logic",
        ))
    elif metrics.latency_p50 > 15:
        issues.append(Issue(
            severity="warning",
            prompt_name=metrics.name,
            metric="latency_p50",
            message=f"P50 latency {metrics.latency_p50}s exceeds 15s",
            recommendation="Consider simplifying prompt sections",
        ))

    # Quality
    if metrics.quality_count > 0 and metrics.quality_avg < 3.0:
        issues.append(Issue(
            severity="critical",
            prompt_name=metrics.name,
            metric="quality_avg",
            message=f"Quality average {metrics.quality_avg} is below 3.0",
            recommendation="Major review needed — prompt may be producing poor outputs",
        ))
    elif metrics.quality_count > 0 and metrics.quality_avg < 4.0:
        issues.append(Issue(
            severity="warning",
            prompt_name=metrics.name,
            metric="quality_avg",
            message=f"Quality average {metrics.quality_avg} is below 4.0",
            recommendation="Review user feedback and adjust prompt",
        ))

    # Changes frequency
    if metrics.changes_this_month > 2:
        issues.append(Issue(
            severity="info",
            prompt_name=metrics.name,
            metric="changes_this_month",
            message=f"{metrics.changes_this_month} changes this month (recommended: ≤ 2)",
            recommendation="Consider batching changes to reduce instability",
        ))

    # Status
    if metrics.status == "deprecated":
        issues.append(Issue(
            severity="info",
            prompt_name=metrics.name,
            metric="status",
            message="Prompt is deprecated",
            recommendation="Plan migration to new version or remove",
        ))
    elif metrics.status == "draft":
        issues.append(Issue(
            severity="warning",
            prompt_name=metrics.name,
            metric="status",
            message="Prompt is in draft status",
            recommendation="Complete validation and move to testing/validated",
        ))

    return issues


def generate_html_report(metrics_list: list[PromptMetrics], issues: list[Issue]) -> str:
    """Генерирует HTML-отчёт."""
    now = date.today().strftime("%Y-%m-%d %H:%M")

    critical_count = sum(1 for i in issues if i.severity == "critical")
    warning_count = sum(1 for i in issues if i.severity == "warning")
    info_count = sum(1 for i in issues if i.severity == "info")

    healthy_count = sum(1 for m in metrics_list if m.test_pass_rate >= 95 and m.latency_p50 < 15)

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
        <h1>🔧 Prompt Library Dashboard</h1>
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
                <div class="value {'red' if critical_count > 0 else 'green'}">{critical_count}</div>
            </div>
            <div class="card">
                <h3>Warnings</h3>
                <div class="value {'yellow' if warning_count > 0 else 'green'}">{warning_count}</div>
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
"""

    for m in metrics_list:
        test_class = "green" if m.test_pass_rate >= 95 else ("yellow" if m.test_pass_rate >= 80 else "red")
        status_class = "green" if m.status == "validated" else ("yellow" if m.status == "testing" else "red")

        html += f"""                <tr>
                    <td><strong>{m.name}</strong></td>
                    <td>{m.version}</td>
                    <td><span class="badge badge-{status_class}">{m.status}</span></td>
                    <td><span class="badge badge-{test_class}">{m.test_pass_rate}%</span></td>
                    <td>{m.latency_p50}s</td>
                    <td>{m.quality_avg if m.quality_count > 0 else '—'}</td>
                    <td>{m.usage_count}</td>
                </tr>
"""

    html += """            </tbody>
        </table>

"""

    if issues:
        html += """        <h2>⚠️ Issues</h2>
        <div class="issues">\n"""
        for issue in sorted(issues, key=lambda x: {"critical": 0, "warning": 1, "info": 2}[x.severity]):
            html += f"""            <div class="issue issue-{issue.severity}">
                <strong>[{issue.severity.upper()}]</strong> {issue.prompt_name} — {issue.metric}<br>
                {issue.message}<br>
                <em>→ {issue.recommendation}</em>
            </div>\n"""
        html += """        </div>
"""

    html += """    </div>
</body>
</html>
"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate prompt library reports")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--strict", action="store_true", help="Show only critical/warning issues")
    args = parser.parse_args()

    library_root = Path(__file__).parent.parent
    prompts = discover_prompts(library_root)

    if not prompts:
        print("⚠️  No prompts found.")
        sys.exit(0)

    # Собираем метрики
    metrics_list = [collect_metrics(p) for p in prompts]

    # Проверяем quality gates
    all_issues = []
    for m in metrics_list:
        issues = check_quality_gate(m)
        all_issues.extend(issues)

    if args.strict:
        all_issues = [i for i in all_issues if i.severity in ("critical", "warning")]

    # JSON-вывод
    if args.json:
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
                for i in all_issues
            ],
            "summary": {
                "total_prompts": len(metrics_list),
                "healthy": sum(1 for m in metrics_list if m.test_pass_rate >= 95),
                "critical_issues": sum(1 for i in all_issues if i.severity == "critical"),
                "warning_issues": sum(1 for i in all_issues if i.severity == "warning"),
            },
        }
        output_str = json.dumps(output, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(output_str, encoding="utf-8")
            print(f"✅ JSON report written to {args.output}")
        else:
            print(output_str)
        return

    # HTML-вывод
    if args.html:
        html = generate_html_report(metrics_list, all_issues)
        if args.output:
            Path(args.output).write_text(html, encoding="utf-8")
            print(f"✅ HTML report written to {args.output}")
        else:
            print(html)
        return

    # Markdown-вывод (по умолчанию)
    now = date.today().strftime("%Y-%m-%d")

    critical_count = sum(1 for i in all_issues if i.severity == "critical")
    warning_count = sum(1 for i in all_issues if i.severity == "warning")
    info_count = sum(1 for i in all_issues if i.severity == "info")
    healthy_count = sum(1 for m in metrics_list if m.test_pass_rate >= 95 and m.latency_p50 < 15)

    md = f"""# Prompt Library Report

**Date:** {now}
**Prompts:** {len(metrics_list)} | **Healthy:** {healthy_count} | **Issues:** {critical_count} critical, {warning_count} warnings, {info_count} info

---

## Summary

| Метрика | Значение |
|---------|----------|
| Total prompts | {len(metrics_list)} |
| Healthy (tests ≥ 95%, latency < 15s) | {healthy_count}/{len(metrics_list)} |
| Critical issues | {critical_count} |
| Warnings | {warning_count} |
| Info | {info_count} |

---

## Per-Prompt

"""

    for m in metrics_list:
        md += f"### {m.name} (v{m.version}, {m.status})\n\n"
        md += f"| Метрика | Значение |\n|---------|----------|\n"
        md += f"| Test pass rate | {m.test_pass_rate}% |\n"
        md += f"| Latency P50 | {m.latency_p50}s |\n"
        md += f"| Latency P95 | {m.latency_p95}s |\n"
        md += f"| Quality Avg | {m.quality_avg if m.quality_count > 0 else '—'} |\n"
        md += f"| Usage count | {m.usage_count} |\n"
        md += f"| Changes this month | {m.changes_this_month} |\n\n"

    if all_issues:
        md += "---\n\n## Issues\n\n"
        for issue in sorted(all_issues, key=lambda x: {"critical": 0, "warning": 1, "info": 2}[x.severity]):
            md += f"- **[{issue.severity.upper()}]** {issue.prompt_name} — {issue.metric}: {issue.message}\n"
            md += f"  → {issue.recommendation}\n"
        md += "\n"

    if args.output:
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"✅ Report written to {args.output}")
    else:
        print(md)


if __name__ == "__main__":
    main()
