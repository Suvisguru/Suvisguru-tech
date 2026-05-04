"""K-ADV-NET N1 — CNI internals + eBPF + BGP at scale."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CNI internals — veth, CNI plugin, eBPF datapath, BGP fabric.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Highway HQ · K-Highway — packet from Pod through CNI to BGP fabric</text>
  <rect x="40" y="70" width="160" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="120" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">veth pair</text>
  <text x="120" y="108" text-anchor="middle" font-size="9" fill="#1F2433">Pod ↔ host netns</text>
  <text x="120" y="124" text-anchor="middle" font-size="9" fill="#1F2433">on-ramp</text>
  <rect x="220" y="70" width="160" height="100" rx="10" fill="#3878B5" stroke="#1F2433"/>
  <text x="300" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">CNI plugin</text>
  <text x="300" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Cilium / Calico / Flannel</text>
  <text x="300" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">routing + policy + IPAM</text>
  <rect x="400" y="70" width="160" height="100" rx="10" fill="#FAC775" stroke="#1F2433"/>
  <text x="480" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">eBPF datapath</text>
  <text x="480" y="108" text-anchor="middle" font-size="9" fill="#1F2433">in-kernel programs</text>
  <text x="480" y="124" text-anchor="middle" font-size="9" fill="#1F2433">no userspace hop</text>
  <rect x="580" y="70" width="140" height="100" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="650" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">BGP fabric</text>
  <text x="650" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">node ↔ ToR ↔ DC</text>
  <text x="650" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">native routing</text>
</svg>"""


LESSON = LessonSpec(
    num="01",
    title_short="CNI + eBPF + BGP",
    title_full="N1 · CNI Internals, eBPF, BGP at Scale",
    title_html="K-ADV-NET N1 · CNI + eBPF + BGP",
    module_eyebrow="Module N1 · Highway HQ — packet from Pod through CNI to BGP fabric",
    hero_sub_html='Three foundational layers of K8s networking. <strong>CNI</strong>: the spec + plugin model that gives a Pod a network. <strong>eBPF</strong>: kernel-attached programs that make modern CNIs (Cilium, Calico) faster + more programmable than iptables-based stacks. <strong>BGP at scale</strong>: native routing of Pod CIDRs to top-of-rack switches, removing the encap-overhead tax for clusters that own their fabric.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Cluster latency P99 jumped 4×. Engineer runs <code>tcpdump</code> on the node — packets are taking the long route via overlay encap that should have been short-circuited. The CNI was misconfigured for native routing but the BGP peer wasn\'t up. <em>The kernel datapath was right, the fabric routing was wrong.</em> Today\'s lesson: how the three layers fit + how to debug when one is misconfigured.",
    stamp_html="<strong>CNI = Pod\'s network. eBPF = in-kernel programmable datapath; replaces iptables for modern CNIs. BGP = native routing across the fabric; eliminates encap tax. Pick CNI by features (NetPol, mesh integration, eBPF maturity) + scale.</strong>",
    district_pin="knet-junction01",
    district_label="Highway HQ",
    sections=[
        Section(
            eyebrow="Section 1.1 · CNI spec + plugin choice",
            h2="What CNI does, who provides it",
            body_html="""    <p><strong>CNI (Container Network Interface)</strong> is a thin spec — a binary that takes a JSON config + a network namespace, attaches an interface, returns the IP. K8s calls CNI per Pod create/delete; CNI plugin handles the network. Plugins fall into families:</p>
    <ul>
      <li><strong>Cilium</strong>: eBPF-native; rich features (NetworkPolicy, ClusterMesh, Service mesh, observability via Hubble, mTLS); modern default for non-cloud-managed clusters.</li>
      <li><strong>Calico</strong>: BGP + iptables/eBPF; NetworkPolicy heritage; widely deployed in regulated workloads.</li>
      <li><strong>Cloud-managed</strong>: AWS VPC CNI (ENI per Pod), Azure CNI, GKE Dataplane V2 (Cilium-based) — tightly cloud-integrated; managed for you.</li>
      <li><strong>Flannel</strong>: simple overlay; lightweight; legacy or learning use.</li>
    </ul>
    <p>Pick by needs: features (NetPol, mesh, observability), scale (per-node Pod density), control (your own fabric vs cloud).</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · eBPF datapath",
            h2="Kernel-attached programs replace iptables",
            body_html="""    <p><strong>eBPF</strong> (extended Berkeley Packet Filter) lets you attach small programs to kernel hooks — at TC ingress/egress, XDP, socket, syscall. CNIs like Cilium attach programs that do load-balancing, NetworkPolicy enforcement, encapsulation, observability — all in-kernel, no userspace round-trip.</p>
    <p>Why this matters at scale: <strong>iptables</strong> rules grow linearly with Service count; cluster with 10K Services has chains so long that connection setup costs ms. <strong>eBPF maps</strong> are O(1) hash lookups + O(N) for some policy paths but with much better constants. Cilium reports up to 5× lower P99 latency vs iptables-based stacks at 10K-Service scale.</p>
    <p>Other eBPF wins: <strong>Hubble</strong> gives per-flow visibility without packet capture; <strong>Tetragon</strong> does runtime security at kernel level; <strong>XDP</strong> for DDoS protection at line rate. The same eBPF infrastructure powers networking + security + observability.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · BGP at scale",
            h2="Native Pod-CIDR routing across the fabric",
            body_html="""    <p>By default, Pod CIDRs are local to the cluster — a node\'s Pods can\'t be reached natively from other nodes. CNIs solve this with <strong>encapsulation</strong> (VXLAN / Geneve) — wrap the Pod packet in a node-to-node tunnel — or <strong>native routing</strong> via BGP.</p>
    <p>With <strong>BGP</strong>, each node peers with the top-of-rack (ToR) switch and advertises its Pod CIDR. The ToR routes Pod-IP packets directly to the right node. <em>No encap tax</em>; line-rate forwarding; latency drops; MTU isn\'t reduced.</p>
    <p>Operationally: BGP requires fabric cooperation. Cloud clusters often can\'t (AWS VPC won\'t accept your BGP peer); they fall back to encap or use VPC-route-injection patterns. Bare-metal + on-prem clusters with their own fabric → BGP shines. <strong>MetalLB</strong>, <strong>Cilium BGP Control Plane</strong>, <strong>Calico BGP</strong> are the implementations.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · IPAM + scale considerations",
            h2="IP address management + density limits",
            body_html="""    <p><strong>IPAM</strong>: who hands out Pod IPs. Three patterns:</p>
    <ul>
      <li><strong>CIDR-per-node</strong>: each node gets a /24 (or larger) from a cluster CIDR; CNI hands out Pod IPs from the node\'s slice. Simple; wastes IPs at low Pod density.</li>
      <li><strong>Cluster-pool dynamic</strong>: CNI requests a sub-CIDR per node on demand; better packing at the cost of CNI-control-plane chatter (Cilium\'s ipam=cluster-pool).</li>
      <li><strong>Cloud ENI per Pod</strong>: AWS VPC CNI; each Pod gets its own ENI in the VPC; ENI count caps Pod density. Trunk ENI / IPv4 prefix delegation lifts the cap.</li>
    </ul>
    <p><strong>Scale gotchas</strong>: conntrack saturation at high CPS (especially short-lived connections) — tune <code>nf_conntrack_max</code>; switch to eBPF where conntrack isn\'t used. MTU mismatch causes silent drops on encap paths — set Pod MTU to (host MTU − encap overhead) explicitly. NodeLocal DNSCache reduces CoreDNS load 5×.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="Why does Cilium with eBPF outperform Calico with iptables at 10K-Service scale?",
            options=[
                ("Cilium uses a different language.", False),
                ("eBPF maps are O(1) hash lookups; iptables chains are O(N) and grow with Service count.", True),
                ("Cilium runs in userspace.", False),
            ],
            feedback="iptables chains are walked linearly per packet. At thousands of Services, latency adds up. eBPF maps replace the linear walk with hash lookups.",
        ),
        3: PauseCheck(
            question="A bare-metal cluster has high latency from encap tax. What\'s the path?",
            options=[
                ("Switch to overlay encryption.", False),
                ("Configure BGP between nodes + ToR switches; advertise Pod CIDRs natively.", True),
                ("Reduce Pod density.", False),
            ],
            feedback="BGP eliminates encap by routing Pod CIDRs natively via ToR. MetalLB / Cilium BGP / Calico BGP make this practical.",
        ),
    },
    before_after_before='<p>Pre-eBPF / pre-BGP, K8s networking ran on overlay (VXLAN / IP-in-IP) + iptables. At 10K-Service scale, iptables walks added latency. Encap reduced MTU + added CPU. Observability required tcpdump + ad-hoc tools.</p>',
    before_after_after='<p>Modern: eBPF datapath (Cilium / GKE Dataplane V2 / Calico eBPF) gives O(1) Service lookups; BGP native routing eliminates encap; Hubble / Pixie give built-in observability. Same hardware, 5× better latency tail.</p>',
    before_after_caption='<p class="ba-caption"><em>The kernel + the fabric matter. Pick CNI + routing model to match cluster scale + control.</em></p>',
    analogy_intro_html='''<p>K-Highway is the cluster\'s interstate. Every Pod is a vehicle entering the highway. The <strong>on-ramp</strong> (veth pair) connects the Pod\'s driveway to the host\'s lane. The <strong>highway controller</strong> (CNI plugin) decides which lane the vehicle takes, applies tolls (NetworkPolicy), and routes onward.</p>
    <p>Underneath the asphalt is a layer of <strong>kernel-level traffic management</strong> (eBPF) — tiny programmable rules that route, filter, and observe packets without ever leaving the kernel. Old highways used a long checklist (iptables) that every vehicle waited at; modern highways use a hash-keyed kiosk (eBPF map) — pull a slip, walk through.</p>
    <p>Beyond the cluster, the highway connects to the <strong>regional fabric</strong> via BGP. Each toll-booth (node) advertises its lane numbers (Pod CIDR) to the regional dispatch (ToR). Vehicles from another region can route directly to the right lane — no detour through tunnels.</p>''',
    translation_rows=[
        ("On-ramp", "veth pair (Pod ↔ host netns)"),
        ("Highway controller", "CNI plugin (Cilium / Calico / VPC CNI / Flannel)"),
        ("Kernel toll kiosks", "eBPF programs (TC ingress/egress, XDP, socket)"),
        ("Old long checklist at toll", "iptables chains (linear, slow at scale)"),
        ("Hash-keyed kiosk", "eBPF maps (O(1) lookups)"),
        ("Regional dispatch", "BGP peer (ToR / fabric)"),
        ("Lane numbers advertised", "Pod CIDRs advertised via BGP"),
        ("IP plate dispenser per region", "IPAM (CIDR-per-node / cluster-pool / ENI-per-Pod)"),
        ("Tunnel detour", "VXLAN / Geneve encapsulation"),
        ("Dashcam observability", "Hubble (Cilium eBPF flow log)"),
    ],
    analogy_stops="A highway\'s lanes are physical; CNI lanes are eBPF maps + iptables. Misconfiguration is invisible until a probe runs (tcpdump, hubble, kubectl trace).",
    eli5="Every Pod is a car entering the highway. A controller decides which lane it takes. The road has tiny smart sensors (eBPF) that route + observe in real time. The highway connects to the city via a regional dispatch (BGP) so cars don\'t need to take detours.",
    eli10="<strong>CNI</strong> = plugin model that gives a Pod a network. Cilium (eBPF), Calico (BGP / eBPF), VPC CNI (cloud), Flannel (overlay). <strong>eBPF</strong> = kernel-attached programs handling routing + LB + policy + observability in-kernel; replaces iptables for scale. <strong>BGP</strong> = native fabric routing of Pod CIDRs; eliminates encap tax; needs fabric cooperation. <strong>IPAM</strong>: CIDR-per-node, cluster-pool, or ENI-per-Pod. <strong>Scale gotchas</strong>: conntrack saturation, MTU mismatch, DNS load.",
    scenarios=[
        Scenario(
            name="Cilium eBPF migration — 5× latency tail improvement",
            body="A 200-engineer SaaS migrated from kube-proxy iptables to Cilium kube-proxy-replacement (eBPF). At 8K Services, P99 connection-setup latency dropped from 30ms to 6ms. Same hardware, same workloads.",
        ),
        Scenario(
            name="Bare-metal BGP — encap tax eliminated",
            body="A bare-metal cluster ran VXLAN encap; MTU reduced; CPU on encap rose 8% per node. Adopted Calico BGP peering with ToR switches; advertised Pod CIDRs; encap dropped; throughput rose 30%; CPU dropped.",
        ),
        Scenario(
            name="AWS VPC CNI ENI density crisis",
            body="A team ran AWS VPC CNI; m5.large nodes hit ENI limits; Pods stuck PENDING. Enabled <strong>prefix delegation</strong> (each ENI gets a /28); per-node Pod density rose 16×. Same instance type; same VPC.",
        ),
        Scenario(
            name="Outage — MTU mismatch",
            body="A team adopted a new CNI without updating Pod MTU. Encap packets exceeded host MTU; large requests silently dropped (small worked). 6-hour debug. Postmortem: explicit MTU calculation in CNI config; CI test for jumbo-payload paths.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"All CNIs are equivalent — pick the one that\'s defaulted.\"",
            truth="Major differences: NetPol support (Calico, Cilium yes; Flannel no), eBPF (Cilium, Calico yes; VPC CNI partial), ClusterMesh / multi-cluster (Cilium yes), observability (Cilium\'s Hubble vs nothing). Pick by feature needs, not default.",
        ),
        Misconception(
            myth="\"eBPF replaces iptables completely.\"",
            truth="In modern CNIs (Cilium, Calico-eBPF), eBPF replaces kube-proxy iptables for Service load balancing + NetPol. iptables/nftables remain for some host firewall + edge cases. Cilium has \"kube-proxy-replacement\" mode that fully eliminates kube-proxy.",
        ),
        Misconception(
            myth="\"BGP is too complex; just use overlay.\"",
            truth="For non-cloud clusters (bare-metal, on-prem), BGP is the standard. Calico\'s BIRD or Cilium\'s BGP Control Plane both handle the BGP-to-ToR peering with minimal config. The complexity vs encap tax trade favors BGP for scale.",
        ),
    ],
    flashcards=[
        Flashcard(front="What does CNI hand to a Pod?", back="A network interface (typically veth) + IP via IPAM + routes + DNS config. The CNI plugin is invoked by kubelet on Pod create/delete with a JSON config."),
        Flashcard(front="Three CNI families + what differentiates them?", back="<strong>Cilium</strong> (eBPF-native, rich features), <strong>Calico</strong> (BGP heritage, NetworkPolicy mature), <strong>cloud-managed</strong> (AWS VPC CNI / Azure CNI / GKE DPv2 — cloud-integrated)."),
        Flashcard(front="What does eBPF replace at K8s scale?", back="<strong>iptables</strong> chains for kube-proxy Service load balancing + NetworkPolicy enforcement. eBPF maps are O(1) lookups; iptables walks are O(N) per chain."),
        Flashcard(front="When can you use BGP?", back="When you control the fabric (bare-metal / on-prem) or your cloud allows BGP advertisements. Cloud-managed clusters (AWS / Azure / GCP) don\'t accept your BGP peers; they have their own routing."),
        Flashcard(front="Three IPAM patterns?", back="<strong>CIDR-per-node</strong> (each node a /24 slice), <strong>cluster-pool dynamic</strong> (CNI requests sub-CIDR on demand), <strong>cloud ENI per Pod</strong> (AWS VPC CNI; each Pod gets a VPC IP)."),
        Flashcard(front="What is Hubble?", back="Cilium\'s eBPF-based observability layer. Per-flow logs (source/dest, verdict, latency) without sidecars or packet capture. Foundation of cluster-wide network visibility."),
        Flashcard(front="MTU pitfall in CNI?", back="If Pod MTU = host MTU but the CNI uses encap (VXLAN / Geneve), encap header pushes packet over host MTU → fragmentation or drops. Set Pod MTU explicitly = host MTU − encap overhead."),
        Flashcard(front="Conntrack saturation symptom + fix?", back="High connection setup rate (CPS) overflows nf_conntrack_max → SYN drops + retries. Fix: tune <code>nf_conntrack_max</code> + <code>hashsize</code>; consider eBPF (which doesn\'t use conntrack for some flows)."),
    ],
    quizzes=[
        Quiz(
            prompt="A team\'s GKE cluster is fine but their on-prem K8s cluster has 4× higher P99 latency. Diagnose with the CNI + eBPF + BGP framework.",
            answer="Three checks in order. (1) <strong>kube-proxy / Service LB</strong>: is on-prem still iptables-based? Service-LB latency at scale is the most common culprit. Switch to Cilium kube-proxy-replacement or Calico eBPF. (2) <strong>Routing</strong>: is on-prem using overlay (VXLAN / IP-in-IP)? If the fabric supports BGP, configure peering — eliminate encap. Run tcpdump to confirm packets aren\'t encapsulated. (3) <strong>MTU + conntrack</strong>: tcpdump for fragmentation; check <code>nf_conntrack_count</code> vs <code>nf_conntrack_max</code>; resize if near limit. <strong>Hubble flow logs</strong> (or equivalent) on each cluster reveal latency per flow + verdict; comparing surfaces the gap quickly.",
        ),
        Quiz(
            prompt="A team adopted Cilium for the eBPF wins but kept Calico for NetworkPolicy because \"Cilium NetPol is too new.\" Defend or refute.",
            answer="<strong>Refute (gently).</strong> Cilium NetworkPolicy is GA + mature; the cluster running two CNIs is the riskier setup. Two CNIs means: (a) routing rules from both, often conflicting; (b) NetPol from both, with one likely silently shadowing the other; (c) two failure modes, two debugging tool sets, two operational teams. <strong>The path</strong>: pick one CNI; trust its NetPol implementation; if Cilium NetPol has a feature gap, file an upstream issue (Cilium responds quickly). The Calico-as-only-NetPol pattern is a transition state, not a long-term architecture. <strong>Cilium NetPol gives more</strong>: L7 policy (HTTP method / path), DNS-based egress, ClusterMesh policy across clusters — all things vanilla NetPol doesn\'t do.",
        ),
        Quiz(
            prompt="The CFO sees \"$2k/month for Hubble\" and asks to disable it. Defend.",
            answer="\"<strong>Hubble pays for itself in time-to-debug.</strong> Three reasons: (1) <strong>Per-flow visibility</strong>: when a Service is misbehaving, Hubble shows verdict per flow (allowed / dropped + reason) without packet capture or app changes. The next outage saves more than $2k in engineer hours. (2) <strong>NetworkPolicy debugging</strong>: \"why is Pod A failing to reach Pod B?\" Hubble answers in seconds — Hubble shows the policy verdict directly. Without it: tcpdump + manual rule walk = hours. (3) <strong>Compliance</strong>: regulated workloads need flow logs. Without Hubble, we\'re building bespoke logging. <strong>Trim instead</strong>: lower retention from 7 days to 1 day; cut cost ~70% while keeping live debugging. <strong>Don\'t disable a debug tool to save what one outage costs.</strong>\"",
            cyoa=True,
            cyoa_tag="how the network architect defended Hubble",
        ),
    ],
    glossary=[
        GlossaryItem(name="CNI", definition="Container Network Interface. Spec for plugins giving Pods networks. Plugin invoked by kubelet on Pod create/delete."),
        GlossaryItem(name="veth pair", definition="Linux virtual interface pair — one end in Pod netns, other end in host netns. Pod\'s on-ramp."),
        GlossaryItem(name="eBPF", definition="extended Berkeley Packet Filter — small programs attached to kernel hooks. Powers modern CNI datapath + observability + security."),
        GlossaryItem(name="iptables (kube-proxy)", definition="Legacy K8s Service load balancer using iptables chains. O(N) per packet at scale."),
        GlossaryItem(name="kube-proxy-replacement", definition="Cilium\'s mode replacing kube-proxy with eBPF programs. O(1) Service LB lookups."),
        GlossaryItem(name="BGP", definition="Border Gateway Protocol. Advertises Pod CIDRs to fabric (ToR switches); enables native routing without encap."),
        GlossaryItem(name="VXLAN / Geneve", definition="Overlay encapsulation. Wraps Pod packet in node-to-node tunnel. Adds MTU overhead + CPU."),
        GlossaryItem(name="Hubble", definition="Cilium\'s eBPF observability — per-flow logs + L7 verdicts + service map without sidecars."),
        GlossaryItem(name="IPAM", definition="IP address management. CIDR-per-node / cluster-pool / cloud ENI patterns."),
        GlossaryItem(name="conntrack", definition="Linux kernel connection-tracking. Saturates at high CPS; eBPF can bypass for some flows."),
    ],
    recap_lead="Three layers: CNI (Pod\'s network), eBPF (in-kernel datapath replacing iptables), BGP (native fabric routing eliminating encap tax). Pick by features, scale, control. Tune MTU + conntrack + DNS at scale.",
    recap_next='<strong>Next — N2: Gateway API at fleet scale.</strong> GatewayClass + Gateway + HTTPRoute / GRPCRoute / TCPRoute; cross-namespace routing via ReferenceGrant; BackendTLSPolicy; Ingress migration; controller choice (Envoy Gateway, Istio, Cilium, NGINX).',
)
