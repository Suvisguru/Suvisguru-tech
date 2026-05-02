from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Watchtower entrance: an authentication checkpoint where guards check IDs (OIDC, certs, tokens), then pass visitors to a permissions desk that consults role binders for verbs vs resources.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">WATCHTOWER · AUTHENTICATION + AUTHORISATION CHECKPOINT</text>
  <!-- Auth checkpoint -->
  <g transform="translate(40,55)">
    <rect width="180" height="120" rx="8" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="90" y="18" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">AUTHENTICATION</text>
    <text x="90" y="30" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">\"who are you?\"</text>
    <rect x="14" y="40" width="76" height="22" rx="3" fill="#5A9F7A"/>
    <text x="52" y="54" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">OIDC (humans)</text>
    <rect x="94" y="40" width="72" height="22" rx="3" fill="#A04832"/>
    <text x="130" y="54" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">SA token (Pods)</text>
    <rect x="14" y="66" width="76" height="22" rx="3" fill="#E8B547"/>
    <text x="52" y="80" text-anchor="middle" font-size="7" fill="#5A4F45" font-weight="700">client cert</text>
    <rect x="94" y="66" width="72" height="22" rx="3" fill="#4A8FA8"/>
    <text x="130" y="80" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">webhook</text>
    <text x="90" y="106" text-anchor="middle" font-size="8" fill="#FBF1D6" font-style="italic">structured auth config (1.32+)</text>
  </g>
  <!-- Arrow -->
  <path d="M 230 115 L 270 115" stroke="#A04832" stroke-width="3" marker-end="url(#arr)"/>
  <defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#A04832"/></marker></defs>
  <!-- AuthZ -->
  <g transform="translate(280,40)">
    <rect width="360" height="150" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="180" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">AUTHORISATION</text>
    <text x="180" y="26" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">\"can you do this?\"</text>
    <!-- Roles -->
    <rect x="14" y="34" width="160" height="50" rx="4" fill="#E0EEF3" stroke="#4A8FA8" stroke-width="1"/>
    <text x="20" y="48" font-size="8" font-weight="700" fill="#3F4A5E">Role / ClusterRole</text>
    <text x="20" y="60" font-size="7" fill="#5A4F45">verbs: get, list, watch</text>
    <text x="20" y="70" font-size="7" fill="#5A4F45">resources: pods, services</text>
    <text x="20" y="80" font-size="7" fill="#5A4F45">resourceNames: optional</text>
    <!-- Subjects -->
    <rect x="186" y="34" width="160" height="50" rx="4" fill="#FBE8DC" stroke="#A04832" stroke-width="1"/>
    <text x="192" y="48" font-size="8" font-weight="700" fill="#3F4A5E">Binding</text>
    <text x="192" y="60" font-size="7" fill="#5A4F45">subjects:</text>
    <text x="200" y="70" font-size="7" fill="#5A4F45">- User: alice@corp</text>
    <text x="200" y="80" font-size="7" fill="#5A4F45">- ServiceAccount: prom</text>
    <!-- Result -->
    <rect x="14" y="92" width="332" height="40" rx="4" fill="#E0EFE6" stroke="#3D7857" stroke-width="1.2"/>
    <text x="180" y="108" text-anchor="middle" font-size="9" font-weight="700" fill="#3D7857">verb + resource + subject → ALLOW / DENY</text>
    <text x="180" y="122" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">first match wins; no implicit deny rule needed</text>
  </g>
  <text x="340" y="217" text-anchor="middle" font-size="0" fill="#3F4A5E"></text>
</svg>"""

LESSON = LessonSpec(
    num="27",
    title_short="RBAC &amp; Auth",
    title_full="RBAC & Authentication · Roles, Bindings, OIDC, Structured Auth",
    title_html="Lesson 27 — RBAC & Authentication · K-COM",
    module_eyebrow="Module 13 · Lesson 27 · who are you, and what can you do?",
    hero_sub_html='Two questions every API request answers: <strong>authentication</strong> (\"who are you?\") and <strong>authorisation</strong> (\"can you do this?\"). The first is plug-in: OIDC, certs, tokens, webhooks. The second is <strong>RBAC</strong>: a flat verb-on-resource model that\'s deceptively powerful. Today\'s lesson: both, plus the <em>structured authentication config</em> (GA in 1.32) that finally cleaned up the auth flag-soup.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Friday afternoon penetration test. The pen-tester finds a Pod running with the <code>default</code> ServiceAccount in the <code>default</code> namespace. They <code>kubectl exec</code> in and check token permissions: <code>kubectl auth can-i list secrets --all-namespaces</code> returns <strong>yes</strong>. They list every Secret across the cluster and find an admin kubeconfig. Game over. Root cause: someone, three years ago, ran <code>kubectl create clusterrolebinding wide-open --clusterrole=cluster-admin --serviceaccount=default:default</code> for "a quick test" and forgot to delete it. <em>Default-deny isn\'t the default.</em> RBAC requires intentional design. This lesson is the design.',
    stamp_html='Two checks: <strong>authentication</strong> (who are you?) and <strong>authorisation</strong> (RBAC: verb on resource for subject). Authentication is plug-in: OIDC for humans, ServiceAccount tokens for Pods, certs/webhooks for special cases. RBAC has four objects: <strong>Role</strong> + <strong>RoleBinding</strong> (namespace-scoped), <strong>ClusterRole</strong> + <strong>ClusterRoleBinding</strong> (cluster-wide). First match wins; if no rule allows, the request is denied.',
    district_pin="kt-pin27",
    district_label="Watchtower — Identity & Permissions Bureau",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Every API request is a 4-tuple",
            body_html="""    <p>Every request to the kube-apiserver gets reduced to four things: <strong>subject</strong> (who is asking), <strong>verb</strong> (what they want to do — get/list/watch/create/update/patch/delete), <strong>resource</strong> (what kind of thing — pods, secrets, deployments, etc.), <strong>scope</strong> (cluster-wide or specific namespace). The API server runs each request through two stages:</p>
    <ul>
      <li><strong>Authentication</strong> turns the request into a subject (user identity). \"Who is asking?\" Plug-in: OIDC, ServiceAccount tokens (TokenRequest API), client certs, static tokens (deprecated), bootstrap tokens, webhook authenticators.</li>
      <li><strong>Authorisation</strong> takes the subject + verb + resource + scope and asks: \"is this allowed?\" K8s ships with one primary authorizer: <strong>RBAC</strong> (others exist — Node, ABAC, Webhook — but RBAC is the bread and butter).</li>
    </ul>
    <p>If authorisation says yes, the request goes to <strong>admission</strong> (Lesson 28). If anywhere in this chain says no, the request is rejected with a clean 401/403.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The four RBAC objects",
            h2="Roles + Bindings, namespace and cluster",
            body_html="""    <div class="role-grid">
      <div class="role r1">
        <span class="role-icon">📋</span>
        <h3 class="role-name">Role</h3>
        <p class="role-tag">namespace-scoped permissions</p>
        <p class="role-desc">A list of rules: \"<code>verbs: [get, list, watch]</code> on <code>resources: [pods, services]</code>.\" Lives in a namespace; rules apply only to that namespace\'s resources.</p>
        <p class="role-who">Use for: per-team or per-app permissions inside a namespace.</p>
      </div>
      <div class="role r2">
        <span class="role-icon">🔗</span>
        <h3 class="role-name">RoleBinding</h3>
        <p class="role-tag">grants a Role to subjects</p>
        <p class="role-desc">Maps subjects (User, Group, ServiceAccount) to a Role. The binding lives in the same namespace as the Role; subjects can be from any namespace.</p>
        <p class="role-who">Use for: \"this team\'s SA gets these permissions in their namespace.\"</p>
      </div>
      <div class="role r3">
        <span class="role-icon">🏛️</span>
        <h3 class="role-name">ClusterRole</h3>
        <p class="role-tag">cluster-wide permissions</p>
        <p class="role-desc">Same shape as Role, cluster-scoped. Can list cluster-scoped resources (nodes, persistentvolumes, namespaces themselves) <em>and</em> can be referenced by RoleBindings to grant rights inside one namespace without redefining rules.</p>
        <p class="role-who">Use for: cluster-admin roles, reusable role definitions, scraping-style permissions (read all Pods cluster-wide).</p>
      </div>
      <div class="role r4">
        <span class="role-icon">🌐</span>
        <h3 class="role-name">ClusterRoleBinding</h3>
        <p class="role-tag">grants a ClusterRole cluster-wide</p>
        <p class="role-desc">Maps subjects to a ClusterRole at cluster scope. Subject can do whatever the ClusterRole says, in every namespace + cluster-wide resources.</p>
        <p class="role-who">Use for: cluster-admin grants, infra controllers, monitoring agents.</p>
      </div>
    </div>
    <p style="margin-top:18px"><strong>Key principle:</strong> RBAC is purely additive. There are no Deny rules. If no Role grants the verb on the resource, the request is denied. If you want to revoke, you remove the binding (or restrict the Role\'s verbs).</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Authentication mechanisms",
            h2="From flag soup to structured auth config",
            body_html="""    <p>K8s historically configured auth via API-server flags: <code>--oidc-issuer-url</code>, <code>--oidc-client-id</code>, <code>--oidc-username-claim</code>, … one OIDC issuer per cluster, no easy way to add a second, no way to express \"if username matches X then claim Y means Z.\" The <strong>Structured Authentication Configuration</strong> (alpha 1.29, beta 1.30, GA 1.32) replaces all that with a YAML file.</p>
    <p>What it gets you:</p>
    <ul>
      <li><strong>Multiple JWT issuers</strong> in one cluster — corp OIDC + GitHub OIDC + Google Workspace, each with its own claim mapping.</li>
      <li><strong>CEL expressions</strong> for username and group derivation. \"username = email if domain matches corp.com else email + \':external\'\".</li>
      <li><strong>Audience-bound</strong> issuer validation — protect against token confusion attacks.</li>
      <li><strong>Hot reload</strong> — change the config, API server picks it up without restart.</li>
    </ul>
    <p>Authentication mechanisms in 2026 (in priority of usage):</p>
    <ul>
      <li><strong>OIDC</strong> (humans) — corp SSO, GitHub, Google Workspace. Every CI tool integrates.</li>
      <li><strong>ServiceAccount tokens</strong> (Pods) — projected, bound, short-lived. See Lesson 21.</li>
      <li><strong>X.509 client certs</strong> — cluster admins, kubeadm bootstrap. CN = username; O = group.</li>
      <li><strong>Webhook authenticator</strong> — defer to an external service. Useful for IAM-style integration.</li>
      <li><strong>Static tokens</strong> — DEPRECATED. Don\'t use in new clusters.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.9 · Practical RBAC patterns",
            h2="What good cluster RBAC looks like",
            body_html="""    <p>Three rules every team should follow:</p>
    <ol>
      <li><strong>Least privilege.</strong> A Pod that reads ConfigMaps doesn\'t need <code>list, watch, create, update, patch, delete</code>. It needs <code>get</code>. Audit your SA bindings; tighten them.</li>
      <li><strong>One ServiceAccount per workload.</strong> Don\'t let unrelated workloads share the same SA — a bug in one becomes a permission inheritance issue for the other. The <code>default</code> SA in every namespace should be permissionless (no RoleBindings).</li>
      <li><strong>Avoid <code>*</code> verbs.</strong> <code>verbs: [\"*\"]</code> means every verb K8s adds in the future automatically applies. Spell out the verbs you want.</li>
    </ol>
    <p>Common mis-grants to watch for:</p>
    <ul>
      <li><code>cluster-admin</code> grants — review every ClusterRoleBinding to <code>cluster-admin</code>. Each one is the keys to the kingdom.</li>
      <li><code>secrets</code> read access in unexpected places. Auditors love finding controllers that have read access to all Secrets when they only need a few.</li>
      <li><code>pods/exec</code> grants — anyone who can <code>exec</code> can effectively do whatever a Pod can do. Tight scope these.</li>
      <li>Wildcard resource grants — <code>resources: [\"*\"]</code> grants access to every K8s resource, including future CRDs.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>Run <code>kubectl auth can-i --list --as=system:serviceaccount:foo:bar</code> to enumerate everything an SA can do. <code>rakkess</code> and <code>rbac-tool</code> are popular utilities for visualising the full RBAC graph. Most production clusters benefit from running these as part of CI on every RBAC change — the diff catches accidentally-overpermissioned bindings before they merge.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A Pod\'s ServiceAccount is bound to a Role that grants <code>verbs: [get, list]</code> on <code>configmaps</code> in namespace <code>app</code>. The Pod tries to read a ConfigMap in namespace <code>kube-system</code>. What happens?",
            options=[
                ("a) Allowed — the Role grants get/list on configmaps", False),
                ("b) Denied — the Role is namespace-scoped to <code>app</code>; it doesn\'t apply outside that namespace", True),
                ("c) Allowed if the kube-system ConfigMap is named the same", False),
            ],
            feedback="<strong>Answer: b.</strong> Roles + RoleBindings are namespace-scoped. The Pod can read ConfigMaps in <code>app</code> only. To read ConfigMaps cluster-wide, you\'d need a ClusterRole + ClusterRoleBinding. RBAC is intentionally narrow — \"can I do X in Y?\" not \"can I do X anywhere?\"",
        ),
    },
    before_after_before='<p>Pre-OIDC, pre-bound-tokens era: <code>kubectl create clusterrolebinding</code> with hand-crafted ServiceAccount tokens, kubeconfigs distributed via Slack, the same cluster-admin token shared across the team. Auth flags hard-coded into kube-apiserver; one OIDC provider only. \"Quick tests\" granted permanent cluster-admin to default SAs. <em>The default attacker objective: find an over-permissioned default SA.</em></p>',
    before_after_after='<p>OIDC for humans (corp SSO + audit), bound tokens for Pods, structured auth config for cleaner setup, RBAC reviewed in CI via <code>rakkess</code> and policy reports. Default SA in every namespace: permissionless. Pen-test finds nothing interesting on the default SA path.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">RBAC is the API server\'s most under-appreciated feature: by being purely additive (no deny rules), it\'s simple to reason about. The complexity is in your bindings, not in the model.</p>',
    analogy_intro_html='<p>Watchtower stands at the edge of K-Town: the city\'s identity-and-permissions bureau. Two checkpoints, in order. The <strong>identity desk</strong> verifies who you are — corp employee badge (OIDC), Pod license plate (ServiceAccount token), notarised letter of introduction (client cert), or a third-party endorsement (webhook authenticator). The <strong>permissions desk</strong> consults a binder of <em>roles</em> — each role lists \"verbs you can perform on resources you can touch\" — and a binder of <em>bindings</em> mapping people and Pods to roles.</p><p>Two scopes. The <strong>district binder</strong> (Role + RoleBinding) covers permissions inside one neighbourhood. The <strong>city binder</strong> (ClusterRole + ClusterRoleBinding) covers the whole city plus the city-wide registries. Permissions are <em>additive</em>: no role binder ever has a "no" rule. If your role doesn\'t grant the verb, the answer is no by default. If you want to revoke, the desk tears your binding out of the binder.</p>',
    translation_rows=[
        ("The identity desk", "Authentication (OIDC, SA tokens, certs, webhooks)"),
        ("Corp employee badge", "OIDC token from corp SSO"),
        ("Pod license plate", "ServiceAccount projected JWT"),
        ("The district binder", "<code>Role</code> + <code>RoleBinding</code>"),
        ("The city-wide binder", "<code>ClusterRole</code> + <code>ClusterRoleBinding</code>"),
        ("\"Verbs on resources\" rule", "RBAC rule: <code>verbs: [...]</code> on <code>resources: [...]</code>"),
        ("\"No\" rules don\'t exist; revoke = tear out binding", "Additive-only RBAC; no Deny rules"),
        ("\"Quick test\" cluster-admin grant from 3 years ago", "Stale ClusterRoleBinding to cluster-admin"),
        ("New, cleaned-up identity desk software", "Structured Authentication Configuration (GA 1.32)"),
    ],
    analogy_stops="The analogy stops here: real RBAC is a programmatic match against verbs/resources/names — there\'s no human reading a binder. And authentication isn\'t \"checking a badge\"; it\'s cryptographic verification of a signed token, with all the implications about key rotation and replay.",
    eli5='Two doors. The first asks: who are you? Show your badge. The second asks: are you allowed to do this thing here? Look at the binder. If your name and the thing aren\'t both in the binder, sorry — you can\'t.',
    eli10="Every API request: authenticate (who?) → authorise (allowed?). Authentication is plug-in: OIDC, SA tokens (modern bound JWTs), client certs, webhooks. Authorisation is mostly RBAC: <code>Role</code> + <code>RoleBinding</code> (namespace) and <code>ClusterRole</code> + <code>ClusterRoleBinding</code> (cluster). Rules are <em>additive</em> — no Deny. First match wins. Structured Auth Config (GA 1.32) lets you configure multiple OIDC issuers and CEL-based claim mapping in one YAML file. Modern best practice: OIDC for humans, bound SA tokens for Pods, default SAs permissionless, one SA per workload, audit RBAC graphs in CI.",
    scenarios=[
        Scenario(name="A SaaS using corp SSO via OIDC", body="Structured Auth Config maps email → user, Okta groups → K8s groups. Cluster admins are in the <code>k8s-cluster-admins</code> Okta group. Adding/removing admins is an Okta change, not a kubeconfig redistribution. Audit logs show every API call by corp username. SOC2 happy."),
        Scenario(name="A bank running zero shared kubeconfigs", body="Every developer authenticates via OIDC. <code>kubectl</code> uses the OIDC client plugin; tokens last 1 hour, refreshed silently. No shared static tokens exist anywhere. When a developer leaves the org, they\'re removed from Okta; their cluster access ends within minutes."),
        Scenario(name="A startup that audits RBAC in CI", body="Every PR touching a <code>RoleBinding</code> or <code>ClusterRoleBinding</code> runs <code>rbac-tool</code> + <code>kubectl auth can-i --list</code> diff. PR description requires explaining permission additions. The platform team has caught two cluster-admin grants that would have bypassed every other security control."),
        Scenario(name="A team using webhook authn for AWS IAM identity", body="Webhook authenticator integrates with AWS IAM; <code>eks-iam-authenticator</code> validates an AWS-signed token and returns an identity. K8s RBAC sees \"<code>arn:aws:iam::123:role/PlatformEng</code>\" as a username; bindings reference it. AWS-side IAM changes propagate to K8s instantly."),
    ],
    misconceptions=[
        Misconception(myth="RBAC has Deny rules.", truth="It doesn\'t. RBAC is purely additive. Anything not explicitly allowed is denied by default. To \"deny\" something, you remove the binding that grants it. If you need true deny semantics (block specific operations even if other rules allow), use admission control (ValidatingAdmissionPolicy / Kyverno / OPA) — covered in Lesson 28."),
        Misconception(myth="The <code>default</code> ServiceAccount in every namespace is harmless.", truth="It\'s harmless only if no RoleBindings reference it. By default, K8s ships <code>default</code> with no permissions. Many teams accidentally add bindings for \"convenience\" — these become privilege-escalation footholds. Pod Security Admission can enforce \"must specify a non-default SA.\""),
        Misconception(myth="<code>cluster-admin</code> is a normal role.", truth="It\'s the highest-privilege role: <code>verbs: [\"*\"]</code> on <code>resources: [\"*\"]</code> on all <code>apiGroups: [\"*\"]</code>. Anyone bound to it can do anything in the cluster. Treat every <code>ClusterRoleBinding</code> to <code>cluster-admin</code> as critical infrastructure; review them quarterly."),
    ],
    flashcards=[
        Flashcard(front="The 4-tuple of every API request?", back="Subject (who) + verb (action) + resource (what kind) + scope (cluster or namespace). The authoriser checks if any rule grants this combination."),
        Flashcard(front="Role vs ClusterRole?", back="Role: namespace-scoped, applies to namespaced resources only. ClusterRole: cluster-scoped, applies to cluster resources <em>and</em> can be referenced by RoleBinding to grant scoped access without re-defining."),
        Flashcard(front="RoleBinding vs ClusterRoleBinding?", back="RoleBinding: grants a Role (or ClusterRole) within one namespace. ClusterRoleBinding: grants a ClusterRole cluster-wide. The Role/Binding split is the key idea."),
        Flashcard(front="Why is RBAC additive?", back="Simplicity: no precedence rules to reason about. \"Is there a binding granting this verb?\" If yes, allow. If no, deny. Removing access = removing bindings."),
        Flashcard(front="What is Structured Auth Config?", back="K8s 1.32 GA. YAML file replacing OIDC + token flag soup on kube-apiserver. Supports multiple JWT issuers, CEL claim mapping, hot reload."),
        Flashcard(front="<code>kubectl auth can-i</code>?", back="Built-in command. <code>kubectl auth can-i list secrets --all-namespaces</code> answers yes/no for the current user. With <code>--as</code> you can impersonate (if you have impersonate permission) and check anyone\'s access."),
        Flashcard(front="Common over-grant: <code>verbs: [\"*\"]</code>?", back="Means \"every verb K8s adds in the future automatically applies.\" Avoid in production. Spell out the verbs you actually need."),
        Flashcard(front="What is impersonate verb?", back="Special verb: <code>kubectl --as=user</code> requires the requesting subject to have <code>impersonate</code> on the user. Used for debugging RBAC and integration testing."),
    ],
    quizzes=[
        Quiz(prompt="A team\'s monitoring controller needs to <code>list</code> all Pods cluster-wide. Two ways to grant this. Which is better, and why?", answer="<strong>Better:</strong> create a ClusterRole with <code>verbs: [list, watch], resources: [pods]</code>, then a ClusterRoleBinding to the monitoring SA. <strong>Alternative (worse):</strong> create a RoleBinding in every namespace. Why ClusterRoleBinding is better: (1) one object, not N. (2) Automatically applies to new namespaces. (3) Clearly expresses intent: \"this is cluster-wide read.\" The downside is wider blast radius — if the monitoring SA is compromised, the attacker can read all Pods. Mitigate by ensuring the monitoring SA can\'t do anything else (no exec, no get on secrets, etc.)."),
        Quiz(prompt="A pen-tester finds a Pod with <code>kubectl auth can-i list secrets --all-namespaces</code> = yes. What\'s the playbook to remediate without breaking the workload?", answer="<strong>Step 1:</strong> identify why. Is the Pod\'s SA bound to a ClusterRoleBinding to <code>cluster-admin</code> or similar? <code>kubectl get clusterrolebindings -o json | jq '.items[] | select(.subjects[]?.name == \"&lt;sa-name&gt;\")'</code>. <strong>Step 2:</strong> understand the legitimate need. Maybe the workload needs to read <em>one specific</em> Secret. Maybe nothing — it was a test that wasn\'t cleaned up. <strong>Step 3:</strong> replace the over-grant with a minimal Role: <code>verbs: [get], resources: [secrets], resourceNames: [the-one-it-needs]</code>. <strong>Step 4:</strong> verify the workload still works (canary deploy). <strong>Step 5:</strong> add a CI check that prevents this regression. <strong>Step 6:</strong> audit other namespaces for similar over-grants — they probably exist too."),
        Quiz(prompt="The CISO asks: \"prove that no Pod in the production cluster can list Secrets in <code>kube-system</code>.\" <strong>Click for the audit walkthrough. ▼</strong>", cyoa=True, cyoa_tag="the audit walkthrough", answer="<strong>(1) Enumerate all SAs:</strong> <code>kubectl get sa -A -o name | wc -l</code>. <strong>(2) For each SA, check the relevant verb:</strong> <code>kubectl auth can-i list secrets --as=system:serviceaccount:&lt;ns&gt;:&lt;sa&gt; -n kube-system</code>. Script this; expect every result to be \"no\". Any \"yes\" is the audit finding. <strong>(3) For deeper assurance:</strong> use <code>rakkess</code> or <code>kubectl-who-can list secrets --namespace kube-system</code>. The output shows every subject (User, Group, ServiceAccount) that has the permission. Compare against an allow-list of intended subjects. <strong>(4) Add to CI:</strong> store the expected allow-list in git; run the same audit on every RBAC change PR. Catch new grants at PR time, not pen-test time. <strong>(5) Defense in depth:</strong> AdminNetworkPolicy at the network layer to deny <code>kube-system</code> egress from non-system namespaces. Layered defenses make audit findings rare."),
    ],
    glossary=[
        GlossaryItem(name="Authentication", definition="Establishing who is asking. Plug-in: OIDC, SA tokens, certs, webhooks."),
        GlossaryItem(name="Authorisation", definition="Deciding if the authenticated subject is allowed. RBAC is the standard authorizer."),
        GlossaryItem(name="RBAC", definition="Role-Based Access Control. Four objects: Role, RoleBinding, ClusterRole, ClusterRoleBinding."),
        GlossaryItem(name="Role", definition="Namespace-scoped permission set: verbs on resources."),
        GlossaryItem(name="ClusterRole", definition="Cluster-scoped permission set. Reusable from RoleBindings for namespace-scoped grants."),
        GlossaryItem(name="RoleBinding", definition="Maps subjects (User/Group/SA) to a Role or ClusterRole within a namespace."),
        GlossaryItem(name="ClusterRoleBinding", definition="Maps subjects to a ClusterRole cluster-wide."),
        GlossaryItem(name="OIDC", definition="OpenID Connect. Standard for federated identity. The default integration for human users."),
        GlossaryItem(name="Structured Auth Config", definition="K8s 1.32 GA. YAML config replacing flag-soup; supports multiple JWT issuers + CEL claim mapping."),
        GlossaryItem(name="cluster-admin", definition="Built-in ClusterRole with all verbs on all resources. The keys to the kingdom; review every binding."),
        GlossaryItem(name="kubectl auth can-i", definition="Built-in command for checking permissions. With <code>--as</code> impersonate, with <code>--list</code> enumerate."),
        GlossaryItem(name="rakkess / rbac-tool", definition="Community CLI tools for visualising the full RBAC graph. Useful in CI."),
    ],
    recap_lead="Authentication answers \"who?\"; RBAC answers \"can you do this?\". Four objects: Role / RoleBinding (namespace) and ClusterRole / ClusterRoleBinding (cluster). Additive only. OIDC for humans, bound SA tokens for Pods, default SAs permissionless, one SA per workload.",
    recap_next="<strong>Next — Lesson 28: Admission Control.</strong> When RBAC says yes, the request goes through admission. ValidatingAdmissionPolicy (in-cluster CEL), Pod Security Admission (PSA), webhook admission, mutation. The Watchtower interior.",
)
