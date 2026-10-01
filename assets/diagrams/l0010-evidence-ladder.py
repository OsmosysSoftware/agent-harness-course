#!/usr/bin/env python3
"""Lesson 10: which record to trust, strongest first, and checking one claim -> l0010-evidence-ladder.svg.
Step groups are "st sN"; a group listing several steps stays lit through them. Styles: assets/parts/l0010.css."""
from pathlib import Path

RUNGS = [
    # (step classes, number, title, proves, can't)
    ("s1", "1", "Raw transcript (.jsonl, /export)", "what was asked, run and seen, in order",
     "that anyone read it · it can hold secrets"),
    ("s2 s5", "2", "Git history", "what changed, by whom, in what order",
     "why · and it can be replayed afterwards"),
    ("s3", "3", "Files in the repo", "what exists right now",
     "when it arrived, or what it steered"),
    ("s4 s5", "4", "Notes, README, reflections", "why, in someone’s own words",
     "anything, until checked against 1 and 2"),
]


def rung(i, steps, num, title, proves, cant):
    y = 24 + i * 102
    claim = ' l10-claim' if num == "4" else ''
    return (f'<g class="st {steps}"><rect class="l10-rung{claim}" x="70" y="{y}" width="450" height="88" rx="10"/>'
            f'<circle class="l10-num" cx="100" cy="{y + 44}" r="17"/><text class="l10-numtxt" x="100" y="{y + 50}">{num}</text>'
            f'<text class="l10-title" x="132" y="{y + 28}">{title}</text>'
            f'<text class="l10-proves" x="132" y="{y + 54}">✓ {proves}</text>'
            f'<text class="l10-cant" x="132" y="{y + 76}">✗ {cant}</text></g>')


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 450" role="img" aria-label="A ladder of evidence, strongest '
    'first. 1, the raw transcript: shows what was asked, run and seen, in order, but not that anyone read it, and it can '
    'hold secrets. 2, git history: what changed, by whom and in what order, but not why, and it can be replayed afterwards. '
    '3, files in the repo: what exists now, but not when it arrived. 4, notes, README and reflections: claims, to check '
    'against 1 and 2. Example: a note says JWT was rejected, and a commit one minute later adds JWT, so the note is stale.">',
    '<defs><marker id="l10l-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
    'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
    # strength rail (always visible)
    '<path class="l10-rail" d="M36,40 L36,404" marker-end="url(#l10l-head)"/>'
    '<text class="l10-railtxt" transform="rotate(-90 26 222)" x="26" y="222">stronger  →  weaker</text>',
]
parts += [rung(i, *r) for i, r in enumerate(RUNGS)]
parts += [
    # the claim to check (s4, s5)
    '<g class="st s4 s5"><text class="l10-head" x="560" y="40">Checking one claim</text>'
    '<rect class="l10-card l10-claim" x="560" y="56" width="270" height="78" rx="8"/>'
    '<text class="l10-cardname" x="574" y="80">a note in the repo says</text>'
    '<text class="l10-quote" x="574" y="112">“JWT rejected, not requested”</text>'
    '<path class="l10-link" d="M520,370 C540,370 540,95 556,95"/></g>',
    # the git evidence and the verdict (s5)
    '<g class="st s5"><path class="arc" d="M695,138 L695,178" marker-end="url(#l10l-head)"/>'
    '<text class="l10-small" x="706" y="164">check it against git</text>'
    '<rect class="l10-card" x="560" y="186" width="270" height="78" rx="8"/>'
    '<text class="l10-cardname" x="574" y="210">git log, one minute later</text>'
    '<text class="l10-mono" x="574" y="242">a commit adds JWT</text>'
    '<path class="l10-link" d="M520,170 C540,170 540,225 556,225"/>'
    '<rect class="l10-verdict" x="560" y="290" width="270" height="40" rx="20"/>'
    '<text class="l10-verdicttxt" x="695" y="316">STALE · git contradicts it</text>'
    '<text class="l10-small" x="695" y="360" style="text-anchor:middle">Label each claim TRUE, STALE or</text>'
    '<text class="l10-small" x="695" y="380" style="text-anchor:middle">UNVERIFIABLE, as in lesson 9.</text></g>',
    "</svg>",
]
Path(__file__).with_name("l0010-evidence-ladder.svg").write_text("\n".join(parts) + "\n")
print("wrote l0010-evidence-ladder.svg")
