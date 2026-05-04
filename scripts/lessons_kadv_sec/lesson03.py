"""K-ADV-SEC S3 — Admission policy architecture (Kyverno + Gatekeeper hybrid)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Admission policy hybrid — mutating + validating + PolicyReport.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Checkpoint Gates · K-Citadel — three desks: mutate · validate · report</text>
  <rect x="40" y="70" width="200" height="100" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Kyverno (mutating)</text>
  <text x="140" y="108" text-anchor="middle" font-size="9" fill="#1F2433">YAML rules + JMESPath</text>
  <text x="140" y="124" text-anchor="middle" font-size="9" fill="#1F2433">defaults + patches</text>
  <text x="140" y="148" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">K8s-native ergonomics</text>
  <rect x="260" y="70" width="200" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="360" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Gatekeeper (validating)</text>
  <text x="360" y="108" text-anchor="middle" font-size="9" fill="#1F2433">OPA / Rego</text>
  <text x="360" y="124" text-anchor="middle" font-size="9" fill="#1F2433">formal logic rules</text>
  <text x="360" y="148" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">complex constraints</text>
  <rect x="480" y="70" width="240" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">PolicyReport CRD</text>
  <text x="600" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">unified report (Kyverno + Gatekeeper)</text>
  <text x="600" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">+ ValidatingAdmissionPolicy + CEL</text>
  <text x="600" y="148" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">policy-as-code in CI</text>
</svg>"""


LESSON = LessonSpec(
    num="03",
    title_short="admission policy",
    title_full="S3 · Admission Policy Architecture (Kyverno + Gatekeeper hybrid)",
    title_html="K-ADV-SEC S3 · Admission Policy Architecture",
    module_eyebrow="Module S3 · the Checkpoint Gates — three desks: mutate · validate · report",
    hero_sub_html='Three admission desks. <strong>Kyverno</strong>: K8s-native YAML rules + JMESPath; mutating (defaults + patches) + validating + generating; ergonomic for K8s teams. <strong>Gatekeeper</strong>: OPA / Rego; formal-logic rules; ConstraintTemplate + Constraint; complex cross-resource constraints. <strong>ValidatingAdmissionPolicy + CEL</strong> (built-in K8s 1.30+): inline rules, no webhook latency. <strong>PolicyReport CRD</strong>: unified results across all engines — one search surface for compliance. The hybrid pattern uses Kyverno for most things, Gatekeeper for the formal-logic outliers, CEL inline where webhook latency matters.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A policy you wrote last quarter blocked a critical deploy because it required a specific label format. The team can\'t deploy a fix until the policy is removed. You realise: <em>policies were enforced cluster-wide on day one without an audit / warn period</em>. Today\'s lesson: design admission policy in three lifecycle stages — audit → warn → enforce — and pick engines per use case.",
    stamp_html="<strong>Hybrid: Kyverno for K8s-native YAML rules; Gatekeeper for OPA/Rego complex logic; ValidatingAdmissionPolicy + CEL inline for hot-path validation. Always roll out policies audit → warn → enforce. PolicyReport unifies feeds.</strong>",
    district_pin="ksec-bastion03",
    district_label="Checkpoint Gates",
    sections=[
        Section(
            eyebrow="Section 1.1 · admission lifecycle",
            h2="audit → warn → enforce — never ship enforce on day one",
            body_html="""    <p>K8s admission webhooks operate in three modes per policy: <strong>audit</strong> (record violations; don\'t block), <strong>warn</strong> (return warnings to <code>kubectl</code> output; don\'t block), <strong>enforce</strong> (block the request). Roll every new policy through the lifecycle:</p>
    <ul>
      <li><strong>Audit (1-2 weeks)</strong>: deploy in audit mode; collect violations from PolicyReport / metrics; review false positives + edge cases.</li>
      <li><strong>Warn (1-2 weeks)</strong>: enable warn; teams see the rule in their <code>kubectl apply</code> output; complaints surface before they become incidents.</li>
      <li><strong>Enforce</strong>: block. Document the policy + waiver path before flipping.</li>
    </ul>
    <p>Skip steps and you ship outages. Slow rollouts catch the policy that\'s right in theory and wrong in practice.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Kyverno",
            h2="K8s-native YAML rules; mutating / validating / generating",
            body_html="""    <p><strong>Kyverno</strong> is policy-as-K8s-CRDs. You write <code>ClusterPolicy</code> / <code>Policy</code> objects with <code>match</code> selectors + <code>rules</code> using JMESPath expressions over the resource. Rule kinds:</p>
    <ul>
      <li><strong>mutate</strong>: patch the object (set defaults, add labels, inject sidecars). E.g., \"every Pod gets <code>resources.requests.cpu: 100m</code> if missing.\"</li>
      <li><strong>validate</strong>: pass/fail check (return failed message). E.g., \"every Pod must have <code>imagePullPolicy: Always</code>.\"</li>
      <li><strong>generate</strong>: create downstream resources triggered by parent (e.g., new Namespace → auto-create default NetworkPolicy + ResourceQuota).</li>
      <li><strong>verifyImages</strong>: image-signature check via Cosign / Sigstore (covered in S5).</li>
    </ul>
    <p>Kyverno wins for: K8s-shop teams; rules that are mostly K8s-resource-shaped; teams not wanting to learn Rego. Performance: webhook latency typically &lt;50ms per request.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Gatekeeper (OPA)",
            h2="ConstraintTemplate + Constraint; formal logic in Rego",
            body_html="""    <p><strong>Gatekeeper</strong> is OPA (Open Policy Agent) wrapped as a K8s admission controller. You author:</p>
    <ul>
      <li><strong>ConstraintTemplate</strong>: a CRD definition + Rego policy logic (e.g., template \"K8sRequiredLabels\" with Rego logic).</li>
      <li><strong>Constraint</strong>: an instance of the template with parameters (e.g., \"K8sRequiredLabels: required labels = [team, cost-center]; match Pods\").</li>
    </ul>
    <p>Rego shines on <strong>cross-resource logic</strong>: \"this Service can only target Pods labelled X if those Pods exist in this list of allowed namespaces — and the source Pod\'s SA must be in that list.\" Rego is a real query language; Kyverno\'s JMESPath is more limited. Gatekeeper wins for: complex correlations, formal-logic-heavy compliance, teams already invested in OPA.</p>
    <p>Trade-off: Rego is a learning curve. For a typical K8s team, 80% of policies are K8s-shape and Kyverno is faster to author; the 20% that are complex go to Gatekeeper.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · ValidatingAdmissionPolicy + CEL + PolicyReport",
            h2="Inline policy without a webhook + unified reporting",
            body_html="""    <p><strong>ValidatingAdmissionPolicy</strong> (K8s 1.30+ stable) lets you write validation rules in <strong>CEL (Common Expression Language)</strong> directly in K8s objects — <em>no webhook</em>. The apiserver evaluates them inline. <em>Major win</em>: zero webhook latency, no extra component to operate, no webhook outage risk. Use for hot-path rules where every millisecond counts (admission to a high-throughput cluster).</p>
    <p>Limits: CEL is simpler than Rego or JMESPath — no calls to external data, no cross-resource lookups within one rule. For complex needs, stick with Kyverno / Gatekeeper.</p>
    <p><strong>PolicyReport CRD</strong> (Kyverno + Gatekeeper both write to it): one cluster-wide unified report of policy results per resource. Compliance dashboards query PolicyReports; engineers see violations in one place; SIEM ingestion is uniform.</p>
    <p><strong>Hybrid pattern</strong>: 70% policies in Kyverno (ergonomic + K8s-native), 20% in Gatekeeper (complex logic), 10% in ValidatingAdmissionPolicy (hot-path latency-sensitive). Each engine reports to PolicyReport. Compliance + ops see one view.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A new policy blocks deploys in production on day one — outage. What was missed in the rollout?",
            options=[
                ("Should have used a different engine.", False),
                ("Should have run audit → warn → enforce over weeks; skipped audit / warn.", True),
                ("Should have written it in CEL.", False),
            ],
            feedback="Audit then warn then enforce. False positives surface in audit; complaints surface in warn; enforce is the last step after a real-world calibration period.",
        ),
        3: PauseCheck(
            question="A simple rule \"every Pod must have a team label\" — which engine first?",
            options=[
                ("Gatekeeper / Rego — formal logic.", False),
                ("Kyverno (K8s-native YAML; trivial JMESPath rule) or ValidatingAdmissionPolicy + CEL.", True),
                ("Custom webhook in Go.", False),
            ],
            feedback="Simple K8s-shape rules are best in Kyverno or CEL — readable, fast, and the team doesn\'t need Rego expertise. Reserve Gatekeeper for the complex logic.",
        ),
    },
    before_after_before='<p>Pre-policy clusters had documentation \"please add resource limits\" + occasional code review. Drift was constant. Compliance evidence was \"trust us\" + a sample of YAML files. Bad images, missing labels, privileged Pods all slipped through.</p>',
    before_after_after='<p>Modern admission applies policy at apiserver: every request mutated + validated; PolicyReport tracks every decision; compliance evidence is automatic + queryable; engineers see violations in <code>kubectl apply</code> output. Hybrid Kyverno + Gatekeeper + CEL covers the spectrum from K8s-shape to complex to hot-path.</p>',
    before_after_caption='<p class="ba-caption"><em>Pick the engine to fit the rule, not the other way around. And always audit before enforcing.</em></p>',
    analogy_intro_html='''<p>The Checkpoint Gates are three desks at the second wall. The first desk (<strong>mutating</strong>) hands every visitor a standard-issue helmet + name tag (defaults + labels) before they pass through. The second desk (<strong>validating</strong>) checks the visitor\'s papers against the rule book — pass or fail. A third desk (<strong>generating</strong>) emits side-effect paperwork (auto-create NetworkPolicy when a new Namespace appears).</p>
    <p>Two rule-book authors share the work. One writes in plain K8s ergonomic syntax (Kyverno YAML + JMESPath). The other writes in formal-logic ledger (Gatekeeper / Rego) for the complex rules. Both append to a single archive (<strong>PolicyReport CRD</strong>) so compliance can audit one shelf.</p>
    <p>A new rule is never enforced overnight — it goes through three phases: <strong>audit</strong> (shadow log), <strong>warn</strong> (visitors see a yellow note), <strong>enforce</strong> (visitor turned away at gate).</p>''',
    translation_rows=[
        ("Standard-issue helmet + name tag", "Kyverno mutate (defaults + labels)"),
        ("Rule-book check (pass/fail)", "Kyverno / Gatekeeper validate"),
        ("Side-effect paperwork", "Kyverno generate (auto-create resources)"),
        ("K8s-ergonomic rule book", "Kyverno YAML + JMESPath"),
        ("Formal-logic ledger", "Gatekeeper OPA / Rego"),
        ("Inline gate-check (no helper desk)", "ValidatingAdmissionPolicy + CEL"),
        ("Single audit shelf", "PolicyReport CRD"),
        ("Shadow log", "audit mode"),
        ("Yellow warning slip", "warn mode"),
        ("Gate-turn-away", "enforce mode"),
    ],
    analogy_stops="A real gate-keeper checks one document; admission webhooks evaluate every rule on every API call (potentially thousands per minute). Webhook latency adds up — keep policies tight or move to ValidatingAdmissionPolicy + CEL.",
    eli5="Three desks at the gate. The first hands you a helmet so you\'re always equipped. The second checks your papers against the rule book. The third writes paperwork for what your visit triggers. Different rule books exist for K8s-shape rules vs complex logic vs latency-sensitive rules. Your cluster does the same.",
    eli10="<strong>Three engines</strong>: Kyverno (K8s-native YAML + JMESPath; mutate/validate/generate/verifyImages), Gatekeeper (OPA + Rego; complex logic), ValidatingAdmissionPolicy + CEL (inline, no webhook, hot-path). <strong>PolicyReport CRD</strong> unifies results. <strong>Lifecycle</strong>: audit → warn → enforce, weeks each. <strong>Hybrid pattern</strong>: 70/20/10 Kyverno/Gatekeeper/CEL.",
    scenarios=[
        Scenario(
            name="Kyverno default — every Pod gets resource requests",
            body="A platform team ships a Kyverno mutate rule: every Pod with no <code>resources.requests.cpu</code> gets <code>100m</code>; no <code>requests.memory</code> gets <code>128Mi</code>. <em>Audit → warn → enforce</em> over 4 weeks. PolicyReport tracked. Cluster baseline now sane; capacity planning works.",
        ),
        Scenario(
            name="Gatekeeper formal logic — Service-to-Namespace correlation",
            body="A regulated cluster requires \"a Service\'s selector may only target Pods in a namespace listed in the Service\'s allowed-targets annotation.\" Cross-resource correlation; Kyverno\'s JMESPath struggles; Gatekeeper Rego handles it cleanly. ConstraintTemplate ships once; per-Service Constraint declares the allowed-targets list.",
        ),
        Scenario(
            name="ValidatingAdmissionPolicy + CEL hot-path",
            body="A 1000-rps internal cluster API needs every PUT to validate one field. Webhook latency would add ~30ms per request — 30 seconds of cumulative latency per second. ValidatingAdmissionPolicy + CEL evaluates inline, ~0ms. Teams adopt for the latency-sensitive policies.",
        ),
        Scenario(
            name="Outage — enforced on day one",
            body="A team enabled \"every Pod requires team label\" enforce immediately. Existing CI tooling didn\'t set the label; deploys broke cluster-wide. 90-min outage. Postmortem: every new policy walks audit → warn → enforce; the team\'s runbook now requires evidence of audit-period violation count before enforcing.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Pick one engine — Kyverno OR Gatekeeper, not both.\"",
            truth="<strong>Hybrid is the standard pattern.</strong> Kyverno for ergonomic K8s rules, Gatekeeper for complex logic, ValidatingAdmissionPolicy + CEL for hot-path. PolicyReport unifies the feeds. Forcing one engine for everything = either dumbed-down policies (Kyverno-only for complex needs) or pain (Gatekeeper for trivial rules).",
        ),
        Misconception(
            myth="\"ValidatingAdmissionPolicy + CEL is just a stripped-down Kyverno.\"",
            truth="It\'s <em>inline in the apiserver</em> — no webhook, no extra latency, no extra component to operate. For hot-path or simple rules, it\'s the right tool. CEL is more limited than JMESPath/Rego; for complex needs, Kyverno or Gatekeeper still win.",
        ),
        Misconception(
            myth="\"Audit mode is for the audit team; engineers don\'t need it.\"",
            truth="Audit mode is for <em>every team rolling out a policy</em>. It\'s the calibration phase — find false positives, edge cases, missing exemptions. Skip it and the policy that\'s right in theory ships incidents in practice.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three K8s admission engines and when to pick each?", back="<strong>Kyverno</strong>: K8s-native YAML + JMESPath, mutate/validate/generate (ergonomic, K8s-shape rules). <strong>Gatekeeper</strong>: OPA + Rego (formal-logic, cross-resource correlation). <strong>ValidatingAdmissionPolicy + CEL</strong>: inline no-webhook (hot-path latency-sensitive)."),
        Flashcard(front="Three rollout phases for a new policy?", back="<strong>Audit</strong> (record violations, don\'t block) → <strong>Warn</strong> (return warnings in kubectl output) → <strong>Enforce</strong> (block). 1-2 weeks per phase typical."),
        Flashcard(front="What does Kyverno mutate look like?", back="ClusterPolicy with <code>rules: [{name, match, mutate: {patchStrategicMerge: ...}}]</code>. Adds defaults / labels / sidecars to admission requests before persisting."),
        Flashcard(front="ConstraintTemplate vs Constraint in Gatekeeper?", back="<strong>ConstraintTemplate</strong>: defines the schema + Rego logic for a class of policy. <strong>Constraint</strong>: an instance of the template with parameters + match selector. Templates are reusable; Constraints are specific."),
        Flashcard(front="What does Kyverno generate do?", back="Auto-creates downstream resources triggered by parent. Pattern: \"new Namespace → generate default NetworkPolicy + ResourceQuota.\" Replaces manual onboarding scripts."),
        Flashcard(front="PolicyReport CRD — what\'s the win?", back="Unified results from Kyverno + Gatekeeper + (any other PolicyReport-aware engine). One CRD list to query for compliance evidence; one feed to ship to SIEM. Replaces engine-specific dashboards."),
        Flashcard(front="When use ValidatingAdmissionPolicy + CEL?", back="(1) Hot-path rules where webhook latency matters. (2) Simple rules that don\'t need cross-resource lookups. (3) Reducing webhook count for ops simplicity. (4) Avoid for complex / cross-resource — those go to Kyverno or Gatekeeper."),
        Flashcard(front="Why is Rego harder than Kyverno YAML?", back="Rego is a logic-programming language with set semantics; learning curve is real. Pays off for complex policies (cross-resource correlation, set membership, transitive checks). Don\'t use Rego for trivial \"label must exist\" — too much overhead."),
    ],
    quizzes=[
        Quiz(
            prompt="Design admission for a regulated cluster: every Pod must have resource requests + limits; certain namespaces must have NetworkPolicy + ResourceQuota; images must be from a list of registries; Service-to-Namespace targeting must be on an allow-list. Which rules go where?",
            answer="<strong>Kyverno (mutate + validate)</strong>: (a) mutate — Pods with no resource requests get sane defaults; new namespaces auto-generate default NetworkPolicy + ResourceQuota (generate rule). (b) validate — Pods MUST have resource limits (warn → enforce). <strong>Kyverno verifyImages</strong>: Cosign-verify images from approved registries (covered in S5; Kyverno-native). <strong>Gatekeeper</strong>: Service-to-Namespace allow-list (cross-resource lookup; Rego ConstraintTemplate \"AllowedServiceTargets\" with Constraint per Service group). <strong>PolicyReport</strong>: all engines write to it; compliance dashboard reads one CRD list. <strong>Rollout</strong>: audit each policy 2 weeks → warn 2 weeks → enforce; ship in waves so ops can absorb violations.",
        ),
        Quiz(
            prompt="A team wrote a Gatekeeper Rego rule. Performance is poor — admission p99 hit 800ms. Walk through diagnostic + fix.",
            answer="(1) <strong>Profile</strong>: Gatekeeper exposes Prometheus metrics — <code>opa_evaluation_duration_seconds</code>; identify which ConstraintTemplate is slow. (2) <strong>Read the Rego</strong>: common slow patterns — wildcard matches across all resources, <code>data.inventory</code> queries that scan thousands of objects, deeply nested rule recursion. (3) <strong>Tighten the match selector</strong>: scope Constraint to specific Kinds + namespaces; OPA evaluates only matching requests. (4) <strong>Index data references</strong>: pre-compute mappings via Gatekeeper Sync + use indexed lookups in Rego. (5) <strong>Move simple rules to ValidatingAdmissionPolicy + CEL</strong>: webhook eliminated; latency drops to ~0ms. (6) <strong>Final option</strong>: rewrite the policy in Kyverno if Rego complexity isn\'t actually needed for that rule.",
        ),
        Quiz(
            prompt="Leadership says: \"too many policies are slowing things down. Disable admission webhooks for the dev cluster.\" Defend keeping them on.",
            answer="\"<strong>Disabling admission in dev means dev becomes a test bed for misconfigurations that ship to prod.</strong> Three reasons admission stays on dev: (1) <strong>Catch issues early</strong>: if a Pod is missing resource requests, dev is where we want to find that, not staging or prod. (2) <strong>Train the developer feedback loop</strong>: developers who see admission warnings in dev <code>kubectl apply</code> output learn the rules. Disabling means they ship YAMLs that fail in staging — slower iteration. (3) <strong>Preserve dev / prod parity</strong>: bugs that only manifest in prod because admission caught them in dev are real bugs we shouldn\'t paper over. <strong>If admission is genuinely slow:</strong> profile the policies (which Kyverno rule, which Gatekeeper Constraint), tighten match selectors, move simple rules to CEL inline. Latency budget is a tunable; security posture should not be the variable.\"",
            cyoa=True,
            cyoa_tag="how the security architect kept dev admission on",
        ),
    ],
    glossary=[
        GlossaryItem(name="Admission webhook", definition="Pluggable extension to apiserver that mutates or validates requests after authn/authz, before persisting."),
        GlossaryItem(name="Kyverno", definition="K8s-native policy engine using ClusterPolicy / Policy CRDs with JMESPath. Mutate / validate / generate / verifyImages."),
        GlossaryItem(name="Gatekeeper", definition="OPA-based admission controller. ConstraintTemplate defines schema + Rego; Constraint is an instance."),
        GlossaryItem(name="OPA / Rego", definition="Open Policy Agent + its query language. General-purpose policy with set semantics + cross-resource logic."),
        GlossaryItem(name="ValidatingAdmissionPolicy", definition="K8s 1.30+ built-in admission via CEL — inline, no webhook, no extra component."),
        GlossaryItem(name="CEL (Common Expression Language)", definition="Google\'s expression language; used in K8s ValidatingAdmissionPolicy + many other places. Simpler than Rego."),
        GlossaryItem(name="PolicyReport CRD", definition="Cluster-wide unified report of policy decisions. Both Kyverno + Gatekeeper write to it."),
        GlossaryItem(name="audit / warn / enforce", definition="Three lifecycle modes for any new policy. Audit = log only; Warn = kubectl warning; Enforce = block."),
        GlossaryItem(name="Kyverno generate", definition="Rule kind that creates downstream resources triggered by parent (e.g., new Namespace → generate NetworkPolicy)."),
        GlossaryItem(name="ClusterPolicy / Policy", definition="Kyverno CRDs — ClusterPolicy is cluster-scoped; Policy is namespace-scoped."),
    ],
    recap_lead="Three admission engines, three roles. Kyverno for K8s-native ergonomics; Gatekeeper for formal-logic complex correlation; ValidatingAdmissionPolicy + CEL for hot-path inline. PolicyReport unifies. Audit → warn → enforce. The hybrid pattern is the answer.",
    recap_next='<strong>Next — S4: PSA Restricted + runtime detection.</strong> Pod Security Admission migration playbook (privileged → baseline → restricted); Falco / Tetragon eBPF-based runtime detection at scale; alert pipelines.',
)
