# NOTES — Lesson 08: Installing and Configuring ESXi

## Files produced

- `brief.yaml` — intake brief in **per-subtopic** format (6 subtopics, each with its own pedagogical block).
- `lesson.md` — sectioned by subtopic; each subtopic carries its own concept / before-after / analogy / quick check / ELI5 / ELI10 / real-world block.
- `flashcards.yaml` — 20 cards grouped by subtopic with section markers (4/3/3/3/3/4 distribution).
- `quiz.yaml` — 12 questions (2 per subtopic). Mix of pause-the-animation and standalone.
- `diagram.svg` — single shared diagram for the whole lesson: 6-station configuration journey (install → accounts → DCUI/Host Client → services → NTP/DNS/routing → lockdown).
- `animation.html` — single shared animation with 6 mode toggles, one per subtopic. Pause/Play + Speed slider parity to lessons 1-5.
- `/preview-lesson-08.html` (project root) — per-subtopic interactive preview page with sticky sub-nav.

## Structural format

This is the **first lesson** produced under the per-subtopic rule (memory:
`feedback_per_subtopic_structure.md`). Each of the 6 subtopics is treated as a
mini-lesson with the full pedagogical pattern. The shared lesson-level
artifacts (1 diagram, 1 animation, 1 brief, 1 NOTES.md) cover the whole
journey; the per-subtopic structure lives inside the prose, flashcards,
quiz, and preview page.

Visual marker convention used in the preview page:
`Subtopic N of 6: <title>` header on every subtopic block, color-coded
left border per subtopic.

## Alignment verifications performed

Per the alignment-verification protocol (memory: `feedback_verify_alignment.md`):

- **Diagram (`diagram.svg`)**: ViewBox 1100×720. 6 cards 160px wide with 20px gap → total 1060px → 20px margins each side (verified arithmetically). Card y=230, height=340, accent strip at y=562 (h=8). Connecting arrows from card right edge (e.g., x=180) to next card left edge (x=200) along y=400. "Start here" cue points down to station 1 from y=150 to y=222.
- **Animation (`animation.html`)**: ViewBox 1040×540. Each of the 6 mode groups uses 8s loop. Mode-switching via CSS attribute selectors on `data-mode`. Spinning clock in services mode uses `animateTransform` with NO `transform-origin` attribute (per DECISIONS.md, SMIL `transform-origin` rule).
- **Preview page**: Subtopic sticky sub-nav at `top: 98px` (below 49px topbar + 49px course-nav). Scroll-padding-top: 130px so anchored navigation lands cleanly under both nav bars.

## Convention checks

- **Hypervisor color**: slate `#3F4A5E` per STYLE.md.
- **Per-subtopic accent colors**: 1 slate `#3F4A5E`, 2 purple `#5E4A8E`, 3 teal `#2E7A8C`, 4 green `#1F8A60`, 5 warn-orange `#B85829`, 6 danger-red `#8E2A2A`. Same color scale used in diagram, animation buttons, and preview-page subtopic headers for visual continuity.
- **Action buttons (mode toggles, quick-check options, quiz reveal, station cards)**: pulse animation applied (memory: `feedback_action_buttons.md`).
- **Hover-to-define**: `ESXi`, `bare-metal hypervisor`, `kickstart`, `Auto Deploy`, `HCL`, `vCenter SSO`, `DCUI`, `vmkernel`, `lockdown mode`, `exception users` wrapped in `.term` with tooltip + click-to-pin.
- **Course-nav**: lesson 08 inserted after 07 across all 8 preview pages (01-08).
- **Sub-nav (new)**: in-lesson sticky nav with the 6 subtopics, each linked to its anchor. Updates active state on scroll.

## Decisions logged this lesson

None new. The per-subtopic structure rule and visual marker convention were
already logged in memory before this lesson started. Per-subtopic accent
colors are an extension of existing color usage in the design system, not a
new convention.

## Open follow-ups

- Lessons 9-12 still to be produced under per-subtopic format:
  - Lesson 9 — Deploying and Configuring vCenter (~8 subtopics)
  - Lesson 10 — Configuring vSphere Networking (~5 subtopics)
  - Lesson 11 — Configuring vSphere Storage (~6 subtopics)
  - Lesson 12 — Deploying Virtual Machines (~12 subtopics)
- The course-nav across lessons 01-08 currently lists 8 lessons; will need to grow as 9-12 are added.
