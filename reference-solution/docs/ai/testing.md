# Testing

- Integration tests use `WebApplicationFactory<Program>` over **real SQLite**, in memory, on one shared
  open `SqliteConnection("Filename=:memory:")` per factory (see `tests/StockApi.Tests/StockApiFactory.cs`).
- **Never use the EF Core InMemory provider.** It can't run `ExecuteUpdateAsync`, and it rejects transactions by default.
  Microsoft "strongly discourages" it for testing. If a test can't run production code, change the
  test setup, never the production code. If neither works, use 1-3-1.
- Every stock change needs a concurrency test (see `ConcurrencyTests.cs`).
- A test must fail if the feature breaks. For each assertion, be able to name the production line
  whose removal makes it fail.
- Names: `Method_Condition_Result`, e.g. `PlaceOrder_InsufficientStock_Returns409AndKeepsStock`.
