#!/usr/bin/env python3
"""Patch legacy hand-edited K-COM lesson HTMLs: wrap top-level localStorage
calls in safeStorageGet/safeStorageSet so a SecurityError on file:// origins
(Safari) does not halt the rest of the script — including the animation code
that lives in the same <script> tag.
"""
import os
import re
import sys

ROOT = "/Users/skudarav/Projects/suvisguru-tech"

# Lessons L01-L18 + L7-5 are hand-authored (no spec under scripts/lessons/).
# L19-L44 + K-VAN + K-EKS get the fix via the generator's SCRIPT_BLOCK regen.
TARGETS = [f"preview-kubernetes-lesson-{i:02d}.html" for i in range(1, 19)]
TARGETS.append("preview-kubernetes-lesson-7-5.html")

SAFE_HELPERS = """
  function safeStorageGet(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function safeStorageSet(key, val) { try { localStorage.setItem(key, val); } catch (e) {} }

"""


def patch(path):
    txt = open(path).read()
    if "safeStorageGet" in txt:
        return False, "already patched"
    if "localStorage.getItem('lesson-theme')" not in txt:
        return False, "no localStorage usage found"

    # 1. Inject the safe helpers right after the first <script> tag at end of body.
    new_txt = re.sub(
        r"(<script>\n)(\s*//\s*theme toggle\n)?",
        r"\1" + SAFE_HELPERS,
        txt,
        count=1,
    )

    # 2. Replace the unsafe getItem/setItem calls.
    new_txt = new_txt.replace(
        "localStorage.getItem('lesson-theme')",
        "safeStorageGet('lesson-theme')",
    )
    new_txt = new_txt.replace(
        "localStorage.setItem('lesson-theme', next)",
        "safeStorageSet('lesson-theme', next)",
    )

    if new_txt == txt:
        return False, "no change made"
    open(path, "w").write(new_txt)
    return True, "patched"


def main():
    patched = 0
    for fname in TARGETS:
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            print(f"  SKIP {fname} (missing)")
            continue
        ok, msg = patch(path)
        flag = "✓" if ok else "·"
        print(f"  {flag} {fname}: {msg}")
        if ok:
            patched += 1
    print(f"\n{patched}/{len(TARGETS)} files patched.")


if __name__ == "__main__":
    main()
