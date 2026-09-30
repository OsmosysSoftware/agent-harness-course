#!/usr/bin/env bash
# PostToolUse on Edit|Write: format the C# file the agent just wrote, so the quality gate never fails on whitespace.
input=$(cat)
file=$(printf '%s' "$input" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
case "$file" in
  *.cs) ;;
  *) exit 0 ;;
esac
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
rel=${file#"$PWD"/}
# whitespace formatting only: fast, and needs no build
dotnet format whitespace StockApi.sln --include "$rel" >/dev/null 2>&1 || true
exit 0
