from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="EKS Auto Mode: NodePool / NodeClass cards driving AWS-managed nodes; consolidation arrow merging boxes; built-in components row.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">EKS AUTO MODE · CONCIERGE FOR NODES</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <rect x="14" y="34" width="180" height="100" rx="6" fill="#3F4A5E"/>
    <text x="104" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">NodePool / NodeClass</text>
    <text x="104" y="70" text-anchor="middle" font-size="8" fill="#FBE8DC">requirements + constraints</text>
    <text x="104" y="84" text-anchor="middle" font-size="8" fill="#FBE8DC">disruption budget</text>
    <text x="104" y="98" text-anchor="middle" font-size="8" fill="#FBE8DC">max node lifetime</text>
    <text x="104" y="120" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">declarative inputs</text>
    <rect x="206" y="34" width="180" height="100" rx="6" fill="#A04832"/>
    <text x="296" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">AWS Auto Mode brain</text>
    <text x="296" y="68" text-anchor="middle" font-size="8" fill="#FBE8DC">picks instance type</text>
    <text x="296" y="80" text-anchor="middle" font-size="8" fill="#FBE8DC">provisions EC2</text>
    <text x="296" y="92" text-anchor="middle" font-size="8" fill="#FBE8DC">consolidates idle</text>
    <text x="296" y="104" text-anchor="middle" font-size="8" fill="#FBE8DC">replaces aged nodes</text>
    <text x="296" y="120" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">controller (~Karpenter-style)</text>
    <rect x="398" y="34" width="186" height="100" rx="6" fill="#5A9F7A"/>
    <text x="491" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">built-in components</text>
    <text x="491" y="68" text-anchor="middle" font-size="8" fill="#FBE8DC">VPC CNI · EBS CSI · LB controller</text>
    <text x="491" y="80" text-anchor="middle" font-size="8" fill="#FBE8DC">CoreDNS · health checks · GPU</text>
    <text x="491" y="92" text-anchor="middle" font-size="8" fill="#FBE8DC">immutable Bottlerocket AMIs</text>
    <text x="491" y="104" text-anchor="middle" font-size="8" fill="#FBE8DC">auto-rotated regularly</text>
    <text x="491" y="120" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">no add-on management</text>
    <rect x="14" y="142" width="572" height="14" rx="3" fill="#ECEFF5" stroke="#3F4A5E"/>
    <text x="300" y="152" text-anchor="middle" font-size="8" fill="#3F4A5E" font-style="italic">Auto Mode vs Managed NG: AWS owns the lifecycle. vs Karpenter: AWS bundles it + manages it.</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="02",
    title_short="EKS Auto Mode",
    title_full="E2 · EKS Auto Mode — AWS Picks the Nodes",
    title_html="K-EKS E2 · EKS Auto Mode",
    module_eyebrow="Module E2 · concierge service for the cluster\'s nodes",
    hero_sub_html='Auto Mode is AWS\'s answer to \"I don\'t want to think about nodes.\" You declare workload <strong>NodePools</strong> + <strong>NodeClasses</strong>; AWS provisions EC2, manages lifecycle, consolidates idle capacity, replaces aged nodes — all automatic. Plus AWS bundles + manages the core add-ons (VPC CNI, EBS CSI, LB controller, CoreDNS).',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Pre-Auto-Mode, your team operated three managed Node Groups (general / memory / GPU), Karpenter on top, and per-node Bottlerocket update cadence. Every K8s upgrade meant: AMI bump on each NG, Karpenter version bump, drain + uncordon dance, validate add-ons. Three days of work per quarter. <em>Auto Mode collapses all of that to \"AWS handles it.\"</em> The trade: less control over instance choice + AMI customisation. Today\'s lesson: when that trade is right.',
    stamp_html='EKS Auto Mode = AWS\'s built-in compute layer. You declare <strong>NodePool</strong> (label/taint/disruption rules) + <strong>NodeClass</strong> (instance constraints). AWS provisions EC2, picks instance type, manages lifecycle, consolidates idle, replaces nodes on a regular cadence (max node lifetime). Bundles core add-ons (VPC CNI, EBS CSI, LB controller, CoreDNS, GPU plugins, health checkers) — AWS upgrades them. <strong>Auto Mode vs Managed NG vs Karpenter</strong>: Auto Mode is the modern default for new clusters; doesn\'t fit every shop.',
    district_pin="ks-floor02",
    district_label="Concierge Service",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What Auto Mode owns and what it doesn\'t",
            body_html="""    <p>Auto Mode (released GA in late 2024) is EKS\'s built-in compute and add-on layer. AWS bundles together:</p>
    <ul>
      <li><strong>Compute provisioning</strong> — Karpenter-style instance picking + provisioning + consolidation. AWS owns the controller; you don\'t install or upgrade it.</li>
      <li><strong>Core add-ons</strong> — VPC CNI, EBS CSI, AWS Load Balancer Controller, CoreDNS, kube-proxy. AWS keeps them updated; you don\'t install or upgrade them.</li>
      <li><strong>Immutable AMIs</strong> — Bottlerocket-based; AWS rotates regularly (max node lifetime).</li>
      <li><strong>Health checks + auto-replace</strong> — bad nodes get drained + replaced automatically.</li>
    </ul>
    <p>What Auto Mode doesn\'t own: your workloads, your IAM (still IRSA / Pod Identity), your VPC + subnet design, your storage decisions beyond EBS. You still write Deployments, Services, etc.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · NodePools and NodeClasses",
            h2="The two CRDs you actually write",
            body_html="""    <p>Auto Mode uses Karpenter-style CRDs (familiar if you\'ve run open-source Karpenter):</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># NodePool — workload-facing rules
apiVersion: karpenter.sh/v1
kind: NodePool
metadata: {name: default}
spec:
  template:
    spec:
      nodeClassRef:
        group: eks.amazonaws.com
        kind: NodeClass
        name: default
      requirements:
      - {key: kubernetes.io/arch, operator: In, values: [amd64, arm64]}
      - {key: karpenter.sh/capacity-type, operator: In, values: [spot, on-demand]}
      taints: []
  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 30s
    expireAfter: 720h            # max node lifetime: 30 days
  limits: {cpu: 1000, memory: 1000Gi}

---
# NodeClass — Auto-Mode-specific config (subnet/SG selectors, etc.)
apiVersion: eks.amazonaws.com/v1
kind: NodeClass
metadata: {name: default}
spec:
  role: AmazonEKSAutoNodeRole
  subnetSelectorTerms:
  - tags: {kubernetes.io/role/internal-elb: "1"}
  securityGroupSelectorTerms:
  - tags: {Name: my-cluster-node-sg}</code></pre>
    <p><strong>NodePool</strong> = workload constraints (arch, capacity type, instance family, disruption rules). <strong>NodeClass</strong> = AWS-specific networking (subnets, SGs, tags). Multiple NodePools per cluster is the norm (one for general, one for GPU, one for spot).</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Disruption + lifecycle",
            h2="Consolidation, expiration, replacement",
            body_html="""    <ul>
      <li><strong>WhenUnderutilized consolidation</strong>: Auto Mode periodically checks if running nodes can be replaced with fewer/cheaper ones. If yes, drains and recreates. The default; saves cost on bursty workloads.</li>
      <li><strong>WhenEmpty consolidation</strong>: only consolidate fully-empty nodes. Slower but more predictable; less Pod churn.</li>
      <li><strong>consolidateAfter</strong>: cooldown between consolidation passes (e.g., 30s). Prevents thrashing.</li>
      <li><strong>expireAfter (max node lifetime)</strong>: every node is replaced after N hours. Default 720h (30 days). Forces regular rotation; ensures latest AMI; bounds patch drift.</li>
      <li><strong>disruption budgets</strong>: per-NodePool, control how aggressively AWS can drain. Coordinated with PodDisruptionBudgets at the workload level.</li>
    </ul>
    <p>Auto Mode emits K8s events on each disruption: <code>kubectl get events -A | grep -i nodeclaim</code>. Watch for unexpected churn during bootstrap.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Auto Mode vs Managed NG vs Karpenter",
            h2="When to pick which",
            body_html="""    <table class="data-table">
      <thead><tr><th></th><th>Managed NG</th><th>Karpenter (DIY)</th><th>EKS Auto Mode</th></tr></thead>
      <tbody>
        <tr><td>Who picks instance type</td><td>You (per NG)</td><td>Karpenter (per Pod)</td><td>AWS Auto Mode (per Pod)</td></tr>
        <tr><td>Lifecycle owner</td><td>AWS lifecycle controller</td><td>You operate Karpenter</td><td>AWS Auto Mode</td></tr>
        <tr><td>Consolidation</td><td>None (manual)</td><td>Yes</td><td>Yes (built-in)</td></tr>
        <tr><td>Add-on management</td><td>You install + upgrade</td><td>You install + upgrade</td><td>AWS bundles + upgrades</td></tr>
        <tr><td>Customisation</td><td>High (custom AMIs)</td><td>High (Karpenter is yours)</td><td>Lower (Bottlerocket only)</td></tr>
        <tr><td>Best for</td><td>Predictable, capacity-known workloads</td><td>Cost optimisation + control</td><td>New clusters; small ops teams</td></tr>
      </tbody>
    </table>
    <p><strong>2026 default</strong>: new clusters → EKS Auto Mode unless you have a specific reason not to (custom AMI, kernel modules, regulatory, very-high-control). Existing Karpenter shops can migrate cluster-by-cluster.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>Pricing: EKS Auto Mode adds a per-vCPU-hour management fee on top of EC2 cost. For a typical workload it\'s 12-15% premium. The math: you save the SRE time + you avoid most node-related incidents. Most teams find it worth it.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your existing cluster runs Karpenter, ALB controller, EBS CSI, all installed via Helm. You want to migrate to EKS Auto Mode. What\'s the right approach?',
            options=[
                ('a) Toggle Auto Mode on; AWS automatically takes over your existing components', False),
                ('b) Stand up a new cluster with Auto Mode enabled, migrate workloads via GitOps, decommission the old cluster. Or: use AWS\'s Auto Mode migration guide which uninstalls existing components in stages.', True),
                ('c) You can\'t migrate; rebuild from scratch', False),
            ],
            feedback='<strong>Answer: b.</strong> Auto Mode owns specific components; can\'t coexist with hand-installed copies. AWS provides a migration path (uninstall self-managed Karpenter, ALB controller, etc., then enable Auto Mode), but the safer pattern is blue-green: new cluster with Auto Mode + migrate workloads. Existing Karpenter clusters are most disrupted.',
        ),
    },
    before_after_before='<p>Karpenter Helm chart pinned + monitored. ALB controller installed + IAM attached + CRDs upgraded. EBS CSI version-tracked. AMI bumps for each NG every quarter. Three add-ons to upgrade per K8s minor. Five hours of node-related ops per week.</p>',
    before_after_after='<p>Auto Mode toggled on. NodePool + NodeClass YAML in git. Add-ons managed by AWS. Node lifecycle, instance picking, consolidation, AMI rotation — all handled. Hours of node ops per week: 0-1.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Auto Mode is to nodes what EKS itself is to the control plane: AWS owns the operational toil; you keep the workload control.</p>',
    analogy_intro_html='<p>The Concierge Service desk on the K-Skyline lobby. Tell the concierge what you need (NodePool: \"this many guests, these dietary needs, this budget tier\"); they assign rooms (NodeClasses → EC2 instances), refresh them on a schedule (max node lifetime), upgrade the bedding (AMI rotation), close unused rooms (consolidation). The concierge also manages the building\'s shared services (CNI, CSI, LB) so you don\'t. You walk in, hand them a list, and the rooms appear.</p>',
    translation_rows=[
        ('The concierge service desk', 'EKS Auto Mode'),
        ('Your guest list + needs', '<code>NodePool</code> requirements'),
        ('Room-type catalogue', '<code>NodeClass</code> (subnets, SGs, instance constraints)'),
        ('Refreshing rooms on a schedule', '<code>expireAfter</code> (max node lifetime)'),
        ('Combining lightly-occupied rooms', 'Consolidation (<code>WhenUnderutilized</code>)'),
        ('Replacing a sick guest\'s room', 'Health-check + auto-replace'),
        ('Hotel\'s shared utilities', 'Built-in CNI / CSI / LB / CoreDNS'),
        ('Concierge tip on the bill', 'Auto Mode per-vCPU-hour premium'),
    ],
    analogy_stops="The analogy stops here: EKS Auto Mode is software, not staff. The \"concierge\" is a controller in the control plane reconciling NodePool/NodeClass to EC2 calls.",
    eli5='You don\'t pick the rooms in the hotel — you tell the front desk what you need (\"two adults, one cot\") and they pick. They also clean and refresh the rooms automatically.',
    eli10="EKS Auto Mode is Karpenter + core add-ons bundled into EKS, owned by AWS. You declare NodePool (workload constraints) + NodeClass (AWS-specific). AWS provisions EC2, manages lifecycle, consolidates idle, replaces nodes after expireAfter, and updates the bundled add-ons (VPC CNI, EBS CSI, LB controller, CoreDNS). vs Managed NG: AWS owns the lifecycle. vs Karpenter: AWS bundles + manages it. Premium ~12-15% on top of EC2.",
    scenarios=[
        Scenario(name='A SaaS using Auto Mode for everything', body='Single NodePool with arch In [amd64, arm64], spot+on-demand, WhenUnderutilized consolidation, expireAfter 7 days. Cluster of 25 workloads scales 8 → 30 nodes during day, consolidates back to 8 overnight. Add-ons just work. SRE team: 1.'),
        Scenario(name='A bank using Auto Mode + a separate managed NG', body='Auto Mode for general workloads. Separate managed Node Group for a regulated workload requiring a hardened custom AMI Auto Mode doesn\'t support. Two compute paths in one cluster; both use the same VPC + IAM.'),
        Scenario(name='A startup migrating from Karpenter to Auto Mode', body='Followed AWS\'s migration guide: paused Karpenter consolidation; uninstalled Karpenter Helm release; enabled Auto Mode; recreated NodePools with the new CRD shapes. Total downtime: 0 (Karpenter-managed nodes drained as Auto Mode took over). One sprint of validation.'),
        Scenario(name='A team picking Managed NG over Auto Mode', body='Heavy use of EBS RAID-0 across multiple volumes, requires a custom Bottlerocket build with kernel modules. Auto Mode\'s standard AMI doesn\'t fit. Sticking with Managed NG + custom AMI; revisiting Auto Mode if AWS adds custom-AMI support.'),
    ],
    misconceptions=[
        Misconception(myth='\"Auto Mode is just Karpenter renamed.\"', truth='Mostly true at the compute layer, but Auto Mode bundles core add-ons too (VPC CNI, EBS CSI, LB controller, CoreDNS). And AWS owns the lifecycle of all of that — you don\'t install or upgrade.'),
        Misconception(myth='\"Auto Mode is more expensive than Managed NG + Karpenter.\"', truth='Per-vCPU premium ~12-15%. But you save SRE time on Karpenter ops + add-on upgrades + AMI lifecycle. For most teams the all-in TCO is similar or better.'),
        Misconception(myth='\"Once on Auto Mode, you can\'t use other compute options.\"', truth='You can mix. Auto Mode + a separate Managed NG for a custom-AMI workload + Fargate for tiny workloads — all in one cluster.'),
    ],
    flashcards=[
        Flashcard(front='What does Auto Mode bundle?', back='Karpenter-style compute (NodePools + NodeClasses) + core add-ons (VPC CNI, EBS CSI, AWS LB controller, CoreDNS, kube-proxy, GPU plugins) + Bottlerocket AMIs. AWS owns lifecycle of all.'),
        Flashcard(front='NodePool vs NodeClass?', back='NodePool = workload-facing (requirements, taints, disruption budget, expireAfter). NodeClass = AWS-specific (subnets, SGs, IAM role, AMI). Multiple NodePools per cluster is normal.'),
        Flashcard(front='What is consolidation?', back='Auto Mode periodically checks if running nodes can be replaced with fewer/cheaper ones. WhenUnderutilized = aggressive (drain + replace lightly-loaded). WhenEmpty = only fully-empty nodes.'),
        Flashcard(front='expireAfter / max node lifetime?', back='Time after which Auto Mode replaces a node regardless of load. Default 720h (30 days). Forces AMI rotation + bounds patch drift.'),
        Flashcard(front='disruption budget (Auto Mode)?', back='Per-NodePool cap on simultaneous voluntary disruptions. Coordinated with PodDisruptionBudgets at the workload level. Prevents over-aggressive consolidation.'),
        Flashcard(front='Auto Mode vs Karpenter?', back='Functionally similar at compute layer. Auto Mode = AWS bundles + manages it. DIY Karpenter = you install + upgrade. Auto Mode adds bundled add-ons; DIY Karpenter is just compute.'),
        Flashcard(front='Auto Mode vs Managed NG?', back='Managed NG = you pick instance type + count per NG; AWS does lifecycle. Auto Mode = AWS picks instance type per Pod + does lifecycle + consolidation. Auto Mode is dynamic; NG is static.'),
        Flashcard(front='Auto Mode pricing model?', back='Per-vCPU-hour management premium on top of underlying EC2. ~12-15% for typical workloads. Trades cost for SRE time saved.'),
    ],
    quizzes=[
        Quiz(prompt='You enable Auto Mode on a new cluster. After 1 hour, your dashboards show 25 small nodes coming up + going down. Diagnosis?', answer='<strong>Consolidation thrashing.</strong> Common causes: (1) <em>consolidateAfter too short</em>. Default is fine; if you set 0s, Auto Mode reconsiders every cycle. Bump to 30s+. (2) <em>Pod placement is unstable</em>. Workloads coming + going (e.g., a Deployment with PreferNoSchedule that flips placement). Fix: tune affinity / topology spread for stability. (3) <em>Mismatched disruption budgets</em>: PDBs + NodePool budgets fighting. Verify both. <strong>Diagnostic:</strong> <code>kubectl get nodeclaims -A</code> + <code>kubectl get events -A | grep -i nodeclaim</code> show consolidation reasoning. <strong>Long-term:</strong> graph node count over time + cluster cost; if cost is volatile, tune.'),
        Quiz(prompt='You\'re running Karpenter v1.0 + EKS managed Node Group + AWS LB Controller (Helm). Migration plan to Auto Mode?', answer='<strong>Pre-migration:</strong> staging cluster on Auto Mode; validate workloads (especially Deployments with hostNetwork or kernel-version assumptions). <strong>Production migration:</strong> (1) <strong>Pause Karpenter</strong> consolidation by setting all NodePools to 0 limits. (2) <strong>Enable Auto Mode</strong> on the cluster (<code>aws eks update-cluster-config --compute-config enabled=true</code>). (3) <strong>Define new NodePools</strong> in the karpenter.sh API; Auto Mode picks them up. (4) <strong>Drain existing Karpenter nodes</strong> one at a time; Auto Mode provisions replacements. (5) <strong>Uninstall Karpenter Helm release</strong>; remove RBAC. (6) <strong>Uninstall AWS LB Controller</strong> Helm; Auto Mode\'s built-in version takes over. <strong>Roll-back path:</strong> disable Auto Mode (<code>compute-config enabled=false</code>) + reinstall Karpenter from values.yaml in git. Test the rollback in staging before prod. <strong>Total time:</strong> 1-2 weeks for a 30-node cluster including validation.'),
        Quiz(prompt='You\'re asked to recommend Auto Mode vs Karpenter vs Managed NG for a new cluster. <strong>Click for the decision tree. ▼</strong>', cyoa=True, cyoa_tag='the decision tree', answer='<strong>Step 1: do you need custom AMIs / kernel modules / specific Bottlerocket variants?</strong> Yes → Managed NG (Auto Mode\'s AMI is fixed). No → continue. <strong>Step 2: do you have an existing Karpenter investment + a strong opinion about its config (custom plugins, custom controllers)?</strong> Yes → keep Karpenter; revisit Auto Mode in 12 months. No → continue. <strong>Step 3: is your team small (≤2 SREs) and are you fine with AWS-bundled add-ons?</strong> Yes → Auto Mode (saves the most time). No → continue. <strong>Step 4: do you have predictable, sustained workloads where reserved capacity or Savings Plans dominate cost?</strong> Yes → Managed NG with RIs/SP optimised. No → Auto Mode (consolidation handles it). <strong>Step 5: are you in a region without Auto Mode yet?</strong> Yes → Managed NG + Karpenter; migrate when available. <strong>Most teams in 2026 land on Auto Mode</strong> by default + a small Managed NG for special workloads. <strong>Karpenter DIY</strong> remains for shops that want full control of the compute layer.'),
    ],
    glossary=[
        GlossaryItem(name='EKS Auto Mode', definition='AWS\'s built-in Karpenter-style compute layer + core add-on bundle. AWS owns lifecycle.'),
        GlossaryItem(name='NodePool', definition='Karpenter / Auto Mode CRD: workload-facing (requirements, taints, disruption, expireAfter, limits).'),
        GlossaryItem(name='NodeClass', definition='Auto Mode CRD: AWS-specific config (subnets, SGs, IAM role, AMI).'),
        GlossaryItem(name='Consolidation', definition='Auto Mode behaviour: replace running nodes with fewer/cheaper ones when load allows. WhenUnderutilized vs WhenEmpty.'),
        GlossaryItem(name='expireAfter', definition='Max node lifetime. Default 720h (30 days). Forces AMI rotation.'),
        GlossaryItem(name='Disruption budget (NodePool)', definition='Per-NodePool cap on simultaneous voluntary disruptions.'),
        GlossaryItem(name='NodeClaim', definition='Karpenter / Auto Mode internal CRD representing an in-flight node provision request. Useful for debugging.'),
        GlossaryItem(name='Bottlerocket', definition='AWS\'s minimal, immutable, container-optimised OS. Auto Mode default.'),
        GlossaryItem(name='Karpenter (open-source)', definition='AWS\'s open-source provisioner. Auto Mode is the bundled, managed version.'),
        GlossaryItem(name='Built-in components (Auto Mode)', definition='VPC CNI, EBS CSI, AWS LB Controller, CoreDNS, kube-proxy, GPU plugins, health checkers — AWS bundles + upgrades.'),
        GlossaryItem(name='Managed Node Groups', definition='AWS-managed EC2 ASGs with predefined instance type. Static; you tune capacity.'),
        GlossaryItem(name='Auto Mode premium', definition='~12-15% per-vCPU-hour fee on top of EC2 cost. Trades for SRE time saved.'),
    ],
    recap_lead='Auto Mode = Karpenter-style compute + bundled add-ons, AWS-owned. NodePool + NodeClass declare your wants; AWS provisions, lifecycles, consolidates, replaces. Modern default for new clusters; trade some control for less ops.',
    recap_next='<strong>Next — E3: AWS Networking for EKS.</strong> VPC CNI internals, ENI exhaustion, AWS Load Balancer Controller, Gateway API via VPC Lattice, ExternalDNS, PrivateLink integration.',
)
