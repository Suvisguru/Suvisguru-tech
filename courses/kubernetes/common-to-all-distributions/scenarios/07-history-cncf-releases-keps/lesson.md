# Lesson 07 — Kubernetes History · CNCF · Releases · KEPs · Feature Gates

> Course: Kubernetes — Common to all distributions
> Lesson 07 of 17 in K-COM. **Module 1 final lesson** — how Kubernetes
> evolves as a project.
> Companion preview: `/preview-kubernetes-lesson-07.html`.

---

## 1. Concept

Kubernetes didn't appear out of nowhere. It descended from systems Google
had been running for over a decade, and it's developed today by hundreds
of contributors at hundreds of companies through a formal process. Five
foundational topics about how Kubernetes evolves as a project:

**Lineage.** Borg → Omega → Kubernetes. Borg was Google's internal
cluster manager from the early 2000s; the Borg paper was published in
2015. Omega was a research successor (paper 2013). Kubernetes was
open-sourced in June 2014 and reached 1.0 in July 2015. The name is Greek
for "helmsman"; "K8s" is K + 8 letters + s.

**CNCF.** The same month Kubernetes hit 1.0 (July 2015), it was donated
to the Cloud Native Computing Foundation — a Linux Foundation project
hosting vendor-neutral cloud-native open-source projects. Kubernetes
became the CNCF's first graduated project in March 2018. The CNCF now
hosts hundreds of projects (Prometheus, Envoy, Helm, Argo, etc.).

**Release cadence.** Kubernetes ships roughly 3 minor releases per year
(it was 4/year through 2022, slowed to 3/year in 2023). Each minor
release is patched for ~14 months — 12 months of active patches plus a
2-month EOL transition. The most recent 3 minor versions are actively
patched at any time.

**KEPs.** Kubernetes Enhancement Proposals — the formal change-management
process. Any non-trivial change goes through a KEP: a markdown document
in github.com/kubernetes/enhancements, reviewed by the relevant SIG
(Special Interest Group), tracked through stages.

**Feature gates.** Per-feature on/off flags. Each feature progresses
through three stages: **Alpha** (off by default, may break or be removed),
**Beta** (since 1.24+, new beta features are off by default; API may
still change), **GA / Stable** (on by default, backward-compatibility
guaranteed, removal needs multi-release deprecation).

**Conformance.** The CNCF Certified Kubernetes program. Distributions
that pass the test suite (run via `hydrophone`, historically `sonobuoy`)
can call themselves "Certified Kubernetes." Vendor-specific features sit
outside conformance — they're product additions, not the standard.

---

## Alpha · Beta · GA in detail

| Stage | Default | Stability | Production? |
|-------|---------|-----------|-------------|
| **Alpha** | OFF (must enable) | may break / change | NO · dev/test only |
| **Beta** | OFF for new betas (since K8s 1.24) | mostly stable, may still tweak | CASE BY CASE · vet first |
| **GA** | ON by default | backward-compatible, guaranteed | YES · default for production |

Production rule: **use GA features only**. Vet beta case-by-case. Reserve
alpha for dev/test clusters.

---

## 2. Before / After

**Before — 2014.** Running containers at scale meant either home-grown
shell scripts or one of several competing systems: Borg (Google
internal), Mesos + Marathon, Docker Swarm, Nomad, CoreOS fleet. Each had
its own API. Each had its own community. Workload portability across
clouds was a custom integration job per cloud.

**After — today.** Kubernetes is the standard. Every major cloud provides
a managed Kubernetes service (EKS, AKS, GKE) with the same upstream API.
Workload portability is roughly real — same manifests work across clouds.
The CNCF landscape has hundreds of projects, but Kubernetes is the spine.

What didn't get easier: Kubernetes is not simple. Its API surface is
enormous, conformance only covers the API not the operational reality,
and distributions still vary in defaults, networking, storage, and
security.

---

## 3. Analogy — train-line testing for new signals

When a railway introduces a new signal system, they don't switch the
entire intercity network at once. They test on a quiet branch line first,
where breakage is acceptable and few passengers are affected. Once the
signal works there, they roll it out to a moderately busy line — more
traffic, more learning. Once that's proven, they finally enable it on the
main intercity routes where millions of passengers depend on it.

By the time you ride the main line, the signals are *boring on purpose*.
They've been observed long enough to be predictable. The reason intercity
travel feels safe is precisely because the signals were tested somewhere
quiet first.

Kubernetes feature gates work exactly the same way. Alpha is the branch
line: things break, that's the point. Beta is the moderately busy line:
most things work, but the railroad tells you "we may still tweak the
signal pattern." GA is the main intercity line: stable, predictable, and
removing a signal requires its own multi-year process.

**Mapping:**

- Quiet branch line = alpha
- Moderately busy line = beta
- Main intercity line = GA / Stable
- Railroad's signal-testing process = KEPs (Kubernetes Enhancement Proposals)
- Signal designers = SIGs (Special Interest Groups)
- Operating standards body = the CNCF and the Kubernetes project

---

## 4. ELI5 / ELI10

**ELI5.** Kubernetes is a tool that lots of people work on together. When
they want to add something new, they try it carefully in a tiny test
version (alpha), then in a slightly bigger version (beta), and only then
put it in the real version everyone uses (GA). This is like testing a
new train signal on a quiet train line before using it on the busy ones.

**ELI10.** Kubernetes started inside Google as a project called Borg,
then a research version called Omega, then the open-source Kubernetes
(2014). It's now run by the Cloud Native Computing Foundation (CNCF),
and developed by hundreds of contributors. New features go through a
formal process called a KEP and graduate through three stages — alpha
(off, unstable), beta (off-by-default for new features, mostly stable),
GA (on-by-default, backward compatible). Three minor releases per year,
each supported for ~14 months. The CNCF runs a "Certified Kubernetes"
conformance program so distros (EKS, AKS, GKE, OpenShift) all behave the
same at the API level.

---

## 5. Real-world scenarios

**Platform team's "GA only in prod" rule.** A platform team standardised
on "we ship workloads against GA APIs only." This rule meant they were
never burned by a beta change between K8s 1.27 and 1.28 (when
InPlacePodVerticalScaling changed shape during beta), but they did wait
an extra year to use Gateway API in production until v1 GA. Their
neighbour team made the opposite call (run alpha aggressively) and spent
two on-call weeks rebuilding workloads when an alpha API was renamed in
a minor release.

**"Kubernetes-compatible" vs "Certified Kubernetes."** A team picked a
cheap distribution that called itself "Kubernetes-compatible." Six months
in, they hit a feature that worked on EKS but not on this distribution —
the distribution had skipped some less-common API endpoints. Manifests
had to be rewritten. They migrated to a Certified Kubernetes distribution
and the issue went away. Lesson: "Certified Kubernetes" is a real CNCF
program with a real test suite (run via hydrophone). "Compatible" is a
marketing term.

**Tracking KEPs to plan a year ahead.** A senior platform engineer at a
large enterprise reads every KEP that gets accepted. He keeps a roadmap
of "features that will be GA in K8s 1.30," "features still in alpha but
worth watching," and "features being deprecated." This lets the platform
team know — months in advance — what'll change and what'll be removed.

**Quarterly K8s upgrade cadence.** An ops team upgrades production
clusters every 4 months — one minor version at a time. They never skip
versions and never run the latest version in prod — they wait one minor
release for "early adopter pain" to be reported and patched. So: latest
minor in dev/staging, minus-one in production.

---

## 6. Animated illustration

Four modes in the preview animation:

1. **Alpha.** Stage badge red. Off by default. May break/vanish. ~10% adoption (early adopters in dev clusters).
2. **Beta.** Stage badge gold. Off for new betas (since K8s 1.24). Mostly stable. ~40% adoption.
3. **GA.** Stage badge green. On by default. Backward compatibility guaranteed. ~90% adoption (everyone uses it).
4. **Full lifecycle.** Cycles through alpha → beta → GA every 3 seconds, showing the graduation visually.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
