#!/usr/bin/env python3
"""K-GKE (Google GKE) lesson generator.

Mirrors scripts/k_aks_lesson_generator.py for the K-GKE curriculum.
Universe: K-Garden — Google-managed botanical garden / orchard;
10 plots mapping G1-G10 (G10 = capstone).
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(ROOT, "scripts"))
from k8s_lesson_generator import (  # noqa: E402
    BASE_CSS, SCRIPT_BLOCK, LessonSpec, Animation, _render_animation,
)


# ---------------------------------------------------------------------------
# K-Garden atlas — 10 plots / facilities of the Google-managed garden
# ---------------------------------------------------------------------------

KGARDEN_PLOTS = [
    ("kg-plot01", "G1", 100, 70, "Visitors' Pavilion", "architecture", "anchor"),
    ("kg-plot02", "G2", 240, 70, "The Almanac Hut", "release channels", None),
    ("kg-plot03", "G3", 380, 70, "Pathways &amp; Trellises", "VPC + Gateway + LB", None),
    ("kg-plot04", "G4", 520, 70, "Gatekeeper's Lodge", "WIF + BinAuth + Posture", None),
    ("kg-plot05", "G5", 660, 70, "Reservoir &amp; Compost", "PD + Filestore + Hyperdisk", None),
    ("kg-plot06", "G6", 100, 200, "Auto-Greenhouse", "scaling + cost", None),
    ("kg-plot07", "G7", 240, 200, "Watchtower", "GMP + Cloud Mon + Trace", None),
    ("kg-plot08", "G8", 380, 200, "Research Greenhouse", "Fleets + AI/ML", None),
    ("kg-plot09", "G9", 520, 200, "Plant Doctor's Hut", "GCP-specific RCA", None),
    ("kg-plot10", "G10", 660, 200, "Harvest Festival", "capstone", None),
]

K_GKE_RAIL = [
    ("01", "G1 GKE architecture &amp; modes"),
    ("02", "G2 versioning &amp; channels"),
    ("03", "G3 GKE networking"),
    ("04", "G4 identity &amp; security"),
    ("05", "G5 GKE storage"),
    ("06", "G6 scaling &amp; cost"),
    ("07", "G7 GKE observability"),
    ("08", "G8 Enterprise (Fleets) &amp; AI/ML"),
    ("09", "G9 troubleshooting"),
    ("10", "G10 capstone harvest"),
]

TOTAL_LESSONS_KGKE = 10


def _strip_index_kgke(num: str) -> int | None:
    try:
        return int(num) - 1
    except ValueError:
        return None


def _render_plot(plot: tuple, active_id: str) -> str:
    slug, num, x, y, label, sub, special = plot
    is_active = slug == active_id
    classes = ["pin"]
    if special == "anchor":
        classes.append("pin-anchor")
    if is_active:
        classes.append("active")
    cls = " ".join(classes)
    halo_r = 22 if special == "anchor" else 18
    circle_r = 14 if special == "anchor" else 10
    circle_fill = "#3F4A5E" if special == "anchor" else "#9D9389"
    num_fontsize = 11 if special == "anchor" else 9
    num_y = 4 if special == "anchor" else 3
    label_y = 34 if special == "anchor" else 26
    label_fontsize = 11 if special == "anchor" else 10
    label_fontweight = ' font-weight="700"' if special == "anchor" else ""
    label_color = "#3F4A5E" if special == "anchor" else "#6B6058"
    sub_html = ""
    if sub:
        sub_y = 46 if special == "anchor" else 38
        sub_html = f'<text class="pin-sub" y="{sub_y}" text-anchor="middle" font-family="sans-serif" font-size="9" font-style="italic" fill="#9D9389">{sub}</text>'
    return (
        f'<g class="{cls}" id="{slug}" transform="translate({x},{y})">'
        f'<circle class="pin-halo" r="{halo_r}" fill="#D97757" opacity="0"/>'
        f'<circle class="pin-circle" r="{circle_r}" fill="{circle_fill}" stroke="#FBF7F0" stroke-width="{2.5 if special=="anchor" else 2}"/>'
        f'<text class="pin-num" y="{num_y}" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="{num_fontsize}" font-weight="700" fill="#FBF7F0">{num}</text>'
        f'<text class="pin-label" y="{label_y}" text-anchor="middle" font-family="sans-serif" font-size="{label_fontsize}" fill="{label_color}"{label_fontweight}>{label}</text>'
        f'{sub_html}'
        f'</g>'
    )


def _render_kgarden_map(active_plot: str, lesson_num: str, plot_label: str) -> str:
    plots_svg = "\n    ".join(_render_plot(p, active_plot) for p in KGARDEN_PLOTS)
    active_idx = _strip_index_kgke(lesson_num)
    strip_parts = []
    for i in range(TOTAL_LESSONS_KGKE):
        cls = "ktown-strip-pin"
        if i == 0:
            cls += " ktown-strip-anchor"
        if i == active_idx:
            cls += " active"
        strip_parts.append(f'<li class="{cls}"></li>')
    strip_html = "\n    ".join(strip_parts)
    aria_label = f"Module G{int(lesson_num)}, {plot_label}."
    return f"""<div class="ktown-map-wrap">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" class="ktown-map" role="img" aria-label="K-Garden map: G{int(lesson_num)}">
    <title>K-Garden map · G{int(lesson_num)}</title>
    <desc>Stylised Google-managed garden / orchard. {plot_label} highlighted.</desc>
    <defs>
      <linearGradient id="kg-soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#E8EFE0" stop-opacity="0.7"/><stop offset="100%" stop-color="#A8C896" stop-opacity="0.55"/></linearGradient>
      <linearGradient id="kg-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7AB3CC" stop-opacity="0.16"/><stop offset="100%" stop-color="#3F4A5E" stop-opacity="0.30"/></linearGradient>
    </defs>
    <rect x="20" y="20" width="760" height="360" rx="14" fill="url(#kg-soil)" stroke="#7BA068" stroke-width="1"/>
    <text x="400" y="38" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="10" font-weight="700" letter-spacing="3" fill="#9D9389">K · GARDEN · GCP REGION</text>
    <line x1="40" y1="130" x2="780" y2="130" stroke="#5F5E5A" stroke-width="0.7" stroke-dasharray="2,4" opacity="0.4"/>
    <line x1="40" y1="260" x2="780" y2="260" stroke="#5F5E5A" stroke-width="0.7" stroke-dasharray="2,4" opacity="0.4"/>
    <text x="48" y="120" font-family="sans-serif" font-size="8" font-style="italic" fill="#9D9389">front of garden — pavilion &amp; planting</text>
    <text x="48" y="252" font-family="sans-serif" font-size="8" font-style="italic" fill="#9D9389">deeper plots — operations &amp; harvest</text>
    {plots_svg}
  </svg>
  <ol class="ktown-strip" aria-hidden="true">
    {strip_html}
  </ol>
  <p class="ktown-strip-label">\U0001F33F <strong>{plot_label}</strong> <span>· G{int(lesson_num)} of {TOTAL_LESSONS_KGKE}</span><span class="visually-hidden">{aria_label}</span></p>
</div>"""


def _render_concept_rail_kgke(current_num: str) -> str:
    items = []
    found = False
    for num, label in K_GKE_RAIL:
        if num == current_num:
            cls = "concept-rail-item current"
            icon = "▶"
            here = '<span class="concept-rail-here">← here</span>'
            found = True
        elif not found:
            cls = "concept-rail-item done"
            icon = "✓"
            here = ""
        else:
            cls = "concept-rail-item"
            icon = "○"
            here = ""
        items.append(f'  <div class="{cls}"><span class="concept-rail-icon">{icon}</span><span>{label}</span>{here}</div>')
    return f"""<aside class="concept-rail" aria-label="K-GKE module journey">
  <span class="concept-rail-title">K-GKE modules</span>
{chr(10).join(items)}
</aside>"""


def _render_section(sec) -> str:
    return f"""  <section class="s">
    <span class="s-eyebrow">{sec.eyebrow}</span>
    <h2>{sec.h2}</h2>
{sec.body_html}
  </section>"""


def _render_pause_check(pc) -> str:
    opts = "\n        ".join(
        f'<li><button type="button" class="pause-check-opt" data-correct="{str(c).lower()}">{t}</button></li>'
        for t, c in pc.options
    )
    return f"""  <div class="pause-check">
    <div class="pause-check-box">
      <span class="pause-check-tag">⏸ Pause and check</span>
      <p class="pause-check-q">{pc.question}</p>
      <ul class="pause-check-opts">
        {opts}
      </ul>
      <p class="pause-check-feedback">{pc.feedback}</p>
    </div>
  </div>"""


def render_lesson_kgke(spec: LessonSpec) -> str:
    css = BASE_CSS + (spec.extra_css or "")
    map_html = _render_kgarden_map(spec.district_pin, spec.num, spec.district_label)
    rail_html = _render_concept_rail_kgke(spec.num)

    sections_html = []
    for i, sec in enumerate(spec.sections):
        sections_html.append(_render_section(sec))
        if i in spec.pause_check_after_section:
            sections_html.append(_render_pause_check(spec.pause_check_after_section[i]))
    sections_block = "\n\n".join(sections_html)

    ba_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 2 · Before &amp; After</span>
    <h2>What changes when you adopt this</h2>
    <div class="ba-grid">
      <div class="ba before"><span class="ba-label">Before</span>{spec.before_after_before}</div>
      <div class="ba after"><span class="ba-label">After</span>{spec.before_after_after}</div>
    </div>
    {spec.before_after_caption}
  </section>"""

    legend_rows = "\n".join(
        f'          <tr><td>{story}</td><td>{k8s}</td></tr>'
        for story, k8s in spec.translation_rows
    )
    analogy_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 3 · Analogy</span>
    <h2>The story for this plot</h2>
{spec.analogy_intro_html}
    <div class="translation-legend">
      <table>
        <thead><tr><th>In the story…</th><th>…in GKE / GCP</th></tr></thead>
        <tbody>
{legend_rows}
        </tbody>
      </table>
    </div>
    <p class="analogy-stops">⚠️ <em>{spec.analogy_stops}</em></p>
  </section>"""

    eli_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 4 · Two-level explanation</span>
    <h2>Two ways to hear it</h2>
    <div class="eli">
      <div class="eli-card">
        <span class="eli-tag five">ELI5 · explain like I'm 5</span>
        <p>{spec.eli5}</p>
      </div>
      <div class="eli-card">
        <span class="eli-tag ten">ELI10 · explain like I'm 10</span>
        <p>{spec.eli10}</p>
      </div>
    </div>
  </section>"""

    scenarios_html = "\n".join(
        f'      <div class="scenario"><p class="scenario-name">{s.name}</p><p>{s.body}</p></div>'
        for s in spec.scenarios
    )
    scenarios_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 5 · Real-world scenarios</span>
    <h2>How GCP-shop teams do this</h2>
    <div class="scenarios">
{scenarios_html}
    </div>
  </section>"""

    anim_section, anim_script = _render_animation(spec.animation)

    miscs_html = "\n".join(
        f'        <div class="misc-card">'
        f'<div class="misc-row misc-myth"><strong>Myth:</strong> {m.myth}</div>'
        f'<div class="misc-row misc-truth"><strong>Truth:</strong> {m.truth}</div>'
        f'</div>'
        for m in spec.misconceptions
    )
    flashcards_html = "\n".join(
        f'      <div class="flashcard"><div class="flashcard-inner">'
        f'<div class="flashcard-face flashcard-front">{f.front}<div class="flashcard-hint">tap to flip</div></div>'
        f'<div class="flashcard-face flashcard-back">{f.back}</div>'
        f'</div></div>'
        for f in spec.flashcards
    )

    quiz_cards_html = []
    for q in spec.quizzes:
        if q.cyoa:
            quiz_cards_html.append(
                f'      <div class="quiz-card cyoa-quiz">'
                f'<span class="cyoa-tag">\U0001F3AC Choose Your Own Adventure</span>'
                f'<p class="quiz-prompt">{q.prompt}</p>'
                f'<button class="quiz-reveal" type="button">Show what happened</button>'
                f'<div class="quiz-answer"><span class="quiz-answer-tag">{q.cyoa_tag}</span>{q.answer}</div>'
                f'</div>'
            )
        else:
            quiz_cards_html.append(
                f'      <div class="quiz-card">'
                f'<p class="quiz-prompt">{q.prompt}</p>'
                f'<button class="quiz-reveal" type="button">Show answer</button>'
                f'<div class="quiz-answer"><span class="quiz-answer-tag">answer</span>{q.answer}</div>'
                f'</div>'
            )
    quizzes_html = "\n".join(quiz_cards_html)

    misc_quiz_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 7 · Misconceptions, flashcards &amp; quiz</span>
    <h2>Lock it in</h2>
    <p>A few common misconceptions to clear up first, then the flashcards and quiz.</p>
    <div class="misconceptions">
      <h3>Common Misconceptions</h3>
      <div class="misconceptions-grid">
{miscs_html}
      </div>
    </div>
    <div class="flashcard-grid">
{flashcards_html}
    </div>
    <div class="quiz-grid" style="margin-top:24px">
{quizzes_html}
    </div>
  </section>"""

    glossary_html = "\n".join(
        f'      <div class="gloss-item"><div class="gloss-name">{g.name}</div><div class="gloss-def">{g.definition}</div></div>'
        for g in spec.glossary
    )
    glossary_block = f"""  <details class="glossary">
    <summary>Words from this module · open if you want a quick reference</summary>
    <div class="glossary-grid">
{glossary_html}
    </div>
  </details>"""

    recap_block = f"""  <section class="recap">
    <span class="recap-badge">✓ Module G{int(spec.num)} complete</span>
    <p>{spec.recap_lead}</p>
    <p class="recap-next">{spec.recap_next}</p>
  </section>"""

    if anim_script:
        combined_script = SCRIPT_BLOCK.rstrip().rstrip("</script>").rstrip() + "\n" + anim_script + "\n</script>\n"
    else:
        combined_script = SCRIPT_BLOCK

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{spec.title_html}</title>
<style>{css}</style>
</head>
<body data-theme="light">

{rail_html}

<header class="topbar">
  <div class="topbar-inner">
    <a href="#" class="brand"><span class="brand-mark">SG</span><span>Suvis Guru</span><span class="course"> · K-GKE · Module G{int(spec.num)}</span></a>
    <span class="progress-pill">G{int(spec.num)} · {spec.title_short}</span>
    <button class="theme-toggle" id="theme-toggle" type="button">\U0001F319 Dark</button>
  </div>
</header>

<p class="district-line">\U0001F33F K-Garden plot: <strong>{spec.district_label}</strong>.</p>

{map_html}

<main>

  <section class="hero">
    <span class="eyebrow">{spec.module_eyebrow}</span>
    <h1>{spec.title_full}</h1>
    <p class="hero-sub">{spec.hero_sub_html}</p>
    <div class="hero-illu">
{spec.hero_illu_svg}
    </div>
  </section>

  <div class="nightmare">
    <div class="nightmare-box">
      <span class="nightmare-tag">\U0001F6A8 The 3 AM Nightmare</span>
      <p>{spec.nightmare_html}</p>
    </div>
  </div>

  <div class="stamp">
    <p class="stamp-box">\U0001F3AF <strong>If you remember nothing else:</strong> {spec.stamp_html}</p>
  </div>

{sections_block}

{ba_block}

{analogy_block}

{eli_block}

{scenarios_block}

{anim_section}

{misc_quiz_block}

{glossary_block}

  <div class="stamp">
    <p class="stamp-box">\U0001F3AF <strong>If you remember nothing else:</strong> {spec.stamp_html}</p>
  </div>

{recap_block}

</main>

<footer>Suvis Guru · K-GKE · Module G{int(spec.num)} of {TOTAL_LESSONS_KGKE} · grounded in cloud.google.com/kubernetes-engine</footer>

{combined_script}
</body>
</html>
"""


def load_spec_module(path: str):
    abs_path = os.path.abspath(path)
    spec_dir = os.path.dirname(abs_path)
    if spec_dir not in sys.path:
        sys.path.insert(0, spec_dir)
    spec_name = os.path.splitext(os.path.basename(abs_path))[0]
    spec_obj = importlib.util.spec_from_file_location(spec_name, abs_path)
    mod = importlib.util.module_from_spec(spec_obj)
    spec_obj.loader.exec_module(mod)
    return mod


def _maybe_attach_animation_kgke(spec: LessonSpec, spec_path: str) -> None:
    spec_dir = os.path.dirname(os.path.abspath(spec_path))
    anim_path = os.path.join(spec_dir, "animations.py")
    if not os.path.exists(anim_path):
        return
    if spec_dir not in sys.path:
        sys.path.insert(0, spec_dir)
    spec_obj = importlib.util.spec_from_file_location("animations_kgke", anim_path)
    mod = importlib.util.module_from_spec(spec_obj)
    spec_obj.loader.exec_module(mod)
    animations = getattr(mod, "ANIMATIONS", {})
    if spec.num in animations and spec.animation is None:
        spec.animation = animations[spec.num]


def _run_audits_kgke() -> int:
    import subprocess
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_lessons_kgke.py")
    if not os.path.exists(path):
        return 0
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    if result.returncode != 0:
        print("\n>>> audit_lessons_kgke.py FAILED <<<")
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return 1
    print(f"audit: audit_lessons_kgke.py ✓ ({(result.stdout.splitlines() or [''])[0]})")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("specs", nargs="+", help="K-GKE spec modules")
    parser.add_argument("--out", default=ROOT)
    parser.add_argument("--no-audit", action="store_true")
    args = parser.parse_args()

    for spec_path in args.specs:
        mod = load_spec_module(spec_path)
        if not hasattr(mod, "LESSON"):
            sys.exit(f"{spec_path}: missing LESSON")
        spec: LessonSpec = mod.LESSON
        _maybe_attach_animation_kgke(spec, spec_path)
        html = render_lesson_kgke(spec)
        out_path = os.path.join(args.out, f"preview-kubernetes-gke-lesson-{spec.num}.html")
        with open(out_path, "w") as f:
            f.write(html)
        print(f"wrote {out_path}")

    if args.no_audit:
        print("\n[--no-audit] skipped post-generation audits.")
        return
    print()
    if _run_audits_kgke():
        sys.exit(2)


if __name__ == "__main__":
    main()
