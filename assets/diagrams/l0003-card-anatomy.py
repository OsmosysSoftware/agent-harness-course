#!/usr/bin/env python3
"""Lesson 3: anatomy of a 1-3-1 card -> l0003-card-anatomy.svg (inlined by build_diagrams.py).
A real-shaped hand-over (EF InMemory vs the guarded UPDATE) on the left; on the right, what each part prevents.
Groups carry step classes s1..s4. Colours come from course.css + assets/parts/l0003.css."""
from pathlib import Path

W, H = 860, 430
L = ' style="text-anchor:start"'
p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Anatomy of a 1-3-1 card. '
     'One problem names the real blocker. Three options each carry their cost, so the workaround the agent would have taken '
     'is visible. One recommendation lets you answer in a word. Then it waits, and changes nothing until you answer.">',
     '<rect class="l3-card" x="30" y="20" width="450" height="390" rx="14"/>']


def callout(step, y_card, y, title, l1, l2):
    return (f'<g class="st {step}"><path class="l3-lead" d="M484,{y_card} C505,{y_card} 505,{y - 6} 530,{y - 6}"/>'
            f'<circle class="l3-dot" cx="484" cy="{y_card}" r="4"/>'
            f'<text class="lbl" x="540" y="{y}"{L}>{title}</text>'
            f'<text class="sub" x="540" y="{y + 21}"{L}>{l1}</text>'
            f'<text class="sub" x="540" y="{y + 40}"{L}>{l2}</text></g>')


# 1 problem
p.append('<g class="st s1"><rect class="l3-row" x="46" y="36" width="418" height="92" rx="8"/>'
         '<text class="l3-key" x="62" y="60">1 PROBLEM</text>'
         '<text class="l3-txt" x="62" y="84">InMemory can’t run ExecuteUpdateAsync, and</text>'
         '<text class="l3-txt" x="62" y="106">that guarded UPDATE is what stops overselling.</text></g>')
p.append(callout("s1", 82, 70, "1 problem", "The real blocker, not “it failed”.", "A wrong diagnosis shows up here."))
# 3 options
p.append('<g class="st s2"><text class="l3-key" x="62" y="160">3 OPTIONS</text>')
opts = [("1  Test on real SQLite", " · the repo’s own setup", "l3-dim"),
        ("2  InMemory for the rest", " · PlaceAsync untested", "l3-dim"),
        ("3  Rewrite as read-then-write", " · oversells", "l3-cost")]
for i, (main, cost, cc) in enumerate(opts):
    y = 170 + 38 * i
    p.append(f'<rect class="l3-row" x="46" y="{y}" width="418" height="30" rx="7"/>'
             f'<text class="l3-txt" x="62" y="{y + 20}">{main}<tspan class="{cc}">{cost}</tspan></text>')
p.append('</g>')
p.append(callout("s2", 225, 185, "3 options, each with its cost", "The shortcut it would have taken", "is on the list, with its price."))
# 1 recommendation
p.append('<g class="st s3"><rect class="l3-badge" x="46" y="300" width="132" height="28" rx="14"/>'
         '<text class="l3-badgetxt" x="112" y="319">RECOMMEND 1</text>'
         '<text class="l3-txt" x="192" y="319">fix the test setup, not the code</text></g>')
p.append(callout("s3", 314, 290, "1 recommendation", "You can reply “1” and move on,", "or disagree with a reason."))
# then wait
p.append('<g class="st s4"><text class="l3-wait" x="62" y="378">Waiting for your call.</text></g>')
p.append(callout("s4", 373, 372, "Then it stops", "Nothing installed, launched,", "downgraded or deleted meanwhile."))
p.append("</svg>")
Path(__file__).with_name("l0003-card-anatomy.svg").write_text("\n".join(p) + "\n")
print("wrote l0003-card-anatomy.svg")
