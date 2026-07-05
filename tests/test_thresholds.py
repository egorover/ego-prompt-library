"""Unit tests for metrics thresholds loading."""

from unittest.mock import MagicMock, patch

import pytest

from metrics.thresholds import get_metrics_thresholds


class TestMetricsThresholds:
    """Тесты для загрузки порогов quality gate."""

    def test_thresholds_returns_dict(self):
        """get_metrics_thresholds возвращает словарь."""
        thresholds = get_metrics_thresholds()
        assert isinstance(thresholds, dict)

    def test_thresholds_has_all_metrics(self):
        """Все метрики присутствуют в порогах."""
        thresholds = get_metrics_thresholds()
        assert "test_pass_rate" in thresholds
        assert "latency_p50" in thresholds
        assert "quality_avg" in thresholds
        assert "changes_per_month" in thresholds

    def test_thresholds_default_values(self):
        """Значения порогов соответствуют дефолтным."""
        thresholds = get_metrics_thresholds()
        assert thresholds["test_pass_rate"]["warning"] == 95
        assert thresholds["test_pass_rate"]["critical"] == 80
        assert thresholds["latency_p50"]["warning"] == 15
        assert thresholds["latency_p50"]["critical"] == 30
        assert thresholds["quality_avg"]["warning"] == 4.0
        assert thresholds["quality_avg"]["critical"] == 3.0
        assert thresholds["changes_per_month"]["warning"] == 2

    def test_thresholds_from_config(self):
        """Пороги загружаются из config при наличии."""
        mock_thresholds = MagicMock()
        mock_thresholds.test_pass_rate_warning = 90.0
        mock_thresholds.test_pass_rate_critical = 75.0
        mock_thresholds.latency_p50_warning = 20.0
        mock_thresholds.latency_p50_critical = 40.0
        mock_thresholds.quality_avg_warning = 3.5
        mock_thresholds.quality_avg_critical = 2.5
        mock_thresholds.changes_per_month_warning = 3

        mock_cfg = MagicMock()
        mock_cfg.metrics_thresholds = mock_thresholds

        with patch("metrics.thresholds._get_config", return_value=mock_cfg):
            thresholds = get_metrics_thresholds()

        assert thresholds["test_pass_rate"]["warning"] == 90.0
        assert thresholds["test_pass_rate"]["critical"] == 75.0
        assert thresholds["latency_p50"]["warning"] == 20.0
        assert thresholds["quality_avg"]["warning"] == 3.5

    def test_thresholds_fallback_on_config_error(self):
        """При ошибке конфига — используются дефолтные значения."""
        with patch("metrics.thresholds._get_config", side_effect=RuntimeError("Config unavailable")):
            # get_metrics_thresholds должен перехватить RuntimeError и вернуть дефолты
            thresholds = get_metrics_thresholds()

        assert thresholds["test_pass_rate"]["warning"] == 95
        assert thresholds["latency_p50"]["critical"] == 30

    def test_thresholds_fallback_on_none_config(self):
        """При None конфиге — используются дефолтные значения."""
        with patch("metrics.thresholds._get_config", return_value=None):
            thresholds = get_metrics_thresholds()

        assert thresholds["test_pass_rate"]["warning"] == 95

    def test_thresholds_changes_per_month_no_critical(self):
        """changes_per_month не имеет critical порога."""
        thresholds = get_metrics_thresholds()
        assert "critical" not in thresholds["changes_per_month"]
