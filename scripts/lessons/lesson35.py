from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Power Station resilience floor: a multi-zone redundant power grid, a PDB switch limiting how many generators can be down at once, and a regional DR map showing failover to a second city.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">POWER STATION · RESILIENCE FLOOR</text>
  <!-- Zones -->
  <g transform="translate(40,55)">
    <text x="120" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">MULTI-ZONE GRID</text>
    <rect x="0" y="22" width="80" height="80" rx="6" fill="#E0EEF3" stroke="#4A8FA8" stroke-width="1.5"/>
    <text x="40" y="38" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">zone-A</text>
    <rect x="6" y="44" width="68" height="14" rx="2" fill="#5A9F7A"/>
    <text x="40" y="55" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">3 replicas</text>
    <rect x="6" y="62" width="68" height="14" rx="2" fill="#5A9F7A"/>
    <text x="40" y="73" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">3 replicas</text>
    <rect x="80" y="22" width="80" height="80" rx="6" fill="#E0EFE6" stroke="#5A9F7A" stroke-width="1.5"/>
    <text x="120" y="38" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">zone-B</text>
    <rect x="86" y="44" width="68" height="14" rx="2" fill="#5A9F7A"/>
    <text x="120" y="55" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">3 replicas</text>
    <rect x="86" y="62" width="68" height="14" rx="2" fill="#5A9F7A"/>
    <text x="120" y="73" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">3 replicas</text>
    <rect x="160" y="22" width="80" height="80" rx="6" fill="#FBE8DC" stroke="#A04832" stroke-width="1.5"/>
    <text x="200" y="38" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">zone-C ✗</text>
    <rect x="166" y="44" width="68" height="14" rx="2" fill="#9D9389"/>
    <text x="200" y="55" text-anchor="middle" font-size="7" fill="#FBE8DC" font-weight="700">offline</text>
    <text x="120" y="118" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">66% capacity still serving</text>
  </g>
  <!-- PDB switch -->
  <g transform="translate(310,55)">
    <rect width="160" height="100" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">PodDisruptionBudget</text>
    <rect x="14" y="32" width="132" height="22" rx="2" fill="#5A9F7A"/>
    <text x="20" y="46" font-size="8" font-weight="700" fill="#FFFFFF">minAvailable: 6</text>
    <rect x="14" y="58" width="132" height="22" rx="2" fill="#A04832"/>
    <text x="20" y="72" font-size="8" font-weight="700" fill="#FFFFFF">block draining 7th pod</text>
    <text x="80" y="92" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">at most 2 disrupted at once</text>
  </g>
  <!-- DR map -->
  <g transform="translate(490,55)">
    <rect width="150" height="100" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="75" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">REGIONAL DR</text>
    <rect x="10" y="22" width="60" height="36" rx="3" fill="#5A9F7A"/>
    <text x="40" y="42" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">us-east</text>
    <text x="40" y="54" text-anchor="middle" font-size="7" fill="#FFFFFF">primary</text>
    <line x1="72" y1="40" x2="88" y2="40" stroke="#A04832" stroke-width="1.5" stroke-dasharray="2,2"/>
    <rect x="90" y="22" width="60" height="36" rx="3" fill="#9D9389"/>
    <text x="120" y="42" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">us-west</text>
    <text x="120" y="54" text-anchor="middle" font-size="7" fill="#FBE8DC">warm</text>
    <text x="75" y="78" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">RPO: 5 min</text>
    <text x="75" y="90" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">RTO: 15 min</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="35",
    title_short="reliability &amp; HA",
    title_full="Reliability & HA · PDB, Multi-Zone, Regional DR",
    title_html="Lesson 35 — Reliability & HA · K-COM",
    module_eyebrow="Module 15 · Lesson 35 · staying up when things break",
    hero_sub_html='Autoscaling matches capacity to demand. <strong>Reliability</strong> matches <em>availability</em> to <em>failures</em>: zone outages, node drains, individual Pod crashes, regional disasters. Three layers — <strong>PodDisruptionBudgets</strong>, <strong>multi-zone topology</strong>, <strong>regional disaster recovery</strong>.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='An availability zone fails. The cluster has 18 Pods of <code>checkout-service</code>. Topology spread is set, so Pods are distributed 6-6-6 across zones. Zone B fails → 12 healthy Pods remain. Service degrades briefly, then HPA scales up + Karpenter adds nodes, and full capacity returns within a minute. <em>The post-mortem is short: \"zone B failed; we noticed because monitoring told us; users saw 30 seconds of elevated latency.\"</em> Compare to the team without zone spread: 100% Pod loss, full outage, multi-hour recovery. Topology spread + PDBs + multi-zone is the reliability budget. This lesson is the toolkit.',
    stamp_html='Three layers: <strong>PodDisruptionBudget (PDB)</strong> caps voluntary disruptions (drains, autoscaler, upgrades). <strong>Topology spread + zone-aware autoscaling</strong> survives zone failures. <strong>Regional DR</strong> (multi-region GitOps + DNS-level failover, or active-active mesh) survives a region. Most outages are voluntary — get the PDB right, you avoid most of them.',
    district_pin="kt-pin34",
    district_label="Power Station — Resilience Floor",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Voluntary vs involuntary disruption",
            body_html="""    <p>Pods get killed for two kinds of reasons:</p>
    <ul>
      <li><strong>Voluntary disruption</strong> — node drain, cluster upgrade, deployment rollout, autoscaler scale-down. The cluster <em>chose</em> to disrupt this Pod. K8s respects <strong>PodDisruptionBudgets</strong> here; a PDB-protected workload can\'t be voluntarily killed if doing so would violate the budget.</li>
      <li><strong>Involuntary disruption</strong> — node hardware failure, kernel OOM, zone outage. The cluster didn\'t choose; it just happened. PDBs don\'t apply.</li>
    </ul>
    <p>Most outages in mature clusters are <em>voluntary disruptions gone wrong</em>: an upgrade that drained too many Pods at once, a Karpenter consolidation that nuked a service\'s only available zone, a manual node drain that ignored PDBs. The single biggest reliability investment is correctly-set PDBs — and they\'re cheap to write.</p>
    <p>For involuntary disruption, the answer is redundancy: spread across zones, replication, sometimes regions. The cluster can\'t prevent a hardware failure; it can ensure a hardware failure isn\'t a service failure.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · PodDisruptionBudgets",
            h2="The single most important reliability primitive",
            body_html="""    <p>A <strong>PDB</strong> says: \"during voluntary disruptions, keep at least N Pods of this Deployment available\" (or \"don\'t disrupt more than M at once\").</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: {name: checkout-pdb}
spec:
  selector: {matchLabels: {app: checkout}}
  minAvailable: 6        # never less than 6 ready
  # OR maxUnavailable: 2 # never more than 2 disrupted at once</code></pre>
    <p>Pick one of <code>minAvailable</code> or <code>maxUnavailable</code> — not both. Use <code>minAvailable</code> when you want a hard floor (\"6 must always be running\"). Use <code>maxUnavailable</code> when you want headroom for rollouts (\"only 25% can be down\").</p>
    <p>What PDBs actually do:</p>
    <ul>
      <li>Block <code>kubectl drain</code> on a node if it would violate the budget. Drain blocks until the violator is rescheduled elsewhere.</li>
      <li>Block <strong>cluster autoscaler</strong> + <strong>Karpenter</strong> consolidation that would violate the budget.</li>
      <li>Don\'t block involuntary disruptions (zone outage, node hardware failure).</li>
    </ul>
    <p>Common bug: PDB with <code>minAvailable: 100%</code>. The Deployment can never be drained for upgrades; cluster maintenance gets stuck. Set <code>minAvailable</code> to a number you can actually sustain (e.g., for a 3-replica service, <code>minAvailable: 2</code> = at most 1 down at a time).</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Multi-zone topology",
            h2="Surviving zone failures",
            body_html="""    <p>Lesson 22 covered topology spread. For reliability, the rules tighten:</p>
    <ul>
      <li><strong>Always</strong> spread by <code>topology.kubernetes.io/zone</code> with <code>maxSkew: 1</code>, <code>whenUnsatisfiable: DoNotSchedule</code>.</li>
      <li>Pair with a <code>maxUnavailable</code>-style PDB.</li>
      <li>Replicas should be ≥ zones (3 zones = ≥3 replicas) to actually populate every zone.</li>
      <li>For StatefulSets, use <code>volumeClaimTemplates</code> with a <code>WaitForFirstConsumer</code> StorageClass (Lesson 18). Otherwise the disk gets provisioned in one zone, the Pod can\'t schedule there, Pod stays Pending forever.</li>
    </ul>
    <p>Cluster-level practices:</p>
    <ul>
      <li>Cluster Autoscaler / Karpenter must be aware of zone limits — Karpenter NodePool can specify <code>topology.kubernetes.io/zone</code> in its requirements; the scheduler and Karpenter together keep nodes spread.</li>
      <li>Use <strong>Service<code>topologySpreadConstraints</code> with the <code>topology.kubernetes.io/zone</code> key</strong> for Service traffic to prefer same-zone targets (reduces inter-zone egress costs; needs careful failure-mode design).</li>
      <li>Make sure stateful storage (databases, queues) is multi-zone-aware: managed RDS Multi-AZ, regional Cloud SQL, multi-region Cassandra.</li>
    </ul>
    <p>The default state of a managed K8s cluster (EKS, GKE, AKS) in 2026 is multi-zone. Single-zone clusters are increasingly rare in production.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Regional DR — RPO, RTO, and choices",
            h2="When a region fails",
            body_html="""    <p>Multi-zone handles single-zone failures. <strong>Regional DR</strong> handles a whole region going down (rare, but it happens — AWS us-east-1 has a 90-minute outage in 2017, 2021, and 2024). Two metrics define the strategy:</p>
    <ul>
      <li><strong>RPO</strong> (Recovery Point Objective) — how much data loss is acceptable? \"Up to 5 minutes\" = sync state to DR every 5 min.</li>
      <li><strong>RTO</strong> (Recovery Time Objective) — how fast must you be back up? \"15 minutes\" = automated failover; \"1 hour\" = manual.</li>
    </ul>
    <p>Three patterns:</p>
    <ul>
      <li><strong>Cold DR</strong> — DR cluster exists but inactive. State backed up nightly. Failover involves spinning everything up. RPO: 24h, RTO: hours. Cheap; significant data loss possible.</li>
      <li><strong>Warm DR</strong> — DR cluster running but smaller. Continuous data replication. Failover scales up. RPO: minutes, RTO: 15-30 min. Moderate cost.</li>
      <li><strong>Active-Active</strong> — both regions serving traffic. Stateful tier replicates bidirectionally (Cassandra, CockroachDB, multi-region Spanner). RPO: 0, RTO: seconds. Expensive; complex consistency.</li>
    </ul>
    <p>Most enterprise-K8s setups in 2026 use <strong>warm DR with GitOps</strong>: same manifests deployed to two clusters in two regions; one is primary; database replicates across; DNS-level failover (Route53, Cloud DNS, Cloudflare) flips on detection. The exact same Deployment / Service / HPA / etc. lives in both clusters, deployed by the same Argo CD or Flux.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The real reliability practice: <strong>chaos engineering</strong>. Run periodic experiments — \"kill a zone,\" \"kill 50% of Pods,\" \"increase latency to one dependency\" — and verify the cluster recovers. Tools: Chaos Mesh, LitmusChaos. Without periodic testing, your DR plan is hypothesis. Game-day every quarter is the discipline difference between teams that survive incidents and teams that learn during them.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A team has a 6-replica Deployment with a PDB <code>minAvailable: 5</code>. They run <code>kubectl drain node-X</code> which has 4 of those Pods running on it. What happens?",
            options=[
                ("a) All 4 Pods drain immediately", False),
                ("b) Drain blocks: evicting the 2nd Pod would leave 4 available, violating minAvailable=5. Drain proceeds Pod by Pod, waiting for new replicas to come up before each eviction", True),
                ("c) Drain fails with an error", False),
            ],
            feedback="<strong>Answer: b.</strong> PDBs make drain wait for replacement Pods. The drain commits eventually but each eviction respects the budget. This is exactly the right behavior — protects availability during voluntary disruption.",
        ),
    },
    before_after_before='<p>Pre-PDB: rolling cluster upgrade kills 80% of replicas of a service in 30 seconds because the upgrade tooling didn\'t check budgets. Outage. Post-mortem: \"we should have been more careful.\" Single-zone deploys: zone failure = full outage. \"Disaster recovery\" = a 47-page wiki page nobody has tested.</p>',
    before_after_after='<p>PDBs on every production Deployment. Drains respect them; consolidation respects them; upgrades respect them. Multi-zone topology spread is mandatory; zone failures cause minutes of degradation, not hours of outage. Regional DR via warm-standby + GitOps; quarterly game-days verify it works.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">PDBs are the cheapest reliability investment in K8s — three lines of YAML per Deployment. Almost every \"K8s outage during a rollout\" story has a missing PDB at its core.</p>',
    analogy_intro_html='<p>The Power Station\'s resilience floor has three controls. The <strong>maintenance interlock</strong> (PDB) prevents the operator from taking too many generators offline at once — \"you must keep 6 running; before you take generator 7 offline, you have to start a replacement.\" The <strong>multi-zone wiring</strong> (topology spread + zone-aware nodes) ensures your generators are spread across the city\'s three districts so a district outage doesn\'t kill all of them. The <strong>regional substation</strong> (DR) is the second power station in a different city, kept warm, ready to take over when this city\'s station goes dark. Three layers, each handles a different failure scope.</p>',
    translation_rows=[
        ("Maintenance interlock", "<code>PodDisruptionBudget</code>"),
        ("\"You must keep 6 running\"", "<code>minAvailable: 6</code>"),
        ("\"At most 2 down at once\"", "<code>maxUnavailable: 2</code>"),
        ("Generators spread across districts", "Topology spread by zone"),
        ("Hardware failure (involuntary)", "Pod killed by zone/node failure"),
        ("Operator-initiated maintenance (voluntary)", "Pod evicted by drain / autoscaler / upgrade"),
        ("Second power station in another city", "Regional DR cluster"),
        ("How fresh is the second city\'s data?", "RPO (Recovery Point Objective)"),
        ("How fast can the second city take over?", "RTO (Recovery Time Objective)"),
        ("Practising failover quarterly", "Chaos engineering / game-days"),
    ],
    analogy_stops="The analogy stops here: real K8s disruption is bound by Linux process termination + Pod lifecycle, not generators. And regional DR depends heavily on stateful tier (databases, message queues) being designed to replicate — without that, the K8s layer alone can\'t fail over.",
    eli5='Three rules for keeping the lights on. (1) Don\'t turn off too many bulbs at the same time. (2) Spread bulbs across rooms. (3) Have a backup house with a backup set of bulbs.',
    eli10="Voluntary disruption (drains, upgrades) is bounded by PDBs. Involuntary disruption (hardware failure) is mitigated by replication + topology spread. Multi-zone is mandatory for production; replicas ≥ zones; PVCs use WaitForFirstConsumer SCs. Regional DR has three patterns: cold (cheap, slow), warm (moderate), active-active (expensive, fast). RPO + RTO define the trade. Practice failover quarterly; without testing, your DR plan is fiction.",
    scenarios=[
        Scenario(name="A SaaS surviving a zone outage in 30 seconds", body="6-replica Deployment, topology spread by zone (3-3-3), PDB minAvailable=4, 3-zone EKS cluster. Zone-A goes down. 4 healthy Pods continue serving (slightly degraded throughput). HPA scales up; Karpenter provisions in zones B/C. Within 60 seconds, full capacity restored. Engineers see the alert + the auto-recovery in the same minute."),
        Scenario(name="A bank running active-active across us-east-1 and us-west-2", body="Two clusters, identical Argo CD deploys. CockroachDB across regions for stateful tier; Cassandra for high-write traffic. AWS Global Accelerator routes by latency. Half the traffic each region. Quarterly game-day: take down us-east-1 entirely; verify us-west-2 absorbs 100% of traffic. Last 4 game-days: clean."),
        Scenario(name="A startup with cold DR (cheap)", body="Primary cluster only. Nightly Velero backups to S3. Manifests in git via Argo CD. DR runbook: spin up new cluster, restore Velero backup, point DNS. RTO: ~4 hours. RPO: ~24 hours. Sufficient for their stage; will upgrade to warm DR pre-IPO."),
        Scenario(name="A platform team running quarterly chaos days", body="Chaos Mesh experiments scheduled monthly: random Pod kills, network partitions, simulated zone outages. Findings drive PDB tightening, dashboards, runbooks. After 4 chaos days, MTTR for production incidents dropped 60%. \"What we learned in chaos\" became a KPI."),
    ],
    misconceptions=[
        Misconception(myth="PDBs prevent all Pod kills.", truth="PDBs only block <em>voluntary</em> disruptions (drain, autoscaler, upgrade). Hardware/zone failures bypass PDBs entirely. PDBs are reliability for planned changes, not disasters."),
        Misconception(myth="Topology spread alone is enough.", truth="Topology spread without a PDB means an upgrade can still kill all your Pods at once if it bypasses budgets. Pair them. Spread for placement; PDB for disruption rate."),
        Misconception(myth="DR = backup.", truth="Backup is data recovery. DR is service continuity. Backups don\'t mean fast recovery — restoring 10 TB of database from S3 is 12+ hours. DR means active redundancy that can take over fast."),
    ],
    flashcards=[
        Flashcard(front="Voluntary vs involuntary disruption?", back="Voluntary: cluster chose (drain, autoscaler, upgrade). Bounded by PDBs. Involuntary: just happened (hardware, zone). PDBs don\'t apply; redundancy + spread does."),
        Flashcard(front="PDB minAvailable vs maxUnavailable?", back="Pick one. <code>minAvailable</code>: hard floor (\"keep ≥ N ready\"). <code>maxUnavailable</code>: bounded disruption (\"≤ M down at once\"). Both express the same idea differently; pick whichever reads clearer for your case."),
        Flashcard(front="When does a PDB matter?", back="During <code>kubectl drain</code> on a node with PDB-protected Pods. During cluster autoscaler / Karpenter consolidation. During controlled upgrades. NOT during involuntary failures."),
        Flashcard(front="Topology spread for HA?", back="<code>topologyKey: topology.kubernetes.io/zone</code>, <code>maxSkew: 1</code>, <code>whenUnsatisfiable: DoNotSchedule</code>. Add a similar hostname spread for in-zone protection. Replicas ≥ zones."),
        Flashcard(front="Why WaitForFirstConsumer for StatefulSets?", back="Topology spread schedules a Pod in a zone first; the PVC is then provisioned in the same zone. With <code>Immediate</code> binding mode, the PVC could land in a zone the Pod can\'t reach — Pod stays Pending forever."),
        Flashcard(front="RPO vs RTO?", back="RPO = Recovery Point Objective (max acceptable data loss). RTO = Recovery Time Objective (max acceptable downtime). Both expressed in time. Both drive DR strategy."),
        Flashcard(front="Cold / warm / active-active DR?", back="Cold = standby exists, manual failover (RTO hours). Warm = standby running smaller, automated scale-up (RTO 15-30 min). Active-active = both serving (RTO seconds, expensive, complex)."),
        Flashcard(front="What is chaos engineering?", back="Practice of injecting failures (Pod kills, network partitions, zone outages) to verify the system recovers. Tools: Chaos Mesh, LitmusChaos. Without it, your DR plan is hypothesis."),
    ],
    quizzes=[
        Quiz(prompt="A team\'s 5-replica Deployment has <code>minAvailable: 5</code>. They run an upgrade. The upgrade hangs for 30 minutes. Diagnosis?", answer="The PDB is set so tight that <strong>no</strong> Pod can be evicted: any eviction would drop available below 5. Fix: change to <code>minAvailable: 4</code> (one can be down) or <code>maxUnavailable: 1</code>. <strong>General rule:</strong> always allow at least one Pod-worth of disruption headroom for upgrades + drains. Otherwise the cluster gets stuck and ops humans bypass the PDB (defeating the purpose) to make progress."),
        Quiz(prompt="A team\'s StatefulSet uses <code>volumeClaimTemplates</code> with a default StorageClass that has <code>volumeBindingMode: Immediate</code>. They configure topology spread by zone. After deploy, half the Pods are Pending. Diagnosis?", answer="<strong>Classic combo bug.</strong> With Immediate binding, the PVC is provisioned <em>before</em> the Pod is scheduled — and it lands in some zone (often us-east-1a). Topology spread then tries to schedule the Pod in another zone (us-east-1b) — but cloud block storage can\'t cross zones. Pod is Pending. <strong>Fix:</strong> change StorageClass to <code>volumeBindingMode: WaitForFirstConsumer</code>. The scheduler picks the Pod\'s zone first; PVC is provisioned in the same zone. Always WaitForFirstConsumer in multi-zone clusters."),
        Quiz(prompt="The CISO mandates a quarterly DR test. Design the runbook. <strong>Click for the playbook. ▼</strong>", cyoa=True, cyoa_tag="the playbook", answer="<strong>Pre-test:</strong> communicate. \"Game day at 2 PM Wednesday — DR cluster will be promoted, primary disabled.\" Stakeholders, support, customer comms team aware. <strong>Step 1 — Capture state.</strong> RPO check: when was the last DB replication? Note the timestamp. <strong>Step 2 — Trigger the failure.</strong> AWS console: terminate primary cluster\'s zone(s) or stop the EKS control plane (or simulate it via DNS-level failover script). <strong>Step 3 — Watch automated recovery.</strong> Monitor: did DNS flip? Did warm-standby cluster scale up? How long did it take? Did any user requests fail? <strong>Step 4 — Verify functionality.</strong> Smoke test: login, checkout, search. Watch synthetic monitoring. <strong>Step 5 — Verify data integrity.</strong> Pull a recent record from primary and DR; verify they match (within RPO bound). <strong>Step 6 — Failback.</strong> Once confident, restore primary; flip DNS back. Verify no data loss in either direction. <strong>Step 7 — Post-mortem.</strong> What went well? What broke? What\'s the action list? Update runbooks; tighten alerts; fix gaps. <strong>Cadence:</strong> quarterly. The teams that survive real outages are the ones for whom failover is muscle memory, not theory."),
    ],
    glossary=[
        GlossaryItem(name="PodDisruptionBudget (PDB)", definition="API object: cap voluntary disruptions for selected Pods. minAvailable or maxUnavailable."),
        GlossaryItem(name="Voluntary disruption", definition="Pod eviction the cluster initiated: drain, autoscaler, upgrade. PDBs apply."),
        GlossaryItem(name="Involuntary disruption", definition="Pod killed without cluster choice: hardware, zone, kernel OOM. PDBs don\'t apply."),
        GlossaryItem(name="Topology spread", definition="Schedule replicas evenly across topology buckets (zone, hostname). Lesson 22."),
        GlossaryItem(name="WaitForFirstConsumer", definition="StorageClass binding mode: provision PV in same zone as the consuming Pod. Required for multi-zone."),
        GlossaryItem(name="RPO", definition="Recovery Point Objective. Max acceptable data loss in a disaster."),
        GlossaryItem(name="RTO", definition="Recovery Time Objective. Max acceptable downtime."),
        GlossaryItem(name="Cold DR", definition="Standby site exists but inactive. Cheap; slow recovery."),
        GlossaryItem(name="Warm DR", definition="Standby running smaller; data replicated. Moderate cost; minutes RTO."),
        GlossaryItem(name="Active-active", definition="Both sites serving. RTO seconds; expensive; needs careful consistency."),
        GlossaryItem(name="Chaos engineering", definition="Practice of injecting failures to verify recovery. Chaos Mesh, LitmusChaos."),
        GlossaryItem(name="Velero", definition="Backup tool for K8s objects + persistent volumes. Common in cold-DR strategies."),
    ],
    recap_lead="PDBs cap voluntary disruptions; topology spread + multi-zone survives zone failures; regional DR (warm or active-active) survives a region. The cheapest reliability investment is a correctly-set PDB on every production Deployment.",
    recap_next="<strong>Next — Lesson 36: Kustomize.</strong> Module 16 begins — application delivery. New K-Town district: Print Shop. Why YAML duplication is the single biggest source of Ops toil, and how Kustomize\'s overlay model addresses it.",
)
