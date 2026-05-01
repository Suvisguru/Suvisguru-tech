# Production notes — Lesson 07: SDDC and public cloud

## Files produced
- brief.yaml, lesson.md, flashcards.yaml (10), quiz.yaml (3)
- diagram.svg (side-by-side: on-prem SDDC and AWS, both with identical layer y-positions)
- animation.html (5 modes: compute, storage, network, management, cloud)
- /preview-lesson-07.html (5-tab layer tour ending with "→ Cloud")

## Alignment audit performed pre-ship
- diagram.svg: Both stacks (on-prem and AWS) use identical layer y-positions — Management y=120-180, Services y=180-300 (3 boxes each 144 wide × 14 gap × 3 = 460 wide), Hardware y=300-380. All adjacent layers abut at integer y boundaries. Stacks at x=70-530 (left) and x=570-1030 (right), symmetric around canvas mid (550). ✓
- animation.html each mode: Mgmt band y=110-170 abuts services y=170-290 abuts hardware y=290-370. Services row 3 boxes equal width (190+15+190+15+190 = 600 within stack 600 wide; gap 15 each, but 0 padding). Wait — let me re-verify: services x=0,205,410 width 190 each; gaps = 205-190=15 and 410-395=15. Equal. ✓
- preview-lesson-07.html hero stage SVG: viewBox 700×320. buildLayer function produces identical structure for each mode; only highlighting differs. Mgmt y=40-90 abuts Services y=90-200 abuts Hardware y=200-260. ✓

## Convention checks
- No `transform-origin` on rotation groups (none present).
- Action buttons pulse.
- 5 hover-to-define terms tagged: SDDC, vSAN, NSX, software-defined (implicit), hyperscale.
- Inline knowledge check after analogy.
- Apartment-building analogy extended (city, software-defined).
- Mobile responsive at 720px.
