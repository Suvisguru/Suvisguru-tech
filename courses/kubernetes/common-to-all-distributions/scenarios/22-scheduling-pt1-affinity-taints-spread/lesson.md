# Lesson 22 — Scheduling Part 1 · Affinity, Taints, Topology Spread

> Course: Kubernetes — Common to all distributions
> Module 11 · Scheduling · Lesson 1 of 2
> Companion preview: `/preview-kubernetes-lesson-22.html`.

---

**🎯 If you remember nothing else:** The scheduler does **filter → score → bind**. You shape filtering with **nodeSelector**, **affinity / anti-affinity**, **taints + tolerations**, and **topology spread constraints**. The single most consequential rule for production: **spread across zones**.

## 1. What the scheduler actually does

When you create a Pod with no `nodeName`, it sits in `Pending`. The kube-scheduler is a controller watching unscheduled Pods. For each one, it runs a two-phase decision:
    
      - **Filter (predicates):** remove every node that *can't* host this Pod. Reasons: not enough CPU/memory, doesn't match nodeSelector, has a NoSchedule taint the Pod doesn't tolerate, doesn't satisfy affinity/anti-affinity, fails a custom plugin's check. After filtering you have a candidate set.

      - **Score (priorities):** rank candidates by various plugins — most-allocated, least-allocated, image-locality, topology-spread, inter-pod affinity scoring, custom plugins. Highest score wins.

    
    Once a node is picked, the scheduler writes `spec.nodeName` on the Pod via the API. The kubelet on that node sees the assignment, pulls the image, starts the containers. The scheduler doesn't move Pods after they're placed — that's the kubelet's eviction logic plus controllers like the descheduler.

## 2. From simple labels to expressive matching

**nodeSelector** is the original tool: a flat `map[string]string`. The Pod says `nodeSelector: {disktype: ssd}`; the scheduler keeps only nodes with that label. Hard match, no flexibility, deprecated for new use cases — but still ubiquitous because it's tiny.
    **Node affinity** is the modern, expressive successor. Two flavours:
    
      - `requiredDuringSchedulingIgnoredDuringExecution` — must match (filter). Like nodeSelector but with `In`, `NotIn`, `Exists`, `Gt`, `Lt` operators.

      - `preferredDuringSchedulingIgnoredDuringExecution` — soft preference (score). Fall back to other nodes if the preferred ones aren't available.

    
    **Inter-pod affinity / anti-affinity** ties Pod placement to *where other Pods are*. Anti-affinity is the workhorse for spreading: "don't put two replicas of this Deployment on the same node" expressed as `topologyKey: kubernetes.io/hostname` + `labelSelector: matchLabels: {app: web}`.

## 3. Nodes refuse; Pods opt in

Affinity is the Pod expressing a preference. **Taints** are the inverse — the *node* says "don't schedule things here unless they explicitly accept this taint." Three effects:
    
      - `NoSchedule` — scheduler refuses to place new Pods that don't tolerate this taint.

      - `PreferNoSchedule` — try to avoid, but okay if no alternative.

      - `NoExecute` — even running Pods get evicted if they don't tolerate the taint.

    
    A Pod tolerates a taint by listing it under `spec.tolerations`. Common patterns:
    
      - **Dedicated node pools**: taint GPU nodes `gpu=true:NoSchedule`; only GPU workloads tolerate it. Non-GPU Pods stay off (and don't waste expensive capacity).

      - **Maintenance**: `kubectl drain node-x` taints with `NoExecute`; running Pods evict, no new ones land.

      - **Node problems**: the node-problem-detector taints failing nodes; non-tolerant workloads reschedule away.

    
    [ deep dive — skip if new ]The taints+tolerations pair is the single mechanism behind *cordoning* (taint → no new Pods), *draining* (taint with NoExecute → evict + no new Pods), *node-not-ready handling* (auto-applied `node.kubernetes.io/not-ready:NoExecute` with a 5-min toleration window), and *spot/preemptible nodes* (taint to keep critical workloads off). Master taints and you understand most of the cluster's lifecycle behavior.

## 4. The single most useful scheduling primitive

You almost always want replicas of a workload *spread across zones, racks, or hosts* — both for HA and for fair use of capacity. Anti-affinity used to be the way; topology spread is now strictly better.
    A constraint says: "for Pods matching this selector, the difference between the most-loaded topology bucket and the least-loaded should be at most `maxSkew`."
    
      - `topologyKey: topology.kubernetes.io/zone` + `maxSkew: 1` — spread evenly across zones.

      - `topologyKey: kubernetes.io/hostname` + `maxSkew: 1` — at most one extra Pod on any one node.

      - `whenUnsatisfiable: DoNotSchedule` — hard. `ScheduleAnyway` — soft (score-only).

    
    Pair zone-spread with hostname-spread for full protection: across zones first (HA), within zones across hosts (don't pile on one machine). Most production Deployments should have both.
    K8s 1.33+ added `matchLabelKeys` for cleaner rolling-update behavior (skew is computed per-revision so old + new replicas don't double-count). New code should use it.

## Before / After

**Before.** Pre-spread era: 12 web Pods, all 12 happen to land in `us-east-1a` because the scheduler optimised for image locality. Zone fails. Service is gone. Engineers are awake. Post-mortem starts with "we should have spread."

**After.** Topology spread + anti-affinity: 12 Pods land 4-4-4 across `us-east-1a/b/c`, no two on the same node within a zone. Zone fails. Eight Pods still serving; HPA scales up. Service degrades briefly, never goes down. The post-mortem is short.

Topology spread is the cheapest reliability win in K8s. Two YAML fields, no extra controllers, ~zero performance cost. Set it on every production Deployment.

## Analogy — the K-Town district

The Dispatch Office routes trucks (Pods) to depots (nodes) across three districts (zones). The dispatcher (kube-scheduler) has a board with every depot's status. Trucks come in with stickers — "I need a refrigerated depot" (*nodeSelector: refrigerated=true*), "I prefer the harbour district but the airport district works too" (*preferred affinity*), "I cannot share a depot with another delivery from my own company" (*pod anti-affinity*).Each depot has its own warning signs: "no flammables" (*NoSchedule taint*), "evacuating — leave by 5 PM" (*NoExecute taint*). Trucks carrying flammables won't go there unless their driver has the special permit (*toleration*).And there's the city-wide spread rule: *no district may have more than one extra truck of any one company*. The dispatcher checks the board before binding any truck. Filter, score, bind. The whole system is designed to make the wrong choice hard.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The dispatcher | kube-scheduler |
| "I need a refrigerated depot" sticker | `nodeSelector` / required node affinity |
| "I prefer the harbour, but airport works" sticker | Preferred node affinity |
| "Don't park me next to another truck from my company" | Pod anti-affinity |
| "No flammables" sign at the depot | `NoSchedule` taint |
| "Evacuating now" sign | `NoExecute` taint |
| Driver's special permit | Toleration on the Pod |
| City-wide "no district more than one truck above the rest" | `topologySpreadConstraints` with `maxSkew: 1` |

⚠️ *Analogy stops here:* The analogy stops here: the dispatcher in K-Town only places new trucks. Once parked, trucks don't move on their own — that's a separate process called the descheduler (or pod-driven evictions during draining), and it's outside this lesson.

## ELI5 / ELI10

**ELI5.** Imagine 12 toy cars and 3 toy garages. The toy cars don't want to all crowd into one garage — they each pick a different garage. That's "topology spread." Some garages have a "no toy trucks" sign — those are taints. Toy trucks need a sticker to enter (toleration).

**ELI10.** The kube-scheduler picks a node for every Pod. It does **filter → score → bind**. You shape the filter with: `nodeSelector` (flat label match), node affinity (operator-rich match, required or preferred), inter-pod affinity / anti-affinity (relative to other Pods), taints + tolerations (nodes repel; Pods opt in), and topology spread constraints (don't bunch up). For production, always: zone-spread + hostname-spread + reasonable resource requests. Skip these and the scheduler will technically work — and your zone-failure post-mortem will be long.

## Real-world scenarios

- **A SaaS standard production Deployment.** Every Deployment ships with two topology-spread constraints (zone, hostname), maxSkew 1, both DoNotSchedule. Plus pod anti-affinity (preferred) for backwards compat. Engineers don't touch these — they're enforced via a Kyverno mutation that adds them automatically if a Deployment forgets.
- **A bank running ML training on dedicated GPUs.** GPU nodes tainted `gpu=nvidia-h100:NoSchedule`. Training Pods tolerate it. Inference Pods tolerate it AND have node affinity for the same label. CPU-only workloads have no toleration so they never waste expensive capacity. Spot GPUs additionally have `spot:NoSchedule` — only batch training tolerates that one.
- **A startup using PreferNoSchedule for cost-skewing.** Cluster mostly on-demand nodes plus a few spot nodes. Spot tainted with `cost-tier=spot:PreferNoSchedule` + a tag `cost-tier=spot`. Stateful production Pods have no toleration → land on on-demand. Batch jobs explicitly tolerate spot AND have node affinity for it → land on spot first; fall back to on-demand if no spot capacity.
- **A team using descheduler for drift correction.** The descheduler runs as a CronJob. Detects Pods that violate topology-spread (e.g., from old, pre-constraint Deployments) and evicts them. The scheduler then re-places correctly. Slow, gentle, in-place rebalancing without redeploys.

## Common misconceptions

- **Myth:** Anti-affinity and topology spread do the same thing.
  **Truth:** Anti-affinity says "don't put two of these on the same X." Topology spread says "distribute across X with at most maxSkew imbalance." Spread scales with replica count; anti-affinity doesn't. Spread is generally what you actually want.
- **Myth:** `preferred` affinity is mostly the same as `required`.
  **Truth:** Preferred is a *scoring* input — the scheduler will pick a non-preferred node if the preferred one's at capacity. Required is a *filter* — the Pod stays Pending forever if no matching node exists. Use required only for hard constraints (GPU type, kernel version).
- **Myth:** `maxSkew: 0` is the strictest possible setting.
  **Truth:** `maxSkew` is required to be at least 1 (skew of 0 makes no mathematical sense — it would mean every bucket has exactly the same count, which is impossible at most replica counts).

## Recap

Scheduler does filter → score → bind. nodeSelector / affinity say where Pods can go; taints + tolerations say where nodes accept; topology spread keeps the load balanced across failure domains. For production, always set zone + hostname spread.

**Next — Lesson 23: Scheduling Part 2.** The advanced controls — Pod priority and preemption, Dynamic Resource Allocation (DRA, GA in 1.34) for GPUs, NUMA topology, scheduler profiles. The dispatch office's executive routing.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
