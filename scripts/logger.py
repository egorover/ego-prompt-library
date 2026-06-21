#!/usr/bin/env python3
"""
Модуль логирования.

Предоставляет типизированный логгер с поддержкой уровней,
форматирования и вывода в консоль/файл.
"""

import logging
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

from config import config


def setup_logger(
    name: str = "prompt-library",
    level: Optional[str] = None,
    log_file: Optional[Path] = None,
) -> logging.Logger:
    """Настраивает и возвращает логгер.

    Args:
        name: Имя логгера.
        level: Уровень логирования (переопределяет config).
        log_file: Путь к файлу логов (опционально).

    Returns:
        Настроенный logging.Logger.
    """
    log_level = level or config.log_level

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Очистка предыдущих handler'ов
    logger.handlers.clear()

    # Форматирование
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Rich Handler для консоли
    console = Console(stderr=True)
    rich_handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        markup=False,
        show_path=False,
    )
    rich_handler.setFormatter(formatter)
    logger.addHandler(rich_handler)

    # File Handler (опционально)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Глобальный логгер по умолчанию
logger = setup_logger()


def get_logger(name: str) -> logging.Logger:
    """Возвращает именованный логгер.

    Args:
        name: Имя логгера (обычно __name__ модуля).

    Returns:
        logging.Logger.
    """
    return logging.getLogger(name)
