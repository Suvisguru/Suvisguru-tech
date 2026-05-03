# K-EKS E2 — E2 · EKS Auto Mode — AWS Picks the Nodes

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E2 · EKS Auto Mode
> Companion preview: `/preview-kubernetes-eks-lesson-02.html`.

---

**🎯 If you remember nothing else:** EKS Auto Mode = AWS's built-in compute layer. You declare **NodePool** (label/taint/disruption rules) + **NodeClass** (instance constraints). AWS provisions EC2, picks instance type, manages lifecycle, consolidates idle, replaces nodes on a regular cadence (max node lifetime). Bundles core add-ons (VPC CNI, EBS CSI, LB controller, CoreDNS, GPU plugins, health checkers) — AWS upgrades them. **Auto Mode vs Managed NG vs Karpenter**: Auto Mode is the modern default for new clusters; doesn't fit every shop.

## 1. What Auto Mode owns and what it doesn't

Auto Mode (released GA in late 2024) is EKS's built-in compute and add-on layer. AWS bundles together:
    
      - **Compute provisioning** — Karpenter-style instance picking + provisioning + consolidation. AWS owns the controller; you don't install or upgrade it.

      - **Core add-ons** — VPC CNI, EBS CSI, AWS Load Balancer Controller, CoreDNS, kube-proxy. AWS keeps them updated; you don't install or upgrade them.

      - **Immutable AMIs** — Bottlerocket-based; AWS rotates regularly (max node lifetime).

      - **Health checks + auto-replace** — bad nodes get drained + replaced automatically.

    
    What Auto Mode doesn't own: your workloads, your IAM (still IRSA / Pod Identity), your VPC + subnet design, your storage decisions beyond EBS. You still write Deployments, Services, etc.

## 2. The two CRDs you actually write

Auto Mode uses Karpenter-style CRDs (familiar if you've run open-source Karpenter):
    `# NodePool — workload-facing rules
apiVersion: karpenter.sh/v1
kind: NodePool
metadata: {name: default}
spec:
  template:
    spec:
      nodeClassRef:
        group: eks.amazonaws.com
        kind: NodeClass
        name: default
      requirements:
      - {key: kubernetes.io/arch, operator: In, values: [amd64, arm64]}
      - {key: karpenter.sh/capacity-type, operator: In, values: [spot, on-demand]}
      taints: []
  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 30s
    expireAfter: 720h            # max node lifetime: 30 days
  limits: {cpu: 1000, memory: 1000Gi}

---
# NodeClass — Auto-Mode-specific config (subnet/SG selectors, etc.)
apiVersion: eks.amazonaws.com/v1
kind: NodeClass
metadata: {name: default}
spec:
  role: AmazonEKSAutoNodeRole
  subnetSelectorTerms:
  - tags: {kubernetes.io/role/internal-elb: "1"}
  securityGroupSelectorTerms:
  - tags: {Name: my-cluster-node-sg}`
    **NodePool** = workload constraints (arch, capacity type, instance family, disruption rules). **NodeClass** = AWS-specific networking (subnets, SGs, tags). Multiple NodePools per cluster is the norm (one for general, one for GPU, one for spot).

## 3. Consolidation, expiration, replacement

- **WhenUnderutilized consolidation**: Auto Mode periodically checks if running nodes can be replaced with fewer/cheaper ones. If yes, drains and recreates. The default; saves cost on bursty workloads.

      - **WhenEmpty consolidation**: only consolidate fully-empty nodes. Slower but more predictable; less Pod churn.

      - **consolidateAfter**: cooldown between consolidation passes (e.g., 30s). Prevents thrashing.

      - **expireAfter (max node lifetime)**: every node is replaced after N hours. Default 720h (30 days). Forces regular rotation; ensures latest AMI; bounds patch drift.

      - **disruption budgets**: per-NodePool, control how aggressively AWS can drain. Coordinated with PodDisruptionBudgets at the workload level.

    
    Auto Mode emits K8s events on each disruption: `kubectl get events -A | grep -i nodeclaim`. Watch for unexpected churn during bootstrap.

## 4. When to pick which

Managed NGKarpenter (DIY)EKS Auto Mode
      
        Who picks instance typeYou (per NG)Karpenter (per Pod)AWS Auto Mode (per Pod)
        Lifecycle ownerAWS lifecycle controllerYou operate KarpenterAWS Auto Mode
        ConsolidationNone (manual)YesYes (built-in)
        Add-on managementYou install + upgradeYou install + upgradeAWS bundles + upgrades
        CustomisationHigh (custom AMIs)High (Karpenter is yours)Lower (Bottlerocket only)
        Best forPredictable, capacity-known workloadsCost optimisation + controlNew clusters; small ops teams
      
    
    **2026 default**: new clusters → EKS Auto Mode unless you have a specific reason not to (custom AMI, kernel modules, regulatory, very-high-control). Existing Karpenter shops can migrate cluster-by-cluster.
    [ deep dive — skip if new ]Pricing: EKS Auto Mode adds a per-vCPU-hour management fee on top of EC2 cost. For a typical workload it's 12-15% premium. The math: you save the SRE time + you avoid most node-related incidents. Most teams find it worth it.

## Before / After

**Before.** Karpenter Helm chart pinned + monitored. ALB controller installed + IAM attached + CRDs upgraded. EBS CSI version-tracked. AMI bumps for each NG every quarter. Three add-ons to upgrade per K8s minor. Five hours of node-related ops per week.

**After.** Auto Mode toggled on. NodePool + NodeClass YAML in git. Add-ons managed by AWS. Node lifecycle, instance picking, consolidation, AMI rotation — all handled. Hours of node ops per week: 0-1.

Auto Mode is to nodes what EKS itself is to the control plane: AWS owns the operational toil; you keep the workload control.

## Analogy — the K-Skyline floor

The Concierge Service desk on the K-Skyline lobby. Tell the concierge what you need (NodePool: "this many guests, these dietary needs, this budget tier"); they assign rooms (NodeClasses → EC2 instances), refresh them on a schedule (max node lifetime), upgrade the bedding (AMI rotation), close unused rooms (consolidation). The concierge also manages the building's shared services (CNI, CSI, LB) so you don't. You walk in, hand them a list, and the rooms appear.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| The concierge service desk | EKS Auto Mode |
| Your guest list + needs | `NodePool` requirements |
| Room-type catalogue | `NodeClass` (subnets, SGs, instance constraints) |
| Refreshing rooms on a schedule | `expireAfter` (max node lifetime) |
| Combining lightly-occupied rooms | Consolidation (`WhenUnderutilized`) |
| Replacing a sick guest's room | Health-check + auto-replace |
| Hotel's shared utilities | Built-in CNI / CSI / LB / CoreDNS |
| Concierge tip on the bill | Auto Mode per-vCPU-hour premium |

⚠️ *Analogy stops here:* The analogy stops here: EKS Auto Mode is software, not staff. The "concierge" is a controller in the control plane reconciling NodePool/NodeClass to EC2 calls.

## ELI5 / ELI10

**ELI5.** You don't pick the rooms in the hotel — you tell the front desk what you need ("two adults, one cot") and they pick. They also clean and refresh the rooms automatically.

**ELI10.** EKS Auto Mode is Karpenter + core add-ons bundled into EKS, owned by AWS. You declare NodePool (workload constraints) + NodeClass (AWS-specific). AWS provisions EC2, manages lifecycle, consolidates idle, replaces nodes after expireAfter, and updates the bundled add-ons (VPC CNI, EBS CSI, LB controller, CoreDNS). vs Managed NG: AWS owns the lifecycle. vs Karpenter: AWS bundles + manages it. Premium ~12-15% on top of EC2.

## Real-world scenarios

- **A SaaS using Auto Mode for everything.** Single NodePool with arch In [amd64, arm64], spot+on-demand, WhenUnderutilized consolidation, expireAfter 7 days. Cluster of 25 workloads scales 8 → 30 nodes during day, consolidates back to 8 overnight. Add-ons just work. SRE team: 1.
- **A bank using Auto Mode + a separate managed NG.** Auto Mode for general workloads. Separate managed Node Group for a regulated workload requiring a hardened custom AMI Auto Mode doesn't support. Two compute paths in one cluster; both use the same VPC + IAM.
- **A startup migrating from Karpenter to Auto Mode.** Followed AWS's migration guide: paused Karpenter consolidation; uninstalled Karpenter Helm release; enabled Auto Mode; recreated NodePools with the new CRD shapes. Total downtime: 0 (Karpenter-managed nodes drained as Auto Mode took over). One sprint of validation.
- **A team picking Managed NG over Auto Mode.** Heavy use of EBS RAID-0 across multiple volumes, requires a custom Bottlerocket build with kernel modules. Auto Mode's standard AMI doesn't fit. Sticking with Managed NG + custom AMI; revisiting Auto Mode if AWS adds custom-AMI support.

## Common misconceptions

- **Myth:** "Auto Mode is just Karpenter renamed."
  **Truth:** Mostly true at the compute layer, but Auto Mode bundles core add-ons too (VPC CNI, EBS CSI, LB controller, CoreDNS). And AWS owns the lifecycle of all of that — you don't install or upgrade.
- **Myth:** "Auto Mode is more expensive than Managed NG + Karpenter."
  **Truth:** Per-vCPU premium ~12-15%. But you save SRE time on Karpenter ops + add-on upgrades + AMI lifecycle. For most teams the all-in TCO is similar or better.
- **Myth:** "Once on Auto Mode, you can't use other compute options."
  **Truth:** You can mix. Auto Mode + a separate Managed NG for a custom-AMI workload + Fargate for tiny workloads — all in one cluster.

## Recap

Auto Mode = Karpenter-style compute + bundled add-ons, AWS-owned. NodePool + NodeClass declare your wants; AWS provisions, lifecycles, consolidates, replaces. Modern default for new clusters; trade some control for less ops.

**Next — E3: AWS Networking for EKS.** VPC CNI internals, ENI exhaustion, AWS Load Balancer Controller, Gateway API via VPC Lattice, ExternalDNS, PrivateLink integration.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
