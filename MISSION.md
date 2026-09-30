# Mission: Configuring AI coding agents on real projects (the harness, not the prompt)

## Why
Osmosys .NET trainees already use Claude Code, Codex or Antigravity, but only as a single chat. In the last agentic assessment none of the six reviewed repos had a harness, and the agents made the human's decisions for them. The next assessment grades the harness in the first 30 minutes and then runs a swap test. This course gets each trainee from "prompt-driven chat" to "a repo whose rules, skills, reviewers and guards steer any agent", before that assessment.

## Success looks like
- In 30 minutes, on a fresh starter repo and before any feature code: commit an `AGENTS.md` index, one skill, one reviewer agent, and one hook or permission rule (checkpoint 1).
- A fresh agent session given an unseen task in their repo follows the invariants, runs their skills, and stops with a 1-3-1 hand-over when it is stuck (the swap test).
- Every commit is a reviewed slice that goes through a commit skill, with the company identity, no AI trailer, no secrets and no build output.
- They can say which guard type blocks which failure, and they can show their own rejections in a raw transcript.

## Constraints
- Experienced developers who are new to agent configuration: dense, not dumbed down; define each term once.
- Tool-neutral first (AGENTS.md, `.agents/skills`), then Claude Code, with the Codex and Antigravity equivalent shown for each.
- .NET 8 stack throughout: ASP.NET Core, EF Core + SQLite, xUnit.
- Every lesson starts from a real incident in `ai-assessment-review.html`.
- Version-specific behaviour is flagged with the date it was verified.

## Out of scope
- Prompt-writing technique for its own sake.
- Building MCP servers or plugins (they only use existing ones).
- CI pipelines beyond one mention; the graded harness is local.
