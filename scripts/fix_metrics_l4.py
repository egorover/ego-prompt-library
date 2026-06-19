#!/usr/bin/env python3
"""Fix metrics-l4.md quality section."""

from pathlib import Path

p = Path("docs/metrics-l4.md")
content = p.read_text(encoding="utf-8")

old = """### Quality Rating

```markdown
# Quality Ratings: <role-name>

## 2026-06

| Date       | User | Relevance | Completeness | Structure | Value | Avg |
|------------|------|-----------|--------------|-----------|-------|-----|
| 2026-06-19 | alice | 5 | 4 | 5 | 4 | 4.5 |
| 2026-06-19 | bob   | 4 | 5 | 4 | 5 | 4.5 |
```"""

new = """### Quality Rating

```markdown
# Quality Ratings: <role-name>

## 2026-06

| Date | User | Relevance | Completeness | Structure | Value | Scenario | Notes | Avg |
|------|------|-----------|--------------|-----------|-------|----------|-------|-----|
| 2026-06-19 | alice | 5 | 4 | 5 | 4 | Написание функции | Отличный код | 4.5 |
| 2026-06-19 | bob | 4 | 5 | 4 | 5 | Дебаггинг | Чёткое решение | 4.5 |
```"""

if old in content:
    content = content.replace(old, new)
    p.write_text(content, encoding="utf-8")
    print("[OK] Updated docs/metrics-l4.md")
else:
    print("[WARN] Pattern not found — content may already be different")
