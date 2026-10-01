#!/usr/bin/env python3
"""Lesson 2: "Which file does Claude read?" -> l0002-which-file.svg (inlined by build_diagrams.py).
Four repo folders side by side, one scenario each. A file Claude Code loads gets a check mark,
a skipped one a cross and a strike-through. Each panel is one step (s1..s4) for the step-through.
Colours come from course.css plus assets/parts/l0002.css, so it follows light/dark themes."""
from pathlib import Path

W, H, PW, GAP, X0 = 960, 300, 216, 24, 12
DOC = '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/>'
FOLDER = '<path d="M3 6h6l2 2h10v11H3z"/>'

# title, sub-title, rows [(name, loaded, note)], verdict lines
PANELS = [
    ("AGENTS.md alone", "your repo after this lesson",
     [("AGENTS.md", True, "")], ["Reads AGENTS.md"]),
    ("A CLAUDE.md appears", "committed by anyone",
     [("CLAUDE.md", True, ""), ("AGENTS.md", False, "")], ["Reads CLAUDE.md only"]),
    ("Add CLAUDE.local.md", "private notes, not committed",
     [("CLAUDE.local.md", True, ""), ("AGENTS.md", False, "")], ["AGENTS.md skipped,", "no warning"]),
    ("CLAUDE.md imports it", "first line: @AGENTS.md",
     [("CLAUDE.md", True, ""), ("AGENTS.md", True, "via @import")], ["Reads both,", "AGENTS.md once"]),
]


def row(x, y, name, loaded, note):
    cls = "doc read" if loaded else "doc skip"
    mark = (f'<text class="mark ok" x="{x + 20}" y="{y + 23}">✓</text>' if loaded
            else f'<text class="mark no" x="{x + 20}" y="{y + 23}">✕</text>')
    out = [f'<rect class="{cls}" x="{x}" y="{y}" width="{PW - 28}" height="34" rx="7"/>', mark,
           f'<g class="ico" transform="translate({x + 30},{y + 7}) scale(0.85)">{DOC}</g>',
           f'<text class="fname" x="{x + 52}" y="{y + 22}">{name}</text>']
    if not loaded:
        out.append(f'<line class="strike" x1="{x + 50}" y1="{y + 17}" x2="{x + 54 + 8.6 * len(name)}" y2="{y + 17}"/>')
    if note:
        out.append(f'<text class="note" x="{x + 52}" y="{y + 52}">{note}</text>')
    return "".join(out)


parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         'aria-label="Which instruction file Claude Code reads. AGENTS.md alone: it reads AGENTS.md. With a CLAUDE.md: '
         'it reads CLAUDE.md only. With a CLAUDE.local.md: AGENTS.md is skipped with no warning. With a CLAUDE.md whose '
         'first line is @AGENTS.md: it reads both, AGENTS.md once.">']
for i, (title, sub, rows, verdict) in enumerate(PANELS):
    x = X0 + i * (PW + GAP)
    step = f"s{i + 1}"
    g = [f'<g class="st {step}">',
         f'<rect class="ring-node panel" x="{x}" y="8" width="{PW}" height="{H - 16}" rx="14"/>',
         f'<text class="num" x="{x + 22}" y="40">{i + 1}</text>',
         f'<text class="lbl" x="{x + 38}" y="40" style="text-anchor:start;font-size:15px">{title}</text>',
         f'<text class="sub" x="{x + 14}" y="62" style="text-anchor:start;font-size:13px">{sub}</text>',
         f'<g class="ico" transform="translate({x + 14},{76}) scale(0.9)">{FOLDER}</g>',
         f'<text class="fname dim" x="{x + 40}" y="{93}">stockapi/</text>']
    for j, (name, loaded, note) in enumerate(rows):
        g.append(row(x + 14, 106 + j * 46, name, loaded, note))
    vy = H - 62 if len(verdict) == 2 else H - 44
    g.append(f'<line class="rule" x1="{x + 14}" y1="{H - 88}" x2="{x + PW - 14}" y2="{H - 88}"/>')
    for k, line in enumerate(verdict):
        g.append(f'<text class="verdict" x="{x + PW / 2}" y="{vy + k * 22}">{line}</text>')
    g.append("</g>")
    parts.append("".join(g))
parts.append("</svg>")
Path(__file__).with_name("l0002-which-file.svg").write_text("\n".join(parts) + "\n")
print("wrote l0002-which-file.svg")
