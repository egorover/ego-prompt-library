"""Unit tests for CLI entry points via subprocess.

Skipped on Windows due to [WinError 10106] — Windows named pipe limitation.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


@pytest.mark.skipif(sys.platform == "win32", reason="Windows subprocess pipe limitation [WinError 10106]")
class TestReportCli:
    """Тесты CLI report_cli.py через subprocess."""

    def test_json_output_no_prompts(self, tmp_path: Path):
        """report_cli --json без промптов — пустой результат."""
        project_root = tmp_path / "project"
        project_root.mkdir(parents=True)
        (project_root / "prompts").mkdir()

        import shutil

        src = SCRIPTS_DIR
        dst = project_root / "scripts"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        result = subprocess.run(
            [sys.executable, str(project_root / "scripts" / "report_cli.py"), "--json"],
            cwd=project_root,
            capture_output=True,
            text=True,
            env={"PYTHONPATH": str(project_root)},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["prompts"] == []
        assert data["summary"]["total_prompts"] == 0

    def test_json_output_with_prompts(self, tmp_path: Path):
        """report_cli --json с промптом — содержит метрики."""
        project_root = tmp_path / "project"
        project_root.mkdir(parents=True)
        prompts_dir = project_root / "prompts"
        prompts_dir.mkdir()
        prompt_dir = prompts_dir / "test-role"
        prompt_dir.mkdir()

        (prompt_dir / "prompt.md").write_text(
            "## 1. Identity & Purpose\n## 2. Context & Domain\n## 3. Decision Framework\n"
            "## 4. Interaction Rules\n## 5. Output Format\n## 6. Anti-Patterns\n## 7. Quick Reference\n",
            encoding="utf-8",
        )
        (prompt_dir / "card.md").write_text(
            "## Metadata\n| Name | test-role | Version | v1.0 | Status | validated | Author | dev | Created | 2026-01-01 | Updated | 2026-06-01 | Category | test |\n"
            "## Description\nTest\n## Input / Output\nTest\n## Scope & Boundaries\nTest\n"
            "## Constraints & Anti-Patterns\nTest\n## Usage Examples\nTest\n"
            "## Validation Status\nTest\n## Related Files\nTest\n",
            encoding="utf-8",
        )
        (prompt_dir / "test-cases.md").write_text(
            "### TC-001: Test 1\n- **Status:** ✅\n### TC-002: Test 2\n- **Status:** ✅\n",
            encoding="utf-8",
        )
        (prompt_dir / "changelog.md").write_text("## [v1.0.0] — 2026-06-01\n", encoding="utf-8")

        import shutil

        src = SCRIPTS_DIR
        dst = project_root / "scripts"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        result = subprocess.run(
            [sys.executable, str(project_root / "scripts" / "report_cli.py"), "--json"],
            cwd=project_root,
            capture_output=True,
            text=True,
            env={"PYTHONPATH": str(project_root)},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert len(data["prompts"]) == 1
        assert data["prompts"][0]["name"] == "test-role"
        assert data["prompts"][0]["test_pass_rate"] == 100.0


@pytest.mark.skipif(sys.platform == "win32", reason="Windows subprocess pipe limitation [WinError 10106]")
class TestMetricsCollector:
    """Тесты для scripts/metrics-collector.py."""

    def test_delegates_to_main_module(self, tmp_path: Path):
        """metrics-collector.py вызывает metrics.__main__.main()."""
        project_root = tmp_path / "project"
        project_root.mkdir(parents=True)
        (project_root / "prompts").mkdir()

        import shutil

        src = SCRIPTS_DIR
        dst = project_root / "scripts"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        result = subprocess.run(
            [sys.executable, str(project_root / "scripts" / "metrics-collector.py"), "--json"],
            cwd=project_root,
            capture_output=True,
            text=True,
            env={"PYTHONPATH": str(project_root)},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "No prompts found" in result.stdout or "WARN" in result.stdout

    def test_module_entry_point(self, tmp_path: Path):
        """python -m scripts.metrics работает."""
        project_root = tmp_path / "project"
        project_root.mkdir(parents=True)
        (project_root / "prompts").mkdir()

        import shutil

        src = SCRIPTS_DIR
        dst = project_root / "scripts"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        result = subprocess.run(
            [sys.executable, "-m", "scripts.metrics", "--json"],
            cwd=project_root,
            capture_output=True,
            text=True,
            env={"PYTHONPATH": str(project_root)},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
