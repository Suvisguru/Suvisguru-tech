"""Shorthand for K-ECS spec modules."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from k8s_lesson_generator import (  # noqa: E402, F401
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem, Animation, AnimationScene, AnimationPhase,
)
