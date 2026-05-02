from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Watchtower policy library: shelves of policy YAML, with Kyverno (K8s-native, YAML rules) and OPA Gatekeeper (Rego rules) as side-by-side cabinets, plus a policy report board.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">WATCHTOWER · POLICY LIBRARY</text>
  <!-- Kyverno cabinet -->
  <g transform="translate(40,55)">
    <rect width="200" height="140" rx="8" fill="#5A9F7A" stroke="#3D7857" stroke-width="2"/>
    <text x="100" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">KYVERNO</text>
    <text x="100" y="34" text-anchor="middle" font-size="8" fill="#FFFFFF" font-style="italic">K8s-native · YAML rules</text>
    <rect x="14" y="44" width="172" height="22" rx="2" fill="#FFFFFF"/>
    <text x="20" y="58" font-size="8" fill="#3D7857" font-weight="700">validate · require labels</text>
    <rect x="14" y="68" width="172" height="22" rx="2" fill="#FFFFFF"/>
    <text x="20" y="82" font-size="8" fill="#3D7857" font-weight="700">mutate · add sidecar</text>
    <rect x="14" y="92" width="172" height="22" rx="2" fill="#FFFFFF"/>
    <text x="20" y="106" font-size="8" fill="#3D7857" font-weight="700">generate · NetworkPolicy</text>
    <rect x="14" y="116" width="172" height="18" rx="2" fill="#FBF1D6"/>
    <text x="20" y="129" font-size="8" fill="#5A4F45" font-weight="700">verifyImages · cosign</text>
  </g>
  <!-- Gatekeeper cabinet -->
  <g transform="translate(260,55)">
    <rect width="200" height="140" rx="8" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="100" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">OPA GATEKEEPER</text>
    <text x="100" y="34" text-anchor="middle" font-size="8" fill="#FBF1D6" font-style="italic">Rego rules · ConstraintTemplate</text>
    <rect x="14" y="44" width="172" height="40" rx="2" fill="#5A4F45"/>
    <text x="20" y="58" font-size="7" fill="#E8B547">package k8sallowedrepos</text>
    <text x="20" y="68" font-size="7" fill="#FBF1D6">violation[{...}] {{</text>
    <text x="24" y="78" font-size="7" fill="#FBF1D6">not startswith(image,...)</text>
    <rect x="14" y="88" width="172" height="22" rx="2" fill="#FBF1D6"/>
    <text x="20" y="102" font-size="8" fill="#5A4F45" font-weight="700">ConstraintTemplate</text>
    <rect x="14" y="112" width="172" height="22" rx="2" fill="#FBF1D6"/>
    <text x="20" y="126" font-size="8" fill="#5A4F45" font-weight="700">Constraint instances</text>
  </g>
  <!-- Policy report -->
  <g transform="translate(480,55)">
    <rect width="160" height="140" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="80" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">POLICY REPORT</text>
    <text x="80" y="26" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">audit · per-namespace</text>
    <rect x="10" y="34" width="140" height="20" rx="2" fill="#E0EFE6" stroke="#3D7857" stroke-width="0.8"/>
    <text x="14" y="48" font-size="8" fill="#3D7857">✓ pass · 412</text>
    <rect x="10" y="58" width="140" height="20" rx="2" fill="#FBE8DC" stroke="#A04832" stroke-width="0.8"/>
    <text x="14" y="72" font-size="8" fill="#A04832">✗ fail · 7</text>
    <rect x="10" y="82" width="140" height="20" rx="2" fill="#FBF1D6" stroke="#8B5A00" stroke-width="0.8"/>
    <text x="14" y="96" font-size="8" fill="#8B5A00">⚠ warn · 18</text>
    <text x="80" y="120" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">PolicyReport CRD</text>
    <text x="80" y="132" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">— common to both</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="29",
    title_short="policy engines",
    title_full="Policy Engines · Kyverno and OPA Gatekeeper in Depth",
    title_html="Lesson 29 — Policy Engines · K-COM",
    module_eyebrow="Module 13 · Lesson 29 · the policy-as-code workhorses",
    hero_sub_html='Lesson 28 introduced VAP/MAP for in-cluster CEL admission. Beyond CEL — for image verification, object generation, cross-resource validation, declarative policy reports — clusters use a <strong>policy engine</strong>. Two stand out in 2026: <strong>Kyverno</strong> (K8s-native, YAML) and <strong>OPA Gatekeeper</strong> (Rego, more flexible).',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Compliance audit. Auditor: \"prove every production image is signed by your CI key.\" Team\'s answer: \"we have a CI step that signs.\" Auditor: \"who enforces it at deploy time?\" Team realises: nothing. A developer with cluster access could push an unsigned image. Three years of compliance work in jeopardy. The fix is one Kyverno policy: <code>verifyImages</code> with the public key. Five minutes of YAML, zero CI changes, full enforcement at the API server. <em>Policy engines turn aspirational rules into enforced ones.</em>',
    stamp_html='<strong>Kyverno</strong> uses K8s-native YAML for policies (validate / mutate / generate / cleanup / verifyImages). <strong>OPA Gatekeeper</strong> uses Rego (more powerful, harder to learn) via <code>ConstraintTemplate</code> + <code>Constraint</code>. Both produce <strong>PolicyReport</strong> CRDs (a CNCF standard). Pick Kyverno for K8s-only governance; pick Gatekeeper if you already run OPA for non-K8s policy.',
    district_pin="kt-pin27",
    district_label="Watchtower — Policy Library",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What a policy engine actually does",
            body_html="""    <p>A policy engine plugs into K8s admission as a webhook (validating + mutating). On every request, it consults its policy library and replies allow / deny / mutate. That replaces hand-rolled webhooks with a <strong>declarative, auditable</strong> policy library managed in git.</p>
    <p>Five common policy capabilities (Kyverno + Gatekeeper both cover most of them):</p>
    <ul>
      <li><strong>Validate</strong> — accept / reject based on object content. \"Pods must have liveness probes.\"</li>
      <li><strong>Mutate</strong> — rewrite objects. \"Inject default topology-spread constraints.\"</li>
      <li><strong>Generate</strong> — create related objects on triggers. \"When a new namespace is created, create a NetworkPolicy in it.\"</li>
      <li><strong>Cleanup</strong> — delete stale objects. \"Delete completed Jobs older than 7 days.\"</li>
      <li><strong>Verify images</strong> — check image signatures (cosign / Sigstore) and SBOM presence.</li>
    </ul>
    <p>Both engines write reports as <strong>PolicyReport</strong> CRDs (a CNCF Policy WG standard) — every namespace gets a list of pass/fail/warn results. This is your audit evidence: <code>kubectl get policyreport -A</code>.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Kyverno — the K8s-native option",
            h2="YAML policies, no DSL to learn",
            body_html="""    <p>Kyverno was designed K8s-first: policies look like K8s manifests. No new language to learn. The four policy CRDs:</p>
    <ul>
      <li><code>ClusterPolicy</code> / <code>Policy</code> — the rule definitions. Cluster or namespace scope.</li>
      <li><code>PolicyException</code> — explicit exclusions for specific namespaces / workloads. Auditable.</li>
      <li><code>ClusterCleanupPolicy</code> / <code>CleanupPolicy</code> — scheduled deletion rules.</li>
      <li><code>VerifyImages</code> — cosign / Sigstore image verification.</li>
    </ul>
    <p>A typical Kyverno rule:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: require-team-label}
spec:
  validationFailureAction: Enforce
  rules:
  - name: require-team
    match: {any: [{resources: {kinds: [Deployment]}}]}
    validate:
      message: "Deployment must have a 'team' label"
      pattern:
        metadata:
          labels:
            team: "?*"</code></pre>
    <p>Patterns use simple wildcards: <code>?*</code> = required + non-empty, <code>?*</code> = required, etc. For richer logic, Kyverno supports JMESPath and (from v1.11) CEL expressions. The K8s-native feel is its biggest strength: ops engineers can write policies the day they install it.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · OPA Gatekeeper — the Rego option",
            h2="Maximum flexibility, steep learning curve",
            body_html="""    <p>Open Policy Agent (OPA) is a general-purpose policy engine — not K8s-specific. <strong>Gatekeeper</strong> is OPA\'s K8s integration. Policies are written in <strong>Rego</strong>, a declarative logic language. Two CRDs:</p>
    <ul>
      <li><strong><code>ConstraintTemplate</code></strong> — defines a policy <em>type</em> with parameters and Rego logic. \"This template enforces that images come from certain repos; the repos are a parameter.\"</li>
      <li><strong><code>Constraint</code></strong> — instances of a template with specific parameters. \"For namespace A, images must come from <code>internal/</code> or <code>cgr.dev/</code>.\"</li>
    </ul>
    <p>Rego excerpt for the same image-repo policy:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>package k8sallowedrepos
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not any_match(container.image)
  msg := sprintf("image %v from disallowed repo", [container.image])
}
any_match(image) {
  startswith(image, input.parameters.repos[_])
}</code></pre>
    <p>Rego is more powerful than CEL or JMESPath — it can do unification, recursion, complex query logic. The downside: most ops engineers don\'t know it, and debugging Rego is harder. Gatekeeper shines in regulated environments that already use OPA for non-K8s policy (Terraform, IAM, microservice authz).</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Picking one — and the policy-as-code workflow",
            h2="When you should pick which",
            body_html="""    <p>The 2026 guidance:</p>
    <ul>
      <li><strong>Use Kyverno when:</strong> K8s is your only policy domain; ops engineers (not platform engineers) own the policies; you want to ship policies the same week you install the engine.</li>
      <li><strong>Use OPA Gatekeeper when:</strong> You already run OPA for non-K8s things (Terraform validation, microservice authz); you have engineers who know Rego; you need policy logic CEL/JMESPath can\'t express.</li>
      <li><strong>Use both when:</strong> You\'re a large org with separate domains. Most don\'t need this.</li>
    </ul>
    <p>The policy-as-code workflow (works for both):</p>
    <ol>
      <li><strong>Policies in git.</strong> One repo, with PR review for every change. Policies as YAML files; CI runs <code>kyverno test</code> or Gatekeeper\'s test framework against fixture inputs.</li>
      <li><strong>GitOps deploy.</strong> Argo CD or Flux applies policies. Same workflow as any other K8s manifest.</li>
      <li><strong>Audit reports.</strong> <code>kubectl get policyreport -A -o jsonpath</code> dumps the current state. Pipe to your dashboard / SIEM.</li>
      <li><strong>Exemption process.</strong> When a workload genuinely needs an exception, file a <code>PolicyException</code> (Kyverno) or scope a Constraint differently (Gatekeeper). Exceptions are first-class objects, not exceptions in code.</li>
    </ol>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The CNCF Policy Working Group standardised PolicyReport in 2023; both Kyverno and Gatekeeper emit them. This means downstream tooling (Falco for runtime alerts, custom dashboards, Grafana panels) can consume policy results from <em>any</em> engine without engine-specific code. Even custom webhook policies can produce PolicyReport CRDs to participate in this ecosystem.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="Your org already runs OPA for Terraform policy validation in CI. You\'re adding K8s admission policies. Which engine fits best?",
            options=[
                ("a) Kyverno — it\'s simpler", False),
                ("b) Gatekeeper — you already have Rego expertise; share rules + tooling across domains", True),
                ("c) Roll your own webhook", False),
            ],
            feedback="<strong>Answer: b.</strong> If your org has Rego skills + existing OPA infrastructure, Gatekeeper extends that into K8s naturally. The shared engine reduces tool surface. If you had no Rego experience, Kyverno would be faster to adopt.",
        ),
    },
    before_after_before='<p>Pre-policy-engine era: every policy was a hand-rolled webhook (Go service + cert management + Pod redundancy + ad-hoc tests). Each policy = a project. Auditors ask \"show me your enforced rules\" → you point at a Confluence page. Exceptions live in YAML comments and tribal memory.</p>',
    before_after_after='<p>Modern: one Kyverno or Gatekeeper install. Policies as YAML in git, deployed via GitOps. <code>kubectl get policyreport</code> shows current state. Exceptions are <code>PolicyException</code> objects with PR review history. Auditors get a dashboard, not a wiki.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Policy engines + GitOps + PolicyReport is the cleanest compliance story K8s has ever had. The bar of evidence is now \"show me the YAML and the report,\" not \"explain your process.\"</p>',
    analogy_intro_html='<p>Watchtower expanded its admission hallway from Lesson 28 with a full <strong>policy library</strong>. Two cabinets stand side by side. The <strong>Kyverno cabinet</strong> holds rules in plain K-Town vernacular: \"Deployment must have a team label.\" Anyone who can read a Permit Office form can read a Kyverno rule. The <strong>OPA Gatekeeper cabinet</strong> holds rules in a more powerful — but harder to read — formal logic language (Rego), in two parts: a <em>template</em> describing the rule\'s shape, and <em>instances</em> with the specific values for this cluster. Both cabinets produce identical filing reports (PolicyReport CRDs), which makes the auditor\'s job easy: same form regardless of which cabinet wrote the rule.</p>',
    translation_rows=[
        ("Plain-K-Town-vernacular cabinet", "Kyverno"),
        ("Formal-logic cabinet (Rego)", "OPA Gatekeeper"),
        ("Rule template + instances split", "<code>ConstraintTemplate</code> + <code>Constraint</code>"),
        ("Standard filing report", "<code>PolicyReport</code> CRD"),
        ("Mutation: \"add this stamp before forwarding\"", "Kyverno mutate / generate"),
        ("Image-signature checking machine", "<code>verifyImages</code> with cosign"),
        ("\"Excluded by special permit\"", "<code>PolicyException</code> object"),
        ("Cabinet contents in git, deployed by GitOps", "Policy-as-code workflow"),
    ],
    analogy_stops="The analogy stops here: real policy engines are admission webhooks performing decisions in milliseconds. Their evaluation is bounded — Rego with deeply nested logic can be slow; Kyverno patterns can\'t express recursion at all. Pick complexity to match what you actually need.",
    eli5='Two big rule-books for what\'s allowed in the building. One is in plain English. One is in lawyer language. Both produce the same report when an inspector visits.',
    eli10="Policy engines plug into K8s admission and centralise rules. <strong>Kyverno</strong>: K8s-native YAML, no DSL, validate/mutate/generate/cleanup/verifyImages. <strong>OPA Gatekeeper</strong>: Rego-based, more powerful, harder to learn, two-CRD model (ConstraintTemplate + Constraint). Both emit standard PolicyReport CRDs for audit. Picked by org context: Kyverno for K8s-only with ops-team ownership; Gatekeeper for orgs with existing Rego/OPA. Workflow: policies in git → GitOps → PolicyReport audit → PolicyExceptions for the rare opt-out.",
    scenarios=[
        Scenario(name="A SaaS using Kyverno for governance", body="20 ClusterPolicies covering: required labels, NetworkPolicy generation per namespace, image-repo allow-list, cosign image verification, Job cleanup after 7 days, sidecar injection. Total YAML: ~600 lines in git. Auditor reads the policies directly; spends 30 minutes confirming, calls it a day."),
        Scenario(name="A bank running Gatekeeper for cross-domain policy", body="Gatekeeper enforces K8s admission. Same Rego library used by their Terraform-pipeline-Conftest setup for IaC validation. One source of truth for policy logic across IaC + cluster admission. Compliance team trained once, applies everywhere."),
        Scenario(name="A startup migrating from custom webhooks", body="Six hand-rolled validating webhooks, total 3000 LoC of Go. Replaced by 12 Kyverno policies (~250 lines YAML). Engineering hours saved per month: 8. Number of admission outages: dropped to zero (the webhooks used to crash occasionally during deploys; Kyverno is robust)."),
        Scenario(name="A team using Kyverno verifyImages with cosign", body="ClusterPolicy verifies every image is signed by the org\'s cosign public key. Build pipeline signs on push. Unsigned images = rejected at admission. Catches: leaked image-pull credentials being used to run an attacker image. Real incident found in audit logs after policy was installed."),
    ],
    misconceptions=[
        Misconception(myth="Kyverno is just for simple cases; Gatekeeper is for serious work.", truth="Kyverno covers ~90% of typical policies, including image verification + signature checks. \"Serious\" depends on what you mean — for K8s-only, both are equally serious. Gatekeeper\'s edge is multi-domain orgs already using OPA."),
        Misconception(myth="VAP replaces Kyverno / Gatekeeper.", truth="VAP/MAP cover simple per-object rules. For generation, image verification, cleanup, cross-object validation, you still need a policy engine. The 2026 stack is VAP/MAP + Kyverno/Gatekeeper, not one or the other."),
        Misconception(myth="Policies in git = policies that work.", truth="Policies must be tested. Both Kyverno (<code>kyverno test</code>) and Gatekeeper (<code>gator</code>) ship test frameworks. Without tests, a renamed field in K8s upstream silently breaks your policies — and you discover it during incidents."),
    ],
    flashcards=[
        Flashcard(front="Kyverno vs OPA Gatekeeper?", back="Kyverno: K8s-native YAML, no DSL, four capability families. Gatekeeper: Rego-based, OPA\'s K8s integration. ConstraintTemplate + Constraint model. Kyverno is more popular in K8s-only shops; Gatekeeper in OPA-heavy orgs."),
        Flashcard(front="Five Kyverno capabilities?", back="validate, mutate, generate, cleanup, verifyImages. The single engine covers all five. Gatekeeper covers validate + mutate; cleanup/generate need other tools."),
        Flashcard(front="ConstraintTemplate vs Constraint?", back="ConstraintTemplate = rule type with Rego + parameter schema. Constraint = an instance with specific parameters. Gatekeeper-only model — Kyverno collapses this into a single ClusterPolicy/Policy."),
        Flashcard(front="What is PolicyReport?", back="CNCF standard CRD emitted by both Kyverno and Gatekeeper. Per-namespace summary of pass/fail/warn. <code>kubectl get policyreport -A</code> for the audit picture."),
        Flashcard(front="What is verifyImages in Kyverno?", back="Kyverno policy type that checks image signatures (cosign / Sigstore) and SBOM presence at admission. Reject unsigned images. Lesson 30 covers supply chain in depth."),
        Flashcard(front="PolicyException?", back="Kyverno CRD for explicit, auditable opt-outs. \"Namespace X is exempt from policy Y because reason Z.\" Same review process as the policy itself."),
        Flashcard(front="What language is Rego?", back="Open Policy Agent\'s declarative logic language. Powerful (unification, recursion). Steeper learning curve than CEL or YAML patterns. Used outside K8s too — Terraform, microservice authz, etc."),
        Flashcard(front="Both produce PolicyReports — why does that matter?", back="Standard format means downstream tools (Falco, dashboards, SIEMs) consume policy results from any engine without engine-specific code."),
    ],
    quizzes=[
        Quiz(prompt="A team adopts Kyverno. They write a policy requiring every Deployment to have a <code>team</code> label. They forget to test it. The next morning, the platform team\'s in-cluster operators (which deploy as Deployments without that label) are stuck. What\'s the playbook?", answer="<strong>Immediate:</strong> add a <code>PolicyException</code> for the platform team\'s namespaces while you fix the rollout. <strong>Process fix:</strong> (1) Enforce policies in <code>Audit</code> mode first — they log violations but don\'t block. Watch the report for a few days. (2) When you have a baseline, switch to <code>Enforce</code>. (3) Always test with <code>kyverno test</code> against fixtures including platform components. (4) Review policy reports cluster-wide weekly — the report is the leading indicator of broken assumptions. The pattern \"Audit-mode → soak → Enforce-mode\" is the standard rollout for any new restrictive policy."),
        Quiz(prompt="A team\'s Gatekeeper Constraint is rejecting valid Pods with a confusing error. The Rego in the ConstraintTemplate is hard to debug. What\'s the diagnostic toolchain?", answer="<strong>(1) Rego playground (rego.openpolicy.org)</strong> — paste the rule + a test Pod input, see what evaluates. <strong>(2) <code>gator test</code></strong> — Gatekeeper\'s CLI test framework. Define expected results in YAML; <code>gator test</code> runs them locally. <strong>(3) <code>kubectl describe constraint</code></strong> — Gatekeeper writes evaluation traces here. <strong>(4) Enable Gatekeeper\'s audit mode</strong> at TRACE level: <code>--log-level=DEBUG</code>. <strong>(5) For complex rules, factor them.</strong> Rego supports composition; smaller rules are easier to debug than monolithic ones. <strong>Long-term:</strong> require unit tests for every Rego rule before merging — catch bugs before they hit a cluster. Gatekeeper\'s steep learning curve is real; teams that succeed with it invest heavily in tests + tooling."),
        Quiz(prompt="The CISO mandates: \"every production image must be cosign-signed by our CI key.\" Pick + implement the simplest correct enforcement. <strong>Click for the Kyverno solution. ▼</strong>", cyoa=True, cyoa_tag="the Kyverno solution", answer="<strong>(1) Generate the cosign keypair</strong> in CI (or use Sigstore keyless if you can). Store the public key in a ConfigMap or directly in the policy. <strong>(2) Write a Kyverno ClusterPolicy</strong>: <pre style='background:#F5EFE3;padding:6px;font-size:11px'>apiVersion: kyverno.io/v2beta1\nkind: ClusterPolicy\nspec:\n  rules:\n  - name: verify-prod-images\n    match:\n      resources:\n        kinds: [Pod]\n        namespaceSelector:\n          matchLabels: {env: prod}\n    verifyImages:\n    - imageReferences: [\"prod-registry.corp/*\"]\n      mutateDigest: true\n      attestors:\n      - entries:\n        - keys: {publicKeys: \"-----BEGIN PUBLIC KEY-----\\n...\\n-----END PUBLIC KEY-----\"}</pre> <strong>(3) Test:</strong> apply policy in Audit mode; watch report for legitimate failures (e.g., third-party images you forgot). <strong>(4) Add exceptions</strong> for known third-party images (e.g., <code>cgr.dev/chainguard</code> already-signed images via their separate keys). <strong>(5) Switch to Enforce.</strong> <strong>(6) Pipe PolicyReports into your SOC dashboard.</strong> Total time: 2 hours of YAML + a week of soak. Compare to building a custom webhook: 2 weeks of Go + ongoing maintenance. The Kyverno solution is also easier to audit — the YAML is the spec."),
    ],
    glossary=[
        GlossaryItem(name="Policy engine", definition="System for centrally managing K8s admission policies. Two main: Kyverno, OPA Gatekeeper."),
        GlossaryItem(name="Kyverno", definition="K8s-native policy engine. YAML policies. Validate/mutate/generate/cleanup/verifyImages."),
        GlossaryItem(name="OPA / Gatekeeper", definition="Open Policy Agent + its K8s integration. Uses Rego. Powerful but steeper learning curve."),
        GlossaryItem(name="ClusterPolicy / Policy", definition="Kyverno CRD. ClusterPolicy is cluster-scoped; Policy is namespace-scoped."),
        GlossaryItem(name="ConstraintTemplate", definition="Gatekeeper CRD: rule type with Rego + parameter schema."),
        GlossaryItem(name="Constraint", definition="Gatekeeper CRD: instance of a ConstraintTemplate with specific parameters."),
        GlossaryItem(name="PolicyReport", definition="CNCF-standard CRD for policy outcomes. Both engines emit. Used for audit + dashboards."),
        GlossaryItem(name="PolicyException", definition="Kyverno CRD for explicit opt-outs. Auditable, version-controlled."),
        GlossaryItem(name="verifyImages", definition="Kyverno policy that checks image signatures (cosign) at admission."),
        GlossaryItem(name="Rego", definition="OPA\'s declarative policy language. Used by Gatekeeper. Also used outside K8s."),
        GlossaryItem(name="Audit / Enforce mode", definition="Kyverno: log violations vs reject them. Standard rollout: Audit first, then Enforce."),
        GlossaryItem(name="kyverno test / gator test", definition="CLI test frameworks for the two engines. Always test policies before deploy."),
    ],
    recap_lead="Policy engines centralise admission rules as code. Kyverno (YAML) for K8s-only governance; Gatekeeper (Rego) for OPA-heavy orgs. Both emit PolicyReports for audit. Workflow: policies in git → GitOps → reports → exceptions as objects.",
    recap_next="<strong>Next — Lesson 30: Supply Chain Security.</strong> The other half of trust: are the images you\'re running what you think they are? Cosign, Sigstore, SLSA, SBOMs, attestations. Bank Vault Quarter — the trust ledger.",
)
