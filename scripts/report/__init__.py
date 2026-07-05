#!/usr/bin/env python3
"""Report subpackage for prompt library.

Provides:
- JSON report generation
- HTML report generation
- Markdown report generation
- Text sanitization
- utils for shared report logic
"""

import sys
from pathlib import Path

try:
    from .json_report import generate_json_report
    from .html_report import generate_html_report
    from .md_report import generate_md_report
    from .sanitize import sanitize
    from .utils import compute_summary
except ImportError:
    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from scripts.report.json_report import generate_json_report  # type: ignore[import]
    from scripts.report.html_report import generate_html_report  # type: ignore[import]
    from scripts.report.md_report import generate_md_report  # type: ignore[import]
    from scripts.report.sanitize import sanitize  # type: ignore[import]
    from scripts.report.utils import compute_summary  # type: ignore[import]

__all__ = [
    "generate_json_report",
    "generate_html_report",
    "generate_md_report",
    "sanitize",
    "compute_summary",
]
