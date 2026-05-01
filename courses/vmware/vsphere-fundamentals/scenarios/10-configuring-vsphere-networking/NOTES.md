# NOTES — Lesson 10: Configuring vSphere Networking

## Files produced

- `brief.yaml` — intake brief in per-subtopic format (6 subtopics).
- `lesson.md` — sectioned by subtopic.
- `flashcards.yaml` — 18 cards grouped by subtopic (3 per).
- `quiz.yaml` — 12 questions (2 per subtopic). Mix of pause-the-animation and standalone.
- `diagram.svg` — single shared diagram: 6-station networking journey.
- `animation.html` — single shared animation with 6 mode toggles. Pause/Play + Speed parity to lessons 1-9.
- `/preview-lesson-10.html` (project root) — per-subtopic interactive preview.

## Structural format

Per-subtopic format. Same template as lesson 8 (also 6 subtopics).

Subtopic accent colors reuse the same 6-color palette: 1 slate, 2 purple, 3 teal, 4 green, 5 warn-orange, 6 danger-red.

## Alignment verifications performed

- **Diagram**: ViewBox 1100×720. 6 cards 160w × 340h with 20px gap. 6×160 + 5×20 + 2×20 = 1100 ✓. Card x: 20, 200, 380, 560, 740, 920. Inter-card arrows on midline y=400 from card right edge to next card left edge.
- **Animation**: ViewBox 1040×540. 6 mode groups. No `transform-origin` attribute on rotation groups (none exist this lesson; only animate/animateTransform without rotation rotation-origin issues). Each mode runs 6-8 second loops.
- **Preview page**: Sub-nav at `top: 98px`, scroll-padding-top 130px. 6 sub-links fit in scrollable horizontal nav. Hero journey grid `repeat(6, 1fr)` on wide / `repeat(3, 1fr)` mid / `repeat(2, 1fr)` narrow.

## Convention checks

- All action buttons (mode toggles, quick-check options, quiz reveal, station cards) use the pulse animation per `feedback_action_buttons.md`.
- Hover-to-define on: vSwitch, vSS, vDS, uplink, port group, vmkernel, VLAN tagging, VST, LACP, NetFlow, NIC teaming, beacon probing.
- Course-nav: lesson 10 inserted after 09 across all 10 preview pages (01-10).

## Decisions logged this lesson

None new. All conventions reused from earlier lessons.

## Open follow-ups

- Lessons 11 and 12 still to be produced under per-subtopic format:
  - Lesson 11 — Configuring vSphere Storage
  - Lesson 12 — Deploying Virtual Machines
