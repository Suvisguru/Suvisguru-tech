"""Per-module Section 6 animations for K-GKE G1-G10."""

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


# G1 — modes: Standard vs Autopilot
SCENE_G1 = f'''        {_mode_label()}
        {_box(40, 70, 150, 100, "Google-managed", "control plane (free)", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(220, 60, 200, 50, "GKE Standard", "you manage node pools", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(220, 130, 200, 50, "GKE Autopilot", "Google manages nodes · per-Pod billing", fill="#A04832", label_color="#FFFFFF")}
        {_box(450, 70, 270, 100, "Customer-managed data plane", "VPC + node pools + workloads + IAM + cost", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}'''

ANIM_G1 = Animation(
    h2="GKE shared responsibility — Standard vs Autopilot",
    intro="Two GKE shapes; one shared-responsibility split.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_G1,
    initial_packet_xy=(115, 120),
    initial_readout='<strong>Watching:</strong> two GKE modes side by side.',
    scenes=[
        AnimationScene(
            mode_id="standard",
            button_label="▶ GKE Standard path",
            mode_label="Mode: GKE Standard — you manage node pools",
            phases=[
                P(readout='<strong>Step 1.</strong> Google runs the control plane (free, regional 3-zone HA).', move_to=(295, 85), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Standard: you create + size node pools (System / User / Spot / GPU).', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> Highest flexibility, highest ops surface. Pick when you need every knob.', move_to=(580, 120), duration_ms=900, pause_after_ms=2000),
            ],
        ),
        AnimationScene(
            mode_id="autopilot",
            button_label="▶ GKE Autopilot path",
            mode_label="Mode: GKE Autopilot — Google manages nodes; per-Pod billing",
            phases=[
                P(readout='<strong>Step 1.</strong> Google runs the control plane.', move_to=(295, 85), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Autopilot: Google manages nodes; admission webhooks enforce safety; per-Pod billing.', move_to=(295, 155), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Idle = $0; Pod-level SLA; minimal ops surface.', move_to=(580, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# G2 — release channels
SCENE_G2 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "v1.34 release", "Google ships", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "Rapid channel", "weeks behind upstream", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 80, 130, 60, "Regular (default)", "balanced cadence", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 80, 130, 60, "Stable", "conservative", fill="#7AB3CC", label_color="#FBF1D6")}
        {_box(640, 80, 100, 60, "Extended", "~2 yr LTS", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(40, 160, 700, 50, "maintenance window + exclusion + Pub/Sub upgrade notifications", "operator controls", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}'''

ANIM_G2 = Animation(
    h2="A new minor walks down the release channels",
    intro="Rapid first; then Regular; then Stable; LTS minors land in Extended.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_G2,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a new minor flow through the channels.',
    scenes=[
        AnimationScene(
            mode_id="cadence",
            button_label="▶ release cadence walk",
            mode_label="Mode: a new minor flows Rapid → Regular → Stable → Extended",
            phases=[
                P(readout='<strong>Step 1.</strong> Google releases v1.34. Lands in Rapid first.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Bakes weeks in Rapid; canary clusters validate.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> Promoted to Regular. Default channel; SLA.', move_to=(405, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Validated further; promoted to Stable.', move_to=(565, 110), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Designated minors get LTS in Extended (~2 yr).', move_to=(690, 110), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Operator controls: maintenance window + exclusions + Pub/Sub notifications.', move_to=(390, 185), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# G3 — networking — request walks via Gateway → NEG → Pod
SCENE_G3 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "internet client", "GET /api", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "GKE Gateway", "Gateway API", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 90, 130, 60, "NEG (container-native)", "Pod IPs", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 30, 110, 50, "Cilium dataplane", "Dataplane V2", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 100, 110, 50, "Pod (alias IP)", "VPC-native", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 170, 110, 50, "Cloud NAT", "egress (no SNAT exhaust)", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(640, 90, 100, 60, "→ outbound API", "Stripe / GitHub", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_G3 = Animation(
    h2="A request walks — internet → Gateway → NEG → Pod (alias IP) → Cloud NAT egress",
    intro="Two flows: ingress + egress; the modern GKE networking pattern.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_G3,
    initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> a request reach a GKE Pod via Gateway controller.',
    scenes=[
        AnimationScene(
            mode_id="ingress",
            button_label="▶ ingress: internet → Pod",
            mode_label="Mode: GKE Gateway + NEG + VPC-native + Dataplane V2",
            phases=[
                P(readout='<strong>Step 1.</strong> Internet client hits Gateway global anycast IP.', move_to=(95, 120), duration_ms=400),
                P(readout='<strong>Step 2.</strong> GKE Gateway controller programs Cloud LB; matches HTTPRoute.', move_to=(245, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> NEG holds Pod IPs (container-native LB); kube-proxy not in path.', move_to=(405, 120), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Cilium eBPF dataplane (Dataplane V2) routes; NetworkPolicy enforced.', move_to=(555, 55), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Pod has real VPC IP via alias range; serves the request.', move_to=(555, 125), duration_ms=900, pause_after_ms=2000),
            ],
        ),
        AnimationScene(
            mode_id="egress",
            button_label="▶ egress via Cloud NAT",
            mode_label="Mode: Pod → outbound API via Cloud NAT",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod calls outbound API (Stripe).', move_to=(555, 125), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Egress routes via Cloud NAT — managed; per-IP SNAT scales automatically.', move_to=(555, 195), duration_ms=900),
                P(readout='<strong>Step 3.</strong> External API responds; return path same.', move_to=(690, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# G4 — security pipeline image → BinAuth → Pod
SCENE_G4 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "build CI", "image", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "Artifact Registry", "scan + KMS attest", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 130, 50, "Binary Authorization", "verify attestation", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "Policy Controller", "PSA + custom rules", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "Confidential GKE", "AMD SEV / Intel TDX", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 90, 110, 60, "Pod Running", "secure", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 90, 100, 60, "CTD watch", "Security Command Center", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_G4 = Animation(
    h2="A signed image walks from CI to a guarded Pod",
    intro="Sign + scan → BinAuth verify → Policy admission → Confidential node → CTD runtime.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_G4,
    initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> a hardened deploy path.',
    scenes=[
        AnimationScene(
            mode_id="signed",
            button_label="▶ signed image lifecycle",
            mode_label="Mode: CI → AR scan + KMS attest → BinAuth → Policy → Confidential → CTD",
            phases=[
                P(readout='<strong>Step 1.</strong> CI builds image; pushes to Artifact Registry; scan emits attestation via KMS.', move_to=(245, 120), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Binary Authorization at admission verifies attestation.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Policy Controller enforces PSA Restricted + custom rules.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Pod scheduled on Confidential GKE Node — silicon memory encryption.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Pod Running.', move_to=(555, 120), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Container Threat Detection (in SCC) watches runtime behaviour.', move_to=(690, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# G5 — PVC → PD vs Filestore vs Hyperdisk
SCENE_G5 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "PVC submitted", "RWO or RWX?", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "StorageClass picker", "PD vs Files vs Hyperdisk", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "pd-balanced", "RWO single-zone", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "Hyperdisk + Pool", "live IOPS retier (VAC)", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "Filestore RWX / GCS FUSE", "shared / object", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "WaitForFirstConsumer", "AZ-aligned", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Pod Running", "PV mounted", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_G5 = Animation(
    h2="A PVC picks the right CSI driver",
    intro="Same PVC; different access modes; very different storage backends.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_G5,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> PVC binding for different access modes.',
    scenes=[
        AnimationScene(
            mode_id="pd",
            button_label="▶ RWO → pd-balanced",
            mode_label="Mode: RWO PVC → pd-balanced + WaitForFirstConsumer",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod requests RWO 50 GiB pd-balanced.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Default SC has WaitForFirstConsumer — wait for Pod scheduling.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Scheduler picks node in us-central1-a; PD provisions in same zone.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Mount succeeds; Pod Running.', move_to=(555, 110), duration_ms=900, pause_after_ms=2000),
            ],
        ),
        AnimationScene(
            mode_id="hyperdisk",
            button_label="▶ Hyperdisk + VAC live retier",
            mode_label="Mode: Hyperdisk + Storage Pool + VolumeAttributesClass",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod\'s PVC bound to Hyperdisk Balanced from a Storage Pool.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Black Friday burst — apply VAC with target 16K IOPS.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Hyperdisk applies online; no Pod restart; new IOPS available.', move_to=(555, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# G6 — NAP burst + consolidation + Compute Class
SCENE_G6 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "100 Pending Pods", "burst", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "NAP + Compute Class", "watches scheduler", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "Spot Cobalt T2A (ARM)", "Scale-Out class · cheap", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "GPU pool A4 H200", "Accelerator class", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "TPU Trillium", "Accelerator class", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "Autopilot per-Pod billing", "idle = $0", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "BQ cost export", "per-namespace", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_G6 = Animation(
    h2="NAP picks SKU mix; Autopilot bills per Pod; BQ exposes per-namespace cost",
    intro="Burst → optimal SKU mix → per-Pod billing → cost visibility.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_G6,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a 100-Pod burst handled by NAP.',
    scenes=[
        AnimationScene(
            mode_id="burst",
            button_label="▶ burst + per-Pod billing + cost",
            mode_label="Mode: NAP picks Spot ARM / GPU / TPU; Autopilot bills per Pod; BQ shows cost",
            phases=[
                P(readout='<strong>Step 1.</strong> 100 Pods Pending — kube-scheduler can\'t place them.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> NAP + Compute Classes pick SKUs across the catalog.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Spot Cobalt T2A (ARM) for cost-tolerant; ~25% cheaper.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> GPU pool A4 H200 for ML; TPU Trillium for distributed training.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Autopilot bills per Pod-second; idle = $0.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 6.</strong> BigQuery cost export joins billing rows with namespace metadata.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# G7 — observability signal flow → AMG
SCENE_G7 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "Pod", "emits signals", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "OpenTelemetry / agent", "auto-instrumented", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 130, 50, "GMP", "Prometheus metrics", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "Cloud Logging", "logs + Logs Explorer", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "Cloud Trace + Profiler", "spans + flame graphs", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "managed Grafana", "joined view", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "burn-rate alert", "Pub/Sub → PD", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_G7 = Animation(
    h2="A signal travels from Pod to PagerDuty",
    intro="Three pipes joined in managed Grafana; SLO burn-rate alert fires.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_G7,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a metric → GMP → Grafana → SLO alert.',
    scenes=[
        AnimationScene(
            mode_id="trace",
            button_label="▶ signal flow + SLO alert",
            mode_label="Mode: GMP / Cloud Logging / Cloud Trace → Grafana → burn-rate alert",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod emits a Prometheus metric, a structured log, and a span.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> OpenTelemetry / agent ships signals via the right exporter.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Metric → GMP (managed Prometheus, PromQL).', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Log → Cloud Logging / Logs Explorer.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Span → Cloud Trace; Profiler captures flame graph.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Managed Grafana joins all three; SLO panel turns red.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 7.</strong> Burn-rate alert (14× sustainable for 1h) → Pub/Sub → PagerDuty.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# G8 — Fleet workload propagation + AI inference
SCENE_G8 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "platform team", "git push", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "Fleet + Config Sync", "RootSync + RepoSync", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 110, 50, "GKE us-central1", "synced", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 90, 110, 50, "GKE-on-AWS eu-west", "synced", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 150, 110, 50, "GKE-on-VMware on-prem", "synced", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(480, 80, 130, 60, "Inference Gateway", "KV-cache routing", fill="#A04832", label_color="#FFFFFF")}
        {_box(630, 80, 100, 60, "vLLM A4 H200", "Llama 3 70B", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_G8 = Animation(
    h2="Fleet propagates policy to all clusters; AI Inference Gateway routes intelligently",
    intro="One git push → all clusters reconcile; LLM request routed by KV-cache locality.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_G8,
    initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> Fleet propagation + AI inference flow.',
    scenes=[
        AnimationScene(
            mode_id="propagate",
            button_label="▶ Fleet propagation",
            mode_label="Mode: Config Sync — apply once, sync everywhere",
            phases=[
                P(readout='<strong>Step 1.</strong> Platform team commits NetworkPolicy + Inference config to git.', move_to=(95, 120), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Fleet + Config Sync reconciles to all members.', move_to=(245, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Fan-out: native GKE us-central1...', move_to=(395, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> ...GKE-on-AWS eu-west...', move_to=(395, 115), duration_ms=900),
                P(readout='<strong>Step 5.</strong> ...GKE-on-VMware on-prem. All clusters reconcile.', move_to=(395, 175), duration_ms=900, pause_after_ms=1800),
            ],
        ),
        AnimationScene(
            mode_id="inference",
            button_label="▶ AI inference flow",
            mode_label="Mode: GKE Inference Gateway routes to vLLM with KV-cache locality",
            phases=[
                P(readout='<strong>Step 1.</strong> User asks Llama 3 70B follow-up question.', move_to=(95, 120), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Inference Gateway looks at conversation ID; routes to Pod with warm KV cache.', move_to=(545, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> vLLM Pod on A4 H200 generates first token in &lt; 500ms.', move_to=(680, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# G9 — WIF 401 troubleshooting playbook
SCENE_G9 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "Pod 401", "Storage denied", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "Cloud Status", "GCP-side OK", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "Audit Logs", "cluster recreated 2d ago", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "gcpdiag lint", "WIF mismatch flagged", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "Logs Explorer", "saved query for IAM audit", fill="#A04832", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "fix WIF Pool", "OIDC issuer URL", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Pod Running", "fixed", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_G9 = Animation(
    h2="WIF 401 — diagnose with Cloud Status → Audit Logs → gcpdiag → fix",
    intro="The standard GKE triage playbook applied to a WIF 401.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_G9,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a WIF 401 root-cause hunt.',
    scenes=[
        AnimationScene(
            mode_id="diag",
            button_label="▶ diagnose + fix",
            mode_label="Mode: WIF 401 → fed cred OIDC issuer mismatch → fix",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod returns 401 from Storage.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Check Cloud Status Dashboard first — GCP side healthy.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Audit Logs show: cluster recreated 2 days ago by IaC pipeline.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> gcpdiag lint flags: WIF Pool fed cred trusts old OIDC issuer URL.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Logs Explorer saved query confirms with the precise audit trail.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Update WIF Pool federated credential issuer to new cluster\'s OIDC URL.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 7.</strong> Pod\'s next call succeeds; postmortem updates IaC re-create runbook.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# G10 — capstone walk
SCENE_G10 = f'''        {_mode_label()}
        {_box(40, 90, 130, 50, "Phase A — base", "Autopilot + Cilium + WIF", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(200, 90, 130, 50, "Phase B — platform", "MCG + WIF + storage + obs", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(360, 90, 130, 50, "Phase C — ops + AI", "BinAuth + Flux + Inference GW", fill="#A04832", label_color="#FFFFFF")}
        {_box(520, 90, 110, 50, "Phase D — defence", "review + drill", fill="#E8B547", label_color="#5A4F45")}
        {_box(660, 90, 80, 50, "K-GKE-complete", "graduate", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_G10 = Animation(
    h2="The K-GKE capstone — A → B → C → D",
    intro="Four phases; each gates the next.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_G10,
    initial_packet_xy=(95, 115),
    initial_readout='<strong>Watching:</strong> the K-GKE capstone walk.',
    scenes=[
        AnimationScene(
            mode_id="walk",
            button_label="▶ end-to-end walk",
            mode_label="Mode: A → B → C → D → K-GKE-complete",
            phases=[
                P(readout='<strong>Phase A.</strong> Regional Autopilot + Cilium dataplane + private + WIF + Stable channel.', move_to=(105, 115), duration_ms=900),
                P(readout='<strong>Phase B.</strong> Multi-Cluster Gateway + WIF + storage + GMP + AMG + SLO Monitoring.', move_to=(265, 115), duration_ms=900),
                P(readout='<strong>Phase C.</strong> Binary Auth + Policy Controller + Config Sync + Backup for GKE + Inference Gateway + vLLM.', move_to=(425, 115), duration_ms=900),
                P(readout='<strong>Phase D.</strong> Architecture defended; live drill: node kill + IAM revoke + CTD finding + DR restore + 10× inference burst.', move_to=(575, 115), duration_ms=900),
                P(readout='<strong>K-GKE-complete.</strong> Terraform + arch doc + DR runbook + AI runbook + drill recording. Graduate.', move_to=(700, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


ANIMATIONS = {
    "01": ANIM_G1, "02": ANIM_G2, "03": ANIM_G3, "04": ANIM_G4, "05": ANIM_G5,
    "06": ANIM_G6, "07": ANIM_G7, "08": ANIM_G8, "09": ANIM_G9, "10": ANIM_G10,
}
