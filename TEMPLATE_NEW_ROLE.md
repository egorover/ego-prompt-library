# Шаблон: добавление новой prompt-роли

Данный шаблон позволяет быстро добавить новую AI-роль в библиотеку, сохраняя единый стандарт качества и структуры.

Полные спецификации: [conventions.md](docs/conventions.md), [governance.md](docs/governance.md).

---

## 1. Создание структуры директории

```bash
# Создай директорию новой роли
mkdir -p prompts/<role-name>/metrics
```

Где `<role-name>` — имя роли в kebab-case (например: `python-dev`, `devops-engineer`, `qa-automator`).

---

## 2. Заполнение файлов роли

Создай следующие файлы в `prompts/<role-name>/`:

### 2.1. `prompt.md` — ядро роли (7 секций по conventions)

Структура:

```markdown
# <Role-Name>

## 1. Identity & Purpose
## 2. Context & Domain
## 3. Decision Framework
## 4. Interaction Rules
## 5. Output Format
## 6. Anti-Patterns
## 7. Quick Reference
```

Смотри `prompts/python-architect/prompt.md` как пример.

### 2.2. `card.md` — карточка роли

```markdown
# <Role-Name> — Card

## Metadata

| Field      | Value                    |
|------------|--------------------------|
| Name       | <role-name>              |
| Version    | v1.1.0                   |
| Author     | <your-name>              |
| Status     | draft                    |
| Created    | YYYY-MM-DD               |
| Updated    | YYYY-MM-DD               |
| Category   | <category>               |
| Source     | <internal|external>      |

## Description
...

## Input / Output
...

## Scope & Boundaries
...

## Constraints & Anti-Patterns
...

## Usage Examples
...

## Validation Status
...

## Related Files
...
```

### 2.3. `test-cases.md` — тестовые кейсы

```markdown
# <Role-Name> — Test Cases

## Test Suite Overview

| Метрика            | Значение |
|--------------------|----------|
| Всего кейсов       | N        |
| Пройдено           | M        |
| Пропущено          | P        |

## Test Cases

### TC-001: <Краткое описание>

- **Input:** <входные данные>
- **Expected:** <ожидаемый результат>
- **Criteria:** <критерий оценки>
- **Status:** ⏳

### TC-002: ...

## Edge Cases

### EC-001: ...

## Metrics
...
```

### 2.4. `changelog.md` — история изменений

```markdown
# <Role-Name> — Changelog

## [v1.1.0] — YYYY-MM-DD

| Field    | Value              |
|----------|--------------------|
| Version  | v1.1.0             |
| Date     | YYYY-MM-DD         |
| Author   | <your-name>        |
| Type     | feat               |
| Summary  | Initial version    |

### Changes
- Первоначальная версия промпта
- Создана базовая структура
- Создана карточка роли
- Добавлены базовые тестовые кейсы
```

### 2.5. `metrics/` — метрики роли

Создай файлы в `prompts/<role-name>/metrics/`:

- **dashboard.md** — обзорная панель метрик
- **usage.md** — метрики использования
- **quality.md** — метрики качества
- **latency.md** — метрики задержек

Примеры смотри в `prompts/python-architect/metrics/`.

---

## 3. Автоматическая проверка

После создания файлов запусти валидатор:

```bash
python scripts/validate.py prompts/<role-name>
```

Он проверит:
- ✅ Наличие всех обязательных файлов
- ✅ Корректность Markdown-структуры
- ✅ Наличие всех required-секций в `prompt.md`
- ✅ Валидность метаданных в `card.md`
- ✅ Тестовые кейсы имеют ID и описания
- ✅ Метрики валидны

---

## 4. Сбор метрик

```bash
python scripts/metrics-collector.py prompts/<role-name>
```

---

## 5. Генерация отчёта

```bash
python scripts/report_cli.py
```

Отчёт будет сгенерирован по ВСЕМ ролям, включая новую.

---

## Checklist добавления роли

- [ ] Создана директория `prompts/<role-name>/`
- [ ] Создана директория `prompts/<role-name>/metrics/`
- [ ] Заполнен `prompt.md` (7 секций по conventions.md)
- [ ] Заполнена `card.md` (metadata, description, input/output, scope, examples)
- [ ] Заполнены `test-cases.md` (минимум 5 TC + edge-cases)
- [ ] Создан `changelog.md` с первой версией
- [ ] Созданы метрики в `metrics/`
- [ ] Запущен `python scripts/validate.py prompts/<role-name>` — без ошибок
- [ ] Запущены метрики `python scripts/metrics-collector.py prompts/<role-name>`
- [ ] Статус в card.md изменён на `validated`

---

## Пример: добавление python-dev

```bash
# 1. Создать структуру
mkdir -p prompts/python-dev/metrics

# 2. Скопировать и заполнить файлы (см. выше)
# prompts/python-dev/prompt.md
# prompts/python-dev/card.md
# prompts/python-dev/test-cases.md
# prompts/python-dev/changelog.md
# prompts/python-dev/metrics/dashboard.md
# prompts/python-dev/metrics/usage.md
# prompts/python-dev/metrics/quality.md
# prompts/python-dev/metrics/latency.md

# 3. Валидация
python scripts/validate.py prompts/python-dev

# 4. Метрики
python scripts/metrics-collector.py prompts/python-dev

# 5. Общий отчёт
python scripts/report_cli.py
```

Всё — CI автоматически подхватит новую роль.
