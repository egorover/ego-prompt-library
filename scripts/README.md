# Prompt Library Scripts

## Scripts

### `validate.py` — Валидация структуры

```bash
# Валидировать все промпты
python scripts/validate.py

# Конкретный промпт
python scripts/validate.py prompts/python-architect

# Строгий режим (warnings = errors)
python scripts/validate.py --strict

# JSON-вывод для CI
python scripts/validate.py --json
```

### `metrics-collector.py` — Сбор метрик

```bash
# Собрать метрики для всех промптов
python scripts/metrics-collector.py --all

# Конкретный промпт
python scripts/metrics-collector.py prompts/python-architect

# Обновить dashboards
python scripts/metrics-collector.py --all --dashboard

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

## GitHub Actions

| Workflow | Файл | Когда |
|----------|------|-------|
| Prompt CI | `.github/workflows/prompt-ci.yml` | PR/push (validate + metrics) |
| Dashboard Update | `.github/workflows/dashboard-update.yml` | Monthly/Manual |

## Entry points (pip install -e .)

| Команда | Модуль |
|---------|--------|
| `prompt-validate` | `scripts.validate:main` |
| `prompt-metrics` | `scripts.metrics.__main__:main` |
| `prompt-report` | `scripts.report_cli:main` |
