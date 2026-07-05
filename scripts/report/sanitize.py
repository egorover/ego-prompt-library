#!/usr/bin/env python3
"""Report text sanitization utilities.

Removes surrogate characters and other non-encodable sequences
from strings to prevent UnicodeEncodeError when writing UTF-8 files.
"""


def sanitize(text: str) -> str:
    """Очищает строку от surrogate-символов и некорректных UTF-8 последовательностей.

    Args:
        text: Исходная строка, возможно содержащая некорректные символы.

    Returns:
        Очищенная строка, безопасная для записи в UTF-8.
    """
    if not isinstance(text, str):
        return text

    # Удаляем surrogate-символы (U+D800–U+DFFF)
    sanitized = text.encode("utf-8", errors="replace").decode("utf-8")

    # Дополнительная очистка от нулевых байтов и других управляющих символов
    sanitized = sanitized.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")

    return sanitized
