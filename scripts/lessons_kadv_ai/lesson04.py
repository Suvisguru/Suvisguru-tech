"""K-ADV-AI I4 — LLM serving (vLLM / TGI / Triton / NIM / llm-d)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LLM serving — vLLM TGI Triton NIM llm-d."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Model-Rendering Hall · K-Observatory — five LLM servers; pick by needs</text><rect x="40" y="70" width="130" height="100" rx="10" fill="#3F4A5E"/><text x="105" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">vLLM</text><text x="105" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">PagedAttn + cont.batching</text><rect x="190" y="70" width="130" height="100" rx="10" fill="#5DCAA5"/><text x="255" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">TGI (HF)</text><text x="255" y="108" text-anchor="middle" font-size="9" fill="#1F2433">HF text-generation-inference</text><rect x="340" y="70" width="130" height="100" rx="10" fill="#FF9900"/><text x="405" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Triton</text><text x="405" y="108" text-anchor="middle" font-size="9" fill="#1F2433">multi-framework</text><rect x="490" y="70" width="130" height="100" rx="10" fill="#5A6B81"/><text x="555" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">NIM Operator</text><text x="555" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">NVIDIA-managed</text><rect x="640" y="70" width="80" height="100" rx="10" fill="#A04832"/><text x="680" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">llm-d</text><text x="680" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">K8s-native</text></svg>"""


LESSON = LessonSpec(
    num="04", title_short="LLM serving", title_full="I4 · LLM Serving — vLLM, TGI, NVIDIA Triton, NIM Operator, llm-d",
    title_html="K-ADV-AI I4 · LLM Serving", module_eyebrow="Module I4 · Model-Rendering Hall — five LLM servers; pick by needs",
    hero_sub_html='<strong>vLLM</strong>: PagedAttention + continuous batching; high-throughput open-source; widely adopted. <strong>TGI</strong> (Hugging Face text-generation-inference): batch + streaming; HF-ecosystem-native. <strong>NVIDIA Triton</strong>: multi-framework (TF / PyTorch / ONNX / TensorRT); production-grade. <strong>NIM Operator</strong>: NVIDIA-managed inference (commercial). <strong>llm-d</strong>: K8s-native LLM serving framework (newer); built around K8s scaling primitives.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. LLM inference latency P99 5×; GPU memory exhausted; KV-cache thrashing. <em>Wrong server choice (or wrong tuning) for the workload</em>. Today\'s lesson: pick the right LLM server + understand PagedAttention + continuous batching.",
    stamp_html="<strong>vLLM = throughput + flexibility for open-source LLMs. Triton = multi-framework + production. NIM = NVIDIA-managed. TGI = HF-native. llm-d = K8s-native. Pick by model + ecosystem + ops appetite.</strong>",
    district_pin="kai-array04", district_label="Model-Rendering Hall",
    sections=[
        Section(eyebrow="Section 1.1 · vLLM",
            h2="PagedAttention + continuous batching",
            body_html="""    <p><strong>vLLM</strong>: open-source LLM serving from UC Berkeley + community. Two key innovations:</p>
    <ul>
      <li><strong>PagedAttention</strong>: KV-cache paged like virtual memory. Reduces memory waste from variable-length contexts; 2-4× higher throughput.</li>
      <li><strong>Continuous batching</strong>: requests batch dynamically (not fixed at start of decode); GPU utilization much higher.</li>
    </ul>
    <p>Models: Llama / Mistral / Qwen / Gemma / DeepSeek + custom. Quantization: AWQ / GPTQ / FP8. Distributed serving: tensor + pipeline + expert parallel.</p>
    <p>Best fit for most open-source LLM serving."""),
        Section(eyebrow="Section 1.2 · TGI + Triton",
            h2="HF-native + multi-framework production",
            body_html="""    <p><strong>TGI (Text Generation Inference)</strong>: Hugging Face\'s server. Streaming + batching + flash attention. HF-ecosystem-native (any HF model just works). Less throughput than vLLM at peak but easier HF model integration.</p>
    <p><strong>NVIDIA Triton</strong>: multi-framework production server. Supports TensorFlow, PyTorch, ONNX, TensorRT, custom Python backends. Concurrent model execution + dynamic batching + ensembles. Strong for non-LLM (CV / classical) + LLM via TensorRT-LLM backend.</p>
    <p>Pick: TGI for HF-native; Triton for multi-framework or non-LLM mix or TensorRT-optimised LLMs."""),
        Section(eyebrow="Section 1.3 · NIM Operator + llm-d",
            h2="NVIDIA-managed + K8s-native",
            body_html="""    <p><strong>NIM (NVIDIA Inference Microservice) Operator</strong>: commercial NVIDIA-managed inference. Pre-optimised model containers (per GPU); operator deploys + autoscales + monitors. Trade self-host for vendor-managed perf + support.</p>
    <p><strong>llm-d</strong>: K8s-native LLM serving framework (Red Hat + Google + community, 2024-2025). Built around K8s primitives — Service, Deployment, HPA + custom controllers for LLM-specific autoscaling (queue depth + KV-cache fullness). Newer; growing.</p>
    <p>Pick NIM if NVIDIA-managed perf + commercial support matters. Pick llm-d for K8s-native primitives + open-source."""),
        Section(eyebrow="Section 1.4 · selection + tuning playbook",
            h2="model + serving runtime + autoscale",
            body_html="""    <p><strong>Selection grid</strong>:</p>
    <ul>
      <li><em>Open-source LLMs</em> (Llama / Mistral / Qwen): vLLM (default).</li>
      <li><em>Hugging Face ecosystem</em>: TGI.</li>
      <li><em>Multi-framework or TensorRT-LLM</em>: Triton.</li>
      <li><em>NVIDIA-managed perf + support</em>: NIM Operator.</li>
      <li><em>K8s-native primitives + open-source</em>: llm-d.</li>
    </ul>
    <p><strong>Tuning</strong>: per-server batching + max sequence length + KV-cache size; quantization (AWQ / GPTQ / FP8) for smaller / faster; tensor parallel for large models across GPUs; KServe + ServingRuntime wraps the chosen server with autoscale + canary."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="What does PagedAttention solve?",
            options=[("Network bandwidth.", False), ("KV-cache memory waste from variable-length contexts; enables higher throughput.", True), ("CPU bottleneck.", False)],
            feedback="PagedAttention pages KV-cache memory; reduces fragmentation; 2-4× throughput. Foundation of vLLM\'s perf."),
        3: PauseCheck(question="Pick LLM server for an open-source Llama model with high throughput required.",
            options=[("Triton.", False), ("vLLM (PagedAttention + continuous batching).", True), ("NIM (commercial).", False)],
            feedback="vLLM is the open-source default for high-throughput LLM serving."),
    },
    before_after_before='<p>Pre-vLLM, LLM serving used naive batching (fixed batch at start of decode); GPUs underutilized; latency tail high; KV-cache memory waste.</p>',
    before_after_after='<p>Modern: vLLM / TGI / Triton / NIM / llm-d. PagedAttention + continuous batching unlock 2-4× throughput. Pick server per model + ecosystem; KServe + ServingRuntime wraps for K8s autoscale + canary.</p>',
    before_after_caption='<p class="ba-caption"><em>LLM serving has matured into a competitive landscape; pick deliberately.</em></p>',
    analogy_intro_html='''<p>Model-Rendering Hall has five rendering stations. <strong>vLLM</strong> the high-throughput open-source easel — paged + continuous-batched. <strong>TGI</strong> the HF-ecosystem station. <strong>Triton</strong> the multi-framework production station. <strong>NIM</strong> the NVIDIA-managed gallery. <strong>llm-d</strong> the K8s-native easel. Pick by what you\'re rendering.</p>''',
    translation_rows=[
        ("High-throughput open-source easel", "vLLM (PagedAttention + continuous batching)"),
        ("HF-ecosystem station", "TGI (Hugging Face text-generation-inference)"),
        ("Multi-framework production station", "NVIDIA Triton"),
        ("NVIDIA-managed gallery", "NIM Operator (commercial)"),
        ("K8s-native easel", "llm-d (K8s-native primitives)"),
        ("Paint paging system", "PagedAttention KV-cache"),
        ("Continuous group rendering", "Continuous batching"),
        ("Compressed-paint mode", "Quantization (AWQ / GPTQ / FP8)"),
    ],
    analogy_stops="A real easel is fixed; LLM servers evolve weekly with model architectures. Stay current; benchmark per workload.",
    eli5="Five rendering stations for LLMs. Pick the right one for the model + ecosystem + ops appetite.",
    eli10="<strong>vLLM</strong>: PagedAttention + continuous batching; open-source default. <strong>TGI</strong>: HF-native batching + streaming. <strong>Triton</strong>: multi-framework production; TensorRT-LLM backend. <strong>NIM Operator</strong>: NVIDIA-managed (commercial). <strong>llm-d</strong>: K8s-native framework. <strong>Tuning</strong>: batching, max-seq, quantization, tensor parallel.",
    scenarios=[
        Scenario(name="Llama 3 serving on vLLM", body="Team adopts vLLM for Llama 3 70B; tensor parallel across 4 H100s; AWQ quantized for memory; throughput 4× naive; KServe ServingRuntime wraps with autoscale."),
        Scenario(name="Triton + TensorRT-LLM for production fleet", body="Mixed-model fleet (LLM + CV + classifier). Triton serves all via single server; TensorRT-LLM optimises LLM perf. Single observability stack."),
        Scenario(name="NIM for managed inference", body="Compliance team wants NVIDIA-managed support. NIM Operator deploys pre-optimised models; commercial support; trade self-tune for vendor-managed."),
        Scenario(name="Outage — KV-cache thrashing pre-vLLM", body="Naive serving with long-context prompts; KV-cache OOM; latency spike. Postmortem: migrate to vLLM + PagedAttention; throughput + stability fixed."),
    ],
    misconceptions=[
        Misconception(myth="\"vLLM is faster for everything.\"", truth="vLLM is best for open-source LLMs at high throughput. For multi-framework or non-LLM mix, Triton wins. For HF model integration, TGI ergonomics."),
        Misconception(myth="\"Triton replaces vLLM.\"", truth="Triton + TensorRT-LLM backend competes for LLM serving but vLLM has innovations (PagedAttention, continuous batching) Triton matches differently. Test per workload."),
        Misconception(myth="\"NIM is just vLLM in a box.\"", truth="NIM is NVIDIA-curated container with optimised model + runtime + commercial support. Trade open-source flexibility for vendor-managed perf."),
    ],
    flashcards=[
        Flashcard(front="vLLM\'s two key innovations?", back="<strong>PagedAttention</strong> (KV-cache paged like virtual memory; reduces fragmentation) + <strong>continuous batching</strong> (requests batch dynamically; higher GPU util)."),
        Flashcard(front="TGI vs vLLM?", back="<strong>TGI</strong> = HF-ecosystem-native; easier HF model integration. <strong>vLLM</strong> = higher throughput at peak; broader optimization toolkit."),
        Flashcard(front="When pick Triton?", back="Multi-framework fleet (TF / PyTorch / ONNX / Triton custom) or TensorRT-LLM optimised LLMs. Production-grade for mixed-model serving."),
        Flashcard(front="NIM Operator — what does it provide?", back="Pre-optimised model containers (per GPU model); operator deploys + autoscales + monitors; commercial NVIDIA support."),
        Flashcard(front="llm-d — what makes it K8s-native?", back="Built around K8s primitives — Service / Deployment / HPA + LLM-specific autoscaling (queue depth + KV-cache fullness). Newer; open-source."),
        Flashcard(front="LLM quantization options?", back="<strong>AWQ</strong> (Activation-aware Weight Quantization), <strong>GPTQ</strong>, <strong>FP8</strong>, <strong>INT4 / INT8</strong>. Trade accuracy for memory + throughput."),
        Flashcard(front="Tensor parallel — what does it solve?", back="Splits one model across multiple GPUs for memory + speed. Tensor parallel = layers split; pipeline parallel = stages split. Combine for very large models."),
        Flashcard(front="KServe + LLM serving?", back="ServingRuntime wraps vLLM / TGI / Triton / NIM as K8s-native InferenceService. Adds autoscale + canary + multi-model serving."),
    ],
    quizzes=[
        Quiz(prompt="Deploy Llama 3 70B inference fleet for high-throughput. Walk steps.",
            answer="(1) <strong>Pick vLLM</strong>: open-source default; high throughput; PagedAttention + continuous batching. (2) <strong>Quantize model</strong>: AWQ for ~50% memory reduction with minimal accuracy loss. (3) <strong>Tensor parallel</strong>: 70B across 4×H100 (each ~25GB after AWQ). (4) <strong>KServe ServingRuntime</strong>: wrap vLLM as InferenceService. (5) <strong>Autoscale</strong>: HPA on request count or KServe queue-based. (6) <strong>Observability</strong>: Prometheus per-server (TTFT, TPOT, throughput, KV-cache util). (7) <strong>Canary</strong>: KServe traffic split for new model versions."),
        Quiz(prompt="Multi-model fleet: 3 LLMs + 5 CV models + 2 classifiers. Pick server.",
            answer="<strong>NVIDIA Triton</strong>: one server handles all frameworks (TF / PyTorch / ONNX / TensorRT-LLM for LLMs) + concurrent model execution + dynamic batching + model ensembles. Single server simplifies ops; per-framework optimisation via TensorRT-LLM for LLMs. Alternative: Triton for non-LLM + vLLM for LLMs (separate fleets); both work; Triton-only is simpler."),
        Quiz(prompt="The CFO sees NVIDIA NIM cost: \"build it ourselves with vLLM.\" Defend / refute.",
            answer="\"<strong>It\'s a make-vs-buy on perf-tuning + support.</strong> NIM = pre-optimised + commercial support; vLLM = self-tune + community. Three considerations: (1) <strong>Engineering cost</strong>: vLLM tuning (quantization, batching, parallel) is 1-2 engineer-weeks per model. NIM ships pre-optimised. (2) <strong>Support</strong>: NVIDIA NIM has commercial SLA; vLLM = community. For prod-critical, NIM\'s SLA matters. (3) <strong>Flexibility</strong>: vLLM open-source = customisable; NIM closed. <strong>Right answer per team</strong>: small team without GPU experts → NIM. Mature ML platform team → vLLM. Hybrid: NIM for stable models; vLLM for cutting-edge.\"", cyoa=True, cyoa_tag="how the platform engineer framed make-vs-buy"),
    ],
    glossary=[
        GlossaryItem(name="vLLM", definition="UC Berkeley open-source LLM server. PagedAttention + continuous batching."),
        GlossaryItem(name="PagedAttention", definition="KV-cache paged like virtual memory. Reduces fragmentation; 2-4× throughput."),
        GlossaryItem(name="continuous batching", definition="Requests batch dynamically (not fixed at decode start). Higher GPU util."),
        GlossaryItem(name="TGI", definition="Hugging Face Text Generation Inference. HF-ecosystem-native; streaming + batching."),
        GlossaryItem(name="NVIDIA Triton", definition="Multi-framework inference server. TF / PyTorch / ONNX / TensorRT-LLM."),
        GlossaryItem(name="TensorRT-LLM", definition="NVIDIA library optimising LLMs for TensorRT runtime. Used by Triton + NIM."),
        GlossaryItem(name="NIM Operator", definition="NVIDIA Inference Microservice; commercial managed serving."),
        GlossaryItem(name="llm-d", definition="K8s-native LLM serving framework. Built on K8s primitives + LLM-specific autoscaling."),
        GlossaryItem(name="quantization (AWQ / GPTQ / FP8)", definition="Model compression — fewer bits per weight; trade accuracy for memory + throughput."),
        GlossaryItem(name="tensor parallel", definition="Split model layers across GPUs for memory + speed."),
    ],
    recap_lead="Five LLM servers: vLLM (open-source default), TGI (HF-native), Triton (multi-framework), NIM (managed), llm-d (K8s-native). Pick by model + ecosystem + ops appetite. Wrap with KServe for autoscale + canary.",
    recap_next='<strong>Next — I5: AI Gateway / LLM Gateway patterns (Envoy AI Gateway, Kong AI Gateway).</strong>',
    architecture_svg='''<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LLM serving stack: KServe + ServingRuntime wraps vLLM / TGI / Triton / NIM / llm-d.">
  <rect x="10" y="10" width="740" height="220" rx="12" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">LLM SERVING · KSERVE WRAPS 5 SERVING RUNTIMES</text>
  <rect x="20" y="50" width="160" height="65" rx="6" fill="#3F4A5E"/>
  <text x="100" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Model artifact</text>
  <text x="100" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">OCI registry / S3</text>
  <text x="100" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">+ Cosign sig + SBOM</text>
  <line x1="180" y1="82" x2="210" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aI4)"/>
  <defs><marker id="aI4" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><polygon points="0 0, 10 5, 0 10" fill="#5A4F45"/></marker></defs>
  <rect x="210" y="50" width="180" height="65" rx="6" fill="#5DCAA5"/>
  <text x="300" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">KServe InferenceService</text>
  <text x="300" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">predictor + transformer + explainer</text>
  <text x="300" y="100" text-anchor="middle" font-size="8" fill="#1F2433">Knative autoscale or HPA</text>
  <line x1="390" y1="82" x2="420" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aI4)"/>
  <rect x="420" y="50" width="180" height="65" rx="6" fill="#FF9900"/>
  <text x="510" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">ServingRuntime</text>
  <text x="510" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">per-framework template</text>
  <text x="510" y="100" text-anchor="middle" font-size="8" fill="#1F2433">image + protocol + caps</text>
  <line x1="600" y1="82" x2="630" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aI4)"/>
  <rect x="630" y="50" width="110" height="65" rx="6" fill="#A04832"/>
  <text x="685" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">GPU Pod</text>
  <text x="685" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">MIG instance</text>
  <text x="685" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">tensor parallel</text>
  <rect x="20" y="130" width="140" height="55" rx="6" fill="#5A6B81"/>
  <text x="90" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">vLLM</text>
  <text x="90" y="166" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">PagedAttn + cont.batching</text>
  <text x="90" y="178" text-anchor="middle" font-size="8" fill="#FBE8DC">open-source default</text>
  <rect x="170" y="130" width="140" height="55" rx="6" fill="#5DCAA5"/>
  <text x="240" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">TGI</text>
  <text x="240" y="166" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">HF-ecosystem-native</text>
  <text x="240" y="178" text-anchor="middle" font-size="8" fill="#1F2433">streaming + batching</text>
  <rect x="320" y="130" width="140" height="55" rx="6" fill="#FF9900"/>
  <text x="390" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Triton</text>
  <text x="390" y="166" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">multi-framework</text>
  <text x="390" y="178" text-anchor="middle" font-size="8" fill="#1F2433">+ TensorRT-LLM</text>
  <rect x="470" y="130" width="140" height="55" rx="6" fill="#5E4A8E"/>
  <text x="540" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">NIM Operator</text>
  <text x="540" y="166" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">NVIDIA-managed</text>
  <text x="540" y="178" text-anchor="middle" font-size="8" fill="#FBE8DC">commercial</text>
  <rect x="620" y="130" width="120" height="55" rx="6" fill="#FAC775"/>
  <text x="680" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">llm-d</text>
  <text x="680" y="166" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">K8s-native</text>
  <text x="680" y="178" text-anchor="middle" font-size="8" fill="#5A4F45">queue + KV-cache aware</text>
  <rect x="20" y="195" width="720" height="30" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="215" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">Quantization (AWQ / GPTQ / FP8 / INT4) · tensor + pipeline parallel for large models · canary via KServe revisions</text>
</svg>''',
    architecture_caption='LLM serving stack: model artifact → KServe InferenceService (autoscale + canary) → ServingRuntime template wraps the chosen runtime (vLLM / TGI / Triton / NIM / llm-d) → GPU Pods (MIG-sliced or whole-GPU). Quantization + tensor parallel for large models.',
)
