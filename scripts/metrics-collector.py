#!/usr/bin/env python3
"""Backward-compatible entry point — delegates to metrics.__main__."""

import sys
from pathlib import Path

# Add parent dir to sys.path so relative imports work when run directly
_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir.parent) not in sys.path:
    sys.path.insert(0, str(_scripts_dir.parent))

from metrics.__main__ import main

if __name__ == "__main__":
    main()
