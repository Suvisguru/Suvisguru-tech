# Lesson 08 — How Containers Actually Work (Linux Namespaces · cgroups · Capabilities)

> Course: Kubernetes — Common to all distributions
> Lesson 08 of 17 in K-COM. **Module 2 begins** — Containers (Comprehensive),
> Lesson 1 of 5.
> Companion preview: `/preview-kubernetes-lesson-08.html`.

---

## 1. Concept

A container isn't a magical sandbox. It's a regular Linux process that
the kernel *tricks* into thinking it's alone on the machine. Five Linux
features make this work, and they all came from the kernel — not from
Docker, not from Kubernetes. Docker just made them easy to use.

**Namespaces** give each container its own private view of system
resources. There are 8 namespace types in modern Linux: PID, NET, MNT,
UTS, IPC, USER, cgroup, and time.

**cgroups (control groups)** are the meters. Each container gets a
budget for CPU, memory, disk I/O, and network bandwidth. Try to use more
than your budget, and the kernel throttles you (or kills the process for
memory). Two versions: v1 (legacy, hierarchies per resource) and v2
(unified hierarchy, modern default since ~2022).

**Capabilities** chop the old "root vs not-root" model into ~40
fine-grained permissions. Instead of giving a container full root, you
give it just `NET_BIND_SERVICE` or just `SYS_TIME`. Containers should
drop everything they don't need.

**seccomp** filters which Linux system calls a container can make.
Modern container runtimes apply a default profile blocking the ~70
most-dangerous syscalls (out of ~300 total). Custom profiles available
for tighter restriction.

**AppArmor / SELinux** are mandatory access control (MAC) systems.
Ubuntu/Debian default to AppArmor; RHEL/Fedora default to SELinux. They
define explicit policies — "this container can read these files but not
those" — at a layer below normal Linux permissions.

That's it. Five Linux features. Stack them together and you have a
container. Take them away and a container is just a normal process.

---

## The 8 namespaces

| Namespace | What it isolates |
|-----------|------------------|
| PID | Process IDs — container sees its own PID 1, 2, 3 |
| NET | Network interfaces, IPs, routes, firewall |
| MNT | Filesystem mounts — container's root FS |
| UTS | Hostname and domain name |
| IPC | Inter-process communication |
| USER | User and group ID mapping |
| cgroup | View of the cgroup hierarchy |
| time | Monotonic and boot clocks (newest) |

When you create a container, the runtime calls `clone()` with flags like
`CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS` to put the new process in
fresh namespaces. That single syscall is the moment a "container" comes
into existence.

---

## 2. Before / After

**Before — pre-2008.** Multiple processes on one Linux machine shared
everything: same PID space, same network, same filesystem, same hostname.
Process A could see B's PIDs, ports, files. If A started a runaway loop,
it stole all the CPU. Companies that wanted real isolation used VMs.

**After — namespaces + cgroups.** Linux added namespaces and cgroups
over the late 2000s. By 2013, Docker showed how to combine them into
something usable. Now multiple processes can run on the same kernel but
think they're alone, with hard limits on CPU and memory. That's a
container.

What didn't change: containers still share the kernel. A kernel exploit
affects everything. For untrusted multi-tenancy, use VMs or sandboxed
runtimes (gVisor, Kata).

---

## 3. Analogy — an office building with utility meters

Think of a 4-story office building. Many tenants share the same
building — same foundation, same plumbing, same electricity. But each
tenant rents a private office: their own door, desk, walls, filing
cabinet. From inside, it feels like their own space.

The building has a utility meter for each office. Office A pays for the
electricity it uses. Office B has its own meter. The landlord caps how
much power each office can pull. There's a security guard at each door
checking IDs.

Linux containers work exactly the same way. Namespaces are the office
walls. cgroups are the utility meters. Capabilities, seccomp, and
AppArmor/SELinux are the security guards. The building (host kernel) is
shared, but each container thinks it's alone.

**Mapping:**

- Office building = host machine + Linux kernel
- Each office = a container
- Office walls + private door = namespaces
- Utility meters = cgroups
- Doorman / security guard = capabilities + seccomp + AppArmor/SELinux
- Shared building utilities = the kernel

---

## 4. ELI5 / ELI10

**ELI5.** Imagine a big shared playroom. Linux puts up little curtains
so each kid has their own pretend room. Each kid has a snack bowl with
rules on how many cookies they can eat. And there's a teacher checking
what they're allowed to do. The kids share the same playroom floor (the
kernel) but they each think they have their own little space.

**ELI10.** A container is just a regular Linux process with three things
added by the kernel: **namespaces** (it sees its own private slice of
process IDs, network, files, hostname, etc.), **cgroups** (it has hard
limits on CPU, memory, disk I/O), and **security policies**
(capabilities, seccomp, AppArmor/SELinux — fine-grained control over
what kernel actions it can perform). When you "start a container" with
Docker or containerd, the runtime calls `clone()` with namespace flags,
configures cgroups, drops most capabilities, and applies a seccomp
profile. The result is a process that thinks it's alone on the machine.
Hundreds can run on one host because they all share the host's kernel —
way more efficient than VMs.

---

## 5. Real-world scenarios

**Container OOM-killed at 256Mi.** An engineer notices their pod keeps
restarting. `kubectl describe pod` shows reason: `OOMKilled`. They had
set memory limit to 256Mi. The app legitimately needed 350Mi at peak.
The kernel's cgroup-v2 memory controller saw memory usage exceed the
cgroup's limit and killed PID 1 in the container. Fix: bump the limit.

**Container can't bind to port 80.** A developer's containerized web
app fails: `permission denied` binding to port 80. The container is
running as a non-root user (good practice). Ports below 1024 require
`CAP_NET_BIND_SERVICE`. Modern container runtimes drop this capability.
Fix: bind to 8080 and let the load balancer rewrite, or explicitly add
`NET_BIND_SERVICE` to capabilities.

**Container A sees container B's processes.** A security audit finds
container A can see container B's process list via `ps`. Investigation:
someone set `hostPID: true` in container A's pod spec, sharing the
host's PID namespace. Fix: remove `hostPID: true`. Audit other
"host*" fields too.

**Custom seccomp profile for sandboxed code execution.** A team runs
untrusted user code (a code-execution playground). The default seccomp
profile blocks ~70 syscalls but still allows things like `ptrace`. They
write a custom seccomp profile blocking ptrace, ioctl, and several
others. The user code runs normal Python; it can't escape the sandbox.

---

## 6. Animated illustration

Three modes in the preview animation:

1. **Build a container.** Kernel adds namespaces (step 1), cgroups
   (step 2), capabilities dropped (step 3), seccomp + LSM applied
   (step 4). After step 4, the process is now a "container."
2. **Memory limit hit (OOMKilled).** Container memory usage rises from
   128Mi → 240Mi → 256Mi. At limit, the kernel fires SIGKILL on PID 1.
   Container exits with code 137. Pod restarts.
3. **hostPID: true escape.** Pod set with `hostPID: true`. Container
   running `ps -ef` sees every host process. Lesson: every `host*` field
   drops a namespace.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
