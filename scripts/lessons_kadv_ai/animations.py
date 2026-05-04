"""Per-module Section 6 animations for K-ADV-AI I1-I8."""

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
        h2=h2, intro=intro,
        svg_viewbox="0 0 760 230", svg_body=scene_body,
        initial_packet_xy=(115, 110), initial_readout=f'<strong>Watching:</strong> {h2.lower()}.',
        scenes=[AnimationScene(mode_id=f"i{num}", button_label=button_label, mode_label=mode_label, phases=phases)],
    )


SCENE_I1 = f'''        {_mode_label()}
        {_box(40, 70, 180, 80, "GPU node", "NVIDIA H100", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(240, 70, 180, 80, "device plugin / GPU Op", "advertises GPU resources", fill="#5DCAA5", label_color="#1F2433")}
        {_box(440, 70, 180, 80, "MIG / DRA", "slice GPU into eyepieces", fill="#FF9900", label_color="#1F2433")}
        {_box(640, 70, 80, 80, "Pod schedules", "with GPU", fill="#5A6B81", label_color="#FBF1D6")}'''
ANIM_I1 = _make(1, "GPU node → device plugin → DRA → Pod",
    "GPU node advertises; DRA gives shared / multi-vendor slices; Pod requests + schedules.",
    SCENE_I1, "▶ GPU scheduling walk", "Mode: GPU resource scheduling",
    [P(readout='<strong>Step 1.</strong> GPU node joins; NVIDIA driver + container runtime configured.', move_to=(130, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> NVIDIA device plugin (or GPU Operator) advertises <code>nvidia.com/gpu</code> resources.', move_to=(330, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> MIG (Multi-Instance GPU) or DRA slices GPU into shareable units.', move_to=(530, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> Pod requests <code>nvidia.com/gpu: 1</code> or DRA claim; scheduler places.', move_to=(680, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_I2 = f'''        {_mode_label()}
        {_box(40, 70, 200, 80, "ResourceFlavor + ClusterQueue", "Kueue capacity model", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(260, 70, 200, 80, "LocalQueue + Workload", "tenant submits", fill="#5DCAA5", label_color="#1F2433")}
        {_box(480, 70, 240, 80, "Volcano gang scheduling", "all-or-nothing", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "MultiKueue federates fleets — submit once; runs in any cluster with capacity", "multi-cluster batch", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_I2 = _make(2, "Kueue admits + Volcano gangs",
    "Tenant submits; Kueue admits per quota; Volcano schedules all-or-nothing; MultiKueue federates clusters.",
    SCENE_I2, "▶ batch + gang walk", "Mode: Kueue + Volcano + MultiKueue",
    [P(readout='<strong>Step 1.</strong> Kueue ResourceFlavor + ClusterQueue model the cluster\'s capacity.', move_to=(140, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> Tenant submits Workload to LocalQueue; Kueue admits per quota.', move_to=(360, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Volcano gang-schedules — N Pods start together (no partial start).', move_to=(600, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> MultiKueue federates: submit once; run in any cluster with capacity.', move_to=(380, 185), duration_ms=900, pause_after_ms=2000)])


SCENE_I3 = f'''        {_mode_label()}
        {_box(40, 70, 180, 80, "KubeRay", "Ray on K8s", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(240, 70, 180, 80, "Kubeflow", "training / pipelines", fill="#5DCAA5", label_color="#1F2433")}
        {_box(440, 70, 180, 80, "KServe", "inference + autoscale", fill="#FF9900", label_color="#1F2433")}
        {_box(640, 70, 80, 80, "JobSet", "multi-pod jobs", fill="#5A6B81", label_color="#FBF1D6")}'''
ANIM_I3 = _make(3, "Research-hall tools — KubeRay / Kubeflow / KServe / JobSet",
    "Pick the tool by ML phase: distributed compute / pipelines / inference / multi-pod jobs.",
    SCENE_I3, "▶ research-hall tour", "Mode: ML stack",
    [P(readout='<strong>Step 1.</strong> KubeRay = Ray on K8s; distributed compute, RLlib, training.', move_to=(130, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> Kubeflow = training jobs + pipelines + Notebooks.', move_to=(330, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> KServe = inference + autoscaling + canary.', move_to=(530, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> JobSet = multi-pod batch (gang-scheduled compatible).', move_to=(680, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_I4 = f'''        {_mode_label()}
        {_box(40, 70, 130, 80, "model artifact", "OCI / S3", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(190, 70, 130, 80, "vLLM / TGI", "high-throughput", fill="#5DCAA5", label_color="#1F2433")}
        {_box(340, 70, 130, 80, "Triton", "multi-framework", fill="#FF9900", label_color="#1F2433")}
        {_box(490, 70, 130, 80, "NIM Operator", "NVIDIA-managed", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(640, 70, 80, 80, "llm-d", "K8s-native", fill="#A04832", label_color="#FBF1D6")}'''
ANIM_I4 = _make(4, "LLM serving — vLLM / TGI / Triton / NIM / llm-d",
    "Five inference servers; pick by throughput + framework + ops model.",
    SCENE_I4, "▶ LLM serving tour", "Mode: LLM serving options",
    [P(readout='<strong>Step 1.</strong> Model artifact from OCI registry / S3 / model store.', move_to=(105, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> vLLM / TGI = high-throughput open-source; PagedAttention + continuous batching.', move_to=(255, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> NVIDIA Triton = multi-framework (TF / PyTorch / ONNX / TensorRT).', move_to=(405, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> NIM Operator = NVIDIA-managed inference; commercial.', move_to=(555, 110), duration_ms=900),
     P(readout='<strong>Step 5.</strong> llm-d = K8s-native LLM serving framework (newer).', move_to=(680, 110), duration_ms=900, pause_after_ms=2200)])


SCENE_I5 = f'''        {_mode_label()}
        {_box(40, 70, 200, 80, "client request", "with prompt + budget", fill="#5DCAA5", label_color="#1F2433")}
        {_box(260, 70, 220, 80, "AI Gateway (Envoy AI / Kong AI)", "model routing + auth + rate", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(500, 70, 220, 80, "model backend", "vLLM / Triton / NIM", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "AI Gateway adds: per-model auth + rate + budget + safety + observability", "L7 LLM features", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_I5 = _make(5, "AI Gateway routes prompt + applies policy",
    "Client → AI Gateway (auth + rate + safety) → model backend.",
    SCENE_I5, "▶ AI Gateway path", "Mode: AI Gateway L7 LLM",
    [P(readout='<strong>Step 1.</strong> Client request with prompt + budget header + auth.', move_to=(140, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> AI Gateway routes per model name + tenant + cost budget.', move_to=(370, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Backend (vLLM / Triton / NIM) generates; tokens stream.', move_to=(610, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> Gateway applies safety filter + cost log + observability.', move_to=(380, 185), duration_ms=900, pause_after_ms=2000)])


SCENE_I6 = f'''        {_mode_label()}
        {_box(40, 70, 180, 80, "RDMA / EFA fabric", "low-latency interconnect", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(240, 70, 180, 80, "JuiceFS / Alluxio", "shared model storage", fill="#5DCAA5", label_color="#1F2433")}
        {_box(440, 70, 180, 80, "OCI artifacts (models)", "OCI registry + ggml / safetensors", fill="#FF9900", label_color="#1F2433")}
        {_box(640, 70, 80, 80, "GPU nodes", "consume", fill="#5A6B81", label_color="#FBF1D6")}'''
ANIM_I6 = _make(6, "High-speed fabric + storage for AI",
    "RDMA / EFA for inter-GPU; JuiceFS / Alluxio for model loading; OCI artifacts for distribution.",
    SCENE_I6, "▶ AI infra tour", "Mode: AI fabric + storage",
    [P(readout='<strong>Step 1.</strong> RDMA / EFA connects GPU nodes for collective ops.', move_to=(130, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> JuiceFS / Alluxio = shared model store; load once cache everywhere.', move_to=(330, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> OCI artifacts (models as OCI images) = standardized distribution.', move_to=(530, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> GPU nodes pull + load; warm cache speeds startup.', move_to=(680, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_I7 = f'''        {_mode_label()}
        {_box(40, 70, 200, 80, "GPU sharing strategies", "MIG / time-slicing / DRA", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(260, 70, 200, 80, "tenant isolation", "namespace + Quota", fill="#5DCAA5", label_color="#1F2433")}
        {_box(480, 70, 240, 80, "cost optimisation", "Spot GPU + idle reclaim + queue", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "tenant-fair sharing of expensive GPUs; secure isolation; cost in budget", "operational fabric", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_I7 = _make(7, "GPU sharing + multi-tenant + cost",
    "MIG / time-slicing for sharing; Quota for tenancy; Spot + idle reclaim for cost.",
    SCENE_I7, "▶ shared-GPU walk", "Mode: GPU sharing economics",
    [P(readout='<strong>Step 1.</strong> MIG / time-slicing / DRA make GPUs shareable.', move_to=(140, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> Per-tenant Quota + namespace isolation.', move_to=(360, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Spot GPU + idle reclaim + Kueue queue = budget-friendly.', move_to=(600, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_I8 = f'''        {_mode_label()}
        {_box(40, 70, 130, 60, "GPU + DRA", "I1", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(190, 70, 130, 60, "Kueue + Volcano", "I2", fill="#5DCAA5", label_color="#1F2433")}
        {_box(340, 70, 130, 60, "KServe + JobSet", "I3", fill="#FF9900", label_color="#1F2433")}
        {_box(490, 70, 130, 60, "vLLM + NIM", "I4", fill="#A04832", label_color="#FBF1D6")}
        {_box(640, 70, 80, 60, "AI Gw", "I5", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "+ RDMA + JuiceFS + multi-tenant + cost optimization + observability", "I6 + I7 + ops", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_I8 = _make(8, "Operating Observatory — every K-ADV-AI concept",
    "Full reference AI inference platform.",
    SCENE_I8, "▶ full reference observatory", "Mode: capstone AI platform",
    [P(readout='<strong>Phase A.</strong> GPU nodes + DRA + GPU Operator.', move_to=(105, 100), duration_ms=900),
     P(readout='<strong>Phase B.</strong> Kueue admission + Volcano gang scheduling + MultiKueue federation.', move_to=(255, 100), duration_ms=900),
     P(readout='<strong>Phase C.</strong> KServe inference + JobSet batch + Kubeflow pipelines.', move_to=(405, 100), duration_ms=900),
     P(readout='<strong>Phase D.</strong> vLLM / Triton / NIM serving with autoscale.', move_to=(555, 100), duration_ms=900),
     P(readout='<strong>Phase E.</strong> AI Gateway: per-model auth + rate + safety + observability.', move_to=(680, 100), duration_ms=900),
     P(readout='<strong>Phase F.</strong> RDMA + JuiceFS + multi-tenant Quota + Spot + cost dashboards.', move_to=(380, 185), duration_ms=900, pause_after_ms=2400)])


ANIMATIONS = {"01": ANIM_I1, "02": ANIM_I2, "03": ANIM_I3, "04": ANIM_I4, "05": ANIM_I5, "06": ANIM_I6, "07": ANIM_I7, "08": ANIM_I8}
