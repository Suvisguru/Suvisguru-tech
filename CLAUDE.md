# Standing instructions for Claude Code sessions in this repo

You are operating inside a content factory that produces visually-driven technical training lessons at scale. Your output must be consistent across thousands of lessons produced over months by many sessions. This file is your standing protocol.

## At the start of every session

Before doing anything else, read these files in order:

1. `PROJECT.md` — what we are building and how
2. `DECISIONS.md` — meaningful past choices and their reasoning
3. `STYLE.md` — house style for visuals, motion, narrative, interaction
4. `QUALITY.md` — drafting protocol and definition of "good enough to ship"

If the current task is producing a lesson, also read:

5. The five most recently modified lessons in the same domain (look in `/courses/{domain}/`) — to maintain stylistic continuity
6. The component library inventory at `/library/primitives/{domain}/` — to know what already exists

After reading, briefly confirm in one sentence that you have absorbed the protocol, then proceed with the task.

## When the founder uploads a topic to /inbox

Treat the inbox file as a topic submission. Your first action is to produce a structured intake brief at `/courses/{domain}/{course-slug}/scenarios/{nn-slug}/brief.yaml` and present it to the founder for approval. Do not begin lesson production until the brief is approved.

The brief must cover: granularity (course / sub-topic / concept), parent topic if applicable, prerequisites the learner is assumed to have, the moments of confusion this lesson will resolve, and (if the topic is large) a proposed split into sub-topic lessons.

If the topic is too large for a single lesson, propose the split. The founder approves the split before any lesson production begins.

## When producing a lesson

Walk the nine-stage pipeline defined in PROJECT.md:

1. Intake (already done if briefing is approved)
2. Decomposition (already done if briefing is approved)
3. Concept explanation
4. Before/after, analogy, ELI5/ELI10
5. Real-world scenarios
6. Static SVG diagram
7. Animated SVG illustration
8. Flashcards and quiz
9. Self-review against STYLE.md, QUALITY.md, and the definition of done

Produce sections incrementally. After each major section, summarize what you produced and ask if the founder wants revisions before proceeding.

Apply the **layman-first scaffolding** to every lesson preview: Nightmare opener at the top, one-sentence stamp at top and bottom, two mid-lesson pause-and-checks, Translation Legend in the analogy section, Common Misconceptions panel before the quiz, "analogy stops here" callout where the analogy has a known cliff, "skip if new" tags on advanced paragraphs, persistent left-rail concept map. These are not optional. See STYLE.md for the component spec of each, and QUALITY.md for the bar each must meet.

Apply the **unified analogical universe** convention for the domain. For Kubernetes that is K-Town — see STYLE.md "Unified analogical universe — Kubernetes (K-Town)" for the cast (Mayor Katie, Podrick, the Thermostat) and the district-to-lesson mappings. Each lesson opens with a district line and includes the K-Town map graphic with the current district highlighted.

## Quality gating

For every section with a creative dimension (analogy, ELI5, ELI10, real-world scenarios, before/after, Nightmare opener, one-sentence stamp), follow the drafting protocol in QUALITY.md: generate at least three substantively different drafts, self-critique each one, select a winner with reasoning, revise once, and save the discarded drafts to `NOTES.md` in the lesson folder. Do not present a section to the founder that you know is mediocre.

## When you encounter a needed primitive that does not exist in the library

Stop. Draft the primitive in `/library/primitives/{domain}/{primitive-name}.svg` and present it for approval. Do not embed an ad-hoc version inline in the lesson. The library is canonical.

## When you encounter a needed analogical district that doesn't exist in the universe

Same protocol. Stop. Propose the new district — where it sits in the city, who lives there, what the analogy element maps to — and seek founder approval. Once approved, add it to STYLE.md "Unified analogical universe" and log it in DECISIONS.md before using it in a lesson.

## When you make a non-trivial choice

Anything that affects future lessons or contradicts a previous pattern is non-trivial. Examples: introducing a new color, a new component shape, a new motion convention, a new section format, a new file location, a new recurring character, a new district.

Before committing such a choice, draft a DECISIONS.md entry following the template in that file, and ask the founder for approval. After approval, append the entry to DECISIONS.md in the same commit as the change.

## When you establish a new visual or narrative convention

Update STYLE.md in the same commit as the lesson that introduced it. Never let a convention be implicit. If you produce two lessons with different conventions for the same situation, drift has begun.

## File and folder conventions

- Lessons live under `/courses/{domain}/{course-slug}/scenarios/{nn-slug}/` where `nn` is a zero-padded number reflecting course order.
- Slugs are lowercase, hyphenated, no spaces, no special characters.
- Every lesson folder contains: `brief.yaml`, `lesson.md`, `diagram.svg`, `animation.html`, `flashcards.yaml`, `quiz.yaml`, optionally `voiceover.md` and `NOTES.md`.
- Inbox files live under `/inbox/` and are dated in the filename: `YYYY-MM-DD-topic-slug.md`.
- Multi-lesson task briefs (e.g., a full course revision plan) live under `/tasks/` with a descriptive filename and are deleted or archived to `/tasks/archive/` once executed.

## Memory and continuity

You do not retain memory across sessions. Continuity comes from the files. Three rules:

- Always read PROJECT.md, DECISIONS.md, STYLE.md, and QUALITY.md at session start. No exceptions.
- Always read the five most recently modified lessons in the same domain before producing a new one. This is what keeps the 800th lesson looking like the 1st.
- Always log decisions and update style guide in the commit where the change occurred. Never defer.

## What you do not do

- Do not invent new section structures. The seven sections are fixed.
- Do not redraw existing primitives. The library is canonical.
- Do not invent a new analogy when the lesson's domain has a unified-universe district mapping for the topic. Use the assigned district.
- Do not introduce a new recurring character without a DECISIONS.md entry. The cast is canonical.
- Do not skip the layman-first scaffolding (Nightmare, stamp, pause-and-checks, Translation Legend, Misconceptions). Each is a hard gate.
- Do not produce a lesson without an approved brief.
- Do not skip the static diagram before the animation.
- Do not skip the QUALITY.md drafting protocol. Generate multiple drafts; self-critique; pick a winner with reasoning.
- Do not ship a lesson without flashcards and quiz.
- Do not silently establish new conventions. STYLE.md must always reflect reality.

If you are uncertain whether something is a deviation from the protocol, stop and ask the founder.
