#!/usr/bin/env python3
"""Build a single-file combined view of all K-GKE modules.

Mirror of scripts/build_combined_course_kaks.py, targeting K-GKE (10 modules).
Output: preview-kubernetes-gke-course-all.html at the repo root.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LESSONS = [
    ("01", "preview-kubernetes-gke-lesson-01.html", "G1 · GKE Architecture and Modes"),
    ("02", "preview-kubernetes-gke-lesson-02.html", "G2 · Versioning and Release Channels"),
    ("03", "preview-kubernetes-gke-lesson-03.html", "G3 · GKE Networking"),
    ("04", "preview-kubernetes-gke-lesson-04.html", "G4 · Identity and Security"),
    ("05", "preview-kubernetes-gke-lesson-05.html", "G5 · GKE Storage"),
    ("06", "preview-kubernetes-gke-lesson-06.html", "G6 · Scaling and Cost"),
    ("07", "preview-kubernetes-gke-lesson-07.html", "G7 · GKE Observability"),
    ("08", "preview-kubernetes-gke-lesson-08.html", "G8 · Enterprise (Fleets) and AI/ML"),
    ("09", "preview-kubernetes-gke-lesson-09.html", "G9 · GKE Troubleshooting"),
    ("10", "preview-kubernetes-gke-lesson-10.html", "G10 · Capstone — Reference Garden"),
]


def extract_style_and_body(path):
    content = open(path).read()
    m = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    style = m.group(1) if m else ""
    body_start = content.index('</header>') + len('</header>')
    body_end = content.index('</footer>', body_start) + len('</footer>')
    body = content[body_start:body_end].strip()
    return style, body


def main():
    bundles = []
    for num, fname, title in LESSONS:
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            sys.exit(f"missing: {path}")
        style, body = extract_style_and_body(path)
        bundles.append({"num": num, "fname": fname, "title": title, "style": style, "body": body})

    out = [
        "<!DOCTYPE html>", '<html lang="en">', "<head>", '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"<title>K-GKE · The Whole Course (all {len(LESSONS)} modules)</title>", "<style>",
    ]
    for b in bundles:
        out.append(f"\n/* ============ {b['fname']} ============ */")
        out.append(b["style"])
    out.append("""
.course-topbar{position:sticky;top:0;background:rgba(251,247,240,.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);z-index:200;display:flex;align-items:center;gap:14px;padding:10px 20px;font-family:inherit}
[data-theme="dark"] .course-topbar{background:rgba(27,24,20,.95)}
.course-topbar .brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:14px;color:var(--ink);text-decoration:none}
.course-topbar .brand-mark{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,var(--warm),var(--gold));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:12px;box-shadow:var(--shadow-sm)}
.course-topbar .brand-meta{color:var(--ink-soft);font-weight:400;font-size:13px}
.course-topbar .lesson-jump{margin-left:auto;background:var(--bg-card);border:1px solid var(--line);color:var(--ink);padding:6px 10px;border-radius:var(--r-pill);font-size:13px;font-family:inherit;cursor:pointer;max-width:280px}
.course-topbar .theme-toggle{background:var(--bg-card);border:1px solid var(--line);color:var(--ink);padding:6px 12px;border-radius:var(--r-pill);font-size:12px;font-family:inherit;cursor:pointer}
.course-topbar .theme-toggle:hover{background:var(--accent-soft)}
.course-toc{max-width:820px;margin:36px auto 48px;padding:24px 32px;background:var(--bg-card);border:1px solid var(--line);border-radius:var(--r-card);box-shadow:var(--shadow-sm)}
.course-toc h2{font-size:24px;font-weight:700;margin:0 0 8px;color:var(--ink);letter-spacing:-0.2px}
.course-toc .toc-sub{color:var(--ink-soft);font-size:14.5px;line-height:1.6;margin:0 0 18px;font-style:italic}
.course-toc .toc-caveat{background:var(--gold-soft);border:1px dashed var(--gold);border-radius:var(--r-soft);padding:10px 14px;font-size:13.5px;color:var(--ink);line-height:1.55;margin:0 0 18px}
.course-toc ol{padding:0 0 0 24px;margin:0}
.course-toc li{margin:7px 0;line-height:1.5;font-size:14px}
.course-toc a{color:var(--accent);text-decoration:none;font-weight:600}
.course-toc a:hover{text-decoration:underline}
.course-sidebar{display:none;font-family:inherit}
.course-sidebar h3{font-size:11px;font-weight:700;color:var(--ink-faint);text-transform:uppercase;letter-spacing:1.5px;margin:0 0 10px}
.course-sidebar ol{list-style:none;padding:0;margin:0}
.course-sidebar a{display:flex;gap:8px;padding:5px 10px;color:var(--ink-soft);text-decoration:none;border-radius:var(--r-soft);border-left:2px solid transparent;font-size:12.5px;line-height:1.45;transition:background .15s var(--ease),color .15s var(--ease)}
.course-sidebar a:hover{color:var(--ink);background:var(--bg-soft)}
.course-sidebar a.current{color:var(--ink);font-weight:600;border-left-color:var(--warm);background:var(--bg-soft)}
.course-sidebar .num{color:var(--ink-faint);font-weight:700;min-width:32px;flex:0 0 auto}
@media (min-width:1240px){.course-sidebar{display:block;position:fixed;top:76px;left:max(16px,calc(50vw - 600px));width:180px;max-height:calc(100vh - 96px);overflow-y:auto;z-index:80;padding:14px 8px 14px 0}}
.course-section{border-top:6px solid var(--accent);margin-top:80px;scroll-margin-top:72px}
.course-section:first-of-type{border-top:0;margin-top:0}
.course-section .concept-rail{display:none!important}
.course-section header.topbar{display:none}
.course-section-banner{max-width:820px;margin:0 auto;padding:18px 24px 0;font-size:13px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:1.5px}
.course-section-banner span{color:var(--ink-faint);font-weight:400;letter-spacing:0;text-transform:none;font-size:13px;margin-left:8px}
.course-back-to-toc{position:fixed;bottom:24px;right:24px;background:var(--accent);color:#fff;padding:10px 18px;border-radius:var(--r-pill);font-size:13px;font-weight:600;text-decoration:none;box-shadow:var(--shadow-md);z-index:150;opacity:.92}
.course-back-to-toc:hover{opacity:1}
[data-theme="dark"] .course-back-to-toc{color:var(--bg)}
""")
    out.append("</style></head>")
    out.append('<body data-theme="light">')

    out.append('<header class="course-topbar">')
    out.append('  <a href="#course-toc" class="brand"><span class="brand-mark">SG</span><span>Suvis Guru</span><span class="brand-meta"> · K-GKE · the whole course</span></a>')
    out.append('  <select class="lesson-jump" id="lesson-jump" aria-label="Jump to module">')
    out.append('    <option value="">Jump to module…</option>')
    for b in bundles:
        out.append(f'    <option value="lesson-{b["num"]}">{b["title"]}</option>')
    out.append("  </select>")
    out.append('  <button class="theme-toggle" id="theme-toggle" type="button">🌙 Dark</button>')
    out.append("</header>")

    out.append('<aside class="course-sidebar" aria-label="K-GKE module navigation">')
    out.append(f'  <h3>The {len(LESSONS)} modules</h3>')
    out.append('  <ol>')
    for b in bundles:
        out.append(f'    <li><a href="#lesson-{b["num"]}"><span class="num">G{int(b["num"])}</span><span>{b["title"]}</span></a></li>')
    out.append('  </ol>')
    out.append('</aside>')

    out.append('<section class="course-toc" id="course-toc">')
    out.append("  <h2>K-GKE — Google GKE, Google-managed Kubernetes</h2>")
    out.append(f'  <p class="toc-sub">All {len(LESSONS)} K-GKE modules concatenated. Prereq: K-COM curriculum + GCP basics (IAM, VPC, GCE, Cloud LB, PD/Filestore, Cloud Logging/Monitoring).</p>')
    out.append('  <div class="toc-caveat"><strong>Heads up:</strong> Animations are disabled in this combined view. For interactive animations, open a per-module page directly.</div>')
    out.append("  <ol>")
    for b in bundles:
        out.append(f'    <li><a href="#lesson-{b["num"]}">{b["title"]}</a></li>')
    out.append("  </ol>")
    out.append("</section>")

    script_re = re.compile(r"<script>.*?</script>", re.DOTALL)
    for b in bundles:
        body = script_re.sub("", b["body"])
        out.append(f'<section class="course-section" id="lesson-{b["num"]}" aria-labelledby="lesson-{b["num"]}-banner">')
        out.append(f'  <div class="course-section-banner" id="lesson-{b["num"]}-banner">{b["title"]}</div>')
        out.append(body)
        out.append("</section>")

    out.append('<a href="#course-toc" class="course-back-to-toc">↑ TOC</a>')
    out.append("<script>")
    out.append("""
function safeStorageGet(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
function safeStorageSet(key, val) { try { localStorage.setItem(key, val); } catch (e) {} }
try { (function() {
  const themeToggle = document.getElementById('theme-toggle');
  if (!themeToggle) return;
  const stored = safeStorageGet('lesson-theme');
  if (stored) {
    document.body.setAttribute('data-theme', stored);
    themeToggle.textContent = stored === 'dark' ? '☀ Light' : '🌙 Dark';
  }
  themeToggle.addEventListener('click', () => {
    const cur = document.body.getAttribute('data-theme');
    const next = cur === 'light' ? 'dark' : 'light';
    document.body.setAttribute('data-theme', next);
    themeToggle.textContent = next === 'dark' ? '☀ Light' : '🌙 Dark';
    safeStorageSet('lesson-theme', next);
  });
})(); } catch (e) { console.warn('theme toggle setup failed', e); }
try { (function() {
  const jump = document.getElementById('lesson-jump');
  if (!jump) return;
  jump.addEventListener('change', () => { if (jump.value) { location.hash = '#' + jump.value; jump.value = ''; } });
})(); } catch (e) { console.warn('lesson-jump setup failed', e); }
try { document.querySelectorAll('.flashcard').forEach(card => card.addEventListener('click', () => card.classList.toggle('flipped'))); } catch (e) { console.warn('flashcard setup failed', e); }
try { document.querySelectorAll('.quiz-reveal').forEach(btn => {
  const showText = btn.textContent;
  const hideText = showText.replace(/^Show/, 'Hide');
  btn.addEventListener('click', () => { const ans = btn.parentElement.querySelector('.quiz-answer'); const open = ans.classList.toggle('show'); btn.textContent = open ? hideText : showText; });
}); } catch (e) { console.warn('quiz reveal setup failed', e); }
try { document.querySelectorAll('.pause-check-box').forEach(box => {
  const opts = box.querySelectorAll('.pause-check-opt');
  const fb = box.querySelector('.pause-check-feedback');
  opts.forEach(opt => opt.addEventListener('click', () => { opts.forEach(o => o.classList.remove('correct','wrong')); opt.classList.add(opt.dataset.correct === 'true' ? 'correct' : 'wrong'); fb.classList.add('show'); }));
}); } catch (e) { console.warn('pause-check setup failed', e); }
""")
    out.append("</script></body></html>")

    output_path = os.path.join(ROOT, "preview-kubernetes-gke-course-all.html")
    text = "\n".join(out)
    open(output_path, "w").write(text)
    print(f"Wrote {output_path} ({len(text):,} bytes, {len(bundles)} modules)")


if __name__ == "__main__":
    main()
