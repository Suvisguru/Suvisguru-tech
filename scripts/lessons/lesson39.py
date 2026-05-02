from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Public library Flux wing: a row of specialised controllers — Source Controller, Kustomize Controller, Helm Controller, Notification Controller — each with its own CRD on the desk.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">PUBLIC LIBRARY · FLUX CD WING</text>
  <g transform="translate(40,55)"><rect width="140" height="120" rx="6" fill="#3F4A5E"/><text x="70" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">source-controller</text><rect x="14" y="32" width="112" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="46" font-size="8" fill="#5A4F45" font-weight="700">GitRepository</text><rect x="14" y="56" width="112" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="70" font-size="8" fill="#5A4F45" font-weight="700">HelmRepository</text><rect x="14" y="80" width="112" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="94" font-size="8" fill="#5A4F45" font-weight="700">OCIRepository</text><rect x="14" y="104" width="112" height="14" rx="2" fill="#FBF1D6"/><text x="20" y="114" font-size="7" fill="#5A4F45" font-weight="700">Bucket</text></g>
  <g transform="translate(200,55)"><rect width="140" height="120" rx="6" fill="#5A9F7A"/><text x="70" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">kustomize-controller</text><rect x="14" y="32" width="112" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="46" font-size="8" fill="#5A4F45" font-weight="700">Kustomization</text><text x="70" y="80" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">build + apply</text><text x="70" y="95" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">prune + heal</text></g>
  <g transform="translate(360,55)"><rect width="140" height="120" rx="6" fill="#A04832"/><text x="70" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">helm-controller</text><rect x="14" y="32" width="112" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="46" font-size="8" fill="#5A4F45" font-weight="700">HelmRelease</text><text x="70" y="80" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">install / upgrade</text><text x="70" y="95" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">drift detect</text></g>
  <g transform="translate(520,55)"><rect width="120" height="120" rx="6" fill="#E8B547"/><text x="60" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">notif-controller</text><rect x="14" y="32" width="92" height="20" rx="2" fill="#FBF7F0"/><text x="20" y="46" font-size="8" fill="#5A4F45" font-weight="700">Provider</text><rect x="14" y="56" width="92" height="20" rx="2" fill="#FBF7F0"/><text x="20" y="70" font-size="8" fill="#5A4F45" font-weight="700">Alert</text><text x="60" y="100" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">Slack / webhook</text></g>
</svg>"""

LESSON = LessonSpec(
    num="39",
    title_short="Flux CD",
    title_full="GitOps with Flux CD · Multi-Controller Architecture",
    title_html="Lesson 39 — GitOps with Flux CD · K-COM",
    module_eyebrow="Module 17 · Lesson 39 · the other major GitOps tool",
    hero_sub_html='<strong>Flux CD</strong> is the other major GitOps tool. Same goal as Argo CD — git as source of truth, continuous reconciliation — different architecture: <strong>multiple specialised controllers</strong> instead of one big one. Source controller fetches; Kustomize controller renders; Helm controller installs; Notification controller alerts. Each can be installed independently.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Argo CD\'s monolithic controller hits memory limits during a sync of 800 Applications. The team\'s on-call gets paged. Flux\'s answer to scale: don\'t put everything in one binary. Source-controller does git pulls; Kustomize-controller does renders; Helm-controller does Helm; each scales independently. Flux\'s architecture biases toward modularity. Argo CD\'s biases toward UI ergonomics. Both work; the choice is taste.',
    stamp_html='Flux uses <strong>specialised controllers per concern</strong>: <code>GitRepository</code> / <code>HelmRepository</code> / <code>OCIRepository</code> for sources; <code>Kustomization</code> for Kustomize-based deploys; <code>HelmRelease</code> for Helm; <code>Alert</code> + <code>Provider</code> for notifications. CLI is <code>flux</code>. CRD-only — no built-in UI. Best for: GitOps-native shops that prefer kubectl as the interface.',
    district_pin="kt-pin06",
    district_label="Public Library — Flux CD Wing",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Same goal, different architecture",
            body_html="""    <p>Flux and Argo CD share the GitOps goal but diverge architecturally. Where Argo CD ships one big controller binary + a UI, Flux ships <strong>five specialised controllers</strong>:</p>
    <ul>
      <li><strong>source-controller</strong> — fetches from sources. CRDs: <code>GitRepository</code>, <code>HelmRepository</code>, <code>HelmChart</code>, <code>OCIRepository</code>, <code>Bucket</code>.</li>
      <li><strong>kustomize-controller</strong> — renders Kustomize + applies. CRD: <code>Kustomization</code> (note: distinct from Kustomize\'s own <code>kustomization.yaml</code>).</li>
      <li><strong>helm-controller</strong> — installs Helm releases declaratively. CRD: <code>HelmRelease</code>.</li>
      <li><strong>notification-controller</strong> — sends alerts on events. CRDs: <code>Alert</code>, <code>Provider</code>, <code>Receiver</code>.</li>
      <li><strong>image-automation-controller</strong> + <strong>image-reflector-controller</strong> — automated image-tag updates in git from OCI registry events.</li>
    </ul>
    <p>Each controller is installed via the Flux Helm chart or <code>flux install</code>. They\'re independent — install only what you need. Each scales horizontally on its own.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The bootstrap flow",
            h2="\"Flux bootstrapping its own GitOps\"",
            body_html="""    <p>The classic install: <code>flux bootstrap github --owner=myorg --repository=fleet-infra --branch=main --path=clusters/prod</code>. This:</p>
    <ol>
      <li>Adds Flux\'s controller manifests to the git repo at the specified path.</li>
      <li>Installs Flux on the cluster.</li>
      <li>Sets up a <code>GitRepository</code> + <code>Kustomization</code> pointing at the same path.</li>
      <li>From then on, Flux manages itself: edit the manifests in git, Flux applies the change.</li>
    </ol>
    <p>This \"GitOps for GitOps\" pattern is part of Flux\'s ergonomic; you don\'t hand-manage Flux upgrades — they\'re a <code>flux bootstrap</code> rerun or a manifest tweak.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · The CRDs in practice",
            h2="GitRepository, Kustomization, HelmRelease",
            body_html="""    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># Source: where to fetch from
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata: {name: web-app, namespace: flux-system}
spec:
  interval: 1m
  url: https://github.com/myorg/web-app
  ref: {branch: main}
---
# Kustomization: render + apply from a source
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata: {name: web-prod, namespace: flux-system}
spec:
  interval: 5m
  path: ./overlays/prod
  prune: true
  sourceRef: {kind: GitRepository, name: web-app}
  targetNamespace: web-prod
  healthChecks:
  - {kind: Deployment, name: web, namespace: web-prod}
---
# HelmRelease: install a chart
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata: {name: cert-manager, namespace: cert-manager}
spec:
  interval: 5m
  chart:
    spec:
      chart: cert-manager
      version: 1.14.x
      sourceRef: {kind: HelmRepository, name: jetstack, namespace: flux-system}
  values: {installCRDs: true}</code></pre>
    <p>Common pattern: use Flux\'s <code>Kustomization</code> CRD to render Kustomize-style overlays from a git path; use <code>HelmRelease</code> for vendor charts. Each CRD has its own status, events, and reconcile loop.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Notification controller, image automation",
            h2="The pieces beyond sync",
            body_html="""    <p><strong>notification-controller</strong> turns Flux events into outbound alerts. Provider points at Slack/Discord/Teams/PagerDuty/generic webhook; Alert filters which events to send. \"Notify Slack on every <code>Kustomization</code> reconcile failure in production namespaces.\"</p>
    <p><strong>image-automation-controller + image-reflector-controller</strong>: automate image-tag bumps. The reflector watches an OCI registry; when a new tag matches a policy, image-automation-controller commits the tag bump back to git. Closes the loop: build → push → flux auto-bumps → flux applies. CI pushes; Flux deploys.</p>
    <p>Compared to Argo CD Image Updater, Flux\'s image automation is more flexible (commits to git, so you have a record + PR review possible) but requires more setup. Most Flux shops use it for non-critical paths and let humans bump prod via PR.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The Flux vs Argo CD choice is mostly cultural. <strong>Argo CD shines</strong>: rich UI, easier ramp-up, Application abstraction, ApplicationSet PR generator (preview envs!). <strong>Flux shines</strong>: composable, kubectl-only, more flexible source types (Bucket, OCI, generic), tighter K8s feel. The CNCF graduation paths converged in 2024 — both are stable, both are widely adopted. Pick by your team\'s preference; both work.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A Flux <code>Kustomization</code> applies but the rendered manifests have an error (missing CRD). What\'s the diagnostic command?",
            options=[
                ("a) <code>kubectl get pods -n flux-system</code>", False),
                ("b) <code>flux get kustomizations -A</code> and inspect the conditions; or <code>kubectl describe kustomization &lt;name&gt;</code> for events", True),
                ("c) Re-bootstrap Flux", False),
            ],
            feedback="<strong>Answer: b.</strong> Flux\'s diagnostics live on the CRDs themselves. <code>flux get</code> commands wrap kubectl with friendlier output. Each Kustomization\'s <code>status.conditions</code> shows the latest reconcile result with a clear error message.",
        ),
    },
    before_after_before='<p>Pre-GitOps. CI ran kubectl apply. Same problems as Argo CD\'s before — drift, lost changes, unclear truth. Bonus problem if you wanted CRD-only ops: Argo CD\'s UI was central to its value but you couldn\'t fully manage it via kubectl.</p>',
    before_after_after='<p>Flux: every concern is a CRD. <code>kubectl get gitrepositories,kustomizations,helmreleases -A</code> shows the whole picture. CI/CD purists love it. UIs (Weave GitOps, Capacitor) exist as add-ons but aren\'t required.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Argo CD vs Flux is a matter of taste. Both deliver the GitOps experience. Flux for kubectl-first shops; Argo CD for UI-first shops.</p>',
    analogy_intro_html='<p>The Public Library has a Flux wing alongside the Argo CD reading room. Same goal — keep shelves matching the catalogue — but different staffing model. Instead of one librarian doing everything, Flux has <strong>specialised desks</strong>: a fetching desk (source-controller), a Kustomize-shelving desk, a Helm-shelving desk, a notifications desk. Each desk handles its concern; they coordinate by handing off to each other. The visitor (operator) interacts with each desk via paper forms (CRDs) — there\'s no central counter — but every desk\'s status is on a public bulletin board for inspection.</p>',
    translation_rows=[
        ("Fetching desk", "<code>source-controller</code> + <code>GitRepository</code>/<code>HelmRepository</code>/<code>OCIRepository</code>"),
        ("Kustomize-shelving desk", "<code>kustomize-controller</code> + <code>Kustomization</code> CRD"),
        ("Helm-shelving desk", "<code>helm-controller</code> + <code>HelmRelease</code>"),
        ("Notifications desk", "<code>notification-controller</code> + <code>Alert</code>/<code>Provider</code>"),
        ("Image-bump assistant", "<code>image-automation-controller</code>"),
        ("Public bulletin board (status)", "CRD <code>.status</code> fields + events"),
        ("\"Self-installs from a git checkout\"", "<code>flux bootstrap</code>"),
    ],
    analogy_stops="The analogy stops here: Flux controllers are independent processes scheduled by K8s, not desks. They communicate via Kubernetes API objects, not paperwork.",
    eli5='Like Argo CD, but each job has a different worker. One fetches the books. One organises the shelves. One sends notes. They share the same plan.',
    eli10="Flux is GitOps via specialised controllers. <code>source-controller</code> handles GitRepository / HelmRepository / OCIRepository. <code>kustomize-controller</code> applies Kustomization CRDs. <code>helm-controller</code> applies HelmRelease CRDs. <code>notification-controller</code> alerts. <code>image-automation-controller</code> auto-bumps tags. CRD-only by default; UIs available as add-ons (Weave GitOps, Capacitor). Flux bootstrap installs Flux into a cluster managing itself via git.",
    scenarios=[
        Scenario(name="A SaaS using Flux with image-automation", body="CI builds + pushes signed images. image-reflector-controller watches OCI; image-automation-controller bumps tags in git on new releases. Kustomize-controller applies the bump. End-to-end: push image → 60-second reconcile → live in cluster. No manual step from build to deploy."),
        Scenario(name="A bank running multi-tenant Flux", body="Each tenant gets a namespace + a Flux Kustomization scoped to their git path. Tenant-RBAC limits which paths Flux can touch. Cluster admin owns the top-level Flux install + GitRepository CRDs; tenants own Kustomizations within their namespace. Clean tenant boundary."),
        Scenario(name="A startup using Flux for vendor charts", body="cert-manager, Argo Rollouts, Prometheus, etc., all installed via HelmRelease CRDs. <code>helm-controller</code> manages upgrades by updating the version field in git; rollback is a git revert. Less hand-tooling than Helm CLI. Reproducible across clusters."),
        Scenario(name="A team that picked Flux over Argo CD for kubectl-first culture", body="Engineering team mostly senior with deep K8s knowledge. They wanted kubectl as the only interface; UI as optional. Flux\'s CRD-first model fit. \"What\'s the state?\" answered by <code>kubectl get -A</code>. Slack alerts via notification-controller. Total UI: zero by design."),
    ],
    misconceptions=[
        Misconception(myth="Flux is older and less feature-rich than Argo CD.", truth="Flux v1 was older; Flux v2 (current) is a complete rewrite with the multi-controller architecture. Both are CNCF graduated; both have rich feature sets; pick by preference."),
        Misconception(myth="Flux has no UI.", truth="Flux\'s built-in UI is minimal. <strong>Weave GitOps</strong> + <strong>Capacitor</strong> are popular dashboards layered on top. The default experience is kubectl + flux CLI."),
        Misconception(myth="You can\'t use Helm with Flux.", truth="Flux\'s <code>HelmRelease</code> CRD is one of its core features. Many shops use Flux specifically for Helm management."),
    ],
    flashcards=[
        Flashcard(front="Flux\'s five core controllers?", back="source-controller, kustomize-controller, helm-controller, notification-controller, image-automation + image-reflector-controllers."),
        Flashcard(front="GitRepository CRD?", back="Source-controller CRD. Defines a git URL + ref + interval. Source-controller fetches and exposes the contents to other controllers."),
        Flashcard(front="Kustomization CRD?", back="Distinct from <code>kustomization.yaml</code>. The K8s CRD points at a source path, runs <code>kustomize build</code>, applies result. Has <code>prune</code>, <code>healthChecks</code>, <code>dependsOn</code> fields."),
        Flashcard(front="HelmRelease CRD?", back="Declarative Helm install. Points at a chart source + values; helm-controller manages install/upgrade/rollback."),
        Flashcard(front="flux bootstrap?", back="One command to install Flux into a cluster + commit Flux\'s own manifests to a git repo. From then on, Flux manages itself via GitOps."),
        Flashcard(front="dependsOn?", back="Kustomization field: \"don\'t apply this until that Kustomization is healthy.\" Used for ordering: install CRDs first, then operators."),
        Flashcard(front="Notification provider types?", back="Slack, Discord, Microsoft Teams, PagerDuty, OpsGenie, generic webhook, GitHub/GitLab/Bitbucket commit-status, Forge, Grafana, Sentry."),
        Flashcard(front="image-automation flow?", back="image-reflector watches OCI; when a new tag matches policy, image-automation-controller commits the tag bump back to git. Source-controller picks up; Kustomize-controller deploys."),
    ],
    quizzes=[
        Quiz(prompt="A team is choosing between Argo CD and Flux. They have 80 microservices, ~30 engineers, mix of Kustomize and Helm. What factors should drive the choice?", answer="<strong>Both work.</strong> Factors that tip the choice: <strong>Argo CD if:</strong> (1) team values UI for visibility — Argo CD\'s default UI is excellent. (2) need PR-preview-environments — ApplicationSet PR generator is purpose-built. (3) onboarding new engineers fast — UI lowers ramp time. <strong>Flux if:</strong> (1) team is kubectl-first — Flux feels native. (2) need multi-source flexibility (S3 buckets, generic OCI) — Flux\'s source types are broader. (3) prefer composable architecture (install only what you need). (4) heavy Helm — HelmRelease is first-class, more flexible than Argo CD\'s Helm support. <strong>Same regardless:</strong> both need git workflow discipline; both have CNCF graduate maturity; both integrate with Kustomize + Helm. Pilot one for a quarter; switch only if you hit a hard limit (rare). Most successful shops use whichever they tried first."),
        Quiz(prompt="A Flux <code>HelmRelease</code> for cert-manager keeps showing <code>Stalled</code> after upgrade. What\'s the diagnostic path?", answer="<strong>(1) <code>flux get helmreleases -A</code></strong> — see the high-level state. <strong>(2) <code>kubectl describe helmrelease cert-manager</code></strong> — read the <code>status.conditions</code>. Common stalled reasons: (a) values schema validation failed — check the chart\'s values.schema.json against your values. (b) hook timeout — increase <code>spec.timeout</code>. (c) immutable field change — Helm can\'t modify it; needs uninstall + reinstall. <strong>(3) <code>kubectl logs -n flux-system deploy/helm-controller</code></strong> — controller logs show the actual Helm error. <strong>(4) <code>flux suspend helmrelease cert-manager</code></strong> + manual fix + <code>flux resume</code> — bypass automation while you debug. <strong>(5) Last resort: uninstall + reinstall.</strong> <code>kubectl delete helmrelease cert-manager</code> (forces uninstall). Restore the HelmRelease YAML in git (Flux re-installs). Test changes in dev / staging first."),
        Quiz(prompt="Engineering manager: \"we\'re adopting GitOps. Pick Flux or Argo CD by Friday.\" <strong>Click for the decision framework. ▼</strong>", cyoa=True, cyoa_tag="the decision framework", answer="<strong>(1) Survey the team.</strong> 5-minute poll: do they prefer GUIs or kubectl? Are they comfortable with K8s CRDs as the primary interface? Strong GUI preference → Argo CD. Strong kubectl preference → Flux. <strong>(2) Audit existing infrastructure.</strong> Already using Helm heavily? Flux\'s HelmRelease is more flexible. Already using lots of multi-cluster? Argo CD\'s ApplicationSet cluster generator + UI is helpful. <strong>(3) Pick the use case driving the decision.</strong> Need preview environments per PR? Argo CD\'s PR generator is purpose-built; Flux requires more glue. Need multi-source (Bucket, OCI, generic git)? Flux\'s source types are broader. <strong>(4) Pilot.</strong> Set up one cluster on each, with 3-5 microservices each, for 2 weeks. Compare engineer feedback. <strong>(5) Decide; commit.</strong> Both tools support migration if you need to switch later, but it\'s rare. The bigger risk is indecision; pick + commit + onboard. <strong>(6) Don\'t over-engineer the decision.</strong> Either tool works. The 80% of value is GitOps itself; the tool is the 20%."),
    ],
    glossary=[
        GlossaryItem(name="Flux CD", definition="Multi-controller GitOps tool. CNCF graduated. CRD-driven; minimal default UI."),
        GlossaryItem(name="source-controller", definition="Fetches from GitRepository, HelmRepository, OCIRepository, Bucket sources."),
        GlossaryItem(name="GitRepository", definition="Source-controller CRD: git URL + ref + interval."),
        GlossaryItem(name="kustomize-controller", definition="Renders Kustomize + applies."),
        GlossaryItem(name="Kustomization (Flux CRD)", definition="Declares a Kustomize-built deploy. Distinct from <code>kustomization.yaml</code>."),
        GlossaryItem(name="helm-controller", definition="Manages Helm releases declaratively."),
        GlossaryItem(name="HelmRelease", definition="Helm-controller CRD. Declarative Helm install/upgrade."),
        GlossaryItem(name="notification-controller", definition="Sends alerts on Flux events. CRDs: Provider, Alert, Receiver."),
        GlossaryItem(name="image-automation-controller", definition="Auto-bumps image tags in git on new OCI versions."),
        GlossaryItem(name="image-reflector-controller", definition="Watches OCI registries, exposes new tags as ImagePolicy CRDs."),
        GlossaryItem(name="flux bootstrap", definition="Install Flux into a cluster + commit Flux\'s own manifests to git."),
        GlossaryItem(name="Weave GitOps / Capacitor", definition="Optional UIs for Flux. Layer on top of CRDs."),
    ],
    recap_lead="Flux is GitOps via specialised controllers. Source-controller fetches, kustomize-controller applies Kustomize, helm-controller manages Helm, notification-controller alerts. CRD-first; no built-in UI. Same goal as Argo CD; different aesthetic.",
    recap_next="<strong>Next — Lesson 40: Progressive Delivery.</strong> The next layer above GitOps — controlled rollouts, automated canary analysis, automated rollback. Argo Rollouts and Flagger.",
)
