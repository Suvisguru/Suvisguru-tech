from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="VPC: 3 AZs with public + private subnets, ENIs from VPC CNI assigning Pod IPs, ALB at the edge, ExternalDNS to Route 53.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">AWS NETWORKING FOR EKS · VPC + CNI + LB</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">VPC · 3 AZs · public/private subnets</text>
    <rect x="14" y="34" width="186" height="100" rx="4" fill="#E0EEF3" stroke="#4A8FA8"/>
    <text x="107" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">us-east-1a</text>
    <rect x="22" y="58" width="68" height="20" rx="2" fill="#3F4A5E"/><text x="56" y="71" text-anchor="middle" font-size="7" fill="#FBF1D6">public</text>
    <rect x="22" y="84" width="68" height="20" rx="2" fill="#5A9F7A"/><text x="56" y="97" text-anchor="middle" font-size="7" fill="#FFFFFF">private</text>
    <rect x="22" y="110" width="170" height="18" rx="2" fill="#A04832"/><text x="107" y="123" text-anchor="middle" font-size="7" fill="#FBE8DC">VPC CNI: ENIs + IPs</text>
    <rect x="206" y="34" width="186" height="100" rx="4" fill="#E0EFE6" stroke="#5A9F7A"/>
    <text x="299" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">us-east-1b</text>
    <rect x="214" y="58" width="68" height="20" rx="2" fill="#3F4A5E"/><text x="248" y="71" text-anchor="middle" font-size="7" fill="#FBF1D6">public</text>
    <rect x="214" y="84" width="68" height="20" rx="2" fill="#5A9F7A"/><text x="248" y="97" text-anchor="middle" font-size="7" fill="#FFFFFF">private</text>
    <rect x="214" y="110" width="170" height="18" rx="2" fill="#A04832"/><text x="299" y="123" text-anchor="middle" font-size="7" fill="#FBE8DC">VPC CNI: ENIs + IPs</text>
    <rect x="398" y="34" width="186" height="100" rx="4" fill="#FBF1D6" stroke="#8B5A00"/>
    <text x="491" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">us-east-1c</text>
    <rect x="406" y="58" width="68" height="20" rx="2" fill="#3F4A5E"/><text x="440" y="71" text-anchor="middle" font-size="7" fill="#FBF1D6">public</text>
    <rect x="406" y="84" width="68" height="20" rx="2" fill="#5A9F7A"/><text x="440" y="97" text-anchor="middle" font-size="7" fill="#FFFFFF">private</text>
    <rect x="406" y="110" width="170" height="18" rx="2" fill="#A04832"/><text x="491" y="123" text-anchor="middle" font-size="7" fill="#FBE8DC">VPC CNI: ENIs + IPs</text>
    <rect x="14" y="138" width="572" height="18" rx="3" fill="#3F4A5E"/><text x="300" y="151" text-anchor="middle" font-size="8" fill="#FBF1D6">ALB Ingress · NLB Service · ExternalDNS → Route 53 · Gateway API → VPC Lattice</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="03",
    title_short="AWS networking",
    title_full="E3 · AWS Networking for EKS (VPC CNI, ALB/NLB, Gateway API, VPC Lattice)",
    title_html="K-EKS E3 · AWS Networking",
    module_eyebrow="Module E3 · the communication tower",
    hero_sub_html='EKS networking is AWS networking. <strong>AWS VPC CNI</strong> gives Pods real VPC IPs (no overlay) — fast, but burns IPs. <strong>AWS Load Balancer Controller</strong> turns Ingress/Service into ALB/NLB. <strong>VPC Lattice + Gateway API</strong> for service-to-service across VPCs/accounts. <strong>ExternalDNS</strong> for Route 53. <strong>PrivateLink</strong> + <strong>Transit Gateway</strong> for cross-account/region.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Production cluster runs out of Pod IPs at noon during a traffic spike. Investigation: VPC CNI was using one secondary IP per Pod; instance type only supports 18 IPs. New Pods stuck Pending: <code>0/15 nodes available: 15 had no Pod IPs available</code>. Recovery: enable prefix delegation (16x more IPs per ENI), restart aws-node DaemonSet. <em>The default VPC CNI mode is wrong for any meaningful cluster — you fix it before launch or you fix it during the outage.</em>',
    stamp_html='AWS VPC CNI gives Pods real VPC IPs via secondary ENIs/IPs. <strong>Enable prefix delegation</strong> (16x more IPs per ENI) — this is non-negotiable for serious clusters. <strong>AWS LB Controller</strong> creates ALBs from Ingress/HTTPRoute, NLBs from Services. <strong>VPC Lattice + AWS Gateway API Controller</strong> for cross-VPC service-to-service. <strong>ExternalDNS</strong> for Route 53. <strong>SG-for-pods</strong> for per-Pod security groups. <strong>Cilium / Calico / AWS Cilium dataplane</strong> as alternatives.',
    district_pin="ks-floor03",
    district_label="Communication Tower",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="VPC CNI — IP exhaustion is the default",
            body_html="""    <p>AWS VPC CNI gives every Pod a real IP from your VPC subnet. No VXLAN, no overlay — Pods are first-class VPC citizens. Pod-to-Pod traffic stays in VPC routing; Pod-to-AWS-service traffic uses VPC endpoints; SG-for-pods works on real ENIs.</p>
    <p>The cost: every Pod consumes a real VPC IP. Each EC2 instance type supports a fixed number of <strong>ENIs</strong> + <strong>IPs per ENI</strong>. A <code>t3.medium</code> supports 3 ENIs × 6 IPs = 18 IPs. A <code>m5.large</code> = 3 × 10 = 30. <em>That\'s your Pod limit per node</em>.</p>
    <p><strong>Prefix delegation</strong> (default-disabled, but you should enable it): the CNI gets <code>/28</code> prefixes (16 IPs each) per ENI instead of single IPs. Same 3 ENIs now hold 48 IPs. <strong>Enable this on every cluster.</strong></p>""",
        ),
        Section(
            eyebrow="Section 1.5 · CNI options + IP-exhaustion mitigations",
            h2="VPC CNI variants + alternatives",
            body_html="""    <ul>
      <li><strong>AWS VPC CNI (default)</strong> — Pods get VPC IPs. Enable prefix delegation. Use <strong>custom networking</strong> if your VPC is small + you need separate Pod subnets (often a /16 just for Pods).</li>
      <li><strong>SG-for-pods</strong> — assign SecurityGroups to specific Pods (not just nodes). Useful for fine-grained AWS-service ACLs (e.g., \"only Pods with this SG can hit the RDS\").</li>
      <li><strong>IPv6 / dual-stack</strong> — every Pod gets an IPv6 (unlimited), eliminating IP exhaustion entirely. Some workloads fully on IPv6.</li>
      <li><strong>Cilium on EKS</strong> — replace VPC CNI with Cilium. eBPF data plane, kube-proxy replacement, Hubble, FQDN policies. Trades VPC integration for Cilium features.</li>
      <li><strong>Calico on EKS</strong> — overlay or BGP. Mature; FIPS variants.</li>
      <li><strong>AWS Cilium dataplane</strong> — newer hybrid: AWS-supported Cilium with VPC CNI integration. Best of both.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.7 · Load balancers + Gateway",
            h2="AWS LB Controller + Gateway API + VPC Lattice",
            body_html="""    <p><strong>AWS Load Balancer Controller</strong> watches K8s objects + provisions AWS LBs:</p>
    <ul>
      <li><strong>Ingress</strong> with <code>kubernetes.io/ingress.class: alb</code> → ALB (L7 routing, TLS termination, WAF integration).</li>
      <li><strong>Service type=LoadBalancer</strong> with <code>service.beta.kubernetes.io/aws-load-balancer-type: external</code> → NLB (L4, low latency, static IP, EIP).</li>
      <li><strong>Target type</strong>: <code>ip</code> (LB sends to Pod IPs directly — modern default; needs VPC CNI or Cilium with VPC routing) or <code>instance</code> (LB sends to node, kube-proxy redirects — legacy).</li>
      <li>Annotations control: scheme (internal/internet-facing), subnets, SSL cert, WAF, access logs, and ~50 more.</li>
    </ul>
    <p><strong>AWS Gateway API Controller for VPC Lattice</strong> (released GA 2024): implements Gateway API for cross-VPC / cross-account service-to-service. Each VPC Lattice service group spans VPCs + accounts; service mesh-like without sidecars. New clusters in 2026 increasingly use this for multi-account architectures.</p>
    <p><strong>ExternalDNS</strong>: K8s controller that watches Ingresses + Services + HTTPRoutes with hostname annotations + creates Route 53 records. Use private hosted zones for internal services.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Beyond the cluster — VPC integration",
            h2="PrivateLink, TGW, EFA",
            body_html="""    <ul>
      <li><strong>VPC Endpoints</strong>: Pods reach AWS services (ECR, S3, KMS, STS) without going to the internet. Required for private clusters.</li>
      <li><strong>PrivateLink</strong>: expose your service via an interface VPC endpoint to other accounts. EKS itself uses PrivateLink for the private endpoint.</li>
      <li><strong>Transit Gateway</strong>: hub-and-spoke connectivity between many VPCs. Pod traffic between VPCs routes via TGW.</li>
      <li><strong>EFA (Elastic Fabric Adapter)</strong>: high-speed network for HPC/AI training. Pods running ML training across multiple nodes use EFA for low-latency, low-jitter all-to-all communication. Requires specific instance types (P4d/P5, etc.) + EFA device plugin.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>EFA + Kubernetes is a niche but high-value combo: distributed PyTorch / NCCL training scales near-linearly to 100s of GPUs over EFA. Without EFA, the network becomes the bottleneck at ~16 GPUs.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question='You launch an EKS cluster on m5.large nodes. Each node hits ~25 Pods, then new Pods stay Pending with \"no IPs available.\" What\'s wrong + the fastest fix?',
            options=[
                ('a) Add more nodes', False),
                ('b) Enable prefix delegation on the VPC CNI (one config change → 5x more IPs per node, no node replacement needed)', True),
                ('c) Switch to Cilium', False),
            ],
            feedback='<strong>Answer: b.</strong> m5.large default IP limit ≈ 30 IPs/node. Prefix delegation bumps to ~110+. <code>kubectl set env -n kube-system ds/aws-node ENABLE_PREFIX_DELEGATION=true</code> + restart. New Pods provision IPs from <code>/28</code> prefixes. Don\'t add more nodes for an IP shortage problem.',
        ),
    },
    before_after_before='<p>Default VPC CNI; IP exhaustion at 30 Pods/node. ALBs created by hand via console + DNS records typed into Route 53 by an SRE. Cross-VPC traffic via VPC peering + complex SGs. \"Why is the LB stuck pending\" answered with shrugs.</p>',
    before_after_after='<p>VPC CNI with prefix delegation; 4-5x more Pods per node. AWS LB Controller turns Ingress YAML into ALB. ExternalDNS handles Route 53. Cross-VPC via VPC Lattice + Gateway API. Cluster networking is YAML.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">EKS networking is the place new shops trip on AWS-specific gotchas first. Prefix delegation + AWS LB Controller + ExternalDNS are the three you must get right at launch.</p>',
    analogy_intro_html='<p>The Communication Tower stands tall above the K-Skyline. The building manager (AWS) operates the central exchange (VPC); the building\'s wiring (subnets) reaches every floor across three wings (AZs). Each tenant unit (Pod) has its own phone number on the building\'s public exchange (real VPC IPs via VPC CNI). The doorman (ALB / NLB) routes incoming visitors to the right unit. The address book (ExternalDNS → Route 53) keeps everything findable. And for tenants in different sister buildings (VPCs / accounts), the inter-building shuttle (VPC Lattice) lets them call each other directly.</p>',
    translation_rows=[
        ('Building\'s central exchange', 'VPC + subnets'),
        ('Each unit\'s phone number from the building\'s book', 'Pod IP from VPC subnet (VPC CNI)'),
        ('Limit on how many phones per floor', 'ENIs × IPs per instance type'),
        ('Bulk-line phone bundle (more numbers per cable)', 'Prefix delegation (/28 per ENI)'),
        ('Doorman accepting visitors', 'ALB / NLB via AWS LB Controller'),
        ('Building address book', 'Route 53 via ExternalDNS'),
        ('Inter-building shuttle', 'VPC Lattice + AWS Gateway API Controller'),
        ('Per-unit call screening', 'SG-for-pods'),
        ('Express line to the data centre across town', 'EFA for HPC/AI'),
    ],
    analogy_stops="The analogy stops here: VPC CNI is software running on each node, hooking into Linux networking namespaces. Real packet flow involves ENI attachments, ip-rule policies, and route table lookups — much more involved than \"phone numbers.\"",
    eli5='Every Pod gets a real address in the building. The doorman (ALB) sends visitors to the right Pod. The address book (Route 53) keeps everyone\'s number current.',
    eli10="AWS VPC CNI gives Pods real VPC IPs (no overlay). Enable prefix delegation = 16x more IPs/ENI. AWS Load Balancer Controller turns Ingress → ALB, Service type=LB → NLB; target type IP for Pod-direct routing. AWS Gateway API Controller implements Gateway API via VPC Lattice for cross-VPC services. ExternalDNS syncs to Route 53. SG-for-pods for per-Pod SGs. Alternatives: Cilium on EKS, Calico, AWS Cilium dataplane.",
    scenarios=[
        Scenario(name='A SaaS hitting IP exhaustion at scale', body='Default VPC CNI; cluster grew from 50 to 500 Pods; nodes saturated at IP limits well before CPU/mem. Fix: enabled prefix delegation cluster-wide, no node replacement needed; per-node Pod density jumped 4x. Saved ~$8K/month on right-sizing nodes.'),
        Scenario(name='A bank using AWS LB Controller for ALB Ingress', body='Single ALB serves 40 hostnames via host-based routing rules; cert-manager populates ACM certs; ExternalDNS creates internal Route 53 records. Adding a new service is a YAML PR. Cost: ~$25/month for the LB; ~$0 for cert + DNS.'),
        Scenario(name='A multi-account team using VPC Lattice', body='4 AWS accounts, 6 VPCs, dozens of services. Pre-Lattice: cross-account SG sprawl + custom service discovery + VPC peering complexity. Lattice: each service registered once; consumed by HTTPRoute from any account. Cross-account traffic just works.'),
        Scenario(name='An ML team running PyTorch on EFA', body='32 P5 nodes, EFA enabled, NCCL configured. PyTorch DDP scales 32 GPUs at 92% efficiency; without EFA, was 65%. The EFA setup is non-trivial (instance types + driver + plugin) but pays off massively for distributed training.'),
    ],
    misconceptions=[
        Misconception(myth='\"Default VPC CNI is fine.\"', truth='Default = single secondary IPs per ENI = severe Pod density limits on most instance types. Enable prefix delegation on every cluster at launch. Or use Cilium / dual-stack / IPv6.'),
        Misconception(myth='\"ALB target type instance is the safer default.\"', truth='Target type <code>ip</code> is the modern default — LB sends directly to Pod IPs (skipping kube-proxy + the per-node hop). Faster, more accurate health checks. <code>instance</code> is legacy.'),
        Misconception(myth='\"VPC Lattice replaces a service mesh.\"', truth='Lattice is AWS\'s opinionated cross-VPC service-to-service. It overlaps with mesh features but doesn\'t replace mesh entirely (no sidecar mTLS within a single cluster, fewer L7 features). Often paired with Cilium / Linkerd inside the cluster + Lattice across.'),
    ],
    flashcards=[
        Flashcard(front='How does AWS VPC CNI assign Pod IPs?', back='Pods get real IPs from VPC subnets. CNI manages secondary IPs on ENIs attached to each node. Default: 1 IP per slot. With prefix delegation: 16 IPs per slot.'),
        Flashcard(front='Why prefix delegation?', back='Default VPC CNI hits IP exhaustion at 30-60 Pods/node depending on instance type. Prefix delegation gives /28 (16 IPs) per slot, 4-5x density. Enable on every cluster.'),
        Flashcard(front='AWS LB Controller — what does it create?', back='From Ingress: ALB (L7 routing, TLS, WAF). From Service type=LoadBalancer: NLB (L4, low latency, static IP). From HTTPRoute (Gateway API): ALB. Annotations control behavior.'),
        Flashcard(front='Target type ip vs instance?', back='ip: ALB/NLB sends directly to Pod IP (modern default; needs VPC CNI). instance: sends to node, kube-proxy hops to Pod (legacy; one extra hop, less accurate health checks).'),
        Flashcard(front='What is VPC Lattice?', back='AWS service for cross-VPC / cross-account service-to-service connectivity + access control. Implements Gateway API via the AWS Gateway API Controller. Service-mesh-adjacent without sidecars.'),
        Flashcard(front='SG-for-pods?', back='Assign SecurityGroups to specific Pods (not just nodes). Enables fine-grained AWS-service ACLs (e.g., \"only Pods with SG-X can reach RDS\"). Configured via <code>SecurityGroupPolicy</code> CRD.'),
        Flashcard(front='ExternalDNS for EKS?', back='K8s controller. Watches Ingresses + Services + HTTPRoutes with hostname annotations; syncs to Route 53 (public + private hosted zones).'),
        Flashcard(front='When to use Cilium on EKS?', back='When you want eBPF data plane + Hubble + kube-proxy replacement + FQDN policies. Trades VPC IP integration for Cilium\'s feature set. AWS Cilium dataplane is the hybrid newer offering.'),
    ],
    quizzes=[
        Quiz(prompt='You\'re launching a new EKS cluster on c6i.large nodes. The team plans for ~50 Pods/node. Default VPC CNI. What\'s the IP-density check + fix?', answer='<strong>c6i.large</strong> default = 3 ENIs × 9 IPs = 27 IPs per node. 50 Pods/node won\'t fit. <strong>Two fixes:</strong> (1) <strong>Enable prefix delegation</strong> on the VPC CNI: <code>kubectl set env -n kube-system ds/aws-node ENABLE_PREFIX_DELEGATION=true</code> + restart. Now each ENI gets <code>/28</code> = 16 IPs; 3 ENIs × 16 = 48 IPs (still tight at 50 — bump instance to c6i.xlarge or use IPv6). (2) <strong>Custom networking</strong>: dedicate a separate VPC subnet for Pods (different CIDR), removes the node-subnet IP contention. <strong>Always test density at launch</strong>; learning about IP exhaustion in production is too late.'),
        Quiz(prompt='Your team\'s Ingress shows <code>FailedDeployModel</code> with \"unable to find any subnet with required tag.\" Diagnose.', answer='AWS LB Controller discovers subnets by tag: <code>kubernetes.io/role/elb</code> for internet-facing ALBs and <code>kubernetes.io/role/internal-elb</code> for internal. <strong>Fix:</strong> tag at least 2 subnets in different AZs with the appropriate value. <code>aws ec2 create-tags --resources subnet-xxx --tags Key=kubernetes.io/role/elb,Value=1</code>. Also: tag with <code>kubernetes.io/cluster/&lt;cluster-name&gt;: owned</code> (or <code>shared</code> if other clusters share). After tagging: <code>kubectl rollout restart -n kube-system deployment aws-load-balancer-controller</code>. New Ingress create should provision an ALB within minutes.'),
        Quiz(prompt='You\'re asked to design networking for a 4-account, 6-VPC EKS multi-cluster architecture. <strong>Click for the playbook. ▼</strong>', cyoa=True, cyoa_tag='the playbook', answer='<strong>(1) Per-VPC EKS clusters.</strong> Each account/VPC has its own EKS cluster. Avoid the single-cluster-many-VPCs path (complex CNI + ENI mgmt). <strong>(2) VPC Lattice for cross-VPC services.</strong> Each cluster registers services into VPC Lattice; consumers from other clusters reference via Gateway API HTTPRoutes pointing at Lattice services. AWS handles cross-account routing + IAM-based authz. <strong>(3) Per-cluster Cilium</strong> (or Cilium dataplane) for in-cluster mTLS + L7 + observability (Hubble). Cilium\'s identity model integrates with Lattice authz at the boundary. <strong>(4) ExternalDNS</strong> per cluster, scoped to per-cluster zones. <strong>(5) Resource Access Manager (RAM)</strong> for sharing VPC Lattice service networks across accounts. <strong>(6) Transit Gateway</strong> for non-Lattice traffic (private DBs, on-prem, partners). <strong>(7) Pod Identity (E4) per cluster</strong> for AWS-service access; cross-account roles via STS AssumeRole. <strong>Result:</strong> each cluster autonomous, networking cleanly composable, identity flows through Lattice + IAM. Far simpler than peered-VPC + custom mesh sprawl.'),
    ],
    glossary=[
        GlossaryItem(name='AWS VPC CNI', definition='Default EKS CNI. Pods get real IPs from VPC subnets via secondary ENIs/IPs.'),
        GlossaryItem(name='Prefix delegation', definition='VPC CNI mode: <code>/28</code> (16 IPs) per ENI slot instead of one. Enable on every cluster.'),
        GlossaryItem(name='ENI (Elastic Network Interface)', definition='Virtual NIC attached to an EC2 instance. EKS Pods consume secondary IPs from these.'),
        GlossaryItem(name='Custom networking (VPC CNI)', definition='Pods get IPs from a separate subnet (not the node subnet). Separates Pod IP space from node IP space.'),
        GlossaryItem(name='SG-for-pods', definition='SecurityGroupPolicy CRD; assigns SGs to specific Pods. Per-Pod AWS-service ACLs.'),
        GlossaryItem(name='AWS Load Balancer Controller', definition='K8s controller; provisions ALB (from Ingress / HTTPRoute) and NLB (from Service type=LoadBalancer).'),
        GlossaryItem(name='Target type (ALB/NLB)', definition='ip = direct to Pod IPs (modern). instance = to node + kube-proxy hop (legacy).'),
        GlossaryItem(name='AWS Gateway API Controller', definition='K8s controller; implements Gateway API via VPC Lattice. Cross-VPC + cross-account service-to-service.'),
        GlossaryItem(name='VPC Lattice', definition='AWS service for cross-VPC / cross-account service connectivity + IAM-based authz. Mesh-adjacent without sidecars.'),
        GlossaryItem(name='ExternalDNS', definition='Watches K8s objects with hostname annotations + syncs Route 53 records (public + private zones).'),
        GlossaryItem(name='PrivateLink', definition='AWS service for exposing services across accounts via interface VPC endpoints.'),
        GlossaryItem(name='Transit Gateway', definition='AWS hub-and-spoke router connecting many VPCs + on-prem.'),
        GlossaryItem(name='EFA', definition='Elastic Fabric Adapter. High-speed network for HPC / AI distributed training. Specific instance types only.'),
    ],
    recap_lead='VPC CNI = real Pod IPs (enable prefix delegation). AWS LB Controller = ALB/NLB from K8s YAML. Gateway API + VPC Lattice = cross-VPC/account services. ExternalDNS for Route 53. SG-for-pods for fine-grained AWS ACLs.',
    recap_next='<strong>Next — E4: Identity and Access (EKS-Specific).</strong> IAM access entries, IRSA, Pod Identity. The two-axis identity model (AWS IAM + K8s RBAC).',
)
