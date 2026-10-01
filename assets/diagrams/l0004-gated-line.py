#!/usr/bin/env python3
"""Lesson 4: one giant prompt vs a gated line -> l0004-gated-line.svg (inlined by build_diagrams.py).
Themed by classes in course.css and assets/parts/l0004.css. Step groups are "st sN"; a group carries
several step classes when it should stay lit in later steps, so the right-hand history builds up."""
from pathlib import Path

LATER = {2: "s2 s3 s4 s5", 3: "s3 s4 s5", 4: "s4 s5", 5: "s5"}
GX = 470  # x of the git line on the right


def plan_row(y, step, title, msg, sub):
    return (f'<g class="st {LATER[step]}">'
            f'<circle class="dot plan" cx="{GX}" cy="{y + 30}" r="9"/>'
            f'<text class="lbl l4-left" x="{GX + 22}" y="{y + 12}">{title}</text>'
            f'<text class="mono" x="{GX + 22}" y="{y + 35}">{msg}</text>'
            f'<text class="sub l4-left" x="{GX + 22}" y="{y + 57}">{sub}</text></g>')


def slice_row(y, step, msg):
    chips, x, out = [("one slice", 86), ("tests ✓", 80), ("you review", 100)], GX + 22, []
    for i, (label, w) in enumerate(chips):
        out.append(f'<rect class="chip{" pass" if "✓" in label else ""}" x="{x}" y="{y - 6}" width="{w}" height="28" rx="14"/>'
                   f'<text class="chiptxt" x="{x + w / 2}" y="{y + 13}">{label}</text>')
        x += w
        if i < len(chips) - 1:
            out.append(f'<path class="arc" d="M{x + 4},{y + 8} L{x + 20},{y + 8}" marker-end="url(#gl-head)"/>')
            x += 26
    return (f'<g class="st {LATER[step]}">{"".join(out)}'
            f'<circle class="dot" cx="{GX}" cy="{y + 42}" r="9"/>'
            f'<text class="mono" x="{GX + 22}" y="{y + 47}">{msg}</text></g>')


tiles = "".join(f'<rect class="tile" x="{68 + c * 30}" y="{172 + r * 21}" width="24" height="15" rx="3"/>'
                for r in range(6) for c in range(10))
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 440" role="img" aria-label="Left: one prompt, '
    '“build the whole project”, produces a single commit of 60 files whose message says it adds tests. Right: a plan '
    'committed alone, then slices that each pass tests and your review before their own commit; a requirement change '
    'goes into the plan, committed alone, before it is built.">',
    '<defs><marker id="gl-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
    '<path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
    '<rect class="panel" x="10" y="10" width="410" height="420" rx="14"/>',
    '<rect class="panel" x="440" y="10" width="410" height="420" rx="14"/>',
    '<text class="hub" x="215" y="44">One giant prompt</text>',
    '<text class="hub" x="645" y="44">A gated line</text>',
    # left: the blob
    '<g class="st s1">'
    '<rect class="bubble" x="40" y="64" width="350" height="46" rx="12"/>'
    '<text class="mono l4-mid" x="215" y="92">“Build the whole project for me”</text>'
    '<path class="arc" d="M215,114 L215,150" marker-end="url(#gl-head)"/>'
    f'<rect class="blob" x="55" y="158" width="320" height="176" rx="10"/>{tiles}'
    '<text class="lbl" x="215" y="320">1 commit · 60 files</text>'
    '<text class="mono l4-mid" x="215" y="362">message: “add tests”</text>'
    '<text class="sub" x="215" y="386">the message describes a sliver of it</text>'
    '<text class="bad" x="215" y="414">✕ nothing to review, revert or bisect in pieces</text></g>',
    # right: the history
    f'<path class="rail" d="M{GX},74 L{GX},400"/>',
    plan_row(70, 2, "Plan, edited by you", "docs(plan): low-stock endpoint", "1 file: ai-session/PLAN.md"),
    slice_row(156, 3, "feat(products): low-stock endpoint"),
    plan_row(226, 4, "Requirement changed: plan first", "docs(plan): add skuPrefix filter", "decided before it is built"),
    slice_row(312, 5, "feat(products): skuPrefix filter"),
    '<g class="st s5"><text class="good" x="645" y="414">✓ every commit fits on one screen</text></g>',
    "</svg>",
]
Path(__file__).with_name("l0004-gated-line.svg").write_text("\n".join(parts) + "\n")
print("wrote l0004-gated-line.svg")
