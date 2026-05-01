# Lesson 09 — Deploying and Configuring vCenter Server

> Format: **per-subtopic** (eight subtopics, each a mini-lesson). Shared
> diagram, animation, and preview-page hero treat the lesson as one journey.

---

## Lesson opener

You have one or more healthy ESXi hosts (lesson 8). On their own, each host
is an island — its own UI, its own users, its own logs. **vCenter Server**
is the central management plane that ties many hosts into one cluster of
clusters and gives you the features you actually came for: vMotion, HA, DRS,
templates, content libraries, fleet-wide policy.

This lesson stands up vCenter from zero in eight moves:

1. **What vCenter is** and why you need it.
2. **Prerequisites** — DNS, NTP, network, sizing.
3. **Stage 1** — deploy the appliance OVA.
4. **Stage 2** — first-time setup.
5. **SSO and identity sources** — wire up corporate Active Directory.
6. **Roles, privileges, permissions** — the RBAC model.
7. **Inventory hierarchy** + **backup** — organize and protect.
8. **vCenter HA** — keep the management plane up.

---

# Subtopic 1 of 8: What vCenter Server is and why you need it

## Concept

**vCenter Server** is the central control plane for a vSphere environment.
It runs as a single virtual appliance — the **vCenter Server Appliance
(VCSA)** — on top of an ESXi host. From vCenter, one team can manage
hundreds of hosts and thousands of VMs through a single web UI (the
vSphere Client) and one API.

VCSA is a Photon Linux VM that VMware ships pre-built. Inside it: Postgres
database, vCenter services, the vSphere Client web app, the SSO service,
and the lifecycle/update services. You don't install vCenter on Windows
anymore (VMware retired that path in vSphere 7) — the appliance is the
only path now.

What vCenter unlocks that you can't do from a standalone host:

- **vMotion**: move running VMs between hosts with no downtime.
- **DRS**: load-balance VMs across a cluster automatically.
- **vSphere HA**: restart VMs on a different host if one fails.
- **Templates and content libraries**: reusable VM blueprints, shared
  across hosts.
- **Distributed switches**: one network config across the cluster.
- **Fleet-wide policy**: tag, baseline, patch, monitor at scale.

Without vCenter, you can run VMs on individual hosts via the Host Client
— but you can't migrate them, you can't fail them over, and you can't
manage more than a tiny lab without losing your mind.

## Before / After

**Before**: You manage hosts one at a time via the Host Client. To move a
VM from host A to host B, you shut it down, copy its files, and re-register
it on B. There's no central audit log, no central permissions, no live
migration.

**After**: vCenter is up. You log in to the vSphere Client and see all
your hosts in one place. To move a VM, you right-click and pick vMotion.
A central audit log shows who did what, where. Permissions are managed
once and apply across the fleet.

## Analogy

If a host is one apartment building, vCenter is the city's central
operations office that watches every building. From there, one team can
move tenants between buildings (vMotion), automatically balance occupancy
(DRS), and rebuild a flooded building's tenants in another building (HA).
Without the central office, every building has its own manager, with no
coordination — which is fine if you have one building, painful if you
have ten.

## Quick check

> **Question** — A team runs 12 ESXi hosts but never deployed vCenter,
> managing each host through the Host Client. They want to "move a running
> VM from host-3 to host-7 without downtime." Can they do it?
>
> **Answer** — No. Live migration (vMotion) is a vCenter feature; the Host
> Client alone can't do it. They can shut down the VM, copy its files,
> register it on host-7, and start it — but that's not vMotion, and it
> involves downtime. They need vCenter.

## ELI5

A single computer brain (one ESXi host) can do its own job. But once you
have many of them, you want one boss who watches them all and can move
work between them. vCenter is that boss.

## ELI10

vCenter Server is software that runs as a virtual machine on top of an
ESXi host. Its job is to manage many other ESXi hosts together: see them
all in one screen, move VMs between them while running, restart VMs
automatically if a host dies, balance load across hosts, and keep one
audit trail of who did what. You install it as a pre-built appliance
(VCSA) — basically, a VM that already has all the vCenter software
installed and ready to go. Every production vSphere environment runs
vCenter; managing more than a couple of hosts without it is impractical.

## Real world — what you see live

Same admin, same Tuesday, two parallel universes:

- **Without vCenter**: opens 12 browser tabs, one Host Client per host.
  Wants to know if any host has a degraded fan: clicks through 12
  hardware-health pages. Wants to shift a VM off host-3 because of a
  RAM issue: shuts the VM down, downloads the .vmx, uploads it to host-7,
  re-registers, powers on. Fifteen minutes of downtime per VM.
- **With vCenter**: one tab. Hardware view shows all 12 hosts; the bad
  fan is highlighted in red. Right-click a VM → Migrate → pick host-7 →
  it lives-moves in 60 seconds with no downtime.

---

# Subtopic 2 of 8: vCenter prerequisites — DNS, NTP, network, sizing

## Concept

You can't just download the VCSA OVA and click Install. The deployer asks
for things that, if wrong, leave you with a half-configured appliance that
you'll end up redeploying. Get four buckets right *before* you launch the
installer.

**DNS.** The vCenter FQDN (e.g., `vc-01.lab.local`) must resolve forward
**and** reverse. If the PTR record is missing, certificate generation in
Stage 2 produces a vCenter that works but trips AD/SSO/integration in
weird ways later. Add A and PTR records before you start.

**NTP.** The target ESXi host (where vCenter will run) and the appliance
itself must be in time-sync. Clock drift between vCenter and its hosts is
the source of about 80% of "weird vCenter" problems. Configure NTP on
the host (lesson 8, subtopic 5) and point vCenter at the same time
sources during Stage 2.

**Network.** Pick the management port group the appliance will sit on,
its IP, gateway, and subnet mask. Pre-allocate the IP in IPAM so it
doesn't get re-issued. If your management network is on a non-default
VLAN, make sure that VLAN is on the host's vSwitch already.

**Sizing.** Pick a deployment size that matches the *future* fleet, not
just today's:

- **Tiny** — up to 10 hosts, 100 VMs (lab / small).
- **Small** — up to 100 hosts, 1,000 VMs.
- **Medium** — up to 400 hosts, 4,000 VMs.
- **Large** — up to 1,000 hosts, 10,000 VMs.
- **X-Large** — up to 2,000 hosts, 35,000 VMs.

You can scale the appliance up later, but it's a maintenance window;
sizing right the first time is cheaper.

## Before / After

**Before**: You download the OVA on a Friday afternoon, launch the
installer, and the first screen asks for an FQDN that doesn't resolve.
You patch DNS, restart the installer, and the next screen asks for an
NTP server you forgot to verify. You give up and go home.

**After**: You walk through a 5-item checklist: A record, PTR record,
NTP server reachable, IP free in IPAM, size chosen. Open the installer,
the first screen accepts the FQDN cleanly, every subsequent screen has
its inputs ready. Twenty minutes from launch to a running appliance.

## Analogy

vCenter prereqs are like the building permit checklist before you pour
foundation. You can pour without the permits, but the city won't let you
turn on power, and you'll be tearing things up to fix it later.

## Quick check

> **Question** — The installer's first screen rejects your FQDN with an
> error like "name does not resolve." You open a terminal and `ping
> vc-01.lab.local` works. What's the most likely cause?
>
> **Answer** — Missing reverse DNS (PTR record) for `10.20.30.50` →
> `vc-01.lab.local`. The installer checks both forward AND reverse and
> won't let you continue without both. Add the PTR record, retry.

## ELI5

Before you build the new big building (vCenter), the city needs to know
what its address is, what time it is, and where it sits. If any of those
are wrong, the building will be confused for years.

## ELI10

vCenter is picky about its environment. Before you install it, four things
have to be right: (1) DNS — the name you'll give vCenter must resolve to
its IP and the IP must resolve back to the name. (2) NTP — the host
running vCenter must have the correct time. (3) Network — pick the IP
and port group up front. (4) Sizing — choose Tiny / Small / Medium / Large
/ X-Large based on how many hosts and VMs you'll eventually manage.
Skipping any of these doesn't usually fail the install loudly — it
deploys a vCenter that misbehaves later.

## Real world — what you see live

You launch the VCSA installer. Stage 1 wants an FQDN: you type
`vc-01.lab.local`. Installer validates: forward DNS ✓, reverse DNS ✓.
Next screen wants an NTP server: you type `time.lab.local`. Installer
pings it: ✓. Next screen wants a deployment size: you pick Small (you
have 30 hosts today, plan for 80). Next screen wants the target host:
`esx-01.lab.local`. Installer connects, lists datastores. You pick
the storage policy. Click Next, Next, Deploy. Stage 1 starts.

---

# Subtopic 3 of 8: Stage 1 — Deploy the appliance OVA

## Concept

The vCenter installer is a two-stage GUI. **Stage 1** is "deploy the OVA
to a target host." It does not start vCenter; it just lands the appliance
VM on a host and wires its basic settings.

Where the installer runs: on **your laptop** (or jump server), not on the
host. You launch the installer from the VCSA ISO, it talks to the target
ESXi host directly via the host's management API, and it pushes the OVA
across.

What you choose in Stage 1:

- **Target host** (ESXi) and **root credentials** for that host.
- **Appliance VM name** (often the same as the FQDN: `vc-01.lab.local`).
- **Root password** for the appliance itself (different from the host's
  root password — store it in the same vault).
- **Deployment size** (Tiny / Small / Medium / Large / X-Large) and
  **storage size** (Default / Large / X-Large).
- **Datastore** for the appliance VM.
- **Network port group**, **IP**, **gateway**, **subnet**, **DNS**, and
  **FQDN**.

Stage 1 takes 5–10 minutes. It writes a Photon-Linux VM with all vCenter
binaries pre-installed but not yet started. When Stage 1 finishes, the
installer offers a button: **Continue to Stage 2**.

## Before / After

**Before**: A cleanly installed and configured ESXi host with no
appliance running on it.

**After**: The host shows a new VM named `vc-01.lab.local`, powered on,
running Photon Linux. The vCenter services are *not* started yet — you
can't log in to vSphere Client. You proceed to Stage 2.

## Analogy

Stage 1 is moving a pre-fab office trailer onto the building site. It's
already wired and plumbed; you just choose where it sits and which
utilities to plug into. The lights aren't on yet — that's Stage 2.

## Quick check

> **Question** — Stage 1 finishes successfully. You browse to
> `https://vc-01.lab.local/` to log in. The page returns 503. Are you
> in trouble?
>
> **Answer** — No. Stage 1 only deploys the appliance; it doesn't start
> vCenter services. The 503 is expected until Stage 2 runs and starts the
> services. Click "Continue to Stage 2" in the installer (or relaunch
> the installer in resume mode) and you'll get a working login after
> Stage 2 completes.

## ELI5

Stage 1 puts the new big building on the lot. The doors are closed and
the lights are off — that part comes next.

## ELI10

The vCenter installer has two phases. Phase 1 (Stage 1) deploys the
appliance — a pre-built VM containing everything vCenter needs — onto
the ESXi host you point it at. It's a software equivalent of "drop a
ready-made box on the floor." When Stage 1 finishes, the appliance VM
exists and is powered on, but the vCenter services inside it haven't
started. Phase 2 (Stage 2) is what turns it into a real vCenter.

## Real world — what you see live

You double-click the VCSA installer on your laptop. It opens a four-icon
launcher: Install, Upgrade, Migrate, Restore. You click Install. Stage 1
starts. Click through introduction. Accept license. Pick "vCenter
Server." Type the target host (`esx-01.lab.local`), root password,
accept the cert. Pick the appliance VM name (`vc-01.lab.local`), root
password. Choose deployment size (Small). Pick the datastore (`ds-vsan`).
Configure network: port group `mgmt`, IP `10.20.30.50/24`, gateway
`10.20.30.1`, DNS `10.20.30.10`, FQDN `vc-01.lab.local`. Click Next →
Finish. Watch a progress bar for ~7 minutes. "Stage 1 deployment
completed successfully." Click "Continue."

---

# Subtopic 4 of 8: Stage 2 — First-time setup

## Concept

**Stage 2** is the moment vCenter becomes a real, usable thing. It
configures NTP, the SSO domain, and starts the services inside the
appliance.

What you choose in Stage 2:

- **NTP servers** for the appliance (e.g., `time.lab.local`).
- **SSH access** to the appliance (off is fine; you almost never SSH in).
- **SSO domain name** — defaults to `vsphere.local`. Keep it unless you
  have a specific reason to change (changing later is hard).
- **SSO administrator password** for `administrator@vsphere.local` —
  this is the SSO god-mode account; store it in the vault.
- **CEIP** opt-in (telemetry) — your call.

Then it runs. A long progress bar. "Setting up SSO domain ..." "Starting
services ..." "Verifying ..." It can take 10–15 minutes. Don't close the
window.

When Stage 2 completes, the installer shows a Done page with a link to
`https://vc-01.lab.local/ui/`. That's vSphere Client. Click it, log in
as `administrator@vsphere.local` with the SSO password. You're in
vCenter.

If Stage 2 hangs or fails, the appliance VM is still there from Stage 1
— you can re-run the installer in resume mode. You don't have to start
over.

## Before / After

**Before**: Appliance VM running but vCenter services not started; web
UI returns 503; SSO domain doesn't exist yet.

**After**: vCenter is alive. vSphere Client loads at
`https://vc-01.lab.local/ui/`. You can log in as
`administrator@vsphere.local`. The inventory tree is empty; that's the
next subtopic.

## Analogy

Stage 2 is the city inspector turning on the breakers, plugging in the
phone, and stamping the certificate of occupancy. The trailer was
on-site after Stage 1; Stage 2 is when it becomes a working office.

## Quick check

> **Question** — Stage 2 hangs at "Starting services" for 25 minutes.
> Your laptop's screen is black; you might have lost the installer
> window. What do you do?
>
> **Answer** — Don't reboot the appliance. Reopen the VCSA installer and
> choose the resume option (or browse to
> `https://vc-01.lab.local:5480/`, log in as the appliance root user,
> and check the install status from the VAMI). The OVA from Stage 1 is
> persisted on disk; Stage 2 can pick up where it left off.

## ELI5

Stage 2 turns on the lights, plugs in the phone, and opens the front
door of the new building.

## ELI10

After Stage 1 puts the appliance VM on the host, Stage 2 actually
configures it: NTP, SSO domain (the security domain that authenticates
users), the password for the master admin account, and starting the
vCenter services. Stage 2 takes longer than Stage 1 because services
need to start in order and verify each other. When it finishes, you
have a vCenter you can log in to.

## Real world — what you see live

You click "Continue to Stage 2." Type NTP servers. Decide SSH (off).
Confirm SSO domain `vsphere.local`. Set the
`administrator@vsphere.local` password (32 chars, vault). Click
Finish. Progress bar: "Setting up..." for 12 minutes. "vSphere Client
URL: https://vc-01.lab.local/ui/". Click the link. Login screen.
Username: `administrator@vsphere.local`. Password: from vault. Click
Login. vSphere Client loads. Empty inventory tree on the left. You
made it.

---

# Subtopic 5 of 8: vCenter SSO and identity sources

## Concept

**vCenter Single Sign-On (SSO)** is the identity layer of vCenter. When
you log in to vSphere Client, you don't authenticate to vCenter directly
— you authenticate to SSO, which issues a token that vCenter trusts.
Same SSO can issue tokens for ESXi hosts (in lockdown mode, exception
users live alongside this), for vCenter HA, for solution users (vSAN
Health, vROps).

Out of the box, SSO has one identity source: the **SSO domain itself**
(`vsphere.local`), with one user (`administrator@vsphere.local`). That's
fine for the first 30 minutes; long-term, you add your corporate
identity provider as an **identity source**.

Common identity sources:

- **Active Directory (Integrated Windows Authentication)** — most
  common; requires the appliance to be joined to your AD domain.
- **AD over LDAP** — connect over LDAP/LDAPS; doesn't require domain
  join.
- **OpenLDAP** — non-Microsoft directories.
- **AD FS** (federation) — if you have a federation provider already.

Once an identity source is added, you grant **vCenter permissions** (next
subtopic) to AD users and groups, and they log in with their corporate
identity (e.g., `alice@corp.local`).

Why you don't make `administrator@vsphere.local` the daily account:
it's the SSO god-mode account — it can change SSO itself, including
removing all your other admins. Treat it like ESXi root: long random
password, in the vault, glass-break only.

## Before / After

**Before**: Only `administrator@vsphere.local` can log in. Six admins
share that password. Audit log shows that SSO god-mode account doing
everything.

**After**: AD is added as an identity source. AD groups are mapped to
vCenter roles. Each admin logs in with their own AD identity; the audit
log shows their name. `administrator@vsphere.local` lives in the vault.

## Analogy

SSO is the building's badge-reader system. Identity sources are the HR
systems it pulls from — corporate AD, contractor LDAP. Without it,
every door has its own keypad and its own list of people. With it, one
badge gets you everywhere your role allows, and HR is the source of
truth for who exists.

## Quick check

> **Question** — A new admin needs to log in to vCenter. Their corporate
> identity exists in AD. What's the cleanest way to give them access?
>
> **Answer** — (1) Make sure AD is an identity source on vCenter SSO.
> (2) Add their AD account (or, better, an AD group they're in) to a
> vCenter permission with the appropriate role. They log in to vSphere
> Client with `their-name@corp.local`, get authenticated by AD via SSO,
> and see exactly the inventory their role allows. Don't create a local
> SSO account for them.

## ELI5

The big building has one master key for emergencies, but everyone else
gets in with their work badge from their company. The badge reader
checks with the company's HR system to make sure the badge is real and
the person still works there.

## ELI10

vCenter doesn't manage users itself — it delegates that to a service
called Single Sign-On (SSO). SSO can use one or more "identity sources"
— places where user accounts actually live. The default identity source
is a built-in one called `vsphere.local` with one admin user. In
production, you add Active Directory as an identity source so people
can log in with their normal corporate username and password. SSO
issues a token after authentication; vCenter trusts that token. This
keeps vCenter out of the password business and lets HR-driven changes
(joiner, leaver, role change) propagate naturally.

## Real world — what you see live

vCenter is up. You log in as `administrator@vsphere.local`. Navigate to
**Administration → Single Sign On → Configuration → Identity Sources**.
Click **Add Identity Source**. Choose "Active Directory over LDAP."
Type AD domain `corp.local`, base DN, service account credentials. Save.
Now under **Users and Groups**, you can search for AD users. Add
`Domain Admins` (or, better, `vSphere-Admins`) to a vCenter permission
in the next subtopic. Log out. Log back in as `alice@corp.local`. You're
in.

---

# Subtopic 6 of 8: Roles, privileges, and permissions (RBAC)

## Concept

vCenter's RBAC has three building blocks. Mix them up and you'll get
permissions wrong:

- **Privilege** — an atomic action. e.g., `Virtual Machine.Power.Power On`,
  `Datastore.Browse Datastore`. There are hundreds. You don't manage
  privileges directly day-to-day.
- **Role** — a named bundle of privileges. e.g., the predefined
  "Administrator" role contains every privilege; "Read-Only" contains
  view privileges only. You can create custom roles by selecting
  privileges.
- **Permission** — a (user-or-group, role, inventory-object) triple.
  "Alice has the VM Power User role on the Production folder." That's
  one permission.

**Inheritance** matters. Permissions can be set as **propagating** (apply
to the object and all children below it) or **non-propagating** (apply
only to the object itself). Propagation is on by default and is what
makes "give Alice admin on the entire datacenter" work.

**Predefined roles** worth knowing:

- **Administrator** — full control. Reserve for senior staff.
- **Read-Only** — view but cannot change. Junior engineers, monitoring.
- **Virtual Machine User** — limited day-to-day VM operations (power
  on/off, console).
- **Virtual Machine Power User** — full VM lifecycle plus snapshot.
- **No Access** — denies access at this object (overrides inherited
  Allow above).
- **No Cryptography Administrator** — Administrator minus encryption
  privileges.

**Global permissions** apply *across the entire vCenter inventory* and
also apply to objects that don't appear in the inventory (e.g., tag
categories). Use sparingly; usually for the small admin team. Object
permissions apply to a specific datacenter, folder, cluster, host, or VM
— and to its children if propagating.

## Before / After

**Before**: Everyone with vCenter access has Administrator. The audit
log shows lots of activity but no one has thought about who can do what.
A junior engineer accidentally deletes a production VM "to clean up."

**After**: A small set of senior engineers has Administrator at the
global level. The Production folder has VM Power User assigned to a
"Production-Ops" AD group. The Lab folder has VM Power User assigned to
a "Dev-Engineers" AD group. Junior engineers have Read-Only. The
accidental delete becomes structurally impossible.

## Analogy

Roles are job titles ("night shift janitor"). Privileges are the
individual things they can do ("open janitor closet", "mop floor").
Permissions assign a job title to a person at a specific place ("Alice
is night shift janitor, on Floor 3 only"). Propagation is whether the
assignment also covers Floor 4 above it (no — Alice's permission is on
Floor 3 and below, not above).

## Quick check

> **Question** — You assign Alice the "Read-Only" role on the
> "Production" folder, propagating. Inside Production, there's a VM
> "vm-payments" where you also assign Alice the "Virtual Machine Power
> User" role, non-propagating. What can Alice do to vm-payments?
>
> **Answer** — Power user actions. Object-level permissions override
> inherited permissions on the same object. The Read-Only inherited
> from Production is overridden by the Virtual Machine Power User
> assignment on vm-payments specifically. Outside of vm-payments,
> Alice still only has Read-Only.

## ELI5

vCenter has badges (roles), abilities each badge gives you (privileges),
and where each badge works (permissions on a folder, room, or just one
chair). You can have a special badge for one chair that overrides what
your normal badge says.

## ELI10

Three concepts: a **privilege** is one tiny thing you can do (turn a VM
on, look at a datastore). A **role** is a named set of privileges (e.g.,
"Read-Only" = many view privileges; "Administrator" = every privilege).
A **permission** is the assignment that says "this user/group has this
role on this part of the inventory." Permissions can propagate down to
child objects or stop at the object you set them on. Permissions on a
child object override inherited permissions for that specific object.

## Real world — what you see live

vCenter inventory has a folder called "Production" with 40 VMs. You
right-click Production → Add Permission. Pick the AD group `corp\Prod
-Ops`. Pick the role `Virtual Machine Power User`. Check "Propagate to
children." Save. Now anyone in `Prod-Ops` can power-cycle, snapshot, and
open consoles for any VM under Production. They cannot create or delete
VMs (those privileges aren't in Power User). Mission accomplished:
operational access without destructive ability.

---

# Subtopic 7 of 8: Inventory hierarchy and vCenter backup

## Concept

vCenter organizes everything into an **inventory hierarchy**. The
top-level objects you create:

- **Datacenter** — a logical container, usually one per physical
  datacenter or per business region.
- **Folder** — for grouping (VM folders, host folders) for permissions
  and tags.
- **Cluster** — a group of hosts that share resources and behave as one
  for HA, DRS, vMotion.
- **Host** — an ESXi host added to vCenter (it leaves the standalone
  Host Client world and is now managed by vCenter).
- **VM** — virtual machines on hosts, inside folders.

Networks (port groups, distributed switches) and datastores (VMFS, NFS,
vSAN) appear under their datacenter as separate views.

You can rearrange the hierarchy later, but plan it up front; permissions
and tags follow it.

**vCenter backup** protects the appliance itself. vCenter has built-in
**file-based backup** that ships its database and configuration to an
external target (FTPS, SFTP, HTTPS, NFS, or SMB). Configure it from the
appliance VAMI (`https://vc-01.lab.local:5480/`) under Backup. Schedule
it nightly. Keep at least 7 backups, ideally 30.

A backed-up vCenter can be restored to a fresh appliance in ~30 minutes
— way faster than rebuilding inventory, permissions, certs, and AD
binding from scratch.

**Take a fresh backup before any major operation**: upgrade, certificate
rotation, SSO change. If something goes wrong, the rollback is
"redeploy + restore," not "argue with logs for two days."

## Before / After

**Before**: Inventory is a flat list of 40 hosts, each with random
folders. Permissions are scattered. There is no vCenter backup;
"the VMs are backed up" is the only answer to the disaster question.

**After**: Three datacenters by region. Each datacenter has folders for
Prod, Dev, Sandbox. Hosts are organized into clusters by datacenter.
File-based backup runs nightly to an SFTP target. Last 30 nightly
backups are retained. A test restore was performed in the lab last
quarter and worked.

## Analogy

Inventory is the building directory: every floor (datacenter), wing
(folder), conference room (cluster), desk (host), and chair (VM) is
named and addressable. Backup is the photocopy of the directory you
keep off-site, so a fire doesn't take the directory with it.

## Quick check

> **Question** — Your vCenter appliance has just experienced a
> catastrophic disk failure. Your VMs are running fine on their hosts
> (vCenter going down doesn't take VMs down). What's your best path
> back to a working vCenter?
>
> **Answer** — Deploy a fresh VCSA OVA (Stage 1), then in Stage 2
> choose "Restore" instead of "Install" and point at your most recent
> file-based backup. The restored vCenter comes back with all
> inventory, permissions, certs, AD binding, and configuration — at
> the time of the last backup. Total time: ~30–45 minutes. The hosts
> rejoin automatically.

## ELI5

The big building has rooms organized into floors and wings, with names.
The directory tells you what's where. The photocopy of the directory
lives somewhere safe so if the building burns down, you still know what
was there.

## ELI10

vCenter organizes hosts and VMs into a tree: datacenters at the top,
then folders, then clusters of hosts, then VMs inside hosts. This tree
is what permissions attach to. vCenter itself is a single VM that holds
all this tree state plus configuration. Lose the appliance and you lose
everything *about* the inventory (the VMs themselves are still on hosts,
but vCenter doesn't know about them). File-based backup ships the
appliance's state to an external target nightly so you can rebuild
quickly if the appliance dies.

## Real world — what you see live

In vSphere Client → vCenter → Configure → Backup. Click "Configure" or
"Edit." Backup location: `sftp://backup.lab.local/vcsa-backups`.
Username, password. Schedule: daily at 02:00. Retention: keep last 30.
Encrypted backups: yes (set a passphrase, store in vault). Click Save.
Run "Backup Now" to verify the target is reachable. Watch a small log
roll. Done. Now you sleep better.

---

# Subtopic 8 of 8: vCenter High Availability (intro)

## Concept

**vCenter HA** is a vCenter-specific high-availability feature: it
protects the vCenter appliance itself. Don't confuse it with **vSphere
HA** (which protects guest VMs by restarting them on other hosts after
a host failure) — vSphere HA does nothing for vCenter itself.

vCenter HA works by running three nodes:

- **Active** — the live vCenter the world talks to.
- **Passive** — a clone of Active that stays in sync via replication.
- **Witness** — a small node whose only job is to break ties when
  Active and Passive disagree about which is alive.

If Active fails (host failure, OS issue, network partition), Passive
sees the failure (Witness confirms), promotes itself to Active, and
takes over the same FQDN and IP. Failover takes a few minutes.

Constraints to know:

- Three nodes, three different hosts, ideally on different power and
  network paths.
- All three are full appliance VMs — vCenter HA isn't free in resource
  terms.
- vCenter HA is configured *after* vCenter is up (a wizard from vSphere
  Client).
- You can disable, redeploy, and reconfigure it without losing data.

When you skip vCenter HA: small environments where a 30-minute
restore-from-backup is acceptable. When you enable it: large
environments where ops blindness during a vCenter outage is expensive
or unacceptable.

## Before / After

**Before**: One vCenter VM. If its host fails, vSphere HA may restart
it on another host (~5–10 minutes), but the host failure itself can
also take down vCenter HA's own machinery. Worst case: 30+ minutes
restoring from backup.

**After**: Three vCenter HA nodes spread across three hosts. Active
fails at 02:14; Passive promotes at 02:17; clients don't notice except
for a brief connection blip. The team's pager doesn't even fire.

## Analogy

vCenter HA is the building having a second control room with a hot
spare manager and a tie-breaker witness in a different building. If the
main control room goes down, the spare takes over within minutes; the
witness ensures both don't accidentally claim to be primary.

## Quick check

> **Question** — Your vSphere environment has vSphere HA enabled on
> every cluster. Someone says "we're protected against vCenter going
> down — vSphere HA will restart it." Are they right?
>
> **Answer** — Partially. vSphere HA *will* restart the vCenter VM on
> another host if its host dies — that's worth something. But during
> the restart window (5–10 minutes), vCenter is unreachable. For full
> protection against a vCenter outage, you want vCenter HA (active /
> passive / witness), which fails over in 1–3 minutes and doesn't
> depend on vSphere HA's restart cycle.

## ELI5

There's a backup boss watching the main boss. If the main boss falls
asleep, the backup takes over right away. A third person watches both
to make sure only one is calling the shots at a time.

## ELI10

vCenter is a single VM. If it dies, you can't manage vSphere until you
restore from backup — which can take 30+ minutes. vCenter HA fixes that
by running three nodes: an Active (the live one), a Passive (an
identical standby kept in sync), and a Witness (a small node whose only
job is to confirm whether Active really died, so Passive doesn't
incorrectly take over). Failover happens in minutes with the Active
keeping its IP and DNS name. It's a more expensive setup (three nodes
instead of one), so small environments often skip it and rely on
backup-and-restore instead.

## Real world — what you see live

In vSphere Client → vCenter → Configure → vCenter HA. Click "Set Up
vCenter HA." Wizard asks: management network, HA network, three target
hosts (one each for Active, Passive, Witness). It clones the Active
appliance to make Passive and Witness, configures replication, and
brings them online. Total wizard time: ~15 minutes. Now the
vCenter HA panel shows three green nodes. You schedule a planned
maintenance on the Active host's hardware: Passive takes over in two
minutes, you do the maintenance, Active comes back, and you fail back
on your schedule.

---

## Lesson recap (cross-subtopic)

One appliance. Eight phases of stand-up:

1. Understand what vCenter is and why you need it (vMotion, HA, fleet
   management).
2. Get the prereqs right (DNS, NTP, network, sizing).
3. Stage 1: deploy the appliance OVA.
4. Stage 2: setup; vCenter becomes alive.
5. Wire up SSO with your real identity source (Active Directory).
6. Build the RBAC model (roles, permissions, propagation).
7. Build the inventory hierarchy and configure file-based backup.
8. Optionally, deploy vCenter HA for management-plane resilience.

Get those eight right and the management plane is healthy. Lesson 10
moves to the network layer the hosts and VMs sit on.
