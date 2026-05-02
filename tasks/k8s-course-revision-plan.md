# Kubernetes Course Revision — Implementation Plan for Claude Code

> **Audience for this brief:** Claude Code (or equivalent agent) executing edits on the course's HTML files.
> **Audience for the course itself:** absolute beginners with zero infrastructure background.
> **Goal:** lift the course from "well-researched intro" to "the Kubernetes course laymen actually finish" — without rewriting it.

---

## 0. Context

The course consists of 15 standalone HTML lessons (a 16th and 17th are planned but out of scope here). Each lesson is one self-contained page with a consistent layout: header, intro paragraph, multiple numbered sections (Concept, Before & After, Analogy, Two-level explanation, Real-world scenarios, Animation, Flashcards & Quiz), a glossary panel, and a footer. The CSS/visual language is already established and high quality — **do not redesign it**. All new components must adopt the existing class system, colour tokens, spacing scale, typography, and dark-mode behaviour.

The work in this plan is divided into six phases. Phases 1–4 set up the scaffolding and shared components; Phase 5 applies them to each lesson; Phase 6 verifies. **Do them in order.** A change to the shared component template late in the run is much cheaper than retrofitting 15 lessons.

---

## 1. Files

```
preview-kubernetes-lesson-01.html   ← What is Kubernetes?
preview-kubernetes-lesson-02.html   ← VMs vs Containers
preview-kubernetes-lesson-03.html   ← Cloud-Native Principles
preview-kubernetes-lesson-04.html   ← 12-Factor + Microservices vs Monoliths
preview-kubernetes-lesson-05.html   ← When K8s Fits / Overkill
preview-kubernetes-lesson-06.html   ← GitOps · Platform Eng · SRE · Multi-Tenancy
preview-kubernetes-lesson-07.html   ← History · CNCF · Releases · KEPs · Feature Gates
preview-kubernetes-lesson-08.html   ← Linux Namespaces · cgroups · Capabilities
preview-kubernetes-lesson-09.html   ← Container Runtimes & OCI
preview-kubernetes-lesson-10.html   ← Image Building · Multi-stage · Distroless · SBOM
preview-kubernetes-lesson-11.html   ← Container Security & Registries
preview-kubernetes-lesson-12.html   ← PID 1 & Container Lifecycle
preview-kubernetes-lesson-13.html   ← Cluster Architecture
preview-kubernetes-lesson-14.html   ← The K8s API & YAML
preview-kubernetes-lesson-15.html   ← Pods Deep Dive
```

A draft file (`preview-kubernetes-lesson-03-draft.html`) exists and may be ignored unless explicitly asked.

A new file will be created during this work:

```
preview-kubernetes-lesson-7-5.html   ← NEW · "Level 0 Primer" before Module 2
```

---

## 2. Execution Order

| Phase | What | Why first |
|---|---|---|
| 0 | Discovery — read 2–3 lessons end-to-end | Understand existing CSS classes, design tokens, HTML structure before touching anything |
| 1 | Accuracy fixes (4 small edits) | High confidence, low risk, builds momentum |
| 2 | Build cross-cutting component templates | Need these before they can be applied lesson-by-lesson |
| 3 | Vocabulary canonicalization pass | Easier as a global find-and-verify before content edits |
| 4 | K-Town unified universe — pick names, write the cross-lesson "cast" intro | One naming decision, applied everywhere |
| 5 | Per-lesson application (the bulk of the work) | Apply scaffolding + lesson-specific edits |
| 6 | Verification pass | Catch drift |

---

## 3. Phase 0 — Discovery (do not skip)

Before any edits, read end-to-end:

1. `preview-kubernetes-lesson-01.html` — establishes the visual baseline.
2. `preview-kubernetes-lesson-08.html` — densest technical content; tests the limits of the design system.
3. `preview-kubernetes-lesson-13.html` — heavy on diagrams; shows how the layout handles complexity.

While reading, **inventory** (write a short note to yourself or to the user):

- Existing CSS class names for: panels/cards, callouts, accent colours, dark-mode variables, the section header pattern, the flashcard component, the quiz/Q&A component, the glossary, the lesson breadcrumb, and the footer.
- The HTML pattern for "Section N · Title" headings.
- The CSS variables in use (colours, spacing, font sizes).
- Whether there's a shared `<style>` per file or external stylesheet.

You'll reuse these in Phase 2. **All new components must visually match. If a colour or spacing decision is needed, use existing tokens — do not invent new ones.**

---

## 4. Phase 1 — Accuracy Fixes

Four small edits. Do these first as warm-up.

### 4.1 Unify the seccomp syscall count

The course currently contradicts itself:

- **Lesson 08** says the default seccomp profile blocks "**~70** most-dangerous syscalls (out of ~300 total)."
- **Lesson 11** says it blocks "**~50** dangerous syscalls."

Both numbers appear in body text *and* flashcards. The actual count varies by runtime version (containerd's `RuntimeDefault` is roughly 40–65 syscalls depending on architecture and version).

**Action:** Pick one canonical phrasing and apply it everywhere it appears in Lessons 08 and 11. Use:

> "blocks roughly 40–65 dangerous syscalls (varies by runtime version) out of ~300 total"

Edit body prose, the tile description ("seccomp · syscall whitelist"), the flashcard, the glossary, and any quiz answer that mentions a specific number.

### 4.2 Fix the InPlacePodVerticalScaling example in Lesson 07

The current "Platform team's 'GA only in prod' rule" panel claims a team got burned because **InPlacePodVerticalScaling changed shape during beta between K8s 1.27 and 1.28**. Factually wrong: that feature was **alpha** in 1.27 and 1.28, not beta (it didn't reach beta until ~1.33).

**Action:** Replace the example with one of these (pick one):

- **Gateway API** pre-GA churn — multiple shape changes during beta in 2022–2023 before v1.0 GA in October 2023.
- **PodDisruptionBudget** beta-to-GA renames — simpler and uncontroversial.

Suggested replacement text (drop-in for the existing scenario block):

> A platform team standardised on "we ship workloads against GA APIs only; beta features are evaluated case by case; alpha is dev-only." This rule meant they were never burned by Gateway API's beta-period field renames (v1beta1 → v1) — they waited an extra year and got the GA contract. Their next-door neighbour team made the opposite call (run alpha aggressively for early features) and spent two on-call weeks rebuilding workloads when an alpha API was renamed in a minor release.

### 4.3 Resolve the apartment-metaphor collision (Lessons 02 ↔ 15)

Lesson 02 says: "**Each apartment = one container.**"
Lesson 15 says: "**Apartment = Pod**, roommates = containers."

This will confuse beginners as soon as they reach Module 3.

**Action:** Edit **Lesson 15 only**. Replace the Pod analogy frame so Pod is *not* an "apartment." Use **"shared studio loft"** or **"co-living unit"** consistently throughout Lesson 15 — analogy section, ELI5/ELI10, glossary, headers, mapping table, animation captions. Lesson 02 stays untouched.

In the Lesson 15 mapping table, replace `Apartment = Pod` with:

```
• Co-living unit (one address, shared kitchen) = Pod
• Roommates = containers in the pod
• Shared kitchen = network namespace (talk via localhost)
• Shared bathroom = IPC namespace
• Each roommate's bedroom = filesystem & PID namespaces (per container)
```

The H1 panel should also change `POD = ONE APARTMENT` → `POD = ONE CO-LIVING UNIT`.

### 4.4 Add a GKE/AKS pricing footnote (Lesson 13)

The "Managed CP (GKE) saved a startup from etcd backup nightmares" panel asserts "GKE control plane is ~$73/cluster/month." That's correct for GKE Standard but not for AKS (free) or GKE Autopilot (different pricing model).

**Action:** Add a one-line footnote-style annotation under the scenario:

> *Pricing as of 2024: GKE Standard ~$73/cluster/mo; AKS free; EKS $73/mo; GKE Autopilot bills per-pod. Check your provider's current pricing — the conclusion (managed beats self-managed at this team size) doesn't change.*

Use whatever footnote/aside style already exists in the course.

---

## 5. Phase 2 — Cross-Cutting Components

Build these as reusable HTML/CSS templates **once**. They will be applied to every lesson in Phase 5. Each component must inherit existing colour tokens and spacing — don't introduce new ones unless absolutely required.

For each component below, the spec gives:

- **Where it goes** in lesson structure
- **What it contains** (slots / variables)
- **Visual notes** (callout colour, icon, etc., using existing tokens)
- **Example** drawn from a lesson the user can verify against

After building each component template, save it to a new comment block at the top of `preview-kubernetes-lesson-01.html` so all 15 lessons can reference the same reusable HTML markup. Or keep templates in a separate scratch file — your call.

### 5.1 Component: `nightmare-box` — the "3 AM Nightmare" opener

**Where:** First element below the `<h1>` of every lesson, *before* the existing intro paragraph.

**What it contains:**
- Header label: "🚨 The 3 AM Nightmare"
- 2–3 sentence scenario in second person ("It's 3 AM. You wake up to…")
- A closing line that anchors the lesson: "This lesson is about why that happens, and the [N-line] fix that prevents it."

**Visual notes:** Use a warm/amber accent (existing warning token). Slightly distinct from the regular section panels — this is the *grabber*. Should feel a touch dramatic but not garish.

**Example (Lesson 12):**

> 🚨 **The 3 AM Nightmare**
> It's 3 AM. Your deploy went out clean. But somehow 4% of customer orders vanished mid-checkout, and your logs just say "Killed". By morning you have 47 angry support tickets and no idea which pods got hit. This lesson is about why that happens — and the one line of YAML that prevents it.

Per-lesson Nightmare scripts are listed in §8.

### 5.2 Component: `one-sentence-stamp` — the bolded takeaway

**Where:** Two places — once just under the Nightmare box (at the top), once at the very bottom just above the "Lesson complete" closer.

**What it contains:** Exactly one sentence. The irreducible takeaway of the lesson. No qualifications, no parenthetical jargon.

**Visual notes:** Distinct visual treatment — boxed with a strong border colour from the accent palette, slightly larger font than body, centered text. The same style for both placements (top and bottom).

**Example (Lesson 03):**

> **🎯 If you remember nothing else: Kubernetes is a thermostat. You set what you want; it watches forever; gaps close automatically.**

Per-lesson stamps are listed in §8.

### 5.3 Component: `translation-legend` — story → tech mapping

**Where:** Inside the Analogy section (Section 3), *after* the prose narrative and *before* the existing "The mapping:" bullet list. Most lessons already have a "The mapping:" block — this component reframes and standardises it as the explicit bridge between the story and the jargon.

**What it contains:** A two-column table:

| In the story… | …in Kubernetes |
|---|---|
| The captain on the bridge | PID 1 |
| The lighthouse | the kubelet |
| The lighthouse signal | SIGTERM |
| (etc.) |  |

**Visual notes:** Same visual weight as a mapping panel. Clear vertical rule between columns. Each row should *click* — left side reads as story; right side reads as tech.

**Why it matters:** Right now lessons interleave story and jargon in the same sentence ("The captain (PID 1) hears the lighthouse (kubelet)"). That triggers impostor syndrome in beginners. Separating them — story first as a narrative, then a clean translation table, then technical body using the tech terms — gives the brain time to lock the story in before vocabulary load arrives.

**Action in Phase 5:** For every lesson, take the existing prose analogy and the "The mapping:" bullet list, and convert the bullet list into this table format. The prose stays as is.

### 5.4 Component: `misconceptions-panel` — common beginner traps

**Where:** New section inserted between **Section 6 (Animation)** and **Section 7 (Flashcards & quiz)**. Number it Section 6.5 or rename Section 7 → Section 8 if cleaner.

**What it contains:** Header "Common Misconceptions", followed by exactly 3 entries per lesson, each in this shape:

> **Myth:** A container has its own operating system.
> **Truth:** It shares the host's kernel. The "OS-like" feel comes from a private view of files and processes — not a real second OS.

**Visual notes:** Each entry is a small card. Myth row has a red/strike accent; truth row has a green/check accent. Compact — three of these should fit comfortably on one screen.

Per-lesson misconceptions are listed in §8.

### 5.5 Component: `analogy-stops-here` — inline callout

**Where:** Inline within the Analogy section, immediately after the analogy is fully introduced. Used **only when the analogy has a known cliff** — i.e., a place beginners predictably overextend it.

**What it contains:** Single sentence starting with the warning icon.

**Visual notes:** A small `⚠️` callout — yellow accent — same width as a body paragraph, narrower than full-section panels. Subtle, not loud.

**Examples:**

- Lesson 02: ⚠️ *The analogy stops here: unlike apartments, you can run thousands of containers on one computer. The plumbing doesn't get clogged.*
- Lesson 03: ⚠️ *The analogy stops here: a real thermostat only watches temperature. Kubernetes runs many thermostats at once — one per type of resource (Deployments, Services, Jobs…), all running in parallel.*
- Lesson 06: ⚠️ *The analogy stops here: the GitOps controller doesn't argue with you. If the catalog says "shelve it under N", it shelves it under N — even if a human walked by and put the book somewhere "more sensible."*

Per-lesson cliff callouts are noted in §8 where they apply (not every lesson needs one).

### 5.6 Component: `skip-if-new` — depth marker

**Where:** Tag on paragraphs or sub-sections that are correct and useful but unnecessary for absolute beginners. Examples: cgroup v1 vs v2 (Lesson 08), hydrophone vs sonobuoy (Lesson 07), Raft consensus internals (Lesson 13).

**What it contains:** Small inline pill at the start of the paragraph: `[ deep dive — skip if new ]`.

**Visual notes:** Muted/grey pill. Reduces the visual weight of the paragraph slightly so a beginner's eye glides past it.

**Action:** When applying lesson-by-lesson, identify 1–3 paragraphs per Module-2/Module-3 lesson that should carry this tag. Don't tag intro lessons (01–05); the goal there is full engagement.

### 5.7 Component: `pause-and-check` — mid-lesson comprehension micro-quiz

**Where:** Two per lesson — one inserted between Section 1 and Section 2, one between Section 4 and Section 5.

**What it contains:** A single multiple-choice question (2–3 options), inline reveal of the correct answer with a one-sentence "why."

**Visual notes:** Smaller, lighter than the end-of-lesson quiz. Header reads "⏸ Pause and check." Designed to be quick — no longer than 30 seconds of reader time.

**Why:** All quizzes currently come at the end. By that time a struggling reader has consumed 1,500 words with no comprehension check. These mid-lesson stops catch confusion early.

**Example (Lesson 03, after Section 1):**

> **⏸ Pause and check:** You write a YAML file saying "I want 3 copies of my app." A server crashes. What does Kubernetes do?
>
> a) Sends an email asking what to do
> b) Notices the gap and starts a 3rd copy on a different server
> c) Updates the YAML file
>
> *Answer: **b**. The controller is constantly reading what you said you wanted (3 copies) and what's actually running (now 2 after the crash). It closes the gap by starting a replacement. You stay asleep.*

Per-lesson pause-and-check questions are listed in §8.

### 5.8 Component: `concept-rail` — persistent left-rail progress map

**Where:** Floating left rail, visible on every lesson, fixed-position so it stays as the reader scrolls.

**What it contains:** A vertical list of 17 concept-mastery items (one per lesson), with three states:
- **✓ green** — completed
- **▶ yellow** — current lesson
- **○ grey** — future

The labels should describe **concepts mastered**, not lesson titles:

```
✓ what Kubernetes is              (L01)
✓ containers vs VMs               (L02)
✓ the reconciliation loop         (L03)
✓ how apps should be designed     (L04)
✓ when K8s makes sense            (L05)
✓ how mature teams operate it     (L06)
✓ how the project evolves         (L07)
▶ how containers actually work    (L08) ← you are here
○ runtimes & the OCI standard     (L09)
○ how images are built            (L10)
○ container security              (L11)
○ how containers shut down        (L12)
○ cluster architecture            (L13)
○ K8s API & YAML                  (L14)
○ Pods deep dive                  (L15)
○ workload controllers            (L16)
○ services & networking           (L17)
```

**Visual notes:** Narrow rail (~180–220px). Collapsible on mobile. Use existing colour tokens (accent for current, dim for future). Each item is just text + status icon — no boxes/panels.

**Implementation note:** Each lesson's rail is hard-coded with that lesson highlighted as current. No state persistence needed — the rail reflects "this lesson's position in the journey," not actual user progress.

### 5.9 NEW FILE: `preview-kubernetes-lesson-7-5.html` — Level 0 Primer

A short interstitial lesson that sits between Lesson 07 and Lesson 08. Reason: Module 2 (Lessons 08–12) silently assumes the reader knows what a process is, what an OS is, what a kernel is, and what root means. Most laymen won't.

**Title:** "Lesson 7.5 — How a Linux Computer Works in 5 Minutes"

**Subtitle:** "A quick primer before Module 2. Skip if you already know what a kernel is."

**Length:** 5 short sections. No quiz, no flashcards, no animation. Plain prose with one diagram.

**Sections:**

1. **What a computer actually does.** It runs *programs*. A running program is called a *process*. Your laptop right now has hundreds of them — your browser, the clock, the wifi, the music app.
2. **What an operating system is.** Software that decides which process gets the CPU, the memory, and the disk, when. The traffic cop. Linux, macOS, Windows are operating systems.
3. **What the kernel is.** The OS's heart. The part that talks to the actual hardware (CPU, RAM, network card). When a program wants something from the hardware, it asks the kernel. That ask is called a *system call* (or *syscall*).
4. **What "root" means.** The administrator account on a Linux machine. Root can do anything — read any file, change any setting, install anything. By default, *most programs should NOT run as root.*
5. **Why this matters for containers.** A container is a program (a process) that the kernel has been tricked into thinking it's alone on the machine. Module 2 is about how that trick works.

**Visual:** One simple diagram — Hardware → Kernel → OS → Processes — with each layer labelled.

**Style:** Match Lesson 01's tone exactly. No jargon beyond what's defined in the lesson itself. Short paragraphs.

**Footer link:** "Ready for Module 2? → Lesson 08."

**Cross-link from Lesson 08:** Add a small banner at the top of Lesson 08:

> *New to Linux? Take a 5-minute detour through [Lesson 7.5 — How a Linux Computer Works](preview-kubernetes-lesson-7-5.html) first.*

### 5.10 Component: `cyoa-quiz` — Choose-Your-Own-Adventure quiz item

**Where:** Replaces ONE of the three existing end-of-lesson scenario questions in Section 7. The other two stay factual.

**What it contains:** A scenario framed as a story decision, with a "click to see what happens" reveal that includes a tiny ASCII/text graphic for the failure case.

**Visual notes:** Light playful styling. Optional emoji. The reveal can be longer than other quiz answers — this is the *memorable* one.

**Example (Lesson 12):**

> **🎬 Choose Your Own Adventure**
> You hire a rookie captain (`bash`) for your container ship. The lighthouse blinks SIGTERM. The captain… does nothing. He didn't think it applied to him. **Click to see what happens to the crew. ▼**
>
> *Reveal:*
>
> ```
>   harbour clock: 0s     ⏰ ───── 30s ──── 💀
>   crew status:    [loading cargo] → [still loading] → [SIGKILL]
>   passengers:     ████████████████████ 47% lost
> ```
>
> The harbour waited the full 30-second grace period, then pulled the gangway with `SIGKILL`. The crew never got the message and were still loading cargo when the lights went out. Half the orders dropped. Fix: hire `tini` as your captain — he forwards every signal he receives, on time, every time.

Per-lesson CYOA scenarios are listed in §8.

---

## 6. Phase 3 — Vocabulary Canonicalization

Run a global pass to unify drifting synonyms. The course currently uses multiple phrases for the same concept, sometimes within a single lesson.

**Canonical terms (use these; don't drift):**

| Canonical | Acceptable as first-mention gloss only | Avoid |
|---|---|---|
| **desired state** | "what you want" *(parenthetical only, on first mention per lesson)* | "the spec", "your declared intent", "what you said" — when used as a standalone term |
| **actual state** | "what's running" *(parenthetical only)* | "current state", "live state", "reality" |
| **controller** | "the small program watching forever" *(parenthetical only)* | "the loop", "the reconciler" — as the standalone term |
| **reconciliation loop** | "the loop" *(after first mention in a lesson)* | "the reconcile cycle", "the watch loop" |
| **Pod** *(capitalised)* | — | "pod" (lowercase) when referring to the K8s object |
| **the kubelet** | "the node agent" *(parenthetical, first mention only)* | "the agent" — ambiguous |
| **the API server** | "the only door in" *(parenthetical, first mention only)* | "the K8s API" — implies the protocol, not the component |

**Action:**

1. Run a search across all 15 files for each "Avoid" phrase.
2. For each hit, replace with the canonical term — *unless* it's a deliberate first-mention gloss in parentheses.
3. After replacement, re-read the surrounding sentence — synonyms sometimes carry rhythmic value the canonical term lacks. If the sentence reads worse, re-cast the sentence (don't restore the synonym).

This pass is mechanical-ish but must be done by reading, not blind find-and-replace.

---

## 7. Phase 4 — The Unified K-Town Universe

The course currently uses 13+ distinct analogies (property manager, apartments, thermostat, shipping containers, restaurants, industrial kitchen, library, trains, office buildings, warehouses, bakery, bank, ship, airport, permit office, shared apartment). Each lesson asks the reader to spin up a fresh mental model. That's real cognitive tax.

The fix is **not** to flatten all analogies into one — each individual analogy is strong. The fix is to set them inside a single shared *world*: the city of **K-Town** (alternative name acceptable: **Cluster City**). Each existing analogy becomes a *district* of that city. The cast and the city map persist; the lesson-specific analogy zooms into that district.

### 7.1 The cast (recurring across all lessons)

- **Mayor Katie.** The city's manager. Personifies Kubernetes itself. Appears in Lesson 01 ("the property manager") and is name-dropped in any lesson that needs a "Kubernetes did this" actor.
- **Podrick.** The unit/box/parcel that gets placed, moved, packed, deployed. Personifies the Pod (and by extension a workload). Has a face on the small character illustration.
- **The Thermostat.** The wise old gadget, slightly grandfatherly, who explains control loops. Lives on the wall in every building of K-Town. Speaks in Lesson 03 and reappears as a knowing wink whenever a new reconciliation loop is introduced (Lessons 06, 13, 14).

Optional supporting characters used sparingly:

- **Captain Tini.** The well-trained ship captain in Lesson 12. Appears once.
- **Inspector Pause.** The silent guard at the door of every co-living unit in Lesson 15.

These characters do not need fully drawn art on every page. A small recurring icon (silhouette) in the margins is enough.

### 7.2 The districts (one analogy per lesson, all in one city)

| Lesson | District / Setting |
|---|---|
| 01 | **Mayor's Office** (Katie running the city) |
| 02 | **Residential District** (houses vs apartment buildings) |
| 03 | **Climate Control Tower** (every building has thermostats — featured here) |
| 04 | **Port + Restaurant Row** (standard shipping containers + food courts) |
| 05 | **Industrial Kitchen Block** (vs a single toaster on someone's counter) |
| 06 | **Public Library** |
| 07 | **K-Town Rail Yard** (alpha branch line → main intercity) |
| 08 | **Office Tower with Utility Meters** |
| 09 | **Customs Warehouse** (forklifts moving standard containers) |
| 10 | **Bakery District** (recipes, ovens, cakes, ingredient lists, baker's seal) |
| 11 | **K-Town Bank Vault Quarter** |
| 12 | **K-Town Harbour** (lighthouse + ship + captain) |
| 13 | **K-Town International Airport** (control tower + terminals) |
| 14 | **City Hall — Permit Office** |
| 15 | **Co-Living Quarter** (Pod = co-living unit, NOT apartment) |

### 7.3 Implementation

Two pieces of new content needed:

**(a) A small "K-Town map" graphic.** SVG. Shows all 15 districts as pins on a stylised city map, with the current lesson's pin glowing/highlighted. Place it once per lesson, just under the breadcrumb header. Reuse the same SVG; only the highlighted pin changes per lesson.

**(b) An opening line on each lesson** (just inside the H1 area, before the Nightmare box):

> *📍 Today's stop in K-Town: **the Bakery District**.*

Or whatever district fits the lesson. One line. Sets the world without being twee.

### 7.4 What NOT to do

- **Do not rewrite the existing analogies.** Each one stays as is. The framing just nests them inside K-Town.
- **Do not introduce more than 3 recurring characters.** Beyond Katie, Podrick, and the Thermostat, every additional character is overhead.
- **Do not let the city framing crowd the actual content.** It's a wrapper, not the lesson.

---

## 8. Phase 5 — Per-Lesson Application

For **every** lesson, apply the following pattern:

1. **K-Town district line** at the top.
2. **3 AM Nightmare box** below the H1.
3. **One-sentence stamp** at the top (under the Nightmare) and at the bottom (just above "Lesson complete").
4. **Two `pause-and-check` stops** mid-lesson (between §1↔§2 and §4↔§5).
5. **Translation Legend table** in the Analogy section, replacing the existing "The mapping:" bullet list.
6. **`analogy-stops-here` callout** where applicable (most lessons).
7. **Common Misconceptions panel** (3 myths) before the quiz.
8. **One CYOA quiz item** replacing one of the three existing scenario questions.
9. **Concept rail** on the left, with the current lesson highlighted.
10. **Vocabulary canonicalization** sweep within the lesson (from Phase 3).

Per-lesson specifics below. Each block gives you the *content* — the Nightmare script, the stamp, the misconceptions, the CYOA scenario, the pause-checks, plus any lesson-specific edits.

---

### 8.1 Lesson 01 — What is Kubernetes?

**District:** Mayor's Office (Katie running the city).

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> It's 3 AM on a Saturday. Your phone buzzes. The website is down. You SSH into the server, squint at logs by candlelight, restart things by hand, hope you didn't break something else. By the time you're back to bed, it's dawn. Now imagine three apps and ten servers. This lesson is about what happens when you stop doing that — and let software do it instead.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: Kubernetes runs your apps across many computers, watches them forever, and fixes things automatically — so you can sleep.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** You tell Kubernetes "run 3 copies of my app." It places them. One server crashes. What happens?
> a) Kubernetes calls your phone
> b) Kubernetes places a replacement on a healthy server
> c) Nothing — you have to fix it manually
>
> *Answer: **b**. That's the whole point. Self-healing without paging a human.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** A 3-engineer startup with 1 small app is debating "should we move to Kubernetes?" What's the right answer?
> a) Yes, it's the modern way
> b) No — Kubernetes pays back at scale; for one app it's overkill
> c) Yes, but only on weekends
>
> *Answer: **b**. The cluster itself is a small project to keep alive. With one app, you're paying the cost without getting the benefit. Lesson 05 goes deeper.*

**Common Misconceptions:**
1. *Myth:* Kubernetes replaces my code / fixes my bugs. *Truth:* It runs your app and recovers it from infrastructure failures. Buggy code stays buggy.
2. *Myth:* Kubernetes only runs in the cloud. *Truth:* It can run on your laptop, in a data centre, on bare metal, or anywhere else.
3. *Myth:* "K8s" is a different product. *Truth:* It's the same thing — "K-eight-S" is shorthand for the 8 letters between K and s in "Kubernetes."

**CYOA item:** Replace the third existing scenario question ("Why does describing what you want…") with:

> **🎬 Choose Your Own Adventure**
> You're a small fintech startup with 3 engineers and 1 app. A friend says "you should be on Kubernetes — it's the modern way." You spin up a cluster. **Click to see what happens to your team. ▼**
> *Reveal:* Six months later, two of your three engineers are full-time keeping the cluster healthy: upgrades, observability, security patches, certificate rotation. You shipped half the features you would have on a managed app platform. Your investors notice. You eventually move back to Render and keep Kubernetes only for the one service that justifies it. **Lesson:** Kubernetes pays back at scale. For one tiny app, it's an industrial kitchen for your morning toast.

**Lesson-specific edits:**
- Move the "BEFORE · 3 AM" / "AFTER · 3 AM" graphic *above* the H2 "What Kubernetes actually is." Pain first, concept second.
- Add Katie as the named "property manager" character — currently the analogy is anonymous.

**`analogy-stops-here`:** *⚠️ The analogy stops here: a property manager handles dozens of apartments. Kubernetes handles thousands of apps across thousands of machines. Property managers also charge fees. Kubernetes is free.*

---

### 8.2 Lesson 02 — Virtualization vs Containerization

**District:** Residential District.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> Your team needs to ship 60 microservices. Each one runs in its own virtual machine. Each VM carries a full operating system — that's 60 copies of Linux, hogging RAM and disk. Booting one takes minutes. Cold starts during traffic spikes are the difference between a sale and a lost customer. This lesson is about the lighter alternative — and why Kubernetes was built on top of it.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: VMs are houses (own everything, heavy). Containers are apartments (shared building, light).**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** A VM image is typically 5–20 GB. A container image is typically 10–500 MB. Why the gap?
> a) Containers compress better
> b) A VM ships a whole operating system inside; a container ships only the app
> c) Containers store fewer files
>
> *Answer: **b**. The OS-shaped chunk is what's missing.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** A bank wants to run apps for three competing customers on the same hardware. The customers don't trust each other. VMs or containers?
> a) Containers — they're faster
> b) VMs (or sandboxed runtimes like gVisor) — separate kernels per customer
> c) Either is fine
>
> *Answer: **b**. Plain containers share the host kernel. A kernel exploit in one customer's container could reach others. VMs give each customer their own kernel — much stronger isolation.*

**Common Misconceptions:**
1. *Myth:* A container has its own operating system. *Truth:* It shares the host's kernel. The "OS-like" feel is a private view, not a real second OS.
2. *Myth:* Containers replaced VMs. *Truth:* They're complementary. Most cloud Kubernetes runs containers *inside* VMs the cloud provides.
3. *Myth:* Containers are unsafe because they share a kernel. *Truth:* They're safe enough for trusting tenants. For hostile multi-tenancy, use VMs or sandboxed runtimes (gVisor, Kata).

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> You're running a CI system. Every commit triggers 50,000 test jobs per day. You build it on VMs, because "VMs are isolated and safe." **Click to see what happens to your bill. ▼**
> *Reveal:* Each VM takes 90 seconds to boot. Each test takes 30 seconds. So 75% of your CI time and budget is spent waiting for VMs to boot. Containers boot in milliseconds. Switching cuts your CI bill by ~70% and triples throughput. **Lesson:** pick the lighter unit when the workload churns.

**Lesson-specific edits:**
- No changes to the apartment analogy here. (Lesson 15 will be the one to change — see §8.15.)

**`analogy-stops-here`:** *⚠️ The analogy stops here: unlike apartments, you can run thousands of containers on one computer. The plumbing doesn't get clogged.*

---

### 8.3 Lesson 03 — Cloud-Native Principles

**District:** Climate Control Tower (every building in K-Town has thermostats).

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> Your deploy script has 200 lines of bash. Step 4 runs `ssh` to 30 servers. Tonight, on server 17, step 4 fails — and you have no idea what state servers 1–16 are in, or 18–30. Are they on the new version? The old? Half each? You can't tell without looking. The script can't recover; it just stopped. This lesson is about the model that makes that whole class of problem go away.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: Kubernetes is a thermostat. You set what you want; controllers watch forever; gaps close automatically. Everything else in the course is a variation of this loop.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** Your YAML says `replicas: 3`. A pod crashes. Now 2 are running. What does the controller do?
> a) Sends an email
> b) Notices the gap (3 ≠ 2) and starts a 3rd pod on a healthy node
> c) Updates the YAML to say `replicas: 2`
>
> *Answer: **b**. The controller is constantly comparing desired (3) to actual (2). When they differ, it acts. Forever. That's the loop.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** Imperative vs declarative — which one is Kubernetes?
> a) Imperative: "do step 1, then step 2, then step 3"
> b) Declarative: "I want this end state; figure it out"
> c) Both
>
> *Answer: **b**. You write the goal; controllers figure out the steps. That's why K8s recovers from failures — it doesn't have a "step 4 failed" problem because there's no fixed step 4.*

**Common Misconceptions:**
1. *Myth:* The reconciliation loop runs once and stops when everything matches. *Truth:* It never stops. When the gap is zero it idles, but it keeps watching. The moment something drifts (a crash, a manual edit), the loop fires again.
2. *Myth:* Declarative means "I never write any logic." *Truth:* You still write a correct spec. If the YAML says "3 copies of a broken app," you'll get 3 copies of a broken app — restarted forever.
3. *Myth:* There's one big controller in Kubernetes. *Truth:* There are dozens, each watching one type of resource (Deployments, Services, Jobs…), all running the same loop pattern in parallel.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> You SSH into a production node and "quickly" hand-edit a config to fix an issue. Your cluster is GitOps-managed by Argo CD. You log off feeling smart. **Click to see what happens in 30 seconds. ▼**
> *Reveal:* Argo CD reads your hand-edit (drift), reads what Git says (the source of truth), notices they differ, reverts your change. Slack pings the team channel: `drift detected, reconciled to git/main`. Your "fix" is gone. **Lesson:** in a GitOps world, Git is the truth. Out-of-band edits get politely undone — by design.

**Lesson-specific edits:**
- Anthropomorphise the Thermostat lightly: give it a tiny grandfatherly voice in one of the section blurbs. ("The Thermostat doesn't ask why the room got cold. It just fires the heater again.") Keep it minimal — one or two callouts, not a takeover.

**`analogy-stops-here`:** *⚠️ The analogy stops here: a real thermostat watches one thing — temperature. Kubernetes runs many "thermostats" at once, one per resource type, all in parallel.*

---

### 8.4 Lesson 04 — 12-Factor Apps + Microservices vs Monoliths

**District:** Port + Restaurant Row.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> You're moving an app to Kubernetes. The app reads its database password from a file at `/etc/myapp/db.conf`, written by a Chef recipe at server-provisioning time. You bring it up in a Kubernetes pod. The file isn't there. The app crashes on startup. Pods are temporary; pod filesystems disappear. Your weekend is gone. This lesson is about the 12 rules that prevent you from ever fighting the platform like this again.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: a 12-factor app is a standard shipping container — drops cleanly into any platform. Microservices vs monoliths is about size, not virtue. Most teams should start with a modular monolith.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** Where should an app's database password live?
> a) Hardcoded in source code
> b) In a file under `/etc/` written by a Chef recipe
> c) In an environment variable, injected by the platform
>
> *Answer: **c**. Factor 3 (Config) — env vars, never code, never baked-in files. Same image, different config per environment.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** A 6-engineer startup is debating "should we start with microservices or a monolith?"
> a) Microservices — that's how Netflix did it
> b) Modular monolith — clear boundaries, simple ops
> c) Doesn't matter
>
> *Answer: **b**. Microservices push complexity from the codebase to the network: tracing, retries, timeouts, separate dashboards, separate on-call. A 6-engineer team rarely has the operational maturity for that. Start with a modular monolith; split a service out only when scale or team boundaries clearly demand it.*

**Common Misconceptions:**
1. *Myth:* Microservices are always better than monoliths. *Truth:* They're an answer to *organisational scale*, not a starting architecture. Shopify runs hundreds of engineers on one Rails monolith — and ships daily.
2. *Myth:* 12-factor is just a coding style. *Truth:* It's the contract between your app and any modern platform. Violating it doesn't fail tests — it fails Tuesday afternoons in production.
3. *Myth:* Stateless means "the app doesn't store anything." *Truth:* Stateless means *the process* doesn't hold important state in memory. State lives in attached backing services — Postgres, Redis, S3 — that survive restarts.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> Your team writes logs to `/var/log/myapp.log`, rotated by a cron job. You move to Kubernetes "as is." **Click to see what happens to your logs. ▼**
> *Reveal:* The pod restarts. The pod's filesystem disappears. Your logs disappear with it. Cron isn't running. Log rotation never happened. You're trying to investigate a 3 AM outage with nothing to look at. **Fix:** Factor 11 — write logs to stdout. Kubernetes captures them, ships them to your aggregator, retains them as policy. The platform owns log lifecycle; your app stays generic.

**Lesson-specific edits:** None beyond the standard pattern.

**`analogy-stops-here`:** *⚠️ The analogy stops here: standard shipping containers are 20 or 40 feet long. Software containers are whatever size you make them — the "standard" is the interface, not the dimensions.*

---

### 8.5 Lesson 05 — When Kubernetes Fits / Overkill

**District:** Industrial Kitchen Block (vs a single toaster on someone's counter).

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> You adopted Kubernetes "because it's the modern way." A year in, two of your four engineers are full-time on cluster ops: upgrades, observability, security patches, certificate rotation, on-call. You're shipping fewer features than you would have on Heroku. Your investors are asking why. This lesson is about reading the situation honestly *before* adoption — not after.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: Kubernetes pays back at operational scale (many services, many teams). For a single small app, it's an industrial kitchen for your morning toast.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** Three engineers, one Django app, one Postgres, deploying twice a week. Does Kubernetes fit?
> a) Yes — it's the standard
> b) No — managed app platform (Render, Fly, Heroku) is a better fit at this size
> c) Only if they're remote
>
> *Answer: **b**. Kubernetes pays back when many services and many teams are the bottleneck. With one app and three engineers, the cluster itself becomes the bottleneck.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** A high-frequency trading firm has a trading engine that needs sub-100µs latency. K8s networking adds 50–200µs per pod hop. Should the trading engine run on Kubernetes?
> a) Yes — it's the modern way
> b) No — bare metal with kernel-bypass networking
> c) Only the dashboards
>
> *Answer: **b** (and also c). The trading engine goes on bare metal. The dashboards (normal HTTP latency) can happily sit on K8s. Different workloads, different platforms.*

**Common Misconceptions:**
1. *Myth:* Kubernetes makes one app simpler. *Truth:* It never does. It pays off when the *count* of things you're operating becomes the bottleneck.
2. *Myth:* Managed Kubernetes is the same operational burden as self-managed. *Truth:* Managed (EKS/AKS/GKE) takes the control plane off your plate — that's most of the ongoing pain.
3. *Myth:* If we don't pick Kubernetes now, we'll regret it later. *Truth:* Most teams are better off starting on a managed app platform and migrating *if* they outgrow it. Migrations are real but cheaper than two engineers full-time on cluster ops at year one.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> Your CEO read a Hacker News post and announces "we're moving to Kubernetes by Q3." Your team is 4 engineers, 1 app, 100 daily users. **Click to see how this goes. ▼**
> *Reveal:* By Q4 you've shipped half the planned features. One engineer quit because "I joined to build a product, not babysit YAML." The CEO eventually asks "what would have happened on Render?" The answer is: same product, twice the velocity, no cluster on-call. **Lesson:** "the modern way" without "the modern need" is just the modern bill.

**Lesson-specific edits:** None beyond the standard pattern.

**`analogy-stops-here`:** *⚠️ The analogy stops here: a kitchen and a toaster cost different amounts. Kubernetes can be free if you self-manage — the cost is engineering time, which is harder to see on a cloud bill.*

---

### 8.6 Lesson 06 — GitOps · Platform Engineering · SRE · Multi-Tenancy

**District:** Public Library.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> Your one ops engineer is the bottleneck for every deploy across 6 product teams. Every change is a ticket. Tickets pile up. Deploys take days. The ops engineer is on call for everything they didn't write. They're burning out and the company can't ship. This lesson is about the org shape that fixes this — and why it's not just a tooling change.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: five practices that compound — GitOps + platform engineering + SRE + service ownership + multi-tenancy. None is a Kubernetes feature; all are practices Kubernetes enables.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** GitOps puts the source of truth in:
> a) The cluster
> b) An ops engineer's head
> c) A Git repository
>
> *Answer: **c**. An agent in the cluster watches Git and reconciles. Same loop pattern as a Kubernetes controller, just one level up.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** "You build it, you run it" means:
> a) Developers do everything; no ops team
> b) The team that built the service is on its on-call rotation
> c) Only senior engineers go on call
>
> *Answer: **b**. The team that wrote the code is paged when it breaks. Reliability emerges from incentive — they fix the things that wake them up.*

**Common Misconceptions:**
1. *Myth:* GitOps is just "use Git for your YAML." *Truth:* It's an *agent in the cluster* continuously reconciling state to match Git. Manual edits get reverted. That's the part that makes it powerful.
2. *Myth:* SRE = "ops, but renamed." *Truth:* SRE adds explicit reliability targets (SLOs) and an *error budget* — when you've spent the budget on outages, you slow down feature work and fix things. It's an operating model, not a job title.
3. *Myth:* Multi-tenancy means one cluster per team. *Truth:* Soft tenancy = one cluster, isolated by namespaces + RBAC + quotas (for trusted tenants). Hard tenancy (separate clusters or vCluster) is for *untrusted* tenants only.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> Your platform team runs an "ops ticket queue" for 6 product teams. Tickets average 2 days to close. **Click to see the year-end review. ▼**
> *Reveal:* Two engineers quit (burnout). The remaining ops engineer is on call for 6 teams' code they didn't write. Deploys average 2 days from PR to live. Product velocity is half of what it could be. The fix isn't more tooling — it's restructuring: platform team owns the road; product teams own their services and their pages. Reliability follows incentive.

**Lesson-specific edits:** None beyond the standard pattern.

**`analogy-stops-here`:** *⚠️ The analogy stops here: a librarian doesn't argue with you. The GitOps controller doesn't either — if Git says shelve under N, it shelves under N. No "but I think it's better here."*

---

### 8.7 Lesson 07 — History · CNCF · Releases · KEPs · Feature Gates

**District:** K-Town Rail Yard.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> You enabled a Kubernetes alpha feature in production "to get ahead." Six months later you upgrade the cluster. The feature was renamed. Your manifests don't apply. Your deploys are broken. You spend two on-call weeks rebuilding workloads. This lesson is about the lifecycle every Kubernetes feature graduates through — and why "GA only in prod" is the rule that keeps you out of this hole.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: every Kubernetes feature graduates alpha → beta → GA, like train signals tested on a quiet branch line first. Production runs on GA.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** What does "GA" mean in Kubernetes?
> a) "Good Available"
> b) "General Availability" — stable, on by default, backward-compatibility guaranteed
> c) "Google Approved"
>
> *Answer: **b**. GA carries the strongest compatibility guarantee K8s offers.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** Your team is debating whether to enable a new beta feature in production.
> a) Yes — beta is mostly stable
> b) Read the KEP, vet case-by-case, decide based on risk
> c) Never use anything until it's GA
>
> *Answer: **b**. Beta APIs *can* still change shape. The right move is vetting per feature, per cluster, per risk profile — not a blanket yes or no.*

**Common Misconceptions:**
1. *Myth:* Alpha = "almost done." *Truth:* Alpha = "off by default, may break, may vanish without deprecation." Production-hostile by design.
2. *Myth:* Kubernetes belongs to Google. *Truth:* It came out of Google in 2014, but it's been governed by the CNCF (a Linux Foundation project) since 2015. Hundreds of contributors at hundreds of companies.
3. *Myth:* "Kubernetes-compatible" and "Certified Kubernetes" mean the same thing. *Truth:* Certified Kubernetes is a CNCF program with a specific test suite. "Compatible" is marketing.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> You read about a shiny new alpha feature and enable it cluster-wide. Your prod runs on it. **Click to see what happens at the next minor upgrade. ▼**
> *Reveal:* The alpha API was renamed without deprecation (legal under alpha rules). Your manifests don't apply. Pods stuck. You spend two weeks rewriting workloads. **Lesson:** alpha is the quiet branch line where breakage is expected. Production is the main intercity. Don't run intercity trains on branch-line tracks.

**Lesson-specific edits:**
- **Apply Phase 1.2:** Replace the InPlacePodVerticalScaling example with the Gateway API example.
- Apply `skip-if-new` tag to the conformance / hydrophone-vs-sonobuoy paragraph.

**`analogy-stops-here`:** *⚠️ The analogy stops here: trains test new signals once per signal. Kubernetes tests every feature, separately, every release. There's no shared "main line approval."*

---

### 8.8 Lesson 08 — Linux Namespaces, cgroups, Capabilities

**District:** Office Tower with Utility Meters.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> Your container keeps getting killed. The logs say `OOMKilled`. You set the memory limit to 256Mi. The app reports it only uses 200MB. Why is it dying? Because the kernel — the *real* boss of the whole machine — is enforcing limits you didn't fully understand. This lesson is about the five Linux features that decide what your container can and can't do. No magic. Just plumbing.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: a container is a Linux process with walls (namespaces), meters (cgroups), and rules about what it can do (capabilities, seccomp, LSM). Five kernel features, no magic.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** What stops one container from seeing another container's processes?
> a) The container runtime
> b) Linux namespaces — specifically the PID namespace
> c) Encryption
>
> *Answer: **b**. Each container gets a private view of process IDs. Without that namespace, `ps` would show every process on the host.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** A container hits 257MB of memory; its `limits.memory` is 256Mi. What happens?
> a) The container slows down
> b) The kernel kills the container's PID 1 (OOM)
> c) The container gets more memory automatically
>
> *Answer: **b**. cgroup memory limits aren't suggestions. The kernel enforces them with `OOMKilled`.*

**Common Misconceptions:**
1. *Myth:* "Container" is a Linux feature. *Truth:* Containers are made by *combining* five kernel features (namespaces + cgroups + capabilities + seccomp + LSM). The runtime (Docker, containerd) bundles them. The kernel does the work.
2. *Myth:* Each container has its own kernel. *Truth:* All containers on a host share the host's kernel. That's the whole point — and the whole risk. A kernel exploit can break out of any container.
3. *Myth:* `limits` and `requests` are the same thing. *Truth:* `requests` is what the scheduler reserves (the floor). `limits` is the hard ceiling (CPU throttled, memory OOM-killed above).

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> A teammate adds `hostNetwork: true` to a pod spec "just to test something." **Click to see what they just did. ▼**
> *Reveal:* The container now shares the host's network stack — same IPs, same interfaces, same firewall rules. It can bind to any host port (and conflict with anything else on the host). It can sniff traffic on host interfaces. K8s Service discovery often breaks because the pod has the host's IP, not a pod IP. **Lesson:** every `host*` field (`hostNetwork`, `hostPID`, `hostIPC`) drops a namespace and gives the container access to host resources. Powerful for specific cases (CNI plugins). Footgun for normal apps.

**Lesson-specific edits:**
- **Apply Phase 1.1:** Unify the seccomp count with Lesson 11 (use the canonical phrasing).
- Add a banner at the very top: *"New to Linux? Take a 5-minute detour through Lesson 7.5 — How a Linux Computer Works."*
- Apply `skip-if-new` tag to the cgroup v1 vs v2 paragraph.

**`analogy-stops-here`:** *⚠️ The analogy stops here: an office building has one electrical panel that can be overloaded by one tenant. The kernel can be DoSed by a noisy container too — but cgroups make this much harder than the real-world equivalent.*

---

### 8.9 Lesson 09 — Container Runtimes & OCI

**District:** Customs Warehouse.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> Your team built an app on an ARM Mac (M-series). You deploy to AMD64 nodes in EKS. The pod crashes immediately: `exec format error`. You can't tell from the message that the binary is the wrong architecture. You stare at logs for an hour. This lesson is about the format that makes containers portable — and the standard that lets one image work on every CPU and every cloud.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: OCI is the standard. Runtimes are forklifts. Layers stack. Tags move; digests don't. Pin to digests in production.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** What does "OCI" stand for?
> a) Open Container Image
> b) Open Container Initiative — Linux Foundation standards body since 2015
> c) Operating Container Index
>
> *Answer: **b**. Three specs (image, runtime, distribution). The contract that lets any runtime work with any registry.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** You see `nginx:1.27` and `nginx@sha256:abc…`. Which is safe to use in production?
> a) The tag — it's friendlier
> b) The digest — it's immutable
> c) Either, doesn't matter
>
> *Answer: **b**. Tags can be moved by the publisher. Digests are SHA-256 of the manifest — same content always = same digest. Pin to digests for reproducibility.*

**Common Misconceptions:**
1. *Myth:* Docker is the only container runtime. *Truth:* Modern Kubernetes runs `containerd` or `CRI-O` by default. Docker is a higher-level platform that uses `containerd` underneath.
2. *Myth:* `latest` is fine for production. *Truth:* `latest` is the worst tag offender. It's mutable. Two pods with the same `latest` tag can run different code on different nodes after a re-push. Pin to a digest.
3. *Myth:* An image works on any CPU. *Truth:* Only if it was built multi-arch (`docker buildx --platform linux/amd64,linux/arm64`). Otherwise an ARM build will not run on AMD64 nodes.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> Your team uses `image: my-app:latest` in production "so we always get the newest version." **Click to see what happens on Friday at 6 PM. ▼**
> *Reveal:* Someone pushes a new `latest` with a bad migration. Pods restarting through the night pick up the new image. By Saturday morning, half the pods are on the bad image and half on the old — depending on when each pod last restarted. You can't even reproduce the issue locally because `latest` is whatever it is right now. **Fix:** pin to a digest. Use Renovate to bump digests via PR with tests. Reproducibility AND staying current.

**Lesson-specific edits:**
- Apply `skip-if-new` tag to the runc vs crun vs youki comparison paragraph.

**`analogy-stops-here`:** *⚠️ The analogy stops here: a real shipping container has fixed dimensions. A software image is whatever size the layers add up to. The "standard" is the format, not the size.*

---

### 8.10 Lesson 10 — Image Building

**District:** Bakery District.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> Your Node.js image is 1.2 GB. CVE scans flag 124 vulnerabilities, mostly in libraries you don't even use. Production pulls take 90 seconds — that's 90 seconds of extra outage every time something restarts. Your security team is asking pointed questions. This lesson is about the changes that take that image from 1.2 GB to 80 MB and from 124 CVEs to 8 — without touching your app code.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: build small (multi-stage), ship smaller (distroless), sign your work, generate an SBOM, scan for CVEs. That's a production-grade image.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** A multi-stage Dockerfile has:
> a) Multiple Dockerfiles in one repo
> b) Multiple `FROM` statements — a "build" stage with full toolchain, a "runtime" stage with only the artifact
> c) Multiple containers running in parallel
>
> *Answer: **b**. Final image is 10–100× smaller because the runtime stage doesn't carry compilers, source code, or dev dependencies.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** What's an SBOM?
> a) "Service Bound Object Metadata"
> b) Software Bill of Materials — machine-readable list of every component in your image
> c) A type of container
>
> *Answer: **b**. When the next Log4Shell drops, an SBOM database lets you grep for the vulnerable library across hundreds of services in seconds. Without one, days.*

**Common Misconceptions:**
1. *Myth:* Distroless means "no Linux." *Truth:* Distroless images include just enough Linux to run your app — and nothing else (no shell, no package manager, no debugger). The runtime is still Linux underneath.
2. *Myth:* Smaller image = always better. *Truth:* Distroless and `scratch` are harder to debug. The right answer is "smallest base that runs your app *and* lets you investigate when needed" — sometimes that's a slim variant, not scratch.
3. *Myth:* Image signing prevents bugs. *Truth:* Signing prevents *tampering*. It tells you the image was built by your pipeline and hasn't been swapped. It says nothing about whether the code is correct.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> An attacker compromises your CI credentials and pushes a malicious image to your registry under a legitimate tag. Your prod has a Kyverno admission policy requiring images to be signed by your team's Cosign key. **Click to see what happens. ▼**
> *Reveal:* The malicious image isn't signed — the attacker had registry creds but not the Cosign key. Kubernetes refuses to admit the pod. The incident is contained at the admission boundary, before any malicious code ran. Your incident retrospective is about why the CI creds were compromised, not about a breached cluster. **Lesson:** image signing turns a tag-swap from a breach into a denied admission.

**Lesson-specific edits:**
- Apply `skip-if-new` tag to the buildx multi-arch internals paragraph.

**`analogy-stops-here`:** *⚠️ The analogy stops here: a real cake gets baked once and eaten. A container image gets pulled millions of times. Optimisation matters here in a way it doesn't for cakes.*

---

### 8.11 Lesson 11 — Container Security & Registries

**District:** K-Town Bank Vault Quarter.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> Your web app gets compromised through an unsanitised input. The attacker gets a shell *as root* inside the container. They write a webshell to disk, escalate via a kernel CVE, pivot to the host, then to other pods. By morning, your cluster is gone. The same bug, on a hardened pod, is a Tuesday afternoon ticket. This lesson is the 12 lines of YAML that change which one happens.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: where the image came from (auth + pull policy) plus how it runs (non-root, read-only, drop caps, seccomp) shrinks blast radius 10×.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** Your image is in a private registry. Your pod can't pull it (`ImagePullBackOff`). What's missing?
> a) The cluster doesn't have internet
> b) An `imagePullSecret` with the registry credentials
> c) The image doesn't exist
>
> *Answer: **b**. The kubelet needs credentials to pull from private registries. Create a `kubernetes.io/dockerconfigjson` secret and reference it in the pod spec via `imagePullSecrets`.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** Pick the safest of these settings for a production pod:
> a) Run as root, all capabilities, writable filesystem
> b) Run as non-root (UID 1000), drop ALL caps, read-only filesystem, seccomp RuntimeDefault
> c) Run as root, drop ALL caps
>
> *Answer: **b**. Each of those settings shrinks the blast radius of a bug. Together they match the Pod Security Standards "Restricted" profile.*

**Common Misconceptions:**
1. *Myth:* Running as root inside a container is safe because the container is isolated. *Truth:* Container root + a kernel exploit = host root. Run as a non-root UID by default.
2. *Myth:* `imagePullPolicy: Always` is overkill. *Truth:* For mutable tags it's the only safe policy. For digest-pinned images, the question is moot — same digest, same content, every time.
3. *Myth:* Pod Security Standards are something you have to install. *Truth:* They're built into the Kubernetes API server (since 1.25). Apply via namespace labels — no third-party admission needed.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> A new dev tries to deploy a pod with `securityContext: { privileged: true }` "for easier debugging." Your namespace is labeled `pod-security.kubernetes.io/enforce: restricted`. **Click to see what happens. ▼**
> *Reveal:* The API server rejects the pod at admission with a clear message: `violates PodSecurity 'restricted:latest' — privileged is not allowed`. The conversation moves from "let's just allow it" to "let's fix the actual debugging tooling." Defaults won. **Lesson:** opt-in security is opt-out reality. Set the namespace policy and let the API server hold the line.

**Lesson-specific edits:**
- **Apply Phase 1.1:** Unify the seccomp count with Lesson 08.

**`analogy-stops-here`:** *⚠️ The analogy stops here: a bank vault has one combination. A container has dozens of independent locks (each `securityContext` field). Skipping any one is leaving a door cracked.*

---

### 8.12 Lesson 12 — PID 1 & Container Lifecycle

**District:** K-Town Harbour.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> It's 3 AM. Your deploy went out clean. But somehow 4% of customer orders vanished mid-checkout, and your logs just say `Killed`. By morning you have 47 angry support tickets and no idea which pods got hit. This lesson is about why that happens — and the one line of YAML (`ENTRYPOINT ["tini", "--", ...]`) that prevents it.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: PID 1 inside your container has two jobs Linux normally hands to systemd — forward signals and reap zombies. Wrap your entrypoint in `tini`. Handle SIGTERM. Add a `preStop` sleep. Tune the grace period.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** Your container's Dockerfile has `CMD ["bash", "start.sh"]` and `start.sh` runs `node server.js &`. K8s sends SIGTERM. What happens?
> a) Node receives SIGTERM and shuts down gracefully
> b) Bash (PID 1) receives it but doesn't forward it; Node never knows
> c) Both processes get the signal
>
> *Answer: **b**. Bash is PID 1 and doesn't forward signals to background children. Node never learns the pod is shutting down. After 30s grace, SIGKILL. In-flight requests dropped.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** During rolling updates, a small fraction of requests return 502 for a few seconds. Pods are healthy. The app handles SIGTERM correctly. What's the cause?
> a) The app is broken
> b) Race condition: load balancer is still sending traffic to a pod whose port has already closed
> c) The cluster is overloaded
>
> *Answer: **b**. The endpoints update is slower than the app's shutdown. Fix: add a `preStop` hook that sleeps 10s before SIGTERM is sent — gives the LB time to drain the pod from rotation.*

**Common Misconceptions:**
1. *Myth:* SIGKILL is "just a stronger SIGTERM." *Truth:* SIGKILL is uncatchable, kernel-level. Your app *cannot* clean up under SIGKILL — it just dies. That's why graceful shutdown matters.
2. *Myth:* `terminationGracePeriodSeconds` is a hint. *Truth:* It's a hard wall-clock timer. SIGKILL fires at the end. Tune it (60s, 300s) for slow shutdowns — databases, queue workers, big flushes.
3. *Myth:* Zombies are theoretical. *Truth:* A Java app spawning subprocesses without `waitpid()` will fill the PID table over hours. Real outage. `tini` solves it for free.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> You hire a rookie captain (`bash`) for your container ship. The lighthouse blinks SIGTERM. The captain… does nothing. He didn't think it applied to him. **Click to see what happens to the crew. ▼**
> *Reveal:*
> ```
>   harbour clock: 0s ─────────── 30s ───── 💀
>   crew status:    [loading]  [still loading]  [SIGKILL]
>   passengers:    ████████████████ 47% lost
> ```
> The harbour waited the full 30-second grace, then pulled the gangway with SIGKILL. The crew never got the message and were still loading cargo when the lights went out. **Fix:** hire `tini` as your captain — he forwards every signal he receives, on time, every time. `ENTRYPOINT ["tini", "--", "node", "server.js"]`. One line.

**Lesson-specific edits:** None beyond the standard pattern.

**`analogy-stops-here`:** *⚠️ The analogy stops here: a real captain can refuse to leave port. PID 1 cannot refuse SIGKILL — it's uncatchable. The only way to leave on your own terms is to leave during the grace period.*

---

### 8.13 Lesson 13 — Cluster Architecture

**District:** K-Town International Airport.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> A network partition isolates 2 of your 3 etcd nodes from each other. Quorum is lost. The cluster goes read-only — no new pods scheduled, no failover, no Deployments updated. Anything currently running keeps running, but the cluster is frozen in amber. You can't even apply the fix. This lesson is about the brain–muscle split that makes Kubernetes work, and where it breaks if you're not careful.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: control plane decides; nodes execute. Five control-plane components, three node components, one API door between them. Memorize the 6-hop pod-creation flow.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** Which component is the *only door* into a Kubernetes cluster?
> a) etcd
> b) The API server
> c) The kubelet
>
> *Answer: **b**. Every read, every write, every watch goes through the API server. Nothing talks to etcd directly. That's the design.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** Your 3-member etcd cluster loses 2 nodes. What happens?
> a) The cluster keeps running normally
> b) The cluster goes read-only — quorum lost
> c) Kubernetes schedules new etcd pods automatically
>
> *Answer: **b**. 3 members tolerate 1 failure. Lose 2, you're below quorum. 5-member etcd tolerates 2 failures.*

**Common Misconceptions:**
1. *Myth:* The control plane runs your apps. *Truth:* Control plane decides; worker nodes run. In production they're usually different machines, often with taints to keep workloads off the CP.
2. *Myth:* Components talk directly to each other. *Truth:* Everything goes through the API server. The scheduler doesn't tell the kubelet anything — it writes a Binding; the kubelet's watch picks it up.
3. *Myth:* Self-managed Kubernetes is "more flexible." *Truth:* For most teams under 50 engineers, managed (EKS/GKE/AKS) is a no-brainer. Self-managed wins for specific cases: bare metal, regulated environments, or 100+ clusters.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> You run `kubectl apply -f pod.yaml`. **Click to trace exactly what happens. ▼**
> *Reveal:*
> ```
>   1. kubectl  → API server     (POST /api/v1/.../pods)
>   2. API srvr → etcd           (validate, persist)
>   3. scheduler watches API     (picks node-3, POSTs Binding)
>   4. kubelet on node-3 watches (sees its pod)
>   5. kubelet  → runtime        (pull image, start)
>   6. kubelet  → API server     (PATCH status: Running)
> ```
> Notice every hop routes through the API server. The scheduler never tells the kubelet anything directly. **That single-door discipline is the architectural constraint that makes K8s scale.**

**Lesson-specific edits:**
- **Apply Phase 1.4:** Add the GKE/AKS/Autopilot pricing footnote.
- Apply `skip-if-new` tag to the Raft consensus / leader-election internals paragraphs.

**`analogy-stops-here`:** *⚠️ The analogy stops here: an airport tower has one radio operator. The Kubernetes API server is replicated 3+ ways behind a load balancer — multiple operators, all serving the same view, any can fail.*

---

### 8.14 Lesson 14 — The K8s API & YAML

**District:** City Hall — Permit Office.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> An engineer ran `kubectl scale deployment api --replicas=10` to handle a slow service. It worked. Three days later, a CI deploy from the git-tracked YAML (which still says `replicas: 3`) ran. `apply` diffed, scaled DOWN to 3 mid-traffic-spike. 5xx surge. This lesson is about why imperative kubectl is dangerous, and why every K8s object has the same 4-section permit form.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: every K8s object is the same 4-block form (`apiVersion + kind + metadata + spec`). `kubectl explain` is the manual. Never use imperative kubectl in production. CRDs make custom types first-class.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** Which of these is *not* a mandatory block in every Kubernetes YAML?
> a) `apiVersion`
> b) `status`
> c) `metadata`
>
> *Answer: **b**. `status` is filled in by controllers, not by you. The four mandatory blocks are `apiVersion`, `kind`, `metadata`, `spec`.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** You don't know if `replicaCount` or `replicas` is the right field name. What's the fastest way to find out?
> a) Google it
> b) `kubectl explain deployment.spec` — the cluster's own schema
> c) Read the source code
>
> *Answer: **b**. Your cluster ships with the manual built in. Reflects the *exact* version you're running, including any CRDs.*

**Common Misconceptions:**
1. *Myth:* CRDs are second-class objects. *Truth:* Once registered, they get the same RBAC, audit, validation, and storage as built-ins. cert-manager's `Certificate` and a Pod are equivalent in the API server's eyes.
2. *Myth:* `kubectl run` and `kubectl create` are the right way to deploy. *Truth:* Those are imperative — direct mutations with no audit trail. Production should always use `kubectl apply -f` (and ideally GitOps on top).
3. *Myth:* Labels and annotations are interchangeable. *Truth:* Labels are *indexed* and used for selection (`-l app=foo`). Annotations are free-form metadata, not selectable. If you'd ever filter by it, it's a label.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> Your YAML has `replicaCount: 3` (the right field is `replicas`). You run `kubectl apply --dry-run=client`. It passes. You commit. **Click to see what happens at deploy. ▼**
> *Reveal:* `--dry-run=client` only does shallow client-side validation — it doesn't know your cluster's actual schema. The deploy goes to prod. The API server rejects: `unknown field "spec.replicaCount"`. CI fails. Incident. **Fix:** always use `kubectl apply --server-side --dry-run=server` in CI. That talks to the actual API server and catches typos like this — including CRD-specific fields client-side validation misses.

**Lesson-specific edits:** None beyond the standard pattern.

**`analogy-stops-here`:** *⚠️ The analogy stops here: a permit office has business hours. The Kubernetes API server is always open and serves thousands of requests per second.*

---

### 8.15 Lesson 15 — Pods Deep Dive

**District:** Co-Living Quarter.

**3 AM Nightmare:**
> 🚨 **The 3 AM Nightmare**
> Your team's web app needs Postgres ready before it starts. The Dockerfile has `sleep 5` in the entrypoint as a "wait for DB" hack. Tonight, Postgres takes 7 seconds to be ready. Your app crashes on its first query. The pod restarts. Crashes again. Restarts. Hits CrashLoopBackOff. This lesson is about the Pod patterns — init containers, sidecars, ephemeral debug — that turn this whole class of pain into one-line YAML.

**One-sentence stamp:**
> 🎯 **If you remember nothing else: a Pod is the atomic unit of scheduling — one address, multiple containers sharing network and IPC. Init runs first, sidecars run alongside, ephemeral containers visit to debug.**

**Pause-and-check #1 (after Section 1):**
> ⏸ **Pause and check:** What's the atomic unit of scheduling in Kubernetes?
> a) A container
> b) A Pod
> c) A node
>
> *Answer: **b**. The container is the *packaging* unit. The Pod is what Kubernetes places on a node. Most pods have one container — but the rule "one or more containers, scheduled together" enables sidecars, init containers, and ephemeral debug.*

**Pause-and-check #2 (after Section 4):**
> ⏸ **Pause and check:** Your distroless container has no shell. It just started returning 500s. How do you debug it?
> a) `kubectl exec -it ... bash` (won't work — no shell)
> b) `kubectl debug -it broken-pod --image=busybox --target=app -- sh`
> c) Restart the pod and hope the bug goes away
>
> *Answer: **b**. `kubectl debug` adds an *ephemeral container* to the running pod. Sibling to the broken container, sharing its PID namespace. You get a shell without modifying the production image.*

**Common Misconceptions:**
1. *Myth:* "QoS class Guaranteed" means the pod always gets the memory it asks for. *Truth:* Guaranteed only affects *eviction priority* under node pressure. Within the pod, the limit is still a hard cap — exceeding it = OOM, regardless of class.
2. *Myth:* Sidecars are just "two containers in a pod." *Truth:* Native sidecars (K8s 1.28+) are init containers with `restartPolicy: Always`. Start before main, stay running, properly handled at shutdown. Old-style "just two containers" had lifecycle gotchas.
3. *Myth:* The `pause` container is something you write. *Truth:* It's invisible infrastructure. Every pod has one; you never see it in YAML. It holds the pod's network/IPC namespaces open so app containers can come and go without losing the IP.

**CYOA item:**
> **🎬 Choose Your Own Adventure**
> Your team sets `requests.memory: 1Gi` and `limits.memory: 1Gi` (QoS class: Guaranteed). The app spikes to 1.2Gi during bursts. **Click to see what happens. ▼**
> *Reveal:* OOMKilled. Every burst. The team thought "Guaranteed" meant "always gets the memory" — it doesn't. It means "request == limit, last to be evicted under *node* pressure." Within the pod, the limit is a hard cap. **Fix:** raise the limit (becomes Burstable but survives spikes), or right-size the app. QoS is about node-level eviction priority, not pod-level memory grants.

**Lesson-specific edits:**
- **Apply Phase 1.3:** Replace "apartment = Pod" with "co-living unit = Pod" throughout. Edit:
  - The H1 visual panel (`POD = ONE APARTMENT` → `POD = ONE CO-LIVING UNIT`).
  - The Section 3 prose (replace all "apartment" instances when referring to the Pod).
  - The mapping table.
  - The ELI5 / ELI10 paragraphs.
  - The glossary if relevant.
- Apply `skip-if-new` tag to the QoS-class-and-eviction internals paragraph.

**`analogy-stops-here`:** *⚠️ The analogy stops here: real co-living units have one front door but many bedrooms. Pods *can* share a PID namespace too (`shareProcessNamespace: true`), and any container can hold the pod's IP — there's no "main bedroom" that's special.*

---

## 9. Phase 6 — Verification

After all per-lesson edits land, do a final pass:

### 9.1 Cross-lesson consistency

- [ ] Every lesson has the K-Town district line at the top.
- [ ] Every lesson has the 3 AM Nightmare box.
- [ ] Every lesson has the one-sentence stamp at top *and* bottom.
- [ ] Every lesson has 2 pause-and-check items mid-lesson.
- [ ] Every lesson has the Translation Legend table in Section 3.
- [ ] Every lesson has the Common Misconceptions panel before the quiz.
- [ ] Every lesson has 1 CYOA quiz item among the three end-of-lesson scenarios.
- [ ] Every lesson has the persistent left-rail concept map.
- [ ] Lesson 7.5 exists.
- [ ] Lesson 08 has the cross-link to Lesson 7.5.

### 9.2 Accuracy spot-checks

- [ ] Seccomp count is identical in Lessons 08 and 11.
- [ ] Lesson 07 no longer references InPlacePodVerticalScaling — uses Gateway API instead.
- [ ] Lesson 15 uses "co-living unit" everywhere; no "apartment = Pod" remains.
- [ ] Lesson 13 has the GKE/AKS/Autopilot pricing footnote.

### 9.3 Vocabulary spot-checks

Search for the "Avoid" terms from §6 across all 15 lessons. Each hit must either be:
- A deliberate first-mention parenthetical gloss, or
- Replaced with the canonical term.

### 9.4 Visual spot-check

- [ ] Open Lesson 01, 08, and 13 in a browser. New components match existing visual language. Dark mode works. Mobile layout doesn't break (the concept rail collapses).

### 9.5 Reading spot-check

- [ ] Read Lesson 08 from top to bottom as if you're a layman. The Lesson 7.5 link should appear before any unfamiliar term. The Nightmare lands. The misconceptions feel useful, not obvious.
- [ ] Read Lesson 12. The CYOA reveal reads playfully but lands the technical lesson.

---

## 10. Out of Scope (do not do)

- **Do not** redesign the visual language. New components inherit from existing tokens.
- **Do not** rewrite the existing analogies. Each one stays — the K-Town framing nests them, doesn't replace them.
- **Do not** translate, expand, or shorten the existing prose unless explicitly listed in §8.
- **Do not** introduce new dependencies (no new fonts, no new JS frameworks).
- **Do not** add quizzes beyond what's specified.
- **Do not** edit the draft file (`preview-kubernetes-lesson-03-draft.html`).

---

## 11. Definition of Done

The work is complete when:

1. All 4 accuracy fixes (§4) are applied.
2. All 8 cross-cutting components (§5.1–§5.8) are built and applied to every lesson.
3. Lesson 7.5 (§5.9) exists and is linked from Lesson 08.
4. Vocabulary canonicalization (§6) has been swept across all lessons.
5. The K-Town universe (§7) is established with cast and districts.
6. Every per-lesson punch-list in §8 is fully applied.
7. The Phase 6 verification checklist (§9) passes.
8. Visual and reading spot-checks (§9.4–§9.5) pass.

When done, summarize back: which lessons changed, how many lines diffed in each, and any decisions that required judgment (e.g., colour-token choices, copy variants).

---

*End of plan.*
