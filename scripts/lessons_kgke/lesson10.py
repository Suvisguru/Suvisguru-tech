"""K-GKE G10 — Capstone (Regional Autopilot + Multi-Cluster Gateway + WIF + BinAuth + GMP + Backup + Config Sync + AI inference)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="K-GKE capstone — regional Autopilot with Multi-Cluster Gateway + WIF + Binary Auth + GMP + Backup for GKE + Config Sync + AI Inference Gateway.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Harvest Festival — the K-GKE reference garden</text>
  <rect x="40" y="70" width="170" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="125" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Phase A — base</text>
  <text x="125" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">Regional Autopilot</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">Multi-zone</text>
  <text x="125" y="131" text-anchor="middle" font-size="9" fill="#FBF1D6">Dataplane V2 (Cilium)</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">Stable channel</text>
  <text x="125" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">private cluster + WIF</text>
  <rect x="225" y="70" width="170" height="120" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="310" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Phase B — platform</text>
  <text x="310" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Multi-Cluster Gateway</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Workload Identity Federation</text>
  <text x="310" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">PD CSI + Backup for GKE</text>
  <text x="310" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">GMP + Cloud Monitoring + AMG</text>
  <text x="310" y="160" text-anchor="middle" font-size="9" fill="#FFFFFF">SLO Monitoring</text>
  <rect x="410" y="70" width="170" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="495" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Phase C — ops &amp; AI</text>
  <text x="495" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Binary Authorization</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Policy Controller (Fleet)</text>
  <text x="495" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">Config Sync from Git</text>
  <text x="495" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">Inference Gateway + vLLM</text>
  <text x="495" y="160" text-anchor="middle" font-size="9" fill="#FFFFFF">DR drill quarterly</text>
  <rect x="595" y="70" width="125" height="120" rx="10" fill="#E8B547" stroke="#3F4A5E"/>
  <text x="657" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#5A4F45">Phase D</text>
  <text x="657" y="105" text-anchor="middle" font-size="9" fill="#5A4F45">defence</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#5A4F45">peer review</text>
  <text x="657" y="135" text-anchor="middle" font-size="9" fill="#5A4F45">live drill</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#5A4F45">DR restore</text>
  <text x="657" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#5A4F45">K-GKE-complete</text>
</svg>"""


LESSON = LessonSpec(
    num="10",
    title_short="capstone harvest",
    title_full="G10 · Capstone — Regional Autopilot Reference Garden with AI Inference",
    title_html="K-GKE G10 · Capstone — Reference Garden",
    module_eyebrow="Module G10 · Harvest Festival — tie everything together",
    hero_sub_html='<strong>The K-GKE reference garden.</strong> Regional Autopilot + Multi-Cluster Gateway (multi-cluster) + Workload Identity Federation + Binary Authorization + GMP + Backup for GKE + Config Sync from Git + AI inference workload with GKE Inference Gateway. Multi-region active-active; SLO-first alerting; quarterly DR drill. <em>Build it; defend it; drill it.</em>',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Six months from today. The cluster you\'re about to design will run 80% of revenue — payments, identity, ML inference, sessions. Will it survive a region-failure drill? Will the LLM inference workload meet p99 latency targets at 10× current load? Will the next pen-test report come back clean? Will tenant-A\'s noisy job kill tenant-B\'s SLA? <em>Today\'s lesson: assemble all 9 prior modules into a single defendable design.</em>",
    stamp_html="<strong>Build the four-phase stack: Phase A (regional Autopilot + Cilium + Stable channel + private + WIF), Phase B (Multi-Cluster Gateway + WIF + storage + GMP + AMG + SLO), Phase C (BinAuth + Policy Controller + Config Sync + Backup + AI Inference Gateway + vLLM), Phase D (peer review + live DR drill). Defend it.</strong>",
    district_pin="kg-plot10",
    district_label="Harvest Festival",
    sections=[
        Section(
            eyebrow="Section 1.1 · Phase A — base",
            h2="Phase A — regional Autopilot, Cilium, private, Stable channel",
            body_html="""    <p><strong>Goal:</strong> a defendable base cluster with no public attack surface, modern networking, multi-zone resilience, predictable upgrades.</p>
    <ol>
      <li><strong>Regional Autopilot</strong> — Google manages nodes; per-Pod billing; Pod-level SLA; admission webhooks enforce safety baseline. Regional control plane = 3-zone HA. <em>Default for new prod K-GKE clusters.</em></li>
      <li><strong>Stable release channel</strong> — conservative upgrade cadence; predictable; SLA on supported versions. Set maintenance window Tue 02-06 UTC; document maintenance exclusion calendar.</li>
      <li><strong>Private cluster + master authorized networks</strong> — apiserver public endpoint restricted to corp VPN egress IPs (or fully private + Connect Gateway).</li>
      <li><strong>VPC-native + GKE Dataplane V2 (Cilium)</strong> — Pod IPs from oversized secondary range (planned for 5× current scale); eBPF dataplane; NetworkPolicy default-deny per namespace.</li>
      <li><strong>Cloud NAT</strong> for egress with FQDN-allow-list firewall for outbound (Stripe, GitHub, internal APIs).</li>
      <li><strong>Workload Identity Federation</strong> enabled at cluster create. OIDC issuer URL captured in cluster-config repo.</li>
    </ol>
    <p><em>Phase A success criterion:</em> cluster created via Terraform; <code>kubectl</code> works only via Connect Gateway / IAM-authenticated kubeconfig; no public IPs in cluster\'s GCE-managed-instance-group; Pod IP secondary range usage &lt; 20%.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Phase B — platform",
            h2="Phase B — Multi-Cluster Gateway, identity, storage, observability",
            body_html="""    <p><strong>Multi-cluster networking</strong>:
    <ul>
      <li><strong>Three regional Autopilot clusters</strong> registered into a Fleet (us-central1, europe-west4, asia-southeast1).</li>
      <li><strong>Multi-Cluster Gateway (MCG)</strong> via Gateway API — single global anycast IP routes to nearest healthy cluster.</li>
      <li>HTTPRoutes + per-cluster backend Services with NEG-based container-native LB.</li>
      <li>Failure of one cluster: traffic routes to remaining clusters; DNS-side failover not needed.</li>
    </ul>
    <p><strong>Identity</strong>:
    <ul>
      <li><strong>Workload Identity Federation for GKE</strong> per workload — narrow G-SAs scoped to specific resources.</li>
      <li>Local accounts disabled; IAM Conditions + just-in-time access via PIM-style elevation.</li>
      <li>Connect Gateway for break-glass kubectl access.</li>
    </ul>
    <p><strong>Storage</strong>:
    <ul>
      <li>Default StorageClass = pd-balanced with WaitForFirstConsumer; Hyperdisk Balanced + Storage Pools for sustained-IOPS workloads.</li>
      <li>Regional PD for cross-zone-attach stateful workloads; VolumeAttributesClass for live IOPS retier.</li>
      <li>Filestore Enterprise for RWX needs; GCS FUSE for ML datasets; Parallelstore for distributed training I/O.</li>
      <li>Secret Manager CSI for keyless secrets; auto-rotation enabled.</li>
    </ul>
    <p><strong>Observability</strong>:
    <ul>
      <li>Cloud Logging + Cloud Monitoring (auto); GMP enabled for app metrics; managed Grafana joining all data sources.</li>
      <li>Apiserver / scheduler / controller-manager metrics + audit logs to Cloud Logging (--monitoring=… and --logging=… flags).</li>
      <li>Cloud Trace + Cloud Profiler enabled.</li>
      <li><strong>Service Monitoring</strong> defines per-service SLOs; burn-rate alerts route to Pub/Sub → PagerDuty / Teams.</li>
    </ul>
    <p><em>Phase B success criterion:</em> sample app deploys via Terraform / Config Sync; pulls a Secret Manager secret via WIF; serves traffic through Multi-Cluster Gateway; appears in AMG with RED panels and a burn-rate alert.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Phase C — ops + AI",
            h2="Phase C — Binary Auth, Policy Controller, Config Sync, Backup for GKE, AI inference",
            body_html="""    <p><strong>Security + admission</strong>:
    <ul>
      <li><strong>Binary Authorization</strong> in <em>enforce</em> mode: only images with attestation from the scan-then-sign pipeline (Artifact Registry scan → KMS-signed attestation) may run.</li>
      <li><strong>Policy Controller</strong> (managed Gatekeeper) fleet-wide: Restricted PSA baseline, registry allowlist (only images.gcr.io/our-org/*), label requirements, NetworkPolicy presence checks.</li>
      <li><strong>Container Threat Detection (in SCC)</strong> + <strong>Security Posture</strong> dashboard for runtime + posture findings.</li>
      <li><strong>Confidential GKE Nodes</strong> (Compute Class with N2D AMD SEV-SNP) for the PHI-handling workload.</li>
      <li><strong>CMEK</strong> across PD / Secret Manager / Artifact Registry; rotated on Cloud KMS schedule.</li>
    </ul>
    <p><strong>GitOps</strong>:
    <ul>
      <li><strong>Config Sync</strong> with three repos: <em>cluster-config</em> (Fleet-level), <em>platform</em> (Container Insights config, MCG, MI/role assignments), <em>workloads</em> (per-tenant or per-team).</li>
      <li>RootSync + RepoSync per cluster; drift detection on; manual edits reverted by reconcile loop.</li>
    </ul>
    <p><strong>DR</strong>:
    <ul>
      <li><strong>Backup for GKE</strong>: nightly cluster-wide manifests + PV snapshots; cross-region replication via paired backup region.</li>
      <li>RTO target 60 min for full cluster restore; RPO 24h.</li>
      <li><em>Tested quarterly</em> via blue-green cluster restore drill.</li>
    </ul>
    <p><strong>AI inference workload (the showcase)</strong>:
    <ul>
      <li><strong>GKE Inference Gateway</strong> with KV-cache aware routing.</li>
      <li><strong>vLLM</strong> Pods serving Llama 3 70B on Compute Class Accelerator (A4 H200).</li>
      <li>Kueue queues for batch fine-tuning jobs; JobSet for multi-host TPU training.</li>
      <li>SLO: p95 first-token-latency &lt; 500ms; cost-per-token tracked via BQ + Service Monitoring.</li>
    </ul>
    <p><em>Phase C success criterion:</em> three pull requests can change cluster behaviour; one pen-test exercise passes Defender + admission policies; DR drill restores within RTO; inference workload meets SLO at peak.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · Phase D — defend it, drill it",
            h2="Phase D — defend, drill, deliver",
            body_html="""    <p>You don\'t finish K-GKE by handing in Terraform. You finish by <strong>defending it</strong> in front of a peer panel and surviving a <strong>live drill</strong>.</p>
    <p><strong>Architecture defence</strong> (60 minutes, with senior platform reviewer):</p>
    <ol>
      <li>Walk the network diagram — VPC, subnets, secondary ranges, MCG, Cloud NAT, Private endpoints.</li>
      <li>Walk the identity diagram — WIF Pool + federated credentials + G-SAs per workload + IAM scope; break-glass IAM + PIM.</li>
      <li>Walk the storage diagram — StorageClass defaults, Regional PD usage, snapshot + Backup for GKE policy.</li>
      <li>Walk the observability diagram — three pipes into AMG, SLOs + burn-rate alerts, on-call playbook.</li>
      <li>Walk the upgrade runbook — Stable channel, maintenance window, exclusions, blue-green node-pool fallback.</li>
      <li>Walk the DR runbook — Backup for GKE schedule, restore steps, RTO/RPO targets, drill cadence.</li>
      <li>Walk the AI inference runbook — Inference Gateway routing, vLLM Pod sizing, model cache strategy, SLO + cost per token.</li>
    </ol>
    <p><strong>Live drill</strong> (90 minutes):</p>
    <ul>
      <li>Reviewer kills a node. Cluster Autoscaler / Autopilot replaces; workloads re-schedule; AMG dashboards stay green.</li>
      <li>Reviewer revokes a G-SA IAM role. Pod throws 401; Logs Explorer + Audit Logs locate the change; fix and re-run within 15 min.</li>
      <li>Reviewer applies a high-severity Container Threat Detection finding. You walk the response: alert → triage → remediation → admission policy hardening.</li>
      <li>Reviewer initiates a DR scenario: restore last night\'s Backup for GKE backup into a sibling cluster; verify workloads come up; document deltas.</li>
      <li>Reviewer simulates a 10× LLM inference burst. Inference Gateway routes intelligently; vLLM scales (HPA + Compute Class autoprovisions GPU); SLO holds; cost-per-token logged.</li>
    </ul>
    <p><em>K-GKE-complete</em>: Terraform + per-cluster Markdown architecture doc + DR runbook + AI inference runbook + live-drill recording. <em>You can hand this to a successor and they can run it.</em></p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="In your reference garden, why is Multi-Cluster Gateway preferred over per-region Cloud DNS failover?",
            options=[
                ("Cloud DNS failover is deprecated.", False),
                ("Multi-Cluster Gateway gives a single global anycast IP with traffic to nearest healthy cluster + automatic failover; DNS failover has TTL latency + stale-cache risk.", True),
                ("Both are identical.", False),
            ],
            feedback="MCG is the modern multi-region active-active primitive. DNS failover has TTL + cache issues; MCG fails over at the IP layer with sub-second propagation.",
        ),
    },
    before_after_before='<p>Pre-K-GKE-curriculum operators built GKE clusters one feature at a time, learning each surface only when it failed. Six months in: a half-Modern, half-Legacy cluster with mixed identity (some service principal, some WIF), bring-your-own observability, no Defender / posture findings, an Ingress controller installed by Helm, no GitOps, no DR drill, no upgrade plan, no Inference Gateway. <em>Tribal knowledge in three engineers\' heads.</em></p>',
    before_after_after='<p>The K-GKE reference garden is <strong>defendable</strong>: every choice is justified, every alternative considered, every failure mode mapped to a runbook. <em>Regional Autopilot + Cilium + Stable channel + private + WIF</em> for base; <em>MCG + WIF + storage + GMP/AMG/SLO</em> for platform; <em>BinAuth + Policy Controller + Config Sync + Backup + AI Inference Gateway + vLLM</em> for ops; <em>defence + drill</em> for confidence. A new operator can read the architecture doc, run the runbook, and operate the garden.</p>',
    before_after_caption='<p class="ba-caption"><em>You can\'t cargo-cult a reference garden from the internet — you have to walk every choice yourself. K-GKE Capstone is that walk, defended.</em></p>',
    analogy_intro_html='''<p>The <strong>Harvest Festival</strong> is K-Garden\'s graduation event. Today you\'re the candidate. Four phases of the ceremony.</p>
    <p><strong>Phase A — your base plot</strong> (regional Autopilot). You designed and built it: regional 3-zone control plane, Cilium runners delivering messages, private cluster, Stable Almanac for predictable seasons, sealed worker permits via WIF.</p>
    <p><strong>Phase B — your services</strong> (platform). Multi-Garden Concierge (MCG) routes visitors to the nearest healthy garden. Sealed worker permits per worker (WIF + G-SAs scoped narrowly). Library reservoir (storage) configured. Watchtower (observability) staffed; SLO scribe defines the contracts.</p>
    <p><strong>Phase C — your governance + AI lab</strong>. Inspection Bench (Binary Auth) refuses unattested packages. Door rules (Policy Controller) enforced fleet-wide. Daily Git reconciler (Config Sync) syncs the rule book. Disaster-Relief Vault (Backup for GKE) rehearsed. AI lab serves Llama 3 70B inference via the model-aware Concierge (Inference Gateway) + vLLM specialty inference rooms on A4 H200 plots.</p>
    <p><strong>Phase D — your defence</strong>. The senior gardener walks your garden, asks questions, fires alarms — you respond from the runbooks. <em>If you survive an unannounced live drill, you graduate.</em></p>''',
    translation_rows=[
        ("Phase A — base plot", "Regional Autopilot + Cilium + Stable + private + WIF"),
        ("Multi-Garden Concierge", "Multi-Cluster Gateway (MCG)"),
        ("Sealed worker permit", "Workload Identity Federation"),
        ("Library reservoir", "PD + Hyperdisk + Filestore + Backup for GKE"),
        ("Watchtower bell + SLO scribe", "GMP + AMG + Service Monitoring + burn-rate alerts"),
        ("Inspection Bench", "Binary Authorization"),
        ("Door rules fleet-wide", "Policy Controller + Config Sync"),
        ("Disaster-Relief Vault", "Backup for GKE"),
        ("Model-aware Concierge", "GKE Inference Gateway with KV-cache routing"),
        ("Specialty inference rooms", "vLLM Pods on Compute Class Accelerator (A4 H200)"),
        ("Phase D — defence", "Architecture review + live chaos drill"),
        ("Survive the drill", "Recover from chaos events using runbooks"),
        ("Graduation diploma", "K-GKE-complete: Terraform + arch doc + DR runbook + AI runbook + drill recording"),
    ],
    analogy_stops="A real festival is a one-time ceremony; the K-GKE capstone\'s value is that the artifacts (Terraform, runbooks, drill scripts) are reusable next time around — and the next operator can graduate themselves.",
    eli5="To graduate from K-Garden you build a small base plot, hire your services, set up your governance and AI lab, then the senior gardener walks through and tries to break things. You fix them on the spot using the runbooks. Then you graduate.",
    eli10="The K-GKE reference garden: Phase A (Regional Autopilot + Cilium + Stable channel + private + WIF). Phase B (Multi-Cluster Gateway + WIF + storage + GMP + AMG + SLO Monitoring). Phase C (Binary Auth + Policy Controller + Config Sync + Backup for GKE + Inference Gateway + vLLM). Phase D (architecture defence + live chaos drill: node kill, IAM revoke, CTD finding, DR restore, 10× inference burst). Deliverables: Terraform + arch doc + DR runbook + AI runbook + drill recording.",
    scenarios=[
        Scenario(
            name="SaaS — full reference garden as the new platform-team standard",
            body="A SaaS adopts K-GKE reference garden as the standard for all new prod GKE deployments. Terraform modules version-pinned in a shared repo. Per-tenant garden shapes only diverge on size + region. Defence + drill required before any new garden goes prod. <em>Onboarding new clusters: 4 hours including drill, vs 6 weeks ad-hoc previously.</em>",
        ),
        Scenario(
            name="ML platform — Inference Gateway + vLLM at 10K req/sec",
            body="ML platform serves Llama 3 70B at 10K req/sec across three regional Autopilot clusters via MCG. Inference Gateway routes by KV-cache locality + prompt size. vLLM Pods on Compute Class Accelerator A4 H200; Kueue queues for batch fine-tuning. SLO p95 latency 480ms; cost-per-token tracked. <em>10K req/sec at 60% lower cost vs naive routing.</em>",
        ),
        Scenario(
            name="Bank — DR drill quarterly restored cluster in 42 min",
            body="Bank schedules nightly Backup for GKE backups, cross-region. Quarterly DR drill: spin up empty regional Autopilot in DR region; restore from latest backup; verify workloads. Last drill: restoration completed in 42 min; auditor approved RTO target of < 60 min. <em>DR is rehearsed muscle, not a hopeful plan.</em>",
        ),
        Scenario(
            name="Live drill — IAM revocation diagnosed and fixed in 11 min",
            body="During quarterly drill, reviewer revokes a G-SA Storage Object Viewer role. Pod throws 401. AMG dashboard fires red within seconds. On-call opens Logs Explorer with the saved query for IAM audit; finds the IAM change in Audit Logs; restores via gcloud command; Pod recovers within 11 min. <em>Total elapsed: under 15 min from page to resolution; runbook validated.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Autopilot gives me everything; I don\'t need to design.\"",
            truth="Autopilot gives you a coherent default. It does <em>not</em> design your VPC, your identity model, your DR strategy, your egress posture, your AI inference architecture, or your governance. The capstone exists because you still own those decisions — Autopilot frees you to focus on them.",
        ),
        Misconception(
            myth="\"I can copy the reference garden from the internet and skip the defence.\"",
            truth="The defence + drill aren\'t bureaucracy — they\'re where you discover that the copied design doesn\'t match your VPC, your tenant model, your compliance, or your team\'s on-call topology. <em>The garden you can defend is the only garden you should run.</em>",
        ),
        Misconception(
            myth="\"DR drills are over-engineering for a startup.\"",
            truth="A startup can lose its company to a single 3 AM data event. The drill cost (one engineer half a day per quarter) is a fraction of one outage. Even a basic Backup for GKE restore of a non-prod cluster, executed once, surfaces the assumptions that would cost a week during a real incident.",
        ),
    ],
    flashcards=[
        Flashcard(front="Four phases of the K-GKE capstone?", back="<strong>Phase A</strong> base (regional Autopilot + Cilium + Stable channel + private + WIF). <strong>Phase B</strong> platform (MCG + WIF + storage + GMP/AMG/SLO). <strong>Phase C</strong> ops + AI (BinAuth + Policy Controller + Config Sync + Backup for GKE + Inference Gateway + vLLM). <strong>Phase D</strong> defence + live drill."),
        Flashcard(front="What does \"defendable\" mean for the reference garden?", back="Every choice can be justified by trade-offs the operator can articulate: why Autopilot over Standard, why Cilium, why Stable channel, why MCG, why Backup for GKE, why Inference Gateway. A peer reviewer can ask \"why X?\" for each component and get a coherent answer."),
        Flashcard(front="Three Config Sync repo patterns?", back="<strong>cluster-config</strong> (Fleet seed + RootSync), <strong>platform</strong> (Container Insights, MCG, MI/role assignments), <strong>workloads</strong> (per-tenant or per-team apps). Each has its own RBAC + reviewer set."),
        Flashcard(front="Five chaos events in the live drill?", back="(1) Kill a node — Autopilot replaces. (2) Revoke a G-SA IAM role — Pod 401, Audit Logs surface, fix. (3) CTD finding — triage + remediation + admission policy hardening. (4) DR restore — Backup for GKE into sibling cluster within RTO. (5) 10× inference burst — Inference Gateway + vLLM scaling holds SLO."),
        Flashcard(front="Why include AI inference in the reference capstone?", back="Most modern GKE deployments include some AI/ML serving workload. The capstone showcases the modern AI inference pattern: Inference Gateway + vLLM + Compute Class Accelerator + Kueue/JobSet for batch + cost-per-token KPI. Operating an AI workload defendably is part of the K-GKE skill bundle."),
        Flashcard(front="What makes the upgrade runbook safe?", back="Stable release channel + planned maintenance window + maintenance exclusion calendar + Pub/Sub upgrade notifications + pre-flight via gcpdiag / kubent. PDB-tested workloads + blue-green node-pool fallback for high-stakes."),
        Flashcard(front="What does \"K-GKE-complete\" mean as a deliverable?", back="Terraform code + per-cluster architecture Markdown + DR runbook + AI inference runbook + live-drill recording. A successor operator can read the docs, run the runbooks, and operate the garden without you."),
        Flashcard(front="Why is the egress allow-list (Cloud NAT + FQDN-allow firewall) part of the capstone?", back="Catches data exfiltration at the network layer. A compromised Pod with WIF-bound G-SA to Storage can still try to exfil to an arbitrary FQDN; firewall denies anything not on the allow-list. Defence in depth — WIF scope + NetworkPolicy + Cloud NAT + firewall + CTD runtime detection."),
    ],
    quizzes=[
        Quiz(
            prompt="The peer reviewer asks: \"Why did you pick Autopilot + Stable channel instead of Standard + Regular?\" Walk the answer.",
            answer="<strong>(1) Autopilot operational depth:</strong> Google manages nodes; per-Pod billing aligns spend to actual usage; Pod-level SLA; admission webhooks enforce safety baseline. We don\'t want platform engineers managing node SKUs at this stage. <strong>(2) Stable channel:</strong> for prod, the upgrade premium of conservative cadence is worth more than the latest features. New minors land in Rapid first; bake in Regular; arrive in Stable when validated. We test new features on a separate canary cluster on Rapid. <strong>(3) Trade-offs accepted:</strong> Autopilot blocks privileged / hostNetwork / hostPath workloads — none of our app patterns need them. Stable means we get features 4-12 weeks later than Rapid — fine for our launch cadence. <strong>(4) Alternatives valid:</strong> Standard for clusters with niche kernel needs; Regular for teams that want the latest features sooner. The capstone is opinionated; alternatives have their place.",
        ),
        Quiz(
            prompt="During the live drill the reviewer revokes a G-SA Storage Object Viewer role. Pod 401s. Walk the response under 15 minutes.",
            answer="(1) AMG dashboard fires red (Pod returns 5xx). PagerDuty via Pub/Sub Notification Channel. (2) Open AMG; confirm failing service via RED dashboard. (3) Open Logs Explorer with saved query for IAM audit; filter to past 30 min; find the role assignment removal in <code>cloudaudit.googleapis.com/activity</code> with timestamp + initiator. (4) Re-create role assignment via gcloud: <code>gcloud projects add-iam-policy-binding ... --member=serviceAccount:G-SA --role=roles/storage.objectViewer</code>. (5) Pod\'s next SDK call succeeds (token refreshed by WIF metadata server automatically). (6) Postmortem note: this kind of reverted manual change should have been blocked by Policy Controller / Org Policy on IAM — file improvement.",
        ),
        Quiz(
            prompt="The CTO walks in: \"Why are we paying for GKE Enterprise on top of Autopilot? That\'s a lot of zeros.\" Final defence.",
            answer="\"<strong>Enterprise pays off for our scale (3 regions × multiple clusters + planned multi-cloud).</strong> Without Enterprise: per-cluster Argo CD with chart drift; per-cluster Helm-installed Gatekeeper with admission policies that drift; mesh-of-meshes for cross-cluster mTLS; manual coordination of multi-cluster ingress. With Enterprise: Config Sync + Policy Controller + Cloud Service Mesh + Connect Gateway + MCG come as managed surfaces; one repo describes the rules; reconciled fleet-wide; one global anycast IP. The Enterprise license is real money but trades against per-cluster ops + the chart drift / mesh-of-meshes complexity that bites at our scale. <em>If we were running 1-2 clusters total, Enterprise would be premature.</em> At our 3-region active-active footprint, it\'s the right call.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CTO",
        ),
    ],
    glossary=[
        GlossaryItem(name="K-GKE reference garden", definition="The opinionated production GKE topology the capstone defends: regional Autopilot + Cilium + Stable + private + WIF + MCG + Backup for GKE + Inference Gateway + vLLM."),
        GlossaryItem(name="Phase A / B / C / D", definition="Capstone build phases: Base / Platform / Ops + AI / Defence-and-drill."),
        GlossaryItem(name="Defendable", definition="Every architectural choice can be justified by trade-offs the operator can articulate to a peer reviewer."),
        GlossaryItem(name="Live drill", definition="Reviewer-led chaos exercise: node kill, IAM revoke, CTD finding, DR restore, inference burst. Validates the runbooks."),
        GlossaryItem(name="K-GKE-complete", definition="Capstone deliverable: Terraform + per-cluster architecture doc + DR runbook + AI inference runbook + drill recording."),
        GlossaryItem(name="App-of-Apps GitOps layout", definition="Three Config Sync repos (cluster-config, platform, workloads) reconciled hierarchically."),
        GlossaryItem(name="DR drill cadence", definition="Quarterly exercise restoring a Backup for GKE backup into a sibling cluster within the RTO target. Updates the runbook with deltas."),
        GlossaryItem(name="Architecture Markdown doc", definition="Per-cluster human-readable description of every choice + the alternative considered + the rationale."),
        GlossaryItem(name="Backup for GKE schedule", definition="Nightly cluster-wide manifests + PV snapshots; cross-region replication; tested via drill."),
        GlossaryItem(name="GKE Enterprise license", definition="Add-on tier that enables Fleets / Config Sync / Policy Controller / CSM / MCG. Cost-justified at multi-cluster + multi-cloud scale."),
        GlossaryItem(name="Inference Gateway runbook", definition="Per-model routing strategy, vLLM Pod sizing, KV-cache config, SLO + cost-per-token KPI."),
        GlossaryItem(name="Egress allow-list", definition="Cloud NAT + FQDN-restricted egress firewall. Catches data exfiltration; complements WIF scoping + NetworkPolicy + CTD."),
    ],
    recap_lead="K-GKE Capstone built. Phase A (base) → Phase B (platform) → Phase C (ops + AI) → Phase D (defended + drilled). The reference garden is your starting template for any new prod GKE deployment — adapt; don\'t reinvent.",
    recap_next='<strong>K-GKE curriculum complete.</strong> You can architect, version, network, identity-secure, store, scale, observe, federate, troubleshoot, and defend a production GKE deployment with AI inference end-to-end. Next paths: K-COM (deepen K8s itself) · K-VAN (operate K8s yourself, off-cloud) · K-EKS (the AWS counterpart) · K-AKS (the Azure counterpart) · or build internal training rolling K-GKE into your org\'s onboarding.',
)
