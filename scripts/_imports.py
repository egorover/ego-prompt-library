"""Unified import compatibility for standalone and package execution.

All scripts should import from this module to avoid circular imports
and ensure consistent import patterns.
"""

try:
    from .logger import get_logger, setup_logger
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
    from logger import get_logger, setup_logger
    from shared import (
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
    from config import config

__all__ = [
    "METRICS_THRESHOLDS",
    "config",
    "discover_prompts",
    "get_logger",
    "parse_status",
    "read_file",
    "Required_FILES",
    "REQUIRED_PROMPT_SECTIONS",
    "REQUIRED_CARD_SECTIONS",
    "REQUIRED_METADATA_FIELDS",
    "VALID_STATUSES",
    "ValidationResult",
]