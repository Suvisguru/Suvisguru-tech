# Lesson 21 — ServiceAccounts & Certificates · Tokens, Projected JWTs, cert-manager, Cluster PKI

> Course: Kubernetes — Common to all distributions
> Module 10 · Config & Identity · Lesson 2 of 2
> Companion preview: `/preview-kubernetes-lesson-21.html`.

---

**🎯 If you remember nothing else:** Every Pod has a **ServiceAccount** (its workload identity). Modern clusters use **projected, short-lived, audience-bound JWTs** — *not* the legacy long-lived Secret tokens. For TLS certs (Ingress, webhooks, mTLS), use **cert-manager** — never hand-roll OpenSSL.

## 1. Workload identity vs human identity

Two kinds of identity in K8s. **Users** are humans (or external CI systems) authenticated through OIDC, certificates, or static tokens — they're *not* a K8s API object; they're a string the API server accepts. **ServiceAccounts** are workload identities — actual API objects in a namespace, used by Pods to talk to the API server (or to any other identity-aware service).
    Every Pod runs as a ServiceAccount. If you don't specify one, it's `default`. The kubelet projects a JWT into the Pod (under `/var/run/secrets/kubernetes.io/serviceaccount/token`); any process in the Pod can read it and use it as a Bearer token to talk to the API server.
    The big shift between K8s 1.21 and today: tokens are now **short-lived (1h default), audience-bound (a JWT `aud` claim), and auto-refreshed** by the kubelet. Pre-1.21, tokens were stored in long-lived Secrets and never expired — a leak was a permanent compromise. Modern clusters: a leaked token is useful for at most an hour.

## 2. Projected vs legacy ServiceAccount tokens

Legacy (pre-1.24)Projected / Bound (modern)
      
      
        LifetimeForever1 hour default; refreshed at 80%
        StorageLong-lived `Secret` objectRead from kubelet's mount; never touches etcd
        AudienceImplicit (API server only)Explicit `aud` claim
        On Pod deleteToken still validToken bound to Pod UID — invalid the moment Pod dies
        Created byK8s auto-created a Secret per SAYou ask for one explicitly via `TokenRequest` API or volume projection
      
    
    Default behaviour in 1.24+: K8s no longer auto-creates a long-lived Secret per ServiceAccount. The Pod gets a projected token via the `serviceAccountToken` volume projection. *If you find a long-lived SA token Secret in a modern cluster, it was created intentionally — typically as an integration credential for an external system that can't refresh.*

## 3. Why every K8s component has a certificate

Every TLS connection between cluster components — API server ↔ kubelet, kubelet ↔ apiserver, etcd ↔ etcd, controller-manager ↔ apiserver — is mTLS-authenticated with X.509 certificates. The default tooling (kubeadm, the major distros, the cloud-managed control planes) sets up a small PKI:
    
      - **Cluster CA** — the root that signs everything. Lives in `/etc/kubernetes/pki/ca.crt` on a kubeadm-managed control plane.

      - **API server cert** — signed by the CA; presented when clients talk to `kubernetes.default.svc`.

      - **kubelet certs** — one per node; signed by the CA via the **kubelet-bootstrap** flow at node join. Auto-rotated.

      - **etcd peer + client certs** — internal to etcd; signed by a separate etcd CA usually.

      - **Front-proxy CA** — separate CA used for aggregated API servers (extension API servers, metrics-server).

    
    For application-level TLS (Ingress endpoints, webhook configurations, app-to-app mTLS), don't extend the cluster CA — that's its job, not yours. Stand up **cert-manager** for app-level certs; it's a CRD-driven controller that integrates with Let's Encrypt, Vault, your cluster's CA, or any other ACME-compatible issuer.
    [ deep dive — skip if new ]The OIDC discovery endpoint at `/.well-known/openid-configuration` on the API server publishes the cluster's JWT verification keys. This is what lets external systems (AWS IAM Roles for Service Accounts, GCP Workload Identity Federation, Vault) *verify* a projected SA token without contacting the API server. The token itself is a standards-compliant OIDC JWT — that's the whole basis for cluster-to-cloud workload identity.

## 4. Three CRDs you actually use

📜
        Issuer / ClusterIssuer
        where certs come from
        Defines a CA source: Let's Encrypt (HTTP-01 or DNS-01 ACME), Vault PKI, an internal CA, or a self-signed root. `Issuer` is namespace-scoped; `ClusterIssuer` is cluster-wide.
        Set up once per environment.
      
      
        🪪
        Certificate
        a specific cert request
        "Issue a cert for these DNS names, valid for X days, store the result in this Secret named Y." cert-manager renews it before expiry (default at 2/3 of lifetime).
        One per app / Ingress / mTLS endpoint.
      
      
        🎫
        CertificateRequest / Order
        internal accounting
        CRs and Orders are intermediate objects cert-manager creates while talking to the issuer. You don't write them; they're useful for debugging stuck issuance.
        Read-only for users.
      
    
    A typical Ingress with TLS: define a `ClusterIssuer` for Let's Encrypt prod, then add the `cert-manager.io/cluster-issuer` annotation on your Ingress. cert-manager creates the `Certificate`, runs the ACME flow, stores the result in a `kubernetes.io/tls` Secret, and the Ingress controller picks it up. Renewals happen automatically. Total Ops touch: zero after setup.

## Before / After

**Before.** Pre-1.24 era: every ServiceAccount had a permanent `Secret` token. Leak = permanent compromise. Cluster certs renewed by writing a runbook and praying a junior engineer remembered to run it before the cert expired. Application TLS = OpenSSL commands in a wiki page, last updated three years ago.

**After.** Modern cluster: projected tokens are short-lived (1h), audience-bound, auto-refreshed. Cluster control-plane certs auto-rotated via kubeadm or the managed control plane. Application TLS via `cert-manager` + a `ClusterIssuer`; you write a `Certificate` and forget about it forever. The runbook is gone — replaced by declarative resources.

The single most under-appreciated migration in K8s history was bound service account tokens. Pre-2022 most clusters had thousands of permanent credentials lying around. Post-2024, virtually none.

## Analogy — the K-Town district

The Permit Office issues two kinds of paperwork. The **passport** (ServiceAccount) is the identity itself: it says "this is app-x, vouched for by the city." The **travel pass** (token) is what app-x actually presents at every checkpoint: it's a stamped, time-limited document the kid courier carries in their pocket. Old K-Town used to issue passes that never expired — a lost pass meant someone could impersonate you forever. New K-Town issues passes that expire in an hour and are auto-refreshed by the courier office (the kubelet).Behind another counter: the **certificate press**. cert-manager runs the press: it talks to a recognised authority (Let's Encrypt, Vault, the city CA), gets a sealed certificate, hands it to whoever asked, and pre-emptively reprints it before it expires. Nobody hand-cuts certificates anymore in modern K-Town.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The passport with the holder's photo | `ServiceAccount` object |
| The stamped travel pass | Projected JWT (1h, audience-bound, refreshed by kubelet) |
| Travel passes that never expired (old) | Legacy long-lived SA token Secrets (pre-1.24 default) |
| The city's seal of authenticity | Cluster CA cert (signs API server, kubelet, etcd certs) |
| The certificate press | cert-manager controller |
| A standing relationship with a cert authority | `ClusterIssuer` (e.g., Let's Encrypt, Vault PKI) |
| Today's certificate request slip | `Certificate` object |
| The seal-checking machine at the customs line | API server's TLS chain validation |

⚠️ *Analogy stops here:* The analogy stops here: real K8s tokens are JWTs, signed cryptographically — the whole stack of trust depends on whether the cluster's signing key is protected. "The city CA" is one private key on disk; lose it and the whole metaphor collapses.

## ELI5 / ELI10

**ELI5.** Every Pod gets a name badge (ServiceAccount) and a paper hall pass (the token). The hall pass expires in an hour and the front desk (kubelet) gives you a new one before it runs out. Long ago hall passes never expired and that was a problem.

**ELI10.** Every Pod runs as a `ServiceAccount` — a workload identity. The kubelet projects a short-lived (1h), audience-bound JWT into the Pod at `/var/run/secrets/kubernetes.io/serviceaccount/token`. The Pod presents it as a Bearer token. Lost or leaked = useful for at most an hour. Cluster components (apiserver, kubelet, etcd) authenticate to each other with X.509 certs from a small per-cluster PKI. For application-layer TLS, run `cert-manager` + a `ClusterIssuer` and let it handle issuance + rotation declaratively.

## Real-world scenarios

- **A SaaS using IAM Roles for ServiceAccounts (IRSA) on EKS.** The Pod's projected JWT has audience `sts.amazonaws.com`. STS verifies it by hitting EKS's OIDC endpoint, returns AWS credentials. The Pod authenticates to AWS without ever holding an AWS access key. Rotation: kubelet refreshes the JWT every 50 minutes; AWS creds get re-issued in turn.
- **A bank running mTLS between every microservice.** cert-manager has a Vault PKI ClusterIssuer. Every Deployment has a Certificate sidecar that issues a 24h cert. Service mesh (Linkerd, in this case) consumes the cert. Hard mTLS everywhere. Vault rotates the intermediate CA quarterly; cert-manager re-issues on the next renewal.
- **A startup with a Let's Encrypt setup that took 5 minutes.** Install cert-manager → apply a `ClusterIssuer` for Let's Encrypt → add `cert-manager.io/cluster-issuer: letsencrypt-prod` annotation on the Ingress. cert-manager runs the HTTP-01 challenge, gets a cert, stores it in a Secret, the Ingress controller picks it up. Renewals are silent.
- **A team that audited their old long-lived tokens.** Found 47 ServiceAccount Secrets created pre-1.21 that nobody remembered. Half were unused; the other half belonged to integrations they could migrate to bound tokens. The cleanup deleted 38 of them, replaced 9 with bound tokens or workload-identity flows. Surface area for credential theft dropped by an order of magnitude.

## Common misconceptions

- **Myth:** `kubectl create token` is just for testing.
  **Truth:** It's the recommended way to mint a one-off token for an external integration in 2026. The legacy way (create a Secret of type `kubernetes.io/service-account-token`) still works but is discouraged. `kubectl create token sa-name --duration=1h --audience=foo` issues a bound token via the TokenRequest API.
- **Myth:** cert-manager can manage the cluster's control-plane certs.
  **Truth:** No. Control-plane PKI (apiserver, kubelet, etcd) is managed by kubeadm, the distro (kops, k3s, RKE2), or the managed cloud control plane. cert-manager is for *application-layer* certs (Ingress, webhooks, mTLS). Mixing the two will break things.
- **Myth:** The default ServiceAccount is fine.
  **Truth:** It's fine until you grant it a Role and forget that *every* Pod in that namespace inherits it. Treat `default` as no-permissions; create per-workload SAs and bind RBAC to them. Pod Security Admission can enforce "every Pod must specify a non-default SA."

## Recap

Pods get an identity (ServiceAccount) and a short-lived, bound token (projected JWT). Cluster components trust each other via a small PKI. App-level TLS is cert-manager + a ClusterIssuer; never hand-roll OpenSSL.

**Next — Lesson 22: Scheduling Part 1.** How K8s decides which node a Pod lands on. Affinity and anti-affinity, taints and tolerations, topology-spread constraints. Dispatch Office routes the trucks.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
