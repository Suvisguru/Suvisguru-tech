# K-OCP O13 — O13 · Capstone — Multi-Tenant OCP Reference Foundry

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O13 · Capstone Foundry
> Companion preview: `/preview-kubernetes-ocp-lesson-13.html`.

---

**🎯 If you remember nothing else:** **Build the four-phase stack: Phase A (IPI base + EUS + private + OVN-K), Phase B (ODF + SCCs + RHACS + observability), Phase C (Pipelines + GitOps + Virtualization + OADP + disconnected), Phase D (RHACM federation + live drill + must-gather pack). Defend it.**

## 1. Phase A — IPI base + EUS + private + OVN-K

**Goal:** a defendable base cluster with no public attack surface, modern networking, EUS-channel stability, and HCP-ready for multi-tenant.
    
      - **Installation:** IPI on bare metal (with Redfish-supported hardware) or AWS. 3 master + 5 worker minimum; add ODF storage nodes (3+) on bare metal. Plan for HCP host capacity if multi-tenant cluster-per-customer.

      - **Channel:** EUS for ~24-month support window. Premium subscription tier.

      - **Private cluster:** apiserver via private endpoint + master authorized networks; no public LB. SSH disabled (RHCOS default).

      - **Networking:** OVN-Kubernetes (default); cluster network /14 + service network /16; multi-zonal worker nodes (for cloud) or multi-rack (for bare metal).

      - **Cluster identity:** least-privilege node SA + per-tenant ServiceAccounts. Workload Identity Federation for Pod-to-cloud (where applicable).

      - **Maintenance:** EUS upgrade cadence (every 2 years EUS-to-EUS). MachineConfigPool roll discipline. `oc adm upgrade` with conditional risk assessment.

    
    *Phase A success criterion:* cluster created via `openshift-install`; private + EUS; no public IPs in MC_*; `oc adm upgrade` shows clean upgrade path; etcd backup scheduled.

## 2. Phase B — ODF + SCCs + RHACS + observability

**Storage**:
    
      - **ODF** on 3-5 dedicated worker nodes with attached storage (NVMe). CephRBD for RWO; CephFS for RWX; NooBaa for object (registry + Prometheus long-term + OADP destination).

      - Per-cloud CSI for cloud-installed clusters; ODF for on-prem.

      - **Internal registry** on NooBaa (zone-resilient).

    
    **Identity + Security**:
    
      - **OAuth** integrated with corp OIDC / LDAP; HTPasswd as break-glass.

      - **OCP RBAC** with least-privilege; Project-scoped admins per tenant.

      - **SCCs**: restricted-v2 default; only escalate explicitly per workload SA via documented exception process.

      - **RHACS / StackRox**: deploy Central + Sensor on each ManagedCluster (via RHACM Policy). Vuln + compliance + network graph + runtime + admission.

      - **Compliance Operator**: weekly CIS + PCI-DSS scans; auto-remediation where applicable.

      - **Binary Authorization-equivalent**: Cosign-signed images + Policy Controller verify signature at admission.

      - **FIPS** mode if federal compliance required (install-time choice).

    
    **Observability**:
    
      - Cluster Monitoring (built-in) + UWM for app metrics. Long-term storage to NooBaa S3.

      - OpenShift Logging (Loki + Vector); apps / infra / audit streams routed appropriately. Audit stream forwarded to SOC Splunk.

      - Distributed Tracing (Tempo + OTel) for app-tier visibility.

      - NetObserv (eBPF) for network flow visibility.

      - **SLO-first alerting**: burn-rate alerts via Prometheus rules; Alertmanager → PagerDuty.

    
    *Phase B success criterion:* sample app deploys via Pipelines; pulls Secret Manager secret via Workload Identity Federation; serves traffic through Routes; appears in Cluster Monitoring + Logging + Tracing dashboards with burn-rate alert.

## 3. Phase C — Pipelines + GitOps + Virtualization + OADP + disconnected

**CI/CD**:
    
      - **OpenShift Pipelines (Tekton)**: PipelineRun on PR; build via S2I or Docker strategy; output to internal registry; sign with Cosign; tag in ImageStream.

      - **OpenShift GitOps (Argo CD)**: 3 repos — cluster-config, platform (RHACS, Logging, Monitoring, ODF, MetalLB, etc.), workloads. RootSync + RepoSync. Drift detection on.

      - Promotion: Pipeline tags image; Argo CD detects + reconciles to staging; manual gate to prod.

    
    **Virtualization workload**:
    
      - OpenShift Virtualization Operator installed.

      - Migration Toolkit for Virtualization (MTV) ingests legacy Windows VMs from vSphere.

      - VMs run alongside container workloads; same RBAC + SCCs (anyuid where the VM image needs it); same monitoring + logging.

      - Live migration enabled for maintenance drains.

    
    **DR**:
    
      - **OADP (Velero-based)**: nightly cluster-wide backup + PV snapshots; cross-region replicated to NooBaa S3 in DR region.

      - **etcd backup**: scheduled daily + weekly + monthly retention; ship snapshots off-cluster.

      - RTO target 60 min for full cluster restore; RPO 24h. *Tested quarterly* via blue-green cluster restore drill.

    
    **Disconnected update path**:
    
      - Mirror registry (Quay or mirror-registry).

      - oc-mirror with ImageSetConfiguration for OCP releases + Operator catalogs.

      - Disconnected OSUS Operator for upgrade graph.

      - Sneakernet / data-diode procedure documented.

    
    *Phase C success criterion:* three pull requests can change cluster behaviour; one DR drill restores cluster within RTO; disconnected patch tested end-to-end.

## 4. Phase D — RHACM federation + defence + live drill + must-gather pack

**RHACM federation**:
    
      - RHACM hub cluster (could be the platform cluster or a dedicated mgmt cluster).

      - Each tenant cluster registered as ManagedCluster (via klusterlet).

      - PolicySet enforces fleet-wide: NetworkPolicy default-deny, RHACS Sensor installed, OADP backup configured, PSA Restricted, Binary Auth attestor.

      - ApplicationSet pushes baseline platform services to all clusters.

      - ObservabilityAddon aggregates fleet metrics.

      - HCP Cluster Lifecycle for cluster-density at scale (per-tenant clusters via HCP).

    
    **Architecture defence** (60 min, with senior platform reviewer):
    
      - Walk the network diagram — VPC, subnets, OVN-K CIDRs, Routes / AGC, MetalLB BGP.

      - Walk the identity diagram — OAuth IDP, OCP RBAC + Project-scoped admins, SCC matrix per workload.

      - Walk the storage diagram — ODF Ceph topology, NooBaa S3 destinations (registry, monitoring, OADP), CephFS RWX usage.

      - Walk the security stack — Compliance Operator scans + history, RHACS posture + runtime + admission, Cosign signing pipeline.

      - Walk the observability diagram — three pipes (metrics + logs + traces) + NetObserv + COO; SLOs + burn-rate alerts; on-call playbook.

      - Walk the upgrade runbook — EUS channel, MCP roll discipline, surge upgrade, blue-green node-pool fallback, disconnected mirror.

      - Walk the DR runbook — OADP schedule, etcd backup schedule, restore steps, RTO/RPO, drill cadence.

      - Walk the AI / Virt workload runbook — KubeVirt VM lifecycle, KServe inference, MTV migration plan.

    
    **Live drill** (90 min):
    
      - Reviewer kills a worker node. MCO + MachineSet replace; workloads re-schedule; ODF rebalances; CO's stay Available.

      - Reviewer revokes an OCP RBAC binding for an SA. Pod throws 403; Audit Logs + Logs Explorer surface; restore + postmortem in 15 min.

      - Reviewer applies a critical CTD finding. RHACS triage → admission policy hardening → PolicySet update via RHACM.

      - Reviewer initiates DR scenario: restore latest OADP backup into a sibling cluster within RTO. Validate workloads.

      - Reviewer simulates 10× inference burst. KServe scales; ODF + Prometheus storage hold; SLO maintained.

      - Reviewer simulates etcd quorum loss. Documented disaster-recovery procedure restores from snapshot.

    
    **must-gather pack:** standard `oc adm must-gather` + targeted gathers (Logging, Tracing, NetObserv, ODF, RHACS, OADP, RHACM, Virtualization). Pre-canned bundle for first-response support cases.
    *K-OCP-complete*: Bicep / Terraform / OpenShift install configs + per-cluster Markdown architecture doc + DR runbook + AI runbook + Virt runbook + must-gather pack + live-drill recording.

## Before / After

**Before.** Pre-K-OCP-curriculum operators built OCP clusters one feature at a time: install IPI, then add Logging Operator manually, then ODF without planning storage topology, then RHACS as an afterthought, then GitOps installed via Helm-instead-of-Operator, no etcd backup schedule, no disconnected mirror, no must-gather pack, no DR drill. *Tribal knowledge in three engineers' heads.*

**After.** The K-OCP reference foundry is **defendable**: every choice justified, every alternative considered, every failure mode mapped. *IPI + EUS + private + OVN-K* for base; *ODF + SCCs + RHACS + observability* for platform; *Pipelines + GitOps + Virt + OADP + disconnected* for ops; *RHACM federation + defence + drill + must-gather* for confidence. A new operator can read the architecture doc, run the runbooks, and operate the cluster.

*You can't cargo-cult a reference foundry from the internet — you have to walk every choice yourself. K-OCP Capstone is that walk, defended.*

## Analogy — the K-Foundry bay

The **Grand Opening** at K-Foundry is the graduation event. Today you're the candidate. Four phases.
    **Phase A — your base foundry** (IPI + EUS + private + OVN-K). Foundation poured: 3 control nodes + workers + ODF storage; private apiserver; long-term-lease subscription (EUS); modern networking with Routes + AGC.
    **Phase B — your services** (ODF + SCCs + RHACS + observability). Inventory warehouse stocked (ODF block + RWX + S3); Safety Office staffed (SCCs default-restricted-v2 + RHACS + Compliance + Cosign); Control Tower running (Cluster Monitoring + Logging + Tracing + NetObserv).
    **Phase C — your governance + AI/Virt** (Pipelines + GitOps + Virtualization + DR). Mold Shop running (Pipelines for CI; GitOps for CD); Special Castings Wing alive (KubeVirt VMs migrated from VMware via MTV alongside containers); DR plan (OADP + etcd backup) rehearsed; disconnected update procedure documented.
    **Phase D — your federation + defence** (RHACM + drill). Multi-Foundry Network ties tenant clusters together (RHACM hub + ManagedClusters + PolicySet + ApplicationSet + ObservabilityAddon); senior gardener walks your foundry, runs an unannounced drill (node kill, RBAC revoke, CTD finding, DR restore, etcd quorum loss). *Survive the drill, you graduate.*

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| Phase A — base foundry | IPI + EUS + private + OVN-K + 3+5 nodes + ODF storage nodes |
| Long-term lease | EUS channel |
| Phase B — services | ODF + SCCs + RHACS + Cluster Monitoring + Logging + Tracing + NetObserv |
| Inventory warehouse | ODF (Ceph + NooBaa) |
| Safety Office | SCCs + RHACS + Compliance Operator |
| Control Tower | Cluster Monitoring + Logging + Tracing + NetObserv |
| Phase C — apps + Virt + DR | Pipelines + GitOps + Virtualization (MTV) + OADP + disconnected mirror |
| Mold Shop | Pipelines (Tekton) + GitOps (Argo CD) |
| Special Castings Wing | OpenShift Virtualization (KubeVirt) + MTV migration |
| Disaster-Relief Vault | OADP + etcd backup + DR drill |
| Phase D — federation + drill | RHACM hub + ManagedClusters + PolicySet + ApplicationSet + must-gather pack |
| Multi-Foundry Network | RHACM federation |
| Live drill | Recover from chaos events using runbooks |
| Graduation diploma | K-OCP-complete: install configs + arch docs + DR runbook + AI/Virt runbook + must-gather pack + drill recording |

⚠️ *Analogy stops here:* A real Grand Opening is a one-time event; the K-OCP capstone's value is reusable artifacts (install configs, runbooks, drill scripts) so the next operator can graduate themselves.

## ELI5 / ELI10

**ELI5.** To graduate from K-Foundry you build a base foundry, stock it with shelves + safety + monitoring, set up the production lines + DR plan, then federate to other foundries. The senior gardener walks through and tries to break things; you fix them on the spot.

**ELI10.** K-OCP reference foundry: Phase A (IPI + EUS + private + OVN-K base). Phase B (ODF + SCCs + RHACS + Cluster Monitoring + Logging + Tracing). Phase C (Pipelines + GitOps + Virtualization with MTV + OADP + disconnected). Phase D (RHACM federation + live drill + must-gather pack). Deliverables: install configs + arch doc + DR runbook + AI/Virt runbook + must-gather pack + drill recording.

## Real-world scenarios

- **Bank — full reference foundry as platform standard.** A regulated bank adopts K-OCP reference foundry as the standard. IPI bare-metal install configs in git; per-cluster Markdown arch docs; defence + drill required before any new cluster goes prod. *Onboarding new clusters: 4 hours including drill, vs 6 weeks ad-hoc.*
- **VMware migration — 200 VMs to OCP Virtualization in 6 months.** Bank migrates 200 legacy VMs from vSphere to OCP via MTV. VMs run alongside containers under one RBAC, one observability, one DR. Phased migration: dev VMs first (1 month), staging VMs (2 months), prod VMs (3 months). *VMware contract not renewed; ~$2M annual savings.*
- **Multi-tenant SaaS — HCP per tenant via RHACM.** A SaaS gives each enterprise customer their own OCP cluster. RHACM Cluster Lifecycle provisions HCP clusters on signup; control planes pack densely on host clusters; data planes in customer accounts. ApplicationSet deploys baseline (RHACS Sensor, OADP, observability) per cluster. *Cluster-per-tenant operationalisable at SaaS scale.*
- **Live drill — etcd quorum loss recovered in 47 min.** During quarterly drill, reviewer simulates etcd quorum loss on a sibling cluster. Documented procedure: restore from latest etcd snapshot to one master; cluster operators reconcile; re-add other masters. *47 min total; auditor satisfied with RTO; runbook validated.*

## Common misconceptions

- **Myth:** "OCP gives me everything; I don't need to design."
  **Truth:** OCP gives a coherent platform. It does *not* design your network, your identity model, your tenant boundaries, your DR strategy, your egress posture, your SCC matrix, or your governance. The capstone exists because you still own those decisions — OCP frees you to focus on them.
- **Myth:** "I can copy the reference foundry from the internet and skip the defence."
  **Truth:** The defence + drill aren't bureaucracy — they're where you discover that the copied design doesn't match your network, your tenant model, your compliance, or your team's on-call topology. *The foundry you can defend is the only foundry you should run.*
- **Myth:** "DR drills are over-engineering."
  **Truth:** A startup can lose its company to a single 3 AM event. The drill cost (one engineer half-day per quarter) is a fraction of one outage. Even a basic OADP restore on a non-prod cluster surfaces the assumptions that would cost a week during a real incident.

## Recap

K-OCP Capstone built. Phase A (base) → Phase B (platform) → Phase C (apps + Virt + DR) → Phase D (RHACM + defended + drilled). The reference foundry is your starting template for any new prod OCP deployment.

**K-OCP curriculum complete.** You can architect, install, network, secure, manage Operators, build + ship workloads, store, operate, run VMs + AI + edge, federate multi-cluster, observe, troubleshoot, and defend a production OCP deployment end-to-end. Next paths: K-COM (deepen K8s itself) · K-VAN (operate K8s yourself, off-cloud) · K-EKS / K-AKS / K-GKE (managed-cloud counterparts) · or build internal training rolling K-OCP into your org's onboarding.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
