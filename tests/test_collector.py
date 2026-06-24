"""Unit tests for metrics collector."""

from metrics.collector import (
    parse_metadata,
    count_usage,
    count_changes_this_month,
)


class TestParseMetadata:
    """Тесты для parse_metadata()."""

    def test_valid_metadata(self):
        """Парсит корректные метаданные."""
        content = """## Metadata

| Field | Value |
|-------|-------|
| Name | python-architect |
| Version | v1.1.0 |
| Author | test |
| Status | validated |
| Created | 2026-01-01 |
| Updated | 2026-06-21 |
| Category | architecture |
"""
        metadata = parse_metadata(content)
        assert metadata["Name"] == "python-architect"
        assert metadata["Version"] == "v1.1.0"
        assert metadata["Status"] == "validated"

    def test_missing_fields(self):
        """Пропускает отсутствующие поля."""
        content = """## Metadata

| Field | Value |
|-------|-------|
| Name | test |
"""
        metadata = parse_metadata(content)
        assert metadata["Name"] == "test"
        assert "Version" not in metadata


class TestCountUsage:
    """Тесты для count_usage()."""

    def test_empty_usage(self):
        """Пустой usage — 0."""
        assert count_usage("") == 0

    def test_header_only(self):
        """Только заголовок — 0."""
        content = """| Date | User | Scenario |
|------|------|----------|"""
        assert count_usage(content) == 0

    def test_with_entries(self):
        """С записями — считает правильно."""
        content = """| Date | User | Scenario |
|------|------|----------|
| 2026-06-21 | alex | Test 1 |
| 2026-06-20 | egor | Test 2 |
| 2026-06-19 | admin | Test 3 |"""
        assert count_usage(content) == 3


class TestCountChangesThisMonth:
    """Тесты для count_changes_this_month()."""

    def test_no_versions(self):
        """Нет версий — 0."""
        assert count_changes_this_month("# Changelog") == 0

    def test_current_month_versions(self):
        """Версии за текущий месяц — считает."""
        from datetime import date

        now = date.today()
        current_month = now.strftime("%Y-%m")
        content = f"""## [v1.1.0] — {current_month}-15

## [v1.0.0] — {current_month}-01"""
        count = count_changes_this_month(content)
        assert count == 2

    def test_previous_month_versions(self):
        """Версии за прошлый месяц — не считает."""
        from datetime import date, timedelta

        now = date.today()
        last_month = now.replace(day=1) - timedelta(days=1)
        last_month_str = last_month.strftime("%Y-%m")
        content = f"## [v1.0.0] — {last_month_str}-15"
        count = count_changes_this_month(content)
        assert count == 0
