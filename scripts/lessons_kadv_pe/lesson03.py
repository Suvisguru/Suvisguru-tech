"""K-ADV-PE P3 — Crossplane v2."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Crossplane v2 — XRD + Composition + Functions + Providers + Configuration package."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Composition Workbench · K-Workshop — platform-as-API</text><rect x="40" y="70" width="170" height="100" rx="10" fill="#3F4A5E"/><text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">XRD</text><text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">user-facing CRD schema</text><rect x="225" y="70" width="170" height="100" rx="10" fill="#5DCAA5"/><text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Composition + Functions</text><text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">KCL / Pkl / Go / patch-and-transform</text><rect x="410" y="70" width="170" height="100" rx="10" fill="#5A6B81"/><text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Providers</text><text x="495" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">AWS / Azure / GCP / SaaS</text><rect x="595" y="70" width="125" height="100" rx="10" fill="#FF9900"/><text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Config pkg</text><text x="657" y="108" text-anchor="middle" font-size="9" fill="#1F2433">shareable</text></svg>"""


LESSON = LessonSpec(
    num="03", title_short="Crossplane v2", title_full="P3 · Crossplane v2 — Providers, Compositions, XRDs, Functions, ConfigurationPackages",
    title_html="K-ADV-PE P3 · Crossplane v2", module_eyebrow="Module P3 · Composition Workbench — platform-as-API",
    hero_sub_html='<strong>Crossplane v2</strong>: K8s control plane for cloud + SaaS. <strong>XRD</strong> (CompositeResourceDefinition): user-facing CRD schema (e.g., XPostgresInstance). <strong>Composition</strong>: how to render the user\'s Claim into Provider resources. <strong>Functions</strong>: pluggable composition logic — KCL / Pkl / Go templates / patch-and-transform — replacing legacy patches. <strong>Providers</strong>: cloud + SaaS resource controllers (provider-aws-eks, provider-azure, provider-gcp, provider-github, provider-vault, etc.). <strong>ConfigurationPackages</strong>: shareable bundles distributed via OCI registries.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Two teams created the same Postgres instance manually with subtle differences — one has backups, one doesn\'t. <em>Without a platform API, every team rolls their own infra; drift is constant.</em> Today\'s lesson: Crossplane gives the platform team a CRD as the API; tenants consume; consistency is automatic.",
    stamp_html="<strong>Crossplane v2: XRD = user-facing CRD; Composition + Functions = render logic; Providers = AWS / Azure / GCP / SaaS controllers; ConfigurationPackage = shareable bundle. Platform-as-API; one consistent shape for every tenant.</strong>",
    district_pin="kpe-bench03", district_label="Composition Workbench",
    sections=[
        Section(eyebrow="Section 1.1 · platform-as-API",
            h2="K8s control plane for cloud resources",
            body_html="""    <p>Crossplane runs in your cluster as a CRD-driven control plane for external resources. Apply a CR; Crossplane reconciles in the cloud. <em>kubectl is the API for everything</em> — cloud + SaaS + on-prem.</p>
    <p>Compared to Terraform: Crossplane is <em>continuous reconciliation</em> (drift auto-corrected), runs <em>in-cluster</em> (no separate state file), uses <em>K8s primitives</em> (RBAC, audit, GitOps). Trade: K8s as the runtime; learning curve for non-K8s shops.</p>"""),
        Section(eyebrow="Section 1.2 · XRD + Composition",
            h2="Define the user API + render logic",
            body_html="""    <p><strong>XRD (CompositeResourceDefinition)</strong>: declares a user-facing CRD (e.g., <code>XPostgresInstance</code>) with schema + claim type (namespaced version). Tenants create Claims; XR controller reconciles.</p>
    <p><strong>Composition</strong>: per XRD, declares how to render to Provider resources. e.g., XPostgresInstance Composition renders: AWS RDSInstance + DBSubnetGroup + IAMRole + KMS Key + Backup config. Tenants see one CR; platform composes the stack.</p>
    <p><strong>Multiple Compositions per XRD</strong>: \"AWS-RDS Postgres\" + \"Azure-Database-Postgres\" + \"on-prem-CloudNativePG\" — same user-facing XRD; cloud-specific render logic. Selector at Claim picks Composition.</p>"""),
        Section(eyebrow="Section 1.3 · Functions",
            h2="Pluggable composition logic — KCL / Pkl / Go / patch-and-transform",
            body_html="""    <p><strong>Functions</strong> (Crossplane v1.14+) replace legacy patch-and-transform with a pluggable pipeline. Each Function is a container; Composition declares a list of Function calls; each transforms the desired state.</p>
    <p>Common Functions: <strong>function-go-templating</strong> (Go templates), <strong>function-kcl</strong> (KCL — typed config language), <strong>function-pkl</strong> (Pkl — Apple\'s config language), <strong>function-patch-and-transform</strong> (legacy YAML patches), <strong>function-cel</strong> (CEL expressions).</p>
    <p>Pick by team\'s ergonomics. KCL + Pkl typed; Go templating familiar; CEL expression-style. Functions are versioned + tested independently."""),
        Section(eyebrow="Section 1.4 · Providers + ConfigurationPackages",
            h2="Provider ecosystem + shareable bundles",
            body_html="""    <p><strong>Providers</strong>: per-platform controllers. <em>provider-upjet-aws</em> + <em>provider-upjet-azure</em> + <em>provider-upjet-gcp</em> ship Terraform-resource-equivalent CRDs. <em>provider-kubernetes</em> + <em>provider-helm</em> for in-cluster. <em>provider-github</em>, <em>provider-vault</em>, <em>provider-cloudflare</em>, etc. for SaaS.</p>
    <p>Provider auth via ProviderConfig: cloud creds (IRSA / Workload Identity for least-privilege) or static creds.</p>
    <p><strong>ConfigurationPackages</strong>: bundle XRDs + Compositions + Function references + Provider references in one OCI artifact. <code>crossplane xpkg push registry.example.com/my-platform:v1.0</code>. Install on any cluster: same platform shape everywhere. <em>Shareable platforms across teams + companies</em>.</p>"""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="What\'s Crossplane vs Terraform fundamental difference?",
            options=[("Crossplane is faster.", False), ("Crossplane is continuous reconciliation in-cluster; Terraform is one-shot apply.", True), ("Terraform supports more clouds.", False)],
            feedback="Crossplane reconciles continuously (drift auto-corrected); Terraform applies once + walks away. Different operational model."),
        3: PauseCheck(question="What does ConfigurationPackage enable?",
            options=[("Compression.", False), ("Shareable XRDs + Compositions + Functions as one OCI artifact installable on any cluster.", True), ("Faster Provider sync.", False)],
            feedback="Configuration packages bundle the platform shape for distribution. Same package on every cluster = same platform."),
    },
    before_after_before='<p>Pre-Crossplane: Terraform per team or manual cloud console. Drift constant. Tenant onboarding bespoke. State files everywhere.</p>',
    before_after_after='<p>Crossplane v2: XRDs are the API; Compositions + Functions render to Providers; ConfigurationPackages distribute the platform. Tenants <code>kubectl apply</code> a Claim; consistent infra ships.</p>',
    before_after_caption='<p class="ba-caption"><em>Platform-as-API. Tenants consume; platform team owns the API contract.</em></p>',
    analogy_intro_html='''<p>The Composition Workbench is where the Master Craftsperson designs reusable assemblies. The blueprint (XRD) declares what the customer asks for. The assembly instructions (Composition + Functions) explain how to combine standard parts (Providers) to fulfill the order. The whole assembly ships as a sealed package (ConfigurationPackage) to other workshops; install once, build the same assembly anywhere.</p>''',
    translation_rows=[
        ("Customer order form", "XRD (CompositeResourceDefinition)"),
        ("Customer order", "Claim"),
        ("Assembly instructions", "Composition"),
        ("Pluggable assembly steps", "Functions (KCL / Pkl / Go / patch-and-transform / CEL)"),
        ("Standard parts catalog", "Providers (provider-upjet-aws / azure / gcp / SaaS)"),
        ("Sealed package", "ConfigurationPackage (OCI artifact)"),
        ("Workshop installation", "crossplane xpkg install"),
    ],
    analogy_stops="A real assembly is one-time; Crossplane reconciles continuously — drift is auto-corrected (sometimes surprising if a human edited the resource directly).",
    eli5="A workbench where the master writes assembly instructions for the most-asked customer orders. Customer says \"I want this kind of thing\"; the workbench reads the order; combines standard parts; ships the result. The whole workbench can be sealed + sent to another shop.",
    eli10="<strong>XRD</strong>: user-facing CRD + Claim type. <strong>Composition</strong>: render logic per XRD; selectable per Claim. <strong>Functions</strong>: pluggable pipeline (KCL / Pkl / Go templates / patch-and-transform / CEL). <strong>Providers</strong>: cloud + SaaS controllers (Upjet-generated for AWS/Azure/GCP). <strong>ConfigurationPackage</strong>: OCI-distributed bundle.",
    scenarios=[
        Scenario(name="XPostgresInstance — one CRD, three clouds", body="Platform ships XPostgresInstance XRD + 3 Compositions (AWS RDS / Azure Database / GCP CloudSQL). Tenant Claims pick cloud via label; consistent backup + IAM + monitoring across all three."),
        Scenario(name="XTenantNamespace — onboarding", body="XTenantNamespace XRD ships namespace + RBAC + NetPol + Quota + service-catalog entry. Tenant Claim form-fillable; new tenant ready in 5 minutes."),
        Scenario(name="ConfigurationPackage distributed across business units", body="Platform team ships one ConfigurationPackage (XPostgres + XTenantNamespace + XBucket); 8 BU clusters install; same shape everywhere."),
        Scenario(name="Outage — drift auto-corrected", body="A human edited an RDS instance via console; Crossplane saw drift; reconciled back to spec. Postmortem: enable manual-edit detection alerts; train teams that Crossplane is source of truth."),
    ],
    misconceptions=[
        Misconception(myth="\"Crossplane replaces Terraform.\"", truth="Different model. Crossplane = continuous reconciliation in-cluster; Terraform = one-shot apply. Many teams use both: Crossplane for runtime cloud + SaaS resources; Terraform for one-shot bootstrap (VPC / cluster itself)."),
        Misconception(myth="\"Functions are too new.\"", truth="Crossplane v1.14+ Functions are GA + recommended. Legacy patch-and-transform still supported but Functions are more pluggable + better tested."),
        Misconception(myth="\"Providers + Compositions are too low-level for tenants.\"", truth="That\'s the point. Tenants don\'t see Providers or Compositions; they see XRDs (high-level API). Platform team owns the low-level mapping."),
    ],
    flashcards=[
        Flashcard(front="Crossplane four core concepts?", back="<strong>XRD</strong> (CompositeResourceDefinition; user-facing CRD + Claim), <strong>Composition</strong> (render logic), <strong>Functions</strong> (pluggable pipeline), <strong>Providers</strong> (cloud + SaaS controllers)."),
        Flashcard(front="What does an XRD declare?", back="The user-facing CRD schema + Claim type. Tenants create Claims; XR controller reconciles per Composition."),
        Flashcard(front="Composition Function options?", back="<strong>function-kcl</strong>, <strong>function-pkl</strong>, <strong>function-go-templating</strong>, <strong>function-patch-and-transform</strong>, <strong>function-cel</strong>. Pluggable; pick per ergonomics."),
        Flashcard(front="Provider auth pattern?", back="ProviderConfig CR with credentials reference. Best practice: IRSA / Workload Identity for least-privilege; not static cloud keys."),
        Flashcard(front="What\'s a ConfigurationPackage?", back="OCI artifact bundling XRDs + Compositions + Function refs + Provider refs. Distributed via OCI registry; installable on any cluster."),
        Flashcard(front="Crossplane vs Terraform — when each?", back="<strong>Terraform</strong>: one-shot bootstrap (VPC / cluster). <strong>Crossplane</strong>: continuous reconciliation of runtime resources (DBs / queues / IAM / SaaS). Often used together."),
        Flashcard(front="Multiple Compositions per XRD — what enables?", back="Same user-facing API across clouds (XPostgresInstance → AWS RDS / Azure Database / GCP CloudSQL). Selector at Claim picks the right Composition."),
        Flashcard(front="Crossplane drift handling?", back="Continuous reconciliation. Manual cloud-console edits are detected + reverted to spec. Surprising if not expected; alarm on drift events for visibility."),
    ],
    quizzes=[
        Quiz(prompt="Build XPostgresInstance for AWS + Azure with backup + monitoring + IAM. Walk steps.",
            answer="(1) Define <strong>XRD XPostgresInstance</strong> with schema (size, engine version, backup retention, monitoring level). (2) Write <strong>Composition for AWS</strong>: function-kcl pipeline that renders RDSInstance + DBSubnetGroup + IAMRole + KMS Key + AWS Backup BackupVault. (3) Write <strong>Composition for Azure</strong>: similar pipeline rendering Azure Database for PostgreSQL + Backup + Monitor + KMS. (4) <strong>ProviderConfig</strong> for each (IRSA / Workload Identity). (5) <strong>Tenant Claim</strong>: <code>apiVersion: db.example.com/v1; kind: PostgresInstance; spec: {size: 50Gi, engine: 15.x, providerSelector: {matchLabels: {cloud: aws}}}</code>. (6) <strong>Bundle</strong>: ConfigurationPackage shipped to all clusters."),
        Quiz(prompt="Drift auto-correction surprised a team that manually edited an RDS instance. Walk the runbook.",
            answer="(1) <strong>Detect</strong>: Crossplane events show \"reconciliation revert\" on the resource. (2) <strong>Communicate</strong>: alarm to team Slack; manual edits are not the change path. (3) <strong>Path</strong>: change the spec via Claim or Composition; Crossplane will reconcile. (4) <strong>Education</strong>: cluster runbook says \"Crossplane is source of truth; manual changes will revert.\" (5) <strong>Optional</strong>: enable Crossplane\'s drift-tolerance flag for resources where manual changes are intentional."),
        Quiz(prompt="Leadership says: \"Terraform works. Don\'t add Crossplane.\" Defend.",
            answer="\"<strong>Crossplane + Terraform aren\'t either-or — they coexist.</strong> Three reasons we adopt Crossplane: (1) <strong>Continuous reconciliation</strong>: drift auto-corrected; not deferred until next terraform apply. (2) <strong>Tenant self-service</strong>: tenants kubectl apply Claims; no Terraform expertise required; XRD is the API. (3) <strong>Composition reuse</strong>: ConfigurationPackages share platform shape across clusters / BUs. Terraform modules don\'t share like this. <strong>Where Terraform stays</strong>: cluster + VPC bootstrap (one-shot setup). <strong>Where Crossplane wins</strong>: tenant-facing runtime resources. <strong>Net</strong>: Crossplane gives leverage Terraform can\'t; both have a place.\"", cyoa=True, cyoa_tag="how the platform engineer defended Crossplane"),
    ],
    glossary=[
        GlossaryItem(name="Crossplane", definition="K8s control plane for cloud + SaaS. CNCF Incubating. Continuous reconciliation."),
        GlossaryItem(name="XRD (CompositeResourceDefinition)", definition="User-facing CRD schema + Claim type. The API tenants consume."),
        GlossaryItem(name="Composition", definition="Per-XRD render logic — Functions pipeline emitting Provider resources."),
        GlossaryItem(name="Function (Crossplane)", definition="Pluggable composition step. KCL / Pkl / Go templates / patch-and-transform / CEL."),
        GlossaryItem(name="Provider", definition="Cloud / SaaS controller (provider-upjet-aws, provider-azure, provider-vault, etc.). Reconciles external resources."),
        GlossaryItem(name="Claim", definition="Tenant\'s namespaced CR matching an XRD. \"Customer order.\""),
        GlossaryItem(name="ConfigurationPackage", definition="OCI bundle of XRDs + Compositions + Function refs + Provider refs. Distribute platform shape."),
        GlossaryItem(name="Upjet", definition="Crossplane code generator producing Providers from Terraform Provider schemas."),
        GlossaryItem(name="ProviderConfig", definition="Per-Provider CR with auth (IRSA / Workload Identity / static)."),
        GlossaryItem(name="drift reconciliation", definition="Crossplane reverts manual edits to match spec; alarm + educate teams."),
    ],
    recap_lead="Crossplane v2: XRDs are the platform API; Compositions + Functions render; Providers reconcile cloud/SaaS; ConfigurationPackages distribute. Continuous reconciliation; tenant self-service via Claims.",
    recap_next='<strong>Next — P4: Argo CD ApplicationSets + OPA / Kyverno guardrails.</strong> Fleet GitOps + policy gates.',
)
