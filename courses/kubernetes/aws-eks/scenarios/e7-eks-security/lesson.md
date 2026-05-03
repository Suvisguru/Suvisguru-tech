# K-EKS E7 — E7 · EKS Security (KMS, GuardDuty, ECR signing, Bottlerocket, audit)

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E7 · EKS Security
> Companion preview: `/preview-kubernetes-eks-lesson-07.html`.

---

**🎯 If you remember nothing else:** EKS security baseline: **KMS envelope encryption** for K8s Secrets + EBS + EFS (CMK, not default key); **GuardDuty EKS Protection** (audit) + **Runtime Monitoring** (eBPF threat detection); **Inspector + ECR enhanced scanning** (Snyk-powered CVE); **Cosign + AWS Signer** for image signing + verifyImages admission; **ECR replication + pull-through cache**; **Bottlerocket** immutable nodes; **PSA Restricted**; **private cluster endpoint**; **CloudTrail audit**; **IAM Access Analyzer**; **FIPS** for regulated.

## 1. Layer AWS on top of K8s security

K8s security baselines (PSA, NetworkPolicy, RBAC, audit log, encryption-at-rest) — covered in K-COM L27-L31 + K-VAN V9. EKS adds AWS-native primitives that complement them. The full posture stack:
    
      - **K8s baselines**: RBAC + access entries, PSA, NetworkPolicy, audit, encryption-at-rest.

      - **AWS layer**: KMS for encryption, GuardDuty for threat detection, Inspector for image scanning, AWS Signer / ECR signing, Bottlerocket nodes, CloudTrail.

      - **Identity**: Pod Identity / IRSA (E4) for least-privilege Pod-to-AWS.

      - **Network**: SG-for-pods (E3), private cluster endpoint, VPC endpoints.

## 2. Secrets, EBS, EFS, ECR

- **Secrets at rest in etcd**: enable EKS secrets encryption with a KMS Customer Managed Key (CMK) at cluster create. Pre-existing clusters: enable via `aws eks update-cluster-config`; existing Secrets need re-write to be encrypted (`kubectl get secrets -A -o json | kubectl replace -f -`).

      - **EBS volumes**: every StorageClass should have `encrypted: true + kmsKeyId` (E5). Default to a CMK; the AWS-managed default key has fewer controls.

      - **EFS / FSx**: encryption-at-rest with KMS CMK. Encryption-in-transit via TLS to the EFS mount.

      - **ECR images**: ECR encrypts at rest by default (KMS); use a CMK for compliance.

      - **CloudWatch Logs / S3 buckets**: KMS-encrypted; same CMK or per-purpose CMKs.

    
    **Key management strategy**: one CMK per environment (dev / staging / prod) per region. Rotate annually (KMS supports automatic). Audit access via CloudTrail.

## 3. GuardDuty EKS + Inspector + signing

**Amazon GuardDuty EKS Protection** (released 2022): analyses Kubernetes audit logs for suspicious patterns (privilege escalation, anonymous API access, etc.). *Enable on every cluster — free first 30 days, modest cost after*.
    **GuardDuty EKS Runtime Monitoring** (2023): eBPF-based agent (DaemonSet, AWS-managed) detects runtime threats — process anomalies, network anomalies, file-system anomalies — without requiring you to operate Falco.
    **Amazon Inspector + ECR Enhanced Scanning** (Snyk-powered): scan ECR images for CVEs continuously. Findings in Security Hub. ECR Enhanced Scanning is opt-in per-repo.
    **Image signing**: **Cosign** (Sigstore, OSS) is the de-facto standard. **AWS Signer** (managed signing service) integrates with ECR + Cosign. Pipeline: build → sign with Cosign keyless or AWS Signer → push to ECR → admission controller (Kyverno verifyImages) verifies before admission.
    **ECR features**: *replication* (cross-region or cross-account), *pull-through cache* (proxy public registries through your private ECR), *repository policies* (IAM controlling pulls/pushes per repo).

## 4. Bottlerocket, PSA, private endpoint, CloudTrail, FIPS

- **Bottlerocket**: AWS's immutable, container-optimised OS. Read-only root FS, dm-verity, automatic updates via update operator. Smaller attack surface vs Amazon Linux 2; default for EKS Auto Mode.

      - **Pod Security Standards**: label every namespace `pod-security.kubernetes.io/enforce: restricted`. Workloads requiring privileged escape get exception namespaces (CSI drivers, monitoring agents).

      - **SG-for-pods** (E3): per-Pod SecurityGroups for fine-grained AWS-service ACLs. The right path to "only Pod X can reach RDS Y."

      - **Private cluster endpoint**: `endpointPrivateAccess: true, endpointPublicAccess: false`. `kubectl` reachable only from within the VPC (or via VPN / Direct Connect / PrivateLink).

      - **CloudTrail audit**: every EKS API call logged. Plus K8s control-plane logs (E8) cover in-cluster auth + API requests.

      - **IAM Access Analyzer**: detects unintended cross-account access in IAM policies + S3 / KMS resource policies.

      - **FIPS**: required for regulated environments (FedRAMP, FedRAMP-Mod). EKS supports FIPS endpoints; node OS choice (Bottlerocket FIPS, RHEL FIPS) for FIPS-validated crypto.

    
    [ deep dive — skip if new ]For PCI / HIPAA-regulated workloads: above + dedicated tenancy, dedicated KMS keys per workload class, per-namespace audit log destinations, segregated IAM admin. Add ~3-6 months of compliance implementation per regulation.

## Before / After

**Before.** Public cluster endpoint, IAM-only protection. Secrets unencrypted in etcd. EBS encrypted with default key. No image scanning. No runtime threat detection. CloudTrail enabled but nobody reads it. "Compliance evidence" is a wiki page.

**After.** Private endpoint, only-via-VPN access. KMS CMK encrypts secrets / EBS / EFS / ECR. GuardDuty EKS Runtime Monitoring on. Inspector continuous CVE scan. Kyverno verifyImages enforces Cosign signatures. CloudTrail forwards to SIEM. PSA Restricted everywhere except documented exceptions.

EKS security is layering AWS-native services on top of K8s baselines. Each layer adds defense without requiring you to operate the security tooling.

## Analogy — the K-Skyline floor

The Vault Mezzanine sits one floor above the lobby — visible from below, but glass-walled and key-locked. Inside: the master keychain (KMS), the radar dish scanning for intruders (GuardDuty), the conveyor-belt scanner reading every package on entry (Inspector + ECR Enhanced Scanning), the notary stamping authentic packages (AWS Signer + Cosign), the immutable-floor-tile certification (Bottlerocket), the elevator restriction (private cluster endpoint), the building-wide audit ledger (CloudTrail). The vault staff are the AWS security services; you tell them what to watch + they handle the rest.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Master keychain | KMS Customer Managed Keys |
| Radar scanning patrons | GuardDuty EKS Protection (audit) |
| Doorman watching for actual misbehaviour | GuardDuty EKS Runtime Monitoring (eBPF) |
| Conveyor scanner at entry | Amazon Inspector + ECR Enhanced Scanning |
| Notary stamping authentic packages | AWS Signer + Cosign + Kyverno verifyImages |
| Immutable-floor certification | Bottlerocket OS |
| Elevator restricted to keycard holders | Private cluster endpoint |
| Building audit ledger | CloudTrail (EKS API + AWS resource changes) |
| Cross-account loan oversight | IAM Access Analyzer |

⚠️ *Analogy stops here:* The analogy stops here: real AWS security services run as separate AWS-side compute (GuardDuty + Inspector are out-of-cluster; Runtime Monitoring is an in-cluster DaemonSet). The vault metaphor undersells the IAM + audit plumbing.

## ELI5 / ELI10

**ELI5.** Locks on every door (KMS), cameras watching the building (GuardDuty), inspector at the front desk checking IDs (Inspector + ECR), and a logbook of every visitor (CloudTrail). All run by the building staff (AWS).

**ELI10.** EKS security baseline: KMS CMK for Secrets + EBS + EFS + ECR. GuardDuty EKS Protection + Runtime Monitoring (eBPF). Inspector + ECR Enhanced Scanning for CVEs. Cosign + AWS Signer + Kyverno verifyImages. Bottlerocket immutable nodes. PSA Restricted + SG-for-pods. Private cluster endpoint. CloudTrail audit. IAM Access Analyzer for unintended cross-account. FIPS for regulated workloads.

## Real-world scenarios

- **A SaaS with full GuardDuty + Inspector + ECR signing.** GuardDuty EKS Audit + Runtime Monitoring on. Findings forwarded to PagerDuty for P0 (e.g., privilege escalation). ECR Enhanced Scanning for every push; severity Critical = block deploy via Kyverno + verifyImages. Pipeline signs every image with Cosign keyless via GitHub OIDC; cluster admission verifies. Compliance: SOC2 + ISO27001 evidence largely automated.
- **A bank with private endpoint + FIPS Bottlerocket + dedicated KMS per workload.** EKS endpoint private only. Direct Connect from corporate. Bottlerocket FIPS variant on all nodes. KMS CMK per workload class (payments / accounts / analytics) with separate IAM. CloudTrail forwarded to SIEM. Annual external audit; minor findings only.
- **A team that learned about default KMS.** Enabled secrets encryption at cluster create with the AWS-managed default key. Compliance auditor flagged: "can't prove you control the key." Migration: created CMK; updated EKS encryption config; rewrote all Secrets to re-encrypt with new key. Lesson: always CMK from the start.
- **A startup using ECR pull-through cache.** Heavy use of public images (postgres, redis, busybox). Set up ECR pull-through cache for Docker Hub + Quay. Now: image pulls go to private ECR, which fetches from public on cache miss. Resilient to Docker Hub rate limits + outages; supply-chain visibility for every image.

## Common misconceptions

- **Myth:** "AWS-managed KMS key is fine for production secrets."
  **Truth:** Functionally encrypted, but you don't control rotation, can't restrict access cross-account, can't prove key control to an auditor. Always CMK for production. Cost is negligible ($1/month per key).
- **Myth:** "GuardDuty Runtime Monitoring is just Falco."
  **Truth:** Same data plane (eBPF), but AWS-managed: no DaemonSet to operate, integrated with Security Hub / EventBridge, AWS handles updates. Falco is more flexible (custom rules); GuardDuty is operationally simpler.
- **Myth:** "Private endpoint means I can't kubectl from anywhere."
  **Truth:** Private endpoint = reachable from within the VPC. Engineers reach it via: VPN, AWS Client VPN, Direct Connect, jump host in the VPC, or AWS SSM Session Manager + port-forwarding. Modern shops use SSM tunneling for kubectl.

## Recap

EKS security = AWS layer (KMS + GuardDuty + Inspector + Signer) on top of K8s baselines (PSA + RBAC + NetworkPolicy + audit). Pod Identity (E4) for least-privilege Pod-to-AWS. Bottlerocket nodes. Private endpoint. CloudTrail audit.

**Next — E8: EKS Observability.** CloudWatch Container Insights, AMP, AMG, ADOT, X-Ray, control-plane logs, AWS Split Cost Allocation.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
