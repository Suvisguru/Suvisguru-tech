# K-OCP O9 — O9 · OpenShift Virtualization (KubeVirt), AI (RHODS), Edge (SNO + MicroShift)

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O9 · Virtualization, AI, and Edge
> Companion preview: `/preview-kubernetes-ocp-lesson-09.html`.

---

**🎯 If you remember nothing else:** **OCP Virtualization runs VMs as first-class CRs alongside containers; same RBAC, same storage, same networking. OpenShift AI = the Red Hat AI/ML platform stack. SNO + MicroShift extend OCP to the edge; RHACM federates fleets.**

## 1. OpenShift Virtualization — VMs as first-class K8s workloads

**OpenShift Virtualization** = productized **KubeVirt**. Lets you run VMs (Windows, RHEL, Ubuntu, etc.) as **VirtualMachine** CRs alongside containers in the same OCP cluster. Use cases:
    
      - Migrate from VMware vSphere — modernize at your own pace, keep VMs you can't containerize yet.

      - Legacy Windows apps that don't containerize cleanly.

      - Mixed workloads (containers + VMs) sharing the same Networks / NetworkPolicy / Routes / RBAC.

    
    **Core CRs:**
    
      - **VirtualMachine (VM)** — declarative VM spec.

      - **VirtualMachineInstance (VMI)** — running VM (auto-created from VM by virt-controller).

      - **DataVolume** — VM disk storage abstraction (creates a PVC + populates from a source — HTTP image, registry, blank, etc.).

      - **VirtualMachineSnapshot / VirtualMachineRestore** — point-in-time snapshots of VMs.

      - **VirtualMachineInstanceMigration** — live migration to another node.

    
    **Live migration** moves a running VM between nodes (for maintenance / draining) without VM downtime. Requires shared storage (RWX or pre-attached block). Hot-plug NICs and disks on running VMs.
    Networking: Multus Pod-secondary networks for VM-to-physical-network bridging; VM gets a real VLAN-routed IP. **OpenShift Virtualization Operator** installs CRDs + virt-controllers + virt-launcher + virt-handler.

## 2. OpenShift AI — Jupyter, KServe, Kubeflow, distributed training

**OpenShift AI** (rebranded from *Red Hat OpenShift Data Science (RHODS)*) = Red Hat's ML platform on OCP. Components:
    
      - **Notebooks** — Jupyter, JupyterLab, RStudio, Visual Studio Code on Pods. Per-user workspaces; image catalog with curated stacks (PyTorch, TensorFlow, XGBoost).

      - **KServe** — managed Knative-based model-serving. Handles transformer-class large-model inference; auto-scaling, GPU support.

      - **Kubeflow Pipelines (DSP — Data Science Pipelines)** — ML workflow orchestration; reproducible training runs.

      - **Distributed training** via Kubeflow training operator (PyTorchJob, TFJob, MPIJob, MXJob).

      - **RHEL AI** integration — Red Hat's base inference platform with InstructLab + IBM Granite models; can be hosted on OCP via OpenShift AI.

    
    GPU workloads: **NVIDIA GPU Operator** manages drivers, runtime, device plugin. Pods request `nvidia.com/gpu`. MIG (Multi-Instance GPU) supported on H100/H200.
    For distributed training across many GPU nodes: combine PyTorchJob + topology-aware scheduling + RDMA / InfiniBand networking via SR-IOV.
    Use cases: enterprise model training + serving on OCP; combining traditional analytics + LLM inference on one platform; air-gapped + on-prem AI deployments where SaaS isn't an option.

## 3. SNO + MicroShift + Local Zones — edge variants

**Single Node OpenShift (SNO)** — full OCP on one node. Same APIs, same operators, same web console as multi-node OCP. Use cases:
    
      - Edge sites: cell towers, retail stores, factory floors, branch offices.

      - Compact deployments where the cost of 3+2 is unjustified.

      - Constrained sites: limited rack space / power / cooling.

    
    Trade-off: no zone redundancy; etcd is single-node (data resilience via storage backup, not quorum).
    **MicroShift** — even smaller (sub-1GB-RAM) variant of OCP for IoT gateways, ATMs, kiosks, embedded devices. Subset of OCP CRDs (Routes, OperatorHub not included; lighter API surface). Optimised for 100s-of-MB footprint + restart in seconds.
    **Local Zones** — AWS/Azure-style hyperscaler edge presence. ROSA on Local Zones extends ROSA into edge AWS metro POPs (Los Angeles, Boston, etc.) for ultra-low-latency to local users. Same OCP APIs; less round-trip to nearest data center.
    All three federate into **RHACM** for fleet-wide management (covered in O10): one console manages 800 SNOs, 1000 MicroShifts, and the central + Local Zones clusters.

## 4. Combining the three — AI inference at edge, VMs migrated to OCP

**VMware migration to OCP Virtualization**: **Migration Toolkit for Virtualization (MTV)** — Operator-based tool that ingests VMs from vSphere and converts them to KubeVirt VirtualMachines on OCP. Schedule batches; preserve IPs; minimal downtime. *Path-of-record for vSphere → OCP modernisation.*
    **AI inference at edge**: deploy KServe + small LLMs (e.g., Granite, Llama 3 8B) on SNO at the edge. Local inference reduces latency + privacy. RHACM pushes models to the fleet of SNOs.
    **RHEL AI on OCP**: RHEL AI is Red Hat's curated inference platform with IBM Granite models + InstructLab for fine-tuning. Hosted on OCP via OpenShift AI; enterprise-supported AI stack.
    **Specialty hardware:** SR-IOV + DPDK for network-intensive AI workloads; Confidential Computing (AMD SEV) for sensitive PHI training; CMEK for encryption at rest.

## Before / After

**Before.** Pre-OCP Virtualization, VMs and K8s lived in separate worlds. VMware for legacy + Windows; K8s for new microservices. Two control planes; two ops teams; two RBAC systems; two storage stacks. AI workloads needed bring-your-own Jupyter + KServe + GPU operator. Edge K8s was DIY — k3s/k0s/MicroK8s with no Red Hat support; or full OCP that didn't fit on small hardware.

**After.** OCP unifies: **VMs (KubeVirt) + containers + AI workloads + edge sites** on one platform. **OpenShift Virtualization** + **MTV** for VMware migration. **OpenShift AI** for ML platform (notebooks + KServe + Kubeflow + RHEL AI). **SNO + MicroShift + Local Zones** for edge variants. **RHACM** manages the fleet.

*One platform for VMs + containers + AI + edge. Modernise legacy VMs without big-bang rewrites; deploy AI inference where the data lives.*

## Analogy — the K-Foundry bay

The **Special Castings Wing** at K-Foundry handles the unusual products. Three specialty production lines.
    The **VM Casting Line** (OpenShift Virtualization / KubeVirt) makes VM-shaped products alongside the container-shaped ones. Same molds, same conveyors, same paint shop — but the output is a Windows server or RHEL VM instead of a container. The Migration Toolkit (MTV) takes vSphere-shaped products from the old foundry next door and recasts them as KubeVirt VMs.
    The **AI Lab Wing** (OpenShift AI / RHODS) handles ML workloads: scientist notebooks (Jupyter), model serving (KServe), pipelines (Kubeflow). Specialty heavy machinery (NVIDIA GPU Operator) for training; MIG to slice big GPUs into small ones; RHEL AI integration for productised inference.
    The **Branch Foundry Network** (Edge) extends the foundry to remote sites. Single Node OpenShift (SNO) at retail stores + cell sites; MicroShift at IoT / ATM / kiosk; Local Zones at hyperscaler edge POPs. RHACM (next bay) coordinates them all.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| VM Casting Line | OpenShift Virtualization (KubeVirt) |
| VM-shaped product | VirtualMachine (VM) CR + VirtualMachineInstance (VMI) |
| VM disk recipe | DataVolume CR |
| In-flight VM relocation | Live migration (VirtualMachineInstanceMigration CR) |
| Hot-attach a NIC / drive | Hot-plug NICs / disks on running VM |
| vSphere migration loader | Migration Toolkit for Virtualization (MTV) |
| AI Lab Wing | OpenShift AI (formerly RHODS) |
| Scientist notebook | Jupyter / JupyterLab / RStudio / VS Code on Pods |
| Model-serving turbine | KServe (Knative-based model serving) |
| ML workflow pipeline | Kubeflow Data Science Pipelines (DSP) |
| Distributed training rig | Kubeflow PyTorchJob / TFJob / MPIJob |
| Heavy-machinery manager | NVIDIA GPU Operator + MIG slicing |
| Productised inference platform | RHEL AI (Granite models + InstructLab) |
| Branch Foundry — full-OCP edge | Single Node OpenShift (SNO) |
| Branch Foundry — IoT/ATM | MicroShift (sub-GB OCP) |
| Hyperscaler edge POP | Local Zones (ROSA / OCP on AWS/Azure edge regions) |

⚠️ *Analogy stops here:* A real foundry has fixed casting lines; OCP's VM-and-container coexistence is software-defined. KubeVirt VMs share Pod scheduling + networking + storage primitives — the metaphor underplays the integration depth.

## ELI5 / ELI10

**ELI5.** The Special Wing makes three things alongside regular containers: VMs (with the same controls as containers), AI experiments (with notebooks + GPU + model serving), and edge sites (small foundries at remote locations). Same factory; specialty production lines.

**ELI10.** OCP Virtualization (KubeVirt) runs VMs as first-class CRs (VirtualMachine, DataVolume, live migration, hot-plug). MTV ingests VMware VMs. OpenShift AI = Jupyter notebooks + KServe model serving + Kubeflow Pipelines + distributed training + RHEL AI integration; NVIDIA GPU Operator + MIG. Edge = SNO (full OCP single node), MicroShift (sub-GB ultra-edge), Local Zones (hyperscaler edge). RHACM federates fleets.

## Real-world scenarios

- **Bank — VMware migration via MTV; 200 VMs in 6 months.** A bank with 200 legacy VMs on vSphere installs OpenShift Virtualization + MTV. 6-month migration: batch ingestion of VMs as VirtualMachine CRs; same network IPs preserved; minimal user-visible downtime. *VMware contract not renewed.*
- **ML team — OpenShift AI for enterprise model training.** An ML team needs on-prem training (PHI data; can't leave the data centre). OpenShift AI installed on a 4-node GPU cluster (H100). Notebooks for scientists; PyTorchJob for distributed training; KServe for inference. RHEL AI hosts production Granite-3 inference. *End-to-end ML platform without SaaS.*
- **Retail — SNO at 800 stores + RHACM.** Grocery chain runs OCP at 800 stores. Each store: 1 SNO node hosting POS + inventory + local AI inference (vision-based shelf monitoring). RHACM federates the fleet; new app rollout via Argo CD ApplicationSet → 800 stores in 30 minutes.
- **Telco — Local Zones for sub-10ms 5G core.** Telco running 5G UPF on ROSA in AWS Local Zones (Los Angeles, NYC, Chicago metros). Sub-10ms latency to local subscribers. Same OCP APIs as core ROSA cluster; deployed via RHACM Cluster Lifecycle.

## Common misconceptions

- **Myth:** "VMs in OCP are second-class — containers are the real deal."
  **Truth:** VirtualMachine CRs use the same Pod scheduling + networking + storage + RBAC + monitoring as containers. *VMs are first-class K8s workloads in OCP Virtualization.* Same kubectl/oc; same console; same Operators. Mixed workloads in the same cluster work cleanly.
- **Myth:** "OpenShift AI is just rebranded RHODS."
  **Truth:** **Yes** — Red Hat OpenShift Data Science (RHODS) was renamed to OpenShift AI. Same product evolution; expanded scope to include broader AI use cases beyond data science (LLM serving, RHEL AI integration). The brand changed; the platform continues.
- **Myth:** "SNO is just OCP on a small VM for testing."
  **Truth:** SNO is a **specific cluster topology**: full OCP control plane + worker on one node. Production-ready for edge use cases. Single etcd (no quorum); data resilience via storage backup. *Different from "OCP on small VM for testing" — designed for real edge production.*

## Recap

Three specialty production lines: VM (KubeVirt) + AI (RHODS / OpenShift AI) + Edge (SNO / MicroShift / Local Zones). MTV brings vSphere VMs in; RHACM federates the edge fleet.

**Next — O10: Multi-Cluster with ACM.** RHACM (Open Cluster Management) — ManagedClusters, Placement, ApplicationSets, Policy, ObservabilityAddon. Hosted Control Planes at scale; Submariner integration.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
