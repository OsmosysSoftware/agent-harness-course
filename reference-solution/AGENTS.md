# StockApi: agent instructions

A small inventory API: products with a unique SKU and a stock count; orders reserve stock.
.NET 8, ASP.NET Core controllers, EF Core + SQLite, xUnit. Brief: `BRIEF.md`.

## Commands
- Build: `dotnet build -warnaserror`
- Test: `dotnet test`
- Format check: `dotnet format --verify-no-changes`
- Run: `dotnet run --project src/StockApi` (API on the port printed at startup)

## Definition of done (every slice)
1. The quality gate passes: format check, then build, then test (skill `quality-gate`).
2. A reviewer agent has read the diff: `test-reviewer` always; `stock-invariant-reviewer` when stock or orders change.
3. The human has approved the commit message drafted by the `commit` skill. Never commit or push otherwise.

## Invariants (never break; details in docs/ai/invariants.md)
- Stock never goes below zero, including under concurrent orders.
- Every stock change is ONE guarded UPDATE (`ExecuteUpdateAsync` with `Stock >= n` in the WHERE); never read-then-write.
- Target framework is `net8.0`. Do not change it.
- Out of scope: auth, UI, payments. Decline and say so if asked to add them.
- No secrets in git: config values come from environment variables; `.env` is git-ignored.

## When you are stuck: 1-3-1
If a tool, SDK, test provider or environment blocks you, or a fix would change an invariant,
a requirement or the machine: STOP. Do not work around it. Reply with exactly
- **1 problem**: what is blocked and why it matters,
- **3 options**, with the trade-off of each,
- **1 recommendation**,
then wait for the human's decision. Never install, launch, downgrade or delete to get unstuck.

## Workflow
Plan first, then one slice at a time: docs/ai/workflow.md

## More context (read when relevant)
- Invariants and why: docs/ai/invariants.md
- Code layout and naming: docs/ai/conventions.md
- How to test (no EF InMemory): docs/ai/testing.md
- Deliberate decisions: docs/decisions/
