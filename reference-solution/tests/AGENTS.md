# Tests: agent instructions

Loaded in addition to the root AGENTS.md when working in `tests/`.

- Real SQLite only (shared in-memory connection via `StockApiFactory`). EF InMemory is forbidden.
- Do not weaken a test to make it pass. If production code and a test disagree, 1-3-1.
- Every stock-changing endpoint has a concurrency test: N parallel requests, assert successes ≤ stock.
- Full rules: ../docs/ai/testing.md
