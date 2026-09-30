#!/usr/bin/env bash
# SessionStart: plain stdout becomes context for the agent. Report the environment, and never fix it.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
echo "Session preflight (report only; if anything is missing, use 1-3-1, do not install or start it):"

sdks=$(dotnet --list-sdks 2>/dev/null | awk '{print $1}' | tr '\n' ' ')
case " $sdks" in
  *" 8."*) echo "- .NET SDK: OK (installed: $sdks). Target framework must stay net8.0." ;;
  *) echo "- .NET SDK: MISSING 8.x (installed: ${sdks:-none}). Do NOT downgrade net8.0. Present a 1-3-1." ;;
esac

if docker info >/dev/null 2>&1; then echo "- Docker: running"; else echo "- Docker: not running (do not start it; ask the human if you need it)"; fi

if [ "$(git config core.hooksPath 2>/dev/null)" = ".githooks" ]; then echo "- Git hooks: enabled"; else echo "- Git hooks: NOT enabled in this clone (ask the human to run: git config core.hooksPath .githooks)"; fi
echo "- Git: branch $(git branch --show-current 2>/dev/null), $(git status --porcelain 2>/dev/null | wc -l | tr -d ' ') uncommitted path(s), email $(git config user.email 2>/dev/null || echo unset)"

if [ -f ai-session/PLAN.md ]; then
  next=$(grep -m1 -E '^\s*- \[ \]' ai-session/PLAN.md | sed 's/^\s*- \[ \] //')
  echo "- Plan: next unchecked slice: ${next:-none (all done, or the plan needs updating)}"
else
  echo "- Plan: no ai-session/PLAN.md yet. Explore, then propose a plan before any code."
fi
exit 0
