#!/usr/bin/env python3
"""K-GKE (Google GKE) lesson generator — thin config caller.

All rendering lives in scripts/multi_course_renderer.py. This file only
declares the K-GKE CourseConfig and calls run_course_main().
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KGARDEN_PLOTS = [
    ("kg-plot01", "G1", 100, 70, "Visitors' Pavilion", "architecture", "anchor"),
    ("kg-plot02", "G2", 240, 70, "The Almanac Hut", "release channels", None),
    ("kg-plot03", "G3", 380, 70, "Pathways &amp; Trellises", "VPC + Gateway + LB", None),
    ("kg-plot04", "G4", 520, 70, "Gatekeeper's Lodge", "WIF + BinAuth + Posture", None),
    ("kg-plot05", "G5", 660, 70, "Reservoir &amp; Compost", "PD + Filestore + Hyperdisk", None),
    ("kg-plot06", "G6", 100, 200, "Auto-Greenhouse", "scaling + cost", None),
    ("kg-plot07", "G7", 240, 200, "Watchtower", "GMP + Cloud Mon + Trace", None),
    ("kg-plot08", "G8", 380, 200, "Research Greenhouse", "Fleets + AI/ML", None),
    ("kg-plot09", "G9", 520, 200, "Plant Doctor's Hut", "GCP-specific RCA", None),
    ("kg-plot10", "G10", 660, 200, "Harvest Festival", "capstone", None),
]

K_GKE_RAIL = [
    ("01", "G1 GKE architecture &amp; modes"),
    ("02", "G2 versioning &amp; channels"),
    ("03", "G3 GKE networking"),
    ("04", "G4 identity &amp; security"),
    ("05", "G5 GKE storage"),
    ("06", "G6 scaling &amp; cost"),
    ("07", "G7 GKE observability"),
    ("08", "G8 Enterprise (Fleets) &amp; AI/ML"),
    ("09", "G9 troubleshooting"),
    ("10", "G10 capstone harvest"),
]


CONFIG = CourseConfig(
    course_code="K-GKE",
    course_letter="G",
    course_full_name="Google GKE",
    universe_name="K-Garden",
    universe_emoji="\U0001F33F",  # 🌿
    district_kind="plot",
    legend_subject="GKE / GCP",
    real_world_heading="How GCP-shop teams do this",
    atlas_pins=KGARDEN_PLOTS,
    rail_items=K_GKE_RAIL,
    pin_prefix="kg-plot",
    total_lessons=10,
    html_filename_segment="gke",
    audit_script_basename="audit_lessons_kgke.py",
    footer_grounded_url="cloud.google.com/kubernetes-engine",
    map_floor_stroke="#7BA068",
    map_subtitle="K · GARDEN · GCP REGION",
    map_desc_subject="Google-managed garden / orchard",
    map_grad_id_primary="kg-soil",
    map_grad_id_secondary="kg-sky",
    map_grad_primary_stops=(
        ("0%", "#E8EFE0", "0.7"),
        ("100%", "#A8C896", "0.55"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#7AB3CC", "0.16"),
        ("100%", "#3F4A5E", "0.30"),
    ),
    map_dividers=[
        (130, "0.4", 120, "front of garden — pavilion &amp; planting"),
        (260, "0.4", 252, "deeper plots — operations &amp; harvest"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
