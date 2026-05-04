# K-ADV-AI I2 — I2 · Kueue + MultiKueue + Volcano Gang Scheduling

> Course: K-ADV-AI (advanced specialization)
> Module I2 · Kueue + Volcano
> Companion preview: `/preview-kubernetes-adv-ai-lesson-02.html`.

---

**🎯 If you remember nothing else:** **Kueue: K8s batch admission with quota. Volcano: gang scheduling for multi-Pod jobs. MultiKueue: federate batch across many clusters. Together: AI / batch workloads with quota + admission + gang + fleet.**

## 1. ResourceFlavor + ClusterQueue + LocalQueue + Workload

**ResourceFlavor**: cluster's capacity slice (e.g., "H100-flavor"). **ClusterQueue**: cluster-scoped queue declaring quota per ResourceFlavor + cohort + preemption rules. **LocalQueue**: namespace-scoped pointer to ClusterQueue. **Workload**: Kueue-tracked job (Job / JobSet / RayJob / MPIJob).
    Tenant submits Job to LocalQueue; Kueue admits if quota available; Pods then schedule normally.

## 2. all-or-nothing + min-member + queue priorities

**Volcano** scheduler runs alongside or replaces kube-scheduler. Schedules *PodGroup* (gang) atomically: all min-member Pods schedule together or none do.
    Avoids the half-running half-pending failure mode for distributed training. PodGroup priorities + queue admission supplement default scheduling.

## 3. Submit once; runs in any cluster with capacity

**MultiKueue**: control-plane Kueue cluster federates worker Kueue clusters. Tenant submits Workload to control plane; MultiKueue routes to worker cluster with capacity.
    Wins: *burst across clouds*, *multi-region GPU pools*, *spot-fallback*. ML platform spans many clusters; tenants see one queue.

## 4. Job / JobSet / RayJob / MPIJob + Kubeflow integration

Kueue admits standard K8s **Job** + **JobSet** (multi-pod) + **RayJob** (KubeRay) + **MPIJob** (Kubeflow MPI Operator) + **PyTorchJob** / **TFJob** (Kubeflow Training Operator).
    Pattern: Kubeflow Training Operator submits PyTorchJob → Kueue admits → Volcano gang-schedules → distributed training runs. End-to-end batch ML pipeline.

## Before / After

**Before.** Pre-Kueue / Volcano, batch jobs hit ResourceQuota or scheduled per-Pod; distributed training half-stuck; multi-cluster batch impossible without bespoke routing.

**After.** Kueue admits per quota + cohort; Volcano gang-schedules; MultiKueue federates clusters. Tenants submit; platform handles routing + admission + gang.

*Batch + AI workloads need queue + gang + federation; default K8s scheduling alone isn't enough.*

## Analogy — the K-Observatory array

The Observation Queue is the observatory's scheduling office. Astronomers submit observation requests; the queue's admission desk (Kueue) checks quota + admits. The control-room scheduler (Volcano) ensures multi-telescope observations start together — no half-started observations. Multi-observatory federation (MultiKueue) routes observations to whichever facility has capacity.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Observation request | Workload (Job / JobSet / RayJob / MPIJob) |
| Telescope kind quota | ResourceFlavor + ClusterQueue |
| Astronomer's queue ticket | LocalQueue (namespace-scoped) |
| Multi-telescope all-or-nothing | Volcano gang scheduling |
| Multi-observatory routing | MultiKueue federation |
| Quota cohort + preemption | ClusterQueue cohort + preemption |

⚠️ *Analogy stops here:* A real observation queue is paper; Kueue is K8s CRDs continuously reconciled. Quota is dynamic (cohort lending); not just static.

## ELI5 / ELI10

**ELI5.** A queue admits batch jobs to the cluster like a coffee shop's order line. A scheduler ensures multi-cup orders start together. A federation across shops finds a free counter.

**ELI10.** **Kueue**: ResourceFlavor + ClusterQueue + LocalQueue + Workload model. Admits batch (Job / JobSet / RayJob / MPIJob / PyTorchJob) per quota. **Volcano**: gang-schedule PodGroup atomically; all-or-nothing. **MultiKueue**: federate Workloads across clusters; submit once. **Integrations**: KubeRay + Kubeflow Training Operator + MPI Operator.

## Real-world scenarios

- **Distributed training — Volcano gang.** ML team's 16-Pod PyTorchJob hung pending half-up. Migrated to Volcano: PodGroup admits 16 Pods together; training starts cleanly. Throughput up; partial-start incidents zero.
- **Kueue cohort lending.** Two teams share a GPU pool. Each has 8-GPU quota; cohort lends idle quota across teams. Team A bursts to 16 GPU when Team B idle; reverts when B requests. Utilization rises without contention.
- **MultiKueue across clouds.** ML platform fleets across AWS + GCP + on-prem. Tenants submit RayJobs to control-plane Kueue; MultiKueue routes per available capacity. Spot-fallback across clouds; tenant doesn't care which cloud.
- **Outage — non-Kueue partial-fill.** Pre-Kueue, Job's Pods scheduled greedily; partial-fill during high-demand; jobs deadlocked. Postmortem: adopt Kueue + Volcano; gang admit prevents.

## Common misconceptions

- **Myth:** "Kueue replaces ResourceQuota."
  **Truth:** They're complementary. ResourceQuota = per-namespace static cap. Kueue = batch admission + cohort + preemption. Both useful for different patterns.
- **Myth:** "Volcano replaces kube-scheduler."
  **Truth:** Volcano can either replace or run alongside kube-scheduler. Modern pattern: Volcano for gang-scheduled batch; kube-scheduler for everything else. Coexist.
- **Myth:** "MultiKueue is required for multi-cluster ML."
  **Truth:** Optional. MultiKueue is the K8s-native answer. Some platforms use Argo Workflows + custom routing; both work; MultiKueue is the standard for new builds.

## Recap

Kueue admits batch with quota + cohort; Volcano gang-schedules multi-Pod jobs; MultiKueue federates clusters. Together: AI / batch workloads with quota + admission + gang + fleet.

**Next — I3: Ray + Kubeflow + KServe + JobSet.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
