from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Inside the Switchboard: a network of veth pairs connecting Pods to a node bridge, the bridge plugged into a CNI router, and a node-to-node tunnel labeled VXLAN/native routing/eBPF.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">SWITCHBOARD · WIRING ROOM (CNI INSIDE)</text>
  <!-- Node A -->
  <g transform="translate(40,55)">
    <rect width="220" height="120" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="110" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">node-A</text>
    <!-- Pods with veth -->
    <rect x="14" y="22" width="50" height="38" rx="3" fill="#5A9F7A"/>
    <text x="39" y="42" text-anchor="middle" font-size="8" font-weight="700" fill="#FFFFFF">pod-1</text>
    <text x="39" y="52" text-anchor="middle" font-size="6" fill="#FFFFFF">10.1.1.4</text>
    <rect x="74" y="22" width="50" height="38" rx="3" fill="#5A9F7A"/>
    <text x="99" y="42" text-anchor="middle" font-size="8" font-weight="700" fill="#FFFFFF">pod-2</text>
    <text x="99" y="52" text-anchor="middle" font-size="6" fill="#FFFFFF">10.1.1.5</text>
    <rect x="134" y="22" width="50" height="38" rx="3" fill="#5A9F7A"/>
    <text x="159" y="42" text-anchor="middle" font-size="8" font-weight="700" fill="#FFFFFF">pod-3</text>
    <text x="159" y="52" text-anchor="middle" font-size="6" fill="#FFFFFF">10.1.1.6</text>
    <!-- veth pairs -->
    <line x1="39" y1="60" x2="39" y2="74" stroke="#3F4A5E" stroke-width="1.5"/>
    <text x="44" y="69" font-size="6" fill="#5A4F45" font-style="italic">veth</text>
    <line x1="99" y1="60" x2="99" y2="74" stroke="#3F4A5E" stroke-width="1.5"/>
    <line x1="159" y1="60" x2="159" y2="74" stroke="#3F4A5E" stroke-width="1.5"/>
    <!-- Bridge -->
    <rect x="14" y="74" width="170" height="22" rx="2" fill="#3F4A5E"/>
    <text x="99" y="89" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">cni0 / cilium_host</text>
    <!-- Out -->
    <line x1="184" y1="85" x2="220" y2="85" stroke="#A04832" stroke-width="2"/>
    <text x="100" y="113" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">veth pairs into a node bridge</text>
  </g>
  <!-- Tunnel -->
  <g transform="translate(260,80)">
    <text x="80" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">node ↔ node</text>
    <line x1="0" y1="40" x2="160" y2="40" stroke="#A04832" stroke-width="2.5" stroke-dasharray="6,4"/>
    <rect x="55" y="32" width="50" height="20" rx="3" fill="#FBE8DC" stroke="#A04832" stroke-width="1"/>
    <text x="80" y="46" text-anchor="middle" font-size="7" fill="#A04832" font-weight="700">VXLAN / native</text>
    <text x="80" y="68" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">CNI plugin's job</text>
  </g>
  <!-- Node B -->
  <g transform="translate(420,55)">
    <rect width="220" height="120" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="110" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">node-B</text>
    <rect x="14" y="22" width="50" height="38" rx="3" fill="#5A9F7A"/>
    <text x="39" y="42" text-anchor="middle" font-size="8" font-weight="700" fill="#FFFFFF">pod-4</text>
    <text x="39" y="52" text-anchor="middle" font-size="6" fill="#FFFFFF">10.1.2.4</text>
    <rect x="74" y="22" width="50" height="38" rx="3" fill="#5A9F7A"/>
    <text x="99" y="42" text-anchor="middle" font-size="8" font-weight="700" fill="#FFFFFF">pod-5</text>
    <text x="99" y="52" text-anchor="middle" font-size="6" fill="#FFFFFF">10.1.2.5</text>
    <rect x="134" y="22" width="50" height="38" rx="3" fill="#5A9F7A"/>
    <text x="159" y="42" text-anchor="middle" font-size="8" font-weight="700" fill="#FFFFFF">pod-6</text>
    <text x="159" y="52" text-anchor="middle" font-size="6" fill="#FFFFFF">10.1.2.6</text>
    <line x1="39" y1="60" x2="39" y2="74" stroke="#3F4A5E" stroke-width="1.5"/>
    <line x1="99" y1="60" x2="99" y2="74" stroke="#3F4A5E" stroke-width="1.5"/>
    <line x1="159" y1="60" x2="159" y2="74" stroke="#3F4A5E" stroke-width="1.5"/>
    <rect x="14" y="74" width="170" height="22" rx="2" fill="#3F4A5E"/>
    <text x="99" y="89" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">cni0 / cilium_host</text>
    <line x1="0" y1="85" x2="14" y2="85" stroke="#A04832" stroke-width="2"/>
  </g>
  <text x="340" y="200" text-anchor="middle" font-size="11" fill="#3F4A5E" font-style="italic">Every Pod → veth → node bridge → CNI's overlay or routing → another node's bridge → another Pod. That’s K8s networking, in nine words.</text>
</svg>"""

LESSON = LessonSpec(
    num="24",
    title_short="net foundations &amp; CNI",
    title_full="Networking Foundations · Linux Primitives, CNI, MTU",
    title_html="Lesson 24 — Networking Foundations & CNI · K-COM",
    module_eyebrow="Module 12 · Lesson 24 · what's actually under the Service abstraction",
    hero_sub_html='Lesson 17 introduced Services as if Pod IPs just exist. They don\'t — every Pod IP is a Linux interface plumbed through a series of primitives by a <strong>CNI plugin</strong>. Understanding that path is the difference between writing YAML and debugging real outages.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Inter-Pod traffic between Pods on different nodes is mysteriously slow — exactly 200ms tail latency. Same-node traffic is fine. SSH into a node, <code>ip link</code> shows the CNI bridge. <code>ip route</code> shows pod routes. <code>ifconfig</code> shows MTU 1500 on every interface. <em>The cluster runs VXLAN encapsulation</em> with an effective MTU of 1450. Every cross-node packet is hitting the underlay\'s 1500 limit, fragmenting, retransmitting. Engineer fixes by setting Pod-MTU 1450 on the CNI ConfigMap. Latency drops to 1.2ms. Lesson learned: K8s networking is just Linux networking with a million more namespaces, and MTU mismatches still kill you.',
    stamp_html='Every Pod gets a Linux <code>veth</code> pair pulled into a node bridge. The <strong>CNI plugin</strong> creates the veth, assigns the IP, and connects nodes (encapsulation or native routing). Modern CNIs (<strong>Cilium</strong>) use <strong>eBPF</strong> instead of iptables — much faster and more observable. The most common production bug: <strong>MTU mismatch</strong>.',
    district_pin="kt-pin17",
    district_label="Switchboard — Wiring Room",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="The Linux primitives behind every Pod",
            body_html="""    <p>K8s networking is not new infrastructure — it's <em>Linux networking applied at scale</em>. Each node is a regular Linux box with extra namespaces. Each Pod has its own <code>net</code> namespace (covered in Lesson 8) — its own loopback, its own routing table, its own iptables/nftables. The Pod sees a single network interface (<code>eth0</code>); the host sees its other end as a <code>veth</code> pair.</p>
    <p>The four primitives you need:</p>
    <ul>
      <li><strong><code>veth</code> pair</strong> — a virtual cable. One end is in the Pod's net namespace as <code>eth0</code>; the other is on the host. Whatever's sent into one end pops out the other.</li>
      <li><strong>Bridge</strong> (e.g., <code>cni0</code>, <code>cilium_host</code>) — a virtual L2 switch on the host. Every Pod's host-side veth plugs into it. Pods on the same node can talk to each other across the bridge with no further help.</li>
      <li><strong>Routing table</strong> — for cross-node traffic, the host's routing table must know "Pod 10.1.2.4 is on node-B." That entry is installed by the CNI plugin (or by BGP if the CNI uses native routing).</li>
      <li><strong>iptables / nftables / eBPF</strong> — packet rules: NAT for outbound traffic, Service load balancing (kube-proxy), NetworkPolicy enforcement.</li>
    </ul>
    <p>Run <code>ip link show</code>, <code>ip route show</code>, <code>iptables -t nat -L -n</code> on any K8s node and you see exactly this. K8s doesn't add anything new at the data-plane layer — it choreographs a thousand standard Linux pieces.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · CNI — the plugin contract",
            h2="One spec, many implementations",
            body_html="""    <p>The <strong>Container Network Interface (CNI)</strong> is a CNCF spec. Two roles: a <em>runtime</em> (the kubelet, in K8s) calls <em>plugins</em> (binaries on the node) at three lifecycle moments — ADD (set up Pod networking), DEL (tear down), CHECK (verify). The plugin's job: create the Pod's veth, assign an IP, set up routing. The runtime feeds back to K8s.</p>
    <p>The major CNI plugins:</p>
    <table class="data-table">
      <thead><tr><th>Plugin</th><th>Style</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>Cilium</td><td>eBPF, native routing or VXLAN</td><td>Fastest, best observability, supersedes kube-proxy. De-facto modern choice.</td></tr>
        <tr><td>Calico</td><td>BGP routing, optional VXLAN, eBPF data plane</td><td>Mature, widely deployed in regulated environments. Strong policy support.</td></tr>
        <tr><td>Flannel</td><td>VXLAN encapsulation</td><td>Simple, common in lab clusters. Limited policy support.</td></tr>
        <tr><td>AWS VPC CNI</td><td>Pod gets a real ENI IP</td><td>EKS default. No encapsulation; Pods are first-class VPC citizens.</td></tr>
        <tr><td>Azure CNI / GKE Dataplane V2</td><td>Cloud-native</td><td>GKE Dataplane V2 = Cilium-based by default in 2026.</td></tr>
      </tbody>
    </table>
    <p style="margin-top:18px">Two big architectural choices: <strong>encapsulation vs native routing</strong> (does each cross-node packet get wrapped in a VXLAN header, or do nodes route directly?), and <strong>iptables vs eBPF</strong> for Service load balancing (eBPF is dramatically faster at scale — kube-proxy with iptables hits perf cliffs at ~5000 Services).</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · MTU — the silent killer",
            h2="The thing that kills latency you can't explain",
            body_html="""    <p>The <strong>Maximum Transmission Unit (MTU)</strong> is the largest packet your interface can send without fragmentation. Standard Ethernet: 1500 bytes. VXLAN encapsulation adds 50 bytes of header. So your Pod's effective MTU on a VXLAN-overlay cluster is 1450, not 1500. <em>If the CNI hasn't told the Pod's eth0 about this</em>, the Pod thinks it can send 1500-byte packets, the host wraps them in VXLAN making 1550, the underlay rejects them, fragmentation/retransmits ensue.</p>
    <p>Symptoms: cross-node traffic mysteriously slow, sometimes specific HTTP requests time out (the ones with bodies large enough to hit MTU), TCP throughput plateaus way below line rate. The diagnostic command:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># From inside a Pod
ping -M do -s 1472 &lt;another-pod-ip&gt;   # 1472 + 28 (ICMP+IP) = 1500
# If this fails with "Frag needed", you have an MTU mismatch.</code></pre>
    <p>Modern CNIs (Cilium, Calico) auto-detect underlay MTU and configure Pod MTU accordingly. Older or hand-rolled setups: read the CNI's docs, set MTU explicitly. AWS EKS clusters: jumbo frames (MTU 9001) on most instance types — your CNI should pick this up.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The classic MTU bug: a cluster runs fine for months. Someone migrates from VXLAN to native routing (no encap header). They forget to bump the Pod MTU back up to 1500. Now Pods send 1450-byte packets when 1500-byte underlay is available — 3% throughput loss for no reason. Or vice versa. The fix: pin Pod MTU to <code>$UNDERLAY_MTU - $ENCAP_OVERHEAD</code> in the CNI config and forget it.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · kube-proxy and its eBPF replacement",
            h2="Where Service IPs come from",
            body_html="""    <p>Lesson 17 covered ClusterIP from the user's view: \"Service has a virtual IP that load-balances to the Pods.\" The implementation was <strong>kube-proxy</strong>: a per-node DaemonSet writing iptables rules. Each Service got a chain with one rule per backend Pod, randomised. It worked, it scaled to a few thousand Services, and then it didn't.</p>
    <p>Modern alternative: <strong>eBPF-based Service routing</strong> (Cilium kube-proxy replacement, Calico eBPF data plane, GKE Dataplane V2). The kernel's eBPF programs do Service load balancing in the network stack at the socket level — no iptables chains, no per-rule overhead. At 50,000 Services Cilium beats iptables-mode kube-proxy by orders of magnitude on throughput and connection establishment time.</p>
    <p>Beyond performance: eBPF gives you observability the iptables model couldn't. Cilium Hubble exposes per-flow visibility (which Pod is talking to which Service, what's getting denied by NetworkPolicy, where latency is). Tools like <code>tcpdump -i any</code> on a node now have a structured equivalent.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team reports cross-node Pod traffic is 200ms slow but same-node traffic is microseconds. <code>ping -M do -s 1472</code> from inside a Pod fails with \"Frag needed.\" What's the most likely cause?",
            options=[
                ("a) The CNI plugin is broken — reinstall it", False),
                ("b) MTU mismatch — Pods think they can send 1500-byte packets but the encap overhead makes them larger than the underlay allows", True),
                ("c) Pod IPs are misconfigured", False),
            ],
            feedback="<strong>Answer: b.</strong> Classic MTU bug. Fix: lower Pod MTU to underlay minus encap overhead (e.g., 1450 for VXLAN over 1500 underlay). Modern CNIs (Cilium, Calico) auto-detect; older or hand-rolled setups need explicit config.",
        ),
    },
    before_after_before='<p>Pre-CNI / pre-eBPF era: docker0 bridge per node, iptables for everything, kube-proxy generating thousands of rules per Service. Cross-node debugging meant <code>tcpdump -i eth0</code> on every hop. NetworkPolicy was best-effort. Service performance ceiling somewhere around 5000 Services.</p>',
    before_after_after='<p>Modern era: standardised CNI plugins, eBPF data plane (Cilium / Calico eBPF), per-flow observability via Hubble, NetworkPolicy enforced in kernel programs, Service performance scales linearly to 50K+ Services. The IP layer feels boring — exactly the goal.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Cilium\'s 2024-25 dominance pushed the rest of the industry toward eBPF. By 2026 nearly every new cluster is eBPF-based; iptables-mode kube-proxy is legacy.</p>',
    analogy_intro_html='<p>The Switchboard is K-Town\'s telephone exchange (Lesson 17 was the customer-facing front desk). Today we go behind the wall. Every apartment (Pod) has a phone (eth0) connected to a wire (one end of a <strong>veth pair</strong>) running to the building\'s switchboard (the node bridge). The switchboard connects every apartment in the building. To reach an apartment in <em>another</em> building, the call goes out through the building\'s trunk line, across town, into the other building\'s switchboard.</p><p>The <strong>CNI plugin</strong> is the contractor who runs all this wiring. Different contractors use different methods: Cilium uses eBPF (think: programmable junctions in the wire), Calico uses BGP (the buildings know each other\'s routing maps directly), Flannel uses VXLAN (every cross-building call gets wrapped in an extra envelope). All of them deliver the call. They differ on speed, observability, and how they handle policy.</p>',
    translation_rows=[
        ("The phone in the apartment", "Pod's <code>eth0</code> interface"),
        ("The wire from phone to switchboard", "<code>veth</code> pair (Pod side + host side)"),
        ("The building's switchboard", "Node bridge (<code>cni0</code>, <code>cilium_host</code>)"),
        ("The contractor who ran the wiring", "CNI plugin"),
        ("The trunk line between buildings", "Inter-node tunnel (VXLAN) or direct route"),
        ("The wrapped envelope on cross-building calls", "VXLAN encapsulation header (50 bytes)"),
        ("Wires too thin for fat envelopes", "MTU mismatch (encap overhead exceeds Pod MTU)"),
        ("Pre-eBPF: kube-proxy iptables — old-school operator boards", "iptables-mode kube-proxy"),
        ("eBPF: programmable junctions in the wire itself", "Cilium / GKE Dataplane V2 / Calico eBPF"),
    ],
    analogy_stops="The analogy stops here: real packets aren't \"calls\" — they're datagrams that can be lost, reordered, or split mid-flight. The CNI's job is harder than wiring; it has to handle live re-IPing, Pod churn, and policy enforcement in microseconds.",
    eli5='Every toy phone has a wire. The wire goes to a big board in the room (the bridge). The room\'s board connects to the room next door\'s board. The contractor who put in the wires is the CNI.',
    eli10="Each Pod has a Linux network namespace with its own <code>eth0</code>. <code>eth0</code> is one end of a <code>veth</code> pair; the other end is on the host plugged into a bridge. Cross-node traffic goes through inter-node routing or VXLAN encap. The CNI plugin is the per-node binary the kubelet calls (ADD/DEL/CHECK) on Pod lifecycle to set this up. The biggest production bug is MTU mismatch when encap overhead exceeds underlay capacity. Modern CNIs use eBPF instead of iptables for Service load balancing — much faster at scale and dramatically more observable.",
    scenarios=[
        Scenario(name="A SaaS migrating from kube-proxy to Cilium", body="Replaced kube-proxy with Cilium's kube-proxy replacement. Service-establishment latency dropped from 50µs to 8µs. NetworkPolicy moved from iptables to eBPF; no perf cliff at high rule count. Hubble lit up with per-flow visibility — they found three policy violations they didn't know existed."),
        Scenario(name="A bank running Calico with BGP peering", body="No encap. Every node BGP-peers with the top-of-rack switch. Pod IPs routable across the data center directly. No VXLAN overhead, no MTU surprises. Tradeoff: requires network team coordination and infrastructure that supports BGP."),
        Scenario(name="An EKS cluster using AWS VPC CNI", body="Pods get real VPC ENI IPs. Pod-to-Pod traffic goes through the VPC, no overlay, no encap. MTU = 9001 (jumbo frames). Tradeoff: ENI count limits how many Pods per node; needs careful node-type selection."),
        Scenario(name="A team debugging a 200ms latency that wasn't supposed to be there", body="Symptoms: only large HTTP responses slow. <code>ping -M do -s 1472</code> failed cross-node. MTU mismatch confirmed. CNI ConfigMap MTU bumped from 1500 to 1450 to account for VXLAN overhead. Latency normalised. Total fix time: 4 hours of mystery + 2 minutes of fix."),
    ],
    misconceptions=[
        Misconception(myth="K8s networking is its own special thing.", truth="K8s networking is Linux networking applied with namespaces and a CNI plugin. Every primitive (<code>veth</code>, bridges, routing tables, iptables) is bog-standard Linux. The novelty is automation, not the data plane."),
        Misconception(myth="Encapsulation is a performance disaster.", truth="VXLAN encap costs ~5-10% throughput on most workloads. Native routing is faster but requires infrastructure cooperation (BGP-capable switches, or cloud VPC integration). For most clusters, encap is fine; chase native routing only when measured throughput matters."),
        Misconception(myth="kube-proxy is required for K8s networking to work.", truth="kube-proxy implements <em>Services</em> (ClusterIP/NodePort), not Pod-to-Pod connectivity. CNIs like Cilium replace kube-proxy entirely. Pod-to-Pod just needs the CNI."),
    ],
    flashcards=[
        Flashcard(front="Three Linux primitives behind a Pod's network?", back="<code>veth</code> pair (virtual cable, Pod end + host end), bridge (virtual L2 switch on the host), routing table + iptables/nftables/eBPF rules for forwarding/policy."),
        Flashcard(front="What is CNI?", back="Container Network Interface — CNCF spec. The kubelet (runtime) calls a CNI plugin binary at Pod ADD/DEL/CHECK. Plugin sets up the Pod's networking. Vendor implementations: Cilium, Calico, Flannel, AWS VPC, Azure CNI, etc."),
        Flashcard(front="Encapsulation vs native routing?", back="Encap (VXLAN/Geneve): wrap each cross-node packet in an outer UDP header. Works on any network. Costs ~5-10% throughput + adds MTU overhead. Native routing: nodes route directly using BGP or cloud VPC integration. Faster, requires infrastructure support."),
        Flashcard(front="What's an MTU mismatch?", back="Pod thinks MTU is X, but encap overhead means real maximum is X-50. Packets at X get fragmented or dropped. Symptom: cross-node tail latency spikes for large packets. Fix: pin Pod MTU below underlay minus encap overhead."),
        Flashcard(front="Why does eBPF beat iptables for Service routing?", back="iptables = linear chain of rules per Service, O(n) per packet. eBPF = compiled programs running at kernel hooks, O(1) per packet. At 5K+ Services, iptables hits a perf cliff; eBPF scales linearly to 50K+."),
        Flashcard(front="What is Hubble?", back="Cilium's observability layer. Per-flow visibility: who's talking to whom, what's blocked by policy, where latency lives. Standard tool in Cilium-based clusters since 2023."),
        Flashcard(front="Why does GKE Dataplane V2 matter?", back="GKE's default data plane is Cilium-based since 2024. Means most new GKE clusters get eBPF + Hubble out of the box. AKS and EKS have similar offerings (AKS Cilium, EKS-with-Cilium addon)."),
        Flashcard(front="What's <code>kube-proxy ipvs</code> mode?", back="Older alternative to iptables mode. Uses Linux IPVS (in-kernel L4 LB). Better than iptables at high Service counts but less common now that eBPF-based CNIs replace kube-proxy outright."),
    ],
    quizzes=[
        Quiz(prompt="A Pod's <code>eth0</code> is up, IP looks right, but <code>curl another-pod-ip</code> times out. Same-node Pods reach each other fine. What do you check first?", answer="Cross-node connectivity → check the inter-node path. (1) <code>ip route</code> on the source node — does it have a route to the destination Pod's CIDR? (2) <code>iptables -L FORWARD -n -v</code> — is the FORWARD chain accepting? (3) Underlay reachability — can the source node ping the destination node? (4) MTU — try <code>ping -M do -s 1472 dest-pod-ip</code>; if it fails, MTU. (5) NetworkPolicy — is one denying? CNI logs (<code>kubectl -n kube-system logs ds/cilium</code>) usually narrow it down within minutes."),
        Quiz(prompt="Your team migrated from Flannel (VXLAN) to Cilium native-routing mode. After the migration, throughput went UP — but a few specific apps now get TCP resets on big payloads. What's wrong?", answer="MTU. Native routing has no encap overhead, so the underlay's full MTU is usable. If the new CNI config didn't bump Pod MTU back up (or worse, set it lower than the underlay), you can have either (a) Pod MTU too low — wasting capacity but otherwise fine, or (b) Pod MTU too high — packets bigger than what some intermediate hop allows, causing PMTU discovery messages that get blocked, leading to silent black-holing of large flows. Check <code>cilium config</code> for <code>mtu</code> setting; ping with DF bit set; verify ICMP-needed messages aren't being dropped by network ACLs."),
        Quiz(prompt="A platform team running 30K Services hits a kube-proxy perf cliff. <code>iptables-save | wc -l</code> returns 480,000 rules. They consider migrating to eBPF. <strong>Click for the migration playbook. ▼</strong>", cyoa=True, cyoa_tag="the migration playbook", answer="Migration is non-trivial — but well-trodden. Sequence: (1) Pilot Cilium on a non-prod cluster of similar scale; verify NetworkPolicy semantics match. (2) Install Cilium alongside kube-proxy on a prod cluster (Cilium has <code>kubeProxyReplacement: false</code> mode). Cilium handles CNI; kube-proxy still handles Services. (3) Switch to <code>kubeProxyReplacement: true</code> on a node-by-node basis using node selectors. (4) Validate with Hubble that Service traffic is flowing through eBPF. (5) Drain and remove kube-proxy DaemonSet. <strong>Pitfalls:</strong> some old apps depend on iptables-visible rules (rare), some firewalls inspect iptables for compliance evidence (more common in regulated industries — Cilium has equivalents but auditors may need to be educated). <strong>Payoff:</strong> Service latency drops 5-10x at scale, NetworkPolicy enforcement gains observability, kube-proxy maintenance disappears."),
    ],
    glossary=[
        GlossaryItem(name="veth", definition="Virtual Ethernet pair. One end in the Pod's net namespace; the other on the host."),
        GlossaryItem(name="Bridge", definition="Virtual L2 switch on a node. Pods' host-side veths plug into it."),
        GlossaryItem(name="CNI", definition="Container Network Interface — CNCF spec for K8s network plugins. Runtime calls plugin on Pod ADD/DEL/CHECK."),
        GlossaryItem(name="Cilium", definition="Modern CNI based on eBPF. De-facto choice for new clusters in 2026."),
        GlossaryItem(name="Calico", definition="Mature CNI; BGP routing, optional eBPF data plane. Strong NetworkPolicy support."),
        GlossaryItem(name="Flannel", definition="Simple VXLAN-based CNI. Common in lab clusters."),
        GlossaryItem(name="VXLAN", definition="Virtual eXtensible LAN. UDP-based encapsulation; ~50-byte overhead per packet."),
        GlossaryItem(name="Native routing", definition="Cross-node traffic uses real IP routing (BGP or cloud VPC) instead of encapsulation."),
        GlossaryItem(name="MTU", definition="Maximum Transmission Unit — largest packet size. Encap overhead reduces effective Pod MTU."),
        GlossaryItem(name="kube-proxy", definition="DaemonSet implementing Services via iptables, IPVS, or eBPF (replaceable by Cilium)."),
        GlossaryItem(name="eBPF", definition="In-kernel programmable hooks. Modern CNIs use it for data plane and observability."),
        GlossaryItem(name="Hubble", definition="Cilium's flow-level observability. Per-flow visibility into traffic and policy decisions."),
    ],
    recap_lead="Pods get veth pairs into a node bridge; CNI plugin handles routing across nodes (encap or native). Modern CNIs (Cilium) use eBPF for both data plane and Service routing — much faster than iptables-mode kube-proxy. The single most common production bug is MTU mismatch.",
    recap_next="<strong>Next — Lesson 25: Gateway API.</strong> The Ingress API is being retired in favour of the Gateway API across the entire ecosystem. Roles, listeners, routes, the Ingress NGINX migration story, and what changes for app teams. Switchboard, customer side.",
)
