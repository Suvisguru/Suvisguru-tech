"""K-ADV-AI I3 — Ray + Kubeflow + KServe + JobSet."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ray + Kubeflow + KServe + JobSet."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Research Hall · K-Observatory — distributed compute + pipelines + serving</text><rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E"/><text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">KubeRay (Ray)</text><text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">distributed compute</text><rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5"/><text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Kubeflow</text><text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">training + pipelines</text><rect x="410" y="70" width="170" height="100" rx="10" fill="#FF9900"/><text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">KServe</text><text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">inference + autoscale</text><rect x="595" y="70" width="125" height="100" rx="10" fill="#5A6B81"/><text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">JobSet</text><text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">multi-pod jobs</text></svg>"""


LESSON = LessonSpec(
    num="03", title_short="Ray + Kubeflow + KServe", title_full="I3 · Ray + Kubeflow + KServe + JobSet",
    title_html="K-ADV-AI I3 · Ray + Kubeflow + KServe", module_eyebrow="Module I3 · Research Hall — distributed compute + pipelines + serving",
    hero_sub_html='<strong>KubeRay</strong>: Ray on K8s (distributed compute, RLlib, training, serving). <strong>Kubeflow</strong>: training operators (PyTorchJob / TFJob / MPIJob), pipelines, Notebooks, Katib (HPO), Model Registry. <strong>KServe</strong>: inference serving with autoscaling + canary + InferenceService CRD. <strong>JobSet</strong>: multi-pod jobs primitive (gang-compatible).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. ML team running training jobs by hand on bespoke EC2 instances; data scientist needed to learn boto3. <em>Without K8s-native ML tooling, every ML workflow is bespoke.</em> Today\'s lesson: KubeRay + Kubeflow + KServe + JobSet make ML workloads first-class K8s.",
    stamp_html="<strong>KubeRay = distributed compute. Kubeflow = training + pipelines + HPO. KServe = inference. JobSet = multi-pod jobs. Pick by ML phase; integrate via Kueue / Volcano for batch admission + gang.</strong>",
    district_pin="kai-array03", district_label="Research Hall",
    sections=[
        Section(eyebrow="Section 1.1 · KubeRay", h2="Ray on K8s — distributed compute primitive",
            body_html="""    <p><strong>Ray</strong>: distributed Python framework. <strong>KubeRay</strong> operator: <code>RayCluster</code> (long-running cluster), <code>RayJob</code> (one-shot), <code>RayService</code> (serving).</p>
    <p>Use cases: distributed training (Ray Train); reinforcement learning (RLlib); hyperparameter tuning (Ray Tune); generic distributed Python (Ray Core); LLM serving (Ray Serve / vLLM).</p>
    <p>Pattern: data scientist writes Python; KubeRay materialises Ray cluster; auto-scales workers; jobs submit + run."""),
        Section(eyebrow="Section 1.2 · Kubeflow", h2="Training operators + Pipelines + Notebooks + HPO",
            body_html="""    <p><strong>Kubeflow Training Operator</strong>: PyTorchJob / TFJob / MPIJob / XGBoostJob / PaddleJob — distributed training across Pods.</p>
    <p><strong>Kubeflow Pipelines</strong>: workflow engine (Argo-based). DAGs of training / preprocessing / evaluation.</p>
    <p><strong>Kubeflow Notebooks</strong>: per-user Jupyter / VSCode in K8s with PVCs + GPU.</p>
    <p><strong>Katib</strong>: hyperparameter tuning (random / Bayesian / NAS); spawns trial Pods.</p>
    <p><strong>Model Registry</strong>: versioned model artifacts; integrates with KServe."""),
        Section(eyebrow="Section 1.3 · KServe",
            h2="Inference with InferenceService + autoscaling + canary",
            body_html="""    <p><strong>KServe</strong>: K8s-native inference platform. <code>InferenceService</code> CRD declares predictor (e.g., vLLM / Triton / TensorFlow Serving) + transformer + explainer.</p>
    <p>Autoscaling via Knative serverless OR HPA. Canary traffic split per InferenceService revision (10% canary → 100%). Multi-model serving + custom protocols.</p>
    <p>Integrates with Model Registry for versioned model rollout. ServingRuntime CRD bundles per-framework runtime templates."""),
        Section(eyebrow="Section 1.4 · JobSet", h2="multi-pod jobs primitive",
            body_html="""    <p><strong>JobSet</strong> (K8s SIG): replaces the legacy ParallelMaster pattern. Declares N replicaJobs (each a Job spec) + completionMode + failurePolicy. Designed for distributed training, MPI, gang-scheduled batch.</p>
    <p>Integrates with Kueue (admission) + Volcano (gang scheduling). Common pattern: PyTorchJob / RayJob → JobSet → Pods.</p>
    <p>JobSet controller GA-ready in K8s 1.32+. Replaces bespoke per-framework job management for multi-pod workloads."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="When pick KubeRay vs Kubeflow training operator?",
            options=[("Always Kubeflow.", False), ("KubeRay for distributed Python (Ray Core / Tune / Train); Kubeflow operators for framework-specific (PyTorch / TF / MPI).", True), ("Always KubeRay.", False)],
            feedback="KubeRay shines for general distributed Python + RL + HPO. Kubeflow operators are framework-specific + integrate with the rest of Kubeflow (Pipelines / Katib)."),
        3: PauseCheck(question="What does JobSet replace?",
            options=[("kube-scheduler.", False), ("Bespoke per-framework multi-pod job management; foundation primitive for gang-compatible batch.", True), ("ResourceQuota.", False)],
            feedback="JobSet is the SIG-Apps primitive for multi-pod jobs. Frameworks (PyTorchJob / RayJob / MPIJob) increasingly use JobSet under the hood."),
    },
    before_after_before='<p>Pre-K8s-native ML tooling, ML workflows ran on bespoke VMs / Slurm / EC2 + boto3. Pipelines hand-orchestrated; serving = Flask app + Nginx; HPO bespoke. Data scientists were also infra engineers.</p>',
    before_after_after='<p>Modern: KubeRay for distributed compute; Kubeflow for training + pipelines + HPO + Notebooks; KServe for inference; JobSet for multi-pod jobs. Data scientists write Python / YAML; platform handles the rest.</p>',
    before_after_caption='<p class="ba-caption"><em>K8s-native ML tooling lets data scientists be data scientists.</em></p>',
    analogy_intro_html='''<p>Research Hall has four equipment kits. <strong>KubeRay</strong>: distributed-computation rig — many CPUs / GPUs cooperating on one task. <strong>Kubeflow</strong>: framework-specific tooling — PyTorch / TF / MPI training operators + pipelines + Notebooks + HPO. <strong>KServe</strong>: serving counter — production inference with autoscale + canary. <strong>JobSet</strong>: multi-pod-job primitive — the K8s-native foundation for the others.</p>''',
    translation_rows=[
        ("Distributed-computation rig", "KubeRay (RayCluster / RayJob / RayService)"),
        ("PyTorch training operator", "Kubeflow PyTorchJob"),
        ("TF training operator", "Kubeflow TFJob"),
        ("MPI training operator", "Kubeflow MPIJob"),
        ("Pipeline DAG engine", "Kubeflow Pipelines"),
        ("Per-user Jupyter", "Kubeflow Notebooks"),
        ("HPO sweep engine", "Katib"),
        ("Inference counter", "KServe InferenceService"),
        ("Multi-pod-job primitive", "JobSet"),
    ],
    analogy_stops="A research lab has fixed bench layout; K8s ML tooling evolves continuously — new operators, new servers, new gang patterns. Stay current.",
    eli5="Four kits in the research hall. One for distributed compute, one for training, one for serving, one for multi-pod jobs. Pick the right kit for the right ML phase.",
    eli10="<strong>KubeRay</strong>: Ray on K8s; RayCluster + RayJob + RayService. <strong>Kubeflow</strong>: Training Operator (PyTorchJob / TFJob / MPIJob) + Pipelines + Notebooks + Katib + Model Registry. <strong>KServe</strong>: InferenceService with autoscale + canary; ServingRuntime templates. <strong>JobSet</strong>: K8s SIG primitive for multi-pod jobs.",
    scenarios=[
        Scenario(name="KubeRay distributed training", body="Ray Train scaled across 32 H100s via KubeRay. Data scientist writes Ray Train script; KubeRay materialises cluster; auto-scaling workers; checkpoints to S3."),
        Scenario(name="Kubeflow Pipelines for ETL → train → eval", body="Daily DAG: data prep → PyTorchJob train → Katib HPO → eval → Model Registry → KServe deploy. Pipeline runs unattended; failures alarm."),
        Scenario(name="KServe canary rollout", body="New model version deployed as KServe revision; 10% canary; observability shows latency + accuracy; auto-promote at 24h SLO pass."),
        Scenario(name="Outage — non-K8s-native ML rolled out manually", body="Pre-Kubeflow team manually rolled inference; canary scripts buggy; latency spike rolled out to 100% before noticed. Postmortem: KServe canary + auto-rollback."),
    ],
    misconceptions=[
        Misconception(myth="\"Pick one ML framework; ignore others.\"", truth="Most orgs use multiple — PyTorch for research, TF for serving, MPI for HPC, Ray for distributed Python. Kubeflow + KubeRay supports all; pick per workload."),
        Misconception(myth="\"KServe is just an Ingress for ML.\"", truth="KServe adds: framework-specific predictors, autoscaling (Knative or HPA), canary, multi-model serving, custom protocols, model registry integration. Ingress alone is missing all of that."),
        Misconception(myth="\"JobSet is too new.\"", truth="K8s 1.32+ stable. SIG-Apps mature; foundation for next-gen multi-pod jobs."),
    ],
    flashcards=[
        Flashcard(front="KubeRay three CRDs?", back="<strong>RayCluster</strong> (long-running), <strong>RayJob</strong> (one-shot), <strong>RayService</strong> (serving)."),
        Flashcard(front="Kubeflow Training Operator job kinds?", back="<strong>PyTorchJob</strong>, <strong>TFJob</strong>, <strong>MPIJob</strong>, <strong>XGBoostJob</strong>, <strong>PaddleJob</strong>."),
        Flashcard(front="What does Kubeflow Pipelines do?", back="DAG workflow engine (Argo-based) for ML — preprocess → train → eval → deploy. Reusable components + parameterized."),
        Flashcard(front="KServe InferenceService components?", back="<strong>predictor</strong> (per-framework runtime: vLLM / Triton / TF Serving / sklearn), <strong>transformer</strong> (pre/post-processing), <strong>explainer</strong> (interpretability)."),
        Flashcard(front="KServe autoscaling options?", back="<strong>Knative serverless</strong> (scale-to-zero on idle) or <strong>HPA</strong> (CPU / mem / requests). Knative for bursty / cost-sensitive; HPA for steady."),
        Flashcard(front="JobSet vs Job?", back="<strong>Job</strong> = single-template parallel Pods. <strong>JobSet</strong> = multiple Job templates (replicaJobs) — for distributed training where each replica may differ."),
        Flashcard(front="Katib — what does it do?", back="HPO (hyperparameter optimization) — random / Bayesian / TPE / NAS. Spawns Trial Pods; collects metrics; converges to best params."),
        Flashcard(front="ServingRuntime in KServe?", back="Per-framework runtime template — declares container image + protocol + capabilities. ServingRuntime <code>kserve-vllm</code> + InferenceService picks it for vLLM serving."),
    ],
    quizzes=[
        Quiz(prompt="Design end-to-end ML platform: data prep → train → eval → serve.",
            answer="(1) <strong>Kubeflow Pipelines</strong>: DAG. (2) <strong>Step 1: data prep</strong> = container reading from S3, transforming, writing to S3. (3) <strong>Step 2: train</strong> = PyTorchJob (Kubeflow Training Operator) or RayJob (KubeRay) gang-scheduled by Volcano + admitted by Kueue. (4) <strong>Step 3: HPO</strong> = Katib Experiment with PyTorchJob trial template. (5) <strong>Step 4: eval</strong> = container; metrics to Model Registry. (6) <strong>Step 5: deploy</strong> = KServe InferenceService update; canary 10% then 100%. (7) <strong>Observability</strong>: Pipelines UI shows DAG; KServe metrics + traces."),
        Quiz(prompt="ML team\'s training jobs are bespoke shell scripts on EC2. Walk migration to Kubeflow.",
            answer="(1) <strong>Identify training framework</strong>: PyTorch / TF / MPI? Pick matching Kubeflow operator. (2) <strong>Containerise</strong>: training script in Docker image with framework + deps. (3) <strong>PyTorchJob YAML</strong> with replicas + GPU spec + S3-mounted data. (4) <strong>Kueue</strong> admission to GPU pool. (5) <strong>Volcano</strong> gang-schedule for multi-pod. (6) <strong>Pipeline</strong>: wrap in Kubeflow Pipelines for reproducibility. (7) <strong>Validate</strong>: same training accuracy + faster iteration loop."),
        Quiz(prompt="The CFO sees Kubeflow + KubeRay + KServe overhead. Defend.",
            answer="\"<strong>Each operator solves a class of bespoke work — bespoke means slow + error-prone.</strong> Three reasons stack stays: (1) <strong>Reproducibility</strong>: Pipelines DAGs reproducible across environments; bespoke scripts are not. (2) <strong>HPO</strong>: Katib runs 100s of trials in parallel; bespoke would run sequentially or skip HPO entirely. (3) <strong>Production serving</strong>: KServe canary + autoscale built-in; bespoke serving = roll-your-own-Ingress + bugs. <strong>Operator overhead</strong>: each is one Helm chart + few CRDs; minor. <strong>Saved engineer-time</strong>: data scientists write models, not boto3.\"", cyoa=True, cyoa_tag="how the platform engineer defended Kubeflow stack"),
    ],
    glossary=[
        GlossaryItem(name="KubeRay", definition="Ray on K8s operator. RayCluster + RayJob + RayService."),
        GlossaryItem(name="Ray", definition="Distributed Python framework — Ray Core + Train + Tune + Serve + RLlib."),
        GlossaryItem(name="Kubeflow Training Operator", definition="PyTorchJob / TFJob / MPIJob / XGBoostJob / PaddleJob distributed training operators."),
        GlossaryItem(name="Kubeflow Pipelines", definition="Argo-based ML workflow engine. DAGs + reusable components + parameterized."),
        GlossaryItem(name="Kubeflow Notebooks", definition="Per-user Jupyter / VSCode / RStudio in K8s with PVCs + GPU."),
        GlossaryItem(name="Katib", definition="Hyperparameter optimization — random / Bayesian / TPE / NAS. Spawns trial Pods."),
        GlossaryItem(name="KServe", definition="K8s-native inference. InferenceService + ServingRuntime + autoscale + canary."),
        GlossaryItem(name="InferenceService (KServe)", definition="CRD declaring predictor + transformer + explainer + autoscale."),
        GlossaryItem(name="ServingRuntime", definition="KServe per-framework runtime template (vLLM / Triton / TF Serving / sklearn)."),
        GlossaryItem(name="JobSet", definition="K8s SIG multi-pod jobs primitive; replicaJobs + completionMode + failurePolicy."),
    ],
    recap_lead="KubeRay = distributed compute. Kubeflow = training + pipelines + HPO + Notebooks + Model Registry. KServe = inference with autoscale + canary. JobSet = multi-pod jobs primitive. Combine via Kueue + Volcano.",
    recap_next='<strong>Next — I4: LLM serving (vLLM / TGI / Triton / NIM / llm-d).</strong>',
)
