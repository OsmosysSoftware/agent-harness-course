# Conventions

- Layout: `Controllers/` (HTTP; simple reads may use `StockDbContext` directly, like `ProductsController`), `Services/`
  (rules, transactions and every stock change), `Domain/` (entities), `Data/` (DbContext).
- The reference shape for a resource is `ProductsController` + its tests. Copy it (skill `new-endpoint`).
- Errors are `ProblemDetails`: 400 validation, 404 missing, 409 conflict (duplicate SKU, insufficient stock).
- Everything is async, with a `CancellationToken` passed through.
- Nullable is enabled, and warnings are errors (`Directory.Build.props`).
- Versions: `net8.0`, EF Core 8.0.x. For any library API you are not sure of, look it up (context7 MCP)
  instead of relying on memory.
- SQLite can't ORDER BY or compare `DateTimeOffset` in SQL; store it with `DateTimeOffsetToBinaryConverter`.
  See the [EF Core SQLite limitations](https://learn.microsoft.com/en-us/ef/core/providers/sqlite/limitations).
- Comments: one or two lines, and the "why" points to docs, e.g. `// see docs/decisions/0001`.
