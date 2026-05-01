# Production notes — Lesson 03: VMware, vSphere, and the components

## Files produced
- brief.yaml, lesson.md, flashcards.yaml (10), quiz.yaml (3)
- diagram.svg (vCenter at top, two hosts, shared datastore, with vSwitch detail)
- animation.html (5 modes: esxi, vcenter, vms, datastores, networks)
- /preview-lesson-03.html (5-tab component tour hero, full lesson)

## Alignment audit performed pre-ship

For every illustration in this lesson, the seven-point alignment protocol from
`/STYLE.md` was walked:

- **diagram.svg.** vCenter centered at canvas mid (550); host groups at x=150 and x=570 (centered with equal margins); inside each host VMs (y=10-70) abut hypervisor (y=70-90) abut chassis (y=90-200); connector lines vCenter→hosts and hosts→datastore use the same trunk pattern; datastore centered (x=350-750) below hosts. Verified: every adjacent layer shares an integer y boundary.
- **animation.html.** Each of the 5 modes verified independently. ESXi mode: VMs y=0-80 abut hypervisor y=80-110 abut chassis y=110-270. vCenter mode: trunk from vCenter (520, 160) → splitter (165) → 5 host tops (230). VMs mode: single VM with OS layer y=80-120 abut app layer y=130 (8px gap intentional for visual separation between OS and app). Datastores mode: connector lines from each host bottom-center to datastore top edge. Networks mode: VM-to-vSwitch connectors at y=110-140; packet animation along verified path.
- **preview-lesson-03.html hero stage.** ViewBox 640 × 280. ESXi tab: VMs y=50-110 abut Hyper y=110-138 abut Chassis y=138-228. vCenter tab: vCenter at y=30-90, trunk to (320, 115), splitter (115), 5 hosts at y=130. VMs tab: single large VM with internal OS/App/Resources layout. Datastores tab: 2 hosts top, datastore bottom, dashed connectors. Networks tab: 4 VMs → vSwitch → NIC, packet animation path verified.

## Convention checks
- No `transform-origin` attribute on rotation groups (none present).
- All primary `.btn` and `.reveal-btn` carry the pulse animation per the action-button rule.
- 5 hover-to-define terms tagged in preview (ESXi, vCenter Server, datastore — plus 2 contextual).
- Inline knowledge check after analogy section (vCenter-down case).
- Apartment-building analogy extended (property management company = vCenter).
- Mobile responsive breakpoint at 720px.

## Items deliberately deferred
- Per-component deep dives (vMotion mechanics, HA, DRS) — separate later lessons.
- vSphere-specific features beyond the five core components — later lessons.
