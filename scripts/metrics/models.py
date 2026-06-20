#!/usr/bin/env python3
"""Data models for prompt metrics.

Defines:
- PromptMetrics: dataclass for all collected metrics
- Issue: dataclass for quality gate violations
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PromptMetrics:
    """All collected metrics for a single prompt.

    Attributes:
        name: Имя промпта (directory name).
        usage_count: Количество использований.
        test_pass_rate: Процент пройденных тестов.
        test_total: Общее количество тестов.
        test_passed: Количество пройденных тестов.
        latency_p50: Медианное время генерации (сек).
        latency_p95: P95 время генерации (сек).
        latency_p99: P99 время генерации (сек).
        quality_avg: Средняя оценка качества (1-5).
        quality_count: Количество оценок качества.
        changes_this_month: Количество изменений в этом месяце.
        open_issues: Количество открытых проблем.
        version: Версия промпта (например, v1.1.0).
        status: Статус (draft/testing/validated/deprecated).
    """
    name: str
    usage_count: int = 0
    test_pass_rate: float = 100.0
    test_total: int = 0
    test_passed: int = 0
    latency_p50: float = 0.0
    latency_p95: float = 0.0
    latency_p99: float = 0.0
    quality_avg: float = 0.0
    quality_count: int = 0
    changes_this_month: int = 0
    open_issues: int = 0
    version: str = ""
    status: str = ""

    def to_dict(self) -> dict:
        """Конвертирует метрики в словарь для JSON-сериализации.

        Returns:
            Словарь с метриками.
        """
        return {
            "name": self.name,
            "usage_count": self.usage_count,
            "test_pass_rate": self.test_pass_rate,
            "latency_p50": self.latency_p50,
            "latency_p95": self.latency_p95,
            "latency_p99": self.latency_p99,
            "quality_avg": self.quality_avg,
            "quality_count": self.quality_count,
            "changes_this_month": self.changes_this_month,
            "open_issues": self.open_issues,
            "version": self.version,
            "status": self.status,
        }


@dataclass
class Issue:
    """Quality gate violation.

    Attributes:
        severity: Уровень серьёзности (critical/warning/info).
        prompt_name: Имя промпта с проблемой.
        metric: Название метрики.
        message: Описание проблемы.
        recommendation: Рекомендация по исправлению.
    """
    severity: str  # critical, warning, info
    prompt_name: str
    metric: str
    message: str
    recommendation: str
