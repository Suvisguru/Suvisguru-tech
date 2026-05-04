#!/usr/bin/env python3
"""K-ADV-SEC (Kubernetes Security Architect) lesson generator — thin config caller.

Universe: K-Citadel (fortified citadel — walls, gates, vault, sentries, audit
archives, war room). Pin prefix `ksec-bastion`. Course letter S. 8 modules.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_course_renderer import CourseConfig, run_course_main  # noqa: E402


KCITADEL_BASTIONS = [
    ("ksec-bastion01", "S1", 100, 70, "Threat Map Room", "zero-trust", "anchor"),
    ("ksec-bastion02", "S2", 240, 70, "Authorization Desk", "RBAC", None),
    ("ksec-bastion03", "S3", 380, 70, "Checkpoint Gates", "admission", None),
    ("ksec-bastion04", "S4", 520, 70, "Mandatory-Helmet Zones", "PSA + runtime", None),
    ("ksec-bastion05", "S5", 660, 70, "Seal Workshop", "signing + SBOM", None),
    ("ksec-bastion06", "S6", 100, 200, "Armored Vault", "secrets + mTLS", None),
    ("ksec-bastion07", "S7", 240, 200, "Audit + War Room", "compliance + IR", None),
    ("ksec-bastion08", "S8", 380, 320, "Defendable Citadel", "capstone", None),
]

K_ADV_SEC_RAIL = [
    ("01", "S1 threat-modeling + zero-trust"),
    ("02", "S2 RBAC at scale"),
    ("03", "S3 admission policy architecture"),
    ("04", "S4 PSA + runtime detection"),
    ("05", "S5 image signing + SBOM"),
    ("06", "S6 secrets + mTLS + mesh"),
    ("07", "S7 audit + compliance + IR"),
    ("08", "S8 capstone citadel"),
]


CONFIG = CourseConfig(
    course_code="K-ADV-SEC",
    course_letter="S",
    course_full_name="Kubernetes Security Architect",
    universe_name="K-Citadel",
    universe_emoji="\U0001F3F0",  # 🏰
    district_kind="bastion",
    legend_subject="Kubernetes security",
    real_world_heading="How regulated platforms do this",
    atlas_pins=KCITADEL_BASTIONS,
    rail_items=K_ADV_SEC_RAIL,
    pin_prefix="ksec-bastion",
    total_lessons=8,
    html_filename_segment="adv-sec",
    audit_script_basename="audit_lessons_kadv_sec.py",
    footer_grounded_url="kubernetes.io/docs/concepts/security",
    map_floor_stroke="#5A4A36",
    map_subtitle="K · CITADEL · SECURITY ARCHITECT",
    map_desc_subject="fortified citadel for Kubernetes security",
    map_grad_id_primary="kc-stone",
    map_grad_id_secondary="kc-banner",
    map_grad_primary_stops=(
        ("0%", "#EAE2D2", "0.6"),
        ("100%", "#C8B89A", "0.55"),
    ),
    map_grad_secondary_stops=(
        ("0%", "#8E2A2A", "0.18"),
        ("100%", "#3F4A5E", "0.30"),
    ),
    map_dividers=[
        (130, "0.4", 120, "outer perimeter — modeling, identity, gates, runtime"),
        (260, "0.4", 252, "inner stronghold — vault, audit, war room"),
    ],
)


if __name__ == "__main__":
    run_course_main(CONFIG)
