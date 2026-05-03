# K-AKS A2 — A2 · Azure Identity and Access (Entra ID, Workload Identity, Azure RBAC)

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A2 · Entra and Workload Identity
> Companion preview: `/preview-kubernetes-aks-lesson-02.html`.

---

**🎯 If you remember nothing else:** **Two surfaces: Entra ID authenticates humans to kube-apiserver (Azure RBAC for K8s preferred); Workload Identity authenticates Pods to Azure services (federated credentials replace deprecated Pod Identity). Disable local accounts; use managed identities, not service principals.**

## 1. Two identity surfaces — keep them separated

AKS identity has *two completely separate* surfaces. Confusing them is the #1 root cause of "why can't I do X?" tickets.
    
      - **Surface 1 — human → cluster.** Who can call `kube-apiserver`? *Authentication* via Entra ID. *Authorization* via either Kubernetes RBAC (managed in cluster as `Role`/`ClusterRole`) or **Azure RBAC for Kubernetes Authorization** (managed in Entra as Azure roles bound to scopes — recommended for new clusters).

      - **Surface 2 — Pod → Azure service.** How does a Pod call Key Vault, Storage, ACR, Service Bus, etc., without baking secrets in code? **Workload Identity** — the Pod's ServiceAccount is federated with an Entra application via the cluster's OIDC issuer. Pod gets an OIDC token; Entra exchanges it for an Azure access token; Pod calls the Azure SDK normally.

    
    Old-and-deprecated paths: **aad-pod-identity** (pre-Workload Identity Pod-to-Azure auth, deprecated 2024) and **service principals** for cluster identity (replaced by managed identities). If you inherit a cluster using either, the upgrade path is migration to Workload Identity + managed identity.

## 2. Human auth — kubelogin and disable local accounts

When a human runs `kubectl` against an Entra-integrated AKS cluster, the auth flow is:
    
      - kubectl reads `kubeconfig`; sees an exec credential plugin pointing at `kubelogin`.

      - kubelogin opens a browser (or uses device code) to authenticate the user against Entra ID — Conditional Access policies fire here (MFA, device compliance, location, risk score).

      - Entra returns an access token scoped to the AKS cluster.

      - kubectl sends the token to kube-apiserver as a Bearer.

      - apiserver validates the token signature against Entra; extracts the user / group claims.

      - Authorization: either Azure RBAC for K8s (Entra-side) or in-cluster RBAC (RoleBinding/ClusterRoleBinding referencing the Entra principal).

    
    **Two kubeconfigs:** `az aks get-credentials` returns an Entra-integrated config (default). `az aks get-credentials --admin` returns the cluster-admin local-account kubeconfig (bypasses Entra entirely — emergency-only). **Disable local accounts** (`--disable-local-accounts`) on production clusters so the admin kubeconfig path doesn't exist; emergencies use a designated break-glass Entra group.
    **Conditional Access for kubectl:** the same Entra Conditional Access policies that gate the Azure Portal apply to `kubectl`. You can require MFA every kubectl session, deny kubectl from untrusted networks, require a compliant Intune-managed device, etc.

## 3. Pod auth — Workload Identity (federated credentials)

Workload Identity lets a Pod call Azure services *without any secret stored in the cluster*. The flow:
    
      - Cluster has an **OIDC issuer URL** (enabled with `--enable-oidc-issuer`).

      - You create an Entra application (or use a user-assigned managed identity) and add a **federated credential** trusting `{cluster-OIDC}/serviceaccount/{namespace}/{sa-name}`.

      - You annotate the K8s ServiceAccount: `azure.workload.identity/client-id: <app-client-id>`.

      - Your Pod uses that ServiceAccount and is labelled `azure.workload.identity/use: "true"`.

      - Workload Identity webhook injects two env vars + a projected ServiceAccount token into the Pod.

      - Azure SDK in the Pod sees the env vars, exchanges the SA token for an Azure access token via Entra, calls Key Vault / ACR / Storage / Service Bus normally.

    
    The result: **no secret in cluster, no secret to rotate, no secret to leak.** Tokens are short-lived; the OIDC trust is revocable per federated credential.
    **Managed identity vs Entra app for Workload Identity:** both work. **User-assigned managed identity** is preferred for new setups — its lifecycle is independent of the cluster, supports cross-RG / cross-subscription scenarios, and is targetable by Azure RBAC. **Entra application** is needed for cross-tenant trust.

## 4. ACR + Key Vault — the two adjacent services

**ACR (Azure Container Registry)** integration: `az aks update --attach-acr <registry>` grants the cluster's kubelet identity the **AcrPull** role on the registry. Pods can then pull `myregistry.azurecr.io/myapp:v1` without any imagePullSecret. *The kubelet identity is a separate user-assigned managed identity (not the cluster identity)* — created automatically per cluster, used only for ACR pulls.
    For private ACR (no public endpoint), use **Private Link** + a Private DNS zone bound to the cluster's VNet. Cluster-to-ACR traffic stays on the Microsoft backbone.
    **Key Vault integration** via the **Secrets Store CSI driver + Azure Key Vault provider**: a SecretProviderClass declares which secrets/keys/certs to fetch; the driver mounts them into the Pod as files (and optionally syncs to a K8s Secret). Workload Identity authenticates the driver to Key Vault. *Auto-rotation: enable the rotation poller and set `rotationPollInterval`* — secrets refresh in the volume, and (if synced) the K8s Secret updates so the Pod can pick up via volume reload or rolling restart.

## Before / After

**Before.** Pre-Workload-Identity AKS clusters used **aad-pod-identity** — a DaemonSet (NMI) intercepted IMDS calls from Pods and exchanged the Pod's assigned identity for tokens. It worked but was operationally fragile: the NMI DaemonSet had to run on every node, IMDS interception broke with some host networking modes, and the AzureIdentityBinding CRD was confusing. Plus pre-Entra-RBAC clusters used **service principals** with a long-lived secret stored as `aks-service-principal` — leaks, rotation pain, expiring creds taking down clusters.

**After.** Workload Identity replaces aad-pod-identity entirely: *no DaemonSet, no IMDS interception, no NMI* — just a webhook that injects env vars + a projected SA token into the Pod, and a federated credential on the Entra side. Token never touches disk. Same Pod code (Azure SDK) just works. **Managed identity** replaces service-principal for cluster identity: Azure rotates the credential automatically; you never see it. Combined with Azure RBAC for K8s + Conditional Access, the human-and-Pod identity story finally feels coherent.

*aad-pod-identity is deprecated; new clusters must use Workload Identity. Service-principal AKS clusters must migrate to managed identity.*

## Analogy — the K-Campus wing

The **Registrar's Office** sits in the middle of K-Campus. Everyone — Faculty, students, contractors, robots — must check in at the Registrar before they're allowed into any building. The Registrar is **Entra ID**: the single source of truth for who you are.
    There are **two windows** at the Registrar. Window 1 (**Visitor Badges**): humans show up with their photo ID; the Registrar checks the campus database, runs Conditional Access checks ("are you on a managed device? did you swipe MFA?"), and prints a badge that says "Allowed in Building B for the next 8 hours." That badge is the kubelogin token.
    Window 2 (**Worker Permits**): a robot worker (a Pod) shows up needing access to the Library (Key Vault). It doesn't carry an ID — instead it shows the Registrar a sealed envelope (the projected ServiceAccount token) issued by its home department (the OIDC issuer). The Registrar checks the federated credential ("yes, this department's envelopes are trusted to vouch for workers in *that* service-account slot"), prints a Worker Permit (Azure access token), and the robot walks to the Library.
    The deprecated old way: every robot used to carry a permanent badge stapled to its chest (a service-principal secret). Robots lost badges; badges expired; replacing them was a nightmare. Workload Identity is "no permanent badge, just a sealed envelope you generate fresh every time."

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| The Registrar | Microsoft Entra ID (formerly Azure AD) |
| Visitor Badge window | kubelogin → kube-apiserver token |
| Worker Permit window | Workload Identity → Azure access token |
| Conditional Access checks | MFA, device compliance, location, risk |
| Sealed envelope from a department | Projected ServiceAccount token (OIDC) |
| Federated credential | Trust between Entra app/MI and the OIDC issuer + SA |
| Permanent stapled badge (deprecated) | Service principal secret |
| Worker Permit valid for X hours | Azure access token TTL (~1h, refreshed) |
| Two-window separation | Surface 1 (human → cluster) vs Surface 2 (Pod → Azure) |
| Disabled side door | `--disable-local-accounts` kills bypass kubeconfig |
| Break-glass key in the Director's safe | Designated Entra Break-Glass group with cluster-admin |

⚠️ *Analogy stops here:* The Registrar metaphor implies one centralised authority. In reality Entra ID is replicated globally and tokens are validated cryptographically — no per-request round trip to a single Registrar.

## ELI5 / ELI10

**ELI5.** There's one office on campus that knows everybody. Before you go into any building, you stop there and they print you a paper badge that says where you can go. Robots have a different paper called a Worker Permit — they get it the same way every time, instead of carrying a key around their neck that could fall off.

**ELI10.** AKS auth has two surfaces. Humans authenticate to `kube-apiserver` via Entra ID + kubelogin (Conditional Access policies fire — MFA, device, location), authorize via Azure RBAC for K8s (preferred) or in-cluster RBAC. Pods authenticate to Azure services via **Workload Identity**: cluster has an OIDC issuer, ServiceAccount is annotated with a client ID, federated credential on an Entra app/MI trusts that SA, webhook injects an SA token + env vars into the Pod, Azure SDK exchanges the SA token for an access token via Entra. **No secrets stored anywhere.** Disable local accounts; use managed identities not service principals; aad-pod-identity is dead.

## Real-world scenarios

- **Bank — Conditional Access + break-glass Entra group.** A bank requires every `kubectl` session against prod to require: a compliant Intune device, MFA every 8 hours, only from corporate VPN egress IPs. They configure these as Conditional Access policies on the AKS cluster's Entra application. `--disable-local-accounts` removes the admin kubeconfig escape hatch. A break-glass Entra group with cluster-admin role exists for emergencies; membership is monitored in Sentinel. *One bypass attempt = SOC ticket.*
- **Migration — aad-pod-identity → Workload Identity in 4 sprints.** Pre-existing AKS cluster uses aad-pod-identity for ~30 microservices. Engineering team migrates per-service across 4 sprints: enable OIDC issuer + Workload Identity webhook on the cluster, create user-assigned MIs per service (Bicep modules), add federated credentials, annotate ServiceAccounts, label Pods, drop aad-pod-identity binding. *No code changes — Azure SDK auto-detects the credential source via env vars.* aad-pod-identity uninstalled at sprint 5.
- **ML team — Workload Identity for Storage + Key Vault.** An ML training Pod needs read on a 200-TB blob container and three secrets from Key Vault. Single user-assigned MI per training job; federated credential to the job's SA; MI granted Storage Blob Data Reader on the container + Key Vault Secrets User on three secrets. Pod uses default Azure SDK chain. *Job logs show no credentials, only MI client ID; if the job leaks logs, no auth material is exposed.*
- **Multi-tenant SaaS — per-tenant federated credential.** A SaaS where each tenant's workload runs in its own namespace with its own ServiceAccount. One Entra app per tenant; one federated credential per tenant's SA. Tenant A's Pod can never get Tenant B's tokens — the SA subject doesn't match. *Tenant isolation enforced at the federated-credential layer, not just RBAC.*

## Common misconceptions

- **Myth:** "Workload Identity is just aad-pod-identity rebranded."
  **Truth:** Different architecture. aad-pod-identity ran an NMI DaemonSet that intercepted IMDS calls and translated them to Azure tokens. Workload Identity uses an admission webhook + projected ServiceAccount tokens + OIDC federated credentials — *no DaemonSet, no IMDS interception, no NMI*. aad-pod-identity is deprecated; new clusters cannot install it.
- **Myth:** "Azure RBAC for K8s and Kubernetes RBAC are the same thing."
  **Truth:** **Kubernetes RBAC** = Role/ClusterRole/RoleBinding objects in the cluster, evaluated by kube-apiserver against the user's Entra principal. **Azure RBAC for Kubernetes Authorization** = Azure-side roles (e.g. *Azure Kubernetes Service RBAC Reader*) assigned at cluster/namespace scope in Entra, evaluated by an apiserver auth webhook talking to Azure. They can coexist; Azure RBAC for K8s is the modern path for Entra-integrated clusters.
- **Myth:** "`--admin` kubeconfig is fine for daily use."
  **Truth:** The `--admin` kubeconfig is the local cluster-admin account — bypasses Entra entirely, has no Conditional Access, no MFA, no audit trail beyond raw apiserver logs. On production clusters it should be disabled (`--disable-local-accounts`) and only re-enabled for emergencies. Daily use must go through Entra-integrated kubeconfig with kubelogin.

## Recap

Two surfaces: humans via Entra+kubelogin+Azure RBAC for K8s; Pods via Workload Identity. Local accounts disabled, break-glass Entra group, ACR + Key Vault wired in cleanly.

**Next — A3: AKS Networking.** Azure CNI vs Azure CNI Overlay vs CNI by Cilium vs BYO; private clusters; API VNet integration; AGIC vs Application Gateway for Containers (AGC); Web App Routing add-on; SNAT exhaustion; NetworkPolicy options.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
