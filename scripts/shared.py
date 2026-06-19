#!/usr/bin/env python3
"""
Shared utilities for prompt library scripts.

Provides:
- Common constants (file names, sections, thresholds)
- Reusable functions (read_file, discover_prompts, parse_status)
"""

import re
from pathlib import Path
from typing import Optional

# ── Constants ──────────────────────────────────────────────────────────────

REQUIRED_FILES = [
    "prompt.md",
    "card.md",
    "test-cases.md",
    "changelog.md",
]

REQUIRED_PROMPT_SECTIONS = [
    "1. Identity & Purpose",
    "2. Context & Domain",
    "3. Decision Framework",
    "4. Interaction Rules",
    "5. Output Format",
    "6. Anti-Patterns",
    "7. Quick Reference",
]

REQUIRED_CARD_SECTIONS = [
    "## Metadata",
    "## Description",
    "## Input / Output",
    "## Scope & Boundaries",
    "## Constraints & Anti-Patterns",
    "## Usage Examples",
    "## Validation Status",
    "## Related Files",
]

REQUIRED_METADATA_FIELDS = [
    "Name",
    "Version",
    "Author",
    "Status",
    "Created",
    "Updated",
    "Category",
]

VALID_STATUSES = {"draft", "testing", "validated", "deprecated"}

# ── Metrics thresholds ────────────────────────────────────────────────────

METRICS_THRESHOLDS = {
    "test_pass_rate": {"warning": 95, "critical": 80},
    "latency_p50": {"warning": 15, "critical": 30},
    "quality_avg": {"warning": 4.0, "critical": 3.0},
    "changes_per_month": {"warning": 2},
}

# ── Core functions ────────────────────────────────────────────────────────


def read_file(path: Path) -> str:
    """Read file content with UTF-8 encoding."""
    return path.read_text(encoding="utf-8")


def discover_prompts(library_root: Path) -> list[Path]:
    """Find all prompt directories under <root>/prompts/."""
    prompts_dir = library_root / "prompts"
    if not prompts_dir.exists():
        return []
    return sorted(d for d in prompts_dir.iterdir() if d.is_dir())


def parse_status(card_content: str) -> str:
    """Extract prompt status from card.md Metadata section only."""
    in_metadata = False
    for line in card_content.split("\n"):
        if "## Metadata" in line:
            in_metadata = True
            continue
        if in_metadata and line.startswith("##"):
            break
        for status in VALID_STATUSES:
            if f"| {status} " in line or f"| {status}$" in line:
                return status
    return "unknown"
