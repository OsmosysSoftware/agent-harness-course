---
name: quality-gate
description: Run the format, build and test gate for this .NET solution and report the first failure. Use after every slice and before every commit, or when the user asks "is it green?".
---

# Quality gate

Run `bash .agents/skills/quality-gate/gate.sh` from the repository root.
It runs three steps and stops at the first failure:

1. `dotnet format --verify-no-changes`: formatting matches `.editorconfig`
2. `dotnet build -warnaserror`: no warnings, no errors
3. `dotnet test --no-build`: every test passes

Then:
- **Green**: report "quality gate: green" with the test count line.
- **Red**: quote the failing step's first error verbatim (file:line and message), then fix it.
  - Formatting: run `dotnet format` and re-run the gate.
  - Build or test: fix the cause in the code the slice touched.
  - **Never** delete, skip (`[Fact(Skip=…)]`) or weaken a test to go green.
  - **Never** change production logic to suit a test tool (for example, rewriting an atomic UPDATE so that
    EF InMemory can run it). If the only way to green touches an invariant, stop and use 1-3-1.
- After two failed fix attempts on the same error, stop and use 1-3-1.
