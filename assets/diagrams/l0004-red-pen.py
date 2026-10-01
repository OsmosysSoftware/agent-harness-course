#!/usr/bin/env python3
"""Lesson 4: the agent's draft plan, marked up by the human -> l0004-red-pen.svg (inlined by build_diagrams.py).
The draft is always visible; each red-pen edit is a step group ("st sN") that stays lit in later steps."""
from pathlib import Path

LATER = {1: "s1 s2 s3 s4 s5", 2: "s2 s3 s4 s5", 3: "s3 s4 s5", 4: "s4 s5", 5: "s5"}
X = 56


def line(y, text, cls="mono"):
    return f'<text class="{cls}" x="{X}" y="{y}">{text}</text>'


def note(y, *rows):  # margin note in red pen, one tspan per row
    spans = "".join(f'<tspan x="612" dy="{0 if i == 0 else 19}">{r}</tspan>' for i, r in enumerate(rows))
    return f'<text class="pentext" x="612" y="{y}">{spans}</text>'


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 460" role="img" aria-label="The agent’s draft '
    'ai-session/PLAN.md with your red-pen edits: a slice that is too big is split in two, each slice gets a named '
    'test, an email feature that is not in the brief is struck out, and the page is stamped approved and committed alone.">',
    '<rect class="paper" x="30" y="20" width="560" height="420" rx="6"/>',
    line(54, "ai-session/PLAN.md", "mono strong"),
    line(96, "## Goal"),
    line(120, "List products that are running low on stock."),
    line(156, "## Slices"),
    line(184, "- [ ] low-stock endpoint, validation, tests at the end"),
    line(264, "- [ ] email the buyer when stock is low"),
    line(300, "## Decisions made by the human"),
    line(324, "- (your entries from lesson 3, kept)"),
    line(360, "Approved by: ____________"),
    # s1: whose draft this is
    f'<g class="st {LATER[1]}"><rect class="tag" x="420" y="36" width="150" height="26" rx="13"/>'
    '<text class="chiptxt" x="495" y="54">agent’s draft</text></g>',
    # s2: too big -> split
    f'<g class="st {LATER[2]}"><path class="pen" d="M52,179 L512,179"/>'
    f'<text class="pentext" x="76" y="210">[ ] list: stock ≤ threshold, default 5</text>'
    f'<text class="pentext" x="76" y="236">[ ] 400 if threshold is outside 0–1000</text>'
    f'<path class="pen" d="M600,186 C585,190 560,196 520,184"/>'
    f'{note(176, "too big:", "one behaviour per slice")}</g>',
    # s3: missing tests -> add
    f'<g class="st {LATER[3]}"><text class="pentext" x="420" y="210">+ test</text>'
    '<text class="pentext" x="420" y="236">+ test 1001</text>'
    f'{note(222, "no test named:", "add one per slice")}</g>',
    # s4: scope creep -> strike
    f'<g class="st {LATER[4]}"><path class="pen" d="M52,259 L380,259"/><path class="pen" d="M52,265 L380,253"/>'
    f'{note(272, "not in BRIEF.md: cut")}</g>',
    # s5: signed and stamped
    f'<g class="st {LATER[5]}"><text class="pentext" x="168" y="355">your name, today</text>'
    '<g transform="rotate(-6 450 395)"><rect class="stamp" x="330" y="366" width="240" height="60" rx="8"/>'
    '<text class="stamptxt" x="450" y="394">APPROVED</text>'
    '<text class="stampsub" x="450" y="415">committed alone, before code</text></g>'
    f'{note(372, "git commit -m", "“docs(plan): low-stock", "endpoint”  · 1 file")}</g>',
    "</svg>",
]
Path(__file__).with_name("l0004-red-pen.svg").write_text("\n".join(parts) + "\n")
print("wrote l0004-red-pen.svg")
