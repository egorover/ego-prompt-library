#!/usr/bin/env python3
"""Report subpackage for prompt library.

Provides:
- JSON report generation
- HTML report generation
- Markdown report generation
- CLI entry point
- utils for shared report logic
"""

from report.json_report import generate_json_report
from report.html_report import generate_html_report
from report.md_report import generate_md_report
from report.utils import compute_summary

__all__ = [
    "generate_json_report",
    "generate_html_report",
    "generate_md_report",
    "compute_summary",
]
