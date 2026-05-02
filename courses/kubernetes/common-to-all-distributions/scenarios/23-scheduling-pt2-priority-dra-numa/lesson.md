# Lesson 23 — Scheduling Part 2 · Priority, DRA, NUMA, Profiles

> Course: Kubernetes — Common to all distributions
> Module 11 · Scheduling · Lesson 2 of 2
> Companion preview: `/preview-kubernetes-lesson-23.html`.

---

**🎯 If you remember nothing else:** **PriorityClass + preemption** decides who runs when the cluster is full. **Dynamic Resource Allocation (DRA)** — GA in K8s 1.34 — replaces ad-hoc device plugins with a structured CRD model for GPUs, FPGAs, NICs. **Topology Manager** + **CPU Manager** keep latency-sensitive workloads on the same NUMA node as their memory.

## 1. When the cluster is full, who wins?

The basic scheduler (Lesson 22) places Pods on nodes that fit them. But when nothing fits, by default the Pod just stays Pending. That's fine for batch work; it's terrible for production traffic-serving workloads. **Pod priority + preemption** tells the scheduler: "if this Pod can't fit, evict lower-priority Pods to make room."
    You define a `PriorityClass` object cluster-wide (`system-cluster-critical` = 2000000000, `system-node-critical` = 2000001000 are reserved; user-defined classes typically range from 0 to 1 billion). Pods reference a `priorityClassName`. When a high-priority Pod can't be scheduled, the scheduler picks the lowest-priority Pod(s) it can evict to free up the resources, evicts them (gracefully, with a configurable termination grace period), and places the high-priority Pod.
    The classic three-tier setup: `critical` (=1000) for traffic-serving workloads, `standard` (=500) for the rest of production, `batch` (=10) for non-urgent work. Add an `opportunistic` (=-100) for spot-instance throwaway work that gets nuked first. Most clusters need exactly this hierarchy.

## 2. GPUs (and friends) get a structured API — GA in 1.34

For years, "give my Pod a GPU" was implemented via the device-plugin API: a privileged DaemonSet on the node, an ad-hoc `resources.limits: nvidia.com/gpu: 1` field, no support for sharing, no support for "I want a GPU with at least 80GB," no support for FPGAs / RDMA NICs / SR-IOV VFs as first-class objects. It was a hack that lasted a decade.
    **Dynamic Resource Allocation (DRA)** — GA in Kubernetes 1.34 — replaces device plugins with a proper API:
    
      - **DeviceClass** — cluster-scoped: "this is a class of devices, here's what attributes they have, here's the driver."

      - **ResourceClaim** — namespace-scoped: a Pod's request for a device — "I need an H100 with at least 80 GiB and CUDA 12.4."

      - **ResourceClaimTemplate** — like a PVC template: a Pod can ask for a one-shot claim that gets created and torn down with the Pod.

      - **ResourceSlice** — the kubelet publishes one per node, listing the actual devices available with their attributes.

    
    DRA solves what device plugins couldn't: structured attributes (CEL expressions in claims), partitioned devices (MIG slices), inter-Pod sharing of a device (one ResourceClaim → multiple Pods), and the basic dignity of being a real K8s object.
    [ deep dive — skip if new ]If you're starting a fresh cluster on K8s 1.34+, use DRA from day 1. If you're on an older cluster, the device plugin API still works — and the major vendors (NVIDIA, Intel, AMD) ship both DRA drivers and legacy device plugins for the transition. The migration is being driven by NVIDIA's MIG (Multi-Instance GPU) story; sharing a single H100 across multiple Pods isn't really expressible without DRA.

## 3. When microseconds matter

Modern servers have multiple **NUMA nodes** — physically separate CPU sockets each with attached RAM. Accessing memory on the local NUMA node is fast (~80ns); going across the inter-socket link to memory on another NUMA node is 2-3× slower. For latency-sensitive workloads (HFT, real-time inference, NFV), this matters.
    K8s exposes three coordinated managers:
    
      - **CPU Manager** (kubelet feature) — with `policy: static`, dedicates whole CPU cores to Guaranteed-QoS Pods that ask for integer CPU. Other Pods stay off those cores. Removes context-switching jitter.

      - **Memory Manager** — pins memory allocation to specific NUMA nodes.

      - **Topology Manager** — coordinates the above plus device assignments (GPUs, NICs) so they all land on the same NUMA node. `policy: single-numa-node` = enforce same-NUMA; `restricted` = allow cross-NUMA but flag; `best-effort` = try, don't enforce.

    
    Combined effect: a latency-sensitive Pod gets dedicated CPU cores, RAM allocated on the same NUMA node, and (if it asked for one) a GPU/NIC also on that NUMA node. Nothing crosses the inter-socket link. Tail latency drops by 20-50% in extreme cases.

## 4. When one scheduler isn't enough

A **scheduler profile** is a named configuration of the kube-scheduler's plugins, scores, and weights. The default profile (`default-scheduler`) handles every Pod that doesn't specify `spec.schedulerName`. You can run multiple profiles in the same kube-scheduler process for different workload types — or run a separate scheduler binary entirely.
    Common patterns:
    
      - **Bin-packing for batch:** a profile with `NodeResourcesFit: scoring=MostAllocated` packs Pods tightly to maximise spot-eviction efficiency. Default profile uses `LeastAllocated` for spread.

      - **Latency-optimised profile:** heavy weight on `InterPodAffinity` + `NodeAffinity` + `TopologyManager` hint, lighter on resource utilisation.

      - **Volcano / Yunikorn:** entirely separate batch schedulers for ML training (gang scheduling, queues, fair-share).

    
    The custom-plugin SDK lets you write Go plugins for filter/score/permit/reserve/postBind phases. Most users don't need this — they need to combine existing plugins differently. But for the cases that do need it, the SDK is mature.

## Before / After

**Before.** Pre-priority: cluster full → critical Pod sits Pending. Engineer wakes up, manually kills batch jobs, prays they didn't lose state. GPU requests by string match (`nvidia.com/gpu`) — no way to ask for "H100 with 80 GiB" or "MIG slice." Latency-sensitive Pods scheduled wherever; tail latency wobbles for unexplained reasons.

**After.** PriorityClass + preemption → cluster full + critical incoming → batch evicted automatically, critical placed in seconds. DRA → declarative ResourceClaim with attributes; scheduler matches structurally. Topology Manager → CPU + memory + GPU all on same NUMA node; tail latency stable.

DRA is the most consequential scheduler change since the original K8s API. By 2027, device plugins will look quaint.

## Analogy — the K-Town district

Back to Dispatch Office, but now we're past the routing board into the VIP wing. Three new desks. The **priority desk** hands out lane stickers — VIP, premium, regular, walk-in. When the road is jammed and a VIP truck can't move, the dispatcher pulls a regular truck to the side (gracefully — the regular driver's called, given time to finish loading) and lets the VIP through. The **specialty equipment desk** (DRA) is where trucks request specific tools — "I need a refrigerated trailer with 80 cubic feet" — and the desk matches against the actual truck inventory by attribute, not by name. The **route engineering desk** (Topology Manager) handles trucks that need to stay on one specific highway loop because their cargo is sensitive to inter-zone transit.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| VIP / premium / regular lane stickers | `PriorityClass` objects |
| Pulling the regular truck aside for the VIP | Preemption + graceful eviction |
| "I need a refrigerated trailer with 80 cubic feet" | `ResourceClaim` with attribute selectors |
| The truck inventory at each depot | `ResourceSlice` published by kubelet |
| "This is a refrigerated trailer" classification | `DeviceClass` |
| Trucks that must stay on one highway loop | Topology Manager `single-numa-node` policy |
| Different routing manuals for different cargo types | Scheduler profiles |

⚠️ *Analogy stops here:* The analogy stops here: real DRA is a structured API with CEL expressions, not a paper request. And NUMA is a hardware reality of how RAM is wired to CPU sockets — there's no "highway loop" actually moving anything; it's electrons over a memory bus.

## ELI5 / ELI10

**ELI5.** Some toys are special — they go first. If the toy box is full, regular toys move out so the special toy can fit. Some toys need a specific kind of plug (a GPU plug). Some toys break if their batteries are too far away — they need batteries right next to them.

**ELI10.** Three advanced scheduling primitives. **PriorityClass** + preemption: critical Pods evict lower-priority Pods when the cluster is full. **DRA** (Dynamic Resource Allocation, GA in 1.34): structured request/match for GPUs/FPGAs/NICs with attributes ("H100 with 80 GiB"); replaces the legacy device-plugin API. **Topology Manager** + CPU Manager + Memory Manager: keep latency-sensitive workloads' CPU, RAM, and devices co-located on the same NUMA node. Plus scheduler profiles for using different bin-packing strategies for different workload types.

## Real-world scenarios

- **A SaaS during traffic spikes.** `critical` = 1000 (payment), `standard` = 500 (everything user-facing), `batch` = 10 (analytics, ML), `opportunistic` = -100 (spot-eligible). When traffic spikes preempt batch and opportunistic. The autoscaler then catches up. SREs sleep through what would have been a paging incident.
- **A bank running ML training on shared H100s.** DRA + NVIDIA's DRA driver. Each Pod's `ResourceClaim` requests one MIG slice of an H100 — say 1g.10gb (1/7 of an H100). Scheduler matches by attribute. Eight Pods can share one H100. Pre-DRA: each Pod requested a whole H100 — 8× the cost.
- **A trading firm running latency-sensitive Pods.** Topology Manager `policy: single-numa-node`. CPU Manager `policy: static`. Pods request integer CPU, Guaranteed QoS. Memory Manager pins RAM. Tail latency P99 dropped from 2.1ms to 0.7ms with no application change.
- **An ML lab running Volcano alongside default scheduler.** Default scheduler handles user-facing workloads. Volcano (in `kube-system`) handles ML training jobs with gang scheduling — all 16 workers must start at once or none start (no half-started training). Different `schedulerName` per job. Both schedulers coexist because they don't fight over the same Pods.

## Common misconceptions

- **Myth:** Preemption kicks in instantly.
  **Truth:** Evicted Pods get their normal grace period (default 30s, configurable per-Pod). The high-priority Pod waits for the eviction. Total time-to-place ≈ grace period + scheduler latency. Plan for ~1 minute, not instant.
- **Myth:** DRA replaces resource requests/limits.
  **Truth:** No. CPU and memory are still `resources.requests/limits` as before. DRA is for *devices* — GPUs, FPGAs, RDMA NICs, SR-IOV VFs. The two systems coexist.
- **Myth:** Topology Manager `single-numa-node` always speeds things up.
  **Truth:** Only for workloads that pin CPU, memory, and devices. For workloads that don't request integer CPU or specific devices, the policy has no effect. Worse: in resource-constrained clusters it can cause Pending Pods that would have placed cross-NUMA happily.

## Recap

PriorityClass + preemption decides who runs when full. DRA is the modern device API (GPUs, FPGAs, NICs) — GA in 1.34. Topology Manager keeps CPU, memory, and devices on the same NUMA node for latency-sensitive workloads. Scheduler profiles let you mix bin-packing strategies.

**Next — Lesson 24: Networking Foundations & CNI.** The Module 12 networking deep dive begins. Linux network primitives, the CNI specification, MTU debugging, and the major plugin landscape (Cilium, Calico, Flannel). Switchboard, behind the wires.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
