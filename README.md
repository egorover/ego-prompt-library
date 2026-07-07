# Ego Prompt Library

> Production-ready фреймворк для разработки, тестирования и управления AI prompt-ролями.  
> Промпты управляются как код: code review, версионирование, метрики, CI/CD.

**Дата актуализации:** 2026-07-07 06:07  
**Версия:** 1.1.0  
**Статус:** ✅ Active | **Maturity Level:** 3.5 (Library Asset)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pydantic](https://img.shields.io/badge/Pydantic-2.x-6666ff?logo=pydantic)
![Rich](https://img.shields.io/badge/Rich-13.x%2B-6666ff)
![License](https://img.shields.io/badge/License-Internal-red)
![Status](https://img.shields.io/badge/Status-Level%203.5%20Library%20Asset-orange)
![Version](https://img.shields.io/badge/Version-1.1.0-blue)
![CI](https://img.shields.io/badge/CI-Validate%20✅-green)
![Tests](https://img.shields.io/badge/Tests-132%20passed%2C%204%20skipped-brightgreen)
![Coverage](https://img.shields.io/badge/Coverage-69.14%25-ff69b4)

## 🎯 Что это такое

Это **универсальный фреймворк** для создания профессиональных AI-ролей. Не просто библиотека промптов — а полноценная система управления prompt-инструментами:

- ✅ **Создание** — шаблоны и валидация для быстрой разработки новых ролей
- ✅ **Тестирование** — 136 тестов, покрытие 69%
- ✅ **Метрики** — usage, latency, quality, test pass rate
- ✅ **CI/CD** — автоматическая проверка при каждом PR
- ✅ **Governance** — процессы review, версионирование, депреция
- ✅ **Отчётность** — dashboards, quality gates, тренды

## 📊 Maturity Ladder

Библиотека спроектирована для достижения **уровня 4 (Governed & Measured)**:

| Уровень | Название | Статус |
|---------|----------|--------|
| 1. Personal | Личный промпт | ✅ Пройден |
| 2. Team Template | Командный шаблон | ✅ Пройден |
| 3. Library Asset | Элемент библиотеки | ✅ Пройден |
| 4. Governed & Measured | Управляемый и контролируемый | 🟢 В процессе (9/10) |

### Что нужно для полного перехода на Level 4

| Требование | Статус | Примечание |
|------------|--------|------------|
| Промпты управляются как код | ✅ Готово | PR, review, changelog |
| Версионирование (SemVer) | ✅ Готово | card.md + changelog.md |
| Тесты для каждой роли | ✅ Готово | validate.py + test-cases.md |
| CI/CD воркфлоу | ✅ Готово | 2 workflow-файла в `.github/` |
| Quality gates в коде | ✅ Готово | report_cli.py + ci-check.py |
| **Quarterly Review** | ✅ Проведён | [2026-Q2 review](docs/quarterly-reviews/2026-Q2.md) |
| **Deprecation process** | ✅ Задокументирован | Процесс в governance.md |
| **Production metrics** | 🟢 Собраны | python-architect: 3 оценки, python-dev: 5 оценок |

**Для получения ✅ — выполнить 1 шаг:**

1. Продолжать собирать quality-оценки после каждого использования (цель: ≥ 10 оценок на роль)

## 📈 Текущие метрики проекта

| Метрика | Значение |
|---------|----------|
| **Всего файлов** | 89 |
| **Строк кода** | 8 696 |
| **Python файлов** | 25 (scripts) + 15 (tests) |
| **Тестов** | 136 (132 passed, 4 skipped) |
| **Покрытие кода** | 69.14% |
| **Промпт-ролей** | 2 |
| **CI pass rate** | 100% |
| **Overall Score** | 8.30/10 |

## 🏗 Архитектура

```
ego-prompt-library/
├── README.md                  # Этот файл
├── .gitignore
├── .env                       # Переменные окружения (локальные)
├── .env.example               # Пример переменных окружения
├── .pre-commit-config.yaml    # pre-commit hooks (ruff, mypy, codespell)
├── LICENSE
├── pyproject.toml             # PEP 621 конфигурация
├── AUDIT_REPORT.md            # Аудит проекта (2026-07-07)
├── TEMPLATE_NEW_ROLE.md       # Шаблон добавления новой роли
├── .coverage                  # Данные покрытия кода
├── .venv/                     # Виртуальное окружение (изолировано)
├── prompts/                   # Промпт-роли (production артефакты)
│   ├── python-architect/      # v1.1.0 (validated)
│   │   ├── prompt.md          # Ядро роли (7 секций)
│   │   ├── card.md            # Карточка роли (metadata, input/output, scope)
│   │   ├── test-cases.md      # Тесты (TC + Edge Cases + Metrics)
│   │   ├── changelog.md       # История изменений (SemVer)
│   │   └── metrics/           # Метрики роли
│   │       ├── dashboard.md   # Обзорная панель
│   │       ├── usage.md       # Частота использования
│   │       ├── quality.md     # Оценка качества (1-5)
│   │       └── latency.md     # Время генерации
│   └── python-dev/            # v1.0.0 (validated)
│       ├── prompt.md
│       ├── card.md
│       ├── test-cases.md
│       ├── changelog.md
│       └── metrics/
│           ├── dashboard.md
│           ├── usage.md
│           ├── quality.md
│           └── latency.md
├── .github/                   # CI/CD workflows
│   └── workflows/
│       ├── prompt-ci.yml      # Валидация при PR/push
│       └── dashboard-update.yml # Monthly dashboard + quarterly review
├── docs/                      # Документация
│   ├── playbook.md            # Руководство: создание, обновление, валидация
│   ├── conventions.md         # Соглашения: форматирование, структуры, шаблоны
│   ├── governance.md          # Управление: roles, PR, review, metrics, deprecation
│   ├── metrics.md             # Система метрик и dashboards
│   ├── INDEX.md               # Индекс документации
│   └── quarterly-reviews/
│       └── 2026-Q2.md         # Отчёт Q2 2026
├── templates/                 # Шаблоны для новых промптов
│   ├── prompt-template.md
│   ├── card-template.md
│   ├── test-template.md
│   └── changelog-template.md
└── scripts/                   # Валидация, метрики, CI, отчёты
    ├── __init__.py
    ├── _imports.py            # Compatibility imports
    ├── ci-check.py            # CI-скрипт для GitHub Actions
    ├── config.py              # Конфигурация (Pydantic BaseSettings)
    ├── logger.py              # Логирование (Rich)
    ├── shared.py              # Общие константы и утилиты
    ├── validate.py            # CLI-валидатор структуры
    ├── metrics-collector.py   # Сбор метрик из всех ролей
    ├── report_cli.py          # Генерация отчётов (MD/HTML/JSON)
    ├── metrics/               # Система метрик и quality gate
    │   ├── __init__.py
    │   ├── __main__.py        # CLI entry point
    │   ├── _imports.py
    │   ├── collector.py       # Сборщик метрик
    │   ├── dashboard.py       # Обновление dashboard
    │   ├── gate_checks.py     # Отдельные проверки (P0-P3)
    │   ├── models.py          # Pydantic-модели метрик
    │   ├── parsers.py         # Парсеры dashboard/quality/latency
    │   ├── quality_gate.py    # Quality gate orchestrator
    │   └── thresholds.py      # Пороги метрик
    └── report/                # Генерация отчётов
        ├── __init__.py
        ├── html_report.py     # HTML generator
        ├── json_report.py     # JSON generator
        ├── md_report.py       # Markdown generator
        ├── sanitize.py        # UTF-8 sanitizer (surrogate chars)
        └── utils.py           # Shared report logic
```

## 🚀 Возможности

### 1. Создание ролей
- **Шаблоны** — готовые файлы для быстрой старта новой роли
- **Валидатор** — проверка структуры, секций, метаданных
- **Шаблон добавления** — пошаговая инструкция `TEMPLATE_NEW_ROLE.md`

### 2. Тестирование
- **Регрессионные тесты** — TC-001, TC-002... для каждой роли
- **Edge cases** — граничные сценарии
- **Автоматическая проверка** — `validate.py --strict`
- **136 тестов**, покрытие 69%

### 3. Метрики
- **Usage count** — частота использования
- **Test pass rate** — % пройденных тестов (цель: ≥ 95%)
- **Latency P50/P95/P99** — время генерации (цель: P50 < 15s)
- **Quality Avg** — оценка качества (цель: ≥ 4.0)
- **Changes/month** — частота изменений (цель: ≤ 2)
- **Dashboard** — сводная панель с трендами

### 4. CI/CD
- **GitHub Actions** — автоматическая валидация при каждом PR
- **Quality gates** — проверка по метрикам
- **JSON-вывод** — интеграция с любыми CI-системами
- **Monthly dashboards** — автоматическое обновление 1-го числа

### 5. Governance
- **Роли** — Owner, Reviewer, Maintainer
- **Версионирование** — Semantic Versioning (v1.0.0, v1.1.0, v2.0.0)
- **PR Process** — checklist → review → approval → merge
- **Deprecation** — graceful deprecation с grace period
- **Quarterly Review** — проверка актуальности каждый квартал

### 6. Отчётность
- **Markdown-отчёты** — текстовая сводка
- **HTML-дашборды** — визуальная панель
- **JSON** — для интеграции с внешними системами
- **Quality Gates** — автоматическое выявление проблем
- **UTF-8 sanitizer** — защита от surrogate characters

## 📦 Промпты

| Промпт | Версия | Статус | Файлов | Строк |
|--------|--------|--------|--------|-------|
| [python-architect](prompts/python-architect/) | v1.1.0 | ✅ validated | 8 | 482 |
| [python-dev](prompts/python-dev/) | v1.0.0 | ✅ validated | 8 | 483 |

## 🛠 Scripts

### `validate.py` — Валидация структуры

```bash
# Все промпты
python scripts/validate.py

# Конкретный промпт
python scripts/validate.py prompts/python-architect

# Строгий режим
python scripts/validate.py --strict

# JSON для CI
python scripts/validate.py --json
```

### `metrics-collector.py` — Сбор метрик

```bash
# Все промпты
python scripts/metrics-collector.py --all

# Конкретный промпт
python scripts/metrics-collector.py prompts/python-architect

# Обновить dashboards
python scripts/metrics-collector.py --dashboard

# JSON-вывод
python scripts/metrics-collector.py --all --json > metrics.json
```

### `report_cli.py` — Генерация отчётов

```bash
# Markdown-отчёт
python scripts/report_cli.py --output report.md

# HTML-дашборд
python scripts/report_cli.py --html --output dashboard.html

# JSON для CI
python scripts/report_cli.py --json --output report.json

# Только проблемы
python scripts/report_cli.py --strict
```

### `ci-check.py` — CI-скрипт

```bash
python scripts/ci-check.py
```

## 🧪 Тесты

```bash
# Запуск всех тестов
python -m pytest tests/ -q --no-cov

# С покрытием кода
python -m pytest tests/ --cov=scripts --cov-report=term-missing

# С фильтрацией по модулю
python -m pytest tests/test_config.py -v
```

**Результаты:** 132 passed, 4 skipped (Windows subprocess tests)

## 🛡 Линтинг и статический анализ

```bash
# Ruff (linting + formatting)
ruff check scripts/ tests/
ruff format scripts/ tests/

# MyPy (type checking)
python -m mypy scripts/

# Codespell (проверка орфографии)
codespell scripts/ tests/
```

## 📚 Документация

| Документ | Описание |
|----------|----------|
| [playbook.md](docs/playbook.md) | Руководство: создание, обновление, валидация |
| [conventions.md](docs/conventions.md) | Соглашения: форматирование, структуры, шаблоны |
| [governance.md](docs/governance.md) | Управление: roles, PR, review, metrics, deprecation |
| [metrics.md](docs/metrics.md) | Система метрик и dashboards |
| [INDEX.md](docs/INDEX.md) | Индекс документации |
| [AUDIT_REPORT.md](AUDIT_REPORT.md) | Аудит проекта (2026-07-07) |
| [TEMPLATE_NEW_ROLE.md](TEMPLATE_NEW_ROLE.md) | Шаблон добавления новой роли |
| [scripts/README.md](scripts/README.md) | Описание скриптов |

## 🔄 Добавление новой роли

Смотри [TEMPLATE_NEW_ROLE.md](TEMPLATE_NEW_ROLE.md) — пошаговая инструкция.

Быстрый старт:

```bash
# 1. Создать структуру
mkdir -p prompts/<role-name>/metrics

# 2. Заполнить файлы (см. шаблон)
# prompts/<role-name>/prompt.md
# prompts/<role-name>/card.md
# prompts/<role-name>/test-cases.md
# prompts/<role-name>/changelog.md
# prompts/<role-name>/metrics/{dashboard,usage,quality,latency}.md

# 3. Валидация
python scripts/validate.py prompts/<role-name>

# 4. Метрики
python scripts/metrics-collector.py prompts/<role-name>

# 5. Отчёт
python scripts/report_cli.py --output report.md
```

## 🤝 Governance

Полный процесс управления: [docs/governance.md](docs/governance.md)

- **Roles:** Owner, Reviewer, Maintainer
- **Process:** PR → Review → Merge
- **Versioning:** Semantic Versioning (v1.0.0, v1.1.0, v2.0.0)
- **Deprecation:** Grace period 2 release cycles
- **Review:** Quarterly review актуальности

## 📊 Metrics

Система метрик: [docs/metrics.md](docs/metrics.md)

Каждый промпт собирает:
- **Usage** — частота и сценарии использования
- **Test pass rate** — стабильность тестов (цель: ≥ 95%)
- **Latency** — время генерации P50/P95/P99 (цель: P50 < 15s)
- **Quality** — оценка пользователя (1-5, цель: ≥ 4.0)
- **Dashboard** — сводка с трендами

Quality Gates:
- 🔴 **Critical** — test pass rate < 80%, quality < 3.0, latency > 30s
- 🟡 **Warning** — test pass rate < 95%, quality < 4.0, latency > 15s
- 🟢 **Healthy** — все метрики в норме

## 🔧 Установка

### Требования

- Python 3.10+
- pip

### Настройка окружения

```bash
# 1. Создать виртуальное окружение
python -m venv .venv

# 2. Активировать (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 3. Установить зависимости
pip install -e ".[dev]"

# 4. Создать .env из примера
Copy-Item .env.example .env

# 5. Настроить pre-commit
pre-commit install
```

## 📝 License

Внутренняя библиотека.

---

**Актуализировано:** 2026-07-07 06:07  
**Следующая актуализация:** 2026-10-07 (Q3 2026)
