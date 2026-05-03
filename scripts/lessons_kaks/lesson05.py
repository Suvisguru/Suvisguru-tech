"""K-AKS A5 — AKS Scaling (Cluster Autoscaler, NAP/Karpenter, KEDA, Spot, GPU, ARM, Confidential)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AKS scaling — Cluster Autoscaler, Node Auto Provisioning, KEDA, specialty pools.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Auditorium — flexing capacity</text>
  <rect x="50" y="60" width="160" height="130" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="130" y="80" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">node-side</text>
  <text x="130" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6">Cluster Autoscaler</text>
  <text x="130" y="113" text-anchor="middle" font-size="8" font-style="italic" fill="#FBF1D6">(per-pool min/max)</text>
  <text x="130" y="132" text-anchor="middle" font-size="9" fill="#FBF1D6">Node Auto Provisioning</text>
  <text x="130" y="145" text-anchor="middle" font-size="8" font-style="italic" fill="#FBF1D6">(Karpenter for AKS)</text>
  <text x="130" y="170" text-anchor="middle" font-size="9" fill="#FBF1D6">PDB-aware drains</text>
  <rect x="225" y="60" width="160" height="130" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="305" y="80" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">Pod-side</text>
  <text x="305" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">HPA · CPU/mem/custom</text>
  <text x="305" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">VPA · right-sizing</text>
  <text x="305" y="135" text-anchor="middle" font-size="9" fill="#FFFFFF">KEDA · event-driven</text>
  <text x="305" y="150" text-anchor="middle" font-size="8" font-style="italic" fill="#FFFFFF">Service Bus, queue, cron…</text>
  <rect x="400" y="60" width="310" height="130" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="555" y="80" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">specialty node pools</text>
  <text x="555" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Spot — up to 90% off · 30s eviction</text>
  <text x="555" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">GPU — NC/ND · NVIDIA driver preinstalled</text>
  <text x="555" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">Windows — Server 2022 for .NET Framework</text>
  <text x="555" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">ARM — Cobalt, Ampere Altra (~25% cheaper)</text>
  <text x="555" y="160" text-anchor="middle" font-size="9" fill="#FFFFFF">Confidential — DCasv5/ECasv5 AMD SEV-SNP</text>
</svg>"""


LESSON = LessonSpec(
    num="05",
    title_short="AKS scaling",
    title_full="A5 · AKS Scaling (Cluster Autoscaler, NAP, KEDA, Spot, GPU, ARM, Confidential)",
    title_html="K-AKS A5 · AKS Scaling",
    module_eyebrow="Module A5 · the Auditorium — capacity that flexes",
    hero_sub_html='Two scaling axes. <strong>Node-side</strong>: Cluster Autoscaler (per-pool min/max — primary), <strong>Node Auto Provisioning (NAP)</strong> = AKS\'s Karpenter (default in AKS Automatic). <strong>Pod-side</strong>: HPA, VPA, <strong>KEDA add-on</strong> (event-driven — Service Bus, queues, cron, custom). Specialty pools: <strong>Spot</strong> (up to 90% off, 30s eviction), <strong>GPU</strong> (NC/ND), <strong>Windows Server 2022</strong>, <strong>ARM</strong> (Cobalt, Ampere Altra ~25% cheaper), <strong>Confidential</strong> (DCasv5/ECasv5 with AMD SEV-SNP).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"100 Pods stuck Pending — InsufficientCpu.\"</em> Cluster Autoscaler logs: <code>scale-up: 0 nodes added</code>. You realise the User node pool is at <code>maxCount: 5</code> and is already at 5. Plus the Spot pool is empty because the SKU you picked is unavailable in this region right now. Plus a third autoscaler (KEDA) is trying to scale the Deployment that\'s blocked. <em>Three autoscalers, no plan.</em> Today\'s lesson: how the four scaling planes interact and where each one belongs.",
    stamp_html="<strong>Cluster Autoscaler is per-pool min/max for fixed shapes; NAP (AKS Karpenter) provisions any shape on demand. KEDA scales Pods on events. Use Spot + ARM for cost; GPU/Confidential for special workloads. PDBs guard maintenance drains.</strong>",
    district_pin="kc-wing05",
    district_label="The Auditorium",
    sections=[
        Section(
            eyebrow="Section 1.1 · Cluster Autoscaler",
            h2="Cluster Autoscaler — the per-pool primary",
            body_html="""    <p><strong>Cluster Autoscaler (CA)</strong> is the default node-side autoscaler in AKS Standard. Per node pool: set <code>--min-count</code> and <code>--max-count</code>. CA watches for unschedulable Pods and scales the pool out (up to max); watches underutilised nodes and scales in (down to min, respecting PDBs).</p>
    <ul>
      <li><strong>Mental model:</strong> CA reasons about <em>VMSS scale operations</em>, not individual nodes. Scale operations have minute-scale latency.</li>
      <li><strong>Per-pool tuning:</strong> <code>scale-down-delay-after-add</code>, <code>scale-down-unneeded-time</code>, <code>scan-interval</code>, <code>balance-similar-node-groups</code>.</li>
      <li><strong>Limits:</strong> CA can only scale within an existing pool\'s VM SKU. Mixing instance shapes = many pools = operational overhead. CA also can\'t pick spot vs on-demand dynamically — that\'s a different pool.</li>
      <li><strong>PDB-aware drains:</strong> when scaling in or upgrading, CA drains nodes respecting PodDisruptionBudgets. A workload with <code>maxUnavailable: 0</code> + min replicas = blocking. Set PDBs that don\'t deadlock scale-down.</li>
    </ul>"""
        ),
        Section(
            eyebrow="Section 1.2 · Node Auto Provisioning (Karpenter for AKS)",
            h2="Node Auto Provisioning — Karpenter for AKS",
            body_html="""    <p><strong>Node Auto Provisioning (NAP)</strong> is AKS\'s implementation of the Karpenter autoscaler — the same primitives EKS users know. <em>Default in AKS Automatic.</em> Available in preview for AKS Standard.</p>
    <ul>
      <li><strong>How it differs from CA:</strong> instead of per-pool min/max, NAP looks at the whole pool of Pending Pods and computes a near-cost-optimal node mix on the fly. Pick from a wide SKU catalog (D-series, B-series, ARM, spot mixes), not a fixed pool.</li>
      <li><strong>NodePool + NodeClass</strong> (K8s CRDs) — declare the workload\'s requirements (instance family, max-CPU, OS, zones) and Azure picks the cheapest fitting SKU. Aged-node lifecycle: NAP replaces nodes after a <code>expireAfter</code> ttl (default 21 days) — no patch debt.</li>
      <li><strong>Consolidation:</strong> NAP periodically re-bins Pods onto fewer nodes when utilisation drops, then terminates the empty nodes. <em>Idle-spend reduction without manual intervention.</em></li>
      <li><strong>When to pick NAP over CA:</strong> mixed workloads where node-shape diversity matters; cost optimisation across spot/on-demand/ARM; teams that want fewer pools to manage.</li>
    </ul>"""
        ),
        Section(
            eyebrow="Section 1.3 · KEDA — event-driven Pod scaling",
            h2="KEDA — event-driven Pod scaling (managed add-on)",
            body_html="""    <p><strong>KEDA (Kubernetes Event-Driven Autoscaler)</strong> is a managed AKS add-on that scales Pods on external events, not just CPU/memory. <em>Default in AKS Automatic.</em></p>
    <ul>
      <li><strong>Scalers</strong> (60+): Azure Service Bus queue depth, Storage Queue depth, Event Hub backlog, Cosmos DB lease changes, Kafka lag, RabbitMQ, Cron schedules, Prometheus query, custom (your own metric).</li>
      <li><strong>ScaledObject</strong> CRD wraps a Deployment + scaler config. KEDA creates an HPA under the hood; injects external metrics into the K8s metrics API; HPA reacts.</li>
      <li><strong>Scale-to-zero:</strong> KEDA is the canonical way to scale to <em>zero replicas</em> when there\'s no event. CPU-based HPA can\'t do this (it needs at least 1 Pod to read CPU from). KEDA can — service bus has 0 messages → 0 replicas → 0 cost.</li>
      <li><strong>Combining with HPA:</strong> ScaledObject can also reference standard CPU/memory metrics; one Deployment can scale on \"queue depth OR CPU\".</li>
    </ul>
    <p><strong>VPA (Vertical Pod Autoscaler):</strong> right-sizes Pod requests over time based on observed usage. Useful for workloads with poorly-tuned CPU/memory requests. <em>Cannot use with HPA on the same metric</em>.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · Specialty node pools",
            h2="Specialty node pools — Spot, GPU, Windows, ARM, Confidential",
            body_html="""    <p>Beyond the standard System / User pools, AKS supports several specialty pools. Each is a separate node pool — combine pools per cluster.</p>
    <ul>
      <li><strong>Spot pool</strong> — Spot VMs, up to 90% off, evictable on 30 seconds notice. Auto-tainted <code>kubernetes.azure.com/scalesetpriority=spot:NoSchedule</code>; workloads must tolerate. Ideal: batch jobs, ML training, fault-tolerant queue workers.</li>
      <li><strong>GPU pool</strong> — NC-series (NVIDIA T4 / A100 / H100) or ND-series. AKS GPU image (<code>UbuntuGPU</code>) ships drivers preinstalled; alternative is the NVIDIA GPU Operator. Pods request <code>nvidia.com/gpu: 1</code>.</li>
      <li><strong>Windows pool</strong> — Windows Server 2022 nodes for .NET Framework workloads. Mixed Linux+Windows clusters are normal.</li>
      <li><strong>ARM pool</strong> — Azure Cobalt 100 / Ampere Altra (D-pls/D-pds-v5). ~25% cheaper than equivalent x86 D-series. Workloads must have ARM64 container images.</li>
      <li><strong>Confidential Computing pool</strong> — DCasv5 / ECasv5 SKUs with AMD SEV-SNP. Memory encryption with attestation; for workloads handling regulated PII / financial data needing in-use encryption.</li>
      <li><strong>FIPS pool</strong> — node OS configured for FIPS 140-2 cryptography. Required for some US federal compliance contexts.</li>
    </ul>
    <p><strong>Multi-zone scaling:</strong> at pool create, set zones. Pool autoscale spreads across zones. Combine with topology-spread constraints on Pods for tight zone placement.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A workload has bursty arrival but a wide range of Pod sizes. The team is paying too much because each existing pool is sized to the largest Pod in it. What\'s the fix?",
            options=[
                ("Add more pools.", False),
                ("Switch to <strong>Node Auto Provisioning (NAP)</strong> — Azure picks near-cost-optimal node SKUs per Pending Pod, then consolidates idle.", True),
                ("Increase HPA target CPU.", False),
            ],
            feedback="NAP solves the per-pool sizing problem by provisioning across the SKU catalog on demand and re-binning during consolidation.",
        ),
    },
    before_after_before='<p>Pre-Karpenter AKS scaling = <strong>Cluster Autoscaler per pool</strong>. Mixed-workload teams ended up with 8-15 node pools (one per workload shape) — operational nightmare. Spot-only meant declaring a separate Spot pool; mixing on-demand with spot in one workload required complex tolerations + nodeAffinity. KEDA add-on existed but was bring-your-own. ARM workloads required separate pool + image discipline. Confidential was preview-only.</p>',
    before_after_after='<p>Modern AKS (Automatic by default; NAP add-on for Standard) gives you <strong>Node Auto Provisioning</strong> — declare what your workloads need; Azure picks the optimal node SKUs from the entire catalog on demand, and consolidates during idle. KEDA is a managed add-on (no Helm). Spot, GPU, Windows, ARM, Confidential, FIPS pools are all first-class. Plus PDB-aware drains during planned maintenance windows protect availability. <em>Right-size happens automatically; you only declare workload intent.</em></p>',
    before_after_caption='<p class="ba-caption"><em>The era of pool-sprawl is over. NAP + KEDA + Spot + ARM gives small teams Google-tier elasticity without ops cost.</em></p>',
    analogy_intro_html='''<p>The <strong>Auditorium</strong> on K-Campus has chairs that flex with the crowd. Two staffs handle different jobs.</p>
    <p>The <strong>House Manager</strong> (Cluster Autoscaler) walks the rows: \"Section A is full → wheel in 5 more chairs from the loading dock; Section A is empty → wheel them back.\" Section A only has one type of chair (a node pool); if you need bigger chairs, the House Manager opens Section B. <em>Lots of sections; lots of management.</em></p>
    <p>The <strong>Concierge</strong> (Node Auto Provisioning / Karpenter for AKS) is a different staffer: \"15 people just arrived — let me look at the warehouse and pick the best chair-mix to seat them all cheaply.\" The Concierge picks tall chairs for tall people, kid chairs for kids, folding chairs for the budget-conscious — <em>no fixed sections required</em>. Later: \"Half the seats are empty — let me re-arrange so we use fewer rows and put the unused chairs back.\"</p>
    <p>The <strong>Door Counter</strong> (KEDA) sits at the entrance: \"50 people just queued at the side door (Service Bus) — Concierge, prepare for 50 more chairs.\" Or: \"The side door is empty — bring the chairs back to zero, no Pods running, no cost.\"</p>
    <p>The Auditorium also stocks <em>specialty chairs</em>: discounted folding seats (Spot — cheap, but ushers can ask people to leave with 30s notice), reinforced seats with built-in microscopes (GPU), Microsoft-branded swivel chairs (Windows), eco-friendly bamboo seats (ARM, ~25% cheaper), and lockboxes-with-chairs for sensitive guests (Confidential).</p>''',
    translation_rows=[
        ("House Manager (per-section)", "Cluster Autoscaler — per-pool min/max"),
        ("Concierge (whole-warehouse)", "Node Auto Provisioning (NAP) / Karpenter for AKS"),
        ("Door Counter (queue depth)", "KEDA — event-driven Pod scaling"),
        ("Right-size each chair to the guest", "VPA — Vertical Pod Autoscaler"),
        ("Discounted folding seats (30s notice)", "Spot node pool"),
        ("Reinforced seats with microscopes", "GPU pool (NC/ND-series)"),
        ("Microsoft-branded swivel chairs", "Windows Server 2022 pool"),
        ("Bamboo eco seats (~25% off)", "ARM pool (Cobalt, Ampere Altra)"),
        ("Lockbox-chairs for sensitive guests", "Confidential pool (DCasv5/ECasv5, AMD SEV-SNP)"),
        ("\"Don\'t move chair while someone\'s in it\"", "PodDisruptionBudget — protects drains"),
        ("\"Spread guests across rows\"", "topology-spread constraints / multi-zone"),
    ],
    analogy_stops="The Auditorium metaphor flattens latency — real-world node provisioning takes 1-3 minutes; consolidation cycles take longer. Pods can\'t literally \"move\" without restart unless you\'re using VPA-in-place (preview).",
    eli5="The auditorium has clever staff. One says \"this section is full — bring more chairs.\" Another says \"forget sections, let me look at everyone and pick the right chair mix.\" A third stands at the door and says \"50 more people are coming, prep extra chairs.\" Plus they have a few specialty chairs — discount, fancy, big.",
    eli10="AKS scaling = node-side + Pod-side + specialty pools. <strong>Node-side:</strong> Cluster Autoscaler (per-pool min/max, predictable, simple) or Node Auto Provisioning (Karpenter — picks optimal SKUs across the catalog, consolidates idle). <strong>Pod-side:</strong> HPA (CPU/mem), VPA (right-sizing), KEDA (60+ event scalers, scale-to-zero). <strong>Specialty:</strong> Spot (90% off, 30s eviction), GPU, Windows, ARM (Cobalt/Altra), Confidential (DCasv5 with SEV-SNP), FIPS. PDBs guard drains; multi-zone via pool zones + topology-spread constraints.",
    scenarios=[
        Scenario(
            name="Batch workloads on Spot — 70% cost reduction",
            body="A media company runs nightly video transcoding — fault-tolerant, retry-safe. They add a Spot pool autoscaling 0-50 nodes. Workloads tolerate the spot taint and use a checkpoint-resume pattern: if evicted, the next Pod resumes from where the prior left off. Steady-state cost: 70% lower than on-demand. <em>Eviction rate ~3% — well within their tolerance.</em>",
        ),
        Scenario(
            name="Order-processing — KEDA + Service Bus, scale-to-zero",
            body="An e-commerce backend processes order events from Azure Service Bus. Outside business hours, queue depth = 0 → KEDA scales the Deployment to 0 Pods. During peak: 5K messages/min → KEDA scales to 50 Pods (target = 100 messages/Pod). Outside peak (1 message in 30 minutes): wakes 1 Pod for 5 minutes. <em>Off-hours infra cost approaches zero.</em>",
        ),
        Scenario(
            name="ML training on GPU spot — A100 sweep at fraction of cost",
            body="An ML team runs hyperparameter sweeps on NC A100 nodes. Single GPU pool: spot, autoscale 0-20. Each training Pod tolerates the spot taint, requests <code>nvidia.com/gpu: 8</code>, checkpoints to Blob every 10 minutes. Eviction → resumes on next allocated node. <em>Effective rate: ~$2/A100/hr vs $4 on-demand; same throughput; 50% saving.</em>",
        ),
        Scenario(
            name="Multi-zone Postgres + PDB — survived AZ outage",
            body="A 3-replica Postgres StatefulSet, each Pod pinned to a different zone, PDB <code>maxUnavailable: 1</code>. AZ-1 went dark at 02:14. Two Pods still running; PDB blocked CA from draining either. KEDA + HPA didn\'t fire (DB Pods not in scaling). At 02:31 AZ-1 recovered; 3rd Pod re-scheduled. <em>Application latency rose by 2× during 17 minutes; no data loss; no human intervention.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"NAP and Cluster Autoscaler do the same thing.\"",
            truth="<strong>CA</strong> = per-pool min/max scaling. You define the pool\'s VM SKU; CA scales count. <strong>NAP</strong> = per-Pod node provisioning across the entire SKU catalog. NAP makes pool selection automatic; CA makes pool count automatic. NAP needs no fixed pools (it can create them); CA needs you to create them.",
        ),
        Misconception(
            myth="\"KEDA is just HPA with more sources.\"",
            truth="KEDA does that, plus enables <strong>scale-to-zero</strong>. HPA needs at least 1 Pod to read metrics; KEDA can drive replicas to 0 when external events show no load (queue empty, no cron firing). For event-driven workloads with idle hours, scale-to-zero is the cost story HPA alone cannot deliver.",
        ),
        Misconception(
            myth="\"Spot pools always save money.\"",
            truth="Spot saves <em>only when your workload tolerates eviction</em> — checkpoint-resume, idempotent retries, fault-tolerant queue consumption. If a workload restarts losing work or fails customer-facing requests during eviction, the SLA hit + retries cost more than on-demand. Use Spot for batch / ML / queue workers; not for stateful primaries.",
        ),
    ],
    flashcards=[
        Flashcard(front="Cluster Autoscaler vs NAP — when to use which?", back="<strong>CA</strong> = per-pool min/max; predictable, simple, you pick the pool SKU. <strong>NAP</strong> = per-Pod provisioning across SKU catalog; cost-optimal mix; consolidation rebins idle. NAP for mixed workloads + cost focus; CA for fixed shapes + simplicity. NAP is default in AKS Automatic."),
        Flashcard(front="What does KEDA do that HPA can\'t?", back="Scale on <strong>external events</strong> (Service Bus queue depth, Event Hub backlog, Storage Queue, Cron, Prometheus query, 60+ scalers) and <strong>scale to zero</strong>. HPA needs ≥1 Pod to read CPU; KEDA can run a Deployment at 0 replicas when no events."),
        Flashcard(front="Why are Spot pools auto-tainted?", back="To prevent regular workloads from accidentally landing on evictable nodes. Workloads that tolerate the <code>kubernetes.azure.com/scalesetpriority=spot:NoSchedule</code> taint are explicitly opting in to potential eviction with 30 seconds notice."),
        Flashcard(front="ARM node pools — when worth it?", back="Cobalt 100 / Ampere Altra are ~25% cheaper than equivalent x86 D-series for compute-bound workloads. Worth it when your container images are built for ARM64 (multi-arch images via <code>buildx</code>) and your workload runs cleanly on ARM."),
        Flashcard(front="Confidential Computing pools — what problem do they solve?", back="In-use memory encryption with attestation. AMD SEV-SNP on DCasv5/ECasv5 SKUs encrypts the VM\'s memory so even Azure host operators can\'t inspect it. For PII/PCI/financial workloads where in-use confidentiality is contractually required."),
        Flashcard(front="Why does PDB matter for autoscaling?", back="When CA / NAP scales in or maintenance drains a node, it respects PodDisruptionBudgets. A PDB with <code>maxUnavailable: 0</code> + min replicas = drain blocked. A workload with no PDB = no protection during drains. Set realistic PDBs that allow drains without dropping availability."),
        Flashcard(front="VPA — when to use, when to avoid?", back="<strong>Use:</strong> workloads with poorly-tuned CPU/memory requests; long-running services where right-sizing pays off. <strong>Avoid:</strong> on the same metric as HPA — you\'ll get scaling-on-scaling oscillation. Run VPA in <em>recommend</em> mode, then manually update; or use VPA on workloads HPA doesn\'t touch."),
        Flashcard(front="Multi-zone scaling pattern?", back="Pool created with <code>--zones 1 2 3</code>; CA spreads node count across zones. Combine with Pod topology-spread constraints (<code>topologyKey: topology.kubernetes.io/zone</code>) to keep replicas balanced. Storage: ZRS or per-zone PV pinning + app-level replication."),
    ],
    quizzes=[
        Quiz(
            prompt="100 Pods stuck Pending. CA logs: <code>scale-up: max-count reached on user-pool</code>. The team\'s emergency fix is to bump max-count from 5 to 50. What\'s the longer-term issue?",
            answer="Bumping max-count works for the immediate firefight but masks the deeper problem: a <em>fixed pool size</em> doesn\'t adapt to traffic shape. The team should consider migrating that workload to <strong>NAP (Node Auto Provisioning)</strong> so Azure picks node SKUs and counts on demand from the broader catalog — no max-count to forget. Alternatively split bursty workloads into a separate pool with a much higher max + scale-down-delay tuned for their traffic pattern.",
        ),
        Quiz(
            prompt="A team enables KEDA on a Service Bus queue scaler with target = 100 messages/Pod. Queue spikes to 50K messages. What does KEDA do and what could go wrong?",
            answer="KEDA computes desired replicas = 50000/100 = 500. Through HPA, it tries to scale the Deployment to 500. Things that can go wrong: (1) <strong>Cluster Autoscaler / NAP can\'t provision 500 nodes\' worth of Pods fast enough</strong> (CA scale operations take minutes), so initial backlog drain is slow; (2) the Deployment lacks a <code>maxReplicas</code> cap → runaway scaling exhausts subnet IPs / quota; (3) downstream DB / Service Bus connection limits choke before Pods can drain the queue. Fixes: cap maxReplicas; pre-warm a baseline; use NAP for fast provisioning; adjust target down if downstream is the bottleneck.",
        ),
        Quiz(
            prompt="The CFO sees the cluster bill, asks: \"Why aren\'t we 100% on Spot?\" The platform engineer freezes. What does she say?",
            answer="\"<strong>Because not every workload tolerates 30 seconds of eviction notice.</strong> Spot saves money only when the workload is fault-tolerant — checkpoint-resume, idempotent retries, queue-driven, or stateless replicas. Our stateful primaries, our user-facing low-latency APIs, and our control-plane workloads can\'t live on Spot — eviction = SLA breach + customer impact + replay cost greater than the saving. The right mix is Spot for batch / ML / queue workers (~30% of our spend), on-demand for stateful + low-latency (~70%). We\'re on it.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CFO",
        ),
    ],
    glossary=[
        GlossaryItem(name="Cluster Autoscaler (CA)", definition="Per-pool min/max node autoscaler. Adds/removes VMSS instances to satisfy Pending Pods."),
        GlossaryItem(name="Node Auto Provisioning (NAP)", definition="AKS\'s implementation of Karpenter. Provisions nodes across the SKU catalog on demand; consolidates idle capacity. Default in AKS Automatic."),
        GlossaryItem(name="KEDA", definition="Kubernetes Event-Driven Autoscaler. Managed AKS add-on. 60+ event scalers; scale-to-zero capable."),
        GlossaryItem(name="HPA", definition="Horizontal Pod Autoscaler — scales replicas on CPU / memory / custom metrics. Cannot scale to 0."),
        GlossaryItem(name="VPA", definition="Vertical Pod Autoscaler — right-sizes Pod CPU/memory requests over time. Don\'t mix with HPA on the same metric."),
        GlossaryItem(name="ScaledObject", definition="KEDA CRD — wraps a Deployment + scaler config; KEDA creates an HPA + injects external metrics."),
        GlossaryItem(name="Spot pool", definition="Node pool of Azure Spot VMs (up to 90% off, 30s eviction warning). Auto-tainted; workloads must tolerate."),
        GlossaryItem(name="GPU pool", definition="NC-series (NVIDIA T4 / A100 / H100) or ND-series. AKS GPU image preinstalls drivers; alternative is NVIDIA GPU Operator."),
        GlossaryItem(name="ARM pool", definition="Azure Cobalt 100 / Ampere Altra. ~25% cheaper than equivalent x86. Requires ARM64 container images."),
        GlossaryItem(name="Confidential Computing pool", definition="DCasv5/ECasv5 with AMD SEV-SNP. Memory encryption with attestation for regulated workloads."),
        GlossaryItem(name="PodDisruptionBudget (PDB)", definition="Caps how many Pods of a workload can be unavailable during voluntary disruption (drain, scale-in, upgrade)."),
        GlossaryItem(name="topology-spread constraints", definition="Pod scheduling hint that distributes replicas across zones / nodes for resilience."),
    ],
    recap_lead='Two scaling axes mapped: node-side (CA vs NAP) and Pod-side (HPA / VPA / KEDA). Specialty pools (Spot, GPU, Windows, ARM, Confidential, FIPS) are first-class. PDBs and topology-spread protect availability.',
    recap_next='<strong>Next — A6: AKS Security.</strong> Azure Policy for AKS (Gatekeeper-based), Microsoft Defender for Containers, Image Cleaner, ACR scanning + content trust, Workload Identity (recap), PSA, Azure Firewall, FIPS pools, host encryption, Confidential Containers (Kata + AMD SEV-SNP), Trusted Launch, Azure Linux 2 → 3 / Ubuntu 24 migration.',
)
