# K-GKE G7 — G7 · GKE Observability (Cloud Logging + Monitoring + GMP + Grafana + Trace + Profiler + SLO)

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G7 · GKE Observability
> Companion preview: `/preview-kubernetes-gke-lesson-07.html`.

---

**🎯 If you remember nothing else:** **Three pipes auto-enabled (Cloud Monitoring metrics + Cloud Logging logs + Cloud Trace spans). GMP for Prometheus + managed Grafana for the joined view. SLO-first alerting via Service Monitoring. BigQuery cost export ties everything to spend.**

## 1. Cloud Logging + Cloud Monitoring — auto-enabled for GKE

**Cloud Logging** is auto-enabled for GKE clusters. Container stdout/stderr, kubelet, system, and (if enabled in diagnostic settings) control-plane logs all flow to a Log Analytics-equivalent *log bucket*. Query via **Logs Explorer** with the *Logs Query Language* (LQL — similar to grep+filter, simpler than KQL).
    *Structured logs*: emit JSON to stdout from your app and Cloud Logging parses it. Fields searchable as labels. Standard Cloud Logging libraries for Go / Python / Java / Node make this idiomatic.
    **Cloud Monitoring** auto-collects K8s metrics (CPU, memory, container restarts, scheduled vs running Pod counts, etc.) plus per-node + per-cluster GCE metrics. Pre-built *GKE dashboards* in the Cloud Monitoring console cover the standard panes. Workspace concept lets you join metrics across multiple projects.
    **Error Reporting** auto-clusters similar exception traces from your app logs into *error groups*; tracks first-seen, last-seen, occurrence count. Replaces the manual log-grep-for-stack-traces workflow.

## 2. Managed Service for Prometheus (GMP) + managed Grafana

**Managed Service for Prometheus (GMP)** = Google's managed Prometheus-as-a-service. Enable per cluster (`--enable-managed-prometheus`); the GMP collector scrapes Pod metrics annotated with the standard Prometheus annotations + ServiceMonitor / PodMonitor CRDs. Stores in a managed time-series backend; queries via PromQL through the GMP query frontend.
    *Why GMP on top of Cloud Monitoring*: Cloud Monitoring covers GKE-native metrics; GMP covers *application metrics in standard Prometheus format* (counters, gauges, histograms emitted by libraries like prometheus_client, Micrometer). Use both in the same cluster.
    **Managed Grafana options**:
    
      - **Self-hosted Grafana** on GKE → GMP as Prometheus data source + Cloud Monitoring as Stackdriver data source.

      - **Grafana Cloud** integration via OAuth — managed by Grafana Labs.

      - **Native Cloud Monitoring dashboards** for cases where you don't need full Grafana flexibility.

    
    Grafana joins the three pipes (GMP for app metrics, Cloud Monitoring for infra metrics, Cloud Logging for logs via the Cloud Logging data source plugin). Cloud Trace spans visible inline. *One dashboard for the whole picture.*

## 3. Cloud Trace + Cloud Profiler

**Cloud Trace** = managed distributed tracing. Auto-collects traces from any app emitting **OpenTelemetry** spans or using the **Cloud Trace SDK** directly. Standard libraries auto-instrument HTTP, gRPC, SQL, gcloud SDK calls. Sampling configurable (10% of low-value, 100% of error / high-latency).
    Trace view shows *end-to-end timing* of a request across services: e.g., "checkout request, 850ms total: 120ms in API gateway, 80ms in auth, 600ms in DB query, 50ms in payment provider call." Click a span for downstream child spans. Span tags propagate the K8s metadata (Pod name, namespace, node) for correlation with logs + metrics.
    **Cloud Profiler** = continuous CPU + heap profiling. The Profiler agent (no app changes for some languages, library import for others) samples in production with low overhead. View flame graphs in the Cloud console. *Find the function that's burning 30% of your CPU but you didn't know it.*
    **Pattern**: spans give the request-level timing; logs give the per-step narrative; profiler gives the per-function cost. Together they answer "why is this slow?" + "where is the CPU going?"

## 4. Control-plane metrics/logs + SLO Monitoring + alerting policies

**Control-plane metrics + logs**: enable apiserver, scheduler, and controller-manager *metric + log export* in the cluster's monitoring/logging config (`--monitoring=SYSTEM,WORKLOAD,APISERVER,CONTROLLER_MANAGER,SCHEDULER`). Apiserver request rate, latency, error rate land in Cloud Monitoring; audit logs in Cloud Logging.
    **Service Monitoring (SLO)** = define SLOs declaratively: "99.5% of HTTP requests to checkout return 200 with latency < 300ms over a 28-day rolling window." Service Monitoring tracks attainment + burn rate. Alerting on *burn rate* rather than raw error rate gives you actionable signal: "the service is burning error budget 14× faster than sustainable" → page now; "burning 1.5×" → ticket. *Modern SRE alerting; replaces threshold-on-raw-metric noise.*
    **Alerting policies** (Cloud Monitoring) — define metric / log / SLO conditions; route to *Notification Channels* (Pub/Sub → Cloud Functions → PagerDuty / Teams / Slack / email; or direct PagerDuty integration). Use Pub/Sub for fan-out and audit (every alert is a Pub/Sub message you can replay).
    **BigQuery cost view** (recap from G6): BQ billing export + GKE cost allocation = per-namespace cost dashboards in Looker Studio / Grafana. Join cost data with utilisation metrics from GMP / Cloud Monitoring to compute *cost per request* at the service level.

## Before / After

**Before.** Pre-managed GKE observability = Bring Your Own Prometheus + Bring Your Own Grafana + Bring Your Own log shipper + ELK or Loki + custom alert routing. Operators ran 5+ Helm charts and a separate VMSS for the metrics+logs stack. Apiserver logs were essentially invisible without diagnostic-settings wiring. Tracing was unsupported in the basic stack — Cloud Trace existed but was a separate sale.

**After.** Modern GKE auto-enables **Cloud Logging** + **Cloud Monitoring**; **GMP** + **managed Grafana** add Prometheus + flexible visualisation; **Cloud Trace + Cloud Profiler** are first-class for app perf; **Service Monitoring** turns SLOs into burn-rate alerts; **BigQuery cost export** ties spend to workload. *Five managed services replace a 12-component homemade stack.*

*The DIY observability era is over for GKE. Wire up GMP + Grafana + SLO Monitoring; review the Cloud Logging cost monthly; the rest is mostly auto.*

## Analogy — the K-Garden plot

The **Watchtower** at K-Garden is staffed all hours by three observers + an SLO scribe.
    The **Heartbeat Drummer** (metrics) plays a regular cadence: "how full are the plots? how warm is the climate? how fast is the irrigation?" The Cloud Monitoring drummer tracks garden-aware patterns; the GMP drummer follows industry-standard Prometheus rhythms.
    The **Story Scribe** (logs) writes everything narratable: "Gardener A opened greenhouse 3 at 14:32; the irrigation valve in plot 7 reported error." The Cloud Logging scribe's book is queryable via Logs Explorer.
    The **Journey Tracker** (traces) follows one visitor end-to-end: "the visitor entered through Path A, picked up tickets at the Pavilion, walked to Plot 3, watered for 5 minutes, took a soil sample, left through the East Gate." Cloud Trace shows each segment's duration. **Cloud Profiler** is the time-and-motion observer who tells you which gardener spent most of the day on what motion.
    The **SLO Scribe** (Service Monitoring) keeps the contract: "the irrigation service must successfully water plots within 300ms 99.5% of the time over 28 days." When the contract burn rate spikes ("we're burning 14× the sustainable rate"), the Watchtower bell rings (alerting policies → Pub/Sub → PagerDuty).
    The **Garden Accountant** from G6 (BigQuery cost) joins the Watchtower's data: "this plot costs $X/day; it serves Y requests/day; cost per request = Z."

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| Heartbeat Drummer | Metrics — Cloud Monitoring (auto) |
| GMP drummer | Managed Service for Prometheus + PromQL |
| Story Scribe | Logs — Cloud Logging + Logs Explorer |
| Auto-clustered exception groups | Error Reporting |
| Journey Tracker | Cloud Trace — end-to-end distributed tracing |
| Time-and-motion observer | Cloud Profiler — CPU + heap profiles |
| Apiserver / scheduler watchman | Control-plane metrics + audit logs (--monitoring=APISERVER, etc.) |
| SLO Scribe | Service Monitoring — define SLOs, track burn rate |
| Watchtower bell | Alerting policies → Notification Channels (Pub/Sub → PagerDuty / Teams) |
| "Burning 14× sustainable" | Burn-rate-based alerting |
| Joined Watchtower dashboard | Managed Grafana with GMP + Cloud Monitoring + Cloud Logging data sources |
| Garden Accountant's ledger | BigQuery cost export + GKE cost allocation |

⚠️ *Analogy stops here:* A real Watchtower's observers see the same scene; in real systems the three pipes can be sampled / stored separately. Cloud Logging cost can be the dominant observability line item — without retention discipline it dwarfs everything else.

## ELI5 / ELI10

**ELI5.** The Watchtower has three observers (a drummer for metrics, a scribe for stories, a tracker for visitor journeys) and a scribe who tracks the irrigation contract. They tell you when something's wrong before customers notice.

**ELI10.** GKE observability auto-enables Cloud Logging + Cloud Monitoring. **GMP** adds managed Prometheus for app metrics; **managed Grafana** joins everything in one dashboard. **Cloud Trace** for end-to-end distributed traces; **Cloud Profiler** for CPU/heap profiling. **Error Reporting** auto-clusters exception traces. **Service Monitoring** defines SLOs + burn-rate alerts. **Alerting policies** route to Pub/Sub → PagerDuty / Teams. **BigQuery cost view** ties spend to workload. Enable apiserver / scheduler / controller-manager metrics + logs in monitoring/logging config.

## Real-world scenarios

- **SaaS — RED dashboard in managed Grafana joining GMP + Cloud Monitoring.** A SaaS team builds a per-service RED dashboard (Rate, Errors, Duration) in managed Grafana. Rate + Errors from GMP via PromQL on app-emitted prometheus_client counters. Duration from Cloud Trace span percentiles via the Cloud Trace data source. Cluster + node metrics from Cloud Monitoring. *One dashboard, three data sources, MTTR for p99 spikes drops to ~10 min.*
- **Bank — apiserver audit log to Cloud Logging + Sentinel via Pub/Sub.** Bank enables --monitoring=APISERVER + audit log routing. Sink ships audit logs to a Log Analytics-style log bucket; Pub/Sub fan-out forwards to Sentinel SOC. SOC rules detect kubectl exec into prod, RBAC changes outside CI, secret reads from unexpected SAs. *SOC owns the GKE security story; platform team owns alert wiring.*
- **SLO-first alerting reduces pager noise.** Team had threshold alerts: "alert if 5xx rate > 1%." Result: 4-12 pages/day, 80% noise. Migration to **burn-rate alerts** via Service Monitoring: "alert if 28-day burn rate > 14× over a 1-hour window." Now ~1 page/day, ~0 noise. *SLO-first alerting respects error budget; raw thresholds don't.*
- **Profiler caught a 30% CPU regression no one noticed.** Cloud Profiler flame graphs review: a recent code change introduced a regex compile in a hot loop, burning 30% of pod CPU. Refactored to compile once. *Cluster CPU dropped 25% across the affected service's namespace; cost saving paid for the Profiler license many times over.*

## Common misconceptions

- **Myth:** "Cloud Monitoring covers Prometheus metrics."
  **Truth:** Cloud Monitoring auto-collects *K8s + GCE infrastructure metrics*, not app-emitted Prometheus metrics. For app metrics in Prometheus format, enable **GMP**. Both can coexist in one cluster; both queryable from managed Grafana.
- **Myth:** "Threshold alerts are equivalent to SLO burn-rate alerts."
  **Truth:** Threshold alerts fire on raw metric values ("error rate > 1%"). They're noisy: any blip pages. Burn-rate alerts fire on *error-budget consumption rate* ("burning 14× faster than sustainable over 1h"). They wait for sustained breach + scale with severity — page when you're actually losing budget. SRE-grade alerting.
- **Myth:** "Cloud Logging retention defaults are fine."
  **Truth:** Defaults: 30 days for most logs in default log buckets. Often too short for compliance + too long for high-volume noisy logs. *Tune per log bucket*: shorter retention for chatty / dev; longer for audit. Plus consider routing to a custom log bucket with reduced cost; or to BigQuery for SQL-style analysis. Without discipline log ingest cost dominates GKE bills.

## Recap

Three pipes auto-enabled (Logging + Monitoring + Trace); GMP + managed Grafana for the joined view; SLO-first alerting via Service Monitoring; BigQuery cost ties spend to workload.

**Next — G8: GKE Enterprise (Fleets) and AI/ML.** Fleet management across GCP/AWS/Azure/on-prem; Config Sync; Policy Controller; Cloud Service Mesh across fleets; Connect Gateway; Multi-cluster Ingress / Gateway; GKE on AWS / Azure / VMware / bare metal; AI/ML on GKE (JobSet, Kueue, NVIDIA GPU Operator, MIG, TPU multi-host, Ray, GKE Inference Gateway, vLLM/NIM/Triton).

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
