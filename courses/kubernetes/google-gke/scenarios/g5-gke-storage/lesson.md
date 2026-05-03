# K-GKE G5 — G5 · GKE Storage (PD, Hyperdisk + Storage Pools, Filestore, GCS FUSE, Parallelstore)

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G5 · GKE Storage
> Companion preview: `/preview-kubernetes-gke-lesson-05.html`.

---

**🎯 If you remember nothing else:** **Default to PD CSI (pd-balanced) with WaitForFirstConsumer for RWO; Regional PD for cross-zone resilience; Hyperdisk + Storage Pools + VolumeAttributesClass for tunable performance; Filestore for RWX; GCS FUSE for cheap object datasets; Parallelstore for HPC/AI; Backup for GKE for managed DR.**

## 1. Persistent Disk CSI — RWO default

**Persistent Disk CSI driver** = default RWO storage. Backed by Compute Engine Persistent Disks. Tiers in increasing performance/cost:
    
      - **pd-standard** (HDD, cheapest) — for cold / archival workloads.

      - **pd-balanced** (recommended default) — SSD-backed; balanced cost/perf for most stateful workloads.

      - **pd-ssd** — high-IOPS SSD; for latency-sensitive DBs.

      - **pd-extreme** (legacy) — superseded by Hyperdisk.

    
    **Zone affinity (critical):** a standard PD lives in *one zone*. A Pod can mount a PD only if scheduled in that same zone. The default StorageClass has `volumeBindingMode: WaitForFirstConsumer` — disk provisioning waits until the Pod is scheduled, then provisions in the right zone. *Custom StorageClasses without this setting re-introduce the zone-mismatch bug.*
    **Regional PD** = synchronous replication across two zones in a region. Survives single-zone failure; can attach to a Pod in either zone. Higher latency than zonal; the right choice for stateful workloads needing HA without app-level replication.

## 2. Hyperdisk + Storage Pools + VolumeAttributesClass

**Hyperdisk** = next-gen GCP block storage. Variants:
    
      - **Hyperdisk Balanced** — general-purpose; replaces pd-balanced for many use cases.

      - **Hyperdisk Throughput** — high-throughput workloads (analytics, log processing).

      - **Hyperdisk Extreme** — extreme IOPS; for SAP HANA, large OLTP.

      - **Hyperdisk ML** — optimised for ML training data loading; multi-attach supported.

    
    **Storage Pools** = the pool-based capacity model: provision capacity + IOPS + throughput at the *pool* level; carve PVCs out of the pool. *Decouples per-PVC over-provisioning from total cost.* Many workloads at low utilisation share the pool; cost reflects actual consumption.
    **VolumeAttributesClass** (K8s GA feature) — change a PV's performance attributes *online*, no remount. With Hyperdisk: change IOPS / throughput targets via a `VolumeAttributesClass` reference on the PVC. Example: tune Postgres from 3,000 IOPS to 16,000 for a holiday-traffic event without restarting the Pod.
    **Snapshots** (K8s VolumeSnapshot CRD) — point-in-time backup of a PV; restore by creating a new PVC with `dataSource` pointing at the snapshot. Cross-region snapshot replication via the Compute Engine snapshot location.
    **Online expansion** — increase PVC size; Hyperdisk + PD support online filesystem grow without unmount.

## 3. Filestore CSI + GCS FUSE CSI + Parallelstore CSI

**Filestore CSI** = RWX shared filesystem via NFS. Tiers: *Basic HDD/SSD* (legacy), *Zonal* (single zone), *Enterprise* (multi-zone HA). Use cases: shared writable storage across multiple Pods (CMS uploads, build artifacts, ML scratch). *Avoid for high-IOPS DB workloads* — Hyperdisk Extreme is the right tier for that.
    **GCS FUSE CSI** = mount a GCS bucket as a filesystem in a Pod. Backed by Cloud Storage FUSE. Use cases: huge ML training datasets read sequentially (TBs at object-storage cost ~$0.02/GB-month vs PD ~$0.17/GB-month for Standard tier); image/asset libraries; cheap append-only logs. *Performance is not block-class* — fine for sequential reads, not transactional DBs. Caching modes available for repeat-read workloads.
    **Parallelstore CSI** = managed parallel filesystem for HPC + AI training. Backed by DDN EXAScaler. Throughput in the GiB/s range across multiple clients. Use cases: distributed training where multiple GPU nodes need to read training data simultaneously at line rate; HPC simulations; anything that hits the bandwidth wall on standard NFS. *Pricier per GB; the right answer when training-step time is bottlenecked on data loading.*

## 4. Backup for GKE + Secret Manager CSI + topology-aware scheduling

**Backup for GKE** = managed backup service. Captures cluster-wide K8s manifests + Persistent Volume snapshots + (optionally) cross-region restoration. Schedule + retention policies via the Backup for GKE API. Restore into the same or a different cluster. *The DR primitive — wire this in early; it's much harder to retrofit during an incident.*
    **Secret Manager CSI driver** (covered in G4) — mount Secret Manager secrets as files in Pods, WIF-authenticated, auto-rotation. The clean way to consume secrets without K8s Secrets in etcd.
    **Topology-aware scheduling:** StorageClass `allowedTopologies` can constrain disks to specific zones (e.g., force DB disks into `us-central1-a` for a hot/warm DR pattern). Combined with Pod nodeSelector or topology-spread constraints to keep workloads + storage co-located.
    **CMEK across storage:** all five backends support CMEK via Cloud KMS — disks, Filestore, GCS, Parallelstore, snapshots — for compliance + key sovereignty. Key rotation is a Cloud KMS operation; PVs continue to work transparently.

## Before / After

**Before.** Pre-CSI GKE used in-tree volume drivers — limited features, no online resize for a long time, no VolumeSnapshot CRD, no VolumeAttributesClass. RWX needed third-party Helm-installed nfs-server-provisioner with manual Filestore wiring. ML training data on PD = expensive; HPC parallel filesystems were DIY (Lustre on GCE). DR was "hope you have a snapshot script."

**After.** Modern GKE ships **five managed CSI drivers** (PD, Hyperdisk + Storage Pools, Filestore, GCS FUSE, Parallelstore) with VolumeSnapshot, online expansion, VolumeAttributesClass for live tier changes. **Backup for GKE** is the managed DR primitive (cluster-wide manifests + PV snapshots; cross-region restoration). Secret Manager CSI for keyless secrets. *Storage in GKE is now declarative, performant, and survivable.*

*Pick the backend that matches the access mode + performance class. Don't skip Backup for GKE — DR not wired before incident = DR not available during incident.*

## Analogy — the K-Garden plot

The **Reservoir & Compost** is the K-Garden's storage building. Five backends.
    **Personal water tanks** (Persistent Disk): one tank per gardener, fast, locked. The tank lives in a specific zone of the garden; for cross-zone resilience, use the Regional PD twin-tank that replicates synchronously across two zones.
    **Hyperdisk pool**: instead of buying a personal tank, you draw from a *shared reservoir* the head gardener provisions; capacity, IOPS, and throughput are pool-level. A magical valve (VolumeAttributesClass) lets you turn the pressure up live without unhooking your hose. Variants: balanced for general use, throughput-tuned for big sprinklers, extreme for HANA-class precision irrigation, ML-tuned for training-data multi-attach.
    **Shared communal sink** (Filestore): multiple gardeners use the same NFS sink for shared seedling washing. Enterprise tier replicates across zones.
    **Compost pile / mulch warehouse** (GCS FUSE): cheap stacks holding 200 TB of training data; you fetch by armful when needed. Sequential reads only — not for transactional grabs.
    **HPC parallel pump system** (Parallelstore): when 100 gardeners are all loading training data simultaneously and your throughput needs are GiB/s.
    And the **Disaster-Relief Vault** (Backup for GKE) is the managed insurance: weekly snapshots of the whole garden's state, restorable into a new garden in a different region.

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| Personal water tank | Persistent Disk CSI — RWO PV |
| Tank in a specific zone | Single-zone pd-ssd / pd-balanced |
| Twin-tank cross-zone | Regional PD |
| Shared reservoir + magical valve | Hyperdisk + Storage Pools + VolumeAttributesClass |
| Magical pressure valve | VolumeAttributesClass — live IOPS / throughput change |
| Communal sink (NFS) | Filestore CSI — RWX |
| Filestore zonal vs Enterprise | Single-zone vs multi-zone HA |
| Compost pile / mulch warehouse | GCS FUSE CSI |
| HPC parallel pump system | Parallelstore CSI (HPC / AI training) |
| Disaster-Relief Vault | Backup for GKE |
| Vault key-fetch desk | Secret Manager CSI driver (covered in G4) |
| "Wait for the gardener before issuing the tank" | `volumeBindingMode: WaitForFirstConsumer` |
| Photocopying a chapter | VolumeSnapshot CRD |
| Adding shelves to existing tank | Online volume expansion |
| "Padlock with your key on every storage room" | CMEK via Cloud KMS |

⚠️ *Analogy stops here:* A garden's tanks are physical and bounded; CSI drivers can be added or upgraded without rebuilding the cluster. Real Hyperdisk has compatibility constraints with specific machine families the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** Five storage choices: a personal tank, a shared reservoir with a magical pressure valve, a communal sink, a compost-warehouse for huge cheap stuff, and a parallel-pump for HPC. Plus an insurance vault that backs up the whole garden weekly.

**ELI10.** GKE storage = five managed CSI drivers. **PD CSI** for RWO (pd-balanced default; pd-ssd; **Regional PD** for cross-zone HA; default StorageClass uses WaitForFirstConsumer for zone-correct provisioning). **Hyperdisk + Storage Pools** for tunable IOPS/throughput + VolumeAttributesClass live changes. **Filestore CSI** for RWX (NFS, Enterprise tier multi-zone). **GCS FUSE CSI** for cheap object-as-FS (ML datasets). **Parallelstore CSI** for HPC/AI parallel filesystem. Plus **Backup for GKE** for managed DR (cluster-wide manifests + PV snapshots, cross-region restore). VolumeSnapshot CRD for backup; online expansion supported; CMEK across all backends.

## Real-world scenarios

- **Postgres on GKE — Regional PD for HA without app-level replication.** A small Postgres workload on GKE — single primary, no streaming replica yet. Team uses **Regional PD** on a Hyperdisk Balanced StorageClass. PVC bound to a Regional PD that replicates synchronously across us-central1-a + us-central1-c. Pod scheduled in either zone can mount. *Single-zone failure: Pod re-schedules to surviving zone with same data.*
- **ML team — GCS FUSE for 200 TB training data.** ML team needs read-only access to 200 TB image datasets across hundreds of training Pods. PD for this = $30K+/month. **GCS FUSE** mounts the bucket as a Pod filesystem; sequential reads with caching mode. Cost: ~$4K/month (Cool tier). *Same throughput; ~85% saving.*
- **Hyperdisk + VolumeAttributesClass for Black Friday burst.** Postgres workload on Hyperdisk Balanced provisioned at 3,000 IOPS / 240 MiB/s. Black Friday traffic 10×. Team creates a VolumeAttributesClass with 16,000 IOPS / 800 MiB/s, references it from the PVC. Hyperdisk applies online; no Pod restart. After the event, switch back to the lower-spec VAC. *Pay for high tier only during the burst.*
- **Bank — quarterly Backup for GKE drill restored cluster in 35 minutes.** A bank schedules nightly Backup for GKE backups: cluster-wide manifests + all PV snapshots, cross-region replication to the paired DR region. Quarterly drill: spin up empty cluster in DR region; restore from latest backup; verify workloads. *Last drill: restoration completed in 35 minutes; auditor approved RTO target of < 1 hour.*

## Common misconceptions

- **Myth:** "Regional PD doubles my storage cost for free HA."
  **Truth:** Regional PD synchronously replicates across two zones. Cost is roughly 2x a single-zone disk + small write-latency overhead (sync replication). For workloads that don't need cross-zone attach, single-zone PD + Backup for GKE for DR is cheaper. Pick Regional PD when the workload genuinely needs cross-zone attach.
- **Myth:** "Storage Pools are for cost-saving teams; everyone else uses individual Hyperdisks."
  **Truth:** Storage Pools shine when you have *many PVCs at low utilisation*. Pool capacity and IOPS budget shared = aggregate spend matches actual peak rather than sum-of-per-PVC peaks. For one or two huge PVCs at sustained 100% utilisation, individual Hyperdisks are simpler. The mental model: pool when you have many tenants; individual when you have few large ones.
- **Myth:** "GCS FUSE is fine for transactional databases."
  **Truth:** GCS FUSE is object-storage-as-FS. Eventual consistency on metadata + non-POSIX semantics (no fsync guarantees, no real file locking, latency in the 100ms+ range for object operations). Catastrophic for transactional DBs. Excellent for ML datasets, image/asset libraries, append-only log archives — anything sequential-read.

## Recap

Five storage backends mapped to use cases; Hyperdisk + Storage Pools + VolumeAttributesClass for tunable performance; Backup for GKE wired early; multi-zone via Regional PD or topology + WaitForFirstConsumer.

**Next — G6: GKE Scaling and Cost.** Cluster Autoscaler, Node Auto-Provisioning (NAP), Autopilot scheduling/billing, Compute Classes (Balanced / Performance / Scale-Out / Accelerator), Spot, GPU (A3/A4 with H100/H200/B200), TPU (Trillium / Ironwood), HPA with custom metrics, BigQuery cost export.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
