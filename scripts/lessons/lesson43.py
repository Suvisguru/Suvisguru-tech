from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Switchboard mesh wing: a control plane (Istio/Linkerd/Cilium) drawing a graph of services, mTLS padlocks on every edge, sidecar/ambient mode comparison, observability stream.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">SWITCHBOARD · SERVICE MESH WING</text>
  <g transform="translate(40,55)"><rect width="240" height="120" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/><text x="120" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">SERVICE GRAPH</text>
    <circle cx="60" cy="60" r="20" fill="#5A9F7A"/><text x="60" y="64" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">A</text>
    <circle cx="140" cy="50" r="20" fill="#4A8FA8"/><text x="140" y="54" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">B</text>
    <circle cx="200" cy="80" r="20" fill="#A04832"/><text x="200" y="84" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">C</text>
    <circle cx="100" cy="100" r="20" fill="#E8B547"/><text x="100" y="104" text-anchor="middle" font-size="8" fill="#5A4F45" font-weight="700">D</text>
    <line x1="80" y1="60" x2="120" y2="55" stroke="#3D7857" stroke-width="2"/><text x="100" y="50" text-anchor="middle" font-size="6" fill="#3D7857">🔒mTLS</text>
    <line x1="160" y1="60" x2="180" y2="75" stroke="#3D7857" stroke-width="2"/>
    <line x1="80" y1="80" x2="100" y2="95" stroke="#3D7857" stroke-width="2"/>
    <line x1="120" y1="100" x2="180" y2="90" stroke="#3D7857" stroke-width="2"/>
  </g>
  <g transform="translate(300,55)"><rect width="160" height="120" rx="6" fill="#3F4A5E"/><text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">CONTROL PLANE</text>
    <rect x="14" y="32" width="132" height="20" rx="2" fill="#FBE8DC"/><text x="20" y="46" font-size="8" fill="#A04832" font-weight="700">Istio (ambient)</text>
    <rect x="14" y="56" width="132" height="20" rx="2" fill="#E0EFE6"/><text x="20" y="70" font-size="8" fill="#3D7857" font-weight="700">Linkerd</text>
    <rect x="14" y="80" width="132" height="20" rx="2" fill="#E0EEF3"/><text x="20" y="94" font-size="8" fill="#3F4A5E" font-weight="700">Cilium Mesh</text>
    <text x="80" y="115" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">policy + cert + xDS</text></g>
  <g transform="translate(480,55)"><rect width="160" height="60" rx="6" fill="#FBF1D6" stroke="#8B5A00" stroke-width="1.5"/><text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">SIDECAR MODE</text><text x="80" y="36" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">envoy per Pod</text><text x="80" y="50" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">+ mem · + mgmt</text></g>
  <g transform="translate(480,125)"><rect width="160" height="60" rx="6" fill="#E0EFE6" stroke="#3D7857" stroke-width="1.5"/><text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#3D7857">AMBIENT MODE</text><text x="80" y="36" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">node-level proxy</text><text x="80" y="50" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">no per-Pod overhead</text></g>
</svg>"""

LESSON = LessonSpec(
    num="43",
    title_short="service mesh",
    title_full="Service Mesh · Istio Ambient, Linkerd, Cilium Mesh",
    title_html="Lesson 43 — Service Mesh · K-COM",
    module_eyebrow="Module 18 · Lesson 43 · the data-plane layer",
    hero_sub_html='A <strong>service mesh</strong> adds mTLS, observability, traffic shaping, and policy at the network layer — without app changes. The 2026 mesh landscape is dominated by <strong>Istio Ambient</strong> (no sidecars), <strong>Linkerd</strong> (smallest, fastest), and <strong>Cilium Service Mesh</strong> (eBPF-native). Each takes a different bet on the architecture.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Compliance asks: \"is every internal service-to-service call encrypted?\" Without mTLS — the answer is no. Adding TLS to every service means: writing TLS code in every language, managing certs per app, rotating per service, fighting mismatched library versions. <em>A service mesh provides mTLS as infrastructure</em>: zero app changes, automatic cert rotation, policy declared centrally. Plus observability and traffic shaping for free. The trade is operational complexity — the mesh itself is now part of your platform.',
    stamp_html='Three meshes worth knowing in 2026: <strong>Istio Ambient</strong> (node-level + waypoint proxies; supersedes the original sidecar architecture), <strong>Linkerd</strong> (purpose-built for K8s; smallest + fastest), <strong>Cilium Service Mesh</strong> (eBPF-native; integrates with the CNI). All provide: mTLS by default, observability (golden signals + traces), traffic shaping (canary, retries, timeouts), policy. <strong>Sidecar vs ambient:</strong> the trend is decisively away from per-Pod sidecars.',
    district_pin="kt-pin17",
    district_label="Switchboard — Service Mesh Wing",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What a mesh adds",
            body_html="""    <p>A service mesh is a <strong>data plane</strong> (proxies in your traffic path) + a <strong>control plane</strong> (policy + cert + config distribution). The mesh:</p>
    <ul>
      <li>Wraps every service-to-service call in <strong>mTLS</strong>. Cert per workload identity (the SPIFFE/SPIRE pattern). Automatic rotation.</li>
      <li>Records <strong>per-call telemetry</strong>: latency, success rate, request size. Aggregated into Prometheus + traces.</li>
      <li>Enforces <strong>traffic policy</strong>: timeouts, retries, circuit breakers, traffic splits, header-based routing.</li>
      <li>Enforces <strong>authz policy</strong>: \"service X can call service Y\\\'s GET endpoint but not POST.\"</li>
    </ul>
    <p>All of this without app changes. The proxy intercepts traffic; the app uses HTTP/gRPC normally. The mesh adds the security + observability layer.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Sidecar vs ambient",
            h2="The architectural shift of 2024-26",
            body_html="""    <p>Original mesh design (Istio classic, Linkerd 1, all early meshes): <strong>sidecar</strong> proxy. Inject an Envoy / linkerd-proxy / similar into every Pod alongside the app container. Every Pod\'s traffic goes through its sidecar.</p>
    <p>Sidecar pros: per-Pod isolation; works regardless of node configuration. Sidecar cons: 100-500MB extra memory per Pod, 0.5-1 vCPU per Pod, complex Pod startup ordering, every restart is a sidecar restart.</p>
    <p><strong>Ambient mode</strong> (Istio 1.22+ Ambient GA, similar in Cilium): no sidecars. Instead:</p>
    <ul>
      <li>L4 traffic (mTLS, basic policy) handled by a <strong>node-level proxy</strong> (zone, like a CNI agent). One per node.</li>
      <li>L7 features (HTTP/gRPC routing, retries, etc.) handled by <strong>waypoint proxies</strong> — Pods deployed selectively for namespaces/services that need them.</li>
    </ul>
    <p>Ambient pros: dramatically less overhead (no sidecar per Pod), simpler Pod lifecycle, opt-in L7 (don\'t pay for it where you don\'t need it). Ambient cons: less per-Pod isolation, newer, fewer integrations.</p>
    <p>By 2026, ambient mode is the recommended default for new Istio installs. Linkerd hasn\'t adopted ambient (their sidecar is so small that the trade-off doesn\'t apply). Cilium\'s mesh is naturally node-level via eBPF.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · The three main meshes",
            h2="Istio Ambient, Linkerd, Cilium Service Mesh",
            body_html="""    <p><strong>Istio Ambient</strong>: most feature-rich. Full HTTP/2 + gRPC support. Strong VirtualService / DestinationRule / AuthorizationPolicy CRDs. Wide ecosystem. Best when you need rich traffic-shaping + policy and you have ops headcount to operate it.</p>
    <p><strong>Linkerd</strong>: smallest + fastest mesh. Sidecars are tiny (Rust). Simplicity over flexibility. Best when you want mTLS + golden signals + simple policy with minimal operational overhead.</p>
    <p><strong>Cilium Service Mesh</strong>: integrates with Cilium CNI (Lesson 24). eBPF data plane; no extra proxy in many cases. Best when you\'re already running Cilium for networking and want to add mesh capabilities.</p>
    <p>2026 trade-off matrix:</p>
    <table class="data-table">
      <thead><tr><th></th><th>Istio Ambient</th><th>Linkerd</th><th>Cilium</th></tr></thead>
      <tbody>
        <tr><td>Setup complexity</td><td>High</td><td>Low</td><td>Low (if Cilium already deployed)</td></tr>
        <tr><td>Per-Pod overhead</td><td>~0 (ambient)</td><td>~50MB sidecar</td><td>~0 (eBPF)</td></tr>
        <tr><td>Traffic-shaping richness</td><td>High</td><td>Medium</td><td>Medium-High</td></tr>
        <tr><td>mTLS</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
        <tr><td>Multi-cluster</td><td>Strong</td><td>Strong</td><td>Strong</td></tr>
      </tbody>
    </table>""",
        ),
        Section(
            eyebrow="Section 1.9 · When to (and not to) adopt a mesh",
            h2="Cost-benefit",
            body_html="""    <p>A mesh adds operational complexity. Worth it when:</p>
    <ul>
      <li><strong>Compliance demands mTLS</strong> for service-to-service traffic. Most regulated industries.</li>
      <li><strong>You have many services</strong> (50+) where per-app TLS would mean N independent implementations.</li>
      <li><strong>You need traffic-shaping</strong> (canary, retries, circuit-breaking) and don\'t want to build into apps. Lesson 40\'s progressive delivery often pairs with mesh.</li>
      <li><strong>You need richer observability</strong> than what app-level instrumentation provides — per-flow telemetry without changing apps.</li>
    </ul>
    <p>Skip when:</p>
    <ul>
      <li>You have ≤10 services. Mesh overhead exceeds value.</li>
      <li>You have one cluster, no compliance pressure, and existing observability/TLS via OTel + cert-manager + your CI signing chain.</li>
      <li>Your team can\'t commit to operating an additional control plane.</li>
    </ul>
    <p>The 2026 trend: <strong>most mid-to-large orgs run a mesh</strong>; <strong>most small startups don\'t</strong>. The threshold is somewhere around 30 services + 1 platform-engineering team that can own the mesh.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The Gateway API + Service Mesh interface (mesh-aware gateways) is converging in 2026. Both Istio and Linkerd are increasingly using Gateway API as their north-south Gateway interface. Long term, the boundary between \"ingress controller\" and \"mesh\" is blurring; Gateway API + mesh is becoming one continuous traffic-management layer.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team has 8 microservices. They\'re considering a service mesh because they want mTLS. Worth the operational cost?",
            options=[
                ("a) Yes, definitely — meshes are always worth it", False),
                ("b) Probably not — at 8 services, cert-manager + workload identity + OTel for observability is simpler. Wait until 30+ services or compliance pressure.", True),
                ("c) Yes, install Istio and put every Pod in mesh", False),
            ],
            feedback="<strong>Answer: b.</strong> A mesh\'s value scales with service count + compliance need. At 8 services, simpler primitives (cert-manager, OTel SDK, NetworkPolicy) cover most of what a mesh provides at lower operational cost. Revisit when service count grows or regulators enter the picture.",
        ),
    },
    before_after_before='<p>Pre-mesh: TLS implementation in every app. Different libraries, different rotation patterns, plaintext between services in 30% of apps because \"we\'ll add TLS later.\" Observability requires manual instrumentation per app. Traffic shaping (canary, retries) baked into application code, different per language.</p>',
    before_after_after='<p>Mesh: mTLS everywhere by default. Cert rotation invisible. Per-flow observability without app changes. Traffic-shaping declared in CRDs (VirtualService, AuthorizationPolicy). Adopted with sidecar costs (overhead) or ambient (no sidecars).</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">The mesh debate of 2025-26 was \"is the operational cost worth it?\" Ambient mode tipped many \"no\" votes to \"yes\" by removing the per-Pod overhead.</p>',
    analogy_intro_html='<p>The Switchboard\'s mesh wing handles all the calls inside a building. A central control board (control plane) issues every phone (workload) a unique ID and a sealed line (mTLS). Two architectures. The <strong>old way</strong>: each phone has its own little operator next to it (sidecar). The <strong>new way</strong>: each floor has one operator (node-level proxy) handling all the floor\'s phones, and certain busy departments get a dedicated line operator (waypoint proxy) for advanced features like retry-on-busy or traffic-split. The control board ensures every call is encrypted, logged, and routed by city policy.</p>',
    translation_rows=[
        ("Phone with its own operator", "Sidecar mesh (Istio classic, Linkerd)"),
        ("Floor-level operator (one per floor)", "Node-level proxy (Istio Ambient ztunnel, Cilium eBPF)"),
        ("Dedicated department line operator", "Waypoint proxy (Istio Ambient L7)"),
        ("Sealed line (encrypted call)", "mTLS"),
        ("Central control board", "Mesh control plane"),
        ("\"Department X can call Y but not Z\"", "AuthorizationPolicy"),
        ("\"On busy, retry up to 3 times\"", "VirtualService retries"),
        ("\"Send 10% to canary line\"", "VirtualService traffic split"),
        ("Per-call audit log", "Mesh-emitted telemetry"),
    ],
    analogy_stops="The analogy stops here: real meshes do millions of decisions per second via Envoy or eBPF, not human operators. mTLS is cryptographic key exchange + certificate validation per connection, not a sealed line.",
    eli5='Every phone in the building has a special line that nobody else can listen to. There\'s a central console that knows who can call whom.',
    eli10="Service mesh = data plane (proxies) + control plane. mTLS by default, per-flow observability, traffic shaping, authz policy — all without app changes. Sidecar mode (proxy per Pod) is the original; ambient mode (node-level + waypoint proxies) reduces overhead. Three main meshes in 2026: Istio Ambient (richest), Linkerd (simplest), Cilium Service Mesh (eBPF-native). Skip if you have &lt;30 services and no compliance pressure.",
    scenarios=[
        Scenario(name="A bank running Linkerd for mTLS-everywhere", body="50 microservices. mTLS required by compliance. Linkerd was chosen for simplicity + small footprint. <60MB per sidecar. Auto-rotation of certs every 24h. mTLS audit logs satisfy regulators. Operational overhead: ~0.5 platform engineer."),
        Scenario(name="A SaaS migrating from Istio sidecar to Ambient", body="Started on Istio classic in 2022. By 2024, sidecar overhead became painful (memory, startup time). Migrated to Ambient mode in 2025: ztunnel DaemonSet + waypoint proxies for HTTPRoute consumers. ~70% reduction in mesh-related Pod resource use. Same Istio CRDs."),
        Scenario(name="A startup using Cilium Service Mesh", body="Cilium was already the CNI. Enabling Cilium Service Mesh added mTLS + observability (Hubble) without adding new proxies. eBPF handles the data plane in-kernel. Lower latency than sidecar meshes. Tradeoff: mesh features evolve with Cilium\'s roadmap."),
        Scenario(name="A team that didn\'t adopt a mesh", body="12 microservices, single region, internal-only. Looked at Istio + Linkerd + Cilium. Decided: cert-manager for app-level TLS, OTel SDK for observability, NetworkPolicy for authz. Total mesh-equivalent cost: 0 platform-engineering hours. Re-evaluate at 30+ services."),
    ],
    misconceptions=[
        Misconception(myth="A service mesh replaces NetworkPolicy.", truth="They\'re different layers. NetworkPolicy is L3/4 (IP + port). Mesh AuthorizationPolicy is L7 (HTTP method + path + headers). Use both: NetworkPolicy as broad allow-list; AuthorizationPolicy for fine-grained service-level rules."),
        Misconception(myth="Sidecar mode is always too expensive.", truth="Linkerd\'s sidecar is so small (~30-50MB) that the trade-off rarely matters. Istio classic\'s sidecar is large (~200-400MB) so ambient was a major win there. Pick the mesh based on your service count + footprint constraints."),
        Misconception(myth="A service mesh is required for mTLS.", truth="Plenty of alternatives: cert-manager + Envoy in your app; SPIRE + workload identity; mTLS via mesh sidecar + native code. Mesh is the easiest path; not the only one."),
    ],
    flashcards=[
        Flashcard(front="What is a service mesh?", back="Data plane (proxies in traffic path) + control plane (policy + cert + config). Adds mTLS, observability, traffic shaping, policy without app changes."),
        Flashcard(front="Sidecar vs ambient mode?", back="Sidecar: proxy per Pod; per-Pod overhead but full isolation. Ambient: node-level proxy for L4 + selective waypoint proxies for L7; less overhead, newer."),
        Flashcard(front="Istio Ambient components?", back="ztunnel (node-level DaemonSet for mTLS + L4); waypoint proxies (Pods, deployed selectively for L7 features); istiod control plane."),
        Flashcard(front="Linkerd architecture?", back="Sidecar-based (Rust proxy, very small). Control plane: identity, destination, policy. Simplest mesh by design."),
        Flashcard(front="Cilium Service Mesh?", back="eBPF-based data plane integrated with Cilium CNI. No extra proxy for many features. Hubble for observability. Best when Cilium is already your CNI."),
        Flashcard(front="What is mTLS in mesh context?", back="Mutual TLS between service-to-service calls. Each workload has a cert tied to its identity (SPIFFE-style). Auto-rotated by control plane."),
        Flashcard(front="VirtualService / AuthorizationPolicy (Istio)?", back="VirtualService: traffic-shaping rules (routing, retries, splits). AuthorizationPolicy: which clients (by identity) can call this service\'s endpoints."),
        Flashcard(front="When to skip a mesh?", back="≤10-30 services, no compliance pressure, observability via OTel SDK works, mTLS via cert-manager works. Mesh overhead exceeds value at small scale."),
    ],
    quizzes=[
        Quiz(prompt="A team enables Istio Ambient on a 200-Pod cluster. After enable, they see 30% of services have higher latency. What\'s the diagnosis?", answer="<strong>Common causes:</strong> (1) <em>Waypoint proxy not deployed</em>. Some services need L7 features (retries, header routing); without a waypoint, the calls fall back to L4 only — features silently inactive but no perf regression there. Latency regression is more often: (2) <em>ztunnel CPU starvation</em>. Node\'s ztunnel pod doesn\'t have enough CPU; queueing builds up. Tune resource requests. (3) <em>Application-level retries on top of mesh retries</em>. Doubled retry storms. Either disable mesh retries or app retries; not both. (4) <em>mTLS handshake on every connection</em>. Long-lived connections amortise; short-lived bursts pay the handshake cost. Tune connection pool sizes. <strong>Diagnostic:</strong> Hubble / Envoy access logs; mesh-side latency vs app-side latency. The latter doesn\'t lie."),
        Quiz(prompt="A team\'s Linkerd dashboard shows their <code>checkout</code> service has 0.5% 5xx but no clear cause in app logs. How to use mesh observability?", answer="<strong>Linkerd\'s</strong> per-flow telemetry shows the call graph + per-call status. <strong>Steps:</strong> (1) <code>linkerd viz tap deploy/checkout</code> — see live request streaming with status codes. (2) Filter for 5xx; look at peer service. The 5xx might originate from a downstream call, not from <code>checkout</code> itself. (3) <code>linkerd viz top deploy/checkout</code> — top routes by error rate. Pinpoint the failing endpoint. (4) Cross-reference with traces (if OTel is wired up). <strong>Without mesh:</strong> you\'d add logs in every service, cross-correlate by request ID, check timestamps. Mesh observability cuts that workflow to seconds."),
        Quiz(prompt="The platform team is choosing between Istio Ambient and Linkerd for a 100-service cluster. <strong>Click for the decision framework. ▼</strong>", cyoa=True, cyoa_tag="the decision framework", answer="<strong>Same considerations as Argo CD vs Flux but with different criteria:</strong> <strong>Pick Linkerd when:</strong> (1) operational simplicity is the top concern. Linkerd has the smallest learning curve. (2) Per-Pod overhead is non-issue (your services are mid-to-large; Linkerd\'s ~50MB doesn\'t matter). (3) You don\'t need rich L7 traffic shaping; mTLS + golden signals + simple authz is enough. <strong>Pick Istio Ambient when:</strong> (1) You need rich L7 traffic shaping (header routing, complex retries, fault injection). (2) You\'re already in the Istio ecosystem (Kiali, etc.). (3) Multi-cluster or virtual-machine workloads. <strong>Pilot:</strong> install both side-by-side on a non-prod cluster; deploy 5-10 representative services to each; compare ops engineer feedback after 2 weeks. <strong>Migration:</strong> mesh migrations are non-trivial (cert / identity / policy reauthoring). Pick once + commit. <strong>Cilium Service Mesh:</strong> the wildcard if you\'re already running Cilium. Lower per-Pod overhead than either; less mature L7 features."),
    ],
    glossary=[
        GlossaryItem(name="Service mesh", definition="Data-plane proxies + control plane providing mTLS, observability, traffic policy."),
        GlossaryItem(name="Sidecar mode", definition="Proxy per Pod. Original mesh architecture."),
        GlossaryItem(name="Ambient mode (Istio)", definition="Node-level proxy (ztunnel) + selective waypoint proxies. No per-Pod sidecar."),
        GlossaryItem(name="ztunnel", definition="Istio Ambient\'s node-level DaemonSet handling mTLS + L4 policy."),
        GlossaryItem(name="Waypoint proxy", definition="Istio Ambient Pod handling L7 features (HTTP routing, retries) for selected namespaces/services."),
        GlossaryItem(name="Linkerd", definition="Lightweight CNCF mesh. Rust sidecar; simpler than Istio."),
        GlossaryItem(name="Cilium Service Mesh", definition="Mesh integrated with Cilium CNI. eBPF data plane."),
        GlossaryItem(name="VirtualService (Istio)", definition="Traffic routing CRD: matches + actions (route, retry, fault inject)."),
        GlossaryItem(name="AuthorizationPolicy (Istio)", definition="L7 authz CRD: \"identity X may call service Y\\\'s endpoint Z.\""),
        GlossaryItem(name="SPIFFE / SPIRE", definition="Standard for workload identity certs. Used by most meshes."),
        GlossaryItem(name="Envoy", definition="High-performance L7 proxy. Underlying data plane for Istio + many gateways."),
        GlossaryItem(name="Linkerd-proxy", definition="Linkerd\'s Rust-based sidecar. Smaller + faster than Envoy for mesh use cases."),
    ],
    recap_lead="Service mesh adds mTLS + observability + traffic policy at the network layer with no app changes. Ambient (Istio) or eBPF (Cilium) reduces overhead vs sidecar. Skip if you have <30 services and no compliance pressure; adopt above that threshold.",
    recap_next="<strong>Next — Lesson 44: Troubleshooting Methodology.</strong> The capstone — methodical investigation under pressure, drills, common failure patterns. New K-Town district: Detective\'s Office.",
)
