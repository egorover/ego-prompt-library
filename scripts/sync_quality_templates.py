#!/usr/bin/env python3
"""
Script to synchronize quality.md templates across all prompt projects.
Ensures consistent rating format: Relevance, Completeness, Structure, Value + Context.
"""

import sys
from pathlib import Path

TEMPLATE = """\
# Quality Ratings: {project_name}

## Quality Log

| Date | User | Relevance | Completeness | Structure | Value | Scenario | Notes | Avg |
|------|------|-----------|--------------|-----------|-------|----------|-------|-----|

> Оценивай после каждого использования: 1 (плохо) — 5 (отлично).
> - **Relevance** — насколько ответ релевантен запросу
> - **Completeness** — полнота решения
> - **Structure** — читаемость и структура кода
> - **Value** — практическая польза
> - **Scenario** — краткое описание задачи

## Summary

- **Average Rating:** —
- **Total Ratings:** 0
- **Trend:** —
"""

ROOT_DIR = Path(__file__).parent.parent
METRICS_PATTERN = ROOT_DIR / "prompts" / "**" / "metrics" / "quality.md"


def extract_project_name(file_path: Path) -> str:
    """Extract project name from path (e.g., prompts/python-dev/metrics/quality.md -> python-dev)."""
    try:
        return file_path.parts[file_path.parts.index("prompts") + 1]
    except ValueError:
        return "unknown"


def sync_quality_file(file_path: Path) -> None:
    """Update or create quality.md with the unified template."""
    project_name = extract_project_name(file_path)
    content = TEMPLATE.format(project_name=project_name)
    
    file_path.write_text(content, encoding="utf-8")
    print(f"[OK] Synced: {file_path}")


def main() -> None:
    prompts_dir = ROOT_DIR / "prompts"
    quality_files = [f for f in prompts_dir.rglob("quality.md") if "metrics" in str(f.parent)]
    
    if not quality_files:
        print("[WARN] No quality.md files found under prompts/**/metrics/")
        return

    for q_file in quality_files:
        sync_quality_file(q_file)
    
    print(f"\n[TOTAL] Synced: {len(quality_files)} files")


if __name__ == "__main__":
    main()
