# AUDIT REPORT — Ego Prompt Library

**Дата аудита:** 2026-06-21  
**Ветка:** `curs/audit`  
**Аудитор:** Cursor AI (тотальный аудит)  
**Объект:** Ego Prompt Library v1.0.0  
**Статус проекта:** Level 3 (Library Asset) → Level 4 (Governed & Measured) в процессе

---

## 1. Executive Summary

| Категория | Критические | Серьёзные | Средние | Низкие | Итого |
|-----------|:-----------:|:---------:|:-------:|:------:|:-----:|
| Баги / Ошибки | 3 | 1 | 1 | 0 | **5** |
| Doc ↔ Code расхождения | 0 | 4 | 3 | 2 | **9** |
| CI/CD | 2 | 1 | 1 | 0 | **4** |
| Технический долг | 0 | 1 | 3 | 2 | **6** |
| Governance / Data | 0 | 2 | 2 | 1 | **5** |
| **ИТОГО** | **5** | **9** | **10** | **5** | **29** |

**Общий вердикт:** Проект имеет зрелую архитектуру промптов и документацию, но **ключевой инструментарий метрик и отчётности неработоспособен** при запуске через документированный способ (`python scripts/metrics-collector.py`). Предыдущий отчёт (2026-06-21) ошибочно заявлял «0 issues» — часть проблем не была устранена или регрессировала.

**Что работает:** `validate.py`, `ci-check.py` — оба промпта проходят strict-валидацию.  
**Что сломано:** `metrics-collector.py`, `report_cli.py`, pip entry points, CI jobs metrics/dashboard.

---

## 2. Методология

| Область | Действие |
|---------|----------|
| Структура репозитория | Инвентаризация 54 файлов, 2 промпт-роли |
| Скрипты | Запуск CLI, анализ импортов, pyproject.toml |
| Промпты | validate.py --json, ручной обзор card/prompt/test-cases/metrics |
| CI/CD | Анализ `.github/workflows/*.yml` vs реальный API скриптов |
| Документация | Сверка README, docs/, scripts/README с кодом |
| Governance | Сверка с maturity ladder и governance.md |
| Тесты | Поиск unit/integration tests |

---

## 3. Критические проблемы (5)

### 3.1 🔴 ImportError — metrics-collector и report_cli не запускаются

**Файлы:** `scripts/metrics-collector.py`, `scripts/report_cli.py`, `scripts/metrics/*.py`  
**Симптом:**
```
ImportError: attempted relative import beyond top-level package
  File scripts/metrics/parsers.py, line 10: from ..logger import get_logger
```
**Причина:** При запуске `python scripts/metrics-collector.py` каталог `scripts/` попадает в `sys.path`, пакет `metrics` импортируется как top-level, а относительные импорты `from ..logger` ожидают родителя `scripts`.  
**Затронуто:** 7 файлов в `scripts/metrics/` используют `from ..logger`, `from ..shared`.  
**Impact:** Весь pipeline метрик и отчётов не работает локально и в CI.

**Рекомендация:** Унифицировать импорты по паттерну `shared.py` (try/except relative/absolute) или запускать только через `python -m scripts.metrics` с корректной package-структурой.

---

### 3.2 🔴 parse_quality() — неверные индексы колонок

**Файл:** `scripts/metrics/parsers.py:106-114`

```python
parts = [p.strip() for p in line.split("|")]
# parts[0] = '' (пустой от leading |)
# parts[1] = Date, parts[2] = User, parts[3] = Relevance ...
relevance = int(parts[2])  # ← читает User ("admin"), не Relevance
```

**Impact:** Парсер возвращает `0.0, 0` для всех промптов, хотя `quality.md` содержит данные. Dashboard показывает `Quality Avg: —` при наличии 3 оценок у python-architect.

**Рекомендация:** Использовать индексы `parts[3:7]` или парсить колонку `Avg` напрямую; добавить unit-тесты на реальные строки таблицы.

---

### 3.3 🔴 pyproject.toml entry points нерабочие

**Файл:** `pyproject.toml:22-25`

```toml
prompt-metrics = "scripts.metrics.collector:main"  # collector.py не содержит main()
prompt-report = "scripts.report_cli:main"
```

**Симптом после `pip install -e .`:**
```
ModuleNotFoundError: No module named 'scripts'
```

**Причина:** `setuptools` не настраивает `scripts` как importable package; entry point ссылается на несуществующую функцию `main` в `collector.py`.

**Рекомендация:** Добавить `packages = ["scripts"]` / `package_dir`, перенести `main` в `collector.py` или указать `scripts.metrics.__main__:main`.

---

### 3.4 🔴 CI workflow metrics job гарантированно падает

**Файл:** `.github/workflows/prompt-ci.yml:76-82`

```yaml
- name: Run metrics collection
  run: python scripts/metrics-collector.py --all
```

**Проблемы:**
1. ImportError (см. 3.1) — скрипт не стартует
2. Флаг `--all` **не существует** в argparse (`metrics-collector.py`) — после исправления импортов будет `unrecognized arguments: --all`

**Impact:** Job `metrics` на push в main не выполняет заявленную функцию.

---

### 3.5 🔴 CI workflow dashboard-update аналогично сломан

**Файл:** `.github/workflows/dashboard-update.yml:41-49`

Использует те же нерабочие команды:
```bash
python scripts/metrics-collector.py --all --dashboard --json
python scripts/report_cli.py --output report.md
```

**Impact:** Ежемесячное обновление dashboard и quarterly review не работают.

---

## 4. Серьёзные проблемы (9)

### 4.1 🟠 README — ложные данные по quality-метрикам

**Файл:** `README.md:39`

| Утверждение в README | Факт в `quality.md` |
|----------------------|---------------------|
| python-architect: 3 оценки, avg 4.7 | 3 оценки, avg **4.6** (Summary) |
| python-dev: 5 оценок, avg 4.8 | **0 оценок**, Summary пустой |

---

### 4.2 🟠 README — дублированная строка в таблице промптов

**Файл:** `README.md:129-131` — `python-dev` указан дважды с идентичными данными.

---

### 4.3 🟠 Документация ссылается на несуществующий `report.py`

**Файлы:** `README.md`, `scripts/README.md`, `docs/metrics.md`, docstring в `report_cli.py`  
**Факт:** Файл называется `report_cli.py`, `report.py` отсутствует.

---

### 4.4 🟠 Документация ссылается на несуществующий флаг `--all`

**Файлы:** `README.md`, `scripts/README.md`, `docs/metrics.md`, CI workflows  
**Факт:** `metrics-collector.py` принимает только positional `target`, `--json`, `--dashboard`, `--report`.

---

### 4.5 🟠 ci-check.py не используется в CI

**Файлы:** `scripts/ci-check.py`, `.github/workflows/prompt-ci.yml`  
**Факт:** README заявляет «CI-скрипт для GitHub Actions», но workflow вызывает `validate.py` напрямую. Дублирование логики без интеграции.

---

### 4.6 🟠 Dashboard quality не синхронизирован с quality.md

**Файл:** `prompts/python-architect/metrics/dashboard.md`  
**Факт:** Summary показывает `Quality Avg: —`, хотя `quality.md` содержит 3 записи (avg 4.6). Связано с багом парсера (3.2) и неработающим CI metrics job (3.4).

---

### 4.7 🟠 Quarterly Review не проводился

**Файл:** `README.md:37`, `docs/governance.md`  
**Факт:** Процесс задокументирован, первый review запланирован на Q3 2026, но не выполнен. Блокирует полный переход на Level 4.

---

### 4.8 🟠 validate.py — слабая проверка секции Constraints

**Файл:** `scripts/shared.py:45` — `REQUIRED_CARD_SECTIONS` содержит `"## Constraints"`  
**Факт:** Карточки используют `"## Constraints & Anti-Patterns"`. Проверка `'## Constraints' in content` проходит по подстроке, но не валидирует каноническое имя секции из `conventions.md`.

---

### 4.9 🟠 config.py — мёртвый код

**Файл:** `scripts/config.py`  
**Фact:** Pydantic Config с порогами quality gate и `.env` override. **Ни один скрипт не импортирует `config`.** Пороги дублируются в `shared.METRICS_THRESHOLDS`. `.env.example` обещает override, который не работает.

---

## 5. Средние проблемы (10)

| # | Проблема | Файл(ы) | Детали |
|---|----------|---------|--------|
| 5.1 | Нет unit-тестов Python | — | 0 файлов `test_*.py`; парсеры и quality gate не покрыты |
| 5.2 | validate job не fail-fast | `prompt-ci.yml:46` | `\|\| true` на JSON-шаге; human-readable с `continue-on-error: true` |
| 5.3 | `.gitignore` игнорирует `*.json` | `.gitignore:41` | Слишком широко; может скрыть нужные JSON-артефакты |
| 5.4 | python-dev changes/month = 3 | dashboard.md | Warning-порог (≤2) превышен, не отражено в README maturity |
| 5.5 | python-dev Updated устарел | `card.md` | Updated: 2026-06-18 vs architect 2026-06-21 |
| 5.6 | playbook.md — устаревшее имя секции | `docs/playbook.md:57` | `## Constraints` вместо `## Constraints & Anti-Patterns` |
| 5.7 | metrics job не устанавливает deps | `prompt-ci.yml` | Нет `pip install -e .`; pydantic/rich не нужны для validate, но нужны для metrics/report |
| 5.8 | quarterly-review job logic | `dashboard-update.yml:135` | `if: failure()` на create issue — issue создаётся только при падении шага, не при найденных warnings |
| 5.9 | Quality gate не проверяет metrics | `prompt-ci.yml` | quality-gate читает только validation-results.json, не метрики |
| 5.10 | Предыдущий AUDIT_REPORT некорректен | `AUDIT_REPORT.md` (до замены) | Заявлял 0 issues; импорты и парсер не были проверены end-to-end |

---

## 6. Низкие проблемы (5)

| # | Проблема | Детали |
|---|----------|--------|
| 6.1 | README architecture diagram | Упоминает `report.py`, фактически `report_cli.py` + `scripts/report/` |
| 6.2 | License | «Внутренняя библиотека» — нет LICENSE файла |
| 6.3 | Нет pre-commit hooks | governance.md рекомендует, не настроено |
| 6.4 | Edge cases не нумеруются TC-XXX | validate считает только `TC-\d+:`, EC-001 не входит в count (7 TC + 2 EC = корректно по факту) |
| 6.5 | pip dependencies не закреплены | `pydantic>=2.0` без upper bound |

---

## 7. Аудит промпт-артефактов

### 7.1 python-architect (v1.1.0, validated)

| Артефакт | Статус | Замечания |
|----------|--------|-----------|
| prompt.md (7 секций) | ✅ | Полная структура |
| card.md | ✅ | Metadata полная, Constraints & Anti-Patterns |
| test-cases.md | ✅ | 7 TC + 2 EC, все ✅ |
| changelog.md | ✅ | SemVer entries |
| metrics/usage.md | ✅ | 2 записи (2026-06) |
| metrics/quality.md | ✅ | 3 оценки, avg 4.6 |
| metrics/latency.md | ✅ | Данные присутствуют |
| metrics/dashboard.md | ⚠️ | Quality Avg = — (stale из-за парсера) |

### 7.2 python-dev (v1.0.0, validated)

| Артефакт | Статус | Замечания |
|----------|--------|-----------|
| prompt.md (7 секций) | ✅ | Полная структура |
| card.md | ✅ | Metadata полная |
| test-cases.md | ✅ | 7 TC + 2 EC, все ✅ |
| changelog.md | ✅ | SemVer entries |
| metrics/usage.md | ✅ | 1 запись |
| metrics/quality.md | ⚠️ | 0 оценок (против README: «5 оценок») |
| metrics/latency.md | ✅ | Данные присутствуют |
| metrics/dashboard.md | ⚠️ | changes/month = 3 (🟡 warning) |

### 7.3 Validation results (2026-06-21)

```
validate.py --json  → status: pass (2/2 prompts)
ci-check.py --strict → [OK] All 2 prompt(s) validated successfully
```

---

## 8. Аудит скриптов

| Скрипт | Статус | Примечание |
|--------|--------|------------|
| `validate.py` | ✅ Работает | JSON + strict mode |
| `ci-check.py` | ✅ Работает | Не подключён к CI |
| `metrics-collector.py` | ❌ ImportError | Блокер |
| `report_cli.py` | ❌ ImportError | Блокер |
| `config.py` | ⚠️ Не используется | Dead code |
| `shared.py` | ✅ | Константы, discover_prompts |
| `logger.py` | ✅ | Rich logging |
| `metrics/parsers.py` | ❌ Баг parse_quality | Off-by-one |
| `metrics/collector.py` | ⚠️ | Логика OK, импорты сломаны |
| `metrics/quality_gate.py` | ⚠️ | Рефакторинг OK, не тестируется |
| `metrics/gate_checks.py` | ✅ | 5 checker-функций |
| `metrics/dashboard.py` | ⚠️ | Зависит от сломанного collector |
| `report/md_report.py` | ⚠️ | Не проверен (blocked by import) |
| `report/html_report.py` | ⚠️ | Не проверен |
| `report/json_report.py` | ⚠️ | Не проверен |
| `report/utils.py` | ✅ | compute_summary вынесен |

---

## 9. Аудит CI/CD

```
prompt-ci.yml
├── validate     ✅ (validate.py) — но soft-fail на шагах
├── metrics      ❌ ImportError + --all
└── quality-gate ⚠️ — только validation JSON, не metrics

dashboard-update.yml
├── update-dashboard  ❌ metrics + report сломаны
└── quarterly-review ⚠️ — зависит от артефактов предыдущего job
```

**Рекомендуемый минимальный fix CI:**
1. `pip install -e .` перед metrics/report
2. Убрать `--all` или добавить alias
3. Исправить импорты
4. Подключить `ci-check.py` или убрать из docs

---

## 10. Maturity Ladder — актуальный статус

| Требование Level 4 | Статус | Аудит |
|--------------------|--------|-------|
| Промпты как код | ✅ | PR, review, changelog |
| SemVer | ✅ | card.md + changelog.md |
| Тесты для ролей | ✅ | 7 TC + 2 EC на роль |
| CI/CD workflows | ⚠️ | Validate OK; metrics/report broken |
| Quality gates в коде | ❌ | Код есть, pipeline не работает |
| Quarterly Review | ❌ | Не проводился |
| Deprecation process | ✅ | Задокументирован |
| Production metrics | ⚠️ | Данные в md есть; автосбор сломан |

**Текущий уровень:** 3+ (между Library Asset и Governed & Measured)  
**Для Level 4:** исправить metrics pipeline + провести Q3 review + ≥10 quality-оценок на роль

---

## 11. Приоритетный план исправлений

### P0 — Блокеры (немедленно)

1. **Fix imports** в `scripts/metrics/*` — fallback pattern как в `shared.py`
2. **Fix parse_quality** — индексы колонок `parts[3:7]`
3. **Fix pyproject.toml** — packages + корректные entry points
4. **Fix CI workflows** — убрать `--all`, добавить `pip install`

### P1 — Высокий (эта неделя)

5. Синхронизировать README с фактическими метриками
6. Переименовать `report.py` → `report_cli.py` в документации (или добавить symlink/wrapper)
7. Обновить `REQUIRED_CARD_SECTIONS` → `## Constraints & Anti-Patterns`
8. Запустить metrics-collector и обновить dashboards

### P2 — Средний (этот спринт)

9. Подключить `config.py` к gate_checks или удалить dead code
10. Добавить unit-тесты для parsers и quality_gate
11. Провести первый Quarterly Review
12. Собрать quality-оценки для python-dev

### P3 — Низкий

13. pre-commit hooks, LICENSE, pin dependencies

---

## 12. Сильные стороны проекта

- Чёткая 7-секционная структура промптов с шаблонами
- Comprehensive governance (roles, PR process, deprecation)
- Два production-ready промпта с полным набором артефактов
- validate.py — надёжный и работающий валидатор
- Хорошая модульная декомпозиция scripts (metrics/, report/)
- Type hints, logging, pydantic config (задумано)
- Документация: playbook, conventions, governance, metrics — полная

---

## 13. Заключение

Ego Prompt Library — **зрелый фреймворк для управления промптами** с отличной документацией и структурой артефактов. Однако **измерительная часть (Level 4) фактически не функционирует**: metrics-collector, report generator и связанные CI jobs сломаны из-за ошибок импортов и бага в парсере quality.

Предыдущий аудит от 2026-06-21 содержал **ложное заключение «0 issues»** — рекомендуется проводить аудит с обязательным end-to-end запуском всех CLI-инструментов.

**Следующий аудит:** 2026-09-21 (после исправления P0/P1)

---

*Отчёт сгенерирован автоматически. Дата: 2026-06-21.*
