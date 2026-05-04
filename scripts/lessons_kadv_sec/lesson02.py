"""K-ADV-SEC S2 — RBAC design at scale."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="RBAC binding chain — subject + role + binding + audit.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Authorization Desk · K-Citadel — three things bind every authorisation</text>
  <rect x="40" y="70" width="170" height="100" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Subject</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">User · Group · ServiceAccount</text>
  <text x="125" y="128" text-anchor="middle" font-size="9" fill="#FBF1D6">via OIDC / SA token</text>
  <text x="125" y="152" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">who is asking</text>
  <rect x="225" y="70" width="220" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="335" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Role / ClusterRole</text>
  <text x="335" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">verbs (get/list/create/delete)</text>
  <text x="335" y="128" text-anchor="middle" font-size="9" fill="#FBF1D6">on resources (Pods/Deployments/...)</text>
  <text x="335" y="152" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">what is permitted</text>
  <rect x="460" y="70" width="260" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="590" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">RoleBinding / ClusterRoleBinding</text>
  <text x="590" y="108" text-anchor="middle" font-size="9" fill="#1F2433">in this namespace (or cluster)</text>
  <text x="590" y="128" text-anchor="middle" font-size="9" fill="#1F2433">subject ←→ role</text>
  <text x="590" y="152" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">where + how it binds</text>
</svg>"""


LESSON = LessonSpec(
    num="02",
    title_short="RBAC at scale",
    title_full="S2 · RBAC Design at Scale",
    title_html="K-ADV-SEC S2 · RBAC Design at Scale",
    module_eyebrow="Module S2 · the Authorization Desk — three things bind every authorisation",
    hero_sub_html='RBAC = three building blocks: <strong>subject</strong> (User / Group / ServiceAccount via OIDC or SA token), <strong>Role / ClusterRole</strong> (verbs on resources), <strong>RoleBinding / ClusterRoleBinding</strong> (which subjects get which role in which namespace or cluster). At scale: <strong>aggregation patterns</strong> (admin / edit / view + custom aggregations), <strong>OIDC group → Role mapping</strong>, <strong>audit-driven narrowing</strong> (find unused verbs and remove them), <strong>tooling</strong> (rakkess, kubectl-who-can, krew rbac-tool, audit2rbac).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. The auditor pulls a sample of 20 ServiceAccounts; <em>17 of them have <code>cluster-admin</code></em>. The team gave broad bindings during the rush of building the platform; nobody narrowed afterward. Compliance evidence collapses. Today\'s lesson: design RBAC so over-broad bindings are detected + removed before audit, not at audit.",
    stamp_html="<strong>RBAC = subject + role + binding. Use ClusterRole-aggregation for composability. Map OIDC groups to Roles, never to cluster-admin. Run audit-driven narrowing (audit2rbac) quarterly. Default-deny is the cluster\'s posture; cluster-admin is reserved for break-glass.</strong>",
    district_pin="ksec-bastion02",
    district_label="Authorization Desk",
    sections=[
        Section(
            eyebrow="Section 1.1 · the three building blocks",
            h2="Subject, Role / ClusterRole, RoleBinding / ClusterRoleBinding",
            body_html="""    <p><strong>Subject</strong> is who is asking — User (typically OIDC-authenticated humans), Group (an OIDC claim), or ServiceAccount (Pod identity). The apiserver resolves the subject from the request\'s authentication.</p>
    <p><strong>Role</strong> (namespaced) and <strong>ClusterRole</strong> (cluster-scoped) declare <em>verbs on resources</em> — e.g., <code>get/list/watch on pods</code>. Verbs: get, list, watch, create, update, patch, delete, deletecollection, plus subresource verbs (<code>pods/exec</code>, <code>pods/log</code>). Resources can be wildcarded (<code>*</code>) but rarely should be.</p>
    <p><strong>RoleBinding</strong> ties a subject to a Role <em>within one namespace</em>. <strong>ClusterRoleBinding</strong> ties a subject to a ClusterRole <em>across the whole cluster</em>. A ClusterRole can also be referenced by a RoleBinding to grant the ClusterRole\'s verbs <em>in just that namespace</em> — composable.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · aggregation patterns",
            h2="Built-in admin / edit / view + custom aggregation",
            body_html="""    <p>K8s ships four <strong>built-in ClusterRoles</strong>: <code>cluster-admin</code> (god mode — all verbs all resources), <code>admin</code> (all verbs all resources within a namespace), <code>edit</code> (read+write most resources, no RBAC), <code>view</code> (read-only most resources). For most teams: bind <code>edit</code> or <code>view</code>, never <code>cluster-admin</code>.</p>
    <p><strong>Aggregation</strong>: ClusterRoles can declare <code>aggregationRule.clusterRoleSelectors</code> matching label selectors; the apiserver merges all matching ClusterRoles\' rules. Pattern: ship a CRD with a small ClusterRole carrying the CRD\'s verbs + label <code>rbac.authorization.k8s.io/aggregate-to-edit: true</code> — automatically rolled into <code>edit</code>. Operators do this; you can too.</p>
    <p><strong>Custom aggregation</strong>: build platform-specific roles (<code>platform-developer</code>, <code>platform-readonly</code>) by aggregating finer-grained ClusterRoles. Bind groups (e.g., OIDC group <code>devs</code>) to these aggregated roles instead of bespoke RoleBindings per Service.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · OIDC + ServiceAccount best practices",
            h2="Humans via OIDC, workloads via SA — different patterns",
            body_html="""    <p><strong>OIDC for humans</strong>: configure apiserver flags to trust an OIDC issuer (Okta / Auth0 / Keycloak / Google / Azure AD). Tokens carry <code>sub</code> (user) + <code>groups</code> (claim mapped to K8s groups). RoleBindings reference groups (e.g., <code>oidc-group:platform-engineers</code>) — <em>never bind to individuals</em>; group membership is the abstraction.</p>
    <p><strong>ServiceAccount tokens</strong>: every Pod has one (default = <code>default</code> SA in its namespace). <em>Disable auto-mount</em> on the default SA (<code>automountServiceAccountToken: false</code>) and create per-workload SAs with explicit RoleBindings. <strong>Projected SA tokens</strong> (audience-scoped, short-lived, auto-rotating) are the modern pattern; replace static SA tokens.</p>
    <p><strong>Service-to-API patterns</strong>: an app calling the K8s API uses its Pod\'s SA. Scope the SA to <em>only the verbs on the resources the app actually calls</em>. Common over-grant: an app reads ConfigMaps but its SA has <code>configmap:*</code> (write too) — narrow to <code>get,list</code>.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · scale tooling + narrowing playbook",
            h2="audit2rbac, rakkess, kubectl-who-can, periodic narrowing",
            body_html="""    <p>At 30+ services, RBAC drift is inevitable without tooling.</p>
    <ul>
      <li><strong>rakkess</strong> (<code>kubectl access-matrix</code>): show what every SA / user can do across resources. Find over-broad bindings.</li>
      <li><strong>kubectl-who-can</strong>: \"who can <verb> <resource>?\" — quickly find dangerous bindings.</li>
      <li><strong>audit2rbac</strong>: from audit logs, generate the <em>minimum</em> RBAC rules a workload actually used. Run during a representative period; replace the SA\'s broad RoleBinding with the generated narrow one.</li>
      <li><strong>krew rbac-tool</strong>: visualise binding graphs; find unused; lookup permissions per subject.</li>
    </ul>
    <p><strong>Quarterly narrowing playbook</strong>: (1) Pull audit logs for past 90 days. (2) Per Service / SA, run audit2rbac to compute used permissions. (3) Diff against current binding — flag delta as candidate to remove. (4) Apply in dev / staging; observe one week; promote to prod. (5) Document the cut in change log. <em>Bind permissions you need; remove what you don\'t.</em></p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A team grants <code>cluster-admin</code> to every developer because RoleBindings \"are too granular.\" What\'s the standard alternative?",
            options=[
                ("Custom ClusterRole that\'s slightly narrower.", False),
                ("Use the built-in <code>edit</code> ClusterRole, bound per-namespace via RoleBinding (not ClusterRoleBinding).", True),
                ("Disable RBAC entirely.", False),
            ],
            feedback="The <code>edit</code> ClusterRole + per-namespace RoleBinding gives developers full read+write within their namespaces without granting RBAC verbs themselves or cross-namespace access.",
        ),
        3: PauseCheck(
            question="What does audit2rbac do?",
            options=[
                ("Generates audit log queries from RBAC bindings.", False),
                ("Reads audit logs + emits the minimum RBAC rules a workload actually used.", True),
                ("Replaces RBAC with audit-only mode.", False),
            ],
            feedback="audit2rbac is the audit-driven narrowing tool. Run during a representative period; produces the minimum-viable RoleBinding for the workload\'s actual API usage.",
        ),
    },
    before_after_before='<p>Pre-disciplined-RBAC, teams bound <code>cluster-admin</code> to every developer, every CI runner, every operator. SAs auto-mounted at default. Tokens were long-lived. Bindings drifted as new things were added; nothing was ever removed. Audit findings: dozens of unjustified cluster-admin bindings; no clear who-can-do-what story.</p>',
    before_after_after='<p>Modern RBAC: OIDC groups bound to aggregated platform roles; per-workload SAs with audit2rbac-narrowed bindings; auto-mount disabled on default SA; projected short-lived tokens; periodic narrowing reviews. <em>Audit can answer "who can call DELETE on Secrets" in 60 seconds.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Bind groups, not people. Bind narrow Roles, not cluster-admin. Run audit2rbac every quarter.</em></p>',
    analogy_intro_html='''<p>The Authorization Desk is the second wall of the Citadel. Every visitor presents a citizenship paper (subject), the gate-keeper consults a ledger of <strong>verbs</strong> (Role) — \"may enter the courtyard, may read the registry, may not approach the vault\" — and a <strong>binding scroll</strong> (RoleBinding) names which gate this verb-list applies at.</p>
    <p>Three desks share the load. The <strong>citizenship desk</strong> identifies (OIDC + SA tokens + mTLS). The <strong>verb desk</strong> records what each role may do (Roles + ClusterRoles). The <strong>binding desk</strong> assigns ledger pages to gate-keepers (RoleBindings). Aggregation lets one verb-list inherit pieces of another (admin/edit/view + custom aggregations) — saves rewriting.</p>
    <p>The Captain of the Watch reviews the ledgers quarterly with <strong>audit2rbac</strong>: the audit archive shows which verbs each citizen actually used; the ledgers get narrowed to match. Bindings that were never exercised are removed.</p>''',
    translation_rows=[
        ("Citizenship paper", "Subject (User / Group / ServiceAccount)"),
        ("OIDC papers from a foreign embassy", "OIDC token + groups claim"),
        ("Pod\'s in-cluster ID badge", "ServiceAccount token"),
        ("Short-lived stamped pass", "Projected ServiceAccount token (audience + expiry)"),
        ("Verb ledger", "Role / ClusterRole"),
        ("Built-in role tiers (admin/edit/view)", "Built-in ClusterRoles (admin / edit / view / cluster-admin)"),
        ("Inheritance chains", "ClusterRole aggregation via aggregationRule"),
        ("Binding scroll (this namespace only)", "RoleBinding"),
        ("Cluster-wide binding scroll", "ClusterRoleBinding"),
        ("Quarterly ledger review", "audit2rbac + rakkess + kubectl-who-can review"),
    ],
    analogy_stops="A real ledger is paper; K8s RBAC is policy evaluated by the apiserver per request — fast, deterministic, but invisible until tested. Test with <code>kubectl auth can-i</code>.",
    eli5="Imagine three desks at the gate. One checks who you are. Another reads which doors that kind of person may open. A third writes down where the rules apply. Your cluster has three K8s objects doing the same thing: subject, role, binding.",
    eli10="Three building blocks: <strong>Subject</strong> (User / Group / ServiceAccount; humans via OIDC, workloads via SA tokens — projected, short-lived). <strong>Role / ClusterRole</strong> (verbs on resources; built-ins admin/edit/view; aggregation via labels). <strong>RoleBinding / ClusterRoleBinding</strong> (binds subject to role; namespace-scoped or cluster-scoped). At scale: bind groups (not individuals); use built-in <code>edit</code> + per-namespace RoleBinding; disable default SA auto-mount; run audit2rbac quarterly to narrow.",
    scenarios=[
        Scenario(
            name="Platform team — OIDC group → aggregated Role",
            body="A 200-engineer org uses Okta. Group <code>k8s-developers</code> is bound (ClusterRoleBinding) to a custom aggregated <code>platform-developer</code> ClusterRole that combines the built-in <code>edit</code> + custom verbs (<code>get/list</code> on Backstage CRDs, <code>create/delete</code> on PRs to GitOps). New devs join group → access lands in 30 seconds; nothing per-developer.",
        ),
        Scenario(
            name="Per-workload SA narrowed by audit2rbac",
            body="An app reads ConfigMaps + lists Pods. Initial RoleBinding gave <code>edit</code>. Quarterly review: audit2rbac shows actual usage = <code>get/list configmap</code> + <code>list pod</code>. Narrowed RoleBinding reflects that. <em>Cut from \"can write everything\" to \"can read two things\"</em> with no app changes.",
        ),
        Scenario(
            name="Break-glass cluster-admin via JIT",
            body="Cluster-admin removed for all standing bindings. On-call invokes a JIT process (Vault SSH-style or a workflow approval) that issues a 1-hour cluster-admin kubeconfig + alarms in Slack. <em>Standing privilege replaced by audited just-in-time elevation.</em>",
        ),
        Scenario(
            name="Audit finding — 17/20 SAs with cluster-admin",
            body="An auditor sampled SAs in a regulated cluster; 17/20 had cluster-admin. Postmortem: SAs were broadly bound during the platform build phase; nothing narrowed after. Action: audit2rbac campaign over 60 days; quarterly narrowing now standard. Compliance gap closed.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"<code>cluster-admin</code> is for cluster admins; that\'s OK.\"",
            truth="<strong>cluster-admin = god mode</strong> — every verb on every resource including RBAC (can create/modify any binding). Use ONLY for break-glass elevation, never for standing access. Even cluster operators usually need only <code>admin</code>-equivalent ClusterRoles scoped to platform namespaces.",
        ),
        Misconception(
            myth="\"Every Pod needs the default ServiceAccount.\"",
            truth="The default SA gets auto-mounted unless explicitly disabled (<code>automountServiceAccountToken: false</code>). Most Pods don\'t need to call the K8s API at all — auto-mount + default SA = an attacker\'s gift if the Pod is compromised. Disable auto-mount; create per-workload SAs only when needed.",
        ),
        Misconception(
            myth="\"Aggregation is just for built-in roles like edit.\"",
            truth="<strong>You can build your own aggregated ClusterRoles</strong> for platform abstractions. Aggregation lets a CRD\'s small ClusterRole automatically merge into <code>edit</code> via a label — your platform can compose <code>platform-developer</code> from many small pieces. This is how operators integrate cleanly without modifying built-in roles.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three RBAC building blocks?", back="<strong>Subject</strong> (User / Group / ServiceAccount), <strong>Role / ClusterRole</strong> (verbs on resources), <strong>RoleBinding / ClusterRoleBinding</strong> (binds subject to role in scope)."),
        Flashcard(front="Built-in ClusterRoles?", back="<strong>cluster-admin</strong> (everything; break-glass only), <strong>admin</strong> (everything in a namespace including RBAC), <strong>edit</strong> (read+write most resources, NO RBAC), <strong>view</strong> (read-only)."),
        Flashcard(front="Why use ClusterRole + RoleBinding (not ClusterRoleBinding)?", back="Grants the ClusterRole\'s verbs <em>only within one namespace</em>. The most common safe pattern: <code>edit</code> ClusterRole + RoleBinding in dev / staging / prod-team namespace per developer group."),
        Flashcard(front="What does audit2rbac do?", back="Reads K8s audit logs and emits the minimum-viable RoleBinding (or ClusterRoleBinding) for the verbs/resources actually used by a subject during the audit window. Foundation of audit-driven narrowing."),
        Flashcard(front="Why bind to OIDC groups, not individuals?", back="(1) Reduces churn — joining a group → access lands instantly; leaving → revokes. (2) Smaller binding count. (3) Audit shows \"all platform-engineers\" not \"alice + bob + ...\". (4) Compliance evidence cleaner."),
        Flashcard(front="How does ClusterRole aggregation work?", back="A ClusterRole has <code>aggregationRule.clusterRoleSelectors</code> matching label selectors; apiserver merges all matching ClusterRoles\' rules. Operators ship a small ClusterRole with <code>rbac.authorization.k8s.io/aggregate-to-edit: true</code> → automatically inherited by <code>edit</code>."),
        Flashcard(front="Projected ServiceAccount token vs static SA token?", back="<strong>Projected</strong>: short-lived (1 hour default), audience-bounded, auto-rotating; modern default. <strong>Static</strong>: long-lived (no expiry), persists in a Secret; legacy + dangerous if leaked. Set <code>automountServiceAccountToken</code> appropriately."),
        Flashcard(front="What does <code>kubectl auth can-i</code> do?", back="Tests whether the current (or specified) subject can perform a verb on a resource. Use as: <code>kubectl auth can-i get pods --as=system:serviceaccount:default:my-sa</code>. Foundation of RBAC testing in CI / runbooks."),
    ],
    quizzes=[
        Quiz(
            prompt="A new operator pattern requires a Pod to <code>create</code> SubjectAccessReviews + <code>list</code> Roles. What\'s the safest binding?",
            answer="(1) Create a <strong>per-workload ServiceAccount</strong> in the operator\'s namespace. (2) Create a <strong>narrow ClusterRole</strong>: <code>rules: [{apiGroups: [authorization.k8s.io], resources: [subjectaccessreviews], verbs: [create]}, {apiGroups: [rbac.authorization.k8s.io], resources: [roles], verbs: [list]}]</code>. (3) <strong>ClusterRoleBinding</strong> ties the SA to that ClusterRole (cluster-scoped because the operator may inspect across namespaces). (4) Optional: scope tighter via <code>resourceNames</code> if the operator only inspects specific Roles. (5) Disable auto-mount on default SA in the namespace; explicitly reference the new SA in the operator Pod.",
        ),
        Quiz(
            prompt="Audit shows the CI runner SA has <code>cluster-admin</code>. Walk through the audit2rbac narrowing process.",
            answer='(1) <strong>Capture audit period</strong>: ensure audit policy logs every CI-runner-SA action with Request body level for at least 90 days (or representative window covering all CI workflows). (2) <strong>Run audit2rbac</strong>: <code>audit2rbac --filter (users: ci:runner)</code> against the audit log → emits a tightly-scoped Role + RoleBinding YAML. (3) <strong>Review</strong>: human reads the generated rules; flags anything that looks too narrow (CI may rotate paths). (4) <strong>Stage</strong>: apply generated bindings in dev cluster; observe one full release cycle. (5) <strong>Promote</strong>: replace cluster-admin binding in prod with the narrowed version. (6) <strong>Continuous monitoring</strong>: Falco / audit alerts on AccessDenied for that SA → adjust narrow binding if legitimate verb is missing.',
        ),
        Quiz(
            prompt="Leadership says \"merge all per-team RBAC into one global \'developer\' role for simplicity.\" Defend per-team RBAC.",
            answer="\"<strong>One global developer role is the audit anti-pattern that gets cited every time.</strong> Three reasons per-team RBAC stays: (1) <strong>Blast radius</strong>: if alice (team A) is compromised, the breach should not give the attacker access to team B\'s namespace. Per-team binding contains it. Global role removes the boundary. (2) <strong>Compliance</strong>: PCI / HIPAA / SOC2 expect role separation tied to data scope. \"Every developer can edit every namespace\" fails on first audit. (3) <strong>Operational hygiene</strong>: per-team role + RoleBinding scoped to team\'s namespace means new team onboarding follows a template — no special-case bindings. <strong>The simplicity win is illusory</strong>: per-team is more bindings but each is the same shape; it\'s 10 lines of YAML per team via Crossplane / OPA / GitOps. <strong>The cost is paid once at platform-build time; the safety dividend is paid every audit cycle and every incident.</strong>\"",
            cyoa=True,
            cyoa_tag="how the security architect defended per-team RBAC",
        ),
    ],
    glossary=[
        GlossaryItem(name="Subject", definition="Who is asking — User, Group, or ServiceAccount. Resolved by apiserver from request authentication."),
        GlossaryItem(name="Role / ClusterRole", definition="Verbs on resources. Role = namespace-scoped; ClusterRole = cluster-scoped."),
        GlossaryItem(name="RoleBinding / ClusterRoleBinding", definition="Ties subject to a role. RoleBinding = namespace-scoped; ClusterRoleBinding = cluster-scoped."),
        GlossaryItem(name="ClusterRole + RoleBinding combo", definition="Most common safe pattern: ClusterRole defines verbs (composable), RoleBinding scopes to one namespace."),
        GlossaryItem(name="cluster-admin", definition="Built-in ClusterRole — every verb every resource. Reserve for break-glass; never standing access."),
        GlossaryItem(name="ClusterRole aggregation", definition="aggregationRule + label selectors merge matching ClusterRoles. Operators use aggregate-to-edit/view labels."),
        GlossaryItem(name="audit2rbac", definition="Tool that reads audit logs + emits the minimum RBAC rules a workload actually used."),
        GlossaryItem(name="rakkess", definition="kubectl plugin showing the access-matrix of a subject across resources. Find over-broad bindings fast."),
        GlossaryItem(name="kubectl-who-can", definition="Reverse query: who can <verb> <resource>? Foundation of break-glass discovery + audit prep."),
        GlossaryItem(name="automountServiceAccountToken", definition="Pod-level boolean. False prevents the default SA token mounting; recommended cluster-wide except where the Pod actually calls K8s API."),
    ],
    recap_lead="RBAC = subject + role + binding. Aggregation patterns compose. OIDC groups bind to aggregated roles. Per-workload SAs are narrow. Quarterly audit2rbac narrows further. Cluster-admin is break-glass; default-deny is the cluster\'s posture.",
    recap_next='<strong>Next — S3: Admission Policy Architecture.</strong> Kyverno + Gatekeeper hybrid; mutating vs validating; ValidatingAdmissionPolicy + CEL inline; PolicyReport CRD; policy-as-code in CI.',
)
