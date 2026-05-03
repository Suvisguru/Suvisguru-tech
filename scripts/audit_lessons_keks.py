#!/usr/bin/env python3
"""K-EKS cross-lesson audit — mechanical + content (mirror of K-VAN audit)."""

import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LESSON_FILES = sorted(
    f for f in os.listdir(ROOT)
    if f.startswith("preview-kubernetes-eks-lesson-") and f.endswith(".html")
)

EXPECTED_ACTIVE_FLOOR = {f"{i:02d}": f"ks-floor{i:02d}" for i in range(1, 12)}
EXPECTED_DOTS = 11
TOTAL_LESSONS = 11

issues = defaultdict(list)


def report(category, lesson, msg):
    issues[category].append(f"E{int(lesson)}: {msg}")


for filename in LESSON_FILES:
    m = re.match(r"preview-kubernetes-eks-lesson-(\d+)\.html", filename)
    if not m:
        continue
    num = m.group(1)
    content = open(os.path.join(ROOT, filename)).read()

    for tag in ("section", "div", "main"):
        opens = len(re.findall(f"<{tag}[\\s>]", content))
        closes = content.count(f"</{tag}>")
        if opens != closes:
            report("STRUCTURAL", num, f"<{tag}> mismatch: {opens}/{closes}")

    floor_ids = re.findall(r'id="(ks-floor\d+)"', content)
    if len(floor_ids) != 11:
        report("KSKYLINE", num, f"expected 11 K-Skyline floors, found {len(floor_ids)}")
    active = re.findall(r'<g class="pin[^"]*active[^"]*" id="(ks-floor\d+)"', content)
    expected = EXPECTED_ACTIVE_FLOOR.get(num)
    if expected and (not active or active[0] != expected):
        report("KSKYLINE", num, f"active floor = {active[0] if active else 'NONE'}, expected {expected}")

    strip_pins = re.findall(r'<li class="ktown-strip-pin[^"]*"', content)
    if len(strip_pins) != EXPECTED_DOTS:
        report("KSKYLINE", num, f"expected {EXPECTED_DOTS} strip dots, found {len(strip_pins)}")

    of_matches = re.findall(r'E\d+\s+of\s+(\d+)', content)
    for m_str in of_matches:
        if int(m_str) != TOTAL_LESSONS:
            report("FOOTER", num, f'"E… of {m_str}" — expected of {TOTAL_LESSONS}')

    if 'id="lesson-anim"' not in content:
        report("ANIMATION", num, "missing #lesson-anim SVG")
    if 'id="anim-pkg"' not in content:
        report("ANIMATION", num, "missing #anim-pkg")
    if 'class="anim-btn' not in content:
        report("ANIMATION", num, "missing .anim-btn buttons")

    vb = re.search(r'<svg viewBox="(\d+) (\d+) (\d+) (\d+)"[^>]*id="lesson-anim"', content)
    if vb:
        vbw, vbh = int(vb.group(3)), int(vb.group(4))
        for x_str, y_str in re.findall(r'"move_to":\s*\[(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\]', content):
            x, y = float(x_str), float(y_str)
            if x < 0 or x > vbw or y < 0 or y > vbh:
                report("ANIMATION", num, f"move_to ({x},{y}) outside viewBox {vbw}x{vbh}")

    eyebrows = re.findall(r'<span class="s-eyebrow">([^<]+)</span>', content)
    for need in ["Section 1", "Section 2", "Section 3", "Section 4", "Section 5", "Section 6", "Section 7"]:
        if not any(eb.startswith(need) for eb in eyebrows):
            report("SECTIONS", num, f"missing {need}")

    stamps = content.count('class="stamp-box"')
    if stamps != 2:
        report("WORDS", num, f"expected 2 .stamp-box, found {stamps}")

    if 'analogy-stops' not in content:
        report("WORDS", num, "missing analogy-stops callout")

    if 'class="glossary"' not in content:
        report("GLOSS", num, "missing glossary")
    else:
        items = re.findall(r'class="gloss-item"', content)
        if len(items) < 4:
            report("GLOSS", num, f"glossary has only {len(items)} items")

    if 'class="recap"' not in content:
        report("RECAP", num, "missing recap card")

    scene_blob = re.search(r'const SCENES = (\[.*?\]);', content)
    if scene_blob:
        referenced = set()
        for inner in re.findall(r'"set_text":\s*\[(.*?)\]\s*,\s*"set_attr"', scene_blob.group(1), flags=re.DOTALL):
            for elt_id in re.findall(r'\[\s*"([^"]+)"', inner):
                referenced.add(elt_id)
        for inner in re.findall(r'"set_attr":\s*\[(.*?)\]\s*\}', scene_blob.group(1), flags=re.DOTALL):
            for elt_id in re.findall(r'\[\s*"([^"]+)"', inner):
                referenced.add(elt_id)
        for elt_id in referenced:
            if elt_id == "anim-mode-label":
                continue
            if f'id="{elt_id}"' not in content:
                report("REFS", num, f"animation references missing id={elt_id!r}")


print(f"Audited {len(LESSON_FILES)} K-EKS lesson files.")
total = sum(len(v) for v in issues.values())
if total == 0:
    print("✓ No issues found.")
    sys.exit(0)

print(f"\n{total} issue(s):\n")
for cat in sorted(issues):
    print(f"== {cat} ({len(issues[cat])}) ==")
    for line in issues[cat][:25]:
        print(f"  {line}")
    print()
sys.exit(1)
