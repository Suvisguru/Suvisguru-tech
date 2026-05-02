#!/usr/bin/env python3
"""Inject Section 6 animation + JS into L18.

L18 is hand-authored (predates the lesson generator). This one-shot
script slots the animation block between Section 5 (real-world) and
Section 7 (misconceptions), and appends the animation JS to the
existing <script> block.

Idempotent — running twice is a no-op.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts/lessons"))

from k8s_lesson_generator import _render_animation
from animations import ANIMATIONS


def main() -> None:
    path = os.path.join(ROOT, "preview-kubernetes-lesson-18.html")
    content = open(path).read()
    if 'id="lesson-anim"' in content:
        print("L18 already has animation; skipping.")
        return

    section_html, script_js = _render_animation(ANIMATIONS["18"])
    if not section_html:
        sys.exit("L18 animation spec missing")

    # Anchor: the SECTION 7 comment in L18 is exactly:
    #   <!-- ============================== SECTION 7 — MISCONCEPTIONS + FLASHCARDS + QUIZ ============================== -->
    section7_anchor = "  <!-- ============================== SECTION 7"
    if section7_anchor not in content:
        sys.exit("section 7 anchor not found in L18")
    content = content.replace(
        section7_anchor,
        section_html + "\n\n" + section7_anchor,
        1,
    )

    # Append the animation JS to the existing <script> block.
    # Find the last </script> before </body> and insert the JS just before it.
    body_close = content.rfind("</body>")
    if body_close == -1:
        sys.exit("</body> not found")
    script_close = content.rfind("</script>", 0, body_close)
    if script_close == -1:
        sys.exit("</script> not found")
    content = content[:script_close] + "\n" + script_js + "\n" + content[script_close:]

    open(path, "w").write(content)
    print("L18: animation inserted")


if __name__ == "__main__":
    main()
