"""Unified import compatibility for standalone and package execution.

All scripts should import from this module to avoid circular imports
and ensure consistent import patterns.

Note: This file intentionally uses try/except for fallback imports
which mypy flags as redefinition — suppressed below.
"""

try:
    from .logger import get_logger  # type: ignore[no-redef]
    from .shared import (
        METRICS_THRESHOLDS,
        discover_prompts,
        parse_status,
        read_file,
        ValidationResult,
        REQUIRED_FILES,
        REQUIRED_PROMPT_SECTIONS,
        REQUIRED_CARD_SECTIONS,
        REQUIRED_METADATA_FIELDS,
        VALID_STATUSES,
    )
    from .config import config
except ImportError:
    from logger import get_logger  # type: ignore[no-redef]
    from shared import (  # type: ignore[no-redef]
        METRICS_THRESHOLDS,
        discover_prompts,
        parse_status,
        read_file,
        ValidationResult,
        REQUIRED_FILES,
        REQUIRED_PROMPT_SECTIONS,
        REQUIRED_CARD_SECTIONS,
        REQUIRED_METADATA_FIELDS,
        VALID_STATUSES,
    )
    from config import config  # type: ignore[no-redef]

__all__ = [
    "METRICS_THRESHOLDS",
    "REQUIRED_FILES",
    "config",
    "discover_prompts",
    "get_logger",
    "parse_status",
    "read_file",
    "REQUIRED_PROMPT_SECTIONS",
    "REQUIRED_CARD_SECTIONS",
    "REQUIRED_METADATA_FIELDS",
    "VALID_STATUSES",
    "ValidationResult",
]
