"""K-AKS A4 — AKS Storage (Disks, Files, Blob, NetApp, Container Storage, Secrets Store CSI)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AKS storage CSI drivers and access modes.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">The Library — five storage backends</text>
  <rect x="50" y="60" width="130" height="120" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="115" y="82" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Azure Disks</text>
  <text x="115" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">RWO block</text>
  <text x="115" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">Premium SSD v2</text>
  <text x="115" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">Ultra Disk</text>
  <text x="115" y="150" text-anchor="middle" font-size="8" fill="#FFFFFF">VolumeAttributesClass</text>
  <text x="115" y="165" text-anchor="middle" font-size="8" fill="#FFFFFF">live tier change</text>
  <rect x="194" y="60" width="130" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="259" y="82" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Azure Files</text>
  <text x="259" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">RWX shared FS</text>
  <text x="259" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">SMB or NFS</text>
  <text x="259" y="135" text-anchor="middle" font-size="8" fill="#FFFFFF">multi-AZ via ZRS</text>
  <rect x="338" y="60" width="130" height="120" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="403" y="82" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Azure NetApp</text>
  <text x="403" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Files</text>
  <text x="403" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">SAP HANA · DBs</text>
  <text x="403" y="135" text-anchor="middle" font-size="8" fill="#FFFFFF">extreme low-latency</text>
  <rect x="482" y="60" width="130" height="120" rx="10" fill="#E8B547" stroke="#3F4A5E"/>
  <text x="547" y="82" text-anchor="middle" font-size="11" font-weight="700" fill="#5A4F45">Azure Blob</text>
  <text x="547" y="100" text-anchor="middle" font-size="9" fill="#5A4F45">BlobFuse2 CSI</text>
  <text x="547" y="115" text-anchor="middle" font-size="9" fill="#5A4F45">object as FS</text>
  <text x="547" y="135" text-anchor="middle" font-size="8" fill="#5A4F45">cheap · ML datasets</text>
  <rect x="626" y="60" width="84" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="668" y="82" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Container</text>
  <text x="668" y="98" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Storage</text>
  <text x="668" y="115" text-anchor="middle" font-size="9" fill="#FBF1D6">local NVMe</text>
  <text x="668" y="130" text-anchor="middle" font-size="9" fill="#FBF1D6">+ ANF + Disks</text>
  <text x="668" y="155" text-anchor="middle" font-size="8" fill="#FBF1D6">unified plane</text>
</svg>"""


LESSON = LessonSpec(
    num="04",
    title_short="AKS storage",
    title_full="A4 · AKS Storage (Disks, Files, NetApp, Blob, Container Storage)",
    title_html="K-AKS A4 · AKS Storage",
    module_eyebrow="Module A4 · the Library — where data lives",
    hero_sub_html='Five storage backends as managed CSI drivers. <strong>Azure Disks CSI</strong> for RWO block (Premium SSD v2 default; Ultra Disk for extreme IOPS; <strong>VolumeAttributesClass</strong> for live tier changes). <strong>Azure Files CSI</strong> for RWX (SMB / NFS). <strong>Azure NetApp Files</strong> for low-latency DBs / SAP HANA. <strong>Azure Blob CSI</strong> via BlobFuse2 for object-as-filesystem. <strong>Azure Container Storage</strong> as the unified plane. Plus <strong>Secrets Store CSI</strong> for Key Vault.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"PostgreSQL Pod stuck Pending — disk attach failed.\"</em> Pod was scheduled on a node in <code>eastus-3</code>; PVC was bound to a Premium SSD in <code>eastus-1</code> (single-zone). Cross-AZ disk attach is not supported. The disk you provisioned for high-availability — isn\'t available where the Pod ended up. You realise <em>you didn\'t set <code>volumeBindingMode: WaitForFirstConsumer</code> on the StorageClass</em>. Today\'s lesson: pick the right storage backend, set zone-awareness right.",
    stamp_html="<strong>Default to Azure Disks CSI (Premium SSD v2) for RWO with WaitForFirstConsumer; Azure Files for RWX; ANF for low-latency DBs; Blob for cheap object access. Use VolumeAttributesClass to resize/retier without remount; Secrets Store CSI for Key Vault.</strong>",
    district_pin="kc-wing04",
    district_label="The Library",
    sections=[
        Section(
            eyebrow="Section 1.1 · Azure Disks CSI",
            h2="Azure Disks CSI — the RWO default",
            body_html="""    <p><strong>Azure Disks CSI driver</strong> is the default for ReadWriteOnce (RWO) Persistent Volumes. Backed by Azure Managed Disks. Tiers in increasing performance/cost: <strong>Standard HDD</strong> (cheapest), <strong>Standard SSD</strong>, <strong>Premium SSD</strong>, <strong>Premium SSD v2</strong> (current recommended default — independent IOPS / throughput tuning), <strong>Ultra Disk</strong> (sub-millisecond, extreme IOPS for SAP HANA / huge OLTP).</p>
    <p><strong>Critical detail — zone affinity:</strong> a Premium SSD lives in one availability zone. A Pod can only mount a disk if the Pod is scheduled in the same zone. The <strong>StorageClass</strong> shipped with AKS sets <code>volumeBindingMode: WaitForFirstConsumer</code> — disk provisioning is delayed until the Pod is scheduled, then the disk is provisioned in that Pod\'s zone. <em>If you create a custom StorageClass without this setting, you re-introduce the cross-AZ-attach failure.</em></p>
    <p><strong>VolumeAttributesClass</strong> (GA) is the K8s-native way to change a PV\'s performance tier <em>without remount</em>. Premium SSD v2: change IOPS / throughput on a running PV via a <code>VolumeAttributesClass</code> reference. Ultra Disk: same. Workload doesn\'t restart.</p>
    <p><strong>ZRS (Zone-Redundant Storage):</strong> for Standard SSD and Premium SSD, Azure offers a ZRS variant that replicates synchronously across three zones — disk can attach to a Pod in any zone of the region. <em>Higher latency than LRS, but solves cross-AZ attach for stateful workloads that need it.</em></p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Azure Files CSI + ANF",
            h2="Azure Files CSI + Azure NetApp Files",
            body_html="""    <p><strong>Azure Files CSI</strong> for ReadWriteMany (RWX). Backed by Azure Files. Two protocols:</p>
    <ul>
      <li><strong>SMB</strong> — works on Linux + Windows nodes. Most common.</li>
      <li><strong>NFS v4.1</strong> — Linux only; better for POSIX semantics. Premium tier required for NFS.</li>
    </ul>
    <p>Use cases: shared writable storage across multiple Pods (CMS file uploads, shared logs, ML datasets being written by multiple workers). Premium tier for performance; ZRS for multi-AZ resilience. <em>Avoid for high-IOPS DB workloads — Disks or ANF are far faster.</em></p>
    <p><strong>Azure NetApp Files (ANF)</strong> — managed NetApp ONTAP service, exposed to AKS via the ANF CSI driver. Tier choices: Standard / Premium / Ultra (in MiB/s per TiB). For SAP HANA, large Postgres / Oracle / SQL Server, low-latency DB workloads needing &lt; 1ms. Higher base cost than Files but in a different performance class.</p>
    <p><strong>Azure Container Storage</strong> — unified data plane that exposes <em>local NVMe (ephemeral disks on the node)</em> as Persistent Volumes alongside Disks and ANF. Use case: high-IOPS stateful workloads where you can tolerate node-loss replication done at the application layer (Cassandra, Elasticsearch, Kafka). Replaces the older OpenEBS / local-PV setups.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Blob CSI + Secrets Store CSI",
            h2="Blob CSI (BlobFuse2) + Secrets Store CSI",
            body_html="""    <p><strong>Azure Blob CSI</strong> mounts an Azure Blob container as a filesystem inside a Pod, via <strong>BlobFuse2</strong>. Two access modes: <em>BlobFuse</em> (caching, POSIX-ish) and <em>NFS 3.0</em> (for storage accounts that support it). Use cases: huge ML training datasets (TBs of read-only inputs cheaply held in Blob); image/asset libraries; cheap append-only logs. <em>Performance is not Disk-class</em> — fine for sequential reads, not for transactional DBs.</p>
    <p><strong>Secrets Store CSI driver + Azure Key Vault provider</strong>: declares secrets/keys/certs to fetch via a <code>SecretProviderClass</code>; mounts them as files in Pods. Authenticates to Key Vault via <strong>Workload Identity</strong>. Optional: sync to a K8s Secret. Auto-rotation polls Key Vault and updates the volume; the Pod sees fresh values via volume reload (or rolling restart). <em>The clean way to consume Key Vault secrets in AKS — no app code changes.</em></p>"""
        ),
        Section(
            eyebrow="Section 1.4 · snapshots, expansion, topology",
            h2="Snapshots, expansion, ZRS, topology-aware scheduling",
            body_html="""    <p><strong>VolumeSnapshot</strong> (K8s standard CRD) backed by Azure Managed Disk snapshots — point-in-time backup of a PV. Restore by creating a new PVC with <code>dataSource</code> pointing at the snapshot. Cross-region restore via storage account replication.</p>
    <p><strong>Volume expansion</strong> — Azure Disks CSI supports online expansion. Edit the PVC\'s <code>spec.resources.requests.storage</code> upward; the disk grows; the filesystem grows. <em>Not all disk types support online expansion in all sizes</em> — check tier limits.</p>
    <p><strong>ZRS variants</strong> — for stateful workloads needing AZ resilience without app-level replication, switch the StorageClass to a ZRS-backed disk type. Trade-off: slightly higher latency.</p>
    <p><strong>Topology-aware scheduling:</strong> StorageClass <code>allowedTopologies</code> can constrain disks to specific zones (e.g. force all DB disks into <code>eastus-1</code> to align with a hot/warm DR pattern). Combined with Pod nodeSelector / topology spread constraints to keep workloads + storage co-located.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A Pod with a Premium SSD PVC keeps failing to start in a multi-zone cluster. What\'s the most likely fix?",
            options=[
                ("Switch to Standard HDD.", False),
                ("Use a StorageClass with <code>volumeBindingMode: WaitForFirstConsumer</code> so the disk is provisioned in the Pod\'s zone — or use a ZRS-backed StorageClass.", True),
                ("Increase replica count.", False),
            ],
            feedback="Single-zone disks can\'t cross-AZ-attach. WaitForFirstConsumer aligns disk creation with Pod scheduling; ZRS replicates the disk across zones.",
        ),
    },
    before_after_before='<p>Pre-CSI AKS used in-tree volume drivers — limited features, slow innovation cycle, no online resize, no snapshot CRD, no VolumeAttributesClass. RWX needed third-party Helm-installed nfs-server-provisioner with manual storage account wiring. Secret consumption from Key Vault required custom init-containers calling the Key Vault REST API and writing files. Stateful workloads on multi-AZ clusters routinely failed cross-AZ attach because StorageClasses lacked <code>WaitForFirstConsumer</code>.</p>',
    before_after_after='<p>Modern AKS ships <strong>five managed CSI drivers</strong> (Disks, Files, Blob, ANF, Container Storage) with <strong>VolumeSnapshot</strong>, <strong>online expansion</strong>, and <strong>VolumeAttributesClass</strong> (live tier change without remount). RWX is one PVC. Key Vault secrets mount as files via the Secrets Store CSI driver, authenticated by Workload Identity. <code>WaitForFirstConsumer</code> is the default. Stateful workloads work cleanly across zones with ZRS or topology-aware scheduling.</p>',
    before_after_caption='<p class="ba-caption"><em>Storage in AKS is now declarative and survivable. The hard part shifted from "how do I attach a disk?" to "what backend matches my workload?"</em></p>',
    analogy_intro_html='''<p>The <strong>Library</strong> is K-Campus\'s storage building. Five wings hold different kinds of books, each suited to a different purpose.</p>
    <p><strong>Wing A — Personal lockers</strong> (Azure Disks): one student per locker, fast, locked. The locker lives in a specific corner of the building (an availability zone). If you want a multi-corner locker, use the ZRS lockers — slightly slower but accessible from any corner. The Library has a special trick: you can swap out the lock to upgrade the locker speed without taking your books out (<strong>VolumeAttributesClass</strong>).</p>
    <p><strong>Wing B — Reading rooms</strong> (Azure Files): multiple students share the same desk and the same papers. Read-write-many. Use SMB (works for everyone, even Windows visitors) or NFS (Linux scholars only).</p>
    <p><strong>Wing C — Reference rare-books</strong> (Azure NetApp Files): super-fast access for the most demanding scholars (SAP HANA, big databases). Pricier librarians, but they hand you the book in under a millisecond.</p>
    <p><strong>Wing D — Warehouse</strong> (Azure Blob via BlobFuse2): cheap stacks holding 10 TB of training data; you fetch a chapter at a time. Not for transactional reads.</p>
    <p><strong>Wing E — The vault</strong> (Secrets Store CSI + Key Vault): no books here, only sealed envelopes containing keys, certs, secrets. The Library Concierge (Workload Identity) opens envelopes for authorised Pods only.</p>''',
    translation_rows=[
        ("Personal locker", "Azure Disks CSI — RWO Persistent Volume"),
        ("Locker that lives in a specific corner", "Single-zone Premium SSD"),
        ("Multi-corner locker (slightly slower)", "ZRS-backed Disk"),
        ("Swap-out lock without removing books", "VolumeAttributesClass — live tier change"),
        ("Shared reading room desk", "Azure Files CSI — RWX (SMB or NFS)"),
        ("Rare-books wing", "Azure NetApp Files — sub-ms latency"),
        ("Warehouse stacks", "Azure Blob CSI via BlobFuse2"),
        ("The vault of sealed envelopes", "Secrets Store CSI + Azure Key Vault"),
        ("Library Concierge", "Workload Identity — authorises secret retrieval"),
        ("\"Wait for the student before issuing the locker\"", "<code>volumeBindingMode: WaitForFirstConsumer</code>"),
        ("Photocopying a chapter", "VolumeSnapshot CRD"),
        ("Adding shelves to an existing locker", "Online volume expansion"),
        ("Local NVMe drawer at every desk", "Azure Container Storage — local NVMe as PVs"),
    ],
    analogy_stops="A library has fixed wings; CSI drivers can be added or upgraded without rebuilding the cluster. Real CSI also has driver-version compatibility windows the metaphor doesn\'t capture.",
    eli5="A big library with five wings. One wing has lockers for one student. Another has shared desks for groups. One has fast lookups for important books. One has cheap stacks for huge collections. One has a vault for secret keys. You pick the wing that matches what your work needs.",
    eli10="AKS storage = five managed CSI drivers. <strong>Disks</strong> for RWO (default Premium SSD v2 with WaitForFirstConsumer for zone-correct provisioning; VolumeAttributesClass for live tier changes; ZRS for multi-AZ). <strong>Files</strong> for RWX (SMB / NFS). <strong>NetApp Files</strong> for sub-ms DB latency. <strong>Blob</strong> via BlobFuse2 for huge object datasets. <strong>Container Storage</strong> for local NVMe-as-PV. Plus <strong>Secrets Store CSI</strong> with Key Vault provider, authed by Workload Identity. VolumeSnapshot CRD for backup; online expansion supported.",
    scenarios=[
        Scenario(
            name="Postgres on AKS — single-zone Disks + ZRS for DR",
            body="A Postgres workload runs as a 3-replica StatefulSet. Each replica is pinned to a specific zone (anti-affinity), each with a Premium SSD v2 in that same zone. Cross-zone replication is handled by Postgres streaming replication. For DR, weekly VolumeSnapshots cross-region replicate via storage account GRS to a paired region. <em>Tested DR restore: full Postgres rebuild from snapshot in 18 minutes.</em>",
        ),
        Scenario(
            name="ML pipeline — Blob CSI for 200 TB of training data",
            body="An ML team needs read-only access to 200 TB of image datasets across hundreds of training Pods. Storing this on Premium SSD = $50K/month. Storing on Blob (Cool tier) = $2K/month. They mount the container via Azure Blob CSI (BlobFuse2 caching mode); training I/O is sequential reads — perfect Blob workload. <em>96% cost reduction; same throughput thanks to BlobFuse2 read cache + parallel readers.</em>",
        ),
        Scenario(
            name="SaaS — RWX shared logs via Azure Files SMB",
            body="A SaaS has 12 microservices that all need to write to a shared rolling-log directory consumed by Filebeat. Single Azure Files share, mounted RWX as SMB by all 12 Deployments. Premium tier for IOPS. ZRS for AZ resilience. <em>One PVC, twelve Pods writing concurrently, no NFS server to operate.</em>",
        ),
        Scenario(
            name="Bank — Key Vault secrets via Secrets Store CSI",
            body="A bank rotates DB credentials every 24 hours via Key Vault\'s rotation policy. Pods mount the secret via Secrets Store CSI driver with the Azure Key Vault provider, Workload-Identity-authenticated. Driver\'s rotation poller pulls Key Vault every 2 minutes. App watches the file and reloads its DB pool when the file changes — <em>zero restart, zero downtime, zero secret in Pod env.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"My Premium SSD will reattach to any Pod regardless of zone.\"",
            truth="Premium SSDs are single-zone resources. A disk created in <code>eastus-1</code> can only attach to a Pod scheduled in <code>eastus-1</code>. Without <code>WaitForFirstConsumer</code> + topology-aware scheduling, the kube-scheduler will happily place a Pod in <code>eastus-2</code> and the attach will fail. Use the default StorageClass (which has WaitForFirstConsumer) or a ZRS variant.",
        ),
        Misconception(
            myth="\"I should resize disks by recreating the PVC.\"",
            truth="Azure Disks CSI supports <strong>online volume expansion</strong>. Edit the PVC\'s <code>spec.resources.requests.storage</code> upward; the underlying disk grows; the filesystem grows. No remount, no Pod restart needed. Recreating the PVC throws away the data.",
        ),
        Misconception(
            myth="\"VolumeAttributesClass and StorageClass are the same.\"",
            truth="<strong>StorageClass</strong> defines how PVs get <em>provisioned</em>. <strong>VolumeAttributesClass</strong> (GA) defines how an <em>existing</em> PV\'s attributes (IOPS, throughput) can be modified after creation, without remount. They\'re complementary — use VAC to retier a Premium SSD v2 from 3000 IOPS to 16000 IOPS without losing data.",
        ),
    ],
    flashcards=[
        Flashcard(front="Five AKS managed CSI drivers?", back="<strong>Azure Disks</strong> (RWO block), <strong>Azure Files</strong> (RWX SMB/NFS), <strong>Azure NetApp Files</strong> (low-latency DBs / SAP HANA), <strong>Azure Blob</strong> (BlobFuse2 for object-as-FS), <strong>Azure Container Storage</strong> (local NVMe + unified plane). Plus <strong>Secrets Store CSI</strong> (Key Vault)."),
        Flashcard(front="Why is <code>WaitForFirstConsumer</code> critical for multi-AZ AKS?", back="Single-zone disks can\'t cross-AZ-attach. WaitForFirstConsumer delays disk provisioning until the Pod is scheduled, then provisions the disk in that Pod\'s zone. Without it, the scheduler may place the Pod in zone A but the disk got provisioned in zone B = attach failure."),
        Flashcard(front="What does VolumeAttributesClass do?", back="K8s-native (GA) way to change a PV\'s performance attributes (IOPS, throughput) on a running workload — no remount. Useful for Premium SSD v2 / Ultra Disk where you tune IOPS independently. Reference a VAC from the PVC."),
        Flashcard(front="When should you use ZRS-backed disks?", back="When you need <em>cross-zone disk attach</em> for stateful workloads without app-level replication — single-region multi-AZ resilience. Trade-off: slightly higher latency than LRS. Available for Standard SSD and Premium SSD."),
        Flashcard(front="How does Secrets Store CSI consume Key Vault?", back="A <code>SecretProviderClass</code> declares which Key Vault secrets/keys/certs to fetch. The driver authenticates via <strong>Workload Identity</strong>, pulls them from Key Vault, mounts them as files in the Pod. Optional sync to K8s Secret. Auto-rotation poller refreshes the volume."),
        Flashcard(front="When should you use Azure NetApp Files?", back="Sub-millisecond latency, high IOPS workloads — SAP HANA, large transactional DBs (Oracle / Postgres / SQL Server with extreme requirements). Higher base cost than Files; different performance class."),
        Flashcard(front="Azure Container Storage — what problem does it solve?", back="Unified data plane — exposes <em>local NVMe ephemeral disks</em> on nodes as Persistent Volumes alongside Disks and ANF. For workloads with app-layer replication (Cassandra, Elasticsearch, Kafka) where local NVMe IOPS matters and you tolerate node-loss replication."),
        Flashcard(front="Two Azure Files protocols and when to pick each?", back="<strong>SMB</strong> — works on Linux + Windows; default. <strong>NFS v4.1</strong> — Linux only; Premium tier required; better POSIX semantics; pick when apps need POSIX file locking or fork()-style behaviours."),
    ],
    quizzes=[
        Quiz(
            prompt="A team migrates a stateful workload to a multi-zone AKS cluster. They wrote a custom StorageClass without specifying <code>volumeBindingMode</code>. Pods now intermittently fail to start. What\'s happening?",
            answer="Default volumeBindingMode is <code>Immediate</code> — disks are provisioned as soon as the PVC is created, in whichever zone the storage controller picks. The kube-scheduler then schedules the Pod independently — and may place it in a different zone. Cross-zone attach is unsupported for single-zone disks. Fix: edit the StorageClass to <code>volumeBindingMode: WaitForFirstConsumer</code>; new PVCs will provision in the correct zone. (Existing mis-zoned PVCs need recreating in the right zone or migration to ZRS.)",
        ),
        Quiz(
            prompt="A Postgres Premium SSD v2 is provisioned at 3000 IOPS / 125 MiB/s. Holiday traffic 10×; the team needs 16K IOPS. What\'s the safe path that doesn\'t require Pod restart?",
            answer="Create a <strong>VolumeAttributesClass</strong> with the new IOPS / throughput targets. Reference it from the PVC: <code>spec.volumeAttributesClassName: postgres-high-iops</code>. The Azure CSI driver applies the new attributes to the underlying Premium SSD v2 online — no detach, no remount, no Pod restart. Postgres continues serving traffic; new IOPS available within seconds.",
        ),
        Quiz(
            prompt="The team mounts secrets via env vars from a K8s Secret. Key Vault rotates the DB password nightly. What\'s the gap, and how does Secrets Store CSI close it?",
            answer="K8s Secrets backed by env vars are evaluated at Pod start — they don\'t reflect post-start changes to the underlying Secret. So if Key Vault rotates the password and the team\'s controller updates the K8s Secret, the running Pod still has the old password as an env var until restart. <strong>Secrets Store CSI driver</strong> mounts the secret as a file in the Pod\'s filesystem, with the Azure Key Vault provider auto-rotation poller refreshing the file from Key Vault on a schedule. The app watches the file (e.g. via <code>fsnotify</code>) and reloads its DB pool with the new password — no Pod restart.",
            cyoa=True,
            cyoa_tag="why secrets-as-env-vars is a footgun",
        ),
    ],
    glossary=[
        GlossaryItem(name="Azure Disks CSI", definition="Default RWO storage driver. Backed by Azure Managed Disks (Standard / Premium / Premium v2 / Ultra)."),
        GlossaryItem(name="Premium SSD v2", definition="Recommended general-purpose Disk tier — independent IOPS / throughput tuning, finer-grained pricing."),
        GlossaryItem(name="Ultra Disk", definition="Highest-performance Disk tier — sub-millisecond latency, extreme IOPS for SAP HANA / massive OLTP."),
        GlossaryItem(name="VolumeAttributesClass", definition="K8s GA feature — change a PV\'s performance attributes (IOPS / throughput) without remount."),
        GlossaryItem(name="ZRS (Zone-Redundant Storage)", definition="Disk variant replicated synchronously across three AZs in a region. Enables cross-zone attach."),
        GlossaryItem(name="Azure Files CSI", definition="RWX storage driver via Azure Files. SMB (Linux+Windows) or NFS v4.1 (Linux only, Premium tier)."),
        GlossaryItem(name="Azure NetApp Files (ANF)", definition="Managed NetApp ONTAP — sub-ms latency for SAP HANA, large DBs."),
        GlossaryItem(name="Azure Blob CSI / BlobFuse2", definition="Mount Azure Blob containers as filesystems. Cheap object storage for ML datasets, asset libraries."),
        GlossaryItem(name="Azure Container Storage", definition="Unified storage plane — exposes local NVMe + Disks + ANF as PVs through one API."),
        GlossaryItem(name="Secrets Store CSI driver", definition="Mount external secret stores (Key Vault, etc.) as Pod files. Auto-rotation polls Key Vault."),
        GlossaryItem(name="WaitForFirstConsumer", definition="StorageClass binding mode that delays PV provisioning until the Pod is scheduled — ensures zone alignment."),
        GlossaryItem(name="VolumeSnapshot", definition="K8s standard CRD for point-in-time PV backup. Backed by Azure Managed Disk snapshots."),
    ],
    recap_lead='Five storage backends mapped to use cases; VolumeAttributesClass for live tier change; Secrets Store CSI for Key Vault. Multi-AZ stateful is solved (WaitForFirstConsumer or ZRS).',
    recap_next='<strong>Next — A5: AKS Scaling.</strong> Cluster Autoscaler (default), Karpenter for AKS / Node Auto Provisioning (NAP), KEDA, Spot pools, GPU, Windows, ARM (Cobalt, Ampere Altra), Confidential Computing nodes (DCasv5/ECasv5), PDB-aware maintenance, multi-zone scaling.',
)
