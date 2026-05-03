"""K-GKE G3 — GKE Networking (VPC-native, Dataplane V2, Gateway, NEG, MCI, Cloud Service Mesh)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GKE networking — VPC-native, Dataplane V2, Gateway, NEG, multi-cluster, Cloud Service Mesh.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Pathways &amp; Trellises — six networking surfaces</text>
  <rect x="40" y="70" width="160" height="120" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="120" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">VPC-native (alias IP)</text>
  <text x="120" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Pod range secondary</text>
  <text x="120" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Svc range secondary</text>
  <text x="120" y="135" text-anchor="middle" font-size="9" fill="#FFFFFF">IP planning matters</text>
  <text x="120" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">routes-based legacy</text>
  <rect x="220" y="70" width="160" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="300" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Dataplane V2</text>
  <text x="300" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Cilium-based eBPF</text>
  <text x="300" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">default for new</text>
  <text x="300" y="135" text-anchor="middle" font-size="9" fill="#FFFFFF">NetworkPolicy + obs</text>
  <text x="300" y="155" text-anchor="middle" font-size="9" fill="#FFFFFF">no kube-proxy</text>
  <rect x="400" y="70" width="160" height="120" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="480" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Gateway controller</text>
  <text x="480" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">Gateway API native</text>
  <text x="480" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">multi-cluster Gateway</text>
  <text x="480" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">NEG (container-native)</text>
  <text x="480" y="155" text-anchor="middle" font-size="9" fill="#FBF1D6">Ingress (Cloud LB) legacy</text>
  <rect x="580" y="70" width="140" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="650" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">multi-cluster + mesh</text>
  <text x="650" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">MCI / MCS</text>
  <text x="650" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">Cloud Service Mesh</text>
  <text x="650" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">Shared VPC</text>
  <text x="650" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">NCC + private DNS</text>
  <text x="650" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">Cloud NAT + firewall</text>
</svg>"""


LESSON = LessonSpec(
    num="03",
    title_short="GKE networking",
    title_full="G3 · GKE Networking (VPC-native, Dataplane V2, Gateway, multi-cluster, CSM)",
    title_html="K-GKE G3 · GKE Networking",
    module_eyebrow="Module G3 · the Pathways &amp; Trellises",
    hero_sub_html='<strong>VPC-native (alias IP)</strong> with pod/service secondary ranges (routes-based is legacy). <strong>GKE Dataplane V2</strong> = Cilium-based eBPF, default for new clusters. <strong>GKE Ingress</strong> (Cloud LB programmed by Ingress objects, legacy path) and the modern <strong>GKE Gateway controller</strong> (first-class Gateway API + multi-cluster Gateway). <strong>NEG</strong> + container-native LB. <strong>Multi Cluster Ingress / Multi Cluster Services (MCI/MCS)</strong>. <strong>Cloud Service Mesh</strong> (managed Istio). Plus Network Connectivity Center, Shared VPC, firewall rules, DNS.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"NEG health checks failing for ingress backend; 503s to all customers.\"</em> You realise the firewall rule blocking GFE health-check IP ranges (<code>35.191.0.0/16</code>, <code>130.211.0.0/22</code>) was overwritten by a Terraform refactor yesterday. NEG can\'t mark Pod IPs healthy; load balancer drains backends. <em>Half your traffic now goes nowhere.</em> Today\'s lesson: GKE networking surfaces and how to reason about each one.",
    stamp_html="<strong>VPC-native + Dataplane V2 + Gateway API + NEG container-native LB is the modern default. Plan IP space (Pod + Service secondary ranges) generously; firewall the GFE health-check ranges open; use Cloud NAT for egress; Cloud Service Mesh for mTLS + traffic management.</strong>",
    district_pin="kg-plot03",
    district_label="Pathways &amp; Trellises",
    sections=[
        Section(
            eyebrow="Section 1.1 · VPC-native + IP planning",
            h2="VPC-native (alias IP) + IP planning",
            body_html="""    <p><strong>VPC-native</strong> clusters give every Pod and Service a real VPC IP via <em>alias IP ranges</em> on the node. Pods communicate directly via VPC routing — no NAT, no overlay encap. <em>The default for new GKE clusters; routes-based legacy is deprecated.</em></p>
    <p>VPC-native clusters need three IP ranges:</p>
    <ul>
      <li><strong>Node range (primary subnet)</strong> — IPs for nodes themselves. Plan: max-nodes you\'ll ever scale to.</li>
      <li><strong>Pod secondary range</strong> — IPs allocated to Pods. Per-node alias range carved from this. Plan: <code>(max-nodes × default-max-pods-per-node × 2 buffer)</code>. <em>Default 110 Pods per node × 1024 nodes = ~225K IPs needed</em>; underspecify and you stop scheduling Pods even with empty CPU.</li>
      <li><strong>Service secondary range</strong> — IPs for ClusterIP Services. Smaller; default sufficient for most clusters.</li>
    </ul>
    <p><strong>IP exhaustion mitigation:</strong> use larger Pod secondary ranges from the start (you can\'t resize a Pod range in place — need new node pool with different range). Tune <code>--max-pods-per-node</code> (default 110; can be lowered to reduce per-node alias usage). Use Discontiguous Multi-Pod CIDR for very large clusters. <em>Plan IP space at cluster creation; this bites later otherwise.</em></p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Dataplane V2 + NetworkPolicy + Cloud NAT",
            h2="Dataplane V2 + NetworkPolicy + Cloud NAT",
            body_html="""    <p><strong>GKE Dataplane V2</strong> = Cilium-based eBPF dataplane. Default for new clusters. Replaces kube-proxy (iptables / IPVS). Faster service routing, better observability (Hubble flow visibility), L4 + L7 NetworkPolicy.</p>
    <p><strong>NetworkPolicy</strong>: standard K8s NetworkPolicy works on Dataplane V2. Plus <em>FQDN NetworkPolicy</em> (block egress to specific DNS names — useful for data-exfiltration prevention). Plus Cilium NetworkPolicy CRD for L7 rules (\"allow GET /api on this service, deny POST\"). <em>Default-deny per namespace + explicit allow lists</em> is the standard zero-trust posture.</p>
    <p><strong>Cloud NAT</strong> for egress: Pods on private clusters have no public IPs. Outbound to internet (Stripe, package registries, third-party APIs) goes through Cloud NAT — managed NAT, scales NAT ports per attached IP. Avoids the SNAT-exhaustion class of outage that LB-shared SNAT causes on other clouds.</p>
    <p><strong>Master authorized networks</strong> + <strong>private cluster</strong> from G1 apply at the network layer — control-plane access restricted to specific CIDRs, nodes private with Cloud NAT for egress.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Ingress, Gateway, NEG, container-native LB",
            h2="Ingress, Gateway, NEG, container-native load balancing",
            body_html="""    <p><strong>GKE Ingress</strong> (legacy path) — controller programs a Google Cloud Load Balancer (HTTP(S) LB) from <code>Ingress</code> objects. Backend = NEG (Network Endpoint Group) of Pod IPs (container-native LB). Annotations on the Ingress configure the LB (TLS cert, backend config, Cloud Armor policy, IAP).</p>
    <p><strong>GKE Gateway controller</strong> (modern) — first-class <strong>Gateway API</strong> support. Resources: <code>GatewayClass</code> (e.g. <code>gke-l7-global-external-managed</code>), <code>Gateway</code>, <code>HTTPRoute</code>, <code>TLSRoute</code>, <code>TCPRoute</code>. Cleaner separation of platform-team (Gateway) and app-team (HTTPRoute) responsibilities. Supports <em>multi-cluster Gateway</em> across clusters in a fleet.</p>
    <p><strong>NEG (Network Endpoint Group)</strong> = the GCP LB primitive that holds Pod IPs (container-native LB) instead of node IPs (instance-group LB). Faster failure detection (LB sees Pod IP go away immediately instead of via kube-proxy NAT chain), lower latency. <em>Required for Ingress / Gateway in modern GKE.</em></p>
    <p><strong>Multi Cluster Ingress (MCI) + Multi Cluster Services (MCS)</strong> = single Ingress / Service that fronts Pods across multiple GKE clusters in a fleet (different regions). MCI gives you a global anycast IP with traffic routed to the nearest healthy cluster. MCS lets a Service in cluster A address Pods in cluster B. <em>Foundation for multi-region active-active.</em></p>"""
        ),
        Section(
            eyebrow="Section 1.4 · Cloud Service Mesh, Shared VPC, NCC, firewall, DNS",
            h2="Cloud Service Mesh, Shared VPC, NCC, firewall + DNS",
            body_html="""    <p><strong>Cloud Service Mesh (CSM)</strong> = managed Istio for GKE. Sidecars on Pods for mTLS / traffic management / observability; Google operates the control plane. Works fleet-wide via GKE Enterprise — <em>cross-cluster mTLS without DIY mesh-of-meshes</em>.</p>
    <p><strong>Shared VPC</strong> — host project owns the VPC + subnets; service projects (multiple GKE clusters across teams) attach. Centralised network ops; team-level cluster autonomy. Common enterprise pattern.</p>
    <p><strong>Network Connectivity Center (NCC)</strong> = hub-spoke connectivity orchestrator: cross-region VPC peering, on-prem hybrid (Cloud Interconnect / Cloud VPN spokes), inter-cloud connectivity. For multi-cluster + hybrid topologies.</p>
    <p><strong>Firewall rules</strong> — <em>critical:</em> firewall must allow GFE health-check IP ranges (<code>35.191.0.0/16</code>, <code>130.211.0.0/22</code>) to reach NEG-backed Pods, or LBs report all backends unhealthy. Plus standard Pod-to-Pod permits (Cilium NetworkPolicy is layered on top).</p>
    <p><strong>DNS troubleshooting</strong>: <strong>Cloud DNS for GKE</strong> (managed kube-dns alternative, scales better; use <code>--cluster-dns=clouddns</code>). NodeLocal DNSCache to reduce DNS latency + load on cluster DNS. CoreDNS in default mode for compatibility. <em>DNS issues are the #2 cause of intermittent failures after IP exhaustion.</em></p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A new GKE cluster has 200 nodes and Pods are stuck Pending with \"InsufficientPodCapacity.\" Where do you look first?",
            options=[
                ("Add more CPU.", False),
                ("Inspect the Pod secondary range size — was it sized for 200 × 110 Pods × 2 buffer at create time?", True),
                ("Re-roll the cluster.", False),
            ],
            feedback="VPC-native Pod IPs come from the Pod secondary range. Underspecify it and you exhaust IPs before exhausting CPU; the only fix is a new node pool with a larger Pod range — can\'t resize the existing range in place.",
        ),
    },
    before_after_before='<p>Pre-Dataplane-V2 GKE used kube-proxy (iptables/IPVS) for service routing. Pre-Gateway-controller, ingress meant the legacy Ingress object + Cloud LB. Multi-cluster anything = bring-your-own. Network Policy was bring-your-own (Calico). Mesh was bring-your-own (self-installed Istio). Routes-based clusters were the default — slow VPC-route lookups capped at low scale. IP planning was an afterthought.</p>',
    before_after_after='<p>Modern GKE ships <strong>VPC-native + Dataplane V2 + Gateway API + NEG container-native LB</strong> as defaults. Multi Cluster Ingress + Multi Cluster Services let one Service span clusters. <strong>Cloud Service Mesh</strong> is managed Istio. <strong>Cloud DNS for GKE</strong> + NodeLocal DNSCache solve scale-related DNS issues. <em>Operations + workloads share a coherent network model.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Plan IP space generously at creation; everything else is reasonable defaults.</em></p>',
    analogy_intro_html='''<p>The <strong>Pathways &amp; Trellises</strong> are the hidden infrastructure of the K-Garden — paths visitors walk, irrigation pipes that connect plots, trellises that direct climbing plants where to grow. Six surfaces.</p>
    <p>The <strong>address scheme</strong>: every plant has a real garden address (VPC-native alias IP), not just a tag. The garden has three address books: one for the plot beds (Node range), one for the plants (Pod secondary range), and one for the watering taps (Service secondary range). <em>Underspecify the plant address book and you can\'t plant new flowers even in empty beds.</em></p>
    <p>The <strong>path engineer</strong> is the <em>Cilium runner</em> (Dataplane V2) who delivers messages between plants via eBPF lanes — much faster than the old hand-delivered (kube-proxy) routes. The Cilium runner also enforces \"who can talk to whom\" rules (NetworkPolicy).</p>
    <p>The <strong>front gates</strong> — visitors used to enter through the slow gatekeeper (legacy Ingress controller programming Cloud LB). The modern garden has a Concierge (Gateway controller) who works the same Cloud LB but speaks Gateway API natively and can run a single concierge desk across multiple gardens at once (multi-cluster Gateway).</p>
    <p>The <strong>plant directory</strong> (NEG) lists each plant\'s exact address; the front-gate Concierge sends visitors directly to the plant, not via a generic plot lookup.</p>
    <p>The <strong>delivery dock</strong> (Cloud NAT) handles all packages leaving the garden — managed by Google, scales to plenty.</p>
    <p>And the <strong>plant-to-plant courier service</strong> (Cloud Service Mesh) is a managed Istio offering: every plant gets a personal courier (sidecar) for mTLS-encrypted notes between plants — and you can extend the courier service across multiple gardens worldwide.</p>''',
    translation_rows=[
        ("Garden address scheme", "VPC-native (alias IP)"),
        ("Plot bed address book", "Node range (primary subnet)"),
        ("Plant address book", "Pod secondary range (alias IP per node)"),
        ("Watering-tap address book", "Service secondary range (ClusterIP)"),
        ("Cilium runner with eBPF lanes", "Dataplane V2"),
        ("\"Who can talk to whom\" rules", "NetworkPolicy (incl. FQDN, L7 via Cilium)"),
        ("Slow gatekeeper", "GKE Ingress (legacy controller path)"),
        ("Modern Concierge", "GKE Gateway controller (Gateway API)"),
        ("Concierge across gardens", "Multi-cluster Gateway / MCI"),
        ("Plant directory", "NEG (Network Endpoint Group, container-native LB)"),
        ("Delivery dock", "Cloud NAT (egress for private clusters)"),
        ("Plant-to-plant courier", "Cloud Service Mesh (managed Istio)"),
        ("Shared garden plumbing", "Shared VPC (host + service projects)"),
        ("Inter-garden tunnel network", "Network Connectivity Center"),
        ("Health inspector visit lane", "Firewall rule allowing 35.191.0.0/16 + 130.211.0.0/22 (GFE health checks)"),
    ],
    analogy_stops="A garden\'s path layout is fixed; GKE\'s VPC-native is software-defined and reshapes per node-pool config — but Pod CIDRs cannot be resized in place, so the metaphor under-states this constraint.",
    eli5="Plants in the garden have real addresses (not nicknames) so they can talk to each other directly. A fast runner delivers messages and enforces the rules of who-can-talk-to-whom. The front gate has a modern Concierge who handles visitors. Letters out of the garden go through a delivery dock. And there\'s a courier service for private notes between plants.",
    eli10="GKE networking = VPC-native (alias IP, real Pod IPs) with three IP ranges (node + Pod secondary + Service secondary — plan generously). Dataplane V2 (Cilium-based eBPF, default) replaces kube-proxy + adds NetworkPolicy + L7 + Hubble. GKE Gateway controller (Gateway API) is the modern ingress; legacy Ingress works but Gateway is preferred. NEG = container-native LB (Pod IPs in the LB backend, not node IPs). MCI/MCS for multi-cluster. Cloud Service Mesh = managed Istio. Cloud NAT for egress. Firewall must allow GFE health-check ranges 35.191.0.0/16 + 130.211.0.0/22.",
    scenarios=[
        Scenario(
            name="SaaS — multi-region active-active via Multi Cluster Ingress",
            body="A SaaS runs three regional GKE clusters (us, eu, asia). Single Multi Cluster Ingress provides one global anycast IP; traffic routed to the nearest healthy cluster. Failover automatic if a region degrades. <em>One DNS name, one cert, three clusters.</em>",
        ),
        Scenario(
            name="Bank — Shared VPC + Cloud Service Mesh fleet-wide mTLS",
            body="A bank\'s host project owns the VPC; six service projects each run team-owned GKE clusters. Cloud Service Mesh (managed Istio) registered in the fleet provides mTLS between Pods across clusters + projects. Network team owns the VPC + firewall; team clusters consume it. <em>Centralised compliance, distributed app teams.</em>",
        ),
        Scenario(
            name="IP exhaustion outage — Pod range too small",
            body="A cluster created with default Pod secondary range (/14 ≈ 256K IPs sounded plenty). Six months later, autoscaling hits 800 nodes × 110 Pods × per-node alias overhead = exhausted. New Pods stuck Pending with no IPs. Fix: create new node pool with much larger Pod range; drain old workloads; delete old pool. <em>Cannot resize in place.</em>",
        ),
        Scenario(
            name="NEG health-check 503s root-caused by missing firewall rule",
            body="An ingress backend started returning 503s. NEG marked all Pod IPs unhealthy. Root cause: Terraform refactor removed the firewall rule allowing <code>35.191.0.0/16</code> + <code>130.211.0.0/22</code> (GFE health-check IPs) into the Pod range. Restored rule; NEG marked Pods healthy in 30 seconds. <em>Postmortem: pin the GFE-allow rule with a documented Terraform comment so future refactors don\'t remove it.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Routes-based clusters still work fine.\"",
            truth="Routes-based GKE clusters are <em>legacy</em> and deprecated. They use VPC routes for Pod traffic, hitting per-VPC route quota at low scale (a few hundred routes total). All new clusters should be VPC-native (alias IP); existing routes-based clusters need migration via blue-green to a new VPC-native cluster.",
        ),
        Misconception(
            myth="\"NEG and Instance Group LB backends are interchangeable.\"",
            truth="<strong>NEG (container-native LB)</strong> = LB sends traffic directly to Pod IPs (via VPC-native alias IPs). Faster failure detection, lower latency, kube-proxy not in the data path. <strong>Instance Group LB</strong> = LB sends traffic to node external IPs; kube-proxy NATs to Pods. Slower failure detection, kube-proxy hop. <em>NEG is required for modern Ingress / Gateway and for Cloud Service Mesh.</em>",
        ),
        Misconception(
            myth="\"Dataplane V2 only matters for NetworkPolicy.\"",
            truth="Dataplane V2 also: replaces kube-proxy (faster service routing, fewer iptables rules), enables Hubble flow observability, supports FQDN NetworkPolicy and L7 policies via Cilium, accelerates Service ClusterIP performance at scale. NetworkPolicy is one feature; the dataplane upgrade affects everything.",
        ),
    ],
    flashcards=[
        Flashcard(front="What is VPC-native (alias IP)?", back="GKE\'s default networking: Pods + Services get real VPC IPs via alias ranges on nodes. Three IP ranges needed: node primary subnet + Pod secondary range + Service secondary range. Routes-based is legacy."),
        Flashcard(front="Why is IP planning critical at cluster creation?", back="Pod secondary range cannot be resized in place. Underspecifying = stop scheduling Pods even with empty CPU. Plan: <code>(max-nodes × max-pods-per-node × 2 buffer)</code>. Migration off requires new node pool with larger range + drain + delete old."),
        Flashcard(front="What is GKE Dataplane V2?", back="Cilium-based eBPF dataplane. Default for new clusters. Replaces kube-proxy. Faster service routing + L4/L7 NetworkPolicy + FQDN NetworkPolicy + Hubble flow observability. No kube-proxy iptables sprawl."),
        Flashcard(front="GKE Gateway controller vs legacy Ingress?", back="<strong>Gateway controller</strong>: first-class Gateway API (HTTPRoute, TCPRoute, TLSRoute, GatewayClass), supports multi-cluster Gateway. <strong>Legacy Ingress</strong>: Ingress objects programming Cloud LB; still supported but Gateway is the modern path."),
        Flashcard(front="What is a NEG?", back="<strong>Network Endpoint Group</strong> = container-native LB primitive that holds Pod IPs (not node IPs). Required for modern Ingress / Gateway / Cloud Service Mesh. Faster failure detection, kube-proxy not in data path."),
        Flashcard(front="Multi Cluster Ingress (MCI) — what does it solve?", back="One global anycast IP serving Pods across multiple GKE clusters in a fleet (different regions). Traffic routed to nearest healthy cluster. Failover automatic. Foundation for multi-region active-active without per-region DNS gymnastics."),
        Flashcard(front="What two firewall ranges must be allowed for NEG health checks?", back="<code>35.191.0.0/16</code> and <code>130.211.0.0/22</code> — GFE health-check source ranges. Without these, LB marks all NEG-backed Pods unhealthy. Pin this firewall rule with a comment so refactors don\'t remove it."),
        Flashcard(front="What is Cloud Service Mesh?", back="Managed Istio for GKE. Google operates the control plane; sidecars on Pods give mTLS / traffic management / observability. Works fleet-wide via GKE Enterprise — cross-cluster mTLS without DIY mesh-of-meshes."),
    ],
    quizzes=[
        Quiz(
            prompt="200 Pods stuck Pending, scheduler logs say \"insufficient cpu/memory\" but <code>kubectl top nodes</code> shows nodes mostly idle. The cluster has been growing for months. What\'s the likely cause and the fix?",
            answer="<strong>Pod secondary IP range exhaustion.</strong> VPC-native clusters allocate per-node alias IP ranges out of the cluster\'s Pod secondary range. As nodes grow, the per-node alias bites further into the secondary; eventually the secondary is exhausted and new Pods can\'t get IPs even on nodes with free CPU. Fix: cannot resize in place — create a new node pool with a larger Pod CIDR range; cordon + drain old node pool with PDB safety; delete old pool. Future: plan Pod range generously at cluster creation; use Discontiguous Multi-Pod CIDR for very large clusters.",
        ),
        Quiz(
            prompt="The team has Cloud Armor + Identity-Aware Proxy + Backend Service config to apply to an Ingress. Should they keep using the legacy Ingress object or migrate to Gateway API? Walk through the trade-offs.",
            answer="<strong>Both work; Gateway is the modern preferred path.</strong> Legacy Ingress: simpler if you have a single LB per cluster + per-app annotations + features fully supported by the Ingress annotation set. Gateway API: cleaner separation of concerns (platform team owns Gateway/GatewayClass; app teams own HTTPRoute), supports multi-cluster Gateway, future GKE feature investment. Migration tactic: parallel-run for a sprint (point a test DNS at the new Gateway-fronted endpoint), validate Cloud Armor + IAP behavior, swap DNS, decommission old Ingress. <em>For new ingresses, start with Gateway API; for stable existing Ingresses without pain, migrate at a calmer time.</em>",
        ),
        Quiz(
            prompt="Black Friday morning. Suddenly every customer-facing endpoint returns 503. Cloud Monitoring shows NEG backends 100% unhealthy. What\'s the first thing you check?",
            answer="<strong>Firewall rule allowing GFE health-check IP ranges</strong> — <code>35.191.0.0/16</code> and <code>130.211.0.0/22</code> must permit ingress to the Pod range over the health-check port. Most common cause of \"all backends unhealthy at once\": a recent Terraform/firewall change removed or modified that rule. Validate via <code>gcloud compute firewall-rules list</code> + check the relevant <em>allow-rules</em>. Fix: restore the rule. Postmortem: add a Cloud Monitoring alert on NEG backend health < 100% for >5 min; pin the GFE-allow rule with a Terraform comment + lifecycle ignore_changes block to prevent accidental drift.",
            cyoa=True,
            cyoa_tag="how on-call diagnosed Black Friday 503s in 4 minutes",
        ),
    ],
    glossary=[
        GlossaryItem(name="VPC-native cluster", definition="GKE default — Pods + Services get real VPC IPs via alias ranges. Routes-based is legacy."),
        GlossaryItem(name="Pod secondary range", definition="Subnet secondary range from which Pod IPs are allocated. Can\'t resize in place; plan generously."),
        GlossaryItem(name="Service secondary range", definition="Subnet secondary range for ClusterIP Services."),
        GlossaryItem(name="GKE Dataplane V2", definition="Cilium-based eBPF dataplane. Default for new GKE clusters. Replaces kube-proxy + adds NetworkPolicy + Hubble + L7."),
        GlossaryItem(name="GKE Gateway controller", definition="Modern ingress: first-class Gateway API support; multi-cluster Gateway; cleaner platform/app separation."),
        GlossaryItem(name="NEG (Network Endpoint Group)", definition="Container-native LB primitive holding Pod IPs. Required for modern Ingress / Gateway / CSM. kube-proxy out of data path."),
        GlossaryItem(name="Multi Cluster Ingress (MCI)", definition="One global anycast IP fronting Pods across multiple GKE clusters in a fleet. Traffic to nearest healthy cluster."),
        GlossaryItem(name="Multi Cluster Services (MCS)", definition="A Service in cluster A can address Pods in cluster B (across fleet). Foundation for cross-cluster service mesh."),
        GlossaryItem(name="Cloud Service Mesh (CSM)", definition="Managed Istio for GKE. Google operates control plane; sidecars provide mTLS, traffic management, observability."),
        GlossaryItem(name="Shared VPC", definition="Host project owns VPC + subnets; service projects (multiple GKE clusters) attach. Centralised network ops; team-level autonomy."),
        GlossaryItem(name="Cloud NAT", definition="Managed NAT for egress. For private clusters: outbound to internet (registries, third-party APIs)."),
        GlossaryItem(name="GFE health-check ranges", definition="<code>35.191.0.0/16</code> + <code>130.211.0.0/22</code>. Firewall must allow these to Pod range, or NEG backends mark unhealthy."),
    ],
    recap_lead='Six surfaces: VPC-native + Dataplane V2 + Gateway/Ingress + NEG + MCI/MCS + CSM. Plan IP space at creation; firewall the GFE ranges; Cloud NAT for egress.',
    recap_next='<strong>Next — G4: GKE Identity and Security.</strong> IAM + RBAC + IAM Conditions; Workload Identity Federation for GKE; Binary Authorization; Security Posture; Container Threat Detection (SCC); Confidential GKE Nodes (AMD SEV / Intel TDX); Shielded GKE Nodes; Secret Manager CSI; Artifact Registry; Policy Controller + Config Sync; GKE Sandbox (gVisor); CMEK.',
)
