"""K-ADV-PE P4 — Argo CD ApplicationSets + OPA / Kyverno guardrails."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ApplicationSet + guardrails."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Batch-Crafting Jig · K-Workshop — fleet GitOps + policy gates</text><rect x="40" y="70" width="200" height="100" rx="10" fill="#3F4A5E"/><text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">ApplicationSet</text><text x="140" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">generators (clusters/git/list)</text><rect x="260" y="70" width="200" height="100" rx="10" fill="#5DCAA5"/><text x="360" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Per-cluster App</text><text x="360" y="108" text-anchor="middle" font-size="9" fill="#1F2433">from one chart + values</text><rect x="480" y="70" width="240" height="100" rx="10" fill="#A04832"/><text x="600" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">OPA / Kyverno guardrails</text><text x="600" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">PR + admission + sync</text></svg>"""


LESSON = LessonSpec(
    num="04", title_short="ApplicationSets + guardrails", title_full="P4 · Argo CD ApplicationSets + OPA / Kyverno Guardrails",
    title_html="K-ADV-PE P4 · ApplicationSets + Guardrails", module_eyebrow="Module P4 · Batch-Crafting Jig — fleet GitOps + policy gates",
    hero_sub_html='<strong>Argo CD ApplicationSet</strong>: CR generating Argo CD Applications from generators (clusters / git directories / list / matrix / merge). One template + N clusters = N Apps with cluster-label values. <strong>OPA / Kyverno guardrails</strong>: policy gates at three layers — PR-time (kyverno-cli / conftest in CI), admission (Kyverno / Gatekeeper webhook), Argo CD sync (PreSync hooks running policy checks). Together: fleet GitOps + uniform policy.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A new tenant\'s app deployed cluster-wide via Argo CD ApplicationSet — but nobody added their image registry to the allowlist. <em>The deploy succeeded; the Pods crashed image-pull-error across every cluster simultaneously</em>. Today\'s lesson: ApplicationSets need policy gates so fleet-wide deploys can\'t fleet-wide-fail.",
    stamp_html="<strong>ApplicationSet generates per-cluster Apps from one template; OPA + Kyverno gate at PR + admission + sync. Fleet velocity + fleet safety.</strong>",
    district_pin="kpe-bench04", district_label="Batch-Crafting Jig",
    sections=[
        Section(eyebrow="Section 1.1 · ApplicationSet generators",
            h2="Five generator kinds for fleet patterns",
            body_html="""    <p><strong>List generator</strong>: explicit list of items; one App per item.</p>
    <p><strong>Cluster generator</strong>: iterates over Argo CD-registered clusters; one App per cluster (auto-discovered).</p>
    <p><strong>Git generator</strong>: scans a Git repo directory or files; one App per directory/file.</p>
    <p><strong>Matrix generator</strong>: composes two generators (e.g., clusters × git directories).</p>
    <p><strong>Merge generator</strong>: combines generators with overlay precedence.</p>
    <p>Cluster + git generators are the fleet-GitOps default — \"every cluster gets every app declared in this directory.\""""),
        Section(eyebrow="Section 1.2 · per-cluster values",
            h2="Cluster labels feed template parameters",
            body_html="""    <p>Cluster generator surfaces cluster labels as template variables: <code>{{name}}</code>, <code>{{server}}</code>, <code>{{metadata.labels.region}}</code>. Template uses these to differentiate per-cluster (region-specific endpoints, cluster-specific replicas, env-specific values).</p>
    <p>Pattern: cluster label <code>tier=prod</code> → ApplicationSet template renders <code>replicas: 5</code>; <code>tier=dev</code> → <code>replicas: 1</code>. One ApplicationSet handles both."""),
        Section(eyebrow="Section 1.3 · policy gates at three layers",
            h2="PR-time + admission + sync",
            body_html="""    <p><strong>PR-time</strong>: <code>kyverno-cli</code> / <code>conftest</code> in CI. Block bad YAML before merge. Fast feedback for developers.</p>
    <p><strong>Admission</strong>: Kyverno / Gatekeeper webhook. Block at apiserver if PR-time gate was bypassed or new policy added.</p>
    <p><strong>Sync</strong>: Argo CD PreSync hook runs policy checks against rendered manifests; blocks deploy if violation. Catches pre-render issues + drift.</p>
    <p>Three layers because: PR-time catches early; admission catches anything that slips; sync catches policy drift at deploy time."""),
        Section(eyebrow="Section 1.4 · ApplicationSet operational patterns",
            h2="staged rollouts + sync waves + ProgressiveSync",
            body_html="""    <p><strong>Sync waves</strong>: annotation <code>argocd.argoproj.io/sync-wave: \"-1\"</code> orders resource sync (CRDs first, then operators, then Apps).</p>
    <p><strong>ProgressiveSync</strong> (alpha → beta): per-cluster rollout with health gates. Apply to dev cluster first; if healthy, apply to next; abort on first unhealthy. Replaces big-bang ApplicationSet deploy.</p>
    <p><strong>Per-environment App tier</strong>: ApplicationSet generates Apps in waves: dev → staging → prod. Combined with ProgressiveSync = safe fleet rollouts.</p>
    <p><strong>RBAC</strong>: ApplicationSet ownership separate from App. Platform team owns ApplicationSets; tenants own per-app values via Git PRs."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Best generator for \"every Argo CD-registered cluster gets this app\"?",
            options=[("List generator.", False), ("Cluster generator.", True), ("Matrix generator.", False)],
            feedback="Cluster generator iterates over registered clusters; auto-extends as new clusters register."),
        3: PauseCheck(question="Why three policy gate layers?",
            options=[("Belt and suspenders.", False), ("PR-time = fast feedback; admission = catch drift; sync = catch render-time issues.", True), ("Required by Argo CD.", False)],
            feedback="Each layer catches a different class. Three layers + uniform policy = no class slips through to prod."),
    },
    before_after_before='<p>Pre-ApplicationSet: per-cluster Argo CD Application files manually maintained. Drift across clusters; new cluster = manual file copy. Policy enforced ad-hoc.</p>',
    before_after_after='<p>ApplicationSet generates per-cluster Apps from one template; OPA + Kyverno gates at PR + admission + sync. Fleet GitOps with uniform policy.</p>',
    before_after_caption='<p class="ba-caption"><em>One template, many clusters; three policy layers; staged rollouts.</em></p>',
    analogy_intro_html='''<p>The Batch-Crafting Jig in the workshop fixtures one master template + many empty wagon frames; the master pours per-frame variations from a labels list. Three quality inspectors review at three checkpoints: at-PR, at-assembly, at-shipping.</p>''',
    translation_rows=[
        ("Master template", "ApplicationSet template"),
        ("Empty wagon frames", "Per-cluster Argo CD Apps generated"),
        ("Per-frame label", "Cluster label (tier / region / etc.)"),
        ("PR inspector", "kyverno-cli / conftest in CI"),
        ("Assembly inspector", "Admission webhook (Kyverno / Gatekeeper)"),
        ("Shipping inspector", "Argo CD PreSync hook"),
        ("Staged rollout", "ProgressiveSync (dev → staging → prod)"),
    ],
    analogy_stops="Wagon frames are physical; per-cluster Apps are CRDs. Drift detection via ProgressiveSync + Argo CD health checks.",
    eli5="One master template churns out many wagons sized per cluster. Three quality checks: at the design table, at assembly, at the loading dock.",
    eli10="<strong>ApplicationSet</strong>: 5 generators (List / Cluster / Git / Matrix / Merge); generates per-cluster Apps. <strong>Templates</strong> use cluster labels for per-cluster values. <strong>Policy gates</strong>: PR-time (kyverno-cli / conftest), admission (Kyverno / Gatekeeper), sync (PreSync hook). <strong>ProgressiveSync</strong>: staged dev → prod with health gates.",
    scenarios=[
        Scenario(name="One ApplicationSet → 30 clusters", body="Platform team\'s ApplicationSet uses Cluster generator + values from cluster labels (tier/region/env). 30 clusters auto-onboard; new cluster registration = new App appears."),
        Scenario(name="Three-layer policy catches misconfig", body="A tenant PR'd a privileged Pod. PR-time kyverno-cli flagged; PR blocked. Admission also configured; sync hook also runs. Misconfig never reaches prod."),
        Scenario(name="ProgressiveSync — bad release auto-aborted", body="ProgressiveSync waved to dev → staging; staging health failed; rollout aborted before prod. Postmortem on dev change; fix; re-deploy. Saved a fleet outage."),
        Scenario(name="Outage — image registry not allowlisted", body="ApplicationSet deployed; Pods image-pull-error fleet-wide. Postmortem: PR-time gate didn\'t check registry allowlist; added rule; re-test."),
    ],
    misconceptions=[
        Misconception(myth="\"ApplicationSet is just a Helm chart of Apps.\"", truth="ApplicationSet has structured generators (Clusters / Git / Matrix); auto-extends as inputs change. Helm-of-Apps is static; ApplicationSet is dynamic."),
        Misconception(myth="\"Admission policy alone is enough.\"", truth="Admission catches at apiserver; PR-time gives faster feedback to developers + sync hook catches render-time issues. Three layers each catch different classes."),
        Misconception(myth="\"ProgressiveSync slows deploys unacceptably.\"", truth="ProgressiveSync adds 10-30 min per wave but prevents fleet-wide outages. Cost worth paying for prod tier; dev tier can be big-bang."),
    ],
    flashcards=[
        Flashcard(front="Five ApplicationSet generators?", back="<strong>List</strong> (explicit), <strong>Cluster</strong> (registered clusters), <strong>Git</strong> (repo dirs/files), <strong>Matrix</strong> (cross of two), <strong>Merge</strong> (overlay precedence)."),
        Flashcard(front="Cluster generator output?", back="One Argo CD App per registered cluster. Cluster labels surface as template variables for per-cluster values."),
        Flashcard(front="Three policy gate layers?", back="<strong>PR-time</strong> (kyverno-cli / conftest in CI), <strong>admission</strong> (Kyverno / Gatekeeper webhook), <strong>sync</strong> (Argo CD PreSync hook). Catches drift + late additions + render-time issues."),
        Flashcard(front="Sync waves — what do they do?", back="Annotation <code>argocd.argoproj.io/sync-wave: N</code> orders resource sync. Lower N = sooner. Use for CRDs (-1), operators (0), apps (1)."),
        Flashcard(front="ProgressiveSync — what does it add?", back="Staged per-cluster rollout with health gates. Apply to dev → staging → prod; abort on first unhealthy. Replaces big-bang ApplicationSet deploy."),
        Flashcard(front="ApplicationSet RBAC pattern?", back="Platform team owns ApplicationSets; tenants own per-app values via Git PRs. ApplicationSet template + tenant values = per-cluster App."),
        Flashcard(front="Matrix generator — when use?", back="When per-cluster + per-app combinations needed (e.g., 5 clusters × 10 apps = 50 Apps). Each combination becomes one App."),
        Flashcard(front="Why is OPA conftest useful at PR-time?", back="Conftest runs Rego against any structured config (YAML / JSON / HCL); fast feedback in CI before merge; catches policy violations earlier than admission."),
    ],
    quizzes=[
        Quiz(prompt="Design fleet GitOps: 30 clusters across 3 tiers (dev / staging / prod), 20 platform apps. How does ApplicationSet structure look?",
            answer="(1) One <strong>Matrix generator</strong>: clusters × git directories. (2) <strong>Cluster generator</strong> with <code>matchLabels: {tier: dev}</code> + similar for staging + prod. (3) <strong>Git generator</strong> reads <code>apps/&lt;tier&gt;/</code> directories listing 20 platform apps. (4) <strong>Template</strong> uses cluster.labels for per-cluster values; per-tier app set differs (some apps prod-only). (5) <strong>ProgressiveSync</strong>: dev wave → staging wave → prod wave with health gates between. (6) <strong>Three policy gates</strong>: PR-time conftest in CI; admission Kyverno; PreSync hook. <em>Net</em>: 30 clusters × ~15 apps = ~450 Apps generated, all from ~20 lines of ApplicationSet."),
        Quiz(prompt="A tenant PR adds a new app; PR-time gate passes; admission rejects in dev. Why might that happen?",
            answer="Admission policies updated since CI ran or different rules in different environments. Common: dev cluster has tighter PSA Restricted than CI mock; or new Kyverno policy added between CI run + admission. Fix: (1) sync CI policy bundle with cluster\'s policy state; (2) treat admission rejection as the source of truth + retro the PR-time gate. (3) For consistency: cluster\'s Kyverno policies bundled in CI conftest container."),
        Quiz(prompt="Leadership says: \"why ProgressiveSync? Argo CD sync is fine.\" Defend.",
            answer="\"<strong>Big-bang sync to 30 clusters means a bad release breaks 30 clusters simultaneously.</strong> ProgressiveSync waves: dev → staging → prod with health gates. Bad releases catch in dev; ~5 min per wave overhead; fleet-wide outage probability drops to near-zero. <strong>Cost</strong>: 15-30 min slower fleet rollouts; the next prevented incident pays for years.\"", cyoa=True, cyoa_tag="how the platform engineer defended ProgressiveSync"),
    ],
    glossary=[
        GlossaryItem(name="ApplicationSet", definition="Argo CD CRD generating Applications from generators. Fleet GitOps."),
        GlossaryItem(name="ApplicationSet generator", definition="List / Cluster / Git / Matrix / Merge. Each produces template inputs."),
        GlossaryItem(name="ProgressiveSync", definition="Argo CD ApplicationSet feature for staged per-cluster rollouts with health gates."),
        GlossaryItem(name="Sync wave", definition="argocd.argoproj.io/sync-wave annotation ordering resource sync; lower N first."),
        GlossaryItem(name="kyverno-cli", definition="CLI for running Kyverno policies against YAML files. CI gate."),
        GlossaryItem(name="conftest", definition="OPA-based CLI running Rego against structured config. CI gate; multi-format."),
        GlossaryItem(name="PreSync hook", definition="Argo CD hook running before sync; can run policy checks against rendered manifests."),
        GlossaryItem(name="cluster generator", definition="ApplicationSet generator iterating over registered Argo CD clusters."),
    ],
    recap_lead="ApplicationSet for fleet GitOps; OPA + Kyverno gates at PR + admission + sync; ProgressiveSync for staged rollouts. Fleet velocity with fleet safety.",
    recap_next='<strong>Next — P5: Tenant onboarding + resource templates + cost controls + service catalogs.</strong>',
)
