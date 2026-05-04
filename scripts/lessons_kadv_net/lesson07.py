"""K-ADV-NET N7 — Capstone: multi-cluster network across EKS + AKS + GKE + on-prem."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Capstone — multi-cluster, multi-cloud network.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Multi-Region Highway Map · K-Highway — every K-ADV-NET layer in one architecture</text>
  <rect x="40" y="70" width="130" height="60" rx="10" fill="#3878B5" stroke="#1F2433"/>
  <text x="105" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">EKS us-east</text>
  <text x="105" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Cilium + Hubble</text>
  <rect x="190" y="70" width="130" height="60" rx="10" fill="#5E4A8E" stroke="#1F2433"/>
  <text x="255" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">AKS eastus</text>
  <text x="255" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Azure CNI + Cilium</text>
  <rect x="340" y="70" width="130" height="60" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="405" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">GKE europe-w</text>
  <text x="405" y="108" text-anchor="middle" font-size="9" fill="#1F2433">DPv2 (Cilium)</text>
  <rect x="490" y="70" width="130" height="60" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="555" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">OCP / Tanzu</text>
  <text x="555" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">on-prem</text>
  <rect x="640" y="70" width="80" height="60" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="680" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">DNS+LB</text>
  <text x="680" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">global</text>
  <rect x="40" y="160" width="680" height="50" rx="10" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="180" text-anchor="middle" font-size="11" font-weight="700" fill="#A04832">Cilium ClusterMesh + Submariner + Skupper + AdminNetworkPolicy + Gateway API + private hybrid</text>
  <text x="380" y="198" text-anchor="middle" font-size="9" font-style="italic" fill="#A04832">multi-cloud network as code</text>
</svg>"""


LESSON = LessonSpec(
    num="07",
    title_short="capstone — multi-region",
    title_full="N7 · Capstone — Multi-Cluster Network Across EKS + AKS + GKE + On-Prem",
    title_html="K-ADV-NET N7 · Capstone",
    module_eyebrow="Module N7 · Multi-Region Highway Map — every K-ADV-NET layer in one architecture",
    hero_sub_html='Reference architecture: 5 clusters across AWS + Azure + GCP + OpenShift on-prem + Tanzu. <strong>Cilium ClusterMesh</strong> between same-CNI cloud peers; <strong>Submariner</strong> for cross-CNI on-prem path; <strong>Skupper</strong> for partner integration; <strong>Gateway API</strong> per region with global DNS + LB; <strong>AdminNetworkPolicy</strong> fleet-wide; <strong>Hubble</strong> + Pixie + Tetragon everywhere; <strong>private clusters</strong> + DX/ER/CI hybrid; <strong>egress gateways</strong> per cluster; <strong>kube-burner</strong> CI for perf regressions; <strong>runbook</strong> covering per-bridge failure modes.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM during a region-wide AWS outage. The team\'s primary cluster (EKS us-east) is gone. <em>Without multi-region + cross-cluster + global LB, the whole product is down</em>. Today\'s lesson: design the multi-cloud network so a single cloud / region failure is a 5-minute failover, not a 5-hour outage.",
    stamp_html="<strong>Multi-cloud network = ClusterMesh + Submariner + Skupper + Gateway API + ANP fleet-wide + Hubble everywhere + runbooks. Pick bridges per peer trust + perf; private + hybrid clusters; global LB / DNS for failover.</strong>",
    district_pin="knet-junction07",
    district_label="Multi-Region Highway Map",
    sections=[
        Section(
            eyebrow="Section 1.1 · architecture",
            h2="5 clusters, 4 clouds, 4 bridges",
            body_html="""    <p><strong>Clusters</strong>: EKS us-east-1 (primary); EKS eu-west-1 (DR); AKS eastus (regulated workloads); GKE europe-west1 (data residency); OCP on-prem (legacy + regulated). All Cilium where cloud allows; OCP runs OVN-K with bridge to Cilium pattern.</p>
    <p><strong>Bridges</strong>: ClusterMesh between EKS pair (same CNI, same cloud); Submariner between cloud peers + OCP; Skupper to partner clusters. Routing via Gateway API per cluster + global LB (Route 53 / Azure Traffic Manager / GCP Global LB) for failover.</p>
    <p><strong>Connectivity</strong>: AWS DX + Azure ExpressRoute + GCP Cloud Interconnect to corporate DC. Private clusters; apiserver via PSC / Private Endpoint. Egress gateways per cluster route outbound through audited paths.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · the policy stack",
            h2="ANP fleet-wide; per-cluster NP; mesh L7 policy",
            body_html="""    <p><strong>AdminNetworkPolicy fleet-wide</strong>: GitOps-deployed via Argo CD ApplicationSets. Org rules: \"deny ingress from sandbox-* to prod-*; deny egress to RFC-1918 from prod-*; require mTLS for east-west.\"</p>
    <p><strong>NetworkPolicy per team</strong>: default-deny + explicit allow. Generated from service catalog + Hubble flow observation in dev + curated in Git.</p>
    <p><strong>Mesh L7 (Linkerd ambient)</strong>: AuthorizationPolicy per Service — \"only orders SA may call payments SA on POST /charge.\" Mesh traffic shifting + canary.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · observability + tracing",
            h2="Hubble + Pixie + Tetragon everywhere; multi-cluster",
            body_html="""    <p><strong>Hubble</strong> in every cluster + Hubble Relay aggregating across clusters. Per-flow + L7 verdicts cluster-wide. Hubble UI shows multi-cluster service map.</p>
    <p><strong>Pixie</strong> on every cluster: per-Service L7 trace; per-endpoint latency. CI pulls Pixie data + alarms on regressions.</p>
    <p><strong>Tetragon</strong>: kernel-level event log per cluster; SIEM aggregates; rules detect novel patterns.</p>
    <p><strong>kube-burner</strong>: CI gates on cluster perf regressions; runs against staging clusters before any CNI / mesh upgrade.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · failover + runbook",
            h2="region failover + per-bridge runbooks",
            body_html="""    <p><strong>Region failover</strong>: global LB health checks per cluster\'s ingress; failed cluster removed from rotation in &lt; 60s; traffic shifts to healthy clusters. Stateful workloads either active-active (replicated state) or active-passive (controlled failover with promote / demote).</p>
    <p><strong>Per-bridge runbooks</strong>: ClusterMesh apiserver down (rebuild from etcd); Submariner gateway dead (failover to redundant gateway); Skupper VAN router stuck (re-establish TLS); Gateway controller crashloop (rollback CRD). Each runbook tested via game days.</p>
    <p><strong>Disaster scenarios</strong>: region outage drill quarterly; cross-cloud failover drill semi-annually; partner-cluster integration regression annually. Time-to-detect / time-to-recover measured + improved.</p>
    <p><strong>The architecture is not the work; the discipline of operating it is.</strong></p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="Why use ClusterMesh + Submariner + Skupper instead of one bridge for everything?",
            options=[
                ("Vendor neutrality.", False),
                ("Each bridge fits a different trust + CNI + perf scenario; using the wrong tool for one peer wastes performance or security.", True),
                ("Cost.", False),
            ],
            feedback="ClusterMesh same-CNI low-latency; Submariner cross-CNI L4; Skupper cross-org L7. Each pulls in opposite directions; matching bridge to peer pattern wins.",
        ),
        3: PauseCheck(
            question="Why are quarterly region-failover drills non-optional?",
            options=[
                ("Tradition.", False),
                ("Untested failover rots; drills measure + improve recovery time.", True),
                ("Required by HIPAA.", False),
            ],
            feedback="Multi-cloud failover paths involve global LB + DNS + state replication + connection draining. Each can rot. Drills find the rust before incidents.",
        ),
    },
    before_after_before='<p>Single-cloud / single-cluster + ad-hoc multi-cluster patterns. Region outage = product outage. Cross-cluster traffic via VPN. Observability fragmented. Runbooks aspirational.</p>',
    before_after_after='<p>Multi-cloud reference: bridges per peer pattern; ANP fleet-wide; Hubble + Pixie everywhere; private + hybrid; global LB failover. Region failure = 5-minute failover; partner integration = day-of standup.</p>',
    before_after_caption='<p class="ba-caption"><em>Pick bridges by peer pattern; ANP fleet-wide; observe everything; drill the runbook quarterly.</em></p>',
    analogy_intro_html='''<p>The capstone Highway Captain administers five cities across four nations. Each city pair is connected by the right bridge — twin-city expressways where the cities share planners, border-tunnels for different planners, diplomatic-pouches for foreign neighbours. Federal customs sets non-negotiable rules; each city refines within. Traffic helicopters circle every city; reports stream to the central command. The Captain runs region-failover drills every quarter — vehicles destined for the offline city redirect to the next-closest city in &lt; 1 minute.</p>
    <p>The capstone is the sum of N1-N6: bridges (N3), Gateway API (N2), CNI + eBPF + BGP (N1), mesh + DNS (N4), policy + private + hybrid (N5), tracing + perf (N6). Plus operational rhythm.</p>''',
    translation_rows=[
        ("Five cities, four nations", "5 clusters across AWS + Azure + GCP + on-prem"),
        ("Twin-city expressway", "Cilium ClusterMesh (same-CNI peers)"),
        ("Border-tunnel", "Submariner (cross-CNI peer)"),
        ("Diplomatic-pouch", "Skupper (partner / cross-org)"),
        ("City entrance signs", "Gateway API per cluster"),
        ("Federal customs rules", "AdminNetworkPolicy fleet-wide"),
        ("Helicopters everywhere", "Hubble / Pixie / Tetragon multi-cluster"),
        ("Region-failover drill", "Global LB failover + cross-cluster state"),
        ("Diplomatic embassy line", "Private apiserver + DX/ER/CI hybrid"),
    ],
    analogy_stops="A real city has fixed roads; cluster bridges + policy are software. Region failover scenarios must be exercised; they don\'t self-verify.",
    eli5="Five cities; four bridges; central air-traffic control; quarterly disaster drills. The capstone is everything connected, observed, and exercised.",
    eli10="<strong>Clusters</strong>: EKS x2 + AKS + GKE + OCP-on-prem. <strong>Bridges</strong>: ClusterMesh + Submariner + Skupper. <strong>Edge</strong>: Gateway API + global LB / DNS. <strong>Policy</strong>: AdminNetworkPolicy + NP + mesh AuthorizationPolicy. <strong>Observability</strong>: Hubble + Pixie + Tetragon multi-cluster. <strong>Connectivity</strong>: private clusters + DX/ER/CI hybrid + egress gateways. <strong>Operational rhythm</strong>: kube-burner CI + quarterly failover drills + per-bridge runbooks.",
    scenarios=[
        Scenario(
            name="Real region failover — 90-second recovery",
            body="A real AWS us-east-1 brownout: global LB health checks marked the EKS us-east cluster unhealthy at T+45s; Route 53 shifted traffic to EKS eu-west-1; user impact &lt; 90s. Stateful Services already replicated. <em>The drill the team ran 3 weeks before paid off.</em>",
        ),
        Scenario(
            name="Partner integration via Skupper — 1-day standup",
            body="A new partner Service needed integration. Skupper VAN: partner side router peered with our router via TLS; Service exposed only via the VAN; no VPN, no firewall changes. Standup: 1 day; weeks shorter than VPN setup.",
        ),
        Scenario(
            name="ANP caught a misconfigured tenant",
            body="A new tenant team\'s NetworkPolicy allowed egress to RFC-1918. AdminNetworkPolicy denied; tenant\'s deploy logged the override at admission. Tenant updated their NetworkPolicy; deploy went through; no compromise reached prod.",
        ),
        Scenario(
            name="Outage — Submariner gateway across clouds",
            body="Submariner gateway between EKS + on-prem OCP failed in middle of replication. Failover to redundant gateway in 6 seconds. Postmortem: validated the redundant-gateway path quarterly; ensure ARP convergence + BGP withdrawal happens cleanly.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Multi-cloud is over-engineered for most teams.\"",
            truth="Region failover (multi-region single-cloud) is a baseline for any product with paying customers. Multi-cloud (cross-cloud failover) earns its complexity for regulated / global / partner-heavy workloads. Match the architecture to the risk + customer expectations.",
        ),
        Misconception(
            myth="\"One bridge for all clusters is simpler.\"",
            truth="Forcing one bridge means accepting it\'s suboptimal for some peer patterns. The right answer is: pick the right bridge per peer; the bridges coexist; runbooks document each. Simplicity isn\'t \"one tool\"; it\'s \"fewest right tools.\"",
        ),
        Misconception(
            myth="\"GitOps + Argo CD ApplicationSets fleet-deploy everything; no per-cluster work needed.\"",
            truth="ApplicationSets handle per-cluster deployment, but per-cluster differences (e.g., cloud-specific Storage / LB / IAM annotations) need the App template to handle. Fleet GitOps is foundation; per-cluster engineering still applies.",
        ),
    ],
    flashcards=[
        Flashcard(front="Capstone bridge selection per peer pattern?", back="<strong>Same-CNI same-org peers</strong>: Cilium ClusterMesh. <strong>Cross-CNI peers</strong>: Submariner. <strong>Cross-org / firewall-segmented</strong>: Skupper. <strong>Mesh-heavy already</strong>: Istio multi-cluster."),
        Flashcard(front="Capstone observability stack?", back="<strong>Hubble Relay</strong> aggregates per-cluster Hubble; multi-cluster service map. <strong>Pixie</strong> per cluster + L7 trace. <strong>Tetragon</strong> per cluster + SIEM aggregation. <strong>kube-burner</strong> in CI for perf regressions."),
        Flashcard(front="Region failover RTO target?", back="P95 &lt; 90 seconds for stateless workloads via global LB health checks; stateful workloads depend on replication strategy + acceptable RPO."),
        Flashcard(front="ApplicationSet pattern for fleet?", back="Argo CD ApplicationSet generates Application per cluster from a generator (clusters / git directories / list); same chart deployed everywhere with per-cluster values from cluster labels."),
        Flashcard(front="Per-bridge runbook scope?", back="ClusterMesh apiserver rebuild; Submariner gateway failover; Skupper TLS re-establish; Gateway controller rollback. Each tested quarterly."),
        Flashcard(front="Hybrid connectivity choices?", back="<strong>AWS Direct Connect</strong> + DX Gateway + Transit Gateway. <strong>Azure ExpressRoute</strong> + ER Gateway + vWAN. <strong>GCP Cloud Interconnect</strong> + Cloud Router. <strong>VPN</strong> for backup."),
        Flashcard(front="Drill cadence?", back="<strong>Quarterly</strong>: region-failover drill. <strong>Semi-annually</strong>: cross-cloud failover drill. <strong>Annually</strong>: partner-integration regression. Time-to-detect + time-to-recover measured."),
        Flashcard(front="Why ANP fleet-wide?", back="Org-wide rules can\'t be enforced if each cluster manages NP locally. ANP via GitOps = single source of truth; rule changes propagate to all clusters via ApplicationSet; compliance evidence is fleet-level."),
    ],
    quizzes=[
        Quiz(
            prompt="Walk a new team through the multi-cluster capstone in 5 minutes.",
            answer="\"Five clusters across AWS + Azure + GCP + on-prem; each Cilium where the cloud allows. Bridges: ClusterMesh between cloud peers; Submariner to OCP; Skupper for partners. Each cluster has Gateway API at the edge; global LB / DNS routes between regions for failover. AdminNetworkPolicy is GitOps-deployed cluster-wide via ApplicationSets — fleet-uniform org rules. Per-team NetworkPolicy + mesh AuthorizationPolicy. Hubble Relay aggregates flow logs across clusters; Pixie per-cluster L7 trace; Tetragon to SIEM. Private clusters + DX/ER/CI for hybrid. Egress gateways per cluster. kube-burner in CI catches perf regressions before deploy. Quarterly region-failover drills + per-bridge runbooks. Onboarding day-1: Service Catalog template ships you a workload pre-wired with NetPol + mesh + Hubble + observability — you don\'t configure networking; you consume the platform.\"",
        ),
        Quiz(
            prompt="A new region (Tokyo) is needed. Walk the rollout in this architecture.",
            answer="(1) <strong>Provision EKS cluster</strong> in ap-northeast-1 via Crossplane + Cilium installation. (2) <strong>Connect to ClusterMesh</strong> with existing EKS pair; Pod CIDRs allocated to avoid overlap. (3) <strong>Wire AdminNetworkPolicy</strong>: ApplicationSet picks up new cluster; org rules apply automatically. (4) <strong>Gateway API</strong> per region; cert-manager issues TLS; global LB adds Tokyo as healthy target. (5) <strong>Hubble</strong> + Pixie + Tetragon: agents deploy via DaemonSet through the platform template. (6) <strong>kube-burner CI</strong> baseline for new cluster. (7) <strong>Runbook update</strong>: per-bridge failure modes for Tokyo paths. (8) <strong>Game day</strong>: simulated region outage to validate failover from Tokyo to nearest cluster. <em>Time: 1 week of platform work; 1 week of validation; ready for production traffic.</em>",
        ),
        Quiz(
            prompt="Leadership says: \"this multi-cloud architecture is 30% more expensive than single-cloud. Pick one cloud + simplify.\" Defend.",
            answer="\"<strong>Multi-cloud is insurance against region + cloud + vendor failure modes.</strong> Three reasons it stays: (1) <strong>Cloud-region failure</strong>: 2024 saw 4 multi-hour AWS region outages + 2 Azure region outages. Single-cloud customers lost. Multi-cloud customers shifted in &lt; 90s. (2) <strong>Vendor pricing leverage</strong>: when AWS raises prices or changes terms, we have negotiation power because we can shift workloads. Single-cloud has no leverage. (3) <strong>Compliance + jurisdictions</strong>: data residency rules force GCP for EU customers, Azure for Microsoft-shop customers, on-prem for regulated. Multi-cloud is the consequence of customer needs, not architecture aesthetics. <strong>The 30% cost premium is the price of resilience + leverage + customer reach</strong>. Trim where you can (right-size, Spot, autoscale, S3 IA archive) but don\'t cut the architecture that lets us survive a cloud outage.\"",
            cyoa=True,
            cyoa_tag="how the network architect defended multi-cloud",
        ),
    ],
    glossary=[
        GlossaryItem(name="multi-cloud network", definition="Clusters across multiple cloud providers + on-prem connected via bridges. Enables region + vendor + jurisdiction failover."),
        GlossaryItem(name="ClusterMesh", definition="Cilium\'s same-CNI multi-cluster bridge. eBPF native routing."),
        GlossaryItem(name="Submariner", definition="CNI-agnostic L4 IPsec multi-cluster bridge."),
        GlossaryItem(name="Skupper", definition="L7 application-layer multi-cluster + cross-org bridge. Egress-only TLS."),
        GlossaryItem(name="Gateway API per region", definition="Each cluster hosts its own Gateway; global LB / DNS routes between regions."),
        GlossaryItem(name="ApplicationSet", definition="Argo CD CRD generating Apps per cluster from generators. Fleet GitOps pattern."),
        GlossaryItem(name="region failover RTO", definition="Time from region outage detection to traffic shifted. Multi-region target P95 &lt; 90s."),
        GlossaryItem(name="kube-burner CI", definition="Synthetic-load perf testing as CI gate. Catches CNI / mesh upgrade regressions."),
        GlossaryItem(name="game day", definition="Scheduled exercise of failure scenarios. Quarterly region-failover; semi-annual cross-cloud; annual partner-integration."),
        GlossaryItem(name="operational rhythm", definition="Drills + CI gates + runbook reviews on cadence. The discipline that keeps multi-cloud reliable."),
    ],
    recap_lead="Multi-cloud network = bridges per peer + ANP fleet-wide + Hubble everywhere + private hybrid + Gateway API + global LB + runbooks tested via game days. Architecture is the assembly; operational rhythm is the discipline.",
    recap_next='<strong>K-ADV-NET complete.</strong> 7 modules. From CNI internals (N1) to multi-cloud capstone (N7). Next K-ADV course: <em>K-ADV-PE</em> (Platform Engineering — K-Workshop) or per founder direction.',
    architecture_svg='''<svg viewBox="0 0 760 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="K-ADV-NET capstone: 5 clusters across AWS + Azure + GCP + on-prem with bridges per peer pattern + global LB + ANP + Hubble.">
  <rect x="10" y="10" width="740" height="260" rx="12" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">K-ADV-NET CAPSTONE · MULTI-CLOUD MULTI-CLUSTER NETWORK</text>
  <rect x="20" y="50" width="130" height="60" rx="6" fill="#3878B5"/>
  <text x="85" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">EKS us-east</text>
  <text x="85" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">Cilium + Hubble</text>
  <rect x="160" y="50" width="130" height="60" rx="6" fill="#5E4A8E"/>
  <text x="225" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">AKS eastus</text>
  <text x="225" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">Azure CNI + Cilium</text>
  <rect x="300" y="50" width="130" height="60" rx="6" fill="#5DCAA5"/>
  <text x="365" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">GKE europe</text>
  <text x="365" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">Dataplane V2</text>
  <rect x="440" y="50" width="130" height="60" rx="6" fill="#A04832"/>
  <text x="505" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">OCP on-prem</text>
  <text x="505" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">OVN-K</text>
  <rect x="580" y="50" width="160" height="60" rx="6" fill="#3F4A5E"/>
  <text x="660" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Global LB + DNS</text>
  <text x="660" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">Route 53 / Traffic Mgr / GCP LB</text>
  <text x="660" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">cross-region failover</text>
  <rect x="20" y="125" width="220" height="55" rx="6" fill="#FAC775"/>
  <text x="130" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">Cilium ClusterMesh</text>
  <text x="130" y="161" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">same-CNI peers (cloud)</text>
  <text x="130" y="174" text-anchor="middle" font-size="8" fill="#5A4F45">eBPF-native</text>
  <rect x="250" y="125" width="160" height="55" rx="6" fill="#5DCAA5"/>
  <text x="330" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Submariner</text>
  <text x="330" y="161" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">cloud ↔ on-prem</text>
  <text x="330" y="174" text-anchor="middle" font-size="8" fill="#1F2433">L4 IPsec</text>
  <rect x="420" y="125" width="160" height="55" rx="6" fill="#FF9900"/>
  <text x="500" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Skupper</text>
  <text x="500" y="161" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">partner integration</text>
  <text x="500" y="174" text-anchor="middle" font-size="8" fill="#1F2433">L7 VAN</text>
  <rect x="590" y="125" width="150" height="55" rx="6" fill="#5A6B81"/>
  <text x="665" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Gateway API</text>
  <text x="665" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">per-cluster ingress</text>
  <text x="665" y="174" text-anchor="middle" font-size="8" fill="#FBE8DC">+ private + DX/ER/CI</text>
  <rect x="20" y="195" width="720" height="65" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="215" text-anchor="middle" font-size="11" font-weight="700" fill="#A04832">AdminNetworkPolicy fleet-wide (GitOps via ApplicationSets) · per-team NetPol within</text>
  <text x="380" y="231" text-anchor="middle" font-size="9" fill="#5A4F45" font-style="italic">Hubble Relay + Pixie + Tetragon multi-cluster · kube-burner CI gates · per-bridge runbooks</text>
  <text x="380" y="247" text-anchor="middle" font-size="9" fill="#5A4F45">Region failover quarterly · cross-cloud semi-annually · target P95 RTO &lt; 90 sec</text>
</svg>''',
    architecture_caption='Multi-cloud network: 5 clusters across AWS + Azure + GCP + on-prem; bridges per peer pattern (ClusterMesh same-CNI / Submariner heterogeneous / Skupper partner). Gateway API + global LB for region failover. AdminNetworkPolicy fleet-wide. Hubble + Pixie + Tetragon. Game-day-tested runbooks.',
)
