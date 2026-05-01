# NOTES — Lesson 12: Deploying Virtual Machines

## Files produced

- `brief.yaml`, `lesson.md`, `flashcards.yaml` (24 cards), `quiz.yaml` (16 questions), `diagram.svg`, `animation.html`, `/preview-lesson-12.html`.

## Format

Per-subtopic, 8 subtopics. Same template as lesson 9 (also 8 subtopics). Subtopic accent colors reuse the 8-color palette: 1 slate, 2 purple, 3 teal, 4 green, 5 warn-orange, 6 danger-red, 7 blue, 8 olive.

## Alignment verifications

- **Diagram**: ViewBox 1100×720. Two rows of 4 cards each; cards 220w × 220h; gap 60; margin 20. 4×220 + 3×60 + 2×20 = 1100 ✓. Card x: 20, 300, 580, 860. Row 1 y=170, row 2 y=410. Row-to-row connector arc verified end points.
- **Animation**: ViewBox 1040×540. 8 mode groups. No `transform-origin` on any rotation groups (none used in this lesson). Each mode 6-10 second loops.
- **Preview**: Sub-nav `top: 98px`, scroll-padding-top 130px. 8 sub-links horizontal. Hero journey grid `repeat(4, 1fr)` on wide / `repeat(2, 1fr)` mid / `1fr` narrow. Course-completion card uses success-green gradient for visual punctuation.

## Convention checks

- All action buttons (mode toggles, quick-check options, quiz reveal, station cards) use the pulse animation.
- Hover-to-define on: vCPU, vRAM, vDisk, vNIC, virtual hardware version, template, clone, content library, OVF, OVA, snapshot, VMware Tools, hot-add operations.
- Course-nav: lesson 12 inserted after 11 across all 12 preview pages (01-12).

## Decisions logged this lesson

None new. All conventions reused from earlier lessons.

## Course completion

vSphere Fundamentals — 12 lessons complete:

- 01 What is virtualization
- 02 Benefits of virtualization
- 03 VMware vSphere components
- 04 History of virtualization
- 05 vSphere context and resources
- 06 Types of hypervisors
- 07 SDDC and public cloud
- 08 Installing and Configuring ESXi (per-subtopic, 6 sub)
- 09 Deploying and Configuring vCenter (per-subtopic, 8 sub)
- 10 Configuring vSphere Networking (per-subtopic, 6 sub)
- 11 Configuring vSphere Storage (per-subtopic, 6 sub)
- 12 Deploying Virtual Machines (per-subtopic, 8 sub) — this lesson

Lessons 1-7 are in the original (collapsed) format per the per-subtopic
rule's scope (only applies to lessons produced from rule-creation
onward). Lessons 8-12 are all per-subtopic.

The completion card on `preview-lesson-12.html` provides a visual
"course done" summary.

## Open follow-ups

- None for this lesson.
- Course-level: founder may want a course-index page (e.g.,
  `/preview-index.html`) or a dashboard summarizing all 12 lessons.
  Not in scope for lesson 12 itself.
