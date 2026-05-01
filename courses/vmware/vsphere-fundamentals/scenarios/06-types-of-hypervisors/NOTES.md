# Production notes — Lesson 06: Types of hypervisors

## Files produced
- brief.yaml, lesson.md, flashcards.yaml (10), quiz.yaml (3)
- diagram.svg (side-by-side stacks; both share hardware bottom y=480)
- animation.html (2 modes: type1, type2)
- /preview-lesson-06.html (2-tab Type 1/Type 2 hero)

## Alignment audit performed pre-ship
- diagram.svg: Type 1 stack — VMs y=240-380 abut Hypervisor y=380-430 abut Hardware y=430-480. Type 2 stack — VMs y=200-320 abut Hypervisor app y=320-380 abut Host OS y=380-430 abut Hardware y=430-480. Both stacks share hardware bottom at y=480; Type 2 starts higher because of the extra layer. ✓
- animation.html Type 1: VMs y=80-260 abut Hypervisor y=260-320 abut Hardware y=320-400. ✓
- animation.html Type 2: VMs y=80-220 abut Hypervisor app y=220-280 abut Host OS y=280-340 abut Hardware y=340-410. ✓
- Hero Type 1 SVG: VMs y=46-186 abut Hypervisor y=186-236 abut Hardware y=236-296. ✓
- Hero Type 2 SVG: VMs y=46-156 abut Hypervisor app y=156-200 abut Host OS y=200-244 abut Hardware y=244-296. ✓

## Convention checks
- No `transform-origin` on rotation groups (none present).
- Action buttons pulse.
- 4 hover-to-define terms tagged: bare-metal, kernel, Type 2, host operating system.
- Inline knowledge check after analogy.
- Apartment-building analogy extended (purpose-built building vs basement apartments).
- Mobile responsive at 720px.
