# K-EKS E4 — E4 · Identity and Access (Access Entries, IRSA, Pod Identity)

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E4 · Identity and Access
> Companion preview: `/preview-kubernetes-eks-lesson-04.html`.

---

**🎯 If you remember nothing else:** Two identity layers: **AWS IAM** (cluster API access — CreateCluster, DescribeNodegroup, kubeconfig retrieval) and **K8s RBAC** (in-cluster — get pods, edit deployments). Map IAM → K8s via **access entries** (modern, recommended) or **aws-auth ConfigMap** (legacy, fragile). For Pod-to-AWS-service: **EKS Pod Identity** (Pod Identity Agent + association API — modern, simpler) or **IRSA** (OIDC provider + IAM trust policy — legacy but still common).

## 1. Two identity surfaces

EKS has two identity systems running in parallel:
    
      - **AWS IAM** — Who can call AWS EKS APIs (`eks:CreateCluster`, `eks:DescribeNodegroup`, `eks:UpdateClusterConfig`). Also: who can retrieve a kubeconfig (`aws eks update-kubeconfig`). IAM principals are users / roles / federated identities.

      - **K8s RBAC** — Who can do what *inside* the cluster (get pods, edit deployments, read secrets). RBAC subjects are K8s users / groups / ServiceAccounts.

    
    The bridge is the **access entry** (or legacy `aws-auth` ConfigMap): "this AWS IAM principal maps to this K8s username + group, which the cluster's ClusterRoleBindings reference." Without the bridge, an IAM admin gets a kubeconfig but can't list a Pod.

## 2. The modern path + the legacy hazard

**Access entries** (released GA 2024) are the modern path. Configured via the EKS API (or eksctl / Terraform); each access entry maps an IAM principal ARN to a K8s username + groups + access-policy. AWS validates the mapping before applying.
    `aws eks create-access-entry \
  --cluster-name prod \
  --principal-arn arn:aws:iam::123:role/PlatformEngineer \
  --type STANDARD \
  --kubernetes-groups platform-admins

aws eks associate-access-policy \
  --cluster-name prod \
  --principal-arn arn:aws:iam::123:role/PlatformEngineer \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy \
  --access-scope type=cluster`
    **aws-auth ConfigMap** (legacy) is a YAML in `kube-system`. Edit it to add/remove IAM mappings. Hazards: (1) syntax errors lock everyone out. (2) Concurrent edits race. (3) GitOps-managed aws-auth conflicts with manual emergency edits. **Migrate to access entries.**
    EKS supports a precedence: access entries take precedence over aws-auth when both exist for the same principal. New clusters: access-entries-only. Old clusters: migrate.

## 3. OIDC + trust policy + ServiceAccount

**IRSA (IAM Roles for Service Accounts)** lets a Pod assume an IAM role to call AWS services (S3, SQS, KMS, etc.). The flow:
    
      - EKS publishes an OIDC discovery endpoint per cluster.

      - You create an IAM role with a *trust policy* allowing the cluster's OIDC provider to assume it for a specific SA.

      - Annotate the SA: `eks.amazonaws.com/role-arn: arn:aws:iam::...`.

      - The Pod's projected JWT (audience `sts.amazonaws.com`) is exchanged via STS for AWS creds.

      - AWS SDKs in the Pod auto-pick up the creds via `~/.aws/credentials`-equivalent env vars.

    
    It works, but: (1) trust policies are wordy + error-prone. (2) Per-cluster OIDC providers proliferate. (3) Cross-cluster reuse is awkward. (4) Cross-account flows require additional STS hops.

## 4. Pod Identity Agent + association API

**EKS Pod Identity** (released GA 2023) is the modern, simpler successor to IRSA. The flow:
    
      - Install the **Pod Identity Agent** as a managed add-on (one-time per cluster; AWS upgrades).

      - Create an IAM role with a trust policy allowing `pods.eks.amazonaws.com` as principal.

      - Create a Pod Identity association: `aws eks create-pod-identity-association --cluster-name X --namespace ns --service-account sa --role-arn ...`.

      - Pods running as that SA get AWS creds via the agent. SDKs pick up automatically.

    
    Why it's better: no per-cluster OIDC provider; trust policy is identical across clusters; cross-account is one association call; the agent handles the heavy lifting. **For new clusters in 2026: Pod Identity. For existing IRSA: migrate at your pace.**
    **IAM Identity Center (SSO)**: federate human identities to AWS via SAML/OIDC; assume IAM roles per session; access entries grant K8s permissions to those roles. The full chain: corp SSO → IAM role → access entry → K8s group → ClusterRoleBinding.
    [ deep dive — skip if new ]For ECR pulls + Secrets Manager + KMS access, the simplest pattern: a single role with all required AWS permissions, associated to a SA, used by every Pod that needs cross-AWS-service access. Per-namespace roles for least privilege.

## Before / After

**Before.** Single shared `aws-auth` ConfigMap edited via `kubectl edit cm`. Three engineers tried to edit at once last quarter; YAML conflicts; cluster locked everyone out for 45 minutes. IRSA per-cluster OIDC providers + trust-policy edits per role; cross-account = manual STS hops.

**After.** Access entries managed via Terraform; per-IAM-principal mappings in git, applied via API not ConfigMap edit. Pod Identity Agent installed; one association per (SA, role); cross-account = one association call. Audit log shows every change.

EKS identity has had a generational upgrade in 2023-24: access entries replaced aws-auth, Pod Identity replaced IRSA. New clusters: use the modern path; legacy: migrate.

## Analogy — the K-Skyline floor

The Security Desk in K-Skyline has two checkpoints. The **building entrance** (AWS IAM) checks who can even enter the tower — admins, vendors, residents. The **elevator panel** (K8s RBAC) controls which floors each entrant can reach. Between them: the **guest registry** (access entries) maps building entries to elevator codes. For visiting your bank vault on another floor (AWS service from a Pod): the **concierge note** (Pod Identity) tells the elevator that the bearer's elevator code includes vault access. The legacy **blue-key system** (IRSA) used a per-floor key card the visitor had to pre-arrange.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Building entrance check | AWS IAM (eks:* permissions) |
| Elevator panel access | K8s RBAC (Role/ClusterRole) |
| Guest registry mapping entry → elevator code | Access entries (modern) |
| Hand-edited paper guestbook | aws-auth ConfigMap (legacy, fragile) |
| Concierge note for vault access | EKS Pod Identity (Pod Identity Agent + association) |
| Blue-key system per floor | IRSA (OIDC provider + trust policy) |
| Federated visitor pass from sister hotels | IAM Identity Center (SSO) → IAM role → access entry → K8s group |

⚠️ *Analogy stops here:* The analogy stops here: real auth is cryptographic — JWT exchange via STS, signed kubeconfig tokens, OIDC discovery endpoints. The desk metaphor undersells the trust chain.

## ELI5 / ELI10

**ELI5.** Two doors. The first door checks if you're allowed in the building (IAM). The second door checks which rooms you can enter (K8s RBAC). The hotel keeps a list of who matches what.

**ELI10.** Two identity layers in EKS: AWS IAM (who can call EKS APIs + retrieve kubeconfig) and K8s RBAC (in-cluster permissions). Bridge via access entries (modern, API-managed) or aws-auth ConfigMap (legacy, fragile). For Pod → AWS service: EKS Pod Identity (modern, agent-based, association API) or IRSA (legacy, OIDC + trust policy). New clusters use access entries + Pod Identity; old clusters migrate.

## Real-world scenarios

- **A SaaS managing access via Terraform + access entries.** Every IAM role mapped to a K8s group via Terraform-managed access entries. New engineer = PR adds them to the IAM role + the access entry; merge auto-syncs. No more manual aws-auth edits.
- **A bank using SSO + access entries + per-namespace Pod Identity.** Corp Okta → IAM Identity Center → IAM role per team → access entry per role → K8s group → namespace-scoped Role. Pods get AWS access via Pod Identity associations per (namespace, SA). Zero shared kubeconfigs; full audit trail.
- **A team migrating IRSA → Pod Identity.** New SAs use Pod Identity. Old IRSA SAs left in place; tracked for migration. Per-SA migration: install Pod Identity Agent; create association; remove IRSA annotation; restart Pod. Quarter-long phased migration; no big bang.
- **A team that locked everyone out.** Junior engineer edited `aws-auth` ConfigMap; YAML indent error parsed as removing all admins. EKS Console fix: AWS recommends pre-existing access entries for emergency admin recovery (the access-entry API can't be locked out by ConfigMap edits). Lesson: migrate to access entries before you need them.

## Common misconceptions

- **Myth:** "AWS IAM admin = K8s admin."
  **Truth:** IAM admin lets you retrieve kubeconfig + manage the cluster object; doesn't imply K8s RBAC permissions. The two are separate. Bridge via access entry / aws-auth.
- **Myth:** "IRSA is fine; no need to migrate to Pod Identity."
  **Truth:** IRSA works but: per-cluster OIDC, per-role trust-policy edits, awkward cross-cluster + cross-account. Pod Identity is simpler + more uniform. Migrate at your pace; new SAs default to Pod Identity.
- **Myth:** "aws-auth ConfigMap is the same as access entries."
  **Truth:** ConfigMap = legacy, edited in-cluster, prone to lockout. Access entries = API-managed, AWS-validated, can't lock you out via ConfigMap mistake. New clusters: access entries only.

## Recap

IAM (cluster API) + K8s RBAC (in-cluster). Bridge via access entries (modern) or aws-auth (legacy). Pod-to-AWS-service via Pod Identity (modern) or IRSA (legacy). SSO via IAM Identity Center.

**Next — E5: EKS Storage.** EBS / EFS / FSx CSI drivers, S3 Mountpoint, snapshots, KMS encryption, zone-aware provisioning.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
