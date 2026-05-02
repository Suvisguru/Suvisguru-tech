from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Power station: a bank of meters reading CPU/memory/queue depth, controls labeled HPA/VPA/KEDA, and the substation outside connected to a Karpenter / Cluster Autoscaler that adds or removes generators (nodes).">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">POWER STATION · DEMAND-BASED CAPACITY</text>
  <!-- Meters -->
  <g transform="translate(40,55)">
    <text x="100" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">DEMAND METERS</text>
    <rect x="0" y="22" width="200" height="24" rx="3" fill="#E0EEF3" stroke="#4A8FA8" stroke-width="1"/>
    <text x="6" y="38" font-size="8" fill="#3F4A5E" font-weight="700">HPA · CPU/mem/custom</text>
    <rect x="0" y="50" width="200" height="24" rx="3" fill="#FBE8DC" stroke="#A04832" stroke-width="1"/>
    <text x="6" y="66" font-size="8" fill="#A04832" font-weight="700">VPA · resize Pod requests</text>
    <rect x="0" y="78" width="200" height="24" rx="3" fill="#E0EFE6" stroke="#3D7857" stroke-width="1"/>
    <text x="6" y="94" font-size="8" fill="#3D7857" font-weight="700">KEDA · queue depth, events</text>
  </g>
  <!-- Substation -->
  <g transform="translate(280,55)">
    <rect width="200" height="120" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="100" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">SUBSTATION · NODE COUNT</text>
    <rect x="14" y="32" width="172" height="22" rx="2" fill="#5A9F7A"/>
    <text x="20" y="46" font-size="8" font-weight="700" fill="#FFFFFF">Cluster Autoscaler · classic</text>
    <rect x="14" y="58" width="172" height="22" rx="2" fill="#A04832"/>
    <text x="20" y="72" font-size="8" font-weight="700" fill="#FFFFFF">Karpenter · modern, fast</text>
    <text x="100" y="100" text-anchor="middle" font-size="8" fill="#FBF1D6" font-style="italic">adds/removes nodes</text>
    <text x="100" y="112" text-anchor="middle" font-size="8" fill="#FBF1D6" font-style="italic">based on Pending Pods</text>
  </g>
  <!-- Generators -->
  <g transform="translate(500,55)">
    <text x="70" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">GENERATORS · nodes</text>
    <rect x="0" y="22" width="60" height="40" rx="4" fill="#5A9F7A"/>
    <text x="30" y="42" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">m6.large</text>
    <text x="30" y="55" text-anchor="middle" font-size="7" fill="#FBE8DC">on-demand</text>
    <rect x="80" y="22" width="60" height="40" rx="4" fill="#E8B547"/>
    <text x="110" y="42" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">m6.spot</text>
    <text x="110" y="55" text-anchor="middle" font-size="7" fill="#5A4F45">cheap+evictable</text>
    <rect x="0" y="72" width="60" height="40" rx="4" fill="#A04832"/>
    <text x="30" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">g5.gpu</text>
    <text x="30" y="105" text-anchor="middle" font-size="7" fill="#FBE8DC">specialty</text>
    <rect x="80" y="72" width="60" height="40" rx="4" fill="#9D9389" stroke="#5A4F45" stroke-width="1.5" stroke-dasharray="3,2"/>
    <text x="110" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">+ new</text>
    <text x="110" y="105" text-anchor="middle" font-size="7" fill="#FBE8DC">on-demand</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="34",
    title_short="autoscaling",
    title_full="Autoscaling · HPA, VPA, KEDA, Cluster Autoscaler, Karpenter",
    title_html="Lesson 34 — Autoscaling · K-COM",
    module_eyebrow="Module 15 · Lesson 34 · matching capacity to demand",
    hero_sub_html='Two scaling questions. <strong>How many replicas?</strong> — answered by HPA / VPA / KEDA at the workload level. <strong>How many nodes?</strong> — answered by Cluster Autoscaler or Karpenter at the cluster level. Together they let the cluster grow + shrink to match real demand without over-provisioning.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Black Friday at 3 PM. Traffic 5× normal. The Deployment is at <code>replicas: 4</code> — fixed. CPU is pinned at 100%; latency rising; HPA isn\'t configured. Manual scale-up to <code>replicas: 20</code> — but cluster is full. Cluster Autoscaler isn\'t configured either. Engineer manually adds nodes via the cloud console while traffic continues to spike. 47 minutes of degradation. <em>Both layers of autoscaling needed to be in place</em>. Today\'s lesson is how to set up both correctly so 3 AM Black Friday doesn\'t exist for you next year.',
    stamp_html='<strong>Workload scaling</strong>: HPA (CPU/memory/custom metrics), VPA (right-size requests), KEDA (event-based — queue depth, Kafka lag, etc.). <strong>Cluster scaling</strong>: Cluster Autoscaler (legacy, node-group based) or <strong>Karpenter</strong> (modern, fast, picks instance type per Pending Pod). Combine for end-to-end scaling.',
    district_pin="kt-pin34",
    district_label="Power Station — Demand-Based Capacity",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Two scaling layers, two different problems",
            body_html="""    <p><strong>Workload scaling</strong> answers \"how many replicas of this Deployment do I need?\" Driven by signals: CPU, memory, queue depth, RPS, custom metrics. Adjusts the <code>replicas</code> field on Deployments / StatefulSets.</p>
    <p><strong>Cluster scaling</strong> answers \"how many nodes does the cluster need?\" Driven by Pending Pods (\"there are Pods that don\'t fit, add nodes\") and idle nodes (\"this node has no Pods, remove it\"). Adjusts the cloud auto-scaling group / instance fleet.</p>
    <p>The two interact. Scaling Pods up creates Pending Pods → triggers cluster scale-up. Scaling Pods down empties nodes → triggers cluster scale-down. Get one without the other and you either over-spend (lots of nodes, few Pods) or have outages (lots of Pods, no nodes).</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · HPA — the workhorse",
            h2="Replica scaling on metrics",
            body_html="""    <p><strong>Horizontal Pod Autoscaler (HPA)</strong> scales the replica count based on observed metrics. Built-in metrics: CPU and memory utilisation as % of requests. External / custom metrics: anything Prometheus can serve via the Prometheus Adapter or external metrics adapter.</p>
    <p>The math: \"if the average CPU per replica is 80% but target is 50%, increase replicas to bring the average down.\" Specifically: <code>desired = ceil(current_replicas × current_metric / target_metric)</code>.</p>
    <p>Modern HPA (autoscaling/v2) supports:</p>
    <ul>
      <li><strong>Multiple metrics</strong> — scale to whichever requires more replicas (CPU OR queue depth, take the max).</li>
      <li><strong>Behaviour</strong> — separate scale-up and scale-down policies. Scale up fast (double per minute) to handle spikes; scale down slow (10% per 5 min) to avoid flapping.</li>
      <li><strong>Stabilisation windows</strong> — \"don\'t scale down until the lower number is sustained for 5 minutes.\"</li>
    </ul>
    <p>Common mistakes:</p>
    <ul>
      <li>HPA without resource requests on the Pods — HPA can\'t calculate utilisation; it does nothing.</li>
      <li>HPA on a Deployment that uses <code>replicas:</code> in the manifest — the next <code>kubectl apply</code> resets to the manifest value, fighting HPA. Use a HelmChart that omits replicas, or detach replicas from GitOps drift detection.</li>
      <li>Memory-based HPA on apps that don\'t release memory — replicas only grow.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.7 · VPA and KEDA",
            h2="Two specialised cousins of HPA",
            body_html="""    <p><strong>Vertical Pod Autoscaler (VPA)</strong> doesn\'t change replica count — it changes per-Pod resource requests. The recommender component watches actual usage; over time, it suggests \"this Pod uses 200m CPU on average; you have 500m requested; lower it to 250m.\" The updater component evicts Pods to apply the new sizing.</p>
    <p>VPA modes:</p>
    <ul>
      <li><code>Off</code> — recommend only; don\'t apply.</li>
      <li><code>Initial</code> — apply at Pod creation time.</li>
      <li><code>Auto</code> / <code>Recreate</code> — evict + recreate Pods to apply.</li>
      <li><code>InPlaceOrRecreate</code> (1.33+) — try in-place resize without evicting; fall back if the kernel doesn\'t allow it.</li>
    </ul>
    <p>VPA\'s sweet spot: workloads with predictable resource usage where right-sizing yields cost savings. Avoid for HPA-targeted workloads (HPA + VPA fighting each other).</p>
    <p><strong>KEDA</strong> (Kubernetes Event-Driven Autoscaling) extends HPA with custom \"scalers\": Kafka lag, RabbitMQ queue depth, Postgres row count, S3 object count, Azure Event Hubs, GCP Pub/Sub, AWS SQS, and 60+ more. KEDA can scale a Deployment to <strong>zero</strong> when there\'s no work — perfect for event-driven workloads. It then re-creates Pods on first event arrival.</p>
    <p>KEDA is now widely deployed for: queue workers, scheduled batch jobs that should disappear off-hours, ML inference services with bursty demand, and serverless-style K8s workloads.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Cluster scaling — Karpenter beats Cluster Autoscaler",
            h2="The most consequential ops change of 2024-26",
            body_html="""    <p><strong>Cluster Autoscaler (CA)</strong> is the original. Watches for Pending Pods; if any can\'t fit, scales up the matching auto-scaling group (ASG). Scales down idle nodes. Works fine; predictable.</p>
    <p><strong>Karpenter</strong> (AWS-originated, now multi-cloud) is the modern replacement:</p>
    <ul>
      <li><strong>No node groups required</strong> — Karpenter picks the best instance type per Pending Pod. \"Need 2 GPUs and 32 GiB? I\'ll spin up a g5.xlarge. 0.25 CPU and 256 MiB? I\'ll use a t3.nano.\"</li>
      <li><strong>Faster</strong> — Karpenter spins up nodes in 20-40 seconds. CA goes through ASG APIs and is typically 60-120s.</li>
      <li><strong>Cost-aware</strong> — picks the cheapest instance that fits constraints; tracks spot prices.</li>
      <li><strong>Consolidation</strong> — periodically checks if running nodes can be replaced with fewer/cheaper ones; drains and recreates.</li>
      <li><strong>Multi-cloud</strong> — originally AWS, now production-ready on Azure (KAITO derivatives) and GCP.</li>
    </ul>
    <p>Karpenter\'s trade-off: more dynamic node identities (\"one node per Pod request\" can mean many small nodes) — operational tooling that assumes long-lived nodes (e.g., manual SSH, node-bound persistent state) doesn\'t fit. Most teams adopt Karpenter and design around it.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The 2026 default for new EKS clusters is Karpenter, not CA. AWS has been pushing it heavily. The migration story (CA → Karpenter) is straightforward: install Karpenter, let it manage new nodes, drain old ASG nodes, decommission CA. Most clusters complete the migration in a sprint.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A team configures HPA on their Deployment but forgets to set <code>resources.requests.cpu</code> on the Pods. The HPA shows <code>&lt;unknown&gt;</code> for current utilisation and never scales. Why?",
            options=[
                ("a) HPA needs a metrics-server install", False),
                ("b) HPA calculates utilisation as a percentage of <code>resources.requests</code> — without a request, there\'s no denominator", True),
                ("c) HPA only works for stateless workloads", False),
            ],
            feedback="<strong>Answer: b.</strong> HPA computes <code>current_utilisation / target_utilisation</code> where current is measured CPU and the comparison is against the request. No request = no comparison = HPA is inert. <strong>Always set resource requests when using HPA.</strong>",
        ),
    },
    before_after_before='<p>Pre-autoscaling: hand-tuned <code>replicas: 8</code>. Over-provisioned for normal load (4-5 replicas would do); under-provisioned for peaks (need 30 replicas). Cluster nodes provisioned for max + headroom; expensive idle capacity 90% of the time. Manual scale-up during incidents. Frequent fights between dev (\"we need more capacity\") and finance (\"why is the cluster bill so high?\").</p>',
    before_after_after='<p>HPA on every Deployment based on actual demand signals. KEDA scales queue workers 0 → 50 based on actual queue depth. Karpenter spins up the cheapest instance type per Pending Pod, consolidates idle capacity. Cluster bill drops 30-50% while peak handling improves. Finance and dev are friends.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Karpenter\'s 2024-26 dominance turned cluster-autoscaling from \"sluggish ASG churn\" into \"actually-real-time capacity matching.\" New clusters default to it; old clusters migrate.</p>',
    analogy_intro_html='<p>The Power Station district runs K-Town\'s capacity. Inside, three demand meters tell the operator how loaded the system is. The <strong>load meter</strong> (HPA) shows \"current generators are at 80% capacity — fire up another\" — and adjusts the number of <em>generators</em> running. The <strong>generator-size meter</strong> (VPA) says \"this generator was sized for 1000 kW but uses 400 — replace it with a smaller one.\" The <strong>queue meter</strong> (KEDA) watches incoming work orders: \"50 customers waiting; spin up a few more dedicated lines.\" Outside, the substation manager (Cluster Autoscaler / Karpenter) handles the actual generators — when the operator says \"more capacity!\" they procure additional generators from the city\'s rental fleet, picking the cheapest fit.</p>',
    translation_rows=[
        ("The load meter", "<code>HorizontalPodAutoscaler</code> (HPA)"),
        ("The generator-size meter", "<code>VerticalPodAutoscaler</code> (VPA)"),
        ("The queue meter", "<strong>KEDA</strong>"),
        ("Generator (running unit of capacity)", "Pod replica"),
        ("The substation manager", "<strong>Karpenter</strong> / <strong>Cluster Autoscaler</strong>"),
        ("Generator rental fleet", "Cloud instance fleet (EC2, Compute Engine, etc.)"),
        ("Picking generator type per order", "Karpenter NodeClass / NodePool selection"),
        ("Combining old generators into fewer big ones", "Karpenter consolidation"),
        ("Generator running on cheaper short-term contract", "Spot instances"),
    ],
    analogy_stops="The analogy stops here: Pods aren\'t generators; their state matters (StatefulSet ordinality, PVC binding, in-flight requests). Naive scale-down is destructive — Pod-disruption-budgets + graceful termination matter. Lesson 35 covers the reliability side.",
    eli5='Two thermostats. One says how many lights to turn on (more people = more lights). One says how many extra rooms to open in the house (more people = more rooms). Together they keep things just right.',
    eli10="Workload scaling: HPA (replica count by CPU/memory/custom metrics), VPA (per-Pod request right-sizing), KEDA (event-driven scalers — queue depth, Kafka lag, etc., scale-to-zero supported). Cluster scaling: Cluster Autoscaler (legacy, node-group based) or Karpenter (modern, picks instance type per Pending Pod, faster, cost-aware, consolidation). HPA needs resource requests to compute utilisation. Don\'t pair HPA + VPA on the same Pod (they fight). For 2026 EKS clusters, default to Karpenter.",
    scenarios=[
        Scenario(name="A SaaS using HPA + Karpenter", body="HPA on every Deployment based on CPU + custom metric (request rate via Prometheus Adapter). Karpenter dynamically provisions m6i (general) and t3 (burstable) instances based on Pod size. Spot instances for stateless. Black Friday spike handled in 90 seconds end-to-end (Pod scale + node scale)."),
        Scenario(name="A bank with KEDA-driven Kafka workers", body="Stream-processing service scales 0 → 100 based on Kafka consumer lag. KEDA scaler reads lag from Prometheus; HPA derived from KEDA scales the Deployment. Off-hours: 0 Pods. Lag detected: scale to 50 within 30 seconds. Total cost saved per quarter: significant."),
        Scenario(name="A startup using VPA in Initial mode", body="VPA recommends; only applies at Pod creation (no live evictions). Engineers see VPA recommendations on a Grafana panel; review weekly. New deploys get the right-sized requests automatically. Existing Pods kept until rolling deploy. CPU/memory waste cut by 40%."),
        Scenario(name="A team migrating CA → Karpenter", body="Old: 4 ASGs (general / memory / GPU / spot). Karpenter replaces with 4 NodePools, but lets it pick instance types within each. Spinup time dropped from 90s to 30s. Idle capacity dropped (Karpenter consolidates). Operational tooling that SSH\'d into specific node names broke; rewrote to use kubectl-only instead."),
    ],
    misconceptions=[
        Misconception(myth="HPA + VPA on the same Pod is more powerful.", truth="They\'ll fight: HPA decides \"need more replicas because CPU is high\" while VPA decides \"increase per-Pod CPU request because actual usage is high.\" Both can work simultaneously only with VPA in <code>Off</code>/<code>Initial</code> mode (recommend, apply at create) — never with VPA <code>Auto</code>."),
        Misconception(myth="KEDA replaces HPA.", truth="KEDA <em>extends</em> HPA. KEDA scalers compute \"desired replicas\" then create an HPA object on your behalf. Underneath, it\'s still HPA. KEDA\'s value is the scaler library + scale-to-zero."),
        Misconception(myth="Karpenter is AWS-only.", truth="Originally yes; in 2026 supported on Azure (with Microsoft\'s KAITO + community drivers), GCP (community), and being explored on others. AWS is still the strongest support; new on other clouds."),
    ],
    flashcards=[
        Flashcard(front="Two scaling layers?", back="Workload (replicas: HPA, VPA, KEDA). Cluster (nodes: Cluster Autoscaler, Karpenter). Need both for end-to-end scaling."),
        Flashcard(front="HPA math?", back="<code>desired_replicas = ceil(current_replicas × current_metric / target_metric)</code>. Computed on average across replicas. Driven by metrics-server + (optionally) Prometheus Adapter for custom metrics."),
        Flashcard(front="HPA without resource requests?", back="Doesn\'t work. HPA computes utilisation as <code>current / requested</code>; no request = no denominator = no scaling."),
        Flashcard(front="What is VPA?", back="Vertical Pod Autoscaler. Adjusts per-Pod <code>resources.requests</code> based on observed usage. Three modes: Off (recommend), Initial (apply at create), Auto (evict + recreate)."),
        Flashcard(front="What is KEDA?", back="Kubernetes Event-Driven Autoscaling. Extends HPA with 60+ event-based scalers: Kafka, RabbitMQ, queue depth, Pub/Sub, etc. Scale-to-zero supported."),
        Flashcard(front="Cluster Autoscaler vs Karpenter?", back="CA: ASG-based, slower (60-120s), node-group constrained. Karpenter: dynamic, fast (20-40s), picks instance type per Pod, cost-aware consolidation. Karpenter is the 2026 default."),
        Flashcard(front="Karpenter NodeClass / NodePool?", back="NodeClass: cloud-specific config (subnets, security groups, AMI). NodePool: general scaling parameters (instance types allowed, taints to apply, limits)."),
        Flashcard(front="Spot instance scheduling?", back="Karpenter has first-class spot support. Mark NodePool with spot capacity, deal with eviction notices via PodDisruptionBudgets + graceful termination. Often 50-80% cost savings on tolerant workloads."),
    ],
    quizzes=[
        Quiz(prompt="A team\'s HPA is configured with <code>targetCPUUtilizationPercentage: 70</code>. Their replicas keep flapping between 4 and 6. What\'s the diagnosis?", answer="Likely diagnoses: <strong>(1) Stabilization windows missing.</strong> Default scale-down stabilization is 5 min; scale-up is 0. If your traffic oscillates around the threshold, replicas oscillate. <strong>Fix:</strong> set <code>behavior.scaleDown.stabilizationWindowSeconds: 300</code> + slower scale-down policies. <strong>(2) Scale up too aggressive.</strong> Default scale-up policy is +100% per 15s. Once it scales up, CPU dips below 70%, then scales down, then traffic comes back. <strong>Fix:</strong> tune scale-up to +25% per 60s. <strong>(3) Resource requests too low.</strong> If CPU request is 100m and actual is 80m, you\'re at 80% utilisation; small changes flip the threshold. <strong>Fix:</strong> set requests at the 50th percentile of actual usage. <strong>(4) Replicas too few.</strong> With 4 replicas, one Pod\'s CPU spike moves the average significantly. With 10 replicas, the same spike is barely visible. <strong>Fix:</strong> raise minReplicas to a level where one Pod is &lt; 20% of total."),
        Quiz(prompt="A team\'s KEDA scaler reads from a Postgres queue (count of unprocessed rows). They scale 1 → 50. After deployment, replicas climb to 50 even when the queue is empty. What\'s wrong?", answer="<strong>Possibilities:</strong> (1) Their KEDA scaler query: <code>SELECT count(*) FROM jobs WHERE status = \'pending\'</code>. The <code>'pending'</code> string was written as <code>'PENDING'</code> in the table. Query returns wrong count → scale incorrectly. <strong>(2)</strong> The KEDA poll interval is too long; queue is empty briefly between bursts but KEDA hasn\'t re-checked. <strong>(3)</strong> KEDA is configured with a <code>cooldownPeriod</code> set too high; replicas stay scaled-up for 30 minutes after queue empties. <strong>Diagnosis:</strong> <code>kubectl describe scaledobject</code> — look at <code>Conditions</code> + <code>currentMetricValue</code>. <code>kubectl logs deploy/keda-operator</code> — actual scaler queries + responses. <strong>Fix:</strong> validate the query directly against the database; tune cooldown to 1-2 min for fast-changing queues."),
        Quiz(prompt="The platform team is migrating from Cluster Autoscaler to Karpenter on a 200-node EKS cluster. <strong>Click for the migration playbook. ▼</strong>", cyoa=True, cyoa_tag="the migration playbook", answer="<strong>Phase 1 — Install Karpenter alongside CA.</strong> Both run; CA continues to manage existing ASGs; Karpenter handles new NodePools you define. <strong>Phase 2 — Define NodePools.</strong> Mirror the ASG shape: a general-purpose NodePool, a memory-optimized NodePool, a GPU NodePool. Each has cloud-specific NodeClass (subnets, AMI, IAM role). <strong>Phase 3 — Migrate workload-by-workload.</strong> Add a node selector or affinity matching Karpenter NodePool labels. Verify Karpenter creates new nodes; verify Pod fits. Drain matching ASG nodes. <strong>Phase 4 — Decommission ASGs.</strong> When all workloads migrated, scale ASGs to 0; eventually delete. <strong>Phase 5 — Decommission CA.</strong> <code>helm uninstall cluster-autoscaler</code>. <strong>Pitfalls:</strong> (1) Operational tooling that SSH-d into named nodes (e.g., debug scripts referencing <code>ip-10-1-2-3.compute.internal</code>) breaks — Karpenter\'s nodes are ephemeral, names change. (2) PodDisruptionBudgets must be tight; Karpenter consolidates aggressively. (3) Spot eviction handling — Karpenter respects <code>do-not-disrupt</code> annotations but stateful workloads need careful PDBs. <strong>Total time:</strong> 2-4 weeks. <strong>Payoff:</strong> 30%+ cost savings on a typical cluster, faster scaling, simpler operational model."),
    ],
    glossary=[
        GlossaryItem(name="HorizontalPodAutoscaler (HPA)", definition="Adjusts replica count based on metrics. autoscaling/v2 supports multiple metrics + behaviour fields."),
        GlossaryItem(name="VerticalPodAutoscaler (VPA)", definition="Adjusts per-Pod resource requests based on observed usage. Three modes: Off, Initial, Auto."),
        GlossaryItem(name="KEDA", definition="Kubernetes Event-Driven Autoscaling. 60+ scalers; scale-to-zero supported."),
        GlossaryItem(name="ScaledObject", definition="KEDA CRD wrapping a Deployment with event-driven scaling rules."),
        GlossaryItem(name="Cluster Autoscaler (CA)", definition="Original cluster-level autoscaler. ASG-based. Predictable; slower than Karpenter."),
        GlossaryItem(name="Karpenter", definition="Modern cluster autoscaler. Picks instance type per Pending Pod. Fast (20-40s), cost-aware, consolidates."),
        GlossaryItem(name="NodePool / NodeClass (Karpenter)", definition="Karpenter CRDs. NodePool = scaling parameters. NodeClass = cloud-specific (subnet, AMI)."),
        GlossaryItem(name="Consolidation (Karpenter)", definition="Periodic check: can existing nodes be replaced with fewer/cheaper ones? Drains + recreates if yes."),
        GlossaryItem(name="metrics-server", definition="Required component for HPA. Aggregates Pod CPU/memory metrics from kubelets."),
        GlossaryItem(name="Prometheus Adapter / external-metrics", definition="Bridges custom Prometheus metrics into the K8s metrics API for HPA."),
        GlossaryItem(name="PodDisruptionBudget (PDB)", definition="Limit on simultaneous voluntary disruptions. Critical for spot + Karpenter scenarios. Lesson 35."),
        GlossaryItem(name="Stabilization window", definition="HPA setting: ignore scale-down decisions for N seconds. Reduces flapping."),
    ],
    recap_lead="Workload scaling (HPA/VPA/KEDA) + cluster scaling (Karpenter or CA) match capacity to demand end-to-end. HPA needs requests; KEDA scales by event signals; VPA right-sizes; Karpenter picks instance types per Pod and consolidates aggressively.",
    recap_next="<strong>Next — Lesson 35: Reliability & HA.</strong> The flip side of autoscaling — staying up under failures. PodDisruptionBudgets, multi-zone topology, regional disaster recovery, the chaos engineering loop.",
)
