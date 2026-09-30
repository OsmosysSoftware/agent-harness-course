#!/usr/bin/env bash
# Quality gate: format -> build -> test, stop at the first failure.
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

step() { printf '\n== %s ==\n' "$1"; }

step "1/3 format (dotnet format --verify-no-changes)"
dotnet format --verify-no-changes || { echo "GATE FAILED at format: run 'dotnet format' and re-run"; exit 1; }

step "2/3 build (dotnet build -warnaserror)"
dotnet build -warnaserror --nologo -v q || { echo "GATE FAILED at build"; exit 1; }

step "3/3 test (dotnet test --no-build)"
dotnet test --no-build --nologo -v q || { echo "GATE FAILED at test"; exit 1; }

echo; echo "quality gate: green"
