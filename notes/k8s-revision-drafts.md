# K-Town revision — drafts not chosen

Discarded drafts from the K-Town revision, kept per QUALITY.md drafting
protocol. The accepted draft (and the rationale for picking it) is in
the matching DECISIONS.md entry.

---

## 2026-05-02 — L01 K-Town universe intro

**Accepted:** Draft D (synthesis), placed at top of L01 between the
district line and the K-Town map. See DECISIONS.md
"L01 K-Town universe intro" entry for the live copy.

### Drafts not chosen

#### Draft A — Cast-first, listy

> This map is K-Town. Every Kubernetes lesson in this course is set in
> one of its 16 districts — same city, same characters, same world.
> **Mayor Katie** runs the place (she's Kubernetes). **Podrick** is the
> unit that gets placed and moved (a *Pod*). **The Thermostat** is the
> wise old gadget on the wall in every building who explains how things
> keep themselves running. Today's stop is the Mayor's Office. You'll
> meet the Thermostat in Lesson 03; you'll meet Podrick everywhere.

**Why discarded:** Solid cast introduction but mild "same X" repetition
("same city, same characters, same world"). Closing forward-pointers
read as a checklist. Loses the visual anchor to the map graphic the
reader has just seen. Draft D pulls the cast structure from this one
but tightens the language and adds the map anchor.

#### Draft B — Why-first, motivational

> You'll notice every lesson opens with a stop somewhere in K-Town.
> That's not whimsy — it's a working agreement. The Kubernetes ecosystem
> invents its own metaphor for almost every concept (pods, captains,
> controllers, schedulers), and beginners burn cognitive energy spinning
> up a new mental model every chapter. K-Town is one shared city where
> every concept lives in its own district, and three characters keep
> showing up: **Mayor Katie** (the city manager — that's Kubernetes),
> **Podrick** (the unit being placed — a *Pod*), and **The Thermostat**
> (the wise old gadget explaining feedback loops). Same world, every
> lesson. Your first stop is Katie's office.

**Why discarded:** Strongest *explanation* of the why — actually engages
the cognitive-tax framing the K-Town decision was built on, which is
the deepest possible defense of the universe. But two failures: (1)
the lead "You'll notice every lesson opens with…" assumes the reader
has already seen multiple lessons, which is wrong on Lesson 1 — they're
opening their *first* lesson and have noticed nothing yet. (2) "That's
not whimsy — it's a working agreement" reads as defensive ("we're
explaining ourselves") rather than confident framing. The brand
promise is that K-Town just *is* the universe; preemptively defending
it tells the reader to be suspicious. Draft D drops the defense.

#### Draft C — Tour-guide voice, map-anchored

> 📍 **You're starting at the Mayor's Office** — the slate pin in the
> centre of the map above. Every lesson in this course visits one
> district of K-Town, and the same three characters keep showing up:
> **Mayor Katie** running the city (she *is* Kubernetes), **Podrick**
> the box that gets placed (a *Pod*), and **The Thermostat** — the wise
> gadget on every wall, who'll explain how things keep themselves
> running starting Lesson 03. Same city, every lesson. Today, Katie.

**Why discarded** (it nearly won): Strongest *visual anchoring* — the
"slate pin in the centre of the map" reference points the reader at
the thing they just saw. Tour-guide voice is consistent with the
K-Town conceit. "Today, Katie" closer lands. Risk: introduces "Pod"
with just `(a *Pod*)` and no forward pointer — a beginner who doesn't
yet know what a Pod is gets a parenthetical they can't fully cash.
Draft D inherits Draft C's voice and map anchor but adds the
"Lesson 15 goes deep" forward pointer for Pod and a "first speaking
part, Lesson 03" pointer for the Thermostat — gives curious readers
where to follow each character.

### Self-critique on the winner (Draft D)

What works: tour-guide voice, map anchor ("slate pin in the centre"),
named cast with forward pointers, "Today: Katie" closer. ~95 words —
a frame, not a lesson, per STYLE.md "Do not let the city framing crowd
the actual content."

What's mediocre: the "(first speaking part, Lesson 03)" parenthetical
is slightly jokey — could read as cute rather than informative.
Acceptable risk; the playfulness is consistent with the rest of the
K-Town conceit (the Thermostat is itself a slightly grandfatherly
character per STYLE.md).

What I'd change with one more revision: nothing — this is the right
balance for the slot. If the founder pushes back on tone, swap "first
speaking part" → "first appears" for a more neutral register.

Ship-ready: yes.

---

## 2026-05-02 — L01 K-Town meta explainer (the why-K-Town pre-lesson aside)

**Accepted:** Draft D (synthesis), placed at top of L01 between the
district line and the K-Town universe intro. See DECISIONS.md
"L01 K-Town meta explainer" entry for the live copy.

### Drafts not chosen

#### Draft A — Friendly + concrete examples

> 🏙 **Why we built K-Town.** Kubernetes has a lot of jargon — Pods,
> controllers, kubelets, sidecars, schedulers, the API server, on and on.
> Each one is its own concept, and trying to learn them as raw vocabulary
> is exhausting. So we built **K-Town**: a stylised city where every
> Kubernetes concept is a place or a person you can picture. Want to know
> what a Pod is? Visit the Co-Living Quarter. Curious about how Kubernetes
> makes decisions? Stop by the Mayor's Office. Same city every lesson,
> same characters keep showing up, same rules. By Lesson 5 you'll have a
> mental map of Kubernetes that fits on a postcard. That's the trick.

**Why discarded:** Friendliest tone, names a concrete payoff ("mental
map that fits on a postcard"). But the concrete examples leak future
districts the reader hasn't met yet — "Co-Living Quarter" is L15, far
away — and "Visit the X to learn about Y" is a CTA the page can't
fulfill (the lesson navigation doesn't yet exist; readers have to
manually open other lessons). Risk of disorienting the very
first-time reader the explainer is for.

#### Draft B — Explicit "most tutorials do X, we do Y"

> 🏙 **About K-Town.** Most Kubernetes tutorials hit you with a wall of
> new vocabulary on day one — Pods, controllers, the API server, kubelets,
> sidecars, schedulers — and ask you to absorb each one as an abstract
> technical term. We took a different approach. We built a stylised city
> called **K-Town** and mapped every Kubernetes concept onto a place or a
> person inside it. The whole course is a tour: each lesson visits one
> district, learns what happens there, and connects it back to the wider
> city. By the end you'll have a single coherent mental picture of
> Kubernetes — one map of one place — instead of a vocabulary list with
> 60 disconnected entries. That's how K-Town makes the learning stick.

**Why discarded:** Strongest *contrast framing* — actually explains the
pedagogical choice by naming what other tutorials get wrong. But the
"Most Kubernetes tutorials hit you with…" lead is comparative and
slightly defensive; it tells the reader "we know what you've been
through" before the reader has even started. For a first-time reader
who hasn't tried other tutorials, the comparison falls flat. Draft D
keeps the substance (jargon is exhausting; concrete map is the answer)
without comparing.

#### Draft C — Confident "first, a word about K-Town"

> 🏙 **First, a word about K-Town.** Kubernetes is a big system with a
> lot of moving parts, and most people learning it for the first time get
> drowned in vocabulary — Pods, controllers, kubelets, sidecars,
> schedulers — before they can build a picture of what's happening. So we
> built one for you. **K-Town is a stylised city**, and every Kubernetes
> concept lives somewhere in it. Each lesson is one stop on a tour of the
> city. You'll learn the place (the analogy), then the technical name for
> it (the K8s term). By the end of the course you won't have memorised 60
> disconnected terms — you'll have walked a city you know. That's the
> whole framing.

**Why discarded** (it nearly won): Tightest of the three. "First, a
word about K-Town" is a confident, self-aware lead. "Walked a city you
know" is the strongest closer in any draft. But misses one thing the
synthesis adds: a navigational pointer telling the reader what's about
to happen on the page next ("the map below… the panel under it
introduces the recurring characters"). Without that pointer, the
reader doesn't know the cast intro is coming and might think the meta
block IS the framing — and then encounter the cast block as a
duplicate. Draft D inherits Draft C's voice and tightens further.

### Self-critique on the winner (Draft D)

What works: three short paragraphs in a why → how → payoff arc.
"Walked a city you know" closer (borrowed from Draft C). Explicit
navigational pointer at the end ("the map below… the panel under it
introduces the recurring characters. From there, the lesson begins.")
— layman-first signal that signposts what the reader is about to see.

What's mediocre: "60 disconnected terms" is a slightly arbitrary
number — the K8s vocabulary canon list in STYLE.md has 7 canonical
terms, the lesson-15 mapping had 15 rows, and the full course
vocabulary is more than 60 but not exactly. The number is rhetorical,
not a count. Acceptable.

What I'd change with one more revision: nothing. The structure is
why-built-K-Town → how-K-Town-works → what-the-payoff-is →
what-comes-next-on-this-page. Each paragraph is one move. Ship-ready.

Ship-ready: yes.
