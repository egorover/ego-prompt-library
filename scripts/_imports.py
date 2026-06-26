"""Unified import compatibility for standalone and package execution.

All scripts should import from this module to avoid circular imports
and ensure consistent import patterns.
"""

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
    from logger import get_logger
    from shared import (
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
