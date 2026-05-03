"""K-ECS C5 — ECS Storage."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS storage — bind mounts, Docker volumes, EFS, FSx, ephemeral storage.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Cargo Holds · K-Harbor — five storage shapes, pick by lifetime + sharing</text>
  <rect x="40" y="70" width="135" height="120" rx="10" fill="#7AB3CC" stroke="#1F2433"/>
  <text x="107" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">ephemeral</text>
  <text x="107" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Fargate 20→200 GiB</text>
  <text x="107" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">per-Task scratch</text>
  <text x="107" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">dies with Task</text>
  <text x="107" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">EC2: host disk</text>
  <rect x="190" y="70" width="135" height="120" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="257" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">bind mount</text>
  <text x="257" y="108" text-anchor="middle" font-size="9" fill="#1F2433">EC2 host path</text>
  <text x="257" y="124" text-anchor="middle" font-size="9" fill="#1F2433">EC2-only</text>
  <text x="257" y="144" text-anchor="middle" font-size="9" fill="#1F2433">cheap, fast</text>
  <text x="257" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">host-coupled</text>
  <rect x="340" y="70" width="135" height="120" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="407" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Docker volume</text>
  <text x="407" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">EBS / local on EC2</text>
  <text x="407" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">EC2-only</text>
  <text x="407" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">REX-Ray plugin</text>
  <text x="407" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">legacy pattern</text>
  <rect x="490" y="70" width="135" height="120" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="557" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">EFS</text>
  <text x="557" y="108" text-anchor="middle" font-size="9" fill="#1F2433">NFSv4 RWX</text>
  <text x="557" y="124" text-anchor="middle" font-size="9" fill="#1F2433">cross-AZ</text>
  <text x="557" y="144" text-anchor="middle" font-size="9" fill="#1F2433">access points</text>
  <text x="557" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">shared-state win</text>
  <rect x="640" y="70" width="80" height="120" rx="10" fill="#5E4A8E" stroke="#1F2433"/>
  <text x="680" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">FSx</text>
  <text x="680" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Windows /</text>
  <text x="680" y="122" text-anchor="middle" font-size="9" fill="#FBF1D6">NetApp ONTAP</text>
  <text x="680" y="142" text-anchor="middle" font-size="9" fill="#FBF1D6">SMB / NFS</text>
  <text x="680" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">specialty use</text>
</svg>"""


LESSON = LessonSpec(
    num="05",
    title_short="ECS storage",
    title_full="C5 · ECS Storage — Ephemeral, Bind, Docker, EFS, FSx",
    title_html="K-ECS C5 · ECS Storage",
    module_eyebrow="Module C5 · Cargo Holds — five storage shapes; pick by lifetime + sharing",
    hero_sub_html='Five storage shapes for ECS Tasks. <strong>Ephemeral storage</strong> — per-Task scratch (Fargate default 20 GiB → 200 GiB; EC2 launch uses host disk). <strong>Bind mount</strong> — EC2 host path; cheap, fast, host-coupled (lost on host change). <strong>Docker volume</strong> — EBS / local volume on EC2 host (legacy pattern). <strong>EFS</strong> — NFSv4 managed filesystem; RWX-equivalent across many Tasks and AZs; access points for path / UID / perm isolation; <em>the shared-state answer for ECS</em>. <strong>FSx for Windows File Server / NetApp ONTAP</strong> — SMB / NFS-attach for Windows or higher-tier file storage needs.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. The image-processing Service runs on Fargate. Default ephemeralStorage = 20 GiB. A user uploads a 4 GB ZIP that expands to 35 GB during processing. Disk full. Task crashes. <em>Ephemeral storage you didn\'t tune is the disk fault you didn\'t see coming.</em> Today\'s lesson: pick the right storage shape per workload + know what happens when each one runs out.",
    stamp_html="<strong>Pick storage by lifetime + sharing. Ephemeral = per-Task scratch (sized in Task Definition). EFS = the only RWX-across-Tasks-across-AZs answer. Bind mounts + Docker volumes are EC2-only legacy. FSx for Windows or NetApp use cases. Always set ephemeralStorage explicitly on Fargate when you need >20 GiB.</strong>",
    district_pin="kh-pier05",
    district_label="Cargo Holds",
    sections=[
        Section(
            eyebrow="Section 1.1 · ephemeral storage",
            h2="Per-Task scratch, sized at Task Definition",
            body_html="""    <p><strong>Fargate</strong> Tasks ship with <em>20 GiB ephemeral storage by default</em>. Set <code>ephemeralStorage.sizeInGiB</code> in the Task Definition top level (range 21-200). Stored on the underlying microVM; <strong>destroyed when the Task stops</strong> — no persistence across Task restarts.</p>
    <p><strong>EC2 launch</strong>: ephemeral storage is the host disk filesystem. Containers see whatever path they bind-mount; quotas are not enforced per-Task by ECS. Tune via the host\'s root volume size + cleanup containers (or use Bottlerocket\'s built-in image GC).</p>
    <p><strong>External / ECS Anywhere</strong>: same as EC2 — the host\'s disk is the ephemeral pool.</p>
    <p><strong>Use cases</strong>: temp file processing, image build buffers, in-memory-DB write-ahead logs that get checkpointed to durable storage. Anywhere you don\'t need state to survive Task restart.</p>
    <p><strong>Encryption</strong>: ephemeral storage on Fargate is encrypted with AWS-managed keys by default; customer-managed KMS keys via <code>ephemeralStorageKmsKeyId</code> (ECS Fargate platform version 1.4.0+).</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · bind mounts + Docker volumes",
            h2="EC2-launch storage patterns",
            body_html="""    <p><strong>Bind mounts</strong>: declare a Task-level <code>volumes</code> entry with <code>host: { sourcePath: "/data" }</code>. Containers mount it via <code>mountPoints</code>. Cheap; uses host filesystem. <em>Lost when Task moves hosts</em> (ECS may reschedule on a different EC2). <em>EC2 launch only.</em></p>
    <p><strong>Docker volumes</strong>: Task-level <code>volumes</code> with <code>dockerVolumeConfiguration</code>. Driver options: <code>local</code> (Docker\'s default — host-local), <code>rexray/ebs</code> (EBS-backed via REX-Ray plugin — legacy), other community drivers. <em>EC2 launch only.</em> Setup overhead: install + configure the volume driver on every EC2 host (custom AMI or daemonset Tasks).</p>
    <p><strong>Why these are legacy</strong>: with awsvpc + Fargate dominant, host-coupled storage is rarely the right answer. EFS or ephemeral storage covers most needs; Docker volume drivers require host AMI work that ECS\'s shift to managed launch types eliminates. Documented for completeness; pick EFS/ephemeral instead for new workloads.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · EFS — the shared-state answer",
            h2="NFSv4 managed filesystem; access points; mount targets per AZ",
            body_html="""    <p><strong>EFS</strong> is a managed NFSv4 filesystem mounted via <code>volumes[].efsVolumeConfiguration</code>. Multiple Tasks across multiple AZs mount the same filesystem — true RWX-equivalent. Pay-per-GB-month (Standard or IA storage classes); throughput modes (Bursting, Provisioned, Elastic).</p>
    <p><strong>Access points</strong>: managed entrypoints into an EFS filesystem with a <em>path + POSIX UID/GID + permission</em>. One access point per Task workload. Configure in Task Definition: <code>accessPointId</code> + <code>iam: ENABLED</code>. ECS auto-mounts at the access point\'s root path; the Task sees only its own subtree; UID/GID enforced server-side.</p>
    <p><strong>IAM auth</strong>: <code>iam: ENABLED</code> + <code>transitEncryption: ENABLED</code> + execution role policy <code>elasticfilesystem:ClientMount + ClientWrite</code> on the FS or access point. Replaces relying on host-level NFS auth.</p>
    <p><strong>Mount targets</strong>: one per AZ in your VPC. Tasks must be in subnets that can reach the access point\'s mount target (NFS port 2049). Endpoint SG allows port 2049 from Task SGs.</p>
    <p><strong>Performance gotcha</strong>: EFS Standard is durable + cross-AZ but has higher latency than EBS or local SSD. For high-IOPS small-file workloads, prefer ephemeralStorage + S3 archival or step out to EBS-on-EC2.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · FSx for Windows / NetApp ONTAP",
            h2="SMB and higher-tier file storage",
            body_html="""    <p><strong>FSx for Windows File Server</strong>: managed Windows-native SMB share. Use when Tasks are Windows containers needing SMB shares (legacy Windows apps, file-share-based integrations). Configure in Task Definition with <code>fsxWindowsFileServerVolumeConfiguration</code>: <code>fileSystemId</code> + <code>rootDirectory</code> + <code>authorizationConfig</code> (credentialsParameter pointing at SSM/Secrets credentials + domain). Active Directory integration via AWS Managed Microsoft AD or self-managed AD.</p>
    <p><strong>FSx for NetApp ONTAP</strong>: enterprise-grade NFS / SMB / iSCSI managed by AWS. Multi-protocol (a Linux Task and a Windows Task can share the same dataset). Snapshots, FlexClone, replication, deduplication. Integration with ECS works via <code>volumes[].efsVolumeConfiguration</code>-style mounting (NFS endpoint pinned in subnet) — treat the ONTAP NFS endpoint like an EFS mount target. <em>Choose for use cases needing snapshot speed, multi-protocol, or NetApp-specific features.</em></p>
    <p><strong>FSx for OpenZFS / FSx for Lustre</strong> <span class="skip-tag">[ deep dive — skip if new ]</span>: less common with ECS but supported via similar NFS-mount patterns. Lustre for HPC + ML training data lakes; OpenZFS for snapshot-heavy use.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A Fargate Task processes 4 GB ZIPs that expand to 35 GB during decompression. Default ephemeralStorage = 20 GiB. What\'s the fix?",
            options=[
                ("Move to EC2 launch — Fargate has fixed disk.", False),
                ("Set <code>ephemeralStorage.sizeInGiB = 50</code> (or higher) in the Task Definition.", True),
                ("Add an EFS mount and write the temp files there.", False),
            ],
            feedback="Fargate ephemeralStorage is bumpable up to 200 GiB via Task Definition top-level field. EFS works too but adds NFS round trips for what\'s really just per-Task scratch. EC2 isn\'t needed.",
        ),
        3: PauseCheck(
            question="A Service has 10 Tasks across 3 AZs that all need to write to the same upload directory. Which storage shape?",
            options=[
                ("Bind mount — fast and cheap.", False),
                ("EFS with an access point — RWX across Tasks and AZs.", True),
                ("Ephemeral — let each Task write its own copy.", False),
            ],
            feedback="EFS is the only ECS storage shape that gives RWX semantics across many Tasks and many AZs. Access points isolate the upload directory cleanly.",
        ),
    },
    before_after_before='<p>Pre-EFS, ECS Tasks needing shared state used hand-rolled patterns: rsync from S3 on Task start, scp between EC2 hosts, EBS volumes attached/detached via Lambda, or hosting the share on a single EC2 with NFS server (single point of failure). Stateful workloads on ECS were rare because the storage story was painful.</p>',
    before_after_after='<p>Modern ECS storage is five well-defined shapes — ephemeral for per-Task scratch, EFS for cross-Task RWX, FSx for specialty needs, bind/Docker for EC2-launch legacy. Access points + IAM-auth give clean per-workload isolation. <em>Stateful ECS workloads are now a Tuesday-deploy.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Pick by lifetime first. Per-Task = ephemeral; cross-Task / cross-AZ = EFS; specialty = FSx; EC2-only legacy = bind / Docker. The shape decides the rest.</em></p>',
    analogy_intro_html='''<p>Down at the harbor\'s <strong>Cargo Holds</strong> there are five places to put cargo while ships work.</p>
    <p><strong>The ship\'s own scratch hold</strong> (ephemeral storage) is where each ship dumps temp cargo during the voyage. When the ship sails, the scratch hold goes with it — and when it docks at the breaker\'s yard, everything in it is gone. Cheap, fast, and yours alone. Each ship picks its scratch-hold size when it gets the cargo manifest.</p>
    <p><strong>The dock\'s back-room locker</strong> (bind mount, EC2-only) is a corner of the dock office where one ship borrows shelf space. Cheap, but only that ship at that dock can use it; if the ship moves to another dock the cargo is left behind.</p>
    <p><strong>The dock\'s rented locker</strong> (Docker volume, EC2-only) is similar — a dock-managed locker, possibly attached to a portable case (EBS via plugin) that can be moved. Fiddly to set up; mostly used by long-time tenants.</p>
    <p><strong>The harbor warehouse</strong> (EFS) is the shared building every ship can reach from any dock — fully fireproof and replicated across the harbor district. Multiple ships read and write at once. The harbor master assigns each ship its own gated room (access point) so paperwork and crews stay separate.</p>
    <p><strong>The specialty bonded warehouse</strong> (FSx for Windows / NetApp ONTAP) is a separate facility for Windows-only ships or for cargo that needs ONTAP\'s snapshot + dedup features. Niche; pick when the use case demands it.</p>''',
    translation_rows=[
        ("Ship\'s scratch hold (sized at boarding)", "ephemeralStorage (Fargate 20→200 GiB; sized in Task Definition)"),
        ("Dock back-room corner", "bind mount (EC2 launch host path)"),
        ("Dock rented locker", "Docker volume (REX-Ray / local on EC2)"),
        ("Harbor shared warehouse", "EFS — RWX across Tasks + AZs"),
        ("Warehouse gated room", "EFS access point (path + UID/GID + perms)"),
        ("Mount targets (one per AZ)", "EFS mount target per AZ"),
        ("Bonded Windows warehouse", "FSx for Windows File Server"),
        ("ONTAP specialty warehouse", "FSx for NetApp ONTAP (multi-protocol + snapshots)"),
        ("Warehouse access guard list", "IAM-auth: elasticfilesystem:ClientMount/ClientWrite"),
    ],
    analogy_stops="A real warehouse holds whatever you put in it; EFS access points enforce server-side UID/GID semantics that surface as POSIX permissions inside the Task. Some POSIX patterns (e.g., setuid binaries) interact differently than on local disk.",
    eli5="Ships have five places to put cargo. The ship\'s own scratch hold dies with the ship. The dock corner is shared with one ship at one dock. The shared warehouse can be reached from every dock by every ship at the same time. The bonded Windows warehouse is for Windows-only ships. Pick by what the cargo is and how long you need to keep it.",
    eli10="<strong>ephemeral</strong> = per-Task scratch (Fargate 20→200 GiB; EC2 host disk). <strong>bind mount</strong> = EC2 host path (host-coupled; legacy). <strong>Docker volume</strong> = EBS / local on EC2 (REX-Ray plugin; legacy). <strong>EFS</strong> = managed NFSv4; RWX cross-Task cross-AZ; access points + IAM auth + mount targets per AZ; the shared-state answer. <strong>FSx for Windows</strong> = SMB share for Windows containers. <strong>FSx for NetApp ONTAP</strong> = multi-protocol enterprise NFS/SMB.",
    scenarios=[
        Scenario(
            name="Image processing — bumped ephemeralStorage to 50 GiB",
            body="A 30-engineer media-processing SaaS resizes user-uploaded videos. ZIPs decompress to ~30 GB during work. Task Definition sets <code>ephemeralStorage.sizeInGiB = 50</code> on Fargate; per-Task workspace is local SSD-fast; nothing persists between Tasks. <em>One field flip; problem gone.</em>",
        ),
        Scenario(
            name="Shared uploads — EFS with access points",
            body="A team has an upload Service + a periodic-cleanup Service. EFS filesystem with one access point per workload (uploads, archives, previews); each Service\'s Task Definition mounts its specific access point. UID/GID isolation prevents cross-workload writes. <em>Multi-Task RWX without rolling NFS by hand.</em>",
        ),
        Scenario(
            name="Windows legacy — FSx for Windows + Active Directory",
            body="A regulated insurance back-office runs a Windows .NET service that expects an SMB share for input/output documents. ECS on EC2 (Windows ECS-optimised AMI). Task Definition mounts FSx for Windows File Server; AD authentication via <code>authorizationConfig</code>. <em>Lift-and-shift Windows app onto ECS without changing the storage assumption.</em>",
        ),
        Scenario(
            name="Outage — bind mount drift after host replacement",
            body="A team had bind-mounts to <code>/data/app-state</code> on EC2 hosts. Auto Scaling replaced one host overnight; new host had no <code>/data/app-state</code>; Tasks rescheduled there crashed (or wrote to a fresh empty path with no realisation). <em>Postmortem</em>: migrate to EFS — host-independent shared storage. <em>Bind mounts are a footgun for anything stateful.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Fargate ephemeral storage is unlimited / you don\'t need to size it.\"",
            truth="<strong>20 GiB default; capped at 200 GiB.</strong> Workloads exceeding 20 GiB must set <code>ephemeralStorage.sizeInGiB</code> in the Task Definition. Failing to do so produces \"no space left on device\" errors mid-Task that look like app bugs.",
        ),
        Misconception(
            myth="\"EFS is just a slower EBS.\"",
            truth="EFS and EBS solve different problems. <strong>EBS</strong> is single-instance block storage (one EC2 attaches one volume). <strong>EFS</strong> is multi-instance file storage (many Tasks across many AZs share). EFS is higher-latency than EBS; you trade for cross-Task / cross-AZ RWX. Don\'t pick by speed alone.",
        ),
        Misconception(
            myth="\"Bind mounts work fine on Fargate.\"",
            truth="<strong>Bind mounts are EC2 launch only.</strong> Fargate has no host filesystem you can bind to. The Fargate equivalents are ephemeralStorage (per-Task scratch) and EFS (cross-Task shared).",
        ),
    ],
    flashcards=[
        Flashcard(front="Fargate ephemeralStorage default + max?", back="<strong>20 GiB default</strong>; bumpable to <strong>200 GiB</strong> via Task Definition <code>ephemeralStorage.sizeInGiB</code>. Per-Task scratch; destroyed on Task stop. KMS-encrypted (AWS-managed default; customer-managed via <code>ephemeralStorageKmsKeyId</code>)."),
        Flashcard(front="Five ECS storage shapes?", back="<strong>ephemeral</strong> (per-Task scratch), <strong>bind mount</strong> (EC2 host path; legacy), <strong>Docker volume</strong> (EBS / local on EC2; legacy), <strong>EFS</strong> (NFSv4 RWX cross-Task cross-AZ), <strong>FSx</strong> (Windows / NetApp ONTAP)."),
        Flashcard(front="EFS access points — what do they isolate?", back="A managed entrypoint with <strong>path + POSIX UID/GID + permissions</strong>. Each Task workload gets its own access point; subtree visible to that Task only; UID/GID enforced server-side. One filesystem can host many access points."),
        Flashcard(front="EFS IAM auth — what enables it?", back="<code>iam: ENABLED</code> + <code>transitEncryption: ENABLED</code> in the volumeConfiguration; execution role policy with <code>elasticfilesystem:ClientMount</code> + <code>elasticfilesystem:ClientWrite</code> on the filesystem or access point. Replaces relying on NFS host-level auth."),
        Flashcard(front="Why are bind mounts and Docker volumes legacy?", back="EC2-launch only; host-coupled (bind mounts lost when Task moves hosts); volume drivers (REX-Ray etc.) require host AMI work that\'s sidestepped by Fargate + EFS. Use EFS or ephemeralStorage for new workloads."),
        Flashcard(front="When pick FSx for Windows over EFS?", back="When Tasks are Windows containers needing SMB shares. EFS is NFSv4 — Linux-friendly; Windows containers can\'t mount NFS in ECS\'s supported pattern. FSx for Windows = managed SMB + AD integration."),
        Flashcard(front="EFS mount targets — how many do you need?", back="<strong>One per AZ</strong> in your VPC. Tasks land in subnets that have a path to a mount target. The mount target\'s SG must allow NFS (port 2049) from the Task SGs."),
        Flashcard(front="High-IOPS small-file workload — EFS or alternative?", back="EFS Standard has higher latency than local SSD or EBS. For IOPS-sensitive small-file work, prefer <strong>ephemeralStorage</strong> + S3 archive, or step to EBS-on-EC2-launch. EFS shines for shared-state RWX, not raw IOPS."),
    ],
    quizzes=[
        Quiz(
            prompt="An ECS Task Definition mounts an EFS access point but Tasks fail to start with \"Could not mount EFS: timed out\". The execution role policy looks correct. What else?",
            answer="Check in this order: (1) <strong>EFS mount targets exist in the AZs the Tasks land in</strong> (one per AZ in the VPC). (2) <strong>Mount target SG allows NFS (TCP 2049) from the Task SGs</strong>. (3) <strong>Task subnet route table</strong> can reach the mount target ENI. (4) <strong>Access point still exists + IAM auth enabled</strong>. (5) <strong>transitEncryption</strong> matches the access point\'s settings — mismatch produces silent timeouts. The most common cause is SG: mount target SG is shared by the EFS service and frequently overlooked when adding a new Task SG.",
        ),
        Quiz(
            prompt="The team wants to move from bind-mounts on EC2 to EFS to enable Fargate. What\'s the migration path for an existing service holding 200 GiB of state?",
            answer="(1) <strong>Provision EFS</strong> + access point in the target VPC, mount targets in each AZ. (2) <strong>One-time copy</strong>: spin up an EC2 instance that mounts both the existing bind path and the new EFS access point; rsync the data. (3) <strong>Update Task Definition</strong>: replace the bind-mount volume with an efsVolumeConfiguration; same containerPath via mountPoints. (4) <strong>Cutover</strong> — UpdateService to the new revision. (5) <strong>Validate</strong> — Tasks restart, see EFS-mounted contents at the same path. (6) <strong>Decommission</strong> the old bind-mount EC2 capacity. Add deployment circuit breaker so a bad migration auto-rolls back.",
        ),
        Quiz(
            prompt="The CFO sees the EFS bill: \"$300/month for storage that\'s mostly idle. Switch to bind mounts.\" Defend EFS.",
            answer="\"<strong>Three reasons EFS stays:</strong> (1) <strong>RWX cross-AZ</strong> — bind mounts are single-host; we\'d give up the multi-AZ resilience of running Tasks in three subnets. (2) <strong>State doesn\'t move with Tasks</strong> — when ECS reschedules a Task to a different host (instance replacement, autoscaling, deploy), bind-mount state is gone; that\'s how we lost a customer\'s data the last time we tried this. (3) <strong>EFS Infrequent Access (IA) storage class</strong> auto-tiers cold files to ~$0.025/GB-month; we can flip that on and reduce ~70% of the bill without changing the architecture. <strong>The architectural property of EFS — that any Task on any host in any AZ sees the same filesystem — is why we\'re using it. Bind mounts trade away that property for $200/month savings, and we\'ve done that experiment before.</strong>\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CFO",
        ),
    ],
    glossary=[
        GlossaryItem(name="ephemeralStorage", definition="Per-Task scratch disk. Fargate default 20 GiB, max 200 GiB. EC2 launch uses host disk."),
        GlossaryItem(name="bind mount", definition="Task-level volume pointing to an EC2 host path. EC2-launch only; host-coupled; legacy."),
        GlossaryItem(name="Docker volume", definition="Task-level volume using a Docker volume driver (local, REX-Ray/EBS). EC2-launch only; legacy."),
        GlossaryItem(name="EFS", definition="Managed NFSv4 filesystem. RWX-equivalent across many Tasks and AZs; mount targets per AZ."),
        GlossaryItem(name="EFS access point", definition="Managed entrypoint into an EFS filesystem with path + POSIX UID/GID + permissions. Per-workload isolation."),
        GlossaryItem(name="EFS IAM auth", definition="elasticfilesystem:ClientMount/ClientWrite on the FS or access point — replaces NFS host-level auth."),
        GlossaryItem(name="EFS mount target", definition="ENI per AZ that Tasks connect to (NFS port 2049). One per AZ in the filesystem\'s VPC."),
        GlossaryItem(name="FSx for Windows File Server", definition="Managed SMB share with AD integration. For Windows containers needing SMB."),
        GlossaryItem(name="FSx for NetApp ONTAP", definition="Multi-protocol enterprise file storage (NFS / SMB / iSCSI) with snapshots, dedup, replication."),
        GlossaryItem(name="ephemeralStorageKmsKeyId", definition="Optional Task Definition field for customer-managed KMS key encrypting Fargate ephemeralStorage."),
    ],
    recap_lead="Five storage shapes; pick by lifetime + sharing. Ephemeral for per-Task scratch (size it!), EFS for shared-state RWX, FSx for Windows / ONTAP specialty. Bind mounts and Docker volumes are EC2-only legacy.",
    recap_next='<strong>Next — C6: ECS Deployment and Scaling.</strong> Rolling updates (deploymentConfiguration, minimumHealthyPercent, maximumPercent); circuit breaker; rollback. Blue/green via CodeDeploy; external deployment controller. Service Auto Scaling. Cluster auto scaling (capacity providers with managed scaling). Placement constraints + strategies.',
)
