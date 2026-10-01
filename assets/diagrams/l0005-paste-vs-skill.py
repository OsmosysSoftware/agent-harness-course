#!/usr/bin/env python3
"""Lesson 5: a prompt pasted by hand vs a skill in the repo -> l0005-paste-vs-skill.svg (inlined by build_diagrams.py).
Left: one template, pasted into three sessions, and the copies drift. Right: one SKILL.md in the repo that every
session loads by name, fixed once in a commit. Colours come from course.css + assets/parts/l0005.css.
Groups carry step classes s1..s6; a group with several step classes stays lit across those steps."""
from pathlib import Path

W, H = 900, 470
p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="A pasted prompt versus a '
     'skill. Left: one commit template kept in a notes file is pasted by hand into three sessions; one copy names the '
     'wrong project and another has lost its secret-scan line. Right: the procedure is one SKILL.md file in the repo; '
     'every session loads the same file by typing /commit, and one reviewed commit fixes it for every later run.">',
     '<defs><marker id="l5p-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
     'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
     '<text class="l5-tag l5-bad" x="40" y="34">PASTED BY HAND</text>',
     '<text class="l5-tag l5-good" x="480" y="34">A SKILL IN THE REPO</text>',
     '<path class="rule" d="M450,20 L450,450"/>']

# s1: the template in a notes file
p.append('<g class="st s1 s2 s3"><rect class="paper" x="40" y="50" width="370" height="74" rx="6"/>'
         '<text class="mono strong" x="58" y="78">notes/commit-prompt.txt</text>'
         '<text class="mono" x="58" y="104">Commit for StockApi; scan secrets.</text></g>')


def bubble(y, who, text, wrong, mark, why, cls):
    box = "l5-bubble wrong" if wrong else "l5-bubble"
    out = (f'<g class="{cls}"><path class="l5-paste" d="M58,124 L58,{y + 40} L70,{y + 40}" marker-end="url(#l5p-head)"/>'
           f'<rect class="{box}" x="76" y="{y}" width="334" height="80" rx="12"/>'
           f'<text class="note l5-left" x="92" y="{y + 22}">{who}</text>'
           f'<text class="mono" x="92" y="{y + 46}">{text}</text>'
           f'<text class="mark {"no" if wrong else "ok"}" x="392" y="{y + 24}">{mark}</text>')
    if why:
        out += f'<text class="note l5-left l5-bad" x="92" y="{y + 68}">{why}</text>'
    return out + "</g>"


p.append(bubble(148, "Session 1 · pasted by you", "Commit for StockApi; scan secrets.", False, "✓", "", "st s1"))
p.append(bubble(244, "Session 2 · pasted from an old copy", "Commit for <tspan class=\"l5-badtxt\">ExamDomain (Angular)</tspan>.",
                True, "✕", "another project’s name, left in", "st s2"))
p.append(bubble(340, "Session 3 · a teammate’s copy", "Commit for StockApi.", True, "✕",
                "the secret-scan line is gone", "st s3"))
p.append('<g class="st s3"><text class="sub" x="225" y="448">three copies, three procedures</text></g>')

# s4: one file in the repo
p.append('<g class="st s4 s5 s6"><rect class="l5-repo" x="480" y="50" width="390" height="190" rx="10"/>'
         '<text class="fname dim" x="500" y="82">stockapi/</text>'
         '<text class="fname" x="516" y="110">.agents/skills/commit/</text>'
         '<rect class="doc read" x="532" y="124" width="170" height="36" rx="7"/>'
         '<g class="ico" transform="translate(542,130) scale(0.85)"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/></g>'
         '<text class="fname" x="566" y="148">SKILL.md</text>'
         '<text class="note l5-left" x="500" y="196">versioned in git, cloned with the code,</text>'
         '<text class="note l5-left" x="500" y="216">changed only through a reviewed diff</text></g>')

# s5: every session loads it by name
for i, x in enumerate((540, 675, 810)):
    p.append(f'<g class="st s5 s6"><path class="arc" d="M{617 + (i - 1) * 40},240 L{x},{298}" marker-end="url(#l5p-head)"/>'
             f'<circle class="ring-node" cx="{x}" cy="332" r="30"/>'
             f'<text class="fname" x="{x}" y="337" style="text-anchor:middle;font-size:13px">/commit</text>'
             f'<text class="sub" x="{x}" y="386">session {i + 1}</text>'
             f'<text class="mark ok" x="{x}" y="408">✓</text></g>')
p.append('<g class="st s5"><text class="sub" x="675" y="448">same file, same steps, every run</text></g>')

# s6: fix it once
p.append('<g class="st s6"><rect class="chip pass" x="714" y="126" width="144" height="32" rx="16"/>'
         '<text class="chiptxt" x="786" y="147">1 commit fixes it</text>'
         '</g>')

p.append("</svg>")
Path(__file__).with_name("l0005-paste-vs-skill.svg").write_text("\n".join(p) + "\n")
print("wrote l0005-paste-vs-skill.svg")
