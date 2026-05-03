#!/usr/bin/env python3
"""K-OCP (Red Hat OpenShift) lesson generator — thin config caller.

All rendering lives in scripts/multi_course_renderer.py. This file only
declares the K-OCP CourseConfig and calls run_course_main().
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KFOUNDRY_BAYS = [
    ("ko-bay01", "O1", 100, 70, "Welcome Hall", "architecture", "anchor"),
    ("ko-bay02", "O2", 280, 70, "Construction Site", "installation", None),
    ("ko-bay03", "O3", 460, 70, "Pipework &amp; Conveyors", "OVN-K + Routes", None),
    ("ko-bay04", "O4", 640, 70, "Safety Office", "SCC + RHACS", None),
    ("ko-bay05", "O5", 100, 180, "Operator Hub", "OLM", None),
    ("ko-bay06", "O6", 280, 180, "Mold Shop", "S2I + Pipelines + GitOps", None),
    ("ko-bay07", "O7", 460, 180, "Inventory Warehouse", "ODF + OADP", None),
    ("ko-bay08", "O8", 640, 180, "Maintenance Bay", "EUS + MCO + upgrades", None),
    ("ko-bay09", "O9", 100, 290, "Special Castings Wing", "Virt + AI + Edge", None),
    ("ko-bay10", "O10", 280, 290, "Multi-Foundry Network", "ACM + Hypershift", None),
    ("ko-bay11", "O11", 460, 290, "Control Tower", "Monitoring + Loki + Tempo", None),
    ("ko-bay12", "O12", 640, 290, "Diagnostic Lab", "must-gather", None),
    ("ko-bay13", "O13", 380, 370, "Grand Opening", "capstone", None),
]

K_OCP_RAIL = [
    ("01", "O1 OCP architecture"),
    ("02", "O2 installation models"),
    ("03", "O3 OCP networking"),
    ("04", "O4 OCP security"),
    ("05", "O5 Operators &amp; OLM"),
    ("06", "O6 workloads &amp; DevEx"),
    ("07", "O7 OCP storage"),
    ("08", "O8 OCP operations"),
    ("09", "O9 Virt + AI + Edge"),
    ("10", "O10 multi-cluster (ACM)"),
    ("11", "O11 observability"),
    ("12", "O12 troubleshooting"),
    ("13", "O13 capstone foundry"),
]


CONFIG = CourseConfig(
    course_code="K-OCP",
    course_letter="O",
    course_full_name="Red Hat OpenShift",
    universe_name="K-Foundry",
    universe_emoji="\U0001F3ED",  # 🏭
    district_kind="bay",
    legend_subject="OpenShift / Red Hat",
    real_world_heading="How OpenShift teams do this",
    atlas_pins=KFOUNDRY_BAYS,
    rail_items=K_OCP_RAIL,
    pin_prefix="ko-bay",
    total_lessons=13,
    html_filename_segment="ocp",
    audit_script_basename="audit_lessons_kocp.py",
    footer_grounded_url="docs.openshift.com",
    map_viewbox="0 0 800 420",
    map_floor_height=380,
    map_floor_stroke="#A04832",
    map_subtitle="K · FOUNDRY · RED HAT OPENSHIFT",
    map_desc_subject="Red Hat OpenShift enterprise factory",
    map_grad_id_primary="ko-floor",
    map_grad_id_secondary="ko-fire",
    map_grad_primary_stops=(
        ("0%", "#FBF1D6", "0.7"),
        ("100%", "#E8DDC8", "0.55"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#A04832", "0.16"),
        ("100%", "#3F4A5E", "0.30"),
    ),
    map_dividers=[
        (130, "0.4", 120, "welcome &amp; foundation bays"),
        (240, "0.4", 232, "production &amp; ops bays"),
        (350, "0.3", 342, "specialty &amp; multi-foundry bays"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
