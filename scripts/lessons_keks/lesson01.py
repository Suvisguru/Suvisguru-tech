from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="EKS architecture: AWS-managed control plane in a fenced area, customer-managed nodes (managed NG / self-managed / Fargate / Auto Mode / Hybrid) in the tenant area, VPC + IAM around them.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">EKS · SHARED RESPONSIBILITY ARCHITECTURE</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <rect x="14" y="34" width="280" height="50" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="154" y="54" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">AWS-managed control plane</text>
    <text x="154" y="68" text-anchor="middle" font-size="8" fill="#FBF1D6" font-style="italic">apiserver · etcd · scheduler · controller-manager</text>
    <text x="154" y="80" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">multi-AZ · auto-patched · highly available</text>
    <rect x="306" y="34" width="280" height="50" rx="6" fill="#FBF1D6" stroke="#8B5A00" stroke-width="2"/>
    <text x="446" y="54" text-anchor="middle" font-size="10" font-weight="700" fill="#8B5A00">Your VPC · Your nodes</text>
    <text x="446" y="68" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">workloads · data · IAM · network · cost</text>
    <text x="446" y="80" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">5 node options below</text>
    <rect x="14" y="92" width="115" height="34" rx="3" fill="#5A9F7A"/><text x="71" y="108" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">managed NG</text><text x="71" y="120" text-anchor="middle" font-size="7" fill="#FBE8DC">EC2 lifecycle</text>
    <rect x="135" y="92" width="115" height="34" rx="3" fill="#A04832"/><text x="192" y="108" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">self-managed</text><text x="192" y="120" text-anchor="middle" font-size="7" fill="#FBE8DC">EC2 you operate</text>
    <rect x="256" y="92" width="115" height="34" rx="3" fill="#E8B547"/><text x="313" y="108" text-anchor="middle" font-size="8" fill="#5A4F45" font-weight="700">Fargate</text><text x="313" y="120" text-anchor="middle" font-size="7" fill="#5A4F45">serverless pods</text>
    <rect x="377" y="92" width="115" height="34" rx="3" fill="#3F4A5E"/><text x="434" y="108" text-anchor="middle" font-size="8" fill="#FBF1D6" font-weight="700">EKS Auto Mode</text><text x="434" y="120" text-anchor="middle" font-size="7" fill="#FBE8DC">AWS picks node</text>
    <rect x="498" y="92" width="88" height="34" rx="3" fill="#FBE8DC" stroke="#A04832" stroke-width="1"/><text x="542" y="108" text-anchor="middle" font-size="8" fill="#A04832" font-weight="700">Hybrid Nodes</text><text x="542" y="120" text-anchor="middle" font-size="7" fill="#5A4F45">on-prem</text>
    <rect x="14" y="134" width="572" height="22" rx="3" fill="#ECEFF5" stroke="#3F4A5E"/><text x="300" y="148" text-anchor="middle" font-size="8" fill="#3F4A5E" font-weight="700">VPC + IAM + KMS + ELB + CloudWatch + EBS/EFS — every K-EKS module sits inside these AWS surrounding services</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="01",
    title_short="EKS architecture",
    title_full="E1 · EKS Architecture and Shared Responsibility",
    title_html="K-EKS E1 · EKS Architecture",
    module_eyebrow="Module E1 · the AWS-managed control plane + your nodes",
    hero_sub_html='EKS = AWS runs the K8s control plane (apiserver, etcd, scheduler, controller-manager) across 3 AZs, auto-patched, highly available. <strong>You</strong> still own VPC + nodes + workloads + IAM + cost. Five node options: <strong>managed NG, self-managed, Fargate, EKS Auto Mode, EKS Hybrid Nodes</strong>.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Your team picks EKS thinking \"AWS handles everything.\" Six months in, an EKS minor goes EOL — your version is past <strong>standard support</strong> + 12 months into <strong>extended support</strong> at $0.60/hour premium per cluster ($5K/year extra). Plus your VPC CNI is on a deprecated version, no node group has a defined max-unavailable, and <code>aws-auth</code> ConfigMap is the only way anyone can authenticate. <em>EKS is shared responsibility, not magic responsibility.</em> This module is the map of who owns what.',
    stamp_html='EKS = AWS runs control plane (apiserver, etcd, scheduler, controller-manager) across 3 AZs. You run the rest: nodes (5 options), VPC, IAM, workloads, cost. <strong>Version policy</strong>: 14 months standard support + 12 months extended support per minor. Track AWS\'s EKS version lifecycle, not just upstream. Provision via Console / AWS CLI / eksctl / Terraform / EKS Blueprints / CDK / Pulumi / Crossplane.',
    district_pin="ks-floor01",
    district_label="Lobby & Floor Plan",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What EKS is and isn't",
            body_html="""    <p>EKS is Amazon\'s managed Kubernetes. AWS operates the control plane: 3 apiservers in 3 AZs behind an NLB, etcd cluster, scheduler, controller-manager, addon controllers — all running on AWS-owned infrastructure you never SSH into. AWS patches them, scales them, monitors them. You hit a single endpoint (<code>https://&lt;clusterID&gt;.gr7.us-east-1.eks.amazonaws.com</code>) and call it a cluster.</p>
    <p>What EKS is <em>not</em>: a runtime for your workloads (those run on nodes you provision). A network manager (you own the VPC + subnets + SGs). An identity store (you wire IAM ↔ K8s RBAC yourself). A cost-control system (you choose instances + autoscaling + spot). EKS is <em>K8s minus control-plane operations</em>. Everything else is yours.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Five node options",
            h2="Where your Pods actually run",
            body_html="""    <table class="data-table">
      <thead><tr><th>Option</th><th>What it is</th><th>When</th></tr></thead>
      <tbody>
        <tr><td><strong>Managed Node Groups</strong></td><td>EC2 ASGs AWS provisions + lifecycle-manages. You pick instance type + count + AMI. AWS handles drains + rolling updates on AMI/version refresh.</td><td>Default for most teams. Predictable, simple.</td></tr>
        <tr><td><strong>Self-managed nodes</strong></td><td>You bring your own ASG / EC2 + join to the cluster. Maximum control; maximum operational burden.</td><td>Custom AMIs (Bottlerocket variants, hardened images), niche kernel modules, regulated environments needing full ownership.</td></tr>
        <tr><td><strong>AWS Fargate</strong></td><td>Serverless Pods. No nodes; AWS schedules each Pod on its own micro-VM. Pay per Pod-second.</td><td>Bursty / event-driven; teams that don\'t want to think about nodes; small simple workloads.</td></tr>
        <tr><td><strong>EKS Auto Mode</strong></td><td>AWS picks the right EC2 instance per Pod, manages lifecycle + upgrades + consolidation. Like Karpenter built into the cluster.</td><td>Modern default for new clusters in 2026 (covered in detail in E2).</td></tr>
        <tr><td><strong>EKS Hybrid Nodes</strong></td><td>On-prem / edge nodes joining an EKS cluster. Useful for hybrid workloads.</td><td>Bursty cloud + steady on-prem; latency-sensitive workloads at the edge.</td></tr>
      </tbody>
    </table>
    <p style="margin-top:18px"><strong>You can mix node options in one cluster.</strong> Critical workloads on managed NG; bursty on Fargate; everything else on EKS Auto Mode is a common pattern in 2026.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Endpoint, network, version policy",
            h2="The five EKS-specific decisions you make once",
            body_html="""    <ul>
      <li><strong>EKS platform version:</strong> a minor K8s version + patch + AWS extensions. AWS releases new platform versions ~monthly. Track via <code>aws eks describe-cluster --query cluster.platformVersion</code>.</li>
      <li><strong>Cluster endpoint access</strong>: public, private, or hybrid (public + private). Production should use <strong>private</strong> (your VPC routes to the EKS endpoint via PrivateLink-like ENIs) for security; <strong>hybrid</strong> if you need <code>kubectl</code> from a corporate network without VPN.</li>
      <li><strong>Cluster security groups</strong>: AWS creates one for the control plane; nodes get a separate one. Worker SG allows 443 to control plane; control plane SG allows API traffic from worker subnets.</li>
      <li><strong>VPC + subnet design</strong>: at least 2 (preferably 3) AZs. Public subnets for ELBs; private subnets for nodes. Plan IP space — the AWS VPC CNI (E3) burns ENIs and secondary IPs aggressively.</li>
      <li><strong>Tagging</strong>: tag every EKS resource (cluster, nodegroup, EBS volumes, ENIs). Cost allocation, automation, compliance — all rely on tags.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.9 · Provisioning options + version lifecycle",
            h2="How clusters get created",
            body_html="""    <ul>
      <li><strong>AWS Console</strong> — quickest demo path. Production: never (no audit trail).</li>
      <li><strong>AWS CLI</strong> — <code>aws eks create-cluster</code>. Scriptable but verbose.</li>
      <li><strong>eksctl</strong> — Weaveworks-built, AWS-blessed. Single YAML defines cluster + nodegroups + addons. Standard for hands-on / labs.</li>
      <li><strong>Terraform / EKS Blueprints</strong> — for IaC shops. EKS Blueprints (community) provide opinionated, batteries-included Terraform modules. The 2026 production default for serious shops.</li>
      <li><strong>AWS CDK</strong> — for TypeScript/Python orgs. <code>aws-cdk-lib/aws-eks</code>.</li>
      <li><strong>Pulumi</strong> — multi-language, similar shape to CDK.</li>
      <li><strong>Crossplane</strong> — declarative AWS resources via K8s CRDs. \"K8s creates EKS clusters\" — useful for fleet management.</li>
    </ul>
    <p><strong>Version policy that matters in 2026:</strong> AWS gives 14 months of <strong>standard support</strong> per minor version (matching upstream K8s patch support window) + 12 additional months of <strong>extended support</strong> at $0.60/hour premium per cluster. After standard support ends, you pay extra OR upgrade. Plan upgrade cadence around AWS\'s lifecycle, not just upstream\'s.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The standard support timeline ≈ 14 months because AWS lags upstream by ~1-3 months on minor release availability + the upstream patch window is ~12 months. Always check <code>aws eks describe-cluster-versions</code> + the EKS docs for current dates.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='You have a high-traffic web tier (predictable load, sustained), a batch ML pipeline (bursty, hours-long), and admin tools (always-on, low resource). What\'s a good node-option mix?',
            options=[
                ('a) All Fargate', False),
                ('b) Web on managed NG (predictable, RIs/Savings Plan), batch on EKS Auto Mode (spot-friendly, scales on demand), admin on Fargate (no node mgmt for tiny workloads)', True),
                ('c) All managed NG; one ASG sized for peak', False),
            ],
            feedback='<strong>Answer: b.</strong> Mix node options to match workload shape. Predictable workloads → managed NG with reserved capacity. Bursty → Auto Mode (spot + consolidation). Tiny + simple → Fargate (no node ops). Don\'t pay for what you don\'t need.',
        ),
    },
    before_after_before='<p>Self-managed K8s on EC2: kubeadm, kube-vip, manual etcd backups, OS patching schedule, control-plane HA you operate, version upgrades you orchestrate. Plus all the AWS networking + IAM + storage. Two SREs full-time minimum.</p>',
    before_after_after='<p>EKS: AWS runs the control plane. You define cluster + node options + IAM + network in IaC. Half an SRE. Trade-off: $0.10/hour per cluster (~$876/year), $0.60/hour during extended support, plus you give up some kernel + control-plane tunability.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">EKS is right when AWS is your home + control-plane ops aren\'t your differentiator. K-VAN is right when you need that ownership.</p>',
    analogy_intro_html='<p>Welcome to K-Skyline — the AWS Region\'s premier managed-K8s tower. The lobby is bright; the floor plan is on the wall. The building manager (AWS) operates the elevators (apiserver), the central HVAC (etcd), the back office (scheduler + controller-manager). You rent units (clusters); you furnish them (workloads); you pay for the power you draw (instance hours, storage, traffic). The lobby map shows ten more floors (E2-E11) — each handles one piece of the tenancy: who delivers your packages (networking), who lets visitors in (identity), where your storage is (vault), how upgrades happen (renovation wing), and so on.</p>',
    translation_rows=[
        ('Tower lobby + floor plan', 'EKS architecture'),
        ('Building manager (AWS staff)', 'AWS-managed control plane'),
        ('The elevator banks', 'kube-apiserver behind an NLB'),
        ('Central HVAC humming below', 'etcd cluster'),
        ('Your rented unit', 'EKS cluster (you provision)'),
        ('How the unit\'s wired into the building', 'VPC + subnets + security groups'),
        ('Who staffs your unit', 'Node options: managed NG / self-managed / Fargate / Auto Mode / Hybrid'),
        ('Your monthly statement', 'Cluster $0.10/h + node + storage + traffic; +$0.60/h during extended support'),
    ],
    analogy_stops="The analogy stops here: real EKS isn\'t a single building — it\'s a regional service spanning 3+ AZs with cross-AZ replication. Tower metaphor undersells the multi-AZ nature.",
    eli5='AWS runs the brain of your Kubernetes cluster (the control plane). You bring the workers (the nodes) and decide how they look. Like renting a serviced apartment vs building your own house.',
    eli10="EKS = managed K8s control plane (apiserver/etcd/scheduler/controller-manager) running on AWS infra across 3 AZs, auto-patched, highly available. You bring nodes (5 options: managed NG / self-managed / Fargate / Auto Mode / Hybrid), VPC, IAM, workloads. Version policy: 14 months standard support + 12 months extended support per minor. Provision via Console / AWS CLI / eksctl / Terraform / CDK / Pulumi / Crossplane. EKS Blueprints is the modern Terraform-based default.",
    scenarios=[
        Scenario(name='A SaaS using EKS Auto Mode + Argo CD', body='Single multi-AZ cluster. Auto Mode handles every node decision. Argo CD pulls from git for workload manifests + add-ons. Two engineers part-time. ~$5K/month for 60 small workloads at scale; AWS handles control plane upgrades transparently.'),
        Scenario(name='A bank with private endpoint + managed NG', body='Cluster endpoint private only. <code>kubectl</code> reachable via internal Direct Connect from corporate network. Managed Node Groups with hardened Bottlerocket AMIs (Module E7). Version pinned 1 minor behind latest; quarterly upgrades. Compliance approved.'),
        Scenario(name='A startup using eksctl for fast iteration', body='Single YAML file per cluster (dev/staging/prod). <code>eksctl create cluster -f cluster-prod.yaml</code> spins up cluster + nodegroups + add-ons + IRSA in one command. Cluster creation: ~15 min. Migration to Terraform planned at scale.'),
        Scenario(name='A team using EKS Blueprints (Terraform)', body='Terraform module defines: VPC, EKS cluster, managed NG, Fargate profiles, IAM roles, IRSA roles, add-ons (CNI/CoreDNS/EBS CSI), Karpenter, ALB controller, ExternalDNS. New cluster = <code>terraform apply</code>. Production-grade defaults baked in.'),
    ],
    misconceptions=[
        Misconception(myth='\"EKS handles everything for me.\"', truth='EKS handles the control plane. You handle nodes, networking, IAM, workloads, cost, security posture, observability, upgrades of nodes/add-ons. The shared-responsibility line is sharp.'),
        Misconception(myth='\"Cluster endpoint should be public for kubectl convenience.\"', truth='Production should be private (or private + hybrid with strict allowlists). Public endpoint = the K8s API on the internet, protected only by IAM auth. One mis-scoped IAM grant + you\'re a target.'),
        Misconception(myth='\"Standard support is forever.\"', truth='~14 months per minor. After that, extended support kicks in at $0.60/hour premium. AWS will eventually deprecate. Track AWS\'s lifecycle, not just upstream\'s.'),
    ],
    flashcards=[
        Flashcard(front='What does AWS manage in EKS?', back='Control plane: kube-apiserver, etcd, scheduler, controller-manager, addon controllers. Across 3 AZs. Auto-patched. Highly available. Hidden infrastructure you never SSH into.'),
        Flashcard(front='Five EKS node options?', back='Managed Node Groups (EC2 ASG AWS lifecycle), Self-managed (your EC2), AWS Fargate (serverless Pods), EKS Auto Mode (AWS picks instances), EKS Hybrid Nodes (on-prem joining EKS).'),
        Flashcard(front='EKS version support window?', back='14 months standard support + 12 months extended support per minor. Extended is +$0.60/hour per cluster.'),
        Flashcard(front='Cluster endpoint access modes?', back='Public (internet-reachable), Private (VPC-only via PrivateLink-like ENIs), Hybrid (both). Production = private (or private + strict-CIDR public).'),
        Flashcard(front='What is EKS platform version?', back='AWS\'s versioning of the cluster: minor K8s + patch + AWS-specific addons + features. Released ~monthly. <code>aws eks describe-cluster --query cluster.platformVersion</code>.'),
        Flashcard(front='What\'s eksctl for?', back='AWS-blessed CLI (Weaveworks). Single YAML defines cluster + nodegroups + addons + IAM + IRSA. Standard for hands-on use.'),
        Flashcard(front='What are EKS Blueprints?', back='Terraform modules + reference architectures from AWS for production EKS. Batteries-included; opinionated. The 2026 IaC default for serious EKS shops.'),
        Flashcard(front='Crossplane for EKS?', back='Declarative AWS resources via K8s CRDs. A management cluster creates + reconciles EKS workload clusters via YAML. Useful for fleet management.'),
    ],
    quizzes=[
        Quiz(prompt='You\'re sizing a new EKS cluster for a small SaaS. ~10 microservices, modest traffic, dev team of 5. What architecture?', answer='<strong>Single cluster, multi-AZ.</strong> 3 AZs in a single region; private subnets for nodes, public for ELBs. <strong>Endpoint:</strong> private + hybrid with corporate IP allowlist (so <code>kubectl</code> works from offices). <strong>Nodes:</strong> EKS Auto Mode (no node ops for the tiny team) — or 1-2 small managed Node Groups if Auto Mode isn\'t available in your region yet. <strong>IaC:</strong> eksctl YAML to start; migrate to EKS Blueprints (Terraform) at scale. <strong>Add-ons:</strong> AWS LB Controller, ExternalDNS, EBS CSI, cert-manager via add-on or Helm. <strong>Cost ballpark:</strong> $0.10/h cluster + ~3 t3.medium nodes ($90/month) + EBS + ELB ~$30/month + traffic. ~$200/month for the platform; workload cost on top.'),
        Quiz(prompt='Your EKS cluster is on K8s 1.32. AWS bills you $0.10/hour. Six months later you see a charge of $0.70/hour. What happened?', answer='<strong>Standard support ended on K8s 1.32.</strong> AWS is now charging the $0.60/hour <strong>extended support</strong> premium on top of the $0.10/hour cluster fee. <strong>Two paths:</strong> (1) Upgrade to a supported minor (1.33+) — eliminates the premium. <strong>Recommended.</strong> (2) Keep paying extended support if you genuinely can\'t upgrade now (e.g., a deprecated CRD-using operator). Eventually AWS will fully deprecate the version even on extended support; you\'ll be forced upgrade. <strong>Lesson:</strong> track <code>aws eks describe-cluster-versions</code> output in CI; alert when standard support ends in &lt; 90 days. Don\'t learn this from a billing spike.'),
        Quiz(prompt='You\'re asked to choose between eksctl, EKS Blueprints (Terraform), Crossplane for production cluster provisioning. <strong>Click for the decision walk. ▼</strong>', cyoa=True, cyoa_tag='the decision walk', answer='<strong>Pick eksctl when:</strong> you\'re iterating on cluster shape, single team owns the cluster, you don\'t already have IaC tooling. Single YAML; fastest path; well-documented; AWS-supported. <strong>Pick EKS Blueprints (Terraform) when:</strong> you\'re a multi-team org with existing Terraform investment, you\'ll operate ≥ 3 clusters, you want production defaults baked in (Karpenter + ALB + IRSA + add-ons all pre-configured). Most production shops in 2026 land here. <strong>Pick Crossplane when:</strong> you\'re building a platform team that operates many clusters, you want to declare clusters as K8s YAML (so the same GitOps flow that manages workloads also manages clusters), you have a management cluster running. <strong>Decision tree:</strong> &lt;3 clusters → eksctl. ≥ 3 clusters + Terraform shop → Blueprints. Many clusters + platform team → Crossplane. <strong>Common starting pattern:</strong> eksctl in dev to learn; promote to Blueprints for staging/prod. Cluster API on EKS (CAPA + EKS provider) is another emerging path — similar to Crossplane but K8s-SIG-native.'),
    ],
    glossary=[
        GlossaryItem(name='EKS', definition='Amazon Elastic Kubernetes Service. Managed K8s control plane on AWS.'),
        GlossaryItem(name='EKS platform version', definition='AWS-versioned K8s+patch+addons combo. ~monthly releases.'),
        GlossaryItem(name='Managed Node Groups', definition='EC2 ASGs AWS provisions + lifecycle-manages on your behalf. Default node option.'),
        GlossaryItem(name='Self-managed nodes', definition='EC2 you provision + join to the EKS cluster yourself. Maximum control.'),
        GlossaryItem(name='AWS Fargate (for EKS)', definition='Serverless Pods. AWS schedules each on a micro-VM; no nodes to manage. Pay per Pod-second.'),
        GlossaryItem(name='EKS Auto Mode', definition='AWS picks the right EC2 per Pod, manages lifecycle + upgrades + consolidation. Modern default.'),
        GlossaryItem(name='EKS Hybrid Nodes', definition='On-prem / edge nodes joining an EKS cluster. Hybrid workloads.'),
        GlossaryItem(name='Standard support (EKS)', definition='14 months of regular pricing per minor. After that, extended support kicks in.'),
        GlossaryItem(name='Extended support (EKS)', definition='Additional 12 months at +$0.60/hour per cluster. Buys time to upgrade.'),
        GlossaryItem(name='Cluster endpoint access', definition='Public, private, or hybrid. Production = private or hybrid.'),
        GlossaryItem(name='eksctl', definition='AWS-blessed CLI for EKS provisioning. Single YAML defines cluster + nodegroups + addons.'),
        GlossaryItem(name='EKS Blueprints', definition='AWS reference Terraform modules for production EKS. Opinionated, batteries-included.'),
        GlossaryItem(name='Crossplane', definition='Declarative AWS resources via K8s CRDs. Used for fleet management.'),
    ],
    recap_lead='EKS = AWS-managed control plane + your-managed nodes/network/IAM/workloads. Five node options. 14+12 months version support. Provision via eksctl (start) → Terraform/Blueprints (scale) → Crossplane (fleet).',
    recap_next='<strong>Next — E2: EKS Auto Mode.</strong> Modern default for new clusters. AWS picks EC2 + handles lifecycle + consolidation. Like Karpenter built into the cluster.',
)
