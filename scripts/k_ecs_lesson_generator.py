#!/usr/bin/env python3
"""K-ECS (AWS ECS — non-Kubernetes companion course) lesson generator.

Thin config caller; all rendering lives in scripts/multi_course_renderer.py.
This is the first non-K8s course in the K-* family; the K- prefix is family
branding for the courseware platform, not a K8s claim. See DECISIONS.md
2026-05-03 K-ECS entry + STYLE.md K-Harbor section.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KHARBOR_PIERS = [
    ("kh-pier01", "C1", 100, 70, "Harbor Office", "architecture", "anchor"),
    ("kh-pier02", "C2", 240, 70, "Cargo Manifests", "task defs", None),
    ("kh-pier03", "C3", 380, 70, "Lookout &amp; Comms", "networking", None),
    ("kh-pier04", "C4", 520, 70, "Customs House", "IAM + secrets", None),
    ("kh-pier05", "C5", 660, 70, "Cargo Holds", "EFS + FSx + ephemeral", None),
    ("kh-pier06", "C6", 100, 200, "Loading Crew Yard", "deploy + scale", None),
    ("kh-pier07", "C7", 240, 200, "Lighthouse", "Container Insights", None),
    ("kh-pier08", "C8", 380, 200, "Outport Station", "ECS Anywhere", None),
    ("kh-pier09", "C9", 520, 200, "Salvage Office", "troubleshoot", None),
    ("kh-pier10", "C10", 660, 200, "Grand Voyage", "capstone", None),
]

K_ECS_RAIL = [
    ("01", "C1 ECS architecture"),
    ("02", "C2 task defs &amp; containers"),
    ("03", "C3 ECS networking"),
    ("04", "C4 IAM &amp; security"),
    ("05", "C5 ECS storage"),
    ("06", "C6 deploy &amp; scaling"),
    ("07", "C7 observability"),
    ("08", "C8 ECS Anywhere"),
    ("09", "C9 troubleshooting"),
    ("10", "C10 capstone voyage"),
]


CONFIG = CourseConfig(
    course_code="K-ECS",
    course_letter="C",
    course_full_name="AWS ECS",
    universe_name="K-Harbor",
    universe_emoji="⚓",  # ⚓
    district_kind="pier",
    legend_subject="ECS / AWS",
    real_world_heading="How AWS ECS teams do this",
    atlas_pins=KHARBOR_PIERS,
    rail_items=K_ECS_RAIL,
    pin_prefix="kh-pier",
    total_lessons=10,
    html_filename_segment="ecs",
    audit_script_basename="audit_lessons_kecs.py",
    footer_grounded_url="docs.aws.amazon.com/ecs",
    map_floor_stroke="#2E5A8E",
    map_subtitle="K · HARBOR · AWS ECS",
    map_desc_subject="AWS-managed working harbor",
    map_grad_id_primary="kh-water",
    map_grad_id_secondary="kh-pier",
    map_grad_primary_stops=(
        ("0%", "#E8F0F5", "0.7"),
        ("100%", "#C5D8E3", "0.6"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#7AB3CC", "0.18"),
        ("100%", "#2E5A8E", "0.32"),
    ),
    map_dividers=[
        (130, "0.4", 120, "front harbor — arrival, manifests, entry"),
        (260, "0.4", 252, "deeper berths — ops, observability, troubleshooting"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
