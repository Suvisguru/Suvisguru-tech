"""Per-module Section 6 animations for K-ADV-NET N1-N7."""

from _helpers import Animation, AnimationScene, AnimationPhase as P


def _box(x, y, w, h, label, sub=None, fill="#FFFFFF", stroke="#3F4A5E", label_color="#3F4A5E"):
    sub_html = f'<text x="{x+w//2}" y="{y+38}" text-anchor="middle" font-size="9" fill="#6B6058">{sub}</text>' if sub else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        f'<text x="{x+w//2}" y="{y+22}" text-anchor="middle" font-size="11" font-weight="700" fill="{label_color}">{label}</text>'
        f'{sub_html}'
    )


def _mode_label(x=380, y=22):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="13" font-weight="600" fill="#3F4A5E" id="anim-mode-label">Mode</text>'


# N1 — CNI + eBPF + BGP
SCENE_N1 = f'''        {_mode_label()}
        {_box(40, 70, 150, 100, "Pod / veth pair", "node-local", fill="#5DCAA5", label_color="#1F2433")}
        {_box(220, 70, 150, 100, "CNI plugin", "Cilium / Calico / Flannel", fill="#3878B5", label_color="#FBF1D6")}
        {_box(400, 70, 150, 100, "eBPF program", "kernel datapath", fill="#FAC775", label_color="#1F2433")}
        {_box(580, 70, 140, 100, "BGP fabric", "node ↔ ToR ↔ DC", fill="#5A6B81", label_color="#FBF1D6")}'''

ANIM_N1 = Animation(
    h2="Pod packet → veth → eBPF → BGP fabric",
    intro="A packet leaves a Pod, hits the CNI, gets accelerated by eBPF, lands on the BGP-routed fabric.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_N1,
    initial_packet_xy=(115, 120),
    initial_readout='<strong>Watching:</strong> a packet through the CNI + BGP fabric.',
    scenes=[
        AnimationScene(
            mode_id="ebpf_path",
            button_label="▶ Pod → fabric",
            mode_label="Mode: Pod packet through CNI + eBPF + BGP",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod sends packet through veth pair into the host\'s network namespace.', move_to=(115, 120), duration_ms=900),
                P(readout='<strong>Step 2.</strong> CNI plugin (Cilium / Calico) handles routing, encapsulation, policy.', move_to=(295, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> eBPF program intercepts in-kernel — applies LB / NetPol / encap with no userspace hop.', move_to=(475, 120), duration_ms=900),
                P(readout='<strong>Step 4.</strong> BGP advertises Pod CIDRs to ToR; fabric routes natively.', move_to=(650, 120), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# N2 — Gateway API
SCENE_N2 = f'''        {_mode_label()}
        {_box(40, 70, 160, 80, "GatewayClass", "city operator", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(220, 70, 160, 80, "Gateway", "listener bank (host:port:protocol)", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(400, 70, 200, 80, "HTTPRoute / GRPCRoute / TCPRoute", "match + filter + backend ref", fill="#5DCAA5", label_color="#1F2433")}
        {_box(620, 70, 100, 80, "Service / Pod", "backend", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "BackendTLSPolicy + ReferenceGrant + cross-namespace routing — fleet-scale Gateway API", "richer than Ingress", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_N2 = Animation(
    h2="Gateway API at fleet scale",
    intro="GatewayClass → Gateway → HTTPRoute → Service. Three roles; cross-namespace routing.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_N2,
    initial_packet_xy=(115, 110),
    initial_readout='<strong>Watching:</strong> a request via Gateway API.',
    scenes=[
        AnimationScene(
            mode_id="gw",
            button_label="▶ Gateway → Route → backend",
            mode_label="Mode: Gateway API hierarchy",
            phases=[
                P(readout='<strong>Step 1.</strong> GatewayClass = the controller / city operator (e.g., Envoy Gateway, Istio).', move_to=(120, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Gateway = listener bank (port 443 HTTPS + cert + hostname).', move_to=(300, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> HTTPRoute attaches to Gateway; matches + filters; refs backend Service.', move_to=(500, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Cross-namespace via ReferenceGrant; BackendTLSPolicy for re-encrypt.', move_to=(670, 110), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# N3 — Multi-cluster networking
SCENE_N3 = f'''        {_mode_label()}
        {_box(40, 70, 180, 90, "Cluster A", "EKS in us-east-1", fill="#3878B5", label_color="#FBF1D6")}
        {_box(290, 70, 180, 90, "Cluster B", "GKE in europe-west1", fill="#5A9F7A", label_color="#FBF1D6")}
        {_box(540, 70, 180, 90, "Cluster C", "AKS in eastus", fill="#5E4A8E", label_color="#FBF1D6")}
        {_box(40, 180, 680, 50, "Submariner / Skupper / Cilium ClusterMesh / Istio multi-cluster — pick by trust + perf needs", "inter-cluster fabric options", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_N3 = Animation(
    h2="Inter-cluster bridges — Submariner / Skupper / Cilium ClusterMesh / Istio multi-cluster",
    intro="Three clouds; one logical network. Pick the bridge by trust model + perf.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_N3,
    initial_packet_xy=(135, 110),
    initial_readout='<strong>Watching:</strong> cross-cluster traffic.',
    scenes=[
        AnimationScene(
            mode_id="multi",
            button_label="▶ multi-cluster routing",
            mode_label="Mode: cross-cluster traffic",
            phases=[
                P(readout='<strong>Step 1.</strong> Cluster A in AWS east; service-A invokes service-B in another cluster.', move_to=(135, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Bridge (Submariner / Cilium ClusterMesh / Skupper / Istio) tunnels or routes across.', move_to=(380, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Cluster B in GCP serves; latency + encryption per the bridge\'s design.', move_to=(630, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Pick bridge by needs: low-latency (Cilium ClusterMesh BGP), zero-trust (Skupper / Istio), L4-only (Submariner).', move_to=(380, 205), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# N4 — Service mesh + DNS + IPv6
SCENE_N4 = f'''        {_mode_label()}
        {_box(40, 70, 180, 80, "Service mesh", "Istio / Linkerd / Cilium", fill="#5DCAA5", label_color="#1F2433")}
        {_box(240, 70, 180, 80, "CoreDNS at scale", "NodeLocal DNSCache", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(440, 70, 280, 80, "IPv6 / dual-stack", "host + Pod + Service", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "DNS scale = NodeLocal DNSCache + ndots + autoPath. IPv6 = enable on cluster + CNI + Service", "scaling tips", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_N4 = Animation(
    h2="Service mesh + DNS + IPv6 at scale",
    intro="Three concerns interlock: who handles east-west; how DNS scales; how dual-stack works.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_N4,
    initial_packet_xy=(130, 110),
    initial_readout='<strong>Watching:</strong> mesh + DNS + IPv6 layout.',
    scenes=[
        AnimationScene(
            mode_id="mesh_dns",
            button_label="▶ mesh + DNS + IPv6",
            mode_label="Mode: scale concerns",
            phases=[
                P(readout='<strong>Step 1.</strong> Mesh handles Pod-to-Pod mTLS + retries + observability.', move_to=(130, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> DNS at scale: NodeLocal DNSCache + ndots:1 + autoPath cuts CoreDNS load 5×.', move_to=(330, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> IPv6 / dual-stack: every Pod gets IPv4 + IPv6; Services dual-listening.', move_to=(580, 110), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# N5 — NetworkPolicy + egress + private
SCENE_N5 = f'''        {_mode_label()}
        {_box(40, 70, 180, 80, "NetworkPolicy default-deny", "+ explicit allow per consumer", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(240, 70, 180, 80, "egress gateway", "all egress through one path", fill="#A04832", label_color="#FBF1D6")}
        {_box(440, 70, 180, 80, "private cluster", "no public apiserver", fill="#5DCAA5", label_color="#1F2433")}
        {_box(640, 70, 80, 80, "hybrid", "VPN + DX", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "AdminNetworkPolicy (org-wide) > NetworkPolicy (team) > BaselineANP. CIDR + FQDN egress controls.", "policy hierarchy", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_N5 = Animation(
    h2="NetworkPolicy hierarchy + egress controls",
    intro="Default-deny; org policy beats team policy; egress through gateway; private + hybrid.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_N5,
    initial_packet_xy=(130, 110),
    initial_readout='<strong>Watching:</strong> NetPol + egress + private.',
    scenes=[
        AnimationScene(
            mode_id="netpol",
            button_label="▶ policy + egress walk",
            mode_label="Mode: policy hierarchy",
            phases=[
                P(readout='<strong>Step 1.</strong> Default-deny NetworkPolicy at namespace; explicit allow per consumer.', move_to=(130, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Egress goes through a single egress gateway — auditable + controllable.', move_to=(330, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Private cluster: apiserver private; nodes private; access via VPN / DX.', move_to=(530, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> AdminNetworkPolicy (org-wide) overrides NetworkPolicy (team).', move_to=(380, 185), duration_ms=900, pause_after_ms=2200),
            ],
        ),
    ],
)


# N6 — Packet tracing + perf
SCENE_N6 = f'''        {_mode_label()}
        {_box(40, 70, 200, 80, "Hubble (Cilium)", "eBPF flow logs", fill="#3878B5", label_color="#FBF1D6")}
        {_box(260, 70, 200, 80, "Pixie / Tetragon", "syscall + L7 trace", fill="#5DCAA5", label_color="#1F2433")}
        {_box(480, 70, 240, 80, "tcpdump / kubectl-trace / kube-burner", "kernel + cluster perf", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "MTU mismatch, conntrack saturation, kernel scheduling — tuning surfaces from these tools", "common findings", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_N6 = Animation(
    h2="Packet tracing + performance tuning",
    intro="Hubble + Pixie + tcpdump surface what\'s happening; tuning closes the loop.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_N6,
    initial_packet_xy=(140, 110),
    initial_readout='<strong>Watching:</strong> packet tracing tools.',
    scenes=[
        AnimationScene(
            mode_id="trace",
            button_label="▶ packet tracing tour",
            mode_label="Mode: trace + tune",
            phases=[
                P(readout='<strong>Step 1.</strong> Hubble = Cilium\'s eBPF flow log; per-Pod connection visibility.', move_to=(140, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Pixie + Tetragon = syscall + L7 trace; HTTP / DNS / SQL inspection without app changes.', move_to=(360, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> tcpdump / kubectl-trace / kube-burner = kernel + cluster-wide perf.', move_to=(600, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Common findings: MTU mismatch, conntrack saturation, kernel tuning.', move_to=(380, 185), duration_ms=900, pause_after_ms=2200),
            ],
        ),
    ],
)


# N7 — Capstone: multi-region, multi-cloud
SCENE_N7 = f'''        {_mode_label()}
        {_box(40, 70, 130, 60, "EKS us-east", "AWS region", fill="#3878B5", label_color="#FBF1D6")}
        {_box(190, 70, 130, 60, "AKS eastus", "Azure region", fill="#5E4A8E", label_color="#FBF1D6")}
        {_box(340, 70, 130, 60, "GKE europe-west1", "GCP region", fill="#5A9F7A", label_color="#FBF1D6")}
        {_box(490, 70, 130, 60, "OCP / Tanzu", "on-prem", fill="#A04832", label_color="#FBF1D6")}
        {_box(640, 70, 80, 60, "fleet mgr", "+ DNS + LB", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "Cilium ClusterMesh + Submariner + Istio multi-cluster + Skupper + AdminNetworkPolicy + Gateway API + private hybrid", "multi-cloud network", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_N7 = Animation(
    h2="Multi-cluster network across EKS + AKS + GKE + on-prem",
    intro="Five clusters across three clouds + on-prem. One logical network, multiple bridges.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_N7,
    initial_packet_xy=(105, 100),
    initial_readout='<strong>Watching:</strong> the multi-region capstone.',
    scenes=[
        AnimationScene(
            mode_id="capstone",
            button_label="▶ multi-cloud network walk",
            mode_label="Mode: full multi-region capstone",
            phases=[
                P(readout='<strong>Phase A.</strong> Five clusters across AWS + Azure + GCP + on-prem.', move_to=(105, 100), duration_ms=900),
                P(readout='<strong>Phase B.</strong> Cilium ClusterMesh between same-cloud peers; Submariner + Skupper for cross-cloud.', move_to=(255, 100), duration_ms=900),
                P(readout='<strong>Phase C.</strong> Gateway API at edge per region; cross-region via global LB + DNS.', move_to=(405, 100), duration_ms=900),
                P(readout='<strong>Phase D.</strong> AdminNetworkPolicy enforces org-wide rules; team NetworkPolicies refine.', move_to=(555, 100), duration_ms=900),
                P(readout='<strong>Phase E.</strong> Private clusters + hybrid via VPN/DX; egress gateways auditable.', move_to=(680, 100), duration_ms=900),
                P(readout='<strong>Phase F.</strong> Hubble + Pixie everywhere; latency budgets per path; runbook closes the loop.', move_to=(380, 185), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


ANIMATIONS = {
    "01": ANIM_N1,
    "02": ANIM_N2,
    "03": ANIM_N3,
    "04": ANIM_N4,
    "05": ANIM_N5,
    "06": ANIM_N6,
    "07": ANIM_N7,
}
