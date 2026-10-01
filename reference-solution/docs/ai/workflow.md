# Workflow

## The loop
1. **Explore**: read the relevant code and docs. Do not edit yet (plan mode, if your tool has one).
2. **Plan**: write or update `ai-session/PLAN.md`: slices, each with its test and the files it touches.
   The human edits and approves it. The plan is committed on its own (`docs(plan): …`) before any code.
3. **One slice**: implement only the next unchecked slice in the plan.
4. **Quality gate**: run the `quality-gate` skill. Fix failures; if a fix would touch an invariant, use 1-3-1.
5. **Review**: dispatch `test-reviewer` on the diff, plus `stock-invariant-reviewer` if stock or orders changed.
   Report its findings to the human. The author never grades its own work.
6. **Commit**: run the `commit` skill. It drafts the message and waits for approval. Never push.
7. Tick the slice in `PLAN.md` and go back to step 3.

## When requirements change mid-task
Stop the current slice. Update `PLAN.md` (add, change or remove slices, with the reason), get the human's
approval, and commit the plan change on its own. Then continue. Never absorb a new requirement into
a slice silently.

## Git rules
- One slice per commit, Conventional Commits, company email, no AI co-author trailers.
- Never rewrite history (`rebase`, `reset --hard`, `commit --amend` on pushed work, force-push).
- Never stage `bin/`, `obj/`, `tmp/`, `*.db` or `.env`.

## When stuck
Use 1-3-1 (see AGENTS.md). Do not poll or retry blindly: after one failed retry, hand over.
