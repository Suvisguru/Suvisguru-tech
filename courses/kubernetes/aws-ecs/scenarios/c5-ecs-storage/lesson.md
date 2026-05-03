# K-ECS C5 — C5 · ECS Storage — Ephemeral, Bind, Docker, EFS, FSx

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C5 · ECS Storage
> Companion preview: `/preview-kubernetes-ecs-lesson-05.html`.

---

**🎯 If you remember nothing else:** **Pick storage by lifetime + sharing. Ephemeral = per-Task scratch (sized in Task Definition). EFS = the only RWX-across-Tasks-across-AZs answer. Bind mounts + Docker volumes are EC2-only legacy. FSx for Windows or NetApp use cases. Always set ephemeralStorage explicitly on Fargate when you need >20 GiB.**

## 1. Per-Task scratch, sized at Task Definition

**Fargate** Tasks ship with *20 GiB ephemeral storage by default*. Set `ephemeralStorage.sizeInGiB` in the Task Definition top level (range 21-200). Stored on the underlying microVM; **destroyed when the Task stops** — no persistence across Task restarts.
    **EC2 launch**: ephemeral storage is the host disk filesystem. Containers see whatever path they bind-mount; quotas are not enforced per-Task by ECS. Tune via the host's root volume size + cleanup containers (or use Bottlerocket's built-in image GC).
    **External / ECS Anywhere**: same as EC2 — the host's disk is the ephemeral pool.
    **Use cases**: temp file processing, image build buffers, in-memory-DB write-ahead logs that get checkpointed to durable storage. Anywhere you don't need state to survive Task restart.
    **Encryption**: ephemeral storage on Fargate is encrypted with AWS-managed keys by default; customer-managed KMS keys via `ephemeralStorageKmsKeyId` (ECS Fargate platform version 1.4.0+).

## 2. EC2-launch storage patterns

**Bind mounts**: declare a Task-level `volumes` entry with `host: { sourcePath: "/data" }`. Containers mount it via `mountPoints`. Cheap; uses host filesystem. *Lost when Task moves hosts* (ECS may reschedule on a different EC2). *EC2 launch only.*
    **Docker volumes**: Task-level `volumes` with `dockerVolumeConfiguration`. Driver options: `local` (Docker's default — host-local), `rexray/ebs` (EBS-backed via REX-Ray plugin — legacy), other community drivers. *EC2 launch only.* Setup overhead: install + configure the volume driver on every EC2 host (custom AMI or daemonset Tasks).
    **Why these are legacy**: with awsvpc + Fargate dominant, host-coupled storage is rarely the right answer. EFS or ephemeral storage covers most needs; Docker volume drivers require host AMI work that ECS's shift to managed launch types eliminates. Documented for completeness; pick EFS/ephemeral instead for new workloads.

## 3. NFSv4 managed filesystem; access points; mount targets per AZ

**EFS** is a managed NFSv4 filesystem mounted via `volumes[].efsVolumeConfiguration`. Multiple Tasks across multiple AZs mount the same filesystem — true RWX-equivalent. Pay-per-GB-month (Standard or IA storage classes); throughput modes (Bursting, Provisioned, Elastic).
    **Access points**: managed entrypoints into an EFS filesystem with a *path + POSIX UID/GID + permission*. One access point per Task workload. Configure in Task Definition: `accessPointId` + `iam: ENABLED`. ECS auto-mounts at the access point's root path; the Task sees only its own subtree; UID/GID enforced server-side.
    **IAM auth**: `iam: ENABLED` + `transitEncryption: ENABLED` + execution role policy `elasticfilesystem:ClientMount + ClientWrite` on the FS or access point. Replaces relying on host-level NFS auth.
    **Mount targets**: one per AZ in your VPC. Tasks must be in subnets that can reach the access point's mount target (NFS port 2049). Endpoint SG allows port 2049 from Task SGs.
    **Performance gotcha**: EFS Standard is durable + cross-AZ but has higher latency than EBS or local SSD. For high-IOPS small-file workloads, prefer ephemeralStorage + S3 archival or step out to EBS-on-EC2.

## 4. SMB and higher-tier file storage

**FSx for Windows File Server**: managed Windows-native SMB share. Use when Tasks are Windows containers needing SMB shares (legacy Windows apps, file-share-based integrations). Configure in Task Definition with `fsxWindowsFileServerVolumeConfiguration`: `fileSystemId` + `rootDirectory` + `authorizationConfig` (credentialsParameter pointing at SSM/Secrets credentials + domain). Active Directory integration via AWS Managed Microsoft AD or self-managed AD.
    **FSx for NetApp ONTAP**: enterprise-grade NFS / SMB / iSCSI managed by AWS. Multi-protocol (a Linux Task and a Windows Task can share the same dataset). Snapshots, FlexClone, replication, deduplication. Integration with ECS works via `volumes[].efsVolumeConfiguration`-style mounting (NFS endpoint pinned in subnet) — treat the ONTAP NFS endpoint like an EFS mount target. *Choose for use cases needing snapshot speed, multi-protocol, or NetApp-specific features.*
    **FSx for OpenZFS / FSx for Lustre** [ deep dive — skip if new ]: less common with ECS but supported via similar NFS-mount patterns. Lustre for HPC + ML training data lakes; OpenZFS for snapshot-heavy use.

## Before / After

**Before.** Pre-EFS, ECS Tasks needing shared state used hand-rolled patterns: rsync from S3 on Task start, scp between EC2 hosts, EBS volumes attached/detached via Lambda, or hosting the share on a single EC2 with NFS server (single point of failure). Stateful workloads on ECS were rare because the storage story was painful.

**After.** Modern ECS storage is five well-defined shapes — ephemeral for per-Task scratch, EFS for cross-Task RWX, FSx for specialty needs, bind/Docker for EC2-launch legacy. Access points + IAM-auth give clean per-workload isolation. *Stateful ECS workloads are now a Tuesday-deploy.*

*Pick by lifetime first. Per-Task = ephemeral; cross-Task / cross-AZ = EFS; specialty = FSx; EC2-only legacy = bind / Docker. The shape decides the rest.*

## Analogy — the K-Harbor pier

Down at the harbor's **Cargo Holds** there are five places to put cargo while ships work.
    **The ship's own scratch hold** (ephemeral storage) is where each ship dumps temp cargo during the voyage. When the ship sails, the scratch hold goes with it — and when it docks at the breaker's yard, everything in it is gone. Cheap, fast, and yours alone. Each ship picks its scratch-hold size when it gets the cargo manifest.
    **The dock's back-room locker** (bind mount, EC2-only) is a corner of the dock office where one ship borrows shelf space. Cheap, but only that ship at that dock can use it; if the ship moves to another dock the cargo is left behind.
    **The dock's rented locker** (Docker volume, EC2-only) is similar — a dock-managed locker, possibly attached to a portable case (EBS via plugin) that can be moved. Fiddly to set up; mostly used by long-time tenants.
    **The harbor warehouse** (EFS) is the shared building every ship can reach from any dock — fully fireproof and replicated across the harbor district. Multiple ships read and write at once. The harbor master assigns each ship its own gated room (access point) so paperwork and crews stay separate.
    **The specialty bonded warehouse** (FSx for Windows / NetApp ONTAP) is a separate facility for Windows-only ships or for cargo that needs ONTAP's snapshot + dedup features. Niche; pick when the use case demands it.

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Ship's scratch hold (sized at boarding) | ephemeralStorage (Fargate 20→200 GiB; sized in Task Definition) |
| Dock back-room corner | bind mount (EC2 launch host path) |
| Dock rented locker | Docker volume (REX-Ray / local on EC2) |
| Harbor shared warehouse | EFS — RWX across Tasks + AZs |
| Warehouse gated room | EFS access point (path + UID/GID + perms) |
| Mount targets (one per AZ) | EFS mount target per AZ |
| Bonded Windows warehouse | FSx for Windows File Server |
| ONTAP specialty warehouse | FSx for NetApp ONTAP (multi-protocol + snapshots) |
| Warehouse access guard list | IAM-auth: elasticfilesystem:ClientMount/ClientWrite |

⚠️ *Analogy stops here:* A real warehouse holds whatever you put in it; EFS access points enforce server-side UID/GID semantics that surface as POSIX permissions inside the Task. Some POSIX patterns (e.g., setuid binaries) interact differently than on local disk.

## ELI5 / ELI10

**ELI5.** Ships have five places to put cargo. The ship's own scratch hold dies with the ship. The dock corner is shared with one ship at one dock. The shared warehouse can be reached from every dock by every ship at the same time. The bonded Windows warehouse is for Windows-only ships. Pick by what the cargo is and how long you need to keep it.

**ELI10.** **ephemeral** = per-Task scratch (Fargate 20→200 GiB; EC2 host disk). **bind mount** = EC2 host path (host-coupled; legacy). **Docker volume** = EBS / local on EC2 (REX-Ray plugin; legacy). **EFS** = managed NFSv4; RWX cross-Task cross-AZ; access points + IAM auth + mount targets per AZ; the shared-state answer. **FSx for Windows** = SMB share for Windows containers. **FSx for NetApp ONTAP** = multi-protocol enterprise NFS/SMB.

## Real-world scenarios

- **Image processing — bumped ephemeralStorage to 50 GiB.** A 30-engineer media-processing SaaS resizes user-uploaded videos. ZIPs decompress to ~30 GB during work. Task Definition sets `ephemeralStorage.sizeInGiB = 50` on Fargate; per-Task workspace is local SSD-fast; nothing persists between Tasks. *One field flip; problem gone.*
- **Shared uploads — EFS with access points.** A team has an upload Service + a periodic-cleanup Service. EFS filesystem with one access point per workload (uploads, archives, previews); each Service's Task Definition mounts its specific access point. UID/GID isolation prevents cross-workload writes. *Multi-Task RWX without rolling NFS by hand.*
- **Windows legacy — FSx for Windows + Active Directory.** A regulated insurance back-office runs a Windows .NET service that expects an SMB share for input/output documents. ECS on EC2 (Windows ECS-optimised AMI). Task Definition mounts FSx for Windows File Server; AD authentication via `authorizationConfig`. *Lift-and-shift Windows app onto ECS without changing the storage assumption.*
- **Outage — bind mount drift after host replacement.** A team had bind-mounts to `/data/app-state` on EC2 hosts. Auto Scaling replaced one host overnight; new host had no `/data/app-state`; Tasks rescheduled there crashed (or wrote to a fresh empty path with no realisation). *Postmortem*: migrate to EFS — host-independent shared storage. *Bind mounts are a footgun for anything stateful.*

## Common misconceptions

- **Myth:** "Fargate ephemeral storage is unlimited / you don't need to size it."
  **Truth:** **20 GiB default; capped at 200 GiB.** Workloads exceeding 20 GiB must set `ephemeralStorage.sizeInGiB` in the Task Definition. Failing to do so produces "no space left on device" errors mid-Task that look like app bugs.
- **Myth:** "EFS is just a slower EBS."
  **Truth:** EFS and EBS solve different problems. **EBS** is single-instance block storage (one EC2 attaches one volume). **EFS** is multi-instance file storage (many Tasks across many AZs share). EFS is higher-latency than EBS; you trade for cross-Task / cross-AZ RWX. Don't pick by speed alone.
- **Myth:** "Bind mounts work fine on Fargate."
  **Truth:** **Bind mounts are EC2 launch only.** Fargate has no host filesystem you can bind to. The Fargate equivalents are ephemeralStorage (per-Task scratch) and EFS (cross-Task shared).

## Recap

Five storage shapes; pick by lifetime + sharing. Ephemeral for per-Task scratch (size it!), EFS for shared-state RWX, FSx for Windows / ONTAP specialty. Bind mounts and Docker volumes are EC2-only legacy.

**Next — C6: ECS Deployment and Scaling.** Rolling updates (deploymentConfiguration, minimumHealthyPercent, maximumPercent); circuit breaker; rollback. Blue/green via CodeDeploy; external deployment controller. Service Auto Scaling. Cluster auto scaling (capacity providers with managed scaling). Placement constraints + strategies.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
