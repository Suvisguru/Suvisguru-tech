# Standing instructions for Claude Code sessions in this repo

You are operating inside a content factory that produces visually-driven technical training lessons at scale. Your output must be consistent across thousands of lessons produced over months by many sessions. This file is your standing protocol.

## At the start of every session

Before doing anything else, read these files in order:

1. `PROJECT.md` — what we are building and how
2. `DECISIONS.md` — meaningful past choices and their reasoning
3. `STYLE.md` — house style for visuals, motion, narrative, interaction

If the current task is producing a lesson, also read:

4. The five most recently modified lessons in the same domain (look in `/courses/{domain}/`) — to maintain stylistic continuity
5. The component library inventory at `/library/primitives/{domain}/` — to know what already exists

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
9. Self-review against STYLE.md and the definition of done

Produce sections incrementally. After each major section, summarize what you produced and ask if the founder wants revisions before proceeding.

## When you encounter a needed primitive that does not exist in the library

Stop. Draft the primitive in `/library/primitives/{domain}/{primitive-name}.svg` and present it for approval. Do not embed an ad-hoc version inline in the lesson. The library is canonical.

## When you make a non-trivial choice

Anything that affects future lessons or contradicts a previous pattern is non-trivial. Examples: introducing a new color, a new component shape, a new motion convention, a new section format, a new file location.

Before committing such a choice, draft a DECISIONS.md entry following the template in that file, and ask the founder for approval. After approval, append the entry to DECISIONS.md in the same commit as the change.

## When you establish a new visual or narrative convention

Update STYLE.md in the same commit as the lesson that introduced it. Never let a convention be implicit. If you produce two lessons with different conventions for the same situation, drift has begun.

## File and folder conventions

- Lessons live under `/courses/{domain}/{course-slug}/scenarios/{nn-slug}/` where `nn` is a zero-padded number reflecting course order.
- Slugs are lowercase, hyphenated, no spaces, no special characters.
- Every lesson folder contains: `brief.yaml`, `lesson.md`, `diagram.svg`, `animation.html`, `flashcards.yaml`, `quiz.yaml`, optionally `voiceover.md` and `NOTES.md`.
- Inbox files live under `/inbox/` and are dated in the filename: `YYYY-MM-DD-topic-slug.md`.

## Memory and continuity

You do not retain memory across sessions. Continuity comes from the files. Three rules:

- Always read PROJECT.md, DECISIONS.md, and STYLE.md at session start. No exceptions.
- Always read the five most recently modified lessons in the same domain before producing a new one. This is what keeps the 800th lesson looking like the 1st.
- Always log decisions and update style guide in the commit where the change occurred. Never defer.

## What you do not do

- Do not invent new section structures. The seven sections are fixed.
- Do not redraw existing primitives. The library is canonical.
- Do not produce a lesson without an approved brief.
- Do not skip the static diagram before the animation.
- Do not ship a lesson without flashcards and quiz.
- Do not silently establish new conventions. STYLE.md must always reflect reality.

If you are uncertain whether something is a deviation from the protocol, stop and ask the founder.