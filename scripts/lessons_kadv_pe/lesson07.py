"""K-ADV-PE P7 — Platform SLOs + chargeback / showback (OpenCost / Kubecost)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Platform SLOs + chargeback."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Workshop Accounting · K-Workshop — platform contract + cost transparency</text><rect x="40" y="70" width="200" height="100" rx="10" fill="#5DCAA5"/><text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Platform SLOs</text><text x="140" y="108" text-anchor="middle" font-size="9" fill="#1F2433">availability + latency + headroom</text><rect x="260" y="70" width="200" height="100" rx="10" fill="#3F4A5E"/><text x="360" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">OpenCost / Kubecost</text><text x="360" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">per-Pod cost</text><rect x="480" y="70" width="240" height="100" rx="10" fill="#FF9900"/><text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Chargeback / showback</text><text x="600" y="108" text-anchor="middle" font-size="9" fill="#1F2433">per team / cost-center</text></svg>"""


LESSON = LessonSpec(
    num="07", title_short="SLOs + chargeback", title_full="P7 · Platform SLOs + Chargeback / Showback (OpenCost / Kubecost)",
    title_html="K-ADV-PE P7 · SLOs + Chargeback", module_eyebrow="Module P7 · Workshop Accounting — platform contract + cost transparency",
    hero_sub_html='<strong>Platform SLOs</strong>: published like vendor SLAs — cluster availability, deploy latency, capacity headroom, onboarding latency, IR. Reviewed quarterly with stakeholders. <strong>OpenCost / Kubecost</strong>: aggregate cloud bill + per-Pod utilization → cost per cost-center / tenant / namespace. <strong>Chargeback</strong> (real bill to team) vs <strong>showback</strong> (visible cost without billing). Behavior change: tenants see their cost, self-tune, request cheaper instance types / smaller Quotas.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. End of fiscal year; cloud bill 40% over budget. Finance can\'t allocate to teams; engineering says \"not us\"; everyone\'s right + wrong. <em>Without chargeback / showback, there\'s no incentive to optimise + no audit trail of who\'s using what.</em> Today\'s lesson: platform SLOs + cost transparency = healthy platform economics.",
    stamp_html="<strong>Platform SLOs are the contract; OpenCost / Kubecost surfaces cost per team. Chargeback (real bill) drives optimisation; showback (visible cost) is the gentle nudge. Both pay for themselves in tenant-driven cost reduction.</strong>",
    district_pin="kpe-bench07", district_label="Workshop Accounting",
    sections=[
        Section(eyebrow="Section 1.1 · platform SLOs", h2="Publish the contract; review quarterly",
            body_html="""    <p>Platform team publishes SLOs:</p>
    <ul>
      <li><strong>Cluster availability</strong>: per tier; 99.9 / 99.95 / 99.99%.</li>
      <li><strong>Deploy latency</strong>: P95 git push → running &lt; 5 min.</li>
      <li><strong>Capacity headroom</strong>: ≥ 20% free; auto-scale before saturation.</li>
      <li><strong>Onboarding latency</strong>: P95 new tenant &lt; 1 day; new service &lt; 30 min.</li>
      <li><strong>Incident response</strong>: P95 detect &lt; 5 min; respond &lt; 15 min; resolve per severity.</li>
    </ul>
    <p>Visible in Backstage; quarterly stakeholder review; failures → postmortem + roadmap items."""),
        Section(eyebrow="Section 1.2 · OpenCost vs Kubecost", h2="Cost allocation foundations + commercial extension",
            body_html="""    <p><strong>OpenCost</strong> (CNCF Incubating): open-source. Aggregates cloud-provider bill + per-Pod CPU / memory / storage / network utilization → per-Pod cost. Foundational. Free.</p>
    <p><strong>Kubecost</strong> (commercial; built on OpenCost): adds richer dashboards + chargeback automation + recommendations + multi-cluster aggregation. Commercial tiers for budget alerts / forecasting / governance.</p>
    <p>Most teams: start with OpenCost; upgrade to Kubecost when chargeback automation needed. Both compatible."""),
        Section(eyebrow="Section 1.3 · chargeback vs showback",
            h2="Real bill vs visible cost",
            body_html="""    <p><strong>Showback</strong>: every team sees their cost in dashboards. No actual bill exchange; visibility drives behavior. Easier to roll out; lower friction.</p>
    <p><strong>Chargeback</strong>: monthly bill from platform team to consuming team; finance allocates real $$. Stronger behavior change; more political.</p>
    <p>Most orgs run showback first; mature to chargeback when teams accustomed + finance ready. Kubecost automates chargeback; OpenCost foundations + custom integration for showback dashboards."""),
        Section(eyebrow="Section 1.4 · cost optimisation playbook",
            h2="What teams do once they see cost",
            body_html="""    <p>Once tenants see cost, common optimisations:</p>
    <ul>
      <li><strong>Right-size requests</strong>: many Pods request 2× what they use. VPA recommendations + manual review.</li>
      <li><strong>Spot / Preemptible</strong> for tolerable workloads — 60-90% discount.</li>
      <li><strong>Scale-to-zero</strong> for off-hours (Knative / KEDA scale-to-zero).</li>
      <li><strong>ARM64 / Graviton</strong> — 20-30% cheaper for compatible workloads.</li>
      <li><strong>Reserved Instances / Savings Plans / CUDs</strong> for steady baseline.</li>
      <li><strong>Storage tiering</strong>: log archive to S3 IA / Glacier; hot data on EBS gp3.</li>
    </ul>
    <p>Platform team publishes the playbook; tenants self-tune. Visible cost = behavior change."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why publish platform SLOs?",
            options=[("Compliance.", False), ("Tenants know what to expect; platform team has measurable contract.", True), ("Required by HIPAA.", False)],
            feedback="SLOs make platform expectations explicit + measurable; failures drive postmortems + roadmap; tenant capacity planning depends on them."),
        3: PauseCheck(question="Showback vs chargeback?",
            options=[("Showback always wins.", False), ("Showback = visible cost; chargeback = real bill. Showback first; chargeback when org is ready.", True), ("They\'re the same.", False)],
            feedback="Showback drives behavior via visibility; chargeback adds real $$ allocation. Most orgs roll showback first; mature to chargeback."),
    },
    before_after_before='<p>Pre-cost-transparency, platform team paid the cloud bill; tenants had no incentive to optimise. Bills surprised; allocation was \"trust us\"; teams optimised only when paged.</p>',
    before_after_after='<p>Platform SLOs published; OpenCost / Kubecost surface per-team cost; chargeback or showback drives behavior. Right-sizing + Spot + scale-to-zero adopted by tenants without platform-team push.</p>',
    before_after_caption='<p class="ba-caption"><em>SLOs = the contract. Cost transparency = the incentive. Together = a healthy platform business.</em></p>',
    analogy_intro_html='''<p>Workshop Accounting is the master\'s ledger room. The walls show the workshop\'s commitments to apprentices (SLOs). The ledgers track every apprentice\'s consumed materials (OpenCost). Monthly bills go out (chargeback) or visible reports (showback) — apprentices see their consumption + adjust.</p>''',
    translation_rows=[
        ("Workshop commitments wall", "Platform SLOs (uptime + latency + headroom + onboarding + IR)"),
        ("Apprentice material ledger", "OpenCost / Kubecost"),
        ("Monthly bill", "Chargeback (real cost allocation)"),
        ("Visible report", "Showback (visible without billing)"),
        ("Cost-center stamp", "cost-center label on every Pod"),
        ("Optimisation playbook", "right-size + Spot + scale-to-zero + ARM64 + RIs"),
        ("VPA recommendations", "Vertical Pod Autoscaler advisory mode"),
    ],
    analogy_stops="Workshop ledgers are paper; cost data is API + dashboards. Per-Pod cost is a function of cloud bill + utilisation snapshots; not always penny-precise.",
    eli5="Two things on the wall: what the workshop promises (SLOs) + what each apprentice spends (cost). Apprentices see their costs and learn to spend less.",
    eli10="<strong>Platform SLOs</strong>: published per tier; cluster availability + deploy latency + capacity headroom + onboarding + IR. <strong>OpenCost</strong> (CNCF) + <strong>Kubecost</strong> (commercial extension): per-Pod / per-namespace / per-tenant cost from cloud bill + utilization. <strong>Chargeback</strong> (real bill) vs <strong>showback</strong> (visible). <strong>Optimisation playbook</strong>: right-size + Spot + scale-to-zero + ARM64 + RIs / SP / CUDs.",
    scenarios=[
        Scenario(name="Showback drove tenant behavior", body="6 months after Kubecost rolled out: per-tenant cost reports in Slack weekly. Top spenders right-sized; one team adopted Spot for batch; aggregate cluster cost dropped 22% without platform-team intervention."),
        Scenario(name="SLO breach drove roadmap", body="Onboarding-latency SLO P95 &lt; 1 day broke at 6 days. Postmortem: Crossplane reconciliation lag from missing CRDs. Roadmap item: pre-install required CRDs in cluster bootstrap. SLO recovered next quarter."),
        Scenario(name="Chargeback rollout — finance + engineering aligned", body="After 6 months of showback, org rolled chargeback. Each team\'s cloud cost in their P&L. CFO supports platform team\'s capacity expansion proposals because cost mapping is clear."),
        Scenario(name="Outage — surprise $40k from one tenant", body="Pre-controls, one tenant\'s Quota limit was high; Pods consumed; cost spiked. OpenCost + budget alerts + tighter Quota added. Same shape no longer possible."),
    ],
    misconceptions=[
        Misconception(myth="\"Platform SLOs are aspirational; nobody enforces.\"", truth="If unenforced, tenants don\'t plan around them. Quarterly stakeholder review + postmortem on misses + roadmap items make SLOs real."),
        Misconception(myth="\"OpenCost is precise.\"", truth="OpenCost is best-effort allocation: cloud-bill aggregates + per-Pod utilization snapshots. ~5-10% precision; good enough for chargeback at the team level."),
        Misconception(myth="\"Chargeback is too political; just use showback.\"", truth="Showback is fine for some orgs; chargeback aligns engineering with finance. Mature orgs run chargeback; the political work is one-time setup."),
    ],
    flashcards=[
        Flashcard(front="Five typical platform SLOs?", back="Cluster availability per tier; deploy latency P95 &lt; 5 min; capacity headroom ≥ 20%; onboarding latency P95 &lt; 1 day; IR detect &lt; 5min / contain &lt; 15min."),
        Flashcard(front="OpenCost vs Kubecost?", back="<strong>OpenCost</strong>: CNCF open-source foundation. <strong>Kubecost</strong>: commercial product on top with richer dashboards + chargeback + recommendations + forecasting."),
        Flashcard(front="Chargeback vs showback?", back="<strong>Showback</strong>: visible cost; no real bill exchange. <strong>Chargeback</strong>: real $$ allocated to consuming teams. Showback first; chargeback when org ready."),
        Flashcard(front="Cost optimisation playbook?", back="Right-size requests (VPA recommend); Spot/Preemptible; scale-to-zero (Knative/KEDA); ARM64/Graviton; RIs/SP/CUDs; storage tiering."),
        Flashcard(front="Why cost-center labels on every Pod?", back="OpenCost / Kubecost allocate cost using labels. Without label, cost goes to \"unallocated\" bucket; chargeback breaks. Mutating webhook injects label if missing."),
        Flashcard(front="VPA advisory mode?", back="Vertical Pod Autoscaler reads usage + recommends per-Pod requests/limits. Use in advisory (not auto-apply) to surface right-sizing opportunities to tenants."),
        Flashcard(front="SLO breach → what happens?", back="Postmortem (NIST 800-61 style for non-incident perf misses); roadmap items added; quarterly stakeholder review tracks closure. SLOs drive backlog priority."),
        Flashcard(front="Capacity headroom — why ≥ 20%?", back="Below 20%, autoscaler can\'t respond to spikes; saturation cascades. 20% is the empirical threshold for \"new Pod can schedule fast\"; headroom is the proactive buffer."),
    ],
    quizzes=[
        Quiz(prompt="Roll out OpenCost + showback in a 100-engineer org. Walk steps.",
            answer="(1) <strong>Cost-center labels</strong>: Kyverno mutating webhook injects on every Pod / Service / PVC. (2) <strong>Install OpenCost</strong>: Helm chart in monitoring namespace. (3) <strong>Configure cloud-billing integration</strong>: AWS Cost + Usage Reports / Azure Cost Management / GCP BigQuery export. (4) <strong>Validate</strong>: per-namespace cost reports match cloud-billing aggregates ±10%. (5) <strong>Backstage plugin</strong>: surface per-service cost in service page. (6) <strong>Weekly Slack reports</strong>: top spenders + week-over-week. (7) <strong>Optimisation playbook</strong>: published; teams self-tune. (8) <strong>Quarterly review</strong>: aggregate cost trends + biggest savings."),
        Quiz(prompt="A tenant asks: \"why does our team\'s bill keep rising?\" Walk an analysis.",
            answer="(1) <strong>Open Kubecost dashboard</strong>: per-namespace cost over time. (2) <strong>Drill down</strong>: top Pods by cost; growing? new workloads? (3) <strong>Right-size check</strong>: VPA recommendations show over-provisioned. (4) <strong>Workload class check</strong>: any moved from Spot to On-Demand? (5) <strong>Storage check</strong>: PVC growth? log archive policy? (6) <strong>Recommendation</strong>: specific Pods to right-size; Spot opportunities; storage tiering; ARM64 candidates. (7) <strong>Track</strong>: target % cost reduction; review in 30 days."),
        Quiz(prompt="The CFO asks why we don\'t just rate-limit clusters by quota and skip chargeback. Defend.",
            answer="\"<strong>Quota caps + chargeback aren\'t either-or.</strong> Quota = hard cap (preventive); chargeback = behavior change (proactive). Three reasons we run both: (1) <strong>Within-quota optimisation</strong>: a team at 90% Quota with right-sizing could be at 60% — cheaper for the org without changing Quota. Chargeback drives this. (2) <strong>Cross-team comparison</strong>: chargeback surfaces team-X is 3× team-Y for similar workloads — anomaly investigation. (3) <strong>Finance alignment</strong>: cloud cost in team P&L = engineering accountable to budget. Quota alone says \"can\'t exceed\"; chargeback says \"this is yours\". Together: sane caps + sane usage.\"", cyoa=True, cyoa_tag="how the platform engineer defended chargeback"),
    ],
    glossary=[
        GlossaryItem(name="Platform SLO", definition="Published platform contract: availability + deploy latency + capacity headroom + onboarding + IR."),
        GlossaryItem(name="OpenCost", definition="CNCF Incubating cost allocation. Cloud bill + per-Pod utilization → per-Pod cost."),
        GlossaryItem(name="Kubecost", definition="Commercial product on OpenCost. Richer dashboards + chargeback + recommendations + forecasting."),
        GlossaryItem(name="Chargeback", definition="Real $$ allocation: consuming team sees cost in their P&L."),
        GlossaryItem(name="Showback", definition="Visible cost; no real bill exchange. Behavior change via transparency."),
        GlossaryItem(name="cost-center label", definition="Mutating-injected label on Pod / Service / PVC; foundation for OpenCost allocation."),
        GlossaryItem(name="VPA advisory mode", definition="Vertical Pod Autoscaler in recommend-only mode; surfaces right-sizing without auto-apply."),
        GlossaryItem(name="Spot / Preemptible / SPOT_VM", definition="Cheaper cloud instances reclaimable on short notice; 60-90% discount; tolerated by stateless / restartable workloads."),
        GlossaryItem(name="RI / Savings Plans / CUDs", definition="AWS Reserved Instances / Savings Plans / GCP Committed Use Discounts. Steady-baseline discount."),
        GlossaryItem(name="ARM64 / Graviton", definition="ARM-architecture instances; 20-30% cheaper than equivalent x86. Compatible workloads only."),
    ],
    recap_lead="Platform SLOs published as contract; OpenCost / Kubecost surface per-team cost; showback or chargeback drives behavior. Cost optimisation playbook + tenant self-tune.",
    recap_next='<strong>Next — P8: Capstone — self-service IDP with namespace provisioning, RBAC, quotas, NetworkPolicy, GitOps, app templates, observability, cost labels, policy guardrails.</strong>',
)
