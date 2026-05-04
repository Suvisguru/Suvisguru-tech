"""K-ADV-SEC S1 — Threat modeling, zero-trust, multi-tenant isolation."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="K-Citadel — outer perimeter, identity gate, tenant zone, vault.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Threat Map Room · K-Citadel — four concentric layers, never one wall</text>
  <rect x="40" y="70" width="170" height="120" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Outer perimeter</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">untrusted internet</text>
  <text x="125" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">DDoS / WAF / public LB</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">+ Ingress / Gateway</text>
  <text x="125" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">first wall</text>
  <rect x="225" y="70" width="170" height="120" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Identity gate</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">OIDC + mTLS + SA tokens</text>
  <text x="310" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">RBAC verb-level authz</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">never trust, always check</text>
  <text x="310" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">authenticate every step</text>
  <rect x="410" y="70" width="170" height="120" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Tenant zone</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">Namespace + RBAC</text>
  <text x="495" y="124" text-anchor="middle" font-size="9" fill="#1F2433">+ NetworkPolicy + PSA</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#1F2433">+ ResourceQuota + LimitRange</text>
  <text x="495" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">soft / hard multi-tenant</text>
  <rect x="595" y="70" width="125" height="120" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Vault + audit</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Secrets / KMS</text>
  <text x="657" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">audit.k8s.io</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">SIEM pipeline</text>
  <text x="657" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">deepest stronghold</text>
</svg>"""


LESSON = LessonSpec(
    num="01",
    title_short="threat modeling + zero-trust + tenancy",
    title_full="S1 · Threat Modeling, Zero-Trust, Multi-Tenant Isolation",
    title_html="K-ADV-SEC S1 · Threat Modeling + Zero-Trust + Tenancy",
    module_eyebrow="Module S1 · the Threat Map Room — four concentric layers, never one wall",
    hero_sub_html='Security architecture for K8s starts with <strong>threat modeling</strong> (STRIDE — Spoofing / Tampering / Repudiation / Info disclosure / DoS / Elevation of privilege), the <strong>zero-trust</strong> stance (no implicit trust at any boundary; every step authenticates + authorises), and the <strong>multi-tenant isolation</strong> design (soft = same cluster + namespace boundaries; hard = vCluster / virtual cluster or one cluster per tenant). Four concentric layers — perimeter, identity, tenant zone, vault — each catches different failure modes.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A web app on the cluster was compromised through a known CVE in an old base image. The attacker spawned a shell, then exec\'d into another Pod via the cluster\'s ServiceAccount token mounted by default. <em>The cluster was a single trust zone — once inside the perimeter, lateral movement was free.</em> Today\'s lesson: design defence-in-depth so a perimeter compromise stops at the next gate.",
    stamp_html="<strong>Threat-model first; zero-trust everywhere; multi-tenant isolation by design. Four layers: perimeter, identity, tenant zone, vault. Each layer authenticates + authorises independently. A breach at one layer must not become a breach of the next.</strong>",
    district_pin="ksec-bastion01",
    district_label="Threat Map Room",
    sections=[
        Section(
            eyebrow="Section 1.1 · threat modeling for K8s",
            h2="STRIDE applied to a Kubernetes cluster",
            body_html="""    <p><strong>STRIDE</strong> walks every component asking what could go wrong. For a K8s cluster:</p>
    <ul>
      <li><strong>Spoofing</strong>: someone presents as another principal — stolen ServiceAccount token, leaked kubeconfig, OIDC token theft. <em>Defence</em>: short-lived tokens (projected JWTs / IRSA / Workload Identity), mTLS, audit replay-detection.</li>
      <li><strong>Tampering</strong>: image swapped between build + deploy; manifest mutated in transit. <em>Defence</em>: signed images (Cosign), SBOM + provenance attestation, GitOps as source-of-truth.</li>
      <li><strong>Repudiation</strong>: actor denies an action. <em>Defence</em>: audit.k8s.io logs every authz decision; SIEM retention.</li>
      <li><strong>Information disclosure</strong>: secrets leaked via env, logs, mountPoints. <em>Defence</em>: Secrets Manager / Vault, KMS at rest, log redaction, mesh mTLS in transit.</li>
      <li><strong>Denial of service</strong>: noisy neighbour or attack consumes CPU / memory / API quota. <em>Defence</em>: ResourceQuota, LimitRange, PriorityClass, API priority + fairness.</li>
      <li><strong>Elevation of privilege</strong>: container escape, RBAC verb misuse, ServiceAccount over-broad. <em>Defence</em>: PSA Restricted, runtime detection (Falco / Tetragon), RBAC least-privilege, no privileged unless justified.</li>
    </ul>
    <p>Run STRIDE per Service. Document what each Service does + handles + needs; the answers drive every policy in the layers below.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · zero-trust for K8s",
            h2="No implicit trust at any boundary",
            body_html="""    <p>Zero-trust says: <em>every request authenticates + authorises, every time, regardless of network position</em>. Translated to K8s:</p>
    <ul>
      <li><strong>API server</strong>: every call presents identity (token / cert); RBAC checks every verb; admission applies every policy. No \"internal traffic\" exception.</li>
      <li><strong>Pod-to-Pod</strong>: mTLS via service mesh (Istio / Linkerd) — SPIFFE/SPIRE-issued workload identity; default-deny NetworkPolicy; explicit allow rules per consumer.</li>
      <li><strong>Pod-to-cloud-API</strong>: workload identity (IRSA / Workload Identity / Pod Identity) — no static credentials; short-lived tokens scoped per Pod.</li>
      <li><strong>Human access</strong>: OIDC SSO; short-lived kubeconfig (15-60 min); MFA for cluster admin; just-in-time RBAC for production.</li>
    </ul>
    <p>The opposite (perimeter-trust) says \"once you\'re inside the firewall, you\'re trusted.\" In a cluster, that means an attacker who lands one Pod has free range. Zero-trust closes that.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · multi-tenant isolation",
            h2="Soft (namespace) vs hard (vCluster / per-cluster)",
            body_html="""    <p><strong>Soft multi-tenancy</strong>: tenants share a cluster; isolation via Namespace + RBAC + NetworkPolicy + PSA + ResourceQuota + LimitRange. Cheap; suits internal teams + low-risk SaaS. <em>Cannot fully isolate at the kernel level</em> — a kernel CVE crosses namespaces.</p>
    <p><strong>Hard multi-tenancy via virtual clusters</strong> (vCluster / Capsule / Loft): each tenant gets its own apiserver + control plane running inside the host cluster\'s namespaces. Tenants see a real cluster; admins manage them centrally. Stronger isolation than namespace-only, cheaper than per-cluster.</p>
    <p><strong>Hard multi-tenancy via per-cluster</strong>: one cluster per tenant. Strongest isolation. Highest infrastructure cost. Use for regulated workloads, untrusted third-party code, jurisdictional data residency.</p>
    <p><strong>Choosing</strong>: high-trust internal teams → soft. Untrusted code or strict compliance → hard via vCluster or per-cluster. Start soft + escalate as risk warrants.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · the four concentric layers",
            h2="Perimeter · Identity · Tenant zone · Vault",
            body_html="""    <p>Every K-ADV-SEC concept slots into one of four layers. Each layer authenticates + authorises independently; a breach at one layer must not become a breach of the next.</p>
    <ol>
      <li><strong>Perimeter</strong>: untrusted-Internet boundary. Tools: AWS WAF / Azure Front Door / Cloudflare; Ingress / Gateway with TLS termination; rate limiting; bot detection. <em>What can fail</em>: DDoS, OWASP Top-10 attacks, leaked credentials brute-force.</li>
      <li><strong>Identity</strong>: every principal proves who they are. Tools: OIDC for humans; ServiceAccount JWTs (projected, short-lived) for workloads; mTLS via mesh; cert-manager + SPIFFE/SPIRE for workload identity. <em>What can fail</em>: token theft, replay, weak rotation.</li>
      <li><strong>Tenant zone</strong>: namespace-level isolation. Tools: Namespace + RBAC (Roles + Bindings) + NetworkPolicy (default-deny + explicit allow) + PSA Restricted + ResourceQuota + LimitRange. Optional: vCluster for stronger isolation. <em>What can fail</em>: over-broad RBAC, missing NetPol, hostPath escapes, unbounded resources.</li>
      <li><strong>Vault</strong>: deepest stronghold. Tools: External Secrets Operator + Vault / Secrets Manager + KMS; audit.k8s.io webhook to SIEM; signed images (Cosign + SBOM + VEX); break-glass + IR runbooks. <em>What can fail</em>: secret leak, missing audit, unverified image, slow IR.</li>
    </ol>
    <p>The layers are concentric, not stacked — a request reaches the vault only after passing each prior layer.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="STRIDE\'s \"Elevation of privilege\" — which Kubernetes defence is most relevant?",
            options=[
                ("ResourceQuota.", False),
                ("PSA Restricted + RBAC least-privilege + runtime detection.", True),
                ("Image signing.", False),
            ],
            feedback="Elevation = container escape or RBAC misuse. PSA Restricted (no privileged / hostPath / capabilities) + RBAC least-privilege scope + Falco/Tetragon runtime catches what slips through.",
        ),
        3: PauseCheck(
            question="A startup wants to share one cluster across two teams that don\'t fully trust each other\'s code. Which isolation model?",
            options=[
                ("Soft multi-tenancy with namespaces only.", False),
                ("Hard multi-tenancy via vCluster or per-cluster.", True),
                ("No isolation — they\'re the same company.", False),
            ],
            feedback="Untrusted code sharing one kernel = soft multi-tenancy is risky. vCluster gives each team a virtual control plane with stronger isolation; per-cluster is even stronger if budgets allow.",
        ),
    },
    before_after_before='<p>Pre-zero-trust K8s clusters were a single trust zone. Once a workload landed inside the cluster network, it could call the API server with the default ServiceAccount token (auto-mounted everywhere), reach any Pod (no NetworkPolicy default-deny), and read or write secrets the kubelet had access to. A web-app CVE became a cluster compromise.</p>',
    before_after_after='<p>Modern K-ADV-SEC clusters apply zero-trust: every Pod has its own ServiceAccount with short-lived projected tokens; default-deny NetworkPolicy with explicit allow per consumer; mesh-mTLS for Pod-to-Pod; PSA Restricted blocks privileged + hostPath; runtime detection (Falco / Tetragon) catches escape attempts. <em>One Pod compromise stops at the next gate.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Defence-in-depth, not a single wall. Each layer is small; together they\'re strong.</em></p>',
    analogy_intro_html='''<p>K-Citadel is a fortified citadel. The Threat Map Room is the first chamber every architect visits — pinned to the wall is a STRIDE wheel, a list of every entry point, every internal corridor, and every place secrets are kept.</p>
    <p>The citadel has four concentric walls. The <strong>outer wall</strong> faces the open countryside (untrusted Internet) — guards inspect every visitor for weapons (WAF / DDoS protections). Past the outer wall is the <strong>identity gate</strong> — every visitor presents papers, even citizens (zero-trust). Past identity is the <strong>tenant compound</strong> — different families occupy walled compounds with their own gate-keepers (namespaces with RBAC + NetworkPolicy). Deepest is the <strong>armored vault</strong> — secrets, audit logs, signed manifests; only authorised stewards reach it.</p>
    <p>The Captain of the Watch (you) maps every corridor: where can a compromise at one wall go? Where does it stop? The citadel is designed so any single wall failing is a contained event — the next wall holds.</p>''',
    translation_rows=[
        ("Threat Map Room", "Threat-modeling exercise (STRIDE per Service)"),
        ("Outer wall", "Perimeter — Ingress / Gateway / WAF / public LB"),
        ("Identity gate", "AuthN — OIDC + mTLS + ServiceAccount tokens"),
        ("Verbs on the gate-keeper\'s scroll", "RBAC verbs (get/list/create) on resources"),
        ("Walled compound (one family)", "Namespace + RBAC + NetworkPolicy + PSA"),
        ("Compound\'s rationing rules", "ResourceQuota + LimitRange"),
        ("Stronger walls between compounds", "vCluster / per-cluster (hard multi-tenancy)"),
        ("Armored vault", "Secrets Manager / Vault + KMS"),
        ("Vault keeper\'s ledger", "audit.k8s.io → SIEM"),
        ("Sealed papers from the printer", "Cosign-signed image + SBOM + VEX"),
        ("Standing order \"never trust, always check\"", "Zero-trust posture"),
    ],
    analogy_stops="A real citadel\'s walls are physical and slow to breach; K8s \"walls\" are policy + identity + crypto, and a missing policy is invisible until tested. Game days are how you find missing walls.",
    eli5="A castle has many walls — outer wall, identity gate, family compounds, armored vault. Each wall checks every visitor independently. If one wall fails, the next still holds. Your cluster works the same way: every Pod, every secret, every API call passes multiple checks.",
    eli10="<strong>Threat model</strong> = STRIDE walk per Service. <strong>Zero-trust</strong> = no implicit trust at any boundary; mTLS + workload identity + RBAC at every step. <strong>Multi-tenant isolation</strong>: soft (Namespace + RBAC + NetPol + PSA + Quota) for high-trust; hard (vCluster / per-cluster) for untrusted code or compliance. <strong>Four concentric layers</strong>: perimeter, identity, tenant zone, vault — each authenticates + authorises independently.",
    scenarios=[
        Scenario(
            name="Fintech — STRIDE per critical Service",
            body="A 100-engineer fintech runs STRIDE on every Service handling money. <em>Spoofing</em>: short-lived OIDC + IRSA. <em>Tampering</em>: signed images + GitOps. <em>Repudiation</em>: audit.k8s.io to compliance SIEM with 7-year retention. <em>Disclosure</em>: Vault + KMS + mesh-mTLS. <em>DoS</em>: ResourceQuota + PriorityClass. <em>Elevation</em>: PSA Restricted + Falco. <em>One pattern across services; auditors map controls to STRIDE categories.</em>",
        ),
        Scenario(
            name="SaaS — soft multi-tenancy with namespace-per-customer",
            body="A 25-engineer SaaS isolates customers via Namespace + RBAC + NetPol default-deny + PSA Restricted + per-customer ResourceQuota. Tenants see only their namespace; service accounts scoped tightly; mesh-mTLS for Service-to-Service. <em>Soft works because tenants don\'t run arbitrary code; they consume the SaaS app.</em>",
        ),
        Scenario(
            name="Regulated — hard multi-tenancy via vCluster",
            body="A health-tech runs PHI for multiple hospitals. Each hospital gets a vCluster; vClusters share host cluster nodes; control planes are isolated. <em>Tenants see real K8s clusters</em> with their own RBAC, NetPol, even some CRDs. Compliance reviewers map a vCluster to a tenant boundary cleanly.",
        ),
        Scenario(
            name="Outage — perimeter-only design failed",
            body="A startup put all security at the WAF + Ingress. A vulnerable image got past CI; once running, the app called the API server using its auto-mounted ServiceAccount token (kept default permissions); read other Pods\' secrets; exfiltrated. <em>One wall, one breach.</em> Postmortem: layer 2 + 3 + 4 added.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Cluster-internal traffic is trusted; mTLS only matters for Internet-facing.\"",
            truth="Zero-trust says <strong>every</strong> request authenticates. Pod-to-Pod calls without mTLS = an attacker who lands one Pod can impersonate any consumer of any other Service. Mesh-mTLS or workload identity at every hop is the standard.",
        ),
        Misconception(
            myth="\"Namespace + RBAC alone is enough multi-tenancy.\"",
            truth="Namespaces share a kernel. A kernel CVE that allows container escape crosses namespaces freely. Namespace + RBAC + NetPol + PSA + Quota together cover most threats; truly untrusted code needs vCluster or per-cluster.",
        ),
        Misconception(
            myth="\"Threat modeling is a security-team activity, not a platform activity.\"",
            truth="Platform engineers <em>own</em> half the controls (RBAC, NetPol, PSA, admission, mesh, audit). Threat modeling done without platform input misses controls; done without security input misses threats. Joint exercise per service.",
        ),
    ],
    flashcards=[
        Flashcard(front="STRIDE — what does it stand for?", back="<strong>S</strong>poofing, <strong>T</strong>ampering, <strong>R</strong>epudiation, <strong>I</strong>nfo disclosure, <strong>D</strong>oS, <strong>E</strong>levation of privilege. Walk every Service through each category."),
        Flashcard(front="Zero-trust in one sentence?", back="No implicit trust at any boundary; every request authenticates + authorises every time regardless of network position."),
        Flashcard(front="Three multi-tenancy models?", back="<strong>Soft</strong> (Namespace + RBAC + NetPol + PSA + Quota — high-trust), <strong>Hard via vCluster</strong> (virtual control plane per tenant — untrusted code), <strong>Hard via per-cluster</strong> (one cluster per tenant — strongest, highest cost)."),
        Flashcard(front="Four concentric K-Citadel layers?", back="<strong>Perimeter</strong> (Ingress + WAF), <strong>Identity</strong> (OIDC + mTLS + SA tokens + RBAC), <strong>Tenant zone</strong> (Namespace + NetPol + PSA + Quota), <strong>Vault</strong> (Secrets + KMS + audit + signed images)."),
        Flashcard(front="What does mesh-mTLS prevent?", back="Lateral movement between Pods after one is compromised. Without mTLS, an attacker calls any Service freely; with mesh-mTLS + workload identity, the attacker\'s call is unsigned and rejected."),
        Flashcard(front="Why soft multi-tenancy isn\'t enough for untrusted code?", back="Namespaces share the host kernel. A kernel-level CVE (container escape) crosses namespace boundaries. vCluster gives a separate apiserver but still shares the kernel — mitigation includes Kata Containers / gVisor for kernel-level isolation. Per-cluster is the only fully-isolated option."),
        Flashcard(front="Why audit.k8s.io is foundational, not optional?", back="Repudiation defence + compliance evidence + IR detection all require audit logs. Without audit, a breach has no forensic trail and compliance can\'t be evidenced. Wire it before the first prod cluster ships."),
        Flashcard(front="Workload identity — what does IRSA / Workload Identity / Pod Identity replace?", back="Long-lived AWS / GCP / Azure credentials baked into images or env vars. Replaced by short-lived tokens scoped per Pod via federation between K8s ServiceAccount and cloud IAM. No static creds in images / config."),
    ],
    quizzes=[
        Quiz(
            prompt="Walk a STRIDE exercise for a payment-processing Service that calls Stripe + writes to Postgres + reads JWT-auth\'d HTTP requests. Name one defence per STRIDE category.",
            answer="<strong>Spoofing</strong>: short-lived projected JWT for Pod identity + IRSA for AWS access; mTLS for outbound to Stripe (Stripe\'s server identity verified). <strong>Tampering</strong>: Cosign-signed image + GitOps source-of-truth + SBOM tracking. <strong>Repudiation</strong>: audit.k8s.io with full Request body retention; immutable storage. <strong>Info disclosure</strong>: Stripe API key in External Secrets / Vault; KMS-encrypted at rest; mesh-mTLS in transit; log redaction for card data. <strong>DoS</strong>: ResourceQuota + LimitRange on the namespace; rate limiting at the API gateway; HPA tied to request count. <strong>Elevation</strong>: PSA Restricted (no privileged / hostPath); RBAC tightly scoped (only Stripe webhook handler can call its API); Falco rule alerting on unusual syscalls.",
        ),
        Quiz(
            prompt="A team has soft multi-tenancy across 30 namespaces. Audit asks them to harden tenancy. What\'s the upgrade path that doesn\'t require migrating every workload?",
            answer="(1) <strong>Tighten the soft layer first</strong>: NetworkPolicy default-deny + explicit allow per consumer; PSA Restricted enabled cluster-wide; ResourceQuota + LimitRange per namespace; tighter RBAC (no cluster-admin to tenant SAs). (2) <strong>Add layered controls</strong>: External Secrets per namespace; Falco runtime detection; mesh-mTLS for east-west. (3) <strong>For specific high-risk tenants</strong>: migrate to vCluster — they get a virtual control plane while sharing host nodes. Migration is namespace-by-namespace; existing manifests still apply. (4) <strong>Per-cluster only for the highest-risk tenants</strong> (regulated PHI, untrusted code, jurisdiction). Layered approach lets risk drive cost.",
        ),
        Quiz(
            prompt="The CISO says \"adopt zero-trust by next quarter.\" Defend a phased plan that prioritises risk + reversibility.",
            answer="\"<strong>Zero-trust isn\'t a switch — it\'s a posture across many controls.</strong> Phased plan ordered by risk reduction per week of effort: <strong>Week 1-2:</strong> audit.k8s.io to SIEM + RBAC review (find over-broad bindings). <strong>Week 3-4:</strong> NetworkPolicy default-deny + explicit allow per Service (foundation for everything else). <strong>Week 5-8:</strong> mesh-mTLS rollout (Istio or Linkerd) — turn on for one critical Service path first; expand. <strong>Week 9-10:</strong> short-lived projected SA tokens cluster-wide; remove auto-mount on default SAs. <strong>Week 11-12:</strong> PSA Restricted enforce on non-privileged namespaces + Falco / Tetragon runtime alerting. <strong>Quarter 2:</strong> External Secrets + signed-image admission. <strong>Each step is reversible</strong> via feature flags or staged rollout; <strong>each step independently reduces blast radius</strong>; the team owns the operational impact at every phase. Big-bang zero-trust always fails; layered always succeeds.\"",
            cyoa=True,
            cyoa_tag="how the security architect phased the rollout",
        ),
    ],
    glossary=[
        GlossaryItem(name="STRIDE", definition="Threat-modeling framework: Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation of privilege."),
        GlossaryItem(name="Zero-trust", definition="Posture: no implicit trust at any boundary; every request authenticates + authorises regardless of network position."),
        GlossaryItem(name="Soft multi-tenancy", definition="Namespace + RBAC + NetPol + PSA + Quota for tenants sharing one cluster + kernel."),
        GlossaryItem(name="vCluster", definition="Virtual cluster — its own apiserver + control plane running inside a host cluster\'s namespace. Stronger isolation than namespace-only."),
        GlossaryItem(name="Workload identity", definition="Short-lived tokens federated between K8s ServiceAccount and cloud IAM (IRSA / Workload Identity / Pod Identity). Replaces long-lived static creds."),
        GlossaryItem(name="Projected ServiceAccount token", definition="Short-lived JWT mounted via projected volume; rotates automatically; bounded audience + expiration."),
        GlossaryItem(name="Default-deny NetworkPolicy", definition="Cluster-wide stance — no Pod-to-Pod traffic allowed by default; explicit allow rules required per consumer."),
        GlossaryItem(name="Pod Security Admission Restricted", definition="The strictest PSA profile — no privileged, no hostPath, drop ALL capabilities, runAsNonRoot, seccompProfile required."),
        GlossaryItem(name="audit.k8s.io", definition="K8s audit subsystem — every authz decision + request body (configurable) logged. Foundation for compliance + IR."),
        GlossaryItem(name="SPIFFE / SPIRE", definition="Workload-identity standard + reference implementation. Issues short-lived X.509 certs to Pods; foundation for mesh-mTLS."),
    ],
    recap_lead="Threat-model first, zero-trust always, multi-tenancy by design. Four concentric layers: perimeter, identity, tenant zone, vault. Each layer authenticates independently. The next 7 modules each deepen one of the layers — RBAC at scale (S2), admission policy (S3), PSA + runtime (S4), signed images (S5), secrets + mesh (S6), audit + compliance + IR (S7), and the capstone (S8) wires them all into a defendable citadel.",
    recap_next='<strong>Next — S2: RBAC Design at Scale.</strong> Subjects + Roles + Bindings; aggregation patterns; tooling (rakkess, kubectl-who-can); audit-driven RBAC narrowing; namespace-scoped vs cluster-scoped; OIDC group → Role mappings.',
    architecture_svg='''<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Threat modeling + zero-trust + tenancy: 4 concentric defence layers + STRIDE wheel + tenancy options.">
  <rect x="10" y="10" width="740" height="220" rx="12" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">FOUR CONCENTRIC DEFENCE LAYERS · STRIDE-MAPPED</text>
  <rect x="20" y="50" width="170" height="65" rx="6" fill="#3F4A5E"/>
  <text x="105" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Perimeter</text>
  <text x="105" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">untrusted Internet</text>
  <text x="105" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">WAF · Ingress / Gateway</text>
  <text x="105" y="112" text-anchor="middle" font-size="7" fill="#FBE8DC">DoS · Tampering</text>
  <line x1="190" y1="82" x2="220" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aS1)"/>
  <defs><marker id="aS1" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><polygon points="0 0, 10 5, 0 10" fill="#5A4F45"/></marker></defs>
  <rect x="220" y="50" width="170" height="65" rx="6" fill="#5A6B81"/>
  <text x="305" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Identity</text>
  <text x="305" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">OIDC + mTLS + SA tokens</text>
  <text x="305" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">RBAC · workload identity</text>
  <text x="305" y="112" text-anchor="middle" font-size="7" fill="#FBE8DC">Spoofing · Repudiation</text>
  <line x1="390" y1="82" x2="420" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aS1)"/>
  <rect x="420" y="50" width="170" height="65" rx="6" fill="#5DCAA5"/>
  <text x="505" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Tenant zone</text>
  <text x="505" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">Namespace + RBAC + NetPol</text>
  <text x="505" y="100" text-anchor="middle" font-size="8" fill="#1F2433">+ PSA + Quota / vCluster</text>
  <text x="505" y="112" text-anchor="middle" font-size="7" fill="#1F2433">Elevation · DoS</text>
  <line x1="590" y1="82" x2="620" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aS1)"/>
  <rect x="620" y="50" width="120" height="65" rx="6" fill="#A04832"/>
  <text x="680" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Vault</text>
  <text x="680" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">Secrets + KMS</text>
  <text x="680" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">audit log · sigs</text>
  <text x="680" y="112" text-anchor="middle" font-size="7" fill="#FBE8DC">Disclosure</text>
  <rect x="20" y="130" width="350" height="50" rx="6" fill="#FAC775"/>
  <text x="195" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">Soft multi-tenancy</text>
  <text x="195" y="166" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">Namespace + RBAC + NetPol + PSA + Quota — high-trust</text>
  <rect x="380" y="130" width="360" height="50" rx="6" fill="#5E4A8E"/>
  <text x="560" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Hard multi-tenancy</text>
  <text x="560" y="166" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">vCluster (virtual control plane) · per-cluster · Kata Containers / gVisor</text>
  <rect x="20" y="195" width="720" height="30" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="215" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">STRIDE wheel: Spoofing · Tampering · Repudiation · Info disclosure · DoS · Elevation — each maps to specific K8s controls</text>
</svg>''',
    architecture_caption='Four concentric layers (perimeter, identity, tenant, vault); each authenticates independently; breach at one stops at the next. STRIDE wheel maps each threat category to specific K8s controls. Soft tenancy for high-trust; hard tenancy (vCluster / per-cluster) for untrusted code.',
)
