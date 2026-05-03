# K-AKS A1 — A1 · AKS Architecture and Shared Responsibility

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A1 · AKS Architecture
> Companion preview: `/preview-kubernetes-aks-lesson-01.html`.

---

**🎯 If you remember nothing else:** **AKS = Azure-managed control plane (free, multi-AZ) + customer-managed node pools (System / User / Spot / Win / GPU). Choose AKS Automatic for preconfigured observability and identity; AKS Standard for full control. Provision via Portal, az CLI, ARM/Bicep, Terraform, Pulumi, or Crossplane.**

## 1. AKS is the Azure-managed K8s control plane

**AKS is a managed Kubernetes service.** Azure operates the control plane (apiserver, etcd, scheduler, controller-manager) across availability zones. The control plane is **free** on the Free tier (no SLA), or paid on the Standard / Premium tiers (financially-backed SLA + LTS access). You SSH no etcd; you patch no apiserver. Azure does both.
    **What AKS does *not* manage:** your VNet, your node pools (the VMs that actually run Pods), your workloads, your IAM, your costs, your add-ons (unless you're on AKS Automatic), your DR. The mental rule: *everything below the apiserver is Azure's; everything above is yours.*
    **What runs in your subscription:** the *node resource group* (auto-created, named `MC_<rg>_<cluster>_<region>`) — contains the node pool VMSS, the cluster Load Balancer, and any add-on resources. *You can read it but should not edit it directly* — Azure reconciles changes back.

## 2. Five node-pool types and when to use each

An AKS cluster has at least one **node pool** = a VMSS (Virtual Machine Scale Set) of identical VMs. Five types:
    
      - **System node pool** (mandatory; minimum 1) — runs CoreDNS, metrics-server, AKS overlay agents, Konnectivity. Linux only. Taint: `CriticalAddonsOnly=true:NoSchedule` by convention so user workloads don't crowd it. *Don't run app workloads here — instability cascades.*

      - **User node pool** — your application workloads. Add as many as you need.

      - **Spot node pool** — discounted (up to 90% off) Spot VMs that Azure can evict with 30-second warning. Auto-tainted `kubernetes.azure.com/scalesetpriority=spot:NoSchedule` — workloads must explicitly tolerate.

      - **Windows node pool** — Windows Server 2022 nodes for .NET Framework workloads. Mixed Linux/Windows clusters are normal. Cannot run on the System pool — must add a separate Windows pool.

      - **GPU node pool** — Standard_NC* / ND* SKUs with NVIDIA drivers + the `nvidia.com/gpu` device plugin. AKS GPU image (`UbuntuGPU`) ships drivers preinstalled.

    
    **Pool-level config:** VM size, count (min/max for autoscaling), zones, taints, labels, OS SKU (Ubuntu 22.04 / Azure Linux 3 / Windows Server 2022), max-pods-per-node, OS disk type (Managed / Ephemeral), node image upgrade channel.

## 3. AKS Standard vs AKS Automatic

**AKS Standard** is the historical default: you create a cluster; you turn on add-ons one by one (Container Insights, Managed Prometheus, Workload Identity, Azure RBAC, etc.); you pick node pool sizes; you tune everything yourself. Highest flexibility, most setup.
    **AKS Automatic** (GA April 2025) preconfigures the production-ready stack: **Managed Prometheus + Managed Grafana + Container Insights** (observability), **Workload Identity + Azure RBAC for K8s + local accounts disabled** (identity), **NAP (Node Auto Provisioning)** instead of manual node pools, **KEDA + VPA** for autoscaling, **image cleaner + auto-upgrade** for ops, **NetworkPolicy via Cilium** by default. *You declare workloads; Azure picks node sizes, scales, patches, and observes.*
    **Pick Automatic if:** standard production AKS, and you're happy delegating size/scaling decisions. **Pick Standard if:** you need fine-grained control (custom CNI, Windows-only clusters, FIPS compliance, custom node images, specific add-on combinations Automatic doesn't support).

## 4. Six ways to provision an AKS cluster

Pick one tool and stick with it across the lifecycle. Mixing tools = drift. The six common paths:
    
      - **Azure Portal** — for a one-off learning cluster or a quick demo. Not for production (no source of truth).

      - **Azure CLI (`az aks create`)** — interactive scripting, ad-hoc clusters. Good for runbooks. The Portal generates equivalent CLI commands.

      - **ARM / Bicep** — Azure-native IaC. Bicep is the modern syntax (compiled to ARM JSON). Tight Azure integration; deploys via `az deployment group create`.

      - **Terraform AzureRM provider** — the most popular cross-platform IaC for AKS. Strong community, mature modules. State management is your responsibility (use Azure Storage backend with state locking).

      - **Pulumi** — IaC in real programming languages (TypeScript, Python, Go, C#). Same Azure resources as Terraform; more expressive for complex logic.

      - **Crossplane** — Kubernetes-native IaC (Azure resources as Custom Resources reconciled by a control-plane cluster). Useful when AKS provisions other AKS clusters via GitOps.

    
    **Production rule:** AKS clusters live in Git via Bicep / Terraform / Pulumi / Crossplane. Portal + CLI for exploration only.

## Before / After

**Before.** "K8s in Azure" used to mean **aks-engine** (deprecated) or hand-rolled VMSS + kubeadm. Operators wrote ARM templates that provisioned VMs, ran cloud-init scripts to install kubelet/kubeadm, bootstrapped the control plane on three VMs, configured etcd Raft, secured certs by hand, and were responsible for every patch. **Six weeks to a working cluster; one ops engineer per cluster, full-time.**

**After.** AKS gives you a control plane in 5-10 minutes via `az aks create` or one Bicep file. Azure runs apiserver + etcd + scheduler + controller-manager across AZs, free. **AKS Automatic** goes further: it preconfigures Managed Prometheus + Grafana + Container Insights + Workload Identity + Azure RBAC + NAP + KEDA in the same call. **Six minutes to a production-shaped cluster; one ops engineer manages dozens.** The remaining work is what you uniquely care about: VNet design, identity model, workloads, cost.

*The six-weeks-of-cluster-plumbing era is over. The trade-off: you must learn AKS's opinions (node resource group, AKS Automatic defaults, version policy) instead of K8s's opinions.*

## Analogy — the K-Campus wing

K-Campus is the Azure-managed campus complex. The **Welcome Center** is where you arrive: there's a wall map, a glass case showing the campus floor plan, and a Facilities Director who explains the rules. Azure (the Facilities Director) operates the lights, the HVAC, the alarm system, and the campus shuttle — you (the Faculty) lease wings of buildings to host your departments. The map shows which buildings Azure runs and which buildings *you* run.
    The Welcome Center wall has two big panels. **Left panel: Azure runs this** — the central plant, the campus DNS, the security cameras, the elevators. You don't see them; you can't edit them; they just work. **Right panel: You run this** — your department offices (workloads), the staff you hire (identity), the storerooms (storage), the budget. *Everything visible from the floor plan is one of those two columns.* No surprise pre-existing buildings. No "shared" buildings.
    Some Faculty pick **AKS Standard** — they want to choose every paint colour and every desk arrangement themselves. Other Faculty pick **AKS Automatic** — they want Azure to set up the projector, the whiteboard, the lighting, and the fire alarm with sensible defaults so they can teach class on day one.

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| Welcome Center floor plan | AKS shared-responsibility model |
| Facilities Director (Azure) | Azure-managed control plane |
| Left panel — Azure runs this | kube-apiserver, etcd, scheduler, controller-manager |
| Right panel — you run this | VNet, node pools, workloads, IAM, costs |
| Wings of the campus | Node pools — System, User, Spot, Windows, GPU |
| The mandatory front desk | System node pool (CoreDNS, metrics-server) |
| Pre-furnished classroom | AKS Automatic |
| Empty classroom you furnish | AKS Standard |
| Building keys + ID badge | Cluster identity (managed identity) |
| Service-room next door | Node Resource Group (MC_*) |
| Architectural blueprint repo | Bicep / Terraform / Pulumi / Crossplane |

⚠️ *Analogy stops here:* The campus has fixed walls; an AKS cluster has elastic node pools that grow and shrink during the day. The Welcome Center map is a snapshot; reality is a movie.

## ELI5 / ELI10

**ELI5.** Azure runs a giant brain at the campus that decides where your work happens. You bring the workers (your apps). Azure picks the rooms; the brain tells the workers which room to go to. You pay for the rooms, not the brain.

**ELI10.** AKS is Azure operating the K8s control plane (apiserver, etcd, scheduler, controller-manager) across availability zones for free, while you operate the node pools (VMSS of VMs) where your Pods actually run. There are five node-pool flavours (System / User / Spot / Windows / GPU). You can take the no-decisions path with **AKS Automatic** (preconfigures Managed Prometheus, Grafana, Container Insights, Workload Identity, NAP, KEDA) or the full-control path with **AKS Standard**. Provision via Portal, Azure CLI, Bicep, Terraform, Pulumi, or Crossplane.

## Real-world scenarios

- **Mid-size SaaS, first AKS cluster — picks AKS Automatic.** A 50-engineer SaaS migrating from VMs to K8s. They have no platform team and don't want one. They pick **AKS Automatic**. In one `az aks create` command they get: Managed Prometheus + Grafana, Container Insights, Workload Identity, Azure RBAC, NAP for compute, KEDA + VPA, image cleaner, auto-upgrade. *Day-1 production-shaped cluster with no Helm charts to install.* Trade-off: less knob-twiddling. Worth it for them.
- **Bank, regulatory cluster — picks AKS Standard.** A bank running PCI workloads. They need: a custom NSG ruleset, BYO Cilium with strict NetworkPolicies, FIPS-validated node images, locked-down ACR, no preview features, audit logs to a specific Log Analytics workspace. *AKS Automatic doesn't yet support all those constraints together*. They pick **AKS Standard** and configure each add-on manually via Bicep. Higher setup cost; required for compliance.
- **ML team, GPU spike workloads.** A 200-engineer ML team runs hyperparameter sweeps. Three node pools: **System** (D-series, 3 nodes), **User** (D-series autoscale 5-50 for inference), **GPU Spot** (NC-series A100, autoscale 0-100). The Spot pool runs sweeps; gets evicted; sweeps checkpoint and resume on the next eviction-tolerant node. *Cost: 70% lower than always-on GPU; same throughput.*
- **Multi-tenant SaaS, Crossplane provisions per-tenant clusters.** A SaaS where each enterprise tenant gets their own AKS cluster. Provisioning by hand isn't viable at 200 tenants. They run a single **management AKS cluster** with **Crossplane + Azure provider**. New tenant arrives → operator commits a Tenant CR to git → Argo CD syncs → Crossplane reconciles a new AKS cluster + identity + ACR + Key Vault for that tenant. *Cluster provisioning becomes a git PR.*

## Common misconceptions

- **Myth:** "The control plane is free, so AKS is free."
  **Truth:** Free Tier control plane (no SLA) is free. **Standard Tier** (production SLA) is $0.10/cluster/hour ≈ $73/month. **Premium Tier** (LTS support) is $0.60/cluster/hour. Plus you pay for every node VM, every Managed Disk, every Load Balancer, every public IP, every Log Analytics ingest GB. Control-plane fee is a small fraction; data-plane is the bill.
- **Myth:** "I should run my workloads on the System node pool to save money."
  **Truth:** The System pool is conventionally tainted `CriticalAddonsOnly=true:NoSchedule`. Bypassing the taint means CoreDNS, metrics-server, and Konnectivity compete for CPU with your apps — and a noisy app will starve cluster-critical components. A user pool of the same VM SKU is the same cost.
- **Myth:** "AKS Automatic is just AKS Standard with autoscaling enabled."
  **Truth:** AKS Automatic preconfigures a coherent *production stack*: Managed Prometheus + Grafana + Container Insights observability, Workload Identity + Azure RBAC + local-accounts-disabled identity, NAP for node provisioning, KEDA + VPA for scaling, image cleaner, auto-upgrade, NetworkPolicy via Cilium. It also *removes* some knobs (you can't change the network plugin to Kubenet, can't turn off Workload Identity). Not a flag; a different cluster shape.

## Recap

You can now point at the AKS shared-responsibility split, name the five node-pool types, choose between AKS Standard and AKS Automatic, and pick a provisioning tool. The Welcome Center map is internalised.

**Next — A2: Azure Identity and Access.** Microsoft Entra ID, Workload Identity (replaces Pod Identity), Azure RBAC for K8s, kubelogin, ACR + Key Vault integration, Conditional Access for kubectl.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
