"""K-AKS A11 — Capstone (Private AKS Automatic, Cilium, WI, AGC, Defender, AMP/AMG, Flux, LTS, DR)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="K-AKS capstone — private AKS Automatic + the full reference stack.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Commencement Hall — the K-AKS reference stack</text>
  <rect x="50" y="60" width="180" height="130" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="140" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Phase A — base</text>
  <text x="140" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6">Private AKS Automatic</text>
  <text x="140" y="115" text-anchor="middle" font-size="9" fill="#FBF1D6">API VNet Integration</text>
  <text x="140" y="130" text-anchor="middle" font-size="9" fill="#FBF1D6">Azure CNI + Cilium</text>
  <text x="140" y="145" text-anchor="middle" font-size="9" fill="#FBF1D6">NAP for nodes</text>
  <text x="140" y="160" text-anchor="middle" font-size="9" fill="#FBF1D6">Premium tier (LTS)</text>
  <rect x="245" y="60" width="180" height="130" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="335" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Phase B — platform</text>
  <text x="335" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Workload Identity</text>
  <text x="335" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">AGC (Gateway API)</text>
  <text x="335" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">Disks + Files + KV CSI</text>
  <text x="335" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">Container Insights</text>
  <text x="335" y="160" text-anchor="middle" font-size="9" fill="#FFFFFF">AMP + AMG</text>
  <rect x="440" y="60" width="180" height="130" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="530" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Phase C — ops &amp; DR</text>
  <text x="530" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Defender for Containers</text>
  <text x="530" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">Azure Policy (Gatekeeper)</text>
  <text x="530" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">Flux v2 GitOps</text>
  <text x="530" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">Velero / Backup for AKS</text>
  <text x="530" y="160" text-anchor="middle" font-size="9" fill="#FFFFFF">LTS + blue-green runbook</text>
  <rect x="635" y="60" width="75" height="130" rx="10" fill="#E8B547" stroke="#3F4A5E"/>
  <text x="673" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">Phase D</text>
  <text x="673" y="100" text-anchor="middle" font-size="9" fill="#5A4F45">defence</text>
  <text x="673" y="115" text-anchor="middle" font-size="9" fill="#5A4F45">peer review</text>
  <text x="673" y="135" text-anchor="middle" font-size="9" fill="#5A4F45">live drill</text>
  <text x="673" y="150" text-anchor="middle" font-size="9" fill="#5A4F45">recovery</text>
  <text x="673" y="170" text-anchor="middle" font-size="8" font-style="italic" fill="#5A4F45">K-AKS-complete</text>
</svg>"""


LESSON = LessonSpec(
    num="11",
    title_short="capstone campus",
    title_full="A11 · Capstone — Private AKS Automatic Reference Campus with Everything",
    title_html="K-AKS A11 · Capstone — Reference Stack",
    module_eyebrow="Module A11 · Commencement Hall — tie everything together",
    hero_sub_html='<strong>The K-AKS reference stack.</strong> Private AKS Automatic + API VNet Integration + Azure CNI Powered by Cilium + Node Auto Provisioning + Workload Identity + AGC (Gateway API) + Disks + Files + Key Vault CSI + Container Insights + AMP + AMG + Defender for Containers + Azure Policy (Gatekeeper-Restricted) + Flux v2 GitOps + Velero / Backup for AKS + LTS on Premium tier + blue-green upgrade + DR runbooks. <em>Build it; defend it; drill it.</em>',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Six months from today. The cluster you\'re about to design will be running 80% of revenue — payments, identity, ML, sessions. Will it survive a region-failure drill? Will the LTS migration in 18 months be uneventful? Will the next pen-test report come back clean? Will tenant-A\'s noisy job kill tenant-B\'s SLA? <em>Today\'s lesson: assemble all 10 prior modules into a single defendable design.</em>",
    stamp_html="<strong>Build the four-phase stack: Phase A (private AKS Automatic + Cilium + NAP + LTS), Phase B (WI + AGC + storage + observability), Phase C (Defender + Policy + Flux + Velero + blue-green runbook), Phase D (peer review + live DR drill). Defend it.</strong>",
    district_pin="kc-wing11",
    district_label="Commencement Hall",
    sections=[
        Section(
            eyebrow="Section 1.1 · Phase A — base cluster",
            h2="Phase A — private AKS Automatic on Premium tier",
            body_html="""    <p><strong>Goal:</strong> a defendable base cluster with no public attack surface, modern networking, and an upgrade path measured in years.</p>
    <ol>
      <li><strong>AKS Automatic</strong> on <strong>Premium tier</strong> — preconfigures Container Insights, AMP, AMG, Workload Identity, Azure RBAC for K8s, NAP, KEDA, VPA, image cleaner, auto-upgrade, Cilium NetworkPolicy. Premium tier enables LTS subscription.</li>
      <li><strong>Private cluster</strong> via <strong>API Server VNet Integration</strong> — apiserver is in your hub VNet; no public endpoint. Authorized IP ranges as belt-and-braces if the org policy demands.</li>
      <li><strong>Azure CNI Powered by Cilium</strong> in Overlay mode — Pods on overlay CIDR; nodes in VNet; eBPF dataplane; L4 + L7 NetworkPolicy + Hubble flow visibility.</li>
      <li><strong>Node Auto Provisioning (NAP)</strong> for compute — Azure picks SKU + zones; auto-consolidation; one less ops burden.</li>
      <li><strong>NAT Gateway</strong> for outbound — no LB-shared SNAT; predictable scaling; multi-IP for SNAT capacity.</li>
      <li><strong>Multi-AZ</strong> — pool zones {1,2,3}; Pod topology-spread constraints for even distribution.</li>
    </ol>
    <p><em>Phase A success criterion:</em> cluster created via Bicep / Terraform; <code>kubectl</code> works only via Entra-integrated kubeconfig; no public IPs in MC_*.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Phase B — platform layer",
            h2="Phase B — identity, ingress, storage, observability",
            body_html="""    <p><strong>Identity</strong>: <strong>Workload Identity</strong> wired per workload (no long-lived secrets). User-assigned MIs scoped narrowly per service. <strong>Azure RBAC for K8s</strong> with <em>local accounts disabled</em>. Break-glass Entra group with PIM. Conditional Access requiring MFA + compliant device.</p>
    <p><strong>Ingress</strong>: <strong>Application Gateway for Containers (AGC)</strong> in private mode + Gateway API. HTTPRoutes managed by service teams; default-deny ingress NetworkPolicy.</p>
    <p><strong>Storage</strong>: Premium SSD v2 default StorageClass with <code>WaitForFirstConsumer</code>; Azure Files CSI for RWX shared logs / assets; <strong>Secrets Store CSI</strong> with Azure Key Vault provider, WI-authenticated, rotation-poller enabled.</p>
    <p><strong>Observability</strong>: <strong>Container Insights</strong> (AKS-aware metrics+logs into Log Analytics) + <strong>AMP</strong> (managed Prometheus, scrape per service) + <strong>AMG</strong> (managed Grafana, RED dashboards per service joining AMP + Container Insights + App Insights). Apiserver + audit + audit-admin diagnostic settings → Log Analytics. Action Group → PagerDuty.</p>
    <p><em>Phase B success criterion:</em> a sample app deploys via kubectl; pulls a Key Vault secret via WI; serves traffic through AGC; appears in AMG with RED panels and an alert rule.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Phase C — security, GitOps, DR, upgrade",
            h2="Phase C — Defender, Policy, GitOps, Velero, LTS runbook",
            body_html="""    <p><strong>Security</strong>: <strong>Microsoft Defender for Containers</strong> (image scan + posture + runtime). <strong>Azure Policy for AKS</strong> with the <em>restricted</em> baseline. <strong>PSA Restricted</strong> per namespace. <strong>Image Cleaner</strong> on critical-severity threshold. <strong>Azure Firewall</strong> egress with FQDN allow-list. Cosign / Notation signing on critical images; admission verifier blocks unsigned.</p>
    <p><strong>GitOps</strong>: <strong>Flux v2 add-on</strong>. Three repos: <em>cluster-config</em> (Flux\'s own seed), <em>platform</em> (Container Insights config, AGC, MI/role assignments), <em>workloads</em> (per-tenant or per-team apps). Drift detection on; manual interventions reverted by reconcile loop.</p>
    <p><strong>DR</strong>: <strong>Velero</strong> (or Azure Backup for AKS) — daily cluster-wide backup to a geo-redundant Storage Account. RTO target 60 min for full cluster restore; RPO 24 hours. <em>Tested quarterly</em> via blue-green cluster restore drill.</p>
    <p><strong>Upgrade runbook</strong>: <strong>LTS</strong> on the chosen minor (e.g. v1.30 LTS) for 2-year stability. Pre-flight with <strong>kubent</strong> + <strong>Pluto</strong> against git + cluster. Maintenance window Sundays 02-06 UTC. <strong>Blue-green node pool migration</strong> for high-stakes upgrades. Cluster blue-green held in reserve for major LTS-to-LTS jumps.</p>
    <p><em>Phase C success criterion:</em> three pull requests can change cluster behaviour; one pen-test exercise passes Defender + admission policies; one DR drill restores within RTO.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · Phase D — defend it, drill it",
            h2="Phase D — defend, drill, deliver",
            body_html="""    <p>You don\'t finish K-AKS by handing in a Bicep file. You finish by <strong>defending it</strong> in front of a peer panel and surviving a <strong>live drill</strong>.</p>
    <p><strong>Architecture defence</strong> (60 minutes, with senior platform reviewer):</p>
    <ol>
      <li>Walk the network diagram — VNet, subnets, NSG, AGC, NAT Gateway, Private Endpoint to ACR + Key Vault.</li>
      <li>Walk the identity diagram — Entra app + MI per workload + federated credentials, break-glass Entra group + PIM.</li>
      <li>Walk the storage diagram — StorageClass defaults, ZRS for stateful, snapshot policy.</li>
      <li>Walk the observability diagram — three pipes into AMG, alert routing, on-call playbook.</li>
      <li>Walk the upgrade runbook — LTS rationale, pre-flight, surge, blue-green fallback.</li>
      <li>Walk the DR runbook — Velero schedule, restore steps, RTO/RPO targets, drill cadence.</li>
    </ol>
    <p><strong>Live drill</strong> (90 minutes):</p>
    <ul>
      <li>The reviewer kills a node. NAP replaces; workloads re-schedule; AMG dashboards stay green.</li>
      <li>The reviewer revokes a Workload Identity MI role. Pod throws 401; KQL on AKS audit logs locates the change in Activity Log; fix and re-run within 15 min.</li>
      <li>The reviewer applies a high-severity Defender finding. You walk the response: Defender alert → triage → remediation → admission policy hardening.</li>
      <li>The reviewer initiates a DR scenario: restore last night\'s Velero backup into a sibling cluster; verify workloads come up; document deltas.</li>
    </ul>
    <p><em>K-AKS-complete</em>: Bicep + per-cluster Markdown architecture doc + DR runbook + live-drill recording. <em>You can hand this to a successor and they can run it.</em></p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="In your reference stack, why is API Server VNet Integration preferred over private cluster + Private Link?",
            options=[
                ("Private Link is deprecated.", False),
                ("API Server VNet Integration injects the apiserver into a delegated subnet of your VNet — no Private Link / Private DNS hub-spoke complexity, direct VNet routing, simpler network topology.", True),
                ("Both are identical.", False),
            ],
            feedback="VNet Integration is the modern, simpler topology for new private clusters; existing Private-Link clusters keep working but VNet Integration is recommended going forward.",
        ),
    },
    before_after_before='<p>Pre-K-AKS-curriculum operators built AKS clusters one feature at a time, learning each surface only when it failed. Six months in: a half-Modern, half-Legacy cluster with mixed identity (some service principal, some MI, some WI), bring-your-own observability stack, no Defender, an Ingress controller installed by Helm, no GitOps, no DR drill, no upgrade plan, no LTS. <em>Tribal knowledge in three engineers\' heads.</em></p>',
    before_after_after='<p>The K-AKS reference stack is <strong>defendable</strong>: every choice is justified, every alternative considered, every failure mode mapped to a runbook. <em>Private AKS Automatic + Cilium + NAP + LTS</em> for base; <em>WI + AGC + storage + observability</em> for platform; <em>Defender + Policy + Flux + Velero + blue-green</em> for ops; <em>defence + drill</em> for confidence. A new operator can read the architecture doc, run the runbook, and operate the cluster.</p>',
    before_after_caption='<p class="ba-caption"><em>You can\'t cargo-cult a reference stack from the internet — you have to walk every choice yourself. K-AKS Capstone is that walk, defended.</em></p>',
    analogy_intro_html='''<p>The <strong>Commencement Hall</strong> is where students graduate from K-Campus. Today you\'re the candidate. Four phases of the ceremony:</p>
    <p><strong>Phase A — your dorm building</strong> (base cluster). You designed and built it: doors that lock the right way, plumbing that drains the right way, a back exit (NAT Gateway) sized for finals week. Foundation: solid.</p>
    <p><strong>Phase B — your services</strong> (platform). You hired the registrar (Workload Identity), hired the front-desk concierge (AGC), built the library wing (storage), installed the bell tower (observability). Operations: humming.</p>
    <p><strong>Phase C — your governance</strong> (security + GitOps + DR + upgrade). Campus Police on every shift, the daily Git reconciler running, the disaster-relief plan rehearsed, the long-term lease (LTS) signed. Resilience: rehearsed.</p>
    <p><strong>Phase D — your defence</strong> (peer review + live drill). The senior dean walks your campus, asks questions, fires alarms — you respond from the runbooks. <em>If you survive an unannounced drill, you graduate.</em></p>''',
    translation_rows=[
        ("Phase A — dorm building", "Private AKS Automatic + Cilium + NAP"),
        ("Back exit sized for finals", "NAT Gateway for outbound"),
        ("Apiserver in your own basement", "API Server VNet Integration"),
        ("Phase B — services", "WI + AGC + Storage + AMP/AMG/Container Insights"),
        ("Concierge with preloaded manifest", "AGC + Gateway API"),
        ("Bell tower with three bells", "Three signal pipes (metrics + logs + traces) → AMG"),
        ("Phase C — governance", "Defender + Policy + Flux + Velero + LTS"),
        ("Daily Git reconciler", "Flux v2 add-on (App-of-Apps style)"),
        ("Disaster-relief plan", "Velero / Backup for AKS + DR runbook"),
        ("Long-term lease", "LTS on Premium tier"),
        ("Phase D — defence", "Architecture review + live drill"),
        ("Survive the dean\'s alarms", "Recover from chaos events using runbooks"),
        ("Graduation certificate", "K-AKS-complete: Bicep + arch doc + DR runbook + drill recording"),
    ],
    analogy_stops="A real campus graduation is a one-time ceremony; the K-AKS capstone\'s value is that the artifacts (Bicep, runbooks, drill scripts) are reusable next time around — and the next operator can graduate themselves.",
    eli5="To graduate from K-Campus you build a small dorm, hire your services, set up your governance, then the dean walks through and tries to break things. You fix them on the spot. If you can do all four, you\'re done.",
    eli10="The K-AKS reference stack: Phase A (private AKS Automatic + Cilium + NAP + Premium tier with LTS). Phase B (Workload Identity + AGC + Disks/Files + Key Vault CSI + Container Insights + AMP + AMG). Phase C (Defender for Containers + Azure Policy Restricted + Flux v2 GitOps + Velero/Backup for AKS + blue-green upgrade runbook). Phase D (architecture defence + live chaos drill: node kill, MI revoke, Defender finding, DR restore). Deliverables: Bicep + arch doc + DR runbook + drill recording.",
    scenarios=[
        Scenario(
            name="SaaS — full reference stack as the new platform-team standard",
            body="A SaaS platform team adopts K-AKS reference stack as the standard for all new prod clusters. Bicep modules version-pinned in a shared repo. Per-tenant cluster shapes only diverge on size + region. Defence + drill required before any new cluster goes prod. <em>Onboarding new clusters: 4 hours including drill, vs 6 weeks ad-hoc previously.</em>",
        ),
        Scenario(
            name="Bank — regulated workload on the LTS variant",
            body="A bank\'s payments cluster: full K-AKS stack but pinned to v1.27 LTS for 9-month compliance change-control. AGC in private mode; Confidential Containers pool for one PII subsystem; Azure Firewall Premium with TLS inspection on egress. Quarterly DR drill includes a hypothetical Azure-region-failure scenario; cluster restored into paired region in 53 minutes. <em>Audit clean.</em>",
        ),
        Scenario(
            name="Dev experience — Flux + GitHub Actions = instant new namespace",
            body="A dev team spins up a new app: PR to <em>workloads/</em> repo with new Kustomization → Flux reconciles → AGC HTTPRoute provisioned → AMG dashboard auto-generated from Helm chart annotations → on-call rota updated via Action Group. <em>From PR merged to live: 8 minutes; no platform-team ticket.</em>",
        ),
        Scenario(
            name="Live drill — cluster failure recovered inside RTO",
            body="During the quarterly drill, the reviewer manually deletes the AGC resource. Within 90 seconds: Defender alert, AMG availability red, Flux reconcile detects drift, recreates AGC, HTTPRoutes re-attach, traffic resumes. Total outage: 4 minutes; runbook auto-pinged on-call but did not require human action. <em>The drill validates that GitOps + Flux is the recovery primitive, not just a deployment tool.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"AKS Automatic gives me everything; I don\'t need to design.\"",
            truth="AKS Automatic gives you a coherent default. It does <em>not</em> design your VNet, your identity model, your DR strategy, your egress posture, or your governance. The capstone exists because you still own those decisions — Automatic frees you to focus on them.",
        ),
        Misconception(
            myth="\"I can copy the reference stack from the internet and skip the defence.\"",
            truth="The defence + drill aren\'t bureaucracy — they\'re where you discover that the copied stack doesn\'t match your VNet, your tenant model, your compliance, or your team\'s on-call topology. <em>The cluster you can defend is the only cluster you should run.</em>",
        ),
        Misconception(
            myth="\"DR drills are over-engineering for a startup.\"",
            truth="A startup can lose its company to a single 3 AM data event. The drill cost (one engineer half a day per quarter) is a fraction of one outage. Even a basic Velero restore of a non-prod cluster, executed once, surfaces the assumptions that would cost a week during a real incident.",
        ),
    ],
    flashcards=[
        Flashcard(front="Four phases of the K-AKS capstone?", back="<strong>Phase A</strong> base (private AKS Automatic + Cilium + NAP + Premium/LTS). <strong>Phase B</strong> platform (WI + AGC + storage + AMP/AMG/Container Insights). <strong>Phase C</strong> ops (Defender + Policy + Flux + Velero + blue-green). <strong>Phase D</strong> defence + live drill."),
        Flashcard(front="What does \"defendable\" mean for the reference stack?", back="Every choice can be justified by trade-offs the operator can articulate: why private cluster, why Cilium, why NAP, why LTS, why blue-green for upgrades, why Velero for DR. A peer reviewer can ask \"why X?\" for each component and get a coherent answer."),
        Flashcard(front="Three repos in the GitOps layout?", back="<strong>cluster-config</strong> (Flux\'s own seed), <strong>platform</strong> (Container Insights config, AGC, MI / role assignments), <strong>workloads</strong> (per-tenant or per-team apps). Each has its own RBAC + reviewer set."),
        Flashcard(front="Four chaos events in the live drill?", back="(1) Kill a node — NAP replaces. (2) Revoke a Workload Identity MI role — Pod 401, audit logs surface, fix. (3) Apply a Defender finding — triage + remediation. (4) DR restore — Velero into sibling cluster within RTO."),
        Flashcard(front="Why include LTS in the reference stack?", back="2-year version stability on Premium tier. Avoids quarterly minor jumps for regulated / long-change-control workloads. Costs more ($0.60/cluster-hour vs $0.10 Standard) but predictable upgrade cadence + 24-month support window."),
        Flashcard(front="What makes the upgrade runbook safe?", back="Pre-flight (kubent + Pluto) + planned maintenance window + tunable max-surge + PDB-tested workloads + blue-green node pool fallback for high-stakes + cluster blue-green held in reserve for major LTS-to-LTS jumps."),
        Flashcard(front="What does \"K-AKS-complete\" mean as a deliverable?", back="Bicep code + per-cluster architecture Markdown + DR runbook + live-drill recording. A successor operator can read the docs, run the runbooks, and operate the cluster without you."),
        Flashcard(front="Why is the egress allow-list (Azure Firewall) part of the capstone?", back="Catches data exfiltration at the network layer. A compromised Pod with WI-bound MI to Storage can still try to exfil to an arbitrary FQDN; Azure Firewall denies anything not on the allow-list. Defence in depth — Workload Identity scope + NetworkPolicy + Azure Firewall + Defender runtime detection."),
    ],
    quizzes=[
        Quiz(
            prompt="The peer reviewer asks: \"Why did you pick AKS Automatic + private cluster instead of AKS Standard with manual add-ons?\" Walk the answer.",
            answer="<strong>(1) Default depth:</strong> AKS Automatic preconfigures Container Insights + AMP + AMG + WI + Azure RBAC for K8s + NAP + KEDA + VPA + image cleaner + auto-upgrade + Cilium NetworkPolicy in one cluster create — <em>two months of manual platform-team work avoided</em>. <strong>(2) Coherent opinions:</strong> Automatic\'s defaults are tested together; each component\'s version line is supported by Microsoft as a unit. <strong>(3) Less drift:</strong> ten managed add-ons vs ten Helm charts = ten fewer upgrade-rot risks. <strong>(4) Trade-off acknowledged:</strong> Automatic removes some knobs (no Kubenet, no service-principal cluster identity); we accept these — they\'re things we wouldn\'t pick anyway. <strong>Private cluster (via API VNet Integration):</strong> no public attack surface; pen-test reports thank us. The capstone is intentionally opinionated; the alternatives (Standard + DIY) are valid for teams who genuinely need different choices.",
        ),
        Quiz(
            prompt="During the live drill the reviewer revokes the Workload Identity MI role for Storage. Pod 401s. Walk the response under 10 minutes.",
            answer="(1) AMG availability dashboard fires red within seconds (Pod returns 5xx). (2) On-call gets PagerDuty via Action Group. (3) Open the cluster\'s AMG; confirm the failing service via RED dashboard. (4) Open AKS Diagnostic Settings → KQL on <code>KubeAuditAdmin</code> + <code>AzureActivity</code> in the past 30 min — find the role assignment removal event with timestamp + initiator. (5) Re-create the role assignment via az CLI (<code>az role assignment create --assignee {mi-id} --role 'Storage Blob Data Contributor' --scope ...</code>). (6) Pod\'s next SDK call succeeds (token refreshed by Workload Identity automatically); availability green. (7) Postmortem note: this kind of reverted manual change should have been blocked by Azure Policy / RBAC tightening — file improvement.",
        ),
        Quiz(
            prompt="The CTO walks in: \"Why are we paying Premium tier + LTS — that\'s like $1K/cluster/month extra. Convince me.\" Final defence.",
            answer="\"<strong>Premium gets us LTS — 2-year version stability for the regulated payments cluster.</strong> Without LTS we\'re upgrading a regulated workload every 12 weeks; each upgrade burns 4-8 engineer-days of pre-flight + maintenance + verification (~$10K-20K of engineering time per cluster per cycle). LTS gives us 24 months between minor jumps. Net: Premium tier costs ~$8K/cluster/year extra; saves $40K-80K/cluster/year of upgrade engineering. Plus financially-backed SLA, and access to Microsoft Support for production incidents at the Premium response tier. For our payments cluster, that\'s the right trade-off. For our dev clusters, we run Standard tier with rapid auto-upgrade — different math.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer defended the LTS line item",
        ),
    ],
    glossary=[
        GlossaryItem(name="K-AKS reference stack", definition="The opinionated production AKS topology the K-AKS capstone defends: private AKS Automatic + Cilium + NAP + WI + AGC + Defender + Flux + Velero + LTS."),
        GlossaryItem(name="Phase A / B / C / D", definition="Capstone build phases: Base / Platform / Ops / Defence-and-drill."),
        GlossaryItem(name="Defendable", definition="Every architectural choice can be justified by trade-offs the operator can articulate to a peer reviewer."),
        GlossaryItem(name="Live drill", definition="Reviewer-led chaos exercise: node kill, MI revoke, Defender finding, DR restore. Validates the runbooks."),
        GlossaryItem(name="K-AKS-complete", definition="Capstone deliverable: Bicep + per-cluster architecture doc + DR runbook + drill recording. A successor can operate from these alone."),
        GlossaryItem(name="App-of-Apps GitOps layout", definition="Three Flux repos (cluster-config, platform, workloads) reconciled hierarchically. Cluster bootstrap via cluster-config seed."),
        GlossaryItem(name="DR drill cadence", definition="Quarterly exercise restoring a Velero backup into a sibling cluster within the RTO target. Updates the runbook with deltas."),
        GlossaryItem(name="Architecture Markdown doc", definition="Per-cluster human-readable description of every choice + the alternative considered + the rationale. Lives in the cluster-config repo."),
        GlossaryItem(name="Velero / Backup for AKS", definition="Backup primitive for cluster state + persistent volumes. Geo-redundant Storage Account target. Tested via DR drill."),
        GlossaryItem(name="Premium tier financial SLA", definition="Microsoft\'s contractual SLA for AKS apiserver availability on Premium tier. Required for many enterprise contracts."),
        GlossaryItem(name="Egress allow-list", definition="Azure Firewall FQDN-restricted egress. Catches data exfiltration; complements Workload Identity scoping + NetworkPolicy."),
        GlossaryItem(name="On-call playbook", definition="Per-symptom runbook linking AMG dashboards, KQL queries, az CLI commands, escalation contacts. Lives next to the architecture doc."),
    ],
    recap_lead='K-AKS Capstone built. Phase A (base) → Phase B (platform) → Phase C (ops) → Phase D (defended + drilled). The reference stack is your starting template for any new prod AKS cluster — adapt; don\'t reinvent.',
    recap_next='<strong>K-AKS curriculum complete.</strong> You can architect, identity-secure, network, store, scale, harden, observe, extend, upgrade, troubleshoot, and defend a production AKS cluster end-to-end. Next paths: K-COM (deepen K8s itself) · K-VAN (operate K8s yourself, off-cloud) · K-EKS (the AWS counterpart) · or build internal training rolling K-AKS into your org\'s onboarding.',
)
