# Lesson 12 — Deploying Virtual Machines

> Format: **per-subtopic** (eight subtopics).
> The final lesson in vSphere Fundamentals.

---

## Lesson opener

Hosts (lesson 8) are healthy. vCenter (lesson 9) manages them. The
network (lesson 10) and storage (lesson 11) are wired up. Now we put
**virtual machines** on top — the things this whole stack exists to
serve.

Eight moves to deploy and manage VMs:

1. **VM overview** — what's inside a virtual machine.
2. **Create a new VM** — the wizard, end to end.
3. **Templates and clones** — reusable VM blueprints.
4. **Content libraries** — share templates and ISOs across vCenters.
5. **OVF / OVA** — packaged VM imports.
6. **Snapshots** — point-in-time states (and their costs).
7. **VMware Tools** — the in-guest agent.
8. **Day-2 lifecycle operations** — power, edit, hot-add, migrate, remove.

After this lesson the course is complete: from "what is virtualization"
all the way to "I can deploy production VMs on a vSphere environment I
built."

---

# Subtopic 1 of 8: VM overview — what's inside a virtual machine

## Concept

A virtual machine is a software container that looks, to the operating
system inside it, exactly like a physical computer. From the guest OS's
perspective: real CPU, real memory, real disks, real network cards,
real BIOS/UEFI. Underneath, the hypervisor is presenting all those as
virtual devices it backs with real hardware.

The virtual hardware that makes up a VM:

- **vCPU** — virtual CPUs. The hypervisor maps them to physical cores
  according to its scheduler.
- **vRAM** — virtual memory. Allocated up to the VM's configured size;
  may be reclaimed by ballooning, compression, swap if the host is
  pressured (lesson 5).
- **vDisk (vmdk)** — virtual disks. Stored as files on a datastore
  (lesson 11). One VM can have many.
- **vNIC** — virtual network interface. Attached to a port group
  (lesson 10).
- **vSCSI / vNVMe controllers** — virtual storage controllers the disks
  hang off.
- **CD/DVD drive** — usually mapped to an ISO on a datastore for
  install.
- **BIOS / EFI firmware** — boot firmware. Modern guests use EFI; some
  legacy guests need BIOS.
- **TPM (vTPM)** — virtual TPM for guests that need it (Windows 11,
  BitLocker).

Plus the **virtual hardware version** — a number (e.g., vmx-19, vmx-20)
that defines what virtual devices and features are available. Newer
versions unlock newer features but require newer ESXi to run.

The combination — hardware + virtual hardware version + guest OS — is
what makes a VM. Stored as a folder on a datastore: <code>vm-name.vmx</code>
(config), <code>vm-name.vmdk</code> (disks), and a few support files.

## Before / After

**Before**: You hear "vCPU," "vRAM," "vmdk," "vmx" and they're all
fuzzy.

**After**: You can list the virtual hardware on any VM and explain what
each piece does. You know where the VM's files live and what they're
named.

## Analogy

A VM is a fully-furnished apartment: walls (vRAM), floor (vDisk),
electricity (vCPU), windows (vNIC), and a key (BIOS/UEFI). The
hypervisor is the building infrastructure that makes them possible.

## Quick check

> **Question** — A VM has 4 vCPU configured. The host has 16 physical
> cores. Will the VM use all 16 cores?
>
> **Answer** — No. The VM's guest OS sees 4 CPUs and uses up to 4. The
> hypervisor schedules those 4 vCPUs onto 4 of the host's physical
> cores at a time. Even if the other 12 cores are idle, the VM doesn't
> get them — the vCPU count is a hard contract. To use more cores, the
> VM has to be reconfigured to have more vCPUs.

## ELI5

A virtual machine is a pretend computer. It thinks it has its own
keyboard, screen, brain, and storage — but really all of that is
software that the big computer makes up.

## ELI10

A VM is a software container that behaves like a physical computer to
the OS inside it. It has virtual versions of everything a real computer
has: virtual CPUs (vCPU), virtual memory (vRAM), virtual disks (vmdk),
virtual NICs, even virtual BIOS or EFI. The hypervisor backs all those
virtual things with real host hardware. The VM lives as a folder of
files on a datastore — its config file, its disk files, and a few
support files. The guest OS doesn't know it's virtual.

## Real world — what you see live

vSphere Client → VM → Edit Settings. You see CPU: 4, Memory: 8 GB, Hard
disk 1: 80 GB, Network adapter 1: connected to <code>Prod-VLAN-100</code>,
CD/DVD drive: empty, SCSI controller: VMware Paravirtual, Compatibility
(virtual HW version): ESXi 8.0 (vmx-20). The VM's files live at
<code>[ds-vsan-cluster1] vm-app1/</code>: <code>vm-app1.vmx</code>,
<code>vm-app1-flat.vmdk</code>, <code>vm-app1.nvram</code>,
<code>vmware.log</code>.

---

# Subtopic 2 of 8: Creating a new VM from scratch

## Concept

Create-VM walks through a wizard with a handful of important decisions.
You can do it from vSphere Client → right-click any inventory object →
New Virtual Machine.

The decisions, in order:

- **Creation type** — New VM (we focus here), or from template, OVF,
  clone, etc.
- **Name + location** — VM name, datacenter, folder.
- **Compute** — host or cluster (DRS picks for you in a cluster).
- **Storage** — datastore (or pick by storage policy → SPBM).
- **Compatibility** — virtual hardware version. Default to the latest
  supported by all hosts where the VM might run.
- **Guest OS** — vSphere uses this hint to pick sensible defaults
  (controller type, BIOS vs EFI, recommended hardware).
- **Hardware** — vCPU count, memory, disk size, network port group,
  CD/DVD (mount the install ISO).

The wizard creates the VM as **powered off**. To install an OS:

- Mount the install ISO on the CD/DVD drive (point to an ISO on a
  datastore or a content library).
- Power on the VM. The console attaches to the VM's display; you walk
  through the OS installer.
- After OS install, install **VMware Tools** (subtopic 7).
- Configure the OS (hostname, IP, services, applications).

A handful of sizing rules of thumb:

- Don't over-provision vCPUs — extra vCPUs add scheduling overhead and
  make CPU ready time worse, not better.
- Match memory to the workload; don't reserve unless the application
  needs it.
- Use the **VMware Paravirtual SCSI** controller for performance.
- Use the **VMXNET3** virtual NIC for performance.
- Enable EFI for new Linux/Windows where supported.

## Before / After

**Before**: A new application needs a VM. You click around vSphere
Client and end up with something half-configured because you didn't know
which decisions mattered.

**After**: You walk the wizard with intent: name in the right folder,
SPBM-driven storage, latest compatibility, correct guest OS, sane vCPU
and memory, paravirtual SCSI, VMXNET3 NIC, ISO mounted, ready to power
on.

## Analogy

Creating a new VM is like commissioning a new apartment: pick the
floor (host or cluster), the size (vCPU, vRAM, vDisk), the layout
(controller and NIC types), and the appliances (ISO to install). The
building manager carves it out for the tenant.

## Quick check

> **Question** — You're creating a VM for a Windows Server 2022
> workload. Which virtual NIC type and which SCSI controller do you
> pick by default?
>
> **Answer** — VMXNET3 NIC and VMware Paravirtual SCSI controller.
> Both are paravirtualized — the guest OS uses VMware-specific drivers
> (shipped with VMware Tools) for much better performance than emulated
> alternatives like E1000 NIC and LSI Logic SAS.

## ELI5

To make a new pretend computer, you tell the big computer how big to
make its brain, how much memory, how big a disk, and where to plug it
in. Then you put a setup CD in and turn it on.

## ELI10

Creating a new VM in vSphere is a wizard that asks: what to name it,
where it lives in the inventory, which host or cluster will run it,
which datastore stores its files, what virtual hardware version it
uses, what guest OS goes inside, and what virtual hardware (vCPU, vRAM,
disks, NICs, controllers) it has. After the wizard, the VM exists but
is powered off and empty. You attach an OS installer ISO, power on,
and walk through OS install. After install, install VMware Tools.

## Real world — what you see live

vSphere Client → cluster → New Virtual Machine. Pick "Create a new VM."
Name: <code>vm-app2</code>, folder: Production. Compute: cluster-A
(DRS picks host). Storage: select policy "Gold." Compatibility: ESXi
8.0 (vmx-20). Guest OS: Linux → Ubuntu 22.04 LTS (64-bit). Customize
hardware: 2 vCPU, 4 GB RAM, 60 GB thin disk on Paravirtual SCSI,
VMXNET3 NIC on <code>Prod-VLAN-100</code>, CD/DVD: ISO from content
library "ubuntu-22.04-server-amd64.iso," EFI firmware. Click Finish.
Power on. Install Ubuntu, install open-vm-tools, configure.

---

# Subtopic 3 of 8: Templates and clones

## Concept

A **template** is a special kind of VM you've decided is your gold
standard for some role. You build it once carefully (OS install, all
patches, security baseline, monitoring agents, configured to your
standards) and then convert it to a template.

You can't power on a template — that's the point. It's frozen so it
can't drift. From the template, you **clone** new VMs whenever you need
one.

Two cloning modes:

- **Full clone** — independent copy. The new VM has its own files and
  doesn't depend on the source. Slower to create, takes more space.
- **Linked clone** — copy that shares the source's base files and only
  stores its own changes. Fast to create, smaller. Used for VDI or
  short-lived test VMs. Production server VMs are usually full clones.

When you clone, you can run a **guest OS customization spec**: the
clone gets a unique hostname, MAC, SID (for Windows), IP per a recipe.
Without customization, you'd have N VMs with the same hostname and
MAC — bad day.

The flow:

1. Build a clean VM by hand (OS, patches, agents).
2. Convert to template.
3. Need a new VM? Right-click template → New VM from this Template →
   apply customization spec → done in 5 minutes vs 1 hour of OS install.

Templates pair beautifully with content libraries (next subtopic) so
you can share the same gold image across many vCenters.

## Before / After

**Before**: Every new VM is a fresh OS install. Every team makes
slightly different decisions about disk layout, agents, packages.
Drift across the fleet from day one.

**After**: One template per role (Ubuntu 22.04 baseline, Windows 2022
baseline, RHEL 9 web, etc.). Clones from those templates produce
identical VMs every time. Patches and agent updates: roll into the
template, redeploy.

## Analogy

A template is the gold-standard show apartment. A clone is a copy of
that apartment, ready for a tenant. You build the show apartment
carefully once, then stamp out copies.

## Quick check

> **Question** — You clone a Windows VM from a template 5 times. All 5
> end up with the same hostname and the same Active Directory SID.
> What did you forget?
>
> **Answer** — A guest OS customization spec. The customization spec
> generates a unique hostname, SID, IP per clone using a recipe you
> define. Without it, every clone starts as an exact bit-copy of the
> template — same identity, which causes AD chaos.

## ELI5

Build one perfect pretend computer once, then make copies of it
whenever you need new ones. Don't build each one from scratch every
time.

## ELI10

A template is a frozen VM that you use as a starting point for new
VMs. You build the template carefully once — install the OS, patch it,
add monitoring agents, set a baseline configuration — and then convert
it to a template (which you can't accidentally power on). When you
need a new VM, you clone from the template and apply a customization
spec that gives the clone a unique hostname, MAC address, and IP.
Templates eliminate drift and cut deployment time.

## Real world — what you see live

vSphere Client → vm-template-ubuntu-22 → Right-click → Convert to
Template. Now in the Templates view. Right-click → New VM from this
Template. Wizard: name, folder, compute, storage. Then Customization:
choose "Linux DHCP" customization spec (you defined it earlier with
hostname pattern, domain, time zone, root password). Click Finish.
vSphere clones the template files to a new VM, applies the
customization, powers on. 5 minutes later you have a freshly-named,
freshly-IP'd Ubuntu VM ready.

---

# Subtopic 4 of 8: Content libraries

## Concept

A **content library** is a vCenter-managed repository of OS templates,
ISOs, OVF appliances, scripts — anything you want consistent across
vCenters or across a long timeline.

Two kinds:

- **Local content library** — lives on this vCenter; you upload to it
  directly. Used for storing your team's templates and ISOs.
- **Subscribed content library** — pulls (subscribes) from another
  content library, by URL. The subscribed library can sync periodically
  or on-demand. Used for distributing one team's blueprints to many
  vCenters automatically.

A typical pattern:

- One central vCenter hosts the **published** library with your gold
  templates.
- Every other vCenter has a **subscribed** library pointing at it.
- When you publish a new template to the central library, every vCenter
  has it within hours (or immediately on demand).
- Provisioning from a content-library template uses the local copy on
  whichever vCenter is provisioning, so you don't pay cross-WAN
  transfer at deploy time.

Content libraries also hold ISOs (so the vSphere Client can mount them
directly without datastore browsing) and OVF appliances (so vendors'
appliance templates are findable in one place).

Storage for the library lives on a datastore you pick — often a
dedicated NFS share or a small VMFS volume.

## Before / After

**Before**: 5 vCenters, 5 different ways to hold templates. Some
upload manually; some don't. The "approved Ubuntu base" template is
different in each one. Drift.

**After**: One published content library on the central vCenter holds
the gold templates and ISOs. Every other vCenter subscribes. New
template version published once → propagated to all subscribers
automatically. No more drift.

## Analogy

A content library is the building chain's central catalog of approved
show apartments and decor. Every building copies from the same catalog
so they're consistent.

## Quick check

> **Question** — Your org has 5 datacenters, each with its own vCenter.
> You want every datacenter's deployments to come from the same gold
> Ubuntu template. What's the cleanest way?
>
> **Answer** — A published content library on one vCenter (the central
> one), with the gold template inside. The other 4 vCenters each have
> a subscribed content library pointing at it. Sync settings determine
> whether they pull on-demand or on a schedule. New templates published
> centrally appear at every site.

## ELI5

The big vSphere keeps a shared library of pretend-computer recipes.
Anyone can copy a recipe to make a pretend computer, and everyone uses
the same library so their recipes match.

## ELI10

A content library is a place vCenter manages where you store templates,
ISOs, and OVF appliances. You can have a local library (just on this
vCenter) or a subscribed library (mirrors another library's contents).
Subscribed libraries are how multi-site organizations keep templates in
sync — publish once at a central vCenter, every other vCenter picks it
up automatically. They also let you keep ISOs centrally instead of
scattering them across datastores.

## Real world — what you see live

vSphere Client → Content Libraries → Create. Type: Subscribed content
library. Subscription URL:
<code>https://vc-east.lab.local:443/cls/vcsp/lib/abc123/lib.json</code>.
Authentication: token. Storage: <code>ds-nfs-cl</code>. Sync: on
demand. Save. The library appears with all the templates and ISOs the
publisher exposes. Right-click a template → New VM from this Template
→ deploy locally.

---

# Subtopic 5 of 8: OVF and OVA packages

## Concept

**OVF (Open Virtualization Format)** is an industry-standard packaging
format for virtual machines. An OVF "package" is several files: an
<code>.ovf</code> XML descriptor, one or more <code>.vmdk</code> disk
files, an <code>.mf</code> manifest, optionally a certificate.

**OVA (Open Virtual Appliance)** is the same content packaged as a
single tar archive (a .ova file) for easier distribution.

When you import an OVF/OVA into vSphere, the wizard:

- Reads the descriptor and shows you what the package contains.
- Asks where to put it (datastore, folder, network mappings).
- Validates the manifest (integrity).
- Unpacks the disks onto the datastore and creates the VM.

OVF/OVA are how vendors ship turnkey appliances: VMware's own VCSA,
NSX Manager, vRealize Operations, but also third-party — backup
proxies, security appliances, network appliances, monitoring agents.
You download a .ova from the vendor, import in vSphere, configure,
done.

You can also **export** an existing VM to OVF/OVA from vSphere Client →
right-click → Export OVF Template. That's how you take a VM you built
once and ship it to another environment.

OVF/OVA includes some metadata vSphere honors: virtual hardware
version, guest OS, recommended sizing, network mappings, even
deployment-time prompts for things like IP / DNS / passwords.

## Before / After

**Before**: To deploy a vendor appliance you'd build a VM from scratch,
install their OS, install their software, walk through their
installer. Hours per appliance.

**After**: Vendor ships a .ova. You import. Wizard handles unpack,
config, networking. Five minutes later a working appliance.

## Analogy

OVF/OVA is the flat-pack version of a furnished apartment — boxes you
unpack into a unit. Vendors ship appliances this way so customers can
drop them into any vSphere.

## Quick check

> **Question** — You're given a single .ova file by a vendor. You want
> to deploy their appliance. What do you do?
>
> **Answer** — vSphere Client → File → Deploy OVF Template → upload
> the .ova. The wizard reads the package, lets you pick a name,
> destination folder, host or cluster, datastore, network mapping,
> and any deployment-time config the vendor exposed (often IP
> address, gateway, root password). After import, power on. The
> appliance is up.

## ELI5

OVF is a recipe file that says how to build a pretend computer. OVA is
the same recipe but bundled into one box for easier carrying. You unpack
either one in vSphere and you have a new pretend computer.

## ELI10

OVF (Open Virtualization Format) is a vendor-neutral way of packaging a
VM so it can be moved between hypervisors or shared between
organizations. OVA is the same thing as a single .ova file (a tar
archive) for easier distribution. vSphere can import OVF/OVA packages
to create new VMs and export existing VMs to OVF/OVA. Vendors ship
appliances this way: you download, import, configure, run.

## Real world — what you see live

Download <code>vendor-appliance-1.2.ova</code> from the vendor's portal.
vSphere Client → cluster → Right-click → Deploy OVF Template. Click
"Local file," select the .ova. Wizard validates → asks for VM name →
folder → compute target → storage → network mapping (the appliance has
two NICs; map each to the right port group) → customization (IP
address, gateway, root password). Click Finish. Watch a progress bar
unpack disks. Power on. Browse to the appliance's URL. Done.

---

# Subtopic 6 of 8: VM snapshots

## Concept

A **<span class="term">snapshot<span class="tooltip">A point-in-time saved state of a VM (memory + disks + settings). Used as a short-term safety net before risky changes. Has real ongoing performance and capacity costs — the longer you keep one and the more you have, the worse it gets.</span></span>** captures a VM's state at a point in time —
disk contents, memory contents (optional), settings — so you can roll
back to that point later if something goes wrong. Snapshots are
useful, but they have a real ongoing cost.

How they work mechanically:

- Taking a snapshot creates a delta file (<code>-000001.vmdk</code>
  alongside the base disk) and stops writing to the base.
- All subsequent writes go to the delta. Reads check the delta first,
  fall back to base.
- Each additional snapshot creates another delta. Read paths get
  longer as the chain grows.
- Reverting goes back to the snapshot point.
- Deleting a snapshot **commits** the delta into the base (consolidate)
  — this can take a long time for large deltas and can briefly stun
  the VM.

When snapshots are great:

- Right before a risky change (OS upgrade, app upgrade, config
  rollout). Take snapshot, do the change, validate, delete snapshot.

When snapshots are dangerous:

- Long-term. A 90-day-old snapshot has accumulated huge delta files;
  deleting it can be a multi-hour I/O storm. Performance degrades the
  whole time.
- As a backup mechanism. Snapshots are not backups. They depend on the
  base disks; a datastore failure loses both. Use a real backup tool.
- Many at once. Multiple snapshots multiply the read overhead.

Best practice: **delete snapshots within 24-72 hours**. vCenter alerts
on old snapshots; respect them.

## Before / After

**Before**: Snapshots taken before a change last for weeks. The
datastore fills up with delta files. VMs slow down. Trying to delete
old snapshots causes long stuns.

**After**: Snapshots are short-lived: take, do, validate, delete
within a day or two. Datastore alerts catch any that linger.
Performance stays steady.

## Analogy

A snapshot is a Polaroid of the apartment at a moment in time. Useful
for short-term safety (before changes). Stack too many Polaroids,
though, and the apartment slows down.

## Quick check

> **Question** — A senior engineer says "snapshots are our backup
> strategy." Why are they wrong?
>
> **Answer** — Because snapshots depend on the VM's base disks. If
> the datastore the VM lives on has a failure (lost LUN, vSAN cluster
> loss, NFS export gone), both the base and the snapshots are lost
> together. A real backup goes to a separate, independent storage
> system (SFTP target, a dedicated backup appliance, off-site). Plus
> snapshots cause performance and capacity problems if kept long-term.

## ELI5

A snapshot is a "save point" for a pretend computer so you can go back
if something breaks. It's not a backup — if the storage breaks, the
save point is gone too.

## ELI10

A VM snapshot saves the state of a VM at a moment in time so you can
roll back if a change breaks something. Mechanically, it freezes the
disk file and starts writing changes to a separate delta file. This is
great as a short-term safety net before a risky operation. It's bad as
a long-term strategy: the deltas grow, performance degrades, and
deleting old snapshots can cause long stuns. Snapshots are NOT
backups — if the underlying storage fails, both the base and the
snapshot are lost.

## Real world — what you see live

vSphere Client → VM → Snapshots → Take Snapshot. Name: "before-app-
upgrade-2026-04-30." Description: optional. Snapshot the memory: yes
(captures running state, slower) or no (just disk, faster). Click OK.
Do the upgrade. Test. Either: Delete (commit) the snapshot, or Revert
(go back). Don't leave it; it'll grow and bite you.

---

# Subtopic 7 of 8: VMware Tools

## Concept

**<span class="term">VMware Tools<span class="tooltip">A suite of drivers and a daemon installed inside the guest OS that lets the hypervisor and guest cooperate. Provides paravirtualized device drivers (NIC, SCSI), graceful shutdown/reboot signals, time sync, screen-resolution awareness, file-quiesce for snapshots, and more.</span></span>** is a suite of drivers and an in-guest
daemon that make the guest OS cooperate efficiently with ESXi. Every
production VM should have it installed.

What VMware Tools provides:

- **Paravirtualized device drivers** — VMXNET3 NIC, Paravirtual SCSI,
  better video. Without Tools, the guest falls back to slower emulated
  devices.
- **Graceful shutdown / reboot** — vSphere Client's "Shut Down Guest
  OS" signals the in-guest daemon to do an orderly shutdown. Without
  Tools, that button just hard-powers-off.
- **Time sync** — keep the guest's clock in sync with the host.
- **Heartbeat** — vSphere knows the guest is alive (used by HA's VM
  Monitoring).
- **Quiesce for snapshots** — Tools tells the guest to flush
  filesystem/database buffers before a snapshot, so the snapshot is
  consistent (otherwise it's a crash-consistent snapshot of in-flight
  state).
- **Mouse, screen resolution** — passthroughs for the console.
- **File copy / drag-and-drop** between guest and Client (limited).

For Linux guests, the modern preference is **open-vm-tools**, an
open-source implementation distributed via the Linux distro's package
manager. It's the same VMware-supported codebase, just packaged the
distro-friendly way. Install it (<code>apt install open-vm-tools</code>,
<code>dnf install open-vm-tools</code>) and forget about it.

For Windows, install VMware Tools from the .iso vSphere can mount on
the VM. Modern packages auto-update.

vSphere Client shows Tools status per VM: not installed, current,
out-of-date, running, etc. Stay current.

## Before / After

**Before**: A VM has Tools missing. The "Shut Down Guest" button
hard-powers-off. Time drifts. Snapshots are crash-consistent. The
emulated NIC tops out at lower throughput than VMXNET3 would.

**After**: Tools installed and current. Shutdown is graceful. Time
syncs. Snapshots quiesce. VMXNET3 hits line rate. Heartbeat tells
vSphere the guest is healthy.

## Analogy

VMware Tools is the building's smart-home concierge installed in the
apartment. It lets the building manager (hypervisor) talk to the
tenant (guest OS) — for graceful shutdown, time sync, mouse, the right
drivers.

## Quick check

> **Question** — You take a snapshot of a busy database VM with no
> memory snapshot, and the VM has VMware Tools running. What does
> Tools do for the snapshot?
>
> **Answer** — It quiesces the filesystem (and, on Windows, it asks
> VSS-aware applications like SQL Server to flush) before the snapshot
> is taken. Result: an application-consistent point-in-time on disk.
> Without Tools, you'd get a crash-consistent snapshot — the snapshot
> would be like a power-loss recovery at restore time.

## ELI5

VMware Tools is a helper program inside the pretend computer that lets
the big computer talk to it nicely — for things like turning it off,
keeping its clock right, and using better fake hardware.

## ELI10

VMware Tools is a set of drivers and a daemon installed inside the
guest OS that make the guest cooperate efficiently with the
hypervisor. It provides paravirtualized device drivers (the fast
versions), graceful shutdown signals, time sync, file-quiesce for
clean snapshots, mouse/screen integration, and a heartbeat the
hypervisor reads. Every production VM should have it. Linux uses
open-vm-tools (from the distro's package manager); Windows installs it
from the ISO vSphere can mount.

## Real world — what you see live

Linux (Ubuntu): <code>sudo apt install -y open-vm-tools</code>. Done.
Service is running, status is "Tools current." Windows: vSphere Client
→ VM → Install VMware Tools. The host mounts the Tools ISO on the VM's
CD/DVD. RDP into the VM, run the installer, reboot. Status flips to
"Running, current."

---

# Subtopic 8 of 8: Day-2 lifecycle operations

## Concept

Day-2 operations are everything you do to a VM after it's running.
vSphere Client gives you a long menu; the important ones:

**Power operations:**

- **Power On / Power Off** — the obvious. "Power Off" is a hard pull
  of the plug.
- **Shut Down Guest OS** — graceful shutdown via VMware Tools.
- **Restart Guest OS** — graceful reboot via Tools.
- **Reset** — hard reset (the equivalent of pressing the physical
  reset button).
- **Suspend** — pauses the VM and writes its memory to disk. Resume
  picks up where it left off.

**Edit Settings:**

- Resize vCPU, vRAM, vDisk.
- Add/remove devices: NICs, disks, controllers, USB, serial.
- Change port group (move VM between networks).
- Change boot firmware (BIOS↔EFI is rare and risky).
- Change virtual hardware version (one-way upgrade).

**Hot operations** (without powering off, if guest supports):

- **Hot-add CPU** — add vCPUs while running. Guest must support hot-
  plug CPU.
- **Hot-add memory** — add vRAM while running. Guest must support
  hot-plug memory.
- **Hot-add disk** — add a new vDisk while running.
- **Hot-add NIC** — add a new vNIC while running.
- Hot-extend an existing disk (grow it; guest still has to extend the
  partition / file system).

**Migrations** (covered briefly in lesson 9 vCenter context):

- **vMotion** — move running VM compute between hosts.
- **Storage vMotion** — move VM files to a different datastore while
  running.
- **vMotion + Storage vMotion** combined — move both at once
  (cross-cluster, cross-datacenter).

**Cleanup:**

- **Remove from inventory** — vCenter forgets the VM but the files
  stay on the datastore.
- **Delete from disk** — vCenter forgets AND files are deleted. Be
  sure.

A good operational discipline: take a snapshot before risky Edit
Settings changes; remove the snapshot afterwards. Use Edit Settings
sparingly to grow resources; use it carefully to shrink (some guests
hate having vCPUs removed).

## Before / After

**Before**: Operations on running VMs are scary. Power-off-to-edit is
the only thing the team feels safe doing. Long maintenance windows for
small changes.

**After**: Hot-add for growth. vMotion and Storage vMotion for
relocations. Edit Settings is routine. Maintenance windows are short
and rare; most ops are non-disruptive.

## Analogy

Day-2 ops are the move-in / move-out / renovate / move-down-the-hall
operations once the tenant is in the apartment. The building manager
does them; the tenant rarely notices most.

## Quick check

> **Question** — A VM is running short on memory. The guest OS
> supports memory hot-plug. You want to add 4 GB without shutting it
> down. What do you do?
>
> **Answer** — vSphere Client → VM → Edit Settings → Memory → change
> from 8 GB to 12 GB → Save. Inside the guest, the new memory shows up
> immediately (Linux) or after a brief moment (Windows). No reboot.
> Note: hot-add memory must be enabled on the VM (it's a checkbox in
> Edit Settings) before this works on the guest's first boot.

## ELI5

Once the pretend computer is running, you can change things about it
without turning it off — make it bigger, give it a new disk, move it
to a different room.

## ELI10

Day-2 operations are everything you do to a VM after it's been
created and is running. The big buckets are: power operations
(graceful and hard), edit settings (resize, add/remove devices),
hot operations (do it without rebooting), migrations (vMotion across
hosts, Storage vMotion across datastores), and cleanup (remove from
inventory, delete from disk). Modern vSphere lets most growth
operations happen hot, with no downtime.

## Real world — what you see live

vSphere Client → vm-app1 → Edit Settings. Memory: 8 GB → 12 GB. Save.
Guest sees new memory immediately. Same VM → Storage vMotion to
<code>ds-vsan-cluster1</code> from <code>ds-vmfs-old</code>. Watch
progress bar; VM stays up. Same VM → Migrate → vMotion to host-7. VM
moves; ping continues with one missed packet. Routine.

---

## Lesson recap (cross-subtopic)

Eight moves from "I have a vSphere environment" to "I can run VMs on
it confidently."

1. **VM overview** — vCPU, vRAM, vDisk, vNIC, virtual hardware version.
2. **Create a VM** — wizard in vSphere Client; VMXNET3 NIC, Paravirtual SCSI, EFI.
3. **Templates and clones** — gold-standard VMs you stamp out.
4. **Content libraries** — share templates and ISOs across vCenters.
5. **OVF / OVA** — packaged VM imports (vendor appliances).
6. **Snapshots** — short-term safety net; not backups; delete promptly.
7. **VMware Tools** — every VM. Drivers + graceful shutdown + quiesce.
8. **Day-2 ops** — power, edit, hot-add, vMotion, Storage vMotion.

---

## Course completion

That's vSphere Fundamentals. Twelve lessons. From "what is
virtualization?" to a working understanding of how to design, deploy,
and operate a vSphere environment end to end:

- Lessons 1-4: virtualization itself, its benefits, vSphere components,
  and the history that got us here.
- Lessons 5-7: vSphere's place in the SDDC, hypervisor types, and the
  cloud picture.
- Lessons 8-9: standing up the platform — ESXi hosts and vCenter.
- Lessons 10-11: networking and storage that the platform plugs into.
- Lesson 12 (this one): putting VMs on the platform.

You can now read a vSphere environment, install one, configure one,
and run workloads on it. The next step in any career path is hands-on
practice — and the more advanced VMware tracks (vSAN administration,
NSX, automation, lifecycle, multi-cloud).
