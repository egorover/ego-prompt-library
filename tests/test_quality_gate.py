"""Unit tests for quality gate checks."""

from metrics.models import PromptMetrics
from metrics.quality_gate import check_quality_gate
from metrics.gate_checks import check_test_pass_rate, check_quality, check_latency

_DEFAULT_THRESHOLDS = {
    "test_pass_rate": {"warning": 95.0, "critical": 80.0},
    "latency_p50": {"warning": 15.0, "critical": 30.0},
    "quality_avg": {"warning": 4.0, "critical": 3.0},
    "changes_per_month": {"warning": 2},
}


def test_healthy_prompt_no_issues():
    metrics = PromptMetrics(
        name="test-role",
        test_pass_rate=100.0,
        latency_p50=5.0,
        quality_avg=4.5,
        quality_count=3,
        changes_this_month=1,
        status="validated",
    )
    issues = check_quality_gate(metrics)
    assert issues == []


def test_critical_test_pass_rate():
    metrics = PromptMetrics(name="test-role", test_pass_rate=70.0)
    issues = check_test_pass_rate(metrics, _DEFAULT_THRESHOLDS)
    assert len(issues) == 1
    assert issues[0].severity == "critical"
    assert issues[0].metric == "test_pass_rate"


def test_warning_quality():
    metrics = PromptMetrics(name="test-role", quality_avg=3.5, quality_count=2)
    issues = check_quality(metrics, _DEFAULT_THRESHOLDS)
    assert len(issues) == 1
    assert issues[0].severity == "warning"


def test_critical_latency():
    metrics = PromptMetrics(name="test-role", latency_p50=35.0)
    issues = check_latency(metrics, _DEFAULT_THRESHOLDS)
    assert len(issues) == 1
    assert issues[0].severity == "critical"


def test_draft_status_warning():
    metrics = PromptMetrics(name="test-role", status="draft")
    issues = check_quality_gate(metrics)
    assert any(i.metric == "status" and i.severity == "warning" for i in issues)
