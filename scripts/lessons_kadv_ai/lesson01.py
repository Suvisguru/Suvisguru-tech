"""K-ADV-AI I1 — GPU nodes + NVIDIA device plugin / GPU Operator + MIG + DRA."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GPU + device plugin + MIG + DRA."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Optics Bay · K-Observatory — GPUs as telescopes; slice + share</text><rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E"/><text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">GPU node</text><text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">H100 / A100 / B200</text><rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5"/><text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">device plugin / GPU Op</text><text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">advertises GPU resources</text><rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900"/><text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">MIG slices</text><text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">7 instances / H100</text><rect x="595" y="70" width="125" height="100" rx="10" fill="#5A6B81"/><text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">DRA</text><text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">multi-vendor</text></svg>"""


LESSON = LessonSpec(
    num="01", title_short="GPU + DRA + MIG", title_full="I1 · GPU Nodes + NVIDIA Device Plugin / GPU Operator + MIG + DRA",
    title_html="K-ADV-AI I1 · GPU + DRA + MIG", module_eyebrow="Module I1 · Optics Bay — GPUs as telescopes; slice + share",
    hero_sub_html='<strong>GPU node</strong>: NVIDIA H100 / H200 / A100 / B200 / GH200; AMD MI300; Google TPU. <strong>NVIDIA device plugin</strong>: advertises <code>nvidia.com/gpu</code>. <strong>GPU Operator</strong>: bundles driver + container runtime + DCGM + MIG manager + node feature discovery. <strong>MIG (Multi-Instance GPU)</strong>: hardware-partition H100 / A100 into up to 7 isolated instances. <strong>DRA (Dynamic Resource Allocation)</strong>: K8s 1.32+ stable; multi-vendor structured parameters; replaces per-vendor device plugins for advanced scheduling.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. ML team\'s training job stuck Pending — \"no GPU available.\" Cluster has 8 H100s; 7 are running tiny inference workloads using whole GPUs. <em>Without MIG / DRA, every Pod takes a whole GPU; sharing is impossible.</em> Today\'s lesson: slice GPUs + use DRA so one telescope serves many observers.",
    stamp_html="<strong>NVIDIA device plugin = baseline; GPU Operator = full stack; MIG = hardware partition for sharing; DRA = K8s-native multi-vendor advanced scheduling. Pick stack by GPU model + sharing needs.</strong>",
    district_pin="kai-array01", district_label="Optics Bay",
    sections=[
        Section(eyebrow="Section 1.1 · GPU node basics", h2="Driver + container runtime + node labels",
            body_html="""    <p>GPU node setup: NVIDIA driver (version-pinned per CUDA + framework); container runtime configured for GPU passthrough (containerd <code>nvidia</code> runtime class); node labels marking GPU model + count.</p>
    <p>Per-cluster: separate GPU node pools (NodePool / MachineSet) labelled <code>accelerator: nvidia-h100</code>; nodeSelector / affinity in Pods picks the right pool.</p>
    <p>Cloud-managed: AWS p5/p4d, GCP A3/A4, Azure ND/NV families. Bring-your-own: Bottlerocket / Ubuntu + GPU Operator handles driver + runtime."""),
        Section(eyebrow="Section 1.2 · NVIDIA device plugin + GPU Operator", h2="Baseline + full-stack",
            body_html="""    <p><strong>NVIDIA device plugin</strong> (DaemonSet): advertises <code>nvidia.com/gpu</code> resources to kubelet. Pod requests <code>resources.limits.nvidia.com/gpu: 1</code>; scheduler places.</p>
    <p><strong>GPU Operator</strong>: opinionated bundle — installs driver (containerized), container runtime, DCGM (metrics), MIG manager, node feature discovery, GPUDirect Storage / RDMA. Recommended for any cluster that takes GPU work seriously.</p>
    <p>Operator-managed driver = no host-level driver install drift; upgrades via Helm + node draining."""),
        Section(eyebrow="Section 1.3 · MIG (Multi-Instance GPU)",
            h2="Hardware partition H100 / A100 into shareable instances",
            body_html="""    <p><strong>MIG</strong>: H100 / A100-only feature. Hardware-partitions one GPU into up to 7 instances (H100: 1g.10gb / 2g.20gb / 3g.40gb / 7g.80gb). Each instance has dedicated SMs + memory + L2 cache; full isolation.</p>
    <p>Configure via MIG manager (in GPU Operator) per node. Pod requests <code>nvidia.com/mig-1g.10gb: 1</code>; scheduler matches instance.</p>
    <p>Trade: one GPU\'s aggregate compute = sum of slices; no oversubscription. Best for many small inference Pods + tenant isolation."""),
        Section(eyebrow="Section 1.4 · DRA (Dynamic Resource Allocation)",
            h2="K8s-native multi-vendor advanced scheduling",
            body_html="""    <p><strong>DRA</strong> (K8s 1.32 stable): the K8s-native replacement for per-vendor device plugins. Vendor ships a DRA driver; declares <em>structured parameters</em> for the device class (memory size, model, MIG profile, RDMA capability). Pods declare claims; scheduler matches.</p>
    <p>Wins: <em>multi-vendor</em> (NVIDIA + AMD + TPU + custom accelerators all use DRA), <em>partial sharing</em> (multiple Pods can claim parts of one device), <em>complex placement</em> (NUMA, RDMA-enabled, same-NUMA Pods together).</p>
    <p>Adoption: NVIDIA DRA driver, AMD DRA driver, GKE TPU DRA driver shipping. New cluster setup increasingly defaults to DRA over per-vendor device plugins."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why use GPU Operator over plain device plugin?",
            options=[("Performance.", False), ("Bundles driver + runtime + MIG manager + DCGM + RDMA — full stack vs baseline.", True), ("Required by NVIDIA.", False)],
            feedback="GPU Operator is opinionated all-in-one. Plain device plugin = just resource advertisement; you wire driver / runtime / MIG manager separately."),
        3: PauseCheck(question="Which use case benefits most from MIG?",
            options=[("Single large training job.", False), ("Many small inference Pods sharing one H100 with isolation.", True), ("Bandwidth-heavy ETL.", False)],
            feedback="MIG hardware-partitions; each instance is isolated. Many small Pods + tenant isolation = perfect fit. Single large job = use whole GPU."),
    },
    before_after_before='<p>Pre-MIG / DRA, every GPU Pod took a whole GPU. Underutilization rampant; cost / utilization mismatch; long pending queues for tiny inference jobs.</p>',
    before_after_after='<p>MIG slices H100 into 7 instances; DRA structured parameters for advanced scheduling; GPU Operator manages full stack. One GPU serves many tenants; utilization rises 3-5×.</p>',
    before_after_caption='<p class="ba-caption"><em>Slice + share + structured-schedule. Expensive GPUs deserve expensive utilization.</em></p>',
    analogy_intro_html='''<p>The Optics Bay houses the observatory\'s telescopes (GPUs). Old practice: each astronomer booked a whole telescope for the night even if they only needed a wide-angle lens. New practice: <strong>MIG</strong> partitions each telescope into separate eyepieces — 7 astronomers can observe at once, each with isolated optics. <strong>DRA</strong> is the booking system that handles many telescope vendors (NVIDIA + AMD + TPU) with one form: \"I need a 80GB-memory eyepiece on a node with low-latency to other observers in my project.\"</p>''',
    translation_rows=[
        ("Telescope", "GPU (H100 / A100 / B200 / TPU)"),
        ("Observatory floor manager", "GPU Operator"),
        ("Telescope availability bell", "NVIDIA device plugin"),
        ("Eyepiece partitions", "MIG instances (1g.10gb / 2g.20gb / etc.)"),
        ("Multi-vendor booking system", "DRA (Dynamic Resource Allocation)"),
        ("Booking form fields", "Structured parameters (memory / RDMA / NUMA)"),
        ("Telescope nightly utilization", "GPU utilization (DCGM metrics)"),
    ],
    analogy_stops="A real telescope has fixed optics; MIG instances are hardware-partitioned but configurable per-node. DRA is structured-API; vendors must ship drivers.",
    eli5="One big telescope can be split into 7 eyepieces so 7 astronomers can use it at once. A booking system handles different telescope brands with one form.",
    eli10="<strong>GPU node</strong>: NVIDIA driver + containerd runtime + node labels. <strong>NVIDIA device plugin</strong>: advertises GPU resources. <strong>GPU Operator</strong>: opinionated bundle (driver + runtime + DCGM + MIG mgr + RDMA). <strong>MIG</strong>: H100/A100 hardware partition (up to 7 instances). <strong>DRA</strong>: K8s-native multi-vendor structured parameters; replaces vendor device plugins for advanced scheduling.",
    scenarios=[
        Scenario(name="Inference fleet — MIG cuts cost 4×", body="Inference workload using one H100 per Pod (most Pods using &lt; 20% GPU). Migrate to MIG 1g.10gb per Pod; one H100 hosts 7 inference Pods; cost / Pod drops 4×."),
        Scenario(name="DRA — multi-vendor cluster", body="Cluster has NVIDIA + AMD GPUs. DRA: one ResourceClaim API for both vendors. Pod claims memory + framework requirement; scheduler picks matching device. Replaces 2 separate device plugins."),
        Scenario(name="GPU Operator simplifies driver lifecycle", body="Pre-Op: bare-metal driver install drift across nodes; CUDA version mismatches. Post-Op: containerized driver via Operator; Helm-managed; deterministic across nodes."),
        Scenario(name="Outage — driver mismatch", body="Pre-Op cluster: H100 driver upgraded on some nodes; CUDA 12.0 vs 12.2; some workloads crashed. Postmortem: install GPU Operator; consistent driver via Helm + DaemonSet."),
    ],
    misconceptions=[
        Misconception(myth="\"NVIDIA device plugin enough; skip GPU Operator.\"", truth="Device plugin is one DaemonSet; Operator bundles driver + runtime + DCGM + MIG mgr + RDMA. Operator saves weeks of bespoke setup; recommended for any production cluster."),
        Misconception(myth="\"DRA replaces GPU Operator.\"", truth="DRA replaces per-vendor device plugin\'s scheduling role. GPU Operator still handles driver + runtime + DCGM + MIG mgr — orthogonal concerns."),
        Misconception(myth="\"MIG is always better than time-slicing.\"", truth="MIG is hardware-isolated; time-slicing is software-shared (lower isolation; QoS sensitive). Both are useful; MIG for isolation; time-slicing for elastic sharing where collisions are tolerable."),
    ],
    flashcards=[
        Flashcard(front="What does NVIDIA device plugin do?", back="DaemonSet advertising <code>nvidia.com/gpu</code> resources to kubelet. Pod requests; scheduler places."),
        Flashcard(front="GPU Operator components?", back="Driver (containerized) + container runtime + DCGM (metrics) + MIG manager + Node Feature Discovery + GPUDirect Storage / RDMA."),
        Flashcard(front="MIG profile syntax?", back="<code>nvidia.com/mig-Xg.Ygb</code> where X = compute slices (1-7 on H100), Y = memory GB. e.g., <code>nvidia.com/mig-1g.10gb: 1</code>."),
        Flashcard(front="DRA — what\'s structured parameters?", back="Vendor declares device-specific spec (memory size, model, MIG profile, RDMA capability); Pod claims with parameters; scheduler matches. Multi-vendor friendly."),
        Flashcard(front="MIG-supported GPU models?", back="H100 (up to 7 partitions per GPU), A100 (up to 7), GH200. Not B200 (different architecture)."),
        Flashcard(front="DCGM exporter — what does it provide?", back="GPU metrics (utilization, memory, power, temperature, ECC errors) → Prometheus. Foundation of GPU observability."),
        Flashcard(front="When use time-slicing vs MIG?", back="<strong>MIG</strong>: isolation matters; tenant security; predictable QoS. <strong>Time-slicing</strong>: elastic sharing; bursty workloads; lower-priority workloads."),
        Flashcard(front="DRA vs device plugin — when each?", back="<strong>DRA</strong> (K8s 1.32+ stable): multi-vendor + advanced scheduling + partial sharing. <strong>Device plugin</strong>: legacy + per-vendor; still works; will phase out."),
    ],
    quizzes=[
        Quiz(prompt="A team has 8× H100 cluster + many small inference Pods. Walk MIG setup.",
            answer="(1) <strong>Install GPU Operator</strong> via Helm with MIG support enabled. (2) <strong>Configure MIG profile per node</strong>: e.g., 7× 1g.10gb instances per H100 → 56 inference slots cluster-wide. (3) <strong>Update Pod manifests</strong>: <code>resources.limits: nvidia.com/mig-1g.10gb: 1</code>. (4) <strong>Validate</strong>: DCGM metrics show per-instance utilization. (5) <strong>Production rollout</strong>: per-node-group MIG profile (some nodes 1g.10gb for inference; others whole-GPU for training); nodeSelector picks right pool. (6) <strong>Operational</strong>: tune MIG profile per workload mix; monitor underutilization."),
        Quiz(prompt="Cluster has NVIDIA + AMD GPUs. Walk DRA adoption.",
            answer="(1) <strong>Upgrade K8s</strong> to 1.32+ (DRA stable). (2) <strong>Install vendor DRA drivers</strong>: NVIDIA DRA driver + AMD DRA driver. (3) <strong>Define ResourceClass</strong> for each vendor or unified abstraction. (4) <strong>Update Pods</strong>: replace nodeSelector + device plugin requests with ResourceClaim referring to the structured params (memory, framework). (5) <strong>Scheduler</strong> matches Pods to devices via DRA. (6) <strong>Migrate gradually</strong>: per-workload, alongside legacy device plugin until full DRA cutover."),
        Quiz(prompt="The CFO sees H100 cost: \"why pay for H100 if we use 20%?\" Defend.",
            answer="\"<strong>The H100 underutilization is fixable; H100 model isn\'t.</strong> Three options: (1) <strong>MIG</strong>: hardware-partition into 7 instances; one H100 → 7 inference Pods; utilization 4×; cost / Pod 4× lower. (2) <strong>Time-slicing</strong>: software-share GPU across multiple Pods; cheaper than MIG; lower isolation. (3) <strong>Right-size</strong>: maybe inference doesn\'t need H100; A10 / L40 / consumer GPUs cost 1/3 with adequate perf for many models. <strong>Investment</strong>: GPU Operator + MIG enablement + workload audit = 1 platform-engineer-week. <strong>Saves</strong>: 50%+ of GPU bill once optimised. <strong>Don\'t cancel H100; optimise it.</strong>\"", cyoa=True, cyoa_tag="how the platform engineer defended H100 + MIG"),
    ],
    glossary=[
        GlossaryItem(name="NVIDIA device plugin", definition="DaemonSet advertising nvidia.com/gpu resources to kubelet."),
        GlossaryItem(name="GPU Operator", definition="NVIDIA-published Operator bundling driver + runtime + DCGM + MIG manager + RDMA + GPUDirect Storage."),
        GlossaryItem(name="MIG (Multi-Instance GPU)", definition="H100 / A100 hardware partition into up to 7 isolated instances."),
        GlossaryItem(name="DRA", definition="Dynamic Resource Allocation; K8s 1.32+ stable; multi-vendor structured parameters."),
        GlossaryItem(name="DCGM", definition="NVIDIA Data Center GPU Manager. Metrics exporter for Prometheus."),
        GlossaryItem(name="time-slicing GPU", definition="Software-shared GPU across multiple Pods; lower isolation than MIG."),
        GlossaryItem(name="ResourceClaim (DRA)", definition="Pod-attached claim referring to a ResourceClass with structured parameters."),
        GlossaryItem(name="GPUDirect RDMA", definition="GPU memory directly accessible by RDMA NIC; eliminates host CPU copy for AI training collective ops."),
        GlossaryItem(name="containerd nvidia runtime", definition="Container runtime mode passing GPU through to container; enabled per Pod via runtimeClassName."),
        GlossaryItem(name="Bottlerocket", definition="AWS minimal container OS; supports GPU via NVIDIA driver bundle."),
    ],
    recap_lead="GPU node + GPU Operator (driver/runtime/DCGM/MIG/RDMA) + MIG (hardware partition) + DRA (multi-vendor scheduling). Slice + share + structured-schedule = high GPU utilization.",
    recap_next='<strong>Next — I2: Kueue + MultiKueue + Volcano gang scheduling.</strong>',
    architecture_svg='''<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GPU node + device plugin / GPU Operator + MIG slices + DRA multi-vendor scheduling.">
  <rect x="10" y="10" width="740" height="220" rx="12" fill="#FBF7F0" stroke="#1F2433"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">GPU NODE · DRIVER + DEVICE PLUGIN + MIG + DRA</text>
  <rect x="20" y="50" width="220" height="65" rx="6" fill="#3F4A5E"/>
  <text x="130" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">GPU node (H100 / A100 / B200)</text>
  <text x="130" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">NVIDIA driver + containerd nvidia runtime</text>
  <text x="130" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">node label: accelerator: nvidia-h100</text>
  <line x1="240" y1="82" x2="270" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aI1)"/>
  <defs><marker id="aI1" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><polygon points="0 0, 10 5, 0 10" fill="#5A4F45"/></marker></defs>
  <rect x="270" y="50" width="220" height="65" rx="6" fill="#5DCAA5"/>
  <text x="380" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">GPU Operator (DaemonSet)</text>
  <text x="380" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">device plugin · DCGM · MIG mgr</text>
  <text x="380" y="100" text-anchor="middle" font-size="8" fill="#1F2433">advertises nvidia.com/gpu</text>
  <line x1="490" y1="82" x2="520" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aI1)"/>
  <rect x="520" y="50" width="220" height="65" rx="6" fill="#FF9900"/>
  <text x="630" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">MIG instances (H100/A100)</text>
  <text x="630" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">7×1g.10gb / 3×2g.20gb / etc.</text>
  <text x="630" y="100" text-anchor="middle" font-size="8" fill="#1F2433">hardware-isolated</text>
  <rect x="20" y="130" width="350" height="55" rx="6" fill="#5A6B81"/>
  <text x="195" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">DRA (K8s 1.32+ stable)</text>
  <text x="195" y="166" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">Dynamic Resource Allocation · multi-vendor</text>
  <text x="195" y="178" text-anchor="middle" font-size="8" fill="#FBE8DC">structured parameters · partial sharing</text>
  <rect x="380" y="130" width="360" height="55" rx="6" fill="#5E4A8E"/>
  <text x="560" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Pod requests + scheduler placement</text>
  <text x="560" y="166" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">resources.limits.nvidia.com/mig-1g.10gb: 1</text>
  <text x="560" y="178" text-anchor="middle" font-size="8" fill="#FBE8DC">or DRA ResourceClaim with structured params</text>
  <rect x="20" y="195" width="720" height="30" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="215" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">DCGM exporter → Prometheus → utilization dashboards · GPUDirect Storage + RDMA when configured</text>
</svg>''',
    architecture_caption='GPU node ships NVIDIA driver + nvidia containerd runtime; GPU Operator deploys device plugin + DCGM + MIG manager. MIG hardware-partitions H100/A100 into up to 7 isolated instances. DRA gives multi-vendor structured-parameter scheduling. DCGM exporter → Prometheus.',
)
