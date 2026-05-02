#!/usr/bin/env python3
"""K-Town expansion — add 6 new district pins for L18-L44.

The K-Town map currently has 18 pins (L01-L17 + L7.5 primer). This
script adds the 6 new district pins introduced for the L18-L44
batch, propagates them to every older lesson HTML, and updates the
mobile dot-strip + label.

New districts:
  27 Watchtower            (740, 105)  security cluster-side
  32 Observatory           (230, 105)  observability
  34 Power Station         (230, 295)  scale & resilience
  36 Print Shop            (410, 295)  delivery
  42 Workshop              (700, 305)  operators
  44 Detective's Office    (770, 245)  troubleshooting

These positions are already encoded in the lesson generator
(scripts/k8s_lesson_generator.py KTOWN_PINS) — this script just
propagates them backward into the older lessons + the canonical
primitive.

Idempotent — running twice is a no-op.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_pin_inline(num_id: str, num_label: str, x: int, y: int, label: str, sub: str | None = None) -> str:
    """Single-line inline pin, matching the format used in lesson HTML files."""
    sub_html = ""
    if sub:
        sub_html = f'<text class="pin-sub" y="38" text-anchor="middle" font-family="sans-serif" font-size="8" font-style="italic" fill="#9D9389">{sub}</text>'
    return (
        f'    <g class="pin" id="kt-pin{num_id}" transform="translate({x},{y})">'
        f'<circle class="pin-halo" r="18" fill="#D97757" opacity="0"/>'
        f'<circle class="pin-circle" r="10" fill="#9D9389" stroke="#FBF7F0" stroke-width="2"/>'
        f'<text class="pin-num" y="3" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="9" font-weight="700" fill="#FBF7F0">{num_label}</text>'
        f'<text class="pin-label" y="26" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#6B6058">{label}</text>'
        f'{sub_html}'
        f'</g>'
    )


NEW_PINS = [
    ("27", "27", 740, 105, "Watchtower", "security"),
    ("32", "32", 230, 105, "Observatory", "observability"),
    ("34", "34", 230, 295, "Power Station", "scale & resilience"),
    ("36", "36", 410, 295, "Print Shop", "delivery"),
    ("42", "42", 700, 305, "Workshop", "operators"),
    ("44", "44", 770, 245, "Detective's Office", "troubleshooting"),
]

NEW_PIN_BLOCKS = [make_pin_inline(*p) for p in NEW_PINS]

# Anchor: insert after kt-pin17 (last pin in the existing 18-pin map).
# Use a regex because the active class varies per file.
PIN17_RE = re.compile(
    r'<g class="pin( active)?" id="kt-pin17" transform="translate\(530,290\)">'
    r'<circle class="pin-halo" r="18" fill="#D97757" opacity="0"/>'
    r'<circle class="pin-circle" r="10" fill="#9D9389" stroke="#FBF7F0" stroke-width="2"/>'
    r'<text class="pin-num" y="3" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="9" font-weight="700" fill="#FBF7F0">17</text>'
    r'<text class="pin-label" y="26" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#6B6058">Switchboard</text>'
    r'</g>'
)

# Update the "lesson N of M" suffix in the strip label.
STRIP_LABEL_RE = re.compile(r'(\Wlesson\s+\d+\s+of\s+)(\d+)(\W)')

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
    "preview-kubernetes-lesson-16.html",
    "preview-kubernetes-lesson-17.html",
    "preview-kubernetes-lesson-18.html",
]


def expand_inline(content: str, label: str) -> str | None:
    if 'id="kt-pin27"' in content:
        return None  # already applied

    matches = list(PIN17_RE.finditer(content))
    if not matches:
        sys.exit(f"[{label}] kt-pin17 anchor not found")
    if len(matches) != 1:
        sys.exit(f"[{label}] kt-pin17 matched {len(matches)} times — expected 1")
    m = matches[0]
    insert_text = "\n" + "\n".join(NEW_PIN_BLOCKS)
    content = content[:m.end()] + insert_text + content[m.end():]

    # Add 6 dots to the strip <ol>
    strip_close = re.compile(r'(<ol class="ktown-strip"[^>]*>.*?)(</ol>)', re.DOTALL)
    m = strip_close.search(content)
    if not m:
        sys.exit(f"[{label}] strip <ol> not found")
    inside, close = m.group(1), m.group(2)
    extra_dots = "    " + "\n    ".join(['<li class="ktown-strip-pin"></li>'] * 6) + "\n  "
    content = content.replace(inside + close, inside + extra_dots + close, 1)

    # Update "lesson N of M" suffix to "of 24" (24 = 18 existing + 6 new districts).
    # Only update if M < 24; preserves explicit larger counts if any.
    def replace_of(match: re.Match) -> str:
        existing = int(match.group(2))
        new = max(existing, 24)
        return f"{match.group(1)}{new}{match.group(3)}"

    content = STRIP_LABEL_RE.sub(replace_of, content)
    return content


def expand_primitive(content: str) -> str | None:
    if 'id="kt-pin27"' in content:
        return None

    # The primitive uses multi-line indented blocks. Find the kt-pin17
    # block and append the 6 new pins after it.
    pin17_pattern = re.compile(
        r'(    <g class="pin" id="kt-pin17" transform="translate\(530,290\)">\s*'
        r'<circle class="pin-halo".*?</g>)',
        re.DOTALL,
    )
    m = pin17_pattern.search(content)
    if not m:
        sys.exit("[primitive] kt-pin17 anchor not found")

    new_block = "\n\n".join(NEW_PIN_BLOCKS)
    return content[:m.end()] + "\n\n" + new_block + content[m.end():]


def main() -> None:
    primitive_path = os.path.join(ROOT, "library/primitives/kubernetes/k-town-map.svg")
    if os.path.exists(primitive_path):
        content = open(primitive_path).read()
        updated = expand_primitive(content)
        if updated is None:
            print("  primitive: already expanded, skipping")
        else:
            open(primitive_path, "w").write(updated)
            print("  primitive: 6 new pins added")
    else:
        print(f"  primitive missing: {primitive_path}")

    for fname in LESSON_FILES:
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            print(f"  {fname}: file missing, skipping")
            continue
        content = open(path).read()
        updated = expand_inline(content, fname)
        if updated is None:
            print(f"  {fname}: already expanded, skipping")
        else:
            open(path, "w").write(updated)
            print(f"  {fname}: pins + strip dots added")

    print("\nDone.")


if __name__ == "__main__":
    main()
