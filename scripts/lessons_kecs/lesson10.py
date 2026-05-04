"""K-ECS C10 — Capstone: Multi-Service Fargate App."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS capstone — multi-service Fargate app with Service Connect, ALB blue/green, EFS, Secrets, autoscaling.">
  <rect x="20" y="20" width="720" height="200" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Grand Voyage · K-Harbor — the reference multi-service Fargate app</text>
  <rect x="40" y="70" width="170" height="60" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">ALB</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#1F2433">blue + green TGs</text>
  <text x="125" y="124" text-anchor="middle" font-size="9" fill="#1F2433">CodeDeploy hooks</text>
  <rect x="40" y="150" width="170" height="60" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="125" y="172" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Service Auto Scaling</text>
  <text x="125" y="188" text-anchor="middle" font-size="9" fill="#1F2433">target tracking + Spot</text>
  <text x="125" y="202" text-anchor="middle" font-size="9" fill="#1F2433">capacity provider strategy</text>
  <rect x="225" y="70" width="170" height="60" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Service A (api)</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Fargate, awsvpc</text>
  <text x="310" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">execution + task role</text>
  <rect x="225" y="150" width="170" height="60" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="310" y="172" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Service B (worker)</text>
  <text x="310" y="188" text-anchor="middle" font-size="9" fill="#FBF1D6">Fargate Spot, queue</text>
  <text x="310" y="202" text-anchor="middle" font-size="9" fill="#FBF1D6">SQS-driven</text>
  <rect x="410" y="70" width="170" height="60" rx="10" fill="#3878B5" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Service Connect</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">east-west L7</text>
  <text x="495" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">retries + metrics</text>
  <rect x="410" y="150" width="170" height="60" rx="10" fill="#7AB3CC" stroke="#1F2433"/>
  <text x="495" y="172" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Container Insights</text>
  <text x="495" y="188" text-anchor="middle" font-size="9" fill="#FBF1D6">FireLens to S3 + CW</text>
  <text x="495" y="202" text-anchor="middle" font-size="9" fill="#FBF1D6">ADOT + X-Ray</text>
  <rect x="595" y="70" width="125" height="60" rx="10" fill="#5E4A8E" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">EFS</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">shared uploads</text>
  <text x="657" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">access points</text>
  <rect x="595" y="150" width="125" height="60" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="657" y="172" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Secrets + KMS</text>
  <text x="657" y="188" text-anchor="middle" font-size="9" fill="#FBF1D6">Secrets Manager</text>
  <text x="657" y="202" text-anchor="middle" font-size="9" fill="#FBF1D6">customer KMS keys</text>
</svg>"""


LESSON = LessonSpec(
    num="10",
    title_short="capstone",
    title_full="C10 · Capstone — The Reference Multi-Service Fargate Harbor",
    title_html="K-ECS C10 · Capstone",
    module_eyebrow="Module C10 · Grand Voyage — every K-Harbor concept in one defendable architecture",
    hero_sub_html='The reference K-Harbor: <strong>two ECS Services on Fargate</strong> (an HTTPS API + an SQS-driven worker), <strong>ALB with blue/green via CodeDeploy</strong>, <strong>Service Connect</strong> east-west, <strong>EFS with access points</strong> for shared uploads, <strong>Secrets Manager + customer KMS keys</strong> for credentials, <strong>Container Insights + FireLens (CW + S3) + ADOT/X-Ray</strong> for observability, <strong>Service Auto Scaling</strong> target-tracking, <strong>Capacity Provider strategy</strong> blending Fargate base + Fargate Spot for the worker, <strong>deployment circuit breaker</strong> on every Service, and a <strong>failure-recovery runbook</strong> mapping every cause class to a 5-minute fix.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM on launch night. Tax season starts in 4 hours. The team is cutting over from a single-EC2 monolith to ECS. There\'s no rollback path. Forty engineers are watching the deploy graph. <em>Today\'s capstone: design + walk through a defendable reference architecture that ships everything you\'ve learned in C1-C9 — and gives you the rollback path before you need it.</em>",
    stamp_html="<strong>The reference K-Harbor: Service Connect + ALB blue/green + EFS + Secrets/KMS + Container Insights + FireLens + ADOT/X-Ray + Service Auto Scaling + Fargate/Spot mix + circuit breaker + runbook. Every concept in C1-C9 has a place; the runbook closes the loop.</strong>",
    district_pin="kh-pier10",
    district_label="Grand Voyage",
    sections=[
        Section(
            eyebrow="Section 1.1 · the architecture",
            h2="Two Services, one ALB, Service Connect, EFS, Secrets",
            body_html="""    <p><strong>Cluster</strong>: <code>prod</code> with Container Insights enabled + Service Connect namespace <code>prod.local</code>.</p>
    <p><strong>Service A — api</strong>: HTTPS API. Fargate launch type. <code>desiredCount: 6</code>. Task Definition: 1 vCPU + 2 GiB; awsvpc; <code>ephemeralStorage: 30 GiB</code>; one container <em>app</em> + one Firelens sidecar <em>log_router</em>. <code>capacityProviderStrategy: [{FARGATE, weight:1, base:6}]</code>. Two ALB target groups (blue + green) registered via <code>deploymentController: CODE_DEPLOY</code>. Service Connect <code>publishes: api</code>.</p>
    <p><strong>Service B — worker</strong>: SQS consumer. Fargate launch type with Spot. <code>desiredCount: 2 (base) + auto-scaled by queue depth</code>. Task Definition: 0.5 vCPU + 1 GiB; awsvpc; <em>app</em> + <em>log_router</em> + <em>adot</em> sidecars. <code>capacityProviderStrategy: [{FARGATE, weight:1, base:2}, {FARGATE_SPOT, weight:4, base:0}]</code>. Service Connect <code>discovers: api</code> (worker calls API for callbacks).</p>
    <p><strong>EFS</strong>: filesystem with two access points — <code>/uploads</code> (shared by api + worker), <code>/archive</code> (worker write-only). IAM-auth + transit-encryption ON. Mount targets in all three AZs.</p>
    <p><strong>Secrets</strong>: Secrets Manager <code>prod/db</code>, <code>prod/api-key</code>, <code>prod/external-svc</code>; all encrypted with the <code>prod-app-secrets</code> customer KMS key. Execution role allows GetSecretValue + KMS Decrypt.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · IAM design",
            h2="Three roles per Service; least-privilege by default",
            body_html="""    <p><strong>Per-Service execution role</strong>: ECR pull on the specific repo + GetSecretValue on the specific Secret ARNs + KMS Decrypt on the specific KMS key + CloudWatch Logs CreateLogStream/PutLogEvents on the specific log group + (api only) Firelens sidecar permissions.</p>
    <p><strong>Per-Service task role</strong>:
    <em>api</em>: <code>dynamodb:GetItem/PutItem</code> on <code>arn:...table/orders</code>; <code>s3:GetObject/PutObject</code> on <code>arn:...bucket/uploads/*</code>; <code>sqs:SendMessage</code> on the worker queue. Plus ssmmessages:* for ECS Exec.
    <em>worker</em>: <code>sqs:ReceiveMessage/DeleteMessage</code> on the queue; <code>s3:GetObject</code> on uploads; <code>elasticfilesystem:ClientMount/ClientWrite</code> on the EFS access points; xray:PutTraceSegments + cloudwatch:PutMetricData. Plus ssmmessages.</p>
    <p><strong>CI/CD deploy role</strong>: <code>ecs:RegisterTaskDefinition</code>, <code>ecs:UpdateService</code>, <code>codedeploy:CreateDeployment</code>, <code>iam:PassRole</code> on the execution + task role ARNs only. <em>No</em> direct AWS access overlapping with what the running Tasks have. Three-role separation: deploy creds, launch creds, runtime creds — three different scopes.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · deploy + scaling + observability",
            h2="Blue/green + circuit breaker + autoscaling + telemetry",
            body_html="""    <p><strong>Blue/green deploy via CodeDeploy</strong>: <em>linear 10% per 5 min</em> with CloudWatch alarms — 5xxRate &gt; 1% over 1 min OR P95Latency &gt; 800ms over 5 min triggers auto-rollback. BeforeAllowTraffic Lambda smoke-tests the green TG. AfterAllowTraffic Lambda updates SLO dashboards.</p>
    <p><strong>Deployment circuit breaker</strong> on the worker (rolling deploys for non-blue/green): <code>{ enable: true, rollback: true }</code>. Catches bad worker images without touching ALB-traffic-weight machinery.</p>
    <p><strong>Service Auto Scaling</strong>:
    <em>api</em>: target tracking on <code>ALBRequestCountPerTarget = 200</code>; min 6, max 50.
    <em>worker</em>: target tracking on <code>SQSApproximateNumberOfMessagesVisible = 100</code>; min 2, max 30.</p>
    <p><strong>Capacity providers</strong>: api on Fargate base (steady traffic; Spot interruption unacceptable for live API). Worker on Fargate base + Fargate Spot weighted 4:1 (queue tolerates interruption; ECS reschedules interrupted Tasks).</p>
    <p><strong>Observability</strong>: Container Insights on; FireLens routes all logs to <em>CloudWatch live (14d)</em> + <em>S3 archive (Glacier after 30d)</em>; ADOT sidecar on every Service exports OTel traces to X-Ray + metrics to AMP. Service Connect emits per-service rps/latency/5xx automatically.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · failure-recovery runbook",
            h2="Every cause class → a 5-minute fix",
            body_html="""    <p>The runbook. Pinned to the team\'s wiki + linked from oncall pages.</p>
    <p><strong>Symptom: Service A degraded (5xx spike + ALB unhealthy targets).</strong>
    Step 1: <code>describe-services</code> events — circuit breaker / CodeDeploy alarm fired? If yes, rollback in flight; wait 5 min for stabilisation.
    Step 2: <code>describe-tasks --desired-status STOPPED</code> on recently stopped Tasks; read stoppedReason. If <em>OutOfMemoryError</em> → bump TD memory + redeploy. If <em>CannotPullContainerError</em> → check ECR perms / KMS / network.
    Step 3: ECS Exec into a RUNNING Task (any Task in the Service); curl localhost; check downstream connectivity to dependencies.
    Step 4: If symptoms remain after fix: <code>UpdateService --force-new-deployment</code> — replaces all Tasks.</p>
    <p><strong>Symptom: deploy stuck at 50% blue/green.</strong>
    Step 1: CodeDeploy console — which Lambda hook is failing? Read its log group.
    Step 2: Manual decision: continue to 100% (if symptoms are noise) or auto-rollback. Default = auto-rollback after 10 min if not progressing.
    Step 3: Postmortem the bad-revision Tasks (still queryable in Stopped status).</p>
    <p><strong>Symptom: worker queue depth not draining.</strong>
    Step 1: Check Service Auto Scaling — is it scaling out? <code>describe-scalable-target</code> + <code>describe-scaling-activities</code>.
    Step 2: Spot interruption rate up? Check capacity-provider strategy; consider temporarily shifting weight toward base Fargate.
    Step 3: Worker Task crashlooping? <code>describe-tasks STOPPED</code> in Service B; same chain.</p>
    <p><strong>Symptom: EFS-mounted Tasks stuck PROVISIONING.</strong>
    Step 1: Mount target SG allows NFS (2049) from Task SG?
    Step 2: Subnet IPs available?
    Step 3: EFS access point still exists + IAM auth allowed?</p>
    <p><strong>The runbook lives because someone walks through it during low-stress dev / staging incidents</strong> — at least monthly. <em>Game days</em> simulate failures; the runbook gets refined.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="Why is the worker on Fargate Spot but the api isn\'t?",
            options=[
                ("Spot is cheaper, so all workloads should use it.", False),
                ("Worker tolerates Task interruption (queue retry); api can\'t (live request loss).", True),
                ("Fargate Spot is required for SQS.", False),
            ],
            feedback="Spot interruptions are tolerable for queue-driven workers (ECS reschedules; SQS messages reappear). They\'re not tolerable for live HTTPS APIs (in-flight requests get 503s). The capacity-provider strategy reflects this.",
        ),
        3: PauseCheck(
            question="The runbook says \"<code>describe-tasks --desired-status STOPPED</code> first\" before restarting anything. Why?",
            options=[
                ("It\'s the fastest way to free capacity.", False),
                ("Stopped Tasks have stoppedReason — the cause data — that disappears once you replace Tasks blindly.", True),
                ("It\'s an AWS billing requirement.", False),
            ],
            feedback="Stopped Tasks are the evidence. Read stoppedReason + exit code first. Restart-and-pray loses the evidence and forces another debug cycle.",
        ),
    },
    before_after_before='<p>Pre-this-design, AWS-shop teams running multi-service apps stitched together: a single big EC2 + Docker Compose, manual ALB target registration, host-baked secrets, ad-hoc log shipping, no traces, no autoscaling, no rollback path. Production incidents were day-long investigations.</p>',
    before_after_after='<p>The reference K-Harbor wires every C1-C9 concept into one defendable architecture. Service Connect for east-west; ALB blue/green for safe deploys; EFS for shared state; Secrets Manager + KMS for credentials; Container Insights + FireLens + ADOT/X-Ray for observability; Service Auto Scaling + Spot mix for cost + bursty load; circuit breaker + runbook for the rollback path. <em>Production incidents are 5-minute investigations.</em></p>',
    before_after_caption='<p class="ba-caption"><em>The capstone is not a new concept — it\'s the disciplined assembly of everything before it. If your real architecture matches this, you have a defendable ECS deployment.</em></p>',
    analogy_intro_html='''<p>The harbor master arrives at the <strong>Grand Voyage</strong> ceremony. Every pier is wired correctly. The signal flag tower (ALB) routes incoming traffic; the smart relay station (Service Connect) handles east-west. The cargo holds (EFS) hold shared state. The customs vault (Secrets + KMS) is double-locked. The lighthouse (Container Insights + FireLens + ADOT/X-Ray) sees every signal. The loading crew yard (Service Auto Scaling + capacity providers) sizes itself for the day\'s load. The salvage office (the runbook) has every failure family already mapped to a clear response. Two ships sail today — the API and the worker — each on the right kind of capacity. <strong>The harbor is ready for the season.</strong></p>
    <p>The Grand Voyage is not a new concept; it\'s every previous district woven into one defendable harbor. C1\'s ECS shapes; C2\'s Task Definitions; C3\'s networking; C4\'s IAM + KMS; C5\'s storage; C6\'s deploy + scaling; C7\'s observability; C8\'s hybrid (kept simple here — pure cloud). Every K-Harbor lesson has a place on the map.</p>
    <p>The runbook is the discipline that keeps the harbor running when storms come. Each cause class — radio mast (ENI), warehouse handoff (image pull), customs vault (IAM/KMS), cargo too heavy (memory), lost crew letter (Essential exited), unhealthy ship (target health) — has a 5-minute response with a clear command. The harbor master practices the runbook on calm days so it\'s muscle memory by midnight.</p>''',
    translation_rows=[
        ("Grand Voyage ceremony", "Capstone reference architecture"),
        ("Two ships sailing today", "Service A (api) + Service B (worker)"),
        ("Signal flag tower", "ALB with blue/green target groups + CodeDeploy"),
        ("Smart relay station", "Service Connect east-west"),
        ("Shared cargo hold", "EFS + access points (uploads + archive)"),
        ("Customs vault, double-locked", "Secrets Manager + customer KMS keys"),
        ("Three letters per captain (deploy / launch / voyage)", "CI/CD role + execution role + task role"),
        ("Lighthouse with four observers", "Container Insights + FireLens + ADOT + X-Ray"),
        ("Load-aware crew yard", "Service Auto Scaling target tracking + capacity providers"),
        ("Steady ships on chartered berth", "Fargate base capacity"),
        ("Bursting ships on rented dock", "Fargate Spot weighted strategy"),
        ("Storm runbook on the wall", "5-minute failure-recovery runbook"),
    ],
    analogy_stops="A real harbor has years of accumulated muscle memory; the runbook only works if you exercise it during calm seas. Game days are the harbor\'s storm drills.",
    eli5="The Grand Voyage is the day everything we\'ve built ships at once. Every pier is wired right. The harbor master can route ships and the Salvage Office knows how to handle every kind of trouble in five minutes. The runbook is the harbor\'s storm playbook — practice it on calm days.",
    eli10="Two Services on Fargate (api with blue/green via CodeDeploy + Service Auto Scaling target-tracking on ALBRequestCountPerTarget; worker on Fargate base + Fargate Spot weighted strategy with target-tracking on SQS depth), Service Connect east-west, ALB north-south, EFS shared state with access points + IAM auth, Secrets Manager + customer KMS keys, three IAM roles (CI/CD + execution + task), Container Insights + FireLens (CW + S3 archive) + ADOT + X-Ray, deployment circuit breaker on every Service, runbook mapping every cause class to a 5-minute fix.",
    scenarios=[
        Scenario(
            name="Ship-it-Friday — first prod deploy on this architecture",
            body="A 30-engineer SaaS replaces their single-EC2 + Compose stack with this reference. Day-1 deploy: blue/green via CodeDeploy with linear 10%-per-5min shift; CloudWatch alarms gate. <em>Five minutes from \"go\" to \"100% on green\"</em>; existing stack drained; team watches dashboards. Container Insights + traces show normal traffic. <em>Not a heroic deploy — a scripted one.</em>",
        ),
        Scenario(
            name="Black Friday — autoscaling held",
            body="Tax-deadline traffic 8× normal. <code>ALBRequestCountPerTarget</code> climbed; api Service scaled out from 6 to 28 over 12 minutes via target tracking. Worker queue depth spiked; Spot Tasks scaled out cheaply (some interruptions; SQS retries handled them). Latency P95 stayed under 300ms. <em>The runbook never opened.</em>",
        ),
        Scenario(
            name="Bad deploy → blue/green rollback → 5-min postmortem",
            body="A Friday deploy raised P95 latency above the 800ms alarm threshold during the 10% canary phase. CodeDeploy auto-rolled-back; listener flipped to blue; users saw a brief 30-second tail elevation. Postmortem chain (describe-tasks STOPPED on green Tasks → CloudWatch logs → root cause = stale cache stampede on cold-start) took 5 minutes; fixed in next revision; on-call closed the page. <em>The system caught itself.</em>",
        ),
        Scenario(
            name="Game day — runbook proven on staging",
            body="The team ran a quarterly game day on staging. Killed a Fargate Spot Task → autoscale replaced. Nuked the EFS mount target SG → Tasks PROVISIONING; runbook chain found the cause in 3 minutes. Tampered a Secret\'s KMS key policy → ResourceInitializationError; runbook chain found it in 4 minutes. <em>Confidence in the runbook is built before the storm, not during it.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"This is over-engineered for a startup.\"",
            truth="Every layer here exists because something <em>doesn\'t</em> exist without it: blue/green for safe deploys, circuit breaker for runaway rollouts, observability for unknown unknowns, runbook for incident response. <strong>The marginal cost</strong> of including all of it on day 1 is small (Service Catalog templates do the heavy lift); the marginal cost of <em>adding it after the first incident</em> is much larger.",
        ),
        Misconception(
            myth="\"Blue/green is always better than rolling.\"",
            truth="Blue/green excels for <em>internet-facing</em> services where listener-flip-rollback is faster than launch-new-Task-rollback. For internal-only Services, rolling deploy + circuit breaker is simpler + cheaper (no two-target-group machinery) and almost as safe. The reference uses blue/green on api (internet-facing) and rolling on worker (internal queue consumer).",
        ),
        Misconception(
            myth="\"The runbook is documentation; we don\'t need to practice it.\"",
            truth="<strong>Untested runbooks rot.</strong> The cause-class commands change as AWS APIs evolve; the team\'s muscle memory fades; new failure modes emerge. Quarterly game days on staging keep both the runbook and the team current.",
        ),
    ],
    flashcards=[
        Flashcard(front="Why Fargate base for api but Fargate Spot for worker?", back="API serves live HTTPS — Spot interruption = real user 503s. Worker drains an SQS queue — Spot interruption = ECS reschedules + SQS resurfaces the message. Capacity-provider strategy reflects this: api 100% Fargate; worker base + Spot-weighted."),
        Flashcard(front="Three IAM roles in this architecture and what each does?", back="<strong>CI/CD role</strong>: deploy (RegisterTaskDefinition, UpdateService, CodeDeploy CreateDeployment, PassRole). <strong>Execution role</strong>: launch (ECR pull, Secrets fetch, KMS Decrypt, CloudWatch Logs). <strong>Task role</strong>: runtime (DynamoDB, S3, SQS, EFS ClientMount, X-Ray PutTraceSegments)."),
        Flashcard(front="What two CloudWatch alarms drive the CodeDeploy auto-rollback?", back="<strong>5xxRate &gt; 1% over 1 min</strong> (errors during canary) and <strong>P95Latency &gt; 800 ms over 5 min</strong> (latency regression). Both attached to the Deployment Group; either tripping rolls back."),
        Flashcard(front="api Service Auto Scaling target metric?", back="<code>ALBRequestCountPerTarget = 200</code>. min 6, max 50. Target tracking computes desired count to keep request load per Task at the target."),
        Flashcard(front="Worker Service Auto Scaling target metric?", back="<code>SQSApproximateNumberOfMessagesVisible = 100</code>. min 2, max 30. Scales out when queue depth grows; scales in when it drains."),
        Flashcard(front="What does the runbook do that automation doesn\'t?", back="Runbooks bridge the cases automation hasn\'t encoded yet — novel failures, multi-cause incidents, anything where a human needs to read the chain + decide. The runbook is the team\'s muscle memory in a written form, kept current via game days."),
        Flashcard(front="EFS access point design here?", back="Two access points: <code>/uploads</code> (api + worker both mount; api PUTs, worker GETs) and <code>/archive</code> (worker write-only; long-term retention). Each has its own POSIX UID/GID + path scope."),
        Flashcard(front="Three observability layers in this architecture?", back="<strong>Container Insights</strong> (cluster + service + task metrics + dashboards). <strong>FireLens</strong> sidecar logs to CloudWatch (14d) + S3 Glacier archive (long-term). <strong>ADOT</strong> sidecar exports OTel traces to X-Ray + metrics to AMP."),
    ],
    quizzes=[
        Quiz(
            prompt="A new engineer joins. What\'s the 2-minute architecture orientation?",
            answer="\"Two ECS Services on Fargate. <strong>api</strong> is HTTPS, behind ALB with blue/green via CodeDeploy. <strong>worker</strong> is queue-driven on Fargate Spot. They talk via Service Connect. State lives in DynamoDB (orders) and EFS (uploads). Secrets in Secrets Manager, KMS-customer-keyed. Three IAM roles per Service: CI/CD (deploy creds), execution (launch creds), task (runtime creds). Container Insights + FireLens + ADOT/X-Ray for observability. Service Auto Scaling target-tracks request count for api and queue depth for worker. Deployment circuit breaker on; CodeDeploy alarm-gated. The runbook on the wiki maps every common failure to a 5-minute fix. Game days quarterly to keep it sharp.\" Then walk them through the runbook and one game-day exercise.",
        ),
        Quiz(
            prompt="The CFO wants 30% cost reduction. Defend this architecture vs cuts.",
            answer="\"<strong>The architecture already takes the major cost-saving steps.</strong> Worker on Fargate Spot saves ~70% on that fleet. CloudWatch logs go to S3 Glacier after 30 days (saves ~80% on long-term retention vs CloudWatch retention). Service Auto Scaling shrinks both Services to baseline during off-hours. <strong>Possible further trims:</strong> (1) move worker base from 2 → 1 Fargate (~$50/mo); (2) move api from 6 → 4 Fargate baseline + scale-up faster (~$200/mo, riskier); (3) FireLens filter DEBUG logs out of CloudWatch (~$300/mo); (4) Container Insights metric-filtering for low-signal metrics (~$100/mo). <strong>Combined: ~$650/mo savings without architectural cuts.</strong> Cuts I would NOT make: ALB (it\'s not the cost center), Secrets Manager (KMS-encrypted is non-negotiable), ADOT/X-Ray (without traces, the next P99 incident takes days). The architecture is already optimised; don\'t weaken the operational core to chase the last 10%.\"",
        ),
        Quiz(
            prompt="Friday afternoon: a junior engineer pushes a Task Definition revision that changes <code>memory</code> from 2048 to 512. Walk through what happens in this architecture, end to end.",
            answer="(1) <strong>CodeDeploy starts</strong> linear 10% per 5 min canary. New Tasks (rev N+1, 512 MiB) launch into green TG. (2) <strong>Container OOMs at startup</strong> — apps using more than 512 MiB memory get SIGKILL. stoppedReason: OutOfMemoryError; exit code 137. (3) <strong>Green TG target health</strong> goes Unhealthy. (4) <strong>5xxRate alarm</strong> in CodeDeploy Deployment Group trips (Tasks not serving). (5) <strong>CodeDeploy auto-rollback</strong> — listener flips back to blue (rev N, 2048 MiB Tasks); green Tasks deregistered + drained; users saw maybe 30 seconds of elevated latency. (6) <strong>On-call paged</strong> by the rollback notification. (7) <strong>Runbook step 2</strong>: describe-tasks STOPPED on the green Tasks; stoppedReason OutOfMemoryError; exit code 137; in CloudWatch see \"OOMKilled\". (8) <strong>Root cause</strong> identified in 2 minutes; junior engineer pings on Slack; new revision fixes the regression in code review; deploy resumes by 17:30. <strong>The architecture caught the failure, rolled back automatically, and gave the team a 5-minute postmortem.</strong> No customer-facing outage; one alarm; one paged engineer; one PR.",
            cyoa=True,
            cyoa_tag="how the architecture handled the bad Friday deploy",
        ),
    ],
    glossary=[
        GlossaryItem(name="reference architecture", definition="A proven blueprint for a class of system. K-ECS\'s reference is multi-service Fargate with the elements listed."),
        GlossaryItem(name="game day", definition="Scheduled exercise where the team intentionally injects failures to validate the runbook + observability + autoscaling responses."),
        GlossaryItem(name="capacity provider strategy", definition="Per-Service mix of capacity providers (Fargate base + Spot weight). Distributes Tasks per the strategy ratios."),
        GlossaryItem(name="ALBRequestCountPerTarget", definition="CloudWatch metric — requests per ALB target per minute. Common Service Auto Scaling target metric for HTTP services."),
        GlossaryItem(name="SQSApproximateNumberOfMessagesVisible", definition="Queue depth metric. Common autoscaling target for queue-consumer workers."),
        GlossaryItem(name="BeforeAllowTraffic Lambda", definition="CodeDeploy hook — runs after green Tasks register but before traffic shifts; smoke-test gate."),
        GlossaryItem(name="AfterAllowTraffic Lambda", definition="CodeDeploy hook — runs after 100% traffic on green; for SLO updates / notifications."),
        GlossaryItem(name="three-role separation", definition="CI/CD role + execution role + task role. Three different scopes; container code can\'t see deploy or launch creds."),
        GlossaryItem(name="runbook", definition="Written, exercised playbook mapping symptoms to 5-minute fix sequences. Lives because game days keep it current."),
        GlossaryItem(name="defendable architecture", definition="Architecture an engineer can explain end-to-end + justify each component. Quality bar: can a new hire ramp in 2 days?"),
    ],
    recap_lead="The reference K-Harbor: two Fargate Services, ALB blue/green via CodeDeploy, Service Connect east-west, EFS + Secrets Manager + KMS, Container Insights + FireLens + ADOT/X-Ray, Service Auto Scaling, Fargate base + Spot mix, circuit breaker, three-role IAM separation, and a runbook kept current by game days. Every K-ECS concept woven into one defendable architecture.",
    recap_next='<strong>K-ECS complete.</strong> 10 modules. 30+ hours of content. From C1\'s five-shape selection guide to C10\'s reference architecture. The K-Harbor map is fully populated. <em>Next courses in the K-* family</em> — possibly K-Lambda (event-driven AWS), K-AppRunner (single-service PaaS), or a return to the K8s family with K-K3s (k3s/k0s/MicroK8s). Decisions per founder direction.',
    architecture_svg='''<svg viewBox="0 0 760 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="K-ECS capstone reference: ALB blue/green, two ECS Services on Fargate, Service Connect, EFS, Secrets, observability.">
  <rect x="10" y="10" width="740" height="260" rx="12" fill="#FBF7F0" stroke="#3878B5"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">K-ECS CAPSTONE · MULTI-SERVICE FARGATE REFERENCE</text>
  <rect x="20" y="50" width="160" height="70" rx="6" fill="#FF9900"/>
  <text x="100" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">ALB</text>
  <text x="100" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">blue + green TGs</text>
  <text x="100" y="100" text-anchor="middle" font-size="8" fill="#1F2433">CodeDeploy + alarms</text>
  <line x1="180" y1="85" x2="210" y2="85" stroke="#5A4F45" stroke-width="2" marker-end="url(#a10)"/>
  <defs><marker id="a10" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><polygon points="0 0, 10 5, 0 10" fill="#5A4F45"/></marker></defs>
  <rect x="210" y="50" width="200" height="70" rx="6" fill="#3878B5"/>
  <text x="310" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Service A · api</text>
  <text x="310" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">Fargate · 6 Tasks · awsvpc</text>
  <text x="310" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">target tracking RPS</text>
  <line x1="410" y1="85" x2="440" y2="85" stroke="#5A4F45" stroke-width="2" marker-end="url(#a10)"/>
  <rect x="440" y="50" width="200" height="70" rx="6" fill="#5DCAA5"/>
  <text x="540" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Service Connect</text>
  <text x="540" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">east-west L7 mesh</text>
  <text x="540" y="100" text-anchor="middle" font-size="8" fill="#1F2433">retries + metrics</text>
  <line x1="640" y1="85" x2="670" y2="85" stroke="#5A4F45" stroke-width="2" marker-end="url(#a10)"/>
  <rect x="670" y="50" width="70" height="70" rx="6" fill="#3F4A5E"/>
  <text x="705" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Service B</text>
  <text x="705" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">worker</text>
  <text x="705" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">SQS · Spot</text>
  <rect x="20" y="135" width="180" height="60" rx="6" fill="#A04832"/>
  <text x="110" y="155" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Secrets + KMS</text>
  <text x="110" y="171" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">execution role fetches</text>
  <text x="110" y="184" text-anchor="middle" font-size="8" fill="#FBE8DC">customer KMS keys</text>
  <rect x="220" y="135" width="180" height="60" rx="6" fill="#5E4A8E"/>
  <text x="310" y="155" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">EFS access points</text>
  <text x="310" y="171" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">/uploads · /archive</text>
  <text x="310" y="184" text-anchor="middle" font-size="8" fill="#FBE8DC">RWX cross-AZ</text>
  <rect x="420" y="135" width="180" height="60" rx="6" fill="#5A6B81"/>
  <text x="510" y="155" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">FireLens + Container Insights</text>
  <text x="510" y="171" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">CW + S3 archive</text>
  <text x="510" y="184" text-anchor="middle" font-size="8" fill="#FBE8DC">+ ADOT / X-Ray</text>
  <rect x="620" y="135" width="120" height="60" rx="6" fill="#FAC775"/>
  <text x="680" y="155" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">Auto Scaling</text>
  <text x="680" y="171" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">target tracking</text>
  <text x="680" y="184" text-anchor="middle" font-size="8" fill="#5A4F45">RPS + queue depth</text>
  <rect x="20" y="210" width="720" height="50" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="230" text-anchor="middle" font-size="11" font-weight="700" fill="#A04832">Three-role IAM separation: CI/CD · execution role · task role</text>
  <text x="380" y="246" text-anchor="middle" font-size="9" fill="#5A4F45" font-style="italic">Capacity Provider strategy: Fargate base + Fargate Spot weighted · circuit breaker on every Service · runbook + game days quarterly</text>
</svg>''',
    architecture_caption='Two Fargate Services (api + worker) behind ALB with blue/green via CodeDeploy. Service Connect mesh for east-west. EFS shared state, Secrets + KMS, Container Insights + FireLens + ADOT/X-Ray. Auto Scaling on RPS / queue depth. Three-role IAM. Spot blend on the worker. The reference K-Harbor.',
)
