"""K-ADV-DR D2 — GitOps-driven recovery + cluster rebuild + application restore."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GitOps recovery."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Ship Rebuild Yard · K-Lifeboat — rebuild from Git + backups in &lt; 30 min</text><rect x="40" y="70" width="200" height="100" rx="10" fill="#A04832"/><text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">cluster destroyed</text><text x="140" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">total loss</text><rect x="260" y="70" width="200" height="100" rx="10" fill="#3F4A5E"/><text x="360" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">rebuild via IaC</text><text x="360" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Terraform / Crossplane</text><rect x="480" y="70" width="240" height="100" rx="10" fill="#5DCAA5"/><text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">GitOps + Velero restore</text><text x="600" y="108" text-anchor="middle" font-size="9" fill="#1F2433">Argo CD syncs + PVC restore</text></svg>"""


LESSON = LessonSpec(
    num="02", title_short="GitOps recovery", title_full="D2 · GitOps-Driven Recovery + Cluster Rebuild + Application Restore",
    title_html="K-ADV-DR D2 · GitOps Recovery", module_eyebrow="Module D2 · Ship Rebuild Yard — rebuild from Git + backups in &lt; 30 min",
    hero_sub_html='Total cluster loss → rebuild path. <strong>Cluster IaC</strong>: Terraform / Crossplane / Pulumi rebuilds the cluster (control plane + node pools + IAM + networking). <strong>GitOps</strong> (Argo CD / Flux): syncs all apps from Git as soon as cluster is up. <strong>Velero restore</strong>: PVC + Secret + ConfigMap data restored. <strong>Order matters</strong>: cluster → CRDs → operators → apps → restore data. End-to-end RTO &lt; 30 min for well-built systems.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Cluster is gone. Team has Terraform for the cluster + Velero backups for data + Argo CD for apps. <em>But: the order matters; without a tested runbook, the rebuild is chaos</em>. Today\'s lesson: the order + the runbook + the drill.",
    stamp_html="<strong>Recovery order: cluster IaC → CRDs → operators → apps (GitOps) → Velero restore. Tested via quarterly drill. RTO &lt; 30 min for well-built systems.</strong>",
    district_pin="kdr-cell02", district_label="Ship Rebuild Yard",
    sections=[
        Section(eyebrow="Section 1.1 · cluster IaC rebuild",
            h2="Terraform / Crossplane / Pulumi",
            body_html="""    <p>Cluster itself is rebuildable from IaC. Terraform / Crossplane / Pulumi declares: control plane (managed K8s service) + node pools + IAM + networking + DNS.</p>
    <p>Rebuild time: 5-15 min on managed K8s; 30-60 min on self-managed (etcd restore + control-plane bootstrap). Cluster name + cloud account + region preserved (or new region for disaster).</p>
    <p>Pre-prep: IaC tested + drill-rebuilt quarterly to non-prod; runbook updated."""),
        Section(eyebrow="Section 1.2 · GitOps sync",
            h2="Argo CD / Flux re-creates everything",
            body_html="""    <p>Once cluster is up: install <strong>Argo CD</strong> / <strong>Flux</strong> (one Helm chart). Argo CD reads Git; reconciles all Apps. Within 5-10 min, all workloads spawn.</p>
    <p><strong>Sync waves</strong> matter: CRDs first (sync wave -2), operators (sync wave -1), apps (sync wave 0+). Without ordering, apps fail because their CRDs don\'t exist yet.</p>
    <p>ApplicationSet generators replicate fleet-wide; new cluster picks up automatically."""),
        Section(eyebrow="Section 1.3 · Velero restore",
            h2="PVCs + Secrets + ConfigMaps",
            body_html="""    <p><strong>Velero restore</strong> per backup. Restore order: per-namespace; high-priority first (databases / auth services); low-priority later. <code>velero restore create --from-backup &lt;name&gt;</code>.</p>
    <p><strong>Mapping</strong>: <code>--namespace-mappings</code> if restoring to a different namespace; <code>--include-resources</code> to limit scope.</p>
    <p>External services (RDS / Vault) restore separately via their own DR procedures. Coordinate the timeline."""),
        Section(eyebrow="Section 1.4 · runbook + drill",
            h2="Tested quarterly; RTO measured",
            body_html="""    <p><strong>Runbook</strong>: numbered steps; per cluster shape; tested. Common skeleton:</p>
    <ol>
      <li>Provision cluster via Terraform / Crossplane (~5-15 min).</li>
      <li>Install Argo CD / Flux (~2 min).</li>
      <li>Argo CD syncs CRDs + operators (sync wave) (~5 min).</li>
      <li>Argo CD syncs apps (~5 min).</li>
      <li>Velero restore PVCs + Secrets + ConfigMaps (~5 min).</li>
      <li>Validate: SLO metrics return.</li>
      <li>DNS swap to new cluster (Route 53 / Azure DNS).</li>
      <li>Tenant communications.</li>
    </ol>
    <p><strong>Quarterly drill</strong>: full rebuild to non-prod; measure RTO; update runbook. Find issues before real loss."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why IaC for cluster rebuild?",
            options=[("Required by K8s.", False), ("Reproducible cluster shape; rebuild in minutes vs hours of manual work.", True), ("Faster than kubectl.", False)],
            feedback="IaC encodes cluster spec; new cluster matches old cluster\'s shape automatically. Manual rebuild = hours + drift."),
        3: PauseCheck(question="Why sync waves matter in restore?",
            options=[("Performance.", False), ("CRDs must exist before custom resources reference them; operators before apps.", True), ("Required by Argo CD.", False)],
            feedback="CRDs (sync wave -2) → operators (sync wave -1) → apps (sync wave 0+). Without order, apps fail because CRDs don\'t exist yet."),
    },
    before_after_before='<p>Pre-GitOps recovery: total cluster loss = days of manual rebuild from notes + memory + Slack scrollback. RTO measured in days.</p>',
    before_after_after='<p>GitOps + IaC + Velero: cluster IaC + GitOps sync + Velero restore. RTO &lt; 30 min for well-built systems. Runbook + drill mandatory.</p>',
    before_after_caption='<p class="ba-caption"><em>Cluster as cattle, not pet. Rebuildable in minutes from Git + backups.</em></p>',
    analogy_intro_html='''<p>Ship Rebuild Yard: when a ship is lost, the yard rebuilds from blueprints (IaC) + cargo manifests (Git) + cargo backups (Velero). The Drill Master practices quarterly so the rebuild flows in &lt; 30 min.</p>''',
    translation_rows=[
        ("Ship blueprints", "Terraform / Crossplane / Pulumi"),
        ("Cargo manifests", "Git source-of-truth (apps + config)"),
        ("Cargo backup vaults", "Velero backup of PVCs + Secrets"),
        ("Yard rebuild order", "cluster → CRDs → operators → apps → data restore"),
        ("Sync wave priority", "argocd.argoproj.io/sync-wave annotation"),
        ("Drill Master", "DR engineer / on-call"),
    ],
    analogy_stops="A real ship is physical; cluster is config + state. Backups + IaC = rebuildable; verify quarterly.",
    eli5="When a ship is lost, the yard rebuilds from blueprints + cargo lists + cargo backups. Practice every quarter so the rebuild is fast.",
    eli10="<strong>Cluster IaC</strong> (Terraform / Crossplane / Pulumi) → <strong>GitOps sync</strong> (Argo CD / Flux with sync waves: CRDs → operators → apps) → <strong>Velero restore</strong> (PVCs + Secrets + ConfigMaps). RTO &lt; 30 min. Quarterly drill mandatory.",
    scenarios=[
        Scenario(name="Quarterly drill — 22-min rebuild", body="Quarterly disaster drill: destroy non-prod cluster; rebuild from Terraform + Argo CD + Velero. Measured: 22 min from start to SLO-passing. Runbook validated."),
        Scenario(name="Real cluster loss — 28 min recovery", body="Bad upgrade corrupted prod cluster; rebuild via runbook in 28 min; tenants noticed brief degradation; full recovery within RTO."),
        Scenario(name="Sync wave caught CRD-first ordering", body="Initial recovery attempt failed; apps referenced CRDs not yet created. Postmortem: sync waves -2 / -1 / 0+ for CRDs / operators / apps. Subsequent drill clean."),
        Scenario(name="Outage — Velero backup not tested", body="Backup existed but restore failed (StorageClass mismatch new cluster vs old). 6-hour outage. Postmortem: quarterly restore drill to find these gaps."),
    ],
    misconceptions=[
        Misconception(myth="\"Velero alone is enough.\"", truth="Velero handles K8s objects + PVCs; cluster itself needs IaC; secrets often need separate ESO + Vault recovery; DNS + external services need own DR. Coordinate."),
        Misconception(myth="\"Argo CD will figure out the order.\"", truth="Without sync waves, Argo CD applies in graph order — apps before CRDs may fail. Annotate sync-wave for deterministic ordering."),
        Misconception(myth="\"GitOps recovery is too complex; just snapshot the cluster.\"", truth="Snapshot-based recovery has limits (state drift, can\'t cross-region, large size). GitOps + IaC + Velero is more flexible + recoverable to any cluster shape."),
    ],
    flashcards=[
        Flashcard(front="Recovery order from total cluster loss?", back="(1) Cluster IaC; (2) Argo CD / Flux; (3) CRDs (sync wave -2); (4) Operators (sync wave -1); (5) Apps; (6) Velero restore PVCs + Secrets; (7) Validate; (8) DNS swap."),
        Flashcard(front="Cluster IaC tools?", back="<strong>Terraform</strong>, <strong>Crossplane</strong>, <strong>Pulumi</strong>. Pick by team\'s ecosystem; same outcome (cluster rebuilt to spec)."),
        Flashcard(front="Sync wave annotation?", back="<code>argocd.argoproj.io/sync-wave: \"N\"</code>. Lower N = sooner. Use -2 for CRDs, -1 for operators, 0+ for apps."),
        Flashcard(front="Velero restore command?", back="<code>velero restore create --from-backup &lt;name&gt;</code> + optional flags: --namespace-mappings + --include-resources + --restore-volumes."),
        Flashcard(front="Why runbook?", back="Numbered steps; per cluster shape; tested. Eliminates panic-driven misordering during real incidents."),
        Flashcard(front="RTO target for well-built K8s recovery?", back="P95 &lt; 30 min for managed K8s + GitOps + Velero. Slower (60-120 min) for self-managed with etcd restore."),
        Flashcard(front="DNS swap during recovery?", back="Route 53 / Azure DNS / Cloud DNS health-check + manual or automated swap to new cluster\'s LB."),
        Flashcard(front="What\'s NOT covered by GitOps + Velero?", back="External managed services (RDS / Vault / S3 / SaaS). Each has own DR; coordinate timelines."),
    ],
    quizzes=[
        Quiz(prompt="Walk total-cluster-loss recovery for an EKS cluster.",
            answer="(1) <strong>Trigger runbook</strong>: cluster destroyed (real or drill). (2) <strong>Provision new EKS cluster</strong> via Terraform (~10 min). (3) <strong>Install Argo CD</strong> via Helm (~2 min). (4) <strong>Argo CD ApplicationSet</strong> auto-discovers new cluster + syncs Apps. (5) <strong>Sync wave order</strong>: CRDs (-2) → operators like cert-manager / ESO (-1) → apps (0+) → ~10 min. (6) <strong>Velero restore</strong>: per-namespace; high-priority first. (7) <strong>External Secrets</strong>: ESO re-syncs from Vault (kept external). (8) <strong>DNS swap</strong>: Route 53 record points at new ALB. (9) <strong>Validate</strong>: SLO metrics return; tenant tests pass. (10) <strong>Postmortem</strong>: timeline + RTO measured + runbook updates."),
        Quiz(prompt="A team\'s drill reveals 90-min rebuild (target 30 min). Walk improvement.",
            answer="(1) <strong>Profile each phase</strong>: cluster IaC (15 min), CRDs (5 min), operators (15 min), apps (10 min), Velero (40 min — bottleneck), DNS swap (5 min). (2) <strong>Optimise Velero</strong>: parallel restore; CSI snapshots faster than Restic / Kopia for large volumes; smaller backup units (per-namespace). (3) <strong>Pre-warm cluster</strong>: keep DR cluster warm with same cluster shape; on disaster, just sync apps + restore data — skip cluster IaC. (4) <strong>Iterate</strong>: drill again next quarter; measure improvement."),
        Quiz(prompt="The CFO asks: \"why pay for DR engineering + drills?\" Defend.",
            answer="\"<strong>Without tested DR, an outage is open-ended; with tested DR, RTO is bounded.</strong> Three reasons: (1) <strong>Customer expectations</strong>: enterprise customers want 99.9-99.99% SLA; without DR, single failure breaks SLA. (2) <strong>Compliance</strong>: SOC2 / HIPAA / PCI all require tested DR. (3) <strong>Cost of bad outage</strong>: customer churn + lawsuits + reputation. <strong>DR engineering cost</strong>: ~1-2 engineers + Velero / K10 + drill time. <strong>Cost of one severe outage</strong>: orders of magnitude more.\"", cyoa=True, cyoa_tag="how the DR architect defended drills"),
    ],
    glossary=[
        GlossaryItem(name="GitOps recovery", definition="Cluster rebuild from Git source-of-truth + IaC + backups."),
        GlossaryItem(name="Cluster IaC", definition="Terraform / Crossplane / Pulumi declaring cluster control-plane + node pools + IAM + networking."),
        GlossaryItem(name="Sync wave", definition="argocd.argoproj.io/sync-wave; orders Argo CD resource sync; CRDs first, apps last."),
        GlossaryItem(name="ApplicationSet (DR)", definition="Argo CD ApplicationSet auto-discovers new cluster + syncs Apps; foundation of fleet GitOps."),
        GlossaryItem(name="Velero restore", definition="<code>velero restore create --from-backup</code> with mapping options."),
        GlossaryItem(name="Pre-warmed DR cluster", definition="DR cluster maintained at standby; apps sync on disaster; faster than cluster-IaC-from-zero."),
        GlossaryItem(name="DNS swap", definition="Route 53 / Azure DNS / Cloud DNS update pointing at new cluster\'s LB."),
        GlossaryItem(name="Runbook", definition="Numbered DR steps; per-cluster-shape; tested quarterly."),
        GlossaryItem(name="RTO", definition="Recovery Time Objective; max acceptable time to recover."),
        GlossaryItem(name="RPO", definition="Recovery Point Objective; max acceptable data loss window."),
    ],
    recap_lead="GitOps recovery: cluster IaC → CRDs (sync wave) → operators → apps → Velero restore PVCs / Secrets → DNS swap → validate. Quarterly drill measures + improves RTO.",
    recap_next='<strong>Next — D3: Cross-region DR + RPO/RTO + restore testing.</strong>',
)
