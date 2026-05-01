# NOTES — Lesson 11: Configuring vSphere Storage

## Files produced

- `brief.yaml`, `lesson.md`, `flashcards.yaml` (18 cards), `quiz.yaml` (12 questions), `diagram.svg`, `animation.html`, `/preview-lesson-11.html`.

## Format

Per-subtopic, 6 subtopics. Same template as lessons 8 and 10. Subtopic accent colors reuse the same palette: 1 slate, 2 purple, 3 teal, 4 green, 5 warn-orange, 6 danger-red.

## Alignment verifications

- **Diagram**: ViewBox 1100×720. 6 cards 160w × 340h with 20px gap. Math: 6×160 + 5×20 + 2×20 = 1100 ✓. Card x: 20, 200, 380, 560, 740, 920. Inter-card arrows on midline y=400.
- **Animation**: ViewBox 1040×540. 6 mode groups; no `transform-origin` on rotation groups (none in this lesson). Mode 1 (overview) cycles a yellow highlight box across the four datastore-type cards over 12s.
- **Preview**: Sub-nav `top: 98px`, scroll-padding-top 130px. 6 sub-links. Hero journey grid `repeat(6, 1fr)` on wide / `repeat(3, 1fr)` mid / `repeat(2, 1fr)` narrow.

## Convention checks

- Action buttons (mode toggles, quick-check options, quiz reveal, station cards) use the pulse animation.
- Hover-to-define on: datastore, VMFS, LUN, HBA, multipathing, NFS, vSAN, vVols, VASA, SPBM.
- Course-nav: lesson 11 inserted after 10 across all 11 preview pages (01-11).

## Decisions logged this lesson

None new.

## Open follow-ups

- Lesson 12 — Deploying Virtual Machines.
