"""K-GKE G8 — GKE Enterprise (Fleets) + AI/ML on GKE."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GKE Enterprise (Fleets) + AI/ML on GKE — Config Sync, Policy Controller, CSM, Connect Gateway, MCI/MCG, GKE on AWS/Azure/VMware/bare metal, JobSet, Kueue, GPU Operator, MIG, TPU multi-host, Ray, Inference Gateway, vLLM/NIM/Triton.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Research Greenhouse — fleets + AI/ML</text>
  <rect x="40" y="70" width="200" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="140" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">fleets — multi-cluster + multi-cloud</text>
  <text x="140" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">Config Sync (GitOps)</text>
  <text x="140" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">Policy Controller</text>
  <text x="140" y="131" text-anchor="middle" font-size="9" fill="#FBF1D6">Cloud Service Mesh fleet-wide</text>
  <text x="140" y="145" text-anchor="middle" font-size="9" fill="#FBF1D6">Connect Gateway · MCI / MCG</text>
  <text x="140" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">GKE on AWS/Azure/VMware/BM</text>
  <rect x="255" y="70" width="200" height="120" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="355" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">batch + scheduling</text>
  <text x="355" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">JobSet API</text>
  <text x="355" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Kueue (queueing)</text>
  <text x="355" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">priority + preemption</text>
  <text x="355" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">multi-host TPU pods</text>
  <rect x="470" y="70" width="120" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="530" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">accelerators</text>
  <text x="530" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">NVIDIA GPU Operator</text>
  <text x="530" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">MIG slicing</text>
  <text x="530" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">TPU Trillium / Ironwood</text>
  <text x="530" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">Ray on GKE</text>
  <rect x="605" y="70" width="115" height="120" rx="10" fill="#E8B547" stroke="#3F4A5E"/>
  <text x="662" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#5A4F45">inference</text>
  <text x="662" y="105" text-anchor="middle" font-size="9" fill="#5A4F45">GKE Inference Gateway</text>
  <text x="662" y="118" text-anchor="middle" font-size="9" fill="#5A4F45">model-aware routing</text>
  <text x="662" y="131" text-anchor="middle" font-size="9" fill="#5A4F45">vLLM</text>
  <text x="662" y="145" text-anchor="middle" font-size="9" fill="#5A4F45">NVIDIA NIM</text>
  <text x="662" y="158" text-anchor="middle" font-size="9" fill="#5A4F45">Triton</text>
</svg>"""


LESSON = LessonSpec(
    num="08",
    title_short="enterprise + AI/ML",
    title_full="G8 · GKE Enterprise (Fleets) and AI/ML on GKE",
    title_html="K-GKE G8 · Enterprise + AI/ML",
    module_eyebrow="Module G8 · the Research Greenhouse — fleets + AI/ML",
    hero_sub_html='<strong>GKE Enterprise (Fleets):</strong> fleet management across GCP / AWS / Azure / on-prem; <strong>Config Sync</strong> (GitOps); <strong>Policy Controller</strong>; <strong>Cloud Service Mesh</strong> across fleets; <strong>Connect Gateway</strong>; <strong>Multi-Cluster Ingress / Gateway (MCI / MCG)</strong>. <strong>GKE on AWS / Azure / VMware / bare metal</strong>. <strong>AI/ML on GKE:</strong> <strong>JobSet API</strong> for multi-Job orchestration; <strong>Kueue</strong> for batch queueing; <strong>NVIDIA GPU Operator</strong>; <strong>MIG</strong> slicing; <strong>TPU multi-host</strong>; <strong>Ray on GKE</strong>; <strong>GKE Inference Gateway</strong> with model-aware routing; <strong>vLLM / NVIDIA NIM / Triton</strong> on GKE.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. You\'re paged: <em>\"Multi-cluster Ingress backend cluster <code>us-east1</code> degraded — 100% of fleet traffic now hitting <code>europe-west1</code>; latency 4× SLO.\"</em> You realise you have no Config Sync rule for the failover thresholds; the team last reconfigured MCI by hand six months ago and nobody documented it. <em>Five-cluster fleet, no GitOps, no playbook.</em> Today\'s lesson: GKE Enterprise (Fleets) for unified governance + AI/ML on GKE for the modern accelerator workload.",
    stamp_html="<strong>Fleets unify policy + GitOps + mesh + multi-cluster ingress across GCP and beyond. AI/ML on GKE = JobSet + Kueue for batch; GPU Operator + MIG + TPU multi-host for compute; Inference Gateway + vLLM/NIM/Triton for serving. Use both pillars for production AI platforms.</strong>",
    district_pin="kg-plot08",
    district_label="Research Greenhouse",
    sections=[
        Section(
            eyebrow="Section 1.1 · GKE Enterprise (Fleets)",
            h2="GKE Enterprise — Fleets, Config Sync, Policy Controller, CSM",
            body_html="""    <p><strong>Fleet</strong> = a logical grouping of GKE clusters (and Anthos-registered non-GKE clusters) under one governance plane. Register clusters with <code>gcloud container fleet memberships register</code>. Fleet enables:</p>
    <ul>
      <li><strong>Config Sync</strong> = continuous GitOps reconciliation. <code>RootSync</code> + <code>RepoSync</code> CRDs reconcile manifests from a Git repo into clusters. Drift detection on; manual edits reverted. Three repo patterns: per-tenant repos / per-environment repos / per-cluster repos. Replaces self-installed Argo CD or Flux.</li>
      <li><strong>Policy Controller</strong> = managed OPA Gatekeeper. Fleet-wide admission policies via Constraint templates; built-in baselines (Pod security standard, registry restriction, label requirements); custom Rego or CEL.</li>
      <li><strong>Cloud Service Mesh (CSM)</strong> = managed Istio across fleet members. <em>mTLS between Pods across clusters</em>; cross-fleet traffic management; service-to-service auth via SPIFFE identity. The Istio control plane is Google-operated; sidecars in each member cluster.</li>
    </ul>
    <p><strong>Connect Gateway</strong> = run kubectl against any registered fleet cluster via the GCP control plane. No need to expose individual cluster apiserver IPs to humans; auth via GCP IAM; works for clusters behind NAT / on-prem / in other clouds.</p>
    <p><strong>Multi Cluster Ingress (MCI) / Multi Cluster Gateway (MCG)</strong> (covered in G3) — single global anycast IP across fleet clusters; traffic to nearest healthy member; failover automatic.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · GKE on AWS / Azure / VMware / bare metal",
            h2="GKE on AWS / Azure / VMware / bare metal (Anthos Multi-Cloud + on-prem)",
            body_html="""    <p>GKE Enterprise extends GKE\'s management surface beyond GCP:</p>
    <ul>
      <li><strong>GKE on AWS</strong> — full GKE control plane running in the customer\'s AWS account. Same kubectl + Cloud Console + fleet experience. Workloads on EC2 instances; storage on EBS; networking on AWS VPC. <em>For multi-cloud teams who want one operational model.</em></li>
      <li><strong>GKE on Azure</strong> — same as above for Azure. Workloads on Azure VMs.</li>
      <li><strong>GKE on VMware</strong> — Anthos clusters on customer\'s vSphere on-prem. Standardised K8s on the existing virtualisation estate.</li>
      <li><strong>GKE on bare metal</strong> — Anthos clusters directly on customer hardware (Intel / AMD x86 / ARM). For edge data centres + telco / industrial workloads.</li>
    </ul>
    <p><em>All four</em> register into the same Fleet as native GCP GKE clusters → unified Config Sync, Policy Controller, CSM, observability. <em>One operational story across the entire K8s estate.</em></p>"""
        ),
        Section(
            eyebrow="Section 1.3 · AI/ML — batch + accelerators",
            h2="AI/ML on GKE — JobSet, Kueue, GPU Operator, MIG, TPU multi-host, Ray",
            body_html="""    <p><strong>Batch + scheduling</strong>:
    <ul>
      <li><strong>JobSet API</strong> — orchestrate sets of K8s Jobs together (success, failure, dependency). For multi-host distributed training: launch N Jobs simultaneously; coordinate ranks; handle failure as a unit.</li>
      <li><strong>Kueue</strong> — Kubernetes-native batch queueing. ClusterQueue + LocalQueue + Workload CRDs. Priority + preemption; quota borrowing across teams; preserves the K8s API. <em>The modern way to run batch on K8s.</em></li>
      <li>Combine: Kueue queues Workloads; admitted Workloads create JobSets; JobSets launch GPU/TPU Pods.</li>
    </ul>
    <p><strong>NVIDIA GPU Operator</strong> — manages NVIDIA driver + container runtime + device plugin lifecycle on GPU node pools. Replaces the manual node-image driver-version juggling. Required for advanced features (MIG, NVLink, RDMA).</p>
    <p><strong>MIG (Multi-Instance GPU)</strong> — slice a single H100 / H200 GPU into multiple smaller virtual GPUs (e.g., 7 × 10GB MIGs from one 80GB H100). Each MIG appears as <code>nvidia.com/mig-1g.10gb: 1</code> resource. Lets cost-effective inference share a high-end GPU across multiple Pods.</p>
    <p><strong>TPU multi-host</strong> — TPU v5e+ pods span multiple node-host VMs sharing one logical TPU pod. Requires special node-pool topology (single VM = host; pod = multiple hosts) + workload integration via JobSet for coordinated launch. <em>Distributed training at TPU scale.</em></p>
    <p><strong>Ray on GKE</strong> — KubeRay operator manages Ray clusters as RayCluster CRDs. Train and serve large models with Ray\'s distributed primitives (Tasks, Actors, Datasets, Train, Serve). KubeRay handles head + worker Pod orchestration on GKE.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · AI/ML — inference (GKE Inference Gateway + vLLM/NIM/Triton)",
            h2="AI/ML inference — GKE Inference Gateway + vLLM / NVIDIA NIM / Triton",
            body_html="""    <p><strong>GKE Inference Gateway</strong> = an extension of the GKE Gateway API for AI inference. Model-aware routing: route requests by model name, prompt size, batching opportunity, prefix-cache hit. Supports KV-cache aware routing for transformer inference (route follow-up requests in the same conversation back to the same Pod with the warm KV cache). <em>Optimised cost-per-token for LLM serving.</em></p>
    <p><strong>vLLM</strong> — high-throughput LLM serving with PagedAttention + continuous batching. The de-facto choice for GPU inference of open-weights models (Llama / Mistral / Qwen / etc.). Runs as a Pod with model loaded into GPU memory. <em>Combine with Inference Gateway for production-scale serving.</em></p>
    <p><strong>NVIDIA NIM</strong> — NVIDIA-packaged inference microservice container. Pre-built for popular models with optimised kernels, TensorRT-LLM, Triton inside. Runs on GKE GPU node pools. NVIDIA-supported.</p>
    <p><strong>Triton Inference Server</strong> — NVIDIA\'s general-purpose inference server. Multi-framework (TensorRT, ONNX, PyTorch, TensorFlow); multi-model; ensemble pipelines. Older-but-mature; NIM is the modern wrapper for LLMs.</p>
    <p><strong>End-to-end inference platform pattern</strong>: Inference Gateway (model-aware routing) → vLLM Pods (GPU serving) on Compute Class Accelerator A4 H200 → Cloud Trace for end-to-end latency → SLO Monitoring with cost-per-token KPI joined from BQ. <em>Production AI inference platform on GKE.</em></p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A platform team has 30 GKE clusters + 5 EKS clusters from an acquisition. They want one place to deploy a NetworkPolicy and have it land everywhere. What\'s the GCP-native answer?",
            options=[
                ("Write a script that loops kubectl across contexts.", False),
                ("Enable GKE Enterprise; register all 35 clusters into a Fleet (EKS via Connect agent); use Config Sync to deploy the NetworkPolicy from one Git repo to all members.", True),
                ("Migrate all clusters to GKE first.", False),
            ],
            feedback="Fleets + Config Sync = one governance plane across multi-cloud K8s. EKS / on-prem clusters register via the Connect agent and become Config Sync targets just like native GKE.",
        ),
    },
    before_after_before='<p>Pre-fleet GKE multi-cluster ops = scripts looping kubectl. Pre-Config-Sync GitOps = self-installed Argo CD per cluster. Pre-Inference-Gateway, LLM serving needed manual model→Pod routing or naive HTTP load-balancing (which broke KV-cache locality). Pre-Kueue, batch on K8s was DIY queueing. Multi-cloud K8s = three different operational stories. AI/ML on K8s was assembly required.</p>',
    before_after_after='<p>Modern GKE Enterprise: <strong>fleets</strong> unify policy + GitOps + mesh across GCP/AWS/Azure/on-prem. <strong>Config Sync + Policy Controller + CSM</strong> are managed. <strong>Connect Gateway</strong> + MCI/MCG handle multi-cluster operations. <strong>AI/ML platform pattern</strong>: JobSet + Kueue for batch; GPU Operator + MIG + TPU multi-host + Ray for compute; Inference Gateway + vLLM / NIM / Triton for serving. <em>Production AI platform on GKE in weeks, not quarters.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Fleets are the unifier; AI/ML on GKE is the use case GKE was designed for from the start.</em></p>',
    analogy_intro_html='''<p>The <strong>Research Greenhouse</strong> is K-Garden\'s most ambitious building. Two wings.</p>
    <p>The <strong>Multi-Garden Wing</strong> (Fleets) connects this garden to dozens of others — same head-gardener manuals, same security guards, same seasonal calendar — even gardens hosted by other operators (AWS, Azure, on-prem). One Git repo (Config Sync) describes the standard practices; every garden in the network reconciles to it. The <strong>Network Concierge</strong> (Connect Gateway) lets a head gardener visit any garden via one badge. The <strong>Sister-Garden Front Gates</strong> (MCI/MCG) route visitors to the nearest healthy garden automatically.</p>
    <p>The <strong>AI Lab Wing</strong> handles the high-tech crops. <em>JobSet</em> + <em>Kueue</em> coordinate large batch experiments across plots. <em>NVIDIA GPU Operator</em> manages the heavy machinery; <em>MIG</em> slices an H100 microscope into seven smaller microscopes for budget experiments. <em>TPU multi-host</em> coordinates Google-designed accelerator pods across multiple host VMs for distributed training. <em>Ray</em> handles parallel orchestration.</p>
    <p>For <em>serving</em> trained models, the lab has the <strong>Inference Gateway</strong> — a model-aware concierge that routes requests by model name, prompt size, conversation history (KV-cache locality). The serving runtimes are <em>vLLM</em>, <em>NVIDIA NIM</em>, or <em>Triton</em> — each a specialty tool for inference at scale.</p>''',
    translation_rows=[
        ("Multi-Garden Wing", "GKE Enterprise (Fleets)"),
        ("One Git repo for standard practices", "Config Sync (RootSync + RepoSync)"),
        ("House rules enforced at every gate", "Policy Controller (managed Gatekeeper)"),
        ("Encrypted notes between plants in any garden", "Cloud Service Mesh fleet-wide"),
        ("Network Concierge", "Connect Gateway (kubectl across fleet)"),
        ("Sister-Garden Front Gates", "Multi-Cluster Ingress / Multi-Cluster Gateway"),
        ("Other operators\' gardens", "GKE on AWS / Azure / VMware / bare metal"),
        ("AI Lab Wing", "AI/ML on GKE pillar"),
        ("Coordinated batch experiments", "JobSet API"),
        ("Experiment queue", "Kueue (ClusterQueue + LocalQueue + Workload)"),
        ("Heavy-machinery manager", "NVIDIA GPU Operator"),
        ("H100 sliced into smaller microscopes", "MIG (Multi-Instance GPU)"),
        ("Coordinated TPU pod", "TPU multi-host pods (TPU v5e+)"),
        ("Parallel orchestration framework", "Ray on GKE (KubeRay)"),
        ("Model-aware concierge", "GKE Inference Gateway (KV-cache aware routing)"),
        ("Specialty inference rooms", "vLLM / NVIDIA NIM / Triton on GKE"),
    ],
    analogy_stops="A research lab\'s equipment is fixed; AI/ML on GKE is rapidly evolving (Inference Gateway is recent; TPU + GPU SKUs change). The metaphor under-captures version-velocity in this space.",
    eli5="There\'s a special wing that connects the garden to other gardens worldwide so they all use the same rules. There\'s also an AI lab with super-fast computers that train and serve smart models. Special staff route requests to the right model.",
    eli10="GKE Enterprise (Fleets) = fleet of clusters (GKE + GKE-on-AWS/Azure/VMware/bare-metal); Config Sync for GitOps; Policy Controller for admission; Cloud Service Mesh fleet-wide mTLS; Connect Gateway for kubectl-across-clusters; MCI/MCG for multi-cluster ingress. AI/ML on GKE: JobSet + Kueue for batch; GPU Operator + MIG + TPU multi-host + Ray for compute; Inference Gateway + vLLM/NIM/Triton for serving.",
    scenarios=[
        Scenario(
            name="Bank — fleet of 50 clusters under Config Sync + Policy Controller",
            body="Bank registers 35 GKE + 10 GKE-on-AWS + 5 GKE-on-VMware clusters into a Fleet. Config Sync deploys uniform NetworkPolicies + PSA labels + RBAC bindings from one Git repo to all 50 clusters. Policy Controller blocks non-compliant Pods at admission everywhere. CSM provides cross-cluster mTLS. <em>One governance model across heterogeneous K8s.</em>",
        ),
        Scenario(
            name="LLM inference platform — Inference Gateway + vLLM on A4 H200",
            body="Team serves Llama 3 70B inference. <strong>Inference Gateway</strong> routes by model name + KV-cache locality (chats stick to the same Pod for cache reuse). <strong>vLLM</strong> Pods on Compute Class Accelerator with A4 H200. SLO: p95 first-token-latency &lt; 500ms; cost-per-token tracked via BQ. <em>Throughput +60% vs naive routing thanks to KV-cache locality.</em>",
        ),
        Scenario(
            name="ML training — Kueue + JobSet + TPU multi-host",
            body="ML team runs distributed training jobs on TPU. Kueue ClusterQueue defines team quotas + priority; submit a Workload CR; admitted Workload creates a JobSet; JobSet launches a TPU multi-host pod with 4 hosts × 4 chips per host. Failed host = JobSet treats it as failure of the entire training run; Kueue requeues with priority. <em>Production batch ML platform; quota + priority + preemption all built-in.</em>",
        ),
        Scenario(
            name="Ray on GKE for distributed feature engineering",
            body="Data team has a 50TB feature engineering job. Deploy <strong>RayCluster</strong> via KubeRay on GKE Standard with Compute Class Scale-Out (T2D ARM, low cost-per-vCPU). Ray Tasks fan out to ~500 workers; Ray Datasets read from BigQuery; results stream to GCS. <em>Job completes in 18 min vs 4hr on a single VM. Cluster destroyed after job; per-second billing.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Fleets are just a name for grouping clusters in the GCP console.\"",
            truth="Fleets are an active control plane. Fleet membership enables fleet-scoped Config Sync, Policy Controller, CSM, Connect Gateway, MCI/MCG, fleet-default settings. <em>Capabilities, not just labels.</em> Without Fleet membership, those features don\'t apply.",
        ),
        Misconception(
            myth="\"Inference Gateway and regular Gateway API are the same.\"",
            truth="Inference Gateway is an extension of Gateway API specifically for AI inference. Adds model-aware routing (route by model name), KV-cache locality (route follow-up requests in a conversation to the same Pod), prompt-size routing (small prompts to high-throughput Pods, large prompts to large-memory Pods). Regular Gateway API doesn\'t know about model semantics.",
        ),
        Misconception(
            myth="\"vLLM, NIM, and Triton are interchangeable.\"",
            truth="<strong>vLLM</strong> = open-source LLM-specialised serving with PagedAttention + continuous batching; best for open-weights LLMs at scale. <strong>NIM</strong> = NVIDIA-packaged inference microservice; pre-built for popular models with TensorRT-LLM optimisations + Triton inside; NVIDIA-supported with NVIDIA enterprise license. <strong>Triton</strong> = NVIDIA general-purpose inference server (older-but-mature, multi-framework, not LLM-specific). Pick vLLM for community LLMs at scale; NIM for vendor-supported LLMs; Triton for general-purpose multi-framework inference (CV / classical ML).",
        ),
    ],
    flashcards=[
        Flashcard(front="What is a GKE Fleet?", back="A logical grouping of clusters (GKE + Anthos-registered non-GKE) under one governance plane. Enables Config Sync, Policy Controller, CSM, Connect Gateway, MCI/MCG, fleet-default settings. Register with <code>gcloud container fleet memberships register</code>."),
        Flashcard(front="What does Config Sync do?", back="Continuous GitOps reconciliation. RootSync + RepoSync CRDs reconcile manifests from Git into clusters. Drift detection on; manual edits reverted. Three repo patterns: per-tenant / per-environment / per-cluster."),
        Flashcard(front="What is Connect Gateway?", back="Run kubectl against any registered fleet cluster via the GCP control plane. No need to expose individual cluster apiserver IPs to humans; auth via GCP IAM. Works for clusters behind NAT / on-prem / in other clouds."),
        Flashcard(front="GKE on AWS / Azure / VMware / bare metal — what are these?", back="Anthos Multi-Cloud + on-prem variants of GKE. Full GKE control plane runs in customer\'s AWS / Azure / vSphere / bare-metal estate. Workloads on local infra. All register into the same Fleet for unified governance."),
        Flashcard(front="What is Kueue?", back="Kubernetes-native batch queueing. ClusterQueue (cluster-wide capacity + priority) + LocalQueue (namespace-level) + Workload CRD. Quota borrowing across teams; priority + preemption. Replaces DIY batch schedulers."),
        Flashcard(front="What is JobSet API?", back="Orchestrate sets of K8s Jobs together: success / failure / dependency relationships. For multi-host distributed training where N Jobs must launch simultaneously and fail/succeed as a unit (e.g., TPU multi-host pods, multi-node GPU training)."),
        Flashcard(front="What is MIG and when use it?", back="<strong>Multi-Instance GPU</strong> — slice a single H100/H200 into multiple smaller virtual GPUs (e.g., 7 × 10GB MIGs from one 80GB H100). Use when you have inference workloads that don\'t need the full GPU; share a high-end GPU across multiple Pods cost-effectively."),
        Flashcard(front="What does GKE Inference Gateway add over regular Gateway?", back="Model-aware routing: route by model name; KV-cache locality (follow-up requests in a conversation go back to the same Pod with warm cache); prompt-size routing (small prompts → high-throughput Pods, large prompts → large-memory Pods). Optimises cost-per-token for LLM serving."),
    ],
    quizzes=[
        Quiz(
            prompt="A platform team wants to roll out a single PSA Restricted label change across 25 GKE clusters in 3 regions + 5 GKE-on-AWS clusters. They have no Fleet today. What\'s the rollout plan?",
            answer="(1) Enable GKE Enterprise on the project. (2) Register all 30 clusters into a Fleet (the GKE-on-AWS clusters via the Connect agent). (3) Create a Config Sync RootSync from a Git repo containing the namespace label change. (4) Apply RootSync to all fleet members (or a subset via labels / selectors). (5) Config Sync reconciles to every cluster within minutes. (6) Verify via Connect Gateway: <code>kubectl --context fleet/cluster-X get ns -L pod-security.kubernetes.io/enforce</code>. <em>Total: hours, not weeks; future changes are one git commit.</em>",
        ),
        Quiz(
            prompt="An LLM team serves Llama 3 70B from 12 vLLM Pods on A4 H200. Latency is high; cost-per-token is 2× what they expect. They use a regular Gateway with round-robin load balancing. What\'s the obvious upgrade?",
            answer="<strong>GKE Inference Gateway with KV-cache locality routing.</strong> Round-robin sends each conversation\'s follow-up requests to a random Pod — KV cache is cold; vLLM has to recompute attention over the prompt prefix. Inference Gateway routes follow-up requests in the same conversation back to the same Pod with the warm KV cache, often reducing per-request compute by 50-80% on long conversations. Throughput goes up; cost-per-token drops. Plus model-aware routing — split traffic by prompt size (small to high-throughput Pods, large to large-memory Pods).",
        ),
        Quiz(
            prompt="The CTO walks in: \"We have 5 clusters, no Fleet. Why would we pay for GKE Enterprise?\" Defend the line item.",
            answer="\"<strong>Fleet pays off when you have governance work that should be uniform across clusters.</strong> At 5 clusters: Config Sync removes per-cluster Argo CD operation. Policy Controller enforces admission policies fleet-wide instead of per-cluster Helm chart drift. Cloud Service Mesh handles cross-cluster mTLS without DIY mesh-of-meshes. Connect Gateway lets the on-call team kubectl any cluster from one CLI without per-cluster auth setup. MCI/MCG provides global anycast IP for active-active across regions. <em>The 5-cluster threshold is where the per-cluster ops cost crosses the Fleet license cost; below that, vanilla GKE is fine. Above that, Fleet is the operational unifier.</em> If we plan to grow past 10 clusters or add multi-cloud, enable Fleet now and front-load the muscle memory.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CTO",
        ),
    ],
    glossary=[
        GlossaryItem(name="Fleet", definition="Logical grouping of GKE + Anthos clusters under one governance plane. Enables Config Sync, Policy Controller, CSM, Connect Gateway, MCI/MCG."),
        GlossaryItem(name="Config Sync", definition="Continuous GitOps reconciliation. RootSync + RepoSync CRDs."),
        GlossaryItem(name="Policy Controller", definition="Managed OPA Gatekeeper. Fleet-wide admission policies via Constraint templates / Rego / CEL."),
        GlossaryItem(name="Cloud Service Mesh (CSM)", definition="Managed Istio across fleet members. Cross-cluster mTLS + traffic management."),
        GlossaryItem(name="Connect Gateway", definition="kubectl any registered fleet cluster via the GCP control plane. Auth via GCP IAM."),
        GlossaryItem(name="GKE on AWS / Azure / VMware / bare metal", definition="Anthos Multi-Cloud + on-prem GKE. Full GKE control plane in customer\'s estate; registers into Fleet."),
        GlossaryItem(name="JobSet API", definition="K8s API for orchestrating sets of Jobs together: success / failure / dependency. For multi-host distributed training."),
        GlossaryItem(name="Kueue", definition="K8s-native batch queueing. ClusterQueue + LocalQueue + Workload CRD. Priority + preemption + quota borrowing."),
        GlossaryItem(name="NVIDIA GPU Operator", definition="Manages NVIDIA driver + container runtime + device plugin lifecycle on GPU pools."),
        GlossaryItem(name="MIG (Multi-Instance GPU)", definition="Slice an H100/H200 into multiple smaller virtual GPUs. Cost-effective inference sharing."),
        GlossaryItem(name="TPU multi-host", definition="TPU v5e+ pods spanning multiple host VMs. Special node-pool topology + JobSet for coordinated launch."),
        GlossaryItem(name="Ray on GKE (KubeRay)", definition="KubeRay operator manages RayCluster CRDs. Ray Tasks / Actors / Datasets / Train / Serve on GKE."),
        GlossaryItem(name="GKE Inference Gateway", definition="Gateway API extension for AI inference. Model-aware routing, KV-cache locality, prompt-size routing."),
        GlossaryItem(name="vLLM", definition="High-throughput LLM serving with PagedAttention + continuous batching."),
        GlossaryItem(name="NVIDIA NIM", definition="NVIDIA-packaged inference microservice. Pre-built for popular models; TensorRT-LLM + Triton inside."),
        GlossaryItem(name="Triton Inference Server", definition="NVIDIA general-purpose inference server. Multi-framework, multi-model, ensemble pipelines."),
    ],
    recap_lead='Two pillars: GKE Enterprise (Fleets) for cross-cluster + multi-cloud governance; AI/ML on GKE for batch (JobSet/Kueue) + accelerators (GPU Operator/MIG/TPU/Ray) + serving (Inference Gateway + vLLM/NIM/Triton).',
    recap_next='<strong>Next — G9: GKE Troubleshooting (GCP-Specific).</strong> IAM/RBAC mismatch, WIF token issues, Autopilot admission rejection, Node pool / MIG failures, IP exhaustion, NEG health-check failures, Ingress provisioning, firewall blocks, Cloud NAT/SNAT, DNS, storage attach, release channel / maintenance exclusion issues, gcpdiag, GKE Recommender, Logs Explorer.',
)
