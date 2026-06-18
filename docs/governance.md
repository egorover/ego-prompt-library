# Governance — Управление промптами как кодом

## Обзор

Этот документ определяет процессы, правила и ответственности за управление промптами
в библиотеке. Промпты на этом уровне — не текст, а first-class артефакты,
равнозначные коду в продуктивной кодовой базе.

## Principles

1. **Промпт — это код.** Требует ревью, тестов, версионирования и документации.
2. **Изменения прозрачны.** Любой изменён может быть откатён через changelog.
3. **Качество измеримо.** Каждый промпт проходит через метрики и тесты.
4. **Ответственность ясна.** У каждого промпта есть owner и reviewers.
5. **Эволюция контролируема.** Deprecation и миграция — не хаотичные, а по процессу.

## Roles

| Роль           | Ответственность                                      | Кол-во |
|----------------|------------------------------------------------------|--------|
| **Owner**      | Создание и поддержка промпта, ревью изменений         | 1 на промпт |
| **Reviewer**   | Ревью PR с изменениями промпта                       | 1-2    |
| **Maintainer** | Глобальная консистентность библиотеки, merge PR       | 2-3    |
| **User**       | Потребитель промптов, создаёт issues при проблемах   | N      |

### Owner

- Единственный point-of-contact для промпта
- Принимает решения об изменениях в рамках conventions
- Обновляет карточку, тесты и метрики
- Проводит quarterly review

### Reviewer

- Проверяет PR на соответствие conventions
- Валидирует тест-кейсы
- Оценивает impact изменений на existing users

### Maintainer

- Управляет репозиторием (branches, CI, releases)
- Принимает/отклоняет крупные архитектурные изменения
- Управляет deprecation policy
- Ведёт changelog библиотеки

## Pull Request Process

### Когда нужен PR

| Изменение                        | PR нужен |
|----------------------------------|----------|
| Исправление опечатки в prompt.md | ✅       |
| Добавление нового тест-кейса     | ✅       |
| Обновление changelog             | ✅       |
| Создание нового промпта          | ✅       |
| Обновление шаблонов              | ✅       |
| Изменение conventions            | ✅       |

### Checklist PR

```markdown
## PR Checklist

- [ ] Соответствует conventions.md
- [ ] Обновлена card.md (metadata, status)
- [ ] Обновлены test-cases.md (добавлены/изменены кейсы)
- [ ] Обновлён changelog.md
- [ ] Все тест-кейсы прошли (указать статус)
- [ ] Owner подтвердил изменения
- [ ] Получено ≥1 approval от Reviewer
```

### Review Criteria

Reviewer проверяет:

1. **Консистентность** — соответствует ли conventions
2. **Полноту** — все ли файлы обновлены
3. **Тесты** — покрывают ли изменения тест-кейсы
4. **Impact** — не сломает ли это existing users
5. **Ясность** — можно ли понять изменение без доп. контекста

## Code Review Checklist

### Для prompt.md

- [ ] Нет противоречий между разделами
- [ ] Приоритеты (Must/Should/Can) не конфликтуют
- [ ] Output Format детерминирован
- [ ] Anti-Patterns актуальны
- [ ] Quick Reference покрывает частые кейсы

### Для card.md

- [ ] Metadata полная и актуальная
- [ ] Status соответствует реальному состоянию
- [ ] Input/Output описаны корректно
- [ ] Validation Status обновлён

### Для test-cases.md

- [ ] Новые кейсы покрывают новые сценарии
- [ ] Нет дублирующихся кейсов
- [ ] Criteria измеримы и объективны
- [ ] Status отражает реальный результат

## Branching Model

```
main (production)
  ├── feature/add-new-role
  ├── feature/improve-python-architect
  └── hotfix/fix-prompt-contradiction
```

### Правила

- **main** — защищённая ветка, только через PR с approval
- **feature/** — для новых промптов и крупных изменений
- **hotfix/** — для срочных исправлений, затем merge в main + merge back в feature

## Versioning Policy

Semantic Versioning для каждого промпта:

| Тип изменения       | Версия | Пример      |
|---------------------|--------|-------------|
| Breaking change     | MAJOR  | v2.0.0      |
| New feature         | MINOR  | v1.1.0      |
| Fix / refactor      | PATCH  | v1.0.1      |

### Что считается breaking change

- Изменение Output Format (структуры ответа)
- Удаление раздела из prompt.md
- Изменение Input/Output карточки
- Изменение семантики приоритетов (Must/Should/Can)

### Миграция при breaking change

1. Создать новую версию промпта (v2.x.x)
2. Старую пометить как `deprecated` в card.md
3. Добавить migration guide в changelog
4. Дать grace period (минимум 1 release cycle)

## Deprecation Policy

### Жизненный цикл промпта

```
draft → testing → validated → (deprecated) → removed
```

### Когда помечать deprecated

- Промпт заменён новым (v2)
- Промпт больше не актуален (технологии изменились)
- Промпт не используется > 6 месяцев
- Обнаружены критические антипаттерны

### Процесс deprecation

```
1. Owner создаёт PR: помечает Status = deprecated
2. В changelog добавляет reason и альтернативу
3. Grace period: 2 release cycle (минимум 30 дней)
4. После grace period: архивирует или удаляет
5. В README.md обновляет ссылку на замену
```

### Статус deprecation в текущей библиотеке

| Промпт | Заменён? | Причина |
|--------|----------|---------|
| python-architect (v1.1.0) | ❌ Нет | Активная версия |
| python-dev (v1.0.0) | ❌ Нет | Активная версия |

**Резюме:** ни один промпт не требует deprecation — все актуальны и используются.
Процесс документирован, но не применялся на практике.

## Metrics

### Что измеряем

| Метрика                | Где                           | Как часто |
|------------------------|-------------------------------|-----------|
| **Usage count**        | issue / PR references         | weekly    |
| **Test pass rate**     | test-cases.md Status          | per change|
| **Prompt latency**     | время генерации (замерять)    | monthly   |
| **Output quality**     | user feedback / rating        | monthly   |
| **Change frequency**   | changelog.md                  | weekly    |
| **Open issues**        | issues по промпту             | weekly    |

### Dashboard (руководство по интерпретации)

| Индикатор    | 🟢 Норма     | 🟡 Внимание    | 🔴 Критично    |
|-------------|--------------|----------------|----------------|
| Test pass   | ≥ 95%        | 80-95%         | < 80%          |
| Latency     | < 15s        | 15-30s         | > 30s          |
| Usage       | растёт       | стабильно      | падает > 30%   |
| Open issues | < 3          | 3-5            | > 5            |

## Quality Gates

### Gate 1: Pre-commit (Owner)

- [ ] Промпт отформатирован (UTF-8, LF, 120 chars)
- [ ] Нет placeholder-текста (`<...>`)
- [ ] Читаем и проверяем вручную

### Gate 2: CI Check (Automated)

- [ ] Структура файлов соответствует conventions
- [ ] Все обязательные секции присутствуют
- [ ] Markdown валиден

### Gate 3: Review (Reviewer)

- [ ] Соответствует checklist
- [ ] Тесты проходят
- [ ] Changelog обновлён

### Gate 4: Merge (Maintainer)

- [ ] ≥1 approval
- [ ] CI прошёл
- [ ] Version bumped корректно
- [ ] Changelog записан

## Quarterly Review

Каждый квартал (январь, апрель, июль, октябрь):

1. **Owner** проводит review всех своих промптов
2. Проверяет актуальность контекста и технологий
3. Обновляет метрики и статусы
4. Выявляет deprecated candidates
5. **Maintainer**汇总 результаты и принимает решения

## Emergency Process

### Критический баг в промпте

1. Owner создаёт hotfix PR (обходит обычный процесс)
2. → 1 reviewer (любой доступный)
3. Merge immediately → main
4. Post-mortem в течение 24 часов
5. Записать lessons learned

### Неудовлетворительный результат от промпта

1. User создаёт issue с example входа/выхода
2. Owner triage в течение 48 часов
3. Если подтверждено — hotfix или minor fix
4. Добавить в test-cases как regression test
