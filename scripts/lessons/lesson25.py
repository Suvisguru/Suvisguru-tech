from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Switchboard customer counter: GatewayClass posters on the wall, a Gateway machine with three plugged listeners, and three routes (HTTPRoute, GRPCRoute, TCPRoute) clipped to a route board.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">SWITCHBOARD · CUSTOMER COUNTER (GATEWAY API)</text>
  <!-- GatewayClass poster -->
  <g transform="translate(40,55)">
    <rect width="100" height="100" rx="6" fill="#FFFFFF" stroke="#3F4A5E" stroke-width="1.5"/>
    <text x="50" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">GatewayClass</text>
    <line x1="14" y1="28" x2="86" y2="28" stroke="#9D9389" stroke-width="0.5"/>
    <text x="50" y="44" text-anchor="middle" font-size="8" fill="#5A4F45">controller:</text>
    <text x="50" y="56" text-anchor="middle" font-size="8" font-weight="700" fill="#3F4A5E">envoy-gw</text>
    <text x="50" y="72" text-anchor="middle" font-size="8" fill="#5A4F45">or</text>
    <text x="50" y="84" text-anchor="middle" font-size="8" font-weight="700" fill="#3F4A5E">cilium-gw</text>
    <text x="50" y="120" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">cluster-scoped recipe</text>
  </g>
  <!-- Gateway machine -->
  <g transform="translate(170,40)">
    <rect width="200" height="140" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="100" y="18" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">GATEWAY · listener bank</text>
    <!-- Listeners -->
    <rect x="14" y="28" width="172" height="28" rx="3" fill="#5A9F7A"/>
    <text x="100" y="46" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">:443 HTTPS · *.example.com</text>
    <rect x="14" y="62" width="172" height="28" rx="3" fill="#4A8FA8"/>
    <text x="100" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">:80 HTTP · redirect</text>
    <rect x="14" y="96" width="172" height="28" rx="3" fill="#A04832"/>
    <text x="100" y="114" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">:9090 gRPC · api.internal</text>
    <text x="100" y="135" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">infra team owns this</text>
  </g>
  <!-- Route board -->
  <g transform="translate(400,40)">
    <rect width="240" height="140" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="120" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">ROUTE BOARD · app-team-owned</text>
    <rect x="10" y="22" width="220" height="30" rx="3" fill="#FBF1D6" stroke="#8B5A00" stroke-width="1.2"/>
    <text x="14" y="36" font-size="8" font-weight="700" fill="#8B5A00">HTTPRoute</text>
    <text x="14" y="48" font-size="7" fill="#5A4F45">/api/v1 → svc-api  |  /shop → svc-shop</text>
    <rect x="10" y="58" width="220" height="30" rx="3" fill="#E0EFE6" stroke="#3D7857" stroke-width="1.2"/>
    <text x="14" y="72" font-size="8" font-weight="700" fill="#3D7857">GRPCRoute</text>
    <text x="14" y="84" font-size="7" fill="#5A4F45">api.proto.UserService → svc-users</text>
    <rect x="10" y="94" width="220" height="30" rx="3" fill="#FBE8DC" stroke="#A04832" stroke-width="1.2"/>
    <text x="14" y="108" font-size="8" font-weight="700" fill="#A04832">TCPRoute / TLSRoute</text>
    <text x="14" y="120" font-size="7" fill="#5A4F45">port 6443 → svc-postgres</text>
  </g>
  <text x="340" y="200" text-anchor="middle" font-size="11" fill="#3F4A5E" font-style="italic">GatewayClass = recipe · Gateway = listener bank · Route = traffic clip · Three roles, separate ownership.</text>
</svg>"""

LESSON = LessonSpec(
    num="25",
    title_short="Gateway API",
    title_full="Gateway API · Roles, Listeners, Routes, and the Ingress Sunset",
    title_html="Lesson 25 — Gateway API · K-COM",
    module_eyebrow="Module 12 · Lesson 25 · the Ingress successor",
    hero_sub_html='Ingress was K8s\'s original L7 traffic API — and it stopped scaling years ago. The <strong>Gateway API</strong> (GA in K8s 1.31; v1 stable everywhere by 2026) replaces it with a <strong>three-role, three-object</strong> model that separates infrastructure, gateway, and route concerns. <strong>Ingress NGINX is officially retiring in 2026</strong>; this is the migration target.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Friday morning: announcement drops that Ingress NGINX (kubernetes/ingress-nginx) will stop receiving security patches at end of 2026. The team has 47 production Ingress objects, hand-rolled annotations, and a custom ConfigMap with 200 settings. The migration target is Gateway API + a Gateway-API-conformant controller (Envoy Gateway, Cilium Gateway, etc.). The team panics. They\'ve been ignoring Gateway API for two years. <em>The migration is doable</em> — Ingress NGINX itself ships <code>InGate</code>, a one-shot translator. But the <em>real</em> work is changing the team\'s mental model from "everything in one Ingress YAML" to the new role-separated structure. This lesson is that mental model.',
    stamp_html='Gateway API splits Ingress into three roles: <strong>GatewayClass</strong> (cluster recipe — infra team), <strong>Gateway</strong> (listener bank — platform team), <strong>HTTPRoute / GRPCRoute / TCPRoute / TLSRoute</strong> (traffic clips — app teams). The same logical setup as Ingress, but with cleaner ownership boundaries and far more expressiveness. Ingress NGINX is sunsetting in 2026 — start the migration now.',
    district_pin="kt-pin17",
    district_label="Switchboard — Customer Counter",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why Ingress wasn't enough",
            body_html="""    <p>The Ingress API (in beta from 2015, finally stable in 2020) gave us "expose HTTP routes from outside the cluster." It worked. It also accumulated every limitation of a v1 API: no traffic splitting, no header manipulation, no separate concerns for infra vs apps, no good story for non-HTTP traffic, vendor-specific behavior locked behind <em>annotations</em>. Annotations on an Ingress object became the de-facto extension mechanism — and they're untyped strings that vary per controller.</p>
    <p>The <strong>Gateway API</strong> (Kubernetes SIG-Network, work started in 2019) is the redesign. Not just \"Ingress v2\" — a structurally different model with three explicit roles and CRDs for each:</p>
    <ul>
      <li><strong>Infrastructure provider</strong> — defines a <code>GatewayClass</code>: \"this controller (Envoy Gateway, Cilium Gateway, NGINX Gateway Fabric, Istio gateways) handles Gateways of this class.\"</li>
      <li><strong>Cluster operator</strong> — creates <code>Gateway</code> objects: \"give me a listener on :443 with these TLS certs, accepting routes from these namespaces.\"</li>
      <li><strong>Application developer</strong> — creates <code>HTTPRoute</code> / <code>GRPCRoute</code> / <code>TCPRoute</code> / <code>TLSRoute</code> objects: \"this hostname/path → my Service.\"</li>
    </ul>
    <p>The big change for app teams: you don\'t describe the listener anymore. The platform team owns the Gateway; you just attach a Route to it. The old "every team writes their own Ingress with annotations" pattern is gone.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The three role-objects",
            h2="GatewayClass, Gateway, Route",
            body_html="""    <div class="role-grid">
      <div class="role r1">
        <span class="role-icon">🏛️</span>
        <h3 class="role-name">GatewayClass</h3>
        <p class="role-tag">recipe · cluster-scoped</p>
        <p class="role-desc">Cluster-scoped: \"controller X handles Gateways of class Y.\" Ships with the Gateway controller; cluster operators reference it. Like StorageClass.</p>
        <p class="role-who">Owned by: infrastructure team / Gateway controller install</p>
      </div>
      <div class="role r2">
        <span class="role-icon">🚪</span>
        <h3 class="role-name">Gateway</h3>
        <p class="role-tag">listener bank · namespace-scoped</p>
        <p class="role-desc">A specific gateway with one or more listeners. Each listener is (port, protocol, optionally hostname, TLS config). Specifies which namespaces' Routes can attach via <code>allowedRoutes</code>.</p>
        <p class="role-who">Owned by: platform team</p>
      </div>
      <div class="role r3">
        <span class="role-icon">🛣️</span>
        <h3 class="role-name">HTTPRoute (and friends)</h3>
        <p class="role-tag">traffic clip · namespace-scoped</p>
        <p class="role-desc">"Match these hostnames + paths/headers, route to these backends with these weights." Far richer than Ingress: header matching, traffic splitting, request rewriting, retries, timeouts. GRPCRoute, TCPRoute, TLSRoute, UDPRoute exist for non-HTTP.</p>
        <p class="role-who">Owned by: app teams</p>
      </div>
    </div>
    <p style="margin-top:18px">A Route attaches to a Gateway via <code>parentRefs</code>. The Gateway's <code>allowedRoutes</code> field gates which namespaces / Route kinds can attach. This is the explicit cross-tenancy model Ingress never had.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · What HTTPRoute can do that Ingress couldn't",
            h2="Out of annotations, into a typed schema",
            body_html="""    <p>Most Ingress controllers had de-facto annotations for traffic splitting (canary), header rewriting, retries. Each controller's syntax differed; cross-controller migration was painful. Gateway API moves all of this into the typed Route schema:</p>
    <ul>
      <li><strong>Traffic splitting:</strong> a single Route can backendRef two Services with weights (90/10 for canary).</li>
      <li><strong>Header / path rewriting:</strong> filters on a route can rewrite request URLs and headers in-flight.</li>
      <li><strong>Request mirroring:</strong> send a copy of every request to a debug Service while the real one is unaffected.</li>
      <li><strong>Retries / timeouts:</strong> declarative per-route, no controller-specific annotations.</li>
      <li><strong>Method matching:</strong> match by HTTP method (GET/POST), not just path/host.</li>
      <li><strong>RBAC-friendly:</strong> apps can have full control of their Routes without ops worrying about port conflicts or TLS.</li>
    </ul>
    <p>Gateway API also has a formal <strong>conformance test suite</strong>. Controllers advertise which features they support. Switching from Envoy Gateway to NGINX Gateway Fabric means re-running conformance and fixing any unsupported features — not rewriting hundreds of annotations.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · The Ingress NGINX retirement",
            h2="What's actually happening in 2026",
            body_html="""    <p>The community-maintained <code>kubernetes/ingress-nginx</code> project (the de-facto Ingress controller for years) announced in March 2025 it would stop accepting new features and would EOL security patches by end of 2026. Reasons cited: limited contributor capacity, fundamental architectural debt (NGINX as a templated config), and the existence of a clearer successor (NGINX Gateway Fabric, F5\'s officially-supported Gateway-API-conformant controller).</p>
    <p>The migration story:</p>
    <ul>
      <li><strong>Tool: <code>InGate</code></strong> — Ingress NGINX\'s own translator that converts existing Ingress YAML to Gateway API objects. Not perfect but covers ~80% of typical setups.</li>
      <li><strong>Strategy:</strong> install a Gateway-API-conformant controller alongside Ingress NGINX (Envoy Gateway, NGINX Gateway Fabric, Cilium Gateway, Istio); migrate Routes incrementally with DNS cut-over per app; decommission Ingress NGINX last.</li>
      <li><strong>Don\'t panic deadline:</strong> Ingress objects still work in K8s — just unmaintained Ingress controllers won\'t receive CVEs. You have through 2026 to migrate at sane pace.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The political subtext: Ingress NGINX was always community-maintained without F5\'s direct backing. NGINX Gateway Fabric is F5-supported and Gateway-API-native — it\'s the supported successor. Other vendors saw the gap and moved their Gateway implementations earlier (Envoy Gateway, Cilium Gateway, Istio Gateway). The Gateway API itself is vendor-neutral; the choice of controller is yours. Most new clusters in 2026 are choosing Envoy Gateway or Cilium Gateway.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A platform team owns a Gateway listening on :443. App-team-A wants to attach an HTTPRoute matching <code>app-a.example.com</code>; app-team-B wants <code>app-b.example.com</code>. Both are in different namespaces. What does the platform team configure on the Gateway?",
            options=[
                ("a) Nothing — Routes can attach freely from any namespace by default", False),
                ("b) Set <code>allowedRoutes.namespaces.from: All</code> (or a selector) on the Gateway's listener so cross-namespace Routes can attach", True),
                ("c) Create one Gateway per namespace", False),
            ],
            feedback="<strong>Answer: b.</strong> By default a Gateway's listener only accepts Routes from its own namespace (<code>from: Same</code>). To enable cross-namespace attachment, set <code>allowedRoutes.namespaces.from: All</code> or use a label selector. This is the explicit cross-tenancy model — much clearer than Ingress's free-for-all.",
        ),
    },
    before_after_before='<p>Old way: every team writes an <code>Ingress</code> with the controller\'s annotations (<code>nginx.ingress.kubernetes.io/...</code>) for canary splits, rewrites, retries. Cross-controller migration = rewrite every Ingress. Tenancy via namespace + RBAC luck. Listener config baked into Ingress objects so app teams accidentally control TLS.</p>',
    before_after_after='<p>Gateway API: platform team owns Gateway (listeners, TLS, allowedRoutes). App teams own HTTPRoutes with first-class fields for splits/rewrites/retries. Switching controllers = rerun conformance. Tenancy explicit via <code>allowedRoutes</code>. Same listener serves many apps without a single shared annotation soup.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Gateway API was the most-discussed K8s API of 2024-25 for good reason. It\'s the cleanest single API redesign in the ecosystem\'s history.</p>',
    analogy_intro_html='<p>Switchboard, customer counter side. The old setup had every business carrying a single big poster with their phone number, address, who could call them, what hours they answered, and the rules for caller ID — all stuck on one wall, written by anyone, contradicting each other. <em>Ingress, with its annotations, on a wall.</em></p><p>The new layout has three separate workstations. The infra office hangs <strong>operating-license posters</strong> (GatewayClass): "the city contracts so-and-so for this kind of switchboard." The platform team operates the <strong>main switchboard machine</strong> (Gateway): a bank of physical jacks at specific addresses (listeners), each jack with its own line and posted rules about who can plug in. App teams clip their own <strong>route slips</strong> (HTTPRoute) onto a board: "calls to this number, from this exchange, route to my building, here are the rules for split-percentage and retry." Three roles, three artefacts, no overlap.</p>',
    translation_rows=[
        ("Operating-license poster", "<code>GatewayClass</code>"),
        ("The switchboard machine and its bank of jacks", "<code>Gateway</code> with listeners (port, protocol, hostname, TLS)"),
        ("Posted rules for which exchanges may plug into a jack", "<code>allowedRoutes</code> on a listener"),
        ("Clipped route slip on the board", "<code>HTTPRoute</code> (and GRPCRoute, TCPRoute, TLSRoute, UDPRoute)"),
        ("Split-percentage rules on a slip", "Backend weights for canary / blue-green"),
        ("In-flight call edits (rewrite extension)", "Filters: URLRewrite, HeaderModifier"),
        ("The annotation soup on the old single poster", "Ingress + controller-specific annotations"),
        ("\"This switchboard contractor is shutting down\" notice", "Ingress NGINX EOL end of 2026"),
    ],
    analogy_stops="The analogy stops here: real Gateway implementations are programs (Envoy Gateway, Cilium Gateway), not switchboards. And the \"three roles\" are an organisational ideal — small teams may collapse them, and that\'s fine; the API just makes the boundaries possible.",
    eli5='Old way: one big sign for each store, with everything on it, half of it in code only the sign-maker understood. New way: a city sign for the road type, a building manager for the front-desk hours, and each store keeps a small slip on a shared board for "if someone asks for me, send them in."',
    eli10="The Gateway API replaces the Ingress API. Three CRDs split the concerns: GatewayClass (cluster-level recipe; infra team), Gateway (listener bank; platform team), HTTPRoute / GRPCRoute / TCPRoute / TLSRoute (traffic rules; app teams). Routes attach to Gateways via <code>parentRefs</code>; Gateways gate cross-namespace attachment via <code>allowedRoutes</code>. First-class support for traffic splitting, header rewriting, mirroring, retries, timeouts — all the things that used to be controller-specific annotations on Ingress. Ingress NGINX is EOL end of 2026; the upgrade path is Gateway API + Envoy Gateway / Cilium Gateway / NGINX Gateway Fabric.",
    scenarios=[
        Scenario(name="A SaaS replacing 47 Ingress objects with Gateway API", body="One Gateway per cluster (managed by platform team), Routes per app team. Started with the InGate translator for the bulk migration; hand-fixed the 12 with custom annotations. Total migration: 6 weeks, including testing. End state: app teams own their HTTPRoutes, no platform-team approval needed for new routes."),
        Scenario(name="A bank using Cilium Gateway", body="Cilium provides both CNI and Gateway in the same DaemonSet. Single eBPF-based data plane for cluster-internal traffic and ingress. Hubble shows per-flow visibility from external request through Routes to backend Pods. Operations team has one fewer thing to deploy."),
        Scenario(name="A startup running Envoy Gateway for richer traffic shaping", body="Used HTTPRoute weighted backends for canary deploys: 90% to <code>v1</code>, 10% to <code>v2</code>. Increment to 50/50, then 0/100 over a week. Pushed via GitOps; no controller annotations. Same flow gets metrics/tracing in Envoy admin endpoint."),
        Scenario(name="A team that mirrors prod traffic to staging", body="HTTPRoute filter <code>RequestMirror</code> sends a copy of every prod request to the staging Service. Staging gets real prod traffic shape without affecting prod responses. Used to validate the next release before promoting it."),
    ],
    misconceptions=[
        Misconception(myth="Gateway API is just Ingress with new YAML.", truth="It\'s a structural redesign with explicit role separation, first-class non-HTTP routes, conformance testing, and typed traffic-shaping fields. Migrating means reorganising who owns what, not just rewriting Ingress."),
        Misconception(myth="You have to migrate to Gateway API before end of 2026.", truth="Ingress objects still work — what\'s EOL is the <em>kubernetes/ingress-nginx</em> controller specifically. Other Ingress controllers (NGINX Inc, Traefik, HAProxy, etc.) keep working. But the entire ecosystem is moving to Gateway API; do the migration on your terms before it becomes urgent."),
        Misconception(myth="Gateway API can\'t do everything Ingress NGINX did.", truth="Conformance varies by controller. Most popular Gateway controllers cover the standard feature set; vendor-specific extensions (Lua scripts, ModSecurity rules) need vendor-specific extensions. Check your specific Gateway controller\'s feature matrix."),
    ],
    flashcards=[
        Flashcard(front="Three Gateway API roles?", back="GatewayClass (cluster, infra-team-owned, recipe). Gateway (namespace, platform-team-owned, listener bank). Route (namespace, app-team-owned, traffic clip). Roles map to organisational responsibility; small teams may collapse them."),
        Flashcard(front="What's a listener?", back="A (port, protocol, optional hostname, optional TLS) tuple on a Gateway. Each listener has its own <code>allowedRoutes</code> rules about which Routes from which namespaces can attach."),
        Flashcard(front="HTTPRoute vs GRPCRoute vs TCPRoute vs TLSRoute?", back="HTTPRoute = full HTTP/2 features. GRPCRoute = gRPC-aware (method matching). TCPRoute = raw TCP backend selection. TLSRoute = SNI-based routing for TLS without termination."),
        Flashcard(front="parentRefs?", back="Field on a Route specifying which Gateway(s) it attaches to. Cross-namespace by name + namespace; allowed only if the Gateway listener's <code>allowedRoutes</code> permits."),
        Flashcard(front="Traffic splitting in HTTPRoute?", back="Multiple backendRefs in a rule with weights. <code>weight: 90</code> on backend A and <code>weight: 10</code> on backend B = 90/10 split. Canary in pure declarative YAML."),
        Flashcard(front="Common Gateway controllers?", back="Envoy Gateway, NGINX Gateway Fabric (F5-supported), Cilium Gateway, Istio Gateways, Traefik, HAProxy Kubernetes Ingress (now Gateway-capable), Kong Gateway, Solo gloo. Pick by org familiarity + conformance level."),
        Flashcard(front="What is conformance?", back="Formal test suite the Gateway API project ships. Controllers run conformance and publish their support level (Core / Extended / Implementation-specific). Lets you switch controllers with confidence."),
        Flashcard(front="When does Ingress NGINX EOL?", back="End of 2026 — kubernetes/ingress-nginx specifically (not NGINX Inc.'s commercial NGINX or any other Ingress controller). Migrate to Gateway API + a conformant controller."),
    ],
    quizzes=[
        Quiz(prompt="A team has a single Ingress with 28 hosts on it (NGINX annotations for split, retry, headers). They start a Gateway API migration. What's the right first step?", answer="Don\'t convert all 28 at once. <strong>(1)</strong> Install a Gateway controller alongside Ingress NGINX (Envoy Gateway is a common choice). <strong>(2)</strong> Create a single Gateway with listeners matching the existing Ingress's TLS setup. <strong>(3)</strong> Pick one host (the lowest-stakes one), create an HTTPRoute, switch DNS for that host. Validate. <strong>(4)</strong> Repeat for the next host. <strong>(5)</strong> When all 28 hosts are on the Gateway, decommission the old Ingress. Tools like InGate help with the bulk YAML transformation; the careful per-host cutover is the safe migration sequence."),
        Quiz(prompt="The Gateway API has GRPCRoute, TCPRoute, TLSRoute, UDPRoute. When would you pick TLSRoute over HTTPRoute?", answer="TLSRoute does <em>SNI-based routing without TLS termination</em>. Use case: a Pod-managed service that wants to handle its own TLS internally (e.g., a database with mTLS, a service mesh proxy) — but you still want to use the cluster's external Gateway as a passthrough load balancer. The Gateway looks at the Server Name Indication (SNI) field in the TLS handshake to pick a backend, then passes the bytes through. HTTPRoute would terminate TLS, see the HTTP requests, and re-encrypt to the backend if needed. TLSRoute = no termination. TCPRoute = no SNI inspection at all, just a flat L4 proxy."),
        Quiz(prompt="The platform team installs Cilium Gateway in production but app teams keep getting 503s on cross-namespace HTTPRoutes. <strong>Click for the diagnosis. ▼</strong>", cyoa=True, cyoa_tag="the diagnosis", answer="The most common cause: the Gateway's listeners specify <code>allowedRoutes.namespaces.from: Same</code> (the default), so Routes in other namespaces are silently rejected. <strong>Diagnosis steps:</strong> (1) <code>kubectl get httproute -A</code> — for each, check <code>status.parents.conditions</code>. Routes that didn't attach show <code>Accepted=False</code> with reason <code>NotAllowedByListeners</code>. (2) <code>kubectl get gateway</code> — inspect the listeners' <code>allowedRoutes</code>. <strong>Fix:</strong> set <code>allowedRoutes.namespaces.from: All</code> (loose) or <code>Selector</code> with a namespace label match (tighter). Once the Route attaches, traffic flows. <strong>Why this is a feature, not a bug:</strong> the explicit attach model prevents app-team A from accidentally claiming app-team B\'s hostname — which used to happen all the time with Ingress."),
    ],
    glossary=[
        GlossaryItem(name="Gateway API", definition="K8s SIG-Network successor to Ingress. v1 stable in K8s 1.31; broadly conformant in 2026."),
        GlossaryItem(name="GatewayClass", definition="Cluster-scoped recipe linking a controller to Gateway implementations. Like StorageClass."),
        GlossaryItem(name="Gateway", definition="Namespace-scoped object representing a specific gateway with listeners. Owned by platform team."),
        GlossaryItem(name="Listener", definition="A (port, protocol, hostname, TLS) tuple on a Gateway. Has its own allowedRoutes."),
        GlossaryItem(name="HTTPRoute", definition="App-team-owned object: match HTTP requests on host/path/headers/method, route to backends with weights, apply filters."),
        GlossaryItem(name="GRPCRoute", definition="gRPC-method-aware route. Backends are gRPC services; matching by RPC."),
        GlossaryItem(name="TCPRoute / TLSRoute / UDPRoute", definition="Layer-4 routing CRDs. TLSRoute does SNI passthrough; TCPRoute is flat L4."),
        GlossaryItem(name="parentRefs", definition="Field on Routes pointing at the Gateway(s) they attach to."),
        GlossaryItem(name="allowedRoutes", definition="Field on a listener gating which namespaces / Route kinds can attach."),
        GlossaryItem(name="Conformance", definition="Formal test suite verifying a controller implements Gateway API correctly. Levels: Core, Extended, Implementation-specific."),
        GlossaryItem(name="InGate", definition="Ingress NGINX's own Ingress→Gateway-API translator tool. Bulk-converts existing setups."),
        GlossaryItem(name="Ingress NGINX EOL", definition="The kubernetes/ingress-nginx project stops receiving security patches end of 2026. Migrate to Gateway API."),
    ],
    recap_lead="Three roles, three CRDs: GatewayClass (cluster recipe), Gateway (listener bank), HTTPRoute/etc (app-team traffic clips). Cleaner ownership, first-class traffic shaping, conformance testing, non-HTTP support. Ingress NGINX EOL'd end of 2026 — start the migration.",
    recap_next="<strong>Next — Lesson 26: AdminNetworkPolicy & FQDN policies.</strong> NetworkPolicy v1 was app-team-controlled and additive-only — there was no \"admin override.\" The new <code>AdminNetworkPolicy</code> + <code>BaselineAdminNetworkPolicy</code> APIs give cluster admins enforceable network rules, plus FQDN-based policies for egress to external services. Switchboard, security wing.",
)
