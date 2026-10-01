#!/usr/bin/env python3
"""Lesson 5: the commit skill as a checkpoint line -> l0005-checkpoint.svg (inlined by build_diagrams.py).
A staged change travels left to right through seven gates; under each gate hangs what that gate turns away.
Gates stay lit once passed (cumulative step classes); the rejected item lights only on its own step.
Colours come from course.css + assets/parts/l0005.css."""
from pathlib import Path

W, H = 900, 350
Y = 110          # the wire
GX = [140, 245, 350, 455, 560, 665, 770]
GATES = [
    ("See what’s", "staged", "git add -A", "never used"),
    ("No build", "output", "obj/, tmp/,", "bin/, .env"),
    ("No", "secrets", "Key: “Sup…", "signing key"),
    ("Work", "identity", "a personal", "address"),
    ("Message", "from the diff", "“Update the", "changes”"),
    ("You", "approve", "no yes,", "no commit"),
    ("Commit,", "never push", "git push", "is yours"),
]

p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="The commit skill as a '
     'checkpoint line. A staged change passes seven gates in order: see what is staged (never git add -A), refuse build '
     'output such as obj and tmp, refuse secrets, check the work email identity, draft the message from the diff, wait '
     'for your approval, then commit and never push. Under each gate is what it turns away.">',
     '<defs><marker id="l5c-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
     'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
     f'<path class="l5-wire" d="M84,{Y} L842,{Y}"/>']

# the staged change: a small parcel of files, always visible
p.append(f'<g class="st s1"><rect class="l5-repo" x="22" y="{Y - 30}" width="60" height="60" rx="8"/>'
         f'<g class="ico" transform="translate(36,{Y - 16}) scale(1.35)"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/></g>'
         f'<text class="l5-glbl" x="52" y="{Y + 54}">staged</text><text class="l5-glbl" x="52" y="{Y + 72}">change</text></g>')

for i, (a, b, r1, r2) in enumerate(GATES):
    n = i + 1
    x = GX[i]
    later = " ".join(f"s{k}" for k in range(n, 8))
    prev = 84 if i == 0 else GX[i - 1] + 38
    p.append(f'<g class="st {later}"><path class="arc" d="M{prev},{Y} L{x - 42},{Y}" marker-end="url(#l5c-head)"/>'
             f'<rect class="ring-node" x="{x - 38}" y="{Y - 32}" width="76" height="64" rx="12"/>'
             f'<text class="num" x="{x}" y="{Y + 7}" style="font-size:22px">{n}</text>'
             f'<text class="l5-glbl" x="{x}" y="{Y - 60}">{a}</text>'
             f'<text class="l5-glbl" x="{x}" y="{Y - 41}">{b}</text></g>')
    # what this gate turns away
    p.append(f'<g class="st s{n}"><path class="l5-drop" d="M{x},{Y + 34} L{x},{Y + 70}"/>'
             f'<rect class="l5-rej" x="{x - 50}" y="{Y + 74}" width="100" height="58" rx="9"/>'
             f'<text class="l5-rejtxt" x="{x}" y="{Y + 98}">{r1}</text>'
             f'<text class="l5-rejtxt" x="{x}" y="{Y + 118}">{r2}</text>'
             f'<text class="mark no" x="{x}" y="{Y + 158}">✕</text></g>')

# the end of the line: one commit, made locally
p.append(f'<g class="st s7"><path class="arc" d="M{GX[-1] + 38},{Y} L{846},{Y}" marker-end="url(#l5c-head)"/>'
         f'<circle class="l5-done" cx="866" cy="{Y}" r="14"/>'
         f'<text class="mark ok" x="866" y="{Y + 6}">✓</text>'
         f'<text class="l5-glbl" x="866" y="{Y - 60}">one</text><text class="l5-glbl" x="866" y="{Y - 41}">commit</text></g>')

p.append(f'<text class="sub" x="450" y="{H - 14}">Each gate stops the line and tells you what to do; none of them works around a failure.</text>')
p.append("</svg>")
Path(__file__).with_name("l0005-checkpoint.svg").write_text("\n".join(p) + "\n")
print("wrote l0005-checkpoint.svg")
