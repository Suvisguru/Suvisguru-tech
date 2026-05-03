# K-AKS A8 — A8 · AKS Add-ons and Platform Features

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A8 · Add-ons and Platform
> Companion preview: `/preview-kubernetes-aks-lesson-08.html`.

---

**🎯 If you remember nothing else:** **Use AKS managed add-ons (KEDA / Dapr / Istio / Flux / WI / KV provider / App Routing) instead of self-installed Helm charts. Arc-enable on-prem clusters; AKS Hybrid for Azure Local; Edge Essentials for single-node. Fleet Manager when you have many clusters.**

## 1. Managed add-ons — pre-built, supported, lifecycle-managed

AKS ships these as **managed add-ons** — Microsoft installs, upgrades, and supports them. Compared to bring-your-own Helm charts: faster onboarding, no Helm-rot, security patches automatic, fewer version-skew incidents.
    
      - **KEDA** (covered in A5) — event-driven Pod scaling.

      - **Dapr** — distributed application runtime: pluggable building blocks (state stores, pub/sub, secrets, bindings) via sidecar. Polyglot apps speak HTTP/gRPC to the Dapr sidecar instead of cloud SDKs. *Cleaner cloud-portability story.*

      - **Istio-based service mesh add-on** — Microsoft-managed Istio control plane. Sidecars on Pods (mTLS, traffic management, retries, observability). Released as the Microsoft-supported alternative to self-installed Istio / Linkerd. Be intentional: a service mesh is a real operational commitment.

      - **Flux v2 GitOps add-on** — continuous reconciliation from a Git repo. `FluxConfiguration` CRD wraps a GitRepository + Kustomization / HelmRelease. Replaces in-cluster Argo CD installs with managed Flux at the AKS Resource Provider level.

      - **Workload Identity** (covered in A2) — federated credentials for Pod auth.

      - **Azure Key Vault Secrets Provider** (covered in A4) — Secrets Store CSI driver + Azure Key Vault provider, packaged as a managed add-on.

      - **Application Routing add-on** (covered in A3) — managed NGINX ingress + cert-manager + Azure DNS.

    
    **Decision:** if a managed add-on covers your need, *use it*. The cost of self-installed Helm vs managed add-on is steep over time — broken upgrades, missing security patches, cluster-specific tribal knowledge.

## 2. Azure Arc-enabled Kubernetes — non-AKS clusters under Azure governance

**Azure Arc-enabled Kubernetes** = bring any conformant K8s cluster (on-prem, AWS EKS, GCP GKE, hand-rolled kubeadm, OpenShift, etc.) under Azure's management plane. Install the `azure-arc` agent in the cluster; the cluster appears as an Azure resource; you can apply Azure Policy, Defender, GitOps (Flux), Monitor (Container Insights), Workload Identity, Key Vault CSI — same surface as AKS.
    
      - **Use cases:** brownfield K8s clusters from acquisitions; multi-cloud K8s ops standardised on Azure tooling; on-prem clusters that need cloud-native security/observability without migrating workloads to AKS.

      - **Trade-off:** the cluster's control plane is still operated by you (or whoever runs the source cluster) — Arc gives you Azure-side management; it doesn't make a non-AKS cluster managed.

      - **Connectivity**: requires outbound HTTPS from the cluster to the Azure Arc Resource Bridge endpoints. Air-gapped clusters need disconnected Arc (preview).

## 3. AKS Hybrid + AKS Edge Essentials

**AKS on Azure Local (formerly Azure Stack HCI / AKS hybrid)** — full AKS control plane running on customer-owned hyperconverged infrastructure (HPE, Dell, Lenovo certified hardware running Azure Local OS). Same kubectl surface, same managed add-ons (where supported), same Azure governance via Arc. *For regulated workloads / data residency / data sovereignty.*
    **AKS Edge Essentials** — lightweight single-node (or small-cluster) AKS for Windows / Linux IoT edge devices. Designed for retail, factory floors, ATMs, kiosks. Manageable from Azure via Arc; runs on hardware as small as a NUC. *For workloads that must execute physically near the data source.*
    **Picking among on-prem options:**
    
      - Existing on-prem K8s, want Azure governance? → **Arc-enabled K8s**.

      - Building net-new on-prem and want Microsoft to operate the K8s + provide certified hardware? → **AKS on Azure Local**.

      - Edge / single-node / sub-second locality? → **AKS Edge Essentials**.

## 4. Azure Kubernetes Fleet Manager — many-cluster operations

**Fleet Manager** turns N AKS clusters into a single managed fleet. The Fleet itself is an Azure resource — you join member AKS clusters; Fleet provides:
    
      - **Workload propagation** — apply a K8s manifest (Deployment, ConfigMap, etc.) to all member clusters with one apply (or to a subset based on labels / selectors). *One source of truth for fleet-wide infra.*

      - **Cluster placement** — schedule a workload to specific clusters by label / region / capacity heuristics.

      - **Update orchestration** — coordinated cluster upgrade waves (e.g. dev first, prod second; one region at a time). Pause / resume / skip per cluster.

      - **Multi-cluster L4 load balancing** via Service Fabric Mesh-style features (preview / GA per region).

    
    **When you need Fleet Manager:** ~10+ AKS clusters, especially if any of (multi-region active-active, per-tenant cluster strategy, regulated/sovereignty isolation, or staged rollout discipline). *Below 10 clusters, manual ops + GitOps usually suffice.*

## Before / After

**Before.** Pre-managed-add-on AKS = Helm-everywhere. Engineers installed cert-manager, KEDA, Workload Identity, Secrets Store CSI, NGINX ingress, Dapr, Linkerd, Argo CD, and Prometheus Operator each as a Helm chart per cluster. Upgrades were per-chart per-cluster; chart break × cluster count = ops fire-quarter. Multi-cloud K8s had no unified governance — separate dashboards per provider; separate audit pipes; separate cost views. Multi-cluster ops required scripts looping over `kubectl --context`.

**After.** Modern AKS ships **managed add-ons** (KEDA, Dapr, Istio, Flux v2, WI, Key Vault provider, App Routing) — installed by the AKS Resource Provider, upgraded with the cluster, supported by Microsoft. **Azure Arc** brings non-AKS clusters under Azure governance. **AKS Hybrid + Edge Essentials** let AKS run on customer hardware. **Fleet Manager** turns 100 clusters into one fleet for workload propagation, placement, and coordinated upgrades.

*The era of "every team operates a Helm-chart farm" is over. Managed add-ons + Arc + Fleet shift the operational burden from per-cluster engineers to the AKS Resource Provider.*

## Analogy — the K-Campus wing

The **Student Union** is the building where shared services are stocked: copying machine, vending, post office, conference rooms. Faculty don't run their own copy machines.
    The **Counter Window** stocks managed add-ons. KEDA is the queue-watcher. Dapr is the universal adapter (any app speaks the Union's standard interface, the Union talks to whatever cloud DB or pub/sub exists outside). Istio is the in-house security and traffic engineer who walks every package between offices, signing it (mTLS), measuring delays (telemetry), and rerouting around closed corridors. Flux v2 is the daily reconciler — checks Git every minute and ensures every shelf in every wing matches the recipe in the book.
    The **Inter-campus Mailroom** (Azure Arc) reaches off-campus. Other campuses (on-prem K8s, EKS, GKE) sign up to share Azure governance — same Defender, same Policy, same Flux GitOps — without moving their buildings. **AKS Hybrid** is when Microsoft sends a turnkey campus building to your private estate. **Edge Essentials** is the satellite kiosk you set up at a single corner store.
    The **Provost's Office** (Fleet Manager) sits above all campuses — applies one curriculum to many campuses, schedules upgrade waves region by region, propagates one rule everywhere with one click.

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| Counter Window — shared services | Managed add-ons surface |
| Universal adapter | Dapr — pluggable building blocks via sidecar |
| In-house traffic engineer | Istio-based service mesh add-on |
| Daily reconciler | Flux v2 GitOps add-on |
| Queue-watcher | KEDA |
| Sealed-envelope worker permits | Workload Identity |
| Vault key-fetch desk | Key Vault Secrets Provider (Secrets Store CSI) |
| In-house mailroom (NGINX) | Application Routing add-on |
| Off-campus inter-campus mailroom | Azure Arc-enabled Kubernetes |
| Microsoft-built turnkey campus | AKS on Azure Local (Hybrid) |
| Single-corner satellite kiosk | AKS Edge Essentials |
| Provost's Office | Azure Kubernetes Fleet Manager |
| Coordinated curriculum updates | Fleet update orchestration / upgrade waves |

⚠️ *Analogy stops here:* A Provost can't actually micromanage every classroom; Fleet Manager can't hide K8s's eventual consistency or per-cluster RBAC nuances — workloads do still need per-cluster reconciliation.

## ELI5 / ELI10

**ELI5.** The Student Union has all the shared stuff. You don't run your own copy machine — you use the Union's. Same with the campus services: Microsoft runs the queue-watcher, the security guards, the daily Git syncer. You just turn them on.

**ELI10.** **Managed add-ons** = AKS-installed-and-supported KEDA / Dapr / Istio mesh / Flux v2 GitOps / Workload Identity / Key Vault provider / App Routing. **Arc-enabled K8s** brings non-AKS clusters under Azure governance (Policy / Defender / Monitor / Flux). **AKS Hybrid (Azure Local)** = Microsoft-operated AKS on certified customer hardware. **AKS Edge Essentials** = single-node edge AKS. **Fleet Manager** = workload propagation, placement, coordinated upgrades for 10+ AKS clusters.

## Real-world scenarios

- **SaaS — Dapr unifies polyglot stack.** A SaaS has services in Go, Python, Node, and .NET. Each team had picked its own state-store/pub-sub library. Dapr standardises: every service uses Dapr building blocks (state, pub/sub, secrets); Dapr sidecar talks to Cosmos DB, Service Bus, Key Vault. *One platform team owns infra integrations; product teams ship features faster.*
- **Brownfield M&A — Arc-enable acquired company's on-prem K8s.** A bank acquires a fintech with ten on-prem K8s clusters running OpenShift. Migration to AKS would take a year. Short-term: Arc-enable each cluster (one az command per cluster). Result: Defender for Containers + Azure Policy + Container Insights + Flux v2 GitOps + Workload Identity working on the legacy clusters in two weeks. *Compliance posture aligned without workload migration.*
- **Retail edge — AKS Edge Essentials at 800 stores.** A grocery chain runs inventory + POS workloads at each store. Per-store hardware: NUC running AKS Edge Essentials, single-node, Arc-connected for management. Workloads: local inventory cache, in-store ML for restock prediction. *800 single-node clusters managed centrally; deploys via Arc-enabled Flux.*
- **Multi-region SaaS — 100 clusters under Fleet Manager.** A SaaS runs 100 AKS clusters (5 regions × 20 tenants each). Fleet Manager joins all 100 as members. Common workloads (cluster autoscaler config, NetworkPolicy, ingress controller) deployed once via workload propagation. Upgrade orchestration cycles dev clusters first, prod next, by region wave. *One platform engineer manages the fleet; tenants don't see the choreography.*

## Common misconceptions

- **Myth:** "Managed add-on means I lose all configuration control."
  **Truth:** Managed add-ons are *opinionated* but not opaque. You configure them via standard CRDs (FluxConfiguration, ScaledObject, etc.) and Azure-side resources. What you give up is *installing/upgrading/patching the controller itself* — not the workload-level configuration.
- **Myth:** "Arc-enabled K8s is the same as AKS — I can run it the same way."
  **Truth:** Arc gives you Azure-side *management surface* (Policy, Defender, Monitor, Flux). The K8s control plane is still whatever it was — kubeadm, OpenShift, EKS, GKE. You're still on the hook for upgrades, scaling, patching of that control plane. AKS Hybrid (AKS on Azure Local) is the path where Microsoft operates the K8s control plane on your hardware.
- **Myth:** "Service mesh is always worth it."
  **Truth:** A service mesh is a real operational commitment — sidecar resource overhead, mesh-config drift, version-bump testing across hundreds of services. Worth it when you genuinely need mTLS-everywhere + L7 traffic management + cross-team observability. For a 5-service project, an mTLS mesh is probably yak-shaving. The Istio add-on lowers the bar but doesn't eliminate it.

## Recap

Managed add-ons replace Helm sprawl; Arc, Hybrid, and Edge Essentials extend AKS beyond Azure data centres; Fleet Manager handles many-cluster ops.

**Next — A9: AKS Upgrades and Operations.** AKS version support (N-2 + LTS); platform support N-3; AKS Release Tracker; auto-upgrade channels; node image upgrades; planned maintenance windows; surge upgrades; blue-green node pool migration; API deprecations; certificate rotation.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
