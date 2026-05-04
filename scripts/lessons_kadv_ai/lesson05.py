"""K-ADV-AI I5 — AI / LLM Gateway patterns (Envoy AI Gateway, Kong AI Gateway)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AI Gateway."><rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/><text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Triage Desk · K-Observatory — AI Gateway = L7 LLM features</text><rect x="40" y="70" width="200" height="100" rx="10" fill="#5DCAA5"/><text x="140" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">client request</text><text x="140" y="108" text-anchor="middle" font-size="9" fill="#1F2433">prompt + budget + auth</text><rect x="260" y="70" width="220" height="100" rx="10" fill="#3F4A5E"/><text x="370" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">AI Gateway</text><text x="370" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">Envoy AI / Kong AI / Portkey</text><text x="370" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">model routing + auth + rate + safety</text><rect x="500" y="70" width="220" height="100" rx="10" fill="#FF9900"/><text x="610" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">model backends</text><text x="610" y="108" text-anchor="middle" font-size="9" fill="#1F2433">vLLM / Triton / NIM / OpenAI</text></svg>"""


LESSON = LessonSpec(
    num="05", title_short="AI Gateway", title_full="I5 · AI / LLM Gateway Patterns (Envoy AI Gateway, Kong AI Gateway)",
    title_html="K-ADV-AI I5 · AI Gateway", module_eyebrow="Module I5 · Triage Desk — AI Gateway = L7 LLM features",
    hero_sub_html='<strong>AI Gateway</strong>: L7 ingress with LLM-aware features. <strong>Envoy AI Gateway</strong>: Gateway API + LLM extensions; routing per model name; per-tenant rate limits + token budgets; safety filters. <strong>Kong AI Gateway</strong>: Kong-based; multi-provider routing (OpenAI / Anthropic / local); cache + transformations. <strong>Portkey</strong> (commercial): unified LLM access layer; observability + cache + load balancing across providers.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. One tenant\'s prompt floods the LLM fleet; another tenant\'s SLA breached. <em>Without per-tenant rate limit + token budget at the gateway, one tenant DoS\'s the platform.</em> Today\'s lesson: AI Gateway adds LLM-aware L7 protection.",
    stamp_html="<strong>AI Gateway = L7 LLM ingress with model routing + per-tenant token budgets + safety filters + multi-provider failover. Envoy AI Gateway / Kong AI Gateway / Portkey.</strong>",
    district_pin="kai-array05", district_label="Triage Desk",
    sections=[
        Section(eyebrow="Section 1.1 · what makes a gateway AI-aware",
            h2="Beyond L7 — model routing + tokens + safety",
            body_html="""    <p>Generic L7 gateways (Ingress / Gateway API) handle host + path + method + headers. <strong>AI Gateway</strong> adds LLM-aware features:</p>
    <ul>
      <li><strong>Model name routing</strong>: route per OpenAI-style <code>model</code> field in request body — \"gpt-4 → premium pool; gpt-3.5 → standard pool.\"</li>
      <li><strong>Token-aware rate limit</strong>: per-tenant tokens-per-minute (input + output); prevents one tenant draining quota.</li>
      <li><strong>Token-aware cost budget</strong>: per-tenant monthly token budget; reject when exhausted.</li>
      <li><strong>Safety filters</strong>: PII redaction; jailbreak detection; output moderation (Llama Guard / Azure Content Safety).</li>
      <li><strong>Caching</strong>: identical-prompt response cache; massive cost saving for repeated queries.</li>
      <li><strong>Failover</strong>: provider A primary; provider B fallback if A degraded.</li>
    </ul>"""),
        Section(eyebrow="Section 1.2 · Envoy AI Gateway",
            h2="Gateway API + LLM-specific extensions",
            body_html="""    <p><strong>Envoy AI Gateway</strong>: Envoy + Gateway API + LLM extensions. <em>AIGatewayRoute</em> CRD declares model routing + token rate limit + cost budget per backend. Backends = OpenAI-API-compatible (vLLM / TGI / Triton with OpenAI shim / actual OpenAI / etc.).</p>
    <p>Pattern: tenant request hits Envoy AI Gateway; gateway authenticates; checks token budget (Redis-backed); routes per model; streams response back; logs token consumption."""),
        Section(eyebrow="Section 1.3 · Kong AI Gateway + Portkey",
            h2="Kong-based + commercial LLM access layer",
            body_html="""    <p><strong>Kong AI Gateway</strong>: built on Kong; multi-provider routing (OpenAI / Anthropic / local LLM); transformations (translate request shapes between providers); semantic caching; pre/post-processing plugins.</p>
    <p><strong>Portkey</strong>: commercial managed LLM access layer. Unified API across 200+ models; observability + cache + load balancing + failover. Trade self-host for hosted simplicity."""),
        Section(eyebrow="Section 1.4 · pattern + design", h2="Per-tenant routing + safety + observability",
            body_html="""    <p><strong>Pattern</strong>: every LLM request goes through AI Gateway. Gateway:</p>
    <ol>
      <li>Authenticates tenant (JWT).</li>
      <li>Checks per-tenant rate limit (TPM) + cost budget.</li>
      <li>Applies safety filter (input PII detection / jailbreak detection).</li>
      <li>Routes per model name to right backend (local LLM / OpenAI API / partner API).</li>
      <li>Streams response back; applies output safety filter.</li>
      <li>Logs token consumption for billing + observability.</li>
    </ol>
    <p><strong>Design</strong>: Redis or KV for token counters; Prometheus for metrics; Loki / Splunk for prompt audit (with PII redaction); per-tenant dashboards in Backstage."""),
    ],
    pause_check_after_section={
        0: PauseCheck(question="Why is generic Gateway API not enough for LLM workloads?",
            options=[("Performance.", False), ("LLM needs token-aware rate limits + cost budgets + safety filters + model routing — features generic L7 doesn\'t provide.", True), ("Required by NVIDIA.", False)],
            feedback="LLM serving has unique L7 needs (tokens, cost, safety) that generic Gateway API doesn\'t handle. AI Gateway extensions fill the gap."),
        3: PauseCheck(question="Why semantic caching for LLM?",
            options=[("Performance only.", False), ("Identical / near-identical prompts return cached response; massive cost saving for repeated queries.", True), ("Required by OpenAI.", False)],
            feedback="LLM tokens are expensive. Semantic cache catches similar prompts; cost can drop 50%+ for chat / FAQ workloads. Embedding-based similarity match."),
    },
    before_after_before='<p>Pre-AI-Gateway, LLM ingress = generic Ingress + per-app rate limit; no token-aware budget; no safety; one tenant could DoS; cost surprises.</p>',
    before_after_after='<p>AI Gateway: per-tenant token budget + rate limit + safety filters + model routing + multi-provider failover + semantic cache. LLM serving has L7 protection.</p>',
    before_after_caption='<p class="ba-caption"><em>LLM L7 needs differ from web L7. AI Gateway is the right layer.</em></p>',
    analogy_intro_html='''<p>The Triage Desk at K-Observatory routes requests to the right rendering hall. Customers arrive with requests + budgets + permits (tokens + auth). The triage clerk checks budget (token rate limit), routes to the right hall (model name), filters dangerous requests (safety), and logs everything for billing.</p>''',
    translation_rows=[
        ("Triage clerk", "AI Gateway (Envoy AI / Kong AI / Portkey)"),
        ("Customer permit", "JWT auth"),
        ("Token budget", "Tokens-per-minute rate limit"),
        ("Monthly account", "Cost budget per tenant"),
        ("Hall routing form", "Model name routing"),
        ("Dangerous-request filter", "Safety filter (PII / jailbreak / Llama Guard)"),
        ("Frequent-question shortcut", "Semantic cache"),
        ("Backup hall", "Multi-provider failover (OpenAI / Anthropic / local)"),
    ],
    analogy_stops="A real triage desk is paper; AI Gateway is policy + Redis + safety models — invisible until tested. Synthetic abuse traffic verifies behavior.",
    eli5="Triage desk routes LLM requests, checks budget, filters bad asks, picks the right model. Saves money + protects platform.",
    eli10="<strong>AI Gateway</strong>: L7 LLM-aware ingress. <strong>Envoy AI Gateway</strong>: Gateway API + AIGatewayRoute extensions. <strong>Kong AI Gateway</strong>: multi-provider + semantic cache. <strong>Portkey</strong>: commercial managed. <strong>Features</strong>: model routing + token rate limit + cost budget + safety filter + cache + failover.",
    scenarios=[
        Scenario(name="Per-tenant token budget cut DoS risk", body="One tenant\'s prompt-flood maxed out shared LLM; AI Gateway with per-tenant TPM rate limit blocks; other tenants unaffected. Postmortem: TPM tunable per tier."),
        Scenario(name="Multi-provider failover", body="OpenAI degraded; AI Gateway auto-failover to Anthropic for the same logical model; users notice nothing. SLA preserved."),
        Scenario(name="Semantic cache cut cost 60%", body="Customer-support chat had 70% prompt similarity (FAQ-style). Semantic cache hit rate 60%; LLM cost dropped accordingly without changing user experience."),
        Scenario(name="Outage — no safety filter", body="Pre-AI-Gateway, jailbreak prompts produced harmful outputs; reputational risk. Postmortem: Llama Guard at gateway; harmful prompts filtered; safer."),
    ],
    misconceptions=[
        Misconception(myth="\"Generic Gateway API handles LLM.\"", truth="Generic GW API doesn\'t know about tokens, prompt content, or safety. AI Gateway extensions add LLM-aware semantics. Both can coexist (AI Gateway sits behind Gateway API)."),
        Misconception(myth="\"Cache is unsafe for LLM.\"", truth="Semantic cache (with embedding similarity threshold) is safe + cost-effective for stable prompts. Tune similarity threshold per workload; cache invalidation when prompt strategy changes."),
        Misconception(myth="\"Failover doesn\'t work for LLM (different models give different answers).\"", truth="Within a model class (gpt-4 vs Claude Opus), responses are similar enough for many use cases. For deterministic answers, single-provider; for chat / general queries, failover preserves UX during one provider\'s outage."),
    ],
    flashcards=[
        Flashcard(front="What does AI Gateway add over generic Gateway API?", back="Token-aware rate limit + cost budget + safety filters (PII / jailbreak) + model routing + semantic cache + multi-provider failover. LLM-aware L7."),
        Flashcard(front="Envoy AI Gateway primary CRD?", back="<strong>AIGatewayRoute</strong> — declares model routing + token rate limit + cost budget per backend. Backends are OpenAI-API-compatible (vLLM / TGI / actual OpenAI)."),
        Flashcard(front="Kong AI Gateway differentiator?", back="Multi-provider transformations (translate between OpenAI / Anthropic / local LLM request shapes); semantic caching; Kong plugin ecosystem."),
        Flashcard(front="Portkey what is it?", back="Commercial managed unified LLM access layer; 200+ models; observability + cache + load balancing + failover. Trade self-host for hosted."),
        Flashcard(front="Token budget enforcement — where stored?", back="Redis or KV for fast counters; per-tenant key; rate-limit reset windows. Common pattern."),
        Flashcard(front="Safety filters — examples?", back="<strong>Llama Guard</strong> (Meta), <strong>Azure Content Safety</strong>, <strong>NVIDIA NeMo Guardrails</strong>, custom regex / classifier. Both input + output filtering."),
        Flashcard(front="Semantic cache vs exact cache?", back="<strong>Exact</strong>: hash of prompt; only identical hits. <strong>Semantic</strong>: embedding distance; near-identical prompts hit cache. Higher hit rate; tune similarity threshold."),
        Flashcard(front="Multi-provider failover criteria?", back="Provider degraded (latency / errors above threshold); failover to second provider. Within model class for similar UX."),
    ],
    quizzes=[
        Quiz(prompt="Design AI Gateway for multi-tenant LLM platform.",
            answer="(1) <strong>Envoy AI Gateway</strong> deployed via Gateway API. (2) <strong>Per-tenant JWT auth</strong>: tenant ID extracted; rate limit + budget keyed by tenant. (3) <strong>AIGatewayRoute per model</strong>: gpt-4 → openai backend; llama-3-70b → local vLLM. (4) <strong>Redis token counters</strong>: TPM enforcement per tenant per model. (5) <strong>Safety filters</strong>: input PII redaction (regex + classifier); output moderation via Llama Guard. (6) <strong>Semantic cache</strong>: Redis + embedding model; 0.95 similarity threshold for chat. (7) <strong>Failover</strong>: OpenAI primary; Anthropic fallback per model class. (8) <strong>Observability</strong>: Prometheus metrics (TPM / cost / cache-hit / safety-trigger); Loki for prompt audit logs (PII-redacted)."),
        Quiz(prompt="A tenant complains: \"my budget hit but the response was the same as cached.\" Walk diagnostic.",
            answer="(1) <strong>Cache logic check</strong>: was this prompt in semantic cache? Why not? Embedding similarity threshold maybe too tight. (2) <strong>Cost accounting</strong>: did the gateway log the cache HIT but still deduct tokens? Bug in the budget logic. (3) <strong>Fix</strong>: cache HIT should not deduct tokens; only cache MISS does. (4) <strong>Adjust similarity threshold</strong>: if 0.99 too tight, lower to 0.95 for chat; raise for code-gen. (5) <strong>Audit</strong>: per-tenant cache-hit ratio dashboard; tune per workload. <em>Caching alignment with billing is the most common AI Gateway bug.</em>"),
        Quiz(prompt="The CFO sees Portkey cost; \"build it ourselves with Envoy AI Gateway.\" Defend / refute.",
            answer="\"<strong>Build-vs-buy on AI Gateway: Portkey is hosted; Envoy AI Gateway is open-source self-hosted.</strong> Three considerations: (1) <strong>Engineering time</strong>: Portkey live in days; self-build = months. (2) <strong>Multi-provider</strong>: Portkey supports 200+ models with normalised API; self-build = bespoke per provider. (3) <strong>Observability</strong>: Portkey ships dashboards; self-build = wire Prometheus + Loki. <strong>Where build wins</strong>: niche compliance requirements; specific providers Portkey doesn\'t support; cost at very large scale (Portkey is per-token pricing). <strong>Right answer per team</strong>: small/medium → Portkey for time-to-value. Large with strict compliance → Envoy AI Gateway. Hybrid: Portkey for non-critical routing; Envoy AI Gateway for compliance-bound paths.\"", cyoa=True, cyoa_tag="how the platform engineer framed AI Gateway make-vs-buy"),
    ],
    glossary=[
        GlossaryItem(name="AI Gateway", definition="L7 LLM-aware ingress. Token-aware rate limit + cost + safety + multi-provider routing."),
        GlossaryItem(name="Envoy AI Gateway", definition="Envoy + Gateway API + AIGatewayRoute LLM extensions; open-source."),
        GlossaryItem(name="Kong AI Gateway", definition="Kong-based AI Gateway; multi-provider transformations + semantic cache + plugins."),
        GlossaryItem(name="Portkey", definition="Commercial managed unified LLM access layer; 200+ models; cache + failover."),
        GlossaryItem(name="AIGatewayRoute", definition="Envoy AI Gateway CRD declaring model routing + rate + cost budget per backend."),
        GlossaryItem(name="token-aware rate limit", definition="Tokens-per-minute (input + output) per tenant; not just request-per-second."),
        GlossaryItem(name="cost budget (LLM)", definition="Per-tenant monthly token budget enforced at gateway."),
        GlossaryItem(name="semantic cache", definition="Embedding-similarity cache for LLM responses; high hit rate for stable prompts."),
        GlossaryItem(name="Llama Guard / NeMo Guardrails", definition="LLM safety filter models; classify input / output for harmful content."),
        GlossaryItem(name="multi-provider failover", definition="Gateway routes to backup provider when primary degraded."),
    ],
    recap_lead="AI Gateway = L7 LLM-aware ingress. Envoy AI Gateway / Kong AI Gateway / Portkey. Token rate limit + cost budget + safety filters + model routing + semantic cache + multi-provider failover. LLM serving needs LLM-aware L7.",
    recap_next='<strong>Next — I6: High-speed networking (RDMA, EFA) + storage throughput + JuiceFS / Alluxio + OCI artifacts for models.</strong>',
)
