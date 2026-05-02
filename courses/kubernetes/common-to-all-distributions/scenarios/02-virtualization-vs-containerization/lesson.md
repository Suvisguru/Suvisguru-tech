# Lesson 02 — Virtualization vs Containerization

> Course: Kubernetes — Common to all distributions
> Lesson 02 of 17 in K-COM. Foundational concept lesson.
> Companion preview: `/preview-kubernetes-lesson-02.html`.

---

## 1. Concept

A virtual machine (VM) is a complete pretend computer running inside a real
one. It has its own OS, its own kernel, its own simulated disk and network —
everything a real computer has, just in software. The software that creates
VMs is called a hypervisor. One physical server might run 5–50 VMs.

A container is much lighter. It's a single isolated process that *shares*
the host computer's operating system. It packages the app and the files it
needs, but doesn't carry its own OS — it borrows the one running underneath.
The software that creates containers is called a container runtime
(containerd, CRI-O, runc, Docker). One server might run hundreds or thousands
of containers.

Both are ways to run multiple apps on one computer with isolation. The
difference is how much each carries. A VM carries a whole OS. A container
carries just the app. That single difference is what gives containers their
speed (no OS to boot), density (no per-app OS overhead), and portability
(image is small) — and it's why Kubernetes picked containers as its unit.

---

## 2. Before / After

**Before (VMs only).** One server might run 3–10 VMs. Each VM carried a full
operating system, so gigabytes of RAM and disk went to OSes alone. Booting
a VM took minutes. Distributing an app meant shipping a 5–20 GB VM image.

**After (Containers).** One server might run hundreds of containers. Each
container shares the host OS, so the only thing inside is the app and its
files (10–500 MB). Starting takes milliseconds. Distributing means pushing
a small container image to a registry.

What didn't change: the physical hardware underneath. Both are still slicing
real CPU, RAM, disk, network — just with different overhead per slice.

---

## 3. Analogy — houses vs apartments

Two ways to house a hundred families.

**Option A.** Build a hundred separate houses, each on its own plot, each
with its own roof, foundation, water heater, furnace, electrical panel.
Every family is fully self-contained. Lots of land, lots of duplicated
infrastructure, very strong walls between families.

**Option B.** Build one apartment building with a hundred units. Each
family has their own door and walls, but the building's foundation, roof,
heating, plumbing, and electricity are all shared. Way less land. Faster
to build. Maintenance happens once, not a hundred times. Trade-off: a
problem in shared infrastructure affects everyone.

VMs are houses. Containers are apartments.

**Mapping:**

- Each house = one VM
- Each apartment = one container
- Building's shared infrastructure = the host OS kernel
- The land underneath = the physical hardware
- Apartment walls between units = Linux namespaces and cgroups

---

## 4. ELI5 / ELI10

**ELI5.** A virtual machine is a pretend tiny computer inside a big computer.
Each pretend computer has its own everything, like a real one. A container
is more like a little room inside a big room — just enough walls to keep
things separate, but it shares the floor and the lights and the air with
all the other little rooms.

**ELI10.** A VM is a complete simulated computer. The hypervisor tricks each
VM into thinking it has its own CPU, RAM, disk, OS. Each VM boots like a real
computer because to itself it *is* one. A container takes a much smaller
approach: it shares the host's OS, but uses Linux features — *namespaces*
and *cgroups* — to give each container its own private view of files,
processes, and network. Same kernel underneath, different views on top.
That's why containers are tiny and start instantly.

---

## 5. Real-world scenarios

**Legacy Windows Server 2008 app.** An accounting system from 2008 still
runs the back office. The cleanest answer is a VM — gives the app its own
Windows Server 2008 environment. Containers don't help: the app needs that
specific OS.

**SaaS startup with 60 microservices.** Containers are the obvious choice —
each service ships as a small image, starts in under a second, packs densely
onto a few VMs (yes, the containers run inside VMs from the cloud provider —
they're complementary).

**Multi-tenant SaaS with hostile tenants.** Different banks, different
agencies, different competing brands. Need stronger isolation than "shared
kernel with namespaces." Use VMs or sandboxed runtimes (gVisor / Kata) so
each tenant gets its own kernel.

**CI/CD running 50,000 test jobs per day.** Containers nail this — spin up,
run, tear down, repeat, with almost no overhead. A VM-based pipeline would
burn most of its time waiting for VMs to boot.

---

## 6. Animated illustration

Three modes in the preview:

1. **VM startup.** Hypervisor allocates → guest OS boots (slow) → app starts.
   Timer reaches several seconds before the app appears.
2. **Container startup.** Host OS already running → container runtime ready
   → app starts as a process. Timer barely moves.
3. **Density comparison.** Same hardware: 3 VMs fit on the left, 12+
   containers fit on the right. Visual demonstration of density difference.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).

---

## Self-critique notes

- **Analogy:** Houses vs apartments. Maps cleanly: own roof = own kernel;
  shared building infrastructure = host OS; walls between apartments =
  namespaces/cgroups. Survives follow-ups ("what about an apartment fire?"
  → "kernel exploit").
- **Density:** ~6 sections after hero, ~10 minute read + 5 minute interactive.
- **Vocabulary:** VM, container, hypervisor, runtime, kernel, namespaces,
  cgroups all defined inline. Specific tools (containerd, KVM, ESXi) named
  but explained as examples rather than required vocabulary.
- **First-time-learner test:** The houses-vs-apartments illustration carries
  the central insight visually. Even without reading the prose, a learner
  sees "house = own everything, apartment = shared infrastructure."
