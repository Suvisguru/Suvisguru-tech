"""K-ECS C2 — Task Definitions and Containers."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Task Definition shape — family + revision, containers, volumes, two IAM roles.">
  <rect x="20" y="20" width="720" height="200" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Cargo Manifests · K-Harbor — one immutable JSON, every Task is a stamped copy</text>
  <rect x="40" y="70" width="220" height="140" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="150" y="96" text-anchor="middle" font-size="13" font-weight="700" fill="#FBF1D6">Task Definition</text>
  <text x="150" y="116" text-anchor="middle" font-size="10" fill="#FBF1D6">family: my-app</text>
  <text x="150" y="132" text-anchor="middle" font-size="10" fill="#FBF1D6">revision: 42 (immutable)</text>
  <text x="150" y="150" text-anchor="middle" font-size="10" fill="#FBF1D6">CPU + memory at task level</text>
  <text x="150" y="166" text-anchor="middle" font-size="10" fill="#FBF1D6">network mode: awsvpc</text>
  <text x="150" y="186" text-anchor="middle" font-size="10" fill="#FBF1D6">ephemeralStorage / runtimePlatform</text>
  <rect x="280" y="70" width="220" height="60" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="390" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">container: app</text>
  <text x="390" y="108" text-anchor="middle" font-size="9" fill="#1F2433">image, ports, env, healthCheck, dependsOn</text>
  <rect x="280" y="150" width="220" height="60" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="390" y="172" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">container: log-router</text>
  <text x="390" y="188" text-anchor="middle" font-size="9" fill="#1F2433">Firelens sidecar — Fluent Bit</text>
  <rect x="520" y="70" width="200" height="60" rx="10" fill="#FBE8DC" stroke="#A04832"/>
  <text x="620" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#A04832">execution role</text>
  <text x="620" y="108" text-anchor="middle" font-size="9" fill="#A04832">ECR pull + Secrets fetch + logs</text>
  <rect x="520" y="150" width="200" height="60" rx="10" fill="#7AB3CC" stroke="#1F2433"/>
  <text x="620" y="172" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">task role</text>
  <text x="620" y="188" text-anchor="middle" font-size="9" fill="#FBF1D6">app → S3, DynamoDB, etc.</text>
</svg>"""


LESSON = LessonSpec(
    num="02",
    title_short="task definitions & containers",
    title_full="C2 · Task Definitions and Containers",
    title_html="K-ECS C2 · Task Definitions and Containers",
    module_eyebrow="Module C2 · the Cargo Manifests — one immutable JSON, every Task is a stamped copy",
    hero_sub_html='Task Definition is the <em>cargo manifest</em>: a versioned JSON spec that completely describes a Task. Each change creates a new <strong>revision</strong> (e.g., <code>my-app:42</code>) — old revisions stay around for rollback. The shape: <em>family + revision</em>, <em>network mode</em>, <em>CPU + memory at task level</em>, <em>ephemeralStorage</em> + <em>runtimePlatform</em>, an array of <em>containerDefinitions</em>, an array of <em>volumes</em>, and two IAM roles (<em>execution role</em> for launch-time AWS access, <em>task role</em> for runtime app access).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A migration ran <code>register-task-definition</code> with the wrong CPU number — 256 instead of 2048. The new revision rolled out; every Task hit the lower CPU cap; latency 10×; ALB target health flapped. <em>You can\'t edit a Task Definition revision in place — they\'re immutable.</em> You register a new revision with the correct value and update the Service. Today\'s lesson: get the cargo manifest right the first time and know exactly which fields are which.",
    stamp_html="<strong>Task Definitions are immutable; every change is a new revision. Two IAM roles: execution (image pull + secrets + logs) vs task (your app\'s AWS calls). awsvpc is the recommended network mode for almost every Task. Sidecars share the Task\'s network namespace + task-level volumes via mountPoints.</strong>",
    district_pin="kh-pier02",
    district_label="Cargo Manifests",
    sections=[
        Section(
            eyebrow="Section 1.1 · Task Definition top-level fields",
            h2="family, revision, network mode, CPU + memory, ephemeralStorage, runtimePlatform",
            body_html="""    <p><strong>family + revision</strong>: each Task Definition has a <code>family</code> name (e.g., <code>my-app</code>) and a monotonic <code>revision</code> number per family (1, 2, 3, …). Reference as <code>my-app:42</code>. Revisions are <em>immutable</em> — you never edit; you register a new revision. Old revisions remain queryable + usable for rollback (until DEREGISTER + the cleanup grace period).</p>
    <p><strong>networkMode</strong>: <code>awsvpc</code> (recommended; ENI per Task; SG per Task), <code>bridge</code> (Docker bridge — EC2-launch only; legacy), <code>host</code> (Task uses host network — EC2-launch; collisions if multiple Tasks bind the same port), <code>none</code> (no network). Fargate <em>requires</em> awsvpc.</p>
    <p><strong>cpu + memory</strong>: declared at <em>task level</em> (the sum across all containers) and optionally per-container. Fargate has a fixed CPU/memory matrix (256/0.5GB up to 16384/120GB); EC2 launch lets you specify any combination that fits the host. Per-container <code>memoryReservation</code> is a soft limit; <code>memory</code> is the hard limit. Per-container <code>cpu</code> is a relative weight (units), not a hard cap unless paired with cgroup limits.</p>
    <p><strong>ephemeralStorage</strong>: Fargate Tasks get <em>20 GiB default</em> ephemeral storage; bumpable up to 200 GiB via <code>ephemeralStorage.sizeInGiB</code>. EC2 launch: ephemeral storage is the host disk path (no per-Task quota by default).</p>
    <p><strong>runtimePlatform</strong>: <code>operatingSystemFamily</code> (LINUX, WINDOWS_SERVER_2019_FULL/CORE, WINDOWS_SERVER_2022_FULL/CORE) + <code>cpuArchitecture</code> (X86_64, ARM64). ARM64 + Graviton is materially cheaper for compatible workloads — pick early.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · containerDefinitions",
            h2="image, ports, env, secrets, dependsOn, healthCheck, logConfiguration, ulimits, linuxParameters",
            body_html="""    <p><strong>image</strong>: <code>account.dkr.ecr.region.amazonaws.com/repo:tag</code> (or public registry). Pinned digests (<code>@sha256:…</code>) preferred over mutable tags for production.</p>
    <p><strong>portMappings</strong>: array of <code>{containerPort, hostPort, protocol}</code>. With awsvpc network mode <code>hostPort</code> must equal <code>containerPort</code>. ALB target groups bind to <code>containerPort</code> via target type IP.</p>
    <p><strong>environment + secrets</strong>: plain <code>environment</code> for non-sensitive values; <code>secrets</code> array for values fetched from <strong>Secrets Manager</strong> or <strong>SSM Parameter Store</strong> at Task launch (the execution role policy must allow the fetch). Secrets are injected as env vars in the running container — never logged + KMS-encrypted in transit.</p>
    <p><strong>dependsOn</strong>: lists other containers in the same Task that must reach a state (<code>START</code>, <code>COMPLETE</code>, <code>SUCCESS</code>, <code>HEALTHY</code>) before this one starts. Use for sidecar boot order (e.g., the app waits for the log-router to be HEALTHY).</p>
    <p><strong>healthCheck</strong>: command + interval + timeout + retries + startPeriod. Reports container health to ECS; ALB target health is separate (HTTP probe by ALB).</p>
    <p><strong>logConfiguration</strong>: <em>awslogs</em> (CloudWatch — default), <em>awsfirelens</em> (route via Firelens sidecar to anywhere), <em>splunk</em>, <em>fluentd</em>, <em>journald</em>. Production default = awsfirelens for routing flexibility; awslogs for simplicity.</p>
    <p><strong>ulimits + linuxParameters</strong> <span class="skip-tag">[ deep dive — skip if new ]</span>: ulimits set RLIMIT_NOFILE etc.; linuxParameters configures capabilities, devices, sharedMemorySize, swappiness, init process. Touch only when a workload demands it.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · volumes",
            h2="bind mounts, Docker volumes, EFS, FSx for Windows / ONTAP",
            body_html="""    <p><strong>volumes</strong> are declared at the Task Definition top level and <em>mounted</em> by containers via <code>mountPoints</code> (<code>{containerPath, sourceVolume, readOnly}</code>). Five flavours:</p>
    <ul>
      <li><strong>Bind mount</strong> — host path on the EC2 instance (EC2 launch only). Cheap, fast, host-coupled. Lost when Task moves hosts.</li>
      <li><strong>Docker volume</strong> — Docker plugin volume on EC2 host (e.g., REX-Ray, EBS-bound via plugin). EC2 launch only.</li>
      <li><strong>EFS</strong> — managed NFSv4 filesystem; <strong>RWX-equivalent</strong> across many Tasks and AZs; supports IAM-based authorization + EFS access points (path + UID/GID + permission isolation per Task). The shared-state answer for ECS.</li>
      <li><strong>FSx for Windows File Server</strong> — for Windows Tasks needing SMB share. Configure in Task Definition with <code>fsxWindowsFileServerVolumeConfiguration</code>.</li>
      <li><strong>FSx for NetApp ONTAP</strong> — NFS-attach for higher-tier file storage (multi-protocol, snapshots, replication). Configure via <code>fsxWindowsFileServerVolumeConfiguration</code>-style block (FSx ONTAP is treated similarly).</li>
    </ul>
    <p><strong>Sharing volumes between containers</strong>: declare the volume once at Task level; multiple containers list the same <code>sourceVolume</code> in their <code>mountPoints</code>. Classic use: app container writes to <code>/var/log/app</code>; Firelens sidecar reads from the same mount and ships off-host.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · sidecars + task-level volumes + the two IAM roles",
            h2="Sidecars share the Task; execution role vs task role",
            body_html="""    <p><strong>Sidecars</strong>: a Task can have multiple containers — one app + one or more sidecars (log router, proxy, observability collector, init helper). Sidecars share the Task\'s <em>network namespace</em> (in awsvpc mode they share the same ENI), Task-level volumes, lifecycle (one container stop → whole Task stops if <code>essential: true</code>), and IAM via the task role.</p>
    <p><strong>essential</strong>: container-level boolean; if <code>true</code> (default for the app) and that container exits, the whole Task is stopped (with <code>stoppedReason</code> = "Essential container in task exited"). Sidecars that should crash without taking the Task down get <code>essential: false</code> — but log routers usually stay <code>essential: true</code> so log loss surfaces fast.</p>
    <p><strong>Execution role</strong>: assumed by the <em>ECS agent / Fargate</em> at Task launch to do <em>infrastructure</em> things — pull image from ECR, fetch Secrets Manager / SSM values, send container logs to CloudWatch. <code>AmazonECSTaskExecutionRolePolicy</code> is the AWS-managed baseline. Add KMS Decrypt for the Secrets KMS key. <em>The execution role is launch-time scaffolding; the running app does NOT use it.</em></p>
    <p><strong>Task role</strong>: assumed by the <em>application code</em> at runtime via the ECS metadata endpoint. Grants the app permission to call AWS APIs (e.g., S3 Put, DynamoDB UpdateItem). <strong>Always least-privilege</strong>: scope to the specific resources + actions the app actually performs. Default to denying everything else.</p>
    <p><em>Different roles, different policies, different lifecycles.</em> Forgetting which is which is the most common ECS-IAM bug.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A team registered <code>my-app:43</code> with the wrong CPU number, then realised. What\'s the fix?",
            options=[
                ("Edit revision 43 in place to correct the value.", False),
                ("Register revision 44 with the correct value, then UpdateService to use 44.", True),
                ("Delete revision 43 to fall back to 42.", False),
            ],
            feedback="Task Definition revisions are immutable. Register a new revision with the correct value and roll forward. The bad revision can be DEREGISTERed once nothing references it.",
        ),
        3: PauseCheck(
            question="Which IAM role lets a running container call S3 PutObject?",
            options=[
                ("Task execution role.", False),
                ("Task role.", True),
                ("ECS agent\'s host EC2 role.", False),
            ],
            feedback="The task role is what the running app code assumes via the ECS metadata endpoint. Execution role is launch-time scaffolding (image pull, secrets, logs). Get this distinction wrong and your app gets either too much or too little permission.",
        ),
    },
    before_after_before='<p>Pre-immutable Task Definitions, teams edited live container configs by SSHing into hosts. Drift was constant. Rolling back meant remembering what the previous shape was. Sidecars that should have run alongside the app were skipped or run as separate ECS Tasks (no shared volumes; no shared lifecycle). Secrets were baked into images or stuffed into env vars committed to source. The execution-role / task-role distinction wasn\'t in the pattern; teams gave the app every permission the agent had.</p>',
    before_after_after='<p>Modern Task Definitions are immutable JSON, versioned per change. Sidecars are first-class — share network and volumes; the app + log-router + envoy / agent run as one Task. Secrets are fetched at launch from Secrets Manager / SSM; KMS-encrypted; not in source. The execution role / task role split keeps launch-time AWS access separate from runtime app access. Rolling back is "UpdateService to revision N-1." <em>The cargo manifest is the source of truth; everything else is derived.</em></p>',
    before_after_caption='<p class="ba-caption"><em>The Task Definition is the only thing you really write for a workload. Get its shape right and most of the rest follows.</em></p>',
    analogy_intro_html='''<p>Down at the harbor, every ship\'s captain checks in at <strong>Cargo Manifests</strong>. The manifest is a stamped numbered form: family name (<em>"my-app"</em>), revision number (<em>42</em>), the type of ship (LINUX or WINDOWS, X86_64 or ARM64), how much cargo (CPU + memory), how much spare deck (ephemeralStorage), and what kind of berth wiring (network mode).</p>
    <p>Inside the manifest is the <strong>cargo list</strong> — every container you\'re putting on the ship. For each container: which warehouse to fetch it from (image), what doors open out (portMappings), what crew badges go inside (environment + secrets), what shipboard rituals must finish first (dependsOn), how the medic reports its health (healthCheck), and where its logs are funnelled (logConfiguration).</p>
    <p>The captain hands the form to the harbor master with two signed letters of authority. The first is for <em>boarding day only</em> — it\'s how the dock crew unlock the ECR warehouse and the secrets vault to load the ship before sailing (<strong>execution role</strong>). The second is what the captain carries on the voyage and uses to call ahead to ports along the way (<strong>task role</strong>). Different letters, different scopes. The dock crew never use the captain\'s voyage letter; the captain never uses the boarding-day letter.</p>''',
    translation_rows=[
        ("Stamped numbered form", "Task Definition (immutable revision)"),
        ("Family name + form number", "family + revision (e.g., my-app:42)"),
        ("Ship type (Linux/Windows × arch)", "runtimePlatform (operatingSystemFamily, cpuArchitecture)"),
        ("How much cargo + spare deck", "CPU + memory + ephemeralStorage"),
        ("Berth wiring", "networkMode (awsvpc / bridge / host / none)"),
        ("Cargo list (per container)", "containerDefinitions array"),
        ("Warehouse address", "image (e.g., ECR URI)"),
        ("Crew badges, sealed", "environment + secrets (Secrets Manager / SSM)"),
        ("Shipboard rituals before sailing", "dependsOn (container startup ordering)"),
        ("Medic\'s health checks", "healthCheck command"),
        ("Log funnel", "logConfiguration (awslogs / awsfirelens / etc.)"),
        ("Boarding-day letter (dock crew)", "task execution role — image pull + secrets + logs"),
        ("Voyage letter (captain carries)", "task role — app\'s AWS calls at runtime"),
        ("Shared deck space", "Task-level volumes + container mountPoints"),
    ],
    analogy_stops="A real cargo ship\'s manifest is paper and changes during the voyage if needed. ECS Task Definition revisions are <em>completely</em> immutable — you never edit; you register a new revision. Even a typo means revision N+1.",
    eli5="Every running ship in the harbor is a copy of a stamped form called a Task Definition. The form has the ship\'s family name, a number, what cargo to load, what cargo doors open, who can fetch the cargo from the warehouse, and what the cargo can do once it\'s sailing. You can\'t edit a stamped form. If something\'s wrong, you stamp a new one.",
    eli10="A Task Definition is JSON: <code>family</code> + <code>revision</code> (immutable per change), <code>networkMode</code> (awsvpc recommended), <code>cpu</code> + <code>memory</code> at task level, <code>ephemeralStorage</code>, <code>runtimePlatform</code>, an array of <code>containerDefinitions</code> (image, ports, env + secrets, dependsOn, healthCheck, logConfiguration, ulimits, linuxParameters), an array of <code>volumes</code> (bind / Docker / EFS / FSx), and two IAM roles — <strong>execution role</strong> (launch-time: pull ECR + fetch Secrets + write logs) and <strong>task role</strong> (runtime: the app\'s AWS calls). Sidecars share the Task\'s ENI + volumes + lifecycle; <code>essential</code> per container controls whether one container exit stops the whole Task.",
    scenarios=[
        Scenario(
            name="API + Firelens sidecar — log routing without an agent on every host",
            body="A 60-engineer SaaS runs a Node.js API. Task Definition has two containers: <strong>app</strong> (essential: true, logConfiguration: awsfirelens) + <strong>log-router</strong> (Fluent Bit, essential: true, logConfiguration: awslogs). App stdout flows to the sidecar; sidecar routes to OpenSearch + S3 archive. <em>No daemonset, no host agents — Task carries its own logging.</em>",
        ),
        Scenario(
            name="ARM64 cost win — Graviton retrofit",
            body="A 25-engineer team flipped <code>cpuArchitecture</code> from <code>X86_64</code> to <code>ARM64</code> + rebuilt their Node + Java images for arm64. Fargate Graviton pricing is ~20% lower per vCPU-hour; image sizes are similar; perf is competitive on most non-AVX workloads. <em>One config flip + a multi-arch image build saved ~$2k/month.</em>",
        ),
        Scenario(
            name="Stateful migration — adding EFS to a Task",
            body="A team migrating a legacy uploader to ECS. The app expects local <code>/var/uploads</code> — but they need state to persist across Task restarts and to be shared with a periodic-cleanup Task. Task Definition gets a <code>volumes</code> entry pointing to an EFS access point; both Task Definitions mount it via <code>mountPoints</code>. <em>RWX shared state without redesigning the app.</em>",
        ),
        Scenario(
            name="IAM bug — execution role given S3 access; app couldn\'t Put",
            body="An on-call engineer added <code>s3:PutObject</code> to the execution role (intending to grant runtime access). Task launched fine but app calls returned AccessDenied. The fix: move the policy to the <em>task role</em>. <em>Execution role does launch-time AWS work; task role is what the running container assumes.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"You can edit a Task Definition revision after it\'s registered.\"",
            truth="No. Revisions are <strong>immutable</strong>. Each change registers a new revision (e.g., 42 → 43). Old revisions stay queryable and usable for rollback until DEREGISTER. This is intentional — it\'s what makes rollbacks deterministic.",
        ),
        Misconception(
            myth="\"Execution role and task role are the same; ECS just renamed it.\"",
            truth="Different roles, different lifecycles. <strong>Execution role</strong> is assumed by the agent / Fargate <em>at launch time</em> to pull images, fetch secrets, write logs. <strong>Task role</strong> is assumed by the <em>running container code</em> via the ECS metadata endpoint, granting the app its AWS API permissions. The split exists so the app never sees the launch-time credentials.",
        ),
        Misconception(
            myth="\"Sidecar containers run as separate Tasks.\"",
            truth="No. Sidecars are additional containers <em>inside the same Task</em> — they share the Task\'s ENI (in awsvpc), Task-level volumes, lifecycle, and the same task role. ECS schedules and stops them together. Putting a sidecar in a separate Task loses all of that.",
        ),
    ],
    flashcards=[
        Flashcard(front="What does immutable mean for Task Definitions?", back="Once registered, a revision\'s contents never change. Each change is a new revision (my-app:42 → my-app:43). Old revisions stay around for rollback. UpdateService points the Service at the new revision."),
        Flashcard(front="Four ECS network modes — and which is recommended?", back="<strong>awsvpc</strong> (recommended; ENI per Task; SG per Task; required for Fargate), <strong>bridge</strong> (Docker bridge; EC2-launch legacy), <strong>host</strong> (host network; collisions if multiple Tasks bind same port), <strong>none</strong> (no network)."),
        Flashcard(front="Where does ephemeralStorage live and what\'s the Fargate default + max?", back="In Task Definition top-level <code>ephemeralStorage.sizeInGiB</code>. Fargate default = <strong>20 GiB</strong>; bumpable to <strong>200 GiB</strong>. EC2 launch uses host disk."),
        Flashcard(front="What does runtimePlatform let you set?", back="<code>operatingSystemFamily</code> (LINUX, WINDOWS_SERVER_2019 / 2022 FULL/CORE) and <code>cpuArchitecture</code> (X86_64 or ARM64 — Graviton). Pick ARM64 for cost wins on compatible workloads."),
        Flashcard(front="Two ways to inject Secrets into a container?", back="<code>secrets</code> array with valueFrom = Secrets Manager ARN or SSM parameter ARN. Execution role policy must allow Secrets Manager / SSM Get + KMS Decrypt for the encryption key. Injected as env vars at launch; not logged."),
        Flashcard(front="What does dependsOn do?", back="Container-level field listing other containers in the same Task and the state they must reach (START / COMPLETE / SUCCESS / HEALTHY) before this container starts. Use for sidecar boot order — app waits for log-router HEALTHY."),
        Flashcard(front="EFS for ECS — what\'s the win?", back="Managed NFSv4 filesystem; <strong>RWX-equivalent</strong> across many Tasks and AZs; IAM-based authorization; access points isolate path + UID/GID + perms per Task. Use for shared state, uploads, durable on-Task-restart storage."),
        Flashcard(front="Three logConfiguration options most teams use?", back="<strong>awslogs</strong> (CloudWatch — default, simple), <strong>awsfirelens</strong> (route via Firelens sidecar to anywhere — OpenSearch / Kinesis / S3 / Splunk), <strong>splunk / fluentd / journald</strong> (specific destinations). Production default for flexibility = awsfirelens."),
    ],
    quizzes=[
        Quiz(
            prompt="A Task Definition with two containers (app + Firelens) is failing — the app starts but Firelens sidecar exits within 5 seconds with \"Could not fetch logs\". Where do you look first?",
            answer="The Firelens sidecar is failing because it can\'t talk to the destination AWS service (OpenSearch / Kinesis / etc.). Two checks in order: (1) <strong>Task role</strong> permissions — the running Firelens container uses the task role to call the destination service; missing perms = silent fail. Add <code>opensearch:ESHttp*</code> or equivalent. (2) <strong>VPC connectivity</strong> — if the destination is in a private VPC and the Task is in an isolated subnet, ensure VPC endpoints (or NAT gateway egress) exist for the destination service. Logs from the sidecar itself land in CloudWatch via the sidecar\'s <em>own</em> awslogs configuration — start there.",
        ),
        Quiz(
            prompt="The team wants per-container CPU caps so a runaway sidecar can\'t starve the app. Where do they configure that?",
            answer="Per-container <code>cpu</code> in containerDefinitions is a <em>relative weight</em>, not a hard cap (Linux cpu shares semantics). For a <strong>hard limit</strong> use <code>cpuShares</code> + <code>memoryReservation</code> (soft floor) and <code>memory</code> (hard cap). At the Linux cgroup level, ECS doesn\'t expose <code>cpu_quota_us</code> directly — but on Fargate the Task\'s overall CPU is capped by the Task-level <code>cpu</code> field, and the per-container weights divide that. The cleanest answer: <strong>tune at Task level</strong> (set Task <code>cpu</code> to enough total + per-container <code>cpu</code> weights to bias toward app), and accept that ECS doesn\'t implement K8s-style hard CPU limits per container without leaving the orchestrator.",
        ),
        Quiz(
            prompt="An on-call engineer wires <code>s3:PutObject</code> into the task <em>execution</em> role (instead of the task role) and pushes a deploy. The app continues to fail PutObject calls. They escalate after 90 minutes. What was the fix and why does this confuse so many engineers?",
            answer="<strong>Fix:</strong> move the policy from execution role to task role; leave the execution role with only image pull + secrets + logs. <strong>Why the confusion:</strong> both are \"task IAM\" in the docs sidebar, both attach to a Task Definition, both involve assume-role chains. The mental model that locks it in: <em>execution role is the dock crew loading your ship at launch; task role is the captain on the voyage</em>. Dock crew never sail; the captain never unloads cargo at boarding. Forgetting this costs hours every quarter on every team.",
            cyoa=True,
            cyoa_tag="how the on-call engineer learned the difference",
        ),
    ],
    glossary=[
        GlossaryItem(name="Task Definition family", definition="The named series of related Task Definition revisions (e.g., my-app). Revisions are numbered within a family."),
        GlossaryItem(name="Task Definition revision", definition="One immutable JSON spec, monotonically numbered per family. New revision per change."),
        GlossaryItem(name="awsvpc network mode", definition="ENI per Task; SG per Task. Required for Fargate; recommended for EC2 launch."),
        GlossaryItem(name="ephemeralStorage", definition="Per-Task scratch disk. Fargate default 20 GiB → max 200 GiB."),
        GlossaryItem(name="runtimePlatform", definition="operatingSystemFamily (LINUX / WINDOWS variants) + cpuArchitecture (X86_64 / ARM64)."),
        GlossaryItem(name="containerDefinitions", definition="Array of containers in a Task — image, ports, env, secrets, dependsOn, healthCheck, logConfiguration, ulimits, linuxParameters."),
        GlossaryItem(name="dependsOn", definition="Container-level: this container waits until another reaches START / COMPLETE / SUCCESS / HEALTHY."),
        GlossaryItem(name="essential", definition="Container-level boolean. If true and that container exits, the whole Task stops with stoppedReason = Essential container exited."),
        GlossaryItem(name="execution role", definition="IAM role assumed by ECS agent / Fargate at Task launch — image pull, fetch Secrets, write CloudWatch logs."),
        GlossaryItem(name="task role", definition="IAM role assumed by running container code via ECS metadata endpoint — the app\'s AWS API permissions."),
        GlossaryItem(name="EFS access point", definition="Managed entrypoint into an EFS filesystem with path + POSIX UID/GID + permissions; isolates Tasks."),
        GlossaryItem(name="awsfirelens", definition="logDriver routing container logs through a Firelens sidecar (Fluent Bit / Fluentd) to anywhere — OpenSearch, S3, Kinesis, Splunk."),
    ],
    recap_lead="Task Definitions are immutable JSON manifests. Get the network mode right (awsvpc), CPU + memory + ephemeralStorage sized, the right runtimePlatform (Graviton if compatible), the containerDefinitions correct (especially dependsOn + healthCheck + logConfiguration), the volumes wired to mountPoints across containers, and the two IAM roles separated cleanly — execution for launch, task for runtime.",
    recap_next='<strong>Next — C3: ECS Networking.</strong> Network modes (bridge, host, awsvpc — recommended, none); awsvpc ENI per Task + SG per Task; Service Connect (modern east-west); Service Discovery via Cloud Map; ALB + NLB integration with target type IP; VPC Lattice for ECS.',
)
