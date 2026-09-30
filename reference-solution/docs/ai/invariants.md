# Invariants

These rules hold for every change. A change that breaks one is wrong, even if the tests pass.

## 1. Stock never goes below zero, even under concurrency
- A stock decrement is a single guarded UPDATE:
  `db.Products.Where(p => p.Id == id && p.Stock >= qty).ExecuteUpdateAsync(...)`.
  If 0 rows are affected, there wasn't enough stock (or the product is missing). Decide 404 or 409 after that.
- **Forbidden pattern:** load the entity, check `Stock`, assign `Stock -= qty`, `SaveChanges`.
  Without a write lock, two requests both read 3 and both write 0: 6 units sold of 3 (an oversell).
  On SQLite it only *looks* safe inside `BeginTransaction()`, because Microsoft.Data.Sqlite takes the
  write lock immediately. Drop the transaction (EF InMemory forces that) or move to SQL Server
  (READ COMMITTED) and it oversells. The guarded UPDATE is safe on any provider.
- The decrement and the order insert run in one transaction.
- Returning stock (cancel, refund) is also a single UPDATE, in a transaction with the state change.
- The guard test is `tests/StockApi.Tests/ConcurrencyTests.cs`: 12 concurrent orders for a product with
  3 units must yield exactly 3 successes. Any stock change must keep it green.
- Why: docs/decisions/0001-atomic-guarded-update.md

## 2. The contract is the brief
- Endpoints are exactly those in `BRIEF.md` plus the ones a human-approved plan adds.
- Out of scope: authentication, UI, payments.

## 3. Environment
- Target framework `net8.0`. If the SDK is missing, that is a 1-3-1, not a downgrade.
- Do not start, stop or install software on the machine (Docker, SDKs, databases). Ask.

## 4. Secrets
- No keys, passwords or connection strings with credentials in tracked files.
- Put real values in `.env` (git-ignored), and document the names in `.env.example`.
