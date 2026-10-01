#!/usr/bin/env python3
"""Lesson 2: "An index, not a manual" -> l0002-index.svg (inlined by build_diagrams.py).
Left: the short root AGENTS.md, drawn as a page with its sections. Right: the detail files it points to.
Steps: s1 root loads every session; s2 a linked doc is opened on demand; s3 a nested AGENTS.md loads
when Claude reads a file in tests/; s4 after compaction only the root file is re-read.
Group class s0 is never highlighted, so it stays dim while stepping (workflow.md: unused this task)."""
from pathlib import Path

W, H = 960, 480
DOC = '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/>'
LX, LY, LW, LH = 30, 60, 330, 370          # root card
RX, RW, RH = 600, 330, 66                   # right-hand cards

# root card sections: heading, number of faux text lines, link target (or None)
SECTIONS = [("## Commands", 2, None),
            ("## Definition of done", 2, None),
            ("## Invariants", 2, "invariants"),
            ("## Workflow", 0, "workflow"),
            ("## More context", 0, "testing")]
LINKS = {"invariants": "→ docs/ai/invariants.md", "workflow": "→ docs/ai/workflow.md", "testing": "→ docs/ai/testing.md"}
RIGHT = {  # key: (y, file name, sub-line, step)
    "invariants": (46, "docs/ai/invariants.md", "the why behind each invariant", "s2"),
    "workflow": (146, "docs/ai/workflow.md", "plan first, one slice at a time", "s0"),
    "testing": (246, "docs/ai/testing.md", "real SQLite, never EF InMemory", "s3"),
    "tests": (370, "tests/AGENTS.md", "loads when Claude reads a test file", "s3"),
}


def card(x, y, name, sub, step):
    return (f'<g class="st {step}"><rect class="ring-node" x="{x}" y="{y}" width="{RW}" height="{RH}" rx="10"/>'
            f'<g class="ico" transform="translate({x + 14},{y + 12})">{DOC}</g>'
            f'<text class="fname" x="{x + 46}" y="{y + 29}">{name}</text>'
            f'<text class="sub" x="{x + 46}" y="{y + 51}" style="text-anchor:start;font-size:13px">{sub}</text></g>')


def arrow(x1, y1, x2, y2, step):
    mx = (x1 + x2) / 2
    return (f'<g class="st {step}"><path class="arc" d="M{x1},{y1} C{mx},{y1} {mx},{y2} {x2 - 10},{y2}" '
            f'marker-end="url(#l2-head)"/></g>')


parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         'aria-label="The root AGENTS.md is a short index that loads every session. Its lines point to '
         'docs/ai/invariants.md, workflow.md and testing.md, which are opened only when a task needs them. '
         'tests/AGENTS.md loads when Claude reads a file in tests. After compaction only the root file is re-read.">',
         '<defs><marker id="l2-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>']

# root card (on in step 1 and again in step 4)
g = [f'<g class="st s1 s4"><rect class="ring-node" x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="12"/>',
     f'<g class="ico" transform="translate({LX + 16},{LY + 14})">{DOC}</g>',
     f'<text class="lbl" x="{LX + 48}" y="{LY + 32}" style="text-anchor:start">AGENTS.md</text>',
     f'<text class="sub" x="{LX + LW - 16}" y="{LY + 32}" style="text-anchor:end;font-size:13px">about 30 lines</text>']
y = LY + 70
link_y = {}
for head, lines, link in SECTIONS:
    g.append(f'<text class="fname sec" x="{LX + 18}" y="{y}">{head}</text>')
    y += 18
    for k in range(lines):
        g.append(f'<rect class="bar" x="{LX + 18}" y="{y - 8}" width="{LW - 60 - 40 * k}" height="7" rx="3.5"/>')
        y += 15
    if link:
        g.append(f'<text class="fname link" x="{LX + 30}" y="{y + 2}">{LINKS[link]}</text>')
        link_y[link] = y - 3
        y += 24
    y += 8
g.append("</g>")
parts.append("".join(g))

# tags above and below the root card
parts.append(f'<g class="st s1"><text class="note strong" x="{LX + LW / 2}" y="{LY - 18}" style="text-anchor:middle">'
             'loads at the start of every session</text></g>')
parts.append(f'<g class="st s4"><text class="note strong" x="{LX + LW / 2}" y="{LY + LH + 30}" style="text-anchor:middle">'
             'after compaction: re-read from disk</text></g>')

# arrows from the link lines to the cards, then the cards
for key in ("invariants", "workflow", "testing"):
    cy, name, sub, step = RIGHT[key]
    parts.append(arrow(LX + LW + 4, link_y[key], RX, cy + RH / 2, step))
ty = RIGHT["tests"][0]
parts.append(f'<g class="st s3"><path class="arc" d="M{RX + RW / 2},{ty - 2} L{RX + RW / 2},{RIGHT["testing"][0] + RH + 10}" '
             f'marker-end="url(#l2-head)"/></g>')
for key, (cy, name, sub, step) in RIGHT.items():
    parts.append(card(RX, cy, name, sub, step))
parts.append(f'<g class="st s3"><text class="note" x="{RX + RW / 2 - 24}" y="{ty - 24}" style="text-anchor:end">its last line points here</text></g>')
parts.append("</svg>")
Path(__file__).with_name("l0002-index.svg").write_text("\n".join(parts) + "\n")
print("wrote l0002-index.svg")
