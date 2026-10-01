#!/usr/bin/env python3
"""Lesson 11: the swap test -> l0011-swap-test.svg (inlined into lessons/0011-capstone.html).
Top: fresh clone -> clean profile -> one unseen task -> you watch in silence. Bottom: a scorecard of four questions,
each scored pass / partial / fail, with the evidence one dry run produced. Last: any partial or fail loops back as a
committed harness fix. Themed by course.css + assets/parts/l0011.css."""
from pathlib import Path

W, H = 960, 560
ICONS = {
    "clone": '<path d="M3 7h6l2 2h10v10H3z"/><path d="M8 14h8M13 11l3 3-3 3"/>',
    "profile": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/><path d="M3 3l18 18"/>',
    "task": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    "watch": '<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
}
# x, icon, label, sub, step
STATIONS = [
    (110, "clone", "Fresh clone", "hooks switched on", "s1"),
    (340, "profile", "Clean profile", "no personal skills", "s2"),
    (590, "task", "One unseen task", "pasted, nothing else", "s3"),
    (830, "watch", "You watch", "and say nothing", "s3"),
]
SY = 74
# step, question, evidence from the one dry run on the practice repo
QUESTIONS = [
    ("s4", "1. Rules loaded, invariant followed?", "guarded UPDATE, one transaction"),
    ("s5", "2. Skills ran?", "new-endpoint, quality-gate 20/20"),
    ("s6", "3. A reviewer or guard caught something?", "test-reviewer found 2 gaps"),
    ("s7", "4. Stopped and asked when unsure?", "stopped for plan approval"),
]
CX0, CY0, CW = 30, 196, 900
RH = 58
PILLS = [("pass", "Pass", 466), ("partial", "Partial", 542), ("fail", "Fail", 618)]

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="The swap test. A fresh '
       'clone with git hooks switched on, a session with a clean profile, one unseen task pasted with nothing else, and '
       'you watching without a word. Then a scorecard: rules loaded and invariant followed; skills ran; a reviewer or guard '
       'caught something; it stopped and asked when unsure. Each is scored pass, partial or fail with a transcript line. '
       'In one dry run on the practice repo all four passed. Any partial or fail becomes one committed harness fix, then a '
       'new run.">',
       '<defs><marker id="l11s-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
       'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>']

# stations and the arrows between them
for i, (x, icon, label, sub, step) in enumerate(STATIONS):
    g = [f'<g class="st {step}">']
    if i:
        px = STATIONS[i - 1][0]
        g.append(f'<path class="arc" d="M{px + 40},{SY} L{x - 42},{SY}" marker-end="url(#l11s-head)"/>')
    g.append(f'<circle class="ring-node" cx="{x}" cy="{SY}" r="32"/>'
             f'<g class="ico" transform="translate({x - 16},{SY - 16}) scale(1.3333)">{ICONS[icon]}</g>'
             f'<text class="lbl" x="{x}" y="{SY + 56}" style="font-size:15px">{label}</text>'
             f'<text class="sub" x="{x}" y="{SY + 75}" style="font-size:13px">{sub}</text></g>')
    out.append("".join(g))
out.append(f'<g class="st s3"><text class="l11-quote" x="{STATIONS[2][0]}" y="{SY - 46}">“Add PATCH /api/bookings/{{id}}/reschedule.”</text></g>')

# scorecard
out.append(f'<rect class="l11-card" x="{CX0}" y="{CY0}" width="{CW}" height="{RH * 4 + 54}" rx="12"/>')
out.append(f'<text class="l11-cardhead" x="{CX0 + 22}" y="{CY0 + 32}">Scorecard</text>')
for key, txt, x in PILLS:
    out.append(f'<text class="l11-colhead" x="{x}" y="{CY0 + 32}">{txt}</text>')
out.append(f'<text class="l11-colhead" x="{CX0 + CW - 22}" y="{CY0 + 32}" style="text-anchor:end">one dry run showed</text>')
for i, (step, q, ev) in enumerate(QUESTIONS):
    y = CY0 + 54 + i * RH
    g = [f'<g class="st {step}"><rect class="l11-row" x="{CX0 + 10}" y="{y}" width="{CW - 20}" height="{RH - 8}" rx="8"/>',
         f'<text class="l11-q" x="{CX0 + 26}" y="{y + 31}">{q}</text>']
    for key, txt, x in PILLS:
        g.append(f'<rect class="l11-pill {key}{" picked" if key == "pass" else ""}" x="{x - 32}" y="{y + 12}" width="64" height="26" rx="13"/>')
    g.append(f'<path class="l11-check" d="M{PILLS[0][2] - 8},{y + 25} l5,5 l10,-11"/>')
    g.append(f'<text class="l11-ev" x="{CX0 + CW - 26}" y="{y + 31}">{ev}</text></g>')
    out.append("".join(g))

# fix forward: from the scorecard back to the start
fy = CY0 + RH * 4 + 54
out.append(f'<g class="st s8"><path class="l11-loop" d="M{CX0 + CW / 2},{fy + 4} L{CX0 + CW / 2},{fy + 40} '
           f'L14,{fy + 40} L14,{SY} L{STATIONS[0][0] - 40},{SY}" marker-end="url(#l11s-head)"/>'
           f'<rect class="l11-fixbox" x="{CX0 + CW / 2 - 4}" y="{fy + 24}" width="404" height="32" rx="16"/>'
           f'<text class="l11-fix" x="{CX0 + CW / 2 + 198}" y="{fy + 45}">partial or fail → one committed fix → run again</text></g>')
out.append("</svg>")
Path(__file__).with_name("l0011-swap-test.svg").write_text("\n".join(out) + "\n")
print("wrote l0011-swap-test.svg")
