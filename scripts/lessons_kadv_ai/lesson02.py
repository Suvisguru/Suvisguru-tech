"""K-ADV-AI I2 — Kueue + MultiKueue + Volcano gang scheduling."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Kueue + Volcano + MultiKueue."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Observation Queue · K-Observatory — admit + gang-schedule + federate</text><rect x="40" y="70" width="200" height="100" rx="10" fill="#3F4A5E"/><text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Kueue</text><text x="140" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">admit jobs to Quota</text><rect x="260" y="70" width="200" height="100" rx="10" fill="#5DCAA5"/><text x="360" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Volcano</text><text x="360" y="108" text-anchor="middle" font-size="9" fill="#1F2433">gang scheduling (all-or-nothing)</text><rect x="480" y="70" width="240" height="100" rx="10" fill="#FF9900"/><text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">MultiKueue</text><text x="600" y="108" text-anchor="middle" font-size="9" fill="#1F2433">federate fleets</text></svg>"""


LESSON = LessonSpec(
    num="02", title_short="Kueue + Volcano", title_full="I2 · Kueue + MultiKueue + Volcano Gang Scheduling",
    title_html="K-ADV-AI I2 · Kueue + Volcano", module_eyebrow="Module I2 · Observation Queue — admit + gang-schedule + federate",
    hero_sub_html='<strong>Kueue</strong> (CNCF): K8s-native job admission. ResourceFlavor + ClusterQueue + LocalQueue model capacity; admits Workloads (Jobs / JobSets / RayJobs / MPIJob) per quota. <strong>Volcano</strong>: gang scheduling — all-or-nothing for multi-Pod jobs. <strong>MultiKueue</strong>: federate Workloads across many clusters; submit once; runs anywhere with capacity.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Distributed training of 16 Pods stalled with 14 running + 2 stuck Pending. <em>K8s schedules Pods independently; multi-Pod jobs need all-or-nothing.</em> Today\'s lesson: Kueue + Volcano give batch admission + gang scheduling so multi-Pod jobs work.",
    stamp_html="<strong>Kueue: K8s batch admission with quota. Volcano: gang scheduling for multi-Pod jobs. MultiKueue: federate batch across many clusters. Together: AI / batch workloads with quota + admission + gang + fleet.</strong>",
    district_pin="kai-array02", district_label="Observation Queue",
    sections=[
        Section(eyebrow="Section 1.1 · Kueue model", h2="ResourceFlavor + ClusterQueue + LocalQueue + Workload",
            body_html="""    <p><strong>ResourceFlavor</strong>: cluster\'s capacity slice (e.g., \"H100-flavor\"). <strong>ClusterQueue</strong>: cluster-scoped queue declaring quota per ResourceFlavor + cohort + preemption rules. <strong>LocalQueue</strong>: namespace-scoped pointer to ClusterQueue. <strong>Workload</strong>: Kueue-tracked job (Job / JobSet / RayJob / MPIJob).</p>
    <p>Tenant submits Job to LocalQueue; Kueue admits if quota available; Pods then schedule normally."""),
        Section(eyebrow="Section 1.2 · Volcano gang scheduling",
            h2="all-or-nothing + min-member + queue priorities",
            body_html="""    <p><strong>Volcano</strong> scheduler runs alongside or replaces kube-scheduler. Schedules <em>PodGroup</em> (gang) atomically: all min-member Pods schedule together or none do.</p>
    <p>Avoids the half-running half-pending failure mode for distributed training. PodGroup priorities + queue admission supplement default scheduling."""),
        Section(eyebrow="Section 1.3 · MultiKueue federation",
            h2="Submit once; runs in any cluster with capacity",
            body_html="""    <p><strong>MultiKueue</strong>: control-plane Kueue cluster federates worker Kueue clusters. Tenant submits Workload to control plane; MultiKueue routes to worker cluster with capacity.</p>
    <p>Wins: <em>burst across clouds</em>, <em>multi-region GPU pools</em>, <em>spot-fallback</em>. ML platform spans many clusters; tenants see one queue."""),
        Section(eyebrow="Section 1.4 · workload kinds + integrations",
            h2="Job / JobSet / RayJob / MPIJob + Kubeflow integration",
            body_html="""    <p>Kueue admits standard K8s <strong>Job</strong> + <strong>JobSet</strong> (multi-pod) + <strong>RayJob</strong> (KubeRay) + <strong>MPIJob</strong> (Kubeflow MPI Operator) + <strong>PyTorchJob</strong> / <strong>TFJob</strong> (Kubeflow Training Operator).</p>
    <p>Pattern: Kubeflow Training Operator submits PyTorchJob → Kueue admits → Volcano gang-schedules → distributed training runs. End-to-end batch ML pipeline."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why use Kueue ClusterQueue?",
            options=[("Replaces ResourceQuota.", False), ("Adds quota-aware admission for batch jobs (vs ResourceQuota which is per-namespace static).", True), ("Required for K8s 1.32.", False)],
            feedback="Kueue ClusterQueue is admission with cohort + preemption + waiting-queue semantics; ResourceQuota is per-namespace static. Different concerns; both useful."),
        3: PauseCheck(question="Why gang scheduling for distributed training?",
            options=[("Faster than default.", False), ("All-or-nothing — N Pods start together or none do; avoids half-running half-pending hangs.", True), ("Required by NVIDIA.", False)],
            feedback="Distributed training needs all participants up to start; without gang, partial start hangs. Volcano gang-schedules atomically."),
    },
    before_after_before='<p>Pre-Kueue / Volcano, batch jobs hit ResourceQuota or scheduled per-Pod; distributed training half-stuck; multi-cluster batch impossible without bespoke routing.</p>',
    before_after_after='<p>Kueue admits per quota + cohort; Volcano gang-schedules; MultiKueue federates clusters. Tenants submit; platform handles routing + admission + gang.</p>',
    before_after_caption='<p class="ba-caption"><em>Batch + AI workloads need queue + gang + federation; default K8s scheduling alone isn\'t enough.</em></p>',
    analogy_intro_html='''<p>The Observation Queue is the observatory\'s scheduling office. Astronomers submit observation requests; the queue\'s admission desk (Kueue) checks quota + admits. The control-room scheduler (Volcano) ensures multi-telescope observations start together — no half-started observations. Multi-observatory federation (MultiKueue) routes observations to whichever facility has capacity.</p>''',
    translation_rows=[
        ("Observation request", "Workload (Job / JobSet / RayJob / MPIJob)"),
        ("Telescope kind quota", "ResourceFlavor + ClusterQueue"),
        ("Astronomer\'s queue ticket", "LocalQueue (namespace-scoped)"),
        ("Multi-telescope all-or-nothing", "Volcano gang scheduling"),
        ("Multi-observatory routing", "MultiKueue federation"),
        ("Quota cohort + preemption", "ClusterQueue cohort + preemption"),
    ],
    analogy_stops="A real observation queue is paper; Kueue is K8s CRDs continuously reconciled. Quota is dynamic (cohort lending); not just static.",
    eli5="A queue admits batch jobs to the cluster like a coffee shop\'s order line. A scheduler ensures multi-cup orders start together. A federation across shops finds a free counter.",
    eli10="<strong>Kueue</strong>: ResourceFlavor + ClusterQueue + LocalQueue + Workload model. Admits batch (Job / JobSet / RayJob / MPIJob / PyTorchJob) per quota. <strong>Volcano</strong>: gang-schedule PodGroup atomically; all-or-nothing. <strong>MultiKueue</strong>: federate Workloads across clusters; submit once. <strong>Integrations</strong>: KubeRay + Kubeflow Training Operator + MPI Operator.",
    scenarios=[
        Scenario(name="Distributed training — Volcano gang", body="ML team\'s 16-Pod PyTorchJob hung pending half-up. Migrated to Volcano: PodGroup admits 16 Pods together; training starts cleanly. Throughput up; partial-start incidents zero."),
        Scenario(name="Kueue cohort lending", body="Two teams share a GPU pool. Each has 8-GPU quota; cohort lends idle quota across teams. Team A bursts to 16 GPU when Team B idle; reverts when B requests. Utilization rises without contention."),
        Scenario(name="MultiKueue across clouds", body="ML platform fleets across AWS + GCP + on-prem. Tenants submit RayJobs to control-plane Kueue; MultiKueue routes per available capacity. Spot-fallback across clouds; tenant doesn\'t care which cloud."),
        Scenario(name="Outage — non-Kueue partial-fill", body="Pre-Kueue, Job\'s Pods scheduled greedily; partial-fill during high-demand; jobs deadlocked. Postmortem: adopt Kueue + Volcano; gang admit prevents."),
    ],
    misconceptions=[
        Misconception(myth="\"Kueue replaces ResourceQuota.\"", truth="They\'re complementary. ResourceQuota = per-namespace static cap. Kueue = batch admission + cohort + preemption. Both useful for different patterns."),
        Misconception(myth="\"Volcano replaces kube-scheduler.\"", truth="Volcano can either replace or run alongside kube-scheduler. Modern pattern: Volcano for gang-scheduled batch; kube-scheduler for everything else. Coexist."),
        Misconception(myth="\"MultiKueue is required for multi-cluster ML.\"", truth="Optional. MultiKueue is the K8s-native answer. Some platforms use Argo Workflows + custom routing; both work; MultiKueue is the standard for new builds."),
    ],
    flashcards=[
        Flashcard(front="Kueue four concepts?", back="<strong>ResourceFlavor</strong> (capacity slice), <strong>ClusterQueue</strong> (cluster quota + cohort + preemption), <strong>LocalQueue</strong> (namespace-scoped), <strong>Workload</strong> (Kueue-tracked job)."),
        Flashcard(front="What is gang scheduling?", back="All-or-nothing scheduling for multi-Pod jobs. N Pods (PodGroup min-member) start together or none start. Volcano implements."),
        Flashcard(front="MultiKueue what does it federate?", back="Workloads across worker Kueue clusters; control-plane Kueue routes per available capacity. Tenants see one queue; platform spans many clusters."),
        Flashcard(front="Cohort lending in Kueue?", back="Multiple ClusterQueues in same cohort can borrow idle quota from each other. Per-team quota stays the contract; bursts use cohort spare."),
        Flashcard(front="Workload kinds Kueue admits?", back="Job, JobSet, RayJob (KubeRay), MPIJob (MPI Operator), PyTorchJob / TFJob (Training Operator), plus custom CRDs via Kueue integration."),
        Flashcard(front="When use Volcano?", back="Multi-Pod jobs needing all-or-nothing (distributed training, MPI). Single-Pod jobs don\'t need it. Often run alongside kube-scheduler."),
        Flashcard(front="Kueue preemption?", back="Higher-priority Workload can preempt running lower-priority Workloads in the same cohort. Configurable per ClusterQueue."),
        Flashcard(front="Pattern for distributed training?", back="Kubeflow PyTorchJob / TFJob → Kueue admits → Volcano gang-schedules → training runs. End-to-end batch ML."),
    ],
    quizzes=[
        Quiz(prompt="Walk Kueue + Volcano setup for a multi-tenant ML cluster.",
            answer="(1) <strong>Install Kueue</strong> Helm + Volcano Helm. (2) <strong>ResourceFlavor</strong> per accelerator type (H100, A100). (3) <strong>ClusterQueue per team</strong> with quota + cohort \"ml-cohort\" for cohort lending. (4) <strong>LocalQueue</strong> in each tenant namespace. (5) <strong>PyTorchJob</strong> / <strong>RayJob</strong> annotation: <code>kueue.x-k8s.io/queue-name: ...</code>. (6) <strong>Volcano</strong>: PodGroup auto-created from Job; gang-schedules. (7) <strong>Validate</strong>: Kueue dashboards show admission queue depth + cohort utilization."),
        Quiz(prompt="MultiKueue across 3 clusters — design federation.",
            answer="(1) <strong>Pick control-plane cluster</strong>: small dedicated cluster running MultiKueue Admission webhook. (2) <strong>Worker clusters</strong>: each runs Kueue + ClusterQueue + ResourceFlavor matching the federation\'s capacity. (3) <strong>MultiKueue config</strong>: control plane registers worker cluster connections (kubeconfig + auth). (4) <strong>Tenant submits Workload</strong> to control plane; MultiKueue routes to worker. (5) <strong>Spot fallback</strong>: configure cohort priorities so on-demand cluster gets first dibs; spot cluster receives overflow."),
        Quiz(prompt="The CFO sees Volcano cost (yet-another-controller). Defend.",
            answer="\"<strong>Without gang scheduling, distributed training jobs deadlock — wasted GPU-hours.</strong> Three reasons Volcano stays: (1) <strong>Half-started jobs are catastrophic at GPU scale</strong>: 14/16 H100s allocated but training stuck = 14 H100s burning $$ doing nothing. (2) <strong>Operator overhead is small</strong>: Volcano is one Helm chart + a few CRDs; runs alongside kube-scheduler. (3) <strong>Standardisation</strong>: alternative is bespoke per-Job retry logic; Volcano is the upstream answer. <strong>Cost</strong>: trivial. <strong>Saved</strong>: hours of GPU-time per partial-start incident.\"", cyoa=True, cyoa_tag="how the platform engineer defended Volcano"),
    ],
    glossary=[
        GlossaryItem(name="Kueue", definition="CNCF K8s-native batch admission. ResourceFlavor + ClusterQueue + LocalQueue + Workload."),
        GlossaryItem(name="ResourceFlavor", definition="Capacity slice in Kueue (e.g., GPU type / Spot vs On-Demand)."),
        GlossaryItem(name="ClusterQueue", definition="Cluster-scoped quota + cohort + preemption + Workload admission."),
        GlossaryItem(name="LocalQueue", definition="Namespace-scoped pointer to ClusterQueue. Tenant\'s submission target."),
        GlossaryItem(name="Volcano", definition="Batch scheduler; gang scheduling for multi-Pod jobs (PodGroup)."),
        GlossaryItem(name="MultiKueue", definition="Federates Workloads across many clusters via control-plane / worker Kueue."),
        GlossaryItem(name="Workload (Kueue)", definition="Kueue-tracked job. Job / JobSet / RayJob / MPIJob / PyTorchJob / TFJob + custom."),
        GlossaryItem(name="cohort", definition="Group of ClusterQueues that lend each other idle quota."),
        GlossaryItem(name="gang scheduling", definition="All-or-nothing scheduling for multi-Pod jobs. Volcano implements."),
        GlossaryItem(name="PodGroup", definition="Volcano CRD declaring a gang. min-member Pods schedule atomically."),
    ],
    recap_lead="Kueue admits batch with quota + cohort; Volcano gang-schedules multi-Pod jobs; MultiKueue federates clusters. Together: AI / batch workloads with quota + admission + gang + fleet.",
    recap_next='<strong>Next — I3: Ray + Kubeflow + KServe + JobSet.</strong>',
)
