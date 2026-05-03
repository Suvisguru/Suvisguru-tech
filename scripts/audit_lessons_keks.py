#!/usr/bin/env python3
"""K-EKS cross-lesson audit — thin caller of audit_lessons_shared."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_lessons_shared import CourseAuditConfig, run_audit_main  # noqa: E402


CONFIG = CourseAuditConfig(
    course_code="K-EKS",
    course_letter="E",
    html_filename_prefix="preview-kubernetes-eks-lesson-",
    pin_prefix="ks-floor",
    universe_label="K-Skyline",
    total_lessons=11,
)


if __name__ == "__main__":
    run_audit_main(CONFIG)
