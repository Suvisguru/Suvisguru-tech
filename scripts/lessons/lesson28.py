from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Watchtower hallway after the auth checkpoint: a request envelope passes a mutation desk that adds stamps, then a validation desk with PSA / VAP / webhook checks; rejected envelopes go into a deny tray.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">WATCHTOWER · ADMISSION HALLWAY</text>
  <!-- Envelope incoming -->
  <g transform="translate(30,90)">
    <rect width="60" height="40" rx="3" fill="#FBF1D6" stroke="#5A4F45" stroke-width="1.4"/>
    <path d="M 0 0 L 30 22 L 60 0" fill="none" stroke="#5A4F45" stroke-width="1.4"/>
    <text x="30" y="58" text-anchor="middle" font-size="8" font-weight="700" fill="#5A4F45">request</text>
  </g>
  <!-- Arrow -->
  <line x1="100" y1="110" x2="135" y2="110" stroke="#A04832" stroke-width="2.5" marker-end="url(#arr2)"/>
  <defs><marker id="arr2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#A04832"/></marker></defs>
  <!-- Mutation desk -->
  <g transform="translate(140,55)">
    <rect width="140" height="120" rx="6" fill="#E8B547" stroke="#8B5A00" stroke-width="1.5"/>
    <text x="70" y="18" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">MUTATION</text>
    <text x="70" y="32" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">add defaults / labels</text>
    <rect x="14" y="42" width="112" height="18" rx="2" fill="#FBF1D6"/>
    <text x="20" y="55" font-size="7" fill="#5A4F45">+ default labels</text>
    <rect x="14" y="64" width="112" height="18" rx="2" fill="#FBF1D6"/>
    <text x="20" y="77" font-size="7" fill="#5A4F45">+ topology spread</text>
    <rect x="14" y="86" width="112" height="18" rx="2" fill="#FBF1D6"/>
    <text x="20" y="99" font-size="7" fill="#5A4F45">+ resource defaults</text>
  </g>
  <line x1="290" y1="110" x2="325" y2="110" stroke="#A04832" stroke-width="2.5" marker-end="url(#arr2)"/>
  <!-- Validation desk -->
  <g transform="translate(330,40)">
    <rect width="180" height="150" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="90" y="18" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">VALIDATION</text>
    <text x="90" y="30" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">accept / reject</text>
    <rect x="14" y="40" width="152" height="22" rx="2" fill="#5A9F7A"/>
    <text x="20" y="54" font-size="7" font-weight="700" fill="#FFFFFF">PSA · namespace label</text>
    <rect x="14" y="66" width="152" height="22" rx="2" fill="#A04832"/>
    <text x="20" y="80" font-size="7" font-weight="700" fill="#FFFFFF">VAP · CEL in-cluster</text>
    <rect x="14" y="92" width="152" height="22" rx="2" fill="#4A8FA8"/>
    <text x="20" y="106" font-size="7" font-weight="700" fill="#FFFFFF">webhook · Kyverno/OPA</text>
    <text x="90" y="135" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">all must accept</text>
  </g>
  <line x1="520" y1="80" x2="555" y2="80" stroke="#3D7857" stroke-width="2.5" marker-end="url(#arr3)"/>
  <line x1="520" y1="160" x2="555" y2="160" stroke="#A04832" stroke-width="2.5" marker-end="url(#arr2)"/>
  <defs><marker id="arr3" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#3D7857"/></marker></defs>
  <!-- Persisted -->
  <g transform="translate(560,55)">
    <rect width="80" height="50" rx="4" fill="#E0EFE6" stroke="#3D7857" stroke-width="1.5"/>
    <text x="40" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#3D7857">etcd</text>
    <text x="40" y="40" text-anchor="middle" font-size="7" fill="#3D7857" font-style="italic">accepted</text>
  </g>
  <g transform="translate(560,135)">
    <rect width="80" height="50" rx="4" fill="#FBE8DC" stroke="#A04832" stroke-width="1.5"/>
    <text x="40" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">DENY</text>
    <text x="40" y="40" text-anchor="middle" font-size="7" fill="#A04832" font-style="italic">rejected</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="28",
    title_short="admission control",
    title_full="Admission Control · ValidatingAdmissionPolicy, PSA, Webhooks",
    title_html="Lesson 28 — Admission Control · K-COM",
    module_eyebrow="Module 13 · Lesson 28 · the last gate before etcd",
    hero_sub_html='Authentication answered \"who?\"; RBAC answered \"can you?\". Admission asks \"<strong>should you?</strong>\" — the last gate before a write hits etcd. K8s ships built-in admission controllers (PSA, ResourceQuota, LimitRange) and lets you add your own via two paths: in-cluster CEL via <strong>ValidatingAdmissionPolicy</strong> (GA in 1.30) and external webhooks (Kyverno, OPA Gatekeeper).',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Compliance audit. Auditor: \"prove no privileged Pods can run in production.\" Team\'s answer: \"we have a runbook saying don\'t do that.\" Auditor: \"is it enforced?\" Silence. Reality: a developer ran <code>kubectl run debug --privileged --image=alpine</code> two months ago to debug a network issue, never cleaned up. Pod still running with full host access. <strong>Admission control</strong> is the layer that would have rejected that <code>kubectl run</code> at the API server before it ever reached etcd. Today\'s lesson: how to lock the gate.',
    stamp_html='Admission runs <em>after</em> auth/RBAC, <em>before</em> persistence. <strong>Mutating</strong> admission can rewrite the object (add defaults, inject sidecars). <strong>Validating</strong> admission can accept or reject. Three modern tools: <strong>Pod Security Admission (PSA)</strong> for the standard Pod-security profiles, <strong>ValidatingAdmissionPolicy (VAP)</strong> for CEL-based rules in-cluster (no webhook needed, GA 1.30), and <strong>policy webhooks</strong> (Kyverno, OPA Gatekeeper) for richer logic.',
    district_pin="kt-pin27",
    district_label="Watchtower — Admission Hallway",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Where admission sits in the request flow",
            body_html="""    <p>Walk a write request through the API server:</p>
    <ol>
      <li><strong>Authentication</strong> establishes the user.</li>
      <li><strong>Authorisation (RBAC)</strong> checks if the verb on the resource is allowed.</li>
      <li><strong>Mutating admission</strong> — controllers can rewrite the object before it\'s validated.</li>
      <li><strong>Schema validation</strong> — does the object match its CRD/built-in schema?</li>
      <li><strong>Validating admission</strong> — final accept/reject by validators.</li>
      <li><strong>Persistence</strong> — write to etcd. Done.</li>
    </ol>
    <p>Mutating runs first; validating runs last. The order matters: mutators can add fields that validators check. A common pattern: mutating admission injects a default <code>resources.requests</code> if the Pod didn\'t set one; validating admission then enforces \"all containers must have requests.\"</p>
    <p>Built-in admission controllers ship with kube-apiserver: <code>NamespaceLifecycle</code>, <code>ResourceQuota</code>, <code>LimitRange</code>, <code>PodSecurity</code> (PSA), <code>ServiceAccount</code> (auto-injects the SA token mount), and ~20 others. They run automatically and don\'t need external infrastructure.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Pod Security Admission (PSA)",
            h2="The successor to PodSecurityPolicy",
            body_html="""    <p>K8s 1.25 removed <strong>PodSecurityPolicy</strong> (PSP) — the original Pod-level security policy CRD that nobody loved. Replaced by <strong>Pod Security Admission</strong> (PSA): a built-in admission controller, namespace-scoped, configured via labels.</p>
    <p>Three security profiles, ordered by strictness:</p>
    <ul>
      <li><strong><code>privileged</code></strong> — \"do whatever you want\" (= no restrictions).</li>
      <li><strong><code>baseline</code></strong> — disallow known-dangerous things: privileged containers, hostPath, hostNetwork, hostPID. Permits most of what apps actually need.</li>
      <li><strong><code>restricted</code></strong> — strong hardening: must run as non-root, drop ALL capabilities (or all but a small allow-list), seccomp/AppArmor required, read-only root filesystem encouraged. The 80% of workloads that don\'t need elevation should run here.</li>
    </ul>
    <p>For each namespace, set labels:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>pod-security.kubernetes.io/enforce: restricted
pod-security.kubernetes.io/enforce-version: latest
pod-security.kubernetes.io/audit: restricted
pod-security.kubernetes.io/warn: restricted</code></pre>
    <p><code>enforce</code> rejects violations. <code>audit</code> logs them. <code>warn</code> shows them to the user. Most teams ship namespaces with <code>enforce: baseline</code> + <code>warn: restricted</code> as a transition pattern.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · ValidatingAdmissionPolicy (VAP)",
            h2="Custom rules in-cluster, no webhook needed",
            body_html="""    <p>Pre-VAP, custom admission rules required a <strong>webhook</strong>: a separate Pod the API server calls on every admission. Webhooks add latency, fail-open vs fail-closed tradeoffs, and a chicken-and-egg problem (\"the webhook is down, can I deploy a fix?\").</p>
    <p><strong>ValidatingAdmissionPolicy</strong> (alpha 1.26, beta 1.28, GA 1.30) lets you write admission rules in <strong>CEL</strong> (Common Expression Language) and run them <em>inside the API server</em>. No webhook, no Pod, no latency. Two CRDs:</p>
    <ul>
      <li><strong><code>ValidatingAdmissionPolicy</code></strong> — defines the rule. Selects which resources to apply to. CEL expression returns true (allow) or false (deny).</li>
      <li><strong><code>ValidatingAdmissionPolicyBinding</code></strong> — binds the policy to specific namespaces or label selectors. Same shape as RoleBinding.</li>
    </ul>
    <p>Example CEL: \"every Deployment must have a <code>team</code> label.\" CEL: <code>has(object.metadata.labels.team)</code>. Selector: <code>resources: [\"deployments\"]</code>. Binding: every namespace except <code>kube-system</code>. Done — five-line YAML, in-cluster enforcement, zero infrastructure.</p>
    <p>K8s 1.32 added <strong>MutatingAdmissionPolicy</strong> for in-cluster mutation via JSONPatch / CEL — replacing many simple Kyverno mutate policies. By 2026, most teams have migrated their simple validation/mutation rules to VAP/MAP and reserve webhooks (Kyverno, OPA) for cross-cutting policies that need richer logic or external state.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The big architectural win of VAP: admission rules are <em>inspectable</em>. Operators can <code>kubectl get validatingadmissionpolicies</code> and read the CEL. With webhooks, you have to know which Pod implements which rule and read its source. VAP is also the basis for K8s\'s emerging \"policy as data\" story — you ship policies as YAML alongside your manifests.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Webhook admission (Kyverno, Gatekeeper)",
            h2="When CEL isn\'t enough",
            body_html="""    <p>VAP/MAP cover most of what teams used to need webhooks for. The remaining cases (richer logic, external lookups, complex state, generation/cleanup, image scanning integration) still call for webhook-based policy engines:</p>
    <ul>
      <li><strong>Kyverno</strong> — K8s-native; policies as YAML (no DSL). Mutate, validate, generate, cleanup. Most popular in 2026 by deployments.</li>
      <li><strong>OPA Gatekeeper</strong> — uses Rego. More flexible, much steeper learning curve. Strong in regulated environments.</li>
      <li><strong>Custom webhooks</strong> — write your own. Use only when off-the-shelf tools genuinely can\'t express your rule.</li>
    </ul>
    <p>Webhook gotchas:</p>
    <ul>
      <li><strong>Fail policy.</strong> If the webhook is unreachable, do you allow the request (<code>failurePolicy: Ignore</code>) or block it (<code>Fail</code>)? Wrong choice = either security gap or cluster-wide outage.</li>
      <li><strong>Latency.</strong> Every admission request waits for the webhook. A slow webhook degrades every <code>kubectl apply</code>. Cap timeouts (<code>timeoutSeconds: 5</code>).</li>
      <li><strong>Self-bootstrapping.</strong> If your webhook validates itself, you can\'t deploy the webhook. Most policy engines exclude their own namespace; check yours does.</li>
    </ul>
    <p>By 2026, the practical pattern: PSA at the security baseline, VAP/MAP for simple custom rules, Kyverno or Gatekeeper for cross-cutting governance. Lesson 29 covers the policy engines in depth.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team applies a Pod manifest with no <code>resources.requests</code>. The cluster has a mutating admission policy that adds default requests, plus a validating policy that requires every container to have requests. What happens?",
            options=[
                ("a) Pod is rejected — no requests on submission", False),
                ("b) Mutator adds default requests; validator sees them and accepts", True),
                ("c) The two policies conflict; admin must resolve manually", False),
            ],
            feedback="<strong>Answer: b.</strong> Mutating admission runs first, adds the defaults. The validator runs later and sees the now-mutated object with requests in place. This is exactly the intended pattern: mutate-then-validate.",
        ),
    },
    before_after_before='<p>Pre-VAP era: every custom rule was a webhook. Each webhook = a Pod, a Service, certificate management, fail-policy decisions, latency on every admission. Most clusters had 5-10 different webhooks; debugging \"why was my Pod rejected\" meant chasing logs across pods. PodSecurityPolicy (PSP) was the only built-in security primitive, and it was being removed.</p>',
    before_after_after='<p>2026 stack: PSA at the namespace-label level (no infra). VAP/MAP for custom CEL rules in-cluster (no infra). Kyverno or Gatekeeper for the truly complex stuff. Webhook count goes from 10 to 1-2. Admission decisions are inspectable: <code>kubectl get vap</code> shows the rules.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">VAP\'s GA in K8s 1.30 was the most important admission-layer change since admission webhooks were introduced. By 2027, simple webhook-based policy will look anachronistic.</p>',
    analogy_intro_html='<p>The Watchtower\'s admission hallway runs after the identity desk. Three stations along the way. The <strong>stamping desk</strong> (mutating admission) adds default stamps to incoming envelopes — \"please add return address, signature, today\'s date.\" The envelope keeps moving. The <strong>standards bench</strong> (Pod Security Admission) checks every envelope against three pre-printed standards (privileged / baseline / restricted) — namespaces post their preferred standard at their door. The <strong>custom rules counter</strong> (ValidatingAdmissionPolicy) reads CEL expressions written by the cluster\'s policy team — \"every envelope must have a <code>team</code> label\" — and stamps yes or no. Past all three, the envelope reaches the filing room (etcd).</p><p>Two extra rooms behind the counter: a <strong>policy engine office</strong> (Kyverno / OPA Gatekeeper) for rules richer than CEL can handle, and a <strong>webhook switchboard</strong> for the few legacy custom rules. Every desk can stop the envelope; only stamps from the standards bench and custom-rules counter actually <em>say no</em>.</p>',
    translation_rows=[
        ("The stamping desk", "Mutating admission (built-in + webhooks + MutatingAdmissionPolicy)"),
        ("The standards bench", "Pod Security Admission (privileged / baseline / restricted)"),
        ("Pre-printed standards on namespace doors", "PSA labels: <code>pod-security.kubernetes.io/enforce</code>"),
        ("Custom rules counter with CEL slips", "<code>ValidatingAdmissionPolicy</code> + Binding"),
        ("Policy engine office", "Kyverno / OPA Gatekeeper webhooks"),
        ("Filing room", "etcd"),
        ("\"Stop the envelope\" stamp", "Validating admission denial"),
        ("\"Add stamp before forwarding\"", "Mutating admission injection"),
    ],
    analogy_stops="The analogy stops here: real admission decisions happen in microseconds at the API server. Webhook-based ones add network round-trips; in-cluster (VAP/PSA) ones are virtually free. Pick admission patterns with this perf in mind.",
    eli5='Before your drawing goes on the fridge, three checks. First: someone adds your name (mutate). Second: it must follow house rules (PSA). Third: it must follow Mom\'s extra rules (VAP). If any check says no, no fridge.',
    eli10="Admission runs after RBAC, before etcd. Two phases: <strong>mutating</strong> (rewrite the object — defaults, sidecars, labels) and <strong>validating</strong> (accept/reject). Built-in: PSA (Pod Security Admission, replacing PSP) with three profiles (privileged/baseline/restricted) configured via namespace labels. Custom rules: <strong>ValidatingAdmissionPolicy</strong> (GA 1.30) and <strong>MutatingAdmissionPolicy</strong> (1.32+) using CEL — in-cluster, no webhook. Beyond CEL: Kyverno and OPA Gatekeeper webhooks for cross-cutting governance. Modern stack: PSA + VAP + Kyverno or Gatekeeper covers nearly all needs.",
    scenarios=[
        Scenario(name="A SaaS enforcing labels via VAP", body="VAP requires every Deployment to have <code>team</code>, <code>cost-center</code>, <code>environment</code> labels. CEL: <code>has(object.metadata.labels.team) && has(object.metadata.labels[\"cost-center\"])</code>. Bound to every namespace except kube-system. Cost reporting works because every workload has a cost-center label."),
        Scenario(name="A bank running PSA at restricted", body="Production namespaces have <code>enforce: restricted</code>. Workloads must run as non-root, drop ALL capabilities, use seccomp profile <code>RuntimeDefault</code>. Pen-test fails repeatedly because nothing privileged can run. Auditor signs off: \"the cluster enforces hardening at the API.\""),
        Scenario(name="A startup using Kyverno for image policies", body="Kyverno policy: every container image must be from <code>internal-registry.corp/</code> or <code>cgr.dev/chainguard/</code>. <code>quay.io/some-random/image</code> rejected. Combined with VAP for label requirements + PSA for security. Single Kyverno install replaces what used to be five custom webhooks."),
        Scenario(name="A team migrating from webhooks to VAP", body="Had a webhook enforcing \"every Pod must have liveness probe.\" Migration: rewrote as 4-line VAP CEL. Webhook deleted. <code>kubectl apply</code> latency dropped 18ms. Mean Time To Investigate \"why was my Pod rejected\" dropped to seconds: <code>kubectl get validatingadmissionpolicies</code> + read."),
    ],
    misconceptions=[
        Misconception(myth="Mutating and validating admission run together.", truth="They run in two distinct phases. Mutating runs first, validators run after schema check. The two-phase split is intentional: it lets mutators add fields that validators can rely on. <em>All</em> mutators run before any validator."),
        Misconception(myth="VAP can\'t do everything Kyverno does.", truth="Correct — VAP is intentionally simpler. CEL handles validation and (in MAP) basic JSONPatch mutation. Kyverno adds object generation, cleanup, image verification, complex pattern-matching. Use the right tool: VAP for simple per-object rules; Kyverno/Gatekeeper for cross-cutting flows."),
        Misconception(myth="<code>failurePolicy: Fail</code> is always the safer choice for webhooks.", truth="It\'s safer for security but riskier for cluster availability. If the webhook Pod crashes during a kube-apiserver restart, no Pod can be created until the webhook recovers — <em>including the webhook\'s own Pod</em>. Most clusters use <code>Fail</code> with careful exclusions (kube-system, the webhook\'s own namespace) and tight Pod redundancy."),
    ],
    flashcards=[
        Flashcard(front="When does admission run?", back="After authentication + RBAC, before etcd persistence. Two phases: mutating (rewrite) then validating (accept/reject)."),
        Flashcard(front="What is PSA?", back="Pod Security Admission. Built-in admission controller. Three profiles (privileged/baseline/restricted) configured via namespace labels. Replaced PodSecurityPolicy in K8s 1.25."),
        Flashcard(front="Three PSA labels?", back="<code>pod-security.kubernetes.io/enforce</code> (block violations), <code>audit</code> (log violations), <code>warn</code> (show user). Different profiles per label allow gradual rollout."),
        Flashcard(front="What is ValidatingAdmissionPolicy (VAP)?", back="K8s 1.30 GA. CEL-based admission rules running in-cluster (no webhook). Two CRDs: <code>ValidatingAdmissionPolicy</code> (rule) + <code>ValidatingAdmissionPolicyBinding</code> (selector for which namespaces/objects)."),
        Flashcard(front="What is MutatingAdmissionPolicy (MAP)?", back="K8s 1.32+. The mutating cousin of VAP — rewrite objects via CEL/JSONPatch in-cluster, no webhook. Replaces many simple Kyverno mutate policies."),
        Flashcard(front="Kyverno vs OPA Gatekeeper?", back="Kyverno: K8s-native, YAML policies, mutate/validate/generate/cleanup. Gatekeeper: Rego-based, K8s\'s flagship OPA integration, harder to learn but more flexible. Kyverno is more common in 2026."),
        Flashcard(front="failurePolicy on a webhook?", back="<code>Fail</code> = block the request if webhook is unreachable. <code>Ignore</code> = allow it. <code>Fail</code> is safer for security, riskier for availability — pair with careful exclusions."),
        Flashcard(front="Order: which admission runs first?", back="All <em>mutating</em> admission controllers run before any <em>validating</em> admission controller. Within each phase, ordering is by registration order (built-ins by name, webhooks by alphabetical name)."),
    ],
    quizzes=[
        Quiz(prompt="A team adds a ValidatingAdmissionPolicy: \"every container image must come from <code>cgr.dev/...</code> or <code>internal-registry.corp/...</code>.\" The first apply works; the second fails with \"image violates policy.\" How do you debug?", answer="<strong>Step 1:</strong> read the rejection message. The API server returns the policy name + violated rule. <strong>Step 2:</strong> <code>kubectl get vap &lt;name&gt; -o yaml</code> to inspect the CEL. CEL is ordinary YAML; you can read it. <strong>Step 3:</strong> use the CEL expression evaluator: <code>kubectl alpha cel-eval</code> (or any CEL playground) to test the expression against your object. <strong>Step 4:</strong> if it\'s a legitimate exception, add the team\'s namespace to the policy\'s exceptions via VAP exceptions or a label selector on the binding. <strong>Diagnostic-friendliness</strong> is one of VAP\'s biggest wins over webhooks — admission rejections are auditable as data, not opaque webhook errors."),
        Quiz(prompt="A namespace is labelled <code>pod-security.kubernetes.io/enforce: restricted</code>. A developer applies a Pod manifest with <code>securityContext.runAsNonRoot: true</code> but no <code>seccompProfile</code> set. PSA rejects it. Why, and what\'s the fix?", answer="<strong>Why:</strong> PSA <code>restricted</code> profile requires every container to have <code>seccompProfile: RuntimeDefault</code> (or a localhost profile). Setting only <code>runAsNonRoot</code> isn\'t enough. <strong>Fix:</strong> add <code>spec.securityContext.seccompProfile.type: RuntimeDefault</code> at the Pod level (applies to all containers) or per-container. Other restricted requirements: <code>runAsNonRoot: true</code>, drop ALL capabilities, no <code>privileged</code>, no <code>hostPath/hostNetwork/hostPID</code>, AppArmor profile (default OK). For new manifests, copy from a known-good restricted-profile template. K8s docs publish a baseline + restricted reference YAML."),
        Quiz(prompt="The platform team migrates 12 simple webhook policies to VAP. After migration, one webhook (still in place for richer logic) is taking 800ms per admission. <strong>Click for the diagnostic + fix. ▼</strong>", cyoa=True, cyoa_tag="the diagnostic + fix", answer="<strong>Step 1:</strong> identify what the webhook does. Is it making external HTTP calls? Querying a database? Each external call adds latency. <strong>Step 2:</strong> measure where the time goes — add tracing to the webhook\'s admission handler. <strong>Step 3:</strong> common fixes: (a) cache external lookups (e.g., image scan results) in the webhook\'s memory with TTLs. (b) <code>matchPolicy: Exact</code> instead of <code>Equivalent</code> if your selector doesn\'t need wildcard expansion. (c) Tighten <code>rules</code> on the MutatingWebhookConfiguration to only invoke on relevant objects (e.g., only Pods, not every resource). (d) Bump replica count + use anti-affinity to keep webhook Pods on different nodes. <strong>Step 4:</strong> if the rule can be expressed in CEL, migrate it to VAP — VAP is essentially zero-latency. Webhooks are reserved for true cross-cutting policies. <strong>Long-term:</strong> the trend is clear — push everything possible into VAP/MAP, leave webhooks for richer logic with deliberate latency budgets."),
    ],
    glossary=[
        GlossaryItem(name="Admission control", definition="API-server stage between RBAC and persistence. Two phases: mutating + validating."),
        GlossaryItem(name="Mutating admission", definition="Rewrites the request object before validation. Built-in or webhook or MAP."),
        GlossaryItem(name="Validating admission", definition="Accepts or rejects. Built-in or webhook or VAP."),
        GlossaryItem(name="Pod Security Admission (PSA)", definition="Built-in admission controller; namespace-labelled profiles (privileged/baseline/restricted). Replaces PodSecurityPolicy."),
        GlossaryItem(name="ValidatingAdmissionPolicy (VAP)", definition="K8s 1.30 GA. In-cluster CEL-based validating admission; no webhook needed."),
        GlossaryItem(name="MutatingAdmissionPolicy (MAP)", definition="K8s 1.32+. CEL/JSONPatch in-cluster mutation."),
        GlossaryItem(name="ValidatingAdmissionPolicyBinding", definition="Selector for which namespaces / objects the VAP applies to."),
        GlossaryItem(name="CEL", definition="Common Expression Language — Google\'s small expression language. Used by VAP/MAP and many K8s extension points."),
        GlossaryItem(name="Kyverno", definition="K8s-native policy engine. YAML policies for mutate/validate/generate/cleanup."),
        GlossaryItem(name="OPA Gatekeeper", definition="Open Policy Agent\'s K8s integration. Uses Rego."),
        GlossaryItem(name="failurePolicy", definition="Webhook config: <code>Fail</code> blocks if unreachable, <code>Ignore</code> allows."),
        GlossaryItem(name="ResourceQuota / LimitRange", definition="Built-in admission controllers enforcing namespace-level quotas + per-Pod min/max limits."),
    ],
    recap_lead="Admission runs after RBAC, before etcd. Mutating adds defaults; validating accepts/rejects. PSA covers Pod-security baselines via namespace labels. VAP/MAP handle custom CEL rules in-cluster. Kyverno + Gatekeeper handle the rest. Modern admission stacks have far fewer webhooks and far more inspectable policies than 2022.",
    recap_next="<strong>Next — Lesson 29: Policy Engines.</strong> Kyverno and OPA Gatekeeper in depth. When to choose which, common policy patterns, the policy-as-code workflow.",
)
