# Decisions log

This file records meaningful choices made during the project, the context, and the reasoning. Append-only — never edit historical entries. If a decision is reversed, add a new entry referencing the old one.

Each entry follows this format:

## [Date] — [Short title]

**Context:** What situation prompted this decision.

**Decision:** What we chose to do.

**Reasoning:** Why this option won over alternatives.

**Alternatives considered:** What else was on the table and why it lost.

**Revisit when:** Conditions under which this should be reopened.

---

## 2026-04-29 — SVG + HTML widgets over a 3D animation framework

**Context:** Need to produce animated illustrations of packet flows, storage I/O, system architectures across multiple technical domains. Considered Three.js, Lottie, Rive, raw SVG.

**Decision:** Author lessons as raw SVG inside HTML widgets, with motion driven by `getPointAtLength` along an SVG `<path>` and continuous components driven by SMIL `<animateTransform>`.

**Reasoning:** SVG renders crisply at any size, embeds anywhere, requires no runtime, and is text-editable in Git so changes are diffable and AI-generatable. HTML widget wrapper gives us controls (pause, speed, mode toggles) without leaving the standard. The proof-of-concept VMware packet flow validated this works at the quality bar we want.

**Alternatives considered:** Three.js (too heavy, requires runtime, motion-graphics talent we do not have). Lottie (locks us into After Effects authoring). Rive (less Git-friendly, harder to AI-generate).

**Revisit when:** We need true 3D scenes (e.g., spatial navigation through a datacenter rack) or interactive simulations beyond what SVG paths can express.

---

## 2026-04-29 — Lesson, not scenario, as the atomic unit

**Context:** Earlier draft used "scenario" as the atomic unit. As the factory model emerged, "scenario" became one section of a larger lesson — specifically, the animated illustration plus its real-world examples. The lesson is what gets produced and shipped.

**Decision:** The atomic unit is a *lesson*, defined as a fixed seven-section package: concept, before/after, analogy, ELI5/ELI10, real-world scenarios, animated illustration, flashcards/quiz. "Scenario" now refers narrowly to the situations described in section 5 of a lesson.

**Reasoning:** Predictable structure makes mass production possible. A reviewer can compare two lessons in seconds because they have the same shape. AI output is more reliable when the target structure is fixed. Variable structure is the enemy of consistency at scale.

**Alternatives considered:** Variable lesson structure adapted per topic (more flexible, but unreviewable at scale and produces inconsistent learner experience).

**Revisit when:** A topic genuinely cannot fit the seven-section structure — e.g., a comparison-of-options topic with no flow to animate. We may need a second template type for those.

---

## 2026-04-29 — Fixed seven-section lesson structure

**Context:** Needed to define what "a lesson" actually contains. Considered a flexible structure where the AI picks sections based on the topic.

**Decision:** Every lesson contains exactly seven sections in fixed order: concept explanation, before/after, analogy, ELI5/ELI10, real-world scenarios, animated illustration, flashcards/quiz.

**Reasoning:** Predictability serves the learner (they know what to expect from any lesson) and serves production (output is reviewable against a fixed template). The cost of occasionally including a section that doesn't fit perfectly is far less than the cost of inconsistent learner experience and unreviewable output.

**Alternatives considered:** Flexible structure ("AI picks the right sections per topic"). Optional sections ("most lessons have these but some skip flashcards"). Both create review overhead and learner inconsistency.

**Revisit when:** User testing reveals that one section is consistently skipped or unhelpful for a specific kind of topic.

---

## 2026-04-29 — Founder-approved intake brief before production starts

**Context:** Topics arrive in the inbox at various granularities — sometimes a whole course, sometimes a single concept. Producing a lesson without a clear brief leads to scope drift and rework.

**Decision:** Every inbox submission generates a structured intake brief that the founder reviews and approves before any production work begins. The brief defines the granularity, the prerequisites, the moments of confusion to resolve, and (if the topic is large) the proposed sub-topic split.

**Reasoning:** A 5-minute review at the brief stage prevents 2 hours of rework after the lesson is produced. The founder's intent gets captured explicitly rather than reconstructed later from incomplete output.

**Alternatives considered:** Skip the brief and produce directly from the inbox file (faster per lesson but produces frequent rework). Have AI fully decide the granularity (loses the founder's curriculum intent).

**Revisit when:** Brief approval becomes a bottleneck because volume is high and briefs are repetitive enough to template.

---

## 2026-04-29 — Component library is canonical, not optional

**Context:** Each lesson needs primitives — server, switch, VM, cable, etc. Without rules, each lesson would re-draw its own versions.

**Decision:** The component library at `/library/primitives/{domain}/` is the canonical source. Lessons assemble from the library; they do not redraw. When a needed primitive does not exist, the factory drafts it, the founder approves, and it joins the library before being used in the lesson.

**Reasoning:** The 50th lesson must look like the 1st. The only way that happens at AI-driven volume is for the visual vocabulary to be a finite, stable set. The component library is also the most valuable asset the platform accumulates over time.

**Alternatives considered:** Allow per-lesson redrawing (faster short-term, kills consistency long-term).

**Revisit when:** Never. This is foundational.

---

## 2026-04-29 — Ship VMware first, do not launch six domains at once

**Context:** Vision spans six domains. Temptation to start all in parallel.

**Decision:** Ship a complete VMware fundamentals course (30-50 lessons) as the first product. Do not begin the second domain until phase 1 has real learners and real feedback.

**Reasoning:** The brand promise is built on quality of course one, not catalog breadth. The founder has VMware domain expertise and existing proof-of-concept content. Phase 1 reveals pricing, lesson length, narration style, assessment design, and production tempo — all unknowns that inform every subsequent course.

**Alternatives considered:** Launch a "fundamentals across all domains" sampler (impressive-looking but everything is shallow). Start with AWS for market size (no proof-of-concept, no domain expertise on hand).

**Revisit when:** VMware course has 100+ paying learners and stable production process.

---

## 2026-04-29 — Hypervisor and software-layer abstractions render as a slate band (#3F4A5E)

**Context:** Lesson 01 needs to render the hypervisor as a distinct visual element. The existing palette is allocated: networking teal/blue, storage coral/amber, encapsulation purple, failure red, healthy green, inactive gray. None apply to a software abstraction layer.

**Decision:** Hypervisor and similar software-layer abstractions render as a horizontal slate band with fill #3F4A5E and stroke #1F2433. Three thin horizontal hairlines (#536179 at 0.6 opacity) suggest "layer made of code." Label rendered in light text #E8E8E0, sans-serif 13px weight 500, letter-spacing 1.5px, centered horizontally.

**Reasoning:** Slate carries an "infrastructure / foundational" connotation that doesn't collide with any existing reserved color meaning. The horizontal-band shape reinforces the "between hardware and VMs" relationship.

**Alternatives considered:** Reuse #2A2A2E (dark gray) — rejected, conflicts with TOR switch chassis. Reuse teal — rejected, networking-coded. Use a unique shade outside existing families — selected.

**Revisit when:** A second software-layer abstraction (e.g., guest OS visual treatment, container runtime) needs a distinct color and would conflict.

---

## 2026-04-29 — Utilization meters use a single neutral fill regardless of percentage

**Context:** Lesson 01's pedagogy hinges on visualizing low (pre-virt) vs. high (post-virt) hardware utilization. Considered green/red value-encoding but it conflicts with reserved STYLE.md meanings.

**Decision:** Utilization meters use a single neutral fill #5A6B81 (a step lighter than hypervisor slate, signaling "related software-layer family") regardless of fill percentage. The pedagogical contrast is conveyed by fill *level* and the numeric label, not by color shifts.

**Reasoning:** Avoids palette collision with green=healthy, red=failure, amber=VLAN, teal=networking. More honest pedagogically — utilization isn't binary good-vs-bad; the visual contrast (mostly empty vs. mostly full) does the teaching.

**Alternatives considered:** Color-by-value (green high / red low or vice versa) — rejected, overloads existing reserved meanings. Two separate primitives for low and high utilization — rejected, breaks "primitive is canonical."

**Revisit when:** A future lesson needs to encode utilization-state risk (e.g., overcommit warning). At that point, consider an amber overlay on top of the existing fill rather than changing the base fill color.

---

## 2026-04-29 — Vertical stacking convention: VMs above, hypervisor in the middle, host below

**Context:** A choice about vertical layering in any diagram or animation that shows a virtualized host. Either order is technically defensible.

**Decision:** Render order from bottom to top is host → hypervisor band → VMs. The hypervisor band always sits *between* the host and the VMs.

**Reasoning:** Matches the apartment-building analogy frame (apartments above, building underneath, superintendent in the middle managing both). Also matches the dominant industry convention for virtualization stack diagrams. Pedagogical: "between" is the relationship the lesson teaches; the visual must reinforce it.

**Alternatives considered:** VMs at the bottom — rejected, contradicts industry convention and the analogy. Hypervisor as a side-bar — rejected, loses the "between" relationship.

**Revisit when:** Never. This is foundational.

---

## 2026-04-29 — Default consolidation visual shows 8 VMs on the post-virt host

**Context:** The "after" mode of the lesson 01 animation needs to visually demonstrate consolidation. The choice is how many VMs to render on the single host.

**Decision:** Show 8 VMs in two rows of four, atop one rack-server-rear (480 wide). Each VM tile is 120 × 56 by default, so 4 tiles align cleanly with the host's full width.

**Reasoning:** Eight is enough to feel meaningfully different from the four "before" servers (creates visual contrast and the consolidation message). Few enough to render legibly without crowding. Real consolidation can reach 50:1, but the visual goal is concept communication, not maximum.

**Alternatives considered:** 4 VMs (visually too similar to before count, contrast reads weakly). 16+ VMs (crowded; tile labels become unreadable at primitive default size).

**Revisit when:** A later lesson on consolidation ratios specifically.

---

## 2026-04-29 — Hardware sub-component labels exempt from the 11px text floor

**Context:** Lesson 01's static diagram scales primitives (Before grid at 0.55, After stack at 0.85). After scaling, sub-component labels inside `rack-server-rear` (PSU 1/2, I/O, "2-port NIC", "empty PCIe") render below the 11px STYLE.md floor. Bumping these labels in the primitive would inflate the rack-server-rear footprint and break compositions like the 4-across Before grid.

**Decision:** STYLE.md's 11px floor applies to primary content text — component labels, status text, body labels, utilization values. Hardware sub-component labels inside primitives are categorized as decorative texture and exempt from the floor.

**Reasoning:** A viewer recognizes a PSU by its circular fan grille and chassis position, not by reading "PSU 1." The labels exist to disambiguate at full primitive scale; in scaled compositions, primitive shape and proportion carry the recognition. Treating these labels as decorative texture matches how they actually function in the visual hierarchy.

**Alternatives considered:** Bump primitive text sizes — rejected, cascades through every VMware lesson and breaks the 4-across Before grid. Forbid scaling — rejected, compositions that contrast pre/post or many/one require it.

**Revisit when:** User testing reveals learners can't identify a hardware sub-component from shape alone. At that point, redesign the primitive's hardware aesthetic to convey identity through shape and proportion, and remove the sub-labels entirely.

---

## 2026-04-30 — Lessons render as a single-page interactive HTML preview

**Context:** PROJECT.md anticipates a render pipeline that turns a lesson folder into a static site. While that pipeline is built, lessons need to be presentable to learners and reviewers. A static document with embedded media isn't enough — first-time learners need to interact with the concept to understand it.

**Decision:** Each lesson ships as `preview-lesson-{nn}.html` at the project root, hand-authored for now using the conventions documented in STYLE.md "Lesson preview page" section. The page is a single scrollable column with a sticky top bar, a hero containing an interactive widget, prose sections each paired with an inline visualization, an inline knowledge check, ELI5/ELI10 tabs, accordion scenarios, embedded animation, flip flashcards, reveal-style quiz, and a recap card. Reference implementation: `preview-lesson-01.html`.

**Reasoning:** First-time learners report that "article with a video at the end" doesn't work — they need to *do* something with the concept, not just read about it. The single-page scrollable layout, with interactive widgets attached to the prose that motivates them, is the format that produces the "I get it now" reaction in user testing. Modeled on Bartosz Ciechanowski's blog, distill.pub, and Nicky Case's explorables.

**Alternatives considered:** Multi-page lesson with chapter navigation — rejected, breaks reading flow and adds chrome without value at this length. Video-first lesson — rejected, gates learning on video production capacity and doesn't let learners control pacing per concept. Plain-text lesson with "open animation in another tab" — rejected, was the original approach and produced the feedback that prompted this decision.

**Revisit when:** Volume reaches the point where hand-authoring is the bottleneck (~10-15 lessons), at which point the patterns become a templated render pipeline that ingests the canonical lesson folder and produces this same shape automatically.

---

## 2026-04-30 — Hero must contain an interactive widget that demonstrates the lesson's idea

**Context:** Even within the single-page preview, learners can scroll past walls of text without engaging. The traditional "concept paragraphs first, animation at the end" structure delays first-touch by minutes. The first ten seconds of any lesson decide whether the learner stays.

**Decision:** Every lesson's hero contains an interactive widget below the title and subtitle. The widget demonstrates the lesson's central idea in a small number of clicks (lesson 01: eight clicks to build a virtualized host). The lesson begins with experience, not text.

**Reasoning:** A learner who has just clicked +Add a VM eight times and seen the host fill from 0% to 72% has *already learned* the lesson's core takeaway. Everything that follows reinforces that initial demonstration with depth, analogy, scenarios, and practice. The text earns its place by adding to an existing intuition, not by trying to build that intuition from words alone.

**Alternatives considered:** Hero with a static graphic only — rejected, doesn't engage. Hero with an autoplaying animation only — rejected, doesn't give the learner agency. Hero with a video — rejected, gates pacing on someone else's tempo.

**Revisit when:** A lesson topic genuinely cannot be reduced to a one-widget interaction. At that point, design a constellation of small widgets that together represent the lesson's central idea — but never fall back to "text first."

---

## 2026-04-30 — Hover-to-define + click-to-pin tooltips for technical terms on first appearance

**Context:** Lesson 01 introduces multiple technical terms (virtual machine, hypervisor, host, capacity planning, isolation, utilization). A first-time learner trips on every undefined term. Forcing them to flip back to a glossary breaks reading flow.

**Decision:** Every technical term that a first-time learner could trip on gets a dotted-underline tooltip on its **first prominent appearance** in the lesson prose. Hover (desktop), click or tap (mobile and click-to-pin desktop) reveals a 1-2 sentence definition. Subsequent appearances are bare text. Tooltip writing includes the analogy mapping where relevant ("isolation — like the locks on each apartment door").

**Reasoning:** First-appearance tagging is the editorial convention used by NYT, FT, Stripe Press explainers — a learner sees the underline once, learns the meaning, reads bare text the second time without friction. Tagging every appearance creates visual noise and signals "this term is hard" instead of "you know this now."

**Alternatives considered:** Glossary appendix — rejected, requires the learner to leave the flow. Tag every appearance — rejected, visually noisy and patronizing on second read. No tooltips, define inline in prose only — rejected, makes the prose dense.

**Revisit when:** Never. This is foundational.

---

## 2026-04-30 — SMIL rotation groups must not carry the `transform-origin` attribute

**Context:** The PSU fan rotation in the rack-server-rear primitive uses SMIL `animateTransform` with `from="0 cx cy" to="360 cx cy"`. Originally the wrapping `<g>` also carried `transform-origin="cx cy"` as an SVG attribute. In some browser SMIL implementations the two specifications conflict and the rotation visibly drifts off-center.

**Decision:** Rotation groups driven by `animateTransform` must not declare `transform-origin` as an SVG attribute. The rotate origin is specified solely through `animateTransform`'s rotate parameters. This applies to every primitive containing a rotating element and every consumer that embeds such a primitive.

**Reasoning:** `animateTransform` replaces the element's `transform` attribute, but `transform-origin` (a presentation attribute mapped to the CSS property) survives and is applied additively in some renderers. The cross-browser-safe pattern is to use only the rotate origin baked into the animateTransform values.

**Alternatives considered:** Use CSS animations with `transform-origin: center` instead of SMIL — viable but requires a CSS class on every primitive instance and pulls another technology into the stack. Specify rotation origin only via `transform-origin` and a `from="0" to="360"` rotate — relies on consistent CSS-property handling across SMIL implementations, which is what bit us in the first place.

**Revisit when:** Never. This is foundational.

---

## 2026-05-01 — Open Kubernetes domain in parallel with VMware (qualifies 2026-04-29 "Ship VMware first")

**Context:** The 2026-04-29 decision said no second domain should begin until VMware had 100+ paying learners and a stable production process. The founder has now elected to scaffold a Kubernetes course (`courses/kubernetes/common-to-all-distributions/`) before those conditions are met.

**Decision:** Open the `kubernetes` domain alongside `vmware`. Initial course slug is `common-to-all-distributions` — content meant to apply across all Kubernetes distributions (vanilla, EKS, AKS, GKE, OpenShift, Rancher, etc.) rather than any single vendor flavor. Mirror the existing folder convention: `courses/kubernetes/{course-slug}/scenarios/{nn-slug}/` for lessons, `library/primitives/kubernetes/` for primitives. Both folders are seeded with `.gitkeep` placeholders since Git does not track empty directories.

**Reasoning:** Founder's explicit instruction overrides the earlier sequencing decision. The 2026-04-29 reasoning — that brand quality depends on depth in domain one before breadth — still stands as a guideline; this entry records the deliberate exception, not its repeal. Production capacity for Kubernetes lessons should not crowd out the VMware course; this is scaffolding for parallel future work, not a pivot away from VMware.

**Alternatives considered:** Defer until VMware course meets the 100-learner bar — rejected by founder. Use a different domain name (`k8s`) — rejected, full word matches the `vmware` / `aws` / `azure` pattern in PROJECT.md. Use a vendor-specific first course (e.g., `eks-fundamentals`) — rejected, founder specified distribution-agnostic content as the entry point.

**Revisit when:** VMware lesson production tempo demonstrably slows because Kubernetes work is competing for attention. At that point, pause Kubernetes production and reassert the original sequencing.

---

## 2026-05-01 — Per-domain preview filename pattern

**Context:** VMware previews live at the repo root as `preview-lesson-01.html` through `-15.html`. Kubernetes is now opening as a second domain in parallel. Without a naming rule, the next preview would either collide (two different domains sharing `preview-lesson-16.html`) or have to renumber.

**Decision:** Per-domain preview filenames. Pattern: `preview-{domain}-lesson-NN.html`. Kubernetes Lesson 01 ships as `preview-kubernetes-lesson-01.html`. VMware preserves its existing `preview-lesson-NN.html` series (no rename for the 15 already shipped).

**Reasoning:** Each domain has its own lesson sequence and progression. Sharing a flat numeric series would require a global ordering decision that doesn't reflect how learners traverse a course. Per-domain numbering keeps each track self-contained at the repo root and signals at a glance which course a preview belongs to. Renaming the existing VMware files would generate noise without any benefit — leave them alone, they're already linked from each other.

**Alternatives considered:** Continue the flat sequence as `preview-lesson-16.html` (loses domain context, blurs which course a learner is in). Move previews into per-domain subfolders (cleaner long-term but requires updating every internal href across 15 existing files for no immediate benefit). Number per domain but use a different separator (`preview_kubernetes_01.html`) — rejected for inconsistency with the existing hyphenated filenames.

**Revisit when:** Per-domain sequences exceed ~30 lessons or the repo-root file list becomes unmanageable. At that point, move to a `previews/{domain}/` subfolder structure with the same per-domain numbering inside.

---

## 2026-05-01 — Initial Kubernetes primitive set: pod-tile, node-tile, control-plane-band, controller-icon

**Context:** K-COM Lesson 01 needed visual primitives for pods, nodes, the control plane, and controllers. The library was empty. Per CLAUDE.md the founder normally approves each primitive individually, but this lesson was produced under the founder's standing "no per-stage approval" instruction.

**Decision:** Ship four foundational K8s primitives in this commit, sized and styled for cross-lesson reuse across the 17-module track:

- `pod-tile.svg` (110×78). Warm cream body + slate header, container squares inside in slate, status dot top-right. Encodes pod state (running / pending / failed / terminating / drift) via header fill + dot color + body border. Five state colors documented in STYLE.md "Kubernetes-specific conventions."
- `node-tile.svg` (240×180). Same body palette as pod-tile + role pill + dashed pod-docking area + status pill. Sized so 4 pod-tiles dock comfortably (2×2 in 220×144 area).
- `control-plane-band.svg` (600×56). Slate band reusing the hypervisor-band slate (#3F4A5E) — distinct from VMware's via four labelled component dots (api-server / etcd / scheduler / controller-manager) instead of the three hairlines used for hypervisors.
- `controller-icon.svg` (64×64). A spinning-arrows ring around a slate disc with a center letter slot for controller identity (D=Deployment, R=ReplicaSet, etc.). Used wherever a lesson narrates a control loop. Three SMIL-rotated arrows; rotation origin baked into animateTransform per the 2026-04-29 SMIL rule.

Other K8s components (etcd cylinder, scheduler icon, separate api-server icon) are deferred until later lessons need them — better to define each primitive in the lesson where it first earns its existence than to over-create now.

**Reasoning:** These four cover Module 1's pedagogy (the reconciliation loop, pet vs cattle, control vs data plane) and will be reused in Modules 3, 5, 6, 7, 11, 12, 13, 17. Same structural pattern as VMware primitives (XML header comment with description, slot anchors, states, and consumer override conventions; `<symbol>` + `<use>`) so future cross-domain reviewers see the same shape. Pod-state color encoding extends the existing palette without new families: green = healthy, gold = pending/in-flight, red = failure, gray = inactive — all already in STYLE.md. Coral (#B85829) for drift extends the storage I/O coral family with a related meaning (an in-flight thing the system is acting on).

**Alternatives considered:** Ship only pod-tile + node-tile (rejected — control-plane-band carries a lesson-01 illustration; needed now). Combine all four into one multi-symbol file (rejected — diverges from the per-file pattern of the VMware primitives, which would hurt long-term reviewability). Use Kubernetes' official 2D iconography (rejected per STYLE.md "Cloud service icons render as flat, recognizable shapes — never lift official icons"). Embed primitives inline in this lesson without library files (rejected — violates "the library is canonical").

**Revisit when:** A future Kubernetes lesson needs a primitive that doesn't exist yet (etcd, scheduler, individual api-server icon, CSI plugin, ingress). At that point, draft the new primitive in the same lesson commit and add it to the library — same rule.

---

## 2026-05-01 — Per-subtopic structure as the default for multi-subtopic lessons

**Context:** PROJECT.md defines a fixed 7-section lesson template. Across the VMware track, lessons that cover multiple subtopics evolved (per recorded user feedback in the auto-memory store) to nest a complete pedagogical block — concept + before/after + analogy + quick-check + ELI5/10 + real-world + flashcards + quiz — inside each subtopic, rather than once for the whole lesson. K-COM Lesson 01 followed the same pattern.

**Decision:** When a lesson covers multiple subtopics, each subtopic gets its own complete pedagogical block. The 7-section structure is preserved (it's now the structure of each subtopic, not just the lesson as a whole), and shared lesson-level artifacts (hero widget, animation, recap) wrap the subtopics. The per-subtopic block also includes a "Words you'll meet in this section" glossary card grid and 1-3 inline SVG illustrations.

**Reasoning:** Multi-subtopic lessons that share one analogy and one set of flashcards across very different concepts confuse first-time learners — the analogy stretches past where it teaches, and the flashcards underrepresent each subtopic. Per-subtopic blocks let each subtopic carry its own analogy and its own assessment, which holds the first-timer's hand more closely. The cost is more content per lesson, which is acceptable given the platform's value proposition.

**Alternatives considered:** One pedagogical block per lesson regardless of subtopic count (the original PROJECT.md interpretation; produces uneven coverage when subtopics diverge). One block per lesson plus inline mini-recaps per subtopic (lighter, but doesn't give each subtopic its own analogy / quick-check, which is what hooks first-timers). Per-subtopic blocks but shared analogy across all subtopics (rejected — different concepts often want different analogies).

**Revisit when:** User testing reveals that per-subtopic blocks fatigue learners on long lessons (10+ subtopics). At that point, consider a "compact" per-subtopic block that omits the ELI5/ELI10 pair and rolls up flashcards/quiz to lesson level for subtopics 6+.
---

## 2026-05-02 — Layman-first scaffolding components added across the lesson preview structure

**Context:** First-time-learner testing of the Kubernetes course revealed that even well-researched lessons fail when read by someone with no infrastructure background. Specific failures: pain (the "why should I care") arrives too late or implicitly; technical jargon and analogies are interleaved in the same sentence ("the captain (PID 1) hears the lighthouse (kubelet)"), triggering impostor syndrome; the seven existing sections give no mid-lesson comprehension checkpoints; predictable beginner misconceptions ("a container has its own OS") are never explicitly called out; the persistent left-rail showing "where am I in the journey" is missing.

**Decision:** Introduce a fixed set of layman-first scaffolding components that every lesson preview must include. These wrap and frame the seven content sections rather than replacing them:

- **Nightmare opener** — 2-3 sentence pain-first hook below the H1.
- **One-sentence stamp** — boxed irreducible takeaway, repeated at top and bottom.
- **District line** — one-line pin into the domain's unified analogical universe.
- **Pause-and-check (×2)** — 30-second multiple-choice comprehension pulses, mid-lesson at fixed positions.
- **Translation Legend** — story → tech mapping table inside Section 3 (replaces the bare "mapping" bullet list).
- **Common Misconceptions panel** — exactly three myth/truth pairs at the start of Section 7.
- **Analogy-stops-here callout** — inline ⚠️ note inside Section 3 where the analogy has a known cliff.
- **Skip-if-new tag** — muted pill marking advanced paragraphs as optional reading for beginners.
- **Persistent concept rail** — fixed left-rail showing the lesson's place in the course's journey.
- **CYOA quiz reveal** — one of the existing quiz questions per lesson is reframed as a story-style failure reveal.

The Common Misconceptions block is content; everything else is chrome. The Misconceptions block is folded into Section 7 (which is renamed in PROJECT.md from "Flashcards & Quiz" to "Common Misconceptions, Flashcards & Quiz") rather than added as an eighth section. This preserves the seven-section invariant established by the 2026-04-29 decision.

Component visual specs in STYLE.md "Layman-first scaffolding components." Quality bar for each component in QUALITY.md "What 'good' means, by scaffolding component." Both files are updated in the same commit as this decision.

**Reasoning:** The brand promise is that anyone willing to learn — including a layman — can understand the material. The seven content sections do not, on their own, deliver that promise. Each scaffolding component addresses a specific layman failure mode observed in testing. They are all hard gates because each one, missed, breaks the promise.

The decision to fold Misconceptions into Section 7 (rather than create Section 8) is deliberate: the seven-section structure is foundational per the original 2026-04-29 decision, and the misconceptions content belongs adjacent to flashcards and quiz (assessment cluster). Adding an eighth section would force a structural change with cascading review implications across all existing lessons.

**Alternatives considered:** Add Misconceptions as a new Section 8 — rejected, breaks the foundational seven-section invariant. Treat all scaffolding as fully optional — rejected, makes the brand promise probabilistic instead of guaranteed. Apply only to new lessons, not retroactively — rejected for the Kubernetes course since the existing 15 lessons have already been through layman testing and need the fixes.

**Revisit when:** User testing reveals that one of the scaffolding components is consistently skipped, ignored, or harmful for a specific kind of topic. At that point, demote the component to optional or remove it.

---

## 2026-05-02 — Unified analogical universe per domain — pattern established

**Context:** The Kubernetes course as written through Lesson 15 contains 13+ distinct analogies (property manager, apartments, thermostat, shipping containers, restaurants, industrial kitchen, library, trains, office buildings, warehouses, bakery, bank, ship, airport, permit office, shared apartment). Each lesson asks the reader to spin up a fresh mental model. First-time-learner testing surfaced this as a real cognitive tax — readers reported "fatigue from learning each new metaphor" and one direct collision (apartment = container in Lesson 02 vs apartment = Pod in Lesson 15).

**Decision:** Each domain may establish a single unified analogical universe within which every lesson's analogy lives as a *district* of that universe. The pattern, when applied to a domain:

- Name the universe (e.g., a city, a port, a garden).
- Establish a recurring cast of 2-4 named characters that appear across lessons.
- Map each lesson's analogy to a specific district within the universe, recorded in STYLE.md.
- Add a small map graphic — a single SVG of the universe — that appears once per lesson with the current district highlighted.
- Open every lesson with a one-line district pin.

This is a non-trivial choice for any domain — log it in DECISIONS.md before applying. The current Kubernetes universe (K-Town) is established in a separate decision (2026-05-02 — Kubernetes domain — K-Town as the unified universe). VMware does not yet have a designated universe; do not invent one without an approved DECISIONS entry.

**Reasoning:** Beginners build mental maps by accumulating familiarity with one consistent world. Each fresh analogy demands fresh mental setup before any technical learning can land. A unified universe converts that one-time tax (learning the city) into compounding return (every subsequent lesson reuses the city's vocabulary, characters, and geography). The cost is a one-time domain-wide commitment to the universe's vocabulary; the benefit is every subsequent lesson.

The pattern is per-domain rather than global because different domains map naturally to different worlds (Kubernetes maps to a city; storage might map to a port; ML pipelines might map to a factory). Forcing one universe across all domains would dilute each.

**Alternatives considered:** Continue with per-lesson analogies (the existing approach) — rejected, fatigues beginners and produces collisions. One global universe across all domains — rejected, no single metaphor stretches that far without becoming abstract. Apply the unified universe only at course level rather than domain level — rejected, multiple courses within a domain (e.g., Kubernetes fundamentals, Kubernetes networking, Kubernetes operators) benefit from sharing the same world.

**Revisit when:** A second domain establishes its own universe and we have evidence of how the pattern generalizes. At that point, formalize cross-domain conventions (e.g., "every domain's universe has a recurring 'system' character analogous to Mayor Katie").

---

## 2026-05-02 — Kubernetes domain — K-Town as the unified universe

**Context:** Per the same-day decision establishing the unified-analogical-universe pattern, the Kubernetes domain needs a specific universe instance. The existing analogies across the 15 written lessons cluster naturally around urban infrastructure (apartments, libraries, banks, airports, harbors, permit offices, etc.).

**Decision:** Kubernetes lessons are set in **K-Town**, a stylised city. Each existing lesson analogy is mapped to a named district. Three recurring characters anchor the cast:

- **Mayor Katie** — personifies Kubernetes as the property manager / city manager. Appears in Lesson 01.
- **Podrick** — the unit/box/parcel that gets placed and moved. Personifies a Pod / workload.
- **The Thermostat** — the wise old gadget explaining control loops. Appears in Lesson 03 and reappears whenever a new reconciliation loop is introduced.

Two optional supporting characters appear sparingly: Captain Tini (Lesson 12, harbour district) and Inspector Pause (Lesson 15, co-living quarter). Additional characters require their own DECISIONS entry.

The 15 districts are mapped lesson-by-lesson in STYLE.md "Unified analogical universe — Kubernetes (K-Town)." Lesson 7.5 (a new Level 0 primer — see separate decision) gets its own district: Foundation Tour. Apartment metaphor collision is resolved by giving Lesson 02 the Residential District (apartment = container) and Lesson 15 the Co-Living Quarter (co-living unit = Pod). Apartment is no longer used to mean Pod anywhere.

**Reasoning:** A city naturally houses every existing analogy in the course (residential, commercial, civic, transportation, industrial). The cast members are minimal (three regulars) but each carries strong load — Katie embodies Kubernetes as an actor, Podrick gives workloads a face, the Thermostat is the recurring oracle for the reconciliation loop. Co-living unit resolves the apartment collision without inventing a new metaphor for Pods.

**Alternatives considered:** A "Megaport" framing as the universe — rejected, doesn't naturally house the thermostat (the most important analogy in the course, Lesson 03), nor the bakery (Lesson 10), nor the permit office (Lesson 14). A more abstract "Cluster Cosmos" with planets per concept — rejected, abstract metaphors don't anchor in everyday experience. No universe at all (keep per-lesson analogies) — rejected per the unified-universe decision above.

**Revisit when:** The course expands beyond ~30 lessons and the city map becomes too dense to read. At that point, consider K-Town districts as nested sub-cities (the K-Town Industrial Quarter has its own internal districts).

---

## 2026-05-02 — Vocabulary canonicalization — Kubernetes canon list

**Context:** Across the 15 Kubernetes lessons as written, multiple synonyms drift for the same concept, sometimes within a single lesson. Examples: "desired state" / "what you want" / "the spec" / "your declared intent" all referring to the same thing; "controller" / "the loop" / "the reconciler" / "small program watching forever" likewise. Beginners learning the field through these lessons get repeatedly re-introduced to the same idea under different labels.

**Decision:** Each domain maintains a canonical-term list. Lessons use canonical terms throughout body text and quiz answers; "acceptable on first mention" terms may appear once in parentheses as a gloss on the canonical term, never as the standalone term in subsequent uses.

The Kubernetes canon list (full table in STYLE.md "Vocabulary canonicalization"):

- desired state (canonical) — "what you want" (gloss only)
- actual state (canonical) — "what's running" (gloss only)
- controller (canonical) — "the small program watching forever" (gloss only)
- reconciliation loop (canonical) — "the loop" (only after first mention in a lesson)
- Pod (capitalised, canonical) — never lowercase pod
- the kubelet (canonical) — "the node agent" (gloss only)
- the API server (canonical) — never "the K8s API"

VMware, AWS, and other domain canon lists will be added as those courses develop a long-tail of synonym drift.

**Reasoning:** Synonyms make a lesson feel writerly to the author and confusing to the beginner. The canonical-vs-gloss distinction preserves rhythmic prose (the gloss adds variety once) without paying the comprehension cost (the canonical term carries the meaning everywhere else). The cost is editorial discipline; the benefit is every beginner builds the same mental anchor for the same concept.

**Alternatives considered:** Allow synonyms freely (the existing approach) — rejected, surfaces the drift problem we're trying to solve. Forbid all synonyms entirely (no glosses) — rejected, makes prose mechanical and removes the first-mention scaffolding that helps beginners. Maintain a global canon across domains — rejected, the same word can mean different things across domains (e.g., "controller" in Kubernetes vs ML-Ops).

**Revisit when:** A new term enters circulation that has multiple existing variants in the wild and we need to pick one for the canon. At that point, append to the relevant domain table rather than re-deciding the policy.

---

## 2026-05-02 — Prerequisite primers — the Lesson N.5 pattern

**Context:** Module 2 of the Kubernetes course (Lessons 08-12) silently assumes the reader knows what a process is, what an operating system is, what a kernel is, and what root means. Most laymen don't. Layman-test feedback on Lesson 08 was uniformly negative — the lesson is technically correct and beautifully written but lands hard for anyone without prior Linux exposure.

**Decision:** When a content module assumes prior knowledge a layman won't have, a short interstitial primer at `N.5` is the established pattern. The first instance is **Lesson 7.5 — How a Linux Computer Works in 5 Minutes**, sitting between Lesson 07 (end of Module 1) and Lesson 08 (start of Module 2).

Primer specifications:

- 5 short sections, ~5 minutes total reading time.
- Plain prose only. No quiz, no flashcards, no animation.
- One simple diagram acceptable but not required.
- Tone matches Lesson 01 — friendly, no jargon beyond what the primer itself defines.
- Footer link: "Ready for Module N? → Lesson NN."
- Cross-link from the dependent lesson at the very top: "*New to [topic]? Take a 5-minute detour through Lesson N.5 — [Title].*"

Primers are first-class lesson files (`preview-{domain}-lesson-N-5.html`) and inherit the same scaffolding as full lessons (Nightmare opener may be omitted if the primer's purpose is purely scaffolding; district line and concept rail still apply).

**Reasoning:** A primer is cheaper than rewriting the dependent lesson to define every prerequisite term inline (which would balloon Lesson 08 by 60%). It's also more honest — laymen who already know the prerequisites can skip; those who don't get explicit help. Numbering as N.5 rather than re-numbering the entire course preserves existing cross-references.

**Alternatives considered:** Define every prerequisite term inline in the dependent lesson — rejected, dilutes the lesson's actual content and signals "this lesson is hard" instead of "you can do this with a 5-minute warm-up." Maintain a separate glossary appendix — rejected, requires the learner to leave the flow. Renumber lessons (so "Lesson 08" becomes "Lesson 09" and the primer is "Lesson 08") — rejected, breaks every existing cross-reference and makes future renumbering tempting (which it shouldn't be).

**Revisit when:** A primer becomes long enough to warrant its own first-time-learner test (>1500 words). At that point, promote it to a full lesson and re-number, accepting the cross-reference cost.
