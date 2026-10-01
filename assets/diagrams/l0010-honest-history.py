#!/usr/bin/env python3
"""Lesson 10: an honest history vs a replayed one, and a mistake fixed forward vs force-pushed away
-> l0010-honest-history.svg. Step groups are "st sN". Styles: assets/parts/l0010.css."""
from pathlib import Path

X0, X1 = 200, 820          # time axis, 09:00 .. 18:00
HOURS = ["09:00", "12:00", "15:00", "18:00"]


def axis(y):
    out = f'<path class="l10-axis" d="M{X0},{y} L{X1},{y}"/>'
    for i, h in enumerate(HOURS):
        x = X0 + i * (X1 - X0) / 3
        out += (f'<path class="l10-tick" d="M{x:.0f},{y - 6} L{x:.0f},{y + 6}"/>'
                f'<text class="l10-hour" x="{x:.0f}" y="{y + 24}">{h}</text>')
    return out


# honest: commits when slices went green
HONEST = [0.06, 0.13, 0.27, 0.34, 0.46, 0.58, 0.63, 0.77, 0.88, 0.95]
honest = "".join(f'<circle class="l10-dot" cx="{X0 + f * (X1 - X0):.0f}" cy="70" r="7"/>' for f in HONEST)

# replayed: a stack at one instant
bx = X0 + 0.92 * (X1 - X0)
stack = "".join(f'<rect class="l10-burst" x="{bx - 9:.0f}" y="{196 - i * 9}" width="18" height="7" rx="2"/>'
                for i in range(11))


def commit(x, y, label, cls=""):
    return (f'<circle class="l10-commit {cls}" cx="{x}" cy="{y}" r="17"/>'
            f'<text class="l10-ctxt {cls}" x="{x}" y="{y + 5}">{label}</text>')


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 560" role="img" aria-label="Top: an honest history has '
    'commits spread across the day, one per finished slice. A replayed history has dozens of commits stamped with the '
    'same second, written after the work was done. Bottom: a mistake on a shared branch. Fixed forward, a new revert '
    'commit undoes it and both stay visible. Force-pushed away, the remote is rewritten, teammates’ copies no longer '
    'match, and the record of the mistake is gone; branch protection can refuse the push.">',
    '<defs><marker id="l10h-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
    'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
    # row 1: honest
    '<g class="st s1"><text class="l10-row" x="30" y="66">Honest</text>'
    '<text class="l10-rowsub" x="30" y="86">one commit per slice</text>'
    + axis(70) + honest + '</g>',
    # row 2: replayed
    '<g class="st s2"><text class="l10-row" x="30" y="186">Replayed</text>'
    '<text class="l10-rowsub" x="30" y="206">written afterwards</text>'
    + axis(206) + stack +
    f'<text class="l10-burstlbl" x="{bx - 22:.0f}" y="112" style="text-anchor:end">56 commits, one timestamp</text>'
    f'<path class="l10-lead" d="M{bx - 18:.0f},108 L{bx - 4:.0f},108 L{bx - 4:.0f},100"/>'
    '<rect class="l10-term" x="200" y="122" width="430" height="46" rx="6"/>'
    '<text class="l10-mono" x="214" y="141">$ git log --format=%ci | sort | uniq -c | awk …</text>'
    '<text class="l10-mono l10-badtxt" x="214" y="160">     56 ‹the same second›</text></g>',
    '<path class="l10-divider" d="M30,262 L830,262"/>',
    '<text class="l10-head" x="30" y="296">A mistake reaches the shared branch</text>',
    # bottom left: the chain with the mistake (s3, s5)
    '<g class="st s3 s5"><text class="l10-sidehead" x="30" y="336">Fix forward</text>'
    '<path class="l10-chain" d="M54,390 L330,390"/>'
    + commit(54, 390, "A") + commit(144, 390, "B") + commit(234, 390, "X", "l10-x")
    + '<text class="l10-small" x="234" y="436" style="text-anchor:middle">the mistake</text></g>',
    # revert (s5)
    '<g class="st s5">' + commit(324, 390, "R", "l10-r")
    + '<text class="l10-small" x="324" y="436" style="text-anchor:middle">git revert X</text>'
    '<text class="l10-good" x="30" y="482">✓ X and its undo both stay in the log</text>'
    '<text class="l10-good" x="30" y="506">✓ every copy of the branch still agrees</text></g>',
    # bottom right: force-push (s4)
    '<g class="st s4"><text class="l10-sidehead" x="470" y="336">Force-push it away</text>'
    '<path class="l10-chain" d="M494,390 L640,390"/>'
    + commit(494, 390, "A") + commit(584, 390, "B")
    + '<circle class="l10-ghost" cx="674" cy="390" r="17"/><text class="l10-ctxt l10-gtxt" x="674" y="395">X</text>'
    '<path class="l10-strike" d="M656,372 L692,408 M692,372 L656,408"/>'
    '<rect class="l10-refuse" x="712" y="372" width="118" height="36" rx="8"/>'
    '<text class="l10-refusetxt" x="771" y="388">branch protection</text>'
    '<text class="l10-refusetxt" x="771" y="402">can refuse it</text>'
    '<text class="l10-badtxt l10-plain" x="470" y="482">✗ teammates who pulled X no longer match</text>'
    '<text class="l10-badtxt l10-plain" x="470" y="506">✗ the record of the mistake is gone</text></g>',
    "</svg>",
]
Path(__file__).with_name("l0010-honest-history.svg").write_text("\n".join(parts) + "\n")
print("wrote l0010-honest-history.svg")
