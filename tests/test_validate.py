"""Unit tests for prompt validation."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from validate import (
    validate_files,
    validate_prompt_structure,
    validate_card_structure,
    validate_metadata,
    validate_test_cases,
    validate_changelog,
)


class TestValidateFiles:
    """Тесты для validate_files()."""

    def test_missing_files(self, tmp_path: Path):
        """Если обязательные файлы отсутствуют — ошибки."""
        errors, warnings = validate_files(tmp_path)
        assert len(errors) == 4  # 4 обязательных файла

    def test_empty_files(self, tmp_path: Path):
        """Если файлы пустые — ошибки."""
        for f in ["prompt.md", "card.md", "test-cases.md", "changelog.md"]:
            (tmp_path / f).write_text("", encoding="utf-8")
        errors, warnings = validate_files(tmp_path)
        assert len(errors) == 4  # все пустые

    def test_valid_files(self, tmp_path: Path):
        """Если файлы есть и не пустые — без ошибок."""
        for f in ["prompt.md", "card.md", "test-cases.md", "changelog.md"]:
            (tmp_path / f).write_text("content", encoding="utf-8")
        errors, warnings = validate_files(tmp_path)
        assert len(errors) == 0


class TestValidatePromptStructure:
    """Тесты для validate_prompt_structure()."""

    def test_missing_sections(self):
        """Если секции отсутствуют — ошибки."""
        content = "# Title\n\n## Other Section"
        errors = validate_prompt_structure(content)
        assert len(errors) == 7

    def test_all_sections_present(self):
        """Если все секции есть — без ошибок."""
        content = "\n".join([
            "# Title",
            "## 1. Identity & Purpose",
            "## 2. Context & Domain",
            "## 3. Decision Framework",
            "## 4. Interaction Rules",
            "## 5. Output Format",
            "## 6. Anti-Patterns",
            "## 7. Quick Reference",
        ])
        errors = validate_prompt_structure(content)
        assert len(errors) == 0


class TestValidateCardStructure:
    """Тесты для validate_card_structure()."""

    def test_missing_sections(self):
        """Если секции отсутствуют — ошибки."""
        content = "# Title"
        errors = validate_card_structure(content)
        assert len(errors) == 8

    def test_all_sections_present(self):
        """Если все секции есть — без ошибок."""
        content = "\n".join([
            "## Metadata",
            "## Description",
            "## Input / Output",
            "## Scope & Boundaries",
            "## Constraints & Anti-Patterns",
            "## Usage Examples",
            "## Validation Status",
            "## Related Files",
        ])
        errors = validate_card_structure(content)
        assert len(errors) == 0


class TestValidateMetadata:
    """Тесты для validate_metadata()."""

    def test_missing_fields(self):
        """Если поля отсутствуют — ошибки."""
        content = "## Metadata\n\n| Name | test |"
        errors, warnings = validate_metadata(content)
        assert len(errors) >= 1  # минимум одно missing field

    def test_valid_metadata(self):
        """Если все поля есть — без ошибок."""
        content = """## Metadata

| Field | Value |
|-------|-------|
| Name | test |
| Version | v1.0.0 |
| Author | test |
| Status | validated |
| Created | 2026-01-01 |
| Updated | 2026-01-01 |
| Category | test |
"""
        errors, warnings = validate_metadata(content)
        assert len(errors) == 0

    def test_placeholder_warning(self):
        """Если есть YYYY-MM-DD — предупреждение."""
        content = """## Metadata

| Field | Value |
|-------|-------|
| Name | test |
| Version | YYYY-MM-DD |
| Author | test |
| Status | validated |
| Created | YYYY-MM-DD |
| Updated | YYYY-MM-DD |
| Category | test |
"""
        errors, warnings = validate_metadata(content)
        assert any("placeholder" in w for w in warnings)


class TestValidateTestCases:
    """Тесты для validate_test_cases()."""

    def test_no_test_cases(self):
        """Если нет тестов — ошибка."""
        content = "# Test Cases"
        errors, warnings = validate_test_cases(content)
        assert any("No test cases" in e for e in errors)

    def test_few_test_cases(self):
        """Если мало тестов (< 5) — предупреждение."""
        content = "### TC-001: Test 1\n\n### TC-002: Test 2"
        errors, warnings = validate_test_cases(content)
        assert any("Only 2 test cases" in w for w in warnings)

    def test_valid_test_cases(self):
        """Если тестов достаточно — без ошибок."""
        content = "\n".join([f"### TC-00{i}: Test {i}" for i in range(1, 6)])
        errors, warnings = validate_test_cases(content)
        assert len(errors) == 0


class TestValidateChangelog:
    """Тесты для validate_changelog()."""

    def test_no_version(self):
        """Если нет версий — ошибка."""
        content = "# Changelog"
        errors, warnings = validate_changelog(content)
        assert any("No versioned entries" in e for e in errors)

    def test_valid_version(self):
        """Если версия есть — без ошибок."""
        content = "## [v1.0.0] — 2026-01-01"
        errors, warnings = validate_changelog(content)
        assert len(errors) == 0

    def test_unreleased_warning(self):
        """Если есть Unreleased — предупреждение."""
        content = """## [Unreleased]

## [v1.0.0] — 2026-01-01"""
        errors, warnings = validate_changelog(content)
        assert any("Unreleased" in w for w in warnings)