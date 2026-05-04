# K-ADV-AI I7 — I7 · GPU Sharing + Multi-Tenant Security + Cost Optimization

> Course: K-ADV-AI (advanced specialization)
> Module I7 · GPU Sharing + Tenant + Cost
> Companion preview: `/preview-kubernetes-adv-ai-lesson-07.html`.

---

**🎯 If you remember nothing else:** **Share via MIG / time-slice / DRA. Isolate via namespace + Quota + MIG. Economise via Spot + idle reclaim + Kueue queue + RIs/SP/CUDs + right-size. The expensive GPU deserves utilization + governance + cost discipline.**

## 1. MIG vs time-slicing vs DRA vs MPS

**MIG (Multi-Instance GPU)**: hardware-isolated partition (H100/A100). Each instance has dedicated SMs + memory + L2. Strong isolation; up to 7 partitions / GPU.
    **Time-slicing**: software-shared via NVIDIA driver; multiple Pods per GPU; round-robin GPU access. Lower isolation; oversubscription possible.
    **DRA**: structured-parameter scheduling; supports MIG + time-slicing + custom; multi-vendor.
    **MPS (Multi-Process Service)**: NVIDIA library allowing multiple processes share GPU concurrently (vs serialised). Different from time-slicing; useful for many-small-process inference.

## 2. Isolation primitives + tenant boundary

GPU multi-tenancy needs *both* K8s isolation + GPU isolation:
    
      - **Namespace + RBAC + NetPol + Quota** (per K-ADV-SEC patterns).

      - **MIG instances**: hardware-isolated; tenant boundary at MIG instance level; one tenant's instance can't affect another's.

      - **Time-slicing isolation gap**: shared GPU memory; one Pod's OOM can crash sibling Pods. Acceptable for trusted-tenant; risky for untrusted.

      - **Node taint per tenant**: dedicate certain GPU nodes to specific tenants for hard isolation.

      - **AI Gateway per-tenant token budget**: prevent runaway requests at L7.

## 3. Spot + idle reclaim + Kueue queue + RIs + ARM

**Spot GPU**: 60-90% discount; reclaimed on short notice. Tolerable for batch / training / fault-tolerant inference. Pair with checkpointing.
    **Idle reclaim**: detect idle GPUs (no process for N min); auto-evict; rejoin to general pool.
    **Kueue queue**: hold low-priority jobs until capacity; preempt for high-priority.
    **RIs / Savings Plans / CUDs**: 30-50% discount on baseline GPU capacity.
    **ARM-based GPUs**: NVIDIA Grace Hopper / GH200 — ARM CPU + Hopper GPU; cheaper for compatible workloads.
    **Right-sizing**: many workloads request whole GPU but use 20%; MIG into 1g.10gb cuts cost 4×.

## 4. Quotas + dashboards + chargeback

Per-tenant **GPU Quota** at K8s + Kueue level. **OpenCost / Kubecost** shows GPU cost / tenant; alerts at 75% / 95% of budget.
    **Chargeback**: GPU bill allocated to tenant; visible in their P&L. Drives self-tune (right-sizing, MIG adoption, Spot).
    **Idle GPU dashboard**: surface DCGM metrics; alarm on < 20% utilization for > 1 hour. Tenant + platform team review monthly.

## Before / After

**Before.** Pre-controls, GPU clusters operated like dev clusters — no quota, no sharing, no isolation, no cost transparency. Bills surprised; one tenant could DoS; underutilization rampant.

**After.** Modern: MIG / time-slicing / DRA for sharing; namespace + Quota + MIG isolation for security; Spot + idle reclaim + Kueue + RIs + chargeback for economics. GPU clusters operated like the expensive resource they are.

*Share + isolate + economise. The GPU is the most expensive resource; treat it that way.*

## Analogy — the K-Observatory array

The Sharing Committee at the observatory governs telescope use. Telescopes are split into eyepieces (MIG); some shared by appointment (time-slicing); booking goes through committee (DRA / Kueue). Different astronomer groups have isolated telescope sessions (namespace + Quota); the committee tracks per-group usage + sends monthly bills (chargeback). Idle telescopes get reclaimed (idle reclaim); cheap rental telescopes available for fault-tolerant work (Spot).

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Eyepiece partition | MIG instance |
| Shared appointment | Time-slicing |
| Multi-vendor booking | DRA |
| Concurrent processes per telescope | MPS |
| Astronomer group session | Namespace + per-tenant Quota |
| Hardware isolation across groups | MIG isolation between tenants |
| Cheap rental telescope | Spot GPU |
| Auto-reclaim idle telescopes | Idle GPU reclaim |
| Booking queue | Kueue priority + queue |
| Long-term lease discount | RIs / Savings Plans / CUDs |

⚠️ *Analogy stops here:* A telescope is fixed; GPU sharing is software-defined + driver-mediated. MIG is more rigid than time-slicing; DRA more flexible than both.

## ELI5 / ELI10

**ELI5.** Telescopes are expensive. Split them into eyepieces (MIG) so 7 astronomers share. Different groups have isolated time. Cheap rental scopes for chores. Bill each group; recover idle scopes.

**ELI10.** **Sharing**: MIG (hardware partition) / time-slicing (software) / DRA (structured) / MPS (multi-process). **Multi-tenant security**: namespace + Quota + MIG isolation + node taint per tenant + AI Gateway token budget. **Cost**: Spot + idle reclaim + Kueue queue + RIs/SP/CUDs + ARM (Grace Hopper) + right-size + chargeback.

## Real-world scenarios

- **MIG cut inference cost 4×.** Inference fleet on whole H100s; each Pod 20% util. MIG 1g.10gb per Pod; one H100 → 7 Pods; cost / Pod 4× lower; same throughput.
- **Spot GPU for training.** Fault-tolerant training adopted Spot G5 + Spot G6 fleet; checkpoint every 15 min; reclaim handled gracefully. Cost dropped 70%; training time +5% (recovery from interruptions).
- **Chargeback drove right-sizing.** Showback dashboards revealed top spenders. Teams right-sized: whole-GPU → MIG 3g.40gb; whole-GPU → MIG 1g.10gb for inference. Aggregate GPU bill dropped 35% over a quarter.
- **Outage — shared time-slicing crashed sibling Pods.** Time-slicing deployed; one Pod's GPU OOM crashed all sibling Pods. Postmortem: MIG for production; time-slice OK for dev / experimental only.

## Common misconceptions

- **Myth:** "Time-slicing is always cheaper than MIG."
  **Truth:** Both share GPU; time-slicing oversubscribes (more Pods possible) but isolation gaps cost recovery time. MIG fixed-cost; time-slicing variable-cost. Workload + isolation needs decide.
- **Myth:** "Spot GPU is too unreliable for ML."
  **Truth:** With checkpointing, Spot is fine for fault-tolerant training. Inference: tolerated for stateless + dynamic-route patterns; not for low-latency-critical.
- **Myth:** "GPU chargeback is too political."
  **Truth:** GPUs are the most expensive resource; chargeback aligns engineering + finance. Same logic as cloud chargeback in K-ADV-PE; just bigger numbers.

## Recap

GPU sharing (MIG / time-slicing / DRA / MPS) + multi-tenant security (namespace + Quota + MIG isolation) + cost optimization (Spot + idle reclaim + Kueue + RIs + ARM + right-sizing). The expensive GPU deserves discipline.

**Next — I8: Capstone — production AI inference platform.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
