# K-EKS E5 — E5 · EKS Storage (EBS, EFS, FSx, S3 Mountpoint)

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E5 · EKS Storage
> Companion preview: `/preview-kubernetes-eks-lesson-05.html`.

---

**🎯 If you remember nothing else:** Storage CSI drivers (managed add-ons): **EBS CSI** (RWO block; gp3 default; **VolumeAttributesClass for live IOPS/throughput tuning**), **EFS CSI** (RWX, multi-AZ), **FSx CSI** (Lustre / NetApp ONTAP / OpenZFS), **S3 Mountpoint CSI** (object as FS, read-heavy). **snapshot-controller** for VolumeSnapshot. **KMS encryption** on every StorageClass. **WaitForFirstConsumer** for zone-aware provisioning.

## 1. Pick storage by access pattern, not by name

DriverAccess modeWhen$/GB-month (rough)
      
        **EBS CSI**RWO (one node)Stateful workloads (Postgres, Redis); single-replica primary$0.08 (gp3); $0.125 (io2)
        **EFS CSI**RWX (many nodes)Shared content stores, log staging, multi-Pod readers$0.30 (Standard); $0.16 (IA)
        **FSx Lustre CSI**RWX HPCHPC, ML training datasets, parallel filesystems~$0.25-0.60 depending on tier
        **FSx ONTAP CSI**RWX enterprise NASNetApp shops; enterprise NFS/SMBpremium
        **FSx OpenZFS CSI**RWX with snapshots/clonesHeavy snapshot/clone use; faster than EFS for some patterns~$0.10
        **S3 Mountpoint CSI**RWX read-mostlyML datasets, logs archive, immutable content$0.023 (Standard) + request fees

## 2. gp3 / io2 + VolumeAttributesClass

**gp3** (general purpose SSD) is the default for most workloads. **io2** (provisioned IOPS) for > 16K IOPS or sub-ms latency requirements. **st1/sc1** (HDD) for cold logs / batch.
    2026 game-changer: **VolumeAttributesClass** (K8s 1.34 GA, EBS CSI supports it). Live re-tune IOPS / throughput on a PVC by changing one label — no detach, no Pod restart. Promo traffic spike: bump from 3000 IOPS to 8000 IOPS in 30 seconds.
    `# StorageClass — gp3 with KMS encryption + WaitForFirstConsumer
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: gp3-encrypted}
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-east-1:123:key/abc"
volumeBindingMode: WaitForFirstConsumer    # critical for multi-AZ
reclaimPolicy: Delete
allowVolumeExpansion: true
---
# VolumeAttributesClass — premium burst
apiVersion: storage.k8s.io/v1beta1
kind: VolumeAttributesClass
metadata: {name: premium-burst}
driverName: ebs.csi.aws.com
parameters:
  iops: "8000"
  throughput: "500"`

## 3. When EBS isn't enough

**EFS CSI**: RWX, multi-AZ, infinite scale. Mounts as NFS. Good for shared content + log staging. Slower than local EBS; $0.30/GB-month vs $0.08. Provisioning modes: *dynamic* (CSI creates EFS access points per PVC) or *static* (point at an existing EFS).
    **FSx Lustre CSI**: RWX, parallel filesystem, HPC-grade throughput. Used for ML training datasets where 1000s of GPUs read concurrently. Pricier; provisioning is slow (15+ min).
    **FSx ONTAP CSI**: NetApp ONTAP. Enterprise NAS features (NFS+SMB, dedup, replication). Used by orgs with existing NetApp investment + workloads needing premium NAS.
    **FSx OpenZFS CSI**: cheaper than ONTAP; great snapshot + clone performance.
    **S3 Mountpoint CSI** (newer; 2023 GA): mounts an S3 bucket as a filesystem. Read-mostly; writes are append-only or full-object-rewrite. Killer use case: ML training reads 10TB dataset from S3 directly without staging to EBS.

## 4. Cross-cutting decisions

- **snapshot-controller**: install once cluster-wide. Enables `VolumeSnapshot` CRD; CSI drivers (EBS, EFS, FSx) implement the actual snapshot.

      - **KMS encryption**: every StorageClass should set `encrypted: true` + `kmsKeyId`. Default to a customer-managed key (CMK), not the AWS-managed default key — gives you key-rotation control + cross-account access constraints.

      - **volumeBindingMode: WaitForFirstConsumer**: *required* in multi-AZ clusters. Without it, EBS provisions in a random AZ before the Pod is scheduled; Pod lands in a different AZ; FailedAttachVolume forever.

      - **Multi-attach errors**: EBS attaches to one node at a time. Pod reschedules to a different node → AWS detaches from old + attaches to new; takes ~6 min worst case. For high-availability stateful: use StatefulSet (stable identity per Pod) + per-Pod EBS via volumeClaimTemplates; reduces but doesn't eliminate attach delays.

    
    [ deep dive — skip if new ]EBS multi-attach (RWX EBS via io2 + special config) exists but rarely fits — the EBS multi-attach is volume-level, not filesystem-level; you need a cluster-aware filesystem on top. Most teams use EFS for RWX instead.

## Before / After

**Before.** Manual EBS volumes attached via console + edits to fstab on EC2. Backup script to S3 maybe runs nightly. KMS on some volumes. Multi-AZ failures involve recovery scripts a junior engineer wrote.

**After.** EBS CSI managed add-on. PVC YAML in git creates volume + KMS-encrypted by default. WaitForFirstConsumer for zone alignment. VolumeSnapshot for backup. VAC for live perf changes. Storage is K8s-native.

EKS storage works exactly like vanilla K8s storage with the AWS CSIs and KMS-by-default — once you align CIDR / AZ / encryption at launch.

## Analogy — the K-Skyline floor

The Storage Vault occupies a quiet floor of K-Skyline. Walk in: rows of safe-deposit boxes (EBS — one tenant per box, RWO), shared filing cabinets (EFS — many tenants, RWX), specialty vaults for HPC tenants (FSx Lustre / ONTAP / OpenZFS), and a vast warehouse you can shelf-mount (S3 Mountpoint). Every box, cabinet, vault is locked with the building's master key system (KMS). The vault clerk schedules photographs of every box overnight (snapshots). And there's a clear rule: *safe-deposit boxes don't move floors* (EBS is single-AZ).

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Safe-deposit box (one tenant) | EBS volume (RWO) |
| Shared filing cabinet (many tenants) | EFS (RWX) |
| HPC parallel-access vault | FSx Lustre |
| Enterprise NAS specialty vault | FSx ONTAP |
| Cheap photo-loving vault | FSx OpenZFS |
| Public archive shelf-mountable | S3 Mountpoint |
| Master key system | KMS encryption (encrypted: true + kmsKeyId) |
| Overnight box photographs | VolumeSnapshot via snapshot-controller |
| Boxes don't move floors | EBS is single-AZ; multi-AZ Pod = wait or snapshot |
| Live re-renting with new IOPS tier | VolumeAttributesClass (live IOPS change) |

⚠️ *Analogy stops here:* The analogy stops here: real CSI drivers run as DaemonSets + controller Deployments coordinating with EBS / EFS / FSx APIs over IAM-authenticated calls. The vault is software, not steel.

## ELI5 / ELI10

**ELI5.** Different lockers for different needs. Solo locker (EBS), shared library (EFS), super-fast HPC locker (FSx), and a giant photo-warehouse you can pretend is a locker (S3 Mountpoint). All locked with the same master key system.

**ELI10.** Four CSI driver families: EBS (RWO block, default); EFS (RWX shared, multi-AZ); FSx Lustre/ONTAP/OpenZFS (specialty); S3 Mountpoint (object as FS, read-heavy). All install as managed add-ons. Always set encrypted+kmsKeyId on StorageClasses. WaitForFirstConsumer for multi-AZ. VolumeAttributesClass (1.34) for live IOPS changes on EBS. snapshot-controller cluster-wide enables VolumeSnapshot.

## Real-world scenarios

- **A SaaS using gp3 + VAC for promotional bursts.** Standard StorageClass: gp3 3000 IOPS / 125 MB/s. Promo VAC: 8000 IOPS / 500 MB/s. PVC patched at 14:00 → live re-tune in 30s → patched back at 22:00. Cost only during the window. Saved a permanent over-provision.
- **A bank with multi-AZ Postgres on StatefulSet + EBS.** 3 Postgres replicas, each with own EBS via volumeClaimTemplates. WaitForFirstConsumer. Pod-Disruption-Budget minAvailable=2. Rolling Pod restart: each Pod's EBS detaches + reattaches in same AZ; ~30s each; replication catches up.
- **An ML team using S3 Mountpoint for training data.** 4 TB image dataset in S3. S3 Mountpoint CSI mounts the bucket as `/data`. PyTorch reads directly. No staging to EBS. Cost: ~$100/month for the dataset + read requests. Pre-Mountpoint: copying to EFS or EBS cost 10× more + staging time was hours.
- **A team that fixed a multi-AZ scheduling issue.** HPA scaled a StatefulSet from 1 → 3. Original Immediate-binding StorageClass provisioned all 3 PVCs in us-east-1a. Topology-spread placed Pods in 1a, 1b, 1c. 2 Pods Pending. Migration: delete failed PVCs, switch StorageClass to WaitForFirstConsumer, redeploy. Now zone-aligned.

## Common misconceptions

- **Myth:** "EBS RWO means one Pod."
  **Truth:** RWO = one node. Multiple Pods on the same node can mount the same EBS. RWOP (1.27+) is the new "one Pod" semantic.
- **Myth:** "WaitForFirstConsumer is just an optimisation."
  **Truth:** In multi-AZ clusters it's a correctness fix. Without it, EBS volumes land in random AZs and Pods stuck Pending. Always use it.
- **Myth:** "S3 Mountpoint is a full POSIX filesystem."
  **Truth:** Read-mostly. Writes are append-only or full-object replace. No directory rename, no random write into a file. Great for ML datasets, awkward for general apps.

## Recap

Four CSI drivers (EBS / EFS / FSx / S3) as managed add-ons. KMS-encrypted by default. WaitForFirstConsumer in multi-AZ. VolumeAttributesClass for live perf changes. snapshot-controller cluster-wide for VolumeSnapshot.

**Next — E6: EKS Compute and Autoscaling.** Karpenter (recommended), Cluster Autoscaler (legacy), spot strategies, Graviton, GPU + Inferentia + Trainium for AI/ML.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
