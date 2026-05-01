# Lesson 01 — How does Kubernetes know to fix things on its own?

> Course: Kubernetes — Common to all distributions
> Lesson 01 of the K-COM track. Module 1, Part 1.
> Format: single-concept lesson, drawn-metaphor (thermostat).
> Companion preview: `/preview-kubernetes-lesson-01.html`.

---

## The promise

Kubernetes works exactly like the thermostat in your house. You set what you
want, it reads what is, and it closes the gap forever. Once you see that, the
rest of Kubernetes is variations on the same loop.

---

## 1. Concept

A reconciliation loop is a small program that does one thing forever: it reads
what you said you wanted, looks at what actually exists, and makes a small
change to close the gap. Then it does it again. The thermostat in your house
is the most familiar example — you set the dial, it reads the room, it fires
the furnace when there's a gap, it stops when the gap is closed, and it
keeps watching for the next gap.

Kubernetes is a building full of thermostats. The Deployment thermostat
watches "how many copies of this app should exist." The Node thermostat
watches "is this machine still healthy." The Job thermostat watches "did
this batch task finish." Each one runs its own loop on its own resource,
forever.

---

## 2. Before / After

**Before.** A Saturday at 3 AM. A cloud server reboots itself for maintenance
and the app on it doesn't come back up. The on-call engineer wakes up to
error pages, drives to a coffee shop, spends six hours bringing the system
back. They lose the weekend.

**After.** Same time, six months later. The cloud machine rotates out at
3 AM. The Kubernetes thermostat notices within 30 seconds that one copy is
missing. It starts a new copy on a different machine. The on-call engineer
wakes up to a calm Slack message: *self-healed at 3:14 AM — no action needed.*

What did not change: things still break. Machines still die. The 3 AM event
still happens. What changed is *who* deals with it (a tiny program watching
forever) and how long it takes (seconds, not hours).

---

## 3. Analogy — the thermostat

You set the dial to 21°C. That is the desired state. The thermostat reads the
room — say it's 18°C. That is the actual state. It computes the difference
(a 3°C gap) and runs the heater — the controller action. It keeps reading the
room. When the room hits 21°C, the heater stops. When the room cools again,
the heater fires again.

The thermostat never declares victory and walks away. That's the entire
analogy. Kubernetes is a building full of thermostats, one per kind of
resource.

---

## 4. ELI5 / ELI10

**ELI5.** A thermostat watches the room and turns the heater on when it's
too cold and off when it's warm enough. It never stops watching. Kubernetes
is a building full of tiny thermostats — one watches "how many copies of this
app are running," another watches "is this computer still alive." When
something doesn't match what you asked for, the thermostat fixes it.

**ELI10.** A reconciliation loop is a small program that reads desired state,
observes actual state, and takes the minimum action to close the gap, on
repeat. The Deployment controller does this for replica count: if you said
three replicas and one died, it creates a fourth pod to bring the count back
up. The Node controller does this for node health: if a node hasn't checked
in for a while, it marks it unschedulable and lets other controllers move
the pods elsewhere. This is why Kubernetes survives node failures and pod
crashes — nothing is "set up once and forgotten."

---

## 5. Real-world

A small SaaS team ran their app on a cloud VM. Every quarter they lost a
weekend to "the VM rebooted and the app didn't come back." After moving to
Kubernetes, that pattern stopped. The reconciliation loop replaced the
on-call page.

A separate idea worth mentioning: people talk about servers two ways —
as **pets** (named, hand-tuned, irreplaceable) or as **cattle** (identical,
numbered, interchangeable). Kubernetes treats every machine as cattle, which
is what makes "lose one, replace it automatically" possible. And Kubernetes
configuration is **declarative** (here's a photo of the dish I want) instead
of **imperative** (here are the 47 steps to make it). Both ideas exist
specifically because the reconciliation loop demands them.

---

## 6. Animated illustration

The lesson preview's hero is an interactive thermostat. Drag the orange dot
around the dial to set the desired temperature. Watch the furnace fire when
there's a gap. Click "open a window" to force the room to cool — the
thermostat keeps fighting it forever. That is the lesson, made visible.

A separate Kubernetes-specific animation lives at `animation.html` showing
the same loop with K8s vocabulary in three modes: scale-up, self-heal on
failure, drift correction. Use it after the thermostat lands.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (5 cards) and `quiz.yaml` (3 pause-the-thermostat
questions).

---

## What did NOT make this lesson (deliberately)

The original Module 1 outline included twelve-factor apps, microservices vs
modular monoliths, when Kubernetes fits and when it doesn't, GitOps, platform
engineering, SRE, service ownership, multi-tenancy, the Borg → Omega → K8s
lineage, CNCF, release cadence, KEPs, and feature gates. All of these are
real and worth teaching — but cramming them into Lesson 01 fails first-timers
even when each is well-written.

The redesign moves them to dedicated lessons in Module 1:

- **Lesson 02:** Apps that fit pods (twelve-factor + microservices vs modular monoliths).
- **Lesson 03:** When Kubernetes is the right tool (and when it isn't).
- **Lesson 04:** How mature teams operate Kubernetes (GitOps + platform engineering + SRE + service ownership + multi-tenancy).
- **Lesson 05:** Where Kubernetes came from and how it ships (Borg → Omega → K8s, CNCF, release cadence, KEPs, feature gates, conformance).

Then K-COM Module 2 (Containers) opens the box on what runs inside a pod.

---

## Self-critique notes (per QUALITY.md)

- **Analogy:** Thermostat is structural. Dial = desired, thermometer = actual,
  brain = controller, furnace firing = controller action. Survives every
  follow-up question I can throw at it ("what's a node failure?" → "an open
  window"; "what's a Deployment?" → "a different number on the dial").
- **Glossary placement:** Moved to footer. Vocabulary appears inline only
  after the metaphor lands.
- **Visuals:** Drawn metaphors only — actual thermostat with dial, actual
  house cross-section with furnace, actual cute pets and cattle with faces,
  actual recipe scroll vs photo of dish. No block diagrams.
- **Density:** ~8 sections, ~5 minute reading time + ~5 minute interactive.
  Down from the original ~60 content blocks.
- **First-time-learner test:** Lesson opens with a question ("how does
  Kubernetes fix things on its own?"), interactive widget answers it
  visually before any vocabulary. Lesson ends with the learner curious
  about Lesson 02, not exhausted.
