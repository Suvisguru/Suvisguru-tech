"""K-ECS C8 — ECS Anywhere and Hybrid."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS Anywhere — control plane in cloud, capacity on-prem; SSM + ECS agent registration; limits.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Outport Station · K-Harbor — your hardware joins the harbor; control plane stays in the cloud</text>
  <rect x="40" y="70" width="200" height="120" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">on-prem / edge server</text>
  <text x="140" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">your hardware</text>
  <text x="140" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">your network</text>
  <text x="140" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">SSM agent installed</text>
  <text x="140" y="170" text-anchor="middle" font-size="9" fill="#FBF1D6">ECS agent installed</text>
  <text x="140" y="188" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">launches outbound HTTPS</text>
  <rect x="260" y="70" width="200" height="55" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="360" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">SSM activation</text>
  <text x="360" y="108" text-anchor="middle" font-size="9" fill="#1F2433">code + ID for registration</text>
  <rect x="260" y="140" width="200" height="55" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="360" y="162" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">external capacity provider</text>
  <text x="360" y="178" text-anchor="middle" font-size="9" fill="#1F2433">requiresAttributes: EXTERNAL</text>
  <rect x="480" y="70" width="240" height="120" rx="10" fill="#7AB3CC" stroke="#1F2433"/>
  <text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">limits</text>
  <text x="600" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">no awsvpc network mode</text>
  <text x="600" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">no ALB integration</text>
  <text x="600" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">bridge / host / none only</text>
  <text x="600" y="160" text-anchor="middle" font-size="9" fill="#FBF1D6">no Service Connect</text>
  <text x="600" y="176" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">pick workloads carefully</text>
</svg>"""


LESSON = LessonSpec(
    num="08",
    title_short="ECS Anywhere",
    title_full="C8 · ECS Anywhere and Hybrid — On-Prem and Edge Capacity",
    title_html="K-ECS C8 · ECS Anywhere",
    module_eyebrow="Module C8 · the Outport Station — your hardware joins the harbor",
    hero_sub_html='<strong>ECS Anywhere</strong> registers your-own-hardware (on-prem servers, edge devices, VMs in another cloud) into an ECS Cluster as <em>external instances</em>. Workflow: SSM activation code → install SSM agent + ECS agent → external instance registers + appears in the Cluster\'s capacity. ECS schedules Tasks marked <code>requiresAttributes: EXTERNAL</code> onto external capacity. <strong>Use cases</strong>: regulated workloads on-prem, edge processing close to data, gradual cloud migration. <strong>Limits</strong>: no awsvpc, no ALB integration, no Service Connect, no Fargate. <em>Pick the workload mix carefully — ECS Anywhere is a bridge, not a destination.</em>',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. The on-prem batch processor stopped pulling work. The ECS Anywhere Cluster shows the external instance as ACTIVE, but no Tasks are running. The on-call engineer SSHes (the on-prem instance has SSH; not Fargate); finds the SSM agent stuck after a week-long outbound connectivity blip. <em>External instances don\'t self-heal connectivity the way managed AWS capacity does.</em> Today\'s lesson: ECS Anywhere is real but the operational model is different.",
    stamp_html="<strong>ECS Anywhere = control plane in AWS, capacity on your hardware. SSM + ECS agents register external instances. Networking is bridge/host (no awsvpc on external; no ALB). Pick for regulated, edge, hybrid bridge use cases — not for general-purpose workloads.</strong>",
    district_pin="kh-pier08",
    district_label="Outport Station",
    sections=[
        Section(
            eyebrow="Section 1.1 · architecture",
            h2="Control plane in AWS, capacity on your hardware",
            body_html="""    <p><strong>ECS Anywhere</strong> extends the standard ECS control plane to capacity outside AWS. Your servers — on-prem racks, edge devices in retail / industrial sites, VMs in another cloud — register as <em>external instances</em>. ECS schedules Tasks onto them as if they were EC2 capacity, with constraints filtering "external-only" workloads.</p>
    <p><strong>Communications path</strong>: external instance → outbound HTTPS to SSM Messages + ECS regional endpoints. <em>No inbound port</em> — the agents make the connection out. Behind a corporate firewall, only outbound 443 is needed (plus ICMP-based AWS health probes if Network Reachability is configured).</p>
    <p><strong>Cluster shape</strong>: one ECS Cluster can have a mix of EC2, Fargate, and external capacity providers. Services declare which capacity they want via <code>capacityProviderStrategy</code>; Tasks marked <code>requiresAttributes</code> for <code>ecs.os-type=linux</code> and the EXTERNAL filter land on external instances.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · registering an external instance",
            h2="SSM activation + agent installation",
            body_html="""    <p><strong>Step 1 — SSM activation</strong>: <code>aws ssm create-activation</code> generates a one-time activation code + ID. Activations have a default-instance-name + IAM role + region.</p>
    <p><strong>Step 2 — install agents on the server</strong>: AWS provides a single shell script that installs the SSM agent + ECS agent + activates with the SSM code. Run as root.</p>
    <pre><code>curl --proto "https" -o "/tmp/ecs-anywhere-install.sh" \\
  "https://amazon-ecs-agent.s3.amazonaws.com/ecs-anywhere-install-latest.sh"

sudo bash /tmp/ecs-anywhere-install.sh \\
  --region us-east-1 \\
  --cluster my-cluster \\
  --activation-id $ACTIVATION_ID \\
  --activation-code $ACTIVATION_CODE</code></pre>
    <p><strong>Step 3 — verification</strong>: <code>aws ssm describe-instance-information</code> shows the registered server (Instance ID like <code>mi-XXXX</code>); <code>aws ecs list-container-instances</code> shows it in the ECS Cluster. Status: ACTIVE means it\'s ready for Tasks.</p>
    <p><strong>De-registration</strong>: <code>aws ecs deregister-container-instance</code> + <code>aws ssm deregister-managed-instance</code>; uninstall the agents from the server.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · networking, storage, and known limits",
            h2="bridge/host network only; no ALB; storage on host",
            body_html="""    <p><strong>Networking limits</strong>: external instances <em>do NOT support awsvpc</em> (no VPC ENIs on your hardware). Tasks use <em>bridge</em> or <em>host</em> network mode. Inbound traffic goes to the host\'s IP + container port; firewall + DNS are your responsibility.</p>
    <p><strong>ALB integration is unsupported</strong> on external instances — ALB target type IP requires awsvpc; target type instance requires the instance to be in the VPC. For ingress to external instance Tasks, options are: (a) on-prem load balancer in front, (b) DNS round-robin, (c) Tasks publishing to a queue / event bus.</p>
    <p><strong>Service Connect is not supported</strong> on external — east-west service discovery for external Tasks rolls over to Cloud Map (DNS) only.</p>
    <p><strong>Storage</strong>: bind mounts to host paths work fine. EFS / FSx are AWS-cloud-only; not directly mountable on external. For shared state across cloud + on-prem, use S3 + S3 Gateway endpoint at the cloud side and S3 SDK calls from on-prem (or design for asynchronous handoff).</p>
    <p><strong>Operational</strong>: external instances don\'t auto-heal — if the SSM agent dies or connectivity is lost, the instance disappears from the Cluster but ECS doesn\'t replace it (you\'re running it, not AWS). Capacity providers + managed scaling don\'t apply to external. <em>Treat external instances as carefully provisioned long-lived workers.</em></p>"""
        ),
        Section(
            eyebrow="Section 1.4 · use cases + selection criteria",
            h2="When ECS Anywhere fits — and when it doesn\'t",
            body_html="""    <p><strong>Strong fit</strong>:</p>
    <ul>
      <li><em>Regulated workloads on-prem</em> — data residency rules forbid cloud; ECS control plane orchestrates locally-running containers under one Cluster you can also run cloud workloads in.</li>
      <li><em>Edge processing</em> — retail stores, factory floors, oilfield sensors; one ECS Cluster orchestrates per-site capacity for local data processing; periodic results upload to cloud.</li>
      <li><em>Gradual cloud migration</em> — register existing on-prem servers into a new Cluster; deploy on both old + new gradually; decommission on-prem capacity as cloud takes over.</li>
      <li><em>Hybrid burst</em> — steady on-prem + cloud burst; same Task Definitions deploy both places; capacity-provider strategy allocates per workload.</li>
    </ul>
    <p><strong>Weak fit (don\'t pick)</strong>:</p>
    <ul>
      <li>General-purpose web services — ALB + awsvpc + Service Connect missing kills the modern operational model.</li>
      <li>Workloads needing EFS / FSx / RWX cross-Task storage — those are cloud-side only.</li>
      <li>High-churn workloads — external instance churn is your operational burden; managed cloud capacity is more efficient.</li>
    </ul>
    <p><strong>Bottom line</strong>: ECS Anywhere is a <em>bridge</em>. Pick when you have specific reasons to keep capacity outside AWS; don\'t pick because it sounds easier than managing standalone Docker hosts.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="What network connectivity does an external instance need?",
            options=[
                ("Inbound TCP 443 from AWS to the instance.", False),
                ("Outbound HTTPS to SSM Messages + ECS endpoints; no inbound from AWS.", True),
                ("VPN tunnel from on-prem to AWS.", False),
            ],
            feedback="The agents make outbound HTTPS connections; AWS never reaches inbound to your server. This is what makes ECS Anywhere firewall-friendly behind corporate networks.",
        ),
        3: PauseCheck(
            question="A team wants to use ECS Anywhere for their next general-purpose web service. Why is this probably the wrong fit?",
            options=[
                ("ECS Anywhere is too new.", False),
                ("No awsvpc + no ALB + no Service Connect — operational model is materially weaker.", True),
                ("ECS Anywhere doesn\'t support Linux containers.", False),
            ],
            feedback="External instances don\'t support awsvpc, ALB integration, or Service Connect. For a workload that benefits from those, plain ECS on Fargate or EC2 is the right fit.",
        ),
    },
    before_after_before='<p>Pre-ECS-Anywhere, hybrid workloads ran two separate orchestrators: ECS in the cloud, plain Docker / Compose / Swarm on-prem. Two operational models, two deploy pipelines, two monitoring stacks. Drift was constant. Migrating workload between environments meant rewriting the orchestration layer.</p>',
    before_after_after='<p>Modern ECS Anywhere keeps the control plane unified — one Cluster, one set of Task Definitions, one deployment workflow, one monitoring story. Capacity providers split the difference: cloud + on-prem capacity in one strategy. <em>The orchestrator stops being a per-environment burden.</em> Limits remain (networking surface narrower on external) but the bridge use case is well-served.</p>',
    before_after_caption='<p class="ba-caption"><em>ECS Anywhere is a real product, not a sales-deck checkbox. Use it for the bridge cases it\'s designed for; don\'t default to it for everything.</em></p>',
    analogy_intro_html='''<p>The harbor isn\'t the only place ships dock. Some captains have private wharves at remote islands or up in the river estuary. The <strong>Outport Station</strong> is how those private wharves get registered into the K-Harbor system.</p>
    <p>The harbor master sends a <em>signed activation slip</em> (SSM activation code) to the wharf owner; the wharf owner installs two pieces of harbor equipment on their dock — a <strong>radio reporter</strong> (SSM agent) and a <strong>cargo handler</strong> (ECS agent) — and uses the slip to introduce the wharf to the harbor master. From then on, the wharf appears on the harbor map; the harbor master can route ships to it just like any harbor pier.</p>
    <p>But: it\'s still a private wharf, not a harbor pier. <strong>The harbor\'s shared comms tower (awsvpc + Service Connect)</strong> doesn\'t reach the wharf — local communications are by megaphone (bridge mode) or shouting from the deck (host network). <strong>The harbor\'s entrance flag tower (ALB)</strong> can\'t see ships at the wharf — incoming traffic from the open sea has to be handled by the wharf owner\'s own signal system. <strong>The shared warehouse (EFS)</strong> is on the harbor side; cargo at the wharf can\'t directly access it.</p>
    <p>The wharf is great when the cargo has to stay off-harbor for legal reasons (data residency), or when the wharf is closer to the source (edge processing), or when the wharf is being phased into the harbor over time (gradual migration). For everyday cargo work, it\'s simpler to dock at the harbor proper.</p>''',
    translation_rows=[
        ("Outport Station", "ECS Anywhere registration layer"),
        ("Private wharf at a remote island", "external instance (on-prem / edge / other cloud)"),
        ("Signed activation slip", "SSM activation code + ID"),
        ("Radio reporter on the wharf", "SSM agent on external instance"),
        ("Cargo handler on the wharf", "ECS agent on external instance"),
        ("Wharf appears on harbor map", "external instance ACTIVE in Cluster"),
        ("Harbor\'s shared comms tower (out of reach)", "awsvpc network mode (unsupported on external)"),
        ("Harbor\'s flag tower (out of reach)", "ALB integration (unsupported on external)"),
        ("Megaphone / shouting from deck", "bridge / host network mode"),
        ("Wharf-side cargo (cloud warehouse out of reach)", "EFS / FSx (cloud-only; not on external)"),
        ("Mixed flotilla — harbor + wharf assignments", "capacity provider strategy with EXTERNAL + Fargate / EC2"),
    ],
    analogy_stops="A real wharf is permanent capacity; ECS external instances disconnect when the agent stops or connectivity is lost — they vanish from the Cluster. There\'s no \"empty wharf\" — the wharf disappears from the harbor map.",
    eli5="Some captains have private docks far from the harbor. The harbor master can still send them ships if they install harbor radios. But the private docks don\'t get the harbor\'s loudspeakers, the harbor\'s flag tower, or the harbor\'s shared warehouse. They\'re great for cargo that has to stay near the private dock, but harder for general-purpose work.",
    eli10="<strong>ECS Anywhere</strong>: external instances (on-prem / edge / other cloud) join an ECS Cluster via <code>SSM agent + ECS agent</code> + an SSM activation code. <strong>Limits</strong>: no awsvpc, no ALB, no Service Connect, no Fargate, no EFS / FSx. <strong>Network modes</strong>: bridge / host / none. <strong>Storage</strong>: host filesystem only. <strong>Use cases</strong>: data-residency, edge, gradual migration, hybrid burst. <strong>Don\'t use for</strong>: general web services where the missing surface kills the operational model.",
    scenarios=[
        Scenario(
            name="Edge — retail store inventory processor",
            body="A retailer has 800 stores. Each store\'s back-office runs a small server processing point-of-sale data; results upload to cloud nightly. <strong>ECS Anywhere</strong>: each store is an external instance in a regional ECS Cluster; same Task Definitions deploy to all 800. <em>One Cluster + one CI pipeline; no per-store orchestration tooling.</em>",
        ),
        Scenario(
            name="Compliance — healthcare analytics on-prem",
            body="A health system can\'t move PHI to cloud. They run analytics Tasks on-prem racks; results aggregated to cloud (de-identified). ECS Anywhere keeps the orchestration unified — same TDs, same deploy story, same observability stack — while keeping data on regulated hardware. <em>Compliance + operational sanity.</em>",
        ),
        Scenario(
            name="Migration bridge — gradual cloud move over 18 months",
            body="A team migrating 40 services from on-prem to cloud. Phase 1: register on-prem servers as external; deploy ECS Tasks side-by-side with the legacy systemd-managed processes. Phase 2: spin up Fargate capacity in the same Cluster; capacity-provider strategy weights cloud-first, external-fallback. Phase 3: drain external; deregister. <em>The Cluster shape never changed; capacity moved underneath.</em>",
        ),
        Scenario(
            name="Bad fit — \"replace Docker Compose with ECS Anywhere\" for a web app",
            body="A team running a 5-service web app on a single on-prem server in Compose tried ECS Anywhere as a \"pro upgrade.\" Lost ALB integration, lost service mesh, lost shared volumes across services (no EFS-equivalent). Operational complexity rose without orchestration value. <em>Postmortem</em>: stay on Compose for this case; pick ECS in the cloud or EKS if you want a real orchestrator.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"ECS Anywhere lets me run Fargate on-prem.\"",
            truth="No. <strong>Fargate is AWS-managed cloud capacity</strong>; it doesn\'t exist outside AWS. ECS Anywhere lets you register your own hardware as <em>external</em> capacity in an ECS Cluster. The Tasks running on external instances run on your hardware; the Cluster\'s control plane stays in AWS.",
        ),
        Misconception(
            myth="\"External instances support all ECS features.\"",
            truth="Significant limits: <strong>no awsvpc, no ALB, no Service Connect, no EFS / FSx, no managed scaling</strong>. Plan workload selection accordingly; ECS Anywhere is a bridge for specific use cases, not a drop-in equivalent of cloud-side ECS.",
        ),
        Misconception(
            myth="\"External instances self-heal like EC2 ASG.\"",
            truth="External instances are <strong>your operational responsibility</strong>. If the agent dies, the host crashes, or connectivity drops, ECS removes the instance from capacity but doesn\'t replace it. You run it; you fix it. (Capacity providers + managed scaling don\'t apply to external.)",
        ),
    ],
    flashcards=[
        Flashcard(front="Two agents an external instance needs?", back="<strong>SSM agent</strong> (registers + maintains channel back to AWS) + <strong>ECS agent</strong> (manages Task lifecycle on the host). The AWS install script installs both."),
        Flashcard(front="What does <code>aws ssm create-activation</code> produce?", back="A one-time <strong>activation code + activation ID</strong> used by the agent install script to register the host into SSM (and thereby into the ECS Cluster)."),
        Flashcard(front="What network direction is required for ECS Anywhere?", back="<strong>Outbound HTTPS only</strong> to SSM Messages + ECS regional endpoints. No inbound from AWS to your hardware. Firewall-friendly."),
        Flashcard(front="Three network modes supported on external instances?", back="<strong>bridge</strong> (Docker bridge), <strong>host</strong> (host network namespace), <strong>none</strong>. <em>awsvpc is NOT supported</em> on external."),
        Flashcard(front="Can external instances integrate with ALB?", back="No. ALB target type IP requires awsvpc; target type instance requires the instance be in a VPC. External instance Tasks need on-prem LB or DNS round-robin or queue-based ingress instead."),
        Flashcard(front="Strong-fit ECS Anywhere use cases?", back="<strong>Regulated on-prem (data residency)</strong>, <strong>edge processing (retail / factory / oilfield)</strong>, <strong>gradual cloud migration bridge</strong>, <strong>hybrid burst (steady on-prem + cloud burst)</strong>."),
        Flashcard(front="Weak-fit cases (don\'t pick ECS Anywhere)?", back="General-purpose web services (lose ALB + awsvpc + Service Connect), workloads needing EFS / FSx (cloud-side only), high-churn workloads (external operational burden = yours)."),
        Flashcard(front="What\'s the requiresAttributes filter for external Tasks?", back="<code>requiresAttributes</code> array on a Task Definition can include <code>ecs.os-type=linux</code> + <code>ecs.cluster-resources</code> conditions. The EXTERNAL launch type filter routes Tasks to external capacity within a multi-launch-type Cluster."),
    ],
    quizzes=[
        Quiz(
            prompt="A team wants to register 50 retail-store on-prem servers as external instances. What\'s the operational pattern that scales?",
            answer="(1) <strong>Pre-shared activation</strong>: create one SSM activation per store (or a few shared activations with high registration limits); deliver the activation IDs + codes to each store via secure config management (SSM Parameter Store fetch from cloud, secrets distribution tool). (2) <strong>Automated agent install</strong>: bake the install script into the store\'s base image / config-management playbook so new servers register on first boot. (3) <strong>Cluster naming</strong>: one ECS Cluster per region (or per tenant) with all stores in it; use ECS attributes to tag store-id (e.g., <code>store=4521</code>) so Task placement can target individual stores. (4) <strong>Monitoring</strong>: alarm on per-store \"external instance count\" dropping (lost connectivity at a store). (5) <strong>De-registration runbook</strong>: when a store closes, run deregister-container-instance + SSM deregister-managed-instance + uninstall agents.",
        ),
        Quiz(
            prompt="An external instance shows ACTIVE in the Cluster but ECS isn\'t scheduling Tasks onto it. The Service has 5 desired Tasks; only 3 are running. What\'s the diagnostic?",
            answer="Check in order: (1) <strong>Task Definition launch type compatibility</strong> — is <code>EXTERNAL</code> in the <code>requiresCompatibilities</code> array? If only <code>EC2</code>, the scheduler won\'t place on external. (2) <strong>Capacity provider strategy</strong> — is the Service\'s strategy including the external capacity provider, or is it Fargate-only? (3) <strong>Resources on the instance</strong> — does the external host have free CPU + memory matching the Task requirements? <code>describe-container-instances</code> shows registered + remaining resources. (4) <strong>Placement constraints</strong> — does the Service have constraints filtering only certain attributes the external instance lacks? (5) <strong>Network mode</strong> — is the Task Definition using awsvpc? External doesn\'t support it; Task can\'t place. (6) <strong>External instance status detail</strong> — agent connection status; SSM agent / ECS agent process state; outbound 443 connectivity from the host.",
        ),
        Quiz(
            prompt="Leadership says: \"We\'re mid-cloud-migration. Move all on-prem workloads to ECS Anywhere this quarter — same orchestrator everywhere.\" The fleet has 60 services, 40 of which are public web. Defend a more conservative plan.",
            answer="\"<strong>The blanket-move would lose us important operational machinery on the 40 public-web services.</strong> ECS Anywhere is right for: regulated on-prem, edge, hybrid bridge, gradual migration. It\'s wrong for: general public-web (no ALB integration, no awsvpc + SG-per-Task, no Service Connect, no EFS for shared state). For the 40 public-web services, we should: (1) keep them on-prem temporarily on whatever they\'re running today, (2) migrate them <em>directly to cloud Fargate</em> via standard refactor (containerise + register with cloud Cluster), and (3) bypass the ECS-Anywhere step entirely. The remaining 20 (batch + edge + regulated) are real ECS Anywhere candidates. <strong>Phased plan</strong>: first the 20 onto Anywhere this quarter (low risk, real value), then the 40 onto cloud Fargate over next two quarters (more refactor, but the destination is the right shape). Forcing all 60 through Anywhere now means rebuilding ALB integrations afterward — wasted work.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer defended the conservative plan",
        ),
    ],
    glossary=[
        GlossaryItem(name="ECS Anywhere", definition="ECS feature registering on-prem / edge / other-cloud hardware as external instances in an ECS Cluster."),
        GlossaryItem(name="external instance", definition="An ECS-registered host that\'s not EC2 or Fargate. Identified by mi-XXXX SSM Instance ID."),
        GlossaryItem(name="SSM activation", definition="One-time code + ID for registering a managed instance into SSM. Bridges to ECS Anywhere registration."),
        GlossaryItem(name="ECS agent on external", definition="The standard ECS agent binary running on your hardware; same protocol as on EC2."),
        GlossaryItem(name="EXTERNAL launch type", definition="Task Definition + capacity-provider concept routing Tasks to external instances."),
        GlossaryItem(name="bridge network mode", definition="Docker bridge networking; supported on external instances. Containers share host\'s ENI; ports mapped."),
        GlossaryItem(name="host network mode", definition="Container uses host\'s network namespace directly; supported on external. hostPort = containerPort."),
        GlossaryItem(name="data residency", definition="Compliance requirement that data stay in a geographic / legal jurisdiction. A common ECS Anywhere driver."),
        GlossaryItem(name="capacity-provider strategy with EXTERNAL", definition="Mixed-capacity Service that can land Tasks on external + cloud capacity per strategy weights."),
        GlossaryItem(name="ECS attribute", definition="Key-value tag on a container instance (built-in or custom). Used in placement constraints to target hosts."),
    ],
    recap_lead="ECS Anywhere extends the ECS control plane to your hardware via SSM + ECS agents. Strong fit for regulated on-prem, edge, gradual migration, hybrid burst. Limits (no awsvpc, no ALB, no Service Connect) mean general-purpose web services should stay on cloud-side ECS or EKS.",
    recap_next='<strong>Next — C9: ECS Troubleshooting.</strong> Tasks stuck PROVISIONING / PENDING (ENI, image pull, IAM); stoppedReason taxonomy (CannotPullContainerError, ResourceInitializationError, OutOfMemoryError); deployment circuit breaker firings; Service Connect endpoint issues; ALB target health failures.',
)
