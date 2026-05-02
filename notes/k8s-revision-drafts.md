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
