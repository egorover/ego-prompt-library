"""Unit tests for report generators."""

from scripts.metrics.models import PromptMetrics, Issue
from scripts.report.json_report import generate_json_report
from scripts.report.md_report import generate_md_report
from scripts.report.html_report import generate_html_report
from scripts.report.utils import compute_summary


def test_compute_summary_empty():
    summary = compute_summary([], [])
    assert summary["total_prompts"] == 0
    assert summary["healthy"] == 0
    assert summary["critical_issues"] == 0


def test_compute_summary_healthy():
    metrics = [
        PromptMetrics(name="role1", test_pass_rate=100.0, latency_p50=5.0, status="validated"),
    ]
    summary = compute_summary(metrics, [])
    assert summary["total_prompts"] == 1
    assert summary["healthy"] == 1


def test_compute_summary_with_issues():
    metrics = [
        PromptMetrics(name="role1", test_pass_rate=100.0, latency_p50=5.0),
    ]
    issues = [
        Issue(severity="critical", prompt_name="role1", metric="quality", message="Low quality", recommendation="Fix"),
        Issue(
            severity="warning", prompt_name="role1", metric="latency", message="High latency", recommendation="Optimize"
        ),
        Issue(severity="info", prompt_name="role1", metric="status", message="Draft", recommendation="Validate"),
    ]
    summary = compute_summary(metrics, issues)
    assert summary["critical_issues"] == 1
    assert summary["warning_issues"] == 1
    assert summary["info_issues"] == 1


def test_generate_json_report():
    metrics = [
        PromptMetrics(name="test-role", test_pass_rate=100.0, latency_p50=5.0, quality_avg=4.5, quality_count=3),
    ]
    report = generate_json_report(metrics, [])
    assert '"test-role"' in report
    assert '"test_pass_rate": 100.0' in report


def test_generate_json_report_strict():
    metrics = [PromptMetrics(name="test-role")]
    issues = [
        Issue(severity="critical", prompt_name="test-role", metric="q", message="bad", recommendation="fix"),
        Issue(severity="info", prompt_name="test-role", metric="q", message="info", recommendation="ok"),
    ]
    report = generate_json_report(metrics, issues, strict=True)
    assert '"critical"' in report
    assert '"info"' not in report


def test_generate_md_report():
    metrics = [
        PromptMetrics(name="test-role", test_pass_rate=100.0, latency_p50=5.0),
    ]
    report = generate_md_report(metrics, [])
    assert "# Prompt Library Report" in report
    assert "## Per-Prompt" in report
    assert "test-role" in report


def test_generate_md_report_with_issues():
    metrics = [PromptMetrics(name="test-role")]
    issues = [
        Issue(
            severity="critical", prompt_name="test-role", metric="quality", message="Low quality", recommendation="Fix"
        ),
    ]
    report = generate_md_report(metrics, issues)
    assert "## Issues" in report
    assert "[CRITICAL]" in report


def test_generate_html_report():
    metrics = [
        PromptMetrics(name="test-role", test_pass_rate=100.0, latency_p50=5.0, status="validated"),
    ]
    report = generate_html_report(metrics, [])
    assert "<!DOCTYPE html>" in report
    assert "test-role" in report
    assert "badge-green" in report


def test_generate_html_report_with_issues():
    metrics = [PromptMetrics(name="test-role")]
    issues = [
        Issue(severity="critical", prompt_name="test-role", metric="quality", message="Low", recommendation="Fix"),
    ]
    report = generate_html_report(metrics, issues)
    assert "issue-critical" in report
