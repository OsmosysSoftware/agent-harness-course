# Agent Harness Resources

All links were checked live on 2026-09-30. Claude Code was v2.1.284 locally.

## Knowledge

### Claude Code (official docs, code.claude.com)
- [Claude Code 101 (Anthropic Academy)](https://academy.claude.com/courses/claude-code-101)
  Four modules: the agentic loop, first prompt, daily workflows, customising. Use for: the pre-work before lesson 1.
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
  The loop (gather context, act, verify), tools, the context window, and how subagents start fresh. Use for: lesson 1.
- [Context window](https://code.claude.com/docs/en/context-window)
  The "what survives compaction" table. Use for: lesson 1's case that prose rules drift.
- [Permission modes](https://code.claude.com/docs/en/permission-modes)
  The default (Manual), acceptEdits, plan, auto, dontAsk and bypassPermissions modes, and plan mode. Use for: lessons 1 and 4.
- [Best practices](https://code.claude.com/docs/en/best-practices)
  Explore, then plan, then code, then commit; keeping CLAUDE.md short; `/clear`. Use for: lesson 4.
- [Memory: CLAUDE.md, AGENTS.md, imports, rules](https://code.claude.com/docs/en/memory)
  Native AGENTS.md (v2.1.277+), load order, 4-hop imports, `paths:` rules, the under-200-lines target. Use for: lesson 2.
- [Settings](https://code.claude.com/docs/en/settings) and the [settings reference](https://code.claude.com/docs/en/settings-reference)
  Precedence, and the `attribution` key. Use for: lesson 7.
- [Permissions](https://code.claude.com/docs/en/permissions)
  The allow/ask/deny syntax (`Bash(git commit *)`), evaluated deny, then ask, then allow. Use for: lesson 7.
- [Skills](https://code.claude.com/docs/en/skills)
  The SKILL.md frontmatter and `disable-model-invocation`; commands merged into skills. Use for: lesson 5.
- [Subagents](https://code.claude.com/docs/en/sub-agents)
  `.claude/agents/*.md`, the `tools` allowlist, fresh context, explicit invocation. Use for: lesson 6.
- [Hooks guide](https://code.claude.com/docs/en/hooks-guide) and the [hooks reference](https://code.claude.com/docs/en/hooks)
  PreToolUse deny JSON, exit code 2, `${CLAUDE_PROJECT_DIR}`. Use for: lesson 7.
- [MCP](https://code.claude.com/docs/en/mcp)
  `claude mcp add`, the local/project/user scopes, `.mcp.json`, the approval prompt. Use for: lesson 8.
- [Output styles](https://code.claude.com/docs/en/output-styles)
  The built-in Learning style (`TODO(human)`), and output style vs CLAUDE.md, skill or hook. Use for: lessons 1 and 2.
- [Common workflows](https://code.claude.com/docs/en/common-workflows)
  Plan mode, resuming sessions, worktrees. Use for: lessons 4 and 10.
- [Changelog](https://code.claude.com/docs/en/changelog)
  Use for: re-checking every `version-specific` badge.

### Tool-neutral and other agents
- [AGENTS.md standard](https://agents.md/)
  "A README for agents", stewarded by the Agentic AI Foundation (Linux Foundation); the nearest file wins. Use for: lesson 2.
- [Codex: AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  The global and override files, root-to-cwd concatenation, the 32 KiB default. Use for: lesson 2's Codex panel.
- [Codex: config basics](https://learn.chatgpt.com/docs/config-file/config-basic), [approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security), [rules](https://learn.chatgpt.com/docs/agent-configuration/rules)
  `approval_policy` (`untrusted` retired), `sandbox_mode`, `prefix_rule` allow/prompt/forbidden. Use for: lessons 1 and 7.
- [Codex: skills](https://learn.chatgpt.com/docs/build-skills), [hooks](https://learn.chatgpt.com/docs/hooks), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
  `.agents/skills`, `.codex/hooks.json`, `.codex/agents/*.toml`, `[mcp_servers.x]`. Use for: the Codex panels in lessons 5 to 8.
- [Antigravity: rules](https://antigravity.google/docs/rules), [skills](https://antigravity.google/docs/skills), [workflows](https://antigravity.google/docs/ide/workflows), [permissions](https://antigravity.google/docs/permissions), [hooks](https://antigravity.google/docs/hooks), [MCP](https://antigravity.google/docs/mcp), [subagents](https://antigravity.google/docs/subagents)
  AGENTS.md is read as always_on; `.agents/rules`, `.agents/skills`, `.agents/hooks.json`, `.agents/mcp_config.json`; workflows are deprecated by 2026-11-01. Use for: the Antigravity panels.

### .NET and guard tooling
- [EF Core InMemory provider](https://learn.microsoft.com/en-us/ef/core/providers/in-memory/) and [Testing without the database](https://learn.microsoft.com/en-us/ef/core/testing/testing-without-the-database)
  InMemory is "strongly discouraged" for testing and has no ExecuteUpdate. Use for: lesson 3's InMemory trap.
- [EF Core SQLite limitations](https://learn.microsoft.com/en-us/ef/core/providers/sqlite/limitations)
  DateTimeOffset ordering and comparison are evaluated on the client. Use for: lesson 8.
- [SQLite transactions](https://www.sqlite.org/lang_transaction.html)
  One writer at a time, and BEGIN IMMEDIATE. Use for: lessons 6 and 9 (the stock invariant ADR).
- [dotnet format](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format)
  `--verify-no-changes` and `--include`. Use for: lesson 5's quality gate and lesson 7's format hook.
- [MSBuild command line (-warnAsError)](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-command-line-reference)
  Use for: lesson 5.
- [gitleaks](https://github.com/gitleaks/gitleaks)
  `gitleaks git --pre-commit --staged` (v8.30.1; `protect` is deprecated). Use for: lesson 7.
- [githooks and core.hooksPath](https://git-scm.com/docs/githooks)
  Hooks must be executable, and `core.hooksPath` has to be set in every clone. Use for: lesson 7.
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
  Use for: lesson 5's commit skill and lesson 7's commit-msg hook.
- [context7](https://github.com/upstash/context7)
  Live library docs over MCP (`@upstash/context7-mcp` 4.1.1, or the remote `https://mcp.context7.com/mcp`). Use for: lesson 8.

## Wisdom (communities)
- [anthropics/claude-code on GitHub](https://github.com/anthropics/claude-code)
  Issues and changelog, maintained by Anthropic. Use for: checking whether a behaviour is a known bug before building around it.
- [OpenAI Developer Community: Codex](https://community.openai.com/)
  Use for: Codex config and AGENTS.md behaviour.
- [Google AI Developers Forum](https://discuss.ai.google.dev/)
  Use for: Antigravity rules, skills and permissions.
- Internal: a weekly 30-minute harness review at Osmosys, where trainees swap repos and run each other's swap test. Use for: real feedback on whether a harness steers someone else's agent.

## Gaps
- No official source for Codex's commit-attribution default, or for Codex's session file path. Test on the installed version.
- No maintained, official read-only SQLite MCP server; the reference server is archived. Lesson 8 uses a SQLite connection opened with `mode=ro` instead.
