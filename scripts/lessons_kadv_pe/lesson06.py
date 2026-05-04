"""K-ADV-PE P6 — Workload abstractions: Score, KubeVela / OAM, Radius, Humanitec."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Workload abstractions."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Standard Tool Set · K-Workshop — workload abstractions on top of K8s</text><rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E"/><text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Score</text><text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">CNCF; YAML; portable</text><rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5"/><text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">KubeVela / OAM</text><text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">CUE-based; typed</text><rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900"/><text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Radius (MS)</text><text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">app-graph; Bicep</text><rect x="595" y="70" width="125" height="100" rx="10" fill="#5A6B81"/><text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Humanitec</text><text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">opinionated PaaS</text></svg>"""


LESSON = LessonSpec(
    num="06", title_short="workload abstractions", title_full="P6 · Workload Abstractions: Score, KubeVela / OAM, Radius, Humanitec",
    title_html="K-ADV-PE P6 · Workload Abstractions", module_eyebrow="Module P6 · Standard Tool Set — workload abstractions on top of K8s",
    hero_sub_html='Four workload abstractions trying to hide K8s complexity from developers. <strong>Score</strong> (CNCF Sandbox): YAML spec; \"workload + dependencies\"; portable across K8s + ECS + Cloud Run. <strong>KubeVela / OAM</strong>: CUE-based typed app definition; trait composition. <strong>Radius</strong> (Microsoft): app-graph (resources + connections); Bicep authoring. <strong>Humanitec</strong>: opinionated PaaS-style; portal-driven; commercial.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A new developer needs to write 200 lines of YAML for a service. They copy from another team\'s repo; subtly different; deploy fails; they file a ticket. <em>Without an abstraction, every developer is a K8s engineer</em>. Today\'s lesson: workload abstractions trade portability + opinionation for developer ergonomics.",
    stamp_html="<strong>Score / OAM / Radius / Humanitec abstract K8s for developers. Pick by team ergonomics + portability needs. Platform team owns the abstraction; developers consume.</strong>",
    district_pin="kpe-bench06", district_label="Standard Tool Set",
    sections=[
        Section(eyebrow="Section 1.1 · Score", h2="Workload + dependencies in YAML; portable",
            body_html="""    <p><strong>Score</strong> (CNCF Sandbox): minimal YAML spec. Declares <em>workload</em> (containers + scaling) + <em>resources</em> (DBs / queues / DNS) + <em>service</em> (ports). <strong>score-compose</strong> renders to Docker Compose; <strong>score-helm</strong> renders to Helm chart; <strong>score-k8s</strong> directly to K8s manifests; <strong>score-ecs</strong> to AWS ECS Task Defs.</p>
    <p>Win: <em>portable</em>. Same Score spec runs in dev (Compose), staging (K8s), prod (K8s + Crossplane DBs). Reduce dev/prod divergence."""),
        Section(eyebrow="Section 1.2 · KubeVela / OAM", h2="CUE-based typed application model",
            body_html="""    <p><strong>OAM (Open Application Model)</strong>: spec for <em>Components</em> (workloads) + <em>Traits</em> (cross-cutting concerns: scaling, ingress, observability) + <em>Policies</em> + <em>Workflows</em>. Defines structure separate from implementation.</p>
    <p><strong>KubeVela</strong>: K8s implementation of OAM. <em>CUE-based</em> — typed config language (more constraints than YAML; less verbose). Compose Components + Traits per app; ship to many clusters.</p>
    <p>Win: <em>typed app definitions</em>; trait composition replaces copy-paste-yaml across teams."""),
        Section(eyebrow="Section 1.3 · Radius",
            h2="App-graph + recipes (Microsoft)",
            body_html="""    <p><strong>Radius</strong> (Microsoft, open source): models app as a <em>graph</em> — resources (compute / DB / cache) + connections between them. Authoring in <strong>Bicep</strong> (or YAML). Recipes encapsulate per-environment infrastructure (Postgres in dev = local container; in prod = managed Postgres).</p>
    <p>Compared to OAM: graph-centric (relationships first-class); cloud-agnostic; tight Bicep ergonomics for Azure shops.</p>
    <p>Win: <em>relationships are explicit + typed</em>; environment-specific recipes hide cloud differences."""),
        Section(eyebrow="Section 1.4 · Humanitec + selection",
            h2="Opinionated PaaS + how to choose",
            body_html="""    <p><strong>Humanitec</strong>: commercial; portal-driven; opinionated PaaS-style. Tenants pick from a menu; Humanitec handles K8s + Terraform + GitOps under the hood. Trade self-host for hosted simplicity.</p>
    <p><strong>Selection grid</strong>:</p>
    <ul>
      <li><em>Want portability across K8s + ECS + Cloud Run + Compose</em>: Score.</li>
      <li><em>Want typed app model + trait composition</em>: KubeVela / OAM.</li>
      <li><em>Want app-graph model + Bicep / Azure-shop ergonomics</em>: Radius.</li>
      <li><em>Want hosted PaaS-as-a-service</em>: Humanitec.</li>
    </ul>
    <p>None of these replace K8s; they\'re higher-level abstractions on top."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why pick Score over writing K8s YAML directly?",
            options=[("Score is faster.", False), ("Same spec runs in Compose dev + K8s prod + ECS staging — portability.", True), ("Score has more features.", False)],
            feedback="Portability is the key Score win. Reduces dev/prod divergence + lets a service deploy to multiple targets without rewrites."),
        3: PauseCheck(question="A team\'s app is essentially a graph of services + databases + caches. Which abstraction fits?",
            options=[("Score.", False), ("Radius — graph-centric model with explicit connections.", True), ("OAM.", False)],
            feedback="Radius models apps as graphs with first-class relationships. Bicep authoring; recipes per environment. Strong fit when relationships matter."),
    },
    before_after_before='<p>Pre-abstractions, developers wrote 200 lines of K8s YAML per service. Copy-paste-modify drift; per-team variation; high cognitive load.</p>',
    before_after_after='<p>Workload abstraction: developer writes 30-line spec; platform-owned tooling renders K8s + cloud + observability. Portable + typed + composable.</p>',
    before_after_caption='<p class="ba-caption"><em>Hide K8s complexity from developers; platform team owns the abstraction.</em></p>',
    analogy_intro_html='''<p>The Standard Tool Set on the workshop wall has four kits. Score is a portable toolbox — same tools work in any workshop. KubeVela is a precision-tool case — typed parts compose. Radius is a wiring-diagram drafting set — graph-first, lots of connections. Humanitec is a fully-equipped vendor truck — show up, choose from the menu.</p>''',
    translation_rows=[
        ("Portable toolbox", "Score (CNCF; portable across K8s/ECS/Compose)"),
        ("Precision-tool case", "KubeVela / OAM (CUE typed; trait composition)"),
        ("Wiring-diagram set", "Radius (Microsoft; app-graph + Bicep)"),
        ("Vendor truck", "Humanitec (commercial PaaS-as-a-service)"),
        ("Tool template", "Component + Trait (OAM) / Resource (Radius) / Workload (Score)"),
        ("Per-shop adapter", "Score-compose / score-helm / Radius recipe"),
    ],
    analogy_stops="A real toolbox is fixed; abstractions evolve as K8s evolves. Each abstraction lags K8s features; check abstraction\'s coverage of the K8s features you need.",
    eli5="Four kits on the wall. Pick the one that matches your team. Each kit hides the K8s clutter and lets developers describe their service simply.",
    eli10="<strong>Score</strong>: CNCF; portable; YAML workload + resources + service. <strong>KubeVela / OAM</strong>: CUE-typed; Components + Traits + Policies + Workflows. <strong>Radius</strong>: app-graph + Bicep; recipes per environment. <strong>Humanitec</strong>: opinionated PaaS; commercial; hosted.",
    scenarios=[
        Scenario(name="Score for portable services", body="A 50-engineer org runs services in Compose dev + EKS staging + GKE prod. Score spec one place; per-target Score CLI renders. Dev/prod divergence shrinks; new developers learn Score, not three platforms."),
        Scenario(name="KubeVela for opinionated tenant defaults", body="Platform team ships OAM Components: \"web-service,\" \"worker,\" \"scheduled-job.\" Each Component bundles K8s manifests + observability + scaling Traits. Tenants compose; can\'t deviate without platform-PR."),
        Scenario(name="Radius for app-graph thinking", body="An Azure-shop org models apps as graphs: web-frontend → api → cache + db + queue. Radius encodes connections. Per-environment recipes: dev = local container; prod = Azure managed services. Bicep authoring familiar."),
        Scenario(name="Humanitec for fast PaaS adoption", body="A 25-engineer SaaS adopts Humanitec to skip platform-build phase. Tenants self-serve via portal; Humanitec runs the K8s + Crossplane + GitOps under the hood. Trade self-build for hosted speed."),
    ],
    misconceptions=[
        Misconception(myth="\"Workload abstractions replace K8s.\"", truth="They\'re abstractions <em>on top of</em> K8s (or other targets). The K8s underneath is still the runtime; abstraction renders to it."),
        Misconception(myth="\"Pick the most popular abstraction.\"", truth="Pick by team\'s ergonomics + needs. Score for portability; OAM for typed composition; Radius for graph thinking; Humanitec for hosted. Forcing the wrong one = friction."),
        Misconception(myth="\"Once abstracted, no team needs K8s knowledge.\"", truth="Platform team needs deep K8s + the abstraction\'s rendering layer. Developers can be K8s-free <em>most</em> of the time but need basics for incidents."),
    ],
    flashcards=[
        Flashcard(front="Score — what\'s the win?", back="<strong>Portable</strong> across targets (K8s / ECS / Compose / Cloud Run). Same spec; per-target render via score-CLI."),
        Flashcard(front="KubeVela — based on what model?", back="<strong>Open Application Model (OAM)</strong>: Components + Traits + Policies + Workflows. CUE-typed; trait composition."),
        Flashcard(front="Radius — what\'s its differentiator?", back="App as a <strong>graph</strong>: resources + connections first-class. Authored in Bicep or YAML; per-env recipes hide cloud."),
        Flashcard(front="Humanitec — what does it offer?", back="Commercial hosted PaaS on top of K8s + Crossplane + GitOps. Portal-driven; trade self-build for speed."),
        Flashcard(front="Component vs Trait in OAM?", back="<strong>Component</strong>: workload type (web-service / worker). <strong>Trait</strong>: cross-cutting concern (scaling / ingress / observability). Compose Components + Traits per app."),
        Flashcard(front="Score CLI variants?", back="<strong>score-compose</strong> (Docker Compose), <strong>score-helm</strong> (Helm chart), <strong>score-k8s</strong> (K8s manifests), <strong>score-ecs</strong> (AWS ECS Task Defs)."),
        Flashcard(front="Radius recipe — what does it do?", back="Environment-specific implementation of an abstract resource. \"DB recipe\" in dev = local container; in prod = managed Postgres + IRSA. Tenant spec stays the same."),
        Flashcard(front="When NOT use a workload abstraction?", back="When team is small + already comfortable with K8s + service shapes are highly varied. Abstractions add a layer to maintain; pay only when developer-ergonomics gain exceeds maintenance cost."),
    ],
    quizzes=[
        Quiz(prompt="A 200-engineer org wants to adopt a workload abstraction. How to choose?",
            answer="(1) <strong>Map team needs</strong>: portability across targets? Score. Typed app model? OAM. Graph thinking + Azure? Radius. Hosted PaaS? Humanitec. (2) <strong>Pilot</strong>: pick 1-2 services on the candidate; measure developer-time-to-first-deploy + maintenance burden. (3) <strong>Ecosystem fit</strong>: does the abstraction integrate with our Backstage + Argo CD + Crossplane? (4) <strong>Roadmap</strong>: how active is the project? Score is CNCF Sandbox (newer); KubeVela / OAM more mature; Radius backed by Microsoft. (5) <strong>Decision</strong>: pick + commit; migrating between abstractions later is expensive."),
        Quiz(prompt="A team adopts OAM but finds platform team drowning in Trait maintenance. What\'s the path?",
            answer="(1) <strong>Audit Traits</strong>: how many are bespoke per team? Reduce + standardize. (2) <strong>Component over Trait</strong>: if 3+ teams need the same pattern, make it a Component, not 3 Traits. (3) <strong>Trait registry</strong>: small canonical set with stewardship; tenant requests for new = PR + review. (4) <strong>OAM upstream</strong>: contribute reusable Traits back; less custom maintenance. (5) <strong>Re-evaluate</strong>: if maintenance &gt; benefit, consider lighter abstraction (Score)."),
        Quiz(prompt="The CFO sees Humanitec\'s $10/dev/mo: \"build it ourselves; cheaper.\" Defend Humanitec.",
            answer="\"<strong>Build-vs-buy on platform: Humanitec is 1-2 platform engineers\' year of work, hosted from day-1.</strong> Three reasons: (1) <strong>Time-to-value</strong>: Humanitec live in days; self-build = months. Developers wait for platform vs already producing. (2) <strong>Total cost</strong>: $10/dev/mo for 100 devs = $12k/yr. One platform engineer is $200k+. Humanitec is cheaper for any team &lt; 1500 devs. (3) <strong>Ongoing maintenance</strong>: Humanitec updates abstractions + handles K8s upgrades; we\'d own that work otherwise. <strong>When build wins</strong>: huge org with platform-team economies of scale; specific compliance requirement that hosted can\'t meet. <strong>For us, hosted wins until we\'re too big to fit.</strong>\"", cyoa=True, cyoa_tag="how the platform engineer defended Humanitec"),
    ],
    glossary=[
        GlossaryItem(name="Score", definition="CNCF Sandbox workload spec; portable across K8s / ECS / Compose / Cloud Run."),
        GlossaryItem(name="OAM", definition="Open Application Model; spec for Component + Trait + Policy + Workflow."),
        GlossaryItem(name="KubeVela", definition="K8s implementation of OAM; CUE-based; trait composition."),
        GlossaryItem(name="Radius", definition="Microsoft\'s open-source app-graph platform; Bicep authoring; per-env recipes."),
        GlossaryItem(name="Humanitec", definition="Commercial hosted PaaS on K8s + Crossplane + GitOps; portal-driven."),
        GlossaryItem(name="Component (OAM)", definition="Workload type (web-service / worker / scheduled-job)."),
        GlossaryItem(name="Trait (OAM)", definition="Cross-cutting concern (scaling / ingress / observability) attached to Component."),
        GlossaryItem(name="Recipe (Radius)", definition="Environment-specific implementation of an abstract resource. Dev = local; prod = managed."),
    ],
    recap_lead="Score / OAM / Radius / Humanitec abstract K8s for developers. Pick by ergonomics + portability needs; platform team owns the abstraction.",
    recap_next='<strong>Next — P7: Platform SLOs + chargeback / showback (OpenCost / Kubecost).</strong>',
)
