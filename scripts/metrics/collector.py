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

from logger import get_logger
from shared import read_file, parse_status
from metrics.parsers import parse_latency, parse_quality, parse_test_results
from metrics.models import PromptMetrics

logger = get_logger(__name__)


def parse_metadata(card_content: str) -> dict[str, str]:
    """Извлекает метаданные из card.md секции Metadata.

    Args:
        card_content: Содержимое card.md.

    Returns:
        Словарь {ключ: значение}.
    """
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
    """Считает количество использований по usage.md entries.

    Парсит строки таблицы, где есть хотя бы 3 непустых поля (кроме заголовка).

    Args:
        usage_content: Содержимое usage.md.

    Returns:
        Количество использований.
    """
    count = 0
    lines = usage_content.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        # Пропускаем заголовок и разделитель
        parts = [p.strip() for p in line.split("|")]
        if i == 0 and any("Date" in p or "Дата" in p for p in parts):
            continue
        if "---" in line:
            continue
        # Считаем строку с данными: минимум 3 непустых поля
        non_empty = [p for p in parts if p and p != "—"]
        if len(non_empty) >= 3:
            count += 1
    return count


def count_changes_this_month(changelog_content: str) -> int:
    """Считает количество версий за текущий месяц.

    Args:
        changelog_content: Содержимое changelog.md.

    Returns:
        Количество версий за текущий месяц.
    """
    now = date.today()
    current_month = now.strftime("%Y-%m")

    try:
        versions = re.findall(
            r"## \[v?\d+\.\d+\.\d+\].*?(\d{4}-\d{2}-\d{2})",
            changelog_content,
            re.DOTALL,
        )
        return sum(1 for v_date in versions if v_date.startswith(current_month))
    except re.error as e:
        logger.error("Regex error in changelog: %s", e)
        return 0


def collect_metrics(prompt_dir: Path) -> PromptMetrics:
    """Собирает все метрики для одного промпта.

    Args:
        prompt_dir: Путь к директории промпта.

    Returns:
        PromptMetrics с заполненными полями.
    """
    logger.info("Collecting metrics for: %s", prompt_dir.name)
    name = prompt_dir.name
    metrics = PromptMetrics(name=name)

    try:
        # Card
        card_path = prompt_dir / "card.md"
        if card_path.exists():
            card_content = read_file(card_path)
            metadata = parse_metadata(card_content)
            metrics.version = metadata.get("Version", "")
            metrics.status = parse_status(card_content)
            logger.debug("Card metadata: version=%s, status=%s", metrics.version, metrics.status)

        # Changelog + usage
        changelog_path = prompt_dir / "changelog.md"
        if changelog_path.exists():
            changelog_content = read_file(changelog_path)
            metrics.changes_this_month = count_changes_this_month(changelog_content)
            logger.debug("Changes this month: %d", metrics.changes_this_month)

        # Usage
        usage_path = prompt_dir / "metrics" / "usage.md"
        if usage_path.exists():
            metrics.usage_count = count_usage(read_file(usage_path))
            logger.debug("Usage count: %d", metrics.usage_count)

        # Test cases
        test_path = prompt_dir / "test-cases.md"
        if test_path.exists():
            test_content = read_file(test_path)
            passed, total = parse_test_results(test_content)
            metrics.test_passed = passed
            metrics.test_total = total
            metrics.test_pass_rate = round((passed / total * 100), 1) if total > 0 else 100.0
            logger.debug("Tests: %d/%d (%.1f%%)", passed, total, metrics.test_pass_rate)

        # Latency
        latency_path = prompt_dir / "metrics" / "latency.md"
        if latency_path.exists():
            latency_content = read_file(latency_path)
            metrics.latency_p50, metrics.latency_p95, metrics.latency_p99 = parse_latency(latency_content)
            logger.debug("Latency: P50=%.1fs, P95=%.1fs, P99=%.1fs", metrics.latency_p50, metrics.latency_p95, metrics.latency_p99)

        # Quality
        quality_path = prompt_dir / "metrics" / "quality.md"
        if quality_path.exists():
            quality_content = read_file(quality_path)
            metrics.quality_avg, metrics.quality_count = parse_quality(quality_content)
            logger.debug("Quality: avg=%.1f, count=%d", metrics.quality_avg, metrics.quality_count)

    except Exception as e:
        logger.error("Error collecting metrics for %s: %s", prompt_dir.name, e, exc_info=True)
        # Возвращаем метрики с нулевыми значениями (частичный результат)

    logger.info("Metrics collected for %s: version=%s, status=%s", prompt_dir.name, metrics.version, metrics.status)
    return metrics
