# Ego Prompt Library

> Production-ready фреймворк для разработки, тестирования и управления AI prompt-ролями.
> Промпты управляются как код: code review, версионирование, метрики, CI/CD.

## 🎯 Что это такое

Это **универсальный фреймворк** для создания профессиональных AI-ролей. Не просто библиотека промптов — а полноценная система управления prompt-инструментами:

- ✅ **Создание** — шаблоны и валидация для быстрой разработки новых ролей
- ✅ **Тестирование** — регрессионные тесты для каждой роли
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
| 4. Governed & Measured | Управляемый и контролируемый | 🟢 В процессе |

### Что нужно для полного перехода на Level 4

| Требование | Статус | Примечание |
|------------|--------|------------|
| Промпты управляются как код | ✅ Готово | PR, review, changelog |
| Версионирование (SemVer) | ✅ Готово | card.md + changelog.md |
| Тесты для каждой роли | ✅ Готово | validate.py + test-cases.md |
| CI/CD воркфлоу | ✅ Готово | 2 workflow-файла в `.github/` |
| Quality gates в коде | ✅ Готово | report.py + ci-check.py |
| **Quarterly Review** | ⚠️ Не проводился | Первый review запланировать на Q3 2026 |
| **Deprecation process** | ✅ Задокументирован | Процесс в governance.md, ни один промпт не требует deprecation |
| **Production metrics** | 🟢 Собраны | 3 оценки у python-architect (avg 4.7), 5 у python-dev (avg 4.8) |

**Для получения ✅ — выполнить 2 шага:**

1. Провести первый Quarterly Review (проверить актуальность обоих промптов)
2. Продолжать собирать quality-оценки после каждого использования (цель: ≥ 10 оценок на роль)

## 🏗 Архитектура

```
ego-prompt-library/
├── README.md                  # Этот файл
├── .gitignore
├── TEMPLATE_NEW_ROLE.md       # Шаблон добавления новой роли
├── prompts/                   # Промпт-роли (production артефакты)
│   └── python-architect/      # ← одна роль = одна директория
│       ├── prompt.md          # Ядро роли (7 секций)
│       ├── card.md            # Карточка роли (metadata, input/output, scope)
│       ├── test-cases.md      # Тесты (TC + Edge Cases + Metrics)
│       ├── changelog.md       # История изменений (SemVer)
│       └── metrics/           # Метрики роли
│           ├── dashboard.md   # Обзорная панель
│           ├── usage.md       # Частота использования
│           ├── quality.md     # Оценка качества (1-5)
│           └── latency.md     # Время генерации
│   └── python-dev/            # Вторая роль (development)
├── .github/                   # CI/CD workflows
│   └── workflows/
│       ├── prompt-ci.yml      # Валидация при PR/push
│       └── dashboard-update.yml # Monthly dashboard + quarterly review
├── docs/                      # Документация
│   ├── playbook.md            # Руководство: создание, обновление, валидация
│   ├── conventions.md         # Соглашения: форматирование, структуры, шаблоны
│   ├── governance.md          # Управление: roles, PR, review, metrics, deprecation
│   └── metrics.md             # Система метрик и dashboards
├── templates/                 # Шаблоны для новых промптов
│   ├── prompt-template.md
│   ├── card-template.md
│   ├── test-template.md
│   └── changelog-template.md
└── scripts/                   # Валидация, метрики, CI, отчёты
    ├── validate.py            # CLI-валидатор структуры
    ├── ci-check.py            # CI-скрипт для GitHub Actions
    ├── metrics-collector.py   # Сбор метрик из всех ролей
    ├── report.py              # Генерация отчётов (MD/HTML/JSON)
    └── README.md
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

## 📦 Промпты

| Промпт | Версия | Статус | Описание |
|--------|--------|--------|----------|
| [python-architect](prompts/python-architect/) | v1.1.0 | ✅ validated | AI-роль для проектирования архитектуры Python-проектов |
| [python-dev](prompts/python-dev/) | v1.0.0 | ✅ validated | AI-роль для написания производственного Python-кода |
| [python-dev](prompts/python-dev/) | v1.0.0 | ✅ validated | AI-роль для написания производственного Python-кода |

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

### `report.py` — Генерация отчётов

```bash
# Markdown-отчёт
python scripts/report.py --output report.md

# HTML-дашборд
python scripts/report.py --html --output dashboard.html

# JSON для CI
python scripts/report.py --json --output report.json

# Только проблемы
python scripts/report.py --strict
```

### `ci-check.py` — CI-скрипт

```bash
python scripts/ci-check.py
```

## 📚 Документация

| Документ | Описание |
|----------|----------|
| [playbook.md](docs/playbook.md) | Руководство: создание, обновление, валидация |
| [conventions.md](docs/conventions.md) | Соглашения: форматирование, структуры, шаблоны |
| [governance.md](docs/governance.md) | Управление: roles, PR, review, metrics, deprecation |
| [metrics.md](docs/metrics.md) | Система метрик и dashboards |
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
python scripts/report.py --output report.md
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

## 📝 License

Внутренняя библиотека.
