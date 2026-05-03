#!/usr/bin/env python3
"""K-GKE cross-lesson audit — thin caller of audit_lessons_shared."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_lessons_shared import CourseAuditConfig, run_audit_main  # noqa: E402


CONFIG = CourseAuditConfig(
    course_code="K-GKE",
    course_letter="G",
    html_filename_prefix="preview-kubernetes-gke-lesson-",
    pin_prefix="kg-plot",
    universe_label="K-Garden",
    total_lessons=10,
)


if __name__ == "__main__":
    run_audit_main(CONFIG)
