# K-EKS E6 — E6 · EKS Compute and Autoscaling (Karpenter, Spot, Graviton, GPU)

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E6 · Compute and Autoscaling
> Companion preview: `/preview-kubernetes-eks-lesson-06.html`.

---

**🎯 If you remember nothing else:** **Karpenter** = recommended autoscaler for EKS. NodePool + EC2NodeClass per workload class. Consolidation: WhenUnderutilized (aggressive) or WhenEmpty (conservative). **Spot** (60-90% off) for tolerant workloads + spot interruption handling. **Graviton ARM** (~25% cheaper, often faster per dollar). **GPUs** (P/G families) + **Inferentia/Trainium** + **Neuron device plugin** + **EFA** for distributed training. **Savings Plans / RIs** on the always-on baseline.

## 1. Karpenter beats Cluster Autoscaler on EKS

**Cluster Autoscaler (CA)**: legacy. Scales Auto Scaling Groups based on Pending Pods. Each ASG is a fixed instance type. Spinning up new capacity = 60-120s. No instance-type optimisation per Pod. Doesn't consolidate.
    **Karpenter**: modern. Picks the best EC2 instance type per Pending Pod. 20-40s spin-up. Consolidation built-in. Spot-aware. Mixed instance families per NodePool. AWS-built (open-source); EKS Auto Mode bundles + manages it.
    For new EKS clusters: **EKS Auto Mode** (which is Karpenter under the hood; AWS owns lifecycle — see E2). For existing clusters or shops wanting to manage Karpenter directly: **self-managed Karpenter**.

## 2. The CRDs you write

`# NodePool — workload-facing
apiVersion: karpenter.sh/v1
kind: NodePool
metadata: {name: general-spot}
spec:
  template:
    spec:
      nodeClassRef: {group: karpenter.k8s.aws, kind: EC2NodeClass, name: default}
      requirements:
      - {key: kubernetes.io/arch, operator: In, values: [amd64, arm64]}
      - {key: karpenter.sh/capacity-type, operator: In, values: [spot, on-demand]}
      - {key: karpenter.k8s.aws/instance-family, operator: In, values: [c6i, m6i, c7g, m7g]}
      - {key: karpenter.k8s.aws/instance-size, operator: NotIn, values: [nano, micro]}
      taints: []
  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 30s
    expireAfter: 720h
  limits: {cpu: 1000, memory: 1000Gi}
---
# EC2NodeClass — AWS-specific (only for self-managed Karpenter)
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata: {name: default}
spec:
  amiFamily: Bottlerocket
  role: KarpenterNodeRole
  subnetSelectorTerms: [{tags: {karpenter.sh/discovery: prod}}]
  securityGroupSelectorTerms: [{tags: {karpenter.sh/discovery: prod}}]`

## 3. Spot, Graviton, Savings Plans

- **Spot**: unused EC2 capacity at 60-90% discount. AWS may interrupt with 2-min notice. Karpenter handles interruption (drains node gracefully) automatically. **Workload fit**: stateless, retry-tolerant, batch. **Avoid**: stateful primaries, long-running jobs without checkpointing.

      - **Graviton (ARM)**: AWS's ARM-based EC2 (m7g, c7g, r7g). Typically 20-30% cheaper for similar performance. Most modern container images are multi-arch. Just add `arm64` to NodePool requirements + use multi-arch images.

      - **Savings Plans / Reserved Instances**: on the always-on baseline (e.g., the bottom 30% of your average node count). Karpenter targets these instance types first; spot fills the bursts.

      - **Right-sizing**: tools like AWS Compute Optimizer + Karpenter's consolidation handle this automatically.

## 4. Compute for AI workloads

- **P5 / G5 (NVIDIA GPUs)**: training (P5 = H100; P4 = A100) + inference (G5 = A10G; G6 = L40S). **NVIDIA device plugin** exposes GPUs to K8s. Pod requests `nvidia.com/gpu: 1`.

      - **Inferentia 2 (Inf2)**: AWS-designed inference chip. Cheaper than GPU for served models. Requires **AWS Neuron SDK** + Neuron device plugin.

      - **Trainium 2 (Trn2)**: AWS-designed training chip. Scales to large clusters. Same Neuron SDK + device plugin.

      - **EFA (Elastic Fabric Adapter)**: low-latency network for distributed training. Required for NCCL all-reduce at scale on multi-node GPU. Specific instance types only (P5/Trn2). Karpenter NodePool requirement: `vpc.amazonaws.com/efa: "true"`.

    
    [ deep dive — skip if new ]For ML platform teams: dedicated Karpenter NodePool per accelerator family (GPU spot for training, Inferentia for serving, CPU for general). Each with appropriate taints + tolerations to keep general workloads off expensive accelerators.

## Before / After

**Before.** Cluster Autoscaler + 1-3 fixed-instance NGs. m5.large for everything. No spot. Reserved Instance commitment for the wrong instance family. Idle nodes overnight. Surprise AWS bill at quarter-end.

**After.** Karpenter picks instance per Pod. Spot 70% of compute. Graviton for new workloads (multi-arch images). RIs / SP on baseline only. Consolidation overnight reduces idle. Cost down 35-50% on the same workload mix.

Karpenter on EKS is one of the highest-leverage cost optimizations available — and it improves reliability (spot interruption handling, consolidation graceful) at the same time.

## Analogy — the K-Skyline floor

The Power Floor is the hum of the building. The dispatcher (Karpenter) sits at a console showing real-time demand from every floor (Pods). When a new workload arrives, dispatcher picks the best generator from the rental fleet (EC2): a Graviton-ARM unit for energy efficiency, a spot generator for non-critical loads, a GPU rig for the AI workshop. When demand drops, generators are released (consolidation). The fleet manager has SLAs (NodePool limits) and disruption budgets so critical workloads aren't turfed out at the wrong moment.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Power dispatcher console | Karpenter controller |
| Workload demand sheet | Pending Pods |
| Generator type catalogue | Instance families (c6i, m6i, c7g, P5, Inf2) |
| Energy-efficient ARM generator | Graviton (m7g, c7g, r7g) |
| Spot-rate generator | Spot capacity (60-90% off) |
| AI workshop's specialty rig | GPU / Inferentia / Trainium with Neuron + EFA |
| Releasing under-utilised generators | Consolidation (WhenUnderutilized) |
| Long-term lease on baseline | Savings Plans / RIs |

⚠️ *Analogy stops here:* The analogy stops here: real Karpenter is a controller speaking to AWS EC2 + ASG APIs, evaluating 100s of instance type options per pending Pod. The dispatcher metaphor undersells the optimization math.

## ELI5 / ELI10

**ELI5.** Smart power-station operator. Picks the right type of generator for the job (small for small jobs, big for big), uses cheap energy when possible, turns off generators when not needed.

**ELI10.** Karpenter = recommended EKS autoscaler. NodePool (workload constraints) + EC2NodeClass (AWS specifics). Picks instance type per Pod. Consolidation reduces idle. Spot for cost (60-90% off). Graviton ARM (~25% cheaper). Savings Plans on baseline. GPU/Inferentia/Trainium for AI with Neuron device plugin + EFA. EKS Auto Mode bundles Karpenter; self-managed Karpenter still common.

## Real-world scenarios

- **A SaaS using Karpenter + 70% spot.** Single NodePool: c6i / m6i / c7g / m7g instance families, spot+on-demand, WhenUnderutilized consolidation. Karpenter picks 70% spot, 30% on-demand for non-tolerant workloads. AWS bill ~40% lower than the same workload on managed NGs.
- **A bank using Karpenter + RIs on baseline.** Always-on baseline of ~30 m6i.large covered by Compute Savings Plans (~30% off SP rate). Karpenter's NodePool prefers m6i.large to land on the SP-covered capacity; spot for bursts. Cost-finance reconciliation easier; baseline predictable.
- **An ML team running PyTorch on P5 + EFA.** Dedicated NodePool: P5.48xlarge, EFA enabled, taint `nvidia.com/gpu`:NoSchedule. Training Pods tolerate; nothing else schedules there. NCCL benchmarks: 96% scaling efficiency 16 → 64 GPUs over EFA. Cost: $32K/month for the GPU pool; pays back in faster training cycles.
- **An inference team migrating CPU → Inferentia.** Identified 5 always-on inference Pods on c6i.4xlarge. Migrated models to Neuron-compiled versions; switched to Inf2.xlarge (~3× cheaper for the same throughput). Cost saved: ~$1500/month per service.

## Common misconceptions

- **Myth:** "Spot is too risky for production."
  **Truth:** Spot interruption is 2 min notice + Karpenter handles drain. For stateless workloads with PDBs, spot is fine in production. AWS's spot-interruption rate per instance type is published; pick types with low rates (often older generations).
- **Myth:** "Graviton requires re-architecting workloads."
  **Truth:** Most modern container images are multi-arch (or trivially rebuildable). Java, Go, Python, Node — all run on ARM. Test on staging; the gotchas are usually obscure native-binary dependencies (e.g., very-old C extensions in Python wheels).
- **Myth:** "Karpenter and Cluster Autoscaler can coexist."
  **Truth:** Technically yes, but they'll fight over scaling decisions. Pick one. Migration: install Karpenter, validate it's picking up Pending Pods, then disable CA on the relevant NGs.

## Recap

Karpenter is the recommended EKS autoscaler (and the engine inside Auto Mode). NodePool + EC2NodeClass + consolidation. Cost stack: spot + Graviton + Savings Plans on baseline + right-sizing. AI: GPU / Inferentia / Trainium with Neuron + EFA.

**Next — E7: EKS Security.** KMS encryption for secrets / EBS / EFS, GuardDuty EKS Protection + Runtime Monitoring, Security Hub, Inspector, ECR scanning + signing, Bottlerocket nodes, FIPS, CloudTrail.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
