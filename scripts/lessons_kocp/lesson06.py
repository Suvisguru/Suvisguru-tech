"""K-OCP O6 — Workloads and Developer Experience (S2I, BuildConfig, ImageStream, Pipelines, GitOps, Serverless, Dev Spaces)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OCP developer experience — S2I, BuildConfigs, Pipelines, GitOps, Serverless, Service Mesh, Dev Spaces.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Mold Shop — build, ship, run with developer-friendly tooling</text>
  <rect x="40" y="65" width="170" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="125" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">build pipeline (built-in)</text>
  <text x="125" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">S2I (Source-to-Image)</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">BuildConfig + Build</text>
  <text x="125" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">ImageStream + tags</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">internal registry</text>
  <rect x="225" y="65" width="170" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="310" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">CI / CD (managed)</text>
  <text x="310" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">OpenShift Pipelines</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">(Tekton)</text>
  <text x="310" y="135" text-anchor="middle" font-size="9" fill="#FFFFFF">OpenShift GitOps</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">(Argo CD)</text>
  <rect x="410" y="65" width="170" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="495" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">runtimes (managed)</text>
  <text x="495" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">Serverless (Knative)</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">Service Mesh (Istio)</text>
  <text x="495" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">Dev Spaces (Che)</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">Helm in OCP</text>
  <rect x="595" y="65" width="125" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="657" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">workloads</text>
  <text x="657" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">Deployment (modern)</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">DeploymentConfig (legacy)</text>
  <text x="657" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">Templates</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">Developer Catalog</text>
</svg>"""


LESSON = LessonSpec(
    num="06", title_short="workloads &amp; DevEx",
    title_full="O6 · Workloads and Developer Experience (S2I + BuildConfigs + Pipelines + GitOps + Serverless + Service Mesh + Dev Spaces)",
    title_html="K-OCP O6 · Workloads + Developer Experience",
    module_eyebrow="Module O6 · the Mold Shop",
    hero_sub_html='Built-in: <strong>Source-to-Image (S2I)</strong> + <strong>BuildConfig</strong> + <strong>Build</strong> + <strong>ImageStream</strong> + <strong>ImageStreamTag</strong> + internal registry. <strong>DeploymentConfig (legacy)</strong> vs <strong>Deployment</strong>. <strong>Templates</strong>. Managed via Operators: <strong>OpenShift Pipelines</strong> (Tekton-based), <strong>OpenShift GitOps</strong> (Argo CD-based), <strong>OpenShift Serverless</strong> (Knative), <strong>OpenShift Service Mesh</strong> (Istio), <strong>OpenShift Dev Spaces</strong> (Eclipse Che). <strong>Helm in OCP</strong> via Developer Catalog. <strong>Web console</strong> Developer perspective for topology + dev workflows.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"Build is failing — \'sti-build\' container error\".</em> The team\'s Source-to-Image build for a Java app stopped working overnight. The S2I builder image (<code>java-openshift-s2i</code>) was updated in the OperatorHub catalog; the BuildConfig pinned no specific tag; the ImageStream auto-resolved to the new builder; the new builder requires a different env var. Plus the BuildConfig output goes to an ImageStream that\'s referenced by a DeploymentConfig (legacy) using image triggers — last build broke the trigger and replicaSet rollout failed silently. <em>Three OCP-specific concepts (S2I + ImageStream + DeploymentConfig) interlocked in failure.</em> Today\'s lesson: the Mold Shop tools.",
    stamp_html="<strong>S2I + BuildConfig + ImageStream is the OCP-native build pipeline; works alongside (not replacing) external CI. Pipelines (Tekton) and GitOps (Argo CD) ship as managed Operators. Serverless / Service Mesh / Dev Spaces are productized Knative / Istio / Che. Use Deployment over DeploymentConfig for new workloads.</strong>",
    district_pin="ko-bay06", district_label="Mold Shop",
    sections=[
        Section(eyebrow="Section 1.1 · S2I + BuildConfig + ImageStream", h2="S2I + BuildConfig + ImageStream + internal registry",
            body_html="""    <p><strong>Source-to-Image (S2I)</strong> = build container images from source code <em>without</em> writing a Dockerfile. S2I builder images encode the build logic for a language/framework (Java, Node, Python, Ruby, etc.). You provide source repo URL; S2I clones, builds, packages, outputs an image to the internal registry.</p>
    <p><strong>BuildConfig</strong> declares: source (Git URL + branch + context-dir), strategy (S2I vs Docker vs Custom), output (target ImageStreamTag), triggers (webhook / image-change / manual). One BuildConfig → many <strong>Build</strong> CRs (each Build is one execution).</p>
    <p><strong>ImageStream</strong> = abstraction over container image tags. <code>my-app:latest</code> as an ImageStreamTag points to a specific image SHA in the internal registry. Decouples consumers (Deployments) from concrete image versions; updates flow via image triggers.</p>
    <p><strong>Internal container registry</strong> (<code>image-registry.openshift-image-registry.svc:5000</code>) — built-in registry hosting BuildConfig outputs + ImageStream-tracked images. Project-scoped namespaces; RBAC via OCP roles.</p>
    <p><strong>oc new-app</strong> + <strong>oc new-build</strong> — quick-start commands: <code>oc new-app https://github.com/my/repo</code> autodetects language → creates BuildConfig + ImageStream + Service + DeploymentConfig + Route in one command. Great for dev-stage spin-up.</p>"""),
        Section(eyebrow="Section 1.2 · Deployment vs DeploymentConfig + Templates", h2="DeploymentConfig (legacy) vs Deployment + Templates",
            body_html="""    <p><strong>DeploymentConfig (DC)</strong> = OCP\'s pre-Deployment workload primitive. Predates K8s\' Deployment + ReplicaSet. Has unique features: image triggers (auto-deploy on ImageStream tag change), config-change triggers, lifecycle hooks (pre / mid / post deploy), automatic rollback on failed deploy.</p>
    <p><strong>Deployment</strong> (K8s standard) = the recommended workload primitive. ReplicaSet-based; rolling updates; rollback via kubectl rollout undo. <em>For new workloads, use Deployment</em>; DeploymentConfig is legacy + still supported but no longer the default.</p>
    <p><strong>When DC over Deployment?</strong> When you genuinely need OCP-specific image-triggered redeploys without external CI. Otherwise Deployment + image-trigger via Pipelines / GitOps / external CI is the modern path.</p>
    <p><strong>Templates</strong> = pre-OperatorHub mechanism for app templates. Parameterised YAML (image, replicas, resources, etc.) instantiated via <code>oc process &lt;template&gt; -p PARAM=value | oc apply -f -</code>. Still used in Developer Catalog. Largely superseded by Helm + Operators for new platforms but still common.</p>"""),
        Section(eyebrow="Section 1.3 · Pipelines + GitOps + Serverless + Service Mesh",
            h2="OpenShift Pipelines (Tekton) + GitOps (Argo CD) + Serverless (Knative) + Service Mesh (Istio)",
            body_html="""    <p><strong>OpenShift Pipelines</strong> = managed <strong>Tekton</strong>. Pipeline + Task + PipelineRun + TaskRun CRs. Container-native CI/CD; Pods run each task. Tekton Hub catalog of reusable Tasks. <em>Replaces Jenkins on OCP.</em></p>
    <p><strong>OpenShift GitOps</strong> = managed <strong>Argo CD</strong>. Application + ApplicationSet + AppProject CRs. Continuous reconciliation from Git into clusters. Replaces self-installed Argo CD or Flux. Sync wave / hooks support. Multi-cluster via ApplicationSet.</p>
    <p><strong>OpenShift Serverless</strong> = managed <strong>Knative</strong>. Knative Serving (autoscale to zero, request-based scaling, traffic splitting) + Knative Eventing (event-driven workflows). For request-driven workloads with idle cost concerns; for event consumers (Kafka / CloudEvents).</p>
    <p><strong>OpenShift Service Mesh</strong> = managed <strong>Istio</strong>. Sidecars on Pods for mTLS, traffic management, observability. Multi-cluster mesh + Gateway API support. Managed by the Service Mesh Operator; cluster-scoped Istio control plane.</p>"""),
        Section(eyebrow="Section 1.4 · Dev Spaces + Helm + Developer Catalog + Console workflows",
            h2="Dev Spaces (Eclipse Che) + Helm + Developer Catalog + web console workflows",
            body_html="""    <p><strong>OpenShift Dev Spaces</strong> = managed <strong>Eclipse Che</strong>. Cloud-hosted dev environments (Pods running editor + tools) for browser-based development. Devfiles define the workspace stack. <em>For onboarding, demo environments, or laptop-less dev.</em></p>
    <p><strong>Helm in OCP</strong> — fully supported. Helm charts visible in the <strong>Developer Catalog</strong> alongside Templates and Operator-installable apps. Add custom Helm chart repos via <code>HelmChartRepository</code> CR. Tiller-less (Helm 3+); RBAC via the user\'s OCP credentials.</p>
    <p><strong>Developer Catalog</strong> = Developer perspective view of installable apps: Templates + Helm charts + S2I builders + Operator-backed services. Click-to-deploy with parameterised forms.</p>
    <p><strong>Web console workflows:</strong>
    <ul>
      <li><strong>Topology view</strong> — visualises Project: Deployments, Services, Routes, Pods + their connections. Click an icon for actions (scale, edit, view logs, port-forward, debug).</li>
      <li><strong>Pipelines view</strong> — Tekton Pipeline runs + logs + success/failure timeline.</li>
      <li><strong>Builds view</strong> — BuildConfig + Build status + logs.</li>
      <li><strong>Add+ menu</strong> — quick-start: From Git, From Container image, From Catalog (Templates + Helm), Container Image, Database, etc.</li>
    </ul></p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A team is starting a new Spring Boot app on OCP. Should they use S2I, Dockerfile build, or external CI?",
        options=[("DeploymentConfig + S2I — that\'s the OCP way.", False),
            ("Pick by team preference: S2I for fastest no-Dockerfile path; Dockerfile (Docker strategy in BuildConfig) for full control; external CI (e.g., GitHub Actions building + pushing to ACR/Quay/internal registry) for portability across clusters. All three valid; Deployment is the workload primitive in any case.", True),
            ("Always use Templates.", False)],
        feedback="No single right answer — pick by team\'s portability needs + Dockerfile experience. Use Deployment (not DeploymentConfig) for new workloads regardless.",
    )},
    before_after_before='<p>Pre-Operator-managed CI/CD on K8s = self-installed Argo CD + Tekton + Knative + Istio + cert-manager + 5 more Helm charts. Each chart has its own upgrade cycle; chart drift was constant. Dev environments meant per-developer laptop setup with widely-varying tool versions. No built-in build path — devs wrote Dockerfiles or external CI configs.</p>',
    before_after_after='<p>OCP ships <strong>S2I + BuildConfig + ImageStream + internal registry</strong> as built-in build path. Managed Operators: <strong>Pipelines (Tekton)</strong>, <strong>GitOps (Argo CD)</strong>, <strong>Serverless (Knative)</strong>, <strong>Service Mesh (Istio)</strong>, <strong>Dev Spaces (Eclipse Che)</strong>. <strong>Developer Catalog</strong> + topology view in web console. <em>End-to-end developer experience without assembly.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Red Hat productizes the major K8s dev tools as supported Operators. Less assembly; one vendor accountable for the whole DX stack.</em></p>',
    analogy_intro_html='''<p>The <strong>Mold Shop</strong> at K-Foundry is where raw material (source code) becomes finished products (running workloads). The Foundry-Master-built tools sit on the workbench:</p>
    <p>The <strong>S2I press</strong> takes source code + a builder image (one for Java, one for Python, etc.) and stamps out a finished container image. No Dockerfile required — the builder image\'s knowledge handles the language-specific packaging. The <strong>BuildConfig recipe card</strong> declares what to build; each <strong>Build job ticket</strong> is one execution. The <strong>ImageStream conveyor</strong> tracks finished images by tag; downstream consumers (Deployments) listen for new tags and roll forward.</p>
    <p>For more complex CI/CD, the <strong>Pipelines (Tekton) workshop</strong> chains Tasks into Pipelines. The <strong>GitOps (Argo CD) reconciler</strong> continuously syncs from Git to cluster — git push = production rollout.</p>
    <p>For specialty runtimes: <strong>Serverless (Knative)</strong> for scale-to-zero request workloads; <strong>Service Mesh (Istio)</strong> for sidecar-managed mTLS + routing; <strong>Dev Spaces (Eclipse Che)</strong> for browser-based dev environments.</p>
    <p>The <strong>Developer Catalog</strong> is the parts catalog visible to app devs: Templates + Helm charts + S2I builders + Operator-backed services. The <strong>topology view</strong> in the web console shows the running Project as a graph.</p>''',
    translation_rows=[("S2I press", "Source-to-Image (S2I) build strategy"),
        ("Builder image (per-language)", "S2I builder image (java / python / nodejs / etc.)"),
        ("Recipe card", "BuildConfig"),
        ("Build job ticket", "Build CR (one execution)"),
        ("ImageStream conveyor", "ImageStream + ImageStreamTag (decouples consumers from image SHAs)"),
        ("Internal-parts warehouse", "Internal container registry (image-registry.openshift-image-registry.svc:5000)"),
        ("Quick-start order command", "<code>oc new-app</code> + <code>oc new-build</code>"),
        ("Foundry workshop chain", "OpenShift Pipelines (Tekton) — Pipeline + Task + PipelineRun"),
        ("Continuous-sync reconciler", "OpenShift GitOps (Argo CD) — Application + ApplicationSet"),
        ("Scale-to-zero turbine", "OpenShift Serverless (Knative)"),
        ("Sidecar-mediated traffic shop", "OpenShift Service Mesh (Istio)"),
        ("Cloud-hosted dev workshop", "OpenShift Dev Spaces (Eclipse Che)"),
        ("Pre-built Mold Shop catalog", "Developer Catalog (Templates + Helm + S2I + Operators)"),
        ("Foundry overview map", "Web console Topology view"),
        ("Pre-Deployment workload primitive", "DeploymentConfig (DC) — legacy, still supported"),
        ("Modern workload primitive", "Deployment (K8s standard)")],
    analogy_stops="A real mold shop has fixed press lines; OCP\'s build/CI/runtime stack is software-defined. Helm chart drift across teams is a real failure mode the metaphor doesn\'t capture.",
    eli5="The Mold Shop turns code into running apps. The S2I press handles the basic stamp-out for common languages; the Pipelines workshop handles fancier CI; the GitOps reconciler keeps the cluster matching what\'s in git. Plus specialty runtimes for scale-to-zero, mesh routing, and browser dev environments.",
    eli10="OCP DX = built-in S2I + BuildConfig + ImageStream + internal registry; managed Operators for OpenShift Pipelines (Tekton), OpenShift GitOps (Argo CD), OpenShift Serverless (Knative), OpenShift Service Mesh (Istio), OpenShift Dev Spaces (Eclipse Che); Helm in Developer Catalog; <code>oc new-app</code> for quick-start. Use Deployment (not DeploymentConfig) for new workloads. Topology view + Developer perspective in web console.",
    scenarios=[
        Scenario(name="SaaS — GitOps + Pipelines for git-push-to-prod",
            body="A SaaS uses OpenShift GitOps + Pipelines: developer pushes to feature branch → Pipeline runs unit tests + builds container via S2I to ImageStream → on merge to main, Pipeline tags image → Argo CD detects change → reconciles to staging → automated promotion job to prod after smoke tests. <em>Git push to prod takes 12 minutes.</em>"),
        Scenario(name="Legacy migration — Java apps S2I-built without Dockerfiles",
            body="A bank migrates 40 legacy Java apps to OCP. They use the Java S2I builder; no Dockerfiles to write. <code>oc new-app</code> per app generates BuildConfig + Deployment + Service + Route. Builder image upgrades flow automatically via image triggers. <em>40 apps containerised + deployed in 2 weeks; no Dockerfile expertise required.</em>"),
        Scenario(name="Event-driven — OpenShift Serverless scales to zero between events",
            body="A retail platform processes order events from Kafka. Each consumer is a Knative Service; idle = zero replicas; events arrive → Knative scales pods up; processed → scale back to zero. <em>Off-hours infra cost approaches zero; no over-provisioning required.</em>"),
        Scenario(name="Onboarding — Dev Spaces saved 3 days per new hire",
            body="A 200-engineer team uses Dev Spaces for new-hire onboarding. Day 1: log into console, click \"Open in Dev Spaces\" on the project repo, get a fully-configured workspace (Java 17 + Maven + IDE + dependencies pre-loaded). <em>3 days of laptop setup compressed to 5 minutes.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"Use DeploymentConfig because it\'s OCP-native.\"",
            truth="<strong>Deployment</strong> is the modern recommendation for new workloads. DeploymentConfig is legacy + still supported but not preferred. Use Deployment + image triggers via Pipelines / GitOps / external CI for the modern path. DC only when you specifically need its OCP-only image-trigger feature without external CI."),
        Misconception(myth="\"S2I is a black box; I have no control over the build.\"",
            truth="S2I builder images are open and customisable. Add scripts via <code>.s2i/bin/</code> in your repo (assemble, run, save-artifacts hooks). Customise base images to add packages. Or use <strong>Docker strategy</strong> BuildConfig for full Dockerfile control. S2I covers 80% case; Docker covers the rest."),
        Misconception(myth="\"OpenShift Pipelines is just rebranded Jenkins.\"",
            truth="<strong>Pipelines = Tekton</strong>, container-native CI/CD where each Task runs as a Pod. No Jenkins server, no plugin sprawl, no JVM tuning. Tekton has its own Hub of reusable Tasks. Different paradigm from Jenkins; better-suited to K8s-native workflows."),
    ],
    flashcards=[
        Flashcard(front="What is Source-to-Image (S2I)?", back="Build container images from source code without writing a Dockerfile. Builder images per-language (Java / Python / Node / etc.) encode build logic. <code>oc new-app https://github.com/my/repo</code> autodetects + creates BuildConfig + ImageStream + Service + Route + DC."),
        Flashcard(front="BuildConfig + Build + ImageStream — what does each do?", back="<strong>BuildConfig</strong>: declares source + strategy + output + triggers. <strong>Build</strong>: one execution of a BuildConfig. <strong>ImageStream</strong>: abstraction over image tags; decouples consumers from concrete SHAs."),
        Flashcard(front="Deployment vs DeploymentConfig — which to use?", back="Use <strong>Deployment</strong> (K8s standard) for new workloads. <strong>DeploymentConfig</strong> is OCP legacy with image-triggers + config-change triggers built in; still supported but Deployment + GitOps/Pipelines image-trigger is the modern path."),
        Flashcard(front="OpenShift Pipelines vs OpenShift GitOps?", back="<strong>Pipelines</strong> = Tekton; CI workflows (test/build/lint) as Tasks chained into Pipelines. <strong>GitOps</strong> = Argo CD; continuous reconciliation from git to cluster. Used together: Pipelines build + push + tag; GitOps deploys."),
        Flashcard(front="What is OpenShift Serverless?", back="Managed Knative — Knative Serving (autoscale to zero, request-based, traffic splitting) + Knative Eventing (event-driven workflows). For idle-tolerant request workloads + event consumers."),
        Flashcard(front="What is OpenShift Service Mesh?", back="Managed Istio — sidecar-injected mTLS, traffic management, observability. Multi-cluster mesh + Gateway API support. Service Mesh Operator + ServiceMeshControlPlane CR."),
        Flashcard(front="What is OpenShift Dev Spaces?", back="Managed Eclipse Che — cloud-hosted dev environments. Pods run editor + dev tools; browser access. Devfiles define workspace stack. For onboarding / demo / laptop-less dev."),
        Flashcard(front="Where do you find Helm in OCP?", back="<strong>Developer Catalog</strong> in the Developer perspective. Built-in Helm 3+ support (no Tiller). Add custom Helm chart repos via <code>HelmChartRepository</code> CR. RBAC via user\'s OCP credentials."),
    ],
    quizzes=[
        Quiz(prompt="A new team starting on OCP. They want to deploy a Spring Boot app. Walk through the simplest path.",
            answer="(1) Create a Project: <code>oc new-project myapp</code>. (2) <code>oc new-app https://github.com/team/myapp.git</code> — autodetects Java; uses Java S2I builder; creates BuildConfig + ImageStream + Deployment + Service. (3) <code>oc expose service/myapp</code> — creates a Route with auto-generated hostname. (4) Wait for Build to complete: <code>oc logs -f bc/myapp</code>. (5) App reachable at the Route URL. <em>~5 minutes from git URL to deployed Pod.</em> For prod: layer on Pipelines for CI gates + GitOps for deployment reconciliation."),
        Quiz(prompt="An S2I build started failing after a builder image update. What\'s the diagnostic + recovery?",
            answer="(1) <code>oc get builds -n &lt;project&gt;</code> — find the failed Build. (2) <code>oc logs build/&lt;name&gt;</code> — error from S2I assemble script. (3) Compare against the previous (working) builder image: <code>oc describe is &lt;builder-is&gt;</code> for tag history. (4) Pin BuildConfig\'s strategy to a specific builder ImageStreamTag (don\'t auto-track latest): <code>spec.strategy.sourceStrategy.from.name: &quot;openshift/java:11&quot;</code>. (5) Re-trigger build. (6) For production: pin builder versions in BuildConfig; review builder image release notes before bumping."),
        Quiz(prompt="The CTO asks: \"Why are we using OpenShift Pipelines instead of Jenkins we already have?\" Defend.",
            answer="\"<strong>OpenShift Pipelines (Tekton) is K8s-native CI/CD.</strong> Each Task runs as a Pod — no Jenkins server to operate, no plugin sprawl, no JVM tuning, no jobs queued behind a single coordinator. PipelineRuns + TaskRuns are CRs we can manage via GitOps. Tekton Hub has reusable Tasks for common operations (git clone, S2I build, Argo CD sync, etc.) — we share these across projects. Compared to Jenkins: zero infrastructure to operate; native to OCP\'s Operator + RBAC model; integrated with the Developer perspective for visibility. <em>Cost saving: we shut down 3 Jenkins controllers + ~12 agents that we were operating.</em> Where Jenkins still wins: shops with deep Jenkins-pipeline-as-code investments + custom Groovy + a Jenkins admin team — migration cost matters. For new shops, Pipelines is the default.\"",
            cyoa=True, cyoa_tag="how the platform engineer answered the CTO"),
    ],
    glossary=[
        GlossaryItem(name="S2I (Source-to-Image)", definition="OCP build strategy: builder image + source repo → container image. No Dockerfile required."),
        GlossaryItem(name="BuildConfig", definition="CR declaring source + strategy (S2I/Docker/Custom) + output + triggers (webhook / image-change / manual)."),
        GlossaryItem(name="Build", definition="One execution of a BuildConfig. Pod runs the build."),
        GlossaryItem(name="ImageStream", definition="Abstraction over image tags. Decouples consumers from concrete image SHAs."),
        GlossaryItem(name="ImageStreamTag", definition="A specific tag in an ImageStream pointing at a specific image SHA."),
        GlossaryItem(name="Internal registry", definition="image-registry.openshift-image-registry.svc:5000 — built-in container registry per cluster."),
        GlossaryItem(name="oc new-app / oc new-build", definition="Quick-start commands. <code>oc new-app GIT_URL</code> autodetects + creates BuildConfig + IS + Deployment + Service + Route."),
        GlossaryItem(name="DeploymentConfig (DC)", definition="OCP\'s pre-Deployment workload primitive. Image triggers + lifecycle hooks. Legacy; use Deployment for new workloads."),
        GlossaryItem(name="Template", definition="Parameterised YAML instantiated via <code>oc process</code>. Pre-OperatorHub mechanism. Still in Developer Catalog."),
        GlossaryItem(name="OpenShift Pipelines", definition="Managed Tekton — Pipeline / Task / PipelineRun / TaskRun CRs."),
        GlossaryItem(name="OpenShift GitOps", definition="Managed Argo CD — Application / ApplicationSet / AppProject CRs."),
        GlossaryItem(name="OpenShift Serverless", definition="Managed Knative — Serving + Eventing. Scale-to-zero, request-based, event-driven."),
        GlossaryItem(name="OpenShift Service Mesh", definition="Managed Istio — sidecar mTLS + traffic + observability + Gateway API."),
        GlossaryItem(name="OpenShift Dev Spaces", definition="Managed Eclipse Che — cloud-hosted dev environments via Devfiles."),
        GlossaryItem(name="Developer Catalog", definition="Web console catalog of installable apps: Templates + Helm + S2I + Operator-backed services."),
        GlossaryItem(name="Topology view", definition="Web console graph of a Project: Deployments + Services + Routes + Pods + connections."),
    ],
    recap_lead='Built-in: S2I + BuildConfig + ImageStream + registry. Managed Operators: Pipelines + GitOps + Serverless + Service Mesh + Dev Spaces. Use Deployment for new workloads.',
    recap_next='<strong>Next — O7: OpenShift Storage.</strong> ODF (Ceph + NooBaa + Rook) for block/file/object; Local + LVM Storage Operators (single-node/edge); CSI per-cloud (vSphere, EBS, Disk/File, GCE PD); RWX storage; snapshots; OADP (Velero-based); registry storage; monitoring storage.',
)
