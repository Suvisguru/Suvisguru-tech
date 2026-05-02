#!/usr/bin/env python3
"""Build a single-file combined view of all 16 K-COM lessons.

Output: preview-kubernetes-course-all.html at the repo root.

Each lesson HTML is a complete self-contained page (its own <head>,
<body>, ID namespace, fixed-position concept rail, and animation
<script>). Naive concatenation breaks: topbars stack, concept rails
layer on top of each other, animation IDs collide.

This script:
  1. Extracts each lesson's <style> block and body content (the
     range from </header> through </footer>, inclusive).
  2. Concatenates the styles. CSS duplicates are harmless.
  3. Wraps each lesson's body in <section class="course-section"
     id="lesson-NN">.
  4. Adds a course-level topbar with theme toggle + lesson-jump
     dropdown, and a TOC section listing all 16 lessons.
  5. Replaces the 16 per-lesson <script> blocks with one
     consolidated set of document-wide handlers (theme toggle,
     flashcard flip, quiz reveal, pause-and-check). Per-lesson
     animation logic is dropped — animations require unique-per-page
     element IDs that the 16 lessons reuse, so they would collide.
     Diagrams remain visible as static SVGs.

Caveats documented at the top of the output HTML.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LESSONS = [
    ("01", "preview-kubernetes-lesson-01.html", "What is Kubernetes?"),
    ("02", "preview-kubernetes-lesson-02.html", "Virtualization vs Containerization"),
    ("03", "preview-kubernetes-lesson-03.html", "Cloud-Native Principles"),
    ("04", "preview-kubernetes-lesson-04.html", "12-Factor + Microservices vs Monoliths"),
    ("05", "preview-kubernetes-lesson-05.html", "When K8s Fits / Overkill"),
    ("06", "preview-kubernetes-lesson-06.html", "GitOps · Platform Eng · SRE · Multi-Tenancy"),
    ("07", "preview-kubernetes-lesson-07.html", "History · CNCF · Releases · KEPs · Feature Gates"),
    ("7-5", "preview-kubernetes-lesson-7-5.html", "How a Linux Computer Works in 5 Minutes (primer)"),
    ("08", "preview-kubernetes-lesson-08.html", "Linux Namespaces · cgroups · Capabilities"),
    ("09", "preview-kubernetes-lesson-09.html", "Container Runtimes & OCI"),
    ("10", "preview-kubernetes-lesson-10.html", "Image Building · Multi-stage · Distroless · SBOM"),
    ("11", "preview-kubernetes-lesson-11.html", "Container Security & Registries"),
    ("12", "preview-kubernetes-lesson-12.html", "PID 1 & Container Lifecycle"),
    ("13", "preview-kubernetes-lesson-13.html", "Cluster Architecture"),
    ("14", "preview-kubernetes-lesson-14.html", "The K8s API & YAML"),
    ("15", "preview-kubernetes-lesson-15.html", "Pods Deep Dive"),
    ("16", "preview-kubernetes-lesson-16.html", "Workload Controllers · Deployment, StatefulSet, DaemonSet, Job, CronJob"),
    ("17", "preview-kubernetes-lesson-17.html", "Services & Networking · ClusterIP, NodePort, LoadBalancer, Ingress, NetworkPolicy"),
    ("18", "preview-kubernetes-lesson-18.html", "Storage Pt 1 · PV, PVC, StorageClass"),
    ("19", "preview-kubernetes-lesson-19.html", "Storage Pt 2 · CSI, Snapshots, VolumeAttributesClass"),
    ("20", "preview-kubernetes-lesson-20.html", "Configuration & Secrets · ConfigMap, Secret, KMS, ESO"),
    ("21", "preview-kubernetes-lesson-21.html", "ServiceAccounts & Certificates · Tokens, cert-manager, PKI"),
    ("22", "preview-kubernetes-lesson-22.html", "Scheduling Pt 1 · Affinity, Taints, Topology Spread"),
    ("23", "preview-kubernetes-lesson-23.html", "Scheduling Pt 2 · Priority, DRA, NUMA, Profiles"),
    ("24", "preview-kubernetes-lesson-24.html", "Networking Foundations · Linux Primitives, CNI, MTU"),
    ("25", "preview-kubernetes-lesson-25.html", "Gateway API · Roles, Listeners, Routes, Ingress Sunset"),
    ("26", "preview-kubernetes-lesson-26.html", "AdminNetworkPolicy & FQDN-Based Egress"),
    ("27", "preview-kubernetes-lesson-27.html", "RBAC & Authentication · Roles, Bindings, OIDC"),
    ("28", "preview-kubernetes-lesson-28.html", "Admission Control · ValidatingAdmissionPolicy, PSA, Webhooks"),
    ("29", "preview-kubernetes-lesson-29.html", "Policy Engines · Kyverno and OPA Gatekeeper"),
    ("30", "preview-kubernetes-lesson-30.html", "Supply Chain Security · Cosign, Sigstore, SLSA, SBOM"),
    ("31", "preview-kubernetes-lesson-31.html", "Multi-Tenancy & Hardening · Quotas, kube-bench, HNC"),
    ("32", "preview-kubernetes-lesson-32.html", "Observability Pt 1 · Logs and Metrics"),
    ("33", "preview-kubernetes-lesson-33.html", "Observability Pt 2 · Traces, eBPF, SLOs"),
    ("34", "preview-kubernetes-lesson-34.html", "Autoscaling · HPA, VPA, KEDA, Karpenter"),
    ("35", "preview-kubernetes-lesson-35.html", "Reliability & HA · PDB, Multi-Zone, Regional DR"),
    ("36", "preview-kubernetes-lesson-36.html", "Kustomize · Overlay-Based Manifest Customisation"),
    ("37", "preview-kubernetes-lesson-37.html", "Helm 3 · Charts, Values, Hooks, OCI"),
    ("38", "preview-kubernetes-lesson-38.html", "GitOps with Argo CD · Application CRD, Sync, Drift"),
    ("39", "preview-kubernetes-lesson-39.html", "GitOps with Flux CD · Multi-Controller Architecture"),
    ("40", "preview-kubernetes-lesson-40.html", "Progressive Delivery · Argo Rollouts and Flagger"),
    ("41", "preview-kubernetes-lesson-41.html", "CRDs Deep Dive · Schema, CEL, Conversion Webhooks"),
    ("42", "preview-kubernetes-lesson-42.html", "Operators with Kubebuilder · controller-runtime, OLM"),
    ("43", "preview-kubernetes-lesson-43.html", "Service Mesh · Istio Ambient, Linkerd, Cilium Mesh"),
    ("44", "preview-kubernetes-lesson-44.html", "Troubleshooting Methodology + Drills (Capstone)"),
]


def extract_style_and_body(path: str):
    content = open(path).read()

    # Pull the <style>...</style> block (each lesson has exactly one).
    m = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    style = m.group(1) if m else ""

    # Pull body content from after </header> through </footer> inclusive.
    # </header> closes the per-lesson topbar; </footer> closes the per-lesson footer.
    body_start = content.index('</header>') + len('</header>')
    body_end = content.index('</footer>', body_start) + len('</footer>')
    body = content[body_start:body_end].strip()

    return style, body


def main() -> None:
    bundles = []
    for num, fname, title in LESSONS:
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            sys.exit(f"missing: {path}")
        style, body = extract_style_and_body(path)
        bundles.append({"num": num, "fname": fname, "title": title, "style": style, "body": body})

    # ---- Build the combined HTML ----
    out: list[str] = []
    out.append("<!DOCTYPE html>")
    out.append('<html lang="en">')
    out.append("<head>")
    out.append('<meta charset="UTF-8">')
    out.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    out.append(f"<title>K-COM · The Whole Course (all {len(LESSONS)} lessons)</title>")
    out.append("<style>")

    # Concatenate every lesson's <style> block. Duplicate CSS rules are
    # harmless (last-one-wins identically). The :root + dark-theme blocks
    # are identical across all 16 files; per-lesson custom blocks
    # (.prim-grid, .build-grid, .flow-list, .ha-grid, .qos, etc.) are
    # unique class names and don't conflict.
    for b in bundles:
        out.append(f"\n/* ============ {b['fname']} ============ */")
        out.append(b["style"])

    out.append("""
/* === Combined-view-only overrides (course chrome) === */
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
.course-toc .toc-caveat strong{color:var(--ink);font-weight:600}
.course-toc ol{columns:2;column-gap:32px;padding:0 0 0 24px;margin:0}
@media (max-width:640px){.course-toc ol{columns:1}}
.course-toc li{margin:7px 0;line-height:1.5;break-inside:avoid;font-size:14px}
.course-toc li::marker{color:var(--ink-faint);font-weight:700}
.course-toc a{color:var(--accent);text-decoration:none;font-weight:600}
.course-toc a:hover{text-decoration:underline}
.course-toc li.primer{font-style:italic;color:var(--ink-soft)}
.course-toc li.primer::marker{color:var(--gold)}

/* Left sidebar — fixed list of all 16 lessons, visible at >=1240px */
.course-sidebar{display:none;font-family:inherit}
.course-sidebar h3{font-size:11px;font-weight:700;color:var(--ink-faint);text-transform:uppercase;letter-spacing:1.5px;margin:0 0 10px}
.course-sidebar ol{list-style:none;padding:0;margin:0}
.course-sidebar li{margin:1px 0}
.course-sidebar a{display:flex;gap:8px;padding:5px 10px;color:var(--ink-soft);text-decoration:none;border-radius:var(--r-soft);border-left:2px solid transparent;font-size:12.5px;line-height:1.45;transition:background .15s var(--ease),color .15s var(--ease)}
.course-sidebar a:hover{color:var(--ink);background:var(--bg-soft)}
.course-sidebar a.current{color:var(--ink);font-weight:600;border-left-color:var(--warm);background:var(--bg-soft)}
.course-sidebar .num{color:var(--ink-faint);font-weight:700;min-width:26px;flex:0 0 auto}
.course-sidebar a.current .num{color:var(--accent)}
.course-sidebar li.primer a{font-style:italic;color:var(--ink-faint)}
.course-sidebar li.primer a.current{color:var(--ink);font-style:italic}
@media (min-width:1240px){
  .course-sidebar{display:block;position:fixed;top:76px;left:max(16px,calc(50vw - 600px));width:180px;max-height:calc(100vh - 96px);overflow-y:auto;z-index:80;padding:14px 8px 14px 0}
}

.course-section{border-top:6px solid var(--accent);margin-top:80px;scroll-margin-top:72px}
.course-section:first-of-type{border-top:0;margin-top:0}
.course-section .concept-rail{display:none!important}
.course-section header.topbar{display:none}

.course-section-banner{max-width:820px;margin:0 auto;padding:18px 24px 0;font-size:13px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:1.5px}
.course-section-banner span{color:var(--ink-faint);font-weight:400;letter-spacing:0;text-transform:none;font-size:13px;margin-left:8px}

.course-back-to-toc{position:fixed;bottom:24px;right:24px;background:var(--accent);color:#fff;padding:10px 18px;border-radius:var(--r-pill);font-size:13px;font-weight:600;text-decoration:none;box-shadow:var(--shadow-md);z-index:150;opacity:.92}
.course-back-to-toc:hover{opacity:1}
[data-theme="dark"] .course-back-to-toc{color:var(--bg)}

@media print{
  .course-back-to-toc,.course-topbar{display:none}
  .course-section{break-before:page;border-top:0}
}
""")
    out.append("</style>")
    out.append("</head>")
    out.append('<body data-theme="light">')

    # --- Course-level topbar ---
    out.append('<header class="course-topbar">')
    out.append('  <a href="#course-toc" class="brand">'
               '<span class="brand-mark">SG</span>'
               '<span>Suvis Guru</span>'
               '<span class="brand-meta"> · K-COM · the whole course</span>'
               '</a>')
    out.append('  <select class="lesson-jump" id="lesson-jump" aria-label="Jump to lesson">')
    out.append('    <option value="">Jump to lesson…</option>')
    for b in bundles:
        out.append(f'    <option value="lesson-{b["num"]}">Lesson {b["num"]} — {b["title"]}</option>')
    out.append("  </select>")
    out.append('  <button class="theme-toggle" id="theme-toggle" type="button">🌙 Dark</button>')
    out.append("</header>")

    # --- Left sidebar (visible at >=1240px) ---
    out.append('<aside class="course-sidebar" aria-label="Course lesson navigation">')
    out.append(f'  <h3>The {len(LESSONS)} lessons</h3>')
    out.append('  <ol>')
    for b in bundles:
        cls = ' class="primer"' if 'primer' in b['title'].lower() else ''
        # Shortened display title for sidebar so it fits 180px width
        short = b['title'].split(' (primer)')[0]
        # Aggressively shorten common long forms
        short = short.replace('Cloud-Native ', '').replace('Multi-stage · Distroless · SBOM', '· Distroless · SBOM').replace('· KEPs · Feature Gates', '· KEPs')
        out.append(f'    <li{cls}><a href="#lesson-{b["num"]}"><span class="num">{b["num"]}</span><span>{short}</span></a></li>')
    out.append('  </ol>')
    out.append('</aside>')

    # --- Course TOC ---
    out.append('<section class="course-toc" id="course-toc">')
    out.append("  <h2>K-COM — the whole course in one page</h2>")
    out.append(f"  <p class=\"toc-sub\">All {len(LESSONS)} K-COM lessons concatenated into one scrollable document. Use the dropdown in the top bar to jump between lessons, or click a lesson title below.</p>")
    out.append("  <div class=\"toc-caveat\"><strong>Heads up:</strong> Animations are disabled in this combined view (per-lesson animation scripts use shared element IDs that would collide across sections). For interactive animations, open the per-lesson page directly. Static diagrams, flashcards, quizzes, and pause-and-checks all work in this combined view.</div>")
    out.append("  <ol>")
    for b in bundles:
        cls = "primer" if "primer" in b["title"].lower() else ""
        cls_attr = f' class="{cls}"' if cls else ""
        out.append(f'    <li{cls_attr}><a href="#lesson-{b["num"]}">Lesson {b["num"]} — {b["title"]}</a></li>')
    out.append("  </ol>")
    out.append("</section>")

    # --- Each lesson as a section ---
    # Strip per-lesson <script> blocks from each body — animations would
    # collide on shared IDs (lesson-anim, anim-pkg, srv-1-rect, etc.) and
    # JS variables (animTimer, currentMode) would be redefined 16 times.
    script_re = re.compile(r"<script>.*?</script>", re.DOTALL)

    for b in bundles:
        body = b["body"]
        body = script_re.sub("", body)
        out.append(f'<section class="course-section" id="lesson-{b["num"]}" aria-labelledby="lesson-{b["num"]}-banner">')
        out.append(f'  <div class="course-section-banner" id="lesson-{b["num"]}-banner">Lesson {b["num"]}<span>· {b["title"]}</span></div>')
        out.append(body)
        out.append("</section>")

    # --- Back-to-TOC FAB ---
    out.append('<a href="#course-toc" class="course-back-to-toc">↑ TOC</a>')

    # --- Consolidated document-wide JS handlers ---
    out.append("<script>")
    out.append("""
// Theme toggle (single, document-wide)
(function() {
  const themeToggle = document.getElementById('theme-toggle');
  const stored = localStorage.getItem('lesson-theme');
  if (stored) {
    document.body.setAttribute('data-theme', stored);
    themeToggle.textContent = stored === 'dark' ? '☀ Light' : '🌙 Dark';
  }
  themeToggle.addEventListener('click', () => {
    const cur = document.body.getAttribute('data-theme');
    const next = cur === 'light' ? 'dark' : 'light';
    document.body.setAttribute('data-theme', next);
    themeToggle.textContent = next === 'dark' ? '☀ Light' : '🌙 Dark';
    localStorage.setItem('lesson-theme', next);
  });
})();

// Lesson jump dropdown
(function() {
  const jump = document.getElementById('lesson-jump');
  jump.addEventListener('change', () => {
    if (jump.value) {
      location.hash = '#' + jump.value;
      jump.value = '';
    }
  });
})();

// Flashcards (document-wide)
document.querySelectorAll('.flashcard').forEach(card => {
  card.addEventListener('click', () => card.classList.toggle('flipped'));
});

// Quiz reveals (document-wide; handles "Show answer" + CYOA "Show what happened")
document.querySelectorAll('.quiz-reveal').forEach(btn => {
  const showText = btn.textContent;
  const hideText = showText.replace(/^Show/, 'Hide');
  btn.addEventListener('click', () => {
    const ans = btn.parentElement.querySelector('.quiz-answer');
    const open = ans.classList.toggle('show');
    btn.textContent = open ? hideText : showText;
  });
});

// Pause-and-check (document-wide)
document.querySelectorAll('.pause-check-box').forEach(box => {
  const opts = box.querySelectorAll('.pause-check-opt');
  const fb = box.querySelector('.pause-check-feedback');
  opts.forEach(opt => {
    opt.addEventListener('click', () => {
      opts.forEach(o => o.classList.remove('correct','wrong'));
      opt.classList.add(opt.dataset.correct === 'true' ? 'correct' : 'wrong');
      fb.classList.add('show');
    });
  });
});

// Sidebar scroll-spy — highlight the current lesson as the reader scrolls
(function() {
  const sidebarLinks = document.querySelectorAll('.course-sidebar a');
  const linkByHash = {};
  sidebarLinks.forEach(a => { linkByHash[a.getAttribute('href')] = a; });
  const sections = document.querySelectorAll('.course-section');
  if (!sections.length || !sidebarLinks.length) return;

  function setCurrent(id) {
    sidebarLinks.forEach(a => a.classList.remove('current'));
    const a = linkByHash['#' + id];
    if (a) a.classList.add('current');
  }

  // IntersectionObserver — fires when a section enters the trigger zone
  // (top 30% of viewport). The most-recent intersecting section is "current."
  let lastIntersecting = null;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        lastIntersecting = entry.target.id;
        setCurrent(entry.target.id);
      }
    });
  }, { rootMargin: '-72px 0px -60% 0px', threshold: 0 });

  sections.forEach(s => observer.observe(s));

  // Also respond to clicks on sidebar links — set immediately rather than
  // waiting for the scroll to land.
  sidebarLinks.forEach(a => {
    a.addEventListener('click', () => setCurrent(a.getAttribute('href').slice(1)));
  });
})();
""")
    out.append("</script>")
    out.append("</body>")
    out.append("</html>")

    output_path = os.path.join(ROOT, "preview-kubernetes-course-all.html")
    text = "\n".join(out)
    open(output_path, "w").write(text)
    print(f"Wrote {output_path} ({len(text):,} bytes, {len(bundles)} lessons)")


if __name__ == "__main__":
    main()
