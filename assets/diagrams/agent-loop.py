#!/usr/bin/env python3
"""Draw the lesson-1 agent loop as an illustrated cycle -> agent-loop.svg (inlined by build_diagrams.py).
Colours come from CSS classes in course.css, so the picture follows light/dark themes.
Each group carries a step class (s1..s5) that course.js highlights in the step-through."""
import math
from pathlib import Path

CX, CY, R = 470, 215, 150
ICONS = {
    "you": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "context": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 13h10M7 16h6"/>',
    "model": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z"/>',
    "harness": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "tools": '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.2L4 17l3 3 5.3-5.2a4 4 0 0 0 5.2-5.3l-2.6 2.6-2.4-.6-.6-2.4z"/>',
}
# name, angle on the ring (deg, 0 = right, clockwise), label, sublabel, step
RING = [("context", -90, "Context window", "everything it knows", "s2"),
        ("model", -18, "Model", "picks the next step", "s3"),
        ("harness", 54, "Harness", "can say no", "s4"),
        ("tools", 126, "Tools", "read · edit · run", "s5")]


def pt(deg, r=R):
    a = math.radians(deg)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def station(name, x, y, label, sub, step, side="below"):
    if side == "right":  # label beside the node, clear of the ring's arrows
        lx, ly, anchor = x + 58, y - 2, ' style="text-anchor:start"'
        sy = ly + 20
    else:
        lx, ly, anchor, sy = x, y + 66, "", y + 86
    return (f'<g class="st {step}"><circle class="ring-node" cx="{x:.1f}" cy="{y:.1f}" r="44"/>'
            f'<g class="ico" transform="translate({x - 22:.1f},{y - 22:.1f}) scale(1.8333)">{ICONS[name]}</g>'
            f'<text class="lbl" x="{lx:.1f}" y="{ly:.1f}"{anchor}>{label}</text>'
            f'<text class="sub" x="{lx:.1f}" y="{sy:.1f}"{anchor}>{sub}</text></g>')


def arc(a1, a2, step, num, note=""):
    # arc along the ring from a1 to a2 (clockwise), trimmed so it starts and ends outside the nodes
    s, e = a1 + 20, a2 - 20
    (x1, y1), (x2, y2) = pt(s), pt(e)
    mid = (s + e) / 2
    lx, ly = pt(mid, R + 30)
    large = 1 if (e - s) > 180 else 0
    t = f'<text class="num" x="{lx:.1f}" y="{ly + 5:.1f}">{num}</text>'
    return (f'<g class="st {step}"><path class="arc" d="M{x1:.1f},{y1:.1f} A{R},{R} 0 {large} 1 {x2:.1f},{y2:.1f}" '
            f'marker-end="url(#loop-head)"/>{t}{note}</g>')


parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 450" role="img" '
         'aria-label="The agent loop: you send a message into the context window; the model reads it all and picks a '
         'tool call; the harness allows or denies it; the tool runs and its result goes back into the context window.">',
         '<defs><marker id="loop-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         '<path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
         f'<circle class="track" cx="{CX}" cy="{CY}" r="{R}"/>',
         f'<text class="hub" x="{CX}" y="{CY - 6}">one turn</text><text class="hubsub" x="{CX}" y="{CY + 16}">repeats until done</text>']
# arcs between ring stations (clockwise), and back from tools to context
angles = [a for _, a, *_ in RING]
parts.append(arc(angles[0], angles[1], "s2", "2"))
parts.append(arc(angles[1], angles[2], "s3", "3"))
deny_x, deny_y = pt((angles[2] + angles[1]) / 2, R - 46)
parts.append(arc(angles[2], angles[3], "s4", "4",
                 f'<text class="deny" x="{pt(54, R - 70)[0]:.1f}" y="{pt(54, R - 70)[1]:.1f}">✕ or ✓</text>'))
parts.append(arc(angles[3], angles[0] + 360, "s5", "5"))
# you -> context
cx, cy = pt(-90)
parts.append(f'<g class="st s1"><path class="arc" d="M150,{cy:.1f} L{cx - 52:.1f},{cy:.1f}" marker-end="url(#loop-head)"/>'
             f'<text class="num" x="{(150 + cx - 52) / 2:.1f}" y="{cy - 10:.1f}">1</text></g>')
parts.append(station("you", 100, cy, "You", "type a message", "s1"))
for name, a, label, sub, step in RING:
    x, y = pt(a)
    parts.append(station(name, x, y, label, sub, step, "right" if name in ("model", "harness") else "below"))
parts.append("</svg>")
Path(__file__).with_name("agent-loop.svg").write_text("\n".join(parts) + "\n")
print("wrote agent-loop.svg")
