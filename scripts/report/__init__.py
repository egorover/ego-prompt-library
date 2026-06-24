#!/usr/bin/env python3
"""Report subpackage for prompt library.

Provides:
- JSON report generation
- HTML report generation
- Markdown report generation
- utils for shared report logic
"""

try:
    from .json_report import generate_json_report  # type: ignore[no-redef]
    from .html_report import generate_html_report  # type: ignore[no-redef]
    from .md_report import generate_md_report  # type: ignore[no-redef]
    from .utils import compute_summary  # type: ignore[no-redef]
except ImportError:
    try:
        from report.json_report import generate_json_report  # type: ignore[no-redef]
        from report.html_report import generate_html_report  # type: ignore[no-redef]
        from report.md_report import generate_md_report  # type: ignore[no-redef]
        from report.utils import compute_summary  # type: ignore[no-redef]
    except ImportError:
        from scripts.report.json_report import generate_json_report  # type: ignore[no-redef]
        from scripts.report.html_report import generate_html_report  # type: ignore[no-redef]
        from scripts.report.md_report import generate_md_report  # type: ignore[no-redef]
        from scripts.report.utils import compute_summary  # type: ignore[no-redef]

__all__ = [
    "generate_json_report",
    "generate_html_report",
    "generate_md_report",
    "compute_summary",
]
