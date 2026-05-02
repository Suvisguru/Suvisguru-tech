#!/usr/bin/env python3
"""K-Town expansion — add L16 (Dispatch Office) and L17 (Switchboard) pins.

The K-Town map primitive currently has 16 pins (L01–L15 + L7.5 primer).
This script:
  1. Adds two new pin <g> elements to the canonical primitive at
     library/primitives/kubernetes/k-town-map.svg.
  2. Propagates the same two pins into the inline K-Town SVG copy in
     every one of the 16 existing lesson HTML files.
  3. Adds two new <li class="ktown-strip-pin"></li> entries to each
     lesson's mobile dot-strip <ol> so the strip grows from 16 → 18.

New pin coordinates (inside the existing 800×420 viewBox — no resize):
  L16 Dispatch Office  → (295, 255) — civic-adjacent slot between
                          L15 (170,255) and L14 (470,255).
  L17 Switchboard      → (530, 290) — commercial-east slot east of
                          L10 (350,290).

Both new pins ship as `class="pin"` (no `active`) in all existing
lessons. The L16 and L17 lessons themselves carry the `active` class
on their own pin and the corresponding strip dot.

Idempotent — running twice finds no remaining instances of the original
16-pin pattern and exits cleanly.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PIN16 = (
    '    <g class="pin" id="kt-pin16" transform="translate(295,255)">'
    '<circle class="pin-halo" r="18" fill="#D97757" opacity="0"/>'
    '<circle class="pin-circle" r="10" fill="#9D9389" stroke="#FBF7F0" stroke-width="2"/>'
    '<text class="pin-num" y="3" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="9" font-weight="700" fill="#FBF7F0">16</text>'
    '<text class="pin-label" y="26" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#6B6058">Dispatch Office</text>'
    '</g>'
)

PIN17 = (
    '    <g class="pin" id="kt-pin17" transform="translate(530,290)">'
    '<circle class="pin-halo" r="18" fill="#D97757" opacity="0"/>'
    '<circle class="pin-circle" r="10" fill="#9D9389" stroke="#FBF7F0" stroke-width="2"/>'
    '<text class="pin-num" y="3" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="9" font-weight="700" fill="#FBF7F0">17</text>'
    '<text class="pin-label" y="26" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#6B6058">Switchboard</text>'
    '</g>'
)

# Anchor: the kt-pin12 (Harbour) element followed by </svg>. Last pin in the existing inline SVG.
# Use a regex because L12 itself has class="pin active" on kt-pin12 while all other lessons have class="pin".
PIN12_RE = re.compile(
    r'<g class="pin( active)?" id="kt-pin12" transform="translate\(570,340\)">'
    r'<circle class="pin-halo" r="18" fill="#D97757" opacity="0"/>'
    r'<circle class="pin-circle" r="10" fill="#9D9389" stroke="#FBF7F0" stroke-width="2"/>'
    r'<text class="pin-num" y="3" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="9" font-weight="700" fill="#FBF7F0">12</text>'
    r'<text class="pin-label" y="26" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#6B6058">Harbour</text>'
    r'</g>'
)

LESSON_FILES = [
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


def expand_inline(content: str, label: str) -> str | None:
    """Add the 2 new pins after kt-pin12 in the K-Town map SVG, and
    add 2 new dots to the strip <ol>. Returns updated content or None
    if already-applied."""
    if 'id="kt-pin16"' in content or 'id="kt-pin17"' in content:
        return None  # already applied

    # 1. Insert new pins after kt-pin12 (the last existing pin in the SVG draw order).
    matches = list(PIN12_RE.finditer(content))
    if not matches:
        sys.exit(f"[{label}] kt-pin12 anchor not found")
    if len(matches) != 1:
        sys.exit(f"[{label}] kt-pin12 matched {len(matches)} times — expected 1")
    m = matches[0]
    content = content[:m.end()] + f'\n{PIN16}\n{PIN17}' + content[m.end():]

    # 2. Add 2 dots to the dot-strip: insert before </ol> of the <ol class="ktown-strip">.
    strip_close_pattern = re.compile(
        r'(<ol class="ktown-strip"[^>]*>.*?)(</ol>)',
        re.DOTALL,
    )
    m = strip_close_pattern.search(content)
    if not m:
        sys.exit(f"[{label}] strip <ol> not found")
    inside, close = m.group(1), m.group(2)
    new_inside = inside + '    <li class="ktown-strip-pin"></li>\n    <li class="ktown-strip-pin"></li>\n  '
    content = content.replace(inside + close, new_inside + close, 1)

    return content


def expand_primitive(content: str) -> str | None:
    """Same pin-add logic on the standalone primitive file. The
    primitive uses <symbol> for embedding, but the pin elements are
    direct children at the same level of indentation."""
    if 'id="kt-pin16"' in content or 'id="kt-pin17"' in content:
        return None

    if PIN12_FULL not in content:
        sys.exit("[primitive] kt-pin12 anchor not found")
    new_pin_block = f'{PIN12_FULL}\n\n{PIN16}\n\n{PIN17}'
    return content.replace(PIN12_FULL, new_pin_block, 1)


def update_primitive_header(content: str) -> str:
    """Update the slot-anchors comment table in the primitive's header
    to record the two new districts."""
    old = (
        "    15 Co-Living Quarter                   (170, 255)\n\n"
        "  Background features"
    )
    new = (
        "    15 Co-Living Quarter                   (170, 255)\n"
        "    16 K-Town Dispatch Office              (295, 255)\n"
        "    17 K-Town Switchboard                  (530, 290)\n\n"
        "  Background features"
    )
    if old not in content:
        return content  # already updated, no-op
    return content.replace(old, new, 1)


def main() -> None:
    # The primitive is hand-edited separately (different formatting — multi-line indented
    # vs the lessons' single-line inline format).
    print("  (Skip primitive — hand-edit due to formatting difference.)")

    # Update each lesson's inline copy + strip
    for fname in LESSON_FILES:
        path = os.path.join(ROOT, fname)
        content = open(path).read()
        new_content = expand_inline(content, fname)
        if new_content is None:
            print(f"  {fname}: already expanded, skipping")
        else:
            open(path, "w").write(new_content)
            print(f"  {fname}: pins + strip dots added")

    print("\nDone.")


if __name__ == "__main__":
    main()
