"""K-ADV-PE P8 — Capstone: self-service IDP."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Capstone IDP — every K-ADV-PE concept woven."><rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Equipped Workshop · K-Workshop — every K-ADV-PE concept in one IDP</text><rect x="40" y="70" width="130" height="60" rx="10" fill="#3F4A5E"/><text x="105" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Backstage</text><rect x="190" y="70" width="130" height="60" rx="10" fill="#5DCAA5"/><text x="255" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">Crossplane</text><rect x="340" y="70" width="130" height="60" rx="10" fill="#FF9900"/><text x="405" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">Argo CD AS</text><rect x="490" y="70" width="130" height="60" rx="10" fill="#A04832"/><text x="555" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">OPA / Kyverno</text><rect x="640" y="70" width="80" height="60" rx="10" fill="#5A6B81"/><text x="680" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">OAM</text><rect x="40" y="140" width="680" height="60" rx="10" fill="#FBE8DC" stroke="#A04832"/><text x="380" y="162" text-anchor="middle" font-size="11" font-weight="700" fill="#A04832">+ OpenCost + Platform SLOs + tenant onboarding + golden paths</text><text x="380" y="182" text-anchor="middle" font-size="9" font-style="italic" fill="#A04832">developer self-service end-to-end</text></svg>"""


LESSON = LessonSpec(
    num="08", title_short="capstone IDP", title_full="P8 · Capstone — Self-Service IDP",
    title_html="K-ADV-PE P8 · Capstone IDP", module_eyebrow="Module P8 · Equipped Workshop — every K-ADV-PE concept in one architecture",
    hero_sub_html='Reference architecture: <strong>Backstage</strong> portal with catalog + TechDocs + Scaffolder + 100+ plugins; <strong>Crossplane</strong> XRDs as platform API; <strong>Argo CD ApplicationSets</strong> for fleet GitOps; <strong>OPA + Kyverno</strong> guardrails at PR + admission + sync; <strong>Score / OAM</strong> workload abstraction; <strong>OpenCost / Kubecost</strong> chargeback / showback; <strong>Platform SLOs</strong> published; <strong>tenant onboarding</strong> templated; <strong>day-1 governance</strong> baked in; <strong>operational rhythm</strong> (game days + cost reviews + SLO retros).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A new dev needs a service in 30 min. Without an IDP: file ticket, wait days. With this capstone: open Backstage; pick template; fill 5 fields; deploy in 10 min; day-1 governance + cost label + SLO. <em>Today\'s capstone is the workshop fully equipped.</em>",
    stamp_html="<strong>Equipped IDP: Backstage + Crossplane + Argo CD + OPA + Score / OAM + OpenCost + SLOs + tenant onboarding + game-day rhythm. Self-service end-to-end; day-1 governance day-0; new tenant in &lt; 1 day; new service in &lt; 30 min.</strong>",
    district_pin="kpe-bench08", district_label="Equipped Workshop",
    sections=[
        Section(eyebrow="Section 1.1 · the architecture", h2="Storefront + API + GitOps + governance",
            body_html="""    <p><strong>Storefront</strong>: Backstage portal with Catalog (every service registered), TechDocs (per-repo docs), Scaffolder (golden paths), Plugins (Argo CD / K8s / PagerDuty / Datadog / OpenCost / Crossplane / Kubernetes).</p>
    <p><strong>API</strong>: Crossplane XRDs (XPostgresInstance / XBucket / XQueue / XTenantNamespace / XCert) — tenants consume; platform team owns Compositions + Functions + Providers.</p>
    <p><strong>Fleet GitOps</strong>: Argo CD ApplicationSets across all clusters; per-cluster values from labels; ProgressiveSync dev → staging → prod.</p>
    <p><strong>Governance</strong>: OPA + Kyverno gates at PR + admission + sync; PSA Restricted; per-namespace Quota + LimitRange + NetPol; OPA conftest in CI.</p>"""),
        Section(eyebrow="Section 1.2 · self-service flows", h2="Onboard a tenant; ship a service",
            body_html="""    <p><strong>Onboard a tenant</strong>: Backstage form (name + tier + cost-center) → Crossplane XTenantNamespace Claim → GitOps PR auto-merged → Argo CD reconciles → namespace + RBAC + NetPol + Quota + cost label ready in 5 min.</p>
    <p><strong>Ship a new service</strong>: Backstage Scaffolder (\"new Go service\") → repo + Helm + CI + Argo CD App + observability + Score spec generated → first deploy in 10 min.</p>
    <p><strong>Provision infra</strong>: Backstage service catalog → pick XRD (XPostgres) → fill form → Crossplane Claim → GitOps PR → resource ships in minutes.</p>"""),
        Section(eyebrow="Section 1.3 · workload abstraction + observability + cost",
            h2="Score / OAM + OpenCost + dashboards in Backstage",
            body_html="""    <p><strong>Score spec</strong> in every repo: 30-line workload definition; score-helm renders to chart at build; portable to dev/staging/prod targets.</p>
    <p><strong>Observability bundled</strong>: Prometheus + Grafana + Loki + Tempo / X-Ray pre-wired per template; Datadog plugin in Backstage; OpenTelemetry for tracing.</p>
    <p><strong>Cost labels</strong>: Kyverno mutating webhook injects on every Pod / Service / PVC; OpenCost / Kubecost dashboards in Backstage service page; budget alerts via Slack."""),
        Section(eyebrow="Section 1.4 · operational rhythm", h2="Game days + cost reviews + SLO retros",
            body_html="""    <p><strong>Quarterly game days</strong>: simulate platform failure (Argo CD down, Crossplane provider stuck, GitOps PR storm) + measure response.</p>
    <p><strong>Monthly cost review</strong>: top spenders, optimisation playbook adoption, chargeback / showback adjustments.</p>
    <p><strong>Quarterly SLO retro</strong>: any SLO breach? Postmortem. Roadmap items. Stakeholder review.</p>
    <p><strong>Continuous developer NPS</strong>: quarterly survey + open-text feedback drives platform roadmap.</p>
    <p><strong>The architecture is the easy part; the operational rhythm is the discipline that keeps the workshop equipped.</strong>"""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="What\'s the IDP\'s primary success metric?",
            options=[("Number of clusters.", False), ("Developer NPS + time-to-first-deploy + onboarding latency — customer-facing metrics.", True), ("CPU utilization.", False)],
            feedback="IDP is platform-as-product; customer (developer) metrics are primary. Operational metrics (cluster availability) support; developer success is the goal."),
        3: PauseCheck(question="Why are quarterly game days non-optional?",
            options=[("Tradition.", False), ("Untested platform failure modes rot; game days verify runbook + IDP self-heal.", True), ("Required by SOC2.", False)],
            feedback="Game days exercise platform-side failures (Argo CD outage, Crossplane stuck, GitOps PR storm). Time-to-detect / contain measured + improved."),
    },
    before_after_before='<p>Pre-IDP: per-team platform pieces; manual tickets; bespoke tenancy; cost surprises; SLOs aspirational; no game days; reactive ops.</p>',
    before_after_after='<p>Equipped IDP: every K-ADV-PE concept woven. Self-service end-to-end; day-1 governance; cost transparency; SLOs as contract; game days exercise; developer NPS as metric.</p>',
    before_after_caption='<p class="ba-caption"><em>The architecture is widely-known; the operational rhythm is the differentiator.</em></p>',
    analogy_intro_html='''<p>The Equipped Workshop has every blueprint, every tool, every standard part stocked. Apprentices walk in, self-serve. The Master Craftsperson reviews monthly cost reports + quarterly SLO retros + game-day exercises. New apprentice in 30 min from form to ship.</p>''',
    translation_rows=[
        ("Storefront", "Backstage portal"),
        ("Platform API", "Crossplane XRDs"),
        ("Fleet GitOps", "Argo CD ApplicationSets"),
        ("Quality inspectors", "OPA + Kyverno gates (PR + admission + sync)"),
        ("Standard tool kits", "Score / OAM workload abstractions"),
        ("Workshop accounting", "OpenCost / Kubecost"),
        ("Workshop commitments", "Platform SLOs"),
        ("Apprentice intake", "Tenant onboarding (XTenantNamespace)"),
        ("Quarterly drills", "Game days"),
        ("Master Craftsperson reviews", "Quarterly SLO retros + monthly cost review"),
    ],
    analogy_stops="A real workshop has fixed assets; an IDP evolves continuously — new XRDs, new templates, new policies. The capstone is a snapshot; tomorrow it grows.",
    eli5="The complete workshop. Apprentices walk in, fill out a form, ship their wagon. The master keeps the workshop equipped + organized.",
    eli10="<strong>Storefront</strong>: Backstage. <strong>API</strong>: Crossplane XRDs. <strong>GitOps</strong>: Argo CD ApplicationSets + ProgressiveSync. <strong>Governance</strong>: OPA + Kyverno + PSA + Quota. <strong>Workload</strong>: Score / OAM. <strong>Cost</strong>: OpenCost + Kubecost + showback / chargeback. <strong>Contract</strong>: Platform SLOs. <strong>Onboarding</strong>: templated; day-1 governance. <strong>Operational rhythm</strong>: game days + cost reviews + SLO retros + developer NPS.",
    scenarios=[
        Scenario(name="New developer onboarded in 60 minutes", body="Day 1: Backstage account; pick \"new Go service\"; deploy in 10 min; day-1 observability + cost + SLO. Within an hour: producing user-visible feature."),
        Scenario(name="New tenant in 30 minutes", body="Form → Claim → PR → Argo CD reconciles. Namespace + RBAC + NetPol + Quota + cost label + Backstage entry ready."),
        Scenario(name="Quarterly cost review drove behavior", body="Showback dashboards highlighted top spenders; teams adopted Spot + scale-to-zero; aggregate cost dropped 25% over a quarter without platform-team push."),
        Scenario(name="Game day caught Crossplane provider stuck", body="Simulated provider-aws Pod restart loop; Crossplane stuck; tenant Claims pending. Runbook: provider-aws restart; ProviderConfig auth verify; eventual reconcile. Time-to-recover &lt; 15 min; runbook updated."),
    ],
    misconceptions=[
        Misconception(myth="\"This architecture is over-engineered for &lt; 100-engineer teams.\"", truth="Marginal cost of building from day-1 is moderate; cost of retrofitting after the team grows is enormous. Service Catalog template + golden paths from day-1 = engineers grow into the discipline."),
        Misconception(myth="\"Once built, the IDP runs itself.\"", truth="IDP is a product; needs continuous roadmap + customer feedback. Without operational rhythm + dev NPS, the IDP rots."),
        Misconception(myth="\"Backstage alone is the IDP.\"", truth="Backstage is the storefront; Crossplane is the API; Argo CD is the runtime; OPA + Kyverno are the gates; OpenCost is the accounting; SLOs are the contract. Together they form the IDP."),
    ],
    flashcards=[
        Flashcard(front="IDP\'s seven core elements?", back="Backstage + Crossplane + Argo CD + OPA / Kyverno + Score / OAM + OpenCost / Kubecost + Platform SLOs."),
        Flashcard(front="Day-1 governance day-0 — what does it mean?", back="Every guardrail (RBAC, NetPol, Quota, cost label, observability) baked into templates. New resources born compliant."),
        Flashcard(front="Tenant onboarding pipeline in capstone?", back="Backstage form → Crossplane XTenantNamespace Claim → GitOps PR → Argo CD reconciles → namespace + RBAC + NetPol + Quota + cost label ready in 5 min."),
        Flashcard(front="New service onboarding pipeline?", back="Backstage Scaffolder → repo + Helm + CI + Argo CD App + observability + Score spec → first deploy in 10 min."),
        Flashcard(front="Operational rhythm?", back="Quarterly game days + monthly cost review + quarterly SLO retro + continuous developer NPS. The discipline that keeps the IDP equipped."),
    ],
    quizzes=[
        Quiz(prompt="Walk a new engineer through the IDP in 5 minutes.",
            answer="\"Three ways into the workshop. (1) <strong>Backstage portal</strong>: catalog + docs + scaffolder + plugins; daily home page. (2) <strong>Crossplane XRDs</strong>: kubectl apply a Claim for a Postgres / Bucket / Queue / Namespace. (3) <strong>Score spec</strong>: in your repo, declare workload + dependencies; rendered to K8s by score-helm. <strong>Day-1 governance</strong>: every namespace + service has RBAC + NetPol + Quota + cost label baked in. <strong>Cost transparency</strong>: per-team cost in Slack weekly. <strong>SLOs</strong>: published; we hit them or postmortem. <strong>Game days quarterly</strong>; cost reviews monthly; SLO retros quarterly. <strong>NPS survey</strong>: tell us what\'s broken — we ship roadmap from your feedback.\""),
        Quiz(prompt="Leadership says: \"build IDP this quarter.\" Defend phasing.",
            answer="\"<strong>Phased adoption beats big-bang.</strong> Phasing: (1) Q1 — Backstage portal + Catalog auto-discovery + 1 Scaffolder template. Quick value; visible portal. (2) Q2 — Crossplane self-service namespace + Argo CD ApplicationSet for a few apps. (3) Q3 — OPA + Kyverno gates + tenant onboarding flow. (4) Q4 — OpenCost + SLOs + workload abstraction. Each step is 1-quarter; each delivers value; bug-budget for course-correct. Big-bang quarter = months of build, no value, high risk.\"", cyoa=True, cyoa_tag="how the platform engineer phased the IDP"),
        Quiz(prompt="The CFO sees IDP team is 5 engineers. \"Why?\" Defend.",
            answer="\"<strong>Five engineers serving 200 developers = 1:40 leverage.</strong> Without IDP, those 200 devs each spend ~10% on platform-glue work — equivalent to 20 dev-engineers wasted. IDP team\'s 5 = net 15 engineer-equivalents added. Plus quality (uniform governance) + speed (10-min new service) + cost (cost transparency drives 20% bill reduction). <strong>Net</strong>: IDP team pays for itself in saved engineer-time + reduced cloud bill within 1 quarter. Not overhead — multiplier.\""),
    ],
    glossary=[
        GlossaryItem(name="Equipped IDP", definition="Backstage + Crossplane + Argo CD + OPA + Score/OAM + OpenCost + SLOs + tenant onboarding + game-day rhythm."),
        GlossaryItem(name="Day-1 governance", definition="RBAC + NetPol + Quota + cost label + observability baked into onboarding templates."),
        GlossaryItem(name="Service catalog (capstone)", definition="Backstage entries for XRDs (XPostgres / XBucket / XQueue / XCert); tenants browse + provision."),
        GlossaryItem(name="ProgressiveSync (capstone)", definition="Per-cluster staged rollout with health gates; dev → staging → prod waves."),
        GlossaryItem(name="Operational rhythm", definition="Game days + cost reviews + SLO retros + dev NPS surveys on cadence."),
        GlossaryItem(name="Developer NPS", definition="Quarterly customer-success metric for the IDP team; drives roadmap."),
        GlossaryItem(name="Time-to-first-deploy", definition="From new dev signup to first user-visible feature shipping. Capstone target: &lt; 1 day."),
        GlossaryItem(name="Time-to-onboard-tenant", definition="From form submit to namespace ready. Capstone target: &lt; 5 min."),
    ],
    recap_lead="Equipped IDP: Backstage + Crossplane + Argo CD + OPA + Score / OAM + OpenCost + SLOs + tenant onboarding + operational rhythm. Self-service end-to-end; day-1 governance; new tenant in &lt; 1 day; new service in &lt; 30 min.",
    recap_next='<strong>K-ADV-PE complete.</strong> 8 modules. From IDP foundations (P1) to capstone (P8). Next K-ADV course: <em>K-ADV-AI</em> (K-Observatory) or per founder direction.',
    architecture_svg='''<svg viewBox="0 0 760 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="K-ADV-PE capstone IDP: Backstage + Crossplane + Argo CD + OPA + Score/OAM + OpenCost + SLOs woven into self-service IDP.">
  <rect x="10" y="10" width="740" height="260" rx="12" fill="#FBF7F0" stroke="#7F5A2A"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">K-ADV-PE CAPSTONE · SELF-SERVICE INTERNAL DEVELOPER PLATFORM</text>
  <rect x="20" y="50" width="220" height="60" rx="6" fill="#3F4A5E"/>
  <text x="130" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Backstage (storefront)</text>
  <text x="130" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">Catalog + TechDocs + Scaffolder</text>
  <text x="130" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">+ 100 plugins (Argo CD / K8s / PD)</text>
  <line x1="240" y1="80" x2="270" y2="80" stroke="#5A4F45" stroke-width="2" marker-end="url(#aP8)"/>
  <defs><marker id="aP8" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><polygon points="0 0, 10 5, 0 10" fill="#5A4F45"/></marker></defs>
  <rect x="270" y="50" width="220" height="60" rx="6" fill="#5DCAA5"/>
  <text x="380" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Crossplane v2 (platform API)</text>
  <text x="380" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">XRDs · Compositions · Functions</text>
  <text x="380" y="100" text-anchor="middle" font-size="8" fill="#1F2433">XPostgres · XBucket · XTenantNS</text>
  <line x1="490" y1="80" x2="520" y2="80" stroke="#5A4F45" stroke-width="2" marker-end="url(#aP8)"/>
  <rect x="520" y="50" width="220" height="60" rx="6" fill="#FF9900"/>
  <text x="630" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Argo CD ApplicationSets</text>
  <text x="630" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">fleet GitOps</text>
  <text x="630" y="100" text-anchor="middle" font-size="8" fill="#1F2433">+ ProgressiveSync</text>
  <rect x="20" y="125" width="220" height="55" rx="6" fill="#A04832"/>
  <text x="130" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">OPA + Kyverno guardrails</text>
  <text x="130" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">PR-time + admission + sync</text>
  <text x="130" y="174" text-anchor="middle" font-size="8" fill="#FBE8DC">PolicyReport unified</text>
  <rect x="270" y="125" width="220" height="55" rx="6" fill="#5A6B81"/>
  <text x="380" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Score / OAM workload abstraction</text>
  <text x="380" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">developer-facing spec</text>
  <text x="380" y="174" text-anchor="middle" font-size="8" fill="#FBE8DC">portable to any target</text>
  <rect x="520" y="125" width="220" height="55" rx="6" fill="#1F8A60"/>
  <text x="630" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">OpenCost + Kubecost</text>
  <text x="630" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">per-tenant chargeback</text>
  <text x="630" y="174" text-anchor="middle" font-size="8" fill="#FBE8DC">budget alerts</text>
  <rect x="20" y="195" width="720" height="65" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="215" text-anchor="middle" font-size="11" font-weight="700" fill="#A04832">Tenant onboarding pipeline · Platform SLOs published · Game days quarterly</text>
  <text x="380" y="231" text-anchor="middle" font-size="9" fill="#5A4F45" font-style="italic">form → Crossplane Claim → GitOps PR → Argo CD reconciles → namespace ready &lt; 5 min</text>
  <text x="380" y="247" text-anchor="middle" font-size="9" fill="#5A4F45">Day-1 governance baked in (RBAC + NetPol + Quota + cost label) · Developer NPS measured</text>
</svg>''',
    architecture_caption='Equipped IDP: Backstage storefront + Crossplane platform API + Argo CD fleet GitOps + OPA/Kyverno guardrails + Score/OAM workload abstraction + OpenCost chargeback. Tenant onboarding templated; day-1 governance day-0; platform SLOs published; game days quarterly.',
)
