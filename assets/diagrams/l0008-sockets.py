#!/usr/bin/env python3
"""Lesson 8: what an MCP server is -- a process that plugs extra tools into the harness -> l0008-sockets.svg.
Step groups are "st sN"; a group listing several steps stays lit through them. Styles: assets/parts/l0008.css.
Tool names were measured with tools/list against @upstash/context7-mcp@4.1.1 (2026-10-01)."""
from pathlib import Path


def lines(x, y, rows, cls, gap=19):
    return "".join(f'<text class="{cls}" x="{x}" y="{y + i * gap}">{t}</text>' for i, t in enumerate(rows))


def socket(x, y):
    return (f'<rect class="l8-socket" x="{x}" y="{y - 16}" width="22" height="32" rx="5"/>'
            f'<circle class="l8-pin" cx="{x + 11}" cy="{y - 6}" r="2.6"/><circle class="l8-pin" cx="{x + 11}" cy="{y + 6}" r="2.6"/>')


def plug(x, y):
    return (f'<rect class="l8-plug" x="{x}" y="{y - 13}" width="24" height="26" rx="5"/>'
            f'<path class="l8-prong" d="M{x},{y - 6} L{x - 10},{y - 6} M{x},{y + 6} L{x - 10},{y + 6}"/>')


LOCK = ('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>')

parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 500" role="img" aria-label="What an MCP server is. '
    'Claude Code, the harness, has built-in tools such as Read, Edit and Bash, and two sockets. The context7 server, '
    'named in .mcp.json and started with npx at a pinned version, plugs into one socket. It is a process on your '
    'machine running as you, and it sends your query to context7.com. Its two tools, mcp__context7__resolve-library-id '
    'and mcp__context7__query-docs, join the tool list and pass the same permission check as any tool. A lock on its '
    'cable shows that a project server waits for your approval. A community SQLite server stays unplugged: its vetting '
    'tag has unanswered questions, so it is not added; read-only data comes through Bash with sqlite3 -readonly -safe.">',
    # harness (always visible)
    '<rect class="l8-harness" x="20" y="40" width="360" height="420" rx="16"/>',
    '<text class="lbl" x="200" y="72">Claude Code (the harness)</text>',
    '<text class="sub" x="200" y="94">runs the loop from lesson 1</text>',
    '<text class="l8-key" x="44" y="132">TOOLS THE MODEL CAN CALL</text>',
    '<rect class="l8-row" x="40" y="142" width="320" height="30" rx="7"/>'
    '<text class="l8-code" x="54" y="162">Read · Edit · Write · Bash · …</text>',
    socket(370, 230), socket(370, 380),
    # s1: built-ins only
    '<g class="st s1"><text class="l8-note" x="356" y="132" style="text-anchor:end">built in</text></g>',
    # s2: .mcp.json starts a process
    '<g class="st s2 s3 s4">'
    '<path class="l8-cable" d="M392,230 C430,230 430,150 470,150"/>' + plug(470, 150)
    + '<rect class="l8-server" x="494" y="58" width="346" height="190" rx="12"/>'
    '<text class="l8-srvname" x="512" y="86">context7</text>'
    '<text class="l8-srvsub" x="600" y="86">an MCP server</text>'
    '<text class="l8-mono-sm" x="512" y="112">npx -y @upstash/context7-mcp@4.1.1</text>'
    + lines(512, 140, ["a process on your machine,", "running as you"], "l8-plain", 19)
    + lines(512, 192, ["sends your question to context7.com,", "returns library docs as text"], "l8-note", 18)
    + '</g>',
    # s3: its tools join the list
    '<g class="st s3 s4">'
    '<rect class="l8-row l8-new" x="40" y="182" width="320" height="30" rx="7"/>'
    '<text class="l8-code" x="52" y="202">mcp__context7__resolve-library-id</text>'
    '<rect class="l8-row l8-new" x="40" y="218" width="320" height="30" rx="7"/>'
    '<text class="l8-code" x="52" y="238">mcp__context7__query-docs</text>'
    '<text class="l8-note" x="44" y="272">same permission check as any tool</text></g>',
    # s4: approval lock on the cable
    '<g class="st s4"><circle class="l8-lockbg" cx="431" cy="190" r="20"/>'
    '<g class="l8-lock" transform="translate(419,178)">' + LOCK + '</g>'
    '<rect class="l8-badge" x="494" y="258" width="346" height="34" rx="17"/>'
    '<text class="l8-badgetxt" x="667" y="280">⏸ Pending approval until you say yes</text></g>',
    # s5: a candidate that stays unplugged
    '<g class="st s5">'
    '<path class="l8-cable l8-loose" d="M392,380 C420,380 440,392 452,400"/>'
    '<rect class="l8-server l8-cand" x="494" y="312" width="346" height="164" rx="12"/>'
    '<text class="l8-srvname" x="512" y="340">a community SQLite server</text>'
    '<text class="l8-q" x="512" y="368">☐ who maintains it? when was its last release?</text>'
    '<text class="l8-q" x="512" y="392">☐ have you read the source?</text>'
    '<text class="l8-q" x="512" y="416">☐ can it write, delete or run commands?</text>'
    '<g transform="rotate(-6 760 452)"><rect class="l8-stamp" x="688" y="434" width="138" height="34" rx="6"/>'
    '<text class="l8-stamptxt" x="757" y="457">NOT ADDED</text></g>'
    '<rect class="l8-row l8-alt" x="40" y="396" width="320" height="48" rx="7"/>'
    '<text class="l8-code" x="52" y="416">Bash: sqlite3 -readonly -safe …</text>'
    '<text class="l8-note" x="52" y="436">the database engine refuses writes</text></g>',
    "</svg>",
]
Path(__file__).with_name("l0008-sockets.svg").write_text("\n".join(parts) + "\n")
print("wrote l0008-sockets.svg")
