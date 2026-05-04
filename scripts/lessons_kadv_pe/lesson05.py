"""K-ADV-PE P5 — Tenant onboarding + resource templates + cost controls + service catalogs."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Tenant onboarding pipeline."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Apprentice Intake · K-Workshop — templated tenancy</text><rect x="40" y="70" width="170" height="100" rx="10" fill="#5DCAA5"/><text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Backstage form</text><text x="125" y="108" text-anchor="middle" font-size="9" fill="#1F2433">name + tier + cost-center</text><rect x="225" y="70" width="170" height="100" rx="10" fill="#3F4A5E"/><text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">XTenantNamespace</text><text x="310" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">RBAC + NetPol + Quota</text><rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900"/><text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">resource templates</text><text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">per-tier defaults</text><rect x="595" y="70" width="125" height="100" rx="10" fill="#5A6B81"/><text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">cost controls</text><text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">label + budget</text></svg>"""


LESSON = LessonSpec(
    num="05", title_short="tenant onboarding + cost", title_full="P5 · Tenant Onboarding + Resource Templates + Cost Controls + Service Catalogs",
    title_html="K-ADV-PE P5 · Tenant Onboarding", module_eyebrow="Module P5 · Apprentice Intake — templated tenancy",
    hero_sub_html='Tenant onboarding via Backstage form → Crossplane Claim → GitOps PR → namespace ready in minutes. <strong>Resource templates</strong> per tier (gold / silver / bronze): different Quota + NetPol + LimitRange + observability defaults. <strong>Cost controls</strong>: cost-center labels on every Pod; budget alerts via OpenCost / Kubecost. <strong>Service catalogs</strong>: tenants browse + provision pre-approved DBs / queues / Buckets via XRDs.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Cost report shows one tenant\'s namespace consumed $40k unbudgeted. <em>No quota cap; no cost label; no budget alert</em>. Today\'s lesson: every tenant onboarding ships with quota + cost label + budget alert from day-1.",
    stamp_html="<strong>Tenant onboarding via templated Crossplane Claim. Tiers + Quotas + cost labels + budget alerts baked in. Service catalog of pre-approved resources via XRDs. Day-1 economic governance.</strong>",
    district_pin="kpe-bench05", district_label="Apprentice Intake",
    sections=[
        Section(eyebrow="Section 1.1 · onboarding flow", h2="Form → Claim → PR → namespace",
            body_html="""    <p>Step 1: <strong>Backstage Scaffolder form</strong> — tenant name, owner, tier (gold/silver/bronze), cost-center, expected workload class.</p>
    <p>Step 2: <strong>Crossplane Claim</strong> renders Namespace + RoleBinding (per OIDC group) + NetworkPolicy default-deny + ResourceQuota + LimitRange + cost label + Backstage Catalog entry.</p>
    <p>Step 3: <strong>GitOps PR</strong> auto-opened against fleet repo; policy gates run; auto-merge for trusted; human-approved for novel patterns.</p>
    <p>Step 4: <strong>Argo CD ApplicationSet</strong> picks up the new namespace claim; reconciles; namespace materializes within minutes."""),
        Section(eyebrow="Section 1.2 · resource tiers", h2="Gold / silver / bronze defaults",
            body_html="""    <p>Tiers encode per-tenant resource defaults:</p>
    <ul>
      <li><strong>Gold</strong>: ResourceQuota 50 vCPU + 100 GiB; PriorityClass guaranteed; multi-AZ NodeAffinity; HPA + PDB defaults; 99.95% SLO.</li>
      <li><strong>Silver</strong>: 20 vCPU + 40 GiB; standard PriorityClass; single-AZ tolerated; 99.9% SLO.</li>
      <li><strong>Bronze</strong>: 5 vCPU + 10 GiB; low PriorityClass; preemptible nodes OK; 99% SLO.</li>
    </ul>
    <p>Tiers map to cost: gold = ~5×bronze. Tenant chooses + accepts the budget at intake."""),
        Section(eyebrow="Section 1.3 · cost controls",
            h2="Labels + OpenCost / Kubecost + budget alerts",
            body_html="""    <p><strong>Cost label</strong>: every Pod / Service / PVC carries <code>cost-center</code> + <code>tenant</code> labels (mutating webhook injects if missing).</p>
    <p><strong>OpenCost / Kubecost</strong>: aggregate cloud bill + per-Pod utilization; report cost per cost-center / tenant / namespace. Backstage plugin surfaces in service page.</p>
    <p><strong>Budget alerts</strong>: per-tenant monthly budget; OpenCost emits Slack/email at 50% / 75% / 95% / 100% of budget.</p>
    <p><strong>Hard caps</strong>: ResourceQuota enforces; tenant\'s requests cannot exceed. Hard cap + budget alert = no cost surprises."""),
        Section(eyebrow="Section 1.4 · service catalog", h2="XRDs as the menu of pre-approved resources",
            body_html="""    <p><strong>Service catalog</strong>: Backstage shows XRDs (XPostgresInstance, XBucket, XQueue, XCert) as service-template entries. Tenants browse; click \"Provision\"; Backstage form → Crossplane Claim → resource ships.</p>
    <p>Catalog entries include: schema (what to fill in), tier defaults, cost estimate per tier, owning team, runbook link.</p>
    <p>Pattern: every recurring infra request becomes a catalog entry; tenant self-service replaces the platform-team ticket."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="What does the Backstage form trigger?",
            options=[("A direct kubectl apply.", False), ("A Crossplane Claim + GitOps PR + Argo CD reconcile.", True), ("A Slack message.", False)],
            feedback="Form → Claim → PR → Argo CD = templated path; auditable + reversible."),
        3: PauseCheck(question="Why ResourceQuota + budget alert (not just one)?",
            options=[("Belt and suspenders.", False), ("Quota = hard cap (preventive); budget alert = early warning (informational).", True), ("Required by K8s.", False)],
            feedback="Hard cap stops cost; alert warns before cap. Both required for graceful + safe."),
    },
    before_after_before='<p>Pre-templated tenancy: each new tenant 2-week setup; bespoke YAML; no cost labels; surprise bills.</p>',
    before_after_after='<p>Tenant onboarding form → Claim → PR → namespace in &lt; 1 day. Tiers encode quota + cost defaults. OpenCost surfaces per-tenant cost; budget alerts; service catalog of pre-approved resources.</p>',
    before_after_caption='<p class="ba-caption"><em>Day-1 governance + economics + service catalog. New tenant in &lt; 1 day.</em></p>',
    analogy_intro_html='''<p>Apprentice Intake is the workshop\'s door. New apprentices fill out the intake form (Backstage); the form picks a tier (gold / silver / bronze) which determines the workspace size + tools issued + budget. The intake clerk (Crossplane Claim) materialises the workspace. The accountant (OpenCost) tracks every apprentice\'s consumed materials; alarms when budget approaches. A menu (service catalog) lets apprentices order pre-approved tools without back-and-forth.</p>''',
    translation_rows=[
        ("Apprentice Intake form", "Backstage Scaffolder form"),
        ("Tier (gold/silver/bronze)", "Resource tier (Quota + NetPol + PriorityClass)"),
        ("Intake clerk", "Crossplane Claim"),
        ("Workspace materialisation", "Namespace + RBAC + NetPol + Quota + LimitRange"),
        ("Accountant\'s ledger", "OpenCost / Kubecost"),
        ("Budget alarm", "Slack/email at 75% / 95% / 100% of budget"),
        ("Pre-approved tool menu", "Service catalog of XRDs"),
    ],
    analogy_stops="A real apprentice intake is one-time; tenant tiers can be promoted (silver → gold) via PR — graceful upgrade path matters.",
    eli5="Fill out the form. Pick a tier. The workspace + tools + budget materialize. The accountant warns you before you blow the budget.",
    eli10="<strong>Onboarding</strong>: Backstage form → Crossplane Claim → GitOps PR → Argo CD. <strong>Tiers</strong>: gold/silver/bronze with Quota + PriorityClass + NetPol defaults. <strong>Cost</strong>: cost-center label + OpenCost / Kubecost + budget alerts. <strong>Service catalog</strong>: XRDs as menu items in Backstage.",
    scenarios=[
        Scenario(name="New tenant in 30 minutes", body="A team needs a new namespace; form → Claim → PR → Argo CD reconciles in 25 min. Day-1 quota + cost label + NetPol + RBAC; team starts deploying immediately."),
        Scenario(name="Budget alert caught runaway dev workload", body="A dev image had a memory leak; namespace approached 100% of monthly budget by mid-month. OpenCost alarm at 75%; team paged; fixed; budget recovered."),
        Scenario(name="Tier promotion via PR", body="A silver tenant\'s prod workload outgrew tier; team PRs the Claim with tier=gold; quota + observability defaults upgrade overnight."),
        Scenario(name="Outage — no quota; surprise $40k bill", body="Pre-controls, one tenant ran 200 unconstrained Pods; cloud bill spiked. Postmortem: ResourceQuota + cost label mandatory; budget alerts wired; never again."),
    ],
    misconceptions=[
        Misconception(myth="\"Cost labels don\'t need to be enforced.\"", truth="Without a mutating webhook adding cost-center labels, tenants forget. OpenCost / Kubecost can\'t allocate; cost surprises follow."),
        Misconception(myth="\"Service catalog is fancy YAML.\"", truth="Service catalog = XRDs + Backstage Scaffolder integration. Tenants browse + click; Crossplane provisions. Replaces ticket queue + per-resource bespoke."),
        Misconception(myth="\"Tiers are restrictive.\"", truth="Tiers are <em>defaults</em>; tenants pick at intake; promote via PR. Tiers eliminate per-tenant Quota math; PR for the 20% that need different shapes."),
    ],
    flashcards=[
        Flashcard(front="Tenant onboarding pipeline?", back="Backstage form → Crossplane Claim → GitOps PR → Argo CD ApplicationSet → namespace materializes."),
        Flashcard(front="What\'s in a tier definition?", back="ResourceQuota + LimitRange + NetworkPolicy default + PriorityClass + observability defaults + SLO + cost estimate. Per-tier (gold / silver / bronze)."),
        Flashcard(front="Cost label enforcement?", back="Mutating Kyverno webhook injects <code>cost-center</code> + <code>tenant</code> labels on every Pod / Service / PVC. Required for OpenCost allocation."),
        Flashcard(front="OpenCost vs Kubecost?", back="<strong>OpenCost</strong> = open-source CNCF project; foundational. <strong>Kubecost</strong> = vendor product on top with richer dashboards + chargeback features. Both compatible."),
        Flashcard(front="Budget alert thresholds?", back="<strong>50%</strong> info, <strong>75%</strong> Slack, <strong>95%</strong> page on-call, <strong>100%</strong> hard alarm. Per-tenant budgets monthly."),
        Flashcard(front="Service catalog entries — what they list?", back="Schema (XRD spec), tier defaults, cost estimate per tier, owning team, runbook link, last-updated date. Backstage Catalog entries."),
        Flashcard(front="Hard cap vs alert?", back="<strong>ResourceQuota</strong> = hard cap (preventive — apiserver rejects new resource if over). <strong>Budget alert</strong> = informational. Both required."),
        Flashcard(front="Tier promotion — what\'s the path?", back="PR to update Claim spec.tier; Argo CD reconciles; quota + defaults upgrade. ~10 minutes; reversible."),
    ],
    quizzes=[
        Quiz(prompt="A new product team needs a tenant. Walk the day-1 setup.",
            answer="(1) Team fills <strong>Backstage form</strong>: name, owner, tier=silver, cost-center=B-205. (2) <strong>Crossplane Claim</strong> renders namespace + RBAC (binds team\'s OIDC group) + NetPol default-deny + ResourceQuota silver-tier (20vCPU, 40GiB) + LimitRange + cost label + Backstage entry. (3) <strong>GitOps PR</strong>: opened, policy gates run (Kyverno + conftest), auto-merge for trusted. (4) <strong>Argo CD</strong>: ApplicationSet picks up; reconciles; namespace ready in 5 min. (5) <strong>Team starts deploying</strong>: Backstage Scaffolder \"new Go service\" template. <strong>Total time: ~30 min from form to first deploy.</strong>"),
        Quiz(prompt="Tenant\'s monthly bill projects 2× budget mid-month. Walk the response.",
            answer="(1) <strong>OpenCost alarm</strong> fires at 75%; team gets Slack notification. (2) <strong>Investigation</strong>: Kubecost dashboard shows top spenders by Pod/Deployment; identify runaway. (3) <strong>Mitigation</strong>: scale down / right-size requests / fix bug. (4) <strong>If continued</strong>: 95% threshold pages on-call; ResourceQuota stops new Pods at 100%; tenant\'s deployments halted (graceful — not retroactive). (5) <strong>Postmortem</strong>: tenant + platform review; right-size tier (silver → gold? or actually need bronze?); update Claim if appropriate."),
        Quiz(prompt="Leadership says: \"why pay OpenCost? cloud provider\'s billing is enough.\" Defend.",
            answer="\"<strong>Cloud bills aggregate by service; OpenCost allocates by Pod / namespace / tenant.</strong> Three reasons: (1) <strong>Allocation</strong>: cloud bill says \"$40k for EC2\"; OpenCost says \"$15k tenant-A, $10k tenant-B, $15k platform.\" Without OpenCost no chargeback. (2) <strong>Real-time</strong>: cloud bills are end-of-month; OpenCost is hourly. Catch runaway in hours, not month-end. (3) <strong>Behavior change</strong>: tenants who see their cost change behavior. Hidden cost = no incentive. <strong>OpenCost is free (CNCF open-source); the install + dashboards are an engineer-week.</strong>\"", cyoa=True, cyoa_tag="how the platform engineer defended OpenCost"),
    ],
    glossary=[
        GlossaryItem(name="Tenant onboarding", definition="Templated workflow creating a new namespace + governance via Backstage + Crossplane + GitOps."),
        GlossaryItem(name="Resource tier", definition="Predefined Quota + NetPol + PriorityClass + observability defaults (gold / silver / bronze)."),
        GlossaryItem(name="ResourceQuota", definition="Hard cap on namespace\'s aggregate Pod requests / limits / counts."),
        GlossaryItem(name="LimitRange", definition="Default + max per-Pod / per-container limits within namespace."),
        GlossaryItem(name="OpenCost", definition="CNCF open-source cost allocation. Aggregates cloud bill + utilization; per-Pod / per-namespace / per-tenant cost."),
        GlossaryItem(name="Kubecost", definition="Vendor product on top of OpenCost — richer dashboards + chargeback + insights."),
        GlossaryItem(name="cost-center label", definition="Mutating-injected label on every Pod / Service / PVC; foundation for OpenCost allocation."),
        GlossaryItem(name="Service catalog", definition="Backstage entries for pre-approved XRDs (DBs / queues / buckets). Tenant browses + provisions."),
        GlossaryItem(name="Tier promotion", definition="PR updating Claim spec.tier; Argo CD reconciles; quota + defaults upgrade."),
    ],
    recap_lead="Tenant onboarding via Backstage + Crossplane + GitOps. Tiers encode defaults. OpenCost / Kubecost surface cost per tenant. Service catalog of pre-approved resources. Day-1 governance + economics.",
    recap_next='<strong>Next — P6: Workload abstractions (Score, OAM, Radius, Humanitec).</strong>',
)
