# K-ADV-AI I1 — I1 · GPU Nodes + Device Plugin + GPU Operator + MIG + DRA

> Course: K-ADV-AI (advanced specialization)
> Module I1 · GPU + DRA + MIG
> Companion preview: `/preview-kubernetes-adv-ai-lesson-01.html`.

---

**🎯 If you remember nothing else:** **NVIDIA device plugin = baseline; GPU Operator = full stack; MIG = hardware partition for sharing; DRA = K8s-native multi-vendor advanced scheduling. Pick stack by GPU model + sharing needs.**

## 1. Driver + container runtime + node labels

GPU node setup: NVIDIA driver (version-pinned per CUDA + framework); container runtime configured for GPU passthrough (containerd `nvidia` runtime class); node labels marking GPU model + count.
    Per-cluster: separate GPU node pools (NodePool / MachineSet) labelled `accelerator: nvidia-h100`; nodeSelector / affinity in Pods picks the right pool.
    Cloud-managed: AWS p5/p4d, GCP A3/A4, Azure ND/NV families. Bring-your-own: Bottlerocket / Ubuntu + GPU Operator handles driver + runtime.

## 2. Baseline + full-stack

**NVIDIA device plugin** (DaemonSet): advertises `nvidia.com/gpu` resources to kubelet. Pod requests `resources.limits.nvidia.com/gpu: 1`; scheduler places.
    **GPU Operator**: opinionated bundle — installs driver (containerized), container runtime, DCGM (metrics), MIG manager, node feature discovery, GPUDirect Storage / RDMA. Recommended for any cluster that takes GPU work seriously.
    Operator-managed driver = no host-level driver install drift; upgrades via Helm + node draining.

## 3. Hardware partition H100 / A100 into shareable instances

**MIG**: H100 / A100-only feature. Hardware-partitions one GPU into up to 7 instances (H100: 1g.10gb / 2g.20gb / 3g.40gb / 7g.80gb). Each instance has dedicated SMs + memory + L2 cache; full isolation.
    Configure via MIG manager (in GPU Operator) per node. Pod requests `nvidia.com/mig-1g.10gb: 1`; scheduler matches instance.
    Trade: one GPU's aggregate compute = sum of slices; no oversubscription. Best for many small inference Pods + tenant isolation.

## 4. K8s-native multi-vendor advanced scheduling

**DRA** (K8s 1.32 stable): the K8s-native replacement for per-vendor device plugins. Vendor ships a DRA driver; declares *structured parameters* for the device class (memory size, model, MIG profile, RDMA capability). Pods declare claims; scheduler matches.
    Wins: *multi-vendor* (NVIDIA + AMD + TPU + custom accelerators all use DRA), *partial sharing* (multiple Pods can claim parts of one device), *complex placement* (NUMA, RDMA-enabled, same-NUMA Pods together).
    Adoption: NVIDIA DRA driver, AMD DRA driver, GKE TPU DRA driver shipping. New cluster setup increasingly defaults to DRA over per-vendor device plugins.

## Before / After

**Before.** Pre-MIG / DRA, every GPU Pod took a whole GPU. Underutilization rampant; cost / utilization mismatch; long pending queues for tiny inference jobs.

**After.** MIG slices H100 into 7 instances; DRA structured parameters for advanced scheduling; GPU Operator manages full stack. One GPU serves many tenants; utilization rises 3-5×.

*Slice + share + structured-schedule. Expensive GPUs deserve expensive utilization.*

## Analogy — the K-Observatory array

The Optics Bay houses the observatory's telescopes (GPUs). Old practice: each astronomer booked a whole telescope for the night even if they only needed a wide-angle lens. New practice: **MIG** partitions each telescope into separate eyepieces — 7 astronomers can observe at once, each with isolated optics. **DRA** is the booking system that handles many telescope vendors (NVIDIA + AMD + TPU) with one form: "I need a 80GB-memory eyepiece on a node with low-latency to other observers in my project."

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Telescope | GPU (H100 / A100 / B200 / TPU) |
| Observatory floor manager | GPU Operator |
| Telescope availability bell | NVIDIA device plugin |
| Eyepiece partitions | MIG instances (1g.10gb / 2g.20gb / etc.) |
| Multi-vendor booking system | DRA (Dynamic Resource Allocation) |
| Booking form fields | Structured parameters (memory / RDMA / NUMA) |
| Telescope nightly utilization | GPU utilization (DCGM metrics) |

⚠️ *Analogy stops here:* A real telescope has fixed optics; MIG instances are hardware-partitioned but configurable per-node. DRA is structured-API; vendors must ship drivers.

## ELI5 / ELI10

**ELI5.** One big telescope can be split into 7 eyepieces so 7 astronomers can use it at once. A booking system handles different telescope brands with one form.

**ELI10.** **GPU node**: NVIDIA driver + containerd runtime + node labels. **NVIDIA device plugin**: advertises GPU resources. **GPU Operator**: opinionated bundle (driver + runtime + DCGM + MIG mgr + RDMA). **MIG**: H100/A100 hardware partition (up to 7 instances). **DRA**: K8s-native multi-vendor structured parameters; replaces vendor device plugins for advanced scheduling.

## Real-world scenarios

- **Inference fleet — MIG cuts cost 4×.** Inference workload using one H100 per Pod (most Pods using < 20% GPU). Migrate to MIG 1g.10gb per Pod; one H100 hosts 7 inference Pods; cost / Pod drops 4×.
- **DRA — multi-vendor cluster.** Cluster has NVIDIA + AMD GPUs. DRA: one ResourceClaim API for both vendors. Pod claims memory + framework requirement; scheduler picks matching device. Replaces 2 separate device plugins.
- **GPU Operator simplifies driver lifecycle.** Pre-Op: bare-metal driver install drift across nodes; CUDA version mismatches. Post-Op: containerized driver via Operator; Helm-managed; deterministic across nodes.
- **Outage — driver mismatch.** Pre-Op cluster: H100 driver upgraded on some nodes; CUDA 12.0 vs 12.2; some workloads crashed. Postmortem: install GPU Operator; consistent driver via Helm + DaemonSet.

## Common misconceptions

- **Myth:** "NVIDIA device plugin enough; skip GPU Operator."
  **Truth:** Device plugin is one DaemonSet; Operator bundles driver + runtime + DCGM + MIG mgr + RDMA. Operator saves weeks of bespoke setup; recommended for any production cluster.
- **Myth:** "DRA replaces GPU Operator."
  **Truth:** DRA replaces per-vendor device plugin's scheduling role. GPU Operator still handles driver + runtime + DCGM + MIG mgr — orthogonal concerns.
- **Myth:** "MIG is always better than time-slicing."
  **Truth:** MIG is hardware-isolated; time-slicing is software-shared (lower isolation; QoS sensitive). Both are useful; MIG for isolation; time-slicing for elastic sharing where collisions are tolerable.

## Recap

GPU node + GPU Operator (driver/runtime/DCGM/MIG/RDMA) + MIG (hardware partition) + DRA (multi-vendor scheduling). Slice + share + structured-schedule = high GPU utilization.

**Next — I2: Kueue + MultiKueue + Volcano gang scheduling.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
