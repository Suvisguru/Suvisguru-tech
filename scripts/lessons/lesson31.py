from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Watchtower aerial: a tower overlooking a grid of fenced tenant compounds, each with its own quota meter, RBAC plaque, NetworkPolicy fence, and PSA banner. A separate panel shows kube-bench scoring.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">WATCHTOWER · MULTI-TENANT VIEW</text>
  <!-- Tenant grid -->
  <g transform="translate(40,55)">
    <text x="160" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">TENANT NAMESPACES</text>
    <!-- Tenant 1 -->
    <g transform="translate(0,22)"><rect width="100" height="120" rx="6" fill="#E0EEF3" stroke="#4A8FA8" stroke-width="1.5"/><text x="50" y="16" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">team-a</text><rect x="10" y="24" width="80" height="12" rx="2" fill="#FBF1D6"/><text x="50" y="33" text-anchor="middle" font-size="6" fill="#5A4F45" font-weight="700">quota: 8 CPU</text><rect x="10" y="40" width="80" height="12" rx="2" fill="#E0EFE6"/><text x="50" y="49" text-anchor="middle" font-size="6" fill="#3D7857" font-weight="700">RBAC: team-a only</text><rect x="10" y="56" width="80" height="12" rx="2" fill="#FBE8DC"/><text x="50" y="65" text-anchor="middle" font-size="6" fill="#A04832" font-weight="700">NP: deny-cross</text><rect x="10" y="72" width="80" height="12" rx="2" fill="#3F4A5E"/><text x="50" y="81" text-anchor="middle" font-size="6" fill="#FBF1D6" font-weight="700">PSA: restricted</text></g>
    <g transform="translate(110,22)"><rect width="100" height="120" rx="6" fill="#E0EFE6" stroke="#5A9F7A" stroke-width="1.5"/><text x="50" y="16" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">team-b</text><rect x="10" y="24" width="80" height="12" rx="2" fill="#FBF1D6"/><text x="50" y="33" text-anchor="middle" font-size="6" fill="#5A4F45" font-weight="700">quota: 4 CPU</text><rect x="10" y="40" width="80" height="12" rx="2" fill="#E0EFE6"/><text x="50" y="49" text-anchor="middle" font-size="6" fill="#3D7857" font-weight="700">RBAC: team-b only</text><rect x="10" y="56" width="80" height="12" rx="2" fill="#FBE8DC"/><text x="50" y="65" text-anchor="middle" font-size="6" fill="#A04832" font-weight="700">NP: deny-cross</text><rect x="10" y="72" width="80" height="12" rx="2" fill="#3F4A5E"/><text x="50" y="81" text-anchor="middle" font-size="6" fill="#FBF1D6" font-weight="700">PSA: restricted</text></g>
    <g transform="translate(220,22)"><rect width="100" height="120" rx="6" fill="#FBE8DC" stroke="#A04832" stroke-width="1.5"/><text x="50" y="16" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">team-c</text><rect x="10" y="24" width="80" height="12" rx="2" fill="#FBF1D6"/><text x="50" y="33" text-anchor="middle" font-size="6" fill="#5A4F45" font-weight="700">quota: 12 CPU</text><rect x="10" y="40" width="80" height="12" rx="2" fill="#E0EFE6"/><text x="50" y="49" text-anchor="middle" font-size="6" fill="#3D7857" font-weight="700">RBAC: team-c only</text><rect x="10" y="56" width="80" height="12" rx="2" fill="#FBE8DC"/><text x="50" y="65" text-anchor="middle" font-size="6" fill="#A04832" font-weight="700">NP: deny-cross</text><rect x="10" y="72" width="80" height="12" rx="2" fill="#3F4A5E"/><text x="50" y="81" text-anchor="middle" font-size="6" fill="#FBF1D6" font-weight="700">PSA: restricted</text></g>
  </g>
  <!-- kube-bench card -->
  <g transform="translate(400,55)">
    <rect width="240" height="140" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="120" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">CIS BENCHMARK · kube-bench</text>
    <rect x="14" y="22" width="212" height="20" rx="2" fill="#E0EFE6" stroke="#3D7857"/>
    <text x="20" y="36" font-size="8" font-weight="700" fill="#3D7857">PASS · 4.1.1 secure kubelet config</text>
    <rect x="14" y="46" width="212" height="20" rx="2" fill="#E0EFE6" stroke="#3D7857"/>
    <text x="20" y="60" font-size="8" font-weight="700" fill="#3D7857">PASS · 5.1.1 cluster-admin</text>
    <rect x="14" y="70" width="212" height="20" rx="2" fill="#FBE8DC" stroke="#A04832"/>
    <text x="20" y="84" font-size="8" font-weight="700" fill="#A04832">FAIL · 5.7.3 default SA</text>
    <rect x="14" y="94" width="212" height="20" rx="2" fill="#FBF1D6" stroke="#8B5A00"/>
    <text x="20" y="108" font-size="8" font-weight="700" fill="#8B5A00">WARN · 1.2.6 audit log</text>
    <text x="120" y="132" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">112/120 controls passing</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="31",
    title_short="multi-tenancy",
    title_full="Multi-Tenancy & Hardening · Quotas, Limits, kube-bench, Hierarchies",
    title_html="Lesson 31 — Multi-Tenancy & Hardening · K-COM",
    module_eyebrow="Module 13 · Lesson 31 · the security and isolation toolkit",
    hero_sub_html='K8s namespaces are <em>logical</em> boundaries — not security boundaries by default. To turn a namespace into something close to a tenant boundary, you stack: <strong>RBAC</strong> (Lesson 27) + <strong>NetworkPolicy / ANP</strong> (Lessons 17, 26) + <strong>PSA</strong> (Lesson 28) + <strong>ResourceQuota</strong> + <strong>LimitRange</strong>. Plus <strong>kube-bench</strong> for cluster-level CIS hardening, and the <strong>HierarchicalNamespaces</strong> CRD for namespace trees.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Multi-tenant SaaS cluster. Tenant A\'s ML training job runs without a ResourceQuota. By accident, it requests 200 GB of memory and gets it. The node\'s kubelet starts evicting other Pods to make room. Tenant B\'s production traffic-serving workload eviction-storms across the cluster. Outage spreads to four customers. <em>The fix is mundane: ResourceQuota + LimitRange in every tenant namespace</em>. The CIS Kubernetes Benchmark mandates this. Today\'s lesson is the hardening toolkit that turns this from theoretical compliance into actually enforced.',
    stamp_html='Namespaces are logical, not security boundaries. Multi-tenancy stacks: RBAC + NetworkPolicy + PSA + <strong>ResourceQuota</strong> (cap CPU/mem/object counts per namespace) + <strong>LimitRange</strong> (per-Pod min/max defaults). Run <strong>kube-bench</strong> regularly for CIS Benchmark scoring. Use <strong>HierarchicalNamespaces (HNC)</strong> for namespace trees with inherited policy. For real isolation: <strong>vCluster</strong>, <strong>kata containers</strong>, or separate clusters.',
    district_pin="kt-pin27",
    district_label="Watchtower — Tenant Compound Aerial",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="The myth of namespace isolation",
            body_html="""    <p>Namespaces are an organisational primitive: scope for names (\"<code>web</code> in <code>team-a</code>\" doesn\'t collide with \"<code>web</code> in <code>team-b</code>\"), scope for RBAC, scope for ResourceQuota. <em>They\'re not security boundaries by default</em>. Out of the box:</p>
    <ul>
      <li>Pods in different namespaces share a node — a kernel exploit in one Pod compromises the node.</li>
      <li>Pods in different namespaces can talk to each other (until a NetworkPolicy says otherwise).</li>
      <li>Anyone with cluster-admin sees everything.</li>
      <li>Resource exhaustion in one namespace can starve others.</li>
    </ul>
    <p>To approximate tenant isolation, you stack:</p>
    <ol>
      <li><strong>RBAC</strong> — tenants can only see/touch their own namespace.</li>
      <li><strong>NetworkPolicy / ANP</strong> — tenants can\'t talk to each other.</li>
      <li><strong>PSA</strong> — Pods can\'t escape via privileged options.</li>
      <li><strong>ResourceQuota</strong> — tenants can\'t starve others.</li>
      <li><strong>LimitRange</strong> — Pods always have requests + limits.</li>
    </ol>
    <p>This is \"soft multi-tenancy\" — sufficient when tenants are within one organisation. For \"hard multi-tenancy\" (untrusted tenants), you need stronger isolation: vCluster (virtual K8s in a Pod), kata containers (lightweight VM per Pod), or separate clusters.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · ResourceQuota and LimitRange",
            h2="The two namespace-level resource gates",
            body_html="""    <p><strong>ResourceQuota</strong> caps total resources usable in a namespace:</p>
    <ul>
      <li><code>requests.cpu</code>, <code>requests.memory</code>, <code>limits.cpu</code>, <code>limits.memory</code> — total across all Pods.</li>
      <li><code>persistentvolumeclaims</code>, <code>requests.storage</code> — storage objects + total size.</li>
      <li>Object counts: <code>pods</code>, <code>services</code>, <code>secrets</code>, <code>configmaps</code>.</li>
      <li>Special: <code>count/{resource}</code> for arbitrary CRDs.</li>
    </ul>
    <p>If a Pod creation would exceed the quota, the Pod is rejected at admission with a clear message. Empower this with PriorityClass scopes (Lesson 23): \"this quota only applies to Pods at priority &lt; standard,\" so critical workloads can preempt batch.</p>
    <p><strong>LimitRange</strong> sets per-Pod or per-container min/max + defaults:</p>
    <ul>
      <li><code>default</code> requests + limits (applied if Pod spec omits them).</li>
      <li>Min / max — reject Pods outside this range.</li>
      <li>Default request / limit ratios.</li>
    </ul>
    <p>The pair: ResourceQuota caps the tenant\'s aggregate; LimitRange ensures every Pod has reasonable defaults so they actually count toward the quota. Without LimitRange, a Pod with no resource requests counts as 0 against ResourceQuota — quota becomes meaningless.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · kube-bench and CIS Benchmark",
            h2="Run the audit, fix what fails",
            body_html="""    <p>The <strong>CIS Kubernetes Benchmark</strong> is a community-maintained checklist of hardening controls — kubelet flags, API server flags, etcd encryption, RBAC defaults, PSA enforcement, network policy presence. <strong>kube-bench</strong> (Aqua) is the open-source tool that runs the benchmark against a cluster and produces pass / fail / warn results.</p>
    <p>Typical first-run findings:</p>
    <ul>
      <li>API server: <code>--anonymous-auth=false</code> not set (anonymous requests allowed).</li>
      <li>Kubelet: <code>--read-only-port=10255</code> still open (deprecated, leaks metrics).</li>
      <li>etcd: client cert auth not enforced.</li>
      <li>Default ServiceAccount: has automount enabled.</li>
      <li>No audit policy configured.</li>
    </ul>
    <p>Run kube-bench on every cluster on a schedule (e.g., a CronJob with the kube-bench image). Pipe results into PolicyReports or a SIEM. Track score over time as a metric.</p>
    <p>For managed clusters (EKS, GKE, AKS), some controls are not your responsibility (the cloud manages the API server). kube-bench has provider-specific profiles — pick the right one to avoid false alarms on cloud-managed components.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Hierarchical Namespaces and isolation patterns",
            h2="When flat namespaces aren\'t enough",
            body_html="""    <p>Flat namespaces work fine for ~50 tenants. Beyond that, the policy soup gets unwieldy: every new namespace needs a NetworkPolicy, ResourceQuota, RBAC bindings created. Two patterns scale:</p>
    <ul>
      <li><strong>HierarchicalNamespaces (HNC)</strong> — a CRD that creates parent/child relationships. RBAC + NetworkPolicy + ResourceQuota inherit from parent to child. Tenant gets a parent namespace; sub-environments (dev / staging / prod) are child namespaces. Policy maintained at the parent.</li>
      <li><strong>Cluster-API + per-tenant clusters</strong> — for hard multi-tenancy, give each tenant a dedicated cluster managed via Cluster API. More overhead, complete isolation.</li>
      <li><strong>vCluster</strong> — runs a virtual K8s API server inside a host cluster\'s Pod. Tenants get a real K8s cluster experience (their own kube-apiserver, schedulers, CRDs) without provisioning real nodes. Isolation by virtualisation.</li>
    </ul>
    <p>Other isolation knobs:</p>
    <ul>
      <li><strong>Node pools per tenant</strong> — taint nodes; only tenant\'s SA can tolerate. Reduces noisy-neighbour and kernel-shared-attack-surface.</li>
      <li><strong>Kata Containers / gVisor</strong> — runtime-level sandbox. Each Pod runs in a lightweight VM (Kata) or syscall-filtering process (gVisor). Defense-in-depth against kernel exploits.</li>
      <li><strong>Pod-to-Pod mTLS via service mesh</strong> — Lesson 43. Adds identity-aware encryption to soft tenancy.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The 2026 reality: most enterprise multi-tenancy is soft tenancy with the standard stack (RBAC + ANP + PSA + Quota + LimitRange) plus per-tenant node pools for noisy-neighbour control. Hard tenancy (truly untrusted users running arbitrary code) is rare outside of CI build runners, Jupyter notebook hosting, and similar use cases — those should use vCluster or separate clusters.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A tenant namespace has a ResourceQuota of <code>requests.cpu: 8</code> but no LimitRange. A user submits 50 Pods with no <code>resources.requests</code> set. What happens?",
            options=[
                ("a) Pods are rejected — quota is enforced", False),
                ("b) Pods are admitted — they each count as 0 CPU against the quota; quota is effectively bypassed", True),
                ("c) Pods get default 500m requests and the quota fills up at 16 Pods", False),
            ],
            feedback="<strong>Answer: b.</strong> Without LimitRange providing defaults, Pods without explicit requests count as zero against ResourceQuota. The quota becomes meaningless. <strong>Always pair ResourceQuota with LimitRange</strong> so every Pod has reasonable defaults that actually consume quota.",
        ),
    },
    before_after_before='<p>\"We use namespaces for tenants.\" Reality: tenant A\'s workload eats every node\'s memory; tenant B is evicted; cross-tenant network traffic flows freely; nobody noticed someone enabled host networking on a Pod last quarter. Compliance audit reveals 23 CIS findings nobody had time to fix.</p>',
    before_after_after='<p>Namespace = RBAC + ANP + PSA + ResourceQuota + LimitRange. Per-tenant node pools for noisy-neighbour control. kube-bench scoring tracked as a metric, baseline: 95%+. New tenant onboarding = a Helm chart that lays down all the boilerplate. Auditor pulls a kube-bench report; sees compliance evidence.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Namespaces don\'t isolate; <em>policy stacks</em> isolate. The cluster\'s safety is the sum of its policies.</p>',
    analogy_intro_html='<p>From the Watchtower we look down at K-Town\'s tenant district: a fenced grid of compounds, each with its own gate, RBAC plaque on the door, NetworkPolicy fence around it, posted PSA standard on the wall, and a metered utility meter (ResourceQuota) that cuts power when the tenant exceeds their allocation. A separate watchtower department runs a regular CIS audit (kube-bench) and posts the city\'s overall score on a noticeboard. New tenants get a standard build (a Helm chart laying all this down). For sensitive operations (banks, ML training labs), tenants get either an isolated wing (per-tenant node pool) or their own out-building (vCluster / separate cluster).</p>',
    translation_rows=[
        ("Compound fence", "<code>NetworkPolicy</code> + <code>AdminNetworkPolicy</code>"),
        ("RBAC plaque on the door", "<code>Role</code> / <code>RoleBinding</code> per namespace"),
        ("Posted PSA standard", "<code>pod-security.kubernetes.io/enforce</code> label"),
        ("Metered utility meter", "<code>ResourceQuota</code>"),
        ("Default fixture sizes", "<code>LimitRange</code>"),
        ("Citywide CIS audit", "kube-bench against CIS Kubernetes Benchmark"),
        ("Compound family tree", "HierarchicalNamespaces (HNC)"),
        ("Isolated outbuilding", "vCluster / per-tenant cluster"),
        ("Hardened delivery vehicle", "Kata Containers / gVisor"),
    ],
    analogy_stops="The analogy stops here: K8s tenants don\'t have a real fence — every namespace shares the underlying nodes. \"Isolation\" is a sum of policies; for true isolation use vCluster, Kata, or separate clusters.",
    eli5='Each kid gets their own room with their own toys, their own snack budget, and a list of rules on the door. They can\'t go into other kids\' rooms. The grown-ups check the rule lists are still up.',
    eli10="Multi-tenancy in K8s is layered policy. Per namespace: RBAC restricts visibility/actions, NetworkPolicy or ANP restricts traffic, PSA enforces Pod-security profile, ResourceQuota caps total resource use, LimitRange enforces sane per-Pod defaults. kube-bench scores the whole cluster against the CIS Kubernetes Benchmark; treat the score as a tracked metric. For scale, HierarchicalNamespaces (HNC) lets policies cascade down a namespace tree. For untrusted tenants, escalate to vCluster, Kata Containers, gVisor, or separate clusters.",
    scenarios=[
        Scenario(name="A SaaS with 200 tenant namespaces", body="HNC for tenant tree (parent: org, children: dev/staging/prod). NetworkPolicy + RBAC inherited from parent. Per-namespace ResourceQuota + LimitRange laid down by a Kyverno generate policy when a new namespace is created. Onboarding new tenant: 1 Helm release. Time-to-isolated-tenant: 5 minutes."),
        Scenario(name="A bank running per-tenant node pools", body="Tenants tagged by sensitivity: <code>sensitivity=public</code>, <code>sensitivity=internal</code>, <code>sensitivity=restricted</code>. Node pools tainted matching. Public tenants can\'t reach restricted nodes; restricted Pods can\'t share kernels with less-trusted ones. Combined with PSA-restricted profile + Falco runtime monitoring."),
        Scenario(name="A startup running CI build pods", body="Each PR builds in an ephemeral namespace with vCluster (isolated K8s API). Build job runs in Kata Containers (lightweight VM per Pod). Tenant code can\'t escape into the host cluster. After CI, namespace is deleted via Kyverno cleanup policy."),
        Scenario(name="A team using kube-bench in CI", body="Every cluster runs kube-bench daily as a CronJob, output piped to S3. CI pipeline pulls latest report; fails if score drops below 92%. Average score: 96%, with the 4% being known-acceptable findings (audit log centralisation pending). Compliance auditor receives the historical trend."),
    ],
    misconceptions=[
        Misconception(myth="Namespaces are security boundaries.", truth="They\'re organisational boundaries. Security comes from layered policy: RBAC + NetworkPolicy + PSA + Quota + LimitRange. Without them, a namespace is just a name prefix."),
        Misconception(myth="ResourceQuota alone protects against noisy neighbours.", truth="Without LimitRange providing defaults, Pods can submit with zero requests and not count against quota. Always pair them. Many real outages start here."),
        Misconception(myth="kube-bench has to be 100% to be useful.", truth="100% is rarely realistic — some controls don\'t apply to your setup, some are deliberately exempted. Track the trend, document exceptions, focus on closing the gaps that matter (RBAC, PSA, audit log)."),
    ],
    flashcards=[
        Flashcard(front="Are namespaces security boundaries?", back="No, they\'re organisational/logical boundaries. Security comes from layered policy: RBAC + NetworkPolicy/ANP + PSA + ResourceQuota + LimitRange."),
        Flashcard(front="ResourceQuota?", back="Caps namespace-aggregate resource usage: CPU, memory, storage, object counts. Enforced at admission. Can be scoped to PriorityClasses."),
        Flashcard(front="LimitRange?", back="Per-Pod or per-container min/max + defaults. Applies <em>defaults</em> to Pods missing requests/limits. Required for ResourceQuota to actually work."),
        Flashcard(front="Why pair ResourceQuota + LimitRange?", back="Without LimitRange defaults, Pods without explicit requests count as 0 toward quota. Quota becomes ineffective. LimitRange ensures sane defaults; quota then actually caps."),
        Flashcard(front="What is kube-bench?", back="Aqua\'s open-source tool. Runs CIS Kubernetes Benchmark against a cluster and reports pass/fail/warn. Run on schedule; treat score as metric."),
        Flashcard(front="HierarchicalNamespaces (HNC)?", back="CRD adding parent/child relationships. RBAC + NetworkPolicy + ResourceQuota cascade down. Scales policy management at 50+ tenants."),
        Flashcard(front="vCluster?", back="Run a virtual K8s API server in a Pod. Tenants get a full K8s experience without real cluster overhead. Strong isolation."),
        Flashcard(front="When do you need hard multi-tenancy?", back="Truly untrusted code execution: CI build runners, Jupyter notebook hosting, multi-tenant SaaS where tenants run arbitrary workloads. Use vCluster, Kata, or separate clusters."),
    ],
    quizzes=[
        Quiz(prompt="Your CISO says: \"prove no Pod in production can run privileged.\" What\'s the layered control + audit?", answer="<strong>Control layers:</strong> (1) PSA: <code>pod-security.kubernetes.io/enforce: restricted</code> on every prod namespace. Restricts privileged, hostPath, hostNetwork, etc. (2) Kyverno or VAP rule: \"<code>spec.containers[*].securityContext.privileged != true</code>\" — defense in depth. (3) NetworkPolicy + AdminNetworkPolicy: even if a privileged Pod somehow runs, its egress is restricted. <strong>Audit:</strong> (1) <code>kubectl get pods -A -o jsonpath='{.items[?(@.spec.containers[*].securityContext.privileged==true)]}'</code> — should return nothing. (2) PolicyReport CRD output: any violations of \"no privileged\" policies. (3) kube-bench control 5.2.1 (\"minimize the admission of privileged containers\"): should pass. (4) Audit log: alerts on any Pod creation with <code>privileged: true</code>. The combination is what holds up under scrutiny."),
        Quiz(prompt="A platform team operates 200 tenant namespaces flat. Adding a new policy means a Kyverno generate rule + 200 places to update. They consider HNC. Worth it?", answer="<strong>Yes, with caveats.</strong> HNC lets parent policies cascade — write once, apply to many. <strong>Trade-offs:</strong> (1) HNC is a CRD + controller — operational complexity. (2) Some K8s features don\'t play perfectly with HNC (specific webhook patterns). (3) HNC\'s policy inheritance covers RBAC, NetworkPolicy, ResourceQuota, LimitRange — exactly the right primitives. <strong>Migration:</strong> install HNC; pick a pilot tenant; create a parent namespace; convert child relationships incrementally. <strong>Verdict:</strong> at 50+ tenants, HNC pays off. At &lt;20, the overhead probably isn\'t worth it. The 2026 community trend is HNC-or-cluster-API for orgs at scale."),
        Quiz(prompt="You\'re asked to spec a new \"hard multi-tenant\" cluster for hosting customer-uploaded ML notebooks. Tenants are untrusted. <strong>Click for the design. ▼</strong>", cyoa=True, cyoa_tag="the design", answer="<strong>Recommended approach: vCluster + Kata Containers + per-tenant node pools.</strong> <strong>Layer 1 — vCluster per tenant.</strong> Each tenant gets a virtual K8s API server in a Pod. Tenant\'s API operations don\'t touch the host cluster\'s API server. Tenants can install CRDs, create their own RBAC, etc. Strong API-level isolation. <strong>Layer 2 — Kata Containers as runtime class.</strong> Inside the vCluster, Pods run in Kata\'s lightweight VMs. Kernel exploits don\'t escape the VM. <strong>Layer 3 — per-tenant node pools.</strong> Each tenant\'s vCluster Pods run on tenant-specific tainted nodes. Even if VM escape happens, blast radius is one tenant\'s nodes. <strong>Layer 4 — strong AdminNetworkPolicy.</strong> Tenants can\'t reach each other\'s vClusters or the host cluster\'s control plane. <strong>Layer 5 — runtime monitoring with Falco.</strong> Detect anomalous syscall patterns; alert + auto-isolate. <strong>Layer 6 — quotas at vCluster + node-pool level.</strong> Bound resource use. <strong>Trade-off:</strong> ~3-4× the operational complexity of soft multi-tenancy. Right for genuinely untrusted code; overkill for most multi-team enterprise clusters. <strong>Alternative:</strong> for the most untrusted code, give each tenant a separate dedicated cluster — at scale this is cheaper than the multi-layer approach above."),
    ],
    glossary=[
        GlossaryItem(name="Soft multi-tenancy", definition="Multiple teams sharing a cluster, separated by namespaces + policy. Standard enterprise pattern."),
        GlossaryItem(name="Hard multi-tenancy", definition="Untrusted tenants. Requires VM-level or separate-cluster isolation."),
        GlossaryItem(name="ResourceQuota", definition="Namespace-level cap on total resource usage and object counts."),
        GlossaryItem(name="LimitRange", definition="Per-Pod min/max and defaults for resources. Required to make ResourceQuota effective."),
        GlossaryItem(name="kube-bench", definition="Aqua\'s tool for running CIS Kubernetes Benchmark. Produces pass/fail/warn report."),
        GlossaryItem(name="CIS Kubernetes Benchmark", definition="Community-maintained hardening checklist. The de-facto standard for K8s security baseline."),
        GlossaryItem(name="HierarchicalNamespaces (HNC)", definition="CRD adding parent/child namespace relationships with policy inheritance."),
        GlossaryItem(name="vCluster", definition="Virtual K8s API server inside a host cluster\'s Pod. Strong API-level isolation per tenant."),
        GlossaryItem(name="Kata Containers", definition="Container runtime that runs each Pod in a lightweight VM. Kernel-level isolation."),
        GlossaryItem(name="gVisor", definition="Google\'s syscall-filtering sandbox. Runs containers in a userspace kernel for syscall isolation."),
        GlossaryItem(name="Cluster API", definition="K8s SIG project for managing K8s clusters declaratively. Used for per-tenant cluster patterns."),
        GlossaryItem(name="Falco", definition="CNCF runtime security tool. Detects anomalous syscall patterns at runtime."),
    ],
    recap_lead="Namespaces aren\'t security boundaries; layered policy is. RBAC + NetworkPolicy + PSA + ResourceQuota + LimitRange make a namespace approximate a tenant. kube-bench tracks CIS compliance. HNC scales policy. For untrusted tenants: vCluster, Kata, separate clusters.",
    recap_next="<strong>Next — Lesson 32: Observability Part 1.</strong> Module 14 begins. Logs and metrics — the core observability signals, OpenTelemetry, Prometheus + push gateway alternatives, log pipelines (Vector, Fluent Bit). New K-Town district: Observatory.",
)
