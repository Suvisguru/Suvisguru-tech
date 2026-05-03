"""Per-module Section 6 animations for K-ECS C1-C10."""

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


# C1 — ECS shapes: Service / Task lifecycle
SCENE_C1 = f'''        {_mode_label()}
        {_box(40, 70, 150, 100, "AWS-managed", "control plane (regional)", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(220, 60, 200, 50, "ECS Service", "keeps N Tasks running", fill="#3878B5", label_color="#FFFFFF")}
        {_box(220, 130, 200, 50, "Task (group of containers)", "Task Definition rev N", fill="#5DCAA5", label_color="#1F2433")}
        {_box(450, 70, 270, 100, "Capacity (EC2 / Fargate / External)", "ECS agent on each host", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}'''

ANIM_C1 = Animation(
    h2="ECS shapes — Service maintains N Tasks across capacity",
    intro="Service → Task → Container → Capacity. The Harbor Master assigns; the Tugboat Skipper places.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_C1,
    initial_packet_xy=(115, 120),
    initial_readout='<strong>Watching:</strong> ECS Service maintains N Tasks across capacity.',
    scenes=[
        AnimationScene(
            mode_id="rolling",
            button_label="▶ Service runs Tasks across capacity",
            mode_label="Mode: Service maintains desired Task count",
            phases=[
                P(readout='<strong>Step 1.</strong> AWS runs the regional ECS control plane.', move_to=(295, 85), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Service holds desired Task count + Task Definition revision.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> Task = group of containers, scheduled together onto capacity.', move_to=(295, 155), duration_ms=900),
                P(readout='<strong>Step 4.</strong> ECS agent on each host pulls the assignment + runs containers.', move_to=(580, 120), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# C2 — Task Definition: family + revision + container definitions
SCENE_C2 = f'''        {_mode_label()}
        {_box(40, 70, 200, 60, "Task Definition", "family: my-app, revision: 42", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(40, 150, 200, 50, "execution role + task role", "ECR pull + app permissions", fill="#FBF1D6", stroke="#8B5A00", label_color="#8B5A00")}
        {_box(280, 70, 200, 60, "container: app", "image, ports, env, healthCheck", fill="#5DCAA5", label_color="#1F2433")}
        {_box(280, 150, 200, 60, "container: log-router", "Firelens sidecar", fill="#7AB3CC", label_color="#FFFFFF")}
        {_box(520, 70, 200, 140, "shared task volumes", "bind / EFS / ephemeral", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_C2 = Animation(
    h2="Task Definition revision applied",
    intro="Family + revision + containers + roles + volumes — one immutable manifest.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_C2,
    initial_packet_xy=(95, 100),
    initial_readout='<strong>Watching:</strong> a Task Definition revision laid out.',
    scenes=[
        AnimationScene(
            mode_id="td",
            button_label="▶ Task Definition walk-through",
            mode_label="Mode: Task Definition shape — family / revision / containers / volumes",
            phases=[
                P(readout='<strong>Step 1.</strong> Family: my-app. Each change creates a new revision.', move_to=(140, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Execution role pulls image + Secrets; task role gives the running app least-privilege AWS access.', move_to=(140, 175), duration_ms=900),
                P(readout='<strong>Step 3.</strong> One container is the app; sidecars (e.g., Firelens) share the Task.', move_to=(380, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Sidecars share network namespace + task-level volumes.', move_to=(380, 180), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Volumes mount on multiple containers — bind, Docker, EFS, FSx, ephemeral.', move_to=(620, 140), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# C3 — Networking: awsvpc ENI + Service Connect + ALB
SCENE_C3 = f'''        {_mode_label()}
        {_box(40, 80, 130, 60, "Internet client", "https://app.example.com", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(190, 80, 130, 60, "ALB", "target type: IP", fill="#FF9900", label_color="#1F2433")}
        {_box(340, 80, 130, 60, "Task ENI", "awsvpc, SG per Task", fill="#5DCAA5", label_color="#1F2433")}
        {_box(490, 80, 230, 60, "Service Connect proxy", "east-west service discovery + LB", fill="#3878B5", label_color="#FFFFFF")}
        {_box(190, 160, 530, 50, "Cloud Map / Service Connect endpoints", "service-to-service lookup", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_C3 = Animation(
    h2="A request reaches an ECS Task in awsvpc + Service Connect",
    intro="Internet → ALB (target type IP) → Task ENI → app; east-west traffic via Service Connect.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_C3,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a request hits an awsvpc Task via ALB target-type IP.',
    scenes=[
        AnimationScene(
            mode_id="north",
            button_label="▶ north–south path (Internet → Task)",
            mode_label="Mode: Internet → ALB → Task ENI",
            phases=[
                P(readout='<strong>Step 1.</strong> Client hits ALB on port 443.', move_to=(255, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> ALB target group has IPs (Task ENIs) — not instances.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> ALB routes to a healthy Task ENI; SG per Task gates traffic.', move_to=(405, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Task receives request; Service Connect proxy is in the loop only for east-west.', move_to=(605, 110), duration_ms=900, pause_after_ms=2000),
            ],
        ),
        AnimationScene(
            mode_id="east",
            button_label="▶ east–west path (Task → Task)",
            mode_label="Mode: Service-A Task → Service Connect → Service-B Task",
            phases=[
                P(readout='<strong>Step 1.</strong> Task A calls service-b.cluster:8080 — Service Connect resolves it.', move_to=(450, 185), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Cloud Map / Service Connect maps name → healthy Task ENIs.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> Service Connect proxy load-balances + retries + emits metrics.', move_to=(605, 110), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# C4 — IAM: execution role pulls ECR; task role lets app call AWS
SCENE_C4 = f'''        {_mode_label()}
        {_box(40, 70, 200, 60, "task execution role", "ECR pull + Secrets fetch + log writer", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(40, 150, 200, 60, "task role", "app → S3, DynamoDB, etc.", fill="#5DCAA5", label_color="#1F2433")}
        {_box(280, 70, 200, 60, "ECR private repo", "image pulled on Task launch", fill="#FF9900", label_color="#1F2433")}
        {_box(280, 150, 200, 60, "Secrets Manager / SSM", "injected as env at start", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}
        {_box(520, 70, 200, 60, "VPC endpoints", "ECR + Logs + SSM private", fill="#7AB3CC", label_color="#FFFFFF")}
        {_box(520, 150, 200, 60, "KMS key", "encrypts secrets + log group", fill="#5E4A8E", label_color="#FBF1D6")}'''

ANIM_C4 = Animation(
    h2="Two roles, one Task — execution role vs task role",
    intro="Execution role launches; task role runs. Different boundaries; different policies.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_C4,
    initial_packet_xy=(95, 100),
    initial_readout='<strong>Watching:</strong> the two IAM roles a Task uses.',
    scenes=[
        AnimationScene(
            mode_id="iam",
            button_label="▶ launch sequence: roles in action",
            mode_label="Mode: execution role → task role",
            phases=[
                P(readout='<strong>Step 1.</strong> ECS agent uses task execution role to pull image from ECR.', move_to=(380, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Execution role also fetches Secrets Manager values + injects as env.', move_to=(380, 180), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Container starts. App now uses task role for its AWS calls.', move_to=(140, 180), duration_ms=900),
                P(readout='<strong>Step 4.</strong> VPC endpoints keep ECR + Logs + SSM traffic on private network; KMS encrypts secrets + logs.', move_to=(620, 180), duration_ms=900, pause_after_ms=2200),
            ],
        ),
    ],
)


# C5 — Storage: bind, Docker volumes, EFS, FSx, ephemeral
SCENE_C5 = f'''        {_mode_label()}
        {_box(40, 70, 150, 60, "ephemeral storage", "Fargate: 20 GiB default → 200 GiB", fill="#7AB3CC", label_color="#FFFFFF")}
        {_box(210, 70, 150, 60, "bind mount", "host path (EC2 launch)", fill="#5DCAA5", label_color="#1F2433")}
        {_box(380, 70, 150, 60, "Docker volume", "EBS/local on EC2 host", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(550, 70, 170, 60, "EFS file system", "RWX-equivalent across Tasks", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 150, 240, 60, "FSx for Windows / NetApp ONTAP", "Windows / NFS-attach", fill="#5E4A8E", label_color="#FBF1D6")}
        {_box(300, 150, 420, 60, "Task: containers share volumes via mountPoints", "task-level volumes definition", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_C5 = Animation(
    h2="Five storage shapes a Task can mount",
    intro="Ephemeral, bind, Docker, EFS, FSx. Pick by lifetime and sharing.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_C5,
    initial_packet_xy=(115, 100),
    initial_readout='<strong>Watching:</strong> the five storage shapes for ECS Tasks.',
    scenes=[
        AnimationScene(
            mode_id="storage",
            button_label="▶ storage shapes walk-through",
            mode_label="Mode: ECS storage options",
            phases=[
                P(readout='<strong>Step 1.</strong> Ephemeral: per-Task scratch (Fargate 20→200 GiB; tunable).', move_to=(115, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Bind mount: EC2 host path (EC2 launch only).', move_to=(285, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Docker volume: EBS / local on EC2 host.', move_to=(455, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> EFS: RWX across Tasks + AZs (the shared-storage answer).', move_to=(635, 100), duration_ms=900),
                P(readout='<strong>Step 5.</strong> FSx for Windows / ONTAP for NTFS or NFS-attach use cases.', move_to=(160, 180), duration_ms=900),
                P(readout='<strong>Step 6.</strong> All flow into Task-level volumes; containers share via mountPoints.', move_to=(510, 180), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# C6 — Deployment: rolling vs blue/green
SCENE_C6 = f'''        {_mode_label()}
        {_box(40, 80, 130, 60, "Service rev N", "8 Tasks running", fill="#5DCAA5", label_color="#1F2433")}
        {_box(190, 80, 130, 60, "Service rev N+1", "rolling start", fill="#FF9900", label_color="#1F2433")}
        {_box(340, 80, 130, 60, "circuit breaker", "watch failures → rollback", fill="#A04832", label_color="#FFFFFF")}
        {_box(490, 80, 130, 60, "ALB target group", "minHealthy / maxPercent", fill="#3878B5", label_color="#FFFFFF")}
        {_box(640, 80, 80, 60, "drain old", "stop drained", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "blue/green via CodeDeploy: two target groups, listener swap, traffic shift", "alternative path", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_C6 = Animation(
    h2="A Service rolls to a new revision (with circuit breaker)",
    intro="ECS rolling deploy: start new, drain old, watch ALB target health; circuit breaker rolls back on failure.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_C6,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> a rolling deployment with circuit breaker.',
    scenes=[
        AnimationScene(
            mode_id="rolling",
            button_label="▶ rolling deploy (default)",
            mode_label="Mode: ECS rolling — start new, drain old",
            phases=[
                P(readout='<strong>Step 1.</strong> Current Service holds 8 Tasks at rev N.', move_to=(105, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> UpdateService → rev N+1 starts new Tasks, respects minimumHealthyPercent.', move_to=(255, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> ALB target health validates; bad rev triggers circuit breaker → rollback.', move_to=(405, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Healthy new Tasks come up; old Tasks drain (deregister + connection drain).', move_to=(555, 110), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Old stopped; Service stable at rev N+1.', move_to=(680, 110), duration_ms=900, pause_after_ms=2000),
            ],
        ),
        AnimationScene(
            mode_id="bluegreen",
            button_label="▶ blue/green (CodeDeploy)",
            mode_label="Mode: CodeDeploy blue/green — two target groups + listener swap",
            phases=[
                P(readout='<strong>Step 1.</strong> Two ALB target groups: blue (live) + green (new).', move_to=(380, 185), duration_ms=900),
                P(readout='<strong>Step 2.</strong> CodeDeploy launches green; canary 10% test traffic.', duration_ms=400, pause_after_ms=900),
                P(readout='<strong>Step 3.</strong> Health gate passes → listener flips to green; blue stays warm for fast rollback.', move_to=(555, 110), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# C7 — Observability: Container Insights + ECS Exec + Firelens + ADOT
SCENE_C7 = f'''        {_mode_label()}
        {_box(40, 70, 200, 60, "ECS Task (app + sidecars)", "stdout / stderr / metrics", fill="#5DCAA5", label_color="#1F2433")}
        {_box(280, 70, 180, 60, "Firelens sidecar", "Fluent Bit / Fluentd", fill="#FF9900", label_color="#1F2433")}
        {_box(500, 70, 220, 60, "logs route → CloudWatch / S3 / Kinesis / OpenSearch", "configurable destinations", fill="#3878B5", label_color="#FFFFFF")}
        {_box(40, 150, 200, 60, "Container Insights", "metrics + dashboards", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(280, 150, 180, 60, "ECS Exec", "interactive shell", fill="#5E4A8E", label_color="#FBF1D6")}
        {_box(500, 150, 220, 60, "ADOT collector + X-Ray", "metrics + traces", fill="#7AB3CC", label_color="#FFFFFF")}'''

ANIM_C7 = Animation(
    h2="Where ECS observability signals go",
    intro="Logs via Firelens; metrics via Container Insights; traces via ADOT + X-Ray; debug via ECS Exec.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_C7,
    initial_packet_xy=(95, 100),
    initial_readout='<strong>Watching:</strong> ECS observability signal paths.',
    scenes=[
        AnimationScene(
            mode_id="obs",
            button_label="▶ signal-path walk-through",
            mode_label="Mode: ECS observability paths",
            phases=[
                P(readout='<strong>Step 1.</strong> App emits stdout + metrics + traces.', move_to=(140, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Firelens sidecar (Fluent Bit) routes logs anywhere.', move_to=(370, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Logs land in CloudWatch / S3 / Kinesis / OpenSearch.', move_to=(610, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Container Insights = preconfigured metrics + dashboards.', move_to=(140, 180), duration_ms=900),
                P(readout='<strong>Step 5.</strong> ECS Exec = interactive shell into a running Task (no SSH).', move_to=(370, 180), duration_ms=900),
                P(readout='<strong>Step 6.</strong> ADOT collector ships metrics + traces; X-Ray for distributed tracing.', move_to=(610, 180), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# C8 — ECS Anywhere: external instance registers
SCENE_C8 = f'''        {_mode_label()}
        {_box(40, 80, 220, 60, "on-prem / edge server", "your hardware, your network", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(280, 80, 200, 60, "SSM agent + ECS agent", "registered with cluster", fill="#5DCAA5", label_color="#1F2433")}
        {_box(500, 80, 220, 60, "ECS control plane (cloud)", "schedules onto external", fill="#3878B5", label_color="#FFFFFF")}
        {_box(40, 160, 680, 50, "limits: no ALB integration on external; awsvpc network mode unsupported; Bridge / Host / None", "pick workloads carefully", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_C8 = Animation(
    h2="On-prem hardware joins an ECS cluster",
    intro="ECS Anywhere — same Task Definitions, hybrid capacity. Bridge use cases only.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_C8,
    initial_packet_xy=(95, 110),
    initial_readout='<strong>Watching:</strong> external server registering with ECS.',
    scenes=[
        AnimationScene(
            mode_id="anywhere",
            button_label="▶ external instance registration",
            mode_label="Mode: ECS Anywhere registration + scheduling",
            phases=[
                P(readout='<strong>Step 1.</strong> SSM activation + ECS agent install on the on-prem server.', move_to=(150, 110), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Server registers as external instance into the cluster.', move_to=(380, 110), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Control plane assigns Tasks; capability filter matches "EXTERNAL".', move_to=(610, 110), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Limits: no awsvpc, no ALB integration on external. Bridge/host network only.', move_to=(380, 185), duration_ms=900, pause_after_ms=2200),
            ],
        ),
    ],
)


# C9 — Troubleshooting: stop reasons + circuit breaker
SCENE_C9 = f'''        {_mode_label()}
        {_box(40, 70, 180, 60, "Task PROVISIONING → PENDING", "ENI, image pull, IAM", fill="#FF9900", label_color="#1F2433")}
        {_box(240, 70, 180, 60, "stoppedReason", "CannotPullContainerError / ResourceInitializationError / OOMK", fill="#A04832", label_color="#FFFFFF")}
        {_box(440, 70, 180, 60, "deployment circuit breaker", "watches failures → auto-rollback", fill="#3878B5", label_color="#FFFFFF")}
        {_box(640, 70, 80, 60, "rollback", "to prior rev", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "Service Connect / ALB target health failure → circuit breaker fires; review CloudWatch + Container Insights", "fast feedback loop", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_C9 = Animation(
    h2="A bad deploy fires the circuit breaker",
    intro="Stuck PENDING → stoppedReason → circuit breaker → rollback. Read the chain top-down.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_C9,
    initial_packet_xy=(95, 100),
    initial_readout='<strong>Watching:</strong> a failure path through ECS.',
    scenes=[
        AnimationScene(
            mode_id="trbl",
            button_label="▶ failure path",
            mode_label="Mode: PENDING → stoppedReason → circuit breaker → rollback",
            phases=[
                P(readout='<strong>Step 1.</strong> Task stuck PENDING — check ENI, image pull, IAM resolution.', move_to=(130, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> If it stops with CannotPullContainerError → ECR perms or VPC endpoints missing.', move_to=(330, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Circuit breaker counts failures within rollout window.', move_to=(530, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Threshold tripped → automatic rollback to prior revision.', move_to=(680, 100), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Postmortem from CloudWatch + Container Insights + Task stoppedReason history.', move_to=(380, 185), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# C10 — Capstone: the full reference harbor
SCENE_C10 = f'''        {_mode_label()}
        {_box(40, 70, 130, 60, "ALB", "blue + green target groups", fill="#FF9900", label_color="#1F2433")}
        {_box(190, 70, 130, 60, "ECS Service", "Fargate, awsvpc, blue/green", fill="#3878B5", label_color="#FFFFFF")}
        {_box(340, 70, 130, 60, "Service Connect", "east-west", fill="#5DCAA5", label_color="#1F2433")}
        {_box(490, 70, 130, 60, "EFS / Secrets / KMS", "RWX + secrets at rest", fill="#5E4A8E", label_color="#FBF1D6")}
        {_box(640, 70, 80, 60, "Insights", "metrics + logs", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "Service Auto Scaling + Capacity Providers (Fargate + Spot) + circuit breaker + CodeDeploy + runbook", "operational fabric", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_C10 = Animation(
    h2="The full reference K-Harbor",
    intro="Multi-service Fargate app: Service Connect + ALB + EFS + Secrets + CodeDeploy + Container Insights + autoscaling + runbook.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_C10,
    initial_packet_xy=(105, 100),
    initial_readout='<strong>Watching:</strong> the full capstone reference architecture.',
    scenes=[
        AnimationScene(
            mode_id="capstone",
            button_label="▶ end-to-end reference harbor",
            mode_label="Mode: full reference K-Harbor",
            phases=[
                P(readout='<strong>Phase A.</strong> Internet → ALB; blue/green target groups via CodeDeploy.', move_to=(105, 100), duration_ms=900),
                P(readout='<strong>Phase B.</strong> ECS Services on Fargate, awsvpc network, ENI per Task.', move_to=(255, 100), duration_ms=900),
                P(readout='<strong>Phase C.</strong> East-west via Service Connect; service discovery + retries + metrics.', move_to=(405, 100), duration_ms=900),
                P(readout='<strong>Phase D.</strong> EFS for shared state; Secrets Manager + KMS for credentials.', move_to=(555, 100), duration_ms=900),
                P(readout='<strong>Phase E.</strong> Container Insights + Firelens for telemetry; ECS Exec for live debug.', move_to=(680, 100), duration_ms=900),
                P(readout='<strong>Phase F.</strong> Service Auto Scaling + Capacity Providers blend Fargate + Fargate Spot; circuit breaker + runbook close the loop.', move_to=(380, 185), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


ANIMATIONS = {
    "01": ANIM_C1,
    "02": ANIM_C2,
    "03": ANIM_C3,
    "04": ANIM_C4,
    "05": ANIM_C5,
    "06": ANIM_C6,
    "07": ANIM_C7,
    "08": ANIM_C8,
    "09": ANIM_C9,
    "10": ANIM_C10,
}
