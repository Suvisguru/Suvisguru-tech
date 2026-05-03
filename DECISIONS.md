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

---

## 2026-05-02 — K-Town revision Phase 1 — accuracy fixes and primer-filename convention

**Context:** Phase 1 of the Kubernetes course revision (`tasks/k8s-course-revision-plan.md`). Four small accuracy fixes plus one governing-file addition. Bundled here as a single phase entry per the founder-approved "one DECISIONS entry per phase commit" rule for this revision.

**Decision:** Four content fixes plus one STYLE.md addition:

1. **Seccomp default-profile syscall count canonicalised to "roughly 40–65 dangerous syscalls (varies by runtime version) out of ~300 total."** Lesson 08 previously said "~70" in six places (concept body, primitive tile description, real-world scenario, flashcard, glossary, animation step-4 status string). Lesson 11 said "~50" in three places (securityContext prevents-table, flashcard, glossary). Both numbers were brittle — containerd's `RuntimeDefault` count varies by architecture and version (40–65 is the realistic spread). The new phrasing is accurate without pretending to a precision the runtime doesn't actually offer.

2. **Lesson 07 "GA only in prod" scenario rewritten to use Gateway API instead of InPlacePodVerticalScaling.** The original example claimed InPlacePodVerticalScaling changed shape *during beta* between K8s 1.27 and 1.28 — factually wrong; that feature was **alpha** in 1.27 and 1.28 and didn't reach beta until 1.33. Replaced with Gateway API's beta-period field renames (v1beta1 → v1) before October 2023 GA — same pedagogical point, factually correct, less in-the-weeds.

3. **Lesson 13 Managed CP scenario gets a one-line pricing footnote.** The "GKE control plane is ~$73/cluster/mo" claim is correct only for GKE Standard. AKS is free; EKS is $73/mo; GKE Autopilot bills per-pod. Added a small italic muted footnote inside the same `.scenario` panel making the variation explicit and noting the conclusion (managed beats self-managed at this team size) is unchanged.

4. **STYLE.md "Preview filename per domain" gets a primer-filename convention.** The 2026-05-02 prerequisite-primer DECISIONS entry left the filename casing implicit. Established explicitly: Lesson-N.5 primers substitute a hyphen for the dot — `preview-{domain}-lesson-N-5.html` (e.g. `preview-kubernetes-lesson-7-5.html`). No leading zero on the integer part. Filesystem-friendly and unambiguous.

**Reasoning:** All four are low-risk, high-confidence corrections that make the course more accurate without touching the visual language or pedagogy. Bundling them as Phase 1 builds momentum before the larger Phase 2 component-template work and gives the founder a small reviewable diff to validate the revision plan's discipline before bigger changes land.

**Alternatives considered:** Apply each fix as its own commit — rejected, four trivial commits add noise without adding review value when they share a phase. Defer the seccomp fix to Phase 5 lesson-by-lesson — rejected, the contradiction between L08 and L11 is what makes it Phase-1 material; touching only one lesson would leave the contradiction. Drop "varies by runtime version" from the canonical phrasing for brevity — rejected, the variation is the honest thing and is exactly why neither "~70" nor "~50" was right.

**Revisit when:** A future lesson cites a more specific seccomp count from a specific runtime version (legitimate if the lesson is about that runtime). At that point, that lesson can override the canonical phrasing inline rather than re-deciding the policy.

---

## 2026-05-02 — K-Town revision Phase 2 — k-town-map primitive and layman-first component family

**Context:** Phase 2 of the Kubernetes course revision (`tasks/k8s-course-revision-plan.md`). Builds the K-Town map primitive plus the ten reusable scaffolding components STYLE.md "Layman-first scaffolding components" calls for, and applies the full set to `preview-kubernetes-lesson-01.html` so it becomes the live K-Town reference STYLE.md already names. Bundled here as a single phase entry per the founder-approved per-phase-commit rule.

**Decision:** Two related sub-decisions held in one entry:

**Sub-decision A — `library/primitives/kubernetes/k-town-map.svg`.** A single canonical SVG with 16 named pins (15 lessons plus the Lesson 7.5 primer) on a stylised city map, viewBox 800×420. Pins follow consistent structure (`<g class="pin" id="kt-pinNN">` containing `pin-halo`, `pin-circle`, `pin-num`, `pin-label`). The Mayor's Office (L01) anchor pin uses radius 14 (vs 10 for normal pins), an extra `pin-anchor` class, and an italic "city anchor" subtitle so it stays visually present across all lessons in slate (`--accent`); the L7.5 primer pin uses an extra `pin-primer` class with a dashed circle stroke and an italic "primer" subtitle. Each lesson inlines the SVG body and adds the `active` class to that lesson's pin to highlight it in warm coral (`--warm`). Inline `fill="…"` attributes on the circles are kept as readable defaults (so the file renders sensibly when opened directly); host-page CSS rules using design tokens override at runtime via standard CSS specificity. Geographic logic: civic core in center, transport ring on perimeter (rail north, airport northeast, harbour/port south on a bay gradient), residential cluster (L02 + L15) west, commercial cluster (L06/L08/L09/L11) east, food/industrial corridor (L05/L10/L04) running through the south-center, primer pin (L7.5) parked bottom-left as a "you start here" arrival gate.

**Sub-decision A.1 (mobile fallback).** Below 720px viewport width the full SVG map collapses to a horizontal "you-are-here" dot strip — 16 small dots in a row with the active dot in warm coral and a one-line label ("📍 **District** · lesson N of 16") plus a `visually-hidden` accessibility line ("Lesson N of 16, District."). Justified because at 360px the full map's pin labels become ~4–5px and unreadable, and the strip preserves the only mobile-relevant signal (position-in-journey) without competing with the existing district line above. The `visually-hidden` utility uses the standard clip-rect-zero pattern. The strip itself is `aria-hidden="true"` to avoid 16 unhelpful screen-reader announcements; the `visually-hidden` span is the screen-reader-friendly position phrase.

**Sub-decision B — Layman-first component family.** Ten reusable scaffolding components plus the `.s code` and `.visually-hidden` utilities, all CSS-only and inheriting existing tokens (`--accent`, `--warm`, `--good`, `--ink-faint`, `--gold`, `--bg-soft`, `--r-card`, `--r-soft`, `--r-pill`, `--ease`). No new tokens introduced. The component family lives inline in L01's `<style>` block fenced by the comment `/* ============ LAYMAN-FIRST SCAFFOLDING (K-Town revision Phase 2) ============ */`; Phase 5 lessons copy the block verbatim into their own `<style>`. A working note at `notes/k8s-component-templates.md` documents the slot-by-slot HTML pattern for propagation but is **not** the source of truth — L01 is.

The components, in slot order:

1. **Concept rail** (`<aside class="concept-rail">`). Fixed-position 170px-wide left rail, visible at viewport ≥1240px (hidden otherwise — the K-Town dot strip covers narrower screens). 18 vertical items (15 lessons + L7.5 primer + L16/L17 placeholders for the planned course continuation). States: `current` (▶ slate + "← you are here"), `done` (✓ green), default (○ ink-faint). Hard-coded per lesson, no state persistence.
2. **District line** (`<p class="district-line">`). Single line above the K-Town map. `📍 Today's stop in K-Town: **{District Name}**.`
3. **K-Town map** (Sub-decision A above).
4. **Nightmare opener** (`<div class="nightmare">`). Warm-soft panel with `🚨 The 3 AM Nightmare` tag in warm-deep, 2–3 sentence pain-first scenario, sits between hero and Section 1.
5. **One-sentence stamp** (`<div class="stamp">`). Slate-bordered centered box with `🎯 If you remember nothing else: …`. Identical content at top (immediately under Nightmare) and bottom (immediately above the recap card).
6. **Pause-and-check** (`<div class="pause-check">`). Gold-soft dashed-border box with three button options and inline reveal feedback. Two per lesson — between §1↔§2 and §4↔§5.
7. **Translation Legend** (`<div class="translation-legend">`). Two-column table inside §3 replacing the existing "The mapping:" `<ul>`. Headers: "In the story…" / "…in Kubernetes". Stacks to single column below 600px width.
8. **Analogy-stops-here** (`<p class="analogy-stops">`). Gold-soft inline callout with ⚠️ prefix, italic, narrower than full panels. Inside §3 after the Translation Legend. Used selectively — not every lesson has a known cliff.
9. **Misconceptions panel** (`<div class="misconceptions">`). Three myth/truth `.misc-card` blocks at the start of §7 (per STYLE.md / DECISIONS 2026-05-02 — folded into §7, not a new §8). Myth row uses `--warm-soft`; truth row uses `--good-soft`.
10. **CYOA quiz reveal** (`<div class="quiz-card cyoa-quiz">`). Gold-tinted variant of the existing `.quiz-card`. Story-framed prompt with `🎬 Choose Your Own Adventure` tag, replaces one of the three existing scenario quiz items per lesson.
11. **Skip-if-new pill** (`<span class="skip-pill">`). Defined in CSS for future Module-2/3 lessons that need it; not used in L01.

A small JS update in the existing `<script>` block: the quiz-reveal handler is rewritten to handle both "Show answer" and the new CYOA "Show what happened" labels via a `/^Show/ → Hide` prefix substitution, and a pause-and-check handler is added.

**Reasoning:** STYLE.md "Layman-first scaffolding components" specifies the visual family; DECISIONS 2026-05-02 mandates them on every lesson. Phase 2 turns those specs into one shared CSS block plus matching HTML markup, with L01 as the live reference so future agents pattern-match from a real implementation rather than a description. Reusing existing tokens (no new colours, no new radii) means the components can't visually drift from the rest of the system. The `.s code` rule and `.visually-hidden` utility are bundled because they are foundational utilities the component family depends on (inline code in pause-check answers; screen-reader text on the dot-strip label) — adding them as one-off later commits would split the bundled-decision rule artificially.

The K-Town map's mobile fallback is a sub-decision of Sub-decision A rather than a separate entry because the full-map and dot-strip are two faces of the same primitive: the map is the desktop affordance, the strip is the mobile affordance, both express the same "where am I in the universe" data. They share class names (`active`, `pin-anchor`-equivalent `ktown-strip-anchor`) and the same activation pattern (one element gets the `active` class per lesson).

L01 is updated in this commit so it stops being aspirational reference and starts being load-bearing reference. STYLE.md "Kubernetes-specific conventions. Established in K-COM Lesson 01…" now matches reality.

**Alternatives considered:** Build templates in a separate `notes/k8s-component-templates.md` and use it as the source of truth — rejected, the working note is fine for documentation but lessons need a live HTML reference to copy from; living-in-the-source is the existing pattern (the VMware lessons have no separate template file, they inherit from `preview-lesson-01.html`). Use SVG `<use href="library/primitives/kubernetes/k-town-map.svg#k-town-map">` to reference the map externally rather than inlining — rejected, external `<use>` references break CSS styling of inner elements (`.pin-circle`, `.pin-label`) across the shadow boundary in some browsers, and the existing lesson primitives (rack-server-rear, hero illustrations) are inlined for the same reason. Make the map a desktop-only artefact and leave mobile blank — rejected, the journey-progression cue is exactly what mobile readers need most. Add new colour tokens for the mobile dot-strip (`--strip-active`, `--strip-anchor`) — rejected, existing `--warm` / `--accent` / `--ink-faint` carry the meanings already; inventing parallel tokens would fragment the palette. Place the Misconceptions panel as a new §8 (an option the K-Town plan §5.4 left open) — rejected, DECISIONS 2026-05-02 already foreclosed this; the seven-section invariant is foundational.

**Revisit when:** A second domain (VMware, AWS) reaches scaffolding parity and we discover that a component generalises differently across domains. At that point, abstract the divergent piece into a per-domain override rather than a global rewrite. Or: a Phase-5 lesson uncovers a layout case the templates don't handle cleanly (e.g. a multi-subtopic lesson where the mid-lesson pause-checks need to land at non-§1/§4 boundaries). At that point, extend the component spec with a documented variant rather than letting the variant drift inline.

---

## 2026-05-02 — K-Town revision Phase 5 batch 1 — L02–L04 scaffolding + first canon sweep

**Context:** Phase 5 of the Kubernetes course revision (`tasks/k8s-course-revision-plan.md`) propagates the layman-first scaffolding component family from L01 (the live reference built in Phase 2) to the remaining lessons. This entry covers batch 1: L02 Virtualization vs Containerization, L03 Cloud-Native Principles, L04 12-Factor + Microservices vs Monoliths. Phases 3 (vocab canonicalization) and 4 (per-lesson district lines + map embeds) fold into Phase 5 per the founder-approved plan-collapse — so each lesson gets its scaffolding, district line, K-Town map, and canon sweep applied in one pass instead of three. Also bundles a small STYLE.md correction surfaced during Phase 2 review and a fix to the L01 reference.

**Decision:** Five sub-decisions held in one entry:

**Sub-decision A — Phase 5 propagation pattern.** Each lesson in this batch (L02, L03, L04) receives, in lesson-source order: the scaffolding CSS block (copied verbatim from L01); the concept rail (with that lesson marked `current`, all earlier marked `done`); the district line and the K-Town map (with `active` on that lesson's pin, anchor pin staying slate); the Nightmare opener and one-sentence stamp at the top; pause-and-check #1 between §1 and §2; the Translation Legend table replacing the existing "The mapping:" `<ul>` in §3, with an analogy-stops-here callout below; pause-and-check #2 between §4 and §5; Section 7 eyebrow + intro updated and the Common Misconceptions panel inserted before the flashcard grid; the third existing scenario quiz card replaced with a CYOA item per the K-Town plan §8.NN; the bottom stamp above the recap card; and the smarter quiz-reveal handler plus the new pause-and-check handler in the script block. The transformation is implemented as `scripts/apply_phase5_batch1.py` so the same per-lesson recipe can be re-applied verbatim to subsequent batches with new per-lesson data, rather than hand-edited each time. The script is idempotent — running it twice on the same lesson aborts with an anchor-not-found error because the second pass can no longer find the original anchor strings.

**Sub-decision B — L01 dot-strip bug fix.** Phase 2's L01 reference shipped with the dot-strip's `ktown-strip-anchor active` class on position 9 (an arithmetic error during initial layout), but the strip is supposed to read left-to-right in curriculum order — Mayor's Office (L01) is position 1. Fixed in this commit so that L01 anchors at position 1 with `active`, and L02–L04 inherit the corrected pattern. Future batches use the same convention.

**Sub-decision C — Vocabulary canonicalization sweep, batch 1 results.** Per STYLE.md "Vocabulary canonicalization", the canon list flags "the spec", "your declared intent", "what you said", "current state", "live state", "reality", "the loop" (standalone), "the reconcile cycle", "the watch loop", lowercase "pod"/"pods", "the agent", and "the K8s API" as terms to avoid. Sweep results across this batch:

- **L02:** zero hits. The lesson is about VMs vs containers and predates the per-lesson reconciliation-loop terminology that produces most canon drift. No edits required.
- **L03:** seven hits, all in the cloud-native-principles lesson where desired/actual-state language is most active. Fixed: §1 concept paragraph rewritten to introduce `desired state (what you want)` and `actual state (what's running)` as canonical first-mention glosses; the `the spec vs reality` shorthand in the seven-principles list rewritten to `what you want vs what's actually running`; §1.5 principle tag changed from `the **spec** vs **reality**` to `**desired** vs **actual**`; the §2 after-state paragraph's `"matches the spec"` becomes `"matches the desired state"`; the §3 illu-caption drops the now-redundant `(what you said)` and `(what's running)` parentheticals (glosses are first-mention only per canon); the desired/actual flashcard back rewrites `what you said you wanted` and `live cluster` to canonical phrasings; the glossary def for "Desired state" rewrites `What you said you wanted` to `What you want`; the animation status string `'You changed the spec to 5'` becomes `'You changed the desired state to 5'`. Plus 22 lowercase `pod`/`pods` instances capitalised to `Pod`/`Pods` via a global `pod` → `Pod` substitution (applied via Edit's `replace_all`), with a single follow-up cleanup converting `"horizontal Pod autoscaler"` (the awkward output of the global) to `Horizontal Pod Autoscaler` — the K8s canonical Title Case form for that resource kind.
- **L04:** four lowercase `pod`/`pods` instances, capitalised via the same global substitution. No `the spec` / `what you said` / similar drift in L04 prose.

The global `pod` → `Pod` substitution is safe across these files because none of L02–L04 contain non-K8s "pod" usages (no "tripod", "podcast", "pod-tile" CSS class, etc.) and the existing capitalised "Pod"/"Pods" instances aren't case-sensitively rewritten by the substitution.

**Sub-decision D — STYLE.md concept rail breakpoint correction.** The Phase 2 implementation hides the rail at < 1240px and lets the K-Town dot-strip carry the mobile journey indicator. STYLE.md "Persistent concept rail" originally said "collapses to a horizontal progress bar at top of the page" below 720px — written before the dot-strip existed. STYLE.md is updated in this commit to match Phase 2 reality: "Visibility: rendered only at viewport ≥ 1240px (where the centred 820px main + the 170-180px rail + breathing space all fit). Below 1240px the rail is hidden; the K-Town dot-strip already serves the 'where am I in the journey' function for narrower viewports, so duplicating it as a horizontal bar would clutter mobile." Bundled into the batch-1 commit per the founder-approved "no separate STYLE.md commit just for it" rule.

**Sub-decision E — Translation Legend phrasing per lesson.** Per the canon and STYLE.md spec, the Translation Legend's left column is jargon-free story elements and the right column is canonical technical terms. Per-lesson phrasings:

- **L02 Residential District:** rows preserved structurally from the existing mapping (Each house → VM; Each apartment → container; Building's shared infrastructure → Host kernel; Land underneath → Physical hardware; Walls between apartments → Linux namespaces and cgroups). Right-column phrasing slightly tightened (e.g., "The host operating system's kernel" not just "the host operating system kernel"). The existing parenthetical "(the things that keep one container's view of the world separate from another's)" on the namespaces row is dropped from the right column — that's analogy-back-reference, not a canonical-term gloss.
- **L03 Climate Control Tower:** rows preserved (thermostat dial → YAML manifest with desired-state gloss; room → live cluster with actual-state gloss; thermostat brain → controller; thermometer → cluster reporting; heater firing → controller acting; never stops watching → reconciliation loop). Right column makes the `desired state` and `actual state` glosses explicit and italic so they read as first-mention canonical glosses.
- **L04 Port + Restaurant Row:** rows preserved (standard ISO container → 12-factor app; custom crate → pre-12-factor app; single restaurant → monolith; restaurant with stations → modular monolith; food court → microservices). Right-column phrasing made parallel — each row a single noun phrase rather than the original mix of noun phrases and parenthetical commentary.

No new rows added or dropped in any lesson. Where the original mapping list had parenthetical commentary in the left column ("apartment walls between units", "building's shared infrastructure"), the parenthetical was preserved in the left column where it carried sensory load and dropped where it duplicated the analogy.

**Reasoning:** Doing CSS + scaffolding + canon-sweep + district-line + map-embed as one per-lesson pass minimises the number of times each file needs to be opened and reduces the risk of canon drift sneaking in between commits. The Python helper is the right tool for the volume — 11+ near-identical structural transformations per lesson × 3 lessons would have meant 30+ Edit calls each requiring a unique anchor; a script with explicit anchor strings is more reliable and the script itself is reviewable. The L01 dot-strip fix is a tiny correction that's cheap to bundle here rather than ship as its own commit. The STYLE.md correction is genuinely an improvement on the original spec — the dot-strip wasn't designed yet when the rail spec was written — and bundling it with the batch keeps the doc in sync with what's actually shipped.

The Translation Legend phrasing sub-decision is mostly mechanical (canonical right column, jargon-free left), but a few rows required a judgment call when the original mapping had parenthetical commentary that was either useful (kept) or redundant (dropped). Recording these per-row choices here so future revisions can see the rationale rather than reverse-engineer it.

**Alternatives considered:** Apply each lesson's scaffolding by hand-editing rather than scripting — rejected, error-prone at this volume and harder to audit. Treat the L01 dot-strip bug as an inconsequential cosmetic detail and leave it — rejected, position 1 = anchor + L01 active is the convention every subsequent lesson inherits, and a bug in the reference cascades. Defer the canon sweep to a separate Phase 3 pass after all scaffolding lands — rejected; opening each file once is cheaper than opening it twice, and discovering canon hits while the prose context is fresh is easier than re-reading later. Skip the global `pod` → `Pod` substitution and do per-line edits — rejected, the substitution is provably safe across these files (no non-K8s pod usages) and the global approach is faster; the single "horizontal Pod autoscaler" awkward output is fixed inline.

**Revisit when:** A future batch surfaces canon hits the script's data structures don't anticipate (e.g., a lesson uses `the loop` standalone in body prose where the global substitution can't fix it). At that point, extend the per-lesson data with explicit canon-rewrite pairs rather than relying on global substitutions. Or: a future lesson has a non-K8s "pod" usage (e.g., a pod of dolphins as analogy material) that would be incorrectly capitalised — at that point, switch from `replace_all` to per-line edits for that lesson.

---

## 2026-05-02 — K-Town revision Phase 5 batch 2 — L05–L07 scaffolding + canon sweep

**Context:** Phase 5 batch 2 propagates the layman-first scaffolding family to L05 (When Kubernetes Fits / Overkill — Industrial Kitchen Block district), L06 (GitOps · Platform Engineering · SRE · Multi-Tenancy — Public Library district), and L07 (History · CNCF · Releases · KEPs · Feature Gates — K-Town Rail Yard district). Carries founder's blanket approval for all subsequent batches as long as the established protocol is followed (per-batch commit + DECISIONS entry + push, no deviation from the propagation pattern).

**Decision:** Three sub-decisions held in one entry:

**Sub-decision A — Script generalisation.** Created `scripts/apply_phase5_batch.py` as the successor to `scripts/apply_phase5_batch1.py`. The transform structure is identical; the new file accumulates per-lesson data dicts as the revision works through subsequent batches and uses an `ENABLED` list at the bottom to gate which lessons get rewritten. Each batch updates `ENABLED` to the lesson keys for that batch and runs the script. The original batch-1 script is preserved as a historical artifact (it documents what was applied to L02–L04). Future batches modify `apply_phase5_batch.py` only — append new lesson dicts, set `ENABLED`, run, commit.

**Sub-decision B — Canon sweep results, batch 2.**

- **L05 (Industrial Kitchen Block):** one lowercase `pod` hit in the §5 HFT scenario ("per pod hop"). Capitalised via global `pod` → `Pod` substitution. No prose drift on `the spec` / `what you said` / similar — L05 is about adoption fit, not desired-state language, so canon drift is naturally low.
- **L06 (Public Library):** ~15 lowercase `pod`/`pods` hits, mostly in the GitOps animation script's status strings and one flashcard. All capitalised via the global substitution. No prose drift on other Avoid-terms — L06 uses the canonical desired-state language that L03 already established.
- **L07 (K-Town Rail Yard):** zero lowercase pod hits (the lesson is meta — it's about how features evolve, not about Pod-level mechanics). One `the K8s API` hit in the Conformance glossary entry: rewritten to `the Kubernetes API`. The canon's Avoid entry says "the K8s API — implies the protocol, not the component" — in the conformance context the sentence really IS about the protocol/contract, so substituting `the API server` (the canonical *component* term) would change the meaning. Used the longer-form `the Kubernetes API` instead — same protocol-surface meaning, removes the ambiguous `K8s API` abbreviation.

The user's explicit caution about L07 — "GA / beta / alpha terminology... domain vocabulary, not synonym drift. Don't substitute them." — was respected: alpha/beta/GA, KEP, SIG, conformance, Certified Kubernetes are all domain vocab and stay verbatim. The script has no rule that touches them.

The user's other explicit caution — "L07 already has the InPlacePodVerticalScaling → Gateway API edit from Phase 1" — was respected: the §5 Gateway API scenario remained untouched by the batch 2 transform (the script's anchors are §1, §2, §3 mapping list, §4, §7 — none overlap with the §5 scenario). Verified post-transform: `InPlacePod` zero hits, `Gateway API` one hit at the expected line.

**Sub-decision C — L07 skip-if-new tag.** Per the K-Town plan §8.7 lesson-specific note ("Apply skip-if-new tag to the conformance / hydrophone-vs-sonobuoy paragraph"), L07's body paragraph at line ~573 (the Conformance description with `hydrophone` / `sonobuoy` mentions) carries the `class="skip-block"` wrapper plus a leading `<span class="skip-pill">[ deep dive — skip if new ]</span>`. This is the first lesson to use the skip-if-new component — defined in the L01 CSS but not previously triggered in batch 1. STYLE.md "Skip-if-new tag: 1-3 per lesson maximum, only in Module-2-and-deeper lessons" — L07 is end-of-Module-1; the plan calls for it specifically because the conformance paragraph genuinely is optional reading for absolute beginners.

**Reasoning:** Batch 2 is mechanically identical to batch 1 except for the per-lesson data, so the script generalisation pays off here: writing the per-lesson dicts took ~15 minutes vs hand-applying ~33 Edit calls per lesson. The canon sweep is naturally lighter than batch 1 because L05–L07 are about operational practice (when to adopt, who runs it, how it evolves) rather than the desired/actual-state machinery that drove L03's drift. The L07 skip-if-new tag is low-risk: visual treatment is muted-pill + 0.85 opacity on the paragraph, which signals "optional" without hiding content from the curious reader.

**Alternatives considered:** Apply L07's `the K8s API` fix as `the API server` — rejected, would change the sentence's meaning (the conformance test is about the API surface / protocol, not the API server component). Skip the L07 skip-if-new tag and apply skip-if-new only in Module 2 lessons — rejected, the K-Town plan §8.7 specifically calls for it on the conformance paragraph and the paragraph genuinely is the kind of "correct, useful, unnecessary for absolute beginners" content the tag is designed for. Replace `apply_phase5_batch1.py` rather than keeping it as historical — rejected, the batch-1 script documents what was applied to L02–L04 in commit `70174c3` and is the cheapest form of audit trail; deleting it would leave a gap in the revision's history.

**Revisit when:** A future batch's canon sweep needs more elaborate per-lesson rewrites than `replace_all` can express (e.g., a lesson with mixed Pod / pod usages where some are non-K8s). At that point, extend the per-lesson data dict with an explicit `canon_rewrites: list[(old, new)]` field and apply it as a final pass in `transform()`.

---

## 2026-05-02 — K-Town revision Phase 5 batch 3 — L7.5 primer + L08 scaffolding

**Context:** Phase 5 batch 3 covers two distinct artefacts: the brand-new Lesson-7.5 primer (`preview-kubernetes-lesson-7-5.html`) authored from scratch per K-Town plan §5.9, and the standard scaffolding propagation to L08 (Linux Namespaces · cgroups · Capabilities — Office Tower with Utility Meters district), which is the first Module 2 lesson and therefore the first lesson reached by readers who took the primer detour.

**Decision:** Three sub-decisions held in one entry:

**Sub-decision A — L7.5 primer file authored from scratch.** Per the K-Town plan §5.9 spec and the 2026-05-02 prerequisite-primer DECISIONS entry, the primer is a fresh standalone file at `preview-kubernetes-lesson-7-5.html`. Five short sections (What a computer actually does · What an OS is · What the kernel is · What "root" means · Why this matters for containers), one diagram (Hardware → Kernel → OS → Processes), no quiz / no flashcards / no animation. The standard scaffolding subset that applies to a primer: concept rail (L7.5 marked current, primer-italic class), district line (Foundation Tour), K-Town map (kt-pin7-5 active with the dashed-stroke primer styling), top + bottom one-sentence stamps with identical content, and the dot-strip mobile fallback. The Nightmare opener is omitted per plan §5.9 ("Nightmare opener may be omitted if the primer's purpose is purely scaffolding"). Pause-and-checks, Translation Legend, Misconceptions panel, CYOA, and skip-if-new are also omitted — there's no §1–§7 structure to attach them to, and a primer reading at this depth doesn't need comprehension gates. The primer's CSS is a curated subset of the L01 scaffolding block (only the rules the primer actually uses), plus a small `.primer-note` callout class for the cross-link banners that doesn't exist in regular lessons.

**Sub-decision B — L08 cross-link banner to the primer.** Per K-Town plan §5.9, L08 carries a small italicised banner immediately after the hero `</section>` and above the Nightmare opener: "📎 New to Linux? Take a 5-minute detour through [Lesson 7.5 — How a Linux Computer Works](preview-kubernetes-lesson-7-5.html) first." Inline-styled (no new CSS class) because this is a one-off — only L08 needs it, and adding a `.primer-banner` rule to the shared scaffolding block would mean every lesson hauls a class it never uses. If a future lesson needs the same banner pattern (e.g., a hypothetical Lesson 12.5), revisit and promote to a shared class.

**Sub-decision C — L08 cgroup v1/v2 skip-if-new tag.** Per K-Town plan §8.8, the §1 Concept paragraph defining cgroups is split into two: the canonical "cgroups are the meters" sentence stays in the main paragraph, and the trailing "Two versions exist — cgroup v1 (legacy) vs cgroup v2 (unified, modern default since ~2022)" detail is split off into its own `<p class="skip-block">` with a leading `[ deep dive — skip if new ]` pill. A factual sentence about Kubernetes 1.25+ requiring v2 for certain features (PSI-based memory pressure, `memory.high` soft cap) is folded into the skip-block paragraph as the kind of "correct, useful, unnecessary for absolute beginners" content the tag is designed for. This is L08's only skip-if-new tag — within plan §5.6's "1-3 per lesson maximum, only Module-2-and-deeper lessons" rule.

**Canon sweep results:** L08 had 5 lowercase pod/pods hits in §5 real-world scenarios and the animation script. All capitalised via global `pod` → `Pod` substitution. Note: this includes one `<code>kubectl describe pod</code>` (CLI command) which becomes `<code>kubectl describe Pod</code>` — kubectl accepts both case forms for resource names; the K8s docs convention is lowercase but the canon prefers Pod. Trade-off accepted: canonical noun usage prioritised over CLI doc convention. If this becomes confusing in user testing, the per-line CLI-command exemption can be added to a future per-lesson `canon_rewrites` field.

**Reasoning:** The primer is structurally different from regular lessons — it's a 5-minute reading detour, not a full pedagogical unit. Authoring it from scratch (rather than running the scaffolding script and then deleting unused parts) keeps the file lean and signals "this is a different kind of artefact." The L08 cross-link is small and context-specific; making it a one-off is cheaper than adding shared CSS for a single use-case. The cgroup v1/v2 skip-if-new tag is the right scope per plan — beginners need to know cgroups exist and limit resources, but the v1-vs-v2 history isn't needed until the reader is debugging or operating Kubernetes 1.25+.

**Alternatives considered:** Run the scaffolding script on the primer and post-process — rejected, the primer's structure (5 short prose sections, one diagram, no §-named blocks) doesn't match the script's anchors and would force fragile workarounds. Tag the entire cgroup paragraph as skip-block — rejected, beginners genuinely need to know cgroups exist; only the v1/v2 history is the optional bit. Add a shared `.primer-banner` class to L01's CSS — rejected, single-use class would bloat the scaffolding block; promote later if needed. Capitalise `pod` only outside `<code>` blocks — rejected for now, would require per-line edits across the file; the global is faster and the CLI-Pod-vs-pod ambiguity is small.

**Revisit when:** A second primer is needed (e.g., a hypothetical "Networking primer" between Lessons 16 and 17). At that point, factor the primer-specific CSS subset and the `.primer-note` class into a shared snippet so the second primer doesn't repeat L7.5's bespoke styling.

---

## 2026-05-02 — K-Town revision Phase 5 batch 4 — L09–L11 scaffolding + canon sweep

**Context:** Phase 5 batch 4 propagates the layman-first scaffolding family to L09 (Container Runtimes & OCI — Customs Warehouse), L10 (Image Building · Multi-stage · Distroless · SBOM — Bakery District), and L11 (Container Security & Registries — K-Town Bank Vault Quarter). All three are Module 2 lessons (after L08), so each receives at least one `skip-if-new` tag where the K-Town plan §8.NN calls for it.

**Decision:** Three sub-decisions:

**Sub-decision A — Section 7 intro pattern made flexible.** L10 was the first lesson to ship without a `<p>` intro paragraph between its §7 H2 and the flashcard grid (`<h2>Lock it in</h2>` → straight into `<div class="flashcard-grid">`). The script's regex `SECTION7_INTRO_PATTERN` required the intro `<p>`. Updated to make the `<p>([^<]+)</p>` group optional (`(?:    <p>([^<]+)</p>\n)?`) so future lessons missing an intro paragraph don't fail. The replacement text always emits the canonical intro phrase ("Three common misconceptions to clear up first, then the flashcards and quiz.") so output is uniform across all lessons regardless of whether the original had one. Caught and fixed mid-batch — re-ran with L10 + L11 after the regex update; L09 was already done before the issue surfaced.

**Sub-decision B — Skip-if-new tags applied per K-Town plan.**

- **L09:** the §1 Concept paragraph describing the high-level vs low-level container runtime split (`runc` / `crun` / `youki`) wraps in `<p class="skip-block">` with the `[ deep dive — skip if new ]` pill. Justified per plan §8.9 — beginners need to know that "container runtime" exists; the runc-vs-crun-vs-youki history is correct, useful, and unnecessary for the first read.
- **L10:** the §1 Concept paragraph on `docker buildx --platform` multi-arch builds wraps in `skip-block`. Plan §8.10 calls this paragraph "buildx multi-arch internals." Beginners don't need cross-architecture build details on the first read; they encounter the symptom (wrong-arch crash) in L09's CYOA, then the fix shows up here for the curious.
- **L11:** no skip-if-new tag added in this batch. Plan §8.11 calls only for the seccomp count Phase 1 fix (already shipped in commit `e55069b` and verified preserved across L11's prevents-row, flashcard, and glossary entries). No other §8.11 paragraph is "advanced enough to skip"; L11's content is core hardening practice that beginners should engage with.

**Sub-decision C — Canon sweep results.**

- **L09:** 10 lowercase pod hits, all in body prose and flashcard backs (Pods stuck in ImagePullBackOff, etc.). Capitalised via global. Includes one `<code>kubectl describe pod</code>` → `<code>kubectl describe Pod</code>` per the batch-3 precedent.
- **L10:** 1 lowercase pod hit (a "drop into a Pod" body reference). Capitalised via global. No prose drift on other Avoid-terms.
- **L11:** 46 lowercase pod hits — the highest count of any lesson in the revision. Reasonably so, since L11 is about hardening Pods specifically. All capitalised via global. Phase 1's seccomp count fix is preserved across all three of its locations (L11 prevents-row, flashcard, glossary). The Translation Legend has 10 rows (one row dropped from the original 11, since the "vendor seal on the box → image signing (cosign — Lesson 10)" row was a back-reference to L10's content rather than a native L11 mapping; preserving it here would have made the legend redundant). All other rows preserved structurally.

**Reasoning:** The Section 7 regex flexibility caught a real lesson-shape variant; making the intro paragraph optional (rather than requiring it) means the script keeps working as future lessons drift toward terser §7 intros. The two skip-if-new placements (L09 runtimes, L10 buildx) follow plan §8.NN exactly — no judgment call on placement, just execution. The L11 Translation Legend's 10-row trim is the only meaningful editorial call: dropping the cosign back-reference row keeps the legend honest about *this lesson's* analogy load and avoids creating apparent contradictions if a reader has skipped L10 (the cross-reference would dangle).

**Alternatives considered:** Hand-edit L10 to add a stub `<p>` intro to satisfy the original regex — rejected, the regex flexibility is the right fix and benefits future lessons. Add skip-if-new to L11 (e.g., on the Pod Security Standards version-history paragraph) — rejected, the plan §8.11 doesn't call for it and L11's content is genuinely production-relevant for beginners. Preserve the L11 cosign back-reference row in the Translation Legend — rejected, the row creates a hanging cross-reference that's confusing if read alone.

**Revisit when:** A future lesson uses a non-standard §7 structure the regex still doesn't match (e.g., §7 nested inside a `<div>` wrapper). At that point, refactor the §7 detection to walk the DOM rather than regex-match the surface text. Or: a future lesson's existing mapping list has rows that genuinely shouldn't be in the Translation Legend (cross-references, decorative entries) and the script should expose a `tl_drop_rows` field per lesson rather than requiring per-lesson hand editing.

---

## 2026-05-02 — K-Town revision Phase 5 batch 5 — L12–L14 scaffolding + canon sweep

**Context:** Phase 5 batch 5 propagates the layman-first scaffolding family to L12 (PID 1 & Container Lifecycle — K-Town Harbour), L13 (Cluster Architecture — K-Town International Airport), and L14 (The K8s API & YAML — City Hall · Permit Office). L12 and L13 are the first lessons whose CYOA reveals contain ASCII text graphics — the `pre`-formatted disaster-clock and request-trace visuals defined in the K-Town plan §8.12 / §8.13.

**Decision:** Three sub-decisions:

**Sub-decision A — ASCII text graphics in L12 / L13 CYOA reveals.** L12's CYOA reveal (the rookie-bash captain) and L13's CYOA reveal (the `kubectl apply` request trace) include `<pre>` blocks rendered with the `.cyoa-quiz .quiz-answer pre` rule defined in L01's scaffolding CSS (Phase 2). L12 shows a 30-second harbour clock with crew status and passenger loss; L13 shows the 6-hop request flow from kubectl through API server / etcd / scheduler / kubelet / runtime. Both render in monospace at font-size 12px on a `--bg-soft` background — the formatting that was already provisioned for these specific cases. No new CSS introduced; the rule fires for the first time in this batch.

**Sub-decision B — L13 skip-if-new tag on the Raft / leader-election paragraph.** Per K-Town plan §8.13, the §1.9 HA-control-plane card describing etcd's Raft consensus mechanics gets the `skip-block` class plus the `[ deep dive — skip if new ]` pill. The original paragraph already covered the operating-load-bearing fact ("lose majority → cluster goes read-only"); the skip-block expansion adds a closing sentence pointing readers who want the full Raft mechanics (term numbers, vote requests, log replication) at the Raft paper. The class is composed onto the existing `.ha-desc` class — no clash because `.ha-desc` doesn't set opacity. Plan §8.13 also called for a Phase 1 GKE/AKS/Autopilot pricing footnote (already shipped in commit `e55069b`); verified preserved in this batch (1 hit).

**Sub-decision C — L14 Translation Legend trimmed from 16 to 10 rows.** L14's original mapping list was 16 rows — the most of any lesson — covering API form structure, validation, filing, kubectl variants, and labels-vs-annotations. STYLE.md says 5–10 rows; 16 reads as overload regardless of source-material density. Trimmed to 10 by:
- Combining "custom permit template" + "custom inspector" into one row that reads "A custom permit template plus its own inspector → A CRD plus a controller (the operator pattern)" — preserves the operator-pattern teaching in one row instead of two.
- Dropping "different counters → API groups" — the API groups concept appears in L14 prose; doesn't need a Translation Legend row.
- Dropping "clerk validating → server-side OpenAPI validation" — appears in L14 prose and quiz answers.
- Dropping "asking the clerk to fill it for you → kubectl create (imperative)" — the imperative-vs-declarative teaching is carried by the Misconceptions panel's myth/truth on `kubectl run` / `kubectl create`.
- Dropping "coloured sticker on the form → labels" + "sticky notes → annotations" as separate rows — the labels-vs-annotations distinction is in the Misconceptions panel and doesn't need a legend row.

The remaining 10 rows preserve the load-bearing apiVersion/kind/metadata/spec/status structure, the kubectl-explain handbook, the etcd filing cabinet, kubectl-apply-as-form-submission, and the CRD+operator pattern.

**Canon sweep results:** L12 24 lowercase pod hits (signal-handling and zombie-reaping prose); L13 56 hits (the highest of any lesson, since L13 traces Pod creation through every CP component); L14 17 hits (mostly in the cert-manager CYOA reveal and §5 scenarios). All capitalised via global `pod` → `Pod` substitution. No prose drift on other Avoid-terms across any of the three.

**Reasoning:** The ASCII reveals in L12/L13 are the most visually distinctive CYOA cases in the entire course; provisioning the `<pre>` styling in Phase 2 paid off here without any new CSS. The L13 skip-if-new placement is a literal execution of plan §8.13 — Raft mechanics are the textbook example of "correct, useful, unnecessary for absolute beginners." The L14 Translation Legend trim is the largest editorial call this batch — 16 rows would have been 60% larger than every other lesson's legend and would have read as catalog rather than mapping. The combined "custom permit template + custom inspector" row collapses two analogy elements into one technical concept (CRD + operator), which is how the operator pattern is taught everywhere in the K8s ecosystem.

**Alternatives considered:** Render the L12/L13 ASCII reveals as inline SVG instead of `<pre>` text — rejected, the plan specifies text-graphic visuals, the `<pre>` rule was already provisioned, and SVG would reintroduce primitive-drafting overhead on a one-off illustration. Tag L14's Misconceptions content with skip-if-new — rejected, all three L14 misconceptions (CRDs second-class, imperative vs declarative, labels vs annotations) are exactly the things beginners actually believe; not optional. Preserve all 16 L14 Translation Legend rows — rejected, would have been the longest legend in the course by a wide margin and crowded into pure catalog territory.

**Revisit when:** A future lesson's CYOA needs a different visual style (e.g., a small SVG diagram rather than ASCII text) — at that point, the `.cyoa-quiz .quiz-answer` block already accepts arbitrary HTML, so the lesson can inline whatever it needs without new CSS. Or: a future Translation Legend genuinely needs more than 10 rows (e.g., a lesson with a many-to-many mapping). At that point, expose a `legend_density: 'wide'` flag in the per-lesson dict that switches to a 2-column-per-row stacked layout below 600px instead of the current single-column stack.

---

## 2026-05-02 — K-Town revision Phase 5 batch 6 — L15 scaffolding + apartment→co-living rewrite

**Context:** Phase 5's final batch covers Lesson 15 (Pods Deep Dive — Co-Living Quarter). L15 carries a special lesson-specific edit deferred from Phase 1: the apartment-as-Pod analogy is rewritten throughout the lesson to "co-living unit" so it stops colliding with L02's apartment-as-container metaphor (per K-Town plan §4.3 and STYLE.md "Crucial collision to avoid"). L15 also gets a skip-if-new tag on the QoS-class-and-eviction internals paragraph per plan §8.15.

**Decision:** Three sub-decisions:

**Sub-decision A — apartment→co-living unit substitution sweep.** Per K-Town plan §4.3 ("Replace the Pod analogy frame so Pod is *not* an 'apartment.' Use **'shared studio loft'** or **'co-living unit'** consistently throughout Lesson 15"). Picked **co-living unit** (the plan's first-listed option). Applied as a six-step substitution sequence to handle both grammatical context and casing:

1. `"shared studio apartment"` → `"co-living unit"` (1 hit at the §3 H2 + opening prose)
2. `"shared apartment"` → `"co-living unit"` (1 hit at the hero-sub)
3. `"studio apartment"` → `"co-living unit"` (1 hit in the hero illustration aria-label)
4. `"apartment"` → `"co-living unit"` (remaining lowercase mentions in prose, §3 H2 follow-up paragraphs, recap)
5. `"Apartment"` → `"Co-living unit"` (capitalized SVG comments + the original mapping row label)
6. `"APARTMENT"` → `"CO-LIVING UNIT"` (all-caps SVG inner text: `POD = ONE APARTMENT` → `POD = ONE CO-LIVING UNIT`, `POD · APARTMENT`, etc.)

One grammatical artifact ("an co-living unit" produced by the naive lowercase substitution in the ELI5 paragraph) hand-fixed to "a co-living unit" as a final pass. No other grammar issues surfaced. Verified: zero remaining "apartment" tokens in L15; 20 "co-living unit" tokens replacing them.

The Translation Legend uses 10 native co-living rows (per K-Town plan §4.3 prescription) that replace the original 15-row mapping. Rows preserved structurally: co-living unit + roommates + shared kitchen (network namespace) + shared bathroom (IPC) + each roommate's bedroom (filesystem & PID namespaces) + the doorbell (Pod IP) + handyman (init container) + helpful housemate (sidecar) + visiting plumber (ephemeral debug) + superintendent (kubelet) + rent-control class (QoS). Dropped 5 rows from the original (doorman/ambassador, translator/adapter, reserved utilities, maximum utilities, separate rent-control row) — the ambassador/adapter patterns are still discussed in L15 prose; the requests/limits → utilities mapping is covered by the QoS row.

**Sub-decision B — L15 skip-if-new tag on the QoS-class-and-eviction paragraph.** Per K-Town plan §8.15, the §1.9 italic-aside paragraph that explains "QoS doesn't grant extra memory. Even Guaranteed Pods get OOM-killed when they exceed their <em>own</em> limit. Class only affects eviction order when the <em>node</em> runs short" gets the `skip-block` class plus the `[ deep dive — skip if new ]` pill. The original paragraph's inline style (italic, ink-soft color, smaller font-size) is preserved on the same element via the `style="..."` attribute — no clash with `.skip-block` which only adds `opacity: .85`. A closing sentence about the eviction algorithm walking BestEffort → Burstable → Guaranteed (tiebreak by oldest creation time) added inside the skip-block — gives the curious reader the full mechanic without expanding the main lesson body.

**Sub-decision C — Standard scaffolding + canon sweep.** Standard transform via `apply_phase5_batch.py` (ENABLED=["L15"]): scaffolding CSS, concept rail (L01–L14 done, L15 current, L16/L17 default), district line, K-Town map (kt-pin15 active), Nightmare opener, top + bottom stamps, two pause-and-checks, Translation Legend in §3, analogy-stops-here callout, Misconceptions panel in §7, CYOA quiz, smarter quiz-reveal + pause-check JS. Canon sweep: 51 lowercase pod/pods hits before the apartment rewrite (and 0 after sequential apartment → co-living + lowercase pod → Pod substitutions). Final state: 99 canonical Pod/Pods references, zero lowercase pod, zero remaining apartment-as-Pod usages.

**Reasoning:** L15's apartment rewrite is the only deferred edit from Phase 1 — it was deferred precisely because it required surgical care across the whole lesson rather than a one-line fix. Doing it during Phase 5 alongside the scaffolding propagation means the file is touched once, end-to-end, with the new analogy and the new scaffolding consistent from start to finish. The 6-step casing-aware substitution sequence is small, mechanical, and reviewable — preferable to per-line manual edits across ~20 instances. The "an co-living unit" grammar slip caught by post-substitution grep is the only place where naive replacement broke English; one targeted fix preserves the rewrite's correctness without complicating the substitution rules. The Translation Legend trim from 15 to 10 rows follows the same logic as L11/L14 — preserve load-bearing analogy elements; drop rows that duplicate content already carried elsewhere in the lesson.

**Alternatives considered:** Use "shared studio loft" instead of "co-living unit" (plan §4.3 also offered this as an alternative) — rejected, "co-living unit" is the more common idiomatic phrase in 2020s English and matches the K-Town district name "Co-Living Quarter" exactly. Hand-edit each apartment occurrence individually — rejected, ~20 occurrences in distinct contexts (hero-sub, aria-label, SVG inner text, prose, mapping, ELI5, recap) makes the scripted-substitution approach faster and less error-prone. Tag the QoS paragraph as a full skip-block (apply class to the wrapping `<section>`) — rejected, the §1.9 section's headline + 3 QoS card entries are core content; only the trailing italic aside is "advanced + optional." Preserve the existing 15 mapping rows in the Translation Legend — rejected, would have been the longest legend in the course and would have included rows (ambassador/adapter, requests/limits separately) that duplicate prose content.

**Revisit when:** A reader of L02 and L15 reports that "co-living unit vs apartment" still feels arbitrary. At that point, consider whether the analogical universe needs a stronger architectural reason for the choice (e.g., L15's co-living quarter explicitly being a different building in K-Town's residential district from L02's apartment building, with a map zoom-in). Or: a future Phase 6 verification finds an apartment reference in L15 that the substitution sequence missed. At that point, add an explicit final-pass verification grep to the script.

---

## 2026-05-02 — K-Town revision Phase 5 complete

**Status:** All 16 K-COM lesson files (L01 reference + L02–L15 + L7.5 primer) carry the full layman-first scaffolding family. Apartment→co-living rewrite complete in L15. Phase 1 fixes preserved across L07 (Gateway API), L08 (seccomp), L11 (seccomp), L13 (GKE pricing). Vocabulary canon sweep applied across all lessons. STYLE.md and DECISIONS.md kept in sync. The next step is Phase 6 verification: open each lesson in light + dark mode at desktop and mobile widths, confirm no regressions in animations, and run the cross-lesson consistency checklist from `tasks/k8s-course-revision-plan.md` §9.

---

## 2026-05-02 — K-Town revision Phase 6 — automated verification clean

**Context:** Phase 6 cross-lesson verification per K-Town plan §9. Automated checks (§9.1 cross-lesson consistency, §9.2 accuracy spot-checks, §9.3 vocabulary canon spot-checks) run via grep across all 16 lesson files. Visual / reading spot-checks (§9.4 / §9.5) require browser review and remain for the founder.

**Decision:** Two minor canon-polish fixes surfaced during the verification grep, applied as a finalization commit:

1. **L13 line 992** — kubelet first-mention gloss `(the agent that runs your Pods)` → `(the node agent that runs your Pods)`. Per STYLE.md vocab canon: `the kubelet (canonical) — "the node agent" (gloss only)`. Strict reading: bare "the agent" is in the Avoid column as ambiguous; "the node agent" is the acceptable parenthetical gloss form. The change is a one-word polish.
2. **L07 line 1074** — recap-next text `what's actually inside a pod` → `what's actually inside a Pod`. Slipped through the batch-2 sweep because the recap card content was added to L07 in Phase 5 with lowercase pod and the batch-2 grep ran before the scaffolding insertion. One-character polish.

**Verification results:**

| Check | Status |
|---|---|
| Cross-lesson scaffolding (15 regular lessons + L7.5 primer) | ✅ uniform 1/1/1/1/1/2/2/1/1/3/1 across all regular lessons; primer correctly omits Nightmare/pause-checks/TL/analogy-stops/misc/CYOA |
| Seccomp count canonical phrasing in L08 (×6) and L11 (×3) | ✅ |
| L07 Phase 1 Gateway API edit preserved, no InPlacePod | ✅ |
| L13 Phase 1 GKE pricing footnote preserved | ✅ |
| L08 cross-link to L7.5 present | ✅ |
| L15 apartment→co-living rewrite complete | ✅ 0 apartment hits, 20 co-living references |
| Vocabulary canon — Avoid terms across all 16 lessons | ✅ 0 hits for `the spec` (real), `your declared intent`, `what you said`, `live state`, `the reconcile cycle`, `the watch loop`, `the K8s API`, `the agent` (after polish) |
| Lowercase pod across all 16 lessons | ✅ 0 hits (after L07 polish) |

False-positive notes: grep for "the spec" caught "the specific machine" (L04) and "the specific capabilities" (L11) — substring matches; not vocab violations. L13 has two literal `Pod.spec` field references ("kubelet reads the spec" in the request-trace; "controller WATCH picks up the spec" in the animation) — these refer to the literal `spec:` field of the Pod resource, not the abstract concept of desired state, so they stay.

**Reasoning:** The two polish fixes are too small to defer to a separate batch; both are one-token edits and both are clearly canon hits the earlier sweeps missed (L13's "the agent" was added to the Translation Legend's neighborhood, not the body prose batch-1/batch-2 sweep targeted; L07's lowercase pod entered via the Phase 5 recap-next which postdated the canon grep). Bundling them with the Phase 6 verification commit is cheaper than a separate fix-up commit.

**Phase 6 follow-ups for the founder (not automated):**

- **§9.4 Visual spot-check:** open L01, L08, L13 in a browser. Confirm new components match existing visual language. Toggle light/dark. Resize to <720px (mobile) and confirm the K-Town map collapses to the dot-strip with the correct active position.
- **§9.5 Reading spot-check:** read L08 (Module 2 entry) end-to-end as a layman, paying attention to whether the L7.5 cross-link banner lands clearly. Read L12 (PID 1) for the CYOA harbour-clock ASCII reveal — confirm the visual lands the failure moment.

**Revisit when:** A future user testing pass surfaces a different class of canon hit the grep didn't catch (e.g., conjugated forms like "agentless" or "speccing"). At that point, expand the canon-grep regex set rather than re-do the sweep.

---

## 2026-05-02 — K-Town revision Phase 6 follow-up — dot-strip list-style fix

**Context:** Browser visual review at viewport widths below 720px revealed that the K-Town mobile dot-strip rendered as unreadable mush — default browser `list-style-type: decimal` was painting "1. 2. 3. …" numerals on top of the 16 dot pins. The original scaffolding CSS block (built in Phase 2, propagated verbatim across all 16 lesson files in Phase 5) didn't reset list-style on `.ktown-strip`. Bug visible on every lesson at narrow viewport widths.

**Decision:** Add a base-level CSS rule to the scaffolding block:

```css
.ktown-strip{list-style:none;padding:0;margin:0}
.ktown-strip,.ktown-strip-label{display:none}
```

The reset rule sits *outside* the `@media (max-width:720px)` block so it applies whether the strip is hidden (>720px desktop) or shown (≤720px mobile). The existing `margin:0;padding:0` inside the `@media` block become redundant but harmless — left untouched to keep the diff minimal.

Applied via `scripts/fix_ktown_strip_liststyle.py` to all 16 K-COM lesson files (L01–L15 + L7.5 primer) in one pass. Idempotent — a second run finds no remaining instances of the original combined-only rule and exits cleanly. Verified all 16 files now contain the new base rule and still contain the original combined display:none rule.

`notes/k8s-component-templates.md` updated to document the `list-style:none` requirement so future scaffolding propagation doesn't reintroduce the bug.

**Reasoning:** Single-line CSS fix to a 16-file scaffolding block — script is the right tool for reliability and idempotency, same rationale as the per-batch propagation scripts. Keeping the original combined `display:none` rule intact (rather than refactoring it) minimises the diff and preserves every other CSS rule's specificity exactly. Putting the reset on a base rule (rather than inside the `@media` block) is forward-proof: if STYLE.md or a future scaffolding refactor extends the strip to other contexts (a sticky-header micro-strip, an in-flow tracker), the list-style reset already applies.

**Alternatives considered:** Suppress markers via `.ktown-strip::marker { content: '' }` — rejected. `::marker` works for `display:list-item` items and is well-supported in modern Chrome / Safari / Firefox, but its handling of the bullet/number gap reservation differs across browsers (some leave the gutter visible even when the marker content is empty). `list-style: none` collapses the gutter completely and is the standard idiomatic reset, supported in every browser since the 1990s. Use `<ul>` instead of `<ol>` and rely on the smaller default bullet — rejected, the dot-strip is a *position-in-sequence* indicator (lesson 1 of 16, lesson 2 of 16, etc.), so the underlying semantic *is* an ordered list; switching to `<ul>` would be semantically wrong even if the visual is identical with the reset applied. Add the reset only inside the `@media` block — rejected, even though the strip is `display:none` above 720px and the bullets aren't visible there, putting the reset on the base rule is one source of truth that survives any future change to the strip's visibility breakpoint.

**Revisit when:** Future scaffolding work refactors the dot-strip from `<ol>` to a non-list element (e.g., `<div role="list">` with `<div role="listitem">` children — semantically equivalent, ARIA-explicit, and avoids the implicit list-style problem at the root). At that point, the `list-style:none` rule becomes unnecessary and can be removed from the scaffolding CSS block. The `<ol>` choice was historical (the strip was originally drafted with `<ol>` because "ordered" matched the pedagogical intent of the lesson sequence); migrating to `role="list"` would be cleaner long-term but is not worth the one-time refactor cost on its own.

---

## 2026-05-02 — L01 K-Town universe intro — close the explainer gap

**Context:** Browser review of Lesson 01 surfaced a real gap in the K-Town framing: every lesson references K-Town (district line, map graphic, strip label, SVG title — 7+ tokens per file) but no lesson explains *what* K-Town is to a first-time reader. The K-Town plan §7.3 only specified the map graphic and the per-lesson district line; the cast (Mayor Katie, Podrick, the Thermostat) and the universe-as-frame concept were assumed to be absorbed gradually as each lesson used them. A reader landing on Lesson 01 sees "K-Town" in the chrome but has to infer the framing from the property-manager analogy and the map. Founder asked for an explicit explainer at the top of L01.

**Decision:** Add a short K-Town universe intro block to L01 only, sitting between the district line and the K-Town map graphic. ~95 words. Reading order becomes:

1. District line (one-line orientation: "Today's stop in K-Town: Mayor's Office").
2. **K-Town intro (NEW)** — names the universe, the 16-district structure, and the three recurring characters with forward pointers to where each character matures.
3. K-Town map graphic (visual rendering of the universe).
4. Hero (eyebrow / H1 / hero-sub / hero-illu).
5. Nightmare opener.
6. (rest of lesson scaffolding + body).

Shipped copy:

> 📍 **You're starting at the Mayor's Office** — the slate pin in the centre of the map below. Every lesson in this course visits one of K-Town's 16 districts; three characters recur across them. **Mayor Katie** runs the city — she *is* Kubernetes. **Podrick** is the unit that gets placed and moved (a *Pod* — Lesson 15 goes deep). **The Thermostat** is the wise gadget on every wall, who explains how things keep themselves running (first speaking part, Lesson 03). Same city, every lesson. Today: Katie.

One new CSS class: `.ktown-intro` — soft-cream `--bg-soft` background, 1px `--line` border, `--r-soft` corner radius, max-width 680px to match the map's content rail. Theme-aware via the existing `[data-theme="dark"]` overrides.

L01 only — other lessons keep just the district line + map. The intro's job is onboarding; once the reader has seen K-Town once, the per-lesson district line + map are enough.

**Drafting protocol per QUALITY.md:** Three substantively different drafts generated (cast-first listy / why-first motivational / tour-guide voice), self-critiqued, synthesised into a winning Draft D. Discards saved to `notes/k8s-revision-drafts.md` with per-draft rationale for why they lost. Brief summary:

- **Draft A (cast-first)** — solid but slightly listy, no map anchor.
- **Draft B (why-first motivational)** — strongest explanation of the cognitive-tax rationale but defensive ("That's not whimsy — it's a working agreement") and assumes the reader has already seen multiple lessons.
- **Draft C (tour-guide)** — strongest visual anchoring ("the slate pin in the centre"), tightest voice, but introduces "Pod" without a forward pointer.
- **Draft D (synthesis, shipped)** — Draft C's voice + map anchor, Draft A's clean cast list, plus explicit forward pointers for Pod (→ Lesson 15) and the Thermostat (→ Lesson 03).

**Reasoning:** The intro pays back the one-time cognitive-setup cost of K-Town for every subsequent lesson. STYLE.md "Unified analogical universe" already defines the cast and the city; this block is the prose surface that introduces them to the reader. Placing it between the district line and the map matches the reading order "orient → explain → visualize → engage" — by the time the reader scrolls into the lesson body proper, they know what K-Town is and who lives there. Restricting to L01 (rather than every lesson) keeps the framing as onboarding, not as recurring chrome — STYLE.md "Don't let the city framing crowd the actual content."

The "(first speaking part, Lesson 03)" parenthetical is mildly jokey but consistent with the Thermostat's slightly-grandfatherly character per STYLE.md "Unified analogical universe — Kubernetes (K-Town)." Acceptable register risk.

**Alternatives considered:** Place the intro inside L01's hero (between H1 and hero-sub) — rejected, would compete with the lesson's own opening claim ("What is Kubernetes?") for the reader's first focus. Place it inside the `.ktown-map-wrap` div as a caption *under* the map — rejected, the visual reading order "see the city, then read about it" is acceptable but the chosen "read first, then see the visual" is slightly stronger because the intro names the slate-pin-at-centre that the reader is about to look at. Make the intro a `<details>` collapsible on every lesson (collapsed by default except L01) so returning readers can refresh — rejected for now as scope expansion; can promote later if user testing wants it. Push the intro into Lesson 7.5 primer instead — rejected, L7.5 is read by readers who need a Linux primer specifically; not all L01 readers go through it.

**Revisit when:** User testing surfaces that returning readers want a K-Town reminder on later lessons, OR a second domain (VMware, AWS) reaches universe parity and needs its own intro pattern. At the second-domain point, factor `.ktown-intro` into a generalised `.universe-intro` class so the same shape works for whatever the next domain's universe is named.

---

## 2026-05-02 — L01 K-Town meta explainer — close the why-K-Town gap

**Context:** Founder review of the just-shipped K-Town universe intro (DECISIONS entry directly above) surfaced a deeper gap: the universe intro names the cast (Mayor Katie, Podrick, the Thermostat) but doesn't first tell the reader *why* K-Town exists at all — that it's a teaching device chosen to make Kubernetes' concept-heavy vocabulary easier to absorb. A first-time reader landing on Lesson 01 needs the meta explanation ("we built a stylised city to help you learn") *before* the specific cast introduction ("Katie does X, Podrick does Y"). Otherwise the cast intro reads as a charming-but-arbitrary list rather than the deliberate pedagogical move it is.

**Decision:** Add a second L01-only block — the **K-Town meta explainer** — sitting between the district line and the universe intro. ~125 words, three short paragraphs in a why → how → payoff arc, ending with an explicit navigational pointer telling the reader what comes next on the page. New reading order on Lesson 01:

1. District line ("📍 Today's stop in K-Town: Mayor's Office.").
2. **K-Town meta explainer (NEW)** — what K-Town is, why we built it, how each lesson uses it, what the reader should expect to walk away with. Slate-left-border `<aside>`, ~125 words.
3. K-Town universe intro (the cast — Katie / Podrick / Thermostat). Soft-cream box, ~95 words.
4. K-Town map graphic (the visual rendering of the universe).
5. Hero / Nightmare / stamp / lesson body.

Shipped copy (Draft D, synthesis of three substantively different drafts per QUALITY.md):

> 🏙 **Before we start — about K-Town**
>
> Kubernetes has a lot of moving parts and a lot of jargon (Pods, controllers, kubelets, sidecars, schedulers, the API server). Learning each one as an abstract technical term is exhausting and easy to forget.
>
> So instead of starting with vocabulary, we built **K-Town** — a stylised city where every Kubernetes concept lives somewhere you can picture. Each lesson takes you to one district. You learn the place first (a property manager, a thermostat, a bakery) and then the technical name for it.
>
> By the end of the course you won't have memorised 60 disconnected terms — you'll have walked a city you know. The map below shows the whole city; the panel under it introduces the recurring characters. From there, the lesson begins.

One new CSS class: `.ktown-meta` — slate left-border accent (4px), no fill background, max-width 680px to align with the map's content rail and the universe intro below. Visually distinct from `.ktown-intro` (which has the soft-cream fill) — the meta block reads as "the author speaking to you before the lesson starts" while the cast block reads as "framed callout." Both theme-aware via the existing `[data-theme="dark"]` overrides.

L01 only — same scope as the cast intro. Together the two blocks give a first-time reader a complete onboarding arc: meta (why) → cast (who) → map (where) → lesson (what). Subsequent lessons keep just the district line + map; the reader has been onboarded.

**Drafting protocol per QUALITY.md:** Three substantively different drafts generated (concrete-examples / explicit-contrast / confident-lead), self-critiqued, synthesised into Draft D. Discards saved to `notes/k8s-revision-drafts.md` with per-draft rationale. Brief summary:

- **Draft A (concrete examples)** — friendliest tone but leaks future districts the reader hasn't met.
- **Draft B (explicit contrast)** — strongest framing but slightly defensive ("Most tutorials do X").
- **Draft C (confident lead)** — tightest voice but missed the navigational pointer.
- **Draft D (synthesis, shipped)** — inherits Draft C's voice + closer ("walked a city you know"), adds Draft A's why-first framing minus the leaked-districts trap, adds an explicit "the map below… the panel under it… from there, the lesson begins" pointer that signposts the rest of the page for the reader.

**Reasoning:** The two L01-only blocks operate at different levels of abstraction and answer different reader questions: "What's the framing for this whole course?" (the meta block) vs "Who am I going to meet across the lessons?" (the universe intro). Splitting them rather than combining keeps each tight and unambiguous. The slate left-border style on the meta block (vs the soft-cream box on the universe intro) gives the reader a visual cue that these are different *kinds* of pre-lesson context — the meta is a teacher's note before class begins; the cast intro is the front-of-the-room introduction of the recurring players. Together they form an arc that the lesson body completes.

The closing "From there, the lesson begins" is intentional — it tells the reader explicitly that the meta + cast + map are scaffolding and the actual lesson body is about to start. Layman-first signposting.

**Alternatives considered:** Combine the meta and cast into one longer block — rejected, would be ~220 words and would obscure the distinction between "why this universe exists" and "who lives in it." Place the meta block *below* the cast intro (so cast comes first) — rejected, the meta explanation is the deeper why; readers absorb it more cleanly when it precedes the specifics rather than retroactively justifying them. Make the meta block a `<details>` collapsed by default — rejected, the pedagogical why is exactly what an absolute-beginner first-time reader most needs to read; hiding it behind a click would defeat the purpose. Apply the meta block to every lesson — rejected, the meta is onboarding (read once, internalised); repeating it on L02–L15 would clutter chrome that's already dense.

**Revisit when:** A reader test surfaces that some readers skip the meta block and head straight for the lesson body. At that point, consider styling the meta block more like the existing Nightmare opener (warm-coral border + tag) so it reads as more visually arresting. Or, conversely, if testing surfaces that readers feel the meta block is *too much* upfront context, consider moving it inside an opt-in `<details summary="What is K-Town?">` so the curious can open it and the impatient can skip. Either change is a one-class-edit and ~5 minutes of work.

---

## 2026-05-02 — K-Town expansion — two new districts for Lessons 16 and 17

**Context:** The K-Town revision plan (`tasks/k8s-course-revision-plan.md`) covered Lessons 01–15. Lessons 16 (workload controllers) and 17 (services & networking) appeared in the concept rail of every lesson as "future" items but had no district assigned, no per-lesson copy, and no pin on the K-Town map. Founder asked to "proceed with creating rest of the lessons" with full blanket approval. New districts must be added to the K-Town universe before lesson production per CLAUDE.md "When you encounter a needed analogical district that doesn't exist in the universe."

**Decision:** Two new K-Town districts and the corresponding map / strip / cast updates.

**Sub-decision A — Lesson 16 → K-Town Dispatch Office** (workforce dispatch and work-order tracking).

The analogy: workload controllers are the city's workforce dispatch service. **Deployments** are rotating shifts — anyone fills the slot, last shift's worker rolls off as next shift's worker rolls on (interchangeable Pods, rolling updates). **StatefulSets** are assigned-seat employees — Anna at desk-0, Brian at desk-1, each keeps their identity across shifts (stable Pod identity for stateful apps). **DaemonSets** are the one-per-building watchman (one Pod per node). **Jobs** are one-time work orders. **CronJobs** are the scheduled maintenance round (every Tuesday at 2 AM). The Dispatch Office is the controller that issues, tracks, and reissues these orders — when a worker leaves, the office sends a replacement; when shift demand changes, the office adjusts the headcount.

Pin position: (295, 255) — civic-adjacent slot in the existing 800×420 viewBox, between L15 Co-Living Quarter (170, 255) and L14 City Hall · Permit Office (470, 255). Reads geographically as another piece of municipal infrastructure adjacent to the civic core.

**Sub-decision B — Lesson 17 → K-Town Switchboard** (the city's telephone exchange and street-routing system).

The analogy: services and networking are how citizens reach businesses and how packages move regardless of which building anyone is in today. **ClusterIP** is the internal directory — Pods find each other by service name without knowing the address. **NodePort** is the public phone booth on each block. **LoadBalancer** is the dispatch operator routing incoming calls to the next available booth. **Ingress** is the city's main-entrance turnstile (HTTP/HTTPS routing rules). **Gateway API** is the next-gen turnstile system the city is migrating to. **NetworkPolicy** is the traffic rules — who's allowed to call whom.

Pin position: (530, 290) — commercial-east slot, east of L10 Bakery District (350, 290) and south-west of L09 Customs Warehouse (660, 265). Reads geographically as commercial / civic-tech infrastructure.

**Sub-decision C — Map + strip propagation.** The K-Town map primitive (`library/primitives/kubernetes/k-town-map.svg`) grew from 16 pins to 18. Per the Phase 2 inline-embed convention, every existing lesson's K-Town SVG is a copy of the primitive's symbol body — so the same two pins must be added to all 16 existing lessons (L01–L15 + L7.5 primer). Same applies to the mobile dot-strip `<ol>` (currently 16 dots; now 18). Propagation handled by `scripts/expand_ktown_to_18_pins.py` — idempotent script with explicit anchor strings, runs in seconds. The L16 and L17 lessons themselves carry the `active` class on their respective new pin and the corresponding strip dot.

**Sub-decision D — Concept rail unchanged.** The 18-item concept rail in every existing lesson already lists L16 ("workload controllers") and L17 ("services & networking") as future `○` items — these were future-proofed in the Phase 2 build. No retrofit needed. When the new lessons ship, their own concept rails mark L16 / L17 as `▶ current` per the existing convention.

**Sub-decision E — Recurring cast unchanged.** STYLE.md "Unified analogical universe" lists Mayor Katie, Podrick, and the Thermostat as the three regular characters. L16 introduces a *role* — the Dispatcher — but not as a named recurring character; the Dispatcher is a job title for whichever controller is being discussed. L17 introduces the *Switchboard Operator* in the same role-not-character sense. Per STYLE.md "Beyond Katie, Podrick, and the Thermostat, every additional character is overhead" — both new districts honour this rule.

**Reasoning:** Both districts fit the existing K-Town map without requiring a viewBox extension (which would have meant updating the inline SVG of every lesson's mapped coordinates, not just adding pins). The chosen positions also make geographic sense — L16 sits in the civic / municipal-services row alongside L14 Permit Office and L15 Co-Living Quarter; L17 sits in the commercial-east row alongside L09 Customs Warehouse and L10 Bakery District. The analogies map the K8s controllers and Service types one-to-one with intuitive city-life equivalents (rotating shifts vs assigned-seat workers, phone booth vs internal directory) — reading either district's Translation Legend should produce the click STYLE.md "Analogy" voice asks for.

**Alternatives considered:** Place L16 (Dispatch) at (340, 145) — upper-middle row — rejected, would crowd the existing row of L02 / L06 / L11 + the new L17 placement. Use an entirely new "Crew HQ" framing for L16 — rejected, "Dispatch Office" is more widely understood and maps more cleanly to the controller-issues-and-tracks-work-orders behaviour. Use "Postal Exchange" for L17 — rejected, telephone-exchange (Switchboard) maps better to the protocol-level routing semantics (ClusterIP/NodePort/LoadBalancer all about *who-finds-whom*, not *who-delivers-what*). Promote the Dispatcher and the Switchboard Operator to recurring cast members — rejected, would expand cast beyond the 3-character cap STYLE.md set. Extend the 800×420 viewBox to 800×460 to fit a fresh row for the new pins — rejected, would require updating the viewBox in all 16 inline copies (extra script complexity for marginal layout gain).

**Revisit when:** A future lesson's analogy genuinely demands a fourth recurring character (e.g., a Lesson on persistent volumes might need a "warehouseman" character to anchor PV/PVC/StorageClass). At that point, log a separate DECISIONS entry per "Do not introduce a new recurring character without a DECISIONS.md entry." Or: a future Lesson 18 / 19 needs a district that doesn't fit the current viewBox — at that point, extend to 800×460 in one batch rather than incremental viewBox bumps.

## 2026-05-03 — K-Town expansion — six new districts for L18-L44 + lesson generator pattern

**Context:** Founder requested overnight production of L18-L44 (the full 17-module syllabus). 27 lessons in one batch, with explicit blanket approval. Hand-authoring per-lesson HTML at the L17 reference-implementation cadence (~1000 lines each, ~27,000 lines total) was infeasible within a single session's output budget. Several lessons also introduced topics with no obvious match to the existing 18 K-Town districts (security cluster-side, observability, autoscaling, application delivery, operators, troubleshooting). Per CLAUDE.md "When you encounter a needed analogical district that doesn't exist in the universe, propose the new district before using it" — and per the curriculum plan in `tasks/k8s-comprehensive-curriculum-plan.md` which pre-listed the 6 anticipated new districts.

**Decision:** A lesson-generator architecture for the L18-L44 batch + 6 new K-Town districts.

**Sub-decision A — Lesson generator at `scripts/k8s_lesson_generator.py`.**

Each L18-L44 lesson is authored as a Python `LessonSpec` dataclass under `scripts/lessons/lessonNN.py` containing only the unique-per-lesson content (hero SVG, sections, scenarios, flashcards, quizzes, glossary, recap). The shared template (CSS, K-Town map SVG with current-pin highlighted, concept rail with current row marked, topbar, district line, dot-strip, end-of-page script block) is rendered by the generator from `BaseLessonSpec` shared with the canonical L18 reference. Run via `python3 scripts/k8s_lesson_generator.py scripts/lessons/lessonNN.py`. Output: `preview-kubernetes-lesson-NN.html` matching the established L17/L18 template.

This trades hand-tuning per-lesson micro-variation for consistent structural output. A regression in any one lesson is fixable by editing the spec module + regenerating, not patching 27 separate HTML files. The generator does not produce per-lesson animation `<script>` blocks — only static SVG illustrations — because animation work was out of scope for this batch (see L17 for the per-lesson animation pattern).

**Sub-decision B — Six new K-Town districts** (positions inside the existing 800×420 viewBox; no viewBox bump):

| # | District | Pin | Lessons that use it |
|---|---|---|---|
| 27 | **Watchtower** (security cluster-side: RBAC, admission, hardening) | (740, 105) | L27 (RBAC), L28 (admission), L29 (policy engines), L31 (multi-tenancy) |
| 32 | **Observatory** (observability: logs, metrics, traces, eBPF, SLOs) | (230, 105) | L32 (logs+metrics), L33 (traces+eBPF+SLOs) |
| 34 | **Power Station** (capacity & resilience: autoscaling + HA) | (230, 295) | L34 (autoscaling), L35 (PDB / multi-zone / DR) |
| 36 | **Print Shop** (application delivery: Kustomize, Helm, progressive delivery) | (410, 295) | L36 (Kustomize), L37 (Helm), L40 (progressive delivery) |
| 42 | **Workshop** (operators / custom controllers) | (700, 305) | L42 (Kubebuilder + controller-runtime) |
| 44 | **Detective's Office** (troubleshooting / investigation methodology) | (770, 245) | L44 (capstone troubleshooting) |

Each district anchors at least one lesson; several anchor 2-4 lessons (security stack, observability, autoscaling+reliability, delivery). Existing districts are reused where the topic naturally lives there: L18-L19 reuse Customs Warehouse (storage); L20-L21 reuse Permit Office (paperwork / credentials); L22-L23 reuse Dispatch Office (routing); L24-L26 + L43 reuse Switchboard (network); L30 reuses Bank Vault Quarter (trust ledger); L38-L39 reuse Public Library (catalogue / source-of-truth); L41 reuses Permit Office (custom forms = CRDs).

**Sub-decision C — Pin propagation script.** `scripts/expand_ktown_to_24_pins.py` (mirror of the L16/L17 expansion script) adds the 6 new pins to the canonical primitive (`library/primitives/kubernetes/k-town-map.svg`) and to the inline K-Town SVG copy in every older lesson (L01-L17 + L7.5 + the previously-shipped L18). Also extends the mobile dot-strip from 18 → 24 entries and updates the "lesson N of M" suffix. Idempotent; safe to re-run.

**Sub-decision D — Recurring cast unchanged.** Per the L16/L17 entry's STYLE.md cap of 3 recurring characters (Mayor Katie, Podrick, the Thermostat), the new districts introduce *roles* not *named characters*: the Watchman (Watchtower), the Astronomer (Observatory), the Substation Manager (Power Station), the Press Operator (Print Shop), the Master Craftsperson (Workshop), the Detective (Detective's Office). These are job titles for whichever controller / SRE / operator is being discussed, not new cast members.

**Reasoning:** Pre-listing the new districts in `tasks/k8s-comprehensive-curriculum-plan.md` (the curriculum brief approved before this session began) avoided per-district approval pauses during overnight production. The lesson-generator architecture is the only realistic path from "L18 hand-authored as the reference implementation" to "L19-L44 shipped consistent with L18" within a single session's output budget. Reusing existing districts wherever the topic fits keeps the K-Town atlas focused (24 pins, not 27) and avoids the "every lesson is a new place" beginner-overload the unified-universe pattern was designed to prevent in the first place. The 6 new districts cluster geographically — Observatory + Power Station fill the previously-empty top-left and middle-left of the city, Watchtower + Detective's Office occupy the security/investigation side of the east wall, Print Shop + Workshop fill the south-central commercial belt — which keeps the map readable.

**Alternatives considered:** Hand-author all 27 lessons. Rejected — output budget. Skip new districts and shoehorn every L18-L44 topic into existing districts. Rejected — security topics have nothing to do with the warehouse/library/switchboard analogies, and forced metaphors would break the pattern that makes K-Town valuable. Bump viewBox to 800×500 to add a fresh row of pins. Rejected — would require updating viewBox in every inline SVG copy across all 19 older files; the chosen 6 positions fit the existing viewBox. Use a separate map for the L18-L44 lessons. Rejected — the whole point of the unified atlas is one map; visitors should see the city growing, not a fork.

**Revisit when:** A future K-COM expansion (e.g., a deep dive into edge K8s, mobile Pods, multi-cluster fleet management) needs additional districts that don't fit the 800×420 viewBox. At that point, bump to 800×500 in one coordinated update (script + primitive + propagation across all 45 lesson files). Or: when an L18-L44 lesson is ready for the per-lesson animation pass — the generator's static-SVG output is intentionally the floor, not the ceiling.

## 2026-05-03 — Audit runs immediately after every generation pass

**Context:** L01-L17 + L7.5 + L18-L44 build complete (45 lessons). The first cross-lesson audit found 62 mechanical issues (footer "of N" stale on every older lesson, strip-dot count inconsistent — 24 / 30 / 45 — across batches, L18 animation referencing a nonexistent element id, L18 packet motion landing in dead space, L18 strip label saying "lesson 19 of 24"). Every one of these would have been caught at generation time if an audit had run automatically. Founder asked: make the audit run immediately after generation as a standing rule.

**Decision:** Two audit scripts always run after any generation/regeneration pass. The lesson generator (`scripts/k8s_lesson_generator.py`) auto-runs both audits at end-of-main and exits non-zero if either reports issues. CLAUDE.md "Audit runs immediately after generation" rule documents this.

**Sub-decision A — Two audit scripts.**

  - `scripts/audit_lessons.py` — mechanical: HTML tag balance per lesson, all 24 K-Town pins present, active pin matches expected district, strip dot count = 45, footer/strip-label "of N" = 45, animation block presence for L18-L44, animation packet move_to within viewBox, animation set_text/set_attr targets reference existing element ids.
  - `scripts/audit_lessons_v2.py` — content + alignment: required sections present (1, 1.5? optional, 2, 3, 4, 5, 6 for L18-L44, 7), animation packet move_to lands inside (or within 30px of) a scene rect (catches dead-space motion), ELI5 length 12-130 words, stamp present at top and bottom, glossary + recap present, concept-rail count consistency across L19-L44.

**Sub-decision B — Primer exemption.**

L7-5 (the prerequisite primer per DECISIONS 2026-05-02 "Lesson N.5 pattern") is intentionally lighter and exempt from v2's "Section 7 / glossary / analogy-stops" checks. The exemption is hard-coded as `PRIMER_EXEMPT = {"7-5"}` in `audit_lessons_v2.py`. All non-primer lessons must pass both audits cleanly.

**Sub-decision C — Generator integration.**

`k8s_lesson_generator.py` runs both audits via `subprocess` after every successful render. Output is concise (one line per audit when clean; full failure block when not). The generator exits with code 2 if either audit reports issues, blocking accidental commits of broken lessons. A `--no-audit` flag exists for emergency bypass but is not the default and is documented as not recommended in CLAUDE.md.

**Reasoning:** Audit-after-generation is the cheapest, highest-leverage quality control. The same regex that flagged "of 16" stale footers across L01-L17 catches the next regression in seconds. Coupling it to the generator means there's no path where a developer runs the generator, eyeballs the output, and ships without checking — every regen is an audit. The two-audit split (mechanical vs content) keeps each fast (~50ms cluster-wide) and lets us iterate on each independently as new categories of issue emerge.

**Alternatives considered:** Run audit only in CI. Rejected — too slow a feedback loop; developers iterate locally. Run audit on every git commit hook. Rejected — runs even for unrelated changes (docs, scripts), adds friction. Block via mandatory pre-commit script rather than wiring into the generator. Rejected — generator is the single chokepoint where lesson HTML is produced; better to enforce there. Single combined audit script. Rejected — mechanical and content checks have very different false-positive profiles; splitting them lets each be tuned independently.

**Revisit when:** A new lesson type is introduced (e.g., a new primer style, an "interactive lab" lesson) that legitimately fails one of the v2 checks. At that point: add it to the exemption set + log here. Or: a new audit category (image alignment math, vocabulary canon enforcement, accessibility) gets enough wins to justify a v3 audit script — same auto-run pattern.
