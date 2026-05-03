"""Per-lesson Section 6 animations for L18-L44.

Each entry in ANIMATIONS maps a lesson number to an `Animation` describing:
- the static SVG scene (boxes + labels with element ids)
- 2-3 modes (buttons), each a sequence of phases
- per-phase: readout HTML, packet motion, optional element-text/attribute swaps

The generator (k8s_lesson_generator.py) wires the data into a single
generic JS animation runner. Auto-loops; mode buttons restart with the
chosen scene.

Convention: each scene's first phase moves the packet from the initial
position to the first waypoint; subsequent phases continue from where
the previous phase ended. The packet hides + resets when the loop
restarts.
"""

from _helpers import Animation, AnimationScene, AnimationPhase as P


def _box(x, y, w, h, label, sub=None, fill="#FFFFFF", stroke="#3F4A5E", label_color="#3F4A5E"):
    sub_html = f'<text x="{x+w//2}" y="{y+38}" text-anchor="middle" font-size="9" fill="#6B6058">{sub}</text>' if sub else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        f'<text x="{x+w//2}" y="{y+22}" text-anchor="middle" font-size="11" font-weight="700" fill="{label_color}">{label}</text>'
        f'{sub_html}'
    )


def _label(x, y, text, size=10, color="#5A4F45", weight=400):
    fw = f' font-weight="{weight}"' if weight != 400 else ""
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{color}"{fw}>{text}</text>'


def _arrow(x1, y1, x2, y2, color="#9D9389", dashed=True):
    da = ' stroke-dasharray="3,3"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.2"{da}/>'


def _mode_label(x=380, y=22):
    # Generator wires #anim-mode-label per scene; the element is required.
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="13" font-weight="600" fill="#3F4A5E" id="anim-mode-label">Mode</text>'


# ===================================================================
# L18 — Storage Pt 1: PV / PVC / StorageClass
# ===================================================================
SCENE_L18 = f'''        {_mode_label()}
        {_box(40, 70, 130, 70, "PVC", "user request", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(220, 70, 130, 70, "StorageClass", "the recipe", fill="#ECEFF5", stroke="#3F4A5E")}
        {_box(400, 70, 130, 70, "Provisioner", "the CSI driver", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(580, 70, 140, 70, "PV", "the actual disk", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_label(105, 195, "Pod", 10, "#3F4A5E", 700)}
        {_label(105, 210, '"I need 10Gi"', 9, "#6B6058")}
        {_arrow(170, 105, 220, 105)}{_arrow(350, 105, 400, 105)}{_arrow(530, 105, 580, 105)}'''

ANIM_L18 = Animation(
    h2="Watch a PVC bind to a PV — three reclaim outcomes",
    intro="A Pod requests 10Gi via a PVC. The StorageClass tells the provisioner how to make a PV. Then the PVC is deleted — three different reclaim policies, three outcomes.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_L18,
    initial_packet_xy=(105, 105),
    initial_readout='<strong>Watching:</strong> a Pod\'s PVC arrives at the StorageClass; the provisioner creates a PV; PV binds to PVC. Then watch what happens when the PVC is deleted.',
    scenes=[
        AnimationScene(
            mode_id="delete",
            button_label="▶ reclaim: Delete (default)",
            mode_label="Mode: reclaimPolicy=Delete — disk removed with PVC",
            phases=[
                P(readout='<strong>Step 1.</strong> PVC submitted; <code>storageClassName: fast-ssd</code>.', move_to=(285, 105), duration_ms=900),
                P(readout='<strong>Step 2.</strong> StorageClass invokes the provisioner.', move_to=(465, 105), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Provisioner creates a PV; binds to PVC. Pod mounts <code>/data</code>.', move_to=(650, 105), duration_ms=900),
                P(readout='<strong>Step 4.</strong> User <code>kubectl delete pvc</code>. Reclaim=Delete → PV + underlying disk gone.', move_to=(650, 200), duration_ms=900, pause_after_ms=2200,
                  set_text=[("anim-mode-label", "Mode: reclaimPolicy=Delete — disk removed with PVC")]),
            ],
        ),
        AnimationScene(
            mode_id="retain",
            button_label="▶ reclaim: Retain",
            mode_label="Mode: reclaimPolicy=Retain — PV kept; data preserved",
            phases=[
                P(readout='<strong>Step 1.</strong> PVC submitted with <code>storageClassName: prod-retain</code>.', move_to=(285, 105), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Provisioner creates PV bound to the PVC.', move_to=(650, 105), duration_ms=1100),
                P(readout='<strong>Step 3.</strong> User deletes PVC. PV moves to <code>Released</code> state — data still there.', duration_ms=400, pause_after_ms=1800,
                  set_text=[("anim-mode-label", "Mode: reclaimPolicy=Retain — PV kept in Released state")]),
                P(readout='<strong>Step 4.</strong> A human reviews + deletes the PV manually when ready. Safer for production data.', duration_ms=400, pause_after_ms=2200),
            ],
        ),
        AnimationScene(
            mode_id="static",
            button_label="▶ static provisioning",
            mode_label="Mode: static provisioning — admin pre-creates PVs",
            phases=[
                P(readout='<strong>Step 1.</strong> Admin pre-creates a PV by hand (NFS export, pre-existing SAN volume).', move_to=(650, 105), duration_ms=900,
                  set_text=[("anim-mode-label", "Mode: static — admin pre-creates PV")]),
                P(readout='<strong>Step 2.</strong> Later, a PVC is submitted that matches the existing PV\'s capacity + access mode.', move_to=(105, 105), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Controller binds the PVC to the existing PV. No provisioner involved.', move_to=(650, 105), duration_ms=1100, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L19 — Storage Pt 2: CSI / Snapshots / VolumeAttributesClass
# ===================================================================
SCENE_L19 = f'''        {_mode_label()}
        {_box(40, 70, 120, 60, "PVC: db-data", "100Gi gp3", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(220, 70, 200, 60, "CSI Driver", "EBS", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(480, 70, 240, 60, "Cloud Storage (EBS)", "100Gi · 3000 IOPS", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(60, 170, 180, 60, "VolumeSnapshot", "point-in-time copy", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(280, 170, 180, 60, "Cloned PVC", "dataSource=PVC", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(500, 170, 220, 60, "VolumeAttributesClass", "premium-burst · 8000 IOPS", fill="#ECEFF5", stroke="#3F4A5E")}
        {_arrow(160, 100, 220, 100)}{_arrow(420, 100, 480, 100)}'''

ANIM_L19 = Animation(
    h2="Four things a CSI driver can do — pick a mode",
    intro="The same EBS-backed PVC can be snapshotted, cloned, expanded, or live-tuned. Each is a CSI driver call from the K8s API.",
    svg_viewbox="0 0 760 250",
    svg_body=SCENE_L19,
    initial_packet_xy=(100, 100),
    initial_readout='<strong>Watching:</strong> a PVC bound to an EBS-backed PV. Click a mode to see what the CSI driver does.',
    scenes=[
        AnimationScene(
            mode_id="snapshot",
            button_label="▶ VolumeSnapshot",
            mode_label="Mode: VolumeSnapshot — point-in-time copy",
            phases=[
                P(readout='<strong>Step 1.</strong> Apply a <code>VolumeSnapshot</code> referencing the PVC.', move_to=(320, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> CSI driver calls <code>CreateSnapshot</code> on EBS — instant block-level snapshot.', move_to=(600, 100), duration_ms=1000),
                P(readout='<strong>Step 3.</strong> Snapshot stored as a <code>VolumeSnapshotContent</code>; survives PVC deletion.', move_to=(150, 200), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="clone",
            button_label="▶ Clone (dataSource: PVC)",
            mode_label="Mode: Clone — fast-path PVC copy",
            phases=[
                P(readout='<strong>Step 1.</strong> Apply a new PVC with <code>dataSource: existing-PVC</code>.', move_to=(370, 200), duration_ms=900),
                P(readout='<strong>Step 2.</strong> CSI driver does block-level copy-on-write — much faster than <code>kubectl cp</code>.', move_to=(320, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Cloned PVC ready in seconds. Same StorageClass, same namespace, independent disk.', move_to=(370, 200), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="vac",
            button_label="▶ VolumeAttributesClass (live re-tune)",
            mode_label="Mode: VolumeAttributesClass — change perf live (1.34 GA)",
            phases=[
                P(readout='<strong>Step 1.</strong> Patch PVC: <code>volumeAttributesClassName: premium-burst</code>.', move_to=(610, 200), duration_ms=900),
                P(readout='<strong>Step 2.</strong> CSI driver calls EBS <code>ModifyVolume</code> to bump IOPS → 8000.', move_to=(320, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Disk is re-tuned in place. No detach. No Pod restart. ~30 seconds.', move_to=(600, 100), duration_ms=1000,
                  set_text=[("anim-mode-label", "Mode: VolumeAttributesClass — live performance change")]),
                P(readout='<strong>Done.</strong> After the burst, patch back to the standard tier. Old playbook would have meant a failover.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L20 — Configuration & Secrets
# ===================================================================
SCENE_L20 = f'''        {_mode_label()}
        {_box(40, 70, 120, 80, "Source", "where the value lives", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(230, 70, 160, 80, "K8s API", "ConfigMap or Secret", fill="#ECEFF5", stroke="#3F4A5E")}
        {_box(450, 70, 130, 80, "kubelet", "projects to Pod", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(620, 70, 120, 80, "Pod", "/data or env", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_arrow(160, 110, 230, 110)}{_arrow(390, 110, 450, 110)}{_arrow(580, 110, 620, 110)}'''

ANIM_L20 = Animation(
    h2="Three ways a Pod gets its config — pick a mode",
    intro="ConfigMap as a file, Secret as an env var, or a credential synced in from Vault via External Secrets Operator. Same Pod, three sources.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L20,
    initial_packet_xy=(100, 110),
    initial_readout='<strong>Watching:</strong> the journey from source-of-truth to Pod. Pick a mode.',
    scenes=[
        AnimationScene(
            mode_id="cm-file",
            button_label="▶ ConfigMap as file",
            mode_label="Mode: ConfigMap mounted as a volume",
            phases=[
                P(readout='<strong>Step 1.</strong> <code>kubectl apply -f cm.yaml</code> — ConfigMap stored in etcd as plain UTF-8.', move_to=(310, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Kubelet sees the Pod\'s <code>volumes: configMap</code> mount.', move_to=(515, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Each key becomes a file under the mount. Updates auto-resync within ~60s. App watches with inotify.', move_to=(680, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="secret-env",
            button_label="▶ Secret as env var",
            mode_label="Mode: Secret as env var (read once at start)",
            phases=[
                P(readout='<strong>Step 1.</strong> Secret stored — base64-encoded in etcd. <em>Encrypted at rest only if KMS is configured.</em>', move_to=(310, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Kubelet reads via API; injects as env var on Pod start.', move_to=(515, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> App reads <code>os.environ["DB_PASSWORD"]</code> once. <em>Rotation requires Pod restart</em>.', move_to=(680, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="eso",
            button_label="▶ External Secrets Operator (Vault)",
            mode_label="Mode: ESO syncs from Vault to a K8s Secret",
            initial_set_text=[("anim-source-label", "Vault")],
            phases=[
                P(readout='<strong>Step 1.</strong> Source of truth is HashiCorp Vault. <code>ExternalSecret</code> CRD points at a Vault path.', move_to=(100, 110), duration_ms=400, pause_after_ms=600),
                P(readout='<strong>Step 2.</strong> ESO controller polls Vault on the refresh interval (default 1h).', move_to=(310, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> ESO writes a K8s Secret. Kubelet projects it into the Pod normally.', move_to=(515, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Vault rotation propagates: ESO refresh → Secret update → file watch → live reload.', move_to=(680, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L21 — ServiceAccounts & Certificates
# ===================================================================
SCENE_L21 = f'''        {_mode_label()}
        {_box(40, 70, 120, 80, "Pod", "ServiceAccount=app-x", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(220, 70, 160, 80, "TokenRequest API", "kubelet asks", fill="#ECEFF5", stroke="#3F4A5E")}
        {_box(440, 70, 160, 80, "Signed JWT", "1h · audience-bound", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(640, 70, 100, 80, "API Server", "verifies", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_arrow(160, 110, 220, 110)}{_arrow(380, 110, 440, 110)}{_arrow(600, 110, 640, 110)}'''

ANIM_L21 = Animation(
    h2="Watch a Pod prove its identity — modern vs legacy tokens",
    intro="Modern: kubelet mints a short-lived audience-bound JWT every hour. Legacy: a long-lived Secret token sat in etcd forever.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L21,
    initial_packet_xy=(100, 110),
    initial_readout='<strong>Watching:</strong> a Pod authenticating to the API server. Pick a token model.',
    scenes=[
        AnimationScene(
            mode_id="bound",
            button_label="▶ Bound projected token (modern)",
            mode_label="Mode: bound projected token (1h · audience-bound · refreshed)",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod spawns with <code>serviceAccountName: app-x</code>.', move_to=(300, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Kubelet calls TokenRequest API; receives a short-lived JWT bound to Pod UID.', move_to=(520, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod presents JWT as Bearer token; API server verifies signature + claims.', move_to=(690, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> At ~50 min, kubelet refreshes. Leaked JWT useful for at most an hour.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="legacy",
            button_label="▶ Legacy SA token Secret",
            mode_label="Mode: legacy SA token (long-lived; pre-1.24)",
            phases=[
                P(readout='<strong>Step 1.</strong> K8s pre-1.24 auto-created a Secret per SA holding a token that <em>never expired</em>.', move_to=(300, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Pod mounted the Secret; presented its token.', move_to=(520, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Leaked token = permanent compromise. Modern clusters disable this.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="irsa",
            button_label="▶ IRSA / Workload Identity",
            mode_label="Mode: IRSA — exchange JWT for cloud creds (no static AWS keys)",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod\'s projected JWT carries audience <code>sts.amazonaws.com</code>.', move_to=(520, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Pod calls AWS STS <code>AssumeRoleWithWebIdentity</code> presenting the JWT.', move_to=(690, 110), duration_ms=900,
                  set_text=[("anim-mode-label", "Mode: IRSA — STS verifies via cluster's OIDC discovery endpoint")]),
                P(readout='<strong>Step 3.</strong> STS verifies via cluster\'s OIDC discovery endpoint, returns AWS creds. No static access key anywhere.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L22 — Scheduling Pt 1
# ===================================================================
SCENE_L22 = f'''        {_mode_label()}
        {_box(40, 70, 110, 80, "Pending Pod", "needs a node", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(200, 60, 100, 50, "node-A", "zone us-1a", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(200, 130, 100, 50, "node-B", "zone us-1b", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(330, 60, 100, 50, "node-C", "zone us-1a", fill="#9D9389", stroke="#A04832", label_color="#FBF1D6")}
        {_box(330, 130, 100, 50, "node-D", "zone us-1b", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(460, 60, 100, 50, "node-E", "zone us-1c", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(460, 130, 100, 50, "node-F", "zone us-1c", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(590, 90, 150, 60, "Scheduler", "filter → score → bind", fill="#3F4A5E", label_color="#FBF1D6")}'''

ANIM_L22 = Animation(
    h2="Watch the scheduler land a Pod — three placement modes",
    intro="Six nodes across three zones; node-C is tainted. Watch how nodeSelector, taints, and topology spread change the outcome.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L22,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a Pending Pod looking for a home. Each mode tells the scheduler different rules.',
    scenes=[
        AnimationScene(
            mode_id="nodeselector",
            button_label="▶ nodeSelector: zone=us-1a",
            mode_label="Mode: nodeSelector restricts to zone us-1a only",
            phases=[
                P(readout='<strong>Step 1.</strong> Scheduler\'s filter phase: keep only nodes labelled zone=us-1a.', move_to=(665, 120), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Candidates: node-A and node-C. node-C has a NoSchedule taint → excluded.', move_to=(250, 85), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod bound to node-A. <code>spec.nodeName: node-A</code>.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="taint",
            button_label="▶ Taint + toleration",
            mode_label="Mode: Pod tolerates the taint on node-C",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod adds <code>tolerations: [key=gpu, value=true]</code> matching node-C\'s taint.', move_to=(665, 120), duration_ms=900),
                P(readout='<strong>Step 2.</strong> node-C is no longer excluded from filter. Now in the candidate set.', move_to=(380, 85), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Score phase picks node-C (least-allocated). Pod lands on the dedicated GPU node.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="spread",
            button_label="▶ topologySpread maxSkew=1",
            mode_label="Mode: topology spread enforces zone balance",
            phases=[
                P(readout='<strong>Step 1.</strong> 6 replicas in flight. Scheduler aims for 2-2-2 across zones.', move_to=(665, 120), duration_ms=900),
                P(readout='<strong>Step 2.</strong> us-1c has 0 Pods so far → highest score for node-E.', move_to=(510, 85), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod placed in us-1c. Skew across zones stays ≤ 1.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L23 — Scheduling Pt 2
# ===================================================================
SCENE_L23 = f'''        {_mode_label()}
        {_box(40, 60, 110, 50, "P=10 batch", "low priority", fill="#9D9389", label_color="#FFFFFF")}
        {_box(40, 120, 110, 50, "P=1000 critical", "high priority", fill="#A04832", label_color="#FFFFFF")}
        {_box(200, 60, 130, 110, "Cluster: full", "no fit", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(370, 60, 160, 50, "Step 1: identify victim", "lowest priority", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(370, 120, 160, 50, "Step 2: evict gracefully", "30s grace", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(560, 90, 180, 60, "High-priority Pod placed", "running", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_L23 = Animation(
    h2="Preemption, DRA, NUMA — three advanced scheduling primitives",
    intro="When the cluster is full, who gets evicted? When a Pod needs an H100 with 80GB, how does the scheduler match it? When microseconds matter, how does NUMA pinning help?",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L23,
    initial_packet_xy=(95, 145),
    initial_readout='<strong>Watching:</strong> a critical Pod arrives at a full cluster. Pick a mode.',
    scenes=[
        AnimationScene(
            mode_id="preempt",
            button_label="▶ Preemption (priority)",
            mode_label="Mode: PriorityClass + preemption",
            phases=[
                P(readout='<strong>Step 1.</strong> P=1000 Pod wants to schedule; cluster has no fit.', move_to=(265, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Scheduler identifies a P=10 batch Pod whose eviction would free room.', move_to=(450, 85), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Batch Pod evicted gracefully (30s grace period for cleanup).', move_to=(450, 145), duration_ms=900),
                P(readout='<strong>Step 4.</strong> P=1000 Pod scheduled. Total time-to-place: ~30s, not Pending forever.', move_to=(650, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="dra",
            button_label="▶ DRA (GPU claim)",
            mode_label="Mode: DRA — match by attribute, not name",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod declares a <code>ResourceClaim</code>: H100 with ≥ 80 GiB, CUDA 12.4.', move_to=(265, 115), duration_ms=900,
                  set_text=[("anim-mode-label", "Mode: DRA — Dynamic Resource Allocation (GA 1.34)")]),
                P(readout='<strong>Step 2.</strong> Scheduler reads <code>ResourceSlice</code> per node; matches by attribute selectors.', move_to=(450, 85), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod placed on a node with a matching MIG slice. Sharing without overprovisioning.', move_to=(650, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="numa",
            button_label="▶ Topology Manager (NUMA)",
            mode_label="Mode: single-numa-node — CPU+RAM+device co-located",
            phases=[
                P(readout='<strong>Step 1.</strong> Latency-sensitive Pod requests integer CPU + Guaranteed QoS.', move_to=(265, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Topology Manager refuses any node where CPU/memory/device split across NUMA nodes.', move_to=(450, 145), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod placed on a node where everything fits one NUMA. P99 latency drops.', move_to=(650, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L24 — Networking Foundations & CNI
# ===================================================================
SCENE_L24 = f'''        {_mode_label()}
        {_box(30, 60, 200, 110, "node-A", "kernel namespaces", fill="#FFFFFF", stroke="#5A4F45")}
        <rect x="50" y="100" width="60" height="40" rx="4" fill="#5A9F7A"/><text x="80" y="120" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">pod-1</text>
        <rect x="120" y="100" width="60" height="40" rx="4" fill="#5A9F7A"/><text x="150" y="120" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">pod-2</text>
        <rect x="50" y="148" width="130" height="14" rx="2" fill="#3F4A5E"/><text x="115" y="158" text-anchor="middle" font-size="8" fill="#FBF1D6" font-weight="700">cni0 bridge</text>
        {_box(530, 60, 200, 110, "node-B", "", fill="#FFFFFF", stroke="#5A4F45")}
        <rect x="550" y="100" width="60" height="40" rx="4" fill="#5A9F7A"/><text x="580" y="120" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">pod-3</text>
        <rect x="620" y="100" width="60" height="40" rx="4" fill="#5A9F7A"/><text x="650" y="120" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">pod-4</text>
        <rect x="550" y="148" width="130" height="14" rx="2" fill="#3F4A5E"/><text x="615" y="158" text-anchor="middle" font-size="8" fill="#FBF1D6" font-weight="700">cni0 bridge</text>
        {_box(280, 90, 200, 50, "Inter-node path", "encap or native routing", fill="#ECEFF5", stroke="#3F4A5E")}'''

ANIM_L24 = Animation(
    h2="Same-node vs cross-node Pod traffic — three CNI modes",
    intro="Same-node traffic crosses the bridge; cross-node traffic crosses the inter-node path. The CNI plugin chooses how that path works.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L24,
    initial_packet_xy=(80, 120),
    initial_readout='<strong>Watching:</strong> a packet leaving pod-1. Pick its destination + the CNI mode.',
    scenes=[
        AnimationScene(
            mode_id="samenode",
            button_label="▶ pod-1 → pod-2 (same node)",
            mode_label="Mode: same-node — bridge only",
            phases=[
                P(readout='<strong>Step 1.</strong> pod-1 sends a packet via its <code>eth0</code> (one end of a veth pair).', move_to=(80, 155), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Other end of the veth is on the host bridge. Packet hits cni0.', move_to=(150, 155), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Bridge forwards to pod-2\'s host-side veth. No encapsulation, no routing table lookup.', move_to=(150, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="vxlan",
            button_label="▶ pod-1 → pod-3 (VXLAN encap)",
            mode_label="Mode: cross-node, VXLAN encapsulation",
            phases=[
                P(readout='<strong>Step 1.</strong> pod-1 sends packet to pod-3\'s IP (10.1.2.4 — in node-B\'s CIDR).', move_to=(80, 155), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Routing table on node-A says: pod-3 is via the VXLAN tunnel to node-B.', move_to=(380, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Packet wrapped in a 50-byte VXLAN/UDP header — adds overhead but works on any underlay.', move_to=(615, 155), duration_ms=900),
                P(readout='<strong>Step 4.</strong> node-B\'s tunnel endpoint unwraps. Packet enters node-B\'s bridge → pod-3.', move_to=(580, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="native",
            button_label="▶ pod-1 → pod-3 (native routing)",
            mode_label="Mode: cross-node, native BGP routing",
            phases=[
                P(readout='<strong>Step 1.</strong> Calico/Cilium BGP-peers with the top-of-rack switch. Pod CIDRs are routable.', move_to=(380, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Packet leaves node-A unwrapped — full underlay MTU available.', move_to=(615, 155), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Packet routed directly to node-B\'s pod CIDR. No encap overhead. Faster.', move_to=(580, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L25 — Gateway API
# ===================================================================
SCENE_L25 = f'''        {_mode_label()}
        {_box(40, 60, 100, 80, "user", "external request", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(180, 60, 180, 80, "Gateway", ":443 listener · TLS", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(400, 30, 170, 60, "HTTPRoute /api", "→ svc-api", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(400, 100, 170, 60, "HTTPRoute /shop", "→ svc-shop", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(610, 30, 130, 60, "svc-api", "Pod set A", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(610, 100, 130, 60, "svc-shop", "Pod set B", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_L25 = Animation(
    h2="Gateway API request flow — host/path routing + canary split",
    intro="The Gateway terminates TLS; HTTPRoutes match by host + path; backendRefs route to Services with optional weights.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_L25,
    initial_packet_xy=(90, 100),
    initial_readout='<strong>Watching:</strong> external requests landing on the Gateway, then HTTPRoute matchers picking a backend.',
    scenes=[
        AnimationScene(
            mode_id="api",
            button_label="▶ /api → svc-api",
            mode_label="Mode: GET /api — first HTTPRoute matches",
            phases=[
                P(readout='<strong>Step 1.</strong> User requests <code>https://acme.com/api/v1/users</code>.', move_to=(270, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Gateway terminates TLS, looks up matching HTTPRoute by host+path.', move_to=(485, 60), duration_ms=900),
                P(readout='<strong>Step 3.</strong> First HTTPRoute matches /api/* → backendRef svc-api.', move_to=(675, 60), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="shop",
            button_label="▶ /shop → svc-shop",
            mode_label="Mode: GET /shop — second HTTPRoute matches",
            phases=[
                P(readout='<strong>Step 1.</strong> User requests <code>https://acme.com/shop/cart</code>.', move_to=(270, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Gateway routes by path; /shop matches the second HTTPRoute.', move_to=(485, 130), duration_ms=900),
                P(readout='<strong>Step 3.</strong> backendRef points at svc-shop. Different team, same Gateway.', move_to=(675, 130), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="canary",
            button_label="▶ canary 90/10 split",
            mode_label="Mode: HTTPRoute backendRef weights 90/10 (canary)",
            phases=[
                P(readout='<strong>Step 1.</strong> /api HTTPRoute has 2 backendRefs: svc-api (weight 90) + svc-api-v2 (weight 10).', move_to=(485, 60), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Gateway distributes traffic: ~9 of 10 requests → svc-api stable.', move_to=(675, 60), duration_ms=900),
                P(readout='<strong>Step 3.</strong> ~1 of 10 → svc-api-v2 canary. Pure declarative — no controller-specific annotations.', move_to=(675, 130), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L26 — AdminNetworkPolicy + FQDN
# ===================================================================
SCENE_L26 = f'''        {_mode_label()}
        {_box(40, 70, 100, 80, "Pod (in app namespace)", "wants egress", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(180, 50, 200, 28, "1. AdminNetworkPolicy", "high priority · admin owns", fill="#A04832", label_color="#FFFFFF")}
        {_box(180, 86, 200, 28, "2. NetworkPolicy", "namespace · team owns", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(180, 122, 200, 28, "3. BaselineAdminNetworkPolicy", "default · admin owns", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(420, 70, 140, 80, "Decision", "allow / deny / pass", fill="#ECEFF5", stroke="#3F4A5E")}
        {_box(600, 70, 140, 80, "Destination", "github.com / *.amazonaws / pastebin", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_L26 = Animation(
    h2="Three-tier policy evaluation — ANP → NetworkPolicy → BANP",
    intro="Each packet runs through ANP first (admin override), then NetworkPolicy (team allow), then BANP (cluster default). Pick a destination.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L26,
    initial_packet_xy=(90, 110),
    initial_readout='<strong>Watching:</strong> egress evaluation. Each tier can short-circuit with allow or deny.',
    scenes=[
        AnimationScene(
            mode_id="github",
            button_label="▶ to github.com (FQDN allowed)",
            mode_label="Mode: egress to github.com (allowed via FQDN policy)",
            phases=[
                P(readout='<strong>Step 1.</strong> Packet hits ANP first. No ANP rule matches github.com → fall through.', move_to=(280, 64), duration_ms=900),
                P(readout='<strong>Step 2.</strong> NetworkPolicy: CNI extension <code>egress.toFQDNs</code> matches github.com → allow.', move_to=(280, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Decision = allow. CNI installs short-lived per-IP rule for the resolved address.', move_to=(490, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Packet reaches github.com. CI build can clone code.', move_to=(670, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="pastebin",
            button_label="▶ to pastebin.com (BANP denies)",
            mode_label="Mode: egress to pastebin.com — caught by default-deny BANP",
            phases=[
                P(readout='<strong>Step 1.</strong> Packet hits ANP. No specific rule for pastebin.com → fall through.', move_to=(280, 64), duration_ms=900),
                P(readout='<strong>Step 2.</strong> NetworkPolicy: namespace has no egress allow for pastebin.com → fall through.', move_to=(280, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> BANP: cluster default-deny on egress except DNS / kube-apiserver → deny.', move_to=(280, 136), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Packet dropped. Exfiltration prevented.', move_to=(490, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="kubesys",
            button_label="▶ to kube-system (ANP denies)",
            mode_label="Mode: egress to kube-system — ANP override denies",
            phases=[
                P(readout='<strong>Step 1.</strong> Packet hits ANP. Rule: \"deny egress to kube-system from app namespaces.\"', move_to=(280, 64), duration_ms=900),
                P(readout='<strong>Step 2.</strong> ANP Deny terminates evaluation immediately. Team policies cannot override.', duration_ms=400, pause_after_ms=1500),
                P(readout='<strong>Step 3.</strong> Packet dropped at the admin tier. Exactly the property NetworkPolicy v1 lacked.', move_to=(490, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L27 — RBAC & Authentication
# ===================================================================
SCENE_L27 = f'''        {_mode_label()}
        {_box(40, 70, 110, 80, "Subject", "user / SA", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(190, 60, 140, 30, "Authentication", "OIDC / SA token / cert", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(190, 100, 140, 30, "RBAC authoriser", "verb on resource", fill="#A04832", label_color="#FFFFFF")}
        {_box(190, 140, 140, 30, "Admission", "PSA / VAP / webhook", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(370, 60, 130, 110, "Role binder", "matched", fill="#ECEFF5", stroke="#3F4A5E")}
        {_box(540, 60, 110, 50, "✓ ALLOW", "writes to etcd", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(540, 120, 110, 50, "✗ DENY", "401 / 403", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_L27 = Animation(
    h2="A request through authn + RBAC — three identity types",
    intro="Every API request walks identity → permission → admission. Pick an identity and watch the path.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L27,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a request looking for permission to <code>list secrets</code>. Each identity has its own check path.',
    scenes=[
        AnimationScene(
            mode_id="user",
            button_label="▶ Human user via OIDC",
            mode_label="Mode: human user via OIDC",
            phases=[
                P(readout='<strong>Step 1.</strong> User\'s kubectl presents an OIDC token from corp SSO.', move_to=(260, 75), duration_ms=900),
                P(readout='<strong>Step 2.</strong> API server validates JWT signature; identity = alice@corp.', move_to=(260, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> RBAC: <code>cluster-admins</code> ClusterRoleBinding includes alice → allow.', move_to=(435, 115), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Admission OK. Read returns Secrets.', move_to=(595, 85), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="sa",
            button_label="▶ Pod via SA token",
            mode_label="Mode: Pod presents bound SA token",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod presents projected JWT from <code>/var/run/secrets/.../token</code>.', move_to=(260, 75), duration_ms=900),
                P(readout='<strong>Step 2.</strong> API server validates signature + claims; identity = system:serviceaccount:app:web.', move_to=(260, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> RBAC: web SA has Role for ConfigMaps, NOT Secrets → deny.', move_to=(435, 115), duration_ms=900),
                P(readout='<strong>Step 4.</strong> 403 Forbidden. Pod sees the error; can\'t list Secrets.', move_to=(595, 145), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="anon",
            button_label="▶ Anonymous request",
            mode_label="Mode: anonymous request (no token)",
            phases=[
                P(readout='<strong>Step 1.</strong> Request arrives with no Authorization header.', move_to=(260, 75), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Authentication: identity = system:anonymous (if anonymous-auth=true) or 401.', move_to=(260, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> RBAC: no rule grants system:anonymous → deny. Production should disable anonymous-auth.', move_to=(595, 145), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L28 — Admission Control
# ===================================================================
SCENE_L28 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "request", "Pod create", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(190, 80, 130, 60, "Mutating", "add defaults", fill="#E8B547", stroke="#8B5A00", label_color="#5A4F45")}
        {_box(360, 80, 130, 60, "Validating", "PSA · VAP · webhook", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(540, 30, 200, 50, "Schema validation passes", "object well-formed", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(540, 90, 200, 50, "Persisted to etcd", "Pod scheduled", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(540, 150, 200, 50, "Rejected — DENY", "psa.restricted violation", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_L28 = Animation(
    h2="Admission flow — accepted vs rejected",
    intro="Pod-create requests go through mutation, then schema, then validation. Three modes: clean accept; mutator-fixed; PSA reject.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L28,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a Pod-create request walking the admission chain.',
    scenes=[
        AnimationScene(
            mode_id="accept",
            button_label="▶ Clean accept",
            mode_label="Mode: well-formed, policy-compliant Pod",
            phases=[
                P(readout='<strong>Step 1.</strong> Mutating admission: nothing to add — Pod already has labels + requests.', move_to=(255, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Validating admission: PSA <code>baseline</code> profile satisfied.', move_to=(425, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Persisted to etcd. Scheduler picks it up.', move_to=(640, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="mutate",
            button_label="▶ Mutator injects defaults",
            mode_label="Mode: Pod missing label; mutator adds default",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod has no <code>team</code> label. Kyverno mutate policy injects <code>team: unassigned</code>.', move_to=(255, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Validating admission then sees the now-mutated Pod with the required label.', move_to=(425, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Accepted. Mutate-then-validate is the standard pattern.', move_to=(640, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="reject",
            button_label="▶ PSA rejects privileged",
            mode_label="Mode: PSA restricted denies privileged Pod",
            phases=[
                P(readout='<strong>Step 1.</strong> Mutating admission: nothing to do.', move_to=(255, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Validating: PSA reads namespace label <code>enforce: restricted</code>.', move_to=(425, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod has <code>privileged: true</code> → rejected with clear message. Never reaches etcd.', move_to=(640, 175), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L29 — Policy Engines
# ===================================================================
SCENE_L29 = f'''        {_mode_label()}
        {_box(40, 80, 130, 60, "kubectl apply", "Deployment", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(210, 60, 200, 30, "Kyverno (YAML)", "ClusterPolicy", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(210, 100, 200, 30, "Gatekeeper (Rego)", "ConstraintTemplate", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(210, 140, 200, 30, "VAP (CEL in-cluster)", "no webhook", fill="#A04832", label_color="#FFFFFF")}
        {_box(450, 80, 130, 60, "PolicyReport", "pass / fail / warn", fill="#ECEFF5", stroke="#3F4A5E")}
        {_box(610, 80, 130, 60, "Apply or Reject", "etcd or 403", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_L29 = Animation(
    h2="Three engines, three policies, one decision",
    intro="The same admission decision runs through Kyverno or Gatekeeper or VAP. All produce a standard PolicyReport.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L29,
    initial_packet_xy=(105, 110),
    initial_readout='<strong>Watching:</strong> a Deployment apply consulting each engine in turn.',
    scenes=[
        AnimationScene(
            mode_id="kyverno",
            button_label="▶ Kyverno (YAML)",
            mode_label="Mode: Kyverno ClusterPolicy validates YAML rules",
            phases=[
                P(readout='<strong>Step 1.</strong> Apply hits Kyverno admission webhook.', move_to=(305, 75), duration_ms=900),
                P(readout='<strong>Step 2.</strong> ClusterPolicy validates: every container image must come from <code>cgr.dev/*</code>. Pass.', move_to=(515, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> PolicyReport CRD updated; apply allowed.', move_to=(675, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="gatekeeper",
            button_label="▶ OPA Gatekeeper (Rego)",
            mode_label="Mode: Gatekeeper ConstraintTemplate (Rego)",
            phases=[
                P(readout='<strong>Step 1.</strong> Apply hits Gatekeeper admission webhook.', move_to=(305, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Rego evaluates: <code>k8sallowedrepos</code> — same image-allow-list, expressed in Rego.', move_to=(515, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Same PolicyReport format → consumable by the same dashboards as Kyverno.', move_to=(675, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="vap",
            button_label="▶ VAP (CEL in-cluster)",
            mode_label="Mode: ValidatingAdmissionPolicy in-cluster (no webhook)",
            phases=[
                P(readout='<strong>Step 1.</strong> Apply hits the API server. VAP CEL evaluated <em>inside</em> kube-apiserver.', move_to=(305, 155), duration_ms=900),
                P(readout='<strong>Step 2.</strong> CEL: <code>has(object.metadata.labels.team)</code> — fast, no network call.', move_to=(515, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Decision returned. Latency essentially zero. Webhook count drops.', move_to=(675, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L30 — Supply Chain Security
# ===================================================================
SCENE_L30 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "git push", "source commit", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(180, 80, 130, 60, "SLSA L3 build", "GHA OIDC", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 180, 50, "OCI Registry · image", "sha256:abc...", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(340, 90, 180, 50, "OCI · SBOM (CycloneDX)", "components inventory", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(340, 150, 180, 50, "OCI · cosign signature", "Fulcio cert + Rekor", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(550, 80, 100, 60, "K8s admit", "verifyImages", fill="#A04832", label_color="#FFFFFF")}
        {_box(680, 80, 80, 60, "Pod runs", "OK", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_L30 = Animation(
    h2="Build → sign → verify chain — three deploy paths",
    intro="A signed image with SLSA provenance + SBOM passes admission. An unsigned image, or a signed-by-wrong-key image, fails.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L30,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> CI building + signing + the cluster verifying. Pick a deploy path.',
    scenes=[
        AnimationScene(
            mode_id="signed",
            button_label="▶ Signed + SBOM (pass)",
            mode_label="Mode: full chain — signed image, SLSA provenance, SBOM",
            phases=[
                P(readout='<strong>Step 1.</strong> CI builds; SLSA L3 provenance attestation generated by GHA.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Cosign keyless signs image; SBOM uploaded as OCI attestation.', move_to=(430, 60), duration_ms=900),
                P(readout='<strong>Step 3.</strong> K8s verifyImages: signature matches Fulcio cert from our GitHub org → pass.', move_to=(600, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Pod runs. End-to-end auditable chain.', move_to=(720, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="unsigned",
            button_label="▶ Unsigned image (reject)",
            mode_label="Mode: unsigned image — admission rejects",
            phases=[
                P(readout='<strong>Step 1.</strong> Build pipeline didn\'t sign (or attacker pushed direct to registry).', move_to=(430, 60), duration_ms=900),
                P(readout='<strong>Step 2.</strong> verifyImages policy: no signature found → reject.', move_to=(600, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod blocked at admission. Never reaches etcd.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="wrong-key",
            button_label="▶ Wrong key (reject)",
            mode_label="Mode: image signed by an unknown key",
            phases=[
                P(readout='<strong>Step 1.</strong> Image is signed — but Fulcio cert\'s OIDC subject doesn\'t match expected GitHub org.', move_to=(430, 175), duration_ms=900),
                P(readout='<strong>Step 2.</strong> verifyImages: identity mismatch → reject. Catches stolen registry credentials.', move_to=(600, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod blocked. Sigstore identity is the trust root, not just the registry credential.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L31 — Multi-Tenancy & Hardening
# ===================================================================
SCENE_L31 = f'''        {_mode_label()}
        {_box(40, 60, 130, 110, "tenant-a", "isolated namespace", fill="#E0EEF3", stroke="#4A8FA8")}
        <rect x="60" y="92" width="90" height="18" rx="2" fill="#5A9F7A"/><text x="105" y="105" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">RBAC</text>
        <rect x="60" y="114" width="90" height="18" rx="2" fill="#A04832"/><text x="105" y="127" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">NetworkPolicy</text>
        <rect x="60" y="136" width="90" height="18" rx="2" fill="#3F4A5E"/><text x="105" y="149" text-anchor="middle" font-size="8" fill="#FBF1D6" font-weight="700">PSA + Quota</text>
        {_box(220, 60, 130, 110, "tenant-b", "another namespace", fill="#E0EFE6", stroke="#5A9F7A")}
        <rect x="240" y="92" width="90" height="18" rx="2" fill="#5A9F7A"/>
        <rect x="240" y="114" width="90" height="18" rx="2" fill="#A04832"/>
        <rect x="240" y="136" width="90" height="18" rx="2" fill="#3F4A5E"/>
        {_box(390, 70, 160, 90, "Cross-tenant attempt", "blocked at NP layer", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(580, 70, 160, 90, "Quota exhaustion", "scheduler refuses", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}'''

ANIM_L31 = Animation(
    h2="What stops noisy-neighbour and cross-tenant leaks",
    intro="Tenant namespaces stacked with RBAC + NetworkPolicy + PSA + ResourceQuota + LimitRange. Pick a failure scenario.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L31,
    initial_packet_xy=(105, 110),
    initial_readout='<strong>Watching:</strong> tenant isolation in action.',
    scenes=[
        AnimationScene(
            mode_id="cross",
            button_label="▶ tenant-a → tenant-b (NP blocks)",
            mode_label="Mode: cross-tenant traffic blocked by NetworkPolicy",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod in tenant-a tries to reach a Service in tenant-b.', move_to=(285, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> NetworkPolicy ingress rule on tenant-b: deny except from same namespace + monitoring.', move_to=(470, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Packet dropped. Cross-tenant lateral movement prevented.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="quota",
            button_label="▶ tenant-a tries 200Gi RAM (Quota blocks)",
            mode_label="Mode: ResourceQuota refuses overrun",
            phases=[
                P(readout='<strong>Step 1.</strong> tenant-a applies a Pod requesting 200Gi memory.', move_to=(105, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> ResourceQuota for tenant-a caps total memory at 32Gi → admission rejects.', move_to=(660, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod never created. Other tenants protected from noisy-neighbour eviction.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="psa",
            button_label="▶ tenant-a tries privileged (PSA blocks)",
            mode_label="Mode: PSA restricted refuses privileged Pod",
            phases=[
                P(readout='<strong>Step 1.</strong> tenant-a applies a Pod with <code>privileged: true</code>.', move_to=(105, 145), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Namespace has <code>pod-security.kubernetes.io/enforce: restricted</code>.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> PSA rejects: container kernel-escape paths closed off.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L32 — Observability Pt 1: Logs + Metrics
# ===================================================================
SCENE_L32 = f'''        {_mode_label()}
        {_box(40, 70, 130, 80, "Pod", "stdout / /metrics", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(200, 70, 160, 80, "OTel Collector", "DaemonSet", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(390, 30, 170, 50, "Loki", "log store", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(390, 90, 170, 50, "Prometheus", "metrics TSDB", fill="#E0EEF3", stroke="#4A8FA8", label_color="#3F4A5E")}
        {_box(390, 150, 170, 50, "Grafana", "dashboards / alerts", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(590, 90, 150, 60, "On-call sees", "spike alert", fill="#A04832", label_color="#FFFFFF")}'''

ANIM_L32 = Animation(
    h2="A log line and a metric — the two pillars in motion",
    intro="App writes to stdout + exposes /metrics. OTel ships both. Backend dashboards alert on patterns.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L32,
    initial_packet_xy=(105, 110),
    initial_readout='<strong>Watching:</strong> a log line and a metric flowing from the Pod.',
    scenes=[
        AnimationScene(
            mode_id="log",
            button_label="▶ a log line",
            mode_label="Mode: app log line → Loki",
            phases=[
                P(readout='<strong>Step 1.</strong> App writes <code>ERROR: payment timeout</code> to stdout.', move_to=(280, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> OTel Collector tails <code>/var/log/containers/...</code>; parses; ships via OTLP.', move_to=(475, 50), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Loki indexes labels (app=payment, level=ERROR). Searchable in seconds.', move_to=(665, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="metric",
            button_label="▶ a metric scrape",
            mode_label="Mode: /metrics scrape → Prometheus",
            phases=[
                P(readout='<strong>Step 1.</strong> Prometheus scrapes <code>:9090/metrics</code> every 15s.', move_to=(280, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> OTel Collector receives + adds labels (pod, namespace).', move_to=(475, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Prometheus stores time-series; PromQL aggregations available.', move_to=(665, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="alert",
            button_label="▶ alert fires",
            mode_label="Mode: error rate breaches threshold → alert + dashboard",
            phases=[
                P(readout='<strong>Step 1.</strong> AlertManager evaluates <code>rate(http_5xx[5m]) > 10</code>.', move_to=(475, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Threshold breached → fire alert → Grafana panel turns red.', move_to=(475, 175), duration_ms=900),
                P(readout='<strong>Step 3.</strong> On-call paged. Dashboard linked from runbook annotation.', move_to=(665, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L33 — Observability Pt 2: Traces, eBPF, SLOs
# ===================================================================
SCENE_L33 = f'''        {_mode_label()}
        {_box(30, 80, 100, 60, "user", "request", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        <rect x="160" y="60" width="200" height="14" rx="2" fill="#3F4A5E"/><text x="166" y="71" font-size="8" fill="#FBF1D6" font-weight="700">gateway</text>
        <rect x="180" y="78" width="180" height="14" rx="2" fill="#5A9F7A"/><text x="186" y="89" font-size="8" fill="#FFFFFF" font-weight="700">checkout</text>
        <rect x="200" y="96" width="120" height="14" rx="2" fill="#4A8FA8"/><text x="206" y="107" font-size="8" fill="#FFFFFF" font-weight="700">auth</text>
        <rect x="220" y="114" width="80" height="14" rx="2" fill="#A04832"/><text x="226" y="125" font-size="8" fill="#FFFFFF" font-weight="700">db (slow)</text>
        {_box(400, 60, 150, 80, "Tempo / Jaeger", "trace backend", fill="#ECEFF5", stroke="#3F4A5E")}
        {_box(580, 60, 160, 80, "Grafana flame", "auth.db slowest span", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(170, 150, 200, 50, "eBPF (Hubble)", "kernel-level flows", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(400, 150, 340, 50, "SLO + burn-rate alert", "98.5% target · 73% budget left", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}'''

ANIM_L33 = Animation(
    h2="Trace a slow request — eBPF and SLOs as backstops",
    intro="Three modes: distributed trace pinpoints the slow span; eBPF captures the same flow at the kernel; SLO burn-rate decides whether to page.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L33,
    initial_packet_xy=(85, 110),
    initial_readout='<strong>Watching:</strong> a slow checkout request across services.',
    scenes=[
        AnimationScene(
            mode_id="trace",
            button_label="▶ distributed trace",
            mode_label="Mode: trace shows where time went",
            phases=[
                P(readout='<strong>Step 1.</strong> Request enters gateway → checkout → auth → db. Each hop adds a span.', move_to=(270, 95), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Spans shipped via OTLP to Tempo; reassembled by trace ID.', move_to=(475, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Flame graph shows db span at 60ms (90% of total). Bug located in 5 minutes.', move_to=(660, 100), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="ebpf",
            button_label="▶ eBPF (Hubble)",
            mode_label="Mode: eBPF observes kernel-level — no app changes",
            phases=[
                P(readout='<strong>Step 1.</strong> Cilium/Hubble has eBPF probes on every TCP connect/accept on every node.', move_to=(270, 175), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Per-flow telemetry: src=auth, dst=db, latency=58ms, status=200.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> Catches the slowdown without touching app code. Useful for legacy + closed-source services.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="slo",
            button_label="▶ SLO burn-rate",
            mode_label="Mode: SLO 99.9% target — burn-rate alert decides",
            phases=[
                P(readout='<strong>Step 1.</strong> SLO: 99.9% of checkout under 200ms over 30 days. Budget = 0.1%.', move_to=(570, 175), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Last 1h: 94% under 200ms. Burning budget at 6× normal rate.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> Multi-window burn-rate alert fires. Pages on-call <em>before</em> the SLO breaks.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L34 — Autoscaling
# ===================================================================
SCENE_L34 = f'''        {_mode_label()}
        {_box(40, 60, 110, 60, "Demand spike", "5x normal", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 50, 130, 30, "HPA", "CPU/mem/custom", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 30, "KEDA", "queue depth", fill="#E8B547", stroke="#8B5A00", label_color="#5A4F45")}
        {_box(180, 130, 130, 30, "VPA", "right-size requests", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 80, 120, 60, "Replicas grow", "4 → 16 Pods", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(490, 80, 120, 60, "Karpenter", "node fit?", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(640, 80, 100, 60, "New nodes", "spun up", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_L34 = Animation(
    h2="Replicas grow → nodes follow — three scaler modes",
    intro="Workload-level scaler fires; if no node fits, cluster-level scaler provisions. Pick a scaling signal.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_L34,
    initial_packet_xy=(95, 90),
    initial_readout='<strong>Watching:</strong> demand → workload scaler → cluster scaler.',
    scenes=[
        AnimationScene(
            mode_id="hpa",
            button_label="▶ HPA on CPU",
            mode_label="Mode: HPA scales replicas on CPU utilisation",
            phases=[
                P(readout='<strong>Step 1.</strong> CPU per replica jumps from 50% to 95%.', move_to=(245, 65), duration_ms=900),
                P(readout='<strong>Step 2.</strong> HPA computes desired = 4 × (95/70) = 6 replicas. Scales up.', move_to=(400, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Some new Pods can\'t fit. Karpenter receives Pending Pods.', move_to=(550, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Karpenter spins up the cheapest fitting instance type. Pods schedule.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="keda",
            button_label="▶ KEDA on queue depth",
            mode_label="Mode: KEDA scales on Kafka lag",
            phases=[
                P(readout='<strong>Step 1.</strong> Kafka topic lag rises to 50K messages.', move_to=(245, 105), duration_ms=900),
                P(readout='<strong>Step 2.</strong> KEDA scaler maps lag → desired replicas. Grows worker Deployment 0 → 30.', move_to=(400, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Karpenter provisions; workers drain the queue; KEDA scales back to 0.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="vpa",
            button_label="▶ VPA right-sizes",
            mode_label="Mode: VPA observes actual usage; right-sizes requests",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod requests 1 CPU but actually uses 250m on average over a week.', move_to=(245, 145), duration_ms=900),
                P(readout='<strong>Step 2.</strong> VPA recommender suggests requests=300m. Updater evicts + recreates Pod.', move_to=(400, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> 3 small Pods can now fit on a node where 1 oversized one used to live.', move_to=(550, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L35 — Reliability & HA
# ===================================================================
SCENE_L35 = f'''        {_mode_label()}
        {_box(40, 50, 100, 100, "zone us-1a", "2 Pods", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        <circle cx="90" cy="100" r="8" fill="#5A9F7A"/><circle cx="90" cy="125" r="8" fill="#5A9F7A"/>
        {_box(160, 50, 100, 100, "zone us-1b", "2 Pods", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        <circle cx="210" cy="100" r="8" fill="#5A9F7A"/><circle cx="210" cy="125" r="8" fill="#5A9F7A"/>
        {_box(280, 50, 100, 100, "zone us-1c", "2 Pods (failing)", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        <circle cx="330" cy="100" r="8" fill="#9D9389"/><circle cx="330" cy="125" r="8" fill="#9D9389"/>
        {_box(410, 60, 150, 80, "PDB minAvailable=4", "voluntary disruption cap", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(580, 30, 160, 50, "warm DR cluster", "us-west-2", fill="#9D9389", label_color="#FBF1D6")}
        {_box(580, 90, 160, 50, "auto-scale recovery", "HPA + Karpenter", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}'''

ANIM_L35 = Animation(
    h2="What happens when things break — three failure modes",
    intro="Zone failure (involuntary), drain (voluntary, PDB-protected), regional DR — three distinct failure handling paths.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_L35,
    initial_packet_xy=(330, 100),
    initial_readout='<strong>Watching:</strong> 6 Pods spread across 3 zones. Pick a failure scenario.',
    scenes=[
        AnimationScene(
            mode_id="zone",
            button_label="▶ zone-c fails",
            mode_label="Mode: zone outage — topology spread saves the service",
            phases=[
                P(readout='<strong>Step 1.</strong> Zone us-1c goes dark. 2 Pods unreachable; 4 healthy in 1a + 1b.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 2.</strong> Service mesh / kube-proxy removes failed endpoints; traffic shifts.', move_to=(150, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> HPA scales up + Karpenter adds nodes in healthy zones. Recovery in ~60s.', move_to=(660, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="drain",
            button_label="▶ drain a node (PDB)",
            mode_label="Mode: voluntary drain bounded by PodDisruptionBudget",
            phases=[
                P(readout='<strong>Step 1.</strong> Operator runs <code>kubectl drain node-X</code> in zone us-1a.', move_to=(85, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> PDB minAvailable=4 — eviction blocked until replacement Pod is Ready.', move_to=(485, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod by Pod, drain proceeds. Service stays at ≥ 4 ready.', move_to=(85, 125), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="dr",
            button_label="▶ regional failover",
            mode_label="Mode: us-east-1 region down — warm DR takes over",
            phases=[
                P(readout='<strong>Step 1.</strong> Whole region us-east-1 unreachable. Detection via external probes.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 2.</strong> DNS-level failover (Route53) flips to us-west-2 warm cluster.', move_to=(660, 55), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Warm cluster scales up to absorb full traffic. RTO ~15 min.', move_to=(660, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L36 — Kustomize
# ===================================================================
SCENE_L36 = f'''        {_mode_label()}
        {_box(40, 60, 130, 110, "base/", "deployment.yaml + svc.yaml + cm.yaml", fill="#FFFFFF", stroke="#3F4A5E")}
        {_box(200, 30, 160, 40, "overlays/dev", "replicas: 1, image: dev", fill="#E0EEF3", stroke="#4A8FA8")}
        {_box(200, 80, 160, 40, "overlays/staging", "replicas: 2", fill="#FBF1D6", stroke="#8B5A00")}
        {_box(200, 130, 160, 40, "overlays/prod", "replicas: 6, HPA, PDB", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(390, 80, 120, 60, "kustomize build", "merge", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(540, 80, 200, 60, "Final YAML manifest", "ready to apply", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_L36 = Animation(
    h2="Same base, three environments — pick an overlay",
    intro="Kustomize takes the base + an overlay\'s patches and produces a final manifest. No string templating.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_L36,
    initial_packet_xy=(105, 115),
    initial_readout='<strong>Watching:</strong> kustomize build merging base + overlay.',
    scenes=[
        AnimationScene(
            mode_id="dev",
            button_label="▶ overlays/dev",
            mode_label="Mode: build dev — base + tiny dev patch",
            phases=[
                P(readout='<strong>Step 1.</strong> Read base/kustomization.yaml → 3 resources.', move_to=(280, 50), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Apply dev overlay: replicas → 1, image → dev tag.', move_to=(450, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Final manifest: same K8s objects, dev-specific values. Apply with <code>kubectl apply -k</code>.', move_to=(640, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="staging",
            button_label="▶ overlays/staging",
            mode_label="Mode: build staging",
            phases=[
                P(readout='<strong>Step 1.</strong> Same base.', move_to=(280, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Apply staging overlay: replicas → 2, env vars adjusted.', move_to=(450, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Final manifest. Same shape as dev; different values.', move_to=(640, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="prod",
            button_label="▶ overlays/prod",
            mode_label="Mode: build prod — base + heavier overlay",
            phases=[
                P(readout='<strong>Step 1.</strong> Same base.', move_to=(280, 150), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Prod overlay adds: replicas=6, HPA YAML, PDB YAML, NetworkPolicy.', move_to=(450, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Final manifest: 6 K8s objects (3 base + 3 overlay-only). Production-ready.', move_to=(640, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L37 — Helm 3
# ===================================================================
SCENE_L37 = f'''        {_mode_label()}
        {_box(30, 60, 140, 110, "OCI registry", "chart cert-manager:1.14", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(190, 60, 130, 110, "values.yaml", "user overrides", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(340, 60, 130, 110, "helm install", "render templates", fill="#A04832", label_color="#FFFFFF")}
        {_box(490, 60, 130, 110, "K8s API", "create resources", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 60, 100, 110, "Release Secret", "history", fill="#ECEFF5", stroke="#3F4A5E")}'''

ANIM_L37 = Animation(
    h2="Helm install / upgrade / rollback — release lifecycle",
    intro="Charts pulled from OCI; templates rendered with values; release recorded as a Secret. Rollback re-applies a prior revision.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L37,
    initial_packet_xy=(100, 115),
    initial_readout='<strong>Watching:</strong> a Helm release lifecycle.',
    scenes=[
        AnimationScene(
            mode_id="install",
            button_label="▶ helm install",
            mode_label="Mode: helm install",
            phases=[
                P(readout='<strong>Step 1.</strong> <code>helm install cm oci://registry/charts/cert-manager --version 1.14</code>.', move_to=(255, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Helm pulls chart; merges values.yaml with user overrides.', move_to=(405, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Renders templates → posts to K8s API.', move_to=(555, 115), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Release recorded as Secret <code>sh.helm.release.v1.cm.v1</code>.', move_to=(690, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="upgrade",
            button_label="▶ helm upgrade",
            mode_label="Mode: helm upgrade — apply new version",
            phases=[
                P(readout='<strong>Step 1.</strong> <code>helm upgrade cm ... --version 1.15</code>.', move_to=(100, 115), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Helm renders v1.15; diffs against previous render; applies changes.', move_to=(405, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> New Release Secret <code>sh.helm.release.v1.cm.v2</code>. Old kept for rollback.', move_to=(690, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="rollback",
            button_label="▶ helm rollback",
            mode_label="Mode: helm rollback to previous revision",
            phases=[
                P(readout='<strong>Step 1.</strong> <code>helm rollback cm 1</code>.', move_to=(690, 115), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Helm reads Secret v1; re-applies that manifest set.', move_to=(555, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Cluster reverts to v1.14. Hooks that ran during upgrade are NOT undone — plan migrations to be reversible.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L38 — Argo CD
# ===================================================================
SCENE_L38 = f'''        {_mode_label()}
        {_box(40, 60, 130, 110, "git repo", "manifests/main", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(190, 60, 140, 110, "Argo CD", "watch + reconcile", fill="#A04832", label_color="#FFFFFF")}
        {_box(350, 60, 130, 110, "Cluster", "live state", fill="#FFFFFF", stroke="#5A4F45")}
        {_box(500, 30, 240, 50, "Synced ✓", "live = git", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(500, 90, 240, 50, "OutOfSync (drift)", "kubectl edit detected", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(500, 150, 240, 50, "selfHeal reverts", "manual edit lost", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}'''

ANIM_L38 = Animation(
    h2="Argo CD reconciles — three sync states",
    intro="Push to git → Argo CD applies. Hand-edit cluster → drift detected. selfHeal=true → drift reverted.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L38,
    initial_packet_xy=(105, 115),
    initial_readout='<strong>Watching:</strong> the GitOps reconciliation loop.',
    scenes=[
        AnimationScene(
            mode_id="push",
            button_label="▶ git push → sync",
            mode_label="Mode: developer pushes to git → Argo CD syncs",
            phases=[
                P(readout='<strong>Step 1.</strong> Developer merges PR to main. Manifest updated.', move_to=(105, 115), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Argo CD polls git (or webhook); detects diff.', move_to=(260, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Argo CD applies via kube-apiserver. State = Synced.', move_to=(415, 115), duration_ms=900),
                P(readout='<strong>Step 4.</strong> UI shows green Synced + Healthy.', move_to=(620, 55), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="drift",
            button_label="▶ kubectl edit → drift",
            mode_label="Mode: hand-edit creates drift; Argo CD shows OutOfSync",
            phases=[
                P(readout='<strong>Step 1.</strong> Engineer runs <code>kubectl edit deployment</code> during incident. Replicas changed.', move_to=(415, 115), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Argo CD\'s next compare detects: cluster ≠ git.', move_to=(260, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> UI shows OutOfSync (orange). On-call sees the drift on the dashboard.', move_to=(620, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="heal",
            button_label="▶ selfHeal reverts",
            mode_label="Mode: selfHeal=true reverts drift automatically",
            phases=[
                P(readout='<strong>Step 1.</strong> Drift detected as before.', move_to=(260, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> selfHeal=true → Argo CD re-applies git state, overwriting the manual edit.', move_to=(415, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> State back to Synced. Discipline enforced: git is the only mutator.', move_to=(620, 175), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L39 — Flux CD
# ===================================================================
SCENE_L39 = f'''        {_mode_label()}
        {_box(40, 60, 110, 110, "git repo", "manifests/", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(170, 30, 160, 40, "source-controller", "fetch", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(170, 80, 160, 40, "kustomize-controller", "render + apply", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(170, 130, 160, 40, "helm-controller", "HelmRelease", fill="#A04832", label_color="#FFFFFF")}
        {_box(350, 60, 130, 110, "Cluster", "applied", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(500, 60, 240, 110, "notification-controller", "Slack alert on failure", fill="#E8B547", stroke="#8B5A00", label_color="#5A4F45")}'''

ANIM_L39 = Animation(
    h2="Flux\'s multi-controller flow — three resource types",
    intro="Source-controller fetches; specialised controllers render + apply. Notifications fan out to Slack/Teams/etc.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_L39,
    initial_packet_xy=(95, 115),
    initial_readout='<strong>Watching:</strong> Flux\'s composable controllers in action.',
    scenes=[
        AnimationScene(
            mode_id="kustomize",
            button_label="▶ Kustomization",
            mode_label="Mode: kustomize-controller applies a Kustomization",
            phases=[
                P(readout='<strong>Step 1.</strong> source-controller pulls git; exposes content.', move_to=(250, 50), duration_ms=900),
                P(readout='<strong>Step 2.</strong> kustomize-controller reads Kustomization CRD; runs <code>kustomize build</code>.', move_to=(250, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Applies the rendered manifest. Status updated on the Kustomization CRD.', move_to=(415, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="helm",
            button_label="▶ HelmRelease",
            mode_label="Mode: helm-controller manages a release",
            phases=[
                P(readout='<strong>Step 1.</strong> source-controller fetches a chart from HelmRepository (or OCIRepository).', move_to=(250, 50), duration_ms=900),
                P(readout='<strong>Step 2.</strong> helm-controller reads HelmRelease CRD; renders chart with values; applies.', move_to=(250, 150), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Status reflects install/upgrade outcome. Drift triggers re-apply.', move_to=(415, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="alert",
            button_label="▶ failure → notification",
            mode_label="Mode: reconcile fails → notification-controller alerts",
            phases=[
                P(readout='<strong>Step 1.</strong> kustomize-controller fails to apply (CRD missing).', move_to=(250, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> notification-controller picks up the event from CRD status.', move_to=(620, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Provider (Slack webhook) fires. On-call sees the failure within seconds.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L40 — Progressive Delivery
# ===================================================================
SCENE_L40 = f'''        {_mode_label()}
        {_box(40, 60, 100, 60, "user request", "100% traffic", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(170, 60, 200, 60, "Gateway / Ingress", "weighted split", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(400, 30, 170, 50, "stable v1.2", "weight 90", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(400, 90, 170, 50, "canary v1.3", "weight 10", fill="#E8B547", stroke="#8B5A00", label_color="#5A4F45")}
        {_box(600, 60, 140, 60, "AnalysisTemplate", "success rate ≥ 99?", fill="#A04832", label_color="#FFFFFF")}
        {_box(170, 150, 270, 50, "promote → 100% canary", "rollout complete", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(470, 150, 270, 50, "abort → 0% canary", "auto rollback", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_L40 = Animation(
    h2="Canary release — promote vs abort",
    intro="Argo Rollouts splits traffic 90/10; AnalysisTemplate runs queries; auto-promote on success or auto-abort on failure.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L40,
    initial_packet_xy=(90, 90),
    initial_readout='<strong>Watching:</strong> a canary phase deciding promote vs abort.',
    scenes=[
        AnimationScene(
            mode_id="promote",
            button_label="▶ canary metrics OK → promote",
            mode_label="Mode: canary success — promote",
            phases=[
                P(readout='<strong>Step 1.</strong> Rollout enters canary phase: 10% → v1.3, 90% → v1.2.', move_to=(270, 90), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Some traffic flows to canary v1.3.', move_to=(485, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> AnalysisTemplate evaluates Prometheus query → success rate 99.7%.', move_to=(670, 90), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Pass → ramp 25% → 50% → 100%. v1.3 promoted; v1.2 scaled down.', move_to=(305, 175), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="abort",
            button_label="▶ canary degrades → abort",
            mode_label="Mode: canary fails analysis — abort",
            phases=[
                P(readout='<strong>Step 1.</strong> Canary phase begins: 10% → v1.3.', move_to=(270, 90), duration_ms=900),
                P(readout='<strong>Step 2.</strong> v1.3 has a bug: 5xx error rate spikes on canary Pods.', move_to=(485, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> AnalysisTemplate fails. Threshold breached.', move_to=(670, 90), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Auto-abort: drop traffic to 0% canary; scale v1.3 down. Total user impact: ~30s degraded for 10% of traffic.', move_to=(605, 175), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="bluegreen",
            button_label="▶ blue/green (atomic switch)",
            mode_label="Mode: blue/green — deploy + smoke + flip",
            phases=[
                P(readout='<strong>Step 1.</strong> v1.3 deployed alongside v1.2; no traffic yet.', move_to=(485, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Smoke tests run against v1.3 internally. AnalysisTemplate checks pass.', move_to=(670, 90), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Service selector flipped: 100% to v1.3 atomically. Old kept around for instant rollback.', move_to=(305, 175), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L41 — CRDs Deep Dive
# ===================================================================
SCENE_L41 = f'''        {_mode_label()}
        {_box(40, 60, 130, 110, "CR (v1alpha1)", "user-applied", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(190, 60, 140, 110, "API server", "validate + mutate", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(350, 50, 140, 50, "x-kubernetes-validations", "CEL inline", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(350, 110, 140, 50, "Conversion webhook", "v1alpha1 ↔ v1", fill="#A04832", label_color="#FFFFFF")}
        {_box(510, 60, 110, 110, "etcd", "stored as v1", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}
        {_box(640, 60, 100, 110, "Reconciler", "reads as v1", fill="#ECEFF5", stroke="#3F4A5E")}'''

ANIM_L41 = Animation(
    h2="CR write/read across versions — pick a path",
    intro="CRD has v1alpha1 + v1; storage version is v1. Watch the conversion webhook + CEL validation along the way.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_L41,
    initial_packet_xy=(105, 115),
    initial_readout='<strong>Watching:</strong> a CR moving through API server, schema, conversion, persistence.',
    scenes=[
        AnimationScene(
            mode_id="cel",
            button_label="▶ CEL validation",
            mode_label="Mode: CEL inline rule rejects bad input",
            phases=[
                P(readout='<strong>Step 1.</strong> User applies CR with <code>maxReplicas: 3, replicas: 5</code>.', move_to=(260, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> API server runs CEL: <code>self.maxReplicas >= self.replicas</code> → false.', move_to=(420, 75), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Apply rejected with clear error. No webhook involved.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="convert",
            button_label="▶ v1alpha1 write → v1 storage",
            mode_label="Mode: write v1alpha1; conversion webhook converts to v1 for storage",
            phases=[
                P(readout='<strong>Step 1.</strong> User applies CR at apiVersion v1alpha1.', move_to=(260, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> CEL validation passes. Conversion webhook called: v1alpha1 → v1.', move_to=(420, 135), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Stored in etcd as v1 (the storage version).', move_to=(565, 115), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Operator reads as v1 (its preferred version). Conversion is invisible to the operator.', move_to=(690, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="status",
            button_label="▶ controller writes status",
            mode_label="Mode: controller writes via /status subresource",
            phases=[
                P(readout='<strong>Step 1.</strong> Reconciler observes desired state.', move_to=(690, 115), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Patches status: <code>kubectl patch ... --subresource=status</code>.', move_to=(420, 135), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Spec untouched; status updated. Convention: spec = user; status = controller.', move_to=(565, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L42 — Operators
# ===================================================================
SCENE_L42 = f'''        {_mode_label()}
        {_box(40, 60, 110, 110, "user", "kubectl apply CR", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(170, 60, 140, 110, "API server", "writes etcd", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(330, 60, 150, 110, "Operator Pod", "watch loop", fill="#A04832", label_color="#FFFFFF")}
        {_box(500, 60, 130, 110, "Reconcile()", "create resources", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(650, 60, 100, 110, "Owned objects", "StatefulSet, Service, Secret", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_L42 = Animation(
    h2="A reconcile loop in motion — three lifecycle moments",
    intro="Create CR → operator reconciles → owned objects appear. Update CR → operator diffs and patches. Delete CR → finalizer cleans up external state.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_L42,
    initial_packet_xy=(95, 115),
    initial_readout='<strong>Watching:</strong> the operator pattern in motion.',
    scenes=[
        AnimationScene(
            mode_id="create",
            button_label="▶ create CR",
            mode_label="Mode: create — first reconcile",
            phases=[
                P(readout='<strong>Step 1.</strong> User applies <code>PostgresCluster</code> CR.', move_to=(240, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> API server writes to etcd; operator\'s informer cache sees the new object.', move_to=(405, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Reconcile() runs: creates StatefulSet + Service + Secret with owner refs.', move_to=(565, 115), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Status patched on CR: <code>conditions: [{type: Ready, status: True}]</code>.', move_to=(700, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="update",
            button_label="▶ update CR",
            mode_label="Mode: update — reconcile diffs and patches",
            phases=[
                P(readout='<strong>Step 1.</strong> User edits CR: replicas 3 → 5.', move_to=(240, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Watch fires on the operator. Reconcile() reads new spec.', move_to=(405, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Reconciler patches StatefulSet replicas → 5. Idempotent: re-running same input = same result.', move_to=(700, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="delete",
            button_label="▶ delete CR (finalizer)",
            mode_label="Mode: delete — finalizer cleans up before letting CR vanish",
            phases=[
                P(readout='<strong>Step 1.</strong> User runs <code>kubectl delete pgcluster x</code>. K8s sets DeletionTimestamp.', move_to=(240, 115), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Finalizer present → CR not yet deleted. Operator sees DeletionTimestamp.', move_to=(405, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Reconciler runs cleanup: deletes external S3 backups, releases cloud resources.', move_to=(565, 115), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Removes its finalizer; CR deletion completes. Owned objects garbage-collected via owner refs.', move_to=(700, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L43 — Service Mesh
# ===================================================================
SCENE_L43 = f'''        {_mode_label()}
        {_box(40, 60, 100, 110, "service A", "Pod", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(160, 60, 100, 50, "sidecar (envoy)", "per Pod", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(160, 120, 100, 50, "ztunnel (ambient)", "per Node", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(280, 60, 140, 110, "mTLS in flight", "encrypted", fill="#A04832", label_color="#FFFFFF")}
        {_box(440, 60, 100, 110, "service B", "Pod", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(560, 60, 180, 110, "Control plane", "policy + cert + telemetry", fill="#ECEFF5", stroke="#3F4A5E")}'''

ANIM_L43 = Animation(
    h2="Sidecar vs ambient — same mesh outcome, different overhead",
    intro="Service A calls service B over mTLS. Sidecar mode: a proxy per Pod. Ambient mode: a node-level proxy + selective waypoint Pods.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_L43,
    initial_packet_xy=(90, 110),
    initial_readout='<strong>Watching:</strong> service-to-service traffic via the mesh.',
    scenes=[
        AnimationScene(
            mode_id="sidecar",
            button_label="▶ sidecar mode",
            mode_label="Mode: sidecar — proxy per Pod",
            phases=[
                P(readout='<strong>Step 1.</strong> Service A makes plain HTTP to service B.', move_to=(210, 85), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Sidecar intercepts; wraps in mTLS using cert from control plane.', move_to=(350, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Encrypted bytes traverse the network; B\'s sidecar unwraps + delivers to app.', move_to=(490, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Telemetry emitted to control plane. Cost: ~200MB sidecar per Pod.', move_to=(650, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="ambient",
            button_label="▶ ambient mode (Istio)",
            mode_label="Mode: ambient — node-level ztunnel handles L4",
            phases=[
                P(readout='<strong>Step 1.</strong> Service A makes plain HTTP. No sidecar in the Pod.', move_to=(210, 145), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Node\'s ztunnel intercepts at the network namespace boundary; wraps in mTLS.', move_to=(350, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Encrypted bytes leave the node; B\'s ztunnel unwraps; delivers to app.', move_to=(490, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Same mesh outcome. ~70% lower per-Pod overhead. L7 features need a waypoint Pod.', move_to=(650, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="cilium",
            button_label="▶ Cilium (eBPF)",
            mode_label="Mode: Cilium — eBPF in-kernel; no extra proxy",
            phases=[
                P(readout='<strong>Step 1.</strong> Service A sends. Cilium\'s eBPF intercepts at the kernel.', move_to=(210, 145), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Per-flow policy + mTLS decided in eBPF programs. No userspace proxy hop.', move_to=(350, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Bytes leave the node. Hubble emits per-flow telemetry from the same eBPF.', move_to=(650, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# L44 — Troubleshooting
# ===================================================================
SCENE_L44 = f'''        {_mode_label()}
        {_box(40, 60, 130, 110, "Symptom", "Pods stuck Pending", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(190, 60, 140, 110, "Reproduce", "yes — every apply", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(350, 60, 140, 110, "Observe", "describe + events + logs", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(510, 60, 110, 110, "Hypothesise", "missing PVC binding", fill="#ECEFF5", stroke="#3F4A5E")}
        {_box(640, 60, 100, 110, "Verify fix", "WaitForFirstConsumer", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_L44 = Animation(
    h2="A debugging session, walked methodically",
    intro="Symptom → Reproduce → Observe → Hypothesise → Verify. Pick one of three real failure patterns from earlier lessons.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_L44,
    initial_packet_xy=(105, 115),
    initial_readout='<strong>Watching:</strong> the triage methodology applied to a real symptom.',
    scenes=[
        AnimationScene(
            mode_id="pending",
            button_label="▶ Pending Pods (storage zone)",
            mode_label="Mode: PVC + multi-zone scheduling",
            phases=[
                P(readout='<strong>Step 1.</strong> Symptom: Deployment\'s Pod stays Pending in a multi-zone cluster.', move_to=(105, 115), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Reproduce: <code>kubectl apply</code> Pod manifest reproducibly fails.', move_to=(260, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Observe: <code>kubectl describe pod</code> events: \"FailedAttachVolume — disk in different zone\".', move_to=(420, 115), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Hypothesise: StorageClass uses <code>volumeBindingMode: Immediate</code>; PVC was provisioned in a different zone.', move_to=(565, 115), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Fix: switch SC to <code>WaitForFirstConsumer</code>; recreate PVC; Pod schedules.', move_to=(690, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="oom",
            button_label="▶ OOMKilled cycle",
            mode_label="Mode: OOM kill investigation",
            phases=[
                P(readout='<strong>Step 1.</strong> Symptom: Pod restarts every few minutes. <code>kubectl get pod</code> shows RESTARTS=12.', move_to=(105, 115), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Observe: <code>kubectl describe</code> → \"Last State: Terminated, Reason: OOMKilled\".', move_to=(420, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> <code>kubectl logs --previous</code> for context before crash. Memory usage climbing.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 4.</strong> Hypothesise: limit too low for actual workload. Profile + raise <code>resources.limits.memory</code>.', move_to=(565, 115), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Fix verified: no more restarts; usage stable.', move_to=(690, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="403",
            button_label="▶ RBAC 403 forbidden",
            mode_label="Mode: 403 Forbidden — RBAC narrowing",
            phases=[
                P(readout='<strong>Step 1.</strong> Symptom: Pod logs show \"403 Forbidden — secrets is forbidden\".', move_to=(105, 115), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Observe: <code>kubectl auth can-i list secrets --as=system:sa:ns:app</code> → no.', move_to=(420, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Hypothesise: SA missing Role binding for the operation.', move_to=(565, 115), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Fix: add Role + RoleBinding granting <code>get</code> on the specific Secret name. Verify with <code>can-i</code>.', move_to=(690, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# ===================================================================
# Registry — keyed by lesson number string
# ===================================================================

ANIMATIONS = {
    "18": ANIM_L18,
    "19": ANIM_L19,
    "20": ANIM_L20,
    "21": ANIM_L21,
    "22": ANIM_L22,
    "23": ANIM_L23,
    "24": ANIM_L24,
    "25": ANIM_L25,
    "26": ANIM_L26,
    "27": ANIM_L27,
    "28": ANIM_L28,
    "29": ANIM_L29,
    "30": ANIM_L30,
    "31": ANIM_L31,
    "32": ANIM_L32,
    "33": ANIM_L33,
    "34": ANIM_L34,
    "35": ANIM_L35,
    "36": ANIM_L36,
    "37": ANIM_L37,
    "38": ANIM_L38,
    "39": ANIM_L39,
    "40": ANIM_L40,
    "41": ANIM_L41,
    "42": ANIM_L42,
    "43": ANIM_L43,
    "44": ANIM_L44,
}
