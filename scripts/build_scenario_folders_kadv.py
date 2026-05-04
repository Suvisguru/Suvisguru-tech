#!/usr/bin/env python3
"""K-ADV-* scenario folder builder — handles all 5 K-ADV courses.

Per course: writes brief.yaml + lesson.md + flashcards.yaml + quiz.yaml under
courses/kubernetes/{course-folder}/scenarios/{nn-slug}/ for every K-ADV module.
"""

import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from k8s_lesson_generator import LessonSpec  # noqa: E402

# Per-course config: (lesson-dir-suffix, course-folder, course-code, course-letter, universe)
COURSES = [
    ("sec", "advanced-security", "K-ADV-SEC", "S", "K-Citadel", "kubernetes-security"),
    ("net", "advanced-networking", "K-ADV-NET", "N", "K-Highway", "kubernetes-networking"),
    ("pe", "advanced-platform-engineering", "K-ADV-PE", "P", "K-Workshop", "platform-engineering"),
    ("ai", "advanced-ai-ml-gpus", "K-ADV-AI", "I", "K-Observatory", "kubernetes-ai-ml"),
    ("dr", "advanced-disaster-recovery", "K-ADV-DR", "D", "K-Lifeboat", "kubernetes-dr"),
]

LESSON_META = {
    "sec": {
        "01": ("s1-threat-modeling-zero-trust-tenancy", "Module S1 · Threat Modeling, Zero-Trust, Tenancy", "S1 · Threat Modeling, Zero-Trust, Multi-Tenant Isolation"),
        "02": ("s2-rbac-at-scale", "Module S2 · RBAC at Scale", "S2 · RBAC Design at Scale"),
        "03": ("s3-admission-policy", "Module S3 · Admission Policy", "S3 · Admission Policy Architecture"),
        "04": ("s4-psa-runtime", "Module S4 · PSA + Runtime", "S4 · PSA Restricted + Runtime Detection"),
        "05": ("s5-signing-sbom-slsa-vex", "Module S5 · Signing + SBOM + SLSA + VEX", "S5 · Image Signing, SBOM, SLSA, in-toto, VEX"),
        "06": ("s6-secrets-mtls-mesh", "Module S6 · Secrets + mTLS + Mesh", "S6 · Secrets + mTLS + Service Mesh Security"),
        "07": ("s7-audit-compliance-ir", "Module S7 · Audit + Compliance + IR", "S7 · Audit Log Analytics + Compliance Evidence + IR"),
        "08": ("s8-capstone-defendable-platform", "Module S8 · Capstone", "S8 · Capstone — Defendable Regulated Platform"),
    },
    "net": {
        "01": ("n1-cni-ebpf-bgp", "Module N1 · CNI + eBPF + BGP", "N1 · CNI Internals, eBPF, BGP at Scale"),
        "02": ("n2-gateway-api", "Module N2 · Gateway API", "N2 · Gateway API at Fleet Scale"),
        "03": ("n3-multi-cluster-networking", "Module N3 · Multi-Cluster Networking", "N3 · Multi-Cluster Networking"),
        "04": ("n4-mesh-dns-ipv6", "Module N4 · Mesh + DNS + IPv6", "N4 · Service Mesh + DNS + IPv6"),
        "05": ("n5-networkpolicy-egress-private", "Module N5 · NetworkPolicy + Egress + Private", "N5 · NetworkPolicy + Egress + Private + Hybrid"),
        "06": ("n6-packet-tracing-perf", "Module N6 · Packet Tracing + Perf", "N6 · Packet Tracing + Performance Tuning"),
        "07": ("n7-capstone-multi-region", "Module N7 · Capstone", "N7 · Capstone — Multi-Cluster Network"),
    },
    "pe": {
        "01": ("p1-idp-foundations", "Module P1 · IDP Foundations", "P1 · IDP Foundations + Golden Paths + Self-Service Namespaces"),
        "02": ("p2-backstage", "Module P2 · Backstage", "P2 · Backstage Deep Dive"),
        "03": ("p3-crossplane-v2", "Module P3 · Crossplane v2", "P3 · Crossplane v2"),
        "04": ("p4-applicationsets-guardrails", "Module P4 · ApplicationSets + Guardrails", "P4 · Argo CD ApplicationSets + OPA / Kyverno Guardrails"),
        "05": ("p5-tenant-onboarding-cost", "Module P5 · Tenant Onboarding + Cost", "P5 · Tenant Onboarding + Resource Templates + Cost Controls"),
        "06": ("p6-workload-abstractions", "Module P6 · Workload Abstractions", "P6 · Workload Abstractions: Score, OAM, Radius, Humanitec"),
        "07": ("p7-slos-chargeback", "Module P7 · SLOs + Chargeback", "P7 · Platform SLOs + Chargeback / Showback"),
        "08": ("p8-capstone-idp", "Module P8 · Capstone IDP", "P8 · Capstone — Self-Service IDP"),
    },
    "ai": {
        "01": ("i1-gpu-dra-mig", "Module I1 · GPU + DRA + MIG", "I1 · GPU Nodes + Device Plugin + GPU Operator + MIG + DRA"),
        "02": ("i2-kueue-volcano", "Module I2 · Kueue + Volcano", "I2 · Kueue + MultiKueue + Volcano Gang Scheduling"),
        "03": ("i3-ray-kubeflow-kserve", "Module I3 · Ray + Kubeflow + KServe", "I3 · Ray + Kubeflow + KServe + JobSet"),
        "04": ("i4-llm-serving", "Module I4 · LLM Serving", "I4 · LLM Serving — vLLM, TGI, Triton, NIM, llm-d"),
        "05": ("i5-ai-gateway", "Module I5 · AI Gateway", "I5 · AI / LLM Gateway Patterns"),
        "06": ("i6-rdma-storage", "Module I6 · RDMA + Storage", "I6 · RDMA / EFA + Storage Throughput + JuiceFS / Alluxio + OCI Artifacts"),
        "07": ("i7-gpu-sharing-tenant-cost", "Module I7 · GPU Sharing + Tenant + Cost", "I7 · GPU Sharing + Multi-Tenant Security + Cost Optimization"),
        "08": ("i8-capstone-ai-platform", "Module I8 · Capstone AI Platform", "I8 · Capstone — Production AI Inference Platform"),
    },
    "dr": {
        "01": ("d1-etcd-velero-k10-cloudcasa", "Module D1 · etcd + Velero + K10 + CloudCasa", "D1 · etcd Backup + Velero + Kasten K10 + CloudCasa"),
        "02": ("d2-gitops-recovery", "Module D2 · GitOps Recovery", "D2 · GitOps-Driven Recovery + Cluster Rebuild"),
        "03": ("d3-cross-region-dr", "Module D3 · Cross-Region DR", "D3 · Cross-Region DR + RPO / RTO + Restore Testing"),
        "04": ("d4-secrets-dns-stateful-managed-dr", "Module D4 · Secrets + DNS + Stateful + Managed DR", "D4 · Secret + DNS + Stateful + Managed-Service DR"),
        "05": ("d5-capstone-total-loss-drill", "Module D5 · Capstone Total-Loss Drill", "D5 · Capstone — Destroy + Rebuild Production Cluster"),
    },
}


def yaml_escape(s):
    return s.replace("'", "''")


def html_to_md(s):
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


def load_spec(suffix, num):
    path = os.path.join(ROOT, f"scripts/lessons_kadv_{suffix}/lesson{num}.py")
    spec_obj = importlib.util.spec_from_file_location(f"lesson_{suffix}_{num}", path)
    sys.path.insert(0, os.path.dirname(path))
    mod = importlib.util.module_from_spec(spec_obj)
    spec_obj.loader.exec_module(mod)
    return mod.LESSON


def emit_brief(suffix, course_folder, course_code, letter, universe, fact_check_topic, num, slug, module, title, spec):
    outcomes = [f"Learner can explain {html_to_md(s.h2)[0].lower()}{html_to_md(s.h2)[1:]}." for s in spec.sections[:3]]
    stamp = html_to_md(spec.stamp_html)
    scenarios = [html_to_md(s.body).split('.')[0] + '.' for s in spec.scenarios[:4]]
    metaphor = f"{universe} · {spec.district_label} — {html_to_md(spec.analogy_intro_html)[:200]}"
    parts = [
        f"# Intake brief — {letter}{int(num)}, {course_code}",
        f"# Topic: {title}",
        f"# {module}",
        "",
        "lesson:",
        f"  title: '{yaml_escape(title)}'",
        f"  slug: '{slug}'",
        "  domain: 'kubernetes'",
        f"  course_slug: '{course_folder}'",
        f"  position: {num}",
        "  granularity: 'module'",
        "  brief_drafted_on: '2026-05-04'",
        f"  central_metaphor: '{yaml_escape(metaphor)}'",
        f"  module: '{yaml_escape(module)}'",
        "",
        "learner_profile:",
        "  prerequisites:",
        "    - 'K-COM curriculum complete (L01-L44).'",
        "    - 'At least one distribution course (K-EKS / K-AKS / K-GKE / K-OCP / K-VAN).'",
        f"    - '{course_code} modules 1-{int(num) - 1 if int(num) > 1 else 0} (cumulative).'",
        "  assumed_zero_knowledge_of: []",
        "",
        "learning_outcomes:",
    ]
    for o in outcomes:
        parts.append(f"  - '{yaml_escape(o)}'")
    parts += ["", "sections:"]
    for s in spec.sections:
        parts.append(f"  - '{yaml_escape(html_to_md(s.h2))}'")
    parts += ["", "section_5_real_world:", "  count: 4", "  examples:"]
    for s in scenarios:
        parts.append(f"    - '{yaml_escape(s)}'")
    course_segment = "adv-" + suffix
    parts += [
        "",
        "section_6_animated_svg:",
        "  modes_count: 1",
        f"  description: 'See preview-kubernetes-{course_segment}-lesson-{num}.html Section 6 for the live animation.'",
        "",
        "section_7_flashcards_quiz:",
        f"  flashcards: {len(spec.flashcards)}",
        f"  quiz_questions: {len(spec.quizzes)}",
        "",
        "shared_artifacts:",
        f"  preview_page: {{ file: '/preview-kubernetes-{course_segment}-lesson-{num}.html' }}",
        "  lesson_md: { file: 'lesson.md' }",
        f"  flashcards: {{ file: 'flashcards.yaml', count: {len(spec.flashcards)} }}",
        f"  quiz: {{ file: 'quiz.yaml', count: {len(spec.quizzes)} }}",
        "",
        "bar:",
        f"  - '{yaml_escape(stamp)}'",
        "",
        "fact_check_anchors:",
        f"  - 'https://kubernetes.io/docs/concepts/{fact_check_topic}'",
        "  - 'https://kubernetes.io/docs/'",
    ]
    return "\n".join(parts) + "\n"


def emit_lesson_md(course_code, letter, course_segment, num, title, module, spec, universe, district_kind):
    out = [
        f"# {course_code} {letter}{int(num)} — {title}",
        "",
        f"> Course: {course_code} (advanced specialization)",
        f"> {module}",
        f"> Companion preview: `/preview-kubernetes-{course_segment}-lesson-{num}.html`.",
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
        f"## Analogy — the {universe} {district_kind}", "",
        html_to_md(spec.analogy_intro_html), "",
        "**Translation legend.**", "",
        "| In the story… | …in Kubernetes |",
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


def emit_flashcards(course_code, letter, spec):
    out = [f"# Flashcards — {course_code} {letter} (count: {len(spec.flashcards)})", "", "cards:"]
    for i, f in enumerate(spec.flashcards, start=1):
        out.append(f"  - id: {i}")
        out.append("    front: |")
        out.extend(f"      {line}" for line in html_to_md(f.front).splitlines())
        out.append("    back: |")
        out.extend(f"      {line}" for line in html_to_md(f.back).splitlines())
        out.append("")
    return "\n".join(out)


def emit_quiz(course_code, letter, spec):
    out = [f"# Quiz — {course_code} {letter} (count: {len(spec.quizzes)})", "", "questions:"]
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
    DISTRICT_KIND = {"sec": "bastion", "net": "junction", "pe": "bench", "ai": "array", "dr": "cell"}
    for suffix, course_folder, course_code, letter, universe, fact_check_topic in COURSES:
        scenarios_dir = os.path.join(ROOT, f"courses/kubernetes/{course_folder}/scenarios")
        district_kind = DISTRICT_KIND[suffix]
        for num, (slug, module, title) in LESSON_META[suffix].items():
            spec = load_spec(suffix, num)
            folder = os.path.join(scenarios_dir, slug)
            os.makedirs(folder, exist_ok=True)
            files = {
                "brief.yaml": emit_brief(suffix, course_folder, course_code, letter, universe, fact_check_topic, num, slug, module, title, spec),
                "lesson.md": emit_lesson_md(course_code, letter, "adv-" + suffix, num, title, module, spec, universe, district_kind),
                "flashcards.yaml": emit_flashcards(course_code, letter, spec),
                "quiz.yaml": emit_quiz(course_code, letter, spec),
            }
            for fname, content in files.items():
                with open(os.path.join(folder, fname), "w") as f:
                    f.write(content)
        print(f"  {course_code}: wrote {len(LESSON_META[suffix])} folders under {course_folder}")
    print(f"\nDone. {sum(len(v) for v in LESSON_META.values())} folders across 5 K-ADV courses.")


if __name__ == "__main__":
    main()
