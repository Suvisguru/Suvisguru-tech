# K-OCP O4 — O4 · OpenShift Security

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O4 · OpenShift Security
> Companion preview: `/preview-kubernetes-ocp-lesson-04.html`.

---

**🎯 If you remember nothing else:** **Default to restricted-v2 SCC; only escalate explicitly. Use Compliance Operator for CIS/NIST/PCI scans + RHACS for runtime. Integrated OAuth + identity providers; KMS for secrets; FIPS for federal; Kata for sandboxed untrusted workloads.**

## 1. Integrated OAuth + identity providers + OCP RBAC

**OCP's integrated OAuth server** is built into the cluster (cluster operator `authentication`). It backs all human auth + many service-to-service flows.
    **Identity providers** configurable via `OAuth/cluster`: **HTPasswd** (file-based, dev/break-glass), **LDAP** (corporate dir), **OIDC** (Keycloak / Okta / Auth0), **GitHub**, **GitLab**, **Google**, **Keystone** (OpenStack), **RequestHeader** (proxy auth), **BasicAuth**. Multiple IDPs can coexist.
    **OCP RBAC** = K8s RBAC + OCP-specific roles: *cluster-admin*, *admin* (project), *edit* (project), *view* (project), plus all the `system:` roles. `oc adm policy add-role-to-user` / `oc adm policy add-cluster-role-to-user`.
    **ServiceAccounts** — every Project gets *default*, *builder*, and *deployer* SAs by default. Workloads that need scoped permissions get their own SA + RoleBinding.

## 2. Security Context Constraints (SCCs) — five defaults you should know

**SCCs** are OCP's admission system for Pod-security. Predates K8s' Pod Security Admission (PSA). Bound to ServiceAccounts; the Pod's SA must be granted an SCC for the Pod to run.
    Built-in SCCs (most-restrictive to least):
    
      - **restricted-v2** (default) — non-root, drop all caps + add NET_BIND_SERVICE, seccomp RuntimeDefault, no hostPath/hostNet/hostPID/hostIPC, no privileged. *Where every workload should aim.*

      - **nonroot-v2** — must run as non-root (no UID 0); slightly less restrictive on capabilities.

      - **anyuid** — allows any UID. For workloads that hard-code UID (legacy images). Avoid where possible.

      - **hostnetwork** — allows hostNetwork (sees host's network namespace). For node-level networking workloads.

      - **privileged** — full root + caps + host access. Only for cluster-critical infra (CSI drivers, low-level monitoring agents).

    
    **SCC vs PSA:** OCP supports both. PSA labels are honored on namespaces; SCC admission runs in addition. *Default OCP namespaces are pre-labelled with PSA `restricted`; SCC admission enforces parallel constraints.* For new workloads, design for restricted-v2 + PSA restricted; only escalate when proven needed.

## 3. Compliance Operator + RHACS (StackRox)

**Compliance Operator** — runs *OpenSCAP* scans against the cluster + nodes for compliance baselines: **CIS** (Kubernetes Benchmark), **NIST 800-53**, **PCI-DSS**, **FedRAMP**, **HIPAA**. Generates `ComplianceCheckResult` CRDs; suggests automated remediations via `ComplianceRemediation`. Schedule periodic scans via `ScanSettingBinding`.
    **File Integrity Operator (FIO)** — AIDE-based file integrity monitoring on RHCOS. Detects unauthorized changes to critical filesystem paths (`/etc`, `/usr/bin`, etc.). Generates alerts on drift.
    **Security Profiles Operator (SPO)** — manages seccomp + SELinux + AppArmor profiles as K8s resources. Bind to Pods via SPOD CRDs.
    **Red Hat Advanced Cluster Security (RHACS) / StackRox** — comprehensive K8s security platform:
    
      - *Vulnerability management* — image + deployment scans

      - *Compliance* — CIS, NIST, PCI-DSS dashboards

      - *Network graph* — visualises Pod-to-Pod traffic + suggests NetworkPolicies

      - *Runtime threat detection* — eBPF + audit-based; detects shells, miners, lateral movement

      - *Admission control* — block deploys violating policy at admission

    
    Multi-cluster: one RHACS Central manages many Secured Clusters across an organisation.

## 4. KMS + FIPS + OpenShift sandboxed containers (Kata)

**KMS integration** — etcd Secrets encryption with external KMS (AWS KMS, Azure Key Vault, GCP KMS, HashiCorp Vault). `EncryptionConfiguration` on the apiserver. Keys rotated externally; etcd holds ciphertext.
    **FIPS mode** — install OCP with FIPS 140-2 validated cryptography. Set `fips: true` in install-config; cluster boots with FIPS kernel + crypto libraries. Required for federal / regulated workloads. Cannot toggle FIPS post-install.
    **Disconnected security** — air-gapped clusters need security operators (Compliance, RHACS, FIO) installed via mirrored OperatorHub catalogs. RHACS Central sits inside the air-gap; Sensor pods on each cluster phone-home to it.
    **OpenShift sandboxed containers (Kata)** — runs Pods in lightweight VMs (Kata Containers + KVM) for stronger isolation than runc. Per-Pod kernel; container escape doesn't reach host. *For multi-tenant workloads with untrusted code (CI runners, customer-submitted code, sensitive PII).* ~5-15% perf overhead on syscall-heavy workloads.

## Before / After

**Before.** Pre-OCP K8s security was DIY: bring-your-own RBAC discipline, no SCC equivalent, PSP (deprecated), separate compliance scanning tools, separate runtime detection (Falco, Sysdig). Multi-cluster security was scripts. FIPS was a kernel-config exercise. KMS integration was custom. Sandboxed containers required separate runtime install + OS support.

**After.** OCP ships **integrated OAuth + 7 identity providers + OCP RBAC + 5 default SCCs**; **Compliance Operator** for CIS/NIST/PCI/FedRAMP/HIPAA scans; **File Integrity** + **Security Profiles** Operators; **RHACS / StackRox** as the comprehensive K8s security platform; **KMS** integration via apiserver EncryptionConfiguration; **FIPS mode** at install; **Kata sandboxed containers** for stronger isolation.

*Layered defence with Red Hat-supported components: auth + SCC + compliance + runtime + hardware. Each layer is independently meaningful; together they're a defendable security story.*

## Analogy — the K-Foundry bay

The **Safety Office** is the foundry's defence-in-depth headquarters. Four shifts.
    The **Badge Window** (OAuth + RBAC) issues badges to humans (HTPasswd / LDAP / OIDC) and worker-permits to robots (ServiceAccounts). Every visitor and worker passes here.
    The **Safety Inspector's Booth** (SCCs) checks every Pod against the regulations. *restricted-v2* is the default uniform; some specialty workers need *anyuid* exceptions; only critical infrastructure gets *privileged*.
    The **Compliance Auditor's Office** (Compliance Operator + File Integrity + Security Profiles) runs scheduled audits against CIS/NIST/PCI/FedRAMP/HIPAA — generates checklists with auto-remediation suggestions. The **RHACS Watchtower** (StackRox) monitors live: vulnerability scanning, network graph, runtime threat detection, admission control.
    The **Hardware Vault** handles silicon-level concerns: KMS-managed keys for etcd Secrets; FIPS-validated cryptography (chosen at install); Kata sandboxed containers for tenants with untrusted workloads.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| Badge Window | Integrated OAuth server + identity providers |
| Worker permit | ServiceAccount + RoleBinding |
| Foundry-wide role book | OCP RBAC (cluster-admin, admin, edit, view + system:*) |
| Safety Inspector's rule book | SCC list (restricted-v2, nonroot-v2, anyuid, hostnetwork, privileged) |
| Default uniform | restricted-v2 SCC |
| Special-case exception | anyuid / hostnetwork SCC |
| Cluster-critical-infra-only badge | privileged SCC |
| Compliance Auditor's checklists | Compliance Operator (CIS / NIST / PCI / FedRAMP / HIPAA scans) |
| File-integrity tripwires | File Integrity Operator (AIDE-based) |
| Seccomp / SELinux profile bindings | Security Profiles Operator |
| Comprehensive watchtower | RHACS / StackRox (vuln + compliance + network + runtime + admission) |
| Hardware vault keys | KMS-encrypted etcd Secrets |
| FIPS-validated crypto stamp | FIPS install mode |
| Untrusted-worker isolation cell | OpenShift sandboxed containers (Kata) |

⚠️ *Analogy stops here:* A real Safety Office can't look inside Confidential VMs (Kata); SCC bypass via cluster-admin escalation is a real risk the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** The Safety Office checks badges, enforces uniform rules, runs surprise inspections, watches camera feeds, and maintains the vault. Each shift has a different job; together they keep the foundry safe.

**ELI10.** OCP security = OAuth + identity providers + OCP RBAC + ServiceAccounts (authN/Z); SCCs (restricted-v2 default, nonroot-v2, anyuid, hostnetwork, privileged) for Pod-security; Compliance Operator + File Integrity + Security Profiles for compliance; RHACS / StackRox for runtime + admission + network + vuln; KMS for etcd Secrets; FIPS install mode; Kata sandboxed containers for stronger isolation.

## Real-world scenarios

- **Bank — RHACS multi-cluster + Compliance Operator + KMS + FIPS.** A bank's OCP fleet (10 prod clusters) runs RHACS multi-cluster — Central manages all Secured Clusters' policies. Compliance Operator runs weekly PCI-DSS scans; results aggregated in RHACS Central. KMS integration with on-prem HashiCorp Vault for etcd Secrets. FIPS install mode (cannot retrofit; chosen at install).
- **Telco — Kata for untrusted CI tenants.** Telco runs CI for partner integrations on a shared OCP cluster. Risk: malicious build escapes container, attacks node. Solution: dedicated node pool with Kata runtime; CI Pods scheduled there via runtimeClassName. Each Pod runs in its own KVM-backed lightweight VM. *Container escape doesn't cross VM boundary.*
- **SaaS — Compliance Operator finds 73 non-compliant manifests.** A SaaS enables Compliance Operator with the CIS Kubernetes profile. Initial scan: 73 ComplianceCheckResult failures. Operator suggests ComplianceRemediation manifests for ~50 of them (auto-applicable). Manual fixes for the other 23. *CIS score from 41% to 94% in 2 weeks.*
- **anyuid escalation reverted — workload rewritten to non-root.** A team discovered their Helm chart granted anyuid 18 months ago for a single Deployment. They rewrote the chart to use a non-root user UID, removed the SA-to-anyuid binding. *Posture improved; restricted-v2 enforced cluster-wide; one less escalation drift to monitor.*

## Common misconceptions

- **Myth:** "SCCs are obsolete since PSA exists."
  **Truth:** OCP supports both. PSA labels gate at the K8s level; SCCs gate at the OCP admission webhook level. They're complementary; both run in modern OCP. SCCs predate PSA and remain Red Hat-supported. Don't remove SCCs; design for both.
- **Myth:** "FIPS can be enabled later."
  **Truth:** FIPS mode is an **install-time choice** via `fips: true` in install-config. The cluster boots with FIPS-validated crypto libraries + kernel. Cannot retrofit on existing clusters; requires reinstall. Plan + decide at install for federal / regulated workloads.
- **Myth:** "Kata sandboxed containers solve all multi-tenancy security problems."
  **Truth:** Kata adds **strong isolation between Pods** (per-Pod kernel via lightweight VM). It doesn't solve: identity sprawl, RBAC drift, NetworkPolicy gaps, secret rotation, image supply chain. Layer Kata on top of those; not as a replacement.

## Recap

Four shifts: authN/Z (OAuth + RBAC + SAs), SCCs (restricted-v2 default), compliance + RHACS, hardware (KMS / FIPS / Kata).

**Next — O5: Operators and OLM.** Operator Hub + CatalogSources + Subscriptions + InstallPlans + ClusterServiceVersions (CSV) + OperatorGroups + channels + manual vs automatic approval; Operator dependencies; broken-operator recovery; certified vs community vs custom operators.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
