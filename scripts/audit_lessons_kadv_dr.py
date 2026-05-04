#!/usr/bin/env python3
"""K-ADV-DR cross-lesson audit — thin caller of audit_lessons_shared."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_lessons_shared import CourseAuditConfig, run_audit_main  # noqa: E402


CONFIG = CourseAuditConfig(
    course_code="K-ADV-DR",
    course_letter="D",
    html_filename_prefix="preview-kubernetes-adv-dr-lesson-",
    pin_prefix="kdr-cell",
    universe_label="K-Lifeboat",
    total_lessons=5,
)


if __name__ == "__main__":
    run_audit_main(CONFIG)
