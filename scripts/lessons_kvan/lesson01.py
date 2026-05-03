from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drafting hut: a survey table with cluster blueprint, including 3 control plane stones, 3 worker stones, an LB tower, etcd well, and a backup chest off to the side.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">DRAFTING HUT · CLUSTER BLUEPRINT</text>
  <!-- Blueprint paper -->
  <g transform="translate(40,40)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#3F4A5E" stroke-width="1.5"/>
    <text x="300" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="#3F4A5E">HA on-prem cluster · 6 nodes</text>
    <!-- API LB -->
    <rect x="20" y="40" width="100" height="34" rx="4" fill="#A04832"/><text x="70" y="58" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">API LB · :6443</text><text x="70" y="69" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">kube-vip / HAProxy</text>
    <!-- Control plane nodes -->
    <rect x="160" y="40" width="80" height="34" rx="4" fill="#3F4A5E"/><text x="200" y="58" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">cp-1</text><text x="200" y="69" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">apiserver/sched/cm</text>
    <rect x="250" y="40" width="80" height="34" rx="4" fill="#3F4A5E"/><text x="290" y="58" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">cp-2</text>
    <rect x="340" y="40" width="80" height="34" rx="4" fill="#3F4A5E"/><text x="380" y="58" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">cp-3</text>
    <!-- etcd quorum -->
    <rect x="430" y="40" width="80" height="34" rx="4" fill="#5A4F45"/><text x="470" y="58" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">etcd ×3</text><text x="470" y="69" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">stacked</text>
    <!-- Worker nodes -->
    <rect x="20" y="86" width="80" height="34" rx="4" fill="#5A9F7A"/><text x="60" y="104" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">worker-1</text>
    <rect x="110" y="86" width="80" height="34" rx="4" fill="#5A9F7A"/><text x="150" y="104" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">worker-2</text>
    <rect x="200" y="86" width="80" height="34" rx="4" fill="#5A9F7A"/><text x="240" y="104" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">worker-3</text>
    <!-- Storage / backup -->
    <rect x="300" y="86" width="100" height="34" rx="4" fill="#E8B547"/><text x="350" y="104" text-anchor="middle" font-size="9" fill="#5A4F45" font-weight="700">CSI · Longhorn</text>
    <rect x="410" y="86" width="100" height="34" rx="4" fill="#FBE8DC" stroke="#A04832" stroke-width="1.5"/><text x="460" y="104" text-anchor="middle" font-size="9" fill="#A04832" font-weight="700">Velero · backup</text>
    <!-- Network / pod CIDR plan -->
    <rect x="20" y="130" width="490" height="22" rx="3" fill="#E0EEF3" stroke="#4A8FA8"/><text x="265" y="145" text-anchor="middle" font-size="8" fill="#3F4A5E" font-weight="700">Pod CIDR 10.244.0.0/16 · Service CIDR 10.96.0.0/12 · CNI Cilium · Gateway API</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="01",
    title_short="architecture design",
    title_full="V1 · Production Architecture Design for Self-Managed K8s",
    title_html="K-VAN V1 · Production Architecture Design",
    module_eyebrow="Module V1 · self-managed K8s starts before any kubeadm command",
    hero_sub_html='Before you install anything, you draw the cluster on paper. Sizes, topology, network plan, certificate plan, backup plan, upgrade plan. <strong>Every later decision references this drawing.</strong>',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Six months in, you realise the Pod CIDR you chose conflicts with your corporate VPN range. Or that you put etcd on the same disks as the kubelet, and now disk-fsync latency is killing the cluster. Or that you have only 2 control-plane nodes (no quorum). Every one of these is fixable with effort — and 100% preventable by spending a day on the architecture before the install. This module is that day.',
    stamp_html='Production self-managed K8s starts as a <strong>blueprint</strong>: control-plane sizing, worker sizing, etcd sizing, API LB, Pod/Service CIDR, CNI, CSI, OS choice, runtime, HA topology (stacked vs external etcd), backup, upgrade, security baseline. Get the blueprint right; everything downstream is mechanical.',
    district_pin="kf-site01",
    district_label="Drafting Hut",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why the architecture phase exists",
            body_html="""    <p>Managed K8s (EKS / GKE / AKS) hides 80% of the architecture decisions behind a console — the cloud picks the topology, the networking, the upgrade strategy. Self-managed K8s gives you all of those decisions. <em>You are the cloud now</em>. That power is liberating until day 90, when a wrong choice in week 1 forces a cluster rebuild.</p>
    <p>Architecture is the document that turns \"we want a Kubernetes cluster\" into <em>this many CPUs, on these subnets, with these CIDRs, this CNI, this etcd topology, with these backup intervals</em>. It also says what you are <em>not</em> trying to optimise (cost? availability? latency?). Without that explicit list, every later argument is unresolvable.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Sizing — control plane / worker / etcd",
            h2="Three sizing axes",
            body_html="""    <table class="data-table">
      <thead><tr><th>Component</th><th>Drives sizing</th><th>Floor for production</th></tr></thead>
      <tbody>
        <tr><td>Control plane</td><td>Number of nodes, Pods, Services, watch load</td><td>3 nodes (HA quorum) · 4 vCPU / 8 GiB each for ≤ 250 nodes; 8/16 for ≤ 500</td></tr>
        <tr><td>Worker</td><td>Workloads + room to evict</td><td>Mix of sizes; reserve 20% headroom for spikes + rolling updates</td></tr>
        <tr><td>etcd</td><td>Object count, write rate, snapshot size</td><td>3 members minimum · NVMe SSD · 8 GiB+ RAM · 4 vCPU+ · &lt; 10ms p99 fsync</td></tr>
      </tbody>
    </table>
    <p style="margin-top:18px"><strong>Stacked vs external etcd.</strong> Stacked = etcd runs on the same nodes as kube-apiserver. Simpler bootstrap; one less tier to operate. External = etcd on its own nodes. More resilient (apiserver crash doesn\'t affect etcd), more flexible scaling, more ops surface. <em>For a small org, stacked is fine. For 500+ node clusters, external.</em></p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Network plan",
            h2="CIDRs, DNS, and the LB",
            body_html="""    <p>You pick five things, and once they're in production they're hard to change without a cluster rebuild:</p>
    <ul>
      <li><strong>Pod CIDR</strong> — the IP space Pods come from. Default <code>10.244.0.0/16</code>. Must NOT overlap with any network reachable from the cluster (corporate VPN, peered VPCs, on-prem subnets). 65K IPs, divided per node.</li>
      <li><strong>Service CIDR</strong> — virtual IPs for Services. Default <code>10.96.0.0/12</code>. ~1M IPs. Must NOT overlap with Pod CIDR or any reachable network.</li>
      <li><strong>Cluster DNS</strong> — IP within the Service CIDR (typically <code>10.96.0.10</code>) where CoreDNS lives. Hard-coded into <code>/etc/resolv.conf</code> for every Pod.</li>
      <li><strong>Dual-stack / IPv6</strong> — opt-in at install time. Once on, you can\'t un-stack without rebuild. If you\'re running out of IPv4 (cluster of clusters, IP scarcity), plan for v6 or dual-stack from day 1.</li>
      <li><strong>API server LB</strong> — clients always hit <code>https://&lt;LB&gt;:6443</code>. Options: kube-vip (built into your kubeadm bootstrap), HAProxy + keepalived (classic), MetalLB (for L2/BGP), an external hardware LB. The LB IP is part of the API server\'s certificate SANs.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.9 · The other six choices",
            h2="OS, runtime, CNI, CSI, ingress, backup",
            body_html="""    <ul>
      <li><strong>OS</strong> — Ubuntu LTS (most-tested), Debian, Rocky/Alma (RHEL-compatible), Flatcar (immutable), <strong>Talos Linux</strong> (no SSH, API-driven, immutable; modern choice for 2026).</li>
      <li><strong>Runtime</strong> — <strong>containerd 2.x</strong> (the default). CRI-O is the alternative. Docker shim is dead.</li>
      <li><strong>CNI</strong> — Cilium (eBPF, modern default), Calico (BGP, mature), Antrea, Flannel (simple labs), kube-router, OVN-Kubernetes. <em>Lesson V4.</em></li>
      <li><strong>CSI</strong> — Longhorn (cloud-native block, on-prem), Rook-Ceph, OpenEBS, vSphere CSI, your storage vendor. Snapshot controller required for VolumeSnapshot.</li>
      <li><strong>Ingress / Gateway</strong> — Envoy Gateway, Cilium Gateway, Contour (Gateway API). Ingress NGINX is EOL end of 2026.</li>
      <li><strong>Backup</strong> — Velero (the standard), restic for file-level, etcd snapshots for control-plane state.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For air-gapped or compliance-heavy environments, additional choices: image mirror (Harbor + signing), private cert authority, audit log forwarding, SOPS/Sealed Secrets for git-stored secrets, FIPS-mode kernel + crypto. These rarely change once decided; document them in the architecture doc.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team picks Pod CIDR <code>10.10.0.0/16</code>. Their corporate VPN routes <code>10.0.0.0/8</code>. What's the predictable failure?",
            options=[
                ("a) Pods can't reach the internet", False),
                ("b) Pod IPs collide with VPN routes; cross-VPN traffic to/from the cluster gets routed to the wrong place; mysterious connection failures", True),
                ("c) Nothing — the CIDRs are different", False),
            ],
            feedback="<strong>Answer: b.</strong> The cluster's Pod CIDR is a subset of the VPN's <code>10.0.0.0/8</code>. Once you announce that range or rely on routing, packets meant for VPN destinations end up at Pods (or vice versa). Pick CIDRs that <em>cannot overlap</em> with anything you might want to peer with later. Cluster rebuilds are the only fix.",
        ),
    },
    before_after_before='<p>\"We installed kubeadm and it worked.\" Six months later: Pod CIDR overlaps the new VPC peering, etcd disk pressure causes random slowdowns, no documented backup procedure, manual operations only one person knows, no upgrade plan. Migration off this cluster takes a quarter.</p>',
    before_after_after='<p>One-page architecture doc lives in git. CIDRs documented + non-overlapping. etcd on dedicated NVMe. CNI/CSI choices recorded with rationale. Backup interval + restore tested. Upgrade rehearsal scheduled quarterly. The same doc onboards new engineers in an afternoon.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Time spent on the blueprint is the highest-leverage hour you\'ll ever spend on a self-managed cluster.</p>',
    analogy_intro_html='<p>The Drafting Hut is the first stop on the K-Frontier homestead. Before a single tool comes out, you sit at the survey table and draw what you\'re building: where the well goes, where the main house sits, where the watchtower commands the property, how the road approaches the front gate. The drawing names the materials (OS, runtime), the dimensions (CIDR sizes), the foundations (etcd disks), the perimeter (LB, network), and the contingencies (backup chest). You\'ll deviate from it later — but only consciously, with a pencil note.</p>',
    translation_rows=[
        ("Survey table with the cluster blueprint", "Production architecture document"),
        ("Where the well goes", "etcd topology + sizing"),
        ("Main house location", "Control-plane node placement + sizing"),
        ("Property road + front gate", "API server LB + network ingress"),
        ("Plot lines (don't dig past these)", "Pod CIDR + Service CIDR + node subnets"),
        ("Materials list", "OS, runtime, CNI, CSI, ingress controller choices"),
        ("Backup chest", "Velero + etcd snapshot strategy"),
        ("Watchtower position", "Hardening posture + bastion access"),
    ],
    analogy_stops="The analogy stops here: a real cluster has many feedback loops the homestead drawing doesn't capture — autoscaling, controller reconciliation, certificate rotation. The drawing is initial conditions, not the running system.",
    eli5='Before you build a house, you draw it on paper. Where the kitchen goes, where the lights are, where the water comes in. Same with a Kubernetes cluster: you draw it before you start pouring concrete.',
    eli10="Self-managed K8s = you make every architectural choice the cloud usually hides. Sizing (CP / worker / etcd), HA topology (stacked vs external etcd), network plan (Pod CIDR / Service CIDR / DNS / LB / dual-stack), OS, runtime, CNI, CSI, ingress, backup. Document these in a one-page architecture spec before kubeadm runs. Wrong CIDRs and undersized etcd are unfixable without a rebuild.",
    scenarios=[
        Scenario(name="A startup picking stacked etcd + Cilium + Talos", body="3 control-plane + 5 worker bare-metal cluster. Stacked etcd (simpler ops). Talos Linux (immutable, API-driven, no SSH). Cilium CNI with kube-proxy replacement. Pod CIDR <code>192.168.224.0/20</code> (deliberately picked to avoid the corporate <code>10.0.0.0/8</code>). The whole architecture doc fits on two pages."),
        Scenario(name="A bank with external etcd + air-gapped + Calico", body="5 dedicated etcd nodes (NVMe, isolated subnet) + 5 control-plane + 30 worker nodes across 3 racks. Calico with BGP peering to top-of-rack switches (no VXLAN; full underlay routing). Air-gapped install via internal Harbor mirror. RHEL 9 hardened to CIS Level 2. Architecture doc is 18 pages with explicit compliance evidence pointers."),
        Scenario(name="A team that re-architected after pain", body="First cluster: 2 CP nodes (no quorum), shared etcd disks with kubelet, Pod CIDR <code>10.0.0.0/24</code> exhausted at 250 Pods. Rebuilt 18 months in: 3 CP nodes, dedicated etcd disks, Pod CIDR bumped to <code>/16</code>, CNI swapped Flannel → Cilium. The rebuild was 3 weeks of pain that 1 day of architecture would have prevented."),
        Scenario(name="A team using Cluster API (CAPI) for declarative lifecycle", body="Management cluster runs Cluster API. Workload clusters declared as YAML — desired-state managed like any other K8s resource. CAPV (vSphere), CAPA (AWS), CAPZ (Azure), CAPG (GCP) providers handle the underlying infra. Architecture-as-code; new clusters are PRs."),
    ],
    misconceptions=[
        Misconception(myth='\"We can change the Pod CIDR later if we need to.\"', truth='Pod CIDR is set in stone at cluster creation. Changing it is a rebuild. Pick a non-overlapping range, big enough for projected node count × max Pods per node × 2x growth, on day 1.'),
        Misconception(myth='\"Two control-plane nodes is half-redundant.\"', truth='Two etcd members can\'t form quorum after one fails — you need ≥ 3 (or technically odd numbers ≥ 3 — 3, 5, 7). Two CP nodes is worse than one because losing either takes down the cluster. Always odd, always ≥ 3 for HA.'),
        Misconception(myth='\"Talos and Flatcar are exotic; just use Ubuntu.\"', truth='Talos in particular has gained massive adoption in 2024-26 for production self-managed clusters. No SSH, immutable, API-managed. Smaller attack surface, simpler upgrades. Worth evaluating against Ubuntu — the right choice is org-specific, not always the obvious one.'),
    ],
    flashcards=[
        Flashcard(front='Self-managed vs managed K8s — when self-manage?', back='When you need: data sovereignty, on-prem / bare metal / air-gapped, very specific compliance, deep cost optimisation at scale, custom kernel/runtime, cluster-scale your cloud doesn\'t support. Otherwise, managed (EKS/GKE/AKS) usually wins on TCO.'),
        Flashcard(front='Stacked vs external etcd?', back='Stacked = etcd on the same nodes as kube-apiserver (one tier, simpler). External = etcd on dedicated nodes (more resilient, more ops). Most clusters &lt; 250 nodes do fine stacked.'),
        Flashcard(front='Why etcd needs NVMe SSD?', back='etcd writes synchronously and waits for fsync. Slow disks → slow writes → slow API server → cluster-wide degradation. Target &lt; 10ms p99 fsync.'),
        Flashcard(front='Pod CIDR sizing rule of thumb?', back='Each node gets a /24 (256 IPs) by default. With max 110 Pods/node + headroom, that fits. Cluster Pod CIDR = /16 fits 256 nodes. Plan for 2-3x your projected node count.'),
        Flashcard(front='Service CIDR considerations?', back='Default <code>10.96.0.0/12</code> (~1M IPs). Reserve <code>10.96.0.10</code> (or your equivalent) for cluster DNS — every Pod\'s resolv.conf points there.'),
        Flashcard(front='What is Talos Linux?', back='Immutable, API-driven Linux for Kubernetes. No SSH (machine-config API only). Read-only root FS. Smaller attack surface, simpler upgrades. Popular for production self-managed clusters in 2026.'),
        Flashcard(front='What is Cluster API (CAPI)?', back='Declarative cluster lifecycle. A management cluster runs CAPI controllers; workload clusters are YAML. Provider plugins: CAPV (vSphere), CAPA (AWS), CAPZ, CAPG, CAPD (Docker for testing).'),
        Flashcard(front='HA control-plane minimum?', back='3 nodes (odd number ≥ 3 for etcd quorum). 2 nodes is worse than 1 — losing either kills quorum. Production: 3 or 5.'),
    ],
    quizzes=[
        Quiz(prompt='You\'re sizing etcd for a 100-node cluster with ~3000 Pods, modest API write rate. What spec?', answer='3 etcd members (stacked on the control-plane nodes is fine at this size). Per node: 4 vCPU, 8 GiB RAM, 50 GiB NVMe SSD dedicated for etcd data dir, &lt; 10ms p99 fsync verified with <code>fio</code>. Network: low-latency between members (&lt; 10ms). Don\'t share the etcd disk with anything else — not the kubelet, not container images, not logs.'),
        Quiz(prompt='Your team is debating Pod CIDR <code>10.244.0.0/16</code> (kubeadm default) vs <code>192.168.224.0/20</code>. The corporate VPN routes <code>10.0.0.0/8</code>. Which is right and why?', answer='<code>192.168.224.0/20</code>. The kubeadm default <code>10.244.0.0/16</code> is a subset of the VPN\'s <code>10.0.0.0/8</code> — every Pod IP looks like a VPN destination to upstream routers. Symptoms range from \"can\'t reach corporate services from Pods\" to \"corporate hosts can\'t reach the cluster\" to silent black-holing. <code>192.168.224.0/20</code> sits in RFC1918 space the VPN doesn\'t use, gives you 4096 Pod IPs (16 nodes × 256), and can grow with /20 → /16 expansion later. <strong>The kubeadm default is a starting point, not a recommendation.</strong>'),
        Quiz(prompt='You\'re asked to choose between Talos Linux and Ubuntu LTS for a 30-node on-prem cluster. <strong>Click for the decision walk. ▼</strong>', cyoa=True, cyoa_tag='the decision walk', answer='<strong>Pick Talos when:</strong> (1) your team is comfortable with API-driven config (no SSH); (2) you value immutable hosts (kernel + userspace from one signed image); (3) you want simpler upgrades (replace the host image, reboot, done); (4) you don\'t need to install random tools on the host. <strong>Pick Ubuntu when:</strong> (1) your team has deep Ubuntu/Debian expertise + tooling; (2) you need to run agents that don\'t fit Talos\'s extension model; (3) you need root SSH for compliance (some regulators still expect it); (4) you have years of Ansible / playbook investment in Ubuntu hardening. <strong>For a fresh on-prem 30-node cluster in 2026 with a willing team, Talos is the modern default</strong> — smaller attack surface, simpler upgrades, no drift between nodes. The decision is <em>org capability</em>, not technology — both run K8s well.'),
    ],
    glossary=[
        GlossaryItem(name='Self-managed K8s', definition='You install and operate Kubernetes (control plane + workers) yourself, on bare metal / on-prem VMs / IaaS instances. Opposite of managed (EKS/GKE/AKS).'),
        GlossaryItem(name='Stacked etcd', definition='etcd runs on the same nodes as kube-apiserver. Default kubeadm topology.'),
        GlossaryItem(name='External etcd', definition='etcd on dedicated nodes, separate from the apiserver tier.'),
        GlossaryItem(name='Quorum (etcd)', definition='Majority of etcd members reachable. 3 members → 2 reachable for quorum. Odd numbers ≥ 3 for HA.'),
        GlossaryItem(name='Pod CIDR', definition='IP range Pods are allocated from. Cluster-wide; subdivided per node.'),
        GlossaryItem(name='Service CIDR', definition='Virtual IP range for K8s Services (ClusterIPs).'),
        GlossaryItem(name='API server LB', definition='Load balancer in front of kube-apiserver instances. kubeadm clients hit this address.'),
        GlossaryItem(name='kube-vip', definition='Lightweight VIP for the API server LB. Runs as a static pod; popular for kubeadm HA.'),
        GlossaryItem(name='Talos Linux', definition='Immutable, API-driven Linux for K8s. No SSH; configured via machine-config API.'),
        GlossaryItem(name='Cluster API (CAPI)', definition='Declarative cluster lifecycle. Cluster definition is YAML; controllers reconcile.'),
        GlossaryItem(name='kubespray / kOps / RKE2 / k3s', definition='Alternative bootstrappers. kubespray (Ansible), kOps (declarative on cloud), RKE2 (Rancher), k3s (lightweight, edge).'),
        GlossaryItem(name='Air-gapped', definition='Cluster without internet access. Requires internal image mirror, internal CA, internal package repo.'),
    ],
    recap_lead='Architecture-first. Sizing, network plan, OS/runtime/CNI/CSI choices, HA topology, backup, upgrade strategy. One page in git, referenced by every subsequent module.',
    recap_next='<strong>Next — V2: OS and Node Preparation.</strong> Now that you have the blueprint, prepare the soil: kernel modules, sysctl, swap, time sync, runtime install, image pre-pulling. The land has to be cleared before the frame goes up.',
)
