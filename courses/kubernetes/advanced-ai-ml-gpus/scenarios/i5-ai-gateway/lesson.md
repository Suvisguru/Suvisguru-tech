# K-ADV-AI I5 — I5 · AI / LLM Gateway Patterns

> Course: K-ADV-AI (advanced specialization)
> Module I5 · AI Gateway
> Companion preview: `/preview-kubernetes-adv-ai-lesson-05.html`.

---

**🎯 If you remember nothing else:** **AI Gateway = L7 LLM ingress with model routing + per-tenant token budgets + safety filters + multi-provider failover. Envoy AI Gateway / Kong AI Gateway / Portkey.**

## 1. Beyond L7 — model routing + tokens + safety

Generic L7 gateways (Ingress / Gateway API) handle host + path + method + headers. **AI Gateway** adds LLM-aware features:
    
      - **Model name routing**: route per OpenAI-style `model` field in request body — "gpt-4 → premium pool; gpt-3.5 → standard pool."

      - **Token-aware rate limit**: per-tenant tokens-per-minute (input + output); prevents one tenant draining quota.

      - **Token-aware cost budget**: per-tenant monthly token budget; reject when exhausted.

      - **Safety filters**: PII redaction; jailbreak detection; output moderation (Llama Guard / Azure Content Safety).

      - **Caching**: identical-prompt response cache; massive cost saving for repeated queries.

      - **Failover**: provider A primary; provider B fallback if A degraded.

## 2. Gateway API + LLM-specific extensions

**Envoy AI Gateway**: Envoy + Gateway API + LLM extensions. *AIGatewayRoute* CRD declares model routing + token rate limit + cost budget per backend. Backends = OpenAI-API-compatible (vLLM / TGI / Triton with OpenAI shim / actual OpenAI / etc.).
    Pattern: tenant request hits Envoy AI Gateway; gateway authenticates; checks token budget (Redis-backed); routes per model; streams response back; logs token consumption.

## 3. Kong-based + commercial LLM access layer

**Kong AI Gateway**: built on Kong; multi-provider routing (OpenAI / Anthropic / local LLM); transformations (translate request shapes between providers); semantic caching; pre/post-processing plugins.
    **Portkey**: commercial managed LLM access layer. Unified API across 200+ models; observability + cache + load balancing + failover. Trade self-host for hosted simplicity.

## 4. Per-tenant routing + safety + observability

**Pattern**: every LLM request goes through AI Gateway. Gateway:
    
      - Authenticates tenant (JWT).

      - Checks per-tenant rate limit (TPM) + cost budget.

      - Applies safety filter (input PII detection / jailbreak detection).

      - Routes per model name to right backend (local LLM / OpenAI API / partner API).

      - Streams response back; applies output safety filter.

      - Logs token consumption for billing + observability.

    
    **Design**: Redis or KV for token counters; Prometheus for metrics; Loki / Splunk for prompt audit (with PII redaction); per-tenant dashboards in Backstage.

## Before / After

**Before.** Pre-AI-Gateway, LLM ingress = generic Ingress + per-app rate limit; no token-aware budget; no safety; one tenant could DoS; cost surprises.

**After.** AI Gateway: per-tenant token budget + rate limit + safety filters + model routing + multi-provider failover + semantic cache. LLM serving has L7 protection.

*LLM L7 needs differ from web L7. AI Gateway is the right layer.*

## Analogy — the K-Observatory array

The Triage Desk at K-Observatory routes requests to the right rendering hall. Customers arrive with requests + budgets + permits (tokens + auth). The triage clerk checks budget (token rate limit), routes to the right hall (model name), filters dangerous requests (safety), and logs everything for billing.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Triage clerk | AI Gateway (Envoy AI / Kong AI / Portkey) |
| Customer permit | JWT auth |
| Token budget | Tokens-per-minute rate limit |
| Monthly account | Cost budget per tenant |
| Hall routing form | Model name routing |
| Dangerous-request filter | Safety filter (PII / jailbreak / Llama Guard) |
| Frequent-question shortcut | Semantic cache |
| Backup hall | Multi-provider failover (OpenAI / Anthropic / local) |

⚠️ *Analogy stops here:* A real triage desk is paper; AI Gateway is policy + Redis + safety models — invisible until tested. Synthetic abuse traffic verifies behavior.

## ELI5 / ELI10

**ELI5.** Triage desk routes LLM requests, checks budget, filters bad asks, picks the right model. Saves money + protects platform.

**ELI10.** **AI Gateway**: L7 LLM-aware ingress. **Envoy AI Gateway**: Gateway API + AIGatewayRoute extensions. **Kong AI Gateway**: multi-provider + semantic cache. **Portkey**: commercial managed. **Features**: model routing + token rate limit + cost budget + safety filter + cache + failover.

## Real-world scenarios

- **Per-tenant token budget cut DoS risk.** One tenant's prompt-flood maxed out shared LLM; AI Gateway with per-tenant TPM rate limit blocks; other tenants unaffected. Postmortem: TPM tunable per tier.
- **Multi-provider failover.** OpenAI degraded; AI Gateway auto-failover to Anthropic for the same logical model; users notice nothing. SLA preserved.
- **Semantic cache cut cost 60%.** Customer-support chat had 70% prompt similarity (FAQ-style). Semantic cache hit rate 60%; LLM cost dropped accordingly without changing user experience.
- **Outage — no safety filter.** Pre-AI-Gateway, jailbreak prompts produced harmful outputs; reputational risk. Postmortem: Llama Guard at gateway; harmful prompts filtered; safer.

## Common misconceptions

- **Myth:** "Generic Gateway API handles LLM."
  **Truth:** Generic GW API doesn't know about tokens, prompt content, or safety. AI Gateway extensions add LLM-aware semantics. Both can coexist (AI Gateway sits behind Gateway API).
- **Myth:** "Cache is unsafe for LLM."
  **Truth:** Semantic cache (with embedding similarity threshold) is safe + cost-effective for stable prompts. Tune similarity threshold per workload; cache invalidation when prompt strategy changes.
- **Myth:** "Failover doesn't work for LLM (different models give different answers)."
  **Truth:** Within a model class (gpt-4 vs Claude Opus), responses are similar enough for many use cases. For deterministic answers, single-provider; for chat / general queries, failover preserves UX during one provider's outage.

## Recap

AI Gateway = L7 LLM-aware ingress. Envoy AI Gateway / Kong AI Gateway / Portkey. Token rate limit + cost budget + safety filters + model routing + semantic cache + multi-provider failover. LLM serving needs LLM-aware L7.

**Next — I6: High-speed networking (RDMA, EFA) + storage throughput + JuiceFS / Alluxio + OCI artifacts for models.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
