#!/usr/bin/env python3
"""Bring L01-L18 strips + footer in line with the L19-L44 generator output.

After the L18-L44 batch, the curriculum is 45 lessons total (L01-L17
+ L7.5 primer + L18-L44). The lesson generator now produces 45 strip
dots with the active dot at index = lesson number (L7.5 occupies
index 7), strip label "lesson N of 45", and footer "Lesson N of 45".

Older lessons:
  - L01-L15 + L7.5: 24 dots after the L16/L17 expansion + my recent
    24-pin expansion. Active dot at lesson_num index. Footer/strip
    label say "of 16/17/18" (case-mixed bug in the prior expansion).
  - L18: 30 dots (24 + 6 over-expansion bug). Active dot at index 18.
    Footer/strip label say "of 24" (already updated by my prior pass).

This script normalises:
  - Strip dot count → 45
  - Active dot at index = strip_index_for(lesson_num)
  - All "Lesson|lesson N of M" suffixes → "of 45"

Idempotent.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from k8s_lesson_generator import _strip_index_for, TOTAL_LESSONS_IN_CURRICULUM  # noqa: E402

LESSON_FILES = [
    ("01", "preview-kubernetes-lesson-01.html"),
    ("02", "preview-kubernetes-lesson-02.html"),
    ("03", "preview-kubernetes-lesson-03.html"),
    ("04", "preview-kubernetes-lesson-04.html"),
    ("05", "preview-kubernetes-lesson-05.html"),
    ("06", "preview-kubernetes-lesson-06.html"),
    ("07", "preview-kubernetes-lesson-07.html"),
    ("7-5", "preview-kubernetes-lesson-7-5.html"),
    ("08", "preview-kubernetes-lesson-08.html"),
    ("09", "preview-kubernetes-lesson-09.html"),
    ("10", "preview-kubernetes-lesson-10.html"),
    ("11", "preview-kubernetes-lesson-11.html"),
    ("12", "preview-kubernetes-lesson-12.html"),
    ("13", "preview-kubernetes-lesson-13.html"),
    ("14", "preview-kubernetes-lesson-14.html"),
    ("15", "preview-kubernetes-lesson-15.html"),
    ("16", "preview-kubernetes-lesson-16.html"),
    ("17", "preview-kubernetes-lesson-17.html"),
    ("18", "preview-kubernetes-lesson-18.html"),
]


def build_strip(lesson_num: str) -> str:
    """Build a strip <ol> with 45 dots; active at the right index."""
    active_idx = _strip_index_for(lesson_num)
    parts = []
    for i in range(TOTAL_LESSONS_IN_CURRICULUM):
        cls = "ktown-strip-pin"
        if i == 0:
            cls += " ktown-strip-anchor"
        if i == active_idx:
            cls += " active"
        parts.append(f'    <li class="{cls}"></li>')
    return "\n".join(parts) + "\n  "


STRIP_BLOCK_RE = re.compile(
    r'(<ol class="ktown-strip"[^>]*>)(.*?)(</ol>)',
    re.DOTALL,
)
# Updates "lesson|Lesson N of M" → "of 45" anywhere in the file
OF_N_RE = re.compile(r'((?:[Ll])esson\s+\d+(?:\.\d+)?\s+of\s+)(\d+)')


def normalise(content: str, lesson_num: str) -> str:
    # 1. Replace strip <ol> body
    new_strip = build_strip(lesson_num)

    def replace_strip(m: re.Match) -> str:
        return m.group(1) + "\n" + new_strip + m.group(3)

    content, n = STRIP_BLOCK_RE.subn(replace_strip, content, count=1)
    if n != 1:
        raise RuntimeError("strip <ol> not found")

    # 2. Update "of N" → "of 45" wherever it appears
    def replace_of(m: re.Match) -> str:
        return f"{m.group(1)}{TOTAL_LESSONS_IN_CURRICULUM}"

    content = OF_N_RE.sub(replace_of, content)
    return content


def main() -> None:
    for num, fname in LESSON_FILES:
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            print(f"  {fname}: missing, skipping")
            continue
        content = open(path).read()
        try:
            updated = normalise(content, num)
        except RuntimeError as e:
            print(f"  {fname}: {e}, skipping")
            continue
        open(path, "w").write(updated)
        print(f"  L{num}: strip rebuilt to 45 dots, 'of 45' applied")


if __name__ == "__main__":
    main()
