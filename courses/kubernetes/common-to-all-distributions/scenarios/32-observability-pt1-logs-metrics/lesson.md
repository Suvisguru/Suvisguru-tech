# Lesson 32 — Observability Part 1 · Logs and Metrics

> Course: Kubernetes — Common to all distributions
> Module 14 · Observability · Lesson 1 of 2
> Companion preview: `/preview-kubernetes-lesson-32.html`.

---

**🎯 If you remember nothing else:** Three pillars: **logs** (events), **metrics** (numbers), **traces** (request flow — Lesson 33). Modern stack: instrument with **OpenTelemetry SDKs**, ship via **OpenTelemetry Collector**, store in vendor-neutral backends (**Loki** for logs, **Prometheus**/**Mimir**/**VictoriaMetrics** for metrics). The single biggest mistake teams make: not deploying observability infrastructure before they need it.

## 1. Three pillars, one collector

Production debugging answers three questions: **What happened?** (logs — discrete events), **How fast / how much?** (metrics — numeric time series), **Where did time go?** (traces — distributed request flow). Most outages need at least two of three to diagnose.
    Until 2020, each pillar had its own ecosystem: Fluentd / Logstash for logs, Prometheus client libs for metrics, Jaeger / Zipkin / OpenTracing for traces. Each app had three integrations. Then **OpenTelemetry** happened — a CNCF project unifying the SDKs and collector across all three pillars. By 2026, OTel is the de-facto standard. Apps emit signals; the OTel Collector receives them; you choose backends.
    The K8s-specific layer adds:
    
      - **kube-state-metrics** — exposes K8s API state (Pod count, Deployment ready replicas, etc.) as Prometheus metrics.

      - **node-exporter** — exposes node-level metrics (CPU, memory, disk, network) per node.

      - **cAdvisor** (in kubelet) — exposes per-container resource metrics.

      - **OTel Operator** — manages OTel Collector instances + auto-instrumentation injection for common languages.

## 2. From stdout to indexed

K8s convention: containers write logs to **stdout/stderr**, the kubelet captures them, the container runtime writes them to `/var/log/containers/<pod>_<namespace>_<container>.log`. Anything else (writing to a file inside the container, syslog, custom socket) is non-standard and works against you.
    Three collection patterns:
    
      - **Node-level DaemonSet** (most common) — Vector / Fluent Bit / OTel Collector on every node, reading `/var/log/containers/*.log`, parsing, shipping. Scales linearly with nodes; minimal Pod-level overhead.

      - **Sidecar** — a logging container next to each app container. Use for apps that can't emit to stdout (legacy app writing to a file). Ad-hoc, more Pods, more cost.

      - **Direct from app** — app uses an OTel SDK to ship logs. Works but adds latency to the app process; mostly used in modern apps that already use OTel for metrics + traces.

    
    Backends in 2026:
    
      - **Loki** (Grafana Labs) — popular open-source choice. Indexes labels only, full-text search via parsing at query time. Cheap to run.

      - **Elasticsearch / OpenSearch** — full-text indexing. More powerful queries, more expensive ops.

      - **Cloud-native** — CloudWatch (AWS), Cloud Logging (GCP), Azure Log Analytics. Closed but easy.

      - **Vector + S3** — durable, cheap, query later via Athena / Trino.

## 3. From scraping to remote write

Prometheus model: pull-based. A Prometheus server periodically scrapes `/metrics` endpoints exposed by Pods (using the OpenMetrics format), stores time series in its TSDB, exposes them via PromQL.
    The architecture is famously simple, but at scale it shows seams. Single Prometheus instance hits limits at ~10M active series. Three modern options:
    
      - **Prometheus + Thanos / Cortex / Mimir** — Prometheus shards write to a central deduplication/storage layer. Long-term storage on object storage. Mimir (Grafana) is the most popular in 2026.

      - **VictoriaMetrics** — drop-in Prometheus replacement, faster + lower memory at scale. Single-binary cluster mode.

      - **OpenTelemetry-native** — OTel Collector receives metrics, ships via OTLP to any OTLP-compatible backend (Mimir, VictoriaMetrics, vendor SaaS).

    
    What to scrape (the standard K8s metric stack):
    
      - Apps' own `/metrics` via OpenMetrics + ServiceMonitor (Prometheus Operator) or PodMonitor.

      - kube-state-metrics for K8s object state.

      - node-exporter for node-level resources.

      - kubelet/cAdvisor for per-container resources.

      - cluster autoscaler, controller-manager, scheduler — control-plane metrics.

    
    [ deep dive — skip if new ]The cardinality problem: every unique combination of metric labels is a separate time series. A metric with a `user_id` label and 1M users = 1M series. Prometheus doesn't care about the metric values; it cares about the series count. The single most common observability bug: shipping a metric with a high-cardinality label (request_id, user_id, full URL path with IDs). Catch it early; cardinality killers run servers out of memory faster than anything else.

## 4. What good observability looks like

Three artefacts every production service should have:
    
      - **Dashboard** — Grafana panel showing the four golden signals: latency, traffic, errors, saturation. One dashboard per service. Linkable from the runbook.

      - **Alerts** — Prometheus AlertManager rules with PromQL, paging on SLO violations. Alerts have runbooks linked in their annotations.

      - **Runbook** — markdown in git: "if alert X fires, run these queries, look for these patterns, escalate at this signal."

    
    Modern teams also generate this from **SLOs** (Service Level Objectives — covered in Lesson 33). Tools like **Sloth** or **Pyrra** read your SLO definitions and generate the alerts + dashboards automatically. The team writes the SLO; the tools write the boilerplate.
    Common anti-patterns:
    
      - "Page on every 5xx" — death by alert. Page on SLO violation, not transient errors.

      - Alerts without runbooks — pager wakes someone who doesn't know what to do.

      - Vanity dashboards — 40 panels per service nobody reads. Pick the four golden signals; everything else on a secondary dashboard.

      - Logs at INFO level for routine flows — log volume balloons; signal-to-noise drops; cost spikes. Log at WARN or ERROR for routine; INFO only for state changes that might matter in a future incident.

## Before / After

**Before.** Pre-OTel era: Fluentd for logs, Prometheus for metrics, Jaeger for traces — three SDKs, three exporters per app, three on-call dashboards. "Where did the request go?" required correlating across three siloed systems by hand. Cardinality bombs took down Prometheus monthly. Logs at INFO everywhere because nobody had time to tune.

**After.** OpenTelemetry SDKs in every app, OTel Collector as a single ingress, vendor-neutral backends (Loki + Mimir + Tempo). Trace IDs propagated end-to-end. Cardinality monitored as a first-class concern. SLO-driven alerts with linked runbooks. MTTR drops from hours to minutes.

OpenTelemetry adoption was the most consequential observability shift in a decade. By 2026 it's the default; new K8s deployments instrument with OTel from day 1.

## Analogy — the K-Town district

The Observatory sits high above K-Town with three instruments. The **logbook telescope** (logs collector) reads what every building wrote down today — typed messages, errors, traces of activity. The **star chart** (metrics dashboard) shows numerical time series for every quantity worth measuring — temperature, foot traffic, queue depth — refreshed continually. The **OpenTelemetry router** in the dome (OTel Collector) receives signals from every building in a standardised format and forwards them to specialist offices: log archive (Loki), metrics archive (Prometheus / Mimir), and the live alarm board (Grafana). When something goes wrong, the city's on-call walks into the Observatory, glances at the star chart, asks the logbook a question, and is back to bed in minutes.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The logbook telescope | Logs collector (Vector / Fluent Bit / OTel Collector) |
| The star chart | Metrics dashboard (Grafana on Prometheus) |
| The OpenTelemetry router | OTel Collector |
| Standardised signal format | OTLP (OpenTelemetry Protocol) |
| Log archive | Loki / Elasticsearch / S3 |
| Metrics archive | Prometheus / Mimir / VictoriaMetrics |
| Live alarm board | Grafana + AlertManager |
| Star's position drifting suspiciously | Cardinality bomb |

⚠️ *Analogy stops here:* The analogy stops here: real observability backends ingest gigabytes per second and need careful capacity planning; "a telescope" doesn't. And the OTel Collector isn't a router in the network sense — it's a stream-processing pipeline with receivers, processors, and exporters.

## ELI5 / ELI10

**ELI5.** Two notebooks for every building. One says what happened (logs). One has all the numbers (metrics). A friendly robot collects both and puts them in the right drawer so you can find them later.

**ELI10.** Three observability pillars: logs (events), metrics (numbers over time), traces (request flow). OpenTelemetry standardises SDKs + the collector across all three. K8s-specific: pods write to stdout, kubelet captures, a DaemonSet (Vector / Fluent Bit / OTel Collector) ships logs to Loki/Elastic; Prometheus scrapes `/metrics` endpoints (or apps push via OTLP). Avoid high-cardinality metric labels. Pair every alert with a runbook; pair every service with a four-golden-signals dashboard.

## Real-world scenarios

- **A SaaS running OTel + Loki + Mimir.** Every service uses OTel SDKs. OTel Collector DaemonSet receives via OTLP, splits to Loki (logs), Mimir (metrics), Tempo (traces — Lesson 33). Backends are Grafana stack, all open source. Cost: ~10× cheaper than a vendor SaaS, requires more ops effort.
- **A bank running Prometheus + Thanos + ELK.** Prometheus shards per cluster, write through Thanos to S3 for long-term. ELK for logs (full-text search required for compliance). 18-month log retention; PromQL across years via Thanos. Total observability spend: 5% of cluster cost — appropriate for a regulated industry.
- **A startup using a vendor SaaS.** Datadog (or Honeycomb / New Relic). OTel-compatible. One-line agent install. No backend ops. Cost: $$$ at scale. Tradeoff: speed-to-running vs eventual cost. Most startups land here, migrate to self-hosted at $1M+/yr observability spend.
- **A team that fixed an MTTR problem with traces.** Adopted OTel tracing across 14 services. New incident: "checkout slow." Trace shows 4 services contributing to latency; bottleneck is an N+1 query in the inventory service. Pre-tracing, would have meant 2 hours of log-grepping. Post-tracing: 5 minutes.

## Common misconceptions

- **Myth:** Logs replace metrics.
  **Truth:** They're complementary. Logs are great for "what happened in this specific request." Metrics are great for "how does the system behave over time?" Querying logs at scale to compute aggregates is slow + expensive — that's what metrics are for.
- **Myth:** Prometheus is the only metrics solution.
  **Truth:** Prometheus + Mimir / VictoriaMetrics / Thanos / Cortex are the main self-hosted options. Vendor SaaS (Datadog, Honeycomb, etc.) all support OpenMetrics + OTLP. Prometheus is most common; not the only path.
- **Myth:** More logs = better observability.
  **Truth:** More logs = more cost + more noise. Useful logs are sparse: state changes, errors, edge-case branches. Routine info-level on every request is mostly waste. Use metrics for what happens often; logs for what's exceptional.

## Recap

Logs + metrics + (Lesson 33) traces. OTel standardises the SDKs + collector. K8s adds kube-state-metrics + node-exporter + cAdvisor. Avoid cardinality bombs. Pair alerts with runbooks; SLOs drive alerts.

**Next — Lesson 33: Observability Part 2.** Tracing, eBPF-based observability (Hubble, Pixie, Cilium Tetragon), SLOs and the math behind them. Where requests actually spend their time.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
