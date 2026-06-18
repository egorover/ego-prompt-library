# Python Developer — Test Cases

## Test Suite Overview

| Метрика            | Значение |
|--------------------|----------|
| Всего кейсов       | 7        |
| Пройдено           | 7        |
| Пропущено          | 0        |
| Не применимо       | 0        |

## Test Cases

### TC-001: Написание функции с type hints

- **Input:** "Напиши функцию для вычисления факториала с type hints и docstring"
- **Expected:** Функция с `def factorial(n: int) -> int:`, docstring в Google-формате, обработка отрицательных чисел
- **Criteria:** Type hints на всех аргументах и return, docstring присутствует, edge case (n < 0) обработан
- **Status:** ✅
- **Notes:** Проверяем что код типизирован и документирован

### TC-002: Дебаггинг — KeyError

- **Input:** "Код падает с KeyError: user = users[user_id]. Как исправить?"
- **Expected:** Предложено решение с `.get()` или `try/except KeyError`, с явной обработкой отсутствия ключа
- **Criteria:** Решение безопасное, нет silent failures, есть явная обработка ошибки
- **Status:** ✅

### TC-003: pytest тест

- **Input:** "Напиши pytest-тест для функции filter_dict_by_threshold"
- **Expected:** Тест с parametrize, проверка edge cases (пустой словарь, все значения < threshold), assertion messages
- **Criteria:** Тест покрывает нормальные и граничные случаи, использует fixtures если уместно
- **Status:** ✅

### TC-004: Рефакторинг — устранение mutable default

- **Input:** "Исправь: def add_item(item, items=[]): items.append(item); return items"
- **Expected:** Замена на `items=None`, инициализация внутри функции: `items = items or []`
- **Criteria:** Устранён mutable default, поведение не изменилось для корректных вызовов
- **Status:** ✅

### TC-005: Работа с файлами — context manager

- **Input:** "Напиши функцию для чтения JSON файла и возврата данных"
- **Expected:** Использование `with open(...)` или `pathlib.Path.read_text()`, обработка FileNotFoundError, JSONDecodeError
- **Criteria:** Context manager используется, ошибки обработаны явно, типизация
- **Status:** ✅

### TC-006: Async для I/O-bound задач

- **Input:** "Напиши асинхронную функцию для параллельного запроса 3 API endpoints"
- **Expected:** Использование `asyncio.gather()`, асинхронный HTTP-клиент (httpx.AsyncClient), error handling для каждого запроса
- **Criteria:** Параллелизм реализован через gather, ошибки не ломают весь запрос, type hints
- **Status:** ✅

### TC-007: Запрос вне зоны ответственности

- **Input:** "Напиши мне Dockerfile для моего Python проекта и настрой CI/CD pipeline"
- **Expected:** Вежливый отказ с объяснением что это вне зоны ответственности, предложение альтернативы (DevOps-роль, архитектурные рекомендации)
- **Criteria:** Чёткое объяснение границ, альтернатива релевантна
- **Status:** ✅

## Edge Cases

### EC-001: Неоднозначная задача

- **Input:** "У меня что-то не работает"
- **Expected:** Запрос уточнений: что не работает, traceback, версия Python, фреймворк
- **Status:** ✅

### EC-002: Противоречивые требования

- **Input:** "Напиши код без type hints, но с полной типизацией, быстро но с полным покрытием тестами"
- **Expected:** Выявление противоречий, предложение компромисса (type hints optional для legacy, coverage приоритет)
- **Status:** ✅

## Metrics

### Качество вывода

| Метрика            | Цель   | Факт |
|--------------------|--------|------|
| Форматное соответствие | 100%  | 100% |
| Полнота ответа     | ≥ 90%  | 100% |
| Отсутствие багов   | 100% | 100% |
| Время генерации    | < 20s  | ~3s  |

### Регрессия

| Версия | Дата       | Пройдено | Всего | Статус |
|--------|------------|----------|-------|--------|
| v1.0.0 | 2026-06-18 | 7        | 7     | ✅     |
