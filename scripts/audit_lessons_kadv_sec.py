#!/usr/bin/env python3
"""K-ADV-SEC cross-lesson audit — thin caller of audit_lessons_shared."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_lessons_shared import CourseAuditConfig, run_audit_main  # noqa: E402


CONFIG = CourseAuditConfig(
    course_code="K-ADV-SEC",
    course_letter="S",
    html_filename_prefix="preview-kubernetes-adv-sec-lesson-",
    pin_prefix="ksec-bastion",
    universe_label="K-Citadel",
    total_lessons=8,
)


if __name__ == "__main__":
    run_audit_main(CONFIG)
