from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Storage vault: shelves labeled EBS (block), EFS (RWX), FSx (Lustre/ONTAP/OpenZFS), S3 Mountpoint; KMS lock; snapshot timeline.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">STORAGE VAULT · EBS / EFS / FSx / S3</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <rect x="14" y="34" width="140" height="60" rx="4" fill="#3F4A5E"/><text x="84" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">EBS CSI</text><text x="84" y="64" text-anchor="middle" font-size="7" fill="#FBE8DC">RWO block · gp3/io2</text><text x="84" y="76" text-anchor="middle" font-size="7" fill="#FBE8DC">snapshots · VAC live IOPS</text>
    <rect x="160" y="34" width="140" height="60" rx="4" fill="#5A9F7A"/><text x="230" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">EFS CSI</text><text x="230" y="64" text-anchor="middle" font-size="7" fill="#FBE8DC">RWX shared filesystem</text><text x="230" y="76" text-anchor="middle" font-size="7" fill="#FBE8DC">multi-AZ · pay per GB</text>
    <rect x="306" y="34" width="140" height="60" rx="4" fill="#A04832"/><text x="376" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">FSx CSI</text><text x="376" y="64" text-anchor="middle" font-size="7" fill="#FBE8DC">Lustre · ONTAP · OpenZFS</text><text x="376" y="76" text-anchor="middle" font-size="7" fill="#FBE8DC">specialty workloads</text>
    <rect x="452" y="34" width="140" height="60" rx="4" fill="#E8B547"/><text x="522" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">S3 Mountpoint</text><text x="522" y="64" text-anchor="middle" font-size="7" fill="#5A4F45">object storage as FS</text><text x="522" y="76" text-anchor="middle" font-size="7" fill="#5A4F45">read-heavy · ML datasets</text>
    <rect x="14" y="100" width="572" height="22" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="300" y="114" text-anchor="middle" font-size="8" fill="#A04832" font-weight="700">snapshot-controller (cluster-wide) · KMS encryption · zone-aware StorageClass</text>
    <rect x="14" y="128" width="572" height="22" rx="3" fill="#3F4A5E"/><text x="300" y="142" text-anchor="middle" font-size="8" fill="#FBF1D6">multi-attach errors: EBS RWO + Pod rescheduling between AZs is the classic gotcha</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="05",
    title_short="storage",
    title_full="E5 · EKS Storage (EBS, EFS, FSx, S3 Mountpoint)",
    title_html="K-EKS E5 · EKS Storage",
    module_eyebrow="Module E5 · the storage vault",
    hero_sub_html='Four CSI drivers ship as managed add-ons. <strong>EBS CSI</strong> for RWO block (default for stateful workloads); <strong>EFS CSI</strong> for RWX shared filesystem; <strong>FSx CSI</strong> for specialty (Lustre / ONTAP / OpenZFS); <strong>S3 Mountpoint CSI</strong> for object storage as a filesystem. Plus snapshot-controller, KMS encryption, zone-aware StorageClasses.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Pod rescheduled by Karpenter consolidation lands in a different AZ from its EBS volume. <code>FailedAttachVolume</code>. The PVC is wedged for 6 minutes while AWS detaches + reattaches. Your Postgres replica is offline; service is degraded. <em>EBS is single-AZ; cross-AZ Pod movement requires snapshot+restore or you accept the multi-AZ cost</em>. Today\'s module is the storage decision tree that prevents this.',
    stamp_html='Storage CSI drivers (managed add-ons): <strong>EBS CSI</strong> (RWO block; gp3 default; <strong>VolumeAttributesClass for live IOPS/throughput tuning</strong>), <strong>EFS CSI</strong> (RWX, multi-AZ), <strong>FSx CSI</strong> (Lustre / NetApp ONTAP / OpenZFS), <strong>S3 Mountpoint CSI</strong> (object as FS, read-heavy). <strong>snapshot-controller</strong> for VolumeSnapshot. <strong>KMS encryption</strong> on every StorageClass. <strong>WaitForFirstConsumer</strong> for zone-aware provisioning.',
    district_pin="ks-floor05",
    district_label="Storage Vault",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Pick storage by access pattern, not by name",
            body_html="""    <table class="data-table">
      <thead><tr><th>Driver</th><th>Access mode</th><th>When</th><th>$/GB-month (rough)</th></tr></thead>
      <tbody>
        <tr><td><strong>EBS CSI</strong></td><td>RWO (one node)</td><td>Stateful workloads (Postgres, Redis); single-replica primary</td><td>$0.08 (gp3); $0.125 (io2)</td></tr>
        <tr><td><strong>EFS CSI</strong></td><td>RWX (many nodes)</td><td>Shared content stores, log staging, multi-Pod readers</td><td>$0.30 (Standard); $0.16 (IA)</td></tr>
        <tr><td><strong>FSx Lustre CSI</strong></td><td>RWX HPC</td><td>HPC, ML training datasets, parallel filesystems</td><td>~$0.25-0.60 depending on tier</td></tr>
        <tr><td><strong>FSx ONTAP CSI</strong></td><td>RWX enterprise NAS</td><td>NetApp shops; enterprise NFS/SMB</td><td>premium</td></tr>
        <tr><td><strong>FSx OpenZFS CSI</strong></td><td>RWX with snapshots/clones</td><td>Heavy snapshot/clone use; faster than EFS for some patterns</td><td>~$0.10</td></tr>
        <tr><td><strong>S3 Mountpoint CSI</strong></td><td>RWX read-mostly</td><td>ML datasets, logs archive, immutable content</td><td>$0.023 (Standard) + request fees</td></tr>
      </tbody>
    </table>""",
        ),
        Section(
            eyebrow="Section 1.5 · EBS CSI — the workhorse",
            h2="gp3 / io2 + VolumeAttributesClass",
            body_html="""    <p><strong>gp3</strong> (general purpose SSD) is the default for most workloads. <strong>io2</strong> (provisioned IOPS) for &gt; 16K IOPS or sub-ms latency requirements. <strong>st1/sc1</strong> (HDD) for cold logs / batch.</p>
    <p>2026 game-changer: <strong>VolumeAttributesClass</strong> (K8s 1.34 GA, EBS CSI supports it). Live re-tune IOPS / throughput on a PVC by changing one label — no detach, no Pod restart. Promo traffic spike: bump from 3000 IOPS to 8000 IOPS in 30 seconds.</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># StorageClass — gp3 with KMS encryption + WaitForFirstConsumer
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: gp3-encrypted}
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-east-1:123:key/abc"
volumeBindingMode: WaitForFirstConsumer    # critical for multi-AZ
reclaimPolicy: Delete
allowVolumeExpansion: true
---
# VolumeAttributesClass — premium burst
apiVersion: storage.k8s.io/v1beta1
kind: VolumeAttributesClass
metadata: {name: premium-burst}
driverName: ebs.csi.aws.com
parameters:
  iops: "8000"
  throughput: "500"</code></pre>""",
        ),
        Section(
            eyebrow="Section 1.7 · EFS, FSx, S3",
            h2="When EBS isn't enough",
            body_html="""    <p><strong>EFS CSI</strong>: RWX, multi-AZ, infinite scale. Mounts as NFS. Good for shared content + log staging. Slower than local EBS; $0.30/GB-month vs $0.08. Provisioning modes: <em>dynamic</em> (CSI creates EFS access points per PVC) or <em>static</em> (point at an existing EFS).</p>
    <p><strong>FSx Lustre CSI</strong>: RWX, parallel filesystem, HPC-grade throughput. Used for ML training datasets where 1000s of GPUs read concurrently. Pricier; provisioning is slow (15+ min).</p>
    <p><strong>FSx ONTAP CSI</strong>: NetApp ONTAP. Enterprise NAS features (NFS+SMB, dedup, replication). Used by orgs with existing NetApp investment + workloads needing premium NAS.</p>
    <p><strong>FSx OpenZFS CSI</strong>: cheaper than ONTAP; great snapshot + clone performance.</p>
    <p><strong>S3 Mountpoint CSI</strong> (newer; 2023 GA): mounts an S3 bucket as a filesystem. Read-mostly; writes are append-only or full-object-rewrite. Killer use case: ML training reads 10TB dataset from S3 directly without staging to EBS.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Snapshots + KMS + zone awareness",
            h2="Cross-cutting decisions",
            body_html="""    <ul>
      <li><strong>snapshot-controller</strong>: install once cluster-wide. Enables <code>VolumeSnapshot</code> CRD; CSI drivers (EBS, EFS, FSx) implement the actual snapshot.</li>
      <li><strong>KMS encryption</strong>: every StorageClass should set <code>encrypted: true</code> + <code>kmsKeyId</code>. Default to a customer-managed key (CMK), not the AWS-managed default key — gives you key-rotation control + cross-account access constraints.</li>
      <li><strong>volumeBindingMode: WaitForFirstConsumer</strong>: <em>required</em> in multi-AZ clusters. Without it, EBS provisions in a random AZ before the Pod is scheduled; Pod lands in a different AZ; FailedAttachVolume forever.</li>
      <li><strong>Multi-attach errors</strong>: EBS attaches to one node at a time. Pod reschedules to a different node → AWS detaches from old + attaches to new; takes ~6 min worst case. For high-availability stateful: use StatefulSet (stable identity per Pod) + per-Pod EBS via volumeClaimTemplates; reduces but doesn\'t eliminate attach delays.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>EBS multi-attach (RWX EBS via io2 + special config) exists but rarely fits — the EBS multi-attach is volume-level, not filesystem-level; you need a cluster-aware filesystem on top. Most teams use EFS for RWX instead.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your StatefulSet uses <code>volumeBindingMode: Immediate</code>. The cluster spans 3 AZs. After deploy, half the Pods are Pending forever. Diagnosis?',
            options=[
                ('a) The StorageClass is broken', False),
                ('b) Immediate binding provisioned EBS in a random AZ before Pods were scheduled. The scheduler now wants to place Pods in a different AZ to satisfy topology spread; cloud block storage can\'t cross AZs. Switch to WaitForFirstConsumer.', True),
                ('c) Add more nodes', False),
            ],
            feedback='<strong>Answer: b.</strong> Classic multi-AZ + Immediate binding bug. Fix: edit StorageClass to <code>volumeBindingMode: WaitForFirstConsumer</code>; recreate failed PVCs. New PVCs will provision in the Pod\'s zone after scheduling. Always WaitForFirstConsumer on multi-AZ EBS.',
        ),
    },
    before_after_before='<p>Manual EBS volumes attached via console + edits to fstab on EC2. Backup script to S3 maybe runs nightly. KMS on some volumes. Multi-AZ failures involve recovery scripts a junior engineer wrote.</p>',
    before_after_after='<p>EBS CSI managed add-on. PVC YAML in git creates volume + KMS-encrypted by default. WaitForFirstConsumer for zone alignment. VolumeSnapshot for backup. VAC for live perf changes. Storage is K8s-native.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">EKS storage works exactly like vanilla K8s storage with the AWS CSIs and KMS-by-default — once you align CIDR / AZ / encryption at launch.</p>',
    analogy_intro_html='<p>The Storage Vault occupies a quiet floor of K-Skyline. Walk in: rows of safe-deposit boxes (EBS — one tenant per box, RWO), shared filing cabinets (EFS — many tenants, RWX), specialty vaults for HPC tenants (FSx Lustre / ONTAP / OpenZFS), and a vast warehouse you can shelf-mount (S3 Mountpoint). Every box, cabinet, vault is locked with the building\'s master key system (KMS). The vault clerk schedules photographs of every box overnight (snapshots). And there\'s a clear rule: <em>safe-deposit boxes don\'t move floors</em> (EBS is single-AZ).</p>',
    translation_rows=[
        ('Safe-deposit box (one tenant)', 'EBS volume (RWO)'),
        ('Shared filing cabinet (many tenants)', 'EFS (RWX)'),
        ('HPC parallel-access vault', 'FSx Lustre'),
        ('Enterprise NAS specialty vault', 'FSx ONTAP'),
        ('Cheap photo-loving vault', 'FSx OpenZFS'),
        ('Public archive shelf-mountable', 'S3 Mountpoint'),
        ('Master key system', 'KMS encryption (encrypted: true + kmsKeyId)'),
        ('Overnight box photographs', 'VolumeSnapshot via snapshot-controller'),
        ('Boxes don\'t move floors', 'EBS is single-AZ; multi-AZ Pod = wait or snapshot'),
        ('Live re-renting with new IOPS tier', 'VolumeAttributesClass (live IOPS change)'),
    ],
    analogy_stops="The analogy stops here: real CSI drivers run as DaemonSets + controller Deployments coordinating with EBS / EFS / FSx APIs over IAM-authenticated calls. The vault is software, not steel.",
    eli5='Different lockers for different needs. Solo locker (EBS), shared library (EFS), super-fast HPC locker (FSx), and a giant photo-warehouse you can pretend is a locker (S3 Mountpoint). All locked with the same master key system.',
    eli10="Four CSI driver families: EBS (RWO block, default); EFS (RWX shared, multi-AZ); FSx Lustre/ONTAP/OpenZFS (specialty); S3 Mountpoint (object as FS, read-heavy). All install as managed add-ons. Always set encrypted+kmsKeyId on StorageClasses. WaitForFirstConsumer for multi-AZ. VolumeAttributesClass (1.34) for live IOPS changes on EBS. snapshot-controller cluster-wide enables VolumeSnapshot.",
    scenarios=[
        Scenario(name='A SaaS using gp3 + VAC for promotional bursts', body='Standard StorageClass: gp3 3000 IOPS / 125 MB/s. Promo VAC: 8000 IOPS / 500 MB/s. PVC patched at 14:00 → live re-tune in 30s → patched back at 22:00. Cost only during the window. Saved a permanent over-provision.'),
        Scenario(name='A bank with multi-AZ Postgres on StatefulSet + EBS', body='3 Postgres replicas, each with own EBS via volumeClaimTemplates. WaitForFirstConsumer. Pod-Disruption-Budget minAvailable=2. Rolling Pod restart: each Pod\'s EBS detaches + reattaches in same AZ; ~30s each; replication catches up.'),
        Scenario(name='An ML team using S3 Mountpoint for training data', body='4 TB image dataset in S3. S3 Mountpoint CSI mounts the bucket as <code>/data</code>. PyTorch reads directly. No staging to EBS. Cost: ~$100/month for the dataset + read requests. Pre-Mountpoint: copying to EFS or EBS cost 10× more + staging time was hours.'),
        Scenario(name='A team that fixed a multi-AZ scheduling issue', body='HPA scaled a StatefulSet from 1 → 3. Original Immediate-binding StorageClass provisioned all 3 PVCs in us-east-1a. Topology-spread placed Pods in 1a, 1b, 1c. 2 Pods Pending. Migration: delete failed PVCs, switch StorageClass to WaitForFirstConsumer, redeploy. Now zone-aligned.'),
    ],
    misconceptions=[
        Misconception(myth='\"EBS RWO means one Pod.\"', truth='RWO = one node. Multiple Pods on the same node can mount the same EBS. RWOP (1.27+) is the new \"one Pod\" semantic.'),
        Misconception(myth='\"WaitForFirstConsumer is just an optimisation.\"', truth='In multi-AZ clusters it\'s a correctness fix. Without it, EBS volumes land in random AZs and Pods stuck Pending. Always use it.'),
        Misconception(myth='\"S3 Mountpoint is a full POSIX filesystem.\"', truth='Read-mostly. Writes are append-only or full-object replace. No directory rename, no random write into a file. Great for ML datasets, awkward for general apps.'),
    ],
    flashcards=[
        Flashcard(front='Four EKS CSI driver families?', back='EBS (RWO block), EFS (RWX NFS multi-AZ), FSx (Lustre / ONTAP / OpenZFS specialty), S3 Mountpoint (object as FS read-heavy). All as managed add-ons.'),
        Flashcard(front='Why WaitForFirstConsumer in multi-AZ?', back='EBS is single-AZ. Immediate binding provisions volume before Pod scheduling; Pod may land in different AZ → FailedAttachVolume. WaitForFirstConsumer aligns volume to Pod\'s zone.'),
        Flashcard(front='What is VolumeAttributesClass on EBS?', back='K8s 1.34 GA. Live re-tune IOPS / throughput on a PVC by changing label. EBS CSI invokes ModifyVolume — no detach, no Pod restart, ~30s.'),
        Flashcard(front='snapshot-controller — what is it?', back='K8s SIG-Storage component (separate from CSI driver). Translates VolumeSnapshot API objects into CSI snapshot calls. Install once per cluster.'),
        Flashcard(front='gp3 vs io2 vs st1?', back='gp3: general SSD, default, $0.08/GB. io2: provisioned IOPS for &gt; 16K IOPS, $0.125/GB. st1: HDD for cold/batch, $0.045/GB.'),
        Flashcard(front='EFS — when to use?', back='RWX shared filesystem. Multi-AZ. Slower than local EBS but pay-per-use. Good for shared content, log staging, multi-Pod readers.'),
        Flashcard(front='FSx Lustre — when?', back='HPC, ML training. Parallel filesystem, very high throughput. Pricey; long provision time (15+ min).'),
        Flashcard(front='S3 Mountpoint — when?', back='Read-heavy ML datasets, immutable content, archive logs. Cheap (S3 storage prices). Limited write semantics.'),
    ],
    quizzes=[
        Quiz(prompt='Your team\'s ML training Pod fails with <code>permission denied</code> mounting an EFS access point. The IAM policy looks correct. Diagnose.', answer='<strong>Likely two-tier issue:</strong> (1) <strong>EFS access point POSIX UID/GID.</strong> The access point creates files as a specific UID/GID. The Pod\'s container runs as a different UID. <code>fsGroup</code> in PodSpec should match the EFS access-point GID. (2) <strong>Pod Identity / IRSA</strong> for the EFS CSI controller pods. The controller needs IAM permissions to call EFS. Verify the SA association. <strong>Diagnose:</strong> <code>kubectl describe pvc</code> for events; <code>kubectl logs -n kube-system efs-csi-controller-XXX</code>; check the EFS access-point definition in AWS Console for UID/GID. <strong>Fix:</strong> align Pod\'s fsGroup with EFS access-point GID; verify IAM policy includes <code>elasticfilesystem:DescribeAccessPoints + ClientMount + ClientWrite</code>.'),
        Quiz(prompt='You\'re asked to make an EBS-backed Postgres survive an AZ outage. What design?', answer='<strong>EBS is single-AZ; can\'t survive AZ loss directly.</strong> Two patterns: (1) <strong>Postgres replication across AZs</strong>: 3 Postgres Pods (StatefulSet), each in its own AZ via topology-spread, each with its own EBS. Postgres handles replication (sync or async). AZ outage → 2 surviving Pods take over. (2) <strong>Aurora / RDS Multi-AZ</strong>: take Postgres out of EKS entirely; let AWS handle Multi-AZ. Pods connect to RDS endpoint. <strong>For pure-K8s in EKS:</strong> pattern 1, often via the Crunchy or CloudNativePG operator. <strong>Snapshot strategy</strong>: VolumeSnapshot per replica nightly to S3-backed snapshot storage. <strong>Don\'t</strong> rely on EBS Multi-AZ — there isn\'t a thing for general EBS volumes; only specific io2 multi-attach (limited).'),
        Quiz(prompt='Migration from EBS-only to EBS + S3 Mountpoint for ML training data. <strong>Click for the playbook. ▼</strong>', cyoa=True, cyoa_tag='the playbook', answer='<strong>(1) Move dataset to S3.</strong> If currently on EBS / EFS, copy to an S3 bucket. Versioned bucket recommended. <strong>(2) Install S3 Mountpoint CSI</strong> as a managed add-on. <strong>(3) Create IAM role + Pod Identity association</strong> for the training SA: read access to the dataset bucket. <strong>(4) Define StorageClass + PVC</strong>: <pre style=\'background:#F5EFE3;padding:6px;font-size:11px\'>apiVersion: v1\nkind: PersistentVolume\nmetadata: {name: training-data}\nspec:\n  capacity: {storage: 4Ti}\n  accessModes: [ReadOnlyMany]\n  csi:\n    driver: s3.csi.aws.com\n    volumeAttributes:\n      bucketName: training-data-prod\n      mountOptions: \"--allow-other,--region us-east-1\"</pre> <strong>(5) PVC + Pod</strong>: PVC binds to the static PV; Pod mounts at <code>/data</code>. PyTorch reads directly. <strong>(6) Validate</strong> training throughput vs old EBS-staged approach. <strong>(7) Decommission EBS staging</strong> volumes after validation. <strong>Cost</strong>: S3 storage at $0.023/GB-month + read requests per epoch — vs EBS $0.08/GB constantly. For a 4 TB dataset trained 10× per month: S3 ~$95/month vs EBS ~$320/month + staging time. <strong>Caveat:</strong> S3 Mountpoint write semantics limited; if your training writes intermediate checkpoints, separate EBS PVC for that.'),
    ],
    glossary=[
        GlossaryItem(name='EBS CSI', definition='AWS-managed add-on. Provisions Elastic Block Store volumes for K8s. RWO. Default for stateful workloads.'),
        GlossaryItem(name='gp3 / io2 / st1', definition='EBS volume types. gp3 = general SSD (default). io2 = provisioned IOPS. st1 = HDD throughput.'),
        GlossaryItem(name='VolumeAttributesClass (EBS)', definition='K8s 1.34 GA. Live re-tune IOPS / throughput. EBS CSI invokes ModifyVolume.'),
        GlossaryItem(name='EFS CSI', definition='Managed add-on. Provisions EFS access points or mounts existing EFS. RWX, multi-AZ.'),
        GlossaryItem(name='FSx Lustre CSI', definition='Managed add-on for FSx for Lustre. HPC parallel filesystem.'),
        GlossaryItem(name='FSx ONTAP CSI', definition='Managed add-on for FSx for NetApp ONTAP. Enterprise NAS.'),
        GlossaryItem(name='FSx OpenZFS CSI', definition='Managed add-on for FSx for OpenZFS. Snapshot + clone heavy.'),
        GlossaryItem(name='S3 Mountpoint CSI', definition='Mounts S3 bucket as a filesystem. Read-mostly; ML datasets, archive logs.'),
        GlossaryItem(name='snapshot-controller', definition='K8s SIG-Storage component. Translates VolumeSnapshot CRDs to CSI snapshot calls. Install cluster-wide.'),
        GlossaryItem(name='WaitForFirstConsumer', definition='StorageClass binding mode. Provision PV after Pod scheduling — aligns volume to Pod\'s zone.'),
        GlossaryItem(name='Customer-managed KMS key (CMK)', definition='Your KMS key (vs AWS-managed default). Gives rotation control + cross-account constraints.'),
        GlossaryItem(name='Multi-attach error (EBS)', definition='EBS attaches to one node. Pod reschedule = detach + reattach; ~6 min worst case. Mitigate via StatefulSet + topology spread.'),
    ],
    recap_lead='Four CSI drivers (EBS / EFS / FSx / S3) as managed add-ons. KMS-encrypted by default. WaitForFirstConsumer in multi-AZ. VolumeAttributesClass for live perf changes. snapshot-controller cluster-wide for VolumeSnapshot.',
    recap_next='<strong>Next — E6: EKS Compute and Autoscaling.</strong> Karpenter (recommended), Cluster Autoscaler (legacy), spot strategies, Graviton, GPU + Inferentia + Trainium for AI/ML.',
)
