# NOTES — Lesson 09: Deploying and Configuring vCenter Server

## Files produced

- `brief.yaml` — intake brief in per-subtopic format (8 subtopics).
- `lesson.md` — sectioned by subtopic; each subtopic carries the full pedagogical pattern.
- `flashcards.yaml` — 24 cards grouped by subtopic with section markers (3 per subtopic).
- `quiz.yaml` — 16 questions (2 per subtopic). Mix of pause-the-animation and standalone.
- `diagram.svg` — single shared diagram: 8-station deployment journey in two rows of four.
- `animation.html` — single shared animation with 8 mode toggles. Pause/Play + Speed slider parity to lessons 1-8.
- `/preview-lesson-09.html` (project root) — per-subtopic interactive preview page.

## Structural format

Per-subtopic format (per `feedback_per_subtopic_structure.md`). Same template as
lesson 8, scaled up to 8 subtopics.

Subtopic accent color palette:
- 1 Overview: `#3F4A5E` slate
- 2 Prereqs: `#5E4A8E` purple
- 3 Stage 1: `#2E7A8C` teal
- 4 Stage 2: `#1F8A60` green
- 5 SSO: `#B85829` warn-orange
- 6 RBAC: `#8E2A2A` danger-red
- 7 Inventory + Backup: `#1A6FA8` blue (new for this lesson; extends existing palette)
- 8 vCenter HA: `#5C7A1F` olive (new for this lesson; extends existing palette)

## Alignment verifications performed

Per `feedback_verify_alignment.md`:

- **Diagram (`diagram.svg`)**: ViewBox 1100×720. Two rows of 4 cards each; cards 220w × 220h; gap 60; margin 20 each side (4*220 + 3*60 + 2*20 = 1100 ✓). Card x positions: 20, 300, 580, 860. Row 1 y=170, row 2 y=410. Inter-card arrows on midline y=280 (row 1) / y=520 (row 2), from card right edge to next card left edge. Curved row-to-row connector goes off the right of card 4 down to the left of card 5 with a U-turn shape (verified end points: (1080,335) → (130,520)).
- **Animation (`animation.html`)**: ViewBox 1040×540. 8 mode groups. Spinning backup-icon arrow in inventory mode uses `animateTransform` with NO `transform-origin` attribute (per DECISIONS.md SMIL rule). Each mode runs an 8-second loop.
- **Preview page**: Sub-nav at `top: 98px`, scroll-padding-top 130px. 8 sub-links fit in scrollable horizontal nav. Hero journey grid uses `repeat(4, 1fr)` on wide / `repeat(2, 1fr)` mid / `1fr` narrow.

## Convention checks

- Hypervisor color slate `#3F4A5E` used for vCenter appliance and SSO box per STYLE.md.
- Action buttons (mode toggles, quick-check options, quiz reveal, station cards) use the pulse animation per `feedback_action_buttons.md`.
- Hover-to-define on: vCenter Server, VCSA, Photon OS, OVA, SSO, identity source, RBAC, role, permission, propagating, vCenter HA. All wrapped in `.term` with click-to-pin.
- Course-nav: lesson 09 inserted after 08 across all 9 preview pages (01-09).

## Decisions logged this lesson

None new. Two new accent colors added (#1A6FA8 blue for inventory, #5C7A1F olive
for HA) to extend the per-subtopic color scale to 8. Treated as a natural
extension of the existing palette, not a new convention worth a DECISIONS.md
entry.

## Open follow-ups

- Lessons 10-12 still to be produced under per-subtopic format:
  - Lesson 10 — Configuring vSphere Networking
  - Lesson 11 — Configuring vSphere Storage
  - Lesson 12 — Deploying Virtual Machines
