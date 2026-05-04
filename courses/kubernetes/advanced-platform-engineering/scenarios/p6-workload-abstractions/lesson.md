# K-ADV-PE P6 — P6 · Workload Abstractions: Score, OAM, Radius, Humanitec

> Course: K-ADV-PE (advanced specialization)
> Module P6 · Workload Abstractions
> Companion preview: `/preview-kubernetes-adv-pe-lesson-06.html`.

---

**🎯 If you remember nothing else:** **Score / OAM / Radius / Humanitec abstract K8s for developers. Pick by team ergonomics + portability needs. Platform team owns the abstraction; developers consume.**

## 1. Workload + dependencies in YAML; portable

**Score** (CNCF Sandbox): minimal YAML spec. Declares *workload* (containers + scaling) + *resources* (DBs / queues / DNS) + *service* (ports). **score-compose** renders to Docker Compose; **score-helm** renders to Helm chart; **score-k8s** directly to K8s manifests; **score-ecs** to AWS ECS Task Defs.
    Win: *portable*. Same Score spec runs in dev (Compose), staging (K8s), prod (K8s + Crossplane DBs). Reduce dev/prod divergence.

## 2. CUE-based typed application model

**OAM (Open Application Model)**: spec for *Components* (workloads) + *Traits* (cross-cutting concerns: scaling, ingress, observability) + *Policies* + *Workflows*. Defines structure separate from implementation.
    **KubeVela**: K8s implementation of OAM. *CUE-based* — typed config language (more constraints than YAML; less verbose). Compose Components + Traits per app; ship to many clusters.
    Win: *typed app definitions*; trait composition replaces copy-paste-yaml across teams.

## 3. App-graph + recipes (Microsoft)

**Radius** (Microsoft, open source): models app as a *graph* — resources (compute / DB / cache) + connections between them. Authoring in **Bicep** (or YAML). Recipes encapsulate per-environment infrastructure (Postgres in dev = local container; in prod = managed Postgres).
    Compared to OAM: graph-centric (relationships first-class); cloud-agnostic; tight Bicep ergonomics for Azure shops.
    Win: *relationships are explicit + typed*; environment-specific recipes hide cloud differences.

## 4. Opinionated PaaS + how to choose

**Humanitec**: commercial; portal-driven; opinionated PaaS-style. Tenants pick from a menu; Humanitec handles K8s + Terraform + GitOps under the hood. Trade self-host for hosted simplicity.
    **Selection grid**:
    
      - *Want portability across K8s + ECS + Cloud Run + Compose*: Score.

      - *Want typed app model + trait composition*: KubeVela / OAM.

      - *Want app-graph model + Bicep / Azure-shop ergonomics*: Radius.

      - *Want hosted PaaS-as-a-service*: Humanitec.

    
    None of these replace K8s; they're higher-level abstractions on top.

## Before / After

**Before.** Pre-abstractions, developers wrote 200 lines of K8s YAML per service. Copy-paste-modify drift; per-team variation; high cognitive load.

**After.** Workload abstraction: developer writes 30-line spec; platform-owned tooling renders K8s + cloud + observability. Portable + typed + composable.

*Hide K8s complexity from developers; platform team owns the abstraction.*

## Analogy — the K-Workshop bench

The Standard Tool Set on the workshop wall has four kits. Score is a portable toolbox — same tools work in any workshop. KubeVela is a precision-tool case — typed parts compose. Radius is a wiring-diagram drafting set — graph-first, lots of connections. Humanitec is a fully-equipped vendor truck — show up, choose from the menu.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Portable toolbox | Score (CNCF; portable across K8s/ECS/Compose) |
| Precision-tool case | KubeVela / OAM (CUE typed; trait composition) |
| Wiring-diagram set | Radius (Microsoft; app-graph + Bicep) |
| Vendor truck | Humanitec (commercial PaaS-as-a-service) |
| Tool template | Component + Trait (OAM) / Resource (Radius) / Workload (Score) |
| Per-shop adapter | Score-compose / score-helm / Radius recipe |

⚠️ *Analogy stops here:* A real toolbox is fixed; abstractions evolve as K8s evolves. Each abstraction lags K8s features; check abstraction's coverage of the K8s features you need.

## ELI5 / ELI10

**ELI5.** Four kits on the wall. Pick the one that matches your team. Each kit hides the K8s clutter and lets developers describe their service simply.

**ELI10.** **Score**: CNCF; portable; YAML workload + resources + service. **KubeVela / OAM**: CUE-typed; Components + Traits + Policies + Workflows. **Radius**: app-graph + Bicep; recipes per environment. **Humanitec**: opinionated PaaS; commercial; hosted.

## Real-world scenarios

- **Score for portable services.** A 50-engineer org runs services in Compose dev + EKS staging + GKE prod. Score spec one place; per-target Score CLI renders. Dev/prod divergence shrinks; new developers learn Score, not three platforms.
- **KubeVela for opinionated tenant defaults.** Platform team ships OAM Components: "web-service," "worker," "scheduled-job." Each Component bundles K8s manifests + observability + scaling Traits. Tenants compose; can't deviate without platform-PR.
- **Radius for app-graph thinking.** An Azure-shop org models apps as graphs: web-frontend → api → cache + db + queue. Radius encodes connections. Per-environment recipes: dev = local container; prod = Azure managed services. Bicep authoring familiar.
- **Humanitec for fast PaaS adoption.** A 25-engineer SaaS adopts Humanitec to skip platform-build phase. Tenants self-serve via portal; Humanitec runs the K8s + Crossplane + GitOps under the hood. Trade self-build for hosted speed.

## Common misconceptions

- **Myth:** "Workload abstractions replace K8s."
  **Truth:** They're abstractions *on top of* K8s (or other targets). The K8s underneath is still the runtime; abstraction renders to it.
- **Myth:** "Pick the most popular abstraction."
  **Truth:** Pick by team's ergonomics + needs. Score for portability; OAM for typed composition; Radius for graph thinking; Humanitec for hosted. Forcing the wrong one = friction.
- **Myth:** "Once abstracted, no team needs K8s knowledge."
  **Truth:** Platform team needs deep K8s + the abstraction's rendering layer. Developers can be K8s-free *most* of the time but need basics for incidents.

## Recap

Score / OAM / Radius / Humanitec abstract K8s for developers. Pick by ergonomics + portability needs; platform team owns the abstraction.

**Next — P7: Platform SLOs + chargeback / showback (OpenCost / Kubecost).**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
