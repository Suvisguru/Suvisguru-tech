#!/usr/bin/env python3
"""K-AKS scenario folder builder — mirror of build_scenario_folders_keks.py for K-AKS.

For each K-AKS module A1-A11, writes the four canonical files under
courses/kubernetes/azure-aks/scenarios/{nn-slug}/:

  - brief.yaml  intake brief
  - lesson.md   lesson copy
  - flashcards.yaml
  - quiz.yaml
"""

import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENARIOS = os.path.join(ROOT, "courses/kubernetes/azure-aks/scenarios")
LESSONS_DIR = os.path.join(ROOT, "scripts/lessons_kaks")
sys.path.insert(0, LESSONS_DIR)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from k8s_lesson_generator import LessonSpec  # noqa: E402

LESSON_META = {
    "01": ("a1-aks-architecture", "Module A1 · AKS Architecture", "A1 · AKS Architecture and Shared Responsibility"),
    "02": ("a2-entra-and-workload-identity", "Module A2 · Entra and Workload Identity", "A2 · Azure Identity and Access (Entra ID, Workload Identity, Azure RBAC)"),
    "03": ("a3-aks-networking", "Module A3 · AKS Networking", "A3 · AKS Networking (Azure CNI, AGC, NetworkPolicy, private clusters)"),
    "04": ("a4-aks-storage", "Module A4 · AKS Storage", "A4 · AKS Storage (Disks, Files, NetApp, Blob, Container Storage)"),
    "05": ("a5-aks-scaling", "Module A5 · AKS Scaling", "A5 · AKS Scaling (Cluster Autoscaler, NAP, KEDA, Spot, GPU, ARM, Confidential)"),
    "06": ("a6-aks-security", "Module A6 · AKS Security", "A6 · AKS Security (Defender, Policy, Image Cleaner, FIPS, Confidential Containers)"),
    "07": ("a7-aks-observability", "Module A7 · AKS Observability", "A7 · AKS Observability (Container Insights, AMP, AMG, ADOT, App Insights)"),
    "08": ("a8-aks-add-ons-and-platform", "Module A8 · Add-ons and Platform", "A8 · AKS Add-ons and Platform Features"),
    "09": ("a9-upgrades-and-ops", "Module A9 · Upgrades and Operations", "A9 · AKS Upgrades and Operations"),
    "10": ("a10-troubleshooting", "Module A10 · AKS Troubleshooting", "A10 · AKS Troubleshooting (Azure-Specific)"),
    "11": ("a11-capstone", "Module A11 · Capstone Campus", "A11 · Capstone — Private AKS Automatic Reference Campus with Everything"),
}


def load_spec(num: str) -> LessonSpec:
    path = os.path.join(LESSONS_DIR, f"lesson{num}.py")
    spec_obj = importlib.util.spec_from_file_location(f"lesson{num}", path)
    mod = importlib.util.module_from_spec(spec_obj)
    spec_obj.loader.exec_module(mod)
    return mod.LESSON


def yaml_escape(s: str) -> str:
    return s.replace("'", "''")


def html_to_md(s: str) -> str:
    s = re.sub(r'<code>(.*?)</code>', r'`\1`', s, flags=re.DOTALL)
    s = re.sub(r'<strong>(.*?)</strong>', r'**\1**', s, flags=re.DOTALL)
    s = re.sub(r'<em>(.*?)</em>', r'*\1*', s, flags=re.DOTALL)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', s, flags=re.DOTALL)
    s = re.sub(r'</?(ul|ol|p|h\d|div|span|table|thead|tbody|tr|th|td|a|pre)[^>]*>', '', s, flags=re.IGNORECASE)
    s = re.sub(r'<[^>]+>', '', s)
    s = (s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
           .replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' '))
    return s.strip()


def emit_brief(num: str, slug: str, module: str, title: str, spec: LessonSpec) -> str:
    outcomes = [f"Learner can explain {html_to_md(s.h2)[0].lower()}{html_to_md(s.h2)[1:]}." for s in spec.sections[:3]]
    stamp = html_to_md(spec.stamp_html)
    scenario_lines = [html_to_md(s.body).split('.')[0] + '.' for s in spec.scenarios[:4]]
    metaphor = f"K-Campus · {spec.district_label} — {html_to_md(spec.analogy_intro_html)[:200]}"

    parts = [
        f"# Intake brief — A{int(num)}, K-AKS",
        f"# Topic: {title}",
        f"# {module}",
        "",
        "lesson:",
        f"  title: '{yaml_escape(title)}'",
        f"  slug: '{slug}'",
        "  domain: 'kubernetes'",
        "  course_slug: 'azure-aks'",
        f"  position: {num}",
        "  granularity: 'module'",
        "  brief_drafted_on: '2026-05-03'",
        f"  central_metaphor: '{yaml_escape(metaphor)}'",
        f"  module: '{yaml_escape(module)}'",
        "",
        "learner_profile:",
        "  prerequisites:",
        "    - 'K-COM curriculum complete (L01-L44).'",
        "    - 'Azure basics: Entra ID, VNet, VMSS, LB, Disks/Files, Monitor, Key Vault.'",
        f"    - 'K-AKS modules 1-{int(num) - 1 if int(num) > 1 else 0} (cumulative).'",
        "  assumed_zero_knowledge_of: []",
        "",
        "learning_outcomes:",
    ]
    for o in outcomes:
        parts.append(f"  - '{yaml_escape(o)}'")
    parts += [
        "",
        "sections:",
    ]
    for s in spec.sections:
        parts.append(f"  - '{yaml_escape(html_to_md(s.h2))}'")
    parts += [
        "",
        "section_5_real_world:",
        "  count: 4",
        "  examples:",
    ]
    for s in scenario_lines:
        parts.append(f"    - '{yaml_escape(s)}'")
    parts += [
        "",
        "section_6_animated_svg:",
        "  modes_count: 1-3",
        f"  description: 'See preview-kubernetes-aks-lesson-{num}.html Section 6 for the live animation.'",
        "",
        "section_7_flashcards_quiz:",
        f"  flashcards: {len(spec.flashcards)}",
        f"  quiz_questions: {len(spec.quizzes)}",
        "",
        "shared_artifacts:",
        f"  preview_page: {{ file: '/preview-kubernetes-aks-lesson-{num}.html' }}",
        "  lesson_md: { file: 'lesson.md' }",
        f"  flashcards: {{ file: 'flashcards.yaml', count: {len(spec.flashcards)} }}",
        f"  quiz: {{ file: 'quiz.yaml', count: {len(spec.quizzes)} }}",
        "",
        "bar:",
        f"  - '{yaml_escape(stamp)}'",
        "",
        "fact_check_anchors:",
        "  - 'https://learn.microsoft.com/azure/aks/'",
        "  - 'https://learn.microsoft.com/azure/aks/best-practices'",
        "  - 'https://kubernetes.io/docs/'",
    ]
    return "\n".join(parts) + "\n"


def emit_lesson_md(num: str, title: str, module: str, spec: LessonSpec) -> str:
    out = [
        f"# K-AKS A{int(num)} — {title}",
        "",
        f"> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)",
        f"> {module}",
        f"> Companion preview: `/preview-kubernetes-aks-lesson-{num}.html`.",
        "",
        "---",
        "",
        f"**🎯 If you remember nothing else:** {html_to_md(spec.stamp_html)}",
        "",
    ]
    for i, sec in enumerate(spec.sections, start=1):
        out.append(f"## {i}. {html_to_md(sec.h2)}")
        out.append("")
        out.append(html_to_md(sec.body_html))
        out.append("")
    out += [
        "## Before / After",
        "",
        f"**Before.** {html_to_md(spec.before_after_before)}",
        "",
        f"**After.** {html_to_md(spec.before_after_after)}",
        "",
        html_to_md(spec.before_after_caption),
        "",
        "## Analogy — the K-Campus wing",
        "",
        html_to_md(spec.analogy_intro_html),
        "",
        "**Translation legend.**",
        "",
        "| In the story… | …in AKS / Azure |",
        "|---|---|",
    ]
    for story, k8s in spec.translation_rows:
        out.append(f"| {html_to_md(story)} | {html_to_md(k8s)} |")
    out += [
        "",
        f"⚠️ *Analogy stops here:* {html_to_md(spec.analogy_stops)}",
        "",
        "## ELI5 / ELI10",
        "",
        f"**ELI5.** {html_to_md(spec.eli5)}",
        "",
        f"**ELI10.** {html_to_md(spec.eli10)}",
        "",
        "## Real-world scenarios",
        "",
    ]
    for s in spec.scenarios:
        out.append(f"- **{s.name}.** {html_to_md(s.body)}")
    out += [
        "",
        "## Common misconceptions",
        "",
    ]
    for m in spec.misconceptions:
        out.append(f"- **Myth:** {html_to_md(m.myth)}")
        out.append(f"  **Truth:** {html_to_md(m.truth)}")
    out += [
        "",
        "## Recap",
        "",
        html_to_md(spec.recap_lead),
        "",
        html_to_md(spec.recap_next),
        "",
        "## Flashcards and quiz",
        "",
        f"See `flashcards.yaml` ({len(spec.flashcards)} cards) and `quiz.yaml` ({len(spec.quizzes)} questions).",
    ]
    return "\n".join(out) + "\n"


def emit_flashcards(spec: LessonSpec) -> str:
    out = [f"# Flashcards — K-AKS A (count: {len(spec.flashcards)})", "", "cards:"]
    for i, f in enumerate(spec.flashcards, start=1):
        out.append(f"  - id: {i}")
        out.append("    front: |")
        out.extend(f"      {line}" for line in html_to_md(f.front).splitlines())
        out.append("    back: |")
        out.extend(f"      {line}" for line in html_to_md(f.back).splitlines())
        out.append("")
    return "\n".join(out)


def emit_quiz(spec: LessonSpec) -> str:
    out = [f"# Quiz — K-AKS A (count: {len(spec.quizzes)})", "", "questions:"]
    for i, q in enumerate(spec.quizzes, start=1):
        out.append(f"  - id: {i}")
        if q.cyoa:
            out.append("    type: 'cyoa'")
        out.append("    prompt: |")
        out.extend(f"      {line}" for line in html_to_md(q.prompt).splitlines())
        out.append("    answer: |")
        out.extend(f"      {line}" for line in html_to_md(q.answer).splitlines())
        out.append("")
    return "\n".join(out)


def main() -> None:
    for num, (slug, module, title) in LESSON_META.items():
        spec = load_spec(num)
        folder = os.path.join(SCENARIOS, slug)
        os.makedirs(folder, exist_ok=True)
        files = {
            "brief.yaml": emit_brief(num, slug, module, title, spec),
            "lesson.md": emit_lesson_md(num, title, module, spec),
            "flashcards.yaml": emit_flashcards(spec),
            "quiz.yaml": emit_quiz(spec),
        }
        for fname, content in files.items():
            with open(os.path.join(folder, fname), "w") as f:
                f.write(content)
        print(f"  A{int(num)}: wrote {folder}")
    print(f"\nDone. {len(LESSON_META)} folders.")


if __name__ == "__main__":
    main()
