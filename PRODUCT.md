# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Osmosys .NET trainees: developers with about 2 years of ASP.NET Core and EF Core. They use Claude Code, Codex or Antigravity only as a chat and have never configured an agent. They take the course self-paced, on a laptop, over one to two weeks, with a terminal and an editor open next to the browser.

## Product Purpose
A short course (11 lessons and a capstone, about 12–15 hours) that takes trainees from a single chat to a repo whose rules, skills, reviewers and guards steer any agent. Success: they commit a working harness in the first 30 minutes of the next graded assessment, and the harness passes the swap test. In the swap test, a fresh agent session is given an unseen task in their repo.

## Positioning
Every lesson starts from a real, anonymised incident from a previous assessment ("what happened" vs "what the harness does instead"). Each one ends with an exercise that adds one piece of harness to the same practice repo. It covers several tools: AGENTS.md first, then Claude Code, with Codex and Antigravity equivalents.

## Operating Context
- The reader alternates between the lesson page, a terminal and their practice repo (`~/projects/stockapi`).
- Lessons are read in order, with quizzes for retrieval practice and "Done when" checklists.
- Reference sheets are printed or kept open during the assessment.

## Capabilities and Constraints
- Static HTML on GitHub Pages (OsmosysSoftware/agent-harness-course).
- Every page loads only the shared `assets/course.css` and `assets/course.js`. No external requests, no CDN, works offline.
- Progress is stored per browser (localStorage), with no backend or logins.
- Gamification is light: course progress, per-lesson completion, one badge per lesson, quiz streaks. No XP race or leaderboard.
- Diagrams are authored as D2 text and rendered to SVG at build time.
- Light theme is the default; dark is a toggle.
- Pages must print cleanly.
- Version-specific claims carry a "verified YYYY-MM-DD" badge.

## Brand Commitments
None. The visual identity is the course's own.

## Evidence on Hand
- The lesson content, the anonymised incidents (Trainee A–F, with real commit hashes), the reference solution and the dry-run results.
- No testimonials or completion data exist; don't invent any.

## Product Principles
1. Show, then do: one idea per lesson, made concrete by an incident and practised in the trainee's own repo.
2. Less reading, more doing. Depth is optional and one click away.
3. Truth over polish. Version-specific and unverified claims stay flagged.
4. Progress should feel earned, from completed exercises, not page views.

## Accessibility & Inclusion
Readable in light and dark themes, printable, keyboard-operable quizzes, and no meaning carried by colour alone.
