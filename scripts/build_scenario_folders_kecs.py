#!/usr/bin/env python3
"""K-ECS scenario folder builder — mirror of build_scenario_folders_kgke.py for K-ECS.

For each K-ECS module C1-C10, writes the four canonical files under
courses/kubernetes/aws-ecs/scenarios/{nn-slug}/.

Note: K-ECS is the non-Kubernetes companion course; per DECISIONS.md
2026-05-03 K-ECS entry, the URL prefix and folder under courses/kubernetes/
are platform-organizational, not a K8s claim. The brief + lesson.md make
the non-K8s designation prominent.
"""

import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENARIOS = os.path.join(ROOT, "courses/kubernetes/aws-ecs/scenarios")
LESSONS_DIR = os.path.join(ROOT, "scripts/lessons_kecs")
sys.path.insert(0, LESSONS_DIR)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from k8s_lesson_generator import LessonSpec  # noqa: E402

LESSON_META = {
    "01": ("c1-ecs-architecture", "Module C1 · ECS Architecture", "C1 · ECS Architecture — Cluster, Service, Task, Task Definition, Launch Types"),
    "02": ("c2-task-definitions-and-containers", "Module C2 · Task Definitions and Containers", "C2 · Task Definitions and Containers"),
    "03": ("c3-ecs-networking", "Module C3 · ECS Networking", "C3 · ECS Networking — Network Modes, Service Connect, ALB/NLB, VPC Lattice"),
    "04": ("c4-iam-and-security", "Module C4 · IAM and Security", "C4 · IAM and Security — Roles, Secrets, KMS, ECR, VPC Endpoints"),
    "05": ("c5-ecs-storage", "Module C5 · ECS Storage", "C5 · ECS Storage — Ephemeral, Bind, Docker, EFS, FSx"),
    "06": ("c6-deployment-and-scaling", "Module C6 · Deployment and Scaling", "C6 · ECS Deployment and Scaling"),
    "07": ("c7-ecs-observability", "Module C7 · ECS Observability", "C7 · ECS Observability — Container Insights, ECS Exec, FireLens, ADOT, X-Ray"),
    "08": ("c8-ecs-anywhere", "Module C8 · ECS Anywhere and Hybrid", "C8 · ECS Anywhere and Hybrid — On-Prem and Edge Capacity"),
    "09": ("c9-troubleshooting", "Module C9 · ECS Troubleshooting", "C9 · ECS Troubleshooting — Stuck Tasks, Stopped Reasons, Deploy Failures"),
    "10": ("c10-capstone", "Module C10 · Capstone", "C10 · Capstone — The Reference Multi-Service Fargate Harbor"),
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


def emit_brief(num, slug, module, title, spec):
    outcomes = [f"Learner can explain {html_to_md(s.h2)[0].lower()}{html_to_md(s.h2)[1:]}." for s in spec.sections[:3]]
    stamp = html_to_md(spec.stamp_html)
    scenario_lines = [html_to_md(s.body).split('.')[0] + '.' for s in spec.scenarios[:4]]
    metaphor = f"K-Harbor · {spec.district_label} — {html_to_md(spec.analogy_intro_html)[:200]}"
    parts = [
        f"# Intake brief — C{int(num)}, K-ECS (non-Kubernetes companion course)",
        f"# Topic: {title}",
        f"# {module}",
        "",
        "lesson:",
        f"  title: '{yaml_escape(title)}'",
        f"  slug: '{slug}'",
        "  domain: 'kubernetes'",
        "  course_slug: 'aws-ecs'",
        f"  position: {num}",
        "  granularity: 'module'",
        "  brief_drafted_on: '2026-05-03'",
        f"  central_metaphor: '{yaml_escape(metaphor)}'",
        f"  module: '{yaml_escape(module)}'",
        "",
        "course_disclaimer:",
        "  non_kubernetes: true",
        "  rationale: 'AWS ECS uses its own APIs (Cluster / Service / Task / Task Definition / Capacity Provider / Service Connect) — not K8s APIs. Included as a companion to K-EKS because organisations frequently choose between or coexist with EKS.'",
        "",
        "learner_profile:",
        "  prerequisites:",
        "    - 'AWS basics: IAM, VPC, EC2, ALB, ECR, CloudWatch, Secrets Manager, KMS.'",
        "    - 'Container fundamentals: Docker, image registries, container lifecycle.'",
        f"    - 'K-ECS modules 1-{int(num) - 1 if int(num) > 1 else 0} (cumulative).'",
        "  assumed_zero_knowledge_of:",
        "    - 'Kubernetes Pods / Deployments / Services / Ingress / RBAC / CRDs.'",
        "",
        "learning_outcomes:",
    ]
    for o in outcomes:
        parts.append(f"  - '{yaml_escape(o)}'")
    parts += ["", "sections:"]
    for s in spec.sections:
        parts.append(f"  - '{yaml_escape(html_to_md(s.h2))}'")
    parts += ["", "section_5_real_world:", "  count: 4", "  examples:"]
    for s in scenario_lines:
        parts.append(f"    - '{yaml_escape(s)}'")
    parts += [
        "",
        "section_6_animated_svg:",
        "  modes_count: 1-2",
        f"  description: 'See preview-kubernetes-ecs-lesson-{num}.html Section 6 for the live animation.'",
        "",
        "section_7_flashcards_quiz:",
        f"  flashcards: {len(spec.flashcards)}",
        f"  quiz_questions: {len(spec.quizzes)}",
        "",
        "shared_artifacts:",
        f"  preview_page: {{ file: '/preview-kubernetes-ecs-lesson-{num}.html' }}",
        "  lesson_md: { file: 'lesson.md' }",
        f"  flashcards: {{ file: 'flashcards.yaml', count: {len(spec.flashcards)} }}",
        f"  quiz: {{ file: 'quiz.yaml', count: {len(spec.quizzes)} }}",
        "",
        "bar:",
        f"  - '{yaml_escape(stamp)}'",
        "",
        "fact_check_anchors:",
        "  - 'https://docs.aws.amazon.com/ecs/'",
        "  - 'https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html'",
        "  - 'https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/intro.html'",
    ]
    return "\n".join(parts) + "\n"


def emit_lesson_md(num, title, module, spec):
    out = [
        f"# K-ECS C{int(num)} — {title}",
        "",
        f"> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)",
        f"> {module}",
        f"> Companion preview: `/preview-kubernetes-ecs-lesson-{num}.html`.",
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
        "## Before / After", "",
        f"**Before.** {html_to_md(spec.before_after_before)}", "",
        f"**After.** {html_to_md(spec.before_after_after)}", "",
        html_to_md(spec.before_after_caption), "",
        "## Analogy — the K-Harbor pier", "",
        html_to_md(spec.analogy_intro_html), "",
        "**Translation legend.**", "",
        "| In the story… | …in ECS / AWS |",
        "|---|---|",
    ]
    for story, k8s in spec.translation_rows:
        out.append(f"| {html_to_md(story)} | {html_to_md(k8s)} |")
    out += [
        "",
        f"⚠️ *Analogy stops here:* {html_to_md(spec.analogy_stops)}", "",
        "## ELI5 / ELI10", "",
        f"**ELI5.** {html_to_md(spec.eli5)}", "",
        f"**ELI10.** {html_to_md(spec.eli10)}", "",
        "## Real-world scenarios", "",
    ]
    for s in spec.scenarios:
        out.append(f"- **{s.name}.** {html_to_md(s.body)}")
    out += ["", "## Common misconceptions", ""]
    for m in spec.misconceptions:
        out.append(f"- **Myth:** {html_to_md(m.myth)}")
        out.append(f"  **Truth:** {html_to_md(m.truth)}")
    out += [
        "", "## Recap", "",
        html_to_md(spec.recap_lead), "",
        html_to_md(spec.recap_next), "",
        "## Flashcards and quiz", "",
        f"See `flashcards.yaml` ({len(spec.flashcards)} cards) and `quiz.yaml` ({len(spec.quizzes)} questions).",
    ]
    return "\n".join(out) + "\n"


def emit_flashcards(spec):
    out = [f"# Flashcards — K-ECS C (count: {len(spec.flashcards)})", "", "cards:"]
    for i, f in enumerate(spec.flashcards, start=1):
        out.append(f"  - id: {i}")
        out.append("    front: |")
        out.extend(f"      {line}" for line in html_to_md(f.front).splitlines())
        out.append("    back: |")
        out.extend(f"      {line}" for line in html_to_md(f.back).splitlines())
        out.append("")
    return "\n".join(out)


def emit_quiz(spec):
    out = [f"# Quiz — K-ECS C (count: {len(spec.quizzes)})", "", "questions:"]
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


def main():
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
        print(f"  C{int(num)}: wrote {folder}")
    print(f"\nDone. {len(LESSON_META)} folders.")


if __name__ == "__main__":
    main()
