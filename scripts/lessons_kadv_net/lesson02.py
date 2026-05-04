"""K-ADV-NET N2 — Gateway API at fleet scale."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Gateway API — GatewayClass / Gateway / HTTPRoute hierarchy.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Main Intersection · K-Highway — three roles, one routing chain</text>
  <rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">GatewayClass</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">infra (city operator)</text>
  <text x="125" y="128" text-anchor="middle" font-size="9" fill="#FBF1D6">Envoy Gateway / Istio /</text>
  <text x="125" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">Cilium / NGINX</text>
  <rect x="225" y="70" width="170" height="100" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Gateway</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">listener bank</text>
  <text x="310" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">port + protocol + cert</text>
  <text x="310" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">cluster-/team-shared</text>
  <rect x="410" y="70" width="170" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">HTTPRoute</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">match + filter + backend</text>
  <text x="495" y="124" text-anchor="middle" font-size="9" fill="#1F2433">app-team-owned</text>
  <text x="495" y="144" text-anchor="middle" font-size="9" fill="#1F2433">cross-ns via ReferenceGrant</text>
  <rect x="595" y="70" width="125" height="100" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Service / Pod</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#1F2433">backend</text>
  <text x="657" y="124" text-anchor="middle" font-size="9" fill="#1F2433">+ BackendTLSPolicy</text>
</svg>"""


LESSON = LessonSpec(
    num="02",
    title_short="Gateway API",
    title_full="N2 · Gateway API at Fleet Scale",
    title_html="K-ADV-NET N2 · Gateway API",
    module_eyebrow="Module N2 · Main Intersection — three roles, one routing chain",
    hero_sub_html='<strong>Gateway API</strong> replaces Ingress with a richer + role-separated model. Three roles: <strong>GatewayClass</strong> (infrastructure provider, e.g., Envoy Gateway), <strong>Gateway</strong> (cluster / shared listener bank with cert + hostnames), <strong>HTTPRoute / GRPCRoute / TCPRoute / TLSRoute / UDPRoute</strong> (per-team routing with match + filter + backend). At fleet scale: <strong>cross-namespace</strong> via ReferenceGrant; <strong>BackendTLSPolicy</strong> for backend re-encrypt; <strong>HTTPRouteFilter</strong> for header / URL rewrite; <strong>multi-cluster Gateway</strong> for fleet-wide ingress.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. The Ingress controller hit a regex bug; one team\'s annotation broke routing for every other team. <em>Ingress concentrated all routing config into one shared object</em>. Today\'s lesson: Gateway API\'s role separation prevents this — infrastructure owns the Gateway, app teams own their HTTPRoutes.",
    stamp_html="<strong>Gateway API: GatewayClass (infra) + Gateway (shared listener bank) + HTTPRoute (per-team). ReferenceGrant for cross-namespace; BackendTLSPolicy for re-encrypt. Replaces Ingress + per-controller annotations.</strong>",
    district_pin="knet-junction02",
    district_label="Main Intersection",
    sections=[
        Section(
            eyebrow="Section 1.1 · the three roles",
            h2="GatewayClass · Gateway · HTTPRoute",
            body_html="""    <p><strong>GatewayClass</strong>: cluster-scoped CRD naming the controller (e.g., <code>envoy-gateway</code>) + parameters. Set up by infra team once. Defines who is implementing Gateways in this cluster.</p>
    <p><strong>Gateway</strong>: namespaced; lists listeners (port + protocol + hostname + TLS cert + allowed routes); references a GatewayClass. Typically owned by infra / platform team and shared across multiple app teams.</p>
    <p><strong>HTTPRoute / GRPCRoute / TCPRoute / TLSRoute / UDPRoute</strong>: namespaced; attaches to one or more Gateways via <code>parentRefs</code>; declares match (host + path + headers + method) + filters (header rewrite, redirect, mirror) + backendRefs (Service / Pod). Owned by app teams.</p>
    <p>Role separation is the win: infra controls cert + hostname + TLS termination once; app teams ship routes without touching infra.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · cross-namespace + ReferenceGrant",
            h2="Routes in one namespace pointing at backends in another",
            body_html="""    <p>By default, an HTTPRoute can only reference backendRefs in the <em>same namespace</em>. To route across namespaces: <strong>ReferenceGrant</strong> in the <em>backend\'s</em> namespace explicitly grants the source namespace permission to reference the backend.</p>
    <p>Pattern: Gateway lives in <code>infra</code> namespace; HTTPRoutes in <code>team-X</code> namespaces; backends often in <code>team-X</code> namespace too (no grant needed). Cross-team backends (e.g., a shared identity Service) require ReferenceGrant in the backend namespace.</p>
    <p>This prevents an attacker who controls one namespace from creating routes that hijack traffic to another namespace\'s backends — without explicit cross-namespace consent, the route fails to attach.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · BackendTLSPolicy + filters",
            h2="re-encrypt to backend + header/URL rewrites",
            body_html="""    <p><strong>BackendTLSPolicy</strong> (alpha → beta in newer K8s): tells Gateway to re-encrypt traffic to backends. Default is plain HTTP from Gateway to backend; BackendTLSPolicy switches to HTTPS with caBundle reference. Useful for Pods running TLS terminators or for compliance-required end-to-end encryption.</p>
    <p><strong>HTTPRouteFilter</strong> kinds: <em>RequestHeaderModifier</em> (add/set/remove header); <em>ResponseHeaderModifier</em>; <em>RequestRedirect</em> (HTTP → HTTPS, /old → /new); <em>URLRewrite</em> (path strip / replace); <em>RequestMirror</em> (mirror to another Service for shadow testing); <em>ExtensionRef</em> (controller-specific filters).</p>
    <p>Compared to Ingress\'s annotation-soup, filters are typed CRDs — versioned, schema-validated, controller-portable.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · multi-cluster Gateway + Ingress migration",
            h2="fleet-wide ingress + the path from Ingress",
            body_html="""    <p><strong>Multi-cluster Gateway</strong>: Gateway-api-extensions handle multi-cluster patterns. Cilium ClusterMesh + Gateway, Istio multi-cluster Gateway, GKE Multi-cluster Gateway. Single hostname routes to backends in multiple clusters per region; failover automatic.</p>
    <p><strong>Ingress migration</strong>: per controller, migrate gradually. (1) Pick GatewayClass (often the same controller behind a different CRD). (2) Create Gateway with the same listeners as the existing Ingress. (3) Per Ingress, create equivalent HTTPRoute; switch traffic. (4) Decommission Ingress. Tools: <strong>ingress2gateway</strong> CLI converts manifests automatically.</p>
    <p><strong>Controller choice</strong>: <em>Envoy Gateway</em> (cleanest implementation, CNCF), <em>Istio</em> (full mesh + Gateway), <em>Cilium Gateway</em> (eBPF-native, integrates with Cilium NetPol), <em>NGINX Gateway Fabric</em> (familiar to NGINX teams), <em>cloud-native</em> (GKE Gateway Controller, AKS Application Gateway Controller, AWS Gateway API Controller). All implement the same spec.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="Why does Gateway API separate Gateway from HTTPRoute?",
            options=[
                ("Performance.", False),
                ("Role separation: infra owns Gateway (cert + listener); app teams own HTTPRoute (their routes).", True),
                ("Required by K8s.", False),
            ],
            feedback="The role separation lets infra control TLS + hostname + cert without becoming a bottleneck for every app-team route change. App teams ship routes without infra intervention.",
        ),
        3: PauseCheck(
            question="How do you migrate an existing Ingress fleet to Gateway API?",
            options=[
                ("Big-bang switch — flip everything at once.", False),
                ("Use ingress2gateway CLI; deploy Gateway alongside Ingress; migrate route-by-route.", True),
                ("Wait for Ingress to be deleted from K8s.", False),
            ],
            feedback="Ingress and Gateway API can coexist. Migration is per-controller + per-route; tools like ingress2gateway handle the manifest conversion.",
        ),
    },
    before_after_before='<p>Pre-Gateway API: Ingress + per-controller annotations (NGINX-style, ALB-style, GCE-style). Annotation soup; portability gaps; one controller bug affected every team\'s routes; cross-namespace Service reference impossible.</p>',
    before_after_after='<p>Gateway API: typed CRDs; role separation; ReferenceGrant explicit cross-namespace; BackendTLSPolicy + HTTPRouteFilter as schema-validated objects; portable across controllers (Envoy Gateway, Istio, Cilium, NGINX, cloud-native). Annotation chaos replaced by typed config.</p>',
    before_after_caption='<p class="ba-caption"><em>Three roles, three CRDs, one routing chain. Replaces a decade of Ingress annotation drift.</em></p>',
    analogy_intro_html='''<p>The Main Intersection in K-Highway has three layers of authority. The <strong>city operator</strong> (GatewayClass) builds + maintains the intersection itself; chooses asphalt + signals + traffic-engineering vendor. The <strong>traffic-control engineer</strong> (Gateway) decides which lanes are open at this intersection — the cert, the hostname, the protocol. Each <strong>destination dispatcher</strong> (HTTPRoute) says \"vehicles for my building, take exit 4 + reroute via path X.\"</p>
    <p>The three roles never overlap. The city operator doesn\'t care about your destination. The destination dispatcher doesn\'t change the asphalt. When you need to send vehicles across district lines (cross-namespace), the destination district issues a permit slip (ReferenceGrant) saying \"yes, deliveries from your district may end here.\"</p>''',
    translation_rows=[
        ("City operator", "GatewayClass (controller infrastructure)"),
        ("Traffic-control engineer", "Gateway (listener bank, cert, hostname)"),
        ("Destination dispatcher", "HTTPRoute / GRPCRoute / TLSRoute / TCPRoute"),
        ("Cross-district permit slip", "ReferenceGrant (cross-namespace consent)"),
        ("Vehicle armoring at exit", "BackendTLSPolicy (re-encrypt to backend)"),
        ("Lane filters", "HTTPRouteFilter (header / URL rewrite / redirect / mirror)"),
        ("Fleet of intersections", "Multi-cluster Gateway"),
        ("Old single-board annotations", "Ingress + per-controller annotations (legacy)"),
    ],
    analogy_stops="A real intersection has fixed pavement; Gateway API is virtual — controllers can have bugs, conformance gaps, version skew. Always test with the conformance suite.",
    eli5="Three different people manage one intersection. The city builder makes the road. The traffic engineer decides which lights are on. Each store puts up its own \"go this way for my deliveries\" sign. Each does their job; nobody steps on the others.",
    eli10="<strong>GatewayClass</strong> = controller (Envoy Gateway / Istio / Cilium / NGINX / cloud-native). <strong>Gateway</strong> = cluster/team listener bank (port + protocol + cert + hostnames + allowed routes). <strong>HTTPRoute</strong> (and GRPCRoute / TCPRoute / TLSRoute / UDPRoute) = per-team match + filter + backend ref. <strong>ReferenceGrant</strong> = cross-namespace consent. <strong>BackendTLSPolicy</strong> = re-encrypt to backend. <strong>HTTPRouteFilter</strong> = typed header / URL / redirect / mirror.",
    scenarios=[
        Scenario(
            name="Multi-team cluster — single Gateway, many HTTPRoutes",
            body="A 60-engineer org deploys one Gateway in <code>infra</code> namespace handling api.example.com. Each app team\'s namespace has HTTPRoutes attaching to that Gateway with their hostname / path. Infra owns cert; teams ship routes. Zero coordination required for route changes.",
        ),
        Scenario(
            name="ingress2gateway migration",
            body="A team had 80 Ingress objects across 30 namespaces. Used <code>ingress2gateway</code> CLI to convert; reviewed deltas; deployed Gateway + HTTPRoutes alongside Ingress; switched DNS / traffic; decommissioned Ingress over 4 weeks. Migration low-drama.",
        ),
        Scenario(
            name="Multi-cluster Gateway via Cilium ClusterMesh",
            body="A team needs api.example.com to fail over from us-east-1 cluster to eu-west-1 cluster automatically. Cilium ClusterMesh + Gateway API: HTTPRoute backendRef points at a multi-cluster Service; Cilium routes per-region with health-aware failover. Same DNS; transparent failover.",
        ),
        Scenario(
            name="Outage — annotation typo took down 3 teams",
            body="On the legacy Ingress, a single typo in an NGINX annotation broke routing cluster-wide. Postmortem: schema-typed CRDs (Gateway API) prevent silent annotation typos. Migration to Gateway API now scheduled.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Gateway API is just a renamed Ingress.\"",
            truth="Gateway API has role separation (Gateway + Route owners differ), typed CRDs (no annotations), explicit cross-namespace consent (ReferenceGrant), portable controllers, and broader L4 protocol support (TCPRoute / TLSRoute / UDPRoute). Functionally + architecturally distinct.",
        ),
        Misconception(
            myth="\"You need to migrate everything before using Gateway API.\"",
            truth="Gateway API + Ingress coexist on the same cluster + same controller. Migrate per-route or per-team gradually; the controller serves both during the transition.",
        ),
        Misconception(
            myth="\"Gateway API is too complex for small teams.\"",
            truth="The three CRDs are simpler than Ingress + 30 controller-specific annotations once you have more than one route + one cert. For a single-route demo, Ingress is shorter; for production, Gateway API is clearer.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three core Gateway API CRDs?", back="<strong>GatewayClass</strong> (controller infrastructure; cluster-scoped). <strong>Gateway</strong> (listener bank with cert + hostname + allowed routes; namespaced). <strong>HTTPRoute</strong> (and other Route kinds; match + filter + backend; namespaced)."),
        Flashcard(front="What does ReferenceGrant do?", back="In the backend\'s namespace, explicitly grants source namespaces permission to reference the backend. Without it, cross-namespace HTTPRoute → Service fails to attach."),
        Flashcard(front="HTTPRouteFilter types?", back="<strong>RequestHeaderModifier</strong>, <strong>ResponseHeaderModifier</strong>, <strong>RequestRedirect</strong>, <strong>URLRewrite</strong>, <strong>RequestMirror</strong>, <strong>ExtensionRef</strong> (controller-specific). Typed; schema-validated; portable."),
        Flashcard(front="What is BackendTLSPolicy?", back="Tells Gateway to re-encrypt traffic to backend with HTTPS + caBundle ref. Default Gateway → backend is plain HTTP; BackendTLSPolicy makes it end-to-end encrypted."),
        Flashcard(front="Three Route kinds beyond HTTPRoute?", back="<strong>GRPCRoute</strong> (gRPC), <strong>TCPRoute</strong> (raw TCP — not all controllers), <strong>TLSRoute</strong> (TLS passthrough), <strong>UDPRoute</strong> (UDP). Different controllers support different sets."),
        Flashcard(front="Why role separation matters?", back="Infra owns Gateway (cert, hostname, TLS); app teams own HTTPRoutes (their routes). Infra changes don\'t need app-team coordination; app-team route changes don\'t require infra approval. Pattern scales to many teams."),
        Flashcard(front="ingress2gateway — what does it do?", back="CLI tool converting Ingress manifests to Gateway API equivalents per controller. Output: Gateway + HTTPRoute YAMLs. Not perfect; requires review for annotation-specific behavior."),
        Flashcard(front="When pick Envoy Gateway vs Istio Gateway?", back="<strong>Envoy Gateway</strong>: pure Gateway API; minimal moving parts; recommended if you only need Gateway API. <strong>Istio Gateway</strong>: full mesh integration; pick if you\'re using Istio mesh anyway. Same Envoy data plane in both."),
    ],
    quizzes=[
        Quiz(
            prompt="A team has 30 NGINX Ingresses with annotation soup. Walk through migration to Gateway API.",
            answer="(1) <strong>Pick controller</strong>: NGINX Gateway Fabric (familiar) or Envoy Gateway (cleaner). (2) <strong>Install GatewayClass</strong>: cluster-scoped, references the chosen controller. (3) <strong>Create shared Gateway</strong>: same listeners as existing Ingress (port 443, hostname, cert). (4) <strong>Convert per-Ingress</strong>: <code>ingress2gateway</code> CLI emits HTTPRoute YAML; review for annotation-specific behaviors (auth, rate limit, regex paths). (5) <strong>Test in dev</strong>: deploy Gateway + HTTPRoute alongside Ingress; flip a small traffic share; observe behavior. (6) <strong>Stage</strong>: switch traffic gradually via DNS or per-route. (7) <strong>Decommission Ingress</strong> per route after a stability window. (8) <strong>Update CI / IaC</strong> to ship Gateway API by default. <em>Total time: 2-4 weeks for 30 Ingresses depending on annotation complexity.</em>",
        ),
        Quiz(
            prompt="A tenant team in namespace <code>team-a</code> wants to route to a backend Service in namespace <code>shared-services</code>. Walk what\'s required.",
            answer="(1) <strong>Gateway in infra namespace</strong> already exists and accepts routes from any namespace. (2) <strong>HTTPRoute in <code>team-a</code></strong>: <code>parentRefs</code> → infra Gateway; <code>backendRefs: [{name: shared-svc, namespace: shared-services}]</code>. (3) <strong>ReferenceGrant in <code>shared-services</code></strong>: <code>from: [{group: gateway.networking.k8s.io, kind: HTTPRoute, namespace: team-a}]</code>, <code>to: [{group: \"\", kind: Service, name: shared-svc}]</code>. (4) Without ReferenceGrant, the HTTPRoute attaches but reports condition=ResolvedRefs=False; traffic 503s. (5) <em>Audit pattern</em>: shared-services namespace audits ReferenceGrants quarterly; revokes unused grants.",
        ),
        Quiz(
            prompt="The CFO asks why we don\'t just stay on Ingress. Defend Gateway API.",
            answer="\"<strong>Three reasons Gateway API beats Ingress over time:</strong> (1) <strong>Role separation</strong>: as the cluster grows past 5 app teams, infra-owns-Gateway / teams-own-HTTPRoutes prevents the bottleneck where every route change needs infra. Faster team velocity. (2) <strong>Typed config</strong>: schema-validated CRDs catch typos at apply-time. Annotation typos broke routing in last quarter\'s incident; that class disappears. (3) <strong>Multi-cluster + L4 protocols</strong>: Gateway API handles TCPRoute / TLSRoute / multi-cluster cleanly; Ingress can\'t. <strong>Migration cost is moderate</strong> (ingress2gateway + 2-4 weeks of staged migration); <strong>ongoing benefit is permanent</strong>. The K8s ecosystem is moving in this direction; new features (BackendTLSPolicy, GRPCRoute, multi-cluster) only land in Gateway API. <strong>Staying on Ingress is staying on a deprecated path.</strong>\"",
            cyoa=True,
            cyoa_tag="how the network architect defended Gateway API",
        ),
    ],
    glossary=[
        GlossaryItem(name="Gateway API", definition="K8s SIG Network successor to Ingress. Three core CRDs: GatewayClass + Gateway + Route. Typed; role-separated; portable."),
        GlossaryItem(name="GatewayClass", definition="Cluster-scoped CRD naming the controller + parameters. Set up by infra team."),
        GlossaryItem(name="Gateway", definition="Namespaced CRD listing listeners (port + protocol + cert + hostname + allowed routes). Owned by infra / platform."),
        GlossaryItem(name="HTTPRoute", definition="Namespaced CRD attaching to Gateway via parentRefs; declares match + filter + backendRefs. Owned by app teams."),
        GlossaryItem(name="ReferenceGrant", definition="Backend namespace explicitly grants source namespaces permission to reference. Cross-namespace consent."),
        GlossaryItem(name="BackendTLSPolicy", definition="Re-encrypts Gateway → backend traffic via HTTPS + caBundle. End-to-end encryption pattern."),
        GlossaryItem(name="HTTPRouteFilter", definition="Typed filter on HTTPRoute: header modifier, redirect, URL rewrite, mirror, extension ref. Replaces Ingress annotations."),
        GlossaryItem(name="GRPCRoute / TCPRoute / TLSRoute / UDPRoute", definition="Non-HTTP route kinds. Different controllers support different sets."),
        GlossaryItem(name="ingress2gateway", definition="CLI converting Ingress manifests to Gateway API. Per-controller; review output."),
        GlossaryItem(name="Multi-cluster Gateway", definition="Gateway-api-extensions handling fleet-wide ingress: Cilium ClusterMesh + Gateway, Istio multi-cluster, GKE MCG."),
    ],
    recap_lead="Gateway API: three roles, three CRDs, typed config. ReferenceGrant for cross-namespace; BackendTLSPolicy for re-encrypt; HTTPRouteFilters for rewrites. Migration from Ingress is per-route + gradual.",
    recap_next='<strong>Next — N3: Multi-cluster networking.</strong> Submariner, Skupper, Cilium ClusterMesh, Istio multi-cluster — pick by trust + perf needs; cross-cloud + on-prem patterns.',
)
