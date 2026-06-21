#!/usr/bin/env python3
"""
Parsers — извлечение данных из markdown-файлов промптов.

Каждая функция парсит один тип данных и возвращает строго типизированный результат.
"""

import re

from ..logger import get_logger

logger = get_logger(__name__)


def percentile(values: list[int], p: float) -> float:
    """Вычисляет перцентиль P для списка значений.

    Args:
        values: Список числовых значений.
        p: Перцентиль (0-100).

    Returns:
        Вычисленное значение перцентиля.
    """
    if not values:
        return 0.0
    try:
        sorted_v = sorted(values)
        k = (len(sorted_v) - 1) * (p / 100)
        f = int(k)
        c = f + 1 if f + 1 < len(sorted_v) else f
        d = k - f
        return round(sorted_v[f] + d * (sorted_v[c] - sorted_v[f]), 1)
    except (IndexError, TypeError) as e:
        logger.error("Error calculating percentile P%d: %s", p, e)
        return 0.0


def parse_test_results(test_content: str) -> tuple[int, int]:
    """Извлекает пройденные/общее количество тестов.

    Args:
        test_content: Содержимое test-cases.md

    Returns:
        Кортеж (passed, total) — количество пройденных и общее число тестов.
    """
    try:
        passed = len(re.findall(r"\*\*?Status:\*\*?\s*\u2705", test_content))
        failed = len(re.findall(r"\*\*?Status:\*\*?\s*\u274c", test_content))
        pending = len(re.findall(r"\*\*?Status:\*\*?\s*\u23f3", test_content))
        return passed, passed + failed + pending
    except re.error as e:
        logger.error("Regex error in test results: %s", e)
        return 0, 0


def parse_latency(latency_content: str) -> tuple[float, float, float]:
    """Извлекает P50, P95, P99 из latency.md.

    Args:
        latency_content: Содержимое latency.md

    Returns:
        Кортеж (p50, p95, p99) — перцентили в секундах.
    """
    p50_values: list[int] = []
    p95_values: list[int] = []
    p99_values: list[int] = []

    try:
        for line in latency_content.split("\n"):
            if "|" not in line:
                continue
            time_values = re.findall(r"(\d+)s", line)
            if len(time_values) >= 3:
                p50_values.append(int(time_values[0]))
                p95_values.append(int(time_values[1]))
                p99_values.append(int(time_values[2]))
    except (ValueError, re.error) as e:
        logger.error("Error parsing latency values: %s", e)

    return (
        percentile(p50_values, 50),
        percentile(p95_values, 95),
        percentile(p99_values, 99),
    )


def parse_quality(quality_content: str) -> tuple[float, int]:
    """Извлекает средний рейтинг качества из унифицированного шаблона.

    Args:
        quality_content: Содержимое quality.md

    Returns:
        Кортеж (average, count) — средний рейтинг и количество оценок.
    """
    ratings: list[float] = []

    try:
        for line in quality_content.split("\n"):
            if "|" not in line or not line.startswith("|"):
                continue

            parts = [p.strip() for p in line.split("|")]
            # Формат: | Date | User | Relevance | Completeness | Structure | Value | Scenario | Notes | Avg |
            if len(parts) >= 7:
                try:
                    relevance = int(parts[2])
                    completeness = int(parts[3])
                    structure = int(parts[4])
                    value = int(parts[5])
                    avg = (relevance + completeness + structure + value) / 4
                    if 1 <= avg <= 5:
                        ratings.append(avg)
                except (ValueError, IndexError):
                    continue
    except Exception as e:
        logger.error("Error parsing quality ratings: %s", e)

    if not ratings:
        return 0.0, 0
    return round(sum(ratings) / len(ratings), 1), len(ratings)
