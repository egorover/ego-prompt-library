#!/usr/bin/env python3
"""
Parsers — извлечение данных из markdown-файлов промптов.

Каждая функция парсит один тип данных и возвращает строго типизированный результат.
"""

import re
from pathlib import Path

from shared import read_file


def parse_test_results(test_content: str) -> tuple[int, int]:
    """Извлекает пройденные/общее количество тестов.

    Args:
        test_content: Содержимое test-cases.md

    Returns:
        Кортеж (passed, total) — количество пройденных и общее число тестов.
    """
    passed = len(re.findall(r"\*\*?Status:\*\*?\s*\u2705", test_content))
    failed = len(re.findall(r"\*\*?Status:\*\*?\s*\u274c", test_content))
    pending = len(re.findall(r"\*\*?Status:\*\*?\s*\u23f3", test_content))
    return passed, passed + failed + pending


def parse_latency(latency_content: str) -> tuple[float, float, float]:
    """Извлекает P50, P95, P99 из latency.md.

    Args:
        latency_content: Содержимое latency.md

    Returns:
        Кортеж (p50, p95, p99) — перцентили в секундах.
    """

    def percentile(values: list[int], p: float) -> float:
        if not values:
            return 0.0
        sorted_v = sorted(values)
        k = (len(sorted_v) - 1) * (p / 100)
        f = int(k)
        c = f + 1 if f + 1 < len(sorted_v) else f
        d = k - f
        return round(sorted_v[f] + d * (sorted_v[c] - sorted_v[f]), 1)

    p50_values: list[int] = []
    p95_values: list[int] = []
    p99_values: list[int] = []

    for line in latency_content.split("\n"):
        if "|" not in line:
            continue
        time_values = re.findall(r"(\d+)s", line)
        if len(time_values) >= 3:
            p50_values.append(int(time_values[0]))
            p95_values.append(int(time_values[1]))
            p99_values.append(int(time_values[2]))

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

    if not ratings:
        return 0.0, 0
    return round(sum(ratings) / len(ratings), 1), len(ratings)
