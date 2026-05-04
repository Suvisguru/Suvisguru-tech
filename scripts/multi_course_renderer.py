"""Shared multi-course renderer for the K-* curriculum generators.

K-VAN, K-EKS, K-AKS, K-GKE, K-OCP all share an identical structural
template: atlas-pin map + concept rail + 4 sections + before/after +
analogy + ELI5/10 + scenarios + animation + misconceptions/quiz +
glossary + recap. The differences are entirely encoded in CourseConfig.

Each course's per-course generator becomes a thin file declaring its
config and calling run_course_main().

K-COM (the original generator at k8s_lesson_generator.py) is NOT
refactored — it owns the shared BASE_CSS / SCRIPT_BLOCK / dataclasses /
_render_animation that this module imports, plus has the L7-5 primer
exception and a 24-pin atlas with a different shape.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from k8s_lesson_generator import (  # noqa: E402
    BASE_CSS, SCRIPT_BLOCK, LessonSpec, _render_animation,
)


# ---------------------------------------------------------------------------
# Course configuration — fully describes a K-* course's rendering
# ---------------------------------------------------------------------------

@dataclass
class CourseConfig:
    # Course identity
    course_code: str               # "K-OCP", "K-GKE", "K-AKS", "K-EKS", "K-VAN"
    course_letter: str             # "O", "G", "A", "E", "V" (module letter prefix)
    course_full_name: str          # "Red Hat OpenShift", "Google GKE", ...
    universe_name: str             # "K-Foundry", "K-Garden", "K-Campus", "K-Skyline", "K-Frontier"
    universe_emoji: str            # district-line emoji: "🏭", "🌿", "🏛️", "🏙️", "🏕️"
    district_kind: str             # "bay", "plot", "wing", "floor", "site"
    legend_subject: str            # "OpenShift / Red Hat", "GKE / GCP", ...
    real_world_heading: str        # "How OpenShift teams do this"

    # Atlas + rail
    atlas_pins: list                # [(slug, num, x, y, label, sub, special)]
    rail_items: list                # [(num, label)]
    pin_prefix: str                # "ko-bay" / "kg-plot" / "kc-wing" / "ks-floor" / "kf-site"
    total_lessons: int             # 13 / 10 / 11 / 11 / 11

    # File naming
    html_filename_segment: str     # "ocp", "gke", "aks", "eks", "vanilla"
    audit_script_basename: str     # "audit_lessons_kocp.py", etc.
    footer_grounded_url: str       # "docs.openshift.com" / etc.

    # Optional overrides (default to district_kind / universe_emoji / "Module")
    analogy_section_subject: str = ""      # K-VAN: "build site"; default = district_kind
    strip_label_emoji: str = ""            # default = universe_emoji
    aria_lesson_word: str = "Module"       # K-VAN aria SVG uses "Lesson"

    # Map SVG basics
    map_viewbox: str = "0 0 800 400"       # K-OCP overrides to "0 0 800 420"
    map_floor_height: int = 360            # K-OCP overrides to 380 for 13 pins
    map_floor_stroke: str = "#7BA068"      # rect stroke color
    map_aria_word: str = "map"             # K-VAN: "site map"; K-EKS: "tower map"; default "map"
    map_subtitle: str = ""                 # "K · GARDEN · GCP REGION"
    map_desc_subject: str = ""             # "Google-managed garden / orchard"

    # Map gradients (kf-soil + kf-creek pattern; kg-soil + kg-sky; etc.)
    map_grad_id_primary: str = ""          # "kg-soil"
    map_grad_id_secondary: str = ""        # "kg-sky"
    map_grad_primary_stops: tuple = ()     # ((offset, color, opacity), ...)
    map_grad_secondary_stops: tuple = ()

    # Map decorations + dividers
    map_decorations_svg: str = ""          # raw SVG (K-VAN's creek path/text)
    # Dividers: list of (line_y, line_opacity, label_y_or_None, label_text_or_None)
    map_dividers: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------

def _strip_index(num: str) -> int | None:
    try:
        return int(num) - 1
    except ValueError:
        return None


def render_atlas_pin(pin: tuple, active_id: str) -> str:
    """Render one atlas pin (bay / plot / wing / floor / site)."""
    slug, num, x, y, label, sub, special = pin
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
        sub_html = (
            f'<text class="pin-sub" y="{sub_y}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="9" font-style="italic" '
            f'fill="#9D9389">{sub}</text>'
        )
    return (
        f'<g class="{cls}" id="{slug}" transform="translate({x},{y})">'
        f'<circle class="pin-halo" r="{halo_r}" fill="#D97757" opacity="0"/>'
        f'<circle class="pin-circle" r="{circle_r}" fill="{circle_fill}" '
        f'stroke="#FBF7F0" stroke-width="{2.5 if special=="anchor" else 2}"/>'
        f'<text class="pin-num" y="{num_y}" text-anchor="middle" '
        f'font-family="ui-rounded,sans-serif" font-size="{num_fontsize}" '
        f'font-weight="700" fill="#FBF7F0">{num}</text>'
        f'<text class="pin-label" y="{label_y}" text-anchor="middle" '
        f'font-family="sans-serif" font-size="{label_fontsize}" '
        f'fill="{label_color}"{label_fontweight}>{label}</text>'
        f'{sub_html}'
        f'</g>'
    )


def render_atlas_map(config: CourseConfig, active_pin: str, lesson_num: str, district_label: str) -> str:
    """Render the per-course atlas SVG + strip + label."""
    pins_svg = "\n    ".join(render_atlas_pin(p, active_pin) for p in config.atlas_pins)

    active_idx = _strip_index(lesson_num)
    strip_parts = []
    for i in range(config.total_lessons):
        cls = "ktown-strip-pin"
        if i == 0:
            cls += " ktown-strip-anchor"
        if i == active_idx:
            cls += " active"
        strip_parts.append(f'<li class="{cls}"></li>')
    strip_html = "\n    ".join(strip_parts)

    aria_label = f"{config.aria_lesson_word} {config.course_letter}{int(lesson_num)}, {district_label}."
    map_aria = f"{config.universe_name} {config.map_aria_word}: {config.course_letter}{int(lesson_num)}"
    map_title = f"{config.universe_name} {config.map_aria_word} · {config.course_letter}{int(lesson_num)}"
    map_desc = f"Stylised {config.map_desc_subject}. {district_label} highlighted."
    strip_emoji = config.strip_label_emoji or config.universe_emoji

    # Gradients
    def _grad(grad_id: str, stops: tuple) -> str:
        stop_xml = "".join(
            f'<stop offset="{off}" stop-color="{color}" stop-opacity="{opacity}"/>'
            for off, color, opacity in stops
        )
        return (
            f'<linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">{stop_xml}</linearGradient>'
        )

    defs_xml = (
        _grad(config.map_grad_id_primary, config.map_grad_primary_stops)
        + "\n      "
        + _grad(config.map_grad_id_secondary, config.map_grad_secondary_stops)
    )

    floor_rect = (
        f'<rect x="20" y="20" width="760" height="{config.map_floor_height}" rx="14" '
        f'fill="url(#{config.map_grad_id_primary})" stroke="{config.map_floor_stroke}" stroke-width="1"/>'
    )

    subtitle_xml = (
        f'<text x="400" y="38" text-anchor="middle" font-family="ui-rounded,sans-serif" '
        f'font-size="10" font-weight="700" letter-spacing="3" fill="#9D9389">'
        f'{config.map_subtitle}</text>'
    )

    # Dividers + optional italic labels
    divider_lines = []
    divider_labels = []
    for line_y, line_opacity, label_y, label_text in config.map_dividers:
        divider_lines.append(
            f'<line x1="40" y1="{line_y}" x2="780" y2="{line_y}" stroke="#5F5E5A" stroke-width="0.7" '
            f'stroke-dasharray="2,4" opacity="{line_opacity}"/>'
        )
        if label_y is not None and label_text:
            divider_labels.append(
                f'<text x="48" y="{label_y}" font-family="sans-serif" font-size="8" font-style="italic" '
                f'fill="#9D9389">{label_text}</text>'
            )
    dividers_xml = "\n    ".join(divider_lines + divider_labels)

    body_parts = [floor_rect, subtitle_xml]
    if config.map_decorations_svg:
        body_parts.append(config.map_decorations_svg)
    if dividers_xml:
        body_parts.append(dividers_xml)
    body_parts.append(pins_svg)
    body_xml = "\n    ".join(body_parts)

    return f"""<div class="ktown-map-wrap">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="{config.map_viewbox}" class="ktown-map" role="img" aria-label="{map_aria}">
    <title>{map_title}</title>
    <desc>{map_desc}</desc>
    <defs>
      {defs_xml}
    </defs>
    {body_xml}
  </svg>
  <ol class="ktown-strip" aria-hidden="true">
    {strip_html}
  </ol>
  <p class="ktown-strip-label">{strip_emoji} <strong>{district_label}</strong> <span>· {config.course_letter}{int(lesson_num)} of {config.total_lessons}</span><span class="visually-hidden">{aria_label}</span></p>
</div>"""


def render_concept_rail(config: CourseConfig, current_num: str) -> str:
    """Render the concept rail (left-side journey indicator)."""
    items = []
    found = False
    for num, label in config.rail_items:
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
        items.append(
            f'  <div class="{cls}"><span class="concept-rail-icon">{icon}</span>'
            f'<span>{label}</span>{here}</div>'
        )
    return f"""<aside class="concept-rail" aria-label="{config.course_code} module journey">
  <span class="concept-rail-title">{config.course_code} modules</span>
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


def render_lesson(spec: LessonSpec, config: CourseConfig) -> str:
    """Render one lesson HTML using the shared template + per-course config."""
    css = BASE_CSS + (spec.extra_css or "")
    map_html = render_atlas_map(config, spec.district_pin, spec.num, spec.district_label)
    rail_html = render_concept_rail(config, spec.num)

    sections_html = []
    for i, sec in enumerate(spec.sections):
        sections_html.append(_render_section(sec))
        if i in spec.pause_check_after_section:
            sections_html.append(_render_pause_check(spec.pause_check_after_section[i]))
    sections_block = "\n\n".join(sections_html)

    # Architecture diagram block — between hero and Nightmare opener; mandatory for
    # multi-component-system lessons; optional otherwise.
    if spec.architecture_svg:
        arch_caption = (
            f'<p class="arch-caption">{spec.architecture_caption}</p>'
            if spec.architecture_caption else ""
        )
        arch_block = f"""  <section class="arch-block">
    <span class="arch-tag">\U0001F4D0 Architecture diagram</span>
    <h2>How it actually wires together</h2>
    <div class="arch-svg">
{spec.architecture_svg}
    </div>
{arch_caption}
  </section>"""
    else:
        arch_block = ""

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
    analogy_subject = config.analogy_section_subject or config.district_kind
    analogy_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 3 · Analogy</span>
    <h2>The story for this {analogy_subject}</h2>
{spec.analogy_intro_html}
    <div class="translation-legend">
      <table>
        <thead><tr><th>In the story…</th><th>…in {config.legend_subject}</th></tr></thead>
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
    <h2>{config.real_world_heading}</h2>
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
    <span class="recap-badge">✓ Module {config.course_letter}{int(spec.num)} complete</span>
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
    <a href="#" class="brand"><span class="brand-mark">SG</span><span>Suvis Guru</span><span class="course"> · {config.course_code} · Module {config.course_letter}{int(spec.num)}</span></a>
    <span class="progress-pill">{config.course_letter}{int(spec.num)} · {spec.title_short}</span>
    <button class="theme-toggle" id="theme-toggle" type="button">\U0001F319 Dark</button>
  </div>
</header>

<p class="district-line">{config.universe_emoji} {config.universe_name} {config.district_kind}: <strong>{spec.district_label}</strong>.</p>

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

{arch_block}

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

<footer>Suvis Guru · {config.course_code} · Module {config.course_letter}{int(spec.num)} of {config.total_lessons} · grounded in {config.footer_grounded_url}</footer>

{combined_script}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Spec loader + animation attach + audit subprocess + main
# ---------------------------------------------------------------------------

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


def maybe_attach_animation(spec: LessonSpec, spec_path: str, course_code: str) -> None:
    spec_dir = os.path.dirname(os.path.abspath(spec_path))
    anim_path = os.path.join(spec_dir, "animations.py")
    if not os.path.exists(anim_path):
        return
    if spec_dir not in sys.path:
        sys.path.insert(0, spec_dir)
    spec_obj = importlib.util.spec_from_file_location(
        f"animations_{course_code.lower().replace('-', '_')}", anim_path
    )
    mod = importlib.util.module_from_spec(spec_obj)
    spec_obj.loader.exec_module(mod)
    animations = getattr(mod, "ANIMATIONS", {})
    if spec.num in animations and spec.animation is None:
        spec.animation = animations[spec.num]


def run_audit_subprocess(audit_basename: str) -> int:
    import subprocess
    audit_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), audit_basename)
    if not os.path.exists(audit_path):
        return 0
    result = subprocess.run([sys.executable, audit_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"\n>>> {audit_basename} FAILED <<<")
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return 1
    print(f"audit: {audit_basename} ✓ ({(result.stdout.splitlines() or [''])[0]})")
    return 0


def run_course_main(config: CourseConfig) -> None:
    """Generic main() entry for a course's thin generator file."""
    parser = argparse.ArgumentParser()
    parser.add_argument("specs", nargs="+", help=f"{config.course_code} spec modules")
    parser.add_argument("--out", default=ROOT)
    parser.add_argument("--no-audit", action="store_true")
    args = parser.parse_args()

    for spec_path in args.specs:
        mod = load_spec_module(spec_path)
        if not hasattr(mod, "LESSON"):
            sys.exit(f"{spec_path}: missing LESSON")
        spec: LessonSpec = mod.LESSON
        maybe_attach_animation(spec, spec_path, config.course_code)
        html = render_lesson(spec, config)
        out_path = os.path.join(
            args.out,
            f"preview-kubernetes-{config.html_filename_segment}-lesson-{spec.num}.html"
        )
        with open(out_path, "w") as f:
            f.write(html)
        print(f"wrote {out_path}")

    if args.no_audit:
        print("\n[--no-audit] skipped post-generation audits.")
        return
    print()
    if run_audit_subprocess(config.audit_script_basename):
        sys.exit(2)
