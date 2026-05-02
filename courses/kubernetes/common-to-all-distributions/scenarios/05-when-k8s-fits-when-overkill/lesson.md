# Lesson 05 — When Kubernetes Is Useful, and When It's Overkill

> Course: Kubernetes — Common to all distributions
> Lesson 05 of 17 in K-COM. The honest "should we adopt this?" lesson.
> Companion preview: `/preview-kubernetes-lesson-05.html`.

---

## 1. Concept

Kubernetes is enormously powerful — and that power has a real operational
cost. The cluster itself is a small project to keep healthy: upgrades,
observability, security patches, on-call. That cost is fixed regardless of
how big or small your workloads are.

**Kubernetes pays back when:** you run many services across many teams,
your workloads are dynamic (scale up and down, get rescheduled), you need
workload portability across clouds and environments, and you have the
engineering capacity to operate the cluster itself.

**Kubernetes is overkill when:** you have a single small application that
rarely changes, no platform engineering capacity, latency-sensitive
sub-millisecond workloads, or your real pain is application architecture
not orchestration. Moving a bad app to Kubernetes makes it a bad app on
Kubernetes.

The honest summary: *Kubernetes solves operational scale and heterogeneity.
If you don't have either, you don't need it — and adopting it costs you
more than it gives you.*

---

## The 6-question fit-checker

1. **Will you run 5+ services within 12 months?** Yes → fit grows. No → managed app platform (Render, Fly, Heroku, ECS Fargate).
2. **Do 2+ teams share infrastructure?** Yes → strong fit (namespaces + RBAC). No → simpler tools.
3. **Do workloads scale up & down dynamically?** Yes → great fit (HPA/VPA + cluster autoscaler shine). No → not a strong driver.
4. **Do you need workload portability?** Yes → big advantage (same manifests on EKS/AKS/GKE/on-prem). No → cloud-native single cloud is fine.
5. **Do you have platform engineering capacity?** Yes → adopt confidently. No → DON'T adopt yet (cluster ops without staff = burnout).
6. **Are workloads sub-millisecond latency-sensitive?** Yes → consider alternatives (HFT/RTB pay K8s networking cost). No → no concern.

Three or more "yes" answers and Kubernetes is likely a strong fit. Three
or more "no" and you should look at simpler alternatives first.

---

## 2. Before / After

**Before — year 1 startup.** 3 engineers, 1 service, 1 database. Total
operational time: 2 hours per week. Adding Kubernetes here would add 10
hours per week of cluster maintenance, training, debugging, on-call — for
zero benefit. Right answer: managed app platform (Render, Fly, Heroku) or
single VM with systemd.

**After — year 3 same company.** 40 engineers, 8 services, 4 teams each
wanting independent deploys, 3 environments, traffic scaling 10× daily.
Now ad-hoc tooling is the bottleneck — every team reinvents deploys
differently. Right answer: managed Kubernetes (EKS/AKS/GKE) plus a small
platform team. The cluster cost pays for itself in operational
standardization.

What didn't change: Kubernetes never makes one service simpler. It pays off
only when the *count* of things to operate becomes the bottleneck.

---

## 3. Analogy — industrial kitchen vs the toaster on your counter

Imagine you walk into a professional industrial kitchen. Six chefs, twelve
burners, four ovens, walk-in fridges, prep stations, plating stations, an
expediter calling tickets, a head chef coordinating, dishwashing crew,
ventilation, refrigeration, fire suppression, written service standards.
When you're feeding 800 people for a wedding, you need this. Every piece
of that complexity is doing real work.

Now imagine you're making yourself toast in the morning. You need a
toaster and a counter. If someone built you an industrial kitchen for your
toast, the kitchen would consume more attention than the toast itself.
The kitchen isn't bad — it's *wrong* for the use case.

The question isn't "is Kubernetes good?" Of course it's good. The question
is "are you in the wedding-catering situation, or the morning-toast
situation?"

**Mapping:**

- Industrial kitchen = Kubernetes (powerful platform with rich tooling)
- Many cooks = many teams sharing infrastructure
- Many ovens = many services running concurrently
- Service standards & expediter = consistency, observability, automation
- Toaster = a managed app platform (Render, Fly, Heroku, App Runner)
- "Wrong tool" = building a kitchen for toast (or running K8s for one app)

---

## 4. ELI5 / ELI10

**ELI5.** A big restaurant kitchen with many ovens and many cooks is
amazing if you're feeding hundreds of people. It's silly if you're making
one piece of toast. Kubernetes is the big kitchen. Sometimes you need it;
sometimes you don't.

**ELI10.** Kubernetes is a *platform* — software for running lots of
services across many machines, with deployment, scaling, restarts,
secrets, networking, observability all standardized. When you have lots
of services and multiple teams, that standardization is gold; you don't
want every team inventing their own deploy script. When you have one
service, the platform itself becomes work — you spend time keeping the
cluster healthy instead of building product. A useful test: count the
services you'll deploy and the teams that own them. Below ~5 services and
~2 teams, simpler tools usually win. Above that, the per-service cost of
Kubernetes drops sharply.

---

## 5. Real-world scenarios

**Mid-size media company · 40 services · 6 teams (CLEAR FIT).** Spent 5
years on a custom Capistrano deploy from 2014. Each team's deploys broke
differently. Migrated to managed Kubernetes (EKS) over 6 months: collapsed
40 deploy scripts into one Helm pattern, replaced 6 staging setups with
namespaced previews. Six months in, deploys took 80% less time and platform
engineers shifted to developer-experience work. The investment paid back
inside one year.

**4-engineer fintech · 1 core service + 1 worker (WRONG FIT).** Adopted
Kubernetes "because it's the modern way." Spent a year on cluster ops:
upgrades, observability, security patches, certificate rotation. Shipped
fewer features than they would have on simpler tools. Eventually moved to
ECS Fargate and kept Kubernetes only for the one service that justified
it. Recovered velocity in ~3 months.

**Government agency · citizen portal · compliance-heavy (FIT).** Needed
strict isolation between dev/staging/prod and an audit trail of every
change. Kubernetes gave them per-environment clusters, RBAC for who can
touch what, GitOps so every change has a Git commit, and policy
enforcement via admission controllers. Compliance audits went from a
1-week scramble to "send the auditor a link to the Git repo."

**High-frequency trading firm · sub-millisecond paths (WRONG FIT for the
core).** Trading engine needs sub-100µs latency end-to-end. Kubernetes'
networking adds 50-200µs per pod hop. Manageable for normal HTTP; lethal
for HFT. They run the core engine on bare metal with kernel-bypass
networking (DPDK), and use Kubernetes only for non-latency-critical
services (dashboards, batch analysis, monitoring). Right tool for each
job.

---

## 6. Animated illustration

Three modes in the preview animation:

1. **Tiny (1 app on the cluster).** Most of the cluster is overhead.
   Payback ×0.2 — overkill.
2. **Mid (8 services).** Cluster overhead amortizes. Payback ×3.5 — strong fit.
3. **Big (40 services).** Cluster densely packed. Each marginal service
   nearly free to add. Payback ×9.4 — excellent fit.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
