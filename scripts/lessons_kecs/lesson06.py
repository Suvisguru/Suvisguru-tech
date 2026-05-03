"""K-ECS C6 — Deployment and Scaling."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS deployment + scaling — rolling, blue/green, autoscaling, capacity providers, placement.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Loading Crew Yard · K-Harbor — rolling vs blue/green; capacity providers; auto scaling</text>
  <rect x="40" y="70" width="170" height="120" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">rolling deploy</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">deploymentController: ECS</text>
  <text x="125" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">minHealthy + maxPercent</text>
  <text x="125" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">circuit breaker</text>
  <text x="125" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">default · simple · safe</text>
  <rect x="225" y="70" width="170" height="120" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">blue/green</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">CODE_DEPLOY</text>
  <text x="310" y="124" text-anchor="middle" font-size="9" fill="#1F2433">two TGs + listener swap</text>
  <text x="310" y="144" text-anchor="middle" font-size="9" fill="#1F2433">canary + shift</text>
  <text x="310" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">richer rollback</text>
  <rect x="410" y="70" width="170" height="120" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Service Auto Scaling</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">target tracking</text>
  <text x="495" y="124" text-anchor="middle" font-size="9" fill="#1F2433">step / scheduled</text>
  <text x="495" y="144" text-anchor="middle" font-size="9" fill="#1F2433">CPU / memory / req</text>
  <text x="495" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">App Auto Scaling</text>
  <rect x="595" y="70" width="125" height="120" rx="10" fill="#7AB3CC" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">capacity providers</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">EC2 ASG</text>
  <text x="657" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">Fargate / Spot</text>
  <text x="657" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">managed scaling</text>
  <text x="657" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">strategy + base</text>
</svg>"""


LESSON = LessonSpec(
    num="06",
    title_short="deployment & scaling",
    title_full="C6 · ECS Deployment and Scaling",
    title_html="K-ECS C6 · Deployment and Scaling",
    module_eyebrow="Module C6 · Loading Crew Yard — rolling vs blue/green; capacity providers; auto scaling",
    hero_sub_html='<strong>Three deployment controllers</strong>: <em>ECS</em> (rolling, default), <em>CODE_DEPLOY</em> (blue/green via two target groups), <em>EXTERNAL</em> (you drive the API directly). Rolling tunes via <em>deploymentConfiguration</em>: minimumHealthyPercent + maximumPercent + <strong>deployment circuit breaker</strong> (auto-rollback on failure threshold). <strong>Service Auto Scaling</strong> via Application Auto Scaling — target tracking (CPU / memory / request count), step, scheduled. <strong>Cluster auto scaling</strong> via <strong>capacity providers</strong> (EC2 ASG with managed scaling, Fargate, Fargate Spot). <strong>Placement</strong> via constraints (instance type / AZ / attribute) + strategies (binpack / spread / random).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A bad container image rolled out — every Task crashloops. The Service is at 30% healthy and the rollout keeps churning, replacing healthy old Tasks with broken new ones. <em>The deployment circuit breaker isn\'t enabled.</em> Manual rollback takes 25 minutes during the worst possible time. Today\'s lesson: pick the right deploy + autoscale shape, and <strong>turn on the circuit breaker on every Service.</strong>",
    stamp_html="<strong>Rolling is the default; blue/green is for richer rollback (CodeDeploy). Always enable the deployment circuit breaker. Service Auto Scaling for Task count; capacity providers + managed scaling for cluster nodes. Placement strategies (binpack / spread / random) + constraints set Task→host affinity.</strong>",
    district_pin="kh-pier06",
    district_label="Loading Crew Yard",
    sections=[
        Section(
            eyebrow="Section 1.1 · rolling deployments",
            h2="deploymentConfiguration, minimumHealthyPercent, maximumPercent, circuit breaker",
            body_html="""    <p>Default <code>deploymentController: { type: ECS }</code>. Rolling deploy: ECS starts new Tasks, registers them with the ALB target group, waits for health, drains old Tasks, deregisters and stops them.</p>
    <p><strong>deploymentConfiguration.minimumHealthyPercent</strong>: minimum % of desired-count that must remain RUNNING + healthy during a deploy. Default 100 (no over-provision needed but slower). 50 lets ECS stop half the old Tasks before launching new ones (faster on small Services, riskier capacity dip).</p>
    <p><strong>deploymentConfiguration.maximumPercent</strong>: max % of desired-count Tasks running simultaneously (old + new combined). Default 200 (lets ECS double-deploy). Set to 100 for tight resource scenarios where you can\'t afford extra capacity briefly.</p>
    <p><strong>deploymentCircuitBreaker</strong>: <code>{ enable: true, rollback: true }</code>. ECS watches new Task health during the rollout; if a configurable failure threshold is crossed (Tasks failing or new Tasks failing health checks), it stops the rollout and rolls back to the previous Task Definition revision. <strong>Enable on every Service.</strong> Default is off (legacy).</p>
    <p><strong>healthCheckGracePeriodSeconds</strong>: time after a Task starts before ALB / container health checks count against the deploy decision. Set generously (60-120s) for apps with slow startup.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · blue/green via CodeDeploy",
            h2="Two target groups, listener swap, canary + traffic shift",
            body_html="""    <p><code>deploymentController: { type: CODE_DEPLOY }</code> hands deploys to AWS CodeDeploy. Two ALB target groups (blue + green); CodeDeploy launches new Tasks into the green TG; runs <em>BeforeAllowTraffic</em> Lambda hooks (smoke tests); shifts traffic via the ALB listener; runs <em>AfterAllowTraffic</em> Lambda hooks; drains old Tasks.</p>
    <p><strong>Traffic shift modes</strong>: <em>AllAtOnce</em> (full cutover; fast); <em>Linear</em> (10% per N minutes — gradual); <em>Canary</em> (10% then wait then 100%). Combine with <strong>CloudWatch alarms</strong> in the Deployment Group: alarm trips → CodeDeploy auto-rollback.</p>
    <p><strong>When pick blue/green over rolling?</strong> When you want a separate test surface before traffic shifts (the green TG is private to CodeDeploy until cutover); when you need <em>fast rollback</em> (blue stays warm — listener flip back is seconds, not new-Task-launch); when alarm-driven rollback matters (your CloudWatch metric is the rollback trigger).</p>
    <p><strong>EXTERNAL deployment controller</strong> <span class="skip-tag">[ deep dive — skip if new ]</span>: you drive the deploy via ECS API directly (CreateTaskSet / UpdateServicePrimaryTaskSet / DeleteTaskSet). For custom deploy strategies (Argo Rollouts / Spinnaker-style controllers external to AWS).</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Service Auto Scaling + Cluster auto scaling",
            h2="Task count + node count",
            body_html="""    <p><strong>Service Auto Scaling</strong> uses Application Auto Scaling: register the ECS Service as a scalable target; attach scaling policies. Three policy types:</p>
    <ul>
      <li><strong>Target tracking</strong> (recommended): pick a metric (ECSServiceAverageCPUUtilization, ECSServiceAverageMemoryUtilization, ALBRequestCountPerTarget) + target value (e.g., 60% CPU). Auto Scaling computes the policy.</li>
      <li><strong>Step scaling</strong>: define alarm bands → adjust desired count by N. Older / more manual.</li>
      <li><strong>Scheduled</strong>: cron-style adjustments — \"scale to 50 at 09:00 weekdays\".</li>
    </ul>
    <p><strong>Cluster Auto Scaling</strong> (EC2-launch only): <strong>capacity providers</strong> bind a Cluster to an EC2 Auto Scaling group with managed scaling — ECS computes how many instances are needed to host pending Tasks and scales the ASG. Avoids the older pattern of separate ECS desired-count + Cluster ASG that didn\'t coordinate.</p>
    <p><strong>Capacity provider strategies</strong>: a Service\'s <code>capacityProviderStrategy</code> mixes capacity providers — e.g., 80% Fargate Spot, 20% Fargate base; ECS launches Tasks across the strategy. Use for Spot blending, multi-AZ EC2 + Fargate fallback, etc.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · placement constraints + strategies",
            h2="Where Tasks land on capacity",
            body_html="""    <p><strong>placementConstraints</strong> filter <em>which</em> hosts a Task can run on (EC2 launch only — Fargate ignores). Two kinds:</p>
    <ul>
      <li><code>distinctInstance</code> — at most one Task per host (HA pattern).</li>
      <li><code>memberOf</code> with cluster-query expression — \"only on instances with attribute X\" (instance type, AZ, custom attribute).</li>
    </ul>
    <p><strong>placementStrategies</strong> control <em>preference order</em> for hosts that satisfy the constraints. Three:</p>
    <ul>
      <li><strong>binpack</strong> — pack onto fewest hosts possible (cost optimisation; reduces idle host count).</li>
      <li><strong>spread</strong> — evenly distribute by attribute (e.g., AZ for HA).</li>
      <li><strong>random</strong> — random selection.</li>
    </ul>
    <p><strong>Common combos</strong>: <em>spread by AZ + binpack by memory</em> (HA across AZs while packing memory tight); <em>distinctInstance + spread by AZ</em> (one Task per host across all AZs for control-plane workloads).</p>
    <p><strong>Fargate placement</strong>: AWS picks the underlying microVM placement; you can\'t influence it directly. AZ-spread comes from listing multiple subnets in <code>networkConfiguration</code> (one subnet per AZ).</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A bad image rolls out and crashloop-restarts. The Service is at 30% healthy + churning. What setting catches this in future?",
            options=[
                ("Lower minimumHealthyPercent so ECS stops more Tasks per cycle.", False),
                ("Enable deploymentCircuitBreaker with rollback: true.", True),
                ("Increase healthCheckGracePeriodSeconds so failures are masked.", False),
            ],
            feedback="The deployment circuit breaker watches the rollout, detects the failure pattern, stops the rollout, and rolls back to the previous revision automatically.",
        ),
        3: PauseCheck(
            question="A Service must run exactly one Task per EC2 host (one DaemonSet-like agent per host). Which placement?",
            options=[
                ("Strategy: binpack.", False),
                ("Constraint: distinctInstance.", True),
                ("Strategy: random.", False),
            ],
            feedback="distinctInstance constraint forces at most one Task per host. Pair with desired-count = number of hosts to deploy a per-host agent.",
        ),
    },
    before_after_before='<p>Pre-circuit-breaker, bad ECS deploys ran to completion or hung at partial-healthy state requiring manual UpdateService rollback. Pre-capacity-providers, autoscaling at the Cluster level (EC2 ASG) and Service level (desired count) were uncoordinated — pending Tasks waited for ASG to scale; ASG scaled based on CPU not pending Tasks. Manual sync.</p>',
    before_after_after='<p>Modern ECS deploys watch themselves (circuit breaker auto-rollback), capacity providers coordinate Cluster + Service scaling automatically (managed scaling drives ASG to fit pending Tasks), Service Auto Scaling target-tracks any CloudWatch metric, blue/green via CodeDeploy adds rich rollback semantics, and placement strategies + constraints encode operational intent declaratively.</p>',
    before_after_caption='<p class="ba-caption"><em>Get the deploy controller right + circuit breaker on + capacity providers in place; the rest is mostly tuning.</em></p>',
    analogy_intro_html='''<p>The <strong>Loading Crew Yard</strong> is where new ships get prepared before being moved to active piers. Two crew rotation styles work in this yard.</p>
    <p><strong>Rolling rotation</strong>: the harbor master starts new ships at adjacent slips, lets them warm up + pass medical inspection (ALB target health), then drains the old ships from active piers and decommissions them. The yard stays mostly busy throughout. A <em>safety inspector</em> (the deployment circuit breaker) watches; if too many new ships fail inspection in a window, the inspector calls a halt and reverts to the prior crew. <em>Always enable the safety inspector.</em></p>
    <p><strong>Blue/green rotation</strong> (CodeDeploy): two parallel pier groups (blue + green). Old crew at blue; new crew warms up at green privately. Inspector runs sea-trials at green (CloudWatch alarms during canary). When green passes, the harbor master flips the harbor entrance signal to route incoming shipments to green. Blue stays warm in case a flip-back is needed. Richer; takes a bit more orchestration.</p>
    <p>For sustained traffic, <strong>Service Auto Scaling</strong> watches the active piers\' load (CPU / memory / request count) and adds or drains ships automatically — target tracking is the recommended dial. For the <em>yard\'s capacity itself</em> (how many crew bays exist), <strong>capacity providers</strong> let the harbor master compute "we need 5 more bays for pending ships" and scale the rental yard up — instead of the old pattern of separate yard-sizing and crew-sizing decisions.</p>
    <p>Where ships dock is governed by <strong>placement</strong>: constraints filter the eligible piers (only piers with a certain crane type, only certain AZs); strategies pick among eligibles (pack everything onto the fewest piers for cost, spread evenly across AZs for resilience, distinctInstance for "one per pier").</p>''',
    translation_rows=[
        ("Loading Crew Yard", "ECS deployment + scaling layer"),
        ("Rolling rotation", "deploymentController: ECS (rolling)"),
        ("Safety inspector calls halt", "deploymentCircuitBreaker (auto-rollback)"),
        ("Min healthy + max double-up rules", "minimumHealthyPercent + maximumPercent"),
        ("Sea-trial waiting period", "healthCheckGracePeriodSeconds"),
        ("Two pier groups + entrance flip", "blue/green via CodeDeploy (two target groups)"),
        ("Trial run with canary alarm", "CloudWatch alarm in CodeDeploy Deployment Group"),
        ("Watch the active piers", "Service Auto Scaling (target tracking)"),
        ("Yard rental sizing", "capacity providers + managed scaling"),
        ("Pier eligibility filter", "placementConstraints (distinctInstance / memberOf)"),
        ("Pier preference order", "placementStrategies (binpack / spread / random)"),
    ],
    analogy_stops="A real harbor crew is hours of work; ECS Tasks rotate in seconds. The \"warm up + drain\" sequence is real but the timescales make some patterns from physical-yard logistics not transfer directly.",
    eli5="When you change something in your ship, the harbor swaps in new ships gradually so passengers don\'t notice. A safety inspector watches; if too many new ships fail their checks, she calls a halt and brings back the old ones. There\'s also a fancier swap-out that uses two pier groups — flip a switch when the new group is ready. The yard adds and removes crews automatically based on how busy the piers are.",
    eli10="<strong>Rolling deploys</strong>: minimumHealthyPercent + maximumPercent control the over/under-provision; <strong>deploymentCircuitBreaker</strong> auto-rolls-back. <strong>Blue/green via CodeDeploy</strong>: two target groups + listener swap; canary / linear / all-at-once traffic shift; CloudWatch alarms drive auto-rollback. <strong>Service Auto Scaling</strong>: target tracking (CPU / memory / ALB request count), step, scheduled. <strong>Cluster Auto Scaling</strong>: capacity providers with managed scaling drive EC2 ASGs based on pending Tasks. <strong>Placement</strong>: constraints (distinctInstance, memberOf) + strategies (binpack / spread / random).",
    scenarios=[
        Scenario(
            name="Standard SaaS — rolling + circuit breaker",
            body="A 50-engineer SaaS with 10 ECS Services on Fargate. Every Service has <code>deploymentCircuitBreaker: { enable: true, rollback: true }</code>, minimumHealthyPercent=100, maximumPercent=200. Standard rolling deploys; circuit breaker has caught two bad images this quarter. <em>Default + circuit breaker is the right baseline for almost everything.</em>",
        ),
        Scenario(
            name="Regulated workload — blue/green with CloudWatch alarm gate",
            body="A health-tech runs a PHI-handling API. <strong>blue/green via CodeDeploy</strong>: linear 10%-per-5min traffic shift. CodeDeploy Deployment Group has a CloudWatch alarm on <code>5xx-rate &gt; 1%</code>. Bad deploy → alarm trips → CodeDeploy auto-rollback (listener flips back to blue, green Tasks drained). <em>Compliance gets a documented gradual-rollout + rollback story.</em>",
        ),
        Scenario(
            name="Cost optimisation — Fargate + Fargate Spot blend",
            body="A 25-engineer team runs background workers tolerant to interruption. Capacity provider strategy: <em>2 Tasks Fargate base + 80% Fargate Spot weight</em>. Steady 2 Tasks always; bursts go to Spot at ~70% discount. <strong>Service Auto Scaling target-tracks</strong> SQS queue depth → scales out when backlog grows. <em>Saved ~60% on the worker fleet.</em>",
        ),
        Scenario(
            name="Outage — bad deploy without circuit breaker",
            body="A team rolled a Task Definition revision with a memory leak. Tasks restarted every 8 minutes. Service stayed at 70% healthy churning forever. Latency tail climbed; oncall paged. <strong>30-minute manual rollback</strong> via UpdateService to prior revision. <em>Postmortem</em>: enable deploymentCircuitBreaker on every Service; ship a runbook for prod-rollback under 5 minutes.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"The deployment circuit breaker is on by default.\"",
            truth="It is <strong>off by default</strong> for legacy compatibility. You must explicitly set <code>deploymentCircuitBreaker: { enable: true, rollback: true }</code>. Enable on every Service — the cost is zero; the catch-rate on bad deploys is huge.",
        ),
        Misconception(
            myth="\"Service Auto Scaling and ASG autoscaling are the same.\"",
            truth="<strong>Service Auto Scaling</strong> changes the ECS Service\'s <em>desired Task count</em>. <strong>EC2 ASG autoscaling</strong> changes the <em>EC2 instance count</em>. Two different layers. <strong>Capacity providers + managed scaling</strong> bridge them — managed scaling adjusts the ASG based on pending Task capacity needs.",
        ),
        Misconception(
            myth="\"binpack always saves money.\"",
            truth="<strong>binpack maximises host utilisation</strong> — but if the workload has spiky memory and Tasks land on already-loaded hosts, OOM kills surface. <em>spread by AZ + binpack by memory</em> gets HA + density. Pure binpack on bursty workloads is a famous footgun.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three deploymentController types?", back="<strong>ECS</strong> (rolling, default), <strong>CODE_DEPLOY</strong> (blue/green via two target groups), <strong>EXTERNAL</strong> (you drive deploys via the ECS API directly)."),
        Flashcard(front="What does the deployment circuit breaker do?", back="Watches new Task health during a rollout; if failures cross threshold, stops the rollout and rolls back to the previous Task Definition revision. <strong>Off by default — turn it on.</strong>"),
        Flashcard(front="minimumHealthyPercent + maximumPercent — what do they control?", back="<strong>minimumHealthyPercent</strong>: minimum % of desired-count that stays healthy during a deploy (default 100). <strong>maximumPercent</strong>: max % of desired-count Tasks (old + new) running simultaneously (default 200)."),
        Flashcard(front="Blue/green traffic shift modes?", back="<strong>AllAtOnce</strong> (full cutover), <strong>Linear</strong> (N% per K minutes), <strong>Canary</strong> (N% then wait then 100%). Combine with CloudWatch alarms in the Deployment Group for auto-rollback."),
        Flashcard(front="Three Service Auto Scaling policy types?", back="<strong>Target tracking</strong> (recommended; pick a metric + target value), <strong>step scaling</strong> (alarm bands), <strong>scheduled</strong> (cron-style)."),
        Flashcard(front="Capacity providers — what problem do they solve?", back="Coordinate Cluster + Service scaling. <strong>Managed scaling</strong> sizes the EC2 ASG to fit pending Tasks; capacity provider strategies blend providers (e.g., Fargate base + Fargate Spot weight) for Spot fallback or multi-launch-type Services."),
        Flashcard(front="placementStrategies — three types?", back="<strong>binpack</strong> (fewest hosts), <strong>spread</strong> (evenly by attribute, e.g., AZ for HA), <strong>random</strong>. Combine: spread by AZ + binpack by memory is the common HA + density combo."),
        Flashcard(front="distinctInstance constraint — when use?", back="When you want exactly one Task per host (DaemonSet-like agents, host-coupled monitoring sidecars, anything that should not duplicate per host). EC2-launch only."),
    ],
    quizzes=[
        Quiz(
            prompt="A team\'s Service is on the default rolling deploy. They want to upgrade to blue/green for richer rollback. Walk through the migration steps.",
            answer="(1) Create a <strong>second ALB target group</strong> (green) with the same target type IP + health check; both blue + green register with one ALB listener. (2) Create a <strong>CodeDeploy application + Deployment Group</strong> referencing the ECS Service + both target groups. (3) Update the <strong>Service deploymentController</strong> from ECS to CODE_DEPLOY (this requires a UpdateService with a new task definition; ECS rejects controller change otherwise). (4) Future deploys go through CodeDeploy: launch into green, run BeforeAllowTraffic hooks, shift via listener, run AfterAllowTraffic hooks, drain blue. (5) Add <strong>CloudWatch alarms</strong> to the Deployment Group for auto-rollback on metric breach. <em>Initial migration costs a few hours; future deploys are richer + safer.</em>",
        ),
        Quiz(
            prompt="A Service\'s desired count is 4. CPU is sustained at 85%. Service Auto Scaling target tracking is set to 60% CPU. What happens, and how long until the Service stabilises?",
            answer="<strong>Application Auto Scaling</strong> sees actual CPU (85%) above target (60%) → calculates required Task count to hit 60% → issues <code>UpdateService --desired-count N</code> where N ≈ 4 × (85/60) = ~6 Tasks. ECS launches 2 new Tasks (PROVISIONING → PENDING → RUNNING; ~1-2 min on Fargate, longer on EC2 if ASG must scale). New Tasks register with ALB; load distributes; CPU drops. Auto Scaling waits the cooldown (default 300s) before any further adjustment. <em>Total time</em>: 2-5 minutes from CPU breach to stabilisation, faster on Fargate, slower if EC2 ASG must scale up first.",
        ),
        Quiz(
            prompt="The CFO sees the Fargate bill: \"Move everything to EC2 capacity providers + Spot. Cheaper.\" The fleet has both stateful Services and stateless workers. Defend a hybrid.",
            answer="\"<strong>Spot interruptions are not equally tolerable across services.</strong> Stateful Services (anything with active sessions, in-flight transactions, write-ahead logs) shouldn\'t run on pure Spot — every interruption is potential data loss or angry user. Stateless workers tolerant to interruption (queue consumers, image processors, batch tasks) are exactly the Spot use case — 70% discount, ECS reschedules them on Spot interruption. <strong>The hybrid:</strong> stateful Services on Fargate (or EC2 On-Demand) with capacity-provider strategy = base capacity. Stateless workers on Fargate Spot or EC2 Spot via capacity-provider strategy = weighted Spot with small base. <em>We get the Spot savings on ~60% of compute that can absorb interruption, and we keep the stateful 40% on stable capacity. Pure Spot would cost us a customer-facing incident.</em>\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CFO",
        ),
    ],
    glossary=[
        GlossaryItem(name="deploymentController", definition="ECS / CODE_DEPLOY / EXTERNAL — chooses how Service moves between Task Definition revisions."),
        GlossaryItem(name="deploymentCircuitBreaker", definition="Auto-rollback on rollout failure. Off by default; enable on every Service."),
        GlossaryItem(name="minimumHealthyPercent", definition="Min % of desired-count Tasks that stay healthy during a deploy. Default 100."),
        GlossaryItem(name="maximumPercent", definition="Max % of desired-count Tasks (old + new) running simultaneously during deploy. Default 200."),
        GlossaryItem(name="healthCheckGracePeriodSeconds", definition="Time after Task start before health checks count against the deploy decision."),
        GlossaryItem(name="CodeDeploy blue/green", definition="Two-target-group deploy with listener swap; canary/linear/all-at-once shift; CloudWatch-alarm-driven rollback."),
        GlossaryItem(name="Service Auto Scaling", definition="Application Auto Scaling for ECS Services — target tracking / step / scheduled scaling of desired count."),
        GlossaryItem(name="capacity provider", definition="Cluster ↔ capacity binding (EC2 ASG, Fargate, Fargate Spot). Managed scaling drives ASG to fit Tasks."),
        GlossaryItem(name="capacity provider strategy", definition="Per-Service mix of capacity providers (e.g., Fargate base + Spot weight). ECS distributes Tasks per strategy."),
        GlossaryItem(name="placementConstraints", definition="distinctInstance or memberOf with cluster-query expression. Filters eligible hosts."),
        GlossaryItem(name="placementStrategies", definition="binpack / spread / random — preference order among eligible hosts."),
    ],
    recap_lead="Three deployment controllers; rolling default + circuit breaker is the safe baseline. Blue/green for richer rollback. Service Auto Scaling for Task count; capacity providers for cluster sizing. Placement strategies + constraints encode operational intent.",
    recap_next='<strong>Next — C7: ECS Observability.</strong> CloudWatch Container Insights for ECS; ECS Exec for interactive shell; FireLens (Fluent Bit / Fluentd) for log routing; ADOT for metrics + traces; AWS X-Ray.',
)
