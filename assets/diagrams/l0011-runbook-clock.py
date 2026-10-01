#!/usr/bin/env python3
"""Lesson 11: the 30-minute runbook as a clock face -> l0011-runbook-clock.svg (inlined into lessons/0011-capstone.html).
Five segments (rules, skills, reviewers, guards, prove it) on a 30-minute dial; each step lights its segment, points
the hand at the minute it ends, and adds its commit to the git log beside the clock. Themed by course.css + assets/parts/l0011.css."""
import math
from pathlib import Path

W, H = 960, 470
CX, CY = 268, 238
RO, RI = 176, 122            # outer and inner radius of the segment ring
ICONS = {
    "rules": '<path d="M7 3h8l4 4v14H7z"/><path d="M15 3v4h4M10 12h6M10 16h6"/>',
    "skills": '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.2L4 17l3 3 5.3-5.2a4 4 0 0 0 5.2-5.3l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "reviewers": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
    "guards": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "prove": '<path d="M5 12l4 4 10-10"/>',
}
# step, icon, label, start minute, end minute, commit subject (None = no commit of its own)
SEGS = [
    ("s1", "rules", "Rules", 0, 10, "chore(harness): add agent rules"),
    ("s2", "skills", "Skills", 10, 15, "chore(harness): add commit and quality-gate skills"),
    ("s3", "reviewers", "Reviewers", 15, 22, "chore(harness): add test and booking-overlap reviewers"),
    ("s4", "guards", "Guards", 22, 27, "chore(harness): add permissions, guards and pinned MCP"),
    ("s5", "prove", "Prove it", 27, 30, None),
]
STEPS = [s for s, *_ in SEGS]


def ang(minute):                       # 0 min at 12 o'clock, clockwise, 30 min per turn
    return math.radians(minute * 12 - 90)


def pt(minute, r):
    a = ang(minute)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def seg_path(m1, m2, gap=0.18):
    a, b = m1 + gap, m2 - gap
    (x1, y1), (x2, y2) = pt(a, RO), pt(b, RO)
    (x3, y3), (x4, y4) = pt(b, RI), pt(a, RI)
    large = 1 if (b - a) > 15 else 0
    return (f"M{x1:.1f},{y1:.1f} A{RO},{RO} 0 {large} 1 {x2:.1f},{y2:.1f} "
            f"L{x3:.1f},{y3:.1f} A{RI},{RI} 0 {large} 0 {x4:.1f},{y4:.1f} Z")


out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="The 30-minute runbook as a '
       'clock face. Minutes 0 to 10: rules, committed as chore(harness): add agent rules. Minutes 10 to 15: the commit and '
       'quality-gate skills, committed. Minutes 15 to 22: the test and booking-overlap reviewers, committed. Minutes 22 to 27: '
       'permissions, guards and the pinned MCP server, committed. Minutes 27 to 30: prove it, with a fresh session, the '
       'leftover-words grep and a clean git status. The git log beside the clock grows by one harness commit per segment, '
       'all above the starter import and before any feature code.">']

# dial: faint track, minute ticks, five-minute numbers
out.append(f'<circle class="l11-face" cx="{CX}" cy="{CY}" r="{RO + 14}"/>')
for m in range(30):
    r1 = RO + 4
    r2 = RO + (13 if m % 5 == 0 else 8)
    (x1, y1), (x2, y2) = pt(m, r1), pt(m, r2)
    out.append(f'<path class="l11-tick{" major" if m % 5 == 0 else ""}" d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>')
for m in range(0, 30, 5):
    x, y = pt(m, RI - 16)
    out.append(f'<text class="l11-min" x="{x:.1f}" y="{y + 5:.1f}">{m}</text>')

# segments: icon and label sit inside the ring band
for step, icon, label, m1, m2, _ in SEGS:
    mid = (m1 + m2) / 2
    ix, iy = pt(mid, (RO + RI) / 2)
    g = [f'<g class="st {step}"><path class="l11-seg" d="{seg_path(m1, m2)}"/>',
         f'<g class="ico" transform="translate({ix - 11:.1f},{iy - 11:.1f}) scale(0.9167)">{ICONS[icon]}</g>']
    lx, ly = pt(mid, RO + 36)
    anchor = "start" if lx > CX + 20 else ("end" if lx < CX - 20 else "middle")
    g.append(f'<text class="l11-seglbl" x="{lx:.1f}" y="{ly + 5:.1f}" style="text-anchor:{anchor}">{label}</text>')
    g.append(f'<text class="l11-segmin" x="{lx:.1f}" y="{ly + 22:.1f}" style="text-anchor:{anchor}">{m1}–{m2} min</text>')
    g.append("</g>")
    out.append("".join(g))

# one hand per step, shown only while its step is on (l0011.css), pointing at the minute the segment ends
for step, _, _, m1, m2, _ in SEGS:
    hx, hy = pt(m2, RI - 34)
    out.append(f'<g class="st {step} l11-hand"><path class="l11-handline" d="M{CX},{CY} L{hx:.1f},{hy:.1f}"/>'
               f'<circle class="l11-hub" cx="{CX}" cy="{CY}" r="9"/>'
               f'<text class="l11-time" x="{CX}" y="{CY + (44 if m2 not in (15,) else -30)}">0:{m2:02d}</text></g>')

# git log card: newest at the top, so commit 4 sits highest; each line stays lit from its step onwards
X0, Y0, CW, CH = 518, 24, 428, 400
out.append(f'<rect class="l11-term" x="{X0}" y="{Y0}" width="{CW}" height="{CH}" rx="12"/>')
out.append(f'<rect class="l11-termbar" x="{X0}" y="{Y0}" width="{CW}" height="34" rx="12"/>'
           f'<rect class="l11-termbar" x="{X0}" y="{Y0 + 20}" width="{CW}" height="14"/>')
out.append(f'<text class="l11-termtitle" x="{X0 + 18}" y="{Y0 + 23}">git log --oneline</text>')
commits = [(i, s, c) for i, (s, _, _, _, _, c) in enumerate(SEGS) if c]
out.append(f'<path class="l11-rail" d="M{X0 + 26},{Y0 + 73} L{X0 + 26},{Y0 + 78 + len(commits) * 52 - 5}"/>')
row_y = {}
for n, (i, step, subject) in enumerate(reversed(commits)):
    row_y[step] = Y0 + 78 + n * 52
for i, step, subject in commits:
    y = row_y[step]
    lit = " ".join(STEPS[i:])
    out.append(f'<g class="st {lit}"><circle class="l11-dot" cx="{X0 + 26}" cy="{y - 5}" r="6"/>'
               f'<text class="l11-commit" x="{X0 + 42}" y="{y}">{subject}</text></g>')
ys = Y0 + 78 + len(commits) * 52
out.append(f'<circle class="l11-dot base" cx="{X0 + 26}" cy="{ys - 5}" r="6"/>'
           f'<text class="l11-commit base" x="{X0 + 42}" y="{ys}">chore: import RoomBooking starter</text>')
# the proof lines that close the half hour
py = ys + 48
out.append(f'<g class="st s5"><path class="l11-sep" d="M{X0 + 18},{py - 26} h{CW - 36}"/>'
           f'<text class="l11-proof" x="{X0 + 20}" y="{py}">✓ new session names the overlap invariant</text>'
           f'<text class="l11-proof" x="{X0 + 20}" y="{py + 24}">✓ leftover-words grep prints nothing</text>'
           f'<text class="l11-proof" x="{X0 + 20}" y="{py + 48}">✓ git status: nothing to commit</text></g>')
out.append(f'<text class="l11-note" x="{X0 + CW / 2}" y="{H - 8}">no feature code until all four are in</text>')
out.append("</svg>")
Path(__file__).with_name("l0011-runbook-clock.svg").write_text("\n".join(out) + "\n")
print("wrote l0011-runbook-clock.svg")
