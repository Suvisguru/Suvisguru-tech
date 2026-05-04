# K-ADV-DR D1 — D1 · etcd Backup + Velero + Kasten K10 + CloudCasa

> Course: K-ADV-DR (advanced specialization)
> Module D1 · etcd + Velero + K10 + CloudCasa
> Companion preview: `/preview-kubernetes-adv-dr-lesson-01.html`.

---

**🎯 If you remember nothing else:** **etcd = control-plane state. Velero = workload + PVC backup. K10 = commercial app-aware. CloudCasa = SaaS DR. Always test restore quarterly.**

## 1. Foundation of cluster rebuild

**etcd** holds all K8s API state. `etcdctl snapshot save` creates a point-in-time snapshot. Per-cluster backup pattern: cron-job snapshot every 6h to S3 (encrypted) + retention policy.
    Restore: provision fresh cluster; `etcdctl snapshot restore` the snapshot; control plane reconstructs from etcd. Use case: total cluster loss, control-plane corruption.
    Managed K8s (EKS / GKE / AKS): cloud handles etcd backup; you can't directly snapshot. Backup workloads via Velero instead.

## 2. K8s-native backup; CSI / Kopia / Restic

**Velero**: K8s-native backup framework. Backs up: K8s objects (Deployment / Service / etc.) + PVCs (via CSI snapshot or filesystem-backup with Restic / Kopia).
    Per-cluster: `Backup` CR with namespace selector + schedule; `Restore` CR with mapping. **BackupStorageLocation** = S3 / Azure Blob / GCS. **VolumeSnapshotLocation** per CSI driver.
    Patterns: full-cluster nightly + per-namespace hourly + per-tenant on-demand. Restore: namespace-by-namespace; selective resource restore.

## 3. Commercial app-aware backup

**Kasten K10** (Veeam): commercial K8s backup. Application-aware (knows database state needs quiescing); rich policies (RBAC + RPO + RTO + compliance reports).
    Trade self-host for richer dashboards + commercial support + multi-cluster aggregation.

## 4. SaaS DR-as-a-service + how to choose

**CloudCasa**: SaaS DR — install agent in cluster; backups + restores managed by CloudCasa platform. Trade engineering time for hosted simplicity.
    **Selection**: Velero for K8s-shop self-host; K10 for commercial-support + richer features; CloudCasa for managed-DR-as-a-service. etcd snapshot always required for self-managed clusters.

## Before / After

**Before.** Pre-tested-DR: backups configured but never restored; restore failures discovered during real outage; RTO blown.

**After.** Modern: etcd snapshot + Velero / K10 / CloudCasa with quarterly restore drills; RPO + RTO measured + improved.

*Backup that's never restored is a hope. Quarterly drills convert hope to plan.*

## Analogy — the K-Lifeboat cell

Drill Square is where the lifeboat crew practices. Four kit options: **etcd snapshot** = ship's logbook backup; **Velero** = standard lifeboat kit (CSI snapshots / Kopia / Restic); **Kasten K10** = commercial-grade kit; **CloudCasa** = rented lifeboats with hired crew.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Ship's logbook | etcd snapshot |
| Standard lifeboat kit | Velero + CSI / Kopia / Restic |
| Commercial-grade kit | Kasten K10 (Veeam) |
| Rented lifeboats + crew | CloudCasa (SaaS DR) |
| Drill drill drill | Quarterly restore test |
| Backup destination | BackupStorageLocation (S3 / Blob / GCS) |
| Per-volume snapshot | VolumeSnapshotLocation per CSI driver |

⚠️ *Analogy stops here:* A real lifeboat is physical; backups are bytes — invisible until restore-tested. Untested backup ≈ no backup.

## ELI5 / ELI10

**ELI5.** Four ways to keep a lifeboat ready. The crew practices monthly so the boat works when the ship sinks.

**ELI10.** **etcd snapshot**: control-plane state via etcdctl. **Velero**: K8s-native + CSI snapshots / Kopia / Restic. **Kasten K10**: commercial app-aware. **CloudCasa**: SaaS-managed DR. Quarterly restore-test mandatory.

## Real-world scenarios

- **Velero saved a tenant from accidental deletion.** Tenant accidentally deleted prod namespace; Velero hourly backup restored within 15 min; data loss = 1h (within RPO).
- **K10 for compliance-heavy regulated cluster.** Health-tech runs Kasten K10; commercial support + HIPAA reports; restore-tested monthly with documented RTO.
- **CloudCasa for small team.** 5-engineer SaaS adopts CloudCasa; saved 1-2 engineer-weeks of Velero setup; managed DR for ~$1k/mo.
- **Outage — backup never restored.** Cluster died; team tried Velero restore; StorageClass missing; restore failed; 6-hour outage. Postmortem: quarterly restore drill mandated.

## Common misconceptions

- **Myth:** "Velero backs up everything."
  **Truth:** Velero backs up K8s objects + PVCs; doesn't back up etcd directly (managed K8s = cloud-managed; self-managed = use etcdctl). Doesn't backup external services (RDS, Vault, S3 outside cluster).
- **Myth:** "Backup is the hard part."
  **Truth:** **Restore is the hard part.** Quarterly restore drills find issues that backup verification doesn't — StorageClass mismatches, NetworkPolicy misalignment, dependency order.
- **Myth:** "Cloud-managed K8s makes backup unnecessary."
  **Truth:** Cloud manages etcd; doesn't back up your workloads + PVCs + secrets. Velero / K10 / CloudCasa still required.

## Recap

Backup tools: etcd snapshot (self-managed) + Velero (K8s-native) + K10 (commercial) + CloudCasa (SaaS). Quarterly restore-test mandatory.

**Next — D2: GitOps-driven recovery + cluster rebuild + application restore.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
