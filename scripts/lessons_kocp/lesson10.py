"""K-OCP O10 — Multi-Cluster with ACM (RHACM / Open Cluster Management)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="RHACM — multi-cluster management with ManagedClusters, Placement, ApplicationSets, Policy, Observability.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Multi-Foundry Network — RHACM federation</text>
  <rect x="40" y="65" width="170" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="125" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">cluster lifecycle</text>
  <text x="125" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">ManagedCluster CR</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Placement / PlacementRule</text>
  <text x="125" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">cluster lifecycle (HCP)</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">cluster pools</text>
  <rect x="225" y="65" width="170" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="310" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">applications</text>
  <text x="310" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">ApplicationSet</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">(Argo CD-based)</text>
  <text x="310" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">cluster claims via labels</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">+ Subscription channels</text>
  <rect x="410" y="65" width="170" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="495" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">policy + governance</text>
  <text x="495" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">Policy / PolicySet</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">PlacementBinding</text>
  <text x="495" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">enforce / inform</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">CIS / NIST policies</text>
  <rect x="595" y="65" width="125" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="657" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">obs + multi-cluster</text>
  <text x="657" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">ObservabilityAddon</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">multi-cluster Prom</text>
  <text x="657" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">Submariner integ</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">HCP at scale</text>
</svg>"""


LESSON = LessonSpec(
    num="10", title_short="multi-cluster (ACM)",
    title_full="O10 · Multi-Cluster with ACM (RHACM / Open Cluster Management)",
    title_html="K-OCP O10 · Multi-Cluster (RHACM)",
    module_eyebrow="Module O10 · the Multi-Foundry Network",
    hero_sub_html='<strong>Red Hat Advanced Cluster Management (RHACM)</strong> = the upstream Open Cluster Management. Manage many OCP + non-OCP K8s clusters from one hub. <strong>ManagedCluster</strong> CR per cluster; <strong>Placement</strong> selects clusters by labels; <strong>ApplicationSet</strong> deploys workloads across clusters (Argo CD-based); <strong>Policy + PlacementBinding</strong> enforces governance fleet-wide; <strong>ObservabilityAddon</strong> aggregates metrics across the fleet. <strong>Hosted Control Planes (HyperShift)</strong> at scale via ACM; <strong>Submariner</strong> integration for cross-cluster networking.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"PolicySet violation across 18 of 30 ManagedClusters: privileged Pod detected.\"</em> Someone applied a privileged-Pod spec to a Production cluster bypassing RHACM Policy, then RHACM\'s reconcile detected drift and fired the alert. The PolicySet has Placement that should target only non-prod, but a label drift on a prod cluster put it in scope. <em>You don\'t know whether to enforce-deny + risk workload outage, or inform + chase down the drift first.</em> Today\'s lesson: RHACM\'s ManagedCluster + Placement + ApplicationSet + Policy + ObservabilityAddon model.",
    stamp_html="<strong>RHACM hub manages many OCP + non-OCP K8s clusters as ManagedClusters. Placement selects by labels; ApplicationSet pushes apps; Policy + PlacementBinding governs fleet-wide; ObservabilityAddon aggregates. Add HCP for cluster-density + Submariner for cross-cluster networking.</strong>",
    district_pin="ko-bay10", district_label="Multi-Foundry Network",
    sections=[
        Section(eyebrow="Section 1.1 · ManagedCluster + Placement + cluster lifecycle",
            h2="ManagedCluster + Placement + cluster lifecycle (HCP)",
            body_html="""    <p><strong>RHACM hub cluster</strong> = central management cluster running the <strong>multicluster-engine (MCE)</strong> + RHACM Operators. <strong>ManagedCluster</strong> CRs represent each managed cluster (OCP, EKS, GKE, AKS, OKD, k3s, etc.). Each ManagedCluster has a <em>klusterlet agent</em> running on it for hub-spoke communication.</p>
    <p><strong>Cluster registration:</strong> two paths.
    <ul>
      <li><strong>Manual import</strong>: admin runs <code>oc apply -f klusterlet.yaml</code> on the target cluster pointing at the hub.</li>
      <li><strong>Cluster Lifecycle (Cluster Lifecycle / cluster API)</strong>: hub provisions new OCP clusters from templates (ClusterDeployment / InstallConfig). Supports IPI + Hosted Control Planes (HCP). For HCP: control planes run as Pods inside hub or dedicated HCP-host clusters; data planes are workers in target environments.</li>
    </ul>
    <p><strong>Placement</strong> CR selects ManagedClusters by labels:
    <ul>
      <li>ClusterSelector with matchLabels / matchExpressions.</li>
      <li>NumberOfClusters constraint (e.g., \"deploy to 3 clusters\").</li>
      <li>Tolerations + spread constraints.</li>
    </ul>
    <p>Result: a PlacementDecision listing which ManagedClusters match. Used by ApplicationSet, Policy, ObservabilityAddon.</p>
    <p><strong>Cluster pools</strong> — pre-provisioned ClusterPools that warm-start clusters; admin claims a cluster from the pool when needed.</p>"""),
        Section(eyebrow="Section 1.2 · ApplicationSet + Subscription", h2="ApplicationSet (Argo CD-based) + Subscription model",
            body_html="""    <p><strong>ApplicationSet</strong> (Argo CD CR — RHACM ships managed Argo CD via OpenShift GitOps) — generates Argo CD <code>Application</code>s based on cluster-list generators tied to RHACM Placements.</p>
    <p>Generators include:
    <ul>
      <li><strong>Cluster generator</strong> — creates an Application per cluster matching a label selector.</li>
      <li><strong>List generator</strong> — explicit list.</li>
      <li><strong>Git generator</strong> — derives clusters from files / directories in a Git repo.</li>
      <li><strong>Matrix generator</strong> — combine multiple generators.</li>
    </ul>
    <p>Result: same Helm chart / Kustomize / plain manifests deployed to many clusters with per-cluster parameterisation. Argo CD handles drift detection + sync per cluster.</p>
    <p><strong>RHACM Subscription model</strong> (older path; Argo CD ApplicationSet is now preferred) — Channel + Subscription + PlacementRule for app deployment. Still works; mostly replaced by ApplicationSet for new fleets.</p>"""),
        Section(eyebrow="Section 1.3 · Policy + PlacementBinding + governance", h2="Policy + PlacementBinding — fleet-wide governance",
            body_html="""    <p><strong>Policy</strong> CR = a desired-state declaration enforced across managed clusters. Bound to clusters via <strong>PlacementBinding</strong> + Placement.</p>
    <p><strong>Policy types</strong>:
    <ul>
      <li><strong>Configuration policies</strong> (most common) — wrap arbitrary K8s resources with a desired-state intent.</li>
      <li><strong>Compliance Operator</strong> + RHACM integration — push CIS / NIST / PCI / FedRAMP / HIPAA scan results to the hub.</li>
      <li><strong>Gatekeeper</strong> integration — push Constraints + ConstraintTemplates fleet-wide.</li>
    </ul>
    <p><strong>Remediation modes</strong>:
    <ul>
      <li><strong>inform</strong> — Policy reports compliance status only (no enforcement).</li>
      <li><strong>enforce</strong> — RHACM creates / updates resources to bring clusters to desired state.</li>
    </ul>
    <p><strong>PolicySet</strong> = bundle of related Policies + a single Placement.</p>
    <p>Use cases: enforce \"all production clusters must have NetworkPolicy default-deny\"; \"all clusters must have Compliance Operator installed\"; \"all clusters must have RHACS Sensor.\" Centralised governance + per-cluster compliance dashboards.</p>"""),
        Section(eyebrow="Section 1.4 · ObservabilityAddon + HCP at scale + Submariner",
            h2="ObservabilityAddon + Hosted Control Planes at scale + Submariner",
            body_html="""    <p><strong>ObservabilityAddon</strong> — aggregates Prometheus + Grafana metrics from all ManagedClusters into a multi-cluster observability stack on the hub. Built on Thanos. Single console for fleet-wide dashboards + alerting.</p>
    <p><strong>Hosted Control Planes (HCP) at scale via ACM:</strong>
    <ul>
      <li>HCP control planes run as Pods on hosting clusters (could be the hub itself or dedicated HCP-host clusters).</li>
      <li>Workloads (compute) run in target VPCs / on-prem environments — own data plane.</li>
      <li>RHACM Cluster Lifecycle provisions + manages HCP clusters.</li>
      <li><strong>Density</strong>: dozens of clusters per HCP-host cluster vs traditional 3-master per cluster overhead.</li>
    </ul>
    <p><strong>Submariner integration:</strong> RHACM federates Submariner CRs across ManagedClusters → cross-cluster Pod + Service networking. ServiceExport in cluster A makes a Service reachable from cluster B. Foundation for multi-cluster service mesh + DR.</p>
    <p>Use cases: regulated multi-cloud governance; dev / staging / prod fleet alignment via ApplicationSet; multi-region active-active with Submariner; HCP cluster-density at SaaS scale (per-tenant clusters).</p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A platform team manages 30 OCP clusters + 5 EKS + 3 on-prem K8s. They want one place to deploy a NetworkPolicy fleet-wide. Path?",
        options=[("Per-cluster scripts looping kubectl.", False),
            ("RHACM hub registering all 38 clusters as ManagedClusters; create Placement selecting all; ApplicationSet (or Policy) pushing the NetworkPolicy. Reconciled fleet-wide; drift detection.", True),
            ("Migrate everything to one cluster.", False)],
        feedback="RHACM is the multi-cluster governance plane. ManagedCluster + Placement + ApplicationSet (or Policy) handles the fleet-wide rollout; non-OCP clusters register via klusterlet agent.",
    )},
    before_after_before='<p>Pre-RHACM multi-cluster K8s ops = scripts looping kubectl across contexts; per-cluster Argo CD installs; per-cluster Compliance Operator; no fleet-wide observability; cluster provisioning via per-platform installers (Terraform / openshift-install) without coordination.</p>',
    before_after_after='<p>RHACM unifies: <strong>ManagedCluster + Placement</strong> for fleet membership; <strong>ApplicationSet</strong> (Argo CD) for fleet-wide deploys; <strong>Policy + PlacementBinding</strong> for governance; <strong>ObservabilityAddon</strong> for fleet-wide metrics; <strong>HCP at scale</strong> for cluster density; <strong>Submariner</strong> for cross-cluster networking; <strong>Cluster Lifecycle</strong> for provisioning new clusters from templates.</p>',
    before_after_caption='<p class="ba-caption"><em>One pane of glass for fleet ops; same operating model across OCP + EKS + GKE + AKS + on-prem.</em></p>',
    analogy_intro_html='''<p>The <strong>Multi-Foundry Network</strong> is K-Foundry\'s federation hub. RHACM\'s hub cluster sits in the centre; spoke foundries register as <strong>ManagedClusters</strong>. Each spoke runs a <strong>klusterlet agent</strong> that phones home to the hub.</p>
    <p>The <strong>Placement directory</strong> selects spokes by label (\"all production foundries in EU\"). The hub uses Placements to drive: <strong>ApplicationSet</strong> (deploy workloads to selected spokes via Argo CD), <strong>Policy</strong> (enforce governance + compliance), <strong>ObservabilityAddon</strong> (aggregate metrics).</p>
    <p>The <strong>Cluster Lifecycle Operator</strong> can also provision new spokes (HCP-style — control plane Pods in the hub, workers in customer environments — for cluster density at SaaS scale).</p>
    <p><strong>Submariner integration</strong> federates the spoke networks: a Service exported in spoke A becomes addressable from spoke B. Cross-foundry service mesh with no per-cluster DNS choreography.</p>''',
    translation_rows=[("Federation hub", "RHACM hub cluster + multicluster-engine (MCE)"),
        ("Spoke foundry", "ManagedCluster CR (OCP / EKS / GKE / AKS / on-prem)"),
        ("Phone-home agent", "klusterlet agent on each ManagedCluster"),
        ("Spoke selector by label", "Placement CR (ClusterSelector + NumberOfClusters)"),
        ("Spoke selection result", "PlacementDecision CR"),
        ("Fleet-wide app deploy", "ApplicationSet (Argo CD) + cluster generator"),
        ("Older app subscription model", "Channel + Subscription + PlacementRule (legacy)"),
        ("Fleet-wide governance rule", "Policy CR + PlacementBinding"),
        ("Bundle of policies", "PolicySet"),
        ("Inform vs enforce remediation", "Policy spec.remediationAction"),
        ("Fleet-wide metrics dashboard", "ObservabilityAddon (Thanos-based)"),
        ("Cluster-density mgmt", "Hosted Control Planes (HCP) provisioned via Cluster Lifecycle"),
        ("Pre-warmed cluster pool", "ClusterPool — claim cluster from pool"),
        ("Cross-spoke service mesh", "Submariner integration (ServiceExport / ServiceImport)")],
    analogy_stops="A real federation has fixed treaties; RHACM Placements + Policies are software-defined and reshape constantly. Klusterlet agent failure modes (network partition, hub unreachable) are real ops concerns the metaphor doesn\'t capture.",
    eli5="One central hub manages many factories. The hub has a directory of factories, an app-deployer that pushes to selected factories, a rule book everyone follows, and a metrics dashboard showing all factories together.",
    eli10="RHACM hub = central management cluster + MCE Operators. ManagedCluster CR per cluster + klusterlet agent. Placement selects by labels → PlacementDecision. ApplicationSet (Argo CD) deploys apps fleet-wide. Policy + PlacementBinding enforces governance (inform/enforce). ObservabilityAddon = Thanos-based fleet metrics. HCP at scale via Cluster Lifecycle. Submariner integration for cross-cluster networking.",
    scenarios=[
        Scenario(name="Bank — 50 OCP + 10 EKS clusters under one RHACM hub",
            body="A bank registers 60 clusters into RHACM hub. PolicySet enforces: PSA Restricted, NetworkPolicy default-deny, RHACS Sensor installed, OADP backup configured. ApplicationSet deploys central services (ingress, monitoring, log shipper) to all clusters. ObservabilityAddon aggregates metrics. <em>One operations team manages 60 heterogeneous clusters.</em>"),
        Scenario(name="Telco — 800 SNO cell sites federated",
            body="Telco runs OCP at 800 cell sites. Each SNO registered as ManagedCluster. ApplicationSet deploys site-specific 5G workloads + UPF inference. Policy enforces site-specific firewall rules. ObservabilityAddon collects per-site metrics. RHACM Cluster Lifecycle provisions new sites from templates."),
        Scenario(name="SaaS — HCP cluster-per-tenant at scale",
            body="A SaaS gives each enterprise tenant their own OCP cluster. Traditional 3-master-per-cluster = high overhead at 200 tenants. HCP via RHACM: control planes run as Pods inside 4 hosting clusters; tenants get their own data plane in their own VPC. Cluster Lifecycle provisions per tenant on signup. <em>Cluster density at SaaS scale.</em>"),
        Scenario(name="Active-active multi-region with Submariner",
            body="OCP clusters in 3 regions registered to RHACM hub. Submariner integration federates Pod + Service networks. ServiceExport on critical microservices makes them addressable cross-region. Failover routes traffic across regions transparently. <em>Multi-region active-active without per-region DNS gymnastics.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"RHACM only works with OCP clusters.\"",
            truth="RHACM (= upstream Open Cluster Management) supports any conformant K8s cluster: OCP, OKD, ROSA, ARO, OpenShift Dedicated, EKS, GKE, AKS, k3s, kubeadm, etc. Klusterlet agent is the universal hub-spoke bridge."),
        Misconception(myth="\"PolicySet enforce always = RHACM rewrites my workloads.\"",
            truth="PolicySet enforce mode reconciles to the desired state declared in the Policy. <em>Workloads not covered by the Policy are untouched.</em> Inform mode reports compliance only. Use enforce for cluster-config (NetworkPolicy / SCC bindings); use inform for compliance scans."),
        Misconception(myth="\"HCP is just a cost optimization.\"",
            truth="HCP (Hosted Control Planes) reduces per-cluster overhead but also enables cluster density at scale (dozens of clusters per host cluster), faster cluster provisioning (control plane = Pod set, not 3 VMs), and cleaner separation of cluster-mgmt from workload data plane. Cost is one benefit; speed + density + isolation are others."),
    ],
    flashcards=[
        Flashcard(front="What does RHACM manage?", back="Multi-cluster fleet of OCP + non-OCP K8s clusters. Hub cluster + multicluster-engine (MCE) + klusterlet agent per managed cluster. Cluster lifecycle, Apps, Policy, Observability, multi-cluster networking."),
        Flashcard(front="Five RHACM core surfaces?", back="<strong>Cluster Lifecycle</strong> (provision + import), <strong>Application Lifecycle</strong> (ApplicationSet + Subscription), <strong>Governance/Policy</strong>, <strong>Observability</strong> (ObservabilityAddon), <strong>multi-cluster networking</strong> (Submariner integration)."),
        Flashcard(front="What is Placement?", back="CR selecting ManagedClusters by labels (matchLabels / matchExpressions / NumberOfClusters / tolerations). Result: PlacementDecision. Used by ApplicationSet + Policy + ObservabilityAddon."),
        Flashcard(front="ApplicationSet vs Subscription model?", back="<strong>ApplicationSet</strong> (Argo CD-based) is the modern fleet-deploy primitive — generates Application per cluster matching Placement. <strong>Subscription</strong> (Channel + PlacementRule) is the older RHACM model; still works."),
        Flashcard(front="Policy modes?", back="<strong>inform</strong> — report compliance status only (no enforcement). <strong>enforce</strong> — RHACM reconciles cluster to desired state. PolicySet bundles related policies + Placement."),
        Flashcard(front="What is ObservabilityAddon?", back="Aggregates Prometheus + Grafana metrics from all ManagedClusters into a multi-cluster observability stack on the hub. Built on Thanos. Single console for fleet-wide dashboards + alerts."),
        Flashcard(front="Hosted Control Planes (HCP) at scale via RHACM?", back="HCP control planes run as Pods on hosting clusters (often the hub or dedicated HCP-host clusters); data plane workers in target environments. RHACM Cluster Lifecycle provisions HCP clusters. Density: dozens of clusters per host."),
        Flashcard(front="Submariner integration role in RHACM?", back="Federates Pod + Service networks across ManagedClusters. ServiceExport in cluster A → ServiceImport in cluster B → cross-cluster reachability. Foundation for multi-cluster service mesh + DR."),
    ],
    quizzes=[
        Quiz(prompt="A team enables RHACM PolicySet enforce on a NetworkPolicy default-deny across 30 ManagedClusters. Some clusters have existing namespaces without labels matching the Policy\'s namespaceSelector. What happens, and what\'s the fix?",
            answer="The Policy applies only where its namespaceSelector matches. Namespaces without matching labels are skipped — the Policy doesn\'t fail, it just doesn\'t apply. Result: gaps in policy coverage. Fix: (1) Audit namespaces across the fleet for label drift via the Governance dashboard. (2) Apply missing labels via a separate Policy that enforces label presence. (3) Use a more inclusive namespaceSelector if appropriate (e.g., exclude only system namespaces). (4) Periodic compliance scans surface coverage gaps."),
        Quiz(prompt="A SaaS wants to provision 200 tenant clusters on a budget. Walk through HCP via RHACM.",
            answer="(1) RHACM hub cluster + multicluster-engine. (2) Provision 4-5 HCP-host clusters (these are large OCP clusters with capacity to host control-plane Pods for many tenant clusters). (3) Per tenant: RHACM Cluster Lifecycle creates an HCP cluster — control plane runs as Pods on a host cluster; data plane (worker nodes) runs in tenant\'s VPC / cloud account. (4) RHACM imports the new HCP cluster as a ManagedCluster. (5) ApplicationSet deploys baseline services to the new cluster (RHACS Sensor, OADP, observability). (6) Tenant onboarding = git PR + ~5 minutes for provisioning vs hours-to-days for traditional 3-master clusters. (7) Cost: 4-5 host clusters\' worth of control-plane infrastructure for 200 tenant clusters vs 200 × 3 = 600 master VMs."),
        Quiz(prompt="The CTO asks: \"Why do we need RHACM? We have Argo CD already.\" Defend.",
            answer="\"<strong>Argo CD is one piece of fleet management; RHACM bundles five pieces.</strong> Argo CD = ApplicationSet for fleet-wide deploys (RHACM ships managed Argo CD via OpenShift GitOps). RHACM adds: <strong>Cluster Lifecycle</strong> (provision OCP + HCP clusters from templates; import EKS/GKE/AKS/on-prem), <strong>Policy</strong> (enforce governance fleet-wide via PolicySets — CIS, PSA, NetworkPolicy presence), <strong>Observability</strong> (Thanos-based multi-cluster Prometheus aggregation), <strong>Submariner integration</strong> (cross-cluster Pod + Service networking). At our scale (50+ clusters across multiple clouds + on-prem), assembling these from individual OSS pieces would mean operating Cluster API + per-cluster Argo CD + Open Policy Agent + Thanos + Submariner separately. RHACM gives us one Red Hat-supported platform with one operations model. <em>Argo CD alone covers ~20% of fleet ops; RHACM covers all of it.</em>\"",
            cyoa=True, cyoa_tag="how the platform engineer answered the CTO"),
    ],
    glossary=[
        GlossaryItem(name="RHACM (Red Hat Advanced Cluster Management)", definition="Red Hat\'s productized Open Cluster Management. Multi-cluster lifecycle + apps + policy + observability + networking."),
        GlossaryItem(name="Hub cluster", definition="Central RHACM cluster running multicluster-engine (MCE) + RHACM Operators."),
        GlossaryItem(name="ManagedCluster CR", definition="Per-cluster representation in the hub. Klusterlet agent runs on the spoke for hub-spoke communication."),
        GlossaryItem(name="Klusterlet agent", definition="Pod on each ManagedCluster phoning home to the hub. Universal hub-spoke bridge."),
        GlossaryItem(name="Placement", definition="CR selecting ManagedClusters by labels. Result: PlacementDecision."),
        GlossaryItem(name="ClusterPool", definition="Pre-warmed clusters that admins claim when needed. Reduces cluster-provisioning latency."),
        GlossaryItem(name="ApplicationSet", definition="Argo CD CR generating Applications per cluster matching a generator (Cluster / List / Git / Matrix)."),
        GlossaryItem(name="Policy + PlacementBinding", definition="Fleet-wide governance — policy + Placement target via binding. Modes: inform (report) or enforce (reconcile)."),
        GlossaryItem(name="PolicySet", definition="Bundle of related Policies + a single Placement."),
        GlossaryItem(name="ObservabilityAddon", definition="Thanos-based aggregation of Prometheus metrics from all ManagedClusters into the hub. Single console fleet-wide."),
        GlossaryItem(name="Hosted Control Planes (HCP) via ACM", definition="Control planes as Pods on hosting clusters; data plane in target environments. Cluster density at scale."),
        GlossaryItem(name="Submariner integration", definition="Cross-cluster Pod + Service networking. ServiceExport / ServiceImport CRs."),
    ],
    recap_lead='RHACM = hub + ManagedClusters + Placement + ApplicationSet + Policy + ObservabilityAddon + HCP + Submariner. One pane of glass for fleet ops across OCP + non-OCP K8s.',
    recap_next='<strong>Next — O11: OpenShift Observability.</strong> Built-in Cluster Monitoring (Prometheus + Thanos Querier + Alertmanager) + User Workload Monitoring; OpenShift Logging (Loki + Vector); OpenShift Distributed Tracing (Tempo + OpenTelemetry); Network Observability (NetObserv + eBPF); Cluster Observability Operator.',
)
