# Lesson 06 — Types of hypervisors

*Course: vSphere Fundamentals · Domain: VMware · Position: 06*

---

## 1. Concept explanation

There are two kinds of hypervisors. The difference is where the hypervisor sits relative to the host operating system. The choice between them is a choice between performance and convenience.

**Type 1 (bare-metal).** The hypervisor runs directly on the physical hardware. There is no host operating system. The hypervisor is itself an extremely focused operating system whose only job is running VMs. ESXi is Type 1. So are KVM (built into the Linux kernel), Microsoft Hyper-V, and Xen.

Because Type 1 has no general-purpose OS underneath stealing CPU cycles or making decisions, it gives near-native performance. It also has a smaller attack surface — fewer running services means fewer things to exploit. Type 1 is what production datacenters and public clouds run on.

**Type 2 (hosted).** The hypervisor runs as an application on top of a regular operating system — Windows, macOS, or Linux. The host OS handles the hardware; the hypervisor handles the VMs through the host OS. VMware Workstation, VMware Fusion, Oracle VirtualBox, and Parallels Desktop are all Type 2.

Type 2 is slower than Type 1 because every hardware request goes through one extra layer (the host OS). But Type 2 is dramatically more convenient. A developer can install VirtualBox on their laptop and have a Linux VM running in five minutes, without setting up a bare-metal hypervisor and dedicating a whole machine to it.

**The decision rule.** Production servers and clouds: Type 1. Developer laptops, testing environments, learning: Type 2. The two hypervisor types coexist in modern IT — they're tools for different jobs.

---

## 2. Before / after

**Before VMware ESX (pre-2001 on x86).** The only hypervisors available for x86 were Type 2 — they ran on top of an operating system. Performance was a real problem; running a VM through a hosted hypervisor meant losing 20-30% of the host's performance to the OS overhead. This was tolerable for testing but unacceptable for production workloads.

**After ESX (2001 onward).** Type 1 hypervisors arrived for x86. Production-grade virtualization with near-native performance became available on commodity hardware. Type 2 hypervisors didn't disappear — they remained the right choice for desktop use cases — but production virtualization decisively moved to Type 1, where it remains today.

---

## 3. Analogy — building vs. basement

The apartment-building analogy from Lesson 1 splits naturally into the two hypervisor types.

**Type 1** is a purpose-built apartment building. The whole structure was designed from day one to be apartments. The superintendent owns the whole building. Plumbing, electrical, structural elements — all engineered for the apartment use case. Tenants live in apartments efficiently, with no compromises.

**Type 2** is a single-family house where the owner has converted the basement into a couple of rental units. The owner still lives upstairs, in the main living-space (the host operating system). The basement apartments are real, but they share a front door, share the building's plumbing, and the renters have to coordinate with the owner about everything. It works, but it's not what the building was designed for.

A purpose-built apartment building (Type 1) is more efficient, but it's a bigger commitment. The basement-apartment setup (Type 2) is far more accessible — anyone with a single-family house can do it — but the trade-offs are real.

---

## 4. ELI5 and ELI10

### ELI5

There are two kinds of "computer pretend houses." The first kind is built on the empty land — the apartments are the whole building. That's faster and bigger, but you need a piece of land to start. The second kind is when you have a regular house and you let some friends live in the basement. It's easier to set up — you already have a house — but it's slower because everyone has to use the same front door. Big companies use the first kind. People learning at home use the second kind.

### ELI10

A Type 1 hypervisor (also called bare-metal) runs directly on the hardware. There's no host operating system; the hypervisor itself acts as a minimal, specialized OS. ESXi, KVM, Microsoft Hyper-V, and Xen are Type 1. Type 1 wins on performance — every CPU cycle is available to VMs — and on security, because there's no general-purpose OS providing extra attack surface.

A Type 2 hypervisor runs as an application on top of a normal OS (Windows, macOS, Linux). The host OS handles hardware access; the hypervisor sits above it as another program. VMware Workstation, VMware Fusion, VirtualBox, and Parallels are Type 2. Type 2 loses some performance to the OS layer underneath but is far easier to install — you just install it like any other application.

In practice, Type 1 dominates production and public cloud; Type 2 dominates desktop and developer use. Both will be around for a long time because they serve different needs.

---

## 5. Real-world scenarios

### A datacenter team running ESXi

A 200-host vSphere environment in a financial services company runs ESXi on every physical server. The performance margin matters — at this scale, losing 20% to a host OS would mean buying 40 more physical servers. Type 1 is the only viable choice.

### A developer using VMware Workstation

A backend developer at a SaaS company uses VMware Workstation on their Windows laptop to run three Linux VMs locally — one for each environment they're testing against. They don't care about losing 15% performance; they care that they can spin up a VM in two minutes without IT involvement. Type 2 is the only practical choice.

### A platform team running KVM

A cloud-native platform team at a 500-person tech company runs KVM (Type 1, integrated into Linux) on bare-metal servers, then runs Kubernetes on top. KVM gives them the bare-metal performance Kubernetes needs, while still letting them use familiar Linux tooling for management.

### A trainer teaching a class

A VMware instructor uses VMware Workstation on her teaching laptop to demonstrate ESXi itself — running ESXi as a VM inside Workstation for class demonstrations. It's a Type 1 hypervisor running inside a Type 2 hypervisor. Performance is poor, but it's perfect for showing students how ESXi installs and configures.

---

## 6. Animated illustration

Open `animation.html` for the side-by-side comparison. Two mode buttons toggle between Type 1 and Type 2. The static diagram (`diagram.svg`) shows both stacks together for direct comparison.

---

## 7. Flashcards and quiz

Ten flashcards in `flashcards.yaml` cover the two types, examples, performance differences, and use cases. Three quiz questions test which type applies in different scenarios.
