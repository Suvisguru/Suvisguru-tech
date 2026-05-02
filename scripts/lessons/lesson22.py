from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Dispatch Office bullpen: a dispatcher at a routing board with three colored lanes (zone-A, zone-B, zone-C) routing trucks (Pods) to depots (nodes); some trucks have warning stickers (taints/tolerations), one zone is over-full and the dispatcher is rebalancing.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">DISPATCH OFFICE · ROUTING BOARD</text>
  <!-- Dispatcher -->
  <g transform="translate(40,55)">
    <circle cx="30" cy="20" r="14" fill="#FBF1D6" stroke="#2A2520" stroke-width="1.4"/>
    <circle cx="26" cy="18" r="1.4" fill="#2A2520"/><circle cx="34" cy="18" r="1.4" fill="#2A2520"/>
    <path d="M 24 24 Q 30 28 36 24" stroke="#2A2520" stroke-width="1.2" fill="none" stroke-linecap="round"/>
    <path d="M 18 34 Q 18 80 24 100 L 36 100 Q 42 80 42 34 Z" fill="#3F4A5E"/>
    <text x="30" y="120" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">scheduler</text>
    <text x="30" y="133" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">picks the node</text>
  </g>
  <!-- Routing board with three zones -->
  <g transform="translate(120,40)">
    <rect width="420" height="140" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="210" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">DEPOT MAP · 3 zones</text>
    <!-- Zone A -->
    <rect x="14" y="22" width="124" height="105" rx="4" fill="#E0EEF3" stroke="#4A8FA8" stroke-width="1.2"/>
    <text x="76" y="36" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">zone-A</text>
    <rect x="22" y="44" width="40" height="22" rx="2" fill="#5A9F7A"/><text x="42" y="57" text-anchor="middle" font-size="6" fill="#FFFFFF" font-weight="700">node-a1</text>
    <rect x="68" y="44" width="40" height="22" rx="2" fill="#5A9F7A"/><text x="88" y="57" text-anchor="middle" font-size="6" fill="#FFFFFF" font-weight="700">node-a2</text>
    <circle cx="42" cy="80" r="6" fill="#D97757"/>
    <circle cx="60" cy="80" r="6" fill="#D97757"/>
    <circle cx="78" cy="80" r="6" fill="#D97757"/>
    <text x="76" y="105" text-anchor="middle" font-size="7" fill="#3F4A5E" font-style="italic">3 web Pods · spread</text>
    <!-- Zone B -->
    <rect x="146" y="22" width="124" height="105" rx="4" fill="#E0EFE6" stroke="#5A9F7A" stroke-width="1.2"/>
    <text x="208" y="36" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">zone-B</text>
    <rect x="154" y="44" width="40" height="22" rx="2" fill="#5A9F7A"/><text x="174" y="57" text-anchor="middle" font-size="6" fill="#FFFFFF" font-weight="700">node-b1</text>
    <rect x="200" y="44" width="40" height="22" rx="2" fill="#9D9389" stroke="#A04832" stroke-width="1.5"/>
    <text x="220" y="57" text-anchor="middle" font-size="6" fill="#FFFFFF" font-weight="700">node-b2</text>
    <text x="220" y="74" text-anchor="middle" font-size="6" fill="#A04832" font-weight="700">tainted</text>
    <circle cx="174" cy="85" r="6" fill="#D97757"/>
    <circle cx="174" cy="100" r="6" fill="#D97757"/>
    <text x="208" y="115" text-anchor="middle" font-size="7" fill="#3F4A5E" font-style="italic">no toleration → skip b2</text>
    <!-- Zone C -->
    <rect x="278" y="22" width="124" height="105" rx="4" fill="#FBE8DC" stroke="#A04832" stroke-width="1.2"/>
    <text x="340" y="36" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">zone-C</text>
    <rect x="286" y="44" width="40" height="22" rx="2" fill="#5A9F7A"/><text x="306" y="57" text-anchor="middle" font-size="6" fill="#FFFFFF" font-weight="700">node-c1</text>
    <rect x="332" y="44" width="40" height="22" rx="2" fill="#5A9F7A"/><text x="352" y="57" text-anchor="middle" font-size="6" fill="#FFFFFF" font-weight="700">node-c2</text>
    <circle cx="306" cy="85" r="6" fill="#D97757"/>
    <circle cx="306" cy="100" r="6" fill="#D97757"/>
    <text x="340" y="115" text-anchor="middle" font-size="7" fill="#A04832" font-style="italic">2 — under-spread!</text>
  </g>
  <!-- Legend -->
  <g transform="translate(560,55)">
    <text x="0" y="14" font-size="9" font-weight="700" fill="#5A4F45">key</text>
    <rect x="0" y="22" width="14" height="8" fill="#5A9F7A"/>
    <text x="20" y="29" font-size="8" fill="#5A4F45">healthy node</text>
    <rect x="0" y="36" width="14" height="8" fill="#9D9389" stroke="#A04832" stroke-width="1"/>
    <text x="20" y="43" font-size="8" fill="#5A4F45">tainted node</text>
    <circle cx="7" cy="55" r="5" fill="#D97757"/>
    <text x="20" y="58" font-size="8" fill="#5A4F45">Pod</text>
  </g>
  <text x="340" y="200" text-anchor="middle" font-size="11" fill="#3F4A5E" font-style="italic">The dispatcher’s rules: filter → score → bind. \"Where can I send this truck? Which zone is starving? Who can’t accept it?\"</text>
</svg>"""

LESSON = LessonSpec(
    num="22",
    title_short="scheduling Pt 1",
    title_full="Scheduling Part 1 · Affinity, Taints, Topology Spread",
    title_html="Lesson 22 — Scheduling Part 1: Affinity, Taints, Topology Spread · K-COM",
    module_eyebrow="Module 11 · Lesson 22 · how the scheduler picks a node",
    hero_sub_html='Every Pod has to land somewhere. The scheduler\'s job is <em>pick the right node</em>. Three knobs control its decision: <strong>node selectors / affinity</strong> (where the Pod prefers to be), <strong>taints / tolerations</strong> (where the node refuses to host), and <strong>topology spread</strong> (don\'t pile up in one zone).',
    hero_illu_svg=HERO_SVG,
    nightmare_html='An availability zone fails. Half the cluster\'s nodes vanish. The team has 12 web Pods running — but 11 of them were scheduled in the failed zone because nobody set topology-spread constraints. The remaining 1 Pod is melting under 12× normal traffic. The team frantically re-deploys with anti-affinity, but during the rebalance the cache layer (also single-zone-concentrated) collapses. <em>Two-hour outage, 100% preventable.</em> The scheduler will <em>let</em> you do this — it has no opinion until you tell it to. Today\'s lesson is about telling it.',
    stamp_html='The scheduler does <strong>filter → score → bind</strong>. You shape filtering with <strong>nodeSelector</strong>, <strong>affinity / anti-affinity</strong>, <strong>taints + tolerations</strong>, and <strong>topology spread constraints</strong>. The single most consequential rule for production: <strong>spread across zones</strong>.',
    district_pin="kt-pin16",
    district_label="Dispatch Office — Routing Board",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What the scheduler actually does",
            body_html="""    <p>When you create a Pod with no <code>nodeName</code>, it sits in <code>Pending</code>. The kube-scheduler is a controller watching unscheduled Pods. For each one, it runs a two-phase decision:</p>
    <ul>
      <li><strong>Filter (predicates):</strong> remove every node that <em>can't</em> host this Pod. Reasons: not enough CPU/memory, doesn't match nodeSelector, has a NoSchedule taint the Pod doesn't tolerate, doesn't satisfy affinity/anti-affinity, fails a custom plugin's check. After filtering you have a candidate set.</li>
      <li><strong>Score (priorities):</strong> rank candidates by various plugins — most-allocated, least-allocated, image-locality, topology-spread, inter-pod affinity scoring, custom plugins. Highest score wins.</li>
    </ul>
    <p>Once a node is picked, the scheduler writes <code>spec.nodeName</code> on the Pod via the API. The kubelet on that node sees the assignment, pulls the image, starts the containers. The scheduler doesn't move Pods after they're placed — that's the kubelet's eviction logic plus controllers like the descheduler.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Node selection: nodeSelector vs affinity",
            h2="From simple labels to expressive matching",
            body_html="""    <p><strong>nodeSelector</strong> is the original tool: a flat <code>map[string]string</code>. The Pod says <code>nodeSelector: {disktype: ssd}</code>; the scheduler keeps only nodes with that label. Hard match, no flexibility, deprecated for new use cases — but still ubiquitous because it's tiny.</p>
    <p><strong>Node affinity</strong> is the modern, expressive successor. Two flavours:</p>
    <ul>
      <li><code>requiredDuringSchedulingIgnoredDuringExecution</code> — must match (filter). Like nodeSelector but with <code>In</code>, <code>NotIn</code>, <code>Exists</code>, <code>Gt</code>, <code>Lt</code> operators.</li>
      <li><code>preferredDuringSchedulingIgnoredDuringExecution</code> — soft preference (score). Fall back to other nodes if the preferred ones aren't available.</li>
    </ul>
    <p><strong>Inter-pod affinity / anti-affinity</strong> ties Pod placement to <em>where other Pods are</em>. Anti-affinity is the workhorse for spreading: "don't put two replicas of this Deployment on the same node" expressed as <code>topologyKey: kubernetes.io/hostname</code> + <code>labelSelector: matchLabels: {app: web}</code>.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Taints and tolerations",
            h2="Nodes refuse; Pods opt in",
            body_html="""    <p>Affinity is the Pod expressing a preference. <strong>Taints</strong> are the inverse — the <em>node</em> says "don't schedule things here unless they explicitly accept this taint." Three effects:</p>
    <ul>
      <li><code>NoSchedule</code> — scheduler refuses to place new Pods that don't tolerate this taint.</li>
      <li><code>PreferNoSchedule</code> — try to avoid, but okay if no alternative.</li>
      <li><code>NoExecute</code> — even running Pods get evicted if they don't tolerate the taint.</li>
    </ul>
    <p>A Pod tolerates a taint by listing it under <code>spec.tolerations</code>. Common patterns:</p>
    <ul>
      <li><strong>Dedicated node pools</strong>: taint GPU nodes <code>gpu=true:NoSchedule</code>; only GPU workloads tolerate it. Non-GPU Pods stay off (and don't waste expensive capacity).</li>
      <li><strong>Maintenance</strong>: <code>kubectl drain node-x</code> taints with <code>NoExecute</code>; running Pods evict, no new ones land.</li>
      <li><strong>Node problems</strong>: the node-problem-detector taints failing nodes; non-tolerant workloads reschedule away.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The taints+tolerations pair is the single mechanism behind <em>cordoning</em> (taint → no new Pods), <em>draining</em> (taint with NoExecute → evict + no new Pods), <em>node-not-ready handling</em> (auto-applied <code>node.kubernetes.io/not-ready:NoExecute</code> with a 5-min toleration window), and <em>spot/preemptible nodes</em> (taint to keep critical workloads off). Master taints and you understand most of the cluster's lifecycle behavior.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Topology Spread Constraints",
            h2="The single most useful scheduling primitive",
            body_html="""    <p>You almost always want replicas of a workload <em>spread across zones, racks, or hosts</em> — both for HA and for fair use of capacity. Anti-affinity used to be the way; topology spread is now strictly better.</p>
    <p>A constraint says: "for Pods matching this selector, the difference between the most-loaded topology bucket and the least-loaded should be at most <code>maxSkew</code>."</p>
    <ul>
      <li><code>topologyKey: topology.kubernetes.io/zone</code> + <code>maxSkew: 1</code> — spread evenly across zones.</li>
      <li><code>topologyKey: kubernetes.io/hostname</code> + <code>maxSkew: 1</code> — at most one extra Pod on any one node.</li>
      <li><code>whenUnsatisfiable: DoNotSchedule</code> — hard. <code>ScheduleAnyway</code> — soft (score-only).</li>
    </ul>
    <p>Pair zone-spread with hostname-spread for full protection: across zones first (HA), within zones across hosts (don't pile on one machine). Most production Deployments should have both.</p>
    <p>K8s 1.33+ added <code>matchLabelKeys</code> for cleaner rolling-update behavior (skew is computed per-revision so old + new replicas don't double-count). New code should use it.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team taints all GPU nodes with <code>gpu=true:NoSchedule</code> but doesn't add a toleration to their non-GPU workloads. What happens?",
            options=[
                ("a) Non-GPU Pods can't schedule anywhere; cluster grinds to a halt", False),
                ("b) Non-GPU Pods stay off GPU nodes — exactly the desired behavior", True),
                ("c) Pods fail to start with a permission error", False),
            ],
            feedback="<strong>Answer: b.</strong> The taint repels non-tolerant Pods from <em>those</em> nodes specifically. Other (non-tainted) nodes accept them normally. This is the standard pattern for dedicated node pools — taint to keep general workloads off the expensive capacity.",
        ),
    },
    before_after_before='<p>Pre-spread era: 12 web Pods, all 12 happen to land in <code>us-east-1a</code> because the scheduler optimised for image locality. Zone fails. Service is gone. Engineers are awake. Post-mortem starts with "we should have spread."</p>',
    before_after_after='<p>Topology spread + anti-affinity: 12 Pods land 4-4-4 across <code>us-east-1a/b/c</code>, no two on the same node within a zone. Zone fails. Eight Pods still serving; HPA scales up. Service degrades briefly, never goes down. The post-mortem is short.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Topology spread is the cheapest reliability win in K8s. Two YAML fields, no extra controllers, ~zero performance cost. Set it on every production Deployment.</p>',
    analogy_intro_html='<p>The Dispatch Office routes trucks (Pods) to depots (nodes) across three districts (zones). The dispatcher (kube-scheduler) has a board with every depot\'s status. Trucks come in with stickers — "I need a refrigerated depot" (<em>nodeSelector: refrigerated=true</em>), "I prefer the harbour district but the airport district works too" (<em>preferred affinity</em>), "I cannot share a depot with another delivery from my own company" (<em>pod anti-affinity</em>).</p><p>Each depot has its own warning signs: "no flammables" (<em>NoSchedule taint</em>), "evacuating — leave by 5 PM" (<em>NoExecute taint</em>). Trucks carrying flammables won\'t go there unless their driver has the special permit (<em>toleration</em>).</p><p>And there\'s the city-wide spread rule: <em>no district may have more than one extra truck of any one company</em>. The dispatcher checks the board before binding any truck. Filter, score, bind. The whole system is designed to make the wrong choice hard.</p>',
    translation_rows=[
        ("The dispatcher", "kube-scheduler"),
        ("\"I need a refrigerated depot\" sticker", "<code>nodeSelector</code> / required node affinity"),
        ("\"I prefer the harbour, but airport works\" sticker", "Preferred node affinity"),
        ("\"Don't park me next to another truck from my company\"", "Pod anti-affinity"),
        ("\"No flammables\" sign at the depot", "<code>NoSchedule</code> taint"),
        ("\"Evacuating now\" sign", "<code>NoExecute</code> taint"),
        ("Driver's special permit", "Toleration on the Pod"),
        ("City-wide \"no district more than one truck above the rest\"", "<code>topologySpreadConstraints</code> with <code>maxSkew: 1</code>"),
    ],
    analogy_stops="The analogy stops here: the dispatcher in K-Town only places new trucks. Once parked, trucks don't move on their own — that's a separate process called the descheduler (or pod-driven evictions during draining), and it's outside this lesson.",
    eli5='Imagine 12 toy cars and 3 toy garages. The toy cars don\'t want to all crowd into one garage — they each pick a different garage. That\'s "topology spread." Some garages have a "no toy trucks" sign — those are taints. Toy trucks need a sticker to enter (toleration).',
    eli10="The kube-scheduler picks a node for every Pod. It does <strong>filter → score → bind</strong>. You shape the filter with: <code>nodeSelector</code> (flat label match), node affinity (operator-rich match, required or preferred), inter-pod affinity / anti-affinity (relative to other Pods), taints + tolerations (nodes repel; Pods opt in), and topology spread constraints (don't bunch up). For production, always: zone-spread + hostname-spread + reasonable resource requests. Skip these and the scheduler will technically work — and your zone-failure post-mortem will be long.",
    scenarios=[
        Scenario(name="A SaaS standard production Deployment", body="Every Deployment ships with two topology-spread constraints (zone, hostname), maxSkew 1, both DoNotSchedule. Plus pod anti-affinity (preferred) for backwards compat. Engineers don't touch these — they're enforced via a Kyverno mutation that adds them automatically if a Deployment forgets."),
        Scenario(name="A bank running ML training on dedicated GPUs", body="GPU nodes tainted <code>gpu=nvidia-h100:NoSchedule</code>. Training Pods tolerate it. Inference Pods tolerate it AND have node affinity for the same label. CPU-only workloads have no toleration so they never waste expensive capacity. Spot GPUs additionally have <code>spot:NoSchedule</code> — only batch training tolerates that one."),
        Scenario(name="A startup using PreferNoSchedule for cost-skewing", body="Cluster mostly on-demand nodes plus a few spot nodes. Spot tainted with <code>cost-tier=spot:PreferNoSchedule</code> + a tag <code>cost-tier=spot</code>. Stateful production Pods have no toleration → land on on-demand. Batch jobs explicitly tolerate spot AND have node affinity for it → land on spot first; fall back to on-demand if no spot capacity."),
        Scenario(name="A team using descheduler for drift correction", body="The descheduler runs as a CronJob. Detects Pods that violate topology-spread (e.g., from old, pre-constraint Deployments) and evicts them. The scheduler then re-places correctly. Slow, gentle, in-place rebalancing without redeploys."),
    ],
    misconceptions=[
        Misconception(myth="Anti-affinity and topology spread do the same thing.", truth="Anti-affinity says \"don't put two of these on the same X.\" Topology spread says \"distribute across X with at most maxSkew imbalance.\" Spread scales with replica count; anti-affinity doesn't. Spread is generally what you actually want."),
        Misconception(myth="<code>preferred</code> affinity is mostly the same as <code>required</code>.", truth="Preferred is a <em>scoring</em> input — the scheduler will pick a non-preferred node if the preferred one's at capacity. Required is a <em>filter</em> — the Pod stays Pending forever if no matching node exists. Use required only for hard constraints (GPU type, kernel version)."),
        Misconception(myth="<code>maxSkew: 0</code> is the strictest possible setting.", truth="<code>maxSkew</code> is required to be at least 1 (skew of 0 makes no mathematical sense — it would mean every bucket has exactly the same count, which is impossible at most replica counts)."),
    ],
    flashcards=[
        Flashcard(front="Filter vs Score?", back="Two scheduler phases. Filter: remove ineligible nodes (taints, resource fit, affinity required). Score: rank surviving candidates (preferred affinity, topology spread, image locality, etc.). Highest score wins."),
        Flashcard(front="nodeSelector vs node affinity?", back="nodeSelector = simple <code>map[string]string</code>, hard match. Node affinity = operator-rich (In/NotIn/Exists/Gt/Lt), supports required + preferred. Affinity is the modern API; nodeSelector is still around for simplicity."),
        Flashcard(front="Three taint effects?", back="<code>NoSchedule</code> (don't schedule new), <code>PreferNoSchedule</code> (try not to), <code>NoExecute</code> (evict existing too). Pods opt in via tolerations matching key/value/effect."),
        Flashcard(front="Pod anti-affinity — what's <code>topologyKey</code>?", back="The label key that defines \"sameness.\" <code>kubernetes.io/hostname</code> = same node. <code>topology.kubernetes.io/zone</code> = same AZ. The constraint is evaluated per-bucket of that key."),
        Flashcard(front="Topology spread vs anti-affinity?", back="Spread is N-replica-aware (maxSkew controls imbalance). Anti-affinity is pairwise (\"don't co-locate\"). Spread is generally better for ≥3 replicas; anti-affinity is fine for 2-replica master/replica setups."),
        Flashcard(front="<code>whenUnsatisfiable</code> options?", back="<code>DoNotSchedule</code> — hard, Pod stays Pending if can't satisfy. <code>ScheduleAnyway</code> — soft, prefer satisfaction but place anyway."),
        Flashcard(front="What does drain do at the scheduling level?", back="kubectl drain = cordon (taint <code>node.kubernetes.io/unschedulable:NoSchedule</code>) + evict existing Pods (gracefully). Combined effect: no new Pods land; running Pods rescheduled elsewhere."),
        Flashcard(front="<code>matchLabelKeys</code> in topology spread?", back="K8s 1.33+. Lets the scheduler compute skew per-revision so old and new replicas during a rolling update don't double-count. Cleaner rollouts; recommended for new Deployments."),
    ],
    quizzes=[
        Quiz(prompt="A 6-replica Deployment with <code>topologySpreadConstraints: maxSkew=1, topologyKey=zone, whenUnsatisfiable=DoNotSchedule</code>. The cluster has 3 zones. One zone has a brief capacity issue and only 1 node is available there. What's the placement?", answer="The scheduler aims for 2-2-2 across zones. With the constrained zone capacity-light, it might place 2-2-2 if those nodes can fit two Pods each — but if the constrained zone's single node can only fit 1 Pod, the constraint becomes unsatisfiable: scheduling 3-2-1 would have skew=2 (>1). With <code>DoNotSchedule</code>, two Pods stay Pending until capacity returns. <strong>Lesson:</strong> <code>DoNotSchedule</code> is great for production correctness but can cause Pending Pods during partial outages. Some teams pair <code>maxSkew=1, DoNotSchedule</code> on zone with a relaxed <code>maxSkew=2, ScheduleAnyway</code> on hostname to balance correctness vs flexibility."),
        Quiz(prompt="A junior engineer adds <code>nodeSelector: env=prod</code> to a Pod. There are no nodes labelled <code>env=prod</code>. What's the scheduler's behavior?", answer="The Pod stays in <code>Pending</code> indefinitely with a <code>FailedScheduling</code> event citing \"0/N nodes available: didn't match Pod's node affinity.\" The scheduler doesn't error out — it just keeps trying. Most clusters have monitoring on Pending duration that would alert. <strong>Fix:</strong> either label some nodes <code>env=prod</code>, or change the selector to soft (preferred affinity), or remove it. There's no auto-fallback."),
        Quiz(prompt="The platform team adds a topology-spread enforcement policy via Kyverno. An old Deployment without spread constraints triggers a Pod that lands on an over-loaded zone. <strong>Click for what happens during the rollout. ▼</strong>", cyoa=True, cyoa_tag="during the rollout", answer="Kyverno is mutating-mode: it injects a default topology-spread constraint into every newly-admitted Pod. Old Pods (admitted before the policy) keep running where they are — Kyverno does not retro-evict. On the next rolling update of the old Deployment, new ReplicaSet's Pods get the spread constraint, and they land balanced across zones. The old ReplicaSet's Pods drain over the rollout. So you get \"eventually consistent\" spread without a forced eviction storm. <strong>If you wanted faster correction:</strong> run the descheduler with the <code>RemovePodsViolatingTopologySpreadConstraint</code> strategy. It evicts violators on a schedule; the scheduler re-places. <strong>If you wanted instant correction:</strong> roll the Deployment manually. Each approach trades disruption for correctness — and that's why most platform teams prefer mutating policies + lazy reconcile + descheduler over forced changes."),
    ],
    glossary=[
        GlossaryItem(name="kube-scheduler", definition="Control-plane controller that picks a node for every Pending Pod. Filter → score → bind."),
        GlossaryItem(name="nodeSelector", definition="Pod field: simple required label match against nodes. Subsumed by node affinity."),
        GlossaryItem(name="Node affinity", definition="Pod field with required (filter) and preferred (score) variants. Operator-rich expressions over node labels."),
        GlossaryItem(name="Pod affinity / anti-affinity", definition="Place near (or away from) Pods matching a selector, evaluated per topologyKey."),
        GlossaryItem(name="topologyKey", definition="Node label that defines \"same group\" for affinity / spread. Common: <code>kubernetes.io/hostname</code>, <code>topology.kubernetes.io/zone</code>."),
        GlossaryItem(name="Taint", definition="Node-level repellent. Three effects: NoSchedule, PreferNoSchedule, NoExecute."),
        GlossaryItem(name="Toleration", definition="Pod-level acceptance of a specific taint. Required to schedule on (or remain on) tainted nodes."),
        GlossaryItem(name="topologySpreadConstraints", definition="Pod field for evenly distributing replicas. Fields: <code>maxSkew</code>, <code>topologyKey</code>, <code>whenUnsatisfiable</code>, <code>labelSelector</code>."),
        GlossaryItem(name="maxSkew", definition="Max allowed difference in replica count between the most- and least-loaded buckets. Min 1."),
        GlossaryItem(name="DoNotSchedule / ScheduleAnyway", definition="<code>whenUnsatisfiable</code> options. Hard vs soft enforcement."),
        GlossaryItem(name="Cordon", definition="Mark a node unschedulable (apply <code>node.kubernetes.io/unschedulable:NoSchedule</code>). New Pods avoid it; existing Pods stay."),
        GlossaryItem(name="Drain", definition="Cordon + evict running Pods. Used for node maintenance."),
    ],
    recap_lead="Scheduler does filter → score → bind. nodeSelector / affinity say where Pods can go; taints + tolerations say where nodes accept; topology spread keeps the load balanced across failure domains. For production, always set zone + hostname spread.",
    recap_next="<strong>Next — Lesson 23: Scheduling Part 2.</strong> The advanced controls — Pod priority and preemption, Dynamic Resource Allocation (DRA, GA in 1.34) for GPUs, NUMA topology, scheduler profiles. The dispatch office's executive routing.",
)
