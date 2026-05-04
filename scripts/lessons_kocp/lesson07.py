"""K-OCP O7 — OpenShift Storage (ODF, Local/LVM Operators, CSI per-cloud, RWX, snapshots, OADP)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OCP storage — ODF, Local/LVM Operators, CSI per-cloud, RWX, snapshots, OADP.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Inventory Warehouse — software-defined + cloud + edge</text>
  <rect x="40" y="65" width="170" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="125" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">ODF (Software-defined)</text>
  <text x="125" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">Ceph (block + file)</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">NooBaa (object)</text>
  <text x="125" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">Rook (orchestrator)</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">RWX shared FS</text>
  <rect x="225" y="65" width="170" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="310" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">edge / single-node</text>
  <text x="310" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">Local Storage Operator</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">LVM Storage Operator</text>
  <text x="310" y="135" text-anchor="middle" font-size="9" fill="#FFFFFF">SNO + edge sites</text>
  <rect x="410" y="65" width="170" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="495" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">cloud CSI</text>
  <text x="495" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">vSphere CSI</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">AWS EBS</text>
  <text x="495" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">Azure Disk / File</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">GCP PD</text>
  <rect x="595" y="65" width="125" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="657" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">protection</text>
  <text x="657" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">snapshots</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">OADP (Velero)</text>
  <text x="657" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">registry storage</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">monitoring storage</text>
</svg>"""


LESSON = LessonSpec(
    num="07", title_short="OCP storage",
    title_full="O7 · OpenShift Storage (ODF + Local/LVM Operators + cloud CSI + OADP)",
    title_html="K-OCP O7 · OpenShift Storage",
    module_eyebrow="Module O7 · the Inventory Warehouse",
    hero_sub_html='<strong>OpenShift Data Foundation (ODF)</strong> — Ceph (block + file) + NooBaa (object) + Rook (orchestrator). Software-defined storage built into the cluster. <strong>Local Storage Operator</strong> + <strong>LVM Storage Operator</strong> for single-node / edge. <strong>Per-cloud CSI</strong>: vSphere CSI, AWS EBS, Azure Disk/File, GCP PD. <strong>RWX storage</strong> via ODF CephFS or NFS. <strong>VolumeSnapshot</strong> across CSI drivers. <strong>OADP (OpenShift APIs for Data Protection)</strong> — Velero-based + integrated. Registry storage + monitoring storage planning.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"Container Image registry CO degraded; image pulls returning 5xx.\"</em> The internal registry uses a PVC backed by AWS EBS gp3 in zone-a. Worker nodes scaled to zone-b last night via MachineSet. Registry pod migrated to a zone-b node; PVC failed to attach (cross-zone EBS attach not supported). Plus monitoring (Prometheus) is on a different PVC also single-zone — alerts about the registry are themselves silenced because Prometheus storage is in the same failure domain. <em>You don\'t know the storage architecture for either component.</em> Today\'s lesson: OCP storage planning + multi-zone-aware design + DR.",
    stamp_html="<strong>Default to ODF for software-defined storage with RWX + object; Local/LVM Operators for SNO/edge; per-cloud CSI for cloud-native deployments. Plan registry + monitoring storage at install. OADP for backup/DR.</strong>",
    district_pin="ko-bay07", district_label="Inventory Warehouse",
    sections=[
        Section(eyebrow="Section 1.1 · ODF", h2="OpenShift Data Foundation (ODF) — Ceph + NooBaa + Rook",
            body_html="""    <p><strong>OpenShift Data Foundation (ODF)</strong> is Red Hat\'s software-defined storage platform built on:</p>
    <ul>
      <li><strong>Ceph</strong> — distributed block + filesystem storage. RBD (block) + CephFS (RWX shared FS).</li>
      <li><strong>NooBaa</strong> — multi-cloud object storage gateway. Speaks S3 API; can back to local Ceph or external clouds.</li>
      <li><strong>Rook</strong> — Kubernetes operator that orchestrates Ceph (deployment, scaling, recovery).</li>
    </ul>
    <p>ODF runs <em>inside</em> the OCP cluster — Ceph OSD pods on dedicated worker nodes (typically 3+ nodes with attached local or block-storage devices). Provides:</p>
    <ul>
      <li>Block storage (PVC type RWO) via CephRBD CSI.</li>
      <li>RWX shared filesystem via CephFS CSI.</li>
      <li>Object storage via NooBaa S3 endpoint.</li>
    </ul>
    <p><strong>Use case:</strong> on-prem clusters needing software-defined storage; bare-metal deployments where you don\'t have a cloud-block-storage equivalent; clusters needing RWX without external NFS.</p>
    <p>Sizing: 3+ ODF storage nodes; 4+ TB raw capacity per node typical for small clusters; replicate-3 or erasure-coded; ~2-3x raw → usable conversion.</p>"""),
        Section(eyebrow="Section 1.2 · Local + LVM + cloud CSI", h2="Local Storage Operator + LVM Storage Operator + cloud CSI drivers",
            body_html="""    <p><strong>Local Storage Operator</strong> — for nodes with attached block devices that need to be exposed as PVs (e.g., bare-metal NVMe). Uses <code>LocalVolume</code> + <code>LocalVolumeSet</code> CRs to discover + provision local block devices as PVs. Static-provisioned PVs (no dynamic creation). For workloads that benefit from local storage (Cassandra, Elasticsearch, Kafka).</p>
    <p><strong>LVM Storage Operator (LVMS)</strong> — single-node + edge clusters where ODF\'s 3-node minimum doesn\'t fit. Carves a single node\'s storage into LVM volumes; provides dynamic PVCs from a thin pool. <em>For SNO + MicroShift + small edge clusters.</em></p>
    <p><strong>Per-cloud CSI drivers</strong> shipped with OCP:</p>
    <ul>
      <li><strong>vSphere CSI</strong> — VMDK-backed PVCs on vSphere installations.</li>
      <li><strong>AWS EBS CSI</strong> — gp2/gp3/io1/io2 EBS volumes; single-zone; topology-aware.</li>
      <li><strong>Azure Disk CSI</strong> + <strong>Azure File CSI</strong> — disk for RWO; file for RWX SMB/NFS.</li>
      <li><strong>Google PD CSI</strong> — pd-balanced/pd-ssd; single-zone or Regional PD for cross-zone.</li>
    </ul>
    <p>OCP installs the right CSI driver automatically based on the cluster\'s platform (set during install). Default StorageClass uses <code>volumeBindingMode: WaitForFirstConsumer</code> to align PV creation with Pod scheduling zone.</p>"""),
        Section(eyebrow="Section 1.3 · RWX + snapshots + expansion + VolumeAttributesClass",
            h2="RWX storage + VolumeSnapshot + expansion + VolumeAttributesClass",
            body_html="""    <p><strong>RWX (ReadWriteMany)</strong> options on OCP:</p>
    <ul>
      <li><strong>ODF CephFS</strong> — multi-zone, integrated with cluster.</li>
      <li><strong>Azure Files CSI</strong> (SMB or NFS) — managed RWX on Azure.</li>
      <li><strong>NFS</strong> via external NFS server + nfs-csi-driver Operator (community) — for on-prem with existing NetApp / Isilon.</li>
      <li><strong>EFS CSI</strong> on AWS — managed RWX via Elastic File System.</li>
    </ul>
    <p><strong>VolumeSnapshot</strong> (K8s standard) — supported across all OCP-shipped CSI drivers. Per-PV point-in-time snapshot; restore by creating new PVC with <code>dataSource</code> referencing the snapshot.</p>
    <p><strong>Online volume expansion</strong> — supported by all OCP cloud + ODF CSI drivers. Edit PVC <code>spec.resources.requests.storage</code> upward; CSI driver expands the underlying volume + filesystem.</p>
    <p><strong>VolumeAttributesClass</strong> — K8s GA feature for live tier change without remount. With ODF: change Ceph storage-class quality params on the running PVC. With cloud CSIs: cloud-provider-specific support (e.g., AWS gp3 IOPS retier).</p>"""),
        Section(eyebrow="Section 1.4 · OADP + registry + monitoring", h2="OADP (Velero-based) + registry storage + monitoring storage",
            body_html="""    <p><strong>OADP (OpenShift APIs for Data Protection)</strong> = Velero-based managed backup integrated with OCP. <strong>DataProtectionApplication</strong> CR configures backup destination (S3 / NooBaa / Azure Blob / GCS); <strong>Backup</strong> CR triggers cluster-wide manifest + PV snapshot backup; <strong>Restore</strong> CR rehydrates into the same or different cluster. Cross-cluster + cross-region restore.</p>
    <p>OADP also handles application-consistent snapshots via Velero plugins (Restic-based for non-snapshot-supporting CSI drivers; CSI snapshot for the rest). Schedule + retention policies via Velero Schedule CR.</p>
    <p><strong>Registry storage planning:</strong> the internal container registry needs a PVC backed by storage that survives Pod migration. <em>If using EBS / Azure Disk / GCE PD (single-zone), the registry must be pinned to a single zone</em> — accept the failure mode or switch to ODF / NooBaa / external S3-compatible bucket. For prod, S3 / NooBaa / GCS / Azure Blob is the recommended backend (registry storage doesn\'t need block; object suffices).</p>
    <p><strong>Monitoring storage:</strong> Prometheus stores TSDB data in PVCs (default 15-day retention). Plan storage class + size per cluster. For long-term storage, use Thanos sidecar to ship blocks to S3-compatible storage. <em>Don\'t put Prometheus storage on the same single-zone PD as the workloads it monitors — single-zone failure means alerts about the failure are themselves silenced.</em></p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A SNO cluster needs PVCs for tenant workloads. ODF requires 3+ nodes. What\'s the right Operator?",
        options=[("Skip storage on SNO.", False),
            ("LVM Storage Operator (LVMS) — carves a single node\'s storage into LVM volumes, dynamic PVCs from thin pool. Designed for SNO + edge.", True),
            ("Local Storage Operator — but it does static provisioning, not dynamic.", False)],
        feedback="LVMS is the SNO storage path. Local Storage Operator is for static block-device exposure; LVMS does dynamic LVM-backed PVCs.",
    )},
    before_after_before='<p>Pre-CSI OCP used in-tree volume drivers — fewer features, slow innovation. RWX on bare-metal needed third-party NFS server install. ODF was a separate product with manual operator install. Edge / SNO had no managed storage path; you ran NFS or other DIY. Backup/DR was Velero self-installed; no integrated CR + cluster operator support.</p>',
    before_after_after='<p>OCP ships <strong>ODF as a productized + supported software-defined storage platform</strong> (Ceph + NooBaa + Rook). <strong>Local + LVM Storage Operators</strong> for SNO/edge. <strong>Per-cloud CSI</strong> drivers shipped + auto-installed by platform. <strong>OADP</strong> as integrated Velero-based DR. <strong>VolumeSnapshot</strong> + <strong>online expansion</strong> + <strong>VolumeAttributesClass</strong> across drivers.</p>',
    before_after_caption='<p class="ba-caption"><em>Pick the storage backend that matches your cluster shape: ODF for on-prem multi-node; per-cloud CSI for cloud; LVMS for SNO/edge. Wire OADP for DR before you need it.</em></p>',
    analogy_intro_html='''<p>The <strong>Inventory Warehouse</strong> at K-Foundry is where parts are stored. Multiple shelving systems coexist.</p>
    <p>The <strong>ODF system</strong> is the foundry-built shelving — Ceph robots (block + file storage), NooBaa concierge (S3 object storage), Rook foreman managing it all. Sized for the foundry; replicates parts across 3+ shelves for resilience. Provides every kind of part-storage need (RWO block, RWX shared filesystem, object).</p>
    <p>For <em>satellite warehouses</em> (SNO + edge sites), the <strong>Local + LVM Operators</strong> manage local-only shelves: simpler, smaller, no robot army needed.</p>
    <p>For <em>cloud-built foundries</em>, the right cloud-provider shelf is auto-installed: vSphere shelves on vSphere, EBS on AWS, Disk/File on Azure, PD on GCP. Each respects its cloud\'s zone constraints.</p>
    <p>The <strong>OADP backup desk</strong> (Velero-based) takes nightly inventory snapshots + ships them to a remote vault (S3 / Azure Blob / GCS / NooBaa). Restore = rehydrate into the same or different foundry.</p>''',
    translation_rows=[("ODF foundry-built shelving", "OpenShift Data Foundation (Ceph + NooBaa + Rook)"),
        ("Ceph block-storage robots", "CephRBD CSI (RWO)"),
        ("Ceph file-share robots", "CephFS CSI (RWX)"),
        ("NooBaa S3 concierge", "NooBaa object storage gateway"),
        ("Rook foreman", "Rook operator (orchestrates Ceph)"),
        ("Satellite warehouse shelves", "Local Storage + LVM Storage Operators (SNO/edge)"),
        ("Cloud-provider shelves", "Per-cloud CSI (vSphere / AWS EBS / Azure Disk+File / GCP PD)"),
        ("Wait-for-customer policy", "<code>volumeBindingMode: WaitForFirstConsumer</code>"),
        ("Photocopy a shelf", "VolumeSnapshot CRD"),
        ("Add room to a shelf", "Online volume expansion"),
        ("Live shelf-tier upgrade", "VolumeAttributesClass"),
        ("Backup desk + remote vault", "OADP (Velero) + S3/Azure Blob/GCS backup destination"),
        ("Internal-parts shelf", "Internal container registry storage (PVC or S3-compatible)"),
        ("Monitoring archive shelf", "Prometheus TSDB + Thanos to long-term S3")],
    analogy_stops="A real warehouse has fixed walls; ODF is software-defined and grows by adding worker nodes with disks. Real Ceph requires careful tuning the metaphor doesn\'t capture.",
    eli5="The warehouse has many shelf types: foundry-built (ODF), small-shop shelves (LVMS), cloud-provider shelves (CSI), and a backup desk that copies inventory to a remote vault.",
    eli10="OCP storage = ODF (Ceph + NooBaa + Rook for SDS) + Local Storage Operator + LVM Storage Operator (SNO/edge) + per-cloud CSI (vSphere/EBS/Azure/PD). RWX via ODF CephFS / Azure Files / NFS / EFS. VolumeSnapshot + online expansion + VolumeAttributesClass across drivers. OADP (Velero-based) for backup/DR with S3/Blob/GCS/NooBaa destinations. Plan registry + monitoring storage at install.",
    scenarios=[
        Scenario(name="Bank — ODF on-prem with RWX for shared logs",
            body="On-prem bank cluster: ODF with 4 storage nodes + 8TB local NVMe each. CephRBD provides RWO PVCs; CephFS provides RWX for a shared logs directory consumed by 12 microservices; NooBaa provides internal S3 for image registry + Prometheus long-term storage. <em>One software-defined storage platform; no external SAN required.</em>"),
        Scenario(name="Telco — LVMS on SNO at 800 cell sites",
            body="Each cell site = 1 SNO. LVM Storage Operator carves the single node\'s 2TB SSD into thin-pool LVM volumes; provides dynamic PVCs for site-local workloads. ACM (covered in O10) federates the 800 SNOs."),
        Scenario(name="AWS — registry on NooBaa-backed S3 instead of EBS",
            body="AWS-installed OCP. Default registry uses EBS PVC — single-zone, fails on Pod migration. Migration: install ODF + NooBaa; switch registry to NooBaa S3 endpoint; registry now zone-resilient. Same fix could use AWS S3 directly. <em>Simple registry storage gotcha; bake the fix into install runbook.</em>"),
        Scenario(name="DR drill — OADP restored cluster in 38 minutes",
            body="Bank schedules nightly OADP backups: cluster-wide manifests + PV snapshots; cross-region replicated to S3 in DR region. Quarterly drill: spin up empty cluster in DR region; <code>oc create restore</code>; verify workloads + data come up. <em>Last drill: 38 minutes total; auditor approved RTO of < 1 hour.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"ODF is overkill for small clusters.\"",
            truth="For multi-node clusters needing RWX + object storage + DR alongside RWO, ODF is often the simplest path — one platform vs assembling NFS server + S3 service + block storage separately. <em>For SNO/edge, ODF\'s 3-node minimum doesn\'t fit — use LVMS instead.</em>"),
        Misconception(myth="\"VolumeSnapshot backs up everything.\"",
            truth="VolumeSnapshot is a per-PV point-in-time snapshot — preserves block/file data but not application consistency (e.g., a Postgres mid-transaction snapshot is corrupt without quiescing). For app-consistent backups: Velero/OADP with appropriate Restic or CSI plugin + pre/post hooks (e.g., <code>pg_dump</code> before snapshot)."),
        Misconception(myth="\"Single-zone EBS PVC is fine for everything.\"",
            truth="Single-zone EBS = if the holding zone fails, the PVC is unrecoverable until zone returns. <em>For stateful workloads needing multi-zone, use Regional EBS, ODF (multi-node Ceph spans zones), Azure Files / EFS / Filestore, or app-level replication (Postgres streaming replica)</em>. Internal registry, Prometheus, etcd backups all need multi-zone-aware planning."),
    ],
    flashcards=[
        Flashcard(front="What is ODF?", back="<strong>OpenShift Data Foundation</strong> = Ceph (block + file) + NooBaa (object) + Rook (orchestrator). Software-defined storage platform integrated with OCP. 3+ ODF storage nodes typical."),
        Flashcard(front="When use Local vs LVM Storage Operator?", back="<strong>Local Storage</strong>: static-provisioned PVs from attached block devices (NVMe). <strong>LVM Storage</strong>: dynamic PVCs from a single node\'s LVM thin pool. LVM is the SNO/edge path; Local is for bare-metal local-storage workloads on multi-node clusters."),
        Flashcard(front="OCP cloud CSI drivers shipped?", back="vSphere CSI, AWS EBS CSI, Azure Disk + File CSI, GCP PD CSI. Auto-installed based on cluster platform. Default StorageClass uses WaitForFirstConsumer."),
        Flashcard(front="RWX storage options on OCP?", back="ODF CephFS (multi-zone, integrated), Azure Files (SMB/NFS managed), NFS via external NFS server + nfs-csi-driver, EFS CSI on AWS."),
        Flashcard(front="What is OADP?", back="<strong>OpenShift APIs for Data Protection</strong> — Velero-based managed backup integrated with OCP. DataProtectionApplication + Backup + Restore CRs. S3/Blob/GCS/NooBaa backup destinations."),
        Flashcard(front="VolumeAttributesClass — what does it do?", back="K8s GA feature for live performance-tier change on running PVCs without remount. With ODF: change Ceph storage-class quality params; with cloud CSI: provider-specific (e.g., AWS gp3 IOPS retier)."),
        Flashcard(front="Where should the internal container registry storage live?", back="For prod: object storage backend (NooBaa, AWS S3, Azure Blob, GCS) — survives Pod migration across zones. PVC-backed (EBS/Azure Disk/GCE PD) is single-zone-pinned and breaks on cross-zone Pod migration."),
        Flashcard(front="Why plan Prometheus storage carefully?", back="Prometheus stores TSDB in PVCs. Default 15-day retention. <em>Don\'t share failure domain with workloads it monitors</em> — single-zone failure silences alerts about the failure. Use Thanos to ship to long-term S3 for cross-region resilience."),
    ],
    quizzes=[
        Quiz(prompt="A bank installs OCP on bare metal needing RWX + block + object + S3 + DR. Walk through the storage architecture.",
            answer="(1) Install <strong>ODF</strong> on 4 dedicated worker nodes with attached storage. (2) ODF provides CephRBD (RWO block), CephFS (RWX), NooBaa S3 (object). (3) Default StorageClass uses CephRBD; explicit RWX StorageClass uses CephFS; container registry + Prometheus long-term storage use NooBaa S3 endpoint. (4) Install <strong>OADP</strong> Operator + DataProtectionApplication pointing to off-cluster S3 (a separate cluster, AWS S3, or NooBaa in DR region). Schedule nightly Backup CR. (5) Quarterly DR drill: restore into sibling cluster; verify."),
        Quiz(prompt="A team\'s Pod with PVC fails to mount cross-zone after MachineSet rebalances. Diagnostic + fix?",
            answer="(1) <code>kubectl describe pod</code>: AttachVolume failure, often \"target node does not match volume\'s zone.\" (2) <code>oc get pvc &lt;pvc&gt; -o yaml</code>: check <code>volume.kubernetes.io/selected-node</code> annotation + topology constraints. (3) Default StorageClass\'s <code>volumeBindingMode</code> = WaitForFirstConsumer prevents this for new PVCs; legacy PVCs may not have used WFC. (4) Fix paths: (a) Force the Pod back to the original zone via nodeSelector / topology-spread; (b) Migrate to Regional PD or ODF CephRBD (multi-zone); (c) Recreate PVC + restore from snapshot in the new zone. (5) Long-term: ensure all StorageClasses use WaitForFirstConsumer + plan for cross-zone resilience explicitly via app-level replication or multi-zone storage."),
        Quiz(prompt="The CTO walks in: \"ODF is expensive — why not just use AWS EBS for everything?\" Defend or pivot.",
            answer="\"<strong>It depends on the cluster shape and storage needs.</strong> AWS EBS works well for: cloud-only OCP, RWO workloads, single-zone tolerance. EBS doesn\'t cover: RWX (need Azure Files / EFS — different cost model), object storage (need separate S3 bucket + IAM), software-defined storage on bare-metal (no cloud LB to use). <strong>ODF wins when:</strong> (1) on-prem / hybrid where there\'s no cloud-block-storage equivalent; (2) need for RWX + object integrated; (3) want one operationally-supported platform vs assembling NFS server + S3 service + block storage; (4) data sovereignty / no-cloud-egress requirements. <strong>EBS wins when:</strong> AWS-native shop, all RWO workloads, ok with per-zone-pinned PVCs. <em>For our hybrid bare-metal + cloud workload mix, ODF is right; for an AWS-only shop, EBS + EFS + S3 is right.</em>\"",
            cyoa=True, cyoa_tag="how the platform engineer answered the CTO"),
    ],
    glossary=[
        GlossaryItem(name="ODF", definition="OpenShift Data Foundation. Ceph + NooBaa + Rook. Software-defined storage built into OCP."),
        GlossaryItem(name="Ceph (in ODF)", definition="Distributed block + filesystem storage. RBD (block) + CephFS (RWX shared FS)."),
        GlossaryItem(name="NooBaa", definition="Multi-cloud object storage gateway speaking S3 API. Backs to local Ceph or external clouds."),
        GlossaryItem(name="Rook", definition="K8s operator orchestrating Ceph (deployment, scaling, recovery)."),
        GlossaryItem(name="Local Storage Operator", definition="Static-provisioned PVs from attached block devices (e.g., NVMe). Multi-node bare-metal."),
        GlossaryItem(name="LVM Storage Operator (LVMS)", definition="Dynamic PVCs from single node\'s LVM thin pool. SNO + edge."),
        GlossaryItem(name="vSphere CSI / AWS EBS CSI / Azure Disk-File CSI / GCP PD CSI", definition="Per-cloud CSI drivers OCP auto-installs based on platform."),
        GlossaryItem(name="VolumeSnapshot", definition="K8s standard CRD for PV point-in-time snapshot. Supported across CSI drivers."),
        GlossaryItem(name="VolumeAttributesClass", definition="K8s GA — live performance-tier change without remount."),
        GlossaryItem(name="OADP", definition="OpenShift APIs for Data Protection. Velero-based backup integrated with OCP. DataProtectionApplication + Backup + Restore CRs."),
        GlossaryItem(name="WaitForFirstConsumer", definition="StorageClass binding mode delaying PV creation until Pod scheduling — ensures zone alignment."),
        GlossaryItem(name="Regional PD / multi-zone storage", definition="Storage replicated across zones (Regional PD on GCP, ODF Ceph multi-node, Azure Files ZRS)."),
    ],
    recap_lead='Five storage paths for OCP: ODF (multi-node SDS), Local + LVM Operators (SNO/edge), per-cloud CSI (cloud-native), RWX via CephFS / Azure Files / NFS / EFS, OADP for DR. Plan registry + monitoring storage at install.',
    recap_next='<strong>Next — O8: OpenShift Operations.</strong> ClusterVersion + update channels + EUS + CVO + cluster operators; MachineConfigPools, MachineSets, MachineHealthChecks; node maintenance; etcd backup; must-gather; Insights telemetry; disconnected updates; mirror registry; upgrade risk assessment.',
    architecture_svg='''<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OCP storage stack: ODF, Local/LVM, cloud CSI, RWX (CephFS/EFS), OADP backup.">
  <rect x="10" y="10" width="740" height="220" rx="12" fill="#FBF7F0" stroke="#5A6B81"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">OCP STORAGE · 5 PATHS + CSI BASELINE</text>
  <rect x="20" y="55" width="220" height="55" rx="6" fill="#3F4A5E"/>
  <text x="130" y="75" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Pod requests PVC</text>
  <text x="130" y="91" text-anchor="middle" font-size="9" fill="#FBF1D6" font-style="italic">storageClassName: X</text>
  <text x="130" y="103" text-anchor="middle" font-size="8" fill="#FBE8DC">access mode: RWO / RWX</text>
  <line x1="240" y1="83" x2="270" y2="83" stroke="#5A4F45" stroke-width="2" marker-end="url(#a7)"/>
  <defs><marker id="a7" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><polygon points="0 0, 10 5, 0 10" fill="#5A4F45"/></marker></defs>
  <rect x="270" y="55" width="220" height="55" rx="6" fill="#A04832"/>
  <text x="380" y="75" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">StorageClass + CSI driver</text>
  <text x="380" y="91" text-anchor="middle" font-size="9" fill="#FBF1D6" font-style="italic">provisioner per backend</text>
  <line x1="490" y1="83" x2="520" y2="83" stroke="#5A4F45" stroke-width="2" marker-end="url(#a7)"/>
  <rect x="520" y="55" width="220" height="55" rx="6" fill="#5A9F7A"/>
  <text x="630" y="75" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">PV + storage backend</text>
  <text x="630" y="91" text-anchor="middle" font-size="9" fill="#FBE8DC" font-style="italic">EBS / Disk / PD / NetApp / Ceph</text>
  <rect x="20" y="125" width="135" height="50" rx="6" fill="#5A6B81"/>
  <text x="87" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">ODF</text>
  <text x="87" y="160" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">multi-node SDS</text>
  <rect x="165" y="125" width="135" height="50" rx="6" fill="#FAC775"/>
  <text x="232" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">Local + LVM</text>
  <text x="232" y="160" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">SNO + edge</text>
  <rect x="310" y="125" width="135" height="50" rx="6" fill="#3878B5"/>
  <text x="377" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">cloud CSI</text>
  <text x="377" y="160" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">EBS / Disks / PD</text>
  <rect x="455" y="125" width="135" height="50" rx="6" fill="#5E4A8E"/>
  <text x="522" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">RWX volumes</text>
  <text x="522" y="160" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">CephFS / EFS / NFS</text>
  <rect x="600" y="125" width="140" height="50" rx="6" fill="#1F8A60"/>
  <text x="670" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">OADP</text>
  <text x="670" y="160" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">backup / restore</text>
  <rect x="20" y="185" width="720" height="40" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="205" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">VolumeSnapshot · CSI snapshots · resize · clone · expand · regional / zonal awareness</text>
  <text x="380" y="219" text-anchor="middle" font-size="9" fill="#5A4F45" font-style="italic">Plan registry + monitoring storage at install (Image Registry, Prometheus require persistent backends)</text>
</svg>''',
    architecture_caption='Pod requests PVC referencing a StorageClass; CSI driver provisions PV from the backend (cloud disk / Ceph / NetApp / NFS / Local). Five paths cover the stack: ODF for multi-node SDS, Local/LVM for SNO, cloud CSI for cloud-native, CephFS/EFS for RWX, OADP for backup.',
)
