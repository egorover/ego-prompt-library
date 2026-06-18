# Шаблон: добавление новой prompt-роли

Данный шаблон позволяет быстро добавить новую AI-роль в библиотеку, сохраняя единый стандарт качества и структуры.

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

### 2.1. `prompt.md` — ядро роли

```markdown
# <Role-Name> — System Prompt

## Role Definition
...

## Context
...

## Task
...

## Constraints
...

## Decision Framework
...

## Anti-Patterns
...

## Quick Reference
...
```

Смотри `prompts/python-architect/prompt.md` как пример.

### 2.2. `card.md` — карточка роли

```markdown
# <Role-Name> — Card

## Metadata

| Field      | Value                    |
|------------|--------------------------|
| Name       | <role-name>              |
| Version    | v1.0.0                   |
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

| Критерий     | Статус | Примечание           |
|-------------|--------|----------------------|
| Контракт    | ⬜     | —                    |
| Границы     | ⬜     | —                    |
| Edge-cases  | ⬜     | —                    |
| Регрессия   | ⬜     | —                    |

## Related Files
...
```

### 2.3. `test-cases.md` — тестовые кейсы

```markdown
# <Role-Name> — Test Cases

## Test Cases

### TC-001: <Название теста>

| Field      | Value                    |
|------------|--------------------------|
| ID         | TC-001                   |
| Description| ...                      |
| Input      | ...                      |
| Expected   | ...                      |
| Status     | ⬜ not run                |
| Score      | —                        |

### TC-002: ...

## Edge Cases
...

## Metrics
...
```

### 2.4. `changelog.md` — история изменений

```markdown
# <Role-Name> — Changelog

## [v1.0.0] — YYYY-MM-DD

| Field    | Value              |
|----------|--------------------|
| Version  | v1.0.0             |
| Date     | YYYY-MM-DD         |
| Author   | <your-name>        |
| Type     | feat               |
| Summary  | Initial version    |

### Changes
- Инициальная версия промпта
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
python validate.py prompts/<role-name>
```

Он проверит:
- ✅ Наличие всех обязательных файлов
- ✅ Корректность Markdown-структуры
- ✅ Наличие всех required-секций в `prompt.md`
- ✅ Валидность метаданных в `card.md`
- ✅ Тестовые кейсы имеют ID и описания
- ✅ Метрики валидны

---

## 4. Запуск тестов

```bash
python validate.py prompts/<role-name> --run-tests
```

---

## 5. Сбор метрик

```bash
python metrics-collector.py prompts/<role-name>
```

---

## 6. Генерация отчёта

```bash
python report.py
```

Отчёт будет сгенерирован по ВСЕМ ролям, включая новую.

---

## Checklist добавления роли

- [ ] Создана директория `prompts/<role-name>/`
- [ ] Создана директория `prompts/<role-name>/metrics/`
- [ ] Заполнен `prompt.md` (7 секций по conventions)
- [ ] Заполнена `card.md` (metadata, description, input/output, scope, examples)
- [ ] Заполнены `test-cases.md` (минимум 2 TC + edge-cases)
- [ ] Создан `changelog.md` с первой версией
- [ ] Созданы метрики в `metrics/`
- [ ] Запущен `validate.py` — без ошибок
- [ ] Запущены тесты — пройдены
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
python validate.py prompts/python-dev

# 4. Тесты
python validate.py prompts/python-dev --run-tests

# 5. Метрики
python metrics-collector.py prompts/python-dev

# 6. Общий отчёт
python report.py
```

Всё — CI автоматически подхватит новую роль.
