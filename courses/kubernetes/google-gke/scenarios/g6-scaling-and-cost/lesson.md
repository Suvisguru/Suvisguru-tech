# K-GKE G6 — G6 · GKE Scaling and Cost

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G6 · Scaling and Cost
> Companion preview: `/preview-kubernetes-gke-lesson-06.html`.

---

**🎯 If you remember nothing else:** **Cluster Autoscaler for fixed shapes; NAP picks SKUs across the catalog; Autopilot bills per Pod-second so idle = $0. Compute Classes drive SKU policy; Spot for fault-tolerant; GPU/TPU for AI. Always enable BQ billing export for chargeback.**

## 1. Cluster Autoscaler + Node Auto-Provisioning

**Cluster Autoscaler (CA)** = per-node-pool min/max scaling on GKE Standard. Set `--enable-autoscaling --min-nodes M --max-nodes N` per pool. CA watches for unschedulable Pods and scales out (up to max); watches underutilised nodes and scales in (down to min, respecting PDBs).
    
      - **PDB-aware drains** — when scaling in, CA respects PodDisruptionBudgets. Tight PDBs deadlock scale-down.

      - **Multi-zone CA** — for multi-zonal pools, CA balances nodes across zones.

    
    **Node Auto-Provisioning (NAP)** = GKE's implementation of automatic node-pool creation. Enable with `--enable-autoprovisioning` + bounds (CPU / memory / GPU / TPU). When unschedulable Pods need a SKU you don't have, NAP creates a new node pool with the right shape on demand. *Removes the per-pool sizing problem* — no need to pre-create dozens of pools for every possible workload shape.
    **Autopilot** (covered in G1) is the no-CA-needed shape: Google manages all node operations; you declare Pods; per-Pod billing. The Pod-level SLA + admission constraints are part of the package.

## 2. Compute Classes + HPA + VPA

**Compute Classes** = a GKE primitive that lets you express *node-shape intent* via a `ComputeClass` CRD: priority list of acceptable VM families, optional Spot fallback, optional CMEK key, etc. NAP uses the Compute Class to pick SKUs; Autopilot uses it to pick the underlying compute. Built-in Compute Classes:
    
      - **Balanced** — general-purpose (E2 / N2). Default.

      - **Performance** — N2D / C3 / C4 high-frequency CPUs.

      - **Scale-Out** — Tau T2D / T2A — high-density, lower per-vCPU cost; ARM (T2A).

      - **Accelerator** — GPU / TPU shapes for AI workloads.

    
    **HPA (Horizontal Pod Autoscaler)** + **GCP custom metrics adapter** = scale Pods on Cloud Monitoring custom metrics, not just CPU/memory. Examples: queue depth in Pub/Sub, request rate from Cloud Load Balancing, BigQuery query backlog. *Set maxReplicas* — HPA without a cap is the runaway-cost story.
    **VPA (Vertical Pod Autoscaler)** right-sizes requests over time. **In Autopilot**, VPA-style mutation is built in — Autopilot observes actual usage and (for some workloads) adjusts Pod requests automatically. *Fewer over-provisioned Pods; lower bills.*

## 3. Spot + GPU (A3/A4) + TPU (Trillium / Ironwood)

**Spot VMs** on GKE — up to 91% off list price. Eviction with 30-second notice. Auto-tainted; workloads must tolerate. Ideal: batch jobs, ML training (with checkpointing), CI runners, fault-tolerant queue consumers. *Combine with Spot fallback in Compute Class* so your workload tries Spot first, falls back to on-demand if Spot is unavailable.
    **GPU node pools**:
    
      - **A3** — NVIDIA H100 (Hopper) GPUs. Up to 8 GPUs per VM. For LLM training + high-end inference.

      - **A4** — NVIDIA H200 / B200 (newer Hopper / Blackwell). Higher memory bandwidth + capacity.

      - L4 / L40S / T4 for inference + smaller training.

    
    NVIDIA GPU Operator or GKE's built-in NVIDIA GPU device plugin makes `nvidia.com/gpu` resource available. MIG (Multi-Instance GPU) lets you slice a single H100 into multiple smaller GPUs for inference workloads.
    **TPU** — Google's custom AI accelerator chips:
    
      - **Trillium** — current-gen training/inference TPU. Multi-host pods (TPU v5e+) for distributed training.

      - **Ironwood** — newest gen, optimised for inference at scale.

    
    Multi-host TPU pods require special node-pool topology + workload integration (the JobSet API + Kueue help — covered in G8).

## 4. Cost — BigQuery export + Autopilot per-Pod billing

**GKE cost allocation with BigQuery export** — enable **BigQuery billing export** at the project level + the GKE-specific **cost allocation** feature. Result: per-row cost data joined with K8s metadata (cluster, namespace, workload). Build chargeback dashboards in Looker Studio / Looker / Grafana. *Without this, you can see cluster total but not which team / tenant owns the slice.*
    **Autopilot per-Pod billing**:
    
      - Bills per *Pod-second based on requested CPU / memory / ephemeral storage*.

      - Pod with `requests: 100m / 256Mi` running 1 hour ≈ 0.1 vCPU-hour + 0.25 GiB-hour. Off-hours scale-to-zero of a Deployment = $0.

      - GPU / TPU billed per accelerator-second when using Compute Class Accelerator.

      - Compare to Standard which always bills per node — over-provisioned pools idle most of the day.

    
    **Cost levers:** right-size requests (VPA recommendations or Autopilot auto-mutation); use Spot for fault-tolerant workloads; use Compute Class Scale-Out (T2D / ARM) for compute-bound stateless workloads at ~30% saving; cap HPA maxReplicas; review BQ cost export monthly to catch outliers.
    **Sustained-use + committed-use discounts** (CUDs) — apply to GKE node-VM cost. Negotiate CUDs for the predictable baseline; let burst go through Spot + on-demand.

## Before / After

**Before.** Pre-Autopilot, every GKE cluster billed per node — over-provisioned pools idle most of the day. Pre-NAP, operators created dozens of node pools per cluster (one per workload shape). Pre-Compute Classes, picking the right SKU per workload was a Helm-values exercise. GPU + TPU were Standard-only. BigQuery cost export was bring-your-own; per-namespace cost was opaque.

**After.** Modern GKE: **Autopilot per-Pod billing** aligns spend to actual Pod-seconds. **NAP** creates node pools on demand from the SKU catalog. **Compute Classes** express SKU intent declaratively. **Spot fallback** in Compute Class. **BigQuery billing export** + GKE cost allocation surfaces per-namespace + per-tenant cost. Plus first-class GPU (A3/A4) + TPU (Trillium/Ironwood) for AI. *Spend visibility + flexibility together.*

*The era of cluster bill surprises is over for teams that wire BQ export + use Autopilot or NAP + Compute Classes thoughtfully.*

## Analogy — the K-Garden plot

The **Auto-Greenhouse** is K-Garden's climate-controlled space where capacity flexes with demand. Three staff handle different jobs.
    The **Plot Manager** (Cluster Autoscaler) walks rows in their assigned greenhouse: "this row is full → wheel in 5 more pots from the supply room; this row is empty → roll the empty pots back." The Plot Manager only handles one greenhouse type (one node pool); for new shapes, the Garden Architect (Node Auto-Provisioning) builds a new greenhouse on demand from the catalog.
    The **Robot Caretaker** (Autopilot) runs a different model entirely: visitors arrive with seedlings; the robot plants, waters, prunes; visitors are billed per seedling-day (per-Pod-second), not per greenhouse. Idle = $0.
    The **Greenhouse Catalog** (Compute Classes) describes which greenhouse models the Architect picks — *Balanced* general-purpose, *Performance* high-frequency, *Scale-Out* ARM/Tau low-cost, *Accelerator* for GPU/TPU AI plots.
    Plus *specialty plots*: Spot greenhouses (deep-discount, ushers can ask occupants to leave with 30s notice — for resilient batch crops); GPU plots (A3/A4 with H100/H200/B200 NVIDIA accelerators for AI training); TPU plots (Trillium / Ironwood Google-designed AI accelerators for distributed training).
    And the **Garden Accountant** (BigQuery cost export + GKE cost allocation) breaks the bill down per plot, per tenant, per crop — so the head gardener knows who owes what.

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| Plot Manager (per greenhouse) | Cluster Autoscaler — per-pool min/max |
| Garden Architect (catalog-driven) | Node Auto-Provisioning (NAP) |
| Robot Caretaker | GKE Autopilot — managed nodes + per-Pod billing |
| Greenhouse Catalog | Compute Classes (Balanced / Performance / Scale-Out / Accelerator) |
| Per-seedling-day billing | Autopilot per-Pod-second billing |
| Spot greenhouses (30s notice) | Spot VMs (up to 91% off) |
| Spot fallback in catalog | Compute Class with Spot fallback |
| GPU plots | A3 (H100), A4 (H200/B200) GPU node pools |
| TPU plots | Trillium / Ironwood TPU node pools |
| Slice a greenhouse into smaller plots | MIG — Multi-Instance GPU |
| HPA via custom metric (queue depth) | HPA with GCP custom metrics adapter (Cloud Monitoring source) |
| Right-size each pot to what's in it | VPA / Autopilot auto-mutation of requests |
| Garden Accountant | BigQuery billing export + GKE cost allocation |
| "Per-tenant chargeback" | Per-namespace cost via BQ joined with K8s metadata |
| Pre-paid plot lease | Committed-use discount (CUD) on baseline |

⚠️ *Analogy stops here:* A real greenhouse has fixed walls; Compute Classes + NAP are software-defined and reshape constantly. Real Autopilot has admission constraints (mutates / rejects some Pod specs) the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** The greenhouse has clever staff. One adds and removes pots in their greenhouse. One builds new greenhouses from a catalog when needed. A robot caretaker runs the whole job for some plots and bills per seedling. Special greenhouses for cheap (Spot), GPU, and TPU. An accountant breaks the bill down per plot.

**ELI10.** GKE scaling = node-side (CA per pool, NAP across catalog, Autopilot fully managed) + Pod-side (HPA with custom metrics, VPA / Autopilot auto-mutation). Compute Classes (Balanced / Performance / Scale-Out / Accelerator) drive SKU intent. Specialty hardware: Spot (91% off), GPU (A3 H100, A4 H200/B200), TPU (Trillium / Ironwood). Cost: BigQuery billing export + GKE cost allocation = per-namespace + per-tenant chargeback. Autopilot per-Pod billing = idle = $0.

## Real-world scenarios

- **SaaS — Autopilot + scale-to-zero off-hours.** A SaaS's API workloads on Autopilot. KEDA on Pub/Sub queue depth scales to 0 replicas off-hours. Per-Pod billing = $0 cost during 8 hours of low traffic. Compared to Standard with 5-node baseline pool: ~30% lower monthly bill on the same traffic shape.
- **ML team — Spot A3 H100 for training, on-demand A4 H200 for inference.** ML team uses Compute Class Accelerator: Spot fallback enabled. Training jobs prefer Spot A3 H100 (massive discount + checkpointing tolerates eviction); when Spot unavailable, fall back to on-demand. Inference workloads on dedicated A4 H200 pool, no Spot (latency-sensitive). *Training cost ~70% lower vs all-on-demand; inference SLA preserved.*
- **Multi-tenant cluster — per-namespace chargeback rolled out via BQ export.** Platform team enables BigQuery billing export + GKE cost allocation. Looker Studio dashboard joins billing rows with namespace → tenant mapping. Tenants now see their actual cost; Finance has chargeback. *Outcome: one tenant noticed their over-provisioned Deployment, removed it, saved $4K/month.*
- **Compute Class Scale-Out (T2D ARM) saved 30% on stateless backend.** A stateless backend ran on default Balanced (E2). Migration to Compute Class Scale-Out (Tau T2D ARM) for the workload's ARM-built containers. ~30% lower per-vCPU cost; throughput equivalent. *One Compute Class change; significant saving on the cluster's biggest line item.*

## Common misconceptions

- **Myth:** "Autopilot is always cheaper than Standard."
  **Truth:** Autopilot bills per requested CPU/memory at a markup over raw VM rates. For workloads at **high sustained utilisation on big nodes with big requests**, Standard with packed nodes can be cheaper. Autopilot wins on bursty / event-driven workloads with idle hours and on small clusters where Standard's minimum-viable node pool is over-provisioned. Run the math per workload pattern; both paths are valid.
- **Myth:** "Spot saves money. Period."
  **Truth:** Spot saves only when the workload *tolerates* eviction — checkpoint-resume training, idempotent retries, queue-driven consumers. If the workload restarts losing work or fails customer-facing requests during eviction, the SLA hit + retry cost outweighs the Spot saving. Use Compute Class with Spot fallback to get the saving when Spot is available without breaking when it isn't.
- **Myth:** "GPU is GPU. Pick whichever is available."
  **Truth:** A3 (H100), A4 (H200/B200), L4, L40S, T4 are all NVIDIA GPUs but very different price/perf classes. H100/H200 for LLM training + high-end inference. L4/L40S for cost-effective inference. T4 for legacy or budget inference. *Pick by workload*: LLM training on T4 = wasteful; small-model inference on H100 = wasteful. Compute Class Accelerator + workload selectors target the right pool.

## Recap

Two scaling axes (node-side: CA / NAP / Autopilot; Pod-side: HPA / VPA) + Compute Classes for SKU intent + specialty hardware (Spot / GPU / TPU). Cost surfaced via BQ export.

**Next — G7: GKE Observability.** Cloud Logging + Cloud Monitoring (auto for GKE), Managed Service for Prometheus (GMP), managed Grafana, Cloud Trace, Cloud Profiler, Error Reporting, control-plane metrics/logs, SLO monitoring, alerting policies, BigQuery cost view.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
