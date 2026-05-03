"""K-GKE G5 — GKE Storage (PD / Hyperdisk + Storage Pools, Filestore, GCS FUSE, Parallelstore, Backup for GKE)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GKE storage CSI drivers — PD, Hyperdisk + Storage Pools, Filestore, GCS FUSE, Parallelstore, Backup for GKE.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Reservoir &amp; Compost — five storage backends</text>
  <rect x="40" y="70" width="135" height="120" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="107" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Persistent Disk CSI</text>
  <text x="107" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">RWO block</text>
  <text x="107" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">pd-balanced (default)</text>
  <text x="107" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">pd-ssd</text>
  <text x="107" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">Regional PD (multi-zone)</text>
  <rect x="190" y="70" width="135" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="257" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Hyperdisk</text>
  <text x="257" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Storage Pools</text>
  <text x="257" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">independent IOPS</text>
  <text x="257" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">VolumeAttributesClass</text>
  <text x="257" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">live tier change</text>
  <rect x="340" y="70" width="135" height="120" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="407" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Filestore CSI</text>
  <text x="407" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">RWX shared FS</text>
  <text x="407" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">NFS</text>
  <text x="407" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">Filestore Enterprise</text>
  <text x="407" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">multi-zone option</text>
  <rect x="490" y="70" width="135" height="120" rx="10" fill="#E8B547" stroke="#3F4A5E"/>
  <text x="557" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#5A4F45">GCS FUSE CSI</text>
  <text x="557" y="105" text-anchor="middle" font-size="9" fill="#5A4F45">object as FS</text>
  <text x="557" y="118" text-anchor="middle" font-size="9" fill="#5A4F45">cheap · ML datasets</text>
  <text x="557" y="135" text-anchor="middle" font-size="9" fill="#5A4F45">Parallelstore CSI</text>
  <text x="557" y="148" text-anchor="middle" font-size="9" fill="#5A4F45">HPC / AI training</text>
  <rect x="640" y="70" width="80" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="680" y="88" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Backup</text>
  <text x="680" y="103" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">for GKE</text>
  <text x="680" y="125" text-anchor="middle" font-size="9" fill="#FBF1D6">managed</text>
  <text x="680" y="140" text-anchor="middle" font-size="9" fill="#FBF1D6">cluster-wide</text>
  <text x="680" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">DR primitive</text>
</svg>"""


LESSON = LessonSpec(
    num="05",
    title_short="GKE storage",
    title_full="G5 · GKE Storage (PD, Hyperdisk + Storage Pools, Filestore, GCS FUSE, Parallelstore)",
    title_html="K-GKE G5 · GKE Storage",
    module_eyebrow="Module G5 · the Reservoir &amp; Compost",
    hero_sub_html='Five storage backends as managed CSI drivers. <strong>Persistent Disk CSI</strong> for RWO block (pd-balanced default; pd-ssd; Regional PD for multi-zone HA). <strong>Hyperdisk + Storage Pools</strong> for independent IOPS / throughput tuning + <strong>VolumeAttributesClass</strong> for live tier changes. <strong>Filestore CSI</strong> for RWX (NFS; Enterprise tier multi-zone). <strong>GCS FUSE CSI</strong> for object-as-filesystem. <strong>Parallelstore CSI</strong> for HPC/AI training. Plus <strong>Backup for GKE</strong> as the managed DR primitive.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Postgres CrashLoopBackOff: <em>\"failed to attach disk: zone mismatch\"</em>. PVC bound to a single-zone pd-ssd in <code>us-central1-a</code>; Pod was scheduled in <code>us-central1-c</code>. Cross-zone disk attach is not supported. <em>You used a custom StorageClass without <code>WaitForFirstConsumer</code>.</em> Today\'s lesson: pick the right storage backend; configure zone-awareness right; have Backup for GKE wired before you need it.",
    stamp_html="<strong>Default to PD CSI (pd-balanced) with WaitForFirstConsumer for RWO; Regional PD for cross-zone resilience; Hyperdisk + Storage Pools + VolumeAttributesClass for tunable performance; Filestore for RWX; GCS FUSE for cheap object datasets; Parallelstore for HPC/AI; Backup for GKE for managed DR.</strong>",
    district_pin="kg-plot05",
    district_label="Reservoir &amp; Compost",
    sections=[
        Section(
            eyebrow="Section 1.1 · Persistent Disk CSI",
            h2="Persistent Disk CSI — RWO default",
            body_html="""    <p><strong>Persistent Disk CSI driver</strong> = default RWO storage. Backed by Compute Engine Persistent Disks. Tiers in increasing performance/cost:</p>
    <ul>
      <li><strong>pd-standard</strong> (HDD, cheapest) — for cold / archival workloads.</li>
      <li><strong>pd-balanced</strong> (recommended default) — SSD-backed; balanced cost/perf for most stateful workloads.</li>
      <li><strong>pd-ssd</strong> — high-IOPS SSD; for latency-sensitive DBs.</li>
      <li><strong>pd-extreme</strong> (legacy) — superseded by Hyperdisk.</li>
    </ul>
    <p><strong>Zone affinity (critical):</strong> a standard PD lives in <em>one zone</em>. A Pod can mount a PD only if scheduled in that same zone. The default StorageClass has <code>volumeBindingMode: WaitForFirstConsumer</code> — disk provisioning waits until the Pod is scheduled, then provisions in the right zone. <em>Custom StorageClasses without this setting re-introduce the zone-mismatch bug.</em></p>
    <p><strong>Regional PD</strong> = synchronous replication across two zones in a region. Survives single-zone failure; can attach to a Pod in either zone. Higher latency than zonal; the right choice for stateful workloads needing HA without app-level replication.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Hyperdisk + Storage Pools + VolumeAttributesClass",
            h2="Hyperdisk + Storage Pools + VolumeAttributesClass",
            body_html="""    <p><strong>Hyperdisk</strong> = next-gen GCP block storage. Variants:</p>
    <ul>
      <li><strong>Hyperdisk Balanced</strong> — general-purpose; replaces pd-balanced for many use cases.</li>
      <li><strong>Hyperdisk Throughput</strong> — high-throughput workloads (analytics, log processing).</li>
      <li><strong>Hyperdisk Extreme</strong> — extreme IOPS; for SAP HANA, large OLTP.</li>
      <li><strong>Hyperdisk ML</strong> — optimised for ML training data loading; multi-attach supported.</li>
    </ul>
    <p><strong>Storage Pools</strong> = the pool-based capacity model: provision capacity + IOPS + throughput at the <em>pool</em> level; carve PVCs out of the pool. <em>Decouples per-PVC over-provisioning from total cost.</em> Many workloads at low utilisation share the pool; cost reflects actual consumption.</p>
    <p><strong>VolumeAttributesClass</strong> (K8s GA feature) — change a PV\'s performance attributes <em>online</em>, no remount. With Hyperdisk: change IOPS / throughput targets via a <code>VolumeAttributesClass</code> reference on the PVC. Example: tune Postgres from 3,000 IOPS to 16,000 for a holiday-traffic event without restarting the Pod.</p>
    <p><strong>Snapshots</strong> (K8s VolumeSnapshot CRD) — point-in-time backup of a PV; restore by creating a new PVC with <code>dataSource</code> pointing at the snapshot. Cross-region snapshot replication via the Compute Engine snapshot location.</p>
    <p><strong>Online expansion</strong> — increase PVC size; Hyperdisk + PD support online filesystem grow without unmount.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Filestore + GCS FUSE + Parallelstore",
            h2="Filestore CSI + GCS FUSE CSI + Parallelstore CSI",
            body_html="""    <p><strong>Filestore CSI</strong> = RWX shared filesystem via NFS. Tiers: <em>Basic HDD/SSD</em> (legacy), <em>Zonal</em> (single zone), <em>Enterprise</em> (multi-zone HA). Use cases: shared writable storage across multiple Pods (CMS uploads, build artifacts, ML scratch). <em>Avoid for high-IOPS DB workloads</em> — Hyperdisk Extreme is the right tier for that.</p>
    <p><strong>GCS FUSE CSI</strong> = mount a GCS bucket as a filesystem in a Pod. Backed by Cloud Storage FUSE. Use cases: huge ML training datasets read sequentially (TBs at object-storage cost ~$0.02/GB-month vs PD ~$0.17/GB-month for Standard tier); image/asset libraries; cheap append-only logs. <em>Performance is not block-class</em> — fine for sequential reads, not transactional DBs. Caching modes available for repeat-read workloads.</p>
    <p><strong>Parallelstore CSI</strong> = managed parallel filesystem for HPC + AI training. Backed by DDN EXAScaler. Throughput in the GiB/s range across multiple clients. Use cases: distributed training where multiple GPU nodes need to read training data simultaneously at line rate; HPC simulations; anything that hits the bandwidth wall on standard NFS. <em>Pricier per GB; the right answer when training-step time is bottlenecked on data loading.</em></p>"""
        ),
        Section(
            eyebrow="Section 1.4 · Backup for GKE + Secret Manager CSI + topology",
            h2="Backup for GKE + Secret Manager CSI + topology-aware scheduling",
            body_html="""    <p><strong>Backup for GKE</strong> = managed backup service. Captures cluster-wide K8s manifests + Persistent Volume snapshots + (optionally) cross-region restoration. Schedule + retention policies via the Backup for GKE API. Restore into the same or a different cluster. <em>The DR primitive — wire this in early; it\'s much harder to retrofit during an incident.</em></p>
    <p><strong>Secret Manager CSI driver</strong> (covered in G4) — mount Secret Manager secrets as files in Pods, WIF-authenticated, auto-rotation. The clean way to consume secrets without K8s Secrets in etcd.</p>
    <p><strong>Topology-aware scheduling:</strong> StorageClass <code>allowedTopologies</code> can constrain disks to specific zones (e.g., force DB disks into <code>us-central1-a</code> for a hot/warm DR pattern). Combined with Pod nodeSelector or topology-spread constraints to keep workloads + storage co-located.</p>
    <p><strong>CMEK across storage:</strong> all five backends support CMEK via Cloud KMS — disks, Filestore, GCS, Parallelstore, snapshots — for compliance + key sovereignty. Key rotation is a Cloud KMS operation; PVs continue to work transparently.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A Pod with a pd-ssd PVC keeps failing to start in a multi-zone cluster. Why?",
            options=[
                ("Switch to pd-standard.", False),
                ("Use the default StorageClass with <code>volumeBindingMode: WaitForFirstConsumer</code> so the PD provisions in the Pod\'s zone — or use Regional PD for multi-zone resilience.", True),
                ("Increase replicas.", False),
            ],
            feedback="Single-zone PDs cannot attach across zones. WaitForFirstConsumer aligns provisioning with scheduling; Regional PD adds cross-zone replication.",
        ),
    },
    before_after_before='<p>Pre-CSI GKE used in-tree volume drivers — limited features, no online resize for a long time, no VolumeSnapshot CRD, no VolumeAttributesClass. RWX needed third-party Helm-installed nfs-server-provisioner with manual Filestore wiring. ML training data on PD = expensive; HPC parallel filesystems were DIY (Lustre on GCE). DR was \"hope you have a snapshot script.\"</p>',
    before_after_after='<p>Modern GKE ships <strong>five managed CSI drivers</strong> (PD, Hyperdisk + Storage Pools, Filestore, GCS FUSE, Parallelstore) with VolumeSnapshot, online expansion, VolumeAttributesClass for live tier changes. <strong>Backup for GKE</strong> is the managed DR primitive (cluster-wide manifests + PV snapshots; cross-region restoration). Secret Manager CSI for keyless secrets. <em>Storage in GKE is now declarative, performant, and survivable.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Pick the backend that matches the access mode + performance class. Don\'t skip Backup for GKE — DR not wired before incident = DR not available during incident.</em></p>',
    analogy_intro_html='''<p>The <strong>Reservoir &amp; Compost</strong> is the K-Garden\'s storage building. Five backends.</p>
    <p><strong>Personal water tanks</strong> (Persistent Disk): one tank per gardener, fast, locked. The tank lives in a specific zone of the garden; for cross-zone resilience, use the Regional PD twin-tank that replicates synchronously across two zones.</p>
    <p><strong>Hyperdisk pool</strong>: instead of buying a personal tank, you draw from a <em>shared reservoir</em> the head gardener provisions; capacity, IOPS, and throughput are pool-level. A magical valve (VolumeAttributesClass) lets you turn the pressure up live without unhooking your hose. Variants: balanced for general use, throughput-tuned for big sprinklers, extreme for HANA-class precision irrigation, ML-tuned for training-data multi-attach.</p>
    <p><strong>Shared communal sink</strong> (Filestore): multiple gardeners use the same NFS sink for shared seedling washing. Enterprise tier replicates across zones.</p>
    <p><strong>Compost pile / mulch warehouse</strong> (GCS FUSE): cheap stacks holding 200 TB of training data; you fetch by armful when needed. Sequential reads only — not for transactional grabs.</p>
    <p><strong>HPC parallel pump system</strong> (Parallelstore): when 100 gardeners are all loading training data simultaneously and your throughput needs are GiB/s.</p>
    <p>And the <strong>Disaster-Relief Vault</strong> (Backup for GKE) is the managed insurance: weekly snapshots of the whole garden\'s state, restorable into a new garden in a different region.</p>''',
    translation_rows=[
        ("Personal water tank", "Persistent Disk CSI — RWO PV"),
        ("Tank in a specific zone", "Single-zone pd-ssd / pd-balanced"),
        ("Twin-tank cross-zone", "Regional PD"),
        ("Shared reservoir + magical valve", "Hyperdisk + Storage Pools + VolumeAttributesClass"),
        ("Magical pressure valve", "VolumeAttributesClass — live IOPS / throughput change"),
        ("Communal sink (NFS)", "Filestore CSI — RWX"),
        ("Filestore zonal vs Enterprise", "Single-zone vs multi-zone HA"),
        ("Compost pile / mulch warehouse", "GCS FUSE CSI"),
        ("HPC parallel pump system", "Parallelstore CSI (HPC / AI training)"),
        ("Disaster-Relief Vault", "Backup for GKE"),
        ("Vault key-fetch desk", "Secret Manager CSI driver (covered in G4)"),
        ("\"Wait for the gardener before issuing the tank\"", "<code>volumeBindingMode: WaitForFirstConsumer</code>"),
        ("Photocopying a chapter", "VolumeSnapshot CRD"),
        ("Adding shelves to existing tank", "Online volume expansion"),
        ("\"Padlock with your key on every storage room\"", "CMEK via Cloud KMS"),
    ],
    analogy_stops="A garden\'s tanks are physical and bounded; CSI drivers can be added or upgraded without rebuilding the cluster. Real Hyperdisk has compatibility constraints with specific machine families the metaphor doesn\'t capture.",
    eli5="Five storage choices: a personal tank, a shared reservoir with a magical pressure valve, a communal sink, a compost-warehouse for huge cheap stuff, and a parallel-pump for HPC. Plus an insurance vault that backs up the whole garden weekly.",
    eli10="GKE storage = five managed CSI drivers. <strong>PD CSI</strong> for RWO (pd-balanced default; pd-ssd; <strong>Regional PD</strong> for cross-zone HA; default StorageClass uses WaitForFirstConsumer for zone-correct provisioning). <strong>Hyperdisk + Storage Pools</strong> for tunable IOPS/throughput + VolumeAttributesClass live changes. <strong>Filestore CSI</strong> for RWX (NFS, Enterprise tier multi-zone). <strong>GCS FUSE CSI</strong> for cheap object-as-FS (ML datasets). <strong>Parallelstore CSI</strong> for HPC/AI parallel filesystem. Plus <strong>Backup for GKE</strong> for managed DR (cluster-wide manifests + PV snapshots, cross-region restore). VolumeSnapshot CRD for backup; online expansion supported; CMEK across all backends.",
    scenarios=[
        Scenario(
            name="Postgres on GKE — Regional PD for HA without app-level replication",
            body="A small Postgres workload on GKE — single primary, no streaming replica yet. Team uses <strong>Regional PD</strong> on a Hyperdisk Balanced StorageClass. PVC bound to a Regional PD that replicates synchronously across us-central1-a + us-central1-c. Pod scheduled in either zone can mount. <em>Single-zone failure: Pod re-schedules to surviving zone with same data.</em>",
        ),
        Scenario(
            name="ML team — GCS FUSE for 200 TB training data",
            body="ML team needs read-only access to 200 TB image datasets across hundreds of training Pods. PD for this = $30K+/month. <strong>GCS FUSE</strong> mounts the bucket as a Pod filesystem; sequential reads with caching mode. Cost: ~$4K/month (Cool tier). <em>Same throughput; ~85% saving.</em>",
        ),
        Scenario(
            name="Hyperdisk + VolumeAttributesClass for Black Friday burst",
            body="Postgres workload on Hyperdisk Balanced provisioned at 3,000 IOPS / 240 MiB/s. Black Friday traffic 10×. Team creates a VolumeAttributesClass with 16,000 IOPS / 800 MiB/s, references it from the PVC. Hyperdisk applies online; no Pod restart. After the event, switch back to the lower-spec VAC. <em>Pay for high tier only during the burst.</em>",
        ),
        Scenario(
            name="Bank — quarterly Backup for GKE drill restored cluster in 35 minutes",
            body="A bank schedules nightly Backup for GKE backups: cluster-wide manifests + all PV snapshots, cross-region replication to the paired DR region. Quarterly drill: spin up empty cluster in DR region; restore from latest backup; verify workloads. <em>Last drill: restoration completed in 35 minutes; auditor approved RTO target of &lt; 1 hour.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Regional PD doubles my storage cost for free HA.\"",
            truth="Regional PD synchronously replicates across two zones. Cost is roughly 2x a single-zone disk + small write-latency overhead (sync replication). For workloads that don\'t need cross-zone attach, single-zone PD + Backup for GKE for DR is cheaper. Pick Regional PD when the workload genuinely needs cross-zone attach.",
        ),
        Misconception(
            myth="\"Storage Pools are for cost-saving teams; everyone else uses individual Hyperdisks.\"",
            truth="Storage Pools shine when you have <em>many PVCs at low utilisation</em>. Pool capacity and IOPS budget shared = aggregate spend matches actual peak rather than sum-of-per-PVC peaks. For one or two huge PVCs at sustained 100% utilisation, individual Hyperdisks are simpler. The mental model: pool when you have many tenants; individual when you have few large ones.",
        ),
        Misconception(
            myth="\"GCS FUSE is fine for transactional databases.\"",
            truth="GCS FUSE is object-storage-as-FS. Eventual consistency on metadata + non-POSIX semantics (no fsync guarantees, no real file locking, latency in the 100ms+ range for object operations). Catastrophic for transactional DBs. Excellent for ML datasets, image/asset libraries, append-only log archives — anything sequential-read.",
        ),
    ],
    flashcards=[
        Flashcard(front="Five GKE managed storage CSI drivers?", back="<strong>Persistent Disk</strong> (RWO block; pd-balanced default; Regional PD), <strong>Hyperdisk + Storage Pools</strong> (tunable IOPS/throughput + VolumeAttributesClass), <strong>Filestore</strong> (RWX NFS), <strong>GCS FUSE</strong> (object-as-FS), <strong>Parallelstore</strong> (HPC/AI parallel filesystem). Plus <strong>Backup for GKE</strong> for DR."),
        Flashcard(front="Why is WaitForFirstConsumer critical for multi-zone GKE?", back="Single-zone PDs can\'t cross-zone-attach. WaitForFirstConsumer delays disk provisioning until the Pod is scheduled, so the disk lands in the right zone. Without it, the scheduler may place the Pod in zone A but disk got provisioned in zone B = attach failure."),
        Flashcard(front="What\'s a Regional PD?", back="Persistent Disk synchronously replicated across two zones in a region. Cross-zone attach supported. Survives single-zone failures. ~2x cost + small write-latency overhead vs zonal PD."),
        Flashcard(front="What does VolumeAttributesClass do?", back="K8s GA feature — change a PV\'s performance attributes (IOPS, throughput) <em>online</em>, no remount. With Hyperdisk: tune IOPS up for a holiday burst, then back down — Pod doesn\'t restart."),
        Flashcard(front="When use GCS FUSE CSI?", back="Read-heavy sequential workloads on huge cheap data: ML training datasets (TBs at object-storage prices), image/asset libraries, append-only logs. Not for transactional DBs (eventual consistency on metadata + non-POSIX semantics)."),
        Flashcard(front="When use Parallelstore CSI?", back="HPC + AI training where multiple clients read at GiB/s. Distributed training across many GPU nodes. HPC simulations. Backed by DDN EXAScaler. Pricier per GB; right answer when training-step time is data-loading-bound."),
        Flashcard(front="What is Backup for GKE?", back="Managed backup service: captures cluster-wide K8s manifests + PV snapshots; supports cross-region restoration. Schedule + retention policies via the Backup for GKE API. Wire in early; the DR primitive."),
        Flashcard(front="Storage Pools vs individual Hyperdisks?", back="<strong>Storage Pools</strong> = pool capacity + IOPS + throughput; carve PVCs out. Best when many low-utilisation PVCs share a pool — total cost reflects actual peak. <strong>Individual Hyperdisks</strong> = simpler for few large PVCs at sustained high utilisation."),
    ],
    quizzes=[
        Quiz(
            prompt="A team migrates a stateful workload to a multi-zone GKE cluster. They wrote a custom StorageClass without specifying <code>volumeBindingMode</code>. Pods now intermittently fail to start. What\'s happening?",
            answer="Default volumeBindingMode is <code>Immediate</code> — disks provision as soon as the PVC is created, in whichever zone the controller picks. The kube-scheduler then schedules the Pod independently — and may place it in a different zone. Cross-zone attach is unsupported for single-zone PDs. Fix: edit the StorageClass to <code>volumeBindingMode: WaitForFirstConsumer</code>; new PVCs provision in the correct zone. (Existing mis-zoned PVCs need recreating in the right zone or migration to Regional PD.)",
        ),
        Quiz(
            prompt="A Hyperdisk Balanced PVC was provisioned at 3000 IOPS / 240 MiB/s for Postgres. Black Friday traffic 10×. The team needs 16K IOPS for 5 days. What\'s the safe path that doesn\'t require Pod restart?",
            answer="Create a <strong>VolumeAttributesClass</strong> with target 16K IOPS / 800 MiB/s; reference it from the PVC: <code>spec.volumeAttributesClassName: postgres-burst</code>. Hyperdisk applies online; no detach, no remount, no Pod restart. Postgres continues serving traffic; new IOPS available within seconds. After 5 days: switch the PVC to a lower-spec VAC; pay only for the burst window.",
        ),
        Quiz(
            prompt="The CFO sees the storage bill: \"Why is observability + Backup for GKE costing more than half our cluster compute?\" The platform engineer investigates. What are the levers?",
            answer="Backup costs come from: (1) snapshot frequency (nightly vs hourly), (2) retention period (30 days × all PVs = a lot), (3) cross-region replication. Levers: (a) tune backup schedule to RPO needs — most workloads don\'t need hourly backups. (b) tier retention by data class (PHI longer; ephemeral shorter). (c) cross-region replication only for genuinely DR-tier workloads, not all. (d) review GCS retention + storage class on snapshot data. <em>Common pattern: drop snapshot retention on dev/staging clusters from 30 days to 7; cross-region only for prod regulated workloads. Often 50%+ saving without compromising real DR posture.</em>",
            cyoa=True,
            cyoa_tag="how the platform engineer tuned the backup bill",
        ),
    ],
    glossary=[
        GlossaryItem(name="Persistent Disk CSI", definition="Default RWO storage. pd-standard / pd-balanced / pd-ssd tiers. WaitForFirstConsumer in default StorageClass for zone-correct provisioning."),
        GlossaryItem(name="Regional PD", definition="Persistent Disk synchronously replicated across two zones. Cross-zone attach. Survives single-zone failures."),
        GlossaryItem(name="Hyperdisk", definition="Next-gen GCP block storage. Variants: Balanced, Throughput, Extreme, ML. Decoupled IOPS / throughput tuning."),
        GlossaryItem(name="Storage Pools", definition="Pool-based capacity model: capacity + IOPS + throughput at the pool level; carve PVCs out. Best for many low-utilisation PVCs."),
        GlossaryItem(name="VolumeAttributesClass", definition="K8s GA feature — change PV performance attributes online, no remount. With Hyperdisk: live IOPS / throughput retier."),
        GlossaryItem(name="Filestore CSI", definition="RWX storage via NFS. Tiers: Zonal, Enterprise (multi-zone HA)."),
        GlossaryItem(name="GCS FUSE CSI", definition="Mount a Cloud Storage bucket as a Pod filesystem. Cheap; sequential-read workloads (ML datasets, asset libraries)."),
        GlossaryItem(name="Parallelstore CSI", definition="Managed parallel filesystem (DDN EXAScaler) for HPC + AI training. GiB/s throughput across clients."),
        GlossaryItem(name="Backup for GKE", definition="Managed cluster-wide backup: K8s manifests + PV snapshots; cross-region restore. The DR primitive."),
        GlossaryItem(name="VolumeSnapshot", definition="K8s standard CRD for point-in-time PV backup. Backed by Compute Engine snapshots."),
        GlossaryItem(name="WaitForFirstConsumer", definition="StorageClass binding mode that delays PV provisioning until the Pod is scheduled — ensures zone alignment."),
        GlossaryItem(name="CMEK on storage", definition="Customer-Managed Encryption Keys via Cloud KMS — applies to PD, Filestore, GCS, Parallelstore, snapshots."),
    ],
    recap_lead='Five storage backends mapped to use cases; Hyperdisk + Storage Pools + VolumeAttributesClass for tunable performance; Backup for GKE wired early; multi-zone via Regional PD or topology + WaitForFirstConsumer.',
    recap_next='<strong>Next — G6: GKE Scaling and Cost.</strong> Cluster Autoscaler, Node Auto-Provisioning (NAP), Autopilot scheduling/billing, Compute Classes (Balanced / Performance / Scale-Out / Accelerator), Spot, GPU (A3/A4 with H100/H200/B200), TPU (Trillium / Ironwood), HPA with custom metrics, BigQuery cost export.',
)
