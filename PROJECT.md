# EdTech Content Factory — Visual-First Technical Training

## Vision

Build a content factory that produces visually-driven technical training lessons at scale. The founder uploads a topic; the factory produces a complete lesson package conforming to a fixed structure and house style. Initial domains: VMware, AWS, Azure, GCP, DevOps, MLOps. Brand promise: anyone willing to learn can understand these systems because we make hard concepts visually obvious.

The proof-of-concept is a VMware packet-flow animation: a data packet visibly travels from a VM through a vSwitch, out a NIC port on a realistic Dell PowerEdge rear panel, up a patch cable, into a specific port on a top-of-rack switch, across the switch fabric, and down to a destination VM — with encapsulation shells appearing at the right boundaries and port LEDs lighting in sequence. Mode toggles let the same animation demonstrate L2, L3, and NSX overlay variants. This is the bar for every animated lesson.

## How the factory works

The founder submits a topic at any granularity — a course (`vSphere networking`), a sub-topic (`vSphere standard switching`), or a single concept (`uplink failover with beacon probing`). The factory produces a lesson package containing all required sections (defined below), conforming to the house style (defined in STYLE.md), reusing primitives from the component library, and logging meaningful decisions to DECISIONS.md.

A lesson package is reviewable, revisable, and shippable independently. Many lessons chain into a course.

## The fixed lesson structure

Every lesson produced by the factory contains exactly these seven sections, in this order. None are optional. None are reordered. Predictability is the point.

**1. Concept explanation.** Plain definition of what the topic is, what it does, and why it exists. 150-300 words. No jargon without inline definition.

**2. Before / after comparison.** What did the world look like before this technology existed? What problem did people have? How did that problem get solved (or partially solved) by this technology? Always two columns or two paragraphs explicitly labelled. Examples: how operating systems ran before virtualization vs. after; how applications were deployed before containers vs. after; how networks were configured before SDN vs. after.

**3. Analogy.** A real-world physical metaphor that maps onto the technical concept. Letters and post offices, apartment buildings and rooms, restaurants and kitchens. The analogy is what learners remember; the technical detail layers onto it. One primary analogy per lesson — resist the urge to mix three.

**4. ELI5 and ELI10.** Two stacked explanations. ELI5 (Explain Like I'm 5) is the simplest version, using the analogy from section 3 and assuming zero prior knowledge — under 100 words. ELI10 is the practitioner-junior version, using correct technical terminology but still grounded in the analogy — 150-250 words. A reader should be able to read ELI5, understand it, then read ELI10 and feel they've leveled up.

**5. Real-world scenarios.** Three to five concrete situations where this concept applies in practice. Each scenario names the company type or use case ("a mid-size SaaS company with three regional offices"), states the problem they faced, and shows how the concept solves or partially solves it. These are the "when do I actually use this" anchors. They are not case studies — they are short, vivid, 80-150 words each.

**6. Animated SVG illustration.** A motion-graphic illustration matching the house style in STYLE.md. Mandatory for every lesson. The illustration shows the concept in motion — packet flowing, request being routed, container being scheduled, model being trained. It must conform to the visual conventions and reuse primitives from `/library/primitives/`. The packet/request motion track must trace exactly through visible components.

**7. Flashcards and quiz.** Eight to twelve flashcards (front: question or term; back: 1-3 sentence answer). Two to four pause-the-animation quiz questions that test the mental model rather than memorization ("I've stopped the packet here. What happens next, and why?"). Quiz includes correct answer and the reasoning that explains why it's correct.

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

## The nine-stage production pipeline

For each lesson, the factory walks these stages in order. Skipping any stage produces lessons that fail.

1. **Intake.** Convert the inbox submission into a structured brief.
2. **Decomposition.** If the topic is too large, split it into sub-topics and produce a lesson per sub-topic. The founder approves the split before production.
3. **Concept explanation drafting.** Section 1 of the lesson.
4. **Before/after, analogy, ELI5/ELI10 drafting.** Sections 2-4.
5. **Real-world scenarios drafting.** Section 5.
6. **Static SVG diagram.** Always before animation.
7. **Animated SVG illustration.** Section 6, building on the static diagram.
8. **Flashcards and quiz drafting.** Section 7.
9. **Assembly and self-review.** The factory checks the lesson against STYLE.md and the definition of done (below).
10. **Interactive preview rendering.** The factory builds `preview-lesson-{nn}.html` at the repo root, following the conventions in STYLE.md "Lesson preview page" section. Reference implementation: `preview-lesson-01.html`. Hand-authored for now; templatized once patterns are stable.

## Definition of done for a lesson

A lesson ships when:

- All seven sections are present and meet length/structure requirements.
- The animated illustration conforms to STYLE.md.
- The animation's motion track traces exactly through visible components.
- All terms used are either commonly understood or defined inline on first use.
- The before/after comparison is explicit, not implied.
- The analogy is consistent across ELI5 and ELI10.
- Flashcards cover the core terms; quiz questions test prediction, not recall.
- New visual conventions, if any, have been added to STYLE.md.
- New meaningful decisions, if any, have been logged in DECISIONS.md.
- A learner unfamiliar with the topic could complete the lesson and answer the quiz correctly on first try in user testing.
- The interactive preview page (`preview-lesson-{nn}.html`) renders correctly and meets all conventions in STYLE.md "Lesson preview page" section: hero contains an interactive widget, every concept has an inline visualization, technical terms are tagged on first appearance, an inline knowledge check sits at the right moment, action buttons pulse, dark mode and scroll progress work, and the page is responsive below 720px width.

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