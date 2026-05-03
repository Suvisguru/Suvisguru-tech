# K-OCP O11 — O11 · OpenShift Observability

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O11 · OpenShift Observability
> Companion preview: `/preview-kubernetes-ocp-lesson-11.html`.

---

**🎯 If you remember nothing else:** **Built-in Cluster Monitoring (Prom + Thanos + Alertmanager) + User Workload Monitoring is the metrics foundation. OpenShift Logging (Loki + Vector) for logs. Distributed Tracing (Tempo + OTel) for traces. NetObserv (eBPF) for network flow. SLO-first alerting reduces noise; COO unifies config.**

## 1. Cluster Monitoring (Prometheus + Thanos + Alertmanager) + User Workload Monitoring

**Built-in Cluster Monitoring** ships enabled in every OCP cluster (no opt-in needed). Components managed by the **Cluster Monitoring Operator (CMO)**:
    
      - **Prometheus** — scrapes platform metrics (kubelet, apiserver, controller-manager, scheduler, etcd, ClusterOperators, OperatorHub-installed operators).

      - **Thanos Querier** — multi-Prometheus query layer; supports federation + long-term storage when wired.

      - **Alertmanager** — alert routing + grouping; receivers (PagerDuty, Slack, email, webhook).

      - **kube-state-metrics + node-exporter** — standard exporters.

      - **Telemeter Client** — anonymised cluster health telemetry to Red Hat Insights.

    
    **User Workload Monitoring (UWM)** — opt-in (set `enableUserWorkload: true` in `cluster-monitoring-config` ConfigMap). Lets app teams expose Prometheus metrics from their workloads via **ServiceMonitor / PodMonitor** CRs. Separate Prometheus instance scopes app metrics; Alertmanager handles user alerts.
    **Long-term metrics storage:** wire Thanos Storer + S3-compatible bucket (NooBaa / AWS S3 / Azure Blob); Thanos Querier federates short-term Prometheus + long-term Thanos blocks. Default retention: 15 days per Prometheus.

## 2. OpenShift Logging — Loki + Vector (Fluentd deprecated)

**OpenShift Logging** = managed Operator. Components:
    
      - **Vector** — log collector DaemonSet (replaced Fluentd; Fluentd is deprecated). Faster + lighter; Rust-based.

      - **Loki** — log storage (replaces Elasticsearch; Elasticsearch backend deprecated). Loki uses S3-compatible object storage for log indices + chunks.

      - **LokiStack** CR — declarative LokiOperator config: storage, retention, replication.

    
    **Three log streams:**
    
      - **Application logs** — container stdout/stderr from user namespaces.

      - **Infrastructure logs** — kubelet, kube-apiserver, OCP system namespaces.

      - **Audit logs** — apiserver audit + OAuth audit. Routed separately for compliance.

    
    **ClusterLogForwarder** CR routes logs to one or more outputs: Loki (default), external Splunk / Elasticsearch / Kafka / S3 / syslog. Different streams to different destinations.
    **LogQL** = Loki's query language (Prometheus-PromQL-flavored). Query logs in OCP console *Observe → Logs*; supports both manual + saved queries.

## 3. OpenShift Distributed Tracing — Tempo + OpenTelemetry

**OpenShift Distributed Tracing** = managed Operator. **Tempo** (replaces Jaeger as the storage backend; Jaeger Operator deprecated). Tempo uses S3-compatible object storage; cheaper than Jaeger's Cassandra/Elasticsearch backends.
    **OpenTelemetry (OTel) Operator** — manages OTel Collector deployments. Apps emit OTLP traces; Collector forwards to Tempo. Auto-instrumentation injection for supported languages (Java, Python, Node, .NET) via OTel Operator's instrumentation CR.
    **TempoStack** CR — declarative Tempo configuration: storage backend, retention, replication.
    **TraceQL** = Tempo's query language. Find traces by service, span attributes, latency thresholds. View span timelines in the OCP console.
    Pattern: app emits OTel spans → OTel Collector aggregates → Tempo stores → console + Grafana visualises. Cross-service request tracing across microservice + serverless boundaries.

## 4. NetObserv (eBPF) + Cluster Observability Operator (COO)

**Network Observability (NetObserv) Operator** — eBPF-based flow capture. DaemonSet on each node hooks into kernel; captures Pod-to-Pod, Pod-to-external, DNS lookups. Stores flow data in Loki (or external).
    OCP console: *Observe → Network Traffic* shows flow graph + tabular flows. Filter by namespace, port, label, NetworkPolicy decision (allow/drop). For debugging "why is this connection refused?" + auditing east-west traffic.
    Use cases: NetworkPolicy validation (drops visible), microservice dependency mapping, DNS issue diagnosis, performance bottleneck identification.
    **Cluster Observability Operator (COO)** — unified config + multi-stack observability. Manages multiple Prometheus instances, Tempo, Loki across multiple Projects. Useful for multi-tenant OCP where each Project gets dedicated observability with shared backbone.
    Integration: SLO definitions in Prometheus rules; burn-rate alerts; cross-Operator dashboards in OCP console + external Grafana via Cluster Monitoring data sources.

## Before / After

**Before.** Pre-OCP-managed observability = self-installed Prometheus + Grafana + Loki + Jaeger + Hubble + 8 more Helm charts. Each chart's upgrade cycle independent; chart drift everywhere. No native fleet view. Apiserver / audit logs invisible without diagnostic-settings wiring. Tracing was bring-your-own.

**After.** OCP ships **Cluster Monitoring auto-enabled** (Prom + Thanos + Alertmanager); **User Workload Monitoring** for app metrics; **Logging Operator** (Loki + Vector); **Distributed Tracing Operator** (Tempo + OTel); **NetObserv Operator** (eBPF flow); **Cluster Observability Operator** for unified config. SLO-first alerting via Prometheus rules + Alertmanager.

*Each piece is a managed Operator with one Red Hat support contract; assemble vs DIY-Helm tradeoff is firmly in favour of managed.*

## Analogy — the K-Foundry bay

The **Control Tower** at K-Foundry watches all production. Three signal pipes + a network camera + a unified config console.
    The **Heartbeat Drum** (Cluster Monitoring) plays the foundry's vital signs — Prometheus collects platform metrics; Thanos Querier federates queries; Alertmanager routes alarms. The User Workload Drum (UWM) plays each Project's app-specific metrics.
    The **Story Scribe** (OpenShift Logging — Loki + Vector) writes everything narratable: app logs, infra logs, audit logs. LogQL queries the archive.
    The **Journey Tracker** (Distributed Tracing — Tempo + OTel) follows one request end-to-end across services. TraceQL queries the trace archive.
    The **NetObserv camera** records every Pod-to-Pod packet (eBPF). The **Cluster Observability Operator** conducts the whole orchestra — unified config across the four signal types + multi-stack support for multi-tenant Projects.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| Heartbeat Drum (platform vitals) | Cluster Monitoring — Prometheus + Thanos Querier + Alertmanager |
| Per-Project workload drum | User Workload Monitoring (UWM) |
| Story Scribe | OpenShift Logging — Loki + Vector |
| Three log streams | Application + Infrastructure + Audit log streams |
| Log archive query language | LogQL |
| Log-routing tablet | ClusterLogForwarder CR |
| Journey Tracker | OpenShift Distributed Tracing — Tempo + OpenTelemetry |
| Auto-instrumentation injector | OpenTelemetry Operator + Instrumentation CR |
| Trace query language | TraceQL |
| Network packet camera | Network Observability (NetObserv) Operator (eBPF) |
| Pod-to-Pod flow graph | OCP Console → Observe → Network Traffic |
| Cross-stack conductor | Cluster Observability Operator (COO) |
| Multi-tenant observability backbone | COO managed Prometheus + Tempo + Loki per Project |
| Phone-home health | Telemeter Client → Red Hat Insights |

⚠️ *Analogy stops here:* A real control tower has fixed vantage points; OCP's observability surfaces are software-defined and grow per Operator install. Cardinality explosions in Prometheus are a real failure mode the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** The Control Tower watches the whole foundry: heartbeat drums for vital signs, scribes writing every story, trackers following each visitor, cameras on every walkway. Plus a conductor making sure they all play together.

**ELI10.** OCP observability = built-in Cluster Monitoring (Prometheus + Thanos + Alertmanager) + UWM for app metrics; OpenShift Logging Operator (Loki + Vector — Fluentd deprecated, Elasticsearch deprecated); OpenShift Distributed Tracing Operator (Tempo + OpenTelemetry — Jaeger deprecated); NetObserv Operator (eBPF flow capture); Cluster Observability Operator (COO) for unified config + multi-tenant. SLO-first alerting via Prometheus rules + burn-rate.

## Real-world scenarios

- **SaaS — UWM + Tempo + Loki RED dashboard in console.** A SaaS team enables UWM + Logging + Tracing Operators. App emits prometheus_client + OTel spans. ServiceMonitor scrapes; OTel Collector forwards to Tempo. RED dashboard in console: Rate (Prom rate()), Errors (Prom counter), Duration (Tempo p95). Logs from same Pod available via console *Observe → Logs* in same view. *One console; minutes to dashboard; no external Grafana needed for basics.*
- **Bank — audit log forwarded to Splunk for SOC.** A bank requires apiserver audit logs in their SOC Splunk. ClusterLogForwarder CR routes audit stream to Splunk; application + infrastructure streams stay in Loki. Splunk consumers consume the Splunk-side; OCP team handles Loki-side ops. *Audit log isolation for compliance.*
- **Telco — NetObserv finds NetworkPolicy drops in 2 min.** Telco team enables NetObserv. Microservice A can't reach B; status: timeout. Open *Observe → Network Traffic*; filter by source-namespace=A, destination-namespace=B; see *NetworkPolicy drops* in flow data. NetworkPolicy in B's namespace was missing the allow-rule. Fixed in 2 minutes vs 30+ min of trial-and-error tcpdump.
- **Multi-tenant Project — COO carves dedicated observability.** An ISV runs multi-tenant OCP. Each tenant Project has its own observability requirements (different retention, different Slack channels for alerts, different Grafana orgs). COO manages per-Project Prometheus + Tempo + Loki configs from a central CR set. *Tenant isolation in observability without per-tenant Operator installs.*

## Common misconceptions

- **Myth:** "Fluentd is still the OCP log collector."
  **Truth:** **Fluentd is deprecated** in OpenShift Logging; **Vector** is the current collector. Likewise Elasticsearch backend is deprecated; **Loki** is the current store. Migration: install Logging Operator at current minor; LokiStack CR; ClusterLogForwarder. *Existing Fluentd + Elasticsearch installs need migration; don't deploy fresh on deprecated stack.*
- **Myth:** "Cluster Monitoring covers app metrics."
  **Truth:** **Cluster Monitoring covers platform metrics** (kubelet, apiserver, ClusterOperators, OperatorHub operators). For app metrics, enable **User Workload Monitoring** separately and create ServiceMonitor / PodMonitor CRs in your namespace.
- **Myth:** "Default retention is enough."
  **Truth:** Default Prometheus retention = 15 days; default Loki retention varies. **For compliance + post-incident analysis, plan long-term storage** (Thanos to S3 for metrics; Loki S3-backend for long-term logs; Tempo S3-backend for long-term traces). Without retention discipline, observability bills + storage explode + investigations stall on missing data.

## Recap

Built-in Cluster Monitoring + UWM for metrics; Logging Operator (Loki + Vector) for logs; Distributed Tracing Operator (Tempo + OTel) for traces; NetObserv for network flows; COO for unified config.

**Next — O12: OpenShift Troubleshooting.** oc adm must-gather; oc adm inspect; ClusterOperator degraded; CVO blocked; MCP degraded; Node NotReady; SCC denial; Route + cert issues; internal registry failure; Build failure; Operator CSV failed; CatalogSource failure; OLM Subscription issues; OVN-K + DNS; OAuth failures; etcd backup/restore; disconnected pull failures.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
