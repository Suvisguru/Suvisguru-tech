from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Trenching and wiring: a CNI plugin truck delivering pipes labelled Cilium/Calico/Antrea/Flannel; MTU sign; eBPF tag.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">WIRING &amp; PLUMBING · CNI INSTALL</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">CNI CHOICE MATRIX (vanilla)</text>
    <rect x="14" y="34" width="140" height="60" rx="4" fill="#3F4A5E"/><text x="84" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Cilium</text><text x="84" y="64" text-anchor="middle" font-size="7" fill="#FBF1D6">eBPF data plane</text><text x="84" y="76" text-anchor="middle" font-size="7" fill="#FBF1D6">kube-proxy replace</text><text x="84" y="88" text-anchor="middle" font-size="7" fill="#FBE8DC">Hubble flows</text>
    <rect x="160" y="34" width="140" height="60" rx="4" fill="#5A9F7A"/><text x="230" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">Calico</text><text x="230" y="64" text-anchor="middle" font-size="7" fill="#FFFFFF">BGP-routed</text><text x="230" y="76" text-anchor="middle" font-size="7" fill="#FFFFFF">VXLAN fallback</text><text x="230" y="88" text-anchor="middle" font-size="7" fill="#FBE8DC">eBPF dp option</text>
    <rect x="306" y="34" width="140" height="60" rx="4" fill="#A04832"/><text x="376" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">Antrea / OVN-K</text><text x="376" y="64" text-anchor="middle" font-size="7" fill="#FBE8DC">OVS-based</text><text x="376" y="76" text-anchor="middle" font-size="7" fill="#FBE8DC">SDN-friendly</text>
    <rect x="452" y="34" width="140" height="60" rx="4" fill="#E8B547"/><text x="522" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">Flannel / kube-router</text><text x="522" y="64" text-anchor="middle" font-size="7" fill="#5A4F45">simple labs</text><text x="522" y="76" text-anchor="middle" font-size="7" fill="#5A4F45">limited policy</text>
    <rect x="14" y="104" width="282" height="44" rx="4" fill="#FBE8DC" stroke="#A04832"/><text x="155" y="120" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">Pod CIDR alignment</text><text x="155" y="132" text-anchor="middle" font-size="7" fill="#5A4F45">CNI config MUST match kubeadm podSubnet</text><text x="155" y="144" text-anchor="middle" font-size="7" fill="#5A4F45">otherwise nodes never become Ready</text>
    <rect x="306" y="104" width="290" height="44" rx="4" fill="#E0EFE6" stroke="#3D7857"/><text x="451" y="120" text-anchor="middle" font-size="9" font-weight="700" fill="#3D7857">MTU tuning</text><text x="451" y="132" text-anchor="middle" font-size="7" fill="#5A4F45">underlay - encap overhead = pod MTU</text><text x="451" y="144" text-anchor="middle" font-size="7" fill="#5A4F45">VXLAN: 1500 - 50 = 1450</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="04",
    title_short="CNI &amp; networking",
    title_full="V4 · CNI Installation and Cluster Networking",
    title_html="K-VAN V4 · CNI Installation",
    module_eyebrow="Module V4 · trenching and wiring",
    hero_sub_html='Until a CNI is installed, every node is <code>NotReady</code>. Picking the CNI is the second-most-consequential cluster decision after etcd topology. <strong>Cilium</strong> dominates new clusters in 2026 (eBPF data plane + kube-proxy replacement); <strong>Calico</strong> dominates compliance-heavy environments (BGP, mature, FIPS-able).',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Cluster bootstrapped fine; nodes are NotReady; you install the CNI and… the CNI Pods crash-loop. The error: <code>configured pod CIDR 10.244.0.0/16 doesn\'t match cluster CIDR 192.168.224.0/20</code>. Or worse: nodes go Ready but cross-node Pod traffic times out. The CNI\'s VXLAN MTU is 1450 and your hosts have MTU 1500 — fragmentation black-holing. <em>The CNI install is where misalignments from V1 punish you</em>. This module is the survival kit.',
    stamp_html='Choose CNI by trade-off: <strong>Cilium</strong> (eBPF, fastest, observability via Hubble, kube-proxy replacement), <strong>Calico</strong> (BGP-native, mature, eBPF data plane optional), <strong>Antrea / OVN-K</strong> (OVS-based, SDN-friendly), <strong>Flannel / kube-router</strong> (simple, limited policy). The CNI\'s Pod CIDR config <strong>must match</strong> kubeadm\'s podSubnet. <strong>MTU</strong>: pod MTU = underlay MTU minus encap overhead.',
    district_pin="kf-site04",
    district_label="Wiring &amp; Plumbing",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why CNI is its own decision",
            body_html="""    <p>kubeadm doesn\'t install a CNI on purpose: K8s is intentionally network-plugin-agnostic. The CNI handles three things: assign Pod IPs from the cluster CIDR, route packets between Pods on different nodes, enforce NetworkPolicy. Different CNIs solve all three differently — and you can\'t change CNI on a running cluster without significant ceremony (drain + uninstall + reinstall + reschedule everything).</p>
    <p>For vanilla self-managed in 2026, the realistic choices are Cilium (eBPF), Calico (BGP), Antrea / OVN-Kubernetes (OVS), and Flannel / kube-router for the tiny / lab end. Each has a strong identity:</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The CNI matrix",
            h2="What each is good at",
            body_html="""    <table class="data-table">
      <thead><tr><th>CNI</th><th>Data plane</th><th>NetworkPolicy</th><th>Encryption</th><th>Observability</th><th>Best for</th></tr></thead>
      <tbody>
        <tr><td><strong>Cilium</strong></td><td>eBPF in-kernel</td><td>Standard + L7 + FQDN + cluster-mesh</td><td>WireGuard / IPsec</td><td>Hubble (per-flow)</td><td>Modern default; production at scale</td></tr>
        <tr><td><strong>Calico</strong></td><td>BGP routing or VXLAN; eBPF dp opt-in</td><td>Standard + global + FQDN</td><td>WireGuard / IPsec</td><td>Calico Whisker (newer)</td><td>Compliance, regulated, FIPS</td></tr>
        <tr><td><strong>Antrea</strong></td><td>OVS</td><td>Standard + multi-cluster</td><td>IPsec</td><td>Theia / Antrea UI</td><td>VMware-aligned shops; SDN parity</td></tr>
        <tr><td><strong>OVN-Kubernetes</strong></td><td>OVN/OVS</td><td>Standard</td><td>IPsec</td><td>OVN trace</td><td>OpenShift, large SDN setups</td></tr>
        <tr><td><strong>Flannel</strong></td><td>VXLAN</td><td>Limited (no native enforcement)</td><td>none built-in</td><td>none</td><td>Labs, simplest possible</td></tr>
        <tr><td><strong>kube-router</strong></td><td>BGP</td><td>iptables-based</td><td>none</td><td>Limited</td><td>BGP-only, no VXLAN</td></tr>
      </tbody>
    </table>
    <p style="margin-top:18px"><strong>For a fresh 2026 production cluster: Cilium is the modern default.</strong> Calico is the regulated alternative. The other choices serve specific niches.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Install + alignment",
            h2="Cilium walkthrough (Helm)",
            body_html="""    <p>Cilium ships a Helm chart. Critical alignment with your kubeadm config:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>helm repo add cilium https://helm.cilium.io
helm install cilium cilium/cilium --version 1.16.0 \\
  --namespace kube-system \\
  --set ipam.operator.clusterPoolIPv4PodCIDRList="192.168.224.0/20" \\
  --set kubeProxyReplacement=true \\
  --set k8sServiceHost=api.cluster.corp \\
  --set k8sServicePort=6443 \\
  --set tunnel=disabled \\
  --set ipv4NativeRoutingCIDR=192.168.224.0/20 \\
  --set autoDirectNodeRoutes=true \\
  --set hubble.enabled=true \\
  --set hubble.relay.enabled=true \\
  --set hubble.ui.enabled=true</code></pre>
    <p>What this does: native routing (no VXLAN/Geneve overhead), Cilium replaces kube-proxy entirely (kube-proxy DaemonSet should be deleted: <code>kubectl -n kube-system delete ds kube-proxy</code>), Hubble enabled for per-flow observability.</p>
    <p>Verify after install:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>cilium status --wait
cilium connectivity test    # ~5 min, exhaustive
hubble observe --since 1m   # see flows</code></pre>""",
        ),
        Section(
            eyebrow="Section 1.9 · Operational concerns",
            h2="MTU, dual-stack, multi-network, switching CNIs",
            body_html="""    <p><strong>MTU.</strong> Pod MTU must be ≤ underlay MTU minus encapsulation overhead. VXLAN: 50-byte overhead. Geneve: 60-byte. WireGuard: 60-80. Native routing: 0. Cilium auto-detects but verify: <code>kubectl -n kube-system exec ds/cilium -- cilium status | grep MTU</code>.</p>
    <p><strong>Dual-stack.</strong> If you set both IPv4 + IPv6 in kubeadm\'s <code>networking.podSubnet</code>, the CNI must support dual-stack (Cilium yes, Calico yes, Flannel limited). Once enabled at install, can\'t un-stack without rebuild.</p>
    <p><strong>Multi-network</strong> via <strong>Multus</strong>. A meta-CNI that lets Pods have additional interfaces from secondary CNIs (SR-IOV, MACVLAN). Used in NFV, telecom, ML training with dedicated NICs. Adds operational complexity; only when you need it.</p>
    <p><strong>Switching CNIs on a running cluster.</strong> Painful but doable. Steps: drain nodes, uninstall old CNI (delete DaemonSet, remove <code>/etc/cni/net.d/*</code>, reset iptables), install new CNI, uncordon. Test network policy semantics on a non-prod cluster first; the L4/L7 nuances differ between Cilium and Calico.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For air-gapped: pull all CNI images to your internal registry, configure containerd registry mirror so the CNI Helm chart\'s image references resolve. The CNI typically pulls 4-8 images; small relative to add-on stack.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='You install Cilium with <code>clusterPoolIPv4PodCIDRList="10.244.0.0/16"</code> but kubeadm\'s podSubnet was <code>192.168.224.0/20</code>. What happens?',
            options=[
                ('a) Cilium auto-corrects', False),
                ('b) Cilium allocates Pod IPs from 10.244.0.0/16, but kube-controller-manager\'s --cluster-cidr is 192.168.224.0/20 — routing on cross-node traffic breaks; Pods can\'t reach each other reliably', True),
                ('c) Nothing happens', False),
            ],
            feedback='<strong>Answer: b.</strong> Pod CIDR <strong>must</strong> match between kubeadm config and CNI config. Otherwise the cluster is wedged: Pods get IPs the controller doesn\'t expect, kube-proxy / cilium routes are inconsistent. Always copy the kubeadm <code>podSubnet</code> value into the CNI install.',
        ),
    },
    before_after_before='<p>Cluster bootstrapped, every node NotReady. Trial-and-error CNI install. Wrong Pod CIDR alignment requires reset + reinstall. MTU mismatch causes intermittent failures days later. NetworkPolicy enforcement different from what was assumed.</p>',
    before_after_after='<p>CNI install via Helm + values committed to git. Pod CIDR matches V1 architecture decision. MTU verified at install. <code>cilium connectivity test</code> passes. Hubble shows live flows. NetworkPolicy enforced consistently.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">CNI is "install once, change rarely" — get the choice right before the cluster has workloads.</p>',
    analogy_intro_html='<p>Wiring & Plumbing is the fourth site. The frame is up; now the contractor lays the trenches and runs the cables. Different contractors do this differently. <strong>Cilium</strong> uses programmable junctions (eBPF) right inside the wires; <strong>Calico</strong> uses big ring-main routing (BGP) tying the buildings together; <strong>Flannel</strong> wraps every cross-building call in an extra envelope (VXLAN). The wires must match the building\'s plug-spec (Pod CIDR matches kubeadm config); the cable thickness must accept the largest packets you\'ll send (MTU); and the contractor sets up the meters that show what\'s flowing (Hubble / Whisker).</p>',
    translation_rows=[
        ('The wiring contractor', 'CNI plugin'),
        ('Programmable in-wire junctions', 'Cilium eBPF data plane'),
        ('Ring-main BGP routing', 'Calico BGP'),
        ('Wrapping every cross-building call', 'VXLAN encapsulation'),
        ('Plug-spec matching', 'Pod CIDR alignment kubeadm ↔ CNI'),
        ('Cable thickness limit', 'MTU (underlay − encap overhead)'),
        ('Live flow meters', 'Hubble / Calico Whisker'),
        ('Telecom-grade specialty wiring', 'Multus + secondary CNIs (SR-IOV)'),
    ],
    analogy_stops="The analogy stops here: networking isn't physical wires — every Pod IP is a virtual interface in a Linux namespace. The CNI\'s job is configuring tens of thousands of these abstractions per cluster, not laying cable.",
    eli5='The frame is up but there\'s no electricity yet. The wiring crew picks how to wire it (Cilium / Calico / etc.), runs the wires through the walls, and turns it on.',
    eli10="Until you install a CNI, every node is NotReady. Cilium (eBPF, modern default) or Calico (BGP, mature) for production. Pod CIDR must match between kubeadm config and CNI install. MTU = underlay - encap overhead. Cilium can also replace kube-proxy entirely. Hubble (Cilium) or Whisker (Calico) for per-flow observability. Switching CNIs on a running cluster is possible but painful.",
    scenarios=[
        Scenario(name='A SaaS using Cilium with kube-proxy replacement', body='Cilium installed via Helm. kube-proxy DaemonSet deleted. eBPF handles Service load balancing in-kernel. Hubble enabled for flow visibility. <code>cilium connectivity test</code> in CI on every cluster create. Network performance: cross-node latency 0.4ms; kube-proxy iptables would have been 1.5ms+ at the same scale.'),
        Scenario(name='A bank running Calico with BGP', body='Calico configured for BGP peering with TOR (top-of-rack) switches. No VXLAN — Pod traffic is native routed across the underlay. Compliance team approves: predictable routing, no encap overhead, mature codebase. WireGuard enabled for cross-node mTLS at the data plane. eBPF data plane opt-in for performance.'),
        Scenario(name='An NFV team using Multus + SR-IOV', body='Telco workload (5G User Plane Function) needs dedicated NICs with hardware offload. Multus as meta-CNI; primary CNI is Cilium (for control plane traffic), secondary is SR-IOV (for data plane). Pods get two interfaces. Operational complexity is real; the perf gain (line-rate forwarding) justifies it.'),
        Scenario(name='A team that switched Flannel → Cilium', body='Started with Flannel for simplicity. Hit limitations: weak NetworkPolicy enforcement, no observability, kube-proxy bottleneck at 5K Services. Migration plan: install Cilium with chaining mode (Cilium on top of Flannel) for one week of validation, then drain + uninstall Flannel + reinstall Cilium native. Total downtime per node: ~5 minutes during drain.'),
    ],
    misconceptions=[
        Misconception(myth='\"All CNIs implement NetworkPolicy the same way.\"', truth='Standard NetworkPolicy is a CRD spec — but L7 features, FQDN matching, AdminNetworkPolicy support, encryption all vary. Cilium has the richest feature set; Calico is close; Antrea has multi-cluster; Flannel doesn\'t enforce at all.'),
        Misconception(myth='\"VXLAN is always slower than native routing.\"', truth='VXLAN adds ~5-10% throughput overhead; for most workloads it\'s invisible. Native routing requires BGP-capable infrastructure or cloud VPC integration. Pick by infra capability, not raw perf.'),
        Misconception(myth='\"You can swap CNI without taking workloads down.\"', truth='Possible but messy. Easiest path: drain nodes one at a time, uninstall old CNI, install new CNI, uncordon. Cluster is degraded during the migration. Plan it like a major upgrade.'),
    ],
    flashcards=[
        Flashcard(front='Why is the cluster NotReady after kubeadm init?', back='No CNI installed. The kubelet needs a CNI plugin to set up Pod networking. Install Cilium / Calico / etc., wait 30-60s, nodes go Ready.'),
        Flashcard(front='Pod CIDR alignment rule?', back='kubeadm <code>networking.podSubnet</code> must match the CNI\'s configured cluster CIDR exactly. Mismatch = Pods get wrong IPs, routing breaks, mysterious failures.'),
        Flashcard(front='MTU formula?', back='Pod MTU = underlay MTU − encap overhead. VXLAN: 50 bytes. Geneve: 60. WireGuard: 60-80. Native routing: 0. Modern CNIs auto-detect; verify after install.'),
        Flashcard(front='kube-proxy replacement (Cilium)?', back='Cilium handles Service load balancing in eBPF, eliminating kube-proxy. Set <code>kubeProxyReplacement=true</code> in Helm + delete <code>kube-proxy</code> DaemonSet. Faster + more observable.'),
        Flashcard(front='What is Hubble?', back='Cilium\'s per-flow observability layer. Shows source/dest/protocol/policy decision per packet. Built on the same eBPF data plane.'),
        Flashcard(front='Multus — when?', back='Meta-CNI letting Pods have multiple network interfaces from different CNIs. Use for NFV, telecom (SR-IOV), ML training with dedicated NICs. Adds complexity; only when you need extra interfaces per Pod.'),
        Flashcard(front='Calico BGP vs VXLAN?', back='BGP: native routing, no encap overhead, requires BGP-capable underlay (TOR switches or cloud VPC). VXLAN: works on any L3 underlay, ~5-10% throughput cost. BGP for performance + simplicity; VXLAN for portability.'),
        Flashcard(front='Switching CNIs on a running cluster?', back='Drain node → uninstall old CNI (DaemonSet + /etc/cni/net.d/*) → install new CNI → uncordon. Cluster degraded during migration. Test policy semantics first.'),
    ],
    quizzes=[
        Quiz(prompt='You install Cilium with kube-proxy replacement and enable Hubble. <code>kubectl get pods -n kube-system</code> shows kube-proxy still running. Should you delete it?', answer='Yes — once Cilium is healthy and tests pass. Run <code>cilium status</code>, then <code>cilium connectivity test</code>. If both pass, delete kube-proxy: <code>kubectl -n kube-system delete ds kube-proxy</code>. Cleanup the iptables rules left over: <code>iptables-save | grep -v KUBE | iptables-restore</code> (or just reboot the node, which is cleaner). Failure to delete leaves you in a hybrid state with both managing Service routing — confusing performance characteristics. <strong>Why this matters:</strong> the speedup from kube-proxy replacement only manifests when kube-proxy is gone.'),
        Quiz(prompt='Cross-node Pod traffic mysteriously fails for large payloads (HTTP responses with 4 MB JSON). Same-node fine. Diagnosis?', answer='<strong>MTU mismatch.</strong> Symptoms: small packets work; large packets (>= MTU) get fragmented or dropped. Diagnose: from inside a Pod, <code>ping -M do -s 1472 &lt;another-node-pod-ip&gt;</code>. If \"Frag needed\" returns, MTU is misconfigured. <strong>Fix:</strong> Cilium: <code>helm upgrade cilium cilium/cilium --set MTU=1450</code> (assuming 1500 underlay + VXLAN encap). Calico: edit FelixConfiguration. Then restart the CNI Pods. <strong>Verify:</strong> Pod\'s eth0 MTU matches the new value (<code>kubectl exec pod -- ip link show</code>). <strong>Long-term:</strong> document the underlay MTU in the V1 architecture doc and never trust auto-detection alone.'),
        Quiz(prompt='You\'re asked to switch CNI from Flannel to Cilium on a 30-node production cluster. <strong>Click for the migration playbook. ▼</strong>', cyoa=True, cyoa_tag='the migration playbook', answer='<strong>(1) Pre-flight on staging.</strong> Same migration end-to-end. Validate Cilium NetworkPolicy enforces what your apps expect. <strong>(2) Install Cilium in chaining mode</strong> on prod (Cilium runs alongside Flannel temporarily, providing observability + new policy enforcement without taking over data plane). Validate Hubble flows match expected behavior. <strong>(3) Document rollback.</strong> Helm uninstall cilium = back to Flannel-only. Rehearse it. <strong>(4) One node at a time.</strong> <code>kubectl drain node-X --ignore-daemonsets</code>. Reset CNI on that node: stop kubelet → remove <code>/etc/cni/net.d/*</code> → restart kubelet → Cilium DaemonSet picks up. Verify with a smoke test. <code>kubectl uncordon node-X</code>. <strong>(5) Watch for application errors</strong> as Pods reschedule onto Cilium-only nodes. Common gotcha: NetworkPolicy semantics differ in subtle ways (Cilium\'s identity-based vs Flannel\'s lack thereof). <strong>(6) Continue node-by-node.</strong> 30 nodes × 10 min each = 5 hours of degraded capacity (one node down at a time). Schedule outside peak. <strong>(7) Final cleanup:</strong> uninstall Flannel DaemonSet entirely, remove kube-proxy if Cilium is replacing it. <strong>(8) Update CI</strong> to assert <code>cilium connectivity test</code> on every cluster create going forward. <strong>Total project time:</strong> 1 sprint of prep, 1 evening of execution.'),
    ],
    glossary=[
        GlossaryItem(name='CNI', definition='Container Network Interface — gRPC/CNI-spec plugins kubelet calls to set up Pod networking.'),
        GlossaryItem(name='Cilium', definition='eBPF-based CNI. Modern default for new clusters. kube-proxy replacement, Hubble observability, WireGuard.'),
        GlossaryItem(name='Calico', definition='Mature CNI. BGP-native routing or VXLAN. Optional eBPF data plane. Strong NetworkPolicy.'),
        GlossaryItem(name='Antrea', definition='OVS-based CNI. Multi-cluster support via the Antrea ClusterSet. VMware-aligned.'),
        GlossaryItem(name='OVN-Kubernetes', definition='OVN/OVS-based. OpenShift\'s default. SDN-friendly.'),
        GlossaryItem(name='Flannel', definition='Simple VXLAN-only CNI. Limited NetworkPolicy. Labs / dev only in production-thinking.'),
        GlossaryItem(name='kube-router', definition='BGP-only CNI. iptables-based policy. Niche.'),
        GlossaryItem(name='Multus', definition='Meta-CNI giving Pods multiple network interfaces from secondary CNIs. NFV / SR-IOV use cases.'),
        GlossaryItem(name='kube-proxy replacement', definition='CNI (Cilium / Calico eBPF) handles Service load balancing in-kernel, replacing kube-proxy DaemonSet entirely.'),
        GlossaryItem(name='Hubble', definition='Cilium\'s per-flow observability. Built on eBPF. Shows source/dest/protocol/policy.'),
        GlossaryItem(name='Pod CIDR alignment', definition='kubeadm <code>networking.podSubnet</code> must equal CNI\'s configured cluster CIDR. Mismatch = mysterious failures.'),
        GlossaryItem(name='MTU tuning', definition='Pod MTU = underlay MTU − encap overhead. VXLAN: 50, Geneve: 60, WireGuard: 60-80, native: 0.'),
    ],
    recap_lead='CNI install is install-once, change-rarely. Cilium is the modern default; Calico for compliance. Pod CIDR alignment + MTU tuning are the two install-time gotchas. Hubble or Whisker for observability.',
    recap_next='<strong>Next — V5: Core Add-ons.</strong> CoreDNS, metrics-server, ingress / Gateway, cert-manager, CSI, ExternalDNS, Sealed Secrets / SOPS, monitoring + logging stack. The outbuildings around the main house.',
)
