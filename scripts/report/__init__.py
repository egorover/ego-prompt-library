#!/usr/bin/env python3
"""Report subpackage for prompt library.

Provides:
- JSON report generation
- HTML report generation
- Markdown report generation
- utils for shared report logic
"""

try:
    from .json_report import generate_json_report
    from .html_report import generate_html_report
    from .md_report import generate_md_report
    from .utils import compute_summary
except ImportError:
    from scripts.report.json_report import generate_json_report
    from scripts.report.html_report import generate_html_report
    from scripts.report.md_report import generate_md_report
    from scripts.report.utils import compute_summary

__all__ = [
    "generate_json_report",
    "generate_html_report",
    "generate_md_report",
    "compute_summary",
]
