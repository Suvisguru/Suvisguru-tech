"""K-GKE G1 — GKE Architecture and Modes (Standard, Autopilot, Enterprise)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GKE modes — Standard, Autopilot, Enterprise; regional vs zonal; private cluster.">
  <defs>
    <linearGradient id="ggrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#5A9F7A"/><stop offset="100%" stop-color="#3D7857"/></linearGradient>
  </defs>
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Visitors' Pavilion · K-Garden — three modes, three commitments</text>
  <rect x="50" y="70" width="200" height="120" rx="10" fill="url(#ggrad)" stroke="#3F4A5E"/>
  <text x="150" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">GKE Standard</text>
  <text x="150" y="112" text-anchor="middle" font-size="10" fill="#FBF7F0">you choose node pools</text>
  <text x="150" y="128" text-anchor="middle" font-size="10" fill="#FBF7F0">you tune scaling</text>
  <text x="150" y="148" text-anchor="middle" font-size="10" fill="#FBF7F0">most flexibility</text>
  <text x="150" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF7F0">most ops surface</text>
  <rect x="270" y="70" width="200" height="120" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="370" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">GKE Autopilot</text>
  <text x="370" y="112" text-anchor="middle" font-size="10" fill="#FBF7F0">Google manages nodes</text>
  <text x="370" y="128" text-anchor="middle" font-size="10" fill="#FBF7F0">scaling preconfigured</text>
  <text x="370" y="148" text-anchor="middle" font-size="10" fill="#FBF7F0">per-Pod billing</text>
  <text x="370" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF7F0">Pod-level SLA</text>
  <rect x="490" y="70" width="220" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF7F0">GKE Enterprise</text>
  <text x="600" y="105" text-anchor="middle" font-size="9" fill="#FBF7F0">(formerly Anthos)</text>
  <text x="600" y="125" text-anchor="middle" font-size="10" fill="#FBF7F0">fleets · multi-cloud</text>
  <text x="600" y="142" text-anchor="middle" font-size="10" fill="#FBF7F0">Config Sync · Policy Controller</text>
  <text x="600" y="158" text-anchor="middle" font-size="10" fill="#FBF7F0">Cloud Service Mesh</text>
  <text x="600" y="178" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF7F0">add-on tier on top of Standard/Autopilot</text>
</svg>"""


LESSON = LessonSpec(
    num="01",
    title_short="GKE architecture",
    title_full="G1 · GKE Architecture and Modes (Standard, Autopilot, Enterprise)",
    title_html="K-GKE G1 · GKE Architecture and Modes",
    module_eyebrow="Module G1 · the Visitors' Pavilion — three modes, three commitments",
    hero_sub_html='Three modes. <strong>GKE Standard</strong>: you choose node pools, scaling, and ops. <strong>GKE Autopilot</strong>: Google manages nodes / scaling / security; per-Pod billing; Pod-level SLA. <strong>GKE Enterprise</strong> (formerly Anthos): fleets + multi-cloud + Config Sync + Policy Controller + Cloud Service Mesh — an add-on tier on top of Standard or Autopilot. Plus <em>regional vs zonal</em> control planes, <em>multi-zonal node pools</em>, <em>private clusters</em>, <em>master authorized networks</em>, and provisioning paths (gcloud, Terraform, Config Connector, Pulumi).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Your zonal GKE cluster\'s control plane is unreachable — there\'s a zone outage in the very zone you put your apiserver in. Your workloads are running but you can\'t deploy anything; new Pods can\'t schedule because the apiserver is gone. <em>You realise you picked zonal to save the regional control-plane cost.</em> Today\'s lesson: pick the GKE shape that survives this.",
    stamp_html="<strong>Three modes (Standard / Autopilot / Enterprise) × two control-plane scopes (regional / zonal). Regional control plane + Autopilot is the safe default; pick Standard for full knobs; layer Enterprise for fleets + multi-cloud governance.</strong>",
    district_pin="kg-plot01",
    district_label="Visitors' Pavilion",
    sections=[
        Section(
            eyebrow="Section 1.1 · three modes",
            h2="Three modes — Standard, Autopilot, Enterprise",
            body_html="""    <p><strong>GKE Standard</strong>: you create the cluster, you create node pools (System / User / GPU / Spot), you choose VM SKUs, you wire add-ons. Most flexibility. Highest ops surface. <em>Pick when you need precise control over node shape, custom DaemonSets, niche kernel features, or non-standard CNI.</em></p>
    <p><strong>GKE Autopilot</strong>: <em>Google manages all node operations</em>. You declare workloads with resource requests; Google provisions, scales, secures, upgrades, and bills <strong>per Pod</strong> (not per node). Built-in node-level security baseline (no privileged Pods unless you opt in; no SSH; managed registries; admission webhooks for safety). <em>Pod-level SLA</em> (vs Standard\'s control-plane SLA). Pick when you want minimal ops surface and your workloads fit Autopilot\'s admission constraints. <strong>Autopilot workloads can also run inside Standard clusters</strong> via the Autopilot workload class — gives you per-workload Pod-level billing without committing the whole cluster.</p>
    <p><strong>GKE Enterprise</strong> (formerly Anthos) is a <em>tier on top of</em> Standard or Autopilot, not a third cluster shape. Adds <em>fleet management across GCP / AWS / Azure / on-prem</em>, <em>Config Sync</em> (GitOps), <em>Policy Controller</em> (managed Gatekeeper), <em>Cloud Service Mesh</em> (managed Istio), <em>Connect Gateway</em> (kubectl across registered clusters), <em>multi-cluster Ingress / Gateway</em>. Pick when you have ≥10 GKE clusters or hybrid / multi-cloud K8s under one governance plane.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · regional vs zonal + multi-zonal node pools",
            h2="Regional vs zonal control plane; multi-zonal node pools",
            body_html="""    <p><strong>Zonal cluster</strong>: control plane (apiserver + etcd) lives in <em>one zone</em>. Cheaper. <strong>Single zone outage = control plane down.</strong> Workloads keep running but you can\'t deploy or modify until the zone recovers. <em>Avoid for production.</em></p>
    <p><strong>Regional cluster</strong>: control plane runs in <strong>three zones</strong> within the region (apiserver replicated, etcd quorum across zones). Survives a single-zone outage. Recommended default for prod. <em>Roughly 3× the control-plane cost; trivial vs the cost of a workday-long unable-to-deploy outage.</em></p>
    <p><strong>Multi-zonal node pools</strong>: per node pool, you specify <code>--node-locations zone-a,zone-b,zone-c</code>. Pool autoscaler spreads nodes across zones. Workloads with topology-spread constraints stay balanced. Combine with regional control plane for true multi-zone resilience.</p>
    <p><strong>Quick rule:</strong> <em>regional control plane + multi-zonal node pools</em> = the safe default. Pick zonal only for ephemeral / dev clusters where the cost saving matters and the outage risk is acceptable.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · private clusters + authorized networks",
            h2="Private clusters + master authorized networks",
            body_html="""    <p>By default GKE\'s apiserver has a public endpoint. Three increasingly-locked-down options:</p>
    <ul>
      <li><strong>Master authorized networks</strong> — public endpoint stays; firewall allows only specific CIDRs (your office VPN, your CI runners). Cheapest hardening.</li>
      <li><strong>Private cluster, public endpoint</strong> — nodes have only private IPs (egress via Cloud NAT); apiserver still has a public endpoint with authorized networks restricting access. Common production shape.</li>
      <li><strong>Fully private cluster</strong> — nodes private; apiserver private (Private Service Connect). Access via Cloud Interconnect / Cloud VPN / Connect Gateway. Most secure; requires private DNS + service connectivity design.</li>
    </ul>
    <p><strong>Cluster identity</strong>: GKE clusters use a <em>service account</em> that the nodes run as. Defaults to the Compute Engine default SA (over-broad; rotate to a least-privilege SA per cluster). Workloads use <strong>Workload Identity Federation for GKE</strong> (covered in G4) — Pods authenticate to GCP services without baked secrets.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · provisioning paths",
            h2="Four provisioning paths — gcloud, Terraform, Config Connector, Pulumi",
            body_html="""    <p>Pick one tool and stick with it across the cluster lifecycle. Mixing tools = drift. Four common paths:</p>
    <ul>
      <li><strong>gcloud CLI</strong> (<code>gcloud container clusters create</code>) — interactive scripting, ad-hoc clusters, runbooks. The Cloud Console generates equivalent gcloud commands you can copy.</li>
      <li><strong>Terraform Google provider</strong> — most popular cross-platform IaC. Mature modules, strong community. State management is your responsibility (use GCS bucket backend with state locking).</li>
      <li><strong>Config Connector</strong> — GCP-native operator that manages GCP resources as Kubernetes Custom Resources. Reconciled by a control-plane GKE cluster. Useful when GitOps is the source of truth and Argo CD / Flux already runs your platform — GCP resources slot into the same workflow.</li>
      <li><strong>Pulumi</strong> — IaC in real programming languages (TypeScript, Python, Go). Same GCP resources as Terraform; expressive for complex composition logic.</li>
    </ul>
    <p><strong>Production rule:</strong> GKE clusters live in Git via Terraform / Config Connector / Pulumi. Cloud Console + gcloud for exploration only.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="Which is the safe production default?",
            options=[
                ("Zonal control plane + single-zone node pool — cheapest.", False),
                ("Regional control plane + multi-zonal node pools — survives a single-zone outage.", True),
                ("Zonal control plane in three zones simultaneously.", False),
            ],
            feedback="Regional puts the apiserver + etcd quorum across three zones; multi-zonal node pools spread workloads. The cost premium is small vs the cost of a half-day outage.",
        ),
    },
    before_after_before='<p>Pre-Autopilot, every GKE cluster was Standard — operators sized node pools, picked machine types, managed Cluster Autoscaler tuning, installed every add-on. New developers needed a week to understand the cluster shape. Autoscaling pools to zero was awkward. Cost surprises were common — over-provisioned pools idle most of the day. Multi-cloud K8s governance was bring-your-own; security baseline was bring-your-own.</p>',
    before_after_after='<p>Modern GKE has three intent shapes: <strong>Standard</strong> for full control, <strong>Autopilot</strong> for opinionated managed defaults with per-Pod billing and a Pod-level SLA, <strong>Enterprise</strong> as an add-on tier for fleets + multi-cloud governance + GitOps + service mesh. Regional control planes survive zone outages by default. Workload Identity Federation removes the keys-in-cluster problem. Provisioning is declarative via Terraform / Config Connector / Pulumi. <em>The day-1-cluster-to-day-N-cluster journey is shorter.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Pick the mode that matches your operational appetite. Autopilot for "I want managed defaults"; Standard for "I need every knob"; Enterprise on top when fleets + multi-cloud demand uniform governance.</em></p>',
    analogy_intro_html='''<p>K-Garden is the Google-managed botanical garden / orchard. The <strong>Visitors\' Pavilion</strong> is where every visitor enters: at the door, the Head Gardener (Google) hands you a map and a choice — which kind of plot are you here to plant?</p>
    <p>The map shows three plot styles. <strong>Standard plots</strong>: you choose your own soil mix, your own irrigation schedule, your own seedlings. The Head Gardener supplies the climate-controlled greenhouse but you do the rest. <strong>Autopilot plots</strong>: you arrive with seedlings; the Garden\'s robot caretakers (Google) plant, water, prune, and harvest on a smart schedule; you pay per seedling-day, not per plot. <strong>Enterprise membership</strong>: a top-tier subscription that lets your gardening collective coordinate plots across <em>multiple gardens</em> in different climates (multi-cloud) — same care manuals, same security guards, same seasonal schedule, everywhere.</p>
    <p>The Pavilion also has a wall map showing two layout choices. <em>Single-greenhouse layout</em>: cheaper, but if that greenhouse loses heat overnight your plot is unrecoverable. <em>Three-greenhouse layout</em>: your plants live in three glass houses simultaneously; if one loses heat, the others keep going. <strong>Pick the three-greenhouse layout for anything that has to survive bad weather.</strong></p>''',
    translation_rows=[
        ("Visitors' Pavilion", "GKE entry — pick mode + cluster shape"),
        ("Head Gardener", "Google's GKE management plane"),
        ("Standard plot", "GKE Standard — you manage node pools, scaling, ops"),
        ("Autopilot plot", "GKE Autopilot — managed nodes, per-Pod billing, Pod-level SLA"),
        ("Robot caretakers", "Autopilot's preconfigured platform (security baseline + auto-scaling + admission webhooks)"),
        ("Enterprise membership", "GKE Enterprise (formerly Anthos) — fleets + multi-cloud + Config Sync + Policy Controller + CSM"),
        ("Single-greenhouse layout", "Zonal control plane (single-zone apiserver/etcd)"),
        ("Three-greenhouse layout", "Regional control plane (3-zone apiserver/etcd quorum)"),
        ("Multi-bed planting", "Multi-zonal node pools"),
        ("Locked garden gate + visitor pass", "Private cluster + master authorized networks"),
        ("Smart-seed planting tools", "gcloud / Terraform / Config Connector / Pulumi"),
        ("Garden's house keys (Pod auth)", "Workload Identity Federation for GKE"),
    ],
    analogy_stops="A garden plot is fixed to the season; GKE clusters are software-defined and reshape constantly. Real Autopilot has admission webhooks that quietly mutate or reject Pod specs — a robot caretaker that occasionally refuses to plant your seed.",
    eli5="Google has a giant garden. You can rent a plot and do everything yourself, or you can rent a plot where Google\'s robots plant, water, and harvest for you. There\'s a fancier subscription that also lets you have plots in other gardens around the world all coordinated. And — pick the three-greenhouse layout, not one greenhouse, so a frost in one doesn\'t kill everything.",
    eli10="GKE has three modes. <strong>Standard</strong>: you manage node pools + scaling + ops. <strong>Autopilot</strong>: Google manages nodes + scaling + security baseline; per-Pod billing; Pod-level SLA; Autopilot workloads also run inside Standard clusters. <strong>Enterprise</strong> (formerly Anthos): tier-on-top for fleets + multi-cloud + Config Sync + Policy Controller + Cloud Service Mesh + Connect Gateway + multi-cluster Gateway. Plus regional vs zonal control planes (regional = 3-zone HA), multi-zonal node pools, private clusters + master authorized networks, four provisioning paths (gcloud, Terraform, Config Connector, Pulumi).",
    scenarios=[
        Scenario(
            name="SaaS — first GKE cluster picks Autopilot",
            body="A 40-engineer SaaS migrating from Cloud Run to K8s. They pick <strong>regional Autopilot</strong>. <em>Zero node management</em>: they declare Pods with resource requests; Google handles the rest. Per-Pod billing aligns the cluster bill to actual usage; off-hours cost approaches zero. <em>The platform team they didn\'t hire is the cost saving.</em>",
        ),
        Scenario(
            name="ML team — GKE Standard with GPU node pools",
            body="A 200-engineer ML team needs precise GPU scheduling: A3 H100 nodes for training, A4 H200 for inference, custom NVIDIA driver tuning. <strong>GKE Standard</strong> with three GPU node pools (autoscaling) + custom Compute Classes. Autopilot\'s admission constraints would block their custom DaemonSet for distributed training. <em>Trade-off accepted; they staff a small platform team.</em>",
        ),
        Scenario(
            name="Enterprise IT — fleet of 30 clusters across GCP + AWS + on-prem",
            body="A bank acquired three subsidiaries each with their own K8s footprint. They register all clusters into a <strong>GKE Enterprise fleet</strong>. Config Sync deploys uniform NetworkPolicies / Pod-security baselines from one git repo to all clusters. Policy Controller blocks non-compliant deploys at admission. Cloud Service Mesh handles cross-cluster mTLS. <em>One governance model across heterogeneous K8s.</em>",
        ),
        Scenario(
            name="Outage — zonal cluster, zonal control-plane outage, half-day blackout",
            body="A startup picked zonal GKE for cost. A GCP zone had a control-plane disruption at 09:00. Workloads kept running but the team couldn\'t deploy a critical feature flag flip. <em>5 hours of inability to deploy</em>. Postmortem: migrate all prod clusters to <strong>regional control plane</strong> + multi-zonal node pools. Cost premium per cluster: small. Outage cost: large.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Autopilot is just Standard with autoscaling enabled.\"",
            truth="Autopilot is a different cluster shape. Google manages nodes (you don\'t see them; can\'t SSH; can\'t pick SKU directly except via Compute Classes). Per-Pod billing instead of per-node. Built-in admission webhooks block privileged / hostNetwork / hostPath / non-conforming Pods. <em>Pod-level SLA</em> instead of control-plane SLA. Different operational model, not a flag.",
        ),
        Misconception(
            myth="\"GKE Enterprise is a separate cluster type.\"",
            truth="GKE Enterprise is an add-on tier <em>on top of</em> Standard or Autopilot clusters. You enable it on a project / fleet to get fleets + Config Sync + Policy Controller + Cloud Service Mesh + multi-cluster Ingress + Connect Gateway. The cluster underneath is still Standard or Autopilot.",
        ),
        Misconception(
            myth="\"Regional control plane just means workloads run across zones.\"",
            truth="<strong>Regional control plane</strong> = apiserver + etcd are replicated across three zones in the region. <strong>Multi-zonal node pools</strong> = workloads distributed across zones. They\'re independent settings — you can have a regional control plane + a single-zone node pool (apiserver survives, but workloads don\'t). For full multi-zone resilience, both must be set.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three GKE modes — what differs?", back="<strong>Standard</strong>: you manage node pools, scaling, ops. <strong>Autopilot</strong>: Google manages nodes; per-Pod billing; Pod-level SLA; admission webhooks enforce safety baseline. <strong>Enterprise</strong>: add-on tier on top of Standard or Autopilot for fleets, Config Sync, Policy Controller, Cloud Service Mesh, multi-cluster Ingress."),
        Flashcard(front="Regional vs zonal control plane — what survives?", back="<strong>Regional</strong>: apiserver + etcd in 3 zones; survives 1-zone outage. <strong>Zonal</strong>: apiserver + etcd in 1 zone; zone outage = control plane down (workloads keep running but no deploys). Production default = regional."),
        Flashcard(front="What is GKE Enterprise (formerly Anthos)?", back="A <em>tier-on-top</em> of Standard / Autopilot for governance: fleet management across GCP/AWS/Azure/on-prem, Config Sync (GitOps), Policy Controller (managed Gatekeeper), Cloud Service Mesh (managed Istio), Connect Gateway (kubectl across clusters), multi-cluster Ingress / Gateway."),
        Flashcard(front="Multi-zonal node pools — what is it?", back="A node pool spread across multiple zones via <code>--node-locations</code>. Autoscaler distributes nodes per zone. Combine with regional control plane + Pod topology-spread constraints for true multi-zone resilience."),
        Flashcard(front="Three apiserver-locking-down options?", back="<strong>Master authorized networks</strong> (firewall public endpoint), <strong>private cluster + public endpoint</strong> (nodes private, apiserver public-restricted), <strong>fully private cluster</strong> (apiserver via Private Service Connect)."),
        Flashcard(front="Four GKE provisioning paths?", back="<strong>gcloud CLI</strong> (interactive / runbooks), <strong>Terraform Google provider</strong> (most popular cross-platform), <strong>Config Connector</strong> (GCP-as-K8s-CRDs, GitOps-native), <strong>Pulumi</strong> (real programming languages)."),
        Flashcard(front="What does the Compute Engine default service account do, and why rotate it?", back="GKE clusters use a node SA — defaults to the Compute Engine default SA which has <em>over-broad project Editor permissions</em>. Rotate to a least-privilege per-cluster SA: only what nodes actually need (logging.logWriter, monitoring.metricWriter, storage.objectViewer for image pull, etc.)."),
        Flashcard(front="Per-Pod billing in Autopilot — what does it actually mean?", back="Autopilot bills <em>per Pod-second based on requested CPU/memory</em>, not per node. Pod with <code>requests: 100m/256Mi</code> running 1 hour = ~0.1 vCPU-hour + ~0.25 GiB-hour billed. Off-hours scale-to-zero of a Deployment = $0 cost. (Standard always bills per node, regardless of Pod density.)"),
    ],
    quizzes=[
        Quiz(
            prompt="Your team picks Autopilot for the prod cluster. A developer adds a Helm chart for an old monitoring agent that uses <code>hostPath: /var/log</code>. Deploy fails with admission rejection. What\'s happening, and what\'s the path forward?",
            answer="Autopilot blocks hostPath (and hostNetwork, privileged, hostPID, etc.) at admission via built-in webhooks — security baseline cannot be disabled. The chart was written for unprivileged Standard. Two paths: (1) Pick a Cloud-Logging-aware monitoring tool (GKE auto-ships container logs to Cloud Logging without an agent — Container Logs are available in Logs Explorer). (2) If you genuinely need hostPath, run that workload in a Standard node pool (Autopilot workload class lets you keep most of the cluster on Autopilot pricing while specific workloads run on a managed node pool). Don\'t fight Autopilot\'s constraints; they\'re what give you the per-Pod billing + Pod-level SLA.",
        ),
        Quiz(
            prompt="A platform team has 30 clusters across GCP, EKS, and on-prem K8s. They want one place to deploy a NetworkPolicy and have it land everywhere. What\'s the GCP-native answer?",
            answer="Enable <strong>GKE Enterprise</strong>; register all 30 clusters into a <strong>fleet</strong> (including the EKS and on-prem ones via Connect agent + Connect Gateway). Use <strong>Config Sync</strong> from a single Git repo: one NetworkPolicy YAML; reconciled to every fleet member. <strong>Policy Controller</strong> (managed Gatekeeper) enforces the same admission policies fleet-wide. Cloud Service Mesh extends mTLS across the fleet; Connect Gateway lets you <code>kubectl</code> any registered cluster via the GCP control plane.",
        ),
        Quiz(
            prompt="The CFO sees the cluster bill: \"Why are our six clusters all regional? Switch them to zonal — the apiserver runs three replicas, that\'s overkill.\" Defend the choice.",
            answer="\"<strong>Regional means the apiserver + etcd quorum runs across three zones — survives one zone going dark.</strong> Zonal means apiserver + etcd in one zone; if that zone has a control-plane outage, we can\'t deploy, can\'t scale, can\'t fail-over Pods, can\'t flip a feature flag for half a day. We\'ve had at least one customer-facing incident where the only fix was a kubectl edit; on a zonal cluster during that zone\'s control-plane outage, that incident becomes a multi-hour outage. The control-plane premium is roughly 3× — but our control plane is a small fraction of total spend; nodes + storage + LBs dominate. Regional is a few hundred dollars per cluster per month; zonal cluster outage is six-figure customer impact. We keep regional.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CFO",
        ),
    ],
    glossary=[
        GlossaryItem(name="GKE Standard", definition="GKE mode where you manage node pools, scaling, and ops. Most flexibility."),
        GlossaryItem(name="GKE Autopilot", definition="GKE mode where Google manages nodes, scaling, security baseline. Per-Pod billing; Pod-level SLA; admission webhooks enforce safety."),
        GlossaryItem(name="GKE Enterprise", definition="Add-on tier (formerly Anthos) on Standard/Autopilot. Fleets, Config Sync, Policy Controller, CSM, Connect Gateway, multi-cluster Ingress."),
        GlossaryItem(name="Regional cluster", definition="Control plane (apiserver + etcd) replicated across 3 zones in a region. Survives single-zone outages."),
        GlossaryItem(name="Zonal cluster", definition="Control plane in 1 zone. Cheaper; zone outage = control plane down."),
        GlossaryItem(name="Multi-zonal node pool", definition="Node pool spread across zones via --node-locations. Workloads distributed; topology-spread constraints align."),
        GlossaryItem(name="Master authorized networks", definition="Firewall on the apiserver public endpoint — allow only specified CIDRs."),
        GlossaryItem(name="Private cluster", definition="GKE shape: nodes have only private IPs (Cloud NAT for egress); apiserver may be public-restricted or fully private (PSC)."),
        GlossaryItem(name="Compute Engine default SA", definition="Default node service account with project-Editor — over-broad. Rotate to least-privilege per cluster."),
        GlossaryItem(name="Workload Identity Federation for GKE", definition="GKE\'s Pod-to-GCP auth — federates K8s SA tokens with GCP SAs (or principals). Replaces older Workload Identity GKE Pool model."),
        GlossaryItem(name="Config Connector", definition="GCP-native operator: GCP resources as K8s Custom Resources reconciled in a control-plane GKE cluster."),
        GlossaryItem(name="Connect Gateway", definition="GKE Enterprise feature — kubectl any registered fleet cluster via the GCP control plane."),
    ],
    recap_lead="Three GKE modes (Standard / Autopilot / Enterprise) × control-plane scope (regional vs zonal) × node-pool topology (zonal / multi-zonal) × apiserver exposure (public / authorized / private). Pick mindfully; Autopilot regional is the safe default.",
    recap_next='<strong>Next — G2: GKE Versioning and Release Channels.</strong> Rapid / Regular / Stable / Extended channels; auto-upgrades; maintenance windows + exclusions; version availability + EOS + SLA + upgrade notifications.',
)
