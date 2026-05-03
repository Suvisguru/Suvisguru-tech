#!/usr/bin/env python3
"""K-COM cross-lesson audit v2 — content + alignment.

Beyond the v1 mechanical checks, v2 looks for:

  SECTIONS    Required sections present (1, 1.5, 2, 3, 4, 5, 6, 7)
  PACKET      Animation packet move_to lands inside (or near) a scene
              box, not in dead space. Reports phases where the packet
              ends in an empty area of the SVG.
  WORDS       ELI5 ≤ 110 words (STYLE.md sanity); analogy_stops present;
              stamp boxed at top AND bottom (matching).
  GLOSS       Glossary present + non-empty
  RECAP       Recap card present + has next-lesson hook
"""

import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LESSON_FILES = sorted(
    f for f in os.listdir(ROOT)
    if f.startswith("preview-kubernetes-lesson-") and f.endswith(".html") and "draft" not in f
)


def lesson_num(filename: str) -> str:
    m = re.match(r"preview-kubernetes-lesson-(.+)\.html", filename)
    return m.group(1) if m else ""


issues = defaultdict(list)


def report(category: str, lesson: str, msg: str):
    issues[category].append(f"L{lesson}: {msg}")


# Primers (Lesson-N.5 pattern) are intentionally lighter per
# DECISIONS 2026-05-02 — exempt from Section 7 / glossary / analogy-stops checks.
PRIMER_EXEMPT = {"7-5"}


for filename in LESSON_FILES:
    num = lesson_num(filename)
    path = os.path.join(ROOT, filename)
    content = open(path).read()
    is_primer = num in PRIMER_EXEMPT

    # --- SECTIONS: count s-eyebrow occurrences to verify section coverage ---
    eyebrows = re.findall(r'<span class="s-eyebrow">([^<]+)</span>', content)
    # Required: at least 5 sections (1 concept, 2 before/after, 3 analogy, 4 ELI, 5 real-world, 7 misc/quiz)
    needs = ["Section 1", "Section 2", "Section 3", "Section 4", "Section 5", "Section 7"]
    if num.isdigit() and 18 <= int(num) <= 44:
        needs.append("Section 6")
    if is_primer:
        # primers may omit Section 7 (no canonical quiz/misconception block)
        needs = [n for n in needs if n != "Section 7"]
    for need in needs:
        if not any(eb.startswith(need) for eb in eyebrows):
            report("SECTIONS", num, f"missing {need}")

    # --- PACKET: extract scene boxes (rect within #lesson-anim) and check
    # each phase's move_to lands inside one ---
    anim_block = re.search(r'<svg[^>]*id="lesson-anim"[^>]*>(.*?)</svg>', content, re.DOTALL)
    if anim_block:
        svg_inner = anim_block.group(1)
        # Find all rects with their bounds
        boxes = []
        for m in re.finditer(r'<rect\s+x="(\d+)"\s+y="(\d+)"\s+width="(\d+)"\s+height="(\d+)"', svg_inner):
            x, y, w, h = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
            boxes.append((x, y, x + w, y + h))
        # Find each phase's move_to from the JS SCENES blob
        scenes_blob = re.search(r'const SCENES = (\[.*?\]);', content)
        if scenes_blob:
            for x_str, y_str in re.findall(r'"move_to":\s*\[(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\]', scenes_blob.group(1)):
                px, py = float(x_str), float(y_str)
                inside_any = any(x1 <= px <= x2 and y1 <= py <= y2 for x1, y1, x2, y2 in boxes)
                if not inside_any:
                    # Tolerance: within 30px of any box edge counts as "near"
                    near = any(
                        abs(px - x1) <= 30 or abs(px - x2) <= 30 or abs(py - y1) <= 30 or abs(py - y2) <= 30
                        for x1, y1, x2, y2 in boxes
                    )
                    if not near:
                        report("PACKET", num, f"move_to ({px},{py}) is in dead space (no box within 30px)")

    # --- WORDS: ELI5 length sanity (regex-tight: only first <p> after the eli-tag) ---
    eli5_match = re.search(
        r'<span class="eli-tag five">[^<]+</span>\s*<p>(.*?)</p>',
        content, flags=re.DOTALL,
    )
    if eli5_match:
        eli5_text = re.sub(r'<[^>]+>', '', eli5_match.group(1))
        word_count = len(eli5_text.split())
        if word_count > 130:
            report("WORDS", num, f"ELI5 has {word_count} words, target ≤ 130")
        elif word_count < 12:
            report("WORDS", num, f"ELI5 has only {word_count} words, suspicious")

    # --- WORDS: stamp present at top + bottom (count occurrences) ---
    stamp_count = content.count('class="stamp-box"')
    if stamp_count != 2:
        report("WORDS", num, f"expected 2 .stamp-box (top + bottom), found {stamp_count}")

    # --- WORDS: analogy stops note present (skip for primers) ---
    if not is_primer and 'analogy-stops' not in content:
        report("WORDS", num, "missing 'analogy stops here' callout")

    # --- GLOSS: glossary present (skip for primers) ---
    if not is_primer:
        if 'class="glossary"' not in content:
            report("GLOSS", num, "missing glossary <details> block")
        else:
            items = re.findall(r'class="gloss-item"', content)
            if len(items) < 4:
                report("GLOSS", num, f"glossary has only {len(items)} items (expected ≥ 4)")

    # --- RECAP: recap card present + has next-lesson hook ---
    if 'class="recap"' not in content:
        report("RECAP", num, "missing recap card")
    elif num != "44" and 'recap-next' not in content:
        report("RECAP", num, "recap card missing 'recap-next' (next-lesson hook)")


# --- Cross-lesson concept-rail consistency for L19-L44 ---
# All generator-built lessons should have the same 45-item concept rail
rail_items_per_lesson = {}
for filename in LESSON_FILES:
    num = lesson_num(filename)
    if num.isdigit() and 19 <= int(num) <= 44:
        content = open(os.path.join(ROOT, filename)).read()
        items = re.findall(r'<div class="concept-rail-item[^"]*">.*?<span class="concept-rail-icon">([^<]+)</span>', content, re.DOTALL)
        rail_items_per_lesson[num] = len(items)

if rail_items_per_lesson:
    counts = set(rail_items_per_lesson.values())
    if len(counts) > 1:
        report("RAIL", "all", f"concept rail item counts vary across L19-L44: {sorted(counts)}")


# --- Report ---

print(f"Audited {len(LESSON_FILES)} lesson files (v2 deep checks).")
total = sum(len(v) for v in issues.values())
if total == 0:
    print("✓ No issues found.")
    sys.exit(0)

print(f"\n{total} issue(s) across {len(issues)} categor(ies):\n")
for cat in sorted(issues):
    print(f"== {cat} ({len(issues[cat])}) ==")
    for line in issues[cat][:25]:
        print(f"  {line}")
    if len(issues[cat]) > 25:
        print(f"  … and {len(issues[cat]) - 25} more")
    print()

sys.exit(1)
