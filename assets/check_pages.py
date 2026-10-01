#!/usr/bin/env python3
"""Lint course pages: quiz fairness, local links, no external resources, stylesheet linked.

Usage: python3 assets/check_pages.py [files...]   (default: every lessons/*.html, reference/*.html and index.html)
Exit 1 on any problem.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.srcs, self.styles = [], [], 0
        self.quizzes = []          # list of lists of (text, correct)
        self.in_opt = None
        self.quiz_depth = 0
        self.depth = 0
        self.has_css = False
        self.svg = 0               # <style> inside a rendered diagram's <svg> is allowed

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.depth += 1
        cls = (a.get("class") or "").split()
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("script", "img", "iframe") and a.get("src"):
            self.srcs.append(a["src"])
        if tag == "link" and a.get("rel") == "stylesheet":
            self.srcs.append(a.get("href", ""))
            if a.get("href", "").endswith("assets/course.css"):
                self.has_css = True
        if tag == "svg":
            self.svg += 1
        if tag == "style" and not self.svg:
            self.styles += 1
        if tag == "div" and "quiz" in cls:
            self.quizzes.append([])
        if tag == "button" and "opt" in cls:
            self.in_opt = ["", "data-correct" in a]

    def handle_endtag(self, tag):
        self.depth -= 1
        if tag == "svg":
            self.svg -= 1
        if tag == "button" and self.in_opt is not None:
            self.quizzes[-1].append((self.in_opt[0].strip(), self.in_opt[1]))
            self.in_opt = None

    def handle_data(self, data):
        if self.in_opt is not None:
            self.in_opt[0] += data


def check(path: Path):
    problems = []
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    if not p.has_css:
        problems.append("does not link ../assets/course.css")
    if p.styles:
        problems.append(f"{p.styles} inline <style> block(s); put styles in assets/course.css")
    for s in p.srcs:
        if re.match(r"^(https?:)?//", s):
            problems.append(f"external resource: {s}")
    for href in p.links:
        if re.match(r"^(https?:|mailto:|#)", href):
            continue
        target = (path.parent / href.split("#")[0]).resolve()
        if not target.exists():
            problems.append(f"broken local link: {href}")
    for i, q in enumerate(p.quizzes, 1):
        if not q:
            problems.append(f"quiz {i}: no options")
            continue
        correct = sum(1 for _, c in q if c)
        if correct != 1:
            problems.append(f"quiz {i}: {correct} options marked data-correct (need exactly 1)")
        words = [len(t.split()) for t, _ in q]
        chars = [len(t) for t, _ in q]
        if len(set(words)) != 1:
            problems.append(f"quiz {i}: option word counts differ {words}: " + " | ".join(t for t, _ in q))
        if max(chars) - min(chars) > 8:
            problems.append(f"quiz {i}: option lengths differ by {max(chars) - min(chars)} chars {chars}")
    return problems


def main(argv):
    files = [Path(a).resolve() for a in argv] or sorted(
        list((ROOT / "lessons").glob("*.html")) + list((ROOT / "reference").glob("*.html")) + [ROOT / "index.html"])
    bad = 0
    for f in files:
        if not f.exists():
            continue
        probs = check(f)
        if probs:
            bad += 1
            print(f"✗ {f.relative_to(ROOT)}")
            for pr in probs:
                print(f"    - {pr}")
        else:
            print(f"✓ {f.relative_to(ROOT)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
