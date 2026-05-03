"""Shared audit core for K-VAN, K-EKS, K-AKS, K-GKE, K-OCP courses.

Each per-course audit (audit_lessons_kvan.py etc.) becomes a thin caller
declaring its CourseAuditConfig + invoking audit_course().

K-COM is NOT covered here — it has separate audit_lessons.py + audit_lessons_v2.py
with K-COM-specific checks (24 K-Town pins, 45 strip dots, K-COM section
patterns, L7-5 primer exception).
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class CourseAuditConfig:
    course_code: str          # "K-OCP", "K-GKE", "K-AKS", "K-EKS", "K-VAN"
    course_letter: str        # "O", "G", "A", "E", "V"
    html_filename_prefix: str # "preview-kubernetes-ocp-lesson-"
    pin_prefix: str           # "ko-bay" / "kg-plot" / "kc-wing" / "ks-floor" / "kf-site"
    universe_label: str       # "K-Foundry" / "K-Garden" / "K-Campus" / "K-Skyline" / "K-Frontier"
    total_lessons: int        # 13 / 10 / 11 / 11 / 11


def audit_course(config: CourseAuditConfig) -> int:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    lesson_files = sorted(
        f for f in os.listdir(root)
        if f.startswith(config.html_filename_prefix) and f.endswith(".html")
    )

    expected_active = {
        f"{i:02d}": f"{config.pin_prefix}{i:02d}"
        for i in range(1, config.total_lessons + 1)
    }
    issues = defaultdict(list)

    def report(category, lesson, msg):
        issues[category].append(f"{config.course_letter}{int(lesson)}: {msg}")

    pin_id_re = re.compile(rf'id="({config.pin_prefix}\d+)"')
    active_pin_re = re.compile(
        rf'<g class="pin[^"]*active[^"]*" id="({config.pin_prefix}\d+)"'
    )
    of_re = re.compile(rf'{config.course_letter}\d+\s+of\s+(\d+)')

    for filename in lesson_files:
        m = re.match(rf"{re.escape(config.html_filename_prefix)}(\d+)\.html", filename)
        if not m:
            continue
        num = m.group(1)
        content = open(os.path.join(root, filename)).read()

        # Structural balance
        for tag in ("section", "div", "main"):
            opens = len(re.findall(f"<{tag}[\\s>]", content))
            closes = content.count(f"</{tag}>")
            if opens != closes:
                report("STRUCTURAL", num, f"<{tag}> mismatch: {opens}/{closes}")

        # Atlas pins
        pin_ids = pin_id_re.findall(content)
        if len(pin_ids) != config.total_lessons:
            report(
                config.universe_label.upper().replace("-", ""),
                num,
                f"expected {config.total_lessons} {config.universe_label} pins, found {len(pin_ids)}",
            )
        active = active_pin_re.findall(content)
        expected = expected_active.get(num)
        if expected and (not active or active[0] != expected):
            report(
                config.universe_label.upper().replace("-", ""),
                num,
                f"active pin = {active[0] if active else 'NONE'}, expected {expected}",
            )

        # Strip dots
        strip_pins = re.findall(r'<li class="ktown-strip-pin[^"]*"', content)
        if len(strip_pins) != config.total_lessons:
            report(
                config.universe_label.upper().replace("-", ""),
                num,
                f"expected {config.total_lessons} strip dots, found {len(strip_pins)}",
            )

        # Footer "X of N"
        for m_str in of_re.findall(content):
            if int(m_str) != config.total_lessons:
                report("FOOTER", num, f'"{config.course_letter}… of {m_str}" — expected of {config.total_lessons}')

        # Animation markup
        if 'id="lesson-anim"' not in content:
            report("ANIMATION", num, "missing #lesson-anim SVG")
        if 'id="anim-pkg"' not in content:
            report("ANIMATION", num, "missing #anim-pkg")
        if 'class="anim-btn' not in content:
            report("ANIMATION", num, "missing .anim-btn buttons")

        # Animation viewBox bounds
        vb = re.search(r'<svg viewBox="(\d+) (\d+) (\d+) (\d+)"[^>]*id="lesson-anim"', content)
        if vb:
            vbw, vbh = int(vb.group(3)), int(vb.group(4))
            for x_str, y_str in re.findall(r'"move_to":\s*\[(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\]', content):
                x, y = float(x_str), float(y_str)
                if x < 0 or x > vbw or y < 0 or y > vbh:
                    report("ANIMATION", num, f"move_to ({x},{y}) outside viewBox {vbw}x{vbh}")

        # Section eyebrows
        eyebrows = re.findall(r'<span class="s-eyebrow">([^<]+)</span>', content)
        for need in [f"Section {i}" for i in range(1, 8)]:
            if not any(eb.startswith(need) for eb in eyebrows):
                report("SECTIONS", num, f"missing {need}")

        # Stamp boxes (top + bottom)
        stamps = content.count('class="stamp-box"')
        if stamps != 2:
            report("WORDS", num, f"expected 2 .stamp-box, found {stamps}")

        # Analogy stops + glossary + recap
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

        # Animation references — every set_text/set_attr id must exist
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

    print(f"Audited {len(lesson_files)} {config.course_code} lesson files.")
    total = sum(len(v) for v in issues.values())
    if total == 0:
        print("✓ No issues found.")
        return 0

    print(f"\n{total} issue(s):\n")
    for cat in sorted(issues):
        print(f"== {cat} ({len(issues[cat])}) ==")
        for line in issues[cat][:25]:
            print(f"  {line}")
        print()
    return 1


def run_audit_main(config: CourseAuditConfig) -> None:
    sys.exit(audit_course(config))
