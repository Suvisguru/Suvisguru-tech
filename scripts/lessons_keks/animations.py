"""Per-module Section 6 animations for K-EKS E1-E11."""

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


def _mode_label(x=380, y=22):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="13" font-weight="600" fill="#3F4A5E" id="anim-mode-label">Mode</text>'


# E1 — EKS architecture: AWS owns control plane; you own nodes
SCENE_E1 = f'''        {_mode_label()}
        {_box(40, 70, 150, 90, "AWS-managed", "control plane (CP)", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(220, 35, 150, 50, "kube-apiserver", "multi-AZ HA", fill="#A04832", label_color="#FFFFFF")}
        {_box(220, 95, 150, 50, "etcd", "AWS-owned", fill="#A04832", label_color="#FFFFFF")}
        {_box(220, 155, 150, 50, "controllers", "scheduler", fill="#A04832", label_color="#FFFFFF")}
        {_box(420, 70, 150, 90, "Customer-managed", "data plane", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(600, 35, 130, 50, "Auto Mode", "or Karpenter", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(600, 95, 130, 50, "Managed NG", "EC2 ASG", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(600, 155, 130, 50, "Self-managed / Fargate", "edge cases", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}'''

ANIM_E1 = Animation(
    h2="EKS shared responsibility — what AWS runs vs what you run",
    intro="Two halves: AWS runs the control plane; you choose how to run the nodes.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_E1,
    initial_packet_xy=(115, 115),
    initial_readout='<strong>Watching:</strong> the EKS shared-responsibility split.',
    scenes=[
        AnimationScene(
            mode_id="cp",
            button_label="▶ AWS owns the control plane",
            mode_label="Mode: AWS-managed control plane",
            phases=[
                P(readout='<strong>Step 1.</strong> kube-apiserver runs in a multi-AZ AWS-owned VPC.', move_to=(295, 60), duration_ms=900),
                P(readout='<strong>Step 2.</strong> etcd is AWS-owned and AWS-encrypted; you never SSH it.', move_to=(295, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> kube-controller-manager + scheduler also AWS-managed.', move_to=(295, 180), duration_ms=900, pause_after_ms=2000),
            ],
        ),
        AnimationScene(
            mode_id="dp",
            button_label="▶ you own the data plane",
            mode_label="Mode: customer-managed data plane (5 options)",
            phases=[
                P(readout='<strong>Step 1.</strong> Auto Mode: AWS provisions + lifecycles nodes via Karpenter under the hood.', move_to=(665, 60), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Managed Node Groups: AWS manages an EC2 ASG; you pick instance types.', move_to=(665, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Self-managed or Fargate fill the edges (FIPS, custom AMI, sub-second pods).', move_to=(665, 180), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# E2 — EKS Auto Mode: NodePool + NodeClass → consolidated node
SCENE_E2 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "Pod Pending", "needs c-class", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "NodePool", "Auto Mode default", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "Concierge picks", "spot c7g.large", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(340, 100, 130, 50, "node provisioned", "from NodeClass AMI", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "consolidation", "later, AWS re-bins", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "Pod Running", "scheduled", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "auto-cleaned", "in 21 days", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E2 = Animation(
    h2="Auto Mode walks a Pending Pod to a node — and recycles it later",
    intro="One Pending Pod. Auto Mode sizes a node, runs the workload, and consolidates later.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_E2,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> Auto Mode end-to-end: pending → ready → consolidated.',
    scenes=[
        AnimationScene(
            mode_id="provision",
            button_label="▶ Auto Mode provisioning",
            mode_label="Mode: Auto Mode picks node, schedules, consolidates",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod Pending — needs a c-class instance with 4 vCPU.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Auto Mode NodePool sees the unschedulable Pod.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Concierge picks <code>c7g.large</code> spot Graviton from NodePool requirements.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Node provisioned from NodeClass AMI (Bottlerocket); joins the cluster.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Pod Running. Workload settled.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Hours later, consolidation re-bins workloads onto fewer nodes.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 7.</strong> Empty node hits 21-day max lifetime; AWS cleanly drains and replaces it.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# E3 — VPC CNI prefix delegation + ALB + Gateway API
SCENE_E3 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "Internet client", "GET /api", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "ALB / NLB", "AWS LB Controller", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 90, 130, 60, "TargetGroupBinding", "IP-mode targets", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 30, 110, 50, "VPC CNI", "prefix delegation", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 100, 110, 50, "Pod ENI", "real VPC IP", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 170, 110, 50, "VPC Lattice", "service mesh", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(640, 90, 100, 60, "Pod", "200 OK", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E3 = Animation(
    h2="A request travels — Internet → ALB → IP-target → Pod ENI",
    intro="Two networking modes: ALB ingress with IP targets, then a service-mesh hop via VPC Lattice.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_E3,
    initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> a request reach an EKS Pod via AWS LB Controller.',
    scenes=[
        AnimationScene(
            mode_id="alb",
            button_label="▶ ALB → Pod IP target",
            mode_label="Mode: ALB ingress, IP-mode targets, VPC CNI Pod IP",
            phases=[
                P(readout='<strong>Step 1.</strong> Internet client hits the ALB DNS name.', move_to=(95, 120), duration_ms=400),
                P(readout='<strong>Step 2.</strong> ALB created by AWS LB Controller; route table has IP-mode targets.', move_to=(245, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> TargetGroupBinding tracks the live Pod IPs.', move_to=(405, 120), duration_ms=900),
                P(readout='<strong>Step 4.</strong> VPC CNI assigned this Pod a real VPC IP via prefix delegation.', move_to=(555, 55), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Packet hits Pod ENI on the worker node — no NAT, no overlay.', move_to=(555, 125), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Pod returns 200 OK.', move_to=(690, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="lattice",
            button_label="▶ VPC Lattice service hop",
            mode_label="Mode: cross-VPC service hop via VPC Lattice",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod calls a service in another VPC.', move_to=(555, 125), duration_ms=900),
                P(readout='<strong>Step 2.</strong> VPC Lattice fronts the service; no peering needed.', move_to=(555, 195), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Lattice handles auth + retries; response returns to caller.', move_to=(690, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# E4 — Pod Identity vs IRSA + Access Entries vs aws-auth
SCENE_E4 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "kubectl user", "from IAM role", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "EKS Access Entry", "(replaces aws-auth)", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 80, 130, 60, "RBAC", "policy assignment", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(40, 160, 110, 60, "App Pod", "wants S3", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 160, 130, 60, "Pod Identity Agent", "DaemonSet on node", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(340, 160, 130, 60, "STS AssumeRole", "session creds", fill="#A04832", label_color="#FFFFFF")}
        {_box(500, 120, 110, 60, "AWS S3", "GetObject", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 120, 100, 60, "200 OK", "audit logged", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E4 = Animation(
    h2="Two identities — human via Access Entry, Pod via Pod Identity",
    intro="Top track: a human gets cluster access. Bottom track: a Pod calls AWS.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_E4,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> human and Pod identities each grant access cleanly.',
    scenes=[
        AnimationScene(
            mode_id="human",
            button_label="▶ human via Access Entry",
            mode_label="Mode: human auth via EKS Access Entry + RBAC",
            phases=[
                P(readout='<strong>Step 1.</strong> User runs <code>kubectl</code> with their IAM role.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Access Entry maps the IAM principal to a Kubernetes group.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> RBAC assigns roles by group — no aws-auth ConfigMap drift.', move_to=(405, 110), duration_ms=900, pause_after_ms=1800),
            ],
        ),
        AnimationScene(
            mode_id="pod",
            button_label="▶ Pod via Pod Identity",
            mode_label="Mode: Pod identity to AWS via Pod Identity Agent + STS",
            phases=[
                P(readout='<strong>Step 1.</strong> App Pod wants to read an S3 object.', move_to=(95, 190), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Pod Identity Agent (DaemonSet) intercepts the SDK call.', move_to=(245, 190), duration_ms=900),
                P(readout='<strong>Step 3.</strong> STS AssumeRole returns scoped session creds for this Pod\'s role.', move_to=(405, 190), duration_ms=900),
                P(readout='<strong>Step 4.</strong> S3 GetObject succeeds; CloudTrail audits the call.', move_to=(555, 150), duration_ms=900),
                P(readout='<strong>Step 5.</strong> 200 OK back to the Pod.', move_to=(690, 150), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# E5 — EBS vs EFS picking
SCENE_E5 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "PVC submitted", "RWO or RWX?", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "StorageClass picker", "ebs-csi or efs-csi", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "EBS gp3", "RWO · single-AZ", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "EFS", "RWX · multi-AZ", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "FSx Lustre / S3 Mountpoint", "AI workloads", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "WaitForFirstConsumer", "AZ-aligned", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "Pod Running", "PV mounted", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E5 = Animation(
    h2="A PVC picks the right CSI driver",
    intro="Same PVC; two access modes; very different storage backends.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_E5,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> PVC binding flows for different access modes.',
    scenes=[
        AnimationScene(
            mode_id="ebs",
            button_label="▶ RWO → EBS gp3",
            mode_label="Mode: RWO PVC → EBS gp3, AZ-aligned by WaitForFirstConsumer",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod requests a 50 GiB RWO PVC.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> ebs-csi StorageClass is default; binding deferred until Pod scheduled.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Scheduler picks node in us-east-1a; EBS provisions in same AZ.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Volume attached, mounted, Pod Running.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Resize later via VolumeAttributesClass — no remount.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="efs",
            button_label="▶ RWX → EFS",
            mode_label="Mode: RWX PVC → EFS multi-AZ shared filesystem",
            phases=[
                P(readout='<strong>Step 1.</strong> Two Pods in different AZs need the same write path.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> efs-csi StorageClass selected — only RWX option here.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> EFS mount targets exist in every AZ; Pods both mount the same FS.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Both Pods read + write concurrently; performance is per-IOP, not per-throughput.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# E6 — Karpenter spot+graviton
SCENE_E6 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "100 Pending Pods", "burst arrival", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "Karpenter", "watches scheduler", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "spot Graviton", "c7g · 4× vCPU", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "spot interruption", "2 min warning", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(340, 170, 130, 50, "GPU node", "g5 · inf2 · trn1", fill="#A04832", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "consolidation", "re-bin", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(640, 80, 100, 60, "node count ↓", "savings", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E6 = Animation(
    h2="Karpenter handles bursts and saves money on consolidation",
    intro="Burst arrives → Karpenter picks cheapest fit → consolidation re-bins later.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_E6,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a 100-Pod burst handled by Karpenter, then squeezed.',
    scenes=[
        AnimationScene(
            mode_id="burst",
            button_label="▶ burst + consolidation",
            mode_label="Mode: 100 Pods burst, spot Graviton, then consolidation",
            phases=[
                P(readout='<strong>Step 1.</strong> 100 Pods Pending — kube-scheduler can\'t place them.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Karpenter sees the unschedulable set; computes minimum-cost node mix.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Spot Graviton c7g chosen — cheapest fit; 4× vCPU per node.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Workloads run. Some Pods later finish; nodes go partly empty.', duration_ms=400, pause_after_ms=600),
                P(readout='<strong>Step 5.</strong> Consolidation re-packs Pods onto fewer nodes.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Empty nodes drained + terminated. Cost down ~40%.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="interrupt",
            button_label="▶ spot interruption",
            mode_label="Mode: spot interruption with 2-min handler",
            phases=[
                P(readout='<strong>Step 1.</strong> AWS warns: this spot instance reclaimed in 2 minutes.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 2.</strong> aws-node-termination-handler cordons + drains the node.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Karpenter provisions a replacement; Pods reschedule cleanly.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# E7 — security + supply chain
SCENE_E7 = f'''        {_mode_label()}
        {_box(40, 90, 110, 60, "build CI", "image", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 60, "AWS Signer + Cosign", "signs the image", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 130, 50, "Inspector", "scan image", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "Kyverno", "verify signature", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "Bottlerocket node", "minimal AMI", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 90, 110, 60, "Pod Running", "secure", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(640, 90, 100, 60, "GuardDuty", "runtime watch", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E7 = Animation(
    h2="One signed image walks from CI to a guarded node",
    intro="Sign → scan → admission verify → Bottlerocket → GuardDuty runtime monitoring.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_E7,
    initial_packet_xy=(95, 120),
    initial_readout='<strong>Watching:</strong> a hardened deploy path.',
    scenes=[
        AnimationScene(
            mode_id="signed",
            button_label="▶ signed image lifecycle",
            mode_label="Mode: sign → Inspector scan → Kyverno verify → Bottlerocket → GuardDuty",
            phases=[
                P(readout='<strong>Step 1.</strong> CI builds an image; AWS Signer (or Cosign) signs it.', move_to=(245, 120), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Inspector scans the image for CVEs in ECR.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Kyverno admission policy verifies the signature on Pod create.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Pod scheduled on Bottlerocket — minimal-attack-surface AMI.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Pod Running.', move_to=(555, 120), duration_ms=900),
                P(readout='<strong>Step 6.</strong> GuardDuty Runtime Monitoring inspects syscalls live.', move_to=(690, 120), duration_ms=900, pause_after_ms=2400),
            ],
        ),
        AnimationScene(
            mode_id="unsigned",
            button_label="▶ unsigned image rejected",
            mode_label="Mode: unsigned image blocked at admission",
            phases=[
                P(readout='<strong>Step 1.</strong> An unsigned image arrives.', move_to=(245, 120), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Kyverno verify-image policy fires; signature missing.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Pod creation rejected at admission. CloudTrail logs the deny.', duration_ms=400, pause_after_ms=2400),
            ],
        ),
    ],
)


# E8 — Container Insights + AMP + AMG + ADOT
SCENE_E8 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "Pod", "emits metric", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 80, 130, 60, "ADOT collector", "DaemonSet", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 30, 130, 50, "AMP", "Prometheus metrics", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "CloudWatch", "logs + Container Insights", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "X-Ray", "traces", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(500, 80, 110, 60, "AMG dashboard", "joined view", fill="#A04832", label_color="#FFFFFF")}
        {_box(640, 80, 100, 60, "alert fires", "PagerDuty", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E8 = Animation(
    h2="A signal travels from a Pod to PagerDuty",
    intro="ADOT fans out signals; AMG joins them; an alert fires.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_E8,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a metric → ADOT → AMP → AMG → alert.',
    scenes=[
        AnimationScene(
            mode_id="trace",
            button_label="▶ signal flow",
            mode_label="Mode: ADOT collects, AMP/CW/X-Ray store, AMG visualizes, alert fires",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod emits a Prometheus metric + a structured log + a span.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> ADOT collector (per-node DaemonSet) fans out by signal type.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Metric → AMP (managed Prometheus).', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Log → CloudWatch + Container Insights.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Span → X-Ray.', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 6.</strong> AMG dashboard joins the three; an alert rule sees an SLO breach.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 7.</strong> PagerDuty fires; on-call gets paged.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# E9 — EKS upgrade walk
SCENE_E9 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "v1.32 cluster", "current", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(180, 80, 110, 60, "pre-flight", "kube-no-trouble", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(310, 80, 110, 60, "CP upgrade", "AWS-driven", fill="#A04832", label_color="#FFFFFF")}
        {_box(440, 80, 110, 60, "add-ons", "managed bump", fill="#A04832", label_color="#FFFFFF")}
        {_box(570, 80, 110, 60, "node groups", "one MNG at a time", fill="#A04832", label_color="#FFFFFF")}
        {_box(40, 160, 640, 50, "smoke test pass · v1.33 cluster Ready", "rollback path: blue-green new cluster", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E9 = Animation(
    h2="An EKS minor upgrade — v1.32 → v1.33",
    intro="One minor; pre-flight first; CP then add-ons then nodes.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_E9,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a controlled EKS minor upgrade.',
    scenes=[
        AnimationScene(
            mode_id="upgrade",
            button_label="▶ minor upgrade",
            mode_label="Mode: minor upgrade in EKS-blessed order",
            phases=[
                P(readout='<strong>Step 1.</strong> Cluster on v1.32. Healthy.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Pre-flight: kube-no-trouble + Pluto detect deprecated APIs in YAML.', move_to=(235, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> AWS upgrades the control plane in place. ~30 min, no downtime.', move_to=(365, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Bump managed add-ons (VPC CNI, kube-proxy, CoreDNS, EBS CSI).', move_to=(495, 110), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Roll node groups (Auto Mode handles this; otherwise one MNG at a time).', move_to=(625, 110), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Smoke tests pass. v1.33 cluster Ready.', move_to=(360, 185), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# E10 — Pod stuck Pending: classic CNI IP exhaustion → fix
SCENE_E10 = f'''        {_mode_label()}
        {_box(40, 80, 110, 60, "Pod Pending", "no FailedScheduling", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(180, 80, 130, 60, "kubectl describe", "no clear msg", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 30, 130, 50, "VPC CNI logs", "InsufficientFreeAddressesInSubnet", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 100, 130, 50, "subnet utilization", "/26 · 96% used", fill="#A04832", label_color="#FFFFFF")}
        {_box(340, 170, 130, 50, "fix: prefix delegation", "or bigger subnet", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(500, 80, 110, 60, "ConfigMap update", "rolling restart", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(640, 80, 100, 60, "Pod Running", "fixed", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E10 = Animation(
    h2="A Pod stuck Pending — diagnose VPC CNI IP exhaustion",
    intro="Walk the EKS-specific diagnostic path; the kubelet message alone won\'t help.",
    svg_viewbox="0 0 760 240",
    svg_body=SCENE_E10,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a Pending-Pod root cause hunt.',
    scenes=[
        AnimationScene(
            mode_id="diag",
            button_label="▶ diagnose + fix",
            mode_label="Mode: VPC CNI IP exhaustion → prefix delegation",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod stuck Pending; <code>describe</code> shows no FailedScheduling.', move_to=(95, 110), duration_ms=400),
                P(readout='<strong>Step 2.</strong> Check kubectl events on the node — vague.', move_to=(245, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Look at VPC CNI logs: <code>InsufficientFreeAddressesInSubnet</code>.', move_to=(405, 55), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Subnet utilization view in CloudWatch: 96% on a /26.', move_to=(405, 125), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Fix path: enable VPC CNI prefix delegation (or bigger subnet).', move_to=(405, 195), duration_ms=900),
                P(readout='<strong>Step 6.</strong> Apply VPC CNI ConfigMap; rolling restart of aws-node.', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 7.</strong> Pod Running. RCA filed; runbook updated.', move_to=(690, 110), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


# E11 — capstone tower walk
SCENE_E11 = f'''        {_mode_label()}
        {_box(40, 90, 110, 50, "Phase A", "Auto Mode + ALB", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(180, 90, 130, 50, "Phase B", "identity + storage + obs", fill="#5A9F7A", label_color="#FFFFFF")}
        {_box(340, 90, 130, 50, "Phase C", "security + GitOps + DR + upgrade", fill="#A04832", label_color="#FFFFFF")}
        {_box(500, 90, 110, 50, "Defense", "AWS-style review", fill="#E8B547", label_color="#5A4F45")}
        {_box(640, 90, 100, 50, "K-EKS-complete", "tower stands", fill="#E0EFE6", stroke="#3D7857", label_color="#3D7857")}'''

ANIM_E11 = Animation(
    h2="The K-EKS capstone — A → B → C → defense",
    intro="Four phases; each gates the next. The tower stands when all four pass.",
    svg_viewbox="0 0 760 200",
    svg_body=SCENE_E11,
    initial_packet_xy=(95, 115),
    initial_readout='<strong>Watching:</strong> the K-EKS capstone walk.',
    scenes=[
        AnimationScene(
            mode_id="walk",
            button_label="▶ end-to-end walk",
            mode_label="Mode: A → B → C → defense → K-EKS-complete",
            phases=[
                P(readout='<strong>Phase A.</strong> Multi-AZ EKS Auto Mode cluster + AWS LB Controller. Cluster Ready.', move_to=(95, 115), duration_ms=900),
                P(readout='<strong>Phase B.</strong> Pod Identity + EBS/EFS + AMP/AMG/ADOT + control-plane logs.', move_to=(245, 115), duration_ms=900),
                P(readout='<strong>Phase C.</strong> KMS-encrypted secrets, GuardDuty + Inspector, Argo CD, Velero DR, upgrade rehearsal.', move_to=(385, 115), duration_ms=900),
                P(readout='<strong>Defense.</strong> Architecture defended; live drill restores from S3 backup.', move_to=(555, 115), duration_ms=900),
                P(readout='<strong>K-EKS-complete.</strong> Artifact + reproducible cluster + recovered DR. Done.', move_to=(690, 115), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


ANIMATIONS = {
    "01": ANIM_E1, "02": ANIM_E2, "03": ANIM_E3, "04": ANIM_E4,
    "05": ANIM_E5, "06": ANIM_E6, "07": ANIM_E7, "08": ANIM_E8,
    "09": ANIM_E9, "10": ANIM_E10, "11": ANIM_E11,
}
