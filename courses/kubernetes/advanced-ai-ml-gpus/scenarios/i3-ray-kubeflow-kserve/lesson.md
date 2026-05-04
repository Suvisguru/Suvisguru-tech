# K-ADV-AI I3 — I3 · Ray + Kubeflow + KServe + JobSet

> Course: K-ADV-AI (advanced specialization)
> Module I3 · Ray + Kubeflow + KServe
> Companion preview: `/preview-kubernetes-adv-ai-lesson-03.html`.

---

**🎯 If you remember nothing else:** **KubeRay = distributed compute. Kubeflow = training + pipelines + HPO. KServe = inference. JobSet = multi-pod jobs. Pick by ML phase; integrate via Kueue / Volcano for batch admission + gang.**

## 1. Ray on K8s — distributed compute primitive

**Ray**: distributed Python framework. **KubeRay** operator: `RayCluster` (long-running cluster), `RayJob` (one-shot), `RayService` (serving).
    Use cases: distributed training (Ray Train); reinforcement learning (RLlib); hyperparameter tuning (Ray Tune); generic distributed Python (Ray Core); LLM serving (Ray Serve / vLLM).
    Pattern: data scientist writes Python; KubeRay materialises Ray cluster; auto-scales workers; jobs submit + run.

## 2. Training operators + Pipelines + Notebooks + HPO

**Kubeflow Training Operator**: PyTorchJob / TFJob / MPIJob / XGBoostJob / PaddleJob — distributed training across Pods.
    **Kubeflow Pipelines**: workflow engine (Argo-based). DAGs of training / preprocessing / evaluation.
    **Kubeflow Notebooks**: per-user Jupyter / VSCode in K8s with PVCs + GPU.
    **Katib**: hyperparameter tuning (random / Bayesian / NAS); spawns trial Pods.
    **Model Registry**: versioned model artifacts; integrates with KServe.

## 3. Inference with InferenceService + autoscaling + canary

**KServe**: K8s-native inference platform. `InferenceService` CRD declares predictor (e.g., vLLM / Triton / TensorFlow Serving) + transformer + explainer.
    Autoscaling via Knative serverless OR HPA. Canary traffic split per InferenceService revision (10% canary → 100%). Multi-model serving + custom protocols.
    Integrates with Model Registry for versioned model rollout. ServingRuntime CRD bundles per-framework runtime templates.

## 4. multi-pod jobs primitive

**JobSet** (K8s SIG): replaces the legacy ParallelMaster pattern. Declares N replicaJobs (each a Job spec) + completionMode + failurePolicy. Designed for distributed training, MPI, gang-scheduled batch.
    Integrates with Kueue (admission) + Volcano (gang scheduling). Common pattern: PyTorchJob / RayJob → JobSet → Pods.
    JobSet controller GA-ready in K8s 1.32+. Replaces bespoke per-framework job management for multi-pod workloads.

## Before / After

**Before.** Pre-K8s-native ML tooling, ML workflows ran on bespoke VMs / Slurm / EC2 + boto3. Pipelines hand-orchestrated; serving = Flask app + Nginx; HPO bespoke. Data scientists were also infra engineers.

**After.** Modern: KubeRay for distributed compute; Kubeflow for training + pipelines + HPO + Notebooks; KServe for inference; JobSet for multi-pod jobs. Data scientists write Python / YAML; platform handles the rest.

*K8s-native ML tooling lets data scientists be data scientists.*

## Analogy — the K-Observatory array

Research Hall has four equipment kits. **KubeRay**: distributed-computation rig — many CPUs / GPUs cooperating on one task. **Kubeflow**: framework-specific tooling — PyTorch / TF / MPI training operators + pipelines + Notebooks + HPO. **KServe**: serving counter — production inference with autoscale + canary. **JobSet**: multi-pod-job primitive — the K8s-native foundation for the others.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Distributed-computation rig | KubeRay (RayCluster / RayJob / RayService) |
| PyTorch training operator | Kubeflow PyTorchJob |
| TF training operator | Kubeflow TFJob |
| MPI training operator | Kubeflow MPIJob |
| Pipeline DAG engine | Kubeflow Pipelines |
| Per-user Jupyter | Kubeflow Notebooks |
| HPO sweep engine | Katib |
| Inference counter | KServe InferenceService |
| Multi-pod-job primitive | JobSet |

⚠️ *Analogy stops here:* A research lab has fixed bench layout; K8s ML tooling evolves continuously — new operators, new servers, new gang patterns. Stay current.

## ELI5 / ELI10

**ELI5.** Four kits in the research hall. One for distributed compute, one for training, one for serving, one for multi-pod jobs. Pick the right kit for the right ML phase.

**ELI10.** **KubeRay**: Ray on K8s; RayCluster + RayJob + RayService. **Kubeflow**: Training Operator (PyTorchJob / TFJob / MPIJob) + Pipelines + Notebooks + Katib + Model Registry. **KServe**: InferenceService with autoscale + canary; ServingRuntime templates. **JobSet**: K8s SIG primitive for multi-pod jobs.

## Real-world scenarios

- **KubeRay distributed training.** Ray Train scaled across 32 H100s via KubeRay. Data scientist writes Ray Train script; KubeRay materialises cluster; auto-scaling workers; checkpoints to S3.
- **Kubeflow Pipelines for ETL → train → eval.** Daily DAG: data prep → PyTorchJob train → Katib HPO → eval → Model Registry → KServe deploy. Pipeline runs unattended; failures alarm.
- **KServe canary rollout.** New model version deployed as KServe revision; 10% canary; observability shows latency + accuracy; auto-promote at 24h SLO pass.
- **Outage — non-K8s-native ML rolled out manually.** Pre-Kubeflow team manually rolled inference; canary scripts buggy; latency spike rolled out to 100% before noticed. Postmortem: KServe canary + auto-rollback.

## Common misconceptions

- **Myth:** "Pick one ML framework; ignore others."
  **Truth:** Most orgs use multiple — PyTorch for research, TF for serving, MPI for HPC, Ray for distributed Python. Kubeflow + KubeRay supports all; pick per workload.
- **Myth:** "KServe is just an Ingress for ML."
  **Truth:** KServe adds: framework-specific predictors, autoscaling (Knative or HPA), canary, multi-model serving, custom protocols, model registry integration. Ingress alone is missing all of that.
- **Myth:** "JobSet is too new."
  **Truth:** K8s 1.32+ stable. SIG-Apps mature; foundation for next-gen multi-pod jobs.

## Recap

KubeRay = distributed compute. Kubeflow = training + pipelines + HPO + Notebooks + Model Registry. KServe = inference with autoscale + canary. JobSet = multi-pod jobs primitive. Combine via Kueue + Volcano.

**Next — I4: LLM serving (vLLM / TGI / Triton / NIM / llm-d).**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
