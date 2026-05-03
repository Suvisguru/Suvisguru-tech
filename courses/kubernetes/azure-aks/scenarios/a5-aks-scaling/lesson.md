# K-AKS A5 — A5 · AKS Scaling (Cluster Autoscaler, NAP, KEDA, Spot, GPU, ARM, Confidential)

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A5 · AKS Scaling
> Companion preview: `/preview-kubernetes-aks-lesson-05.html`.

---

**🎯 If you remember nothing else:** **Cluster Autoscaler is per-pool min/max for fixed shapes; NAP (AKS Karpenter) provisions any shape on demand. KEDA scales Pods on events. Use Spot + ARM for cost; GPU/Confidential for special workloads. PDBs guard maintenance drains.**

## 1. Cluster Autoscaler — the per-pool primary

**Cluster Autoscaler (CA)** is the default node-side autoscaler in AKS Standard. Per node pool: set `--min-count` and `--max-count`. CA watches for unschedulable Pods and scales the pool out (up to max); watches underutilised nodes and scales in (down to min, respecting PDBs).
    
      - **Mental model:** CA reasons about *VMSS scale operations*, not individual nodes. Scale operations have minute-scale latency.

      - **Per-pool tuning:** `scale-down-delay-after-add`, `scale-down-unneeded-time`, `scan-interval`, `balance-similar-node-groups`.

      - **Limits:** CA can only scale within an existing pool's VM SKU. Mixing instance shapes = many pools = operational overhead. CA also can't pick spot vs on-demand dynamically — that's a different pool.

      - **PDB-aware drains:** when scaling in or upgrading, CA drains nodes respecting PodDisruptionBudgets. A workload with `maxUnavailable: 0` + min replicas = blocking. Set PDBs that don't deadlock scale-down.

## 2. Node Auto Provisioning — Karpenter for AKS

**Node Auto Provisioning (NAP)** is AKS's implementation of the Karpenter autoscaler — the same primitives EKS users know. *Default in AKS Automatic.* Available in preview for AKS Standard.
    
      - **How it differs from CA:** instead of per-pool min/max, NAP looks at the whole pool of Pending Pods and computes a near-cost-optimal node mix on the fly. Pick from a wide SKU catalog (D-series, B-series, ARM, spot mixes), not a fixed pool.

      - **NodePool + NodeClass** (K8s CRDs) — declare the workload's requirements (instance family, max-CPU, OS, zones) and Azure picks the cheapest fitting SKU. Aged-node lifecycle: NAP replaces nodes after a `expireAfter` ttl (default 21 days) — no patch debt.

      - **Consolidation:** NAP periodically re-bins Pods onto fewer nodes when utilisation drops, then terminates the empty nodes. *Idle-spend reduction without manual intervention.*

      - **When to pick NAP over CA:** mixed workloads where node-shape diversity matters; cost optimisation across spot/on-demand/ARM; teams that want fewer pools to manage.

## 3. KEDA — event-driven Pod scaling (managed add-on)

**KEDA (Kubernetes Event-Driven Autoscaler)** is a managed AKS add-on that scales Pods on external events, not just CPU/memory. *Default in AKS Automatic.*
    
      - **Scalers** (60+): Azure Service Bus queue depth, Storage Queue depth, Event Hub backlog, Cosmos DB lease changes, Kafka lag, RabbitMQ, Cron schedules, Prometheus query, custom (your own metric).

      - **ScaledObject** CRD wraps a Deployment + scaler config. KEDA creates an HPA under the hood; injects external metrics into the K8s metrics API; HPA reacts.

      - **Scale-to-zero:** KEDA is the canonical way to scale to *zero replicas* when there's no event. CPU-based HPA can't do this (it needs at least 1 Pod to read CPU from). KEDA can — service bus has 0 messages → 0 replicas → 0 cost.

      - **Combining with HPA:** ScaledObject can also reference standard CPU/memory metrics; one Deployment can scale on "queue depth OR CPU".

    
    **VPA (Vertical Pod Autoscaler):** right-sizes Pod requests over time based on observed usage. Useful for workloads with poorly-tuned CPU/memory requests. *Cannot use with HPA on the same metric*.

## 4. Specialty node pools — Spot, GPU, Windows, ARM, Confidential

Beyond the standard System / User pools, AKS supports several specialty pools. Each is a separate node pool — combine pools per cluster.
    
      - **Spot pool** — Spot VMs, up to 90% off, evictable on 30 seconds notice. Auto-tainted `kubernetes.azure.com/scalesetpriority=spot:NoSchedule`; workloads must tolerate. Ideal: batch jobs, ML training, fault-tolerant queue workers.

      - **GPU pool** — NC-series (NVIDIA T4 / A100 / H100) or ND-series. AKS GPU image (`UbuntuGPU`) ships drivers preinstalled; alternative is the NVIDIA GPU Operator. Pods request `nvidia.com/gpu: 1`.

      - **Windows pool** — Windows Server 2022 nodes for .NET Framework workloads. Mixed Linux+Windows clusters are normal.

      - **ARM pool** — Azure Cobalt 100 / Ampere Altra (D-pls/D-pds-v5). ~25% cheaper than equivalent x86 D-series. Workloads must have ARM64 container images.

      - **Confidential Computing pool** — DCasv5 / ECasv5 SKUs with AMD SEV-SNP. Memory encryption with attestation; for workloads handling regulated PII / financial data needing in-use encryption.

      - **FIPS pool** — node OS configured for FIPS 140-2 cryptography. Required for some US federal compliance contexts.

    
    **Multi-zone scaling:** at pool create, set zones. Pool autoscale spreads across zones. Combine with topology-spread constraints on Pods for tight zone placement.

## Before / After

**Before.** Pre-Karpenter AKS scaling = **Cluster Autoscaler per pool**. Mixed-workload teams ended up with 8-15 node pools (one per workload shape) — operational nightmare. Spot-only meant declaring a separate Spot pool; mixing on-demand with spot in one workload required complex tolerations + nodeAffinity. KEDA add-on existed but was bring-your-own. ARM workloads required separate pool + image discipline. Confidential was preview-only.

**After.** Modern AKS (Automatic by default; NAP add-on for Standard) gives you **Node Auto Provisioning** — declare what your workloads need; Azure picks the optimal node SKUs from the entire catalog on demand, and consolidates during idle. KEDA is a managed add-on (no Helm). Spot, GPU, Windows, ARM, Confidential, FIPS pools are all first-class. Plus PDB-aware drains during planned maintenance windows protect availability. *Right-size happens automatically; you only declare workload intent.*

*The era of pool-sprawl is over. NAP + KEDA + Spot + ARM gives small teams Google-tier elasticity without ops cost.*

## Analogy — the K-Campus wing

The **Auditorium** on K-Campus has chairs that flex with the crowd. Two staffs handle different jobs.
    The **House Manager** (Cluster Autoscaler) walks the rows: "Section A is full → wheel in 5 more chairs from the loading dock; Section A is empty → wheel them back." Section A only has one type of chair (a node pool); if you need bigger chairs, the House Manager opens Section B. *Lots of sections; lots of management.*
    The **Concierge** (Node Auto Provisioning / Karpenter for AKS) is a different staffer: "15 people just arrived — let me look at the warehouse and pick the best chair-mix to seat them all cheaply." The Concierge picks tall chairs for tall people, kid chairs for kids, folding chairs for the budget-conscious — *no fixed sections required*. Later: "Half the seats are empty — let me re-arrange so we use fewer rows and put the unused chairs back."
    The **Door Counter** (KEDA) sits at the entrance: "50 people just queued at the side door (Service Bus) — Concierge, prepare for 50 more chairs." Or: "The side door is empty — bring the chairs back to zero, no Pods running, no cost."
    The Auditorium also stocks *specialty chairs*: discounted folding seats (Spot — cheap, but ushers can ask people to leave with 30s notice), reinforced seats with built-in microscopes (GPU), Microsoft-branded swivel chairs (Windows), eco-friendly bamboo seats (ARM, ~25% cheaper), and lockboxes-with-chairs for sensitive guests (Confidential).

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| House Manager (per-section) | Cluster Autoscaler — per-pool min/max |
| Concierge (whole-warehouse) | Node Auto Provisioning (NAP) / Karpenter for AKS |
| Door Counter (queue depth) | KEDA — event-driven Pod scaling |
| Right-size each chair to the guest | VPA — Vertical Pod Autoscaler |
| Discounted folding seats (30s notice) | Spot node pool |
| Reinforced seats with microscopes | GPU pool (NC/ND-series) |
| Microsoft-branded swivel chairs | Windows Server 2022 pool |
| Bamboo eco seats (~25% off) | ARM pool (Cobalt, Ampere Altra) |
| Lockbox-chairs for sensitive guests | Confidential pool (DCasv5/ECasv5, AMD SEV-SNP) |
| "Don't move chair while someone's in it" | PodDisruptionBudget — protects drains |
| "Spread guests across rows" | topology-spread constraints / multi-zone |

⚠️ *Analogy stops here:* The Auditorium metaphor flattens latency — real-world node provisioning takes 1-3 minutes; consolidation cycles take longer. Pods can't literally "move" without restart unless you're using VPA-in-place (preview).

## ELI5 / ELI10

**ELI5.** The auditorium has clever staff. One says "this section is full — bring more chairs." Another says "forget sections, let me look at everyone and pick the right chair mix." A third stands at the door and says "50 more people are coming, prep extra chairs." Plus they have a few specialty chairs — discount, fancy, big.

**ELI10.** AKS scaling = node-side + Pod-side + specialty pools. **Node-side:** Cluster Autoscaler (per-pool min/max, predictable, simple) or Node Auto Provisioning (Karpenter — picks optimal SKUs across the catalog, consolidates idle). **Pod-side:** HPA (CPU/mem), VPA (right-sizing), KEDA (60+ event scalers, scale-to-zero). **Specialty:** Spot (90% off, 30s eviction), GPU, Windows, ARM (Cobalt/Altra), Confidential (DCasv5 with SEV-SNP), FIPS. PDBs guard drains; multi-zone via pool zones + topology-spread constraints.

## Real-world scenarios

- **Batch workloads on Spot — 70% cost reduction.** A media company runs nightly video transcoding — fault-tolerant, retry-safe. They add a Spot pool autoscaling 0-50 nodes. Workloads tolerate the spot taint and use a checkpoint-resume pattern: if evicted, the next Pod resumes from where the prior left off. Steady-state cost: 70% lower than on-demand. *Eviction rate ~3% — well within their tolerance.*
- **Order-processing — KEDA + Service Bus, scale-to-zero.** An e-commerce backend processes order events from Azure Service Bus. Outside business hours, queue depth = 0 → KEDA scales the Deployment to 0 Pods. During peak: 5K messages/min → KEDA scales to 50 Pods (target = 100 messages/Pod). Outside peak (1 message in 30 minutes): wakes 1 Pod for 5 minutes. *Off-hours infra cost approaches zero.*
- **ML training on GPU spot — A100 sweep at fraction of cost.** An ML team runs hyperparameter sweeps on NC A100 nodes. Single GPU pool: spot, autoscale 0-20. Each training Pod tolerates the spot taint, requests `nvidia.com/gpu: 8`, checkpoints to Blob every 10 minutes. Eviction → resumes on next allocated node. *Effective rate: ~$2/A100/hr vs $4 on-demand; same throughput; 50% saving.*
- **Multi-zone Postgres + PDB — survived AZ outage.** A 3-replica Postgres StatefulSet, each Pod pinned to a different zone, PDB `maxUnavailable: 1`. AZ-1 went dark at 02:14. Two Pods still running; PDB blocked CA from draining either. KEDA + HPA didn't fire (DB Pods not in scaling). At 02:31 AZ-1 recovered; 3rd Pod re-scheduled. *Application latency rose by 2× during 17 minutes; no data loss; no human intervention.*

## Common misconceptions

- **Myth:** "NAP and Cluster Autoscaler do the same thing."
  **Truth:** **CA** = per-pool min/max scaling. You define the pool's VM SKU; CA scales count. **NAP** = per-Pod node provisioning across the entire SKU catalog. NAP makes pool selection automatic; CA makes pool count automatic. NAP needs no fixed pools (it can create them); CA needs you to create them.
- **Myth:** "KEDA is just HPA with more sources."
  **Truth:** KEDA does that, plus enables **scale-to-zero**. HPA needs at least 1 Pod to read metrics; KEDA can drive replicas to 0 when external events show no load (queue empty, no cron firing). For event-driven workloads with idle hours, scale-to-zero is the cost story HPA alone cannot deliver.
- **Myth:** "Spot pools always save money."
  **Truth:** Spot saves *only when your workload tolerates eviction* — checkpoint-resume, idempotent retries, fault-tolerant queue consumption. If a workload restarts losing work or fails customer-facing requests during eviction, the SLA hit + retries cost more than on-demand. Use Spot for batch / ML / queue workers; not for stateful primaries.

## Recap

Two scaling axes mapped: node-side (CA vs NAP) and Pod-side (HPA / VPA / KEDA). Specialty pools (Spot, GPU, Windows, ARM, Confidential, FIPS) are first-class. PDBs and topology-spread protect availability.

**Next — A6: AKS Security.** Azure Policy for AKS (Gatekeeper-based), Microsoft Defender for Containers, Image Cleaner, ACR scanning + content trust, Workload Identity (recap), PSA, Azure Firewall, FIPS pools, host encryption, Confidential Containers (Kata + AMD SEV-SNP), Trusted Launch, Azure Linux 2 → 3 / Ubuntu 24 migration.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
