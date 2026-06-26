#!/usr/bin/env python3
"""
CI-скрипт для GitHub Actions.

Используется в .github/workflows/prompt-ci.yml
Выполняет строгую валидацию всех промптов через validate.py.
"""

import sys
from pathlib import Path

from rich.console import Console

from _imports import (
    discover_prompts,
    get_logger,
)
from validate import validate_prompt

logger = get_logger(__name__)
console = Console()


def main() -> None:
    """CI entry point — validate all prompts."""
    from config import init

    init()

    library_root = Path(__file__).parent.parent
    prompts = discover_prompts(library_root)

    if not prompts:
        console.print("[WARN] No prompts found. Nothing to validate.", style="yellow")
        sys.exit(0)

    all_passed = True
    for prompt_dir in prompts:
        result = validate_prompt(prompt_dir, strict=True)

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
