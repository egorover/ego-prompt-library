"""Unit tests for metrics parsers."""

import pytest

from metrics.parsers import parse_quality, parse_test_results, parse_latency, percentile


SAMPLE_QUALITY = """
| Date       | User  | Relevance | Completeness | Structure | Value | Scenario | Notes | Avg |
|------------|-------|-----------|--------------|-----------|-------|----------|-------|-----|
| 2026-06-21 | admin | 5         | 4            | 5         | 5     | Architecture audit | Clean | 4.8 |
| 2026-06-20 | admin | 5         | 5            | 4         | 4     | New project | OK | 4.5 |
"""

SAMPLE_TESTS = """
- **Status:** ✅
- **Status:** ✅
- **Status:** ⏳
"""

SAMPLE_LATENCY = """
| Date | P50 | P95 | P99 |
|------|-----|-----|-----|
| 2026-06-21 | 5s | 8s | 12s |
| 2026-06-20 | 6s | 9s | 14s |
"""


# ── percentile ──────────────────────────────────────────────────────


def test_percentile_empty():
    assert percentile([], 50) == 0.0


def test_percentile_single():
    assert percentile([10], 50) == 10.0


# ── parse_quality (positive) ────────────────────────────────────────


def test_parse_quality_from_table():
    avg, count = parse_quality(SAMPLE_QUALITY)
    assert count == 2
    assert avg == 4.7


def test_parse_quality_with_computed_avg():
    """Формат без колонки Avg — вычисление из 4 колонок."""
    data = (
        "| Date       | User  | Relevance | Completeness | Structure | Value | Scenario | Notes |\n"
        "|------------|-------|-----------|--------------|-----------|-------|----------|-------|\n"
        "| 2026-06-21 | admin | 5         | 5            | 5         | 5     | Audit    | —     |\n"
    )
    avg, count = parse_quality(data)
    assert count == 1
    assert avg == 5.0


def test_parse_quality_empty():
    avg, count = parse_quality("| Date | User |\n|------|------|")
    assert count == 0
    assert avg == 0.0


def test_parse_quality_no_content():
    avg, count = parse_quality("")
    assert count == 0
    assert avg == 0.0


# ── parse_quality (negative / robustness) ───────────────────────────


def test_parse_quality_malformed_no_headers():
    """Полный мусор без заголовков — не должно упасть."""
    data = "this is not a table at all\nrandom garbage 12345\n||| |||\n"
    avg, count = parse_quality(data)
    assert count == 0
    assert avg == 0.0


def test_parse_quality_out_of_range_avg():
    """Значения Avg вне [1, 5] — должны быть проигнорированы."""
    data = (
        "| Date       | User  | Relevance | Completeness | Structure | Value | Scenario | Notes | Avg |\n"
        "|------------|-------|-----------|--------------|-----------|-------|----------|-------|-----|\n"
        "| 2026-06-21 | admin | 5         | 5            | 5         | 5     | Audit    | —     | 0.0 |\n"
        "| 2026-06-22 | admin | 5         | 5            | 5         | 5     | Audit    | —     | 6.0 |\n"
    )
    avg, count = parse_quality(data)
    assert count == 0
    assert avg == 0.0


def test_parse_quality_mixed_valid_invalid():
    """Смешанные валидные и невалидные строки."""
    data = (
        "| Date       | User  | Relevance | Completeness | Structure | Value | Scenario | Notes | Avg |\n"
        "|------------|-------|-----------|--------------|-----------|-------|----------|-------|-----|\n"
        "| 2026-06-21 | admin | 5         | 4            | 5         | 5     | Audit    | —     | 4.8 |\n"
        "| 2026-06-22 | admin | bad       | 5            | 4         | 4     | Bad      | —     | bad |\n"
        "| 2026-06-23 | admin | 5         | 5            | 5         | 5     | Good     | —     | 5.0 |\n"
    )
    avg, count = parse_quality(data)
    assert count == 2
    assert avg == pytest.approx(4.9)


def test_parse_quality_partial_columns():
    """Строки с недостаточным числом колонок — игнорируются."""
    data = "| Date | User | Relevance |\n|------|------|-----------|\n| 2026-06-21 | admin | 5 |\n"
    avg, count = parse_quality(data)
    assert count == 0
    assert avg == 0.0


# ── parse_test_results ──────────────────────────────────────────────


def test_parse_test_results():
    passed, total = parse_test_results(SAMPLE_TESTS)
    assert passed == 2
    assert total == 3


def test_parse_test_results_no_tests():
    passed, total = parse_test_results("no tests here")
    assert passed == 0
    assert total == 0


def test_parse_test_results_all_failed():
    data = "- **Status:** ❌\n- **Status:** ❌\n"
    passed, total = parse_test_results(data)
    assert passed == 0
    assert total == 2


# ── parse_latency ───────────────────────────────────────────────────


def test_parse_latency():
    p50, p95, p99 = parse_latency(SAMPLE_LATENCY)
    assert p50 == 5.5
    assert p95 == 8.9
    assert p99 == 14.0


def test_parse_latency_empty():
    p50, p95, p99 = parse_latency("")
    assert p50 == 0.0
    assert p95 == 0.0
    assert p99 == 0.0


def test_parse_latency_malformed():
    """Мусор без корректных строк таблицы — не должно упасть."""
    data = "not a table\n5s\njust text\n"
    p50, p95, p99 = parse_latency(data)
    assert p50 == 0.0
    assert p95 == 0.0
    assert p99 == 0.0


def test_parse_latency_single_row():
    data = "| 2026-06-21 | 10s | 20s | 30s |\n"
    p50, p95, p99 = parse_latency(data)
    assert p50 == 10.0
    assert p95 == 20.0
    assert p99 == 30.0
