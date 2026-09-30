#!/usr/bin/env bash
# PreToolUse guard for Bash: deny commands that rewrite history, destroy data or act on the machine.
# Input: the tool call as JSON on stdin. Output: a deny decision as JSON, or nothing (= normal permission flow).
# No jq needed: we match patterns against the raw JSON text.
input=$(cat)

deny() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$1"
  exit 0
}

# Extract the command string for readable matching (falls back to the whole payload).
cmd=$(printf '%s' "$input" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\(\([^"\\]\|\\.\)*\)".*/\1/p')
[ -z "$cmd" ] && cmd=$input

check() { printf '%s' "$cmd" | grep -Eqi -- "$1"; }

check 'git[[:space:]]+push.*(--force|[[:space:]]-f([[:space:]]|$)|--force-with-lease)' && deny "Force-push rewrites shared history. Ask the human; they push, not the agent."
check 'git[[:space:]]+(reset[[:space:]]+--hard|clean[[:space:]]+-[a-z]*f|filter-branch|filter-repo)' && deny "Destroys work or history. Present a 1-3-1 instead."
check 'git[[:space:]]+(rebase|commit[[:space:]].*--amend)' && deny "History rewriting is not allowed (docs/ai/workflow.md). Make a new commit instead."
check 'rm[[:space:]]+-[a-z]*r[a-z]*f|rm[[:space:]]+-[a-z]*f[a-z]*r|Remove-Item.*-Recurse' && deny "Recursive delete blocked. Name the exact files and ask the human."
check 'drop[[:space:]]+(table|database)|dotnet[[:space:]]+ef[[:space:]]+database[[:space:]]+drop|ensuredeleted' && deny "Dropping a database is a human decision. Present a 1-3-1."
check '(Start-Process|open[[:space:]]+-a|systemctl[[:space:]]+start|service[[:space:]]+[a-z-]+[[:space:]]+start|Docker Desktop)' && deny "Starting software on the machine is the human's call (invariants: environment). Ask them to start it."
check '(apt|apt-get|dnf|yum|brew|winget|choco)[[:space:]]+install|dotnet-install' && deny "Installing software is the human's call. Present a 1-3-1."
check 'TargetFramework>net[0-7]\.|net7\.0|net6\.0' && deny "Target framework is net8.0 (AGENTS.md). A missing SDK is a 1-3-1, not a downgrade."

exit 0
