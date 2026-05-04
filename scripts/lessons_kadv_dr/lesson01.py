"""K-ADV-DR D1 — etcd backup + Velero + Kasten K10 + CloudCasa."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Backup tools — etcd / Velero / K10 / CloudCasa."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Drill Square · K-Lifeboat — four backup paths</text><rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E"/><text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">etcd snapshot</text><text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">control-plane state</text><rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5"/><text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Velero</text><text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">+ CSI snapshots / Kopia / Restic</text><rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900"/><text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Kasten K10</text><text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">app-aware backup</text><rect x="595" y="70" width="125" height="100" rx="10" fill="#5A6B81"/><text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">CloudCasa</text><text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">SaaS DR</text></svg>"""


LESSON = LessonSpec(
    num="01", title_short="etcd + Velero + K10 + CloudCasa", title_full="D1 · etcd Backup + Velero (CSI / Kopia / Restic) + Kasten K10 + CloudCasa",
    title_html="K-ADV-DR D1 · Backup Tools", module_eyebrow="Module D1 · Drill Square — four backup paths",
    hero_sub_html='<strong>etcd snapshot</strong>: <code>etcdctl snapshot save</code> for control-plane state; foundation for cluster rebuild. <strong>Velero</strong>: K8s-native backup; CSI snapshots for storage; Kopia / Restic for any PVC. <strong>Kasten K10</strong>: commercial app-aware backup; richer policies; mature integrations. <strong>CloudCasa</strong>: SaaS DR-as-a-service; managed.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A bad migration deleted half the production namespaces. <em>The team has Velero installed but never tested restore</em>. The first restore attempt fails because the StorageClass doesn\'t exist on the new cluster. Today\'s lesson: backup tools + tested restores; backup that\'s never restored is a hope, not a plan.",
    stamp_html="<strong>etcd = control-plane state. Velero = workload + PVC backup. K10 = commercial app-aware. CloudCasa = SaaS DR. Always test restore quarterly.</strong>",
    district_pin="kdr-cell01", district_label="Drill Square",
    sections=[
        Section(eyebrow="Section 1.1 · etcd backup",
            h2="Foundation of cluster rebuild",
            body_html="""    <p><strong>etcd</strong> holds all K8s API state. <code>etcdctl snapshot save</code> creates a point-in-time snapshot. Per-cluster backup pattern: cron-job snapshot every 6h to S3 (encrypted) + retention policy.</p>
    <p>Restore: provision fresh cluster; <code>etcdctl snapshot restore</code> the snapshot; control plane reconstructs from etcd. Use case: total cluster loss, control-plane corruption.</p>
    <p>Managed K8s (EKS / GKE / AKS): cloud handles etcd backup; you can\'t directly snapshot. Backup workloads via Velero instead."""),
        Section(eyebrow="Section 1.2 · Velero",
            h2="K8s-native backup; CSI / Kopia / Restic",
            body_html="""    <p><strong>Velero</strong>: K8s-native backup framework. Backs up: K8s objects (Deployment / Service / etc.) + PVCs (via CSI snapshot or filesystem-backup with Restic / Kopia).</p>
    <p>Per-cluster: <code>Backup</code> CR with namespace selector + schedule; <code>Restore</code> CR with mapping. <strong>BackupStorageLocation</strong> = S3 / Azure Blob / GCS. <strong>VolumeSnapshotLocation</strong> per CSI driver.</p>
    <p>Patterns: full-cluster nightly + per-namespace hourly + per-tenant on-demand. Restore: namespace-by-namespace; selective resource restore."""),
        Section(eyebrow="Section 1.3 · Kasten K10",
            h2="Commercial app-aware backup",
            body_html="""    <p><strong>Kasten K10</strong> (Veeam): commercial K8s backup. Application-aware (knows database state needs quiescing); rich policies (RBAC + RPO + RTO + compliance reports).</p>
    <p>Trade self-host for richer dashboards + commercial support + multi-cluster aggregation."""),
        Section(eyebrow="Section 1.4 · CloudCasa + selection",
            h2="SaaS DR-as-a-service + how to choose",
            body_html="""    <p><strong>CloudCasa</strong>: SaaS DR — install agent in cluster; backups + restores managed by CloudCasa platform. Trade engineering time for hosted simplicity.</p>
    <p><strong>Selection</strong>: Velero for K8s-shop self-host; K10 for commercial-support + richer features; CloudCasa for managed-DR-as-a-service. etcd snapshot always required for self-managed clusters.</p>"""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why etcd snapshot necessary?",
            options=[("Required by K8s.", False), ("Foundation for total-cluster-loss rebuild; Velero alone doesn\'t restore the control plane.", True), ("Performance.", False)],
            feedback="etcd snapshot = control-plane state. Velero = workloads. Both required for self-managed clusters."),
        3: PauseCheck(question="When pick CloudCasa?",
            options=[("Always.", False), ("When DR engineering time is constrained + hosted SaaS simplicity preferred.", True), ("Required by HIPAA.", False)],
            feedback="CloudCasa is hosted DR-as-a-service; trade engineering time for hosted ease. Velero / K10 if you self-host."),
    },
    before_after_before='<p>Pre-tested-DR: backups configured but never restored; restore failures discovered during real outage; RTO blown.</p>',
    before_after_after='<p>Modern: etcd snapshot + Velero / K10 / CloudCasa with quarterly restore drills; RPO + RTO measured + improved.</p>',
    before_after_caption='<p class="ba-caption"><em>Backup that\'s never restored is a hope. Quarterly drills convert hope to plan.</em></p>',
    analogy_intro_html='''<p>Drill Square is where the lifeboat crew practices. Four kit options: <strong>etcd snapshot</strong> = ship\'s logbook backup; <strong>Velero</strong> = standard lifeboat kit (CSI snapshots / Kopia / Restic); <strong>Kasten K10</strong> = commercial-grade kit; <strong>CloudCasa</strong> = rented lifeboats with hired crew.</p>''',
    translation_rows=[
        ("Ship\'s logbook", "etcd snapshot"),
        ("Standard lifeboat kit", "Velero + CSI / Kopia / Restic"),
        ("Commercial-grade kit", "Kasten K10 (Veeam)"),
        ("Rented lifeboats + crew", "CloudCasa (SaaS DR)"),
        ("Drill drill drill", "Quarterly restore test"),
        ("Backup destination", "BackupStorageLocation (S3 / Blob / GCS)"),
        ("Per-volume snapshot", "VolumeSnapshotLocation per CSI driver"),
    ],
    analogy_stops="A real lifeboat is physical; backups are bytes — invisible until restore-tested. Untested backup ≈ no backup.",
    eli5="Four ways to keep a lifeboat ready. The crew practices monthly so the boat works when the ship sinks.",
    eli10="<strong>etcd snapshot</strong>: control-plane state via etcdctl. <strong>Velero</strong>: K8s-native + CSI snapshots / Kopia / Restic. <strong>Kasten K10</strong>: commercial app-aware. <strong>CloudCasa</strong>: SaaS-managed DR. Quarterly restore-test mandatory.",
    scenarios=[
        Scenario(name="Velero saved a tenant from accidental deletion", body="Tenant accidentally deleted prod namespace; Velero hourly backup restored within 15 min; data loss = 1h (within RPO)."),
        Scenario(name="K10 for compliance-heavy regulated cluster", body="Health-tech runs Kasten K10; commercial support + HIPAA reports; restore-tested monthly with documented RTO."),
        Scenario(name="CloudCasa for small team", body="5-engineer SaaS adopts CloudCasa; saved 1-2 engineer-weeks of Velero setup; managed DR for ~$1k/mo."),
        Scenario(name="Outage — backup never restored", body="Cluster died; team tried Velero restore; StorageClass missing; restore failed; 6-hour outage. Postmortem: quarterly restore drill mandated."),
    ],
    misconceptions=[
        Misconception(myth="\"Velero backs up everything.\"", truth="Velero backs up K8s objects + PVCs; doesn\'t back up etcd directly (managed K8s = cloud-managed; self-managed = use etcdctl). Doesn\'t backup external services (RDS, Vault, S3 outside cluster)."),
        Misconception(myth="\"Backup is the hard part.\"", truth="<strong>Restore is the hard part.</strong> Quarterly restore drills find issues that backup verification doesn\'t — StorageClass mismatches, NetworkPolicy misalignment, dependency order."),
        Misconception(myth="\"Cloud-managed K8s makes backup unnecessary.\"", truth="Cloud manages etcd; doesn\'t back up your workloads + PVCs + secrets. Velero / K10 / CloudCasa still required."),
    ],
    flashcards=[
        Flashcard(front="etcd snapshot — when needed?", back="Self-managed clusters; foundation for total-cluster-loss rebuild. Managed K8s (EKS / GKE / AKS) = cloud handles."),
        Flashcard(front="Velero backup what?", back="K8s objects (Deployment / Service / Secret / etc.) + PVCs (via CSI snapshot or Restic / Kopia)."),
        Flashcard(front="BackupStorageLocation — what is it?", back="Velero CR pointing at S3 / Azure Blob / GCS bucket for backup destination."),
        Flashcard(front="Restic vs Kopia in Velero?", back="<strong>Restic</strong>: longer history; widely deployed. <strong>Kopia</strong>: newer; faster; recommended default in modern Velero."),
        Flashcard(front="Kasten K10 differentiator?", back="App-aware (knows DB quiescing); commercial support; richer policies; multi-cluster aggregation."),
        Flashcard(front="CloudCasa — what does it offer?", back="SaaS DR; agent-based; managed by CloudCasa team; hosted simplicity vs self-host."),
        Flashcard(front="Restore-test cadence?", back="Quarterly minimum; semi-annually for critical clusters. Find issues before real loss."),
        Flashcard(front="What backup doesn\'t cover?", back="External managed services (RDS / Vault / S3 / SaaS) — those have their own DR. Backup your K8s state; align with managed-service DR for the full picture."),
    ],
    quizzes=[
        Quiz(prompt="Design backup for a 50-namespace EKS cluster.",
            answer="(1) <strong>Velero</strong> install via Helm. (2) <strong>BackupStorageLocation</strong>: S3 bucket per environment + KMS-encrypted. (3) <strong>VolumeSnapshotLocation</strong>: AWS EBS CSI driver. (4) <strong>Schedule</strong>: nightly full backup + hourly per-namespace + on-demand pre-deploy. (5) <strong>Retention</strong>: 7-day daily + 4-week weekly + 12-month monthly. (6) <strong>Restore-test quarterly</strong>: pick 1 namespace; restore to dev cluster; validate. (7) <strong>Documented RPO + RTO</strong>: per-tier (gold = 1h RPO / 4h RTO; bronze = 24h)."),
        Quiz(prompt="A team\'s prod cluster died at 2 AM. Walk recovery.",
            answer="(1) <strong>Read runbook</strong>: total-cluster-loss procedure. (2) <strong>Provision new cluster</strong> via Terraform / Crossplane (5-15 min). (3) <strong>Restore etcd</strong> if self-managed (or skip on EKS — control plane is managed). (4) <strong>Velero restore</strong>: per-namespace; high-priority first. (5) <strong>Restore PVCs</strong>: CSI snapshots; mount; verify data. (6) <strong>Restore secrets</strong>: ESO re-syncs from external Vault. (7) <strong>DNS swap</strong>: Route 53 record updates point to new cluster Load Balancer. (8) <strong>Validate</strong>: SLO metrics return; tenants notified. (9) <strong>Postmortem</strong>: timeline + gaps + roadmap."),
        Quiz(prompt="The CFO sees Kasten K10 cost ($30k/yr). Defend or refute.",
            answer="\"<strong>Make-vs-buy on backup tooling.</strong> Velero is free + open-source; K10 is commercial. K10 wins when: (1) regulated cluster needs HIPAA / PCI compliance reports out-of-the-box; (2) commercial support SLA matters; (3) team lacks DR engineering time. Velero wins when: (1) team can self-build dashboards + drills; (2) cost-sensitive; (3) workloads simpler. <strong>Right answer per team</strong>: small / cost-sensitive → Velero. Regulated / commercial-support-needed → K10 or CloudCasa.\"", cyoa=True, cyoa_tag="how the DR architect framed make-vs-buy"),
    ],
    glossary=[
        GlossaryItem(name="etcd", definition="K8s control-plane key-value store; holds all API state."),
        GlossaryItem(name="etcdctl snapshot save", definition="Command creating a point-in-time etcd snapshot for backup."),
        GlossaryItem(name="Velero", definition="CNCF K8s-native backup framework; K8s objects + PVCs via CSI / Restic / Kopia."),
        GlossaryItem(name="BackupStorageLocation", definition="Velero CR pointing at S3 / Azure Blob / GCS for backups."),
        GlossaryItem(name="VolumeSnapshotLocation", definition="Velero CR per CSI driver for volume snapshots."),
        GlossaryItem(name="Restic / Kopia", definition="Filesystem-level backup tools used by Velero for non-CSI volumes. Kopia recommended in modern Velero."),
        GlossaryItem(name="Kasten K10", definition="Veeam\'s commercial K8s backup; app-aware; rich policies."),
        GlossaryItem(name="CloudCasa", definition="SaaS DR-as-a-service for K8s."),
        GlossaryItem(name="restore-test", definition="Quarterly drill restoring backup to non-prod; validates backup is restorable."),
        GlossaryItem(name="RPO / RTO", definition="Recovery Point Objective (data loss window) + Recovery Time Objective (recovery time)."),
    ],
    recap_lead="Backup tools: etcd snapshot (self-managed) + Velero (K8s-native) + K10 (commercial) + CloudCasa (SaaS). Quarterly restore-test mandatory.",
    recap_next='<strong>Next — D2: GitOps-driven recovery + cluster rebuild + application restore.</strong>',
)
