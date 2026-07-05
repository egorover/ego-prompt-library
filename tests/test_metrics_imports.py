"""Unit tests for metrics/_imports.py fallback import mechanism."""

from pathlib import Path



class TestMetricsImports:
    """Тесты для scripts/metrics/_imports.py."""

    def test_import_all_exports(self):
        """Все экспортируемые имена доступны."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "metrics_imports",
            SCRIPTS_DIR / "metrics" / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        expected = ["discover_prompts", "get_logger", "parse_status", "read_file"]
        for name in expected:
            assert hasattr(mod, name), f"Missing export: {name}"

    def test_get_logger_returns_logger(self):
        """get_logger возвращает logger объект."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "metrics_imports",
            SCRIPTS_DIR / "metrics" / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        logger = mod.get_logger("test_module")
        assert logger is not None
        assert hasattr(logger, "info")

    def test_discover_prompts_returns_list(self):
        """discover_prompts возвращает список."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "metrics_imports",
            SCRIPTS_DIR / "metrics" / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        result = mod.discover_prompts(Path("/nonexistent"))
        assert isinstance(result, list)

    def test_parse_status_returns_string(self):
        """parse_status возвращает строку."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "metrics_imports",
            SCRIPTS_DIR / "metrics" / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        result = mod.parse_status("## Metadata\n| Status | validated |\n")
        assert isinstance(result, str)


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
