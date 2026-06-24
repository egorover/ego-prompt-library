#!/usr/bin/env python3
"""Backward-compatible wrapper for report_cli."""

import sys
from pathlib import Path


def main() -> None:
    """Add parent dir to sys.path and delegate to report_cli."""
    _scripts_dir = Path(__file__).resolve().parent
    if str(_scripts_dir.parent) not in sys.path:
        sys.path.insert(0, str(_scripts_dir.parent))

    from report_cli import main as _main  # noqa: PLC0414

    _main()


if __name__ == "__main__":
    main()
