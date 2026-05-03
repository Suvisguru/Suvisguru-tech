"""Per-module Section 6 animations for K-VAN V1-V11."""

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


def _arrow(x1, y1, x2, y2, color="#9D9389"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.2" stroke-dasharray="3,3"/>'


def _mode_label(x=380, y=22):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="13" font-weight="600" fill="#3F4A5E" id="anim-mode-label">Mode</text>'


# V1 — architecture decisions: pick stacked vs external etcd, pick CNI
SCENE_V1 = f'''        {_mode_label()}
        {_box(40, 70, 130, 70, "ARCHITECTURE", "blueprint", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(220, 60, 200, 80, "Decision", "stacked or external etcd?", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(470, 30, 200, 50, "Stacked etcd", "simpler ops · 3 CP", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(470, 110, 200, 50, "External etcd", "5 etcd + 3 CP", fill="#A04832", label_color="#FFFFFF")}'''

ANIM_V1 = Animation(
    h2="Pick the architecture — stacked vs external etcd",
    intro="Same blueprint; two topology choices. Walk both.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_V1,
    initial_packet_xy=(105, 105),
    initial_readout='<strong>Watching:</strong> the architecture decision. Pick a topology.',
    scenes=[
        AnimationScene(
            mode_id="stacked",
            button_label="▶ stacked etcd",
            mode_label="Mode: stacked etcd — etcd on the same nodes as kube-apiserver",
            phases=[
                P(readout='<strong>Step 1.</strong> Architecture says: 3 CP nodes, etcd stacked on each.', move_to=(320, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Decision: stacked. Simpler ops; one less tier.', move_to=(570, 55), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Trade-off: etcd shares disks + CPU with apiserver. Fine for ≤ 250 nodes.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="external",
            button_label="▶ external etcd",
            mode_label="Mode: external etcd — dedicated etcd nodes",
            phases=[
                P(readout='<strong>Step 1.</strong> Architecture says: 5 dedicated etcd + 3 CP nodes.', move_to=(320, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Decision: external. More resilient; more ops.', move_to=(570, 135), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Trade-off: 8 nodes total instead of 3. Right for 500+ node clusters.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# V2 — node prep checklist
SCENE_V2 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "raw node", "freshly imaged", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "load modules", "overlay · br_netfilter", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 80, 130, 60, "sysctl", "ip_forward + bridge", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "containerd", "SystemdCgroup", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "ready", "kubeadm OK", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V2 = Animation(
    h2="Node prep — order matters",
    intro="Walk a raw node through the prep checklist in order.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_V2,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a node going from raw to kubeadm-ready.',
    scenes=[
        AnimationScene(
            mode_id="prep",
            button_label="▶ run the prep checklist",
            mode_label="Mode: ordered prep — modules → sysctl → runtime → ready",
            phases=[
                P(readout='<strong>Step 1.</strong> Raw node booted; nothing K8s-ready yet.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Load kernel modules: <code>overlay</code>, <code>br_netfilter</code>.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Apply sysctl: <code>ip_forward</code>, <code>bridge-nf-call-iptables</code>. Order matters: modules first.', move_to=(405, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Install containerd; set <code>SystemdCgroup = true</code> to match kubelet.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Reboot test, sanity-check, then <code>kubeadm</code> joins cleanly.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# V3 — kubeadm bootstrap (cp1 init, cp2/3 join, workers join)
SCENE_V3 = f'''        {_mode_label()}
        {_box(40, 80, 100, 60, "operator", "kubeadm CLI", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "cp-1", "kubeadm init", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 60, 130, 30, "cp-2", "join --control-plane", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 100, 130, 30, "cp-3", "join --control-plane", fill="#A04832", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "workers", "kubeadm join", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Ready", "all 6 nodes", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V3 = Animation(
    h2="HA bootstrap walk-through",
    intro="One init, two control-plane joins, three worker joins.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_V3,
    initial_packet_xy=(90, 110),
    initial_readout='<strong>Watching:</strong> a 3 CP + 3 worker bootstrap.',
    scenes=[
        AnimationScene(
            mode_id="bootstrap",
            button_label="▶ HA bootstrap",
            mode_label="Mode: HA bootstrap (cp-1 init → cp-2/3 join → workers join)",
            phases=[
                P(readout='<strong>Step 1.</strong> Operator runs <code>kubeadm init --upload-certs</code> on cp-1.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> cp-1 generates certs + bootstraps the control plane. Static pods start.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> cp-2 joins via <code>kubeadm join --control-plane --certificate-key</code>.', move_to=(405, 75), duration_ms=900),
                P(readout='<strong>Step 4.</strong> cp-3 joins likewise. Quorum + HA reached.', move_to=(405, 115), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Workers join via bootstrap token.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 6.</strong> All 6 nodes Ready (after CNI install).', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# V4 — CNI install
SCENE_V4 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "cluster", "NotReady", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "Helm install", "Cilium / Calico", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 80, 130, 60, "CNI Pods", "DaemonSet up", fill="#A04832", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "Pod CIDR", "configured", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Ready", "kubectl get nodes", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V4 = Animation(
    h2="From NotReady to Ready — CNI install",
    intro="Watch Cilium take a freshly bootstrapped cluster from NotReady to all-Ready.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_V4,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a fresh kubeadm cluster waiting for a CNI.',
    scenes=[
        AnimationScene(
            mode_id="cilium",
            button_label="▶ install Cilium",
            mode_label="Mode: install Cilium with kube-proxy replacement",
            phases=[
                P(readout='<strong>Step 1.</strong> All nodes NotReady — no CNI installed.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> <code>helm install cilium cilium/cilium</code> with podCIDR matching kubeadm config.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Cilium DaemonSet rolls out per node; sets up Pod networking.', move_to=(405, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Pod CIDR aligned (no mismatch); MTU verified.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 5.</strong> All nodes Ready. <code>cilium connectivity test</code> passes.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="mismatch",
            button_label="▶ Pod CIDR mismatch",
            mode_label="Mode: Pod CIDR misalignment — failure",
            phases=[
                P(readout='<strong>Step 1.</strong> CNI installed with wrong Pod CIDR.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Pods get IPs from CNI\'s range; controller-manager expects different range.', move_to=(405, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Cross-node Pod traffic broken; nodes flap NotReady.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# V5 — Argo CD App-of-Apps installs everything
SCENE_V5 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "git repo", "platform/", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "Argo CD", "App-of-Apps root", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 130, 30, "cert-manager", "", fill="#E8B547", label_color="#5A4F45")}
        {_box(340, 70, 130, 30, "Gateway", "", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 110, 130, 30, "CSI", "", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 150, 130, 30, "Velero", "", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(500, 80, 110, 60, "all add-ons", "synced", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V5 = Animation(
    h2="Argo CD reconciles the add-on stack",
    intro="One sync brings up the full add-on stack from git.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_V5,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> Argo CD App-of-Apps reconciling.',
    scenes=[
        AnimationScene(
            mode_id="reconcile",
            button_label="▶ reconcile App-of-Apps",
            mode_label="Mode: reconcile the platform from git",
            phases=[
                P(readout='<strong>Step 1.</strong> Git push: new add-on YAML committed to platform/.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Argo CD detects diff; the root App fans out to children.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Each child App syncs: cert-manager…', move_to=(405, 45), duration_ms=900),
                P(readout='<strong>Step 4.</strong> …Gateway…', move_to=(405, 85), duration_ms=900),
                P(readout='<strong>Step 5.</strong> …CSI + Velero. All Apps Synced + Healthy.', move_to=(555, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# V6 — Cluster config (audit + encryption applied)
SCENE_V6 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "kubeadm cfg", "YAML in git", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 140, 60, "apply on cp-1", "static-pod restart", fill="#A04832", label_color="#FFFFFF")}
        {_box(350, 30, 130, 50, "audit log", "to SIEM", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(350, 90, 130, 50, "encryption", "KMS v2 ciphertext", fill="#A04832", label_color="#FFFFFF")}
        {_box(350, 150, 130, 50, "reserved cpu/mem", "kubelet config", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(510, 80, 110, 60, "cluster", "tuned", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V6 = Animation(
    h2="Apply cluster config — audit, encryption, reserved",
    intro="Configuration changes propagate via static-pod restart.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_V6,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> kubeadm cluster config rolling out.',
    scenes=[
        AnimationScene(
            mode_id="apply",
            button_label="▶ apply cluster config",
            mode_label="Mode: apply audit + encryption + reserved",
            phases=[
                P(readout='<strong>Step 1.</strong> Push kubeadm config YAML to git.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Apply on cp-1; kubelet detects static-pod manifest change.', move_to=(250, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Audit log endpoint configured → SIEM.', move_to=(415, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> EncryptionConfiguration loaded → Secrets ciphertext in etcd.', move_to=(415, 115), duration_ms=900),
                P(readout='<strong>Step 5.</strong> kubelet reserved set → node allocatable corrected.', move_to=(415, 175), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Repeat on cp-2/3. Cluster tuned.', move_to=(565, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# V7 — etcd snapshot + restore
SCENE_V7 = f'''        {_mode_label()}
        {_box(40, 60, 110, 100, "etcd cluster", "3 members", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 30, 110, 50, "snapshot save", "etcdctl", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(180, 90, 110, 50, "off-site S3", "30 min cron", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(180, 150, 110, 50, "alarm: NOSPACE", "rare", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(320, 60, 130, 100, "DISASTER", "quorum lost", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(480, 60, 130, 100, "snapshot restore", "fresh 3-member", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 60, 100, 100, "cluster back", "RTO ~10m", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V7 = Animation(
    h2="etcd snapshot save → DR restore",
    intro="Routine snapshot. Then a quorum-loss disaster + restore.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_V7,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> etcd backup + recovery cycle.',
    scenes=[
        AnimationScene(
            mode_id="snapshot",
            button_label="▶ routine snapshot",
            mode_label="Mode: routine snapshot every 30 min",
            phases=[
                P(readout='<strong>Step 1.</strong> Cron fires <code>etcdctl snapshot save</code> on a member.', move_to=(235, 55), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Snapshot file shipped to S3.', move_to=(235, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="restore",
            button_label="▶ DR restore",
            mode_label="Mode: quorum loss → snapshot restore",
            phases=[
                P(readout='<strong>Step 1.</strong> Two of three etcd members crash. Cluster read-only.', move_to=(385, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Operator pulls latest snapshot from S3.', move_to=(235, 115), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Restore on three replacement nodes; bring up new etcd.', move_to=(545, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> apiservers reconnect; controllers reconcile derived state. ~10 min RTO.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# V8 — upgrade walk
SCENE_V8 = f'''        {_mode_label()}
        {_box(40, 70, 110, 60, "v1.35 cluster", "Ready", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(180, 70, 110, 60, "etcd snap", "backup", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(310, 70, 110, 60, "cp-1 upgrade", "kubeadm apply", fill="#A04832", label_color="#FFFFFF")}
        {_box(440, 70, 110, 60, "cp-2/3", "node upgrade", fill="#A04832", label_color="#FFFFFF")}
        {_box(570, 70, 110, 60, "workers", "drain → upgrade", fill="#A04832", label_color="#FFFFFF")}
        {_box(40, 150, 640, 50, "smoke test pass · v1.36 cluster Ready", "rollback path: snapshot restore", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V8 = Animation(
    h2="Upgrade walk — v1.35 → v1.36",
    intro="One minor at a time, in order.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_V8,
    initial_packet_xy=(95, 100),
    initial_readout='<strong>Watching:</strong> a controlled minor upgrade.',
    scenes=[
        AnimationScene(
            mode_id="upgrade",
            button_label="▶ minor upgrade",
            mode_label="Mode: minor upgrade with backups + rollback path",
            phases=[
                P(readout='<strong>Step 1.</strong> Cluster on v1.35. Healthy.', move_to=(95, 100), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Take etcd snapshot + Velero backup. Rollback path established.', move_to=(235, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> <code>kubeadm upgrade apply</code> on cp-1.', move_to=(365, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> <code>kubeadm upgrade node</code> + kubelet upgrade on cp-2/3.', move_to=(495, 100), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Drain → upgrade kubelet → uncordon, on each worker.', move_to=(625, 100), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Smoke tests pass. v1.36 cluster Ready.', move_to=(360, 175), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# V9 — kube-bench scoring
SCENE_V9 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "fresh cluster", "untuned", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 110, 60, "kube-bench", "scan", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(310, 30, 130, 50, "78% pass", "many FAILs", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(310, 100, 130, 50, "fix iteratively", "PSA · RBAC · etc", fill="#A04832", label_color="#FFFFFF")}
        {_box(460, 80, 110, 60, "kube-bench rerun", "weekly cron", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(600, 80, 130, 60, "96% pass", "documented exceptions", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V9 = Animation(
    h2="Hardening posture — kube-bench score over time",
    intro="From untuned to defendable in one sprint.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_V9,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> hardening sprint.',
    scenes=[
        AnimationScene(
            mode_id="harden",
            button_label="▶ harden a fresh cluster",
            mode_label="Mode: hardening sprint",
            phases=[
                P(readout='<strong>Step 1.</strong> Fresh kubeadm cluster, no hardening.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Run kube-bench. Initial score 78%; many FAILs.', move_to=(235, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Triage FAILs. Quick wins: PSA labels, anonymous-auth=false, RBAC review.', move_to=(375, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Fix iteratively. Edit static-pod manifests; apply Kyverno; tighten RBAC.', move_to=(375, 125), duration_ms=900),
                P(readout='<strong>Step 5.</strong> kube-bench rerun (weekly cron). 96% pass; documented exceptions for the rest.', move_to=(515, 110), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Score tracked on Grafana; alerts on regression.', move_to=(665, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# V10 — disaster scenarios drill
SCENE_V10 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "drill cluster", "non-prod", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(180, 80, 130, 60, "chaos engineer", "introduces failure", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 80, 130, 60, "on-call recovers", "blind from runbook", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(500, 80, 110, 60, "stopwatch", "T-T-M tracked", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(640, 80, 100, 60, "debrief", "runbook update", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V10 = Animation(
    h2="A chaos drill in motion",
    intro="One scenario from V10 — the cert-expiry recovery.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_V10,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a chaos drill cycle.',
    scenes=[
        AnimationScene(
            mode_id="cert",
            button_label="▶ cert expiry drill",
            mode_label="Mode: cert expiry → kubeadm certs renew all",
            phases=[
                P(readout='<strong>Step 1.</strong> Drill cluster ready. Chaos engineer + on-call paired.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Engineer rotates cert TTL forward. apiserver fails on next restart.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> On-call sees alerts; SSH to CP node; <code>kubeadm certs check-expiration</code>.', move_to=(405, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Run <code>kubeadm certs renew all</code>; restart kubelet; cluster back.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Debrief: timing recorded; runbook updated with the gotcha.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# V11 — capstone end-to-end walk
SCENE_V11 = f'''        {_mode_label()}
        {_box(40, 90, 110, 50, "Phase A", "build", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 110, 50, "Phase B", "stack + harden", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(320, 90, 110, 50, "Phase C", "DR + upgrade", fill="#A04832", label_color="#FFFFFF")}
        {_box(460, 90, 110, 50, "Defense", "peer review", fill="#E8B547", label_color="#5A4F45")}
        {_box(600, 90, 130, 50, "K-VAN-complete", "artifact + drill", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_V11 = Animation(
    h2="The capstone walk — A → B → C → defense",
    intro="Four phases; each gates the next.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_V11,
    initial_packet_xy=(95, 115),
    initial_readout='<strong>Watching:</strong> a complete capstone walk.',
    scenes=[
        AnimationScene(
            mode_id="walk",
            button_label="▶ end-to-end walk",
            mode_label="Mode: A → B → C → defense → K-VAN-complete",
            phases=[
                P(readout='<strong>Phase A.</strong> Architecture doc + Talos bootstrap + Cilium. Cluster Ready.', move_to=(95, 115), duration_ms=900),
                P(readout='<strong>Phase B.</strong> Argo CD App-of-Apps + cluster tuning + hardening. kube-bench &gt; 95%.', move_to=(235, 115), duration_ms=900),
                P(readout='<strong>Phase C.</strong> etcd snapshots + Velero + upgrade rehearsal + 7 DR runbooks.', move_to=(375, 115), duration_ms=900),
                P(readout='<strong>Defense.</strong> Peer review of artifacts + live chaos drill recovery.', move_to=(515, 115), duration_ms=900),
                P(readout='<strong>K-VAN-complete.</strong> Artifacts + reproduced cluster + recovered disaster. Done.', move_to=(665, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


ANIMATIONS = {
    "01": ANIM_V1, "02": ANIM_V2, "03": ANIM_V3, "04": ANIM_V4,
    "05": ANIM_V5, "06": ANIM_V6, "07": ANIM_V7, "08": ANIM_V8,
    "09": ANIM_V9, "10": ANIM_V10, "11": ANIM_V11,
}
