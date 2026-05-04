"""K-ADV-DR D3 — Cross-region DR + RPO/RTO + restore testing."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Cross-region DR."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Mirror-Ship Harbor · K-Lifeboat — primary + DR region; RPO + RTO measured</text><rect x="40" y="70" width="200" height="100" rx="10" fill="#3F4A5E"/><text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">primary region</text><text x="140" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">us-east-1 active</text><rect x="260" y="70" width="200" height="100" rx="10" fill="#5DCAA5"/><text x="360" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">DR region</text><text x="360" y="108" text-anchor="middle" font-size="9" fill="#1F2433">us-west-2 standby/active</text><rect x="480" y="70" width="240" height="100" rx="10" fill="#FF9900"/><text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">RPO + RTO + restore-test</text><text x="600" y="108" text-anchor="middle" font-size="9" fill="#1F2433">measured + practiced</text></svg>"""


LESSON = LessonSpec(
    num="03", title_short="cross-region DR + RPO/RTO", title_full="D3 · Cross-Region DR + RPO/RTO + Backup Validation + Restore Testing",
    title_html="K-ADV-DR D3 · Cross-Region DR", module_eyebrow="Module D3 · Mirror-Ship Harbor — primary + DR region; RPO + RTO measured",
    hero_sub_html='<strong>Cross-region DR shapes</strong>: <em>active-passive</em> (DR region cold; activate on disaster); <em>active-active</em> (both regions serve traffic; failover instant); <em>warm standby</em> (DR cluster + minimal capacity; scale on disaster). <strong>RPO + RTO</strong>: per-tier (gold = 1h RPO / 4h RTO; bronze = 24h). <strong>Backup validation</strong>: backups tested via restore drill; not just \"backup completed.\" <strong>Restore testing</strong>: quarterly minimum; drives runbook + RTO improvement.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. AWS us-east-1 is down. Your DR plan says \"failover to us-west-2.\" <em>But: the DR cluster has been off for months; nothing is current; failover takes 6 hours instead of 30 min</em>. Today\'s lesson: cross-region DR shapes + measured RPO/RTO + restore tested.",
    stamp_html="<strong>Pick DR shape: active-active / active-passive / warm-standby. Per-tier RPO + RTO. Quarterly restore-test mandatory. Untested backup is hope, not plan.</strong>",
    district_pin="kdr-cell03", district_label="Mirror-Ship Harbor",
    sections=[
        Section(eyebrow="Section 1.1 · DR shapes", h2="active-passive · active-active · warm-standby",
            body_html="""    <p><strong>Active-passive</strong>: primary serves; DR cluster cold (cluster doesn\'t exist or scaled-to-zero). Cheapest. RTO 30-60 min (cluster IaC + GitOps + restore). Use for cost-sensitive non-critical workloads.</p>
    <p><strong>Active-active</strong>: both regions serve via global LB; cross-region replication of state. RTO &lt; 60s; RPO seconds-minutes. Most expensive. Use for tier-1 critical.</p>
    <p><strong>Warm standby</strong>: DR cluster runs; minimal capacity; scale on disaster. RTO 5-10 min. Middle ground. Use for tier-2 important."""),
        Section(eyebrow="Section 1.2 · RPO + RTO per tier",
            h2="Define + publish + measure",
            body_html="""    <p>Define per-tier RPO + RTO commitments:</p>
    <ul>
      <li><strong>Tier-1 (gold)</strong>: RPO &lt; 5 min; RTO &lt; 5 min. Active-active.</li>
      <li><strong>Tier-2 (silver)</strong>: RPO &lt; 1h; RTO &lt; 30 min. Warm standby.</li>
      <li><strong>Tier-3 (bronze)</strong>: RPO &lt; 24h; RTO &lt; 4h. Active-passive.</li>
    </ul>
    <p>Publish to tenants; tenants choose tier; cost varies. Quarterly drill measures actual; gap drives engineering."""),
        Section(eyebrow="Section 1.3 · backup validation",
            h2="\"Backup completed\" ≠ \"restorable\"",
            body_html="""    <p><strong>Backup validation</strong> beyond \"job succeeded\":</p>
    <ul>
      <li><strong>Bit-rot check</strong>: re-read backup; verify checksums. Detect storage corruption.</li>
      <li><strong>Test-restore</strong>: scheduled restore to non-prod cluster; validate apps come up.</li>
      <li><strong>Synthetic transactions</strong>: post-restore, run synthetic queries; compare to pre-backup state.</li>
      <li><strong>Time-bounded</strong>: restore must complete within RTO; alarm if exceeded.</li>
    </ul>
    <p>Tools: Velero schedules + cron-job test-restore + Datadog / Prometheus monitoring of restore-time."""),
        Section(eyebrow="Section 1.4 · restore testing cadence",
            h2="Quarterly minimum; drive RTO improvement",
            body_html="""    <p><strong>Quarterly restore-test</strong>: per critical cluster, full rebuild to non-prod. Measure: time per phase (cluster + GitOps + Velero + DNS); identify bottlenecks; engineer fixes.</p>
    <p><strong>Per-namespace test</strong>: monthly; faster + smaller-scope; catches per-namespace drift.</p>
    <p><strong>Tabletop drill</strong>: paper-walk through scenarios (\"region X down + DR region Y partially degraded\"); identify gaps in runbook before real exercise.</p>
    <p><strong>Cadence</strong>: quarterly full + monthly per-namespace + semi-annual tabletop. Continuous improvement."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="When pick active-active over active-passive?",
            options=[("Always.", False), ("Tier-1 critical workloads where RTO must be &lt; 60s; cost premium accepted.", True), ("Cost-sensitive workloads.", False)],
            feedback="Active-active = highest cost; lowest RTO. Active-passive = lowest cost; longer RTO. Match shape to tier."),
        3: PauseCheck(question="Why monthly per-namespace restore-test in addition to quarterly full?",
            options=[("Compliance.", False), ("Per-namespace drift accumulates faster than quarterly catches; smaller-scope fast tests catch it.", True), ("Faster than quarterly.", False)],
            feedback="Per-namespace tests are faster + cheaper; catch drift between full quarterly drills. Both required for critical clusters."),
    },
    before_after_before='<p>Pre-tested-DR: backups configured; nobody restored; RPO + RTO unmeasured; assumed \"it\'ll work.\" Real outage = chaos.</p>',
    before_after_after='<p>Tested DR: per-tier RPO + RTO; quarterly drill measures; engineering fixes gaps. Real outage = bounded recovery.</p>',
    before_after_caption='<p class="ba-caption"><em>Untested backup = hope. Quarterly drill = plan.</em></p>',
    analogy_intro_html='''<p>Mirror-Ship Harbor: a sister harbor in another region, mirroring the primary. Three operating shapes: <strong>both harbors active</strong> (active-active; ships dock either); <strong>cold mirror</strong> (active-passive; mirror dormant); <strong>warm mirror</strong> (warm-standby; mirror has minimal crew). Drill Master tests the failover quarterly + measures RTO.</p>''',
    translation_rows=[
        ("Both harbors active", "active-active (global LB + cross-region replication)"),
        ("Cold mirror", "active-passive (DR cluster off; rebuild on disaster)"),
        ("Warm mirror", "warm standby (DR cluster runs; minimal capacity)"),
        ("Per-tier mirror commitments", "RPO + RTO per tier"),
        ("Backup-rehydration drill", "Restore-test"),
        ("Tabletop drill", "Paper-walk through scenarios"),
    ],
    analogy_stops="A real harbor is fixed; cluster regions are virtual. Cross-region replication has cloud-specific gotchas (data egress cost; latency).",
    eli5="Sister harbor across the bay. Sometimes both work; sometimes the sister is dormant. Practice the failover every quarter so it\'s fast when needed.",
    eli10="<strong>DR shapes</strong>: active-active / warm-standby / active-passive. <strong>RPO</strong> = data loss window; <strong>RTO</strong> = recovery time. Per-tier commitments published. <strong>Backup validation</strong>: bit-rot + test-restore + synthetic transactions. <strong>Restore-testing</strong>: quarterly full + monthly per-namespace + semi-annual tabletop.",
    scenarios=[
        Scenario(name="Active-active for tier-1 fintech", body="Fintech runs payment processing across us-east-1 + us-west-2 active-active; cross-region DB replication (Aurora Global / Spanner); global LB routes; failover &lt; 60s on region degradation. RTO requirement met."),
        Scenario(name="Warm-standby for tier-2 SaaS", body="SaaS runs primary in us-east-1; DR cluster in us-west-2 minimal-capacity; on disaster, scale + activate. RTO 8 min; cost ~30% premium over single-region. Acceptable for tier-2."),
        Scenario(name="Quarterly drill caught Velero version skew", body="Drill: backup taken on Velero v1.10; new cluster ran v1.13; restore failed schema mismatch. Postmortem: pin Velero version + auto-upgrade in IaC; runbook updated."),
        Scenario(name="Outage — untested DR", body="Pre-drill, DR plan was paper. Real outage: 12-hour recovery (vs target 4h). Postmortem: quarterly drills mandated; staffed.")
    ],
    misconceptions=[
        Misconception(myth="\"Active-active is always best.\"", truth="Cost premium is high (~2× capacity + cross-region traffic). Use only for tier-1 critical. Most workloads suit warm-standby or active-passive."),
        Misconception(myth="\"Backup success metric is enough.\"", truth="Backup that completes ≠ backup that restores. Test-restore quarterly to verify."),
        Misconception(myth="\"Cross-region DR works automatically with managed K8s.\"", truth="EKS / GKE / AKS = managed control plane; you still own cross-region cluster + state replication strategy. Not automatic; deliberate engineering required."),
    ],
    flashcards=[
        Flashcard(front="Three DR shapes?", back="<strong>Active-passive</strong> (DR cold; cheapest), <strong>warm standby</strong> (DR running minimal), <strong>active-active</strong> (both serve; most expensive)."),
        Flashcard(front="RPO vs RTO?", back="<strong>RPO</strong>: max acceptable data loss (window between snapshots). <strong>RTO</strong>: max acceptable recovery time."),
        Flashcard(front="Per-tier RPO/RTO targets?", back="Tier-1 gold: RPO 5min / RTO 5min. Tier-2 silver: RPO 1h / RTO 30min. Tier-3 bronze: RPO 24h / RTO 4h."),
        Flashcard(front="Backup validation steps?", back="(1) Bit-rot check (checksum re-read), (2) Test-restore to non-prod, (3) Synthetic transactions post-restore, (4) Time-bounded restore-time SLO."),
        Flashcard(front="Restore-test cadence?", back="<strong>Quarterly</strong>: full rebuild. <strong>Monthly</strong>: per-namespace. <strong>Semi-annual</strong>: tabletop drill (paper-walk)."),
        Flashcard(front="Cross-region replication options?", back="Cloud DB (Aurora Global / Spanner / Cosmos DB Global) + Velero cross-region BackupStorageLocation + S3 cross-region replication."),
        Flashcard(front="Why tabletop drill in addition to live?", back="Tabletop catches gaps in runbook + decision points before live drill burns time. Cheaper to find issues; faster iteration."),
        Flashcard(front="When is active-active overkill?", back="Tier-2 / tier-3 workloads where users tolerate 5-30 min recovery. Active-active cost premium isn\'t justified."),
    ],
    quizzes=[
        Quiz(prompt="Design DR for a 3-tier (gold / silver / bronze) SaaS.",
            answer="(1) <strong>Tier-1 gold</strong> (payment / auth): active-active across us-east-1 + us-west-2; cross-region Aurora Global; Route 53 global LB. RPO 5min / RTO 5min. (2) <strong>Tier-2 silver</strong> (core API): warm-standby in DR region; minimal capacity (1 of each Service); scale on disaster via Argo CD ApplicationSet + autoscale. RPO 1h (Velero hourly cross-region) / RTO 30min. (3) <strong>Tier-3 bronze</strong> (internal tools): active-passive; DR cluster destroyed when primary healthy; rebuild from IaC + GitOps + Velero on disaster. RPO 24h / RTO 4h. (4) <strong>Quarterly drill</strong> per tier; published RPO/RTO."),
        Quiz(prompt="A team\'s drill measured 5h RTO (target 30min). Walk improvement.",
            answer="(1) <strong>Profile each phase</strong>. (2) <strong>If cluster IaC slow</strong>: pre-warm DR cluster (warm-standby) — eliminates cluster-IaC time. (3) <strong>If Velero restore slow</strong>: parallel restore + smaller backup units; CSI snapshots over Restic. (4) <strong>If GitOps sync slow</strong>: pre-sync ApplicationSets in warm cluster; on disaster, just refresh data. (5) <strong>If DNS slow</strong>: lower TTL on DNS records; pre-stage failover automation. (6) <strong>Re-drill</strong>: verify each fix; iterate."),
        Quiz(prompt="The CFO sees cross-region DR cost premium. Defend per-tier model.",
            answer="\"<strong>DR cost is proportional to RPO/RTO commitment.</strong> Three reasons per-tier wins: (1) <strong>Tier-1 active-active</strong>: 2× cost; required for tier-1 (payment / auth) where outage = customer churn. (2) <strong>Tier-2 warm-standby</strong>: ~30% cost premium; fits tier-2 important. (3) <strong>Tier-3 active-passive</strong>: ~5% premium (just backups); fits tier-3 internal. <strong>Without tiering</strong>: either over-engineer everything (3× cost) or under-engineer everything (catastrophe risk). <strong>Tiered DR matches investment to risk</strong>.\"", cyoa=True, cyoa_tag="how the DR architect defended tiered DR"),
    ],
    glossary=[
        GlossaryItem(name="active-active", definition="Both regions serve traffic; cross-region replication; failover &lt; 60s; most expensive."),
        GlossaryItem(name="active-passive", definition="DR region cold; rebuild on disaster; cheapest; longest RTO."),
        GlossaryItem(name="warm standby", definition="DR cluster runs; minimal capacity; scale on disaster; middle ground."),
        GlossaryItem(name="RPO", definition="Recovery Point Objective; max acceptable data loss window."),
        GlossaryItem(name="RTO", definition="Recovery Time Objective; max acceptable recovery time."),
        GlossaryItem(name="backup validation", definition="Bit-rot check + test-restore + synthetic transactions; verify backup is restorable."),
        GlossaryItem(name="restore-test", definition="Quarterly full rebuild to non-prod; measure RTO; engineer improvements."),
        GlossaryItem(name="tabletop drill", definition="Paper-walk through scenarios; cheap; catches runbook gaps."),
        GlossaryItem(name="cross-region replication", definition="Cloud-native (Aurora Global / Spanner / Cosmos DB) or Velero cross-region BackupStorageLocation."),
        GlossaryItem(name="global LB failover", definition="Route 53 / Azure Traffic Manager / GCP Global LB health-check + automatic failover."),
    ],
    recap_lead="Cross-region DR shapes: active-active / warm-standby / active-passive. Per-tier RPO + RTO. Backup validation. Quarterly restore-test mandatory.",
    recap_next='<strong>Next — D4: Secret recovery + DNS failover + stateful workload DR + managed-service DR limits.</strong>',
)
