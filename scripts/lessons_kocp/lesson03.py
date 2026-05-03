"""K-OCP O3 — OpenShift Networking (OVN-K, Routes vs Ingress vs Gateway API, MetalLB, Multus, NetObserv)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OCP networking — OVN-K, Routes/Ingress/Gateway, NetworkPolicy/EgressIP, Multus, MetalLB, Submariner, NetObserv.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Pipework &amp; Conveyors — networking surfaces</text>
  <rect x="40" y="65" width="170" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="125" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">CNI &amp; networks</text>
  <text x="125" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">OVN-Kubernetes (default)</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">cluster / service / machine</text>
  <text x="125" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">network ranges</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">SDN removed</text>
  <rect x="225" y="65" width="170" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="310" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">ingress</text>
  <text x="310" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">Route (TLS edge / pass / re-enc)</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Ingress (K8s standard)</text>
  <text x="310" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">Gateway API + Istio</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">IngressController + Router pods</text>
  <rect x="410" y="65" width="170" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="495" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">policy &amp; egress</text>
  <text x="495" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">NetworkPolicy</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">AdminNetworkPolicy</text>
  <text x="495" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">EgressIP / Egress firewall</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">Egress router</text>
  <rect x="595" y="65" width="125" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="657" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">specialty</text>
  <text x="657" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">Multus (multi-net)</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">SR-IOV · DPDK</text>
  <text x="657" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">MetalLB · NMState</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">Submariner · NetObserv</text>
</svg>"""


LESSON = LessonSpec(
    num="03", title_short="OCP networking",
    title_full="O3 · OpenShift Networking (OVN-K, Routes vs Ingress vs Gateway, NetworkPolicy, MetalLB, Multus, NetObserv)",
    title_html="K-OCP O3 · OpenShift Networking",
    module_eyebrow="Module O3 · the Pipework &amp; Conveyors",
    hero_sub_html='<strong>OVN-Kubernetes</strong> (default; OpenShift SDN removed). Cluster / service / machine networks. <strong>IngressController + Router pods</strong>; <strong>Routes</strong> (TLS edge / passthrough / re-encrypt) vs <strong>Ingress</strong> vs <strong>Gateway API + Istio</strong>. <strong>NetworkPolicy</strong> + <strong>EgressIP</strong> + <strong>Egress firewall</strong> + <strong>Egress router</strong>. <strong>Multus</strong> for multiple networks; <strong>SR-IOV / DPDK</strong> for telco / NFV; <strong>NMState</strong>. <strong>MetalLB Operator</strong> for bare-metal LoadBalancer. <strong>Submariner</strong> for multi-cluster. <strong>NetObserv</strong> (eBPF flow visibility).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"Routes returning 503; IngressController CO degraded.\"</em> Router pods crash-looping. <code>oc get co/ingress -o yaml</code> shows degraded but no clear cause. The Route\'s TLS edge cert is valid; the backing Service has Endpoints; the Pod is Ready. <em>You don\'t know whether it\'s OVN-Kubernetes routing, NetworkPolicy blocking, EgressIP misconfigured, or a Router-level config drift.</em> Today\'s lesson: OCP networking surfaces — CNI, ingress, policy, specialty.",
    stamp_html="<strong>OVN-Kubernetes is default; SDN is removed. Routes for TLS-aware ingress; Gateway API for modern multi-cluster. NetworkPolicy + EgressIP + Egress firewall for control. Multus + SR-IOV for telco. MetalLB for bare-metal LoadBalancer. NetObserv for flow visibility.</strong>",
    district_pin="ko-bay03", district_label="Pipework &amp; Conveyors",
    sections=[
        Section(eyebrow="Section 1.1 · OVN-Kubernetes + networks", h2="OVN-Kubernetes + cluster/service/machine networks",
            body_html="""    <p><strong>OVN-Kubernetes</strong> is OCP\'s default CNI (default since OCP 4.12; OpenShift SDN was deprecated and is now removed). Built on Open Virtual Network (OVN) + Open vSwitch (OVS). Provides:</p>
    <ul>
      <li>Pod networking (cluster network)</li>
      <li>Service networking (kube-proxy replacement using OVN)</li>
      <li>NetworkPolicy enforcement</li>
      <li>EgressIP, Egress firewall, Egress router CRDs</li>
      <li>Multi-network via Multus integration</li>
      <li>IPv6 + dual-stack</li>
    </ul>
    <p><strong>Three network ranges</strong> defined at install time:</p>
    <ul>
      <li><strong>Cluster network</strong> (Pod CIDR) — default <code>10.128.0.0/14</code>. Pods get IPs from here.</li>
      <li><strong>Service network</strong> (Service CIDR) — default <code>172.30.0.0/16</code>. ClusterIP Services from here.</li>
      <li><strong>Machine network</strong> (host network) — the actual VM/host subnet. Nodes have IPs here.</li>
    </ul>
    <p>Plan ranges generously at install — the cluster network is hard to expand later. Default <code>/14</code> = 256K Pod IPs which is plenty for most. Larger clusters need explicit planning.</p>"""),
        Section(eyebrow="Section 1.2 · Routes + Ingress + Gateway API", h2="Routes + Ingress + Gateway API — three ingress paths",
            body_html="""    <p><strong>Route</strong> = OpenShift\'s ingress primitive (predates K8s Ingress). Configured by the <strong>IngressController</strong> Operator + <strong>Router pods</strong> (HAProxy-based by default). Three TLS termination modes:</p>
    <ul>
      <li><strong>Edge termination</strong> — TLS terminates at the Router; Pod traffic is HTTP. Cert lives on the Route or Router default.</li>
      <li><strong>Passthrough</strong> — TLS passes through Router untouched. Pod terminates TLS itself (e.g. mTLS apps).</li>
      <li><strong>Re-encrypt</strong> — Router terminates the inbound TLS, then re-encrypts to Pod with a separate cert. For Pod-side TLS without sharing the public cert.</li>
    </ul>
    <p><strong>Ingress</strong> (K8s standard) — also supported in OCP. The Ingress controller maps Ingress objects to Routes under the hood. Use Ingress for portability across clusters; Routes for OCP-specific TLS termination flexibility.</p>
    <p><strong>Gateway API</strong> — OpenShift Service Mesh (Istio-based) + Gateway API support. Gateway / GatewayClass / HTTPRoute / TCPRoute. Modern path; for new ingress in OCP 4.13+ on Service Mesh.</p>
    <p><strong>IngressController CRD</strong> — defines the public ingress(es). Default created at install. Add additional IngressControllers for sharded ingress (per-namespace, per-domain, internal-only LB on bare metal, etc.).</p>"""),
        Section(eyebrow="Section 1.3 · NetworkPolicy + EgressIP + Egress firewall", h2="NetworkPolicy + EgressIP + Egress firewall + Egress router",
            body_html="""    <p><strong>NetworkPolicy</strong> (K8s standard) — namespace-scoped Pod-to-Pod allow/deny. Default is allow-all; apply default-deny per Project for zero-trust. Works on OVN-Kubernetes natively.</p>
    <p><strong>AdminNetworkPolicy + BaselineAdminNetworkPolicy</strong> (newer K8s standard) — cluster-wide admission policies for network rules. Override per-namespace NetworkPolicies. Useful for enforcing org-wide deny-egress-to-internet baselines.</p>
    <p><strong>EgressIP</strong> (CRD) — assign a deterministic source IP to traffic egressing from a Project. Useful when an external system whitelists by source IP. The egress IP attaches to a specific node; OCP fails it over to another node if the host fails.</p>
    <p><strong>Egress firewall</strong> (CRD) — restrict which external IPs/domains a Project can talk to. CIDR-based or DNS-name-based rules. Blocks egress at the OVN-K layer.</p>
    <p><strong>Egress router</strong> (CRD) — older mechanism: a dedicated Pod that source-NATs egress traffic to a fixed IP. EgressIP is preferred; Egress router still exists for niche cases.</p>"""),
        Section(eyebrow="Section 1.4 · Multus + SR-IOV + MetalLB + NetObserv + Submariner",
            h2="Multus + SR-IOV / DPDK + MetalLB + NetObserv + Submariner",
            body_html="""    <p><strong>Multus CNI</strong> — attach Pods to <em>multiple networks</em>. The default cluster network plus 1+ additional networks defined as <code>NetworkAttachmentDefinition</code>. For Pods needing direct bridge to a VLAN, SR-IOV adapter, or secondary VPC.</p>
    <p><strong>SR-IOV + DPDK</strong> — Single Root I/O Virtualization gives Pods direct hardware access to a NIC virtual function (VF). DPDK runs network stack in userspace. <em>For telco / NFV: 5G UPF, vRouter, low-latency packet processing.</em> SR-IOV Operator manages VFs.</p>
    <p><strong>NMState Operator</strong> — declarative host-network configuration. <code>NodeNetworkConfigurationPolicy</code> (NNCP) defines bonding, VLANs, bridges, etc., applied per node group. Replaces hand-edited NetworkManager configs.</p>
    <p><strong>MetalLB Operator</strong> — LoadBalancer Service support on bare-metal clusters (no cloud LB available). L2 mode (ARP/NDP) or BGP mode. Address pools allocate VIPs.</p>
    <p><strong>Submariner</strong> — multi-cluster networking: Pod IPs and Services routable across registered clusters. For multi-cluster service mesh + DR.</p>
    <p><strong>NetObserv (Network Observability) Operator</strong> — eBPF-based flow capture. Visualises east-west traffic, NetworkPolicy drops, DNS lookups in the OCP console. Storage backed by Loki (or external).</p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A Project needs all egress traffic to use a fixed source IP for an external API\'s allowlist. What\'s the OCP CRD?",
        options=[("NetworkPolicy.", False),
            ("EgressIP — assigns a deterministic source IP for the Project\'s egress; OVN-K handles failover if the holding node fails.", True),
            ("Route.", False)],
        feedback="EgressIP is the deterministic-source-IP-for-egress primitive. NetworkPolicy controls allow/deny, not source-IP rewriting.",
    )},
    before_after_before='<p>Pre-OVN-K, OCP used OpenShift SDN (now removed). OCP-specific Egress features didn\'t exist; for fixed source IP you ran a sidecar SOCKS proxy. Bare-metal had no LoadBalancer; you used NodePort + external HAProxy. Multi-network was DIY. NetObserv was bring-your-own (Hubble or DIY tcpdump).</p>',
    before_after_after='<p>Modern OCP networking: <strong>OVN-Kubernetes default</strong> + cluster/service/machine networks; <strong>Routes</strong> (TLS edge/pass/re-enc) + <strong>Ingress</strong> + <strong>Gateway API</strong>; <strong>NetworkPolicy</strong> + <strong>EgressIP</strong> + <strong>Egress firewall</strong>; <strong>Multus + SR-IOV + DPDK</strong> for telco; <strong>MetalLB Operator</strong> for bare-metal LB; <strong>Submariner</strong> for multi-cluster; <strong>NetObserv</strong> for eBPF flow visibility.</p>',
    before_after_caption='<p class="ba-caption"><em>OCP networking is now coherent: one CNI (OVN-K), three ingress paths (Routes / Ingress / Gateway API), policy + egress + observability all first-class.</em></p>',
    analogy_intro_html='''<p>The <strong>Pipework &amp; Conveyors</strong> are the foundry\'s hidden infrastructure. The <strong>OVN-Kubernetes Conveyor System</strong> is the standardized rail network — every cart (Pod) gets an address (IP from cluster network); every workstation (Service) gets a virtual address (Service network); the foundry floor itself sits on the machine network.</p>
    <p>Visitors enter through one of three door types: the classic <strong>Route Door</strong> (Foundry-Master-built; TLS edge/passthrough/re-encrypt termination right at the door), the standard <strong>Ingress Door</strong> (K8s-portable but mapped to a Route under the hood), or the modern <strong>Gateway Door</strong> (Gateway API + Istio for service-mesh ingress).</p>
    <p>Inside, the Foundry has <strong>traffic policies</strong>: NetworkPolicy controls which carts can drive between which workstations; EgressIP gives a Project\'s outbound carts a fixed plate (source IP); Egress firewall whitelists which external addresses carts can reach.</p>
    <p>Specialty pipework: <strong>Multus</strong> (multi-track carts wired to multiple networks); <strong>SR-IOV / DPDK</strong> (direct-rail express trains for ultra-low-latency telco workloads); <strong>MetalLB</strong> (bare-metal LB-on-rails); <strong>Submariner</strong> (cross-foundry rail network); <strong>NetObserv</strong> (eBPF flow camera over every rail).</p>''',
    translation_rows=[
        ("OVN-Kubernetes Conveyor System", "OVN-K CNI (default; OCP 4.12+)"),
        ("Cart address", "Pod IP (from cluster network)"),
        ("Workstation virtual address", "Service IP (from service network)"),
        ("Foundry floor address", "Node IP (from machine network)"),
        ("Route Door", "OpenShift Route (TLS edge/pass/re-encrypt)"),
        ("Ingress Door", "K8s Ingress (mapped to Route under the hood)"),
        ("Gateway Door", "Gateway API + OpenShift Service Mesh (Istio)"),
        ("Door operator", "IngressController + Router pods (HAProxy)"),
        ("Inter-station traffic policy", "NetworkPolicy (K8s standard)"),
        ("Cluster-wide policy override", "AdminNetworkPolicy / BaselineAdminNetworkPolicy"),
        ("Fixed plate for outbound carts", "EgressIP (CRD)"),
        ("Allowed external addresses list", "Egress firewall (CRD)"),
        ("Multi-track cart", "Multus + NetworkAttachmentDefinition"),
        ("Express telco rail", "SR-IOV + DPDK"),
        ("Bare-metal LB-on-rails", "MetalLB Operator"),
        ("Cross-foundry rail link", "Submariner"),
        ("Foundry flow camera", "NetObserv (eBPF) Operator"),
    ],
    analogy_stops="A real foundry has fixed pipework; OVN-K is software-defined and reshapes per Pod. SDN-removal means existing OpenShift SDN clusters need migration — an operational lift the metaphor doesn\'t capture.",
    eli5="The factory has invisible rails (network) connecting workstations. Visitors come through doors — the Foundry-Master-built doors handle the TLS keys; standard doors are simpler but map to the same backend. Some carts wear special license plates so the outside world recognises them.",
    eli10="OCP networking = OVN-K CNI (default; SDN removed) + three IP ranges (cluster/service/machine networks). Three ingress paths: Routes (TLS edge/pass/re-enc native), Ingress (K8s portable, maps to Route), Gateway API (Service Mesh modern). Policy + egress: NetworkPolicy / AdminNetworkPolicy / EgressIP / Egress firewall / Egress router. Specialty: Multus multi-net, SR-IOV/DPDK telco, MetalLB bare-metal LB, Submariner multi-cluster, NetObserv eBPF flow visibility, NMState declarative host networking.",
    scenarios=[
        Scenario(name="Bank — EgressIP + Egress firewall for outbound API allowlist",
            body="A bank\'s payment Project must call an external partner API that whitelists by source IP. EgressIP assigns a fixed IP to the Project; Egress firewall restricts the Project\'s egress to only the partner\'s API range. <em>Compliance-mandated allowlist enforced at the cluster network layer.</em>"),
        Scenario(name="Telco — SR-IOV + DPDK for 5G UPF",
            body="Telco running 5G User Plane Function on OCP. Pods need wire-speed packet processing. SR-IOV Operator allocates NIC VFs to UPF Pods; DPDK userspace network stack inside the Pod. Sub-millisecond latency; line-rate throughput. <em>OCP carries telco workloads alongside enterprise workloads on the same platform.</em>"),
        Scenario(name="Bare metal — MetalLB BGP for LoadBalancer Services",
            body="Bare-metal OCP cluster needs <code>type: LoadBalancer</code> Services. MetalLB Operator with BGP mode peers with the data-center spine routers; advertises VIPs from a configured pool. Failover handled at L3 routing layer. <em>Cloud-style LoadBalancer on bare metal.</em>"),
        Scenario(name="Multi-cluster failover — Submariner connects Routes across regions",
            body="Active-active OCP deployment in two regions. Submariner extends Pod + Service networking across both clusters. ServiceExport in cluster A makes a Service reachable from cluster B. Failover routes traffic across regions transparently. <em>Multi-cluster service mesh without per-region DNS choreography.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"OpenShift SDN still works; we can stay on it.\"",
            truth="OpenShift SDN is <strong>removed</strong> (no longer ships in modern OCP minors). Existing SDN clusters MUST migrate to OVN-Kubernetes via documented migration. <em>Plan + execute the migration on a defined schedule</em>; it\'s not optional."),
        Misconception(myth="\"Routes and Ingress do exactly the same thing.\"",
            truth="Routes have OCP-specific TLS termination flexibility (edge / passthrough / re-encrypt) and OCP-native annotations (haproxy timeouts, balance, etc.). Ingress is K8s-portable but maps to Routes via the IngressController under the hood. For OCP-specific TLS modes, use Route directly; for portable manifests, use Ingress."),
        Misconception(myth="\"NetworkPolicy is enough; I don\'t need Egress firewall.\"",
            truth="NetworkPolicy controls allow/deny at the cluster boundary by Pod selector. <strong>Egress firewall</strong> restricts a Project\'s egress to specific <em>external</em> CIDRs / DNS names — useful for compliance \"only call these external APIs.\" They\'re complementary, not duplicates."),
    ],
    flashcards=[
        Flashcard(front="OCP\'s default CNI?", back="<strong>OVN-Kubernetes</strong> (since OCP 4.12; SDN removed). OVN + OVS. Pod networking + Service networking + NetworkPolicy + EgressIP + Egress firewall + Multus integration."),
        Flashcard(front="Three OCP network ranges?", back="<strong>Cluster network</strong> (Pod CIDR; default 10.128.0.0/14), <strong>Service network</strong> (Service CIDR; default 172.30.0.0/16), <strong>Machine network</strong> (host subnet; nodes\' IPs)."),
        Flashcard(front="Three Route TLS termination modes?", back="<strong>Edge</strong> — TLS terminates at Router; Pod gets HTTP. <strong>Passthrough</strong> — TLS passes through; Pod terminates. <strong>Re-encrypt</strong> — Router terminates inbound TLS then re-encrypts to Pod with separate cert."),
        Flashcard(front="EgressIP — what does it do?", back="Assigns a deterministic source IP to a Project\'s egress traffic. Used when external systems whitelist by source IP. OVN-K handles failover if the holding node fails."),
        Flashcard(front="Egress firewall vs NetworkPolicy?", back="<strong>NetworkPolicy</strong> = Pod-to-Pod (in-cluster) allow/deny. <strong>Egress firewall</strong> = restricts Project\'s egress to specific <em>external</em> CIDRs / DNS names. Complementary; both common for zero-trust."),
        Flashcard(front="What does Multus give you?", back="Pods attached to <strong>multiple networks</strong> simultaneously. Default cluster network + 1+ additional networks defined as <code>NetworkAttachmentDefinition</code>. For VLANs / SR-IOV VFs / secondary VPCs."),
        Flashcard(front="When use SR-IOV + DPDK?", back="Telco / NFV workloads needing wire-speed packet processing — 5G UPF, vRouter, ultra-low-latency. SR-IOV Operator allocates NIC VFs; DPDK userspace network stack."),
        Flashcard(front="What is MetalLB Operator and when use it?", back="LoadBalancer Service support on <strong>bare-metal</strong> clusters (no cloud LB). L2 mode (ARP/NDP) or BGP mode. Address pools allocate VIPs. Required for <code>type: LoadBalancer</code> on bare-metal OCP."),
    ],
    quizzes=[
        Quiz(prompt="Routes return 503 across the cluster. Router pods are Running. Where do you look first?",
            answer="(1) <code>oc get co/ingress</code> — is the IngressController CO Available + not Degraded? (2) <code>oc get -n openshift-ingress pods</code> — Router pods Ready + recent restarts? (3) <code>oc logs -n openshift-ingress deployment/router-default</code> — Router runtime errors? (4) For specific Routes: <code>oc describe route &lt;name&gt;</code> — admitted by IngressController? cert valid? backing Service has Endpoints? (5) NetworkPolicy: is the Project denying ingress from openshift-ingress namespace? Add namespace label / explicit allow. (6) EgressIP / Egress firewall: blocking router-to-Pod path? <code>oc get egressfirewall -A</code>."),
        Quiz(prompt="A team needs an internal-only LoadBalancer Service exposed only to the corp network on a bare-metal OCP. Walk through the design.",
            answer="(1) Install MetalLB Operator + create MetalLB instance. (2) Define IPAddressPool with internal-only IPs (corporate VLAN range); set <code>autoAssign: false</code> so explicit allocation. (3) For BGP mode (recommended): create BGPPeer CR + BGPAdvertisement. For L2 mode: create L2Advertisement. (4) Create the Service with <code>type: LoadBalancer</code> + annotation <code>metallb.universe.tf/address-pool: internal-pool</code>. (5) MetalLB allocates a VIP from the internal pool; advertises via BGP/ARP. (6) Combine with NetworkPolicy to restrict Pod-side ingress; use EgressIP if the upstream restricts by source."),
        Quiz(prompt="Saturday. A DBA SSH-debugs a failed cross-region failover. They find Route on cluster A returns 200 but cluster B returns 503. Submariner installed, Service is exported. What\'s the diagnostic ladder?",
            answer="(1) <code>subctl diagnose all</code> — runs Submariner\'s built-in checks for connectivity, gateway health, IPsec tunnels. (2) Check Submariner gateway pods on both clusters: <code>oc get -n submariner-operator pods</code>. Tunnel UP? (3) <code>oc get serviceexport &lt;name&gt; -A</code> on cluster A — Exported + ServiceImport visible on cluster B? (4) On cluster B: try <code>oc exec</code> a Pod and curl the imported Service IP. If timeout: NetworkPolicy on B blocking the Pod from reaching the Submariner-imported Service. (5) Often: cross-cluster Service IP collision — Submariner needs distinct Service CIDRs across clusters. Plan at deploy time.",
            cyoa=True, cyoa_tag="how the failover got debugged"),
    ],
    glossary=[
        GlossaryItem(name="OVN-Kubernetes", definition="OCP\'s default CNI (since 4.12). Built on Open Virtual Network + Open vSwitch. Pod + Service networking + NetworkPolicy + EgressIP."),
        GlossaryItem(name="Cluster / Service / Machine network", definition="The three IP ranges OCP uses: Pod IPs / Service ClusterIPs / node hosts."),
        GlossaryItem(name="Route", definition="OCP ingress primitive. TLS edge / passthrough / re-encrypt termination. Programmed by IngressController + Router pods."),
        GlossaryItem(name="IngressController", definition="OCP CRD defining a public ingress. Default created at install. Add additional for sharded ingress."),
        GlossaryItem(name="Router pods", definition="HAProxy-based ingress pods that implement IngressController/Route routing. In openshift-ingress namespace."),
        GlossaryItem(name="EgressIP", definition="CRD assigning a deterministic source IP to a Project\'s egress. OVN-K handles failover."),
        GlossaryItem(name="Egress firewall", definition="CRD restricting a Project\'s egress to specific external CIDRs / DNS names. Enforced at OVN-K layer."),
        GlossaryItem(name="Multus CNI", definition="Pods attached to multiple networks. Default + NetworkAttachmentDefinition for additional."),
        GlossaryItem(name="SR-IOV Operator", definition="Manages NIC virtual functions for direct-hardware Pod networking. Telco / NFV workloads."),
        GlossaryItem(name="DPDK", definition="Data Plane Development Kit — userspace network stack for ultra-low-latency packet processing."),
        GlossaryItem(name="NMState Operator", definition="Declarative host-network configuration via NodeNetworkConfigurationPolicy."),
        GlossaryItem(name="MetalLB Operator", definition="LoadBalancer Service for bare-metal OCP. L2 (ARP/NDP) or BGP mode."),
        GlossaryItem(name="Submariner", definition="Multi-cluster networking — Pod + Service networking spans registered clusters."),
        GlossaryItem(name="NetObserv (Network Observability) Operator", definition="eBPF-based flow capture + visualisation in OCP console. Backed by Loki."),
    ],
    recap_lead='OVN-K + Routes/Ingress/Gateway + NetworkPolicy/EgressIP/Egress firewall + Multus/SR-IOV/MetalLB + Submariner + NetObserv. The Pipework + Conveyors map is internalised.',
    recap_next='<strong>Next — O4: OpenShift Security.</strong> OAuth providers + integrated OAuth server + LDAP/OIDC/HTPasswd; OCP RBAC + Security Context Constraints (SCCs) — restricted-v2 default; SCC vs PSA; Compliance Operator + File Integrity + Security Profiles; RHACS (StackRox); KMS + FIPS + sandboxed containers (Kata).',
)
