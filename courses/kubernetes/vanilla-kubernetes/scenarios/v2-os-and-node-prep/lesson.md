# K-VAN V2 — V2 · OS and Node Preparation for kubeadm

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V2 · OS and Node Preparation
> Companion preview: `/preview-kubernetes-vanilla-lesson-02.html`.

---

**🎯 If you remember nothing else:** Per-node prep, in order: **kernel modules** (`overlay`, `br_netfilter`), **sysctl** (`net.ipv4.ip_forward=1`, `net.bridge.bridge-nf-call-iptables=1`), **swap OFF**, **time sync**, **container runtime** (`containerd 2.x` with `SystemdCgroup=true`), **image pre-pulling** for air-gap. Reboot, sanity-check, then run kubeadm.

## 1. Why per-node prep exists

Linux is configurable to a fault. K8s assumes a specific configuration: certain kernel modules loaded, certain sysctl values, no swap, a CRI-compatible runtime, the right cgroup driver. The kubelet and CNI plugins fail in confusing ways when these aren't right. The one good thing: the checklist is short and the same on every node.
    Your goal in V2 is a node that, when handed to `kubeadm`, joins the cluster cleanly. That means the same six categories on every node: kernel, network sysctl, swap, time, runtime, hardening.

## 2. What the cluster expects from the host

**Modules to load at boot** (write to `/etc/modules-load.d/k8s.conf`):
    `overlay
br_netfilter`
    Then `modprobe overlay` and `modprobe br_netfilter` for the running kernel.
    **sysctl values** (`/etc/sysctl.d/k8s.conf`):
    `net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1`
    Then `sysctl --system`. `br_netfilter` must be loaded before sysctl applies — order matters.

## 3. The other three categories

**Swap.** Kubelet refuses to start with swap enabled by default (you can enable swap support explicitly via `KubeletConfiguration` in K8s 1.28+, but most production clusters keep it off). Disable now and persist:
    `swapoff -a
sed -i '/ swap / s/^/#/' /etc/fstab`
    **Time sync.** Certificates, etcd, and audit logs all assume monotonic time. Run `chrony` or `systemd-timesyncd`; verify with `chronyc tracking` (offset < 100ms).
    **Container runtime.** Install `containerd 2.x`:
    `# Generate default config
containerd config default | sudo tee /etc/containerd/config.toml

# CRITICAL: enable systemd cgroup driver to match kubelet
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# Optional: configure registry mirror for air-gap or ratelimit avoidance
# [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
#   endpoint = ["https://harbor.corp/v2/dockerhub-proxy"]

systemctl restart containerd
crictl info | grep -i cgroup  # verify systemd`

## 4. Beyond minimum-viable

**Node hardening** (cover at minimum):
    
      - SSH: key-only auth (`PasswordAuthentication no`); root login disabled; SSH on standard port behind a bastion.

      - auditd: enable at boot; ship logs to a central collector.

      - Firewall: `ufw` / `firewalld` allowing only required ports (6443 to CP, 10250 kubelet, etcd 2379-2380 between CP, CNI overlay UDP if applicable).

      - SELinux/AppArmor: keep enabled (`setenforce 1` on RHEL family). K8s components have AppArmor profiles; PSA `restricted` requires AppArmor.

      - Log rotation: `logrotate` for `/var/log/containers/*` and `/var/log/pods/*` if not handled by container runtime.

      - Package management: pin `kubeadm`, `kubelet`, `kubectl`, `containerd` to a known version; `apt-mark hold` / `dnf versionlock` to prevent surprise upgrades.

    
    **Air-gapped image pre-pull.** If the cluster has no internet, you must seed the kubeadm + add-on images on every node:
    `# Online: list and pull
kubeadm config images list --kubernetes-version v1.36
kubeadm config images pull --kubernetes-version v1.36

# Air-gap: ctr -n k8s.io images import <tar> on every node
# Or push to internal registry mirror + configure containerd`
    [ deep dive — skip if new ]For Talos Linux: most of this is the machine-config YAML you write at install time — no manual `modprobe`, no per-node tweaking. The OS image bakes in the right kernel modules and cgroup driver. That's the appeal of immutable infra: V2 collapses to "apply machine-config."

## Before / After

**Before.** SSH into 6 nodes. `vim` some files. Forget one. Run kubeadm. Hang. Diagnose. Fix. Re-run. Hang differently. Repeat for hours. Different team members do it differently; nodes drift; "works on my node" stories abound.

**After.** Per-node prep is one Ansible playbook (or one Talos machine-config YAML). Idempotent, repeatable, version-controlled. New node = run playbook + reboot + verify with a sanity script. kubeadm runs first time. Drift impossible.

Per-node prep is the most automatable layer of self-managed K8s. Manual SSH-and-edit is the wrong unit of work even for one cluster.

## Analogy — the K-Frontier site

Land Clearing is the second site. Trees don't fall and stones don't arrange themselves. Before any frame goes up, the surveyor walks the plot, removes the stumps (legacy services that conflict), checks the soil pH (kernel modules + sysctl), tests the well water (time sync), and stockpiles the materials at the build site (image pre-pull). The work is repetitive but each step prevents a class of later disaster. Skip the soil test, your foundation cracks. Skip the kernel modules, your CNI never starts.

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| Soil pH test | Kernel modules + sysctl |
| Removing stumps + brush | Disabling swap + conflicting services |
| Calibrating tools | Time sync (chrony / timesyncd) |
| The contractor's toolbox | Container runtime (containerd / CRI-O) |
| Cgroup-driver toolbox lock | `SystemdCgroup = true` alignment |
| Stockpiling materials at the site | Image pre-pull for air-gap installs |
| Posted construction rules | Hardening: SSH, audit, firewall, SELinux |

⚠️ *Analogy stops here:* The analogy stops here: kernel modules + sysctl aren't physical preparation — they're knobs in /proc and /sys that only matter at runtime. Setting them and rebooting is more like "flipping breakers" than "clearing land."

## ELI5 / ELI10

**ELI5.** Before you build a treehouse, you check that the tree is healthy and bring all your tools to the spot. Same for a Kubernetes node: check the kernel, turn off swap, install containerd, gather images.

**ELI10.** Per-node prep checklist for kubeadm to work: load kernel modules (`overlay`, `br_netfilter`), set sysctls (`ip_forward`, `bridge-nf-call-iptables`), disable swap, sync time, install + configure containerd 2.x with `SystemdCgroup = true`, harden the host, optionally pre-pull images for air-gap. Order matters: modules before sysctl. Automate via Ansible or use Talos Linux which bakes it in.

## Real-world scenarios

- **A bank using Ansible playbook for 50 nodes.** One playbook. Idempotent. Tests with `--check`. Runs in CI on every change. New rack of 10 nodes onboarded by a junior engineer in an afternoon. Drift detected automatically by a daily Ansible-pull cron.
- **A startup picking Talos to skip V2 entirely.** No SSH, no per-node prep. Machine-config YAML defines the kernel + sysctl + runtime in one place. Boot the Talos image; nodes register themselves. The whole V2 module collapses to writing the machine-config. Trade-off: less flexibility for non-K8s workloads on the host.
- **A team that learned about the cgroup-driver bug.** First install: containerd cgroupfs, kubelet systemd. `kubeadm init` hangs. Three hours of debugging. Now: every node sanity-script checks `crictl info` output before kubeadm runs. Pre-flight assumption — fail loudly, fix instantly.
- **An air-gapped install at a defence contractor.** No internet. `kubeadm config images pull` + `ctr images export` on a connected build host. Tarballs to physical media. `ctr -n k8s.io images import` on every disconnected node. Plus internal Harbor mirror with the rest of the add-on images. Air-gap process documented + automated.

## Common misconceptions

- **Myth:** "Disabling swap is optional in modern K8s."
  **Truth:** K8s 1.28+ supports swap behind a feature gate, but most production clusters still disable it. Memory eviction logic and QoS classes assume no swap; enabling adds complexity. Default to off unless you have a specific reason.
- **Myth:** "The cgroup driver doesn't really matter as long as both ends agree."
  **Truth:** True — but the failure mode when they disagree is opaque. Always systemd in 2026 (it's the default for all major distros + containerd). "Both agree on systemd" is the rule.
- **Myth:** "You can skip `br_netfilter` if your CNI handles its own networking."
  **Truth:** Even Cilium with eBPF prefers `br_netfilter` loaded for compatibility paths. The cost of loading it is essentially zero; load it anyway.

## Recap

Six categories of node prep — kernel, sysctl, swap, time, runtime, hardening — repeated identically on every node. Automate via Ansible or skip with Talos.

**Next — V3: kubeadm Cluster Bootstrap.** Now that the soil is prepared, raise the frame: kubeadm phases, configuration files, HA control plane, worker join, the alternative bootstrappers (kubespray / kOps / Talos / Cluster API).

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
