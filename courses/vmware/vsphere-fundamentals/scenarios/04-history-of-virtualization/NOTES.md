# Production notes — Lesson 04: A short history of virtualization

## Files produced
- brief.yaml, lesson.md, flashcards.yaml (10), quiz.yaml (3)
- diagram.svg (timeline with 6 milestones, equal spacing 180px between)
- animation.html (6 era modes: 1960s, 1998-2001, 2003, 2006, 2013, 2024)
- /preview-lesson-04.html (6-tab era tour hero, full lesson)

## Alignment audit performed pre-ship
- Diagram timeline: 6 milestones at x=100, 280, 460, 640, 820, 1000 — equal 180px spacing verified. Each milestone has icon at y=180, year label y=170 above, title y=110, description y=240/260 below.
- Animation 1998-2001 mode: "before" box and "after" box at translate(140, 130) and (420, 130) — same y, equal width 200, ~70px gap between. Symmetric.
- Animation 2001 mode: VMs y=36-116 abut Hypervisor y=116-138 abut Hardware y=138-190. All adjacent layers share integer y boundaries.
- Animation vMotion mode: source/dest hosts at translate(140, 220) and (680, 220) — same y, equal width 220, hosts symmetric around canvas mid (520).
- Hero era stage SVG: viewBox 720×280 verified for each of 6 eras. 1960s mainframe centered (mainframe x=220-500, canvas mid x=360 → mainframe center x=360 ✓). 2001 ESX VMs/Hypervisor/Hardware abut.

## Convention checks
- No `transform-origin` on rotation groups (none present in this lesson).
- Action buttons pulse (`.btn`, `.reveal-btn`) per rule.
- 4 hover-to-define terms tagged: mainframes, x86, public cloud, containers.
- Inline knowledge check after analogy section.
- Apartment-building analogy extended (city construction history).
- Mobile responsive at 720px.
