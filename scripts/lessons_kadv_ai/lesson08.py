"""K-ADV-AI I8 — Capstone: production AI inference platform."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Capstone AI inference platform."><rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Operating Observatory · K-Observatory — every K-ADV-AI concept woven</text><rect x="40" y="70" width="130" height="60" rx="10" fill="#3F4A5E"/><text x="105" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">GPU + DRA</text><rect x="190" y="70" width="130" height="60" rx="10" fill="#5DCAA5"/><text x="255" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">Kueue + Volcano</text><rect x="340" y="70" width="130" height="60" rx="10" fill="#FF9900"/><text x="405" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#1F2433">KServe + vLLM</text><rect x="490" y="70" width="130" height="60" rx="10" fill="#A04832"/><text x="555" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">AI Gateway</text><rect x="640" y="70" width="80" height="60" rx="10" fill="#5A6B81"/><text x="680" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">RDMA</text><rect x="40" y="160" width="680" height="60" rx="10" fill="#FBE8DC" stroke="#A04832"/><text x="380" y="182" text-anchor="middle" font-size="11" font-weight="700" fill="#A04832">+ JuiceFS + multi-tenant + Spot + cost dashboards + observability</text></svg>"""


LESSON = LessonSpec(
    num="08", title_short="capstone AI platform", title_full="I8 · Capstone — Production AI Inference Platform",
    title_html="K-ADV-AI I8 · Capstone", module_eyebrow="Module I8 · Operating Observatory — every K-ADV-AI concept woven",
    hero_sub_html='Reference architecture: <strong>GPU nodes + DRA + GPU Operator + MIG</strong> for capacity; <strong>Kueue + Volcano + MultiKueue</strong> for batch + admission + gang + federation; <strong>KubeRay + Kubeflow + KServe + JobSet</strong> for the ML stack; <strong>vLLM / Triton / NIM</strong> for LLM serving; <strong>AI Gateway</strong> (Envoy AI) for L7 LLM features; <strong>RDMA / EFA + GPUDirect Storage + JuiceFS / Alluxio + OCI artifacts</strong> for fabric + storage; <strong>multi-tenant Quota + MIG isolation + Spot + chargeback + dashboards</strong> for governance + economics.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. New product launches in 6 hours; AI inference platform must serve 10K rps with 99.9% SLA + multi-tenant + cost-controlled + observable. <em>The capstone shows the assembly that makes that possible</em>.",
    stamp_html="<strong>Operating Observatory: GPU + DRA + Kueue + Volcano + KServe + vLLM + AI Gateway + RDMA + JuiceFS + OCI artifacts + multi-tenant + Spot + chargeback. Every K-ADV-AI concept woven into one production AI inference platform.</strong>",
    district_pin="kai-array08", district_label="Operating Observatory",
    sections=[
        Section(eyebrow="Section 1.1 · capacity + scheduling",
            h2="GPU + Kueue + Volcano + MIG",
            body_html="""    <p><strong>GPU pools</strong>: H100 (training + large LLM), A100 (training + medium LLM), L40 / G5 (inference + light LLM), Spot G6 (fault-tolerant batch). DRA + MIG enabled cluster-wide.</p>
    <p><strong>Kueue + Volcano</strong>: per-team ClusterQueue with cohort lending; gang scheduling for distributed training; MultiKueue federates training across regions for capacity.</p>
    <p><strong>Per-tenant Quota</strong>: gold (10 H100) / silver (4) / bronze (1); MIG-sized inference quotas (1g.10gb)."""),
        Section(eyebrow="Section 1.2 · ML stack + serving",
            h2="KServe + vLLM + Kubeflow + KubeRay",
            body_html="""    <p><strong>Inference</strong>: KServe InferenceService wrapping vLLM ServingRuntime for LLMs; Triton ServingRuntime for non-LLM; autoscale via Knative or HPA.</p>
    <p><strong>Training</strong>: Kubeflow Training Operator (PyTorchJob / TFJob / MPIJob); Kubeflow Pipelines for DAGs; Katib for HPO; Model Registry for versioning.</p>
    <p><strong>Distributed compute</strong>: KubeRay (Ray Train / Tune / RLlib) for distributed Python.</p>
    <p><strong>Multi-pod jobs</strong>: JobSet primitive integrated with Kueue + Volcano."""),
        Section(eyebrow="Section 1.3 · L7 + fabric + storage",
            h2="AI Gateway + RDMA / EFA + JuiceFS + OCI",
            body_html="""    <p><strong>AI Gateway</strong>: Envoy AI Gateway in front of all LLM serving. Per-tenant token rate limit + cost budget; safety filters (Llama Guard); semantic cache (Redis + embedding); multi-provider failover (local LLM ↔ OpenAI ↔ Anthropic).</p>
    <p><strong>RDMA / EFA</strong>: H100 nodes interconnected via EFA on AWS / IB on-prem. Distributed training collective ops at line rate.</p>
    <p><strong>GPUDirect Storage + JuiceFS</strong>: large datasets streamed direct to GPU; models cached cluster-wide via JuiceFS.</p>
    <p><strong>OCI artifacts</strong>: models + SBOM + Cosign signature in Harbor registry; pulled via init-container."""),
        Section(eyebrow="Section 1.4 · governance + economics + ops",
            h2="Multi-tenant + Spot + chargeback + observability + runbooks",
            body_html="""    <p><strong>Multi-tenant</strong>: namespace + RBAC + NetPol + Quota + MIG isolation per K-ADV-SEC; AI Gateway per-tenant token budget.</p>
    <p><strong>Cost</strong>: Spot fleet for fault-tolerant batch; Kubecost per-tenant chargeback; budget alerts; idle reclaim; right-sizing campaigns.</p>
    <p><strong>Observability</strong>: DCGM metrics + Prometheus; per-Service KServe metrics (TTFT / TPOT / queue / cache hit); LLM-specific tracing via OpenTelemetry; Grafana / Datadog dashboards in Backstage per service.</p>
    <p><strong>Runbooks</strong>: GPU-OOM; KV-cache exhaustion; collective op latency; AI Gateway rate limit hit; Spot interruption cascade. Tested via quarterly game days.</p>"""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why include both Kueue + Volcano in capstone?",
            options=[("Redundancy.", False), ("Kueue admits + manages quota; Volcano gang-schedules multi-Pod jobs. Different concerns; both required for batch ML at scale.", True), ("Required by NVIDIA.", False)],
            feedback="Kueue + Volcano are complementary. Kueue handles admission + cohort + preemption; Volcano handles gang scheduling. Together: batch admission + gang."),
        3: PauseCheck(question="Why per-tenant chargeback in capstone?",
            options=[("Cost only.", False), ("Cost transparency drives tenant self-tuning (right-sizing / MIG / Spot adoption); aligns engineering + finance.", True), ("Required by HIPAA.", False)],
            feedback="GPUs are the most expensive resource. Without chargeback, tenants don\'t self-optimise; cost grows. Chargeback is the incentive layer."),
    },
    before_after_before='<p>Pre-capstone: bespoke ML setups; per-team GPU sprawl; no quota; no isolation; no AI Gateway; cost surprises; outages frequent.</p>',
    before_after_after='<p>Operating Observatory: every K-ADV-AI concept woven. Multi-tenant ML platform with GPU sharing + Kueue admission + KServe inference + AI Gateway + RDMA fabric + Spot + chargeback. New tenant in &lt; 1 day; SLA met; cost controlled.</p>',
    before_after_caption='<p class="ba-caption"><em>The architecture is the assembly; the operational rhythm is the discipline.</em></p>',
    analogy_intro_html='''<p>The Operating Observatory is K-Observatory at scale. Every telescope (GPU) is multi-tenant via MIG eyepieces; every astronomer\'s session is queue-managed (Kueue + Volcano); inference goes through the Triage Desk (AI Gateway); collective observations use the Optical Fiber Network (RDMA / EFA); the Cache Room (JuiceFS) holds star maps; the Sharing Committee bills per group + reclaims idle telescopes.</p>
    <p>The Master Astronomer (you) reviews monthly cost reports + quarterly SLO retros + game-day exercises.</p>''',
    translation_rows=[
        ("Telescope farm + eyepieces", "GPU pools + MIG"),
        ("Astronomer queue + admission", "Kueue + Volcano"),
        ("Research-hall workshops", "KubeRay + Kubeflow"),
        ("Rendering halls", "KServe + vLLM"),
        ("Triage desk", "AI Gateway (Envoy AI)"),
        ("Optical fibers", "RDMA / EFA / IB"),
        ("Shared star-map cache", "JuiceFS / Alluxio"),
        ("Catalogue cards", "OCI artifacts (models)"),
        ("Sharing Committee + bills", "Multi-tenant Quota + chargeback"),
    ],
    analogy_stops="A real observatory has fixed assets; AI infra evolves continuously — new GPU models, new servers, new gateways. The capstone is a snapshot.",
    eli5="Big telescope farm + queue + research labs + rendering halls + triage desk + fast wires + shared cache + catalogue + bills + drills. Every piece works together.",
    eli10="<strong>Capacity</strong>: GPU + DRA + GPU Operator + MIG. <strong>Scheduling</strong>: Kueue + Volcano + MultiKueue. <strong>ML stack</strong>: KubeRay + Kubeflow + KServe + JobSet. <strong>Serving</strong>: vLLM + Triton + NIM. <strong>L7</strong>: AI Gateway. <strong>Fabric</strong>: RDMA / EFA + GPUDirect Storage. <strong>Storage</strong>: JuiceFS / Alluxio. <strong>Distribution</strong>: OCI artifacts. <strong>Governance</strong>: multi-tenant Quota + MIG isolation + Spot + chargeback. <strong>Ops</strong>: DCGM + Prometheus + per-service dashboards + runbooks + game days.",
    scenarios=[
        Scenario(name="Production launch — 10K rps with full stack", body="LLM platform launches: vLLM behind KServe behind Envoy AI Gateway; H100 fleet with MIG for inference; Kueue admission; semantic cache; multi-provider failover. Day-1 SLA met; per-tenant chargeback in P&L."),
        Scenario(name="Multi-region failover via MultiKueue", body="us-east-1 GPU capacity exhausted; MultiKueue routes new training jobs to eu-west-1 H100 pool; tenants see no service interruption."),
        Scenario(name="Cost optimisation campaign", body="Quarterly review: top spenders right-sized via MIG; fault-tolerant training migrated to Spot; aggregate GPU bill dropped 35%."),
        Scenario(name="Game day — Spot interruption cascade", body="Simulated mass Spot reclaim; checkpointing + Kueue requeue + MultiKueue failover absorbed gracefully. Runbook validated."),
    ],
    misconceptions=[
        Misconception(myth="\"This is over-engineered for &lt; 10 GPU clusters.\"", truth="Some pieces (DRA, MIG, AI Gateway, JuiceFS) earn at small scale. Skip what isn\'t needed; adopt as scale + tenancy + cost demands."),
        Misconception(myth="\"AI infra is fundamentally different from K8s.\"", truth="AI infra extends K8s via operators + plugins. Same K8s primitives + AI-specific extensions. K8s is the substrate."),
        Misconception(myth="\"Once built, the platform runs itself.\"", truth="Operational rhythm (game days + cost reviews + dashboards) is non-optional. Without rhythm, AI infra rots fast."),
    ],
    flashcards=[
        Flashcard(front="Capstone\'s 8 layers?", back="<strong>Capacity</strong> (GPU + DRA + MIG), <strong>scheduling</strong> (Kueue + Volcano + MultiKueue), <strong>ML stack</strong> (Ray + Kubeflow + KServe + JobSet), <strong>serving</strong> (vLLM / Triton / NIM), <strong>L7</strong> (AI Gateway), <strong>fabric</strong> (RDMA / EFA / GDS), <strong>storage</strong> (JuiceFS / Alluxio + OCI), <strong>governance</strong> (multi-tenant + Spot + chargeback)."),
        Flashcard(front="Per-tenant isolation primitives?", back="Namespace + RBAC + NetPol + GPU Quota + MIG isolation + node taints + AI Gateway token budget."),
        Flashcard(front="Operational rhythm in capstone?", back="Quarterly game days (Spot cascade + GPU OOM + AI Gateway throttle) + monthly cost review + quarterly SLO retro + tenant chargeback."),
        Flashcard(front="Multi-region pattern?", back="MultiKueue federates training across regions; KServe per-region inference + global LB routing."),
        Flashcard(front="LLM serving path in capstone?", back="Client → AI Gateway (auth + budget + safety + cache) → KServe InferenceService → vLLM / Triton / NIM → response stream."),
    ],
    quizzes=[
        Quiz(prompt="Walk a new ML engineer through the capstone in 5 min.",
            answer="\"GPU fleet has H100 (large LLM + training) and L40/G5 (inference + light LLM). MIG splits H100s for inference Pods. Kueue admits jobs per team\'s quota; Volcano gang-schedules distributed training; MultiKueue federates across regions. KubeRay for distributed Python; Kubeflow for training operators + Pipelines + HPO. KServe wraps vLLM / Triton / NIM as InferenceService. AI Gateway in front: per-tenant token budget + safety + semantic cache + multi-provider failover. RDMA / EFA between H100 nodes for collective ops. JuiceFS shared model cache. OCI artifacts for distribution. Cost dashboards per tenant; chargeback monthly; quarterly game days exercise the runbooks. Backstage shows it all in one place.\""),
        Quiz(prompt="A new tenant onboarded; their training jobs underperform. Walk diagnostic.",
            answer="(1) <strong>Quota check</strong>: tenant\'s ClusterQueue full? Cohort spare available? (2) <strong>RDMA</strong>: training using EFA/IB transport? Verify NCCL config. (3) <strong>Storage</strong>: data loading bottleneck? GPUDirect Storage enabled? JuiceFS cache warm? (4) <strong>Gang scheduling</strong>: Volcano PodGroup correct? min-member set? (5) <strong>GPU sharing</strong>: tenant on shared GPUs? Migrate to dedicated for prod. (6) <strong>Profile</strong>: NCCL + CUDA + DCGM utilization to find hotspot."),
        Quiz(prompt="The CFO sees AI infra cost: \"why so much?\" Defend.",
            answer="\"<strong>AI infra is expensive because GPUs are expensive — but the architecture optimises within that constraint.</strong> Three reasons cost is well-managed: (1) <strong>MIG sharing</strong>: H100 cost amortised across 7 tenants per GPU. (2) <strong>Spot fleet</strong>: 60-90% discount for fault-tolerant batch. (3) <strong>Chargeback</strong>: per-tenant visibility drives self-tuning. (4) <strong>RIs/SP</strong>: baseline at 30-50% discount. <strong>Without these</strong>: cost would be 2-3× higher. <strong>Right answer is right-sizing + sharing + chargeback, not cancelling AI</strong>.\"", cyoa=True, cyoa_tag="how the platform engineer answered the CFO"),
    ],
    glossary=[
        GlossaryItem(name="Operating Observatory", definition="Capstone AI inference platform; every K-ADV-AI concept woven."),
        GlossaryItem(name="GPU pool", definition="NodeGroup of GPUs of one model; nodeSelector picks per workload."),
        GlossaryItem(name="MIG inference pool", definition="H100 partitioned to 1g.10gb instances; serves many small inference Pods."),
        GlossaryItem(name="Spot training fleet", definition="Cheaper preemptible GPU fleet; checkpointing handles interruption."),
        GlossaryItem(name="multi-region MultiKueue", definition="Federate training across regions; route per capacity."),
        GlossaryItem(name="per-tenant token budget", definition="AI Gateway enforces per-tenant tokens-per-minute + monthly cost cap."),
        GlossaryItem(name="game day (AI)", definition="Quarterly exercise: GPU OOM, KV-cache exhaustion, Spot cascade, AI Gateway throttle."),
        GlossaryItem(name="chargeback (AI)", definition="GPU cost allocated to consuming team; visible in P&L."),
        GlossaryItem(name="DCGM dashboard", definition="GPU utilization metrics; foundation of right-sizing + idle detection."),
        GlossaryItem(name="model rollout", definition="KServe canary traffic split for new model versions; auto-promote on SLO."),
    ],
    recap_lead="Capstone: GPU + DRA + MIG + Kueue + Volcano + KubeRay + Kubeflow + KServe + vLLM + AI Gateway + RDMA / EFA + JuiceFS + OCI artifacts + multi-tenant Quota + Spot + chargeback + observability + runbooks. Production AI inference platform.",
    recap_next='<strong>K-ADV-AI complete.</strong> 8 modules. From GPU + DRA (I1) to operating observatory (I8). Next K-ADV: <em>K-ADV-DR</em> (K-Lifeboat) — disaster recovery + business continuity.',
)
