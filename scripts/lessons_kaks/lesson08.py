"""K-AKS A8 — AKS Add-ons and Platform Features (Dapr, Istio, Flux, Arc, Hybrid, Edge, Fleet Manager)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AKS managed add-ons and the broader platform — Dapr, Istio, Flux, Workload Identity, App Routing, Arc, Hybrid, Edge, Fleet.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Student Union — managed add-ons + multi-cluster</text>
  <rect x="50" y="60" width="240" height="130" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="170" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">managed add-ons</text>
  <text x="170" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">KEDA · Dapr · Istio mesh</text>
  <text x="170" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">Flux v2 GitOps</text>
  <text x="170" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">Workload Identity (WI)</text>
  <text x="170" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">Key Vault Secrets Provider</text>
  <text x="170" y="160" text-anchor="middle" font-size="9" fill="#FFFFFF">App Routing (NGINX)</text>
  <rect x="305" y="60" width="200" height="130" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="405" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">multi-cluster + edge</text>
  <text x="405" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6">Azure Arc-enabled K8s</text>
  <text x="405" y="113" text-anchor="middle" font-size="8" font-style="italic" fill="#FBF1D6">on-prem / multi-cloud</text>
  <text x="405" y="132" text-anchor="middle" font-size="9" fill="#FBF1D6">AKS Hybrid</text>
  <text x="405" y="145" text-anchor="middle" font-size="8" font-style="italic" fill="#FBF1D6">Azure Local / Stack HCI</text>
  <text x="405" y="160" text-anchor="middle" font-size="9" fill="#FBF1D6">AKS Edge Essentials</text>
  <text x="405" y="173" text-anchor="middle" font-size="8" font-style="italic" fill="#FBF1D6">single-node / edge</text>
  <rect x="520" y="60" width="190" height="130" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="615" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">fleet management</text>
  <text x="615" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Fleet Manager</text>
  <text x="615" y="113" text-anchor="middle" font-size="8" font-style="italic" fill="#FFFFFF">multi-cluster ops</text>
  <text x="615" y="132" text-anchor="middle" font-size="9" fill="#FFFFFF">cluster placement</text>
  <text x="615" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">policy + upgrade waves</text>
  <text x="615" y="160" text-anchor="middle" font-size="9" fill="#FFFFFF">workload propagation</text>
  <text x="615" y="180" text-anchor="middle" font-size="8" font-style="italic" fill="#FFFFFF">100+ clusters? you need this</text>
</svg>"""


LESSON = LessonSpec(
    num="08",
    title_short="AKS add-ons &amp; platform",
    title_full="A8 · AKS Add-ons and Platform Features",
    title_html="K-AKS A8 · Add-ons and Platform Features",
    module_eyebrow="Module A8 · the Student Union — managed add-ons and the broader platform",
    hero_sub_html='<strong>Managed add-ons</strong>: KEDA, Dapr, Istio-based service mesh, Flux v2 GitOps, Workload Identity, Key Vault Secrets Provider, App Routing (managed NGINX). <strong>Multi-cluster + edge</strong>: <strong>Azure Arc-enabled Kubernetes</strong> (on-prem / multi-cloud K8s under Azure governance), <strong>AKS Hybrid</strong> (AKS on Azure Local / Stack HCI), <strong>AKS Edge Essentials</strong> (single-node edge). <strong>Fleet Manager</strong> for managing 100+ AKS clusters as one fleet.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"GitOps reconcile loop is failing across 47 clusters\"</em> — the Flux v2 add-on configuration drifted because someone hand-edited the HelmRelease in one cluster two weeks ago. You\'re kubectl-ing into clusters one at a time. <em>You realise you have no Fleet Manager.</em> Today\'s lesson: the managed add-ons that turn AKS from one cluster into a fleet, and the platform features that take K8s beyond Azure data centers (Arc, Hybrid, Edge).",
    stamp_html="<strong>Use AKS managed add-ons (KEDA / Dapr / Istio / Flux / WI / KV provider / App Routing) instead of self-installed Helm charts. Arc-enable on-prem clusters; AKS Hybrid for Azure Local; Edge Essentials for single-node. Fleet Manager when you have many clusters.</strong>",
    district_pin="kc-wing08",
    district_label="Student Union",
    sections=[
        Section(
            eyebrow="Section 1.1 · managed add-ons",
            h2="Managed add-ons — pre-built, supported, lifecycle-managed",
            body_html="""    <p>AKS ships these as <strong>managed add-ons</strong> — Microsoft installs, upgrades, and supports them. Compared to bring-your-own Helm charts: faster onboarding, no Helm-rot, security patches automatic, fewer version-skew incidents.</p>
    <ul>
      <li><strong>KEDA</strong> (covered in A5) — event-driven Pod scaling.</li>
      <li><strong>Dapr</strong> — distributed application runtime: pluggable building blocks (state stores, pub/sub, secrets, bindings) via sidecar. Polyglot apps speak HTTP/gRPC to the Dapr sidecar instead of cloud SDKs. <em>Cleaner cloud-portability story.</em></li>
      <li><strong>Istio-based service mesh add-on</strong> — Microsoft-managed Istio control plane. Sidecars on Pods (mTLS, traffic management, retries, observability). Released as the Microsoft-supported alternative to self-installed Istio / Linkerd. Be intentional: a service mesh is a real operational commitment.</li>
      <li><strong>Flux v2 GitOps add-on</strong> — continuous reconciliation from a Git repo. <code>FluxConfiguration</code> CRD wraps a GitRepository + Kustomization / HelmRelease. Replaces in-cluster Argo CD installs with managed Flux at the AKS Resource Provider level.</li>
      <li><strong>Workload Identity</strong> (covered in A2) — federated credentials for Pod auth.</li>
      <li><strong>Azure Key Vault Secrets Provider</strong> (covered in A4) — Secrets Store CSI driver + Azure Key Vault provider, packaged as a managed add-on.</li>
      <li><strong>Application Routing add-on</strong> (covered in A3) — managed NGINX ingress + cert-manager + Azure DNS.</li>
    </ul>
    <p><strong>Decision:</strong> if a managed add-on covers your need, <em>use it</em>. The cost of self-installed Helm vs managed add-on is steep over time — broken upgrades, missing security patches, cluster-specific tribal knowledge.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Azure Arc-enabled Kubernetes",
            h2="Azure Arc-enabled Kubernetes — non-AKS clusters under Azure governance",
            body_html="""    <p><strong>Azure Arc-enabled Kubernetes</strong> = bring any conformant K8s cluster (on-prem, AWS EKS, GCP GKE, hand-rolled kubeadm, OpenShift, etc.) under Azure\'s management plane. Install the <code>azure-arc</code> agent in the cluster; the cluster appears as an Azure resource; you can apply Azure Policy, Defender, GitOps (Flux), Monitor (Container Insights), Workload Identity, Key Vault CSI — same surface as AKS.</p>
    <ul>
      <li><strong>Use cases:</strong> brownfield K8s clusters from acquisitions; multi-cloud K8s ops standardised on Azure tooling; on-prem clusters that need cloud-native security/observability without migrating workloads to AKS.</li>
      <li><strong>Trade-off:</strong> the cluster\'s control plane is still operated by you (or whoever runs the source cluster) — Arc gives you Azure-side management; it doesn\'t make a non-AKS cluster managed.</li>
      <li><strong>Connectivity</strong>: requires outbound HTTPS from the cluster to the Azure Arc Resource Bridge endpoints. Air-gapped clusters need disconnected Arc (preview).</li>
    </ul>"""
        ),
        Section(
            eyebrow="Section 1.3 · AKS Hybrid + Edge Essentials",
            h2="AKS Hybrid + AKS Edge Essentials",
            body_html="""    <p><strong>AKS on Azure Local (formerly Azure Stack HCI / AKS hybrid)</strong> — full AKS control plane running on customer-owned hyperconverged infrastructure (HPE, Dell, Lenovo certified hardware running Azure Local OS). Same kubectl surface, same managed add-ons (where supported), same Azure governance via Arc. <em>For regulated workloads / data residency / data sovereignty.</em></p>
    <p><strong>AKS Edge Essentials</strong> — lightweight single-node (or small-cluster) AKS for Windows / Linux IoT edge devices. Designed for retail, factory floors, ATMs, kiosks. Manageable from Azure via Arc; runs on hardware as small as a NUC. <em>For workloads that must execute physically near the data source.</em></p>
    <p><strong>Picking among on-prem options:</strong>
    <ul>
      <li>Existing on-prem K8s, want Azure governance? → <strong>Arc-enabled K8s</strong>.</li>
      <li>Building net-new on-prem and want Microsoft to operate the K8s + provide certified hardware? → <strong>AKS on Azure Local</strong>.</li>
      <li>Edge / single-node / sub-second locality? → <strong>AKS Edge Essentials</strong>.</li>
    </ul></p>"""
        ),
        Section(
            eyebrow="Section 1.4 · Fleet Manager",
            h2="Azure Kubernetes Fleet Manager — many-cluster operations",
            body_html="""    <p><strong>Fleet Manager</strong> turns N AKS clusters into a single managed fleet. The Fleet itself is an Azure resource — you join member AKS clusters; Fleet provides:</p>
    <ul>
      <li><strong>Workload propagation</strong> — apply a K8s manifest (Deployment, ConfigMap, etc.) to all member clusters with one apply (or to a subset based on labels / selectors). <em>One source of truth for fleet-wide infra.</em></li>
      <li><strong>Cluster placement</strong> — schedule a workload to specific clusters by label / region / capacity heuristics.</li>
      <li><strong>Update orchestration</strong> — coordinated cluster upgrade waves (e.g. dev first, prod second; one region at a time). Pause / resume / skip per cluster.</li>
      <li><strong>Multi-cluster L4 load balancing</strong> via Service Fabric Mesh-style features (preview / GA per region).</li>
    </ul>
    <p><strong>When you need Fleet Manager:</strong> ~10+ AKS clusters, especially if any of (multi-region active-active, per-tenant cluster strategy, regulated/sovereignty isolation, or staged rollout discipline). <em>Below 10 clusters, manual ops + GitOps usually suffice.</em></p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="The team is debating between installing Argo CD via Helm vs enabling the Flux v2 add-on. Why pick the managed add-on?",
            options=[
                ("Argo CD is unsupported on AKS.", False),
                ("The managed Flux add-on is installed, upgraded, and supported by Microsoft as a Resource Provider — no Helm-rot, security patches automatic, configured via Azure CLI / Bicep / Portal as <code>FluxConfiguration</code> CRDs.", True),
                ("Flux is faster than Argo CD.", False),
            ],
            feedback="It\'s the operational story: managed Flux is part of the AKS Resource Provider; you don\'t operate the GitOps controller. Argo CD self-install works but you own its lifecycle.",
        ),
    },
    before_after_before='<p>Pre-managed-add-on AKS = Helm-everywhere. Engineers installed cert-manager, KEDA, Workload Identity, Secrets Store CSI, NGINX ingress, Dapr, Linkerd, Argo CD, and Prometheus Operator each as a Helm chart per cluster. Upgrades were per-chart per-cluster; chart break × cluster count = ops fire-quarter. Multi-cloud K8s had no unified governance — separate dashboards per provider; separate audit pipes; separate cost views. Multi-cluster ops required scripts looping over <code>kubectl --context</code>.</p>',
    before_after_after='<p>Modern AKS ships <strong>managed add-ons</strong> (KEDA, Dapr, Istio, Flux v2, WI, Key Vault provider, App Routing) — installed by the AKS Resource Provider, upgraded with the cluster, supported by Microsoft. <strong>Azure Arc</strong> brings non-AKS clusters under Azure governance. <strong>AKS Hybrid + Edge Essentials</strong> let AKS run on customer hardware. <strong>Fleet Manager</strong> turns 100 clusters into one fleet for workload propagation, placement, and coordinated upgrades.</p>',
    before_after_caption='<p class="ba-caption"><em>The era of \"every team operates a Helm-chart farm\" is over. Managed add-ons + Arc + Fleet shift the operational burden from per-cluster engineers to the AKS Resource Provider.</em></p>',
    analogy_intro_html='''<p>The <strong>Student Union</strong> is the building where shared services are stocked: copying machine, vending, post office, conference rooms. Faculty don\'t run their own copy machines.</p>
    <p>The <strong>Counter Window</strong> stocks managed add-ons. KEDA is the queue-watcher. Dapr is the universal adapter (any app speaks the Union\'s standard interface, the Union talks to whatever cloud DB or pub/sub exists outside). Istio is the in-house security and traffic engineer who walks every package between offices, signing it (mTLS), measuring delays (telemetry), and rerouting around closed corridors. Flux v2 is the daily reconciler — checks Git every minute and ensures every shelf in every wing matches the recipe in the book.</p>
    <p>The <strong>Inter-campus Mailroom</strong> (Azure Arc) reaches off-campus. Other campuses (on-prem K8s, EKS, GKE) sign up to share Azure governance — same Defender, same Policy, same Flux GitOps — without moving their buildings. <strong>AKS Hybrid</strong> is when Microsoft sends a turnkey campus building to your private estate. <strong>Edge Essentials</strong> is the satellite kiosk you set up at a single corner store.</p>
    <p>The <strong>Provost\'s Office</strong> (Fleet Manager) sits above all campuses — applies one curriculum to many campuses, schedules upgrade waves region by region, propagates one rule everywhere with one click.</p>''',
    translation_rows=[
        ("Counter Window — shared services", "Managed add-ons surface"),
        ("Universal adapter", "Dapr — pluggable building blocks via sidecar"),
        ("In-house traffic engineer", "Istio-based service mesh add-on"),
        ("Daily reconciler", "Flux v2 GitOps add-on"),
        ("Queue-watcher", "KEDA"),
        ("Sealed-envelope worker permits", "Workload Identity"),
        ("Vault key-fetch desk", "Key Vault Secrets Provider (Secrets Store CSI)"),
        ("In-house mailroom (NGINX)", "Application Routing add-on"),
        ("Off-campus inter-campus mailroom", "Azure Arc-enabled Kubernetes"),
        ("Microsoft-built turnkey campus", "AKS on Azure Local (Hybrid)"),
        ("Single-corner satellite kiosk", "AKS Edge Essentials"),
        ("Provost\'s Office", "Azure Kubernetes Fleet Manager"),
        ("Coordinated curriculum updates", "Fleet update orchestration / upgrade waves"),
    ],
    analogy_stops="A Provost can\'t actually micromanage every classroom; Fleet Manager can\'t hide K8s\'s eventual consistency or per-cluster RBAC nuances — workloads do still need per-cluster reconciliation.",
    eli5="The Student Union has all the shared stuff. You don\'t run your own copy machine — you use the Union\'s. Same with the campus services: Microsoft runs the queue-watcher, the security guards, the daily Git syncer. You just turn them on.",
    eli10="<strong>Managed add-ons</strong> = AKS-installed-and-supported KEDA / Dapr / Istio mesh / Flux v2 GitOps / Workload Identity / Key Vault provider / App Routing. <strong>Arc-enabled K8s</strong> brings non-AKS clusters under Azure governance (Policy / Defender / Monitor / Flux). <strong>AKS Hybrid (Azure Local)</strong> = Microsoft-operated AKS on certified customer hardware. <strong>AKS Edge Essentials</strong> = single-node edge AKS. <strong>Fleet Manager</strong> = workload propagation, placement, coordinated upgrades for 10+ AKS clusters.",
    scenarios=[
        Scenario(
            name="SaaS — Dapr unifies polyglot stack",
            body="A SaaS has services in Go, Python, Node, and .NET. Each team had picked its own state-store/pub-sub library. Dapr standardises: every service uses Dapr building blocks (state, pub/sub, secrets); Dapr sidecar talks to Cosmos DB, Service Bus, Key Vault. <em>One platform team owns infra integrations; product teams ship features faster.</em>",
        ),
        Scenario(
            name="Brownfield M&A — Arc-enable acquired company\'s on-prem K8s",
            body="A bank acquires a fintech with ten on-prem K8s clusters running OpenShift. Migration to AKS would take a year. Short-term: Arc-enable each cluster (one az command per cluster). Result: Defender for Containers + Azure Policy + Container Insights + Flux v2 GitOps + Workload Identity working on the legacy clusters in two weeks. <em>Compliance posture aligned without workload migration.</em>",
        ),
        Scenario(
            name="Retail edge — AKS Edge Essentials at 800 stores",
            body="A grocery chain runs inventory + POS workloads at each store. Per-store hardware: NUC running AKS Edge Essentials, single-node, Arc-connected for management. Workloads: local inventory cache, in-store ML for restock prediction. <em>800 single-node clusters managed centrally; deploys via Arc-enabled Flux.</em>",
        ),
        Scenario(
            name="Multi-region SaaS — 100 clusters under Fleet Manager",
            body="A SaaS runs 100 AKS clusters (5 regions × 20 tenants each). Fleet Manager joins all 100 as members. Common workloads (cluster autoscaler config, NetworkPolicy, ingress controller) deployed once via workload propagation. Upgrade orchestration cycles dev clusters first, prod next, by region wave. <em>One platform engineer manages the fleet; tenants don\'t see the choreography.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Managed add-on means I lose all configuration control.\"",
            truth="Managed add-ons are <em>opinionated</em> but not opaque. You configure them via standard CRDs (FluxConfiguration, ScaledObject, etc.) and Azure-side resources. What you give up is <em>installing/upgrading/patching the controller itself</em> — not the workload-level configuration.",
        ),
        Misconception(
            myth="\"Arc-enabled K8s is the same as AKS — I can run it the same way.\"",
            truth="Arc gives you Azure-side <em>management surface</em> (Policy, Defender, Monitor, Flux). The K8s control plane is still whatever it was — kubeadm, OpenShift, EKS, GKE. You\'re still on the hook for upgrades, scaling, patching of that control plane. AKS Hybrid (AKS on Azure Local) is the path where Microsoft operates the K8s control plane on your hardware.",
        ),
        Misconception(
            myth="\"Service mesh is always worth it.\"",
            truth="A service mesh is a real operational commitment — sidecar resource overhead, mesh-config drift, version-bump testing across hundreds of services. Worth it when you genuinely need mTLS-everywhere + L7 traffic management + cross-team observability. For a 5-service project, an mTLS mesh is probably yak-shaving. The Istio add-on lowers the bar but doesn\'t eliminate it.",
        ),
    ],
    flashcards=[
        Flashcard(front="Seven AKS managed add-ons?", back="<strong>KEDA</strong> (event-driven Pod scaling), <strong>Dapr</strong> (distributed app runtime sidecar), <strong>Istio service mesh</strong>, <strong>Flux v2 GitOps</strong>, <strong>Workload Identity</strong>, <strong>Key Vault Secrets Provider</strong>, <strong>Application Routing</strong> (managed NGINX)."),
        Flashcard(front="When pick Flux v2 add-on vs self-installed Argo CD?", back="<strong>Flux add-on</strong>: Microsoft installs/upgrades/supports; configure via Azure CLI / Bicep / FluxConfiguration CRD; ideal for Azure-aligned shops. <strong>Argo CD</strong>: more UI-rich; multi-tenant with project isolation; ideal where teams want the Argo UX. Both work; Flux is the path-of-least-resistance for AKS."),
        Flashcard(front="What does Dapr do?", back="Sidecar that exposes pluggable building blocks (state store, pub/sub, secrets, bindings, actors) as HTTP/gRPC to the app. App speaks Dapr API, Dapr talks to Cosmos / Service Bus / Key Vault / etc. Decouples app code from cloud-specific SDKs."),
        Flashcard(front="What does Azure Arc-enabled Kubernetes give you?", back="Brings any conformant K8s cluster under Azure\'s management plane: Policy, Defender, Monitor, Flux GitOps, WI, Key Vault CSI. Cluster is registered as an Azure resource via the <code>azure-arc</code> agent. Multi-cloud / on-prem governance unified."),
        Flashcard(front="AKS on Azure Local — what is it?", back="Full AKS running on customer-owned hyperconverged hardware certified by Microsoft (HPE / Dell / Lenovo with Azure Local OS). Microsoft operates the K8s control plane; you operate the data center. Same managed add-ons surface where supported."),
        Flashcard(front="When use AKS Edge Essentials?", back="Single-node (or very small) edge devices — retail, factory, ATM, kiosk. Lightweight K8s, manageable centrally via Arc. Hardware as small as a NUC."),
        Flashcard(front="When do you need Fleet Manager?", back="At ~10+ AKS clusters, especially with multi-region active-active, per-tenant clusters, sovereignty isolation, or staged rollout discipline. Provides workload propagation, cluster placement, coordinated upgrade waves. Below 10 clusters, manual ops + GitOps suffice."),
        Flashcard(front="Three on-prem K8s options under Azure?", back="<strong>Arc-enabled K8s</strong> (existing K8s + Azure governance). <strong>AKS Hybrid (on Azure Local)</strong> (Microsoft-operated AKS on certified hardware). <strong>AKS Edge Essentials</strong> (single-node / very small edge)."),
    ],
    quizzes=[
        Quiz(
            prompt="The team installed cert-manager + Argo CD + Linkerd + Workload Identity + Secrets Store CSI all via Helm a year ago. Half the chart upgrades have broken. What\'s the cleanup path?",
            answer="Inventory: which of these now exist as managed add-ons? <strong>Workload Identity</strong> + <strong>Secrets Store CSI / Key Vault Provider</strong> + <strong>App Routing (cert-manager-equipped NGINX)</strong> + <strong>Flux v2</strong> + <strong>Istio service mesh add-on</strong> all do. Migration order: start with the least-risky (Workload Identity → enable add-on, migrate annotations, drop Helm), then cert-manager (move to App Routing add-on), then GitOps (parallel-run Flux add-on alongside Argo CD until comfortable, then drop Argo). <em>Result: 5 self-installed Helm charts → 0; Microsoft owns the upgrade path.</em>",
        ),
        Quiz(
            prompt="The platform team sponsors a service mesh rollout. Engineers ask: \"What does the Istio add-on give us that vanilla Istio doesn\'t?\" Answer.",
            answer="<strong>Microsoft installs, upgrades, and supports the Istio control plane</strong> — you don\'t handle Istio version-bumps, CVE patches, or operator-config drift across clusters. The data plane (sidecars) is still Istio. Trade-offs: Microsoft chooses the supported version line (one or two minors behind upstream); some Istio features (custom EnvoyFilter, beta APIs) may not be supported. The mesh-as-managed surface is the value; if you need bleeding-edge Istio features, self-install is the alternative.",
        ),
        Quiz(
            prompt="A bank has 50 AKS clusters across 4 regions. Compliance now requires every cluster to enforce a specific NetworkPolicy default-deny + a specific PSA Restricted label. The platform team has no Fleet Manager. How long does this rollout take, and what changes with Fleet Manager?",
            answer="<strong>Without Fleet Manager:</strong> per-cluster work — at minimum a script looping kubectl across 50 contexts, with per-cluster verification. Realistically 1-2 sprints with verification + rollback per cluster + handling per-cluster anomalies. <strong>With Fleet Manager:</strong> create a FleetWorkload resource with the NetworkPolicy + namespace label, apply once, fleet propagates to all 50 members; verify via Fleet status. Hours, not sprints. Plus future compliance changes are one-touch instead of fifty-touch.",
            cyoa=True,
            cyoa_tag="how long the compliance rollout took",
        ),
    ],
    glossary=[
        GlossaryItem(name="Managed add-on", definition="AKS-installed, AKS-upgraded, Microsoft-supported K8s component. Configured via Azure CLI / Bicep / Portal."),
        GlossaryItem(name="Dapr", definition="Distributed application runtime — sidecar exposes pluggable building blocks (state, pub/sub, secrets) as HTTP/gRPC."),
        GlossaryItem(name="Istio service mesh add-on", definition="Microsoft-managed Istio control plane on AKS. Sidecars provide mTLS, traffic management, observability."),
        GlossaryItem(name="Flux v2 GitOps add-on", definition="Continuous reconciliation from Git. FluxConfiguration CRD wraps GitRepository + Kustomization / HelmRelease."),
        GlossaryItem(name="Application Routing add-on", definition="Managed NGINX ingress + cert-manager + Azure DNS. Replaces deprecated HTTP Application Routing."),
        GlossaryItem(name="Azure Arc-enabled Kubernetes", definition="Brings any conformant K8s cluster under Azure governance (Policy, Defender, Monitor, Flux). Cluster registered as Azure resource via azure-arc agent."),
        GlossaryItem(name="AKS on Azure Local", definition="Full AKS running on customer-owned certified hyperconverged hardware. Microsoft operates the K8s control plane."),
        GlossaryItem(name="Azure Local", definition="Microsoft\'s hyperconverged infrastructure OS (formerly Azure Stack HCI). Hardware certified by HPE / Dell / Lenovo."),
        GlossaryItem(name="AKS Edge Essentials", definition="Lightweight single-node AKS for edge / IoT devices. Manageable via Arc."),
        GlossaryItem(name="Azure Kubernetes Fleet Manager", definition="Multi-cluster orchestrator. Workload propagation, cluster placement, coordinated upgrade waves."),
        GlossaryItem(name="FleetWorkload", definition="Fleet Manager CRD that defines a workload to propagate across member clusters."),
        GlossaryItem(name="Update orchestration (Fleet)", definition="Coordinated cluster upgrade waves with pause / resume / skip per cluster."),
    ],
    recap_lead='Managed add-ons replace Helm sprawl; Arc, Hybrid, and Edge Essentials extend AKS beyond Azure data centres; Fleet Manager handles many-cluster ops.',
    recap_next='<strong>Next — A9: AKS Upgrades and Operations.</strong> AKS version support (N-2 + LTS); platform support N-3; AKS Release Tracker; auto-upgrade channels; node image upgrades; planned maintenance windows; surge upgrades; blue-green node pool migration; API deprecations; certificate rotation.',
)
