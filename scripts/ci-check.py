#!/usr/bin/env python3
"""
CI-скрипт для GitHub Actions.

Используется в .github/workflows/prompt-ci.yml
Выполняет строгую валидацию всех промптов.
"""

import sys
from pathlib import Path

from rich.console import Console

from _imports import (
    discover_prompts,
    get_logger,
    ValidationResult,
)

logger = get_logger(__name__)
console = Console()


def main() -> None:
    library_root = Path(__file__).parent.parent
    prompts = discover_prompts(library_root)

    if not prompts:
        console.print("[WARN] No prompts found. Nothing to validate.", style="yellow")
        sys.exit(0)

    all_passed = True
    for prompt_dir in prompts:
        result = ValidationResult(prompt_dir=prompt_dir.name)

        # Inline validation for CI (avoid circular imports)
        try:
            from _imports import read_file, REQUIRED_FILES, REQUIRED_PROMPT_SECTIONS, REQUIRED_CARD_SECTIONS, REQUIRED_METADATA_FIELDS, VALID_STATUSES
            import re

            # Check files
            for filename in REQUIRED_FILES:
                filepath = prompt_dir / filename
                if not filepath.exists():
                    result.errors.append(f"Missing required file: {filename}")
                elif not read_file(filepath).strip():
                    result.errors.append(f"File is empty: {filename}")

            if result.errors:
                result.status = "fail"
            else:
                prompt_content = read_file(prompt_dir / "prompt.md")
                for section in REQUIRED_PROMPT_SECTIONS:
                    if section not in prompt_content:
                        result.errors.append(f"Missing section in prompt.md: {section}")

                card_content = read_file(prompt_dir / "card.md")
                for section in REQUIRED_CARD_SECTIONS:
                    if section not in card_content:
                        result.errors.append(f"Missing section in card.md: {section}")

                metadata_content = ""
                in_metadata = False
                for line in card_content.split("\n"):
                    if "## Metadata" in line:
                        in_metadata = True
                        continue
                    if in_metadata and line.startswith("##"):
                        break
                    if in_metadata:
                        metadata_content += line + "\n"

                for field_name in ["Name", "Version", "Author", "Status", "Created", "Updated", "Category"]:
                    if f"| {field_name}" not in metadata_content:
                        result.errors.append(f"Missing metadata field: {field_name}")

                if not any(status in metadata_content for status in VALID_STATUSES):
                    result.errors.append("No valid status found in metadata")

                test_content = read_file(prompt_dir / "test-cases.md")
                tc_count = len(re.findall(r"TC-\d+:", test_content))
                if tc_count == 0:
                    result.errors.append("No test cases found")
                elif tc_count < 5:
                    result.warnings.append(f"Only {tc_count} test cases (recommended: minimum 5)")

                changelog_content = read_file(prompt_dir / "changelog.md")
                if not re.findall(r"## \[v?\d+\.\d+\.\d+\]", changelog_content):
                    result.errors.append("No versioned entries found in changelog")

        except Exception as e:
            logger.error("Error validating %s: %s", prompt_dir.name, e, exc_info=True)
            result.errors.append(f"Validation error: {e}")
            result.status = "fail"

        if not result.is_valid:
            all_passed = False
            console.print(f"[red][FAIL][/red] {result.prompt_dir}")
            for error in result.errors:
                console.print(f"   {error}")
            for warning in result.warnings:
                console.print(f"   [yellow][WARN][/yellow] {warning}")

    if all_passed:
        console.print(f"[green][OK] All {len(prompts)} prompt(s) validated successfully.[/green]")
    else:
        console.print("\n[red][FAIL] Validation failed for some prompts.[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()