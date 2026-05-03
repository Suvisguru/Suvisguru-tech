"""K-OCP O4 — OpenShift Security (OAuth, SCCs, Compliance Operator, RHACS, FIPS, Kata sandboxed containers)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OCP security stack — OAuth, SCCs, RHACS, Compliance Operator, FIPS, Kata.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Safety Office — defence in depth</text>
  <rect x="40" y="65" width="170" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="125" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">authN / authZ</text>
  <text x="125" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">OAuth providers</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">LDAP · OIDC · HTPasswd</text>
  <text x="125" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">OCP RBAC + ServiceAccts</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">integrated OAuth server</text>
  <rect x="225" y="65" width="170" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="310" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">SCCs</text>
  <text x="310" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">restricted-v2 (default)</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">nonroot-v2 · anyuid</text>
  <text x="310" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">hostnetwork · privileged</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">SCC vs PSA</text>
  <rect x="410" y="65" width="170" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="495" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">compliance + ACS</text>
  <text x="495" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">Compliance Operator</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">File Integrity</text>
  <text x="495" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">Security Profiles</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">RHACS / StackRox</text>
  <rect x="595" y="65" width="125" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="657" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">hardware</text>
  <text x="657" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">KMS integration</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">FIPS 140-2 mode</text>
  <text x="657" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">Kata sandboxed</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">containers</text>
</svg>"""


LESSON = LessonSpec(
    num="04", title_short="OCP security",
    title_full="O4 · OpenShift Security (OAuth, SCCs, Compliance Operator, RHACS, FIPS, Kata)",
    title_html="K-OCP O4 · OpenShift Security",
    module_eyebrow="Module O4 · the Safety Office — defence in depth",
    hero_sub_html='<strong>AuthN</strong>: integrated OAuth server + providers (HTPasswd, LDAP, OIDC, GitHub, Keystone). <strong>AuthZ</strong>: OCP RBAC + ServiceAccounts. <strong>Security Context Constraints (SCCs)</strong>: <code>restricted-v2</code> default, plus <code>nonroot-v2</code>, <code>anyuid</code>, <code>hostnetwork</code>, <code>privileged</code>. SCC vs PSA. <strong>Compliance Operator</strong> (CIS / NIST / PCI-DSS / FedRAMP / HIPAA scans), <strong>File Integrity Operator</strong>, <strong>Security Profiles Operator</strong>. <strong>Red Hat Advanced Cluster Security (RHACS / StackRox)</strong> — vuln + compliance + network graph + runtime + admission. <strong>KMS</strong>, <strong>FIPS</strong>, <strong>OpenShift sandboxed containers (Kata)</strong>.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. RHACS alert: <em>\"crypto-miner detected in production Pod, container.runtime.process anomalous.\"</em> The Pod runs as root (anyuid SCC granted ad-hoc 18 months ago by someone now-departed). The image came from an internal registry but lacks SBOM + CVE scan. Compliance Operator was disabled in this namespace because \"it broke the build\" — last scan from 9 months ago. <em>Blast radius: every secret in the cluster the Pod\'s SA can read.</em> Today\'s lesson: layered OCP security — auth, SCC, compliance, runtime, hardware.",
    stamp_html="<strong>Default to restricted-v2 SCC; only escalate explicitly. Use Compliance Operator for CIS/NIST/PCI scans + RHACS for runtime. Integrated OAuth + identity providers; KMS for secrets; FIPS for federal; Kata for sandboxed untrusted workloads.</strong>",
    district_pin="ko-bay04", district_label="Safety Office",
    sections=[
        Section(eyebrow="Section 1.1 · OAuth + RBAC", h2="Integrated OAuth + identity providers + OCP RBAC",
            body_html="""    <p><strong>OCP\'s integrated OAuth server</strong> is built into the cluster (cluster operator <code>authentication</code>). It backs all human auth + many service-to-service flows.</p>
    <p><strong>Identity providers</strong> configurable via <code>OAuth/cluster</code>: <strong>HTPasswd</strong> (file-based, dev/break-glass), <strong>LDAP</strong> (corporate dir), <strong>OIDC</strong> (Keycloak / Okta / Auth0), <strong>GitHub</strong>, <strong>GitLab</strong>, <strong>Google</strong>, <strong>Keystone</strong> (OpenStack), <strong>RequestHeader</strong> (proxy auth), <strong>BasicAuth</strong>. Multiple IDPs can coexist.</p>
    <p><strong>OCP RBAC</strong> = K8s RBAC + OCP-specific roles: <em>cluster-admin</em>, <em>admin</em> (project), <em>edit</em> (project), <em>view</em> (project), plus all the <code>system:</code> roles. <code>oc adm policy add-role-to-user</code> / <code>oc adm policy add-cluster-role-to-user</code>.</p>
    <p><strong>ServiceAccounts</strong> — every Project gets <em>default</em>, <em>builder</em>, and <em>deployer</em> SAs by default. Workloads that need scoped permissions get their own SA + RoleBinding.</p>"""),
        Section(eyebrow="Section 1.2 · SCCs", h2="Security Context Constraints (SCCs) — five defaults you should know",
            body_html="""    <p><strong>SCCs</strong> are OCP\'s admission system for Pod-security. Predates K8s\' Pod Security Admission (PSA). Bound to ServiceAccounts; the Pod\'s SA must be granted an SCC for the Pod to run.</p>
    <p>Built-in SCCs (most-restrictive to least):</p>
    <ul>
      <li><strong>restricted-v2</strong> (default) — non-root, drop all caps + add NET_BIND_SERVICE, seccomp RuntimeDefault, no hostPath/hostNet/hostPID/hostIPC, no privileged. <em>Where every workload should aim.</em></li>
      <li><strong>nonroot-v2</strong> — must run as non-root (no UID 0); slightly less restrictive on capabilities.</li>
      <li><strong>anyuid</strong> — allows any UID. For workloads that hard-code UID (legacy images). Avoid where possible.</li>
      <li><strong>hostnetwork</strong> — allows hostNetwork (sees host\'s network namespace). For node-level networking workloads.</li>
      <li><strong>privileged</strong> — full root + caps + host access. Only for cluster-critical infra (CSI drivers, low-level monitoring agents).</li>
    </ul>
    <p><strong>SCC vs PSA:</strong> OCP supports both. PSA labels are honored on namespaces; SCC admission runs in addition. <em>Default OCP namespaces are pre-labelled with PSA <code>restricted</code>; SCC admission enforces parallel constraints.</em> For new workloads, design for restricted-v2 + PSA restricted; only escalate when proven needed.</p>"""),
        Section(eyebrow="Section 1.3 · Compliance + RHACS", h2="Compliance Operator + RHACS (StackRox)",
            body_html="""    <p><strong>Compliance Operator</strong> — runs <em>OpenSCAP</em> scans against the cluster + nodes for compliance baselines: <strong>CIS</strong> (Kubernetes Benchmark), <strong>NIST 800-53</strong>, <strong>PCI-DSS</strong>, <strong>FedRAMP</strong>, <strong>HIPAA</strong>. Generates <code>ComplianceCheckResult</code> CRDs; suggests automated remediations via <code>ComplianceRemediation</code>. Schedule periodic scans via <code>ScanSettingBinding</code>.</p>
    <p><strong>File Integrity Operator (FIO)</strong> — AIDE-based file integrity monitoring on RHCOS. Detects unauthorized changes to critical filesystem paths (<code>/etc</code>, <code>/usr/bin</code>, etc.). Generates alerts on drift.</p>
    <p><strong>Security Profiles Operator (SPO)</strong> — manages seccomp + SELinux + AppArmor profiles as K8s resources. Bind to Pods via SPOD CRDs.</p>
    <p><strong>Red Hat Advanced Cluster Security (RHACS) / StackRox</strong> — comprehensive K8s security platform:
    <ul>
      <li><em>Vulnerability management</em> — image + deployment scans</li>
      <li><em>Compliance</em> — CIS, NIST, PCI-DSS dashboards</li>
      <li><em>Network graph</em> — visualises Pod-to-Pod traffic + suggests NetworkPolicies</li>
      <li><em>Runtime threat detection</em> — eBPF + audit-based; detects shells, miners, lateral movement</li>
      <li><em>Admission control</em> — block deploys violating policy at admission</li>
    </ul>
    <p>Multi-cluster: one RHACS Central manages many Secured Clusters across an organisation.</p>"""),
        Section(eyebrow="Section 1.4 · KMS + FIPS + sandboxed containers",
            h2="KMS + FIPS + OpenShift sandboxed containers (Kata)",
            body_html="""    <p><strong>KMS integration</strong> — etcd Secrets encryption with external KMS (AWS KMS, Azure Key Vault, GCP KMS, HashiCorp Vault). <code>EncryptionConfiguration</code> on the apiserver. Keys rotated externally; etcd holds ciphertext.</p>
    <p><strong>FIPS mode</strong> — install OCP with FIPS 140-2 validated cryptography. Set <code>fips: true</code> in install-config; cluster boots with FIPS kernel + crypto libraries. Required for federal / regulated workloads. Cannot toggle FIPS post-install.</p>
    <p><strong>Disconnected security</strong> — air-gapped clusters need security operators (Compliance, RHACS, FIO) installed via mirrored OperatorHub catalogs. RHACS Central sits inside the air-gap; Sensor pods on each cluster phone-home to it.</p>
    <p><strong>OpenShift sandboxed containers (Kata)</strong> — runs Pods in lightweight VMs (Kata Containers + KVM) for stronger isolation than runc. Per-Pod kernel; container escape doesn\'t reach host. <em>For multi-tenant workloads with untrusted code (CI runners, customer-submitted code, sensitive PII).</em> ~5-15% perf overhead on syscall-heavy workloads.</p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A Helm chart\'s Pod fails to start in OCP — admission rejects with \"unable to validate against any SCC.\" The Deployment runs as UID 0. What\'s the right path?",
        options=[("Grant the Pod\'s SA the <strong>privileged</strong> SCC.", False),
            ("Investigate why UID 0 is required; if avoidable, rewrite to non-root + restricted-v2. If genuinely needed (legacy hard-coded image), grant <strong>anyuid</strong> SCC scoped to that SA only.", True),
            ("Disable SCC admission.", False)],
        feedback="Default to restricted-v2 design; if UID 0 is truly required, anyuid is the minimum escalation. Privileged is for cluster-infra workloads only.",
    )},
    before_after_before='<p>Pre-OCP K8s security was DIY: bring-your-own RBAC discipline, no SCC equivalent, PSP (deprecated), separate compliance scanning tools, separate runtime detection (Falco, Sysdig). Multi-cluster security was scripts. FIPS was a kernel-config exercise. KMS integration was custom. Sandboxed containers required separate runtime install + OS support.</p>',
    before_after_after='<p>OCP ships <strong>integrated OAuth + 7 identity providers + OCP RBAC + 5 default SCCs</strong>; <strong>Compliance Operator</strong> for CIS/NIST/PCI/FedRAMP/HIPAA scans; <strong>File Integrity</strong> + <strong>Security Profiles</strong> Operators; <strong>RHACS / StackRox</strong> as the comprehensive K8s security platform; <strong>KMS</strong> integration via apiserver EncryptionConfiguration; <strong>FIPS mode</strong> at install; <strong>Kata sandboxed containers</strong> for stronger isolation.</p>',
    before_after_caption='<p class="ba-caption"><em>Layered defence with Red Hat-supported components: auth + SCC + compliance + runtime + hardware. Each layer is independently meaningful; together they\'re a defendable security story.</em></p>',
    analogy_intro_html='''<p>The <strong>Safety Office</strong> is the foundry\'s defence-in-depth headquarters. Four shifts.</p>
    <p>The <strong>Badge Window</strong> (OAuth + RBAC) issues badges to humans (HTPasswd / LDAP / OIDC) and worker-permits to robots (ServiceAccounts). Every visitor and worker passes here.</p>
    <p>The <strong>Safety Inspector\'s Booth</strong> (SCCs) checks every Pod against the regulations. <em>restricted-v2</em> is the default uniform; some specialty workers need <em>anyuid</em> exceptions; only critical infrastructure gets <em>privileged</em>.</p>
    <p>The <strong>Compliance Auditor\'s Office</strong> (Compliance Operator + File Integrity + Security Profiles) runs scheduled audits against CIS/NIST/PCI/FedRAMP/HIPAA — generates checklists with auto-remediation suggestions. The <strong>RHACS Watchtower</strong> (StackRox) monitors live: vulnerability scanning, network graph, runtime threat detection, admission control.</p>
    <p>The <strong>Hardware Vault</strong> handles silicon-level concerns: KMS-managed keys for etcd Secrets; FIPS-validated cryptography (chosen at install); Kata sandboxed containers for tenants with untrusted workloads.</p>''',
    translation_rows=[("Badge Window", "Integrated OAuth server + identity providers"),
        ("Worker permit", "ServiceAccount + RoleBinding"),
        ("Foundry-wide role book", "OCP RBAC (cluster-admin, admin, edit, view + system:*)"),
        ("Safety Inspector\'s rule book", "SCC list (restricted-v2, nonroot-v2, anyuid, hostnetwork, privileged)"),
        ("Default uniform", "restricted-v2 SCC"),
        ("Special-case exception", "anyuid / hostnetwork SCC"),
        ("Cluster-critical-infra-only badge", "privileged SCC"),
        ("Compliance Auditor\'s checklists", "Compliance Operator (CIS / NIST / PCI / FedRAMP / HIPAA scans)"),
        ("File-integrity tripwires", "File Integrity Operator (AIDE-based)"),
        ("Seccomp / SELinux profile bindings", "Security Profiles Operator"),
        ("Comprehensive watchtower", "RHACS / StackRox (vuln + compliance + network + runtime + admission)"),
        ("Hardware vault keys", "KMS-encrypted etcd Secrets"),
        ("FIPS-validated crypto stamp", "FIPS install mode"),
        ("Untrusted-worker isolation cell", "OpenShift sandboxed containers (Kata)")],
    analogy_stops="A real Safety Office can\'t look inside Confidential VMs (Kata); SCC bypass via cluster-admin escalation is a real risk the metaphor doesn\'t capture.",
    eli5="The Safety Office checks badges, enforces uniform rules, runs surprise inspections, watches camera feeds, and maintains the vault. Each shift has a different job; together they keep the foundry safe.",
    eli10="OCP security = OAuth + identity providers + OCP RBAC + ServiceAccounts (authN/Z); SCCs (restricted-v2 default, nonroot-v2, anyuid, hostnetwork, privileged) for Pod-security; Compliance Operator + File Integrity + Security Profiles for compliance; RHACS / StackRox for runtime + admission + network + vuln; KMS for etcd Secrets; FIPS install mode; Kata sandboxed containers for stronger isolation.",
    scenarios=[
        Scenario(name="Bank — RHACS multi-cluster + Compliance Operator + KMS + FIPS",
            body="A bank\'s OCP fleet (10 prod clusters) runs RHACS multi-cluster — Central manages all Secured Clusters\' policies. Compliance Operator runs weekly PCI-DSS scans; results aggregated in RHACS Central. KMS integration with on-prem HashiCorp Vault for etcd Secrets. FIPS install mode (cannot retrofit; chosen at install)."),
        Scenario(name="Telco — Kata for untrusted CI tenants",
            body="Telco runs CI for partner integrations on a shared OCP cluster. Risk: malicious build escapes container, attacks node. Solution: dedicated node pool with Kata runtime; CI Pods scheduled there via runtimeClassName. Each Pod runs in its own KVM-backed lightweight VM. <em>Container escape doesn\'t cross VM boundary.</em>"),
        Scenario(name="SaaS — Compliance Operator finds 73 non-compliant manifests",
            body="A SaaS enables Compliance Operator with the CIS Kubernetes profile. Initial scan: 73 ComplianceCheckResult failures. Operator suggests ComplianceRemediation manifests for ~50 of them (auto-applicable). Manual fixes for the other 23. <em>CIS score from 41% to 94% in 2 weeks.</em>"),
        Scenario(name="anyuid escalation reverted — workload rewritten to non-root",
            body="A team discovered their Helm chart granted anyuid 18 months ago for a single Deployment. They rewrote the chart to use a non-root user UID, removed the SA-to-anyuid binding. <em>Posture improved; restricted-v2 enforced cluster-wide; one less escalation drift to monitor.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"SCCs are obsolete since PSA exists.\"",
            truth="OCP supports both. PSA labels gate at the K8s level; SCCs gate at the OCP admission webhook level. They\'re complementary; both run in modern OCP. SCCs predate PSA and remain Red Hat-supported. Don\'t remove SCCs; design for both."),
        Misconception(myth="\"FIPS can be enabled later.\"",
            truth="FIPS mode is an <strong>install-time choice</strong> via <code>fips: true</code> in install-config. The cluster boots with FIPS-validated crypto libraries + kernel. Cannot retrofit on existing clusters; requires reinstall. Plan + decide at install for federal / regulated workloads."),
        Misconception(myth="\"Kata sandboxed containers solve all multi-tenancy security problems.\"",
            truth="Kata adds <strong>strong isolation between Pods</strong> (per-Pod kernel via lightweight VM). It doesn\'t solve: identity sprawl, RBAC drift, NetworkPolicy gaps, secret rotation, image supply chain. Layer Kata on top of those; not as a replacement."),
    ],
    flashcards=[
        Flashcard(front="Five default OCP SCCs?", back="<strong>restricted-v2</strong> (default — non-root + drop caps + seccomp), <strong>nonroot-v2</strong> (no UID 0), <strong>anyuid</strong> (any UID — for legacy images), <strong>hostnetwork</strong> (host net namespace), <strong>privileged</strong> (full root + caps — cluster-infra-only)."),
        Flashcard(front="What does the Compliance Operator do?", back="Runs OpenSCAP scans against the cluster + nodes against compliance baselines (CIS K8s Benchmark, NIST 800-53, PCI-DSS, FedRAMP, HIPAA). Generates ComplianceCheckResult + ComplianceRemediation CRDs; auto-remediation suggestions."),
        Flashcard(front="What is RHACS / StackRox?", back="Red Hat Advanced Cluster Security — comprehensive K8s security platform: vulnerability mgmt, compliance dashboards, network graph + suggested NetworkPolicies, runtime threat detection (eBPF + audit), admission control. Multi-cluster: one Central, many Secured Clusters."),
        Flashcard(front="OCP\'s identity providers?", back="HTPasswd, LDAP, OIDC (Keycloak / Okta / Auth0), GitHub, GitLab, Google, Keystone, RequestHeader, BasicAuth. Configured via OAuth/cluster CR. Multiple coexist."),
        Flashcard(front="What is FIPS mode and when set?", back="Install-time choice (<code>fips: true</code> in install-config). Cluster boots with FIPS 140-2 validated crypto libraries + kernel. For federal / regulated workloads. Cannot toggle post-install — plan at install."),
        Flashcard(front="What\'s the difference between SCC and PSA?", back="<strong>SCC</strong> = OCP-native admission webhook (predates PSA). <strong>PSA</strong> = K8s-native namespace-label-based (privileged / baseline / restricted). OCP runs both — design for restricted-v2 SCC + restricted PSA together."),
        Flashcard(front="When use OpenShift sandboxed containers (Kata)?", back="Multi-tenant workloads where stronger isolation than runc is needed: untrusted CI runners, customer-submitted code, sensitive-PII workloads. Per-Pod KVM-backed lightweight VM; container escape doesn\'t reach host. ~5-15% syscall overhead."),
        Flashcard(front="What does the File Integrity Operator do?", back="AIDE-based file-integrity monitoring on RHCOS nodes. Detects unauthorized changes to critical filesystem paths (/etc, /usr/bin, etc.). Generates alerts on drift. For tamper detection on immutable nodes."),
    ],
    quizzes=[
        Quiz(prompt="A Pod fails to start: \"unable to validate against any SCC.\" Walk through the diagnostic.",
            answer="(1) <code>oc describe pod &lt;name&gt;</code> — admission denial messages list the failing SCC checks. (2) Identify the Pod\'s SA. (3) <code>oc get pod &lt;name&gt; -o yaml</code> — what does the Pod request (runAsUser, capabilities, hostPath, etc.)? (4) Compare against the SA\'s currently-granted SCCs: <code>oc adm policy who-can use scc/restricted-v2</code>. (5) Determine fix: rewrite Pod to fit restricted-v2 (best); OR grant the SA an SCC that allows the Pod\'s requests (<code>oc adm policy add-scc-to-user nonroot-v2 -z &lt;sa&gt;</code>); use the most restrictive SCC that satisfies the Pod\'s needs. Don\'t default to privileged."),
        Quiz(prompt="The Compliance Operator scan reports 73 PCI-DSS failures. The team has 2 sprints to remediate. What\'s the workflow?",
            answer="(1) <code>oc get compliancecheckresult -n openshift-compliance</code> — full list of failures + severity. (2) <code>oc get complianceremediation -n openshift-compliance</code> — auto-applicable remediations (the operator generated). (3) Filter by severity: high-severity failures first. (4) Apply remediations: <code>oc patch compliancecheckresult/&lt;name&gt; --type=merge -p \'{\"metadata\":{\"annotations\":{\"compliance.openshift.io/apply-remediation\":\"\"}}}\'</code>. Some remediations are MachineConfigs (require node reboot via MCO drain); plan a maintenance window. (5) Manual fixes for non-auto-remediable (typically RBAC + NetworkPolicy issues). (6) Re-run scan; track score over time. Target: 95%+ pass; document exceptions for the rest."),
        Quiz(prompt="It\'s an audit Saturday. Auditor asks: \"Show me your runtime threat detection.\" The team has RHACS deployed. Walk through the demo.",
            answer="(1) Open RHACS Central UI. (2) Navigate to <em>Violations</em> — recent runtime detections (suspicious shell-in-container, unexpected process exec, lateral-movement attempts, crypto-miner signatures). (3) Click a violation: see Pod, image, SA, deployment, attack details, MITRE ATT&amp;CK technique. (4) Show the <em>Network graph</em> — visual east-west traffic; flag deployments without NetworkPolicy. (5) Show <em>Vulnerability mgmt</em> — recent CVEs in running images. (6) Show <em>Compliance</em> dashboard — PCI/CIS scores. (7) Show <em>Admission policies</em> — which deploys were rejected at admission. <em>One pane for posture + runtime + admission across the fleet.</em>",
            cyoa=True, cyoa_tag="how the audit demo went"),
    ],
    glossary=[
        GlossaryItem(name="OAuth (OCP)", definition="OCP\'s integrated OAuth server + identity provider configuration via OAuth/cluster CR."),
        GlossaryItem(name="Identity provider (IDP)", definition="HTPasswd, LDAP, OIDC, GitHub, GitLab, Google, Keystone, RequestHeader, BasicAuth. Multiple coexist."),
        GlossaryItem(name="OCP RBAC roles", definition="cluster-admin, admin (project), edit (project), view (project), plus system:* roles. <code>oc adm policy</code> grants."),
        GlossaryItem(name="ServiceAccount (default Project SAs)", definition="Every Project gets default, builder, deployer SAs. Custom SAs for scoped workloads."),
        GlossaryItem(name="SCC (Security Context Constraint)", definition="OCP admission system for Pod-security. Bound to ServiceAccounts. Pod\'s SA must be granted an SCC for Pod to run."),
        GlossaryItem(name="restricted-v2 SCC", definition="OCP\'s default. Non-root, drop all caps + add NET_BIND_SERVICE, seccomp RuntimeDefault, no host*, no privileged."),
        GlossaryItem(name="Compliance Operator", definition="OpenSCAP scans against CIS / NIST / PCI / FedRAMP / HIPAA. ComplianceCheckResult + ComplianceRemediation CRDs."),
        GlossaryItem(name="File Integrity Operator (FIO)", definition="AIDE-based file-integrity monitoring on RHCOS. Detects drift on critical paths."),
        GlossaryItem(name="Security Profiles Operator (SPO)", definition="Manages seccomp + SELinux + AppArmor profiles as K8s resources via SPOD."),
        GlossaryItem(name="RHACS / StackRox", definition="Red Hat Advanced Cluster Security. Vuln + compliance + network + runtime + admission. Multi-cluster (Central + Secured)."),
        GlossaryItem(name="KMS integration", definition="External KMS (AWS / Azure / GCP / Vault) for etcd Secrets encryption via apiserver EncryptionConfiguration."),
        GlossaryItem(name="FIPS mode", definition="Install-time choice; cluster boots with FIPS 140-2 validated crypto libs + kernel. Cannot retrofit."),
        GlossaryItem(name="OpenShift sandboxed containers (Kata)", definition="Per-Pod KVM-backed lightweight VM runtime. Stronger isolation than runc. ~5-15% syscall overhead."),
    ],
    recap_lead='Four shifts: authN/Z (OAuth + RBAC + SAs), SCCs (restricted-v2 default), compliance + RHACS, hardware (KMS / FIPS / Kata).',
    recap_next='<strong>Next — O5: Operators and OLM.</strong> Operator Hub + CatalogSources + Subscriptions + InstallPlans + ClusterServiceVersions (CSV) + OperatorGroups + channels + manual vs automatic approval; Operator dependencies; broken-operator recovery; certified vs community vs custom operators.',
)
