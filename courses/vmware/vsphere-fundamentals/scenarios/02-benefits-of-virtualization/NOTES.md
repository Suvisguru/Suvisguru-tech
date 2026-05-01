# Production notes — Lesson 02: Benefits of virtualization

## What was built

- `brief.yaml` — intake brief (self-authored from founder direction).
- `lesson.md` — seven-section prose, structured per PROJECT.md.
- `diagram.svg` — single composition showing all 5 benefits side-by-side as numbered cards.
- `animation.html` — interactive five-mode tour (consolidate / speed / isolate / snapshot / mobility), each with SMIL motion + pause + speed.
- `flashcards.yaml` — 10 cards covering every benefit + analogy mappings + counterintuitive cases.
- `quiz.yaml` — 3 pause-the-animation prediction questions targeting different benefit modes.
- `/preview-lesson-02.html` (project root) — interactive preview page following STYLE.md "Lesson preview page" conventions. Reference implementation: preview-lesson-01.html.

## Production decisions

- **5 benefits in one lesson** rather than splitting. They hang together as the "what virtualization gives you" mental model. Future lessons deep-dive into each (snapshot mechanics, mobility internals, HA, etc.).
- **Apartment-building analogy continues** as canonical (per DECISIONS.md from lesson 01).
- **No VMware product names** (vMotion, HA, DRS, etc.) — generic terms only. Product names introduce in later lessons.
- **Hero widget format**: 5-tab benefit tour with prev/next navigation. Each tab shows a custom inline SVG demonstrating that benefit. Mirrors lesson 01's "Add a VM" hero in spirit (interactive in first 10 seconds) while serving lesson 02's 5-benefit structure.
- **Inline knowledge check** placed after the analogy section, like lesson 01. Tests the snapshot rollback case (the most non-obvious capability).
- **Hover-to-define terms tagged**: snapshot (§2), host (§4 ELI10), provisioning (§4 ELI10), downtime (§4 ELI10).

## Convention checks

| Item | Status |
| ---- | ------ |
| Seven sections present | yes |
| Apartment-building analogy threaded | yes |
| New visual conventions added to STYLE.md | not applicable — used existing primitives + custom inline SVGs only |
| New decisions logged to DECISIONS.md | not applicable — followed conventions established in lesson 01 |
| Action buttons pulse | yes — `.btn` and `.reveal-btn` with `@keyframes btn-pop` + reduced-motion override |
| No `transform-origin` attribute on SMIL rotation groups | verified via grep — no instances |
| Hover-to-define tooltips on first appearance | yes — 4 terms tagged with click/keyboard/Esc behavior |
| Inline knowledge check at counterintuitive moment | yes — snapshot rollback question after analogy |
| Mobile responsive | yes — 720px breakpoint mirrors lesson 01 |
| Dark mode toggle | yes — same CSS-variable approach as lesson 01 |
| Recap card with checkmark list | yes — 5 takeaways, one per benefit, plus next-lesson hook |

## Items deliberately deferred

- Per-benefit deep-dives (snapshot mechanics, mobility internals, HA orchestration) — separate lessons.
- VMware product names — introduced in lesson 03+.
- Resource scheduling — explicitly named as the next lesson at the end of the recap.
