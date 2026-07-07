"""Unit tests for _imports.py fallback import mechanism."""

from pathlib import Path


class TestSharedImports:
    """Тесты для scripts/_imports.py."""

    def test_import_all_exports(self):
        """Все экспортируемые имена доступны."""
        # Импортируем как standalone модуль (как это делают скрипты)
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "_imports",
            SCRIPTS_DIR / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        expected = [
            "REQUIRED_CARD_SECTIONS",
            "REQUIRED_FILES",
            "REQUIRED_METADATA_FIELDS",
            "REQUIRED_PROMPT_SECTIONS",
            "VALID_STATUSES",
            "ValidationResult",
            "discover_prompts",
            "get_logger",
            "parse_status",
            "read_file",
        ]
        for name in expected:
            assert hasattr(mod, name), f"Missing export: {name}"

    def test_required_files_constants(self):
        """REQUIRED_FILES содержит 4 обязательных файла."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "_imports",
            SCRIPTS_DIR / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        assert len(mod.REQUIRED_FILES) == 4
        assert "prompt.md" in mod.REQUIRED_FILES
        assert "card.md" in mod.REQUIRED_FILES

    def test_valid_statuses(self):
        """VALID_STATUSES содержит 4 статуса."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "_imports",
            SCRIPTS_DIR / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        assert mod.VALID_STATUSES == {"draft", "testing", "validated", "deprecated"}

    def test_validation_result_dataclass(self):
        """ValidationResult — dataclass с is_valid и to_dict."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "_imports",
            SCRIPTS_DIR / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        vr = mod.ValidationResult(prompt_dir="test")
        assert vr.is_valid is True
        assert vr.to_dict() == {"prompt_dir": "test", "status": "pass", "errors": [], "warnings": []}

    def test_parse_status_validated(self):
        """parse_status извлекает статус validated."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "_imports",
            SCRIPTS_DIR / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        card = "## Metadata\n| Status | validated |\n"
        assert mod.parse_status(card) == "validated"

    def test_parse_status_unknown(self):
        """parse_status возвращает unknown для невалидного статуса."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "_imports",
            SCRIPTS_DIR / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        card = "## Metadata\n| Status | invalid |\n"
        assert mod.parse_status(card) == "unknown"

    def test_discover_prompts_empty(self):
        """discover_prompts возвращает пустой список если нет prompts/."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "_imports",
            SCRIPTS_DIR / "_imports.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        result = mod.discover_prompts(Path("/nonexistent"))
        assert result == []


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
