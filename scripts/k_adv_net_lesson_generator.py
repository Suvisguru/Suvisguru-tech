#!/usr/bin/env python3
"""K-ADV-NET (Kubernetes Networking Architect) lesson generator — thin config caller.

Universe: K-Highway (interstate highway — lanes, exits, intersections, bridges,
customs, traffic helicopter). Pin prefix `knet-junction`. Course letter N. 7 modules.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KHIGHWAY_JUNCTIONS = [
    ("knet-junction01", "N1", 100, 70, "Highway HQ", "CNI + eBPF + BGP", "anchor"),
    ("knet-junction02", "N2", 280, 70, "Main Intersection", "Gateway API", None),
    ("knet-junction03", "N3", 460, 70, "Inter-City Bridges", "multi-cluster", None),
    ("knet-junction04", "N4", 640, 70, "Express Lanes", "mesh + DNS + IPv6", None),
    ("knet-junction05", "N5", 200, 200, "Customs + Tollbooth", "NetPol + egress", None),
    ("knet-junction06", "N6", 460, 200, "Traffic Helicopter", "tracing + tuning", None),
    ("knet-junction07", "N7", 380, 320, "Multi-Region Map", "capstone", None),
]

K_ADV_NET_RAIL = [
    ("01", "N1 CNI + eBPF + BGP"),
    ("02", "N2 Gateway API at fleet scale"),
    ("03", "N3 multi-cluster networking"),
    ("04", "N4 mesh + DNS + IPv6"),
    ("05", "N5 NetworkPolicy + egress + private"),
    ("06", "N6 packet tracing + perf"),
    ("07", "N7 capstone multi-region"),
]


CONFIG = CourseConfig(
    course_code="K-ADV-NET",
    course_letter="N",
    course_full_name="Kubernetes Networking Architect",
    universe_name="K-Highway",
    universe_emoji="\U0001F6E3️",  # 🛣️
    district_kind="junction",
    legend_subject="Kubernetes networking",
    real_world_heading="How networking architects do this",
    atlas_pins=KHIGHWAY_JUNCTIONS,
    rail_items=K_ADV_NET_RAIL,
    pin_prefix="knet-junction",
    total_lessons=7,
    html_filename_segment="adv-net",
    audit_script_basename="audit_lessons_kadv_net.py",
    footer_grounded_url="kubernetes.io/docs/concepts/services-networking",
    map_floor_stroke="#3F4A5E",
    map_subtitle="K · HIGHWAY · NETWORKING ARCHITECT",
    map_desc_subject="interstate highway for Kubernetes networking",
    map_grad_id_primary="kn-asphalt",
    map_grad_id_secondary="kn-paint",
    map_grad_primary_stops=(
        ("0%", "#D8DCE2", "0.6"),
        ("100%", "#A4ACB8", "0.55"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#FAC775", "0.20"),
        ("100%", "#8B6A1F", "0.30"),
    ),
    map_dividers=[
        (130, "0.4", 120, "core highways — CNI, intersection, bridges, lanes"),
        (260, "0.4", 252, "border + traffic ops"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
