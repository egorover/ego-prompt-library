"""Unit tests for config.py — init() and Config class."""

from unittest.mock import patch

import pytest

from config import (
    Config,
    MetricsThresholds,
    _get_config,
    init,
)


class TestMetricsThresholds:
    """Tests for MetricsThresholds Pydantic model."""

    def test_default_thresholds(self):
        t = MetricsThresholds()
        assert t.test_pass_rate_warning == 95.0
        assert t.test_pass_rate_critical == 80.0
        assert t.latency_p50_warning == 15.0
        assert t.latency_p50_critical == 30.0
        assert t.quality_avg_warning == 4.0
        assert t.quality_avg_critical == 3.0
        assert t.changes_per_month_warning == 2

    def test_custom_thresholds(self):
        t = MetricsThresholds(
            test_pass_rate_warning=90.0,
            latency_p50_warning=20.0,
        )
        assert t.test_pass_rate_warning == 90.0
        assert t.latency_p50_warning == 20.0

    def test_invalid_test_pass_rate_above_100(self):
        with pytest.raises(Exception):
            MetricsThresholds(test_pass_rate_warning=101.0)

    def test_invalid_test_pass_rate_below_0(self):
        with pytest.raises(Exception):
            MetricsThresholds(test_pass_rate_warning=-1.0)

    def test_invalid_latency_below_0(self):
        with pytest.raises(Exception):
            MetricsThresholds(latency_p50_warning=-1.0)

    def test_quality_avg_bounds(self):
        t = MetricsThresholds(quality_avg_warning=4.0, quality_avg_critical=3.0)
        assert t.quality_avg_warning == 4.0
        assert t.quality_avg_critical == 3.0

    def test_invalid_quality_avg_below_1(self):
        with pytest.raises(Exception):
            MetricsThresholds(quality_avg_critical=0.5)

    def test_invalid_quality_avg_above_5(self):
        with pytest.raises(Exception):
            MetricsThresholds(quality_avg_warning=5.5)


class TestConfig:
    """Tests for Config Pydantic BaseSettings."""

    def test_default_config(self):
        cfg = Config()
        assert cfg.environment == "development"
        assert cfg.log_level == "INFO"
        assert cfg.python_io_encoding == "utf-8"
        assert cfg.is_development is True
        assert cfg.is_production is False

    def test_production_config(self):
        cfg = Config(environment="production")
        assert cfg.environment == "production"
        assert cfg.is_production is True
        assert cfg.is_development is False

    def test_invalid_environment(self):
        with pytest.raises(Exception):
            Config(environment="staging")

    def test_invalid_log_level(self):
        with pytest.raises(Exception):
            Config(log_level="TRACE")

    def test_project_root_exists(self):
        cfg = Config()
        assert cfg.project_root.exists()

    def test_prompts_dir_not_exists_by_default(self):
        cfg = Config()
        # prompts dir may not exist in test env
        assert cfg.prompts_dir == cfg.project_root / "prompts"

    def test_scripts_dir(self):
        cfg = Config()
        assert cfg.scripts_dir == cfg.project_root / "scripts"

    def test_metrics_thresholds_default(self):
        cfg = Config()
        assert isinstance(cfg.metrics_thresholds, MetricsThresholds)
        assert cfg.metrics_thresholds.test_pass_rate_warning == 95.0


class TestGetConfig:
    """Tests for _get_config() lazy singleton."""

    def test_get_config_creates_instance(self):
        cfg = _get_config()
        assert isinstance(cfg, Config)

    def test_get_config_returns_same_instance(self):
        cfg1 = _get_config()
        cfg2 = _get_config()
        assert cfg1 is cfg2


class TestInit:
    """Tests for init() function."""

    def setup_method(self):
        """Reset _initialized before each test."""
        import config

        config._initialized = False

    def test_init_called_once(self):
        """init() should be idempotent — only first call has effect."""
        with (
            patch("config.load_dotenv") as mock_load,
            patch("config.configure_console_encoding") as mock_console,
            patch("config.configure_logging") as mock_logging,
        ):
            init()
            mock_load.assert_called_once()
            mock_console.assert_called_once()
            mock_logging.assert_called_once()

    def test_init_idempotent(self):
        """Second call to init() should not re-execute side effects."""
        with (
            patch("config.load_dotenv") as mock_load,
            patch("config.configure_console_encoding") as mock_console,
            patch("config.configure_logging") as mock_logging,
        ):
            # Reset _initialized flag to simulate real scenario
            import config

            config._initialized = False

            init()
            mock_load.assert_called_once()
            mock_console.assert_called_once()
            mock_logging.assert_called_once()

            # Reset counters
            mock_load.reset_mock()
            mock_console.reset_mock()
            mock_logging.reset_mock()

            # Second call should NOT re-execute
            init()
            mock_load.assert_not_called()
            mock_console.assert_not_called()
            mock_logging.assert_not_called()

    def test_init_no_side_effects_on_import(self):
        """Importing config should not trigger load_dotenv, logging, or encoding."""
        # Re-import to simulate fresh import
        import sys

        # Remove cached modules
        modules_to_remove = [m for m in sys.modules if m.startswith("config") or m == "dotenv"]
        for m in modules_to_remove:
            del sys.modules[m]

        # Now import fresh
        with (
            patch("config.load_dotenv") as mock_load,
            patch("config.configure_console_encoding") as mock_console,
            patch("config.configure_logging") as mock_logging,
        ):
            # Import the fresh module
            from config import init as fresh_init

            # init() should NOT have been called yet
            assert mock_load.call_count == 0
            assert mock_console.call_count == 0
            assert mock_logging.call_count == 0

            # Now call init explicitly
            fresh_init()
            mock_load.assert_called_once()
