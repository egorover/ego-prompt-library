# AUDIT REPORT — Ego Prompt Library

**Дата аудита:** 2026-06-20
**Аудитор:** Koda AI
**Объект:** Ego Prompt Library (v1.0.0)
**Статус проекта:** Production-ready, Level 3→4 Governed & Measured

---

## 1. Executive Summary

| Категория | Критические | Серьёзные | MEDIUM | Низкие | Итого |
|-----------|:-----------:|:---------:|:------:|:------:|:-----:|
| Баги / Ошибки | 0 | 2 | 4 | 3 | 9 |
| Дубли / Redundancy | 0 | 1 | 3 | 2 | 6 |
| Технический долг | 0 | 2 | 4 | 2 | 8 |
| Расхождения Doc ↔ Code | 0 | 2 | 3 | 1 | 6 |
| Data / Stale | 0 | 0 | 2 | 2 | 4 |
| **ИТОГО** | **0** | **7** | **16** | **10** | **33** |

**Общий вердикт:** Проект структурно зрелый, хорошо документированный. Требуется исправление 7 серьёзных проблем (преимущественно в парсерах метрик и расхождениях между документацией и реальным кодом), а также устранение дублирования CLI-логики.

---

## 2. Баги и Ошибки

### 2.1 [SEVERE] `parse_status()` — сломанный regex `$` в `shared.py`

**Файл:** `scripts/shared.py` — функция `parse_status()`, строка с `f"| {status}$"`

**Проблема:** `$` внутри f-string-шаблона regex не работает как anchor конца строки. Фраза `f"| {status}$"` создаёт шаблон `"\| draft$"` — `$` интерпретируется буквально. Для статуса `draft` regex ищет строку, заканчивающуюся на `| draft$` (с literal `$`), а не `| draft`.

**Impact:** Статус может не найтись в карточках, где строка заканчивается пробелом или другими символами после значения.

**Рекомендация:** Заменить `f"| {status}$"` на `f"\| {status}\s*\|"` (с явным `$` или без — главное без `$` в f-string).

---

### 2.2 [SEVERE] `report.py` конфликтует с `report/` пакетом

**Файлы:** `scripts/report.py` (CLI entry point) vs `scripts/report/` (пакет с `__init__.py`, `json_report.py`, `html_report.py`, `md_report.py`)

**Проблема:** `scripts/report.py` содержит `from report import generate_json_report, generate_html_report, generate_md_report`. При запуске `python scripts/report.py` Python импортирует `scripts/report/` (пакет), а не `scripts/report.py` (модуль). Это может вызвать ambiguity при импорте.

**Impact:** При запуске из директории `scripts/` импорт может сломаться. При запуске из корня репозитория — работает, но ненадёжно.

**Рекомендация:** Переименовать `scripts/report.py` в `scripts/generate_report.py` или `scripts/report_cli.py`.

---

### 2.3 [MEDIUM] `validate_metadata()` — проверка статуса по всему контенту карточки

**Файл:** `scripts/validate.py`, функция `validate_metadata()`

**Проблема:** Проверяет `if not any(status in content for status in VALID_STATUSES)` по всей карточке, а не только в секции Metadata. Это может дать ложный positive, если статус найден где-то в Usage Examples или других секциях.

**Рекомендация:** Ограничить проверку секцией Metadata (аналогично `parse_status()`).

---

### 2.4 [MEDIUM] `parse_quality()` — ожидаемое количество колонок

**Файл:** `scripts/metrics/parsers.py`, функция `parse_quality()`

**Проблема:** Функция ожидает `len(parts) >= 7` для строк таблицы quality.md. Но шаблон и фактические данные имеют 9 колонок (`| Date | User | Relevance | Completeness | Structure | Value | Scenario | Notes | Avg |`). При изменении шаблона (добавлении/удалении колонок) парсер может начать парсить неверно.

**Рекомендация:** Использовать ключевые имена колонок из заголовка вместо позиций.

---

### 2.5 [MEDIUM] `metrics-collector.py` — конфликтующие импорты

**Файл:** `scripts/metrics-collector.py`

**Проблема:** В строке `from metrics import collect_metrics` импортируется `collect_metrics`, но в коде функции `main()` он нигде не используется — вместо этого вызывается `collect_metrics(p)` из top-level scope. Фактически используется, но импорт из `metrics` конфликтует с импортом `from metrics import update_dashboard` внутри `if args.dashboard`.

**Рекомендация:** Убрать дублирующий импорт, использовать единый `from metrics import collect_metrics, update_dashboard` на top-level.

---

### 2.6 [MEDIUM] `dashboard.md` — жёстко заданная дата обновления

**Файл:** `prompts/python-architect/metrics/dashboard.md`, `prompts/python-dev/metrics/dashboard.md`

**Проблема:** Дата обновления в dashboard зафиксирована как `2026-06-19` (жестко вписана). При следующем запуске CI дата не изменится автоматически, если `update_dashboard()` не вызывался. Функция `update_dashboard()` генерирует новую дату через `date.today()`, но если dashboard файл не существует (header не совпадает), функция просто `return`.

**Рекомендация:** Добавить fallback — если dashboard не найден или header не совпадает, создать новый с актуальной датой.

---

### 2.7 [MEDIUM] `count_usage()` — несовпадение форматов

**Файл:** `scripts/metrics/collector.py`, функция `count_usage()`

**Проблема:** Функция парсит usage.md по формату: `| Date | User | Scenario | Source |`, но фактические файлы имеют разные заголовки:
- `python-architect/metrics/usage.md`: `| Date | User | Scenario | Source |`
- `python-dev/metrics/usage.md`: `| Дата | Сценарий | User | Notes |`

**Impact:** Функция не найдёт данные в `python-dev/metrics/usage.md` (разный порядок колонок и названия заголовков).

**Рекомендация:** Парсить по наличию непустых ячеек, а не по позициям колонок.

---

### 2.8 [MEDIUM] `parse_status()` — тоже проверяет по всему контенту

**Файл:** `scripts/shared.py`, функция `parse_status()`

**Проблема:** Аналогично `validate_metadata()` — ищет статус в `VALID_STATUSES` по всему контенту карточки, а не только в секции Metadata. Может дать ложный positive.

**Рекомендация:** Ограничить поиск секцией Metadata.

---

### 2.9 [LOW] `validate_prompt()` — `relative_to()` на абсолютном пути

**Файл:** `scripts/validate.py`, функция `validate_prompt()`

**Проблема:** `str(prompt_dir.relative_to(prompt_dir.parent.parent))` — если `prompt_dir` — абсолютный путь (что бывает при `Path.resolve()`), `relative_to()` может упасть с `ValueError`, если пути не из одной ветки.

**Рекомендация:** Использовать `prompt_dir.name` как fallback.

---

## 3. Дублирование и Redundancy

### 3.1 [SEVERE] `metrics-collector.py` ↔ `metrics/__main__.py` — дублирование логики

**Файлы:** `scripts/metrics-collector.py` и `scripts/metrics/__main__.py`

**Проблема:** Оба файла выполняют практически одинаковую задачу: собирают метрики для всех промптов и выводят на экран. `metrics-collector.py` — это CLI с аргументами, `__main__.py` — упрощённый entry point для `python -m scripts.metrics`.

**Рекомендация:** Объединить логику в одном месте. `__main__.py` может делегировать вызов `metrics-collector.py` с дефолтными аргументами.

---

### 3.2 [MEDIUM] `validate.py` ↔ `ci-check.py` — дублирование валидации

**Файлы:** `scripts/validate.py` и `scripts/ci-check.py`

**Проблема:** `ci-check.py` импортирует `validate_prompt` из `validate.py` и делает обёртку. Это допустимо, но `ci-check.py` вызывает `validate_prompt` с `strict=True`, что дублирует аргумент CLI `--strict` из `validate.py`.

**Рекомендация:** Допустимо как есть, но рекомендуется добавить `ci-check.py` в `__main__.py` для консистентности.

---

### 3.3 [MEDIUM] Документация — пересекающийся контент

**Файлы:** `docs/playbook.md`, `docs/conventions.md`, `docs/INDEX.md`, `TEMPLATE_NEW_ROLE.md`

**Проблема:** Одна и та же информация (структура промпта, секции, формат тест-кейсов) продублирована в 4 местах без явного разграничения «источник истины».

**Рекомендация:** Определить `conventions.md` как единственный источник истины для структур. В `playbook.md` и `TEMPLATE_NEW_ROLE.md` оставить только ссылки на `conventions.md`.

---

### 3.4 [MEDIUM] HTML/MD/JSON report generators — дублирование summary logic

**Файлы:** `scripts/report/json_report.py`, `scripts/report/html_report.py`, `scripts/report/md_report.py`

**Проблема:** В каждом генераторе дублируется вычисление `critical_count`, `warning_count`, `info_count`, `healthy_count`.

**Рекомендация:** Вынести в утилиту `scripts/report/utils.py` или передать pre-computed summary в каждый генератор.

---

### 3.5 [LOW] `README.md` ↔ `docs/playbook.md` — дублирование Maturity Ladder

**Проблема:** Таблица Maturity Ladder продублирована в README и playbook без ссылок друг на друга.

**Рекомендация:** В README оставить ссылку на `docs/playbook.md#maturity-ladder`.

---

### 3.6 [LOW] `templates/` — шаблон не соответствует conventions

**Файл:** `templates/prompt-template.md`

**Проблема:** Шаблон имеет секции `<ROLE NAME> — Системный промпт`, `Identity & Purpose`, `Context & Domain`... но структура секций отличается от `conventions.md` (в conventions секции помечены как `## 1. Identity & Purpose`, `## 2. Context & Domain` и т.д.).

**Рекомендация:** Привести шаблоны к единому формату conventions.

---

## 4. Технический долг

### 4.1 [SEVERE] Нет `pyproject.toml` / `setup.py`

**Проблема:** Проект — набор Python-скриптов без менеджерной конфигурации. Нет `pyproject.toml`, `requirements.txt`, `setup.cfg`. Невозможно установить как пакет, нет версии, нет entry points.

**Рекомендация:** Создать `pyproject.toml` с `project.name = "ego-prompt-library"`, `project.version`, `scripts/` entry points.

---

### 4.2 [SEVERE] `dashboard-update.yml` — несуществующий artifact

**Файл:** `.github/workflows/dashboard-update.yml`

**Проблема:** Job `quarterly-review` пытается прочитать `report.json` через `Path('report.json').read_text()`, но файл создаётся только в job `update-dashboard` и не передаётся как artifact.

**Impact:** При monthly schedule `report.json` не существует → скрипт падает с FileNotFoundError.

**Рекомендация:** Добавить `actions/upload-artifact` в `update-dashboard` и `actions/download-artifact` в `quarterly-review`.

---

### 4.3 [MEDIUM] `METRICS_THRESHOLDS` — hardcode в `shared.py`

**Файл:** `scripts/shared.py`

**Проблема:** Константы `METRICS_THRESHOLDS` определены в `shared.py`, но значения дублируются в `docs/metrics.md` и `docs/governance.md`. При изменении порогов нужно обновлять 3 места.

**Рекомендация:** Вынести в отдельный `config.py` и ссылаться из документации.

---

### 4.4 [MEDIUM] `quality_gate.py` — монолитная функция

**Файл:** `scripts/metrics/quality_gate.py`

**Проблема:** Функция `check_quality_gate()` (~90 строк) содержит логику для 6 разных метрик в одном блоке. Тестировать и расширять сложно.

**Рекомендация:** Разделить на отдельные функции: `check_test_pass_rate()`, `check_latency()`, `check_quality()`, `check_changes()`, `check_status()`.

---

### 4.5 [MEDIUM] Нет type hints в скриптах

**Файл:** `scripts/validate.py`, `scripts/metrics-collector.py`, `scripts/ci-check.py`

**Проблема:** Скрипты не имеют type hints, что затрудняет рефакторинг и CI-проверки типов.

**Рекомендация:** Добавить type hints и запустить `mypy` через CI.

---

### 4.6 [MEDIUM] `report.py` — Windows encoding fix только в одном файле

**Файл:** `scripts/report.py`

**Проблема:** Блок `if sys.platform == "win32": sys.stdout.reconfigure(encoding="utf-8")` есть только в `report.py`, но не в других скриптах.

**Рекомендация:** Вынести в `shared.py`.

---

### 4.7 [LOW] Нет `.gitignore`

**Проблема:** В README упоминается `.gitignore`, но файл не существует в репозитории.

**Рекомендация:** Создать `.gitignore` с `__pycache__/`, `*.pyc`, `*.pyo`, `*.egg-info/`, `.pytest_cache/`, `venv/`, `report.md`, `dashboard.html`, `report.json`, `metrics-data.json`.

---

### 4.8 [LOW] `metrics-collector.py` — `--all` flag redundant

**Файл:** `scripts/metrics-collector.py`

**Проблема:** Флаг `--all` — это поведение по умолчанию. Наличие flag'а, который ничего не меняет, вводит в заблуждение.

**Рекомендация:** Убрать `--all` или переделать в `--specific` для контраста.

---

## 5. Расхождения Documentation ↔ Code

### 5.1 [SEVERE] `TEMPLATE_NEW_ROLE.md` — несуществующая команда `--run-tests`

**Файл:** `TEMPLATE_NEW_ROLE.md`

**Проблема:** Документация ссылается на `python validate.py prompts/<role-name> --run-tests`, но такого флажка не определён в `validate.py`.

**Рекомендация:** Убрать `--run-tests` из документации или реализовать его.

---

### 5.2 [SEVERE] `conventions.md` — REQUIRED_CARD_SECTIONS не совпадает с реальными карточками

**Файл:** `docs/conventions.md` vs `prompts/python-architect/card.md`

**Проблема:**
- conventions: `## Constraints & Anti-Patterns` (один раздел)
- Реальность: `### Ограничения` + `### Антипаттерны` (два подраздела под `## Constraints & Anti-Patterns`)
- conventions: `## Validation Status` (с эмодзи ⬜ в шаблоне)
- Реальность: `## Validation Status` (с эмодзи ✅ в реальных файлах)

**Impact:** `validate_card_structure()` может не найти `## Constraints & Anti-Patterns` в реальных файлах.

**Рекомендация:** Привести conventions к реальному формату или исправить реальные карточки.

---

### 5.3 [MEDIUM] `conventions.md` — REQUIRED_PROMPT_SECTIONS vs реальные `prompt.md`

**Файл:** `docs/conventions.md` vs `prompts/python-architect/prompt.md`

**Проблема:** conventions указывает секции как `1. Identity & Purpose`, `2. Context & Domain`... Реальные файлы имеют `## 1. Identity & Purpose` (с `##`). Валидатор ищет `1. Identity & Purpose` (без `##`), что должно работать, но форматирование заголовков не совпадает.

**Рекомендация:** Унифицировать формат заголовков.

---

### 5.4 [MEDIUM] `TEMPLATE_NEW_ROLE.md` — `prompt.md` шаблон не соответствует 7-секционной структуре

**Файл:** `TEMPLATE_NEW_ROLE.md`

**Проблема:** В шаблоне секции названы как `## Role Definition`, `## Context`, `## Task`, `## Constraints` — не соответствуют conventions `## 1. Identity & Purpose`, `## 2. Context & Domain` и т.д.

**Рекомендация:** Привести шаблон к формату conventions.

---

### 5.5 [MEDIUM] `README.md` — Architecture diagram не соответствует реальному дереву

**Файл:** `README.md`

**Проблема:** В README архитектура показана с `├── .gitignore` (файла нет), и с `└── scripts/` как последним элементом, но реальное дерево имеет больше файлов и вложенность.

**Рекомендация:** Обновить diagram или заменить на `tree` output.

---

### 5.6 [LOW] Changelog v1.1.0 — опечатка "Инициальная"

**Файл:** `prompts/python-architect/changelog.md`

**Проблема:** `Инициальная версия` вместо `Первоначальная версия` или `Initial version`.

**Рекомендация:** Исправить опечатку.

---

## 6. Stale / Out-of-date Data

### 6.1 [MEDIUM] `python-architect/metrics/usage.md` — данные за 2025-07

**Файл:** `prompts/python-architect/metrics/usage.md`

**Проблема:** Данные датированы июлем 2025. Записи содержат только `| — | — | — | — |`.

**Рекомендация:** Обновить или удалить устаревший месяц.

---

### 6.2 [MEDIUM] `python-architect/metrics/quality.md` — 0 оценок

**Файл:** `prompts/python-architect/metrics/quality.md`

**Проблема:** Quality ratings полностью пусты. README утверждает "3 оценки у python-architect (avg 4.7)".

**Рекомендация:** Обновить quality.md реальными данными или исправить README.

---

### 6.3 [LOW] `python-architect/metrics/latency.md` — данные за 2025-07

**Файл:** `prompts/python-architect/metrics/latency.md`

**Проблема:** Данные за июль 2025. Актуальность под вопросом.

**Рекомендация:** Обновить или архивировать.

---

### 6.4 [LOW] `python-dev/metrics/usage.md` — несовпадение формата с парсером

**Файл:** `prompts/python-dev/metrics/usage.md`

**Проблема:** Заголовок таблицы `| Дата | Сценарий | User | Notes |` не соответствует формату парсера `| Date | User | Scenario | Source |`.

**Рекомендация:** Привести к единому формату.

---

## 7. Recommendations — Priority Matrix

| # | Issue | Priority | Effort | Owner |
|---|-------|:--------:|:------:|-------|
| 2.1 | `parse_status()` regex `$` | **High** | 15 min | Maintainer |
| 2.2 | `report.py` vs `report/` conflict | **High** | 30 min | Maintainer |
| 4.1 | Нет `pyproject.toml` | **High** | 1-2 часа | Maintainer |
| 4.2 | `dashboard-update.yml` missing artifact | **High** | 30 мин | Maintainer |
| 5.1 | `TEMPLATE_NEW_ROLE.md` — `--run-tests` | **High** | 15 мин | Maintainer |
| 5.2 | `conventions.md` vs реальные карточки | **High** | 30 мин | Maintainer |
| 3.1 | `metrics-collector.py` ↔ `__main__.py` | Medium | 1 час | Maintainer |
| 2.5 | `metrics-collector.py` duplicate import | Medium | 10 мин | Maintainer |
| 2.7 | `count_usage()` format mismatch | Medium | 30 мин | Maintainer |
| 4.5 | `quality_gate.py` монолитная функция | Medium | 2 часа | Maintainer |
| 4.4 | `METRICS_THRESHOLDS` hardcode | Medium | 30 мин | Maintainer |
| 5.4 | `TEMPLATE_NEW_ROLE.md` не соответствует 7 секциям | Medium | 1 час | Maintainer |
| 6.1 | `usage.md` за 2025-07 | Low | 15 мин | Owner |
| 6.2 | `quality.md` — 0 оценок vs README | Low | 15 мин | Owner |
| 4.8 | Нет `.gitignore` | Low | 10 мин | Maintainer |

---

## 8. Project Health Overview

### Strengths
- ✅ Хорошо структурированная система промптов (7 секций)
- ✅ Comprehensive governance process
- ✅ CI/CD pipeline с валидацией и quality gates
- ✅ Multiple output formats (MD/HTML/JSON)
- ✅ Метрики и dashboards для каждой роли
- ✅ Чёткие шаблоны для новых ролей

### Weaknesses
- ⚠️ Расхождения между документацией и реальным кодом
- ⚠️ Дублирование CLI-логики
- ⚠️ Stale метрические данные
- ⚠️ Отсутствие package management (`pyproject.toml`)
- ⚠️ Неиспользуемые/устаревшие файлы метрик

### Opportunities
- 📈 Добавить `mypy` в CI для type checking
- 📈 Автоматизировать обновление метрик через GitHub Events API
- 📈 Добавить integration tests для парсеров
- 📈 Поддерживать единый `config.py` для всех порогов

### Threats
- 🔴 `report.py` vs `report/` conflict может сломать CI при изменении CWD
- 🔴 `dashboard-update.yml` может падать при monthly schedule
- 🔴 `parse_status()` может не находить статус — сломает governance flow

---

## 9. Conclusion

Проект находится на **зрелом уровне** с хорошей архитектурой и документацией. Основные проблемы — **расхождения между документацией и кодом** (5.2, 5.4), **конфликт имён** (2.2) и **отсутствие package management** (4.1). Рекомендуется приоритетно исправить 6 issues из секции 7 (High priority), затем устранить Medium и Low issues в рамках следующих итераций.

**Следующий аудит:** 2026-09-20

---

*Отчёт сгенерирован автоматически AI-аудитором Koda.*
