# K-AKS A4 — A4 · AKS Storage (Disks, Files, NetApp, Blob, Container Storage)

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A4 · AKS Storage
> Companion preview: `/preview-kubernetes-aks-lesson-04.html`.

---

**🎯 If you remember nothing else:** **Default to Azure Disks CSI (Premium SSD v2) for RWO with WaitForFirstConsumer; Azure Files for RWX; ANF for low-latency DBs; Blob for cheap object access. Use VolumeAttributesClass to resize/retier without remount; Secrets Store CSI for Key Vault.**

## 1. Azure Disks CSI — the RWO default

**Azure Disks CSI driver** is the default for ReadWriteOnce (RWO) Persistent Volumes. Backed by Azure Managed Disks. Tiers in increasing performance/cost: **Standard HDD** (cheapest), **Standard SSD**, **Premium SSD**, **Premium SSD v2** (current recommended default — independent IOPS / throughput tuning), **Ultra Disk** (sub-millisecond, extreme IOPS for SAP HANA / huge OLTP).
    **Critical detail — zone affinity:** a Premium SSD lives in one availability zone. A Pod can only mount a disk if the Pod is scheduled in the same zone. The **StorageClass** shipped with AKS sets `volumeBindingMode: WaitForFirstConsumer` — disk provisioning is delayed until the Pod is scheduled, then the disk is provisioned in that Pod's zone. *If you create a custom StorageClass without this setting, you re-introduce the cross-AZ-attach failure.*
    **VolumeAttributesClass** (GA) is the K8s-native way to change a PV's performance tier *without remount*. Premium SSD v2: change IOPS / throughput on a running PV via a `VolumeAttributesClass` reference. Ultra Disk: same. Workload doesn't restart.
    **ZRS (Zone-Redundant Storage):** for Standard SSD and Premium SSD, Azure offers a ZRS variant that replicates synchronously across three zones — disk can attach to a Pod in any zone of the region. *Higher latency than LRS, but solves cross-AZ attach for stateful workloads that need it.*

## 2. Azure Files CSI + Azure NetApp Files

**Azure Files CSI** for ReadWriteMany (RWX). Backed by Azure Files. Two protocols:
    
      - **SMB** — works on Linux + Windows nodes. Most common.

      - **NFS v4.1** — Linux only; better for POSIX semantics. Premium tier required for NFS.

    
    Use cases: shared writable storage across multiple Pods (CMS file uploads, shared logs, ML datasets being written by multiple workers). Premium tier for performance; ZRS for multi-AZ resilience. *Avoid for high-IOPS DB workloads — Disks or ANF are far faster.*
    **Azure NetApp Files (ANF)** — managed NetApp ONTAP service, exposed to AKS via the ANF CSI driver. Tier choices: Standard / Premium / Ultra (in MiB/s per TiB). For SAP HANA, large Postgres / Oracle / SQL Server, low-latency DB workloads needing < 1ms. Higher base cost than Files but in a different performance class.
    **Azure Container Storage** — unified data plane that exposes *local NVMe (ephemeral disks on the node)* as Persistent Volumes alongside Disks and ANF. Use case: high-IOPS stateful workloads where you can tolerate node-loss replication done at the application layer (Cassandra, Elasticsearch, Kafka). Replaces the older OpenEBS / local-PV setups.

## 3. Blob CSI (BlobFuse2) + Secrets Store CSI

**Azure Blob CSI** mounts an Azure Blob container as a filesystem inside a Pod, via **BlobFuse2**. Two access modes: *BlobFuse* (caching, POSIX-ish) and *NFS 3.0* (for storage accounts that support it). Use cases: huge ML training datasets (TBs of read-only inputs cheaply held in Blob); image/asset libraries; cheap append-only logs. *Performance is not Disk-class* — fine for sequential reads, not for transactional DBs.
    **Secrets Store CSI driver + Azure Key Vault provider**: declares secrets/keys/certs to fetch via a `SecretProviderClass`; mounts them as files in Pods. Authenticates to Key Vault via **Workload Identity**. Optional: sync to a K8s Secret. Auto-rotation polls Key Vault and updates the volume; the Pod sees fresh values via volume reload (or rolling restart). *The clean way to consume Key Vault secrets in AKS — no app code changes.*

## 4. Snapshots, expansion, ZRS, topology-aware scheduling

**VolumeSnapshot** (K8s standard CRD) backed by Azure Managed Disk snapshots — point-in-time backup of a PV. Restore by creating a new PVC with `dataSource` pointing at the snapshot. Cross-region restore via storage account replication.
    **Volume expansion** — Azure Disks CSI supports online expansion. Edit the PVC's `spec.resources.requests.storage` upward; the disk grows; the filesystem grows. *Not all disk types support online expansion in all sizes* — check tier limits.
    **ZRS variants** — for stateful workloads needing AZ resilience without app-level replication, switch the StorageClass to a ZRS-backed disk type. Trade-off: slightly higher latency.
    **Topology-aware scheduling:** StorageClass `allowedTopologies` can constrain disks to specific zones (e.g. force all DB disks into `eastus-1` to align with a hot/warm DR pattern). Combined with Pod nodeSelector / topology spread constraints to keep workloads + storage co-located.

## Before / After

**Before.** Pre-CSI AKS used in-tree volume drivers — limited features, slow innovation cycle, no online resize, no snapshot CRD, no VolumeAttributesClass. RWX needed third-party Helm-installed nfs-server-provisioner with manual storage account wiring. Secret consumption from Key Vault required custom init-containers calling the Key Vault REST API and writing files. Stateful workloads on multi-AZ clusters routinely failed cross-AZ attach because StorageClasses lacked `WaitForFirstConsumer`.

**After.** Modern AKS ships **five managed CSI drivers** (Disks, Files, Blob, ANF, Container Storage) with **VolumeSnapshot**, **online expansion**, and **VolumeAttributesClass** (live tier change without remount). RWX is one PVC. Key Vault secrets mount as files via the Secrets Store CSI driver, authenticated by Workload Identity. `WaitForFirstConsumer` is the default. Stateful workloads work cleanly across zones with ZRS or topology-aware scheduling.

*Storage in AKS is now declarative and survivable. The hard part shifted from "how do I attach a disk?" to "what backend matches my workload?"*

## Analogy — the K-Campus wing

The **Library** is K-Campus's storage building. Five wings hold different kinds of books, each suited to a different purpose.
    **Wing A — Personal lockers** (Azure Disks): one student per locker, fast, locked. The locker lives in a specific corner of the building (an availability zone). If you want a multi-corner locker, use the ZRS lockers — slightly slower but accessible from any corner. The Library has a special trick: you can swap out the lock to upgrade the locker speed without taking your books out (**VolumeAttributesClass**).
    **Wing B — Reading rooms** (Azure Files): multiple students share the same desk and the same papers. Read-write-many. Use SMB (works for everyone, even Windows visitors) or NFS (Linux scholars only).
    **Wing C — Reference rare-books** (Azure NetApp Files): super-fast access for the most demanding scholars (SAP HANA, big databases). Pricier librarians, but they hand you the book in under a millisecond.
    **Wing D — Warehouse** (Azure Blob via BlobFuse2): cheap stacks holding 10 TB of training data; you fetch a chapter at a time. Not for transactional reads.
    **Wing E — The vault** (Secrets Store CSI + Key Vault): no books here, only sealed envelopes containing keys, certs, secrets. The Library Concierge (Workload Identity) opens envelopes for authorised Pods only.

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| Personal locker | Azure Disks CSI — RWO Persistent Volume |
| Locker that lives in a specific corner | Single-zone Premium SSD |
| Multi-corner locker (slightly slower) | ZRS-backed Disk |
| Swap-out lock without removing books | VolumeAttributesClass — live tier change |
| Shared reading room desk | Azure Files CSI — RWX (SMB or NFS) |
| Rare-books wing | Azure NetApp Files — sub-ms latency |
| Warehouse stacks | Azure Blob CSI via BlobFuse2 |
| The vault of sealed envelopes | Secrets Store CSI + Azure Key Vault |
| Library Concierge | Workload Identity — authorises secret retrieval |
| "Wait for the student before issuing the locker" | `volumeBindingMode: WaitForFirstConsumer` |
| Photocopying a chapter | VolumeSnapshot CRD |
| Adding shelves to an existing locker | Online volume expansion |
| Local NVMe drawer at every desk | Azure Container Storage — local NVMe as PVs |

⚠️ *Analogy stops here:* A library has fixed wings; CSI drivers can be added or upgraded without rebuilding the cluster. Real CSI also has driver-version compatibility windows the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** A big library with five wings. One wing has lockers for one student. Another has shared desks for groups. One has fast lookups for important books. One has cheap stacks for huge collections. One has a vault for secret keys. You pick the wing that matches what your work needs.

**ELI10.** AKS storage = five managed CSI drivers. **Disks** for RWO (default Premium SSD v2 with WaitForFirstConsumer for zone-correct provisioning; VolumeAttributesClass for live tier changes; ZRS for multi-AZ). **Files** for RWX (SMB / NFS). **NetApp Files** for sub-ms DB latency. **Blob** via BlobFuse2 for huge object datasets. **Container Storage** for local NVMe-as-PV. Plus **Secrets Store CSI** with Key Vault provider, authed by Workload Identity. VolumeSnapshot CRD for backup; online expansion supported.

## Real-world scenarios

- **Postgres on AKS — single-zone Disks + ZRS for DR.** A Postgres workload runs as a 3-replica StatefulSet. Each replica is pinned to a specific zone (anti-affinity), each with a Premium SSD v2 in that same zone. Cross-zone replication is handled by Postgres streaming replication. For DR, weekly VolumeSnapshots cross-region replicate via storage account GRS to a paired region. *Tested DR restore: full Postgres rebuild from snapshot in 18 minutes.*
- **ML pipeline — Blob CSI for 200 TB of training data.** An ML team needs read-only access to 200 TB of image datasets across hundreds of training Pods. Storing this on Premium SSD = $50K/month. Storing on Blob (Cool tier) = $2K/month. They mount the container via Azure Blob CSI (BlobFuse2 caching mode); training I/O is sequential reads — perfect Blob workload. *96% cost reduction; same throughput thanks to BlobFuse2 read cache + parallel readers.*
- **SaaS — RWX shared logs via Azure Files SMB.** A SaaS has 12 microservices that all need to write to a shared rolling-log directory consumed by Filebeat. Single Azure Files share, mounted RWX as SMB by all 12 Deployments. Premium tier for IOPS. ZRS for AZ resilience. *One PVC, twelve Pods writing concurrently, no NFS server to operate.*
- **Bank — Key Vault secrets via Secrets Store CSI.** A bank rotates DB credentials every 24 hours via Key Vault's rotation policy. Pods mount the secret via Secrets Store CSI driver with the Azure Key Vault provider, Workload-Identity-authenticated. Driver's rotation poller pulls Key Vault every 2 minutes. App watches the file and reloads its DB pool when the file changes — *zero restart, zero downtime, zero secret in Pod env.*

## Common misconceptions

- **Myth:** "My Premium SSD will reattach to any Pod regardless of zone."
  **Truth:** Premium SSDs are single-zone resources. A disk created in `eastus-1` can only attach to a Pod scheduled in `eastus-1`. Without `WaitForFirstConsumer` + topology-aware scheduling, the kube-scheduler will happily place a Pod in `eastus-2` and the attach will fail. Use the default StorageClass (which has WaitForFirstConsumer) or a ZRS variant.
- **Myth:** "I should resize disks by recreating the PVC."
  **Truth:** Azure Disks CSI supports **online volume expansion**. Edit the PVC's `spec.resources.requests.storage` upward; the underlying disk grows; the filesystem grows. No remount, no Pod restart needed. Recreating the PVC throws away the data.
- **Myth:** "VolumeAttributesClass and StorageClass are the same."
  **Truth:** **StorageClass** defines how PVs get *provisioned*. **VolumeAttributesClass** (GA) defines how an *existing* PV's attributes (IOPS, throughput) can be modified after creation, without remount. They're complementary — use VAC to retier a Premium SSD v2 from 3000 IOPS to 16000 IOPS without losing data.

## Recap

Five storage backends mapped to use cases; VolumeAttributesClass for live tier change; Secrets Store CSI for Key Vault. Multi-AZ stateful is solved (WaitForFirstConsumer or ZRS).

**Next — A5: AKS Scaling.** Cluster Autoscaler (default), Karpenter for AKS / Node Auto Provisioning (NAP), KEDA, Spot pools, GPU, Windows, ARM (Cobalt, Ampere Altra), Confidential Computing nodes (DCasv5/ECasv5), PDB-aware maintenance, multi-zone scaling.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
