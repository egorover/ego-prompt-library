#!/usr/bin/env python3
"""Unit tests for report text sanitization."""

from report.sanitize import sanitize


class TestSanitize:
    """Тесты для функции санитизации текстовых полей."""

    def test_sanitizes_surrogate_characters(self) -> None:
        """Заменяет surrogate-символы на replacement character."""
        # U+D800–U+DFFF — это surrogate-диапазон Unicode
        text_with_surrogates = "test\ud800\udfffstring"
        result = sanitize(text_with_surrogates)
        # После санитизации surrogate должны быть заменены (на ? или \ufffd)
        assert "\ud800" not in result and "\udfff" not in result
        # И строка должна быть валидной UTF-8
        result.encode("utf-8")  # не должен выбрасывать исключение

    def test_sanitizes_null_bytes(self) -> None:
        """Удаляет нулевые байты."""
        text = "hello\x00world"
        result = sanitize(text)
        assert "\x00" not in result
        assert result == "helloworld"

    def test_normalizes_line_endings(self) -> None:
        """Нормализует переносы строк."""
        text = "line1\r\nline2\rline3"
        result = sanitize(text)
        assert "\r" not in result
        assert result == "line1\nline2\nline3"

    def test_passes_through_clean_text(self) -> None:
        """Не изменяет корректный текст."""
        text = "Hello, World! Привет, мир!"
        result = sanitize(text)
        assert result == text

    def test_returns_non_string_unchanged(self) -> None:
        """Возвращает не-строковые типы без изменений."""
        assert sanitize(None) is None
        assert sanitize(123) == 123
        assert sanitize(45.67) == 45.67

    def test_sanitizes_empty_string(self) -> None:
        """Корректно обрабатывает пустую строку."""
        assert sanitize("") == ""

    def test_sanitizes_cyrillic_text(self) -> None:
        """Корректно обрабатывает кириллицу."""
        text = "Тест кириллицы: проверка санитизации"
        result = sanitize(text)
        assert result == text
