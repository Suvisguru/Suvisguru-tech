#!/usr/bin/env python3
"""K-EKS (Amazon EKS) lesson generator — thin config caller.

All rendering lives in scripts/multi_course_renderer.py. This file only
declares the K-EKS CourseConfig and calls run_course_main().
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KSKYLINE_FLOORS = [
    ("ks-floor01", "E1", 100, 70, "Lobby & Floor Plan", "architecture", "anchor"),
    ("ks-floor02", "E2", 240, 70, "Concierge Service", "Auto Mode", None),
    ("ks-floor03", "E3", 380, 70, "Communication Tower", "VPC + LB + DNS", None),
    ("ks-floor04", "E4", 520, 70, "Security Desk", "IAM + IRSA", None),
    ("ks-floor05", "E5", 660, 70, "Storage Vault", "EBS + EFS + FSx", None),
    ("ks-floor06", "E6", 100, 200, "Power Floor", "Karpenter + spot", None),
    ("ks-floor07", "E7", 240, 200, "Vault Mezzanine", "KMS + GuardDuty", None),
    ("ks-floor08", "E8", 380, 200, "Observation Deck", "CloudWatch + AMP", None),
    ("ks-floor09", "E9", 520, 200, "Maintenance Wing", "upgrades", None),
    ("ks-floor10", "E10", 660, 200, "Emergency Plaza", "troubleshoot", None),
    ("ks-floor11", "E11", 380, 320, "Tower Complete", "capstone", None),
]

K_EKS_RAIL = [
    ("01", "E1 EKS architecture"),
    ("02", "E2 EKS Auto Mode"),
    ("03", "E3 AWS networking"),
    ("04", "E4 IAM &amp; identity"),
    ("05", "E5 storage (EBS / EFS / FSx)"),
    ("06", "E6 compute &amp; autoscaling"),
    ("07", "E7 EKS security"),
    ("08", "E8 observability"),
    ("09", "E9 upgrades &amp; ops"),
    ("10", "E10 troubleshooting"),
    ("11", "E11 capstone tower"),
]


CONFIG = CourseConfig(
    course_code="K-EKS",
    course_letter="E",
    course_full_name="Amazon EKS",
    universe_name="K-Skyline",
    universe_emoji="\U0001F3D9️",  # 🏙️
    district_kind="floor",
    legend_subject="EKS / AWS",
    real_world_heading="How AWS-shop teams do this",
    atlas_pins=KSKYLINE_FLOORS,
    rail_items=K_EKS_RAIL,
    pin_prefix="ks-floor",
    total_lessons=11,
    html_filename_segment="eks",
    audit_script_basename="audit_lessons_keks.py",
    footer_grounded_url="docs.aws.amazon.com/eks",
    map_floor_stroke="#E8DDC8",
    map_aria_word="tower map",
    map_subtitle="K · SKYLINE · AWS REGION",
    map_desc_subject="AWS-managed tower",
    map_grad_id_primary="ks-tower",
    map_grad_id_secondary="ks-sky",
    map_grad_primary_stops=(
        ("0%", "#FBF7F0", "0.7"),
        ("100%", "#ECEFF5", "0.6"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#A4B4D0", "0.16"),
        ("100%", "#3F4A5E", "0.30"),
    ),
    map_dividers=[
        (130, "0.4", 120, "tower lobby + main desks"),
        (260, "0.4", 252, "operations + watch decks"),
        (370, "0.3", 362, "capstone"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
