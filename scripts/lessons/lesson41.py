from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Permit office advanced wing: a CRD blueprint with OpenAPI schema sections, CEL validation panel, conversion webhook drawer, and storage-version annotation.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">PERMIT OFFICE · ADVANCED CRD WING</text>
  <g transform="translate(40,55)"><rect width="200" height="140" rx="6" fill="#FFFFFF" stroke="#3F4A5E" stroke-width="1.5"/><text x="100" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">CustomResourceDefinition</text>
    <rect x="14" y="32" width="172" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="46" font-size="8" fill="#5A4F45" font-weight="700">group: example.com</text>
    <rect x="14" y="56" width="172" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="70" font-size="8" fill="#5A4F45" font-weight="700">versions: v1, v2</text>
    <rect x="14" y="80" width="172" height="20" rx="2" fill="#E0EEF3"/><text x="20" y="94" font-size="8" fill="#3F4A5E" font-weight="700">openAPIv3 schema</text>
    <rect x="14" y="104" width="172" height="20" rx="2" fill="#E0EFE6"/><text x="20" y="118" font-size="8" fill="#3D7857" font-weight="700">x-kubernetes-validations CEL</text>
  </g>
  <g transform="translate(260,55)"><rect width="160" height="60" rx="6" fill="#A04832"/><text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">conversion webhook</text><text x="80" y="36" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">v1 ⇄ v2</text><text x="80" y="50" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">on read &amp; write</text></g>
  <g transform="translate(260,125)"><rect width="160" height="60" rx="6" fill="#5A9F7A"/><text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">storage version</text><text x="80" y="36" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">v1 stored in etcd</text><text x="80" y="50" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">v2 served on read</text></g>
  <g transform="translate(440,55)"><rect width="200" height="140" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/><text x="100" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">CR INSTANCES</text>
    <rect x="14" y="32" width="172" height="22" rx="2" fill="#FBE8DC"/><text x="20" y="46" font-size="8" fill="#A04832" font-weight="700">prod-db (apiVersion: v2)</text>
    <rect x="14" y="58" width="172" height="22" rx="2" fill="#E0EFE6"/><text x="20" y="72" font-size="8" fill="#3D7857" font-weight="700">staging-db (v2)</text>
    <rect x="14" y="84" width="172" height="22" rx="2" fill="#FBF1D6"/><text x="20" y="98" font-size="8" fill="#8B5A00" font-weight="700">dev-db (v1)</text>
    <text x="100" y="124" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">stored as v1; served as v2</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="41",
    title_short="CRDs deep dive",
    title_full="CRDs Deep Dive · Schema, CEL, Conversion Webhooks",
    title_html="Lesson 41 — CRDs Deep Dive · K-COM",
    module_eyebrow="Module 18 · Lesson 41 · the K8s extension story in detail",
    hero_sub_html='Lesson 14 introduced CRDs as \"how K8s gets new APIs.\" That was the user view. This lesson is the <em>builder</em> view: writing the CRD schema, validating with <strong>CEL</strong>, evolving versions safely with <strong>conversion webhooks</strong>, and the lifecycle of a published K8s extension.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='You ship a CRD <code>v1alpha1</code> with a schema. A year later, you need to evolve to <code>v1</code>: rename a field, restructure spec, add validation. Naive approach: edit the CRD YAML in place. <em>Existing CRs in etcd still match the old schema</em>. Some fields are silently dropped; some validation now fails on previously-valid CRs; users see strange errors. The right approach: <strong>multiple versions + a conversion webhook + storage version migration</strong>. This lesson is that machinery.',
    stamp_html='A CRD has a name, group, versions, scope, and (per version) an OpenAPI v3 schema. Add <strong>CEL validation</strong> via <code>x-kubernetes-validations</code>. To evolve schemas safely, define multiple <code>versions</code> with one as <code>storage</code> + a <strong>conversion webhook</strong> that translates between them on read/write. <strong>Status subresource</strong> separates user spec from controller writes; <strong>scale subresource</strong> enables HPA on custom kinds.',
    district_pin="kt-pin14",
    district_label="Permit Office — Advanced CRD Wing",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="CRD anatomy",
            body_html="""    <p>A CustomResourceDefinition has these top-level fields:</p>
    <ul>
      <li><code>group</code>, <code>names</code>, <code>scope</code> — namespace identity. <code>group: cert-manager.io</code>, <code>kind: Certificate</code>, <code>listKind: CertificateList</code>, <code>singular: certificate</code>, <code>plural: certificates</code>, <code>scope: Namespaced</code> or <code>Cluster</code>.</li>
      <li><code>versions</code> — list of versions. Each has <code>name</code> (v1alpha1, v1beta1, v1), <code>served</code> (visible to clients), <code>storage</code> (exactly one), and a <code>schema</code>.</li>
      <li><code>conversion</code> — strategy for converting between versions. <code>None</code> (versions identical) or <code>Webhook</code> (call out to your conversion webhook).</li>
    </ul>
    <p>The schema is OpenAPI v3 — same as standard K8s schemas. Add <code>x-kubernetes-validations</code> for CEL rules; <code>x-kubernetes-list-type: map</code> + <code>map-keys</code> for proper merge semantics; <code>x-kubernetes-int-or-string</code> for fields that accept either.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · CEL validation",
            h2="In-CRD validation rules",
            body_html="""    <p>Pre-CEL, validating CRD fields beyond schema constraints required a <em>validating admission webhook</em> — a Pod the API server called for every CR write. Latency, fail-policy decisions, deploy ordering pain.</p>
    <p>CEL validation in CRD schema (GA in K8s 1.29) lets you add rules in the CRD itself:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>spec:
  versions:
  - name: v1
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              replicas: {type: integer, minimum: 1}
              maxReplicas: {type: integer}
            x-kubernetes-validations:
            - rule: "self.maxReplicas >= self.replicas"
              message: "maxReplicas must be ≥ replicas"
            - rule: "self.maxReplicas &lt;= 100"
              message: "maxReplicas cannot exceed 100"</code></pre>
    <p>CEL has access to <code>self</code> (the field being validated), <code>oldSelf</code> (previous value, for transition rules), and built-in functions for working with maps, lists, durations, etc. The big win: validation logic ships with the CRD; no webhook needed.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Multiple versions + conversion webhooks",
            h2="Schema evolution without breaking users",
            body_html="""    <p>You can\'t change a CRD schema in place — existing stored CRs would become invalid. Instead: <strong>add a new version</strong> alongside the old, and a <strong>conversion webhook</strong> that translates between them.</p>
    <p>The flow:</p>
    <ol>
      <li>CRD has <code>v1alpha1</code> served + storage. CRs are stored as v1alpha1 in etcd.</li>
      <li>You add <code>v1</code> with the new shape. Set <code>conversion</code> to <code>Webhook</code> pointing at your conversion service.</li>
      <li>Now CRD has v1alpha1 + v1, both served, v1alpha1 still storage.</li>
      <li>Conversion webhook converts v1alpha1 → v1 on read (when client requests v1), v1 → v1alpha1 on write (storage version).</li>
      <li>Bump <code>storage: true</code> to v1. Now writes are v1; existing v1alpha1-stored CRs are converted on read.</li>
      <li>Run <code>kubectl get</code> on every CR to force a rewrite (or use <code>storage migration</code> mechanism). All CRs now stored as v1.</li>
      <li>Drop v1alpha1 from served. (Or remove via deprecated marker first.)</li>
    </ol>
    <p>The conversion webhook is a small HTTPS service (Pod + Service) responding to <code>POST /convert</code> with the converted object. Most operator frameworks (Kubebuilder, Operator SDK) generate the webhook scaffolding for you.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Subresources, printer columns, and the lifecycle",
            h2="Polish that matters in practice",
            body_html="""    <p>Three CRD features that polish the user experience:</p>
    <ul>
      <li><strong><code>status</code> subresource</strong> — separates the spec (user-managed) from the status (controller-managed). With it enabled, <code>kubectl edit</code> can\'t change status; <code>kubectl patch --subresource=status</code> can. Required for healthy reconciliation patterns.</li>
      <li><strong><code>scale</code> subresource</strong> — exposes a <code>/scale</code> endpoint compatible with HPA. With it enabled, <code>kubectl scale myresource --replicas=5</code> works. HPA can target your CRD.</li>
      <li><strong>Additional printer columns</strong> — <code>kubectl get mykind</code> defaults to NAME + AGE. Add columns: <code>READY</code>, <code>VERSION</code>, <code>STATUS</code>. JSONPath into the spec/status. Massive UX improvement.</li>
    </ul>
    <p>Lifecycle markers:</p>
    <ul>
      <li><strong>deprecated</strong> — mark a version <code>deprecated: true</code> with a <code>deprecationWarning</code>. K8s logs warnings on every API call to that version.</li>
      <li><strong>removal</strong> — drop the version from <code>versions</code>; K8s 410 Gones any client request for it. Make sure no stored CRs are at this version first (run a storage migration).</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The K8s API conventions for versions: <code>v1alpha1</code> = experimental, may break, never default. <code>v1beta1</code> = closer to stable, may still break. <code>v1</code> = stable, won\'t break. Most operators ship many alpha versions before they stabilise. Don\'t depend on alpha CRDs in production unless you control the codebase. Storage version skew (clients on v1, storage on v1alpha2) is a real source of subtle bugs; pin client + cluster + CRD versions deliberately.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A team adds CEL validation <code>self.maxReplicas >= self.replicas</code> to their CRD. They also have an existing CR with <code>replicas: 5, maxReplicas: 3</code>. What happens?",
            options=[
                ("a) The CRD upgrade fails — existing data violates the new validation", False),
                ("b) The upgrade succeeds. The existing CR is grandfathered (CEL applies on writes). The next time someone edits this CR, the validation will reject it until fixed.", True),
                ("c) K8s deletes the invalid CR", False),
            ],
            feedback="<strong>Answer: b.</strong> CEL validates on admission (create / update). Existing data isn\'t retroactively validated. Tighten cautiously — communicate first; consider a one-time audit script to find existing violators.",
        ),
    },
    before_after_before='<p>Schema evolution = pain. \"Just edit the CRD\" silently broke existing CRs. Validation logic lived in webhooks (extra Pods, latency, fail-policy decisions). status subresource not enabled — controllers and users fought over the same fields. <code>kubectl get mykind</code> showed only NAME + AGE; you parsed JSON to see anything useful.</p>',
    before_after_after='<p>CEL validation in the CRD itself — no webhook. Multiple versions + conversion webhook for schema evolution. status subresource separates spec from status. Printer columns make <code>kubectl get</code> useful. Operator framework (Kubebuilder, Operator SDK) generates most of this for you.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">CEL\'s GA in 1.29 was the most consequential CRD change in years. Most validating webhooks for CRDs can now be deleted.</p>',
    analogy_intro_html='<p>Back at the Permit Office, the advanced wing handles custom permit forms (CRDs). New form designs need an <strong>OpenAPI schema</strong> describing every field. Validation rules can be inline (<strong>CEL</strong> annotations on the form) or run by a third-party clerk (validating webhook). When the form design changes, the office keeps both versions for a while — old applications stay in their original shape; a <strong>conversion clerk</strong> (webhook) translates between versions on the fly. Eventually old versions are deprecated and removed once nobody uses them.</p>',
    translation_rows=[
        ("New permit form design", "<code>CustomResourceDefinition</code>"),
        ("Form fields with required types", "<code>openAPIV3Schema</code>"),
        ("Inline validation rules", "<code>x-kubernetes-validations</code> CEL"),
        ("Existing applications kept on old form", "Stored CRs at older version"),
        ("Conversion clerk translating between forms", "Conversion webhook"),
        ("\"Form v1 is the storage version\"", "<code>storage: true</code> on a CRD version"),
        ("Status fields the office writes", "<code>status</code> subresource"),
        ("\"Scale up by amount\" stamp", "<code>scale</code> subresource"),
        ("Printed columns on the office board", "<code>additionalPrinterColumns</code>"),
        ("\"This form is being phased out\"", "<code>deprecated: true</code> on a version"),
    ],
    analogy_stops="The analogy stops here: real conversion webhooks are HTTP/JSON services with retry semantics + TLS auth. The \"clerk\" abstraction undersells the operational care needed.",
    eli5='You write down what your custom form looks like. Rules say what fields are allowed. When you change the form, you keep the old version too and translate between them.',
    eli10="A CRD has versions, schemas, and optional conversion webhooks. CEL validation (GA 1.29) puts validation rules in the CRD itself, replacing many webhooks. Schema evolution: add new version, set up conversion webhook, migrate storage version, drop old version. Subresources (status, scale) and printer columns polish the user experience. Operator frameworks (Kubebuilder, Operator SDK) generate most of the boilerplate.",
    scenarios=[
        Scenario(name="A SaaS migrating an Operator from v1alpha1 to v1", body="Used Kubebuilder to scaffold v1 alongside v1alpha1. Conversion webhook generated. Tested in dev; ran storage migration via <code>kubectl get crd-name -o json | kubectl apply -f -</code> on every CR (forces rewrite at storage version). Marked v1alpha1 deprecated for two minor versions; removed in the third. Zero user-visible breakage."),
        Scenario(name="A bank using CEL for cross-field validation", body="Custom <code>SecurityPolicy</code> CRD. CEL rule: \"if scope=Cluster, then issuer must be present.\" Pre-CEL, this needed a webhook. With CEL, it\'s 4 lines in the CRD. One less Pod to operate; one less point of failure."),
        Scenario(name="A team using subresource scale with HPA", body="<code>WorkerPool</code> custom resource has <code>spec.replicas</code> + <code>status.readyReplicas</code>. Scale subresource enabled. HPA points at the WorkerPool with <code>scaleTargetRef</code>. Standard K8s autoscaling on a custom kind."),
        Scenario(name="A startup with rich printer columns", body="<code>kubectl get certificates</code> shows NAME, READY, SECRET, EXPIRES, AGE. Configured via <code>additionalPrinterColumns</code> on the cert-manager CRD. Saves engineers from <code>kubectl describe</code> for routine status checks."),
    ],
    misconceptions=[
        Misconception(myth="CEL replaces all admission webhooks.", truth="CEL replaces simple per-object validation. Cross-resource validation (\"this CR refers to that ConfigMap; check it exists\") still needs webhook or K8s\'s <code>x-kubernetes-validations</code> with <code>variables</code> referencing other resources (limited). Complex generation/mutation needs Kyverno or webhooks."),
        Misconception(myth="A CRD can have multiple storage versions.", truth="Exactly one version is <code>storage: true</code>. The rest are served versions converted on read/write. Switching storage version requires a migration step (rewrite all CRs) before dropping the old version."),
        Misconception(myth="Conversion webhooks only run during schema migrations.", truth="They run on <em>every</em> read or write of a non-storage version. If a controller still uses v1alpha1 but storage is v1, every reconcile triggers conversion. Latency-sensitive; design webhooks accordingly."),
    ],
    flashcards=[
        Flashcard(front="CRD top-level fields?", back="<code>group</code>, <code>names</code>, <code>scope</code> (Namespaced/Cluster), <code>versions</code> (list with served/storage/schema each), <code>conversion</code> (None or Webhook)."),
        Flashcard(front="What is x-kubernetes-validations?", back="CEL-based validation rules in CRD schema. K8s 1.29 GA. Replaces many validating admission webhooks."),
        Flashcard(front="status subresource?", back="Separates user-managed spec from controller-managed status. Enabled per-version. Required for healthy reconciliation."),
        Flashcard(front="scale subresource?", back="Exposes <code>/scale</code> endpoint. Lets HPA + <code>kubectl scale</code> work on the CRD."),
        Flashcard(front="Multiple versions in a CRD?", back="Define multiple in <code>versions</code> array. Exactly one <code>storage: true</code>. Conversion webhook translates between served versions on read/write."),
        Flashcard(front="Conversion webhook?", back="HTTPS service that converts CR between versions. Called on read (if client requests non-storage version) and on write (if write isn\'t storage version)."),
        Flashcard(front="Storage version migration?", back="To switch storage version safely: add new version with conversion; flip <code>storage: true</code> to new; rewrite all CRs (forces conversion to new storage); drop old version once safe."),
        Flashcard(front="additionalPrinterColumns?", back="Defines columns for <code>kubectl get</code>. JSONPath expressions into the CR. Big UX improvement."),
    ],
    quizzes=[
        Quiz(prompt="A team adds a new optional field to their CRD\'s schema. Stored CRs don\'t have the field. What happens to those CRs on the next reconcile?", answer="<strong>Nothing breaks.</strong> Adding optional fields is backward-compatible: stored CRs without the field are read as having the zero value (empty string, false, missing object). Reconcilers should treat missing fields as defaults. <strong>What\'s NOT backward-compatible:</strong> (1) renaming a field (write old, read new = lost data). (2) Changing a field\'s type (string → int = read fails). (3) Adding a new <em>required</em> field (existing CRs become invalid on next write). For these, you need a new version + conversion webhook. <strong>The K8s API conventions doc</strong> has the full compatibility matrix; consult before any non-additive change."),
        Quiz(prompt="A team\'s conversion webhook is timing out on every reconcile. The Pod logs show 200ms latency per call. What\'s wrong?", answer="<strong>Diagnosis path:</strong> (1) <em>Webhook implementation</em>. Conversion should be near-zero latency — pure data transformation. If your webhook hits a database, that\'s the problem. (2) <em>Network</em>. Webhook Pod scheduled on a node far from kube-apiserver. Use anti-affinity to keep replicas spread; consider DaemonSet pattern. (3) <em>TLS handshake overhead</em>. Use HTTP/2 keep-alives. (4) <em>Storage version mismatch</em>. If your storage is v1alpha1 but every read converts to v1, every reconcile pays the conversion cost. Run storage migration to flip storage to the more-used version. <strong>Long-term fix:</strong> minimise non-storage-version reads; eventually drop the old version. Conversion webhooks are a transitional tool, not a permanent layer."),
        Quiz(prompt="The CRD owner wants to deprecate v1alpha1 (used by 3 customers) in favor of v1. <strong>Click for the deprecation playbook. ▼</strong>", cyoa=True, cyoa_tag="the deprecation playbook", answer="<strong>(1) Mark deprecated.</strong> Set <code>deprecated: true</code> + <code>deprecationWarning: \"use v1 instead; v1alpha1 will be removed in N releases\"</code> on the v1alpha1 version. K8s emits warnings on every v1alpha1 API call; users see them in <code>kubectl</code> output. <strong>(2) Document the migration.</strong> Field-by-field mapping; example before/after manifests; conversion-webhook explanation. <strong>(3) Reach out to the 3 customers.</strong> Direct communication beats banners. Help them with the migration. <strong>(4) Wait at least 2 minor releases.</strong> K8s convention: at least 6 months between deprecation and removal. <strong>(5) Storage migration.</strong> If v1alpha1 was the storage version, change to v1; rewrite all CRs (<code>kubectl get crd-name -o json | kubectl apply -f -</code>). Verify no CR is stored at v1alpha1: <code>kubectl api-resources --api-group=example.com</code>. <strong>(6) Remove v1alpha1.</strong> Drop from <code>versions</code>. Old API calls return 410 Gone. <strong>(7) Optional: chart helper.</strong> Ship a Helm post-install hook or a CLI tool that scans for v1alpha1 usage and emits warnings. <strong>The whole sequence is months</strong>; deprecation is a marathon, not a sprint."),
    ],
    glossary=[
        GlossaryItem(name="CRD", definition="CustomResourceDefinition. Cluster-scoped object defining a new API kind."),
        GlossaryItem(name="CR", definition="Custom Resource. An instance of a CRD. \"<code>kubectl get certificates</code>\" lists CRs."),
        GlossaryItem(name="OpenAPI v3 schema", definition="Standard schema language for CRD field validation."),
        GlossaryItem(name="x-kubernetes-validations (CEL)", definition="K8s 1.29 GA. CEL-based validation rules in CRD schema."),
        GlossaryItem(name="status subresource", definition="Separates user-managed spec from controller-managed status. Required for clean reconciliation."),
        GlossaryItem(name="scale subresource", definition="Exposes /scale endpoint. Enables HPA + <code>kubectl scale</code> on the CRD."),
        GlossaryItem(name="Conversion webhook", definition="HTTPS service called by kube-apiserver to convert CRs between versions."),
        GlossaryItem(name="Storage version", definition="The version CRs are stored as in etcd. Exactly one per CRD; converted on read for other versions."),
        GlossaryItem(name="Storage version migration", definition="Process of rewriting all CRs to a new storage version after flipping it."),
        GlossaryItem(name="additionalPrinterColumns", definition="CRD field defining columns for <code>kubectl get</code>."),
        GlossaryItem(name="deprecated / deprecationWarning", definition="CRD version-level fields signalling phase-out. K8s emits warnings."),
        GlossaryItem(name="Kubebuilder / Operator SDK", definition="Frameworks for generating CRD + controller boilerplate. Lesson 42."),
    ],
    recap_lead="A CRD has schema (OpenAPI v3 + CEL validation), versions (one storage + others served), conversion webhook for evolution, status/scale subresources, and printer columns. CEL replaces most validating webhooks. Operator frameworks generate the scaffolding.",
    recap_next="<strong>Next — Lesson 42: Operators with Kubebuilder.</strong> The CRD is the data; the operator is the brain. Controller-runtime, Kubebuilder, OLM. NEW: Workshop district.",
)
