# K-GKE G8 — G8 · GKE Enterprise (Fleets) and AI/ML on GKE

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G8 · Enterprise (Fleets) and AI/ML
> Companion preview: `/preview-kubernetes-gke-lesson-08.html`.

---

**🎯 If you remember nothing else:** **Fleets unify policy + GitOps + mesh + multi-cluster ingress across GCP and beyond. AI/ML on GKE = JobSet + Kueue for batch; GPU Operator + MIG + TPU multi-host for compute; Inference Gateway + vLLM/NIM/Triton for serving. Use both pillars for production AI platforms.**

## 1. GKE Enterprise — Fleets, Config Sync, Policy Controller, CSM

**Fleet** = a logical grouping of GKE clusters (and Anthos-registered non-GKE clusters) under one governance plane. Register clusters with `gcloud container fleet memberships register`. Fleet enables:
    
      - **Config Sync** = continuous GitOps reconciliation. `RootSync` + `RepoSync` CRDs reconcile manifests from a Git repo into clusters. Drift detection on; manual edits reverted. Three repo patterns: per-tenant repos / per-environment repos / per-cluster repos. Replaces self-installed Argo CD or Flux.

      - **Policy Controller** = managed OPA Gatekeeper. Fleet-wide admission policies via Constraint templates; built-in baselines (Pod security standard, registry restriction, label requirements); custom Rego or CEL.

      - **Cloud Service Mesh (CSM)** = managed Istio across fleet members. *mTLS between Pods across clusters*; cross-fleet traffic management; service-to-service auth via SPIFFE identity. The Istio control plane is Google-operated; sidecars in each member cluster.

    
    **Connect Gateway** = run kubectl against any registered fleet cluster via the GCP control plane. No need to expose individual cluster apiserver IPs to humans; auth via GCP IAM; works for clusters behind NAT / on-prem / in other clouds.
    **Multi Cluster Ingress (MCI) / Multi Cluster Gateway (MCG)** (covered in G3) — single global anycast IP across fleet clusters; traffic to nearest healthy member; failover automatic.

## 2. GKE on AWS / Azure / VMware / bare metal (Anthos Multi-Cloud + on-prem)

GKE Enterprise extends GKE's management surface beyond GCP:
    
      - **GKE on AWS** — full GKE control plane running in the customer's AWS account. Same kubectl + Cloud Console + fleet experience. Workloads on EC2 instances; storage on EBS; networking on AWS VPC. *For multi-cloud teams who want one operational model.*

      - **GKE on Azure** — same as above for Azure. Workloads on Azure VMs.

      - **GKE on VMware** — Anthos clusters on customer's vSphere on-prem. Standardised K8s on the existing virtualisation estate.

      - **GKE on bare metal** — Anthos clusters directly on customer hardware (Intel / AMD x86 / ARM). For edge data centres + telco / industrial workloads.

    
    *All four* register into the same Fleet as native GCP GKE clusters → unified Config Sync, Policy Controller, CSM, observability. *One operational story across the entire K8s estate.*

## 3. AI/ML on GKE — JobSet, Kueue, GPU Operator, MIG, TPU multi-host, Ray

**Batch + scheduling**:
    
      - **JobSet API** — orchestrate sets of K8s Jobs together (success, failure, dependency). For multi-host distributed training: launch N Jobs simultaneously; coordinate ranks; handle failure as a unit.

      - **Kueue** — Kubernetes-native batch queueing. ClusterQueue + LocalQueue + Workload CRDs. Priority + preemption; quota borrowing across teams; preserves the K8s API. *The modern way to run batch on K8s.*

      - Combine: Kueue queues Workloads; admitted Workloads create JobSets; JobSets launch GPU/TPU Pods.

    
    **NVIDIA GPU Operator** — manages NVIDIA driver + container runtime + device plugin lifecycle on GPU node pools. Replaces the manual node-image driver-version juggling. Required for advanced features (MIG, NVLink, RDMA).
    **MIG (Multi-Instance GPU)** — slice a single H100 / H200 GPU into multiple smaller virtual GPUs (e.g., 7 × 10GB MIGs from one 80GB H100). Each MIG appears as `nvidia.com/mig-1g.10gb: 1` resource. Lets cost-effective inference share a high-end GPU across multiple Pods.
    **TPU multi-host** — TPU v5e+ pods span multiple node-host VMs sharing one logical TPU pod. Requires special node-pool topology (single VM = host; pod = multiple hosts) + workload integration via JobSet for coordinated launch. *Distributed training at TPU scale.*
    **Ray on GKE** — KubeRay operator manages Ray clusters as RayCluster CRDs. Train and serve large models with Ray's distributed primitives (Tasks, Actors, Datasets, Train, Serve). KubeRay handles head + worker Pod orchestration on GKE.

## 4. AI/ML inference — GKE Inference Gateway + vLLM / NVIDIA NIM / Triton

**GKE Inference Gateway** = an extension of the GKE Gateway API for AI inference. Model-aware routing: route requests by model name, prompt size, batching opportunity, prefix-cache hit. Supports KV-cache aware routing for transformer inference (route follow-up requests in the same conversation back to the same Pod with the warm KV cache). *Optimised cost-per-token for LLM serving.*
    **vLLM** — high-throughput LLM serving with PagedAttention + continuous batching. The de-facto choice for GPU inference of open-weights models (Llama / Mistral / Qwen / etc.). Runs as a Pod with model loaded into GPU memory. *Combine with Inference Gateway for production-scale serving.*
    **NVIDIA NIM** — NVIDIA-packaged inference microservice container. Pre-built for popular models with optimised kernels, TensorRT-LLM, Triton inside. Runs on GKE GPU node pools. NVIDIA-supported.
    **Triton Inference Server** — NVIDIA's general-purpose inference server. Multi-framework (TensorRT, ONNX, PyTorch, TensorFlow); multi-model; ensemble pipelines. Older-but-mature; NIM is the modern wrapper for LLMs.
    **End-to-end inference platform pattern**: Inference Gateway (model-aware routing) → vLLM Pods (GPU serving) on Compute Class Accelerator A4 H200 → Cloud Trace for end-to-end latency → SLO Monitoring with cost-per-token KPI joined from BQ. *Production AI inference platform on GKE.*

## Before / After

**Before.** Pre-fleet GKE multi-cluster ops = scripts looping kubectl. Pre-Config-Sync GitOps = self-installed Argo CD per cluster. Pre-Inference-Gateway, LLM serving needed manual model→Pod routing or naive HTTP load-balancing (which broke KV-cache locality). Pre-Kueue, batch on K8s was DIY queueing. Multi-cloud K8s = three different operational stories. AI/ML on K8s was assembly required.

**After.** Modern GKE Enterprise: **fleets** unify policy + GitOps + mesh across GCP/AWS/Azure/on-prem. **Config Sync + Policy Controller + CSM** are managed. **Connect Gateway** + MCI/MCG handle multi-cluster operations. **AI/ML platform pattern**: JobSet + Kueue for batch; GPU Operator + MIG + TPU multi-host + Ray for compute; Inference Gateway + vLLM / NIM / Triton for serving. *Production AI platform on GKE in weeks, not quarters.*

*Fleets are the unifier; AI/ML on GKE is the use case GKE was designed for from the start.*

## Analogy — the K-Garden plot

The **Research Greenhouse** is K-Garden's most ambitious building. Two wings.
    The **Multi-Garden Wing** (Fleets) connects this garden to dozens of others — same head-gardener manuals, same security guards, same seasonal calendar — even gardens hosted by other operators (AWS, Azure, on-prem). One Git repo (Config Sync) describes the standard practices; every garden in the network reconciles to it. The **Network Concierge** (Connect Gateway) lets a head gardener visit any garden via one badge. The **Sister-Garden Front Gates** (MCI/MCG) route visitors to the nearest healthy garden automatically.
    The **AI Lab Wing** handles the high-tech crops. *JobSet* + *Kueue* coordinate large batch experiments across plots. *NVIDIA GPU Operator* manages the heavy machinery; *MIG* slices an H100 microscope into seven smaller microscopes for budget experiments. *TPU multi-host* coordinates Google-designed accelerator pods across multiple host VMs for distributed training. *Ray* handles parallel orchestration.
    For *serving* trained models, the lab has the **Inference Gateway** — a model-aware concierge that routes requests by model name, prompt size, conversation history (KV-cache locality). The serving runtimes are *vLLM*, *NVIDIA NIM*, or *Triton* — each a specialty tool for inference at scale.

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| Multi-Garden Wing | GKE Enterprise (Fleets) |
| One Git repo for standard practices | Config Sync (RootSync + RepoSync) |
| House rules enforced at every gate | Policy Controller (managed Gatekeeper) |
| Encrypted notes between plants in any garden | Cloud Service Mesh fleet-wide |
| Network Concierge | Connect Gateway (kubectl across fleet) |
| Sister-Garden Front Gates | Multi-Cluster Ingress / Multi-Cluster Gateway |
| Other operators' gardens | GKE on AWS / Azure / VMware / bare metal |
| AI Lab Wing | AI/ML on GKE pillar |
| Coordinated batch experiments | JobSet API |
| Experiment queue | Kueue (ClusterQueue + LocalQueue + Workload) |
| Heavy-machinery manager | NVIDIA GPU Operator |
| H100 sliced into smaller microscopes | MIG (Multi-Instance GPU) |
| Coordinated TPU pod | TPU multi-host pods (TPU v5e+) |
| Parallel orchestration framework | Ray on GKE (KubeRay) |
| Model-aware concierge | GKE Inference Gateway (KV-cache aware routing) |
| Specialty inference rooms | vLLM / NVIDIA NIM / Triton on GKE |

⚠️ *Analogy stops here:* A research lab's equipment is fixed; AI/ML on GKE is rapidly evolving (Inference Gateway is recent; TPU + GPU SKUs change). The metaphor under-captures version-velocity in this space.

## ELI5 / ELI10

**ELI5.** There's a special wing that connects the garden to other gardens worldwide so they all use the same rules. There's also an AI lab with super-fast computers that train and serve smart models. Special staff route requests to the right model.

**ELI10.** GKE Enterprise (Fleets) = fleet of clusters (GKE + GKE-on-AWS/Azure/VMware/bare-metal); Config Sync for GitOps; Policy Controller for admission; Cloud Service Mesh fleet-wide mTLS; Connect Gateway for kubectl-across-clusters; MCI/MCG for multi-cluster ingress. AI/ML on GKE: JobSet + Kueue for batch; GPU Operator + MIG + TPU multi-host + Ray for compute; Inference Gateway + vLLM/NIM/Triton for serving.

## Real-world scenarios

- **Bank — fleet of 50 clusters under Config Sync + Policy Controller.** Bank registers 35 GKE + 10 GKE-on-AWS + 5 GKE-on-VMware clusters into a Fleet. Config Sync deploys uniform NetworkPolicies + PSA labels + RBAC bindings from one Git repo to all 50 clusters. Policy Controller blocks non-compliant Pods at admission everywhere. CSM provides cross-cluster mTLS. *One governance model across heterogeneous K8s.*
- **LLM inference platform — Inference Gateway + vLLM on A4 H200.** Team serves Llama 3 70B inference. **Inference Gateway** routes by model name + KV-cache locality (chats stick to the same Pod for cache reuse). **vLLM** Pods on Compute Class Accelerator with A4 H200. SLO: p95 first-token-latency < 500ms; cost-per-token tracked via BQ. *Throughput +60% vs naive routing thanks to KV-cache locality.*
- **ML training — Kueue + JobSet + TPU multi-host.** ML team runs distributed training jobs on TPU. Kueue ClusterQueue defines team quotas + priority; submit a Workload CR; admitted Workload creates a JobSet; JobSet launches a TPU multi-host pod with 4 hosts × 4 chips per host. Failed host = JobSet treats it as failure of the entire training run; Kueue requeues with priority. *Production batch ML platform; quota + priority + preemption all built-in.*
- **Ray on GKE for distributed feature engineering.** Data team has a 50TB feature engineering job. Deploy **RayCluster** via KubeRay on GKE Standard with Compute Class Scale-Out (T2D ARM, low cost-per-vCPU). Ray Tasks fan out to ~500 workers; Ray Datasets read from BigQuery; results stream to GCS. *Job completes in 18 min vs 4hr on a single VM. Cluster destroyed after job; per-second billing.*

## Common misconceptions

- **Myth:** "Fleets are just a name for grouping clusters in the GCP console."
  **Truth:** Fleets are an active control plane. Fleet membership enables fleet-scoped Config Sync, Policy Controller, CSM, Connect Gateway, MCI/MCG, fleet-default settings. *Capabilities, not just labels.* Without Fleet membership, those features don't apply.
- **Myth:** "Inference Gateway and regular Gateway API are the same."
  **Truth:** Inference Gateway is an extension of Gateway API specifically for AI inference. Adds model-aware routing (route by model name), KV-cache locality (route follow-up requests in a conversation to the same Pod), prompt-size routing (small prompts to high-throughput Pods, large prompts to large-memory Pods). Regular Gateway API doesn't know about model semantics.
- **Myth:** "vLLM, NIM, and Triton are interchangeable."
  **Truth:** **vLLM** = open-source LLM-specialised serving with PagedAttention + continuous batching; best for open-weights LLMs at scale. **NIM** = NVIDIA-packaged inference microservice; pre-built for popular models with TensorRT-LLM optimisations + Triton inside; NVIDIA-supported with NVIDIA enterprise license. **Triton** = NVIDIA general-purpose inference server (older-but-mature, multi-framework, not LLM-specific). Pick vLLM for community LLMs at scale; NIM for vendor-supported LLMs; Triton for general-purpose multi-framework inference (CV / classical ML).

## Recap

Two pillars: GKE Enterprise (Fleets) for cross-cluster + multi-cloud governance; AI/ML on GKE for batch (JobSet/Kueue) + accelerators (GPU Operator/MIG/TPU/Ray) + serving (Inference Gateway + vLLM/NIM/Triton).

**Next — G9: GKE Troubleshooting (GCP-Specific).** IAM/RBAC mismatch, WIF token issues, Autopilot admission rejection, Node pool / MIG failures, IP exhaustion, NEG health-check failures, Ingress provisioning, firewall blocks, Cloud NAT/SNAT, DNS, storage attach, release channel / maintenance exclusion issues, gcpdiag, GKE Recommender, Logs Explorer.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
