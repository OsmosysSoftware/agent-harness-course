# 0001: Stock changes use one guarded UPDATE, not read-then-write

- Status: accepted
- Date: 2026-09-30

## Context
Orders reserve stock. Under concurrency, a read-then-write (load `Product`, check `Stock >= qty`, assign,
`SaveChanges`) lets two requests read the same value and both succeed. This is how a real
session's code oversold: 12 concurrent orders for 3 units succeeded more than 3 times. It was introduced to
make EF Core InMemory tests pass, because InMemory can't translate `ExecuteUpdateAsync` (and it rejects
transactions by default, so the rewrite loses those too).

On SQLite, read-then-write inside `BeginTransaction()` happens to be serialised: Microsoft.Data.Sqlite starts a
non-deferred transaction, which takes the write lock up front
([docs](https://learn.microsoft.com/en-us/dotnet/standard/data/sqlite/transactions)). That is an accident of one
provider, not a design. We measured it: read-then-write *inside* the transaction passes the concurrency test,
and read-then-write *without* it sells 12 of 3.

## Decision
- Decrement with one statement:
  `UPDATE Products SET Stock = Stock - @q WHERE Id = @id AND Stock >= @q` (`ExecuteUpdateAsync`).
  SQLite runs one writer at a time, so the check and the write can't interleave.
- 0 affected rows means 404 (no product) or 409 (not enough stock).
- The decrement and the order insert share one transaction.
- Tests run on real SQLite. `ConcurrencyTests` is the guard: 12 parallel orders for 3 units give exactly 3 successes.

## Consequences
- EF InMemory can't be used for order tests. That is accepted; see docs/ai/testing.md.
- Anyone "simplifying" this to tracked entities breaks the invariant, and `stock-invariant-reviewer` blocks it,
  even when the concurrency test is still green. The test can't see portability; the reviewer can.
- If the database changes (for example to SQL Server), the same statement stays correct. Revisit only the busy-timeout setting.
