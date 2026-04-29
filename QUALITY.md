# Quality protocol

The brand promise of this platform is that anyone willing to learn can understand these systems because we make hard concepts visually obvious. This document defines what "good enough to ship" means for every lesson section, and the protocol for hitting that bar reliably.

Mediocrity is the existential risk. The agent must treat this document as a hard gate, not a guideline.

## The drafting protocol

For every section that has a creative dimension — analogy, ELI5, ELI10, real-world scenarios, before/after framing — the agent generates at least three substantively different drafts before selecting one. "Substantively different" means different metaphors, different angles, different starting points — not minor rewordings of the same idea.

After generating drafts, the agent self-critiques each one against the criteria below, then either selects a winner with reasoning, or generates additional drafts if none of the candidates meets the bar.

The agent then revises the winner once before showing it to the founder.

The discarded drafts are not deleted. They are saved in `NOTES.md` inside the lesson folder under a section called "Drafts not chosen, with reasoning." This is for the founder's review and for future training of the factory's own taste.

## What "good" means, by section

### Analogy

A great analogy:

- **Maps structurally**, not just superficially. The relationships between parts of the analogy mirror the relationships between parts of the technical concept. A bad analogy says "a hypervisor is like a manager." A good analogy says "a hypervisor is like an apartment building's landlord — it owns the physical building, decides which apartments exist, gives each tenant the illusion of having their own private space, and manages the shared resources (water, electricity, internet) so tenants don't have to think about them."
- **Is sensory and concrete**, not abstract. The reader can see, hear, or touch the thing in their head. Apartments, post offices, kitchens, libraries, restaurants, traffic lights — these work. "A system," "a layer," "a process" — these don't.
- **Is anchored in everyday experience.** The reader has been in an apartment building. They've sent letters. They've waited in line at a coffee shop. They have not run a CNC machine or piloted a submarine. Choose anchors from common life.
- **Holds up under follow-up questions.** A learner who says "wait, so in your apartment analogy, what's the equivalent of a snapshot?" should be able to find the answer naturally — "the landlord takes a photo of every apartment's layout at midnight; if a tenant trashes their place, the landlord can restore the layout from the photo." If the analogy collapses under such questions, it's the wrong analogy.
- **Produces an "oh!" moment.** When the reader hears it, something clicks. They may not be able to articulate why, but they suddenly see the concept differently. This is the test that matters most. If the analogy doesn't produce that click, it's not the right one.

A great analogy is rare. The agent generates at least five candidates and picks the strongest one. If none of the five clicks, generate five more. Do not settle.

### ELI5

A great ELI5:

- **Uses zero jargon.** Not "reduced jargon." Zero. If a technical term must appear, replace it with a plain-language equivalent.
- **Is short.** Under 100 words. Brevity forces clarity.
- **Centers the analogy.** The ELI5 is the analogy in motion. Not "X is like Y, and also here's how X works" — just the analogy carrying the explanation.
- **Reads aloud naturally.** If you read it to a child and they look confused, it failed. The agent should mentally read it aloud and check.
- **Ends with a sentence the reader can repeat back.** "So virtualization is just letting one big computer pretend to be lots of small ones." The closing sentence is what gets remembered.

### ELI10

A great ELI10:

- **Uses correct technical vocabulary**, but defines each term inline on first use.
- **Stays grounded in the same analogy as ELI5.** The reader is leveling up, not switching frames.
- **Adds the "why" that ELI5 omitted.** Why does this technology exist? What problem does it solve that the previous approach couldn't?
- **150-250 words.** Long enough to add real content; short enough that no padding can hide.
- **Ends with the bridge to the practitioner level.** A sentence that hints at what someone with a few years of experience would worry about. "Of course, in real environments, you also have to think about how the hypervisor decides which physical resources go to which virtual machine when they all want the same thing at once — but that's the next lesson."

### Before / after

A great before/after:

- **Names the specific pain.** Not "things were harder" — "a medium-sized company would buy 200 servers, each running one application at 5% utilization, with the rest of the capacity wasted, and a refresh cycle that cost millions every three years."
- **Names the specific relief.** Not "things got better" — "the same workloads now run on 6 physical hosts, capacity is allocated dynamically as demand shifts, and adding a new application takes minutes instead of weeks."
- **Acknowledges what didn't get easier.** Honesty earns trust. "Virtualization didn't eliminate the need to plan capacity — it just shifted the planning from physical procurement to virtual resource allocation."
- **Is symmetric in length and detail.** Before and after each get the same number of sentences. Asymmetry signals one side wasn't thought about as carefully.

### Real-world scenarios

A great real-world scenario:

- **Names the company type concretely.** "A regional bank with 80 branches" beats "a financial services company." "A SaaS startup serving dental offices" beats "a software company." Specificity is credibility.
- **States the actual problem they faced.** Not "they needed virtualization" — "they were running out of rack space in their primary data center and the landlord was raising prices."
- **Shows how the concept solved it, with a number.** "By consolidating their 200 physical servers onto 12 hosts running ESXi, they freed 80% of their rack space and renegotiated their lease." Numbers make scenarios stick.
- **Mentions a complication or trade-off.** No real-world story is purely triumphant. "They did discover that their oldest application, a Windows Server 2003 box for payroll, refused to run reliably as a VM and had to stay physical." This honesty is what separates real scenarios from marketing copy.
- **Is 80-150 words.** Long enough to be vivid, short enough that you can read three of them in a minute.

### Flashcards

A great flashcard set:

- **Each card tests one concept.** No combo cards.
- **Front side is a question or a single term.** Not a multi-part prompt.
- **Back side is 1-3 sentences.** Long answers don't fit on a card and signal the question was too broad.
- **The deck collectively covers every term and concept introduced in the lesson.** No silent gaps.
- **Includes at least two cards that test understanding rather than recall.** "Why does X happen?" not just "What is X?"

### Quiz

A great quiz question:

- **Is a pause-the-animation question wherever the lesson has an animation.** "I've stopped the packet here. What happens next, and why?" forces the learner to predict from a mental model rather than recall a fact.
- **Has a single clearly correct answer**, with reasoning that explains why that answer follows from the lesson's core concept.
- **Includes a thoughtful explanation for the wrong answers**, if multiple-choice. "B is wrong because it confuses VLAN tagging with VXLAN encapsulation, which sit at different layers — see lesson 4."
- **Tests the mental model, not memorization.** "What happens if the active uplink fails while a packet is mid-flight?" beats "What does NIC teaming mean?"

## The self-critique pass

Before showing any section to the founder, the agent performs a self-critique pass. The critique is written down — not just performed silently — and saved in NOTES.md as part of the lesson record.

The critique format for each section:

- What works in this draft.
- What's mediocre or could be better.
- What would I change if I had one more revision.
- Is this good enough to ship, or does it need another draft?

If the answer to the last question is "needs another draft," the agent does the revision before showing the section to the founder. The agent does not present a section it knows is mediocre.

## The "first-time learner" test

For every lesson, the agent imagines a specific first-time learner — someone with general technical literacy but zero exposure to this specific topic — reading the lesson straight through. After producing the full lesson, the agent walks through it as that learner and asks:

- Where would I get confused?
- Where would I have to re-read a sentence?
- Where does a term get used before it's defined?
- Where does the analogy stop helping?
- Where does the lesson assume I know something I don't?

Each "yes" answer is a defect. The agent fixes them before declaring the lesson done.

## What "ship-ready" means

A lesson is ship-ready when:

- Every section meets the criteria above.
- The self-critique pass produced no remaining "needs another draft" verdicts.
- The first-time-learner test surfaced no unfixed confusion points.
- All discarded drafts are saved in NOTES.md with reasoning.
- The founder has reviewed and approved.

The agent does not present a lesson as done unless all five conditions hold.

## The discipline this requires

Generating multiple drafts and self-critiquing takes longer than producing a single draft. This is the cost of quality, and it is non-negotiable. A factory that produces 1000 mediocre lessons is worth less than a factory that produces 200 excellent ones.

If a session feels rushed, slow down. If the founder asks for more lessons faster, the answer is to hire more reviewers, not to skip the protocol. The protocol is what the brand is built on.