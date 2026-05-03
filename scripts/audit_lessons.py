#!/usr/bin/env python3
"""K-COM cross-lesson audit.

Checks every preview-kubernetes-lesson-NN.html for structural and
content consistency. Reports issues grouped by category. Designed to
be re-run after each fix sweep.

Categories:
  STRUCTURAL  HTML tag balance, required sections present
  KTOWN       24 pins present, active pin matches district, strip dots,
              "lesson N of M" label
  ANIMATION   Section 6 present (L18-L44), anim IDs match SVG and JS,
              packet motion targets within viewBox
  VOCAB       Vocabulary-canon violations (lowercase "pod", "the loop"
              as a standalone term, etc.)
  REFS        Element IDs referenced from JS exist in the SVG
  FOOTER      "Lesson N of M" matches expected count

Exits 0 if zero issues found; non-zero otherwise.
"""

import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LESSON_FILES = sorted(
    f for f in os.listdir(ROOT)
    if f.startswith("preview-kubernetes-lesson-") and f.endswith(".html") and "draft" not in f
)


# Map of lesson number -> expected active pin id (district)
EXPECTED_ACTIVE_PIN = {
    "01": "kt-pin01", "02": "kt-pin02", "03": "kt-pin03", "04": "kt-pin04",
    "05": "kt-pin05", "06": "kt-pin06", "07": "kt-pin07", "7-5": "kt-pin7-5",
    "08": "kt-pin08", "09": "kt-pin09", "10": "kt-pin10", "11": "kt-pin11",
    "12": "kt-pin12", "13": "kt-pin13", "14": "kt-pin14", "15": "kt-pin15",
    "16": "kt-pin16", "17": "kt-pin17",
    "18": "kt-pin09", "19": "kt-pin09",  # Customs Warehouse
    "20": "kt-pin14", "21": "kt-pin14",  # Permit Office
    "22": "kt-pin16", "23": "kt-pin16",  # Dispatch Office
    "24": "kt-pin17", "25": "kt-pin17", "26": "kt-pin17",  # Switchboard
    "27": "kt-pin27", "28": "kt-pin27", "29": "kt-pin27",  # Watchtower
    "30": "kt-pin11",  # Bank Vault Quarter
    "31": "kt-pin27",  # Watchtower
    "32": "kt-pin32", "33": "kt-pin32",  # Observatory
    "34": "kt-pin34", "35": "kt-pin34",  # Power Station
    "36": "kt-pin36", "37": "kt-pin36",  # Print Shop
    "38": "kt-pin06", "39": "kt-pin06",  # Public Library
    "40": "kt-pin36",  # Print Shop
    "41": "kt-pin14",  # Permit Office
    "42": "kt-pin42",  # Workshop
    "43": "kt-pin17",  # Switchboard
    "44": "kt-pin44",  # Detective's Office
}


def lesson_num(filename: str) -> str:
    m = re.match(r"preview-kubernetes-lesson-(.+)\.html", filename)
    return m.group(1) if m else ""


issues = defaultdict(list)


def report(category: str, lesson: str, msg: str):
    issues[category].append(f"L{lesson}: {msg}")


# --- Per-lesson checks ---

for filename in LESSON_FILES:
    num = lesson_num(filename)
    path = os.path.join(ROOT, filename)
    content = open(path).read()

    # --- STRUCTURAL: tag balance ---
    for tag in ("section", "div", "main"):
        opens = len(re.findall(f"<{tag}[\\s>]", content))
        closes = content.count(f"</{tag}>")
        if opens != closes:
            report("STRUCTURAL", num, f"<{tag}> mismatch: {opens} open vs {closes} close")

    # --- KTOWN: 24 pins, expected active pin ---
    pin_ids = re.findall(r'id="(kt-pin[0-9-]+)"', content)
    if len(pin_ids) != 24:
        report("KTOWN", num, f"expected 24 K-Town pins, found {len(pin_ids)}")
    EXPECTED_DOTS = 45  # L01-L17 + L7.5 + L18-L44

    active_pins = re.findall(r'<g class="pin[^"]*active[^"]*" id="(kt-pin[0-9-]+)"', content)
    expected = EXPECTED_ACTIVE_PIN.get(num)
    if expected:
        if not active_pins:
            report("KTOWN", num, f"no active pin found (expected {expected})")
        elif active_pins[0] != expected:
            report("KTOWN", num, f"active pin = {active_pins[0]}, expected {expected}")

    # Strip dots
    strip_pins = re.findall(r'<li class="ktown-strip-pin[^"]*"', content)
    if len(strip_pins) != EXPECTED_DOTS:
        report("KTOWN", num, f"expected {EXPECTED_DOTS} strip dots, found {len(strip_pins)}")

    # --- FOOTER: "lesson N of M" consistency ---
    of_matches = re.findall(r'(?:[Ll])esson\s+(\d+(?:\.\d+)?)\s+of\s+(\d+)', content)
    for n_str, m_str in of_matches:
        if int(m_str) != 45:
            report("FOOTER", num, f'"lesson {n_str} of {m_str}" — expected of 45')

    # --- ANIMATION: should be present for L18-L44 ---
    has_anim_svg = 'id="lesson-anim"' in content
    has_anim_pkg = 'id="anim-pkg"' in content
    has_anim_btn = 'class="anim-btn' in content
    has_anim_readout = 'id="anim-readout"' in content
    expects_anim = num.isdigit() and 18 <= int(num) <= 44
    if expects_anim:
        if not has_anim_svg:
            report("ANIMATION", num, "missing #lesson-anim SVG")
        if not has_anim_pkg:
            report("ANIMATION", num, "missing #anim-pkg element")
        if not has_anim_btn:
            report("ANIMATION", num, "missing .anim-btn buttons")
        if not has_anim_readout:
            report("ANIMATION", num, "missing #anim-readout div")

    # --- ANIMATION: packet move targets within viewBox ---
    if has_anim_svg:
        vb = re.search(r'<svg viewBox="(\d+) (\d+) (\d+) (\d+)"[^>]*id="lesson-anim"', content)
        if vb:
            vbw, vbh = int(vb.group(3)), int(vb.group(4))
            # Look for "move_to":[x,y] in the JSON SCENES blob
            for x_str, y_str in re.findall(r'"move_to":\s*\[(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\]', content):
                x, y = float(x_str), float(y_str)
                if x < 0 or x > vbw or y < 0 or y > vbh:
                    report("ANIMATION", num, f"move_to ({x},{y}) outside viewBox {vbw}x{vbh}")

    # --- VOCAB: lowercase "pod" referring to the K8s object ---
    # Allow "Pod" (capitalized), allow lowercase in code/href/url contexts
    # Strip code blocks first
    content_no_code = re.sub(r'<code>.*?</code>', '', content, flags=re.DOTALL)
    content_no_pre = re.sub(r'<pre[^>]*>.*?</pre>', '', content_no_code, flags=re.DOTALL)
    # Look for " pod " or "pod " or " pods " (with surrounding whitespace) lowercase referring to K8s
    # Common false positives: "podcast", "tripod", "iPod" — check for word boundaries with these excluded
    bad_pod = re.findall(r'(?<!web)(?<!\w)pod(s)?(?=\s+(?:get|give|spec|YAML|create|run|deploy|fail|crash|restart|schedul|terminat|kill|placement|name|labels|state|annotation|resources|selector|tolerat|taint|spread|prior|dispatch|with|for|using|exec|template))', content_no_pre)
    if bad_pod:
        # Count occurrences for top-level pattern only
        bad_count = len(bad_pod)
        if bad_count > 0:
            report("VOCAB", num, f"lowercase 'pod' in K8s context ({bad_count} occurrence(s))")

    # --- REFS: animation element IDs referenced by setText/setAttr should exist ---
    # Pull ids from JS scenes data
    scene_blob = re.search(r'const SCENES = (\[.*?\]);', content)
    if scene_blob:
        # Extract every "set_text":[["id","text"], ...] target
        referenced = set()
        for m in re.finditer(r'"set_text":\s*\[(.*?)\]\s*,\s*"set_attr"', scene_blob.group(1), flags=re.DOTALL):
            inner = m.group(1)
            for elt_id in re.findall(r'\[\s*"([^"]+)"', inner):
                referenced.add(elt_id)
        # Also from set_attr triples
        for m in re.finditer(r'"set_attr":\s*\[(.*?)\]\s*\}', scene_blob.group(1), flags=re.DOTALL):
            inner = m.group(1)
            for elt_id in re.findall(r'\[\s*"([^"]+)"', inner):
                referenced.add(elt_id)
        # Check existence in the page
        for elt_id in referenced:
            if elt_id == "anim-mode-label":
                continue  # provided by generator
            if f'id="{elt_id}"' not in content:
                report("REFS", num, f"animation references missing element id={elt_id!r}")


# --- Cross-lesson checks ---

# Footer should say "of N" with N consistent across the new lessons
of_counts = Counter()
for filename in LESSON_FILES:
    num = lesson_num(filename)
    content = open(os.path.join(ROOT, filename)).read()
    for n_str, m_str in re.findall(r'lesson\s+\d+\s+of\s+(\d+)', content, flags=re.IGNORECASE):
        of_counts[m_str] += 1

# (Informational, not a hard check)


# --- Report ---

print(f"Audited {len(LESSON_FILES)} lesson files.")
total = sum(len(v) for v in issues.values())
if total == 0:
    print("✓ No issues found.")
    sys.exit(0)

print(f"\n{total} issue(s) across {len(issues)} categor(ies):\n")
for cat in sorted(issues):
    print(f"== {cat} ({len(issues[cat])}) ==")
    for line in issues[cat][:30]:
        print(f"  {line}")
    if len(issues[cat]) > 30:
        print(f"  … and {len(issues[cat]) - 30} more")
    print()

print(f"Footer 'of N' counts across all files: {dict(of_counts)}")
sys.exit(1)
