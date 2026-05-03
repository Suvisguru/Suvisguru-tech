# K-EKS E11 — E11 · Capstone — Multi-AZ EKS Auto Mode Tower with Everything

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E11 · Capstone Tower
> Companion preview: `/preview-kubernetes-eks-lesson-11.html`.

---

**🎯 If you remember nothing else:** **Capstone deliverables**: (1) Working multi-AZ EKS Auto Mode cluster (3 AZs). (2) EKS Blueprints / Terraform repo reproducing the cluster from scratch. (3) Pod Identity + access entries (no IRSA / aws-auth). (4) KMS CMK encryption everywhere. (5) Gateway API + VPC Lattice for cross-VPC. (6) AMP + AMG + ADOT + control-plane logs. (7) Argo CD App-of-Apps for workloads + add-ons. (8) Eight runbooks for the eight EKS failure patterns. (9) Documented blue-green upgrade rehearsal. (10) DR plan covering AZ failure + region failure. **K-EKS-complete** when a peer reproduces from your artifacts + recovers a chaos-injected disaster.

## 1. What "capstone" means here

K-EKS is 10 modules of how. The capstone is one module of *do*: a single end-to-end project exercising every prior module in sequence. You come out with a working production-grade EKS cluster + IaC + runbooks + the muscle memory to do it again.
    The reference stack is opinionated to keep the project tractable: **EKS Auto Mode** (Karpenter built-in + add-ons bundled), **AWS LB Controller** (built into Auto Mode), **Pod Identity** (modern auth), **KMS CMK** everywhere, **Gateway API + VPC Lattice**, **AMP + AMG + ADOT**, **Argo CD**, **EKS Blueprints (Terraform)**. You can sub equivalents (Calico for Cilium, Datadog for AMG) but the modules apply.

## 2. E1-E3 in sequence

**A.1 Architecture document** (E1). One page: 3 AZs in `us-east-1`, EKS Auto Mode, Pod CIDR `192.168.224.0/20` (non-overlapping with corp VPN), Service CIDR `10.96.0.0/12`, private cluster endpoint, KMS CMK, Pod Identity for auth. Commit to git as `docs/architecture.md`.
    **A.2 EKS Blueprints (Terraform)**. Module deploys: VPC (3 public + 3 private subnets, prefix-delegation-friendly), EKS cluster with Auto Mode enabled, KMS CMK for Secrets encryption, IAM roles (cluster role, Auto Mode node role), control-plane logs (all 5 types), Pod Identity Agent add-on, Container Insights add-on. `terraform apply`; ~20-30 min.
    **A.3 Validate**: `kubectl get nodes` shows nodes from Auto Mode (Bottlerocket); CoreDNS Pods Running; Container Insights dashboard populated.

## 3. E4-E5-E8 in sequence

**B.1 Pod Identity** (E4). Define IAM roles per workload class (e.g., `app-prod-pods`, `logging-pods`, `backup-pods`) — each scoped least-privilege. Pod Identity associations per (namespace, SA) → role. No IRSA. No aws-auth.
    **B.2 Access entries** (E4). Map IAM Identity Center permission sets to K8s groups via access entries. Per-team groups bound to namespace-scoped Roles. Cluster-creator IAM role documented as the break-glass admin.
    **B.3 Storage** (E5). EBS CSI add-on (Auto Mode bundles). Custom StorageClass `gp3-encrypted` with KMS CMK + WaitForFirstConsumer. snapshot-controller (Auto Mode bundles). Optional: EFS CSI for any RWX workloads.
    **B.4 Observability** (E8). AMP workspace + IAM role for ADOT. AMG workspace via Identity Center SSO. ADOT collector DaemonSet (deployed via Helm) scrapes Pod metrics + ships to AMP, traces to X-Ray, logs to CloudWatch. Container Insights enhanced (already from A.2). Split Cost Allocation enabled.

## 4. E6-E7-E9-E10 + capstone deliverables

**C.1 Security** (E7). GuardDuty EKS Protection + Runtime Monitoring on. Inspector enhanced scanning on every ECR repo. Cosign signing in CI; Kyverno verifyImages in admission. PSA Restricted on every prod namespace. AdminNetworkPolicy default-deny + selective allows.
    **C.2 GitOps** (Argo CD). Bootstrap script: helm install Argo CD; root App-of-Apps points at `k8s-platform/apps/`. Argo CD reconciles: cert-manager, ExternalDNS, Kyverno, Falco (or rely on GuardDuty Runtime Monitoring), Velero, AMP+AMG configurations, application Deployments.
    **C.3 Backup + DR**. Velero schedule (nightly); EBS snapshot via CSI snapshot-controller (every 30 min for stateful workloads); cross-region replication of critical data (S3 versioning + cross-region replication for backups). DR plan: **AZ failure** = topology spread + multi-AZ EBS = automatic recovery; **region failure** = secondary cluster in another region (or blue-green migration to one).
    **C.4 Upgrade rehearsal** (E9). Build a staging clone via EKS Blueprints. Walk a minor-version upgrade (control plane → Auto Mode handles add-ons + nodes). Document gotchas. Output: `docs/runbooks/eks-upgrade-vX-to-vY.md`.
    **C.5 Eight runbooks** (E10). One file per failure pattern. Each tested on the staging cluster.
    **C.6 Final review**: a colleague reproduces the cluster from the EKS Blueprints repo + recovers one chaos-injected disaster using your runbook. **K-EKS-complete**.
    [ deep dive — skip if new ]If you have time + budget: build a multi-region active-active EKS pair. Aurora Global Database for stateful tier; Route 53 weighted health-checked records; Argo CD per cluster reconciling the same git path. Multi-region adds ~3 weeks beyond the standard capstone.

## Before / After

**Before.** You've finished K-COM and read all 10 K-EKS modules. You haven't built end-to-end. The gap between knowing and doing only shows up when something breaks in production.

**After.** You've built the reference EKS Auto Mode cluster. You've broken it on purpose and recovered. Your EKS Blueprints repo + runbooks let a colleague reproduce in a day. You can defend any choice in an interview. **K-EKS-complete**.

The capstone exists so the gap between knowing and doing is closed deliberately, not by surprise in production.

## Analogy — the K-Skyline floor

Tower Complete is the K-Skyline's eleventh and final floor — the one that takes in the view of every other floor below. The Drafting Hut's blueprint, the Concierge service running quietly, the Communication Tower's LBs humming, the Security Desk's identity flow, the Storage Vault's encrypted volumes, the Power Floor's right-sized compute, the Vault Mezzanine's detection, the Observation Deck's dashboards, the Maintenance Wing's upgrade calendar, the Emergency Plaza's drilled runbooks. You stand on the roof with the deed in one hand, the keys in the other, the runbook library in your pocket. **K-EKS-complete**.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Tower deed | Architecture document in git |
| Plaque on the lobby | EKS Blueprints / Terraform module |
| Concierge's daily report | Auto Mode + Container Insights dashboards |
| Master keychain in the vault | KMS CMK encrypting Secrets / EBS / EFS / ECR |
| Inter-building shuttle service | VPC Lattice + Gateway API |
| Observation Deck instruments | AMP + AMG + ADOT + X-Ray + control-plane logs |
| Resident registry | Argo CD App-of-Apps in git |
| Insurance policy + drill log | Velero + DR plan + tested runbooks |
| Renovation calendar | Quarterly EKS upgrade cadence |
| Emergency-drill scoreboard | Eight runbooks + chaos drills |

⚠️ *Analogy stops here:* The analogy stops here: the tower is one snapshot. Real EKS clusters evolve continuously — new K8s minors, new add-ons, new workloads. K-EKS-complete means "can build + operate + defend" — not "done forever."

## ELI5 / ELI10

**ELI5.** You've learned how to live in the AWS tower. Now build one yourself, lock it down, set up the alarms, write down what to do in a fire — and prove someone else could do it from your notes.

**ELI10.** Capstone: build a multi-AZ EKS Auto Mode cluster end-to-end. EKS Blueprints (Terraform) for the cluster + VPC + KMS. Pod Identity + access entries for auth. KMS CMK for Secrets / EBS / EFS / ECR. Gateway API + VPC Lattice. AMP + AMG + ADOT. Argo CD GitOps for workloads + add-ons. GuardDuty + Inspector + Cosign. Velero + DR plan. Eight runbooks for E10's failure patterns. Blue-green upgrade rehearsal. Peer review + chaos-drill recovery = K-EKS-complete.

## Real-world scenarios

- **A team finishing K-EKS as their pre-prod milestone.** 4 weeks of dedicated time. EKS Blueprints + Argo CD + observability + security stack + 8 runbooks. Final demo: chaos day on the lab cluster, recovering 3 of E10's scenarios in front of the team. Clear "production-ready" signal.
- **A bank using K-EKS graduates as the AWS Platform team.** Anyone running prod EKS clusters has finished K-EKS. New hires onboarded by working through K-EKS with a buddy. Hand-off quality is hire-time + ongoing.
- **A startup choosing K-EKS over an AWS cert.** K-EKS validates building. Cert validates trivia. Engineering manager: SRE candidates pair on EKS Blueprints + Pod Identity migration + Karpenter consolidation. Artifact (git repo + runbooks) is the portfolio.
- **An open-source contributor giving back.** Used K-EKS to build their first managed cluster. Wrote a blog comparing EKS Auto Mode vs DIY Karpenter; PR'd a typo fix in the K-EKS module; published their EKS Blueprints fork. Cycle complete.

## Common misconceptions

- **Myth:** "The capstone is optional / nice-to-have."
  **Truth:** K-EKS-complete means built end-to-end. Reading the modules without doing the capstone is K-EKS-read. Different skill level.
- **Myth:** "You need a real production cluster to do K-EKS."
  **Truth:** An AWS account + a small lab cluster are enough. Cost: ~$50-200 for the capstone duration. AWS's Free Tier covers some pieces; for full Auto Mode + AMP + observability + a few hours per day for 4 weeks, plan ~$200-400 total.
- **Myth:** "You can skip the runbooks if everything works."
  **Truth:** Runbooks are the deliverable. Working cluster without runbooks = can't hand off + can't recover under pressure. Write them as you go.

## Recap

K-EKS capstone = build the reference EKS stack end-to-end + harden + back up + upgrade + DR-drill + 8 runbooks. Working cluster + EKS Blueprints repo + runbooks + defended decisions + reproduced by a peer = K-EKS-complete.

**Done.** You've walked the K-Skyline tower from lobby to roof. K-EKS ends here; what comes next is operating real EKS clusters with the muscle memory you built.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
