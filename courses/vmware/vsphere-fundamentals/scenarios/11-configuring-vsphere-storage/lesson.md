# Lesson 11 — Configuring vSphere Storage

> Format: **per-subtopic** (six subtopics).

---

## Lesson opener

Hosts and a vCenter without storage hold no VMs. Storage in vSphere is exposed
through **datastores** — logical containers the hypervisor consumes. Six moves
to understand and configure storage:

1. **Overview** — datastores and the four types vSphere supports.
2. **VMFS** on block storage (FC, iSCSI).
3. **NFS** datastores (file storage over IP).
4. **vSAN** — hyperconverged storage built from local host disks.
5. **vVols** — VM-centric storage on smart arrays.
6. **Storage Policy-Based Management (SPBM)** + thin vs thick provisioning.

---

# Subtopic 1 of 6: Storage overview — datastores and the four types

## Concept

A **datastore** is the unit of storage vSphere consumes. It's a logical
container that a host (or a cluster of hosts) mounts and uses to store VM
files (`.vmdk`, `.vmx`, snapshots, ISOs, etc.). All VMs you ever create live
on one or more datastores.

vSphere supports four types of datastore, each with different mechanics
underneath:

- **VMFS** — VMware's clustered file system on **block** storage. The host
  sees a raw LUN over Fibre Channel (FC), FCoE, or iSCSI, formats it with
  VMFS, and shares it among hosts in the cluster.
- **NFS** — vSphere mounts a network file system from a NAS appliance over
  IP. The NAS owns the file system; vSphere just stores files there.
- **vSAN** — vSphere pools the local disks across cluster hosts into one
  software-defined datastore. No external array; the cluster *is* the
  storage.
- **vVols (Virtual Volumes)** — a smart-array datastore where each VM's
  storage is a separate object the array tracks individually. Requires a
  VASA-capable array.

The choice depends on what your storage infrastructure already is. A shop
with an existing FC array uses VMFS. A NAS-centric shop uses NFS. A
greenfield deployment increasingly chooses vSAN. vVols is for shops with
modern arrays that want VM-level storage policy without leaving their
existing array.

vSphere uses the same VM management model regardless of which datastore
type is underneath — the hypervisor presents a consistent surface, the
underlying mechanics differ.

## Before / After

**Before**: You hear "VMFS" and "NFS" and "vSAN" and they all sound like
the same thing — "where VMs live." You can't tell why someone would pick
one over the other.

**After**: You can place each on the spectrum: block-vs-file, external-vs-
local, file-system-on-host vs file-system-on-array, VM-aware vs not. You
know the trade-offs that drive the choice.

## Analogy

A datastore is the building's storage room. Different rooms hold things
differently — VMFS is a shared warehouse floor, NFS is a leased file room
down the hall, vSAN is the building making its own storage room out of
every closet, vVols is a smart locker system that knows what's in each
locker.

## Quick check

> **Question** — A team wants to run VMs but has no external storage
> array — just servers with local disks. They want shared storage that
> all hosts can use. What's their natural choice?
>
> **Answer** — vSAN. It pools the local disks across hosts into one
> software-defined datastore that all hosts can use, with no external
> array required. Other options (VMFS over iSCSI to local LUNs, NFS to a
> separate VM acting as NAS) exist but are workarounds, not the
> intended design.

## ELI5

The big computer needs a place to keep all its little computers' files.
That place is called a datastore. There are different kinds — some are
shared boxes from a central warehouse, some are file rooms next door,
some are made by sharing each computer's own drives.

## ELI10

A datastore is a logical place where vSphere stores virtual machine
files. There are four kinds: VMFS (the host puts a VMware file system on
top of a SAN LUN), NFS (the host mounts a network file system from a
NAS), vSAN (the cluster pools its local disks), and vVols (a smart array
exposes per-VM storage objects). The right choice depends on what
storage you already have. The good news: vSphere abstracts the
differences, so creating, moving, snapshotting, and managing VMs feels
the same whatever's underneath.

## Real world — what you see live

vSphere Client → Datastores. You see a list: <code>ds-vmfs-01</code>
(VMFS over iSCSI), <code>ds-nfs-share</code> (NFS from a NetApp filer),
<code>ds-vsan-cluster1</code> (vSAN pooled from local disks).
Right-click any → New Datastore. The wizard asks Type: VMFS / NFS / vVol.
Pick VMFS, point to a LUN the storage team presented to the hosts,
format with VMFS-6, give it a name. Five minutes later it's mountable on
every host in the cluster.

---

# Subtopic 2 of 6: VMFS datastores on block storage (FC, iSCSI)

## Concept

**VMFS (Virtual Machine File System)** is VMware's clustered file system
designed for shared block storage. The flow:

1. The storage array exposes a **LUN** (Logical Unit Number) — a chunk of
   block storage with a unique identifier.
2. The host sees the LUN through one or more **HBAs** (Host Bus
   Adapters): FC HBA, FCoE CNA, iSCSI initiator (software or hardware).
3. The host formats the LUN with **VMFS** (latest is VMFS-6).
4. Multiple hosts can mount the same VMFS volume simultaneously and
   share VMs across it. VMFS handles the locking that makes that safe.

**Multipathing** matters: each LUN should be reachable through multiple
paths (multiple HBAs, multiple switch fabrics, multiple array
controllers). vSphere uses the **Pluggable Storage Architecture (PSA)**
with selectable path policies:

- **Most Recently Used (MRU)** — uses the most recently working path;
  doesn't fail back automatically. Default for active/passive arrays.
- **Fixed** — sticks with a preferred path; falls back to alternates if
  it fails, then comes back to preferred when available. Active/active.
- **Round Robin** — distributes I/O across all available paths. Most
  active/active arrays. Default for many modern arrays.
- **Vendor-specific (NMP, MEM, etc.)** — array vendors ship their own
  multipathing modules for their hardware.

**Block storage choices**:

- **Fibre Channel (FC)** — purpose-built fabric, very low latency, very
  high cost. Used in big enterprises.
- **iSCSI** — block storage over TCP/IP. Cheaper (rides Ethernet),
  ubiquitous in mid-market and labs.
- **FCoE** — FC frames over Ethernet. Once popular, now declining.

VMFS is the workhorse for pre-vSAN environments and remains common
where existing block storage is in place.

## Before / After

**Before**: Your storage team hands you a 2 TB LUN ID and says "have at
it." You're not sure where to start in vSphere.

**After**: You add the LUN visible to all cluster hosts via FC or iSCSI
to a vSphere datastore wizard, format it as VMFS-6, give it a name, and
mount it. Multipathing config is set to Round Robin. The datastore is
now usable on every host.

## Analogy

VMFS on a block LUN is like a shared warehouse floor with one big
concrete slab — multiple hosts walk in and store crates there
together. Multipathing is having multiple loading docks so you don't
depend on one. VMFS is the floor markings that keep everyone from
running into each other.

## Quick check

> **Question** — A new VMFS datastore is mounted on host-1 only. host-2
> doesn't see it even though both hosts are connected to the same SAN.
> What's the most likely cause?
>
> **Answer** — The LUN isn't presented to host-2 at the array level
> (zoning or LUN masking). The storage team needs to add host-2's WWN
> (FC) or IQN (iSCSI) to the LUN's access list. Once host-2 can see the
> LUN, you can mount the VMFS datastore on it from vSphere Client and
> both hosts will share it.

## ELI5

The big computer can use storage from far away over special cables. The
storage looks like one big disk, and a special way of organizing it
called VMFS lets many computers use it at the same time without
fighting.

## ELI10

VMFS is a special file system that lets multiple ESXi hosts share the
same chunk of block storage (a LUN) without corrupting it. The hosts
talk to the storage over Fibre Channel or iSCSI, format the LUN with
VMFS, and then anyone can read and write VM files on it. Multipathing
gives each LUN multiple physical paths from the host to the array, so a
cable or controller failure doesn't take the storage down.

## Real world — what you see live

vSphere Client → host → Configure → Storage Adapters. You see <code>vmhba0</code>
(FC), <code>vmhba1</code> (FC), <code>vmhba32</code> (iSCSI software adapter).
Each shows discovered devices. Right-click a device → Configure
Multipathing → Round Robin. Now Datastores → New Datastore → VMFS →
choose the device → name it <code>ds-vmfs-prod</code> → format → mount.
The new datastore appears on every host that can see the LUN.

---

# Subtopic 3 of 6: NFS datastores

## Concept

**NFS (Network File System)** is the file-storage option. Instead of the
host getting a raw block LUN and putting a file system on it, the host
mounts a file system that the **NAS appliance** owns. vSphere's job is
much smaller: just talk NFS, store files.

NFS in vSphere supports two versions:

- **NFS v3** — older, classic. UDP/TCP, less efficient for parallel I/O,
  no Kerberos auth (or limited).
- **NFS v4.1** — newer, supports Kerberos, multiple I/O paths, better
  locking. Recommended for new deployments where the array supports it.

What you configure on the host:

- Server address (the NAS's IP or hostname).
- Share path (e.g., <code>/vol/vsphere-prod</code>).
- Datastore name (vSphere's local label).
- Read-only? (rare for VM datastores; useful for ISO repositories).
- NFS version.
- For NFS 4.1, Kerberos credentials if used.

**Why pick NFS over VMFS**:

- Simpler to provision. The NAS team does the file-system work; you just
  mount.
- File-level visibility on the array side (admins can browse VM files
  directly without going through vSphere).
- Often easier to grow (NAS volumes are flexible; LUNs are sized at
  creation).
- IP storage uses the same Ethernet / vmkernel infrastructure as the
  rest.

**Why pick VMFS over NFS**:

- Some shops prefer block for performance / latency on demanding
  workloads.
- VMFS supports certain features (RDM, MSCS shared disks) that NFS
  doesn't.
- Existing FC investment.

## Before / After

**Before**: Need new storage for a project. The block-storage process is
"ticket to storage team, wait two days, get a LUN, configure
multipathing, format VMFS." Slow.

**After**: NAS-team carves a new NFS share in five minutes. You add it
to vSphere as a datastore. Done.

## Analogy

NFS is renting storage space in a shared file room down the hall — no
concrete slab, just a door and a key, and the file room handles its
own filing system. You drop your boxes in; the file room owns where they
sit.

## Quick check

> **Question** — Your team is choosing between NFS and VMFS for a new
> VM datastore. Network is 10 GbE. NAS supports NFS 4.1. The
> application is a moderate-traffic web service. Which is fine, and what
> tilts the decision?
>
> **Answer** — Either is fine for a moderate-traffic web service. The
> tilt: if the team values operational simplicity (faster provisioning,
> easier to grow, file-level visibility on the NAS), pick NFS. If the
> team values FC-style latency and has existing block storage, pick
> VMFS. Neither is wrong; they're optimizing for different things.

## ELI5

NFS is like keeping your stuff in a shared room down the hall instead
of in a big warehouse. Easier to get to, but someone else owns the
room.

## ELI10

NFS is a way for the host to use storage that's actually owned by a NAS
appliance somewhere on the network. The host just mounts the NFS share
as a datastore and stores VM files in it. The NAS handles the file
system; vSphere doesn't have to. NFS is often easier to provision and
grow than VMFS, doesn't need FC hardware, and gives storage admins
file-level visibility into VM files. NFS 4.1 is the modern choice for
new deployments.

## Real world — what you see live

vSphere Client → Datastores → New Datastore → NFS → NFS 4.1. Server:
<code>nas-01.lab.local</code>. Folder: <code>/vol/vsphere-prod</code>.
Datastore name: <code>ds-nfs-prod</code>. Mount on hosts: select all
hosts in the cluster. Save. The datastore appears on every host
simultaneously.

---

# Subtopic 4 of 6: vSAN — hyperconverged storage from host disks

## Concept

**vSAN (Virtual SAN)** is VMware's software-defined storage. Instead of
relying on an external array, vSAN takes the local disks (SSDs, NVMe,
HDDs) on each host in a cluster and pools them into a single,
distributed datastore that all hosts in the cluster see.

This is **<span class="term">HCI<span class="tooltip">Hyperconverged Infrastructure — combining compute, storage, and (sometimes) networking into a single hardware platform managed as one. vSAN is VMware's HCI storage layer; it pools each host's local disks into a cluster-wide datastore.</span></span> (Hyperconverged Infrastructure)** in
vSphere terms: compute and storage live in the same boxes. No external
array, no separate storage admin team needed for storage provisioning,
no LUN dance.

How it works at a high level:

- Each host contributes one or more **disk groups**: one cache disk
  (fast SSD/NVMe) plus one or more capacity disks. The cache absorbs
  writes; capacity stores data.
- vSAN distributes each VM's data across the cluster as **objects**,
  with copies (mirroring) or parity (erasure coding) for resilience.
- A **storage policy** assigned to each VM decides how many copies, what
  performance tier, and what other characteristics the VM's data has.
- All hosts see one logical datastore: <code>vsanDatastore</code>.

vSAN's headline benefits:

- **No external array** — rack two or more hosts, you have shared
  storage.
- **Scale by adding hosts** — both compute and storage grow with the
  cluster.
- **Per-VM policies** — each VM can have a different protection /
  performance profile, set at the policy level.
- **Tight vSphere integration** — vSAN is built into ESXi; vCenter
  manages it.

vSAN versions / configurations:

- **OSA (Original Storage Architecture)** — disk groups with cache +
  capacity disks. The classic.
- **ESA (Express Storage Architecture)** — newer, all-NVMe, no cache
  tier. Uses a single tier with TLC NVMe. Higher performance, simpler
  hardware story. Rolling out as the future.
- **vSAN ReadyNodes** — pre-validated server configurations from
  hardware vendors that VMware certifies for vSAN.

vSAN requires its own VLAN (vmkernel adapter with vSAN service enabled
on each host) and benefits from 25/100 GbE networking.

## Before / After

**Before**: Buying a new vSphere environment means two separate vendor
selections: servers AND a SAN/NAS array. Two procurements, two skill
sets, two integration projects.

**After**: Buy vSAN ReadyNodes. Power them up, install ESXi, deploy
vCenter, enable vSAN. The cluster is its own storage. One vendor, one
skill set, one project.

## Analogy

vSAN is the building making its own storage room out of every closet in
every apartment, then sharing that combined space among everyone. No
external warehouse needed. The building manager sets policies — "every
important file has two copies in different apartments" — and the system
honors it.

## Quick check

> **Question** — A 4-host vSAN cluster. A VM has a storage policy of
> "FTT=1 mirroring" (Failures To Tolerate = 1, mirrored). One host
> dies. What happens to the VM's data?
>
> **Answer** — Nothing visible to the VM. FTT=1 mirroring means every
> piece of the VM's data has two copies on two different hosts. When one
> host dies, the other copy is still available. vSAN may rebuild the
> missing copy on a third host in the background. The VM keeps running.
> If a *second* host died simultaneously and took out the second copy
> too, then we'd have a problem.

## ELI5

Instead of having a separate storage building, every apartment shares
its own storage closet with the whole building. Together they make one
big storage area that everyone can use.

## ELI10

vSAN takes the local disks on every ESXi host in a cluster and pools
them into one big shared datastore. No external SAN or NAS needed.
Each host contributes a disk group (a cache disk and one or more
capacity disks). Each VM's data is spread across the cluster as
objects, with copies or parity for resilience. A storage policy on
each VM decides how many copies, what performance tier, etc. vSAN is
the foundation of VMware's hyperconverged infrastructure (HCI)
strategy: compute and storage in the same boxes, scaling together.

## Real world — what you see live

vSphere Client → Cluster → Configure → vSAN → Services → Configure.
Wizard: enable vSAN, choose deployment type (single site / stretched /
two-node), select disks per host (cache + capacity, or ESA all-NVMe).
Configure vSAN VLAN on the vmkernel adapters. Apply. The cluster
shows a new <code>vsanDatastore</code> visible on all hosts. Total
capacity = sum of capacity disks across hosts. Each VM you deploy
to it gets a storage policy that decides protection and performance.

---

# Subtopic 5 of 6: vVols — VM-centric storage on smart arrays

## Concept

**vVols (Virtual Volumes)** is a storage model that pushes
VM-awareness *into the array*. Instead of one VMFS datastore holding
many VMs as files (where the array sees only a big LUN), each VM's
storage is a separate object the array tracks individually.

The pieces:

- **Storage Container** — the array-side replacement for a LUN. A pool
  of capacity exposed for vVols use.
- **VASA Provider** — the array's API endpoint that vCenter talks to.
  VASA = vSphere APIs for Storage Awareness.
- **Protocol Endpoint** — the data-path connection between hosts and the
  array (FC, iSCSI, NFS — vendor's choice).
- **vVol** — a single storage object representing one piece of one VM
  (one config, one disk, one swap, one snapshot). Created and managed
  by the array.

What this changes:

- The array can apply per-VM policies natively (replication, snapshots,
  encryption, tiering).
- Snapshots and clones are array-native, much faster than VMFS-era
  VM-level snapshots.
- Storage admins see real VM names and individual disks, not opaque
  VMFS files.
- Operations like "give that VM tier-1 latency" become a policy change,
  not a VM migration.

The trade-off: vVols requires a vVol-capable array with a working VASA
provider. Not every array supports it; setup is more involved than
classic VMFS or NFS.

vVols is the natural pair for **<span class="term">SPBM<span class="tooltip">Storage Policy-Based Management — vSphere mechanism for assigning storage policies (capabilities like performance, redundancy, encryption) to VMs. The underlying storage layer is responsible for honoring the policy.</span></span>** (next subtopic) because the
array can natively honor any policy SPBM expresses.

## Before / After

**Before**: VMFS over a LUN. The storage array sees one giant file —
the VMFS volume — with no idea what VMs are in it. Per-VM policies
(replication, snapshots) are coarse: applied at the LUN level for every
VM in it.

**After**: vVols. Each VM is a set of storage objects on the array.
Per-VM array-native snapshots, replication, encryption — all addressed
at the VM granularity, with the array applying the policy.

## Analogy

vVols turn the warehouse into a smart locker system. Each VM gets its
own labelled locker, the warehouse itself tracks contents and
policies, and the building manager just asks "put this VM in a fast
locker" — the warehouse picks the locker.

## Quick check

> **Question** — Your array is vVol-capable but the team is using
> classic VMFS. Why might switching to vVols be worth the trouble?
>
> **Answer** — Per-VM array-native operations: snapshots, clones,
> replication, encryption all expressed at VM granularity instead of
> LUN granularity. Storage policies (SPBM) get honored natively by the
> array. Operationally: storage admins see real VM names and per-disk
> usage, not opaque VMFS files. The trouble: a working VASA provider
> setup and a more complex initial config.

## ELI5

Instead of one big shared storage room with everyone's stuff mixed
together, each VM gets its own labelled box that the storage system
knows about by name.

## ELI10

vVols is a way of doing storage where the array tracks each VM's
storage individually, instead of seeing one big VMFS volume. Each VM
becomes a set of storage objects (config, disks, swap, snapshots) that
the array manages directly. This unlocks per-VM features at the array
level: snapshots, replication, encryption all become VM-granular
instead of LUN-granular. It requires the array to support vVols and
a working VASA provider integration with vCenter, but it's the cleanest
pairing with storage policies.

## Real world — what you see live

vSphere Client → Storage → Storage Providers → Add. Configure VASA
provider URL, credentials. Then Datastores → New Datastore → vVol.
Pick the storage container the array exposes. Mount on cluster hosts.
The new vVol datastore behaves like any datastore in vSphere; under
the covers, every VM you create on it becomes individual vVol objects
on the array.

---

# Subtopic 6 of 6: SPBM + thin/thick provisioning

## Concept

**Storage Policy-Based Management (SPBM)** is vSphere's framework for
assigning storage policies to VMs. Instead of "put VM-X on
datastore-Y," you say "VM-X needs gold tier" and SPBM places it on a
datastore that can honor gold tier.

A storage policy is a list of capabilities the storage must provide:

- Number of failures to tolerate (FTT).
- Replication / mirroring vs erasure coding.
- IOPS limit (or reservation).
- Encryption.
- Tiering / pinning to specific media.
- Vendor-specific features the array exposes.

vSphere ships with built-in policies (vSAN Default, Host-local) and
lets you create custom ones. When you provision a VM you pick a policy;
vSphere finds a datastore that satisfies it (or shows a compliance
warning).

**Thin vs thick provisioning** is a related but separate decision: how
disk space is allocated when you create a virtual disk.

- **Thin provisioned** — the .vmdk only consumes physical space as the
  guest writes data. A 100 GB thin disk that holds 20 GB of data uses
  20 GB on the datastore. Great for over-provisioning; risky if you
  over-commit and run out.
- **Thick provisioned, lazy-zeroed** — full size reserved on creation,
  but blocks zeroed lazily on first write. Faster to create, slight
  perf hit on first writes.
- **Thick provisioned, eager-zeroed** — full size reserved AND zeroed
  on creation. Slowest to create, best subsequent write performance.
  Required for some features (Fault Tolerance, certain clusters).

For most workloads, thin provisioning + monitoring of datastore usage
is the right default. Eager-zeroed thick is for the few VMs that need
it.

## Before / After

**Before**: VM placement is "where is there room?" — manual. Some VMs
end up on slow datastores, some on fast, no consistent policy. Some
disks are thick-provisioned for no reason, eating capacity.

**After**: Three storage policies (Gold, Silver, Bronze) defined.
Every VM gets tagged at provisioning time. Thin provisioning is the
default; eager-zeroed thick is reserved for FT-protected VMs.
Compliance reports flag drift.

## Analogy

SPBM is the building's storage policy: "gold tier = mirrored + fast,"
"silver tier = single copy, slow." You stamp a tier on each VM and the
system honors it. Thin/thick provisioning is whether you reserve all
the floor space up front or grow into it.

## Quick check

> **Question** — You provision a 500 GB VMDK as thin. The VM uses 80
> GB. The datastore is 1 TB and has 20 other VMs on it. The total
> *configured* size of all VMs sums to 1.4 TB — over the datastore.
> What's wrong, what's right, and what should you watch?
>
> **Answer** — Nothing is broken yet; this is normal over-provisioning
> with thin. What's right: storage isn't wasted on data that doesn't
> exist, you're getting more out of the datastore. What to watch:
> total *used* space. If the VMs collectively grow toward 1 TB, you'll
> run out and VMs will pause / fail. Configure datastore alerts at 75%
> / 85% / 95% and have a plan to add capacity or move VMs off.

## ELI5

You can give each room a label like "fancy room" or "basic room," and
the building puts your stuff in a matching room automatically. Some
rooms have all the floor space booked up front, some only get used as
you put boxes in.

## ELI10

Storage Policy-Based Management lets you define storage capabilities
(mirrored, fast, encrypted, etc.) and assign them as policies to VMs.
The hypervisor finds a datastore that can honor the policy and places
the VM there. This separates "what storage qualities does this VM
need" from "which specific datastore does it sit on" — and makes the
storage layer responsible for honoring policy. Thin provisioning lets a
virtual disk consume only the space it actually uses; thick
provisioning reserves the full size up front (and optionally
pre-zeroes it for performance). Most workloads run thin + monitoring;
thick is for the few cases that need it.

## Real world — what you see live

vSphere Client → Policies and Profiles → VM Storage Policies → Create.
Name: <code>Gold</code>. Rules: vSAN > FTT=1 mirroring + IOPS
limit 0. Save. Repeat for Silver, Bronze. Now provision a VM →
Storage section → Storage Policy: Gold. vSphere lists eligible
datastores. Pick one. Choose thin or thick on the disk page (default
thin is fine). Create. The VM is placed and tagged with the policy;
compliance is monitored continuously.

---

## Lesson recap (cross-subtopic)

Six moves from "where do VMs live?" to a storage layer that's
performant, resilient, and policy-driven.

1. **Overview** — datastore is the unit; four types: VMFS, NFS, vSAN, vVols.
2. **VMFS** — VMware's clustered FS on shared block (FC, iSCSI). Multipathing matters.
3. **NFS** — file storage over IP; simpler to provision, NAS owns the FS.
4. **vSAN** — pool local disks across cluster; HCI; no external array.
5. **vVols** — VM-centric storage on smart arrays; per-VM array-native operations.
6. **SPBM + provisioning** — policy-driven placement; thin by default, thick when needed.

Storage is wired up. Lesson 12 deploys VMs onto it.
