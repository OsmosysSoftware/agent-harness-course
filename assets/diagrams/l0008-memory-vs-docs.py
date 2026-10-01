#!/usr/bin/env python3
"""Lesson 8: the same slice written from memory (500) vs after a docs lookup (200) -> l0008-memory-vs-docs.svg.
Step groups are "st sN"; a group listing several steps stays lit through them. Styles: assets/parts/l0008.css.
The error text and the 200 response were measured on the course's reference solution (2026-10-01)."""
from pathlib import Path


def lines(x, y, rows, cls, gap=19):
    return "".join(f'<text class="{cls}" x="{x}" y="{y + i * gap}">{t}</text>' for i, t in enumerate(rows))


def arrow(x1, x2, y, cls=""):
    return f'<path class="arc {cls}" d="M{x1},{y} L{x2},{y}" marker-end="url(#l8m-head)"/>'


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 500" role="img" aria-label="The same slice, two ways. '
    'Top lane, from memory: the agent writes OrderByDescending on CreatedAt, a DateTimeOffset. It compiles, but GET '
    '/api/orders answers 500, and the API log says SQLite does not support expressions of type DateTimeOffset in '
    'ORDER BY clauses. Bottom lane, docs first: the agent calls the context7 query-docs tool, reads that comparison and '
    'ordering of DateTimeOffset need evaluation on the client, stores CreatedAt with DateTimeOffsetToBinaryConverter, '
    'and GET /api/orders answers 200, newest first, with the test green.">',
    '<defs><marker id="l8m-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
    'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
    # lanes (always visible)
    '<rect class="l8-lane l8-lane-bad" x="14" y="14" width="832" height="220" rx="14"/>',
    '<text class="l8-lanetitle l8-badtxt" x="34" y="42">FROM MEMORY</text>',
    '<text class="l8-lanesub" x="160" y="42">the API as the model remembers it</text>',
    '<rect class="l8-lane" x="14" y="258" width="832" height="228" rx="14"/>',
    '<text class="l8-lanetitle l8-goodtxt" x="34" y="286">DOCS FIRST</text>',
    '<text class="l8-lanesub" x="140" y="286">the API as the docs describe it today</text>',
    # s1: the query from memory
    '<g class="st s1 s2">'
    '<rect class="panel" x="34" y="58" width="262" height="150" rx="10"/>'
    '<text class="mono strong" x="48" y="82">OrdersController.cs</text>'
    + lines(48, 108, ["await db.Orders", "  .OrderByDescending(", "     o =&gt; o.CreatedAt)", "  .ToListAsync(ct);"], "l8-code")
    + '<text class="l8-comment" x="48" y="194">// CreatedAt is a DateTimeOffset</text></g>',
    '<g class="st s1"><rect class="chip pass" x="318" y="66" width="150" height="30" rx="15"/>'
    '<text class="chiptxt" x="393" y="86">it compiles ✓</text></g>',
    # s2: the request fails
    '<g class="st s2">' + arrow(298, 324, 150, "l8-arrbad")
    + '<rect class="l8-fail" x="330" y="112" width="140" height="76" rx="10"/>'
    '<text class="l8-mono-sm" x="400" y="134" style="text-anchor:middle">GET /api/orders</text>'
    '<text class="l8-big l8-badtxt" x="400" y="174" style="text-anchor:middle">500</text>'
    + arrow(472, 498, 150, "l8-arrbad")
    + '<rect class="l8-term" x="504" y="58" width="326" height="158" rx="10"/>'
    '<text class="l8-termhead" x="518" y="80">API log</text>'
    + lines(518, 106, ["System.NotSupportedException:", "SQLite does not support expressions", "of type 'DateTimeOffset' in ORDER BY",
                       "clauses. Convert the values to a", "supported type, or use LINQ to …"], "l8-termtxt")
    + '</g>',
    # s3: the lookup
    '<g class="st s3 s4 s5">'
    '<rect class="panel" x="34" y="302" width="262" height="170" rx="10"/>'
    '<rect class="l8-tool" x="46" y="314" width="238" height="28" rx="14"/>'
    '<text class="l8-tooltxt" x="165" y="333">mcp__context7__query-docs</text>'
    '<text class="l8-q" x="48" y="364">“EF Core SQLite limitations”</text>'
    + lines(48, 394, ["“DateTimeOffset … comparison", "and ordering will require", "evaluation on the client”"], "l8-quote", 20)
    + '<text class="l8-src" x="48" y="458">EF Core docs, via context7</text></g>',
    # s4: the converter
    '<g class="st s4 s5">' + arrow(298, 324, 386)
    + '<rect class="panel" x="330" y="302" width="300" height="170" rx="10"/>'
    '<text class="mono strong" x="344" y="326">StockDbContext.cs</text>'
    + lines(344, 352, [".Property(o =&gt; o.CreatedAt)", ".HasConversion(new", "  DateTimeOffsetToBinaryConverter())"], "l8-code")
    + lines(344, 420, ["stored as an INTEGER that SQLite", "can sort; the query stays the same"], "l8-note", 18)
    + '</g>',
    # s5: green
    '<g class="st s5">' + arrow(632, 650, 386)
    + '<rect class="l8-ok" x="656" y="318" width="174" height="140" rx="10"/>'
    '<text class="l8-mono-sm" x="743" y="342" style="text-anchor:middle">GET /api/orders</text>'
    '<text class="l8-big l8-goodtxt" x="743" y="384" style="text-anchor:middle">200</text>'
    '<text class="l8-note" x="743" y="410" style="text-anchor:middle">newest first</text>'
    '<rect class="chip pass" x="676" y="422" width="134" height="26" rx="13"/>'
    '<text class="chiptxt" x="743" y="440">dotnet test ✓</text></g>',
    "</svg>",
]
Path(__file__).with_name("l0008-memory-vs-docs.svg").write_text("\n".join(parts) + "\n")
print("wrote l0008-memory-vs-docs.svg")
