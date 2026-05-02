from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Workshop interior: a kubebuilder workbench with code-gen tools, controller-runtime engine, manager + reconciler diagram, OLM display case for distribution.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">WORKSHOP · OPERATOR BUILDER\'S BENCH</text>
  <g transform="translate(40,55)"><rect width="160" height="120" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/><text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">controller-runtime</text><rect x="14" y="32" width="132" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="46" font-size="8" fill="#5A4F45" font-weight="700">Manager</text><rect x="14" y="56" width="132" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="70" font-size="8" fill="#5A4F45" font-weight="700">Reconciler</text><rect x="14" y="80" width="132" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="94" font-size="8" fill="#5A4F45" font-weight="700">Watches + Cache</text><text x="80" y="115" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">Go SDK</text></g>
  <g transform="translate(220,55)"><rect width="220" height="120" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/><text x="110" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">Kubebuilder scaffold</text><text x="14" y="36" font-size="7" fill="#5A4F45">api/v1/types.go</text><text x="14" y="48" font-size="7" fill="#5A4F45">controllers/db_controller.go</text><text x="14" y="60" font-size="7" fill="#5A4F45">main.go</text><text x="14" y="72" font-size="7" fill="#5A4F45">config/crd/bases/...</text><text x="14" y="84" font-size="7" fill="#5A4F45">config/manager/...</text><text x="14" y="96" font-size="7" fill="#5A4F45">Makefile + Dockerfile</text><text x="110" y="112" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">one command sets it up</text></g>
  <g transform="translate(460,55)"><rect width="180" height="120" rx="6" fill="#A04832"/><text x="90" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">OLM · OperatorHub</text><rect x="14" y="32" width="152" height="20" rx="2" fill="#FBE8DC"/><text x="20" y="46" font-size="8" fill="#A04832" font-weight="700">CSV (ClusterServiceVersion)</text><rect x="14" y="56" width="152" height="20" rx="2" fill="#FBE8DC"/><text x="20" y="70" font-size="8" fill="#A04832" font-weight="700">Subscription + InstallPlan</text><rect x="14" y="80" width="152" height="20" rx="2" fill="#FBE8DC"/><text x="20" y="94" font-size="8" fill="#A04832" font-weight="700">automatic upgrade channels</text><text x="90" y="115" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">distribution + lifecycle</text></g>
</svg>"""

LESSON = LessonSpec(
    num="42",
    title_short="Operators",
    title_full="Operators with Kubebuilder · controller-runtime, OLM",
    title_html="Lesson 42 — Operators with Kubebuilder · K-COM",
    module_eyebrow="Module 18 · Lesson 42 · the brain behind the CRD",
    hero_sub_html='A CRD declares a new kind. An <strong>operator</strong> is the controller that makes that kind <em>do</em> something — reconcile a database, manage certs, run a Kafka cluster, take backups. Modern operators are written with <strong>controller-runtime</strong> (Go SDK) scaffolded by <strong>Kubebuilder</strong>; distributed via plain Helm charts or via the <strong>Operator Lifecycle Manager (OLM)</strong>.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='You wrote a CRD describing a database. Now you need to actually <em>run</em> the database when someone applies a CR. Without an operator: it\'s an inert YAML object. With an operator: a controller watches your CR, creates the StatefulSet + Service + ConfigMap, monitors health, runs backups, handles upgrades. <em>Operators are the most common K8s extension</em>, and writing them used to be hard. controller-runtime + Kubebuilder made it merely tedious.',
    stamp_html='An <strong>operator</strong> = CRD + controller. Use <strong>Kubebuilder</strong> to scaffold a Go project (or <strong>Operator SDK</strong> for Helm/Ansible-based operators). The controller logic lives in a <strong>Reconciler</strong>: \"given the CR\'s desired state, make the cluster match.\" controller-runtime handles watches, caching, queueing, leader election. Distribute via Helm chart or OLM (OperatorHub).',
    district_pin="kt-pin42",
    district_label="Workshop — Operator Builder\'s Bench",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What an operator is",
            body_html="""    <p>The Operator Pattern: package operational knowledge as code. The CRD is the user-facing API; the controller is the operations runbook expressed in Go. The user writes \"<code>kind: PostgresCluster, replicas: 3, storage: 100Gi</code>\"; the operator does everything to make that real.</p>
    <p>The reconcile loop:</p>
    <ol>
      <li>User creates / updates a CR.</li>
      <li>The kube-apiserver writes it to etcd.</li>
      <li>The operator (running as a Pod in the cluster) is watching that CR kind. Receives an event.</li>
      <li>Reconciler reads the current CR + cluster state, computes the diff, applies changes.</li>
      <li>Updates the CR\'s <code>status</code> with what happened.</li>
      <li>Repeats indefinitely (\"reconcile loop\" — runs every change + periodically).</li>
    </ol>
    <p>This is exactly how K8s\'s built-in controllers work (Deployment controller, ReplicaSet controller, etc.). Operators extend the pattern to your custom kinds.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Kubebuilder + controller-runtime",
            h2="The Go-based standard",
            body_html="""    <p><strong>controller-runtime</strong> is the Go library underneath Kubebuilder. It abstracts: API client, informer cache, work queue, leader election, manager (lifecycle of all reconcilers). You write a Reconciler struct with a <code>Reconcile(ctx, req)</code> method; the framework handles everything else.</p>
    <p><strong>Kubebuilder</strong> is the project scaffolder + code generator. <code>kubebuilder init</code> creates the project; <code>kubebuilder create api --group example.com --version v1 --kind PostgresCluster</code> creates the CRD types + controller skeleton. From there you implement the Reconciler.</p>
    <p>A typical Reconciler:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>func (r *PostgresClusterReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. Fetch the CR
    var cluster examplev1.PostgresCluster
    if err := r.Get(ctx, req.NamespacedName, &amp;cluster); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    // 2. Reconcile owned resources
    if err := r.reconcileStatefulSet(ctx, &amp;cluster); err != nil {
        return ctrl.Result{}, err
    }
    if err := r.reconcileService(ctx, &amp;cluster); err != nil {
        return ctrl.Result{}, err
    }
    // 3. Update status
    cluster.Status.ReadyReplicas = ...
    if err := r.Status().Update(ctx, &amp;cluster); err != nil {
        return ctrl.Result{}, err
    }
    return ctrl.Result{}, nil
}</code></pre>
    <p>Use <code>ctrl.SetControllerReference</code> to set owner refs on owned objects (so they\'re garbage-collected when the CR is deleted). Use <code>SetupWithManager</code> to register watches: \"reconcile when the CR changes; reconcile when an owned StatefulSet changes.\"</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Reconciliation patterns",
            h2="Idempotent, level-triggered, observable",
            body_html="""    <p>Three properties every Reconciler should have:</p>
    <ul>
      <li><strong>Idempotent</strong> — running it twice with the same input produces the same result. No \"create if not exists\"; use <code>CreateOrUpdate</code> or <code>Patch</code> with server-side apply.</li>
      <li><strong>Level-triggered, not edge-triggered</strong> — react to current state, not to a specific event. Multiple events for the same CR get coalesced; the Reconciler reads the latest state and acts.</li>
      <li><strong>Observable</strong> — every reconcile updates <code>status</code> with what happened. Conditions, ready replicas, last reconcile time. Users debug via <code>kubectl describe</code>.</li>
    </ul>
    <p>Common patterns:</p>
    <ul>
      <li><strong>Finalizers</strong> — for resources that need cleanup before deletion (e.g., releasing external cloud resources). Add a finalizer; the operator clears it once cleanup is done; only then is the CR actually deleted.</li>
      <li><strong>Conditions</strong> — standardised status fields: <code>type, status, reason, message, lastTransitionTime</code>. Common types: Ready, Progressing, Degraded.</li>
      <li><strong>Events</strong> — operators emit K8s Events on the CR for visibility. <code>kubectl describe</code> shows them; useful for debugging.</li>
      <li><strong>Requeue</strong> — return <code>RequeueAfter: 30 * time.Second</code> to schedule a re-reconcile (poll external API, etc.).</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.9 · Operator distribution: Helm vs OLM",
            h2="How users install your operator",
            body_html="""    <p>Two main distribution paths:</p>
    <ul>
      <li><strong>Helm chart</strong> — the K8s-standard package format (Lesson 37). Works for any operator: chart contains CRDs + RBAC + Deployment for the operator. Users <code>helm install</code>. Mainstream, widely supported.</li>
      <li><strong>OLM (Operator Lifecycle Manager)</strong> — Red Hat\'s framework for operator distribution + lifecycle. Originally OpenShift-only; now mainstream. Users browse <strong>OperatorHub.io</strong>, install via <code>Subscription</code> CRD; OLM handles dependencies, upgrades, channels (stable / fast / dev), conflicts.</li>
    </ul>
    <p>OLM\'s value: automatic upgrade management. Users subscribe to a channel; OLM applies new versions when they\'re published, runs migration scripts, handles upgrade graphs. Helm requires manual <code>helm upgrade</code>.</p>
    <p>OLM\'s cost: an extra layer to learn + extra CRDs in your cluster. Many teams stick with Helm for simplicity.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The 2026 default for new operators: <strong>Helm chart</strong> for general distribution; <strong>OLM</strong> if your target audience is OpenShift-heavy. The CNCF Operator Hub (operatorhub.io) accepts both. Cluster API\'s control plane providers, cert-manager, Argo CD all distribute via Helm. OpenShift-aligned vendors (Red Hat OpenShift Service Mesh, OpenShift Pipelines) use OLM.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team\'s operator deletes the CR but external cloud resources (an S3 bucket, an RDS instance) remain. They want the operator to clean them up first. What\'s the pattern?",
            options=[
                ("a) Use a CronJob to clean up after CR deletion", False),
                ("b) Add a <strong>finalizer</strong> to the CR. Cleanup logic runs in the reconciler when the CR enters deleting state; remove finalizer when done.", True),
                ("c) Watch DeletionTimestamp via a separate controller", False),
            ],
            feedback="<strong>Answer: b.</strong> Finalizers block deletion until removed. Standard pattern: on first reconcile, add finalizer. On reconcile when DeletionTimestamp is set, run cleanup; remove finalizer when done; K8s then completes the deletion. Critical for any operator managing external resources.",
        ),
    },
    before_after_before='<p>Pre-Kubebuilder: write your own informer setup, queue, leader election, RBAC, code generation. Hundreds of lines of boilerplate before you write any business logic. Each operator\'s code looked different; quality varied wildly. Distribution: ad-hoc YAML or hand-rolled Helm charts.</p>',
    before_after_after='<p>Kubebuilder scaffolds the project. controller-runtime handles the framework. Idiomatic Reconciler. Generated CRD YAMLs, RBAC, Dockerfile, Makefile. Distribute via standard Helm chart or OLM. Operators across the ecosystem look similar; ramp-up time for a new operator project: hours, not weeks.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Kubebuilder + controller-runtime is the closest thing K8s has to Rails — opinionated scaffolding that makes the right thing easy. Most production operators built since 2021 use it.</p>',
    analogy_intro_html='<p>Workshop is the K-Town district where master craftspeople build custom assistants — robots that watch over a specific kind of permit (CRD) and take action when one is filed. The Workshop has a <strong>standard workbench</strong> (Kubebuilder) where new craftsperson sets up a project in an afternoon: standard tools, standard layout, standard code-gen. The <strong>engine</strong> (controller-runtime) handles all the boring infrastructure — listening for events, queueing work, surviving restarts. The craftsperson focuses on the business logic: what does this assistant <em>do</em> when a permit changes? Once built, the assistant is packaged for distribution: either a sealed envelope (Helm chart) or a registered subscription (OLM).</p>',
    translation_rows=[
        ("Standard workbench", "Kubebuilder scaffold"),
        ("Workbench engine", "controller-runtime"),
        ("Custom assistant for a permit kind", "Operator (controller for a CRD)"),
        ("Assistant\'s reaction logic", "Reconciler"),
        ("\"React to current state, not what just happened\"", "Level-triggered reconciliation"),
        ("\"Same input, same result\"", "Idempotent reconciler"),
        ("Cleanup before assistant lets the permit go", "Finalizer"),
        ("Status board the assistant updates", "<code>status.conditions</code>"),
        ("Sealed envelope distribution", "Helm chart"),
        ("Subscription registry distribution", "OLM / OperatorHub"),
    ],
    analogy_stops="The analogy stops here: real operators are Pods running real Go binaries. The \"engine\" of controller-runtime is leader election, informer caches, work queues — not actual machinery.",
    eli5='You build a robot that watches your custom forms. When you fill in a form, the robot does the work. Same form = same work; the robot doesn\'t panic.',
    eli10="An operator is a controller for a CRD. Use Kubebuilder (CLI scaffolder) + controller-runtime (Go SDK) to write one. Reconciler reads the CR + current state, makes them match, updates status. Patterns: idempotent, level-triggered, finalizers for cleanup, conditions for status. Distribute via Helm chart (most common) or OLM (Red Hat ecosystem).",
    scenarios=[
        Scenario(name="A SaaS operator managing internal databases", body="<code>InternalDatabase</code> CRD; user specifies size, type, backup policy. Operator creates StatefulSet + Service + Secret + CronJob (backup) + ServiceMonitor. Built with Kubebuilder; ~3000 lines of Go. Distributed via Helm internally; deployed via Argo CD."),
        Scenario(name="A bank using cert-manager (an operator)", body="<code>Issuer</code> + <code>Certificate</code> CRDs. cert-manager operator handles ACME flows, key rotation, secret updates. Distributed via Helm. Reliable, widely deployed; the canonical example of operator value."),
        Scenario(name="An ML platform using a model-serving operator", body="<code>InferenceService</code> CRD (KServe / Seldon). Operator creates a Knative Service or Deployment + autoscaling + canary. Routes inference traffic. Built on controller-runtime; mature project, widely used in ML platforms."),
        Scenario(name="A team migrating from custom controller to Kubebuilder", body="Old controller: ~5000 lines hand-written, used informer-only patterns, no leader election. Migrated to Kubebuilder: ~2200 lines, generated boilerplate, supports HA via leader election, easier to reason about. Migration paid for itself in 6 months of fewer ops issues."),
    ],
    misconceptions=[
        Misconception(myth="Operators must be written in Go.", truth="Most are, because controller-runtime is Go. But Operator SDK supports Helm-based and Ansible-based operators where you write no code. Pure-Helm operators are surprisingly capable: chart + dependency mgmt = an \"operator.\""),
        Misconception(myth="Reconciliation is the same as a webhook.", truth="Reconciliation is async + level-triggered (\"current state vs desired state\"). Webhooks are sync + edge-triggered (\"this specific request, accept or reject\"). Operators usually have both: webhook for admission validation, reconciler for state convergence."),
        Misconception(myth="An operator means OperatorHub + OLM.", truth="OperatorHub is a marketplace; OLM is the lifecycle manager. Both are optional. Most operators in production are installed via plain Helm; OperatorHub is for discovery + Red Hat ecosystem alignment."),
    ],
    flashcards=[
        Flashcard(front="What is an operator?", back="A custom controller for one or more CRDs. Encodes operational knowledge as reconciliation logic."),
        Flashcard(front="What is controller-runtime?", back="Go library providing Manager, Reconciler, watches, cache, leader election. The K8s-canonical operator framework."),
        Flashcard(front="What is Kubebuilder?", back="CLI scaffolder for controller-runtime projects. Generates project structure, CRD types, controller skeleton, RBAC, Dockerfile, Makefile."),
        Flashcard(front="What is Operator SDK?", back="Red Hat\'s operator-building toolkit. Supports Go (similar to Kubebuilder), Helm-based, Ansible-based operators."),
        Flashcard(front="Reconciler signature?", back="<code>Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error)</code>. Returning Result with RequeueAfter schedules another reconcile; error retries with backoff."),
        Flashcard(front="What is a finalizer?", back="String in <code>metadata.finalizers</code>. Blocks resource deletion until removed. Use to ensure operator cleans up external resources before CR vanishes."),
        Flashcard(front="What are conditions?", back="Standardised status fields: type, status (True/False/Unknown), reason, message, lastTransitionTime. Common types: Ready, Progressing, Degraded."),
        Flashcard(front="OLM vs Helm for distribution?", back="Helm: standard package, manual upgrades. OLM: Red Hat lifecycle manager; channels (stable/fast), automatic upgrades, dependency mgmt. Helm is more common; OLM in OpenShift ecosystems."),
    ],
    quizzes=[
        Quiz(prompt="An operator\'s Reconciler runs slowly: 5 seconds per reconcile. Cluster has 200 CRs. Diagnosis?", answer="<strong>Common causes:</strong> (1) <em>API server calls per reconcile</em>. <code>r.Get(...)</code> is cached; <code>r.List(...)</code> with no label selector is expensive. Use the cache; filter at the API level. (2) <em>External calls (cloud SDK, database)</em>. Each reconcile makes external calls; cache + concurrent calls help. (3) <em>Single-threaded reconciler</em>. Set <code>MaxConcurrentReconciles</code> to a higher value (default 1). (4) <em>Hot loop</em>. If reconcile triggers a watch that triggers reconcile, you\'re in a loop. Check that updates aren\'t triggering each other. <strong>Diagnostic:</strong> add Prometheus metrics from controller-runtime (built-in); look at reconcile_time histogram; profile with pprof if needed. <strong>Fix order:</strong> increase concurrency first, optimise hot paths second."),
        Quiz(prompt="A team\'s operator updates the CR\'s spec from inside the Reconciler. Why is this a problem?", answer="<strong>Anti-pattern.</strong> The CR\'s <code>spec</code> is user-managed; the controller writes <code>status</code>. If the controller writes spec, it competes with the user (next <code>kubectl apply</code> reverts the operator\'s change). Also: any change to spec triggers a reconcile; the operator can loop forever. <strong>Fix:</strong> use the <code>status</code> subresource. Read user intent from spec; encode controller observations in status. Use <code>r.Status().Update(ctx, ...)</code>. The spec is what the user wants; status is what the controller observes."),
        Quiz(prompt="A team is starting a new operator project. <strong>Click for the recommended setup. ▼</strong>", cyoa=True, cyoa_tag="the recommended setup", answer="<strong>(1) Bootstrap with Kubebuilder.</strong> <code>kubebuilder init --domain example.com --repo github.com/myorg/db-operator</code>. <code>kubebuilder create api --group databases --version v1alpha1 --kind PostgresCluster --resource --controller</code>. <strong>(2) Define types in <code>api/v1alpha1/postgrescluster_types.go</code>.</strong> Spec for user-facing config; Status for observed state. Add CEL validation via kubebuilder annotations: <code>// +kubebuilder:validation:XValidation:rule=\"self.replicas &gt; 0\"</code>. <strong>(3) Implement Reconciler.</strong> Fetch CR; reconcile owned resources (StatefulSet, Service, Secret, ConfigMap); update status. Use <code>controllerutil.CreateOrUpdate</code> for idempotency. <strong>(4) Add finalizer logic</strong> if you manage external resources. <strong>(5) Tests.</strong> envtest spins up a local kube-apiserver; write integration tests that verify reconcile behaviour. <strong>(6) Distribution.</strong> Default to Helm. Generate the chart from <code>config/</code>. Sign with cosign. Push to OCI registry. <strong>(7) Documentation.</strong> Sample CRs in <code>config/samples/</code>; tutorial in README. <strong>(8) CI.</strong> Lint, test, build image, sign, package chart, publish. <strong>Total time-to-functional-operator:</strong> 1-2 weeks for a competent Go developer. <strong>Total time-to-production:</strong> add 4-8 weeks of testing + observability + multi-version support + operational runbooks."),
    ],
    glossary=[
        GlossaryItem(name="Operator", definition="Custom controller managing CRDs. Encodes operational knowledge."),
        GlossaryItem(name="controller-runtime", definition="Go library: Manager, Reconciler, cache, watches, leader election. Canonical operator framework."),
        GlossaryItem(name="Kubebuilder", definition="CLI scaffolder for controller-runtime projects."),
        GlossaryItem(name="Operator SDK", definition="Red Hat\'s operator builder. Go, Helm, Ansible variants."),
        GlossaryItem(name="Reconciler", definition="Function: read CR + cluster state, make them match, update status. Idempotent + level-triggered."),
        GlossaryItem(name="Manager (controller-runtime)", definition="Holds reconcilers, manages lifecycle, leader election, healthz."),
        GlossaryItem(name="Watches / cache (informer)", definition="Listens to API server for changes; local cache for reads."),
        GlossaryItem(name="Finalizer", definition="String in metadata.finalizers blocking deletion. Use for cleanup of external resources."),
        GlossaryItem(name="Owner reference", definition="Garbage-collection link from a created resource to its CR. Set via <code>controllerutil.SetControllerReference</code>."),
        GlossaryItem(name="Leader election", definition="Multiple replicas; one leader actually reconciles. Built into controller-runtime; use leases."),
        GlossaryItem(name="OLM (Operator Lifecycle Manager)", definition="Red Hat\'s framework for installing/upgrading operators. CRDs: Subscription, InstallPlan, ClusterServiceVersion (CSV)."),
        GlossaryItem(name="OperatorHub.io", definition="Community marketplace for operators. CSV-based packaging."),
    ],
    recap_lead="Kubebuilder + controller-runtime is the canonical operator stack. Reconciler is the loop; idempotent + level-triggered + observable; finalizers + conditions + events for production polish. Distribute via Helm (most common) or OLM (Red Hat ecosystem).",
    recap_next="<strong>Next — Lesson 43: Service Mesh.</strong> The data-plane layer that adds mTLS, observability, traffic shaping to existing services without code changes. Istio ambient, Linkerd, Cilium Service Mesh.",
)
