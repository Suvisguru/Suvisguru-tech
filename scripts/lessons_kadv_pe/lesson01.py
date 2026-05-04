"""K-ADV-PE P1 — IDP foundations + golden paths + self-service namespaces."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="IDP — golden paths + self-service namespaces.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Master Blueprint Library · K-Workshop — platform-as-product</text>
  <rect x="40" y="70" width="170" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">developer = customer</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#1F2433">platform = product</text>
  <rect x="225" y="70" width="170" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">golden paths</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">opinionated templates</text>
  <text x="310" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">repo + CI + manifests</text>
  <rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">self-service NS</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">RBAC + NetPol + Quota</text>
  <text x="495" y="124" text-anchor="middle" font-size="9" fill="#1F2433">templated</text>
  <rect x="595" y="70" width="125" height="100" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">SLO</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">platform contract</text>
</svg>"""


LESSON = LessonSpec(
    num="01",
    title_short="IDP + golden paths",
    title_full="P1 · IDP Foundations + Golden Paths + Self-Service Namespaces",
    title_html="K-ADV-PE P1 · IDP Foundations",
    module_eyebrow="Module P1 · Master Blueprint Library — platform-as-product",
    hero_sub_html='<strong>Internal Developer Platform (IDP)</strong>: the platform team\'s product; developers are customers. <strong>Golden paths</strong>: opinionated templates that ship a service from \"new repo\" to \"production-ready\" with CI + manifests + governance baked in. <strong>Self-service namespaces</strong>: tenants request via portal; namespace + RBAC + NetPol + Quota auto-provisioned. <strong>Platform SLOs</strong>: published like a vendor SLA — uptime, deploy latency, capacity headroom.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A new team needed a service in production by morning; platform team is asleep; team copy-pasted YAML from another team\'s repo + applied manually; no NetPol, no Quota, half-broken RBAC. <em>Without self-service + golden paths, every onboarding is bespoke.</em> Today\'s lesson: build the IDP so onboarding is templated + self-service.",
    stamp_html="<strong>IDP = platform-as-product. Golden paths cover the 80% common cases (new service, new tenant, new namespace). Self-service via Backstage + Crossplane. Platform SLOs published. Platform team measures customer (developer) NPS.</strong>",
    district_pin="kpe-bench01",
    district_label="Master Blueprint Library",
    sections=[
        Section(
            eyebrow="Section 1.1 · platform-as-product",
            h2="Developer is the customer; platform team owns the experience",
            body_html="""    <p><strong>IDP shift</strong>: platform team is no longer \"infra ops\" or \"K8s admins\" — they\'re building a product whose users are developers. Three implications:</p>
    <ul>
      <li><strong>Customer feedback loop</strong>: developer NPS, time-to-first-deploy, time-to-incident-resolution measured. Quarterly developer surveys.</li>
      <li><strong>Roadmap discipline</strong>: features prioritised by customer pain, not infrastructure preferences.</li>
      <li><strong>Documentation as deliverable</strong>: TechDocs / Backstage portal as good as any vendor\'s docs.</li>
    </ul>
    <p>Outcome: developers don\'t \"file tickets with infra\" — they consume self-service. Platform team scales beyond head-count by templating common cases.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · golden paths",
            h2="Opinionated templates — the 80% case automated",
            body_html="""    <p><strong>Golden path</strong>: a pre-built, opinionated way to do a common thing. \"New microservice in Go\" → repo with directory layout + Dockerfile + Helm chart + CI workflow + observability + GitOps onboarding all wired. Developer fills in business logic.</p>
    <p>Implemented via <strong>Backstage Scaffolder</strong>: template + parameters + steps; generates repo + commits initial files + opens PR for cluster onboarding. Developer answers 5 questions; first deploy in 10 minutes.</p>
    <p>Common golden paths: new service (per language), new tenant namespace, new database (Postgres / MySQL / DynamoDB), new ingress / API endpoint, new observability dashboard. <strong>The platform team owns templates</strong>; updates propagate to new services automatically.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · self-service namespaces",
            h2="Templated tenant onboarding with governance baked in",
            body_html="""    <p>Manual namespace creation is the platform-team bottleneck. <strong>Self-service</strong>:</p>
    <ul>
      <li><strong>Backstage form</strong> or CLI command: tenant name, owner, tier (gold / silver / bronze), cost-center.</li>
      <li><strong>Crossplane Claim</strong> renders Namespace + RoleBinding (per OIDC group) + NetworkPolicy default-deny + ResourceQuota + LimitRange + service catalog entry.</li>
      <li><strong>GitOps PR</strong>: human-approved (or automated for trusted requesters); merge → namespace materializes within minutes.</li>
    </ul>
    <p><strong>Day-1 governance is day-0</strong>: the new namespace has every guardrail from the moment it exists. No \"we\'ll add NetworkPolicy later.\"</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · platform SLOs",
            h2="Publish the platform\'s contract like a vendor",
            body_html="""    <p>Platform team publishes <strong>SLOs</strong>:</p>
    <ul>
      <li><strong>Cluster availability</strong>: 99.9% / 99.95% / 99.99% — different per tier.</li>
      <li><strong>Deploy latency</strong>: P95 deploy &lt; 5 min from git push to running.</li>
      <li><strong>Capacity headroom</strong>: never &lt; 20% free; auto-scale before saturation.</li>
      <li><strong>Onboarding latency</strong>: P95 new service &lt; 30 min; new tenant &lt; 1 day.</li>
      <li><strong>Incident response</strong>: P95 detect &lt; 5 min; respond &lt; 15 min; resolve per severity.</li>
    </ul>
    <p>Visible in Backstage; quarterly review with stakeholders; failures trigger postmortem + roadmap items. <em>The platform is held to a contract; tenants know what to expect.</em></p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="What\'s the IDP\'s fundamental shift?",
            options=[
                ("Adopting Kubernetes.", False),
                ("Treating developers as customers; platform team as product team.", True),
                ("Adopting GitOps.", False),
            ],
            feedback="The shift is mindset + practice — measure developer NPS, prioritise by customer pain, treat docs as deliverables. K8s + GitOps are tools; IDP is the operating model.",
        ),
        3: PauseCheck(
            question="Why are platform SLOs published?",
            options=[
                ("Compliance.", False),
                ("Tenants know what to expect; platform team has a measurable contract.", True),
                ("Required by K8s.", False),
            ],
            feedback="Visible SLOs let tenants plan around platform capabilities; platform team operates against a measurable contract; failures trigger postmortems + roadmap items.",
        ),
    },
    before_after_before='<p>Pre-IDP, every team built their own platform pieces. Platform team filed tickets. Onboarding took weeks. Bespoke YAML across teams. Platform team scaled with head-count, not leverage.</p>',
    before_after_after='<p>IDP: platform-as-product; golden paths cover 80%; self-service via Backstage + Crossplane; SLOs published. Onboarding in 1 day; platform team scales beyond head-count.</p>',
    before_after_caption='<p class="ba-caption"><em>Treat developers as customers; ship platform features as a product.</em></p>',
    analogy_intro_html='''<p>K-Workshop\'s Master Blueprint Library shelves hundreds of pre-drafted blueprints. Apprentices (developers) walk in with a request — \"I need a wagon\" — and pick the closest blueprint from the shelf. The shop\'s standard tools, materials, and finishes are pre-stocked. The apprentice fills in the wagon\'s specific cargo carrying capacity; the wagon ships in hours, not weeks.</p>
    <p>The Master Craftsperson (platform team) maintains the blueprints + the standard tools. New blueprints are added by customer demand. Each blueprint comes with a sealed contract (SLO) — \"this wagon meets payload X over Y miles before service.\"</p>''',
    translation_rows=[
        ("Master Blueprint Library", "Internal Developer Platform (IDP)"),
        ("Pre-drafted blueprint", "Golden path / Backstage Scaffolder template"),
        ("Apprentice (customer)", "Developer"),
        ("Master Craftsperson", "Platform engineer"),
        ("Pre-stocked tools + materials", "Standard CI + manifests + observability"),
        ("Sealed contract (SLO)", "Platform SLO (uptime + latency + headroom)"),
        ("Blueprint shelf catalog", "Backstage catalog"),
        ("New blueprint by request", "New golden path / template via PR"),
    ],
    analogy_stops="A real blueprint is paper; golden-path templates evolve as the platform evolves. Old templates produce old shapes; refresh templates as standards drift.",
    eli5="A workshop with shelves of pre-drafted blueprints. You walk in, pick the right blueprint, fill in the small bits, your wagon ships. The workshop\'s manager keeps the blueprints fresh.",
    eli10="<strong>IDP</strong> = platform-as-product; developer is the customer. <strong>Golden paths</strong> = opinionated Backstage Scaffolder templates (repo + CI + manifests + observability). <strong>Self-service NS</strong> = Backstage form → Crossplane Claim → GitOps PR → namespace with RBAC + NetPol + Quota. <strong>Platform SLOs</strong>: cluster availability + deploy latency + capacity headroom + onboarding latency + IR.",
    scenarios=[
        Scenario(
            name="Backstage golden path — new service in 10 minutes",
            body="A 200-engineer org adopts Backstage. \"New Go service\" template generates repo + Helm chart + GitHub Actions + observability + Argo CD onboarding. Developer answers 5 questions; first deploy in 10 minutes; quality bar = day-1 production-ready.",
        ),
        Scenario(
            name="Self-service namespace via Crossplane Claim",
            body="A team needs a new namespace. Backstage form: name + owner + tier + cost-center. Crossplane Claim renders Namespace + RoleBinding + NetPol + Quota + service catalog entry. GitOps PR auto-merged after policy gates. Namespace ready in 5 minutes.",
        ),
        Scenario(
            name="Platform SLO drove a roadmap item",
            body="P95 deploy latency degraded over 6 months — Argo CD sync time grew. Platform SLO breach surfaced in quarterly review; Argo CD + cluster-mesh-apiserver upgrade prioritised; SLO recovered next quarter.",
        ),
        Scenario(
            name="Onboarding bottleneck before IDP",
            body="Pre-IDP, each new tenant was 2-week setup; platform team booked solid. Adopted golden paths + Crossplane self-service; new tenant Day-1 to production. Platform team headcount stayed flat as tenant count tripled.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"IDP is just Backstage.\"",
            truth="Backstage is the storefront; IDP is the operating model. Backstage + Crossplane + Argo CD + OPA + golden paths + tenant catalog + SLOs together form the IDP. Backstage alone without the back-end automation is a portal that doesn\'t self-serve.",
        ),
        Misconception(
            myth="\"Self-service means no platform-team review.\"",
            truth="Self-service automates the 80% common case + leaves human-approved PR for the 20% novel cases. Templates have policy gates; deviations escalate to platform team review. Self-service is templated + governed, not unmanaged.",
        ),
        Misconception(
            myth="\"Platform SLOs are vanity metrics.\"",
            truth="SLOs are the platform team\'s product contract. Without them, tenants don\'t know what to expect; platform team has no measurable goal. SLOs drive roadmap + postmortems; vanity vs operational is a question of follow-through.",
        ),
    ],
    flashcards=[
        Flashcard(front="What\'s the IDP\'s definition?", back="<strong>Internal Developer Platform</strong> — the platform team\'s product, with developers as customers. Includes self-service portal (Backstage), automation (Crossplane / Argo CD), policy (OPA / Kyverno), templates, SLOs."),
        Flashcard(front="Golden path — what does it ship?", back="A new repo + manifests + CI + observability + GitOps onboarding for the 80% common case (e.g., new Go service). Developer fills in business logic; platform-quality from day-1."),
        Flashcard(front="Self-service namespace — what auto-provisions?", back="Namespace + RoleBinding (per OIDC group) + NetworkPolicy default-deny + ResourceQuota + LimitRange + service catalog entry. Day-1 governance day-0."),
        Flashcard(front="Five typical platform SLOs?", back="Cluster availability (99.9-99.99%), deploy latency (P95 &lt; 5 min), capacity headroom (≥ 20% free), onboarding latency (P95 &lt; 1 day for new tenant), IR (detect &lt; 5min, respond &lt; 15min)."),
        Flashcard(front="Backstage Scaffolder — input + output?", back="Input: template (skeleton + parameter spec). Output: new repo + commits + initial PR for cluster onboarding. Developer answers form questions; output materializes."),
        Flashcard(front="Why prioritise developer NPS as a metric?", back="Platform team\'s success = developers\' productivity. Low NPS = platform isn\'t serving customers; high NPS = customer adoption. Quarterly survey + open-text feedback drives roadmap."),
        Flashcard(front="What does \"day-1 governance is day-0\" mean?", back="The new namespace / service / tenant has every guardrail from the moment it exists. Platform team doesn\'t add governance later; it\'s baked into the template."),
        Flashcard(front="Three roles in K-Workshop universe?", back="<strong>Master Craftsperson</strong> (platform engineer), <strong>Apprentice</strong> (developer / consumer), <strong>Foreman</strong> (platform operator running the platform)."),
    ],
    quizzes=[
        Quiz(
            prompt="A 100-engineer org with no IDP wants to bootstrap one in 6 months. Walk the priority order.",
            answer="(1) <strong>Backstage portal</strong> month 1: catalog every service; one or two templates; TechDocs from existing repos. Quick value. (2) <strong>Crossplane self-service namespace</strong> month 2: tenant onboarding form + Crossplane Claim + GitOps. (3) <strong>Argo CD ApplicationSets</strong> month 3: fleet GitOps deploy. (4) <strong>OPA / Kyverno guardrails</strong> month 4: PR-time + admission policy gates. (5) <strong>OpenCost + SLOs</strong> month 5: cost transparency + platform contract. (6) <strong>Iterate on developer NPS</strong> month 6+: quarterly survey drives next features. <em>Each step delivers value; sequential adoption avoids big-bang risk.</em>",
        ),
        Quiz(
            prompt="A platform team is buried in tickets — every team files \"please add label X / open SG / create namespace.\" Walk the path out.",
            answer="(1) <strong>Categorise tickets</strong>: top 80% are self-serviceable patterns. Build self-service for those. (2) <strong>Template the recurring 80%</strong>: namespace creation, label additions, NetPol changes, SG changes — each becomes a Crossplane Claim or Backstage Scaffolder template. (3) <strong>Migrate ticket flow</strong>: \"file ticket\" replaced by \"submit Backstage form\"; ticket queue drains. (4) <strong>Reserve human review</strong> for the 20% novel cases. (5) <strong>Measure</strong>: ticket count drops; developer NPS rises; platform team capacity opens for roadmap work. <em>The mindset is: every recurring ticket is a self-service feature you haven\'t built.</em>",
        ),
        Quiz(
            prompt="Leadership says: \"why pay for an IDP team when we already have platform admins?\" Defend.",
            answer="\"<strong>The IDP team produces leverage; admins produce throughput.</strong> Three reasons: (1) <strong>Scale</strong>: admins\' work scales linearly with head-count + ticket volume. IDP team\'s work scales with template adoption — once a golden path ships, every team consumes it without admin intervention. 100 teams onboarded by one template ≠ 100 admin-tickets. (2) <strong>Quality consistency</strong>: bespoke per-team setup drifts; templated setup is uniform. Compliance audits, security findings, incident patterns all benefit from uniformity. (3) <strong>Developer productivity</strong>: time-to-first-deploy drops from weeks to hours. The cost of delay across 100 engineers is enormous; the IDP team\'s salary is small in comparison. <strong>Reframe</strong>: IDP team is product team building leverage; admin team is the IDP\'s past tense. Both can coexist short-term while migrating ticket queue → self-service.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer defended the IDP team",
        ),
    ],
    glossary=[
        GlossaryItem(name="Internal Developer Platform (IDP)", definition="Platform team\'s product; developers are customers. Backstage + Crossplane + Argo CD + OPA + templates + SLOs."),
        GlossaryItem(name="Golden path", definition="Pre-built opinionated template for a common case (new service, new namespace, new database)."),
        GlossaryItem(name="Backstage", definition="Spotify-originated CNCF developer portal. Catalog + TechDocs + Scaffolder + plugins."),
        GlossaryItem(name="Backstage Scaffolder", definition="Template engine generating repos + manifests from parameters."),
        GlossaryItem(name="Self-service namespace", definition="Templated tenant onboarding via Backstage form → Crossplane Claim → GitOps PR."),
        GlossaryItem(name="Platform SLO", definition="Published platform contract: availability + deploy latency + capacity headroom + onboarding latency + IR."),
        GlossaryItem(name="Developer NPS", definition="Net Promoter Score from developer surveys. Platform-team\'s primary customer-success metric."),
        GlossaryItem(name="Day-1 governance day-0", definition="Pattern: every guardrail (RBAC, NetPol, Quota) baked into the template; new resources born compliant."),
        GlossaryItem(name="Platform team", definition="Product team building the IDP. Master Craftsperson role in K-Workshop."),
        GlossaryItem(name="Service catalog", definition="Registry of every service + owner + tier + dependencies. Backstage hosts; auto-populated from repos."),
    ],
    recap_lead="IDP = platform-as-product. Golden paths cover 80%. Self-service via Backstage + Crossplane. Platform SLOs are the contract. Developer NPS is the success metric.",
    recap_next='<strong>Next — P2: Backstage deep dive.</strong> Catalog, TechDocs, Scaffolder, plugins. The IDP storefront.',
)
