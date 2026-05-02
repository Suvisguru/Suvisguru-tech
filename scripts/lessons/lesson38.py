from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Public library reading room: Argo CD librarian fetching books from a git shelf, holding an Application card, comparing the cluster's current shelf with the desired one and reconciling.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">PUBLIC LIBRARY · ARGO CD READING ROOM</text>
  <!-- Git shelf -->
  <g transform="translate(40,55)"><rect width="140" height="120" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/><text x="70" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">GIT REPOSITORY</text><text x="70" y="34" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">desired state</text>
    <rect x="14" y="44" width="112" height="18" rx="2" fill="#FBF1D6"/><text x="20" y="58" font-size="8" fill="#5A4F45" font-weight="700">manifests/</text>
    <rect x="14" y="64" width="112" height="18" rx="2" fill="#FBF1D6"/><text x="20" y="78" font-size="8" fill="#5A4F45" font-weight="700">helm/</text>
    <rect x="14" y="84" width="112" height="18" rx="2" fill="#FBF1D6"/><text x="20" y="98" font-size="8" fill="#5A4F45" font-weight="700">kustomize/</text></g>
  <!-- Argo CD -->
  <g transform="translate(200,55)"><rect width="140" height="120" rx="6" fill="#A04832" stroke="#1B1814" stroke-width="2"/><text x="70" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">ARGO CD</text><text x="70" y="34" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">controller + UI</text>
    <rect x="14" y="44" width="112" height="20" rx="2" fill="#FBE8DC"/><text x="20" y="58" font-size="8" fill="#A04832" font-weight="700">watch git</text>
    <rect x="14" y="66" width="112" height="20" rx="2" fill="#FBE8DC"/><text x="20" y="80" font-size="8" fill="#A04832" font-weight="700">diff vs cluster</text>
    <rect x="14" y="88" width="112" height="20" rx="2" fill="#FBE8DC"/><text x="20" y="102" font-size="8" fill="#A04832" font-weight="700">sync (apply)</text></g>
  <!-- Cluster -->
  <g transform="translate(360,55)"><rect width="140" height="120" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/><text x="70" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">CLUSTER</text><text x="70" y="34" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">live state</text>
    <rect x="14" y="44" width="112" height="18" rx="2" fill="#5A9F7A"/><text x="20" y="58" font-size="8" fill="#FFFFFF" font-weight="700">Deployment ✓</text>
    <rect x="14" y="64" width="112" height="18" rx="2" fill="#5A9F7A"/><text x="20" y="78" font-size="8" fill="#FFFFFF" font-weight="700">Service ✓</text>
    <rect x="14" y="84" width="112" height="18" rx="2" fill="#FBE8DC"/><text x="20" y="98" font-size="8" fill="#A04832" font-weight="700">drift detected</text></g>
  <!-- App CRD -->
  <g transform="translate(520,55)"><rect width="120" height="120" rx="6" fill="#FBF1D6" stroke="#8B5A00" stroke-width="1.5"/><text x="60" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">Application CRD</text>
    <text x="60" y="40" text-anchor="middle" font-size="8" fill="#5A4F45">source: git repo</text>
    <text x="60" y="54" text-anchor="middle" font-size="8" fill="#5A4F45">path: overlays/prod</text>
    <text x="60" y="68" text-anchor="middle" font-size="8" fill="#5A4F45">dest: cluster + ns</text>
    <text x="60" y="82" text-anchor="middle" font-size="8" fill="#5A4F45">syncPolicy: auto</text>
    <text x="60" y="100" text-anchor="middle" font-size="7" fill="#8B5A00" font-style="italic">one app per env</text></g>
</svg>"""

LESSON = LessonSpec(
    num="38",
    title_short="Argo CD",
    title_full="GitOps with Argo CD · Application CRD, Sync, Drift Detection",
    title_html="Lesson 38 — GitOps with Argo CD · K-COM",
    module_eyebrow="Module 17 · Lesson 38 · git is the source of truth",
    hero_sub_html='\"<strong>Git is the source of truth</strong>\" sounds easy until you realise: who runs <code>kubectl apply</code>? When the cluster drifts, who notices? Who handles \"the manifest in git was bumped — is the cluster updated?\" <strong>Argo CD</strong> automates this loop. It watches a git repo, reconciles the cluster to match, and pages you when reality diverges from intent.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Three engineers each made changes via <code>kubectl edit</code> over two weeks. Nobody updated the manifests in git. Cluster state and git state are now divergent. New deployments overwrite hand-tweaked configs; nobody remembers what was changed or why. <em>This is GitOps drift, and it\'s the original sin of pre-Argo CD K8s.</em> Argo CD watches git, applies it, and screams when somebody else touches the cluster.',
    stamp_html='Argo CD is a controller that watches a git repo + reconciles the cluster to match. Define an <strong>Application</strong> CRD pointing at a git path; Argo CD syncs (auto or manual). Drift detection is built in — if someone <code>kubectl edit</code>s a managed resource, Argo CD shows it as <em>OutOfSync</em>. Pair with <strong>Argo CD Image Updater</strong> for image-bump automation; <strong>App-of-Apps</strong> for managing many Apps at scale.',
    district_pin="kt-pin06",
    district_label="Public Library — Argo CD Reading Room",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why GitOps",
            body_html="""    <p>Pre-GitOps deployment models: <em>imperative push</em>. Engineer (or CI) runs <code>kubectl apply</code>; cluster state changes; nothing tracks the change. Many failure modes:</p>
    <ul>
      <li>Drift — someone <code>kubectl edit</code>s, cluster ≠ git.</li>
      <li>Lost changes — git is updated; nobody applied; cluster still old.</li>
      <li>No audit — what\'s in production right now? Hope your last apply was the truth.</li>
      <li>Hard to roll back — <code>git revert</code> doesn\'t reach the cluster automatically.</li>
    </ul>
    <p>GitOps inverts the model: <em>git is the source of truth; the cluster pulls</em>. A controller (Argo CD) watches git; whenever git changes, the controller applies. Whenever the cluster drifts, the controller notices + alerts (and optionally re-applies).</p>
    <p>The four GitOps principles (OpenGitOps spec): <strong>declarative</strong>, <strong>versioned + immutable</strong>, <strong>pulled automatically</strong>, <strong>continuously reconciled</strong>. Argo CD implements all four.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The Application CRD",
            h2="Argo CD\'s primary unit",
            body_html="""    <p>An <strong>Application</strong> is one tracked deployment unit. Define it once; Argo CD reconciles forever.</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/web-app
    targetRevision: main
    path: overlays/prod
    # OR for Helm:
    # chart: web-app
    # repoURL: oci://registry.corp/charts
    # targetRevision: 1.2.0
    # helm: { values: |- ... }
  destination:
    server: https://kubernetes.default.svc
    namespace: web-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions: [CreateNamespace=true, ServerSideApply=true]</code></pre>
    <p>Source can be plain manifests, Kustomize, Helm chart, Helm chart from OCI, or even a custom plugin. Destination is a cluster + namespace. <code>syncPolicy.automated</code>: auto-sync on git change, auto-prune deleted resources, auto-heal drift.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Sync, drift, and self-healing",
            h2="What Argo CD actually does",
            body_html="""    <p>Three states an Application can be in:</p>
    <ul>
      <li><strong>Synced</strong> — cluster matches git.</li>
      <li><strong>OutOfSync</strong> — cluster differs from git (because git updated, or someone hand-edited).</li>
      <li><strong>Unknown</strong> — Argo CD can\'t reach git or the cluster.</li>
    </ul>
    <p>Two health states layered on top:</p>
    <ul>
      <li><strong>Healthy</strong> — resources are running as expected (Pods ready, etc.).</li>
      <li><strong>Degraded</strong> — applied but something\'s wrong (CrashLoopBackOff, etc.).</li>
    </ul>
    <p>The Argo CD UI shows a colour-coded tree of resources: green Synced+Healthy, yellow Synced+Progressing, red Degraded. One glance per env.</p>
    <p><strong>Self-healing</strong>: if <code>selfHeal: true</code>, Argo CD re-applies whenever drift is detected. Engineer who <code>kubectl edit</code>s gets reverted within seconds. Hard discipline; common in mature shops.</p>
    <p><strong>Sync waves</strong> + <strong>hooks</strong>: order resource application via <code>argocd.argoproj.io/sync-wave: 0/1/2</code> annotations; run pre-sync / post-sync Jobs as hooks. Used for: install CRDs first, then operator, then operator instances.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · App-of-Apps and ApplicationSet",
            h2="Managing many Applications at scale",
            body_html="""    <p>One Application per microservice × per environment = 50 Applications quickly. Two patterns to manage at scale:</p>
    <ul>
      <li><strong>App-of-Apps</strong> — one parent Application points at a git path containing many child Application YAMLs. Argo CD syncs the parent; the parent\'s sync creates/updates the children. Bootstrap in one apply.</li>
      <li><strong>ApplicationSet</strong> — modern alternative. A CRD that generates Applications from a template + a set of inputs. Inputs can be: a list, a set of git directories matching a glob, a set of clusters in Argo CD, even external sources. \"For every directory under <code>apps/</code>, generate an Application targeting that directory.\" Eliminates boilerplate Application YAML.</li>
    </ul>
    <p>ApplicationSet generators in production:</p>
    <ul>
      <li><code>list</code> — explicit list of values.</li>
      <li><code>git</code> — one Application per matching git path.</li>
      <li><code>cluster</code> — one Application per registered cluster (multi-cluster GitOps).</li>
      <li><code>matrix</code> — combinatorial: every Service × every cluster.</li>
      <li><code>pull-request</code> — generate Application per open PR (preview environments!).</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The PR-based ApplicationSet generator is one of the underrated GitOps wins. Open a PR; Argo CD spins up an isolated namespace with the PR\'s manifests; QA tests; merge → namespace destroyed. Preview environments without bespoke tooling. Combined with Karpenter, the cost is just per-PR Pod time.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team\'s Argo CD Application is set to <code>selfHeal: true</code>. An engineer runs <code>kubectl edit deployment</code> to manually scale replicas during an incident. What happens?",
            options=[
                ("a) The change persists permanently", False),
                ("b) Within seconds, Argo CD detects drift, reverts the change to match git, and the manual edit is lost", True),
                ("c) Argo CD locks the engineer out of the deployment", False),
            ],
            feedback="<strong>Answer: b.</strong> selfHeal aggressively reverts drift. <strong>Implication for incidents:</strong> if you need an emergency hand-edit, either disable selfHeal temporarily, sync from a hotfix branch, or set <code>argocd.argoproj.io/sync-options: ApplyOutOfSyncOnly=true</code> for the relevant resource. Don\'t fight selfHeal — work with it.",
        ),
    },
    before_after_before='<p>CI runs <code>kubectl apply</code> from the build pipeline. Sometimes someone <code>kubectl edit</code>s. Drift accumulates. Engineers go to the cluster console to verify what\'s deployed; sometimes they\'re wrong. Rollbacks involve replaying old git commits through CI. \"What\'s in production?\" is a question, not an answer.</p>',
    before_after_after='<p>Argo CD watches git, syncs continuously. UI shows every cluster\'s state at a glance. Drift is impossible (selfHeal reverts it). Rollback = <code>git revert</code> + auto-sync. Audit log is the git log. \"What\'s in production?\" = \"the latest commit on the prod branch.\"</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">GitOps via Argo CD turned K8s deployment from \"a script you ran somewhere\" into \"a continuous reconciliation loop.\" The pre-GitOps days look medieval.</p>',
    analogy_intro_html='<p>The Public Library has a special <strong>Argo CD reading room</strong>. Every cluster is represented by a shelf. Each shelf has a librarian (Argo CD controller) who consults a master catalogue (the git repo) and ensures the shelf matches the catalogue exactly. If a visitor sneaks in and rearranges the books (<code>kubectl edit</code>), the librarian notices instantly and either flags it (notification) or restores order (selfHeal). The catalogue is the truth; the shelf reflects the catalogue. To change the shelf, you change the catalogue (commit to git); the librarian propagates within seconds.</p>',
    translation_rows=[
        ("Master catalogue", "Git repository"),
        ("Library shelf", "Cluster state"),
        ("Librarian", "Argo CD controller"),
        ("\"This shelf must match this section of the catalogue\"", "<code>Application</code> CRD"),
        ("\"Match exactly, no extra books\"", "<code>prune: true</code>"),
        ("\"Restore order if disturbed\"", "<code>selfHeal: true</code>"),
        ("\"Build a card for every section automatically\"", "<code>ApplicationSet</code>"),
        ("\"Open a temporary shelf for every new chapter draft\"", "PR-based ApplicationSet generator"),
        ("\"Every shelf in every branch\"", "Multi-cluster GitOps via cluster generator"),
    ],
    analogy_stops="The analogy stops here: Argo CD also handles complex resource ordering (sync waves, hooks), partial drift (some resources OutOfSync, some Synced), and multi-source apps. The librarian metaphor undersells the precision.",
    eli5='Robot librarian. The plan is in a notebook (git). Every minute, the robot checks the shelf. If wrong, it puts the right books back. If you write in the notebook, the robot updates the shelf.',
    eli10="Argo CD is a GitOps controller. Define an <code>Application</code> CRD pointing at a git path; Argo CD reconciles the cluster to match. Three sync states (Synced/OutOfSync/Unknown) + two health states (Healthy/Degraded). selfHeal reverts manual drift. App-of-Apps + ApplicationSet patterns scale to many apps. PR-based ApplicationSet enables free preview environments.",
    scenarios=[
        Scenario(name="A SaaS using Argo CD as the only deployment path", body="CI builds + signs images, pushes to OCI. Engineers update Helm values or Kustomize overlays in git via PR. Argo CD auto-syncs on merge. Zero <code>kubectl apply</code> in CI; zero <code>kubectl edit</code> in production. Engineering culture: \"if it\'s not in git, it doesn\'t exist.\""),
        Scenario(name="A bank with multi-cluster GitOps", body="40 production clusters across regions. ApplicationSet with cluster generator: one Application per cluster, all from the same git path. Update once in git → all 40 clusters update on next sync. RBAC in Argo CD ensures team A can only sync apps in their projects."),
        Scenario(name="A startup with PR-based preview environments", body="ApplicationSet PR generator. Open PR → temporary namespace + Application created. <code>preview-pr-1234.dev.example.com</code> works. QA tests, designer reviews. Merge → namespace destroyed. Cost: $0.05/PR. Replaces a manual provisioning process that took 30 minutes per request."),
        Scenario(name="A team using selfHeal as a discipline tool", body="Initial pushback: \"can I still kubectl edit during incidents?\" Resolution: dedicated <code>incident</code> branch with hotfix manifests; ops engineers commit there during P0s; Argo CD syncs the hotfix branch immediately. After incident, hotfix gets cherry-picked to main. selfHeal stays on; cultural shift to \"cluster state lives in git.\""),
    ],
    misconceptions=[
        Misconception(myth="GitOps slows down deployment.", truth="It changes the deployment path, not the speed. Argo CD syncs on git push within seconds (or use <code>argocd app sync</code> for instant). The slowness people complain about is <em>discipline</em> (everything via PR), not technology."),
        Misconception(myth="Argo CD replaces CI.", truth="No. CI builds + tests + pushes images. Argo CD deploys. The boundary: CI ends with a manifest update PR; Argo CD picks up from there. Some shops pair Argo CD Image Updater (auto-bumps tags in git) with CI; that automates the handoff."),
        Misconception(myth="You need ApplicationSet for every multi-app setup.", truth="App-of-Apps is sufficient for most cases. ApplicationSet shines when generators (cluster, PR, matrix, git) replace boilerplate. Start with App-of-Apps; switch when boilerplate becomes painful."),
    ],
    flashcards=[
        Flashcard(front="What is GitOps?", back="Git is source of truth; cluster reconciles to match. Four principles: declarative, versioned, pulled, continuously reconciled. Argo CD + Flux are the implementations."),
        Flashcard(front="Argo CD Application CRD?", back="One tracked deployment unit. Source (git repo + path or Helm chart) + destination (cluster + namespace) + sync policy. Argo CD reconciles continuously."),
        Flashcard(front="Sync states?", back="Synced (cluster = git), OutOfSync (cluster ≠ git), Unknown (Argo CD can\'t reach git or cluster)."),
        Flashcard(front="Health states?", back="Healthy (resources happy), Degraded (something failing), Progressing (rolling out), Suspended (paused), Missing (not yet applied)."),
        Flashcard(front="selfHeal?", back="<code>syncPolicy.automated.selfHeal: true</code> — Argo CD reverts drift. Forces \"git is the only mutator\" discipline."),
        Flashcard(front="prune?", back="<code>syncPolicy.automated.prune: true</code> — when a resource is removed from git, Argo CD deletes it from the cluster. Without prune, deletions stay in cluster forever."),
        Flashcard(front="App-of-Apps vs ApplicationSet?", back="App-of-Apps: one parent App points at a path of child App YAMLs. ApplicationSet: a generator-based CRD that templates Applications from inputs (list, git dirs, clusters, PRs)."),
        Flashcard(front="Sync wave?", back="<code>argocd.argoproj.io/sync-wave: 0/1/2</code> annotation. Argo CD applies lower waves first. Used for ordering: CRDs (-1), operators (0), operator instances (1)."),
    ],
    quizzes=[
        Quiz(prompt="An Argo CD Application is OutOfSync. Click \"Sync\" — it stays OutOfSync. What\'s the diagnostic path?", answer="<strong>(1) Argo CD UI</strong> — click on the Application; expand the Diff view. See exactly which resources are different and what fields. <strong>(2) Common causes:</strong> (a) <em>Mutating webhook</em> (Kyverno, Istio, etc.) added a field to the live resource; git doesn\'t have it; Argo CD diffs every sync. <em>Fix:</em> add <code>argocd.argoproj.io/sync-options: IgnoreExtraneous=true</code> on the resource, or use <code>spec.ignoreDifferences</code> on the Application. (b) <em>Server-side defaults</em>. K8s API adds defaults that aren\'t in git. Same fix. (c) <em>Resource managed by another controller</em>. HPA modifies replicas; ConfigMap modified by external-secrets. Either remove from git or use ServerSideApply with field manager. <strong>(3) <code>argocd app diff &lt;name&gt;</code></strong> from CLI for scriptable output. <strong>(4) <code>argocd app sync &lt;name&gt; --force</code></strong> — force re-apply. Sometimes shakes loose stuck syncs."),
        Quiz(prompt="A team adopts Argo CD. After 2 weeks, half the engineers complain it\'s slowing them down. What\'s typically going wrong?", answer="<strong>Common problems:</strong> (1) <em>Too many manual approvals</em>. They have selfHeal off + manual sync; every PR requires explicit Argo CD sync. <em>Fix:</em> auto-sync for non-prod; manual approval only for prod. (2) <em>OutOfSync alarms</em>. Mutating webhooks cause perpetual OutOfSync. <em>Fix:</em> ignoreDifferences. (3) <em>Slow git → cluster latency</em>. Default polling is 3 min. <em>Fix:</em> webhook setup so git pushes trigger immediate refresh, latency drops to seconds. (4) <em>Engineers used to <code>kubectl edit</code></em>. selfHeal reverts; they think Argo CD is broken. <em>Fix:</em> training + cultural shift; \"kubectl edit\" becomes a hotfix-branch commit. (5) <em>Argo CD UI overwhelming</em>. 200 Applications in one project. <em>Fix:</em> AppProjects per team; filter by ownership. <strong>The cultural shift takes a quarter</strong>; once it settles, deployment velocity is higher than pre-Argo CD."),
        Quiz(prompt="The platform team wants every PR to spin up a preview environment with that PR\'s manifests. <strong>Click for the design. ▼</strong>", cyoa=True, cyoa_tag="the ApplicationSet design", answer="<strong>(1) ApplicationSet with PR generator:</strong> <pre style='background:#F5EFE3;padding:6px;font-size:11px'>apiVersion: argoproj.io/v1alpha1\nkind: ApplicationSet\nspec:\n  generators:\n  - pullRequest:\n      github:\n        owner: myorg\n        repo: web-app\n      requeueAfterSeconds: 60\n  template:\n    metadata:\n      name: 'preview-pr-{{number}}'\n    spec:\n      source:\n        repoURL: https://github.com/myorg/web-app\n        targetRevision: '{{head_sha}}'\n        path: deploy\n      destination:\n        namespace: 'pr-{{number}}'\n        server: https://kubernetes.default.svc\n      syncPolicy:\n        automated: {prune: true, selfHeal: true}\n        syncOptions: [CreateNamespace=true]</pre> <strong>(2) DNS:</strong> wildcard <code>*.pr.dev.example.com</code> → ingress controller; per-PR Ingress with hostname <code>preview-pr-1234.pr.dev.example.com</code>. <strong>(3) Cleanup:</strong> when PR is closed/merged, the generator removes the Application; namespace is deleted (prune). <strong>(4) Cost control:</strong> Karpenter scales nodes for active PRs only; cluster autoscaler returns nodes when PRs close. <strong>(5) Required permissions:</strong> Argo CD needs GitHub credentials with repo:read; AppProject permissions to create namespaces. <strong>Result:</strong> PR is opened → 90 seconds → <code>preview-pr-1234.pr.dev.example.com</code> works. PR is merged → 60 seconds → namespace gone. Total ops cost: zero per PR. This is the GitOps preview-environment pattern that replaced custom provisioning systems across the industry."),
    ],
    glossary=[
        GlossaryItem(name="GitOps", definition="Pattern: git is source of truth; cluster reconciles to match. Four principles in OpenGitOps spec."),
        GlossaryItem(name="Argo CD", definition="GitOps controller. CRD-driven. Watches git, reconciles cluster. CNCF graduated."),
        GlossaryItem(name="Application (CRD)", definition="One Argo CD-managed deployment unit. Source + destination + sync policy."),
        GlossaryItem(name="AppProject", definition="Argo CD scoping unit. Limits source repos, destinations, RBAC for a set of Applications."),
        GlossaryItem(name="Sync", definition="Apply git state to cluster. Manual (<code>argocd app sync</code>) or automated."),
        GlossaryItem(name="prune", definition="Delete cluster resources removed from git. <code>syncPolicy.automated.prune: true</code>."),
        GlossaryItem(name="selfHeal", definition="Re-apply when drift detected. <code>syncPolicy.automated.selfHeal: true</code>."),
        GlossaryItem(name="App-of-Apps", definition="Pattern: parent Application syncs child Applications from a git path. Bootstrap many apps in one apply."),
        GlossaryItem(name="ApplicationSet", definition="Generator-based CRD producing Applications from inputs (list, git dirs, clusters, PRs, matrix)."),
        GlossaryItem(name="PR generator", definition="ApplicationSet generator: one Application per open PR. Enables preview environments."),
        GlossaryItem(name="Sync wave", definition="<code>argocd.argoproj.io/sync-wave</code> annotation. Order resource application."),
        GlossaryItem(name="Image Updater", definition="Argo CD companion. Watches OCI registries; updates image tags in git on new versions."),
    ],
    recap_lead="Argo CD is a GitOps controller: declare Applications pointing at git, the controller reconciles continuously. selfHeal + prune make git the only mutator. App-of-Apps + ApplicationSet scale to many apps + clusters. PR-based ApplicationSet gives free preview environments.",
    recap_next="<strong>Next — Lesson 39: GitOps with Flux CD.</strong> The other major GitOps tool. Same goal, different design — controllers + CRDs per concern (sources, kustomizations, helm releases). Public Library, Flux wing.",
)
