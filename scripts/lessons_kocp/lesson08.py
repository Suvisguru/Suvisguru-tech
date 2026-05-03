"""K-OCP O8 — OpenShift Operations (ClusterVersion + EUS + MCO + MachineSets + etcd backup + must-gather)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OCP operations — ClusterVersion + update channels + EUS + MCO + MachineSets + etcd backup + must-gather + Insights.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Maintenance Bay — versions, machines, backups, upgrades</text>
  <rect x="40" y="65" width="170" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="125" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">version + channels</text>
  <text x="125" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">ClusterVersion + CVO</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">stable / fast / candidate</text>
  <text x="125" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">EUS (Extended Update)</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">~24 mo support</text>
  <rect x="225" y="65" width="170" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="310" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">machines + nodes</text>
  <text x="310" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">MachineConfig + MCO</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">MachineConfigPools</text>
  <text x="310" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">MachineSets</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">MachineHealthChecks</text>
  <rect x="410" y="65" width="170" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="495" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">backup + DR</text>
  <text x="495" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">etcd backup</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">must-gather</text>
  <text x="495" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">Insights telemetry</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">support cases</text>
  <rect x="595" y="65" width="125" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="657" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">upgrades</text>
  <text x="657" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">disconnected updates</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">mirror + oc-mirror</text>
  <text x="657" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">upgrade risk</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">assessment</text>
</svg>"""


LESSON = LessonSpec(
    num="08", title_short="OCP operations",
    title_full="O8 · OpenShift Operations (ClusterVersion + EUS + MCO + MachineSets + etcd backup + must-gather)",
    title_html="K-OCP O8 · OpenShift Operations",
    module_eyebrow="Module O8 · the Maintenance Bay",
    hero_sub_html='<strong>ClusterVersion + CVO</strong> + update channels (stable / fast / candidate) + <strong>EUS (Extended Update Support)</strong> for ~24-month support. <strong>MachineConfigPools</strong> + <strong>MachineSets</strong> + <strong>MachineHealthChecks</strong>. Node maintenance + drain + tuning + performance profiles. <strong>etcd backup</strong>, <strong>oc adm must-gather</strong>, <strong>Insights telemetry</strong>, support cases. <strong>Disconnected updates</strong> via mirror registry + oc-mirror. <strong>Upgrade risk assessment</strong> tooling.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"Upgrade hung at 75%; ClusterOperator monitoring degraded; CVO progressing for 3 hours.\"</em> The cluster started a minor upgrade Saturday night during the maintenance window. The MCO drained a node; PDB on a critical workload blocked the drain; node stays cordoned + workloads can\'t move; CVO can\'t complete the upgrade until the MCP rolls. <em>You don\'t know the upgrade rollback story; you don\'t know whether to break the PDB or wait.</em> Today\'s lesson: ClusterVersion lifecycle + MachineConfig/MCP rollouts + etcd backup + must-gather + EUS planning + disconnected updates.",
    stamp_html="<strong>CVO orchestrates ClusterOperators on a channel; pick stable for prod, fast for canary, EUS for regulated. MCO + MachineConfigPools roll node configs sequentially with PDB-aware drain. Always wire etcd backup + mirror registry + must-gather before you need them.</strong>",
    district_pin="ko-bay08", district_label="Maintenance Bay",
    sections=[
        Section(eyebrow="Section 1.1 · ClusterVersion + channels + EUS", h2="ClusterVersion + update channels + EUS",
            body_html="""    <p><strong>ClusterVersion</strong> CR holds the cluster\'s declared + observed version. Edit <code>spec.desiredUpdate</code> or <code>spec.channel</code> to trigger upgrades; CVO orchestrates the rollout across all ClusterOperators.</p>
    <p><strong>Update channels:</strong>
    <ul>
      <li><strong>stable-X.Y</strong> (e.g., <code>stable-4.18</code>) — production. Bug + security fixes within minor X.Y; minor upgrades via channel switch.</li>
      <li><strong>fast-X.Y</strong> — earlier access to newer GA minors. Slightly less baked than stable.</li>
      <li><strong>candidate-X.Y</strong> — release candidates. Pre-production validation only.</li>
      <li><strong>eus-X.Y</strong> — <strong>EUS (Extended Update Support)</strong> channels: ~24-month support windows for designated minor versions. EUS-to-EUS upgrade path (e.g., 4.16 EUS → 4.18 EUS skipping 4.17). For workloads that cannot upgrade quarterly.</li>
    </ul>
    <p><strong>OCP version support:</strong> Red Hat supports at least 4 minors concurrently with phased lifecycles (Full Support → Maintenance Support → Extended Update Support — EUS). Plan upgrades against the support matrix; track EOS dates per minor.</p>
    <p><strong>OpenShift Update Service (OSUS)</strong> serves the upgrade graph. Public clusters fetch from api.openshift.com; disconnected clusters need their own OSUS instance fed by mirrored upgrade-graph data.</p>"""),
        Section(eyebrow="Section 1.2 · MachineConfig + MCP + MachineSet + MHC", h2="MachineConfig + MachineConfigPools + MachineSets + MachineHealthChecks",
            body_html="""    <p><strong>MachineConfig</strong> = declarative RHCOS node config (kernel args, systemd units, files, ignition snippets). Multiple MachineConfig YAMLs are <em>merged</em> per-pool by the MCO into a final rendered config.</p>
    <p><strong>MachineConfigPool (MCP)</strong> = group of nodes sharing a MachineConfig roll. Defaults: <code>master</code> + <code>worker</code> pools. Custom pools via labels for shape-specific configs (e.g., GPU nodes, FIPS nodes, infra nodes).</p>
    <p>When a MachineConfig changes, the MCO renders the new config + rolls the pool: cordon → drain (PDB-aware) → apply config → reboot → uncordon → next node. MCP status: <code>Updated</code> (steady) / <code>Updating</code> (in flight) / <code>Degraded</code> (failed).</p>
    <p><strong>MachineSets</strong> = analogous to ReplicaSets but for the cluster\'s VMs/instances. Cluster Autoscaler scales MachineSets up/down based on Pending Pods. Per-MachineSet: provider config (instance type, AZ, IAM, disk), Machine template.</p>
    <p><strong>MachineHealthChecks (MHC)</strong> = automatic remediation for unhealthy Machines. Define conditions (NotReady > 5min, etc.); MHC deletes + recreates the Machine via the MachineSet.</p>
    <p><strong>Node tuning + performance profiles:</strong> <strong>Node Tuning Operator</strong> + <strong>PerformanceProfile</strong> CR = CPU pinning, hugepages, RT kernel, NUMA-aware tuning. For telco / latency-sensitive workloads.</p>"""),
        Section(eyebrow="Section 1.3 · etcd backup + must-gather + Insights", h2="etcd backup + must-gather + Insights telemetry + support cases",
            body_html="""    <p><strong>etcd backup</strong> = single point of cluster-state truth. Regular backup is mandatory:</p>
    <ul>
      <li>Run <code>oc debug node/&lt;master&gt;</code> + invoke <code>cluster-backup.sh</code> on a master node — produces snapshot + static-pod manifests.</li>
      <li>Schedule via CronJob hosted on infra nodes; ship snapshots off-cluster (S3 / NFS / NetApp).</li>
      <li>Hourly + daily + weekly retention typical.</li>
    </ul>
    <p><strong>oc adm must-gather</strong> = collects diagnostic bundle (logs, configs, ClusterOperator status, events) for a cluster issue. Plus targeted gathers per Operator (e.g., <code>oc adm must-gather --image=registry.redhat.io/openshift-logging/cluster-logging-rhel9-operator-must-gather</code>). Bundle = tarball you attach to support cases.</p>
    <p><strong>oc adm inspect</strong> = focused gather on specific namespaces/resources. Lighter than must-gather.</p>
    <p><strong>Insights telemetry</strong> = OCP\'s phone-home (opt-out): cluster identifies itself to Red Hat Insights, sends anonymised health + version + ClusterOperator status. Red Hat Insights surfaces recommendations + known-issue alerts in console.redhat.com. <em>For air-gapped clusters: opt-out + manage manually.</em></p>
    <p><strong>Support cases:</strong> Red Hat Customer Portal. Include must-gather + ClusterVersion + relevant Operator logs. SLA per support tier.</p>"""),
        Section(eyebrow="Section 1.4 · disconnected updates + upgrade risk assessment",
            h2="Disconnected updates + upgrade risk assessment",
            body_html="""    <p><strong>Disconnected (air-gapped) updates:</strong>
    <ul>
      <li>On internet-connected staging: <code>oc-mirror --config imageset-config.yaml</code> pulls new release + Operator updates.</li>
      <li>Sneakernet (or one-way data diode) to air-gapped facility.</li>
      <li>Internal mirror registry: <code>oc-mirror --from tarball.tar --to docker://mirror.example.com</code>.</li>
      <li>Disconnected OSUS Operator updates the upgrade graph.</li>
      <li>ClusterVersion shows new versions; admin upgrades via <code>oc adm upgrade</code>.</li>
    </ul>
    <p><strong>Upgrade risk assessment:</strong>
    <ul>
      <li><strong>Conditional upgrades</strong>: OCP\'s upgrade graph flags certain upgrade paths as conditionally risky based on cluster characteristics (e.g., specific Operator versions, custom MachineConfigs). CVO surfaces them in <code>oc adm upgrade</code>.</li>
      <li><strong>Insights Advisor</strong>: known-issue checks against your cluster.</li>
      <li><strong>RHACM Cluster Lifecycle</strong> (covered in O10): fleet-wide upgrade orchestration.</li>
      <li><strong>kube-no-trouble + Pluto</strong> for deprecated K8s API usage in workloads.</li>
    </ul>
    <p><strong>Upgrade order:</strong> control plane (CVO) → ClusterOperators → worker MCPs (one MCP at a time, PDB-aware). Master MCP rolls in parallel with CVO; worker MCPs roll after CO\'s converge. EUS-to-EUS skips the intermediate minor.</p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A team wants to skip OCP 4.17 and go from 4.16 EUS directly to 4.18 EUS. Is that possible?",
        options=[("No — must upgrade through every minor.", False),
            ("Yes — EUS-to-EUS upgrade paths exist. Switch channel from <code>eus-4.16</code> to <code>eus-4.18</code>; CVO traverses the EUS-aware graph that allows skipping non-EUS intermediate minors.", True),
            ("Only with Red Hat support intervention.", False)],
        feedback="EUS channels enable EUS-to-EUS skip-minor upgrades. The graph defines acceptable jumps; CVO orchestrates.",
    )},
    before_after_before='<p>Pre-CVO + MCO, K8s upgrades meant per-component upgrade scripts + node OS reboots done by hand or with config management. No coherent ClusterVersion concept. EUS didn\'t exist; you upgraded every minor or fell off support. Disconnected updates were research projects.</p>',
    before_after_after='<p>OCP\'s lifecycle: <strong>ClusterVersion + CVO</strong> orchestrate ClusterOperator upgrades; <strong>MCO + MachineConfigPools</strong> roll RHCOS configs node-by-node with PDB-aware drain; <strong>MachineSets + MachineHealthChecks</strong> manage VM lifecycle + auto-remediation. <strong>EUS</strong> for ~24-month support windows. <strong>etcd backup</strong> + <strong>must-gather</strong> + <strong>Insights</strong> are first-class. <strong>Disconnected</strong> via mirror registry + oc-mirror.</p>',
    before_after_caption='<p class="ba-caption"><em>OCP upgrades are repeatable + auditable; pick channel by risk appetite + change-control cadence.</em></p>',
    analogy_intro_html='''<p>The <strong>Maintenance Bay</strong> is where the foundry stays running. Three crews operate.</p>
    <p>The <strong>Version Crew</strong> (CVO + ClusterOperators) tracks the foundry\'s declared version + ensures all 30+ specialty operators are at that version. Channels: stable, fast, candidate, EUS. EUS is the long-term-lease shop where designated versions get 24-month support.</p>
    <p>The <strong>Floor Crew</strong> (MCO + MachineConfigPools + MachineSets + MachineHealthChecks) maintains the foundry floors (RHCOS): rolls floor-config changes pool-by-pool, drains nodes with PDB safety, replaces failed machines automatically.</p>
    <p>The <strong>Records Crew</strong> (etcd backup + must-gather + Insights + support cases) keeps backups, runs diagnostic gathers when something breaks, and phones home to Red Hat Insights for known-issue alerts.</p>
    <p>For disconnected foundries: oc-mirror brings updates in via sneakernet; disconnected OSUS feeds the local upgrade graph.</p>''',
    translation_rows=[("Foundry version master record", "ClusterVersion CR"),
        ("Version Crew foreman", "Cluster Version Operator (CVO)"),
        ("Specialty operators on the floor", "ClusterOperators (~30 of them)"),
        ("Long-term lease shop", "EUS — Extended Update Support (~24 mo)"),
        ("Floor Crew foreman", "Machine Config Operator (MCO)"),
        ("Floor configuration recipe", "MachineConfig CR"),
        ("Floor crew zone", "MachineConfigPool (MCP) — master / worker / custom"),
        ("VM scale set", "MachineSet"),
        ("Auto-replace bad machine", "MachineHealthCheck (MHC)"),
        ("Workload-tuned node profile", "PerformanceProfile + Node Tuning Operator"),
        ("Foundry inventory backup", "etcd backup (cluster-backup.sh)"),
        ("Diagnostic kit", "<code>oc adm must-gather</code> / <code>oc adm inspect</code>"),
        ("Phone-home telemetry", "Insights — anonymised health to Red Hat"),
        ("Sneakernet update package", "oc-mirror tarball"),
        ("Local upgrade-graph feed", "Disconnected OSUS Operator"),
        ("Conditional upgrade warning", "Upgrade risk assessment in <code>oc adm upgrade</code>")],
    analogy_stops="A real maintenance crew can pause; OCP upgrades in flight need careful PDB planning to avoid mid-roll deadlock the metaphor doesn\'t capture.",
    eli5="Three maintenance crews keep the foundry running: one tracks software versions, one maintains the floors, one keeps records and backups. Long-term-lease customers get a special slow-cadence shop (EUS).",
    eli10="OCP ops = CVO orchestrating ClusterOperators on a channel (stable / fast / candidate / EUS); MCO + MachineConfigPools rolling RHCOS configs node-by-node PDB-aware; MachineSets + MHC manage VM lifecycle; etcd backup mandatory; oc adm must-gather + Insights for diagnosis + recommendations; disconnected via mirror registry + oc-mirror + disconnected OSUS; EUS for ~24-mo support windows + EUS-to-EUS skip-minor upgrades.",
    scenarios=[
        Scenario(name="Bank — EUS channel for the regulated payments cluster",
            body="A regulated bank\'s payments cluster runs OCP on the EUS channel. They hold on a designated EUS minor for ~24 months; EUS-to-EUS upgrade every 2 years. Avoids the per-minor change-control overhead. Premium support tier; stable Operators."),
        Scenario(name="Telco — performance profile + node tuning for 5G UPF",
            body="Telco running 5G UPF needs CPU pinning + hugepages + RT kernel. PerformanceProfile CR + Node Tuning Operator. Custom MachineConfigPool for these nodes. Latency targets under 100µs."),
        Scenario(name="Disconnected upgrade — sneakernet OCP minor update",
            body="Air-gapped SCIF facility. Internet-connected staging runs <code>oc-mirror</code> for the new OCP minor + selected Operators; tarball ships via sneakernet. Internal mirror registry updated; disconnected OSUS feeds the upgrade graph; ClusterVersion shows new minor available; admin upgrades during maintenance window."),
        Scenario(name="DR drill — etcd snapshot restored cluster in 50 minutes",
            body="A bank tests etcd disaster recovery quarterly. Backup taken; cluster simulated catastrophic etcd loss; restore from backup using the documented disaster-recovery procedure on a sibling cluster. <em>50 minutes total restore time; auditor satisfied with RTO.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"EUS means I never have to upgrade.\"",
            truth="EUS = ~24-month support window; you still upgrade — just every 2 years instead of every quarter. After EUS support ends for your version, you must move to the next EUS or current minor. Plan the EUS-to-EUS upgrade well in advance."),
        Misconception(myth="\"etcd is auto-backed-up by OCP.\"",
            truth="<strong>etcd backup is your responsibility.</strong> OCP doesn\'t auto-backup etcd by default. Schedule a CronJob or cron-on-master invoking <code>cluster-backup.sh</code>; ship snapshots off-cluster. Without etcd backup, a quorum-loss event = cluster rebuild from scratch."),
        Misconception(myth="\"must-gather is only for Red Hat support cases.\"",
            truth="must-gather is your <em>own</em> diagnostic tool too. Run it on incidents; bundles include ClusterOperator status, recent events, system logs, configs — useful for postmortem regardless of opening a Red Hat case. Plus targeted gathers per Operator give component-specific deep diagnostic data."),
    ],
    flashcards=[
        Flashcard(front="Update channels in OCP?", back="<strong>stable-X.Y</strong> (production), <strong>fast-X.Y</strong> (earlier GA), <strong>candidate-X.Y</strong> (release candidates), <strong>eus-X.Y</strong> (Extended Update Support, ~24 mo). Switch channel via <code>oc adm upgrade channel</code>."),
        Flashcard(front="What is EUS?", back="<strong>Extended Update Support</strong> — designated OCP minor versions with ~24-month support window. EUS-to-EUS upgrade paths skip non-EUS intermediate minors. For workloads that cannot upgrade quarterly."),
        Flashcard(front="MachineConfig + MCP + MachineSet — what does each manage?", back="<strong>MachineConfig</strong>: RHCOS node config (kernel args, systemd, files). <strong>MachineConfigPool (MCP)</strong>: group of nodes sharing a config roll (default: master, worker; custom for shape-specific). <strong>MachineSet</strong>: VM/instance scale set; CA scales these."),
        Flashcard(front="What is MachineHealthCheck (MHC)?", back="Automatic remediation for unhealthy Machines. Conditions (e.g., NotReady > 5min); MHC deletes + recreates the Machine via the MachineSet."),
        Flashcard(front="Where does Node Tuning Operator + PerformanceProfile fit?", back="Workload-tuned node configs: CPU pinning, hugepages, RT kernel, NUMA-aware. For telco / latency-sensitive workloads. Per-pool via custom MCP."),
        Flashcard(front="How do you backup etcd?", back="<code>oc debug node/&lt;master&gt;</code> + <code>cluster-backup.sh</code>. Schedule as CronJob on infra nodes; ship snapshots off-cluster (S3, NFS, NetApp). Hourly + daily + weekly retention typical."),
        Flashcard(front="What does <code>oc adm must-gather</code> do?", back="Collects diagnostic bundle (logs, configs, ClusterOperator status, events). Targeted variants per Operator. Tarball for Red Hat support cases or your own postmortem."),
        Flashcard(front="What is Insights and what does it do?", back="OCP phone-home telemetry (opt-out). Cluster sends anonymised health + version + Operator status to Red Hat. Insights Advisor surfaces known-issue alerts + recommendations in console.redhat.com."),
    ],
    quizzes=[
        Quiz(prompt="The cluster\'s upgrade is stuck at 75% for 3 hours. ClusterOperator monitoring degraded. Walk through diagnosis.",
            answer="(1) <code>oc get clusterversion -o yaml</code> — current state + conditions. (2) <code>oc get co</code> — which CO\'s are Degraded? (3) For monitoring CO: <code>oc describe co/monitoring</code>. (4) Check CVO logs: <code>oc logs -n openshift-cluster-version deployment/cluster-version-operator</code>. (5) If MCO involved: <code>oc get mcp</code> — pools Updating? Stuck? (6) For stuck MCP roll: <code>oc describe mcp/worker</code> — node-level status, often points to PDB blocking drain. (7) Run <code>oc adm must-gather</code>; open Red Hat support case with bundle. (8) For PDB deadlock: identify offending workload; either fix the PDB (give it 1 unavailable allowance) or temporarily scale up replicas to release the drain."),
        Quiz(prompt="A regulated bank wants to lock OCP to one minor for 2 years. Walk through the design.",
            answer="(1) Pick OCP Premium tier subscription (required for EUS access). (2) Install on a designated EUS minor (e.g., OCP 4.18 EUS). (3) Set channel to <code>eus-4.18</code> in ClusterVersion. (4) Cluster receives only patches within 4.18 for ~24 months. (5) Approaching EUS-EOS: plan + execute EUS-to-EUS upgrade (e.g., to <code>eus-4.20</code>) — CVO traverses skip-minor graph. (6) Scope: this works for 1 cluster or fleet via RHACM Cluster Lifecycle. <em>Trade-off: stability + low change-control burden vs missing latest features for 2 years.</em>"),
        Quiz(prompt="Saturday at the SCIF. The on-call needs to apply a CVE patch. Cluster is air-gapped. Walk through the disconnected upgrade.",
            answer="(1) On internet-connected staging: <code>oc-mirror --config imageset-config.yaml</code> pulls new patch release + relevant Operator updates. Validate the imageset includes the upgrade-graph data. (2) Sneakernet (or data diode) the tarball to the SCIF. (3) On the SCIF mirror registry: <code>oc-mirror --from tarball --to docker://mirror.scif.example.com</code>. (4) Disconnected OSUS Operator should automatically pick up the new graph data; otherwise force refresh. (5) Verify ClusterVersion sees the new patch: <code>oc adm upgrade</code>. (6) Schedule maintenance window. (7) Run <code>oc adm upgrade --to=4.18.X</code>. (8) Monitor: <code>oc get clusterversion + oc get co + oc get mcp</code>. (9) Verify post-upgrade: <code>oc adm must-gather</code> as a baseline; standard smoke tests.",
            cyoa=True, cyoa_tag="how the disconnected patch landed"),
    ],
    glossary=[
        GlossaryItem(name="ClusterVersion", definition="CR holding cluster\'s declared + observed OCP version. Edit spec.desiredUpdate or spec.channel to upgrade."),
        GlossaryItem(name="CVO (Cluster Version Operator)", definition="Orchestrates ~30 ClusterOperator upgrades to the declared version."),
        GlossaryItem(name="Update channels", definition="stable-X.Y (prod), fast-X.Y (earlier GA), candidate-X.Y (RC), eus-X.Y (Extended Update Support)."),
        GlossaryItem(name="EUS (Extended Update Support)", definition="Designated minors with ~24-month support window. EUS-to-EUS skip-minor upgrades."),
        GlossaryItem(name="MachineConfig", definition="Declarative RHCOS config (kernel args, systemd, files). Merged per-pool by MCO."),
        GlossaryItem(name="MachineConfigPool (MCP)", definition="Group of nodes sharing config roll. Default: master, worker. Custom pools by label."),
        GlossaryItem(name="MachineSet", definition="VM/instance scale set. Cluster Autoscaler scales MachineSets."),
        GlossaryItem(name="MachineHealthCheck (MHC)", definition="Auto-remediation: deletes + recreates unhealthy Machines via MachineSet."),
        GlossaryItem(name="Node Tuning Operator + PerformanceProfile", definition="CPU pinning + hugepages + RT kernel + NUMA-aware tuning. Telco / latency workloads."),
        GlossaryItem(name="etcd backup (cluster-backup.sh)", definition="Single source of cluster-state truth. Schedule + ship off-cluster. Mandatory."),
        GlossaryItem(name="oc adm must-gather", definition="Diagnostic bundle for cluster issues. Targeted variants per Operator. For support cases + postmortems."),
        GlossaryItem(name="Insights telemetry", definition="OCP opt-out phone-home. Anonymised health to Red Hat Insights; surfaces known-issue alerts in console.redhat.com."),
        GlossaryItem(name="Disconnected OSUS Operator", definition="Internal upgrade-graph service for air-gapped clusters. Fed by oc-mirror data."),
        GlossaryItem(name="Conditional upgrade", definition="Upgrade graph flags risky paths based on cluster characteristics. Surfaced in <code>oc adm upgrade</code>."),
    ],
    recap_lead='Three crews: Version (CVO + channels + EUS), Floor (MCO + MCPs + MachineSets + MHCs), Records (etcd + must-gather + Insights). Disconnected via oc-mirror + OSUS.',
    recap_next='<strong>Next — O9: OpenShift Virtualization, AI, and Edge.</strong> OpenShift Virtualization (KubeVirt) for VMs as first-class workloads; OpenShift AI (formerly RHODS) for notebooks + KServe + Kubeflow + RHEL AI; SNO + MicroShift + Local Zones for edge.',
)
