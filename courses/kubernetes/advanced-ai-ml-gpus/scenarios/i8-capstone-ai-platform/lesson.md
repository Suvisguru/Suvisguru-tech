# K-ADV-AI I8 — I8 · Capstone — Production AI Inference Platform

> Course: K-ADV-AI (advanced specialization)
> Module I8 · Capstone AI Platform
> Companion preview: `/preview-kubernetes-adv-ai-lesson-08.html`.

---

**🎯 If you remember nothing else:** **Operating Observatory: GPU + DRA + Kueue + Volcano + KServe + vLLM + AI Gateway + RDMA + JuiceFS + OCI artifacts + multi-tenant + Spot + chargeback. Every K-ADV-AI concept woven into one production AI inference platform.**

## 1. GPU + Kueue + Volcano + MIG

**GPU pools**: H100 (training + large LLM), A100 (training + medium LLM), L40 / G5 (inference + light LLM), Spot G6 (fault-tolerant batch). DRA + MIG enabled cluster-wide.
    **Kueue + Volcano**: per-team ClusterQueue with cohort lending; gang scheduling for distributed training; MultiKueue federates training across regions for capacity.
    **Per-tenant Quota**: gold (10 H100) / silver (4) / bronze (1); MIG-sized inference quotas (1g.10gb).

## 2. KServe + vLLM + Kubeflow + KubeRay

**Inference**: KServe InferenceService wrapping vLLM ServingRuntime for LLMs; Triton ServingRuntime for non-LLM; autoscale via Knative or HPA.
    **Training**: Kubeflow Training Operator (PyTorchJob / TFJob / MPIJob); Kubeflow Pipelines for DAGs; Katib for HPO; Model Registry for versioning.
    **Distributed compute**: KubeRay (Ray Train / Tune / RLlib) for distributed Python.
    **Multi-pod jobs**: JobSet primitive integrated with Kueue + Volcano.

## 3. AI Gateway + RDMA / EFA + JuiceFS + OCI

**AI Gateway**: Envoy AI Gateway in front of all LLM serving. Per-tenant token rate limit + cost budget; safety filters (Llama Guard); semantic cache (Redis + embedding); multi-provider failover (local LLM ↔ OpenAI ↔ Anthropic).
    **RDMA / EFA**: H100 nodes interconnected via EFA on AWS / IB on-prem. Distributed training collective ops at line rate.
    **GPUDirect Storage + JuiceFS**: large datasets streamed direct to GPU; models cached cluster-wide via JuiceFS.
    **OCI artifacts**: models + SBOM + Cosign signature in Harbor registry; pulled via init-container.

## 4. Multi-tenant + Spot + chargeback + observability + runbooks

**Multi-tenant**: namespace + RBAC + NetPol + Quota + MIG isolation per K-ADV-SEC; AI Gateway per-tenant token budget.
    **Cost**: Spot fleet for fault-tolerant batch; Kubecost per-tenant chargeback; budget alerts; idle reclaim; right-sizing campaigns.
    **Observability**: DCGM metrics + Prometheus; per-Service KServe metrics (TTFT / TPOT / queue / cache hit); LLM-specific tracing via OpenTelemetry; Grafana / Datadog dashboards in Backstage per service.
    **Runbooks**: GPU-OOM; KV-cache exhaustion; collective op latency; AI Gateway rate limit hit; Spot interruption cascade. Tested via quarterly game days.

## Before / After

**Before.** Pre-capstone: bespoke ML setups; per-team GPU sprawl; no quota; no isolation; no AI Gateway; cost surprises; outages frequent.

**After.** Operating Observatory: every K-ADV-AI concept woven. Multi-tenant ML platform with GPU sharing + Kueue admission + KServe inference + AI Gateway + RDMA fabric + Spot + chargeback. New tenant in < 1 day; SLA met; cost controlled.

*The architecture is the assembly; the operational rhythm is the discipline.*

## Analogy — the K-Observatory array

The Operating Observatory is K-Observatory at scale. Every telescope (GPU) is multi-tenant via MIG eyepieces; every astronomer's session is queue-managed (Kueue + Volcano); inference goes through the Triage Desk (AI Gateway); collective observations use the Optical Fiber Network (RDMA / EFA); the Cache Room (JuiceFS) holds star maps; the Sharing Committee bills per group + reclaims idle telescopes.
    The Master Astronomer (you) reviews monthly cost reports + quarterly SLO retros + game-day exercises.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Telescope farm + eyepieces | GPU pools + MIG |
| Astronomer queue + admission | Kueue + Volcano |
| Research-hall workshops | KubeRay + Kubeflow |
| Rendering halls | KServe + vLLM |
| Triage desk | AI Gateway (Envoy AI) |
| Optical fibers | RDMA / EFA / IB |
| Shared star-map cache | JuiceFS / Alluxio |
| Catalogue cards | OCI artifacts (models) |
| Sharing Committee + bills | Multi-tenant Quota + chargeback |

⚠️ *Analogy stops here:* A real observatory has fixed assets; AI infra evolves continuously — new GPU models, new servers, new gateways. The capstone is a snapshot.

## ELI5 / ELI10

**ELI5.** Big telescope farm + queue + research labs + rendering halls + triage desk + fast wires + shared cache + catalogue + bills + drills. Every piece works together.

**ELI10.** **Capacity**: GPU + DRA + GPU Operator + MIG. **Scheduling**: Kueue + Volcano + MultiKueue. **ML stack**: KubeRay + Kubeflow + KServe + JobSet. **Serving**: vLLM + Triton + NIM. **L7**: AI Gateway. **Fabric**: RDMA / EFA + GPUDirect Storage. **Storage**: JuiceFS / Alluxio. **Distribution**: OCI artifacts. **Governance**: multi-tenant Quota + MIG isolation + Spot + chargeback. **Ops**: DCGM + Prometheus + per-service dashboards + runbooks + game days.

## Real-world scenarios

- **Production launch — 10K rps with full stack.** LLM platform launches: vLLM behind KServe behind Envoy AI Gateway; H100 fleet with MIG for inference; Kueue admission; semantic cache; multi-provider failover. Day-1 SLA met; per-tenant chargeback in P&L.
- **Multi-region failover via MultiKueue.** us-east-1 GPU capacity exhausted; MultiKueue routes new training jobs to eu-west-1 H100 pool; tenants see no service interruption.
- **Cost optimisation campaign.** Quarterly review: top spenders right-sized via MIG; fault-tolerant training migrated to Spot; aggregate GPU bill dropped 35%.
- **Game day — Spot interruption cascade.** Simulated mass Spot reclaim; checkpointing + Kueue requeue + MultiKueue failover absorbed gracefully. Runbook validated.

## Common misconceptions

- **Myth:** "This is over-engineered for < 10 GPU clusters."
  **Truth:** Some pieces (DRA, MIG, AI Gateway, JuiceFS) earn at small scale. Skip what isn't needed; adopt as scale + tenancy + cost demands.
- **Myth:** "AI infra is fundamentally different from K8s."
  **Truth:** AI infra extends K8s via operators + plugins. Same K8s primitives + AI-specific extensions. K8s is the substrate.
- **Myth:** "Once built, the platform runs itself."
  **Truth:** Operational rhythm (game days + cost reviews + dashboards) is non-optional. Without rhythm, AI infra rots fast.

## Recap

Capstone: GPU + DRA + MIG + Kueue + Volcano + KubeRay + Kubeflow + KServe + vLLM + AI Gateway + RDMA / EFA + JuiceFS + OCI artifacts + multi-tenant Quota + Spot + chargeback + observability + runbooks. Production AI inference platform.

**K-ADV-AI complete.** 8 modules. From GPU + DRA (I1) to operating observatory (I8). Next K-ADV: *K-ADV-DR* (K-Lifeboat) — disaster recovery + business continuity.

## Flashcards and quiz

See `flashcards.yaml` (5 cards) and `quiz.yaml` (3 questions).
