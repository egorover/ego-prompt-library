#!/usr/bin/env python3
"""
CI-скрипт для GitHub Actions.

Используется в .github/workflows/prompt-ci.yml
"""

import sys
from pathlib import Path

# Добавляем scripts в path для импорта validate
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from validate import discover_prompts, validate_prompt


def main():
    library_root = Path(__file__).parent.parent
    prompts = discover_prompts(library_root)

    if not prompts:
        print("⚠️  No prompts found. Nothing to validate.")
        sys.exit(0)

    all_passed = True
    for prompt_dir in prompts:
        result = validate_prompt(prompt_dir, strict=True)
        if not result.is_valid:
            all_passed = False
            print(f"❌ {result.prompt_dir}")
            for error in result.errors:
                print(f"   {error}")
            for warning in result.warnings:
                print(f"   ⚠️  {warning}")

    if all_passed:
        print(f"✅ All {len(prompts)} prompt(s) validated successfully.")
    else:
        print(f"\n❌ Validation failed for some prompts.")
        sys.exit(1)


if __name__ == "__main__":
    main()
