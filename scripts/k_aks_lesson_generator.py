#!/usr/bin/env python3
"""K-AKS (Azure AKS) lesson generator.

Mirrors scripts/k_eks_lesson_generator.py for the K-AKS curriculum.
Universe: K-Campus — Azure-managed campus complex; 11 wings mapping A1-A11.
Reuses BASE_CSS, SCRIPT_BLOCK, dataclasses, and _render_animation
from the K-COM generator.
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
# K-Campus atlas — 11 wings of the Azure-managed campus
# ---------------------------------------------------------------------------

KCAMPUS_WINGS = [
    ("kc-wing01", "A1", 100, 70, "Welcome Center", "architecture", "anchor"),
    ("kc-wing02", "A2", 240, 70, "Registrar's Office", "Entra + Workload ID", None),
    ("kc-wing03", "A3", 380, 70, "Pathways & Quad", "VNet + AGC + DNS", None),
    ("kc-wing04", "A4", 520, 70, "The Library", "Disks + Files + Blob", None),
    ("kc-wing05", "A5", 660, 70, "The Auditorium", "CA + KEDA + NAP", None),
    ("kc-wing06", "A6", 100, 200, "Campus Police", "Defender + Policy", None),
    ("kc-wing07", "A7", 240, 200, "Bell Tower", "Monitor + AMP + AMG", None),
    ("kc-wing08", "A8", 380, 200, "Student Union", "Dapr + Istio + Flux + Arc", None),
    ("kc-wing09", "A9", 520, 200, "Maintenance Yard", "upgrades + LTS", None),
    ("kc-wing10", "A10", 660, 200, "Health Clinic", "Azure-specific RCA", None),
    ("kc-wing11", "A11", 380, 320, "Commencement Hall", "capstone", None),
]

K_AKS_RAIL = [
    ("01", "A1 AKS architecture"),
    ("02", "A2 Entra &amp; identity"),
    ("03", "A3 AKS networking"),
    ("04", "A4 storage (Disks / Files / Blob)"),
    ("05", "A5 scaling (CA / KEDA / NAP)"),
    ("06", "A6 AKS security"),
    ("07", "A7 observability"),
    ("08", "A8 add-ons &amp; platform"),
    ("09", "A9 upgrades &amp; ops"),
    ("10", "A10 troubleshooting"),
    ("11", "A11 capstone campus"),
]

TOTAL_LESSONS_KAKS = 11


def _strip_index_kaks(num: str) -> int | None:
    try:
        return int(num) - 1
    except ValueError:
        return None


def _render_wing(wing: tuple, active_id: str) -> str:
    slug, num, x, y, label, sub, special = wing
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


def _render_kcampus_map(active_wing: str, lesson_num: str, wing_label: str) -> str:
    wings_svg = "\n    ".join(_render_wing(w, active_wing) for w in KCAMPUS_WINGS)
    active_idx = _strip_index_kaks(lesson_num)
    strip_parts = []
    for i in range(TOTAL_LESSONS_KAKS):
        cls = "ktown-strip-pin"
        if i == 0:
            cls += " ktown-strip-anchor"
        if i == active_idx:
            cls += " active"
        strip_parts.append(f'<li class="{cls}"></li>')
    strip_html = "\n    ".join(strip_parts)
    aria_label = f"Module A{int(lesson_num)}, {wing_label}."
    return f"""<div class="ktown-map-wrap">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" class="ktown-map" role="img" aria-label="K-Campus map: A{int(lesson_num)}">
    <title>K-Campus map · A{int(lesson_num)}</title>
    <desc>Stylised Azure-managed campus complex. {wing_label} highlighted.</desc>
    <defs>
      <linearGradient id="kc-grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#E8EFE0" stop-opacity="0.6"/><stop offset="100%" stop-color="#C8D8C0" stop-opacity="0.5"/></linearGradient>
      <linearGradient id="kc-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7AB3CC" stop-opacity="0.18"/><stop offset="100%" stop-color="#4A8FA8" stop-opacity="0.32"/></linearGradient>
    </defs>
    <rect x="20" y="20" width="760" height="360" rx="14" fill="url(#kc-grass)" stroke="#A8C4A0" stroke-width="1"/>
    <text x="400" y="38" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="10" font-weight="700" letter-spacing="3" fill="#9D9389">K · CAMPUS · AZURE REGION</text>
    <line x1="40" y1="130" x2="780" y2="130" stroke="#5F5E5A" stroke-width="0.7" stroke-dasharray="2,4" opacity="0.4"/>
    <line x1="40" y1="260" x2="780" y2="260" stroke="#5F5E5A" stroke-width="0.7" stroke-dasharray="2,4" opacity="0.4"/>
    <line x1="40" y1="370" x2="780" y2="370" stroke="#5F5E5A" stroke-width="0.7" stroke-dasharray="2,4" opacity="0.3"/>
    <text x="48" y="120" font-family="sans-serif" font-size="8" font-style="italic" fill="#9D9389">main quad &amp; gateway buildings</text>
    <text x="48" y="252" font-family="sans-serif" font-size="8" font-style="italic" fill="#9D9389">operations &amp; observation halls</text>
    <text x="48" y="362" font-family="sans-serif" font-size="8" font-style="italic" fill="#9D9389">commencement hall</text>
    {wings_svg}
  </svg>
  <ol class="ktown-strip" aria-hidden="true">
    {strip_html}
  </ol>
  <p class="ktown-strip-label">\U0001F3DB️ <strong>{wing_label}</strong> <span>· A{int(lesson_num)} of {TOTAL_LESSONS_KAKS}</span><span class="visually-hidden">{aria_label}</span></p>
</div>"""


def _render_concept_rail_kaks(current_num: str) -> str:
    items = []
    found = False
    for num, label in K_AKS_RAIL:
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
    return f"""<aside class="concept-rail" aria-label="K-AKS module journey">
  <span class="concept-rail-title">K-AKS modules</span>
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


def render_lesson_kaks(spec: LessonSpec) -> str:
    css = BASE_CSS + (spec.extra_css or "")
    map_html = _render_kcampus_map(spec.district_pin, spec.num, spec.district_label)
    rail_html = _render_concept_rail_kaks(spec.num)

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
    <h2>The story for this wing</h2>
{spec.analogy_intro_html}
    <div class="translation-legend">
      <table>
        <thead><tr><th>In the story…</th><th>…in AKS / Azure</th></tr></thead>
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
    <h2>How Azure-shop teams do this</h2>
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
    <span class="recap-badge">✓ Module A{int(spec.num)} complete</span>
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
    <a href="#" class="brand"><span class="brand-mark">SG</span><span>Suvis Guru</span><span class="course"> · K-AKS · Module A{int(spec.num)}</span></a>
    <span class="progress-pill">A{int(spec.num)} · {spec.title_short}</span>
    <button class="theme-toggle" id="theme-toggle" type="button">\U0001F319 Dark</button>
  </div>
</header>

<p class="district-line">\U0001F3DB️ K-Campus wing: <strong>{spec.district_label}</strong>.</p>

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

<footer>Suvis Guru · K-AKS · Module A{int(spec.num)} of {TOTAL_LESSONS_KAKS} · grounded in learn.microsoft.com/azure/aks</footer>

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


def _maybe_attach_animation_kaks(spec: LessonSpec, spec_path: str) -> None:
    spec_dir = os.path.dirname(os.path.abspath(spec_path))
    anim_path = os.path.join(spec_dir, "animations.py")
    if not os.path.exists(anim_path):
        return
    if spec_dir not in sys.path:
        sys.path.insert(0, spec_dir)
    spec_obj = importlib.util.spec_from_file_location("animations_kaks", anim_path)
    mod = importlib.util.module_from_spec(spec_obj)
    spec_obj.loader.exec_module(mod)
    animations = getattr(mod, "ANIMATIONS", {})
    if spec.num in animations and spec.animation is None:
        spec.animation = animations[spec.num]


def _run_audits_kaks() -> int:
    import subprocess
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_lessons_kaks.py")
    if not os.path.exists(path):
        return 0
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    if result.returncode != 0:
        print("\n>>> audit_lessons_kaks.py FAILED <<<")
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return 1
    print(f"audit: audit_lessons_kaks.py ✓ ({(result.stdout.splitlines() or [''])[0]})")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("specs", nargs="+", help="K-AKS spec modules")
    parser.add_argument("--out", default=ROOT)
    parser.add_argument("--no-audit", action="store_true")
    args = parser.parse_args()

    for spec_path in args.specs:
        mod = load_spec_module(spec_path)
        if not hasattr(mod, "LESSON"):
            sys.exit(f"{spec_path}: missing LESSON")
        spec: LessonSpec = mod.LESSON
        _maybe_attach_animation_kaks(spec, spec_path)
        html = render_lesson_kaks(spec)
        out_path = os.path.join(args.out, f"preview-kubernetes-aks-lesson-{spec.num}.html")
        with open(out_path, "w") as f:
            f.write(html)
        print(f"wrote {out_path}")

    if args.no_audit:
        print("\n[--no-audit] skipped post-generation audits.")
        return
    print()
    if _run_audits_kaks():
        sys.exit(2)


if __name__ == "__main__":
    main()
