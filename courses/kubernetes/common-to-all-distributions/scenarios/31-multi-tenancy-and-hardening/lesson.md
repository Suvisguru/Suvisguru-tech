# Lesson 31 — Multi-Tenancy & Hardening · Quotas, Limits, kube-bench, Hierarchies

> Course: Kubernetes — Common to all distributions
> Module 13 · Security · Lesson 5 of 5
> Companion preview: `/preview-kubernetes-lesson-31.html`.

---

**🎯 If you remember nothing else:** Namespaces are logical, not security boundaries. Multi-tenancy stacks: RBAC + NetworkPolicy + PSA + **ResourceQuota** (cap CPU/mem/object counts per namespace) + **LimitRange** (per-Pod min/max defaults). Run **kube-bench** regularly for CIS Benchmark scoring. Use **HierarchicalNamespaces (HNC)** for namespace trees with inherited policy. For real isolation: **vCluster**, **kata containers**, or separate clusters.

## 1. The myth of namespace isolation

Namespaces are an organisational primitive: scope for names ("`web` in `team-a`" doesn't collide with "`web` in `team-b`"), scope for RBAC, scope for ResourceQuota. *They're not security boundaries by default*. Out of the box:
    
      - Pods in different namespaces share a node — a kernel exploit in one Pod compromises the node.

      - Pods in different namespaces can talk to each other (until a NetworkPolicy says otherwise).

      - Anyone with cluster-admin sees everything.

      - Resource exhaustion in one namespace can starve others.

    
    To approximate tenant isolation, you stack:
    
      - **RBAC** — tenants can only see/touch their own namespace.

      - **NetworkPolicy / ANP** — tenants can't talk to each other.

      - **PSA** — Pods can't escape via privileged options.

      - **ResourceQuota** — tenants can't starve others.

      - **LimitRange** — Pods always have requests + limits.

    
    This is "soft multi-tenancy" — sufficient when tenants are within one organisation. For "hard multi-tenancy" (untrusted tenants), you need stronger isolation: vCluster (virtual K8s in a Pod), kata containers (lightweight VM per Pod), or separate clusters.

## 2. The two namespace-level resource gates

**ResourceQuota** caps total resources usable in a namespace:
    
      - `requests.cpu`, `requests.memory`, `limits.cpu`, `limits.memory` — total across all Pods.

      - `persistentvolumeclaims`, `requests.storage` — storage objects + total size.

      - Object counts: `pods`, `services`, `secrets`, `configmaps`.

      - Special: `count/{resource}` for arbitrary CRDs.

    
    If a Pod creation would exceed the quota, the Pod is rejected at admission with a clear message. Empower this with PriorityClass scopes (Lesson 23): "this quota only applies to Pods at priority < standard," so critical workloads can preempt batch.
    **LimitRange** sets per-Pod or per-container min/max + defaults:
    
      - `default` requests + limits (applied if Pod spec omits them).

      - Min / max — reject Pods outside this range.

      - Default request / limit ratios.

    
    The pair: ResourceQuota caps the tenant's aggregate; LimitRange ensures every Pod has reasonable defaults so they actually count toward the quota. Without LimitRange, a Pod with no resource requests counts as 0 against ResourceQuota — quota becomes meaningless.

## 3. Run the audit, fix what fails

The **CIS Kubernetes Benchmark** is a community-maintained checklist of hardening controls — kubelet flags, API server flags, etcd encryption, RBAC defaults, PSA enforcement, network policy presence. **kube-bench** (Aqua) is the open-source tool that runs the benchmark against a cluster and produces pass / fail / warn results.
    Typical first-run findings:
    
      - API server: `--anonymous-auth=false` not set (anonymous requests allowed).

      - Kubelet: `--read-only-port=10255` still open (deprecated, leaks metrics).

      - etcd: client cert auth not enforced.

      - Default ServiceAccount: has automount enabled.

      - No audit policy configured.

    
    Run kube-bench on every cluster on a schedule (e.g., a CronJob with the kube-bench image). Pipe results into PolicyReports or a SIEM. Track score over time as a metric.
    For managed clusters (EKS, GKE, AKS), some controls are not your responsibility (the cloud manages the API server). kube-bench has provider-specific profiles — pick the right one to avoid false alarms on cloud-managed components.

## 4. When flat namespaces aren't enough

Flat namespaces work fine for ~50 tenants. Beyond that, the policy soup gets unwieldy: every new namespace needs a NetworkPolicy, ResourceQuota, RBAC bindings created. Two patterns scale:
    
      - **HierarchicalNamespaces (HNC)** — a CRD that creates parent/child relationships. RBAC + NetworkPolicy + ResourceQuota inherit from parent to child. Tenant gets a parent namespace; sub-environments (dev / staging / prod) are child namespaces. Policy maintained at the parent.

      - **Cluster-API + per-tenant clusters** — for hard multi-tenancy, give each tenant a dedicated cluster managed via Cluster API. More overhead, complete isolation.

      - **vCluster** — runs a virtual K8s API server inside a host cluster's Pod. Tenants get a real K8s cluster experience (their own kube-apiserver, schedulers, CRDs) without provisioning real nodes. Isolation by virtualisation.

    
    Other isolation knobs:
    
      - **Node pools per tenant** — taint nodes; only tenant's SA can tolerate. Reduces noisy-neighbour and kernel-shared-attack-surface.

      - **Kata Containers / gVisor** — runtime-level sandbox. Each Pod runs in a lightweight VM (Kata) or syscall-filtering process (gVisor). Defense-in-depth against kernel exploits.

      - **Pod-to-Pod mTLS via service mesh** — Lesson 43. Adds identity-aware encryption to soft tenancy.

    
    [ deep dive — skip if new ]The 2026 reality: most enterprise multi-tenancy is soft tenancy with the standard stack (RBAC + ANP + PSA + Quota + LimitRange) plus per-tenant node pools for noisy-neighbour control. Hard tenancy (truly untrusted users running arbitrary code) is rare outside of CI build runners, Jupyter notebook hosting, and similar use cases — those should use vCluster or separate clusters.

## Before / After

**Before.** "We use namespaces for tenants." Reality: tenant A's workload eats every node's memory; tenant B is evicted; cross-tenant network traffic flows freely; nobody noticed someone enabled host networking on a Pod last quarter. Compliance audit reveals 23 CIS findings nobody had time to fix.

**After.** Namespace = RBAC + ANP + PSA + ResourceQuota + LimitRange. Per-tenant node pools for noisy-neighbour control. kube-bench scoring tracked as a metric, baseline: 95%+. New tenant onboarding = a Helm chart that lays down all the boilerplate. Auditor pulls a kube-bench report; sees compliance evidence.

Namespaces don't isolate; *policy stacks* isolate. The cluster's safety is the sum of its policies.

## Analogy — the K-Town district

From the Watchtower we look down at K-Town's tenant district: a fenced grid of compounds, each with its own gate, RBAC plaque on the door, NetworkPolicy fence around it, posted PSA standard on the wall, and a metered utility meter (ResourceQuota) that cuts power when the tenant exceeds their allocation. A separate watchtower department runs a regular CIS audit (kube-bench) and posts the city's overall score on a noticeboard. New tenants get a standard build (a Helm chart laying all this down). For sensitive operations (banks, ML training labs), tenants get either an isolated wing (per-tenant node pool) or their own out-building (vCluster / separate cluster).

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Compound fence | `NetworkPolicy` + `AdminNetworkPolicy` |
| RBAC plaque on the door | `Role` / `RoleBinding` per namespace |
| Posted PSA standard | `pod-security.kubernetes.io/enforce` label |
| Metered utility meter | `ResourceQuota` |
| Default fixture sizes | `LimitRange` |
| Citywide CIS audit | kube-bench against CIS Kubernetes Benchmark |
| Compound family tree | HierarchicalNamespaces (HNC) |
| Isolated outbuilding | vCluster / per-tenant cluster |
| Hardened delivery vehicle | Kata Containers / gVisor |

⚠️ *Analogy stops here:* The analogy stops here: K8s tenants don't have a real fence — every namespace shares the underlying nodes. "Isolation" is a sum of policies; for true isolation use vCluster, Kata, or separate clusters.

## ELI5 / ELI10

**ELI5.** Each kid gets their own room with their own toys, their own snack budget, and a list of rules on the door. They can't go into other kids' rooms. The grown-ups check the rule lists are still up.

**ELI10.** Multi-tenancy in K8s is layered policy. Per namespace: RBAC restricts visibility/actions, NetworkPolicy or ANP restricts traffic, PSA enforces Pod-security profile, ResourceQuota caps total resource use, LimitRange enforces sane per-Pod defaults. kube-bench scores the whole cluster against the CIS Kubernetes Benchmark; treat the score as a tracked metric. For scale, HierarchicalNamespaces (HNC) lets policies cascade down a namespace tree. For untrusted tenants, escalate to vCluster, Kata Containers, gVisor, or separate clusters.

## Real-world scenarios

- **A SaaS with 200 tenant namespaces.** HNC for tenant tree (parent: org, children: dev/staging/prod). NetworkPolicy + RBAC inherited from parent. Per-namespace ResourceQuota + LimitRange laid down by a Kyverno generate policy when a new namespace is created. Onboarding new tenant: 1 Helm release. Time-to-isolated-tenant: 5 minutes.
- **A bank running per-tenant node pools.** Tenants tagged by sensitivity: `sensitivity=public`, `sensitivity=internal`, `sensitivity=restricted`. Node pools tainted matching. Public tenants can't reach restricted nodes; restricted Pods can't share kernels with less-trusted ones. Combined with PSA-restricted profile + Falco runtime monitoring.
- **A startup running CI build pods.** Each PR builds in an ephemeral namespace with vCluster (isolated K8s API). Build job runs in Kata Containers (lightweight VM per Pod). Tenant code can't escape into the host cluster. After CI, namespace is deleted via Kyverno cleanup policy.
- **A team using kube-bench in CI.** Every cluster runs kube-bench daily as a CronJob, output piped to S3. CI pipeline pulls latest report; fails if score drops below 92%. Average score: 96%, with the 4% being known-acceptable findings (audit log centralisation pending). Compliance auditor receives the historical trend.

## Common misconceptions

- **Myth:** Namespaces are security boundaries.
  **Truth:** They're organisational boundaries. Security comes from layered policy: RBAC + NetworkPolicy + PSA + Quota + LimitRange. Without them, a namespace is just a name prefix.
- **Myth:** ResourceQuota alone protects against noisy neighbours.
  **Truth:** Without LimitRange providing defaults, Pods can submit with zero requests and not count against quota. Always pair them. Many real outages start here.
- **Myth:** kube-bench has to be 100% to be useful.
  **Truth:** 100% is rarely realistic — some controls don't apply to your setup, some are deliberately exempted. Track the trend, document exceptions, focus on closing the gaps that matter (RBAC, PSA, audit log).

## Recap

Namespaces aren't security boundaries; layered policy is. RBAC + NetworkPolicy + PSA + ResourceQuota + LimitRange make a namespace approximate a tenant. kube-bench tracks CIS compliance. HNC scales policy. For untrusted tenants: vCluster, Kata, separate clusters.

**Next — Lesson 32: Observability Part 1.** Module 14 begins. Logs and metrics — the core observability signals, OpenTelemetry, Prometheus + push gateway alternatives, log pipelines (Vector, Fluent Bit). New K-Town district: Observatory.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
