#!/usr/bin/env python3
"""Lesson 7: the layers a bad action must pass -> l0007-layers.svg (inlined by build_diagrams.py).
Five columns (rule, permission rule, PreToolUse hook, git hook, guard test), five bad actions as rows.
Each row runs left to right until the layer that stops it. Themed by course.css + assets/parts/l0007.css."""
from pathlib import Path

W, H = 960, 540
LX = 20                      # left edge of the row labels
COLS = [322, 452, 582, 712, 842]
CW = 116                     # column width
HEADS = [("Rule", "AGENTS.md", True), ("PreToolUse hook", "Bash only", False),
         ("Permission", "settings.json", False), ("Git hook", ".githooks/", False),
         ("Guard test", "dotnet test", False)]
# (step, label, sub, cells); a cell is ("pass", text) | ("stop", text) | ("none", "")
ROWS = [
    ("s2", "Force-push", "git push --force", [("pass", "talked out of it"), ("stop", "deny + reason"), ("stop", "deny rule"), ("none", ""), ("none", "")]),
    ("s3", "Vague message", "“Update the changes”", [("pass", "you typed it"), ("pass", "doesn’t read it"), ("pass", "doesn’t read it"), ("stop", "commit-msg"), ("none", "")]),
    ("s4", "Committed secret", "a readable JWT key", [("pass", "forgotten"), ("pass", "never sees edits"), ("pass", "an edit is allowed"), ("stop", "pre-commit"), ("none", "")]),
    ("s5", "Overselling rewrite", "read-then-write", [("pass", "“still correct”"), ("pass", "never sees edits"), ("pass", "an edit is allowed"), ("pass", "code looks fine"), ("stop", "3 vs 12 orders")]),
    ("s6", "Same, in a transaction", "still read-then-write", [("pass", ""), ("pass", ""), ("pass", ""), ("pass", ""), ("pass", "green on SQLite")]),
]
Y0, DY = 128, 70


def esc(s):
    return s.replace("&", "&amp;")


out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Five layers a bad action '
       'must pass: a rule in AGENTS.md, which is only a request, then a PreToolUse hook, a permission rule, a git hook and a '
       'guard test. A force-push is stopped by the hook and the permission rule. A vague commit message and a committed '
       'secret pass the agent-side layers and are stopped by the git hooks. An overselling read-then-write rewrite passes '
       'everything until the guard test fails, 12 orders instead of 3. The same rewrite inside a transaction passes the '
       'test too; only the reviewer from lesson 6 catches it.">',
       '<defs><marker id="l7l-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
       'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>']

# columns: one background band each; the "rule" band is dashed (a request, not a guard)
out.append('<g class="st s1">')
for (x, (title, sub, req)) in zip(COLS, HEADS):
    out.append(f'<rect class="l7-col{" req" if req else ""}" x="{x - CW / 2}" y="20" width="{CW}" height="{H - 70}" rx="12"/>')
out.append(f'<text class="l7-note" x="{COLS[0]}" y="{H - 26}">a request</text>')
out.append(f'<text class="l7-note guard" x="{(COLS[1] + COLS[4]) / 2}" y="{H - 26}">guards: code that refuses</text>')
out.append(f'<path class="l7-brace" d="M{COLS[1] - CW / 2 + 6},{H - 44} h{COLS[4] - COLS[1] + CW - 12}"/>')
out.append('</g>')
for (x, (title, sub, req)) in zip(COLS, HEADS):
    out.append(f'<text class="l7-head" x="{x}" y="50">{title}</text><text class="l7-headsub" x="{x}" y="70">{sub}</text>')
out.append(f'<text class="l7-head" x="{LX}" y="50" style="text-anchor:start">A bad action</text>')

for i, (step, label, sub, cells) in enumerate(ROWS):
    y = Y0 + i * DY
    stop_i = next((j for j, (k, _) in enumerate(cells) if k == "stop"), None)
    end_x = COLS[stop_i] - 30 if stop_i is not None else COLS[-1] + CW / 2 + 16
    cls = "st " + step + (" l7-slip" if stop_i is None else "")
    g = [f'<g class="{cls}">',
         f'<text class="lbl" x="{LX}" y="{y - 4}" style="text-anchor:start;font-size:15px">{esc(label)}</text>',
         f'<text class="sub" x="{LX}" y="{y + 15}" style="text-anchor:start;font-size:13px">{esc(sub)}</text>',
         f'<path class="arc" d="M{LX + 196},{y} L{end_x},{y}" marker-end="url(#l7l-head)"/>']
    for j, (kind, text) in enumerate(cells):
        x = COLS[j]
        if kind == "stop":
            g.append(f'<rect class="l7-stop" x="{x - 26}" y="{y - 14}" width="52" height="28" rx="14"/>'
                     f'<text class="l7-stoptxt" x="{x}" y="{y + 5}">STOP</text>'
                     f'<text class="l7-why" x="{x}" y="{y + 32}">{esc(text)}</text>')
        elif kind == "pass":
            g.append(f'<circle class="l7-thru" cx="{x}" cy="{y}" r="5"/>')
            if text:
                g.append(f'<text class="l7-passtxt" x="{x}" y="{y + 26}">{esc(text)}</text>')
        else:
            g.append(f'<text class="l7-none" x="{x}" y="{y + 5}">·</text>')
    if stop_i is None:
        g.append(f'<text class="l7-slipnote" x="{W - 14}" y="{y + 50}">reviewer (lesson 6) catches it</text>')
    g.append('</g>')
    out.append("".join(g))

out.append("</svg>")
Path(__file__).with_name("l0007-layers.svg").write_text("\n".join(out) + "\n")
print("wrote l0007-layers.svg")
