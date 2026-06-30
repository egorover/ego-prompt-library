"""Unified import compatibility for standalone and package execution.

All scripts should import from this module to avoid circular imports
and ensure consistent import patterns.
"""

import sys
from pathlib import Path

try:
    from .logger import get_logger
    from .shared import (
        REQUIRED_CARD_SECTIONS,
        REQUIRED_FILES,
        REQUIRED_METADATA_FIELDS,
        REQUIRED_PROMPT_SECTIONS,
        VALID_STATUSES,
        ValidationResult,
        discover_prompts,
        parse_status,
        read_file,
    )
except ImportError:
    _root = Path(__file__).resolve().parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from logger import get_logger  # type: ignore[import, no-redef]
    from shared import (  # type: ignore[import, no-redef]
        REQUIRED_CARD_SECTIONS,
        REQUIRED_FILES,
        REQUIRED_METADATA_FIELDS,
        REQUIRED_PROMPT_SECTIONS,
        VALID_STATUSES,
        ValidationResult,
        discover_prompts,
        parse_status,
        read_file,
    )

__all__ = [
    "REQUIRED_CARD_SECTIONS",
    "REQUIRED_FILES",
    "REQUIRED_METADATA_FIELDS",
    "REQUIRED_PROMPT_SECTIONS",
    "VALID_STATUSES",
    "ValidationResult",
    "discover_prompts",
    "get_logger",
    "parse_status",
    "read_file",
]
