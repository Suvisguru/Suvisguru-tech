# Lesson 08 — Installing and Configuring ESXi

> Format: **per-subtopic** (six subtopics, each a mini-lesson). The shared
> diagram, animation, and preview-page hero treat the lesson as one journey;
> the prose, flashcards, and quiz treat it as six.

---

## Lesson opener — what we'll do, in one breath

You have a piece of physical (or rented) server hardware. By the end of this
lesson it will be a running, joinable, secure ESXi host. We get there in six
moves, in this order:

1. **Install** the hypervisor on the box.
2. Set up **accounts** so the right people can manage it.
3. Reach the host through **DCUI and the Host Client** to do initial config.
4. Manage host **services** (which run, which don't).
5. Configure **NTP, DNS, and routing** so the host has the correct time, can
   resolve names, and can talk to the right networks.
6. Tighten the host with **lockdown mode** so only sanctioned paths reach it.

Each subtopic below is structured the same way: concept → before/after →
analogy → quick check → ELI5 → ELI10 → real-world → flashcards (subset) →
quiz (subset).

---

# Subtopic 1 of 6: Installing the ESXi host

## Concept

ESXi is a **bare-metal hypervisor** — it installs directly on server hardware,
without any host operating system underneath it. There is no Windows or Linux
in the way; the hypervisor *is* the OS for that box, and everything else runs
as a virtual machine on top.

"Installing ESXi" means writing the hypervisor onto a target boot device on
the server (a USB stick, an SD card, a small M.2 SSD, or a SAN boot LUN), then
configuring the absolute minimum the hypervisor needs to be reachable: a
management IP, a hostname, a root password.

You can do this four ways:

- **Interactive ISO** — boot the installer from a USB stick or virtual CD via
  iLO/iDRAC/IPMI, answer the prompts. This is what most people learn on.
- **Scripted (kickstart)** — same installer, but a `ks.cfg` file answers every
  prompt automatically. Repeatable, used in larger fleets.
- **Auto Deploy (PXE)** — the host boots from the network and pulls its image
  from a vCenter Auto Deploy server. The host can be stateless (image lives
  on the network) or stateful (cached locally). Used at scale.
- **Vendor OEM image** — Dell, HPE, Cisco, etc. ship pre-customized ESXi ISOs
  that bundle the right drivers and firmware tools for their hardware.
  Recommended on supported servers.

Two non-negotiable inputs go into every install:

- The hardware must be on the **VMware Hardware Compatibility List (HCL)**.
  An unsupported NIC or storage controller may install fine and then fail in
  weird ways under load.
- A **root password** that meets complexity. Save it somewhere safe — the
  installer will not let you continue without it, and there is no easy
  reset path on a host you cannot reach.

## Before / After

**Before**: A bare server in a rack with a fresh BIOS/UEFI POST screen. You
can ping the iLO, but the box itself has no operating system. Nothing can
run on it yet.

**After**: ESXi is on the boot device. The host shows the yellow DCUI on the
console, you can browse to `https://<host-ip>` and reach the Host Client, and
the box is ready to be joined to vCenter (lesson 9).

## Analogy

Installing ESXi is like fitting a building's central management system before
the first tenants move in. You decide where the brain sits (boot device),
hand it the master key (root password), and tell it which front door to
answer (which NIC carries management traffic). Until that's done, the
building is a shell — power and walls, no service.

## Quick check

> **Question** — A teammate says: "I installed ESXi on top of Linux and now
> the VMs run inside the ESXi VM." What's wrong with this picture?
>
> **Answer** — ESXi is bare-metal. It doesn't install on top of an OS; it
> *is* the OS. What that teammate actually built is a Type-2 setup (probably
> ESXi nested inside VMware Workstation on Linux). Useful for a lab, but
> not how production ESXi runs.

## ELI5

A regular computer needs Windows or macOS to do anything. ESXi is a special
kind of computer brain that doesn't need any of that — you put ESXi straight
on the computer and now the computer can pretend to be many smaller computers
at the same time.

## ELI10

A normal server has an operating system (Windows Server, Linux) and runs apps
on top of that OS. ESXi replaces the operating system entirely with a
hypervisor — a tiny, purpose-built OS whose only job is to slice the server's
CPU, memory, network, and storage among virtual machines.

Installing ESXi is mostly: download the ISO, boot the server from it, pick a
disk to install onto, set a root password, and confirm the management network.
Ten minutes later you have a running hypervisor that you can reach from a
browser. Where the install gets interesting is everything *around* it: which
disk you choose, which NIC the install picks for management, whether the
server is on the HCL, and whether you used a vendor OEM image so all your
hardware is supported. Get those four right and the rest of vSphere builds on
solid ground.

## Real world — what you see live

You connect to the server's iLO/iDRAC, mount the ESXi ISO as a virtual CD,
and reboot. The installer is mostly black and yellow text. It detects your
disks, asks for the install target, asks for keyboard layout, asks for a
root password, and shows a confirmation screen. You hit F11 and watch a
progress bar. Reboot. The yellow DCUI appears: hostname, management IP,
ESXi build number. From your laptop you browse to `https://<that-ip>`,
log in as `root`, and you're in the Host Client.

---

# Subtopic 2 of 6: ESXi user account best practices

## Concept

Every ESXi host ships with one local account: `root`. It has total power and
no audit trail of *who* used it. That's fine for the first ten minutes after
install. It's not fine forever.

Three patterns make a host's account model healthy:

- **Treat root as glass-break**, not a daily account. Long random password,
  stored in a secret manager, used only when nothing else works (host won't
  join vCenter, network is down, the audit log will show "root" anyway).
- **Use named local accounts** for the small number of people who genuinely
  need direct host access. Each person's actions are tied to their own login,
  so the audit log is meaningful.
- **Delegate auth to vCenter SSO** for daily admin work. The host trusts
  vCenter; vCenter authenticates against your identity provider (AD, LDAP,
  SAML); admins log in to vSphere Client with their own corporate identity.
  Direct host login becomes the exception, not the rule.

ESXi has three predefined roles at host level: **No Access**, **Read-Only**,
and **Administrator**. You can add custom roles if you need finer control,
but most shops live with the defaults plus vCenter-delegated permissions.

A separate decision: do you join the host to Active Directory directly?
Possible, but most shops skip it — they let vCenter do the AD integration and
keep the host itself with a small set of local emergency accounts. One less
moving part on each host.

## Before / After

**Before**: Six admins all share the `root` password. Audit log shows `root`
ran every command. When something breaks, no one knows who did what.

**After**: `root` lives in a vault. Each admin logs in to vSphere Client as
themselves, gets routed through vCenter, and the audit log shows their name.
Direct host access is reserved for emergencies, with named local accounts as
backup.

## Analogy

Account best practice on ESXi is like a building's keycard policy. The
master skeleton key (root) lives in the safe at the front desk — it opens
every door but is only checked out in an emergency, and the checkout is
logged. Everyone else has a personal keycard with only the doors they need.
When something goes wrong, the keycard log tells you who walked through
which door, when.

## Quick check

> **Question** — A new sysadmin will be doing day-to-day VM work via vSphere
> Client. Which account approach is best?
>
> **Answer** — Give them a named identity in your IdP (AD/LDAP/SAML), let
> vCenter SSO authenticate them, and assign the appropriate role at the
> vCenter level. They should almost never log in to a host directly, and
> they definitely should not use `root`.

## ELI5

The key that opens every door in the building should not be the key everyone
carries around. Lock it in the safe. Give people their own little keys for
just the rooms they need. Now if something goes missing, you know whose key
was used.

## ELI10

ESXi has a single super-admin account called `root`. If everyone uses it,
nobody is accountable. Best practice is: keep `root` for emergencies,
create per-person accounts (or, better, log in through vCenter using your
corporate identity), and assign each person only the permissions they need
to do their job. ESXi has built-in roles like "Read-Only" and
"Administrator," so a junior engineer who only needs to look at logs gets
Read-Only, and only senior staff get Administrator. Bonus: the audit log
records who did what, so when something breaks at 2 a.m. you can figure
out who touched what.

## Real world — what you see live

It's the morning after a P1 incident. The team is doing the post-mortem.
Someone asks "who restarted the management agents on host esx-04 last
night?" The audit log says `root`. Four people had the root password.
Nobody admits to it, nobody can prove they didn't. The post-mortem ends
with an action item: stop sharing root.

---

# Subtopic 3 of 6: Configuring host settings via DCUI and Host Client

## Concept

ESXi gives you two consoles to talk to a single host directly, without
vCenter in the loop. They look different, run on different surfaces, and
exist for different moments.

**DCUI — Direct Console User Interface.** This is the yellow-and-black
text screen you see on a monitor plugged into the server (or via iLO/iDRAC
remote console). Press F2, log in as root, and you can: change the
management network IP / VLAN / NIC, change the hostname, change DNS,
restart management agents, view logs, reset to defaults, shut down or
reboot. It runs locally on the host and needs nothing — no network, no
vCenter — to be useful.

**Host Client.** This is a full web UI served by the host itself on port 443.
Browse to `https://<host-ip>`, log in as root (or a local user), and you
get a richer view: VMs, networks, datastores, hardware health, services,
alarms, events. It needs the host's management network to be working, but
once it is, it's a much friendlier surface than DCUI.

The rule of thumb: **DCUI for bootstrapping and recovery, Host Client for
everything else when vCenter is unreachable.** When vCenter is reachable,
you live in the **vSphere Client** instead — Host Client and DCUI become
the friends you remember you have only when vCenter is down.

The single most useful DCUI move to remember: **Restart Management
Agents** (`Troubleshooting Options → Restart Management Agents`). When a
host stops responding to vCenter but the host itself is up, restarting
the management agents fixes it more often than any other single action.

## Before / After

**Before**: vCenter is the only way you've ever touched a host. vCenter
crashes overnight. You have no idea how to verify whether the host is even
healthy.

**After**: You know to walk up to the iLO, open the DCUI, confirm the host
status; if needed, browse to `https://<host-ip>` and use the Host Client.
You have a path that doesn't depend on vCenter being up.

## Analogy

DCUI is the building's basement control panel — small screen, only the
levers that matter in an emergency, and it works even when the elevators
are dead. Host Client is the building manager's tablet — full controls,
nicer interface, but only useful when the building's network is up. The
vSphere Client (covered in lesson 9) is the city's central operations
office that watches every building at once. You use the city office in
normal times, the manager's tablet during local issues, and the basement
panel when nothing else works.

## Quick check

> **Question** — vCenter is down. A host has stopped showing up in vSphere
> Client (because vCenter is down). Network looks fine. What's your first
> move?
>
> **Answer** — Browse to the host's Host Client at `https://<host-ip>`. If
> the Host Client doesn't load, fall back to the DCUI through the iLO and
> restart management agents from there.

## ELI5

The big computer has two ways for a person to talk to it directly. One is
a small yellow screen on the front of the computer, used in emergencies.
The other is a webpage on the computer itself, used when you need to see
more.

## ELI10

ESXi is normally managed from a central tool called vCenter. When vCenter
is unreachable, you still need a way into a single host. ESXi gives you
two: the **DCUI** is a console UI that runs locally on the host (yellow
text, function keys); it works even if the network is down. The **Host
Client** is a web app served by the host itself; it needs the host's
network to work but gives you a much richer view of VMs, datastores, and
services. Same host, two front doors — pick the one that matches what's
broken.

## Real world — what you see live

3 a.m., on-call. vCenter is unresponsive. The on-call engineer pops the
iLO console of the suspect host. Yellow DCUI. Logs show the host is up,
running its VMs. The engineer hits F2 → Troubleshooting → Restart
Management Agents, watches three lines of "Restarted" messages, and moves
on to investigating vCenter itself. Total time on the host: 90 seconds.
That's the value of knowing DCUI.

---

# Subtopic 4 of 6: Managing host services

## Concept

ESXi runs a small set of background services. The interesting ones for
day-to-day admin work are:

- **SSH** — remote shell to the host. Off by default. Enable when you need
  to shell in for diagnostics; disable when done.
- **ESXi Shell** — local shell on the DCUI. Off by default. Enable for
  console-only access during recovery; disable when done.
- **NTP daemon (`ntpd`)** — time sync. Should be on, with the right NTP
  servers configured. Covered in subtopic 5.
- **syslog (`vmsyslogd`)** — log shipping. Configure to send logs to a
  central syslog server.
- **SNMP** — monitoring agent. Configure if your monitoring tooling speaks
  SNMP.
- **CIM** — hardware monitoring agent (used by vendor health plugins).

Each service has a **startup policy** that decides what happens on host
boot. Three values:

- **Start and stop with host** — runs whenever the host is up. Right for
  things that should always be on (NTP, syslog).
- **Start and stop manually** — never starts on boot; admin starts it on
  demand. Right for SSH, ESXi Shell on a hardened production host.
- **Start and stop with port usage** — niche; service runs while a related
  port is open. Rarely changed.

The single most common mistake here: enable SSH for an investigation,
forget to disable it, and 6 months later the security audit asks why SSH
is on. Fix it by leaving the policy at "Start and stop manually" so even
if the service is on, the next reboot puts the host back to a clean state.

## Before / After

**Before**: SSH is on, has been on for 9 months, no one remembers why.
ESXi Shell is on too. The host is shipping logs nowhere. Time is whatever
the BIOS clock thinks it is.

**After**: SSH and ESXi Shell are off (on demand only). NTP daemon runs
on host boot, pointed at the right NTP pool. syslog daemon ships every
log line to the central syslog server. SNMP is on if your monitoring tool
asks for it.

## Analogy

Host services are the building's utilities. Some run always (water, fire
alarm, central heat). Some are only switched on when a maintenance crew
is on-site (gas line to a service room, freight elevator). The startup
policy is the lobby policy that decides which utilities come back up
after a power cut: the always-on ones do, the maintenance-only ones
don't.

## Quick check

> **Question** — You enable SSH on a production host to investigate an
> issue, then close your laptop. Two weeks later, audit asks why SSH was
> on. What policy choice would have prevented this?
>
> **Answer** — Set SSH's startup policy to "Start and stop manually." The
> service stays running until you stop it or the host reboots; on the next
> reboot, it's off automatically. You don't have to remember.

## ELI5

The big computer has lots of little helpers that can be turned on or off.
Some helpers should always be on (the clock helper, the log helper). Some
helpers should only be on when you're working on the computer and then
turned off again (the back-door helper).

## ELI10

ESXi has services for things like time sync, log shipping, remote shell
access, hardware monitoring, and SNMP. You can turn each one on or off
and decide whether it should auto-start when the host boots. As a rule:
auto-start the things you always want (NTP, syslog), leave the
diagnostics-only services (SSH, ESXi Shell) on "manual" so a reboot
returns them to a safe state. Production hosts should not have SSH on
permanently — it's an attack surface, and you don't need it for normal
operations.

## Real world — what you see live

It's a Tuesday and someone runs the monthly compliance scan. Three hosts
fail because SSH is enabled. The team digs in: those hosts had SSH
enabled six months ago for a network troubleshooting session and the
policy was "Start and stop with host." After the next reboot, SSH was
back on. Fix: set the policy to manual everywhere, then disable SSH on
those three hosts.

---

# Subtopic 5 of 6: Configuring NTP, DNS, and routing

## Concept

These three settings look small, but if any one of them is wrong, large
parts of vSphere stop working. Configure them on every host, before you
ever try to join the host to vCenter.

**NTP — Network Time Protocol.** The host's clock should match the rest
of your environment within a few seconds. Why it matters:

- Certificate validation. Most TLS errors at vCenter join time are clock
  drift in disguise.
- Active Directory authentication. Kerberos refuses tickets if the clock
  drifts more than ~5 minutes.
- Logs. Correlating an incident across ten hosts is impossible if their
  clocks disagree.
- vMotion. Migrations between hosts assume coherent clocks for state
  consistency.

Configure NTP servers (your internal NTP servers if you have them; a
public pool like `pool.ntp.org` if you don't). Set the NTP daemon's
startup policy to "Start and stop with host."

**DNS — Domain Name System.** The host needs to resolve names (forward
DNS) and be resolvable by name (reverse DNS / PTR records). Why it
matters:

- vCenter join uses hostnames in certificates. A missing PTR record
  produces a confusing cert error.
- AD integration uses DNS to find domain controllers (SRV records).
- Many vSphere features (VMware Tools repos, content libraries, update
  servers) refer to URLs that need to resolve.

Configure forward and reverse DNS on your DNS server *before* you set
the host's hostname.

**Routing.** Every host has a **default gateway** for its management
vmkernel interface — the router it sends traffic to when the destination
isn't on the local subnet. If you use separate networks for vMotion,
iSCSI, vSAN, NFS, replication, etc. (recommended; covered in lesson 10),
each of those vmkernel interfaces lives on its own subnet and may need
its own static route. Without those routes, you get long mystery
timeouts that are really "no route to host."

## Before / After

**Before**: The host's clock is 4 minutes off. There's no PTR record. The
default gateway points to the wrong router. Joining vCenter fails with a
cryptic certificate error and you spend an afternoon thinking the
problem is the certificate.

**After**: Clock is in sync to the second. Forward and reverse DNS
resolve cleanly. The default gateway is correct, and any extra vmkernel
routes are in place. vCenter join succeeds first try.

## Analogy

NTP is the building's master clock. DNS is the building directory at the
lobby. Routing is the elevator map at every floor. If the clock is wrong,
nobody can agree on when meetings start. If the directory is wrong,
visitors can't find the right floor. If the elevator map is wrong,
everyone gets off at the wrong place. Each one looks small individually;
together they decide whether anyone can find anyone else in the building.

## Quick check

> **Question** — A new ESXi host won't join vCenter. The error mentions
> certificate validation. You've checked the certificate twice. What's
> the next thing to check?
>
> **Answer** — The host's clock. NTP misconfiguration causes most
> "certificate" errors at join time. If the clock drifts more than a
> small window, the host's view of the certificate's validity period
> doesn't line up with reality, and TLS rejects it.

## ELI5

The clock has to be right, the address book has to be right, and the
elevator map has to be right. If any one of those is wrong, nothing in
the building works.

## ELI10

ESXi hosts care a lot about three things: knowing the correct time
(NTP), being able to look up other servers by name (DNS), and knowing
which network gateway to send traffic through (routing). When time is
wrong, certificates fail and Kerberos breaks. When DNS is wrong, vCenter
join fails and AD breaks. When routing is wrong, you get mysterious
timeouts. The fix is the same in each case: configure them carefully on
every host before doing anything else, and double-check them when
something later seems off.

## Real world — what you see live

You're standing up a new host. You've followed the runbook, set the IP,
joined the management network. You go to add the host to vCenter and get
"certificate verification failed." You check the cert. It's valid. You
check the cert again. Still valid. An hour in, you check the time on the
host: it's 4 minutes ahead. NTP isn't configured. You point it at the
internal NTP server, force a sync, retry the join. Works first try.

---

# Subtopic 6 of 6: Configuring ESXi for lockdown mode

## Concept

Lockdown mode is a host-level switch that restricts who can talk to the
host directly, outside of vCenter. It's a security posture choice, not a
performance setting. There are three modes:

- **Disabled** — the default. Anyone with valid host credentials can log
  in directly via Host Client, DCUI, SSH (if on), or PowerCLI/API.
- **Normal** — direct host access is restricted to the DCUI and to a
  small list of *exception users*. Day-to-day admin must go through
  vCenter. The DCUI still works, so an admin at the console can still
  recover the host.
- **Strict** — direct host access is disabled even at the DCUI. The
  *only* path in is through vCenter or via configured exception users.
  Recovery is harder; the lockout is more complete.

**Exception users** are local accounts that bypass lockdown — useful
for service accounts (a backup tool that needs direct host access) or
for break-glass accounts that compliance requires.

When to choose each:

- **Disabled** — labs, isolated test environments where the security
  posture isn't a concern.
- **Normal** — most production environments. Locks down the casual
  bypass routes, keeps the safety net of DCUI for recovery.
- **Strict** — regulated environments (PCI, HIPAA, FedRAMP) where
  compliance demands no direct host access at all.

Two practical reminders:

1. **Test recovery** before you flip Strict on a host you can't physically
   reach. If vCenter dies and you have no exception user, you might be
   reinstalling.
2. **Document exception users**. They're easy to add and easy to forget,
   and they become the next audit finding if no one knows why they exist.

## Before / After

**Before**: Lockdown disabled. Six tools and four people connect
directly to each host via Host Client and SSH. There is no enforced
funnel through vCenter, so the audit log is fragmented across many
sources.

**After**: Lockdown set to Normal. Daily admin goes through vCenter; the
audit trail is centralized. DCUI is still available for emergency
recovery. One service account is in the exception list (and documented).

## Analogy

Lockdown mode is locking the building's side and basement doors so the
only way in is the front lobby (vCenter). Strict mode also locks the
basement key cabinet (DCUI), which means you'd better keep a spare key
with the trusted neighbor (exception user) or you'll be calling a
locksmith. Exception users are the short list of trades who keep their
own key — the elevator company, the alarm company — because turning
them away every visit isn't practical.

## Quick check

> **Question** — A regulated workload requires that no admin connect
> directly to a host. Which lockdown mode and what supporting setup do
> you choose?
>
> **Answer** — Strict mode, with one or two carefully documented
> exception users for service accounts that genuinely need direct host
> access (e.g., a backup agent). All human admin goes through vCenter.

## ELI5

You can lock the building so the only way in is the front door. You can
lock it harder so even the basement door is closed and only people with a
special pass can get in.

## ELI10

Lockdown mode controls who can talk to an ESXi host directly without
going through vCenter. Disabled means anyone with valid credentials can
log in directly. Normal means direct logins are restricted but the
console (DCUI) still works for emergencies. Strict means even the
console is restricted; the only way in is vCenter or a pre-approved
exception user. You pick the mode based on how locked-down you need to
be — production usually picks Normal; regulated environments pick
Strict.

## Real world — what you see live

A compliance audit is coming. The team flips every production host to
Normal lockdown, adds the backup service account to the exception
list on the cluster's hosts, and writes a one-line entry in the runbook
explaining what that exception user is for. The audit asks one question:
"why is account `svc-backup` an exception user?" The team points at the
runbook entry. Audit moves on. That's the whole point of documenting
exceptions.

---

## Lesson recap (cross-subtopic)

One host. Six configuration moves. They go in this order on purpose:

1. **Install** — the box becomes a hypervisor.
2. **Accounts** — you decide who can log in and how.
3. **DCUI / Host Client** — you confirm you can reach the host two ways.
4. **Services** — you decide what the host runs in the background.
5. **NTP / DNS / routing** — you make sure the host knows what time it is,
   what other servers exist, and how to reach them.
6. **Lockdown** — you decide who can bypass vCenter to reach this host.

Get those six right and the host is ready to be joined to vCenter. That's
lesson 9.
