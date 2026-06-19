# Metrics — Система измерений для prompt library

## Обзор

На **Уровне 4 (Governed & Measured)** каждый промпт измеряется по 6 ключевым метрикам.
Данные собираются автоматически через CI и вручную через скрипты.

## Ключевые метрики

| Метрика | Что считаем | Источник | Цель | Частота |
|---------|-------------|----------|------|---------|
| **Usage count** | Количество обращений/версий | changelog.md | растёт | weekly |
| **Test pass rate** | % пройденных тест-кейсов | test-cases.md | ≥ 95% | per change |
| **Latency P50/P95/P99** | Время генерации ответа | latency.md | P50 < 15s | monthly |
| **Quality Avg** | Средняя оценка пользователя | quality.md | ≥ 4.0 | monthly |
| **Changes/mo** | Количество PR в месяц | changelog.md | ≤ 2 | weekly |
| **Open issues** | Нерешённые проблемы | card.md status | < 3 | weekly |

## Структура метрик

Каждый промпт имеет директорию `metrics/`:

```
prompts/<role>/
└── metrics/
    ├── dashboard.md      # Сводка: usage, test%, latency, quality
    ├── usage.md          # Лог использований
    ├── quality.md        # Оценки качества (rating 1-5)
    └── latency.md        # Замеры времени генерации
```

## Автоматический сбор

### Скрипт метрик

```bash
# Собрать метрики для всех промптов
python scripts/metrics-collector.py --all

# Конкретный промпт
python scripts/metrics-collector.py prompts/python-architect

# Обновить dashboards
python scripts/metrics-collector.py --dashboard

# JSON-вывод для CI
python scripts/metrics-collector.py --all --json > metrics.json
```

### Что собирает metrics-collector.py

| Что | Как |
|-----|-----|
| Usage count | Считает версии в changelog.md |
| Test pass rate | Считает ✅/❌/⏳ в test-cases.md |
| Latency P50/P95/P99 | Парсит latency.md, вычисляет перцентили |
| Quality Avg | Среднее из quality.md ratings |
| Changes/mo | Считает changelog entries за текущий месяц |
| Version/Status | Извлекает из card.md metadata |

## Генерация отчётов

### Markdown-отчёт

```bash
python scripts/report.py --output report.md
```

### HTML-дашборд

```bash
python scripts/report.py --html --output dashboard.html
```

### JSON для CI

```bash
python scripts/report.py --json --output report.json
```

## Quality Gates

### Gate 1: Per-Change (CI)

| Метрика | 🟢 Норма | 🟡 Внимание | 🔴 Критично |
|---------|----------|-------------|-------------|
| Test pass rate | ≥ 95% | 80-95% | < 80% |
| Latency P50 | < 15s | 15-30s | > 30s |
| Quality Avg | ≥ 4.0 | 3.0-4.0 | < 3.0 |

**Действие:** CI блокирует merge при критических нарушениях.

### Gate 2: Monthly Review

| Метрика | 🟢 Норма | 🟡 Внимание | 🔴 Критично |
|---------|----------|-------------|-------------|
| Usage count | растёт | стабильно | падает > 30% |
| Changes/mo | ≤ 2 | 3-5 | > 5 |
| Open issues | < 3 | 3-5 | > 5 |

**Действие:** Автоматический отчёт + review в понедельник.

### Gate 3: Quarterly Review

| Метрика | 🟢 Норма | 🟡 Внимание | 🔴 Критично |
|---------|----------|-------------|-------------|
| Stale prompts | 0 | < 10% | ≥ 10% |
| Deprecated | planned | active | missing |
| Test coverage | ≥ 7 TC | 5-6 TC | < 5 TC |

**Действие:** Создаётся issue для ручного review.

## Dashboard

### Dashboard Update Workflow

Запускается автоматически:
- **Ежемесячно** (1-е число, 09:00 UTC) — обновляет dashboards
- **Quarterly** — генерирует полный отчёт + создаёт issue для review

```yaml
# .github/workflows/dashboard-update.yml
# Запускается по schedule и вручную
```

### Dashboard файл

```markdown
# Dashboard: <role-name>

## Summary (2026-06-19)

| Метрика            | Значение | Статус | Тренд  |
|--------------------|----------|--------|--------|
| Usage count        | 5        | ⚪     | → рост |
| Test pass rate     | 100%     | 🟢     | → стаб |
| Latency P50        | 5s       | 🟢     | —      |
| Quality Avg        | 4.2      | 🟢     | —      |
| Changes (this mo)  | 1        | 🟢     | —      |
| Open issues        | 0        | 🟢     | —      |
```

## Ручной сбор метрик

### Usage Log

```markdown
# Usage Log: <role-name>

## 2026-06

| Date       | User  | Scenario            | Source     |
|------------|-------|---------------------|------------|
| 2026-06-19 | alice | Декомпозиция монолита | direct     |
| 2026-06-19 | bob   | Выбор паттерна       | PR #42     |
```

### Quality Rating

```markdown
# Quality Ratings: <role-name>

## 2026-06

| Date | User | Relevance | Completeness | Structure | Value | Scenario | Notes | Avg |
|------|------|-----------|--------------|-----------|-------|----------|-------|-----|
| 2026-06-19 | alice | 5 | 4 | 5 | 4 | Написание функции | Отличный код | 4.5 |
| 2026-06-19 | bob | 4 | 5 | 4 | 5 | Дебаггинг | Чёткое решение | 4.5 |
```

## Автоматизация

### CI Pipeline

```
PR push → validate → metrics → quality-gate → merge
```

1. **validate** — структура файлов, обязательные секции
2. **metrics** — сбор метрик, обновление dashboards
3. **quality-gate** — проверка порогов, комментарий в PR

### GitHub Actions

| Workflow | Когда | Что делает |
|----------|-------|------------|
| `prompt-ci.yml` | PR/push | Валидация + метрики + quality gate |
| `dashboard-update.yml` | Monthly/Manual | Обновление dashboards + quarterly review |

## Troubleshooting

### Метрики не собираются

1. Проверь что `metrics/` директория существует
2. Убедись что файлы не пустые
3. Запусти `python scripts/metrics-collector.py --all --json` для отладки

### Dashboard не обновляется

1. Проверь CI logs
2. Убедись что `GITHUB_TOKEN` имеет права на push
3. Запусти вручную: `workflow_dispatch`

### Качество низкое

1. Проверь test-cases — покрывают ли они реальные сценарии
2. Собери feedback от пользователей
3. Пересмотри Output Format и Anti-Patterns
4. Добавь regression tests

## Best Practices

1. **Собирай метрики регулярно.** Ручной сбор лучше чем ничего.
2. **Обновляй dashboard после каждого значимого изменения.**
3. **Используй CI для автоматизации.** Не полагайся на ручной сбор.
4. **Quarterly review — обязательный.** Не пропускай.
5. **Тренды важнее абсолютных значений.** Растёт или падает?
6. **Quality > Quantity.** 5 хороших тестов лучше 20 плохих.
