#!/usr/bin/env python3
"""Lesson 3: "two ways out of a wall" -> l0003-two-ways.svg (inlined by build_diagrams.py).
The agent hits a missing .NET 8 SDK. Path A decides quietly (net7.0) and surprises you later;
path B hands over a 1-3-1 card and you choose. Colours come from course.css + assets/parts/l0003.css.
Groups carry step classes s1..s7; a group with several step classes stays lit across those steps."""
from pathlib import Path

ICONS = {
    "agent": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z"/>',
    "down": '<path d="M12 4v15"/><path d="M6 13l6 6 6-6"/><path d="M5 4h14"/>',
    "warn": '<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5"/><path d="M12 17.2v.3"/>',
    "you": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
}


def node(name, x, y, label, sub, cls, r=38):
    return (f'<g class="{cls}"><circle class="ring-node" cx="{x}" cy="{y}" r="{r}"/>'
            f'<g class="ico" transform="translate({x - r / 2},{y - r / 2}) scale({r / 24:.4f})">{ICONS[name]}</g>'
            f'<text class="lbl" x="{x}" y="{y + r + 24}">{label}</text>'
            f'<text class="sub" x="{x}" y="{y + r + 43}">{sub}</text></g>')


W, H = 860, 460
p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Two ways out of a wall. '
     'The agent runs dotnet build and finds no .NET 8 SDK. Path A: it quietly retargets net7.0, nobody notices, and the '
     'broken requirement surprises you in review. Path B: it hands over a 1-3-1, one problem, three options with costs and '
     'one recommendation, and waits while you choose.">',
     '<defs><marker id="l3w-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
     '<path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>']

# s1: the agent and the wall
p.append(node("agent", 80, 245, "Agent", "runs dotnet build", "st s1"))
bricks = "".join(f'<path class="l3-brick" d="M200,{y} h30"/>' for y in range(165, 340, 25))
bricks += "".join(f'<path class="l3-brick" d="M{215 if (i % 2) else 208},{150 + 25 * i} v25"/>' for i in range(7))
p.append(f'<g class="st s1"><path class="arc" d="M124,245 L190,245" marker-end="url(#l3w-head)"/>'
         f'<rect class="l3-wall" x="200" y="140" width="30" height="200" rx="3"/>{bricks}'
         f'<text class="lbl" x="215" y="372">No .NET 8 SDK</text>'
         f'<text class="sub" x="215" y="391">only 6 and 7 installed</text></g>')

# path A: decide quietly (s2, s3)
p.append('<text class="l3-tag l3-a" x="252" y="44">A · decides quietly</text>')
p.append('<g class="st bad s2"><path class="arc" d="M234,175 C275,175 290,95 326,95" marker-end="url(#l3w-head)"/></g>')
p.append(node("down", 372, 95, "Retargets net7.0", "one quiet sentence", "st bad s2"))
p.append('<g class="st bad s3"><path class="arc" d="M414,95 L594,95" marker-end="url(#l3w-head)"/>'
         '<text class="sub" x="504" y="83">nobody sees it</text></g>')
p.append(node("warn", 640, 95, "Surprise in review", "a requirement broke", "st bad s3"))

# path B: hand over a 1-3-1 (s4..s7)
p.append('<text class="l3-tag l3-b" x="322" y="214">B · hands over a 1-3-1</text>')
p.append('<g class="st s4 s5 s6 s7"><path class="arc" d="M234,300 L314,300" marker-end="url(#l3w-head)"/>'
         '<rect class="l3-card" x="320" y="226" width="330" height="214" rx="12"/></g>')
p.append('<g class="st s4"><text class="l3-key" x="338" y="252">1 PROBLEM</text>'
         '<text class="l3-txt" x="338" y="273">No .NET 8 SDK; the brief needs net8.0</text></g>')
p.append('<text class="l3-key" x="338" y="303">3 OPTIONS</text>')
opts = [("1  Install the .NET 8 SDK", " · ~5 min", ""),
        ("2  Build in a .NET 8 container", "", ""),
        ("3  Target net7.0", " · breaks the brief", "l3-cost")]
for i, (main, cost, cc) in enumerate(opts):
    y = 312 + 32 * i
    tail = f'<tspan class="{cc}">{cost}</tspan>' if cc else f'<tspan class="l3-dim">{cost}</tspan>'
    p.append(f'<g class="st s5"><rect class="l3-row" x="332" y="{y}" width="306" height="26" rx="6"/>'
             f'<text class="l3-txt" x="344" y="{y + 18}">{main}{tail}</text></g>')
p.append('<g class="st s6"><rect class="l3-badge" x="332" y="408" width="124" height="24" rx="12"/>'
         '<text class="l3-badgetxt" x="394" y="425">RECOMMEND 1</text>'
         '<text class="l3-dim" x="468" y="425">Waiting for your call.</text></g>')
p.append('<g class="st s7"><path class="arc" d="M654,330 L702,330" marker-end="url(#l3w-head)"/></g>')
p.append(node("you", 750, 330, "You choose", "and log it in PLAN.md", "st s7"))
p.append("</svg>")
Path(__file__).with_name("l0003-two-ways.svg").write_text("\n".join(p) + "\n")
print("wrote l0003-two-ways.svg")
