"""Per-module Section 6 animations for K-ADV-DR D1-D5."""

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


def _make(num, h2, intro, scene_body, button_label, mode_label, phases):
    return Animation(
        h2=h2, intro=intro, svg_viewbox="0 0 760 230", svg_body=scene_body,
        initial_packet_xy=(115, 110), initial_readout=f'<strong>Watching:</strong> {h2.lower()}.',
        scenes=[AnimationScene(mode_id=f"d{num}", button_label=button_label, mode_label=mode_label, phases=phases)],
    )


SCENE_D1 = f'''        {_mode_label()}
        {_box(40, 70, 180, 80, "etcd snapshot", "etcdctl snapshot save", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(240, 70, 180, 80, "Velero backup", "+CSI snapshots", fill="#5DCAA5", label_color="#1F2433")}
        {_box(440, 70, 180, 80, "Kasten K10", "app-aware backup", fill="#FF9900", label_color="#1F2433")}
        {_box(640, 70, 80, 80, "CloudCasa", "SaaS DR", fill="#5A6B81", label_color="#FBF1D6")}'''
ANIM_D1 = _make(1, "Backup tools — etcd / Velero / K10 / CloudCasa",
    "Four backup paths — pick by integration + ops appetite.",
    SCENE_D1, "▶ backup tools tour", "Mode: backup options",
    [P(readout='<strong>Step 1.</strong> etcd snapshot — control-plane state; foundation for cluster-rebuild.', move_to=(130, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> Velero — workload + PVC backup; CSI snapshots; Restic / Kopia.', move_to=(330, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Kasten K10 — app-aware backup; commercial; richer policies.', move_to=(530, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> CloudCasa — SaaS DR-as-a-service; managed.', move_to=(680, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_D2 = f'''        {_mode_label()}
        {_box(40, 70, 200, 80, "destroyed cluster", "total loss", fill="#A04832", label_color="#FBF1D6")}
        {_box(260, 70, 200, 80, "rebuild cluster", "Terraform / Crossplane / IaC", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(480, 70, 240, 80, "GitOps recovery + Velero restore", "Argo CD syncs + PVC restore", fill="#5DCAA5", label_color="#1F2433")}'''
ANIM_D2 = _make(2, "GitOps-driven recovery — rebuild from Git + backups",
    "Cluster gone → rebuild via IaC → GitOps syncs apps → Velero restores PVCs.",
    SCENE_D2, "▶ GitOps recovery", "Mode: cluster rebuild",
    [P(readout='<strong>Step 1.</strong> Cluster destroyed (region outage / bad upgrade / human error).', move_to=(140, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> Rebuild cluster via Terraform / Crossplane (5-15 min).', move_to=(360, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> GitOps (Argo CD) syncs apps from Git; Velero restores PVCs.', move_to=(600, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_D3 = f'''        {_mode_label()}
        {_box(40, 70, 200, 80, "primary region", "us-east-1", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(260, 70, 200, 80, "DR region", "us-west-2", fill="#5DCAA5", label_color="#1F2433")}
        {_box(480, 70, 240, 80, "RPO + RTO + restore-test", "measured + practiced", fill="#FF9900", label_color="#1F2433")}'''
ANIM_D3 = _make(3, "Cross-region DR — RPO + RTO + restore testing",
    "Primary region outage → DR region active; RPO + RTO targets met.",
    SCENE_D3, "▶ cross-region DR walk", "Mode: cross-region failover",
    [P(readout='<strong>Step 1.</strong> Primary region (us-east-1) outage.', move_to=(140, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> DR region (us-west-2) activates; cluster + apps + state restored.', move_to=(360, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> RPO (data loss window) + RTO (recovery time) measured against targets.', move_to=(600, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_D4 = f'''        {_mode_label()}
        {_box(40, 70, 170, 80, "Secrets recovery", "Vault snapshot / KMS", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(225, 70, 170, 80, "DNS failover", "Route 53 / Azure DNS", fill="#5DCAA5", label_color="#1F2433")}
        {_box(410, 70, 170, 80, "stateful workload DR", "DB replication + restore", fill="#FF9900", label_color="#1F2433")}
        {_box(595, 70, 125, 80, "managed-svc DR limits", "RDS / Cosmos / Spanner", fill="#5A6B81", label_color="#FBF1D6")}'''
ANIM_D4 = _make(4, "Secret + DNS + stateful + managed-svc DR",
    "Each subsystem has its own DR pattern + limit.",
    SCENE_D4, "▶ specialty DR walk", "Mode: per-subsystem DR",
    [P(readout='<strong>Step 1.</strong> Secrets recovery — Vault snapshot + KMS key restoration.', move_to=(125, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> DNS failover — Route 53 / Azure DNS health check + automatic record swap.', move_to=(310, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Stateful workload DR — DB replication (multi-AZ / cross-region); restore-tested.', move_to=(495, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> Managed-service DR — RDS / Cosmos / Spanner have built-in DR; understand limits.', move_to=(660, 110), duration_ms=900, pause_after_ms=2200)])


SCENE_D5 = f'''        {_mode_label()}
        {_box(40, 70, 130, 60, "Git source", "every config", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(190, 70, 130, 60, "backups", "Velero + DB", fill="#5DCAA5", label_color="#1F2433")}
        {_box(340, 70, 130, 60, "registry", "OCI artifacts", fill="#FF9900", label_color="#1F2433")}
        {_box(490, 70, 130, 60, "secrets", "Vault snapshot", fill="#A04832", label_color="#FBF1D6")}
        {_box(640, 70, 80, 60, "DNS", "Route 53", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "destroy cluster + rebuild from these 5 sources; runbook + drill quarterly", "total-loss drill", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_D5 = _make(5, "Total-loss drill — rebuild from 5 sources",
    "Destroy cluster; rebuild from Git + backups + registry + secrets + DNS.",
    SCENE_D5, "▶ total-loss drill", "Mode: capstone rebuild",
    [P(readout='<strong>Phase A.</strong> Cluster destroyed (intentional drill or real loss).', move_to=(105, 100), duration_ms=900),
     P(readout='<strong>Phase B.</strong> Provision new cluster via Terraform / Crossplane (5-15 min).', move_to=(255, 100), duration_ms=900),
     P(readout='<strong>Phase C.</strong> GitOps sync from Git source-of-truth; apps materialise.', move_to=(405, 100), duration_ms=900),
     P(readout='<strong>Phase D.</strong> Velero restores PVCs from backup; DB restored from snapshot.', move_to=(555, 100), duration_ms=900),
     P(readout='<strong>Phase E.</strong> Vault snapshot restored; secrets re-injected via ESO; DNS swapped.', move_to=(680, 100), duration_ms=900),
     P(readout='<strong>Phase F.</strong> Cluster live within RTO; data within RPO; runbook validated.', move_to=(380, 185), duration_ms=900, pause_after_ms=2400)])


ANIMATIONS = {"01": ANIM_D1, "02": ANIM_D2, "03": ANIM_D3, "04": ANIM_D4, "05": ANIM_D5}
