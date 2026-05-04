# K-ADV-SEC S6 — S6 · Secrets + mTLS + Service Mesh Security

> Course: K-ADV-SEC (advanced specialization)
> Module S6 · Secrets + mTLS + Mesh
> Companion preview: `/preview-kubernetes-adv-sec-lesson-06.html`.

---

**🎯 If you remember nothing else:** **Secrets in external vault, synced via ESO, KMS-encrypted at rest. mTLS via mesh + SPIFFE/SPIRE workload identity. cert-manager + automated rotation. No long-lived static credentials anywhere.**

## 1. Vault / Secrets Manager / Key Vault as source of truth

Pick one external vault. **HashiCorp Vault** for cloud-agnostic / hybrid; **AWS Secrets Manager** for AWS-only; **Azure Key Vault** / **GCP Secret Manager** similar. The vault holds the source-of-truth secrets + handles rotation (Lambda-style or built-in for DBs).
    **External Secrets Operator (ESO)**: K8s controller that watches a `SecretStore` CR (vault auth config) + `ExternalSecret` CR (which secrets to sync where). ESO polls vault; creates/updates K8s Secrets; KMS-encrypts at rest via `--encryption-provider-config`.
    Pattern: per-namespace SecretStore using IRSA / Workload Identity / Pod Identity (no shared cluster-wide vault token). ESO's ServiceAccount in each namespace federates to the vault role for that namespace only — tenant isolation.
    Rotation: vault rotates → ESO detects on next poll → updates K8s Secret → Pods restart on Secret change (via reloader or in-app SDK). End-to-end rotation is a vault-API call.

## 2. Istio / Linkerd / Cilium — sidecar vs ambient

**Service mesh** wraps every Pod-to-Pod call in mTLS automatically. Three popular meshes:
    
      - **Istio**: most features (traffic mgmt + policy + telemetry); sidecar mode (Envoy per Pod) or *ambient mode* (per-node ztunnel + per-namespace waypoint proxy — lower overhead).

      - **Linkerd**: simpler + faster than Istio; Rust micro-proxy; SPIFFE-based identity; ambient-style architecture.

      - **Cilium Service Mesh**: eBPF-based; integrates with Cilium NetworkPolicy + Hubble observability.

    
    All three: every workload gets a SPIFFE ID; mTLS certs are issued per workload; certs auto-rotate hourly; mesh enforces "only signed traffic accepted" per workload. Lateral movement after compromise is blocked at the mesh.

## 3. workload identity standard

**SPIFFE** (Secure Production Identity Framework For Everyone) is the standard for workload identity. SPIFFE IDs look like `spiffe://cluster.local/ns/api/sa/orders`. **SPIRE** is the reference implementation: agents on each node issue short-lived X.509-SVIDs (or JWT-SVIDs) to workloads based on attestation rules.
    Mesh integration: Istio + Linkerd both issue SPIFFE-format certs to Pods. The mesh's control plane calls SPIRE (or its own CA) to issue per-Pod certs.
    **cert-manager**: K8s CRD-based PKI for Ingress / API server / generic certs. Issuer types: ACME (Let's Encrypt), Vault, Venafi, custom CA, self-signed. CertificateRequest + Certificate CRDs auto-rotate via `renewBefore`. Pair with mesh for end-to-end PKI hygiene.

## 4. No static credentials in images, env, or git

The mature pattern is **zero static credentials** in container images, environment variables (committed to git), or Helm values. Sources of secrets:
    
      - **Workload identity** (IRSA / Workload Identity / Pod Identity): cloud auth via federation — Pod's SA token traded for cloud creds at runtime.

      - **External Secrets via ESO**: app secrets (DB passwords, API keys) fetched from vault.

      - **SPIFFE workload identity**: workload-to-workload mTLS identity.

      - **cert-manager**: in-cluster certs (Ingress, internal services).

    
    **Audit**: scan images for hardcoded secrets (gitleaks, trufflehog); scan repos pre-commit (pre-commit hooks + git secrets); SIEM alert on Kubernetes Secret reads (audit.k8s.io). Quarterly review: any namespace with a Secret not managed by ESO or cert-manager → flag + remediate.

## Before / After

**Before.** Pre-vault clusters had secrets in env vars committed to git, ConfigMaps, or hand-rotated K8s Secrets. Rotation was manual + per-deployment — "rotate password 14 times" failure mode. Pod-to-Pod calls were unencrypted in the cluster network. Lateral movement after compromise was free.

**After.** Modern: secrets in external vault, synced via ESO, KMS-encrypted at rest. Pod-to-Pod over mesh-mTLS with SPIFFE workload identity. cert-manager + automated rotation. Workload identity (IRSA / Workload Identity / Pod Identity) for cloud auth. *Zero static credentials anywhere in source.*

*Secrets flow; identity is short-lived; mTLS is automatic. Manual rotation is an anti-pattern.*

## Analogy — the K-Citadel bastion

The deepest stronghold in the citadel is the **Armored Vault**. Originally, secrets were copied by hand to every workshop in the citadel — when a key changed, every workshop had to be visited individually. Things broke when copies drifted; rotation was a multi-day job.
    The modern vault has three improvements. (1) A single **master vault** holds the source-of-truth (Vault / Secrets Manager / Key Vault). (2) **Bonded couriers** (External Secrets Operator) deliver secrets to each workshop on demand — automatically updated when the master changes. (3) Every courier presents their **workshop-specific permit** (per-namespace SecretStore + workload identity) — couriers can't cross-deliver.
    For workshop-to-workshop conversation, every worker now wears a **numbered identity badge** (SPIFFE ID) issued by the citadel's identity bureau (SPIRE), and every conversation is sealed in a tamper-evident envelope (mTLS). The mail-carrier (mesh sidecar) seals + checks every envelope automatically.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Master vault | External vault (HashiCorp / AWS Secrets / Azure KV / GCP SM) |
| Bonded couriers | External Secrets Operator (ESO) |
| Workshop-specific permit | Per-namespace SecretStore + IRSA / Workload Identity |
| Sealed K8s storage chest | K8s Secret with KMS encryption-at-rest |
| Numbered identity badge | SPIFFE workload ID |
| Identity bureau | SPIRE (or mesh CA issuing SPIFFE certs) |
| Tamper-evident envelopes | mTLS via service mesh (Istio / Linkerd / Cilium) |
| Mail-carrier with sealing kit | mesh sidecar (Envoy / Linkerd-proxy / ambient ztunnel) |
| Citadel-wide PKI | cert-manager (Ingress / API / generic certs) |

⚠️ *Analogy stops here:* A real vault holds physical objects; K8s Secrets are policy + bytes. KMS-encryption-at-rest is a config switch (encryption provider config) — easy to forget; verify with `etcdctl get` output.

## ELI5 / ELI10

**ELI5.** The castle has one giant vault holding all the keys. Couriers bring keys to each workshop on schedule; couriers don't share routes. Every worker wears a numbered badge issued by the security office. Every message between workers is sealed in a tamper-proof envelope by the mail-carrier. No keys are left lying around.

**ELI10.** **External vault** holds source-of-truth secrets. **External Secrets Operator (ESO)** syncs vault → K8s Secret per namespace; per-namespace SecretStore with workload identity. **KMS encryption-at-rest** via apiserver config. **Service mesh** (Istio / Linkerd / Cilium) injects sidecars or ambient proxies; auto mTLS for Pod-to-Pod with **SPIFFE**-format certs from **SPIRE**. **cert-manager** for cluster certs. **Workload identity** for cloud auth (IRSA / Workload Identity / Pod Identity). **Zero static creds** in images, env, or git.

## Real-world scenarios

- **Greenfield with Vault + ESO + Linkerd.** A 50-engineer SaaS deploys: HashiCorp Vault as cluster-external secret store; ESO with per-namespace SecretStore + IRSA; Linkerd auto-mTLS cluster-wide. From day one: zero static creds; mesh-mTLS for everything; rotation = vault API call.
- **Brownfield audit + ESO migration.** A team audits 200 namespaces; finds 80 K8s Secrets created manually + ~12 with credentials in git (oops). 6-month migration: vault setup, ESO ExternalSecret per Secret, gradual cutover. Each Secret's replacement validated; old Secret deleted from git history (BFG).
- **Istio ambient — lower overhead than sidecars.** A 1000-Pod cluster previously ran sidecar Istio with ~50 MiB memory overhead per Pod. Migration to Istio ambient: per-node ztunnel + per-namespace waypoint proxies; per-Pod overhead drops to ~5 MiB. mTLS still automatic; same SPIFFE identity model.
- **Outage — vault unreachable; cluster kept running.** An ESO-backed cluster lost vault connectivity for 90 minutes. Existing K8s Secrets stayed in cluster; Pods kept running with last-fetched values. Pod restarts that needed fresh secrets failed PROVISIONING; queued. Vault returned; ESO reconciled in 2 minutes; queued Pods drained. *Local cache + ESO's reconciliation kept blast radius small.*

## Common misconceptions

- **Myth:** "K8s Secrets are encrypted by default."
  **Truth:** K8s Secrets are *base64-encoded by default*, NOT encrypted. To encrypt at rest, configure `--encryption-provider-config` on the apiserver pointing to KMS. Without that, etcd stores plain (base64) values. Verify with `etcdctl get`.
- **Myth:** "Service mesh is overkill for small clusters."
  **Truth:** The mTLS + workload identity benefits apply at any size. Linkerd has the lightest footprint; Istio ambient mode is now competitive. The right question is "do we need Pod-to-Pod mTLS?" — for any cluster handling sensitive data, the answer is yes.
- **Myth:** "SPIFFE / SPIRE adds complexity we don't need."
  **Truth:** If using a service mesh, you're using SPIFFE under the hood whether you know it or not. SPIRE explicit deployment matters when (a) you want workload identity for non-mesh workloads (databases, cloud APIs); (b) you need cross-cluster identity federation. For most teams, mesh-managed SPIFFE is enough.

## Recap

Secrets in external vault, synced via ESO with per-namespace tenant isolation, KMS-encrypted at rest. mTLS via mesh + SPIFFE identity. cert-manager for cluster PKI. Workload identity for cloud auth. Zero static credentials in source.

**Next — S7: Audit log analytics + compliance evidence + IR.** audit.k8s.io webhook → SIEM; PCI / HIPAA / FedRAMP / SOC2 / NIST 800-190 control mapping; break-glass IAM; incident response playbooks.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
