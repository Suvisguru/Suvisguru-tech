#!/usr/bin/env python3
"""K-Town revision Phase 6 follow-up — fix the dot-strip <ol> list-style bug.

Bug: the K-Town mobile dot-strip (visible at viewport widths <720px on
every lesson) renders as an <ol>, and browsers' default list-style-type
of `decimal` paints the numerals "1. 2. 3. …" on top of the dot pins,
making the strip unreadable. The original CSS scaffolding block didn't
reset list-style on .ktown-strip.

Fix: add a base-level rule

    .ktown-strip{list-style:none;padding:0;margin:0}

just before the existing combined display:none rule. Putting it on a
base rule (outside the @media block) means the reset applies whether
the strip is hidden (>720px) or shown (<=720px). The existing
margin:0;padding:0 inside the @media block are now redundant but
harmless — left untouched to keep the diff minimal.

Idempotent: a second run finds no remaining instances of the original
combined rule and exits cleanly.

Targets all 16 K-COM lesson files (L01–L15 + L7.5 primer).
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = [
    "preview-kubernetes-lesson-01.html",
    "preview-kubernetes-lesson-02.html",
    "preview-kubernetes-lesson-03.html",
    "preview-kubernetes-lesson-04.html",
    "preview-kubernetes-lesson-05.html",
    "preview-kubernetes-lesson-06.html",
    "preview-kubernetes-lesson-07.html",
    "preview-kubernetes-lesson-7-5.html",
    "preview-kubernetes-lesson-08.html",
    "preview-kubernetes-lesson-09.html",
    "preview-kubernetes-lesson-10.html",
    "preview-kubernetes-lesson-11.html",
    "preview-kubernetes-lesson-12.html",
    "preview-kubernetes-lesson-13.html",
    "preview-kubernetes-lesson-14.html",
    "preview-kubernetes-lesson-15.html",
]

OLD = "  .ktown-strip,.ktown-strip-label{display:none}"
NEW = "  .ktown-strip{list-style:none;padding:0;margin:0}\n  .ktown-strip,.ktown-strip-label{display:none}"


def main() -> None:
    fixed = 0
    skipped = 0
    for name in FILES:
        path = os.path.join(ROOT, name)
        content = open(path).read()
        if "ktown-strip{list-style:none" in content:
            print(f"  {name}: already fixed, skipping")
            skipped += 1
            continue
        if OLD not in content:
            sys.exit(f"  {name}: anchor not found — aborting (run failed pre-condition)")
        if content.count(OLD) != 1:
            sys.exit(f"  {name}: anchor matched {content.count(OLD)} times, expected exactly 1")
        new_content = content.replace(OLD, NEW, 1)
        open(path, "w").write(new_content)
        print(f"  {name}: fixed")
        fixed += 1
    print(f"\nDone. Fixed: {fixed}. Already-fixed (skipped): {skipped}.")


if __name__ == "__main__":
    main()
