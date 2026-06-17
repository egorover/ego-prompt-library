# Ego Prompt Library

> Production-ready библиотека командных промптов с governance, тестами и CI.
> Промпты управляются как код: code review, версионирование, метрики, депрекация.

## Maturity Ladder

Эта библиотека спроектирована для достижения **уровня 4 (Governed & Measured)**:

| Уровень | Название | Статус |
|---------|----------|--------|
| 1. Personal | Личный промпт | ✅ Пройден |
| 2. Team Template | Командный шаблон | ✅ Пройден |
| 3. Library Asset | Элемент библиотеки | ✅ Пройден |
| 4. Governed & Measured | Управляемый и контролируемый | 🟢 В процессе |

## Структура

```
ego-prompt-library/
├── README.md                  # Этот файл
├── .gitignore
├── prompts/                   # Промпты (production артефакты)
│   └── python-architect/      # ← один промпт = одна директория
│       ├── prompt.md          # Системный промпт (7 секций)
│       ├── card.md            # Карточка роли (metadata, input/output, scope)
│       ├── test-cases.md      # Тесты (TC + Edge Cases + Metrics)
│       └── changelog.md       # История изменений (SemVer)
├── docs/                      # Документация
│   ├── playbook.md            # Руководство: создание, обновление, валидация
│   ├── conventions.md         # Соглашения: форматирование, структуры, шаблоны
│   └── governance.md          # Управление: roles, PR, review, metrics, deprecation
├── templates/                 # Шаблоны для новых промптов
│   ├── prompt-template.md
│   ├── card-template.md
│   ├── test-template.md
│   └── changelog-template.md
└── scripts/                   # Валидация и CI
    ├── validate.py            # CLI-валидатор структуры
    ├── ci-check.py            # CI-скрипт для GitHub Actions
    └── README.md
```

## Промпты

| Промпт | Версия | Статус | Описание |
|--------|--------|--------|----------|
| [python-architect](prompts/python-architect/) | v1.1.0 | ✅ validated | AI-роль для проектирования архитектуры Python-проектов |

## Быстрый старт

### Использование промпта

1. Открой `prompts/<role>/prompt.md`
2. Скопируй содержимое в system message AI-ассистента
3. Готово — роль активна

### Создание нового промпта

```bash
# 1. Скопируй шаблоны
cp templates/* prompts/my-new-role/

# 2. Заполни файлы согласно conventions.md
# 3. Запусти валидацию
python scripts/validate.py prompts/my-new-role/

# 4. Создай PR → review → merge
```

### Валидация

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

## Governance

Полный процесс управления: [docs/governance.md](docs/governance.md)

- **Roles:** Owner, Reviewer, Maintainer
- **Process:** PR → Review → Merge
- **Versioning:** Semantic Versioning (v1.0.0, v1.1.0, v2.0.0)
- **Deprecation:** Grace period 2 release cycles
- **Review:** Quarterly review актуальности

## Metrics

Система метрик: [docs/metrics.md](docs/metrics.md)

Каждый промпт собирает:
- **Usage** — частота и сценарии использования
- **Test pass rate** — стабильность тестов
- **Latency** — время генерации
- **Quality** — оценка пользователя (1-5)
- **Dashboard** — сводка с трендами

## License

Внутренняя библиотека.
