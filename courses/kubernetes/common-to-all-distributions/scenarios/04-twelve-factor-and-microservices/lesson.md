# Lesson 04 — Twelve-Factor Apps + Microservices vs Modular Monoliths

> Course: Kubernetes — Common to all distributions
> Lesson 04 of 17 in K-COM. How to design apps that thrive on Kubernetes,
> and how big each app should be.
> Companion preview: `/preview-kubernetes-lesson-04.html`.

---

## 1. Concept

Two design questions that get asked together because they answer the same
overall question: *how do I design my apps so they thrive in cloud
environments?*

**The Twelve-Factor App** is a 12-rule manifesto written in 2011 by Adam
Wiggins (Heroku co-founder) describing how an app should be built and
packaged so it runs cleanly on any modern platform — including Kubernetes.
The factors cover where config goes, how state is handled, how the app
starts and stops, how logs flow, how backing services are connected. Follow
them and your app drops into a pod with almost no work. Violate them and
your app fights the platform forever.

**Microservices vs monoliths** is the architectural choice about *how big
each app should be*. A monolith is one big deployable that does
everything. Microservices are many small services that communicate over the
network. A modular monolith sits in between: one deployable, but with strict
internal module boundaries.

---

## The 12 factors

1. **Codebase** — One codebase tracked in version control, many deploys.
2. **Dependencies** — Explicitly declare and isolate dependencies (lockfiles).
3. **Config** — Store config in environment variables, never in code.
4. **Backing services** — Treat databases, caches, queues as attached resources.
5. **Build, release, run** — Strictly separate build, release, and run stages.
6. **Processes** — Execute as one or more stateless processes.
7. **Port binding** — Export services via port binding, be self-contained.
8. **Concurrency** — Scale out via the process model.
9. **Disposability** — Fast startup and graceful shutdown.
10. **Dev/prod parity** — Keep dev, staging, and production as similar as possible.
11. **Logs** — Treat logs as event streams written to stdout.
12. **Admin processes** — Run admin tasks as one-off processes against the same code.

Source: [12factor.net](https://12factor.net) by Adam Wiggins, Heroku, 2011.

---

## Three answers to the split question

- **Monolith** — One big deployable. Simple to deploy and debug. Tightly
  couples teams; one bug can affect everything.
- **Modular monolith** — One deployable, but with strict internal module
  boundaries enforced in code. Best of both worlds; needs discipline.
- **Microservices** — Many small services, each owning one capability.
  Independent deploy and scale, at the cost of distributed-systems complexity.

---

## 2. Before / After

**Before (custom-built app).** Reads database password from
`/etc/myapp/db.conf`. Stores user sessions in `sessions/` on disk. Writes
logs to `/var/log/myapp.log` rotated by cron. Hardcodes the staging vs prod
flag in source. Moving servers means recreating that exact filesystem
layout. Running on Kubernetes means lots of fighting.

**After (12-factor app).** Reads database password from `$DB_PASSWORD`.
Sessions in Redis. Logs to stdout. Reads "ENV=prod" from a Kubernetes
Secret. Moving anywhere is a Dockerfile + a Deployment YAML + a Secret.
Sessions survive restarts. Logs flow into your platform's pipeline
automatically.

What didn't change: 12-factor doesn't make your app correct. A buggy
stateless app is still a buggy app. The methodology removes friction with
the platform; application logic is still your problem.

---

## 3. Analogy — shipping containers + restaurants vs food courts

**Twelve-factor = the standard shipping container.** Before standard
containers (1956), every cargo was custom — barrels of oil, bales of cotton,
crates of fruit. Loading a ship took a week. The standard ISO container
changed everything: same dimensions, same lifting points, same
documentation, regardless of what's inside. A 12-factor app is a standard
container for software — same interface to the platform, same way to
receive config, same way to emit logs, same way to start and stop.

**Monolith vs microservices = restaurant vs food court.** A monolith is a
single restaurant: one kitchen, one chef, one menu, one team. Easy to
coordinate, but if the kitchen's busy, every dish slows down. A food court
is many small stalls: each scales staffing independently, but you need
shared infrastructure and coordination is harder. A modular monolith is a
single restaurant with specialty stations.

---

## 4. ELI5 / ELI10

**ELI5.** Imagine your toys all came in different boxes — some round, some
square, some sticky. Hard to put them on shelves! Now imagine all your toys
came in identical square boxes that fit perfectly on any shelf. That's a
12-factor app. As for big-vs-small apps: it's like deciding to build one
giant Lego castle in one piece (monolith) or making it from many smaller
Lego sets that snap together (microservices).

**ELI10.** The 12-factor methodology is twelve rules that turn an
application into a portable, platform-friendly unit: read config from
environment variables, log to stdout, don't store state on local disk,
start and stop quickly, treat external services as swappable URLs. Apps
that follow these rules drop into Kubernetes pods cleanly. The
microservices vs monolith decision is about *granularity*: one big
deployable (monolith) is operationally simpler but couples teams; many
small deployables (microservices) give teams independence but introduce a
"distributed-systems tax" — network calls, retries, timeouts, distributed
tracing, separate dashboards, separate on-call. Most teams should start
with a modular monolith and only split when scale or team boundaries
clearly justify it.

---

## 5. Real-world scenarios

**Heroku and the birth of 12-factor (2011).** Heroku ran tens of thousands
of customer apps on a shared platform. Adam Wiggins and his colleagues
distilled what made the well-behaved apps work into the 12-factor
manifesto. It became the foundational design guide for cloud-native
software.

**Netflix · 1,000+ microservices.** Netflix broke its monolith into
hundreds of microservices starting around 2009. Each team owns a few
services end-to-end. The trade-off: massive investment in observability,
service discovery, traffic management. They built much of this tooling
themselves (Hystrix, Eureka, Zuul). For their scale, the trade-off paid off.

**Shopify · the modular monolith champion.** Shopify chose to keep its
core e-commerce platform as a single Rails monolith — but with rigorous
internal module boundaries enforced by code review, custom linters, and
architectural fitness functions. Hundreds of engineers shipping daily into
one codebase, deploying as one image.

**The startup that microservices'd too early.** A 6-engineer startup
splits its product into 12 microservices "because that's the modern way."
Six months in, they're spending more time managing service-to-service
calls, distributed tracing, and version mismatches than building features.
The fix: collapse most services back into a modular monolith. Microservices
are an answer to organizational scale, not a starting architecture.

---

## 6. Animated illustration

Three modes in the preview animation, all under increasing load:

1. **Monolith under load.** One big deployable. Cart traffic rises; the
   whole monolith must scale together. Other features (login, etc.) get
   slow because they share the same process.
2. **Modular monolith under load.** Same operational shape, but cleaner
   internal boundaries. Cart contention is isolated by module discipline.
   Code is organized so cart could be split out later.
3. **Microservices under load.** Six small services. Cart scales
   independently — 4 copies of cart, 1 copy of everything else. Trade-off:
   six dashboards, six on-call rotations, every call between services is
   now a network call.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
