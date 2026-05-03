# K-VAN V8 — V8 · Upgrades and Patching (kubeadm, version skew, rollback)

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V8 · Upgrades and Patching
> Companion preview: `/preview-kubernetes-vanilla-lesson-08.html`.

---

**🎯 If you remember nothing else:** K8s release cadence: **minor every ~4 months**, patches monthly, ~14 months support per minor. Version skew: **kubelet ≤ apiserver, max 3 minors behind**; never skip a minor on upgrade. Order: **etcd snapshot → cp-1 (kubeadm upgrade apply) → cp-2/3 → kubelet on CP → workers (drain → upgrade → uncordon) → add-ons → CNI/CSI**. Pre-upgrade: scan for deprecated APIs (kubectl convert, Pluto). Rollback: limited — backup-restore is the safety net.

## 1. Why upgrades scare people

Three things make K8s upgrades different from other software:
    
      - **Frequent minors.** Three or four minor releases a year. Skipping is unsafe (can't go 1.32 → 1.36 in one shot — must be 1.32 → 1.33 → 1.34 → 1.35 → 1.36).

      - **Multi-component coordination.** Upgrade apiserver + controller-manager + scheduler + etcd + kubelets + kube-proxy + CNI + CSI + add-ons + CRDs. Each must work together and has its own version skew rules.

      - **Limited rollback.** kubeadm doesn't auto-rollback. The safety net is etcd snapshot + backup → cluster restore. Plan for upgrade-fail by having a tested restore.

## 2. Who can be how far ahead/behind whom

- **kube-apiserver**: highest version. New minor first.

      - **controller-manager / scheduler**: ≤ apiserver. Same minor or one behind during transition.

      - **kubelet**: ≤ apiserver, may be up to 3 minors behind. Practical: don't leave kubelets behind by > 1 minor.

      - **kube-proxy**: same minor as kubelet on its node.

      - **kubectl**: ±1 minor from apiserver.

    
    The skew rules let you upgrade the control plane first, then workers — without a hard cutover. A worker on v1.35 can keep talking to a v1.36 apiserver during the transition.

## 3. One node at a time, control plane first

`# 0. Backup etcd snapshot (V7) — verify it's recent + tested
# 1. Plan
sudo kubeadm upgrade plan v1.36.0

# 2. On cp-1 — apply
sudo apt-get install -y kubeadm=1.36.0-1.1
sudo kubeadm upgrade apply v1.36.0

# 3. On cp-1 — kubelet + kubectl
sudo kubectl drain cp-1 --ignore-daemonsets --delete-emptydir-data
sudo apt-get install -y kubelet=1.36.0-1.1 kubectl=1.36.0-1.1
sudo systemctl daemon-reload && sudo systemctl restart kubelet
sudo kubectl uncordon cp-1

# 4. Repeat steps 2-3 on cp-2, cp-3 (with `kubeadm upgrade node`, not `apply`)
sudo apt-get install -y kubeadm=1.36.0-1.1
sudo kubeadm upgrade node
# ... drain + kubelet + uncordon

# 5. Workers — same drain → kubeadm upgrade node → kubelet → uncordon, one at a time
# 6. Add-ons — Argo CD detects new versions if you've bumped Helm chart values

# 7. CNI / CSI — typically on a different cadence; bump after K8s upgrade settles`
    Surge nodes (extra worker added before upgrade, removed after) make worker upgrades safer for capacity-sensitive clusters.

## 4. Detect breakage early; have a path back

**Pre-upgrade:**
    
      - **Scan for deprecated APIs** in your manifests + git: `pluto detect-files -d <dir>` or `kubectl convert`. Removes are listed in each release's notes.

      - **Check CRD compatibility:** third-party operators often pin to a K8s version range. Check their docs.

      - **Run upgrade on staging first.** Same K8s minor, same add-on versions, same workloads. If it breaks there, fix before prod.

      - **PodDisruptionBudgets** on production workloads to prevent drain from taking too many replicas at once.

      - **Backup-before-upgrade:** fresh etcd snapshot, fresh Velero backup of all namespaces.

    
    **Rollback options** (in increasing pain):
    
      - **Per-component:** downgrade kubelet/kubeadm packages on a node, restart. Limited (apiserver downgrade is more disruptive).

      - **etcd restore:** bring the cluster back to its pre-upgrade snapshot. All workloads come back to that state. Lose any post-upgrade work.

      - **Blue-green clusters:** the safest. Build the new cluster fresh at the new version, migrate workloads via GitOps, decommission the old. Twice the cost during cutover.

    
    For most teams: **etcd restore is the rollback plan**. Make sure you have a tested one.
    [ deep dive — skip if new ]For Talos: upgrades are a single `talosctl upgrade --image talos:v1.x` per node — the OS image is replaced + rebooted. Cluster API: declarative version bump in the Cluster manifest; CAPI rolls nodes. Different operational shape but same skew rules apply.

## Before / After

**Before.** "We'll upgrade later." 18 months pass. Cluster is now 4 minors behind. CVEs accumulate. Operators stop supporting the version. Upgrade requires going through 4 minors with all their breaking changes at once. Migration ends up being a cluster rebuild.

**After.** Quarterly upgrade cadence. Each upgrade rehearsed on staging the prior week. Pluto + kubectl convert in CI on every PR catches deprecated APIs before they ship. etcd snapshot + Velero backup before every upgrade. Rollback playbook drilled. Upgrades feel like routine maintenance.

The cluster that doesn't upgrade routinely is the cluster that has to be rebuilt.

## Analogy — the K-Frontier site

The Renovation site sits next to the main house. Every season, the homesteader rolls in a new floor, replaces a worn beam, swaps the old roof for a better one. The work follows a strict order — you can't replace the roof before the rafters are stable. The contractor knows: **foundation first** (etcd snapshot), **frame next** (control plane), **then floors** (kubelets), **then siding** (workers), **then fixtures** (add-ons + CNI/CSI). And before any of it: **backup the family heirlooms** (etcd + Velero) in case the contractor falls through the floor.

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| Renovation calendar | K8s release cadence (~4 months/minor) |
| "Foundation first" | etcd snapshot before upgrade |
| Frame replacement | kubeadm upgrade apply on cp-1 |
| Mirror the new frame on the other corners | `kubeadm upgrade node` on cp-2/3 |
| New floors over the same frame | kubelet upgrade on each node |
| Siding (one wall at a time) | Worker drain → upgrade → uncordon |
| Light fixtures + plumbing fittings | Add-ons + CNI / CSI |
| Family heirlooms in storage | etcd snapshot + Velero backup before start |
| Contractor's rollback van | Restore from snapshot if upgrade fails |

⚠️ *Analogy stops here:* The analogy stops here: real upgrades don't have nailguns. They have API deprecations, controller restarts, version skew rules, and YAML CRD migrations. The renovation feel undersells the precision needed.

## ELI5 / ELI10

**ELI5.** Every few months, the house gets a renovation. Don't skip three years of renovations and try them all at once — do one per season. Save the family photos before the contractor starts, just in case.

**ELI10.** K8s minors every ~4 months; patches monthly. Skew rule: kubelet may be ≤ 3 minors behind apiserver but never ahead. Upgrade order: etcd snapshot → cp-1 (kubeadm upgrade apply) → cp-2/3 → kubelet on CP → workers (drain + upgrade + uncordon) → add-ons → CNI/CSI. Pre-upgrade: scan for deprecated APIs (Pluto, kubectl convert), test on staging, take etcd snapshot + Velero backup. Rollback: per-component downgrade, etcd restore, or blue-green cluster.

## Real-world scenarios

- **A SaaS doing quarterly upgrades.** Calendar: week 1 = staging upgrade + soak. Week 2 = production CP. Week 3 = production workers. Week 4 = add-on bumps. Repeat next quarter. Upgrades feel boring. Pre-upgrade: Pluto runs in CI on every PR; deprecated APIs caught months before they bite.
- **A bank doing blue-green cluster upgrades.** Build new cluster at v1.36. Migrate workloads via GitOps (Argo CD points at new cluster). Validate. Cut DNS + load balancer. Decommission old cluster. Twice the infra cost during cutover; zero in-place upgrade risk. Used for the most-critical clusters only.
- **A team that hit a 4-minor-behind upgrade.** Cluster on v1.28 in early 2026 (now v1.36 era). Plan: skip n+1 strategy is unsafe, but they can't schedule 4 sequential upgrades. Adopted blue-green: built fresh v1.36 cluster, migrated workloads over 3 weeks via Argo CD, decommissioned old. Total project: 6 weeks; would have been 4-12 months of in-place upgrades + risk.
- **A team using kube-proxy mode change as an upgrade.** K8s 1.31 added nftables mode for kube-proxy (β). Plan: upgrade cluster to 1.32 first; then on a soak weekend, change KubeProxyConfiguration mode iptables → nftables; restart kube-proxy; verify Service traffic still flows. Different from a K8s minor upgrade but follows the same staging-first pattern.

## Common misconceptions

- **Myth:** "kubeadm rolls back automatically on failure."
  **Truth:** No. kubeadm does its best to be atomic per-node, but cluster-wide rollback is on you (snapshot restore or per-component downgrade). Plan for it.
- **Myth:** "You can skip a minor if nothing in your workloads uses removed APIs."
  **Truth:** kubeadm itself enforces +1 minor max. The CRD + admission webhook compat + storage migration + scheduler / kubelet skew rules also assume incremental. Doing it in one shot has been seen to corrupt clusters.
- **Myth:** "Patch versions are safe to skip."
  **Truth:** Mostly true, with exceptions: some patches fix CVEs you should not be running unpatched against. Stay current on patches; skip them only with eyes open.

## Recap

Quarterly upgrades, one minor at a time. Order: etcd snapshot → cp-1 → cp-2/3 → CP kubelets → workers → add-ons → CNI/CSI. Pre-upgrade: deprecated-API scan + staging rehearsal. Rollback: snapshot restore.

**Next — V9: Security Hardening.** CIS benchmark, RBAC least privilege, secret encryption, admission policy, image signing, runtime security, certificate rotation.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
