"""K-ADV-DR D5 — Capstone: destroy + rebuild a complete production cluster."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Capstone DR — total-loss drill."><rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Total-Loss Drill · K-Lifeboat — destroy + rebuild within RTO</text><rect x="40" y="70" width="130" height="60" rx="10" fill="#3F4A5E"/><text x="105" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Git source</text><rect x="190" y="70" width="130" height="60" rx="10" fill="#5DCAA5"/><text x="255" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">Velero + DB</text><rect x="340" y="70" width="130" height="60" rx="10" fill="#FF9900"/><text x="405" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">OCI registry</text><rect x="490" y="70" width="130" height="60" rx="10" fill="#A04832"/><text x="555" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Vault snapshot</text><rect x="640" y="70" width="80" height="60" rx="10" fill="#5A6B81"/><text x="680" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">DNS</text><rect x="40" y="160" width="680" height="60" rx="10" fill="#FBE8DC" stroke="#A04832"/><text x="380" y="185" text-anchor="middle" font-size="11" font-weight="700" fill="#A04832">Destroy cluster + rebuild from these 5 sources within RTO</text></svg>"""


LESSON = LessonSpec(
    num="05", title_short="capstone — total-loss drill", title_full="D5 · Capstone — Destroy + Rebuild a Complete Production Cluster",
    title_html="K-ADV-DR D5 · Capstone", module_eyebrow="Module D5 · Total-Loss Drill — destroy + rebuild within RTO",
    hero_sub_html='Reference DR drill: simulate (or experience) total cluster loss; rebuild end-to-end from <strong>five sources</strong> — <em>Git</em> (config + apps), <em>backups</em> (Velero PVCs + DB snapshots), <em>OCI registry</em> (images + signed artifacts), <em>secrets</em> (external Vault snapshot + KMS replication), <em>DNS</em> (Route 53 / Azure DNS / Cloud DNS). Walk + measure + improve.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. The hypothetical scenario you\'ve drilled became real: cluster gone; data center fire; insurance won\'t cover downtime past 4h. <em>Today\'s capstone: the drill that prepared you for this</em>. End-to-end rebuild within RTO. The runbook works because you exercised it.",
    stamp_html="<strong>Total-loss drill: rebuild from Git + backups + OCI registry + Vault + DNS within RTO. Quarterly drill non-optional. The architecture isn\'t the work; the disciplined exercise is.</strong>",
    district_pin="kdr-cell05", district_label="Total-Loss Drill",
    sections=[
        Section(eyebrow="Section 1.1 · the five sources",
            h2="Git + Velero + OCI + Vault + DNS",
            body_html="""    <p>Total cluster loss recovery requires five sources outside the dead cluster:</p>
    <ul>
      <li><strong>Git</strong>: cluster IaC + GitOps source-of-truth for apps + ApplicationSets.</li>
      <li><strong>Backups</strong>: Velero (PVCs + Secrets + ConfigMaps) + DB snapshots (cross-region replicated).</li>
      <li><strong>OCI registry</strong>: container images + Cosign signatures + SBOMs + model artifacts.</li>
      <li><strong>Secrets</strong>: external Vault HA snapshot + KMS replicated keys.</li>
      <li><strong>DNS</strong>: Route 53 / managed DNS records + health-check failover.</li>
    </ul>
    <p>Each source is independent + survives cluster loss. Coordinate the timeline."""),
        Section(eyebrow="Section 1.2 · the drill sequence",
            h2="Numbered runbook; measured per phase",
            body_html="""    <p>End-to-end runbook:</p>
    <ol>
      <li><strong>Trigger</strong>: cluster confirmed lost (or drill announced); on-call paged.</li>
      <li><strong>Cluster IaC</strong>: Terraform / Crossplane provisions new cluster; Argo CD installed (~10-15 min).</li>
      <li><strong>GitOps sync</strong>: Argo CD ApplicationSet picks up new cluster; CRDs (sync-wave -2) → operators (-1) → apps (0+) (~10 min).</li>
      <li><strong>Vault snapshot restore</strong>: rebuild Vault HA in new region (or DR region already running); ESO re-syncs secrets to new cluster (~5 min).</li>
      <li><strong>Velero restore</strong>: PVCs + Secrets + ConfigMaps from cross-region backup (~5 min).</li>
      <li><strong>DB restore</strong>: managed-DB cross-region promote + custom-DB restore from snapshot (~10 min).</li>
      <li><strong>Validate</strong>: SLO metrics return; tenant smoke tests pass (~5 min).</li>
      <li><strong>DNS swap</strong>: Route 53 record points at new ALB / global LB shifts traffic.</li>
      <li><strong>Tenant communication</strong>: status page update.</li>
    </ol>
    <p><strong>Total RTO target</strong>: 30-60 min for managed K8s + warm DR pattern; longer for cold DR."""),
        Section(eyebrow="Section 1.3 · drill cadence + improvement",
            h2="Quarterly + monthly + tabletop",
            body_html="""    <p>Drill regimen:</p>
    <ul>
      <li><strong>Quarterly full drill</strong>: total cluster destruction in non-prod; full rebuild; measure end-to-end RTO.</li>
      <li><strong>Monthly per-namespace test</strong>: smaller-scope; catches drift between full drills.</li>
      <li><strong>Semi-annual tabletop</strong>: paper-walk through scenarios (\"region down + DR partially degraded\"); identify decision points.</li>
      <li><strong>Per-incident postmortem</strong>: real incidents drive runbook + automation improvements.</li>
    </ul>
    <p>Continuous improvement: every drill produces a runbook delta; every delta improves RTO; over years, RTO trends down."""),
        Section(eyebrow="Section 1.4 · operational rhythm + organisation",
            h2="DR engineering team + roles + budget",
            body_html="""    <p><strong>DR engineering team</strong>: 1-2 engineers focused on backup + restore tooling + drill orchestration. Reports to platform team.</p>
    <p><strong>Roles per drill</strong>: <em>Drill Master</em> (designs scenario + coordinates), <em>On-call</em> (executes runbook), <em>Observer</em> (measures + records), <em>Tenant rep</em> (validates from tenant POV).</p>
    <p><strong>Budget</strong>: drill cluster (non-prod) + cross-region storage + Vault HA + DNS health-check. Single biggest cost: cross-region data transfer.</p>
    <p><strong>Reporting</strong>: per-quarter drill report to leadership: RTO measured + improvements made + outstanding gaps. <strong>The architecture is the easy part; the disciplined exercise is the work.</strong>"""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why five sources outside the cluster?",
            options=[("Best practice.", False), ("Each survives cluster loss; together they let you rebuild fully.", True), ("Required by SOC2.", False)],
            feedback="Each source is independent. Without all five, rebuild is incomplete (e.g., missing secrets, missing data, missing DNS swap)."),
        3: PauseCheck(question="Why monthly per-namespace test in addition to quarterly full?",
            options=[("Compliance only.", False), ("Drift accumulates; smaller fast tests catch issues between full drills.", True), ("Required by Velero.", False)],
            feedback="Per-namespace tests are faster + cheaper; catch drift. Both required for critical clusters."),
    },
    before_after_before='<p>Pre-disciplined-DR: total cluster loss = days of recovery; runbook in someone\'s head; first incident reveals gaps.</p>',
    before_after_after='<p>Disciplined DR: 5 sources + runbook + quarterly drill + measured RTO. Total cluster loss = 30-60 min recovery; SLA preserved.</p>',
    before_after_caption='<p class="ba-caption"><em>Discipline beats hope. Quarterly drill is non-optional.</em></p>',
    analogy_intro_html='''<p>Total-Loss Drill: simulate (or live through) the loss of an entire ship + its harbor. The Drill Master shows the rebuild from five outside sources: blueprints (Git), cargo backups (Velero + DB), warehouse (OCI registry), vault (Vault + KMS), routing tower (DNS). The Captain runs the drill quarterly. Real loss = drill in production with adrenaline.</p>''',
    translation_rows=[
        ("Five outside sources", "Git + Velero + OCI registry + Vault + DNS"),
        ("Drill Master", "DR architect / lead engineer"),
        ("On-call executor", "On-call engineer following runbook"),
        ("Observer / scribe", "Records timing + gaps"),
        ("Tenant rep", "Validates from tenant POV"),
        ("Quarterly full drill", "Total cluster destroy + rebuild"),
        ("Tabletop drill", "Paper-walk scenarios"),
        ("RTO measured + improved", "End-to-end recovery time per quarter"),
    ],
    analogy_stops="A real fleet exercise has fixed assets; cluster + cloud + region setup change. Re-validate runbook after major architecture shifts.",
    eli5="Practice losing the whole castle quarterly so you\'re ready when it happens for real. Five things outside the castle are needed: blueprints, cargo backups, warehouse, vault, signal tower.",
    eli10="<strong>Five sources</strong>: Git + Velero + OCI registry + Vault + DNS. <strong>Runbook</strong>: cluster IaC → GitOps sync (sync waves) → Vault restore → Velero restore → DB restore → validate → DNS swap. <strong>Drill cadence</strong>: quarterly full + monthly per-namespace + semi-annual tabletop. <strong>Roles</strong>: Drill Master + on-call + observer + tenant rep. <strong>Operational rhythm</strong>: continuous improvement.",
    scenarios=[
        Scenario(name="Quarterly drill — 28-min RTO", body="Q3 drill: simulated us-east-1 cluster loss; rebuild followed runbook; measured 28-min end-to-end (vs 30-min target). One gap: Velero parallel restore tuning. Fixed before Q4 drill."),
        Scenario(name="Real incident — runbook saved the day", body="Bad upgrade corrupted prod cluster; on-call followed Q3-drilled runbook; rebuild in 32 min; tenants notified via status page; SLA preserved."),
        Scenario(name="Tabletop caught decision-point gap", body="Tabletop scenario: \"primary region down + DR region partially degraded\" — runbook didn\'t cover. Postmortem: added decision tree (route to which DR region); next drill clean."),
        Scenario(name="Outage — drill skipped for a quarter", body="Skipped Q2 drill due to launches. Q3 real incident; runbook had drift; recovery took 4h instead of 1h. Postmortem: drills are non-optional; protected calendar.")
    ],
    misconceptions=[
        Misconception(myth="\"Backups + GitOps means we don\'t need drills.\"", truth="Untested = unverified. Drills find gaps that backup-success metrics don\'t — schema drift, secret rotation, DNS TTL, runbook ambiguity."),
        Misconception(myth="\"Quarterly is too frequent.\"", truth="Less than quarterly = drift accumulates invisibly. Real loss reveals it; drill finds it on a calm day."),
        Misconception(myth="\"DR is for very large orgs.\"", truth="Even small orgs lose clusters (cloud incident; bad upgrade; human error). RTO commitment varies by org but every cluster benefits from tested DR."),
    ],
    flashcards=[
        Flashcard(front="Five sources for cluster rebuild?", back="<strong>Git</strong> (config + apps + IaC), <strong>backups</strong> (Velero + DB snapshots), <strong>OCI registry</strong> (images + signatures + models), <strong>secrets</strong> (external Vault + KMS), <strong>DNS</strong> (managed DNS + health checks)."),
        Flashcard(front="Drill cadence?", back="<strong>Quarterly</strong> full drill + <strong>monthly</strong> per-namespace + <strong>semi-annual</strong> tabletop. Continuous improvement."),
        Flashcard(front="Drill roles?", back="<strong>Drill Master</strong> (scenario + coordinator), <strong>On-call</strong> (executor), <strong>Observer</strong> (timer / scribe), <strong>Tenant rep</strong> (validation)."),
        Flashcard(front="Capstone runbook order?", back="(1) Cluster IaC; (2) GitOps install + sync waves; (3) Vault restore; (4) Velero restore; (5) DB restore; (6) Validate; (7) DNS swap; (8) Tenant comms."),
        Flashcard(front="RTO target for managed K8s + warm DR?", back="30-60 min end-to-end; longer for cold DR or self-managed clusters."),
        Flashcard(front="Why measure per-phase timing?", back="Identifies bottleneck. Optimise the bottleneck phase; iterate. Without per-phase measurement, optimisation is guesswork."),
        Flashcard(front="What\'s a tabletop drill?", back="Paper-walk through scenarios (no live execution). Cheap; finds runbook gaps + decision-point ambiguities."),
        Flashcard(front="DR engineering team — typical size?", back="1-2 engineers per platform. Owns backup + restore tooling + drill orchestration + DR roadmap."),
    ],
    quizzes=[
        Quiz(prompt="Walk a quarterly total-loss drill end-to-end.",
            answer="(1) <strong>Schedule</strong>: announce drill 1 week ahead; on-call rotation aware; tenant comms paused for drill cluster. (2) <strong>Trigger</strong>: Drill Master destroys non-prod cluster (Terraform destroy or AWS console). (3) <strong>On-call follows runbook</strong>: provision new cluster (~10 min); install Argo CD (~2 min); GitOps sync waves (~10 min); Vault snapshot restore (~5 min); Velero restore (~5 min); DB cross-region promote (~5 min); validate SLOs (~5 min); DNS swap (~2 min). (4) <strong>Observer records</strong>: per-phase timing; deviations from runbook; tenant-rep verification. (5) <strong>Postmortem</strong>: total RTO measured; gaps identified; runbook + tooling improvements queued. (6) <strong>Report</strong>: leadership update with RTO trend."),
        Quiz(prompt="Real cluster lost. On-call follows runbook. Cluster rebuilt at 28 min; tenant complains about app X data missing. Diagnose.",
            answer="(1) <strong>App X data not in Velero backup?</strong> Audit backup scope: was the namespace included? Was the PVC backed up? (2) <strong>External managed-service?</strong> If app X depends on RDS / S3 / external SaaS, those have own DR. Status of that service? (3) <strong>Restore order issue?</strong> App X restored before its dependency was up; data inaccessible. (4) <strong>Schema migration drift?</strong> Backup is older than app expects. (5) <strong>Mitigation</strong>: communicate impact; queued data restore from offline backup if applicable; postmortem covers backup scope review."),
        Quiz(prompt="Leadership says: \"why quarterly drills? we have backups.\" Defend.",
            answer="\"<strong>Quarterly drills are how we know our backups + runbook + team are ready.</strong> Three reasons non-optional: (1) <strong>Drift</strong>: code + config + tooling change every week. Without drill, drift accumulates invisibly. Real loss reveals it; drill finds it on a calm day. (2) <strong>Team readiness</strong>: drill team practices roles; on-call rotation tests muscle memory; tenant rep verifies UX. Without exercise, real loss = first attempt at coordinated rebuild. (3) <strong>Compliance</strong>: SOC2 / HIPAA / FedRAMP all require tested DR. Without drill report, audits fail. <strong>Cost</strong>: ~1 dev-day per quarter per DR engineer + non-prod cluster. <strong>Saved</strong>: bounded RTO during real loss; preserved SLA; preserved customer trust.\"", cyoa=True, cyoa_tag="how the DR architect defended quarterly drills"),
    ],
    glossary=[
        GlossaryItem(name="Total-loss drill", definition="Quarterly full cluster destroy + rebuild; measure end-to-end RTO."),
        GlossaryItem(name="Five sources", definition="Git + Velero / DB backups + OCI registry + Vault + DNS — outside-cluster sources for rebuild."),
        GlossaryItem(name="Drill Master", definition="DR architect coordinating drill scenario + observer."),
        GlossaryItem(name="Tabletop drill", definition="Paper-walk through scenarios; finds runbook gaps cheaply."),
        GlossaryItem(name="Per-phase timing", definition="Measure each drill phase (cluster IaC / GitOps / Vault / Velero / DB / validate / DNS); identify bottleneck."),
        GlossaryItem(name="Continuous improvement (DR)", definition="Every drill produces runbook delta; every delta improves RTO; trend down over years."),
        GlossaryItem(name="DR engineering team", definition="1-2 engineers owning backup + restore + drill orchestration + roadmap."),
        GlossaryItem(name="Drill report", definition="Per-quarter leadership update with RTO trend + improvements + gaps."),
    ],
    recap_lead="Total-loss drill: rebuild from Git + Velero + OCI + Vault + DNS within RTO. Quarterly + monthly + tabletop. Measured per-phase. Continuous improvement. The disciplined exercise is the work.",
    recap_next='<strong>K-ADV-DR complete.</strong> 5 modules. From etcd backup (D1) to total-loss drill (D5). <strong>K-ADV family complete</strong>: K-ADV-SEC + K-ADV-NET + K-ADV-PE + K-ADV-AI + K-ADV-DR — 36 advanced modules across 5 specializations.',
)
