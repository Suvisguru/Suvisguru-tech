from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Security desk: two checkpoints - AWS IAM (cluster-level) and K8s RBAC (in-cluster), connected by access entries (modern) and IRSA / Pod Identity for Pods.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">SECURITY DESK · IAM + K8s RBAC</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <rect x="14" y="34" width="280" height="44" rx="6" fill="#3F4A5E"/><text x="154" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">AWS IAM (cluster-level)</text><text x="154" y="64" text-anchor="middle" font-size="8" fill="#FBE8DC">who can call EKS APIs (CreateCluster, DescribeNodegroup)</text>
    <rect x="306" y="34" width="280" height="44" rx="6" fill="#5A9F7A"/><text x="446" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">K8s RBAC (in-cluster)</text><text x="446" y="64" text-anchor="middle" font-size="8" fill="#FBE8DC">who can call kube-apiserver (get pods, edit deployments)</text>
    <rect x="14" y="84" width="280" height="44" rx="6" fill="#FBF1D6" stroke="#8B5A00"/><text x="154" y="100" text-anchor="middle" font-size="10" font-weight="700" fill="#8B5A00">access entries (modern)</text><text x="154" y="114" text-anchor="middle" font-size="8" fill="#5A4F45">map IAM principal → K8s group/role</text>
    <rect x="306" y="84" width="280" height="44" rx="6" fill="#FBE8DC" stroke="#A04832"/><text x="446" y="100" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">aws-auth ConfigMap (legacy)</text><text x="446" y="114" text-anchor="middle" font-size="8" fill="#5A4F45">edit a ConfigMap to add IAM users — fragile</text>
    <rect x="14" y="134" width="280" height="22" rx="3" fill="#A04832"/><text x="154" y="148" text-anchor="middle" font-size="8" fill="#FBE8DC">IRSA (legacy): OIDC provider + ServiceAccount + IAM role trust</text>
    <rect x="306" y="134" width="280" height="22" rx="3" fill="#5A9F7A"/><text x="446" y="148" text-anchor="middle" font-size="8" fill="#FBE8DC">EKS Pod Identity (modern): Pod Identity Agent + association — simpler</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="04",
    title_short="IAM &amp; identity",
    title_full="E4 · Identity and Access (Access Entries, IRSA, Pod Identity)",
    title_html="K-EKS E4 · Identity and Access",
    module_eyebrow="Module E4 · the security desk",
    hero_sub_html='Two identity surfaces: <strong>AWS IAM</strong> controls who can call EKS APIs (cluster-level); <strong>K8s RBAC</strong> controls who can call kube-apiserver (in-cluster). Bridge via <strong>access entries</strong> (modern) or <strong>aws-auth ConfigMap</strong> (legacy). For Pod-to-AWS-service: <strong>IRSA</strong> (legacy) or <strong>EKS Pod Identity</strong> (modern, simpler).',
    hero_illu_svg=HERO_SVG,
    nightmare_html='New engineer can\'t <code>kubectl get pods</code>. They have AWS IAM admin, but the cluster\'s <code>aws-auth</code> ConfigMap doesn\'t list their role. Edit the ConfigMap; one syntax error locks <em>everyone</em> out (it\'s parsed strictly). Recovery: AWS-side IAM only path is via <code>kubectl edit cm aws-auth</code> from a working session that no longer exists. <em>EKS access entries (the modern path) avoid this entirely</em>: configure via the EKS API, no in-cluster ConfigMap edit, AWS owns the trust path.',
    stamp_html='Two identity layers: <strong>AWS IAM</strong> (cluster API access — CreateCluster, DescribeNodegroup, kubeconfig retrieval) and <strong>K8s RBAC</strong> (in-cluster — get pods, edit deployments). Map IAM → K8s via <strong>access entries</strong> (modern, recommended) or <strong>aws-auth ConfigMap</strong> (legacy, fragile). For Pod-to-AWS-service: <strong>EKS Pod Identity</strong> (Pod Identity Agent + association API — modern, simpler) or <strong>IRSA</strong> (OIDC provider + IAM trust policy — legacy but still common).',
    district_pin="ks-floor04",
    district_label="Security Desk",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Two identity surfaces",
            body_html="""    <p>EKS has two identity systems running in parallel:</p>
    <ul>
      <li><strong>AWS IAM</strong> — Who can call AWS EKS APIs (<code>eks:CreateCluster</code>, <code>eks:DescribeNodegroup</code>, <code>eks:UpdateClusterConfig</code>). Also: who can retrieve a kubeconfig (<code>aws eks update-kubeconfig</code>). IAM principals are users / roles / federated identities.</li>
      <li><strong>K8s RBAC</strong> — Who can do what <em>inside</em> the cluster (get pods, edit deployments, read secrets). RBAC subjects are K8s users / groups / ServiceAccounts.</li>
    </ul>
    <p>The bridge is the <strong>access entry</strong> (or legacy <code>aws-auth</code> ConfigMap): \"this AWS IAM principal maps to this K8s username + group, which the cluster\'s ClusterRoleBindings reference.\" Without the bridge, an IAM admin gets a kubeconfig but can\'t list a Pod.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Access entries vs aws-auth",
            h2="The modern path + the legacy hazard",
            body_html="""    <p><strong>Access entries</strong> (released GA 2024) are the modern path. Configured via the EKS API (or eksctl / Terraform); each access entry maps an IAM principal ARN to a K8s username + groups + access-policy. AWS validates the mapping before applying.</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>aws eks create-access-entry \\
  --cluster-name prod \\
  --principal-arn arn:aws:iam::123:role/PlatformEngineer \\
  --type STANDARD \\
  --kubernetes-groups platform-admins

aws eks associate-access-policy \\
  --cluster-name prod \\
  --principal-arn arn:aws:iam::123:role/PlatformEngineer \\
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy \\
  --access-scope type=cluster</code></pre>
    <p><strong>aws-auth ConfigMap</strong> (legacy) is a YAML in <code>kube-system</code>. Edit it to add/remove IAM mappings. Hazards: (1) syntax errors lock everyone out. (2) Concurrent edits race. (3) GitOps-managed aws-auth conflicts with manual emergency edits. <strong>Migrate to access entries.</strong></p>
    <p>EKS supports a precedence: access entries take precedence over aws-auth when both exist for the same principal. New clusters: access-entries-only. Old clusters: migrate.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · IRSA — the legacy Pod-to-AWS-service path",
            h2="OIDC + trust policy + ServiceAccount",
            body_html="""    <p><strong>IRSA (IAM Roles for Service Accounts)</strong> lets a Pod assume an IAM role to call AWS services (S3, SQS, KMS, etc.). The flow:</p>
    <ol>
      <li>EKS publishes an OIDC discovery endpoint per cluster.</li>
      <li>You create an IAM role with a <em>trust policy</em> allowing the cluster\'s OIDC provider to assume it for a specific SA.</li>
      <li>Annotate the SA: <code>eks.amazonaws.com/role-arn: arn:aws:iam::...</code>.</li>
      <li>The Pod\'s projected JWT (audience <code>sts.amazonaws.com</code>) is exchanged via STS for AWS creds.</li>
      <li>AWS SDKs in the Pod auto-pick up the creds via <code>~/.aws/credentials</code>-equivalent env vars.</li>
    </ol>
    <p>It works, but: (1) trust policies are wordy + error-prone. (2) Per-cluster OIDC providers proliferate. (3) Cross-cluster reuse is awkward. (4) Cross-account flows require additional STS hops.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · EKS Pod Identity — the modern Pod-to-AWS path",
            h2="Pod Identity Agent + association API",
            body_html="""    <p><strong>EKS Pod Identity</strong> (released GA 2023) is the modern, simpler successor to IRSA. The flow:</p>
    <ol>
      <li>Install the <strong>Pod Identity Agent</strong> as a managed add-on (one-time per cluster; AWS upgrades).</li>
      <li>Create an IAM role with a trust policy allowing <code>pods.eks.amazonaws.com</code> as principal.</li>
      <li>Create a Pod Identity association: <code>aws eks create-pod-identity-association --cluster-name X --namespace ns --service-account sa --role-arn ...</code>.</li>
      <li>Pods running as that SA get AWS creds via the agent. SDKs pick up automatically.</li>
    </ol>
    <p>Why it\'s better: no per-cluster OIDC provider; trust policy is identical across clusters; cross-account is one association call; the agent handles the heavy lifting. <strong>For new clusters in 2026: Pod Identity. For existing IRSA: migrate at your pace.</strong></p>
    <p><strong>IAM Identity Center (SSO)</strong>: federate human identities to AWS via SAML/OIDC; assume IAM roles per session; access entries grant K8s permissions to those roles. The full chain: corp SSO → IAM role → access entry → K8s group → ClusterRoleBinding.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For ECR pulls + Secrets Manager + KMS access, the simplest pattern: a single role with all required AWS permissions, associated to a SA, used by every Pod that needs cross-AWS-service access. Per-namespace roles for least privilege.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your dev gets <code>You must be logged in to the server (Unauthorized)</code> when running kubectl. They have AWS IAM admin. Diagnose.',
            options=[
                ('a) Their kubeconfig is broken', False),
                ('b) IAM admin lets them retrieve the kubeconfig (eks:DescribeCluster), but no access entry / aws-auth mapping exists for their IAM role to a K8s group. Add the mapping.', True),
                ('c) The cluster is down', False),
            ],
            feedback='<strong>Answer: b.</strong> AWS IAM and K8s RBAC are separate. Even with full IAM admin, you need a bridge mapping the IAM principal to K8s. Modern fix: <code>aws eks create-access-entry --cluster-name X --principal-arn arn:aws:iam::123:user/dev --type STANDARD --kubernetes-groups system:masters</code> (for full admin) — or a custom group bound to a Role/ClusterRole. Avoid <code>system:masters</code> for non-emergency access.',
        ),
    },
    before_after_before='<p>Single shared <code>aws-auth</code> ConfigMap edited via <code>kubectl edit cm</code>. Three engineers tried to edit at once last quarter; YAML conflicts; cluster locked everyone out for 45 minutes. IRSA per-cluster OIDC providers + trust-policy edits per role; cross-account = manual STS hops.</p>',
    before_after_after='<p>Access entries managed via Terraform; per-IAM-principal mappings in git, applied via API not ConfigMap edit. Pod Identity Agent installed; one association per (SA, role); cross-account = one association call. Audit log shows every change.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">EKS identity has had a generational upgrade in 2023-24: access entries replaced aws-auth, Pod Identity replaced IRSA. New clusters: use the modern path; legacy: migrate.</p>',
    analogy_intro_html='<p>The Security Desk in K-Skyline has two checkpoints. The <strong>building entrance</strong> (AWS IAM) checks who can even enter the tower — admins, vendors, residents. The <strong>elevator panel</strong> (K8s RBAC) controls which floors each entrant can reach. Between them: the <strong>guest registry</strong> (access entries) maps building entries to elevator codes. For visiting your bank vault on another floor (AWS service from a Pod): the <strong>concierge note</strong> (Pod Identity) tells the elevator that the bearer\'s elevator code includes vault access. The legacy <strong>blue-key system</strong> (IRSA) used a per-floor key card the visitor had to pre-arrange.</p>',
    translation_rows=[
        ('Building entrance check', 'AWS IAM (eks:* permissions)'),
        ('Elevator panel access', 'K8s RBAC (Role/ClusterRole)'),
        ('Guest registry mapping entry → elevator code', 'Access entries (modern)'),
        ('Hand-edited paper guestbook', 'aws-auth ConfigMap (legacy, fragile)'),
        ('Concierge note for vault access', 'EKS Pod Identity (Pod Identity Agent + association)'),
        ('Blue-key system per floor', 'IRSA (OIDC provider + trust policy)'),
        ('Federated visitor pass from sister hotels', 'IAM Identity Center (SSO) → IAM role → access entry → K8s group'),
    ],
    analogy_stops="The analogy stops here: real auth is cryptographic — JWT exchange via STS, signed kubeconfig tokens, OIDC discovery endpoints. The desk metaphor undersells the trust chain.",
    eli5='Two doors. The first door checks if you\'re allowed in the building (IAM). The second door checks which rooms you can enter (K8s RBAC). The hotel keeps a list of who matches what.',
    eli10="Two identity layers in EKS: AWS IAM (who can call EKS APIs + retrieve kubeconfig) and K8s RBAC (in-cluster permissions). Bridge via access entries (modern, API-managed) or aws-auth ConfigMap (legacy, fragile). For Pod → AWS service: EKS Pod Identity (modern, agent-based, association API) or IRSA (legacy, OIDC + trust policy). New clusters use access entries + Pod Identity; old clusters migrate.",
    scenarios=[
        Scenario(name='A SaaS managing access via Terraform + access entries', body='Every IAM role mapped to a K8s group via Terraform-managed access entries. New engineer = PR adds them to the IAM role + the access entry; merge auto-syncs. No more manual aws-auth edits.'),
        Scenario(name='A bank using SSO + access entries + per-namespace Pod Identity', body='Corp Okta → IAM Identity Center → IAM role per team → access entry per role → K8s group → namespace-scoped Role. Pods get AWS access via Pod Identity associations per (namespace, SA). Zero shared kubeconfigs; full audit trail.'),
        Scenario(name='A team migrating IRSA → Pod Identity', body='New SAs use Pod Identity. Old IRSA SAs left in place; tracked for migration. Per-SA migration: install Pod Identity Agent; create association; remove IRSA annotation; restart Pod. Quarter-long phased migration; no big bang.'),
        Scenario(name='A team that locked everyone out', body='Junior engineer edited <code>aws-auth</code> ConfigMap; YAML indent error parsed as removing all admins. EKS Console fix: AWS recommends pre-existing access entries for emergency admin recovery (the access-entry API can\'t be locked out by ConfigMap edits). Lesson: migrate to access entries before you need them.'),
    ],
    misconceptions=[
        Misconception(myth='\"AWS IAM admin = K8s admin.\"', truth='IAM admin lets you retrieve kubeconfig + manage the cluster object; doesn\'t imply K8s RBAC permissions. The two are separate. Bridge via access entry / aws-auth.'),
        Misconception(myth='\"IRSA is fine; no need to migrate to Pod Identity.\"', truth='IRSA works but: per-cluster OIDC, per-role trust-policy edits, awkward cross-cluster + cross-account. Pod Identity is simpler + more uniform. Migrate at your pace; new SAs default to Pod Identity.'),
        Misconception(myth='\"aws-auth ConfigMap is the same as access entries.\"', truth='ConfigMap = legacy, edited in-cluster, prone to lockout. Access entries = API-managed, AWS-validated, can\'t lock you out via ConfigMap mistake. New clusters: access entries only.'),
    ],
    flashcards=[
        Flashcard(front='Two EKS identity layers?', back='AWS IAM (cluster-level: eks:* permissions, kubeconfig retrieval). K8s RBAC (in-cluster: get pods, edit deployments). Bridge via access entries / aws-auth.'),
        Flashcard(front='Access entries vs aws-auth?', back='Access entries: API-managed, AWS-validated, modern (2024 GA). aws-auth: legacy ConfigMap edited in <code>kube-system</code>; lockout-prone. New clusters use access entries only.'),
        Flashcard(front='IRSA flow?', back='Cluster has OIDC provider; IAM role has trust policy referencing that OIDC + a specific SA; SA is annotated with role ARN; Pod\'s JWT is exchanged via STS for AWS creds.'),
        Flashcard(front='EKS Pod Identity flow?', back='Pod Identity Agent (managed add-on) running. IAM role trusts <code>pods.eks.amazonaws.com</code>. Pod Identity association maps (cluster, namespace, SA) → role. Pods get creds via agent.'),
        Flashcard(front='Why Pod Identity > IRSA?', back='No per-cluster OIDC provider needed; trust policies uniform across clusters; cross-account is one association; agent handles the JWT-exchange complexity.'),
        Flashcard(front='IAM Identity Center role in EKS access?', back='Federated SSO. Corp SSO → IAM Identity Center → assume IAM role → access entry maps to K8s group → RBAC.'),
        Flashcard(front='When does aws-auth precedence kick in?', back='Both access entries + aws-auth can exist; for the same principal, access entries take precedence. Migrate by adding access entries; once verified, remove from aws-auth.'),
        Flashcard(front='ECR / Secrets Manager / KMS access from Pods?', back='Pod Identity association to a role with the relevant AWS permissions. SDKs in the Pod auto-pick up creds. No long-lived AWS access keys.'),
    ],
    quizzes=[
        Quiz(prompt='You\'re tasked with migrating a 2-year-old EKS cluster from aws-auth ConfigMap + IRSA to access entries + Pod Identity. Plan?', answer='<strong>Two parallel migrations.</strong> <strong>Migration A: aws-auth → access entries.</strong> (1) <strong>Audit current aws-auth</strong>: <code>kubectl -n kube-system get cm aws-auth -o yaml</code>. List every IAM principal + their K8s groups. (2) <strong>Create access entries</strong> for each principal via Terraform / eksctl. Both aws-auth + access entries can coexist; access entries take precedence. (3) <strong>Validate</strong> each principal can still authenticate (smoke-test with <code>kubectl auth can-i</code>). (4) <strong>Remove from aws-auth</strong> once validated. Final aws-auth = empty (just node groups\' system:nodes). <strong>Migration B: IRSA → Pod Identity.</strong> (1) <strong>Install Pod Identity Agent</strong> as a managed add-on. (2) <strong>Per-SA migration</strong>: create a Pod Identity association referencing the same IAM role; smoke-test from a Pod that the AWS SDK picks up creds; remove the IRSA annotation; restart the Pod. (3) <strong>Track progress</strong> in a sheet; ~1 SA per day for medium clusters. <strong>Total project</strong>: 2-4 weeks for a typical cluster.'),
        Quiz(prompt='Your team\'s aws-auth ConfigMap got corrupted; nobody can <code>kubectl</code>. What\'s the recovery without re-creating the cluster?', answer='<strong>Best path: pre-existing access entries.</strong> If you have an access entry for an IAM admin, that path is unaffected by the ConfigMap mistake. <code>aws eks update-kubeconfig</code> + immediately <code>kubectl edit cm aws-auth</code> to fix. <strong>If no access entries:</strong> (1) AWS Console: the cluster\'s creator IAM principal has implicit cluster-admin via the original create-cluster identity. Use that IAM principal\'s credentials. <code>aws sts assume-role</code> if it\'s a role. (2) <strong>Re-add yourself to aws-auth.</strong> (3) <strong>Then create access entries</strong> so this never happens again. <strong>Lesson:</strong> the EKS cluster creator role is your last-resort admin path. Document who/what created the cluster + maintain access to that identity. Migration to access entries removes this fragility.'),
        Quiz(prompt='You\'re asked to design EKS auth for a 4-team org with shared infrastructure. <strong>Click for the design. ▼</strong>', cyoa=True, cyoa_tag='the design', answer='<strong>(1) IAM Identity Center</strong> as the SSO source. Every human authenticates via corp SSO. <strong>(2) IAM permission sets</strong> per team (PlatformAdmin, AppDev, SRE, Auditor). Permission sets allow <code>eks:DescribeCluster</code> + role assumption. <strong>(3) Per-team IAM roles</strong> the permission sets assume into. Naming: <code>arn:aws:iam::123:role/team-a-app-dev</code>. <strong>(4) Per-cluster access entries</strong> mapping each team role to a K8s group. PlatformAdmin → <code>system:masters</code>. AppDev → <code>app-dev-team-a</code> group, with a namespace-scoped Role granting CRUD on Deployments + Services. <strong>(5) Pod Identity Agent</strong> per cluster. <strong>(6) Per-(namespace, SA) Pod Identity associations</strong> for AWS-service access. Per-team IAM roles for Pods (e.g., <code>team-a-app-pods</code> with read-only S3 in team-a buckets only). <strong>(7) GitOps for everything</strong>. All access entries, IAM roles, permission sets in Terraform / IaC. Audit trail in CloudTrail. <strong>Result:</strong> SSO → IAM → access entry → K8s group → namespace-Role. End-to-end identity flow. Zero shared kubeconfigs. Auditable.'),
    ],
    glossary=[
        GlossaryItem(name='AWS IAM (in EKS context)', definition='Controls who can call AWS EKS APIs + retrieve kubeconfig. Cluster-level identity.'),
        GlossaryItem(name='K8s RBAC (in EKS)', definition='Controls in-cluster permissions: get pods, edit deployments, etc. Standard K8s.'),
        GlossaryItem(name='Access entries', definition='Modern (2024 GA) EKS API for mapping IAM principals to K8s groups + access policies. Replaces aws-auth.'),
        GlossaryItem(name='aws-auth ConfigMap', definition='Legacy mechanism in <code>kube-system</code>. Maps IAM ARNs to K8s users/groups. Lockout-prone.'),
        GlossaryItem(name='Access policy (EKS)', definition='AWS-managed K8s permission bundle (e.g., AmazonEKSClusterAdminPolicy). Attached to access entries.'),
        GlossaryItem(name='IRSA', definition='IAM Roles for Service Accounts. Per-cluster OIDC provider + IAM trust policy + SA annotation. Legacy Pod-to-AWS path.'),
        GlossaryItem(name='EKS Pod Identity', definition='Modern Pod-to-AWS path. Pod Identity Agent + Pod Identity associations. Replaces IRSA.'),
        GlossaryItem(name='Pod Identity Agent', definition='Managed add-on. Provides AWS creds to Pods based on associations.'),
        GlossaryItem(name='Pod Identity association', definition='Maps (cluster, namespace, SA) → IAM role. Created via EKS API.'),
        GlossaryItem(name='IAM Identity Center', definition='AWS SSO. Federates human identities; permissions sets assume IAM roles per session.'),
        GlossaryItem(name='Permission set (Identity Center)', definition='Bundle of IAM policies + assignment rules. Maps SSO users to IAM roles per account.'),
        GlossaryItem(name='Cluster creator IAM principal', definition='The IAM identity that ran <code>eks:CreateCluster</code>. Implicit cluster-admin via system:masters mapping.'),
    ],
    recap_lead='IAM (cluster API) + K8s RBAC (in-cluster). Bridge via access entries (modern) or aws-auth (legacy). Pod-to-AWS-service via Pod Identity (modern) or IRSA (legacy). SSO via IAM Identity Center.',
    recap_next='<strong>Next — E5: EKS Storage.</strong> EBS / EFS / FSx CSI drivers, S3 Mountpoint, snapshots, KMS encryption, zone-aware provisioning.',
)
