# K-EKS E1 — E1 · EKS Architecture and Shared Responsibility

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E1 · EKS Architecture
> Companion preview: `/preview-kubernetes-eks-lesson-01.html`.

---

**🎯 If you remember nothing else:** EKS = AWS runs control plane (apiserver, etcd, scheduler, controller-manager) across 3 AZs. You run the rest: nodes (5 options), VPC, IAM, workloads, cost. **Version policy**: 14 months standard support + 12 months extended support per minor. Track AWS's EKS version lifecycle, not just upstream. Provision via Console / AWS CLI / eksctl / Terraform / EKS Blueprints / CDK / Pulumi / Crossplane.

## 1. What EKS is and isn't

EKS is Amazon's managed Kubernetes. AWS operates the control plane: 3 apiservers in 3 AZs behind an NLB, etcd cluster, scheduler, controller-manager, addon controllers — all running on AWS-owned infrastructure you never SSH into. AWS patches them, scales them, monitors them. You hit a single endpoint (`https://<clusterID>.gr7.us-east-1.eks.amazonaws.com`) and call it a cluster.
    What EKS is *not*: a runtime for your workloads (those run on nodes you provision). A network manager (you own the VPC + subnets + SGs). An identity store (you wire IAM ↔ K8s RBAC yourself). A cost-control system (you choose instances + autoscaling + spot). EKS is *K8s minus control-plane operations*. Everything else is yours.

## 2. Where your Pods actually run

OptionWhat it isWhen
      
        **Managed Node Groups**EC2 ASGs AWS provisions + lifecycle-manages. You pick instance type + count + AMI. AWS handles drains + rolling updates on AMI/version refresh.Default for most teams. Predictable, simple.
        **Self-managed nodes**You bring your own ASG / EC2 + join to the cluster. Maximum control; maximum operational burden.Custom AMIs (Bottlerocket variants, hardened images), niche kernel modules, regulated environments needing full ownership.
        **AWS Fargate**Serverless Pods. No nodes; AWS schedules each Pod on its own micro-VM. Pay per Pod-second.Bursty / event-driven; teams that don't want to think about nodes; small simple workloads.
        **EKS Auto Mode**AWS picks the right EC2 instance per Pod, manages lifecycle + upgrades + consolidation. Like Karpenter built into the cluster.Modern default for new clusters in 2026 (covered in detail in E2).
        **EKS Hybrid Nodes**On-prem / edge nodes joining an EKS cluster. Useful for hybrid workloads.Bursty cloud + steady on-prem; latency-sensitive workloads at the edge.
      
    
    **You can mix node options in one cluster.** Critical workloads on managed NG; bursty on Fargate; everything else on EKS Auto Mode is a common pattern in 2026.

## 3. The five EKS-specific decisions you make once

- **EKS platform version:** a minor K8s version + patch + AWS extensions. AWS releases new platform versions ~monthly. Track via `aws eks describe-cluster --query cluster.platformVersion`.

      - **Cluster endpoint access**: public, private, or hybrid (public + private). Production should use **private** (your VPC routes to the EKS endpoint via PrivateLink-like ENIs) for security; **hybrid** if you need `kubectl` from a corporate network without VPN.

      - **Cluster security groups**: AWS creates one for the control plane; nodes get a separate one. Worker SG allows 443 to control plane; control plane SG allows API traffic from worker subnets.

      - **VPC + subnet design**: at least 2 (preferably 3) AZs. Public subnets for ELBs; private subnets for nodes. Plan IP space — the AWS VPC CNI (E3) burns ENIs and secondary IPs aggressively.

      - **Tagging**: tag every EKS resource (cluster, nodegroup, EBS volumes, ENIs). Cost allocation, automation, compliance — all rely on tags.

## 4. How clusters get created

- **AWS Console** — quickest demo path. Production: never (no audit trail).

      - **AWS CLI** — `aws eks create-cluster`. Scriptable but verbose.

      - **eksctl** — Weaveworks-built, AWS-blessed. Single YAML defines cluster + nodegroups + addons. Standard for hands-on / labs.

      - **Terraform / EKS Blueprints** — for IaC shops. EKS Blueprints (community) provide opinionated, batteries-included Terraform modules. The 2026 production default for serious shops.

      - **AWS CDK** — for TypeScript/Python orgs. `aws-cdk-lib/aws-eks`.

      - **Pulumi** — multi-language, similar shape to CDK.

      - **Crossplane** — declarative AWS resources via K8s CRDs. "K8s creates EKS clusters" — useful for fleet management.

    
    **Version policy that matters in 2026:** AWS gives 14 months of **standard support** per minor version (matching upstream K8s patch support window) + 12 additional months of **extended support** at $0.60/hour premium per cluster. After standard support ends, you pay extra OR upgrade. Plan upgrade cadence around AWS's lifecycle, not just upstream's.
    [ deep dive — skip if new ]The standard support timeline ≈ 14 months because AWS lags upstream by ~1-3 months on minor release availability + the upstream patch window is ~12 months. Always check `aws eks describe-cluster-versions` + the EKS docs for current dates.

## Before / After

**Before.** Self-managed K8s on EC2: kubeadm, kube-vip, manual etcd backups, OS patching schedule, control-plane HA you operate, version upgrades you orchestrate. Plus all the AWS networking + IAM + storage. Two SREs full-time minimum.

**After.** EKS: AWS runs the control plane. You define cluster + node options + IAM + network in IaC. Half an SRE. Trade-off: $0.10/hour per cluster (~$876/year), $0.60/hour during extended support, plus you give up some kernel + control-plane tunability.

EKS is right when AWS is your home + control-plane ops aren't your differentiator. K-VAN is right when you need that ownership.

## Analogy — the K-Skyline floor

Welcome to K-Skyline — the AWS Region's premier managed-K8s tower. The lobby is bright; the floor plan is on the wall. The building manager (AWS) operates the elevators (apiserver), the central HVAC (etcd), the back office (scheduler + controller-manager). You rent units (clusters); you furnish them (workloads); you pay for the power you draw (instance hours, storage, traffic). The lobby map shows ten more floors (E2-E11) — each handles one piece of the tenancy: who delivers your packages (networking), who lets visitors in (identity), where your storage is (vault), how upgrades happen (renovation wing), and so on.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Tower lobby + floor plan | EKS architecture |
| Building manager (AWS staff) | AWS-managed control plane |
| The elevator banks | kube-apiserver behind an NLB |
| Central HVAC humming below | etcd cluster |
| Your rented unit | EKS cluster (you provision) |
| How the unit's wired into the building | VPC + subnets + security groups |
| Who staffs your unit | Node options: managed NG / self-managed / Fargate / Auto Mode / Hybrid |
| Your monthly statement | Cluster $0.10/h + node + storage + traffic; +$0.60/h during extended support |

⚠️ *Analogy stops here:* The analogy stops here: real EKS isn't a single building — it's a regional service spanning 3+ AZs with cross-AZ replication. Tower metaphor undersells the multi-AZ nature.

## ELI5 / ELI10

**ELI5.** AWS runs the brain of your Kubernetes cluster (the control plane). You bring the workers (the nodes) and decide how they look. Like renting a serviced apartment vs building your own house.

**ELI10.** EKS = managed K8s control plane (apiserver/etcd/scheduler/controller-manager) running on AWS infra across 3 AZs, auto-patched, highly available. You bring nodes (5 options: managed NG / self-managed / Fargate / Auto Mode / Hybrid), VPC, IAM, workloads. Version policy: 14 months standard support + 12 months extended support per minor. Provision via Console / AWS CLI / eksctl / Terraform / CDK / Pulumi / Crossplane. EKS Blueprints is the modern Terraform-based default.

## Real-world scenarios

- **A SaaS using EKS Auto Mode + Argo CD.** Single multi-AZ cluster. Auto Mode handles every node decision. Argo CD pulls from git for workload manifests + add-ons. Two engineers part-time. ~$5K/month for 60 small workloads at scale; AWS handles control plane upgrades transparently.
- **A bank with private endpoint + managed NG.** Cluster endpoint private only. `kubectl` reachable via internal Direct Connect from corporate network. Managed Node Groups with hardened Bottlerocket AMIs (Module E7). Version pinned 1 minor behind latest; quarterly upgrades. Compliance approved.
- **A startup using eksctl for fast iteration.** Single YAML file per cluster (dev/staging/prod). `eksctl create cluster -f cluster-prod.yaml` spins up cluster + nodegroups + add-ons + IRSA in one command. Cluster creation: ~15 min. Migration to Terraform planned at scale.
- **A team using EKS Blueprints (Terraform).** Terraform module defines: VPC, EKS cluster, managed NG, Fargate profiles, IAM roles, IRSA roles, add-ons (CNI/CoreDNS/EBS CSI), Karpenter, ALB controller, ExternalDNS. New cluster = `terraform apply`. Production-grade defaults baked in.

## Common misconceptions

- **Myth:** "EKS handles everything for me."
  **Truth:** EKS handles the control plane. You handle nodes, networking, IAM, workloads, cost, security posture, observability, upgrades of nodes/add-ons. The shared-responsibility line is sharp.
- **Myth:** "Cluster endpoint should be public for kubectl convenience."
  **Truth:** Production should be private (or private + hybrid with strict allowlists). Public endpoint = the K8s API on the internet, protected only by IAM auth. One mis-scoped IAM grant + you're a target.
- **Myth:** "Standard support is forever."
  **Truth:** ~14 months per minor. After that, extended support kicks in at $0.60/hour premium. AWS will eventually deprecate. Track AWS's lifecycle, not just upstream's.

## Recap

EKS = AWS-managed control plane + your-managed nodes/network/IAM/workloads. Five node options. 14+12 months version support. Provision via eksctl (start) → Terraform/Blueprints (scale) → Crossplane (fleet).

**Next — E2: EKS Auto Mode.** Modern default for new clusters. AWS picks EC2 + handles lifecycle + consolidation. Like Karpenter built into the cluster.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
