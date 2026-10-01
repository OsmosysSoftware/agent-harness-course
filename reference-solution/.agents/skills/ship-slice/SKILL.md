---
name: ship-slice
description: Build the next unchecked slice of ai-session/PLAN.md end to end (test, code, quality gate, reviews, commit), stopping wherever a human decides. Use when the plan is approved and the user says to build, continue or ship the next slice.
disable-model-invocation: true
---

# Ship one slice

This is `docs/ai/workflow.md` steps 3 to 7 as one command. Steps marked **STOP** wait for the human.

0. **Check the start.** `ai-session/PLAN.md` must be committed on its own (`git log --oneline -- ai-session/PLAN.md`
   shows a `docs(plan): …` commit) and `git status` must be clean. If not, say which and stop.
1. **Pick the slice.** The first unchecked one in `PLAN.md`. Name it in one line. If the user asked for something
   the plan doesn't have, **STOP**: that is a requirement change (workflow.md, "When requirements change").
2. **Test first.** For an endpoint, follow the `new-endpoint` skill. Otherwise write the failing test, run it,
   and show it fail for the right reason.
3. **Code.** The smallest change that makes that test pass. Nothing outside the slice.
4. **Gate.** Run the `quality-gate` skill. Fix the cause, never the test. Same failure twice: hand over a 1-3-1.
   **STOP** if a fix would touch an invariant.
5. **Review.** Dispatch `test-reviewer`, plus `stock-invariant-reviewer` if stock or orders changed. Report each
   finding with its file:line. **STOP** on any BLOCK: the human decides.
6. **Commit.** Tick the slice in `PLAN.md`, then run the `commit` skill. It asks before staging and before
   committing. **STOP** there.
7. **Report and stop.** The commit hash, what the reviewers said, and the next unchecked slice. Never start the
   next slice yourself.
