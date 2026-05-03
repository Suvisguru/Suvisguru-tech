#!/usr/bin/env python3
"""K-AKS cross-lesson audit — thin caller of audit_lessons_shared."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_lessons_shared import CourseAuditConfig, run_audit_main  # noqa: E402


CONFIG = CourseAuditConfig(
    course_code="K-AKS",
    course_letter="A",
    html_filename_prefix="preview-kubernetes-aks-lesson-",
    pin_prefix="kc-wing",
    universe_label="K-Campus",
    total_lessons=11,
)


if __name__ == "__main__":
    run_audit_main(CONFIG)
