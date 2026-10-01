# Mission: configure AI coding agents on real projects (the harness, not the prompt)

## Why
Most developers use Claude Code, Codex or Antigravity as a chat. Agents then quietly make decisions that belong to the human: they downgrade a framework, trade correctness for a green test, or commit without asking. This tutorial takes a developer from "prompt-driven chat" to "a repo whose rules, skills, reviewers and guards steer any agent".

## Success looks like
- In about 30 minutes, on a fresh repo and before any feature code, you commit an `AGENTS.md` index, one skill, one reviewer agent, and one hook or permission rule.
- A fresh agent session, given an unseen task in your repo, follows your invariants, runs your skills, and stops with a 1-3-1 hand-over when it is stuck (the swap test).
- Every commit is a reviewed slice made through a commit skill, with your work identity, no AI trailer, no secrets and no build output.

## Constraints
- For experienced developers who are new to agent configuration: dense, not dumbed down; each term defined once.
- Tool-neutral first (AGENTS.md, `.agents/skills`), then Claude Code, with Codex and Antigravity equivalents.
- The examples use .NET 8 (ASP.NET Core, EF Core + SQLite, xUnit); the ideas apply to any stack.
- Every lesson starts from a real, anonymised incident.
- Version-specific behaviour is flagged with the date it was verified.

## Out of scope
- Prompt-writing technique for its own sake.
- Building MCP servers or plugins.
