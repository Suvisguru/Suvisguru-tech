"""K-ADV-NET N3 — Multi-cluster networking."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Multi-cluster networking — four bridge options compared.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Inter-City Bridges · K-Highway — four ways to wire clusters together</text>
  <rect x="40" y="70" width="170" height="100" rx="10" fill="#3878B5" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Cilium ClusterMesh</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">eBPF; same-CNI</text>
  <text x="125" y="128" text-anchor="middle" font-size="9" fill="#FBF1D6">low-latency native</text>
  <rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Submariner</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">L4 IPsec tunnel</text>
  <text x="310" y="128" text-anchor="middle" font-size="9" fill="#1F2433">CNI-agnostic</text>
  <rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Skupper</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">app-layer (L7); Skupper VAN</text>
  <text x="495" y="128" text-anchor="middle" font-size="9" fill="#1F2433">no IP-routing required</text>
  <rect x="595" y="70" width="125" height="100" rx="10" fill="#5E4A8E" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Istio multi-cluster</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">mesh extends</text>
  <text x="657" y="128" text-anchor="middle" font-size="9" fill="#FBF1D6">across clusters</text>
</svg>"""


LESSON = LessonSpec(
    num="03",
    title_short="multi-cluster networking",
    title_full="N3 · Multi-Cluster Networking",
    title_html="K-ADV-NET N3 · Multi-Cluster",
    module_eyebrow="Module N3 · Inter-City Bridges — four ways to wire clusters together",
    hero_sub_html='Four bridge architectures. <strong>Cilium ClusterMesh</strong>: eBPF-native; same-CNI clusters peer; low-latency native routing; best when you control all clusters. <strong>Submariner</strong>: CNI-agnostic L4 IPsec tunnels between clusters; works across any CNI; tunnel overhead. <strong>Skupper</strong>: application-layer (Skupper VAN); no IP-route requirements; great for partner integrations across security domains. <strong>Istio multi-cluster</strong>: mesh extends across clusters with shared identity + policy; richer L7 features at higher complexity.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Cross-cluster traffic between us-east-1 + eu-west-1 is dropping 5% of packets. The team chose a bridge by feature checklist; nobody validated against real network conditions. <em>Bridge architecture should be picked from latency / encryption / security-model trade-offs, not feature parity.</em> Today\'s lesson: pick the right bridge by trust model + perf needs.",
    stamp_html="<strong>Cilium ClusterMesh: low-latency same-CNI; Submariner: CNI-agnostic L4 IPsec; Skupper: L7 app-layer no-IP-route; Istio multi-cluster: mesh extends with shared identity. Pick by trust + perf, not features alone.</strong>",
    district_pin="knet-junction03",
    district_label="Inter-City Bridges",
    sections=[
        Section(
            eyebrow="Section 1.1 · Cilium ClusterMesh",
            h2="eBPF-native, same-CNI peering",
            body_html="""    <p><strong>Cilium ClusterMesh</strong>: clusters running Cilium peer with each other via cluster-mesh-apiserver; etcd-replicated state; Pod-to-Pod traffic routes natively across cluster boundaries via eBPF. <em>Same identity model</em>: SPIFFE IDs unified across clusters; NetworkPolicy rules naturally apply across the mesh.</p>
    <p>Best fit: <em>same operator owns all clusters</em>; bandwidth + latency matter; eBPF observability (Hubble) extends across clusters. Common shape: 3-5 prod clusters in different cloud regions, all Cilium, ClusterMesh + global Services + multi-cluster Hubble.</p>
    <p>Constraints: requires Cilium on all clusters; Pod CIDRs must not overlap (tooling helps allocate); BGP / native routing across cloud region boundaries depends on cloud support (Cilium handles encap fallback).</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Submariner",
            h2="CNI-agnostic L4 IPsec across heterogeneous clusters",
            body_html="""    <p><strong>Submariner</strong>: opens IPsec tunnels between clusters via per-cluster gateways; routes traffic at L4 (Service IP / endpoint slice). Works regardless of CNI — Cilium + Calico + cloud CNI all peer.</p>
    <p>Best fit: <em>heterogeneous cluster fleet</em> (different CNIs, different clouds, including on-prem); L4 routing is enough (no L7 mesh required); operational simplicity.</p>
    <p>Constraints: tunnel encap reduces effective MTU + adds CPU; gateway-per-cluster is single point of failure (deploy redundant gateways). Service Discovery via Lighthouse (DNS) — services across clusters resolved via <code>service.namespace.svc.clusterset.local</code>.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Skupper",
            h2="Application-layer Virtual Application Network",
            body_html="""    <p><strong>Skupper</strong>: deploys per-namespace router; routers connect via TLS (egress only); Services exposed across the VAN. <em>No IP routing requirement</em> — clusters can be in completely different network zones (your VPC + partner VPC + on-prem firewalled DC) without VPN / peering / opening firewall ports.</p>
    <p>Best fit: <em>cross-organization integration</em>; partner Services exposed without giving network access; security-domain-segmented architectures.</p>
    <p>Constraints: L7 only; per-Service overhead (router Pod); not suitable for high-bandwidth east-west; latency higher than ClusterMesh / Submariner. Good for control-plane integrations + occasional service calls; not for replication-heavy workloads.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · Istio multi-cluster + selection",
            h2="mesh-spanning + how to choose",
            body_html="""    <p><strong>Istio multi-cluster</strong>: extends the mesh across clusters with shared / replicated control plane. Two patterns: <em>primary-remote</em> (one control plane manages others) + <em>multi-primary</em> (per-cluster control plane, replicated state). Workload identity unified via SPIFFE federation; AuthorizationPolicy + VirtualService work cluster-spanning.</p>
    <p>Best fit: <em>mesh-heavy deployments</em> already using Istio; rich L7 features required (canary + traffic shifting + mesh observability across clusters); ambitious complexity tolerance.</p>
    <p><strong>Selection grid</strong>: Same operator, all Cilium, low-latency → ClusterMesh. Heterogeneous CNIs, L4 enough → Submariner. Cross-org / firewall-segmented → Skupper. Already on Istio mesh → Istio multi-cluster. Some teams run two (e.g., ClusterMesh internal + Skupper for partners).</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="Three same-cloud Cilium-based clusters need low-latency cross-cluster traffic. Which bridge?",
            options=[
                ("Skupper.", False),
                ("Cilium ClusterMesh — same-CNI, eBPF-native, no encap tax.", True),
                ("Istio multi-cluster.", False),
            ],
            feedback="ClusterMesh is the right answer — same operator, same CNI, native eBPF routing. Lowest latency, native NetPol propagation, native Hubble observability.",
        ),
        3: PauseCheck(
            question="A partner organisation wants to expose one Service to your cluster without giving you VPN or VPC peering. Which bridge?",
            options=[
                ("Cilium ClusterMesh.", False),
                ("Skupper — app-layer VAN; no IP routing required; egress-only TLS.", True),
                ("Submariner.", False),
            ],
            feedback="Skupper is purpose-built for cross-organization integration without network-layer access. Egress-only TLS connections; no VPN, no peering.",
        ),
    },
    before_after_before='<p>Pre-multi-cluster bridges, cross-cluster integration was VPN + manual Service registration + DNS hacks. Each new cluster pair was bespoke; observability fragmented; security model fragile.</p>',
    before_after_after='<p>Modern: ClusterMesh / Submariner / Skupper / Istio multi-cluster handle the bridge per architecture. Native Service discovery, unified identity, per-bridge policy. Pick by trust model + perf needs.</p>',
    before_after_caption='<p class="ba-caption"><em>Bridge choice is architectural, not feature-checklist. Match to trust + latency + CNI.</em></p>',
    analogy_intro_html='''<p>K-Highway connects to other K-cities via four kinds of <strong>bridge</strong>. The <strong>twin-city expressway</strong> (Cilium ClusterMesh) — both cities share the same urban planner; lanes connect natively; vehicles drive across without slowing. The <strong>border-tunnel</strong> (Submariner) — works between any two cities regardless of urban-planning style; encrypted; some toll. The <strong>diplomatic-pouch service</strong> (Skupper) — one city sends sealed couriers via TLS; no road crossing required; great for foreign-city partners. The <strong>shared-rail-network</strong> (Istio multi-cluster) — mesh-style passenger trains run across both cities under shared identity.</p>
    <p>The Captain doesn\'t pick by feature; she picks by <strong>who runs the cities</strong> (one operator vs many) + <strong>how fast traffic must flow</strong> + <strong>whether neighbours allow open lanes</strong>.</p>''',
    translation_rows=[
        ("Twin-city expressway", "Cilium ClusterMesh (same-CNI eBPF native)"),
        ("Border-tunnel", "Submariner (L4 IPsec tunnel; CNI-agnostic)"),
        ("Diplomatic-pouch courier", "Skupper (L7 application-layer VAN)"),
        ("Shared-rail mesh", "Istio multi-cluster (mesh extends with shared identity)"),
        ("Twin-city map", "Cilium ClusterMesh global Services + multi-cluster Hubble"),
        ("Border-tunnel discovery", "Submariner Lighthouse DNS"),
        ("Sealed courier registry", "Skupper VAN Service exposure"),
        ("Mesh-wide identity", "SPIFFE federation across clusters"),
    ],
    analogy_stops="A real bridge can be physically inspected; cluster bridges are policy + encryption + routing — invisible. Synthetic test traffic between clusters is the only reliable verification.",
    eli5="Four kinds of bridges. Same-style cities use a smooth expressway. Different-style cities use a tunnel. Foreign neighbours use a sealed courier. Cities running shared trains use shared rails. Pick by who you\'re connecting + how often traffic flows.",
    eli10="<strong>ClusterMesh</strong>: same-CNI Cilium clusters; eBPF native; lowest latency; unified identity. <strong>Submariner</strong>: CNI-agnostic L4 IPsec gateway pattern; tunnels; Lighthouse DNS. <strong>Skupper</strong>: L7 application VAN; egress-only TLS; no IP-routing required; partner-org pattern. <strong>Istio multi-cluster</strong>: primary-remote or multi-primary; SPIFFE federation; mesh L7 features extend.",
    scenarios=[
        Scenario(
            name="Same-org 5-cluster Cilium ClusterMesh",
            body="A 100-engineer org runs 5 Cilium-on-EKS clusters across 3 regions. ClusterMesh peers them; global Services route to nearest cluster; Hubble shows cross-cluster flows. <em>One identity model, native routing, eBPF observability.</em>",
        ),
        Scenario(
            name="Bank — Submariner across heterogeneous CNIs",
            body="Bank has Cilium-on-EKS + Calico-on-bare-metal + Azure CNI on AKS. Submariner peers all three at L4; gateway redundancy in each; tunnels IPsec-encrypted. CNI heterogeneity preserved; cross-cluster Service discovery via Lighthouse.",
        ),
        Scenario(
            name="Skupper for partner SaaS integration",
            body="A retailer\'s SaaS partner needs to call one billing-Service in our cluster + nothing else. Skupper VAN: partner-side router peers with our router via TLS over public Internet; Service exposed only via the VAN; no VPN, no firewall changes, partner sees nothing else.",
        ),
        Scenario(
            name="Outage — Submariner gateway single point of failure",
            body="A team deployed Submariner with one gateway per cluster. The gateway Pod restarted; cross-cluster traffic dropped for 90 seconds. Postmortem: deploy 2+ gateways per cluster + globalnet HA mode; failover is sub-second. Updated runbook + IaC.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Pick whichever bridge works first.\"",
            truth="Bridge choice is architectural. Switching bridges later means re-running every cross-cluster Service through new connection paths. Pick deliberately based on trust model + perf + heterogeneity.",
        ),
        Misconception(
            myth="\"Multi-cluster mesh requires Istio.\"",
            truth="ClusterMesh / Submariner / Skupper all do multi-cluster Service discovery + connectivity without Istio. Istio mesh is required only when you need full L7 mesh features (canary by header, traffic mirroring, complex AuthorizationPolicy) <em>across clusters</em>.",
        ),
        Misconception(
            myth="\"Skupper is too slow for production.\"",
            truth="Skupper is L7 app-layer; latency higher than IP-level bridges. <em>Right tool for partner integrations + control-plane calls</em>; not for high-bandwidth east-west replication. Used for the right pattern, it\'s production-grade.",
        ),
    ],
    flashcards=[
        Flashcard(front="Four multi-cluster bridge options?", back="<strong>Cilium ClusterMesh</strong> (same-CNI eBPF), <strong>Submariner</strong> (L4 IPsec, CNI-agnostic), <strong>Skupper</strong> (L7 app-layer VAN, no-IP-route), <strong>Istio multi-cluster</strong> (mesh extends; primary-remote / multi-primary)."),
        Flashcard(front="ClusterMesh — when does it shine?", back="Same operator, all Cilium, low-latency required, eBPF observability + NetPol naturally extend. Common in same-org multi-region deployments."),
        Flashcard(front="Submariner Service discovery?", back="<strong>Lighthouse</strong> — multicluster DNS plugin. Services resolve via <code>my-svc.my-ns.svc.clusterset.local</code> (or per-cluster). Works across CNIs."),
        Flashcard(front="Skupper VAN — what is it?", back="Application-level Virtual Application Network. Per-namespace router connects to other-cluster routers via TLS (egress only). Services exposed across VAN; no L3 routing involved."),
        Flashcard(front="Istio multi-cluster patterns?", back="<strong>primary-remote</strong> (one control plane manages others) and <strong>multi-primary</strong> (per-cluster control planes, replicated state). SPIFFE federation = unified workload identity."),
        Flashcard(front="When is L7-only (Skupper) the right answer?", back="Cross-organization integration, security-domain-segmented architectures, partners that won\'t allow VPN / peering. Egress-only TLS suffices."),
        Flashcard(front="Pod CIDR overlap — what bridge handles it?", back="<strong>Submariner Globalnet</strong> + <strong>Cilium ClusterMesh global services</strong> handle overlap via NAT or virtual CIDRs. Skupper / Istio multi-cluster sidestep at L7."),
        Flashcard(front="Multi-cluster failure mode?", back="Bridge gateway single point of failure (Submariner gateway Pod restart). Always deploy 2+ gateways or HA mode. Bridge endpoint health monitoring + alarms."),
    ],
    quizzes=[
        Quiz(
            prompt="A team runs 3 Cilium-on-EKS clusters + 1 partner Calico-on-OCP cluster. Cross-cluster traffic between the EKS clusters is high; the partner needs only one Service exposed. Design.",
            answer="<strong>Two bridges.</strong> (1) <strong>Cilium ClusterMesh</strong> across the 3 EKS clusters: low-latency native routing, unified identity, Hubble cross-cluster observability. (2) <strong>Skupper</strong> from the partner cluster to one of the EKS clusters: L7 VAN exposes only the specific Service to the partner; egress-only TLS; no VPN. <em>The two bridges coexist on the same cluster</em>; ClusterMesh handles internal east-west, Skupper handles partner-org integration. Avoid: trying to use one bridge for both — wrong tool for half the use case.",
        ),
        Quiz(
            prompt="An on-call engineer reports cross-cluster latency spike via Cilium ClusterMesh. Walk diagnostic steps.",
            answer="(1) <strong>Hubble flow logs</strong>: cross-cluster flows show source/dest cluster; identify the impacted path. (2) <strong>Cluster-mesh-apiserver health</strong>: <code>cilium clustermesh status</code> on each cluster; etcd replication healthy? (3) <strong>Underlying network</strong>: cross-region cloud network — provider issue (AWS Health Dashboard, GCP Cloud Status)? (4) <strong>Encap path</strong>: if cross-cloud, encap is unavoidable; check MTU + packet drops via tcpdump on a transit node. (5) <strong>BGP / route table</strong>: Pod-CIDR routes correctly advertised? (6) <strong>Workload contention</strong>: high CPU on the gateway / mesh proxy path? (7) <strong>Mitigation</strong>: shift traffic to a healthier cluster region; engage cloud provider if their fabric. Postmortem documents which signal led to root cause; updates runbook.",
        ),
        Quiz(
            prompt="A team wants to migrate from Submariner (CNI-agnostic, working) to Cilium ClusterMesh for performance. Defend whether to migrate or stay.",
            answer="\"<strong>Migrate only if perf gains justify the effort + you can standardise on Cilium across all clusters.</strong> Three considerations: (1) <strong>CNI homogeneity</strong>: ClusterMesh requires Cilium everywhere. If on-prem is Calico for compliance reasons, you can\'t migrate the on-prem path; you\'d run two bridges. (2) <strong>Perf delta</strong>: Submariner adds tunnel + IPsec overhead; ClusterMesh native routing is materially faster (5-10ms vs 15-25ms cross-region — depends on path). For latency-sensitive paths the migration pays. (3) <strong>Migration cost</strong>: gradual via dual-bridge period (both up; shift Service-by-Service); validation per workload; teams need ClusterMesh training. <strong>If the perf gain is &gt; 10% of P95 SLO budget, migrate</strong>; otherwise the current Submariner is fine. The bridge that works is the bridge that stays.\"",
            cyoa=True,
            cyoa_tag="how the network architect framed migration",
        ),
    ],
    glossary=[
        GlossaryItem(name="Cilium ClusterMesh", definition="Same-CNI eBPF-based multi-cluster bridge. Native routing, unified identity, Hubble observability."),
        GlossaryItem(name="Submariner", definition="CNI-agnostic L4 IPsec tunnel multi-cluster bridge. Lighthouse DNS for service discovery."),
        GlossaryItem(name="Skupper", definition="Application-layer VAN multi-cluster + cross-organization bridge. Egress-only TLS routers per namespace."),
        GlossaryItem(name="Istio multi-cluster", definition="Mesh extends across clusters; primary-remote or multi-primary; SPIFFE federation."),
        GlossaryItem(name="Submariner Globalnet", definition="Submariner feature handling Pod-CIDR overlap via NAT to virtual CIDRs."),
        GlossaryItem(name="cluster-mesh-apiserver", definition="ClusterMesh control-plane component replicating cluster state via etcd."),
        GlossaryItem(name="Lighthouse", definition="Submariner multicluster-DNS plugin. Service resolution across clusters."),
        GlossaryItem(name="Skupper VAN", definition="Skupper Virtual Application Network. App-layer mesh formed by per-namespace routers."),
        GlossaryItem(name="SPIFFE federation", definition="Cross-trust-domain workload identity. Multiple SPIRE servers federate; mesh-mTLS works across clusters."),
        GlossaryItem(name="globalnet", definition="Submariner address-translation for overlapping Pod-CIDRs. Each cluster gets a virtual CIDR; NAT bridges."),
    ],
    recap_lead="Four bridges, four trade-offs. ClusterMesh for same-CNI low-latency. Submariner for heterogeneous L4. Skupper for partner-org L7. Istio multi-cluster for mesh-heavy. Pick by trust + perf + heterogeneity.",
    recap_next='<strong>Next — N4: Service mesh + DNS scaling + IPv6.</strong> Mesh selection + operation; CoreDNS + NodeLocal DNSCache scaling; IPv6 + dual-stack at scale.',
)
