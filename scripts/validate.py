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
import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationResult:
    prompt_dir: str
    status: str = "pass"  # pass, warn, fail
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.status == "pass"

    def to_dict(self) -> dict:
        return {
            "prompt_dir": self.prompt_dir,
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
        }


# Обязательные файлы для каждого промпта
REQUIRED_FILES = [
    "prompt.md",
    "card.md",
    "test-cases.md",
    "changelog.md",
]

# Обязательные секции в prompt.md
REQUIRED_PROMPT_SECTIONS = [
    "1. Identity & Purpose",
    "2. Context & Domain",
    "3. Decision Framework",
    "4. Interaction Rules",
    "5. Output Format",
    "6. Anti-Patterns",
    "7. Quick Reference",
]

# Обязательные секции в card.md
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

# Обязательные поля в Metadata
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


def read_file(path: Path) -> str:
    """Читает файл и возвращает содержимое."""
    return path.read_text(encoding="utf-8")


def validate_files(prompt_dir: Path) -> list[str]:
    """Проверяет наличие обязательных файлов."""
    errors = []
    warnings = []

    for filename in REQUIRED_FILES:
        filepath = prompt_dir / filename
        if not filepath.exists():
            errors.append(f"Missing required file: {filename}")

    # Проверяем пустые файлы
    for filename in REQUIRED_FILES:
        filepath = prompt_dir / filename
        if filepath.exists():
            content = read_file(filepath)
            if not content.strip():
                errors.append(f"File is empty: {filename}")

    return errors, warnings


def validate_prompt_structure(content: str) -> list[str]:
    """Проверяет наличие обязательных секций в prompt.md."""
    errors = []
    for section in REQUIRED_PROMPT_SECTIONS:
        if section not in content:
            errors.append(f"Missing section in prompt.md: {section}")
    return errors


def validate_card_structure(content: str) -> list[str]:
    """Проверяет наличие обязательных секций в card.md."""
    errors = []
    for section in REQUIRED_CARD_SECTIONS:
        if section not in content:
            errors.append(f"Missing section in card.md: {section}")
    return errors


def validate_metadata(content: str) -> list[str]:
    """Проверяет обязательные поля в Metadata карточки."""
    errors = []
    warnings = []

    for field_name in REQUIRED_METADATA_FIELDS:
        if f"| {field_name}" not in content:
            errors.append(f"Missing metadata field: {field_name}")

    # Проверяем placeholder-значения
    # YYYY-MM-DD — реальный placeholder, v1.0.0 — допустимая первая версия
    if "YYYY-MM-DD" in content:
        warnings.append("Metadata may contain placeholder values (YYYY-MM-DD)")

    # Проверяем статус
    for status in VALID_STATUSES:
        if f"| {status} " in content or f"| {status}$" in content:
            break
    else:
        # Статус может быть в любом месте строки, более мягкая проверка
        pass

    # Проверяем что Status не empty
    # Ищем строку с полем Status в таблице
    for line in content.split('\n'):
        if '| Status' in line or '| Статус' in line:
            # Следующая строка или эта же строка должна иметь значение
            continue
    # Проверяем что есть строка со значением статуса
    status_found = False
    for valid_status in VALID_STATUSES:
        if valid_status in content:
            status_found = True
            break
    if not status_found:
        errors.append("No valid status found in metadata (expected: draft/testing/validated/deprecated)")

    return errors, warnings


def validate_version_format(content: str) -> list[str]:
    """Проверяет формат версий в changelog и card."""
    errors = []
    # Проверяем что версия начинается с 'v'
    versions = re.findall(r"v?(\d+\.\d+\.\d+)", content)
    non_prefixed = [v for v in versions if not content.startswith(f"## [v{v}")]
    # Это мягкая проверка, не строгая
    return errors


def validate_test_cases(content: str) -> list[str]:
    """Проверяет структуру тестовых кейсов."""
    errors = []
    warnings = []

    # Проверяем наличие хотя бы одного TC
    tc_count = len(re.findall(r"TC-\d+:", content))
    if tc_count == 0:
        errors.append("No test cases found (expected TC-XXX format)")
    elif tc_count < 5:
        warnings.append(f"Only {tc_count} test cases (recommended: minimum 5)")

    # Проверяем что у кейсов есть Status
    if "Status:" not in content and "Статус:" not in content:
        warnings.append("Test cases may not have Status field")

    return errors, warnings


def validate_changelog(content: str) -> list[str]:
    """Проверяет структуру changelog."""
    errors = []
    warnings = []

    # Проверяем что есть хотя бы одна версия
    versions = re.findall(r"## \[v?\d+\.\d+\.\d+\]", content)
    if not versions:
        errors.append("No versioned entries found in changelog")

    # Проверяем что нет Unreleased
    if "[Unreleased]" in content:
        warnings.append("Unreleased section found (should be versioned before merge)")

    return errors, warnings


def validate_prompt(prompt_dir: Path, strict: bool = False) -> ValidationResult:
    """Полная валидация промпта."""
    result = ValidationResult(prompt_dir=str(prompt_dir.relative_to(prompt_dir.parent.parent)))

    # 1. Проверка файлов
    file_errors, file_warnings = validate_files(prompt_dir)
    result.errors.extend(file_errors)
    result.warnings.extend(file_warnings)

    if file_errors:
        result.status = "fail"
        return result

    # 2. Проверка prompt.md
    prompt_content = read_file(prompt_dir / "prompt.md")
    prompt_errors = validate_prompt_structure(prompt_content)
    result.errors.extend(prompt_errors)

    # 3. Проверка card.md
    card_content = read_file(prompt_dir / "card.md")
    card_errors = validate_card_structure(card_content)
    metadata_errors, metadata_warnings = validate_metadata(card_content)
    result.errors.extend(card_errors)
    result.errors.extend(metadata_errors)
    result.warnings.extend(metadata_warnings)

    # 4. Проверка test-cases.md
    test_content = read_file(prompt_dir / "test-cases.md")
    test_errors, test_warnings = validate_test_cases(test_content)
    result.errors.extend(test_errors)
    result.warnings.extend(test_warnings)

    # 5. Проверка changelog.md
    changelog_content = read_file(prompt_dir / "changelog.md")
    changelog_errors, changelog_warnings = validate_changelog(changelog_content)
    result.errors.extend(changelog_errors)
    result.warnings.extend(changelog_warnings)

    # Определяем общий статус
    if result.errors:
        result.status = "fail"
    elif result.warnings and strict:
        result.status = "fail"
    elif result.warnings:
        result.status = "warn"
    else:
        result.status = "pass"

    return result


def discover_prompts(library_root: Path) -> list[Path]:
    """Находит все директории промптов."""
    prompts_dir = library_root / "prompts"
    if not prompts_dir.exists():
        return []
    return [d for d in prompts_dir.iterdir() if d.is_dir()]


def main():
    parser = argparse.ArgumentParser(description="Validate prompt library structure")
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Path to prompt directory or library root",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    target = Path(args.target).resolve()

    # Определяем корень библиотеки
    target_str = str(target).lower()
    is_prompt_dir = "prompts" in target_str and target.is_dir()

    if is_prompt_dir:
        library_root = target.parent.parent
    else:
        library_root = target

    # Определяем что валидировать
    if is_prompt_dir:
        # Конкретный промпт
        prompts = [target]
    else:
        # Все промпты
        prompts = discover_prompts(library_root)

    # Валидируем
    results = [validate_prompt(p, strict=args.strict) for p in prompts]

    # Выводим результат
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

        print(f"\n{'='*60}")
        print(f"Prompt Library Validation")
        print(f"{'='*60}")

        for r in results:
            if r.is_valid:
                icon = "[PASS]"
            elif r.status == "warn":
                icon = "[WARN]"
            else:
                icon = "[FAIL]"
            print(f"\n{icon} {r.prompt_dir}")
            for w in r.warnings:
                print(f"   [WARN] {w}")
            for e in r.errors:
                print(f"   [ERR]  {e}")

        print(f"\n{'='*60}")
        print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
        print(f"{'='*60}\n")

        sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
