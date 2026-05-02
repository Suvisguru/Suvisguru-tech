from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Print shop floor: a base manifest as a master plate, three overlays as transparency sheets stacked atop labelled dev/staging/prod, output is final printed manifest.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">PRINT SHOP · KUSTOMIZE OVERLAY PRESS</text>
  <!-- Base -->
  <g transform="translate(40,55)"><rect width="120" height="120" rx="6" fill="#FFFFFF" stroke="#3F4A5E" stroke-width="1.5"/><text x="60" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">base/</text><line x1="20" y1="32" x2="100" y2="32" stroke="#9D9389" stroke-width="0.5"/><text x="20" y="46" font-size="8" fill="#5A4F45">deployment.yaml</text><text x="20" y="60" font-size="8" fill="#5A4F45">service.yaml</text><text x="20" y="74" font-size="8" fill="#5A4F45">configmap.yaml</text><text x="60" y="100" text-anchor="middle" font-size="8" font-style="italic" fill="#5A4F45">canonical manifests</text></g>
  <!-- Overlays -->
  <g transform="translate(190,40)">
    <rect width="180" height="50" rx="4" fill="#E0EEF3" stroke="#4A8FA8" stroke-width="1"/><text x="14" y="20" font-size="9" font-weight="700" fill="#3F4A5E">overlays/dev</text><text x="14" y="34" font-size="7" fill="#5A4F45">replicas: 1, image: dev-tag</text>
    <rect width="180" height="50" rx="4" fill="#FBF1D6" stroke="#8B5A00" stroke-width="1" transform="translate(0,55)"/><text x="14" y="75" font-size="9" font-weight="700" fill="#5A4F45">overlays/staging</text><text x="14" y="89" font-size="7" fill="#5A4F45">replicas: 2, env: staging</text>
    <rect width="180" height="50" rx="4" fill="#FBE8DC" stroke="#A04832" stroke-width="1" transform="translate(0,110)"/><text x="14" y="130" font-size="9" font-weight="700" fill="#A04832">overlays/prod</text><text x="14" y="144" font-size="7" fill="#5A4F45">replicas: 6, HPA, PDB</text>
  </g>
  <!-- Press -->
  <g transform="translate(400,80)"><rect width="80" height="60" rx="6" fill="#3F4A5E"/><text x="40" y="34" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">kustomize</text><text x="40" y="50" text-anchor="middle" font-size="7" fill="#FBF1D6">build</text></g>
  <line x1="490" y1="110" x2="520" y2="110" stroke="#A04832" stroke-width="2" marker-end="url(#a6)"/>
  <defs><marker id="a6" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#A04832"/></marker></defs>
  <!-- Output -->
  <g transform="translate(525,55)"><rect width="120" height="120" rx="6" fill="#E0EFE6" stroke="#3D7857" stroke-width="1.5"/><text x="60" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#3D7857">final YAML</text><text x="60" y="40" text-anchor="middle" font-size="7" fill="#5A4F45">deployment+overlay</text><text x="60" y="54" text-anchor="middle" font-size="7" fill="#5A4F45">env-specific</text><text x="60" y="68" text-anchor="middle" font-size="7" fill="#5A4F45">ready to apply</text><text x="60" y="100" text-anchor="middle" font-size="8" font-style="italic" fill="#3D7857">no templating</text></g>
  <text x="340" y="200" text-anchor="middle" font-size="11" fill="#3F4A5E" font-style="italic">Plain YAML at the bottom; transparency overlays per environment; press produces final manifest. No string interpolation, no DSL.</text>
</svg>"""

LESSON = LessonSpec(
    num="36",
    title_short="Kustomize",
    title_full="Kustomize · Overlay-Based Manifest Customisation",
    title_html="Lesson 36 — Kustomize · K-COM",
    module_eyebrow="Module 16 · Lesson 36 · application delivery starts here",
    hero_sub_html='You wrote your first Deployment YAML. Now you need <em>three</em> versions — dev, staging, prod. The naive copy-paste approach is the most expensive Ops mistake in K8s. <strong>Kustomize</strong> is the built-in, template-free answer: plain YAML at the base, environment-specific overlays on top, no Go templates, no string interpolation.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Three weeks into a project, your repo has <code>deployment-dev.yaml</code>, <code>deployment-staging.yaml</code>, <code>deployment-prod.yaml</code>. Each is 200 lines, mostly identical. A change to the readiness probe shape needs to be made in three files; a change to the image tag in three files; PR reviews are 600 lines of diff for what should be 5. Now your team adds a fourth environment. Now you have a Kustomize problem — and it has a Kustomize answer.',
    stamp_html='<strong>Kustomize</strong> takes plain Kubernetes YAML files in a <code>base/</code> + <code>overlays/{env}/</code> structure and produces final manifests via <strong>declarative patches</strong>. Built into <code>kubectl</code> as <code>kubectl apply -k</code>. <em>No templates, no string interpolation</em>. The base is real YAML; overlays are real YAML; the result is real YAML.',
    district_pin="kt-pin36",
    district_label="Print Shop — Kustomize Press",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="The duplication problem and the overlay answer",
            body_html="""    <p>Production K8s has <em>at least</em> three environments per service: dev, staging, prod. Each needs different replicas, image tags, configuration, namespaces, and so on. The naive solutions:</p>
    <ul>
      <li><strong>Copy-paste files per environment</strong> — every change is N edits; drift inevitable.</li>
      <li><strong>String templating (Helm without overlays)</strong> — fast to start, painful at scale; templating turns YAML into a custom DSL.</li>
      <li><strong>Overlay model (Kustomize)</strong> — base YAML stays plain; environment-specific YAML <em>patches</em> the base.</li>
    </ul>
    <p>Kustomize\'s big bet: most production differences between environments are small (<code>replicas: 1</code> → <code>replicas: 6</code>; <code>image: app:dev</code> → <code>image: app:v1.2</code>; namespace; a couple of env vars). Express those as patches; leave the bulk of the manifest unchanged in the base.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The directory structure",
            h2="base/ + overlays/",
            body_html="""    <p>The canonical layout:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>app/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patches.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   └── patches.yaml
    └── prod/
        ├── kustomization.yaml
        ├── patches.yaml
        └── pdb.yaml</code></pre>
    <p><code>base/kustomization.yaml</code> lists the resources in the base:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources: [deployment.yaml, service.yaml, configmap.yaml]
commonLabels:
  app: web</code></pre>
    <p><code>overlays/prod/kustomization.yaml</code> includes the base + applies patches:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: prod
resources:
  - ../../base
  - pdb.yaml             # extra resource only in prod
patches:
  - target: {kind: Deployment, name: web}
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 6
images:
  - name: app
    newTag: v1.2.0</code></pre>
    <p>Run <code>kubectl apply -k overlays/prod/</code>; Kustomize expands the manifest in memory and applies. Or <code>kustomize build overlays/prod/</code> to print the result for review.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · What Kustomize can do",
            h2="The features you actually use",
            body_html="""    <ul>
      <li><strong>Patches</strong> — JSON 6902 (path-based) or strategic-merge (YAML-shape-based). Strategic-merge is more readable; JSON patch is more precise.</li>
      <li><strong>Common labels / annotations</strong> — apply to every resource. \"<code>commonLabels: app: web, env: prod</code>\" → every resource has those labels.</li>
      <li><strong>Name prefix / suffix</strong> — \"<code>namePrefix: prod-</code>\" → every Deployment/Service/etc. is renamed prod-X. Avoids name collisions in shared namespaces.</li>
      <li><strong>Namespace</strong> — set namespace on all resources at once.</li>
      <li><strong>Image transformations</strong> — \"replace image:tag with image:v1.2 throughout.\"</li>
      <li><strong>ConfigMap / Secret generators</strong> — generate ConfigMap/Secret from files or literals; auto-suffix the name with content hash, so changes trigger Pod restart automatically (\"the rolling-update bonus\").</li>
      <li><strong>Components</strong> — reusable transformations across multiple overlays. \"Add monitoring sidecar\" as a Component; reference it from any overlay that wants it.</li>
    </ul>
    <p>What Kustomize won\'t do (and what people complain about):</p>
    <ul>
      <li><strong>Conditionals</strong> — \"if env == prod then add this.\" Kustomize\'s answer: don\'t condition; have separate overlays. Forces clarity.</li>
      <li><strong>Loops</strong> — \"for each item in list, generate a Deployment.\" No. Use a more powerful tool (Helm, jsonnet, CDK8s) if you need dynamic generation.</li>
      <li><strong>Cross-resource references in transformations</strong> — limited.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.9 · Kustomize vs Helm — when to use which",
            h2="Different tools for different problems",
            body_html="""    <p>Kustomize and Helm are not enemies. They solve different problems:</p>
    <ul>
      <li><strong>Use Kustomize when:</strong> you own the manifests; you have a few environments; you want plain YAML; you want zero templating cognitive load.</li>
      <li><strong>Use Helm when:</strong> you ship software to others (charts to the public); you need conditional logic / loops; you need versioned package distribution.</li>
      <li><strong>Use both when:</strong> Helm chart from a vendor (e.g., <code>nginx-ingress</code>) — but you want to patch its values per environment. Use Helm to render, Kustomize to overlay. Argo CD supports this combination.</li>
    </ul>
    <p>Most production teams in 2026 use Kustomize for their <em>own</em> apps and Helm for <em>vendor</em> charts. The split aligns with who owns the manifest — your code in Kustomize; their code in Helm.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The case <em>against</em> Kustomize is real for some teams: nested overlays + Components can become spaghetti. The remedy is discipline — keep overlays shallow (1-2 levels max), prefer flat structure over deep hierarchies, name patches descriptively. Done well, Kustomize repos are easy to navigate years later. Done poorly, they\'re worse than the YAML soup they replaced.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A team\'s Deployment is identical across dev/staging/prod except for image tag and replica count. They\'re considering Helm. What\'s the simpler answer?",
            options=[
                ("a) Helm chart with a values.yaml per environment", False),
                ("b) Kustomize: one base/, three overlays/ each with a small patch for replicas + image", True),
                ("c) Three separate copies of the YAML in three branches", False),
            ],
            feedback="<strong>Answer: b.</strong> For a small set of environment differences, Kustomize is the lighter-weight answer. Plain YAML, no templating cognitive load, built into kubectl. Reach for Helm when you need conditionals, loops, or are publishing a chart for others.",
        ),
    },
    before_after_before='<p>Three copies of every manifest, one per environment. Every change = three PRs (or one giant PR with three sets of identical changes). Drift between environments inevitable; \"works in staging, fails in prod\" stories common.</p>',
    before_after_after='<p>One <code>base/</code> with the canonical manifest. <code>overlays/dev|staging|prod/</code> with small patches (replicas, image, env-specific config). One change to base = applies everywhere. Drift impossible by structure.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Kustomize\'s overlay model is the simplest valid answer to multi-environment K8s manifest management. Built into kubectl since 1.14; no extra tooling needed.</p>',
    analogy_intro_html='<p>The Print Shop has a master plate (the <strong>base manifest</strong>) — the canonical version of every poster the city prints. For each district that orders posters, the operator stacks transparency sheets (<strong>overlays</strong>) on top of the master plate before running the press. \"For East District: replace the date and replicate three times.\" \"For West District: change the colour scheme.\" The master plate never changes; each district\'s overlay is small and specific. The press (the <code>kustomize build</code> command) combines plate + overlay into a final printed poster ready to put up on the wall.</p>',
    translation_rows=[
        ("Master plate", "<code>base/</code>"),
        ("Transparency overlay sheet", "<code>overlays/{env}/kustomization.yaml</code> + patches"),
        ("\"Change replica count\" instruction", "Strategic-merge or JSON patch"),
        ("\"Apply this label everywhere\" stamp", "<code>commonLabels</code>"),
        ("\"Rename to prod-X\" stamp", "<code>namePrefix</code>"),
        ("\"Use this image tag\" rule", "<code>images:</code> transformation"),
        ("Reusable overlay across districts", "<code>Component</code>"),
        ("The press combining plate + overlay", "<code>kubectl apply -k</code> / <code>kustomize build</code>"),
    ],
    analogy_stops="The analogy stops here: real K8s overlays apply via in-memory document merging — there\'s no physical layering. And ConfigMap/Secret content hashes change names automatically; that\'s a feature, not a metaphor.",
    eli5='One main poster. Different stickers for different stores. The press puts the stickers on the poster automatically.',
    eli10="Kustomize manages multi-environment K8s manifests via overlays. Plain YAML at base/, environment-specific patches at overlays/{env}/. Built into kubectl as <code>kubectl apply -k</code>. No string templating. Use it for your own apps; reach for Helm when you need loops/conditionals or are publishing charts.",
    scenarios=[
        Scenario(name="A SaaS standardising on Kustomize for in-house apps", body="One base/ per microservice, three overlays/ for dev/staging/prod. Argo CD watches the overlay paths; per-env apps automatic. Engineers contribute changes to base/; the overlay patches live forever as small env-specific docs."),
        Scenario(name="A bank using Kustomize Components for compliance", body="A <code>compliance/</code> Component adds: PSA-restricted label, NetworkPolicy default-deny, ResourceQuota, audit annotations. Every prod overlay references the Component. Compliance team owns the Component; app teams own their overlays. Single source of truth for compliance baseline."),
        Scenario(name="A startup using Helm + Kustomize", body="<code>helm template</code> renders the vendor chart (Ingress NGINX); the rendered output goes through Kustomize to add namespace + labels + monitoring sidecars. One Argo CD app per environment. Best of both worlds."),
        Scenario(name="A team that fled from copy-paste YAML", body="Started with 3 environments × 14 services = 42 nearly-identical YAML files. Migrated to Kustomize: 14 base/ directories + 3 overlay directories per service. Total YAML lines dropped 62%. Onboarding new env was a copy of an existing overlay."),
    ],
    misconceptions=[
        Misconception(myth="Kustomize is just kubectl\'s built-in version of Helm.", truth="Different model. Helm = templating; Kustomize = overlays. Helm renders strings; Kustomize patches YAML. Both produce K8s manifests, but the development experience and use cases differ."),
        Misconception(myth="You can do conditionals in Kustomize with Components.", truth="Components add transformations; they don\'t conditionally include resources based on a value. The Kustomize answer to \"if condition then resource\" is \"have a separate overlay for that case.\""),
        Misconception(myth="Kustomize can\'t handle complex apps.", truth="It can — but at scale you\'ll feel the limits (no loops/conditionals). Many large orgs use Kustomize successfully for hundreds of services. The discipline is keeping overlays shallow + flat."),
    ],
    flashcards=[
        Flashcard(front="Kustomize directory layout?", back="<code>base/</code> with canonical manifests + <code>kustomization.yaml</code> listing them. <code>overlays/{env}/</code> with environment-specific kustomization.yaml + patches."),
        Flashcard(front="kubectl apply -k vs kubectl apply -f?", back="<code>-k</code> applies a Kustomize directory (renders + applies). <code>-f</code> applies a single YAML file or directory of plain YAMLs."),
        Flashcard(front="Strategic-merge vs JSON 6902 patches?", back="Strategic-merge: YAML-shape patches; readable. JSON 6902: path-based ops (replace, add, remove); precise."),
        Flashcard(front="commonLabels?", back="Apply a label to every resource. <code>commonLabels: app: web</code> → every Deployment, Service, ConfigMap, etc., gets <code>app: web</code>."),
        Flashcard(front="namePrefix / nameSuffix?", back="Add prefix or suffix to every resource\'s metadata.name. Useful for shared-namespace deployments."),
        Flashcard(front="ConfigMap / Secret generators?", back="<code>configMapGenerator</code> in kustomization.yaml: build a ConfigMap from a file or literal; the generated name has a content hash, so changing content auto-rolls Pods."),
        Flashcard(front="Kustomize Components?", back="Reusable transformations. \"Add monitoring sidecar\" as a Component; reference from multiple overlays."),
        Flashcard(front="When NOT Kustomize?", back="When you need conditionals, loops, or are publishing a chart for others. Helm fits those cases. Mix Kustomize on top of Helm for vendor-chart customisation."),
    ],
    quizzes=[
        Quiz(prompt="A team\'s Kustomize overlay produces a different result locally vs in CI. What\'s the diagnosis?", answer="<strong>Common causes:</strong> (1) <em>Different Kustomize versions</em>. <code>kubectl</code>\'s embedded Kustomize lags the standalone <code>kustomize</code> CLI by 1-2 minor versions. Pin the version in CI: <code>kustomize/kustomize@v5.4.0</code>. (2) <em>Path resolution</em>. <code>resources: ../../base</code> works locally if the cwd matches; CI may run from a different cwd. Use absolute paths or relative paths consistent with your repo root. (3) <em>Symlinks</em>. Kustomize follows symlinks differently in some versions. Avoid symlinks. (4) <em>API server validation</em>. <code>kustomize build</code> doesn\'t validate; <code>kubectl apply --dry-run=server</code> does. The local build might pass, the apply fail. <strong>Diagnostic command:</strong> <code>kustomize build overlays/prod/ --output rendered.yaml</code> in both environments and diff the outputs."),
        Quiz(prompt="A junior engineer adds a JSON 6902 patch <code>op: replace, path: /spec/template/spec/containers/0/env/2/value</code>. The patch fails when env vars are reordered. How to make it robust?", answer="JSON 6902 patches use <em>numeric indices</em> — fragile when arrays reorder. <strong>Better:</strong> use a strategic-merge patch that targets by <em>name</em>: <pre style='background:#F5EFE3;padding:6px;font-size:11px'>spec:\n  template:\n    spec:\n      containers:\n      - name: web\n        env:\n        - name: LOG_LEVEL\n          value: debug</pre> Strategic-merge knows that lists with name-keyed items merge by name, not index. Order-independent. Always prefer strategic-merge for env vars, container ports, and other named-list items. JSON 6902 is for cases strategic-merge can\'t express (e.g., specific-index removal)."),
        Quiz(prompt="The platform team wants every prod overlay to enforce: PSA-restricted label, NetworkPolicy default-deny, ResourceQuota. <strong>Click for the Kustomize Component design. ▼</strong>", cyoa=True, cyoa_tag="the Component design", answer="<strong>(1) Create a Component</strong> at <code>components/compliance/</code>: <pre style='background:#F5EFE3;padding:6px;font-size:11px'>apiVersion: kustomize.config.k8s.io/v1alpha1\nkind: Component\nresources:\n  - networkpolicy-default-deny.yaml\n  - resourcequota.yaml\npatches:\n  - target: {kind: Namespace}\n    patch: |-\n      - op: add\n        path: /metadata/labels/pod-security.kubernetes.io~1enforce\n        value: restricted</pre> <strong>(2) Reference from prod overlays:</strong> <pre style='background:#F5EFE3;padding:6px;font-size:11px'># overlays/prod/kustomization.yaml\ncomponents:\n  - ../../components/compliance</pre> <strong>(3) Versioning:</strong> Component is in the same repo (or a separate one referenced by URL). Updates to the Component reach every prod overlay on the next sync. <strong>(4) Audit:</strong> CI check verifies every prod overlay references <code>components/compliance</code>. Missing reference = PR rejected. <strong>(5) Per-tenant overrides:</strong> if a tenant needs different ResourceQuota, they patch the Component\'s output in their overlay — explicit, auditable. <strong>Result:</strong> compliance team owns the Component once; 47 prod overlays inherit. Single source of truth."),
    ],
    glossary=[
        GlossaryItem(name="Kustomize", definition="Built-in K8s tool for overlay-based manifest customisation. <code>kubectl apply -k</code>."),
        GlossaryItem(name="Base", definition="Canonical manifests + a kustomization.yaml. The starting point for overlays."),
        GlossaryItem(name="Overlay", definition="Environment-specific kustomization.yaml referencing the base + patches."),
        GlossaryItem(name="Patch", definition="Modification to base manifests. Strategic-merge (YAML-shape) or JSON 6902 (path-based)."),
        GlossaryItem(name="Strategic-merge patch", definition="YAML-shaped patch using K8s\'s merge semantics (lists merge by name where applicable)."),
        GlossaryItem(name="JSON 6902 patch", definition="Path-based patch using RFC 6902 ops (add, remove, replace, copy, move, test)."),
        GlossaryItem(name="commonLabels / commonAnnotations", definition="Apply to every resource in a kustomization."),
        GlossaryItem(name="namePrefix / nameSuffix", definition="Add prefix or suffix to every resource\'s metadata.name."),
        GlossaryItem(name="configMapGenerator", definition="Generate a ConfigMap from files / literals. Name auto-suffixed with content hash."),
        GlossaryItem(name="Image transformation", definition="Replace image:tag throughout, declared in kustomization.yaml."),
        GlossaryItem(name="Component", definition="Reusable kustomization fragment. Apply transformations + extra resources from multiple overlays."),
        GlossaryItem(name="kustomize build", definition="Renders a kustomization to plain YAML. Used for review or piping to other tools."),
    ],
    recap_lead="Kustomize manages multi-environment K8s manifests via overlays — plain YAML at base/, env-specific patches at overlays/. No templating. Built into kubectl. Use for your own apps; reach for Helm when you need loops/conditionals or are publishing charts.",
    recap_next="<strong>Next — Lesson 37: Helm 3.</strong> The other major application-delivery tool. Charts, values, templates, OCI distribution, signing. Print Shop, vendor side.",
)
