"""K-AKS A1 — AKS Architecture and Shared Responsibility."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AKS architecture: Azure-managed control plane, customer-managed node pools, AKS Standard vs AKS Automatic.">
  <defs>
    <linearGradient id="azuregrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#7AB3CC"/><stop offset="100%" stop-color="#4A8FA8"/></linearGradient>
  </defs>
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="48" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Welcome Center · K-Campus map on the wall</text>
  <rect x="50" y="70" width="200" height="110" rx="10" fill="url(#azuregrad)" stroke="#3F4A5E" stroke-width="1"/>
  <text x="150" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">Azure-managed</text>
  <text x="150" y="112" text-anchor="middle" font-size="10" fill="#FBF7F0">control plane (free)</text>
  <text x="150" y="130" text-anchor="middle" font-size="10" fill="#FBF7F0">apiserver · etcd · scheduler</text>
  <text x="150" y="148" text-anchor="middle" font-size="10" fill="#FBF7F0">controller-manager</text>
  <text x="150" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF7F0">multi-AZ · auto-patched</text>
  <rect x="290" y="70" width="430" height="110" rx="10" fill="#5A9F7A" stroke="#3F4A5E" stroke-width="1"/>
  <text x="505" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">Customer-managed</text>
  <text x="505" y="112" text-anchor="middle" font-size="10" fill="#FFFFFF">VNet · node pools · workloads · IAM · cost</text>
  <rect x="305" y="125" width="95" height="40" rx="5" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="352" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#3F4A5E">System NP</text>
  <text x="352" y="158" text-anchor="middle" font-size="8" fill="#3F4A5E">CoreDNS, etc.</text>
  <rect x="408" y="125" width="95" height="40" rx="5" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="455" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#3F4A5E">User NP</text>
  <text x="455" y="158" text-anchor="middle" font-size="8" fill="#3F4A5E">your apps</text>
  <rect x="511" y="125" width="95" height="40" rx="5" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="558" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#3F4A5E">Spot NP</text>
  <text x="558" y="158" text-anchor="middle" font-size="8" fill="#3F4A5E">cheap</text>
  <rect x="614" y="125" width="95" height="40" rx="5" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="661" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#3F4A5E">GPU/Win NP</text>
  <text x="661" y="158" text-anchor="middle" font-size="8" fill="#3F4A5E">specialty</text>
</svg>"""


LESSON = LessonSpec(
    num="01",
    title_short="AKS architecture",
    title_full="A1 · AKS Architecture and Shared Responsibility",
    title_html="K-AKS A1 · AKS Architecture",
    module_eyebrow="Module A1 · the Azure-managed control plane + your node pools",
    hero_sub_html='AKS = Azure runs the control plane (apiserver, etcd, scheduler, controller-manager) across availability zones, free, auto-patched. <strong>You</strong> still own VNet + node pools + workloads + identity + cost. Two flavours: <strong>AKS Standard</strong> (BYO add-ons) vs <strong>AKS Automatic</strong> (preconfigures Managed Prometheus, Managed Grafana, Container Insights, Workload Identity, KEDA, Azure RBAC).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It's 3 AM. PagerDuty: <em>\"AKS cluster control plane unhealthy.\"</em> You SSH around for the apiserver — it doesn't exist, AKS hides it. You can't see etcd. You start typing <code>az aks ...</code> and realise you don't know whether the System node pool can be deleted, where the kubelet logs live, or what the heck a Node Resource Group is. <em>You inherited the cluster two days ago.</em> Today's lesson: the AKS map.",
    stamp_html="<strong>AKS = Azure-managed control plane (free, multi-AZ) + customer-managed node pools (System / User / Spot / Win / GPU). Choose AKS Automatic for preconfigured observability and identity; AKS Standard for full control. Provision via Portal, az CLI, ARM/Bicep, Terraform, Pulumi, or Crossplane.</strong>",
    district_pin="kc-wing01",
    district_label="Welcome Center",
    sections=[
        Section(
            eyebrow="Section 1.1 · what AKS is and isn't",
            h2="AKS is the Azure-managed K8s control plane",
            body_html="""    <p><strong>AKS is a managed Kubernetes service.</strong> Azure operates the control plane (apiserver, etcd, scheduler, controller-manager) across availability zones. The control plane is <strong>free</strong> on the Free tier (no SLA), or paid on the Standard / Premium tiers (financially-backed SLA + LTS access). You SSH no etcd; you patch no apiserver. Azure does both.</p>
    <p><strong>What AKS does <em>not</em> manage:</strong> your VNet, your node pools (the VMs that actually run Pods), your workloads, your IAM, your costs, your add-ons (unless you're on AKS Automatic), your DR. The mental rule: <em>everything below the apiserver is Azure's; everything above is yours.</em></p>
    <p><strong>What runs in your subscription:</strong> the <em>node resource group</em> (auto-created, named <code>MC_&lt;rg&gt;_&lt;cluster&gt;_&lt;region&gt;</code>) — contains the node pool VMSS, the cluster Load Balancer, and any add-on resources. <em>You can read it but should not edit it directly</em> — Azure reconciles changes back.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · five node-pool types",
            h2="Five node-pool types and when to use each",
            body_html="""    <p>An AKS cluster has at least one <strong>node pool</strong> = a VMSS (Virtual Machine Scale Set) of identical VMs. Five types:</p>
    <ul>
      <li><strong>System node pool</strong> (mandatory; minimum 1) — runs CoreDNS, metrics-server, AKS overlay agents, Konnectivity. Linux only. Taint: <code>CriticalAddonsOnly=true:NoSchedule</code> by convention so user workloads don't crowd it. <em>Don't run app workloads here — instability cascades.</em></li>
      <li><strong>User node pool</strong> — your application workloads. Add as many as you need.</li>
      <li><strong>Spot node pool</strong> — discounted (up to 90% off) Spot VMs that Azure can evict with 30-second warning. Auto-tainted <code>kubernetes.azure.com/scalesetpriority=spot:NoSchedule</code> — workloads must explicitly tolerate.</li>
      <li><strong>Windows node pool</strong> — Windows Server 2022 nodes for .NET Framework workloads. Mixed Linux/Windows clusters are normal. Cannot run on the System pool — must add a separate Windows pool.</li>
      <li><strong>GPU node pool</strong> — Standard_NC* / ND* SKUs with NVIDIA drivers + the <code>nvidia.com/gpu</code> device plugin. AKS GPU image (<code>UbuntuGPU</code>) ships drivers preinstalled.</li>
    </ul>
    <p><strong>Pool-level config:</strong> VM size, count (min/max for autoscaling), zones, taints, labels, OS SKU (Ubuntu 22.04 / Azure Linux 3 / Windows Server 2022), max-pods-per-node, OS disk type (Managed / Ephemeral), node image upgrade channel.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · AKS Standard vs AKS Automatic",
            h2="AKS Standard vs AKS Automatic",
            body_html="""    <p><strong>AKS Standard</strong> is the historical default: you create a cluster; you turn on add-ons one by one (Container Insights, Managed Prometheus, Workload Identity, Azure RBAC, etc.); you pick node pool sizes; you tune everything yourself. Highest flexibility, most setup.</p>
    <p><strong>AKS Automatic</strong> (GA April 2025) preconfigures the production-ready stack: <strong>Managed Prometheus + Managed Grafana + Container Insights</strong> (observability), <strong>Workload Identity + Azure RBAC for K8s + local accounts disabled</strong> (identity), <strong>NAP (Node Auto Provisioning)</strong> instead of manual node pools, <strong>KEDA + VPA</strong> for autoscaling, <strong>image cleaner + auto-upgrade</strong> for ops, <strong>NetworkPolicy via Cilium</strong> by default. <em>You declare workloads; Azure picks node sizes, scales, patches, and observes.</em></p>
    <p><strong>Pick Automatic if:</strong> standard production AKS, and you're happy delegating size/scaling decisions. <strong>Pick Standard if:</strong> you need fine-grained control (custom CNI, Windows-only clusters, FIPS compliance, custom node images, specific add-on combinations Automatic doesn't support).</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · provisioning paths",
            h2="Six ways to provision an AKS cluster",
            body_html="""    <p>Pick one tool and stick with it across the lifecycle. Mixing tools = drift. The six common paths:</p>
    <ul>
      <li><strong>Azure Portal</strong> — for a one-off learning cluster or a quick demo. Not for production (no source of truth).</li>
      <li><strong>Azure CLI (<code>az aks create</code>)</strong> — interactive scripting, ad-hoc clusters. Good for runbooks. The Portal generates equivalent CLI commands.</li>
      <li><strong>ARM / Bicep</strong> — Azure-native IaC. Bicep is the modern syntax (compiled to ARM JSON). Tight Azure integration; deploys via <code>az deployment group create</code>.</li>
      <li><strong>Terraform AzureRM provider</strong> — the most popular cross-platform IaC for AKS. Strong community, mature modules. State management is your responsibility (use Azure Storage backend with state locking).</li>
      <li><strong>Pulumi</strong> — IaC in real programming languages (TypeScript, Python, Go, C#). Same Azure resources as Terraform; more expressive for complex logic.</li>
      <li><strong>Crossplane</strong> — Kubernetes-native IaC (Azure resources as Custom Resources reconciled by a control-plane cluster). Useful when AKS provisions other AKS clusters via GitOps.</li>
    </ul>
    <p><strong>Production rule:</strong> AKS clusters live in Git via Bicep / Terraform / Pulumi / Crossplane. Portal + CLI for exploration only.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="Which is true about the System node pool?",
            options=[
                ("It can be safely used for application workloads if labelled.", False),
                ("It runs cluster-critical add-ons (CoreDNS, etc.) and is conventionally tainted CriticalAddonsOnly so user workloads don't crowd it.", True),
                ("It is optional and many production clusters skip it.", False),
            ],
            feedback="The System pool is mandatory and reserved for cluster-critical components. Run user workloads in a separate User pool to keep the System pool stable.",
        ),
    },
    before_after_before='<p>"K8s in Azure" used to mean <strong>aks-engine</strong> (deprecated) or hand-rolled VMSS + kubeadm. Operators wrote ARM templates that provisioned VMs, ran cloud-init scripts to install kubelet/kubeadm, bootstrapped the control plane on three VMs, configured etcd Raft, secured certs by hand, and were responsible for every patch. <strong>Six weeks to a working cluster; one ops engineer per cluster, full-time.</strong></p>',
    before_after_after='<p>AKS gives you a control plane in 5-10 minutes via <code>az aks create</code> or one Bicep file. Azure runs apiserver + etcd + scheduler + controller-manager across AZs, free. <strong>AKS Automatic</strong> goes further: it preconfigures Managed Prometheus + Grafana + Container Insights + Workload Identity + Azure RBAC + NAP + KEDA in the same call. <strong>Six minutes to a production-shaped cluster; one ops engineer manages dozens.</strong> The remaining work is what you uniquely care about: VNet design, identity model, workloads, cost.</p>',
    before_after_caption='<p class="ba-caption"><em>The six-weeks-of-cluster-plumbing era is over. The trade-off: you must learn AKS\'s opinions (node resource group, AKS Automatic defaults, version policy) instead of K8s\'s opinions.</em></p>',
    analogy_intro_html='''<p>K-Campus is the Azure-managed campus complex. The <strong>Welcome Center</strong> is where you arrive: there\'s a wall map, a glass case showing the campus floor plan, and a Facilities Director who explains the rules. Azure (the Facilities Director) operates the lights, the HVAC, the alarm system, and the campus shuttle — you (the Faculty) lease wings of buildings to host your departments. The map shows which buildings Azure runs and which buildings <em>you</em> run.</p>
    <p>The Welcome Center wall has two big panels. <strong>Left panel: Azure runs this</strong> — the central plant, the campus DNS, the security cameras, the elevators. You don\'t see them; you can\'t edit them; they just work. <strong>Right panel: You run this</strong> — your department offices (workloads), the staff you hire (identity), the storerooms (storage), the budget. <em>Everything visible from the floor plan is one of those two columns.</em> No surprise pre-existing buildings. No "shared" buildings.</p>
    <p>Some Faculty pick <strong>AKS Standard</strong> — they want to choose every paint colour and every desk arrangement themselves. Other Faculty pick <strong>AKS Automatic</strong> — they want Azure to set up the projector, the whiteboard, the lighting, and the fire alarm with sensible defaults so they can teach class on day one.</p>''',
    translation_rows=[
        ("Welcome Center floor plan", "AKS shared-responsibility model"),
        ("Facilities Director (Azure)", "Azure-managed control plane"),
        ("Left panel — Azure runs this", "kube-apiserver, etcd, scheduler, controller-manager"),
        ("Right panel — you run this", "VNet, node pools, workloads, IAM, costs"),
        ("Wings of the campus", "Node pools — System, User, Spot, Windows, GPU"),
        ("The mandatory front desk", "System node pool (CoreDNS, metrics-server)"),
        ("Pre-furnished classroom", "AKS Automatic"),
        ("Empty classroom you furnish", "AKS Standard"),
        ("Building keys + ID badge", "Cluster identity (managed identity)"),
        ("Service-room next door", "Node Resource Group (MC_*)"),
        ("Architectural blueprint repo", "Bicep / Terraform / Pulumi / Crossplane"),
    ],
    analogy_stops="The campus has fixed walls; an AKS cluster has elastic node pools that grow and shrink during the day. The Welcome Center map is a snapshot; reality is a movie.",
    eli5="Azure runs a giant brain at the campus that decides where your work happens. You bring the workers (your apps). Azure picks the rooms; the brain tells the workers which room to go to. You pay for the rooms, not the brain.",
    eli10="AKS is Azure operating the K8s control plane (apiserver, etcd, scheduler, controller-manager) across availability zones for free, while you operate the node pools (VMSS of VMs) where your Pods actually run. There are five node-pool flavours (System / User / Spot / Windows / GPU). You can take the no-decisions path with <strong>AKS Automatic</strong> (preconfigures Managed Prometheus, Grafana, Container Insights, Workload Identity, NAP, KEDA) or the full-control path with <strong>AKS Standard</strong>. Provision via Portal, Azure CLI, Bicep, Terraform, Pulumi, or Crossplane.",
    scenarios=[
        Scenario(
            name="Mid-size SaaS, first AKS cluster — picks AKS Automatic",
            body="A 50-engineer SaaS migrating from VMs to K8s. They have no platform team and don't want one. They pick <strong>AKS Automatic</strong>. In one <code>az aks create</code> command they get: Managed Prometheus + Grafana, Container Insights, Workload Identity, Azure RBAC, NAP for compute, KEDA + VPA, image cleaner, auto-upgrade. <em>Day-1 production-shaped cluster with no Helm charts to install.</em> Trade-off: less knob-twiddling. Worth it for them.",
        ),
        Scenario(
            name="Bank, regulatory cluster — picks AKS Standard",
            body="A bank running PCI workloads. They need: a custom NSG ruleset, BYO Cilium with strict NetworkPolicies, FIPS-validated node images, locked-down ACR, no preview features, audit logs to a specific Log Analytics workspace. <em>AKS Automatic doesn't yet support all those constraints together</em>. They pick <strong>AKS Standard</strong> and configure each add-on manually via Bicep. Higher setup cost; required for compliance.",
        ),
        Scenario(
            name="ML team, GPU spike workloads",
            body="A 200-engineer ML team runs hyperparameter sweeps. Three node pools: <strong>System</strong> (D-series, 3 nodes), <strong>User</strong> (D-series autoscale 5-50 for inference), <strong>GPU Spot</strong> (NC-series A100, autoscale 0-100). The Spot pool runs sweeps; gets evicted; sweeps checkpoint and resume on the next eviction-tolerant node. <em>Cost: 70% lower than always-on GPU; same throughput.</em>",
        ),
        Scenario(
            name="Multi-tenant SaaS, Crossplane provisions per-tenant clusters",
            body="A SaaS where each enterprise tenant gets their own AKS cluster. Provisioning by hand isn't viable at 200 tenants. They run a single <strong>management AKS cluster</strong> with <strong>Crossplane + Azure provider</strong>. New tenant arrives → operator commits a Tenant CR to git → Argo CD syncs → Crossplane reconciles a new AKS cluster + identity + ACR + Key Vault for that tenant. <em>Cluster provisioning becomes a git PR.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"The control plane is free, so AKS is free.\"",
            truth="Free Tier control plane (no SLA) is free. <strong>Standard Tier</strong> (production SLA) is $0.10/cluster/hour ≈ $73/month. <strong>Premium Tier</strong> (LTS support) is $0.60/cluster/hour. Plus you pay for every node VM, every Managed Disk, every Load Balancer, every public IP, every Log Analytics ingest GB. Control-plane fee is a small fraction; data-plane is the bill.",
        ),
        Misconception(
            myth="\"I should run my workloads on the System node pool to save money.\"",
            truth="The System pool is conventionally tainted <code>CriticalAddonsOnly=true:NoSchedule</code>. Bypassing the taint means CoreDNS, metrics-server, and Konnectivity compete for CPU with your apps — and a noisy app will starve cluster-critical components. A user pool of the same VM SKU is the same cost.",
        ),
        Misconception(
            myth="\"AKS Automatic is just AKS Standard with autoscaling enabled.\"",
            truth="AKS Automatic preconfigures a coherent <em>production stack</em>: Managed Prometheus + Grafana + Container Insights observability, Workload Identity + Azure RBAC + local-accounts-disabled identity, NAP for node provisioning, KEDA + VPA for scaling, image cleaner, auto-upgrade, NetworkPolicy via Cilium. It also <em>removes</em> some knobs (you can't change the network plugin to Kubenet, can't turn off Workload Identity). Not a flag; a different cluster shape.",
        ),
    ],
    flashcards=[
        Flashcard(front="What does AKS manage and what do you manage?", back="<strong>Azure manages</strong> the control plane (apiserver, etcd, scheduler, controller-manager) across AZs. <strong>You manage</strong> the VNet, node pools, workloads, identity, and cost. The Node Resource Group (MC_*) lives in your subscription but is reconciled by Azure — read but don't edit."),
        Flashcard(front="What are the five AKS node-pool types?", back="<strong>System</strong> (mandatory, runs CoreDNS, etc.), <strong>User</strong> (your apps), <strong>Spot</strong> (cheap evictable), <strong>Windows</strong> (Server 2022 for .NET Framework), <strong>GPU</strong> (NC/ND SKUs with NVIDIA drivers preinstalled)."),
        Flashcard(front="Difference between AKS Standard and AKS Automatic?", back="<strong>Standard</strong>: you turn on each add-on. <strong>Automatic</strong> (GA Apr 2025): preconfigures Managed Prometheus + Grafana + Container Insights + Workload Identity + Azure RBAC + NAP + KEDA + VPA + image cleaner + auto-upgrade + Cilium NetworkPolicy. Removes some knobs, adds opinionated defaults."),
        Flashcard(front="What's the Node Resource Group (MC_*)?", back="The auto-created Azure resource group that holds the node pool VMSS, cluster Load Balancer, NSGs, public IPs, etc. Named <code>MC_&lt;rg&gt;_&lt;cluster&gt;_&lt;region&gt;</code>. You can read it but Azure reconciles direct edits — change via AKS APIs instead."),
        Flashcard(front="Six provisioning tools for AKS?", back="Portal (demo only), Azure CLI (<code>az aks create</code>), <strong>ARM/Bicep</strong> (Azure-native IaC), <strong>Terraform AzureRM</strong> (most popular cross-platform), <strong>Pulumi</strong> (IaC in real languages), <strong>Crossplane</strong> (Kubernetes-native, useful for cluster-of-clusters)."),
        Flashcard(front="What is Azure Linux 3 and why does it matter?", back="Microsoft's optimised Linux distro for AKS nodes (formerly CBL-Mariner). <strong>Azure Linux 2 reached end of support 2025-11-30</strong> and node images are removed 2026-03-31 — every AKS node currently on AL2 must migrate to <strong>Azure Linux 3</strong> or <strong>Ubuntu 24</strong>. Set the OS SKU at node-pool creation; can't be changed in place."),
        Flashcard(front="What's a managed identity vs a service principal?", back="Both authenticate AKS to other Azure services. <strong>Managed identity</strong> (system-assigned or user-assigned) is the modern path — Azure rotates the secret. <strong>Service principal</strong> is the legacy path — you manage the secret. New AKS clusters default to managed identity; service-principal clusters should be migrated."),
        Flashcard(front="What is the AKS Release Tracker?", back="A public Microsoft tool showing which AKS minor versions are rolling out to which Azure regions. Use it to plan upgrades — a region might be on the new minor while another lags by a week or two. URL: releases.aks.azure.com."),
    ],
    quizzes=[
        Quiz(
            prompt="You ran <code>az aks create</code> and the cluster is ready. You inspect resource groups in your subscription and see two new ones: the one you specified and one called <code>MC_myrg_mycluster_eastus</code>. What is in MC_*, and what should you do with it?",
            answer="The MC_* group is the <strong>Node Resource Group</strong> — Azure auto-created it to hold cluster infrastructure: the node pool VMSS, the cluster Load Balancer, NSGs, public IPs, managed disks, etc. <strong>Read it freely</strong> (great for debugging). <strong>Don't edit it directly</strong> — Azure reconciles changes back. To change anything in MC_*, use the AKS API surface (e.g. <code>az aks nodepool update</code>, <code>az aks update --load-balancer-...</code>).",
        ),
        Quiz(
            prompt="A teammate proposes deploying a new monitoring DaemonSet to the System node pool to \"save costs and avoid a separate pool.\" What's the risk?",
            answer="The System pool is conventionally tainted <code>CriticalAddonsOnly=true:NoSchedule</code>. To land your DaemonSet there, your teammate would either remove that taint (now the System pool runs CoreDNS + metrics-server + Konnectivity + your DaemonSet competing for the same CPU/memory) or add a toleration. Either way: a noisy DaemonSet evicts CoreDNS, your DNS service degrades, every other Pod's resolution starts failing, and you have a cluster-wide outage. <strong>Add a User pool of the same SKU instead</strong> — same cost, isolation preserved.",
        ),
        Quiz(
            prompt="The CTO walks in: \"Auto Mode for EKS is just preview; we should wait for Azure to do the same.\" You've been running AKS Automatic for two months. How do you respond?",
            answer="<strong>AKS Automatic went GA in April 2025</strong>, several months before EKS Auto Mode. It preconfigures Managed Prometheus + Grafana + Container Insights + Workload Identity + Azure RBAC + NAP + KEDA + VPA + image cleaner + auto-upgrade + Cilium NetworkPolicy in one <code>az aks create</code>. You've been on it for two months with zero ops work for those features. Show the CTO the cluster + the Grafana dashboard + the Workload Identity demo. <em>The wait is over.</em>",
            cyoa=True,
            cyoa_tag="the response that earned a follow-up demo invite",
        ),
    ],
    glossary=[
        GlossaryItem(name="AKS", definition="Azure Kubernetes Service — Microsoft's managed K8s service."),
        GlossaryItem(name="Node Resource Group (MC_*)", definition="Auto-created Azure resource group holding node pool VMSS, cluster LB, NSGs, public IPs. Reconciled by Azure; don't edit directly."),
        GlossaryItem(name="Node pool", definition="A VMSS of identical VMs that run Pods. Five types: System, User, Spot, Windows, GPU."),
        GlossaryItem(name="System node pool", definition="Mandatory pool that runs cluster-critical components (CoreDNS, metrics-server, Konnectivity). Conventionally tainted CriticalAddonsOnly=true:NoSchedule."),
        GlossaryItem(name="AKS Standard", definition="Default AKS shape — you turn on add-ons one by one. Highest flexibility, most setup."),
        GlossaryItem(name="AKS Automatic", definition="GA Apr 2025 — preconfigures Managed Prometheus, Grafana, Container Insights, Workload Identity, Azure RBAC, NAP, KEDA, VPA, image cleaner, auto-upgrade, Cilium NetworkPolicy."),
        GlossaryItem(name="AKS Free / Standard / Premium tier", definition="Pricing tiers for the AKS control plane. Free = no SLA. Standard = SLA at $0.10/hr. Premium = LTS access at $0.60/hr."),
        GlossaryItem(name="Managed identity", definition="Azure-managed credential bound to an Azure resource (e.g. AKS cluster). Rotates automatically. System-assigned (lifecycle = parent) or user-assigned (independent lifecycle)."),
        GlossaryItem(name="Service principal", definition="Legacy AKS identity model — you manage the secret. Replaced by managed identities."),
        GlossaryItem(name="VMSS", definition="Virtual Machine Scale Set — Azure's auto-scaling VM group. Each AKS node pool is backed by one VMSS."),
        GlossaryItem(name="Bicep", definition="Microsoft's modern Azure IaC DSL. Compiles to ARM JSON. Tighter syntax than ARM."),
        GlossaryItem(name="AKS Release Tracker", definition="Microsoft's public tool showing which AKS minor versions are available in which regions, so you can time upgrades."),
    ],
    recap_lead='You can now point at the AKS shared-responsibility split, name the five node-pool types, choose between AKS Standard and AKS Automatic, and pick a provisioning tool. The Welcome Center map is internalised.',
    recap_next='<strong>Next — A2: Azure Identity and Access.</strong> Microsoft Entra ID, Workload Identity (replaces Pod Identity), Azure RBAC for K8s, kubelogin, ACR + Key Vault integration, Conditional Access for kubectl.',
)
