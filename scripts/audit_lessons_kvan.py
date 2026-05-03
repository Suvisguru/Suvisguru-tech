#!/usr/bin/env python3
"""K-VAN cross-lesson audit — thin caller of audit_lessons_shared."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_lessons_shared import CourseAuditConfig, run_audit_main  # noqa: E402


CONFIG = CourseAuditConfig(
    course_code="K-VAN",
    course_letter="V",
    html_filename_prefix="preview-kubernetes-vanilla-lesson-",
    pin_prefix="kf-site",
    universe_label="K-Frontier",
    total_lessons=11,
)


if __name__ == "__main__":
    run_audit_main(CONFIG)
