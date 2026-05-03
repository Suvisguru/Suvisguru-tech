# K-OCP O10 — O10 · Multi-Cluster with ACM (RHACM)

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O10 · Multi-Cluster with ACM
> Companion preview: `/preview-kubernetes-ocp-lesson-10.html`.

---

**🎯 If you remember nothing else:** **RHACM hub manages many OCP + non-OCP K8s clusters as ManagedClusters. Placement selects by labels; ApplicationSet pushes apps; Policy + PlacementBinding governs fleet-wide; ObservabilityAddon aggregates. Add HCP for cluster-density + Submariner for cross-cluster networking.**

## 1. ManagedCluster + Placement + cluster lifecycle (HCP)

**RHACM hub cluster** = central management cluster running the **multicluster-engine (MCE)** + RHACM Operators. **ManagedCluster** CRs represent each managed cluster (OCP, EKS, GKE, AKS, OKD, k3s, etc.). Each ManagedCluster has a *klusterlet agent* running on it for hub-spoke communication.
    **Cluster registration:** two paths.
    
      - **Manual import**: admin runs `oc apply -f klusterlet.yaml` on the target cluster pointing at the hub.

      - **Cluster Lifecycle (Cluster Lifecycle / cluster API)**: hub provisions new OCP clusters from templates (ClusterDeployment / InstallConfig). Supports IPI + Hosted Control Planes (HCP). For HCP: control planes run as Pods inside hub or dedicated HCP-host clusters; data planes are workers in target environments.

    
    **Placement** CR selects ManagedClusters by labels:
    
      - ClusterSelector with matchLabels / matchExpressions.

      - NumberOfClusters constraint (e.g., "deploy to 3 clusters").

      - Tolerations + spread constraints.

    
    Result: a PlacementDecision listing which ManagedClusters match. Used by ApplicationSet, Policy, ObservabilityAddon.
    **Cluster pools** — pre-provisioned ClusterPools that warm-start clusters; admin claims a cluster from the pool when needed.

## 2. ApplicationSet (Argo CD-based) + Subscription model

**ApplicationSet** (Argo CD CR — RHACM ships managed Argo CD via OpenShift GitOps) — generates Argo CD `Application`s based on cluster-list generators tied to RHACM Placements.
    Generators include:
    
      - **Cluster generator** — creates an Application per cluster matching a label selector.

      - **List generator** — explicit list.

      - **Git generator** — derives clusters from files / directories in a Git repo.

      - **Matrix generator** — combine multiple generators.

    
    Result: same Helm chart / Kustomize / plain manifests deployed to many clusters with per-cluster parameterisation. Argo CD handles drift detection + sync per cluster.
    **RHACM Subscription model** (older path; Argo CD ApplicationSet is now preferred) — Channel + Subscription + PlacementRule for app deployment. Still works; mostly replaced by ApplicationSet for new fleets.

## 3. Policy + PlacementBinding — fleet-wide governance

**Policy** CR = a desired-state declaration enforced across managed clusters. Bound to clusters via **PlacementBinding** + Placement.
    **Policy types**:
    
      - **Configuration policies** (most common) — wrap arbitrary K8s resources with a desired-state intent.

      - **Compliance Operator** + RHACM integration — push CIS / NIST / PCI / FedRAMP / HIPAA scan results to the hub.

      - **Gatekeeper** integration — push Constraints + ConstraintTemplates fleet-wide.

    
    **Remediation modes**:
    
      - **inform** — Policy reports compliance status only (no enforcement).

      - **enforce** — RHACM creates / updates resources to bring clusters to desired state.

    
    **PolicySet** = bundle of related Policies + a single Placement.
    Use cases: enforce "all production clusters must have NetworkPolicy default-deny"; "all clusters must have Compliance Operator installed"; "all clusters must have RHACS Sensor." Centralised governance + per-cluster compliance dashboards.

## 4. ObservabilityAddon + Hosted Control Planes at scale + Submariner

**ObservabilityAddon** — aggregates Prometheus + Grafana metrics from all ManagedClusters into a multi-cluster observability stack on the hub. Built on Thanos. Single console for fleet-wide dashboards + alerting.
    **Hosted Control Planes (HCP) at scale via ACM:**
    
      - HCP control planes run as Pods on hosting clusters (could be the hub itself or dedicated HCP-host clusters).

      - Workloads (compute) run in target VPCs / on-prem environments — own data plane.

      - RHACM Cluster Lifecycle provisions + manages HCP clusters.

      - **Density**: dozens of clusters per HCP-host cluster vs traditional 3-master per cluster overhead.

    
    **Submariner integration:** RHACM federates Submariner CRs across ManagedClusters → cross-cluster Pod + Service networking. ServiceExport in cluster A makes a Service reachable from cluster B. Foundation for multi-cluster service mesh + DR.
    Use cases: regulated multi-cloud governance; dev / staging / prod fleet alignment via ApplicationSet; multi-region active-active with Submariner; HCP cluster-density at SaaS scale (per-tenant clusters).

## Before / After

**Before.** Pre-RHACM multi-cluster K8s ops = scripts looping kubectl across contexts; per-cluster Argo CD installs; per-cluster Compliance Operator; no fleet-wide observability; cluster provisioning via per-platform installers (Terraform / openshift-install) without coordination.

**After.** RHACM unifies: **ManagedCluster + Placement** for fleet membership; **ApplicationSet** (Argo CD) for fleet-wide deploys; **Policy + PlacementBinding** for governance; **ObservabilityAddon** for fleet-wide metrics; **HCP at scale** for cluster density; **Submariner** for cross-cluster networking; **Cluster Lifecycle** for provisioning new clusters from templates.

*One pane of glass for fleet ops; same operating model across OCP + EKS + GKE + AKS + on-prem.*

## Analogy — the K-Foundry bay

The **Multi-Foundry Network** is K-Foundry's federation hub. RHACM's hub cluster sits in the centre; spoke foundries register as **ManagedClusters**. Each spoke runs a **klusterlet agent** that phones home to the hub.
    The **Placement directory** selects spokes by label ("all production foundries in EU"). The hub uses Placements to drive: **ApplicationSet** (deploy workloads to selected spokes via Argo CD), **Policy** (enforce governance + compliance), **ObservabilityAddon** (aggregate metrics).
    The **Cluster Lifecycle Operator** can also provision new spokes (HCP-style — control plane Pods in the hub, workers in customer environments — for cluster density at SaaS scale).
    **Submariner integration** federates the spoke networks: a Service exported in spoke A becomes addressable from spoke B. Cross-foundry service mesh with no per-cluster DNS choreography.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| Federation hub | RHACM hub cluster + multicluster-engine (MCE) |
| Spoke foundry | ManagedCluster CR (OCP / EKS / GKE / AKS / on-prem) |
| Phone-home agent | klusterlet agent on each ManagedCluster |
| Spoke selector by label | Placement CR (ClusterSelector + NumberOfClusters) |
| Spoke selection result | PlacementDecision CR |
| Fleet-wide app deploy | ApplicationSet (Argo CD) + cluster generator |
| Older app subscription model | Channel + Subscription + PlacementRule (legacy) |
| Fleet-wide governance rule | Policy CR + PlacementBinding |
| Bundle of policies | PolicySet |
| Inform vs enforce remediation | Policy spec.remediationAction |
| Fleet-wide metrics dashboard | ObservabilityAddon (Thanos-based) |
| Cluster-density mgmt | Hosted Control Planes (HCP) provisioned via Cluster Lifecycle |
| Pre-warmed cluster pool | ClusterPool — claim cluster from pool |
| Cross-spoke service mesh | Submariner integration (ServiceExport / ServiceImport) |

⚠️ *Analogy stops here:* A real federation has fixed treaties; RHACM Placements + Policies are software-defined and reshape constantly. Klusterlet agent failure modes (network partition, hub unreachable) are real ops concerns the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** One central hub manages many factories. The hub has a directory of factories, an app-deployer that pushes to selected factories, a rule book everyone follows, and a metrics dashboard showing all factories together.

**ELI10.** RHACM hub = central management cluster + MCE Operators. ManagedCluster CR per cluster + klusterlet agent. Placement selects by labels → PlacementDecision. ApplicationSet (Argo CD) deploys apps fleet-wide. Policy + PlacementBinding enforces governance (inform/enforce). ObservabilityAddon = Thanos-based fleet metrics. HCP at scale via Cluster Lifecycle. Submariner integration for cross-cluster networking.

## Real-world scenarios

- **Bank — 50 OCP + 10 EKS clusters under one RHACM hub.** A bank registers 60 clusters into RHACM hub. PolicySet enforces: PSA Restricted, NetworkPolicy default-deny, RHACS Sensor installed, OADP backup configured. ApplicationSet deploys central services (ingress, monitoring, log shipper) to all clusters. ObservabilityAddon aggregates metrics. *One operations team manages 60 heterogeneous clusters.*
- **Telco — 800 SNO cell sites federated.** Telco runs OCP at 800 cell sites. Each SNO registered as ManagedCluster. ApplicationSet deploys site-specific 5G workloads + UPF inference. Policy enforces site-specific firewall rules. ObservabilityAddon collects per-site metrics. RHACM Cluster Lifecycle provisions new sites from templates.
- **SaaS — HCP cluster-per-tenant at scale.** A SaaS gives each enterprise tenant their own OCP cluster. Traditional 3-master-per-cluster = high overhead at 200 tenants. HCP via RHACM: control planes run as Pods inside 4 hosting clusters; tenants get their own data plane in their own VPC. Cluster Lifecycle provisions per tenant on signup. *Cluster density at SaaS scale.*
- **Active-active multi-region with Submariner.** OCP clusters in 3 regions registered to RHACM hub. Submariner integration federates Pod + Service networks. ServiceExport on critical microservices makes them addressable cross-region. Failover routes traffic across regions transparently. *Multi-region active-active without per-region DNS gymnastics.*

## Common misconceptions

- **Myth:** "RHACM only works with OCP clusters."
  **Truth:** RHACM (= upstream Open Cluster Management) supports any conformant K8s cluster: OCP, OKD, ROSA, ARO, OpenShift Dedicated, EKS, GKE, AKS, k3s, kubeadm, etc. Klusterlet agent is the universal hub-spoke bridge.
- **Myth:** "PolicySet enforce always = RHACM rewrites my workloads."
  **Truth:** PolicySet enforce mode reconciles to the desired state declared in the Policy. *Workloads not covered by the Policy are untouched.* Inform mode reports compliance only. Use enforce for cluster-config (NetworkPolicy / SCC bindings); use inform for compliance scans.
- **Myth:** "HCP is just a cost optimization."
  **Truth:** HCP (Hosted Control Planes) reduces per-cluster overhead but also enables cluster density at scale (dozens of clusters per host cluster), faster cluster provisioning (control plane = Pod set, not 3 VMs), and cleaner separation of cluster-mgmt from workload data plane. Cost is one benefit; speed + density + isolation are others.

## Recap

RHACM = hub + ManagedClusters + Placement + ApplicationSet + Policy + ObservabilityAddon + HCP + Submariner. One pane of glass for fleet ops across OCP + non-OCP K8s.

**Next — O11: OpenShift Observability.** Built-in Cluster Monitoring (Prometheus + Thanos Querier + Alertmanager) + User Workload Monitoring; OpenShift Logging (Loki + Vector); OpenShift Distributed Tracing (Tempo + OpenTelemetry); Network Observability (NetObserv + eBPF); Cluster Observability Operator.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
