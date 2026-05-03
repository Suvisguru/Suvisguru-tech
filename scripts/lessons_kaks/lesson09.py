"""K-AKS A9 — AKS Upgrades and Operations (version policy, LTS, channels, surge, blue-green, cert rotation)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AKS upgrade ladder — control plane, node image, node pool, blue-green; LTS support tier.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Maintenance Yard — versions, channels, waves</text>
  <rect x="50" y="60" width="180" height="130" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="140" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">version policy</text>
  <text x="140" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">N · N-1 · N-2 (community)</text>
  <text x="140" y="113" text-anchor="middle" font-size="9" fill="#FFFFFF">+ N-3 (platform)</text>
  <text x="140" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">+ LTS (designated)</text>
  <text x="140" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">AKS Release Tracker</text>
  <text x="140" y="161" text-anchor="middle" font-size="9" fill="#FFFFFF">(per-region)</text>
  <rect x="245" y="60" width="180" height="130" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="335" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">channels &amp; windows</text>
  <text x="335" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6">auto-upgrade channels</text>
  <text x="335" y="115" text-anchor="middle" font-size="9" fill="#FBF1D6">node-image-upgrade</text>
  <text x="335" y="130" text-anchor="middle" font-size="9" fill="#FBF1D6">planned maintenance</text>
  <text x="335" y="145" text-anchor="middle" font-size="9" fill="#FBF1D6">surge upgrade %</text>
  <rect x="440" y="60" width="180" height="130" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="530" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">upgrade techniques</text>
  <text x="530" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">control plane (in place)</text>
  <text x="530" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">add-ons</text>
  <text x="530" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">node pool surge</text>
  <text x="530" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">blue-green node pool</text>
  <text x="530" y="160" text-anchor="middle" font-size="9" fill="#FFFFFF">cluster blue-green (rare)</text>
  <rect x="635" y="60" width="75" height="130" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="673" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">tail</text>
  <text x="673" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6">API</text>
  <text x="673" y="113" text-anchor="middle" font-size="9" fill="#FBF1D6">deprecations</text>
  <text x="673" y="130" text-anchor="middle" font-size="9" fill="#FBF1D6">cert</text>
  <text x="673" y="143" text-anchor="middle" font-size="9" fill="#FBF1D6">rotation</text>
</svg>"""


LESSON = LessonSpec(
    num="09",
    title_short="AKS upgrades &amp; ops",
    title_full="A9 · AKS Upgrades and Operations",
    title_html="K-AKS A9 · Upgrades and Operations",
    module_eyebrow="Module A9 · the Maintenance Yard",
    hero_sub_html='<strong>Version policy</strong>: AKS supports N (latest), N-1, N-2 community; N-3 platform support; <strong>LTS (Long-Term Support)</strong> for designated versions on Premium tier. <strong>AKS Release Tracker</strong> for regional rollout. <strong>Auto-upgrade channels</strong> (none / patch / stable / rapid / node-image). <strong>Node-image upgrades</strong> separate from K8s upgrades. <strong>Planned maintenance windows</strong>. <strong>Surge upgrades</strong> (%) limit Pod disruption. <strong>Blue-green node pool migration</strong> for high-stakes upgrades. Plus API deprecations, add-on upgrades, certificate rotation.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"Cluster upgrade failed; nodes stuck in NodeUpgradeInProgress; deployments throwing PodDisruptionBudget violations.\"</em> The auto-upgrade fired in the maintenance window the team configured 6 months ago when nobody was paged. Surge upgrade % is at default (10%); a critical service has PDB <code>maxUnavailable: 0</code> + 3 replicas — drain blocks. Cluster is in a halfway state. <em>You don\'t know if rolling back is possible.</em> Today\'s lesson: the ladder of AKS upgrades and the safety net (surge, PDB, blue-green).",
    stamp_html="<strong>Five upgrade things: K8s minor (in place, blue-green for high stakes), node image (separate cycle), add-ons (mostly automatic), surge % to limit blast, PDBs to prevent deadlock. LTS gives you 2-year stability for designated versions. Use the Release Tracker; pre-flight with kube-no-trouble.</strong>",
    district_pin="kc-wing09",
    district_label="Maintenance Yard",
    sections=[
        Section(
            eyebrow="Section 1.1 · version policy + LTS",
            h2="Version policy + LTS — what AKS supports when",
            body_html="""    <p>AKS supports <strong>N (latest minor) + N-1 + N-2</strong> as community-supported versions. Once a version drops below N-2, it enters <strong>platform support</strong> for one more minor (N-3) — security patches only, no feature support, time-limited. After N-3, the cluster cannot be upgraded directly to a supported version; it must be force-upgraded across multiple minors or rebuilt blue-green.</p>
    <p><strong>AKS Long-Term Support (LTS)</strong> = designated minor versions get <strong>2-year support</strong> on the <strong>Premium tier</strong>. Available for select versions (e.g. v1.27 LTS). Use LTS when you cannot upgrade quarterly — regulated industries, ISV-bundled workloads, infrastructure with long change-control cycles. <em>LTS is a Premium-tier feature; budget for it.</em></p>
    <p><strong>The AKS Release Tracker</strong> (releases.aks.azure.com) shows which AKS minor versions are rolled out to which Azure regions. Plan upgrades around regional availability — your East US cluster might have v1.34 ready while West Europe is still on v1.33. Check before scheduling cross-region upgrade waves.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · auto-upgrade channels + maintenance windows",
            h2="Auto-upgrade channels + planned maintenance windows",
            body_html="""    <p><strong>Auto-upgrade channels</strong> let AKS upgrade the cluster automatically:</p>
    <ul>
      <li><code>none</code> — manual upgrades only.</li>
      <li><code>patch</code> — auto-apply patch versions within the current minor (e.g. 1.34.5 → 1.34.7).</li>
      <li><code>stable</code> — auto-apply minor upgrades, lagging the bleeding edge by one (recommended for prod).</li>
      <li><code>rapid</code> — auto-apply the latest minor as soon as it\'s GA (for non-prod / canary).</li>
      <li><code>node-image</code> — separate channel for node OS image upgrades (independent of K8s minor).</li>
    </ul>
    <p><strong>Planned maintenance windows</strong> — schedule the auto-upgrade and maintenance work to specific UTC time slots, e.g. \"Sunday 02:00-06:00 UTC.\" Three sub-types: <code>aksManagedAutoUpgradeSchedule</code> (cluster K8s upgrades), <code>aksManagedNodeOSUpgradeSchedule</code> (node OS upgrades), <code>default</code> (legacy combined window). <em>Always set planned maintenance for prod</em>; otherwise upgrades fire at random.</p>
    <p><strong>Pre-flight:</strong> before any upgrade, run <strong>kube-no-trouble (kubent)</strong> against the cluster to detect deprecated API usage in YAML / Helm charts. Surfaces issues that\'ll bite during the upgrade.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · upgrade techniques",
            h2="Upgrade techniques — surge, blue-green, in place",
            body_html="""    <p><strong>Control-plane upgrade</strong> = AKS-driven, in place, ~30 minutes, no downtime. Apiserver, etcd, scheduler, controller-manager all roll. Use <code>az aks upgrade --control-plane-only</code> first; nodes follow.</p>
    <p><strong>Node pool upgrade with surge</strong> — surge % controls how many extra nodes are added during the rolling upgrade so Pods can drain to fresh nodes before old ones cordon. Defaults to 10% per pool. <em>For low-PDB-tolerance workloads, increase to 33% or 50%</em> — more parallelism, faster upgrade, more capacity needed during the window. <code>az aks nodepool update --max-surge 50%</code>.</p>
    <p><strong>PDB-aware drains:</strong> the upgrade respects PodDisruptionBudgets. A workload with <code>maxUnavailable: 0</code> + min replicas + no surge headroom = <em>upgrade deadlock</em> (drain can\'t evict any Pod). The fix is realistic PDBs that allow at least 1 disruption when you have multiple replicas.</p>
    <p><strong>Blue-green node pool migration</strong> — high-stakes upgrade pattern. Create a new node pool on the target version next to the old; cordon the old, drain workloads (PDB-aware) onto the new, delete the old. <em>Atomic rollback: if the new pool misbehaves, drain back to the old and delete the new.</em> Use this when you can\'t take any drain risk during in-place upgrade.</p>
    <p><strong>Cluster blue-green</strong> = build a whole new cluster on the target version, route traffic via DNS or front-door, decommission the old. <em>Last-resort pattern</em> for major version jumps (cross-LTS), workloads that can\'t survive any in-place change, or when N-3 force-upgrade isn\'t safe.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · API deprecations, add-ons, certificate rotation",
            h2="API deprecations, add-on upgrades, certificate rotation",
            body_html="""    <p><strong>API deprecations</strong> are the silent killer. K8s removes APIs each minor (e.g. <code>networking.k8s.io/v1beta1 Ingress</code> removed in 1.22). Workloads that still reference deprecated APIs fail post-upgrade. Tools: <strong>kube-no-trouble (kubent)</strong> scans live cluster + git for deprecated API usage; <strong>Pluto</strong> scans Helm charts. Run before every minor upgrade.</p>
    <p><strong>Add-on upgrades</strong> — managed add-ons (Defender, Container Insights, KEDA, Flux, etc.) are upgraded by Microsoft as part of the cluster upgrade or independently. Self-installed Helm-chart add-ons are <em>your responsibility</em> — easy to forget, and an old chart can break on the new K8s minor.</p>
    <p><strong>Certificate rotation:</strong>
    <ul>
      <li><strong>Cluster certificates</strong> (apiserver, etcd, kubelet) — rotated automatically by AKS. <code>az aks rotate-certs</code> can force a rotation if needed (e.g. compromise).</li>
      <li><strong>Service Account tokens</strong> — bound (BoundServiceAccountTokens) and short-lived in modern K8s; auto-rotated.</li>
      <li><strong>Add-on certs</strong> (cert-manager-issued, App Routing, etc.) — automatic via the cert-manager controller; verify rotation logs after major upgrades.</li>
    </ul>
    <p><strong>Upgrade order:</strong> (1) pre-flight (kubent), (2) backup (Velero / etcd snapshot via AKS\'s managed backup if available), (3) upgrade non-prod, (4) bake non-prod a week, (5) upgrade prod control plane, (6) upgrade node pools with appropriate surge, (7) verify, (8) repeat for next minor (don\'t skip versions in one go).</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team\'s critical workload has PDB <code>maxUnavailable: 0</code> + 3 replicas. The upgrade is stuck. What\'s the safest fix?",
            options=[
                ("Force-delete the PDB.", False),
                ("Increase max-surge on the node pool to 50% so a fresh node is ready before any old one cordons; the workload\'s replica count + PDB allows drain.", True),
                ("Skip the upgrade.", False),
            ],
            feedback="More surge headroom (or a saner PDB like maxUnavailable: 1) lets drains succeed without violating availability. Force-deleting the PDB defeats the safety it was meant to provide.",
        ),
    },
    before_after_before='<p>Pre-managed AKS upgrades = manual, scary. Operators ran <code>az aks upgrade</code> and watched logs in fear; rollback wasn\'t a single command. Node pools dragged because surge default was 1; PDBs deadlocked drains; LTS didn\'t exist; auto-upgrade channels were minimal. API deprecations bit teams who hadn\'t pre-flighted. Add-ons installed by Helm broke after every minor.</p>',
    before_after_after='<p>Modern AKS gives you <strong>auto-upgrade channels</strong> (patch / stable / rapid / node-image) + <strong>planned maintenance windows</strong> + <strong>tunable surge %</strong> + <strong>LTS</strong> (2 years on Premium tier) + <strong>blue-green node pool</strong> + <strong>kubent / Pluto</strong> for pre-flight. Managed add-ons upgrade with the cluster. Cert rotation is automatic. <em>Upgrades become routine; quarterly minor cycle without a war room.</em></p>',
    before_after_caption='<p class="ba-caption"><em>The era of \"upgrade Saturday\" with the entire team on a bridge call is over for AKS — if you wire up channels, surge, PDBs, and pre-flight correctly.</em></p>',
    analogy_intro_html='''<p>The <strong>Maintenance Yard</strong> is the back-of-campus depot where rolling repairs happen. Three crews work different upgrade jobs.</p>
    <p>The <strong>Roof Crew</strong> (control plane) replaces the campus roof every quarter — no class disruption, residents don\'t see anything change. AKS does this in 30 minutes.</p>
    <p>The <strong>Wing Renovation Crew</strong> (node pool surge upgrade) renovates one wing at a time. They build a temporary annexe (surge nodes), move residents from the old wing to the annexe (drain), demolish + rebuild the old wing, move residents back. <em>Surge %</em> is how many extra annexe rooms they can build at once — bigger annexe = faster renovation but more parking strain. <em>PodDisruptionBudgets</em> are residents\' safety contracts: \"never have fewer than 2 of us in this wing at once.\"</p>
    <p>The <strong>Build-New-Wing Crew</strong> (blue-green node pool) doesn\'t renovate — they build a brand-new wing next to the old one. Residents migrate; old wing gets demolished. <em>Atomic rollback</em>: if the new wing leaks, residents move back to the old.</p>
    <p>The <strong>Long-Term Lease Office</strong> (LTS) runs a separate 2-year-stable wing for residents who absolutely cannot move every quarter. Costs more (Premium tier), guarantees no forced moves for 24 months.</p>
    <p>And there\'s a <strong>Pre-Flight Inspector</strong> (kube-no-trouble + Pluto) who walks every wing before any renovation and flags rooms with outdated wiring (deprecated API usage) — <em>fix before renovation, not during</em>.</p>''',
    translation_rows=[
        ("Roof crew", "Control-plane upgrade (in place, no downtime)"),
        ("Wing renovation", "Node pool upgrade with surge"),
        ("Temporary annexe", "Surge nodes (max-surge %)"),
        ("Resident safety contract", "PodDisruptionBudget (PDB)"),
        ("Build-new-wing crew", "Blue-green node pool migration"),
        ("Atomic rollback", "Drain back to old pool, delete new"),
        ("Build-new-campus crew", "Cluster blue-green (whole new AKS cluster)"),
        ("Long-Term Lease Office", "AKS LTS (2-year support, Premium tier)"),
        ("Pre-Flight Inspector", "kube-no-trouble + Pluto"),
        ("Outdated wiring", "Deprecated API usage"),
        ("Daily auto-fix-it day", "Auto-upgrade channels (patch / stable / rapid)"),
        ("Approved work hours", "Planned maintenance windows"),
        ("Annual lockset rekey", "Certificate rotation"),
    ],
    analogy_stops="A real renovation can pause; a K8s upgrade in flight can\'t easily pause mid-pool. The metaphor underplays the irreversibility of some upgrade steps (e.g., once etcd schema migrates).",
    eli5="The maintenance crew has different jobs. One fixes the roof while everyone keeps working. Another renovates one wing at a time, putting up a temporary tent so people don\'t crowd. Sometimes they build a whole new wing instead. There\'s an inspector who walks the building first to find old wiring before they break the wall open.",
    eli10="AKS upgrades = control plane (in place, ~30 min, no downtime) + node pool (surge % to control parallel, PDB-aware drain) + add-ons (managed = automatic; self-installed = your job). For high-stakes: blue-green node pool (atomic rollback). LTS gives 2-year stability on Premium tier for designated versions. Pre-flight with kube-no-trouble. Schedule with planned maintenance windows + auto-upgrade channels. API deprecations bite if you skip pre-flight; certificate rotation is automatic.",
    scenarios=[
        Scenario(
            name="SaaS — quarterly minor cadence with stable channel + 33% surge",
            body="A SaaS runs 30 AKS clusters on the <code>stable</code> auto-upgrade channel; planned maintenance Sundays 02:00-06:00 UTC; node-pool max-surge = 33%. Upgrades fire automatically; on-call gets a notification but doesn\'t need to be at keyboard. PDBs across all services tested for 33% surge tolerance. <em>Quarterly minor jumps without a war room.</em>",
        ),
        Scenario(
            name="Bank — LTS on Premium tier for the regulated cluster",
            body="A bank\'s payments cluster has 9-month change-control cycles. They cannot upgrade quarterly. Solution: AKS Premium tier + LTS on v1.27. Two years of supported updates without minor jumps. <em>$0.60/cluster-hour Premium tier vs $0.10 Standard — math works out for the regulated workload.</em>",
        ),
        Scenario(
            name="Health-care — blue-green node pool for the SAP HANA workload",
            body="A SAP HANA workload has zero PDB tolerance for unplanned drain. Upgrade strategy: build a new node pool on the target K8s + node OS version next to the existing pool; verify hardware (Ultra Disk attachment, ANF mounts); fence DB application traffic; drain with 60-min grace; delete old pool. <em>Atomic rollback ready until cutover commit.</em>",
        ),
        Scenario(
            name="Pre-flight saved an outage — kubent caught Ingress v1beta1",
            body="A team ran kubent before a 1.21 → 1.22 upgrade. Result: 14 Ingress objects still on <code>networking.k8s.io/v1beta1</code> (removed in 1.22). All in legacy Helm charts. Team migrated charts to <code>networking.k8s.io/v1</code> first; upgrade then went clean. <em>Without kubent, those 14 ingresses would have orphaned post-upgrade — silent partial outage.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"AKS upgrades are zero-downtime by default.\"",
            truth="<strong>Control-plane</strong> upgrades are zero-downtime. <strong>Node pool</strong> upgrades cause Pod restarts during drain. With sane PDBs + surge + multiple replicas, the workload remains available — but individual Pods restart. Single-replica workloads with no PDB are exposed.",
        ),
        Misconception(
            myth="\"I can skip multiple minor versions in one upgrade.\"",
            truth="AKS supports <strong>one minor at a time</strong>. Going from 1.30 to 1.34 = four upgrades, not one. Each has its own pre-flight + window + add-on compatibility check. Trying to leap = AKS will refuse or, if you forced it, you\'re running an unsupported configuration.",
        ),
        Misconception(
            myth="\"LTS means I never have to upgrade.\"",
            truth="LTS = 2-year support for a designated version. After 2 years, the LTS version exits support and you must move to the next LTS or current N-2. <em>You\'re still upgrading; you\'re just doing it every 2 years instead of every quarter.</em> The trade-off is fewer upgrades, more change to absorb at each one.",
        ),
    ],
    flashcards=[
        Flashcard(front="AKS version support window?", back="<strong>N (current) + N-1 + N-2</strong> = community support. <strong>N-3</strong> = platform support (security patches only, time-limited). Below N-3 = unsupported; force-upgrade or rebuild."),
        Flashcard(front="What is AKS LTS?", back="<strong>Long-Term Support</strong> — 2-year support for designated K8s minor versions on Premium tier. For workloads that cannot upgrade quarterly (regulated, long change-control, ISV-bundled)."),
        Flashcard(front="Five auto-upgrade channels?", back="<code>none</code> (manual), <code>patch</code> (within current minor), <code>stable</code> (one minor behind latest — recommended prod), <code>rapid</code> (latest GA), <code>node-image</code> (node OS only, separate channel)."),
        Flashcard(front="Three planned-maintenance window types?", back="<code>aksManagedAutoUpgradeSchedule</code> (K8s upgrades), <code>aksManagedNodeOSUpgradeSchedule</code> (node OS upgrades), <code>default</code> (legacy combined). Always set for prod."),
        Flashcard(front="What does max-surge % do?", back="During a node pool upgrade, surge % adds extra nodes so Pods can drain to fresh nodes before old ones cordon. Default 10%; for low-PDB-tolerance workloads bump to 33-50% for faster + safer drains."),
        Flashcard(front="When use blue-green node pool migration?", back="High-stakes upgrades where in-place drain risk is unacceptable. Build new node pool on target version next to old; drain workloads to new; delete old. Atomic rollback (drain back to old) is available until you delete the old pool."),
        Flashcard(front="What is kube-no-trouble (kubent)?", back="Pre-flight tool that scans the live cluster (and Helm releases) for deprecated K8s API usage. Run before every minor upgrade to catch <code>networking.k8s.io/v1beta1 Ingress</code>-style breakers."),
        Flashcard(front="Where is the AKS Release Tracker?", back="<code>releases.aks.azure.com</code> — public Microsoft tool showing which AKS minor versions are rolled out in which Azure regions. Plan cross-region upgrades using this."),
    ],
    quizzes=[
        Quiz(
            prompt="The team\'s upgrade is stuck — node draining for 90 minutes. <code>kubectl describe</code> on the affected node shows: <em>Cannot evict Pod \'critical-svc-0\' as it would violate the Pod\'s disruption budget.</em> What\'s the immediate remediation and what\'s the structural fix?",
            answer="<strong>Immediate</strong>: temporarily increase replicas of <code>critical-svc</code> from 3 to 4 (so PDB <code>maxUnavailable: 0</code> still allows 1 to drain when there are 4); drain proceeds; restore to 3 after upgrade. <strong>Structural</strong>: rewrite the PDB to <code>maxUnavailable: 1</code> (or <code>minAvailable: 2</code> with 3 replicas). PDB <code>maxUnavailable: 0</code> + zero surge slack = always-deadlock during upgrade. Coordinate with the service owner to make this their default.",
        ),
        Quiz(
            prompt="A regulated cluster is on AKS v1.27 LTS. Two years pass. Now what?",
            answer="LTS support for v1.27 ends. Three options: (1) Move to the next LTS version (e.g. v1.30 LTS) via in-place stepwise upgrades — multiple minor jumps each with pre-flight + maintenance window. (2) Move to current N-2 (community support) and resume quarterly cadence. (3) Rebuild the cluster blue-green on the target version (clean slate). The decision is policy-driven; the LTS-to-LTS jump is the typical path for regulated workloads.",
        ),
        Quiz(
            prompt="It\'s upgrade Saturday. The team set <code>stable</code> auto-upgrade + planned maintenance window. At 02:14 the upgrade starts; at 02:23 it pauses with <em>\"add-on compatibility check failed: cert-manager v1.10 incompatible with target K8s minor.\"</em> The team self-installed cert-manager via Helm a year ago. What now?",
            answer="<strong>The upgrade auto-pauses</strong> rather than breaking — the add-on compatibility check is part of the cluster upgrade preflight. The team has two paths: (1) Upgrade cert-manager Helm chart to a version compatible with the target K8s minor; rerun upgrade. (2) Migrate to the <strong>App Routing add-on</strong> which bundles a managed cert-manager — no more chart-rot. The longer-term lesson: every self-installed add-on is a future upgrade hazard. Move to managed add-ons where they exist (App Routing, KEDA, Flux v2, Workload Identity, Key Vault provider, Istio mesh).",
            cyoa=True,
            cyoa_tag="why managed add-ons matter at upgrade time",
        ),
    ],
    glossary=[
        GlossaryItem(name="AKS version policy", definition="N (current) + N-1 + N-2 community-supported; N-3 platform support; LTS for designated versions on Premium tier."),
        GlossaryItem(name="AKS LTS (Long-Term Support)", definition="2-year support window for designated K8s minor versions. Premium tier."),
        GlossaryItem(name="AKS Release Tracker", definition="releases.aks.azure.com — regional rollout status for AKS minor versions."),
        GlossaryItem(name="Auto-upgrade channels", definition="none / patch / stable / rapid / node-image. Determine when AKS upgrades the cluster automatically."),
        GlossaryItem(name="Planned maintenance window", definition="UTC schedule for upgrades. Three types: aksManagedAutoUpgradeSchedule, aksManagedNodeOSUpgradeSchedule, default."),
        GlossaryItem(name="Node-image upgrade", definition="Separate from K8s upgrade — refreshes the node OS image (kernel, runtime, drivers, security patches)."),
        GlossaryItem(name="max-surge %", definition="Per node pool — % extra nodes added during upgrade so drains have headroom. Default 10%; tune higher for tight PDBs."),
        GlossaryItem(name="PodDisruptionBudget (PDB)", definition="Caps how many Pods of a workload can be unavailable during voluntary disruption (drain, scale-in, upgrade). Wrong PDB = upgrade deadlock."),
        GlossaryItem(name="Blue-green node pool migration", definition="Build new pool on target version; drain workloads from old to new; delete old. Atomic rollback until old pool deletion."),
        GlossaryItem(name="kube-no-trouble (kubent)", definition="Pre-flight tool scanning cluster + Helm for deprecated API usage. Run before every minor upgrade."),
        GlossaryItem(name="Pluto", definition="Companion tool that scans Helm chart manifests for deprecated APIs."),
        GlossaryItem(name="Certificate rotation", definition="AKS auto-rotates cluster certs. <code>az aks rotate-certs</code> can force a rotation. Add-on certs rotated by their controllers."),
    ],
    recap_lead='Five upgrade things mapped: K8s minor + node image + add-ons + surge + PDBs. LTS for stability; pre-flight with kubent; channels + windows for routine; blue-green for high-stakes.',
    recap_next='<strong>Next — A10: AKS Troubleshooting (Azure-specific).</strong> Entra/kubelogin failures, Azure RBAC mismatch, VMSS quota issues, Azure CNI IP exhaustion, CoreDNS, SNAT, LB pending, private DNS, disk attach failures, Key Vault CSI failures, ACR pull failures, MI failures, upgrade blocked, kubectl-aks, AKS Diagnostic Settings, Resource Health.',
)
