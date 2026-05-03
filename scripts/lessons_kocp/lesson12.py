"""K-OCP O12 — OpenShift Troubleshooting (must-gather, CO degraded, MCP degraded, SCC, OAuth, etcd recovery)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OCP troubleshooting — failure patterns + diagnostic toolkit.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Diagnostic Lab — OCP-specific triage</text>
  <rect x="40" y="65" width="320" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="200" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">eight failure pattern families</text>
  <text x="200" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">1. ClusterOperator degraded · CVO blocked</text>
  <text x="200" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">2. MachineConfigPool degraded · Node NotReady</text>
  <text x="200" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">3. SCC denial · Pod admission</text>
  <text x="200" y="144" text-anchor="middle" font-size="9" fill="#FFFFFF">4. Route / cert / internal registry failure</text>
  <text x="200" y="157" text-anchor="middle" font-size="9" fill="#FFFFFF">5. Build failure · CSV failed · CatalogSource issues</text>
  <text x="200" y="170" text-anchor="middle" font-size="9" fill="#FFFFFF">6. OVN-K · DNS Operator · OAuth · etcd · disconnected</text>
  <rect x="375" y="65" width="345" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="547" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">diagnostic toolkit</text>
  <text x="547" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">oc adm must-gather (default + targeted)</text>
  <text x="547" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">oc adm inspect (focused)</text>
  <text x="547" y="131" text-anchor="middle" font-size="9" fill="#FBF1D6">oc debug node/&lt;name&gt;</text>
  <text x="547" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">oc adm node-logs</text>
  <text x="547" y="157" text-anchor="middle" font-size="9" fill="#FBF1D6">Insights Advisor + Red Hat KCS</text>
  <text x="547" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">always start with ClusterOperator status</text>
</svg>"""


LESSON = LessonSpec(
    num="12", title_short="OCP troubleshooting",
    title_full="O12 · OpenShift Troubleshooting (CO degraded, MCP degraded, SCC, Routes, OAuth, etcd recovery, disconnected pull)",
    title_html="K-OCP O12 · OpenShift Troubleshooting",
    module_eyebrow="Module O12 · the Diagnostic Lab",
    hero_sub_html='Eight OCP-specific failure pattern families: <strong>CO degraded + CVO blocked</strong>, <strong>MachineConfigPool degraded + Node NotReady</strong>, <strong>SCC denial</strong>, <strong>Route + cert + internal registry failure</strong>, <strong>Build failure + Operator CSV failed + CatalogSource issues</strong>, <strong>OLM Subscription issues</strong>, <strong>OVN-K + DNS Operator + OAuth failures</strong>, <strong>etcd backup/restore + disconnected pull failures</strong>. Diagnostic toolkit: <code>oc adm must-gather</code> + targeted variants; <code>oc adm inspect</code>; <code>oc debug node</code>; <code>oc adm node-logs</code>; Insights Advisor + Red Hat Knowledge Centered Service (KCS).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"Production cluster cascading failure: Authentication CO degraded → console unreachable → image-registry CO degraded → builds failing → Pipelines stuck.\"</em> One root cause; many cascading symptoms. You don\'t know whether to focus on the OAuth failure (auth CO), the registry failure, or the network issue (DNS Operator) underlying both. The team has Insights but no run-book ordering for cascading-failure scenarios. <em>You\'re ten minutes in and don\'t know where to start.</em> Today\'s lesson: the OCP triage playbook + diagnostic toolkit.",
    stamp_html="<strong>OCP triage playbook: ClusterOperator status first → CVO state → MachineConfigPool roll status → recent Activity. Diagnostic toolkit: must-gather (default + targeted) + oc adm inspect + oc debug node. Eight common failure pattern families with documented recovery paths.</strong>",
    district_pin="ko-bay12", district_label="Diagnostic Lab",
    sections=[
        Section(eyebrow="Section 1.1 · CO + CVO + MCP triage", h2="ClusterOperator + CVO + MachineConfigPool triage",
            body_html="""    <p><strong>ClusterOperator (CO) degraded</strong> — the most common starting symptom. <code>oc get co</code> shows all CO\'s + their Available / Progressing / Degraded conditions. For each Degraded CO:</p>
    <ul>
      <li><code>oc describe co/&lt;name&gt;</code> — status conditions + reason.</li>
      <li><code>oc logs -n openshift-&lt;name&gt; deployment/&lt;operator&gt;</code> — operator logs.</li>
      <li>For some CO\'s: there\'s an OperatorHub-installed Operator behind it (e.g., authentication CO has multiple deployments).</li>
    </ul>
    <p><strong>CVO blocked</strong> — Cluster Version Operator can\'t make progress. <code>oc describe clusterversion</code>:
    <ul>
      <li>Conditions: Progressing, Failing, Available.</li>
      <li>Common: a CO\'s upgrade is failing → CVO pauses; resolve the CO failure first.</li>
      <li>Or: ClusterOperator dependency loop; check upgrade graph + admission webhooks.</li>
    </ul>
    <p><strong>MachineConfigPool (MCP) degraded</strong> — RHCOS roll failed.
    <ul>
      <li><code>oc describe mcp/&lt;pool&gt;</code> — node status, drain reason.</li>
      <li>Most common cause: PDB-blocked drain (node\'s workloads can\'t evict due to tight PDB).</li>
      <li><code>oc get nodes -o wide</code> — find the cordoned node; check why workloads can\'t drain.</li>
      <li>Recovery: relax PDB temporarily; manually evict workloads; re-roll the pool.</li>
    </ul>
    <p><strong>Node NotReady</strong> — kubelet not reporting ready.
    <ul>
      <li><code>oc adm node-logs &lt;node&gt;</code> — system logs.</li>
      <li><code>oc debug node/&lt;node&gt;</code> — privileged debug Pod on the node.</li>
      <li>Common: kubelet panic, container runtime (CRI-O) error, network partition.</li>
    </ul>"""),
        Section(eyebrow="Section 1.2 · SCC + Routes + registry + OAuth", h2="SCC denial + Routes + cert + registry + OAuth failures",
            body_html="""    <p><strong>SCC denial</strong> (\"unable to validate against any SCC\"):
    <ul>
      <li><code>oc describe pod &lt;name&gt;</code> — admission denial detail.</li>
      <li>Identify SA + currently-granted SCCs: <code>oc adm policy who-can use scc/restricted-v2</code>.</li>
      <li>Determine fix: rewrite Pod for restricted-v2 (preferred) OR grant the SA an appropriate SCC.</li>
    </ul>
    <p><strong>Route not working / cert issues</strong>:
    <ul>
      <li><code>oc describe route &lt;name&gt;</code> — admitted by IngressController? Cert valid?</li>
      <li><code>oc logs -n openshift-ingress deployment/router-default</code> — router runtime errors.</li>
      <li>NetworkPolicy: is openshift-ingress allowed to reach the namespace?</li>
      <li>For TLS: <code>openssl s_client -connect &lt;host&gt;:443 -servername &lt;host&gt;</code> — see what cert is served.</li>
    </ul>
    <p><strong>Internal registry failure</strong>:
    <ul>
      <li><code>oc get co/image-registry</code> — degraded? <code>oc describe</code> for reason.</li>
      <li>Most common: storage backend (PVC zone-mismatch, S3 endpoint unreachable, NooBaa down).</li>
      <li>Recovery: switch backend to S3 / NooBaa for zone-resilience; restart registry deployment.</li>
    </ul>
    <p><strong>OAuth failures</strong>:
    <ul>
      <li><code>oc get co/authentication</code> — degraded? <code>oc describe</code>.</li>
      <li>Identity provider unreachable (LDAP / OIDC endpoint down)?</li>
      <li>Cert chain issue (LDAP TLS cert expired)?</li>
      <li><code>oc logs -n openshift-authentication deployment/oauth-openshift</code>.</li>
    </ul>"""),
        Section(eyebrow="Section 1.3 · Build + CSV + Catalog + OVN-K + DNS", h2="Build + CSV + CatalogSource + OVN-K + DNS Operator failures",
            body_html="""    <p><strong>Build failure</strong>:
    <ul>
      <li><code>oc get builds -n &lt;ns&gt;</code> + <code>oc logs build/&lt;name&gt;</code>.</li>
      <li>Common: S2I builder image incompatibility (recently updated builder broke build); pin builder version in BuildConfig.</li>
      <li>Resource limits: builder Pod ran out of memory (typical for Java).</li>
    </ul>
    <p><strong>Operator CSV failed</strong>:
    <ul>
      <li><code>oc describe csv -n &lt;ns&gt; &lt;name&gt;</code> — failure reason.</li>
      <li>Common: missing CRD permissions, RBAC, image pull failure, dependency conflict.</li>
      <li>Recovery: delete Subscription + CSV; reinstall after fixing root cause.</li>
    </ul>
    <p><strong>CatalogSource failure / OLM Subscription stuck</strong>:
    <ul>
      <li><code>oc get catalogsource -n openshift-marketplace</code> + <code>oc describe</code>.</li>
      <li>Common: CatalogSource registry pod failing (image pull from disconnected registry; pod crash loop).</li>
      <li>Subscription stuck: check <code>oc describe sub &lt;name&gt;</code> — InstallPlan available? Approval mode? Channel issues?</li>
    </ul>
    <p><strong>OVN-Kubernetes issues</strong>:
    <ul>
      <li><code>oc get pods -n openshift-ovn-kubernetes</code> — ovnkube-master, ovnkube-node Pods healthy?</li>
      <li><code>oc adm must-gather --image=registry.redhat.io/openshift4/ose-must-gather:latest -- /usr/bin/gather_network_logs</code> — targeted network gather.</li>
      <li>Symptoms: cross-Pod traffic broken, NetworkPolicy not enforced, EgressIP failover stuck.</li>
    </ul>
    <p><strong>DNS Operator failures</strong>:
    <ul>
      <li><code>oc get co/dns</code> — degraded?</li>
      <li><code>oc get pods -n openshift-dns</code> — coredns + node-resolver Pods.</li>
      <li><code>oc rsh &lt;some-pod&gt; nslookup kubernetes.default</code> — DNS resolution from a Pod.</li>
    </ul>"""),
        Section(eyebrow="Section 1.4 · etcd recovery + disconnected pull + diagnostic toolkit",
            h2="etcd recovery + disconnected pull failures + the diagnostic toolkit",
            body_html="""    <p><strong>etcd backup/restore</strong> — disaster recovery procedure:
    <ul>
      <li>Backup: schedule <code>cluster-backup.sh</code> on a master node; ship snapshot off-cluster.</li>
      <li>Restore: documented multi-step procedure — declare disaster, restore snapshot to a single master, validate, re-add other masters. <strong>Practice this on a dev cluster before you need it.</strong></li>
      <li>etcd quorum loss without backup = cluster rebuild.</li>
    </ul>
    <p><strong>Disconnected pull failures</strong>:
    <ul>
      <li><code>oc describe pod &lt;name&gt;</code> — ImagePullBackOff with auth or NXDOMAIN error.</li>
      <li>Check <code>imageContentSourcePolicy</code> / <code>ImageDigestMirrorSet</code> CRs — are the public image refs being redirected to your mirror?</li>
      <li>Mirror registry reachable? Pod running? Auth secret valid?</li>
      <li><code>oc adm release info &lt;version&gt;</code> — list all images in the release; check each is mirrored.</li>
    </ul>
    <p><strong>Diagnostic toolkit:</strong>
    <ul>
      <li><strong><code>oc adm must-gather</code></strong> — full diagnostic bundle. Targeted: <code>--image=registry.redhat.io/&lt;operator&gt;-must-gather</code> for per-operator gather.</li>
      <li><strong><code>oc adm inspect</code></strong> — focused gather on specific namespaces / resources. Lighter than must-gather.</li>
      <li><strong><code>oc debug node/&lt;name&gt;</code></strong> — privileged debug Pod on a specific node. <code>chroot /host</code> for full node OS access.</li>
      <li><strong><code>oc adm node-logs &lt;node&gt; -u &lt;unit&gt;</code></strong> — system journal logs from a node.</li>
      <li><strong>Insights Advisor</strong> (console.redhat.com) — known-issue checks against your cluster.</li>
      <li><strong>Red Hat Knowledge Centered Service (KCS)</strong> — searchable knowledge base of known issues + fixes.</li>
    </ul>
    <p><strong>The standard playbook:</strong> (1) Insights Advisor for known issues; (2) <code>oc get co</code> for CO health; (3) <code>oc get clusterversion</code> for CVO state; (4) <code>oc get mcp</code> for node-roll state; (5) <code>oc adm must-gather</code> for support case + postmortem; (6) <code>oc debug node</code> for node-level investigation.</p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A ClusterOperator is Degraded. Where do you look first?",
        options=[("Restart all Pods.", False),
            ("<code>oc describe co/&lt;name&gt;</code> — status conditions + reason; then operator logs in <code>openshift-&lt;name&gt;</code> namespace.", True),
            ("Reinstall OCP.", False)],
        feedback="ClusterOperator describe gives the why. Logs from the operator deployment in openshift-* namespace give the actionable detail.",
    )},
    before_after_before='<p>Pre-OCP K8s troubleshooting was self-assembly: bring-your-own log search (kibana / loki / external), no consolidated diagnostic gather, no targeted Operator gathers. ClusterOperator + CVO concepts didn\'t exist (per-component upgrade trail). SCC was specific to OCP and engineers came from K8s without it. etcd backup was DIY scripts.</p>',
    before_after_after='<p>OCP ships <strong><code>oc adm must-gather</code></strong> as the canonical diagnostic gather; targeted variants per-operator. <strong>ClusterOperator + CVO + MCP</strong> as triage primitives. <strong>Insights Advisor</strong> as known-issue checker. Documented recovery procedures for etcd disaster recovery + disconnected pull failures + SCC denial + OVN-K + DNS + OAuth + Routes + etc. <em>Triage discipline + the right diagnostic surfaces.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Most OCP outages match a known pattern; the toolkit + playbook turn 4-hour wars into 15-minute recoveries.</em></p>',
    analogy_intro_html='''<p>The <strong>Diagnostic Lab</strong> at K-Foundry is where you go when something\'s wrong. The triage nurse asks the same questions every time, in the same order.</p>
    <p>First: <em>\"What does the master operator board (CVO) say?\"</em> Second: <em>\"Which specialty operators (CO\'s) are flashing red?\"</em> Third: <em>\"Are the floor crews (MCPs) stuck mid-roll?\"</em> Fourth: <em>\"What did Red Hat Insights flag yesterday?\"</em></p>
    <p>The wall has eight common diagnoses pinned: CO + CVO blockages, MCP + Node issues, SCC denials, Route/cert/registry failures, Build/CSV/Catalog issues, OVN-K + DNS Operator failures, OAuth issues, etcd recovery + disconnected pull failures. Each diagnosis has a one-page recovery procedure.</p>
    <p>The <strong>diagnostic toolkit</strong>: <code>must-gather</code> (full diagnostic bundle), <code>inspect</code> (focused), <code>debug node</code> (privileged on-node Pod), <code>adm node-logs</code> (system journal). Plus Insights + KCS (known-issue knowledge bases).</p>''',
    translation_rows=[("Master operator board", "Cluster Version Operator (CVO) status"),
        ("Specialty operators flashing", "ClusterOperator degraded"),
        ("Floor crew stuck mid-roll", "MachineConfigPool (MCP) degraded"),
        ("Operator stalled mid-shift", "Node NotReady"),
        ("Safety inspector denial", "SCC denial — \"unable to validate against any SCC\""),
        ("Conveyor door not opening", "Route admission failure / cert problem"),
        ("Internal-parts warehouse failure", "Internal registry CO degraded"),
        ("Stamp-press jam", "Build failure (S2I builder broke)"),
        ("Specialty-machine install failed", "CSV failed / Subscription stuck / CatalogSource down"),
        ("Foundry rail network partition", "OVN-K node-to-master partition"),
        ("Floor address book down", "DNS Operator failure"),
        ("Badge-printer broken", "OAuth failure"),
        ("Inventory snapshot rebuild", "etcd backup/restore"),
        ("Sealed warehouse pull failure", "Disconnected pull failure (mirror registry)"),
        ("Foundry-master diagnostic kit", "<code>oc adm must-gather</code> / <code>inspect</code> / <code>debug node</code>"),
        ("Foundry-network knowledge base", "Red Hat Insights Advisor + KCS")],
    analogy_stops="A real diagnostic lab can pause; OCP cascading failures can take down adjacent operators in minutes. The metaphor underplays the cascade-failure risk.",
    eli5="When something hurts, you check the master board first, then look for which operators are flashing red, then ask if any floor crews are stuck. The wall has 8 common diagnoses; pick the matching one.",
    eli10="OCP triage = (1) Insights Advisor for known issues, (2) <code>oc get co</code> for ClusterOperator health, (3) <code>oc get clusterversion</code> for CVO state, (4) <code>oc get mcp</code> for node-roll state, (5) <code>oc adm must-gather</code> for support case + postmortem, (6) <code>oc debug node</code> for node-level investigation. Eight failure pattern families: CO/CVO blocked, MCP/Node, SCC, Routes/cert/registry, Builds/CSV/Catalog, OLM Subscription, OVN-K/DNS/OAuth, etcd/disconnected.",
    scenarios=[
        Scenario(name="Cascading failure — DNS Operator down → 4 CO\'s degraded",
            body="DNS Operator goes degraded. Cascading: authentication CO can\'t reach LDAP, image-registry can\'t reach storage, build can\'t pull base images, console can\'t reach apiserver. <strong>Triage</strong>: identify root via Insights or <code>oc get co</code> + check timestamps; fix DNS (CoreDNS Pod CrashLoop, kubeconfig misconfig, NodeNetworkConfigurationPolicy regression); cascading CO\'s recover."),
        Scenario(name="MCP stuck — PDB deadlock during upgrade",
            body="MCP/worker stuck Updating for 90 min. <code>oc describe mcp/worker</code>: 1 node cordoned + drain blocked. <code>oc describe pod</code> on stuck workload: PDB <code>maxUnavailable: 0</code> + 3 replicas. Recovery: temporarily increase replicas to 4 (PDB allows 1 disruption when 4 exist); drain proceeds; restore replicas. Postmortem: document workload PDB requirements; pre-flight check before upgrades."),
        Scenario(name="SCC denial — anyuid escalation reverted",
            body="Helm chart fails admission: \"unable to validate against any SCC.\" Pod runs as UID 0. Investigation: image was built without USER directive (default = root). Fix: rewrite Dockerfile to <code>USER 1001</code>; rebuild; redeploy under restricted-v2 SCC. Avoids granting anyuid SCC permanently."),
        Scenario(name="etcd disaster recovery rehearsed quarterly",
            body="A bank simulates etcd quorum loss on a dev cluster. Documented procedure: declare disaster, stop etcd Pods on remaining masters, restore latest snapshot to one master via <code>etcdctl snapshot restore</code>, restart cluster operators, validate + re-add other masters. <em>Procedure validated; runbook current; team trained.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"must-gather is huge and slow — only run it for support cases.\"",
            truth="<strong>must-gather is a 5-15 min routine collection</strong>. Run it for any non-trivial incident, even if you don\'t open a Red Hat case. The bundle has ClusterOperator status, recent events, system logs, configs — all useful for postmortems. Targeted variants (per-operator) are smaller + faster."),
        Misconception(myth="\"Restart all Pods to fix it.\"",
            truth="<em>Almost never the right first step.</em> Pod restart is a last-resort symptom-treater. Always look at ClusterOperator status, CVO state, MCP roll status, Insights Advisor first. Pod restart hides root cause + may worsen cascading failures by retriggering scheduling pressure."),
        Misconception(myth="\"Insights is just nice-to-have telemetry.\"",
            truth="<strong>Insights Advisor surfaces known-issue checks against YOUR cluster</strong> — \"this version of cluster-network-operator has a known issue X; here\'s the KCS article.\" Saves hours of debugging when the issue is already documented. Disabled by default in air-gapped clusters; manually-fed knowledge base is the fallback."),
    ],
    flashcards=[
        Flashcard(front="OCP triage playbook — first 4 steps?", back="(1) <strong>Insights Advisor</strong> (known issues). (2) <code>oc get co</code> (ClusterOperator health). (3) <code>oc get clusterversion</code> (CVO state). (4) <code>oc get mcp</code> (MachineConfigPool roll state)."),
        Flashcard(front="ClusterOperator degraded — diagnostic command?", back="<code>oc describe co/&lt;name&gt;</code> — status conditions + reason. Then operator logs: <code>oc logs -n openshift-&lt;name&gt; deployment/&lt;operator&gt;</code>."),
        Flashcard(front="MachineConfigPool stuck — most common cause?", back="<strong>PDB-blocked drain</strong>: a node\'s workloads can\'t evict due to tight PodDisruptionBudgets. Fix: relax PDB temporarily OR scale replicas to give PDB headroom OR document + plan around the workload."),
        Flashcard(front="What is <code>oc adm must-gather</code>?", back="OCP\'s canonical diagnostic gather — collects ClusterOperator status, recent events, configs, logs into a tarball. Targeted variants per-operator: <code>--image=&lt;operator&gt;-must-gather</code>."),
        Flashcard(front="What is <code>oc adm inspect</code>?", back="Focused gather on specific namespaces / resources. Lighter than must-gather. For when you know which scope you need + don\'t want the full bundle."),
        Flashcard(front="What is <code>oc debug node/&lt;name&gt;</code>?", back="Privileged debug Pod on a specific node. <code>chroot /host</code> for full node OS access. Replaces SSH (RHCOS disabled SSH by default)."),
        Flashcard(front="SCC denial Pod won\'t start — diagnostic ladder?", back="(1) <code>oc describe pod</code> — admission denial detail. (2) Identify the Pod\'s SA. (3) <code>oc adm policy who-can use scc/restricted-v2</code> + match against Pod\'s SCC requirements. (4) Determine fix: rewrite Pod for restricted-v2 (preferred) OR grant SA appropriate SCC."),
        Flashcard(front="What\'s Insights Advisor?", back="Red Hat\'s known-issue check service. console.redhat.com surfaces issues + KCS articles for YOUR cluster based on Insights telemetry. Disabled in air-gapped — manual KCS lookup is fallback."),
    ],
    quizzes=[
        Quiz(prompt="A cluster\'s authentication CO has been degraded for 2 hours. Walk through the diagnostic ladder.",
            answer="(1) <code>oc get co/authentication</code> — confirm Degraded + check timestamps. (2) <code>oc describe co/authentication</code> — status conditions + reason (often points to OAuth backend issue or specific Pod failure). (3) <code>oc get pods -n openshift-authentication</code> — oauth-openshift Pods. (4) <code>oc logs -n openshift-authentication deployment/oauth-openshift</code> — runtime errors. (5) Common causes: identity provider unreachable (LDAP / OIDC down), TLS cert expired on IDP, NetworkPolicy blocking, kube-apiserver issue. (6) Insights Advisor for known issues. (7) <code>oc adm must-gather</code> + open Red Hat case if root cause unclear."),
        Quiz(prompt="Disconnected cluster: new Operator install fails ImagePullBackOff. Walk through diagnostic.",
            answer="(1) <code>oc describe pod</code> — exact image ref + error (auth or NXDOMAIN). (2) <code>oc get imagecontentsourcepolicy + imagedigestmirrorset</code> — is the public image ref redirected to the mirror? (3) Mirror registry: reachable from cluster? (resolve DNS + curl from a debug Pod) (4) <code>oc adm release info &lt;ocp-version&gt;</code> + check whether the new Operator\'s catalog images are mirrored. (5) Likely fix: <code>oc-mirror</code> the missing images to mirror; restart pull. (6) For Operator install: ensure CatalogSource pod is healthy + can pull catalog index image."),
        Quiz(prompt="Saturday at the SCIF. The on-call has a cascading failure: console down, Pipelines stuck, builds failing. Walk through triage.",
            answer="(1) <strong>Don\'t panic — find the root via CO status.</strong> <code>oc get co</code> from a working terminal: which CO\'s are Degraded with the earliest timestamp? Often DNS Operator, image-registry, or authentication = upstream root cause. (2) <code>oc get clusterversion + oc describe clusterversion</code> for CVO state. (3) <code>oc get mcp</code> for any node-roll issues. (4) Likely scenario: DNS or image-registry root cause; cascading symptoms in pipelines / builds. (5) Address root cause first; cascading CO\'s recover. (6) <code>oc adm must-gather</code> bundle for postmortem. (7) Update runbook with the cascade order: \"if DNS / registry / authentication fails, expect builds / pipelines / console to follow within minutes.\" <em>Cascading failures look complex; usually have one root cause.</em>",
            cyoa=True, cyoa_tag="how the cascading failure was triaged"),
    ],
    glossary=[
        GlossaryItem(name="oc adm must-gather", definition="OCP\'s canonical diagnostic bundle: ClusterOperator status, events, logs, configs. Targeted variants per-operator."),
        GlossaryItem(name="oc adm inspect", definition="Focused gather on specific namespaces / resources. Lighter than must-gather."),
        GlossaryItem(name="oc debug node/<name>", definition="Privileged debug Pod on a node. <code>chroot /host</code> for full node OS access. Replaces SSH on RHCOS."),
        GlossaryItem(name="oc adm node-logs", definition="System journal logs from a node. e.g., <code>oc adm node-logs &lt;node&gt; -u kubelet</code>."),
        GlossaryItem(name="ClusterOperator (CO) Degraded", definition="One of ~30 CO\'s reports unhealthy. Most common starting symptom for OCP outages."),
        GlossaryItem(name="CVO blocked", definition="Cluster Version Operator can\'t make progress; usually because a CO\'s upgrade is failing or admission webhooks are blocking."),
        GlossaryItem(name="MachineConfigPool (MCP) Degraded", definition="RHCOS roll failed; commonly PDB-blocked drain on a worker node."),
        GlossaryItem(name="SCC denial", definition="\"unable to validate against any SCC.\" Pod\'s SA doesn\'t have an SCC that allows the Pod\'s requested security context."),
        GlossaryItem(name="Insights Advisor", definition="Red Hat known-issue check surface in console.redhat.com. Disabled in air-gapped; manual KCS fallback."),
        GlossaryItem(name="KCS (Knowledge Centered Service)", definition="Red Hat\'s searchable knowledge base of known issues + fixes."),
        GlossaryItem(name="etcd disaster recovery", definition="Documented multi-step procedure for restoring from etcd backup after quorum loss. Practice on dev cluster."),
        GlossaryItem(name="Disconnected pull failure", definition="ImagePullBackOff in air-gapped cluster — typically missing imageContentSourcePolicy / ImageDigestMirrorSet redirect, or mirror registry pod down."),
    ],
    recap_lead='Eight failure pattern families + diagnostic toolkit (must-gather + inspect + debug node + Insights + KCS). Triage discipline turns 4-hour wars into 15-minute recoveries.',
    recap_next='<strong>Next — O13: K-OCP Capstone.</strong> Multi-tenant OCP platform (IPI on bare metal or AWS) with ODF + RHACS + OpenShift GitOps + Pipelines + Virtualization workload + RHACM federation; full SCC design + disconnected update + must-gather pack.',
)
