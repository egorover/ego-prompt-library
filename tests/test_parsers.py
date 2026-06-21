"""Unit tests for metrics parsers."""

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


def test_percentile_empty():
    assert percentile([], 50) == 0.0


def test_percentile_single():
    assert percentile([10], 50) == 10.0


def test_parse_quality_from_table():
    avg, count = parse_quality(SAMPLE_QUALITY)
    assert count == 2
    assert avg == 4.7


def test_parse_quality_empty():
    avg, count = parse_quality("| Date | User |\n|------|------|")
    assert count == 0
    assert avg == 0.0


def test_parse_test_results():
    passed, total = parse_test_results(SAMPLE_TESTS)
    assert passed == 2
    assert total == 3


def test_parse_latency():
    p50, p95, p99 = parse_latency(SAMPLE_LATENCY)
    assert p50 == 5.5
    assert p95 == 8.9
    assert p99 == 14.0
