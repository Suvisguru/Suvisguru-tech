# Lesson 19 — Storage Part 2 · CSI, Snapshots, Cloning, VolumeAttributesClass

> Course: Kubernetes — Common to all distributions
> Module 9 · Storage · Lesson 2 of 2
> Companion preview: `/preview-kubernetes-lesson-19.html`.

---

**🎯 If you remember nothing else:** Behind every PVC sits a **CSI driver** — a vendor-supplied plug-in that handles the actual disk plumbing. Once you have a CSI driver you get **snapshots** (point-in-time copies), **cloning** (new PVC from existing PVC or snapshot), **expansion** (grow the disk), and **VolumeAttributesClass** (re-tune performance live, GA in 1.34).

## 1. What CSI actually is

Lesson 18 ended with "the StorageClass calls a provisioner." This lesson is about that provisioner. The **Container Storage Interface (CSI)** is a gRPC API specification — a contract between Kubernetes (the orchestrator) and the storage system (EBS, Ceph, NFS, vSAN, anything). Vendors write CSI drivers that implement the spec; K8s talks to them through standard sidecar containers (`external-provisioner`, `external-attacher`, `external-snapshotter`, `external-resizer`).
    The CSI driver runs in the cluster as a Deployment (the controller-side, one replica) plus a DaemonSet (the node-side, one Pod per node). The controller-side handles *create / delete / attach / detach / snapshot* calls — the cluster-wide stuff. The node-side handles *mount / unmount / format* — the per-node stuff that has to happen on the actual machine where the Pod runs. Every storage operation from the K8s API ends up as a gRPC call into one of those two CSI Pods.
    Why this matters: anything you've ever heard described as "Kubernetes storage" — snapshots, clones, expansion, attribute changes — is actually a CSI driver feature K8s exposes through a standard API. If your driver doesn't implement a feature, K8s can't expose it. Always check your driver's capability list before promising features to a team.

## 2. Snapshots, clones, expansion, attribute changes

📸
        VolumeSnapshot
        point-in-time copy
        Asks the CSI driver to take an instant snapshot of a PVC. The snapshot is a separate object (`VolumeSnapshot` + `VolumeSnapshotContent`) and survives PVC deletion. You can restore by creating a new PVC with `dataSource: VolumeSnapshot`.
        Use for: backups, pre-migration safety nets, dev environments hydrated from prod.
      
      
        🧬
        PVC cloning
        PVC from PVC
        Create a new PVC by setting `dataSource: existing-PVC`. The CSI driver does a fast-path copy (typically a copy-on-write at the storage layer, much faster than a manual `cp`). Both PVCs must be in the same namespace and the same StorageClass.
        Use for: dev clones of prod data, testing schema migrations on a copy.
      
      
        📈
        Volume expansion
        grow without downtime
        Edit the PVC's `spec.resources.requests.storage` upward. If the StorageClass has `allowVolumeExpansion: true` and the CSI driver supports it, the disk and filesystem grow online. Most modern drivers (EBS, GCE PD, Azure Disk, Ceph RBD, Longhorn) support this.
        Use for: an alert says you're at 90% disk; bump the PVC.
      
      
        🎚️
        VolumeAttributesClass (NEW)
        change perf live · GA 1.34
        A new object alongside StorageClass that lets you re-tune *performance attributes* (IOPS, throughput) on a live PVC by changing one label. The CSI driver re-modifies the underlying disk in place. No detach, no snapshot, no Pod restart.
        Use for: temporary performance bursts; tier migrations; cost optimisation.
      
    
    All four require the CSI driver to advertise the relevant capability. `kubectl get csidriver` tells you which features are available. `kubectl get csistoragecapacity` tells you how much capacity each topology has.

## 3. StatefulSet + volumeClaimTemplates

Most stateful workloads use a **StatefulSet** (covered in L16) with `volumeClaimTemplates`. Each replica gets its own PVC named after the Pod (`data-mysql-0`, `data-mysql-1`, …). Pods rescheduling brings the same disk back to the same Pod identity. PVCs are *not* deleted when the StatefulSet is deleted — that's intentional, so you can rebuild a StatefulSet without losing data.
    Two patterns built on this:
    
      - **Backup + restore via VolumeSnapshot.** Snapshot every Pod's PVC nightly. To restore one replica, delete its PVC, create a new one with `dataSource` pointing at the snapshot. The StatefulSet's controller binds the new PVC by name as if nothing happened.

      - **Test environments via cloning.** Clone a prod PVC into a dev namespace (or snapshot then restore), and you've got a realistic test database in seconds, not hours of `pg_dump`.

    
    [ deep dive — skip if new ]The kubelet doesn't talk to your storage system directly. It speaks the Mount Service Interface (MSI) over a Unix socket to the node-side CSI driver Pod, which in turn invokes the cloud or storage SDK. This means the actual mount operation happens inside a privileged container on the node — that's why CSI drivers ship with a privileged DaemonSet. If you've ever seen a CSI driver hang and Pods stuck in `ContainerCreating`, that's typically the node-side Pod failing to complete a mount.

## Before / After

**Before.** Manual snapshots: SSH to the storage system, take a snapshot, write down the ID, copy the ID into a runbook. Backup retention = a script someone updates. Restoring means recreating the volume by hand.Performance changes: detach the volume, modify it through the cloud console, re-attach. Pod restart. Five-minute outage minimum.

**After.** Snapshots: `kubectl apply -f snapshot.yaml`. The `VolumeSnapshot` object lives in the namespace, retention controlled by a `VolumeSnapshotClass`, restoration is just another PVC with `dataSource`.Performance changes: `kubectl edit pvc` + a `volumeAttributesClassName` label change. CSI driver re-tunes the live disk. No Pod restart.

All of this is the same pattern as the rest of K8s: the operator declares intent; a controller (CSI driver) makes it true. Storage joined the declarative party in 2019; live attribute changes joined in 2024.

## Analogy — the K-Town district

Back at the Customs Warehouse, but now we walk behind the counter to the loading dock. The PV (locker) you saw last lesson is still there — but who *delivers* a new locker when one is needed? Who *photographs* a locker for posterity? Who *upgrades* the lock from a basic latch to a deadbolt without unloading anything?That is the **CSI driver**: a licensed contractor truck that pulls up to the dock with all the equipment for one specific kind of storage (the EBS truck, the NFS truck, the Ceph truck). The warehouse manager (Kubernetes) phones the truck through a standard intercom (the CSI gRPC spec); the truck does the work. **Snapshots** are a tenant photographer who copies a locker. **Clones** are a duplicator that makes a working copy. **Expansion** is a foreman who can bolt extensions onto a locker without making the renter empty it. **VolumeAttributesClass** is a quality-of-service dial — turn it up for premium IOPS, turn it down to save money — applied to a locker in use.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The contractor truck pulled up to the dock | The `CSIDriver` object + DaemonSet + Deployment |
| The standard intercom the manager uses | The CSI gRPC API spec |
| The tenant photographer | `VolumeSnapshot` / `VolumeSnapshotContent` |
| The locker duplicator | PVC `dataSource` cloning |
| The foreman bolting on extensions | Volume expansion (`allowVolumeExpansion: true`) |
| The quality-of-service dial | `VolumeAttributesClass` (GA in 1.34) |
| The locker can be at one node only | Multi-attach errors with RWO + cloud block storage |

⚠️ *Analogy stops here:* The analogy stops here: real CSI drivers don't "drive in" — they're permanent Pods running in the cluster. And the snapshot's not a Polaroid; it's typically a copy-on-write block reference at the storage layer, which is why it's instant and storage-efficient.

## ELI5 / ELI10

**ELI5.** Lesson 18 was about the locker (PV), the form (PVC), and the policy (StorageClass). This lesson is about the *person* who actually opens a locker for you, photographs it, copies it, or makes it bigger. That person is the CSI driver. They drive a truck specific to the kind of locker you want.

**ELI10.** The **CSI** (Container Storage Interface) is a gRPC API. Vendors implement it as a CSI driver — typically a Deployment (controller-side: create/attach/snapshot calls) plus a DaemonSet (node-side: mount/format calls). Once the driver is installed, K8s exposes its features via standard objects: `VolumeSnapshot` for backups, PVC `dataSource` for clones, PVC size edits for expansion, and `VolumeAttributesClass` (GA in 1.34) for live performance changes. None of these features are "in" Kubernetes — they're all gated by what your CSI driver supports.

## Real-world scenarios

- **A startup running PostgreSQL on EKS.** Uses the AWS EBS CSI driver. Nightly `VolumeSnapshot` at 2 AM via a CronJob. Retention 30 days via VolumeSnapshotClass. After a botched migration, restoring took 4 minutes — create new PVC from yesterday's snapshot, scale StatefulSet down/up. The team's RTO went from hours to single-digit minutes.
- **A bank running multiple Ceph CSI clusters.** On-prem with Rook-Ceph. Uses RBD for block (RWO) and CephFS for shared (RWX). Policy: every PVC must have a `VolumeAttributesClass` labelling its perf tier. Bronze = HDD pool, silver = SSD, gold = NVMe. Live tier changes happen during business-hour traffic surges; reverted at night.
- **A media company cloning prod into staging.** Production database PVC is 4 TiB. Old staging refresh = 6 hours of pg_dump + restore. New process: `kubectl apply` a clone PVC referencing the prod PVC as `dataSource`. CSI driver does copy-on-write at the storage layer; staging PVC is ready in 90 seconds. Daily refresh now feasible.
- **A SaaS expanding capacity in-place.** Alert: PVC at 88%. Engineer edits the PVC, bumps storage from 100Gi to 250Gi. CSI driver expands the EBS volume; the kubelet runs `resize2fs` on the live filesystem. Pod never restarts. Total time: 90 seconds. The old way (recreate PVC bigger) would have meant a database failover.

## Common misconceptions

- **Myth:** Snapshots are application-consistent.
  **Truth:** They're *crash-consistent* — equivalent to pulling the power cord. Database engines (Postgres, MySQL) usually handle this via their own crash-recovery, but for true app-consistency you want a pre-snapshot quiesce hook (which K8s 1.31+ supports via `VolumeGroupSnapshot` and pre/post hooks).
- **Myth:** VolumeAttributesClass is the same as StorageClass.
  **Truth:** StorageClass = recipe for *provisioning* a new PV. VolumeAttributesClass = recipe for *tuning attributes* on an existing PV. They're separate objects. A PVC has both `storageClassName` (immutable after binding) and `volumeAttributesClassName` (changeable; that's the whole point).
- **Myth:** Multi-attach errors are a Kubernetes bug.
  **Truth:** They're cloud reality. EBS, GCE PD, Azure Disk attach to one node at a time. If a Pod's old node is unreachable but K8s thinks it's still attached, the new Pod's mount fails. The fix is `force-detach` via the CSI driver — most modern drivers do this automatically after a node is marked NotReady.

## Recap

Behind every PVC there's a CSI driver. Once the driver's there, you get snapshots, clones, online expansion, and VolumeAttributesClass for live performance changes — none of which existed in the K8s core; they all came from CSI vendors implementing the spec.

**Next — Lesson 20: Configuration & Secrets.** ConfigMap, Secret, KMS-encryption-at-rest, and the External Secrets Operator. Why "secret" in K8s is mostly a polite fiction unless you wire up encryption-at-rest. Permit Office issues the credentials.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
