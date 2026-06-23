"""Import compatibility for standalone and package execution."""

try:
    from ..logger import get_logger
except ImportError:
    from logger import get_logger

try:
    from ..shared import discover_prompts, parse_status, read_file
except ImportError:
    from shared import discover_prompts, parse_status, read_file

__all__ = [
    "discover_prompts",
    "get_logger",
    "parse_status",
    "read_file",
]
