#!/usr/bin/env python3
"""Lesson 9: docs drift. Claims on the left, the repo's evidence on the right; /update-docs draws a
TRUE / STALE / UNVERIFIABLE line between each pair -> l0009-docs-drift.svg.
Step groups are "st sN". Styles: assets/parts/l0009.css."""
from pathlib import Path

PERSON = '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'

ROWS = [  # (file, claim, evidence file, evidence, verdict, step)
    ("AGENTS.md", "Build: dotnet build -warnaserror", "quality-gate/gate.sh:12", "dotnet build -warnaserror",
     "TRUE", "s2"),
    ("README.md", "Endpoints: 4 listed", "Controllers/*.cs", "6 routes, incl. low-stock, GET orders",
     "STALE", "s3"),
    ("a decisions doc · real project", "JWT: “rejected, not requested”", "git log", "“add JWT”, one minute later",
     "STALE", "s4"),
    ("a notes file", "“we carefully considered SQL Server”", "", "no file, commit or test says so",
     "UNVERIFIABLE", "s5"),
]
TOP, STEP, H = 62, 76, 60


def icon(paths, cx, cy, size=26):
    s = size / 24
    return f'<g class="ico" transform="translate({cx - size / 2:.1f},{cy - size / 2:.1f}) scale({s:.4f})">{paths}</g>'


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 484" role="img" aria-label="Docs drift. Left, four claims '
    'from the docs; right, what the repo shows. The update-docs skill draws a line from each claim to its evidence. '
    'AGENTS.md says build with -warnaserror, and gate.sh line 12 does: TRUE. The README lists 4 endpoints, the controllers '
    'have 6: STALE. A real project’s doc said JWT was rejected, not requested, and git log shows JWT added one minute later: '
    'STALE. “We carefully considered SQL Server” has no file, commit or test behind it: UNVERIFIABLE. It then proposes a '
    'diff for the stale rows only, and waits for you.">',
    '<text class="l9-colhead" x="30" y="40">What the docs say</text>',
    '<text class="l9-colhead" x="520" y="40">What the repo shows</text>',
]
for i, (f, claim, ef, ev, verdict, st) in enumerate(ROWS):
    y = TOP + i * STEP
    cy = y + H / 2
    parts.append(f'<rect class="l9-card" x="30" y="{y}" width="310" height="{H}" rx="9"/>'
                 f'<text class="l9-cardhead" x="44" y="{y + 22}">{f}</text>'
                 f'<text class="l9-claim" x="44" y="{y + 45}">{claim}</text>')
    ecls = "l9-card" if ef else "l9-card l9-empty"
    parts.append(f'<rect class="{ecls}" x="520" y="{y}" width="310" height="{H}" rx="9"/>'
                 + (f'<text class="l9-cardhead" x="534" y="{y + 22}">{ef}</text>'
                    f'<text class="l9-claim" x="534" y="{y + 45}">{ev}</text>' if ef else
                    f'<text class="l9-claim l9-faint" x="534" y="{cy + 5}">{ev}</text>'))
    k = verdict.lower()[:5]
    w = 132 if verdict == "UNVERIFIABLE" else 84
    parts.append(f'<g class="st {st} s6"><line class="l9-link l9-{k}" x1="340" y1="{cy}" x2="520" y2="{cy}"/>'
                 f'<rect class="l9-tag l9-{k}" x="{430 - w / 2}" y="{cy - 13}" width="{w}" height="26" rx="13"/>'
                 f'<text class="l9-tagtxt l9-{k}" x="430" y="{cy + 5}">{verdict}</text></g>')

parts += [
    '<g class="st s1"><text class="l9-caption" x="430" y="470">/update-docs lists each claim, then looks for a file:line, a commit or a test.</text></g>',
    '<g class="st s6">'
    '<rect class="l9-diff" x="140" y="378" width="500" height="64" rx="10"/>'
    '<text class="l9-difftxt" x="160" y="404">Proposed diff, STALE rows only</text>'
    '<text class="l9-code l9-addline" x="160" y="428">+ GET /api/products/low-stock · + GET /api/orders</text>'
    '<path class="arc" d="M640,410 L692,410"/>'
    '<circle class="ring-node" cx="720" cy="410" r="26"/>' + icon(PERSON, 720, 410, 26)
    + '<text class="sub" x="790" y="414">you approve</text></g>',
    "</svg>",
]
Path(__file__).with_name("l0009-docs-drift.svg").write_text("\n".join(parts) + "\n")
print("wrote l0009-docs-drift.svg")
