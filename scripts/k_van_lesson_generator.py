#!/usr/bin/env python3
"""K-VAN (vanilla Kubernetes) lesson generator — thin config caller.

All rendering lives in scripts/multi_course_renderer.py. This file only
declares the K-VAN CourseConfig and calls run_course_main().
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KFRONTIER_SITES = [
    ("kf-site01", "V1", 100, 70, "Drafting Hut", "design", None),
    ("kf-site02", "V2", 230, 70, "Land Clearing", "OS prep", None),
    ("kf-site03", "V3", 360, 70, "Frame Raising", "kubeadm", None),
    ("kf-site04", "V4", 490, 70, "Wiring & Plumbing", "CNI", None),
    ("kf-site05", "V5", 620, 70, "Outbuildings", "add-ons", None),
    ("kf-site06", "V6", 100, 195, "Rules Board", "config", None),
    ("kf-site07", "V7", 240, 200, "The Well", "etcd", "anchor"),
    ("kf-site08", "V8", 380, 195, "Renovation", "upgrades", None),
    ("kf-site09", "V9", 510, 195, "Watchtower", "hardening", None),
    ("kf-site10", "V10", 640, 195, "Drill Square", "troubleshoot", None),
    ("kf-site11", "V11", 720, 320, "Homestead", "capstone", None),
]

K_VAN_RAIL = [
    ("01", "V1 architecture design"),
    ("02", "V2 OS &amp; node prep"),
    ("03", "V3 kubeadm bootstrap"),
    ("04", "V4 CNI &amp; networking"),
    ("05", "V5 core add-ons"),
    ("06", "V6 cluster config"),
    ("07", "V7 etcd production"),
    ("08", "V8 upgrades &amp; patching"),
    ("09", "V9 security hardening"),
    ("10", "V10 troubleshooting"),
    ("11", "V11 capstone homestead"),
]


KVAN_DECORATIONS = (
    '<path d="M 20 350 Q 200 343 400 348 T 780 350 L 780 380 L 20 380 Z" fill="url(#kf-creek)"/>'
    '\n    <path d="M 20 350 Q 200 343 400 348 T 780 350" stroke="#7AB3CC" stroke-width="0.9" fill="none" opacity="0.5"/>'
    '\n    <text x="745" y="372" text-anchor="end" font-family="sans-serif" font-size="8" font-style="italic" '
    'fill="#4A8FA8" opacity="0.7">— creek —</text>'
)


CONFIG = CourseConfig(
    course_code="K-VAN",
    course_letter="V",
    course_full_name="vanilla Kubernetes",
    universe_name="K-Frontier",
    universe_emoji="\U0001F3D5️",  # 🏕️
    district_kind="site",
    legend_subject="vanilla Kubernetes",
    real_world_heading="How real teams do this",
    atlas_pins=KFRONTIER_SITES,
    rail_items=K_VAN_RAIL,
    pin_prefix="kf-site",
    total_lessons=11,
    html_filename_segment="vanilla",
    audit_script_basename="audit_lessons_kvan.py",
    footer_grounded_url="kubernetes.io",
    analogy_section_subject="build site",
    strip_label_emoji="\U0001F4CD",  # 📍
    aria_lesson_word="Lesson",
    map_floor_stroke="#E8DDC8",
    map_aria_word="site map",
    map_subtitle="K · FRONTIER",
    map_desc_subject="map of the K-Frontier homestead",
    map_grad_id_primary="kf-soil",
    map_grad_id_secondary="kf-creek",
    map_grad_primary_stops=(
        ("0%", "#FBF7F0", "0.6"),
        ("100%", "#F5EFE3", "0.6"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#7AB3CC", "0.18"),
        ("100%", "#4A8FA8", "0.32"),
    ),
    map_decorations_svg=KVAN_DECORATIONS,
    map_dividers=[
        (130, "0.4", None, None),
        (260, "0.4", None, None),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
