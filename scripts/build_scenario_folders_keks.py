#!/usr/bin/env python3
"""K-EKS scenario folder builder — mirror of build_scenario_folders_kvan.py for K-EKS.

For each K-EKS module E1-E11, writes the four canonical files under
courses/kubernetes/aws-eks/scenarios/{nn-slug}/:

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
SCENARIOS = os.path.join(ROOT, "courses/kubernetes/aws-eks/scenarios")
LESSONS_DIR = os.path.join(ROOT, "scripts/lessons_keks")
sys.path.insert(0, LESSONS_DIR)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from k8s_lesson_generator import LessonSpec  # noqa: E402

LESSON_META = {
    "01": ("e1-eks-architecture", "Module E1 · EKS Architecture", "E1 · EKS Architecture and Shared Responsibility"),
    "02": ("e2-auto-mode", "Module E2 · EKS Auto Mode", "E2 · EKS Auto Mode — AWS Picks the Nodes"),
    "03": ("e3-aws-networking", "Module E3 · AWS Networking", "E3 · AWS Networking for EKS (VPC CNI, ALB/NLB, Gateway API, VPC Lattice)"),
    "04": ("e4-identity-and-access", "Module E4 · Identity and Access", "E4 · Identity and Access (Access Entries, IRSA, Pod Identity)"),
    "05": ("e5-eks-storage", "Module E5 · EKS Storage", "E5 · EKS Storage (EBS, EFS, FSx, S3 Mountpoint)"),
    "06": ("e6-compute-and-autoscaling", "Module E6 · Compute and Autoscaling", "E6 · EKS Compute and Autoscaling (Karpenter, Spot, Graviton, GPU)"),
    "07": ("e7-eks-security", "Module E7 · EKS Security", "E7 · EKS Security (KMS, GuardDuty, ECR signing, Bottlerocket, audit)"),
    "08": ("e8-eks-observability", "Module E8 · EKS Observability", "E8 · EKS Observability (Container Insights, AMP, AMG, ADOT, X-Ray, control-plane logs)"),
    "09": ("e9-upgrades-and-ops", "Module E9 · Upgrades and Operations", "E9 · EKS Upgrades and Operations"),
    "10": ("e10-troubleshooting", "Module E10 · EKS Troubleshooting", "E10 · EKS Troubleshooting (AWS-Specific)"),
    "11": ("e11-capstone", "Module E11 · Capstone Tower", "E11 · Capstone — Multi-AZ EKS Auto Mode Tower with Everything"),
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
    metaphor = f"K-Skyline · {spec.district_label} — {html_to_md(spec.analogy_intro_html)[:200]}"

    parts = [
        f"# Intake brief — E{int(num)}, K-EKS",
        f"# Topic: {title}",
        f"# {module}",
        "",
        "lesson:",
        f"  title: '{yaml_escape(title)}'",
        f"  slug: '{slug}'",
        "  domain: 'kubernetes'",
        "  course_slug: 'aws-eks'",
        f"  position: {num}",
        "  granularity: 'module'",
        "  brief_drafted_on: '2026-05-03'",
        f"  central_metaphor: '{yaml_escape(metaphor)}'",
        f"  module: '{yaml_escape(module)}'",
        "",
        "learner_profile:",
        "  prerequisites:",
        "    - 'K-COM curriculum complete (L01-L44).'",
        "    - 'AWS basics: VPC, IAM, EC2, S3, CloudWatch.'",
        f"    - 'K-EKS modules 1-{int(num) - 1 if int(num) > 1 else 0} (cumulative).'",
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
        f"  description: 'See preview-kubernetes-eks-lesson-{num}.html Section 6 for the live animation.'",
        "",
        "section_7_flashcards_quiz:",
        f"  flashcards: {len(spec.flashcards)}",
        f"  quiz_questions: {len(spec.quizzes)}",
        "",
        "shared_artifacts:",
        f"  preview_page: {{ file: '/preview-kubernetes-eks-lesson-{num}.html' }}",
        "  lesson_md: { file: 'lesson.md' }",
        f"  flashcards: {{ file: 'flashcards.yaml', count: {len(spec.flashcards)} }}",
        f"  quiz: {{ file: 'quiz.yaml', count: {len(spec.quizzes)} }}",
        "",
        "bar:",
        f"  - '{yaml_escape(stamp)}'",
        "",
        "fact_check_anchors:",
        "  - 'https://docs.aws.amazon.com/eks/latest/userguide/'",
        "  - 'https://docs.aws.amazon.com/eks/latest/best-practices/'",
        "  - 'https://kubernetes.io/docs/'",
    ]
    return "\n".join(parts) + "\n"


def emit_lesson_md(num: str, title: str, module: str, spec: LessonSpec) -> str:
    out = [
        f"# K-EKS E{int(num)} — {title}",
        "",
        f"> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)",
        f"> {module}",
        f"> Companion preview: `/preview-kubernetes-eks-lesson-{num}.html`.",
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
        "## Analogy — the K-Skyline floor",
        "",
        html_to_md(spec.analogy_intro_html),
        "",
        "**Translation legend.**",
        "",
        "| In the story… | …in EKS / AWS |",
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
    out = [f"# Flashcards — K-EKS E (count: {len(spec.flashcards)})", "", "cards:"]
    for i, f in enumerate(spec.flashcards, start=1):
        out.append(f"  - id: {i}")
        out.append("    front: |")
        out.extend(f"      {line}" for line in html_to_md(f.front).splitlines())
        out.append("    back: |")
        out.extend(f"      {line}" for line in html_to_md(f.back).splitlines())
        out.append("")
    return "\n".join(out)


def emit_quiz(spec: LessonSpec) -> str:
    out = [f"# Quiz — K-EKS E (count: {len(spec.quizzes)})", "", "questions:"]
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
        print(f"  E{int(num)}: wrote {folder}")
    print(f"\nDone. {len(LESSON_META)} folders.")


if __name__ == "__main__":
    main()
