# Lesson 18 — Storage Part 1 · PV, PVC, StorageClass

> Course: Kubernetes — Common to all distributions
> Module 9 · Storage · Lesson 1 of 2
> Companion preview: `/preview-kubernetes-lesson-18.html`.

---

**🎯 If you remember nothing else:** Pod storage is ephemeral. To survive a Pod restart, declare a PVC (the request). A StorageClass (the recipe) tells K8s how to provision a PV (the actual disk). The PV binds to the PVC and the Pod mounts it.

## Before / After

**Before.** Manual disk wrangling: SSH to a VM, attach an EBS volume, mkfs, mount, edit /etc/fstab, document in a wiki nobody reads. Multiply by 50 services × 3 environments — permanent backlog.

**After.** PVC manifest declaring 10Gi of fast-ssd. kubectl apply. K8s provisions an EBS volume, formats it, attaches to the node, mounts into the Pod. Pod moves → disk follows. No scripts; the cluster handles it.

Declarative storage is just declarative scheduling, applied to disks. The cluster does the wrangling.

## Analogy — the K-Town district

You arrive at K-Town's Customs Warehouse with goods you need to store. You don't pick a locker yourself — you fill out a rental form describing what you need. The clerk reads your form, checks the locker manifest, and either *assigns* you an unused locker that fits or *orders a new one* built to spec. The clerk hands you a key. The warehouse policy book defines what kinds of lockers exist, how to build new ones, and what happens when a renter leaves.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The rental form you fill out | PersistentVolumeClaim (PVC) |
| The locker assigned to you | PersistentVolume (PV) |
| The warehouse policy book | StorageClass |
| The clerk reading your form | The provisioner (CSI driver) |
| "Just me / many of us / read-only" | Access modes (RWO / RWX / ROX / RWOP) |
| Whether the locker is wiped or saved at checkout | Reclaim policy (Delete vs Retain) |
| "Assign now" vs "wait until you arrive" | Volume binding mode (Immediate vs WaitForFirstConsumer) |

⚠️ *Analogy stops here:* Real lockers don't move. K8s persistent volumes can be detached from one node and re-attached to another (within the same zone for cloud block storage), so a Pod can reschedule and keep its disk.

## ELI5 / ELI10

**ELI5.** Your Pod is like a kid at school. The desk gets cleared at the end of every day. To keep their drawings, they need a *cubby*. They ask the teacher for a cubby. Drawings live in the cubby. The kid can move desks; the cubby stays theirs.

**ELI10.** Pod container filesystem is wiped on restart. To keep data, declare a PVC referencing a StorageClass. The cluster's provisioner creates a PV matching the PVC, binds them, mounts the volume into the Pod. Pod restarts re-attach the same PV. Pick access mode by how many Pods need it; pick reclaim policy by whether deleting the PVC should delete the data; pick WaitForFirstConsumer in any multi-zone cluster.

## Real-world scenarios

- **A SaaS startup running PostgreSQL.** Single primary, two read replicas, all on EKS. Storage class: gp3 with 4000 IOPS, WaitForFirstConsumer, Retain reclaim. Each Pod gets a 200 GiB PVC via StatefulSet's volumeClaimTemplates. Pod restarts re-attach the same disk. When they decommission a replica, the PV stays in Released state — a human verifies and deletes manually. Zero data loss in 18 months.
- **A bank running shared log aggregation.** Five Fluentd Pods need to write into the same staging directory before forwarding to a SIEM. ReadWriteMany on Azure Files (SMB-based). Slower than local SSD but everyone can write concurrently. The team accepted the latency hit for the pipeline simplicity.
- **A media company training ML models.** Training Pods need read access to a 4 TB dataset of pre-processed images. Their CSI driver supports ReadOnlyMany from object storage (S3-via-CSI). Each new training run mounts the same PVC; no copying, no duplication.
- **A retail platform migrating from local disk.** Legacy app wrote to /var/lib/myapp/sessions on the host. New PVC mounted at the same path via subPath. Code unchanged. The PVC handles the persistence; the app code stayed identical. Migration was a YAML change, not a refactor.

## Common misconceptions

- **Myth:** A PVC *is* the disk.
  **Truth:** The PVC is the *request*. The PV is the disk. They're separate objects that bind 1:1. You can delete a PVC without deleting the PV (with Retain reclaim policy).
- **Myth:** WaitForFirstConsumer is just an optimisation.
  **Truth:** It's a correctness fix in any multi-zone cluster. With Immediate binding the disk gets provisioned in some random zone *before* the Pod is scheduled — and cloud block storage can't cross zones. The Pod ends up Pending forever.
- **Myth:** Deleting a PVC deletes the data instantly.
  **Truth:** Depends on the PV's reclaim policy. Delete (default for dynamic) → yes, the disk is gone. Retain → the PV moves to Released; data still there until a human decides. For production data, prefer Retain.

## Recap

Three roles: PVC requests storage, StorageClass tells K8s how to make it, PV is the actual disk. Pod restarts → same PV re-attached. Data survives.

Next — Lesson 19: Storage Part 2. CSI drivers under the hood, snapshots and cloning, the new VolumeAttributesClass for live performance changes (GA in 1.34), stateful patterns, multi-attach errors.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
