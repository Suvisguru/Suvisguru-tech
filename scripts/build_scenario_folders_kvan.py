#!/usr/bin/env python3
"""K-VAN scenario folder builder — mirror of build_scenario_folders.py for K-VAN.

For each K-VAN lesson V1-V11, writes the four canonical files under
courses/kubernetes/vanilla-kubernetes/scenarios/{nn-slug}/:

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
SCENARIOS = os.path.join(ROOT, "courses/kubernetes/vanilla-kubernetes/scenarios")
LESSONS_DIR = os.path.join(ROOT, "scripts/lessons_kvan")
sys.path.insert(0, LESSONS_DIR)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from k8s_lesson_generator import LessonSpec  # noqa: E402

LESSON_META = {
    "01": ("v1-architecture-design", "Module V1 · Production Architecture", "V1 · Production Architecture Design for Self-Managed K8s"),
    "02": ("v2-os-and-node-prep", "Module V2 · OS and Node Preparation", "V2 · OS and Node Preparation for kubeadm"),
    "03": ("v3-kubeadm-bootstrap", "Module V3 · kubeadm Cluster Bootstrap", "V3 · kubeadm Cluster Bootstrap End-to-End"),
    "04": ("v4-cni-installation", "Module V4 · CNI and Networking", "V4 · CNI Installation and Cluster Networking"),
    "05": ("v5-core-add-ons", "Module V5 · Core Add-ons", "V5 · Core Add-ons (CoreDNS, Gateway, cert-manager, CSI, observability, GitOps)"),
    "06": ("v6-cluster-config", "Module V6 · Cluster Configuration", "V6 · Cluster Configuration (apiserver, kubelet, scheduler, kube-proxy)"),
    "07": ("v7-etcd-production", "Module V7 · etcd Production", "V7 · etcd Production-Grade (Raft, Snapshots, Defrag, DR)"),
    "08": ("v8-upgrades-and-patching", "Module V8 · Upgrades and Patching", "V8 · Upgrades and Patching (kubeadm, version skew, rollback)"),
    "09": ("v9-security-hardening", "Module V9 · Security Hardening", "V9 · Security Hardening (CIS, RBAC, PSA, supply-chain, runtime)"),
    "10": ("v10-troubleshooting", "Module V10 · Advanced Troubleshooting", "V10 · Advanced Vanilla Troubleshooting (full disaster scenarios)"),
    "11": ("v11-capstone", "Module V11 · Capstone", "V11 · Capstone — Build, Harden, Back Up, Upgrade, Recover an HA Cluster"),
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
    metaphor = f"K-Frontier · {spec.district_label} — {html_to_md(spec.analogy_intro_html)[:200]}"

    parts = [
        f"# Intake brief — V{int(num)}, K-VAN",
        f"# Topic: {title}",
        f"# {module}",
        "",
        "lesson:",
        f"  title: '{yaml_escape(title)}'",
        f"  slug: '{slug}'",
        "  domain: 'kubernetes'",
        "  course_slug: 'vanilla-kubernetes'",
        f"  position: {num}",
        "  granularity: 'module'",
        "  brief_drafted_on: '2026-05-03'",
        f"  central_metaphor: '{yaml_escape(metaphor)}'",
        f"  module: '{yaml_escape(module)}'",
        "",
        "learner_profile:",
        "  prerequisites:",
        "    - 'K-COM curriculum complete (L01-L44).'",
        f"    - 'K-VAN modules 1-{int(num) - 1 if int(num) > 1 else 0} (cumulative).'",
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
        f"  description: 'See preview-kubernetes-vanilla-lesson-{num}.html Section 6 for the live animation.'",
        "",
        "section_7_flashcards_quiz:",
        f"  flashcards: {len(spec.flashcards)}",
        f"  quiz_questions: {len(spec.quizzes)}",
        "",
        "shared_artifacts:",
        f"  preview_page: {{ file: '/preview-kubernetes-vanilla-lesson-{num}.html' }}",
        "  lesson_md: { file: 'lesson.md' }",
        f"  flashcards: {{ file: 'flashcards.yaml', count: {len(spec.flashcards)} }}",
        f"  quiz: {{ file: 'quiz.yaml', count: {len(spec.quizzes)} }}",
        "",
        "bar:",
        f"  - '{yaml_escape(stamp)}'",
        "",
        "fact_check_anchors:",
        "  - 'https://kubernetes.io/docs/'",
        "  - 'https://github.com/kubernetes/kubeadm'",
    ]
    return "\n".join(parts) + "\n"


def emit_lesson_md(num: str, title: str, module: str, spec: LessonSpec) -> str:
    out = [
        f"# K-VAN V{int(num)} — {title}",
        "",
        f"> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)",
        f"> {module}",
        f"> Companion preview: `/preview-kubernetes-vanilla-lesson-{num}.html`.",
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
        "## Analogy — the K-Frontier site",
        "",
        html_to_md(spec.analogy_intro_html),
        "",
        "**Translation legend.**",
        "",
        "| In the story… | …in vanilla Kubernetes |",
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
    out = [f"# Flashcards — K-VAN V (count: {len(spec.flashcards)})", "", "cards:"]
    for i, f in enumerate(spec.flashcards, start=1):
        out.append(f"  - id: {i}")
        out.append("    front: |")
        out.extend(f"      {line}" for line in html_to_md(f.front).splitlines())
        out.append("    back: |")
        out.extend(f"      {line}" for line in html_to_md(f.back).splitlines())
        out.append("")
    return "\n".join(out)


def emit_quiz(spec: LessonSpec) -> str:
    out = [f"# Quiz — K-VAN V (count: {len(spec.quizzes)})", "", "questions:"]
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
        print(f"  V{int(num)}: wrote {folder}")
    print(f"\nDone. {len(LESSON_META)} folders.")


if __name__ == "__main__":
    main()
