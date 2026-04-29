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

### Hardware aesthetic

Servers render as recognizable rear panels in light silver chassis (#A8A8AC) with rack ears, mounting screws, two PCIe slots (one with a 2-port NIC card showing visible RJ45 jacks, one empty with vent slits), a center I/O cluster, and dual hot-swap PSUs with circular fan grilles. PSU fans rotate continuously via SMIL animation at 4–4.5s per rotation to communicate "powered on."

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

### Pause-and-question quizzes

Quiz questions are pause-the-animation prompts whenever possible: "I've stopped the packet here. What happens next, and why?" The learner predicts the next state from what they've just seen. This is the only assessment style that tests mental-model formation rather than memorization.

### Flashcards

One concept per card. Front: a question or a term. Back: 1-3 sentences. No flashcard contains everything — together, the deck covers the lesson's core terms.

### Pacing controls

Every animation provides pause/play and speed (0.3x to 2x). Pause is for live teaching — the trainer pauses on a critical moment and asks the class. Speed is for reviewing on second pass.

## What never changes

- The packet/request motion track follows the visible cable/connection trajectory exactly. No exceptions.
- Color carries meaning, never decoration.
- Every lesson has all seven sections in fixed order.
- The analogy in section 3 is referenced consistently in ELI5 and ELI10.
- Every lesson ships with flashcards and a quiz.
- The 800th lesson must look like the 1st.