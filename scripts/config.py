#!/usr/bin/env python3
"""
Конфигурация приложения.

Загружает переменные из .env и предоставляет доступ к настройкам
через typed-класс Config (Pydantic BaseSettings).
"""

import os
from functools import cached_property
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


# Загружаем .env из корня проекта
_PROJECT_ROOT = Path(__file__).parent.parent
_ENV_PATH = _PROJECT_ROOT / ".env"

if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)


class MetricsThresholds(BaseModel):
    """Пороги для quality gate метрик.

    Attributes:
        test_pass_rate_warning: Предупреждение при % прохождении тестов ниже.
        test_pass_rate_critical: Критическое значение при % прохождении тестов ниже.
        latency_p50_warning: Предупреждение при P50 выше (сек).
        latency_p50_critical: Критическое значение при P50 выше (сек).
        quality_avg_warning: Предупреждение при среднем рейтинге ниже.
        quality_avg_critical: Критическое значение при среднем рейтинге ниже.
        changes_per_month_warning: Предупреждение при количестве изменений выше.
    """

    test_pass_rate_warning: float = Field(default=95.0, ge=0, le=100)
    test_pass_rate_critical: float = Field(default=80.0, ge=0, le=100)
    latency_p50_warning: float = Field(default=15.0, gt=0)
    latency_p50_critical: float = Field(default=30.0, gt=0)
    quality_avg_warning: float = Field(default=4.0, ge=1, le=5)
    quality_avg_critical: float = Field(default=3.0, ge=1, le=5)
    changes_per_month_warning: int = Field(default=2, ge=0)


class Config(BaseSettings):
    """Глобальная конфигурация приложения.

    Attributes:
        environment: Окружение (development/production).
        log_level: Уровень логирования.
        python_io_encoding: Кодировка ввода-вывода.
        metrics_thresholds: Пороги для quality gate.
    """

    environment: str = Field(default="development", pattern=r"^(development|production)$")
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    python_io_encoding: str = Field(default="utf-8")
    metrics_thresholds: MetricsThresholds = Field(default_factory=MetricsThresholds)

    @cached_property
    def project_root(self) -> Path:
        """Корневая директория проекта.

        Returns:
            Path до корня проекта.
        """
        return _PROJECT_ROOT

    @cached_property
    def prompts_dir(self) -> Path:
        """Директория с промптами.

        Returns:
            Path до папки prompts.
        """
        return self.project_root / "prompts"

    @cached_property
    def scripts_dir(self) -> Path:
        """Директория со скриптами.

        Returns:
            Path до папки scripts.
        """
        return self.project_root / "scripts"

    @property
    def is_production(self) -> bool:
        """Флаг production-окружения."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Флаг development-окружения."""
        return self.environment == "development"


# Глобальный экземпляр конфига
config = Config()


def configure_console_encoding() -> None:
    """Настраивает кодировку консоли для Windows."""
    import sys

    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding=config.python_io_encoding)  # type: ignore[union-attr]
            sys.stderr.reconfigure(encoding=config.python_io_encoding)  # type: ignore[union-attr]
        except (AttributeError, OSError):
            # Fallback для старых Python или терминалов без reconfigure
            os.environ["PYTHONUTF8"] = "1"


def configure_logging() -> None:
    """Настраивает глобальный уровень логирования из конфига."""
    from logger import set_log_level

    set_log_level(config.log_level)


# Инициализация при импорте
configure_console_encoding()
configure_logging()
