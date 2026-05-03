"""K-GKE G6 — GKE Scaling and Cost (CA, NAP, Autopilot billing, Compute Classes, Spot, GPU/TPU, BQ export)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GKE scaling and cost — CA, NAP, Autopilot billing, Compute Classes, Spot, GPU, TPU, BQ export.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Auto-Greenhouse — capacity that flexes + cost that aligns</text>
  <rect x="40" y="70" width="170" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="125" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">node-side</text>
  <text x="125" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">Cluster Autoscaler (per pool)</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">Node Auto-Provisioning</text>
  <text x="125" y="131" text-anchor="middle" font-size="9" fill="#FBF1D6">Autopilot — per-Pod billing</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">Compute Classes</text>
  <rect x="225" y="70" width="170" height="120" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="310" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Pod-side</text>
  <text x="310" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">HPA + custom metrics adapter</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">VPA (right-sizing)</text>
  <text x="310" y="135" text-anchor="middle" font-size="9" fill="#FFFFFF">Autopilot mutates requests</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">based on observation</text>
  <rect x="410" y="70" width="170" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="495" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">specialty hardware</text>
  <text x="495" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Spot VMs (up to 91% off)</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">GPU — A3/A4 (H100/H200/B200)</text>
  <text x="495" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">TPU — Trillium / Ironwood</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">PDB-aware drains + multi-zone</text>
  <rect x="595" y="70" width="125" height="120" rx="10" fill="#E8B547" stroke="#3F4A5E"/>
  <text x="657" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#5A4F45">cost</text>
  <text x="657" y="105" text-anchor="middle" font-size="9" fill="#5A4F45">BigQuery cost export</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#5A4F45">per-namespace allocation</text>
  <text x="657" y="135" text-anchor="middle" font-size="9" fill="#5A4F45">Autopilot per-Pod-second</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#5A4F45">Compute Classes pricing</text>
  <text x="657" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#5A4F45">cost = chargeback foundation</text>
</svg>"""


LESSON = LessonSpec(
    num="06",
    title_short="scaling &amp; cost",
    title_full="G6 · GKE Scaling and Cost",
    title_html="K-GKE G6 · Scaling and Cost",
    module_eyebrow="Module G6 · the Auto-Greenhouse",
    hero_sub_html='<strong>Node-side</strong>: Cluster Autoscaler (per node pool, Standard); <strong>Node Auto-Provisioning (NAP)</strong> picks node SKUs across the catalog; <strong>Autopilot</strong> = no node management + per-Pod billing; <strong>Compute Classes</strong> (Balanced / Performance / Scale-Out / Accelerator) influence node selection. <strong>Pod-side</strong>: HPA + GCP custom metrics adapter; VPA. <strong>Specialty hardware</strong>: Spot (up to 91% off, fault-tolerant); GPU (A3/A4 with H100/H200/B200); TPU (Trillium / Ironwood). <strong>Cost</strong>: BigQuery billing export for per-namespace + per-tenant chargeback.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s month-end. The CFO opens the GCP bill. <em>\"Why is GKE 3× last month?\"</em> You investigate: a developer enabled HPA on a misconfigured Deployment with no maxReplicas; KEDA scaled it to 5,000 Pods overnight; Cluster Autoscaler obediently added 200 nodes. The workload was idle most of that time. <em>BigQuery cost export wasn\'t enabled, so nobody saw it.</em> Today\'s lesson: GKE\'s scaling primitives + how to align cost to actual usage with BQ export.",
    stamp_html="<strong>Cluster Autoscaler for fixed shapes; NAP picks SKUs across the catalog; Autopilot bills per Pod-second so idle = $0. Compute Classes drive SKU policy; Spot for fault-tolerant; GPU/TPU for AI. Always enable BQ billing export for chargeback.</strong>",
    district_pin="kg-plot06",
    district_label="Auto-Greenhouse",
    sections=[
        Section(
            eyebrow="Section 1.1 · Cluster Autoscaler + NAP",
            h2="Cluster Autoscaler + Node Auto-Provisioning",
            body_html="""    <p><strong>Cluster Autoscaler (CA)</strong> = per-node-pool min/max scaling on GKE Standard. Set <code>--enable-autoscaling --min-nodes M --max-nodes N</code> per pool. CA watches for unschedulable Pods and scales out (up to max); watches underutilised nodes and scales in (down to min, respecting PDBs).</p>
    <ul>
      <li><strong>PDB-aware drains</strong> — when scaling in, CA respects PodDisruptionBudgets. Tight PDBs deadlock scale-down.</li>
      <li><strong>Multi-zone CA</strong> — for multi-zonal pools, CA balances nodes across zones.</li>
    </ul>
    <p><strong>Node Auto-Provisioning (NAP)</strong> = GKE\'s implementation of automatic node-pool creation. Enable with <code>--enable-autoprovisioning</code> + bounds (CPU / memory / GPU / TPU). When unschedulable Pods need a SKU you don\'t have, NAP creates a new node pool with the right shape on demand. <em>Removes the per-pool sizing problem</em> — no need to pre-create dozens of pools for every possible workload shape.</p>
    <p><strong>Autopilot</strong> (covered in G1) is the no-CA-needed shape: Google manages all node operations; you declare Pods; per-Pod billing. The Pod-level SLA + admission constraints are part of the package.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Compute Classes + HPA + VPA",
            h2="Compute Classes + HPA + VPA",
            body_html="""    <p><strong>Compute Classes</strong> = a GKE primitive that lets you express <em>node-shape intent</em> via a <code>ComputeClass</code> CRD: priority list of acceptable VM families, optional Spot fallback, optional CMEK key, etc. NAP uses the Compute Class to pick SKUs; Autopilot uses it to pick the underlying compute. Built-in Compute Classes:</p>
    <ul>
      <li><strong>Balanced</strong> — general-purpose (E2 / N2). Default.</li>
      <li><strong>Performance</strong> — N2D / C3 / C4 high-frequency CPUs.</li>
      <li><strong>Scale-Out</strong> — Tau T2D / T2A — high-density, lower per-vCPU cost; ARM (T2A).</li>
      <li><strong>Accelerator</strong> — GPU / TPU shapes for AI workloads.</li>
    </ul>
    <p><strong>HPA (Horizontal Pod Autoscaler)</strong> + <strong>GCP custom metrics adapter</strong> = scale Pods on Cloud Monitoring custom metrics, not just CPU/memory. Examples: queue depth in Pub/Sub, request rate from Cloud Load Balancing, BigQuery query backlog. <em>Set maxReplicas</em> — HPA without a cap is the runaway-cost story.</p>
    <p><strong>VPA (Vertical Pod Autoscaler)</strong> right-sizes requests over time. <strong>In Autopilot</strong>, VPA-style mutation is built in — Autopilot observes actual usage and (for some workloads) adjusts Pod requests automatically. <em>Fewer over-provisioned Pods; lower bills.</em></p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Spot + GPU + TPU",
            h2="Spot + GPU (A3/A4) + TPU (Trillium / Ironwood)",
            body_html="""    <p><strong>Spot VMs</strong> on GKE — up to 91% off list price. Eviction with 30-second notice. Auto-tainted; workloads must tolerate. Ideal: batch jobs, ML training (with checkpointing), CI runners, fault-tolerant queue consumers. <em>Combine with Spot fallback in Compute Class</em> so your workload tries Spot first, falls back to on-demand if Spot is unavailable.</p>
    <p><strong>GPU node pools</strong>:
    <ul>
      <li><strong>A3</strong> — NVIDIA H100 (Hopper) GPUs. Up to 8 GPUs per VM. For LLM training + high-end inference.</li>
      <li><strong>A4</strong> — NVIDIA H200 / B200 (newer Hopper / Blackwell). Higher memory bandwidth + capacity.</li>
      <li>L4 / L40S / T4 for inference + smaller training.</li>
    </ul>
    NVIDIA GPU Operator or GKE\'s built-in NVIDIA GPU device plugin makes <code>nvidia.com/gpu</code> resource available. MIG (Multi-Instance GPU) lets you slice a single H100 into multiple smaller GPUs for inference workloads.</p>
    <p><strong>TPU</strong> — Google\'s custom AI accelerator chips:
    <ul>
      <li><strong>Trillium</strong> — current-gen training/inference TPU. Multi-host pods (TPU v5e+) for distributed training.</li>
      <li><strong>Ironwood</strong> — newest gen, optimised for inference at scale.</li>
    </ul>
    Multi-host TPU pods require special node-pool topology + workload integration (the JobSet API + Kueue help — covered in G8).</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · cost — BigQuery export + Autopilot per-Pod billing",
            h2="Cost — BigQuery export + Autopilot per-Pod billing",
            body_html="""    <p><strong>GKE cost allocation with BigQuery export</strong> — enable <strong>BigQuery billing export</strong> at the project level + the GKE-specific <strong>cost allocation</strong> feature. Result: per-row cost data joined with K8s metadata (cluster, namespace, workload). Build chargeback dashboards in Looker Studio / Looker / Grafana. <em>Without this, you can see cluster total but not which team / tenant owns the slice.</em></p>
    <p><strong>Autopilot per-Pod billing</strong>:
    <ul>
      <li>Bills per <em>Pod-second based on requested CPU / memory / ephemeral storage</em>.</li>
      <li>Pod with <code>requests: 100m / 256Mi</code> running 1 hour ≈ 0.1 vCPU-hour + 0.25 GiB-hour. Off-hours scale-to-zero of a Deployment = $0.</li>
      <li>GPU / TPU billed per accelerator-second when using Compute Class Accelerator.</li>
      <li>Compare to Standard which always bills per node — over-provisioned pools idle most of the day.</li>
    </ul>
    <p><strong>Cost levers:</strong> right-size requests (VPA recommendations or Autopilot auto-mutation); use Spot for fault-tolerant workloads; use Compute Class Scale-Out (T2D / ARM) for compute-bound stateless workloads at ~30% saving; cap HPA maxReplicas; review BQ cost export monthly to catch outliers.</p>
    <p><strong>Sustained-use + committed-use discounts</strong> (CUDs) — apply to GKE node-VM cost. Negotiate CUDs for the predictable baseline; let burst go through Spot + on-demand.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team\'s Standard cluster is paying for 200 nodes that are mostly idle off-hours. Which fix unlocks the off-hours saving?",
            options=[
                ("Increase Cluster Autoscaler scale-down delay.", False),
                ("Switch to Autopilot (per-Pod billing — idle Pods scale to zero) or scale Deployments to zero off-hours via KEDA + use Spot for the rest.", True),
                ("Buy more committed-use discounts.", False),
            ],
            feedback="Standard always bills per node; idle nodes still cost. Autopilot bills per Pod-second; idle = $0. KEDA + scale-to-zero gets you closer to that on Standard.",
        ),
    },
    before_after_before='<p>Pre-Autopilot, every GKE cluster billed per node — over-provisioned pools idle most of the day. Pre-NAP, operators created dozens of node pools per cluster (one per workload shape). Pre-Compute Classes, picking the right SKU per workload was a Helm-values exercise. GPU + TPU were Standard-only. BigQuery cost export was bring-your-own; per-namespace cost was opaque.</p>',
    before_after_after='<p>Modern GKE: <strong>Autopilot per-Pod billing</strong> aligns spend to actual Pod-seconds. <strong>NAP</strong> creates node pools on demand from the SKU catalog. <strong>Compute Classes</strong> express SKU intent declaratively. <strong>Spot fallback</strong> in Compute Class. <strong>BigQuery billing export</strong> + GKE cost allocation surfaces per-namespace + per-tenant cost. Plus first-class GPU (A3/A4) + TPU (Trillium/Ironwood) for AI. <em>Spend visibility + flexibility together.</em></p>',
    before_after_caption='<p class="ba-caption"><em>The era of cluster bill surprises is over for teams that wire BQ export + use Autopilot or NAP + Compute Classes thoughtfully.</em></p>',
    analogy_intro_html='''<p>The <strong>Auto-Greenhouse</strong> is K-Garden\'s climate-controlled space where capacity flexes with demand. Three staff handle different jobs.</p>
    <p>The <strong>Plot Manager</strong> (Cluster Autoscaler) walks rows in their assigned greenhouse: \"this row is full → wheel in 5 more pots from the supply room; this row is empty → roll the empty pots back.\" The Plot Manager only handles one greenhouse type (one node pool); for new shapes, the Garden Architect (Node Auto-Provisioning) builds a new greenhouse on demand from the catalog.</p>
    <p>The <strong>Robot Caretaker</strong> (Autopilot) runs a different model entirely: visitors arrive with seedlings; the robot plants, waters, prunes; visitors are billed per seedling-day (per-Pod-second), not per greenhouse. Idle = $0.</p>
    <p>The <strong>Greenhouse Catalog</strong> (Compute Classes) describes which greenhouse models the Architect picks — <em>Balanced</em> general-purpose, <em>Performance</em> high-frequency, <em>Scale-Out</em> ARM/Tau low-cost, <em>Accelerator</em> for GPU/TPU AI plots.</p>
    <p>Plus <em>specialty plots</em>: Spot greenhouses (deep-discount, ushers can ask occupants to leave with 30s notice — for resilient batch crops); GPU plots (A3/A4 with H100/H200/B200 NVIDIA accelerators for AI training); TPU plots (Trillium / Ironwood Google-designed AI accelerators for distributed training).</p>
    <p>And the <strong>Garden Accountant</strong> (BigQuery cost export + GKE cost allocation) breaks the bill down per plot, per tenant, per crop — so the head gardener knows who owes what.</p>''',
    translation_rows=[
        ("Plot Manager (per greenhouse)", "Cluster Autoscaler — per-pool min/max"),
        ("Garden Architect (catalog-driven)", "Node Auto-Provisioning (NAP)"),
        ("Robot Caretaker", "GKE Autopilot — managed nodes + per-Pod billing"),
        ("Greenhouse Catalog", "Compute Classes (Balanced / Performance / Scale-Out / Accelerator)"),
        ("Per-seedling-day billing", "Autopilot per-Pod-second billing"),
        ("Spot greenhouses (30s notice)", "Spot VMs (up to 91% off)"),
        ("Spot fallback in catalog", "Compute Class with Spot fallback"),
        ("GPU plots", "A3 (H100), A4 (H200/B200) GPU node pools"),
        ("TPU plots", "Trillium / Ironwood TPU node pools"),
        ("Slice a greenhouse into smaller plots", "MIG — Multi-Instance GPU"),
        ("HPA via custom metric (queue depth)", "HPA with GCP custom metrics adapter (Cloud Monitoring source)"),
        ("Right-size each pot to what\'s in it", "VPA / Autopilot auto-mutation of requests"),
        ("Garden Accountant", "BigQuery billing export + GKE cost allocation"),
        ("\"Per-tenant chargeback\"", "Per-namespace cost via BQ joined with K8s metadata"),
        ("Pre-paid plot lease", "Committed-use discount (CUD) on baseline"),
    ],
    analogy_stops="A real greenhouse has fixed walls; Compute Classes + NAP are software-defined and reshape constantly. Real Autopilot has admission constraints (mutates / rejects some Pod specs) the metaphor doesn\'t capture.",
    eli5="The greenhouse has clever staff. One adds and removes pots in their greenhouse. One builds new greenhouses from a catalog when needed. A robot caretaker runs the whole job for some plots and bills per seedling. Special greenhouses for cheap (Spot), GPU, and TPU. An accountant breaks the bill down per plot.",
    eli10="GKE scaling = node-side (CA per pool, NAP across catalog, Autopilot fully managed) + Pod-side (HPA with custom metrics, VPA / Autopilot auto-mutation). Compute Classes (Balanced / Performance / Scale-Out / Accelerator) drive SKU intent. Specialty hardware: Spot (91% off), GPU (A3 H100, A4 H200/B200), TPU (Trillium / Ironwood). Cost: BigQuery billing export + GKE cost allocation = per-namespace + per-tenant chargeback. Autopilot per-Pod billing = idle = $0.",
    scenarios=[
        Scenario(
            name="SaaS — Autopilot + scale-to-zero off-hours",
            body="A SaaS\'s API workloads on Autopilot. KEDA on Pub/Sub queue depth scales to 0 replicas off-hours. Per-Pod billing = $0 cost during 8 hours of low traffic. Compared to Standard with 5-node baseline pool: ~30% lower monthly bill on the same traffic shape.",
        ),
        Scenario(
            name="ML team — Spot A3 H100 for training, on-demand A4 H200 for inference",
            body="ML team uses Compute Class Accelerator: Spot fallback enabled. Training jobs prefer Spot A3 H100 (massive discount + checkpointing tolerates eviction); when Spot unavailable, fall back to on-demand. Inference workloads on dedicated A4 H200 pool, no Spot (latency-sensitive). <em>Training cost ~70% lower vs all-on-demand; inference SLA preserved.</em>",
        ),
        Scenario(
            name="Multi-tenant cluster — per-namespace chargeback rolled out via BQ export",
            body="Platform team enables BigQuery billing export + GKE cost allocation. Looker Studio dashboard joins billing rows with namespace → tenant mapping. Tenants now see their actual cost; Finance has chargeback. <em>Outcome: one tenant noticed their over-provisioned Deployment, removed it, saved $4K/month.</em>",
        ),
        Scenario(
            name="Compute Class Scale-Out (T2D ARM) saved 30% on stateless backend",
            body="A stateless backend ran on default Balanced (E2). Migration to Compute Class Scale-Out (Tau T2D ARM) for the workload\'s ARM-built containers. ~30% lower per-vCPU cost; throughput equivalent. <em>One Compute Class change; significant saving on the cluster\'s biggest line item.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Autopilot is always cheaper than Standard.\"",
            truth="Autopilot bills per requested CPU/memory at a markup over raw VM rates. For workloads at <strong>high sustained utilisation on big nodes with big requests</strong>, Standard with packed nodes can be cheaper. Autopilot wins on bursty / event-driven workloads with idle hours and on small clusters where Standard\'s minimum-viable node pool is over-provisioned. Run the math per workload pattern; both paths are valid.",
        ),
        Misconception(
            myth="\"Spot saves money. Period.\"",
            truth="Spot saves only when the workload <em>tolerates</em> eviction — checkpoint-resume training, idempotent retries, queue-driven consumers. If the workload restarts losing work or fails customer-facing requests during eviction, the SLA hit + retry cost outweighs the Spot saving. Use Compute Class with Spot fallback to get the saving when Spot is available without breaking when it isn\'t.",
        ),
        Misconception(
            myth="\"GPU is GPU. Pick whichever is available.\"",
            truth="A3 (H100), A4 (H200/B200), L4, L40S, T4 are all NVIDIA GPUs but very different price/perf classes. H100/H200 for LLM training + high-end inference. L4/L40S for cost-effective inference. T4 for legacy or budget inference. <em>Pick by workload</em>: LLM training on T4 = wasteful; small-model inference on H100 = wasteful. Compute Class Accelerator + workload selectors target the right pool.",
        ),
    ],
    flashcards=[
        Flashcard(front="Cluster Autoscaler vs NAP vs Autopilot — when to use each?", back="<strong>CA</strong>: per-pool min/max scaling on Standard; predictable, you pick SKU. <strong>NAP</strong>: GKE creates node pools on demand from SKU catalog. <strong>Autopilot</strong>: Google manages all node operations; per-Pod billing; admission webhooks. Standard+CA for predictable shapes; Standard+NAP for mixed shapes; Autopilot for managed defaults + idle savings."),
        Flashcard(front="Four built-in Compute Classes?", back="<strong>Balanced</strong> (E2 / N2 default), <strong>Performance</strong> (N2D / C3 / C4 high-freq), <strong>Scale-Out</strong> (Tau T2D / T2A ARM, low per-vCPU cost), <strong>Accelerator</strong> (GPU / TPU). Custom Compute Class CRD lets you express priority lists + Spot fallback + CMEK."),
        Flashcard(front="What is HPA + GCP custom metrics adapter?", back="HPA scaling on Cloud Monitoring custom metrics — not just CPU/memory. Sources: Pub/Sub queue depth, Cloud LB request rate, BigQuery backlog. Always set maxReplicas — HPA without a cap = runaway cost."),
        Flashcard(front="Why is Spot fallback in Compute Class powerful?", back="Workload tries Spot first (huge discount); if Spot unavailable in the region, falls back to on-demand. You get the saving when Spot is available without your workload breaking when it isn\'t. Configure in the Compute Class spec."),
        Flashcard(front="GPU SKU classes — pick by use case?", back="<strong>A3</strong> = H100 Hopper (LLM training + high-end inference). <strong>A4</strong> = H200 / B200 (newer Hopper / Blackwell — higher memory bandwidth + capacity). <strong>L4 / L40S</strong> = cost-effective inference. <strong>T4</strong> = budget / legacy inference."),
        Flashcard(front="What\'s a TPU and what\'s the current-gen?", back="<strong>TPU</strong> = Google\'s custom AI accelerator chips (Tensor Processing Units). Current-gen training: <strong>Trillium</strong>. Inference at scale: <strong>Ironwood</strong>. Multi-host pods (TPU v5e+) require special node-pool topology — JobSet API + Kueue help schedule them."),
        Flashcard(front="What is GKE cost allocation + BigQuery export?", back="Project-level <strong>BigQuery billing export</strong> + GKE-specific <strong>cost allocation</strong> feature → per-row cost data joined with K8s metadata (cluster, namespace, workload). Foundation for chargeback dashboards in Looker Studio / Grafana."),
        Flashcard(front="How does Autopilot per-Pod billing work?", back="Bills per <em>Pod-second</em> based on requested CPU/memory/ephemeral storage. Pod with 100m/256Mi for 1 hour ≈ 0.1 vCPU-hour + 0.25 GiB-hour. Off-hours scale-to-zero = $0. GPU/TPU billed per accelerator-second when using Compute Class Accelerator."),
    ],
    quizzes=[
        Quiz(
            prompt="A developer enables HPA on a Deployment with no <code>maxReplicas</code>. Custom metrics adapter sees a queue spike; HPA tries to scale to thousands of Pods. What happens, and what\'s the right config?",
            answer="HPA scales toward the computed target (potentially massive). Cluster Autoscaler / NAP adds nodes to schedule them. Cluster cost spikes; subnet may IP-exhaust. <strong>Right config:</strong> always set <code>spec.maxReplicas</code> on every HPA — pick a defensible cap. Plus alert on Pod count > X, plus quotas on namespace resources. <em>HPA without a cap is the runaway-cost story; cap it.</em>",
        ),
        Quiz(
            prompt="The platform team wants \"per-namespace cost visibility for chargeback.\" Walk through the wire-up.",
            answer="(1) Enable <strong>BigQuery billing export</strong> at the billing-account level — exports daily billing data to a BQ dataset. (2) Enable <strong>GKE cost allocation</strong> on the cluster — adds K8s metadata (namespace, workload) to the per-row cost data. (3) Build a Looker Studio (or Grafana / Looker) dashboard joining cost rows with namespace → tenant mapping (your tenancy CMDB or labels). (4) Optionally schedule a monthly export to email tenants their bill. <em>Total wire-up: ~half a day; recurring value: chargeback discipline.</em>",
        ),
        Quiz(
            prompt="The CFO sees the GKE bill and asks: \"Are we using Spot for everything we can?\" Defend or correct.",
            answer="\"<strong>No — and we shouldn\'t be.</strong> Spot saves up to 91% but evictions happen with 30 seconds notice. We use Spot for: (1) batch / training jobs with checkpointing — eviction = lose &lt; 10 min work, cheaper than on-demand. (2) Stateless replicas behind a load balancer with multi-zone anti-affinity — losing one Pod is invisible. (3) CI runners — jobs are idempotent. We do <em>not</em> use Spot for: stateful primaries (eviction = data loss), latency-sensitive customer-facing endpoints (eviction = visible 5xx during reschedule), workloads with no checkpoint protocol. We use Compute Class with Spot <em>fallback</em> on eligible workloads — get the discount when Spot is available, fall back cleanly when it\'s not. Pushing more workloads onto Spot than this would generate SLA breaches that cost more than the saving.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CFO",
        ),
    ],
    glossary=[
        GlossaryItem(name="Cluster Autoscaler (CA)", definition="GKE Standard node-pool min/max scaling. Adds/removes Compute Engine instances to satisfy Pending Pods."),
        GlossaryItem(name="Node Auto-Provisioning (NAP)", definition="Creates node pools on demand from the SKU catalog. Removes per-pool sizing problem."),
        GlossaryItem(name="Compute Class", definition="GKE primitive expressing node-shape intent: priority SKU list + optional Spot fallback + CMEK. Built-in: Balanced / Performance / Scale-Out / Accelerator."),
        GlossaryItem(name="Spot VM", definition="Up to 91% off list price; 30-second eviction warning. Auto-tainted; workloads must tolerate."),
        GlossaryItem(name="A3 / A4 GPU pool", definition="A3 = NVIDIA H100 Hopper. A4 = H200 / B200 (newer Hopper / Blackwell). For LLM training + high-end inference."),
        GlossaryItem(name="MIG (Multi-Instance GPU)", definition="Slice a single H100 into multiple smaller virtual GPUs for inference workloads."),
        GlossaryItem(name="TPU", definition="Google\'s custom AI accelerator. Trillium = current-gen training. Ironwood = inference-optimised next-gen."),
        GlossaryItem(name="HPA + GCP custom metrics adapter", definition="HPA scaling on Cloud Monitoring custom metrics — Pub/Sub queue, LB rate, BQ backlog, etc."),
        GlossaryItem(name="VPA", definition="Vertical Pod Autoscaler — right-sizes Pod requests over time. In Autopilot, a VPA-style mutation is built in."),
        GlossaryItem(name="Autopilot per-Pod billing", definition="Bills per Pod-second based on requested CPU / memory / ephemeral. Idle = $0."),
        GlossaryItem(name="BigQuery billing export", definition="Daily billing rows exported to BQ. Joined with GKE cost allocation metadata for per-namespace chargeback."),
        GlossaryItem(name="GKE cost allocation", definition="Cluster-level feature that adds K8s metadata (namespace, workload) to BQ-exported billing rows."),
    ],
    recap_lead='Two scaling axes (node-side: CA / NAP / Autopilot; Pod-side: HPA / VPA) + Compute Classes for SKU intent + specialty hardware (Spot / GPU / TPU). Cost surfaced via BQ export.',
    recap_next='<strong>Next — G7: GKE Observability.</strong> Cloud Logging + Cloud Monitoring (auto for GKE), Managed Service for Prometheus (GMP), managed Grafana, Cloud Trace, Cloud Profiler, Error Reporting, control-plane metrics/logs, SLO monitoring, alerting policies, BigQuery cost view.',
)
