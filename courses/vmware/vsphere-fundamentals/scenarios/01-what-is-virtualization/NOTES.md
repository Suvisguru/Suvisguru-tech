# Production notes — Lesson 01: What is virtualization?

This file records drafts that were considered and rejected, scoring, and self-critique passes. It is the audit trail for QUALITY.md compliance.

---

## Pass 1 — Concept explanation, before/after, analogy

### 1.A Analogy: candidates considered

Per QUALITY.md, generated 8 substantively different candidates and scored each against the five analogy criteria: structural mapping, sensory/concrete, everyday-experience anchor, holds up under follow-up questions (snapshots, vMotion, HA, resource pools, consolidation ratio), "oh!" moment potential.

#### Candidate 1 — Apartment building **(SELECTED)**

Building = physical server. Apartments = VMs. Superintendent = hypervisor. Shared utilities = shared CPU / RAM / network.

- *Structural fidelity:* very high. The superintendent owns the building, decides which apartments exist, gives each tenant the illusion of private space, and manages shared resources without involving the tenant. That maps tightly to a hypervisor.
- *Sensory anchor:* every reader has been in an apartment building or seen one on screen.
- *Extends to:* snapshots ("superintendent photographs every apartment at midnight, can restore the layout"); vMotion ("tenant's entire apartment is teleported intact to a sister building"); HA ("fire forces near-instant re-housing in a sister building"); resource pools ("a floor reserved for premium tenants"); consolidation ratio ("this high-rise replaced 200 separate houses on the block").
- *"Oh!" moment:* the leap from "one family in a house" to "twenty families in a building of the same footprint" is a universal mental jump that mirrors the technical leap from "one OS on bare metal" to "many OSes on one host."

#### Candidate 2 — Hotel
*Rejected.* Strong sensory anchor but hotels imply temporary stays; VMs run for years. The ratio is also wrong — a hotel has tens of rooms, real consolidation reaches 50:1+. vMotion ("guest teleported between rooms") feels strained.

#### Candidate 3 — Co-working space
*Rejected.* Decent structural map (isolation, shared utilities, building manager). Less universally familiar than apartments — many readers have never been in one. Loses the "lots of rooms sitting idle in a single-family house" pre-virtualization image, which is essential to the before/after.

#### Candidate 4 — Office building / commercial real estate
*Rejected.* Similar map to the apartment building, but offices read as abstract / business-coded. Apartments are more emotionally vivid for a beginner with no IT background.

#### Candidate 5 — Cruise ship cabins
*Rejected.* Temporary-stay problem (cruises end). Less day-to-day familiar. vMotion as "transferring to another ship" feels strained.

#### Candidate 6 — Theater stage hosting many plays in rotation
*Rejected.* Fails on concurrency: only one play runs on a stage at a time. The whole point of virtualization is many VMs running simultaneously, not in rotation.

#### Candidate 7 — Library private study rooms
*Rejected.* Smaller scale; rooms feel like fixed physical partitions rather than dynamically allocated resources. Doesn't extend naturally to consolidation ratios or moving workloads.

#### Candidate 8 — Shared commercial kitchen
*Rejected.* Concurrency issue (kitchens are typically used in time-slot rotation). Doesn't map to "many tenants permanently in residence."

#### Why apartment building won

It is the only candidate that extends cleanly to *all* the futures the brief requires (snapshots, vMotion, HA, resource pools, consolidation ratios) without straining. Note: QUALITY.md cites apartment-building as an example of a good analogy. The candidate was selected on merits — structural mapping, durability, accessibility — not because it appears in the example. The other seven were each tested against the same criteria and lost on specific failure modes recorded above.

### 1.B Before/after: drafts considered

Generated three substantively different angles before selecting.

#### Draft A — Storytelling angle **(SELECTED)**
Opens with a sensory hook ("walk into a typical datacenter in 2000"). Specific numbers (200 servers, 5% utilization, 70% post, 6-week procurement). Symmetric structure. Names the trade-off honestly ("capacity planning didn't disappear, it shifted").

#### Draft B — Financial angle
*Rejected.* Sharp dollar framing ($15,000/server, $2-4M refresh cycle) makes magnitude vivid. But it leans heavy on numbers and loses the "you can see it" feeling that a foundational lesson needs. Better suited to a later cost-modelling lesson.

#### Draft C — Operations angle
*Rejected.* Best at conveying what life felt like for an IT admin (racking, cabling, warm-spare hardware). But the target learner has no IT-admin lens. Persona-specific framing raises the entry bar.

### 1.C Self-critique

#### Concept explanation
- *What works.* Defines virtualization, VM, and hypervisor inline. Sets up the problem and the solution at the right altitude. Keeps VMware product names out (per brief). Closes by naming virtualization as the foundation of cloud, modern storage, and SDN — orienting the learner to what comes next.
- *What's mediocre.* The third paragraph trails into a small list ("higher utilization, faster provisioning, foundation"). The list is true but reads list-y in a section meant to be neutral-authoritative prose.
- *One more revision would.* Tighten the closing sentence to a single clean payoff rather than a triplet.
- *Ship-ready?* Yes, pending founder copy-edit on the close.

#### Before / after
- *What works.* Symmetric paragraph length. Specific numbers that ground the abstraction. The "honest caveat" about capacity planning shows we're not selling.
- *What's mediocre.* "Power and cooling bills fall sharply" is generic where the rest of the paragraph is concrete.
- *One more revision would.* Replace "fall sharply" with a number — but only if the founder is comfortable with a roughly-accurate figure (e.g., "by 50–70% in early consolidation cases"). Left generic for the founder to attach the number they trust.
- *Ship-ready?* Yes, pending founder decision on the number.

#### Analogy
- *What works.* The single-family-house → apartment-building leap is the structural punch line. The superintendent does real work as a stand-in for the hypervisor (manages shared utilities, decides what each tenant gets, enforces isolation). The forward-reference paragraph (vMotion, snapshots, hypervisor) earns its place by setting up the rest of the course.
- *What's mediocre.* In cultures where apartment living is the default, "pre-virtualization = single-family house" lands less viscerally than in a US-suburban frame. This is a small regional reading.
- *One more revision would.* Possibly add a sentence acknowledging that "in some places, the building is already the default — but historically the concentration is recent." Likely adds words without adding clarity. Skipped.
- *Ship-ready?* Yes.

### 1.D First-time-learner check — Pass 1 only

Imagined learner: has used a laptop, has heard the word "server," has never thought about hypervisors.

- *Confusion?* Possibly at "the hypervisor sits between the physical hardware and the virtual machines" — "between" is spatial-metaphorical. The analogy section catches this with the superintendent framing.
- *Re-read?* Concept paragraph 2 if paragraph 1 was skimmed. Acceptable for a foundational lesson.
- *Term used before defined?* Checked. VM defined inline. Hypervisor defined inline. "Physical server" is treated as known.
- *Analogy stops helping?* Not in this pass.
- *Assumed knowledge gap?* The reader is assumed to know what an OS is. This matches the brief.

No unfixed defects in Pass 1.

---

## Pass 2 — ELI5, ELI10, real-world scenarios

### 2.A ELI5: drafts considered

Generated four candidates. Constraint: zero jargon, under 100 words, centered on the apartment-building analogy, ends with a sentence the reader can repeat back.

#### Draft A — "Imagine your computer is like a big house..." **(SELECTED, lightly revised)**
~92 words. Clean opening. Closes with "virtualization just lets one big computer pretend to be lots of small ones" — the line is short, factual, repeatable. Adjusted "building manager" → "person in charge of the building" so it reads aloud cleanly to a child and stays consistent with the "superintendent" used in §3 and ELI10 (which a 10-year-old will accept as the formal version of "the person in charge").

#### Draft B — "Picture a really big house where only one family lives..."
*Rejected.* Same idea as Draft A, slightly more energetic opening. Lost on closing-line sharpness — Draft A's repeatable line was tighter.

#### Draft C — "Imagine a magic apartment manager..."
*Rejected.* Introduced the term "hypervisor" inside ELI5, which violates the zero-jargon rule. Useful as a structural exercise, not as a final.

#### Draft D — "Pretend your computer is a big empty house..."
*Rejected.* "Magic trick" framing was charming but weakens the structural analogy — virtualization is not a trick, it is a real division of resources. The framing pulls toward whimsy instead of clarity.

### 2.B ELI10: drafts considered

Generated three candidates. Constraint: 150–250 words, correct vocabulary defined inline, same analogy as ELI5, adds the "why," ends with a bridge to a practitioner concern.

#### Draft B — "Virtualization works through a piece of software called a hypervisor..." **(SELECTED, lightly revised)**
~215 words. Defines hypervisor and VM inline. Carries the superintendent/apartment frame. Adds the "why" via the five-bedroom-with-one-person line. Bridges with the dishwasher-at-the-same-instant image into resource scheduling.

#### Draft A — "Virtualization is software — called a hypervisor —"
*Rejected.* The opening conflates virtualization (the technique) with the hypervisor (the software that implements it). Concept §1 is precise on this and ELI10 has to match. Easy to fix but Draft B was already cleaner.

#### Draft C — "Virtualization is a software layer called a hypervisor..."
*Rejected.* More precise wording at the open, but the body leaned more practitioner-direct and lost the warmth that should still be present at ELI10 level. Same warmth as ELI5 is the rule.

### 2.C Real-world scenarios: drafts considered

For each scenario, generated two angles and selected one. The four selected scenarios deliberately span four distinct value angles so the reader sees that virtualization is not a one-trick technology:

| # | Scenario | Angle |
| - | -------- | ----- |
| 1 | Regional bank | Hardware consolidation and cost. |
| 2 | State university | Sprawl, electricity, reclaimed floor space. |
| 3 | Manufacturer | Legacy preservation — keeping a 1996 OS alive. |
| 4 | SaaS company | Dev/test agility and release velocity. |

#### Scenario 1 — Regional bank

- Draft 1 (consolidation/cost) **selected.** Numbers: 220 → 14 hosts; $4.2M → $1.1M; 6 weeks → 20 minutes. Trade-off: Windows Server 2003 payroll holdout.
- Draft 2 (regulatory backups + warm-spare avoided) *rejected.* Strong but pulls into snapshot/DR territory, which is forward of this lesson's frame. Draft 1 reinforces the main consolidation thread.

#### Scenario 2 — State university

- Draft 1 (sprawl + electricity + reclaimed rooms) **selected.** Numbers: 340 → 22 hosts; $180K electricity at 60% reduction; four reclaimed rooms. Trade-off: GPU/sensor labs stay physical.
- Draft 2 (release-velocity for course websites) *rejected.* Closer in flavor to scenario 4 (SaaS dev/test). Selecting Draft 1 keeps the four scenarios distinct.

#### Scenario 3 — Manufacturer

- Draft 1 (Windows NT 4, vendor gone, 30 CNC machines) **selected, revised.** Replaced "$2.3 million ERP integration project" with "multi-year, multi-million-dollar control-system overhaul" — more accurate to the domain (CNC control is closer to MES/SCADA than ERP). Replaced "snapshot" with "save a complete copy of the entire environment ... ready to restore from" — the term snapshot has not been formally introduced as a technical term yet.
- Draft 2 (specialty steel + Windows Server 2003) *rejected.* Strong but the 1996/Windows NT 4 detail in Draft 1 lands harder for a beginner's "wait, that still exists?" reaction.

#### Scenario 4 — SaaS company

- Draft 2 (release-velocity + 800 stale VMs) **selected.** Numbers: 4 shared servers → unlimited per-developer environments; 6 weeks → 10 days; security patch same afternoon. Trade-off: 800 stale VMs accumulated — a uniquely virtualization-specific complication that you'd never see with physical hardware (you'd never have 800 forgotten physical servers). Pedagogically useful.
- Draft 1 (dental SaaS, 14 devs, gold-environment for perf bug) *rejected.* Solid, but the stale-VM complication in Draft 2 is more memorable and more uniquely-virtualization in nature.

### 2.D Self-critique

#### ELI5
- *What works.* Stays inside the apartment-building analogy. Zero technical terms. Closing line is short and repeatable.
- *What's mediocre.* "Sharing the building's water and electricity" is shorter than ELI10's equivalent — could add "and internet" for parallelism, but parallelism is less important at age-5 register than rhythm. Left as is.
- *Ship-ready?* Yes.

#### ELI10
- *What works.* Defines hypervisor and VM inline. The dishwasher-at-the-same-instant bridge image is concrete and primes the next lesson naturally.
- *What's mediocre.* "Twenty tenants all want to run the dishwasher" is a small leap from "twenty operating systems live in the same physical box" — most apartments don't have dishwashers. Acceptable image but not airtight.
- *Ship-ready?* Yes.

#### Real-world scenarios
- *What works.* Four distinct angles. Each has at least one specific number and an honest trade-off. The four together answer "where does virtualization actually matter?" from four different vantage points.
- *What's mediocre.* All four scenarios skew toward "small-to-mid US-style organization." None feature a hyperscale or cloud-provider-scale story. That is intentional for this foundational lesson — hyperscale comes in a later lesson — but worth flagging for the founder.
- *Ship-ready?* Yes.

### 2.E First-time-learner check — Pass 2

Walked through §1 → §5 in order as a learner with general computing literacy and zero virtualization exposure.

- *Confusion?* Resource scheduling is named in ELI10 but not defined. It is explicitly framed as "the next lesson," which is acceptable forward-referencing.
- *Term used before defined?* Original draft of scenario 3 used "snapshot" without prior definition. Replaced with plain-language "save a complete copy ... ready to restore from." Original draft of scenario 3 also said "ERP integration project"; replaced with "multi-year, multi-million-dollar control-system overhaul" to avoid an undefined business acronym.
- *Re-read?* Scenario 1's "mainframe-adjacent payroll application" might cause a re-read for a reader who hasn't met "mainframe." Acceptable — the meaning is recoverable from context, and the trade-off lands either way.
- *Analogy stops helping?* No. ELI10's dishwasher line is the only place where the analogy is stretched, and it stretches in the direction of the next lesson, not into confusion.
- *Continuity from Pass 1?* Verified. The "superintendent" maps consistently in §3 and §4. ELI5 uses "person in charge of the building" because "superintendent" is borderline jargon for an age-5 register; the level-up to "superintendent" happens in ELI10. That is the intended ELI5→ELI10 progression.

No unfixed defects in Pass 2.

---

## Pass 3 — Library primitives

Drafted four primitives in `/library/primitives/vmware/`, each as a self-contained .svg with documentation comments, a `<symbol>` definition for re-use, and a preview render:

- `rack-server-rear.svg` — 480 x 200 viewBox. Executes the hardware aesthetic specified in STYLE.md: light silver chassis, rack ears with screws, two PCIe slots (NIC card with two RJ45 jacks; empty slot with vent slits), center I/O cluster, dual hot-swap PSUs with rotating fans (SMIL: top 4.2s, bottom 4.5s — slight offset to avoid lockstep). Connection points documented at NIC ports for later networking lessons.
- `vm-tile.svg` — 120 x 56. Sized so 8 tiles in 2 rows of 4 fit atop a 480-wide host. Header bar (top corners rounded), OS pill, role label, mini activity bar, status dot.
- `hypervisor-layer.svg` — 480 x 30. Slate fill #3F4A5E with three thin horizontal hairlines suggesting "code layer." Label "hypervisor" centered.
- `utilization-meter.svg` — 100 x 18. Single neutral fill color #5A6B81 regardless of percentage; pedagogy carried by fill level and numeric label. Consumer overrides `.utilization-fill` width and `.utilization-label` text.

### 3.A Pending DECISIONS.md entries (move to DECISIONS.md on approval)

> Status: APPLIED. After Pass 3 approval, all four entries below were appended to `/DECISIONS.md` verbatim.


#### 2026-04-29 — Hypervisor and software-layer abstractions render as a slate band (#3F4A5E)

**Context:** Lesson 01 needs to render the hypervisor as a distinct visual element. Existing palette is allocated: networking teal/blue, storage coral/amber, encapsulation purple, failure red, healthy green, inactive gray. None of those apply to a software abstraction layer.

**Decision:** Hypervisor and similar software-layer abstractions render as a horizontal slate band with fill #3F4A5E and stroke #1F2433. Three thin horizontal hairlines (#536179 at 0.6 opacity) suggest "layer made of code." Label rendered in light text #E8E8E0, sans-serif 13px weight 500, letter-spacing 1.5px, centered horizontally.

**Reasoning:** Slate carries an "infrastructure / foundational" connotation that doesn't collide with any existing reserved color meaning. The horizontal-band shape reinforces the relationship "between hardware and VMs."

**Alternatives considered:** Reuse #2A2A2E (dark gray) — rejected, conflicts with TOR switch chassis and would cause confusion when both appear in the same frame. Reuse teal — rejected, networking-coded. Use a unique shade outside existing families — selected.

**Revisit when:** A second software-layer abstraction (e.g., guest OS visual treatment, container runtime) needs a distinct color and would conflict.

#### 2026-04-29 — Utilization meters use a single neutral fill regardless of percentage

**Context:** Lesson 01's pedagogy hinges on visualizing low (pre-virt) vs. high (post-virt) hardware utilization. Considered green/red value-encoding but it conflicts with reserved STYLE.md meanings.

**Decision:** Utilization meters use a single neutral fill #5A6B81 (a step lighter than hypervisor slate, signaling "related software-layer family") regardless of fill percentage. The pedagogical contrast is conveyed by fill *level* and the numeric label, not by color shifts.

**Reasoning:** Avoids palette collision with green=healthy, red=failure, amber=VLAN, teal=networking. More honest pedagogically — utilization isn't binary good-vs-bad; the visual contrast (mostly empty vs. mostly full) does the teaching.

**Alternatives considered:** Color-by-value (green high / red low or vice versa) — rejected, overloads existing reserved meanings. Two separate primitives for low and high utilization — rejected, breaks "primitive is canonical."

**Revisit when:** A future lesson needs to encode utilization-state risk (e.g., overcommit warning). At that point, consider an amber overlay on top of the existing fill rather than changing the base fill color.

#### 2026-04-29 — Vertical stacking convention: VMs above, hypervisor in the middle, host below

**Context:** A choice about vertical layering in any diagram or animation that shows a virtualized host. Either order is technically defensible.

**Decision:** Render order from bottom to top is host → hypervisor band → VMs. The hypervisor band always sits *between* the host and the VMs.

**Reasoning:** Matches the apartment-building analogy frame (apartments above, building underneath, superintendent in the middle managing both). Also matches the dominant industry convention for virtualization stack diagrams. Pedagogical: "between" is the relationship that the lesson teaches; the visual must reinforce it.

**Alternatives considered:** VMs at the bottom — rejected, contradicts industry convention and the analogy. Hypervisor as a side-bar — rejected, loses the "between" relationship.

**Revisit when:** Never. This is foundational.

#### 2026-04-29 — Default consolidation visual shows 8 VMs on the post-virt host

**Context:** The "after" mode of the lesson 01 animation needs to visually demonstrate consolidation. The choice is how many VMs to render on the single host.

**Decision:** Show 8 VMs in two rows of four, atop one rack-server-rear (480 wide). Each VM tile is 120 x 56 by default.

**Reasoning:** Eight is enough VMs to feel meaningfully different from the four "before" servers (creates visual contrast and the consolidation message). Few enough to render legibly without crowding. Real consolidation can reach 50:1, but the visual goal is concept communication, not maximum.

**Alternatives considered:** 4 VMs (visually too similar to before count, the contrast reads weakly). 16+ VMs (crowded; tile labels become unreadable at primitive default size).

**Revisit when:** A later lesson on consolidation ratios specifically.

### 3.B Pending STYLE.md additions (append to STYLE.md on approval)

> Status: APPLIED. After Pass 3 approval, all sub-sections below were appended to `/STYLE.md` (Hypervisor band, VM tile, Utilization meter, Vertical stacking under Visual language; rack-server-rear addendum under Hardware aesthetic).


Append to the **Visual language** section:

#### Hypervisor band
- Color: slate #3F4A5E with darker stroke #1F2433.
- Decoration: three horizontal hairlines #536179 at 0.6 opacity, suggesting "code layer."
- Label: light text #E8E8E0, sans-serif 13px weight 500, letter-spacing 1.5px, centered.
- Default dimensions: 480 x 30 (width matched to rack-server-rear chassis interior).
- Renders between host (below) and VMs (above). Never as a sidebar.

#### VM tile
- Body: rounded rect rx 5, fill #F4F4F0, stroke #5F5E5A 1.2px.
- Header bar: top 16px, top corners rounded only, fill #5F5E5A.
- Header text: white #FFFFFF, sans-serif 10px weight 500, left-aligned 8px from edge.
- OS pill: 32 x 14, rx 2, fill #A8A8AC, white 9px text.
- Role/app label: 10px #3A3A3A.
- Status dot: 2.5px radius, top-right at (110, 8). Idle #5DCAA5 opacity 0.4; active opacity 1.0; failed #E24B4A opacity 1.0.
- Default dimensions: 120 x 56.

#### Utilization meter
- Track: fill #E0E0DE, stroke #9D9D9D 0.5px, rx 2.
- Fill: single color #5A6B81 regardless of percentage. Color does *not* encode value — fill level and numeric label do.
- Label: 9px weight 500 #3A3A3A, centered.
- Default dimensions: 100 x 18.

Append to the **Hardware aesthetic** section:

- Rack-server-rear is canonicalized at viewBox 480 x 200. PSU fans rotate via SMIL animateTransform with offset durations (top 4.2s, bottom 4.5s) so they never appear locked together.
- NIC port LEDs: idle r=1.5 opacity 0.4; active r=2.2 opacity 1.0 (per existing State indicators rule).

Append to the **Vertical stacking** convention (new sub-section under Visual language):

- In any frame showing a virtualized host, the rendering order from bottom to top is: physical host → hypervisor band → VMs. The hypervisor band always sits *between*. Never reorder.

### 3.C Self-critique

#### Rack-server-rear
- *What works.* Conforms to STYLE.md hardware aesthetic. Connection points documented for downstream networking lessons. PSU fan animation gives the "powered on" cue at low cost.
- *What's mediocre.* The 4-triangle PSU fan blade is functional but not beautiful. When rotating it reads as a fan, but a still frame looks slightly cartoony. Acceptable for a primitive — beauty can come later from a 6-blade refinement if user testing flags it.
- *Ship-ready?* Yes.

#### VM tile
- *What works.* Compact enough for 2x4 stacking on a 480-wide host. Header bar gives a readable name slot. OS pill differentiates Linux/Windows/etc. without needing a per-OS icon library yet.
- *What's mediocre.* The mini activity bar inside the tile may visually compete with the host-level utilization meter. Considered removing it; kept it because per-VM activity contributes to the "all VMs are busy" message in the after-mode animation.
- *Ship-ready?* Yes, pending founder check on whether the per-VM activity bar reads as redundant.

#### Hypervisor layer
- *What works.* The slate color reads as "underneath, foundational." The hairline striping suggests "code" without being literal. The label centered with letter-spacing reads as a band rather than a button.
- *What's mediocre.* No state variation defined yet — but lesson 01 doesn't need any. Future lessons (e.g., HA failover) may need a "host failed, this hypervisor is no longer running" state.
- *Ship-ready?* Yes.

#### Utilization meter
- *What works.* Stable single-color fill removes a class of palette-collision bugs. Easy to drive with SMIL on a single rect's width attribute.
- *What's mediocre.* No tick marks (e.g., 25/50/75% gridlines). For lesson 01 the numeric label is enough; future lessons that compare multiple meters in the same frame may want gridlines.
- *Ship-ready?* Yes.

### 3.D Composition check

Verified the four primitives compose correctly for the lesson 01 animation:
- "Before" mode: 4 rack-server-rear at 1.0 scale = 4 x 480 = 1920 wide. Will need to scale to about 0.5 to fit a typical 1200 viewBox. Each gets a single VM tile and a single utilization meter on top.
- "After" mode: 1 rack-server-rear at 1.0 scale (480 wide) with hypervisor band on top (480 x 30 matches), then 2 rows of 4 vm-tile on top (4 tiles x 120 = 480 wide, matches). One larger utilization-meter on the host.

Widths align cleanly. No primitive needs resizing for lesson 01.

---

## Pass 4 — Static side-by-side diagram

`diagram.svg` drafted at viewBox 1200 × 720. Transparent background. Layout:

- Title row at y=42 (20px headings) and italic subtitle at y=64 (12px).
- Vertical dashed divider at x=600.
- **Left half (Before).** 4 rack-server-rear primitives in a 2×2 grid at scale 0.55. Each labelled with its single-app role (mail-server, payroll-db, file-share, dns-server) and its low utilization (7%, 5%, 11%, 4%). Each utilization meter is inlined (track + fill + label) rather than `<use>`-referenced because the fill width and label vary per instance.
- **Right half (After).** Single host stack at scale 0.85: 8 VM tiles in 2 rows of 4, hypervisor-layer band abutting chassis top, rack-server-rear below, host name "host-01", and an enlarged utilization meter at 72%. VM tiles are also inlined so each can carry its own VM name and role label (vm-01 mail-server through vm-08 backup-job — narratively the original 4 plus 4 new ones).
- Bottom summary panel at y=600 with two short couplets framing the message.

PSU fans on all 5 servers rotate continuously per the primitive's SMIL animation. That is the only motion in the static diagram — no workload track, no mode toggle (those come in Pass 5).

### 4.A Composition pattern decision

Two primitives are referenced via `<use href="#...">` (rack-server-rear, hypervisor-layer) because their content does not vary per instance. Two are inlined (vm-tile, utilization-meter) because their text labels and fill widths vary per instance and SVG `<symbol>` does not support parameters cleanly.

This is a composition pattern worth documenting once and reusing: re-use primitives by `<use>` when content is identical; copy the visual spec inline when content varies. The primitive file is the source of truth either way.

### 4.B Self-critique

#### What works
- The 2×2 vs single-stack visual contrast lands the consolidation message at a glance.
- The slate hypervisor band sitting between chassis and VMs reads exactly as the apartment-building analogy describes — the superintendent between the building and the apartments.
- Differential VM activity-bar fills (each VM at a different load) communicate "all of these are running real work" without any further animation.
- Reusing the same workload names from Before (mail-server, payroll-db, file-share, dns-server) inside the After VM list lets the reader trace the consolidation: "the same 4 things, plus 4 more, on one box."

#### What's mediocre
- The Before grid scale (0.55) and the After stack scale (0.85) make the visual sizes asymmetric. The Before tiles look small. Considered a 0.7/0.7 symmetric scale but it forced the After stack to either lose VMs or overflow.
- The After-side host utilization meter is rendered at effective 1.7× of the primitive default (group scale 0.85 × inner scale 2.0). It looks chunky compared to the primitive's reference dimensions. Acceptable for visual prominence but inconsistent with the Before-side meters at 0.55 effective scale.

#### One known defect — typography below STYLE.md 11px floor

STYLE.md specifies "11px minimum for any text inside the visualization." When primitives are scaled in compositions, source font sizes get multiplied by the scale, producing rendered sizes below 11px. Fixed in this draft for the most-egregious cases:

| Element | Source size | Rendered size at scale | Status |
| ------- | ----------- | ---------------------- | ------ |
| Before server names (mail-server, etc.) | bumped 14 → 22px | 12.1px @ 0.55 | OK |
| Before utilization labels (7%, etc.) | bumped 9 → 20px | 11px @ 0.55 | OK |
| Before subtitle, title, captions | source 12-20px | unscaled | OK |
| After VM name (header) | 10px primitive default | 8.5px @ 0.85 | **below 11px** |
| After VM OS pill text | 9px primitive default | 7.65px @ 0.85 | **below 11px** |
| After VM role label | 10px primitive default | 8.5px @ 0.85 | **below 11px** |
| After host-01 label | 14px | 11.9px @ 0.85 | OK |
| After host utilization label (72%) | 9px | 15.3px @ effective 1.7 | OK |
| Hardware sub-component labels (PSU 1, I/O, NIC, empty PCIe) | 8-10px primitive default | 4.4-8.5px in compositions | **below 11px** |

The After VM tiles render slightly small text (8.5px for names and roles). Readable on a desktop monitor at full canvas; not readable on a thumbnail. Hardware sub-component labels render very small (4-8px) when scaled in compositions; they were already borderline in the primitive at 1× scale.

Three options to resolve:

(a) **Accept and ship as-is.** Defensible for the After VMs (still legible at full size). Less defensible for hardware sub-component labels.

(b) **Bump primitive text sizes.** Update vm-tile (header 10→13, OS 9→13, role 10→13) and rack-server-rear (PSU/I/O labels 8→11). Requires bumping VM tile dimensions (120×56 → 120×64) to fit larger text, which cascades to "after" stack height. This is a Pass 3 amendment.

(c) **Update STYLE.md** with a clarification: "11px applies to primary content text (component labels, body text). Structural sub-component labels inside hardware primitives (PSU, I/O cluster, NIC card markings) may render below 11px because they are decorative texture conveying type-of-thing, not primary information."

Recommendation: (a) for ship-now plus (c) for the STYLE.md clarification. The After VM names/roles are big enough at canvas size; the hardware sub-component labels are decorative chrome. A future iteration can revisit if user testing flags actual confusion.

#### One open question — VM tile diversity

All 8 VMs in the After stack render with the same OS pill ("linux"). Realistic but visually monotonous. Considered mixing in 2-3 "windows" pills for diversity. Did not, because: (1) lesson 01's message is consolidation, not heterogeneity, and (2) introducing a "windows" OS pill suggests OS variety is the point, which is forward-of-this-lesson.

### 4.C First-time-learner check — Pass 4

Imagined learner: read sections 1-5 of lesson.md, now sees `diagram.svg`.

- *Confusion?* The hypervisor band's slate color is new and undefined visually. The label "hypervisor" is on the band itself — meaning it should be self-explanatory by reading. Acceptable.
- *Re-read?* Possibly the reader looks at the After stack and asks "are those 8 VMs a sample, or specifically those workloads?" The lesson text doesn't enumerate 8 specific workloads. The VM labels (mail-server, payroll-db, etc.) link back to the Before grid, which is intentional — they should produce the "oh, those are the same things, now combined" reaction.
- *Term used before defined?* "Hypervisor" is defined in lesson.md §1, §3, §4. The diagram uses it without redefining — correct.
- *Does the visual support the analogy?* Yes. The 4 single-family-houses on the left vs. one apartment-building-with-superintendent-and-apartments on the right is exactly the analogy section's framing.
- *Net.* No defects beyond the known typography concern above.

---

## Pass 5 — Animated illustration

`animation.html` written. Self-contained HTML wrapper around an SVG with two top-level mode groups (`<g class="mode-before">` and `<g class="mode-after">`) toggled via a CSS class on the SVG element.

### 5.A Architecture choices

- **Mode toggle.** Both modes coexist in the SVG; CSS hides the inactive one. JS button click swaps which class (`show-before` or `show-after`) is applied. This avoids re-rendering on toggle.
- **Workload motion.** SMIL `<animate>` on rect width attributes drives all bouncing. Each utilization meter and activity bar has its own `dur` value (between 6s and 15s) so the system never visually "locks" in unison.
- **Pause and speed control.** SMIL doesn't natively support pause or speed scaling, so the script pauses SMIL's natural clock (`pauseAnimations()`) and drives the apparent time forward in a `requestAnimationFrame` loop, advancing by `dt × speed` per frame. Pause toggles the loop's advancement; speed slider scales it. This is the standard SMIL-with-controls pattern.
- **Mode reset.** Switching modes resets the clock to 0 so the new mode's animations start fresh, not mid-cycle.
- **Stage labels.** Update on mode toggle, not within a cycle. Lesson 01 has no packet-flow path to trigger sub-stage transitions; mode-tied labels match the workload-visualization shape of this lesson.

### 5.B Motion design

Per-server utilization (Before mode):

| Server | Baseline | Range | Period |
| ------ | -------- | ----- | ------ |
| mail-server | ~7% | 4–9% | 9s |
| payroll-db | ~5% | 3–7% | 11s |
| file-share | ~11% | 8–14% | 10s |
| dns-server | ~4% | 2–7% | 13s |

Per-VM activity (After mode), each VM's bar bounces in a workload-typical range:

| VM | Workload | Range | Period |
| -- | -------- | ----- | ------ |
| vm-01 | mail-server | 38–48 (of 80) | 8s |
| vm-02 | payroll-db | 52–68 | 9s |
| vm-03 | file-share | 38–58 | 11s |
| vm-04 | dns-server | 24–36 | 13s |
| vm-05 | web-app | 58–78 | 7s |
| vm-06 | staging-db | 32–48 | 12s |
| vm-07 | monitoring | 52–62 | 6s |
| vm-08 | backup-job | 36–88 (spiky) | 15s |

Host utilization (After mode): bounces 65–78%, baseline ~72%, period 10s. This is the dominant visual element on the After side — the meter is rendered 280 wide (≈ 2.8× a per-server meter) with the percentage label to the right of the track.

VM status dots pulse opacity 0.4–1.0 with periods 2–5s — communicates "VMs are alive and processing" without being noisy.

PSU fans (4 in Before, 1 in After) rotate continuously per the rack-server-rear primitive.

### 5.C Self-critique

#### What works
- Pause / play / speed all function as expected via the SMIL-clock-driven-by-rAF pattern.
- Mode toggle is clear; resetting the clock on toggle prevents mid-cycle visual confusion.
- Per-VM activity diversity (different bouncing ranges and periods) communicates "all of these are doing real work" without needing colors or extra UI.
- The host utilization meter sized 2.8× per-server meter immediately reads as "the headline metric."
- Backup-job's spike (38–88) is visually striking and pedagogically useful — a real "spike" you'd expect from a backup workload.

#### What's mediocre
- Before-mode utilization bars are very narrow (4–14px wide on a 100-wide track). The bouncing is real but visually subtle; you have to look closely to see they're animating. Could exaggerate the bouncing ranges for more drama, but that would lie about real-world utilization.
- All 8 VMs show the same OS pill ("linux"). Visually monotonous, but matches the Pass 4 decision to defer OS heterogeneity to a later lesson.
- No explicit consolidation-ratio overlay (e.g., "4 servers → 1 host"). The information is implicit in the mode contrast. A small badge could make it explicit but adds chrome.

#### One known limitation — SMIL browser support
SMIL is supported in Chrome, Firefox, Safari, Edge. It is *not* supported in old IE (irrelevant) and there were rumors of deprecation in Chrome that did not materialize. Modern browsers handle this fine. Flagging only because the lesson relies on SMIL for all motion.

#### Speed-control caveat
The SMIL-clock-driven-by-rAF pattern works in modern browsers but has one quirk: SMIL animations defined with `begin="indefinite"` do not start unless explicitly triggered. Our animations use the implicit `begin="0s"` which works with the manual clock. Not a defect for this lesson, but worth remembering for animations that need event-driven triggers.

### 5.D First-time-learner check — Pass 5

Imagined learner: read sections 1–5 of lesson.md, viewed `diagram.svg`, now opens `animation.html`.

- *Confusion?* The default mode is "Before." A learner unfamiliar with the buttons might not realize "After" exists. Mitigation: the two mode buttons are prominent at the top, labelled in plain language. Acceptable.
- *Re-read?* The After-side host utilization label is now to the right of the bar (was on top, fixed mid-pass). Reads cleanly.
- *Term used before defined?* No new terms in the animation that haven't been defined in lesson.md.
- *Visual lands the lesson's claim?* Yes. The Before mode shows mostly-empty bars; the After mode shows a single mostly-full bar with eight active VMs. The contrast is the lesson.
- *Pause / speed work?* Yes — verifiable by clicking. Pause freezes all motion (including PSU fans). Speed slider scales everything proportionally.
- *Net.* No unfixed defects.

---

## Pass 6 — Flashcards, quiz, and ship-readiness review

### 6.A Flashcards

Drafted 10 flashcards in `flashcards.yaml`. Coverage map:

| # | Concept tested | Type |
| - | -------------- | ---- |
| 1 | Virtualization definition | recall |
| 2 | VM definition | recall |
| 3 | Hypervisor (technical) | recall |
| 4 | Hypervisor mapped onto analogy | recall + mapping |
| 5 | Physical server vs VM | comparison |
| 6 | Why consolidation works | understanding |
| 7 | What virtualization did NOT solve | understanding |
| 8 | Map analogy back to concept | understanding (reverse direction) |
| 9 | Isolation: why one VM can't crash others | understanding |
| 10 | What happens without a hypervisor | understanding |

Four cards (6, 7, 9, 10) test understanding rather than recall — exceeds QUALITY.md's "at least two" floor. Card 8 reverses the direction of card 4 (concept → analogy vs. analogy → concept), which probes deeper retention than either alone.

### 6.B Quiz

Drafted 3 pause-the-animation questions in `quiz.yaml`. Each is bound to a specific mode and visual moment:

- **Q1 (After).** Why is the host meter at 72% when no individual VM is at 72%? Tests aggregation — the conceptual heart of consolidation.
- **Q2 (Before).** What would the company do for a fifth application, and what would the new server's utilization look like? Tests prediction from the visible Before-mode pattern.
- **Q3 (After).** What would happen to the 8 VMs if the hypervisor disappeared? Answer in terms of the analogy. Tests the role of the hypervisor *via* the analogy frame.

All three test mental model formation, not recall. Each has a single defensible answer with reasoning.

### 6.C Lesson-wide self-critique against the definition of done

Walking the PROJECT.md / QUALITY.md ship gates:

| Criterion | Status | Notes |
| --------- | ------ | ----- |
| All seven sections present and meet length/structure requirements | PASS | §1 ~230 words, §2 110+110, §3 ~265, §4 ELI5 ~92 + ELI10 ~215, §5 four scenarios at 125-150 each, §6 animation reference, §7 flashcards/quiz reference. |
| Animated illustration conforms to STYLE.md | PASS | Transparent background; sentence case; two type weights; reserved colors used as specified; PSU fans rotate; pause/play and speed (0.3-2×); stage label updates on mode toggle. |
| Animation's motion track traces exactly through visible components | N/A | This is a workload-visualization lesson (utilization bouncing), not a packet/flow lesson. The "motion track" rule applies to flows; here the motion is on rect width attributes for activity bars, which by definition stay inside the components. |
| All terms commonly understood or defined inline on first use | PASS | virtualization (defined §1), VM (defined §1 inline + §4 expanded), hypervisor (defined §1 + §3 by analogy + §4 with vocabulary), physical server (treated as known per brief). Scenario 3 originally used "snapshot" without prior definition; replaced with plain language. Scenario 3 originally used "ERP" without gloss; replaced. |
| Before/after comparison explicit, not implied | PASS | §2 has explicit "Before" / "After" headings and symmetric paragraph structure. The animation makes the comparison interactive. |
| Analogy consistent across ELI5 and ELI10 | PASS | Both use the apartment-building frame. ELI5 uses "person in charge of the building"; ELI10 levels up to "superintendent" — same role, age-appropriate vocabulary. |
| Flashcards cover the core terms | PASS | 10 cards covering every term and concept. |
| Quiz tests prediction, not memorization | PASS | All 3 questions are pause-the-animation prediction prompts. |
| New visual conventions added to STYLE.md | PASS | Hypervisor band, VM tile, Utilization meter, Vertical stacking convention, rack-server-rear PSU-fan timing, typography exemption — all appended to STYLE.md. |
| New meaningful decisions logged in DECISIONS.md | PASS | Five entries appended: hypervisor color, utilization meter neutral fill, vertical stacking, default 8 VMs in consolidation visual, hardware sub-component label exemption. |
| Learner unfamiliar with topic could complete the lesson and answer quiz on first try in user testing | PENDING | Requires actual user testing — flagged for the founder. |

### 6.D Lesson-wide first-time-learner walkthrough

Imagined learner: general computing literacy, has heard the word "server" but never managed one, no exposure to virtualization. Reads §1 → §7, then opens `animation.html`, then attempts the quiz cold.

- *§1 Concept.* Defines V, VM, and hypervisor inline. Lands.
- *§2 Before/after.* Specific numbers ground the abstraction. The honest caveat about capacity planning earns trust.
- *§3 Analogy.* The single-family-house → apartment-building leap is intuitive. The forward-references to vMotion and snapshots are labelled as future-lessons; they don't confuse.
- *§4 ELI5.* Zero jargon, repeatable closing line. Reads aloud naturally.
- *§4 ELI10.* Defines hypervisor and VM inline. The dishwasher bridge to the next lesson is concrete.
- *§5 Scenarios.* Four distinct angles. Each has a number and a complication. The manufacturer scenario (Windows NT 4 from 1996) has high "wait, that still exists?" engagement value.
- *§6 Animation.* Default opens in Before. Mode toggle is clear. Pause/speed work. The 4-vs-8 contrast lands. The host meter bouncing around 72% next to per-VM bars at 30-80% communicates "many partial loads add up."
- *§7 Flashcards / quiz.* Cards that ask "in the analogy, what is X?" reinforce the analogy mapping. Quiz Q1 (the 72% question) is the hardest and the most diagnostic — a learner who answers it correctly has internalized consolidation.

Net: no unfixed defects. Ready for founder review and (when the founder chooses) user testing.

### 6.E Items deliberately deferred

These are *not* defects — they are scoped-out by the brief or by Pass-3/Pass-4 decisions:

- VM heterogeneity (mixing Linux and Windows tiles).
- Explicit "4 → 1" consolidation badge.
- More dramatic Before-mode utilization bouncing ranges.
- Larger primitive text sizes (current sizes covered by STYLE.md exemptions).
- Stage labels that update mid-cycle (no flow-track in this lesson).
- Hyperscale / cloud-provider real-world scenarios (deferred to a later lesson).

Each is logged here so the founder can flag any for follow-up before ship.
