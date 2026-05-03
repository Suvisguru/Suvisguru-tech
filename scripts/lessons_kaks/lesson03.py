"""K-AKS A3 — AKS Networking (Azure CNI variants, private clusters, AGIC vs AGC, NetworkPolicy)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AKS networking — CNI variants, ingress paths, NetworkPolicy.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Pathways &amp; Quad — AKS networking surfaces</text>
  <rect x="50" y="60" width="200" height="130" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="150" y="82" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">CNI choice</text>
  <text x="150" y="100" text-anchor="middle" font-size="9" fill="#FBF7F0">Azure CNI (real VNet IP)</text>
  <text x="150" y="115" text-anchor="middle" font-size="9" fill="#FBF7F0">Azure CNI Overlay (default)</text>
  <text x="150" y="130" text-anchor="middle" font-size="9" fill="#FBF7F0">Azure CNI + Cilium dataplane</text>
  <text x="150" y="145" text-anchor="middle" font-size="9" fill="#FBF7F0">BYO CNI (advanced)</text>
  <text x="150" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF7F0">Kubenet (legacy, deprecated)</text>
  <rect x="270" y="60" width="200" height="130" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="370" y="82" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">ingress / north-south</text>
  <text x="370" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Standard LB (L4)</text>
  <text x="370" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">internal LB · NAT GW</text>
  <text x="370" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">AGIC (App GW v1, legacy)</text>
  <text x="370" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">AGC (Gateway API, modern)</text>
  <text x="370" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FFFFFF">Web App Routing add-on</text>
  <rect x="490" y="60" width="220" height="130" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="600" y="82" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">control / east-west</text>
  <text x="600" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Private cluster (Private Link)</text>
  <text x="600" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">API VNet Integration</text>
  <text x="600" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">Authorized IP ranges</text>
  <text x="600" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">NetworkPolicy: Azure / Calico / Cilium</text>
  <text x="600" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FFFFFF">SNAT-exhaustion is the classic outage</text>
</svg>"""


LESSON = LessonSpec(
    num="03",
    title_short="AKS networking",
    title_full="A3 · AKS Networking (Azure CNI, AGC, NetworkPolicy, private clusters)",
    title_html="K-AKS A3 · AKS Networking",
    module_eyebrow="Module A3 · the campus pathways and quad",
    hero_sub_html='Three networking surfaces: <strong>CNI choice</strong> (Azure CNI / Overlay / Cilium / BYO; Kubenet legacy), <strong>ingress</strong> (Standard LB, internal LB, NAT Gateway, AGIC, Application Gateway for Containers, Web App Routing add-on), and <strong>control</strong> (private cluster via Private Link, API VNet Integration, authorized IP ranges, NetworkPolicy via Azure / Calico / Cilium). SNAT exhaustion is the most common outage.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It's 3 AM. Outage: <em>\"Pods can\'t reach external APIs — SNAT port allocation failures.\"</em> A burst of egress traffic exhausted the cluster\'s shared SNAT pool on the Standard Load Balancer. Two services that hammer external APIs are starving everyone else; new connections from any Pod fail. You realise nobody attached a NAT Gateway. Today\'s lesson: pick the right networking topology before this happens, not after.",
    stamp_html="<strong>Three surfaces: CNI (default Overlay; Cilium for performance), ingress (AGC + Gateway API > AGIC), control (private cluster + API VNet Integration). Always plan IP space and outbound (NAT Gateway, not LB SNAT).</strong>",
    district_pin="kc-wing03",
    district_label="Pathways &amp; Quad",
    sections=[
        Section(
            eyebrow="Section 1.1 · CNI choice",
            h2="CNI choice — five options, default is Overlay",
            body_html="""    <p>Pods need IPs and routing. AKS gives you five CNI options:</p>
    <ul>
      <li><strong>Azure CNI</strong> (legacy default, traditional) — every Pod gets a real IP from the node\'s subnet. <em>Fast, no overlay, but burns IPs</em> (one VNet IP per Pod). Fine for small clusters; doesn\'t scale to large ones.</li>
      <li><strong>Azure CNI Overlay</strong> (current default) — Pods get IPs from a separate <em>overlay</em> CIDR (not in the VNet). Node IPs stay in the VNet; Pod-to-Pod traffic is encapsulated inside VXLAN-like overlay. <em>Solves the IP-exhaustion problem.</em> Some Azure-native integrations (e.g. App Gateway v1 backend pools) need extra hops; AGC handles overlay correctly.</li>
      <li><strong>Azure CNI Powered by Cilium</strong> — Azure CNI for IPAM (real VNet IPs OR overlay), Cilium for the dataplane (eBPF, no kube-proxy needed, NetworkPolicy + observability). <em>Performance + visibility</em>; AKS Automatic uses this by default.</li>
      <li><strong>BYO CNI</strong> — install your own (Calico, Cilium upstream, etc.). Advanced; you own all IPAM + lifecycle. Rare in production.</li>
      <li><strong>Kubenet</strong> — legacy, NAT-on-node model. <em>Deprecated 2024</em>; do not use for new clusters.</li>
    </ul>
    <p><strong>IP planning:</strong> overlay decouples Pod IPs from VNet — you can fit a 10K-node cluster in a /24 VNet. But if you use traditional Azure CNI, do the math: <code>nodes × pods-per-node ≤ subnet capacity</code>. <strong>Pod subnet</strong> (separate from node subnet) is supported with Azure CNI for finer-grained segmentation.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · ingress paths",
            h2="Four ingress paths — pick AGC for new",
            body_html="""    <p>How does outside traffic reach your Pods? Four paths in increasing modernity:</p>
    <ul>
      <li><strong>Standard Load Balancer</strong> (L4) — every <code>Service: type=LoadBalancer</code> provisions one. Public or internal. Backend = Pod IPs (with Azure CNI / Overlay). The cluster\'s outbound SNAT also runs through this LB unless you set the outbound type to NAT Gateway.</li>
      <li><strong>NAT Gateway</strong> (outbound, recommended) — separate Azure resource for egress. Each NAT Gateway provides up to 64K SNAT ports per attached IP, scaling far beyond the LB-shared default. <em>Avoids the SNAT-exhaustion outage class.</em></li>
      <li><strong>AGIC — Application Gateway Ingress Controller</strong> (legacy path) — AKS controller that programs an Application Gateway v1 to route Ingress objects. Works, but slated for end-of-life as Application Gateway for Containers takes over.</li>
      <li><strong>Application Gateway for Containers (AGC)</strong> + Gateway API (modern path) — purpose-built L7 LB for K8s. Configured via <strong>Gateway API</strong> (HTTPRoute, TCPRoute) — the K8s-blessed successor to Ingress. Faster reconcile, native Azure integration.</li>
      <li><strong>Web Application Routing add-on</strong> — managed NGINX inside the cluster + cert-manager + Azure DNS integration. Useful for self-hosted ingress without third-party Helm charts.</li>
    </ul>
    <p><strong>Decision rule:</strong> new clusters → AGC + Gateway API for L7. Existing AGIC clusters → migration plan. Internal-only services → internal LB or AGC private mode.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · private clusters + API VNet integration",
            h2="Private clusters + API VNet Integration",
            body_html="""    <p>By default the AKS apiserver has a public endpoint (FQDN like <code>mycluster-xxxxxx.hcp.eastus.azmk8s.io</code>). Two ways to lock that down:</p>
    <ul>
      <li><strong>Authorized IP ranges</strong> — public endpoint stays, firewall allows only specific CIDRs (your office VPN, your CI runners). Cheapest; no Private Link cost.</li>
      <li><strong>Private cluster</strong> — apiserver exposed via <strong>Private Link</strong> with a Private DNS zone. The FQDN resolves to a private IP inside your VNet (or a peered VNet). Public endpoint disabled entirely. Most secure; needs Private DNS hub-spoke design.</li>
      <li><strong>API Server VNet Integration</strong> (recommended modern path) — apiserver is injected into a delegated subnet of <em>your</em> VNet. No Private Link, no peering hub-spoke. Direct VNet routing. Use this for new clusters that need API isolation.</li>
    </ul>
    <p><strong>Outbound types:</strong> <code>loadBalancer</code> (default, shared SNAT — risk of exhaustion), <code>natGateway</code> (recommended), <code>userDefinedRouting</code> (you provide a route table — for hub-spoke with central NVA), <code>userAssignedNATGateway</code>, <code>none</code> (private + cluster does no internet — for fully airgapped).</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · NetworkPolicy + Web App Routing",
            h2="NetworkPolicy + Web App Routing add-on",
            body_html="""    <p><strong>NetworkPolicy</strong> options (you pick at cluster create; can\'t change in place):</p>
    <ul>
      <li><strong>Azure NetworkPolicy</strong> — Azure-native implementation. Standard NetworkPolicy semantics. Works with Azure CNI + Overlay.</li>
      <li><strong>Calico</strong> — third-party, proven, supports advanced features (egress policy, GlobalNetworkPolicy via Calico CRDs). Free tier.</li>
      <li><strong>Cilium</strong> — eBPF-based; standard NetworkPolicy + Cilium NetworkPolicy CRD (DNS-based, L7 awareness). Default with AKS Automatic + Azure CNI Powered by Cilium.</li>
    </ul>
    <p><strong>Web Application Routing add-on:</strong> turns on a managed NGINX ingress controller + cert-manager + Azure DNS integration. Replaces the older HTTP Application Routing add-on (deprecated). For teams that want self-hosted ingress without operating Helm charts.</p>
    <p><strong>Other plumbing:</strong> dual-stack (IPv4+IPv6) supported with Azure CNI Overlay. Windows networking has its own constraints (no eBPF, NetworkPolicy via Azure or Calico). Private DNS hub-spoke is the typical enterprise topology — central Private DNS zones + cross-VNet links.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A new AKS cluster is bursting external API calls; you see <code>SNAT port allocation</code> failures in Pod logs. What\'s the fix?",
            options=[
                ("Increase the cluster\'s public LB SKU.", False),
                ("Switch outbound type to <strong>NAT Gateway</strong> — provides 64K SNAT ports per attached IP and scales far beyond LB-shared.", True),
                ("Add more nodes.", False),
            ],
            feedback="LB-shared SNAT is the limit. NAT Gateway gives you orders of magnitude more SNAT ports per IP and isolates per-cluster egress. Add it before this becomes a recurring outage.",
        ),
    },
    before_after_before='<p>Pre-Overlay AKS clusters used <strong>traditional Azure CNI</strong>: every Pod consumed a real VNet IP. A 100-node cluster with 30 Pods/node burned 3,000 IPs from your subnet. Plus pre-AGC, ingress meant <strong>AGIC</strong> (programmed Application Gateway v1) — slow reconciles, complex backend pools, awkward overlay handling. Plus default outbound was <strong>LB-shared SNAT</strong> — burst traffic from one service exhausted the pool and broke <em>everything</em>.</p>',
    before_after_after='<p>Modern AKS uses <strong>Azure CNI Overlay</strong> (default) — Pod IPs come from an overlay CIDR; node IPs stay in VNet; one /24 VNet supports a 10K-node cluster. Ingress uses <strong>Application Gateway for Containers</strong> (AGC) configured via <strong>Gateway API</strong> — purpose-built L7, fast reconciles, native overlay support. Egress uses <strong>NAT Gateway</strong> — 64K SNAT ports per IP, no shared exhaustion. <em>The networking stack finally stops being the bottleneck.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Kubenet is deprecated; AGIC is fading; LB-shared SNAT is dangerous. Use Overlay + AGC + NAT Gateway as the modern default.</em></p>',
    analogy_intro_html='''<p>The <strong>Pathways &amp; Quad</strong> are how everything moves around K-Campus. Faculty offices need addresses (IPs); students walk between buildings (Pod-to-Pod traffic); visitors arrive from off-campus and need directions to the right building (ingress); deliveries leave campus to the post office (egress).</p>
    <p>The <strong>address scheme</strong> on campus has options. Traditional: every dorm room has a unique street address from the city block (Azure CNI — every Pod = real VNet IP). Modern: each building has its own internal numbering, the city sees only the building (Azure CNI Overlay — default). High-performance: same as modern, but the building is staffed by Cilium runners who deliver mail with a stopwatch (CNI Powered by Cilium).</p>
    <p>The <strong>front gates</strong> (ingress) — visitors used to be greeted by a slow gatekeeper named AGIC who had to look up a paper map every time. The modern campus has a Concierge Desk (AGC) with the visitor manifest preloaded; visitors get walking directions instantly via Gateway API.</p>
    <p>The <strong>delivery dock</strong> (egress) — for years, all outgoing mail piled into one shared shipping room (LB-shared SNAT) and during finals week the room ran out of shipping labels (SNAT exhaustion). Modern campus added a dedicated post office (NAT Gateway) — virtually unlimited capacity, and one busy professor can\'t starve another.</p>''',
    translation_rows=[
        ("Campus address scheme", "CNI (Azure CNI / Overlay / Cilium / BYO)"),
        ("Modern building-internal numbering", "Azure CNI Overlay — Pods on overlay CIDR"),
        ("Cilium runners with stopwatches", "Azure CNI Powered by Cilium (eBPF dataplane)"),
        ("Slow paper-map gatekeeper", "AGIC — Application Gateway Ingress Controller (legacy)"),
        ("Concierge Desk with preloaded manifest", "AGC + Gateway API"),
        ("In-house mailroom (NGINX inside building)", "Web Application Routing add-on"),
        ("Shared shipping room", "LB-shared SNAT (default outbound)"),
        ("Dedicated post office", "NAT Gateway"),
        ("Locked-gate campus", "Private cluster via Private Link"),
        ("Apiserver in your own building basement", "API Server VNet Integration"),
        ("\"Only these visitor IDs allowed\" list", "Authorized IP ranges"),
        ("Inter-office delivery rules", "NetworkPolicy (Azure / Calico / Cilium)"),
    ],
    analogy_stops="A campus has fixed buildings; a cluster\'s topology is software-defined and reconfigurable. The metaphor doesn\'t capture overlay encapsulation overhead or BGP route propagation across peered VNets.",
    eli5="Every worker on campus needs a desk address. There are different ways to give out addresses — some use real city addresses, some use building-internal numbers. Visitors come in through a front gate and a friendly desk tells them where to go. Deliveries leave through a back gate that has to be big enough that everyone\'s mail fits at once.",
    eli10="AKS networking has three surfaces. <strong>CNI</strong>: Azure CNI Overlay (default) decouples Pod IPs from VNet — solves IP exhaustion. CNI Powered by Cilium adds eBPF dataplane + DNS-aware NetworkPolicy. Kubenet is deprecated. <strong>Ingress</strong>: AGC + Gateway API for new (purpose-built L7); AGIC is legacy. Standard LB for L4; NAT Gateway for egress to avoid shared SNAT exhaustion. <strong>Control</strong>: API VNet Integration injects the apiserver into your VNet (modern); private cluster via Private Link; or authorized IP ranges. NetworkPolicy via Azure / Calico / Cilium — pick at create time.",
    scenarios=[
        Scenario(
            name="Bank — private cluster + API VNet Integration + AGC private mode",
            body="A bank requires no public endpoints. They create the AKS cluster with <strong>API Server VNet Integration</strong> (apiserver IP inside their hub VNet) + Azure CNI Overlay + AGC in private mode (private IP, attached to a private DNS zone). All ingress hits AGC privately; control plane never appears on the public internet. <em>Pen-test report: zero public-IP attack surface.</em>",
        ),
        Scenario(
            name="SaaS — burst traffic broke SNAT, fixed with NAT Gateway",
            body="A SaaS hit a sudden viral moment — 10× outbound API calls. Within minutes Pods started failing with <code>SNAT port allocation</code> errors. Root cause: default LB-shared SNAT. Emergency fix: <code>az aks update --outbound-type managedNATGateway</code> with two static IPs. New SNAT capacity = ~128K ports. <em>Outage resolved in 20 minutes; runbook now mandates NAT Gateway from cluster creation.</em>",
        ),
        Scenario(
            name="Migration — AGIC → AGC across two sprints",
            body="An older cluster runs 40 Ingresses on AGIC + Application Gateway v1. Migration plan: spin up AGC alongside, port Ingresses to <code>HTTPRoute</code> (Gateway API), test in parallel, swap DNS, keep AGIC as fallback for 30 days. Sprint 1 = porting + parallel testing; Sprint 2 = cutover + decommission. <em>No downtime; AGC reconcile times improved 30s → 2s.</em>",
        ),
        Scenario(
            name="Microservices — Cilium NetworkPolicy + L7 awareness",
            body="A 200-service cluster needs strict zero-trust policies. They enable AKS Automatic (Cilium dataplane). Use standard NetworkPolicy for Pod-to-Pod allow lists; use <strong>Cilium NetworkPolicy CRD</strong> for L7 rules (\"frontend can call /api/v1/users on backend, nothing else\"). Cilium\'s Hubble UI shows live flow graphs. <em>Network team and dev team share one mental model.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Kubenet is fine for small clusters.\"",
            truth="Kubenet is deprecated; new AKS clusters cannot use it. Even existing clusters should migrate (Azure has migration tools). The maintained options are Azure CNI, Azure CNI Overlay, Azure CNI Powered by Cilium, and BYO CNI.",
        ),
        Misconception(
            myth="\"AGIC and AGC are the same thing.\"",
            truth="<strong>AGIC</strong> = legacy AKS controller programming Application Gateway v1 via Ingress objects. <strong>AGC</strong> = purpose-built L7 LB programmed via Gateway API (HTTPRoute, TCPRoute). Different Azure SKU, different controller, different K8s API. AGC is the modern path; AGIC is end-of-life-bound.",
        ),
        Misconception(
            myth="\"My cluster doesn\'t need a NAT Gateway because it\'s small.\"",
            truth="Default LB-shared SNAT gives a cluster ~64 ports per node by default — and bursty workloads can exhaust them. Even a 5-node cluster can SNAT-exhaust if a single Pod opens hundreds of outbound connections. NAT Gateway is the safe-by-default choice from cluster creation; the cost of one NAT Gateway is small relative to the cost of an outage.",
        ),
    ],
    flashcards=[
        Flashcard(front="Five AKS CNI options? Default?", back="<strong>Azure CNI</strong> (real VNet IP per Pod), <strong>Azure CNI Overlay</strong> (default — Pod IPs on overlay), <strong>Azure CNI Powered by Cilium</strong> (eBPF dataplane), <strong>BYO CNI</strong>, <strong>Kubenet</strong> (deprecated)."),
        Flashcard(front="Difference between AGIC and AGC?", back="<strong>AGIC</strong> = AKS controller programming Application Gateway v1 from Ingress objects (legacy). <strong>AGC</strong> = Application Gateway for Containers, purpose-built L7 LB programmed via Gateway API (HTTPRoute). AGC is the modern path."),
        Flashcard(front="Why use NAT Gateway over default outbound?", back="Default = LB-shared SNAT, ~64 ports/node, prone to <code>SNAT port allocation</code> exhaustion under burst. NAT Gateway = up to 64K ports per attached IP, scales far beyond, isolates cluster egress. Set <code>--outbound-type managedNATGateway</code>."),
        Flashcard(front="Three ways to lock down the AKS apiserver?", back="<strong>Authorized IP ranges</strong> (firewall the public endpoint), <strong>private cluster</strong> (Private Link + Private DNS), <strong>API Server VNet Integration</strong> (apiserver injected into a delegated subnet of your VNet — modern recommended)."),
        Flashcard(front="NetworkPolicy options?", back="<strong>Azure NetworkPolicy</strong> (Azure-native), <strong>Calico</strong> (third-party, advanced features), <strong>Cilium</strong> (eBPF, L7-aware). Pick at cluster create — cannot change in place."),
        Flashcard(front="What does Azure CNI Overlay solve?", back="The IP-exhaustion problem. Pods get IPs from an overlay CIDR (not consumed from the VNet); node IPs stay in VNet. A /24 VNet supports a 10K-node cluster."),
        Flashcard(front="What\'s the Web Application Routing add-on?", back="Managed NGINX ingress controller + cert-manager + Azure DNS integration. Replaces deprecated HTTP Application Routing add-on. Useful for self-hosted ingress without operating Helm charts."),
        Flashcard(front="Pod subnet vs node subnet?", back="With Azure CNI you can put Pods in a separate subnet from nodes for finer-grained NSG / route-table control. With Overlay this isn\'t needed (Pod IPs come from overlay CIDR)."),
    ],
    quizzes=[
        Quiz(
            prompt="A new cluster has 50 nodes, each with 30 Pods. The VNet subnet is /24 (256 IPs). The cluster won\'t schedule new Pods — \"no available IP\". What CNI is being used and what\'s the fix?",
            answer="<strong>Traditional Azure CNI</strong> — Pods consume real VNet IPs (50 × 30 = 1500 needed; subnet has 256, exhausted). Fix: migrate to <strong>Azure CNI Overlay</strong>. Pods will get IPs from a separate overlay CIDR; node IPs stay in the /24. Migration is in-place via <code>az aks update --network-plugin azure --network-plugin-mode overlay --pod-cidr 10.244.0.0/16</code> (verify subnet is empty of Pods first; review the migration doc).",
        ),
        Quiz(
            prompt="The team wants Pod-to-Pod traffic to be denied by default, with explicit allow rules per service. The cluster is running Azure CNI Overlay. Walk through how to enable that.",
            answer="Step 1: confirm a NetworkPolicy plugin is enabled at cluster create (Azure / Calico / Cilium — can\'t change in place; if absent, this means a new cluster with the plugin). Step 2: deploy a default-deny <code>NetworkPolicy</code> per namespace: <code>podSelector: {}, policyTypes: [Ingress, Egress]</code> with empty allow lists. Step 3: per service, add NetworkPolicies with explicit ingress allow lists from labelled clients. Step 4: monitor Cilium Hubble (or Azure Network Observability) for blocked traffic — surfaces broken expectations.",
        ),
        Quiz(
            prompt="During a Black Friday flash sale a SaaS goes down at 10:23 PM. Pod logs show <code>SNAT port allocation</code> errors. The on-call hits <code>az aks update --outbound-type managedNATGateway</code>. What happens next?",
            answer="The command fails with: <em>\"Cannot change outbound type from \'loadBalancer\' to \'managedNATGateway\' on an existing cluster — outbound type is immutable after creation.\"</em> The on-call now has to (a) provision a NAT Gateway in the node pool subnet manually, or (b) use User-Defined Routing to route 0.0.0.0/0 through the NAT Gateway (then update outbound type to <code>userDefinedRouting</code>, which <em>is</em> changeable). Lesson: make NAT Gateway part of cluster creation — never the emergency fix.",
            cyoa=True,
            cyoa_tag="what happened on the call",
        ),
    ],
    glossary=[
        GlossaryItem(name="Azure CNI Overlay", definition="Default AKS CNI mode. Pod IPs come from an overlay CIDR; node IPs stay in the VNet. Solves IP exhaustion."),
        GlossaryItem(name="Azure CNI Powered by Cilium", definition="Azure CNI for IPAM + Cilium for the dataplane. eBPF, no kube-proxy needed, L7-aware NetworkPolicy. Default with AKS Automatic."),
        GlossaryItem(name="Kubenet", definition="Legacy AKS networking mode (NAT-on-node). Deprecated 2024; cannot be used on new clusters."),
        GlossaryItem(name="AGIC", definition="Application Gateway Ingress Controller — legacy AKS controller programming App Gateway v1 via Ingress."),
        GlossaryItem(name="AGC", definition="Application Gateway for Containers — modern purpose-built L7 LB for K8s, configured via Gateway API."),
        GlossaryItem(name="Gateway API", definition="K8s-blessed successor to Ingress. Resources: Gateway, GatewayClass, HTTPRoute, TCPRoute. AGC is configured via these."),
        GlossaryItem(name="NAT Gateway", definition="Azure egress resource. Up to 64K SNAT ports per attached IP. Replaces LB-shared SNAT for egress; avoids exhaustion."),
        GlossaryItem(name="API Server VNet Integration", definition="Modern AKS feature — apiserver IP is injected into a delegated subnet of your VNet. No Private Link, no peering hub-spoke."),
        GlossaryItem(name="Private cluster", definition="AKS where apiserver is exposed only via Private Link with a Private DNS zone. No public endpoint."),
        GlossaryItem(name="Authorized IP ranges", definition="Firewall on the public apiserver endpoint — allow only specified CIDRs."),
        GlossaryItem(name="SNAT exhaustion", definition="Outage class where shared SNAT ports run out under burst egress; new connections fail. Fixed by NAT Gateway."),
        GlossaryItem(name="Web Application Routing add-on", definition="Managed NGINX ingress + cert-manager + Azure DNS. Replaces deprecated HTTP Application Routing add-on."),
    ],
    recap_lead="Three networking surfaces understood: CNI (Overlay default, Cilium for performance), ingress (AGC + Gateway API for new), control (API VNet Integration + private endpoints). NAT Gateway is the egress safety net.",
    recap_next='<strong>Next — A4: AKS Storage.</strong> Azure Disks CSI (Premium SSD v2, Ultra, VolumeAttributesClass), Azure Files CSI (RWX SMB/NFS), Blob CSI (BlobFuse2), Azure NetApp Files, Azure Container Storage, Secrets Store CSI with Key Vault, snapshots, ZRS, topology-aware scheduling.',
)
