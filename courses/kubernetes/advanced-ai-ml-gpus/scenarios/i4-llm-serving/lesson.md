# K-ADV-AI I4 — I4 · LLM Serving — vLLM, TGI, Triton, NIM, llm-d

> Course: K-ADV-AI (advanced specialization)
> Module I4 · LLM Serving
> Companion preview: `/preview-kubernetes-adv-ai-lesson-04.html`.

---

**🎯 If you remember nothing else:** **vLLM = throughput + flexibility for open-source LLMs. Triton = multi-framework + production. NIM = NVIDIA-managed. TGI = HF-native. llm-d = K8s-native. Pick by model + ecosystem + ops appetite.**

## 1. PagedAttention + continuous batching

**vLLM**: open-source LLM serving from UC Berkeley + community. Two key innovations:
    
      - **PagedAttention**: KV-cache paged like virtual memory. Reduces memory waste from variable-length contexts; 2-4× higher throughput.

      - **Continuous batching**: requests batch dynamically (not fixed at start of decode); GPU utilization much higher.

    
    Models: Llama / Mistral / Qwen / Gemma / DeepSeek + custom. Quantization: AWQ / GPTQ / FP8. Distributed serving: tensor + pipeline + expert parallel.
    Best fit for most open-source LLM serving.

## 2. HF-native + multi-framework production

**TGI (Text Generation Inference)**: Hugging Face's server. Streaming + batching + flash attention. HF-ecosystem-native (any HF model just works). Less throughput than vLLM at peak but easier HF model integration.
    **NVIDIA Triton**: multi-framework production server. Supports TensorFlow, PyTorch, ONNX, TensorRT, custom Python backends. Concurrent model execution + dynamic batching + ensembles. Strong for non-LLM (CV / classical) + LLM via TensorRT-LLM backend.
    Pick: TGI for HF-native; Triton for multi-framework or non-LLM mix or TensorRT-optimised LLMs.

## 3. NVIDIA-managed + K8s-native

**NIM (NVIDIA Inference Microservice) Operator**: commercial NVIDIA-managed inference. Pre-optimised model containers (per GPU); operator deploys + autoscales + monitors. Trade self-host for vendor-managed perf + support.
    **llm-d**: K8s-native LLM serving framework (Red Hat + Google + community, 2024-2025). Built around K8s primitives — Service, Deployment, HPA + custom controllers for LLM-specific autoscaling (queue depth + KV-cache fullness). Newer; growing.
    Pick NIM if NVIDIA-managed perf + commercial support matters. Pick llm-d for K8s-native primitives + open-source.

## 4. model + serving runtime + autoscale

**Selection grid**:
    
      - *Open-source LLMs* (Llama / Mistral / Qwen): vLLM (default).

      - *Hugging Face ecosystem*: TGI.

      - *Multi-framework or TensorRT-LLM*: Triton.

      - *NVIDIA-managed perf + support*: NIM Operator.

      - *K8s-native primitives + open-source*: llm-d.

    
    **Tuning**: per-server batching + max sequence length + KV-cache size; quantization (AWQ / GPTQ / FP8) for smaller / faster; tensor parallel for large models across GPUs; KServe + ServingRuntime wraps the chosen server with autoscale + canary.

## Before / After

**Before.** Pre-vLLM, LLM serving used naive batching (fixed batch at start of decode); GPUs underutilized; latency tail high; KV-cache memory waste.

**After.** Modern: vLLM / TGI / Triton / NIM / llm-d. PagedAttention + continuous batching unlock 2-4× throughput. Pick server per model + ecosystem; KServe + ServingRuntime wraps for K8s autoscale + canary.

*LLM serving has matured into a competitive landscape; pick deliberately.*

## Analogy — the K-Observatory array

Model-Rendering Hall has five rendering stations. **vLLM** the high-throughput open-source easel — paged + continuous-batched. **TGI** the HF-ecosystem station. **Triton** the multi-framework production station. **NIM** the NVIDIA-managed gallery. **llm-d** the K8s-native easel. Pick by what you're rendering.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| High-throughput open-source easel | vLLM (PagedAttention + continuous batching) |
| HF-ecosystem station | TGI (Hugging Face text-generation-inference) |
| Multi-framework production station | NVIDIA Triton |
| NVIDIA-managed gallery | NIM Operator (commercial) |
| K8s-native easel | llm-d (K8s-native primitives) |
| Paint paging system | PagedAttention KV-cache |
| Continuous group rendering | Continuous batching |
| Compressed-paint mode | Quantization (AWQ / GPTQ / FP8) |

⚠️ *Analogy stops here:* A real easel is fixed; LLM servers evolve weekly with model architectures. Stay current; benchmark per workload.

## ELI5 / ELI10

**ELI5.** Five rendering stations for LLMs. Pick the right one for the model + ecosystem + ops appetite.

**ELI10.** **vLLM**: PagedAttention + continuous batching; open-source default. **TGI**: HF-native batching + streaming. **Triton**: multi-framework production; TensorRT-LLM backend. **NIM Operator**: NVIDIA-managed (commercial). **llm-d**: K8s-native framework. **Tuning**: batching, max-seq, quantization, tensor parallel.

## Real-world scenarios

- **Llama 3 serving on vLLM.** Team adopts vLLM for Llama 3 70B; tensor parallel across 4 H100s; AWQ quantized for memory; throughput 4× naive; KServe ServingRuntime wraps with autoscale.
- **Triton + TensorRT-LLM for production fleet.** Mixed-model fleet (LLM + CV + classifier). Triton serves all via single server; TensorRT-LLM optimises LLM perf. Single observability stack.
- **NIM for managed inference.** Compliance team wants NVIDIA-managed support. NIM Operator deploys pre-optimised models; commercial support; trade self-tune for vendor-managed.
- **Outage — KV-cache thrashing pre-vLLM.** Naive serving with long-context prompts; KV-cache OOM; latency spike. Postmortem: migrate to vLLM + PagedAttention; throughput + stability fixed.

## Common misconceptions

- **Myth:** "vLLM is faster for everything."
  **Truth:** vLLM is best for open-source LLMs at high throughput. For multi-framework or non-LLM mix, Triton wins. For HF model integration, TGI ergonomics.
- **Myth:** "Triton replaces vLLM."
  **Truth:** Triton + TensorRT-LLM backend competes for LLM serving but vLLM has innovations (PagedAttention, continuous batching) Triton matches differently. Test per workload.
- **Myth:** "NIM is just vLLM in a box."
  **Truth:** NIM is NVIDIA-curated container with optimised model + runtime + commercial support. Trade open-source flexibility for vendor-managed perf.

## Recap

Five LLM servers: vLLM (open-source default), TGI (HF-native), Triton (multi-framework), NIM (managed), llm-d (K8s-native). Pick by model + ecosystem + ops appetite. Wrap with KServe for autoscale + canary.

**Next — I5: AI Gateway / LLM Gateway patterns (Envoy AI Gateway, Kong AI Gateway).**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
