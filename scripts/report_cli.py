#!/usr/bin/env python3
"""CLI entry point for report generation.

\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0435:
    python scripts/report_cli.py                          # Markdown \u043e\u0442\u0447\u0451\u0442
    python scripts/report_cli.py --output report.md       # \u0432 \u0444\u0430\u0439\u043b
    python scripts/report_cli.py --json                   # JSON-\u0444\u043e\u0440\u043c\u0430\u0442
    python scripts/report_cli.py --html                   # HTML-\u0444\u043e\u0440\u043c\u0430\u0442
    python scripts/report_cli.py --strict                 # \u0442\u043e\u043b\u044c\u043a\u043e critical/warning

    python scripts/report.py ...                          # wrapper \u2192 report_cli
"""

import argparse
import sys
from pathlib import Path

from rich.console import Console

from _imports import (
    discover_prompts,
    get_logger,
)
from metrics import collect_metrics, check_quality_gate
from report import generate_json_report, generate_html_report, generate_md_report

logger = get_logger(__name__)
console = Console()


def main() -> None:
    """Run report generator CLI."""
    parser = argparse.ArgumentParser(description="Generate prompt library reports")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--strict", action="store_true", help="Show only critical/warning issues")
    args = parser.parse_args()

    library_root = Path(__file__).parent.parent
    prompts = discover_prompts(library_root)

    if not prompts:
        console.print("[WARN] No prompts found.", style="yellow")
        sys.exit(0)

    # \u0421\u043e\u0431\u0438\u0440\u0430\u0435\u043c \u043c\u0435\u0442\u0440\u0438\u043a\u0438
    metrics_list = [collect_metrics(p) for p in prompts]

    # \u041f\u0440\u043e\u0432\u0435\u0440\u044f\u0435\u043c quality gates
    all_issues: list = []
    for m in metrics_list:
        issues = check_quality_gate(m)
        all_issues.extend(issues)

    try:
        # JSON-\u0432\u044b\u0432\u043e\u0434
        if args.json:
            report = generate_json_report(metrics_list, all_issues, strict=args.strict)
            if args.output:
                Path(args.output).write_text(report, encoding="utf-8")
                console.print(f"[OK] JSON report written to {args.output}", style="green")
            else:
                console.print(report)
            return

        # HTML-\u0432\u044b\u0432\u043e\u0434
        if args.html:
            report = generate_html_report(metrics_list, all_issues)
            if args.output:
                Path(args.output).write_text(report, encoding="utf-8")
                console.print(f"[OK] HTML report written to {args.output}", style="green")
            else:
                console.print(report)
            return

        # Markdown-\u0432\u044b\u0432\u043e\u0434 (\u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e)
        report = generate_md_report(metrics_list, all_issues)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            console.print(f"[OK] Report written to {args.output}", style="green")
        else:
            console.print(report)
    except Exception as e:
        logger.error("Error generating report: %s", e, exc_info=True)
        console.print(f"[ERROR] Failed to generate report: {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    main()
