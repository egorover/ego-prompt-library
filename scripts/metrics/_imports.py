"""Import compatibility for standalone and package execution.

Uses sys.path manipulation for fallback imports to avoid
3-level nested try/except chains.
"""

import sys
from pathlib import Path

try:
    from ..logger import get_logger  # type: ignore[import-not-found]
except ImportError:
    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from logger import get_logger  # type: ignore[import, no-redef]

try:
    from ..shared import discover_prompts, parse_status, read_file  # type: ignore[import-not-found]
except ImportError:
    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from shared import discover_prompts, parse_status, read_file  # type: ignore[import, no-redef]

__all__ = [
    "discover_prompts",
    "get_logger",
    "parse_status",
    "read_file",
]
