"""Import compatibility for standalone and package execution.

Note: try/except fallback imports are intentionally used for compatibility
with both package and standalone execution — mypy redefinition errors suppressed.
"""

try:
    from ..logger import get_logger  # type: ignore[no-redef]
except ImportError:
    from logger import get_logger  # type: ignore[no-redef]

try:
    from ..shared import discover_prompts, parse_status, read_file  # type: ignore[no-redef]
except ImportError:
    from shared import discover_prompts, parse_status, read_file  # type: ignore[no-redef]

__all__ = [
    "discover_prompts",
    "get_logger",
    "parse_status",
    "read_file",
]
