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