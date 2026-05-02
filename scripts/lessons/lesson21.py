from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Permit Office credentials counter: a clerk hands out a passport (ServiceAccount) and a stamped travel pass (projected token), while behind a partition cert-manager prints time-limited certificates from a PKI press.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">PERMIT OFFICE · IDENTITY &amp; CERTIFICATES BUREAU</text>
  <!-- Passport (ServiceAccount) -->
  <g transform="translate(40,55)">
    <rect width="86" height="100" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="43" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">PERMIT</text>
    <text x="43" y="32" text-anchor="middle" font-size="6" fill="#FBF1D6">PERMIT</text>
    <circle cx="43" cy="56" r="14" fill="#FBF1D6" stroke="#FBF7F0" stroke-width="1"/>
    <circle cx="40" cy="54" r="1.2" fill="#2A2520"/><circle cx="46" cy="54" r="1.2" fill="#2A2520"/>
    <path d="M 39 60 Q 43 62 47 60" stroke="#2A2520" stroke-width="1" fill="none"/>
    <text x="43" y="86" text-anchor="middle" font-size="8" font-weight="700" fill="#FBF1D6">app-x</text>
    <text x="43" y="118" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">ServiceAccount</text>
    <text x="43" y="131" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">the app's identity</text>
  </g>
  <!-- Token (travel pass) -->
  <g transform="translate(160,80)">
    <rect width="120" height="40" rx="4" fill="#FBF1D6" stroke="#8B5A00" stroke-width="1.5"/>
    <text x="60" y="14" text-anchor="middle" font-size="7" font-weight="700" fill="#8B5A00">PROJECTED TOKEN</text>
    <line x1="6" y1="18" x2="114" y2="18" stroke="#8B5A00" stroke-width="0.5"/>
    <text x="6" y="27" font-size="6" fill="#5A4F45">aud: api.cluster</text>
    <text x="6" y="34" font-size="6" fill="#5A4F45">exp: 1h</text>
    <text x="60" y="34" text-anchor="middle" font-size="6" font-weight="700" fill="#A04832">SHORT-LIVED</text>
    <text x="60" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">JWT · Bound</text>
    <text x="60" y="73" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">refreshed by kubelet</text>
  </g>
  <!-- cert-manager press -->
  <g transform="translate(310,40)">
    <rect width="160" height="120" rx="8" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <rect x="14" y="14" width="132" height="66" rx="3" fill="#5A4F45"/>
    <rect x="22" y="22" width="116" height="50" rx="2" fill="#FBF7F0"/>
    <line x1="32" y1="32" x2="128" y2="32" stroke="#9D9389" stroke-width="0.5"/>
    <line x1="32" y1="42" x2="128" y2="42" stroke="#9D9389" stroke-width="0.5"/>
    <line x1="32" y1="52" x2="128" y2="52" stroke="#9D9389" stroke-width="0.5"/>
    <line x1="32" y1="62" x2="100" y2="62" stroke="#9D9389" stroke-width="0.5"/>
    <circle cx="120" cy="62" r="6" fill="#A04832"/>
    <text x="120" y="65" text-anchor="middle" font-size="6" fill="#FFFFFF" font-weight="700">CA</text>
    <text x="80" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">cert-manager</text>
    <text x="80" y="111" text-anchor="middle" font-size="8" fill="#FBF1D6" font-style="italic">issues + rotates X.509</text>
  </g>
  <!-- PKI tree -->
  <g transform="translate(500,55)">
    <text x="75" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">CLUSTER PKI</text>
    <rect x="55" y="22" width="40" height="24" rx="3" fill="#3F4A5E"/>
    <text x="75" y="38" text-anchor="middle" font-size="8" font-weight="700" fill="#FBF1D6">cluster CA</text>
    <line x1="75" y1="46" x2="30" y2="68" stroke="#5A4F45" stroke-width="1.2"/>
    <line x1="75" y1="46" x2="75" y2="68" stroke="#5A4F45" stroke-width="1.2"/>
    <line x1="75" y1="46" x2="120" y2="68" stroke="#5A4F45" stroke-width="1.2"/>
    <rect x="6" y="68" width="48" height="22" rx="3" fill="#5A9F7A"/>
    <text x="30" y="82" text-anchor="middle" font-size="7" font-weight="700" fill="#FFFFFF">apiserver</text>
    <rect x="55" y="68" width="40" height="22" rx="3" fill="#A04832"/>
    <text x="75" y="82" text-anchor="middle" font-size="7" font-weight="700" fill="#FFFFFF">kubelet</text>
    <rect x="100" y="68" width="44" height="22" rx="3" fill="#E8B547"/>
    <text x="122" y="82" text-anchor="middle" font-size="7" font-weight="700" fill="#5A4F45">app TLS</text>
    <text x="75" y="115" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">all signed by the same root</text>
  </g>
  <text x="340" y="200" text-anchor="middle" font-size="11" fill="#3F4A5E" font-style="italic">Identity for Pods · short-lived tokens · automated cert rotation. None of this should be hand-rolled.</text>
</svg>"""

LESSON = LessonSpec(
    num="21",
    title_short="ServiceAccounts &amp; certs",
    title_full="ServiceAccounts & Certificates · Tokens, Projected JWTs, cert-manager, Cluster PKI",
    title_html="Lesson 21 — ServiceAccounts & Certificates · K-COM",
    module_eyebrow="Module 10 · Lesson 21 · workload identity and cluster PKI",
    hero_sub_html='Every Pod has an identity (its <strong>ServiceAccount</strong>) and a credential proving that identity (a <strong>token</strong>). Every TLS connection between cluster components is backed by a <strong>certificate</strong>. This lesson is about the <em>tokens</em> the cluster issues and the <em>PKI</em> that makes them trustable.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Pod was running fine for 18 months — until a Friday at 17:42 when its TLS connections to the API server start failing. Logs show <code>x509: certificate has expired</code>. The on-call engineer SSHs in, runs <code>openssl x509 -enddate</code>, and sees the cert expired today. Nobody on the team had ever rotated a certificate manually. Turns out kubeadm rotates kubelet certs but the team had also issued a long-lived service account token in 2024 (the old default), pinned in a Secret, never refreshed. The fix is moving to <strong>projected service account tokens</strong> (kubelet auto-refreshes them) and putting <strong>cert-manager</strong> in front of every TLS endpoint. This lesson is the toolkit.',
    stamp_html='Every Pod has a <strong>ServiceAccount</strong> (its workload identity). Modern clusters use <strong>projected, short-lived, audience-bound JWTs</strong> — <em>not</em> the legacy long-lived Secret tokens. For TLS certs (Ingress, webhooks, mTLS), use <strong>cert-manager</strong> — never hand-roll OpenSSL.',
    district_pin="kt-pin14",
    district_label="Permit Office — Identity Bureau",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Workload identity vs human identity",
            body_html="""    <p>Two kinds of identity in K8s. <strong>Users</strong> are humans (or external CI systems) authenticated through OIDC, certificates, or static tokens — they're <em>not</em> a K8s API object; they're a string the API server accepts. <strong>ServiceAccounts</strong> are workload identities — actual API objects in a namespace, used by Pods to talk to the API server (or to any other identity-aware service).</p>
    <p>Every Pod runs as a ServiceAccount. If you don't specify one, it's <code>default</code>. The kubelet projects a JWT into the Pod (under <code>/var/run/secrets/kubernetes.io/serviceaccount/token</code>); any process in the Pod can read it and use it as a Bearer token to talk to the API server.</p>
    <p>The big shift between K8s 1.21 and today: tokens are now <strong>short-lived (1h default), audience-bound (a JWT <code>aud</code> claim), and auto-refreshed</strong> by the kubelet. Pre-1.21, tokens were stored in long-lived Secrets and never expired — a leak was a permanent compromise. Modern clusters: a leaked token is useful for at most an hour.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The token model",
            h2="Projected vs legacy ServiceAccount tokens",
            body_html="""    <table class="data-table">
      <thead>
        <tr><th></th><th>Legacy (pre-1.24)</th><th>Projected / Bound (modern)</th></tr>
      </thead>
      <tbody>
        <tr><td>Lifetime</td><td>Forever</td><td>1 hour default; refreshed at 80%</td></tr>
        <tr><td>Storage</td><td>Long-lived <code>Secret</code> object</td><td>Read from kubelet's mount; never touches etcd</td></tr>
        <tr><td>Audience</td><td>Implicit (API server only)</td><td>Explicit <code>aud</code> claim</td></tr>
        <tr><td>On Pod delete</td><td>Token still valid</td><td>Token bound to Pod UID — invalid the moment Pod dies</td></tr>
        <tr><td>Created by</td><td>K8s auto-created a Secret per SA</td><td>You ask for one explicitly via <code>TokenRequest</code> API or volume projection</td></tr>
      </tbody>
    </table>
    <p style="margin-top:18px">Default behaviour in 1.24+: K8s no longer auto-creates a long-lived Secret per ServiceAccount. The Pod gets a projected token via the <code>serviceAccountToken</code> volume projection. <em>If you find a long-lived SA token Secret in a modern cluster, it was created intentionally — typically as an integration credential for an external system that can't refresh.</em></p>""",
        ),
        Section(
            eyebrow="Section 1.7 · The cluster's PKI",
            h2="Why every K8s component has a certificate",
            body_html="""    <p>Every TLS connection between cluster components — API server ↔ kubelet, kubelet ↔ apiserver, etcd ↔ etcd, controller-manager ↔ apiserver — is mTLS-authenticated with X.509 certificates. The default tooling (kubeadm, the major distros, the cloud-managed control planes) sets up a small PKI:</p>
    <ul>
      <li><strong>Cluster CA</strong> — the root that signs everything. Lives in <code>/etc/kubernetes/pki/ca.crt</code> on a kubeadm-managed control plane.</li>
      <li><strong>API server cert</strong> — signed by the CA; presented when clients talk to <code>kubernetes.default.svc</code>.</li>
      <li><strong>kubelet certs</strong> — one per node; signed by the CA via the <strong>kubelet-bootstrap</strong> flow at node join. Auto-rotated.</li>
      <li><strong>etcd peer + client certs</strong> — internal to etcd; signed by a separate etcd CA usually.</li>
      <li><strong>Front-proxy CA</strong> — separate CA used for aggregated API servers (extension API servers, metrics-server).</li>
    </ul>
    <p>For application-level TLS (Ingress endpoints, webhook configurations, app-to-app mTLS), don't extend the cluster CA — that's its job, not yours. Stand up <strong>cert-manager</strong> for app-level certs; it's a CRD-driven controller that integrates with Let's Encrypt, Vault, your cluster's CA, or any other ACME-compatible issuer.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The OIDC discovery endpoint at <code>/.well-known/openid-configuration</code> on the API server publishes the cluster's JWT verification keys. This is what lets external systems (AWS IAM Roles for Service Accounts, GCP Workload Identity Federation, Vault) <em>verify</em> a projected SA token without contacting the API server. The token itself is a standards-compliant OIDC JWT — that's the whole basis for cluster-to-cloud workload identity.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · cert-manager — the practical tool",
            h2="Three CRDs you actually use",
            body_html="""    <div class="role-grid">
      <div class="role r1">
        <span class="role-icon">📜</span>
        <h3 class="role-name">Issuer / ClusterIssuer</h3>
        <p class="role-tag">where certs come from</p>
        <p class="role-desc">Defines a CA source: Let's Encrypt (HTTP-01 or DNS-01 ACME), Vault PKI, an internal CA, or a self-signed root. <code>Issuer</code> is namespace-scoped; <code>ClusterIssuer</code> is cluster-wide.</p>
        <p class="role-who">Set up once per environment.</p>
      </div>
      <div class="role r2">
        <span class="role-icon">🪪</span>
        <h3 class="role-name">Certificate</h3>
        <p class="role-tag">a specific cert request</p>
        <p class="role-desc">"Issue a cert for these DNS names, valid for X days, store the result in this Secret named Y." cert-manager renews it before expiry (default at 2/3 of lifetime).</p>
        <p class="role-who">One per app / Ingress / mTLS endpoint.</p>
      </div>
      <div class="role r3">
        <span class="role-icon">🎫</span>
        <h3 class="role-name">CertificateRequest / Order</h3>
        <p class="role-tag">internal accounting</p>
        <p class="role-desc">CRs and Orders are intermediate objects cert-manager creates while talking to the issuer. You don't write them; they're useful for debugging stuck issuance.</p>
        <p class="role-who">Read-only for users.</p>
      </div>
    </div>
    <p style="margin-top:18px">A typical Ingress with TLS: define a <code>ClusterIssuer</code> for Let's Encrypt prod, then add the <code>cert-manager.io/cluster-issuer</code> annotation on your Ingress. cert-manager creates the <code>Certificate</code>, runs the ACME flow, stores the result in a <code>kubernetes.io/tls</code> Secret, and the Ingress controller picks it up. Renewals happen automatically. Total Ops touch: zero after setup.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A team has a Pod with no <code>serviceAccountName</code> set. Which identity does it run as?",
            options=[
                ("a) <code>system:anonymous</code> — no identity at all", False),
                ("b) The <code>default</code> ServiceAccount in the Pod's namespace, automatically", True),
                ("c) A randomly generated identity per Pod", False),
            ],
            feedback="<strong>Answer: b.</strong> Every namespace gets a <code>default</code> ServiceAccount auto-created. Pods that don't specify one inherit it. This is convenient but means a default SA's RBAC bindings affect <em>every</em> Pod in the namespace — keep <code>default</code> minimally permissioned and create explicit SAs per workload.",
        ),
    },
    before_after_before='<p>Pre-1.24 era: every ServiceAccount had a permanent <code>Secret</code> token. Leak = permanent compromise. Cluster certs renewed by writing a runbook and praying a junior engineer remembered to run it before the cert expired. Application TLS = OpenSSL commands in a wiki page, last updated three years ago.</p>',
    before_after_after='<p>Modern cluster: projected tokens are short-lived (1h), audience-bound, auto-refreshed. Cluster control-plane certs auto-rotated via kubeadm or the managed control plane. Application TLS via <code>cert-manager</code> + a <code>ClusterIssuer</code>; you write a <code>Certificate</code> and forget about it forever. The runbook is gone — replaced by declarative resources.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">The single most under-appreciated migration in K8s history was bound service account tokens. Pre-2022 most clusters had thousands of permanent credentials lying around. Post-2024, virtually none.</p>',
    analogy_intro_html='<p>The Permit Office issues two kinds of paperwork. The <strong>passport</strong> (ServiceAccount) is the identity itself: it says "this is app-x, vouched for by the city." The <strong>travel pass</strong> (token) is what app-x actually presents at every checkpoint: it\'s a stamped, time-limited document the kid courier carries in their pocket. Old K-Town used to issue passes that never expired — a lost pass meant someone could impersonate you forever. New K-Town issues passes that expire in an hour and are auto-refreshed by the courier office (the kubelet).</p><p>Behind another counter: the <strong>certificate press</strong>. cert-manager runs the press: it talks to a recognised authority (Let\'s Encrypt, Vault, the city CA), gets a sealed certificate, hands it to whoever asked, and pre-emptively reprints it before it expires. Nobody hand-cuts certificates anymore in modern K-Town.</p>',
    translation_rows=[
        ("The passport with the holder's photo", "<code>ServiceAccount</code> object"),
        ("The stamped travel pass", "Projected JWT (1h, audience-bound, refreshed by kubelet)"),
        ("Travel passes that never expired (old)", "Legacy long-lived SA token Secrets (pre-1.24 default)"),
        ("The city's seal of authenticity", "Cluster CA cert (signs API server, kubelet, etcd certs)"),
        ("The certificate press", "cert-manager controller"),
        ("A standing relationship with a cert authority", "<code>ClusterIssuer</code> (e.g., Let's Encrypt, Vault PKI)"),
        ("Today's certificate request slip", "<code>Certificate</code> object"),
        ("The seal-checking machine at the customs line", "API server's TLS chain validation"),
    ],
    analogy_stops="The analogy stops here: real K8s tokens are JWTs, signed cryptographically — the whole stack of trust depends on whether the cluster's signing key is protected. \"The city CA\" is one private key on disk; lose it and the whole metaphor collapses.",
    eli5='Every Pod gets a name badge (ServiceAccount) and a paper hall pass (the token). The hall pass expires in an hour and the front desk (kubelet) gives you a new one before it runs out. Long ago hall passes never expired and that was a problem.',
    eli10="Every Pod runs as a <code>ServiceAccount</code> — a workload identity. The kubelet projects a short-lived (1h), audience-bound JWT into the Pod at <code>/var/run/secrets/kubernetes.io/serviceaccount/token</code>. The Pod presents it as a Bearer token. Lost or leaked = useful for at most an hour. Cluster components (apiserver, kubelet, etcd) authenticate to each other with X.509 certs from a small per-cluster PKI. For application-layer TLS, run <code>cert-manager</code> + a <code>ClusterIssuer</code> and let it handle issuance + rotation declaratively.",
    scenarios=[
        Scenario(name="A SaaS using IAM Roles for ServiceAccounts (IRSA) on EKS", body="The Pod's projected JWT has audience <code>sts.amazonaws.com</code>. STS verifies it by hitting EKS's OIDC endpoint, returns AWS credentials. The Pod authenticates to AWS without ever holding an AWS access key. Rotation: kubelet refreshes the JWT every 50 minutes; AWS creds get re-issued in turn."),
        Scenario(name="A bank running mTLS between every microservice", body="cert-manager has a Vault PKI ClusterIssuer. Every Deployment has a Certificate sidecar that issues a 24h cert. Service mesh (Linkerd, in this case) consumes the cert. Hard mTLS everywhere. Vault rotates the intermediate CA quarterly; cert-manager re-issues on the next renewal."),
        Scenario(name="A startup with a Let's Encrypt setup that took 5 minutes", body="Install cert-manager → apply a <code>ClusterIssuer</code> for Let's Encrypt → add <code>cert-manager.io/cluster-issuer: letsencrypt-prod</code> annotation on the Ingress. cert-manager runs the HTTP-01 challenge, gets a cert, stores it in a Secret, the Ingress controller picks it up. Renewals are silent."),
        Scenario(name="A team that audited their old long-lived tokens", body="Found 47 ServiceAccount Secrets created pre-1.21 that nobody remembered. Half were unused; the other half belonged to integrations they could migrate to bound tokens. The cleanup deleted 38 of them, replaced 9 with bound tokens or workload-identity flows. Surface area for credential theft dropped by an order of magnitude."),
    ],
    misconceptions=[
        Misconception(myth="<code>kubectl create token</code> is just for testing.", truth="It's the recommended way to mint a one-off token for an external integration in 2026. The legacy way (create a Secret of type <code>kubernetes.io/service-account-token</code>) still works but is discouraged. <code>kubectl create token sa-name --duration=1h --audience=foo</code> issues a bound token via the TokenRequest API."),
        Misconception(myth="cert-manager can manage the cluster's control-plane certs.", truth="No. Control-plane PKI (apiserver, kubelet, etcd) is managed by kubeadm, the distro (kops, k3s, RKE2), or the managed cloud control plane. cert-manager is for <em>application-layer</em> certs (Ingress, webhooks, mTLS). Mixing the two will break things."),
        Misconception(myth="The default ServiceAccount is fine.", truth="It's fine until you grant it a Role and forget that <em>every</em> Pod in that namespace inherits it. Treat <code>default</code> as no-permissions; create per-workload SAs and bind RBAC to them. Pod Security Admission can enforce \"every Pod must specify a non-default SA.\""),
    ],
    flashcards=[
        Flashcard(front="ServiceAccount vs User?", back="ServiceAccount = workload identity, namespaced API object, used by Pods. User = human (or external system) identity, not a K8s object — just a string the API server's authenticator returns from OIDC/cert/token."),
        Flashcard(front="What's in a projected SA token?", back="A signed JWT with claims: <code>iss</code> (cluster URL), <code>sub</code> (the SA), <code>aud</code> (target audience), <code>exp</code> (1h), and Pod / Node binding info. kubelet refreshes at 80% lifetime."),
        Flashcard(front="Why are tokens \"bound\"?", back="Bound to a specific Pod's UID. The moment the Pod is deleted, the token is invalid for API server auth. Reduces blast radius of leaked credentials."),
        Flashcard(front="What is IRSA / Workload Identity?", back="AWS IRSA + GCP Workload Identity + Azure Workload Identity Federation: cluster's projected JWT is verified by the cloud's STS using K8s's OIDC discovery endpoint. Pod gets cloud credentials without static keys."),
        Flashcard(front="Cluster CA vs front-proxy CA?", back="Cluster CA: signs API server, kubelet, controller-manager, scheduler, etcd certs (typical kubeadm setup uses one root). Front-proxy CA: separate root used by aggregated/extension API servers (metrics-server, custom AAs)."),
        Flashcard(front="cert-manager: Issuer vs ClusterIssuer?", back="Issuer = namespace-scoped (one per team/env). ClusterIssuer = cluster-wide. Same fields. Use ClusterIssuer when one cert source serves many namespaces (e.g., Let's Encrypt prod)."),
        Flashcard(front="HTTP-01 vs DNS-01 ACME?", back="HTTP-01: challenge served from a temporary URL on the host (cert-manager spins up a Pod + Ingress rule). DNS-01: challenge served as a TXT record (cert-manager updates DNS via a provider). DNS-01 supports wildcards; HTTP-01 doesn't."),
        Flashcard(front="When should you NOT use cert-manager?", back="For control-plane PKI — those are managed by kubeadm/distro/cloud control plane. cert-manager is application-layer."),
    ],
    quizzes=[
        Quiz(prompt="A Pod's token works fine when the Pod is running, but a CronJob script tries to capture the token and use it later. The captured token is rejected after a few minutes. Why?", answer="Bound tokens. The token includes the Pod's UID and node binding; the API server validates these on every request. When the Pod terminates (or even just rolls), the binding becomes invalid. <strong>Fix:</strong> use the TokenRequest API directly to mint a longer-lived (but still bounded) token if the use case is legitimate, or restructure so the work happens inside the Pod's lifetime. There's no \"token forever\" option in modern K8s, by design."),
        Quiz(prompt="A team needs to migrate an old integration from a static <code>kubernetes.io/service-account-token</code> Secret to bound tokens. The integration is a third-party SaaS that needs to authenticate to the cluster's API server. What's the modern approach?", answer="Three options ranked best-first: (1) <strong>OIDC federation</strong>: configure the SaaS to trust the cluster's OIDC endpoint and present projected JWTs from a sidecar workload — zero static credentials. (2) <strong>kubectl create token</strong>: issue a longer-lived (e.g., 24h) bound token on a refresh schedule via a CronJob; the SaaS gets rotating creds. (3) <strong>Long-lived SA Secret</strong>: only if (1) and (2) are impossible — and ensure the Secret is in a tightly-RBAC'd namespace and rotated manually. Most modern SaaS integrations support (1) or (2)."),
        Quiz(prompt="On Friday at 5 PM your Ingress starts returning <code>x509: certificate has expired</code>. cert-manager is installed but the Certificate object hasn't renewed. <strong>Click for the diagnostic walk. ▼</strong>", cyoa=True, cyoa_tag="the diagnostic walk", answer="Check in this order: (1) <code>kubectl describe certificate</code> — look at the <code>Status.Conditions</code> and <code>Events</code>. The most common cause is <code>Renewal Failed</code> with an issuer error. (2) <code>kubectl describe issuer / clusterissuer</code> — is the issuer reachable? Let's Encrypt rate-limited? Vault token expired? DNS-01 provider misconfigured? (3) <code>kubectl get certificaterequest -A</code> + describe the most recent — what error is the issuer returning? (4) Common causes: ACME rate limit hit (5 certs/week per registered domain), DNS provider creds rotated, Vault PKI role expired, ClusterIssuer's signing CA actually expired (this is the big one for self-signed roots — they're not magic, they expire too). <strong>Lesson:</strong> set up an alert on <code>cert-manager.io/certificate-expiry</code> with 14-day lead time. Do not learn this on Friday at 5 PM."),
    ],
    glossary=[
        GlossaryItem(name="ServiceAccount (SA)", definition="Namespaced API object representing a workload identity. Every Pod runs as one (defaults to <code>default</code>)."),
        GlossaryItem(name="Bound / projected token", definition="Short-lived (1h), audience-bound JWT issued by the API server's TokenRequest API and projected into Pods by the kubelet."),
        GlossaryItem(name="TokenRequest API", definition="API server endpoint for minting bound tokens. Used by kubelet, also by <code>kubectl create token</code>."),
        GlossaryItem(name="OIDC discovery endpoint", definition="<code>/.well-known/openid-configuration</code> on the apiserver. Publishes verification keys so external systems can validate cluster JWTs."),
        GlossaryItem(name="IRSA / Workload Identity", definition="Cloud-side flow that exchanges a projected K8s JWT for cloud credentials. AWS, GCP, Azure all support it."),
        GlossaryItem(name="Cluster CA", definition="Root certificate authority signing the cluster's control-plane certs. Lives at <code>/etc/kubernetes/pki/ca.crt</code> on kubeadm clusters."),
        GlossaryItem(name="Front-proxy CA", definition="Separate CA for aggregated API servers (metrics-server, extension APIs)."),
        GlossaryItem(name="cert-manager", definition="K8s-native CRD-driven controller for issuing and rotating X.509 certs. De-facto standard for app-layer TLS."),
        GlossaryItem(name="Issuer / ClusterIssuer", definition="cert-manager CRD pointing at a cert source (Let's Encrypt, Vault PKI, internal CA)."),
        GlossaryItem(name="Certificate (cert-manager CRD)", definition="\"Issue a cert for these DNSNames, store in Secret X, renew before expiry.\""),
        GlossaryItem(name="ACME HTTP-01 / DNS-01", definition="Two challenge methods Let's Encrypt uses to verify domain control. cert-manager automates both."),
        GlossaryItem(name="kubernetes.io/tls", definition="Built-in Secret type carrying a TLS cert + key. Consumed by Ingresses, Gateways, webhooks."),
    ],
    recap_lead="Pods get an identity (ServiceAccount) and a short-lived, bound token (projected JWT). Cluster components trust each other via a small PKI. App-level TLS is cert-manager + a ClusterIssuer; never hand-roll OpenSSL.",
    recap_next="<strong>Next — Lesson 22: Scheduling Part 1.</strong> How K8s decides which node a Pod lands on. Affinity and anti-affinity, taints and tolerations, topology-spread constraints. Dispatch Office routes the trucks.",
)
