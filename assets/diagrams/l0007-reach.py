#!/usr/bin/env python3
"""Lesson 7: who each guard binds -> l0007-reach.svg (inlined by build_diagrams.py).
Actors across the top; one row per guard; a filled dot where the guard binds that actor, an empty ring where it doesn't.
Themed by course.css + assets/parts/l0007.css."""
from pathlib import Path

W, H = 900, 450
XS = [330, 440, 550, 660, 770]
ICONS = {
    "you": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "claude": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
    "tool": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 10l3 2-3 2"/><path d="M12 15h5"/>',
    "ci": '<circle cx="12" cy="12" r="3.5"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>',
}
ACTORS = [("you", "You", "in a terminal"), ("claude", "Claude Code", ""), ("tool", "Codex", ""),
          ("tool", "Antigravity", ""), ("ci", "CI", "or a teammate")]
# (step, title, sub, hole, binds per actor)
ROWS = [
    ("s1", "Permission rules,", "PreToolUse hook", "the agent, in Claude Code only", [0, 1, 0, 0, 0]),
    ("s2", "Git hooks", ".githooks/", "anyone who commits, in a clone with core.hooksPath set", [1, 1, 1, 1, 0]),
    ("s3", "Guard test", "ConcurrencyTests", "whoever runs dotnet test, CI included", [1, 1, 1, 1, 1]),
]
Y0, DY = 190, 82

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Who each guard binds. '
       'Permission rules and the PreToolUse hook bind only the agent inside Claude Code. Git hooks bind everyone who '
       'commits in a clone where core.hooksPath is set: you in a terminal, Claude Code, Codex and Antigravity. The guard '
       'test binds whoever runs the tests, including CI.">']
for x in XS:
    out.append(f'<path class="l7-rail" d="M{x},{Y0 - 50} L{x},{Y0 + DY * 2 + 30}"/>')
for x, (ico, name, sub) in zip(XS, ACTORS):
    out.append(f'<circle class="ring-node" cx="{x}" cy="62" r="28"/>'
               f'<g class="ico" transform="translate({x - 14},48) scale(1.1667)">{ICONS[ico]}</g>'
               f'<text class="lbl" x="{x}" y="114" style="font-size:14px">{name}</text>'
               + (f'<text class="sub" x="{x}" y="132" style="font-size:12.5px">{sub}</text>' if sub else ""))
for i, (step, title, sub, who, binds) in enumerate(ROWS):
    y = Y0 + i * DY
    g = [f'<g class="st {step}">',
         f'<rect class="l7-band" x="14" y="{y - 30}" width="{W - 28}" height="60" rx="12"/>',
         f'<text class="lbl" x="34" y="{y - 3}" style="text-anchor:start;font-size:15px">{title}</text>',
         f'<text class="sub" x="34" y="{y + 17}" style="text-anchor:start;font-size:13px">{sub}</text>']
    for x, b in zip(XS, binds):
        g.append(f'<circle class="l7-bind{"" if b else " off"}" cx="{x}" cy="{y}" r="{11 if b else 7}"/>')
        if b:
            g.append(f'<path class="l7-tick" d="M{x - 5},{y} l3.5,3.5 l6.5,-7"/>')
    g.append(f'<text class="l7-who" x="{W // 2 + 70}" y="{y + 46}">binds {who}</text>')
    g.append('</g>')
    out.append("".join(g))
out.append(f'<text class="l7-note" x="{W // 2}" y="{H - 8}">Codex and Antigravity have their own rule and hook files: same idea, separate config</text>')
out.append("</svg>")
Path(__file__).with_name("l0007-reach.svg").write_text("\n".join(out) + "\n")
print("wrote l0007-reach.svg")
