"""K-ADV-AI I6 — RDMA / EFA + storage throughput + JuiceFS / Alluxio + OCI artifacts."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="High-speed AI infra."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Signal Lines · K-Observatory — fabric + storage for AI</text><rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E"/><text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">RDMA / EFA</text><text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">low-latency interconnect</text><rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5"/><text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">JuiceFS / Alluxio</text><text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">distributed model cache</text><rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900"/><text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">OCI artifacts</text><text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">models in OCI registry</text><rect x="595" y="70" width="125" height="100" rx="10" fill="#5A6B81"/><text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">storage throughput</text><text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">GPUDirect Storage</text></svg>"""


LESSON = LessonSpec(
    num="06", title_short="RDMA + storage", title_full="I6 · RDMA / EFA + Storage Throughput + JuiceFS / Alluxio + OCI Artifacts",
    title_html="K-ADV-AI I6 · Fabric + Storage", module_eyebrow="Module I6 · Signal Lines — fabric + storage for AI",
    hero_sub_html='<strong>RDMA / EFA</strong>: low-latency GPU-to-GPU + GPU-to-storage interconnect. AWS EFA on p5; Azure InfiniBand on ND H100; on-prem Mellanox / NVIDIA Quantum-2. <strong>GPUDirect Storage</strong>: NVMe / S3 directly to GPU memory bypassing CPU. <strong>JuiceFS / Alluxio</strong>: distributed model storage with shared cache; load-once cache-everywhere. <strong>OCI artifacts</strong>: models distributed via OCI registries (modelpacks); standardised tooling.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Distributed training of Llama 3 on 32 H100s — collective ops take 5× expected. <em>Without RDMA, GPU-to-GPU traffic goes through TCP / sockets / kernel; latency tail kills training</em>. Today\'s lesson: AI infra needs RDMA fabric + GPU-Direct storage + shared model cache.",
    stamp_html="<strong>RDMA / EFA = required fabric for distributed training. GPUDirect Storage = NVMe → GPU bypasses CPU. JuiceFS / Alluxio = shared model cache. OCI artifacts = standardised model distribution.</strong>",
    district_pin="kai-array06", district_label="Signal Lines",
    sections=[
        Section(eyebrow="Section 1.1 · RDMA / EFA fabric",
            h2="Low-latency GPU-to-GPU interconnect",
            body_html="""    <p><strong>RDMA</strong> (Remote Direct Memory Access): NIC writes directly to remote GPU memory; no CPU + kernel hop. <strong>EFA</strong> (AWS Elastic Fabric Adapter): AWS\'s RDMA-equivalent on p5 / hpc7g instances. <strong>InfiniBand</strong> (NVIDIA Quantum-2): on-prem fabric.</p>
    <p>Win for distributed training: collective ops (all-reduce / all-gather) latency drops 10×; large-model training throughput stays at scale.</p>
    <p>K8s setup: per-node RDMA device plugin advertises <code>nvidia.com/efa</code> or <code>rdma/hca</code>; Pods request via <code>resources.limits</code>; container image uses NCCL with EFA / IB transport.</p>"""),
        Section(eyebrow="Section 1.2 · GPUDirect Storage",
            h2="NVMe / S3 → GPU memory; bypass CPU",
            body_html="""    <p><strong>GPUDirect Storage (GDS)</strong>: NVMe or S3 reads land directly in GPU memory; no host bounce. Throughput rises 2-3× for IO-bound training.</p>
    <p>Setup: NVIDIA driver + GPUDirect Storage library + supported filesystem (BeeGFS / WekaIO / DDN EXAScaler / Lustre). Use cases: large dataset streaming during training; checkpoint write / restore."""),
        Section(eyebrow="Section 1.3 · JuiceFS + Alluxio",
            h2="Distributed shared model cache",
            body_html="""    <p>Loading a 70B model from S3 every Pod restart = ~10 minutes per Pod. <strong>JuiceFS / Alluxio</strong>: per-cluster distributed cache between S3 + Pods. Load once; cache locally; subsequent Pod restarts hit cache (sub-minute).</p>
    <p><strong>JuiceFS</strong>: POSIX-compatible distributed FS with object-storage backend. <strong>Alluxio</strong>: data orchestration layer; caches across nodes; supports many backends. Both K8s-native via DaemonSet + PVC.</p>"""),
        Section(eyebrow="Section 1.4 · OCI artifacts for models",
            h2="Models as OCI images; standardised tooling",
            body_html="""    <p><strong>OCI artifacts</strong>: models packaged as OCI images (modelpacks) + pushed to OCI registries (ECR / GCR / Harbor). Same registry / signing / SBOM / VEX pipeline as container images.</p>
    <p>Tools: <strong>ORAS</strong> (OCI Registry As Storage), <strong>KitOps</strong> (modelpack standard), <strong>Sigstore</strong> for model signing. Pull via <strong>oras pull</strong> or via init-container in Pod.</p>
    <p>Wins: <em>standardised distribution</em>; <em>signing + provenance</em>; <em>caching via registry mirror</em>; <em>versioned</em>."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why RDMA / EFA for distributed training?",
            options=[("Faster than TCP.", False), ("All-reduce / all-gather latency drops 10×; collective ops dominate distributed training.", True), ("Required by NVIDIA.", False)],
            feedback="Collective ops are the dominant cost in distributed training. RDMA bypasses CPU + kernel; latency drops 10×; throughput at 100+ GPU scales depends on this."),
        3: PauseCheck(question="Why use OCI artifacts for models?",
            options=[("Faster.", False), ("Reuse container registry + signing + caching + provenance toolchain; no separate model-storage stack.", True), ("Required by S3.", False)],
            feedback="OCI artifacts piggyback on the container registry ecosystem. Same Cosign signing + SBOM + VEX + caching infrastructure."),
    },
    before_after_before='<p>Pre-RDMA + GDS + cache + OCI: distributed training over TCP (slow); models loaded from S3 every Pod restart; bespoke distribution + verification.</p>',
    before_after_after='<p>RDMA / EFA fabric for collectives; GPUDirect Storage for IO; JuiceFS / Alluxio for shared model cache; OCI artifacts for distribution. AI infra at scale.</p>',
    before_after_caption='<p class="ba-caption"><em>AI workloads have unique fabric + storage needs; standard K8s infra alone underperforms.</em></p>',
    analogy_intro_html='''<p>Signal Lines run between every telescope (GPU) + every storage vault (NVMe / S3 / model cache). <strong>RDMA / EFA</strong>: dedicated low-latency optical fibers between telescopes — astronomers compare observations in real-time. <strong>GPUDirect Storage</strong>: direct pneumatic tubes from vault to telescope — bypass the central registry. <strong>JuiceFS / Alluxio</strong>: shared cache room — load model maps once, every astronomer reads from cache. <strong>OCI artifacts</strong>: standard catalogue cards for every model in the OCI library.</p>''',
    translation_rows=[
        ("Optical fibers between telescopes", "RDMA / EFA / InfiniBand"),
        ("Pneumatic tubes vault → telescope", "GPUDirect Storage"),
        ("Shared cache room", "JuiceFS / Alluxio"),
        ("Standard catalogue cards", "OCI artifacts (modelpacks)"),
        ("Cache + sign tool", "ORAS / KitOps / Sigstore"),
        ("Vault file system", "BeeGFS / WekaIO / Lustre / DDN"),
    ],
    analogy_stops="A real fabric is fiber; RDMA / GDS / cache are software + driver + hardware combined. Verify with NCCL benchmarks (nccl-tests).",
    eli5="High-speed signal lines between telescopes; direct vault-to-telescope tubes; shared cache rooms; standardised catalogue cards. AI needs these; standard K8s infra alone is too slow.",
    eli10="<strong>RDMA / EFA / InfiniBand</strong>: low-latency GPU-to-GPU; collective ops 10× faster. <strong>GPUDirect Storage</strong>: NVMe / S3 → GPU memory bypassing CPU. <strong>JuiceFS / Alluxio</strong>: distributed model cache; load-once cache-everywhere. <strong>OCI artifacts</strong>: models in OCI registry; standardised signing + caching.",
    scenarios=[
        Scenario(name="EFA for Llama 3 training", body="32 H100 distributed training migrated from TCP to AWS EFA. NCCL benchmarks: all-reduce latency 10×; training throughput 2× at same GPU count."),
        Scenario(name="JuiceFS shared model cache", body="Pre-cache: 70B model from S3 every Pod restart ~10 min. Post-JuiceFS: cache hit ~30s. Inference scaling-out time dropped accordingly."),
        Scenario(name="OCI model artifacts via Sigstore", body="Models pushed as OCI artifacts to Harbor; Cosign-signed; pulled by Pods via init-container. Same supply-chain pipeline as container images. Compliance evidence reused."),
        Scenario(name="Outage — collective op latency", body="Pre-RDMA: distributed training slowed unpredictably during peak network use. Postmortem: dedicate RDMA fabric for AI; segregate from general K8s traffic."),
    ],
    misconceptions=[
        Misconception(myth="\"Standard K8s networking is enough for AI.\"", truth="Distributed training collectives over TCP are 5-10× slower than RDMA. At 100+ GPU scale, RDMA isn\'t optional."),
        Misconception(myth="\"GPUDirect Storage is for one filesystem.\"", truth="GDS supports many filesystems (BeeGFS / WekaIO / Lustre / DDN). Not all support equally; benchmark per workload."),
        Misconception(myth="\"OCI artifacts are just for containers.\"", truth="OCI 1.1 referrers + ORAS make OCI registries general-purpose for any artifact. Models, SBOMs, attestations, Helm charts all use OCI."),
    ],
    flashcards=[
        Flashcard(front="What does RDMA do?", back="Remote Direct Memory Access — NIC writes directly to remote memory bypassing CPU + kernel. Foundation of distributed training fabric."),
        Flashcard(front="EFA vs InfiniBand vs RoCE?", back="<strong>EFA</strong> (AWS): RDMA-equivalent on p5 / hpc instances. <strong>InfiniBand</strong> (NVIDIA Quantum-2): on-prem dedicated fabric. <strong>RoCE</strong>: RDMA over Converged Ethernet. All achieve similar perf."),
        Flashcard(front="GPUDirect Storage — what does it do?", back="NVMe / S3 reads land directly in GPU memory; no host bounce. 2-3× IO throughput for training."),
        Flashcard(front="JuiceFS vs Alluxio — what differs?", back="<strong>JuiceFS</strong>: POSIX-compatible distributed FS with object-storage backend. <strong>Alluxio</strong>: data orchestration layer; caches across nodes; supports many backends. Both = shared model cache patterns."),
        Flashcard(front="OCI artifacts for models — tools?", back="<strong>ORAS</strong> (OCI Registry As Storage), <strong>KitOps</strong> (modelpack standard), <strong>Cosign</strong> (signing), <strong>Harbor / ECR / GCR</strong> (registries)."),
        Flashcard(front="When use RDMA?", back="Distributed training (multi-GPU collective ops). Single-GPU inference doesn\'t need it. Threshold: training at 4+ GPUs across nodes."),
        Flashcard(front="K8s RDMA device plugin?", back="Per-node DaemonSet advertising <code>rdma/hca</code> or <code>nvidia.com/efa</code> resources to kubelet. Pods request; placement aware."),
        Flashcard(front="modelpack standard?", back="KitOps modelpack — OCI artifact format standardising model + dataset + code + LICENSE bundling. Open standard for model distribution."),
    ],
    quizzes=[
        Quiz(prompt="Design AI infra for 100-GPU H100 cluster.",
            answer="(1) <strong>EFA / InfiniBand fabric</strong>: H100 nodes interconnected; per-node RDMA device plugin. (2) <strong>GPUDirect Storage</strong> (NVIDIA driver + library) + WekaIO / Lustre filesystem for training data. (3) <strong>JuiceFS</strong> shared cache for models + datasets; load-once across cluster. (4) <strong>OCI registry</strong> (Harbor) for model artifacts; Cosign-signed; SBOM-attached. (5) <strong>NCCL config</strong> per workload: EFA transport for AWS / IB transport on-prem. (6) <strong>Benchmark</strong>: nccl-tests baseline; per-workload benchmarks; tune."),
        Quiz(prompt="Inference fleet scales out; new Pods take 10 min loading model from S3. Walk fix.",
            answer="(1) <strong>JuiceFS or Alluxio</strong>: distributed cache between S3 + Pods. (2) <strong>Cluster setup</strong>: DaemonSet + PVC; Pods mount cache; first Pod warms cache; subsequent hit cache. (3) <strong>Validation</strong>: time-to-first-inference for new Pods drops to ~30s. (4) <strong>Tune</strong>: cache size + eviction; warm cache via init-container on cluster bootstrap."),
        Quiz(prompt="The CFO sees AWS EFA cost. Defend.",
            answer="\"<strong>EFA cost is small vs the cost of slower training.</strong> Without EFA, 32×H100 training takes 5× longer = 5× GPU-hours = 5× cost. Plus delayed model launches. EFA cost = ~10% premium on instance; saves 5× on training time. Net: 4-5× cheaper to use EFA. <strong>For inference fleets</strong>: EFA optional (single-GPU inference doesn\'t need). For training fleets: non-optional.\"", cyoa=True, cyoa_tag="how the platform engineer defended EFA"),
    ],
    glossary=[
        GlossaryItem(name="RDMA", definition="Remote Direct Memory Access; NIC bypasses CPU + kernel for low-latency."),
        GlossaryItem(name="EFA", definition="AWS Elastic Fabric Adapter; RDMA-equivalent on p5 / hpc instances."),
        GlossaryItem(name="InfiniBand", definition="NVIDIA Quantum-2 dedicated fabric; common on-prem AI."),
        GlossaryItem(name="GPUDirect Storage", definition="NVMe / S3 → GPU memory bypassing CPU. NVIDIA library + supported FS."),
        GlossaryItem(name="JuiceFS", definition="POSIX-compatible distributed FS with object-storage backend; shared model cache."),
        GlossaryItem(name="Alluxio", definition="Data orchestration layer; caches across nodes; multi-backend."),
        GlossaryItem(name="OCI artifacts", definition="OCI registry general-purpose artifact storage. Models / SBOMs / attestations."),
        GlossaryItem(name="ORAS", definition="OCI Registry As Storage; CLI for arbitrary artifacts."),
        GlossaryItem(name="modelpack (KitOps)", definition="OCI artifact format standardising model + dataset + code bundling."),
        GlossaryItem(name="NCCL", definition="NVIDIA Collective Communications Library; foundation of distributed-training collectives."),
    ],
    recap_lead="AI fabric: RDMA / EFA / IB. AI storage: GPUDirect Storage + JuiceFS / Alluxio. AI distribution: OCI artifacts. These are the AI-specific infra; standard K8s alone underperforms at 100+ GPU scale.",
    recap_next='<strong>Next — I7: GPU sharing + multi-tenant + cost optimization.</strong>',
)
