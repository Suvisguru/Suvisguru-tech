# Lesson 35 — Reliability & HA · PDB, Multi-Zone, Regional DR

> Course: Kubernetes — Common to all distributions
> Module 15 · Capacity & Resilience · Lesson 2 of 2
> Companion preview: `/preview-kubernetes-lesson-35.html`.

---

**🎯 If you remember nothing else:** Three layers: **PodDisruptionBudget (PDB)** caps voluntary disruptions (drains, autoscaler, upgrades). **Topology spread + zone-aware autoscaling** survives zone failures. **Regional DR** (multi-region GitOps + DNS-level failover, or active-active mesh) survives a region. Most outages are voluntary — get the PDB right, you avoid most of them.

## 1. Voluntary vs involuntary disruption

Pods get killed for two kinds of reasons:
    
      - **Voluntary disruption** — node drain, cluster upgrade, deployment rollout, autoscaler scale-down. The cluster *chose* to disrupt this Pod. K8s respects **PodDisruptionBudgets** here; a PDB-protected workload can't be voluntarily killed if doing so would violate the budget.

      - **Involuntary disruption** — node hardware failure, kernel OOM, zone outage. The cluster didn't choose; it just happened. PDBs don't apply.

    
    Most outages in mature clusters are *voluntary disruptions gone wrong*: an upgrade that drained too many Pods at once, a Karpenter consolidation that nuked a service's only available zone, a manual node drain that ignored PDBs. The single biggest reliability investment is correctly-set PDBs — and they're cheap to write.
    For involuntary disruption, the answer is redundancy: spread across zones, replication, sometimes regions. The cluster can't prevent a hardware failure; it can ensure a hardware failure isn't a service failure.

## 2. The single most important reliability primitive

A **PDB** says: "during voluntary disruptions, keep at least N Pods of this Deployment available" (or "don't disrupt more than M at once").
    `apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: {name: checkout-pdb}
spec:
  selector: {matchLabels: {app: checkout}}
  minAvailable: 6        # never less than 6 ready
  # OR maxUnavailable: 2 # never more than 2 disrupted at once`
    Pick one of `minAvailable` or `maxUnavailable` — not both. Use `minAvailable` when you want a hard floor ("6 must always be running"). Use `maxUnavailable` when you want headroom for rollouts ("only 25% can be down").
    What PDBs actually do:
    
      - Block `kubectl drain` on a node if it would violate the budget. Drain blocks until the violator is rescheduled elsewhere.

      - Block **cluster autoscaler** + **Karpenter** consolidation that would violate the budget.

      - Don't block involuntary disruptions (zone outage, node hardware failure).

    
    Common bug: PDB with `minAvailable: 100%`. The Deployment can never be drained for upgrades; cluster maintenance gets stuck. Set `minAvailable` to a number you can actually sustain (e.g., for a 3-replica service, `minAvailable: 2` = at most 1 down at a time).

## 3. Surviving zone failures

Lesson 22 covered topology spread. For reliability, the rules tighten:
    
      - **Always** spread by `topology.kubernetes.io/zone` with `maxSkew: 1`, `whenUnsatisfiable: DoNotSchedule`.

      - Pair with a `maxUnavailable`-style PDB.

      - Replicas should be ≥ zones (3 zones = ≥3 replicas) to actually populate every zone.

      - For StatefulSets, use `volumeClaimTemplates` with a `WaitForFirstConsumer` StorageClass (Lesson 18). Otherwise the disk gets provisioned in one zone, the Pod can't schedule there, Pod stays Pending forever.

    
    Cluster-level practices:
    
      - Cluster Autoscaler / Karpenter must be aware of zone limits — Karpenter NodePool can specify `topology.kubernetes.io/zone` in its requirements; the scheduler and Karpenter together keep nodes spread.

      - Use **Service`topologySpreadConstraints` with the `topology.kubernetes.io/zone` key** for Service traffic to prefer same-zone targets (reduces inter-zone egress costs; needs careful failure-mode design).

      - Make sure stateful storage (databases, queues) is multi-zone-aware: managed RDS Multi-AZ, regional Cloud SQL, multi-region Cassandra.

    
    The default state of a managed K8s cluster (EKS, GKE, AKS) in 2026 is multi-zone. Single-zone clusters are increasingly rare in production.

## 4. When a region fails

Multi-zone handles single-zone failures. **Regional DR** handles a whole region going down (rare, but it happens — AWS us-east-1 has a 90-minute outage in 2017, 2021, and 2024). Two metrics define the strategy:
    
      - **RPO** (Recovery Point Objective) — how much data loss is acceptable? "Up to 5 minutes" = sync state to DR every 5 min.

      - **RTO** (Recovery Time Objective) — how fast must you be back up? "15 minutes" = automated failover; "1 hour" = manual.

    
    Three patterns:
    
      - **Cold DR** — DR cluster exists but inactive. State backed up nightly. Failover involves spinning everything up. RPO: 24h, RTO: hours. Cheap; significant data loss possible.

      - **Warm DR** — DR cluster running but smaller. Continuous data replication. Failover scales up. RPO: minutes, RTO: 15-30 min. Moderate cost.

      - **Active-Active** — both regions serving traffic. Stateful tier replicates bidirectionally (Cassandra, CockroachDB, multi-region Spanner). RPO: 0, RTO: seconds. Expensive; complex consistency.

    
    Most enterprise-K8s setups in 2026 use **warm DR with GitOps**: same manifests deployed to two clusters in two regions; one is primary; database replicates across; DNS-level failover (Route53, Cloud DNS, Cloudflare) flips on detection. The exact same Deployment / Service / HPA / etc. lives in both clusters, deployed by the same Argo CD or Flux.
    [ deep dive — skip if new ]The real reliability practice: **chaos engineering**. Run periodic experiments — "kill a zone," "kill 50% of Pods," "increase latency to one dependency" — and verify the cluster recovers. Tools: Chaos Mesh, LitmusChaos. Without periodic testing, your DR plan is hypothesis. Game-day every quarter is the discipline difference between teams that survive incidents and teams that learn during them.

## Before / After

**Before.** Pre-PDB: rolling cluster upgrade kills 80% of replicas of a service in 30 seconds because the upgrade tooling didn't check budgets. Outage. Post-mortem: "we should have been more careful." Single-zone deploys: zone failure = full outage. "Disaster recovery" = a 47-page wiki page nobody has tested.

**After.** PDBs on every production Deployment. Drains respect them; consolidation respects them; upgrades respect them. Multi-zone topology spread is mandatory; zone failures cause minutes of degradation, not hours of outage. Regional DR via warm-standby + GitOps; quarterly game-days verify it works.

PDBs are the cheapest reliability investment in K8s — three lines of YAML per Deployment. Almost every "K8s outage during a rollout" story has a missing PDB at its core.

## Analogy — the K-Town district

The Power Station's resilience floor has three controls. The **maintenance interlock** (PDB) prevents the operator from taking too many generators offline at once — "you must keep 6 running; before you take generator 7 offline, you have to start a replacement." The **multi-zone wiring** (topology spread + zone-aware nodes) ensures your generators are spread across the city's three districts so a district outage doesn't kill all of them. The **regional substation** (DR) is the second power station in a different city, kept warm, ready to take over when this city's station goes dark. Three layers, each handles a different failure scope.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Maintenance interlock | `PodDisruptionBudget` |
| "You must keep 6 running" | `minAvailable: 6` |
| "At most 2 down at once" | `maxUnavailable: 2` |
| Generators spread across districts | Topology spread by zone |
| Hardware failure (involuntary) | Pod killed by zone/node failure |
| Operator-initiated maintenance (voluntary) | Pod evicted by drain / autoscaler / upgrade |
| Second power station in another city | Regional DR cluster |
| How fresh is the second city's data? | RPO (Recovery Point Objective) |
| How fast can the second city take over? | RTO (Recovery Time Objective) |
| Practising failover quarterly | Chaos engineering / game-days |

⚠️ *Analogy stops here:* The analogy stops here: real K8s disruption is bound by Linux process termination + Pod lifecycle, not generators. And regional DR depends heavily on stateful tier (databases, message queues) being designed to replicate — without that, the K8s layer alone can't fail over.

## ELI5 / ELI10

**ELI5.** Three rules for keeping the lights on. (1) Don't turn off too many bulbs at the same time. (2) Spread bulbs across rooms. (3) Have a backup house with a backup set of bulbs.

**ELI10.** Voluntary disruption (drains, upgrades) is bounded by PDBs. Involuntary disruption (hardware failure) is mitigated by replication + topology spread. Multi-zone is mandatory for production; replicas ≥ zones; PVCs use WaitForFirstConsumer SCs. Regional DR has three patterns: cold (cheap, slow), warm (moderate), active-active (expensive, fast). RPO + RTO define the trade. Practice failover quarterly; without testing, your DR plan is fiction.

## Real-world scenarios

- **A SaaS surviving a zone outage in 30 seconds.** 6-replica Deployment, topology spread by zone (3-3-3), PDB minAvailable=4, 3-zone EKS cluster. Zone-A goes down. 4 healthy Pods continue serving (slightly degraded throughput). HPA scales up; Karpenter provisions in zones B/C. Within 60 seconds, full capacity restored. Engineers see the alert + the auto-recovery in the same minute.
- **A bank running active-active across us-east-1 and us-west-2.** Two clusters, identical Argo CD deploys. CockroachDB across regions for stateful tier; Cassandra for high-write traffic. AWS Global Accelerator routes by latency. Half the traffic each region. Quarterly game-day: take down us-east-1 entirely; verify us-west-2 absorbs 100% of traffic. Last 4 game-days: clean.
- **A startup with cold DR (cheap).** Primary cluster only. Nightly Velero backups to S3. Manifests in git via Argo CD. DR runbook: spin up new cluster, restore Velero backup, point DNS. RTO: ~4 hours. RPO: ~24 hours. Sufficient for their stage; will upgrade to warm DR pre-IPO.
- **A platform team running quarterly chaos days.** Chaos Mesh experiments scheduled monthly: random Pod kills, network partitions, simulated zone outages. Findings drive PDB tightening, dashboards, runbooks. After 4 chaos days, MTTR for production incidents dropped 60%. "What we learned in chaos" became a KPI.

## Common misconceptions

- **Myth:** PDBs prevent all Pod kills.
  **Truth:** PDBs only block *voluntary* disruptions (drain, autoscaler, upgrade). Hardware/zone failures bypass PDBs entirely. PDBs are reliability for planned changes, not disasters.
- **Myth:** Topology spread alone is enough.
  **Truth:** Topology spread without a PDB means an upgrade can still kill all your Pods at once if it bypasses budgets. Pair them. Spread for placement; PDB for disruption rate.
- **Myth:** DR = backup.
  **Truth:** Backup is data recovery. DR is service continuity. Backups don't mean fast recovery — restoring 10 TB of database from S3 is 12+ hours. DR means active redundancy that can take over fast.

## Recap

PDBs cap voluntary disruptions; topology spread + multi-zone survives zone failures; regional DR (warm or active-active) survives a region. The cheapest reliability investment is a correctly-set PDB on every production Deployment.

**Next — Lesson 36: Kustomize.** Module 16 begins — application delivery. New K-Town district: Print Shop. Why YAML duplication is the single biggest source of Ops toil, and how Kustomize's overlay model addresses it.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
