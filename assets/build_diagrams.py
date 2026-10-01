#!/usr/bin/env python3
"""Render each diagram to SVG and inline it into the pages that reference it.
A diagram is assets/diagrams/<name>.py (a script that writes <name>.svg, for illustrations)
or assets/diagrams/<name>.d2 (rendered with D2, for flowcharts).

A page marks the spot with:  <!-- d2:agent-loop --> ... <!-- /d2 -->
Everything between the markers is replaced by the current SVG, so re-running is safe.
Needs the `d2` binary (https://github.com/terrastruct/d2/releases). Usage: python3 assets/build_diagrams.py
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIAGRAMS = ROOT / "assets" / "diagrams"
MARK = re.compile(r"(<!-- d2:([\w-]+) -->)(.*?)(<!-- /d2 -->)", re.S)


def render(name: str) -> str:
    out = DIAGRAMS / f"{name}.svg"
    py, d2 = DIAGRAMS / f"{name}.py", DIAGRAMS / f"{name}.d2"
    if py.exists():
        subprocess.run(["python3", str(py)], check=True, capture_output=True)
    elif d2.exists() and (not out.exists() or out.stat().st_mtime < d2.stat().st_mtime):
        subprocess.run(["d2", "--pad", "8", str(d2), str(out)], check=True, capture_output=True)
    svg = out.read_text(encoding="utf-8")
    return re.sub(r"^<\?xml[^>]*>\s*", "", svg).strip()


def main():
    for page in sorted(list(ROOT.glob("lessons/*.html")) + list(ROOT.glob("reference/*.html")) + [ROOT / "index.html"]):
        text = page.read_text(encoding="utf-8")
        new = MARK.sub(lambda m: f"{m.group(1)}\n{render(m.group(2))}\n{m.group(4)}", text)
        if new != text:
            page.write_text(new, encoding="utf-8")
            print(f"inlined diagrams into {page.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
