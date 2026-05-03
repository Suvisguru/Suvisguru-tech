#!/usr/bin/env python3
"""K-AKS (Azure AKS) lesson generator — thin config caller.

All rendering lives in scripts/multi_course_renderer.py. This file only
declares the K-AKS CourseConfig and calls run_course_main().
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


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


CONFIG = CourseConfig(
    course_code="K-AKS",
    course_letter="A",
    course_full_name="Azure AKS",
    universe_name="K-Campus",
    universe_emoji="\U0001F3DB️",  # 🏛️
    district_kind="wing",
    legend_subject="AKS / Azure",
    real_world_heading="How Azure-shop teams do this",
    atlas_pins=KCAMPUS_WINGS,
    rail_items=K_AKS_RAIL,
    pin_prefix="kc-wing",
    total_lessons=11,
    html_filename_segment="aks",
    audit_script_basename="audit_lessons_kaks.py",
    footer_grounded_url="learn.microsoft.com/azure/aks",
    map_floor_stroke="#A8C4A0",
    map_subtitle="K · CAMPUS · AZURE REGION",
    map_desc_subject="Azure-managed campus complex",
    map_grad_id_primary="kc-grass",
    map_grad_id_secondary="kc-sky",
    map_grad_primary_stops=(
        ("0%", "#E8EFE0", "0.6"),
        ("100%", "#C8D8C0", "0.5"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#7AB3CC", "0.18"),
        ("100%", "#4A8FA8", "0.32"),
    ),
    map_dividers=[
        (130, "0.4", 120, "main quad &amp; gateway buildings"),
        (260, "0.4", 252, "operations &amp; observation halls"),
        (370, "0.3", 362, "commencement hall"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
