---
name: update-docs
description: Audit docs/ai/*.md, AGENTS.md and README.md against the actual code and propose corrections. Use after a feature lands, before a submission, or when the user asks whether the docs are still true.
---

# Update docs

Docs written from memory drift. This skill compares every claim with the code.

1. List each factual claim in `AGENTS.md`, `docs/ai/*.md`, `docs/decisions/*.md` and `README.md`:
   commands, endpoints, invariants, file paths, versions, "we decided X".
2. For each claim, find the evidence: the file:line, a `git log` entry or a test. Classify it:
   **TRUE** (with evidence), **STALE** (with what the code does now) or **UNVERIFIABLE**.
3. Print a table: claim · verdict · evidence.
4. Propose edits for STALE claims only, as a diff. Do not apply them until the human approves.
5. Never add narrative ("we carefully considered…"). Docs here are instructions for the next agent.
