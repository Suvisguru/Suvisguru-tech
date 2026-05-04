"""K-ECS C1 — ECS Architecture (Cluster, Service, Task, Task Definition, launch types)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS architecture — ECS vs Kubernetes vs Fargate vs App Runner vs Lambda; cluster, service, task, task definition.">
  <defs>
    <linearGradient id="cgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3878B5"/><stop offset="100%" stop-color="#1F4F84"/></linearGradient>
    <linearGradient id="fgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FF9900"/><stop offset="100%" stop-color="#C77600"/></linearGradient>
  </defs>
  <rect x="20" y="20" width="720" height="200" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Harbor Office · K-Harbor — five AWS container shapes, one selection guide</text>
  <rect x="40" y="70" width="135" height="130" rx="10" fill="url(#cgrad)" stroke="#1F2433"/>
  <text x="107" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">ECS</text>
  <text x="107" y="108" text-anchor="middle" font-size="9" fill="#FBF7F0">AWS-native</text>
  <text x="107" y="122" text-anchor="middle" font-size="9" fill="#FBF7F0">orchestrator</text>
  <text x="107" y="142" text-anchor="middle" font-size="9" fill="#FBF7F0">no K8s API</text>
  <text x="107" y="158" text-anchor="middle" font-size="9" fill="#FBF7F0">tight AWS fit</text>
  <text x="107" y="178" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF7F0">least YAML</text>
  <rect x="190" y="70" width="135" height="130" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="257" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">EKS</text>
  <text x="257" y="108" text-anchor="middle" font-size="9" fill="#FBF7F0">managed K8s</text>
  <text x="257" y="122" text-anchor="middle" font-size="9" fill="#FBF7F0">Pods, Deployments</text>
  <text x="257" y="142" text-anchor="middle" font-size="9" fill="#FBF7F0">portable to GKE/AKS</text>
  <text x="257" y="158" text-anchor="middle" font-size="9" fill="#FBF7F0">huge ecosystem</text>
  <text x="257" y="178" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF7F0">most YAML</text>
  <rect x="340" y="70" width="135" height="130" rx="10" fill="url(#fgrad)" stroke="#1F2433"/>
  <text x="407" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">Fargate</text>
  <text x="407" y="108" text-anchor="middle" font-size="9" fill="#FBF7F0">serverless capacity</text>
  <text x="407" y="122" text-anchor="middle" font-size="9" fill="#FBF7F0">for ECS or EKS</text>
  <text x="407" y="142" text-anchor="middle" font-size="9" fill="#FBF7F0">no nodes to manage</text>
  <text x="407" y="158" text-anchor="middle" font-size="9" fill="#FBF7F0">per-Task billing</text>
  <text x="407" y="178" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF7F0">launch type, not product</text>
  <rect x="490" y="70" width="115" height="130" rx="10" fill="#7AB3CC" stroke="#1F2433"/>
  <text x="547" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">App Runner</text>
  <text x="547" y="108" text-anchor="middle" font-size="9" fill="#FBF7F0">code or image →</text>
  <text x="547" y="122" text-anchor="middle" font-size="9" fill="#FBF7F0">HTTPS app</text>
  <text x="547" y="142" text-anchor="middle" font-size="9" fill="#FBF7F0">opinionated PaaS</text>
  <text x="547" y="158" text-anchor="middle" font-size="9" fill="#FBF7F0">single-service web</text>
  <text x="547" y="178" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF7F0">no orchestration knobs</text>
  <rect x="620" y="70" width="100" height="130" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="670" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#3F4A5E">Lambda</text>
  <text x="670" y="108" text-anchor="middle" font-size="9" fill="#3F4A5E">function as</text>
  <text x="670" y="122" text-anchor="middle" font-size="9" fill="#3F4A5E">a service</text>
  <text x="670" y="142" text-anchor="middle" font-size="9" fill="#3F4A5E">15 min max</text>
  <text x="670" y="158" text-anchor="middle" font-size="9" fill="#3F4A5E">event-driven</text>
  <text x="670" y="178" text-anchor="middle" font-size="9" font-style="italic" fill="#3F4A5E">no servers, no Tasks</text>
</svg>"""


LESSON = LessonSpec(
    num="01",
    title_short="ECS architecture",
    title_full="C1 · ECS Architecture — Cluster, Service, Task, Task Definition, Launch Types",
    title_html="K-ECS C1 · ECS Architecture",
    module_eyebrow="Module C1 · the Harbor Office — five AWS container shapes, one selection guide",
    hero_sub_html='<strong>This is not a Kubernetes course.</strong> ECS is AWS\'s own container orchestrator — different APIs from K8s (no Pods, no Deployments, no K8s Services, no Ingress, no RBAC, no CRDs). The shapes: <strong>Cluster</strong> (the harbor itself), <strong>Service</strong> (a long-running pier with N ships always docked), <strong>Task</strong> (one running ship — a group of containers scheduled together), <strong>Task Definition</strong> (the cargo manifest — JSON spec for what a Task should look like). Four launch types: <em>EC2</em> (you own the dock workers), <em>Fargate</em> (AWS owns the dock workers — serverless capacity), <em>External / ECS Anywhere</em> (your-own-hardware piers), and <em>ECS Managed Instances</em> (newest — AWS-managed EC2 with ECS-optimised AMI lifecycle).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Your tax-day SaaS is burning. The CFO chose <em>App Runner</em> last quarter because \"the demo took 20 seconds.\" Tonight a customer is uploading 4 GB of CSVs in a single request. App Runner times out at 120 seconds. There\'s no way to crank that knob — App Runner is opinionated by design. <em>You realise the team needed an orchestrator, not a PaaS.</em> Today\'s lesson: pick the AWS container shape that fits the workload — and know what each shape commits you to.",
    stamp_html="<strong>ECS = AWS-native orchestrator (Cluster / Service / Task / Task Definition); EKS = managed K8s; Fargate = serverless capacity (a launch type, not a product); App Runner = opinionated PaaS for single-service HTTPS apps; Lambda = functions, 15-min cap. Pick by operational appetite + workload shape, not popularity.</strong>",
    district_pin="kh-pier01",
    district_label="Harbor Office",
    sections=[
        Section(
            eyebrow="Section 1.1 · five AWS container shapes",
            h2="ECS vs EKS vs Fargate vs App Runner vs Lambda",
            body_html="""    <p><strong>ECS</strong> (Elastic Container Service): AWS\'s own orchestrator. You declare a Cluster, then Tasks (groups of containers) and Services (long-running Tasks with ALB/NLB integration + auto scaling + rolling deploys). <em>No K8s APIs</em> — no <code>kubectl</code>, no Pods, no YAML manifests. Tight integration with IAM, CloudWatch, ALB, ECR, Secrets Manager. <em>Pick when</em> you\'re AWS-only and want the least YAML possible.</p>
    <p><strong>EKS</strong> (Elastic Kubernetes Service): managed K8s. You get a real K8s API server, real Pods, real Deployments, real CRDs. Portable to GKE / AKS / on-prem. Huge ecosystem (Helm, operators, service mesh). <em>Pick when</em> you need K8s portability or your team already knows K8s. Covered in K-EKS.</p>
    <p><strong>Fargate</strong>: serverless capacity for ECS *or* EKS. Not a product on its own — it\'s a <em>launch type</em>. AWS provisions and bills you per Task (or per Pod, on EKS). No EC2 to patch. <em>Pick when</em> you want zero node management; tolerate the per-Task pricing premium vs raw EC2.</p>
    <p><strong>App Runner</strong>: opinionated PaaS for a single HTTPS service from a Git repo or container image. AWS does build, deploy, scale, TLS, custom domain. <em>120-second request timeout. No sidecars. No background workers. No multi-service.</em> Pick when you want a single web service with zero ops surface. Don\'t pick for batch jobs, long requests, or multi-container apps.</p>
    <p><strong>Lambda</strong>: function-as-a-service. Up to <em>15-minute</em> execution per invocation. Container-image-based or zip-based. Event-driven (S3 / SQS / API Gateway / EventBridge). <em>Pick when</em> the workload is event-driven + short-running + bursty. Not for long-running services (use ECS or EKS).</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · the four ECS shapes",
            h2="Cluster, Service, Task, Task Definition",
            body_html="""    <p><strong>Cluster</strong>: a logical grouping of compute capacity. Empty until you give it Tasks. Can have <em>EC2 capacity</em>, <em>Fargate capacity</em>, <em>external instances</em> (ECS Anywhere), or any mix.</p>
    <p><strong>Task Definition</strong>: a JSON spec describing what one Task should look like — list of containers, CPU + memory, network mode, volumes, IAM roles, log config, environment variables + secrets. <em>Versioned</em> — every change creates a new revision (e.g., <code>my-app:42</code>). The cargo manifest in the analogy.</p>
    <p><strong>Task</strong>: one running instance of a Task Definition. A group of one or more containers scheduled and stopped <em>together</em> (similar to a K8s Pod, but ECS-specific). Has a state (PROVISIONING → PENDING → RUNNING → STOPPED) and stop reason on exit. Can be one-off (run once and stop) or part of a Service.</p>
    <p><strong>Service</strong>: an ECS object that keeps N Tasks running long-term. Manages rolling deployments, integrates with ALB/NLB target groups, supports Service Auto Scaling, and emits service discovery records via Cloud Map or Service Connect. <em>Closest analog to a K8s Deployment + Service combined</em>, but it\'s its own object and cannot be confused with a K8s Service object.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · launch types",
            h2="EC2, Fargate, External (ECS Anywhere), ECS Managed Instances",
            body_html="""    <p><strong>EC2 launch type</strong>: you create EC2 Auto Scaling groups; ECS agents (running on each EC2) report capacity; ECS schedules Tasks onto your EC2s. You own patching + AMI updates + scaling. <em>Cheapest for steady-state workloads</em> with predictable utilisation; supports Spot, Graviton, GPU, large memory ratios.</p>
    <p><strong>Fargate launch type</strong>: AWS owns the underlying capacity. You request a Task with CPU + memory; Fargate provisions a microVM, runs your containers, bills you by Task-second. <em>No EC2</em>. Pricier per vCPU-hour than raw EC2, but the price-of-not-managing-nodes wins for many workloads.</p>
    <p><strong>External instances (ECS Anywhere)</strong>: register your-own-hardware (on-prem servers, edge devices, even VMs in another cloud) into an ECS cluster via the SSM agent + ECS agent. ECS schedules Tasks onto external capacity. <em>Bridge use cases</em>: regulated workloads on-prem, edge processing, gradual cloud migration.</p>
    <p><strong>ECS Managed Instances</strong> <span class="skip-tag">[ deep dive — skip if new ]</span>: AWS-managed EC2 with ECS-optimised AMI lifecycle. AWS patches and rotates the underlying instances on your behalf, but unlike Fargate you still get EC2-style features (full Bottlerocket / AL2023, custom AMIs, Spot, GPU pools). <em>Middle ground</em> between raw EC2 and Fargate.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · ECS internals",
            h2="ECS agent, control plane, scheduler, deployment controller, placement, lifecycle",
            body_html="""    <p><strong>ECS agent</strong>: a small Go binary (open-source) running on every container host (EC2, external instance, or Fargate microVM). Talks to the ECS control plane over outbound HTTPS, reports capacity, pulls Task assignments, manages container lifecycle (image pull, start, stop), and ships logs.</p>
    <p><strong>ECS control plane</strong>: AWS-managed regional service. Holds Cluster + Service + Task Definition + Task state. Receives API calls (RunTask, CreateService, UpdateService, …) and emits Task assignments to ECS agents.</p>
    <p><strong>Service scheduler</strong>: keeps the actual Task count matching the desired count for each Service. Replaces failed Tasks. Drives rolling deployments (start new revision, drain old, watch ALB target health).</p>
    <p><strong>Deployment controller</strong>: orchestrates how a Service moves from one Task Definition revision to the next. Three options: <em>ECS</em> (built-in rolling — default), <em>CODE_DEPLOY</em> (blue/green via CodeDeploy), <em>EXTERNAL</em> (you drive deploys via the ECS API directly).</p>
    <p><strong>Task placement</strong>: when a Task is launched, the placement engine picks compute to run it on, using <em>placement strategies</em> (binpack / spread / random) and <em>placement constraints</em> (instance type, AZ, attribute filters). Fargate ignores most of this — Fargate places one Task per microVM.</p>
    <p><strong>Task lifecycle</strong>: PROVISIONING (capacity being prepared) → PENDING (waiting for ENI / volumes / image pull) → RUNNING (containers up, healthChecks reporting) → STOPPED (stopped reason: USER_INITIATED / OutOfMemoryError / Essential container exited / etc.). Service discovery + load balancing wire up only when state = RUNNING.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A team wants a single HTTPS REST service that auto-scales, with no node management and no orchestrator-level knobs. Which AWS shape?",
            options=[
                ("ECS on Fargate — closest to a managed orchestrator.", False),
                ("App Runner — opinionated single-service PaaS, exactly that shape.", True),
                ("EKS on Fargate — full K8s for portability.", False),
            ],
            feedback="App Runner is the right fit when the workload truly is a single HTTPS service with no orchestration needs. The 120-second request timeout and no-sidecars rule are the trade-offs — accept them and you get the shortest path to deployed.",
        ),
        3: PauseCheck(
            question="A Task is stuck in PENDING for 4 minutes. Which is the most likely cause class?",
            options=[
                ("Service scheduler crashed.", False),
                ("ENI provisioning, image pull, or IAM resolution stalled.", True),
                ("Task Definition revision number rolled over.", False),
            ],
            feedback="PENDING means the agent is waiting on prerequisites — most often awsvpc-ENI provisioning, ECR image pull (network or IAM permissions), or task-execution-role policy resolution. ECS troubleshooting later in the course unpacks the specific failure modes.",
        ),
    },
    before_after_before='<p>Pre-ECS, AWS-shop teams running containers had to roll their own. <em>EC2 Auto Scaling group + custom AMI with Docker baked in + a homemade scheduler in Lambda + an ALB target group registered by hand</em>. Deploying a new version meant SSHing to each instance and running <code>docker pull</code>. Failures were silent. Logs went to disk and rotated. Multi-AZ took weeks of infra work. <em>Each team built their own orchestrator badly.</em></p>',
    before_after_after='<p>Modern ECS gives you the orchestrator out of the box: a Cluster, a Service, a Task Definition, an ALB-integrated rolling deploy, CloudWatch logs by default, IAM-per-Task, multi-AZ from <code>--availability-zones</code>. Add Fargate and the EC2 fleet disappears too. Add Service Connect and east-west service discovery + traffic management land without an extra mesh. <em>The orchestrator is the platform; you ship Task Definitions.</em></p>',
    before_after_caption='<p class="ba-caption"><em>If you\'re AWS-only and don\'t need K8s portability, ECS removes a lot of platform-team work. The trade is: you can\'t lift-and-shift to GKE.</em></p>',
    analogy_intro_html='''<p>K-Harbor is a working AWS-managed harbor. Cargo ships arrive; piers receive them; tugboats nudge each one into its slip. The <strong>Harbor Office</strong> is the first building you see — every captain (operator) checks in there to get a berth assignment.</p>
    <p>On the wall is a chart of five different ways to ship cargo. <strong>ECS</strong>: a full harbor — piers, tugboats, harbor master, you walk in with a cargo manifest and ask for berth. <strong>EKS</strong>: a different harbor across the bay, run to international K8s standard so you can sail your cargo to GCP\'s harbor or Azure\'s harbor without repackaging. <strong>Fargate</strong>: the harbor master arranges <em>self-assembling pop-up piers</em> on demand — no permanent dock workers — and bills you per ship-day. <strong>App Runner</strong>: a curbside drop-off — you hand over a single small package and AWS delivers it; no piers, no manifests, no negotiation. <strong>Lambda</strong>: a pneumatic-tube system for tiny envelopes — fast, but anything over 15 minutes gets stuck in the tube.</p>
    <p>You\'re here for ECS. Inside the harbor: the <strong>Harbor Master</strong> (the ECS control plane) keeps the chart of every pier and ship. Each <strong>pier</strong> (Service) has N ships always docked; if one sinks, the Harbor Master orders a replacement. Each <strong>ship</strong> (Task) carries a group of containers — the Task Definition is the cargo manifest spelling out what containers and how much CPU and memory. The <strong>tugboat skipper</strong> (ECS agent) lives on every dock and actually pushes ships into their slips, reporting back to the Harbor Master.</p>''',
    translation_rows=[
        ("Harbor Office", "ECS Cluster — entry point, configuration"),
        ("Pier (long-term berth with N ships)", "ECS Service — keeps N Tasks running"),
        ("Ship at the pier", "ECS Task — one running instance"),
        ("Cargo manifest", "Task Definition — JSON spec, versioned by revision"),
        ("Harbor Master", "ECS control plane / scheduler / deployment controller"),
        ("Tugboat Skipper", "ECS agent (one per host: EC2, external, or Fargate microVM)"),
        ("Permanent dock workers (you hire them)", "EC2 launch type"),
        ("Pop-up self-assembling piers (AWS arranges)", "Fargate launch type"),
        ("Your-own-warehouse pier across the bay", "External launch type — ECS Anywhere"),
        ("AWS-managed dock workers + swap-out cycle", "ECS Managed Instances launch type"),
        ("International-standard harbor across the bay", "EKS — managed K8s"),
        ("Curbside one-package drop-off", "App Runner — single-service PaaS"),
        ("Pneumatic envelope tubes (15-min cap)", "Lambda — function-as-a-service"),
    ],
    analogy_stops="A real harbor has fixed piers and ships. ECS Tasks are software-defined and disappear in seconds when stopped — there\'s no \"empty pier\" to inspect later. The Harbor Office stays; everything else is ephemeral state in DynamoDB.",
    eli5="AWS has five different ways to run containers. ECS is AWS\'s own way — like a harbor where you bring a list of what\'s in your ship and AWS finds you a pier. EKS is the same idea but built to international Kubernetes standards. Fargate is when AWS arranges pop-up piers so you don\'t hire dock workers. App Runner is a curbside drop-off for one package. Lambda is a pneumatic tube for tiny envelopes. Pick the one that matches what you\'re shipping.",
    eli10="ECS has four shapes — <strong>Cluster</strong> (the harbor), <strong>Service</strong> (a pier that keeps N ships docked long-term), <strong>Task</strong> (one running ship of containers), <strong>Task Definition</strong> (versioned JSON manifest of what a Task should look like). Four launch types: <em>EC2</em> (you manage hosts), <em>Fargate</em> (AWS manages capacity, per-Task billing), <em>External / ECS Anywhere</em> (your hardware joins the cluster), <em>ECS Managed Instances</em> (AWS-managed EC2). The control plane is regional, the ECS agent runs on every host, the service scheduler keeps Task count = desired, and the deployment controller handles rolling or blue/green moves to new Task Definition revisions.",
    scenarios=[
        Scenario(
            name="SaaS — first containerised service picks ECS on Fargate",
            body="A 30-engineer SaaS shipping their first containerised API. They pick <strong>ECS on Fargate</strong>. <em>Zero EC2 to manage</em>: they declare a Service with desired-count = 3 and a Task Definition with one container. ALB integration via target-type IP, blue/green via CodeDeploy, CloudWatch logs by default. <em>The platform team they didn\'t hire is the cost saving.</em>",
        ),
        Scenario(
            name="Batch ML inference — ECS on EC2 with Spot + GPU",
            body="A 200-engineer ML team runs nightly inference on 100 GiB of new images. <strong>ECS on EC2</strong> with <em>g5.xlarge Spot</em> capacity providers; nightly RunTask launches 50 inference Tasks, each with a single GPU container. Cost is ~70% less than On-Demand. Fargate would have worked too but doesn\'t support GPU as broadly + costs more per vCPU-hour for steady batch.",
        ),
        Scenario(
            name="Regulated workload — ECS Anywhere on-prem hardware",
            body="A bank can\'t move customer-data processing to the cloud. They run <strong>ECS Anywhere</strong> on their on-prem rack: SSM agent + ECS agent register external instances; the same Task Definitions deploy on-prem and on Fargate-cloud. <em>Single control plane across regulated and unregulated workloads.</em>",
        ),
        Scenario(
            name="Outage — App Runner picked for a workload that needed ECS",
            body="A startup picked App Runner for their CSV-import API for the demo speed. Production usage included 2-minute uploads. App Runner\'s 120-second request timeout fired; users got 504s. <em>4-hour Sunday outage</em>. Postmortem: migrate to ECS on Fargate (no request timeout cap) with ALB long-running connection support. <em>App Runner was the wrong shape.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"ECS Service is just like a K8s Service.\"",
            truth="No. A K8s Service is a virtual IP + DNS for selecting Pods. An ECS Service is closer to a K8s <em>Deployment</em> — a long-running controller that keeps N Tasks running, drives rolling deploys, and (separately) integrates with ALB/NLB or Service Connect for traffic. The two \"Service\" objects share a name but not a meaning.",
        ),
        Misconception(
            myth="\"Fargate is a separate AWS product from ECS.\"",
            truth="Fargate is a <strong>launch type</strong> — a way to provide capacity to ECS or EKS. The same ECS Cluster can have Fargate Tasks and EC2 Tasks side by side via capacity providers. You don\'t \"choose Fargate\"; you choose ECS-with-Fargate-capacity or EKS-with-Fargate-capacity.",
        ),
        Misconception(
            myth="\"App Runner is just simpler ECS.\"",
            truth="App Runner is a <em>different shape entirely</em> — opinionated PaaS for a single HTTPS service. It has a 120-second request timeout, no sidecars, no multi-container, no orchestration knobs. ECS lets you express any orchestrator pattern; App Runner lets you express \"a web service\". Picking App Runner expecting ECS-like flexibility is the most common AWS-container mistake.",
        ),
    ],
    flashcards=[
        Flashcard(front="Five AWS container shapes — what differs?", back="<strong>ECS</strong>: AWS-native orchestrator (no K8s API). <strong>EKS</strong>: managed K8s. <strong>Fargate</strong>: serverless capacity (launch type for ECS or EKS). <strong>App Runner</strong>: opinionated single-service PaaS (120s timeout, no sidecars). <strong>Lambda</strong>: function-as-a-service, 15-min cap, event-driven."),
        Flashcard(front="ECS shapes — Cluster, Service, Task, Task Definition?", back="<strong>Cluster</strong>: logical grouping of capacity. <strong>Task Definition</strong>: versioned JSON spec for a Task (containers + CPU/memory + network + IAM + logs). <strong>Task</strong>: one running instance of a Task Definition (group of containers scheduled together). <strong>Service</strong>: long-running controller keeping N Tasks running, integrating with ALB/NLB and rolling deploys."),
        Flashcard(front="Four ECS launch types?", back="<strong>EC2</strong>: you manage EC2 ASG + ECS agent on each. <strong>Fargate</strong>: serverless capacity, per-Task billing, no nodes. <strong>External (ECS Anywhere)</strong>: your-own-hardware joins the cluster. <strong>ECS Managed Instances</strong>: AWS-managed EC2 with ECS-optimised AMI lifecycle (middle ground)."),
        Flashcard(front="What is the ECS agent and where does it run?", back="A small Go binary (open-source) on every container host — EC2, external instance, or Fargate microVM. Reports capacity, pulls Task assignments, manages container lifecycle, ships logs. Talks to the regional ECS control plane via outbound HTTPS."),
        Flashcard(front="Three deployment controllers in ECS?", back="<strong>ECS</strong> (built-in rolling — default; <code>deploymentConfiguration</code> with min-healthy/max percent + circuit breaker). <strong>CODE_DEPLOY</strong> (blue/green via CodeDeploy, two target groups). <strong>EXTERNAL</strong> (you drive deploys via ECS API directly — for custom controllers)."),
        Flashcard(front="Task lifecycle states?", back="PROVISIONING (capacity being prepared) → PENDING (waiting for ENI / volumes / image pull) → RUNNING (containers up + healthChecks passing) → STOPPED (with stop reason like USER_INITIATED, OutOfMemoryError, Essential container exited, CannotPullContainerError, ResourceInitializationError)."),
        Flashcard(front="ECS Service vs K8s Service — what\'s the key difference?", back="ECS Service ≈ K8s Deployment (long-running controller maintaining N Tasks + driving rolling deploys). A K8s Service is a virtual-IP + DNS object for selecting Pods. They share a name but not a meaning. ECS does its load balancing via ALB/NLB target groups or Service Connect."),
        Flashcard(front="When to pick ECS over EKS?", back="<em>AWS-only deployment, want least YAML, value tight AWS service integration over K8s portability, team has no existing K8s investment.</em> ECS removes a class of platform-team work; the trade is no portability to GCP/Azure/on-prem K8s. Pick EKS if K8s portability or ecosystem (Helm, operators, mesh) matters."),
    ],
    quizzes=[
        Quiz(
            prompt="A team is choosing between ECS on Fargate and ECS on EC2 for a steady-state web service running 24/7. CFO asks why anyone would pick EC2 if Fargate is \"easier\". Defend the EC2 choice.",
            answer="\"<strong>Fargate is per-vCPU-hour priced ~30-40% higher than equivalent raw EC2 capacity.</strong> For a workload running 24/7 at predictable load, raw EC2 with reserved instances or Savings Plans is materially cheaper. Fargate wins for bursty workloads (off-hours scale-to-near-zero), workloads where node management costs human time, or where Spot interruptions on EC2 are unacceptable. Steady-state always-on web service with predictable utilisation is the textbook EC2 case — we get cheaper compute and the orchestrator still does rolling deploys, autoscaling, healing. We pay the EC2 patching tax (Bottlerocket + ECS-optimised AMI rotations make this small) and we save 30%.\"",
        ),
        Quiz(
            prompt="A new engineer asks: \"Why doesn\'t ECS have Pods?\" Explain.",
            answer="ECS pre-dates wide K8s adoption (~2014) and was designed by AWS as a Docker-first orchestrator with simpler primitives. The ECS <strong>Task</strong> is its closest analog to a K8s Pod — a group of containers scheduled and stopped together, sharing a network namespace (in awsvpc mode), sharing volumes via task-level mounts. The vocabulary differs because the products are independent ancestries: Pods = K8s vocabulary; Tasks = ECS vocabulary. They\'re not interchangeable terms in writing or quizzes — \"Pod\" specifically means the K8s object.",
        ),
        Quiz(
            prompt="The CTO says: \"Move everything to App Runner. Less ops, less code.\" The team has 8 microservices, three of which run async background workers. What happens?",
            answer="App Runner is single-service-HTTPS-only. Three of the eight services don\'t fit at all (background workers don\'t expose HTTPS endpoints — App Runner can\'t schedule them). The other five would need to drop their sidecars (App Runner has no multi-container support). Inter-service traffic would go through public HTTPS or VPC connectors — no Service Connect, no Cloud Map, no internal mesh. The 120-second request timeout would clip any long upload/download or report-generation endpoint. <strong>Result:</strong> within a week, ops surface is up (because the team is rebuilding what App Runner doesn\'t have), and three services are stuck. <strong>The right move:</strong> keep the eight services on ECS Fargate; if a single-service-HTTPS app shows up *new* in the future, App Runner is fine for *that* one.",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CTO",
        ),
    ],
    glossary=[
        GlossaryItem(name="ECS Cluster", definition="Logical grouping of capacity (EC2 / Fargate / external) where Tasks run. The harbor itself in K-Harbor."),
        GlossaryItem(name="ECS Service", definition="Long-running controller maintaining N Tasks, driving rolling deploys, integrating with ALB/NLB or Service Connect."),
        GlossaryItem(name="ECS Task", definition="One running instance of a Task Definition — a group of containers scheduled and stopped together."),
        GlossaryItem(name="Task Definition", definition="Versioned JSON spec for a Task: containers, CPU + memory, network mode, IAM roles, log config, env + secrets. New revision per change."),
        GlossaryItem(name="Container Definition", definition="One element inside a Task Definition\'s containerDefinitions array — image, ports, env, healthCheck, dependsOn, logConfiguration."),
        GlossaryItem(name="ECS launch type", definition="How capacity is provided: EC2 / Fargate / External (ECS Anywhere) / ECS Managed Instances."),
        GlossaryItem(name="Capacity Provider", definition="Object linking a Cluster to capacity (EC2 ASG, Fargate, Fargate Spot, external). Enables managed scaling and Spot fallback."),
        GlossaryItem(name="Service Connect", definition="ECS\'s modern east-west service discovery + traffic management; replaces App Mesh patterns. Covered in C3."),
        GlossaryItem(name="Cloud Map", definition="AWS service discovery for ECS Services (and other workloads) — DNS or HTTP API for service-to-service lookup."),
        GlossaryItem(name="ECS agent", definition="Open-source Go binary on every container host. Reports capacity to control plane; runs and reports container lifecycle."),
        GlossaryItem(name="Deployment controller", definition="ECS / CODE_DEPLOY / EXTERNAL — chooses how Service moves between Task Definition revisions."),
        GlossaryItem(name="Task placement", definition="Engine that picks which capacity to run a Task on — strategies (binpack/spread/random) + constraints (instance type, AZ, attribute)."),
    ],
    recap_lead="ECS is AWS\'s native container orchestrator. Four shapes (Cluster / Service / Task / Task Definition) × four launch types (EC2 / Fargate / External / Managed Instances) × three deployment controllers. Pick by operational appetite + workload shape — App Runner for single-HTTPS-service, Lambda for short event-driven, ECS for orchestration without K8s, EKS for K8s portability.",
    recap_next='<strong>Next — C2: Task Definitions and Containers.</strong> The JSON shape — family + revision, network mode, CPU + memory, ephemeralStorage, runtimePlatform; container definitions (image + ports + env + secrets + dependsOn + healthCheck + logConfiguration + ulimits + linuxParameters); volumes (bind / Docker / EFS / FSx); sidecars + task-level shared volumes; task IAM role vs execution role.',
    architecture_svg='''<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS architecture: control plane + service scheduler + task placement + ECS agent on capacity (EC2 / Fargate / External).">
  <rect x="10" y="10" width="740" height="220" rx="12" fill="#FBF7F0" stroke="#3878B5"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">ECS · CONTROL PLANE + AGENT ON CAPACITY</text>
  <rect x="20" y="50" width="720" height="60" rx="6" fill="#3F4A5E"/>
  <text x="380" y="70" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">AWS-managed ECS control plane (regional)</text>
  <text x="380" y="86" text-anchor="middle" font-size="9" fill="#FBF1D6" font-style="italic">service scheduler · deployment controller · task placement engine · API endpoint</text>
  <text x="380" y="100" text-anchor="middle" font-size="9" fill="#FBE8DC">holds Cluster + Service + Task Definition + Task state</text>
  <rect x="20" y="125" width="170" height="60" rx="6" fill="#FF9900"/>
  <text x="105" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">EC2 launch</text>
  <text x="105" y="161" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">your ASG + ECS agent</text>
  <text x="105" y="173" text-anchor="middle" font-size="8" fill="#1F2433">cheapest steady-state</text>
  <rect x="200" y="125" width="170" height="60" rx="6" fill="#5DCAA5"/>
  <text x="285" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Fargate launch</text>
  <text x="285" y="161" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">AWS-managed microVM</text>
  <text x="285" y="173" text-anchor="middle" font-size="8" fill="#1F2433">per-Task billing</text>
  <rect x="380" y="125" width="170" height="60" rx="6" fill="#A04832"/>
  <text x="465" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">External (ECS Anywhere)</text>
  <text x="465" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">SSM + ECS agent on-prem</text>
  <text x="465" y="173" text-anchor="middle" font-size="8" fill="#FBE8DC">your hardware</text>
  <rect x="560" y="125" width="180" height="60" rx="6" fill="#5E4A8E"/>
  <text x="650" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">ECS Managed Instances</text>
  <text x="650" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">AWS-managed EC2 lifecycle</text>
  <text x="650" y="173" text-anchor="middle" font-size="8" fill="#FBE8DC">middle ground</text>
  <rect x="20" y="195" width="720" height="30" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="215" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">Service holds N Tasks · Task Definition is the immutable JSON manifest · ECS agent reports state to control plane</text>
</svg>''',
    architecture_caption='AWS-managed regional control plane (service scheduler + deployment controller + task placement) talks to ECS agent on each host. Four launch types (EC2 / Fargate / External / Managed Instances) provide capacity; same control plane orchestrates all of them.',
)
