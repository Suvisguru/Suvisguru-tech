#!/usr/bin/env python3
"""K-ADV-AI (Kubernetes for AI / ML / GPUs) lesson generator — thin config caller.

Universe: K-Observatory (research observatory — telescope arrays, computation
core, model-rendering halls, signal lines). Pin prefix `kai-array`. Course letter
I (for AI/Inference; AKS owns A). 8 modules.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KOBSERVATORY_ARRAYS = [
    ("kai-array01", "I1", 100, 70, "Optics Bay", "GPU + DRA + MIG", "anchor"),
    ("kai-array02", "I2", 240, 70, "Observation Queue", "Kueue + Volcano", None),
    ("kai-array03", "I3", 380, 70, "Research Hall", "Ray + Kubeflow + KServe", None),
    ("kai-array04", "I4", 520, 70, "Model-Rendering Hall", "vLLM + Triton + NIM", None),
    ("kai-array05", "I5", 660, 70, "Triage Desk", "AI Gateway", None),
    ("kai-array06", "I6", 100, 200, "Signal Lines", "RDMA + EFA + JuiceFS", None),
    ("kai-array07", "I7", 240, 200, "Sharing Committee", "multi-tenant + cost", None),
    ("kai-array08", "I8", 380, 320, "Operating Observatory", "capstone", None),
]

K_ADV_AI_RAIL = [
    ("01", "I1 GPU + DRA + MIG"),
    ("02", "I2 Kueue + Volcano"),
    ("03", "I3 Ray + Kubeflow + KServe"),
    ("04", "I4 LLM serving"),
    ("05", "I5 AI Gateway"),
    ("06", "I6 RDMA + storage"),
    ("07", "I7 multi-tenant GPU + cost"),
    ("08", "I8 capstone observatory"),
]


CONFIG = CourseConfig(
    course_code="K-ADV-AI",
    course_letter="I",
    course_full_name="Kubernetes for AI / ML / GPUs",
    universe_name="K-Observatory",
    universe_emoji="\U0001F52D",  # 🔭
    district_kind="array",
    legend_subject="Kubernetes for AI / ML",
    real_world_heading="How AI / ML teams do this",
    atlas_pins=KOBSERVATORY_ARRAYS,
    rail_items=K_ADV_AI_RAIL,
    pin_prefix="kai-array",
    total_lessons=8,
    html_filename_segment="adv-ai",
    audit_script_basename="audit_lessons_kadv_ai.py",
    footer_grounded_url="kubernetes.io + nvidia.com/kubernetes + kubeflow.org",
    map_floor_stroke="#1F2433",
    map_subtitle="K · OBSERVATORY · AI / ML / GPUs",
    map_desc_subject="research observatory for Kubernetes AI / ML",
    map_grad_id_primary="ko-night",
    map_grad_id_secondary="ko-stars",
    map_grad_primary_stops=(
        ("0%", "#1F2433", "0.55"),
        ("100%", "#3F4A5E", "0.40"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#FAC775", "0.30"),
        ("100%", "#5DCAA5", "0.20"),
    ),
    map_dividers=[
        (130, "0.4", 120, "outer arrays — optics, queue, research, rendering, gateway"),
        (260, "0.4", 252, "inner observatory — signal, sharing, capstone"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
