"""K-ADV-SEC S7 — Audit log analytics + compliance evidence + IR."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Audit + compliance + IR pipeline.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Audit Archives + War Room · K-Citadel — every action logged, mapped, exercised</text>
  <rect x="40" y="70" width="180" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="130" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">audit.k8s.io</text>
  <text x="130" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">every API request</text>
  <text x="130" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">+ Falco / Tetragon</text>
  <rect x="240" y="70" width="180" height="100" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="330" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">SIEM pipeline</text>
  <text x="330" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Loki / Splunk / OpenSearch</text>
  <text x="330" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">retention + queryable</text>
  <rect x="440" y="70" width="160" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="520" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Compliance maps</text>
  <text x="520" y="108" text-anchor="middle" font-size="9" fill="#1F2433">PCI / HIPAA / SOC2</text>
  <text x="520" y="124" text-anchor="middle" font-size="9" fill="#1F2433">NIST 800-190</text>
  <rect x="620" y="70" width="100" height="100" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="670" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">War Room</text>
  <text x="670" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">break-glass</text>
  <text x="670" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">+ IR runbook</text>
</svg>"""


LESSON = LessonSpec(
    num="07",
    title_short="audit + compliance + IR",
    title_full="S7 · Audit Log Analytics + Compliance Evidence + Incident Response",
    title_html="K-ADV-SEC S7 · Audit + Compliance + IR",
    module_eyebrow="Module S7 · Audit Archives + War Room — every action logged, mapped, exercised",
    hero_sub_html='<strong>audit.k8s.io</strong> logs every authz decision (Metadata / Request / RequestResponse levels). Webhook → SIEM (Loki / Splunk / OpenSearch). <strong>Compliance evidence</strong>: map controls to specific log queries — \"PCI 7.1 = quarterly RBAC review log\"; \"HIPAA §164.308(a)(4) = RoleBinding changes\"; \"SOC2 CC6.1 = privileged access logs\"; \"NIST 800-190 4.4 = image admission denied events.\" <strong>Break-glass IAM</strong>: standing privilege removed; just-in-time elevation via approval workflow + alarmed every time. <strong>IR runbook</strong>: containment → eradication → recovery → postmortem; tested via game days. The war room is where the runbook is exercised on calm days, not invented during incidents.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A breach is suspected; the auditor is on the way at 9 AM. The team can\'t produce evidence of who did what, when. <em>Audit logs went to disk; rotated; never sampled to a SIEM.</em> The team has 6 hours to invent a forensic story. Today\'s lesson: build audit + compliance evidence + IR runbook before the breach, not during.",
    stamp_html="<strong>audit.k8s.io → SIEM pipeline. Map every compliance control to a queryable log surface. Break-glass replaces standing privilege. IR runbook tested via game days. Evidence + readiness are the two outputs.</strong>",
    district_pin="ksec-bastion07",
    district_label="Audit Archives + War Room",
    sections=[
        Section(
            eyebrow="Section 1.1 · audit.k8s.io configuration",
            h2="three log levels, webhook backend, retention policy",
            body_html="""    <p><strong>audit.k8s.io</strong> is the K8s audit subsystem. Configured via <code>--audit-policy-file</code> (what to log) + <code>--audit-webhook-config-file</code> (where to send) on the apiserver. Three levels per rule:</p>
    <ul>
      <li><strong>Metadata</strong>: who, what, when, source IP. No request body. Smallest volume.</li>
      <li><strong>Request</strong>: + request body (e.g., the YAML being created). Medium volume.</li>
      <li><strong>RequestResponse</strong>: + response body. Largest. Use selectively for high-value resources (Secrets, RBAC, Bindings).</li>
    </ul>
    <p><strong>Policy</strong>: typical pattern — Metadata for everything; Request for write verbs; RequestResponse for Secret + RBAC reads/writes; omit noisy probes (kubelet self-checks). YAML lives in Git; rolled via apiserver static-Pod manifest update.</p>
    <p><strong>Backend</strong>: webhook (preferred — async to SIEM); log file (fallback for sampling). Webhook latency must be tight or apiserver throttles.</p>
    <p><strong>Retention</strong>: per compliance regime — PCI 12 months, HIPAA 6 years, SOC2 1 year. Tiered storage: SIEM hot (90 days) + S3 archive (long-term) + Glacier (final).</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · SIEM pipeline + correlation",
            h2="aggregate, correlate, alert",
            body_html="""    <p>Audit alone is data; SIEM is signal. Pipeline:</p>
    <ul>
      <li><strong>Ingest</strong>: webhook → Loki / Splunk / OpenSearch / Datadog / Sentinel. Tagged with cluster + namespace + tenant.</li>
      <li><strong>Index</strong>: structured fields (verb, resource, user, response code, namespace).</li>
      <li><strong>Correlate</strong>: cross-source (audit + Falco + cloud audit + WAF) join on user / Pod / time. Multi-signal incidents surface.</li>
      <li><strong>Alert</strong>: tiered rules (immediate-page / Slack / log-only). Common rules: <em>secret-read by unexpected SA</em>, <em>RoleBinding to cluster-admin</em>, <em>privileged Pod created in non-system namespace</em>, <em>API impersonation used</em>, <em>auth failures spike</em>.</li>
      <li><strong>Dashboards</strong>: per compliance regime. PCI dashboard, HIPAA dashboard, SOC2 dashboard.</li>
    </ul>
    <p>Mature pipelines have <strong>detection-as-code</strong>: SIEM rules in Git; PR reviewed; tested with replay. New rules added when threat models evolve.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · compliance control mapping",
            h2="PCI · HIPAA · FedRAMP · SOC2 · NIST 800-190",
            body_html="""    <p>Compliance regimes ask \"how do you do X?\" Map each control to a specific K8s mechanism + audit query:</p>
    <ul>
      <li><strong>PCI DSS</strong>: 7.1 (least privilege) → RBAC reviews; 8.2 (rotation) → ESO + cert-manager rotation logs; 10.x (audit) → audit.k8s.io retention + SIEM alerts.</li>
      <li><strong>HIPAA</strong>: §164.308(a)(4) (access management) → RoleBinding change logs; §164.312(b) (audit controls) → audit.k8s.io + immutable storage.</li>
      <li><strong>SOC2</strong>: CC6.1 (logical access) → OIDC + RBAC + JIT; CC7.2 (anomaly detection) → Falco + SIEM rules.</li>
      <li><strong>FedRAMP</strong> (Moderate / High): controls AC, AU, CM, IA, SC — map each to specific K8s + cloud config.</li>
      <li><strong>NIST 800-190</strong> (container security): every section maps directly — image trust (S5), runtime (S4), orchestrator (S2/S3), network (S6 mTLS).</li>
    </ul>
    <p>Pattern: <strong>compliance-as-code</strong> — control → SIEM query → expected result. CI runs the mapping nightly; failures surface before audit.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · break-glass + IR runbook",
            h2="JIT elevation + tested incident response",
            body_html="""    <p><strong>Break-glass</strong>: standing cluster-admin removed for everyone. Elevation requires a JIT process — Vault one-time credential, ChatOps approval bot, or AWS SSO emergency role. Every JIT use alarms in Slack + email; expires in 1 hour; logged in audit.k8s.io.</p>
    <p><strong>IR runbook</strong> follows NIST 800-61 / SP 800-184: <em>Containment</em> (cordon node, scale to zero, isolate namespace via NetPol drop-all); <em>Eradication</em> (remove backdoor, rotate compromised secrets, replace from clean image); <em>Recovery</em> (restore from clean state via GitOps; canary + verify); <em>Postmortem</em> (timeline + cause + control gaps + remediation actions).</p>
    <p><strong>Game days</strong> exercise the runbook on calm days. Quarterly: red team injects a known-pattern compromise (curl-bash from a Pod, RoleBinding change, suspicious DNS); on-call follows the runbook; time-to-detect + time-to-contain measured + improved.</p>
    <p>Mature programs have an IR <em>library</em>: scenarios → runbooks → game-day frequency. Each major service has an entry. New CVEs of class X get a runbook + a game day within 30 days.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="What\'s the right audit level for Secret reads?",
            options=[
                ("Metadata only.", False),
                ("RequestResponse — capture both the request and the secret value being returned.", False),
                ("Request — captures who + what was requested without the secret value.", True),
            ],
            feedback="Request level captures the auth context + which Secret was accessed. RequestResponse would capture the actual secret bytes — never log secret values. Metadata-only would miss which Secret.",
        ),
        3: PauseCheck(
            question="What\'s the value of a quarterly game day?",
            options=[
                ("Compliance documentation.", False),
                ("Test the IR runbook + measure time-to-detect / time-to-contain.", True),
                ("Required by ISO 27001.", False),
            ],
            feedback="Runbooks rot. Quarterly game days verify the runbook still fires + the team still knows it. Time-to-detect / time-to-contain are measurable + improvable metrics.",
        ),
    },
    before_after_before='<p>Pre-mature security ops: audit logs to disk; rotated; nobody read them. Compliance evidence was point-in-time PowerPoints + sample YAMLs. Standing cluster-admin to operators. IR was \"call the founder\". Game days didn\'t exist; every incident was a first-time scramble.</p>',
    before_after_after='<p>Modern: audit.k8s.io → SIEM with retention per regime; compliance-as-code maps controls to queries; break-glass replaces standing privilege; IR runbook tested via game days; metrics on time-to-detect + time-to-contain. <em>Audits are routine; incidents are exercises that matter.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Build evidence + readiness on calm days. Both outputs are needed; both decay without exercise.</em></p>',
    analogy_intro_html='''<p>The deepest part of the citadel has two adjoining rooms. The <strong>Audit Archives</strong> hold copies of every gate-keeper\'s decisions, every transaction at the vault, every shift change. The archive is searchable; auditors visit annually and ask \"show me every time someone signed for a vault key in 2025\" — the archivist runs a query.</p>
    <p>The <strong>War Room</strong> next door has wall-mounted maps of every threat scenario the citadel has prepared for. Each scenario has a numbered binder: containment steps, eradication steps, recovery steps, postmortem template. Standing privilege has been removed; the captain elevates only via the alarmed key (break-glass). Quarterly drills test the binders; the captain who can run \"Scenario 17: ransomware on the tenant compound\" by 09:30 doesn\'t need to invent at 03:00.</p>''',
    translation_rows=[
        ("Audit Archives", "audit.k8s.io webhook → SIEM"),
        ("Three archive depths", "audit levels: Metadata / Request / RequestResponse"),
        ("Archivist with a query", "SIEM queries / Loki LogQL / Splunk SPL"),
        ("Cross-source ledgers", "Audit + Falco + cloud audit correlation"),
        ("Compliance review register", "Compliance-as-code (control → query)"),
        ("War Room scenario binders", "IR runbooks (NIST 800-61)"),
        ("Quarterly drills", "Game days"),
        ("Alarmed elevation key", "Break-glass JIT IAM"),
        ("Postmortem ledger", "Incident postmortem template"),
    ],
    analogy_stops="A real archive has paper copies; K8s audit is webhook delivery + SIEM storage — if the webhook misses or SIEM drops, the record is gone. Test the pipeline with synthetic events monthly.",
    eli5="Two rooms. One holds copies of every decision in the castle, organised so anyone can search them. The other has labelled binders for every emergency: what to do first, second, third. The castle\'s leaders practice with the binders monthly so they know them by heart.",
    eli10="<strong>audit.k8s.io</strong> logs every API request via webhook → SIEM (Loki / Splunk). Three levels (Metadata / Request / RequestResponse). Retention per regime (PCI 12mo / HIPAA 6yr / SOC2 1yr). <strong>Correlation</strong>: SIEM rules join audit + Falco + cloud audit. <strong>Compliance mapping</strong>: each control → SIEM query; CI verifies nightly. <strong>Break-glass</strong>: standing cluster-admin removed; JIT elevation alarmed. <strong>IR runbook</strong>: NIST 800-61 phases (containment → eradication → recovery → postmortem); game days quarterly.",
    scenarios=[
        Scenario(
            name="Compliance-as-code dashboards",
            body="A 200-engineer org runs nightly Loki queries mapping every PCI / SOC2 / HIPAA control to log evidence. Failures surface in Slack 14 hours before audits. Auditors review the mapping rather than sample artefacts; audit time drops from 6 weeks to 2 weeks.",
        ),
        Scenario(
            name="Break-glass JIT replaces standing admin",
            body="Standing cluster-admin removed across 5 clusters. JIT process: on-call invokes <code>kubectl-jit grant cluster-admin --reason \"page-12345\" --duration 1h</code>; approval bot in Slack; alarmed; logged. Quarterly review: how often, by whom, why. \"Always-on admin\" replaced by \"earned-once-per-incident.\"",
        ),
        Scenario(
            name="Game day caught a runbook gap",
            body="Quarterly red team simulated a curl-bash compromise on a Pod. On-call followed runbook. Issue: runbook said \"cordon node\" but didn\'t name how to evict the compromised Pod cleanly without losing forensic data. Runbook updated; one-line fix; next game day clean.",
        ),
        Scenario(
            name="Outage — audit pipeline went down quietly",
            body="audit.k8s.io webhook timed out for 6 hours; apiserver buffered + dropped audit events. Nobody noticed; no synthetic-event canary. Postmortem: synthetic event every minute; SIEM alerts if absent &gt; 10 minutes; redundant local-file backend as fallback.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"audit.k8s.io is on by default.\"",
            truth="<strong>It\'s opt-in.</strong> Without <code>--audit-policy-file</code> on apiserver, no audit records are produced. Configure the policy + webhook on day-1 of cluster bring-up, before any production traffic.",
        ),
        Misconception(
            myth="\"Compliance is a once-a-year thing.\"",
            truth="Compliance-as-code makes it nightly. Each control has a query; CI runs queries; failures alert in real-time. Annual audit becomes a review of the mapping, not a forensic reconstruction.",
        ),
        Misconception(
            myth="\"Game days are theatre; the runbook works.\"",
            truth="Untested runbooks rot. APIs change; tools deprecate; team turnover loses tribal knowledge. Quarterly game days catch decay early; first one always finds gaps.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three audit.k8s.io levels?", back="<strong>Metadata</strong> (who/what/when), <strong>Request</strong> (+ request body), <strong>RequestResponse</strong> (+ response body — never for Secrets!). Configure per resource via audit policy file."),
        Flashcard(front="Audit retention per major regime?", back="<strong>PCI</strong>: 12 months (with last 3 immediately accessible). <strong>HIPAA</strong>: 6 years. <strong>SOC2</strong>: 1 year. Tier: SIEM hot 90 days + S3 archive + Glacier."),
        Flashcard(front="What is compliance-as-code?", back="Each compliance control mapped to a SIEM query + expected-result rule. CI runs nightly; failures alert. Replaces annual audit-prep with continuous evidence."),
        Flashcard(front="Break-glass IAM — what does it replace?", back="Standing cluster-admin bindings. Replaced by JIT elevation: short-lived credential, approval workflow, alarmed every use. Audit + compliance evidence is automatic."),
        Flashcard(front="Four IR runbook phases (NIST 800-61)?", back="<strong>Containment</strong> (stop spread), <strong>Eradication</strong> (remove root cause), <strong>Recovery</strong> (restore clean), <strong>Postmortem</strong> (timeline + gaps + remediation actions)."),
        Flashcard(front="What does a game day measure?", back="<strong>Time-to-detect</strong> (alarm fires from compromise event) + <strong>time-to-contain</strong> (compromise blocked from spreading). Both measurable + improvable; per-runbook targets."),
        Flashcard(front="Why never log Secret values in audit?", back="RequestResponse level + Secret reads = secret values land in SIEM logs. Anyone with SIEM read can extract. Use Request level for Secrets (captures access without value); never RequestResponse."),
        Flashcard(front="What\'s a synthetic-audit canary?", back="A scheduled event (e.g., a no-op annotation update) that should appear in audit + SIEM every minute. Absence &gt; 10 minutes = audit pipeline broken; alarm before silent drop becomes invisible."),
    ],
    quizzes=[
        Quiz(
            prompt="A new compliance review asks you to evidence \"PCI 7.1 — least-privilege access management.\" What\'s the audit-driven answer?",
            answer="(1) <strong>Map the control</strong>: 7.1.x covers role-based access. K8s implementation = RBAC + audit. (2) <strong>Evidence query</strong>: SIEM rule \"every RoleBinding / ClusterRoleBinding change in past 90 days\" + \"every cluster-admin binding currently active\". Expected output: changes are PR-approved; cluster-admin only via JIT (zero standing). (3) <strong>Show audit2rbac runs</strong>: quarterly narrowing reports + diffs (evidence of continuous review). (4) <strong>Per-tenant RBAC</strong>: query showing each tenant\'s SAs are scoped only to their namespace. (5) <strong>Document the mapping</strong>: compliance-as-code repo with this control → query + expected result. (6) <strong>Auditor walkthrough</strong>: run the queries live; show the runbook for handling exceptions.",
        ),
        Quiz(
            prompt="A Falco alert fires + audit shows a RoleBinding to cluster-admin was just created from CI. Walk IR steps in the runbook.",
            answer="<strong>Containment (within 5 min):</strong> (1) Revert the RoleBinding via GitOps PR or direct <code>kubectl delete</code> if emergency. (2) Cordon the node where the CI pipeline ran. (3) Suspend the CI runner identity. <strong>Eradication (within 30 min):</strong> (4) Identify which CI pipeline created the binding — was it intentional? Approved? If not, the CI runner credential is compromised; revoke it. (5) Audit log: did the SA do anything else? List all actions. (6) Rotate any secrets the SA may have accessed during the window. <strong>Recovery (within 4 hours):</strong> (7) Verify cluster state matches GitOps source-of-truth. (8) Restore CI from clean image with new credential. (9) Run smoke tests. <strong>Postmortem (within 1 week):</strong> (10) Timeline of detection → containment. (11) How did the bad RoleBinding pass review? Add admission rule blocking CI from creating cluster-admin Bindings. (12) Add a SIEM rule to alert on every cluster-admin Binding creation regardless of source.",
        ),
        Quiz(
            prompt="The CFO asks why we run game days when nothing has gone wrong. Defend.",
            answer="\"<strong>The cost of an untested runbook is paid during the next real incident.</strong> Three reasons game days stay quarterly: (1) <strong>Runbook decay is invisible</strong> until tested. APIs change (Falco rule syntax updates; kubectl flags deprecated); tooling versions move; team membership turns over. The runbook that worked last quarter may not work this quarter. (2) <strong>Time-to-contain is the metric we sell to the board</strong>: \"P95 time-to-contain &lt; 30 minutes\". Without exercise, we can\'t honestly claim that number. Game days produce the evidence. (3) <strong>Real incidents at 3 AM are not the time to discover gaps</strong>. Game days at 2 PM with the team coffee\'d-up is. The cost of a quarterly day (1 dev-day × 6 engineers = ~3k$) is 1/100th of one missed-detection incident. <strong>Game days are how we know we\'re ready, not theatre.</strong>\"",
            cyoa=True,
            cyoa_tag="how the security architect defended game days",
        ),
    ],
    glossary=[
        GlossaryItem(name="audit.k8s.io", definition="K8s audit subsystem. Configured via audit policy + webhook backend. Three levels: Metadata / Request / RequestResponse."),
        GlossaryItem(name="SIEM", definition="Security Information + Event Management. Loki / Splunk / OpenSearch / Sentinel. Aggregates, indexes, correlates, alerts."),
        GlossaryItem(name="Compliance-as-code", definition="Each compliance control mapped to a SIEM query + expected result. CI runs nightly; failures alert; replaces annual audit-prep."),
        GlossaryItem(name="Break-glass IAM", definition="JIT elevation replacing standing privilege. Short-lived credential + approval + alarms + logs."),
        GlossaryItem(name="IR runbook", definition="NIST 800-61 phases — containment / eradication / recovery / postmortem. Per-scenario binder; tested via game days."),
        GlossaryItem(name="Game day", definition="Scheduled exercise where red team injects a known-pattern compromise; on-call follows the runbook; time-to-detect + time-to-contain measured."),
        GlossaryItem(name="audit policy file", definition="YAML defining which resources / verbs at which audit level. Lives in Git; rolled via apiserver static-Pod manifest."),
        GlossaryItem(name="Synthetic-audit canary", definition="Scheduled no-op event appearing in audit. Absence detection alerts when audit pipeline silently drops."),
        GlossaryItem(name="NIST 800-190", definition="NIST application container security guide. Sections map directly to K-ADV-SEC modules."),
        GlossaryItem(name="MITRE ATT&CK for Containers", definition="Tactic + technique catalog for container threats. Map IR runbooks + Falco rules to ATT&CK techniques."),
    ],
    recap_lead="audit.k8s.io → SIEM is the foundation; compliance-as-code is the evidence; break-glass + IR runbook + game days are the readiness. All three on calm days; the war room is exercised, not invented.",
    recap_next='<strong>Next — S8: Capstone — defendable regulated platform.</strong> Every K-ADV-SEC concept woven into one architecture for finance / healthcare. Threat model + zero-trust + RBAC + admission + PSA + signed images + secrets + mTLS + audit + compliance + IR.',
)
