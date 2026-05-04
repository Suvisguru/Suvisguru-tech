#!/usr/bin/env python3
"""K-ADV-AI cross-lesson audit — thin caller of audit_lessons_shared."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_lessons_shared import CourseAuditConfig, run_audit_main  # noqa: E402


CONFIG = CourseAuditConfig(
    course_code="K-ADV-AI",
    course_letter="I",
    html_filename_prefix="preview-kubernetes-adv-ai-lesson-",
    pin_prefix="kai-array",
    universe_label="K-Observatory",
    total_lessons=8,
)


if __name__ == "__main__":
    run_audit_main(CONFIG)
