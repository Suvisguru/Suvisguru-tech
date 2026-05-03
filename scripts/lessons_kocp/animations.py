"""Per-module Section 6 animations for K-OCP O1-O13."""

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


# O1 — OCP architecture
SCENE_O1 = f'''        {_mode_label()}
        {_box(40, 70, 150, 90, "upstream K8s", "+ Red Hat additions", fill="#A04832", label_color="#FFFFFF")}
        {_box(220, 60, 200, 50, "Routes + SCCs + OAuth", "OCP-native", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(220, 130, 200, 50, "OperatorHub-everywhere", "OLM lifecycle", fill="#7AB3CC", label_color="#FBF1D6")}
        {_box(450, 70, 270, 90, "RHCOS + MCO + CVO", "immutable + machine config + version", fill="#3F4A5E", label_color="#FBF1D6")}'''
ANIM_O1 = Animation(
    h2="OCP architecture — what Red Hat adds + how the operators conduct it",
    intro="OCP = upstream K8s + Red Hat additions + RHCOS + MCO + CVO + OLM.",
    svg_viewbox="0 0 760 220", svg_body=SCENE_O1, initial_packet_xy=(115, 115),
    initial_readout='<strong>Watching:</strong> the OCP architecture overlay.',
    scenes=[AnimationScene(mode_id="walk", button_label="▶ OCP architecture overlay",
        mode_label="Mode: upstream K8s + Red Hat additions + RHCOS + MCO + CVO + OLM",
        phases=[
            P(readout='<strong>Step 1.</strong> Start with upstream K8s.', move_to=(115, 115), duration_ms=400),
            P(readout='<strong>Step 2.</strong> Red Hat adds Routes, SCCs, OAuth, OperatorHub-everywhere.', move_to=(320, 85), duration_ms=900),
            P(readout='<strong>Step 3.</strong> Add RHCOS (immutable node OS) + MCO (managing it) + CVO (orchestrating ClusterOperators).', move_to=(585, 115), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O2 — installation pipeline
SCENE_O2 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "install-config", "yaml", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "ignition configs", "bootstrap/master/worker", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 80, 130, 60, "bootstrap node", "temp apiserver + etcd", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "masters join", "real ctrl plane", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "cluster ready", "wait-for OK", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O2 = Animation(
    h2="OCP install dance — install-config → ignition → bootstrap → masters → ready",
    intro="The bootstrap dance.",
    svg_viewbox="0 0 760 220", svg_body=SCENE_O2, initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> the OCP install pipeline.',
    scenes=[AnimationScene(mode_id="install", button_label="▶ install pipeline",
        mode_label="Mode: install-config → ignition → bootstrap → masters → cluster ready",
        phases=[
            P(readout='<strong>Step 1.</strong> install-config.yaml + pull secret.', move_to=(95, 110), duration_ms=400),
            P(readout='<strong>Step 2.</strong> openshift-install creates manifests + ignition configs.', move_to=(245, 110), duration_ms=900),
            P(readout='<strong>Step 3.</strong> Bootstrap node boots; runs temp apiserver + etcd.', move_to=(405, 110), duration_ms=900),
            P(readout='<strong>Step 4.</strong> Masters join bootstrap; real apiserver + etcd quorum take over.', move_to=(555, 110), duration_ms=900),
            P(readout='<strong>Step 5.</strong> Bootstrap destroyed; workers join; cluster Available.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O3 — networking (request walks)
SCENE_O3 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "internet client", "GET /api", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "Router (HAProxy)", "Route TLS edge", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 90, 130, 60, "OVN-K dataplane", "Pod IP routing", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 90, 110, 60, "Pod (Project)", "200 OK", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 90, 100, 60, "← response", "via Route", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O3 = Animation(
    h2="A request walks — internet → Router (Route) → OVN-K → Pod → response",
    intro="OCP ingress + dataplane flow.",
    svg_viewbox="0 0 760 220", svg_body=SCENE_O3, initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> a request reach an OCP Pod via Route.',
    scenes=[AnimationScene(mode_id="walk", button_label="▶ ingress walk",
        mode_label="Mode: Router (HAProxy) + OVN-K + Pod",
        phases=[
            P(readout='<strong>Step 1.</strong> Internet client hits Route hostname.', move_to=(95, 120), duration_ms=400),
            P(readout='<strong>Step 2.</strong> Router (HAProxy in openshift-ingress) handles TLS edge termination.', move_to=(245, 120), duration_ms=900),
            P(readout='<strong>Step 3.</strong> OVN-K routes packet to Pod IP via OVS overlay.', move_to=(405, 120), duration_ms=900),
            P(readout='<strong>Step 4.</strong> Pod responds 200; Router returns to client.', move_to=(555, 120), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O4 — security pipeline
SCENE_O4 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "build CI", "image", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "ACR / Quay scan", "+ Cosign signing", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 130, 50, "Compliance Op", "CIS / NIST", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "SCC restricted-v2", "+ Policy Controller", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "RHACS runtime", "watch", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 90, 110, 60, "Pod Running", "secure", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 90, 100, 60, "Defender / SCC", "audit", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O4 = Animation(
    h2="A signed image walks from CI to a guarded Pod (RHACS-watched)",
    intro="Sign + scan → admission verify → SCC restricted-v2 → RHACS runtime.",
    svg_viewbox="0 0 760 240", svg_body=SCENE_O4, initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> a hardened deploy path.',
    scenes=[AnimationScene(mode_id="signed", button_label="▶ signed image lifecycle",
        mode_label="Mode: CI → scan + sign → Compliance + SCC + Policy verify → RHACS runtime",
        phases=[
            P(readout='<strong>Step 1.</strong> CI builds + Cosign-signs image; pushes to registry.', move_to=(245, 120), duration_ms=900),
            P(readout='<strong>Step 2.</strong> Compliance Operator scans the cluster CIS posture continuously.', move_to=(405, 55), duration_ms=900),
            P(readout='<strong>Step 3.</strong> SCC restricted-v2 + Policy Controller verify Pod at admission.', move_to=(405, 125), duration_ms=900),
            P(readout='<strong>Step 4.</strong> RHACS runtime watches behaviour; admission controller blocks if needed.', move_to=(405, 195), duration_ms=900),
            P(readout='<strong>Step 5.</strong> Pod Running. RHACS continues watching.', move_to=(555, 120), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O5 — OLM pipeline
SCENE_O5 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "Subscription", "+ channel + approval", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "InstallPlan", "deps + RBAC + CRDs", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 80, 130, 60, "manual approval", "(if Manual)", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "CSV", "Pending → Succeeded", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Operator Pod", "running", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O5 = Animation(
    h2="OLM install pipeline — Subscription → InstallPlan → CSV → Operator running",
    intro="The OLM dance.",
    svg_viewbox="0 0 760 220", svg_body=SCENE_O5, initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> OLM install pipeline.',
    scenes=[AnimationScene(mode_id="walk", button_label="▶ OLM pipeline",
        mode_label="Mode: Subscription → InstallPlan → CSV → Operator Running",
        phases=[
            P(readout='<strong>Step 1.</strong> User creates Subscription on stable channel.', move_to=(95, 110), duration_ms=400),
            P(readout='<strong>Step 2.</strong> OLM creates InstallPlan with deps + RBAC + CRDs.', move_to=(245, 110), duration_ms=900),
            P(readout='<strong>Step 3.</strong> If Manual approval: human runs <code>oc patch installplan ... approved:true</code>.', move_to=(405, 110), duration_ms=900),
            P(readout='<strong>Step 4.</strong> CSV phases: Pending → InstallReady → Installing → Succeeded.', move_to=(555, 110), duration_ms=900),
            P(readout='<strong>Step 5.</strong> Operator Pod running; reconciling its CRDs.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O6 — S2I + GitOps pipeline
SCENE_O6 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "git push", "source code", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "Pipelines (Tekton)", "S2I build", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 80, 130, 60, "ImageStream tag", "+ Cosign sign", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "GitOps (Argo CD)", "reconciles", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Deployment Live", "Route reachable", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O6 = Animation(
    h2="git push → Pipelines (S2I) → ImageStream → GitOps reconcile → Deployment live",
    intro="OCP-native CI/CD pipeline.",
    svg_viewbox="0 0 760 220", svg_body=SCENE_O6, initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> git push to live in OCP.',
    scenes=[AnimationScene(mode_id="walk", button_label="▶ git push to live",
        mode_label="Mode: Pipelines + S2I + ImageStream + Cosign + GitOps + Deployment",
        phases=[
            P(readout='<strong>Step 1.</strong> Developer pushes to feature branch.', move_to=(95, 110), duration_ms=400),
            P(readout='<strong>Step 2.</strong> Pipelines (Tekton) PipelineRun: S2I build from source.', move_to=(245, 110), duration_ms=900),
            P(readout='<strong>Step 3.</strong> Image pushed to internal registry; ImageStream tag updated; Cosign signs.', move_to=(405, 110), duration_ms=900),
            P(readout='<strong>Step 4.</strong> GitOps (Argo CD) detects manifest change; reconciles to cluster.', move_to=(555, 110), duration_ms=900),
            P(readout='<strong>Step 5.</strong> Deployment live; Route reachable; production traffic served.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O7 — PVC binding
SCENE_O7 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "PVC submitted", "RWO or RWX?", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "StorageClass picker", "ODF vs CSI", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "ODF CephRBD", "RWO block", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "ODF CephFS", "RWX shared FS", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "NooBaa S3 / Cloud CSI", "object / per-cloud", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "WaitForFirstConsumer", "AZ-aligned", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Pod Running", "PV mounted", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O7 = Animation(
    h2="A PVC picks the right storage backend (ODF, CSI, NooBaa)",
    intro="Same PVC; different access modes; different backends.",
    svg_viewbox="0 0 760 240", svg_body=SCENE_O7, initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> PVC binding for OCP storage.',
    scenes=[AnimationScene(mode_id="rwo", button_label="▶ RWO via ODF CephRBD",
        mode_label="Mode: RWO PVC → ODF CephRBD with WaitForFirstConsumer",
        phases=[
            P(readout='<strong>Step 1.</strong> Pod requests RWO 50 GiB block storage.', move_to=(95, 110), duration_ms=400),
            P(readout='<strong>Step 2.</strong> Default ODF StorageClass selected; WaitForFirstConsumer delays binding.', move_to=(245, 110), duration_ms=900),
            P(readout='<strong>Step 3.</strong> Scheduler picks node; ODF provisions CephRBD volume.', move_to=(405, 55), duration_ms=900),
            P(readout='<strong>Step 4.</strong> Mount succeeds; Pod Running.', move_to=(555, 110), duration_ms=900, pause_after_ms=2000),
        ]),
    AnimationScene(mode_id="rwx", button_label="▶ RWX via ODF CephFS",
        mode_label="Mode: RWX PVC → ODF CephFS shared filesystem",
        phases=[
            P(readout='<strong>Step 1.</strong> Two Pods need shared writable storage.', move_to=(95, 110), duration_ms=400),
            P(readout='<strong>Step 2.</strong> ODF CephFS StorageClass selected — only RWX option here.', move_to=(245, 110), duration_ms=900),
            P(readout='<strong>Step 3.</strong> Both Pods mount the same FS; concurrent read+write.', move_to=(405, 125), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O8 — OCP minor upgrade
SCENE_O8 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "v4.18 cluster", "EUS", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(180, 80, 110, 60, "ClusterVersion", "spec.desiredUpdate", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(310, 80, 110, 60, "CVO", "drives ClusterOperators", fill="#A04832", label_color="#FFFFFF")}
        {_box(440, 80, 110, 60, "MCO + MCP", "node roll PDB-aware", fill="#A04832", label_color="#FFFFFF")}
        {_box(570, 80, 110, 60, "smoke pass", "v4.20 cluster Ready", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(40, 160, 640, 50, "EUS-to-EUS skip-minor; etcd backup precondition; rollback via blue-green", "operating procedure", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O8 = Animation(
    h2="OCP minor upgrade — EUS-to-EUS via CVO + MCP roll",
    intro="EUS-to-EUS skip-minor with etcd backup + blue-green fallback.",
    svg_viewbox="0 0 760 230", svg_body=SCENE_O8, initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> EUS-to-EUS upgrade.',
    scenes=[AnimationScene(mode_id="upgrade", button_label="▶ EUS upgrade walk",
        mode_label="Mode: EUS → EUS upgrade orchestrated by CVO + MCO",
        phases=[
            P(readout='<strong>Step 1.</strong> Cluster on v4.18 EUS. Healthy.', move_to=(95, 110), duration_ms=400),
            P(readout='<strong>Step 2.</strong> Pre-flight: etcd backup + must-gather baseline + Insights review.', duration_ms=400, pause_after_ms=600),
            P(readout='<strong>Step 3.</strong> Switch ClusterVersion channel to eus-4.20; spec.desiredUpdate set.', move_to=(235, 110), duration_ms=900),
            P(readout='<strong>Step 4.</strong> CVO drives ~30 ClusterOperator upgrades in dependency order.', move_to=(365, 110), duration_ms=900),
            P(readout='<strong>Step 5.</strong> MCO + MachineConfigPool roll: drain (PDB-aware) + reboot per node.', move_to=(495, 110), duration_ms=900),
            P(readout='<strong>Step 6.</strong> Smoke tests pass. v4.20 EUS cluster Ready.', move_to=(625, 110), duration_ms=900),
            P(readout='<strong>Step 7.</strong> Rollback path: blue-green to a fresh cluster from etcd snapshot if needed.', move_to=(360, 185), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O9 — Virt + AI + Edge
SCENE_O9 = f'''        {_mode_label()}
        {_box(40, 80, 130, 60, "OCP cluster", "containers + VMs", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(200, 30, 130, 50, "MTV (vSphere)", "ingest VMs", fill="#A04832", label_color="#FFFFFF")}
        {_box(200, 100, 130, 50, "OpenShift Virt", "VirtualMachine CR", fill="#A04832", label_color="#FFFFFF")}
        {_box(200, 170, 130, 50, "live migration", "for drains", fill="#A04832", label_color="#FFFFFF")}
        {_box(360, 80, 130, 60, "OpenShift AI", "Jupyter + KServe + KFP", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(510, 80, 130, 60, "SNO + MicroShift", "edge sites", fill="#7AB3CC", label_color="#FBF1D6")}
        {_box(660, 80, 70, 60, "RHACM", "fleet", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O9 = Animation(
    h2="OCP Virt + AI + Edge — three specialty production lines",
    intro="VMs + AI + Edge alongside containers in one OCP.",
    svg_viewbox="0 0 760 240", svg_body=SCENE_O9, initial_packet_xy=(105, 110),
    initial_readout='<strong>Watching:</strong> the Special Castings Wing.',
    scenes=[AnimationScene(mode_id="walk", button_label="▶ Virt + AI + Edge",
        mode_label="Mode: VirtualMachine + KServe + SNO + RHACM federation",
        phases=[
            P(readout='<strong>Step 1.</strong> OCP cluster runs containers + VMs side by side.', move_to=(105, 110), duration_ms=400),
            P(readout='<strong>Step 2.</strong> MTV ingests VMs from vSphere as VirtualMachine CRs.', move_to=(265, 55), duration_ms=900),
            P(readout='<strong>Step 3.</strong> Live migration moves VMs between nodes for drains.', move_to=(265, 195), duration_ms=900),
            P(readout='<strong>Step 4.</strong> OpenShift AI: Jupyter notebooks + KServe model serving + Kubeflow Pipelines.', move_to=(425, 110), duration_ms=900),
            P(readout='<strong>Step 5.</strong> Edge: SNO at retail / cell sites; MicroShift at IoT; RHACM federates.', move_to=(575, 110), duration_ms=900),
            P(readout='<strong>Step 6.</strong> RHACM hub manages all foundries from one pane.', move_to=(695, 110), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O10 — RHACM federation
SCENE_O10 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "RHACM hub", "MCE", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "PolicySet", "fleet-wide", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 110, 50, "OCP us-east", "Compliant", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 90, 110, 50, "OCP eu-west", "Compliant", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 150, 110, 50, "EKS asia", "Compliant", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(480, 90, 130, 60, "ApplicationSet", "deploys to fleet", fill="#A04832", label_color="#FFFFFF")}
        {_box(630, 90, 100, 60, "Observability", "Thanos hub", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O10 = Animation(
    h2="RHACM hub federates 30 clusters — Policy + ApplicationSet + Observability",
    intro="One hub; many spokes; one governance plane.",
    svg_viewbox="0 0 760 230", svg_body=SCENE_O10, initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> RHACM federation.',
    scenes=[AnimationScene(mode_id="walk", button_label="▶ federation",
        mode_label="Mode: PolicySet + ApplicationSet + ObservabilityAddon across fleet",
        phases=[
            P(readout='<strong>Step 1.</strong> RHACM hub + multicluster-engine.', move_to=(95, 120), duration_ms=400),
            P(readout='<strong>Step 2.</strong> PolicySet enforces NetworkPolicy + RHACS Sensor + OADP across fleet.', move_to=(245, 120), duration_ms=900),
            P(readout='<strong>Step 3.</strong> Spokes fan out: us-east...', move_to=(395, 55), duration_ms=900),
            P(readout='<strong>Step 4.</strong> ...eu-west...', move_to=(395, 115), duration_ms=900),
            P(readout='<strong>Step 5.</strong> ...asia (EKS via klusterlet). All Compliant.', move_to=(395, 175), duration_ms=900),
            P(readout='<strong>Step 6.</strong> ApplicationSet deploys baseline platform services to all clusters.', move_to=(545, 120), duration_ms=900),
            P(readout='<strong>Step 7.</strong> ObservabilityAddon aggregates fleet metrics on the hub.', move_to=(680, 120), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O11 — observability signal flow
SCENE_O11 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "Pod", "emits signals", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "Vector / OTel", "log/trace ship", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 130, 50, "Cluster Monitoring", "Prom + Thanos", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "Loki", "logs + LogQL", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "Tempo", "traces + TraceQL", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "OCP console", "joined view", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Alertmanager", "burn-rate alert", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O11 = Animation(
    h2="A signal travels from Pod to PagerDuty",
    intro="Three pipes joined in OCP console; SLO burn-rate alert.",
    svg_viewbox="0 0 760 240", svg_body=SCENE_O11, initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a metric → Cluster Monitoring → alert.',
    scenes=[AnimationScene(mode_id="trace", button_label="▶ signal flow",
        mode_label="Mode: Cluster Monitoring + Logging + Tracing → Alertmanager",
        phases=[
            P(readout='<strong>Step 1.</strong> Pod emits Prometheus metric, structured log, OTel span.', move_to=(95, 110), duration_ms=400),
            P(readout='<strong>Step 2.</strong> Vector ships logs; OTel collector ships traces.', move_to=(245, 110), duration_ms=900),
            P(readout='<strong>Step 3.</strong> Metric → Cluster Monitoring (Prom + Thanos).', move_to=(405, 55), duration_ms=900),
            P(readout='<strong>Step 4.</strong> Log → Loki; queryable via LogQL.', move_to=(405, 125), duration_ms=900),
            P(readout='<strong>Step 5.</strong> Trace → Tempo; queryable via TraceQL.', move_to=(405, 195), duration_ms=900),
            P(readout='<strong>Step 6.</strong> OCP console joins all three; SLO burn-rate panel turns red.', move_to=(555, 110), duration_ms=900),
            P(readout='<strong>Step 7.</strong> Alertmanager fires; PagerDuty pages on-call.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O12 — troubleshooting cascade
SCENE_O12 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "outage", "cascading", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "Insights Advisor", "known issues", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "oc get co", "CO degraded", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "oc get clusterversion", "CVO state", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "oc get mcp", "MCP roll state", fill="#A04832", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "must-gather", "diagnostic", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(640, 80, 100, 60, "fix + recover", "RTO met", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O12 = Animation(
    h2="OCP triage playbook — Insights → CO → CVO → MCP → must-gather → fix",
    intro="Standard playbook for cascading failures.",
    svg_viewbox="0 0 760 240", svg_body=SCENE_O12, initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> the OCP triage ladder.',
    scenes=[AnimationScene(mode_id="triage", button_label="▶ triage walk",
        mode_label="Mode: triage cascading failure",
        phases=[
            P(readout='<strong>Step 1.</strong> Cascading outage detected.', move_to=(95, 110), duration_ms=400),
            P(readout='<strong>Step 2.</strong> Check Insights Advisor for known issues.', move_to=(245, 110), duration_ms=900),
            P(readout='<strong>Step 3.</strong> oc get co — find Degraded ClusterOperators.', move_to=(405, 55), duration_ms=900),
            P(readout='<strong>Step 4.</strong> oc get clusterversion — CVO state.', move_to=(405, 125), duration_ms=900),
            P(readout='<strong>Step 5.</strong> oc get mcp — node-roll state.', move_to=(405, 195), duration_ms=900),
            P(readout='<strong>Step 6.</strong> oc adm must-gather — bundle for postmortem + Red Hat case.', move_to=(555, 110), duration_ms=900),
            P(readout='<strong>Step 7.</strong> Identified root cause; applied fix; cluster recovered within RTO.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
        ])],
)


# O13 — capstone walk
SCENE_O13 = f'''        {_mode_label()}
        {_box(40, 90, 130, 50, "Phase A — base", "IPI + EUS + private + OVN-K", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(200, 90, 140, 50, "Phase B — platform", "ODF + SCC + RHACS + obs", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(370, 90, 140, 50, "Phase C — apps + Virt", "Pipelines + GitOps + Virt + DR", fill="#A04832", label_color="#FFFFFF")}
        {_box(540, 90, 110, 50, "Phase D — fed/drill", "RHACM + drill", fill="#E8B547", label_color="#5A4F45")}
        {_box(680, 90, 80, 50, "K-OCP-complete", "graduate", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''
ANIM_O13 = Animation(
    h2="The K-OCP capstone walk — A → B → C → D",
    intro="Four phases; each gates the next.",
    svg_viewbox="0 0 760 200", svg_body=SCENE_O13, initial_packet_xy=(105, 115),
    initial_readout='<strong>Watching:</strong> the K-OCP capstone walk.',
    scenes=[AnimationScene(mode_id="walk", button_label="▶ end-to-end walk",
        mode_label="Mode: A → B → C → D → K-OCP-complete",
        phases=[
            P(readout='<strong>Phase A.</strong> IPI base + EUS + private + OVN-K + 3+5 nodes + ODF storage nodes.', move_to=(105, 115), duration_ms=900),
            P(readout='<strong>Phase B.</strong> ODF + SCCs + RHACS + Cluster Monitoring + Logging + Tracing + NetObserv.', move_to=(270, 115), duration_ms=900),
            P(readout='<strong>Phase C.</strong> Pipelines + GitOps + OpenShift Virtualization (MTV) + OADP + disconnected mirror.', move_to=(440, 115), duration_ms=900),
            P(readout='<strong>Phase D.</strong> RHACM federation; live drill: node kill + RBAC revoke + CTD + DR + 10× burst + etcd loss.', move_to=(595, 115), duration_ms=900),
            P(readout='<strong>K-OCP-complete.</strong> Install configs + arch doc + DR runbook + AI/Virt runbook + must-gather pack + drill recording.', move_to=(720, 115), duration_ms=900, pause_after_ms=2400),
        ])],
)


ANIMATIONS = {
    "01": ANIM_O1, "02": ANIM_O2, "03": ANIM_O3, "04": ANIM_O4, "05": ANIM_O5,
    "06": ANIM_O6, "07": ANIM_O7, "08": ANIM_O8, "09": ANIM_O9, "10": ANIM_O10,
    "11": ANIM_O11, "12": ANIM_O12, "13": ANIM_O13,
}
