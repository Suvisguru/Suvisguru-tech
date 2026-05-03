"""K-AKS A2 — Azure Identity and Access (Entra ID, Workload Identity, Azure RBAC for K8s)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two identity surfaces: Entra ID for cluster API access, Workload Identity for Pod-to-Azure-service auth.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Two identity surfaces — Registrar's Office</text>
  <rect x="50" y="60" width="320" height="130" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="210" y="82" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">human → cluster</text>
  <text x="210" y="100" text-anchor="middle" font-size="10" fill="#FBF7F0">Entra ID + Azure RBAC for K8s + kubelogin</text>
  <rect x="70" y="115" width="280" height="60" rx="6" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="210" y="135" text-anchor="middle" font-size="10" font-weight="700" fill="#3F4A5E">Entra principal</text>
  <text x="210" y="150" text-anchor="middle" font-size="9" fill="#3F4A5E">— Conditional Access checks (MFA, device, location) →</text>
  <text x="210" y="165" text-anchor="middle" font-size="9" fill="#3F4A5E">apiserver authorises via Azure RBAC OR K8s RBAC</text>
  <rect x="390" y="60" width="320" height="130" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="550" y="82" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">Pod → Azure service</text>
  <text x="550" y="100" text-anchor="middle" font-size="10" fill="#FFFFFF">Workload Identity (federated cred)</text>
  <rect x="410" y="115" width="280" height="60" rx="6" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="550" y="135" text-anchor="middle" font-size="10" font-weight="700" fill="#3F4A5E">SA token (OIDC) → federated cred</text>
  <text x="550" y="150" text-anchor="middle" font-size="9" fill="#3F4A5E">→ Entra issues access token →</text>
  <text x="550" y="165" text-anchor="middle" font-size="9" fill="#3F4A5E">Pod calls Key Vault / ACR / Storage</text>
</svg>"""


LESSON = LessonSpec(
    num="02",
    title_short="Entra &amp; Workload Identity",
    title_full="A2 · Azure Identity and Access (Entra ID, Workload Identity, Azure RBAC)",
    title_html="K-AKS A2 · Azure Identity and Access",
    module_eyebrow="Module A2 · the Registrar's Office",
    hero_sub_html='Two identity surfaces. <strong>Human → cluster:</strong> Entra ID + Azure RBAC for Kubernetes Authorization + kubelogin + Conditional Access. <strong>Pod → Azure service:</strong> Workload Identity (federated credentials, OIDC issuer) — replaces deprecated Pod Identity. Plus ACR + Key Vault integration; admin vs user kubeconfig; managed identities (system / user-assigned) vs legacy service principals.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It's 3 AM. You\'re paged: <em>\"Pod can\'t fetch secret from Key Vault — 401 Unauthorized.\"</em> You SSH the node — wait, you can\'t, AKS hides it. You check the Pod\'s service account: bound to a managed identity. You check Key Vault access policies: principal listed. You realise the cluster\'s OIDC issuer URL changed when someone re-created the cluster last week, so the federated credential trust no longer matches. <em>Workload Identity tokens look fine but are addressed to a tenant-of-yesteryear.</em> Today\'s lesson: how AKS authentication actually works.",
    stamp_html="<strong>Two surfaces: Entra ID authenticates humans to kube-apiserver (Azure RBAC for K8s preferred); Workload Identity authenticates Pods to Azure services (federated credentials replace deprecated Pod Identity). Disable local accounts; use managed identities, not service principals.</strong>",
    district_pin="kc-wing02",
    district_label="Registrar's Office",
    sections=[
        Section(
            eyebrow="Section 1.1 · the two identity surfaces",
            h2="Two identity surfaces — keep them separated",
            body_html="""    <p>AKS identity has <em>two completely separate</em> surfaces. Confusing them is the #1 root cause of \"why can\'t I do X?\" tickets.</p>
    <ul>
      <li><strong>Surface 1 — human → cluster.</strong> Who can call <code>kube-apiserver</code>? <em>Authentication</em> via Entra ID. <em>Authorization</em> via either Kubernetes RBAC (managed in cluster as <code>Role</code>/<code>ClusterRole</code>) or <strong>Azure RBAC for Kubernetes Authorization</strong> (managed in Entra as Azure roles bound to scopes — recommended for new clusters).</li>
      <li><strong>Surface 2 — Pod → Azure service.</strong> How does a Pod call Key Vault, Storage, ACR, Service Bus, etc., without baking secrets in code? <strong>Workload Identity</strong> — the Pod\'s ServiceAccount is federated with an Entra application via the cluster\'s OIDC issuer. Pod gets an OIDC token; Entra exchanges it for an Azure access token; Pod calls the Azure SDK normally.</li>
    </ul>
    <p>Old-and-deprecated paths: <strong>aad-pod-identity</strong> (pre-Workload Identity Pod-to-Azure auth, deprecated 2024) and <strong>service principals</strong> for cluster identity (replaced by managed identities). If you inherit a cluster using either, the upgrade path is migration to Workload Identity + managed identity.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · human auth — kubelogin",
            h2="Human auth — kubelogin and disable local accounts",
            body_html="""    <p>When a human runs <code>kubectl</code> against an Entra-integrated AKS cluster, the auth flow is:</p>
    <ol>
      <li>kubectl reads <code>kubeconfig</code>; sees an exec credential plugin pointing at <code>kubelogin</code>.</li>
      <li>kubelogin opens a browser (or uses device code) to authenticate the user against Entra ID — Conditional Access policies fire here (MFA, device compliance, location, risk score).</li>
      <li>Entra returns an access token scoped to the AKS cluster.</li>
      <li>kubectl sends the token to kube-apiserver as a Bearer.</li>
      <li>apiserver validates the token signature against Entra; extracts the user / group claims.</li>
      <li>Authorization: either Azure RBAC for K8s (Entra-side) or in-cluster RBAC (RoleBinding/ClusterRoleBinding referencing the Entra principal).</li>
    </ol>
    <p><strong>Two kubeconfigs:</strong> <code>az aks get-credentials</code> returns an Entra-integrated config (default). <code>az aks get-credentials --admin</code> returns the cluster-admin local-account kubeconfig (bypasses Entra entirely — emergency-only). <strong>Disable local accounts</strong> (<code>--disable-local-accounts</code>) on production clusters so the admin kubeconfig path doesn\'t exist; emergencies use a designated break-glass Entra group.</p>
    <p><strong>Conditional Access for kubectl:</strong> the same Entra Conditional Access policies that gate the Azure Portal apply to <code>kubectl</code>. You can require MFA every kubectl session, deny kubectl from untrusted networks, require a compliant Intune-managed device, etc.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Workload Identity",
            h2="Pod auth — Workload Identity (federated credentials)",
            body_html="""    <p>Workload Identity lets a Pod call Azure services <em>without any secret stored in the cluster</em>. The flow:</p>
    <ol>
      <li>Cluster has an <strong>OIDC issuer URL</strong> (enabled with <code>--enable-oidc-issuer</code>).</li>
      <li>You create an Entra application (or use a user-assigned managed identity) and add a <strong>federated credential</strong> trusting <code>{cluster-OIDC}/serviceaccount/{namespace}/{sa-name}</code>.</li>
      <li>You annotate the K8s ServiceAccount: <code>azure.workload.identity/client-id: &lt;app-client-id&gt;</code>.</li>
      <li>Your Pod uses that ServiceAccount and is labelled <code>azure.workload.identity/use: \"true\"</code>.</li>
      <li>Workload Identity webhook injects two env vars + a projected ServiceAccount token into the Pod.</li>
      <li>Azure SDK in the Pod sees the env vars, exchanges the SA token for an Azure access token via Entra, calls Key Vault / ACR / Storage / Service Bus normally.</li>
    </ol>
    <p>The result: <strong>no secret in cluster, no secret to rotate, no secret to leak.</strong> Tokens are short-lived; the OIDC trust is revocable per federated credential.</p>
    <p><strong>Managed identity vs Entra app for Workload Identity:</strong> both work. <strong>User-assigned managed identity</strong> is preferred for new setups — its lifecycle is independent of the cluster, supports cross-RG / cross-subscription scenarios, and is targetable by Azure RBAC. <strong>Entra application</strong> is needed for cross-tenant trust.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · ACR + Key Vault",
            h2="ACR + Key Vault — the two adjacent services",
            body_html="""    <p><strong>ACR (Azure Container Registry)</strong> integration: <code>az aks update --attach-acr &lt;registry&gt;</code> grants the cluster\'s kubelet identity the <strong>AcrPull</strong> role on the registry. Pods can then pull <code>myregistry.azurecr.io/myapp:v1</code> without any imagePullSecret. <em>The kubelet identity is a separate user-assigned managed identity (not the cluster identity)</em> — created automatically per cluster, used only for ACR pulls.</p>
    <p>For private ACR (no public endpoint), use <strong>Private Link</strong> + a Private DNS zone bound to the cluster\'s VNet. Cluster-to-ACR traffic stays on the Microsoft backbone.</p>
    <p><strong>Key Vault integration</strong> via the <strong>Secrets Store CSI driver + Azure Key Vault provider</strong>: a SecretProviderClass declares which secrets/keys/certs to fetch; the driver mounts them into the Pod as files (and optionally syncs to a K8s Secret). Workload Identity authenticates the driver to Key Vault. <em>Auto-rotation: enable the rotation poller and set <code>rotationPollInterval</code></em> — secrets refresh in the volume, and (if synced) the K8s Secret updates so the Pod can pick up via volume reload or rolling restart.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A Pod can\'t fetch a secret from Key Vault — 401 Unauthorized. What\'s the most useful first check?",
            options=[
                ("Restart the Pod.", False),
                ("Verify the federated credential on the Entra app/managed identity points at <code>{cluster-OIDC-issuer}/serviceaccount/{ns}/{sa}</code> matching the Pod\'s ServiceAccount.", True),
                ("Open a network ticket — must be a firewall.", False),
            ],
            feedback="Workload Identity 401s are almost always a federated-credential mismatch — wrong subject, wrong issuer (e.g. cluster recreated and OIDC issuer URL changed), or the SA name typo. Check the trust before chasing network.",
        ),
    },
    before_after_before='<p>Pre-Workload-Identity AKS clusters used <strong>aad-pod-identity</strong> — a DaemonSet (NMI) intercepted IMDS calls from Pods and exchanged the Pod\'s assigned identity for tokens. It worked but was operationally fragile: the NMI DaemonSet had to run on every node, IMDS interception broke with some host networking modes, and the AzureIdentityBinding CRD was confusing. Plus pre-Entra-RBAC clusters used <strong>service principals</strong> with a long-lived secret stored as <code>aks-service-principal</code> — leaks, rotation pain, expiring creds taking down clusters.</p>',
    before_after_after='<p>Workload Identity replaces aad-pod-identity entirely: <em>no DaemonSet, no IMDS interception, no NMI</em> — just a webhook that injects env vars + a projected SA token into the Pod, and a federated credential on the Entra side. Token never touches disk. Same Pod code (Azure SDK) just works. <strong>Managed identity</strong> replaces service-principal for cluster identity: Azure rotates the credential automatically; you never see it. Combined with Azure RBAC for K8s + Conditional Access, the human-and-Pod identity story finally feels coherent.</p>',
    before_after_caption='<p class="ba-caption"><em>aad-pod-identity is deprecated; new clusters must use Workload Identity. Service-principal AKS clusters must migrate to managed identity.</em></p>',
    analogy_intro_html='''<p>The <strong>Registrar\'s Office</strong> sits in the middle of K-Campus. Everyone — Faculty, students, contractors, robots — must check in at the Registrar before they\'re allowed into any building. The Registrar is <strong>Entra ID</strong>: the single source of truth for who you are.</p>
    <p>There are <strong>two windows</strong> at the Registrar. Window 1 (<strong>Visitor Badges</strong>): humans show up with their photo ID; the Registrar checks the campus database, runs Conditional Access checks (\"are you on a managed device? did you swipe MFA?\"), and prints a badge that says \"Allowed in Building B for the next 8 hours.\" That badge is the kubelogin token.</p>
    <p>Window 2 (<strong>Worker Permits</strong>): a robot worker (a Pod) shows up needing access to the Library (Key Vault). It doesn\'t carry an ID — instead it shows the Registrar a sealed envelope (the projected ServiceAccount token) issued by its home department (the OIDC issuer). The Registrar checks the federated credential (\"yes, this department\'s envelopes are trusted to vouch for workers in <em>that</em> service-account slot\"), prints a Worker Permit (Azure access token), and the robot walks to the Library.</p>
    <p>The deprecated old way: every robot used to carry a permanent badge stapled to its chest (a service-principal secret). Robots lost badges; badges expired; replacing them was a nightmare. Workload Identity is \"no permanent badge, just a sealed envelope you generate fresh every time.\"</p>''',
    translation_rows=[
        ("The Registrar", "Microsoft Entra ID (formerly Azure AD)"),
        ("Visitor Badge window", "kubelogin → kube-apiserver token"),
        ("Worker Permit window", "Workload Identity → Azure access token"),
        ("Conditional Access checks", "MFA, device compliance, location, risk"),
        ("Sealed envelope from a department", "Projected ServiceAccount token (OIDC)"),
        ("Federated credential", "Trust between Entra app/MI and the OIDC issuer + SA"),
        ("Permanent stapled badge (deprecated)", "Service principal secret"),
        ("Worker Permit valid for X hours", "Azure access token TTL (~1h, refreshed)"),
        ("Two-window separation", "Surface 1 (human → cluster) vs Surface 2 (Pod → Azure)"),
        ("Disabled side door", "<code>--disable-local-accounts</code> kills bypass kubeconfig"),
        ("Break-glass key in the Director\'s safe", "Designated Entra Break-Glass group with cluster-admin"),
    ],
    analogy_stops="The Registrar metaphor implies one centralised authority. In reality Entra ID is replicated globally and tokens are validated cryptographically — no per-request round trip to a single Registrar.",
    eli5="There\'s one office on campus that knows everybody. Before you go into any building, you stop there and they print you a paper badge that says where you can go. Robots have a different paper called a Worker Permit — they get it the same way every time, instead of carrying a key around their neck that could fall off.",
    eli10="AKS auth has two surfaces. Humans authenticate to <code>kube-apiserver</code> via Entra ID + kubelogin (Conditional Access policies fire — MFA, device, location), authorize via Azure RBAC for K8s (preferred) or in-cluster RBAC. Pods authenticate to Azure services via <strong>Workload Identity</strong>: cluster has an OIDC issuer, ServiceAccount is annotated with a client ID, federated credential on an Entra app/MI trusts that SA, webhook injects an SA token + env vars into the Pod, Azure SDK exchanges the SA token for an access token via Entra. <strong>No secrets stored anywhere.</strong> Disable local accounts; use managed identities not service principals; aad-pod-identity is dead.",
    scenarios=[
        Scenario(
            name="Bank — Conditional Access + break-glass Entra group",
            body="A bank requires every <code>kubectl</code> session against prod to require: a compliant Intune device, MFA every 8 hours, only from corporate VPN egress IPs. They configure these as Conditional Access policies on the AKS cluster\'s Entra application. <code>--disable-local-accounts</code> removes the admin kubeconfig escape hatch. A break-glass Entra group with cluster-admin role exists for emergencies; membership is monitored in Sentinel. <em>One bypass attempt = SOC ticket.</em>",
        ),
        Scenario(
            name="Migration — aad-pod-identity → Workload Identity in 4 sprints",
            body="Pre-existing AKS cluster uses aad-pod-identity for ~30 microservices. Engineering team migrates per-service across 4 sprints: enable OIDC issuer + Workload Identity webhook on the cluster, create user-assigned MIs per service (Bicep modules), add federated credentials, annotate ServiceAccounts, label Pods, drop aad-pod-identity binding. <em>No code changes — Azure SDK auto-detects the credential source via env vars.</em> aad-pod-identity uninstalled at sprint 5.",
        ),
        Scenario(
            name="ML team — Workload Identity for Storage + Key Vault",
            body="An ML training Pod needs read on a 200-TB blob container and three secrets from Key Vault. Single user-assigned MI per training job; federated credential to the job\'s SA; MI granted Storage Blob Data Reader on the container + Key Vault Secrets User on three secrets. Pod uses default Azure SDK chain. <em>Job logs show no credentials, only MI client ID; if the job leaks logs, no auth material is exposed.</em>",
        ),
        Scenario(
            name="Multi-tenant SaaS — per-tenant federated credential",
            body="A SaaS where each tenant\'s workload runs in its own namespace with its own ServiceAccount. One Entra app per tenant; one federated credential per tenant\'s SA. Tenant A\'s Pod can never get Tenant B\'s tokens — the SA subject doesn\'t match. <em>Tenant isolation enforced at the federated-credential layer, not just RBAC.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Workload Identity is just aad-pod-identity rebranded.\"",
            truth="Different architecture. aad-pod-identity ran an NMI DaemonSet that intercepted IMDS calls and translated them to Azure tokens. Workload Identity uses an admission webhook + projected ServiceAccount tokens + OIDC federated credentials — <em>no DaemonSet, no IMDS interception, no NMI</em>. aad-pod-identity is deprecated; new clusters cannot install it.",
        ),
        Misconception(
            myth="\"Azure RBAC for K8s and Kubernetes RBAC are the same thing.\"",
            truth="<strong>Kubernetes RBAC</strong> = Role/ClusterRole/RoleBinding objects in the cluster, evaluated by kube-apiserver against the user\'s Entra principal. <strong>Azure RBAC for Kubernetes Authorization</strong> = Azure-side roles (e.g. <em>Azure Kubernetes Service RBAC Reader</em>) assigned at cluster/namespace scope in Entra, evaluated by an apiserver auth webhook talking to Azure. They can coexist; Azure RBAC for K8s is the modern path for Entra-integrated clusters.",
        ),
        Misconception(
            myth="\"<code>--admin</code> kubeconfig is fine for daily use.\"",
            truth="The <code>--admin</code> kubeconfig is the local cluster-admin account — bypasses Entra entirely, has no Conditional Access, no MFA, no audit trail beyond raw apiserver logs. On production clusters it should be disabled (<code>--disable-local-accounts</code>) and only re-enabled for emergencies. Daily use must go through Entra-integrated kubeconfig with kubelogin.",
        ),
    ],
    flashcards=[
        Flashcard(front="Two AKS identity surfaces — name them.", back="<strong>Surface 1 — human → cluster</strong>: Entra ID auth + Azure RBAC for K8s (or in-cluster RBAC) auth. <strong>Surface 2 — Pod → Azure service</strong>: Workload Identity (federated credential, OIDC, projected SA token) → Entra → Azure access token."),
        Flashcard(front="What does kubelogin do?", back="kubectl exec credential plugin that handles the Entra ID auth flow: opens a browser (or device code), authenticates the user against Entra, fires Conditional Access policies (MFA / device / location), returns an access token to kubectl. apiserver validates the token and authorises via Azure RBAC for K8s or in-cluster RBAC."),
        Flashcard(front="Workload Identity in five steps?", back="1) Enable cluster OIDC issuer. 2) Create Entra app or user-assigned MI; add federated credential trusting <code>{OIDC}/serviceaccount/{ns}/{sa}</code>. 3) Annotate SA with the client-id. 4) Label Pod with <code>azure.workload.identity/use=true</code>. 5) Pod uses Azure SDK; webhook injects env vars + projected SA token; SDK exchanges token via Entra → Azure access token."),
        Flashcard(front="What replaces deprecated aad-pod-identity?", back="<strong>Workload Identity</strong> — no DaemonSet, no IMDS interception, no NMI. Uses admission webhook + projected SA tokens + OIDC federated credentials. aad-pod-identity went deprecated 2024; cannot be installed on new clusters."),
        Flashcard(front="Azure RBAC for K8s vs Kubernetes RBAC?", back="Both authorize. <strong>K8s RBAC</strong> = in-cluster Role/RoleBinding objects, evaluated by kube-apiserver. <strong>Azure RBAC for K8s</strong> = Entra-side Azure roles (Azure Kubernetes Service RBAC Reader/Writer/Admin/Cluster Admin) assigned at cluster or namespace scope. Modern AKS prefers Azure RBAC for K8s for Entra-integrated clusters."),
        Flashcard(front="ACR pull integration — what does <code>--attach-acr</code> do?", back="Grants the cluster\'s <strong>kubelet identity</strong> (a separate user-assigned MI) the <strong>AcrPull</strong> role on the specified ACR. Pods can then pull <code>registry.azurecr.io/img:tag</code> without any imagePullSecret."),
        Flashcard(front="What does <code>--disable-local-accounts</code> do and why use it?", back="Removes the cluster-admin local account. <code>az aks get-credentials --admin</code> stops working. Forces all auth through Entra ID — Conditional Access, MFA, device checks all apply. Production clusters should use this; emergencies use a designated break-glass Entra group."),
        Flashcard(front="Secrets Store CSI + Key Vault — what gets mounted and how?", back="A <code>SecretProviderClass</code> declares which Key Vault secrets/keys/certs to fetch. The Secrets Store CSI driver (with the Azure Key Vault provider) authenticates to Key Vault via Workload Identity and mounts them as files in the Pod. Optional: sync to a K8s Secret. Auto-rotation polls Key Vault on a schedule and updates the volume."),
    ],
    quizzes=[
        Quiz(
            prompt="A new AKS cluster was created two days ago. A Pod that previously worked (Workload Identity → Key Vault) now returns 401 Unauthorized. The Pod\'s ServiceAccount, the federated credential subject, and the Key Vault access policy all look identical to the production cluster. What\'s the likely cause?",
            answer="<strong>The cluster\'s OIDC issuer URL changed.</strong> Each AKS cluster has a unique OIDC issuer. The federated credential\'s <code>issuer</code> field still points at the <em>old</em> cluster\'s OIDC URL — so tokens issued by the new cluster fail trust validation at Entra. Fix: update the federated credential\'s issuer to the new cluster\'s URL (find via <code>az aks show ... --query oidcIssuerProfile.issuerUrl</code>).",
        ),
        Quiz(
            prompt="The platform team enables Azure RBAC for K8s on a cluster that already has a dozen K8s RoleBindings managed by Helm. What happens to those RoleBindings?",
            answer="They keep working. Azure RBAC for K8s is <em>additive</em> — apiserver consults Azure RBAC <em>and</em> in-cluster RBAC; permission grants from either side apply. Existing RoleBindings continue to authorize. Migration plan: move bindings into Azure roles over time so all auth is one source of truth, but the cutover doesn\'t have to be atomic.",
        ),
        Quiz(
            prompt="An on-call engineer is locked out — Conditional Access requires Intune-compliant devices and her laptop is in for repair. Production AKS cluster has <code>--disable-local-accounts</code>. How does she get in to fix the outage?",
            answer="<strong>Break-glass Entra group.</strong> Production clusters with disabled local accounts always have a designated Entra security group (e.g. <em>aks-prod-breakglass</em>) bound to <em>Azure Kubernetes Service RBAC Cluster Admin</em>. Membership is empty in steady state and monitored in Sentinel. The on-call engineer (or their manager) requests just-in-time membership via PIM — gets cluster-admin for 30 minutes, MFA on a phone (no Intune device required), fixes the outage, membership auto-expires, SOC reviews the audit trail.",
            cyoa=True,
            cyoa_tag="how the on-call got in without a laptop",
        ),
    ],
    glossary=[
        GlossaryItem(name="Microsoft Entra ID", definition="Microsoft\'s cloud identity service (formerly Azure AD). Source of truth for user and application identity."),
        GlossaryItem(name="Workload Identity", definition="AKS feature: federate a K8s ServiceAccount with an Entra app/MI via OIDC; Pods get Azure access tokens via Entra without storing secrets."),
        GlossaryItem(name="OIDC issuer", definition="Each AKS cluster exposes a unique OIDC discovery URL. Federated credentials trust this URL + a specific SA subject."),
        GlossaryItem(name="Federated credential", definition="Trust statement on an Entra app or MI: \"tokens from issuer X with subject Y are accepted as proof of identity.\""),
        GlossaryItem(name="Managed identity", definition="Azure-managed credential. <strong>System-assigned</strong> = lifecycle tied to parent. <strong>User-assigned</strong> = independent lifecycle, reusable, recommended."),
        GlossaryItem(name="Service principal", definition="Legacy AKS identity model. Long-lived secret you manage. Replaced by managed identities."),
        GlossaryItem(name="kubelogin", definition="kubectl exec credential plugin that performs the Entra auth flow against the AKS cluster."),
        GlossaryItem(name="Azure RBAC for Kubernetes Authorization", definition="Azure-side roles assigned to Entra principals at cluster/namespace scope, evaluated by an apiserver auth webhook."),
        GlossaryItem(name="K8s RBAC", definition="In-cluster Role/RoleBinding objects, evaluated by kube-apiserver."),
        GlossaryItem(name="Conditional Access", definition="Entra ID policy engine — gate access on MFA, device compliance, location, risk. Applies to kubectl when the cluster is Entra-integrated."),
        GlossaryItem(name="aad-pod-identity", definition="Deprecated pre-Workload-Identity Pod-to-Azure auth. NMI DaemonSet, IMDS interception. Cannot be installed on new clusters."),
        GlossaryItem(name="Secrets Store CSI driver", definition="Mount external secret stores as Pod volumes. Azure Key Vault provider authenticates via Workload Identity."),
    ],
    recap_lead="Two surfaces: humans via Entra+kubelogin+Azure RBAC for K8s; Pods via Workload Identity. Local accounts disabled, break-glass Entra group, ACR + Key Vault wired in cleanly.",
    recap_next='<strong>Next — A3: AKS Networking.</strong> Azure CNI vs Azure CNI Overlay vs CNI by Cilium vs BYO; private clusters; API VNet integration; AGIC vs Application Gateway for Containers (AGC); Web App Routing add-on; SNAT exhaustion; NetworkPolicy options.',
)
