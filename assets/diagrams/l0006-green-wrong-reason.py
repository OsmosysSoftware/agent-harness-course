#!/usr/bin/env python3
"""Lesson 6: a read-then-write diff stays green, but the stock reviewer blocks it -> l0006-green-wrong-reason.svg.
Step groups are "st sN"; a group listing several steps stays lit through them. Styles: assets/parts/l0006.css."""
from pathlib import Path

CODE = [
    (14, "var product = await db.Products.FindAsync(…);"),
    (15, "if (product is null) return …NotFound;"),
    (16, "if (product.Stock &lt; quantity) return …;"),
    (17, ""),
    (18, "product.Stock -= quantity;"),
    (20, "db.Orders.Add(order);"),
    (21, "await db.SaveChangesAsync(ct);"),
]


def lane(y, name):
    return (f'<text class="l6-lane" x="466" y="{y + 5}">{name}</text>'
            f'<rect class="l6-step" x="540" y="{y - 14}" width="92" height="28" rx="6"/><text class="l6-steptxt" x="586" y="{y + 5}">reads 3</text>'
            f'<rect class="l6-step" x="640" y="{y - 14}" width="80" height="28" rx="6"/><text class="l6-steptxt" x="680" y="{y + 5}">3 ≥ 3 ✓</text>'
            f'<rect class="l6-step l6-stepbad" x="728" y="{y - 14}" width="92" height="28" rx="6"/><text class="l6-steptxt" x="774" y="{y + 5}">writes 0</text>')


code = "".join(
    f'<text class="l6-ln" x="58" y="{y}">{n}</text><text class="l6-code" x="76" y="{y}">{t}</text>'
    for (n, t), y in zip(CODE, range(84, 84 + 22 * len(CODE), 22)))

parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 470" role="img" aria-label="Green for the wrong reason. '
    'A read-then-write version of OrderService passes every test, because each test sends one order at a time. '
    'Two orders arriving together both read stock 3, both pass the check and both write 0: six units sold of three. '
    'Measured: 12 concurrent orders for 3 units all succeed without the transaction, and exactly 3 succeed inside one on '
    'SQLite, because the provider locks up front. The stock reviewer reads the code’s shape and blocks line 18.">',
    # s1: the diff
    '<g class="st s1 s2 s5"><rect class="l6-doc" x="30" y="20" width="412" height="226" rx="10"/>'
    '<text class="l6-docname" x="46" y="50">OrderService.cs · scratch branch</text>' + code + '</g>',
    # s2: tests green
    '<g class="st s2"><rect class="chip pass" x="30" y="264" width="250" height="34" rx="17"/>'
    '<text class="chiptxt" x="155" y="286">dotnet test · all passed ✓</text>'
    '<text class="l6-note" x="30" y="324">each test sends one order at a time,</text>'
    '<text class="l6-note" x="30" y="344">so nothing races</text></g>',
    # s3: two orders together
    '<g class="st s3"><text class="l6-head" x="466" y="44">Two orders of 3, stock 3, same moment</text>'
    + lane(84, "Order A") + lane(126, "Order B")
    + '<text class="l6-oversell" x="640" y="180" style="text-anchor:middle">2 orders created · 6 sold of 3</text></g>',
    # s4: measured
    '<g class="st s4"><rect class="l6-measure" x="456" y="206" width="380" height="122" rx="10"/>'
    '<text class="l6-key" x="466" y="230">MEASURED · 12 orders for 3 units, at once</text>'
    '<text class="l6-txt" x="466" y="260">without a transaction</text><text class="l6-bad" x="814" y="260" style="text-anchor:end">12 succeed</text>'
    '<text class="l6-txt" x="466" y="288">inside BeginTransaction (SQLite)</text><text class="l6-ok" x="814" y="288" style="text-anchor:end">3 succeed</text>'
    '<text class="l6-note" x="466" y="314">the second is the provider’s lock, not the design</text></g>',
    # s5: the reviewer blocks the line
    '<g class="st s5"><rect class="l6-hit" x="70" y="153" width="220" height="22" rx="4"/>'
    '<path class="l6-point" d="M290,164 L449,164 L449,356"/>'
    '<rect class="l6-row" x="300" y="356" width="530" height="40" rx="8"/>'
    '<text class="l6-code l6-strong" x="316" y="381">OrderService.cs:18 · read-then-write</text>'
    '<rect class="l6-block" x="652" y="362" width="164" height="28" rx="14"/><text class="l6-blocktxt" x="734" y="381">Verdict: BLOCK</text>'
    '<text class="l6-caption" x="430" y="432" style="text-anchor:middle">The tests check results they can see. The reviewer checks the shape of the code.</text></g>',
    "</svg>",
]
Path(__file__).with_name("l0006-green-wrong-reason.svg").write_text("\n".join(parts) + "\n")
print("wrote l0006-green-wrong-reason.svg")
