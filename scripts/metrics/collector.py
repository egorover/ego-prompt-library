#!/usr/bin/env python3
"""
Collector — сбор метрик для одного промпта.

Извлекает метаданные, считает usage, changes, собирает все метрики.

Использует:
- models.PromptMetrics
- parsers (parse_test_results, parse_latency, parse_quality)
- shared (read_file, parse_status)
"""

import re
from datetime import date
from pathlib import Path

from shared import read_file, parse_status
from metrics.parsers import parse_latency, parse_quality, parse_test_results
from metrics.models import PromptMetrics


def parse_metadata(card_content: str) -> dict:
    """Извлекает метаданные из card.md секции Metadata."""
    metadata: dict[str, str] = {}
    in_metadata = False

    for line in card_content.split("\n"):
        if "## Metadata" in line:
            in_metadata = True
            continue
        if in_metadata and line.startswith("##"):
            break
        if in_metadata:
            match = re.match(r"\|\s*(\w+)\s*\|\s*([^|]+?)\s*\|", line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                if key in ("Name", "Version", "Status", "Updated", "Author", "Category"):
                    metadata[key] = value

    return metadata


def count_usage(usage_content: str) -> int:
    """Считает количество использований по usage.md entries."""
    count = 0
    for line in usage_content.split("\n"):
        if line.startswith("|") and not line.startswith("| Date"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5 and parts[1] and parts[2]:
                count += 1
    return count


def count_changes_this_month(changelog_content: str) -> int:
    """Считает количество версий за текущий месяц."""
    now = date.today()
    current_month = now.strftime("%Y-%m")

    versions = re.findall(
        r"## \[v?\d+\.\d+\.\d+\].*?(\d{4}-\d{2}-\d{2})",
        changelog_content,
        re.DOTALL,
    )
    return sum(1 for v_date in versions if v_date.startswith(current_month))


def collect_metrics(prompt_dir: Path) -> PromptMetrics:
    """Собирает все метрики для одного промпта."""
    name = prompt_dir.name
    metrics = PromptMetrics(name=name)

    # Card
    card_path = prompt_dir / "card.md"
    if card_path.exists():
        card_content = read_file(card_path)
        metadata = parse_metadata(card_content)
        metrics.version = metadata.get("Version", "")
        metrics.status = parse_status(card_content)

    # Changelog + usage
    changelog_path = prompt_dir / "changelog.md"
    if changelog_path.exists():
        changelog_content = read_file(changelog_path)
        metrics.changes_this_month = count_changes_this_month(changelog_content)

    # Usage
    usage_path = prompt_dir / "metrics" / "usage.md"
    if usage_path.exists():
        metrics.usage_count = count_usage(read_file(usage_path))

    # Test cases
    test_path = prompt_dir / "test-cases.md"
    if test_path.exists():
        test_content = read_file(test_path)
        passed, total = parse_test_results(test_content)
        metrics.test_passed = passed
        metrics.test_total = total
        metrics.test_pass_rate = round((passed / total * 100), 1) if total > 0 else 100.0

    # Latency
    latency_path = prompt_dir / "metrics" / "latency.md"
    if latency_path.exists():
        latency_content = read_file(latency_path)
        metrics.latency_p50, metrics.latency_p95, metrics.latency_p99 = parse_latency(latency_content)

    # Quality
    quality_path = prompt_dir / "metrics" / "quality.md"
    if quality_path.exists():
        quality_content = read_file(quality_path)
        metrics.quality_avg, metrics.quality_count = parse_quality(quality_content)

    return metrics
