# Style guide

This document defines the visual, narrative, and interaction language for every lesson produced on the platform. Lesson 800 must look like it came from the same studio as lesson 1.

When in doubt, copy from an existing lesson rather than invent. Inventing is the enemy of consistency.

## Visual language

### Color encoding

Color carries meaning. Do not use color decoratively.

- **Networking traffic:** teal/blue family. Packet payload uses teal #1D9E75. Patch cables use blue #378ADD with darker shadow stroke #0C447C.
- **Storage I/O:** coral/amber family. I/O payload uses coral #D85A30.
- **Encapsulation overlays:** purple #7F77DD for tunneling protocols (Geneve, VXLAN, GRE). Amber #FAC775 for layer-2 tags (VLAN, QinQ).
- **Failure states:** red #E24B4A. Reserved exclusively for failed paths, dead links, error states.
- **Healthy/active state:** green #5DCAA5. LEDs, healthy components, success indicators.
- **Inactive/standby:** gray #5F5E5A. Components present but not on the current path.

Backgrounds and structural elements use neutral grays. Color appears only where it teaches.

### Hypervisor band

When a frame shows the hypervisor as an explicit visual element, it renders as a horizontal slate band:

- Fill #3F4A5E with stroke #1F2433.
- Decoration: three horizontal hairlines #536179 at 0.6 opacity, suggesting "code layer."
- Label: light text #E8E8E0, sans-serif 13px weight 500, letter-spacing 1.5px, centered.
- Default dimensions: 480 × 30 (width matched to a default rack-server-rear).
- Renders between host (below) and VMs (above). Never as a sidebar.

This slate (#3F4A5E) is reserved for software-layer abstractions and does not appear elsewhere in the palette.

### VM tile

A VM renders as a small labelled card:

- Body: rounded rect rx 6, fill #F4F4F0, stroke #5F5E5A 1.2px.
- Header bar: top 18px tall, top corners rounded only, fill #5F5E5A.
- Header text (VM name): white #FFFFFF, sans-serif 11px weight 500, left-aligned 9px from edge.
- OS pill: 34 × 16, rx 3, fill #A8A8AC, white 11px text centered.
- Role/app label: 11px #3A3A3A.
- Activity bar: 80 × 4 track, rx 1, fill #E0E0DE; fill rect #5A6B81.
- Status dot (top-right at (110, 9)): 2.5px radius. Idle #5DCAA5 opacity 0.4; active opacity 1.0; failed #E24B4A opacity 1.0.
- Default dimensions: 120 × 64.

### Utilization meter

A horizontal bar showing CPU/RAM utilization on a server or host:

- Track: fill #E0E0DE, stroke #9D9D9D 0.5px, rx 2.
- Fill: single color #5A6B81 regardless of percentage. Color does *not* encode value — fill level and numeric label do.
- Label: 9px weight 500 #3A3A3A, centered.
- Default dimensions: 100 × 18.

### Vertical stacking

In any frame showing a virtualized host, the rendering order from bottom to top is: physical host → hypervisor band → VMs. The hypervisor band always sits *between*. Never reorder.

### Hardware aesthetic

Servers render as recognizable rear panels in light silver chassis (#A8A8AC) with rack ears, mounting screws, two PCIe slots (one with a 2-port NIC card showing visible RJ45 jacks, one empty with vent slits), a center I/O cluster, and dual hot-swap PSUs with circular fan grilles. PSU fans rotate continuously via SMIL animation at 4–4.5s per rotation to communicate "powered on."

The canonical rack-server-rear primitive lives at `/library/primitives/vmware/rack-server-rear.svg` with viewBox 480 × 200. PSU fans rotate via SMIL animateTransform with offset durations (top 4.2s, bottom 4.5s) so they never appear locked together. NIC port LEDs: idle r=1.5 opacity 0.4; active r=2.2 opacity 1.0.

Top-of-rack switches render as dark chassis (#2A2A2E) with a status LCD panel on the left, a row of 12-16 RJ45 ports across the middle (each with an activity LED above), and SFP+ cages on the right.

Storage arrays render with visible front-panel disk bays.

Cloud service icons (AWS, Azure, GCP) render as flat, recognizable shapes — never photorealistic. Reuse the official-style iconography vocabulary but do not lift official icons. The platform's house version is consistent across clouds: same line weight, same corner radius, same level of abstraction.

Do not invent new hardware shapes per lesson. Pull from `/library/primitives/`.

### Cable conventions

Cables are cubic Bezier curves. Two non-negotiable constraints: the cable visually plugs into a specific identifiable port on each end, and the animated packet's motion track follows the same Bezier coordinates. Packet and cable cannot diverge. If they appear to diverge, the lesson is broken.

Cable rendering is two stacked strokes: a 5px outer dark stroke (#0C447C) at 0.5 opacity, and a 2.5px inner stroke (#378ADD) at full opacity. Both with `stroke-linecap: round`.

### Encapsulation shells

When a packet acquires a header (VLAN tag, Geneve outer, IP header), render it as a labelled shell *around* the payload, not next to it. Shells appear at the boundary where encapsulation occurs and dissolve at the boundary where it's stripped. Nested shells stack outward.

Shell colors:
- VLAN tag: amber fill #FAC775, stroke #854F0B, label like "VLAN 10".
- Geneve/VXLAN outer: purple fill #CECBF6, stroke #534AB7, label "Geneve" or "VXLAN".
- IP/TCP layers (when shown explicitly): blue family.

### Typography

Two weights only — 400 regular, 500 bold. Sentence case for all labels. No ALL CAPS. No mid-sentence bolding.

Sizes inside SVG: 14px for component labels, 12px for subtitles, 11px minimum for any text inside the visualization. Section headings outside the visualization follow standard h1=22px, h2=18px, h3=16px.

The 11px floor applies to *primary* content text — component labels, status text, body labels, utilization values. Hardware sub-component labels inside primitives (PSU, I/O cluster, NIC card markings, "empty PCIe" markings, and similar) are decorative texture conveying type-of-thing visually rather than primary information; they are exempt from the floor and may render below 11px when primitives are scaled in compositions.

### Backgrounds

Widget backgrounds are transparent. The host page provides the surface. Never set a background color on the SVG itself.

## Motion language

### Pacing

A standard animation period is 8-10 seconds for one full cycle. The animation loops automatically and includes pause/play and a speed slider (0.3x to 2x).

### Stage labels

Every animation displays a current stage label outside the SVG (e.g., "TOR switch fabric"). The label updates as the packet/request crosses defined fraction thresholds along the motion path. Stage labels are written in plain language — "physical cable up" not "L2 transmission medium."

### State indicators

Components light up only when the packet/request is at or near them. Port LEDs brighten and grow slightly (r=2.2 active vs r=1.5 idle). Components that pulse continuously (PSU fans, status LEDs unrelated to the flow) communicate "the system is alive" — they do not encode the packet's location.

### Mode toggles

When a lesson has variants (L2/L3/NSX, hit/miss, success/failure, before/after), expose them as mode buttons above the animation. Switching modes resets the cycle and changes which shells appear and which labels are shown — but the motion track itself stays consistent across modes where possible.

## Narrative language

### Section voice

Each of the seven lesson sections has a distinct voice. The factory must hit each consistently.

- **Concept explanation:** Neutral and authoritative. Defines without judgment. "Virtualization is the abstraction of computing resources from the physical hardware they run on."
- **Before / after:** Slightly storytelling. Set the scene. "Before virtualization, every application that needed an operating system needed a dedicated physical server. A medium-sized company might own 200 servers, with the average one running at 5% utilization."
- **Analogy:** Vivid, concrete, sensory. Pick one analogy and commit. "Think of a single physical server as a large house. Without virtualization, only one family lives in the entire house, and most of the rooms stay empty."
- **ELI5:** Conversational, gentle, zero jargon. "Imagine your computer is like a big toy box. Normally only one toy can play at a time. Virtualization lets lots of toys take turns so the toy box is always being used."
- **ELI10:** Same warmth as ELI5 but adds correct terms. "Virtualization is software called a hypervisor that pretends to be a computer for each operating system that runs on top of it. The real computer underneath gets shared, so one physical machine can host many virtual ones at the same time."
- **Real-world scenarios:** Specific and concrete. Name the company type. State the problem. Show the solution. "A regional bank running 80 legacy applications on aging Windows Server 2008 hardware uses VMware to consolidate them onto 6 modern hosts, cutting power and rack costs by 70% and finally allowing snapshot-based DR."
- **Flashcards and quiz:** Direct, no preamble. Question, answer.

### No jargon without immediate definition

If a term appears that wasn't defined in a prerequisite lesson, define it inline on first use. "VXLAN (a way to wrap one Ethernet frame inside another so it can travel across a routed network)" — not just "VXLAN."

### Sentence rhythm

Mix sentence lengths. Long explanatory sentences earn their length by being followed by short anchoring ones. Short sentences land. They give the reader a beat. Then the next idea begins.

## Interaction language

### Action buttons pulse

Primary action buttons in lesson UIs — the buttons the learner is being prompted to click ("Add a VM," "Virtualize the house," "Show answer," "Reveal," etc.) — must have a subtle idle pulse animation. The button gently scales (1.0 → ~1.03) and its shadow expands and contracts on a 2.2-second loop. Pause the animation on `:hover` and `:disabled` so it doesn't fight other states. Respect `prefers-reduced-motion: reduce` and turn it off.

This applies to *primary* action buttons only. Toggle / tab / accordion controls do not pulse — they signal "choose between" rather than "perform action," and they should be obviously clickable through contrast and hover state instead.

The goal is "visible in peripheral vision" rather than "demanding attention." A first-time learner should immediately recognize where the action is without reading instructions.

### Pause-and-question quizzes

Quiz questions are pause-the-animation prompts whenever possible: "I've stopped the packet here. What happens next, and why?" The learner predicts the next state from what they've just seen. This is the only assessment style that tests mental-model formation rather than memorization.

### Flashcards

One concept per card. Front: a question or a term. Back: 1-3 sentences. No flashcard contains everything — together, the deck covers the lesson's core terms.

### Pacing controls

Every animation provides pause/play and speed (0.3x to 2x). Pause is for live teaching — the trainer pauses on a critical moment and asks the class. Speed is for reviewing on second pass.

## Lesson preview page

Every lesson ships as a single-page interactive HTML preview at `/preview-lesson-{nn}.html`, hand-authored for now and replaced by a render pipeline once the patterns are stable. The reference implementation is `preview-lesson-01.html`. Copy from it; do not invent.

### Goal

A first-time learner — general computing literacy, zero exposure to the topic — opens the page and is doing something within ten seconds. They scroll through, interact with inline widgets, get one inline knowledge check, and finish with a recap card. The text is short. The visualizations carry weight.

### Page chrome

- **Sticky top bar.** Brand label on the left ("vSphere Fundamentals"), a dark-mode toggle on the right. Bottom edge of the bar carries a 2px scroll progress fill in the slate accent color.
- **Dark mode.** Light is the default. The toggle persists to `localStorage` (key `lesson-theme`). All colors flip via CSS variables on `[data-theme="dark"]`.
- **Reveal on scroll.** Each section has a `.reveal` class that fades in (opacity + 20px translateY) when it enters the viewport. Respect `prefers-reduced-motion: reduce` and disable.
- **Back-to-top button** appears once the reader has scrolled past the hero.
- **Mobile breakpoint at 720px.** Cards stack to one column, the analogy mapping table collapses to one column, ELI tabs become vertical, the animation iframe shrinks.

### Hero

Centered, eyebrow + h1 + one-sentence subtitle + meta pills (read time, level, domain). Below that — and this is the key — an **interactive widget**. The widget is the lesson's main idea, demonstrated in five seconds. For lesson 01 it's "click +Add a VM eight times and watch the host fill up." Whatever the lesson's central transformation is, the hero widget shows it being done by hand.

The hero widget renders inline SVG using primitives from `/library/primitives/{domain}/`. Embed the canonical primitive's symbol via `<defs>` and reference with `<use>` rather than redrawing. A small `stage-readout` text below the widget narrates state in plain language ("3 VMs on this host. Utilization: 27%.").

### Section pattern

Every numbered lesson section uses the same shape:

1. **Section eyebrow** (12px caps, slate accent, e.g., "Section 1 · Concept").
2. **Section heading** (32-38px, weight 500, line-height 1.2, slight negative letter-spacing).
3. **Chunked prose.** Paragraphs are 1-3 sentences. Walls of text are forbidden. Long paragraphs from `lesson.md` are broken at natural sentence beats.
4. **One pull quote per section** for the lesson's most quotable line — italic, slate left-border, 22-24px.
5. **One inline visualization or widget** for each concept the section introduces. Don't park visualizations at the end. They appear next to the text that motivates them.
6. **Optional callout** for "hold onto this" reinforcement, slate left-border, soft cream background.

### Inline visualizations and widgets

Each section earns its own widget where useful:

- **§1 Concept.** The hero widget already does the work. No additional widget needed unless explaining a sub-concept.
- **§2 Before/after.** A toggle widget showing the "world before" vs "world after" — for lesson 01 this is the 200-server datacenter grid that toggles to 6 hosts. Toggle pill style, big stat numbers updating with the toggle.
- **§3 Analogy.** A morphing illustration. Click a primary action button to transform the analogy state (e.g., house → apartment building). Below the visual, an analogy mapping table (left column = analogy element, arrow, right column = technical concept).
- **§4 ELI5/ELI10.** A pill-shaped tab toggle, not stacked text. Picking your level is a primary interaction, not a side note.
- **§5 Real-world scenarios.** Accordion cards. Header row shows industry icon + headline + key stat (e.g., "$1.1M down from $4.2M"). Click to expand for the full story and the trade-off. Don't show all four expanded by default — let the reader scan headlines first.
- **§6 Animation.** Embedded iframe of the lesson's animation.html. Mode toggle + pause/play + speed slider as defined elsewhere in this document.
- **§7 Flashcards.** 3D-flip cards in a responsive grid (auto-fit, minmax 290px). Front: card number + question + "Click to flip" hint. Back: answer in slate fill, white text. CSS `transform-style: preserve-3d` and `backface-visibility: hidden`.
- **Quiz.** Cards with a "Show answer" reveal button (which itself pulses per the action-button rule). Inside the reveal: green-tinted answer block + cream-tinted reasoning block.

### Inline knowledge check

After the section that introduces the most counterintuitive idea (for lesson 01, this is the analogy section's isolation guarantee), insert one **inline multiple-choice question**. Three options. Click any option for instant feedback — correct option highlights green, wrong option red, with explanatory text that addresses the specific misconception.

This is not a quiz at the end. It's a 30-second confidence check at the moment the learner most needs one.

### Hover-to-define for technical terms

Every technical term that a first-time learner could trip on gets a dotted-underline + tooltip on its **first prominent appearance** in the prose. Subsequent appearances are bare text — a learner sees the underline once, learns the meaning, reads bare text after.

- Visual: dotted underline in the slate accent color, color shift to slate on hover.
- Tooltip: dark slate background, white 14px text, 280px max width, anchored above the term with a small arrow.
- Interaction: hover (desktop), click or tap to pin (mobile and click-to-pin desktop), Enter or Space when keyboard-focused, Esc to close, click outside any term to close all.
- Tooltip writing: 1-2 sentences in plain language. Include the analogy mapping where relevant ("isolation — like the locks on each apartment door").

Lesson 01 tags: virtual machine, operating system, hypervisor, host, isolated, utilization, capacity planning. For each new lesson, identify the terms a first-time learner doesn't know yet and tag the first appearance.

### Recap card

The lesson ends with a recap card, not a "you're done" footer. Style: subtle gradient background, 1px border. Contents:

- A "Lesson N complete" badge in success-green soft.
- A single-sentence headline that reinforces the lesson's spine ("Hold onto the superintendent.").
- A 3-5 item checkmark list of takeaways — short sentences a learner could mentally check off.
- A closing paragraph that hooks into the next lesson without spoiling it.

### Color and typography

Body text 17-18px, line-height 1.65-1.7. Display headings have negative letter-spacing (-0.5 to -1.2px). Two type weights only (400, 500) per the existing typography rule, with 600 reserved for tooltip eyebrow labels and stat values.

Color variables are CSS custom properties on `:root`, shadowed under `[data-theme="dark"]`. Slate accent `#3F4A5E` is the only saturated color used at chrome scale; warm cream `#FAFAF6` for the page; success green and warn coral are reserved for state callouts (knowledge check feedback, scenario tradeoffs, complete badges).

### What never changes (for the preview page specifically)

- The hero contains an interactive widget that demonstrates the lesson's central idea.
- Every concept gets its own inline visualization. No parking visualizations at the end.
- Technical terms are tagged on first appearance with hover/click definitions.
- One inline knowledge check at the right moment.
- Action buttons pulse per the existing rule.
- Mobile-first responsive layout. Test below 720px width.
- Dark mode and scroll-progress bar are standard chrome.
- The recap card is the closing pattern, not "you're done."

## Kubernetes-specific conventions

Established in K-COM Lesson 01 (`preview-kubernetes-lesson-01.html`). When in doubt, copy from there.

### Pod state colors

Pods render via the `pod-tile` primitive (`/library/primitives/kubernetes/pod-tile.svg`). State is encoded in the header bar fill, the status dot color, and the body border:

- **Running** — header `#3F4A5E` (slate), dot `#5DCAA5` (healthy green), body cream `#F4F4F0`. The default.
- **Pending** — header `#5E4A8E` (purple), dot `#FAC775` (gold), body `#FFFCF5`. Pulses (1.4s opacity loop) to communicate "waiting / starting."
- **Failed** — header `#8E2A2A` (deep red), dot `#E24B4A` (failure red), body `#FBE8E8` with red border. Reserved for terminal failure states.
- **Terminating** — header `#9D9D9D` (gray), dot gray, body `#F0F0F0` with **dashed** border. Communicates "ending / being removed."
- **Drift** — header `#B85829` (warn coral), dot gold, body `#FBEDE3`. Used when a pod exists outside the Deployment's ownerReferences (e.g., created by hand) and the controller is about to remove it.

Coral (#B85829) for drift extends the existing storage I/O coral family — both communicate "an in-flight thing the system is acting on." Distinct from failure red (#E24B4A) which means terminal.

### Control plane vs hypervisor band

Both the VMware `hypervisor-layer` and the Kubernetes `control-plane-band` primitives use the same slate fill (`#3F4A5E`) — software-layer abstractions per the original 2026-04-29 decision. They are visually distinguished by their decoration:

- **Hypervisor band:** three horizontal hairlines (`#536179` at 0.6 opacity) — suggests "code layer."
- **Control plane band:** four small "component dots" along its length, labelled `kube-apiserver`, `etcd`, `kube-scheduler`, `controller-manager` — suggests "this band is composed of multiple coordinating services."

### Subtopic header accent colors (per-subtopic structure)

When a lesson uses the per-subtopic format, each subtopic's header carries a distinct left-border accent so the reader can recognise "I'm in subtopic 3" from peripheral vision. The first ten accent colors:

- s1 `#3F4A5E` slate · s2 `#5E4A8E` purple · s3 `#2E7A8C` teal · s4 `#1F8A60` green · s5 `#B85829` coral
- s6 `#8E2A2A` deep red · s7 `#1A6FA8` blue · s8 `#5C7A1F` olive · s9 `#2E5A8E` indigo · s10 `#B85C9E` magenta

Same palette is used for the hero "journey" station numbers so the journey colors match each subtopic's later left-border.

### Preview filename per domain

VMware previews use `preview-lesson-NN.html` (existing series). Kubernetes previews use `preview-kubernetes-lesson-NN.html` so the two domain sequences don't collide at the repo root. Future domains follow the same pattern: `preview-{domain}-lesson-NN.html`.

## What never changes

- The packet/request motion track follows the visible cable/connection trajectory exactly. No exceptions.
- Color carries meaning, never decoration.
- Every lesson has all seven sections in fixed order.
- The analogy in section 3 is referenced consistently in ELI5 and ELI10.
- Every lesson ships with flashcards and a quiz.
- The 800th lesson must look like the 1st.