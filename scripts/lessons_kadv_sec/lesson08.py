"""K-ADV-SEC S8 — Capstone: defendable regulated platform."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Capstone — every K-ADV-SEC layer in one regulated platform.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Defendable Citadel · K-Citadel — every K-ADV-SEC layer in one architecture</text>
  <rect x="40" y="70" width="130" height="60" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="105" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">perimeter</text>
  <text x="105" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Ingress + WAF</text>
  <rect x="40" y="140" width="130" height="60" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="105" y="162" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">RBAC + admission</text>
  <text x="105" y="178" text-anchor="middle" font-size="9" fill="#FBF1D6">Kyverno + Gatekeeper</text>
  <rect x="190" y="70" width="130" height="60" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="255" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">PSA + Falco</text>
  <text x="255" y="108" text-anchor="middle" font-size="9" fill="#1F2433">restricted + runtime</text>
  <rect x="190" y="140" width="130" height="60" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="255" y="162" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">signed images</text>
  <text x="255" y="178" text-anchor="middle" font-size="9" fill="#1F2433">Cosign + SBOM + VEX</text>
  <rect x="340" y="70" width="160" height="60" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="420" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">vault + mTLS</text>
  <text x="420" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">ESO + mesh + SPIFFE</text>
  <rect x="340" y="140" width="160" height="60" rx="10" fill="#5E4A8E" stroke="#1F2433"/>
  <text x="420" y="162" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">audit + IR</text>
  <text x="420" y="178" text-anchor="middle" font-size="9" fill="#FBF1D6">SIEM + game days</text>
  <rect x="520" y="70" width="200" height="130" rx="10" fill="#1F8A60" stroke="#1F2433"/>
  <text x="620" y="92" text-anchor="middle" font-size="13" font-weight="700" fill="#FBF1D6">Compliance map</text>
  <text x="620" y="115" text-anchor="middle" font-size="10" fill="#FBF1D6">PCI · HIPAA · SOC2</text>
  <text x="620" y="135" text-anchor="middle" font-size="10" fill="#FBF1D6">FedRAMP · NIST 800-190</text>
  <text x="620" y="160" text-anchor="middle" font-size="10" fill="#FBF1D6">+ break-glass JIT</text>
  <text x="620" y="180" text-anchor="middle" font-size="10" font-style="italic" fill="#FBF1D6">defendable + exercised</text>
</svg>"""


LESSON = LessonSpec(
    num="08",
    title_short="capstone — defendable platform",
    title_full="S8 · Capstone — Defendable Regulated Platform (Finance / Healthcare)",
    title_html="K-ADV-SEC S8 · Capstone",
    module_eyebrow="Module S8 · the Defendable Citadel — every K-ADV-SEC concept in one architecture",
    hero_sub_html='Reference architecture for a regulated K8s platform serving finance / healthcare workloads. Every K-ADV-SEC concept appears: <strong>S1</strong> threat model + zero-trust + multi-tenant; <strong>S2</strong> per-team RBAC + audit2rbac quarterly; <strong>S3</strong> Kyverno + Gatekeeper hybrid + PolicyReport; <strong>S4</strong> PSA Restricted + Falco / Tetragon eBPF; <strong>S5</strong> Cosign + SBOM + SLSA L3+ + VEX + Kyverno verifyImages; <strong>S6</strong> Vault + ESO + mesh-mTLS + SPIFFE; <strong>S7</strong> audit.k8s.io → SIEM + compliance-as-code + break-glass JIT + game days. The capstone is the disciplined assembly, plus the operational glue (runbooks, game-day cadence, compliance dashboards, oncall rotation).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s a Monday morning. The annual SOC2 audit starts in 3 hours. The architect runs the compliance dashboards: <em>every control is green</em>. The auditor walks in; queries dashboards live; samples one PR; observes a game day on staging. The audit closes in 6 hours instead of 6 weeks. <em>Today\'s lesson is the architecture that makes that possible.</em>",
    stamp_html="<strong>Defendable = (1) every layer wired (S1-S7), (2) audit + compliance dashboards continuous, (3) break-glass replaces standing admin, (4) game days quarterly. The architecture isn\'t the work; the disciplined assembly + exercise is the work.</strong>",
    district_pin="ksec-bastion08",
    district_label="Defendable Citadel",
    sections=[
        Section(
            eyebrow="Section 1.1 · the architecture",
            h2="Cluster + tenant + workload + observability layout",
            body_html="""    <p><strong>Cluster shape</strong>: regional control plane (3-zone HA); private nodes + master authorized networks; PSA enforce-restricted cluster default; audit policy + webhook to SIEM enabled at bring-up.</p>
    <p><strong>Tenants</strong>: hard multi-tenancy via vCluster for untrusted-code tenants; soft multi-tenancy via namespace + RBAC + NetPol + ResourceQuota for trusted teams. Per-tenant SecretStore + workload identity.</p>
    <p><strong>Workloads</strong>: every Service uses a per-workload SA with audit2rbac-narrowed RoleBinding. Pods drop ALL caps; runAsNonRoot; seccompProfile RuntimeDefault. Logs via FireLens / Fluent Bit to SIEM. Traces via OTel + Tempo / X-Ray. Metrics via Prometheus + Grafana.</p>
    <p><strong>Observability</strong>: audit.k8s.io → SIEM (Splunk / Loki); Falco / Tetragon eBPF on every node; Container Insights / cloud-native APM. Compliance-as-code dashboards run nightly.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · the policy stack",
            h2="What admission + runtime enforce, end-to-end",
            body_html="""    <p>From request to running Pod, the controls fire in order:</p>
    <ol>
      <li><strong>Auth</strong>: OIDC for humans (with MFA) or short-lived projected SA for workloads. Tokens have audience + 1-hour TTL.</li>
      <li><strong>RBAC</strong>: per-team / per-workload narrow Roles; cluster-admin only via JIT.</li>
      <li><strong>Mutation</strong>: Kyverno mutate sets resource defaults, adds team / cost-center labels, injects Firelens sidecar.</li>
      <li><strong>Validation</strong>: Kyverno validates label requirements + image registries; Gatekeeper validates cross-resource correlation (Service-to-Namespace allow-list); ValidatingAdmissionPolicy + CEL for hot-path inline rules; Kyverno verifyImages for Cosign sig + SLSA + SBOM presence.</li>
      <li><strong>PSA</strong>: namespace label enforce-restricted blocks privileged / hostPath / capabilities.</li>
      <li><strong>Runtime</strong>: Falco / Tetragon eBPF on the node alerts on shell-in-container, mount(), unexpected egress, RoleBinding mutations.</li>
    </ol>"""
        ),
        Section(
            eyebrow="Section 1.3 · the secret + identity stack",
            h2="External vault → ESO → K8s Secret → Pod; mesh-mTLS; SPIFFE",
            body_html="""    <p><strong>Secrets path</strong>: HashiCorp Vault (HA, KMS-sealed) → ESO with per-namespace SecretStore using IRSA / Workload Identity → K8s Secret (KMS-encrypted at rest) → Pod env / volume mount. Vault rotates DB + API creds via its IAM / DB engines; ESO syncs; reloader restarts Pods.</p>
    <p><strong>Identity</strong>: humans via OIDC (Okta / Auth0); workloads via projected SA tokens federated to cloud IAM (IRSA / Pod Identity / Workload Identity); SPIFFE-format certs from mesh CA for Pod-to-Pod mTLS.</p>
    <p><strong>Mesh</strong>: Istio ambient (or Linkerd / Cilium) cluster-wide. Every Pod-to-Pod call signed + encrypted; cert auto-rotates hourly; AuthorizationPolicy enforces \"only X SA may call Y SA.\"</p>
    <p><strong>cert-manager</strong>: Ingress + internal certs auto-rotated; Let\'s Encrypt for external; private CA for internal.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · audit + compliance + IR",
            h2="Continuous evidence + tested response",
            body_html="""    <p><strong>Audit</strong>: audit.k8s.io with Request level for write verbs + RequestResponse for RBAC; webhook → Splunk; retention tiered (90d hot / 1yr warm / 6yr Glacier). Synthetic-audit canary every minute.</p>
    <p><strong>SIEM rules</strong>: detection-as-code in Git. ~80 rules covering RBAC drift, secret access anomalies, image admission denials, runtime escapes, suspicious DNS, privilege escalations, OIDC anomalies. Tiered (page / Slack / log-only).</p>
    <p><strong>Compliance-as-code</strong>: PCI / HIPAA / SOC2 / FedRAMP / NIST 800-190 controls each map to a SIEM query + expected result. Nightly CI run; failures Slack #compliance-ops within 14h of audit.</p>
    <p><strong>Break-glass</strong>: cluster-admin removed for everyone; JIT process: ChatOps approval bot + 1-hour cred + alarmed. Quarterly review of every JIT use.</p>
    <p><strong>IR</strong>: NIST 800-61 runbooks per scenario class (compromise / lateral / data-exfil / DoS / supply-chain). Quarterly game days inject pattern + measure time-to-detect / time-to-contain. Targets: P95 detect &lt; 5min, contain &lt; 30min.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="Why include vCluster for some tenants but not all?",
            options=[
                ("vCluster is always better.", False),
                ("Hard multi-tenancy (vCluster) for untrusted-code tenants; soft (namespace) for trusted teams — match isolation to risk.", True),
                ("vCluster is required for SOC2.", False),
            ],
            feedback="Hard multi-tenancy adds operational cost; reserve for risk-justified tenants. Trusted internal teams thrive on soft tenancy.",
        ),
        3: PauseCheck(
            question="Why are quarterly game days non-optional in the capstone?",
            options=[
                ("Tradition.", False),
                ("Untested runbooks rot; game days measure + improve time-to-detect / time-to-contain.", True),
                ("Required by HIPAA.", False),
            ],
            feedback="Game days produce the metrics + maintain the muscle memory. The capstone\'s P95 detect / contain numbers come from quarterly exercise; without it the runbook decays invisibly.",
        ),
    },
    before_after_before='<p>Pre-disciplined K8s security: each layer adopted ad-hoc; gaps between layers; audit annual + manual; standing admin; runbook in someone\'s head; first incident reveals the gaps.</p>',
    before_after_after='<p>The Defendable Citadel: every K-ADV-SEC layer wired, integrated, exercised. Compliance is continuous; admin is JIT; runbooks are tested; new threats trigger new rules + game days within 30 days. Audit time drops 70%; mean-time-to-contain &lt; 30 minutes.</p>',
    before_after_caption='<p class="ba-caption"><em>Disciplined assembly + exercise is the work. The architecture is the easy part.</em></p>',
    analogy_intro_html='''<p>The Defendable Citadel\'s architect arrives at the morning audit. Every wall is correctly built (S1-S6); every record is current (S7); the war-room binders are dog-eared from quarterly drills. The auditor reviews three things on the wall: the threat-model wheel (showing every category mapped to a control), the compliance map (every regulator\'s control mapped to a query + last-result timestamp), the IR drill register (last quarter\'s game day timing).</p>
    <p>Inside the citadel: every visitor passes the perimeter, the identity gate, the tenant compound, the vault. Every conversation is mTLS-sealed. Every gate-keeper\'s decision is archived. The Captain of the Watch elevates only via the alarmed key — and the alarm has fired three times this quarter, all expected.</p>
    <p>The capstone is not a new technique; it\'s every prior module woven into one architecture, plus the operational rhythm — runbooks, dashboards, game days — that keeps the citadel <em>defendable</em>, not just defended.</p>''',
    translation_rows=[
        ("Threat-model wheel on the wall", "STRIDE per Service mapped to controls"),
        ("Outer wall + identity gate + compounds + vault", "perimeter + AuthN + tenants + secrets layers"),
        ("Sealed letter to printer; verified at gate", "Cosign + SBOM + SLSA + verifyImages"),
        ("Vault couriers with workshop permits", "ESO with per-namespace SecretStore + workload identity"),
        ("mTLS-sealed conversations", "Mesh-mTLS + SPIFFE per workload"),
        ("Audit archive + compliance maps", "audit.k8s.io → SIEM + compliance-as-code"),
        ("Quarterly drill register", "Game days + IR runbook exercise"),
        ("Alarmed elevation key", "Break-glass JIT IAM"),
    ],
    analogy_stops="A real citadel\'s walls are visible; K8s defenses are configuration + policy + process. Verify each via game-day exercises, not visual inspection.",
    eli5="The complete castle: every wall built, every guard trained, every emergency rehearsed. Compliance audits become a 6-hour walk-through, not a 6-week scramble. Every guard has a binder; every binder is practiced.",
    eli10="Reference architecture: regional cluster + private nodes + PSA Restricted default; vCluster hard tenancy for untrusted; audit2rbac-narrowed per-workload RBAC; Kyverno + Gatekeeper + ValidatingAdmissionPolicy hybrid + verifyImages; Falco / Tetragon eBPF; Vault + ESO + mesh-mTLS + SPIFFE + cert-manager + workload identity; audit.k8s.io → SIEM with synthetic canary + compliance-as-code dashboards; break-glass JIT IAM; quarterly game days with P95 detect &lt; 5min / contain &lt; 30min.",
    scenarios=[
        Scenario(
            name="Fintech regulated platform",
            body="A 100-engineer fintech runs the full stack on EKS. SOC2 + PCI + state-banking-regulator compliance. Audit time dropped from 6 weeks (sample-based) to 2 weeks (compliance-as-code dashboards). Game days catch ~2 control gaps per quarter; remediation in 2 weeks each.",
        ),
        Scenario(
            name="Healthcare PHI platform",
            body="A health-tech runs a PHI platform on AKS with the same architecture. Hard multi-tenancy via vCluster per hospital; per-tenant Vault paths; mesh-mTLS strict; audit retention 6 years (HIPAA). HIPAA security risk assessment maps directly to dashboards.",
        ),
        Scenario(
            name="Game day caught a missing detection",
            body="Q3 game day: red team tried a novel pattern (using a service account JWT to call cloud KMS via IRSA). Existing rules didn\'t fire. New SIEM rule + Falco rule added; rerun next quarter cleanly. Continuous improvement loop.",
        ),
        Scenario(
            name="Outage — game-day-discovered runbook gap",
            body="A real incident: compromised CI runner pushed a malicious image; Cosign verifyImages caught it at admission. Runbook step \"revoke CI runner credentials\" took 12 minutes due to manual approval flow; target was 5 min. Action: ChatOps approval bot for credential revocation; next game day clean.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"This architecture is over-engineered.\"",
            truth="Every layer here exists because <em>something doesn\'t exist without it</em>. The marginal cost of building all layers from day-1 is moderate; the cost of bolting them on after the first audit failure is enormous. Regulated platforms have no \"start small\" path.",
        ),
        Misconception(
            myth="\"Compliance dashboards replace audits.\"",
            truth="Dashboards make audits <em>fast</em> + evidence-based; they don\'t replace human review of judgment calls. Auditors still inspect the mapping (\"why is this query the right evidence for this control?\"). Dashboards reduce audit-prep effort, not the audit itself.",
        ),
        Misconception(
            myth="\"You can\'t have hard multi-tenancy on shared nodes.\"",
            truth="vCluster + Kata Containers / gVisor gives <em>kernel-level</em> isolation while sharing physical nodes. Hard multi-tenancy ≠ per-cluster — modern stacks support it on shared infra at moderate cost. Per-cluster reserved for the strictest regulatory boundaries.",
        ),
    ],
    flashcards=[
        Flashcard(front="Top 3 layers a defendable citadel must wire on day-1?", back="<strong>(1) audit.k8s.io → SIEM</strong> (foundation of all evidence). <strong>(2) RBAC narrowing + admission policy</strong> (Kyverno + Gatekeeper + verifyImages). <strong>(3) Network + secret separation</strong> (NetPol default-deny + ESO + mesh-mTLS)."),
        Flashcard(front="Game-day frequency target?", back="Quarterly minimum. Each game day exercises one IR runbook + measures time-to-detect + time-to-contain. New runbooks tested within 30 days of creation."),
        Flashcard(front="Why break-glass JIT replaces standing cluster-admin?", back="(1) Audit evidence: every elevation logged + alarmed. (2) Blast radius: if a credential leaks, it\'s short-lived. (3) Compliance: \"no standing privileged access\" is a common control — JIT proves it."),
        Flashcard(front="Compliance-as-code value vs annual audit-prep?", back="Continuous evidence + 6× faster audit cycle + earlier detection of control drift (Slack alert vs annual finding). Cost: detection-as-code + compliance-as-code in Git + nightly CI."),
        Flashcard(front="What does the threat-model wheel sit at the centre of?", back="Every other security control. Threat model produces the questions; STRIDE walks the categories; each category maps to specific K8s controls (RBAC, NetPol, PSA, signed images, etc.)."),
        Flashcard(front="Soft + hard multi-tenancy mix — when to mix?", back="When tenants vary in trust. Untrusted code (third-party SaaS, partner integrations) → hard via vCluster + Kata. Trusted internal teams → soft via namespace. Match the isolation cost to the risk."),
        Flashcard(front="Why audit + Falco are both needed?", back="audit.k8s.io captures API-level events (RBAC changes, Secret reads). Falco captures runtime events (syscalls, container behaviour). Different attack stages — admission vs running container. Both required."),
        Flashcard(front="The capstone\'s most-overlooked element?", back="Operational rhythm — game days, compliance dashboards, runbook exercise, break-glass review. The architecture is widely-known; the discipline of operating it is the differentiator."),
    ],
    quizzes=[
        Quiz(
            prompt="Walk a brand-new engineer through the Defendable Citadel in 5 minutes. What\'s the orientation?",
            answer="\"Three things to see: (1) <strong>The compliance dashboard wall</strong>: every PCI / SOC2 / HIPAA control mapped to a query + last-result timestamp. We don\'t prepare for audits — we run them continuously. (2) <strong>The policy stack</strong>: every Pod walks Auth → RBAC → Kyverno → Gatekeeper → CEL → PSA → Falco. Six gates. Each is in Git; each is tested in CI; each runs in the cluster. (3) <strong>The IR runbook shelf</strong>: 12 binders, each tested last quarter, each with measured time-to-contain. Pick any one + we\'ll walk it. <strong>And then the operational rhythm</strong>: detection-as-code in Git; PRs reviewed; quarterly game days; break-glass alarmed in Slack #soc; compliance-as-code nightly. <strong>The work isn\'t the architecture; the work is keeping it disciplined.</strong>\"",
        ),
        Quiz(
            prompt="A startup says: \"we\'re too small for this — we\'ll add it when we hit 50 engineers.\" Defend day-1 adoption.",
            answer="\"<strong>The marginal cost of building K-ADV-SEC layers from day-1 is days of work; the cost of retrofitting at 50 engineers is months.</strong> Three reasons: (1) <strong>Migration tax</strong>: every existing workload has to be re-deployed when you add Kyverno verifyImages, mesh-mTLS, audit pipelines. At 50 engineers + 200 services, the migration is its own project. At day-1 + 5 services, the migration is a Tuesday. (2) <strong>Habits compound</strong>: engineers who started with no admission policy build YAMLs that won\'t pass it; engineers who started with admission policy build correct YAMLs from day-1. Tech debt is the cost of un-learning. (3) <strong>One audit failure undoes years</strong>: a regulated customer asks for SOC2 evidence and you have nothing. The cost of that is a customer lost, possibly lawsuit, possibly the business. <strong>The right answer: ship the layers as a Service Catalog template + a couple of opinionated GitHub Actions on day-1; engineers consume the template; the team grows into the discipline rather than retrofitting it.</strong>\"",
        ),
        Quiz(
            prompt="An incoming auditor says: \"show me you\'re ready for SOC2 Type II.\" Walk the demo.",
            answer="\"<strong>Step 1 — compliance dashboard wall</strong>: every CC + AC + AU control mapped to a SIEM query; CC6.1 (logical access) → \"every RoleBinding change in past 90 days, PR-reviewed\"; CC7.2 (anomaly detection) → \"Falco + audit alerts → IR runbook count\"; AU-2 (auditable events) → audit.k8s.io retention timeline. <strong>Step 2 — live query</strong>: pick any 3 controls; run the query; show the result + the link to the source-of-truth (Git PR for RBAC change, Slack thread for IR alarm). <strong>Step 3 — game-day register</strong>: last 4 quarters with date + scenario + time-to-detect + time-to-contain. <strong>Step 4 — break-glass log</strong>: every JIT cluster-admin grant in past quarter with reason + ticket link. <strong>Step 5 — exception register</strong>: any control with a documented exception (e.g., legacy workload exempted from PSA Restricted) with sunset date. <strong>Step 6 — sample one engineer</strong>: live walkthrough of their PR review process. <strong>Audit closed in 6 hours</strong> instead of 6 weeks. Auditor signs off.\"",
            cyoa=True,
            cyoa_tag="how the platform passed the SOC2 Type II audit",
        ),
    ],
    glossary=[
        GlossaryItem(name="Defendable platform", definition="A platform whose every layer is wired (S1-S7), continuously evidenced, and exercised quarterly. The disciplined assembly is the differentiator."),
        GlossaryItem(name="Detection-as-code", definition="SIEM rules + alert pipelines stored in Git; PR-reviewed; tested via replay; deployed as code."),
        GlossaryItem(name="Compliance-as-code", definition="Each compliance control mapped to a SIEM query; CI runs nightly; failures alert Slack; replaces annual audit-prep."),
        GlossaryItem(name="vCluster + Kata", definition="Hard multi-tenancy stack — vCluster gives per-tenant control plane; Kata Containers gives per-Pod kernel isolation. Sharable nodes."),
        GlossaryItem(name="Service Catalog template", definition="Backstage / IDP template that ships a workload pre-wired with all security layers (RBAC + NetPol + PSA + ESO + mesh + ADOT). Engineers consume; team owns the template."),
        GlossaryItem(name="P95 time-to-detect", definition="From compromise event to first alert. Defendable platform target: &lt; 5 minutes for known patterns."),
        GlossaryItem(name="P95 time-to-contain", definition="From alert to compromise blocked from spreading. Defendable platform target: &lt; 30 minutes."),
        GlossaryItem(name="IR runbook library", definition="Per-scenario IR runbooks (compromise, lateral, data-exfil, DoS, supply-chain). Tested quarterly; new threat → new runbook within 30 days."),
        GlossaryItem(name="Continuous compliance", definition="Posture: compliance is a state evidenced continuously, not a snapshot at audit time. Dashboards + nightly CI + alarms."),
        GlossaryItem(name="Operational rhythm", definition="Quarterly game days + monthly break-glass review + nightly compliance CI + weekly RBAC narrowing review. The discipline that keeps the citadel defendable."),
    ],
    recap_lead="The Defendable Citadel: every K-ADV-SEC layer wired (S1-S7), every audit + compliance control queryable, every IR runbook tested. The work is not the architecture — it\'s the operational rhythm that keeps the architecture defendable.",
    recap_next='<strong>K-ADV-SEC complete.</strong> 8 modules. From threat modeling (S1) to the defendable citadel (S8). Next K-ADV course: <em>K-ADV-NET</em> (Networking Architect — K-Highway), or per founder direction. The Citadel pin map is fully populated.',
)
