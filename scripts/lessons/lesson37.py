from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Print shop vendor counter: a Helm chart presented as a stamped envelope, Chart.yaml + values.yaml + templates/ visible inside, OCI registry icon next to it.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">PRINT SHOP · HELM CHART COUNTER</text>
  <!-- Chart envelope -->
  <g transform="translate(40,55)"><rect width="200" height="140" rx="8" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/><text x="100" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">CHART · my-app v1.2</text><text x="100" y="36" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">Chart.yaml · charts/ · templates/</text>
    <rect x="14" y="46" width="172" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="60" font-size="8" fill="#5A4F45" font-weight="700">templates/deployment.yaml</text>
    <rect x="14" y="68" width="172" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="82" font-size="8" fill="#5A4F45" font-weight="700">templates/service.yaml</text>
    <rect x="14" y="90" width="172" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="104" font-size="8" fill="#5A4F45" font-weight="700">templates/ingress.yaml</text>
    <rect x="14" y="112" width="172" height="20" rx="2" fill="#5A9F7A"/><text x="20" y="126" font-size="8" fill="#FFFFFF" font-weight="700">values.yaml · defaults</text>
  </g>
  <!-- Helm install -->
  <g transform="translate(260,90)"><rect width="100" height="60" rx="6" fill="#A04832"/><text x="50" y="30" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">helm install</text><text x="50" y="46" text-anchor="middle" font-size="8" fill="#FBE8DC">--values prod.yaml</text></g>
  <line x1="370" y1="120" x2="400" y2="120" stroke="#A04832" stroke-width="2" marker-end="url(#a7)"/>
  <defs><marker id="a7" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#A04832"/></marker></defs>
  <!-- Cluster -->
  <g transform="translate(405,55)"><rect width="120" height="140" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/><text x="60" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">CLUSTER</text>
    <rect x="10" y="30" width="100" height="20" rx="2" fill="#5A9F7A"/><text x="60" y="44" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">Deployment</text>
    <rect x="10" y="54" width="100" height="20" rx="2" fill="#5A9F7A"/><text x="60" y="68" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">Service</text>
    <rect x="10" y="78" width="100" height="20" rx="2" fill="#5A9F7A"/><text x="60" y="92" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">Ingress</text>
    <rect x="10" y="102" width="100" height="20" rx="2" fill="#FBF1D6"/><text x="60" y="116" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">Release: my-app v1.2</text>
  </g>
  <!-- OCI registry -->
  <g transform="translate(540,55)"><rect width="100" height="140" rx="6" fill="#E0EEF3" stroke="#4A8FA8" stroke-width="1.5"/><text x="50" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">OCI Registry</text><text x="50" y="38" text-anchor="middle" font-size="7" fill="#5A4F45">helm push my-app:1.2</text><rect x="10" y="48" width="80" height="22" rx="2" fill="#FBE8DC"/><text x="50" y="62" text-anchor="middle" font-size="7" fill="#A04832" font-weight="700">cosign signed</text><rect x="10" y="74" width="80" height="22" rx="2" fill="#FBF1D6"/><text x="50" y="88" text-anchor="middle" font-size="7" fill="#5A4F45" font-weight="700">SBOM</text><text x="50" y="120" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">like image, like chart</text></g>
</svg>"""

LESSON = LessonSpec(
    num="37",
    title_short="Helm 3",
    title_full="Helm 3 · Charts, Values, Hooks, OCI",
    title_html="Lesson 37 — Helm 3 · K-COM",
    module_eyebrow="Module 16 · Lesson 37 · the package manager for K8s",
    hero_sub_html='Helm 3 is the de-facto K8s package manager. A <strong>chart</strong> is a templated bundle of K8s manifests + a values schema + lifecycle hooks. Charts are versioned, distributed via OCI registries, and signed/verified just like container images. The reason every vendor ships their software as a Helm chart.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='You need to deploy a third-party operator: Postgres, Kafka, Argo CD, cert-manager. Each has 30+ K8s objects: Deployments, StatefulSets, CRDs, RBAC, NetworkPolicies. The vendor publishes a Helm chart. <strong>You install with one command</strong>. Without Helm, you\'d be hand-curating 30 YAML files, hoping you\'ve copied the latest config, dealing with version drift on upgrade. Every K8s vendor publishes a chart for a reason: it\'s the standard package format.',
    stamp_html='A Helm <strong>chart</strong> = templates + values schema + Chart.yaml. <code>helm install</code> renders the templates with values, applies to the cluster, records a <strong>release</strong> in a Secret. <code>helm upgrade</code> applies a new chart version + values diff. Charts are distributed via <strong>OCI registries</strong> (same as images). Sign + verify charts with <strong>cosign</strong>. The dominant pattern: Kustomize for your own apps; Helm for vendor software.',
    district_pin="kt-pin36",
    district_label="Print Shop — Helm Chart Counter",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why a package manager",
            body_html="""    <p>The Linux world has APT/YUM/DNF. The container world has registries. The K8s app world has <strong>Helm</strong>. The need is the same: bundle related files, version them, publish them, install with one command, upgrade safely.</p>
    <p>A K8s app is N manifests. Some are CRDs that must apply before others. Some have inter-references (Service references Deployment selector labels). Some need cluster-wide RBAC; some need namespace-scoped RBAC. Hand-managing this for vendor software (Postgres-Operator, cert-manager, Argo CD, etc.) was the original ops pain Helm solved.</p>
    <p>Helm 3 (released 2019) removed the controversial Tiller server component from Helm 2. Today, Helm runs entirely client-side: rendering templates locally, calling the K8s API directly. <em>Releases</em> are tracked in K8s Secrets in the install namespace.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The chart structure",
            h2="What\'s in a chart",
            body_html="""    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>my-app/
├── Chart.yaml          # name, version, dependencies
├── values.yaml         # default values
├── values.schema.json  # JSON-schema for values
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl    # template helpers
│   └── NOTES.txt       # post-install message
├── charts/             # vendored sub-charts
└── crds/               # CRDs (installed first, never templated)</code></pre>
    <p>Templates use Go templating with Helm helpers:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
      - name: web
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: {{ .Values.service.port }}</code></pre>
    <p>The <code>{{ }}</code> markers are Go templates; <code>.Values</code> is the user-provided values; <code>.Chart</code> is metadata; <code>include</code> calls a named template from <code>_helpers.tpl</code>. <code>helm install -f my-values.yaml</code> overrides the default <code>values.yaml</code>.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Lifecycle: install, upgrade, rollback, hooks",
            h2="Operations on a release",
            body_html="""    <p>Each chart installation is a <strong>release</strong>. Releases are namespaced; the same chart can be installed multiple times in different namespaces. Operations:</p>
    <ul>
      <li><code>helm install &lt;name&gt; &lt;chart&gt;</code> — render templates, apply, record release in a Secret.</li>
      <li><code>helm upgrade &lt;name&gt; &lt;chart&gt; --values new.yaml</code> — render with new values, diff, apply changes.</li>
      <li><code>helm rollback &lt;name&gt; &lt;revision&gt;</code> — re-apply a previous revision\'s manifests.</li>
      <li><code>helm uninstall &lt;name&gt;</code> — delete all resources from the release.</li>
      <li><code>helm list</code>, <code>helm status</code>, <code>helm history</code> — inspect releases.</li>
    </ul>
    <p><strong>Hooks</strong> let charts run lifecycle scripts:</p>
    <ul>
      <li><code>pre-install</code> / <code>post-install</code> — run before/after the install. Common: database migration jobs.</li>
      <li><code>pre-upgrade</code> / <code>post-upgrade</code> — run on upgrade.</li>
      <li><code>pre-delete</code> / <code>post-delete</code> — run on uninstall.</li>
      <li><code>pre-rollback</code> / <code>post-rollback</code> — run on rollback.</li>
    </ul>
    <p>Hooks are regular K8s resources (usually Jobs) annotated with <code>helm.sh/hook</code>. The chart includes them; Helm runs them at the right phase.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · OCI distribution + chart signing",
            h2="The 2026 distribution model",
            body_html="""    <p>Pre-2022, Helm charts were distributed via <strong>chart repositories</strong> — HTTP servers serving an <code>index.yaml</code>. It worked but was a parallel infrastructure to container registries.</p>
    <p>Helm 3.8+ supports <strong>OCI registries</strong> as first-class chart sources. <code>helm push my-chart:1.2 oci://registry.corp/charts</code>. Charts live alongside container images. Same auth, same vulnerability scanning, same retention policies. Almost every vendor in 2026 ships charts via OCI.</p>
    <p><strong>Chart signing</strong> via cosign:</p>
    <ul>
      <li><code>cosign sign &lt;chart-oci-ref&gt;</code> — sign a chart in an OCI registry.</li>
      <li><code>helm install --verify ...</code> with <code>cosign-policy</code> — verify before install.</li>
    </ul>
    <p>Combined with Sigstore + admission verification (Lesson 30), the chain is: vendor signs chart in OCI; consumer\'s Helm verifies signature on install; the rendered manifests are themselves run only if the cluster\'s admission policies pass. Three layers of trust.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The K8s ecosystem largely standardised on Helm + OCI by 2024. Argo CD\'s <code>helm-charts</code> source type, Flux\'s <code>HelmChart</code> CRD, and most CI tools support it natively. New vendors publishing K8s software in 2026 default to OCI-distributed Helm charts; the index.yaml-based distribution is legacy.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team installs <code>cert-manager</code> via Helm. They later need to roll back to a previous version. What records the install state Helm uses for rollback?",
            options=[
                ("a) A file on the engineer\'s laptop", False),
                ("b) A Kubernetes Secret in the release namespace, named <code>sh.helm.release.v1.cert-manager.v1</code> etc.", True),
                ("c) An external Helm server", False),
            ],
            feedback="<strong>Answer: b.</strong> Helm 3 stores release state as Secrets in the release namespace. Each revision is a separate Secret. <code>helm history</code> reads them; <code>helm rollback</code> picks an old revision and re-applies.",
        ),
    },
    before_after_before='<p>Hand-deploy 30 manifests for vendor software, hope you got every CRD right, lose track of versions, fight on every upgrade. Custom hooks for migrations done as ad-hoc Jobs you remember to apply. \"Where\'s the latest install procedure?\" lives in tribal memory or out-of-date Confluence.</p>',
    before_after_after='<p>One <code>helm install</code>; release tracked in a Secret; <code>helm upgrade</code> handles version-to-version migration; hooks orchestrate DB migrations; charts are signed; OCI registry distributes them; CI can auto-verify signatures before install. The vendor\'s install procedure is the chart.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Helm 3 + OCI is the K8s software distribution standard. Every major vendor ships charts via OCI in 2026; index.yaml repositories are legacy.</p>',
    analogy_intro_html='<p>Next door to the Kustomize press is the Helm chart counter. Vendors arrive with <strong>sealed envelopes</strong> (charts) — each containing a complete poster set ready to print, plus a parameter sheet (values.yaml) the customer fills in. The press operator runs the envelope through the press once (<code>helm install</code>), customising for the specific district\'s parameter sheet. The shop logs the install in a ledger (the release Secret) so they can roll back if needed. Vendors keep their envelopes in a sealed-envelope warehouse (OCI registry) with notarised stamps (cosign) the press can verify before opening.</p>',
    translation_rows=[
        ("Sealed envelope from a vendor", "Helm chart"),
        ("Parameter sheet customer fills in", "<code>values.yaml</code>"),
        ("Run envelope through press once", "<code>helm install</code>"),
        ("Run again with different parameters", "<code>helm upgrade</code>"),
        ("Press log entry per run", "Release Secret"),
        ("\"Roll back to last entry\"", "<code>helm rollback</code>"),
        ("Pre-print prep stage", "<code>pre-install</code> hook"),
        ("Sealed-envelope warehouse", "OCI registry"),
        ("Notarised stamp on envelope", "Cosign chart signature"),
    ],
    analogy_stops="The analogy stops here: real Helm renders Go templates with values, including conditional branches and loops. Charts can have sub-charts (dependencies). It\'s much more programmable than \"poster + parameter sheet.\"",
    eli5='Vendors give you a recipe with blanks (chart). You fill in the blanks (values). The chef makes your dish (helm install).',
    eli10="A Helm <strong>chart</strong> = Go-templated K8s manifests + values schema + Chart.yaml + lifecycle hooks. <code>helm install</code> renders the templates with user-provided values, applies the result, records a <strong>release</strong> as a Secret. <code>helm upgrade</code> diffs and applies new versions; <code>helm rollback</code> reverts. Charts are distributed via OCI registries (alongside images), signed via cosign. Use Helm for vendor software; Kustomize for your own apps.",
    scenarios=[
        Scenario(name="A SaaS using Helm + Helmfile for vendor software", body="Argo CD installs internal apps via Kustomize. Vendor software (cert-manager, Argo CD itself, Prometheus, Grafana) installed via Helm. Helmfile orchestrates multiple chart installs declaratively. Pinning chart versions in git; OCI registry hosts internal mirror of public charts."),
        Scenario(name="A bank running cosign-verified Helm installs", body="Internal Helm OCI registry. Charts signed by CI via cosign keyless. Cluster admission policy: chart pulls only allowed from internal registry. Verified install ensures supply-chain integrity end-to-end."),
        Scenario(name="A vendor publishing their software as a chart", body="Maintain Chart.yaml with semver. CI runs <code>helm lint</code> + tests on every commit. <code>helm package</code> + <code>helm push</code> to OCI on tag. Documentation references chart version. Customers <code>helm install vendor/their-app --version X.Y.Z</code> and they have the latest tested release."),
        Scenario(name="A team using hooks for safe schema migrations", body="Chart includes a <code>pre-upgrade</code> Job that runs database migration. <code>post-upgrade</code> Job warms the cache. Failing migration aborts the upgrade; broken state is recoverable via <code>helm rollback</code>. The hooks bind release lifecycle to actual application state."),
    ],
    misconceptions=[
        Misconception(myth="Helm 3 still uses Tiller.", truth="Tiller was removed in Helm 3. Modern Helm is purely client-side; release state is in Secrets in your namespace."),
        Misconception(myth="A Helm chart is just YAML with templates.", truth="It\'s also a versioned package, with a defined values schema (values.schema.json), lifecycle hooks, optional sub-charts, and a release-tracking model. Closer to a Linux package than a templated YAML."),
        Misconception(myth="Helm and Kustomize are competing solutions you must pick between.", truth="They solve different problems. Use Helm for distributed/vendor packages; Kustomize for in-house environment differentiation. Most teams use both — Helm for cert-manager, Kustomize for their own services."),
    ],
    flashcards=[
        Flashcard(front="Chart anatomy?", back="<code>Chart.yaml</code> (metadata), <code>values.yaml</code> (default values), <code>values.schema.json</code> (JSON-schema for values), <code>templates/</code> (Go templates), <code>charts/</code> (sub-charts), <code>crds/</code> (CRDs installed first, never templated)."),
        Flashcard(front="Helm 3 release state?", back="Stored in K8s Secrets in the release namespace, named <code>sh.helm.release.v1.&lt;name&gt;.v&lt;rev&gt;</code>. <code>helm history</code> reads them."),
        Flashcard(front="Hook phases?", back="<code>pre-install</code>, <code>post-install</code>, <code>pre-upgrade</code>, <code>post-upgrade</code>, <code>pre-delete</code>, <code>post-delete</code>, <code>pre-rollback</code>, <code>post-rollback</code>. Annotated with <code>helm.sh/hook</code> on regular K8s resources (usually Jobs)."),
        Flashcard(front="OCI distribution?", back="Helm 3.8+ pushes/pulls charts to OCI registries (Docker Hub, Harbor, ECR, GAR). Same auth as images. <code>helm push my-chart oci://registry/charts</code>."),
        Flashcard(front="Chart signing?", back="<code>cosign sign &lt;chart-oci-ref&gt;</code> signs in OCI. <code>helm install --verify</code> with cosign policy verifies before install."),
        Flashcard(front="Helm vs Kustomize?", back="Helm: templates + values + lifecycle + distribution. Best for vendor software. Kustomize: overlays + plain YAML. Best for own apps. Most teams use both."),
        Flashcard(front="What is Helmfile?", back="Tool for declaratively managing multiple Helm releases in one file. Useful for installing many charts (cert-manager + Prometheus + Grafana + ...) in one go."),
        Flashcard(front="What\'s a sub-chart?", back="A chart depended on by another chart. Listed in <code>Chart.yaml dependencies</code>; vendored under <code>charts/</code>. Used to compose: e.g., a Postgres-Operator chart depending on a cert-manager chart."),
    ],
    quizzes=[
        Quiz(prompt="A team\'s <code>helm upgrade</code> fails halfway: some resources updated, some didn\'t. What\'s the recovery path?", answer="<strong>Step 1:</strong> <code>helm history &lt;release&gt;</code> — see the failed revision and the previous good one. <strong>Step 2:</strong> <code>helm rollback &lt;release&gt; &lt;previous-revision&gt;</code> — re-apply the previous version\'s manifests. Helm reconciles the cluster state to the previous revision. <strong>Step 3:</strong> diagnose why the upgrade failed (often: hook timeout, CRD schema mismatch, immutable field change). <strong>Step 4:</strong> fix the chart or values; <code>helm upgrade</code> again. <strong>Important:</strong> hooks that ran before the failure are NOT undone by rollback (e.g., a pre-upgrade migration that already ran). Plan migrations to be reversible (down-migrations), or accept some manual cleanup. <strong>Production hygiene:</strong> always test upgrades in staging first; <code>helm upgrade --atomic</code> auto-rollbacks on failure (good for non-stateful charts; risky for stateful ones)."),
        Quiz(prompt="A vendor\'s Helm chart has a values schema. The team wants to enforce that production never sets <code>insecure: true</code>. What\'s the best mechanism?", answer="<strong>Three layers, in order:</strong> (1) <strong>values.schema.json</strong> in the chart can express \"<code>insecure must be false</code>\" — but the vendor controls this, not you. (2) <strong>Helm values overlay process</strong> — your CI pipeline merges base + env-specific values, validates against your <em>policy</em>, fails if production overrides set <code>insecure: true</code>. <code>helm template + kubeconform + custom checks</code>. (3) <strong>Cluster-side admission</strong> — Kyverno or VAP rule that rejects rendered manifests with insecure-related fields. The first two prevent the bad config; the third stops it even if it slipped through. Defense in depth."),
        Quiz(prompt="The platform team wants to mirror public Helm charts to an internal OCI registry. <strong>Click for the design. ▼</strong>", cyoa=True, cyoa_tag="the design", answer="<strong>(1) Internal OCI registry</strong> — Harbor, ECR, GAR, etc. Already exists for container images. <strong>(2) Mirror process</strong> — daily CronJob or CI scheduled task: <code>helm pull external-repo/cert-manager --version 1.13 --untar=false</code>; <code>helm push cert-manager-1.13.tgz oci://internal-registry/charts</code>. Track which versions are mirrored. <strong>(3) Vulnerability scanning</strong> — Trivy / Grype scan the chart\'s rendered manifests for image references; alert on CVEs. <strong>(4) Signing on mirror</strong> — re-sign with internal cosign key after mirroring; cluster admission verifies internal signature. <strong>(5) Internal index</strong> — for discovery, expose <code>oci://internal-registry/charts</code> as an Argo CD / Flux source. <strong>(6) Air-gapped support</strong> — for clusters without internet, the internal registry is the only path; configuration ensures Helm never reaches public registries. <strong>Result:</strong> single source of truth for charts, vulnerability oversight, supply-chain control. Marginal cost: ~3 hours of CI per week. Marginal benefit: full control of what enters the cluster."),
    ],
    glossary=[
        GlossaryItem(name="Helm 3", definition="K8s package manager. Client-side only (no Tiller). Installs charts as releases."),
        GlossaryItem(name="Chart", definition="Versioned bundle of K8s manifests + values schema + lifecycle hooks. The Helm package format."),
        GlossaryItem(name="Release", definition="A specific install of a chart in a namespace. Tracked as a Secret in that namespace."),
        GlossaryItem(name="Values", definition="User-provided parameters for a chart. <code>values.yaml</code> defaults; <code>-f</code> overrides."),
        GlossaryItem(name="values.schema.json", definition="JSON schema validating user-provided values."),
        GlossaryItem(name="Hook", definition="K8s resource (usually a Job) annotated with a phase. Runs at install/upgrade/delete/rollback boundaries."),
        GlossaryItem(name="Sub-chart / dependency", definition="Chart depended on by another chart. Listed in Chart.yaml; vendored under charts/."),
        GlossaryItem(name="OCI distribution", definition="Helm 3.8+ supports pushing/pulling charts to OCI registries."),
        GlossaryItem(name="Chart signing", definition="Sign charts with cosign in OCI; verify on install."),
        GlossaryItem(name="helm template", definition="Render templates locally without applying. Useful for piping to other tools (Kustomize, kubectl, Argo CD)."),
        GlossaryItem(name="helm upgrade --atomic", definition="If upgrade fails, automatically rollback. Safe for stateless; risky for stateful with hooks."),
        GlossaryItem(name="Helmfile", definition="Tool for declaring multiple Helm releases in one file."),
    ],
    recap_lead="A chart = templated manifests + values + hooks + Chart.yaml. helm install / upgrade / rollback are the operations. Releases are Secrets. OCI distribution is the modern default. Sign with cosign. Use Helm for vendor; Kustomize for in-house.",
    recap_next="<strong>Next — Lesson 38: GitOps with Argo CD.</strong> Module 17 begins — the GitOps half of application delivery. Argo CD makes \"git is the source of truth\" mechanical: it watches your repo and reconciles the cluster.",
)
