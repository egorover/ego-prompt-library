# Latency: python-dev

## Latency Measurements

| TC       | P50  | P95  | P99  | Notes |
|----------|------|------|------|-------|
| TC-001   | 3s   | 4s   | 5s   | Простая функция |
| TC-002   | 2s   | 3s   | 4s   | Дебаггинг |
| TC-003   | 4s   | 5s   | 6s   | pytest тесты |
| TC-004   | 3s   | 4s   | 5s   | Рефакторинг |
| TC-005   | 5s   | 7s   | 8s   | Работа с файлами |
| TC-006   | 6s   | 8s   | 10s  | Async |
| TC-007   | 2s   | 3s   | 3s   | Отказ |

## Summary

- **P50:** 3s
- **P95:** 5s
- **P99:** 6s
- **Target P50 < 15s:** 🟢 Pass
