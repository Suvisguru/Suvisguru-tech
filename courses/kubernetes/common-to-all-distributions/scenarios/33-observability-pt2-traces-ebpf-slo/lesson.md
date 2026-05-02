# Lesson 33 — Observability Part 2 · Traces, eBPF, SLOs

> Course: Kubernetes — Common to all distributions
> Module 14 · Observability · Lesson 2 of 2
> Companion preview: `/preview-kubernetes-lesson-33.html`.

---

**🎯 If you remember nothing else:** **Traces** answer "where did time go in this request?" Implement with OTel SDKs; store in **Tempo / Jaeger**. **eBPF** tools (Hubble, Pixie, Tetragon) get kernel-level visibility without app changes. **SLOs** are explicit reliability targets (e.g., "99.9% of requests under 200ms over 30 days"); the gap between target and reality is your *error budget*. Alerts page when the budget burns fast.

## 1. What a trace is

A **trace** is the record of a single request as it flows through a distributed system. Each unit of work is a **span**: "service X processed step Y in Z ms." Spans are nested: when service A calls service B, A's span contains B's span as a child. Spans share a **trace ID** (so you can find them all) and have **span IDs** + **parent span IDs** (so you can rebuild the tree).
    The OTel model is one trace ID per request, propagated through the call chain via the `traceparent` HTTP header (W3C Trace Context standard). Every service in the chain sees the trace ID, creates its own spans, and ships them to a tracing backend.
    What you get in return: a **flame graph** of one request across N services, showing exactly which span was slow. The single best debugging tool for distributed systems.

## 2. Auto-instrumentation, sampling, backends

**Auto-instrumentation**: OTel ships SDKs for every major language. The Java agent and Python's auto-instrumentor add tracing to many libraries (HTTP clients, gRPC, databases) without code changes. Java: `java -javaagent:opentelemetry-javaagent.jar -jar app.jar`. Python: `opentelemetry-instrument` wraps your entry point. Most apps get traced for free.
    **Sampling**: at scale, tracing 100% of requests is too expensive. Three patterns:
    
      - **Head sampling** — decide at the entry point (gateway): "trace 1% of all requests." Simple, predictable cost. Loses interesting tails.

      - **Tail sampling** — collect everything per request, decide after seeing the result: "trace this if it errored or took >1s." Better signal, harder ops.

      - **Adaptive sampling** — modern approach: combine head + tail. OTel Collector's tail-sampling processor implements this.

    
    **Backends**: **Tempo** (Grafana, object-storage backed, cheap), **Jaeger** (CNCF, mature), vendor SaaS (Honeycomb, Datadog, Lightstep). All consume OTLP.

## 3. The view from the kernel

OTel SDKs require code changes (or auto-instrumentation injection). **eBPF**-based tools observe from the kernel — no app changes, no SDK, no language support needed. The cost: kernel-level metrics, not application semantics.
    Three popular eBPF tools:
    
      - **Hubble** (Cilium) — per-flow network observability. "Service X talked to Y on port 443; 12ms latency; HTTP 200." Built on Cilium's eBPF data plane (Lesson 24).

      - **Pixie** (New Relic, formerly Pixie Labs) — installs as a DaemonSet, instruments syscalls + HTTP/gRPC traffic at the kernel. PXL queries (Python-like) over the in-cluster data. Free for small clusters.

      - **Cilium Tetragon** — security-focused eBPF: detect process exec, file opens, network connects. Generates events for any of these and routes to your SIEM. Powerful for runtime detection.

    
    eBPF is also the backbone of:
    
      - Continuous profiling — **Parca** / **Pyroscope** profile every process in production with low overhead.

      - **Falco** — runtime security: alert on suspicious syscall patterns. Lesson 31.

      - Network performance monitoring — **cilium hubble observe**.

    
    [ deep dive — skip if new ]eBPF's sweet spot: getting visibility into already-deployed apps that you can't modify. Vendor SaaS, legacy services, third-party Pods. The OTel SDK route gives semantically richer signals ("this is the user-checkout flow, this part is auth"). For new code, instrument with OTel; for old/opaque code, layer eBPF on top.

## 4. Error budgets and burn-rate alerts

An **SLO** (Service Level Objective) is a target for a service's reliability over a window. Format: "99.9% of HTTP requests succeed within 200ms, measured over 30 rolling days." Three components:
    
      - **SLI** (indicator) — what you measure. "Successful requests / total requests."

      - **SLO** (objective) — the target. "99.9%."

      - **Error budget** — the allowed failure. 100% - 99.9% = 0.1%. With 1M requests/month, you can fail 1000 and still hit your SLO.

    
    SLOs drive everything else. Alerts fire on **burn rate** — "if you keep failing at this rate, you'll exceed your error budget in 1 hour" — not on raw error counts. Alerts that page humans correspond to budget at risk; alerts that don't are noise.
    Tools that turn SLO definitions into Prometheus alerts:
    
      - **Sloth** (Slok.dev) — YAML SLO → Prometheus rules. Multi-window-multi-burn-rate alerts (Google SRE method) baked in.

      - **Pyrra** — K8s-native; SLO CRD; UI for budget tracking.

      - **OpenSLO** — emerging vendor-neutral spec.

    
    The reliability-cost trade: chasing 99.99% costs 10× more than 99.9%. SLOs are how the org agrees on which trade to make. Engineers don't commit to 99.99% "because reliability is good" — they commit to it because product / users actually need it.

## Before / After

**Before.** Pre-tracing era: "the request is slow" → grep logs across 8 services by timestamp, hope clocks are synced, reconstruct the call chain by hand. SLOs were aspirational notes in a wiki. eBPF was a research curiosity. Each app needed its own custom instrumentation.

**After.** OTel-instrumented services emit traces; one click in Grafana shows the flame graph. Hubble shows per-flow network signals without app changes. Pyrra shows real-time error budget remaining. Alerts fire on burn rate, not raw thresholds. MTTR drops from hours to minutes; on-call sleeps better.

Tracing + eBPF + SLOs is what "observability" actually means in 2026. The Three Pillars era is behind us; the future is unified semantic + kernel signals tied to explicit reliability targets.

## Analogy — the K-Town district

Two more rooms in the Observatory. The **tracing room** has a flight-data recorder for every request: when it entered the city, which buildings it visited, how long it spent in each, who else it talked to. Open one flight record and you see the whole journey as a flame chart. The **eBPF wing** has kernel-level sensors at every building entrance — they don't care what the building does, only what flows in and out at the OS level. Together, the two views answer different questions: tracing gives you semantics ("this is the auth step, this is the cache lookup"), eBPF gives you ground truth ("the kernel saw 7 syscalls and a network read").Off to one side: the **SLO board**. Every service has a reliability target posted publicly. A meter shows error budget remaining. The on-call gets paged when the meter is burning fast — not on every blip, only when reliability is actually at risk.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Flight-data recorder per request | Distributed trace |
| Each leg of the journey on the recorder | Span |
| Recorder ID printed on the boarding pass | Trace ID + W3C traceparent header |
| Flame graph of the whole journey | Trace visualisation (Tempo / Jaeger UI) |
| Kernel-level sensors | eBPF programs |
| Per-flow network sensor | Hubble |
| "What's every process doing right now" sensor | Pixie / Cilium Tetragon |
| Public reliability target | SLO |
| Allowable failure budget | Error budget |
| "Burning too fast" alarm | Burn-rate alert |

⚠️ *Analogy stops here:* The analogy stops here: real traces aren't pre-recorded — they're sampled subsets reconstructed from spans shipped post hoc, and they're only as good as your propagation discipline. "Flight-data recorder for every request" is sampling-dependent.

## ELI5 / ELI10

**ELI5.** Imagine your toy went on an adventure through 5 rooms. The trace is a map showing how long it spent in each room. The eBPF is the doorbell at every room saying "toy went in, toy came out, took 3 minutes." The SLO is your promise: "toy will finish 99 of 100 adventures in time for dinner."

**ELI10.** Traces show where time goes across services — instrument with OTel SDKs; ship spans to Tempo/Jaeger via OTLP. eBPF tools (Hubble, Pixie, Tetragon) observe at the kernel — no app changes. SLOs explicitly state reliability targets (e.g., "99.9% under 200ms over 30 days"); error budget = allowed failures. Burn-rate alerts catch fast burns before SLO is broken. Sloth / Pyrra generate alert rules from SLO YAML.

## Real-world scenarios

- **A SaaS using OTel + Tempo for tracing.** Every Go service has the OTel SDK; auto-instrumentation for HTTP, gRPC, Postgres clients. Tempo backend on S3 for cheap long-term retention. Tail sampling at 100% for errors + slow traces, 1% for normal. Storage cost ~$0.10 per million traces. MTTR for cross-service issues halved.
- **A bank using Cilium Hubble for flow visibility.** Pre-existing apps; instrumentation requires legal review per service. Hubble is install-once and gives per-flow signals immediately: "`auth-service` connected to `user-db`, port 5432, latency 8ms." Found a misrouted flow within first day of install. Compliance pleased: no app changes.
- **A startup using Pixie for live debugging.** Pixie DaemonSet on every node. Engineers run PXL queries in production: "show me all HTTP 500s in the last 5 minutes from service X." Like running tcpdump and Wireshark with structured queries. Especially useful for langs/frameworks where OTel SDKs don't work well.
- **A team using Pyrra for SLO management.** Each service ships an SLO YAML alongside its manifests. Pyrra generates Prometheus burn-rate alerts. Engineers see error-budget remaining on a Grafana panel; product sees SLA status in their dashboards. "Should we deploy this risky change?" answered by checking remaining budget — not gut feel.

## Common misconceptions

- **Myth:** Tracing replaces logs.
  **Truth:** Traces show *where time went* in a request; logs show *what happened* within each step. They're complementary. A span's log statements + the surrounding trace context is more useful than either alone.
- **Myth:** eBPF observability replaces OTel.
  **Truth:** They answer different questions. OTel sees app semantics ("this is a user_login"); eBPF sees the kernel ("this is a connect+sendto+recv"). Combined: powerful. Either alone misses half the picture.
- **Myth:** A 99.99% SLO is more impressive than 99.9%.
  **Truth:** It's also 10× more expensive. "More 9s" isn't a virtue. The right SLO is the one your users actually need; over-targeting wastes engineering capacity.

## Recap

Traces answer where time went across services; eBPF tools observe at the kernel without app changes; SLOs turn observability into reliability commitments. Burn-rate alerts page on actual risk, not raw thresholds.

**Next — Lesson 34: Autoscaling.** HPA, VPA, KEDA, Cluster Autoscaler, Karpenter — how the cluster matches capacity to demand. New K-Town district: Power Station.

## Flashcards and quiz

See `flashcards.yaml` (10 cards) and `quiz.yaml` (3 questions).
