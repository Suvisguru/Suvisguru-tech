#!/usr/bin/env python3
"""K-ADV-PE (Kubernetes Platform Engineering) lesson generator — thin config caller.

Universe: K-Workshop (master craftsperson workshop — golden tools, blueprints,
apprentice paths, batch jigs). Pin prefix `kpe-bench`. Course letter P. 8 modules.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KWORKSHOP_BENCHES = [
    ("kpe-bench01", "P1", 100, 70, "Master Blueprint Library", "IDP + golden paths", "anchor"),
    ("kpe-bench02", "P2", 240, 70, "Catalog Drawer", "Backstage", None),
    ("kpe-bench03", "P3", 380, 70, "Composition Workbench", "Crossplane v2", None),
    ("kpe-bench04", "P4", 520, 70, "Batch-Crafting Jig", "Argo CD ApplicationSets", None),
    ("kpe-bench05", "P5", 660, 70, "Apprentice Intake", "tenant onboarding", None),
    ("kpe-bench06", "P6", 100, 200, "Standard Tool Set", "Score / OAM / Radius", None),
    ("kpe-bench07", "P7", 240, 200, "Workshop Accounting", "SLOs + chargeback", None),
    ("kpe-bench08", "P8", 380, 320, "Equipped Workshop", "capstone", None),
]

K_ADV_PE_RAIL = [
    ("01", "P1 IDP + golden paths"),
    ("02", "P2 Backstage"),
    ("03", "P3 Crossplane v2"),
    ("04", "P4 Argo CD ApplicationSets"),
    ("05", "P5 tenant onboarding"),
    ("06", "P6 workload abstractions"),
    ("07", "P7 SLOs + chargeback"),
    ("08", "P8 capstone IDP"),
]


CONFIG = CourseConfig(
    course_code="K-ADV-PE",
    course_letter="P",
    course_full_name="Kubernetes Platform Engineering",
    universe_name="K-Workshop",
    universe_emoji="\U0001F6E0️",  # 🛠️
    district_kind="bench",
    legend_subject="Kubernetes platform engineering",
    real_world_heading="How platform teams do this",
    atlas_pins=KWORKSHOP_BENCHES,
    rail_items=K_ADV_PE_RAIL,
    pin_prefix="kpe-bench",
    total_lessons=8,
    html_filename_segment="adv-pe",
    audit_script_basename="audit_lessons_kadv_pe.py",
    footer_grounded_url="kubernetes.io/docs/concepts (and platformengineering.org)",
    map_floor_stroke="#7F5A2A",
    map_subtitle="K · WORKSHOP · PLATFORM ENGINEERING",
    map_desc_subject="master craftsperson workshop for Kubernetes platforms",
    map_grad_id_primary="kw-wood",
    map_grad_id_secondary="kw-brass",
    map_grad_primary_stops=(
        ("0%", "#F0E0C0", "0.6"),
        ("100%", "#C09A60", "0.55"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#FAC775", "0.20"),
        ("100%", "#7F5A2A", "0.30"),
    ),
    map_dividers=[
        (130, "0.4", 120, "front benches — blueprints, catalog, composition, batch jig, intake"),
        (260, "0.4", 252, "shop floor — abstractions, accounting, capstone"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
