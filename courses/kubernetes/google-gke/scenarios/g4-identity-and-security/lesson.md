# K-GKE G4 — G4 · GKE Identity and Security

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G4 · Identity and Security
> Companion preview: `/preview-kubernetes-gke-lesson-04.html`.

---

**🎯 If you remember nothing else:** **Layered defence: Workload Identity Federation (no secrets in Pods); Binary Authorization (deploy-time signature/attestation); Policy Controller (admission); Security Posture + CTD (runtime); Confidential / Shielded / Sandbox nodes; CMEK end-to-end. Each layer matters.**

## 1. IAM + RBAC + Workload Identity Federation for GKE

GKE has two identity surfaces.
    
      - **Human → cluster:** GCP IAM authenticates; either GCP IAM (with the *Kubernetes Engine Developer/Admin/Viewer* roles) *or* K8s RBAC authorises (or both — additive). **IAM Conditions** let you scope grants ("allow read of cluster X only if request comes from the corp VPN range"). For audit + just-in-time access, use **IAM PAM** or short-lived role grants.

      - **Pod → GCP service:** **Workload Identity Federation for GKE** — the modern replacement for the older Workload Identity GKE Pool model. The cluster's OIDC issuer + a federated identity pool let K8s ServiceAccounts impersonate or directly authenticate as Google Service Accounts (or directly as principals via WIF principal binding). *Pods get short-lived GCP access tokens with no secret in cluster.*

    
    **Pattern:** annotate K8s SA → bind to G-SA → grant G-SA the IAM roles on target resources (Storage / BigQuery / Pub/Sub / Secret Manager). Pod uses the K8s SA; gcloud SDK in the Pod calls Workload Identity metadata server; gets short-lived G-SA token; calls GCP API normally.
    **Connect Gateway** (covered in G8) lets a human run kubectl against any registered fleet cluster via the GCP control plane — no need to expose individual cluster apiserver IPs to humans; auth flows through IAM.

## 2. Binary Authorization + Artifact Registry + Policy Controller + Config Sync

**Artifact Registry** = GCP's container + package registry. Features: *vulnerability scanning* (continuous CVE scan), *remote repos* (proxy upstream Docker Hub / GitHub Container Registry — protects against upstream blips), *virtual repos* (combine multiple sources behind one URL), *attestations* (signed metadata about images: "this image passed scan," "this image was built by trusted CI").
    **Binary Authorization** (BinAuth) = deploy-time signature / attestation enforcement. Configure a policy: "Pods in namespace X may only run images that have an attestation from Attestor Y." Pods that don't meet the policy are *rejected at admission*. Attestors are typically Google KMS-signed pipelines: "image passed Artifact Registry scan = sign attestation; image was built by trusted CI = sign attestation." *BinAuth + Artifact Registry scanning = supply-chain trust at deploy*.
    **Policy Controller** (managed OPA Gatekeeper) — fleet-wide admission policies. Built-in *Constraint templates* for common policies (require labels, restrict registries, block hostPath, etc.); custom policies via Rego or CEL. Effect: *Audit* (log) or *Enforce* (deny). Ships as part of GKE Enterprise.
    **Config Sync** — fleet-wide GitOps. `RootSync` + `RepoSync` reconcile manifests from Git into clusters. Use to deploy NetworkPolicies, RBAC, ConfigMaps, applications uniformly across the fleet. Drift detection on; manual overrides reverted.

## 3. Security Posture + Container Threat Detection + Secret Manager CSI

**GKE Security Posture dashboard** — continuously evaluates cluster + workloads against the GKE security baseline + CIS K8s Benchmark. Findings: "PSA not enforced in namespace X," "NetworkPolicy missing in namespace Y," "image with critical CVE running in production." Actionable; integrates with Security Command Center.
    **Container Threat Detection (CTD)** — part of **Security Command Center (SCC)**. Runtime threat detection on GKE nodes — watches for known malicious behaviours (suspicious shell-in-container, crypto-miner, lateral movement, K8s-specific TTPs). Alerts ship to SCC + Cloud Logging.
    **Secret Manager CSI driver** — mounts **Secret Manager** secrets as files in Pods. Authenticates via Workload Identity Federation; auto-rotation supported. *Cleaner than env-var Secrets*: file-based, watched by app for changes, no Secret-in-K8s with the rotation gap.
    **Pod Security Admission (PSA)** — same K8s-native PSA standard. Enforce *Restricted* per namespace as the production default. Combines with Policy Controller for custom rules beyond the PSA baseline.

## 4. Shielded nodes + Confidential GKE + GKE Sandbox + CMEK

**Shielded GKE Nodes** — Secure Boot + virtual TPM attestation. Default for new clusters. Catches rootkit injection at boot.
    **Confidential GKE Nodes** — memory encryption with attestation at the silicon level: **AMD SEV / SEV-SNP** (Confidential VMs on N2D / C2D) and **Intel TDX**. Per-Pod memory encrypted; even Google operators cannot read it. For regulated workloads (PII, financial, health, ML on sensitive data).
    **GKE Sandbox (gVisor)** — runs untrusted Pods inside a user-space kernel that intercepts syscalls. Stronger isolation than the default container runtime; performance trade-off (~5-15% on syscall-heavy workloads). For multi-tenant clusters running untrusted workloads (CI runners, customer-submitted code).
    **CMEK (Customer-Managed Encryption Keys)** — encrypt at rest with keys you control via Cloud KMS:
    
      - **Persistent Disks** — node OS disks + PVC disks encrypted with CMEK.

      - **etcd Secrets** — Application-layer Secrets encryption: K8s Secrets in etcd encrypted with CMEK before write.

      - **Artifact Registry images** — image storage encrypted with CMEK.

    
    Combine with **VPC Service Controls** for data-exfiltration boundaries.

## Before / After

**Before.** Pre-Workload-Identity-Federation, Pods used either node-SA tokens (over-broad) or downloaded G-SA JSON keys (long-lived, leak-prone). Binary Authorization existed but admission-only; no scan-then-attest pipeline integration. Container threat detection was bring-your-own. Confidential VMs existed but pre-K8s-aware. PSA was bring-your-own. Multi-cluster policy was scripts looping kubectl across contexts.

**After.** Modern GKE: **Workload Identity Federation** for keyless Pod auth. **Binary Authorization** + **Artifact Registry attestations** = scan-then-attest-then-deploy. **Security Posture** + **Container Threat Detection** in SCC = unified runtime security. **Confidential GKE Nodes** + **Shielded** + **Sandbox** + **CMEK** stack hardware-level guarantees. **Policy Controller + Config Sync** = fleet-wide policy + GitOps admission.

*Each layer is independently meaningful; together they're a coherent defendable security story.*

## Analogy — the K-Garden plot

The **Gatekeeper's Lodge** sits at the entrance to the K-Garden, with four shifts working different jobs.
    The **Identity Window** (IAM + WIF for GKE) checks every visitor and every robot worker. Visitors show their photo ID (IAM); robots present a sealed envelope (WIF for GKE federated credential) tied to their work-permit (G-SA). No worker carries a long-lived key — they fetch a fresh one for each task.
    The **Inspection Bench** (Binary Auth + Artifact Registry) inspects every package arriving at the loading dock. Each package must carry an attestation: "this package was scanned by the Inspector and was clean," "this package was built by the trusted Carpenter." Unattested packages are refused at the gate.
    The **Watchtower** (Security Posture + Container Threat Detection) is staffed all hours. The watchman has a checklist (Posture) of "are all gates locked, are NetworkPolicies set, are CVEs cleared?" and a binoculars (CTD) for "that worker is doing something suspicious — they're digging up someone else's plot."
    The **Building Crew** (Shielded / Confidential / Sandbox / CMEK) reinforces the buildings themselves. Some sheds are reinforced concrete (Shielded), some are vault-grade with silicon-level memory encryption (Confidential GKE — AMD SEV / Intel TDX), some are isolation cells for visiting workers whose intentions you don't fully trust (Sandbox / gVisor). Every storage room is locked with a key you control (CMEK).

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| Identity Window | GCP IAM + K8s RBAC + IAM Conditions |
| Worker sealed envelope | Workload Identity Federation for GKE |
| Worker work-permit (G-SA) | Google Service Account bound to K8s SA |
| Visitor photo ID | Human IAM principal |
| "Only allow ID checks from the corp VPN" | IAM Condition (request.attribute scope) |
| Inspection Bench | Binary Authorization |
| Package attestation | Artifact Registry attestation (KMS-signed) |
| "Where packages come from" | Artifact Registry remote / virtual repo |
| Door rules | Policy Controller (managed Gatekeeper) |
| Garden-wide rule book in Git | Config Sync (GitOps fleet-wide) |
| Watchman's checklist | GKE Security Posture dashboard |
| Watchman's binoculars | Container Threat Detection (in SCC) |
| Vault-grade memory-encrypted shed | Confidential GKE Node (AMD SEV / Intel TDX) |
| Reinforced shed | Shielded GKE Node (Secure Boot + vTPM) |
| Untrusted-worker isolation cell | GKE Sandbox (gVisor) |
| Storage room with your padlock | CMEK on disks / secrets / images |
| File-based key fetch from the locker | Secret Manager CSI driver |

⚠️ *Analogy stops here:* A real Gatekeeper inspects everything; in production, rate-limited inspection + sampling apply. Confidential GKE + Sandbox have measurable performance trade-offs (~5-15% syscall overhead on Sandbox; CPU + boot time on Confidential).

## ELI5 / ELI10

**ELI5.** The garden gate has four shifts. One checks IDs. One checks every package coming in. One has binoculars to spot bad behaviour. One reinforces the buildings themselves. Together they protect the garden.

**ELI10.** GKE security = four layers. **Identity:** IAM + RBAC + IAM Conditions for humans; Workload Identity Federation for GKE for Pods (no keys). **Supply chain + admission:** Binary Authorization for deploy-time signature/attestation; Artifact Registry scan + remote/virtual; Policy Controller (managed Gatekeeper); Config Sync for fleet-wide GitOps. **Runtime + posture:** Security Posture dashboard; Container Threat Detection (SCC); Secret Manager CSI; PSA Restricted. **Node + hardware:** Shielded nodes (default, Secure Boot + vTPM); Confidential GKE (AMD SEV / Intel TDX); GKE Sandbox (gVisor); CMEK on disks / secrets / images.

## Real-world scenarios

- **SaaS — WIF + Secret Manager CSI = no secrets in cluster.** A SaaS migrates from baked G-SA JSON keys to Workload Identity Federation. K8s SAs annotated; G-SAs scoped narrowly per workload; Secret Manager secrets mounted via Secret Manager CSI driver with WIF auth. *Zero long-lived secrets in cluster; zero key rotations to manage; per-Pod blast radius bounded by G-SA scope.*
- **Bank — Binary Authorization with attest-after-scan pipeline.** Bank pipeline: build → push to Artifact Registry → AR scan → if clean: KMS-signed attestation written → deploy. BinAuth policy: "only images with attestation from Attestor X may run." Unsigned + unattested images rejected at admission. *Compliance-clean supply chain; auditable from build to deploy.*
- **Healthcare — Confidential GKE Nodes for PHI training.** ML team trains models on patient data. Confidential GKE node pool (N2D AMD SEV-SNP) for PHI workloads. Memory encrypted at silicon level; Google operators cannot read RAM. External attestation report given to compliance auditor. *HIPAA-style requirements met without on-prem.*
- **CI runners — GKE Sandbox prevents CI escape.** A CI platform runs customer-submitted build jobs on GKE. Risk: malicious build escapes container, attacks node. Solution: dedicated node pool with GKE Sandbox (gVisor) — every CI Pod runs in user-space kernel; syscalls mediated. Even a privileged escape stays contained. *Performance ~10% slower on syscall-heavy builds; acceptable cost for the isolation.*

## Common misconceptions

- **Myth:** "Binary Authorization is admission control. So is PSA. Same thing."
  **Truth:** Different concerns. **PSA** = K8s-native pod-security baseline (no root, no privilege escalation, no hostPath). **Binary Authorization** = deploy-time enforcement of *which images may run* (signature / attestation). Combine: PSA enforces what the Pod can do; BinAuth enforces what image is allowed in the first place. Plus Policy Controller for arbitrary admission policies on top.
- **Myth:** "Workload Identity GKE Pool is the new way to do Pod-to-GCP auth."
  **Truth:** **Workload Identity Federation for GKE** is the current modern path (the federation-based model). The older *Workload Identity GKE Pool* approach still works in many clusters but the recommended pattern for new clusters is WIF for GKE — uses GCP's Workload Identity Federation infrastructure, supports more flexible binding patterns (direct principal, impersonation), aligns with the broader GCP WIF story.
- **Myth:** "Shielded nodes and Confidential GKE Nodes are the same."
  **Truth:** **Shielded** = Secure Boot + virtual TPM attestation (boot-time integrity). *Default for new clusters; no perf cost.* **Confidential GKE Nodes** = AMD SEV / Intel TDX silicon memory encryption (data-in-use). *Specific SKUs (N2D / C2D etc.); has CPU and boot-time cost.* Different threat models; complementary.

## Recap

Four security shifts: identity (IAM + RBAC + WIF for GKE), supply chain + admission (BinAuth + AR + Policy Controller + Config Sync), runtime + posture (Posture + CTD + Secret Manager CSI), node + hardware (Shielded + Confidential + Sandbox + CMEK).

**Next — G5: GKE Storage.** Persistent Disk CSI (pd-balanced, pd-ssd, Hyperdisk + Storage Pools), Filestore CSI (RWX), GCS FUSE CSI, Parallelstore CSI (HPC/AI), Backup for GKE, snapshots, expansion, VolumeAttributesClass with Hyperdisk.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
