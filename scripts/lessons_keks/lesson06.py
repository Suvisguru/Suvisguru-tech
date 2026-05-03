from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Power floor: Karpenter brain provisioning EC2 mix - Graviton ARM, x86, GPU, Inferentia/Trainium - with spot/on-demand badges and consolidation arrows.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">POWER FLOOR · KARPENTER + COMPUTE MIX</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <rect x="14" y="34" width="160" height="120" rx="6" fill="#3F4A5E"/>
    <text x="94" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Karpenter</text>
    <text x="94" y="68" text-anchor="middle" font-size="8" fill="#FBE8DC">NodePool + EC2NodeClass</text>
    <text x="94" y="80" text-anchor="middle" font-size="8" fill="#FBE8DC">consolidation</text>
    <text x="94" y="92" text-anchor="middle" font-size="8" fill="#FBE8DC">spot strategies</text>
    <text x="94" y="104" text-anchor="middle" font-size="8" fill="#FBE8DC">disruption budget</text>
    <text x="94" y="124" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">picks instance type per Pod</text>
    <rect x="186" y="34" width="100" height="36" rx="3" fill="#5A9F7A"/><text x="236" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">Graviton (ARM)</text><text x="236" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">~25% cheaper</text>
    <rect x="296" y="34" width="100" height="36" rx="3" fill="#A04832"/><text x="346" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">x86 m6i / c7i</text><text x="346" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">general workloads</text>
    <rect x="406" y="34" width="100" height="36" rx="3" fill="#E8B547"/><text x="456" y="50" text-anchor="middle" font-size="9" fill="#5A4F45" font-weight="700">spot</text><text x="456" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">60-90% off</text>
    <rect x="186" y="80" width="100" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="236" y="96" text-anchor="middle" font-size="9" fill="#A04832" font-weight="700">P5 / G5 (NVIDIA)</text><text x="236" y="108" text-anchor="middle" font-size="7" fill="#5A4F45">training/inference</text>
    <rect x="296" y="80" width="100" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="346" y="96" text-anchor="middle" font-size="9" fill="#A04832" font-weight="700">Inferentia 2</text><text x="346" y="108" text-anchor="middle" font-size="7" fill="#5A4F45">cheap inference</text>
    <rect x="406" y="80" width="100" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="456" y="96" text-anchor="middle" font-size="9" fill="#A04832" font-weight="700">Trainium 2</text><text x="456" y="108" text-anchor="middle" font-size="7" fill="#5A4F45">training scale</text>
    <rect x="186" y="124" width="320" height="20" rx="3" fill="#3F4A5E"/><text x="346" y="138" text-anchor="middle" font-size="8" fill="#FBF1D6">Cluster Autoscaler (legacy) · EKS Auto Mode (E2) · EFA + Neuron device plugins</text>
    <rect x="514" y="34" width="76" height="120" rx="3" fill="#ECEFF5" stroke="#3F4A5E"/><text x="552" y="58" text-anchor="middle" font-size="8" fill="#3F4A5E" font-weight="700">cost</text><text x="552" y="74" text-anchor="middle" font-size="7" fill="#5A4F45">spot 70% off</text><text x="552" y="86" text-anchor="middle" font-size="7" fill="#5A4F45">SP/RI on baseline</text><text x="552" y="98" text-anchor="middle" font-size="7" fill="#5A4F45">Graviton +25%</text><text x="552" y="110" text-anchor="middle" font-size="7" fill="#5A4F45">consolidation</text><text x="552" y="124" text-anchor="middle" font-size="7" fill="#5A4F45">right-sizing</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="06",
    title_short="compute &amp; autoscaling",
    title_full="E6 · EKS Compute and Autoscaling (Karpenter, Spot, Graviton, GPU)",
    title_html="K-EKS E6 · EKS Compute and Autoscaling",
    module_eyebrow="Module E6 · the power floor",
    hero_sub_html='<strong>Karpenter</strong> is the recommended autoscaler for EKS (and the engine inside Auto Mode). Cluster Autoscaler is legacy. Cost optimisation = <strong>spot</strong> (60-90% off) + <strong>Graviton ARM</strong> (~25% cheaper) + <strong>Savings Plans</strong> on baseline. AI workloads use <strong>GPU (P/G), Inferentia, Trainium</strong> with the Neuron device plugin + EFA.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Production cluster on managed Node Groups + Cluster Autoscaler. Bursty workload scales 50 → 200 Pods; CA spins up 30 m5.large nodes (the only family in the NG). Cost: 30× $0.10/hr for 4 hours = $12/day. Karpenter would have picked t3.medium for the small Pods + c6i.large for the heavier ones, used spot, consolidated to 12 nodes after the burst, costing ~$4/day. <em>Per year: $3K vs $1.5K savings = $1.5K wasted plus all the ops time</em>. Today\'s lesson: pick the right autoscaler.',
    stamp_html='<strong>Karpenter</strong> = recommended autoscaler for EKS. NodePool + EC2NodeClass per workload class. Consolidation: WhenUnderutilized (aggressive) or WhenEmpty (conservative). <strong>Spot</strong> (60-90% off) for tolerant workloads + spot interruption handling. <strong>Graviton ARM</strong> (~25% cheaper, often faster per dollar). <strong>GPUs</strong> (P/G families) + <strong>Inferentia/Trainium</strong> + <strong>Neuron device plugin</strong> + <strong>EFA</strong> for distributed training. <strong>Savings Plans / RIs</strong> on the always-on baseline.',
    district_pin="ks-floor06",
    district_label="Power Floor",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Karpenter beats Cluster Autoscaler on EKS",
            body_html="""    <p><strong>Cluster Autoscaler (CA)</strong>: legacy. Scales Auto Scaling Groups based on Pending Pods. Each ASG is a fixed instance type. Spinning up new capacity = 60-120s. No instance-type optimisation per Pod. Doesn\'t consolidate.</p>
    <p><strong>Karpenter</strong>: modern. Picks the best EC2 instance type per Pending Pod. 20-40s spin-up. Consolidation built-in. Spot-aware. Mixed instance families per NodePool. AWS-built (open-source); EKS Auto Mode bundles + manages it.</p>
    <p>For new EKS clusters: <strong>EKS Auto Mode</strong> (which is Karpenter under the hood; AWS owns lifecycle — see E2). For existing clusters or shops wanting to manage Karpenter directly: <strong>self-managed Karpenter</strong>.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Karpenter NodePools, EC2NodeClasses, consolidation",
            h2="The CRDs you write",
            body_html="""    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># NodePool — workload-facing
apiVersion: karpenter.sh/v1
kind: NodePool
metadata: {name: general-spot}
spec:
  template:
    spec:
      nodeClassRef: {group: karpenter.k8s.aws, kind: EC2NodeClass, name: default}
      requirements:
      - {key: kubernetes.io/arch, operator: In, values: [amd64, arm64]}
      - {key: karpenter.sh/capacity-type, operator: In, values: [spot, on-demand]}
      - {key: karpenter.k8s.aws/instance-family, operator: In, values: [c6i, m6i, c7g, m7g]}
      - {key: karpenter.k8s.aws/instance-size, operator: NotIn, values: [nano, micro]}
      taints: []
  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 30s
    expireAfter: 720h
  limits: {cpu: 1000, memory: 1000Gi}
---
# EC2NodeClass — AWS-specific (only for self-managed Karpenter)
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata: {name: default}
spec:
  amiFamily: Bottlerocket
  role: KarpenterNodeRole
  subnetSelectorTerms: [{tags: {karpenter.sh/discovery: prod}}]
  securityGroupSelectorTerms: [{tags: {karpenter.sh/discovery: prod}}]</code></pre>""",
        ),
        Section(
            eyebrow="Section 1.7 · Cost optimisation",
            h2="Spot, Graviton, Savings Plans",
            body_html="""    <ul>
      <li><strong>Spot</strong>: unused EC2 capacity at 60-90% discount. AWS may interrupt with 2-min notice. Karpenter handles interruption (drains node gracefully) automatically. <strong>Workload fit</strong>: stateless, retry-tolerant, batch. <strong>Avoid</strong>: stateful primaries, long-running jobs without checkpointing.</li>
      <li><strong>Graviton (ARM)</strong>: AWS\'s ARM-based EC2 (m7g, c7g, r7g). Typically 20-30% cheaper for similar performance. Most modern container images are multi-arch. Just add <code>arm64</code> to NodePool requirements + use multi-arch images.</li>
      <li><strong>Savings Plans / Reserved Instances</strong>: on the always-on baseline (e.g., the bottom 30% of your average node count). Karpenter targets these instance types first; spot fills the bursts.</li>
      <li><strong>Right-sizing</strong>: tools like AWS Compute Optimizer + Karpenter\'s consolidation handle this automatically.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.9 · GPU, Inferentia, Trainium, EFA",
            h2="Compute for AI workloads",
            body_html="""    <ul>
      <li><strong>P5 / G5 (NVIDIA GPUs)</strong>: training (P5 = H100; P4 = A100) + inference (G5 = A10G; G6 = L40S). <strong>NVIDIA device plugin</strong> exposes GPUs to K8s. Pod requests <code>nvidia.com/gpu: 1</code>.</li>
      <li><strong>Inferentia 2 (Inf2)</strong>: AWS-designed inference chip. Cheaper than GPU for served models. Requires <strong>AWS Neuron SDK</strong> + Neuron device plugin.</li>
      <li><strong>Trainium 2 (Trn2)</strong>: AWS-designed training chip. Scales to large clusters. Same Neuron SDK + device plugin.</li>
      <li><strong>EFA (Elastic Fabric Adapter)</strong>: low-latency network for distributed training. Required for NCCL all-reduce at scale on multi-node GPU. Specific instance types only (P5/Trn2). Karpenter NodePool requirement: <code>vpc.amazonaws.com/efa: "true"</code>.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For ML platform teams: dedicated Karpenter NodePool per accelerator family (GPU spot for training, Inferentia for serving, CPU for general). Each with appropriate taints + tolerations to keep general workloads off expensive accelerators.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your team uses Cluster Autoscaler with one Managed Node Group of m5.large. The cluster scales 10 → 100 nodes during a marketing campaign. After the campaign, scales back to 10. Cost is high. What\'s the Karpenter pitch?',
            options=[
                ('a) Karpenter would do exactly the same thing.', False),
                ('b) Karpenter picks the right size per Pod (small for small Pods, large for large), can use spot, can consolidate idle nodes — savings often 30-50% on similar workloads.', True),
                ('c) Karpenter only works for GPUs.', False),
            ],
            feedback='<strong>Answer: b.</strong> Per-Pod instance picking + consolidation + spot are Karpenter\'s three big advantages. The scale-down side is huge for bursty workloads — CA leaves nodes around longer than needed.',
        ),
    },
    before_after_before='<p>Cluster Autoscaler + 1-3 fixed-instance NGs. m5.large for everything. No spot. Reserved Instance commitment for the wrong instance family. Idle nodes overnight. Surprise AWS bill at quarter-end.</p>',
    before_after_after='<p>Karpenter picks instance per Pod. Spot 70% of compute. Graviton for new workloads (multi-arch images). RIs / SP on baseline only. Consolidation overnight reduces idle. Cost down 35-50% on the same workload mix.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Karpenter on EKS is one of the highest-leverage cost optimizations available — and it improves reliability (spot interruption handling, consolidation graceful) at the same time.</p>',
    analogy_intro_html='<p>The Power Floor is the hum of the building. The dispatcher (Karpenter) sits at a console showing real-time demand from every floor (Pods). When a new workload arrives, dispatcher picks the best generator from the rental fleet (EC2): a Graviton-ARM unit for energy efficiency, a spot generator for non-critical loads, a GPU rig for the AI workshop. When demand drops, generators are released (consolidation). The fleet manager has SLAs (NodePool limits) and disruption budgets so critical workloads aren\'t turfed out at the wrong moment.</p>',
    translation_rows=[
        ('Power dispatcher console', 'Karpenter controller'),
        ('Workload demand sheet', 'Pending Pods'),
        ('Generator type catalogue', 'Instance families (c6i, m6i, c7g, P5, Inf2)'),
        ('Energy-efficient ARM generator', 'Graviton (m7g, c7g, r7g)'),
        ('Spot-rate generator', 'Spot capacity (60-90% off)'),
        ('AI workshop\'s specialty rig', 'GPU / Inferentia / Trainium with Neuron + EFA'),
        ('Releasing under-utilised generators', 'Consolidation (WhenUnderutilized)'),
        ('Long-term lease on baseline', 'Savings Plans / RIs'),
    ],
    analogy_stops="The analogy stops here: real Karpenter is a controller speaking to AWS EC2 + ASG APIs, evaluating 100s of instance type options per pending Pod. The dispatcher metaphor undersells the optimization math.",
    eli5='Smart power-station operator. Picks the right type of generator for the job (small for small jobs, big for big), uses cheap energy when possible, turns off generators when not needed.',
    eli10="Karpenter = recommended EKS autoscaler. NodePool (workload constraints) + EC2NodeClass (AWS specifics). Picks instance type per Pod. Consolidation reduces idle. Spot for cost (60-90% off). Graviton ARM (~25% cheaper). Savings Plans on baseline. GPU/Inferentia/Trainium for AI with Neuron device plugin + EFA. EKS Auto Mode bundles Karpenter; self-managed Karpenter still common.",
    scenarios=[
        Scenario(name='A SaaS using Karpenter + 70% spot', body='Single NodePool: c6i / m6i / c7g / m7g instance families, spot+on-demand, WhenUnderutilized consolidation. Karpenter picks 70% spot, 30% on-demand for non-tolerant workloads. AWS bill ~40% lower than the same workload on managed NGs.'),
        Scenario(name='A bank using Karpenter + RIs on baseline', body='Always-on baseline of ~30 m6i.large covered by Compute Savings Plans (~30% off SP rate). Karpenter\'s NodePool prefers m6i.large to land on the SP-covered capacity; spot for bursts. Cost-finance reconciliation easier; baseline predictable.'),
        Scenario(name='An ML team running PyTorch on P5 + EFA', body='Dedicated NodePool: P5.48xlarge, EFA enabled, taint <code>nvidia.com/gpu</code>:NoSchedule. Training Pods tolerate; nothing else schedules there. NCCL benchmarks: 96% scaling efficiency 16 → 64 GPUs over EFA. Cost: $32K/month for the GPU pool; pays back in faster training cycles.'),
        Scenario(name='An inference team migrating CPU → Inferentia', body='Identified 5 always-on inference Pods on c6i.4xlarge. Migrated models to Neuron-compiled versions; switched to Inf2.xlarge (~3× cheaper for the same throughput). Cost saved: ~$1500/month per service.'),
    ],
    misconceptions=[
        Misconception(myth='\"Spot is too risky for production.\"', truth='Spot interruption is 2 min notice + Karpenter handles drain. For stateless workloads with PDBs, spot is fine in production. AWS\'s spot-interruption rate per instance type is published; pick types with low rates (often older generations).'),
        Misconception(myth='\"Graviton requires re-architecting workloads.\"', truth='Most modern container images are multi-arch (or trivially rebuildable). Java, Go, Python, Node — all run on ARM. Test on staging; the gotchas are usually obscure native-binary dependencies (e.g., very-old C extensions in Python wheels).'),
        Misconception(myth='\"Karpenter and Cluster Autoscaler can coexist.\"', truth='Technically yes, but they\'ll fight over scaling decisions. Pick one. Migration: install Karpenter, validate it\'s picking up Pending Pods, then disable CA on the relevant NGs.'),
    ],
    flashcards=[
        Flashcard(front='Karpenter vs Cluster Autoscaler?', back='Karpenter: per-Pod instance picking, 20-40s spin-up, consolidation built-in, spot-aware. CA: ASG-based, 60-120s spin-up, fixed instance type per ASG, no consolidation. Karpenter wins on EKS.'),
        Flashcard(front='NodePool + EC2NodeClass — what each defines?', back='NodePool = workload constraints (arch, capacity type, instance family, disruption). EC2NodeClass = AWS specifics (subnets, SGs, AMI, IAM role). Multiple NodePools per cluster.'),
        Flashcard(front='Karpenter consolidation modes?', back='WhenUnderutilized = aggressive (replace lightly-loaded nodes with fewer/cheaper). WhenEmpty = only fully-empty nodes. Default is WhenUnderutilized for cost optimization.'),
        Flashcard(front='How does spot interruption work?', back='AWS sends 2-min interruption notice. Karpenter (or Auto Mode) detects, drains the node gracefully, schedules replacement. PodDisruptionBudgets respected. Workloads with retries / replicas tolerate well.'),
        Flashcard(front='Graviton workload requirements?', back='Multi-arch container image (or arm64-only image). Most managed runtimes (JVM, Go, Python, Node) run on ARM cleanly. Native binary dependencies need testing. NodePool: <code>arch In [arm64]</code> or both archs.'),
        Flashcard(front='When use Inferentia / Trainium vs NVIDIA?', back='Inferentia: cheap inference (3-5x cheaper than GPU for served models). Trainium: training at large scale. Both require Neuron SDK + Neuron device plugin. NVIDIA: established + flexible; safest for novel models.'),
        Flashcard(front='EFA — when?', back='Distributed multi-node GPU training (PyTorch DDP, Horovod, NCCL all-reduce). Specific instance types (P5, Trn2). NodePool requirement: <code>vpc.amazonaws.com/efa: \"true\"</code>.'),
        Flashcard(front='Cost optimization stack on EKS?', back='Karpenter (per-Pod sizing + consolidation) + Spot (60-90% off, retry-tolerant workloads) + Graviton (~25% cheaper) + Savings Plans on always-on baseline + right-sizing.'),
    ],
    quizzes=[
        Quiz(prompt='Your team\'s Karpenter is launching r6i.large for a Pod that requests 0.5 CPU + 1 GiB RAM. Why is it picking such a big instance?', answer='<strong>Diagnose the NodePool requirements.</strong> If <code>karpenter.k8s.aws/instance-size</code> doesn\'t exclude small types, Karpenter should pick a smaller one. Likely causes: (1) <em>NodePool excludes small types</em> — fix the requirement. (2) <em>Subnet IP exhaustion</em> — Karpenter picks bigger types if small types can\'t get IPs (smaller types have fewer ENI slots). Check subnet IP availability + enable VPC CNI prefix delegation (E3). (3) <em>Pod has additional resource requests you didn\'t see</em> — sidecars, init containers, ephemeral storage. <code>kubectl describe pod</code> shows the full resource picture. (4) <em>Topology constraints</em> — if Pod requires a zone that has only large instance availability, Karpenter goes with what\'s there. <strong>Long-term:</strong> log Karpenter decisions: <code>kubectl logs -n karpenter deploy/karpenter</code> + look for <code>Launched node</code> events with the reasoning.'),
        Quiz(prompt='You want to migrate a CPU-based inference service to Inferentia for cost savings. Plan?', answer='<strong>(1) Compile the model with Neuron SDK.</strong> Some model architectures compile cleanly (TF, PyTorch via TorchScript / Optimum); some need rework. Validate accuracy + latency match the CPU baseline. <strong>(2) Build a Neuron-aware container image.</strong> Base image: <code>763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference-neuron:...</code>. Bundle the Neuron-compiled model. <strong>(3) Add a Karpenter NodePool</strong>: Inf2.xlarge, taint <code>aws.amazon.com/neuron</code>:NoSchedule. <strong>(4) Update Deployment</strong>: tolerate the taint, request <code>aws.amazon.com/neuron: 1</code> (Neuron device plugin advertises this resource). <strong>(5) Roll out behind a feature flag / canary.</strong> Compare p99 latency + error rate to CPU. <strong>(6) Validate cost.</strong> Inf2.xlarge ~ $0.76/hr vs c6i.4xlarge ~$0.68/hr — but Inferentia handles 3-5x throughput per chip, so per-request cost drops 50-70%. <strong>(7) Decommission CPU pool.</strong>'),
        Quiz(prompt='You\'re asked to optimize a $10K/month EKS bill. <strong>Click for the playbook. ▼</strong>', cyoa=True, cyoa_tag='the playbook', answer='<strong>(1) Visibility first.</strong> Enable <strong>AWS Split Cost Allocation Data for EKS</strong> + Cost Explorer view per namespace + Kubecost or OpenCost. Map cost to teams + workloads. Find the top 5 spenders. <strong>(2) Karpenter consolidation</strong> on the biggest cluster. If you\'re on managed NGs, install Karpenter (or migrate to Auto Mode). Estimated savings: 20-30%. <strong>(3) Spot adoption</strong> for stateless / batch workloads. NodePool with spot+on-demand; Pods tolerate spot via Karpenter\'s default behaviour. Estimated additional savings: 15-30% of the spot-eligible portion. <strong>(4) Graviton</strong> for new workloads or trivially-portable existing ones (Java/Go/Python). Multi-arch images; NodePool allows arm64. Savings: 20-25% on those workloads. <strong>(5) Savings Plans</strong> on the post-optimization baseline (the consistent 24/7 floor). Don\'t lock in to RIs / SPs <em>before</em> optimizing — you\'d lock in waste. <strong>(6) Right-sizing</strong>: AWS Compute Optimizer + Karpenter consolidation handle this; review quarterly. <strong>(7) Storage</strong>: gp3 instead of gp2 (cheaper + better perf); EFS Lifecycle to IA; S3 Mountpoint instead of staging to EBS. <strong>Total: typically 30-50% reduction</strong> for a cluster that\'s never been optimized. <strong>$10K → $5-7K</strong>.'),
    ],
    glossary=[
        GlossaryItem(name='Karpenter', definition='AWS open-source K8s autoscaler. Per-Pod instance picking, fast spin-up, consolidation, spot-aware.'),
        GlossaryItem(name='NodePool (Karpenter)', definition='Workload-facing CRD: requirements (arch, capacity type, instance family), disruption rules.'),
        GlossaryItem(name='EC2NodeClass', definition='AWS-specific Karpenter CRD: subnets, SGs, AMI, IAM role. (Auto Mode uses NodeClass instead.)'),
        GlossaryItem(name='Consolidation', definition='Karpenter behaviour: replace lightly-loaded nodes with fewer/cheaper ones. WhenUnderutilized vs WhenEmpty.'),
        GlossaryItem(name='Spot capacity', definition='Unused EC2 at 60-90% discount. 2-min interruption notice. Karpenter handles drain.'),
        GlossaryItem(name='Graviton', definition='AWS ARM-based EC2 (m7g, c7g, r7g). ~25% cheaper for similar performance. Multi-arch images required.'),
        GlossaryItem(name='Savings Plans', definition='AWS commitment-based pricing. Compute Savings Plans cover EC2 / Fargate flexibly. Apply to baseline.'),
        GlossaryItem(name='Reserved Instances', definition='Older commitment model. Per-instance-type. Less flexible than Savings Plans.'),
        GlossaryItem(name='NVIDIA device plugin', definition='K8s DaemonSet that advertises <code>nvidia.com/gpu</code> resources. Required for GPU workloads.'),
        GlossaryItem(name='Neuron SDK / device plugin', definition='AWS toolchain for Inferentia + Trainium. Compile models for Neuron; advertise <code>aws.amazon.com/neuron</code> resources.'),
        GlossaryItem(name='EFA (Elastic Fabric Adapter)', definition='Low-latency networking for HPC / distributed training. Specific instance types (P5, Trn2).'),
        GlossaryItem(name='Cluster Autoscaler', definition='Legacy ASG-based autoscaler. Slower, no consolidation, fixed instance type per ASG. Replaced by Karpenter on EKS.'),
    ],
    recap_lead='Karpenter is the recommended EKS autoscaler (and the engine inside Auto Mode). NodePool + EC2NodeClass + consolidation. Cost stack: spot + Graviton + Savings Plans on baseline + right-sizing. AI: GPU / Inferentia / Trainium with Neuron + EFA.',
    recap_next='<strong>Next — E7: EKS Security.</strong> KMS encryption for secrets / EBS / EFS, GuardDuty EKS Protection + Runtime Monitoring, Security Hub, Inspector, ECR scanning + signing, Bottlerocket nodes, FIPS, CloudTrail.',
)
