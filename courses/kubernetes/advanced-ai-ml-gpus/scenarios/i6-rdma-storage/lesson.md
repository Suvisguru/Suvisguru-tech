# K-ADV-AI I6 — I6 · RDMA / EFA + Storage Throughput + JuiceFS / Alluxio + OCI Artifacts

> Course: K-ADV-AI (advanced specialization)
> Module I6 · RDMA + Storage
> Companion preview: `/preview-kubernetes-adv-ai-lesson-06.html`.

---

**🎯 If you remember nothing else:** **RDMA / EFA = required fabric for distributed training. GPUDirect Storage = NVMe → GPU bypasses CPU. JuiceFS / Alluxio = shared model cache. OCI artifacts = standardised model distribution.**

## 1. Low-latency GPU-to-GPU interconnect

**RDMA** (Remote Direct Memory Access): NIC writes directly to remote GPU memory; no CPU + kernel hop. **EFA** (AWS Elastic Fabric Adapter): AWS's RDMA-equivalent on p5 / hpc7g instances. **InfiniBand** (NVIDIA Quantum-2): on-prem fabric.
    Win for distributed training: collective ops (all-reduce / all-gather) latency drops 10×; large-model training throughput stays at scale.
    K8s setup: per-node RDMA device plugin advertises `nvidia.com/efa` or `rdma/hca`; Pods request via `resources.limits`; container image uses NCCL with EFA / IB transport.

## 2. NVMe / S3 → GPU memory; bypass CPU

**GPUDirect Storage (GDS)**: NVMe or S3 reads land directly in GPU memory; no host bounce. Throughput rises 2-3× for IO-bound training.
    Setup: NVIDIA driver + GPUDirect Storage library + supported filesystem (BeeGFS / WekaIO / DDN EXAScaler / Lustre). Use cases: large dataset streaming during training; checkpoint write / restore.

## 3. Distributed shared model cache

Loading a 70B model from S3 every Pod restart = ~10 minutes per Pod. **JuiceFS / Alluxio**: per-cluster distributed cache between S3 + Pods. Load once; cache locally; subsequent Pod restarts hit cache (sub-minute).
    **JuiceFS**: POSIX-compatible distributed FS with object-storage backend. **Alluxio**: data orchestration layer; caches across nodes; supports many backends. Both K8s-native via DaemonSet + PVC.

## 4. Models as OCI images; standardised tooling

**OCI artifacts**: models packaged as OCI images (modelpacks) + pushed to OCI registries (ECR / GCR / Harbor). Same registry / signing / SBOM / VEX pipeline as container images.
    Tools: **ORAS** (OCI Registry As Storage), **KitOps** (modelpack standard), **Sigstore** for model signing. Pull via **oras pull** or via init-container in Pod.
    Wins: *standardised distribution*; *signing + provenance*; *caching via registry mirror*; *versioned*.

## Before / After

**Before.** Pre-RDMA + GDS + cache + OCI: distributed training over TCP (slow); models loaded from S3 every Pod restart; bespoke distribution + verification.

**After.** RDMA / EFA fabric for collectives; GPUDirect Storage for IO; JuiceFS / Alluxio for shared model cache; OCI artifacts for distribution. AI infra at scale.

*AI workloads have unique fabric + storage needs; standard K8s infra alone underperforms.*

## Analogy — the K-Observatory array

Signal Lines run between every telescope (GPU) + every storage vault (NVMe / S3 / model cache). **RDMA / EFA**: dedicated low-latency optical fibers between telescopes — astronomers compare observations in real-time. **GPUDirect Storage**: direct pneumatic tubes from vault to telescope — bypass the central registry. **JuiceFS / Alluxio**: shared cache room — load model maps once, every astronomer reads from cache. **OCI artifacts**: standard catalogue cards for every model in the OCI library.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Optical fibers between telescopes | RDMA / EFA / InfiniBand |
| Pneumatic tubes vault → telescope | GPUDirect Storage |
| Shared cache room | JuiceFS / Alluxio |
| Standard catalogue cards | OCI artifacts (modelpacks) |
| Cache + sign tool | ORAS / KitOps / Sigstore |
| Vault file system | BeeGFS / WekaIO / Lustre / DDN |

⚠️ *Analogy stops here:* A real fabric is fiber; RDMA / GDS / cache are software + driver + hardware combined. Verify with NCCL benchmarks (nccl-tests).

## ELI5 / ELI10

**ELI5.** High-speed signal lines between telescopes; direct vault-to-telescope tubes; shared cache rooms; standardised catalogue cards. AI needs these; standard K8s infra alone is too slow.

**ELI10.** **RDMA / EFA / InfiniBand**: low-latency GPU-to-GPU; collective ops 10× faster. **GPUDirect Storage**: NVMe / S3 → GPU memory bypassing CPU. **JuiceFS / Alluxio**: distributed model cache; load-once cache-everywhere. **OCI artifacts**: models in OCI registry; standardised signing + caching.

## Real-world scenarios

- **EFA for Llama 3 training.** 32 H100 distributed training migrated from TCP to AWS EFA. NCCL benchmarks: all-reduce latency 10×; training throughput 2× at same GPU count.
- **JuiceFS shared model cache.** Pre-cache: 70B model from S3 every Pod restart ~10 min. Post-JuiceFS: cache hit ~30s. Inference scaling-out time dropped accordingly.
- **OCI model artifacts via Sigstore.** Models pushed as OCI artifacts to Harbor; Cosign-signed; pulled by Pods via init-container. Same supply-chain pipeline as container images. Compliance evidence reused.
- **Outage — collective op latency.** Pre-RDMA: distributed training slowed unpredictably during peak network use. Postmortem: dedicate RDMA fabric for AI; segregate from general K8s traffic.

## Common misconceptions

- **Myth:** "Standard K8s networking is enough for AI."
  **Truth:** Distributed training collectives over TCP are 5-10× slower than RDMA. At 100+ GPU scale, RDMA isn't optional.
- **Myth:** "GPUDirect Storage is for one filesystem."
  **Truth:** GDS supports many filesystems (BeeGFS / WekaIO / Lustre / DDN). Not all support equally; benchmark per workload.
- **Myth:** "OCI artifacts are just for containers."
  **Truth:** OCI 1.1 referrers + ORAS make OCI registries general-purpose for any artifact. Models, SBOMs, attestations, Helm charts all use OCI.

## Recap

AI fabric: RDMA / EFA / IB. AI storage: GPUDirect Storage + JuiceFS / Alluxio. AI distribution: OCI artifacts. These are the AI-specific infra; standard K8s alone underperforms at 100+ GPU scale.

**Next — I7: GPU sharing + multi-tenant + cost optimization.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
