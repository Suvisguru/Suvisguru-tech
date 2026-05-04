"""K-ADV-NET N5 — NetworkPolicy at scale + egress + private + hybrid."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="NetworkPolicy hierarchy + egress + private + hybrid.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Customs + Tollbooth · K-Highway — policy hierarchy + audited egress</text>
  <rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">AdminNetworkPolicy</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">org-wide; precedence</text>
  <rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">NetworkPolicy (team)</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">default-deny + allow</text>
  <rect x="410" y="70" width="170" height="100" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">egress gateway</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">all egress audited</text>
  <rect x="595" y="70" width="125" height="100" rx="10" fill="#FAC775" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">private cluster</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#1F2433">+ hybrid VPN/DX</text>
</svg>"""


LESSON = LessonSpec(
    num="05",
    title_short="NetworkPolicy + egress + private",
    title_full="N5 · NetworkPolicy at Scale + Egress + Private + Hybrid",
    title_html="K-ADV-NET N5 · NetworkPolicy + Egress + Private",
    module_eyebrow="Module N5 · Customs + Tollbooth — policy hierarchy + audited egress",
    hero_sub_html='<strong>NetworkPolicy hierarchy</strong>: AdminNetworkPolicy (org-wide, precedence) > NetworkPolicy (team) > BaselineAdminNetworkPolicy (defaults). <strong>Default-deny baseline</strong> + explicit allow per consumer. <strong>Egress gateway</strong>: all cluster egress through one node group; auditable + controllable. <strong>Private clusters</strong>: apiserver private (PSC / Private Endpoint); nodes private. <strong>Hybrid connectivity</strong>: VPN + Direct Connect (AWS) / ExpressRoute (Azure) / Cloud Interconnect (GCP).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A compromised Pod opened an outbound TCP connection to an unknown crypto-miner pool. <em>The team had NetworkPolicy on east-west but not egress controls — egress was open to the Internet from any Pod.</em> Today\'s lesson: egress + private + hybrid + AdminNetworkPolicy close the open-egress class entirely.",
    stamp_html="<strong>Default-deny ingress + egress at namespace; AdminNetworkPolicy for org-wide rules; egress gateway for audit trail; private cluster for apiserver isolation; hybrid VPN/DX for on-prem.</strong>",
    district_pin="knet-junction05",
    district_label="Customs + Tollbooth",
    sections=[
        Section(
            eyebrow="Section 1.1 · NetworkPolicy hierarchy",
            h2="AdminNetworkPolicy + NetworkPolicy + Baseline",
            body_html="""    <p>K8s 1.30+ ships <strong>AdminNetworkPolicy (ANP)</strong> + <strong>BaselineAdminNetworkPolicy (BANP)</strong> as cluster-scoped CRDs alongside namespaced <strong>NetworkPolicy (NP)</strong>:</p>
    <ul>
      <li><strong>AdminNetworkPolicy</strong>: org-wide rules with explicit Pass / Allow / Deny + numeric priority. Set by platform team. Examples: \"deny all egress to RFC-1918 from prod namespace,\" \"allow all from observability namespace.\"</li>
      <li><strong>NetworkPolicy</strong>: namespaced; team-owned; default-deny + explicit allow. Cannot override AdminNetworkPolicy Deny rules.</li>
      <li><strong>BaselineAdminNetworkPolicy</strong>: cluster-scoped default rules below NP. Examples: \"by default allow DNS to kube-system\" so app teams don\'t need to declare it.</li>
    </ul>
    <p>Precedence: ANP &gt; NP &gt; BANP. The hierarchy lets platform enforce non-negotiable rules; teams refine within bounds.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · default-deny baseline + explicit allow",
            h2="The cluster\'s posture is no traffic by default",
            body_html="""    <p><strong>Default-deny</strong>: in every namespace, ship a base NetworkPolicy denying all ingress + egress. Then add explicit allow per consumer / per destination. Patterns:</p>
    <ul>
      <li><strong>Ingress allow</strong>: <code>podSelector: {app: api}; ingress: [{from: [{namespaceSelector: {team: web}}]}]</code> — only web team\'s namespace may call api Pods.</li>
      <li><strong>Egress allow</strong>: <code>egress: [{to: [{namespaceSelector: {kube-system: true}}], ports: [{port: 53}]}]</code> — DNS only.</li>
      <li><strong>FQDN egress</strong> (Cilium / Calico extensions): <code>toFQDNs: [\"api.stripe.com\"]</code> — egress to specific external services without IP enumeration.</li>
    </ul>
    <p>At scale, default-deny is unmaintainable as bespoke per-team work — generate from service catalog metadata or use mesh AuthorizationPolicy as L7 complement.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · egress gateway pattern",
            h2="All cluster egress through one path; auditable",
            body_html="""    <p><strong>Egress gateway</strong>: a node group + Pods designated to handle <em>all</em> outbound cluster traffic. Patterns:</p>
    <ul>
      <li><strong>Cilium egress gateway</strong>: per-namespace / per-Pod-selector route to a designated gateway node; outbound traffic SNAT\'d through that node\'s IP.</li>
      <li><strong>Istio egress gateway</strong>: mesh routes outbound through an egress proxy; L7 inspection + TLS origination.</li>
      <li><strong>Cloud-native</strong>: NAT gateway + IP allowlist per workload (rate limit / log).</li>
    </ul>
    <p>Wins: <em>fixed source IP</em> for partner allowlisting; <em>full audit log</em> of egress destinations; <em>L7 inspection</em> if mesh-based; <em>blocklist for known-bad CIDRs</em>; <em>compliance evidence</em>.</p>
    <p>Gotcha: gateway becomes single point of egress congestion; deploy redundant + autoscale.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · private clusters + hybrid connectivity",
            h2="apiserver isolation + on-prem connectivity",
            body_html="""    <p><strong>Private clusters</strong> (cloud terms vary):</p>
    <ul>
      <li><em>EKS</em>: <code>endpointPrivateAccess: true</code> + <code>endpointPublicAccess: false</code>. Access via VPN / DX / SSM / bastion.</li>
      <li><em>GKE</em>: private cluster + master authorized networks; Private Service Connect for apiserver.</li>
      <li><em>AKS</em>: private cluster + Private Endpoint for apiserver; Azure Bastion access.</li>
    </ul>
    <p><strong>Hybrid connectivity</strong>:</p>
    <ul>
      <li><strong>AWS</strong>: Direct Connect (DX) + DX Gateway + Transit Gateway. Bandwidth dedicated; predictable latency.</li>
      <li><strong>Azure</strong>: ExpressRoute + ER Gateway + vWAN. Similar shape.</li>
      <li><strong>GCP</strong>: Cloud Interconnect + Cloud Router. Per-region attachments.</li>
      <li><strong>VPN</strong>: site-to-site IPsec for lower-bandwidth or backup paths.</li>
    </ul>
    <p>Combine with private cluster + AdminNetworkPolicy: cluster apiserver only reachable via the corporate network; cluster egress goes through DX / ER + corporate firewalls.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A team\'s NetworkPolicy says \"allow ingress from team-X\" but ANP says \"deny ingress from team-X to prod namespace.\" Which wins?",
            options=[
                ("Team NP wins (more specific).", False),
                ("ANP Deny rule wins; NP cannot override.", True),
                ("Both apply.", False),
            ],
            feedback="Precedence: AdminNetworkPolicy &gt; NetworkPolicy. ANP Deny is non-negotiable; NP refines within ANP bounds.",
        ),
        3: PauseCheck(
            question="Why deploy egress through a gateway instead of letting every Pod egress directly?",
            options=[
                ("Mandatory by K8s.", False),
                ("Fixed source IP for partner allowlist + full audit + L7 inspection + blocklists.", True),
                ("Faster.", False),
            ],
            feedback="Egress gateway gives auditable + controllable + fixed-source-IP egress. Critical for compliance + partner integrations + threat detection.",
        ),
    },
    before_after_before='<p>Pre-policy clusters had open egress + flat ingress. Compromised Pod → free outbound to anywhere; lateral movement across all Pods.</p>',
    before_after_after='<p>Modern: AdminNetworkPolicy (org-wide) > NetworkPolicy (team) + default-deny + egress gateway + private cluster + hybrid VPN/DX. Compromise stops at the namespace boundary; egress to known destinations only.</p>',
    before_after_caption='<p class="ba-caption"><em>Default-deny everywhere; explicit allow at scale via service catalog + AdminNetworkPolicy hierarchy.</em></p>',
    analogy_intro_html='''<p>The Customs + Tollbooth marks the cluster\'s borders. A <strong>federal customs office</strong> (AdminNetworkPolicy) sets non-negotiable rules — no traffic to RFC-1918 from prod, no traffic from sandbox to prod ever. Each <strong>team\'s tollbooth</strong> (NetworkPolicy) refines within those rules — \"my namespace accepts ingress from web; egress to api.stripe.com.\"</p>
    <p>Outbound traffic from the city flows through one <strong>customs gate</strong> (egress gateway) — every export logged + checked against the export ledger. The city\'s diplomatic gate (apiserver) is private — only reachable from the corporate diplomatic network (DX / ExpressRoute / VPN).</p>''',
    translation_rows=[
        ("Federal customs office", "AdminNetworkPolicy (cluster-scoped)"),
        ("Team tollbooth", "NetworkPolicy (namespaced)"),
        ("Standing default rules", "BaselineAdminNetworkPolicy"),
        ("Customs gate (export logged)", "Egress gateway (Cilium / Istio / cloud NAT)"),
        ("Allow-list of partner ports", "FQDN egress / partner allowlist"),
        ("Diplomatic gate", "Private apiserver (PSC / Private Endpoint)"),
        ("Diplomatic network connection", "Direct Connect / ExpressRoute / Cloud Interconnect"),
        ("Backup diplomatic line", "Site-to-site VPN"),
    ],
    analogy_stops="A real customs office has paper records; cluster egress logs flow through SIEM; verify with synthetic egress probes.",
    eli5="Three layers of border control. Federal rules nobody overrides. Team rules within those. One gate where all exports go through with logging. The leadership office is private — only reachable from headquarters.",
    eli10="<strong>AdminNetworkPolicy</strong> > <strong>NetworkPolicy</strong> > <strong>BaselineAdminNetworkPolicy</strong> precedence. Default-deny + explicit allow. <strong>Egress gateway</strong> (Cilium / Istio / cloud-NAT) for fixed source IP + audit. <strong>Private cluster</strong> apiserver (EKS endpointPrivateAccess / GKE PSC / AKS Private Endpoint). <strong>Hybrid</strong> via DX / ExpressRoute / Cloud Interconnect / VPN.",
    scenarios=[
        Scenario(
            name="Org-wide ANP with team NP refinement",
            body="A 200-engineer org sets cluster-wide ANP: \"deny ingress from sandbox-* to prod-*; deny egress to RFC-1918 from prod-*.\" Team NPs refine within this; sandbox can\'t accidentally reach prod even with permissive team NP.",
        ),
        Scenario(
            name="Cilium egress gateway for partner allowlist",
            body="Stripe required allowlisting source IPs. Cilium egress gateway routed all <code>app=billing</code> Pod egress through gateway nodes with elastic IPs. Stripe allowlist receives single IP set; rotation handled at gateway.",
        ),
        Scenario(
            name="Private GKE + Cloud Interconnect",
            body="A regulated team\'s GKE cluster has private apiserver + private nodes. Cloud Interconnect between corporate DC + GCP VPC; cluster reachable only from corporate network. Public Internet egress via egress gateway with allowlisted destinations.",
        ),
        Scenario(
            name="Outage — egress gateway single point",
            body="Egress gateway with single Pod replicas; OOM during traffic spike; cluster lost outbound for 4 minutes. Postmortem: HPA on gateway + minimum 3 replicas + node anti-affinity. Updated runbook.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Default-deny is too restrictive for development.\"",
            truth="Dev clusters benefit too — finds missing allow rules early before production. Train developer instinct via dev-cluster default-deny; prod is the same shape.",
        ),
        Misconception(
            myth="\"AdminNetworkPolicy replaces NetworkPolicy.\"",
            truth="They\'re complementary. ANP for org-wide non-negotiable rules; NP for team-scoped allow rules within ANP bounds; BANP for defaults below NP. Three-tier hierarchy.",
        ),
        Misconception(
            myth="\"Private cluster eliminates need for NetworkPolicy.\"",
            truth="Private apiserver protects the control plane; NetworkPolicy protects Pod-to-Pod. Both required; private apiserver doesn\'t prevent lateral movement inside the cluster.",
        ),
    ],
    flashcards=[
        Flashcard(front="K8s NetworkPolicy hierarchy?", back="<strong>AdminNetworkPolicy (ANP)</strong> &gt; <strong>NetworkPolicy (NP)</strong> &gt; <strong>BaselineAdminNetworkPolicy (BANP)</strong>. ANP cluster-scoped with priority + Allow/Pass/Deny; NP namespaced; BANP cluster defaults."),
        Flashcard(front="Default-deny baseline — what does it look like?", back="Per-namespace base NetworkPolicy: <code>policyTypes: [Ingress, Egress]</code> with empty <code>ingress:</code> + empty <code>egress:</code>. All traffic denied; explicit allow rules added per consumer."),
        Flashcard(front="FQDN egress — who supports it?", back="Cilium + Calico extensions support <code>toFQDNs</code> in NetworkPolicy. Resolves DNS + tracks IPs; allows egress to specific external services without enumerating IPs."),
        Flashcard(front="Egress gateway — three implementation patterns?", back="<strong>Cilium egress gateway</strong> (per-Pod-selector SNAT through designated nodes); <strong>Istio egress gateway</strong> (mesh L7 + TLS origination); <strong>cloud-native</strong> (NAT gateway + per-workload allowlist)."),
        Flashcard(front="Private cluster components per cloud?", back="<strong>EKS</strong>: endpointPrivateAccess + endpointPublicAccess=false. <strong>GKE</strong>: private cluster + Private Service Connect. <strong>AKS</strong>: private cluster + Private Endpoint."),
        Flashcard(front="Hybrid connectivity options?", back="<strong>AWS Direct Connect</strong> (+ DX Gateway + Transit Gateway), <strong>Azure ExpressRoute</strong>, <strong>GCP Cloud Interconnect</strong>. <strong>VPN</strong> for backup or lower-bandwidth."),
        Flashcard(front="Why egress through a gateway helps compliance?", back="(1) Single source IP for partner allowlists. (2) Full audit log of egress destinations. (3) Blocklist enforcement at one place. (4) L7 inspection (mesh-based). All map to compliance controls (PCI 1.2 / 1.3, HIPAA §164.312(e))."),
        Flashcard(front="ANP priority ordering?", back="ANP rules ordered by numeric <code>priority</code>; lower number = higher precedence. Explicit Pass / Allow / Deny actions; Pass defers to NP."),
    ],
    quizzes=[
        Quiz(
            prompt="A team has flat NetworkPolicy across 30 namespaces. Audit asks for default-deny + explicit allow. Walk migration steps.",
            answer="(1) <strong>Audit traffic</strong>: Hubble / Cilium flow logs collected over 2 weeks; per-namespace ingress / egress patterns. (2) <strong>Generate baseline NetworkPolicies</strong>: per namespace, default-deny + observed-allow rules. (3) <strong>Stage in dev</strong>: roll one namespace; observe broken paths; refine. (4) <strong>Add ANP at cluster level</strong>: org-wide deny rules (no prod ingress from sandbox; no egress to RFC-1918 from prod). (5) <strong>BANP defaults</strong>: \"all Pods can egress to kube-system DNS\" so teams don\'t re-declare. (6) <strong>Roll prod</strong>: per-namespace; observe; iterate. (7) <strong>Tooling</strong>: NetworkPolicy generator from observed flows (network-policy-generator, krew np-viewer).",
        ),
        Quiz(
            prompt="A compromised Pod attempts egress to a crypto-miner pool. The cluster has default-deny egress + egress gateway. Walk the detection + response.",
            answer="(1) <strong>NetworkPolicy</strong> blocks the egress at namespace boundary; Pod gets connection-refused; logs the failure. (2) <strong>Egress gateway</strong> (if Pod\'s namespace allows egress to gateway): gateway logs the destination IP / hostname; matched against blocklist (Spamhaus / threat intel feeds); blocked at gateway too. (3) <strong>Hubble flow log</strong> records the dropped flow + verdict reason. (4) <strong>SIEM rule</strong> on \"egress denied to threat-intel-listed CIDR\" alerts on-call. (5) <strong>IR runbook</strong>: cordon node, isolate Pod via NP drop-all, snapshot for forensics, replace from clean image. <strong>Layered defence</strong>: NetPol catches at namespace; egress gateway catches at cluster; SIEM catches as alert; IR runbook closes the loop.",
        ),
        Quiz(
            prompt="A team wants to skip the ANP layer — \"NetworkPolicy is enough.\" Defend ANP.",
            answer="\"<strong>NetworkPolicy alone has two failure modes that ANP closes.</strong> (1) <strong>Team-scoped vs org-wide</strong>: NP is per-namespace; if a team makes a permissive NP, no cluster-wide enforcement says \"actually, you can\'t allow that.\" ANP gives platform a non-negotiable layer. (2) <strong>Compliance posture</strong>: regulators want \"the org enforces X\"; per-team NPs are \"each team enforces their own X\" — much weaker evidence. ANP makes the org-level posture explicit + auditable. (3) <strong>Default + override pattern</strong>: BANP provides cluster defaults; teams override via NP; ANP enforces what teams cannot override. <strong>The 3-tier hierarchy mirrors how org IT actually works</strong>: org policy + team config + sane defaults. NP-only collapses this into one layer that doesn\'t scale.\"",
            cyoa=True,
            cyoa_tag="how the network architect defended ANP",
        ),
    ],
    glossary=[
        GlossaryItem(name="NetworkPolicy (NP)", definition="Namespaced K8s CRD; default-deny + explicit allow ingress / egress."),
        GlossaryItem(name="AdminNetworkPolicy (ANP)", definition="Cluster-scoped CRD; org-wide rules with priority + Allow/Pass/Deny actions."),
        GlossaryItem(name="BaselineAdminNetworkPolicy (BANP)", definition="Cluster-scoped CRD; default rules below NP. Set up by platform; teams override via NP."),
        GlossaryItem(name="default-deny", definition="Per-namespace base NetworkPolicy denying all ingress + egress. Foundation of zero-trust K8s."),
        GlossaryItem(name="FQDN egress", definition="Cilium / Calico extension allowing egress to specific DNS names without enumerating IPs."),
        GlossaryItem(name="egress gateway", definition="Designated node group routing all cluster egress; fixed source IP + audit + L7 inspection."),
        GlossaryItem(name="private cluster", definition="apiserver private (PSC / Private Endpoint / VPC-only); nodes private. Access via VPN / DX / bastion."),
        GlossaryItem(name="Direct Connect / ExpressRoute / Cloud Interconnect", definition="Cloud-to-on-prem dedicated network paths. Bandwidth + predictable latency."),
        GlossaryItem(name="ipFamilyPolicy", definition="(NB: from N4) Service spec field for v4/v6 stack mode."),
        GlossaryItem(name="SNAT", definition="Source NAT; egress gateway rewrites source IP to gateway\'s IP for fixed-source-IP partner allowlisting."),
    ],
    recap_lead="Three-tier NetPol hierarchy (ANP > NP > BANP) + default-deny + egress gateway + private cluster + hybrid connectivity. Lateral movement contained at namespace; egress audited; apiserver isolated; on-prem connected.",
    recap_next='<strong>Next — N6: Packet tracing + performance tuning.</strong> Hubble + Pixie + Tetragon + tcpdump + kubectl-trace + kube-burner. Common findings: MTU mismatch, conntrack saturation, kernel scheduling.',
)
