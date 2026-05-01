# Lesson 10 — Configuring vSphere Networking

> Format: **per-subtopic** (six subtopics, each a mini-lesson). Shared
> diagram, animation, and preview-page hero treat the lesson as one journey.

---

## Lesson opener

You have hosts (lesson 8) and a vCenter (lesson 9). They are wired into your
physical network through whatever NICs the server has. Inside ESXi, all that
physical connectivity is exposed through **virtual networks** that VMs and
vCenter services plug into.

This lesson covers six moves to set up those virtual networks:

1. **Overview** of the networking primitives (vSwitch, port group, NIC, vmkernel).
2. **Standard vSwitch (vSS)** — per-host networking, configured on every host.
3. **Distributed vSwitch (vDS)** — cluster-wide networking, configured once.
4. **Port groups and VLAN tagging** — how VMs and services pick a network.
5. **NIC teaming, load balancing, and failover** — multiple physical NICs, one logical pipe.
6. **vmkernel adapters** — special-purpose interfaces for management, vMotion, vSAN, NFS, etc.

---

# Subtopic 1 of 6: vSphere networking overview

## Concept

vSphere networking has four primitives. Understand them and the rest of this
lesson is just configuring them in different shapes.

- **Physical NIC (uplink)**: a real network card on the host. Often called
  `vmnic0`, `vmnic1`, etc. Each is a wire to a physical switch.
- **Virtual switch (vSwitch)**: software inside ESXi that behaves like a
  layer-2 switch. It has uplinks (physical NICs) on one side and ports on
  the other. There are two kinds: Standard vSwitch (vSS) and Distributed
  vSwitch (vDS).
- **Port group**: a named collection of ports on a vSwitch with shared
  policy (VLAN, security, NIC teaming, traffic shaping). VMs plug into a
  port group, not directly into a vSwitch. Two kinds: VM port groups (for
  VMs) and vmkernel port groups (for ESXi's own services).
- **vmkernel adapter**: a virtual interface that ESXi itself uses (not a
  VM) for things like management, vMotion, vSAN, NFS, iSCSI. Lives on a
  vmkernel port group.

The shape: NIC → vSwitch (with uplinks) → port group → VM (or
vmkernel adapter).

This is the same model on every host. The question "vSS or vDS?" only
changes who configures the vSwitch (each host individually, or vCenter
once for the whole cluster).

## Before / After

**Before**: VMs are running on hosts but you're fuzzy on how their network
traffic gets out. You hear "port group" and "vSwitch" and "uplink" and
they all sound interchangeable.

**After**: You can sketch the path: VM → vNIC → port group → vSwitch →
uplink → physical switch. You know each primitive's job and where it
lives.

## Analogy

A vSwitch is the building's internal phone system. Port groups are the
named jacks on each desk: "Sales," "Engineering," "Finance." Uplinks are
the trunk cables to the city telephone exchange. VMs plug into jacks; the
trunk carries traffic to the rest of the world. vmkernel adapters are
the building's own service phones (security, fire alarm, deliveries) on
their own dedicated jacks.

## Quick check

> **Question** — A new VM is being created. Its NIC needs to live on the
> "Production-VLAN-100" network. Where does the VM actually attach?
>
> **Answer** — To the port group named "Production-VLAN-100" on the
> vSwitch. The port group carries the VLAN-100 policy. The VM doesn't
> attach directly to the vSwitch or to the physical NIC.

## ELI5

The big computer has fake network cables inside that look just like real
ones. They plug into fake switches that look just like real ones. The
fake switches connect to real network cards that go out to the real
network.

## ELI10

vSphere networking has four building blocks. A physical NIC is the actual
network card on the server. A vSwitch is software that behaves like a
network switch. A port group is a named bundle of ports on a vSwitch
where everything plugged in shares the same network policy (which VLAN,
which uplinks, which security rules). A vmkernel adapter is a virtual
network interface that ESXi itself uses (for management, vMotion, vSAN,
etc.) — not a VM. VMs plug into VM port groups; ESXi's own services plug
into vmkernel port groups; both kinds of port groups live on a vSwitch
that has physical NIC uplinks to the outside world.

## Real world — what you see live

Open vSphere Client → Host → Configure → Networking → Virtual switches.
You see `vSwitch0` with two uplinks (`vmnic0`, `vmnic1`) and several port
groups: "Management Network" (vmkernel), "VM Network" (default VM port
group), and a few others you've added. Each port group lists its VLAN
ID, its policy, and what's plugged into it. That single screen shows
the whole networking stack on the host.

---

# Subtopic 2 of 6: Standard vSwitch (vSS)

## Concept

A **Standard vSwitch (vSS)** is a vSwitch that lives entirely on one
host. It's the default and ships with every ESXi install. The host that
owns the vSS configures it; nothing about it is shared with other hosts.

This is the trade-off: vSS is simple and free (no extra licensing), but
if you have ten hosts in a cluster and want them to all see "Production
VLAN 100," you have to create a port group named "Production-VLAN-100"
with the same VLAN ID and same policy on every single host. Drift creeps
in — one host has VLAN 110 by typo, vMotion fails for VMs landing
there, you spend an hour finding it.

vSS is the right choice when:

- You're running the free vSphere edition and don't have access to vDS.
- The environment is small (a couple of hosts) and human consistency is
  manageable.
- You're configuring a host before it's joined to vCenter (you literally
  cannot use vDS on a standalone host).
- A handful of edge cases (DPU offload, certain NSX scenarios).

vSS limits you don't get to escape:

- No central config; every host is its own snowflake.
- No LACP (active-active uplink bundling).
- No NetFlow, port mirroring, traffic filtering.
- No private VLANs.
- No Network I/O Control (NIOC).

## Before / After

**Before**: 10 hosts, each with a vSS. New "DMZ-VLAN-200" needs to land
on every host. You SSH into each host (or click into each host's Config
tab), create the port group, set VLAN 200, set the policy. By host 6 you
mistype VLAN 220. VMs land on host 6 and lose connectivity.

**After**: A vDS (next subtopic). Create the port group once in vCenter;
it shows up on all 10 hosts identically. No drift.

## Analogy

A vSS is each apartment building running its own phone system, with its
own wiring closet. Adding a new line means walking to every building
and configuring it identically. Works for one building, painful for ten.

## Quick check

> **Question** — Your cluster has 8 hosts and uses vSS everywhere. You
> add a new VM port group on host-3. Will vMotion work for a VM on that
> port group to host-7?
>
> **Answer** — Only if you also create the *same-named* port group with
> the *same VLAN* on host-7. Otherwise vMotion fails because the
> destination host has no matching port group. This is exactly the
> consistency problem vDS solves.

## ELI5

Each apartment building has its own phone closet. To add a new phone
line that works in every building, you have to go to every building and
add it the same way. It's easy to mess up if you have many buildings.

## ELI10

A Standard vSwitch is a virtual switch that lives on a single ESXi host.
You configure it on each host independently. For VMs to be portable
across hosts (so vMotion works, so HA works), you need to set up the
same port groups with the same names and VLANs on every host. That's
manageable for two hosts and a nightmare for fifty. Standard vSwitches
are the default and free; their cluster-wide cousin (vDS) requires the
Enterprise Plus edition.

## Real world — what you see live

vSphere Client → host-1 → Configure → Networking → vSwitches. You see
`vSwitch0`. Click "Add Network." Choose "Virtual Machine Port Group for
a Standard Switch." Pick `vSwitch0`. Name it `Production-VLAN-100`. VLAN
ID: 100. Click Finish. Now repeat on host-2, host-3, ..., host-10.
Halfway through, your eyes glaze. Welcome to the case for vDS.

---

# Subtopic 3 of 6: Distributed vSwitch (vDS)

## Concept

A **Distributed vSwitch (vDS)** is a vSwitch whose configuration lives
in vCenter and is applied identically to every host that's joined to it.
You configure once; vCenter pushes the config to all member hosts. Drift
goes away.

The trick is that the vDS has two halves:

- **Control plane** — lives in vCenter. Holds the port groups, policies,
  and topology.
- **Data plane** — lives on each host. The hidden vSwitch on each host
  forwards packets locally; it just receives its config from vCenter.

This means hosts can keep forwarding traffic even when vCenter is down.
vDS doesn't put the data path through vCenter; it just puts the
*management* through vCenter.

What vDS gives you that vSS does not:

- **Centralized configuration** — port groups defined once, present
  everywhere.
- **LACP** — bundle multiple uplinks into one logical link with the
  physical switch.
- **NetFlow** — export flow records for network observability.
- **Port Mirroring** — mirror traffic to a sniffer for analysis.
- **Network I/O Control (NIOC)** — share allocations of host bandwidth
  between traffic types (VM, vMotion, vSAN, etc.).
- **Traffic filtering and marking** — DSCP, ACLs at the port group
  level.
- **Private VLANs**.
- **Per-port stats and policies**, not just per-port-group.

The cost: vDS requires the **Enterprise Plus** edition (or specific
bundles). Most production environments at any scale have it.

You usually run a vDS for VM and vMotion traffic and may keep a small
vSS for management on each host as a safety net (so you can still
reach the host if vCenter or the vDS gets sideways).

## Before / After

**Before**: 10 hosts × 8 port groups = 80 places to drift. Adding a new
network is an afternoon. Removing a misconfig is detective work.

**After**: A vDS holds all the port groups. New port group: one click in
vCenter, present on all 10 hosts atomically. Misconfig: one place to
fix. Audit: one place to read. Network admins love vDS.

## Analogy

A vDS is the building complex's shared phone system, configured once at
the central operations office. Adding a new line shows up in every
building automatically. Every building still has its own physical
wiring; the wiring just follows the central plan.

## Quick check

> **Question** — vCenter is down. Your hosts are on a vDS. Is VM network
> traffic still flowing?
>
> **Answer** — Yes. The data plane lives on each host; only the control
> plane (where you change config) is in vCenter. Existing VMs keep their
> connectivity. You just can't make changes — adding a port group, for
> instance — until vCenter is back.

## ELI5

The whole apartment complex's phone system is set up at one central
office. You change something there once, and every building gets the
new setting. If the central office goes home for the night, the phones
still work — you just can't change anything new.

## ELI10

A Distributed vSwitch (vDS) is a vSwitch defined in vCenter and shared
across many hosts. You configure port groups, policies, and uplinks
once at the cluster level; vCenter pushes the configuration to every
host identically. Each host still does its own packet forwarding, so
network traffic keeps flowing even if vCenter goes down. vDS unlocks
features that vSS can't do: LACP, NetFlow, port mirroring, NIOC,
traffic filtering, private VLANs. It requires the Enterprise Plus
edition.

## Real world — what you see live

vSphere Client → Networking inventory tab → Right-click datacenter →
Distributed Switch → New. Wizard: name `dvs-prod`, version 8.0,
uplinks per host (typically 2 or 4). Add member hosts (the wizard
walks them through). Create distributed port groups inside it
(`Prod-VLAN-100`, `vMotion-VLAN-30`, etc.). Each port group's policy is
set once and applied to every host. Migrate VM port groups from the old
vSS to the new vDS using the migration wizard. The old vSS can hang
around for management traffic as a fallback.

---

# Subtopic 4 of 6: Port groups and VLAN tagging

## Concept

A **port group** is a named bundle of ports on a vSwitch with shared
policy. There are two kinds:

- **VM port group** — VMs attach here. Carries VM data traffic.
- **vmkernel port group** — ESXi's own services (management, vMotion,
  vSAN, NFS) attach here, via a vmkernel adapter (subtopic 6).

Port groups carry policy: VLAN ID, NIC teaming, security (forged
transmits, MAC changes, promiscuous mode), traffic shaping, and on vDS,
a lot more.

**VLAN tagging** is how you isolate traffic over a single physical
trunk. Three modes:

- **EST (External Switch Tagging)** — the physical switch tags. The
  vSwitch sees untagged frames. VLAN ID on the port group is 0. Rare.
- **VST (Virtual Switch Tagging)** — the vSwitch tags. VLAN ID on the
  port group is the actual VLAN (1–4094). Most common. The physical
  switch's port is configured as a 802.1Q trunk carrying the VLANs ESXi
  uses.
- **VGT (Virtual Guest Tagging)** — the VM tags. VLAN ID on the port
  group is 4095 (all-VLAN trunk). The VM's OS handles VLAN tagging
  itself. Used for nested virtualization or specific appliances.

For VST (the normal case), the rule of thumb: every port group's VLAN
matches a VLAN trunked on the physical switch. Get this wrong and the
VM has connectivity to nothing.

**Naming** matters: especially on vSS, the port group name must match
across hosts for vMotion to find a destination. On vDS, the name is
defined once at the vDS level — drift is impossible by design.

## Before / After

**Before**: A new VM lands on host-3 in the "Production" port group and
can't talk to anything. You spend an hour. Eventually you find that
host-3's "Production" port group is on VLAN 110, while every other
host has it on VLAN 100. Typo from a year ago.

**After**: The port groups live on a vDS. There is one "Production"
port group with one VLAN ID. Every host gets the same. Typos can't
exist.

## Analogy

Port groups are the named jacks on each desk: "Sales" jack vs
"Engineering" jack. The VLAN ID on the jack tells the wiring which
traffic conduit to send your packets through. Same desk, multiple
jacks, different worlds.

## Quick check

> **Question** — A VM is on the "Production-VLAN-100" port group. The
> VM has connectivity to other VMs in the same port group on the same
> host but not to anything outside. What's the most likely cause?
>
> **Answer** — The physical switch port that the host's uplink connects
> to is not trunking VLAN 100. The vSwitch is tagging VLAN 100 (VST
> mode), but the physical switch is dropping it because its port isn't
> configured to allow VLAN 100. Fix: have the network team add VLAN 100
> to the trunk on that switch port.

## ELI5

Each desk has many jacks for different networks. The jack you plug
into decides what network you can talk on. If the wall socket isn't
wired up for that network, plugging into the jack does nothing.

## ELI10

A port group is a named group of virtual ports on a vSwitch with a
shared policy: which VLAN, which uplinks to use, what kind of security.
VMs attach to a VM port group; ESXi's own services attach to a vmkernel
port group. The VLAN ID on a port group, in the most common setup,
tells the vSwitch what VLAN tag to add to outgoing frames and what tag
incoming frames must have. The physical switch needs to be trunking
those VLANs on the port the host's uplink connects to. If the VLANs
don't match, the VM has no connectivity even though everything looks
right inside ESXi.

## Real world — what you see live

vSphere Client → Networking → Distributed Port Group → New. Name:
`Prod-VLAN-100`. Type: Static binding (default). VLAN type: VLAN. VLAN
ID: 100. Number of ports: 8 (auto-grows as needed). Policy: leave
defaults for now. Save. The new port group appears on every host. You
go to a VM, edit settings, change its NIC to `Prod-VLAN-100`, save. The
VM is now on that VLAN.

---

# Subtopic 5 of 6: NIC teaming, load balancing, and failover

## Concept

Every host should have at least two physical NICs assigned to a vSwitch.
This buys two things: more bandwidth (load balancing) and resilience
(failover). The set of physical NICs assigned to a vSwitch is called a
**team**.

Each port group inherits the team's policy (or overrides it). Five
common load-balancing modes:

- **Route based on originating virtual port (default)** — each VM port
  is pinned to an uplink based on its port number. Simple, works
  everywhere, no physical-switch config needed.
- **Route based on source MAC hash** — hash the VM's MAC to pick an
  uplink. Similar to port-based but stable across vMotion (because the
  MAC follows).
- **Route based on IP hash** — hash source/dest IP. Requires the
  physical switch to do EtherChannel (LAG without LACP).
- **Route based on physical NIC load** — vDS-only. Monitors actual
  utilization and rebalances. Most "set and forget" option for vDS.
- **Use explicit failover order** — only ever use the first listed
  active uplink; failover to standby if it dies. No load balancing.

**Active vs standby uplinks**: active uplinks are used; standby uplinks
sit idle and only take over if all active ones fail. Putting a NIC in
standby is useful for management traffic (you want predictable single
uplink) or to keep traffic types separate.

**Network failure detection**:

- **Link status only** — uplink is "down" only when its physical link
  drops. Misses the case where the cable is up but the upstream switch
  is unreachable.
- **Beacon probing** — ESXi sends little probe frames between team
  members; if probes don't arrive at the others, that uplink is
  considered down. Catches more failure modes; needs an even number of
  uplinks (3+) and only works for certain teaming modes.

**Notify switches** (yes/no): on failover, ESXi sends a RARP so the
upstream switch updates its MAC tables to point to the new uplink. Almost
always yes. Don't turn off unless you have a specific reason.

## Before / After

**Before**: Single uplink per host. NIC fails or cable gets unplugged →
host loses all VM network → vSphere HA kicks in 30 seconds later (if
configured) → VMs restart somewhere else. Disruptive.

**After**: Two-uplink team with active/active load balancing and beacon
probing. Same NIC failure: ESXi notices in milliseconds, fails over to
the surviving uplink, VMs barely notice. No HA event, no restart.

## Analogy

NIC teaming is having two phone lines into the building, both live, with
rules for how calls are split between them and how to fail over if one
line dies. The "load balancing" mode is the rule for splitting; the
"failure detection" is how you decide a line is really dead vs just
noisy.

## Quick check

> **Question** — Your team policy is "Route based on originating virtual
> port." A VM with vCPU 4 generates a sustained 5 Gbps of traffic. Both
> uplinks are 10 Gbps. Will the VM use both uplinks?
>
> **Answer** — No. Originating-port load balancing pins each VM to a
> single uplink. The VM uses one 10 Gbps NIC, not two. To split a
> single-VM flow, you'd need IP hash with EtherChannel on the switch
> (and even then it splits per-flow, not per-packet). Most people
> tolerate the per-VM cap because real workloads are dominated by many
> flows.

## ELI5

The big computer has more than one network cable. Some cables work,
some don't. We have rules for how to share traffic across them and what
to do if one breaks.

## ELI10

NIC teaming groups two or more physical NICs into one logical pipe.
You pick a load-balancing rule that decides which NIC handles which
traffic, and a failover rule that decides what happens if a NIC dies.
The default rule (originating virtual port) is simple and needs no
physical-switch config. Other rules give you more aggregate bandwidth
or more sophisticated failover, sometimes at the cost of physical-switch
configuration. You can mark some NICs as standby so they only take over
if active NICs fail. Beacon probing detects upstream failures that link
status alone misses.

## Real world — what you see live

vSphere Client → host → Configure → Virtual switches → vSwitch0 → Edit
→ Teaming and failover. Load balancing: Route based on physical NIC
load (because we're on a vDS). Network failure detection: Link status
only (default; beacon probing needs odd uplink count). Notify switches:
Yes. Failback: Yes. Active uplinks: vmnic0, vmnic1. Standby uplinks:
none. Save. The same policy now applies on every host that owns this
vDS.

---

# Subtopic 6 of 6: vmkernel adapters

## Concept

A **vmkernel adapter** is a virtual NIC that ESXi itself uses (not a VM).
It lives on a vmkernel port group on a vSwitch (vSS or vDS). Each
vmkernel adapter has an IP, a subnet, and a set of services it carries.

The services that ride on vmkernel adapters:

- **Management** — vSphere Client / API to ESXi. Almost always lives on
  its own (or shared with a generic management VLAN).
- **vMotion** — live VM migration traffic. Needs decent bandwidth and
  ideally its own VLAN.
- **Provisioning** — clone, snapshot, cold migration traffic.
- **Fault Tolerance (FT) logging** — heartbeat between FT primary and
  secondary VMs. Latency-sensitive.
- **vSAN** — vSAN data traffic between hosts. Requires its own dedicated
  VLAN.
- **NFS / iSCSI** — IP storage traffic. Often dedicated VLANs and NICs.
- **vSphere Replication** — replication between sites.
- **vSphere Backup NFC** — backup traffic.

You can stack multiple services on one vmkernel adapter (lab use), but
in production each big traffic type usually gets its own vmkernel on
its own subnet, ideally on its own physical NICs. Why:

- **Performance**: vMotion saturates a 10 GbE link; you don't want it
  competing with VM traffic on the same wire.
- **Security**: storage traffic shouldn't be reachable from VMs.
- **Troubleshooting**: separate networks make troubleshooting and
  packet capture sane.

A typical mid-size host has vmkernels for: management, vMotion, vSAN,
maybe iSCSI/NFS. Each on its own VLAN, often each with two NICs in a
team for resilience.

## Before / After

**Before**: One vmkernel called "Management" carries everything —
management, vMotion, NFS storage. vMotion of a big VM saturates the
link, ESXi's heartbeat with vCenter times out, the host bounces from
"connected" to "not responding." Alarms everywhere. Storage is briefly
unhappy.

**After**: Three vmkernels: Management on VLAN 10, vMotion on VLAN 30,
NFS on VLAN 50, each on its own subnet, each with its own dedicated
NIC pair. vMotion saturating its NIC doesn't touch management or
storage. Everyone sleeps.

## Analogy

vmkernel adapters are the building's own service phones — separate
lines for security, maintenance, deliveries, fire alarm. Mixing them
on one line works in a small building; in a tower, separate lines are
the only sane plan.

## Quick check

> **Question** — A new host has a vmkernel adapter on the management
> VLAN. You want to enable vMotion on the same vmkernel. Should you?
>
> **Answer** — In a lab, sure. In production, almost never. Add a
> *separate* vmkernel for vMotion on its own VLAN, ideally with its own
> NICs. vMotion can saturate a NIC and would compete with management
> traffic on the same vmkernel — risking management timeouts during
> migrations.

## ELI5

The big computer has its own special phone lines that aren't for the
people inside (the VMs). One line is for the building manager
(management), one for moving furniture between buildings (vMotion),
one for the storage closet (storage). Each gets its own line so they
don't interfere.

## ELI10

A vmkernel adapter is a virtual network interface on the host that ESXi
itself uses for its own services — management, vMotion, vSAN, NFS,
iSCSI, FT, replication. Each adapter has an IP and a set of enabled
services. In production, each big traffic type gets its own vmkernel on
its own VLAN, ideally with its own NIC pair. This keeps performance
predictable, security clean, and troubleshooting tractable. A lab can
get away with one vmkernel doing everything; a real environment cannot.

## Real world — what you see live

vSphere Client → host → Configure → Networking → VMkernel adapters →
Add Networking. Choose "VMkernel Network Adapter." Pick the target
vSwitch (or vDS port group). Network label: `vMotion`. VLAN: 30. IPv4:
static, `10.30.30.41/24`. Enabled services: vMotion. Save. Repeat for
vSAN, NFS, etc. Each becomes a separate adapter with its own IP,
subnet, and service.

---

## Lesson recap (cross-subtopic)

Six moves from "VMs are running and you don't know how their packets
get out" to "I can build, scale, and troubleshoot vSphere networks."

1. **Overview** — NIC → vSwitch → port group → VM (or vmkernel).
2. **vSS** — per-host, simple, drift-prone, free.
3. **vDS** — cluster-wide, no drift, Enterprise Plus.
4. **Port groups + VLAN tagging** — VST is most common; VLAN on the
   port group must match a VLAN trunked on the physical switch.
5. **Teaming, load balance, failover** — ≥2 NICs per vSwitch. Default
   "originating port" is fine for most. Beacon probing for paranoid
   detection.
6. **vmkernel adapters** — one per big service (management, vMotion,
   vSAN, NFS), each on its own VLAN/NICs.

Get those right and lesson 11 (storage) plugs into a network that's
ready for it.
