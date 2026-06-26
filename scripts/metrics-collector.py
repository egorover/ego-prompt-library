#!/usr/bin/env python3
"""Backward-compatible entry point — delegates to metrics.__main__.

Usage:
    python scripts/metrics-collector.py --all
"""

import sys
from pathlib import Path


def main() -> None:
    """Add parent dir to sys.path and delegate to metrics.__main__."""
    _scripts_dir = Path(__file__).resolve().parent
    if str(_scripts_dir.parent) not in sys.path:
        sys.path.insert(0, str(_scripts_dir.parent))

    from config import init
    from metrics.__main__ import main as _main  # noqa: PLC0414

    init()
    _main()


if __name__ == "__main__":
    main()
