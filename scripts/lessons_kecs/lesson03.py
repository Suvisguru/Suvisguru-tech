"""K-ECS C3 — ECS Networking (network modes, awsvpc, Service Connect, ALB/NLB, VPC Lattice)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS networking — awsvpc ENI per Task + Service Connect + ALB target type IP + VPC Lattice.">
  <rect x="20" y="20" width="720" height="200" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Lookout & Comms · K-Harbor — every Task gets its own ENI; Service Connect handles east-west</text>
  <rect x="40" y="70" width="180" height="140" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="130" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">awsvpc (recommended)</text>
  <text x="130" y="112" text-anchor="middle" font-size="9" fill="#FBF1D6">ENI per Task</text>
  <text x="130" y="128" text-anchor="middle" font-size="9" fill="#FBF1D6">SG per Task</text>
  <text x="130" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">required for Fargate</text>
  <text x="130" y="170" text-anchor="middle" font-size="9" fill="#FBF1D6">subnet-aware</text>
  <text x="130" y="190" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">VPC-native networking</text>
  <rect x="240" y="70" width="180" height="140" rx="10" fill="#3878B5" stroke="#1F2433"/>
  <text x="330" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Service Connect</text>
  <text x="330" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">modern east-west</text>
  <text x="330" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">service discovery + LB</text>
  <text x="330" y="140" text-anchor="middle" font-size="9" fill="#FBF1D6">retries + timeouts</text>
  <text x="330" y="158" text-anchor="middle" font-size="9" fill="#FBF1D6">app-level metrics</text>
  <text x="330" y="178" text-anchor="middle" font-size="9" fill="#FBF1D6">replaces App Mesh</text>
  <text x="330" y="198" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">sidecar Envoy proxy</text>
  <rect x="440" y="70" width="140" height="140" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="510" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">ALB / NLB</text>
  <text x="510" y="108" text-anchor="middle" font-size="9" fill="#1F2433">north-south traffic</text>
  <text x="510" y="124" text-anchor="middle" font-size="9" fill="#1F2433">target type: IP</text>
  <text x="510" y="140" text-anchor="middle" font-size="9" fill="#1F2433">(in awsvpc)</text>
  <text x="510" y="158" text-anchor="middle" font-size="9" fill="#1F2433">target type: instance</text>
  <text x="510" y="174" text-anchor="middle" font-size="9" fill="#1F2433">(bridge / host)</text>
  <text x="510" y="194" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">+ Cloud Map (legacy)</text>
  <rect x="600" y="70" width="120" height="140" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="660" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">VPC Lattice</text>
  <text x="660" y="108" text-anchor="middle" font-size="9" fill="#1F2433">cross-VPC,</text>
  <text x="660" y="122" text-anchor="middle" font-size="9" fill="#1F2433">cross-account</text>
  <text x="660" y="138" text-anchor="middle" font-size="9" fill="#1F2433">app networking</text>
  <text x="660" y="158" text-anchor="middle" font-size="9" fill="#1F2433">no peering</text>
  <text x="660" y="178" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">+ ECS targets</text>
</svg>"""


LESSON = LessonSpec(
    num="03",
    title_short="ECS networking",
    title_full="C3 · ECS Networking — Network Modes, Service Connect, ALB/NLB, VPC Lattice",
    title_html="K-ECS C3 · ECS Networking",
    module_eyebrow="Module C3 · the Lookout & Comms Tower — every Task gets its own ENI",
    hero_sub_html='<strong>awsvpc</strong> is the recommended network mode (and required for Fargate): each Task gets its own ENI in your VPC and its own Security Group. Three other modes exist (bridge, host, none) — bridge + host are EC2-launch-only legacy. <strong>Service Connect</strong> is the modern east-west traffic layer (service discovery + L7 load balancing + retries + timeouts + app-level metrics) — replaces App Mesh patterns. <strong>Service Discovery via Cloud Map</strong> is the legacy DNS-based path. <strong>ALB / NLB</strong> integration uses target type IP for awsvpc Tasks; <strong>VPC Lattice</strong> connects services across VPCs and accounts without peering.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. The bridge-mode legacy service has 50 Tasks crammed onto 5 EC2 hosts. The platform team adds a new Task with the same hostPort 8080. ECS scheduler can\'t place anywhere — every host\'s 8080 is already taken. Service stays at 9/10 desired. Latency tail explodes. <em>Bridge mode\'s static port mapping caught up with you.</em> Today\'s lesson: pick awsvpc and let every Task have its own ENI.",
    stamp_html="<strong>awsvpc network mode is the recommended default — ENI per Task, SG per Task, required for Fargate. Service Connect is the modern east-west pattern (replaces App Mesh). ALB target type = IP for awsvpc Tasks. VPC Lattice for cross-VPC / cross-account application networking.</strong>",
    district_pin="kh-pier03",
    district_label="Lookout & Comms Tower",
    sections=[
        Section(
            eyebrow="Section 1.1 · network modes",
            h2="bridge, host, awsvpc (recommended), none",
            body_html="""    <p><strong>awsvpc</strong> (recommended): every Task gets its own <em>elastic network interface (ENI)</em> inside one of your VPC subnets. Each Task has its own private IP, its own Security Group(s), and behaves like a tiny EC2 instance from the network\'s perspective. <em>Required for Fargate.</em> Subnet-aware — the Service\'s <code>networkConfiguration</code> lists which subnets and SGs Tasks land in.</p>
    <p><strong>bridge</strong> (EC2 launch only; legacy): the default Docker bridge. Containers share the host\'s ENI; ports are mapped (containerPort → ephemeral hostPort). <em>Hostport collision</em> if two Tasks bind the same port on one host. ALB target type = instance (port range). <em>Avoid for new workloads.</em></p>
    <p><strong>host</strong> (EC2 launch only): containers use the host\'s network namespace directly; <code>hostPort</code> = <code>containerPort</code>. <em>Even more collision-prone</em> — a single Task per port per host. Used historically for sidecar agents that must see the host\'s network.</p>
    <p><strong>none</strong>: no network. Only for batch Tasks that don\'t need network (e.g., they read from S3 via VPC endpoint accessed by the agent\'s host network). Rare.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · awsvpc deep dive",
            h2="ENI per Task, SG per Task, ENI limits, awsvpc trunking",
            body_html="""    <p>In awsvpc, the ECS agent provisions an ENI for the Task before the container starts (Task state PROVISIONING). The ENI is attached to the host (EC2 or Fargate microVM); the Task\'s containers see only that ENI; outbound traffic flows through the VPC route tables.</p>
    <p><strong>SG per Task</strong> is the win — different Tasks on the same host can have completely different ingress/egress rules. The SG is set in the Service\'s <code>networkConfiguration.awsvpcConfiguration.securityGroups</code>. <em>Pre-awsvpc, the SG was a host-level shared concern; now it scopes to the workload.</em></p>
    <p><strong>ENI limits</strong> (EC2 launch only): each EC2 instance has a max ENI count tied to its instance type (e.g., m5.large = 3 ENIs incl. the host\'s primary). Each Task takes one ENI. Trunking — the <strong>awsvpc trunking</strong> feature — lets supported instance types attach a "trunk" ENI that multiplexes many sub-ENIs, raising effective Task density per host. <em>Enable in ECS account settings; opt-in.</em></p>
    <p><strong>Fargate</strong> doesn\'t expose ENI limits to you — each Fargate Task is one microVM with one ENI; there\'s no host-density constraint. The Fargate platform handles VPC routing, ENI lifecycle, and egress IP assignment.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Service Connect + Service Discovery (Cloud Map)",
            h2="Modern east-west and the legacy DNS path",
            body_html="""    <p><strong>Service Connect</strong> (the recommended modern path) wires up east-west service-to-service traffic with a sidecar Envoy proxy. Configure on a per-Service basis: <code>serviceConnectConfiguration</code> declares a namespace and the names this Service publishes / consumes. Tasks call <code>http://service-b.cluster:8080</code>; the Service Connect proxy resolves it to a healthy Task ENI, load-balances, applies timeouts + retries, and emits app-level metrics (rps / latency / 5xx) into CloudWatch + Container Insights. <em>Replaces App Mesh patterns; no separate mesh control plane to run.</em></p>
    <p><strong>Service Discovery via Cloud Map</strong> (legacy but still supported): each Service registers Task ENIs as A records in a Cloud Map private DNS namespace (e.g., <code>service-b.local</code>). Other Tasks resolve the name and connect directly. <em>No L7 features</em> — just DNS. Fine for very simple east-west; missing retries, observability, traffic shaping. Service Connect is the upgrade.</p>
    <p><strong>When to use which</strong>: Service Connect for any Service that does east-west calls. Cloud Map for simple cross-Service DNS without L7 needs. Both can coexist on the same Cluster.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · ALB / NLB integration + VPC Lattice for ECS",
            h2="north-south traffic; cross-VPC application networking",
            body_html="""    <p><strong>ALB integration</strong>: Service\'s <code>loadBalancers</code> array points each Task at a target group. Two target types matter:</p>
    <ul>
      <li><strong>IP</strong> (use with awsvpc): ALB registers Task ENI IPs directly. Stable, fast deregistration, plays well with rolling deploys + CodeDeploy blue/green.</li>
      <li><strong>instance</strong> (use with bridge / host): ALB registers EC2 instance + dynamic port. ENI doesn\'t exist per Task. Older shape; still works.</li>
    </ul>
    <p>Health checks: ALB-level (HTTP probe by ALB) <em>and</em> container healthCheck command in Task Definition. Both report into the rolling-deploy decision logic.</p>
    <p><strong>NLB</strong>: same target-type story (IP for awsvpc); used for TCP/UDP / ultra-low-latency / static IP / TLS passthrough cases. ALB is the right default for HTTP/HTTPS.</p>
    <p><strong>VPC Lattice for ECS</strong>: a managed service-to-service application-networking layer that spans VPCs and accounts <em>without VPC peering</em>. Configure a Lattice Service Network; register ECS Services as Lattice Targets. Lattice handles auth (IAM-based), encryption, observability, and routing across VPC boundaries. <em>Picks the share-services-across-accounts use case</em> that east-west Service Connect can\'t reach (it\'s scoped to one VPC + Cluster).</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A team has a Task that needs different SGs from other Tasks on the same EC2 host. Which network mode lets them do this cleanly?",
            options=[
                ("bridge — port-mapped container networking.", False),
                ("awsvpc — ENI per Task + SG per Task.", True),
                ("host — host network namespace.", False),
            ],
            feedback="awsvpc gives each Task its own ENI and SG. With bridge or host the SG is host-level and shared across all Tasks on the host.",
        ),
        3: PauseCheck(
            question="Which integration pattern is the AWS-recommended modern east-west traffic layer in ECS?",
            options=[
                ("App Mesh + Envoy sidecars per Task.", False),
                ("Service Connect (sidecar Envoy + namespace + L7 features).", True),
                ("Direct ENI-to-ENI calls with no service discovery.", False),
            ],
            feedback="Service Connect is the modern path; App Mesh is being phased down. Service Connect provides L7 LB + retries + timeouts + app-level metrics with managed Envoy sidecars.",
        ),
    },
    before_after_before='<p>Pre-awsvpc, ECS Tasks shared a host\'s ENI in bridge or host mode. Tasks colliding on hostPort. Security Groups host-level — every workload on a host had the same network policy. East-west service discovery was rolled by hand: scripts registering each Task in DNS via the agent metadata API. Cross-VPC traffic went through expensive peering or NLB endpoints. <em>Networking was an obstacle to scaling.</em></p>',
    before_after_after='<p>Modern ECS networking uses awsvpc by default (and Fargate forces it). ENI per Task; SG per Task. Service Connect handles east-west with a sidecar Envoy + L7 features + observability. ALB target type IP integrates cleanly. VPC Lattice extends application networking across VPCs and accounts. <em>Networking is just configuration.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Almost every ECS networking question collapses to: \"are you on awsvpc?\" If yes, the rest follows. If no, you\'re on a legacy path and should plan migration.</em></p>',
    analogy_intro_html='''<p>The <strong>Lookout & Comms Tower</strong> overlooks every pier in K-Harbor. The harbor master uses it to wire each ship\'s communications and route signal traffic between ships and to the outside world.</p>
    <p>In <strong>awsvpc</strong> mode, every ship at every pier gets its own radio mast (ENI) and its own access list (Security Group). Two ships at the same pier can have completely different radio rules. Compared to the <em>old shared-mast</em> approach (bridge / host modes — every ship on a dock used the dock\'s mast and had to negotiate which channel was free), awsvpc is decisively cleaner.</p>
    <p>For ship-to-ship traffic, <strong>Service Connect</strong> is a small relay station beside each ship (sidecar Envoy proxy). The relay knows which ships speak which language (which Service publishes which protocol on which port), routes the call over the radio network, retries when a ship is offline, applies timeouts, and reports back to the harbor\'s observatory (CloudWatch / Container Insights). Compared to the older Cloud Map approach (just a phone book — \"this is service-B\'s number, dial it directly\"), Service Connect gives you the smart switchboard.</p>
    <p>For ship-to-shore traffic (the public Internet calling in), there\'s a <strong>signal flag tower</strong> (ALB / NLB) at the harbor entrance. Ships register their IPs (target type IP) with the tower; the tower routes incoming calls. For talking to <em>other harbors entirely</em> — partner companies, sister offices in other regions — there\'s <strong>VPC Lattice</strong>: a managed inter-harbor switchboard that lets ships in different harbors talk to each other without needing a shared bridge.</p>''',
    translation_rows=[
        ("Lookout & Comms Tower", "ECS networking layer"),
        ("Each ship gets its own radio mast", "awsvpc ENI per Task"),
        ("Each ship\'s radio access list", "Security Group per Task"),
        ("Old shared-mast at the dock", "bridge / host network mode (legacy)"),
        ("Smart relay station beside each ship", "Service Connect sidecar Envoy proxy"),
        ("Phone book at the harbor office", "Cloud Map service discovery (DNS only)"),
        ("Signal flag tower at the harbor entrance", "ALB / NLB"),
        ("Ships registered by IP at the tower", "ALB target type = IP"),
        ("Ships registered by dock + slot", "ALB target type = instance (bridge / host)"),
        ("Inter-harbor switchboard", "VPC Lattice (cross-VPC + cross-account)"),
        ("Trunked masts (advanced docks)", "awsvpc trunking — multiplexed ENIs per host"),
    ],
    analogy_stops="A real harbor has fixed radios; ECS ENIs are software ENIs that AWS provisions and tears down per Task. There\'s no \"left-behind mast\" — when a Task stops, its ENI is gone in seconds.",
    eli5="Every ship gets its own radio. Two ships at the same dock can have totally different radio rules. When ships need to talk to each other there\'s a smart relay that knows everyone\'s phone numbers and reconnects calls if a ship is busy. When the outside world calls in, there\'s a flag tower at the harbor mouth that routes the call to the right ship.",
    eli10="<strong>awsvpc</strong> = ENI + SG per Task; required for Fargate; recommended for EC2 launch. <strong>Service Connect</strong> = managed sidecar Envoy + namespace-scoped service discovery + L7 LB + retries + timeouts + app-level metrics; replaces App Mesh. <strong>Cloud Map</strong> = legacy DNS-only service discovery; coexists. <strong>ALB target type IP</strong> = recommended for awsvpc; ALB registers Task ENI IPs directly. <strong>VPC Lattice for ECS</strong> = managed cross-VPC + cross-account application networking without peering.",
    scenarios=[
        Scenario(
            name="Polyglot fleet — Service Connect across 12 services",
            body="A 100-engineer org has 12 ECS Services on Fargate. They enable Service Connect cluster-wide; each Service publishes its name (e.g., <code>orders.cluster:8080</code>); other Services consume by name. <em>App-level metrics</em> appear automatically in Container Insights; retries handle transient deploy turbulence. Migrating from App Mesh: configure once, App Mesh sidecars retired.",
        ),
        Scenario(
            name="Compliance — SG per Task gates blast radius",
            body="A regulated workload has Tasks A (PII handler) and Tasks B (public web) on the same Cluster + same hosts. Old bridge-mode deployment had one host SG — both got the same rules. Migrating to awsvpc: Task A gets a tight SG (egress only to specific RDS + KMS endpoints), Task B gets a wide-open egress. <em>Compliance audit shifts from \"trust the host config\" to \"trust the per-Task SG.\"</em>",
        ),
        Scenario(
            name="Cross-account integration — VPC Lattice replaces peering",
            body="A platform team owns Service A in Account-1; partner team owns Service B in Account-2. Without Lattice, options were Transit Gateway + cross-account peering (3 weeks of networking work + ongoing NAT cost). With <strong>VPC Lattice</strong>: define a Lattice Service Network; register Service A as a target; share the network with Account-2; Service B in Account-2 calls A by Lattice DNS name with IAM auth. Stand-up: 1 day.",
        ),
        Scenario(
            name="Outage — bridge-mode hostPort collision blocked deploys",
            body="A team running 50 Tasks on bridge-mode EC2 hit hostPort 8080 collision when adding a new Service. Scheduler\'s desired count of 10 stalled at 8 (only 8 hosts had a free 8080). Latency on the failing Service climbed because the desired count was permanent under-provision. <em>Postmortem</em>: migrate to awsvpc. Each Task ENI eliminates the collision class entirely.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Service Connect is just App Mesh with a different name.\"",
            truth="Service Connect is a different design — managed by ECS with cluster-wide namespace + simpler config + tighter ECS integration; no separate App Mesh control plane. App Mesh is general-purpose multi-cluster mesh; Service Connect is purpose-built for ECS east-west and emits ECS-aware metrics.",
        ),
        Misconception(
            myth="\"awsvpc is only for Fargate.\"",
            truth="awsvpc is <em>required for Fargate</em> and <em>recommended for EC2 launch</em>. EC2 launch can also use awsvpc — get the same ENI-per-Task + SG-per-Task benefits on EC2 you get on Fargate. The trade is ENI density per host (mitigated by awsvpc trunking).",
        ),
        Misconception(
            myth="\"VPC Lattice is the same as VPC peering for ECS.\"",
            truth="VPC peering wires VPCs at the network layer (route tables + CIDRs). VPC Lattice is application-layer service networking — registers ECS Services as targets, handles auth (IAM), encryption, retries, observability. Lattice is for service-to-service across boundaries; peering is for raw IP routing.",
        ),
    ],
    flashcards=[
        Flashcard(front="Four ECS network modes — and which is recommended?", back="<strong>awsvpc</strong> (recommended; ENI + SG per Task; required for Fargate), <strong>bridge</strong> (Docker bridge, EC2-only legacy, port-mapped), <strong>host</strong> (host network, EC2-only, hostPort=containerPort), <strong>none</strong> (no network, batch use)."),
        Flashcard(front="What does awsvpc trunking solve?", back="EC2 ENI density. Without trunking, each Task takes one ENI from the host\'s instance-type-limited pool (e.g., m5.large = 3 ENIs total). Trunking attaches a multiplexing trunk ENI; each Task gets a sub-ENI; effective Task density per host rises by 5-10×."),
        Flashcard(front="Service Connect vs Cloud Map — when to use which?", back="<strong>Service Connect</strong> for east-west needing L7 (LB + retries + timeouts + metrics) — modern recommended path. <strong>Cloud Map</strong> for simple DNS-only east-west or workloads not yet on Service Connect; can coexist."),
        Flashcard(front="ALB target types for ECS?", back="<strong>IP</strong> for awsvpc Tasks (registers ENI IP directly — recommended). <strong>instance</strong> for bridge/host Tasks (registers EC2 + dynamic port — legacy)."),
        Flashcard(front="What does VPC Lattice add over Service Connect?", back="<strong>Cross-VPC + cross-account</strong> application-layer service networking without peering. Service Connect is single-VPC + single-Cluster; Lattice spans VPCs and accounts. Lattice adds IAM-based service auth + managed cross-boundary encryption."),
        Flashcard(front="Where is the SG configured for an awsvpc Task?", back="In the Service\'s <code>networkConfiguration.awsvpcConfiguration.securityGroups</code> array. Per-Task — applied to each Task ENI as it\'s provisioned. Different Tasks on the same host can have different SGs."),
        Flashcard(front="What happens during Task PROVISIONING in awsvpc?", back="ECS agent / Fargate requests an ENI from the configured subnets, applies the SGs, attaches it to the host, then transitions to PENDING (waiting on image pull). If ENI provisioning stalls (subnet has no free IPs / IAM denies CreateNetworkInterface) the Task hangs in PROVISIONING."),
        Flashcard(front="Service Connect — what infrastructure does it need?", back="A Cloud Map namespace per Cluster (private DNS), Service Connect enabled on the Service with <code>serviceConnectConfiguration</code> declaring published / consumed names, and a sidecar Envoy proxy injected per Task by ECS automatically."),
    ],
    quizzes=[
        Quiz(
            prompt="A migration is moving 30 ECS Services from bridge-mode to awsvpc. The platform team is worried about ENI limits on existing m5.large hosts. What\'s the path?",
            answer="Three options, in increasing operational ambition. (1) <strong>Right-size to instances with higher ENI ceilings</strong> — m5.4xlarge = 8 ENIs, m6i.8xlarge = 15 — accept the host-density trade for the cleaner Task isolation. (2) <strong>Enable awsvpc trunking</strong> in ECS account settings; supported instance types attach a trunk ENI multiplexing many sub-ENIs; effective Task density per host rises 5-10×. (3) <strong>Move to Fargate</strong> for some Services — no ENI density worry at all; per-Task pricing premium accepted. Most teams pick a mix: trunking for EC2-launch baseline, Fargate for new Services + bursty workloads.",
        ),
        Quiz(
            prompt="An old Service on Cloud Map DNS is failing intermittently — Task A calls Task B and gets timeouts ~5% of the time during deploys. The team wants to move to Service Connect. What changes?",
            answer="Service Connect adds three things on top of DNS: (1) <strong>L7 retries</strong> — the sidecar Envoy retries idempotent requests transparently; transient deploy-window failures disappear from caller logs. (2) <strong>Connection pooling + warm connections</strong> — no DNS-cache TTL surprise during scale-out / scale-in. (3) <strong>App-level metrics</strong> — caller sees rps + latency + 5xx per upstream service in Container Insights without instrumenting the app. Migration: enable Service Connect on each Service; Tasks call <code>service-b.namespace:port</code> as before; behind the scenes the Envoy handles the rest. Cloud Map can stay registered if you want both code paths; or retire it once Service Connect is proven.",
        ),
        Quiz(
            prompt="A platform team accidentally added a permissive 0.0.0.0/0 egress rule to a Task SG that should only egress to a specific S3 VPC endpoint. The compliance auditor flagged it. They\'re considering disabling awsvpc and putting the workload on bridge mode \"to make SG less risky.\" Talk them out of it.",
            answer="\"<strong>Going back to bridge mode is the wrong direction — it makes the auditor\'s job harder, not easier.</strong> In bridge mode, the SG is at the EC2 host level; <em>every Task on that host shares the SG</em>. We\'d either lock down the host SG (breaking other Tasks) or leave the host SG wide-open (breaking compliance). The fix is to <em>fix the awsvpc SG</em>: tighten the egress rules on this Task\'s SG to only the S3 VPC endpoint prefix list. SG-per-Task is exactly what audit wants — workload-scoped network policy that we can show in change history. Reverting to bridge would lose us this and force years of compliance back-fill.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer talked the team off the ledge",
        ),
    ],
    glossary=[
        GlossaryItem(name="awsvpc network mode", definition="ENI per Task + SG per Task. Required for Fargate; recommended for EC2 launch."),
        GlossaryItem(name="ENI", definition="Elastic Network Interface — virtual NIC inside a VPC subnet. Each awsvpc Task gets one."),
        GlossaryItem(name="awsvpc trunking", definition="Multiplexes many sub-ENIs onto one trunk ENI on supported EC2 instance types. Raises Task density."),
        GlossaryItem(name="Service Connect", definition="Modern east-west service mesh for ECS — sidecar Envoy + Cloud Map namespace + L7 LB + retries + timeouts + metrics. Replaces App Mesh."),
        GlossaryItem(name="Cloud Map", definition="AWS service discovery — DNS / HTTP API for Tasks. Legacy ECS east-west path; Service Connect uses Cloud Map under the hood."),
        GlossaryItem(name="ALB target type IP", definition="ALB target group registers Task ENI IPs (awsvpc) directly. Stable, fast deregistration; recommended."),
        GlossaryItem(name="ALB target type instance", definition="ALB registers EC2 instance + dynamic port (bridge / host modes). Legacy."),
        GlossaryItem(name="VPC Lattice for ECS", definition="Managed application-layer service networking spanning VPCs and accounts without peering. ECS Services register as Lattice Targets."),
        GlossaryItem(name="Service Connect namespace", definition="Cloud Map private namespace scoping a set of services for east-west DNS. One per Cluster typically."),
        GlossaryItem(name="Security Group per Task", definition="In awsvpc, the SG attached to the Task\'s ENI — workload-scoped network policy. Configurable in Service networkConfiguration."),
    ],
    recap_lead="ECS networking pivots on awsvpc — ENI + SG per Task. Service Connect for east-west. ALB target type IP for north-south. VPC Lattice for cross-VPC + cross-account. Bridge / host modes are EC2-launch legacy; migrate when possible.",
    recap_next='<strong>Next — C4: IAM and Security.</strong> Task execution role vs task role; Secrets Manager / SSM Parameter Store injection; KMS; ECR auth; private registry auth; SGs; Fargate platform versions and patching; VPC endpoints; compliance (PCI, HIPAA, FedRAMP).',
)
