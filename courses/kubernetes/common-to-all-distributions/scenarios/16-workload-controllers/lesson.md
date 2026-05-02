# Lesson 16 — Workload Controllers · Deployment, StatefulSet, DaemonSet, Job, CronJob

> Course: Kubernetes — Common to all distributions
> Module 4 · Workloads · Lesson 1 of 5
> Companion preview: `/preview-kubernetes-lesson-16.html`.

---

**🎯 If you remember nothing else:** Five workload controllers, each for a specific shape of work — match shape to controller, the rest is mostly tuning.

## Before / After

**Before.** Manage workloads as raw Pods + scripts. Restart by hand. Scale by editing YAML. No standardised rollout. Configuration drift between environments is common.

**After.** Five workload controllers cover ~95% of needs. Deployment for stateless, StatefulSet for stable identity, DaemonSet for per-node, Job/CronJob for batch. Rolling updates declarative. Scale via HPA. Drift impossible because git is source of truth.

K8s's workload controllers are the most-used surface of the API. Get the pattern matching right and most operational complexity disappears.

## Analogy — the K-Town district

K-Town's Dispatch Office handles every kind of work assignment. **Rotating shifts** (Deployments) — anyone can take any slot, last shift's worker rolls off as the next rolls on. **Assigned-seat workers** (StatefulSets) — Anna always at desk-0, Brian at desk-1, even after a break. **Per-building watchmen** (DaemonSets) — exactly one per building. **One-time work orders** (Jobs) — do this and report back. **Scheduled rounds** (CronJobs) — every Tuesday at 2 AM, do that.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Rotating shifts (interchangeable workers) | Deployment + ReplicaSet |
| Assigned-seat employees (Anna at desk-0) | StatefulSet |
| Per-building watchman | DaemonSet |
| One-time work order | Job |
| Scheduled maintenance round | CronJob |
| "Cover the shift no matter who" | Rolling update strategy |
| "Anna's badge stays Anna's badge" | Stable Pod identity in StatefulSet |

⚠️ *Analogy stops here:* Real K8s controllers don't 'dispatch workers' — they reconcile observed state with desired state in a control loop. The dispatch metaphor undersells the level-triggered, idempotent reconciliation that's the secret to K8s's robustness.

## ELI5 / ELI10

**ELI5.** Five kinds of jobs at the dispatch office. Some workers can swap places (Deployment). Some always sit at the same desk (StatefulSet). Some are stationed at every building (DaemonSet). Some come in once for one task (Job). Some come in every Tuesday (CronJob).

**ELI10.** Five workload controllers for five shapes of work: Deployment (stateless, rolling updates), StatefulSet (stable Pod names + per-replica PVCs + ordered startup), DaemonSet (one Pod per node — agents, log shippers), Job (run-to-completion — backoffLimit + completions + parallelism), CronJob (Job on a schedule). Pick by shape; don't fight the model.

## Real-world scenarios

- **A SaaS using Deployment + HPA for stateless web.** Deployment with replicas tied to HPA. Rolling updates happen automatically on image bumps (via Argo CD or kubectl set image). Service in front routes to the current ReplicaSet. Cookie-cutter K8s pattern that works at any scale.
- **A bank running PostgreSQL on StatefulSet.** Three replicas (postgres-0 primary, postgres-1/2 replicas). Each has its own PVC via volumeClaimTemplates. Headless Service for clients to address specific Pods (postgres-0.postgres.namespace.svc). StatefulSet handles rolling restarts in reverse-ordinal order during upgrades.
- **A team running Falco as a DaemonSet for runtime security.** One Falco Pod per node. Watches kernel syscalls via eBPF. Cluster-wide visibility without per-Pod overhead. Tolerations on master nodes too — security applies everywhere.
- **A startup's image-resize Job.** Customer uploads → SQS message → CronJob (every 1 min) checks queue. If items present, spawns Job to drain them. Job creates Pods that process N images then exit. Failed Pods retry up to backoffLimit; after that, Job marked Failed and alerted.

## Common misconceptions

- **Myth:** Deployments and ReplicaSets are interchangeable.
  **Truth:** Deployment is the higher-level abstraction; it manages ReplicaSets to do rolling updates. You write Deployment; you read ReplicaSet history. Direct ReplicaSet usage is rare.
- **Myth:** StatefulSet is required for any Pod with state.
  **Truth:** StatefulSet is required for stable identity + per-replica storage. A single-replica stateful app can run as a Deployment with a PVC. The bar is: do you need stable, predictable Pod names + ordered startup? If yes, StatefulSet.
- **Myth:** CronJob's schedule is reliable.
  **Truth:** It's best-effort. If the cluster is busy or the previous Job is still running, the next schedule may be skipped (per concurrencyPolicy). For mission-critical scheduling, layer on top: monitoring + alerting on missed runs.

## Recap

Five workload controllers cover almost every shape of work in K8s. Match the shape to the controller; the rest is tuning replicas, probes, and resource requests.

Next — Lesson 17: Services & Networking. The other half of the workload story: how Pods reach each other and how the world reaches in.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
