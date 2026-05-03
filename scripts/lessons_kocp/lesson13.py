"""K-OCP O13 — Capstone (Multi-tenant OCP with ODF + RHACS + GitOps + Pipelines + Virt + RHACM + disconnected)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="K-OCP Capstone — multi-tenant OCP reference foundry with everything.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Grand Opening — the K-OCP reference foundry</text>
  <rect x="40" y="65" width="170" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="125" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Phase A — base</text>
  <text x="125" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">IPI bare-metal or AWS</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">3+5 nodes (HCP for tenants)</text>
  <text x="125" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">OVN-K + Routes + AGC</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">EUS channel + private</text>
  <rect x="225" y="65" width="170" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="310" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Phase B — platform</text>
  <text x="310" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">ODF (block + RWX + S3)</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">SCCs (restricted-v2)</text>
  <text x="310" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">RHACS</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">Logging + Monitoring + Tracing</text>
  <rect x="410" y="65" width="170" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="495" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Phase C — apps + DR</text>
  <text x="495" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">Pipelines (Tekton)</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">GitOps (Argo CD)</text>
  <text x="495" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">Virtualization workload</text>
  <text x="495" y="146" text-anchor="middle" font-size="9" fill="#FFFFFF">OADP + disconnected</text>
  <rect x="595" y="65" width="125" height="125" rx="10" fill="#E8B547" stroke="#3F4A5E"/>
  <text x="657" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#5A4F45">Phase D</text>
  <text x="657" y="103" text-anchor="middle" font-size="9" fill="#5A4F45">defence</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#5A4F45">RHACM federation</text>
  <text x="657" y="135" text-anchor="middle" font-size="9" fill="#5A4F45">live drill</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#5A4F45">must-gather pack</text>
  <text x="657" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#5A4F45">K-OCP-complete</text>
</svg>"""


LESSON = LessonSpec(
    num="13", title_short="capstone foundry",
    title_full="O13 · Capstone — Multi-Tenant OCP Reference Foundry with ODF + RHACS + GitOps + Pipelines + Virt + RHACM",
    title_html="K-OCP O13 · Capstone — Reference Foundry",
    module_eyebrow="Module O13 · the Grand Opening — tie everything together",
    hero_sub_html='<strong>The K-OCP reference foundry.</strong> Multi-tenant OCP (IPI on bare metal or AWS) with <strong>ODF</strong> (block + RWX + S3), <strong>RHACS</strong> (vuln + compliance + runtime + admission), <strong>OpenShift GitOps</strong> (Argo CD), <strong>OpenShift Pipelines</strong> (Tekton), <strong>OpenShift Virtualization</strong> (KubeVirt) workload alongside containers, <strong>RHACM</strong> federation. <strong>Full SCC design</strong> (restricted-v2 default + per-workload escalations). <strong>Disconnected update</strong> via mirror registry + oc-mirror. <strong>must-gather pack</strong> as the diagnostic + DR primitive.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Six months from today. The OCP cluster you\'re about to design will run 80% of revenue: payments, identity, ML inference, sessions — plus a legacy Windows VM workload migrating from VMware. Will it survive an etcd disaster + restore drill? Will the RHACS posture hold? Will the disconnected patch in 6 months take 4 hours or 4 days? Will RHACM federate the new region cluster cleanly? Will the must-gather pack include enough for Red Hat support to triage in the first response? <em>Today\'s lesson: assemble all 12 prior modules into a single defendable design.</em>",
    stamp_html="<strong>Build the four-phase stack: Phase A (IPI base + EUS + private + OVN-K), Phase B (ODF + SCCs + RHACS + observability), Phase C (Pipelines + GitOps + Virtualization + OADP + disconnected), Phase D (RHACM federation + live drill + must-gather pack). Defend it.</strong>",
    district_pin="ko-bay13", district_label="Grand Opening",
    sections=[
        Section(eyebrow="Section 1.1 · Phase A — base cluster", h2="Phase A — IPI base + EUS + private + OVN-K",
            body_html="""    <p><strong>Goal:</strong> a defendable base cluster with no public attack surface, modern networking, EUS-channel stability, and HCP-ready for multi-tenant.</p>
    <ol>
      <li><strong>Installation:</strong> IPI on bare metal (with Redfish-supported hardware) or AWS. 3 master + 5 worker minimum; add ODF storage nodes (3+) on bare metal. Plan for HCP host capacity if multi-tenant cluster-per-customer.</li>
      <li><strong>Channel:</strong> EUS for ~24-month support window. Premium subscription tier.</li>
      <li><strong>Private cluster:</strong> apiserver via private endpoint + master authorized networks; no public LB. SSH disabled (RHCOS default).</li>
      <li><strong>Networking:</strong> OVN-Kubernetes (default); cluster network /14 + service network /16; multi-zonal worker nodes (for cloud) or multi-rack (for bare metal).</li>
      <li><strong>Cluster identity:</strong> least-privilege node SA + per-tenant ServiceAccounts. Workload Identity Federation for Pod-to-cloud (where applicable).</li>
      <li><strong>Maintenance:</strong> EUS upgrade cadence (every 2 years EUS-to-EUS). MachineConfigPool roll discipline. <code>oc adm upgrade</code> with conditional risk assessment.</li>
    </ol>
    <p><em>Phase A success criterion:</em> cluster created via <code>openshift-install</code>; private + EUS; no public IPs in MC_*; <code>oc adm upgrade</code> shows clean upgrade path; etcd backup scheduled.</p>"""),
        Section(eyebrow="Section 1.2 · Phase B — platform", h2="Phase B — ODF + SCCs + RHACS + observability",
            body_html="""    <p><strong>Storage</strong>:
    <ul>
      <li><strong>ODF</strong> on 3-5 dedicated worker nodes with attached storage (NVMe). CephRBD for RWO; CephFS for RWX; NooBaa for object (registry + Prometheus long-term + OADP destination).</li>
      <li>Per-cloud CSI for cloud-installed clusters; ODF for on-prem.</li>
      <li><strong>Internal registry</strong> on NooBaa (zone-resilient).</li>
    </ul>
    <p><strong>Identity + Security</strong>:
    <ul>
      <li><strong>OAuth</strong> integrated with corp OIDC / LDAP; HTPasswd as break-glass.</li>
      <li><strong>OCP RBAC</strong> with least-privilege; Project-scoped admins per tenant.</li>
      <li><strong>SCCs</strong>: restricted-v2 default; only escalate explicitly per workload SA via documented exception process.</li>
      <li><strong>RHACS / StackRox</strong>: deploy Central + Sensor on each ManagedCluster (via RHACM Policy). Vuln + compliance + network graph + runtime + admission.</li>
      <li><strong>Compliance Operator</strong>: weekly CIS + PCI-DSS scans; auto-remediation where applicable.</li>
      <li><strong>Binary Authorization-equivalent</strong>: Cosign-signed images + Policy Controller verify signature at admission.</li>
      <li><strong>FIPS</strong> mode if federal compliance required (install-time choice).</li>
    </ul>
    <p><strong>Observability</strong>:
    <ul>
      <li>Cluster Monitoring (built-in) + UWM for app metrics. Long-term storage to NooBaa S3.</li>
      <li>OpenShift Logging (Loki + Vector); apps / infra / audit streams routed appropriately. Audit stream forwarded to SOC Splunk.</li>
      <li>Distributed Tracing (Tempo + OTel) for app-tier visibility.</li>
      <li>NetObserv (eBPF) for network flow visibility.</li>
      <li><strong>SLO-first alerting</strong>: burn-rate alerts via Prometheus rules; Alertmanager → PagerDuty.</li>
    </ul>
    <p><em>Phase B success criterion:</em> sample app deploys via Pipelines; pulls Secret Manager secret via Workload Identity Federation; serves traffic through Routes; appears in Cluster Monitoring + Logging + Tracing dashboards with burn-rate alert.</p>"""),
        Section(eyebrow="Section 1.3 · Phase C — apps + Virt + DR + disconnected",
            h2="Phase C — Pipelines + GitOps + Virtualization + OADP + disconnected",
            body_html="""    <p><strong>CI/CD</strong>:
    <ul>
      <li><strong>OpenShift Pipelines (Tekton)</strong>: PipelineRun on PR; build via S2I or Docker strategy; output to internal registry; sign with Cosign; tag in ImageStream.</li>
      <li><strong>OpenShift GitOps (Argo CD)</strong>: 3 repos — cluster-config, platform (RHACS, Logging, Monitoring, ODF, MetalLB, etc.), workloads. RootSync + RepoSync. Drift detection on.</li>
      <li>Promotion: Pipeline tags image; Argo CD detects + reconciles to staging; manual gate to prod.</li>
    </ul>
    <p><strong>Virtualization workload</strong>:
    <ul>
      <li>OpenShift Virtualization Operator installed.</li>
      <li>Migration Toolkit for Virtualization (MTV) ingests legacy Windows VMs from vSphere.</li>
      <li>VMs run alongside container workloads; same RBAC + SCCs (anyuid where the VM image needs it); same monitoring + logging.</li>
      <li>Live migration enabled for maintenance drains.</li>
    </ul>
    <p><strong>DR</strong>:
    <ul>
      <li><strong>OADP (Velero-based)</strong>: nightly cluster-wide backup + PV snapshots; cross-region replicated to NooBaa S3 in DR region.</li>
      <li><strong>etcd backup</strong>: scheduled daily + weekly + monthly retention; ship snapshots off-cluster.</li>
      <li>RTO target 60 min for full cluster restore; RPO 24h. <em>Tested quarterly</em> via blue-green cluster restore drill.</li>
    </ul>
    <p><strong>Disconnected update path</strong>:
    <ul>
      <li>Mirror registry (Quay or mirror-registry).</li>
      <li>oc-mirror with ImageSetConfiguration for OCP releases + Operator catalogs.</li>
      <li>Disconnected OSUS Operator for upgrade graph.</li>
      <li>Sneakernet / data-diode procedure documented.</li>
    </ul>
    <p><em>Phase C success criterion:</em> three pull requests can change cluster behaviour; one DR drill restores cluster within RTO; disconnected patch tested end-to-end.</p>"""),
        Section(eyebrow="Section 1.4 · Phase D — RHACM federation + defend + drill", h2="Phase D — RHACM federation + defence + live drill + must-gather pack",
            body_html="""    <p><strong>RHACM federation</strong>:
    <ul>
      <li>RHACM hub cluster (could be the platform cluster or a dedicated mgmt cluster).</li>
      <li>Each tenant cluster registered as ManagedCluster (via klusterlet).</li>
      <li>PolicySet enforces fleet-wide: NetworkPolicy default-deny, RHACS Sensor installed, OADP backup configured, PSA Restricted, Binary Auth attestor.</li>
      <li>ApplicationSet pushes baseline platform services to all clusters.</li>
      <li>ObservabilityAddon aggregates fleet metrics.</li>
      <li>HCP Cluster Lifecycle for cluster-density at scale (per-tenant clusters via HCP).</li>
    </ul>
    <p><strong>Architecture defence</strong> (60 min, with senior platform reviewer):</p>
    <ol>
      <li>Walk the network diagram — VPC, subnets, OVN-K CIDRs, Routes / AGC, MetalLB BGP.</li>
      <li>Walk the identity diagram — OAuth IDP, OCP RBAC + Project-scoped admins, SCC matrix per workload.</li>
      <li>Walk the storage diagram — ODF Ceph topology, NooBaa S3 destinations (registry, monitoring, OADP), CephFS RWX usage.</li>
      <li>Walk the security stack — Compliance Operator scans + history, RHACS posture + runtime + admission, Cosign signing pipeline.</li>
      <li>Walk the observability diagram — three pipes (metrics + logs + traces) + NetObserv + COO; SLOs + burn-rate alerts; on-call playbook.</li>
      <li>Walk the upgrade runbook — EUS channel, MCP roll discipline, surge upgrade, blue-green node-pool fallback, disconnected mirror.</li>
      <li>Walk the DR runbook — OADP schedule, etcd backup schedule, restore steps, RTO/RPO, drill cadence.</li>
      <li>Walk the AI / Virt workload runbook — KubeVirt VM lifecycle, KServe inference, MTV migration plan.</li>
    </ol>
    <p><strong>Live drill</strong> (90 min):</p>
    <ul>
      <li>Reviewer kills a worker node. MCO + MachineSet replace; workloads re-schedule; ODF rebalances; CO\'s stay Available.</li>
      <li>Reviewer revokes an OCP RBAC binding for an SA. Pod throws 403; Audit Logs + Logs Explorer surface; restore + postmortem in 15 min.</li>
      <li>Reviewer applies a critical CTD finding. RHACS triage → admission policy hardening → PolicySet update via RHACM.</li>
      <li>Reviewer initiates DR scenario: restore latest OADP backup into a sibling cluster within RTO. Validate workloads.</li>
      <li>Reviewer simulates 10× inference burst. KServe scales; ODF + Prometheus storage hold; SLO maintained.</li>
      <li>Reviewer simulates etcd quorum loss. Documented disaster-recovery procedure restores from snapshot.</li>
    </ul>
    <p><strong>must-gather pack:</strong> standard <code>oc adm must-gather</code> + targeted gathers (Logging, Tracing, NetObserv, ODF, RHACS, OADP, RHACM, Virtualization). Pre-canned bundle for first-response support cases.</p>
    <p><em>K-OCP-complete</em>: Bicep / Terraform / OpenShift install configs + per-cluster Markdown architecture doc + DR runbook + AI runbook + Virt runbook + must-gather pack + live-drill recording.</p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="Why use ODF + NooBaa S3 for the internal registry?",
        options=[("ODF is cheaper.", False),
            ("NooBaa-backed S3 is zone-resilient (registry survives Pod migration); single-zone EBS / Azure Disk / GCE PD pin the registry to one zone — Pod can\'t migrate cross-zone without registry being unavailable.", True),
            ("It\'s required.", False)],
        feedback="Registry on object storage = zone-resilient. PVC-backed registry has the cross-zone-attach failure mode.",
    )},
    before_after_before='<p>Pre-K-OCP-curriculum operators built OCP clusters one feature at a time: install IPI, then add Logging Operator manually, then ODF without planning storage topology, then RHACS as an afterthought, then GitOps installed via Helm-instead-of-Operator, no etcd backup schedule, no disconnected mirror, no must-gather pack, no DR drill. <em>Tribal knowledge in three engineers\' heads.</em></p>',
    before_after_after='<p>The K-OCP reference foundry is <strong>defendable</strong>: every choice justified, every alternative considered, every failure mode mapped. <em>IPI + EUS + private + OVN-K</em> for base; <em>ODF + SCCs + RHACS + observability</em> for platform; <em>Pipelines + GitOps + Virt + OADP + disconnected</em> for ops; <em>RHACM federation + defence + drill + must-gather</em> for confidence. A new operator can read the architecture doc, run the runbooks, and operate the cluster.</p>',
    before_after_caption='<p class="ba-caption"><em>You can\'t cargo-cult a reference foundry from the internet — you have to walk every choice yourself. K-OCP Capstone is that walk, defended.</em></p>',
    analogy_intro_html='''<p>The <strong>Grand Opening</strong> at K-Foundry is the graduation event. Today you\'re the candidate. Four phases.</p>
    <p><strong>Phase A — your base foundry</strong> (IPI + EUS + private + OVN-K). Foundation poured: 3 control nodes + workers + ODF storage; private apiserver; long-term-lease subscription (EUS); modern networking with Routes + AGC.</p>
    <p><strong>Phase B — your services</strong> (ODF + SCCs + RHACS + observability). Inventory warehouse stocked (ODF block + RWX + S3); Safety Office staffed (SCCs default-restricted-v2 + RHACS + Compliance + Cosign); Control Tower running (Cluster Monitoring + Logging + Tracing + NetObserv).</p>
    <p><strong>Phase C — your governance + AI/Virt</strong> (Pipelines + GitOps + Virtualization + DR). Mold Shop running (Pipelines for CI; GitOps for CD); Special Castings Wing alive (KubeVirt VMs migrated from VMware via MTV alongside containers); DR plan (OADP + etcd backup) rehearsed; disconnected update procedure documented.</p>
    <p><strong>Phase D — your federation + defence</strong> (RHACM + drill). Multi-Foundry Network ties tenant clusters together (RHACM hub + ManagedClusters + PolicySet + ApplicationSet + ObservabilityAddon); senior gardener walks your foundry, runs an unannounced drill (node kill, RBAC revoke, CTD finding, DR restore, etcd quorum loss). <em>Survive the drill, you graduate.</em></p>''',
    translation_rows=[("Phase A — base foundry", "IPI + EUS + private + OVN-K + 3+5 nodes + ODF storage nodes"),
        ("Long-term lease", "EUS channel"),
        ("Phase B — services", "ODF + SCCs + RHACS + Cluster Monitoring + Logging + Tracing + NetObserv"),
        ("Inventory warehouse", "ODF (Ceph + NooBaa)"),
        ("Safety Office", "SCCs + RHACS + Compliance Operator"),
        ("Control Tower", "Cluster Monitoring + Logging + Tracing + NetObserv"),
        ("Phase C — apps + Virt + DR", "Pipelines + GitOps + Virtualization (MTV) + OADP + disconnected mirror"),
        ("Mold Shop", "Pipelines (Tekton) + GitOps (Argo CD)"),
        ("Special Castings Wing", "OpenShift Virtualization (KubeVirt) + MTV migration"),
        ("Disaster-Relief Vault", "OADP + etcd backup + DR drill"),
        ("Phase D — federation + drill", "RHACM hub + ManagedClusters + PolicySet + ApplicationSet + must-gather pack"),
        ("Multi-Foundry Network", "RHACM federation"),
        ("Live drill", "Recover from chaos events using runbooks"),
        ("Graduation diploma", "K-OCP-complete: install configs + arch docs + DR runbook + AI/Virt runbook + must-gather pack + drill recording")],
    analogy_stops="A real Grand Opening is a one-time event; the K-OCP capstone\'s value is reusable artifacts (install configs, runbooks, drill scripts) so the next operator can graduate themselves.",
    eli5="To graduate from K-Foundry you build a base foundry, stock it with shelves + safety + monitoring, set up the production lines + DR plan, then federate to other foundries. The senior gardener walks through and tries to break things; you fix them on the spot.",
    eli10="K-OCP reference foundry: Phase A (IPI + EUS + private + OVN-K base). Phase B (ODF + SCCs + RHACS + Cluster Monitoring + Logging + Tracing). Phase C (Pipelines + GitOps + Virtualization with MTV + OADP + disconnected). Phase D (RHACM federation + live drill + must-gather pack). Deliverables: install configs + arch doc + DR runbook + AI/Virt runbook + must-gather pack + drill recording.",
    scenarios=[
        Scenario(name="Bank — full reference foundry as platform standard",
            body="A regulated bank adopts K-OCP reference foundry as the standard. IPI bare-metal install configs in git; per-cluster Markdown arch docs; defence + drill required before any new cluster goes prod. <em>Onboarding new clusters: 4 hours including drill, vs 6 weeks ad-hoc.</em>"),
        Scenario(name="VMware migration — 200 VMs to OCP Virtualization in 6 months",
            body="Bank migrates 200 legacy VMs from vSphere to OCP via MTV. VMs run alongside containers under one RBAC, one observability, one DR. Phased migration: dev VMs first (1 month), staging VMs (2 months), prod VMs (3 months). <em>VMware contract not renewed; ~$2M annual savings.</em>"),
        Scenario(name="Multi-tenant SaaS — HCP per tenant via RHACM",
            body="A SaaS gives each enterprise customer their own OCP cluster. RHACM Cluster Lifecycle provisions HCP clusters on signup; control planes pack densely on host clusters; data planes in customer accounts. ApplicationSet deploys baseline (RHACS Sensor, OADP, observability) per cluster. <em>Cluster-per-tenant operationalisable at SaaS scale.</em>"),
        Scenario(name="Live drill — etcd quorum loss recovered in 47 min",
            body="During quarterly drill, reviewer simulates etcd quorum loss on a sibling cluster. Documented procedure: restore from latest etcd snapshot to one master; cluster operators reconcile; re-add other masters. <em>47 min total; auditor satisfied with RTO; runbook validated.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"OCP gives me everything; I don\'t need to design.\"",
            truth="OCP gives a coherent platform. It does <em>not</em> design your network, your identity model, your tenant boundaries, your DR strategy, your egress posture, your SCC matrix, or your governance. The capstone exists because you still own those decisions — OCP frees you to focus on them."),
        Misconception(myth="\"I can copy the reference foundry from the internet and skip the defence.\"",
            truth="The defence + drill aren\'t bureaucracy — they\'re where you discover that the copied design doesn\'t match your network, your tenant model, your compliance, or your team\'s on-call topology. <em>The foundry you can defend is the only foundry you should run.</em>"),
        Misconception(myth="\"DR drills are over-engineering.\"",
            truth="A startup can lose its company to a single 3 AM event. The drill cost (one engineer half-day per quarter) is a fraction of one outage. Even a basic OADP restore on a non-prod cluster surfaces the assumptions that would cost a week during a real incident."),
    ],
    flashcards=[
        Flashcard(front="Four phases of the K-OCP capstone?", back="<strong>Phase A</strong> base (IPI + EUS + private + OVN-K). <strong>Phase B</strong> platform (ODF + SCCs + RHACS + Monitoring + Logging + Tracing). <strong>Phase C</strong> apps + Virt + DR (Pipelines + GitOps + Virtualization with MTV + OADP + disconnected). <strong>Phase D</strong> RHACM federation + defence + live drill."),
        Flashcard(front="What does \"defendable\" mean for the reference foundry?", back="Every architectural choice can be justified by trade-offs the operator can articulate to a peer reviewer."),
        Flashcard(front="Three Argo CD repos in the GitOps layout?", back="<strong>cluster-config</strong> (RootSync seed), <strong>platform</strong> (RHACS, Logging, Monitoring, ODF, MetalLB, etc.), <strong>workloads</strong> (per-tenant or per-team apps)."),
        Flashcard(front="Six chaos events in the live drill?", back="(1) Kill node — MCO + MachineSet replace. (2) Revoke RBAC binding — 403, Audit Log surfaces, fix. (3) CTD finding — RHACS triage + admission hardening. (4) DR restore — OADP into sibling cluster. (5) 10× inference burst — KServe scales + SLO maintained. (6) etcd quorum loss — documented restore procedure."),
        Flashcard(front="Why include OCP Virtualization in the capstone?", back="Most enterprise migrations to OCP include legacy VM workloads. KubeVirt + MTV give a unified container + VM platform — VMs run alongside containers under one RBAC, observability, DR. Removes the \"two control planes\" problem."),
        Flashcard(front="Why include RHACM in the capstone?", back="Enterprise OCP rarely lives in isolation — multi-cluster fleet (regions, environments, tenants) needs unified policy + apps + observability. RHACM is the multi-cluster governance plane; assemble alternative (per-cluster Argo CD + OPA + custom telemetry aggregation) is too much for the value."),
        Flashcard(front="What makes the upgrade runbook safe?", back="EUS channel + planned maintenance + MachineConfigPool roll discipline + tunable max-surge + PDB-tested workloads + blue-green node-pool fallback for high-stakes + disconnected mirror procedure for air-gapped."),
        Flashcard(front="What does \"K-OCP-complete\" mean as a deliverable?", back="install configs (openshift-install or Bicep/Terraform) + per-cluster architecture Markdown + DR runbook + AI/Virt runbook + must-gather pack + live-drill recording. A successor operator can read the docs, run the runbooks, and operate the cluster without you."),
    ],
    quizzes=[
        Quiz(prompt="The peer reviewer asks: \"Why did you pick IPI + EUS over UPI + Regular channel?\" Defend.",
            answer="\"<strong>IPI</strong>: handles all infra provisioning (VMs, network, LB, DNS) — minutes from openshift-install to working cluster vs days for UPI. We don\'t need UPI\'s flexibility for our standard cloud / supported-bare-metal install. <strong>EUS</strong>: 24-month support for designated minor versions; avoids quarterly minor upgrades for a regulated workload. We accept being slightly behind latest features in exchange for predictable change-control. <strong>Trade-offs accepted:</strong> Regular channel gets newer features faster; UPI fits non-standard infra. For our standard prod path, IPI + EUS is right; we have a separate Regular-channel cluster for canary."),
        Quiz(prompt="During the live drill the reviewer revokes an OCP RBAC binding for an SA. Pod 403s. Walk through the response under 15 minutes.",
            answer="(1) AMG dashboard fires red within seconds (Pod returns 5xx). PagerDuty via Action Group. (2) Open AMG; confirm failing service via RED dashboard. (3) Open Logs Explorer with saved query for kube-audit; filter to past 30 min; find the RoleBinding deletion event with timestamp + initiator. (4) Re-create RoleBinding via <code>oc adm policy add-role-to-user</code> (from git source-of-truth, not free-hand). (5) Pod\'s next call succeeds. (6) Postmortem note: this kind of reverted change should have been blocked by Policy Controller / GitOps drift detection — file improvement to require all RBAC changes via git PR + ArgoCD reconcile."),
        Quiz(prompt="The CTO asks: \"Why are we paying for OCP + ODF + RHACS + RHACM all on top of vanilla K8s? That\'s a lot of zeros.\" Final defence.",
            answer="\"<strong>Each piece replaces something we\'d otherwise build + operate ourselves with Red Hat support attached.</strong> <strong>OCP</strong>: Routes + SCCs + integrated OAuth + registry + console + OperatorHub-everywhere — replaces 8+ self-installed Helm charts. <strong>ODF</strong>: software-defined storage with RWX + S3 — replaces NFS server + S3 service + block storage assembly. <strong>RHACS</strong>: vuln + compliance + runtime + admission in one — replaces Anchore + Falco + custom OPA + manual compliance scans. <strong>RHACM</strong>: multi-cluster apps + policy + observability — replaces per-cluster Argo CD + OPA + custom Thanos federation. <em>Operationally:</em> one vendor accountable for the whole stack; consistent upgrade story (CVO + EUS); single support contract. <em>Financially:</em> OCP + ODF + RHACS + RHACM at our scale (50 clusters, multi-cloud + on-prem) costs roughly the same as one platform engineer\'s annual salary — and it eliminates the need for 6+ platform engineers operating the assembled-from-OSS equivalent. <em>Worth every dollar at our complexity.</em>\"",
            cyoa=True, cyoa_tag="how the platform engineer answered the CTO"),
    ],
    glossary=[
        GlossaryItem(name="K-OCP reference foundry", definition="The opinionated production OCP topology the K-OCP capstone defends: IPI + EUS + private + OVN-K + ODF + SCCs + RHACS + GitOps + Pipelines + Virtualization + RHACM + OADP + disconnected."),
        GlossaryItem(name="Phase A / B / C / D", definition="Capstone build phases: Base / Platform / Apps + Virt + DR / RHACM + Defence-and-drill."),
        GlossaryItem(name="Defendable", definition="Every architectural choice can be justified by trade-offs the operator articulates to a peer reviewer."),
        GlossaryItem(name="Live drill", definition="Reviewer-led chaos exercise: node kill, RBAC revoke, CTD finding, DR restore, inference burst, etcd quorum loss. Validates the runbooks."),
        GlossaryItem(name="K-OCP-complete", definition="Capstone deliverable: install configs + per-cluster arch doc + DR runbook + AI/Virt runbook + must-gather pack + drill recording."),
        GlossaryItem(name="must-gather pack", definition="Pre-canned bundle of standard + targeted must-gather commands per Operator. For first-response support cases."),
        GlossaryItem(name="Three GitOps repos", definition="cluster-config (Fleet seed), platform (RHACS, Logging, Monitoring, ODF, MetalLB), workloads (per-tenant)."),
        GlossaryItem(name="DR drill cadence", definition="Quarterly OADP restore + etcd quorum-loss simulation on dev / sibling clusters. Updates runbook with deltas."),
        GlossaryItem(name="EUS line item justification", definition="24-month support window saves quarterly upgrade burden for regulated workloads — engineering-time saving > Premium-tier subscription cost."),
        GlossaryItem(name="HCP density (capstone)", definition="Per-tenant HCP clusters via RHACM Cluster Lifecycle for SaaS-scale tenancy."),
        GlossaryItem(name="MTV migration plan", definition="Migration Toolkit for Virtualization batch ingest plan from vSphere → KubeVirt VMs. Phased: dev first, staging, prod."),
        GlossaryItem(name="Disconnected pack", definition="oc-mirror + ImageSetConfiguration + sneakernet procedure + disconnected OSUS Operator. For air-gapped patches."),
    ],
    recap_lead='K-OCP Capstone built. Phase A (base) → Phase B (platform) → Phase C (apps + Virt + DR) → Phase D (RHACM + defended + drilled). The reference foundry is your starting template for any new prod OCP deployment.',
    recap_next='<strong>K-OCP curriculum complete.</strong> You can architect, install, network, secure, manage Operators, build + ship workloads, store, operate, run VMs + AI + edge, federate multi-cluster, observe, troubleshoot, and defend a production OCP deployment end-to-end. Next paths: K-COM (deepen K8s itself) · K-VAN (operate K8s yourself, off-cloud) · K-EKS / K-AKS / K-GKE (managed-cloud counterparts) · or build internal training rolling K-OCP into your org\'s onboarding.',
)
