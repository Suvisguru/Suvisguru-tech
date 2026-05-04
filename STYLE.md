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

### Layman-first scaffolding components

The components in this subsection wrap and frame the seven content sections. Their purpose is to earn a layman's attention before the content tries to teach. Every lesson preview must include each of them.

#### Nightmare opener

The first element below the lesson H1, before the existing intro paragraph.

- Header label: "🚨 The 3 AM Nightmare" — 13px caps, weight 500, warm coral accent (uses the existing warn coral, not failure red `#E24B4A`).
- Body: 2-3 sentence scenario in second person. Sensory and time-anchored.
- Closing line: "This lesson is about why that happens — and the [N-line] fix that prevents it."
- Visual treatment: subtle warm-amber background tint, 1px border in the warm coral family, slightly distinct from regular section panels but not garish.
- Width: same as body prose. Padding: same scale as the existing callout.

#### One-sentence stamp

Boxed single-sentence takeaway, repeated in two placements:

- **Top placement:** immediately under the Nightmare opener.
- **Bottom placement:** immediately above the recap card.

Specs:

- A bolded boxed line with a strong border colour from the slate accent palette.
- Center-aligned text, 19-20px (slightly larger than body).
- Leading icon `🎯` and a "If you remember nothing else:" lead-in.
- Identical text at both placements. Repetition is the point.
- Contains zero parenthetical jargon — see QUALITY.md.

#### District line

A single line just under the breadcrumb header (above the Nightmare opener), placing the lesson in the domain's unified analogical universe.

- Format: `📍 Today's stop in [Universe]: **[District Name]**.`
- 14-15px, regular weight on the prefix, weight 500 on the district name.
- Subtle muted color until the district name, which uses the lesson's subtopic accent colour if present.
- One line, no exposition.

#### Translation Legend

A two-column table inside Section 3 (Analogy), placed after the prose narrative and before the existing analogy mapping bullet list (which it replaces).

- Two columns. Headers: "In the story…" and "…in [Domain] (e.g., …in Kubernetes)".
- Vertical divider rule between columns at 0.5px slate.
- Left-column entries are jargon-free — things the reader can picture.
- Right-column entries use the canonical technical vocabulary (see "Vocabulary canonicalization" below).
- 5-10 rows. Fewer feels thin; more is overload.

#### Pause-and-check

A short multiple-choice comprehension check, inserted twice mid-lesson:

- **Position 1:** between Section 1 (Concept) and Section 2 (Before/after).
- **Position 2:** between Section 4 (ELI5/ELI10) and Section 5 (Real-world scenarios).

Specs:

- Header: "⏸ Pause and check" — 14px, slate accent.
- A single multiple-choice question with 2-3 options. Click any option for inline reveal.
- Reveal includes the correct answer plus a one-sentence "why" that surfaces the mental model.
- Lighter visual weight than the existing inline knowledge check — these are confidence pulses, not gates.
- Tested per QUALITY.md: would the immediately preceding paragraph equip the reader to answer correctly?

#### Common Misconceptions panel

Inserted at the start of Section 7, immediately before the flashcards.

- Header: "Common Misconceptions" — same heading style as other section sub-headings.
- Three myth/truth pairs per lesson. Exactly three. No more, no less.
- Each pair is a small card with two rows:
  - **Myth row:** red/strike accent (uses the existing failure red family at reduced saturation), prefix "**Myth:**", one sentence.
  - **Truth row:** green/check accent (uses the existing success green family), prefix "**Truth:**", one sentence.
- Three cards stack vertically and should fit within one screen on desktop.

#### Analogy-stops-here callout

Inline within Section 3 (Analogy), immediately after the analogy is fully introduced, used only when the analogy has a known cliff.

- Format: `⚠️ *The analogy stops here: [one-sentence cliff].*`
- Italic, narrower than full-section panels (same width as a body paragraph).
- Yellow/warn-coral accent, low saturation. Subtle, not loud.
- One sentence, no paragraph.
- Used selectively. Not every lesson needs one — a generic disclaimer dilutes the warning when it matters.

#### Skip-if-new tag

A pill at the start of paragraphs that are correct and useful but unnecessary for absolute beginners (e.g., cgroup v1 vs v2 details, Raft consensus internals, hydrophone vs sonobuoy).

- Pill content: `[ deep dive — skip if new ]`.
- Muted/grey pill (existing inactive `#5F5E5A` family), small, inline at start of paragraph.
- The tagged paragraph itself renders at slightly reduced opacity (0.85) so a beginner's eye glides past.
- Applied at paragraph or sub-section granularity, not sentence level. 1-3 per lesson maximum, only in Module-2-and-deeper lessons.

#### Persistent concept rail

A floating left rail visible while scrolling on desktop.

- Width: 180-220px. Position: fixed-left.
- Vertical list of concept-mastery items (one per lesson in the course), each a single short label describing concepts mastered (not lesson titles).
- Three states with status icons:
  - `✓` (success green) — completed
  - `▶` (slate accent, current) — current lesson, with "← you are here" suffix
  - `○` (muted gray) — future
- Each item is text + icon only, no boxes.
- Visibility: rendered only at viewport ≥ 1240px (where the centred 820px main + the 170-180px rail + breathing space all fit). Below 1240px the rail is hidden; the K-Town dot-strip already serves the "where am I in the journey" function for narrower viewports, so duplicating it as a horizontal bar would clutter mobile.
- Hard-coded per lesson. No state persistence — the rail reflects "this lesson's position in the journey," not actual user progress.

#### CYOA quiz reveal

Variant of the existing quiz reveal pattern. One CYOA question per lesson; the other quiz questions remain factual.

- Framing line above the reveal trigger: "🎬 Choose Your Own Adventure".
- Story-style scenario (1-2 sentences) ending with "**Click to see what happens. ▼**".
- Reveal can include a small ASCII/text graphic for the failure case — a tiny pixel illustration of the disaster (a sinking ship, an OOM-killed pod, an empty replica counter). The visual lands the moment of failure.
- Reveal can be longer than other quiz answers — this is the *memorable* one.
- The technical lesson must be inferable from the reveal alone. No separate "and the lesson is…" tag.

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
- The Nightmare opener appears below the H1 before any other content.
- The one-sentence stamp appears at top and bottom, identical at both placements.
- The district line appears at the top tying the lesson to its domain's unified analogical universe.
- Two pause-and-checks appear mid-lesson at the prescribed positions.
- A Translation Legend table replaces the bare "mapping" bullet list inside Section 3.
- A Common Misconceptions panel (exactly three myth/truth pairs) opens Section 7.
- An "analogy stops here" callout appears inside Section 3 when the analogy has a known cliff.
- "Skip if new" tags mark advanced paragraphs in Module-2-and-deeper lessons.
- A persistent left-rail concept map renders the lesson's place in the journey.
- One quiz question per lesson is a CYOA-style story reveal; the others remain factual.

## Vocabulary canonicalization

Across lessons within a domain, multiple synonyms for the same concept create drift and confuse beginners. Each domain maintains a canonical-term list. Lessons use canonical terms throughout body text and quiz answers; "acceptable on first mention" terms may appear once in parentheses as a gloss on the canonical term, never as the standalone term in subsequent uses.

When in doubt, search the existing course for the term and align with the predominant usage rather than introduce a new variant.

### Kubernetes canonical vocabulary

| Canonical | Acceptable on first mention only (parenthetical gloss) | Avoid |
|---|---|---|
| **desired state** | "what you want" | "the spec", "your declared intent", "what you said" — as standalone terms |
| **actual state** | "what's running" | "current state", "live state", "reality" |
| **controller** | "the small program watching forever" | "the loop", "the reconciler" — as the standalone term |
| **reconciliation loop** | "the loop" *(only after first mention in a lesson)* | "the reconcile cycle", "the watch loop" |
| **Pod** *(capitalised)* | — | "pod" (lowercase) when referring to the K8s object |
| **the kubelet** | "the node agent" | "the agent" — ambiguous |
| **the API server** | "the only door in" | "the K8s API" — implies the protocol, not the component |

VMware, AWS, and other domain canon lists will be added as those courses develop a long-tail of synonym drift.

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

Lesson-N.5 primers (per the 2026-05-02 prerequisite-primer DECISIONS entry) substitute a hyphen for the dot to stay filesystem-friendly: `preview-{domain}-lesson-N-5.html` — for example, `preview-kubernetes-lesson-7-5.html`. No leading zero on the integer part.

### Unified analogical universe — Kubernetes (K-Town)

Every Kubernetes lesson is set in a single shared world: **K-Town**. Each lesson zooms into one *district* of the city. This solves the problem of beginners burning cognitive energy learning a fresh analogy every lesson. The cast and the city map persist; the lesson-specific analogy is a district within the city.

**The cast (recurring across all lessons)**

- **Mayor Katie.** The city's manager. Personifies Kubernetes itself. Appears in Lesson 01 ("the property manager") and is name-dropped in any lesson that needs a "Kubernetes did this" actor.
- **Podrick.** The unit/box/parcel that gets placed, moved, packed, deployed. Personifies the Pod and, by extension, a workload. Has a face on the small character illustration.
- **The Thermostat.** The wise old gadget, slightly grandfatherly, who explains control loops. Lives on the wall in every building of K-Town. Speaks in Lesson 03 and reappears as a knowing wink whenever a new reconciliation loop is introduced (Lessons 06, 13, 14).

Optional supporting characters used sparingly:

- **Captain Tini** (Lesson 12 — the well-trained ship captain in the harbour district).
- **Inspector Pause** (Lesson 15 — the silent guard at the door of every co-living unit).

These characters do not need fully drawn art on every page. A small recurring icon (silhouette) in the margins is enough.

**District map graphic**

A single SVG of K-Town renders once per lesson, just under the breadcrumb header, showing all 24 districts as pins on a stylised city map (18 from L01-L17 + L7.5, plus 6 added for L18-L44). Only the highlighted pin changes per lesson. Districts are reused across multiple lessons when the topic naturally lives in the same metaphor (e.g., L09/L18/L19 all use the Customs Warehouse).

**District-to-lesson mapping**

| Lesson | District / Setting |
|---|---|
| 01 | **Mayor's Office** (Katie running the city) |
| 02 | **Residential District** (houses vs apartment buildings) |
| 03 | **Climate Control Tower** (every building has thermostats — featured here) |
| 04 | **Port + Restaurant Row** (standard shipping containers + food courts) |
| 05 | **Industrial Kitchen Block** (vs a single toaster on someone's counter) |
| 06 | **Public Library** |
| 07 | **K-Town Rail Yard** (alpha branch line → main intercity) |
| 7.5 | **Foundation Tour** (Level 0 primer — a brief layman's intro to processes/OS/kernel) |
| 08 | **Office Tower with Utility Meters** |
| 09 | **Customs Warehouse** (forklifts moving standard containers) |
| 10 | **Bakery District** (recipes, ovens, cakes, ingredient lists, baker's seal) |
| 11 | **K-Town Bank Vault Quarter** |
| 12 | **K-Town Harbour** (lighthouse + ship + captain) |
| 13 | **K-Town International Airport** (control tower + terminals) |
| 14 | **City Hall — Permit Office** |
| 15 | **Co-Living Quarter** (Pod = co-living unit, NOT apartment — apartment is reserved for Lesson 02's container metaphor) |
| 16 | **K-Town Dispatch Office** (workforce dispatch — Deployments are rotating shifts; StatefulSets are assigned-seat employees; DaemonSets are the one-per-building watchman; Jobs are one-time work orders; CronJobs are scheduled maintenance rounds) |
| 17 | **K-Town Switchboard** (the city's telephone exchange and street-routing system — ClusterIP is the internal directory; NodePort is the public phone booth on each block; LoadBalancer is the dispatch operator routing calls; Ingress is the main-entrance turnstile; NetworkPolicy is the traffic rules) |
| 18 | **Customs Warehouse** *(reuse from L09)* — locker-rental front desk; the rental form is the PVC, the locker is the PV, the warehouse policy book is the StorageClass |
| 19 | **Customs Warehouse — Loading Dock** *(reuse from L09)* — the contractor-truck side; the CSI driver is a licensed contractor truck pulling in to install lockers, snapshot them, expand them, or re-tune them |
| 20 | **Permit Office — Configuration Window** *(reuse from L14)* — rate cards (ConfigMaps) at one window, sealed envelopes (Secrets) at another, with a back-room key minter (KMS) and bonded courier from a vault company (External Secrets Operator) |
| 21 | **Permit Office — Identity Bureau** *(reuse from L14)* — passports (ServiceAccounts), short-lived stamped travel passes (projected JWTs), and the certificate press (cert-manager) running the city's PKI |
| 22 | **K-Town Dispatch Office — Routing Board** *(reuse from L16)* — depot map, trucks with stickers (nodeSelector / affinity), warning signs (taints), driver permits (tolerations), city-wide spread rules (topology spread) |
| 23 | **K-Town Dispatch Office — VIP & Specialty Routing** *(reuse from L16)* — priority-class lane stickers, the specialty-equipment desk (DRA) for GPUs/FPGAs/NICs, and the same-NUMA-loop routing for latency-sensitive trucks |
| 24 | **Switchboard — Wiring Room** *(reuse from L17)* — behind the front desk: every apartment's phone connects via a wire (veth) into the building switchboard (node bridge); the contractor (CNI plugin) runs the wiring; trunk lines (encapsulation or native routing) connect buildings |
| 25 | **Switchboard — Customer Counter** *(reuse from L17)* — the new three-role layout: city-issued operating-license posters (GatewayClass), the building's listener bank (Gateway), and app-team-clipped route slips (HTTPRoute) |
| 26 | **Switchboard — Policy Wing** *(reuse from L17)* — three policy desks: City Council ordinances (AdminNetworkPolicy), building-manager rules (NetworkPolicy), default city ordinance shelf (BaselineAdminNetworkPolicy); plus a destination-by-name registry (FQDN policies) |
| 27 | **Watchtower — Identity & Permissions Bureau** *(NEW)* — the city's security tower at the edge: an identity desk (authentication: OIDC / SA tokens / certs) and a permissions desk (RBAC binders mapping subjects to verbs-on-resources) |
| 28 | **Watchtower — Admission Hallway** *(reuse from L27)* — past the auth desk: a stamping desk (mutating admission), a standards bench (Pod Security Admission), and a custom-rules counter (ValidatingAdmissionPolicy with CEL); with a policy-engine office and webhook switchboard behind |
| 29 | **Watchtower — Policy Library** *(reuse from L27)* — two cabinets side by side: the plain-K-Town-vernacular cabinet (Kyverno, YAML rules) and the formal-logic cabinet (OPA Gatekeeper, Rego); both produce the same standard filing report (PolicyReport CRD) |
| 30 | **Bank Vault Quarter — Trust Ledger** *(reuse from L11)* — supply-chain notarisation: declarations of origin (Cosign signatures), build manifests (SLSA provenance), contents inventories (SBOMs), all stamped by a notary (Sigstore / Fulcio) and logged in a public ledger (Rekor) |
| 31 | **Watchtower — Tenant Compound Aerial** *(reuse from L27)* — bird's-eye view of the tenant district: each compound is a namespace ringed by RBAC + NetworkPolicy + PSA + ResourceQuota + LimitRange; CIS audit (kube-bench) scoring posted on a public noticeboard |
| 32 | **Observatory — Logs & Metrics Telescope** *(NEW)* — high above K-Town with three instruments: the logbook telescope (logs collector), the star chart (metrics dashboard), and the OpenTelemetry router forwarding signals to specialist offices (Loki / Mimir / Prometheus / Grafana) |
| 33 | **Observatory — Tracing & Reliability Wing** *(reuse from L32)* — flight-data recorders for every request (distributed traces), kernel-level sensors (eBPF: Hubble / Pixie / Tetragon), and the public SLO board with burn-rate alarms |
| 34 | **Power Station — Demand-Based Capacity** *(NEW)* — three demand meters (HPA / VPA / KEDA) drive an outside substation manager (Cluster Autoscaler / Karpenter) procuring generators (nodes) from the city's rental fleet (cloud instance fleet) |
| 35 | **Power Station — Resilience Floor** *(reuse from L34)* — three resilience controls: the maintenance interlock (PDB), multi-zone wiring (topology spread + zone-aware nodes), and the regional substation (DR cluster in another city) |
| 36 | **Print Shop — Kustomize Press** *(NEW)* — master plates (base manifests) with transparency overlay sheets per environment (overlays/dev|staging|prod); the press combines them via `kubectl apply -k` |
| 37 | **Print Shop — Helm Chart Counter** *(reuse from L36)* — vendors arrive with sealed envelopes (Helm charts) containing complete poster sets + parameter sheet (values.yaml); the press runs the envelope (helm install), logs the run (release Secret), and the warehouse (OCI registry) holds notarised stamps |
| 38 | **Public Library — Argo CD Reading Room** *(reuse from L06)* — every cluster is a shelf; a librarian (Argo CD controller) consults the master catalogue (git) and ensures the shelf matches; visitor edits (drift) are reverted by selfHeal |
| 39 | **Public Library — Flux CD Wing** *(reuse from L06)* — same goal as Argo CD\'s reading room, different staffing: specialised desks (source-controller, kustomize-controller, helm-controller, notification-controller, image-automation) coordinate via paperwork (CRDs) |
| 40 | **Print Shop — Progressive Release Floor** *(reuse from L36)* — phased printing: 5% canary run alongside 95% stable; an inspector (AnalysisTemplate) watches metrics and either ramps up or pulls the new run off the press (auto-rollback) |
| 41 | **Permit Office — Advanced CRD Wing** *(reuse from L14)* — custom permit form designs (CRDs); inline validation rules (CEL); a conversion clerk (webhook) translating between form versions; deprecated-form retirement |
| 42 | **Workshop — Operator Builder's Bench** *(NEW)* — master craftspeople build custom assistants (operators) at standard workbenches (Kubebuilder); the workbench engine (controller-runtime) handles the boring infrastructure; assistants ship as sealed envelopes (Helm) or registered subscriptions (OLM) |
| 43 | **Switchboard — Service Mesh Wing** *(reuse from L17)* — every phone in the building has a sealed line (mTLS) issued by a central control board; sidecar mode (operator next to each phone) vs ambient mode (one operator per floor + dedicated department-line operators) |
| 44 | **Detective's Office — Investigation HQ** *(NEW)* — the last district: corkboard flowchart (triage methodology), evidence kit (kubectl describe, events, logs --previous, top, debug), list of usual suspects (image pulls, RBAC, MTU, certs, admission), drill schedule (chaos engineering / game days) |

**Crucial collision to avoid:** Lesson 02 uses "apartment = container." Lesson 15 must NOT also use "apartment = Pod" — they collide. Lesson 15 uses "co-living unit / shared studio loft = Pod" instead.

**Implementation rules**

- Every lesson opens with a one-line district pin in the format `📍 Today's stop in K-Town: **[District Name]**.`
- Every lesson includes the K-Town map graphic with the current district highlighted.
- Existing per-lesson analogies (the property manager, the apartments, the thermostat, etc.) are *retained* — the K-Town framing nests them, not replaces them.
- Do not introduce new districts without an approved DECISIONS.md entry.
- Do not introduce new recurring cast members without an approved DECISIONS.md entry.

**What NOT to do**

- Do not rewrite the existing analogies. Each one stays as is. K-Town is the wrapper.
- Do not exceed three recurring characters in regular use. Beyond Katie, Podrick, and the Thermostat, every additional character is overhead.
- Do not let the city framing crowd the actual content. It's a frame, not the lesson.

### Unified analogical universe — Vanilla Kubernetes (K-Frontier)

K-VAN (vanilla self-managed K8s; prereq K-COM) uses its own universe: **K-Frontier**. Where K-Town is the city you live in, K-Frontier is the homestead you build from raw land. Each K-VAN module = one build site on the homestead.

**District-to-module mapping**

| Module | Site | Topic |
|---|---|---|
| V1 | **Drafting Hut** | Production architecture design |
| V2 | **Land Clearing** | OS + node prep |
| V3 | **Frame Raising** | kubeadm bootstrap |
| V4 | **Wiring & Plumbing** | CNI install + networking |
| V5 | **Outbuildings** | Core add-on stack |
| V6 | **Rules Board** | Cluster configuration |
| V7 | **The Well** *(anchor)* | etcd production |
| V8 | **Renovation Site** | Upgrades + patching |
| V9 | **Watchtower** | Security hardening |
| V10 | **Drill Square** | Troubleshooting drills |
| V11 | **Complete Homestead** | Capstone |

The Well is the anchor (analogous to Mayor's Office in K-Town) — etcd is the foundation everything else depends on; if the well fails, the whole homestead fails.

**Cast (recurring)**

K-Frontier shares the K-Town cast where helpful (Katie may appear in V1's architecture-decision narration as the cluster manager you're emulating). New K-Frontier-specific characters are <em>roles, not named characters</em>:

- The **Settler** — the operator (you) building the homestead. Every K-VAN module is told from the Settler's POV.
- The **Foreman** — the experienced builder who knows the gotchas. Recurs across modules as a knowing voice.

These are job titles for whichever operator/SRE is being discussed, not new cast members. The 3-character cap from K-COM still applies.

**Implementation rules**

- Every K-VAN module opens with `🏕️ K-Frontier site: **[Site Name]**.` (the K-VAN equivalent of K-COM's `📍 Today's stop in K-Town: **[District Name]**.`).
- Every K-VAN module includes the K-Frontier map graphic with the current site highlighted.
- Map viewBox: 800×400 (smaller than K-Town's 800×420 — fewer sites).
- Map renders by `scripts/k_van_lesson_generator.py:_render_kfrontier_map()` from the same KFRONTIER_SITES list.
- Sub-labels under each site (\"design\", \"OS prep\", \"kubeadm\") give a one-word reminder.
- Strip dot count: 11 (one per module). Anchor at V1 (the Drafting Hut, where any homestead build starts).

### Unified analogical universe — Amazon EKS (K-Skyline)

K-EKS (Amazon EKS, AWS-managed K8s; prereq K-COM + AWS basics) uses its own universe: **K-Skyline**. Where K-Town is the city you live in and K-Frontier is the homestead you build by hand, K-Skyline is the AWS-managed *tower* you rent space in. AWS owns the elevators, HVAC, and security desk; you furnish the floors. Each K-EKS module = one floor (or facility) of the tower.

**Floor-to-module mapping**

| Module | Floor | Topic |
|---|---|---|
| E1 | **Lobby & Floor Plan** *(anchor)* | EKS architecture & shared responsibility |
| E2 | **Concierge Service** | EKS Auto Mode |
| E3 | **Communication Tower** | AWS networking (VPC CNI, ALB/NLB, Gateway API, VPC Lattice) |
| E4 | **Security Desk** | Identity (Access Entries, IRSA, Pod Identity) |
| E5 | **Storage Vault** | EKS storage (EBS, EFS, FSx, S3 Mountpoint) |
| E6 | **Power Floor** | Compute & autoscaling (Karpenter, spot, Graviton, GPU) |
| E7 | **Vault Mezzanine** | EKS security (KMS, GuardDuty, ECR signing, Bottlerocket) |
| E8 | **Observation Deck** | Observability (Container Insights, AMP, AMG, ADOT, X-Ray) |
| E9 | **Maintenance Wing** | Upgrades & operations |
| E10 | **Emergency Plaza** | Troubleshooting (AWS-specific) |
| E11 | **Tower Complete** | Capstone — multi-AZ Auto Mode tower |

The Lobby is the anchor (analogous to Mayor's Office in K-Town) — every visitor enters through the lobby; the floor plan on the wall is the shared-responsibility model that frames everything else.

**Cast (recurring)**

K-Skyline shares the K-COM cast where helpful (Katie may appear in E1 as the building manager who hands over the floor plan). New K-Skyline-specific roles (not named characters):

- The **Tenant** — the AWS-shop platform team (you) leasing floors. Every K-EKS module is told from the Tenant's POV.
- The **Building Manager** — AWS itself, who runs the elevators, HVAC, and lobby (control plane, encryption, region wiring) but never enters tenant floors.
- The **Concierge** — Auto Mode, who furnishes empty floors on request and quietly recycles them when unused.

These are job titles for whichever entity is being discussed, not new cast members. The 3-character cap from K-COM still applies.

**Implementation rules**

- Every K-EKS module opens with `🏙️ K-Skyline floor: **[Floor Name]**.` (the K-EKS equivalent of K-COM's `📍 Today's stop in K-Town: **[District Name]**.` and K-VAN's `🏕️ K-Frontier site:`).
- Every K-EKS module includes the K-Skyline map graphic with the current floor highlighted.
- Map viewBox: 800×400 (matches K-Frontier — fewer modules than K-COM).
- Map renders by `scripts/k_eks_lesson_generator.py:_render_kskyline_map()` from the same KSKYLINE_FLOORS list.
- Sub-labels under each floor (\"architecture\", \"Auto Mode\", \"VPC + LB + DNS\") give a one-word reminder of the AWS service surface.
- Strip dot count: 11 (one per module). Anchor at E1 (the Lobby, where every visitor enters).

### Unified analogical universe — Azure AKS (K-Campus)

K-AKS (Azure AKS, Microsoft-managed K8s; prereq K-COM + Azure basics) uses its own universe: **K-Campus**. Where K-Town is the city you live in, K-Frontier is the homestead you build by hand, and K-Skyline is the AWS-managed tower you rent space in, K-Campus is the **Azure-managed campus complex** — the Facilities Director (Azure) operates the lights, HVAC, security, and grounds; the Faculty (you) lease wings of buildings to host their departments. The Registrar's Office (Entra ID) is central — every visitor checks in there. Each K-AKS module = one wing (or facility) of the campus.

**Wing-to-module mapping**

| Module | Wing | Topic |
|---|---|---|
| A1 | **Welcome Center** *(anchor)* | AKS architecture & shared responsibility |
| A2 | **Registrar's Office** | Identity (Entra ID, Workload Identity, Azure RBAC) |
| A3 | **Pathways & Quad** | Networking (Azure CNI, AGC, NetworkPolicy) |
| A4 | **The Library** | Storage (Disks, Files, NetApp, Blob, Container Storage) |
| A5 | **The Auditorium** | Scaling (Cluster Autoscaler, NAP, KEDA, specialty pools) |
| A6 | **Campus Police** | Security (Defender, Policy, Image Cleaner, FIPS, Confidential) |
| A7 | **Bell Tower** | Observability (Container Insights, AMP, AMG, ADOT) |
| A8 | **Student Union** | Add-ons & platform (Dapr, Istio, Flux, Arc, Hybrid, Edge, Fleet) |
| A9 | **Maintenance Yard** | Upgrades & operations (LTS, channels, surge, blue-green) |
| A10 | **Health Clinic** | Troubleshooting (Azure-specific failure patterns) |
| A11 | **Commencement Hall** | Capstone — defendable reference campus |

The Welcome Center is the K-Campus anchor: every visitor arrives there; the wall map shows the whole campus floor plan (the shared-responsibility model); choices like AKS Standard vs AKS Automatic are explained at the door.

**Cast (recurring)**

K-Campus shares the K-COM cast where helpful. New K-Campus-specific roles (not named characters):

- The **Faculty** — you (department heads leasing wings of buildings). Every K-AKS module is told from the Faculty's POV.
- The **Facilities Director** — Azure platform itself, who runs the lights, HVAC, security cameras, and shuttle (control plane, encryption, region wiring) but never enters faculty offices.
- The **Registrar** — Entra ID, who validates everyone (humans and Pods) before they enter any building. Sits at the centre of the campus by design.

These are job titles for whichever entity is being discussed, not new cast members. The 3-character cap from K-COM still applies.

**Implementation rules**

- Every K-AKS module opens with `🏛️ K-Campus wing: **[Wing Name]**.` (the K-AKS equivalent of K-COM's `📍 Today's stop in K-Town:`, K-VAN's `🏕️ K-Frontier site:`, K-EKS's `🏙️ K-Skyline floor:`).
- Every K-AKS module includes the K-Campus map graphic with the current wing highlighted.
- Map viewBox: 800×400 (matches K-Frontier and K-Skyline — fewer modules than K-COM).
- Map renders by `scripts/k_aks_lesson_generator.py:_render_kcampus_map()` from the same KCAMPUS_WINGS list.
- Sub-labels under each wing (\"architecture\", \"Entra + Workload ID\", \"VNet + AGC + DNS\") give a one-word reminder of the Azure service surface.
- Strip dot count: 11 (one per module). Anchor at A1 (the Welcome Center, where every visitor enters).

### Unified analogical universe — Google GKE (K-Garden)

K-GKE (Google GKE, Google-managed K8s; prereq K-COM + GCP basics) uses its own universe: **K-Garden**. Where K-Town is the city you live in, K-Frontier is the homestead you build by hand, K-Skyline is the AWS-managed tower you rent space in, and K-Campus is the Azure-managed campus complex, K-Garden is the **Google-managed botanical garden / orchard** — the Head Gardener (Google) operates the climate, the irrigation, and the AI-assisted greenhouse; the Plot Holders (you) plant their crops in their reserved plots. Each K-GKE module = one plot or facility of the garden.

**Plot-to-module mapping**

| Module | Plot | Topic |
|---|---|---|
| G1 | **Visitors' Pavilion** *(anchor)* | GKE architecture & modes (Standard / Autopilot / Enterprise) |
| G2 | **The Almanac Hut** | Versioning + release channels (Rapid / Regular / Stable / Extended) |
| G3 | **Pathways & Trellises** | Networking (VPC-native, Dataplane V2, Gateway, NEG, MCI/MCG, CSM) |
| G4 | **Gatekeeper's Lodge** | Identity + security (WIF for GKE, BinAuth, Posture, CTD, Confidential, Sandbox) |
| G5 | **Reservoir & Compost** | Storage (PD, Hyperdisk + Storage Pools, Filestore, GCS FUSE, Parallelstore, Backup for GKE) |
| G6 | **Auto-Greenhouse** | Scaling + cost (CA, NAP, Autopilot billing, Compute Classes, Spot, GPU, TPU, BQ export) |
| G7 | **Watchtower** | Observability (Cloud Logging + Monitoring + GMP + Grafana + Trace + Profiler + SLO) |
| G8 | **Research Greenhouse** | Enterprise (Fleets) + AI/ML (JobSet, Kueue, GPU Operator, MIG, TPU multi-host, Ray, Inference Gateway, vLLM/NIM/Triton) |
| G9 | **Plant Doctor's Hut** | GCP-specific troubleshooting (gcpdiag, GKE Recommender, Logs Explorer, Cloud Status) |
| G10 | **Harvest Festival** | Capstone — defendable reference garden with AI inference |

The Visitors' Pavilion is the K-Garden anchor: every visitor arrives there; the wall map shows the whole garden\'s plot layout (the shared-responsibility model); the choice between Standard, Autopilot, and Enterprise is presented at the door.

**Cast (recurring)**

K-Garden shares the K-COM cast where helpful. New K-Garden-specific roles (not named characters):

- The **Plot Holder** — you (Faculty / department head equivalent), planting crops in your reserved beds.
- The **Head Gardener** — Google\'s GKE management plane: operates climate, irrigation, AI-assisted greenhouse; never enters tenant plots.
- The **Almanac Keeper** — release-channel stewardship (the Almanac Hut staff who track when each new variety becomes available + EOS dates).

These are job titles for whichever entity is being discussed, not new cast members. The 3-character cap from K-COM still applies.

**Implementation rules**

- Every K-GKE module opens with `🌿 K-Garden plot: **[Plot Name]**.` (the K-GKE equivalent of K-COM\'s `📍 Today\'s stop in K-Town:`, K-VAN\'s `🏕️ K-Frontier site:`, K-EKS\'s `🏙️ K-Skyline floor:`, K-AKS\'s `🏛️ K-Campus wing:`).
- Every K-GKE module includes the K-Garden map graphic with the current plot highlighted.
- Map viewBox: 800×400 (matches K-Frontier / K-Skyline / K-Campus — fewer modules than K-COM).
- Map renders by `scripts/k_gke_lesson_generator.py:_render_kgarden_map()` from the same KGARDEN_PLOTS list.
- Sub-labels under each plot (\"architecture\", \"release channels\", \"VPC + Gateway + LB\") give a one-word reminder of the GCP service surface.
- Strip dot count: **10** (one per module — K-GKE has 10 modules, not 11). Anchor at G1 (the Visitors\' Pavilion, where every visitor enters).

### Unified analogical universe — Red Hat OpenShift (K-Foundry)

K-OCP (Red Hat OpenShift Container Platform; prereq K-COM, ref OCP 4.21+) uses its own universe: **K-Foundry**. Where K-Town is the city, K-Frontier is the homestead, K-Skyline is the AWS-managed tower, K-Campus is the Azure-managed campus, and K-Garden is the Google-managed botanical garden, K-Foundry is the **Red Hat enterprise factory** — bays for forge, mold, safety, inventory, maintenance. The Foundry Master (you, the OCP platform admin) runs production with help from the Foreman (CVO) and the Safety Inspector (SCC + Compliance Operator). Each K-OCP module = one bay (or facility) of the foundry. **Pin prefix `ko-bay`** (K-OCP namespaced; the K-Foundry name is for human readability — not required to share initials).

**Bay-to-module mapping (13 bays — largest course)**

| Module | Bay | Topic |
|---|---|---|
| O1 | **Welcome Hall** *(anchor)* | OCP architecture (modes + RHCOS + MCO + CVO + OLM + 8 deployment shapes) |
| O2 | **Construction Site** | Installation models (IPI / UPI / Assisted / Agent + cluster shapes + disconnected) |
| O3 | **Pipework & Conveyors** | Networking (OVN-K, Routes / Ingress / Gateway, NetworkPolicy, MetalLB, Multus, NetObserv) |
| O4 | **Safety Office** | Security (OAuth, SCCs, Compliance Operator, RHACS, FIPS, Kata) |
| O5 | **Operator Hub** | Operators + OLM (CatalogSource → Subscription → InstallPlan → CSV → OperatorGroup) |
| O6 | **Mold Shop** | Workloads + DevEx (S2I + BuildConfig + ImageStream + Pipelines + GitOps + Serverless + Mesh + Dev Spaces) |
| O7 | **Inventory Warehouse** | Storage (ODF + Local/LVM + cloud CSI + RWX + OADP) |
| O8 | **Maintenance Bay** | Operations (ClusterVersion + EUS + MCO + MachineSets + etcd backup + must-gather + disconnected updates) |
| O9 | **Special Castings Wing** | Virtualization (KubeVirt) + AI (RHODS / OpenShift AI) + Edge (SNO + MicroShift + Local Zones) |
| O10 | **Multi-Foundry Network** | Multi-Cluster (RHACM — ManagedClusters, Placement, ApplicationSets, Policy, ObservabilityAddon, HCP, Submariner) |
| O11 | **Control Tower** | Observability (Cluster Monitoring + Loki + Tempo + NetObserv + COO) |
| O12 | **Diagnostic Lab** | Troubleshooting (must-gather + 8 OCP-specific failure pattern families + Insights + KCS) |
| O13 | **Grand Opening** | Capstone — defendable reference foundry with everything |

The Welcome Hall is the K-Foundry anchor: every visitor enters here; the wall map shows the whole foundry layout (the OCP architecture overview); the Foundry Master hands you a hard hat at the door.

**Cast (recurring)**

K-Foundry shares the K-COM cast where helpful. New K-Foundry-specific roles (not named characters):

- The **Foundry Master** — you (OCP platform admin), running production.
- The **Foreman** — Cluster Version Operator (CVO), orchestrating the ~30 ClusterOperators on the floor.
- The **Safety Inspector** — SCC enforcement + Compliance Operator + RHACS, checking every bay against safety regulations.

These are job titles for whichever entity is being discussed, not new cast members. The 3-character cap from K-COM still applies.

**Implementation rules**

- Every K-OCP module opens with `🏭 K-Foundry bay: **[Bay Name]**.` (the K-OCP equivalent of K-COM\'s `📍 Today\'s stop in K-Town:`, K-VAN\'s `🏕️ K-Frontier site:`, K-EKS\'s `🏙️ K-Skyline floor:`, K-AKS\'s `🏛️ K-Campus wing:`, K-GKE\'s `🌿 K-Garden plot:`).
- Every K-OCP module includes the K-Foundry map graphic with the current bay highlighted.
- Map viewBox: 800×420 (slightly taller than K-Frontier / K-Skyline / K-Campus / K-Garden — needs an extra row for 13 bays vs 10-11).
- Map renders by `scripts/k_ocp_lesson_generator.py:_render_kfoundry_map()` from the same KFOUNDRY_BAYS list.
- Sub-labels under each bay (\"architecture\", \"installation\", \"OVN-K + Routes\") give a one-word reminder of the OpenShift surface.
- Strip dot count: **13** (one per module — K-OCP has 13 modules, the largest course). Anchor at O1 (the Welcome Hall, where every visitor enters).
- Pin prefix `ko-bay` (K-OCP namespaced; not `kf-` to avoid collision with K-Frontier `kf-site`).

### Unified analogical universe — AWS ECS (K-Harbor) — *non-Kubernetes companion*

K-ECS (AWS ECS — Elastic Container Service; **not a Kubernetes course**) is shipped under the K-* family naming for organizational consistency, but its content uses ECS APIs (Tasks, Services, Task Definitions, Cluster, Capacity Providers, Service Connect) — not Kubernetes APIs. K-ECS is a *companion* to K-EKS, included because organizations frequently choose between or coexist with EKS. The K- prefix here is family branding, not a claim that ECS uses K8s.

K-ECS uses its own universe: **K-Harbor**. Where K-Town is the city you live in, K-Frontier is the homestead you build by hand, K-Skyline is the AWS-managed tower you rent space in, K-Campus is the Azure-managed campus, K-Garden is the Google-managed garden, and K-Foundry is the Red Hat enterprise factory, K-Harbor is the **AWS-managed working harbor** — a real shipping port where physical containers literally ship in and out. The Harbor Master (ECS control plane) decides which pier each ship docks at; the Tugboat Skipper (ECS agent) actually pulls each container into its slip; the Captain (you, the AWS-shop platform team) shows up with a cargo manifest (Task Definition) and asks for berth. Each K-ECS module = one pier (or facility) of the harbor.

**Pier-to-module mapping (10 piers — matches K-GKE shape: 9 content modules + capstone)**

| Module | Pier | Topic |
|---|---|---|
| C1 | **Harbor Office** *(anchor)* | ECS architecture (Cluster / Service / Task / Task Definition / launch types) |
| C2 | **Cargo Manifests** | Task definitions + container definitions + volumes |
| C3 | **Lookout & Comms Tower** | ECS networking (network modes, awsvpc, Service Connect, Service Discovery, ALB/NLB, VPC Lattice) |
| C4 | **Customs House** | IAM + security (task role vs execution role, Secrets Manager, KMS, ECR auth, VPC endpoints, compliance) |
| C5 | **Cargo Holds** | ECS storage (bind mounts, Docker volumes, EFS, FSx, ephemeral storage) |
| C6 | **Loading Crew Yard** | Deployment + scaling (rolling, blue/green, circuit breaker, Service Auto Scaling, capacity providers, placement) |
| C7 | **Lighthouse** | Observability (Container Insights, ECS Exec, FireLens, ADOT, X-Ray) |
| C8 | **Outport Station** | ECS Anywhere + hybrid |
| C9 | **Salvage Office** | ECS troubleshooting (PROVISIONING/PENDING stuck tasks, stopped reasons, deployment failures, Service Connect / ALB target health) |
| C10 | **Grand Voyage** | Capstone — multi-service Fargate app with Service Connect + ALB + EFS + Secrets Manager + CodeDeploy blue/green + Container Insights + autoscaling + failure-recovery runbook |

The Harbor Office is the K-Harbor anchor: every captain (operator) checks in there; the wall map shows the whole harbor's pier layout (cluster topology + launch type comparison + ECS-vs-EKS-vs-Fargate-vs-App Runner-vs-Lambda selection guide); the Harbor Master hands you a berth assignment at the door.

**Cast (recurring) — roles, not named characters**

K-Harbor is a *non-K8s* universe; the K-COM cast (Mayor Katie / Podrick / Thermostat) does **not** carry over because the underlying machinery is different (ECS scheduler, not kube-scheduler; ECS agent, not kubelet; Tasks, not Pods). Three K-Harbor roles, parallel in shape to K-Skyline / K-Campus / K-Garden / K-Foundry:

- The **Captain** — you (AWS-shop platform team), arriving at the harbor with a cargo manifest (Task Definition) for each cargo run. Every K-ECS module is told from the Captain's POV.
- The **Harbor Master** — ECS control plane: the service scheduler + deployment controller + task placement engine. Decides which pier each task docks at; never boards a ship.
- The **Tugboat Skipper** — the ECS agent (Fargate or EC2-launch-type): the small worker that actually pulls each container off the ship into its slip and reports state back to the Harbor Master.

These are job titles for whichever entity is being discussed, not new cast members. The 3-character cap from K-COM still applies; K-Harbor's Captain / Harbor Master / Tugboat Skipper are the K-ECS equivalents of K-Skyline's Tenant / Building Manager / Concierge.

**Implementation rules**

- Every K-ECS module opens with `⚓ K-Harbor pier: **[Pier Name]**.` (the K-ECS equivalent of K-COM's `📍 Today's stop in K-Town:`, K-VAN's `🏕️ K-Frontier site:`, K-EKS's `🏙️ K-Skyline floor:`, K-AKS's `🏛️ K-Campus wing:`, K-GKE's `🌿 K-Garden plot:`, K-OCP's `🏭 K-Foundry bay:`).
- Every K-ECS module includes the K-Harbor map graphic with the current pier highlighted.
- Map viewBox: 800×400 (matches K-Frontier / K-Skyline / K-Campus / K-Garden — 10 piers fit in two rows + capstone).
- Map renders by `scripts/k_ecs_lesson_generator.py` via the shared `scripts/multi_course_renderer.py` (post-refactor pattern: thin config caller, no per-course render fn).
- Sub-labels under each pier ("architecture", "task defs", "networking + Service Connect") give a one-word reminder of the ECS surface.
- Strip dot count: **10** (one per module — matches K-GKE shape). Anchor at C1 (the Harbor Office, where every captain enters).
- Pin prefix `kh-pier` (K-Harbor namespaced; not colliding with prior `kf-/ks-/kc-/kg-/ko-` prefixes).
- District-line emoji and strip emoji both render `⚓` (anchor); reused — no separate strip emoji as in K-VAN.
- **Vocabulary canonicalization** for ECS: the canonical terms are *Task* (not "pod"), *Task Definition* (not "manifest"), *Service* (the ECS Service object — long-running task scheduler), *Cluster* (an ECS cluster, not a K8s cluster), *Capacity Provider* (not "node group"), *Service Connect* (preferred over App Mesh patterns). Lessons use these throughout body text and quiz answers; K8s-equivalent terms (Pod, Deployment, Service-the-K8s-object) appear in parentheses on first mention only as a gloss for K-EKS-trained readers, never as the standalone term.

### K-ADV — Advanced specializations (post-K-COM, post-distribution-course)

K-ADV-* are *advanced specialization* courses for learners who already have K-COM (and at least one distribution course) under their belt. Five tracks, role-aligned: Security Architect, Networking Architect, Platform Engineering, AI / ML / GPUs, Disaster Recovery + BC. Each gets its own universe, on top of the same K-Town foundations — the universes overlay K8s primitives (Pods, Deployments, Services) with role-specific metaphor; they don't replace them. Pin prefixes follow the `kPREFIX-suffix` pattern so all five are unique against the existing 7 courses.

| Course | Letter | Universe | Emoji | Pin prefix | Modules |
|---|---|---|---|---|---|
| K-ADV-SEC | S | **K-Citadel** | 🏰 | `ksec-bastion` | 8 |
| K-ADV-NET | N | **K-Highway** | 🛣️ | `knet-junction` | 7 |
| K-ADV-PE | P | **K-Workshop** | 🛠️ | `kpe-bench` | 8 |
| K-ADV-AI | I | **K-Observatory** | 🔭 | `kai-array` | 8 |
| K-ADV-DR | D | **K-Lifeboat** | 🛟 | `kdr-cell` | 5 |

Total: 36 modules. Each module ≈ 5-10 hours of advanced content; courses are designed for 40-80 hours each.

#### Unified analogical universe — K-ADV-SEC (K-Citadel)

K-Citadel is a fortified citadel — walls, gates, sentries, an armored vault, an identity bureau, audit archives, a war-room. The K-COM cast (Mayor Katie / Podrick) appears as visitors who must pass through the citadel's controls; new K-Citadel roles (titles, not characters): **Captain of the Watch** (the security architect, you), **Sentry** (admission controllers + RBAC), **Vault Master** (Secrets / KMS / signing). Pin prefix `ksec-bastion`.

| Module | Bastion | Topic |
|---|---|---|
| S1 | **Threat Map Room** *(anchor)* | Threat modeling + zero-trust + multi-tenant isolation |
| S2 | Authorization Desk | RBAC design at scale |
| S3 | Checkpoint Gates | Admission policy architecture (Kyverno + Gatekeeper hybrid) |
| S4 | Mandatory-Helmet Zones | PSA Restricted migration playbook + runtime detection (Falco / Tetragon) |
| S5 | Seal Workshop | Image signing + SBOM + SLSA L3+ + in-toto + VEX in CI/CD |
| S6 | Armored Vault | Secrets at scale + mTLS + service-mesh security |
| S7 | Audit Archives + War Room | Audit log analytics + compliance evidence (PCI / HIPAA / FedRAMP / SOC2 / NIST 800-190) + break-glass + IR playbooks |
| S8 | The Defendable Citadel | Capstone — regulated platform for finance / healthcare |

#### Unified analogical universe — K-ADV-NET (K-Highway)

K-Highway is the interstate highway system — lanes, exits, intersections, bridges between cities, customs at borders, traffic helicopters. Tasks (Pods) are vehicles; Services are carpool stops; Gateways are main intersections; the CNI is the road builder. New roles: **Highway Engineer** (you), **Traffic Cop** (NetworkPolicy enforcement), **Customs Officer** (egress gateways). Pin prefix `knet-junction`.

| Module | Junction | Topic |
|---|---|---|
| N1 | **Highway HQ** *(anchor)* | CNI internals + eBPF + BGP at scale |
| N2 | Main Intersection | Service routing + Gateway API at fleet scale |
| N3 | Inter-City Bridges | Multi-cluster networking (Submariner / Skupper / Cilium ClusterMesh / Istio multi-cluster) |
| N4 | Carpool + Express Lanes | Service mesh selection + DNS scaling + IPv6 / dual-stack at scale |
| N5 | Customs Border + Tollbooth | NetworkPolicy at scale + egress gateways + private clusters + hybrid connectivity |
| N6 | Traffic Helicopter | Packet tracing + performance tuning |
| N7 | Multi-Region Highway Map | Capstone — multi-cluster network across EKS + AKS + GKE + on-prem + OpenShift / Tanzu |

#### Unified analogical universe — K-ADV-PE (K-Workshop)

K-Workshop is a master craftsperson's workshop — golden tools, master blueprints, apprentice intake, batch-crafting jigs, workshop accounting. New roles: **Master Craftsperson** (platform engineer, you), **Apprentice** (developer), **Foreman** (the operator running the platform). Pin prefix `kpe-bench`.

| Module | Bench | Topic |
|---|---|---|
| P1 | **Master Blueprint Library** *(anchor)* | IDP foundations + golden paths + self-service namespaces |
| P2 | Catalog Drawer System | Backstage (catalog, TechDocs, Scaffolder, plugins) |
| P3 | Composition Workbench | Crossplane v2 (Providers, Compositions, XRDs, Functions, ConfigurationPackages) |
| P4 | Batch-Crafting Jig | Argo CD ApplicationSets + OPA / Kyverno guardrails |
| P5 | Apprentice Intake | Tenant onboarding + resource templates + cost controls + service catalogs |
| P6 | Standard Tool Set | Workload abstractions: Score, KubeVela / OAM, Radius, Humanitec |
| P7 | Workshop Accounting | Platform SLOs + chargeback / showback (OpenCost / Kubecost) |
| P8 | The Equipped Workshop | Capstone — self-service IDP with namespace provisioning, RBAC, quotas, NetworkPolicy, GitOps, app templates, observability, cost labels, policy guardrails |

#### Unified analogical universe — K-ADV-AI (K-Observatory)

K-Observatory is a research observatory with telescope arrays, computation core, model-rendering halls, signal-line corridors. GPUs are *telescopes*; MIG slices are *eyepieces*; vLLM / Triton / NIM are *rendering halls*. New roles: **Astronomer** (ML / data scientist), **Optics Engineer** (you), **Patron** (the team paying for the observatory). Pin prefix `kai-array`.

| Module | Array | Topic |
|---|---|---|
| I1 | **Optics Bay** *(anchor)* | GPU nodes + NVIDIA device plugin / GPU Operator + MIG + DRA for GPUs |
| I2 | Observation Queue | Kueue + MultiKueue + Volcano gang scheduling |
| I3 | Research Hall | Ray on Kubernetes (KubeRay) + Kubeflow + KServe + JobSet |
| I4 | Model-Rendering Halls | LLM serving — vLLM, TGI, NVIDIA Triton, NIM Operator, llm-d |
| I5 | Triage Desk | AI / LLM Gateway patterns (Envoy AI Gateway, Kong AI Gateway) |
| I6 | High-Speed Signal Lines | RDMA, EFA, storage throughput, JuiceFS / Alluxio, OCI artifacts for models |
| I7 | Telescope-Sharing Committee | GPU sharing + multi-tenant GPU security + cost optimization |
| I8 | The Operating Observatory | Capstone — production AI inference platform with GPU scheduling + autoscaling + model rollout + observability + cost controls + tenant isolation |

#### Unified analogical universe — K-ADV-DR (K-Lifeboat)

K-Lifeboat is the emergency-drill universe — lifeboats, ship rebuild kits, mirror-ships in other harbors, total-loss restoration. New roles: **Drill Master** (DR architect, you), **Quartermaster** (backup operator), **Cargo Officer** (stateful-data steward). Pin prefix `kdr-cell`.

| Module | Cell | Topic |
|---|---|---|
| D1 | **Drill Square** *(anchor)* | etcd backup + Velero (CSI snapshots / Kopia / Restic) + Kasten K10 + CloudCasa |
| D2 | Ship Rebuild Yard | GitOps-driven recovery + cluster rebuild + application restore |
| D3 | Mirror-Ship Harbor | Cross-region DR + RPO / RTO + backup validation + restore testing |
| D4 | Cargo Recovery Office | Secret recovery + DNS failover + stateful workload DR + managed-service DR limitations |
| D5 | Total-Loss Drill | Capstone — destroy + rebuild a complete production cluster from Git + backups + registry + secrets + DNS + storage snapshots |

**K-ADV implementation rules**

- Every K-ADV module opens with `{universe-emoji} {Universe-Name} {district-kind}: **[District Name]**.` matching the established pattern.
- Every K-ADV module includes the universe map graphic with the current district highlighted.
- Map viewBox: 800×400 (matches K-Frontier / K-Skyline / K-Campus / K-Garden / K-Harbor — fewer modules than K-COM).
- Map renders by `scripts/k_adv_*_lesson_generator.py` via the shared `multi_course_renderer.py` (post-refactor pattern).
- Strip dot count = total module count (8 / 7 / 8 / 8 / 5 per course).
- Per CLAUDE.md "very advanced topics with super easy to understand illustrations and animations": each K-ADV lesson\'s hero illustration uses *simple shapes + clear labels* of the chosen metaphor (e.g., a citadel cross-section with labelled gates), not technical schematics. Animations show the metaphor in motion (e.g., a request entering the citadel passes a gate → a checkpoint → the vault) so a learner sees *the analogy enacted* before they see the technical mapping.
- Vocabulary canonicalization for each course honors the underlying K8s domain (Pods + Deployments + Services + RBAC + NetworkPolicy + admission webhooks + CRDs are the canonical terms; the universe metaphor is the wrapper, not a replacement).

## What never changes

- The packet/request motion track follows the visible cable/connection trajectory exactly. No exceptions.
- Color carries meaning, never decoration.
- Every lesson has all seven sections in fixed order.
- The analogy in section 3 is referenced consistently in ELI5 and ELI10.
- Every lesson ships with flashcards and a quiz.
- Every lesson ships with the layman-first scaffolding (Nightmare, stamp, district line, pause-and-checks, Translation Legend, Misconceptions, concept rail).
- Every Kubernetes lesson lives inside K-Town and uses its assigned district.
- K-ECS is the lone non-Kubernetes K-* course — it lives in K-Harbor and uses ECS vocabulary, not K8s vocabulary.
- K-ADV-* courses overlay role-specific metaphors (citadel / highway / workshop / observatory / lifeboat) on top of K8s primitives — the metaphor is the wrapper, the K8s vocabulary is canonical.
- The 800th lesson must look like the 1st.