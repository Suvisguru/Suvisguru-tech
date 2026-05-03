# K-GKE G10 — G10 · Capstone — Regional Autopilot Reference Garden with AI Inference

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G10 · Capstone Garden
> Companion preview: `/preview-kubernetes-gke-lesson-10.html`.

---

**🎯 If you remember nothing else:** **Build the four-phase stack: Phase A (regional Autopilot + Cilium + Stable channel + private + WIF), Phase B (Multi-Cluster Gateway + WIF + storage + GMP + AMG + SLO), Phase C (BinAuth + Policy Controller + Config Sync + Backup + AI Inference Gateway + vLLM), Phase D (peer review + live DR drill). Defend it.**

## 1. Phase A — regional Autopilot, Cilium, private, Stable channel

**Goal:** a defendable base cluster with no public attack surface, modern networking, multi-zone resilience, predictable upgrades.
    
      - **Regional Autopilot** — Google manages nodes; per-Pod billing; Pod-level SLA; admission webhooks enforce safety baseline. Regional control plane = 3-zone HA. *Default for new prod K-GKE clusters.*

      - **Stable release channel** — conservative upgrade cadence; predictable; SLA on supported versions. Set maintenance window Tue 02-06 UTC; document maintenance exclusion calendar.

      - **Private cluster + master authorized networks** — apiserver public endpoint restricted to corp VPN egress IPs (or fully private + Connect Gateway).

      - **VPC-native + GKE Dataplane V2 (Cilium)** — Pod IPs from oversized secondary range (planned for 5× current scale); eBPF dataplane; NetworkPolicy default-deny per namespace.

      - **Cloud NAT** for egress with FQDN-allow-list firewall for outbound (Stripe, GitHub, internal APIs).

      - **Workload Identity Federation** enabled at cluster create. OIDC issuer URL captured in cluster-config repo.

    
    *Phase A success criterion:* cluster created via Terraform; `kubectl` works only via Connect Gateway / IAM-authenticated kubeconfig; no public IPs in cluster's GCE-managed-instance-group; Pod IP secondary range usage < 20%.

## 2. Phase B — Multi-Cluster Gateway, identity, storage, observability

**Multi-cluster networking**:
    
      - **Three regional Autopilot clusters** registered into a Fleet (us-central1, europe-west4, asia-southeast1).

      - **Multi-Cluster Gateway (MCG)** via Gateway API — single global anycast IP routes to nearest healthy cluster.

      - HTTPRoutes + per-cluster backend Services with NEG-based container-native LB.

      - Failure of one cluster: traffic routes to remaining clusters; DNS-side failover not needed.

    
    **Identity**:
    
      - **Workload Identity Federation for GKE** per workload — narrow G-SAs scoped to specific resources.

      - Local accounts disabled; IAM Conditions + just-in-time access via PIM-style elevation.

      - Connect Gateway for break-glass kubectl access.

    
    **Storage**:
    
      - Default StorageClass = pd-balanced with WaitForFirstConsumer; Hyperdisk Balanced + Storage Pools for sustained-IOPS workloads.

      - Regional PD for cross-zone-attach stateful workloads; VolumeAttributesClass for live IOPS retier.

      - Filestore Enterprise for RWX needs; GCS FUSE for ML datasets; Parallelstore for distributed training I/O.

      - Secret Manager CSI for keyless secrets; auto-rotation enabled.

    
    **Observability**:
    
      - Cloud Logging + Cloud Monitoring (auto); GMP enabled for app metrics; managed Grafana joining all data sources.

      - Apiserver / scheduler / controller-manager metrics + audit logs to Cloud Logging (--monitoring=… and --logging=… flags).

      - Cloud Trace + Cloud Profiler enabled.

      - **Service Monitoring** defines per-service SLOs; burn-rate alerts route to Pub/Sub → PagerDuty / Teams.

    
    *Phase B success criterion:* sample app deploys via Terraform / Config Sync; pulls a Secret Manager secret via WIF; serves traffic through Multi-Cluster Gateway; appears in AMG with RED panels and a burn-rate alert.

## 3. Phase C — Binary Auth, Policy Controller, Config Sync, Backup for GKE, AI inference

**Security + admission**:
    
      - **Binary Authorization** in *enforce* mode: only images with attestation from the scan-then-sign pipeline (Artifact Registry scan → KMS-signed attestation) may run.

      - **Policy Controller** (managed Gatekeeper) fleet-wide: Restricted PSA baseline, registry allowlist (only images.gcr.io/our-org/*), label requirements, NetworkPolicy presence checks.

      - **Container Threat Detection (in SCC)** + **Security Posture** dashboard for runtime + posture findings.

      - **Confidential GKE Nodes** (Compute Class with N2D AMD SEV-SNP) for the PHI-handling workload.

      - **CMEK** across PD / Secret Manager / Artifact Registry; rotated on Cloud KMS schedule.

    
    **GitOps**:
    
      - **Config Sync** with three repos: *cluster-config* (Fleet-level), *platform* (Container Insights config, MCG, MI/role assignments), *workloads* (per-tenant or per-team).

      - RootSync + RepoSync per cluster; drift detection on; manual edits reverted by reconcile loop.

    
    **DR**:
    
      - **Backup for GKE**: nightly cluster-wide manifests + PV snapshots; cross-region replication via paired backup region.

      - RTO target 60 min for full cluster restore; RPO 24h.

      - *Tested quarterly* via blue-green cluster restore drill.

    
    **AI inference workload (the showcase)**:
    
      - **GKE Inference Gateway** with KV-cache aware routing.

      - **vLLM** Pods serving Llama 3 70B on Compute Class Accelerator (A4 H200).

      - Kueue queues for batch fine-tuning jobs; JobSet for multi-host TPU training.

      - SLO: p95 first-token-latency < 500ms; cost-per-token tracked via BQ + Service Monitoring.

    
    *Phase C success criterion:* three pull requests can change cluster behaviour; one pen-test exercise passes Defender + admission policies; DR drill restores within RTO; inference workload meets SLO at peak.

## 4. Phase D — defend, drill, deliver

You don't finish K-GKE by handing in Terraform. You finish by **defending it** in front of a peer panel and surviving a **live drill**.
    **Architecture defence** (60 minutes, with senior platform reviewer):
    
      - Walk the network diagram — VPC, subnets, secondary ranges, MCG, Cloud NAT, Private endpoints.

      - Walk the identity diagram — WIF Pool + federated credentials + G-SAs per workload + IAM scope; break-glass IAM + PIM.

      - Walk the storage diagram — StorageClass defaults, Regional PD usage, snapshot + Backup for GKE policy.

      - Walk the observability diagram — three pipes into AMG, SLOs + burn-rate alerts, on-call playbook.

      - Walk the upgrade runbook — Stable channel, maintenance window, exclusions, blue-green node-pool fallback.

      - Walk the DR runbook — Backup for GKE schedule, restore steps, RTO/RPO targets, drill cadence.

      - Walk the AI inference runbook — Inference Gateway routing, vLLM Pod sizing, model cache strategy, SLO + cost per token.

    
    **Live drill** (90 minutes):
    
      - Reviewer kills a node. Cluster Autoscaler / Autopilot replaces; workloads re-schedule; AMG dashboards stay green.

      - Reviewer revokes a G-SA IAM role. Pod throws 401; Logs Explorer + Audit Logs locate the change; fix and re-run within 15 min.

      - Reviewer applies a high-severity Container Threat Detection finding. You walk the response: alert → triage → remediation → admission policy hardening.

      - Reviewer initiates a DR scenario: restore last night's Backup for GKE backup into a sibling cluster; verify workloads come up; document deltas.

      - Reviewer simulates a 10× LLM inference burst. Inference Gateway routes intelligently; vLLM scales (HPA + Compute Class autoprovisions GPU); SLO holds; cost-per-token logged.

    
    *K-GKE-complete*: Terraform + per-cluster Markdown architecture doc + DR runbook + AI inference runbook + live-drill recording. *You can hand this to a successor and they can run it.*

## Before / After

**Before.** Pre-K-GKE-curriculum operators built GKE clusters one feature at a time, learning each surface only when it failed. Six months in: a half-Modern, half-Legacy cluster with mixed identity (some service principal, some WIF), bring-your-own observability, no Defender / posture findings, an Ingress controller installed by Helm, no GitOps, no DR drill, no upgrade plan, no Inference Gateway. *Tribal knowledge in three engineers' heads.*

**After.** The K-GKE reference garden is **defendable**: every choice is justified, every alternative considered, every failure mode mapped to a runbook. *Regional Autopilot + Cilium + Stable channel + private + WIF* for base; *MCG + WIF + storage + GMP/AMG/SLO* for platform; *BinAuth + Policy Controller + Config Sync + Backup + AI Inference Gateway + vLLM* for ops; *defence + drill* for confidence. A new operator can read the architecture doc, run the runbook, and operate the garden.

*You can't cargo-cult a reference garden from the internet — you have to walk every choice yourself. K-GKE Capstone is that walk, defended.*

## Analogy — the K-Garden plot

The **Harvest Festival** is K-Garden's graduation event. Today you're the candidate. Four phases of the ceremony.
    **Phase A — your base plot** (regional Autopilot). You designed and built it: regional 3-zone control plane, Cilium runners delivering messages, private cluster, Stable Almanac for predictable seasons, sealed worker permits via WIF.
    **Phase B — your services** (platform). Multi-Garden Concierge (MCG) routes visitors to the nearest healthy garden. Sealed worker permits per worker (WIF + G-SAs scoped narrowly). Library reservoir (storage) configured. Watchtower (observability) staffed; SLO scribe defines the contracts.
    **Phase C — your governance + AI lab**. Inspection Bench (Binary Auth) refuses unattested packages. Door rules (Policy Controller) enforced fleet-wide. Daily Git reconciler (Config Sync) syncs the rule book. Disaster-Relief Vault (Backup for GKE) rehearsed. AI lab serves Llama 3 70B inference via the model-aware Concierge (Inference Gateway) + vLLM specialty inference rooms on A4 H200 plots.
    **Phase D — your defence**. The senior gardener walks your garden, asks questions, fires alarms — you respond from the runbooks. *If you survive an unannounced live drill, you graduate.*

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| Phase A — base plot | Regional Autopilot + Cilium + Stable + private + WIF |
| Multi-Garden Concierge | Multi-Cluster Gateway (MCG) |
| Sealed worker permit | Workload Identity Federation |
| Library reservoir | PD + Hyperdisk + Filestore + Backup for GKE |
| Watchtower bell + SLO scribe | GMP + AMG + Service Monitoring + burn-rate alerts |
| Inspection Bench | Binary Authorization |
| Door rules fleet-wide | Policy Controller + Config Sync |
| Disaster-Relief Vault | Backup for GKE |
| Model-aware Concierge | GKE Inference Gateway with KV-cache routing |
| Specialty inference rooms | vLLM Pods on Compute Class Accelerator (A4 H200) |
| Phase D — defence | Architecture review + live chaos drill |
| Survive the drill | Recover from chaos events using runbooks |
| Graduation diploma | K-GKE-complete: Terraform + arch doc + DR runbook + AI runbook + drill recording |

⚠️ *Analogy stops here:* A real festival is a one-time ceremony; the K-GKE capstone's value is that the artifacts (Terraform, runbooks, drill scripts) are reusable next time around — and the next operator can graduate themselves.

## ELI5 / ELI10

**ELI5.** To graduate from K-Garden you build a small base plot, hire your services, set up your governance and AI lab, then the senior gardener walks through and tries to break things. You fix them on the spot using the runbooks. Then you graduate.

**ELI10.** The K-GKE reference garden: Phase A (Regional Autopilot + Cilium + Stable channel + private + WIF). Phase B (Multi-Cluster Gateway + WIF + storage + GMP + AMG + SLO Monitoring). Phase C (Binary Auth + Policy Controller + Config Sync + Backup for GKE + Inference Gateway + vLLM). Phase D (architecture defence + live chaos drill: node kill, IAM revoke, CTD finding, DR restore, 10× inference burst). Deliverables: Terraform + arch doc + DR runbook + AI runbook + drill recording.

## Real-world scenarios

- **SaaS — full reference garden as the new platform-team standard.** A SaaS adopts K-GKE reference garden as the standard for all new prod GKE deployments. Terraform modules version-pinned in a shared repo. Per-tenant garden shapes only diverge on size + region. Defence + drill required before any new garden goes prod. *Onboarding new clusters: 4 hours including drill, vs 6 weeks ad-hoc previously.*
- **ML platform — Inference Gateway + vLLM at 10K req/sec.** ML platform serves Llama 3 70B at 10K req/sec across three regional Autopilot clusters via MCG. Inference Gateway routes by KV-cache locality + prompt size. vLLM Pods on Compute Class Accelerator A4 H200; Kueue queues for batch fine-tuning. SLO p95 latency 480ms; cost-per-token tracked. *10K req/sec at 60% lower cost vs naive routing.*
- **Bank — DR drill quarterly restored cluster in 42 min.** Bank schedules nightly Backup for GKE backups, cross-region. Quarterly DR drill: spin up empty regional Autopilot in DR region; restore from latest backup; verify workloads. Last drill: restoration completed in 42 min; auditor approved RTO target of < 60 min. *DR is rehearsed muscle, not a hopeful plan.*
- **Live drill — IAM revocation diagnosed and fixed in 11 min.** During quarterly drill, reviewer revokes a G-SA Storage Object Viewer role. Pod throws 401. AMG dashboard fires red within seconds. On-call opens Logs Explorer with the saved query for IAM audit; finds the IAM change in Audit Logs; restores via gcloud command; Pod recovers within 11 min. *Total elapsed: under 15 min from page to resolution; runbook validated.*

## Common misconceptions

- **Myth:** "Autopilot gives me everything; I don't need to design."
  **Truth:** Autopilot gives you a coherent default. It does *not* design your VPC, your identity model, your DR strategy, your egress posture, your AI inference architecture, or your governance. The capstone exists because you still own those decisions — Autopilot frees you to focus on them.
- **Myth:** "I can copy the reference garden from the internet and skip the defence."
  **Truth:** The defence + drill aren't bureaucracy — they're where you discover that the copied design doesn't match your VPC, your tenant model, your compliance, or your team's on-call topology. *The garden you can defend is the only garden you should run.*
- **Myth:** "DR drills are over-engineering for a startup."
  **Truth:** A startup can lose its company to a single 3 AM data event. The drill cost (one engineer half a day per quarter) is a fraction of one outage. Even a basic Backup for GKE restore of a non-prod cluster, executed once, surfaces the assumptions that would cost a week during a real incident.

## Recap

K-GKE Capstone built. Phase A (base) → Phase B (platform) → Phase C (ops + AI) → Phase D (defended + drilled). The reference garden is your starting template for any new prod GKE deployment — adapt; don't reinvent.

**K-GKE curriculum complete.** You can architect, version, network, identity-secure, store, scale, observe, federate, troubleshoot, and defend a production GKE deployment with AI inference end-to-end. Next paths: K-COM (deepen K8s itself) · K-VAN (operate K8s yourself, off-cloud) · K-EKS (the AWS counterpart) · K-AKS (the Azure counterpart) · or build internal training rolling K-GKE into your org's onboarding.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
