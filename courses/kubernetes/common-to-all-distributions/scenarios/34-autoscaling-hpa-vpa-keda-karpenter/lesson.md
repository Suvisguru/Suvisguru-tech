# Lesson 34 — Autoscaling · HPA, VPA, KEDA, Cluster Autoscaler, Karpenter

> Course: Kubernetes — Common to all distributions
> Module 15 · Capacity & Resilience · Lesson 1 of 2
> Companion preview: `/preview-kubernetes-lesson-34.html`.

---

**🎯 If you remember nothing else:** **Workload scaling**: HPA (CPU/memory/custom metrics), VPA (right-size requests), KEDA (event-based — queue depth, Kafka lag, etc.). **Cluster scaling**: Cluster Autoscaler (legacy, node-group based) or **Karpenter** (modern, fast, picks instance type per Pending Pod). Combine for end-to-end scaling.

## 1. Two scaling layers, two different problems

**Workload scaling** answers "how many replicas of this Deployment do I need?" Driven by signals: CPU, memory, queue depth, RPS, custom metrics. Adjusts the `replicas` field on Deployments / StatefulSets.
    **Cluster scaling** answers "how many nodes does the cluster need?" Driven by Pending Pods ("there are Pods that don't fit, add nodes") and idle nodes ("this node has no Pods, remove it"). Adjusts the cloud auto-scaling group / instance fleet.
    The two interact. Scaling Pods up creates Pending Pods → triggers cluster scale-up. Scaling Pods down empties nodes → triggers cluster scale-down. Get one without the other and you either over-spend (lots of nodes, few Pods) or have outages (lots of Pods, no nodes).

## 2. Replica scaling on metrics

**Horizontal Pod Autoscaler (HPA)** scales the replica count based on observed metrics. Built-in metrics: CPU and memory utilisation as % of requests. External / custom metrics: anything Prometheus can serve via the Prometheus Adapter or external metrics adapter.
    The math: "if the average CPU per replica is 80% but target is 50%, increase replicas to bring the average down." Specifically: `desired = ceil(current_replicas × current_metric / target_metric)`.
    Modern HPA (autoscaling/v2) supports:
    
      - **Multiple metrics** — scale to whichever requires more replicas (CPU OR queue depth, take the max).

      - **Behaviour** — separate scale-up and scale-down policies. Scale up fast (double per minute) to handle spikes; scale down slow (10% per 5 min) to avoid flapping.

      - **Stabilisation windows** — "don't scale down until the lower number is sustained for 5 minutes."

    
    Common mistakes:
    
      - HPA without resource requests on the Pods — HPA can't calculate utilisation; it does nothing.

      - HPA on a Deployment that uses `replicas:` in the manifest — the next `kubectl apply` resets to the manifest value, fighting HPA. Use a HelmChart that omits replicas, or detach replicas from GitOps drift detection.

      - Memory-based HPA on apps that don't release memory — replicas only grow.

## 3. Two specialised cousins of HPA

**Vertical Pod Autoscaler (VPA)** doesn't change replica count — it changes per-Pod resource requests. The recommender component watches actual usage; over time, it suggests "this Pod uses 200m CPU on average; you have 500m requested; lower it to 250m." The updater component evicts Pods to apply the new sizing.
    VPA modes:
    
      - `Off` — recommend only; don't apply.

      - `Initial` — apply at Pod creation time.

      - `Auto` / `Recreate` — evict + recreate Pods to apply.

      - `InPlaceOrRecreate` (1.33+) — try in-place resize without evicting; fall back if the kernel doesn't allow it.

    
    VPA's sweet spot: workloads with predictable resource usage where right-sizing yields cost savings. Avoid for HPA-targeted workloads (HPA + VPA fighting each other).
    **KEDA** (Kubernetes Event-Driven Autoscaling) extends HPA with custom "scalers": Kafka lag, RabbitMQ queue depth, Postgres row count, S3 object count, Azure Event Hubs, GCP Pub/Sub, AWS SQS, and 60+ more. KEDA can scale a Deployment to **zero** when there's no work — perfect for event-driven workloads. It then re-creates Pods on first event arrival.
    KEDA is now widely deployed for: queue workers, scheduled batch jobs that should disappear off-hours, ML inference services with bursty demand, and serverless-style K8s workloads.

## 4. The most consequential ops change of 2024-26

**Cluster Autoscaler (CA)** is the original. Watches for Pending Pods; if any can't fit, scales up the matching auto-scaling group (ASG). Scales down idle nodes. Works fine; predictable.
    **Karpenter** (AWS-originated, now multi-cloud) is the modern replacement:
    
      - **No node groups required** — Karpenter picks the best instance type per Pending Pod. "Need 2 GPUs and 32 GiB? I'll spin up a g5.xlarge. 0.25 CPU and 256 MiB? I'll use a t3.nano."

      - **Faster** — Karpenter spins up nodes in 20-40 seconds. CA goes through ASG APIs and is typically 60-120s.

      - **Cost-aware** — picks the cheapest instance that fits constraints; tracks spot prices.

      - **Consolidation** — periodically checks if running nodes can be replaced with fewer/cheaper ones; drains and recreates.

      - **Multi-cloud** — originally AWS, now production-ready on Azure (KAITO derivatives) and GCP.

    
    Karpenter's trade-off: more dynamic node identities ("one node per Pod request" can mean many small nodes) — operational tooling that assumes long-lived nodes (e.g., manual SSH, node-bound persistent state) doesn't fit. Most teams adopt Karpenter and design around it.
    [ deep dive — skip if new ]The 2026 default for new EKS clusters is Karpenter, not CA. AWS has been pushing it heavily. The migration story (CA → Karpenter) is straightforward: install Karpenter, let it manage new nodes, drain old ASG nodes, decommission CA. Most clusters complete the migration in a sprint.

## Before / After

**Before.** Pre-autoscaling: hand-tuned `replicas: 8`. Over-provisioned for normal load (4-5 replicas would do); under-provisioned for peaks (need 30 replicas). Cluster nodes provisioned for max + headroom; expensive idle capacity 90% of the time. Manual scale-up during incidents. Frequent fights between dev ("we need more capacity") and finance ("why is the cluster bill so high?").

**After.** HPA on every Deployment based on actual demand signals. KEDA scales queue workers 0 → 50 based on actual queue depth. Karpenter spins up the cheapest instance type per Pending Pod, consolidates idle capacity. Cluster bill drops 30-50% while peak handling improves. Finance and dev are friends.

Karpenter's 2024-26 dominance turned cluster-autoscaling from "sluggish ASG churn" into "actually-real-time capacity matching." New clusters default to it; old clusters migrate.

## Analogy — the K-Town district

The Power Station district runs K-Town's capacity. Inside, three demand meters tell the operator how loaded the system is. The **load meter** (HPA) shows "current generators are at 80% capacity — fire up another" — and adjusts the number of *generators* running. The **generator-size meter** (VPA) says "this generator was sized for 1000 kW but uses 400 — replace it with a smaller one." The **queue meter** (KEDA) watches incoming work orders: "50 customers waiting; spin up a few more dedicated lines." Outside, the substation manager (Cluster Autoscaler / Karpenter) handles the actual generators — when the operator says "more capacity!" they procure additional generators from the city's rental fleet, picking the cheapest fit.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The load meter | `HorizontalPodAutoscaler` (HPA) |
| The generator-size meter | `VerticalPodAutoscaler` (VPA) |
| The queue meter | **KEDA** |
| Generator (running unit of capacity) | Pod replica |
| The substation manager | **Karpenter** / **Cluster Autoscaler** |
| Generator rental fleet | Cloud instance fleet (EC2, Compute Engine, etc.) |
| Picking generator type per order | Karpenter NodeClass / NodePool selection |
| Combining old generators into fewer big ones | Karpenter consolidation |
| Generator running on cheaper short-term contract | Spot instances |

⚠️ *Analogy stops here:* The analogy stops here: Pods aren't generators; their state matters (StatefulSet ordinality, PVC binding, in-flight requests). Naive scale-down is destructive — Pod-disruption-budgets + graceful termination matter. Lesson 35 covers the reliability side.

## ELI5 / ELI10

**ELI5.** Two thermostats. One says how many lights to turn on (more people = more lights). One says how many extra rooms to open in the house (more people = more rooms). Together they keep things just right.

**ELI10.** Workload scaling: HPA (replica count by CPU/memory/custom metrics), VPA (per-Pod request right-sizing), KEDA (event-driven scalers — queue depth, Kafka lag, etc., scale-to-zero supported). Cluster scaling: Cluster Autoscaler (legacy, node-group based) or Karpenter (modern, picks instance type per Pending Pod, faster, cost-aware, consolidation). HPA needs resource requests to compute utilisation. Don't pair HPA + VPA on the same Pod (they fight). For 2026 EKS clusters, default to Karpenter.

## Real-world scenarios

- **A SaaS using HPA + Karpenter.** HPA on every Deployment based on CPU + custom metric (request rate via Prometheus Adapter). Karpenter dynamically provisions m6i (general) and t3 (burstable) instances based on Pod size. Spot instances for stateless. Black Friday spike handled in 90 seconds end-to-end (Pod scale + node scale).
- **A bank with KEDA-driven Kafka workers.** Stream-processing service scales 0 → 100 based on Kafka consumer lag. KEDA scaler reads lag from Prometheus; HPA derived from KEDA scales the Deployment. Off-hours: 0 Pods. Lag detected: scale to 50 within 30 seconds. Total cost saved per quarter: significant.
- **A startup using VPA in Initial mode.** VPA recommends; only applies at Pod creation (no live evictions). Engineers see VPA recommendations on a Grafana panel; review weekly. New deploys get the right-sized requests automatically. Existing Pods kept until rolling deploy. CPU/memory waste cut by 40%.
- **A team migrating CA → Karpenter.** Old: 4 ASGs (general / memory / GPU / spot). Karpenter replaces with 4 NodePools, but lets it pick instance types within each. Spinup time dropped from 90s to 30s. Idle capacity dropped (Karpenter consolidates). Operational tooling that SSH'd into specific node names broke; rewrote to use kubectl-only instead.

## Common misconceptions

- **Myth:** HPA + VPA on the same Pod is more powerful.
  **Truth:** They'll fight: HPA decides "need more replicas because CPU is high" while VPA decides "increase per-Pod CPU request because actual usage is high." Both can work simultaneously only with VPA in `Off`/`Initial` mode (recommend, apply at create) — never with VPA `Auto`.
- **Myth:** KEDA replaces HPA.
  **Truth:** KEDA *extends* HPA. KEDA scalers compute "desired replicas" then create an HPA object on your behalf. Underneath, it's still HPA. KEDA's value is the scaler library + scale-to-zero.
- **Myth:** Karpenter is AWS-only.
  **Truth:** Originally yes; in 2026 supported on Azure (with Microsoft's KAITO + community drivers), GCP (community), and being explored on others. AWS is still the strongest support; new on other clouds.

## Recap

Workload scaling (HPA/VPA/KEDA) + cluster scaling (Karpenter or CA) match capacity to demand end-to-end. HPA needs requests; KEDA scales by event signals; VPA right-sizes; Karpenter picks instance types per Pod and consolidates aggressively.

**Next — Lesson 35: Reliability & HA.** The flip side of autoscaling — staying up under failures. PodDisruptionBudgets, multi-zone topology, regional disaster recovery, the chaos engineering loop.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
