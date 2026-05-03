# K-EKS E9 — E9 · EKS Upgrades and Operations

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E9 · Upgrades and Operations
> Companion preview: `/preview-kubernetes-eks-lesson-09.html`.

---

**🎯 If you remember nothing else:** EKS upgrades: **14 months standard support + 12 months extended support** per minor. Order: **(1) backup + scan** (etcd snapshot equivalent doesn't exist; AWS handles control plane state — but Velero your workloads + scan with Pluto for deprecated APIs); **(2) control plane** (`aws eks update-cluster-version`; ~30-60 min, AWS handles); **(3) Managed Node Groups** (rolling drain via AWS); **(4) Self-managed nodes**; **(5) Fargate Pod refresh** (recreate Pods); **(6) Add-ons** (CNI, CoreDNS, kube-proxy, EBS / EFS CSI); **(7) Verify**. Blue-green cluster for high-stakes upgrades.

## 1. EKS upgrade differences from vanilla K8s

Vanilla K8s upgrades (K-VAN V8): you upgrade etcd snapshot → control plane → kubelets → workers → add-ons. Pure manual orchestration via kubeadm.
    EKS:
    
      - **Control-plane upgrade**: one API call (`aws eks update-cluster-version`); AWS rolls + manages. Takes 30-60 min; cluster API stays available throughout.

      - **Managed Node Group upgrade**: one API call per NG (`aws eks update-nodegroup-version`); AWS does rolling drain via the same lifecycle controller.

      - **Fargate**: no node version per se; new Pods get new platform version automatically. Existing Pods stay until naturally restarted; force-refresh by triggering rolling deploy.

      - **Add-ons** (VPC CNI, CoreDNS, kube-proxy, EBS / EFS CSI): managed-add-on versions tied to K8s versions. AWS Console / CLI to upgrade.

      - **Self-managed nodes**: same as K-VAN V8. You orchestrate the drain + rolling update.

      - **EKS Auto Mode**: AWS handles add-ons + nodes lifecycle. You don't touch them.

## 2. 14 months standard + 12 months extended

Per K8s minor: AWS provides **14 months standard support** at the regular $0.10/hour cluster fee. After that: **12 months extended support** at +$0.60/hour per cluster (~$5K/year extra). After extended ends: AWS forcibly upgrades your cluster (yes, really) — you don't want to be there.
    K8s minors release every ~4 months upstream; AWS lags by 1-2 months. So the standard support window covers ~3 minor versions out — plenty of time if you upgrade quarterly.
    **Track the lifecycle**: `aws eks describe-cluster-versions --include-all` lists every version + dates. Set a calendar alert 60-90 days before standard support ends.

## 3. Step-by-step

- **Pre-flight**: scan manifests for deprecated APIs (`kubectl convert`, Pluto, kube-no-trouble). Check operator + Helm chart compatibility. Validate against staging cluster on the new version.

      - **Backup**: Velero backs up workloads + PVCs. AWS handles etcd internally; you don't snapshot it directly.

      - **Control plane**: `aws eks update-cluster-version --name prod --kubernetes-version 1.36`. AWS rolls in-place; ~30-60 min; API available.

      - **Managed Node Groups**: `aws eks update-nodegroup-version --cluster-name prod --nodegroup-name X`. AWS does rolling drain respecting PDBs. Repeat per NG.

      - **Self-managed nodes**: standard kubeadm-style drain + replace.

      - **Fargate**: trigger rolling deployment to recreate Pods on new platform version.

      - **Add-ons**: `aws eks update-addon --cluster-name prod --addon-name vpc-cni` per add-on. Order: kube-proxy → CoreDNS → VPC CNI → CSI drivers. (Consult docs for each version's required add-on combination.)

      - **Verify**: smoke tests, dashboards, Pod health.

## 4. When in-place isn't safe

For high-stakes upgrades (multi-version jumps, regulated workloads, distrust of in-place):
    
      - **Build new cluster** at the target version (Terraform / Blueprints).

      - **Migrate workloads via GitOps**: Argo CD points new cluster at the same git path. Workloads come up.

      - **Migrate stateful**: snapshot EBS / EFS volumes + restore in new cluster. Or: Velero backup-restore. Or: replicate data continuously (e.g., Postgres replication) + flip primary.

      - **DNS cut-over**: Route 53 weighted records gradually shift traffic from old to new.

      - **Decommission old cluster** after validation.

    
    Twice the infrastructure cost during cutover. Safest upgrade pattern. Used for the most-critical clusters.
    [ deep dive — skip if new ]For air-gapped or regulated environments: extended support gives you breathing room when an upgrade requires more validation than the standard window permits. Don't rely on extended support — but it's there if you need it.

## Before / After

**Before.** Cluster on K8s 1.30; standard support ended 6 months ago; paying $0.60/hr extended. Operators stopped supporting that version. Risky upgrade, no rehearsal cluster. Pluto scan never run.

**After.** Quarterly upgrade calendar. Pluto scans in CI on every PR. Staging cluster mirrors prod; upgrades rehearsed there first. `aws eks update-cluster-version` + add-on updates take an afternoon. Standard support always.

EKS upgrades are easier than vanilla — AWS handles the control plane. The discipline (quarterly cadence, rehearsal, Pluto in CI) is the same.

## Analogy — the K-Skyline floor

The Maintenance Wing handles all the building's renovation work. The contractor (AWS) handles the major renovations on AWS-managed parts (control plane, Managed NG lifecycle, add-on bumps); the tenant (you) handles the workload-side preparation (deprecated-API scans, Velero backups, smoke tests). The renovation calendar (version-support timeline) hangs on the wall: 14-month "warranty period" + 12-month extended-support window. Beyond that, the contractor forcibly renovates.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Renovation calendar | 14 months standard + 12 months extended support |
| Contractor handles structural work | AWS handles control-plane + Managed NG lifecycle |
| Tenant prepares the unit | Pluto scan, Velero backup, Helm + operator compat checks |
| One renovation per cycle | One minor at a time |
| Build a parallel unit + move tenants | Blue-green cluster migration |
| Extended-support fee | $0.60/h premium per cluster |
| Forcible renovation at end of extended | AWS auto-upgrades after extended support ends |

⚠️ *Analogy stops here:* The analogy stops here: AWS's upgrade is mostly transparent because the control plane is in their account; the workloads still execute the K8s upgrade machinery (kubelet versions, API deprecations, etc.).

## ELI5 / ELI10

**ELI5.** Every few months the building gets a renovation. AWS does the heavy lifting; you just clean your room first. If you don't renovate for too long, the building manager forcibly renovates anyway — you want to be ahead of that.

**ELI10.** EKS upgrades: 14 months standard + 12 extended per minor. Order: pre-flight scan (Pluto / kubectl convert) → control plane (AWS handles) → Managed NG (AWS rolling drain) → self-managed → Fargate refresh → add-ons (CNI / CoreDNS / kube-proxy / EBS CSI) → verify. Only +1 minor per update; multi-version jumps via blue-green cluster. Quarterly cadence is the discipline.

## Real-world scenarios

- **A SaaS doing quarterly EKS upgrades.** Calendar: week 1 = staging upgrade. Week 2 = production control plane. Week 3 = nodes + add-ons. Repeat. Pluto in CI catches deprecated APIs. ~4 hours of SRE time per cluster per quarter.
- **A bank using blue-green cluster migration.** Build new EKS cluster at target version. Argo CD migrates workloads. RDS Multi-AZ + Aurora handles state replication. Route 53 weighted records do gradual traffic shift. Old cluster decommissioned after 30 days. Twice the cost during cutover; zero in-place risk.
- **A team that hit extended support and learned.** Cluster on 1.28; standard ended; bill jumped $5K/year. Couldn't upgrade quickly due to a CRD compatibility issue. Bought extended support; planned blue-green migration; completed in 2 sprints. Lesson: Pluto in CI from now on.
- **An EKS Auto Mode user with simplified upgrades.** Auto Mode handles add-ons + node lifecycle. K8s minor upgrade = one API call to update control plane; Auto Mode handles the rest. No add-on update orchestration. Total upgrade time: 1 hour per cluster.

## Common misconceptions

- **Myth:** "AWS upgrades my add-ons automatically."
  **Truth:** Only with EKS Auto Mode (E2). For self-managed add-ons or add-ons installed via Helm: you upgrade. For managed add-ons (e.g., VPC CNI managed): you trigger the upgrade via API, AWS performs.
- **Myth:** "Extended support is fine; I'll stay there."
  **Truth:** Extended support is a runway, not a destination. AWS will eventually fully deprecate the version even on extended support. And you're paying $5K/year per cluster premium.
- **Myth:** "EKS doesn't need pre-upgrade deprecated-API scans."
  **Truth:** Same K8s underneath; same API removals. Pluto / kubectl convert in CI on every PR; alert on deprecated API references.

## Recap

EKS = 14 months standard + 12 extended per minor. AWS handles control plane + Managed NG + add-on upgrades; you handle pre-flight scans + Velero + verification. +1 minor at a time. Blue-green for high stakes.

**Next — E10: EKS Troubleshooting (AWS-specific).** IAM/RBAC failures, IP exhaustion, ALB / NLB stuck, Karpenter issues, Auto Mode disruption, IRSA / Pod Identity failures.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
