from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Customs Warehouse loading dock cross-section: a CSI driver truck parked at the dock, a snapshot photographer copying a locker, and a quality-of-service dial showing slow/medium/fast lanes.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">CUSTOMS WAREHOUSE · LOADING DOCK</text>
  <!-- CSI driver truck -->
  <g transform="translate(40,55)">
    <rect x="0" y="35" width="92" height="46" rx="4" fill="#3F4A5E" stroke="#2A2520" stroke-width="1.5"/>
    <rect x="92" y="48" width="34" height="33" rx="3" fill="#5A9F7A" stroke="#2A2520" stroke-width="1.5"/>
    <rect x="98" y="54" width="22" height="14" rx="1.5" fill="#FBF7F0"/>
    <circle cx="20" cy="86" r="9" fill="#1B1814" stroke="#2A2520" stroke-width="1.4"/>
    <circle cx="20" cy="86" r="3" fill="#9D9389"/>
    <circle cx="100" cy="86" r="9" fill="#1B1814" stroke="#2A2520" stroke-width="1.4"/>
    <circle cx="100" cy="86" r="3" fill="#9D9389"/>
    <text x="46" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF7F0">CSI driver</text>
    <text x="46" y="73" text-anchor="middle" font-size="7" fill="#FBF7F0" font-style="italic">licensed plug-in</text>
    <text x="63" y="115" text-anchor="middle" font-size="9" fill="#3F4A5E" font-style="italic">brings the lockers</text>
  </g>
  <!-- Snapshot photographer -->
  <g transform="translate(190,60)">
    <circle cx="30" cy="20" r="14" fill="#FBF1D6" stroke="#2A2520" stroke-width="1.4"/>
    <circle cx="26" cy="18" r="1.4" fill="#2A2520"/><circle cx="34" cy="18" r="1.4" fill="#2A2520"/>
    <path d="M 26 24 L 34 24" stroke="#2A2520" stroke-width="1.2" stroke-linecap="round"/>
    <path d="M 18 34 Q 18 70 24 90 L 36 90 Q 42 70 42 34 Z" fill="#A04832"/>
    <!-- camera -->
    <rect x="40" y="46" width="34" height="22" rx="2" fill="#2A2520"/>
    <circle cx="57" cy="57" r="7" fill="#3F4A5E" stroke="#9D9389" stroke-width="1"/>
    <circle cx="57" cy="57" r="3" fill="#FBF1D6"/>
    <text x="40" y="115" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">snapshot</text>
    <text x="40" y="128" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">point-in-time copy</text>
  </g>
  <!-- QoS dial -->
  <g transform="translate(330,50)">
    <text x="60" y="14" text-anchor="middle" font-size="9" fill="#5A4F45" font-weight="700">QUALITY DIAL · VolumeAttributesClass</text>
    <circle cx="60" cy="60" r="42" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <circle cx="60" cy="60" r="38" fill="none" stroke="#E8DDC8" stroke-width="1"/>
    <!-- arc segments -->
    <path d="M 28 80 A 38 38 0 0 1 60 22" fill="none" stroke="#5A9F7A" stroke-width="6" stroke-linecap="round"/>
    <path d="M 60 22 A 38 38 0 0 1 92 80" fill="none" stroke="#E8B547" stroke-width="6" stroke-linecap="round"/>
    <path d="M 28 80 A 38 38 0 0 1 92 80" fill="none" stroke="#D97757" stroke-width="0" stroke-linecap="round"/>
    <text x="22" y="78" text-anchor="end" font-size="8" fill="#3D7857">slow</text>
    <text x="98" y="78" text-anchor="start" font-size="8" fill="#A04832">fast</text>
    <text x="60" y="20" text-anchor="middle" font-size="8" fill="#8B5A00">premium</text>
    <!-- needle -->
    <line x1="60" y1="60" x2="78" y2="36" stroke="#2A2520" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="60" cy="60" r="4" fill="#2A2520"/>
    <text x="60" y="118" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">re-tune live</text>
    <text x="60" y="131" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">no Pod restart</text>
  </g>
  <!-- Multi-attach drama -->
  <g transform="translate(490,55)">
    <rect width="160" height="90" rx="6" fill="#FBE8DC" stroke="#A04832" stroke-width="1.5"/>
    <text x="80" y="16" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">MULTI-ATTACH ALERT</text>
    <rect x="20" y="28" width="40" height="50" rx="3" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.2"/>
    <text x="40" y="55" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">PV</text>
    <line x1="60" y1="40" x2="100" y2="40" stroke="#A04832" stroke-width="1.5" stroke-dasharray="3,2"/>
    <line x1="60" y1="60" x2="100" y2="60" stroke="#A04832" stroke-width="1.5" stroke-dasharray="3,2"/>
    <text x="120" y="34" font-size="8" fill="#A04832">node-A ✓</text>
    <text x="120" y="56" font-size="8" fill="#A04832">node-B ✗</text>
    <text x="80" y="83" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">RWO can only attach to one node</text>
  </g>
  <text x="340" y="200" text-anchor="middle" font-size="11" fill="#3F4A5E" font-style="italic">Behind the dock: who actually gives the locker to the truck — and what tricks they can pull.</text>
</svg>"""

LESSON = LessonSpec(
    num="19",
    title_short="storage Pt 2",
    title_full="Storage Part 2 · CSI, Snapshots, Cloning, VolumeAttributesClass",
    title_html="Lesson 19 — Storage Part 2: CSI, Snapshots, VolumeAttributesClass · K-COM",
    module_eyebrow="Module 9 · Lesson 19 · the storage stack under the abstraction",
    hero_sub_html='Behind every PVC there is a <strong>CSI driver</strong> doing the actual attach/format/mount. Once the driver is in place, K8s gets snapshots, cloning, expansion, and (new in 1.34 GA) <strong>live performance changes</strong> via VolumeAttributesClass.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="A storage performance regression hits production. The team's PVCs are all <code>gp3</code> with 3000 IOPS. Marketing's promo just landed; queue depth is climbing; the database needs 8000 IOPS for the next four hours. The <em>old</em> playbook: detach the disk, snapshot it, recreate it with new IOPS, restore from snapshot, hope nothing's lost. Two hours of downtime, weekend gone. The <em>new</em> playbook (K8s 1.34 GA): change one label on the PVC. The CSI driver re-tunes the live disk. Zero downtime.",
    stamp_html="Behind every PVC sits a <strong>CSI driver</strong> — a vendor-supplied plug-in that handles the actual disk plumbing. Once you have a CSI driver you get <strong>snapshots</strong> (point-in-time copies), <strong>cloning</strong> (new PVC from existing PVC or snapshot), <strong>expansion</strong> (grow the disk), and <strong>VolumeAttributesClass</strong> (re-tune performance live, GA in 1.34).",
    district_pin="kt-pin09",
    district_label="Customs Warehouse — Loading Dock",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What CSI actually is",
            body_html="""    <p>Lesson 18 ended with "the StorageClass calls a provisioner." This lesson is about that provisioner. The <strong>Container Storage Interface (CSI)</strong> is a gRPC API specification — a contract between Kubernetes (the orchestrator) and the storage system (EBS, Ceph, NFS, vSAN, anything). Vendors write CSI drivers that implement the spec; K8s talks to them through standard sidecar containers (<code>external-provisioner</code>, <code>external-attacher</code>, <code>external-snapshotter</code>, <code>external-resizer</code>).</p>
    <p>The CSI driver runs in the cluster as a Deployment (the controller-side, one replica) plus a DaemonSet (the node-side, one Pod per node). The controller-side handles <em>create / delete / attach / detach / snapshot</em> calls — the cluster-wide stuff. The node-side handles <em>mount / unmount / format</em> — the per-node stuff that has to happen on the actual machine where the Pod runs. Every storage operation from the K8s API ends up as a gRPC call into one of those two CSI Pods.</p>
    <p>Why this matters: anything you've ever heard described as "Kubernetes storage" — snapshots, clones, expansion, attribute changes — is actually a CSI driver feature K8s exposes through a standard API. If your driver doesn't implement a feature, K8s can't expose it. Always check your driver's capability list before promising features to a team.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The four CSI capabilities you'll use",
            h2="Snapshots, clones, expansion, attribute changes",
            body_html="""    <div class="role-grid">
      <div class="role r1">
        <span class="role-icon">📸</span>
        <h3 class="role-name">VolumeSnapshot</h3>
        <p class="role-tag">point-in-time copy</p>
        <p class="role-desc">Asks the CSI driver to take an instant snapshot of a PVC. The snapshot is a separate object (<code>VolumeSnapshot</code> + <code>VolumeSnapshotContent</code>) and survives PVC deletion. You can restore by creating a new PVC with <code>dataSource: VolumeSnapshot</code>.</p>
        <p class="role-who">Use for: backups, pre-migration safety nets, dev environments hydrated from prod.</p>
      </div>
      <div class="role r2">
        <span class="role-icon">🧬</span>
        <h3 class="role-name">PVC cloning</h3>
        <p class="role-tag">PVC from PVC</p>
        <p class="role-desc">Create a new PVC by setting <code>dataSource: existing-PVC</code>. The CSI driver does a fast-path copy (typically a copy-on-write at the storage layer, much faster than a manual <code>cp</code>). Both PVCs must be in the same namespace and the same StorageClass.</p>
        <p class="role-who">Use for: dev clones of prod data, testing schema migrations on a copy.</p>
      </div>
      <div class="role r3">
        <span class="role-icon">📈</span>
        <h3 class="role-name">Volume expansion</h3>
        <p class="role-tag">grow without downtime</p>
        <p class="role-desc">Edit the PVC's <code>spec.resources.requests.storage</code> upward. If the StorageClass has <code>allowVolumeExpansion: true</code> and the CSI driver supports it, the disk and filesystem grow online. Most modern drivers (EBS, GCE PD, Azure Disk, Ceph RBD, Longhorn) support this.</p>
        <p class="role-who">Use for: an alert says you're at 90% disk; bump the PVC.</p>
      </div>
      <div class="role r4">
        <span class="role-icon">🎚️</span>
        <h3 class="role-name">VolumeAttributesClass (NEW)</h3>
        <p class="role-tag">change perf live · GA 1.34</p>
        <p class="role-desc">A new object alongside StorageClass that lets you re-tune <em>performance attributes</em> (IOPS, throughput) on a live PVC by changing one label. The CSI driver re-modifies the underlying disk in place. No detach, no snapshot, no Pod restart.</p>
        <p class="role-who">Use for: temporary performance bursts; tier migrations; cost optimisation.</p>
      </div>
    </div>
    <p style="margin-top:18px">All four require the CSI driver to advertise the relevant capability. <code>kubectl get csidriver</code> tells you which features are available. <code>kubectl get csistoragecapacity</code> tells you how much capacity each topology has.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Stateful patterns",
            h2="StatefulSet + volumeClaimTemplates",
            body_html="""    <p>Most stateful workloads use a <strong>StatefulSet</strong> (covered in L16) with <code>volumeClaimTemplates</code>. Each replica gets its own PVC named after the Pod (<code>data-mysql-0</code>, <code>data-mysql-1</code>, …). Pods rescheduling brings the same disk back to the same Pod identity. PVCs are <em>not</em> deleted when the StatefulSet is deleted — that's intentional, so you can rebuild a StatefulSet without losing data.</p>
    <p>Two patterns built on this:</p>
    <ul>
      <li><strong>Backup + restore via VolumeSnapshot.</strong> Snapshot every Pod's PVC nightly. To restore one replica, delete its PVC, create a new one with <code>dataSource</code> pointing at the snapshot. The StatefulSet's controller binds the new PVC by name as if nothing happened.</li>
      <li><strong>Test environments via cloning.</strong> Clone a prod PVC into a dev namespace (or snapshot then restore), and you've got a realistic test database in seconds, not hours of <code>pg_dump</code>.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The kubelet doesn't talk to your storage system directly. It speaks the Mount Service Interface (MSI) over a Unix socket to the node-side CSI driver Pod, which in turn invokes the cloud or storage SDK. This means the actual mount operation happens inside a privileged container on the node — that's why CSI drivers ship with a privileged DaemonSet. If you've ever seen a CSI driver hang and Pods stuck in <code>ContainerCreating</code>, that's typically the node-side Pod failing to complete a mount.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A team wants to test a schema migration on a copy of their prod database without affecting prod. The fastest CSI feature to use:",
            options=[
                ("a) <code>VolumeSnapshot</code> + restore into a new PVC", False),
                ("b) Use <code>dataSource: existingPVC</code> to clone the PVC directly", True),
                ("c) <code>kubectl cp</code> the data out and back in", False),
            ],
            feedback="<strong>Answer: b.</strong> Direct PVC cloning is fastest and one step. <code>VolumeSnapshot</code> works too but is a two-step (snapshot + restore). Both rely on the CSI driver's <code>VOLUME_DATA_SOURCE</code> capability.",
        ),
    },
    before_after_before='<p>Manual snapshots: SSH to the storage system, take a snapshot, write down the ID, copy the ID into a runbook. Backup retention = a script someone updates. Restoring means recreating the volume by hand.</p><p>Performance changes: detach the volume, modify it through the cloud console, re-attach. Pod restart. Five-minute outage minimum.</p>',
    before_after_after='<p>Snapshots: <code>kubectl apply -f snapshot.yaml</code>. The <code>VolumeSnapshot</code> object lives in the namespace, retention controlled by a <code>VolumeSnapshotClass</code>, restoration is just another PVC with <code>dataSource</code>.</p><p>Performance changes: <code>kubectl edit pvc</code> + a <code>volumeAttributesClassName</code> label change. CSI driver re-tunes the live disk. No Pod restart.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">All of this is the same pattern as the rest of K8s: the operator declares intent; a controller (CSI driver) makes it true. Storage joined the declarative party in 2019; live attribute changes joined in 2024.</p>',
    analogy_intro_html='<p>Back at the Customs Warehouse, but now we walk behind the counter to the loading dock. The PV (locker) you saw last lesson is still there — but who <em>delivers</em> a new locker when one is needed? Who <em>photographs</em> a locker for posterity? Who <em>upgrades</em> the lock from a basic latch to a deadbolt without unloading anything?</p><p>That is the <strong>CSI driver</strong>: a licensed contractor truck that pulls up to the dock with all the equipment for one specific kind of storage (the EBS truck, the NFS truck, the Ceph truck). The warehouse manager (Kubernetes) phones the truck through a standard intercom (the CSI gRPC spec); the truck does the work. <strong>Snapshots</strong> are a tenant photographer who copies a locker. <strong>Clones</strong> are a duplicator that makes a working copy. <strong>Expansion</strong> is a foreman who can bolt extensions onto a locker without making the renter empty it. <strong>VolumeAttributesClass</strong> is a quality-of-service dial — turn it up for premium IOPS, turn it down to save money — applied to a locker in use.</p>',
    translation_rows=[
        ("The contractor truck pulled up to the dock", "The <code>CSIDriver</code> object + DaemonSet + Deployment"),
        ("The standard intercom the manager uses", "The CSI gRPC API spec"),
        ("The tenant photographer", "<code>VolumeSnapshot</code> / <code>VolumeSnapshotContent</code>"),
        ("The locker duplicator", "PVC <code>dataSource</code> cloning"),
        ("The foreman bolting on extensions", "Volume expansion (<code>allowVolumeExpansion: true</code>)"),
        ("The quality-of-service dial", "<code>VolumeAttributesClass</code> (GA in 1.34)"),
        ("The locker can be at one node only", "Multi-attach errors with RWO + cloud block storage"),
    ],
    analogy_stops="The analogy stops here: real CSI drivers don't \"drive in\" — they're permanent Pods running in the cluster. And the snapshot's not a Polaroid; it's typically a copy-on-write block reference at the storage layer, which is why it's instant and storage-efficient.",
    eli5="Lesson 18 was about the locker (PV), the form (PVC), and the policy (StorageClass). This lesson is about the <em>person</em> who actually opens a locker for you, photographs it, copies it, or makes it bigger. That person is the CSI driver. They drive a truck specific to the kind of locker you want.",
    eli10="The <strong>CSI</strong> (Container Storage Interface) is a gRPC API. Vendors implement it as a CSI driver — typically a Deployment (controller-side: create/attach/snapshot calls) plus a DaemonSet (node-side: mount/format calls). Once the driver is installed, K8s exposes its features via standard objects: <code>VolumeSnapshot</code> for backups, PVC <code>dataSource</code> for clones, PVC size edits for expansion, and <code>VolumeAttributesClass</code> (GA in 1.34) for live performance changes. None of these features are \"in\" Kubernetes — they're all gated by what your CSI driver supports.",
    scenarios=[
        Scenario(name="A startup running PostgreSQL on EKS", body="Uses the AWS EBS CSI driver. Nightly <code>VolumeSnapshot</code> at 2 AM via a CronJob. Retention 30 days via VolumeSnapshotClass. After a botched migration, restoring took 4 minutes — create new PVC from yesterday's snapshot, scale StatefulSet down/up. The team's RTO went from hours to single-digit minutes."),
        Scenario(name="A bank running multiple Ceph CSI clusters", body="On-prem with Rook-Ceph. Uses RBD for block (RWO) and CephFS for shared (RWX). Policy: every PVC must have a <code>VolumeAttributesClass</code> labelling its perf tier. Bronze = HDD pool, silver = SSD, gold = NVMe. Live tier changes happen during business-hour traffic surges; reverted at night."),
        Scenario(name="A media company cloning prod into staging", body="Production database PVC is 4 TiB. Old staging refresh = 6 hours of pg_dump + restore. New process: <code>kubectl apply</code> a clone PVC referencing the prod PVC as <code>dataSource</code>. CSI driver does copy-on-write at the storage layer; staging PVC is ready in 90 seconds. Daily refresh now feasible."),
        Scenario(name="A SaaS expanding capacity in-place", body="Alert: PVC at 88%. Engineer edits the PVC, bumps storage from 100Gi to 250Gi. CSI driver expands the EBS volume; the kubelet runs <code>resize2fs</code> on the live filesystem. Pod never restarts. Total time: 90 seconds. The old way (recreate PVC bigger) would have meant a database failover."),
    ],
    misconceptions=[
        Misconception(myth="Snapshots are application-consistent.", truth="They're <em>crash-consistent</em> — equivalent to pulling the power cord. Database engines (Postgres, MySQL) usually handle this via their own crash-recovery, but for true app-consistency you want a pre-snapshot quiesce hook (which K8s 1.31+ supports via <code>VolumeGroupSnapshot</code> and pre/post hooks)."),
        Misconception(myth="VolumeAttributesClass is the same as StorageClass.", truth="StorageClass = recipe for <em>provisioning</em> a new PV. VolumeAttributesClass = recipe for <em>tuning attributes</em> on an existing PV. They're separate objects. A PVC has both <code>storageClassName</code> (immutable after binding) and <code>volumeAttributesClassName</code> (changeable; that's the whole point)."),
        Misconception(myth="Multi-attach errors are a Kubernetes bug.", truth="They're cloud reality. EBS, GCE PD, Azure Disk attach to one node at a time. If a Pod's old node is unreachable but K8s thinks it's still attached, the new Pod's mount fails. The fix is <code>force-detach</code> via the CSI driver — most modern drivers do this automatically after a node is marked NotReady."),
    ],
    flashcards=[
        Flashcard(front="What does CSI stand for?", back="Container Storage Interface — a gRPC API spec for storage drivers. Vendors implement it; K8s consumes it through sidecar containers (external-provisioner, external-attacher, external-snapshotter, external-resizer)."),
        Flashcard(front="What runs where in a CSI driver?", back="A Deployment (typically 1-2 replicas) for controller-side ops (create, delete, attach, snapshot) + a DaemonSet for node-side ops (mount, format). Both are usually in the <code>kube-system</code> or driver's own namespace."),
        Flashcard(front="VolumeSnapshot — what's a VolumeSnapshotContent?", back="A snapshot has two objects: VolumeSnapshot (namespace-scoped, declared by users) and VolumeSnapshotContent (cluster-scoped, created by the snapshotter; binds the snapshot to the actual storage-system snapshot ID)."),
        Flashcard(front="How do you clone a PVC?", back="Set <code>dataSource: { kind: PersistentVolumeClaim, name: source-pvc }</code> on the new PVC spec. CSI driver does a fast-path copy. Same namespace, same StorageClass required."),
        Flashcard(front="When does volume expansion work online?", back="StorageClass has <code>allowVolumeExpansion: true</code>; CSI driver supports <code>EXPAND_VOLUME</code>; filesystem supports online resize (ext4, XFS do; Btrfs partly). Edit PVC <code>spec.resources.requests.storage</code> upward; can't shrink."),
        Flashcard(front="What is VolumeAttributesClass (VAC)?", back="K8s 1.34 GA. Changes performance attributes (IOPS, throughput) on a live PVC by switching its <code>volumeAttributesClassName</code>. CSI driver re-tunes the underlying disk in place — no detach, no Pod restart."),
        Flashcard(front="Why do multi-attach errors happen?", back="RWO volume + Pod rescheduled before old node releases the attachment. Common when a node goes NotReady. CSI driver's force-detach logic + a node-down detection loop normally clears it within ~6 minutes."),
        Flashcard(front="VolumeGroupSnapshot — what's it for?", back="K8s 1.32+. Snapshots a <em>group</em> of PVCs atomically (e.g., a Postgres data PVC + WAL PVC at the same point in time). Required for true crash-consistent snapshots of multi-volume databases."),
    ],
    quizzes=[
        Quiz(prompt="Your StorageClass has <code>allowVolumeExpansion: true</code> but a PVC edit to grow from 100Gi to 200Gi gets stuck. What's the most likely cause?", answer="Either (1) the underlying CSI driver doesn't advertise <code>EXPAND_VOLUME</code> (rare with modern drivers, common with custom or in-tree-migrated ones), or (2) the filesystem inside the volume doesn't support online resize and the kubelet is waiting for a Pod restart to remount. Check <code>kubectl describe pvc</code> for events; look for <code>FilesystemResizePending</code> — bouncing the Pod typically completes the resize."),
        Quiz(prompt="A team writes a backup CronJob that uses <code>kubectl cp</code> from inside a Postgres Pod to an S3-backed sidecar. What's wrong with this strategy compared to <code>VolumeSnapshot</code>?", answer="Three problems: (1) <code>kubectl cp</code> traffics through the API server, which has hard timeout and size limits; large databases will fail. (2) Backup is application-level not storage-level, so you're paying network egress and CPU. (3) No point-in-time guarantees — Postgres might be writing while you copy. <code>VolumeSnapshot</code> is a storage-layer copy-on-write op, instant, doesn't touch the Pod, and combined with Postgres's WAL gives you crash-consistent recovery."),
        Quiz(prompt="Promo traffic ramps. The team's PostgreSQL PVC needs 8000 IOPS for the next 4 hours; today it's provisioned at 3000. The cluster runs K8s 1.34. <strong>Click for the modern playbook. ▼</strong>", cyoa=True, cyoa_tag="the modern playbook", answer="Define a <code>VolumeAttributesClass</code> with the higher IOPS tier (e.g. <code>tier: premium-burst</code> with 8000 IOPS, 500 MB/s). Patch the PVC: <code>kubectl patch pvc postgres-data --type=merge -p '{\"spec\":{\"volumeAttributesClassName\":\"premium-burst\"}}'</code>. The CSI driver picks this up and modifies the underlying EBS volume in place — no detach, no restart, no snapshot. Postgres keeps serving traffic at the new IOPS within ~30 seconds. After the promo, patch back to the standard tier. Total downtime: zero. <strong>Pre-1.34 alternative:</strong> snapshot-and-restore, which would have meant a 5-10 minute primary failover. VolumeAttributesClass is the single most consequential storage feature K8s shipped in years."),
    ],
    glossary=[
        GlossaryItem(name="CSI", definition="Container Storage Interface — gRPC spec for storage plugins. Replaces in-tree drivers."),
        GlossaryItem(name="CSIDriver object", definition="Cluster-scoped object that registers a CSI driver with K8s. Lists capabilities (snapshots, expansion, etc.)."),
        GlossaryItem(name="VolumeSnapshot", definition="Namespace-scoped object representing a point-in-time copy of a PVC. Survives PVC deletion."),
        GlossaryItem(name="VolumeSnapshotContent", definition="Cluster-scoped object binding a VolumeSnapshot to the storage system's snapshot ID. Like PV is to PVC."),
        GlossaryItem(name="VolumeSnapshotClass", definition="Recipe for taking snapshots — analogous to StorageClass for PVs."),
        GlossaryItem(name="dataSource", definition="PVC field that references either an existing PVC (clone) or a VolumeSnapshot (restore). The CSI driver populates the new volume."),
        GlossaryItem(name="allowVolumeExpansion", definition="StorageClass field. When true and the CSI driver supports it, PVCs can be resized larger by editing storage requests."),
        GlossaryItem(name="VolumeAttributesClass (VAC)", definition="K8s 1.34 GA. Changes a PVC's performance attributes live. Distinct from StorageClass — VAC tunes existing volumes; SC provisions new ones."),
        GlossaryItem(name="external-provisioner", definition="Sidecar container in CSI driver Deployments that watches PVCs and calls the driver's CreateVolume RPC."),
        GlossaryItem(name="external-attacher", definition="Sidecar that calls the driver's ControllerPublishVolume RPC to attach volumes to nodes."),
        GlossaryItem(name="external-snapshotter", definition="Sidecar that watches VolumeSnapshot objects and calls the driver's CreateSnapshot RPC."),
        GlossaryItem(name="VolumeGroupSnapshot", definition="K8s 1.32+. Atomically snapshots multiple PVCs as a group — required for crash-consistent multi-volume DB backups."),
    ],
    recap_lead="Behind every PVC there's a CSI driver. Once the driver's there, you get snapshots, clones, online expansion, and VolumeAttributesClass for live performance changes — none of which existed in the K8s core; they all came from CSI vendors implementing the spec.",
    recap_next="<strong>Next — Lesson 20: Configuration & Secrets.</strong> ConfigMap, Secret, KMS-encryption-at-rest, and the External Secrets Operator. Why \"secret\" in K8s is mostly a polite fiction unless you wire up encryption-at-rest. Permit Office issues the credentials.",
)
