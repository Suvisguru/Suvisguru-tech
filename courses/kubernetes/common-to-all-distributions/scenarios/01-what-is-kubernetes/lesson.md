# Lesson 01 — What is Kubernetes?

> Course: Kubernetes — Common to all distributions
> Lesson 01 of 17 in K-COM. The foundation lesson.
> Format: standard 7 PROJECT.md sections.
> Companion preview: `/preview-kubernetes-lesson-01.html`.

---

## 1. Concept

Kubernetes (often shortened to K8s — the "8" is for the eight letters between
K and s) is software that runs and manages your applications across many
computers at the same time. You give it a description of what you want — for
example, "I want three copies of my web app running" — and Kubernetes figures
out which computers to run them on, watches them, restarts them if they crash,
and adds more copies when you ask for them.

It runs on top of a group of computers called a cluster. A cluster can be
three computers in a closet, or thousands of machines spread across data
centres. Kubernetes treats them as one big pool of resources and decides
where each piece of your app should live.

It exists because modern apps stopped fitting on a single computer. Companies
need to run hundreds of services across many machines, with traffic that goes
up and down through the day, with hardware that occasionally breaks. Doing
all that by hand is impossible. Kubernetes does it automatically.

---

## 2. Before / After

**Before.** Running an app at any real scale meant SSHing into servers,
reading logs by candlelight, restarting things by hand, hoping you didn't
break something else, and documenting what you did so the next person could
find it. Scaling meant buying a bigger server. Adding a new app meant
picking a server, hoping it had capacity, and praying.

**After.** You wrote down — once, in a file — what you want running. When
something breaks, Kubernetes notices in seconds and starts a replacement
on a healthy machine. Scaling is changing one number in a file. Adding a
new app is one more file. Kubernetes places it for you, watches it, and
tells you when something needs your attention.

What didn't get easier: the app itself. Kubernetes won't fix bugs in your
code. It just makes the operations *around* your code automatic.

---

## 3. Analogy — the property manager

You own a few apartment buildings and you don't want to manage them
yourself. So you hire a property manager. You tell the manager what you
want — "keep all the apartments rented to good tenants, fix anything that
breaks, hire a plumber if there's a leak, find a new tenant if one moves
out." And then you go live your life.

The manager handles the day-to-day: showing apartments, signing leases,
calling repair people, replacing broken appliances, balancing tenants
across buildings. You don't think about which plumber to call at 3 AM.
You don't even know there was a leak.

Kubernetes is the property manager for your apps and computers.

**Mapping:**

- You = the engineering team that owns an app
- The property manager = Kubernetes
- Apartment buildings = computers (servers / VMs / cloud machines)
- Tenants = your apps (each one needs an apartment)
- The instructions you gave the manager = your YAML files
- The plumber the manager calls at 3 AM = Kubernetes restarting a crashed app

---

## 4. ELI5 and ELI10

**ELI5.** Imagine you have a lot of toys, and a lot of toy boxes. A friend
(Kubernetes) puts each toy in the right box, makes sure they all stay there,
and brings out a new toy if one breaks. You don't have to remember which toy
is in which box, or check on them. The friend just does it.

**ELI10.** Kubernetes is like a delivery dispatcher for a fleet of trucks.
You tell it what packages need to go where; it picks which truck takes each
one. If a truck breaks down, it sends another truck to finish the job. If
demand goes up, it brings in more trucks. The dispatcher never sleeps. In
Kubernetes, "trucks" are computers, "packages" are your apps, and "the
dispatcher" is Kubernetes itself. The big idea: you describe what you want;
Kubernetes figures out how. That principle (called *declarative
configuration*) is what makes auto-recovery and easy scaling possible.

---

## 5. Real-world scenarios

**A streaming media company (~200 engineers).** Runs hundreds of small
services that together stream video to millions of viewers. Before Kubernetes,
deploying a new version of any one service required a coordinated change
across dozens of servers. Now each team writes a small YAML file and merges
it; Kubernetes rolls the change out, watches for problems, and rolls back if
the new version misbehaves. Average deploy time went from "an afternoon" to
"twelve minutes."

**A regional hospital system (~30 engineers).** Runs the patient records
system, the pharmacy app, and a dozen integrations with lab equipment. The
trade-off: they get the auto-recovery and consistent deploys they need, but
they had to invest in a small platform team to keep the cluster healthy.
After 18 months, downtime is down ~70% and adding a new app takes a day
instead of a sprint.

**A fintech startup (12 engineers).** Initially tried to run everything in
Kubernetes from day one, "because it's the modern way." They spent more time
fixing the cluster than shipping features. After a year they moved most
workloads to a managed app platform (Render, Fly) and kept Kubernetes only
for the one large service that justified it. Lesson: Kubernetes pays back
when you have many services and many teams. With three engineers and one
app, it's overkill.

**A government agency running a citizen portal.** Needed strict isolation
between environments (dev, staging, production) and an audit trail of every
change. Kubernetes gave them per-environment clusters, RBAC for who can touch
what, and Git-tracked deploys. Compliance audits went from a one-week
scramble to "send the auditors a link to the Git repo."

---

## 6. Animated illustration

The lesson preview's animation shows three modes:

1. **Place an app.** Your request flows from "you" through the Kubernetes
   wheel and lands on a server. K8s picked the server with capacity.
2. **Recover from failure.** An app is happily running on server-b.
   Server-b crashes. Kubernetes notices, picks server-c, moves the app
   there. You stayed asleep.
3. **Scale up to 3 copies.** You change the file from 1 copy to 3.
   Kubernetes spreads the three copies across three servers.

The wheel in the middle is Kubernetes; the boxes on the right are your
servers. Watch what happens to the app.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 quiz questions).

---

## Self-critique notes (per QUALITY.md)

- **Analogy:** Property manager → apartment buildings → tenants → plumber.
  Maps cleanly: you, K8s, computers, apps, restarting a crashed app.
- **Concept density:** No K8s jargon beyond "cluster" and "YAML" — both
  defined inline. Words like "controller," "pod," "deployment," "scheduler"
  are deferred to later lessons.
- **Visuals:** One focused illustration per section. Friendly characters
  with simple faces. Drawn metaphors, not block diagrams.
- **First-time-learner test:** Lesson opens with the question "what is
  Kubernetes?" — answers it visually in the hero illustration before any
  explanation begins. Closes with curiosity about Lesson 02 (Virtualization
  vs Containerization).
