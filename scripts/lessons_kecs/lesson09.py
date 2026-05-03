"""K-ECS C9 — Troubleshooting."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS troubleshooting — stuck PENDING, stoppedReason taxonomy, circuit breaker, target health.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Salvage Office · K-Harbor — read the chain top-down</text>
  <rect x="40" y="70" width="170" height="120" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">stuck PENDING</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#1F2433">ENI provisioning</text>
  <text x="125" y="124" text-anchor="middle" font-size="9" fill="#1F2433">image pull (ECR auth)</text>
  <text x="125" y="144" text-anchor="middle" font-size="9" fill="#1F2433">execution role + KMS</text>
  <text x="125" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">read describe-tasks</text>
  <rect x="225" y="70" width="170" height="120" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">stoppedReason</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#FFFFFF">CannotPullContainerError</text>
  <text x="310" y="124" text-anchor="middle" font-size="9" fill="#FFFFFF">ResourceInitializationError</text>
  <text x="310" y="144" text-anchor="middle" font-size="9" fill="#FFFFFF">OutOfMemoryError</text>
  <text x="310" y="160" text-anchor="middle" font-size="9" fill="#FFFFFF">Essential exited</text>
  <text x="310" y="180" text-anchor="middle" font-size="9" font-style="italic" fill="#FFFFFF">exit code in detail</text>
  <rect x="410" y="70" width="170" height="120" rx="10" fill="#3878B5" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">circuit breaker fires</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#FFFFFF">deploy halted</text>
  <text x="495" y="124" text-anchor="middle" font-size="9" fill="#FFFFFF">auto-rollback to prior rev</text>
  <text x="495" y="144" text-anchor="middle" font-size="9" fill="#FFFFFF">CloudWatch alarm</text>
  <text x="495" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FFFFFF">read deployment events</text>
  <rect x="595" y="70" width="125" height="120" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">target health</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#1F2433">ALB / NLB</text>
  <text x="657" y="124" text-anchor="middle" font-size="9" fill="#1F2433">SG / port / path</text>
  <text x="657" y="144" text-anchor="middle" font-size="9" fill="#1F2433">grace period</text>
  <text x="657" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">ECS Exec for live</text>
</svg>"""


LESSON = LessonSpec(
    num="09",
    title_short="ECS troubleshooting",
    title_full="C9 · ECS Troubleshooting — Stuck Tasks, Stopped Reasons, Deploy Failures",
    title_html="K-ECS C9 · ECS Troubleshooting",
    module_eyebrow="Module C9 · Salvage Office — read the chain top-down",
    hero_sub_html='Four families of ECS failure: <strong>stuck PROVISIONING / PENDING</strong> (ENI, image pull, IAM, KMS), <strong>STOPPED with a reason code</strong> (CannotPullContainerError / ResourceInitializationError / OutOfMemoryError / Essential container exited / explicit exit codes), <strong>deploy failures</strong> (circuit breaker fired, CodeDeploy alarm tripped), and <strong>Service Connect / ALB target health failures</strong> (SG, port, path mismatch, slow startup). The fastest debug path: read the chain top-down — describe-tasks → stoppedReason → events → CloudWatch logs → ECS Exec into a Task — and stop the moment the cause is identified.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A Service is at 4/10 desired Tasks; 6 Tasks are stuck PENDING. The on-call engineer reads the events tab on the ECS console; sees \"Service was unable to place a task because no container instance met all of its requirements.\" <em>The error message is generic; the root cause could be any of five different things.</em> Today\'s lesson: a methodical top-down chain to find any ECS failure cause in under 10 minutes.",
    stamp_html="<strong>Read top-down: describe-tasks → stoppedReason → service events → CloudWatch logs → ECS Exec. Each step narrows the cause class. Stop reading the moment the cause is identified — most ECS failures are in the first three categories: ENI / image pull / IAM-KMS.</strong>",
    district_pin="kh-pier09",
    district_label="Salvage Office",
    sections=[
        Section(
            eyebrow="Section 1.1 · stuck PROVISIONING / PENDING",
            h2="ENI, image pull, IAM, KMS — the launch-time failure quartet",
            body_html="""    <p>A Task in PROVISIONING / PENDING for &gt;2 minutes is unhappy. Four likely causes:</p>
    <ol>
      <li><strong>ENI provisioning stalled</strong> (awsvpc) — subnet has no free IPs (<code>VPC.IPAddressLimitExceeded</code>); VPC ENI limit hit per Region; SG references missing. Check: <code>describe-tasks</code> stoppedReason / lastStatus + VPC subnet free IP count + AWS Health Dashboard.</li>
      <li><strong>Image pull stalled / failed</strong> — execution role missing ECR perms; ECR repo policy denies; KMS key for ECR-encrypted repo missing Decrypt; private registry creds wrong (<code>repositoryCredentials</code>); registry network unreachable (no VPC endpoint or NAT). <em>stoppedReason: CannotPullContainerError</em> on the Task.</li>
      <li><strong>Execution role + KMS missed</strong> — execution role missing <code>secretsmanager:GetSecretValue</code> or <code>kms:Decrypt</code> on the secret\'s key. <em>stoppedReason: ResourceInitializationError: unable to retrieve secret value</em>.</li>
      <li><strong>Capacity unavailable</strong> — Service desired count exceeds available capacity in the chosen capacity provider (Fargate quota, EC2 ASG full, external instance count low). Service event: \"unable to place a task because no container instance met all requirements\".</li>
    </ol>
    <p><strong>First-look commands</strong>: <code>aws ecs describe-tasks --cluster X --tasks ID --query "tasks[].lastStatus,stoppedReason"</code> + <code>aws ecs describe-services --query "services[].events[:5]"</code>.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · STOPPED — the stoppedReason taxonomy",
            h2="Read the reason; take the matching action",
            body_html="""    <p><strong>Common stoppedReason values + their cause classes</strong>:</p>
    <ul>
      <li><strong>CannotPullContainerError</strong>: ECR / private registry pull failed. Look at the message tail: <em>"no basic auth credentials"</em> = repositoryCredentials wrong; <em>"manifest unknown"</em> = image tag/digest doesn\'t exist; <em>"AccessDenied"</em> = ECR repo policy or execution role IAM.</li>
      <li><strong>ResourceInitializationError</strong>: launch-time AWS resource fetch failed — Secrets Manager, SSM, KMS, log group create. The message tail names the failed resource.</li>
      <li><strong>OutOfMemoryError</strong>: container hit its memory hard limit. <em>Increase the Task or container <code>memory</code></em>, or fix the leak.</li>
      <li><strong>Essential container in task exited</strong>: an essential container exited with non-zero code; whole Task stopped. Check the container\'s <em>exit code + last log lines</em>.</li>
      <li><strong>Health check failed</strong>: container healthCheck reported unhealthy past the configured retries. Tighten or loosen the healthCheck spec; verify the command works against the container\'s actual entrypoint.</li>
      <li><strong>USER_INITIATED</strong>: someone (or a deploy / scale) explicitly stopped the Task. Not a failure.</li>
    </ul>
    <p><strong>Exit codes</strong>: container <code>exitCode</code> in <code>describe-tasks</code> shows the precise integer. 137 = SIGKILL (often OOM); 139 = SIGSEGV; 143 = SIGTERM (graceful stop). Map to your app\'s known exit-code conventions.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · deployment circuit breaker firings + CodeDeploy rollbacks",
            h2="A deploy halted itself — read why",
            body_html="""    <p>If the deployment <strong>circuit breaker</strong> fires, the Service rolls back to the previous Task Definition revision automatically. The <code>describe-services</code> events tab shows: \"deployment circuit breaker — service has been rolled back\". The root cause is upstream of that — <em>the new revision\'s Tasks failed health</em>. Look at the Tasks of the new (now-rolled-back) revision via <code>list-tasks --desired-status STOPPED</code> + read their stoppedReasons.</p>
    <p><strong>CodeDeploy blue/green rollback</strong>: AWS CodeDeploy console shows a Failed deployment with the alarm that tripped (e.g., \"5xxRate Alarm in ALARM state\"). Linear / canary deploys give you the partial-traffic snapshot before rollback — useful for understanding the failure mode. Hooks (BeforeAllowTraffic / AfterAllowTraffic Lambdas) emit logs in their own log groups; failed hook = failed deploy.</p>
    <p><strong>Common deployment failure patterns</strong>: (a) <em>app crashes on start</em> with new env / secret value (revert; verify config). (b) <em>health check fails</em> because new revision changed startup time (raise healthCheckGracePeriodSeconds). (c) <em>resource limits too tight</em> (revision changed CPU/memory; OOM at start; raise the limit). (d) <em>downstream dependency degraded</em> (new revision\'s integration test fails; not really a deploy failure but symptom shows there).</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · Service Connect / ALB target health failures + ECS Exec for live debug",
            h2="Tasks RUNNING but not serving traffic",
            body_html="""    <p>Task is RUNNING (container started, healthCheck passing) but <strong>ALB target health</strong> is unhealthy. Six causes in increasing rarity:</p>
    <ol>
      <li><strong>SG mismatch</strong> — Task SG doesn\'t allow inbound from ALB SG on the container port. (Most common.)</li>
      <li><strong>Wrong port</strong> — ALB target group port doesn\'t match the Task\'s containerPort.</li>
      <li><strong>Wrong path</strong> — ALB health check path returns non-200 (e.g., <code>/healthz</code> not implemented; redirects to <code>/</code>).</li>
      <li><strong>Slow startup</strong> — app takes &gt; ALB unhealthy threshold × interval to become ready; raise <code>healthCheckGracePeriodSeconds</code> on the Service.</li>
      <li><strong>App crashes on first health probe</strong> — check container logs.</li>
      <li><strong>Network ACLs / route table</strong> — uncommon; subnet config blocking ALB-to-Task path.</li>
    </ol>
    <p><strong>Service Connect endpoint failures</strong>: A Service can\'t reach <code>service-b.namespace</code>. (a) Service Connect not enabled on the consumer Service\'s Service-level config. (b) Consumer doesn\'t have the right namespace ARN in its serviceConnectConfiguration. (c) The Cloud Map namespace SG blocks. (d) The producer Service\'s Tasks are unhealthy and not registered in Service Connect.</p>
    <p><strong>ECS Exec for live debug</strong>: when the issue manifests inside the container (DNS resolution, downstream timeout, in-memory state), Exec into one of the running Tasks: <code>aws ecs execute-command --cluster X --task ID --container Y --command "/bin/sh" --interactive</code>. Run <code>nslookup</code> / <code>curl</code> / <code>netstat</code> / read in-memory state. Faster than restart-and-pray.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A Task is stuck PROVISIONING for 4 minutes. Which is the most actionable first command?",
            options=[
                ("aws ecs execute-command (start a debug shell).", False),
                ("aws ecs describe-tasks --cluster X --tasks ID — read lastStatus + stoppedReason.", True),
                ("Restart the Service via UpdateService.", False),
            ],
            feedback="describe-tasks is the first read in any ECS debug. lastStatus + stoppedReason narrow the failure class to ENI / image pull / IAM-KMS / capacity in seconds.",
        ),
        3: PauseCheck(
            question="A Task is RUNNING and healthCheck is passing but ALB target health is Unhealthy. What\'s the most common cause?",
            options=[
                ("Container is OOMing.", False),
                ("Task SG doesn\'t allow inbound from the ALB SG on the container port.", True),
                ("ECS agent has lost connection.", False),
            ],
            feedback="SG mismatch is the #1 ALB target-health failure cause in awsvpc. Task SG must allow inbound from the ALB SG (specifically — not 0.0.0.0/0) on the container port.",
        ),
    },
    before_after_before='<p>Pre-circuit-breaker, pre-stoppedReason richness, ECS troubleshooting was: notice a Service is unhealthy → guess → restart → guess again. Logs went to CloudWatch but you had to know which log group; events on the Service tab were generic; ECS Exec didn\'t exist. Bad deploys ran to completion or hung at partial-healthy; manual rollback was a 30-minute investigation.</p>',
    before_after_after='<p>Modern ECS troubleshooting follows a chain: describe-tasks gives stoppedReason + exit code; describe-services events show capacity / scheduling failures; CloudWatch + Container Insights show the surrounding metrics; ECS Exec opens a live shell. Most issues are localised to one of four families (ENI, image pull, IAM/KMS, capacity) and surface in the first three commands. The deployment circuit breaker auto-rolls-back; CodeDeploy alarms drive blue/green rollback. <em>Diagnoses that took an hour now take five minutes.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Read the chain top-down. Don\'t debug-by-restart. Most ECS failures live in the first three categories — ENI, image pull, IAM-KMS — and the first three commands surface them.</em></p>',
    analogy_intro_html='''<p>The harbor\'s <strong>Salvage Office</strong> is where things that went wrong come for forensic review. The salvager (you) reads a chain of evidence top-down.</p>
    <p>First the <strong>boarding log</strong> (describe-tasks) — what state is the ship in? Stuck at boarding (PROVISIONING / PENDING) usually means: the customs official couldn\'t set up the radio mast (ENI provisioning), the warehouse couldn\'t hand over the cargo (ECR pull), or the boarding letter was missing the right stamps (IAM / KMS).</p>
    <p>Next the <strong>stop-reason slip</strong> (stoppedReason) — if the ship stopped in the harbor: \"could not pull container\" (warehouse problem), \"resource init error\" (vault / KMS problem), \"out of memory\" (cargo too heavy for the deck), \"essential container exited\" (the captain abandoned ship; check exit code), \"health check failed\" (the medic flunked the ship).</p>
    <p>Then the <strong>harbor events log</strong> (service events) — capacity issues like \"no berth available with the right wiring\" surface here. The <strong>signal officer\'s archive</strong> (CloudWatch logs) holds detailed context. Finally, the salvager can <strong>climb aboard</strong> a still-running but troubled ship (ECS Exec) to inspect the engine room directly — no SSH ladders, no boarding planks, the lighthouse opens an authenticated channel straight in.</p>
    <p>The technique is to read top-down and stop the moment the cause is identified. Most failures live in the first three categories — radio mast, warehouse, boarding letter.</p>''',
    translation_rows=[
        ("Salvage Office", "ECS troubleshooting layer"),
        ("Boarding log", "describe-tasks (lastStatus + stoppedReason)"),
        ("Stuck at radio-mast setup", "ENI provisioning stalled (subnet IPs / SG)"),
        ("Stuck at warehouse handover", "image pull (CannotPullContainerError)"),
        ("Stuck at boarding-letter check", "IAM / KMS (ResourceInitializationError)"),
        ("Stop-reason slip", "stoppedReason field"),
        ("Cargo too heavy for the deck", "OutOfMemoryError (memory limit)"),
        ("Captain abandoned ship", "Essential container in task exited (exit code)"),
        ("Medic flunked the ship", "Health check failed (container healthCheck)"),
        ("Harbor events log", "Service describe-services events"),
        ("Auto-cancel + revert", "deployment circuit breaker rollback"),
        ("Climb aboard the ship", "ECS Exec for live container debug"),
    ],
    analogy_stops="A real ship can have many simultaneous problems; ECS Tasks have one stoppedReason per stop event. The reason names the most-recent + most-specific cause; deeper context is in CloudWatch logs.",
    eli5="When a ship gets in trouble, the salvager reads four pieces of paper in order: the boarding log (where did it stop?), the stop-reason slip (why did it stop?), the harbor events (what was happening around it?), and the signal officer\'s archive (what was it saying?). Then if the ship is still floating, the salvager can climb aboard and look around inside.",
    eli10="Read top-down: <strong>describe-tasks</strong> → lastStatus + stoppedReason; <strong>describe-services</strong> → events for capacity / scheduling; <strong>CloudWatch logs</strong> → app + agent context; <strong>ECS Exec</strong> → live shell into a running container. Common stoppedReasons: <em>CannotPullContainerError</em> (image / IAM / KMS), <em>ResourceInitializationError</em> (Secrets / KMS / log group create), <em>OutOfMemoryError</em> (memory), <em>Essential container exited</em> (app crash; read exit code). Deploy failures: circuit breaker fires + auto-rollback; CodeDeploy alarm rollback. ALB target-health failures most often = SG mismatch.",
    scenarios=[
        Scenario(
            name="Image pull fail — KMS Decrypt missing on execution role",
            body="A Service\'s Tasks all stop with <em>CannotPullContainerError: failed to decrypt image manifest with KMS key arn:...</em>. Execution role had ecr:* on the repo but missed kms:Decrypt on the customer-managed KMS key the ECR repo was encrypted with. <em>Fix in 4 minutes</em> after reading the stoppedReason; would have been an hour of guesswork without it.",
        ),
        Scenario(
            name="OOM after Task Definition revision change",
            body="New revision raised the workload\'s baseline memory; container memory was unchanged; OOM at startup. stoppedReason: <em>OutOfMemoryError: Container killed due to memory usage</em>. Bumped Task Definition memory from 512 to 1024 MiB; new revision; ran clean. Postmortem ticket: add memory-utilisation alarm at 80% as early warning before OOM events.",
        ),
        Scenario(
            name="Stuck PROVISIONING — subnet ran out of IPs",
            body="During an autoscale-out spike, Tasks stuck PROVISIONING with <em>VPC.IPAddressLimitExceeded</em>. The Service\'s subnet (a /27 with 27 usable IPs) was full. Fix: added two more subnets to the Service\'s networkConfiguration; ECS spread Tasks across all three; subnet IP exhaustion no longer a single-subnet issue.",
        ),
        Scenario(
            name="Outage — circuit breaker disabled, bad image churned all night",
            body="A team\'s Service had circuit breaker disabled. A bad image rolled out at 22:00; Tasks crashlooped; rollout never completed. By 03:00 the Service was at 30% healthy. Postmortem: enabled circuit breaker + automated runbook to UpdateService rollback under 5 minutes. <em>The circuit breaker would have caught this in 90 seconds.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"If a Task is RUNNING, the Service is healthy.\"",
            truth="<strong>RUNNING means container started + container healthCheck passing</strong>. ALB target health is separate (HTTP probe by ALB). A Task can be RUNNING but ALB-Unhealthy because of SG, port, or path mismatch — and the Service won\'t serve traffic to it. Always check both layers.",
        ),
        Misconception(
            myth="\"OutOfMemoryError means the host is out of memory.\"",
            truth="No. <strong>OOM here is per-container hard limit</strong> — the container hit its <code>memory</code> hard limit and got SIGKILL. Other containers on the host (and the host itself) are unaffected. The fix is per-container memory + per-Task memory in the Task Definition, not host sizing.",
        ),
        Misconception(
            myth="\"Restart the Service usually fixes ECS issues.\"",
            truth="<strong>Restart-and-pray is the slowest debug technique.</strong> ECS surfaces the failure cause in stoppedReason within seconds of the failure. Restart loses that context (the original Task is gone). Read the chain first; restart only when the chain has named the cause and you\'ve fixed the underlying issue.",
        ),
    ],
    flashcards=[
        Flashcard(front="First command for any ECS troubleshooting?", back="<code>aws ecs describe-tasks --cluster X --tasks ID</code> — read <code>lastStatus</code> + <code>stoppedReason</code> + <code>containers[].exitCode</code>. Narrows cause class in seconds."),
        Flashcard(front="Four stuck-PENDING cause families?", back="(1) <strong>ENI provisioning</strong> (subnet IPs / SG), (2) <strong>image pull</strong> (ECR auth / KMS / network), (3) <strong>IAM/KMS for Secrets</strong> (execution role + KMS Decrypt), (4) <strong>capacity</strong> (Fargate quota, EC2 ASG full, external)."),
        Flashcard(front="CannotPullContainerError sub-causes?", back="<em>\"no basic auth credentials\"</em> = private registry creds. <em>\"manifest unknown\"</em> = image tag/digest gone. <em>\"AccessDenied\"</em> = ECR repo policy or execution role. <em>\"failed to decrypt with KMS\"</em> = KMS Decrypt missing."),
        Flashcard(front="ResourceInitializationError most common cause?", back="Execution role missing <code>secretsmanager:GetSecretValue</code> on the secret ARN, OR missing <code>kms:Decrypt</code> on the secret\'s customer-managed KMS key. Both role policy AND key policy must allow."),
        Flashcard(front="Exit code 137 typically means?", back="SIGKILL — most often the kernel OOM-killer or an OOM-reaped container. Look at memory metrics; bump container <code>memory</code>; investigate leak."),
        Flashcard(front="What does the deployment circuit breaker do on failure?", back="Stops the rollout + auto-rolls-back to the previous Task Definition revision (if <code>rollback: true</code>). Service events tab logs \"deployment circuit breaker\" message; read the rolled-back-revision\'s Task stoppedReasons for the root cause."),
        Flashcard(front="ALB target health is Unhealthy but Task is RUNNING — first check?", back="<strong>SG inbound</strong>: does the Task SG allow inbound from the ALB SG on the container port? Most common ALB-Unhealthy cause."),
        Flashcard(front="ECS Exec — when most useful?", back="When the failure is inside the container and not visible in logs — DNS issues, downstream timeouts, in-memory state inspection. Faster than restart-and-pray. Works on Fargate where SSH doesn\'t exist."),
    ],
    quizzes=[
        Quiz(
            prompt="A Service goes from 10/10 to 3/10 healthy in 5 minutes. Engineers are paged. Walk through the diagnostic chain in order with specific commands.",
            answer="(1) <strong>describe-services</strong>: <code>aws ecs describe-services --cluster X --services Y --query \"services[].events[:10]\"</code>. Read recent events — likely \"task X stopped, reason: ...\" entries. (2) <strong>List recently stopped Tasks</strong>: <code>aws ecs list-tasks --cluster X --service-name Y --desired-status STOPPED</code>. (3) <strong>describe-tasks</strong> on the stopped IDs: <code>describe-tasks --query \"tasks[].[lastStatus,stoppedReason,containers[0].exitCode]\"</code>. Read the reason patterns: are they all the same (systemic — bad deploy, downstream outage, capacity)? Or different (per-Task issue)? (4) <strong>If stoppedReason is generic</strong>: dig into CloudWatch logs for the failing container — <code>aws logs filter-log-events --log-group-name /aws/ecs/X --filter-pattern ERROR</code>. (5) <strong>If RUNNING Tasks are also unhappy</strong>: ECS Exec into one to inspect; check ALB target health; check Service Connect endpoints. (6) <strong>If pattern == bad-deploy</strong>: confirm circuit breaker tripped (events tab); rollback completed; root-cause the bad revision in dev/staging.",
        ),
        Quiz(
            prompt="A new revision deploys; circuit breaker fires; rollback completes; users notice nothing. Postmortem time. What\'s the right depth of investigation?",
            answer="<strong>Investigate fully even though users were unaffected.</strong> The circuit breaker prevented an outage but the bad revision is now an artifact in the system — and the next deploy may run into the same class of issue. (1) Read the bad-revision Tasks\' stoppedReasons (still queryable for STOPPED Tasks). (2) Reproduce in dev or staging — register the bad revision against a non-prod Service; observe the failure mode. (3) Identify the root cause: code regression, env var change, missed migration, dependency outage. (4) Fix in code; ship a new revision (same family); deploy. (5) Add a regression test or pre-deploy check that catches the failure pattern. (6) <strong>Document the failure family</strong> in the team\'s runbook — \"if the Service shows pattern X again, look at Y\" — so the next on-call rotation is faster.",
        ),
        Quiz(
            prompt="A team wants to skip the ECS troubleshooting chain — \"just restart the Service if anything is unhealthy.\" Defend the chain.",
            answer="\"<strong>Restart-as-debug is the slowest, riskiest technique.</strong> Three reasons: (1) <strong>The cause stays</strong>. If a config or IAM change broke this Service, restart launches new Tasks with the same broken config; they\'ll fail again. We churn until we read the actual cause. (2) <strong>The evidence is gone</strong>. STOPPED Tasks have stoppedReason for a finite window; we lose ours by stopping the chain mid-debug. Reading describe-tasks first costs 30 seconds and preserves the evidence. (3) <strong>Some bugs only surface during a specific code path</strong>. Restart hits that path again only randomly; targeted ECS Exec into a struggling Task can run the path on demand. Our SLA on diagnosing ECS issues should be 5 minutes, not 30 — and the chain (describe-tasks → events → logs → ECS Exec) gets us there. Restart-as-debug should be reserved for known-recoverable transient failures, not unknown-root-cause incidents.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer defended the chain",
        ),
    ],
    glossary=[
        GlossaryItem(name="describe-tasks", definition="Primary ECS-troubleshooting API. Returns lastStatus, stoppedReason, container exitCode, healthStatus, and metadata."),
        GlossaryItem(name="stoppedReason", definition="Field on a STOPPED Task naming the cause class — CannotPullContainerError, ResourceInitializationError, OutOfMemoryError, etc."),
        GlossaryItem(name="CannotPullContainerError", definition="Image pull failed — ECR auth, KMS, network, or registry credential issue."),
        GlossaryItem(name="ResourceInitializationError", definition="Launch-time AWS resource fetch failed — Secrets / SSM / KMS / log group create."),
        GlossaryItem(name="OutOfMemoryError (ECS)", definition="Container hit its memory hard limit. Per-container, not per-host."),
        GlossaryItem(name="Essential container exited", definition="An essential container exited with non-zero code; whole Task stopped. Read exit code for specifics."),
        GlossaryItem(name="exit code 137", definition="SIGKILL — typically OOM-killed or kernel-reaped. Map to memory issues first."),
        GlossaryItem(name="exit code 143", definition="SIGTERM — graceful stop. Usually intentional (deploy / scale-in)."),
        GlossaryItem(name="describe-services events", definition="Service-level event log — capacity, scheduling, deploy events. Read alongside describe-tasks."),
        GlossaryItem(name="ALB target health", definition="Separate from container healthCheck. Network-path health (SG, port, path) determined by ALB itself."),
    ],
    recap_lead="Read the chain top-down. describe-tasks → stoppedReason → events → CloudWatch logs → ECS Exec. Most failures cluster in four families: ENI / image pull / IAM-KMS / capacity. Stop reading the moment the cause is identified.",
    recap_next='<strong>Next — C10 capstone: Multi-Service Fargate App.</strong> Service Connect + ALB + EFS + Secrets Manager + CodeDeploy blue/green + Container Insights + autoscaling + failure-recovery runbook. The reference K-Harbor.',
)
