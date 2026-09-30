---
paths:
  - "src/**/Data/**/*.cs"
  - "src/**/Services/**/*.cs"
---

# EF Core rules (Claude Code only; loaded when you read files under Data/ or Services/)

- Stock changes: one guarded `ExecuteUpdateAsync` in a transaction (docs/decisions/0001).
- `DateTimeOffset` columns need `DateTimeOffsetToBinaryConverter` on SQLite before any ORDER BY or comparison.
- Before using an EF Core API you are unsure of, query context7 for EF Core 8 docs.
