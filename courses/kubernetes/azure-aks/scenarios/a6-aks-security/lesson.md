# K-AKS A6 — A6 · AKS Security (Defender, Policy, Image Cleaner, FIPS, Confidential Containers)

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A6 · AKS Security
> Companion preview: `/preview-kubernetes-aks-lesson-06.html`.

---

**🎯 If you remember nothing else:** **Defence in depth: Defender (image scan + posture + runtime) + Azure Policy (Gatekeeper admission) + PSA Restricted + NetworkPolicy default-deny + Workload Identity (no secrets) + Azure Firewall egress. Move from Azure Linux 2 to AL3 or Ubuntu 24 before March 2026.**

## 1. Defender for Containers + ACR scanning

**Microsoft Defender for Containers** is Azure's K8s security plan with three pillars:
    
      - **Image scanning** — every push to ACR triggers a CVE scan; findings appear in Defender + the ACR portal. *Continuous re-scan* as new CVEs are published — an image "clean" yesterday can be "vulnerable" today.

      - **Posture management** — Defender continuously evaluates the cluster against the CIS Kubernetes Benchmark + Azure security baseline. Findings: "PSA not enforced in namespace X", "NetworkPolicy missing in namespace Y", "insecure runtime config Z". Actionable recommendations in the Defender portal.

      - **Runtime threat detection** — Defender agents on each node watch for known malicious behaviours (suspicious shell-in-container, crypto-miner, lateral movement, Kubernetes-specific TTPs). Alerts ship to Sentinel.

    
    **ACR (Azure Container Registry):**
    
      - **Geo-replication** — replicate the registry across regions; Pods pull from the nearest replica.

      - **Content trust / image signing** — sign images with Notation or Cosign; verify signatures via admission policy (e.g. Azure Policy + Notation Verifier or Kyverno).

      - **Private ACR** — disable public endpoint, expose via Private Link, attach Private DNS.

## 2. Azure Policy + PSA + Image Cleaner — admission and posture

**Azure Policy for AKS** = Microsoft's implementation of **OPA Gatekeeper** packaged as an AKS add-on. Built-in initiative *"Kubernetes cluster pod security baseline / restricted standards"* ships hundreds of admission policies. *Effect choice*: Audit (log only) or Deny (block at admission). Custom Constraints / ConstraintTemplates supported.
    **Pod Security Admission (PSA)** — K8s's built-in replacement for PodSecurityPolicy. Three levels: *Privileged / Baseline / Restricted*. Apply via namespace labels: `pod-security.kubernetes.io/enforce: restricted`. Restricted is production default — runs as non-root, no privileged escalation, drops all capabilities, seccomp RuntimeDefault.
    **Image Cleaner for AKS** — DaemonSet that scans node disks for unused or vulnerable images and removes them. *Reduces lateral movement risk* (an attacker landing on a node can't use a stale vulnerable image to pivot). Configure scan schedule + CVE severity threshold.
    **NetworkPolicy default-deny** per namespace + explicit allow lists per service is the standard hardening posture (covered in A3).

## 3. Runtime + Workload Identity + Azure Firewall

**Workload Identity** (covered in A2) is the security baseline for Pod auth — *no long-lived secrets in cluster*. Combined with managed identities scoped narrowly (least privilege per workload), the blast radius of a compromised Pod is bounded by what its MI can do.
    **Azure Firewall** (or **Azure Firewall Premium** for IDPS + TLS inspection) sits between the cluster's VNet and the internet. *Egress filtering*: an FQDN allow-list of permitted destinations (Microsoft Graph, ACR, Key Vault, your own APIs); everything else denied. Catches data exfiltration attempts at the network layer. Pair with NetworkPolicy for in-cluster east-west.
    **CloudTrail equivalent**: **Azure Activity Log** + **Defender alerts** + **Diagnostic Settings → Log Analytics**. Every `az aks ...` change is in Activity Log; every kubectl-as-Entra-principal call is in apiserver audit logs (turn on diagnostic settings to forward to Log Analytics).
    **Private cluster + private ACR + private Key Vault** = no public endpoints across the cluster's adjacent surface. Combined with Conditional Access on the management plane, this is the modern "locked-down enterprise AKS" topology.

## 4. Node OS + hardware — FIPS, Confidential, Trusted Launch, AL2→AL3

**FIPS node pools** — node OS configured for FIPS 140-2 cryptography (SHA-256+, AES-256, etc.). Required for some US federal compliance contexts. Per-pool flag at create time.
    **Host encryption** — encrypts node OS + temp disks with platform-managed or customer-managed (CMK via Key Vault HSM) keys. On by default for new clusters; verify on existing.
    **Trusted Launch VMs** — secure boot + virtual TPM (vTPM) attestation. Default for new node pools on supported SKUs. Catches rootkit injection at boot.
    **Confidential Containers** — Kata Containers runtime + AMD SEV-SNP. Each Pod runs in a hardware-encrypted utility VM with attestation. *Memory encrypted at the silicon level — even Azure host operators can't read it.* For regulated workloads (PII / financial / health).
    **Node OS migration — Azure Linux 2 → AL3 / Ubuntu 24:** *Azure Linux 2.0 reached end of support 2025-11-30; node images are removed from 2026-03-31.* Every AKS node currently on AL2 must migrate. Pick path: **Azure Linux 3** (Microsoft's newer optimised distro; same family) or **Ubuntu 24** (broader ecosystem, broader 3rd-party agent support). Migration = create new pool with target OS SKU, drain workloads from old pool, delete old pool. Cannot change OS SKU in place.

## Before / After

**Before.** Pre-Defender AKS = patchwork. CVE scans by self-installed Trivy or Anchore. PodSecurityPolicy was the admission tool — deprecated 2021. Image Cleaner didn't exist; nodes accumulated vulnerable images for months. NetworkPolicy installation was bring-your-own. Egress filtering = open. *Three different scanners, two different audit log destinations, zero correlation.* Plus Azure Linux didn't exist; Ubuntu 18 was reaching EOL with no managed migration story.

**After.** Modern AKS ships **Defender for Containers** (image + posture + runtime, single pane), **Azure Policy for AKS** (Gatekeeper admission with built-in baseline), **Image Cleaner**, **PSA Restricted** as the production default, **Workload Identity** (no cluster secrets), **Azure Firewall** for egress, **FIPS / Confidential Containers / Trusted Launch** for hardware-level guarantees. Plus **Azure Linux 3** as the optimised, well-maintained node OS path forward.

*Security in AKS is now coherent — one console (Defender), one admission framework (Azure Policy), one identity model (Workload Identity), one egress controller (Azure Firewall).*

## Analogy — the K-Campus wing

**Campus Police** on K-Campus runs four shifts.
    The **Mailroom Shift** (image / supply chain) inspects every box arriving at the loading dock — scans for contraband CVEs, refuses unsigned packages, replicates the safe ones to satellite mailrooms (geo-replication). The mailroom keeps a continuously updated list of "recalled items" (new CVEs) and pulls them off shelves automatically (Image Cleaner).
    The **Door Shift** (admission / posture) checks every guest at every building door — Azure Policy / Gatekeeper says "this guest is wearing the wrong badge, denied," or "this guest needs PSA Restricted clearance." Posture inspectors walk the buildings continuously checking that locks are engaged, fire doors closed, NetworkPolicy default-deny present.
    The **Patrol Shift** (runtime + identity + egress) watches what happens inside. Defender runtime agents look for unusual behaviour. Workload Identity means no master keys are stashed in offices — every worker gets a fresh permit. Azure Firewall guards the only road off campus — only addresses on the allow-list get out.
    The **Building Shift** (node OS + hardware) maintains the buildings themselves. Some buildings are reinforced concrete (FIPS pools), some are vault-grade (Confidential Containers — silicon-encrypted memory), all have tamper-evident seals (Trusted Launch). Plus there's a notice on every Azure Linux 2 building: *"this building closes 2026-03-31; move to Azure Linux 3 or Ubuntu 24."*

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| Mailroom inspectors | ACR + Defender image scanning |
| Recalled-items list | Continuous CVE re-scan |
| Mailroom shelf-purge | Image Cleaner add-on |
| Sealed package signature check | Cosign / Notation + admission verifier |
| Mailroom satellites | ACR geo-replication |
| Door checker | Azure Policy for AKS (Gatekeeper) |
| Restricted-clearance guests | PSA Restricted standard |
| Posture inspector walks | Defender posture management |
| Patrol agents | Defender runtime threat detection |
| No master keys in offices | Workload Identity (no long-lived secrets) |
| Single road off campus + allow-list | Azure Firewall egress filtering |
| Reinforced-concrete buildings | FIPS node pools |
| Vault-grade memory-encrypted offices | Confidential Containers (Kata + AMD SEV-SNP) |
| Tamper-evident door seals | Trusted Launch (secure boot + vTPM) |
| "Building closes 2026-03-31" notice | Azure Linux 2 EOL migration |

⚠️ *Analogy stops here:* A real Campus Police force can't look inside encrypted memory; Confidential Containers can be inspected by their own attestation reports but not by external observers — the metaphor of "vault-grade" is closer to literal in this case.

## ELI5 / ELI10

**ELI5.** Police on campus do four jobs: check what arrives in the mail (boxes), check who comes through doors (guests), watch what happens in buildings (cameras), and keep the buildings strong (locks, walls). Same with AKS — image scans, admission rules, runtime watching, hardware security.

**ELI10.** AKS security is layered. **Image:** Defender + ACR scanning + content trust + Image Cleaner; private ACR for isolation. **Admission/posture:** Azure Policy (Gatekeeper) + PSA Restricted + NetworkPolicy default-deny + Defender posture findings. **Runtime:** Defender runtime detection + Workload Identity (no secrets) + Azure Firewall egress + apiserver audit to Log Analytics. **Node OS / hardware:** FIPS pools, host encryption, Trusted Launch (secure boot + vTPM), Confidential Containers (Kata + AMD SEV-SNP). Migrate Azure Linux 2 → AL3 or Ubuntu 24 by 2026-03-31 (AL2 node images removed).

## Real-world scenarios

- **Bank — Defender + private ACR + signed images.** A bank requires every production image to be signed (Cosign) and scanned (Defender). Pipeline: Build → push to private ACR → Defender scans → if 0 critical CVEs, Cosign signs → admission verifier (Azure Policy with custom Constraint) blocks unsigned or vulnerable images at deploy. Bank also enables continuous re-scan; Image Cleaner removes anything that becomes vulnerable post-deploy. *Compliance audit: zero exception in 6 months.*
- **SaaS — PSA Restricted across all namespaces in one quarter.** A SaaS has 200 microservices that historically ran as root with privileged: true. Q1 plan: enable PSA Audit on all namespaces (no breakage; just findings); per service, fix root + capability + seccomp violations; flip to PSA Warn (informs developers); finally PSA Enforce. *Q1 end: every namespace at PSA Restricted; zero deployment-time surprises in Q2.*
- **Healthcare — Confidential Containers for PHI workloads.** A healthcare ML team trains models on patient data. Compliance requires in-use memory encryption. They add a Confidential Containers node pool (DCasv5, AMD SEV-SNP). PHI-handling Pods are scheduled to that pool via toleration + nodeSelector. Each Pod runs in a Kata utility VM with hardware-encrypted RAM and attestation. *External attestation report given to compliance auditor; audit clears on first review.*
- **Migration — Azure Linux 2 to Ubuntu 24 across 12 clusters.** A platform team has 12 clusters with mixed AL2 / Ubuntu 22 pools. Azure Linux 2 EOL 2025-11-30; node images removed 2026-03-31. Plan: per cluster, create new Ubuntu 24 pool alongside AL2 pool; drain workloads with PDB safety; delete AL2 pool. Two-week sprint per cluster; finished by Feb 2026 with one-month buffer. *No outages; one cluster needed an Ubuntu 24 driver fix for an obscure GPU SKU; otherwise smooth.*

## Common misconceptions

- **Myth:** "PSA replaces Azure Policy / Gatekeeper."
  **Truth:** They're complementary. **PSA** = K8s-native, baseline Pod-security checks (root, capabilities, hostPath, etc.) at three levels. **Azure Policy / Gatekeeper** = arbitrary admission policies (image registry allowlist, label requirements, NetworkPolicy presence, etc.). PSA covers Pod-security baseline; Azure Policy covers everything else.
- **Myth:** "My image was scanned at build time, so it's safe."
  **Truth:** A new CVE published yesterday makes yesterday's "clean" image vulnerable today. Defender for Containers does **continuous re-scan** as the CVE feed updates. Image Cleaner pulls vulnerable images off node disks. Build-time scan is necessary but not sufficient.
- **Myth:** "My Workload Identity-bound MI is small-scope; an attacker compromising a Pod can't do much."
  **Truth:** Verify the MI scope is actually small. Common drift: MI was created with one permission, expanded over time as new features were added, never re-pruned. Defender posture flags over-privileged identities; review quarterly. Combine WI scoping with PSA Restricted (limits what the Pod itself can do on the node) + NetworkPolicy default-deny (limits lateral movement) + Azure Firewall (limits egress to known endpoints).

## Recap

Four security shifts: image (Defender + ACR + Image Cleaner), admission/posture (Azure Policy + PSA), runtime (Defender + WI + Azure Firewall), node OS / hardware (FIPS + Confidential + Trusted Launch + AL3 migration).

**Next — A7: AKS Observability.** Azure Monitor managed Prometheus + Managed Grafana, Container Insights with Log Analytics + KQL, Application Insights for app traces, Azure Monitor managed OpenTelemetry, control-plane diagnostic settings, Network Observability, Cost Management.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
