"""Unit tests for ci-check.py — CI validation entry point."""

import os
import subprocess
import sys
from pathlib import Path


class TestMain:
    """Tests for ci-check.py main() function via subprocess."""

    def test_main_no_prompts(self, tmp_path):
        """When no prompts found, should print warning and exit 0."""
        # Create temp project structure
        project_root = tmp_path / "project"
        project_root.mkdir(parents=True)
        prompts_dir = project_root / "prompts"
        prompts_dir.mkdir()

        # Copy scripts
        import shutil

        src = Path(__file__).parent.parent / "scripts"
        dst = project_root / "scripts"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        # Run ci-check.py
        result = subprocess.run(
            [sys.executable, str(project_root / "scripts" / "ci-check.py")],
            cwd=project_root,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(project_root)},
        )
        assert result.returncode == 0
        assert "No prompts found" in result.stdout

    def test_main_all_prompts_valid(self, tmp_path):
        """When all prompts pass validation, should exit 0."""
        project_root = tmp_path / "project"
        project_root.mkdir(parents=True)
        prompts_dir = project_root / "prompts"
        prompts_dir.mkdir()
        prompt1 = prompts_dir / "valid-prompt"
        prompt1.mkdir()

        # Create required files with proper format
        (prompt1 / "prompt.md").write_text(
            "# 1. Identity & Purpose\n# 2. Context & Domain\n# 3. Decision Framework\n# 4. Interaction Rules\n# 5. Output Format\n# 6. Anti-Patterns\n# 7. Quick Reference\n"
        )
        (prompt1 / "card.md").write_text(
            "## Metadata\n| Name | Test | Version | 1.0 | Status | validated | Author | Dev | Created | 2024-01-01 | Updated | 2024-01-01 | Category | Test |\n## Description\nTest\n## Input / Output\nTest\n## Scope & Boundaries\nTest\n## Constraints & Anti-Patterns\nTest\n## Usage Examples\nTest\n## Validation Status\nTest\n## Related Files\nTest\n"
        )
        (prompt1 / "test-cases.md").write_text(
            "# Test Cases\n## TC-001: Pass\n- [x] Pass\nStatus: Pass\n## TC-002: Pass\n- [x] Pass\nStatus: Pass\n## TC-003: Pass\n- [x] Pass\nStatus: Pass\n## TC-004: Pass\n- [x] Pass\nStatus: Pass\n## TC-005: Pass\n- [x] Pass\nStatus: Pass\n"
        )
        (prompt1 / "changelog.md").write_text("## [v1.0.0] - 2024-01-01\n- Initial release\n")

        # Copy scripts
        import shutil

        src = Path(__file__).parent.parent / "scripts"
        dst = project_root / "scripts"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        # Run ci-check.py
        result = subprocess.run(
            [sys.executable, str(project_root / "scripts" / "ci-check.py")],
            cwd=project_root,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(project_root)},
        )
        assert result.returncode == 0
