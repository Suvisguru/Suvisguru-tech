# EdTech Content Factory — Visual-First Technical Training

## Vision

Build a content factory that produces visually-driven technical training lessons at scale. The founder uploads a topic; the factory produces a complete lesson package conforming to a fixed structure and house style. Initial domains: VMware, AWS, Azure, GCP, DevOps, MLOps. Brand promise: anyone willing to learn — including someone with no infrastructure background — can understand these systems because we make hard concepts visually obvious.

The proof-of-concept is a VMware packet-flow animation: a data packet visibly travels from a VM through a vSwitch, out a NIC port on a realistic Dell PowerEdge rear panel, up a patch cable, into a specific port on a top-of-rack switch, across the switch fabric, and down to a destination VM — with encapsulation shells appearing at the right boundaries and port LEDs lighting in sequence. Mode toggles let the same animation demonstrate L2, L3, and NSX overlay variants. This is the bar for every animated lesson.

## How the factory works

The founder submits a topic at any granularity — a course (`vSphere networking`), a sub-topic (`vSphere standard switching`), or a single concept (`uplink failover with beacon probing`). The factory produces a lesson package containing all required sections (defined below), conforming to the house style (defined in STYLE.md), reusing primitives from the component library, meeting the quality bar (defined in QUALITY.md), and logging meaningful decisions to DECISIONS.md.

A lesson package is reviewable, revisable, and shippable independently. Many lessons chain into a course.

## The fixed lesson structure

Every lesson produced by the factory contains exactly these seven sections, in this order. None are optional. None are reordered. Predictability is the point.

**1. Concept explanation.** Plain definition of what the topic is, what it does, and why it exists. 150-300 words. No jargon without inline definition.

**2. Before / after comparison.** What did the world look like before this technology existed? What problem did people have? How did that problem get solved (or partially solved) by this technology? Always two columns or two paragraphs explicitly labelled. Examples: how operating systems ran before virtualization vs. after; how applications were deployed before containers vs. after; how networks were configured before SDN vs. after.

**3. Analogy.** A real-world physical metaphor that maps onto the technical concept. Letters and post offices, apartment buildings and rooms, restaurants and kitchens. The analogy is what learners remember; the technical detail layers onto it. One primary analogy per lesson — resist the urge to mix three. The analogy section ends with a Translation Legend (a two-column table mapping each story element to its technical counterpart) — see STYLE.md.

**4. ELI5 and ELI10.** Two stacked explanations. ELI5 (Explain Like I'm 5) is the simplest version, using the analogy from section 3 and assuming zero prior knowledge — under 100 words. ELI10 is the practitioner-junior version, using correct technical terminology but still grounded in the analogy — 150-250 words. A reader should be able to read ELI5, understand it, then read ELI10 and feel they've leveled up.

**5. Real-world scenarios.** Three to five concrete situations where this concept applies in practice. Each scenario names the company type or use case ("a mid-size SaaS company with three regional offices"), states the problem they faced, and shows how the concept solves or partially solves it. These are the "when do I actually use this" anchors. They are not case studies — they are short, vivid, 80-150 words each.

**6. Animated SVG illustration.** A motion-graphic illustration matching the house style in STYLE.md. Mandatory for every lesson. The illustration shows the concept in motion — packet flowing, request being routed, container being scheduled, model being trained. It must conform to the visual conventions and reuse primitives from `/library/primitives/`. The packet/request motion track must trace exactly through visible components.

**7. Common Misconceptions, Flashcards, and Quiz.** Three blocks in a fixed order:
   - **Common Misconceptions.** Exactly three myth/truth pairs that call out predictable beginner traps. Each pair is one sentence of myth, one sentence of truth. Per-lesson misconceptions are anchored by what beginners *actually* believe — not strawmen.
   - **Flashcards.** Eight to twelve cards (front: question or term; back: 1-3 sentence answer).
   - **Quiz.** Two to four pause-the-animation questions that test the mental model rather than memorization ("I've stopped the packet here. What happens next, and why?"). One of these questions is a Choose-Your-Own-Adventure variant — a story-framed scenario with a click-to-reveal failure. Quiz includes correct answer and the reasoning that explains why it's correct.

## Layman-first scaffolding

The seven sections above are the *content* of every lesson. The lesson preview HTML wraps that content in scaffolding that earns the layman's attention before the content tries to teach them. Every lesson preview includes:

- **Nightmare opener.** A 2-3 sentence "3 AM Nightmare" box immediately under the lesson H1. Names a specific pain in second person ("It's 3 AM…") and ends with a one-line promise ("This lesson is about why that happens — and the fix that prevents it.") Pain first, concept second.
- **One-sentence stamp.** A bolded, boxed single-sentence takeaway repeated in two places — once under the Nightmare at the top, once just above the recap card at the bottom. If the reader forgets everything else, this is what stays.
- **District line.** One line at the top placing the lesson in the domain's unified analogical universe ("📍 Today's stop in K-Town: **the Bakery District**.") See "Unified analogical universe" below.
- **Pause-and-check (×2).** A short multiple-choice comprehension check inserted twice mid-lesson — once after Section 1 (Concept) and once after Section 4 (ELI5/ELI10). Each is 30 seconds of reader time.
- **Translation Legend.** A two-column "story → technical" mapping table inside Section 3 (Analogy), separating the narrative from the jargon. Right column uses the canonical technical vocabulary defined in STYLE.md.
- **Analogy-stops-here callout.** A small ⚠️ inline note inside Section 3 calling out the place beginners predictably overextend the analogy. Used only where the analogy has a known cliff.
- **Skip-if-new tags.** A muted pill at the start of advanced paragraphs that are correct and useful but unnecessary for absolute beginners (cgroup v1 vs v2, Raft consensus internals, etc.). Signals "decorative texture, optional read."
- **Concept rail.** A persistent left-rail visible while scrolling, showing the lesson's position in the course's concept journey. Hard-coded per-lesson, not stateful.

These scaffolding elements wrap and frame the seven content sections — they do not replace them. STYLE.md gives the visual spec for each. QUALITY.md gives the bar each must meet.

## Unified analogical universe (per domain)

Each domain may establish a single unified analogical universe — a city, a port, a garden — within which every lesson's analogy lives as a *district* of that universe. This solves the problem of beginners burning cognitive energy learning a fresh analogy every lesson; instead they accumulate familiarity with one consistent world.

The pattern, when applied to a domain:

- **Name the universe** (e.g., "K-Town" for Kubernetes).
- **Establish a recurring cast** of 2-4 characters that appear across lessons (e.g., Mayor Katie, Podrick, the Thermostat).
- **Map each lesson's analogy** to a specific district within the universe, recorded in STYLE.md.
- **Add a small map graphic** — a single SVG of the city/port/garden — that appears once per lesson with the current district highlighted.
- **Open every lesson with a one-line district pin** ("📍 Today's stop in K-Town: **the Bakery District**.").

This is a non-trivial choice for any domain — log it in DECISIONS.md before applying. The current Kubernetes universe (K-Town) is specified in STYLE.md "Unified analogical universe — Kubernetes (K-Town)." VMware does not yet have a designated universe; do not invent one without an approved DECISIONS entry.

## Topic submission protocol

The founder submits a topic by creating a folder under `/inbox/` with a filename like `2026-04-29-vsphere-standard-switching.md` containing:

- Topic title
- Domain (VMware / AWS / Azure / GCP / DevOps / MLOps)
- Granularity (course / sub-topic / concept)
- Parent topic, if applicable (e.g., this is a sub-topic of "vSphere networking")
- Prerequisites the learner is assumed to have
- Specific moments of confusion this lesson should resolve, if known
- Any notes, references, or constraints

The factory reads the inbox file and generates a full intake brief in `/courses/{domain}/{course-slug}/scenarios/{nn-slug}/brief.yaml`, which the founder reviews and approves before production starts.

Multi-lesson task briefs (e.g., a full course revision plan) are placed under `/tasks/` with a descriptive filename, executed once, and archived to `/tasks/archive/` afterward.

## The nine-stage production pipeline

For each lesson, the factory walks these stages in order. Skipping any stage produces lessons that fail.

1. **Intake.** Convert the inbox submission into a structured brief.
2. **Decomposition.** If the topic is too large, split it into sub-topics and produce a lesson per sub-topic. The founder approves the split before production.
3. **Concept explanation drafting.** Section 1 of the lesson.
4. **Before/after, analogy, ELI5/ELI10 drafting.** Sections 2-4.
5. **Real-world scenarios drafting.** Section 5.
6. **Static SVG diagram.** Always before animation.
7. **Animated SVG illustration.** Section 6, building on the static diagram.
8. **Common Misconceptions, flashcards, and quiz drafting.** Section 7.
9. **Assembly and self-review.** The factory checks the lesson against STYLE.md, QUALITY.md, and the definition of done (below).
10. **Interactive preview rendering.** The factory builds `preview-{domain}-lesson-{nn}.html` at the repo root, following the conventions in STYLE.md "Lesson preview page" section. The preview wraps the seven content sections in the layman-first scaffolding (Nightmare, stamp, district line, pause-and-checks, Translation Legend, analogy-stops-here callout, concept rail). Reference implementations: `preview-lesson-01.html` (VMware) and `preview-kubernetes-lesson-01.html` (Kubernetes).

## Definition of done for a lesson

A lesson ships when:

**Content gates:**

- All seven sections are present and meet length/structure requirements.
- The animated illustration conforms to STYLE.md.
- The animation's motion track traces exactly through visible components.
- All terms used are either commonly understood or defined inline on first use.
- The before/after comparison is explicit, not implied.
- The analogy is consistent across ELI5 and ELI10.
- The Translation Legend table is present in Section 3 with jargon-free left column.
- Section 7 includes exactly three Common Misconceptions, the flashcards covering core terms, and a quiz with one CYOA-style question among the others.
- Quiz questions test prediction, not recall.

**Scaffolding gates:**

- The Nightmare opener is present, names a specific pain, and ends with the one-line promise.
- The one-sentence stamp appears at top and bottom, identical, irreducible, no parenthetical jargon.
- The district line appears at the top with the correct district per STYLE.md.
- Two pause-and-checks are present at the prescribed positions.
- The "analogy stops here" callout is present where the analogy has a known cliff (most lessons).
- "Skip if new" tags are applied to advanced paragraphs in Module-2-and-deeper lessons.
- The persistent concept rail renders correctly with the current lesson highlighted.

**Quality gates:**

- The QUALITY.md drafting protocol was followed — multiple drafts generated, self-critique recorded, discarded drafts saved to NOTES.md.
- The first-time-learner test was performed and any defects were fixed.
- The layman test (would a non-technical reader make it through and remember the takeaway?) was performed.

**Convention gates:**

- New visual conventions, if any, have been added to STYLE.md.
- New meaningful decisions, if any, have been logged in DECISIONS.md.
- New primitives, if any, have been added to the library.
- New analogical districts, if any, have been added to STYLE.md "Unified analogical universe" and logged in DECISIONS.md.

**Preview gates:**

- A learner unfamiliar with the topic could complete the lesson and answer the quiz correctly on first try in user testing.
- The interactive preview page renders correctly and meets all conventions in STYLE.md "Lesson preview page" section: hero contains an interactive widget, every concept has an inline visualization, technical terms are tagged on first appearance, an inline knowledge check sits at the right moment, action buttons pulse, dark mode and scroll progress work, and the page is responsive below 720px width.

## Component library — the moat

Every domain has a fixed vocabulary of primitives. Standardize on first use; reuse forever. Each primitive is an SVG fragment with documented connection points, states, and a label slot. New lessons assemble primitives — never redraw them. See `/library/primitives/{domain}/` for current inventory.

VMware primitives include: rack server (Dell PowerEdge style rear panel), TOR switch, vSwitch, VM, VMDK, vSAN component, FC switch, NIC card, HBA, datastore, patch cable.

AWS primitives include: VPC boundary, subnet, EC2 instance, security group, ALB, NLB, NAT gateway, internet gateway, S3 bucket, Lambda, RDS, route table, IAM principal, request packet.

Equivalent inventories for Azure, GCP, Kubernetes/DevOps, MLOps. When a primitive is needed that doesn't exist yet, the factory drafts it, the founder approves it, and it is added to the library before being used in the lesson.

## Tech stack

- **Content repo in Git.** Every lesson lives as a folder of files. Reviewable in pull requests, versionable, diffable.
- **SVG + HTML widgets.** Animation authored as raw SVG inside HTML, motion driven by `getPointAtLength` along an SVG `<path>`. SMIL `<animateTransform>` for continuous motion (fans, status LEDs).
- **Render pipeline.** Takes the lesson folder, produces a static site with embedded animations and a video export with synced narration. Build incrementally — start with hand-authored, add templating once patterns repeat.
- **LMS layer.** Static site (Astro or Next.js) with animations as iframes. No custom LMS for the first 6 months.

## File structure
