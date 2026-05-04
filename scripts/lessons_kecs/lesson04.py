"""K-ECS C4 — IAM and Security."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS IAM + security — execution role, task role, Secrets Manager, KMS, VPC endpoints, ECR auth.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Customs House · K-Harbor — two letters of authority + the vault</text>
  <rect x="40" y="70" width="220" height="55" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="150" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">execution role</text>
  <text x="150" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">ECR + Secrets + Logs (launch-time)</text>
  <rect x="40" y="140" width="220" height="55" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="150" y="162" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">task role</text>
  <text x="150" y="178" text-anchor="middle" font-size="9" fill="#1F2433">app → S3, DynamoDB (runtime)</text>
  <rect x="280" y="70" width="200" height="55" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="380" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Secrets Manager / SSM</text>
  <text x="380" y="108" text-anchor="middle" font-size="9" fill="#1F2433">env injection at launch</text>
  <rect x="280" y="140" width="200" height="55" rx="10" fill="#5E4A8E" stroke="#1F2433"/>
  <text x="380" y="162" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">KMS</text>
  <text x="380" y="178" text-anchor="middle" font-size="9" fill="#FBF1D6">encrypts secrets + logs at rest</text>
  <rect x="500" y="70" width="220" height="55" rx="10" fill="#7AB3CC" stroke="#1F2433"/>
  <text x="610" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">VPC endpoints</text>
  <text x="610" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">ECR + Logs + SSM private</text>
  <rect x="500" y="140" width="220" height="55" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="610" y="162" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">compliance scopes</text>
  <text x="610" y="178" text-anchor="middle" font-size="9" fill="#FBF1D6">PCI / HIPAA / FedRAMP</text>
</svg>"""


LESSON = LessonSpec(
    num="04",
    title_short="IAM & security",
    title_full="C4 · IAM and Security — Roles, Secrets, KMS, ECR, VPC Endpoints",
    title_html="K-ECS C4 · IAM and Security",
    module_eyebrow="Module C4 · the Customs House — two letters of authority + the vault",
    hero_sub_html='Two roles per Task: <strong>execution role</strong> (launch-time AWS access — ECR pull, Secrets fetch, log writes) and <strong>task role</strong> (runtime app AWS calls). <strong>Secrets Manager / SSM Parameter Store</strong> inject values at Task launch (KMS-encrypted; never logged). <strong>ECR auth</strong> via the execution role; private-registry auth via repositoryCredentials + Secrets Manager. <strong>VPC endpoints</strong> for ECR / ECS / Logs / SSM keep traffic private. <strong>Fargate platform versions</strong> control patching; <em>LATEST</em> auto-updates, pinned versions for compliance freeze.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A Task is failing CannotPullContainerError on rollout. ECR repo policy looks fine. The execution role has ecr:GetAuthorizationToken. <em>It\'s the KMS key.</em> The image\'s ECR repo is encrypted with a customer KMS key the new execution role can\'t Decrypt. Pulls fail silently. Today\'s lesson: ECS-IAM has more interlocks than \"give the role the action\" — KMS, VPC endpoints, and resource policies all play.",
    stamp_html="<strong>Two roles, different lifecycles. Secrets injected at Task launch by execution role; never logged. KMS Decrypt is the most-forgotten policy on encrypted ECR + Secrets. VPC endpoints keep ECR/Logs/SSM traffic off the public Internet — and required in disconnected/regulated VPCs.</strong>",
    district_pin="kh-pier04",
    district_label="Customs House",
    sections=[
        Section(
            eyebrow="Section 1.1 · execution role vs task role",
            h2="Two roles, two lifecycles, two scopes",
            body_html="""    <p><strong>Execution role</strong> is assumed by the ECS agent / Fargate at Task launch. AWS-managed baseline policy: <code>AmazonECSTaskExecutionRolePolicy</code> (ECR pull, CloudWatch Logs writes). Add: <code>secretsmanager:GetSecretValue</code> for any Secrets Manager ARN you reference, <code>ssm:GetParameters</code> for SSM, <code>kms:Decrypt</code> for the KMS keys protecting those secrets and (if applicable) the ECR repo.</p>
    <p><strong>Task role</strong> is assumed by the running container code via the ECS metadata endpoint (<code>http://169.254.170.2/v2/credentials/...</code>). Scope to the actual AWS APIs your app calls — <code>s3:GetObject</code> on a specific bucket, <code>dynamodb:UpdateItem</code> on a specific table. <strong>Default-deny everything else.</strong> Use IAM Conditions where possible (<code>aws:SourceVpce</code>, <code>aws:PrincipalTag</code>).</p>
    <p>The two roles are <em>completely separate ARNs</em>. No inheritance. The container code never sees execution-role credentials; the agent never uses task-role credentials.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Secrets Manager / SSM injection + KMS",
            h2="Inject at launch; KMS gates Decrypt",
            body_html="""    <p>In Task Definition <code>containerDefinitions[].secrets</code>:</p>
    <pre><code>"secrets": [
  { "name": "DB_PASSWORD", "valueFrom": "arn:aws:secretsmanager:us-east-1:111122223333:secret:prod/db-AbCdEf" },
  { "name": "API_KEY",     "valueFrom": "arn:aws:ssm:us-east-1:111122223333:parameter/api-key" }
]</code></pre>
    <p>At Task launch the execution role calls <code>secretsmanager:GetSecretValue</code> + <code>kms:Decrypt</code> for the secret\'s KMS key. The plaintext is injected as an environment variable in the container. <em>Plaintext does not appear in CloudTrail; the GetSecretValue call does.</em> Rotate secrets via Secrets Manager rotation Lambda; restart Tasks to pick up new values (or use AWS SDK to fetch on-demand from inside the app, signed by the task role).</p>
    <p><strong>KMS pitfall</strong>: customer-managed KMS keys protecting Secrets Manager secrets need <em>two</em> things. (1) The key policy must allow the execution role <code>kms:Decrypt</code>. (2) The execution role policy must allow <code>kms:Decrypt</code> on that key ARN. Missing either side = silent failure at Task launch with stoppedReason ResourceInitializationError.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · ECR auth + private-registry auth + VPC endpoints",
            h2="Image pull paths and how to keep them off the public Internet",
            body_html="""    <p><strong>ECR private repos</strong>: execution role needs <code>ecr:GetAuthorizationToken</code> + <code>ecr:BatchCheckLayerAvailability</code> + <code>ecr:GetDownloadUrlForLayer</code> + <code>ecr:BatchGetImage</code>. ECR repo policy must allow the execution-role principal. If repo is KMS-encrypted, also <code>kms:Decrypt</code> on the repo\'s KMS key.</p>
    <p><strong>Private registries</strong> (Docker Hub paid, GHCR, GitLab Registry): use <code>repositoryCredentials</code> in the Task Definition pointing to a Secrets Manager secret with <code>{"username": "...", "password": "..."}</code>. Execution role gets GetSecretValue on that secret. ECS pulls using those creds.</p>
    <p><strong>VPC endpoints</strong> for ECR / ECS / CloudWatch Logs / SSM / Secrets Manager / STS: keep all control-plane and image-pull traffic on private network — required for disconnected VPCs (no NAT gateway / no public subnets), faster pulls (less hop count), and reduced cost (no NAT gateway data charges). Endpoints needed for ECR pull: <code>com.amazonaws.region.ecr.api</code>, <code>com.amazonaws.region.ecr.dkr</code>, <code>com.amazonaws.region.s3</code> (Gateway endpoint — image layers are S3-backed), CloudWatch Logs, STS.</p>
    <p><strong>Security Groups</strong>: VPC endpoint network interfaces have their own SGs; allow inbound from Task SGs on TCP/443.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · Fargate platform versions, patching, compliance",
            h2="Platform versions, OS patching, regulated workloads",
            body_html="""    <p><strong>Fargate platform versions</strong>: each Task runs on a specific Fargate platform version (e.g., 1.4.0). New platform versions ship with patched kernels + runtime fixes. Pin in <code>platformVersion</code> field of the Service. <em>LATEST</em> = auto-update on Task replacement (good default). Pin to a specific version for compliance change-control or deterministic rollouts.</p>
    <p><strong>EC2-launch patching</strong>: AWS-managed. The ECS-optimised AMI (Amazon Linux 2023 or Bottlerocket) gets new versions; you bake them into your launch templates and roll instances. ECS Managed Instances launch type automates the AMI lifecycle for you. Bottlerocket is the modern choice — minimal container-host OS with atomic updates and rollback.</p>
    <p><strong>Compliance scopes</strong>:</p>
    <ul>
      <li><strong>PCI DSS</strong> — ECS is in scope; design Cluster + Task Definitions + IAM roles + KMS as you would any PCI workload (segmentation via SG, encryption-at-rest, encryption-in-transit, least-privilege roles, audit logging via CloudTrail + ECS event stream).</li>
      <li><strong>HIPAA</strong> — ECS + Fargate are HIPAA-eligible; sign a BAA with AWS; ensure all integrated services (S3, RDS, EFS, KMS) are HIPAA-eligible and properly configured.</li>
      <li><strong>FedRAMP</strong> — ECS available in GovCloud (US) regions and FedRAMP High accounts; use FIPS endpoints; ensure all dependencies meet FedRAMP boundary.</li>
    </ul>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A container starts but immediately fails its first S3 PutObject call with AccessDenied. Where do you look first?",
            options=[
                ("Execution role permissions.", False),
                ("Task role permissions.", True),
                ("ECS agent IAM.", False),
            ],
            feedback="Runtime AWS calls from the running container use the task role. AccessDenied at runtime = task role missing the action or the resource isn\'t in the policy\'s Resource list.",
        ),
        3: PauseCheck(
            question="A Task fails ResourceInitializationError when fetching Secrets. The execution role policy looks fine. What\'s a likely missed piece?",
            options=[
                ("Task role missing <code>secretsmanager:GetSecretValue</code>.", False),
                ("Execution role missing <code>kms:Decrypt</code> on the secret\'s KMS key.", True),
                ("VPC endpoints not set up.", False),
            ],
            feedback="Customer-managed KMS keys require kms:Decrypt on the execution role + key policy allowing the role principal. The secret fetch is the loud failure mode of a missing KMS Decrypt.",
        ),
    },
    before_after_before='<p>Pre-task-role / pre-Secrets-Manager, ECS workloads stuffed AWS credentials into env vars at deploy time, baked them into images, or shared host-level credentials across all Tasks. Secret rotation was a deploy event. KMS encryption was best-effort. Compliance audits found credentials sprayed across CloudFormation, scripts, repos.</p>',
    before_after_after='<p>Modern ECS IAM uses the two-role split, KMS-encrypted Secrets Manager / SSM with execution-role-fetched at launch (no creds in source), task role for runtime app calls (least-privilege per Task), VPC endpoints to keep traffic private, and pinned Fargate platform versions for compliance change-control. Audits map to specific role policies + KMS key policies + endpoint SGs. <em>Workload-scoped, audit-friendly.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Two roles, two policies, one KMS key per concern. Get this right and most security questions are mechanical.</em></p>',
    analogy_intro_html='''<p>The <strong>Customs House</strong> at the harbor is where authority is checked. Every captain (Task) carries two letters from the port authority. The <strong>boarding letter</strong> (execution role) is signed for one purpose only — it lets the dock crew unlock the warehouse (ECR), open the secrets vault (Secrets Manager / SSM), and stamp the logbook (CloudWatch Logs). The dock crew use it once at boarding and never again.</p>
    <p>The <strong>voyage letter</strong> (task role) goes with the captain on the journey. It opens specific port doors at specific destinations: this letter says "captain may unload at S3 bucket X" or "captain may load at DynamoDB table Y." Anything not explicitly listed is denied.</p>
    <p>The customs vault holds <strong>sealed envelopes</strong> (Secrets) — passwords, API keys, certificates. The vault is double-locked: once with the lock the dock crew has the key for (execution-role policy), and once with a master vault key (KMS) which has its <em>own</em> access list. The dock crew need both keys, every time. Forgetting the vault key (KMS Decrypt) is the most common reason a captain can\'t board.</p>
    <p>For sensitive shipments, the harbor has <em>private inland canals</em> (VPC endpoints) to the warehouse, the vault, and the logbook archive — never going out to the public sea. Some shipments (PCI / HIPAA / FedRAMP) are <em>required</em> to use the canals, not the open sea.</p>''',
    translation_rows=[
        ("Boarding letter (one-time use, dock crew)", "execution role — image pull + Secrets fetch + logs"),
        ("Voyage letter (captain carries on journey)", "task role — running app\'s AWS calls"),
        ("Customs vault sealed envelopes", "Secrets Manager / SSM Parameter Store"),
        ("Vault\'s master key (separate access list)", "KMS customer key + key policy"),
        ("Warehouse access stamp", "ECR auth (GetAuthorizationToken + …)"),
        ("Foreign-warehouse paperwork", "repositoryCredentials → Secrets Manager"),
        ("Private inland canals", "VPC endpoints (ECR / Logs / SSM / Secrets Manager)"),
        ("Harbor canal access list", "VPC endpoint SG + endpoint policy"),
        ("Captain\'s vehicle inspection cycle", "Fargate platform version (LATEST or pinned)"),
        ("Customs compliance scopes", "PCI DSS, HIPAA, FedRAMP boundaries"),
    ],
    analogy_stops="A real customs house has paper letters; ECS roles are IAM ARNs the AWS API checks on every request. There is no \"physical letter\" to forge or lose; all auth lives in policy.",
    eli5="Every ship has two letters. One letter the dock crew uses at boarding to unlock the warehouse and the secrets vault. The other letter the captain carries to open doors at other harbors. Different letters, different jobs. The secrets vault has two locks; you need both keys to open it. For sensitive cargo, ships use private inland canals instead of the open sea.",
    eli10="<strong>Execution role</strong>: ECR pull + Secrets fetch + CloudWatch Logs (launch-time, used by ECS agent / Fargate). <strong>Task role</strong>: app\'s runtime AWS calls (assumed via metadata endpoint inside the container). <strong>Secrets Manager / SSM injection</strong>: in <code>secrets</code> array; KMS-encrypted; both execution-role policy AND KMS key policy must allow Decrypt. <strong>ECR auth</strong>: managed-policy baseline + KMS Decrypt for KMS-encrypted repos. <strong>Private-registry auth</strong>: repositoryCredentials → Secrets Manager. <strong>VPC endpoints</strong>: ECR.api + ECR.dkr + S3 Gateway + Logs + STS + SSM + Secrets Manager. <strong>Fargate platform versions</strong>: LATEST or pinned. <strong>Compliance</strong>: PCI / HIPAA / FedRAMP — use FIPS endpoints in regulated boundaries.",
    scenarios=[
        Scenario(
            name="HIPAA — every secret KMS-encrypted with customer keys",
            body="A health-tech runs PHI-handling Tasks. All secrets in Secrets Manager use customer-managed KMS keys (one per environment); execution roles allow only that env\'s KMS key Decrypt. Task role allows specific S3 PHI-bucket reads, conditioned on <code>aws:RequestTag/Patient</code>. CloudTrail captures every Secret fetch. <em>Audit maps cleanly to role policies + key policies.</em>",
        ),
        Scenario(
            name="Disconnected VPC — image pulls via endpoints only",
            body="A regulated workload runs in private subnets with no NAT gateway. VPC endpoints for <code>ecr.api</code>, <code>ecr.dkr</code>, <code>s3</code> (gateway), <code>logs</code>, <code>sts</code>, <code>secretsmanager</code>, <code>ssm</code>. ECS Tasks pull images, fetch secrets, write logs entirely on private network. <em>No public Internet egress; satisfies the network-isolation control.</em>",
        ),
        Scenario(
            name="Quarterly secret rotation — Lambda + Tasks",
            body="A Service stores a database password in Secrets Manager with quarterly rotation. The rotation Lambda updates the secret + the database password atomically. ECS Service has a CloudWatch Events rule on Secret rotation success → triggers <code>UpdateService --force-new-deployment</code>. Tasks restart, fetch the new password via execution role, run with new creds. <em>No human in the loop.</em>",
        ),
        Scenario(
            name="Outage — execution role lost KMS Decrypt",
            body="A team rotated KMS keys and updated key policies but forgot to update <em>execution-role policy</em> to reference the new key ARN. Next deploy: every Task ResourceInitializationError. 25-minute outage until the policy was patched. <em>Postmortem</em>: KMS Decrypt is the most-forgotten ECS-IAM piece; runbook now requires testing in dev with the new key before prod rotation.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"If the role policy allows the action, the call will succeed.\"",
            truth="Multiple gates: role policy, resource policy (KMS key, ECR repo, S3 bucket, Secret), VPC endpoint policy, SCP at the org level, permissions boundary. Any one of them denying = the call fails. Especially KMS — both <em>role policy AND key policy</em> must allow Decrypt for customer-managed keys.",
        ),
        Misconception(
            myth="\"Fargate is auto-patched, so we don\'t need to think about platform versions.\"",
            truth="Fargate platform versions <em>do</em> get patched, but only when Tasks restart with <code>LATEST</code> (or you pin a newer version). A long-lived Service whose Tasks haven\'t cycled may run an older platform version with known CVEs. Force-deployment periodically or use Fargate platform-version pinning + scheduled rotation.",
        ),
        Misconception(
            myth="\"VPC endpoints just save NAT cost.\"",
            truth="Saving NAT cost is a side benefit. The real wins: (1) keep traffic on private network — required for many compliance baselines; (2) faster pulls (fewer hops); (3) more deterministic latency; (4) endpoint policies as a second auth layer. <em>Disconnected VPCs are impossible without VPC endpoints.</em>",
        ),
    ],
    flashcards=[
        Flashcard(front="Execution role — what does it do?", back="Assumed by ECS agent / Fargate at Task <em>launch</em>. ECR pull, fetch Secrets Manager / SSM, write CloudWatch Logs. AWS-managed baseline: <code>AmazonECSTaskExecutionRolePolicy</code>. Add KMS Decrypt for encrypted secrets and ECR."),
        Flashcard(front="Task role — what does it do?", back="Assumed by the <em>running container code</em> via the ECS metadata endpoint. Scope to the actual AWS APIs the app calls. Default-deny; use IAM Conditions for fine-grained scoping."),
        Flashcard(front="Two ways to inject secrets at Task launch?", back="<code>containerDefinitions[].secrets</code> — array of <code>{name, valueFrom: arn-of-secret-or-parameter}</code>. valueFrom can be Secrets Manager ARN or SSM Parameter ARN. Plaintext injected as env var; never logged."),
        Flashcard(front="The most-forgotten ECS-IAM policy?", back="<code>kms:Decrypt</code> on the customer-managed KMS key protecting Secrets Manager secrets or KMS-encrypted ECR repos. Both <em>role policy</em> AND <em>key policy</em> must allow it."),
        Flashcard(front="VPC endpoints needed for ECR pulls in disconnected VPCs?", back="<code>com.amazonaws.region.ecr.api</code>, <code>com.amazonaws.region.ecr.dkr</code>, <code>com.amazonaws.region.s3</code> (Gateway — image layers are S3), CloudWatch Logs, STS, Secrets Manager, SSM."),
        Flashcard(front="Fargate platform versions — pin or LATEST?", back="<strong>LATEST</strong> = auto-update on Task replacement (good default; gets patches). <strong>Pin</strong> = deterministic rollouts; required for some compliance change-control regimes. Cycle Tasks regularly when pinned to absorb patches."),
        Flashcard(front="Private-registry auth — how?", back="<code>repositoryCredentials</code> in the container definition pointing to a Secrets Manager secret containing <code>{username, password}</code>. Execution role allows <code>secretsmanager:GetSecretValue</code> on that secret + <code>kms:Decrypt</code> for its KMS key."),
        Flashcard(front="Compliance scopes for ECS?", back="<strong>PCI DSS</strong> in scope (segmentation via SG; encryption; least-privilege; audit logging). <strong>HIPAA-eligible</strong> with BAA. <strong>FedRAMP</strong> in GovCloud (US) and FedRAMP High accounts (use FIPS endpoints)."),
    ],
    quizzes=[
        Quiz(
            prompt="A new ECS Service deploys; Tasks fail with stoppedReason \"ResourceInitializationError: unable to retrieve secret value\". Walk through the diagnostic steps in order.",
            answer="(1) Read the full <strong>stoppedReason</strong> + look for the secret ARN in the message. (2) Confirm the <strong>execution role policy</strong> allows <code>secretsmanager:GetSecretValue</code> on that ARN (or <code>ssm:GetParameters</code> for SSM). (3) Read the <strong>secret\'s KMS key policy</strong> — does it allow the execution role principal <code>kms:Decrypt</code>? Customer-managed keys need both sides. (4) Check <strong>execution role policy</strong> for <code>kms:Decrypt</code> on that key ARN. (5) If using VPC endpoints, verify the <strong>Secrets Manager VPC endpoint</strong> exists + its endpoint policy doesn\'t block the call. (6) Look in <strong>CloudTrail</strong> for the GetSecretValue call — the error there usually names the missing permission.",
        ),
        Quiz(
            prompt="A team\'s task role allows <code>s3:*</code> on <code>arn:aws:s3:::data-bucket/*</code>. The CISO wants this tightened. What\'s the right scope?",
            answer="Three tightenings layered: (1) <strong>Specific actions</strong> — replace <code>s3:*</code> with the actual actions the app uses (<code>s3:GetObject</code>, <code>s3:PutObject</code>, <code>s3:ListBucket</code>). (2) <strong>Path scoping</strong> — replace <code>data-bucket/*</code> with <code>data-bucket/customer-uploads/*</code> if that\'s the only path. (3) <strong>IAM Conditions</strong> — <code>aws:SourceVpce</code> requires the call come from a specific VPC endpoint; <code>aws:RequestTag/Customer</code> matches the request to the user. Plus <strong>S3 bucket policy</strong> as defense in depth — explicit Allow only for this task role; explicit Deny for everything else.",
        ),
        Quiz(
            prompt="An auditor asks: \"How do you guarantee that an ECS Task\'s container code can never see the credentials your CI/CD pipeline used to deploy it?\" Defend the design.",
            answer="\"<strong>The container code never has any path to the deploy credentials. Three barriers:</strong> (1) Deploy creds (CI/CD role) only call <code>ecs:UpdateService</code>, <code>ecs:RegisterTaskDefinition</code>, <code>iam:PassRole</code> — never assumed by Tasks. (2) The <em>execution role</em> the Tasks use at launch is a separate ARN, scoped narrowly to ECR pull + Secrets fetch + log writes; it has no overlap with the CI/CD role and is not assumable by anything outside of ECS-launch. (3) The <em>task role</em> the running container code assumes via the metadata endpoint is yet a third ARN, with only the runtime AWS APIs the app calls; the container code can\'t even <em>see</em> the execution-role credentials, let alone the CI/CD ones — they\'re held by ECS, not exposed to the container. <strong>Three roles, three scopes, three lifecycles. The container code\'s blast radius is the task role only.</strong>\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the auditor",
        ),
    ],
    glossary=[
        GlossaryItem(name="execution role", definition="IAM role assumed by ECS agent / Fargate at Task launch — image pull, fetch Secrets, write logs."),
        GlossaryItem(name="task role", definition="IAM role assumed by running container code via ECS metadata endpoint — app\'s runtime AWS calls."),
        GlossaryItem(name="containerDefinitions[].secrets", definition="Array injecting Secrets Manager / SSM values as env vars at Task launch. Plaintext never logged."),
        GlossaryItem(name="kms:Decrypt", definition="The most-forgotten ECS-IAM policy. Required on execution role for customer-managed KMS keys protecting secrets or ECR."),
        GlossaryItem(name="repositoryCredentials", definition="Task Definition field pointing at a Secrets Manager secret with private-registry creds."),
        GlossaryItem(name="VPC endpoints (ECR / Logs / SSM)", definition="Private connectivity to AWS services from a VPC. Required for disconnected VPCs; reduces NAT cost."),
        GlossaryItem(name="Fargate platform version", definition="Versioned Fargate runtime. LATEST auto-updates on Task replacement; pinned versions for change-control."),
        GlossaryItem(name="Bottlerocket", definition="Minimal container-host OS; atomic updates with rollback. Modern ECS-optimised AMI choice."),
        GlossaryItem(name="ECS Managed Instances", definition="Launch type where AWS automates the EC2 + AMI lifecycle while you keep EC2-style features (Spot, GPU, custom AMIs)."),
        GlossaryItem(name="ECS metadata endpoint", definition="In-Task HTTP endpoint at 169.254.170.2 — exposes task role credentials, Task metadata, container stats."),
    ],
    recap_lead="ECS security is two roles, three policy layers (role + resource + KMS), VPC endpoints for private traffic, Fargate platform-version hygiene, and compliance scopes mapped to specific service configurations. Get the role split clean and the rest is mechanical.",
    recap_next='<strong>Next — C5: ECS Storage.</strong> Bind mounts; Docker volumes; EFS (RWX-equivalent); FSx for Windows / NetApp ONTAP; ephemeral storage tuning; per-Task vs cross-Task lifetime; mountPoint patterns.',
    architecture_svg='''<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS IAM + security: execution role vs task role; Secrets Manager + KMS; VPC endpoints; ECR auth.">
  <rect x="10" y="10" width="740" height="220" rx="12" fill="#FBF7F0" stroke="#A04832"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">ECS IAM · TWO ROLES + KMS-ENCRYPTED SECRETS + VPC ENDPOINTS</text>
  <rect x="20" y="50" width="200" height="60" rx="6" fill="#3F4A5E"/>
  <text x="120" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">execution role</text>
  <text x="120" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">launch-time · agent uses</text>
  <text x="120" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">ECR pull + Secrets fetch + logs</text>
  <line x1="220" y1="80" x2="250" y2="80" stroke="#5A4F45" stroke-width="2" marker-end="url(#aC4)"/>
  <defs><marker id="aC4" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><polygon points="0 0, 10 5, 0 10" fill="#5A4F45"/></marker></defs>
  <rect x="250" y="50" width="200" height="60" rx="6" fill="#FF9900"/>
  <text x="350" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">ECR + Secrets Manager + SSM</text>
  <text x="350" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">image · creds · API keys</text>
  <text x="350" y="100" text-anchor="middle" font-size="8" fill="#1F2433">customer KMS keys</text>
  <line x1="450" y1="80" x2="480" y2="80" stroke="#5A4F45" stroke-width="2" marker-end="url(#aC4)"/>
  <rect x="480" y="50" width="260" height="60" rx="6" fill="#5DCAA5"/>
  <text x="610" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Task running with task role</text>
  <text x="610" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">runtime · ECS metadata endpoint</text>
  <text x="610" y="100" text-anchor="middle" font-size="8" fill="#1F2433">app→S3/DynamoDB/SQS</text>
  <rect x="20" y="125" width="350" height="55" rx="6" fill="#5A6B81"/>
  <text x="195" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">VPC endpoints</text>
  <text x="195" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">ECR.api · ECR.dkr · S3 · Logs · STS · SSM · SecretsManager</text>
  <text x="195" y="174" text-anchor="middle" font-size="8" fill="#FBE8DC">disconnected VPCs require these</text>
  <rect x="380" y="125" width="360" height="55" rx="6" fill="#5E4A8E"/>
  <text x="560" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">KMS — root of trust</text>
  <text x="560" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">customer-managed keys for Secrets + ECR + ephemeralStorage</text>
  <text x="560" y="174" text-anchor="middle" font-size="8" fill="#FBE8DC">execution role needs kms:Decrypt (most-forgotten policy)</text>
  <rect x="20" y="195" width="720" height="30" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="215" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">Compliance: PCI · HIPAA-eligible · FedRAMP (GovCloud) — map to specific role / KMS / VPC endpoint config</text>
</svg>''',
    architecture_caption='Two roles, two lifecycles: execution role at launch (ECR pull + Secrets fetch + logs); task role at runtime (app\'s AWS calls). KMS protects everything; execution role needs kms:Decrypt on customer-managed keys. VPC endpoints keep traffic private.',
)
