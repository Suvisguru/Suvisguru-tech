# K-ECS C4 — C4 · IAM and Security — Roles, Secrets, KMS, ECR, VPC Endpoints

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C4 · IAM and Security
> Companion preview: `/preview-kubernetes-ecs-lesson-04.html`.

---

**🎯 If you remember nothing else:** **Two roles, different lifecycles. Secrets injected at Task launch by execution role; never logged. KMS Decrypt is the most-forgotten policy on encrypted ECR + Secrets. VPC endpoints keep ECR/Logs/SSM traffic off the public Internet — and required in disconnected/regulated VPCs.**

## 1. Two roles, two lifecycles, two scopes

**Execution role** is assumed by the ECS agent / Fargate at Task launch. AWS-managed baseline policy: `AmazonECSTaskExecutionRolePolicy` (ECR pull, CloudWatch Logs writes). Add: `secretsmanager:GetSecretValue` for any Secrets Manager ARN you reference, `ssm:GetParameters` for SSM, `kms:Decrypt` for the KMS keys protecting those secrets and (if applicable) the ECR repo.
    **Task role** is assumed by the running container code via the ECS metadata endpoint (`http://169.254.170.2/v2/credentials/...`). Scope to the actual AWS APIs your app calls — `s3:GetObject` on a specific bucket, `dynamodb:UpdateItem` on a specific table. **Default-deny everything else.** Use IAM Conditions where possible (`aws:SourceVpce`, `aws:PrincipalTag`).
    The two roles are *completely separate ARNs*. No inheritance. The container code never sees execution-role credentials; the agent never uses task-role credentials.

## 2. Inject at launch; KMS gates Decrypt

In Task Definition `containerDefinitions[].secrets`:
    `"secrets": [
  { "name": "DB_PASSWORD", "valueFrom": "arn:aws:secretsmanager:us-east-1:111122223333:secret:prod/db-AbCdEf" },
  { "name": "API_KEY",     "valueFrom": "arn:aws:ssm:us-east-1:111122223333:parameter/api-key" }
]`
    At Task launch the execution role calls `secretsmanager:GetSecretValue` + `kms:Decrypt` for the secret's KMS key. The plaintext is injected as an environment variable in the container. *Plaintext does not appear in CloudTrail; the GetSecretValue call does.* Rotate secrets via Secrets Manager rotation Lambda; restart Tasks to pick up new values (or use AWS SDK to fetch on-demand from inside the app, signed by the task role).
    **KMS pitfall**: customer-managed KMS keys protecting Secrets Manager secrets need *two* things. (1) The key policy must allow the execution role `kms:Decrypt`. (2) The execution role policy must allow `kms:Decrypt` on that key ARN. Missing either side = silent failure at Task launch with stoppedReason ResourceInitializationError.

## 3. Image pull paths and how to keep them off the public Internet

**ECR private repos**: execution role needs `ecr:GetAuthorizationToken` + `ecr:BatchCheckLayerAvailability` + `ecr:GetDownloadUrlForLayer` + `ecr:BatchGetImage`. ECR repo policy must allow the execution-role principal. If repo is KMS-encrypted, also `kms:Decrypt` on the repo's KMS key.
    **Private registries** (Docker Hub paid, GHCR, GitLab Registry): use `repositoryCredentials` in the Task Definition pointing to a Secrets Manager secret with `{"username": "...", "password": "..."}`. Execution role gets GetSecretValue on that secret. ECS pulls using those creds.
    **VPC endpoints** for ECR / ECS / CloudWatch Logs / SSM / Secrets Manager / STS: keep all control-plane and image-pull traffic on private network — required for disconnected VPCs (no NAT gateway / no public subnets), faster pulls (less hop count), and reduced cost (no NAT gateway data charges). Endpoints needed for ECR pull: `com.amazonaws.region.ecr.api`, `com.amazonaws.region.ecr.dkr`, `com.amazonaws.region.s3` (Gateway endpoint — image layers are S3-backed), CloudWatch Logs, STS.
    **Security Groups**: VPC endpoint network interfaces have their own SGs; allow inbound from Task SGs on TCP/443.

## 4. Platform versions, OS patching, regulated workloads

**Fargate platform versions**: each Task runs on a specific Fargate platform version (e.g., 1.4.0). New platform versions ship with patched kernels + runtime fixes. Pin in `platformVersion` field of the Service. *LATEST* = auto-update on Task replacement (good default). Pin to a specific version for compliance change-control or deterministic rollouts.
    **EC2-launch patching**: AWS-managed. The ECS-optimised AMI (Amazon Linux 2023 or Bottlerocket) gets new versions; you bake them into your launch templates and roll instances. ECS Managed Instances launch type automates the AMI lifecycle for you. Bottlerocket is the modern choice — minimal container-host OS with atomic updates and rollback.
    **Compliance scopes**:
    
      - **PCI DSS** — ECS is in scope; design Cluster + Task Definitions + IAM roles + KMS as you would any PCI workload (segmentation via SG, encryption-at-rest, encryption-in-transit, least-privilege roles, audit logging via CloudTrail + ECS event stream).

      - **HIPAA** — ECS + Fargate are HIPAA-eligible; sign a BAA with AWS; ensure all integrated services (S3, RDS, EFS, KMS) are HIPAA-eligible and properly configured.

      - **FedRAMP** — ECS available in GovCloud (US) regions and FedRAMP High accounts; use FIPS endpoints; ensure all dependencies meet FedRAMP boundary.

## Before / After

**Before.** Pre-task-role / pre-Secrets-Manager, ECS workloads stuffed AWS credentials into env vars at deploy time, baked them into images, or shared host-level credentials across all Tasks. Secret rotation was a deploy event. KMS encryption was best-effort. Compliance audits found credentials sprayed across CloudFormation, scripts, repos.

**After.** Modern ECS IAM uses the two-role split, KMS-encrypted Secrets Manager / SSM with execution-role-fetched at launch (no creds in source), task role for runtime app calls (least-privilege per Task), VPC endpoints to keep traffic private, and pinned Fargate platform versions for compliance change-control. Audits map to specific role policies + KMS key policies + endpoint SGs. *Workload-scoped, audit-friendly.*

*Two roles, two policies, one KMS key per concern. Get this right and most security questions are mechanical.*

## Analogy — the K-Harbor pier

The **Customs House** at the harbor is where authority is checked. Every captain (Task) carries two letters from the port authority. The **boarding letter** (execution role) is signed for one purpose only — it lets the dock crew unlock the warehouse (ECR), open the secrets vault (Secrets Manager / SSM), and stamp the logbook (CloudWatch Logs). The dock crew use it once at boarding and never again.
    The **voyage letter** (task role) goes with the captain on the journey. It opens specific port doors at specific destinations: this letter says "captain may unload at S3 bucket X" or "captain may load at DynamoDB table Y." Anything not explicitly listed is denied.
    The customs vault holds **sealed envelopes** (Secrets) — passwords, API keys, certificates. The vault is double-locked: once with the lock the dock crew has the key for (execution-role policy), and once with a master vault key (KMS) which has its *own* access list. The dock crew need both keys, every time. Forgetting the vault key (KMS Decrypt) is the most common reason a captain can't board.
    For sensitive shipments, the harbor has *private inland canals* (VPC endpoints) to the warehouse, the vault, and the logbook archive — never going out to the public sea. Some shipments (PCI / HIPAA / FedRAMP) are *required* to use the canals, not the open sea.

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Boarding letter (one-time use, dock crew) | execution role — image pull + Secrets fetch + logs |
| Voyage letter (captain carries on journey) | task role — running app's AWS calls |
| Customs vault sealed envelopes | Secrets Manager / SSM Parameter Store |
| Vault's master key (separate access list) | KMS customer key + key policy |
| Warehouse access stamp | ECR auth (GetAuthorizationToken + …) |
| Foreign-warehouse paperwork | repositoryCredentials → Secrets Manager |
| Private inland canals | VPC endpoints (ECR / Logs / SSM / Secrets Manager) |
| Harbor canal access list | VPC endpoint SG + endpoint policy |
| Captain's vehicle inspection cycle | Fargate platform version (LATEST or pinned) |
| Customs compliance scopes | PCI DSS, HIPAA, FedRAMP boundaries |

⚠️ *Analogy stops here:* A real customs house has paper letters; ECS roles are IAM ARNs the AWS API checks on every request. There is no "physical letter" to forge or lose; all auth lives in policy.

## ELI5 / ELI10

**ELI5.** Every ship has two letters. One letter the dock crew uses at boarding to unlock the warehouse and the secrets vault. The other letter the captain carries to open doors at other harbors. Different letters, different jobs. The secrets vault has two locks; you need both keys to open it. For sensitive cargo, ships use private inland canals instead of the open sea.

**ELI10.** **Execution role**: ECR pull + Secrets fetch + CloudWatch Logs (launch-time, used by ECS agent / Fargate). **Task role**: app's runtime AWS calls (assumed via metadata endpoint inside the container). **Secrets Manager / SSM injection**: in `secrets` array; KMS-encrypted; both execution-role policy AND KMS key policy must allow Decrypt. **ECR auth**: managed-policy baseline + KMS Decrypt for KMS-encrypted repos. **Private-registry auth**: repositoryCredentials → Secrets Manager. **VPC endpoints**: ECR.api + ECR.dkr + S3 Gateway + Logs + STS + SSM + Secrets Manager. **Fargate platform versions**: LATEST or pinned. **Compliance**: PCI / HIPAA / FedRAMP — use FIPS endpoints in regulated boundaries.

## Real-world scenarios

- **HIPAA — every secret KMS-encrypted with customer keys.** A health-tech runs PHI-handling Tasks. All secrets in Secrets Manager use customer-managed KMS keys (one per environment); execution roles allow only that env's KMS key Decrypt. Task role allows specific S3 PHI-bucket reads, conditioned on `aws:RequestTag/Patient`. CloudTrail captures every Secret fetch. *Audit maps cleanly to role policies + key policies.*
- **Disconnected VPC — image pulls via endpoints only.** A regulated workload runs in private subnets with no NAT gateway. VPC endpoints for `ecr.api`, `ecr.dkr`, `s3` (gateway), `logs`, `sts`, `secretsmanager`, `ssm`. ECS Tasks pull images, fetch secrets, write logs entirely on private network. *No public Internet egress; satisfies the network-isolation control.*
- **Quarterly secret rotation — Lambda + Tasks.** A Service stores a database password in Secrets Manager with quarterly rotation. The rotation Lambda updates the secret + the database password atomically. ECS Service has a CloudWatch Events rule on Secret rotation success → triggers `UpdateService --force-new-deployment`. Tasks restart, fetch the new password via execution role, run with new creds. *No human in the loop.*
- **Outage — execution role lost KMS Decrypt.** A team rotated KMS keys and updated key policies but forgot to update *execution-role policy* to reference the new key ARN. Next deploy: every Task ResourceInitializationError. 25-minute outage until the policy was patched. *Postmortem*: KMS Decrypt is the most-forgotten ECS-IAM piece; runbook now requires testing in dev with the new key before prod rotation.

## Common misconceptions

- **Myth:** "If the role policy allows the action, the call will succeed."
  **Truth:** Multiple gates: role policy, resource policy (KMS key, ECR repo, S3 bucket, Secret), VPC endpoint policy, SCP at the org level, permissions boundary. Any one of them denying = the call fails. Especially KMS — both *role policy AND key policy* must allow Decrypt for customer-managed keys.
- **Myth:** "Fargate is auto-patched, so we don't need to think about platform versions."
  **Truth:** Fargate platform versions *do* get patched, but only when Tasks restart with `LATEST` (or you pin a newer version). A long-lived Service whose Tasks haven't cycled may run an older platform version with known CVEs. Force-deployment periodically or use Fargate platform-version pinning + scheduled rotation.
- **Myth:** "VPC endpoints just save NAT cost."
  **Truth:** Saving NAT cost is a side benefit. The real wins: (1) keep traffic on private network — required for many compliance baselines; (2) faster pulls (fewer hops); (3) more deterministic latency; (4) endpoint policies as a second auth layer. *Disconnected VPCs are impossible without VPC endpoints.*

## Recap

ECS security is two roles, three policy layers (role + resource + KMS), VPC endpoints for private traffic, Fargate platform-version hygiene, and compliance scopes mapped to specific service configurations. Get the role split clean and the rest is mechanical.

**Next — C5: ECS Storage.** Bind mounts; Docker volumes; EFS (RWX-equivalent); FSx for Windows / NetApp ONTAP; ephemeral storage tuning; per-Task vs cross-Task lifetime; mountPoint patterns.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
