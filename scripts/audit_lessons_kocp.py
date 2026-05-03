#!/usr/bin/env python3
"""K-OCP cross-lesson audit — thin caller of audit_lessons_shared.

All audit logic lives in audit_lessons_shared.audit_course().
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_lessons_shared import CourseAuditConfig, run_audit_main  # noqa: E402


CONFIG = CourseAuditConfig(
    course_code="K-OCP",
    course_letter="O",
    html_filename_prefix="preview-kubernetes-ocp-lesson-",
    pin_prefix="ko-bay",
    universe_label="K-Foundry",
    total_lessons=13,
)


if __name__ == "__main__":
    run_audit_main(CONFIG)
