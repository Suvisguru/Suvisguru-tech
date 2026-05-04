"""K-ADV-PE P2 — Backstage deep dive."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Backstage four pillars."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Catalog Drawer · K-Workshop — Backstage as the IDP storefront</text><rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E"/><text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Catalog</text><text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">every service + owner</text><rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5"/><text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">TechDocs</text><text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">MkDocs from repos</text><rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900"/><text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Scaffolder</text><text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">templates → repos</text><rect x="595" y="70" width="125" height="100" rx="10" fill="#5A6B81"/><text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Plugins</text><text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">100+</text></svg>"""


LESSON = LessonSpec(
    num="02", title_short="Backstage", title_full="P2 · Backstage Deep Dive",
    title_html="K-ADV-PE P2 · Backstage", module_eyebrow="Module P2 · Catalog Drawer — Backstage as the IDP storefront",
    hero_sub_html='<strong>Backstage</strong> (Spotify-originated, CNCF Incubating): the IDP\'s storefront. <strong>Catalog</strong>: every Service / Component / API / Resource / System with owner + tier; auto-discovered from <code>catalog-info.yaml</code> in repos. <strong>TechDocs</strong>: MkDocs auto-rendered per repo; one search across all docs. <strong>Scaffolder</strong>: template engine that generates new repos + manifests from parameters. <strong>Plugins</strong>: 100+ integrations (Argo CD, Kubernetes, PagerDuty, Datadog, GitHub, GitLab, AWS / Azure / GCP).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. On-call asks \"what does service-X actually do? Who owns it?\" The team Slacks five people; nobody knows; the README is empty; the repo\'s last meaningful commit was two years ago. <em>Without a catalog, every incident starts with archaeology.</em> Today\'s lesson: Backstage as the source of truth.",
    stamp_html="<strong>Backstage four pillars: Catalog, TechDocs, Scaffolder, Plugins. Catalog is the source of truth (every service registered with owner + tier). TechDocs surfaces every README; Scaffolder ships golden paths; Plugins integrate everything.</strong>",
    district_pin="kpe-bench02", district_label="Catalog Drawer",
    sections=[
        Section(eyebrow="Section 1.1 · Catalog", h2="Every Component / Service / API / Resource / System registered",
            body_html="""    <p><strong>Catalog</strong>: every entity registered via <code>catalog-info.yaml</code> in the repo (or auto-discovered). Entity kinds: <em>Component</em> (a service), <em>API</em> (REST/gRPC contract), <em>Resource</em> (DB / queue / SaaS), <em>System</em> (collection), <em>Domain</em> (collection of Systems), <em>User / Group</em>.</p>
    <p>Owners + lifecycle (production / experimental / deprecated) + tags + dependencies. \"Who owns service-X?\" answered in &lt; 5 seconds.</p>
    <p>Auto-discovery: GitHub / GitLab integration scans org repos for <code>catalog-info.yaml</code> on cadence; new repos appear automatically.</p>"""),
        Section(eyebrow="Section 1.2 · TechDocs", h2="Per-repo MkDocs rendered centrally",
            body_html="""    <p><strong>TechDocs</strong>: MkDocs (or AsciiDoc) lives in each repo at <code>docs/</code>; Backstage builds + serves centrally. <em>Documentation as code</em>: lives next to the code; PR-reviewed; versioned.</p>
    <p>Search across all repos\' docs from one Backstage search. Replaces wiki silos.</p>
    <p>Build patterns: per-PR build (TechDocs in CI generates static site → S3 / GCS); Backstage TechDocs Backend serves from object storage. Recommended for scale.</p>"""),
        Section(eyebrow="Section 1.3 · Scaffolder", h2="Template engine generating repos + manifests",
            body_html="""    <p><strong>Scaffolder</strong>: templates declare parameters + steps. Steps include: <code>fetch:template</code> (skeleton render), <code>publish:github</code> (create repo), <code>catalog:register</code> (add to catalog), custom action (open PR for cluster onboarding). Parameters via Backstage form.</p>
    <p>Templates live in Git; PR-reviewed; versioned. Per-language / per-pattern: \"new Go service,\" \"new Postgres database,\" \"new tenant namespace.\"</p>
    <p>Custom actions extend Scaffolder for org-specific patterns (e.g., \"create AWS S3 bucket via Crossplane Claim PR\").</p>"""),
        Section(eyebrow="Section 1.4 · Plugins + Software Catalog API",
            h2="Integrations + extensibility",
            body_html="""    <p><strong>Plugins</strong> integrate Backstage with everything: Argo CD (deployment status per service), Kubernetes (cluster + Pod view), PagerDuty (on-call + incidents), GitHub / GitLab (issues + PRs), Datadog / Grafana / Honeycomb (dashboards + traces), AWS / Azure / GCP (cloud resources), security tools (Snyk, Trivy).</p>
    <p>Each plugin is a React component + backend module; cluster admin installs; users see in service page.</p>
    <p><strong>Software Catalog API</strong>: REST + GraphQL; programs query the catalog. CI pipelines + downstream tools consume catalog data — \"who owns this commit?\" \"what tier is this?\" — drives gates / alerts / routing.</p>"""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Where does service ownership live in Backstage?",
            options=[("A separate ops spreadsheet.", False), ("<code>catalog-info.yaml</code> in the repo, surfaced via Catalog.", True), ("Slack channel.", False)],
            feedback="catalog-info.yaml co-located with code; auto-discovered; PR-reviewed; ownership is verifiable + version-controlled."),
        3: PauseCheck(question="What does the Scaffolder produce?",
            options=[("A Backstage UI page.", False), ("New repo + initial commits + catalog registration + optional PRs (e.g., cluster onboarding).", True), ("A Helm chart.", False)],
            feedback="Scaffolder = template engine. Output: full new-service / new-tenant artifact with day-1 governance."),
    },
    before_after_before='<p>Pre-Backstage: ownership in spreadsheets / Slack / nobody-knows. Docs in scattered wikis. New service = manual setup ticket. Plugins absent or per-tool dashboards.</p>',
    before_after_after='<p>Backstage: Catalog is source of truth. TechDocs from repos. Scaffolder ships golden paths. Plugins surface every tool in one place. Service page is the developer\'s home.</p>',
    before_after_caption='<p class="ba-caption"><em>One portal; auto-discovered; doc-as-code; templated.</em></p>',
    analogy_intro_html='''<p>The Catalog Drawer in K-Workshop holds index cards for every tool, every blueprint, every artifact. The card lists who built it, who owns it, what it does, where its docs live (TechDocs cabinet), how to make a new one (Scaffolder template), and which tools integrate (plugins).</p>
    <p>Apprentices flip through the drawer; Master Craftspeople keep it current.</p>''',
    translation_rows=[
        ("Catalog Drawer", "Backstage Catalog"),
        ("Index card", "catalog-info.yaml"),
        ("Tool / blueprint / artifact", "Component / API / Resource / System / Domain"),
        ("Docs cabinet", "TechDocs (per-repo MkDocs)"),
        ("Make-new template", "Scaffolder template"),
        ("Tool integrations", "Plugins (Argo CD / K8s / PagerDuty / etc.)"),
        ("Programmatic queries", "Software Catalog API"),
    ],
    analogy_stops="Index cards are physical; Backstage entities live in a database fed from Git. Stale catalog entries point to vanished services unless cleanup is automated.",
    eli5="A drawer of index cards for everything in the workshop. The cards say who owns it, where the docs are, how to make a new one. Anyone can open the drawer and find what they need.",
    eli10="<strong>Catalog</strong>: every Component / API / Resource / System / Domain registered via catalog-info.yaml. <strong>TechDocs</strong>: per-repo MkDocs auto-built + served centrally. <strong>Scaffolder</strong>: template engine generating new repos + manifests + catalog registration. <strong>Plugins</strong>: 100+ integrations (Argo CD / K8s / Datadog / PagerDuty / cloud / etc.). <strong>Software Catalog API</strong>: REST + GraphQL for programmatic queries.",
    scenarios=[
        Scenario(name="3-AM ownership lookup", body="On-call sees a failing Service; Backstage Catalog → owner + Slack channel + on-call rotation in 10 seconds. Pre-Backstage: 30-min Slack hunt. Time-to-mitigate cut materially."),
        Scenario(name="Auto-discovery from GitHub org", body="200-repo org enables Backstage GitHub integration; existing repos with catalog-info.yaml appear automatically; new repos appear within 30 min. Catalog is current without manual maintenance."),
        Scenario(name="Scaffolder template — new microservice", body="\"New Go service\" template ships repo + Helm + CI + observability + Argo CD app. Developer answers 5 form questions; first deploy in 10 min; 100 services use the same template — uniformity from day 1."),
        Scenario(name="Stale catalog entries", body="Migration deleted services; catalog still listed them. Postmortem: nightly job verifies repo + Service exist; auto-flag stale entries; PR to delete. Catalog hygiene now automated."),
    ],
    misconceptions=[
        Misconception(myth="\"Backstage is just a service catalog.\"", truth="Catalog is one of four pillars. TechDocs + Scaffolder + Plugins make it an IDP storefront, not just a registry."),
        Misconception(myth="\"Backstage requires a dedicated team to operate.\"", truth="A small platform team (1-3 engineers) can operate Backstage at 100+ services. Hosted Backstage (Spotify Portal, Roadie) trades cost for setup time."),
        Misconception(myth="\"Plugins are optional.\"", truth="Without plugins, Backstage is mostly catalog. Argo CD + Kubernetes + PagerDuty plugins turn the service page into the developer\'s home — that\'s where adoption happens."),
    ],
    flashcards=[
        Flashcard(front="Backstage four pillars?", back="<strong>Catalog</strong>, <strong>TechDocs</strong>, <strong>Scaffolder</strong>, <strong>Plugins</strong>."),
        Flashcard(front="catalog-info.yaml lives where?", back="In each repo. Backstage auto-discovers via GitHub / GitLab integration."),
        Flashcard(front="Catalog entity kinds?", back="<strong>Component</strong> (service), <strong>API</strong> (contract), <strong>Resource</strong> (DB / queue), <strong>System</strong> (collection), <strong>Domain</strong> (collection of Systems), <strong>User / Group</strong>."),
        Flashcard(front="TechDocs build pattern at scale?", back="Per-PR CI builds MkDocs static site → S3 / GCS. Backstage TechDocs Backend serves from object storage. No central build bottleneck."),
        Flashcard(front="Scaffolder steps?", back="<code>fetch:template</code> (skeleton), <code>publish:github</code> (create repo), <code>catalog:register</code> (add to Catalog), custom actions for org-specific (cluster onboarding PR, Crossplane Claim, etc.)."),
        Flashcard(front="Most-used Backstage plugins?", back="Argo CD (deploy status), Kubernetes (cluster view), PagerDuty (on-call), GitHub Actions (CI), Datadog / Grafana (dashboards), Snyk (security), AWS / Azure / GCP."),
        Flashcard(front="Software Catalog API — what does it expose?", back="REST + GraphQL access to all catalog entities. CI pipelines + downstream tools query \"who owns this commit?\" \"what tier?\" \"which APIs does this consume?\""),
        Flashcard(front="Hosted Backstage options?", back="<strong>Spotify Portal</strong> (Spotify-managed), <strong>Roadie</strong> (Backstage-as-a-service). Trade self-host setup cost for ongoing fee."),
    ],
    quizzes=[
        Quiz(prompt="A 50-engineer team wants Backstage live in 30 days. Walk priorities.",
            answer="Week 1: deploy Backstage (Helm or hosted); enable GitHub/GitLab integration; catalog auto-discovery seeds. Week 2: install Kubernetes + Argo CD + PagerDuty plugins; configure org\'s SSO. Week 3: write 1-2 Scaffolder templates (new service, new namespace); write a TechDocs example for one repo + train teams. Week 4: rollout — every service team registers catalog-info.yaml + ships docs in repos. Measure NPS at 60 days; iterate next quarter."),
        Quiz(prompt="A Scaffolder template needs to call Crossplane to create a new namespace + Postgres DB. Walk steps.",
            answer="Template steps: (1) <code>fetch:template</code> renders catalog-info.yaml + Postgres CR YAML. (2) Custom action <code>github:openPr</code> opens a PR in the GitOps repo with the namespace + Postgres CRs. (3) PR auto-merges (or human-approved). (4) Argo CD syncs; Crossplane reconciles; namespace + DB materialize. (5) Backstage shows status via Argo CD + Crossplane plugins on the new service\'s page."),
        Quiz(prompt="Leadership says: \"why pay for Backstage when GitHub already shows ownership?\" Defend.",
            answer="\"<strong>GitHub shows code ownership; Backstage shows operational reality.</strong> Three reasons: (1) <strong>Cross-tool surface</strong>: GitHub is one tab; Backstage shows Argo CD deploy status + K8s cluster view + PagerDuty on-call + Datadog metrics + Snyk vulns + cost data on one service page. (2) <strong>Doc + template surface</strong>: TechDocs centralizes docs; Scaffolder enforces day-1 quality. GitHub does neither at scale. (3) <strong>Searchable + queryable</strong>: \"all production-tier Java services owned by team-X with critical CVEs\" answerable via Catalog API. GitHub can\'t. <strong>Cost</strong>: hosted Backstage ~$10-15/dev/mo; self-hosted is one engineer of operational time. <strong>Value</strong>: every developer\'s daily home page; the platform team\'s product surface.\"", cyoa=True, cyoa_tag="how the platform engineer defended Backstage"),
    ],
    glossary=[
        GlossaryItem(name="Backstage", definition="CNCF Incubating developer portal originated by Spotify. Catalog + TechDocs + Scaffolder + Plugins."),
        GlossaryItem(name="catalog-info.yaml", definition="Per-repo file declaring entity (Component / API / etc.) + owner + tier. Auto-discovered by Backstage."),
        GlossaryItem(name="TechDocs", definition="Per-repo MkDocs / AsciiDoc; built in CI; served centrally via Backstage TechDocs Backend."),
        GlossaryItem(name="Scaffolder", definition="Template engine generating new repos + manifests + catalog registration from parameters."),
        GlossaryItem(name="Software Catalog API", definition="REST + GraphQL access to all entities. CI + downstream tools query for ownership + tier + dependencies."),
        GlossaryItem(name="Backstage plugin", definition="React + backend module integrating Backstage with external tools (Argo CD / K8s / PagerDuty / etc.)."),
        GlossaryItem(name="Hosted Backstage", definition="Spotify Portal / Roadie — managed Backstage; trades cost for setup time."),
        GlossaryItem(name="Domain", definition="Catalog entity grouping Systems. Top of the hierarchy."),
    ],
    recap_lead="Backstage = Catalog (source of truth) + TechDocs (doc-as-code) + Scaffolder (golden paths) + Plugins (every tool integrated). The IDP\'s storefront.",
    recap_next='<strong>Next — P3: Crossplane v2.</strong> Providers + Compositions + XRDs + Functions + Configuration packages. Platform-as-API.',
)
