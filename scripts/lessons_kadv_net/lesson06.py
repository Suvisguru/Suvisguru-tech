"""K-ADV-NET N6 — Packet tracing + performance tuning."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Packet tracing tools — Hubble, Pixie, tcpdump, kube-burner.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Traffic Helicopter · K-Highway — see every flow + tune the road</text>
  <rect x="40" y="70" width="170" height="100" rx="10" fill="#3878B5" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Hubble (Cilium)</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">eBPF flow logs</text>
  <text x="125" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">L4 + L7 verdicts</text>
  <rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Pixie / Tetragon</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">syscall + L7 trace</text>
  <text x="310" y="124" text-anchor="middle" font-size="9" fill="#1F2433">no app instrumentation</text>
  <rect x="410" y="70" width="170" height="100" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">tcpdump / kubectl-trace</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">kernel-level capture</text>
  <text x="495" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">low-level</text>
  <rect x="595" y="70" width="125" height="100" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">kube-burner</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#1F2433">cluster perf testing</text>
  <text x="657" y="124" text-anchor="middle" font-size="9" fill="#1F2433">load + timing</text>
</svg>"""


LESSON = LessonSpec(
    num="06",
    title_short="packet tracing + perf",
    title_full="N6 · Packet Tracing + Performance Tuning",
    title_html="K-ADV-NET N6 · Tracing + Tuning",
    module_eyebrow="Module N6 · Traffic Helicopter — see every flow + tune the road",
    hero_sub_html='Tracing tools at four levels. <strong>Hubble</strong> (Cilium): eBPF flow logs with L4 + L7 verdicts (HTTP / DNS / Kafka). <strong>Pixie / Tetragon</strong>: syscall + L7 trace via eBPF; no app instrumentation. <strong>tcpdump / kubectl-trace / kubeshark</strong>: low-level packet capture. <strong>kube-burner</strong>: synthetic load + cluster perf testing. Common findings: <strong>MTU mismatch</strong>, <strong>conntrack saturation</strong>, <strong>kernel scheduling</strong>, <strong>CoreDNS bottleneck</strong>, <strong>noisy neighbour</strong> via host network contention.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Service P99 latency 4× normal. App metrics show all calls slow; CPU normal; memory normal. <em>The team has no flow-level visibility</em>. They\'re guessing. Today\'s lesson: deploy Hubble + Pixie before incidents — your future self thanks you.",
    stamp_html="<strong>Hubble for L4+L7 flows; Pixie / Tetragon for in-app calls without instrumentation; tcpdump for kernel-level when nothing else helps; kube-burner for proactive perf testing. Wire them all in dev so muscle memory exists during incidents.</strong>",
    district_pin="knet-junction06",
    district_label="Traffic Helicopter",
    sections=[
        Section(
            eyebrow="Section 1.1 · Hubble — eBPF flow visibility",
            h2="L4 + L7 verdicts without packet capture",
            body_html="""    <p><strong>Hubble</strong> (Cilium\'s observability layer) shows per-flow events: source / destination Pod, IP, port, verdict (Allowed / Dropped + reason — NetPol rule, RST, etc.), L7 metadata (HTTP method + path + status, DNS name + result, Kafka topic).</p>
    <p>Hubble UI / CLI / Grafana: \"show all denied flows from namespace X past 5 min\" — answer in seconds. Compare to without: tcpdump on every node + manually correlate.</p>
    <p>Hubble flow logs power: NetworkPolicy debugging (\"why is this dropped?\"), security forensics (\"who connected to crypto-pool IPs?\"), latency analysis (\"P99 of HTTP / on this Service\").</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Pixie + Tetragon — application-level eBPF",
            h2="L7 + syscall trace with no app changes",
            body_html="""    <p><strong>Pixie</strong> (CNCF, NewRelic-acquired): eBPF probes for HTTP / gRPC / MySQL / Postgres / Redis / DNS — captures requests + responses (with redaction); script-able with PxL queries. Per-Service traffic + per-endpoint latency without OTel SDKs.</p>
    <p><strong>Tetragon</strong> (Cilium): syscall-level + process-level trace + enforcement. Sees fork / exec / open / connect; emits events to SIEM; can also block at runtime.</p>
    <p>Both use eBPF; both bypass app instrumentation. Pixie shines on \"what is this Service actually doing?\"; Tetragon on security + runtime behavior.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · tcpdump + kubectl-trace + kubeshark",
            h2="When you need to see the actual packets",
            body_html="""    <p>When higher-level tools don\'t answer:</p>
    <ul>
      <li><strong>tcpdump</strong> on a node: <code>kubectl debug node/X -- tcpdump -i any -nn -e</code>. Captures raw frames; great for MTU + checksum + encap problems.</li>
      <li><strong>kubectl-trace</strong>: bpftrace-style scripts run cluster-wide. <code>kubectl trace run node/X -e \"...\"</code> for kernel-level tracing.</li>
      <li><strong>kubeshark</strong>: cluster-wide sniffer with per-Pod filters; UI shows L7 streams (HTTP / gRPC / Kafka). Lower-overhead than tcpdump for ongoing inspection.</li>
      <li><strong>retina</strong> (Microsoft): cluster-wide network observability with eBPF + Prometheus metrics.</li>
    </ul>
    <p>Use these when: encap path debugging, MTU mismatch suspicion, kernel-level perf, custom protocol troubleshooting.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · kube-burner + common perf findings",
            h2="proactive testing + tuning playbook",
            body_html="""    <p><strong>kube-burner</strong>: synthetic load generator. Spin up N Pods + N Services + N CRDs + measure cluster behavior under load. Foundation of perf-test-as-code; CI gates on cluster-perf regressions.</p>
    <p><strong>Common findings + fixes</strong>:</p>
    <ul>
      <li><strong>MTU mismatch</strong>: encap pushes packet over host MTU; large requests fragment / drop. <em>Set Pod MTU = host MTU − encap overhead</em>.</li>
      <li><strong>conntrack saturation</strong>: high CPS overflows nf_conntrack_max. <em>Tune nf_conntrack_max + hashsize; use eBPF to bypass conntrack</em>.</li>
      <li><strong>CoreDNS bottleneck</strong>: 80%+ CPU at scale. <em>NodeLocal DNSCache + ndots:1</em> (covered N4).</li>
      <li><strong>Noisy neighbour</strong>: shared host CPU / network. <em>QoS class Guaranteed + node anti-affinity</em>.</li>
      <li><strong>Kernel scheduling</strong>: high context-switch on overloaded nodes. <em>Right-size; use cpu-manager-policy=static for latency-sensitive</em>.</li>
      <li><strong>Encap overhead</strong>: 15-25% CPU on VXLAN/Geneve. <em>BGP native routing where fabric supports</em>.</li>
    </ul>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A NetworkPolicy is dropping traffic; how do you find which rule is responsible?",
            options=[
                ("Read all NetworkPolicy YAMLs and trace by hand.", False),
                ("Hubble flow log shows verdict + drop reason per flow.", True),
                ("Restart kube-proxy.", False),
            ],
            feedback="Hubble emits the verdict per flow including which rule denied. Seconds vs hours of manual trace.",
        ),
        3: PauseCheck(
            question="A team\'s cluster CPU spikes 25% after a CNI upgrade. First profiling tool?",
            options=[
                ("kube-burner.", False),
                ("Hubble + node-level perf top — encap overhead? conntrack saturation? new CNI feature using kernel?", True),
                ("Restart all Pods.", False),
            ],
            feedback="Hubble for cluster-wide flow patterns; node-level perf tools (perf top, eBPF tracing) for kernel hotspots. Identify the CNI feature responsible; tune or revert.",
        ),
    },
    before_after_before='<p>Pre-eBPF tracing, network debugging was tcpdump + manual correlation + intuition. Hours per incident. App-internal calls invisible without instrumentation.</p>',
    before_after_after='<p>Hubble + Pixie + Tetragon give per-flow + per-syscall + per-app-call visibility via eBPF; tcpdump + kubectl-trace are last-resort. kube-burner verifies perf in CI; common findings have known tunings.</p>',
    before_after_caption='<p class="ba-caption"><em>See the network. Don\'t guess. Profile in dev so muscle memory exists during incidents.</em></p>',
    analogy_intro_html='''<p>The Traffic Helicopter circles K-Highway 24/7. Four cameras + sensors give different views. <strong>Wide-angle camera</strong> (Hubble) sees every vehicle route — license + destination + verdict (allowed / blocked). <strong>In-vehicle dashcam</strong> (Pixie + Tetragon) sees what each driver was doing — calls made, syscalls executed. <strong>Per-lane probe</strong> (tcpdump / kubectl-trace) drops a sensor in one lane for kernel-level depth. <strong>Stress-test convoy</strong> (kube-burner) drives synthetic load + measures.</p>
    <p>The Captain reads the four together. Most issues surface in the wide-angle; some need dashcam; rare ones need probes; perf changes get convoy-tested.</p>''',
    translation_rows=[
        ("Wide-angle camera", "Hubble (Cilium eBPF flow log)"),
        ("In-vehicle dashcam", "Pixie + Tetragon (eBPF syscall + L7)"),
        ("Per-lane probe", "tcpdump / kubectl-trace / kubeshark / retina"),
        ("Stress-test convoy", "kube-burner (synthetic load)"),
        ("Wrong-tire-pressure (MTU mismatch)", "Pod MTU != host MTU − encap overhead"),
        ("Toll booth overflow", "conntrack saturation"),
        ("Tunnel CPU tax", "VXLAN / Geneve encap overhead"),
        ("Single-driver lane delay", "Noisy neighbour / shared CPU"),
    ],
    analogy_stops="A real helicopter sees vehicles physically; cluster traffic is bytes + policy. Tracing tools have observability cost — sample at scale; deploy fully in dev.",
    eli5="Four kinds of camera over the highway. Wide angle for routes. Dashcam for what drivers do. Per-lane probe for kernel-level depth. Stress-test convoy for proactive testing. Read all four when the highway slows.",
    eli10="<strong>Hubble</strong>: eBPF flow logs (L4+L7 verdicts). <strong>Pixie</strong>: eBPF L7 trace (HTTP/gRPC/MySQL/Postgres/Redis/DNS) without app changes. <strong>Tetragon</strong>: syscall + process trace + enforcement. <strong>tcpdump / kubectl-trace / kubeshark / retina</strong>: low-level packet + kernel tracing. <strong>kube-burner</strong>: synthetic load + cluster perf. <strong>Common fixes</strong>: MTU = host − encap; conntrack tuning; NodeLocal DNS; QoS Guaranteed; cpu-manager-policy.",
    scenarios=[
        Scenario(
            name="Hubble caught a drop nobody had seen",
            body="A team\'s API was occasionally returning 502s; app logs blank. Hubble flow log: drop on egress to backend; reason = NetworkPolicy. Bad NP rule was added by mistake; reverted; problem cleared in 5 minutes.",
        ),
        Scenario(
            name="Pixie revealed slow downstream call",
            body="P99 latency drift over weeks. Pixie L7 trace per Service showed HTTP P99 to one upstream API growing — that upstream service was slow; team alerted upstream owner; tail latency clipped.",
        ),
        Scenario(
            name="MTU mismatch found via tcpdump",
            body="Large requests silently dropped. tcpdump on host showed fragmentation + ICMP \"Frag needed\" being filtered. Pod MTU set to 1500 but host VXLAN-tunnel MTU was 1400. Set Pod MTU 1400; problem cleared.",
        ),
        Scenario(
            name="kube-burner CI gate caught conntrack regression",
            body="kube-burner CI test showed P99 latency rising 2× after a CNI version bump. Profile: conntrack table near limit. Tuning + version pinning kept change reversible. Caught before prod.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"tcpdump is the right first tool.\"",
            truth="tcpdump is high-overhead + low-context. Hubble + Pixie + Tetragon read kernel-level eBPF events with structure + verdicts. Use tcpdump only when higher-level tools can\'t see what you need (raw bytes, kernel encap).",
        ),
        Misconception(
            myth="\"Pixie requires changing the app.\"",
            truth="Pixie\'s eBPF probes attach at kernel level + decode L7 protocols (HTTP / gRPC / MySQL / Postgres / Redis / DNS) without any app changes. Add the Pixie agent; it sees existing traffic.",
        ),
        Misconception(
            myth="\"kube-burner is for cluster admins only.\"",
            truth="App teams can use it for capacity-test-as-code: \"my Service can sustain 1000 rps with N replicas\". Run in CI before deployment; perf regressions caught at PR time.",
        ),
    ],
    flashcards=[
        Flashcard(front="What does Hubble give you?", back="Per-flow events from Cilium eBPF — source/dest Pod, IP, port, verdict (Allowed/Dropped + reason), L7 metadata (HTTP / DNS / Kafka). UI + CLI + Grafana."),
        Flashcard(front="Pixie vs OTel SDKs?", back="Pixie uses eBPF probes — sees existing app traffic without code changes. OTel SDKs require code instrumentation but give richer custom metrics. Both useful; complementary."),
        Flashcard(front="When pick tcpdump?", back="Last resort. When higher-level tools (Hubble, Pixie, Tetragon, kubeshark) don\'t answer your question. Encap-debugging, MTU issues, raw-bytes inspection."),
        Flashcard(front="What is kube-burner?", back="Synthetic load generator — spin up N Pods + Services + CRDs + measure cluster behavior. CI-friendly perf testing."),
        Flashcard(front="MTU mismatch symptom?", back="Small requests work; large requests silently drop. Often paired with ICMP \"Fragmentation needed\" being filtered. Fix: Pod MTU = host MTU − encap overhead."),
        Flashcard(front="conntrack saturation symptom?", back="High connection-per-second cluster; nf_conntrack_count near nf_conntrack_max; SYN drops + retries. Fix: tune nf_conntrack_max + hashsize; switch to eBPF (Cilium kube-proxy-replacement)."),
        Flashcard(front="cpu-manager-policy?", back="kubelet flag: <code>none</code> (default; CFS scheduler) or <code>static</code> (exclusive CPU per Guaranteed-QoS Pod). Static reduces context-switch + latency for latency-sensitive workloads."),
        Flashcard(front="Tetragon\'s enforce mode?", back="Tetragon can <em>kill</em> processes / block syscalls in kernel based on rules — runtime enforcement, not just observation. Reserve for tested rules; over-aggressive = self-DoS."),
    ],
    quizzes=[
        Quiz(
            prompt="A team upgrades CNI; cluster latency tail jumps 30%. Walk diagnostic.",
            answer="(1) <strong>Hubble flow latency histograms</strong>: per-Service P99 — which paths regressed? (2) <strong>Node-level perf top + eBPF</strong>: kernel hotspots? Conntrack? Encap path? (3) <strong>Compare CNI configs</strong>: pre / post upgrade — new feature flags? Encap mode change? Kube-proxy-replacement enabled? (4) <strong>kubectl-trace bpftrace</strong>: what kernel functions are hot? (5) <strong>Mitigation</strong>: revert CNI version OR disable the new feature OR scale resource. (6) <strong>Reproduce in dev</strong>: kube-burner with same workload to confirm fix before prod.",
        ),
        Quiz(
            prompt="A regulated cluster needs flow-level audit for every Pod-to-Pod call. Walk the design.",
            answer="(1) <strong>Hubble flow logs</strong>: emitted by Cilium eBPF; export to SIEM (Loki / Splunk) via Fluent Bit / Vector. (2) <strong>Retention</strong>: per-regime (1 year hot + S3 archive). (3) <strong>Per-flow context</strong>: namespace + workload + L7 verdict + drop reason — natively in Hubble events. (4) <strong>SIEM rules</strong>: alarm on \"flow to known-bad CIDRs,\" \"unexpected service-to-service flow,\" \"NetworkPolicy denial spike.\" (5) <strong>Compliance evidence</strong>: queries answer \"every flow into namespace X in past 90 days.\" (6) <strong>Cost</strong>: budget for Hubble retention; sampling for high-cardinality flows is OK if compliance allows.",
        ),
        Quiz(
            prompt="The CFO sees Pixie cost ($800/month) + asks to remove. Defend.",
            answer="\"<strong>Pixie pays for itself the first incident it shortens.</strong> Three reasons: (1) <strong>Zero-instrumentation L7 trace</strong>: no PR to add OTel SDK to every app; instant value. (2) <strong>Latency drift</strong>: Pixie shows P99 per Service per upstream over time — drift surfaces before incidents. (3) <strong>Cost framing</strong>: $800/month is one engineer-day. The next P99 incident saved &gt; one engineer-day. <strong>Trim cost</strong>: lower retention, sample high-cardinality services, scope to prod-only. <strong>Don\'t remove a tool whose value is one incident.</strong>\"",
            cyoa=True,
            cyoa_tag="how the network architect defended Pixie",
        ),
    ],
    glossary=[
        GlossaryItem(name="Hubble", definition="Cilium\'s eBPF-based flow visibility — L4 + L7 verdicts per flow."),
        GlossaryItem(name="Pixie", definition="CNCF eBPF observability — per-Service L7 trace (HTTP / gRPC / DB / DNS) without app changes."),
        GlossaryItem(name="Tetragon", definition="Cilium eBPF syscall + process trace + enforcement — security + runtime visibility."),
        GlossaryItem(name="tcpdump", definition="Classic packet capture; kernel-level. Last-resort tool for raw bytes."),
        GlossaryItem(name="kubectl-trace", definition="bpftrace-style kernel tracing on K8s nodes via kubectl plugin."),
        GlossaryItem(name="kubeshark", definition="Cluster-wide sniffer with per-Pod filters; L7 stream UI."),
        GlossaryItem(name="kube-burner", definition="Synthetic load generator for cluster perf testing — N Pods/Services/CRDs + timing."),
        GlossaryItem(name="conntrack", definition="Linux kernel connection tracker. Saturates at high CPS; tune nf_conntrack_max."),
        GlossaryItem(name="cpu-manager-policy=static", definition="kubelet pins exclusive CPUs to Guaranteed-QoS Pods. Lower context-switch + latency."),
        GlossaryItem(name="MTU mismatch", definition="Pod MTU > host MTU − encap overhead causes silent drops on large packets."),
    ],
    recap_lead="Hubble for flows; Pixie + Tetragon for in-app L7 + syscalls; tcpdump / kubectl-trace last-resort; kube-burner for proactive perf testing. Common fixes: MTU, conntrack, DNS scaling, QoS, cpu-manager-policy.",
    recap_next='<strong>Next — N7: Capstone — multi-cluster network across EKS + AKS + GKE + on-prem.</strong> Bridge selection per region; AdminNetworkPolicy fleet-wide; Hubble across clusters; runbook.',
)
