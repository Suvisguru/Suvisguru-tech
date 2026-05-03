"""Per-module Section 6 animations for K-AKS A1-A11."""

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


# A1 — AKS architecture: Standard vs Automatic
SCENE_A1 = f'''        {_mode_label()}
        {_box(40, 70, 150, 90, "Azure-managed", "control plane (free)", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(220, 35, 150, 50, "AKS Standard", "BYO add-ons", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(220, 95, 150, 50, "AKS Automatic", "preconfigured", fill="#A04832", label_color="#FFFFFF")}
        {_box(420, 70, 290, 90, "customer-managed data plane", "VNet · node pools · workloads · IAM", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(440, 110, 80, 40, "System NP", "CoreDNS", fill="#FFFFFF")}
        {_box(530, 110, 80, 40, "User NP", "your apps", fill="#FFFFFF")}
        {_box(620, 110, 80, 40, "Spot NP", "cheap", fill="#FFFFFF")}'''

ANIM_A1 = Animation(
    h2="AKS shared responsibility — Standard vs Automatic",
    intro="Two AKS shapes; one shared-responsibility split.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_A1,
    initial_packet_xy=(115, 115),
    initial_readout='<strong>Watching:</strong> two AKS shapes side by side.',
    scenes=[
        AnimationScene(
            mode_id="standard",
            button_label="▶ AKS Standard path",
            mode_label="Mode: AKS Standard — full control, manual add-ons",
            phases=[
                P(readout='<strong>Step 1.</strong> Azure runs the control plane (free, multi-AZ).', move_to=(295, 60), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Standard: you add Container Insights, Workload Identity, etc. one by one.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> Five node-pool types in your subscription: System / User / Spot / Win / GPU.', move_to=(565, 130), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Highest flexibility, longest setup. Pick this if you need the knobs.', duration_ms=400, pause_after_ms=2000),
            ],
        ),
        AnimationScene(
            mode_id="automatic",
            button_label="▶ AKS Automatic path",
            mode_label="Mode: AKS Automatic — preconfigured production stack",
            phases=[
                P(readout='<strong>Step 1.</strong> Azure runs the control plane.', move_to=(295, 60), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Automatic: AMP + Grafana + Container Insights + WI + Azure RBAC + NAP + KEDA + Cilium auto-on.', move_to=(295, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Day-1 production stack; node sizing/scaling delegated to Azure.', move_to=(565, 130), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# A2 — Two identity surfaces
SCENE_A2 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "kubectl user", "Entra principal", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "kubelogin", "browser auth + CA", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 80, 130, 60, "kube-apiserver", "Azure RBAC for K8s", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(40, 160, 110, 60, "App Pod", "wants Key Vault", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 160, 130, 60, "WI webhook", "injects SA token", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(340, 160, 130, 60, "Entra federated cred", "→ access token", fill="#A04832", label_color="#FFFFFF")}
        {_box(500, 120, 110, 60, "Key Vault", "GET secret", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 120, 100, 60, "200 OK", "audit logged", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A2 = Animation(
    h2="Two identity surfaces — human via kubelogin, Pod via Workload Identity",
    intro="Top track: human auth. Bottom track: Pod auth.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_A2,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> two AKS auth flows.',
    scenes=[
        AnimationScene(
            mode_id="human",
            button_label="▶ human via kubelogin",
            mode_label="Mode: human → cluster via Entra + Azure RBAC for K8s",
            phases=[
                P(readout='<strong>Step 1.</strong> User runs kubectl with Entra-integrated kubeconfig.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> kubelogin opens browser; Conditional Access fires (MFA / device).', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Token sent to apiserver; Azure RBAC for K8s authorises.', move_to=(405, 110), duration_ms=900, pause_after_ms=1800),
            ],
        ),
        AnimationScene(
            mode_id="pod",
            button_label="▶ Pod via Workload Identity",
            mode_label="Mode: Pod → Azure service via WI federated credential",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod requests a Key Vault secret.', move_to=(95, 190), duration_ms=400),
                P(readout='<strong>Step 2.</strong> WI webhook injects projected SA token + env vars.', move_to=(245, 190), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Federated credential trust matches; Entra returns Azure access token.', move_to=(405, 190), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Key Vault returns the secret; CloudTrail-equivalent (Activity Log) records.', move_to=(555, 150), duration_ms=900),
                P(readout='<strong>Step 5.</strong> 200 OK back to Pod. No long-lived secret stored anywhere.', move_to=(690, 150), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# A3 — Networking — request walks ALB → AGC → Pod
SCENE_A3 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "internet client", "GET /api", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "AGC (Gateway API)", "L7 LB", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 90, 130, 60, "HTTPRoute backend", "Pod IPs (overlay)", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 30, 110, 50, "Azure CNI Overlay", "Pod IPs decoupled", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 100, 110, 50, "Pod", "200 OK", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 170, 110, 50, "NAT Gateway", "egress (no SNAT exhaustion)", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(640, 90, 100, 60, "→ outbound API", "Stripe / Graph", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A3 = Animation(
    h2="A request walks — internet → AGC → Pod (overlay) → NAT Gateway egress",
    intro="Two flows: ingress + egress, with the modern AKS networking pattern.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_A3,
    initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> a request reach an AKS Pod via AGC.',
    scenes=[
        AnimationScene(
            mode_id="ingress",
            button_label="▶ ingress: internet → Pod",
            mode_label="Mode: AGC + Gateway API + Azure CNI Overlay",
            phases=[
                P(readout='<strong>Step 1.</strong> Internet client hits AGC public IP.', move_to=(95, 120), duration_ms=400),
                P(readout='<strong>Step 2.</strong> AGC matches HTTPRoute; finds backend Pod IPs.', move_to=(245, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Routing target: Pod IP from overlay CIDR (decoupled from VNet).', move_to=(405, 120), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Pod responds 200; AGC returns to client.', move_to=(555, 125), duration_ms=900, pause_after_ms=2000),
            ],
        ),
        AnimationScene(
            mode_id="egress",
            button_label="▶ egress via NAT Gateway",
            mode_label="Mode: Pod → outbound API via NAT Gateway",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod calls outbound API (Stripe).', move_to=(555, 125), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Egress routed via NAT Gateway — 64K SNAT ports per IP, no exhaustion.', move_to=(555, 195), duration_ms=900),
                P(readout='<strong>Step 3.</strong> External API responds; return path same.', move_to=(690, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# A4 — PVC picks Disk vs Files
SCENE_A4 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "PVC submitted", "RWO or RWX?", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "StorageClass picker", "disk vs files vs blob", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "Premium SSD v2", "RWO · single-AZ", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "Azure Files (RWX)", "SMB or NFS", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "Blob CSI / ANF", "object / DB extreme", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "WaitForFirstConsumer", "AZ-aligned", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Pod Running", "PV mounted", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A4 = Animation(
    h2="A PVC picks the right CSI driver",
    intro="Same PVC; different access modes; very different storage backends.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_A4,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> PVC binding for different access modes.',
    scenes=[
        AnimationScene(
            mode_id="disk",
            button_label="▶ RWO → Disk",
            mode_label="Mode: RWO PVC → Premium SSD v2 with WaitForFirstConsumer",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod requests RWO 50 GiB Premium SSD v2.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Default SC has WaitForFirstConsumer — wait for Pod scheduling.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Scheduler picks node in eastus-1; disk provisions in same AZ.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Mount succeeds; Pod Running.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Later: tune IOPS up via VolumeAttributesClass — no remount.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="files",
            button_label="▶ RWX → Files",
            mode_label="Mode: RWX PVC → Azure Files (SMB or NFS)",
            phases=[
                P(readout='<strong>Step 1.</strong> Two Pods in two AZs need shared writable storage.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Azure Files CSI selected — only RWX option.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Both Pods mount the same share; concurrent read+write.', move_to=(405, 125), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# A5 — NAP burst + consolidation
SCENE_A5 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "100 Pending Pods", "burst", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "NAP / Karpenter", "watches scheduler", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "Spot pool (Cobalt)", "ARM · cheap", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "GPU pool", "NC A100", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "Confidential", "DCasv5 SEV-SNP", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "consolidation", "rebin idle", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "node count ↓", "savings", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A5 = Animation(
    h2="NAP picks the cheapest node mix and consolidates idle",
    intro="Burst → optimal SKU mix → consolidation cycle.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_A5,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a 100-Pod burst handled by NAP.',
    scenes=[
        AnimationScene(
            mode_id="burst",
            button_label="▶ burst + consolidation",
            mode_label="Mode: NAP picks Spot Cobalt; GPU; consolidates",
            phases=[
                P(readout='<strong>Step 1.</strong> 100 Pods Pending — kube-scheduler can\'t place them.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> NAP sees the unschedulable set; computes optimal SKU mix.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Spot Cobalt (ARM) for cost-tolerant; ~25% cheaper than x86.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> GPU pool A100 for ML; Confidential for one PII pod.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Consolidation rebins idle Pods; empty nodes terminated.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Cost down ~40%.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# A6 — security pipeline image → admission → runtime
SCENE_A6 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "build CI", "image", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "Defender + ACR scan", "Cosign / Notation sign", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 130, 50, "Image Cleaner", "purge vulnerable", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "Azure Policy / PSA", "admission verify", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "Bottlerocket / AL3", "minimal node OS", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 90, 110, 60, "Pod Running", "secure", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 90, 100, 60, "Defender runtime", "watch", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A6 = Animation(
    h2="A signed image walks from CI to a guarded node",
    intro="Sign → scan → admission verify → minimal OS → runtime watch.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_A6,
    initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> a hardened deploy path.',
    scenes=[
        AnimationScene(
            mode_id="signed",
            button_label="▶ signed image lifecycle",
            mode_label="Mode: sign → Defender scan → Policy verify → AL3 → Defender runtime",
            phases=[
                P(readout='<strong>Step 1.</strong> CI builds image; Cosign / Notation signs.', move_to=(245, 120), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Defender scans in ACR; findings queryable.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Azure Policy / PSA Restricted admission verifies signature + Pod settings.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Pod scheduled on Azure Linux 3 (or Bottlerocket-equivalent) — minimal attack surface.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Pod Running. Image Cleaner watches for new CVEs.', move_to=(555, 120), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Defender runtime monitors syscalls live.', move_to=(690, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# A7 — observability signal flow
SCENE_A7 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "Pod", "emits signals", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "ADOT collector", "DaemonSet", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 130, 50, "AMP", "Prometheus metrics", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "Container Insights", "logs + workbooks", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "App Insights / OTel", "traces", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "AMG dashboard", "joined view", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "alert", "Action Group", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A7 = Animation(
    h2="A signal travels from Pod to PagerDuty",
    intro="Three pipes joined in AMG; alert fires.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_A7,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a metric → ADOT → AMP → AMG → alert.',
    scenes=[
        AnimationScene(
            mode_id="trace",
            button_label="▶ signal flow",
            mode_label="Mode: ADOT collects, AMP/CI/App Insights store, AMG visualises, alert fires",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod emits a Prometheus metric, a structured log, and a span.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> ADOT collector (per-node DaemonSet) fans out by signal type.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Metric → AMP (managed Prometheus).', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Log → Container Insights / Log Analytics.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Span → App Insights or managed OpenTelemetry.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 6.</strong> AMG dashboard joins all three; alert rule fires.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 7.</strong> Action Group → PagerDuty / Teams / email.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# A8 — Fleet Manager workload propagation
SCENE_A8 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "platform team", "git push", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "Fleet Manager", "FleetWorkload CR", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 110, 50, "AKS east-us", "synced", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 90, 110, 50, "AKS west-eu", "synced", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 150, 110, 50, "AKS asia-se", "synced", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(480, 90, 110, 60, "all 50 clusters", "policy applied", fill="#A04832", label_color="#FFFFFF")}
        {_box(620, 90, 110, 60, "compliance", "verified", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A8 = Animation(
    h2="Fleet Manager propagates one policy to 50 clusters",
    intro="One git push; one Fleet apply; 50 clusters reconcile.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_A8,
    initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> Fleet workload propagation.',
    scenes=[
        AnimationScene(
            mode_id="propagate",
            button_label="▶ propagate to 50 clusters",
            mode_label="Mode: Fleet Manager — apply once, sync everywhere",
            phases=[
                P(readout='<strong>Step 1.</strong> Platform team commits NetworkPolicy to git.', move_to=(95, 120), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Fleet Manager creates FleetWorkload referencing the policy.', move_to=(245, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Fan-out: east-us...', move_to=(395, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> ...west-eu...', move_to=(395, 115), duration_ms=900),
                P(readout='<strong>Step 5.</strong> ...asia-se. All members reconcile.', move_to=(395, 175), duration_ms=900),
                P(readout='<strong>Step 6.</strong> 50 clusters now enforce the same policy. Compliance report green.', move_to=(675, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# A9 — AKS upgrade walk
SCENE_A9 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "v1.30 cluster", "current", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(180, 80, 110, 60, "pre-flight", "kubent + Pluto", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(310, 80, 110, 60, "CP upgrade", "in place", fill="#A04832", label_color="#FFFFFF")}
        {_box(440, 80, 110, 60, "add-ons", "managed bump", fill="#A04832", label_color="#FFFFFF")}
        {_box(570, 80, 110, 60, "node pools", "surge 33%", fill="#A04832", label_color="#FFFFFF")}
        {_box(40, 160, 640, 50, "smoke pass · v1.31 cluster Ready", "rollback path: blue-green node pool", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A9 = Animation(
    h2="An AKS minor upgrade — v1.30 → v1.31",
    intro="Pre-flight first; CP, then add-ons, then nodes with surge.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_A9,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a controlled AKS minor upgrade.',
    scenes=[
        AnimationScene(
            mode_id="upgrade",
            button_label="▶ minor upgrade",
            mode_label="Mode: minor upgrade in AKS-blessed order",
            phases=[
                P(readout='<strong>Step 1.</strong> Cluster on v1.30. Healthy.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Pre-flight: kubent + Pluto find deprecated APIs in YAML/Helm.', move_to=(235, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Azure upgrades the control plane in place. ~30 min, no downtime.', move_to=(365, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Bump managed add-ons (Container Insights, AMP, Defender, Flux).', move_to=(495, 110), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Roll node pools with surge 33%; PDB-aware drains.', move_to=(625, 110), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Smoke tests pass. v1.31 cluster Ready.', move_to=(360, 185), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# A10 — Workload Identity 401 troubleshooting
SCENE_A10 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "Pod 401", "Key Vault denied", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "Resource Health", "Azure-side OK", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "Activity Log", "cluster recreated 2d ago", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "AKS Diagnostic Settings", "no apiserver errors", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "fix: update fed cred", "OIDC issuer URL", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "redeploy fed cred", "subject matches", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(640, 80, 100, 60, "Pod Running", "fixed", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A10 = Animation(
    h2="Workload Identity 401 — diagnose with Resource Health → Activity Log → fix",
    intro="The standard AKS triage playbook applied to a WI 401.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_A10,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a 401 root-cause hunt.',
    scenes=[
        AnimationScene(
            mode_id="diag",
            button_label="▶ diagnose + fix",
            mode_label="Mode: WI 401 → fed cred OIDC mismatch → fix",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod returns 401 from Key Vault.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Check Azure Resource Health first — Azure side healthy.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Activity Log shows: cluster recreated 2 days ago by IaC pipeline.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> AKS Diagnostic Settings show no apiserver errors.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Diagnosis: cluster\'s OIDC issuer URL changed; fed cred still trusts the old URL.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Update federated credential issuer to the new cluster\'s OIDC URL.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 7.</strong> Pod\'s next call succeeds. Postmortem updates the IaC re-create runbook.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# A11 — capstone walk
SCENE_A11 = f'''        {_mode_label()}
        {_box(40, 90, 130, 50, "Phase A — base", "private + Cilium + NAP", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(200, 90, 130, 50, "Phase B — platform", "WI + AGC + obs", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(360, 90, 130, 50, "Phase C — ops", "Defender + Flux + DR", fill="#A04832", label_color="#FFFFFF")}
        {_box(520, 90, 110, 50, "Phase D — defence", "review + drill", fill="#E8B547", label_color="#5A4F45")}
        {_box(660, 90, 80, 50, "K-AKS-complete", "graduate", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_A11 = Animation(
    h2="The K-AKS capstone — A → B → C → D",
    intro="Four phases; each gates the next.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_A11,
    initial_packet_xy=(95, 115),
    initial_readout='<strong>Watching:</strong> the K-AKS capstone walk.',
    scenes=[
        AnimationScene(
            mode_id="walk",
            button_label="▶ end-to-end walk",
            mode_label="Mode: A → B → C → D → K-AKS-complete",
            phases=[
                P(readout='<strong>Phase A.</strong> Private AKS Automatic + Cilium dataplane + NAP + Premium tier with LTS.', move_to=(105, 115), duration_ms=900),
                P(readout='<strong>Phase B.</strong> Workload Identity + AGC (Gateway API) + storage + Container Insights + AMP + AMG.', move_to=(265, 115), duration_ms=900),
                P(readout='<strong>Phase C.</strong> Defender for Containers + Azure Policy + Flux v2 GitOps + Velero + blue-green upgrade.', move_to=(425, 115), duration_ms=900),
                P(readout='<strong>Phase D.</strong> Architecture defended; live drill: node kill + MI revoke + Defender finding + DR restore.', move_to=(575, 115), duration_ms=900),
                P(readout='<strong>K-AKS-complete.</strong> Bicep + arch doc + DR runbook + drill recording. Graduate.', move_to=(700, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


ANIMATIONS = {
    "01": ANIM_A1, "02": ANIM_A2, "03": ANIM_A3, "04": ANIM_A4,
    "05": ANIM_A5, "06": ANIM_A6, "07": ANIM_A7, "08": ANIM_A8,
    "09": ANIM_A9, "10": ANIM_A10, "11": ANIM_A11,
}
