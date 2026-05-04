"""K-ADV-AI I7 — GPU sharing + multi-tenant security + cost optimization."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GPU sharing + multi-tenant + cost."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Sharing Committee · K-Observatory — share + isolate + economise expensive telescopes</text><rect x="40" y="70" width="200" height="100" rx="10" fill="#3F4A5E"/><text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">GPU sharing</text><text x="140" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">MIG / time-slice / DRA</text><rect x="260" y="70" width="200" height="100" rx="10" fill="#5DCAA5"/><text x="360" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">multi-tenant security</text><text x="360" y="108" text-anchor="middle" font-size="9" fill="#1F2433">namespace + quota + MIG isolate</text><rect x="480" y="70" width="240" height="100" rx="10" fill="#FF9900"/><text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">cost optimisation</text><text x="600" y="108" text-anchor="middle" font-size="9" fill="#1F2433">Spot + reclaim + queue + RIs</text></svg>"""


LESSON = LessonSpec(
    num="07", title_short="GPU sharing + tenant + cost", title_full="I7 · GPU Sharing + Multi-Tenant GPU Security + Cost Optimization",
    title_html="K-ADV-AI I7 · Sharing + Tenant + Cost", module_eyebrow="Module I7 · Sharing Committee — share + isolate + economise expensive telescopes",
    hero_sub_html='<strong>GPU sharing</strong>: MIG (hardware partition) + time-slicing (software) + DRA (structured) + MPS (multi-process). <strong>Multi-tenant security</strong>: namespace isolation + GPU Quota + MIG isolation between tenants + node taints/tolerations + per-tenant token budgets at AI Gateway. <strong>Cost optimization</strong>: Spot GPU + idle reclaim + Kueue queue + Reserved Instances / Savings Plans / CUDs + ARM-based (Grace Hopper, Hopper Superchip), right-sizing.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. ML cluster bill 60% over budget; tenants share GPUs without isolation; one tenant\'s rogue script consumed entire cluster. <em>GPUs are the most expensive resource; sharing without governance + cost controls is unsustainable</em>. Today\'s lesson: share + isolate + economise.",
    stamp_html="<strong>Share via MIG / time-slice / DRA. Isolate via namespace + Quota + MIG. Economise via Spot + idle reclaim + Kueue queue + RIs/SP/CUDs + right-size. The expensive GPU deserves utilization + governance + cost discipline.</strong>",
    district_pin="kai-array07", district_label="Sharing Committee",
    sections=[
        Section(eyebrow="Section 1.1 · GPU sharing strategies",
            h2="MIG vs time-slicing vs DRA vs MPS",
            body_html="""    <p><strong>MIG (Multi-Instance GPU)</strong>: hardware-isolated partition (H100/A100). Each instance has dedicated SMs + memory + L2. Strong isolation; up to 7 partitions / GPU.</p>
    <p><strong>Time-slicing</strong>: software-shared via NVIDIA driver; multiple Pods per GPU; round-robin GPU access. Lower isolation; oversubscription possible.</p>
    <p><strong>DRA</strong>: structured-parameter scheduling; supports MIG + time-slicing + custom; multi-vendor.</p>
    <p><strong>MPS (Multi-Process Service)</strong>: NVIDIA library allowing multiple processes share GPU concurrently (vs serialised). Different from time-slicing; useful for many-small-process inference.</p>"""),
        Section(eyebrow="Section 1.2 · multi-tenant GPU security",
            h2="Isolation primitives + tenant boundary",
            body_html="""    <p>GPU multi-tenancy needs <em>both</em> K8s isolation + GPU isolation:</p>
    <ul>
      <li><strong>Namespace + RBAC + NetPol + Quota</strong> (per K-ADV-SEC patterns).</li>
      <li><strong>MIG instances</strong>: hardware-isolated; tenant boundary at MIG instance level; one tenant\'s instance can\'t affect another\'s.</li>
      <li><strong>Time-slicing isolation gap</strong>: shared GPU memory; one Pod\'s OOM can crash sibling Pods. Acceptable for trusted-tenant; risky for untrusted.</li>
      <li><strong>Node taint per tenant</strong>: dedicate certain GPU nodes to specific tenants for hard isolation.</li>
      <li><strong>AI Gateway per-tenant token budget</strong>: prevent runaway requests at L7.</li>
    </ul>"""),
        Section(eyebrow="Section 1.3 · cost optimisation tactics",
            h2="Spot + idle reclaim + Kueue queue + RIs + ARM",
            body_html="""    <p><strong>Spot GPU</strong>: 60-90% discount; reclaimed on short notice. Tolerable for batch / training / fault-tolerant inference. Pair with checkpointing.</p>
    <p><strong>Idle reclaim</strong>: detect idle GPUs (no process for N min); auto-evict; rejoin to general pool.</p>
    <p><strong>Kueue queue</strong>: hold low-priority jobs until capacity; preempt for high-priority.</p>
    <p><strong>RIs / Savings Plans / CUDs</strong>: 30-50% discount on baseline GPU capacity.</p>
    <p><strong>ARM-based GPUs</strong>: NVIDIA Grace Hopper / GH200 — ARM CPU + Hopper GPU; cheaper for compatible workloads.</p>
    <p><strong>Right-sizing</strong>: many workloads request whole GPU but use 20%; MIG into 1g.10gb cuts cost 4×."""),
        Section(eyebrow="Section 1.4 · operational fabric",
            h2="Quotas + dashboards + chargeback",
            body_html="""    <p>Per-tenant <strong>GPU Quota</strong> at K8s + Kueue level. <strong>OpenCost / Kubecost</strong> shows GPU cost / tenant; alerts at 75% / 95% of budget.</p>
    <p><strong>Chargeback</strong>: GPU bill allocated to tenant; visible in their P&L. Drives self-tune (right-sizing, MIG adoption, Spot).</p>
    <p><strong>Idle GPU dashboard</strong>: surface DCGM metrics; alarm on &lt; 20% utilization for &gt; 1 hour. Tenant + platform team review monthly.</p>"""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="When pick MIG over time-slicing?",
            options=[("Always.", False), ("When isolation matters: tenant security; predictable QoS; production inference.", True), ("Never.", False)],
            feedback="MIG hardware-isolates; time-slicing shares more freely. Isolation needs → MIG; elastic sharing → time-slice."),
        3: PauseCheck(question="A tenant\'s GPU bill jumped 3× last month. First action?",
            options=[("Increase quota.", False), ("Pull DCGM utilization data + Kubecost dashboard; identify which Pod / job; right-size or migrate to MIG / Spot.", True), ("Block the tenant.", False)],
            feedback="Investigate before rate-limiting. Often the answer is right-sizing / MIG adoption / Spot. Cost transparency drives the conversation."),
    },
    before_after_before='<p>Pre-controls, GPU clusters operated like dev clusters — no quota, no sharing, no isolation, no cost transparency. Bills surprised; one tenant could DoS; underutilization rampant.</p>',
    before_after_after='<p>Modern: MIG / time-slicing / DRA for sharing; namespace + Quota + MIG isolation for security; Spot + idle reclaim + Kueue + RIs + chargeback for economics. GPU clusters operated like the expensive resource they are.</p>',
    before_after_caption='<p class="ba-caption"><em>Share + isolate + economise. The GPU is the most expensive resource; treat it that way.</em></p>',
    analogy_intro_html='''<p>The Sharing Committee at the observatory governs telescope use. Telescopes are split into eyepieces (MIG); some shared by appointment (time-slicing); booking goes through committee (DRA / Kueue). Different astronomer groups have isolated telescope sessions (namespace + Quota); the committee tracks per-group usage + sends monthly bills (chargeback). Idle telescopes get reclaimed (idle reclaim); cheap rental telescopes available for fault-tolerant work (Spot).</p>''',
    translation_rows=[
        ("Eyepiece partition", "MIG instance"),
        ("Shared appointment", "Time-slicing"),
        ("Multi-vendor booking", "DRA"),
        ("Concurrent processes per telescope", "MPS"),
        ("Astronomer group session", "Namespace + per-tenant Quota"),
        ("Hardware isolation across groups", "MIG isolation between tenants"),
        ("Cheap rental telescope", "Spot GPU"),
        ("Auto-reclaim idle telescopes", "Idle GPU reclaim"),
        ("Booking queue", "Kueue priority + queue"),
        ("Long-term lease discount", "RIs / Savings Plans / CUDs"),
    ],
    analogy_stops="A telescope is fixed; GPU sharing is software-defined + driver-mediated. MIG is more rigid than time-slicing; DRA more flexible than both.",
    eli5="Telescopes are expensive. Split them into eyepieces (MIG) so 7 astronomers share. Different groups have isolated time. Cheap rental scopes for chores. Bill each group; recover idle scopes.",
    eli10="<strong>Sharing</strong>: MIG (hardware partition) / time-slicing (software) / DRA (structured) / MPS (multi-process). <strong>Multi-tenant security</strong>: namespace + Quota + MIG isolation + node taint per tenant + AI Gateway token budget. <strong>Cost</strong>: Spot + idle reclaim + Kueue queue + RIs/SP/CUDs + ARM (Grace Hopper) + right-size + chargeback.",
    scenarios=[
        Scenario(name="MIG cut inference cost 4×", body="Inference fleet on whole H100s; each Pod 20% util. MIG 1g.10gb per Pod; one H100 → 7 Pods; cost / Pod 4× lower; same throughput."),
        Scenario(name="Spot GPU for training", body="Fault-tolerant training adopted Spot G5 + Spot G6 fleet; checkpoint every 15 min; reclaim handled gracefully. Cost dropped 70%; training time +5% (recovery from interruptions)."),
        Scenario(name="Chargeback drove right-sizing", body="Showback dashboards revealed top spenders. Teams right-sized: whole-GPU → MIG 3g.40gb; whole-GPU → MIG 1g.10gb for inference. Aggregate GPU bill dropped 35% over a quarter."),
        Scenario(name="Outage — shared time-slicing crashed sibling Pods", body="Time-slicing deployed; one Pod\'s GPU OOM crashed all sibling Pods. Postmortem: MIG for production; time-slice OK for dev / experimental only."),
    ],
    misconceptions=[
        Misconception(myth="\"Time-slicing is always cheaper than MIG.\"", truth="Both share GPU; time-slicing oversubscribes (more Pods possible) but isolation gaps cost recovery time. MIG fixed-cost; time-slicing variable-cost. Workload + isolation needs decide."),
        Misconception(myth="\"Spot GPU is too unreliable for ML.\"", truth="With checkpointing, Spot is fine for fault-tolerant training. Inference: tolerated for stateless + dynamic-route patterns; not for low-latency-critical."),
        Misconception(myth="\"GPU chargeback is too political.\"", truth="GPUs are the most expensive resource; chargeback aligns engineering + finance. Same logic as cloud chargeback in K-ADV-PE; just bigger numbers."),
    ],
    flashcards=[
        Flashcard(front="Four GPU sharing strategies?", back="<strong>MIG</strong> (hardware partition; isolation), <strong>time-slicing</strong> (software shared; oversubscription), <strong>DRA</strong> (structured multi-vendor), <strong>MPS</strong> (multi-process concurrent on one GPU)."),
        Flashcard(front="When MIG over time-slicing?", back="Tenant security; production isolation; predictable QoS. Time-slicing for dev / experimental / cooperative workloads."),
        Flashcard(front="Spot GPU — what makes a workload fit?", back="Fault-tolerance — checkpointing + retry; not low-latency-critical inference. Training + batch + queue consumers."),
        Flashcard(front="Idle reclaim — what does it do?", back="DCGM detects no GPU process for N min; eviction policy reclaims to general pool; reduces idle waste."),
        Flashcard(front="ARM-based GPU options?", back="<strong>NVIDIA Grace Hopper / GH200</strong> — ARM CPU + Hopper GPU; cheaper / lower power for compatible workloads."),
        Flashcard(front="Multi-tenant GPU isolation primitives?", back="Namespace + Quota + MIG instance + node taint per tenant + AI Gateway token budget. Layered defence."),
        Flashcard(front="GPU Quota — where set?", back="Per-namespace ResourceQuota with <code>requests.nvidia.com/gpu</code> + Kueue ClusterQueue + per-tier defaults."),
        Flashcard(front="Right-sizing GPU — how to identify?", back="DCGM utilization metrics per Pod; sustained &lt; 30% util = right-size candidate (MIG smaller instance / cheaper GPU model)."),
    ],
    quizzes=[
        Quiz(prompt="Design GPU multi-tenancy + cost for a 50-engineer ML org.",
            answer="(1) <strong>Per-team namespace</strong> + RBAC + NetPol. (2) <strong>GPU Quota per tier</strong> (gold = 10 H100 / silver = 4 / bronze = 1). (3) <strong>MIG-enabled nodes</strong>: H100s partitioned 7×1g.10gb for inference; whole-H100 for training; nodeSelector picks pool. (4) <strong>Kueue admission</strong> per tenant + cohort lending. (5) <strong>Spot fleet</strong> for fault-tolerant training (G5/G6). (6) <strong>OpenCost / Kubecost</strong>: per-tenant chargeback. (7) <strong>Budget alerts</strong>: 75% / 95% / 100% of monthly. (8) <strong>Idle reclaim</strong>: DCGM monitoring + alert + auto-reclaim DaemonSet."),
        Quiz(prompt="A tenant\'s prod inference is unstable on time-sliced GPUs. Walk fix.",
            answer="(1) <strong>Symptom</strong>: time-sliced GPU OOMs cascade across sibling Pods. (2) <strong>Root cause</strong>: time-slicing shares GPU memory; one Pod\'s leak crashes all. (3) <strong>Fix</strong>: migrate prod to MIG instances (hardware-isolated). Inference Pods → 1g.10gb / 2g.20gb. (4) <strong>Validate</strong>: stress-test one Pod\'s OOM; sibling Pods unaffected. (5) <strong>Operational</strong>: time-slicing reserved for dev / experimental; MIG for prod."),
        Quiz(prompt="The CFO asks: \"why GPU bill 60% over forecast?\" Walk diagnostic.",
            answer="\"<strong>Walk Kubecost dashboards top-down.</strong> (1) <strong>Per-tenant cost</strong>: which tenants drove the spike? (2) <strong>Per-Pod cost</strong>: which Pods? Sustained or burst? (3) <strong>DCGM utilization</strong>: are Pods using GPUs (or wasting expensive resources)? (4) <strong>Workload class</strong>: inference / training / experimental? (5) <strong>Action</strong>: right-size (MIG) for low-util; Spot for fault-tolerant; quotas tightened for runaway tenant. <strong>Outcome</strong>: typical 30-40% reduction within a quarter via right-sizing + Spot adoption + idle reclaim. <strong>The 60% overage is fixable; the GPU model isn\'t the issue — utilization + sharing strategy is.</strong>\"", cyoa=True, cyoa_tag="how the platform engineer answered the CFO"),
    ],
    glossary=[
        GlossaryItem(name="MIG", definition="Multi-Instance GPU; hardware partition; H100/A100 only."),
        GlossaryItem(name="time-slicing", definition="Software-shared GPU; multiple Pods round-robin; oversubscription."),
        GlossaryItem(name="DRA", definition="Dynamic Resource Allocation; structured-parameter scheduling; multi-vendor."),
        GlossaryItem(name="MPS", definition="Multi-Process Service; NVIDIA library; multiple processes share GPU concurrently."),
        GlossaryItem(name="Spot GPU", definition="Cheaper preemptible GPU; reclaimed on short notice; needs checkpointing."),
        GlossaryItem(name="idle reclaim", definition="Auto-evict idle GPUs; rejoin to general pool."),
        GlossaryItem(name="Grace Hopper / GH200", definition="NVIDIA ARM CPU + Hopper GPU; cheaper / lower-power."),
        GlossaryItem(name="DCGM utilization", definition="GPU usage % via DCGM exporter; foundation of right-sizing."),
        GlossaryItem(name="GPU Quota", definition="Per-namespace ResourceQuota on <code>nvidia.com/gpu</code> or MIG profile."),
        GlossaryItem(name="cohort (Kueue)", definition="Group of ClusterQueues lending idle quota."),
    ],
    recap_lead="GPU sharing (MIG / time-slicing / DRA / MPS) + multi-tenant security (namespace + Quota + MIG isolation) + cost optimization (Spot + idle reclaim + Kueue + RIs + ARM + right-sizing). The expensive GPU deserves discipline.",
    recap_next='<strong>Next — I8: Capstone — production AI inference platform.</strong>',
)
