#!/usr/bin/env python3
"""CLI entry point for report generation.

Использование:
    python scripts/report_cli.py                          # Markdown отчёт
    python scripts/report_cli.py --output report.md       # в файл
    python scripts/report_cli.py --json                   # JSON-формат
    python scripts/report_cli.py --html                   # HTML-формат
    python scripts/report_cli.py --strict                 # только critical/warning
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
    from config import init

    init()

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

    # Собираем метрики
    metrics_list = [collect_metrics(p) for p in prompts]

    # Проверяем quality gates
    all_issues: list = []
    for m in metrics_list:
        issues = check_quality_gate(m)
        all_issues.extend(issues)

    # Фильтр для strict-режима (убираем info)
    filtered_issues = [i for i in all_issues if not args.strict or i.severity != "info"]

    try:
        # JSON-вывод
        if args.json:
            report = generate_json_report(metrics_list, all_issues, strict=args.strict)
            if args.output:
                Path(args.output).write_text(report, encoding="utf-8")
                console.print(f"[OK] JSON report written to {args.output}", style="green")
            else:
                console.print(report)
            return

        # HTML-вывод
        if args.html:
            report = generate_html_report(metrics_list, filtered_issues)
            if args.output:
                Path(args.output).write_text(report, encoding="utf-8")
                console.print(f"[OK] HTML report written to {args.output}", style="green")
            else:
                console.print(report)
            return

        # Markdown-вывод (по умолчанию)
        report = generate_md_report(metrics_list, filtered_issues)
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
