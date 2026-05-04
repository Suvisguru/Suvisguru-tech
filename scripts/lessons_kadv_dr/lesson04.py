"""K-ADV-DR D4 — Secret recovery + DNS failover + stateful DR + managed-service DR limits."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Specialty DR — secrets / DNS / stateful / managed."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Cargo Recovery Office · K-Lifeboat — specialty DR per subsystem</text><rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E"/><text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Secrets recovery</text><text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Vault snapshot + KMS</text><rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5"/><text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">DNS failover</text><text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">Route 53 / Azure DNS</text><rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900"/><text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">stateful DR</text><text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">DB replication + restore</text><rect x="595" y="70" width="125" height="100" rx="10" fill="#5A6B81"/><text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">managed-svc</text><text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">RDS / Cosmos limits</text></svg>"""


LESSON = LessonSpec(
    num="04", title_short="secrets + DNS + stateful + managed DR", title_full="D4 · Secret Recovery + DNS Failover + Stateful Workload DR + Managed-Service DR Limits",
    title_html="K-ADV-DR D4 · Specialty DR", module_eyebrow="Module D4 · Cargo Recovery Office — specialty DR per subsystem",
    hero_sub_html='<strong>Secret recovery</strong>: external Vault snapshot; KMS key restoration; ESO re-syncs; ProviderConfig refresh. <strong>DNS failover</strong>: Route 53 / Azure DNS / Cloud DNS health-check + automatic record swap; TTL tuning. <strong>Stateful workload DR</strong>: DB replication (multi-AZ + cross-region); restore-tested; consistency model. <strong>Managed-service DR limits</strong>: RDS read-replica promotion; Cosmos DB multi-region; Spanner regional/multi-region; understand RPO + RTO of each.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Velero restored apps; PVCs back; but apps fail to start — secrets unavailable. <em>Vault was in same region; it\'s also down</em>. Today\'s lesson: each subsystem has its own DR pattern; coordinate the timeline.",
    stamp_html="<strong>Each subsystem has DR: secrets via Vault + KMS; DNS via Route 53; stateful via DB replication; managed services have built-in DR with limits. Understand each; coordinate timeline.</strong>",
    district_pin="kdr-cell04", district_label="Cargo Recovery Office",
    sections=[
        Section(eyebrow="Section 1.1 · secret recovery",
            h2="Vault + KMS + ESO chain",
            body_html="""    <p><strong>External Vault</strong>: HA across multiple regions; raft replication for snapshot; quarterly snapshot to immutable storage. <strong>KMS keys</strong>: cross-region replicas (AWS / Azure / GCP all support); root-of-trust survives single-region loss.</p>
    <p>Recovery: rebuild Vault in DR region from snapshot; rotate seal keys; KMS keys auto-replicated; <strong>External Secrets Operator (ESO)</strong> in new cluster re-syncs from Vault; K8s Secrets re-materialise.</p>
    <p>Without external Vault: K8s Secrets can be Velero-backed but tightly coupled to cluster; less flexible."""),
        Section(eyebrow="Section 1.2 · DNS failover",
            h2="Route 53 / Azure DNS + TTL + health checks",
            body_html="""    <p>DNS-based failover: <strong>Route 53</strong> health-check on primary endpoint; on failure, swap A record to DR LB. <strong>Azure DNS</strong> + Traffic Manager equivalent. <strong>GCP Cloud DNS</strong> + Global LB.</p>
    <p>TTL tuning: lower TTL (30-60s) on critical records for faster failover; trade DNS query load for fast failover. Pre-stage low TTL before known maintenance windows.</p>
    <p>External-DNS K8s controller automates DNS records from Service / Ingress; per-cluster setup syncs to managed DNS."""),
        Section(eyebrow="Section 1.3 · stateful workload DR",
            h2="DB replication + restore + consistency",
            body_html="""    <p>Self-managed DBs (PostgreSQL / MySQL operators):</p>
    <ul>
      <li>Multi-AZ replication (primary + 2 standbys via streaming).</li>
      <li>Cross-region streaming replica.</li>
      <li>Backup to S3 / Blob via cron-job (pg_basebackup / wal-g / pgbackrest / Percona XtraBackup).</li>
      <li>Restore-tested quarterly; consistency model (eventual / strong) understood.</li>
    </ul>
    <p>K8s operators (CloudNativePG / Zalando postgres-operator / Strimzi for Kafka): handle replication lifecycle. PVC + CSI snapshot for periodic capture."""),
        Section(eyebrow="Section 1.4 · managed-service DR limits",
            h2="RDS / Cosmos / Spanner — built-in but limited",
            body_html="""    <p><strong>AWS RDS / Aurora</strong>: multi-AZ standby (synchronous; in-region); cross-region read replica (async; promote on disaster); <strong>Aurora Global Database</strong> (async cross-region; minute RPO; global LB). RTO: minutes for promote.</p>
    <p><strong>Azure Cosmos DB</strong>: multi-region built-in; configurable consistency (Strong / Bounded Staleness / Session / Eventual / Consistent Prefix); auto-failover.</p>
    <p><strong>GCP Spanner</strong>: regional (1 region) or multi-region (5+ regions strong consistency); built-in; expensive.</p>
    <p><strong>Limits</strong>: cross-region promotion has data-loss window (RPO &gt; 0); restore-from-snapshot can be slow (TB-scale = hours); test for your data size."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why external Vault for secret recovery?",
            options=[("Faster.", False), ("Vault survives cluster loss; cross-region replicated; ESO re-syncs to new cluster.", True), ("Required by K8s.", False)],
            feedback="External Vault decouples secrets from cluster lifecycle. K8s Secrets in cluster die with cluster; external Vault lives on."),
        3: PauseCheck(question="Aurora cross-region read replica RPO?",
            options=[("Zero.", False), ("Async replication; RPO &gt; 0; typically seconds-to-minutes.", True), ("24 hours.", False)],
            feedback="Async = data not in DR until next replication cycle. Aurora Global Database = single-second RPO; standard cross-region read replica = minutes."),
    },
    before_after_before='<p>Pre-coordinated specialty DR: secrets vanish on cluster loss; DNS swap manual; DB DR vague; managed-service DR assumed-but-untested.</p>',
    before_after_after='<p>External Vault + KMS replication for secrets; Route 53 health-check failover for DNS; DB replication with restore-tested for stateful; managed-service DR understood + tested.</p>',
    before_after_caption='<p class="ba-caption"><em>Each subsystem has its own DR pattern; coordinate the timeline.</em></p>',
    analogy_intro_html='''<p>Cargo Recovery Office handles per-cargo-type recovery. Secrets cargo: separate vault in another region (Vault) + key copies (KMS). Routing cargo: signal flag tower (DNS + health check). Stateful cargo: replicated cargo holds (DB replication). Specialty cargo from vendors: each vendor has own recovery procedure (managed services).</p>''',
    translation_rows=[
        ("Separate vault in another region", "External Vault HA + KMS replicas"),
        ("Vault → ship handoff", "External Secrets Operator re-sync"),
        ("Signal flag tower failover", "Route 53 / Azure DNS / Cloud DNS health check"),
        ("Per-record signal speed", "DNS TTL tuning"),
        ("Replicated cargo holds", "DB streaming replication + cross-region replica"),
        ("Cargo manifest backup", "DB backups to S3 / Blob"),
        ("Vendor cargo recovery", "Managed services (RDS / Cosmos / Spanner)"),
        ("Vendor SLA limits", "Cross-region promotion RPO + RTO"),
    ],
    analogy_stops="A real vendor cargo procedure is well-documented; managed-service DR has gotchas (region-availability, restore-time-at-scale). Test before you need it.",
    eli5="Different cargo needs different recovery. Secrets in a vault elsewhere. Routing through a flag tower. Stateful cargo replicated. Vendor cargo per vendor procedure.",
    eli10="<strong>Secrets</strong>: external Vault HA + KMS replication + ESO re-sync. <strong>DNS</strong>: Route 53 / Azure DNS / Cloud DNS health-check failover; tune TTL. <strong>Stateful</strong>: DB replication + cross-region replica + backups + restore-tested. <strong>Managed services</strong>: RDS / Aurora Global / Cosmos DB / Spanner — built-in DR; understand RPO + RTO + restore time.",
    scenarios=[
        Scenario(name="External Vault saved DR", body="Cluster lost in us-east-1; Vault HA in us-east-1 + us-west-2; rebuild cluster in us-west-2; ESO re-syncs from Vault us-west-2; secrets immediately available."),
        Scenario(name="Route 53 failover automated DNS", body="Primary cluster ALB unhealthy; Route 53 health check fires; A record swaps to DR ALB within 60s. Tenants notice brief blip."),
        Scenario(name="Aurora Global Database for tier-1", body="Fintech runs Aurora Global across us-east-1 + us-west-2; RPO &lt; 1s; on disaster, promote DR to primary; RTO &lt; 1 min. Cost premium accepted for tier-1."),
        Scenario(name="Outage — assumed RDS DR worked", body="Pre-test: assumed RDS multi-AZ = enough. Real disaster: cross-region promotion took 2h. Postmortem: Aurora Global Database; cross-region promotion drilled.")
    ],
    misconceptions=[
        Misconception(myth="\"K8s Secrets are sufficient.\"", truth="Cluster loss = K8s Secrets gone. External Vault is the foundation; K8s Secrets are derived (via ESO) + ephemeral."),
        Misconception(myth="\"DNS TTL of 24h is OK.\"", truth="High TTL = slow DNS failover. Critical records: TTL 30-60s + accept higher DNS query cost."),
        Misconception(myth="\"Managed-service DR is automatic.\"", truth="Managed services offer DR features but require deliberate config + tested promotion. Aurora multi-AZ ≠ Aurora Global Database; understand the difference."),
    ],
    flashcards=[
        Flashcard(front="External Vault — why for DR?", back="Survives cluster loss. Cross-region HA + raft replication. KMS for seal keys cross-region replicated. ESO re-syncs on new cluster."),
        Flashcard(front="DNS failover tools per cloud?", back="<strong>AWS Route 53</strong> + health check. <strong>Azure DNS</strong> + Traffic Manager. <strong>GCP Cloud DNS</strong> + Global LB. Lower TTL (30-60s) for fast failover."),
        Flashcard(front="DB DR options self-managed?", back="Multi-AZ streaming replication; cross-region read replica; backups to S3 (pg_basebackup / wal-g / pgbackrest); CSI snapshots."),
        Flashcard(front="Aurora Global Database vs cross-region read replica?", back="<strong>Aurora Global</strong>: dedicated cross-region replication; RPO &lt; 1s; faster promote (~1 min). <strong>Cross-region read replica</strong>: standard async; RPO seconds-minutes; promote takes longer."),
        Flashcard(front="Cosmos DB consistency levels?", back="<strong>Strong</strong> (linearizable; highest cost), <strong>Bounded Staleness</strong>, <strong>Session</strong>, <strong>Consistent Prefix</strong>, <strong>Eventual</strong> (lowest cost)."),
        Flashcard(front="External-DNS K8s controller?", back="Watches Service / Ingress; syncs records to managed DNS (Route 53 / Cloud DNS / etc.). Automates DNS lifecycle."),
        Flashcard(front="Spanner DR shapes?", back="<strong>Regional</strong> (single region); <strong>multi-region</strong> (5+ regions; strong consistency; expensive)."),
        Flashcard(front="K8s DB operators?", back="<strong>CloudNativePG</strong> (CNCF), <strong>Zalando postgres-operator</strong>, <strong>Strimzi</strong> (Kafka). Handle replication + backup lifecycle."),
    ],
    quizzes=[
        Quiz(prompt="Design DR for an app with Postgres + Redis + Vault secrets + Route 53 DNS.",
            answer="(1) <strong>Postgres</strong>: CloudNativePG operator + cross-region streaming replica + pgbackrest to S3 + restore-tested quarterly. (2) <strong>Redis</strong>: Redis cluster mode + cross-region replication; ephemeral data accepts loss; alternative: Elasticache cross-region. (3) <strong>Vault</strong>: HA in 3 regions; auto-unseal via KMS (cross-region replicated). (4) <strong>DNS</strong>: Route 53 health check on app endpoint; auto-failover to DR LB; TTL 60s. (5) <strong>Coordination</strong>: runbook orders restore: Vault first → DB replicas promote → app + ESO syncs secrets → DNS swap. (6) <strong>Drill quarterly</strong>: measure end-to-end RTO."),
        Quiz(prompt="A team uses RDS multi-AZ. Region outage. Walk failover.",
            answer="(1) <strong>RDS multi-AZ alone</strong>: synchronous standby in same region; doesn\'t help cross-region. (2) <strong>If cross-region read replica configured</strong>: <code>aws rds promote-read-replica</code> in DR region; takes 5-15 min. (3) <strong>App reconfigure</strong>: connection strings point at promoted replica\'s endpoint. (4) <strong>Aurora Global Database</strong> would have been faster (~1 min promotion). (5) <strong>Postmortem</strong>: upgrade to Aurora Global for tier-1; document promote runbook + drill."),
        Quiz(prompt="The CFO sees Aurora Global cost premium (~30% over standard). Defend.",
            answer="\"<strong>Aurora Global Database is the difference between 1-min RTO + 2h RTO during region failure.</strong> Three considerations: (1) <strong>Tier-1 workloads</strong>: 30% premium = small vs cost of 2h customer-facing outage. (2) <strong>Synchronous replication</strong>: RPO &lt; 1s vs minutes for standard cross-region. (3) <strong>Auto-promote</strong>: graceful failover without scripts. <strong>For tier-2 / tier-3</strong>: standard cross-region read replica is fine. <strong>Cost-by-tier</strong>: tier-1 gold = Aurora Global; tier-2 silver = standard async; tier-3 bronze = backup-only.\"", cyoa=True, cyoa_tag="how the DR architect framed Aurora Global cost"),
    ],
    glossary=[
        GlossaryItem(name="External Vault HA", definition="HashiCorp Vault in HA across multiple regions; raft replication; cross-region snapshot."),
        GlossaryItem(name="KMS replication", definition="AWS KMS multi-region keys / Azure Key Vault geo-replicated / GCP KMS multi-region. Root-of-trust survives single-region loss."),
        GlossaryItem(name="External-DNS", definition="K8s controller syncing Service / Ingress records to managed DNS providers."),
        GlossaryItem(name="Route 53 health check", definition="AWS DNS health monitor; automatic record failover."),
        GlossaryItem(name="DNS TTL tuning", definition="Lower TTL (30-60s) for critical records = fast failover; trade DNS query load."),
        GlossaryItem(name="Aurora Global Database", definition="AWS Aurora cross-region with dedicated replication; RPO &lt; 1s; promote-time ~1 min."),
        GlossaryItem(name="Cosmos DB multi-region", definition="Azure built-in multi-region with configurable consistency."),
        GlossaryItem(name="Spanner multi-region", definition="GCP strong-consistency multi-region (5+ regions); expensive."),
        GlossaryItem(name="CloudNativePG", definition="CNCF PostgreSQL K8s operator; replication + backup + lifecycle."),
        GlossaryItem(name="pgbackrest / wal-g", definition="PostgreSQL backup tools; PITR + S3 storage; cross-region replication-friendly."),
    ],
    recap_lead="Specialty DR per subsystem: external Vault + KMS for secrets; Route 53 / Azure DNS health-check for DNS failover; DB replication for stateful; managed services have built-in DR with limits. Coordinate timeline + drill.",
    recap_next='<strong>Next — D5: Capstone — destroy + rebuild a complete production cluster.</strong>',
)
