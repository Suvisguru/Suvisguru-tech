# K-OCP O7 — O7 · OpenShift Storage

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O7 · OpenShift Storage
> Companion preview: `/preview-kubernetes-ocp-lesson-07.html`.

---

**🎯 If you remember nothing else:** **Default to ODF for software-defined storage with RWX + object; Local/LVM Operators for SNO/edge; per-cloud CSI for cloud-native deployments. Plan registry + monitoring storage at install. OADP for backup/DR.**

## 1. OpenShift Data Foundation (ODF) — Ceph + NooBaa + Rook

**OpenShift Data Foundation (ODF)** is Red Hat's software-defined storage platform built on:
    
      - **Ceph** — distributed block + filesystem storage. RBD (block) + CephFS (RWX shared FS).

      - **NooBaa** — multi-cloud object storage gateway. Speaks S3 API; can back to local Ceph or external clouds.

      - **Rook** — Kubernetes operator that orchestrates Ceph (deployment, scaling, recovery).

    
    ODF runs *inside* the OCP cluster — Ceph OSD pods on dedicated worker nodes (typically 3+ nodes with attached local or block-storage devices). Provides:
    
      - Block storage (PVC type RWO) via CephRBD CSI.

      - RWX shared filesystem via CephFS CSI.

      - Object storage via NooBaa S3 endpoint.

    
    **Use case:** on-prem clusters needing software-defined storage; bare-metal deployments where you don't have a cloud-block-storage equivalent; clusters needing RWX without external NFS.
    Sizing: 3+ ODF storage nodes; 4+ TB raw capacity per node typical for small clusters; replicate-3 or erasure-coded; ~2-3x raw → usable conversion.

## 2. Local Storage Operator + LVM Storage Operator + cloud CSI drivers

**Local Storage Operator** — for nodes with attached block devices that need to be exposed as PVs (e.g., bare-metal NVMe). Uses `LocalVolume` + `LocalVolumeSet` CRs to discover + provision local block devices as PVs. Static-provisioned PVs (no dynamic creation). For workloads that benefit from local storage (Cassandra, Elasticsearch, Kafka).
    **LVM Storage Operator (LVMS)** — single-node + edge clusters where ODF's 3-node minimum doesn't fit. Carves a single node's storage into LVM volumes; provides dynamic PVCs from a thin pool. *For SNO + MicroShift + small edge clusters.*
    **Per-cloud CSI drivers** shipped with OCP:
    
      - **vSphere CSI** — VMDK-backed PVCs on vSphere installations.

      - **AWS EBS CSI** — gp2/gp3/io1/io2 EBS volumes; single-zone; topology-aware.

      - **Azure Disk CSI** + **Azure File CSI** — disk for RWO; file for RWX SMB/NFS.

      - **Google PD CSI** — pd-balanced/pd-ssd; single-zone or Regional PD for cross-zone.

    
    OCP installs the right CSI driver automatically based on the cluster's platform (set during install). Default StorageClass uses `volumeBindingMode: WaitForFirstConsumer` to align PV creation with Pod scheduling zone.

## 3. RWX storage + VolumeSnapshot + expansion + VolumeAttributesClass

**RWX (ReadWriteMany)** options on OCP:
    
      - **ODF CephFS** — multi-zone, integrated with cluster.

      - **Azure Files CSI** (SMB or NFS) — managed RWX on Azure.

      - **NFS** via external NFS server + nfs-csi-driver Operator (community) — for on-prem with existing NetApp / Isilon.

      - **EFS CSI** on AWS — managed RWX via Elastic File System.

    
    **VolumeSnapshot** (K8s standard) — supported across all OCP-shipped CSI drivers. Per-PV point-in-time snapshot; restore by creating new PVC with `dataSource` referencing the snapshot.
    **Online volume expansion** — supported by all OCP cloud + ODF CSI drivers. Edit PVC `spec.resources.requests.storage` upward; CSI driver expands the underlying volume + filesystem.
    **VolumeAttributesClass** — K8s GA feature for live tier change without remount. With ODF: change Ceph storage-class quality params on the running PVC. With cloud CSIs: cloud-provider-specific support (e.g., AWS gp3 IOPS retier).

## 4. OADP (Velero-based) + registry storage + monitoring storage

**OADP (OpenShift APIs for Data Protection)** = Velero-based managed backup integrated with OCP. **DataProtectionApplication** CR configures backup destination (S3 / NooBaa / Azure Blob / GCS); **Backup** CR triggers cluster-wide manifest + PV snapshot backup; **Restore** CR rehydrates into the same or different cluster. Cross-cluster + cross-region restore.
    OADP also handles application-consistent snapshots via Velero plugins (Restic-based for non-snapshot-supporting CSI drivers; CSI snapshot for the rest). Schedule + retention policies via Velero Schedule CR.
    **Registry storage planning:** the internal container registry needs a PVC backed by storage that survives Pod migration. *If using EBS / Azure Disk / GCE PD (single-zone), the registry must be pinned to a single zone* — accept the failure mode or switch to ODF / NooBaa / external S3-compatible bucket. For prod, S3 / NooBaa / GCS / Azure Blob is the recommended backend (registry storage doesn't need block; object suffices).
    **Monitoring storage:** Prometheus stores TSDB data in PVCs (default 15-day retention). Plan storage class + size per cluster. For long-term storage, use Thanos sidecar to ship blocks to S3-compatible storage. *Don't put Prometheus storage on the same single-zone PD as the workloads it monitors — single-zone failure means alerts about the failure are themselves silenced.*

## Before / After

**Before.** Pre-CSI OCP used in-tree volume drivers — fewer features, slow innovation. RWX on bare-metal needed third-party NFS server install. ODF was a separate product with manual operator install. Edge / SNO had no managed storage path; you ran NFS or other DIY. Backup/DR was Velero self-installed; no integrated CR + cluster operator support.

**After.** OCP ships **ODF as a productized + supported software-defined storage platform** (Ceph + NooBaa + Rook). **Local + LVM Storage Operators** for SNO/edge. **Per-cloud CSI** drivers shipped + auto-installed by platform. **OADP** as integrated Velero-based DR. **VolumeSnapshot** + **online expansion** + **VolumeAttributesClass** across drivers.

*Pick the storage backend that matches your cluster shape: ODF for on-prem multi-node; per-cloud CSI for cloud; LVMS for SNO/edge. Wire OADP for DR before you need it.*

## Analogy — the K-Foundry bay

The **Inventory Warehouse** at K-Foundry is where parts are stored. Multiple shelving systems coexist.
    The **ODF system** is the foundry-built shelving — Ceph robots (block + file storage), NooBaa concierge (S3 object storage), Rook foreman managing it all. Sized for the foundry; replicates parts across 3+ shelves for resilience. Provides every kind of part-storage need (RWO block, RWX shared filesystem, object).
    For *satellite warehouses* (SNO + edge sites), the **Local + LVM Operators** manage local-only shelves: simpler, smaller, no robot army needed.
    For *cloud-built foundries*, the right cloud-provider shelf is auto-installed: vSphere shelves on vSphere, EBS on AWS, Disk/File on Azure, PD on GCP. Each respects its cloud's zone constraints.
    The **OADP backup desk** (Velero-based) takes nightly inventory snapshots + ships them to a remote vault (S3 / Azure Blob / GCS / NooBaa). Restore = rehydrate into the same or different foundry.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| ODF foundry-built shelving | OpenShift Data Foundation (Ceph + NooBaa + Rook) |
| Ceph block-storage robots | CephRBD CSI (RWO) |
| Ceph file-share robots | CephFS CSI (RWX) |
| NooBaa S3 concierge | NooBaa object storage gateway |
| Rook foreman | Rook operator (orchestrates Ceph) |
| Satellite warehouse shelves | Local Storage + LVM Storage Operators (SNO/edge) |
| Cloud-provider shelves | Per-cloud CSI (vSphere / AWS EBS / Azure Disk+File / GCP PD) |
| Wait-for-customer policy | `volumeBindingMode: WaitForFirstConsumer` |
| Photocopy a shelf | VolumeSnapshot CRD |
| Add room to a shelf | Online volume expansion |
| Live shelf-tier upgrade | VolumeAttributesClass |
| Backup desk + remote vault | OADP (Velero) + S3/Azure Blob/GCS backup destination |
| Internal-parts shelf | Internal container registry storage (PVC or S3-compatible) |
| Monitoring archive shelf | Prometheus TSDB + Thanos to long-term S3 |

⚠️ *Analogy stops here:* A real warehouse has fixed walls; ODF is software-defined and grows by adding worker nodes with disks. Real Ceph requires careful tuning the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** The warehouse has many shelf types: foundry-built (ODF), small-shop shelves (LVMS), cloud-provider shelves (CSI), and a backup desk that copies inventory to a remote vault.

**ELI10.** OCP storage = ODF (Ceph + NooBaa + Rook for SDS) + Local Storage Operator + LVM Storage Operator (SNO/edge) + per-cloud CSI (vSphere/EBS/Azure/PD). RWX via ODF CephFS / Azure Files / NFS / EFS. VolumeSnapshot + online expansion + VolumeAttributesClass across drivers. OADP (Velero-based) for backup/DR with S3/Blob/GCS/NooBaa destinations. Plan registry + monitoring storage at install.

## Real-world scenarios

- **Bank — ODF on-prem with RWX for shared logs.** On-prem bank cluster: ODF with 4 storage nodes + 8TB local NVMe each. CephRBD provides RWO PVCs; CephFS provides RWX for a shared logs directory consumed by 12 microservices; NooBaa provides internal S3 for image registry + Prometheus long-term storage. *One software-defined storage platform; no external SAN required.*
- **Telco — LVMS on SNO at 800 cell sites.** Each cell site = 1 SNO. LVM Storage Operator carves the single node's 2TB SSD into thin-pool LVM volumes; provides dynamic PVCs for site-local workloads. ACM (covered in O10) federates the 800 SNOs.
- **AWS — registry on NooBaa-backed S3 instead of EBS.** AWS-installed OCP. Default registry uses EBS PVC — single-zone, fails on Pod migration. Migration: install ODF + NooBaa; switch registry to NooBaa S3 endpoint; registry now zone-resilient. Same fix could use AWS S3 directly. *Simple registry storage gotcha; bake the fix into install runbook.*
- **DR drill — OADP restored cluster in 38 minutes.** Bank schedules nightly OADP backups: cluster-wide manifests + PV snapshots; cross-region replicated to S3 in DR region. Quarterly drill: spin up empty cluster in DR region; `oc create restore`; verify workloads + data come up. *Last drill: 38 minutes total; auditor approved RTO of < 1 hour.*

## Common misconceptions

- **Myth:** "ODF is overkill for small clusters."
  **Truth:** For multi-node clusters needing RWX + object storage + DR alongside RWO, ODF is often the simplest path — one platform vs assembling NFS server + S3 service + block storage separately. *For SNO/edge, ODF's 3-node minimum doesn't fit — use LVMS instead.*
- **Myth:** "VolumeSnapshot backs up everything."
  **Truth:** VolumeSnapshot is a per-PV point-in-time snapshot — preserves block/file data but not application consistency (e.g., a Postgres mid-transaction snapshot is corrupt without quiescing). For app-consistent backups: Velero/OADP with appropriate Restic or CSI plugin + pre/post hooks (e.g., `pg_dump` before snapshot).
- **Myth:** "Single-zone EBS PVC is fine for everything."
  **Truth:** Single-zone EBS = if the holding zone fails, the PVC is unrecoverable until zone returns. *For stateful workloads needing multi-zone, use Regional EBS, ODF (multi-node Ceph spans zones), Azure Files / EFS / Filestore, or app-level replication (Postgres streaming replica)*. Internal registry, Prometheus, etcd backups all need multi-zone-aware planning.

## Recap

Five storage paths for OCP: ODF (multi-node SDS), Local + LVM Operators (SNO/edge), per-cloud CSI (cloud-native), RWX via CephFS / Azure Files / NFS / EFS, OADP for DR. Plan registry + monitoring storage at install.

**Next — O8: OpenShift Operations.** ClusterVersion + update channels + EUS + CVO + cluster operators; MachineConfigPools, MachineSets, MachineHealthChecks; node maintenance; etcd backup; must-gather; Insights telemetry; disconnected updates; mirror registry; upgrade risk assessment.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
