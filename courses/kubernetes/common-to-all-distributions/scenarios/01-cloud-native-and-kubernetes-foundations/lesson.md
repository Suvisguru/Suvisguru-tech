# Lesson 01 — Cloud-Native and Kubernetes Foundations

> Course: Kubernetes — Common to all distributions  
> Module 1 of 17. First lesson in the K-COM track.  
> Format: per-subtopic structure (5 subtopics).  
> Fact anchors: kubernetes.io/docs, 12factor.net, github.com/cncf/landscape, github.com/kubernetes/enhancements, research.google (Borg & Omega papers).

---

## How to read this lesson

Five subtopics. Each subtopic is a complete mini-lesson — concept, before/after, analogy, quick-check, ELI5/ELI10, real-world story, flashcards, quiz. Read them in order; each builds on the last. The single thread that runs through all five is the **reconciliation loop**: Kubernetes' core idea that you describe what you want and a controller continuously moves the world toward that description.

---

## Subtopic 1 — Cloud-native principles: reconciliation, desired state, pets vs cattle

### 1.1 Concept

"Cloud-native" is a way of building software that assumes the underlying infrastructure is dynamic, that machines fail routinely, and that operators describe outcomes rather than steps. It rests on a small set of repeating ideas:

- **Immutable infrastructure.** Once a server (or container image) is built, it is never modified in place. To change it, you build a new one and replace the old.
- **Declarative configuration.** You write down what the world should look like — "I want three replicas of this app, exposed on port 80" — and submit that. You do *not* write the steps to produce it.
- **Reconciliation loops.** A controller — a small program — reads your declaration (the *desired state*), compares it to what's actually running (the *actual state*), and takes the minimum action to close the gap. Then it does it again. Forever.
- **Desired vs actual state.** These two pictures of the world are always being compared. The control plane stores the desired state. The data plane reports the actual state. Controllers live between them.
- **Pets vs cattle.** A *pet* is a hand-built server you've named, patched personally, and would mourn if it died. A *cow* is one of a thousand identical animals — when one dies, you don't grieve, you just bring in another. Cloud-native treats servers and pods as cattle.
- **Horizontal scaling.** When load grows, you add more identical replicas (scale out), not a bigger machine (scale up). Bigger machines have ceilings; replica counts don't.
- **Failure as normal.** Disks fail, machines reboot, networks partition. Cloud-native systems are designed assuming all this happens routinely; the reconciliation loop is what makes that survivable.

The reconciliation loop is the spine. Everything else in Kubernetes is a specialization of it.

### 1.2 Before / after

**Before (the imperative world).** An ops engineer SSHes into web-01, runs `apt install`, edits a config file, restarts the service, then goes home. Next quarter they SSH back in, can't remember what they changed, and the production environment has slowly drifted from documentation into a place no one can reproduce.

**After (the declarative world).** An engineer writes a YAML file: "three replicas of nginx, version 1.27, listening on port 80." They commit it. A controller reads the file, sees zero replicas exist, creates three. A node fails — actual drops to two; the controller creates a third on a healthy node. Nobody SSHes anywhere. The YAML is the source of truth.

**What did not get easier.** You still have to design the application correctly. The reconciliation loop will not save you from a buggy image, an undersized resource request, or a missing health check. The platform automates the operations *around* the application, not the application itself.

### 1.3 Analogy — the thermostat

A reconciliation loop is a thermostat.

You set the dial to 21°C. That is the *desired state*. The thermostat reads the room — say it's 18°C right now. That is the *actual state*. It computes the difference (a 3°C gap) and runs the heater (the *controller action*). It keeps reading the room. When the room hits 21°C, the heater stops. When the room cools again, the heater fires again. The thermostat never declares victory and walks away.

Kubernetes is a building full of thermostats, one for every kind of resource. The Deployment controller is a thermostat for "how many pod replicas should exist." The Node controller is a thermostat for "is this machine still healthy." The Job controller is a thermostat for "did this batch task finish." Each runs its own loop, on its own resource, forever.

### 1.4 Quick check

A team's web app needs two replicas during the day and ten at night for batch processing. Where does the *desired state* of "ten replicas" live, and what makes it actual?

- **Correct.** The desired state lives in a Kubernetes object (e.g., a Deployment's `spec.replicas: 10`). A controller observes the desired vs actual replica count and creates or deletes pods until they match.
- Wrong: "An ops engineer SSHes in and starts the new pods at 10pm." (That is the imperative world; the controller does this in cloud-native operation.)
- Wrong: "The pods themselves know to multiply at 10pm." (Pods don't self-replicate; the controller does.)
- Wrong: "The kubelet on the node decides to start more pods." (Kubelet runs what it's told; the scheduler and controllers decide.)

### 1.5 ELI5

A thermostat watches the room and turns the heater on when it's too cold and off when it's warm enough. It never stops watching. Kubernetes is a building full of tiny thermostats — one watches "how many copies of this app are running," another watches "is this computer still alive." When something doesn't match what you asked for, the thermostat fixes it.

### 1.6 ELI10

A *reconciliation loop* is a small program that does one thing forever: it reads what you said you wanted, looks at what actually exists, and makes a small change to close the gap. The controller for Deployments does this for replica count: if you said three replicas and one died, it makes a fourth — sorry, a third — to bring the count back up. The controller for Nodes does this for node health: if a node hasn't checked in for a while, it marks it unschedulable and lets other controllers move the pods elsewhere.

This is why Kubernetes survives node failures, network blips, and pods crashing: nothing is "set up once and forgotten." The desired state is a description in the API; the actual state is what's running; controllers are the loop between them. Treating servers as *cattle* (identical, replaceable) instead of *pets* (named, hand-tuned) is what makes this survivable — when a cow dies, you don't grieve, you bring in another. When you operate cloud-native, every server is a cow.

### 1.7 Real-world

A SaaS startup running on three hand-built EC2 instances kept losing a weekend every quarter to "the database VM rebooted and the app didn't come back." Migrating to Kubernetes meant they wrote a Deployment for the app and a StatefulSet for the database. After the move, when an EC2 host was rotated by AWS, the controllers rescheduled the pods onto a healthy host and the on-call engineer woke up to a Slack message saying "self-healed at 3:14am — no action needed." The reconciliation loop ate the page.

### 1.8 Flashcards

1. **What is a reconciliation loop?** A controller program that reads desired state, observes actual state, and takes the minimum action to close the gap — repeatedly, forever.
2. **What is the difference between declarative and imperative configuration?** Declarative says *what* the world should look like ("3 replicas of nginx"). Imperative says *how* to get there ("install nginx, then start 3 copies"). Kubernetes is declarative.
3. **What does "pets vs cattle" mean?** A pet is a hand-tuned named server you'd mourn. Cattle are identical replaceable units. Cloud-native systems treat servers and pods as cattle so failure is routine and recoverable.

### 1.9 Quiz

**Q1 (pause-the-animation).** The animation shows the desired state set to 3 replicas. The actual state is 1. The controller is about to fire. What action will it take, and why?

**Answer.** The controller will create two more pods of the same template, bringing actual to 3. The action is the *minimum* needed to close the gap — it doesn't recreate the existing pod, doesn't delete anything, doesn't restart. It just creates what's missing. That minimum-diff principle is what makes the loop converge cleanly without thrashing.

**Q2.** Why does treating servers as cattle make a system more reliable than treating them as pets?

**Answer.** Pets have unique state and unique knowledge that lives only on that machine. When a pet dies, you have to recreate it from incomplete documentation. Cattle are identical and described declaratively — when one dies, the platform replaces it from the same description. Reliability comes from "any machine can do this job and the platform will replace any that dies," not from "this specific machine never fails."

---

## Subtopic 2 — Twelve-factor apps; microservices vs modular monoliths

### 2.1 Concept

The **twelve-factor methodology** (Heroku co-founder Adam Wiggins, 2011, [12factor.net](https://12factor.net)) is twelve rules for writing applications that run well on dynamic platforms — Heroku originally, but the rules generalize. The factors:

1. Codebase — one codebase tracked in version control, many deploys.
2. Dependencies — explicitly declared and isolated.
3. Config — stored in the environment, never in code.
4. Backing services — treated as attached resources (DB, cache, queue).
5. Build, release, run — strictly separated stages.
6. Processes — execute as one or more stateless processes.
7. Port binding — export services via port binding.
8. Concurrency — scale out via the process model.
9. Disposability — fast startup, graceful shutdown.
10. Dev/prod parity — keep development, staging, production as similar as possible.
11. Logs — treat logs as event streams written to stdout.
12. Admin processes — run admin tasks as one-off processes.

A twelve-factor app drops into a Kubernetes pod almost without modification. A non-twelve-factor app — one that writes config to disk, stores session in local memory, expects a long restart, or reads logs from a fixed file — fights the platform.

**Microservices** split an application into many small services that communicate over the network. **Modular monoliths** keep one deployable but enforce strict module boundaries internally. Microservices pay a coordination cost (network calls, deployment fan-out, distributed tracing); monoliths pay a discipline cost (boundaries that must be preserved by code review, not by network). For most teams, a well-structured modular monolith is the right starting point; microservices are an answer to organizational scale, not a starting architecture.

### 2.2 Before / after

**Before twelve-factor.** An app reads its database password from `/etc/myapp/db.conf`, stores user sessions in a `session/` directory, and writes logs to `/var/log/myapp.log` rotated by a cron job. Moving it to a new server means setting up that exact filesystem layout. Running it on a platform that gives you a fresh container every time means the app loses sessions on every deploy.

**After twelve-factor.** The app reads its database password from `$DB_PASSWORD`, stores sessions in Redis, and writes logs to stdout. Moving it to Kubernetes is a Dockerfile, a Deployment, and an injected secret. Sessions survive deploys because they're not on the pod's filesystem. Logs are a stream the platform collects.

**What did not get easier.** Twelve-factor doesn't make the app *fast* or *correct*. A buggy stateless app is still a buggy app. The methodology removes friction with the platform; the application logic is still your problem.

### 2.3 Analogy — shipping containers

A twelve-factor app is a standard shipping container. The container has fixed dimensions, standard lift points, a manifest on the side, plug points for refrigeration. It rides on a truck, then a ship, then a train, then another truck, and at each transfer the equipment knows what to do because the container is standard.

A non-twelve-factor app is a one-off bespoke crate. It needs custom rigging, a specific kind of forklift, careful loading instructions written by the engineer who built it. Every transfer is a project. The platform can't move it without help.

Microservices are many small containers. Modular monoliths are one big container with internal compartments — the compartments are still real, but the container moves as one piece.

### 2.4 Quick check

A team has a Java app that writes its session state to a `sessions/` directory on the local filesystem. They want to run it on Kubernetes. What's the cleanest fix?

- **Correct.** Move sessions to an external store (Redis, a database, or a sticky session at the load balancer). Pods are disposable; their filesystem can disappear at any reschedule. Twelve-factor calls this "Processes — execute as one or more stateless processes." The session shouldn't live in the pod.
- Wrong: "Mount a persistent volume into every pod and share it." (RWX volumes are slow, complicated, and don't actually solve the problem; they just hide it.)
- Wrong: "Run only one replica so sessions stay on one pod." (You give up scaling and HA. The reconciliation loop will reschedule that one pod and you'll still lose sessions.)
- Wrong: "Disable session expiry." (Doesn't address pod restart. The session was never durable to begin with.)

### 2.5 ELI5

Imagine all the boxes that ship around the world look exactly the same — same size, same lift points, same labels. Now any truck or ship or warehouse can handle any box without reading instructions. A twelve-factor app is one of those boxes. A normal app is a one-off package the post office has to figure out every time.

### 2.6 ELI10

Twelve-factor is a checklist for writing apps that move easily between environments. The rules are simple individually — read config from environment variables, write logs to stdout, don't store state on local disk, start fast, shut down gracefully — but together they remove almost every reason an app would refuse to run on a dynamic platform like Kubernetes. Microservices and modular monoliths are two answers to "how do I split a big app." Microservices split across the network — independent deploy, independent scale, independent failure, with the cost of coordination. A modular monolith splits by code module inside one deployable — easier to deploy and reason about, with the cost of needing real discipline to keep the boundaries clean. Most teams should reach for "modular monolith first, microservices when org or scale demands it" — Kubernetes will run either, and isn't a reason to choose microservices.

### 2.7 Real-world

A 30-engineer SaaS team kept hitting deployment slowdowns on a Rails monolith — a single `bundle install + rails s` took 4 minutes, and cross-team merges blocked each other. They considered breaking into microservices but instead split the codebase into well-defined modules with explicit interfaces, kept the monolith, and added a CI gate that prevented module boundary violations. Deploys stayed fast (one image), team independence improved (modules owned by teams), and they avoided the operational tax of running 12 services with 12 deployments and 12 dashboards. They eventually extracted *one* high-traffic module into its own service when traffic justified it.

### 2.8 Flashcards

1. **What is a twelve-factor app?** An app written to twelve specific guidelines (codebase, dependencies, config, backing services, build/release/run, processes, port binding, concurrency, disposability, dev/prod parity, logs, admin processes) that make it run cleanly on dynamic platforms.
2. **Microservices vs modular monolith — what's the trade?** Microservices split across the network for independent deploy/scale/fail at the cost of coordination overhead. A modular monolith splits inside one deployable for simpler operations at the cost of needing strict discipline to keep boundaries clean.
3. **Why are stateless processes a twelve-factor rule?** Because the platform can stop, move, restart, or replace any process at any time. Anything that lives only inside the process disappears with it. State must live in attached backing services.

### 2.9 Quiz

**Q1.** A team is moving a Python app to Kubernetes. The app currently reads database credentials from `/etc/app/db.conf`, written by a Chef recipe at provisioning time. Which twelve-factor rule does this violate, and what's the cleanest fix?

**Answer.** Violates "Config — stored in the environment, never in code or in baked-in files." Cleanest fix: store credentials as a Kubernetes Secret, mount or inject as environment variables. The app reads `os.environ['DB_PASSWORD']`. The Chef recipe goes away.

**Q2.** Why is a modular monolith often a better starting architecture than microservices for a young team?

**Answer.** Microservices push complexity from inside the codebase to the network — distributed tracing, retries, idempotency, service discovery, separate dashboards, separate on-call. A young team rarely has the operational maturity to absorb that. A modular monolith lets you keep clear internal boundaries with a fraction of the operational tax. You can split out a service later when one module's scale or team boundary actually justifies it.

---

## Subtopic 3 — When Kubernetes is useful, and when it's overkill

### 3.1 Concept

Kubernetes pays back when:

- You run **many services** that each need lifecycle automation (deploy, scale, restart, observe, route traffic).
- Workloads are **dynamic** — they scale up and down, get rescheduled, get replaced.
- You have **multiple teams** sharing infrastructure and want a common platform with isolation.
- You need **portable** workloads — same manifests on local kind, EKS, AKS, GKE, OpenShift.
- You're already paying the cost of distributed systems and want a standard control plane.

Kubernetes is overkill when:

- A **single application** runs fine on a single VM and rarely changes.
- The team has **no platform engineering capacity** — there is no one to run the cluster, observe it, upgrade it, or debug it. Kubernetes is a power tool; it requires operators.
- Workloads are **batch only** — a workflow engine (Airflow, Argo Workflows on a small cluster, plain queue workers) might be enough.
- Latency is **microsecond-sensitive** — Kubernetes adds layers (CNI, kube-proxy or eBPF, ingress) that introduce per-hop latency that's irrelevant at 50ms but matters at 50µs.
- The org's current pain is **application architecture**, not infrastructure orchestration. Moving a bad app to Kubernetes makes it a bad app on Kubernetes.

The honest summary: Kubernetes solves operational scale and heterogeneity. If you don't have operational scale or heterogeneity, you don't need it.

### 3.2 Before / after

**Before — a small startup.** Two services on two VMs, one Postgres on RDS, deployments via a shell script. Total operational load: one engineer, two hours per week. Adding Kubernetes here adds ten hours per week of cluster maintenance, training, debugging, on-call. The startup loses time without gaining anything.

**After — the same startup at series B with 8 services and 4 teams.** Each team wants to deploy independently, share secrets, run staging environments, and add new services without filing a ticket. Now the platform is the bottleneck. Adopting Kubernetes (with a small platform team) replaces 8 different deploy scripts and 4 different staging tents with one common system. The ten hours of cluster work pays for itself in the time it saves elsewhere.

**What did not change.** Kubernetes never makes a single service simpler. It pays off only when the *count* of things to operate is the bottleneck.

### 3.3 Analogy — industrial kitchen

Kubernetes is an industrial kitchen. Many cooks, multiple ovens, walk-in fridges, line orders, prep stations, plating stations, expediter, head chef coordinating, cleaning crew, a written service standard. When you're feeding 800 people for a wedding, you need this.

When you're making yourself toast in the morning, you need a toaster and a counter. If someone built you an industrial kitchen for your toast, the kitchen would consume more attention than the toast. The kitchen isn't bad — it's wrong for the use case.

The question isn't "is Kubernetes good?" It's "are you in the wedding-catering situation, or the morning-toast situation?"

### 3.4 Quick check

A two-person startup ships a Rails app, one PostgreSQL database, and a simple background worker. They get a few hundred users a day. Should they adopt Kubernetes?

- **Correct.** Almost certainly not — yet. Their workload fits comfortably on a managed app platform (Render, Fly, Heroku, even a single VM with systemd). Adopting Kubernetes adds a cluster to operate, a learning curve for two engineers, and complexity that won't pay off until they have many services or many teams. They should revisit when they have ~5+ services, ~3+ teams, or genuine portability needs.
- Wrong: "Yes, Kubernetes is the modern way." (Modern doesn't mean appropriate. Tooling fit matters more than fashion.)
- Wrong: "Yes, they'll need it eventually so start now." (You pay the operational cost from day one for a benefit that arrives years later. Adopt when you need it.)
- Wrong: "Only if they hire a platform engineer first." (Even with a platform engineer, two services don't justify a cluster.)

### 3.5 ELI5

A big restaurant kitchen with many ovens and many cooks is amazing if you're feeding hundreds of people. It's silly if you're making one piece of toast. Kubernetes is the big kitchen.

### 3.6 ELI10

Kubernetes is a *platform* — it solves the problem of running lots of services across many machines, with deployments, scaling, restarts, secrets, networking, and observability all standardized. When you have lots of services and multiple teams, that standardization is gold; you don't want every team inventing their own deploy script. When you have one service, the platform itself becomes the work — you spend time keeping the cluster healthy instead of building product.

A useful test: count the services you'll deploy and the teams that own them. Below ~5 services and ~2 teams, simpler tools (managed platforms, single-VM systemd, serverless) usually win. Above that, the per-service cost of Kubernetes drops sharply — the cluster pays for itself. Above ~15 services and ~5 teams, almost everyone wants the abstractions Kubernetes provides. Latency-sensitive workloads (high-frequency trading, real-time bidding microsecond paths) are a separate category — Kubernetes' network and scheduling layers add per-hop cost that's irrelevant for HTTP APIs but expensive for sub-millisecond paths.

### 3.7 Real-world

A media company with 40 microservices, 6 product teams, and a custom Capistrano deploy from 2014 was spending most of its platform engineering time on "make a deploy work." Migrating to Kubernetes (managed EKS) over six months collapsed 40 deploy scripts into one Helm pattern, replaced six different staging setups with namespaced previews, and freed two engineers to work on developer experience instead of plumbing. Conversely: a four-engineer fintech tried Kubernetes for a single core service plus a job worker, spent a year on cluster operations, and later moved back to ECS Fargate — the platform tax wasn't earning anything for one service.

### 3.8 Flashcards

1. **Name three signals that Kubernetes is the right fit.** Many services to operate, multiple teams sharing infrastructure, dynamic workloads that scale and reschedule, need for workload portability across environments, existing operational maturity to run a cluster.
2. **Name three signals that Kubernetes is overkill.** Single application that rarely changes, no platform engineering capacity, latency-sensitive sub-millisecond workloads, the team's current pain is application architecture rather than orchestration.
3. **Why doesn't moving a small app to Kubernetes make it easier to operate?** Kubernetes solves the *count* problem — running many things — not the per-app complexity problem. A single app on Kubernetes pays the cluster operational cost without getting the benefit; on a single VM, you'd skip the cost entirely.

### 3.9 Quiz

**Q1.** A 6-engineer team has one Django app, one Postgres, two background workers, and a Redis cache. They're considering Kubernetes. What questions should drive the decision?

**Answer.** How many services do they expect to add in 12 months? How many independent teams will own deploys? Do they need workload portability (cloud A → cloud B → on-prem)? Do they have time for cluster operations (upgrades, observability, cost)? If the answers are mostly "stays small," "one team," "no portability need," "no platform time" — they should not adopt yet. If at least three answers point toward growth, adopt.

**Q2.** Why is "we want to use Kubernetes because it's the modern way" a poor reason to adopt it?

**Answer.** Because adoption isn't free — the cluster itself becomes work. Kubernetes pays back in proportion to operational scale (many services, many teams). For workloads that don't have that scale, the operational cost of the platform exceeds the value it delivers. Adopt because the workload shape demands it, not because the technology is in vogue.

---

## Subtopic 4 — GitOps, platform engineering, SRE, service ownership, multi-tenancy

### 4.1 Concept

These five terms describe how mature organizations *operate* Kubernetes once they have it.

- **GitOps** is an operating model where the desired state of the system lives in a Git repository, and an automated agent in the cluster continuously pulls from Git and reconciles. Coined by Weaveworks (Alexis Richardson, 2017). Four formal principles, per [opengitops.dev](https://opengitops.dev): the system is *declarative*, *versioned and immutable* in Git, *pulled automatically* by software agents, and *continuously reconciled*. Tools: Argo CD, Flux CD.
- **Platform engineering** is the discipline of building an internal platform — a "paved road" — that product teams consume. The platform team owns Kubernetes, observability, secrets, CI/CD, ingress; product teams ship apps onto it via a thin interface (manifests, a CLI, a portal). Codified in the [Team Topologies](https://teamtopologies.com) book and the platform-engineering community of the late 2020s.
- **SRE** (Site Reliability Engineering) is Google's operating model, popularized by the 2016 SRE Book (Beyer, Jones, Petoff, Murphy). Core ideas: define reliability with **SLIs** (indicators), **SLOs** (objectives), **SLAs** (agreements); spend an **error budget** on velocity until reliability drops; automate operations as code; treat infrastructure as a software problem.
- **Service ownership** ("you build it, you run it") puts the team that wrote the service on its on-call rotation. The team feels both the deploy pleasure and the 3am page; this aligns incentives toward reliability without bureaucratic enforcement.
- **Multi-tenancy** is sharing one cluster (or one platform) across multiple teams or customers. Soft tenancy = trust between tenants, isolation by namespace + RBAC + quotas. Hard tenancy = no trust between tenants, isolation by separate clusters or virtual clusters (vCluster) + node isolation + strict admission policy. The right point on the spectrum depends on threat model.

These five things compound. GitOps without service ownership becomes a bottleneck on the platform team. Service ownership without SRE becomes burnout. SRE without a platform turns every team into a Kubernetes operator. Multi-tenancy without RBAC and quotas is a noisy-neighbor disaster. Together they define how a healthy Kubernetes-using org runs.

### 4.2 Before / after

**Before.** Operations is a separate ticket queue. To deploy, a developer files a ticket; the ops team patches a server, runs a script, closes the ticket. When the system breaks at 3am, ops gets paged — the developer doesn't. Knowledge of how things actually run lives only in ops; developers ship code blind.

**After.** The platform team builds and runs the cluster. Product teams own their service end-to-end: they write the YAML, commit to Git, an agent reconciles to the cluster, they're on the rotation when their service pages. The platform team monitors error budgets and provides paved roads (templates, dashboards, golden images, security guardrails). Ops as a separate function disappears; reliability becomes a shared property.

**What did not change.** People still need to be on call. Software still breaks. The 3am page still happens. What changes is who answers it (the team that owns the code) and how it gets fixed (with the same observability and tools the team uses every day).

### 4.3 Analogy — the library

GitOps is a library where every change to the shelves starts with a card written in the catalog (a Git commit). A librarian (the controller — Argo CD, Flux) reads new cards, walks to the shelf, and makes the change. Nobody walks past the librarian and rearranges books — and if they do, the librarian notices the drift and puts the books back the way the catalog says.

Platform engineering is the central catalog desk and reading rooms — built once, used by everyone. Service ownership is each section ("Fiction," "Reference," "Periodicals") having its own librarian who knows that section deeply. SRE is the head librarian who watches how often books get misshelved and decides how much risk the library can absorb this quarter. Multi-tenancy is the fact that schools, scholars, and the public all share the same building — separated by hours, by reading rooms, by privileges.

### 4.4 Quick check

A developer SSHes into a production node and changes a ConfigMap by hand because their service is broken at 11pm. The cluster is GitOps-managed by Argo CD. What happens next?

- **Correct.** Argo CD detects the live state has drifted from the Git source and reverts the ConfigMap back to whatever Git says. The developer's hand-edit disappears, often within minutes. The right path is to commit the change to Git (and let Argo CD apply it), or to mark the resource as ignored by Argo CD if it's intentionally externally managed.
- Wrong: "Argo CD records the change as the new desired state." (Argo CD is one-way: Git is truth, cluster is reconciled to it. Live edits are drift, not new truth.)
- Wrong: "The change persists until the next manual sync." (Default sync includes drift correction; manual sync isn't required for revert.)
- Wrong: "The change is allowed because the developer is in a privileged group." (RBAC permitted the change at the API; the GitOps controller still treats it as drift.)

### 4.5 ELI5

A library with rules: every book change starts with a written card in the catalog. A librarian reads new cards and moves the books. Nobody is supposed to rearrange books by walking up to the shelf — and if they do, the librarian puts the books back the way the catalog says.

### 4.6 ELI10

GitOps moves the source of truth from the cluster to a Git repository. An agent inside the cluster watches Git and reconciles the cluster to match — same loop pattern as a Kubernetes controller, just with Git as the desired state. Platform engineering is the discipline of building the paved road that product teams ride on, so each team isn't reinventing CI, secrets, ingress, observability. SRE adds the language of measurable reliability — SLIs, SLOs, error budgets — and the principle that reliability is a feature you trade off against velocity. Service ownership puts the team that built a service on call for it, so the people who can fix a problem are also the people who feel it. Multi-tenancy lets multiple teams share one platform with isolation tuned to the level of trust between them. None of these is a Kubernetes feature — they are operating practices that Kubernetes enables.

### 4.7 Real-world

A retail company with 20 product teams adopted GitOps via Argo CD over a year. Pre-GitOps, their average production change took 2 days from commit to live and required three approvals; post-GitOps, the same change took 14 minutes via PR merge to the env repo. The platform team published a paved-road template — Helm chart skeleton + Argo Application + ServiceMonitor + AlertmanagerConfig — and any new service got all of those for free. Two years later they introduced soft multi-tenancy: each team got its own namespace, ResourceQuotas, NetworkPolicies, and an Argo Project scoped to its repos. They still ran one shared cluster per environment.

### 4.8 Flashcards

1. **What are the four GitOps principles?** Declarative, versioned and immutable in Git, pulled automatically by an agent, continuously reconciled (per opengitops.dev).
2. **Platform engineering vs SRE — what's the difference?** Platform engineering builds the platform product (the paved road). SRE is a reliability practice (SLIs / SLOs / error budgets). They overlap heavily but answer different questions: "what do we ship to product teams" vs "how do we manage reliability over time."
3. **Soft vs hard multi-tenancy?** Soft: trusted tenants share one cluster, isolation via namespaces + RBAC + ResourceQuotas + NetworkPolicy. Hard: untrusted tenants need separate clusters or virtual clusters (vCluster), strict admission policy, dedicated nodes.

### 4.9 Quiz

**Q1.** What's the practical reason that "you build it, you run it" makes services more reliable over time?

**Answer.** Incentive alignment. The team that wrote the code feels the on-call pages. They cannot externalize the cost of bugs onto a separate ops team. Over weeks, they invest in better tests, better observability, better deploy patterns — because *they* will be paged otherwise. Reliability emerges from incentive, not from process.

**Q2.** A team wants to "do GitOps" but their developers regularly run `kubectl apply` from their laptops to fix urgent issues. Why is this a problem and what's the fix?

**Answer.** Live `kubectl apply` makes the cluster the source of truth, not Git. Drift accumulates; the GitOps agent will fight the human edits or the human edits will silently overwrite Git's intent. The fix is to make the Git repo the only path that succeeds: restrict cluster write RBAC to the GitOps controller's service account, and route urgent fixes through PR merge with a fast-track review process. The bias should be that breaking-glass live edits are visible, audited, and rare.

---

## Subtopic 5 — Kubernetes lineage, CNCF, release cadence, KEPs, feature gates

### 5.1 Concept

Kubernetes was created at Google in 2014 as an open-source descendant of two internal cluster-management systems: **Borg** (in production since the early 2000s; paper published 2015) and **Omega** (paper 2013). Borg taught Google how to schedule containers across thousands of machines; Omega was a research successor that explored shared-state scheduling. Kubernetes (Greek for "helmsman"; the "K8s" abbreviation is K + 8 letters + s) was open-sourced in June 2014 and reached 1.0 in July 2015.

That same month (July 2015), Kubernetes was donated to the **Cloud Native Computing Foundation (CNCF)** — a Linux Foundation project formed to host vendor-neutral cloud-native open-source projects. Kubernetes became the CNCF's first graduated project in March 2018. The CNCF now hosts hundreds of projects and publishes the [CNCF Landscape](https://landscape.cncf.io) — a sprawling map of the cloud-native ecosystem.

**Release cadence.** Kubernetes ships ~3 minor releases per year (it was 4/year through 2022; reduced to 3/year starting 2023). Each minor release is supported with patches for ~14 months (12 months of active support + ~2 months of EOL transition), so the last 3 minor versions are actively patched at any time.

**KEPs** (Kubernetes Enhancement Proposals) are the formal change-management process. Any non-trivial change to Kubernetes — a new API, a new field, a behavioral change — goes through a KEP: a markdown document in the [kubernetes/enhancements](https://github.com/kubernetes/enhancements) repo, reviewed by the relevant SIG (Special Interest Group), tracked through stages.

**Feature gates** are the runtime flags that turn individual features on and off. A feature progresses through three stages:

- **Alpha.** Off by default. May be buggy. May be removed without deprecation. Use only in test clusters; never in production.
- **Beta.** Historically *on* by default. As of Kubernetes 1.24+ (KEP-3136), *new* beta features added are *off* by default. Beta features may still change in incompatible ways, but with a deprecation cycle.
- **GA / Stable.** On by default. Backward compatibility guaranteed. Removal requires a multi-release deprecation cycle.

**Conformance** is the [CNCF Certified Kubernetes program](https://www.cncf.io/training/certification/software-conformance/). Distributions that pass the conformance test suite (run via `sonobuoy` historically, now `hydrophone`) can call themselves "Certified Kubernetes" and use the API portably. Vendor-specific *features* (Anthos features, OpenShift Routes, EKS Pod Identity) sit outside conformance — they're product additions, not the standard.

### 5.2 Before / after

**Before Kubernetes.** Running containers at scale meant either home-grown schedulers (most companies stopped at "a script that SSHes to N machines") or one of a few competing systems (Mesos + Marathon, Docker Swarm, Nomad). Each company recreated the same primitives differently. Portability across clouds and on-prem was a custom integration job.

**After Kubernetes.** A single API for "schedule a container, give it an IP, expose it as a service, scale it, restart it on failure" became the de facto standard across clouds, on-prem, and edge. Every major cloud provides a managed Kubernetes service (EKS, AKS, GKE) with the same upstream API. Workload portability is roughly real for the parts that stick to upstream APIs.

**What did not get easier.** Kubernetes is not simple — its API surface is enormous, conformance only covers the API not the operational reality, and the variation between distributions in defaults, networking, storage, and security is still a real cost when moving between them.

### 5.3 Analogy — train-line testing

New Kubernetes features go through alpha → beta → GA the way new train signals get tested on a quiet branch line first, then on a moderately busy line, then on the main intercity route. By the time you ride the main line, the signals are boring on purpose — they've been observed long enough to be predictable. Alpha is the branch line: things break, that's the point. Beta is the moderately busy line: most things work, but the railroad tells you "we may still tweak the signal pattern." GA is the main line: stable, predictable, and removing it requires its own multi-year process.

### 5.4 Quick check

A team wants to use a feature listed as "alpha" in the Kubernetes 1.34 release notes. What should they do?

- **Correct.** Use it only in dev/test clusters and assume it can change incompatibly or disappear before GA. Alpha features are off by default for a reason — they're not stable, they may have known bugs, and the API can change between minor releases. Production should use GA features and explicitly-vetted beta ones.
- Wrong: "Enable the feature gate in production for early adopter advantage." (Alpha features don't carry compatibility guarantees; an upgrade can break the feature or the cluster.)
- Wrong: "Wait for the official cloud provider to enable it." (Cloud providers usually wait for GA; you'd be waiting indefinitely. The right approach is to use it in non-prod and contribute feedback.)
- Wrong: "Only use alpha features if they're in the kube-controller-manager." (Stage matters, not which component owns the gate.)

### 5.5 ELI5

Kubernetes is built by lots of people working together. Whenever they want to add something new, they write down what they want to add, they try it carefully in a test version (alpha), then a slightly more careful version (beta), then a full version (GA). By the time it's "GA," lots of people have used it and it's safe.

### 5.6 ELI10

Kubernetes' lineage is Borg (Google's internal scheduler since the early 2000s) → Omega (a Google research successor, 2013) → Kubernetes (open-sourced 2014, 1.0 in 2015, donated to the CNCF the same year, graduated in 2018). It now ships about three minor releases per year, with each release supported for around 14 months — so at any moment, the most recent three minors are patched. New features are proposed as Kubernetes Enhancement Proposals (KEPs), reviewed by the SIG that owns the area, and shipped through the alpha → beta → GA pipeline. *Feature gates* are the per-feature on/off switches; their default depends on the stage. Alpha is opt-in and unsafe; beta is opt-in for new features (since Kubernetes 1.24) or opt-out for older ones; GA is on and stable. Conformance is the CNCF program that defines what "Certified Kubernetes" means — the API contract that distributions agree to honor — but distributions add their own features on top, which is why one EKS cluster and one OpenShift cluster will look familiar at the API level and very different in operation.

### 5.7 Real-world

A platform team standardized on "we ship workloads against GA APIs only; beta features are evaluated case by case; alpha is dev-only." This rule meant they were never burned by a beta change between Kubernetes 1.27 and 1.28 (when the InPlacePodVerticalScaling feature changed shape twice during beta), but they did wait an extra year to use Gateway API in production until the v1 GA. Their next-door neighbor team made the opposite call (run alpha aggressively for early features) and spent two on-call weeks rebuilding workloads when an alpha API was renamed in a minor release.

### 5.8 Flashcards

1. **What is the Kubernetes lineage?** Borg (Google internal, since early 2000s, paper 2015) → Omega (Google research, paper 2013) → Kubernetes (open-sourced 2014, 1.0 in July 2015, CNCF first graduated project March 2018). "K8s" = K + 8 letters + s.
2. **What's the current Kubernetes release cadence and support window?** Roughly 3 minor releases per year (since 2023; was 4/year before). Each minor release is patched for ~14 months (12 months active + ~2 months EOL transition); the most recent 3 minors are supported at any time.
3. **What does "alpha" feature gate mean and what's the production rule?** Alpha = off by default, may change incompatibly or be removed without deprecation, may be buggy. Production rule: use only GA features (and explicitly vetted beta features); reserve alpha for dev/test clusters.

### 5.9 Quiz

**Q1.** Why is "we use a feature only after it goes GA" usually the right operational rule?

**Answer.** Because GA carries the strongest compatibility guarantee Kubernetes offers — backward-compatible behavior, multi-release deprecation if it's ever removed, on by default. Beta APIs can still change shape; alpha can vanish. Operating production on GA features means upgrades won't surprise you; operating on beta or alpha means you accept upgrade-time refactoring as a routine cost.

**Q2.** A vendor's distribution says it's "Kubernetes-compatible" but not "Certified Kubernetes." What does this difference signal?

**Answer.** Certified Kubernetes is a CNCF program with a specific test suite that the distribution has passed. "Kubernetes-compatible" is not a defined term — it might mean the distribution implements most of the Kubernetes API but has skipped or modified parts of it. The practical risk is portability: your manifests may work, or they may hit an unimplemented API and break in a way that wouldn't happen on a certified cluster. Prefer Certified Kubernetes when portability matters.

---

## Recap

Five subtopics, one spine.

- **Reconciliation loops** are the heart of Kubernetes. Desired state vs actual state, controllers in between, never stopping. Pets vs cattle, declarative vs imperative, failure as normal — these all flow from this one idea.
- **Twelve-factor apps** drop into pods cleanly. Microservices and modular monoliths are both valid; pick by org and scale, not by fashion.
- **Kubernetes is the right tool** when you have many services, many teams, and dynamic workloads. It's overkill when the count is small or there's no platform engineering capacity.
- **GitOps + platform engineering + SRE + service ownership + multi-tenancy** are the operating model that mature Kubernetes orgs converge on. None is a Kubernetes feature; all are practices Kubernetes enables.
- **Borg → Omega → Kubernetes**, ~3 minor releases per year, alpha → beta → GA, KEPs, conformance. The release pipeline is *how* you can trust the platform — features are observed before they're trusted.

**Next lesson — Module 2:** Containers in detail. We open the box on the thing that runs inside a pod — Linux namespaces, cgroups, OCI specs, runtimes, image building, registries, the PID 1 problem.

---

## Self-critique notes (per QUALITY.md)

- **Analogies (5):** Thermostat (subtopic 1) is structural and grounded — desired/actual/controller maps cleanly and survives "what about a thermostat with a schedule" follow-ups (= scheduled scaling). Shipping containers (2) maps factor-by-factor without strain. Industrial kitchen (3) is sensory and supports "when not." Library (4) carries five concepts (catalog = Git, librarian = controller, sections = teams, head librarian = SRE, shared building = multi-tenancy). Train-line testing (5) is concrete and matches the stage progression precisely. All five pass the "oh!" test.
- **ELI5/ELI10 pairing:** Each ELI5 stays under 100 words and centers the analogy without jargon; each ELI10 adds correct terms while staying in the same metaphor.
- **Before/after symmetry:** Each subtopic's before and after are within ~15 words of each other and each acknowledges what didn't change.
- **Real-world scenarios:** Each names a specific company type and includes a specific trade-off / complication — not pure-triumph stories.
- **First-time-learner test:** Cloud-native, declarative, controller, desired/actual state, GitOps, KEP, feature gate, conformance, CNCF — all defined inline on first appearance. The thermostat analogy carries the entire reconciliation concept; once that lands, the rest of the lesson is layering vocabulary on it.
