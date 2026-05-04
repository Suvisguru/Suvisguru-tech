# K-ADV-SEC S8 — S8 · Capstone — Defendable Regulated Platform

> Course: K-ADV-SEC (advanced specialization)
> Module S8 · Capstone
> Companion preview: `/preview-kubernetes-adv-sec-lesson-08.html`.

---

**🎯 If you remember nothing else:** **Defendable = (1) every layer wired (S1-S7), (2) audit + compliance dashboards continuous, (3) break-glass replaces standing admin, (4) game days quarterly. The architecture isn't the work; the disciplined assembly + exercise is the work.**

## 1. Cluster + tenant + workload + observability layout

**Cluster shape**: regional control plane (3-zone HA); private nodes + master authorized networks; PSA enforce-restricted cluster default; audit policy + webhook to SIEM enabled at bring-up.
    **Tenants**: hard multi-tenancy via vCluster for untrusted-code tenants; soft multi-tenancy via namespace + RBAC + NetPol + ResourceQuota for trusted teams. Per-tenant SecretStore + workload identity.
    **Workloads**: every Service uses a per-workload SA with audit2rbac-narrowed RoleBinding. Pods drop ALL caps; runAsNonRoot; seccompProfile RuntimeDefault. Logs via FireLens / Fluent Bit to SIEM. Traces via OTel + Tempo / X-Ray. Metrics via Prometheus + Grafana.
    **Observability**: audit.k8s.io → SIEM (Splunk / Loki); Falco / Tetragon eBPF on every node; Container Insights / cloud-native APM. Compliance-as-code dashboards run nightly.

## 2. What admission + runtime enforce, end-to-end

From request to running Pod, the controls fire in order:
    
      - **Auth**: OIDC for humans (with MFA) or short-lived projected SA for workloads. Tokens have audience + 1-hour TTL.

      - **RBAC**: per-team / per-workload narrow Roles; cluster-admin only via JIT.

      - **Mutation**: Kyverno mutate sets resource defaults, adds team / cost-center labels, injects Firelens sidecar.

      - **Validation**: Kyverno validates label requirements + image registries; Gatekeeper validates cross-resource correlation (Service-to-Namespace allow-list); ValidatingAdmissionPolicy + CEL for hot-path inline rules; Kyverno verifyImages for Cosign sig + SLSA + SBOM presence.

      - **PSA**: namespace label enforce-restricted blocks privileged / hostPath / capabilities.

      - **Runtime**: Falco / Tetragon eBPF on the node alerts on shell-in-container, mount(), unexpected egress, RoleBinding mutations.

## 3. External vault → ESO → K8s Secret → Pod; mesh-mTLS; SPIFFE

**Secrets path**: HashiCorp Vault (HA, KMS-sealed) → ESO with per-namespace SecretStore using IRSA / Workload Identity → K8s Secret (KMS-encrypted at rest) → Pod env / volume mount. Vault rotates DB + API creds via its IAM / DB engines; ESO syncs; reloader restarts Pods.
    **Identity**: humans via OIDC (Okta / Auth0); workloads via projected SA tokens federated to cloud IAM (IRSA / Pod Identity / Workload Identity); SPIFFE-format certs from mesh CA for Pod-to-Pod mTLS.
    **Mesh**: Istio ambient (or Linkerd / Cilium) cluster-wide. Every Pod-to-Pod call signed + encrypted; cert auto-rotates hourly; AuthorizationPolicy enforces "only X SA may call Y SA."
    **cert-manager**: Ingress + internal certs auto-rotated; Let's Encrypt for external; private CA for internal.

## 4. Continuous evidence + tested response

**Audit**: audit.k8s.io with Request level for write verbs + RequestResponse for RBAC; webhook → Splunk; retention tiered (90d hot / 1yr warm / 6yr Glacier). Synthetic-audit canary every minute.
    **SIEM rules**: detection-as-code in Git. ~80 rules covering RBAC drift, secret access anomalies, image admission denials, runtime escapes, suspicious DNS, privilege escalations, OIDC anomalies. Tiered (page / Slack / log-only).
    **Compliance-as-code**: PCI / HIPAA / SOC2 / FedRAMP / NIST 800-190 controls each map to a SIEM query + expected result. Nightly CI run; failures Slack #compliance-ops within 14h of audit.
    **Break-glass**: cluster-admin removed for everyone; JIT process: ChatOps approval bot + 1-hour cred + alarmed. Quarterly review of every JIT use.
    **IR**: NIST 800-61 runbooks per scenario class (compromise / lateral / data-exfil / DoS / supply-chain). Quarterly game days inject pattern + measure time-to-detect / time-to-contain. Targets: P95 detect < 5min, contain < 30min.

## Before / After

**Before.** Pre-disciplined K8s security: each layer adopted ad-hoc; gaps between layers; audit annual + manual; standing admin; runbook in someone's head; first incident reveals the gaps.

**After.** The Defendable Citadel: every K-ADV-SEC layer wired, integrated, exercised. Compliance is continuous; admin is JIT; runbooks are tested; new threats trigger new rules + game days within 30 days. Audit time drops 70%; mean-time-to-contain < 30 minutes.

*Disciplined assembly + exercise is the work. The architecture is the easy part.*

## Analogy — the K-Citadel bastion

The Defendable Citadel's architect arrives at the morning audit. Every wall is correctly built (S1-S6); every record is current (S7); the war-room binders are dog-eared from quarterly drills. The auditor reviews three things on the wall: the threat-model wheel (showing every category mapped to a control), the compliance map (every regulator's control mapped to a query + last-result timestamp), the IR drill register (last quarter's game day timing).
    Inside the citadel: every visitor passes the perimeter, the identity gate, the tenant compound, the vault. Every conversation is mTLS-sealed. Every gate-keeper's decision is archived. The Captain of the Watch elevates only via the alarmed key — and the alarm has fired three times this quarter, all expected.
    The capstone is not a new technique; it's every prior module woven into one architecture, plus the operational rhythm — runbooks, dashboards, game days — that keeps the citadel *defendable*, not just defended.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Threat-model wheel on the wall | STRIDE per Service mapped to controls |
| Outer wall + identity gate + compounds + vault | perimeter + AuthN + tenants + secrets layers |
| Sealed letter to printer; verified at gate | Cosign + SBOM + SLSA + verifyImages |
| Vault couriers with workshop permits | ESO with per-namespace SecretStore + workload identity |
| mTLS-sealed conversations | Mesh-mTLS + SPIFFE per workload |
| Audit archive + compliance maps | audit.k8s.io → SIEM + compliance-as-code |
| Quarterly drill register | Game days + IR runbook exercise |
| Alarmed elevation key | Break-glass JIT IAM |

⚠️ *Analogy stops here:* A real citadel's walls are visible; K8s defenses are configuration + policy + process. Verify each via game-day exercises, not visual inspection.

## ELI5 / ELI10

**ELI5.** The complete castle: every wall built, every guard trained, every emergency rehearsed. Compliance audits become a 6-hour walk-through, not a 6-week scramble. Every guard has a binder; every binder is practiced.

**ELI10.** Reference architecture: regional cluster + private nodes + PSA Restricted default; vCluster hard tenancy for untrusted; audit2rbac-narrowed per-workload RBAC; Kyverno + Gatekeeper + ValidatingAdmissionPolicy hybrid + verifyImages; Falco / Tetragon eBPF; Vault + ESO + mesh-mTLS + SPIFFE + cert-manager + workload identity; audit.k8s.io → SIEM with synthetic canary + compliance-as-code dashboards; break-glass JIT IAM; quarterly game days with P95 detect < 5min / contain < 30min.

## Real-world scenarios

- **Fintech regulated platform.** A 100-engineer fintech runs the full stack on EKS. SOC2 + PCI + state-banking-regulator compliance. Audit time dropped from 6 weeks (sample-based) to 2 weeks (compliance-as-code dashboards). Game days catch ~2 control gaps per quarter; remediation in 2 weeks each.
- **Healthcare PHI platform.** A health-tech runs a PHI platform on AKS with the same architecture. Hard multi-tenancy via vCluster per hospital; per-tenant Vault paths; mesh-mTLS strict; audit retention 6 years (HIPAA). HIPAA security risk assessment maps directly to dashboards.
- **Game day caught a missing detection.** Q3 game day: red team tried a novel pattern (using a service account JWT to call cloud KMS via IRSA). Existing rules didn't fire. New SIEM rule + Falco rule added; rerun next quarter cleanly. Continuous improvement loop.
- **Outage — game-day-discovered runbook gap.** A real incident: compromised CI runner pushed a malicious image; Cosign verifyImages caught it at admission. Runbook step "revoke CI runner credentials" took 12 minutes due to manual approval flow; target was 5 min. Action: ChatOps approval bot for credential revocation; next game day clean.

## Common misconceptions

- **Myth:** "This architecture is over-engineered."
  **Truth:** Every layer here exists because *something doesn't exist without it*. The marginal cost of building all layers from day-1 is moderate; the cost of bolting them on after the first audit failure is enormous. Regulated platforms have no "start small" path.
- **Myth:** "Compliance dashboards replace audits."
  **Truth:** Dashboards make audits *fast* + evidence-based; they don't replace human review of judgment calls. Auditors still inspect the mapping ("why is this query the right evidence for this control?"). Dashboards reduce audit-prep effort, not the audit itself.
- **Myth:** "You can't have hard multi-tenancy on shared nodes."
  **Truth:** vCluster + Kata Containers / gVisor gives *kernel-level* isolation while sharing physical nodes. Hard multi-tenancy ≠ per-cluster — modern stacks support it on shared infra at moderate cost. Per-cluster reserved for the strictest regulatory boundaries.

## Recap

The Defendable Citadel: every K-ADV-SEC layer wired (S1-S7), every audit + compliance control queryable, every IR runbook tested. The work is not the architecture — it's the operational rhythm that keeps the architecture defendable.

**K-ADV-SEC complete.** 8 modules. From threat modeling (S1) to the defendable citadel (S8). Next K-ADV course: *K-ADV-NET* (Networking Architect — K-Highway), or per founder direction. The Citadel pin map is fully populated.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
