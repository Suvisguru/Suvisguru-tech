# NOTES — Lesson 05: vSphere — where it fits, how you access it, what it touches

## Files produced

- `brief.yaml` — intake brief (approved before production).
- `lesson.md` — 7-section prose narrative.
- `flashcards.yaml` — 10 cards covering placement, the 4 UIs, and the 5 hardware resources.
- `quiz.yaml` — 3 pause-the-animation questions (memory overcommit, vCPU contract, Host Client fallback).
- `diagram.svg` — hub-and-spoke: 4 UIs (vSphere Client, Host Client, DCUI, CLI/API) feed into a vSphere center; 5 hardware resources (CPU, memory, network, storage, GPU) feed out. ViewBox 1100×720.
- `animation.html` — 5-mode walkthrough (cpu, memory, network, storage, gpu) with full Pause/Play + Speed slider parity to lessons 1-3.
- `/preview-lesson-05.html` (project root) — interactive preview for learners.

## Structural format

This lesson is in the **collapsed** (single-block) format. The per-subtopic restructure
rule (memory: `feedback_per_subtopic_structure.md`) applies only to lessons produced
*after* the rule was given. Existing lessons 01-07, including this one, stay collapsed
unless explicitly restructured by the founder.

## Alignment verifications performed

Per the alignment-verification protocol (memory: `feedback_verify_alignment.md`):

- **Diagram (`diagram.svg`)**: all 4 UI tiles centered on x=180, y stack at 80, 200, 320, 440 with 100px height + 20px gap → tiles abut the connector channel cleanly. The 5 hardware resource tiles centered on x=920 with same y-rhythm. Center vSphere card (x=440, y=240, 220×240) lines up with the connector midpoints.
- **Animation (`animation.html`)**: hardware band at y=440, host chassis at y=470 → 30px hypervisor band abuts both. VM tiles in CPU/memory modes pinned to integer y boundaries (y=200, 280, 360 with 64px tiles → 16px gaps verified equal).
- **PSU fan rotations**: groups have NO `transform-origin` attribute (per DECISIONS.md: SMIL `transform-origin` rule). Center coordinates drive `animateTransform from="0 cx cy" to="360 cx cy"`.

## Convention checks

- **Hypervisor color**: slate `#3F4A5E` per STYLE.md.
- **Utilization meter fill**: neutral `#5A6B81` per STYLE.md.
- **VM tile**: 120×64 with 11px text per library primitive.
- **Action buttons (Pause/Play, Speed slider, mode toggles)**: pulse animation applied to primary actions.
- **Hover-to-define**: `vSphere Client`, `DCUI`, `PowerCLI`, `NUMA`, `vGPU` wrapped in `.term` with tooltip + click-to-pin behavior in preview page.
- **Course-nav**: lesson 05 inserted between 04 and 06 across all 7 preview pages.

## Decisions logged this lesson

None new. This lesson stays inside existing conventions. The per-subtopic structure
rule was logged separately in memory (not DECISIONS.md, since it is operational
guidance for future sessions rather than a visual/narrative convention).

## Open follow-ups

- None. Lesson 05 is shipped and consistent with lessons 01-04, 06, 07.
