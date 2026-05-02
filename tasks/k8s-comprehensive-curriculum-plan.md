# K-COM Comprehensive Curriculum — Plan for L18 onwards

> **Status:** active. Started 2026-05-02. Lessons 01–17 + L7.5 already shipped.
> Founder asked to cover the full 17-module syllabus. This document is the
> running plan for L18 → L44 produced in prerequisite order.

## Existing lessons (already shipped)

| # | Title | District |
|---|---|---|
| 01 | What is Kubernetes? | Mayor's Office |
| 02 | VMs vs Containers | Residential District |
| 03 | Cloud-Native Principles | Climate Control Tower |
| 04 | 12-Factor + Microservices vs Monoliths | Port + Restaurant Row |
| 05 | When K8s Fits / Overkill | Industrial Kitchen Block |
| 06 | GitOps · Platform Eng · SRE · Multi-Tenancy | Public Library |
| 07 | History · CNCF · Releases · KEPs | K-Town Rail Yard |
| 7.5 | How a Linux Computer Works (primer) | Foundation Tour |
| 08 | Linux Namespaces · cgroups · Capabilities | Office Tower w/ Utility Meters |
| 09 | Container Runtimes & OCI | Customs Warehouse |
| 10 | Image Building · Multi-stage · Distroless | Bakery District |
| 11 | Container Security & Registries | Bank Vault Quarter |
| 12 | PID 1 & Container Lifecycle | K-Town Harbour |
| 13 | Cluster Architecture | K-Town International Airport |
| 14 | The K8s API & YAML | City Hall — Permit Office |
| 15 | Pods Deep Dive | Co-Living Quarter |
| 16 | Workload Controllers | K-Town Dispatch Office |
| 17 | Services & Networking | K-Town Switchboard |

## Planned lessons (L18 → L44)

Districts: deep-dive lessons reuse the most-related existing district unless
the topic genuinely needs its own (those are explicitly noted as **NEW**).

### Phase 1 — Stateful & operational foundations (immediate gaps)

| # | Title | District |
|---|---|---|
| 18 | Storage Part 1 — PV, PVC, StorageClass | Customs Warehouse |
| 19 | Storage Part 2 — CSI, Snapshots, VolumeAttributesClass | Customs Warehouse |
| 20 | Configuration & Secrets — ConfigMap, Secret, KMS, ESO | Permit Office |
| 21 | ServiceAccounts & Certificates — tokens, cert-manager, PKI | Permit Office |
| 22 | Scheduling Part 1 — affinity, taints, topology spread | Dispatch Office |
| 23 | Scheduling Part 2 — priority, DRA, NUMA, GPUs | Dispatch Office |

### Phase 2 — Networking depth (extends L17)

| # | Title | District |
|---|---|---|
| 24 | Networking Foundations — Linux primitives, CNI, MTU | Switchboard |
| 25 | Gateway API — full coverage + Ingress NGINX retirement migration | Switchboard |
| 26 | AdminNetworkPolicy & FQDN policies | Switchboard |

### Phase 3 — Security

| # | Title | District |
|---|---|---|
| 27 | RBAC & Authentication | **NEW: Watchtower** |
| 28 | Admission Control — ValidatingAdmissionPolicy, PSA | Watchtower |
| 29 | Policy Engines — Kyverno + OPA Gatekeeper | Watchtower |
| 30 | Supply Chain Security — Cosign, Sigstore, SLSA, SBOM | Bank Vault Quarter |
| 31 | Multi-Tenancy & Hardening | Watchtower |

### Phase 4 — Observability & Reliability

| # | Title | District |
|---|---|---|
| 32 | Observability Part 1 — Logs + Metrics | **NEW: Observatory** |
| 33 | Observability Part 2 — Tracing + eBPF + SLOs | Observatory |
| 34 | Autoscaling — HPA, VPA, KEDA, Cluster Autoscaler | **NEW: Power Station** |
| 35 | Reliability & HA — PDB, multi-zone, regional DR | Power Station |

### Phase 5 — Application Delivery

| # | Title | District |
|---|---|---|
| 36 | Kustomize | **NEW: Print Shop** |
| 37 | Helm 3 — charts, hooks, OCI, signing | Print Shop |
| 38 | GitOps with Argo CD | Public Library |
| 39 | GitOps with Flux CD | Public Library |
| 40 | Progressive Delivery — Argo Rollouts, Flagger | Print Shop |

### Phase 6 — Advanced

| # | Title | District |
|---|---|---|
| 41 | CRDs Deep Dive — schemas, CEL, conversion webhooks | Permit Office |
| 42 | Operators with Kubebuilder — controller-runtime, OLM | **NEW: Workshop** |
| 43 | Service Mesh — Istio ambient, Linkerd, Cilium Mesh | Switchboard |

### Phase 7 — Capstone

| # | Title | District |
|---|---|---|
| 44 | Troubleshooting Methodology + Drills | **NEW: Detective's Office** |

## New K-Town districts to add (when needed)

Will add as Phase 3 / Phase 4 / Phase 5 / Phase 6 / Phase 7 begin:

- **Watchtower** (security cluster-side — RBAC, admission, hardening)
- **Observatory** (observability — logs, metrics, traces, eBPF)
- **Power Station** (autoscaling, reliability — power scales with demand, redundancy)
- **Print Shop** (application delivery — Helm charts as blueprints, releases as printed editions)
- **Workshop** (CRDs/Operators — custom builds, custom assistants)
- **Detective's Office** (troubleshooting — investigation methodology)

Each gets a DECISIONS.md entry when added, plus a STYLE.md row in the
district table, plus K-Town map pin.

## Concept rail growth

Each new lesson's concept rail extends the previous list. Existing lessons
(L01-L17) continue to show 18 items; new lessons show all items up to
themselves + future lessons as `○`. Long-term we may want a module-level
collapsed rail; for now, the linear list is acceptable.

## K-Town dot-strip

Currently 18 dots. Grows by 1 per new lesson. New lessons include all 18+
dots; existing lessons keep their 18.

## Build pipeline

After each batch of new lessons:
1. Run `python3 scripts/build_combined_course.py` (after extending its
   `LESSONS` list).
2. Re-zip the package via the same command used in earlier turns.

## Resume points for future Claude Code sessions

If a session ends mid-batch:
- Check the most recent commit on `main` for the last lesson shipped.
- Continue from the next planned lesson in this document.
- Each lesson follows the same structure as L16 / L17 (the most recent
  reference implementations). Use those as the template.
- Per-lesson copy isn't pre-drafted — produced fresh per QUALITY.md
  drafting protocol (≥3 drafts → critique → winner → save discards in
  `notes/k8s-revision-drafts.md`). For speed, drafts can be generated
  internally without per-lesson approval pauses, but the protocol applies.
