#!/usr/bin/env python3
"""
Shared utilities for prompt library.

Provides:
- Common constants (file names, sections, thresholds)
- Reusable functions (read_file, discover_prompts, parse_status)
- Type-safe dataclasses for validation results
"""

from dataclasses import dataclass, field
from pathlib import Path

try:
    from .logger import get_logger  # type: ignore[no-redef]
except ImportError:
    from logger import get_logger  # type: ignore[no-redef]

logger = get_logger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────

REQUIRED_FILES: list[str] = [
    "prompt.md",
    "card.md",
    "test-cases.md",
    "changelog.md",
]

REQUIRED_PROMPT_SECTIONS: list[str] = [
    "1. Identity & Purpose",
    "2. Context & Domain",
    "3. Decision Framework",
    "4. Interaction Rules",
    "5. Output Format",
    "6. Anti-Patterns",
    "7. Quick Reference",
]

REQUIRED_CARD_SECTIONS: list[str] = [
    "## Metadata",
    "## Description",
    "## Input / Output",
    "## Scope & Boundaries",
    "## Constraints & Anti-Patterns",
    "## Usage Examples",
    "## Validation Status",
    "## Related Files",
]

REQUIRED_METADATA_FIELDS: list[str] = [
    "Name",
    "Version",
    "Author",
    "Status",
    "Created",
    "Updated",
    "Category",
]

VALID_STATUSES: set[str] = {"draft", "testing", "validated", "deprecated"}


# ── Core functions ────────────────────────────────────────────────────────


def read_file(path: Path) -> str:
    """Read file content with UTF-8 encoding.

    Args:
        path: Путь к файлу.

    Returns:
        Содержимое файла как строка.

    Raises:
        FileNotFoundError: Если файл не найден.
        PermissionError: Если нет прав на чтение.
        UnicodeDecodeError: Если файл не является текстовым.
    """
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.error("File not found: %s", path)
        raise
    except PermissionError:
        logger.error("Permission denied: %s", path)
        raise
    except UnicodeDecodeError:
        logger.error("File is not UTF-8 encoded: %s", path)
        raise


def discover_prompts(library_root: Path) -> list[Path]:
    """Find all prompt directories under <root>/prompts/.

    Args:
        library_root: Корневая директория библиотеки промптов.

    Returns:
        Отсортированный список путей к директориям промптов.
    """
    try:
        prompts_dir = library_root / "prompts"
        if not prompts_dir.exists():
            logger.warning("Prompts directory not found: %s", prompts_dir)
            return []
        prompts = sorted(d for d in prompts_dir.iterdir() if d.is_dir())
        logger.debug("Discovered %d prompt(s) in %s", len(prompts), prompts_dir)
        return prompts
    except OSError as e:
        logger.error("OS error while discovering prompts: %s", e)
        return []


def parse_status(card_content: str) -> str:
    """Extract prompt status from card.md Metadata section only.

    Args:
        card_content: Содержимое карточки промпта.

    Returns:
        Статус промпта или 'unknown'.
    """
    in_metadata: bool = False
    for line in card_content.split("\n"):
        if "## Metadata" in line:
            in_metadata = True
            continue
        if in_metadata and line.startswith("##"):
            break
        if in_metadata and "|" in line:
            for status in VALID_STATUSES:
                if f"| {status}|" in line or f"| {status} " in line:
                    return status
                if "| Status" in line and status in line:
                    return status
    return "unknown"


@dataclass
class ValidationResult:
    """Результат валидации промпта.

    Attributes:
        prompt_dir: Имя директории промпта.
        status: Статус валидации (pass/warn/fail).
        errors: Список ошибок.
        warnings: Список предупреждений.
    """

    prompt_dir: str
    status: str = "pass"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Флаг успешной валидации (без ошибок)."""
        return self.status == "pass"

    def to_dict(self) -> dict:
        """Конвертирует в словарь для JSON-сериализации.

        Returns:
            Словарь с результатами валидации.
        """
        return {
            "prompt_dir": self.prompt_dir,
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
        }
