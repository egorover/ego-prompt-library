#!/usr/bin/env python3
"""
CLI-утилита для валидации структуры промптов.

Использование:
    python scripts/validate.py                      # валидировать все промпты
    python scripts/validate.py prompts/python-architect  # валидировать конкретный промпт
    python scripts/validate.py --strict              # строгий режим (warnings как errors)
    python scripts/validate.py --json                # JSON-вывод для CI
"""

import argparse
import json
import re
import sys
from pathlib import Path

from logger import get_logger
from shared import (
    REQUIRED_FILES,
    REQUIRED_PROMPT_SECTIONS,
    REQUIRED_CARD_SECTIONS,
    REQUIRED_METADATA_FIELDS,
    VALID_STATUSES,
    read_file,
    discover_prompts,
    ValidationResult,
)

logger = get_logger(__name__)


def validate_files(prompt_dir: Path) -> tuple[list[str], list[str]]:
    """Проверяет наличие и непустоту обязательных файлов.

    Args:
        prompt_dir: Путь к директории промпта.

    Returns:
        Кортеж (errors, warnings).
    """
    errors: list[str] = []
    warnings: list[str] = []

    for filename in REQUIRED_FILES:
        filepath = prompt_dir / filename
        try:
            if not filepath.exists():
                errors.append(f"Missing required file: {filename}")
                continue
            if not read_file(filepath).strip():
                errors.append(f"File is empty: {filename}")
        except (OSError, PermissionError) as e:
            errors.append(f"Error reading {filename}: {e}")

    return errors, warnings


def validate_prompt_structure(content: str) -> list[str]:
    """Проверяет наличие обязательных секций в prompt.md.

    Args:
        content: Содержимое prompt.md.

    Returns:
        Список ошибок (пусто если всё ОК).
    """
    return [f"Missing section in prompt.md: {s}" for s in REQUIRED_PROMPT_SECTIONS if s not in content]


def validate_card_structure(content: str) -> list[str]:
    """Проверяет наличие обязательных секций в card.md.

    Args:
        content: Содержимое card.md.

    Returns:
        Список ошибок (пусто если всё ОК).
    """
    return [f"Missing section in card.md: {s}" for s in REQUIRED_CARD_SECTIONS if s not in content]


def validate_metadata(content: str) -> tuple[list[str], list[str]]:
    """Проверяет обязательные поля в Metadata карточки.

    Args:
        content: Содержимое card.md.

    Returns:
        Кортеж (errors, warnings).
    """
    errors: list[str] = []
    warnings: list[str] = []

    metadata_content = _extract_metadata_section(content)

    for field_name in REQUIRED_METADATA_FIELDS:
        if f"| {field_name}" not in metadata_content:
            errors.append(f"Missing metadata field: {field_name}")

    if "YYYY-MM-DD" in metadata_content:
        warnings.append("Metadata may contain placeholder values (YYYY-MM-DD)")

    if not any(status in metadata_content for status in VALID_STATUSES):
        errors.append("No valid status found in metadata (expected: draft/testing/validated/deprecated)")

    return errors, warnings


def _extract_metadata_section(content: str) -> str:
    """Извлекает секцию Metadata из содержимого карточки.

    Args:
        content: Полное содержимое card.md.

    Returns:
        Строка с содержимым секции Metadata.
    """
    metadata_content = ""
    in_metadata = False
    for line in content.split("\n"):
        if "## Metadata" in line:
            in_metadata = True
            continue
        if in_metadata and line.startswith("##"):
            break
        if in_metadata:
            metadata_content += line + "\n"
    return metadata_content


def validate_test_cases(content: str) -> tuple[list[str], list[str]]:
    """Проверяет структуру тестовых кейсов.

    Args:
        content: Содержимое test-cases.md.

    Returns:
        Кортеж (errors, warnings).
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        tc_count = len(re.findall(r"TC-\d+:", content))
        if tc_count == 0:
            errors.append("No test cases found (expected TC-XXX format)")
        elif tc_count < 5:
            warnings.append(f"Only {tc_count} test cases (recommended: minimum 5)")
    except re.error as e:
        errors.append(f"Regex error in test cases: {e}")

    if "Status:" not in content and "Статус:" not in content:
        warnings.append("Test cases may not have Status field")

    return errors, warnings


def validate_changelog(content: str) -> tuple[list[str], list[str]]:
    """Проверяет структуру changelog.

    Args:
        content: Содержимое changelog.md.

    Returns:
        Кортеж (errors, warnings).
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        if not re.findall(r"## \[v?\d+\.\d+\.\d+\]", content):
            errors.append("No versioned entries found in changelog")
    except re.error as e:
        errors.append(f"Regex error in changelog: {e}")

    if "[Unreleased]" in content:
        warnings.append("Unreleased section found (should be versioned before merge)")

    return errors, warnings


def validate_prompt(prompt_dir: Path, strict: bool = False) -> ValidationResult:
    """Полная валидация промпта.

    Args:
        prompt_dir: Путь к директории промпта.
        strict: Строгий режим (warnings как errors).

    Returns:
        ValidationResult.
    """
    logger.info("Validating prompt: %s", prompt_dir.name)
    result = ValidationResult(prompt_dir=prompt_dir.name)

    try:
        # 1. Файлы
        file_errors, file_warnings = validate_files(prompt_dir)
        result.errors.extend(file_errors)
        result.warnings.extend(file_warnings)
        if file_errors:
            result.status = "fail"
            logger.warning("Validation failed for %s: %d errors", prompt_dir.name, len(file_errors))
            return result

        # 2. prompt.md
        prompt_content = read_file(prompt_dir / "prompt.md")
        result.errors.extend(validate_prompt_structure(prompt_content))

        # 3. card.md
        card_content = read_file(prompt_dir / "card.md")
        result.errors.extend(validate_card_structure(card_content))
        meta_errors, meta_warnings = validate_metadata(card_content)
        result.errors.extend(meta_errors)
        result.warnings.extend(meta_warnings)

        # 4. test-cases.md
        test_content = read_file(prompt_dir / "test-cases.md")
        test_errors, test_warnings = validate_test_cases(test_content)
        result.errors.extend(test_errors)
        result.warnings.extend(test_warnings)

        # 5. changelog.md
        changelog_content = read_file(prompt_dir / "changelog.md")
        chg_errors, chg_warnings = validate_changelog(changelog_content)
        result.errors.extend(chg_errors)
        result.warnings.extend(chg_warnings)

    except Exception as e:
        logger.error("Unexpected error validating %s: %s", prompt_dir.name, e, exc_info=True)
        result.errors.append(f"Unexpected error: {e}")
        result.status = "fail"
        return result

    # Статус
    if result.errors:
        result.status = "fail"
    elif result.warnings and strict:
        result.status = "fail"
    elif result.warnings:
        result.status = "warn"
    else:
        result.status = "pass"

    logger.info(
        "Validation result for %s: %s (%d errors, %d warnings)",
        prompt_dir.name,
        result.status,
        len(result.errors),
        len(result.warnings),
    )
    return result


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Validate prompt library structure")
    parser.add_argument("target", nargs="?", default=".", help="Path to prompt directory or library root")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    is_prompt_dir = "prompts" in str(target).lower() and target.is_dir()

    library_root = target.parent.parent if is_prompt_dir else target
    prompts = [target] if is_prompt_dir else discover_prompts(library_root)

    results = [validate_prompt(p, strict=args.strict) for p in prompts]

    if args.json:
        output = {
            "status": "pass" if all(r.is_valid for r in results) else "fail",
            "results": [r.to_dict() for r in results],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        total = len(results)
        passed = sum(1 for r in results if r.is_valid)
        failed = total - passed

        print(f"\n{'=' * 60}")
        print("Prompt Library Validation")
        print(f"{'=' * 60}")

        for r in results:
            icon = {"pass": "[PASS]", "warn": "[WARN]", "fail": "[FAIL]"}[r.status]
            print(f"\n{icon} {r.prompt_dir}")
            for w in r.warnings:
                print(f"   [WARN] {w}")
            for e in r.errors:
                print(f"   [ERR]  {e}")

        print(f"\n{'=' * 60}")
        print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
        print(f"{'=' * 60}\n")

        sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
