#!/usr/bin/env python3
"""Lesson 9: unusual-but-deliberate code, a fresh agent asked to "simplify" it, with and without a pointer
to the ADR -> l0009-odd-code.svg. Step groups are "st sN"; a group listing several steps stays lit through
them. Styles: assets/parts/l0009.css."""
from pathlib import Path

AGENT = '<rect x="4" y="7" width="16" height="12" rx="3"/><path d="M12 7V3"/><circle cx="9" cy="13" r="1.2"/><circle cx="15" cy="13" r="1.2"/>'


def icon(paths, cx, cy, size=26):
    s = size / 24
    return f'<g class="ico" transform="translate({cx - size / 2:.1f},{cy - size / 2:.1f}) scale({s:.4f})">{paths}</g>'


def card(x, y, w, h, name, lines, cls="", start=0):
    out = [f'<rect class="l9-card {cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/>',
           f'<text class="l9-cardhead" x="{x + 14}" y="{y + 22}">{name}</text>']
    for i, (t, c) in enumerate(lines):
        out.append(f'<text class="l9-code {c}" x="{x + 14}" y="{y + 48 + start + i * 21}">{t}</text>')
    return "".join(out)


GUARDED = [
    ("var updated = await db.Products", ""),
    ("\u00a0\u00a0.Where(p =&gt; p.Stock &gt;= q &amp;&amp; …)", ""),
    ("\u00a0\u00a0.ExecuteUpdateAsync(… Stock - q …);", ""),
    ("if (updated == 0) return …;", ""),
]

parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 520" role="img" aria-label="The agent fixes what looks odd. '
    'Top: the stock update is one guarded ExecuteUpdateAsync with no comment. A fresh agent asked to simplify it rewrites it as '
    'load the product, check, subtract, save: shorter, and it oversells under concurrent orders. Bottom: the same code with a '
    'one-line comment pointing to docs/decisions/0001. The agent follows the pointer, reads the decision record, declines, cites '
    '0001 and offers options. Likelier, not guaranteed: the reviewer and the concurrency test still back it up.">',
    '<defs><marker id="l9o-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
    'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
    # lane labels
    '<text class="l9-lane" x="30" y="26">Code alone</text>',
    '<text class="l9-lane" x="30" y="282">Code + a one-line pointer + an ADR</text>',
    '<line class="l9-divider" x1="30" y1="252" x2="830" y2="252"/>',
    # lane A: the odd-looking code
    '<g class="st s1 s2">' + card(30, 38, 330, 140, "OrderService.cs", GUARDED)
    + '<text class="l9-note" x="30" y="204">no entity loaded, no <tspan class="l9-mono">Stock -= q</tspan>: it looks odd</text></g>',
    # lane A: a fresh agent "simplifies" it
    '<g class="st s2">'
    '<rect class="l9-prompt" x="372" y="74" width="128" height="30" rx="15"/>'
    '<text class="l9-prompttxt" x="436" y="94">“simplify this”</text>'
    + icon(AGENT, 436, 134, 28)
    + '<path class="arc" d="M364,150 L508,150" marker-end="url(#l9o-head)"/>'
    + card(520, 38, 310, 140, "the agent’s rewrite", [
        ("var p = await …FindAsync(id);", "l9-bad"),
        ("if (p.Stock &lt; q) return …;", "l9-bad"),
        ("p.Stock -= q;", "l9-bad"),
        ("await db.SaveChangesAsync();", "l9-bad"),
    ], "l9-badcard")
    + '<text class="l9-verdict l9-badtxt" x="675" y="204">shorter, and it oversells</text></g>',
    # lane B: the same code, with the pointer
    '<g class="st s3 s4 s5">'
    '<rect class="l9-hl" x="38" y="324" width="314" height="22" rx="4"/>'
    + card(30, 294, 330, 162, "OrderService.cs", [("// … see docs/decisions/0001.", "l9-comment")] + GUARDED)
    + '</g>',
    # s3: it follows the pointer to the ADR
    '<g class="st s3 s4 s5">'
    + icon(AGENT, 436, 300, 28)
    + '<path class="arc" d="M352,335 C420,335 450,335 508,335" marker-end="url(#l9o-head)"/>'
    '<text class="l9-small" x="436" y="356">follows the pointer</text>'
    + card(520, 294, 310, 92, "docs/decisions/0001-…md", [
        ("Decision: one guarded UPDATE", "l9-docline"),
        ("load, check, save oversells", "l9-docline"),
    ], "l9-doc")
    + '</g>',
    # s4: declines and cites it
    '<g class="st s4 s5">'
    '<rect class="l9-reply" x="520" y="398" width="310" height="58" rx="10"/>'
    '<text class="l9-replytxt" x="534" y="421">Declined: 0001 forbids load-check-save.</text>'
    '<text class="l9-replysub" x="534" y="443">Options: keep it, or a new ADR you approve.</text>'
    '</g>',
    # s5: the honest caveat
    '<g class="st s5">'
    '<text class="l9-caption" x="430" y="496">Likelier, not guaranteed: the stock reviewer and ConcurrencyTests still back it up.</text>'
    '</g>',
    "</svg>",
]
Path(__file__).with_name("l0009-odd-code.svg").write_text("\n".join(parts) + "\n")
print("wrote l0009-odd-code.svg")
