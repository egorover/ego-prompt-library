# Python Architect — Changelog

## [v1.1.0] — 2025-07-12

| Field    | Value              |
|----------|--------------------|
| Version  | v1.1.0             |
| Date     | 2025-07-12         |
| Author   | ego-prompt-library |
| Type     | feat               |
| Summary  | Complete prompt rewrite with 7-section structure |

### Changes
- Полная переписывание prompt.md по структуре conventions (7 разделов)
- Добавлены Decision Framework с приоритетами (Must/Should/Can)
- Добавлены Anti-Patterns и Quick Reference
- Обновлена card.md: заполнены все секции, исправлены ссылки
- Обновлены test-cases.md: добавлены 2 кейса, метрики, edge-cases
- Статус карточки изменён на `validated`

### Breaking Changes
- Изменена структура prompt.md (несовместима с v1.0.0 парсерами)

---

## [v1.0.0] — 2025-07-12

| Field    | Value              |
|----------|--------------------|
| Version  | v1.0.0             |
| Date     | 2025-07-12         |
| Author   | ego-prompt-library |
| Type     | feat               |
| Summary  | Initial version    |

### Changes
- Инициальная версия промпта
- Создана базовая структура (описание, контекст, задачи, ограничения)
- Создана карточка роли
- Добавлены 5 базовых тестовых случаев