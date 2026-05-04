#!/usr/bin/env python3
"""K-ADV-DR (Kubernetes Disaster Recovery and Business Continuity) lesson generator
— thin config caller.

Universe: K-Lifeboat (emergency drills — lifeboats, rebuild kits, mirror-ships in
other harbors, total-loss restoration). Pin prefix `kdr-cell`. Course letter D.
5 modules.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KLIFEBOAT_CELLS = [
    ("kdr-cell01", "D1", 120, 80, "Drill Square", "etcd + Velero + K10", "anchor"),
    ("kdr-cell02", "D2", 320, 80, "Ship Rebuild Yard", "GitOps recovery", None),
    ("kdr-cell03", "D3", 520, 80, "Mirror-Ship Harbor", "cross-region DR + RPO/RTO", None),
    ("kdr-cell04", "D4", 220, 220, "Cargo Recovery", "secrets + DNS + stateful", None),
    ("kdr-cell05", "D5", 460, 220, "Total-Loss Drill", "capstone", None),
]

K_ADV_DR_RAIL = [
    ("01", "D1 etcd + Velero + K10"),
    ("02", "D2 GitOps-driven recovery"),
    ("03", "D3 cross-region DR"),
    ("04", "D4 secrets + DNS + stateful DR"),
    ("05", "D5 capstone total-loss drill"),
]


CONFIG = CourseConfig(
    course_code="K-ADV-DR",
    course_letter="D",
    course_full_name="Kubernetes Disaster Recovery and Business Continuity",
    universe_name="K-Lifeboat",
    universe_emoji="\U0001F6DF",  # 🛟
    district_kind="cell",
    legend_subject="Kubernetes DR / BC",
    real_world_heading="How DR architects do this",
    atlas_pins=KLIFEBOAT_CELLS,
    rail_items=K_ADV_DR_RAIL,
    pin_prefix="kdr-cell",
    total_lessons=5,
    html_filename_segment="adv-dr",
    audit_script_basename="audit_lessons_kadv_dr.py",
    footer_grounded_url="kubernetes.io/docs/concepts (and velero.io / kasten.io)",
    map_floor_stroke="#1A6FA8",
    map_subtitle="K · LIFEBOAT · DR & BUSINESS CONTINUITY",
    map_desc_subject="emergency drill harbor for Kubernetes DR / BC",
    map_grad_id_primary="kl-water",
    map_grad_id_secondary="kl-flag",
    map_grad_primary_stops=(
        ("0%", "#D8E8F2", "0.6"),
        ("100%", "#7AA8C8", "0.55"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#E24B4A", "0.20"),
        ("100%", "#1A6FA8", "0.30"),
    ),
    map_dividers=[
        (160, "0.4", 150, "ready position — drill square + rebuild yard + mirror-ship"),
        (290, "0.4", 280, "live exercise — cargo recovery + total-loss drill"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
