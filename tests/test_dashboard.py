"""Unit tests for metrics dashboard updater."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from metrics.dashboard import (
    _build_trend_rows,
    _get_month_names,
    update_dashboard,
)


@pytest.fixture
def sample_metrics():
    """Создаёт мок PromptMetrics для тестов."""
    m = MagicMock()
    m.name = "test-prompt"
    m.usage_count = 42
    m.test_pass_rate = 98.5
    m.latency_p50 = 12.3
    m.quality_avg = 4.5
    m.quality_count = 3
    m.changes_this_month = 1
    m.open_issues = 0
    return m


# ── _get_month_names ────────────────────────────────────────────────

def test_get_month_names_returns_three():
    months = _get_month_names()
    assert len(months) == 3
    # Формат YYYY-MM
    for m in months:
        parts = m.split("-")
        assert len(parts) == 2
        assert len(parts[0]) == 4
        assert len(parts[1]) == 2


# ── _build_trend_rows ───────────────────────────────────────────────

def test_build_trend_rows_current_month_populated(sample_metrics):
    months = ["2025-01", "2025-02", "2025-03"]
    rows = _build_trend_rows(sample_metrics, months)
    assert len(rows) == 3
    # Последняя строка (текущий месяц) должна содержать данные
    assert str(sample_metrics.usage_count) in rows[-1]
    assert str(sample_metrics.test_pass_rate) in rows[-1]


def test_build_trend_rows_previous_months_dashes(sample_metrics):
    months = ["2025-01", "2025-02", "2025-03"]
    rows = _build_trend_rows(sample_metrics, months)
    # Первые две строки — прочерки
    for row in rows[:2]:
        assert "|" in row
        assert "—" in row


# ── update_dashboard ────────────────────────────────────────────────

class TestUpdateDashboard:
    """Тесты функции update_dashboard."""

    def test_skips_when_no_dashboard_file(self, tmp_path: Path, sample_metrics):
        prompt_dir = tmp_path / "my-prompt"
        prompt_dir.mkdir()
        # metrics/ существует, но dashboard.md нет
        (prompt_dir / "metrics").mkdir()

        update_dashboard(sample_metrics, prompt_dir)
        # Не должно упасть — просто пропускает

    def test_updates_dashboard_content(self, tmp_path: Path, sample_metrics):
        prompt_dir = tmp_path / "my-prompt"
        prompt_dir.mkdir()
        metrics_dir = prompt_dir / "metrics"
        metrics_dir.mkdir()
        dashboard_path = metrics_dir / "dashboard.md"
        dashboard_path.write_text("existing content", encoding="utf-8")

        update_dashboard(sample_metrics, prompt_dir)

        new_content = dashboard_path.read_text(encoding="utf-8")
        assert f"Dashboard: {sample_metrics.name}" in new_content
        assert str(sample_metrics.usage_count) in new_content
        assert f"{sample_metrics.test_pass_rate}%" in new_content
        assert "Тренд" in new_content

    def test_dashboard_green_status_high_pass_rate(self, tmp_path: Path, sample_metrics):
        sample_metrics.test_pass_rate = 100.0
        sample_metrics.latency_p50 = 10.0
        sample_metrics.quality_avg = 4.5
        sample_metrics.open_issues = 1

        prompt_dir = tmp_path / "my-prompt"
        prompt_dir.mkdir()
        (prompt_dir / "metrics").mkdir()
        (prompt_dir / "metrics" / "dashboard.md").write_text("", encoding="utf-8")

        update_dashboard(sample_metrics, prompt_dir)

        content = (prompt_dir / "metrics" / "dashboard.md").read_text(encoding="utf-8")
        assert "🟢" in content  # зелёные статусы

    def test_dashboard_red_status_low_metrics(self, tmp_path: Path, sample_metrics):
        sample_metrics.test_pass_rate = 50.0
        sample_metrics.latency_p50 = 45.0
        sample_metrics.quality_avg = 1.5
        sample_metrics.open_issues = 10

        prompt_dir = tmp_path / "my-prompt"
        prompt_dir.mkdir()
        (prompt_dir / "metrics").mkdir()
        (prompt_dir / "metrics" / "dashboard.md").write_text("", encoding="utf-8")

        update_dashboard(sample_metrics, prompt_dir)

        content = (prompt_dir / "metrics" / "dashboard.md").read_text(encoding="utf-8")
        assert "🔴" in content  # красные статусы

    def test_dashboard_yellow_latency(self, tmp_path: Path, sample_metrics):
        sample_metrics.latency_p50 = 20.0  # между 15 и 30
        sample_metrics.test_pass_rate = 100.0
        sample_metrics.quality_avg = 5.0
        sample_metrics.open_issues = 0

        prompt_dir = tmp_path / "my-prompt"
        prompt_dir.mkdir()
        (prompt_dir / "metrics").mkdir()
        (prompt_dir / "metrics" / "dashboard.md").write_text("", encoding="utf-8")

        update_dashboard(sample_metrics, prompt_dir)

        content = (prompt_dir / "metrics" / "dashboard.md").read_text(encoding="utf-8")
        assert "🟡" in content  # жёлтый для latency

    def test_dashboard_no_quality(self, tmp_path: Path, sample_metrics):
        sample_metrics.quality_count = 0
        sample_metrics.quality_avg = 0.0

        prompt_dir = tmp_path / "my-prompt"
        prompt_dir.mkdir()
        (prompt_dir / "metrics").mkdir()
        (prompt_dir / "metrics" / "dashboard.md").write_text("", encoding="utf-8")

        update_dashboard(sample_metrics, prompt_dir)

        content = (prompt_dir / "metrics" / "dashboard.md").read_text(encoding="utf-8")
        assert "—" in content  # прочерк для quality

    def test_dashboard_writes_utf8(self, tmp_path: Path, sample_metrics):
        """Контент должен быть валидным UTF-8."""
        prompt_dir = tmp_path / "my-prompt"
        prompt_dir.mkdir()
        (prompt_dir / "metrics").mkdir()
        (prompt_dir / "metrics" / "dashboard.md").write_text("", encoding="utf-8")

        update_dashboard(sample_metrics, prompt_dir)

        # Перечитываем как UTF-8 — не должно raise
        content = (prompt_dir / "metrics" / "dashboard.md").read_text(encoding="utf-8")
        assert len(content) > 0
