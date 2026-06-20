# Playbook — Руководство по созданию и использованию промптов

> 📌 Промпты в этой библиотеке — first-class артефакты, равнозначные коду.
> Они проходят code review, тестирование, версионирование и governance.

## Maturity Ladder — Уровни зрелости

Каждый промпт проходит 4 этапа эволюции:

| Уровень | Название | Описание | Что требуется |
|---------|----------|----------|---------------|
| **1** | Personal | Личный промпт, работает у одного | Только prompt.md в голове |
| **2** | Team Template | Командный шаблон с явными входами/выходами | prompt.md + card.md + Output Format |
| **3** | Library Asset | Артефакт библиотеки с карточкой и навигацией | + test-cases.md + changelog.md + README |
| **4** | Governed & Measured | Управляемый как код с метриками и ревью | + governance + CI + metrics + review |

**Цель:** каждый промпт должен достичь уровня 4. Текущее состояние библиотеки — уровень 3→4.

## Структура промпта

Каждый промпт состоит из 4 файлов:

### 1. `prompt.md` — Системный промпт

Системная инструкция, задающая роль AI. Загружается в system message.

**Обязательные секции (7 разделов):**

```markdown
## 1. Identity & Purpose      — Кто и зачем
## 2. Context & Domain        — Когда и в каком контексте
## 3. Decision Framework       — Приоритеты и алгоритм
## 4. Interaction Rules        — Как общаться
## 5. Output Format            — Формат вывода (детерминированный)
## 6. Anti-Patterns            — Чего избегать
## 7. Quick Reference          — Справочная таблица
```

**Правила:**
- Начинайте с чёткого определения роли
- Используйте иерархию приоритетов: `🔴 Must` → `🟡 Should` → `🟢 Can`
- Каждый раздел — **независимая единица знаний** (self-contained)
- Избегайте противоречий между разделами
- Output Format должен быть детерминированным

### 2. `card.md` — Карточка роли

Документация роли. Самодостаточна для нового участника.

**Обязательные секции:**

```markdown
## Metadata            — Имя, версия, автор, статус, категория
## Description          — Описание роли (2-3 абзаца)
## Input / Output       — Входы и выходы (таблицы)
## Scope & Boundaries   — Что входит / не входит
## Constraints          — Ограничения и антипаттерны
## Usage Examples       — Примеры использования
## Validation Status    — Статус валидации по критериям
## Related Files        — Ссылки на связанные файлы
```

**Статусы:** (полная таблица: [conventions.md — Статусы](conventions.md#статусы))

### 3. `test-cases.md` — Тестовые кейсы

Регрессионные проверки для каждого промпта.

**Обязательные секции:**

```markdown
## Test Suite Overview    — Сводная таблица (пройдено/всего)
## Test Cases             — Индивидуальные кейсы (TC-001, TC-002...)
## Edge Cases             — Граничные случаи (EC-001, EC-002...)
## Metrics                — Метрики качества
## Regression             — История регрессий по версиям
```

**Формат тест-кейса:**

```markdown
### TC-001: <Краткое описание>

- **Input:** <входные данные>
- **Expected:** <ожидаемый результат>
- **Criteria:** <критерий оценки>
- **Status:** ✅ / ❌ / ⏳
```

**Правила:**
- Минимум 5 тест-кейсов на промпт
- Каждый кейс — воспроизводимый сценарий
- Criteria должны быть измеримы и объективны
- Status должен отражать реальный результат

### 4. `changelog.md` — История изменений

Лог всех изменений с Semantic Versioning.

**Формат версии:**

```markdown
## [v1.1.0] — 2025-07-12

| Field    | Value              |
|----------|--------------------|
| Version  | v1.1.0             |
| Date     | 2025-07-12         |
| Author   | <author>           |
| Type     | feat / fix / refactor / docs / test / chore |
| Summary  | <краткое описание> |

### Changes
- ...

### Breaking Changes
- ... (если есть)
```

**Типы изменений:** (Semantic Versioning)

Полная таблица типов и версионирования: [conventions.md — Semantic Versioning](conventions.md#semantic-versioning)

## Процесс создания нового промпта

```
1. Изучи conventions.md и governance.md
2. Скопируй шаблоны из templates/
3. Создай директорию: prompts/<role-name>/
4. Напиши prompt.md (ядро — 7 секций)
5. Напиши card.md (документация)
6. Напиши test-cases.md (минимум 5 кейсов)
7. Заполни changelog.md (версия v1.0.0)
8. Запусти валидацию: python scripts/validate.py prompts/<role-name>/
9. Создай PR с checklist
10. Получи approval от Reviewer
11. Merge через Maintainer
12. Обнови README.md библиотеки
```

## Процесс обновления промпта

```
1. Протестируй текущую версию через test-cases
2. Внеси изменения в prompt.md
3. Обнови card.md (metadata, status)
4. Добавь/обнови test-cases
5. Запиши изменение в changelog.md (bump version)
6. Запусти валидацию: python scripts/validate.py prompts/<role-name>/
7. Создай PR с checklist
8. Получи approval от Reviewer
9. Merge через Maintainer
```

## Pull Request Process

> Полный PR Process описан в [governance.md](governance.md).

### Checklist PR

Полный чеклист: [governance.md — PR Checklist](governance.md#pr-checklist)

### Review Criteria

1. **Консистентность** — соответствует conventions
2. **Полнота** — все файлы обновлены
3. **Тесты** — покрывают изменения
4. **Impact** — не сломает existing users
5. **Ясность** — можно понять без доп. контекста

## Валидация

### Автоматическая

```bash
# Валидировать все промпты
python scripts/validate.py

# Валидировать конкретный промпт
python scripts/validate.py prompts/python-architect

# Строгий режим (warnings = errors)
python scripts/validate.py --strict

# JSON-вывод для CI
python scripts/validate.py --json
```

### Ручная (Quality Gates)

Полные quality gates: [governance.md — Quality Gates](governance.md#quality-gates)

## Валидация промпта

Каждый промпт должен пройти:

| Критерий | Описание |
|----------|----------|
| **Контракт** | Соответствует ли вывод ожидаемому формату? |
| **Границы** | Не выходит ли за область ответственности? |
| **Приоритеты** | Нет ли противоречий в правилах? |
| **Edge-cases** | Как ведёт себя на граничных входах? |
| **Регрессия** | Проходят ли все тест-кейсы? |

## Best Practices

1. **Одна роль — один промпт.** Не смешивай несвязанные зоны ответственности.
2. **Детерминированность.** Промпт должен давать предсказуемый результат на одинаковых входах.
3. **Иерархия правил.** Чётко разграничь must / should / can.
4. **Минимум воды.** Каждый абзац должен нести полезную информацию.
5. **Регулярный ревью.** Минимум раз в квартал проверяй актуальность.
6. **Промпт — это код.** Treat it like production code: review, test, version.
7. **Измеряй качество.** Используй метрики для принятия решений.

## Governance

Полный документ по управлению библиотекой: [governance.md](governance.md)

## Metrics

Система метрик и дашборд: [metrics.md](metrics.md)

