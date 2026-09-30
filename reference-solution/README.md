# StockApi

A tiny inventory service (.NET 8, ASP.NET Core, EF Core + SQLite). See `BRIEF.md`.
Agent instructions live in `AGENTS.md`; this file is for humans.

```bash
git config core.hooksPath .githooks            # once per clone: enables pre-commit and commit-msg
dotnet run --project src/StockApi              # creates stock.db on first start
bash .agents/skills/quality-gate/gate.sh       # format check, build -warnaserror, test
```

Endpoints:
- `GET /api/products`, `GET /api/products/{id}`, `GET /api/products/low-stock?threshold=5`
- `POST /api/products` `{sku,name,stock}`
- `GET /api/orders?productId=` (newest first)
- `POST /api/orders` `{productId,quantity}`

Configuration: copy `.env.example` to `.env` (git-ignored) for local overrides.
