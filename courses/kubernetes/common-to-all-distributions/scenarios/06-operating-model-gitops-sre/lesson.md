# Lesson 06 — GitOps · Platform Engineering · SRE · Service Ownership · Multi-Tenancy

> Course: Kubernetes — Common to all distributions
> Lesson 06 of 17 in K-COM. How mature teams operate Kubernetes day-to-day.
> Companion preview: `/preview-kubernetes-lesson-06.html`.

---

## 1. Concept

Once you have Kubernetes installed, the next question is bigger than the
technology itself: *how do we run it as a team, day after day, without it
becoming a mess?* Mature organizations converge on five interlocking
practices.

**GitOps** moves the source of truth to a Git repository. An automated
agent in the cluster watches Git and reconciles. Same loop pattern as a
Kubernetes controller, just with Git as the desired state. Tools: **Argo
CD**, **Flux CD**. Coined by Weaveworks (Alexis Richardson, 2017). Four
formal principles per [opengitops.dev](https://opengitops.dev):
declarative, versioned and immutable, pulled automatically, continuously
reconciled.

**Platform engineering** is the discipline of building an internal
platform — a "paved road" — that product teams consume. The platform team
owns Kubernetes, observability, secrets, CI/CD, ingress; product teams
ship apps onto it via a thin interface. Codified in the Team Topologies
book and the platform-engineering community of the late 2020s.

**SRE** (Site Reliability Engineering) is Google's operating model from
the 2016 SRE Book. Defines reliability with **SLIs** (indicators), **SLOs**
(objectives), **SLAs** (agreements); spends an **error budget** on
velocity until reliability drops. Treats infrastructure as a software
problem.

**Service ownership** ("you build it, you run it") puts the team that
wrote the service on its on-call rotation. Aligns incentives toward
reliability without bureaucratic enforcement.

**Multi-tenancy** is sharing one cluster (or platform) across multiple
teams or customers. Soft = trust between tenants, isolation by namespace +
RBAC + quotas. Hard = no trust, separate clusters or virtual clusters
(vCluster) + node isolation + strict admission policy.

These five compound. None is a Kubernetes feature; all are practices
Kubernetes *enables*.

---

## 2. Before / After

**Before — ops as ticket queue.** Operations is a separate ticket queue.
To deploy, a developer files a ticket; the ops team patches a server, runs
a script, closes the ticket. When the system breaks at 3 AM, ops gets
paged — the developer doesn't. Knowledge of how things actually run lives
only in ops. Developers ship code blind. Ops burns out. Velocity falls.

**After — platform + ownership.** The platform team builds and runs the
cluster + observability + secrets + CI/CD. Product teams own their
services end-to-end: write the YAML, commit to Git, agent reconciles,
they're on the rotation when their service pages. SRE practices measure
reliability. Service ownership aligns incentives. Multi-tenancy keeps
teams isolated. The org scales without the ops queue scaling.

What didn't change: people still need to be on call. Software still breaks.
The 3 AM page still happens. What changes is *who* answers it (the team
that owns the code) and *how* it gets fixed (with the same tools and
observability the team uses every day).

---

## 3. Analogy — the well-run library

Imagine a public library. Every change to the shelves starts with a card
written in the catalog. A librarian reads new cards and walks to the shelf
to make the change. Nobody walks past the librarian and rearranges
books — and if they do, the librarian notices the drift and puts the
books back the way the catalog says.

Different sections (Fiction, Reference, Periodicals) are tended by their
own staff who know that section deeply. The head librarian watches
statistics — books misshelved per day, late returns, complaints — and
decides how much risk the library can absorb this quarter. Schools,
scholars, and the public all share the same building, separated by reading
rooms, by hours, by privileges.

Kubernetes orgs converge on this exact shape.

**Mapping:**

- The card catalog = Git (source of truth for every change)
- The librarian = the GitOps controller (Argo CD / Flux)
- The library building & reading rooms = the platform team's paved road
- The section-owning staff = product teams owning their services and on-call rotations
- The head librarian = SRE practice (measuring reliability with SLIs/SLOs/error budgets)
- Schools, scholars, public sharing the building = multi-tenancy

---

## 4. ELI5 / ELI10

**ELI5.** Think of a really good library. Every book change starts with a
written card in the catalog. A librarian reads the cards and moves the
books. Different sections have their own helpers who know their books
well. The head librarian watches how things are going. And lots of
different people use the library at the same time without bumping into
each other. Kubernetes is run by teams that work like this library.

**ELI10.** Five practices that compound. **GitOps**: Git is the source of
truth, an agent in the cluster reconciles the cluster to match Git — same
loop pattern as a Kubernetes controller. **Platform engineering**: a
platform team builds the paved road (cluster, observability, secrets,
CI/CD); product teams ship apps onto it. **SRE**: measure reliability
with SLIs/SLOs, spend an error budget on shipping velocity. **Service
ownership**: the team that built it is on-call for it. **Multi-tenancy**:
namespaces + RBAC + quotas for trusted tenants; separate clusters or
vCluster for untrusted. None of these is a Kubernetes feature; they're
all practices Kubernetes *enables*.

---

## 5. Real-world scenarios

**Retail company adopts Argo CD across 20 product teams.** Pre-GitOps,
average production change took 2 days from commit to live and required
three approvals. Post-GitOps (Argo CD), the same change took 14 minutes
via PR merge. Platform team published a paved-road template — Helm chart +
Argo Application + ServiceMonitor + AlertmanagerConfig — and any new
service got all of those for free. Two years later they introduced soft
multi-tenancy: each team got its own namespace, ResourceQuotas,
NetworkPolicies, and an Argo Project scoped to its repos.

**SaaS company introduces error budgets — finally shipped less.** A
30-engineer SaaS team kept missing their 99.9% availability target. They
formally adopted SRE practices: defined SLIs, set SLOs, tracked error
budget burn. When they hit 50% of budget burned in week 1, they froze new
feature rollouts and spent the week fixing the unstable database
connection pool. Within 6 months, they were comfortably hitting their SLO
and shipping faster on average — because they no longer needed to fix the
same outages over and over.

**Fintech moves to "you build it, you run it."** A 50-engineer fintech
moved from a centralized ops team to per-team on-call. Initial reaction:
developer protest. Six months later: bug fix turnaround was 70% faster
(because the team that owned the code was paged). On-call load was
actually lower than expected (because product teams started writing better
tests, runbooks, health checks — they were the ones being woken up).
Reliability emerged from incentive, not from process.

**University cluster shared across 12 research labs.** A research
computing platform serves 12 different research labs. Different labs have
different trust levels (some run code from external collaborators), so the
platform uses a mix: trusted labs get namespaces with RBAC + quotas (soft
tenancy); untrusted labs get a vCluster (hard tenancy, separate API
server, isolated). Both models share the same physical cluster underneath,
dramatically reducing cost compared to one cluster per lab.

---

## 6. Animated illustration

Three modes in the preview animation:

1. **GitOps normal flow.** Git declares replicas: 3, cluster has 3 pods.
   Engineer commits "replicas: 5" to Git. Controller observes the gap,
   pulls the new state, creates 2 new pods. Cluster matches Git.
2. **Drift correction.** Steady state at 3 pods. Engineer SSHes in and
   hand-scales to 5. Controller detects drift (cluster ≠ Git). Reverts
   the hand-edit back to 3 pods. Lesson: Git is the only path that
   survives.
3. **New service onboarded.** Team C is new. Opens a PR with a
   paved-road template. PR merged. Controller creates Deployment +
   Service + Ingress + ServiceMonitor + AlertmanagerConfig automatically.
   Time from PR-open to production: 14 minutes.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
