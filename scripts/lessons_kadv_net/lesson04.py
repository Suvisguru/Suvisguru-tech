"""K-ADV-NET N4 — Service mesh + DNS scaling + IPv6/dual-stack."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mesh + DNS + IPv6 — three concerns at scale.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Express Lanes · K-Highway — three scale concerns interlock</text>
  <rect x="40" y="70" width="200" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Service mesh</text>
  <text x="140" y="108" text-anchor="middle" font-size="9" fill="#1F2433">Istio / Linkerd / Cilium</text>
  <text x="140" y="128" text-anchor="middle" font-size="9" fill="#1F2433">sidecar / ambient</text>
  <rect x="260" y="70" width="200" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="360" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">DNS at scale</text>
  <text x="360" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">CoreDNS + NodeLocal</text>
  <text x="360" y="128" text-anchor="middle" font-size="9" fill="#FBF1D6">+ ndots:1 + autoPath</text>
  <rect x="480" y="70" width="240" height="100" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">IPv6 + dual-stack</text>
  <text x="600" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">node + Pod + Service</text>
  <text x="600" y="128" text-anchor="middle" font-size="9" fill="#FBF1D6">staged migration</text>
</svg>"""


LESSON = LessonSpec(
    num="04",
    title_short="mesh + DNS + IPv6",
    title_full="N4 · Service Mesh + DNS Scaling + IPv6/Dual-Stack",
    title_html="K-ADV-NET N4 · Mesh + DNS + IPv6",
    module_eyebrow="Module N4 · Express Lanes — three scale concerns interlock",
    hero_sub_html='<strong>Service mesh selection</strong>: Istio (rich features, complex), Linkerd (Rust, simple, fast), Cilium Service Mesh (eBPF-native), Kuma. Sidecar vs ambient. <strong>DNS at scale</strong>: CoreDNS + NodeLocal DNSCache (5× CoreDNS load reduction); ndots:1 + autoPath; CoreDNS replicas + autoscaling. <strong>IPv6 / dual-stack</strong>: enable on cluster + CNI + Service; staged migration; legacy app readiness; hostNetwork edge cases.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. CoreDNS is overloaded; DNS resolution timing out; cluster-wide service-to-service calls failing. <em>The team didn\'t deploy NodeLocal DNSCache + ndots:1 was the default + CoreDNS had 2 replicas for 500 nodes</em>. Today\'s lesson: tune mesh + DNS + IPv6 before they bottleneck.",
    stamp_html="<strong>Pick mesh by needs (Istio rich; Linkerd simple-fast; Cilium eBPF-native). NodeLocal DNSCache + ndots:1 are non-optional at scale. IPv6 / dual-stack: enable per layer; legacy apps need readiness checks.</strong>",
    district_pin="knet-junction04",
    district_label="Express Lanes",
    sections=[
        Section(
            eyebrow="Section 1.1 · Service mesh selection",
            h2="Istio · Linkerd · Cilium Service Mesh · Kuma",
            body_html="""    <p><strong>Istio</strong>: most features (traffic shifting + canaries + AuthorizationPolicy + L7 metrics + multi-cluster); largest ecosystem; sidecar or ambient mode. Highest complexity; most operational tools needed.</p>
    <p><strong>Linkerd</strong>: Rust micro-proxy; minimal overhead; SPIFFE-based identity; simple operational model; ambient-style by default. Recommended for teams wanting mTLS + retries + metrics without Istio\'s feature surface.</p>
    <p><strong>Cilium Service Mesh</strong>: eBPF-native; integrates with Cilium NetPol + Hubble. Sidecar-less; can run with or without Envoy. Picks if cluster CNI is already Cilium.</p>
    <p><strong>Kuma</strong>: built on Envoy; multi-cluster + multi-mesh patterns; vendor-supported by Kong. Niche compared to Istio / Linkerd / Cilium for K8s-only deployments.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · DNS at scale",
            h2="CoreDNS + NodeLocal DNSCache + ndots tuning",
            body_html="""    <p><strong>CoreDNS</strong> is the cluster DNS server (replaced kube-dns long ago). At scale, CoreDNS Pods become the bottleneck — every Pod resolution hits them.</p>
    <p><strong>NodeLocal DNSCache</strong>: a DaemonSet that runs a CoreDNS instance on every node + intercepts DNS queries via iptables / IPVS. <em>5× reduction in CoreDNS Pod load</em> + lower P99 latency (cache hit on local node = sub-millisecond).</p>
    <p><strong>ndots:1 + autoPath</strong>: K8s default <code>ndots:5</code> means short names are tried with cluster.local + namespace + svc + cluster suffixes — many DNS queries per resolution. Setting <code>ndots:1</code> + autoPath collapses this to fewer queries; further reduces CoreDNS load.</p>
    <p><strong>Sizing</strong>: CoreDNS replicas should scale with node count; HPA on CoreDNS Pods + NodeLocal DNSCache as DaemonSet is the production pattern.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · IPv6 + dual-stack",
            h2="cluster + CNI + Service + Pod IPv6 enablement",
            body_html="""    <p><strong>Dual-stack</strong>: cluster runs both IPv4 + IPv6. Enable across layers:</p>
    <ul>
      <li><strong>kubelet</strong>: <code>--cluster-dns</code> with both v4 + v6 IPs.</li>
      <li><strong>kube-apiserver</strong> + <strong>kube-controller-manager</strong>: <code>--service-cluster-ip-range=10.96.0.0/12,fd00::/108</code> (dual ranges).</li>
      <li><strong>CNI</strong>: Cilium / Calico / VPC CNI all support IPv6 + dual-stack — enable per CNI config.</li>
      <li><strong>Service</strong>: <code>ipFamilyPolicy: PreferDualStack</code> (or RequireDualStack); Services get both v4 + v6 IPs.</li>
    </ul>
    <p><strong>App readiness</strong>: legacy apps may bind only to <code>0.0.0.0</code> (v4) — they don\'t accept v6 traffic. Audit + fix bind addresses to <code>[::]</code> or use dual binds. Tools: <code>netstat</code> / <code>ss</code> on running Pods.</p>
    <p><strong>Migration</strong>: enable dual-stack first; verify v4 still works; gradually shift to v6-primary as apps support it; eventually drop v4 for closed environments.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · interactions + tuning playbook",
            h2="how mesh + DNS + IPv6 interact",
            body_html="""    <p>The three layers interact:</p>
    <ul>
      <li>Mesh adds DNS load (sidecar resolves backends) — NodeLocal DNSCache critical.</li>
      <li>Mesh + IPv6: ensure mesh control plane + sidecars support v6 explicitly. Istio + Linkerd both do; verify in deployment.</li>
      <li>NodeLocal DNSCache must be configured for v6 query patterns when dual-stack.</li>
    </ul>
    <p><strong>Tuning playbook (for any cluster &gt; 100 nodes)</strong>:</p>
    <ol>
      <li>Deploy NodeLocal DNSCache. Drop <code>ndots:1</code>. Verify CoreDNS load.</li>
      <li>Pick + deploy mesh. Audit DNS query patterns post-mesh.</li>
      <li>If IPv6 required: enable per layer; staged.</li>
      <li>Hubble / Pixie / kube-burner profile cluster: latency, error rates, DNS hit ratio.</li>
      <li>Iterate: tune CoreDNS replicas, mesh sidecar resources, IPv6 readiness.</li>
    </ol>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A team wants mTLS + observability without Istio\'s complexity. Which mesh?",
            options=[
                ("Istio (you grow into it).", False),
                ("Linkerd — Rust micro-proxy, minimal overhead, simple operational model.", True),
                ("No mesh — handle mTLS in apps.", False),
            ],
            feedback="Linkerd is purpose-built for the simple-and-fast case. mTLS + retries + metrics out of the box; Istio\'s feature surface optional later.",
        ),
        3: PauseCheck(
            question="A 200-node cluster\'s CoreDNS hits 80% CPU. First action?",
            options=[
                ("Add CoreDNS replicas.", False),
                ("Deploy NodeLocal DNSCache + set ndots:1 — 5× reduction in CoreDNS load.", True),
                ("Switch DNS server.", False),
            ],
            feedback="NodeLocal DNSCache + ndots tuning typically cuts CoreDNS load 5×. Always deploy at &gt; 100 nodes; replica scaling alone is wasteful.",
        ),
    },
    before_after_before='<p>Pre-tuning: mesh adds latency, DNS bottlenecks, IPv6 deferred indefinitely. Cluster scale hits a wall around 200-300 nodes.</p>',
    before_after_after='<p>Tuned: mesh chosen by need (Linkerd simple, Istio for L7 features, Cilium for eBPF-native); NodeLocal DNSCache + ndots:1; dual-stack rolled per layer with app readiness audit. Cluster scales to 1000+ nodes cleanly.</p>',
    before_after_caption='<p class="ba-caption"><em>Three concerns; each has a known tuning answer; ignore at your scale-pain peril.</em></p>',
    analogy_intro_html='''<p>Express Lanes are the cluster\'s high-speed conveyors. Three concerns interlock. The <strong>express-lane operator</strong> (mesh) decides which lanes get TLS-sealed envelopes + retries + metrics. The <strong>sign-system</strong> (DNS) tells every vehicle where to exit; without local cached signs at every intersection, the central sign office is overwhelmed. The <strong>address registry</strong> (IPv6) lets the highway have many more lanes — staged across the system.</p>
    <p>Each concern has a known tuning. The Captain\'s job is to enable each at the right cluster scale.</p>''',
    translation_rows=[
        ("Express-lane operator", "Service mesh (Istio / Linkerd / Cilium / Kuma)"),
        ("Sealed envelopes + retries", "mTLS + automatic retries + observability"),
        ("Sidecar courier next to vehicle", "Sidecar mode (per-Pod proxy)"),
        ("Per-floor courier", "Ambient mode (per-node + per-namespace proxy)"),
        ("Sign-system office (central)", "CoreDNS Pods"),
        ("Local cached signs", "NodeLocal DNSCache (DaemonSet)"),
        ("Ride-share routing tweaks", "ndots:1 + autoPath"),
        ("Wider address registry", "IPv6 / dual-stack at every layer"),
    ],
    analogy_stops="A real express lane has visible pavement; mesh + DNS + IPv6 are policy + config + kernel state. Verify with synthetic queries + Hubble flow logs.",
    eli5="Three things to tune for fast highways. Pick a courier service for sealed packages. Put a local sign-cache at every block so the central sign office isn\'t overwhelmed. Add longer license plates for more cars (IPv6).",
    eli10="<strong>Mesh</strong>: Istio (rich, complex), Linkerd (simple, Rust, fast), Cilium SM (eBPF-native), Kuma (Envoy + multi-mesh). Sidecar or ambient. <strong>DNS scale</strong>: NodeLocal DNSCache (5× reduction) + ndots:1 + autoPath. <strong>IPv6</strong>: enable per layer (kubelet / apiserver / CNI / Service); audit app bind addresses; gradual migration.",
    scenarios=[
        Scenario(
            name="Linkerd for simple mTLS",
            body="A 30-engineer team needs mTLS + retries + metrics. Adopts Linkerd cluster-wide; ~5 MiB per Pod overhead; CLI annotates namespaces; no Rego-style complexity. mTLS automatic; per-Service metrics in Grafana.",
        ),
        Scenario(
            name="NodeLocal DNSCache cut CoreDNS load 80%",
            body="500-node cluster; CoreDNS Pods at 90% CPU; queries 50K rps. Deployed NodeLocal DNSCache (DaemonSet) + dropped to ndots:1. Within 30 min: CoreDNS load 18%; P99 DNS latency 0.3ms; queries to CoreDNS Pods dropped to ~10K rps.",
        ),
        Scenario(
            name="IPv6 readiness audit before migration",
            body="A team auditing 200 services found 35 with hardcoded IPv4 binds. 3-month rolling fix; staged dual-stack rollout; gradual flip to v6-primary. Saved a major outage that would have hit during v4-deprecation deadline.",
        ),
        Scenario(
            name="Istio ambient migration — sidecar overhead halved",
            body="A 1000-Pod Istio sidecar deployment migrated to Istio ambient mode. Per-Pod overhead dropped from ~50 MiB to ~5 MiB; control plane simpler; same mTLS + AuthorizationPolicy. 6-week migration; namespace-by-namespace.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Istio is the only mature mesh.\"",
            truth="Linkerd is CNCF Graduated + production-grade for years. Cilium Service Mesh is eBPF-native. Kuma is Envoy-based. Istio has the most features; not always the right tool.",
        ),
        Misconception(
            myth="\"NodeLocal DNSCache is optional.\"",
            truth="At any cluster &gt; 100 nodes, it\'s a non-optional best practice. Without it, CoreDNS Pods saturate; DNS latency drives every cluster-internal call slower; cluster-wide cascades follow.",
        ),
        Misconception(
            myth="\"IPv6 isn\'t needed yet.\"",
            truth="Cloud providers + many enterprises have IPv6 mandates within 1-3 years. App readiness audits take months. Start dual-stack now; treat v6 as the foundation, not a deferred add-on.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three popular service meshes + their tradeoffs?", back="<strong>Istio</strong> (rich features + complexity), <strong>Linkerd</strong> (Rust micro-proxy + simple), <strong>Cilium SM</strong> (eBPF-native, Cilium-CNI integration). Plus Kuma (Envoy + multi-mesh)."),
        Flashcard(front="What does NodeLocal DNSCache do?", back="DaemonSet running a CoreDNS instance on every node; intercepts DNS queries via iptables / IPVS; cache hits in-node = sub-ms. 5× reduction in CoreDNS Pod load."),
        Flashcard(front="ndots:1 vs ndots:5?", back="ndots:5 (default) tries cluster.local + namespace.svc + ... suffixes for short names = many DNS queries per resolution. ndots:1 + autoPath collapses to fewer queries. Cuts CoreDNS load."),
        Flashcard(front="IPv6 enablement layers?", back="<strong>kubelet</strong> (--cluster-dns dual), <strong>apiserver</strong> + <strong>controller-manager</strong> (--service-cluster-ip-range dual), <strong>CNI</strong> (per CNI config), <strong>Service</strong> (ipFamilyPolicy: PreferDualStack)."),
        Flashcard(front="Common app-readiness IPv6 issue?", back="App binds only to <code>0.0.0.0</code> (v4); doesn\'t accept v6 traffic. Fix to <code>[::]</code> dual-bind or per-language equivalent. Audit before migration."),
        Flashcard(front="Sidecar vs ambient mesh mode?", back="<strong>Sidecar</strong>: Envoy / proxy per Pod; ~50 MiB per Pod; per-Pod policy. <strong>Ambient</strong>: per-node ztunnel + per-namespace waypoint proxy; ~5 MiB per Pod; same mTLS guarantees."),
        Flashcard(front="When add CoreDNS replicas?", back="After NodeLocal DNSCache is in place + ndots tuned. Replicas scale with node count; HPA on CoreDNS Pods. Per ~250 nodes, +1 CoreDNS replica is a baseline."),
        Flashcard(front="autoPath — what is it?", back="DNS feature in CoreDNS that resolves Pod-to-Service queries directly without iterating through search-path suffixes. Reduces CoreDNS load + cuts P99 DNS latency."),
    ],
    quizzes=[
        Quiz(
            prompt="A 500-node cluster reports DNS-related connection failures during peak. Walk diagnostic + fix.",
            answer="(1) <strong>Measure</strong>: CoreDNS Pods\' CPU + queries-per-second. (2) <strong>Verify</strong>: NodeLocal DNSCache deployed? (<code>kubectl get ds node-local-dns -n kube-system</code>). (3) If absent: <strong>deploy NodeLocal DNSCache</strong> first; expect 5× CoreDNS load reduction. (4) <strong>Tune ndots</strong> via PodDNSConfig at cluster level (kubelet) or per Service. (5) <strong>Scale CoreDNS</strong>: HPA min=2 + 1 per 250 nodes. (6) <strong>Profile</strong>: which queries dominate? Service-to-Service short names (use FQDN to avoid search-path) or external DNS (cache external responses longer). (7) <strong>Mesh impact</strong>: if Istio sidecars resolve frequently, configure mesh to use NodeLocal DNSCache too.",
        ),
        Quiz(
            prompt="A team wants Istio for ambient mode\'s lower overhead. Walk the migration from sidecar.",
            answer="(1) <strong>Upgrade Istio</strong> to a release with ambient GA. (2) <strong>Install ambient components</strong>: ztunnel DaemonSet + waypoint proxies. (3) <strong>Per-namespace migration</strong>: label namespace <code>istio.io/dataplane-mode: ambient</code>; new Pods skip sidecar injection; existing Pods get rolled. (4) <strong>Validate per-namespace</strong>: mTLS still enforced; AuthorizationPolicy works; metrics still emit. (5) <strong>Iterate</strong>: namespace-by-namespace; expect 4-6 weeks for 30+ namespaces. (6) <strong>Operational changes</strong>: ambient debugging differs (no per-Pod sidecar logs); update runbooks. (7) <strong>Decommission sidecars</strong> per namespace as ambient validates.",
        ),
        Quiz(
            prompt="The CFO sees mesh sidecar memory cost ($1k/month at 1000 Pods). Asks to remove mesh. Defend.",
            answer="\"<strong>Mesh provides mTLS + retries + L7 observability — three things we\'d need to rebuild without it.</strong> Three reasons mesh stays: (1) <strong>mTLS at scale</strong>: replacing mesh-mTLS means handcrafting cert + workload identity per Service. Months of engineering for one already-solved problem. (2) <strong>Retries + observability</strong>: mesh emits per-Service metrics free; without mesh, every team instruments individually = inconsistent + incomplete. (3) <strong>Operational regression</strong>: lateral-movement defence comes from mTLS. Removing it = single-Pod compromise spreads cluster-wide. <strong>The right move: migrate to ambient mode</strong> ($1k → ~$100/month) instead of removing. Keep the value; cut the cost.\"",
            cyoa=True,
            cyoa_tag="how the network architect defended mesh",
        ),
    ],
    glossary=[
        GlossaryItem(name="Service mesh", definition="Sidecar / ambient proxy layer providing mTLS + retries + observability. Istio / Linkerd / Cilium SM / Kuma."),
        GlossaryItem(name="Sidecar mode", definition="Per-Pod proxy (Envoy / Linkerd-proxy). Per-Pod memory overhead; per-Pod policy."),
        GlossaryItem(name="Ambient mode", definition="Per-node ztunnel + per-namespace waypoint proxy. Lower overhead; same mTLS."),
        GlossaryItem(name="CoreDNS", definition="K8s cluster DNS server; CNCF project. Replaced kube-dns long ago."),
        GlossaryItem(name="NodeLocal DNSCache", definition="DaemonSet running CoreDNS on every node; 5× reduction in central CoreDNS load."),
        GlossaryItem(name="ndots", definition="Resolver option: number of dots required before name treated as fully qualified. K8s default 5; cluster scale wants 1."),
        GlossaryItem(name="autoPath", definition="CoreDNS feature short-cutting search-path iteration for in-cluster Service queries."),
        GlossaryItem(name="dual-stack", definition="Cluster runs both IPv4 + IPv6. Per-layer config (kubelet / apiserver / CNI / Service)."),
        GlossaryItem(name="ipFamilyPolicy", definition="Service spec field: SingleStack / PreferDualStack / RequireDualStack."),
        GlossaryItem(name="Linkerd", definition="CNCF Graduated mesh; Rust micro-proxy; SPIFFE identity; simple operational model."),
    ],
    recap_lead="Three concerns: mesh (Istio / Linkerd / Cilium SM / Kuma; sidecar vs ambient); DNS at scale (NodeLocal DNSCache + ndots:1); IPv6 / dual-stack (per-layer enablement + app readiness). All three are non-optional past 100 nodes.",
    recap_next='<strong>Next — N5: NetworkPolicy at scale + egress + private + hybrid.</strong> AdminNetworkPolicy + NetworkPolicy hierarchy; egress gateway; private clusters; hybrid (VPN + Direct Connect / ExpressRoute) connectivity.',
)
