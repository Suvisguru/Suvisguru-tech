# K-AKS A11 — A11 · Capstone — Private AKS Automatic Reference Campus with Everything

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A11 · Capstone Campus
> Companion preview: `/preview-kubernetes-aks-lesson-11.html`.

---

**🎯 If you remember nothing else:** **Build the four-phase stack: Phase A (private AKS Automatic + Cilium + NAP + LTS), Phase B (WI + AGC + storage + observability), Phase C (Defender + Policy + Flux + Velero + blue-green runbook), Phase D (peer review + live DR drill). Defend it.**

## 1. Phase A — private AKS Automatic on Premium tier

**Goal:** a defendable base cluster with no public attack surface, modern networking, and an upgrade path measured in years.
    
      - **AKS Automatic** on **Premium tier** — preconfigures Container Insights, AMP, AMG, Workload Identity, Azure RBAC for K8s, NAP, KEDA, VPA, image cleaner, auto-upgrade, Cilium NetworkPolicy. Premium tier enables LTS subscription.

      - **Private cluster** via **API Server VNet Integration** — apiserver is in your hub VNet; no public endpoint. Authorized IP ranges as belt-and-braces if the org policy demands.

      - **Azure CNI Powered by Cilium** in Overlay mode — Pods on overlay CIDR; nodes in VNet; eBPF dataplane; L4 + L7 NetworkPolicy + Hubble flow visibility.

      - **Node Auto Provisioning (NAP)** for compute — Azure picks SKU + zones; auto-consolidation; one less ops burden.

      - **NAT Gateway** for outbound — no LB-shared SNAT; predictable scaling; multi-IP for SNAT capacity.

      - **Multi-AZ** — pool zones {1,2,3}; Pod topology-spread constraints for even distribution.

    
    *Phase A success criterion:* cluster created via Bicep / Terraform; `kubectl` works only via Entra-integrated kubeconfig; no public IPs in MC_*.

## 2. Phase B — identity, ingress, storage, observability

**Identity**: **Workload Identity** wired per workload (no long-lived secrets). User-assigned MIs scoped narrowly per service. **Azure RBAC for K8s** with *local accounts disabled*. Break-glass Entra group with PIM. Conditional Access requiring MFA + compliant device.
    **Ingress**: **Application Gateway for Containers (AGC)** in private mode + Gateway API. HTTPRoutes managed by service teams; default-deny ingress NetworkPolicy.
    **Storage**: Premium SSD v2 default StorageClass with `WaitForFirstConsumer`; Azure Files CSI for RWX shared logs / assets; **Secrets Store CSI** with Azure Key Vault provider, WI-authenticated, rotation-poller enabled.
    **Observability**: **Container Insights** (AKS-aware metrics+logs into Log Analytics) + **AMP** (managed Prometheus, scrape per service) + **AMG** (managed Grafana, RED dashboards per service joining AMP + Container Insights + App Insights). Apiserver + audit + audit-admin diagnostic settings → Log Analytics. Action Group → PagerDuty.
    *Phase B success criterion:* a sample app deploys via kubectl; pulls a Key Vault secret via WI; serves traffic through AGC; appears in AMG with RED panels and an alert rule.

## 3. Phase C — Defender, Policy, GitOps, Velero, LTS runbook

**Security**: **Microsoft Defender for Containers** (image scan + posture + runtime). **Azure Policy for AKS** with the *restricted* baseline. **PSA Restricted** per namespace. **Image Cleaner** on critical-severity threshold. **Azure Firewall** egress with FQDN allow-list. Cosign / Notation signing on critical images; admission verifier blocks unsigned.
    **GitOps**: **Flux v2 add-on**. Three repos: *cluster-config* (Flux's own seed), *platform* (Container Insights config, AGC, MI/role assignments), *workloads* (per-tenant or per-team apps). Drift detection on; manual interventions reverted by reconcile loop.
    **DR**: **Velero** (or Azure Backup for AKS) — daily cluster-wide backup to a geo-redundant Storage Account. RTO target 60 min for full cluster restore; RPO 24 hours. *Tested quarterly* via blue-green cluster restore drill.
    **Upgrade runbook**: **LTS** on the chosen minor (e.g. v1.30 LTS) for 2-year stability. Pre-flight with **kubent** + **Pluto** against git + cluster. Maintenance window Sundays 02-06 UTC. **Blue-green node pool migration** for high-stakes upgrades. Cluster blue-green held in reserve for major LTS-to-LTS jumps.
    *Phase C success criterion:* three pull requests can change cluster behaviour; one pen-test exercise passes Defender + admission policies; one DR drill restores within RTO.

## 4. Phase D — defend, drill, deliver

You don't finish K-AKS by handing in a Bicep file. You finish by **defending it** in front of a peer panel and surviving a **live drill**.
    **Architecture defence** (60 minutes, with senior platform reviewer):
    
      - Walk the network diagram — VNet, subnets, NSG, AGC, NAT Gateway, Private Endpoint to ACR + Key Vault.

      - Walk the identity diagram — Entra app + MI per workload + federated credentials, break-glass Entra group + PIM.

      - Walk the storage diagram — StorageClass defaults, ZRS for stateful, snapshot policy.

      - Walk the observability diagram — three pipes into AMG, alert routing, on-call playbook.

      - Walk the upgrade runbook — LTS rationale, pre-flight, surge, blue-green fallback.

      - Walk the DR runbook — Velero schedule, restore steps, RTO/RPO targets, drill cadence.

    
    **Live drill** (90 minutes):
    
      - The reviewer kills a node. NAP replaces; workloads re-schedule; AMG dashboards stay green.

      - The reviewer revokes a Workload Identity MI role. Pod throws 401; KQL on AKS audit logs locates the change in Activity Log; fix and re-run within 15 min.

      - The reviewer applies a high-severity Defender finding. You walk the response: Defender alert → triage → remediation → admission policy hardening.

      - The reviewer initiates a DR scenario: restore last night's Velero backup into a sibling cluster; verify workloads come up; document deltas.

    
    *K-AKS-complete*: Bicep + per-cluster Markdown architecture doc + DR runbook + live-drill recording. *You can hand this to a successor and they can run it.*

## Before / After

**Before.** Pre-K-AKS-curriculum operators built AKS clusters one feature at a time, learning each surface only when it failed. Six months in: a half-Modern, half-Legacy cluster with mixed identity (some service principal, some MI, some WI), bring-your-own observability stack, no Defender, an Ingress controller installed by Helm, no GitOps, no DR drill, no upgrade plan, no LTS. *Tribal knowledge in three engineers' heads.*

**After.** The K-AKS reference stack is **defendable**: every choice is justified, every alternative considered, every failure mode mapped to a runbook. *Private AKS Automatic + Cilium + NAP + LTS* for base; *WI + AGC + storage + observability* for platform; *Defender + Policy + Flux + Velero + blue-green* for ops; *defence + drill* for confidence. A new operator can read the architecture doc, run the runbook, and operate the cluster.

*You can't cargo-cult a reference stack from the internet — you have to walk every choice yourself. K-AKS Capstone is that walk, defended.*

## Analogy — the K-Campus wing

The **Commencement Hall** is where students graduate from K-Campus. Today you're the candidate. Four phases of the ceremony:
    **Phase A — your dorm building** (base cluster). You designed and built it: doors that lock the right way, plumbing that drains the right way, a back exit (NAT Gateway) sized for finals week. Foundation: solid.
    **Phase B — your services** (platform). You hired the registrar (Workload Identity), hired the front-desk concierge (AGC), built the library wing (storage), installed the bell tower (observability). Operations: humming.
    **Phase C — your governance** (security + GitOps + DR + upgrade). Campus Police on every shift, the daily Git reconciler running, the disaster-relief plan rehearsed, the long-term lease (LTS) signed. Resilience: rehearsed.
    **Phase D — your defence** (peer review + live drill). The senior dean walks your campus, asks questions, fires alarms — you respond from the runbooks. *If you survive an unannounced drill, you graduate.*

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| Phase A — dorm building | Private AKS Automatic + Cilium + NAP |
| Back exit sized for finals | NAT Gateway for outbound |
| Apiserver in your own basement | API Server VNet Integration |
| Phase B — services | WI + AGC + Storage + AMP/AMG/Container Insights |
| Concierge with preloaded manifest | AGC + Gateway API |
| Bell tower with three bells | Three signal pipes (metrics + logs + traces) → AMG |
| Phase C — governance | Defender + Policy + Flux + Velero + LTS |
| Daily Git reconciler | Flux v2 add-on (App-of-Apps style) |
| Disaster-relief plan | Velero / Backup for AKS + DR runbook |
| Long-term lease | LTS on Premium tier |
| Phase D — defence | Architecture review + live drill |
| Survive the dean's alarms | Recover from chaos events using runbooks |
| Graduation certificate | K-AKS-complete: Bicep + arch doc + DR runbook + drill recording |

⚠️ *Analogy stops here:* A real campus graduation is a one-time ceremony; the K-AKS capstone's value is that the artifacts (Bicep, runbooks, drill scripts) are reusable next time around — and the next operator can graduate themselves.

## ELI5 / ELI10

**ELI5.** To graduate from K-Campus you build a small dorm, hire your services, set up your governance, then the dean walks through and tries to break things. You fix them on the spot. If you can do all four, you're done.

**ELI10.** The K-AKS reference stack: Phase A (private AKS Automatic + Cilium + NAP + Premium tier with LTS). Phase B (Workload Identity + AGC + Disks/Files + Key Vault CSI + Container Insights + AMP + AMG). Phase C (Defender for Containers + Azure Policy Restricted + Flux v2 GitOps + Velero/Backup for AKS + blue-green upgrade runbook). Phase D (architecture defence + live chaos drill: node kill, MI revoke, Defender finding, DR restore). Deliverables: Bicep + arch doc + DR runbook + drill recording.

## Real-world scenarios

- **SaaS — full reference stack as the new platform-team standard.** A SaaS platform team adopts K-AKS reference stack as the standard for all new prod clusters. Bicep modules version-pinned in a shared repo. Per-tenant cluster shapes only diverge on size + region. Defence + drill required before any new cluster goes prod. *Onboarding new clusters: 4 hours including drill, vs 6 weeks ad-hoc previously.*
- **Bank — regulated workload on the LTS variant.** A bank's payments cluster: full K-AKS stack but pinned to v1.27 LTS for 9-month compliance change-control. AGC in private mode; Confidential Containers pool for one PII subsystem; Azure Firewall Premium with TLS inspection on egress. Quarterly DR drill includes a hypothetical Azure-region-failure scenario; cluster restored into paired region in 53 minutes. *Audit clean.*
- **Dev experience — Flux + GitHub Actions = instant new namespace.** A dev team spins up a new app: PR to *workloads/* repo with new Kustomization → Flux reconciles → AGC HTTPRoute provisioned → AMG dashboard auto-generated from Helm chart annotations → on-call rota updated via Action Group. *From PR merged to live: 8 minutes; no platform-team ticket.*
- **Live drill — cluster failure recovered inside RTO.** During the quarterly drill, the reviewer manually deletes the AGC resource. Within 90 seconds: Defender alert, AMG availability red, Flux reconcile detects drift, recreates AGC, HTTPRoutes re-attach, traffic resumes. Total outage: 4 minutes; runbook auto-pinged on-call but did not require human action. *The drill validates that GitOps + Flux is the recovery primitive, not just a deployment tool.*

## Common misconceptions

- **Myth:** "AKS Automatic gives me everything; I don't need to design."
  **Truth:** AKS Automatic gives you a coherent default. It does *not* design your VNet, your identity model, your DR strategy, your egress posture, or your governance. The capstone exists because you still own those decisions — Automatic frees you to focus on them.
- **Myth:** "I can copy the reference stack from the internet and skip the defence."
  **Truth:** The defence + drill aren't bureaucracy — they're where you discover that the copied stack doesn't match your VNet, your tenant model, your compliance, or your team's on-call topology. *The cluster you can defend is the only cluster you should run.*
- **Myth:** "DR drills are over-engineering for a startup."
  **Truth:** A startup can lose its company to a single 3 AM data event. The drill cost (one engineer half a day per quarter) is a fraction of one outage. Even a basic Velero restore of a non-prod cluster, executed once, surfaces the assumptions that would cost a week during a real incident.

## Recap

K-AKS Capstone built. Phase A (base) → Phase B (platform) → Phase C (ops) → Phase D (defended + drilled). The reference stack is your starting template for any new prod AKS cluster — adapt; don't reinvent.

**K-AKS curriculum complete.** You can architect, identity-secure, network, store, scale, harden, observe, extend, upgrade, troubleshoot, and defend a production AKS cluster end-to-end. Next paths: K-COM (deepen K8s itself) · K-VAN (operate K8s yourself, off-cloud) · K-EKS (the AWS counterpart) · or build internal training rolling K-AKS into your org's onboarding.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
