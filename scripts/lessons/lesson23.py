from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Dispatch Office VIP wing: a priority-class queue with high-priority trucks bumping low-priority ones, a resource-claim window where GPU drivers hand out specialized tools, and a NUMA-aware diagram showing CPU/memory pairs.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">DISPATCH OFFICE · VIP &amp; SPECIALTY ROUTING</text>
  <!-- Priority queue -->
  <g transform="translate(40,55)">
    <text x="55" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">PRIORITY LANE</text>
    <rect x="0" y="22" width="110" height="22" rx="3" fill="#A04832"/>
    <text x="6" y="36" font-size="8" font-weight="700" fill="#FFFFFF">P=1000 critical</text>
    <rect x="0" y="48" width="110" height="22" rx="3" fill="#E8B547"/>
    <text x="6" y="62" font-size="8" font-weight="700" fill="#5A4F45">P=500 prod</text>
    <rect x="0" y="74" width="110" height="22" rx="3" fill="#9D9389"/>
    <text x="6" y="88" font-size="8" font-weight="700" fill="#FFFFFF">P=10 batch</text>
    <text x="55" y="115" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">high preempts low</text>
    <text x="55" y="128" text-anchor="middle" font-size="7" fill="#6B6058" font-style="italic">low evicted to free room</text>
  </g>
  <!-- DRA / Resource Claims -->
  <g transform="translate(180,40)">
    <rect width="160" height="120" rx="6" fill="#FFFFFF" stroke="#3F4A5E" stroke-width="1.5"/>
    <text x="80" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">RESOURCE WINDOW · DRA</text>
    <rect x="14" y="24" width="60" height="32" rx="3" fill="#5A9F7A"/>
    <text x="44" y="38" text-anchor="middle" font-size="7" font-weight="700" fill="#FFFFFF">GPU H100</text>
    <text x="44" y="48" text-anchor="middle" font-size="6" fill="#FFFFFF">+ MIG slice</text>
    <rect x="86" y="24" width="60" height="32" rx="3" fill="#4A8FA8"/>
    <text x="116" y="38" text-anchor="middle" font-size="7" font-weight="700" fill="#FFFFFF">FPGA tile</text>
    <rect x="14" y="62" width="60" height="32" rx="3" fill="#D97757"/>
    <text x="44" y="76" text-anchor="middle" font-size="7" font-weight="700" fill="#FFFFFF">RDMA NIC</text>
    <rect x="86" y="62" width="60" height="32" rx="3" fill="#8B5A00"/>
    <text x="116" y="76" text-anchor="middle" font-size="7" font-weight="700" fill="#FFFFFF">SR-IOV VF</text>
    <text x="80" y="110" text-anchor="middle" font-size="8" fill="#3F4A5E" font-style="italic">ResourceClaim: \"I need 1 H100 with 80GB\"</text>
  </g>
  <!-- NUMA -->
  <g transform="translate(370,40)">
    <text x="80" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">NUMA · CPU + MEMORY pinning</text>
    <rect x="0" y="20" width="76" height="100" rx="4" fill="#E0EEF3" stroke="#4A8FA8" stroke-width="1.2"/>
    <text x="38" y="34" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">node 0</text>
    <rect x="6" y="42" width="64" height="22" rx="2" fill="#3F4A5E"/>
    <text x="38" y="56" text-anchor="middle" font-size="7" fill="#FBF7F0">CPU 0-7</text>
    <rect x="6" y="68" width="64" height="22" rx="2" fill="#5A4F45"/>
    <text x="38" y="82" text-anchor="middle" font-size="7" fill="#FBF7F0">RAM 64GB</text>
    <text x="38" y="105" text-anchor="middle" font-size="7" fill="#3F4A5E" font-style="italic">co-located</text>
    <rect x="84" y="20" width="76" height="100" rx="4" fill="#FBE8DC" stroke="#A04832" stroke-width="1.2"/>
    <text x="122" y="34" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">node 1</text>
    <rect x="90" y="42" width="64" height="22" rx="2" fill="#3F4A5E"/>
    <text x="122" y="56" text-anchor="middle" font-size="7" fill="#FBF7F0">CPU 8-15</text>
    <rect x="90" y="68" width="64" height="22" rx="2" fill="#5A4F45"/>
    <text x="122" y="82" text-anchor="middle" font-size="7" fill="#FBF7F0">RAM 64GB</text>
    <text x="122" y="105" text-anchor="middle" font-size="7" fill="#3F4A5E" font-style="italic">co-located</text>
  </g>
  <!-- Sched profile -->
  <g transform="translate(560,55)">
    <text x="0" y="14" font-size="9" font-weight="700" fill="#5A4F45">profiles</text>
    <rect x="0" y="22" width="80" height="20" rx="2" fill="#3F4A5E"/>
    <text x="6" y="35" font-size="7" fill="#FBF7F0">default</text>
    <rect x="0" y="46" width="80" height="20" rx="2" fill="#A04832"/>
    <text x="6" y="59" font-size="7" fill="#FBF7F0">batch-bin</text>
    <rect x="0" y="70" width="80" height="20" rx="2" fill="#5A9F7A"/>
    <text x="6" y="83" font-size="7" fill="#FBF7F0">latency-min</text>
    <text x="0" y="105" font-size="7" fill="#5A4F45" font-style="italic">multi-scheduler</text>
  </g>
  <text x="340" y="200" text-anchor="middle" font-size="11" fill="#3F4A5E" font-style="italic">Priority decides who waits in line. DRA decides who gets the specialty tools. NUMA decides whether your CPU and your RAM are even introduced.</text>
</svg>"""

LESSON = LessonSpec(
    num="23",
    title_short="scheduling Pt 2",
    title_full="Scheduling Part 2 · Priority, DRA, NUMA, Profiles",
    title_html="Lesson 23 — Scheduling Part 2: Priority, DRA, NUMA · K-COM",
    module_eyebrow="Module 11 · Lesson 23 · the advanced scheduler controls",
    hero_sub_html='When the cluster is full, who gets evicted? When a Pod needs a GPU with specific memory, how does the scheduler match it? When microsecond CPU latency matters, how do you keep code on the same NUMA node as its memory? Three advanced primitives: <strong>PriorityClass</strong>, <strong>Dynamic Resource Allocation (DRA, GA in 1.34)</strong>, and <strong>topology managers</strong>.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Black-Friday traffic peaks. The autoscaler is racing to spin up nodes but the cluster\'s saturated. The team\'s critical payment service is Pending — there\'s no room. Meanwhile, a 4-hour batch ML training job is happily eating four nodes\' worth of GPU. <em>The training job is not Black-Friday-critical, but the scheduler doesn\'t know that.</em> Result: payments degrade for 12 minutes while ops humans manually kill the training. The fix is <strong>PriorityClass + preemption</strong>: critical Pods get a priority of 1000, batch jobs get 10, and when the critical Pod can\'t fit, the scheduler evicts the batch automatically. Today\'s lesson.',
    stamp_html='<strong>PriorityClass + preemption</strong> decides who runs when the cluster is full. <strong>Dynamic Resource Allocation (DRA)</strong> — GA in K8s 1.34 — replaces ad-hoc device plugins with a structured CRD model for GPUs, FPGAs, NICs. <strong>Topology Manager</strong> + <strong>CPU Manager</strong> keep latency-sensitive workloads on the same NUMA node as their memory.',
    district_pin="kt-pin16",
    district_label="Dispatch Office — VIP & Specialty Routing",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="When the cluster is full, who wins?",
            body_html="""    <p>The basic scheduler (Lesson 22) places Pods on nodes that fit them. But when nothing fits, by default the Pod just stays Pending. That's fine for batch work; it's terrible for production traffic-serving workloads. <strong>Pod priority + preemption</strong> tells the scheduler: "if this Pod can't fit, evict lower-priority Pods to make room."</p>
    <p>You define a <code>PriorityClass</code> object cluster-wide (<code>system-cluster-critical</code> = 2000000000, <code>system-node-critical</code> = 2000001000 are reserved; user-defined classes typically range from 0 to 1 billion). Pods reference a <code>priorityClassName</code>. When a high-priority Pod can't be scheduled, the scheduler picks the lowest-priority Pod(s) it can evict to free up the resources, evicts them (gracefully, with a configurable termination grace period), and places the high-priority Pod.</p>
    <p>The classic three-tier setup: <code>critical</code> (=1000) for traffic-serving workloads, <code>standard</code> (=500) for the rest of production, <code>batch</code> (=10) for non-urgent work. Add an <code>opportunistic</code> (=-100) for spot-instance throwaway work that gets nuked first. Most clusters need exactly this hierarchy.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Dynamic Resource Allocation (DRA)",
            h2="GPUs (and friends) get a structured API — GA in 1.34",
            body_html="""    <p>For years, "give my Pod a GPU" was implemented via the device-plugin API: a privileged DaemonSet on the node, an ad-hoc <code>resources.limits: nvidia.com/gpu: 1</code> field, no support for sharing, no support for "I want a GPU with at least 80GB," no support for FPGAs / RDMA NICs / SR-IOV VFs as first-class objects. It was a hack that lasted a decade.</p>
    <p><strong>Dynamic Resource Allocation (DRA)</strong> — GA in Kubernetes 1.34 — replaces device plugins with a proper API:</p>
    <ul>
      <li><strong>DeviceClass</strong> — cluster-scoped: "this is a class of devices, here's what attributes they have, here's the driver."</li>
      <li><strong>ResourceClaim</strong> — namespace-scoped: a Pod's request for a device — \"I need an H100 with at least 80 GiB and CUDA 12.4.\"</li>
      <li><strong>ResourceClaimTemplate</strong> — like a PVC template: a Pod can ask for a one-shot claim that gets created and torn down with the Pod.</li>
      <li><strong>ResourceSlice</strong> — the kubelet publishes one per node, listing the actual devices available with their attributes.</li>
    </ul>
    <p>DRA solves what device plugins couldn't: structured attributes (CEL expressions in claims), partitioned devices (MIG slices), inter-Pod sharing of a device (one ResourceClaim → multiple Pods), and the basic dignity of being a real K8s object.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>If you're starting a fresh cluster on K8s 1.34+, use DRA from day 1. If you're on an older cluster, the device plugin API still works — and the major vendors (NVIDIA, Intel, AMD) ship both DRA drivers and legacy device plugins for the transition. The migration is being driven by NVIDIA's MIG (Multi-Instance GPU) story; sharing a single H100 across multiple Pods isn't really expressible without DRA.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · NUMA, CPU pinning, Topology Manager",
            h2="When microseconds matter",
            body_html="""    <p>Modern servers have multiple <strong>NUMA nodes</strong> — physically separate CPU sockets each with attached RAM. Accessing memory on the local NUMA node is fast (~80ns); going across the inter-socket link to memory on another NUMA node is 2-3× slower. For latency-sensitive workloads (HFT, real-time inference, NFV), this matters.</p>
    <p>K8s exposes three coordinated managers:</p>
    <ul>
      <li><strong>CPU Manager</strong> (kubelet feature) — with <code>policy: static</code>, dedicates whole CPU cores to Guaranteed-QoS Pods that ask for integer CPU. Other Pods stay off those cores. Removes context-switching jitter.</li>
      <li><strong>Memory Manager</strong> — pins memory allocation to specific NUMA nodes.</li>
      <li><strong>Topology Manager</strong> — coordinates the above plus device assignments (GPUs, NICs) so they all land on the same NUMA node. <code>policy: single-numa-node</code> = enforce same-NUMA; <code>restricted</code> = allow cross-NUMA but flag; <code>best-effort</code> = try, don't enforce.</li>
    </ul>
    <p>Combined effect: a latency-sensitive Pod gets dedicated CPU cores, RAM allocated on the same NUMA node, and (if it asked for one) a GPU/NIC also on that NUMA node. Nothing crosses the inter-socket link. Tail latency drops by 20-50% in extreme cases.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Scheduler profiles + multiple schedulers",
            h2="When one scheduler isn't enough",
            body_html="""    <p>A <strong>scheduler profile</strong> is a named configuration of the kube-scheduler's plugins, scores, and weights. The default profile (<code>default-scheduler</code>) handles every Pod that doesn't specify <code>spec.schedulerName</code>. You can run multiple profiles in the same kube-scheduler process for different workload types — or run a separate scheduler binary entirely.</p>
    <p>Common patterns:</p>
    <ul>
      <li><strong>Bin-packing for batch:</strong> a profile with <code>NodeResourcesFit: scoring=MostAllocated</code> packs Pods tightly to maximise spot-eviction efficiency. Default profile uses <code>LeastAllocated</code> for spread.</li>
      <li><strong>Latency-optimised profile:</strong> heavy weight on <code>InterPodAffinity</code> + <code>NodeAffinity</code> + <code>TopologyManager</code> hint, lighter on resource utilisation.</li>
      <li><strong>Volcano / Yunikorn:</strong> entirely separate batch schedulers for ML training (gang scheduling, queues, fair-share).</li>
    </ul>
    <p>The custom-plugin SDK lets you write Go plugins for filter/score/permit/reserve/postBind phases. Most users don't need this — they need to combine existing plugins differently. But for the cases that do need it, the SDK is mature.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A K8s 1.34 cluster has a critical payment Pod stuck Pending. There are six batch jobs running with priority 10; the payment Pod has priority 1000. Cluster is full. What does the scheduler do?",
            options=[
                ("a) Wait — it can't move running Pods", False),
                ("b) Identify the smallest set of priority-10 Pods whose eviction would free enough room for the priority-1000 Pod, evict them gracefully, then schedule the payment Pod", True),
                ("c) Force the payment Pod onto an existing node, killing whichever Pod it lands on", False),
            ],
            feedback="<strong>Answer: b.</strong> Preemption is graceful: scheduler picks victims with the goal of minimising disruption, sends them through normal Pod termination (preStop hooks, grace period), and places the high-priority Pod once room is free. Time-to-place is typically the grace period (default 30s).",
        ),
    },
    before_after_before='<p>Pre-priority: cluster full → critical Pod sits Pending. Engineer wakes up, manually kills batch jobs, prays they didn\'t lose state. GPU requests by string match (<code>nvidia.com/gpu</code>) — no way to ask for "H100 with 80 GiB" or "MIG slice." Latency-sensitive Pods scheduled wherever; tail latency wobbles for unexplained reasons.</p>',
    before_after_after='<p>PriorityClass + preemption → cluster full + critical incoming → batch evicted automatically, critical placed in seconds. DRA → declarative ResourceClaim with attributes; scheduler matches structurally. Topology Manager → CPU + memory + GPU all on same NUMA node; tail latency stable.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">DRA is the most consequential scheduler change since the original K8s API. By 2027, device plugins will look quaint.</p>',
    analogy_intro_html='<p>Back to Dispatch Office, but now we\'re past the routing board into the VIP wing. Three new desks. The <strong>priority desk</strong> hands out lane stickers — VIP, premium, regular, walk-in. When the road is jammed and a VIP truck can\'t move, the dispatcher pulls a regular truck to the side (gracefully — the regular driver\'s called, given time to finish loading) and lets the VIP through. The <strong>specialty equipment desk</strong> (DRA) is where trucks request specific tools — "I need a refrigerated trailer with 80 cubic feet" — and the desk matches against the actual truck inventory by attribute, not by name. The <strong>route engineering desk</strong> (Topology Manager) handles trucks that need to stay on one specific highway loop because their cargo is sensitive to inter-zone transit.</p>',
    translation_rows=[
        ("VIP / premium / regular lane stickers", "<code>PriorityClass</code> objects"),
        ("Pulling the regular truck aside for the VIP", "Preemption + graceful eviction"),
        ("\"I need a refrigerated trailer with 80 cubic feet\"", "<code>ResourceClaim</code> with attribute selectors"),
        ("The truck inventory at each depot", "<code>ResourceSlice</code> published by kubelet"),
        ("\"This is a refrigerated trailer\" classification", "<code>DeviceClass</code>"),
        ("Trucks that must stay on one highway loop", "Topology Manager <code>single-numa-node</code> policy"),
        ("Different routing manuals for different cargo types", "Scheduler profiles"),
    ],
    analogy_stops="The analogy stops here: real DRA is a structured API with CEL expressions, not a paper request. And NUMA is a hardware reality of how RAM is wired to CPU sockets — there's no \"highway loop\" actually moving anything; it's electrons over a memory bus.",
    eli5='Some toys are special — they go first. If the toy box is full, regular toys move out so the special toy can fit. Some toys need a specific kind of plug (a GPU plug). Some toys break if their batteries are too far away — they need batteries right next to them.',
    eli10="Three advanced scheduling primitives. <strong>PriorityClass</strong> + preemption: critical Pods evict lower-priority Pods when the cluster is full. <strong>DRA</strong> (Dynamic Resource Allocation, GA in 1.34): structured request/match for GPUs/FPGAs/NICs with attributes (\"H100 with 80 GiB\"); replaces the legacy device-plugin API. <strong>Topology Manager</strong> + CPU Manager + Memory Manager: keep latency-sensitive workloads' CPU, RAM, and devices co-located on the same NUMA node. Plus scheduler profiles for using different bin-packing strategies for different workload types.",
    scenarios=[
        Scenario(name="A SaaS during traffic spikes", body="<code>critical</code> = 1000 (payment), <code>standard</code> = 500 (everything user-facing), <code>batch</code> = 10 (analytics, ML), <code>opportunistic</code> = -100 (spot-eligible). When traffic spikes preempt batch and opportunistic. The autoscaler then catches up. SREs sleep through what would have been a paging incident."),
        Scenario(name="A bank running ML training on shared H100s", body="DRA + NVIDIA's DRA driver. Each Pod's <code>ResourceClaim</code> requests one MIG slice of an H100 — say 1g.10gb (1/7 of an H100). Scheduler matches by attribute. Eight Pods can share one H100. Pre-DRA: each Pod requested a whole H100 — 8× the cost."),
        Scenario(name="A trading firm running latency-sensitive Pods", body="Topology Manager <code>policy: single-numa-node</code>. CPU Manager <code>policy: static</code>. Pods request integer CPU, Guaranteed QoS. Memory Manager pins RAM. Tail latency P99 dropped from 2.1ms to 0.7ms with no application change."),
        Scenario(name="An ML lab running Volcano alongside default scheduler", body="Default scheduler handles user-facing workloads. Volcano (in <code>kube-system</code>) handles ML training jobs with gang scheduling — all 16 workers must start at once or none start (no half-started training). Different <code>schedulerName</code> per job. Both schedulers coexist because they don't fight over the same Pods."),
    ],
    misconceptions=[
        Misconception(myth="Preemption kicks in instantly.", truth="Evicted Pods get their normal grace period (default 30s, configurable per-Pod). The high-priority Pod waits for the eviction. Total time-to-place ≈ grace period + scheduler latency. Plan for ~1 minute, not instant."),
        Misconception(myth="DRA replaces resource requests/limits.", truth="No. CPU and memory are still <code>resources.requests/limits</code> as before. DRA is for <em>devices</em> — GPUs, FPGAs, RDMA NICs, SR-IOV VFs. The two systems coexist."),
        Misconception(myth="Topology Manager <code>single-numa-node</code> always speeds things up.", truth="Only for workloads that pin CPU, memory, and devices. For workloads that don't request integer CPU or specific devices, the policy has no effect. Worse: in resource-constrained clusters it can cause Pending Pods that would have placed cross-NUMA happily."),
    ],
    flashcards=[
        Flashcard(front="What's a PriorityClass?", back="Cluster-scoped object mapping a name to an integer priority value. Pods reference it via <code>priorityClassName</code>. Higher values = higher priority. Two reserved system classes: <code>system-cluster-critical</code> + <code>system-node-critical</code>."),
        Flashcard(front="When does preemption happen?", back="When a Pod can't be scheduled because no node fits and a lower-priority Pod's eviction would create room. Scheduler picks victims (smallest set, lowest priority), evicts gracefully, places the high-priority Pod."),
        Flashcard(front="What does DRA stand for?", back="Dynamic Resource Allocation. GA in K8s 1.34. Modern API for declaring and matching specialized devices (GPUs, FPGAs, NICs). Replaces device plugins."),
        Flashcard(front="Four DRA objects?", back="<code>DeviceClass</code> (cluster-scoped, like StorageClass for devices), <code>ResourceClaim</code> (namespace-scoped, the request), <code>ResourceClaimTemplate</code> (like volumeClaimTemplates), <code>ResourceSlice</code> (kubelet-published inventory)."),
        Flashcard(front="What does CPU Manager <code>static</code> policy do?", back="Dedicates whole CPU cores to Pods with Guaranteed QoS that request integer CPU. Other Pods are kept off those cores. Removes context-switching jitter for the dedicated Pod."),
        Flashcard(front="Topology Manager <code>single-numa-node</code> policy?", back="Refuses to schedule a Pod unless its CPU, memory, and (DRA) devices can all be allocated on the same NUMA node. Hard same-NUMA enforcement; can cause Pending."),
        Flashcard(front="Scheduler profile vs separate scheduler?", back="Profile = named config in the same kube-scheduler process; Pods opt in via <code>schedulerName</code>. Separate scheduler = different binary (e.g., Volcano) with its own kube-scheduler process. Both coexist because they only handle Pods naming them."),
        Flashcard(front="Bin-packing vs spreading scoring?", back="<code>NodeResourcesFit: MostAllocated</code> = pack Pods tightly (good for batch + spot eviction). <code>LeastAllocated</code> = spread (default; good for traffic-serving). Configured per scheduler profile."),
    ],
    quizzes=[
        Quiz(prompt="A team accidentally creates a PriorityClass with priority 2,000,000,001 — higher than even <code>system-node-critical</code>. What's the risk?", answer="Their Pod can preempt <em>cluster-critical</em> components — kube-proxy, CNI Pods, even kubelet's static Pods. If the high-priority Pod misbehaves and OOMs the node, the very system Pods that would recover the node have already been evicted. <strong>Mitigation:</strong> use ValidatingAdmissionPolicy or Kyverno to cap user-defined priority at, say, 1,000,000,000. Reserved values (≥2,000,000,000) should be off-limits to non-system creators."),
        Quiz(prompt="Pre-DRA, the team's Pod-spec for GPU was <code>resources.limits: nvidia.com/gpu: 1</code>. They migrate to DRA on K8s 1.34. What's the new shape?", answer="Three steps: (1) Define a <code>DeviceClass</code> for NVIDIA GPUs (typically pre-installed by the NVIDIA DRA driver). (2) Per Pod, declare a <code>ResourceClaimTemplate</code> referencing that DeviceClass with attribute selectors (e.g., MIG profile). (3) In the Pod spec, list the claim under <code>spec.resourceClaims</code> and reference it from the container. The old <code>nvidia.com/gpu: 1</code> still works for the legacy device plugin path during transition; both can coexist on a node. Most teams migrate workload-by-workload over a quarter."),
        Quiz(prompt="Black Friday 2026. Traffic spikes 4×. Critical payment Pods are Pending; the autoscaler is mid-flight. <strong>Click for the priority playbook in action. ▼</strong>", cyoa=True, cyoa_tag="the priority playbook in action", answer="The setup: <code>critical=1000</code> (payment), <code>standard=500</code>, <code>batch=10</code>, <code>opportunistic=-100</code>. Sequence of events at minute 0:00 — traffic spike begins; payment HPA wants 8 more replicas; cluster has no fit. <strong>0:01</strong> — scheduler identifies preemption candidates: 12 opportunistic spot Pods running ML inference experiments. Issues evictions with 30s grace. <strong>0:31</strong> — eviction complete; payment Pods place. <strong>0:45</strong> — Cluster Autoscaler / Karpenter (Lesson 34) finishes provisioning new nodes; opportunistic Pods reschedule there. <strong>2:00</strong> — system stable, batch / opportunistic catch up on the new capacity. <strong>Total user impact:</strong> 30 seconds of slightly elevated payment latency. <strong>Without priority + preemption:</strong> 12 minutes of degraded payments while ops humans manually killed batch jobs. <strong>The lesson:</strong> priority hierarchy isn't a feature you bolt on during incidents — it's a posture you bake in before the incident."),
    ],
    glossary=[
        GlossaryItem(name="PriorityClass", definition="Cluster-scoped object: name → integer priority. Pods reference it via <code>priorityClassName</code>."),
        GlossaryItem(name="Preemption", definition="Scheduler-driven eviction of lower-priority Pods to make room for a higher-priority Pod that can't fit."),
        GlossaryItem(name="DRA (Dynamic Resource Allocation)", definition="K8s 1.34 GA. Structured API for specialized devices. Replaces device plugins."),
        GlossaryItem(name="DeviceClass", definition="DRA cluster-scoped object: defines a class of devices and their attributes."),
        GlossaryItem(name="ResourceClaim", definition="DRA namespace-scoped object: a Pod's request for a device."),
        GlossaryItem(name="ResourceClaimTemplate", definition="DRA template referenced from a Pod, generates a per-Pod claim like volumeClaimTemplates."),
        GlossaryItem(name="ResourceSlice", definition="DRA kubelet-published object: per-node inventory of available devices and attributes."),
        GlossaryItem(name="CPU Manager", definition="kubelet feature. <code>static</code> policy dedicates cores to Guaranteed-QoS Pods with integer CPU requests."),
        GlossaryItem(name="Memory Manager", definition="kubelet feature pinning memory allocation to specific NUMA nodes."),
        GlossaryItem(name="Topology Manager", definition="kubelet coordinator for CPU + memory + device locality. Policies: best-effort, restricted, single-numa-node."),
        GlossaryItem(name="Scheduler profile", definition="Named plugin/scoring configuration. Multiple profiles per kube-scheduler process. Pods opt in via <code>schedulerName</code>."),
        GlossaryItem(name="Volcano / Yunikorn", definition="Alternative schedulers for batch / ML workloads with gang scheduling and fair-share."),
    ],
    recap_lead="PriorityClass + preemption decides who runs when full. DRA is the modern device API (GPUs, FPGAs, NICs) — GA in 1.34. Topology Manager keeps CPU, memory, and devices on the same NUMA node for latency-sensitive workloads. Scheduler profiles let you mix bin-packing strategies.",
    recap_next="<strong>Next — Lesson 24: Networking Foundations & CNI.</strong> The Module 12 networking deep dive begins. Linux network primitives, the CNI specification, MTU debugging, and the major plugin landscape (Cilium, Calico, Flannel). Switchboard, behind the wires.",
)
