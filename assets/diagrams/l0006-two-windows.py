#!/usr/bin/env python3
"""Lesson 6: the author's crowded window grading itself vs a reviewer's clean window -> l0006-two-windows.svg.
Step groups are "st sN"; a group listing several steps stays lit through them. Styles: assets/parts/l0006.css."""
from pathlib import Path

PERSON = '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'


def icon(paths, cx, cy, size=30):
    s = size / 24
    return f'<g class="ico" transform="translate({cx - size / 2:.1f},{cy - size / 2:.1f}) scale({s:.4f})">{paths}</g>'


def bubble(y, text, cls=""):
    return (f'<rect class="l6-bubble {cls}" x="52" y="{y}" width="336" height="30" rx="9"/>'
            f'<text class="l6-txt {cls}" x="66" y="{y + 20}">{text}</text>')


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 500" role="img" aria-label="Two context windows. '
    'Left, the author agent’s window is crowded with its own request, workaround, assumption that row locking makes '
    'it safe, and green tests; asked to review itself, it says looks good. Right, a reviewer subagent starts with a '
    'clean window holding only the diff and the invariants file. It points at OrderService.cs line 19, the read-then-write '
    'decrement, marks it a blocker and returns Verdict: BLOCK to you, and you decide.">',
    '<defs><marker id="l6w-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
    'orient="auto-start-reverse"><path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
    # the two windows (always visible)
    '<rect class="l6-win" x="30" y="20" width="380" height="380" rx="12"/>',
    '<rect class="l6-winbar" x="30" y="20" width="380" height="34" rx="12"/><rect class="l6-winbar" x="30" y="40" width="380" height="14"/>',
    '<text class="l6-wintitle" x="48" y="43">Author’s window</text><text class="l6-winmeta" x="392" y="43">most of it full</text>',
    '<rect class="l6-win" x="450" y="20" width="380" height="380" rx="12"/>',
    '<rect class="l6-winbar" x="450" y="20" width="380" height="34" rx="12"/><rect class="l6-winbar" x="450" y="40" width="380" height="14"/>',
    '<text class="l6-wintitle" x="468" y="43">Reviewer’s window</text><text class="l6-winmeta" x="812" y="43">fresh, almost empty</text>',
    # s1: the author's window fills with its own story
    '<g class="st s1 s2">'
    '<text class="l6-faint" x="52" y="78">… many earlier turns …</text>'
    + bubble(88, "you: simplify PlaceAsync")
    + bubble(124, "InMemory can’t run ExecuteUpdateAsync")
    + bubble(160, "so: load, check, decrement, save")
    + bubble(196, "“row locking keeps this safe”", "l6-assume")
    + bubble(232, "dotnet test: all passed ✓")
    + '<text class="l6-faint" x="52" y="290">its reasons, its assumptions, its fix</text></g>',
    # s2: it grades itself
    '<g class="st bad s2"><path class="arc" d="M392,212 C420,240 420,300 360,322" marker-end="url(#l6w-head)"/>'
    '<g transform="rotate(-5 200 340)"><rect class="l6-stamp-ok" x="96" y="314" width="210" height="52" rx="8"/>'
    '<text class="l6-stamptxt-ok" x="201" y="340">LOOKS GOOD</text>'
    '<text class="l6-stampsub-ok" x="201" y="358">judged by its own assumptions</text></g></g>',
    # s3: the reviewer starts clean with two inputs only
    '<g class="st s3 s4 s5">'
    '<rect class="l6-doc" x="470" y="70" width="340" height="128" rx="8"/>'
    '<text class="l6-docname" x="484" y="91">git diff HEAD</text>'
    '<text class="l6-code l6-del" x="484" y="115">- .ExecuteUpdateAsync(… Stock &gt;= n …)</text>'
    '<text class="l6-code l6-add" x="484" y="137">+ var product = await …FindAsync(…)</text>'
    '<text class="l6-code l6-add" x="484" y="159">+ if (product.Stock &lt; quantity) return …</text>'
    '<text class="l6-code l6-add" x="484" y="181">+ product.Stock -= quantity;</text>'
    '<rect class="l6-doc" x="470" y="210" width="340" height="56" rx="8"/>'
    '<text class="l6-docname" x="484" y="231">docs/ai/invariants.md</text>'
    '<text class="l6-code" x="484" y="253">never read-then-write stock</text>'
    '<text class="l6-faint" x="640" y="292" style="text-anchor:middle">no chat, no reasons, no “I’m sure”</text></g>',
    # s4: points at file:line
    '<g class="st s4 s5"><rect class="l6-hit" x="476" y="166" width="236" height="22" rx="4"/>'
    '<text class="l6-code l6-add l6-strong" x="484" y="181">+ product.Stock -= quantity;</text>'
    '<path class="l6-point" d="M712,177 L822,177 L822,329 L812,329"/>'
    '<rect class="l6-row" x="470" y="312" width="340" height="34" rx="6"/>'
    '<text class="l6-code l6-strong" x="482" y="334">OrderService.cs:19</text>'
    '<text class="l6-sev" x="702" y="334">BLOCKER</text></g>',
    # s5: verdict to the human, who decides
    '<g class="st s5"><rect class="l6-block" x="560" y="356" width="160" height="32" rx="16"/>'
    '<text class="l6-blocktxt" x="640" y="377">Verdict: BLOCK</text></g>',
    '<g class="st s5"><path class="arc" d="M640,392 C640,440 520,456 470,456" marker-end="url(#l6w-head)"/>'
    '<circle class="ring-node" cx="430" cy="456" r="30"/>' + icon(PERSON, 430, 456, 30)
    + '<text class="lbl" x="335" y="452" style="text-anchor:end">You decide</text>'
    '<text class="sub" x="335" y="472" style="text-anchor:end">fix, reject or ask why</text></g>',
    "</svg>",
]
Path(__file__).with_name("l0006-two-windows.svg").write_text("\n".join(parts) + "\n")
print("wrote l0006-two-windows.svg")
