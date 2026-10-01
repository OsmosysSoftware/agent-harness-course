---
name: commit
description: Commit the current slice. Use whenever a slice has passed the quality gate and review and the work should be committed, or when the user says "commit". Drafts a Conventional Commit message from the staged diff, refuses secrets and build output, checks your work identity, and waits for human approval. Never pushes.
---

# Commit

Follow every step in order. If any check fails, stop and report; do not work around it.

1. **See what is staged.**
   `git status --short` and `git diff --cached --stat`.
   If nothing is staged, list the changed files, propose which belong to this slice, and ask the human
   before running `git add`. Never use `git add -A` or `git add .`.

2. **Refuse build output and local files.**
   `git diff --cached --name-only | grep -E '(^|/)(bin|obj|tmp)/|\.db$|(^|/)\.env$'`
   If anything matches: stop, list the paths, and propose `git restore --staged <path>` plus a `.gitignore` entry.

3. **Refuse secrets.**
   Run BOTH checks. gitleaks finds known key formats but misses readable config secrets (a JWT signing key
   spelled as a plain English phrase, for example), and the pattern catches those:
   - `git diff --cached -- . ':(exclude)ai-session' | grep -nEi '(key|secret|password|pwd|token)["'\'' ]*[:=] *["'\''][^"'\'' ]{8,}'`
   - `gitleaks git --pre-commit --staged --redact` (if installed; it also scans `ai-session/` transcripts)
   On any finding: stop, show the file and line (redacted), and explain where the value should live
   (environment variable, documented in `.env.example`). Continue only if the human confirms it is not a secret.

4. **Check identity.**
   `git config user.email` must be your work address (`@yourcompany.com`; change this to your own domain).
   If not, stop and ask the human to run `git config user.email <their work email>`. Do not set it yourself.

5. **Draft the message from the diff, not from memory.**
   Read `git diff --cached`. Write:
   - Subject: `type(scope): summary`, imperative, 72 characters or fewer.
     Types: feat, fix, docs, test, refactor, perf, build, ci, chore, style, revert.
     Scope: the area (products, orders, harness, plan …).
   - Body (optional): why, in 1–3 lines; mention any 1-3-1 decision the human made.
   - **No** `Co-Authored-By`, "Generated with" or any other AI attribution line.
   If the diff holds more than one slice, say so and propose splitting it instead of writing one message.

6. **Show and wait.** Print the staged file list and the full message. Ask: "Commit with this message?"
   Wait for an explicit yes. If the human edits the message, use their version verbatim.

7. **Commit.** `git commit -m "<subject>" -m "<body>"`. Report the short hash.

8. **Never push**, never amend a pushed commit, never rebase. Pushing is the human's job.
