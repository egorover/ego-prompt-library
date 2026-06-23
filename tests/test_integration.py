"""Integration tests for the full prompt library pipeline.

Tests the complete flow:
1. Validate prompt structure
2. Collect metrics
3. Check quality gates
4. Generate reports
"""

import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from validate import validate_prompt
from metrics import collect_metrics, check_quality_gate
from report import generate_json_report, generate_md_report, generate_html_report
from metrics.models import PromptMetrics, Issue


class TestIntegrationPipeline:
    """Интеграционные тесты полного пайплайна."""

    def test_full_pipeline_valid_prompt(self):
        """Валидный промпт проходит весь пайплайн."""
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Создаём валидную структуру с правильными секциями
            (tmp_path / "prompt.md").write_text("""# Test Role

## 1. Identity & Purpose
Test purpose.

## 2. Context & Domain
Test context.

## 3. Decision Framework
Test decision.

## 4. Interaction Rules
Test rules.

## 5. Output Format
Test output.

## 6. Anti-Patterns
Test anti-patterns.

## 7. Quick Reference
Test reference.
""", encoding="utf-8")

            (tmp_path / "card.md").write_text("""# Test Role — Card

## Metadata
| Field | Value |
|-------|-------|
| Name | test-role |
| Version | v1.0.0 |
| Author | test |
| Status | validated |
| Created | 2026-01-01 |
| Updated | 2026-06-21 |
| Category | test |

## Description
Test description.

## Input / Output
Test input/output.

## Scope & Boundaries
Test scope.

## Constraints & Anti-Patterns
Test constraints.

## Usage Examples
Test examples.

## Validation Status
Test validation.

## Related Files
Test related.
""", encoding="utf-8")

            (tmp_path / "test-cases.md").write_text("""# Test Cases

## Test Suite Overview
| Metric | Value |
|--------|-------|
| Total | 5 |

### TC-001: Test 1
- **Status:** ✅

### TC-002: Test 2
- **Status:** ✅

### TC-003: Test 3
- **Status:** ✅

### TC-004: Test 4
- **Status:** ✅

### TC-005: Test 5
- **Status:** ✅
""", encoding="utf-8")

            (tmp_path / "changelog.md").write_text("""# Changelog

## [v1.0.0] — 2026-01-01
Initial version.
""", encoding="utf-8")

            # 1. Валидация
            result = validate_prompt(tmp_path)
            assert result.status in ("pass", "warn")

            # 2. Сбор метрик
            metrics = collect_metrics(tmp_path)
            assert metrics.name == tmp_path.name

            # 3. Quality gate
            issues = check_quality_gate(metrics)
            assert isinstance(issues, list)

    def test_full_pipeline_invalid_prompt(self):
        """Невалидный промпт не проходит валидацию."""
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "prompt.md").write_text("", encoding="utf-8")

            result = validate_prompt(tmp_path)
            assert result.status == "fail"

    def test_json_report_generation(self):
        """Генерация JSON отчёта."""
        metrics = [
            PromptMetrics(
                name="test-role",
                test_pass_rate=100.0,
                latency_p50=5.0,
                quality_avg=4.5,
                quality_count=3,
            ),
        ]
        issues = [
            Issue(severity="warning", prompt_name="test-role", metric="quality",
                  message="Low quality", recommendation="Fix"),
        ]

        report = generate_json_report(metrics, issues)
        data = json.loads(report)

        assert "prompts" in data
        assert "issues" in data
        assert "summary" in data
        assert data["prompts"][0]["name"] == "test-role"

    def test_md_report_generation(self):
        """Генерация Markdown отчёта."""
        metrics = [
            PromptMetrics(name="test-role", test_pass_rate=100.0, latency_p50=5.0),
        ]
        issues = []

        report = generate_md_report(metrics, issues)
        assert "# Prompt Library Report" in report
        assert "test-role" in report

    def test_html_report_generation(self):
        """Генерация HTML отчёта."""
        metrics = [
            PromptMetrics(name="test-role", test_pass_rate=100.0, latency_p50=5.0),
        ]
        issues = []

        report = generate_html_report(metrics, issues)
        assert "<!DOCTYPE html>" in report
        assert "test-role" in report
        assert "Prompt Library Dashboard" in report

    def test_quality_gate_critical(self):
        """Quality gate с критическими нарушениями."""
        metrics = PromptMetrics(
            name="bad-role",
            test_pass_rate=50.0,
            latency_p50=40.0,
            quality_avg=2.0,
            quality_count=5,
        )
        issues = check_quality_gate(metrics)

        severities = [i.severity for i in issues]
        assert "critical" in severities

    def test_quality_gate_healthy(self):
        """Quality gate без нарушений."""
        metrics = PromptMetrics(
            name="good-role",
            test_pass_rate=100.0,
            latency_p50=5.0,
            quality_avg=4.5,
            quality_count=3,
            status="validated",
        )
        issues = check_quality_gate(metrics)
        assert issues == []

    def test_summary_computation(self):
        """Вычисление сводной статистики."""
        metrics = [
            PromptMetrics(name="role1", test_pass_rate=100.0, latency_p50=5.0),
            PromptMetrics(name="role2", test_pass_rate=50.0, latency_p50=40.0),
        ]
        issues = [
            Issue(severity="critical", prompt_name="role2", metric="test",
                  message="Low", recommendation="Fix"),
            Issue(severity="warning", prompt_name="role2", metric="latency",
                  message="High", recommendation="Optimize"),
        ]

        from report.utils import compute_summary
        summary = compute_summary(metrics, issues)

        assert summary["total_prompts"] == 2
        assert summary["critical_issues"] == 1
        assert summary["warning_issues"] == 1
        assert summary["healthy"] == 1  # только role1


class TestEdgeCases:
    """Тесты граничных случаев."""

    def test_empty_metrics_list(self):
        """Пустой список метрик."""
        report = generate_json_report([], [])
        data = json.loads(report)
        assert data["prompts"] == []
        assert data["summary"]["total_prompts"] == 0

    def test_empty_issues_list(self):
        """Пустой список проблем."""
        metrics = [PromptMetrics(name="test")]
        report = generate_json_report(metrics, [])
        data = json.loads(report)
        assert data["issues"] == []