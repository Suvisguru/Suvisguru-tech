"""K-OCP O5 — Operators and OLM (CatalogSources, Subscriptions, InstallPlans, CSVs, channels, dependencies)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OpenShift Operator Hub + OLM lifecycle.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Operator Hub — OLM lifecycle pipeline</text>
  <rect x="40" y="65" width="125" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="102" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">CatalogSource</text>
  <text x="102" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">Red Hat Operators</text>
  <text x="102" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">Certified Operators</text>
  <text x="102" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">Community Operators</text>
  <text x="102" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">redhat-marketplace</text>
  <rect x="180" y="65" width="125" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="242" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Subscription</text>
  <text x="242" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">channel: stable</text>
  <text x="242" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">approval: Automatic</text>
  <text x="242" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">vs Manual</text>
  <text x="242" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">installPlanApproval</text>
  <rect x="320" y="65" width="125" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="382" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">InstallPlan</text>
  <text x="382" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">resolves dependencies</text>
  <text x="382" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">creates CSVs</text>
  <text x="382" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">RBAC + CRDs</text>
  <text x="382" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">manual approval gate</text>
  <rect x="460" y="65" width="125" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="522" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">CSV</text>
  <text x="522" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">ClusterServiceVersion</text>
  <text x="522" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">deploys operator</text>
  <text x="522" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">phases: Pending →</text>
  <text x="522" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">InstallReady → Succeeded</text>
  <rect x="600" y="65" width="120" height="125" rx="10" fill="#E8B547" stroke="#3F4A5E"/>
  <text x="660" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#5A4F45">OperatorGroup</text>
  <text x="660" y="103" text-anchor="middle" font-size="9" fill="#5A4F45">scope: AllNamespaces</text>
  <text x="660" y="118" text-anchor="middle" font-size="9" fill="#5A4F45">vs OwnNamespace</text>
  <text x="660" y="133" text-anchor="middle" font-size="9" fill="#5A4F45">vs SingleNamespace</text>
  <text x="660" y="148" text-anchor="middle" font-size="9" fill="#5A4F45">required per Project</text>
</svg>"""


LESSON = LessonSpec(
    num="05", title_short="Operators &amp; OLM",
    title_full="O5 · Operators and OLM (Operator Hub + CatalogSources + Subscriptions + InstallPlans + CSVs + OperatorGroups)",
    title_html="K-OCP O5 · Operators and OLM",
    module_eyebrow="Module O5 · the Operator Hub",
    hero_sub_html='OperatorHub-everywhere is the OCP installation paradigm. <strong>OLM</strong> orchestrates: <strong>CatalogSource</strong> (Red Hat / Certified / Community / Marketplace) → <strong>Subscription</strong> (channel + approval mode) → <strong>InstallPlan</strong> (resolves deps + RBAC + CRDs) → <strong>ClusterServiceVersion (CSV)</strong> (deploys the operator). <strong>OperatorGroup</strong> defines scope (AllNamespaces / OwnNamespace / SingleNamespace). <strong>Channels</strong> (stable / fast / preview) + <strong>manual vs automatic approval</strong>. Operator dependencies + broken-operator recovery. Certified vs Community vs custom operators.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"OperatorHub install of cert-manager Operator stuck in InstallReady; no progress for 2 hours.\"</em> The InstallPlan needs manual approval (you set <code>installPlanApproval: Manual</code> on the Subscription). You forgot to approve. Plus the OperatorGroup in the namespace targets AllNamespaces but the operator only supports OwnNamespace — install would fail anyway. Plus a dependent operator (Red Hat Cert Manager) is on a channel that\'s in conflict. <em>You don\'t know any of this.</em> Today\'s lesson: how OLM actually installs an operator, and what to do when each step gets stuck.",
    stamp_html="<strong>OLM lifecycle: CatalogSource → Subscription (channel + approval) → InstallPlan (deps + RBAC) → CSV (deploys operator). OperatorGroup defines scope. Pick channel by stability tolerance; pick approval mode by upgrade discipline; resolve dependency conflicts before installing.</strong>",
    district_pin="ko-bay05", district_label="Operator Hub",
    sections=[
        Section(eyebrow="Section 1.1 · Operator Hub + CatalogSources", h2="Operator Hub + CatalogSources",
            body_html="""    <p><strong>OperatorHub</strong> is the OCP web console\'s view of installable operators. Sourced from <strong>CatalogSources</strong>:</p>
    <ul>
      <li><strong>Red Hat Operators</strong> — supported by Red Hat. Production-ready.</li>
      <li><strong>Certified Operators</strong> — third-party (IBM, NetApp, Crunchy, etc.) with Red Hat certification.</li>
      <li><strong>Community Operators</strong> — community-maintained. Best-effort.</li>
      <li><strong>Red Hat Marketplace</strong> — purchasable operators with billing integration.</li>
      <li><strong>Custom CatalogSource</strong> — your internal catalog (hosted in your private registry; supports air-gapped + curated installs).</li>
    </ul>
    <p>Each CatalogSource is a Pod running a registry that exposes a gRPC API; OLM queries it to list operators + manifests + dependencies.</p>
    <p>For air-gapped clusters: mirror the catalog images via <code>oc-mirror</code>; deploy a private CatalogSource pointing at the internal mirror.</p>"""),
        Section(eyebrow="Section 1.2 · Subscription + InstallPlan + CSV", h2="Subscription + InstallPlan + CSV — the install pipeline",
            body_html="""    <p><strong>Subscription</strong> CR — declares: which operator (package name), from which CatalogSource, on which channel, with what approval mode (Automatic / Manual). One Subscription per operator per Project.</p>
    <p><strong>OLM workflow:</strong>
    <ol>
      <li>You create a Subscription.</li>
      <li>OLM reads the channel\'s current head + dependencies; creates an <strong>InstallPlan</strong>.</li>
      <li>If <code>installPlanApproval: Automatic</code>, InstallPlan is auto-approved + executed. If Manual: human runs <code>oc patch installplan ... --type merge -p \'{"spec":{"approved":true}}\'</code>.</li>
      <li>InstallPlan creates the <strong>ClusterServiceVersion (CSV)</strong> + dependencies + CRDs + RBAC.</li>
      <li>CSV phases: <em>Pending → InstallReady → Installing → Succeeded</em> (or Failed). Operator Pod runs.</li>
      <li>For upgrades: when CatalogSource publishes a new CSV in the channel, OLM creates a new InstallPlan; same approval flow applies.</li>
    </ol>
    <p><strong>Channel choice:</strong> <em>stable</em> (production), <em>fast</em> (latest GA, faster cadence), <em>preview</em> (pre-release / candidate), version-pinned channels (e.g. <code>4.14</code>). Operator authors define the channels.</p>
    <p><strong>Approval mode:</strong>
    <ul>
      <li><strong>Automatic</strong> — OLM applies new versions when they appear in the channel. Use for non-prod or operators with great backward compatibility.</li>
      <li><strong>Manual</strong> — OLM creates the InstallPlan but pauses; human approves. Use for prod / regulated.</li>
    </ul>"""),
        Section(eyebrow="Section 1.3 · OperatorGroup + scope", h2="OperatorGroup + scope (AllNamespaces / SingleNamespace / OwnNamespace)",
            body_html="""    <p><strong>OperatorGroup</strong> defines the namespaces the operator watches + manages. Required: every Project that hosts an OLM-installed operator must have an OperatorGroup.</p>
    <p><strong>Scope modes:</strong>
    <ul>
      <li><strong>AllNamespaces</strong> — operator watches every namespace cluster-wide. Default for openshift-operators namespace. For platform-wide operators (e.g. cert-manager Operator).</li>
      <li><strong>OwnNamespace</strong> — operator watches only the namespace it\'s installed in. For Project-scoped operators (e.g. one Postgres Operator per tenant).</li>
      <li><strong>SingleNamespace</strong> — operator installed in one namespace, watches another. Less common.</li>
      <li><strong>MultiNamespace</strong> — operator watches multiple specific namespaces. Less common.</li>
    </ul>
    <p>Operator authors declare which scopes their operator supports (<code>installModes</code> in CSV). If your OperatorGroup mode doesn\'t match a supported installMode, the install fails. <em>Check the operator\'s docs before creating the OperatorGroup.</em></p>
    <p><strong>openshift-operators</strong> is the well-known AllNamespaces OperatorGroup namespace; many cluster-wide operators install there.</p>"""),
        Section(eyebrow="Section 1.4 · dependencies + recovery + custom operators",
            h2="Dependencies + broken-operator recovery + custom / certified operators",
            body_html="""    <p><strong>Operator dependencies:</strong> when Operator A requires Operator B, OLM\'s InstallPlan installs B first. If B is unavailable in any catalog, A\'s install fails. <em>The most common cause of \"my operator won\'t install\" is unmet dependencies.</em></p>
    <p>Use <code>oc describe installplan</code> to see required + resolved deps. <code>oc get packagemanifest -A</code> lists all available operators across catalogs.</p>
    <p><strong>Broken-operator recovery:</strong>
    <ul>
      <li>CSV in <em>Failed</em> state: <code>oc describe csv &lt;name&gt;</code> for failure reason; common causes are missing CRD, RBAC denial, image pull failure, dependency conflict.</li>
      <li>Stuck Subscription: delete + recreate; OLM rebuilds InstallPlan.</li>
      <li>CSV upgrade stuck mid-flight: <code>oc delete csv &lt;old-csv&gt;</code>; OLM\'s next reconcile installs new CSV cleanly.</li>
      <li>Last resort: uninstall (delete Subscription + CSV) then reinstall fresh.</li>
    </ul>
    <p><strong>Custom operators:</strong> internal teams build operators with Operator SDK (Go, Ansible, or Helm-based). Publish to your custom CatalogSource. Same OLM lifecycle as Red Hat Operators.</p>
    <p><strong>Certified Operators</strong> are vendor-supported (IBM Cloud Pak, Crunchy Postgres, NetApp Trident, Confluent, etc.). <strong>Community Operators</strong> are best-effort. <em>For prod, prefer Red Hat or Certified.</em></p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A team installs an Operator. CSV stays at \"InstallReady.\" What\'s the most likely cause?",
        options=[("Image pull failure.", False),
            ("<code>installPlanApproval: Manual</code> — InstallPlan needs human approval before CSV proceeds. Run <code>oc patch installplan ... --type merge -p \'{\"spec\":{\"approved\":true}}\'</code>.", True),
            ("CRD conflict.", False)],
        feedback="InstallReady = waiting on InstallPlan approval. Auto-approval makes this transparent; Manual requires explicit human gate.",
    )},
    before_after_before='<p>Pre-OLM K8s operator install was Helm + custom RBAC + manual CRD apply per operator. No dependency resolution. No upgrade gates. No cluster-wide visibility into installed operators. Each team\'s operator drift was their own problem; cluster admins had no inventory.</p>',
    before_after_after='<p>OLM standardises operator lifecycle: <strong>CatalogSources</strong> + <strong>Subscriptions</strong> + <strong>InstallPlans</strong> + <strong>CSVs</strong> + <strong>OperatorGroups</strong>. <strong>Channels</strong> for upgrade cadence; <strong>approval mode</strong> for upgrade discipline; <strong>dependency resolution</strong> built in; <strong>cluster-wide inventory</strong> via <code>oc get csv -A</code>; <strong>certified + community + custom</strong> CatalogSources.</p>',
    before_after_caption='<p class="ba-caption"><em>OLM is the operator-of-operators. Once you understand its CR pipeline, every OperatorHub install becomes predictable.</em></p>',
    analogy_intro_html='''<p>The <strong>Operator Hub</strong> at K-Foundry is where you order specialty machinery. Four catalogs sit on the counter: Red Hat\'s officially-supported parts, Certified third-party parts (IBM, NetApp, etc.), Community parts (best-effort), and the Marketplace (purchasable parts).</p>
    <p>You fill out a <strong>Subscription order form</strong>: which part, from which catalog, what version channel, do I want auto-shipping or hand-approval. The Hub creates an <strong>InstallPlan invoice</strong> listing dependencies + RBAC + CRDs that must be installed first. With auto-approval, the invoice processes immediately; with manual approval, you sign off before any work begins.</p>
    <p>Once approved, the <strong>ClusterServiceVersion (CSV) work-order</strong> deploys the operator. The CSV walks through phases: Pending → InstallReady → Installing → Succeeded. Pod is running; operator is reconciling.</p>
    <p>The <strong>OperatorGroup</strong> is the operator\'s territory permit: AllNamespaces (it patrols the whole foundry) or OwnNamespace (it patrols only one bay). Match the operator\'s declared installModes; the wrong territory permit causes silent install failures.</p>''',
    translation_rows=[("Catalog counter", "CatalogSource (Red Hat / Certified / Community / Marketplace / custom)"),
        ("Subscription order form", "Subscription CR"),
        ("Channel selection", "stable / fast / preview / version-pinned"),
        ("Auto-shipping vs hand-approval", "installPlanApproval: Automatic vs Manual"),
        ("InstallPlan invoice", "InstallPlan CR (lists deps + RBAC + CRDs)"),
        ("Hand-approval signature", "<code>oc patch installplan ... approved:true</code>"),
        ("Work order", "ClusterServiceVersion (CSV)"),
        ("CSV phases", "Pending → InstallReady → Installing → Succeeded (or Failed)"),
        ("Territory permit", "OperatorGroup"),
        ("Cluster-wide patrol", "AllNamespaces scope"),
        ("Single-bay patrol", "OwnNamespace scope"),
        ("Foundry parts inventory", "<code>oc get csv -A</code>"),
        ("Internal-parts catalog", "Custom CatalogSource (private registry)"),
        ("Specialty supported parts", "Certified Operators"),
        ("Best-effort parts", "Community Operators")],
    analogy_stops="A real catalog has fixed inventory; OperatorHub is a live gRPC service with rolling updates. Operator dependency conflicts are a real failure mode the catalog metaphor doesn\'t capture.",
    eli5="The Operator Hub is a parts catalog. You fill an order form (Subscription), the office creates an invoice (InstallPlan) listing what else has to be ordered first, you approve it, then the work order (CSV) installs the part.",
    eli10="OLM = OperatorHub-everywhere lifecycle: CatalogSource (Red Hat/Certified/Community/Marketplace/custom) → Subscription (channel + approval) → InstallPlan (dependencies + RBAC + CRDs) → CSV (deploys operator). OperatorGroup defines scope (AllNamespaces / OwnNamespace / SingleNamespace / MultiNamespace) and must match the operator\'s declared installModes. CSV phases: Pending → InstallReady → Installing → Succeeded. Manual approval mode pauses at InstallReady for human sign-off; Automatic auto-applies. Use Red Hat or Certified for prod; Community for non-prod.",
    scenarios=[
        Scenario(name="Bank — manual approval + custom CatalogSource",
            body="A regulated bank uses only operators from their internal CatalogSource (mirrored from Red Hat + curated by the platform team). Every Subscription has <code>installPlanApproval: Manual</code>. Operator upgrades require change-control approval; platform engineer runs <code>oc patch installplan</code> after approval. <em>Compliance-clean upgrade trail.</em>"),
        Scenario(name="Multi-tenant SaaS — OwnNamespace per-tenant Postgres Operator",
            body="A SaaS where each tenant gets their own Postgres database. Crunchy Data Postgres Operator installed per-tenant Project with OwnNamespace OperatorGroup. Tenant isolation: each tenant\'s operator only manages their own Postgres CRs. <em>Operator-per-tenant pattern.</em>"),
        Scenario(name="Dependency hell — cert-manager required Compliance Operator first",
            body="Team installs cert-manager Operator. InstallPlan fails: depends on Compliance Operator v1.2+ (for CRD compatibility), and the channel pinned to v1.1 in the cluster. Fix: change Compliance Operator Subscription channel to <code>stable</code> (which has v1.2+); cert-manager InstallPlan succeeds on next reconcile. <em>OLM dependency resolution surfaces these conflicts; <code>oc describe installplan</code> tells you.</em>"),
        Scenario(name="Stuck CSV — recovered by deleting + reinstalling Subscription",
            body="An operator CSV stuck in Failed for 3 days due to CRD-conflict drama. Recovery: <code>oc delete subscription &lt;name&gt;</code> + <code>oc delete csv &lt;name&gt;</code> + manually clean orphaned CRDs (rare). Reinstall Subscription; clean CSV install succeeds. <em>Postmortem: documented recovery runbook.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"All Operators install the same way.\"",
            truth="Operators have <strong>different supported installModes</strong>: AllNamespaces, SingleNamespace, OwnNamespace, MultiNamespace. The OperatorGroup must match. Some operators don\'t support every mode. Read the operator\'s docs / packagemanifest to know which modes work."),
        Misconception(myth="\"Manual approval = no auto-upgrades = safer always.\"",
            truth="Manual approval gives you control over <em>when</em> to upgrade — but you must actually approve, otherwise InstallPlans pile up and the operator drifts behind security patches. <em>Manual is safer only if you have a process to approve regularly.</em> If unmanned, automatic with a known channel (stable) may be safer in practice."),
        Misconception(myth="\"Community Operators are fine for production.\"",
            truth="Community Operators are <strong>best-effort</strong> — no Red Hat support contract, no SLA on bug fixes, may have abandoned upstreams. For prod, prefer <strong>Red Hat Operators</strong> or <strong>Certified Operators</strong>. Use Community for evaluation / non-prod or when the only available option."),
    ],
    flashcards=[
        Flashcard(front="Five OLM CRs in the install pipeline?", back="<strong>CatalogSource</strong> (operator catalog), <strong>Subscription</strong> (declares operator+channel+approval), <strong>InstallPlan</strong> (resolves deps+RBAC+CRDs), <strong>ClusterServiceVersion (CSV)</strong> (deploys operator), <strong>OperatorGroup</strong> (defines scope)."),
        Flashcard(front="Four OperatorGroup scope modes?", back="<strong>AllNamespaces</strong> (cluster-wide), <strong>OwnNamespace</strong> (only the install namespace), <strong>SingleNamespace</strong> (one specific namespace), <strong>MultiNamespace</strong> (multiple). Must match operator\'s declared installModes."),
        Flashcard(front="CSV phases?", back="Pending → InstallReady → Installing → Succeeded (or Failed). InstallReady = waiting for approval (Manual mode); auto-approval makes this transparent."),
        Flashcard(front="Subscription channels — pick by what?", back="By upgrade cadence + stability appetite: <strong>stable</strong> (prod), <strong>fast</strong> (latest GA), <strong>preview</strong> (pre-release), or version-pinned (e.g. 4.14). Operator authors define the channels."),
        Flashcard(front="Five CatalogSource types?", back="<strong>Red Hat Operators</strong> (Red Hat-supported), <strong>Certified Operators</strong> (third-party with RH certification), <strong>Community Operators</strong> (best-effort), <strong>Red Hat Marketplace</strong> (purchasable + billing), <strong>custom CatalogSource</strong> (internal mirror)."),
        Flashcard(front="Manual vs Automatic approval — when use which?", back="<strong>Manual</strong>: regulated / change-control workflows; you have a process to approve InstallPlans regularly. <strong>Automatic</strong>: non-prod or operators with strong backward compatibility; saves human attention."),
        Flashcard(front="What does OLM dependency resolution do?", back="When Operator A requires Operator B, OLM\'s InstallPlan installs B first. If B is unavailable in any CatalogSource, A\'s install fails. <code>oc describe installplan</code> shows required + resolved deps."),
        Flashcard(front="Recovery for stuck CSV?", back="(1) Read <code>oc describe csv</code> for failure reason. (2) Delete Subscription + CSV; reinstall. (3) For dependency issues: change channels / CatalogSources to resolve conflict. (4) Last resort: clean up orphaned CRDs (rare; requires care)."),
    ],
    quizzes=[
        Quiz(prompt="An operator install is stuck \"InstallReady\" for hours. Walk through diagnosis.",
            answer="(1) <code>oc get subscription &lt;name&gt;</code> — note <code>installPlanApproval</code> + <code>currentCSV</code>. (2) <code>oc get installplan</code> — find the InstallPlan with <code>spec.approved: false</code>. (3) <code>oc patch installplan &lt;name&gt; --type merge -p \'{\"spec\":{\"approved\":true}}\'</code> approves it. (4) Watch CSV: <code>oc get csv -w</code> — should progress through Installing → Succeeded. (5) If still stuck: <code>oc describe csv</code> for status conditions; common causes are missing CRD permissions, image pull failures, or dependency conflicts."),
        Quiz(prompt="A team needs Postgres Operator per tenant Project. How do they install + scope?",
            answer="Per Project: (1) Create the Project. (2) Create an <strong>OperatorGroup</strong> in that Project with <code>spec.targetNamespaces: [&lt;project&gt;]</code> (OwnNamespace mode). (3) Create the Subscription in that Project pointing at the Postgres Operator (e.g., Crunchy) on a stable channel. (4) OLM installs the operator + CRDs into the Project; the operator only watches/manages CRs in that Project. <em>Per-tenant operator with strict isolation.</em> Verify the operator\'s installModes supports OwnNamespace before this works."),
        Quiz(prompt="Saturday. The CTO Slacks: \"We need Operator X installed in 30 minutes — board demo.\" You check OperatorHub: it\'s a Community Operator, dependency on Operator Y at version pinned to a channel that\'s no longer published. What do you do?",
            answer="(1) <strong>Don\'t install Community Operator in prod for a board demo</strong> — risk of failed install + worse demo. (2) Quick options: (a) Find a Red Hat or Certified equivalent operator that does the same job; install that. (b) Install Community Operator in a temporary scratch Project, demo from there, accept the demo cluster gets thrown away. (c) Pin the dep operator to a manually-mirrored CatalogSource pointing at the older version (custom CatalogSource); risky for time-pressure. (3) Communicate honest constraints to the CTO: \"the supported path takes 2 weeks; the demo path is X with these caveats.\" Don\'t install Community-on-Community-on-conflict at 3pm before a 4pm demo. <em>Operator dependency hell at the wrong moment is the recipe for a failed demo.</em>",
            cyoa=True, cyoa_tag="how the platform engineer handled the demo request"),
    ],
    glossary=[
        GlossaryItem(name="OperatorHub", definition="OCP web console view of installable operators sourced from CatalogSources."),
        GlossaryItem(name="CatalogSource", definition="Pod running a registry exposing operators via gRPC. Red Hat / Certified / Community / Marketplace / custom."),
        GlossaryItem(name="Subscription", definition="CR declaring operator + CatalogSource + channel + approval mode. One per operator per Project."),
        GlossaryItem(name="InstallPlan", definition="OLM-generated CR listing required CSVs + deps + CRDs + RBAC. Manual mode requires human approval."),
        GlossaryItem(name="ClusterServiceVersion (CSV)", definition="OLM CR that deploys the operator + declares its capabilities + dependencies + supported installModes. Phases: Pending → InstallReady → Installing → Succeeded."),
        GlossaryItem(name="OperatorGroup", definition="CR defining the namespaces an operator watches/manages. Modes: AllNamespaces, OwnNamespace, SingleNamespace, MultiNamespace."),
        GlossaryItem(name="installModes", definition="Operator-declared modes the operator supports (AllNamespaces, OwnNamespace, etc.). OperatorGroup mode must match."),
        GlossaryItem(name="Channel", definition="Operator update stream — stable, fast, preview, or version-pinned. Author-defined."),
        GlossaryItem(name="installPlanApproval", definition="Subscription field: Automatic or Manual. Manual pauses at InstallReady for human sign-off."),
        GlossaryItem(name="Red Hat Operators", definition="CatalogSource of Red Hat-supported operators."),
        GlossaryItem(name="Certified Operators", definition="Third-party operators with Red Hat certification (IBM, NetApp, Crunchy, Confluent, etc.)."),
        GlossaryItem(name="Community Operators", definition="Best-effort community-maintained operators. No Red Hat support."),
        GlossaryItem(name="oc-mirror + custom CatalogSource", definition="Disconnected pattern — mirror catalog images to internal registry; private CatalogSource serves them."),
    ],
    recap_lead='OLM lifecycle: CatalogSource → Subscription → InstallPlan → CSV. OperatorGroup defines scope. Channels + approval mode are the upgrade-discipline knobs.',
    recap_next='<strong>Next — O6: Workloads and Developer Experience.</strong> Source-to-Image (S2I) + BuildConfig + ImageStream + Build; DeploymentConfig (legacy) vs Deployment; Templates; OpenShift Pipelines (Tekton); OpenShift GitOps (Argo CD); Serverless (Knative); Service Mesh (Istio); Dev Spaces (Eclipse Che); internal registry; Helm in OCP; web console workflows.',
)
