# K-ADV-SEC S1 — S1 · Threat Modeling, Zero-Trust, Multi-Tenant Isolation

> Course: K-ADV-SEC (advanced specialization)
> Module S1 · Threat Modeling, Zero-Trust, Tenancy
> Companion preview: `/preview-kubernetes-adv-sec-lesson-01.html`.

---

**🎯 If you remember nothing else:** **Threat-model first; zero-trust everywhere; multi-tenant isolation by design. Four layers: perimeter, identity, tenant zone, vault. Each layer authenticates + authorises independently. A breach at one layer must not become a breach of the next.**

## 1. STRIDE applied to a Kubernetes cluster

**STRIDE** walks every component asking what could go wrong. For a K8s cluster:
    
      - **Spoofing**: someone presents as another principal — stolen ServiceAccount token, leaked kubeconfig, OIDC token theft. *Defence*: short-lived tokens (projected JWTs / IRSA / Workload Identity), mTLS, audit replay-detection.

      - **Tampering**: image swapped between build + deploy; manifest mutated in transit. *Defence*: signed images (Cosign), SBOM + provenance attestation, GitOps as source-of-truth.

      - **Repudiation**: actor denies an action. *Defence*: audit.k8s.io logs every authz decision; SIEM retention.

      - **Information disclosure**: secrets leaked via env, logs, mountPoints. *Defence*: Secrets Manager / Vault, KMS at rest, log redaction, mesh mTLS in transit.

      - **Denial of service**: noisy neighbour or attack consumes CPU / memory / API quota. *Defence*: ResourceQuota, LimitRange, PriorityClass, API priority + fairness.

      - **Elevation of privilege**: container escape, RBAC verb misuse, ServiceAccount over-broad. *Defence*: PSA Restricted, runtime detection (Falco / Tetragon), RBAC least-privilege, no privileged unless justified.

    
    Run STRIDE per Service. Document what each Service does + handles + needs; the answers drive every policy in the layers below.

## 2. No implicit trust at any boundary

Zero-trust says: *every request authenticates + authorises, every time, regardless of network position*. Translated to K8s:
    
      - **API server**: every call presents identity (token / cert); RBAC checks every verb; admission applies every policy. No "internal traffic" exception.

      - **Pod-to-Pod**: mTLS via service mesh (Istio / Linkerd) — SPIFFE/SPIRE-issued workload identity; default-deny NetworkPolicy; explicit allow rules per consumer.

      - **Pod-to-cloud-API**: workload identity (IRSA / Workload Identity / Pod Identity) — no static credentials; short-lived tokens scoped per Pod.

      - **Human access**: OIDC SSO; short-lived kubeconfig (15-60 min); MFA for cluster admin; just-in-time RBAC for production.

    
    The opposite (perimeter-trust) says "once you're inside the firewall, you're trusted." In a cluster, that means an attacker who lands one Pod has free range. Zero-trust closes that.

## 3. Soft (namespace) vs hard (vCluster / per-cluster)

**Soft multi-tenancy**: tenants share a cluster; isolation via Namespace + RBAC + NetworkPolicy + PSA + ResourceQuota + LimitRange. Cheap; suits internal teams + low-risk SaaS. *Cannot fully isolate at the kernel level* — a kernel CVE crosses namespaces.
    **Hard multi-tenancy via virtual clusters** (vCluster / Capsule / Loft): each tenant gets its own apiserver + control plane running inside the host cluster's namespaces. Tenants see a real cluster; admins manage them centrally. Stronger isolation than namespace-only, cheaper than per-cluster.
    **Hard multi-tenancy via per-cluster**: one cluster per tenant. Strongest isolation. Highest infrastructure cost. Use for regulated workloads, untrusted third-party code, jurisdictional data residency.
    **Choosing**: high-trust internal teams → soft. Untrusted code or strict compliance → hard via vCluster or per-cluster. Start soft + escalate as risk warrants.

## 4. Perimeter · Identity · Tenant zone · Vault

Every K-ADV-SEC concept slots into one of four layers. Each layer authenticates + authorises independently; a breach at one layer must not become a breach of the next.
    
      - **Perimeter**: untrusted-Internet boundary. Tools: AWS WAF / Azure Front Door / Cloudflare; Ingress / Gateway with TLS termination; rate limiting; bot detection. *What can fail*: DDoS, OWASP Top-10 attacks, leaked credentials brute-force.

      - **Identity**: every principal proves who they are. Tools: OIDC for humans; ServiceAccount JWTs (projected, short-lived) for workloads; mTLS via mesh; cert-manager + SPIFFE/SPIRE for workload identity. *What can fail*: token theft, replay, weak rotation.

      - **Tenant zone**: namespace-level isolation. Tools: Namespace + RBAC (Roles + Bindings) + NetworkPolicy (default-deny + explicit allow) + PSA Restricted + ResourceQuota + LimitRange. Optional: vCluster for stronger isolation. *What can fail*: over-broad RBAC, missing NetPol, hostPath escapes, unbounded resources.

      - **Vault**: deepest stronghold. Tools: External Secrets Operator + Vault / Secrets Manager + KMS; audit.k8s.io webhook to SIEM; signed images (Cosign + SBOM + VEX); break-glass + IR runbooks. *What can fail*: secret leak, missing audit, unverified image, slow IR.

    
    The layers are concentric, not stacked — a request reaches the vault only after passing each prior layer.

## Before / After

**Before.** Pre-zero-trust K8s clusters were a single trust zone. Once a workload landed inside the cluster network, it could call the API server with the default ServiceAccount token (auto-mounted everywhere), reach any Pod (no NetworkPolicy default-deny), and read or write secrets the kubelet had access to. A web-app CVE became a cluster compromise.

**After.** Modern K-ADV-SEC clusters apply zero-trust: every Pod has its own ServiceAccount with short-lived projected tokens; default-deny NetworkPolicy with explicit allow per consumer; mesh-mTLS for Pod-to-Pod; PSA Restricted blocks privileged + hostPath; runtime detection (Falco / Tetragon) catches escape attempts. *One Pod compromise stops at the next gate.*

*Defence-in-depth, not a single wall. Each layer is small; together they're strong.*

## Analogy — the K-Citadel bastion

K-Citadel is a fortified citadel. The Threat Map Room is the first chamber every architect visits — pinned to the wall is a STRIDE wheel, a list of every entry point, every internal corridor, and every place secrets are kept.
    The citadel has four concentric walls. The **outer wall** faces the open countryside (untrusted Internet) — guards inspect every visitor for weapons (WAF / DDoS protections). Past the outer wall is the **identity gate** — every visitor presents papers, even citizens (zero-trust). Past identity is the **tenant compound** — different families occupy walled compounds with their own gate-keepers (namespaces with RBAC + NetworkPolicy). Deepest is the **armored vault** — secrets, audit logs, signed manifests; only authorised stewards reach it.
    The Captain of the Watch (you) maps every corridor: where can a compromise at one wall go? Where does it stop? The citadel is designed so any single wall failing is a contained event — the next wall holds.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Threat Map Room | Threat-modeling exercise (STRIDE per Service) |
| Outer wall | Perimeter — Ingress / Gateway / WAF / public LB |
| Identity gate | AuthN — OIDC + mTLS + ServiceAccount tokens |
| Verbs on the gate-keeper's scroll | RBAC verbs (get/list/create) on resources |
| Walled compound (one family) | Namespace + RBAC + NetworkPolicy + PSA |
| Compound's rationing rules | ResourceQuota + LimitRange |
| Stronger walls between compounds | vCluster / per-cluster (hard multi-tenancy) |
| Armored vault | Secrets Manager / Vault + KMS |
| Vault keeper's ledger | audit.k8s.io → SIEM |
| Sealed papers from the printer | Cosign-signed image + SBOM + VEX |
| Standing order "never trust, always check" | Zero-trust posture |

⚠️ *Analogy stops here:* A real citadel's walls are physical and slow to breach; K8s "walls" are policy + identity + crypto, and a missing policy is invisible until tested. Game days are how you find missing walls.

## ELI5 / ELI10

**ELI5.** A castle has many walls — outer wall, identity gate, family compounds, armored vault. Each wall checks every visitor independently. If one wall fails, the next still holds. Your cluster works the same way: every Pod, every secret, every API call passes multiple checks.

**ELI10.** **Threat model** = STRIDE walk per Service. **Zero-trust** = no implicit trust at any boundary; mTLS + workload identity + RBAC at every step. **Multi-tenant isolation**: soft (Namespace + RBAC + NetPol + PSA + Quota) for high-trust; hard (vCluster / per-cluster) for untrusted code or compliance. **Four concentric layers**: perimeter, identity, tenant zone, vault — each authenticates + authorises independently.

## Real-world scenarios

- **Fintech — STRIDE per critical Service.** A 100-engineer fintech runs STRIDE on every Service handling money. *Spoofing*: short-lived OIDC + IRSA. *Tampering*: signed images + GitOps. *Repudiation*: audit.k8s.io to compliance SIEM with 7-year retention. *Disclosure*: Vault + KMS + mesh-mTLS. *DoS*: ResourceQuota + PriorityClass. *Elevation*: PSA Restricted + Falco. *One pattern across services; auditors map controls to STRIDE categories.*
- **SaaS — soft multi-tenancy with namespace-per-customer.** A 25-engineer SaaS isolates customers via Namespace + RBAC + NetPol default-deny + PSA Restricted + per-customer ResourceQuota. Tenants see only their namespace; service accounts scoped tightly; mesh-mTLS for Service-to-Service. *Soft works because tenants don't run arbitrary code; they consume the SaaS app.*
- **Regulated — hard multi-tenancy via vCluster.** A health-tech runs PHI for multiple hospitals. Each hospital gets a vCluster; vClusters share host cluster nodes; control planes are isolated. *Tenants see real K8s clusters* with their own RBAC, NetPol, even some CRDs. Compliance reviewers map a vCluster to a tenant boundary cleanly.
- **Outage — perimeter-only design failed.** A startup put all security at the WAF + Ingress. A vulnerable image got past CI; once running, the app called the API server using its auto-mounted ServiceAccount token (kept default permissions); read other Pods' secrets; exfiltrated. *One wall, one breach.* Postmortem: layer 2 + 3 + 4 added.

## Common misconceptions

- **Myth:** "Cluster-internal traffic is trusted; mTLS only matters for Internet-facing."
  **Truth:** Zero-trust says **every** request authenticates. Pod-to-Pod calls without mTLS = an attacker who lands one Pod can impersonate any consumer of any other Service. Mesh-mTLS or workload identity at every hop is the standard.
- **Myth:** "Namespace + RBAC alone is enough multi-tenancy."
  **Truth:** Namespaces share a kernel. A kernel CVE that allows container escape crosses namespaces freely. Namespace + RBAC + NetPol + PSA + Quota together cover most threats; truly untrusted code needs vCluster or per-cluster.
- **Myth:** "Threat modeling is a security-team activity, not a platform activity."
  **Truth:** Platform engineers *own* half the controls (RBAC, NetPol, PSA, admission, mesh, audit). Threat modeling done without platform input misses controls; done without security input misses threats. Joint exercise per service.

## Recap

Threat-model first, zero-trust always, multi-tenancy by design. Four concentric layers: perimeter, identity, tenant zone, vault. Each layer authenticates independently. The next 7 modules each deepen one of the layers — RBAC at scale (S2), admission policy (S3), PSA + runtime (S4), signed images (S5), secrets + mesh (S6), audit + compliance + IR (S7), and the capstone (S8) wires them all into a defendable citadel.

**Next — S2: RBAC Design at Scale.** Subjects + Roles + Bindings; aggregation patterns; tooling (rakkess, kubectl-who-can); audit-driven RBAC narrowing; namespace-scoped vs cluster-scoped; OIDC group → Role mappings.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
