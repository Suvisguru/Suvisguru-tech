# K-AKS A7 — A7 · AKS Observability (Container Insights, AMP, AMG, ADOT, App Insights)

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A7 · AKS Observability
> Companion preview: `/preview-kubernetes-aks-lesson-07.html`.

---

**🎯 If you remember nothing else:** **Three pipes (metrics → AMP, logs → Log Analytics, traces → App Insights / managed OTel) joined in Managed Grafana. Container Insights for K8s-aware visualisation; KQL for log search; control-plane diagnostic settings to capture audit + apiserver logs.**

## 1. Container Insights + Managed Prometheus (AMP)

**Container Insights** = AKS-aware metrics + log dashboard, built on Log Analytics. Enable the `monitoring` add-on; an OMS agent DaemonSet ships node + Pod + container metrics + container stdout/stderr logs to a Log Analytics workspace. *Pre-built workbooks*: cluster overview, node health, Pod distribution, top-CPU containers.
    **Azure Monitor managed Prometheus (AMP)** = Microsoft's managed Prometheus-as-a-service. AKS add-on installs the metrics collector (Prometheus Receiver / Azure Monitor Metrics Add-on); cluster + Pod metrics are scraped and stored in AMP. *Compatible with PromQL* + Prometheus alerting. Use AMP for *red-line metrics* (RED: rate, errors, duration; USE: utilization, saturation, errors).
    **Container Insights vs AMP**: complementary, not competing. *Container Insights* = AKS-aware visualization + log integration. *AMP* = open-format Prometheus metrics with PromQL + alerting + Grafana compatibility. Most production AKS clusters enable both.
    **Azure Managed Grafana (AMG)** consumes AMP, Application Insights, Log Analytics, and Azure Monitor as data sources — *one dashboard for all signal types*. Enterprise tier adds RBAC integration with Entra. Pre-built dashboards for AKS ship in the AMG gallery.

## 2. Log Analytics + KQL — log search

**Log Analytics workspace** is Azure's log store. Container Insights writes container logs (`ContainerLogV2` table), kubelet events, and node syslog. Apiserver / audit logs land here too via diagnostic settings. *Standard for AKS deployments — central log destination.*
    **KQL (Kusto Query Language)** is the query language. SQL-like but pipe-based. Example: find all CrashLoopBackOff events in the last hour grouped by Pod:
    `KubeEvents
| where TimeGenerated > ago(1h)
| where Reason == "BackOff"
| summarize Count = count() by PodName, Namespace
| order by Count desc`
    Standard tables: `ContainerLogV2`, `KubeEvents`, `KubeNodeInventory`, `KubePodInventory`, `InsightsMetrics`. *Saved KQL queries* can power alerts ("alert if X CrashLoopBackOff in 5 min") and Grafana panels.
    **Cost levers:** log ingest is the typical AKS observability cost driver. *Sample container logs* in Container Insights config (e.g. drop verbose stdout in dev); *basic logs* tier for high-volume low-query data; *retention period* per table; *Data Collection Rules (DCRs)* route subsets to cheaper destinations.

## 3. App Insights + Azure Monitor managed OpenTelemetry

**Application Insights** is Azure's app-performance monitoring product. Auto-instruments .NET / Node / Python / Java apps with traces, exceptions, dependency maps, transaction details. *End-to-end transaction traces* across services + Azure Functions + SQL DB.
    **Azure Monitor managed OpenTelemetry** = Microsoft's managed OTel-compatible ingestion endpoint (also called the *Azure Monitor OpenTelemetry Distro*). For polyglot teams or open-standard purists. Same backend as App Insights but the collector is OTel-native — your code emits OTel spans/metrics/logs; ADOT-compatible collectors export to Azure Monitor.
    **Pick:** App Insights for .NET-heavy / Microsoft-stack teams who want zero-config auto-instrumentation. Managed OpenTelemetry for polyglot / OSS-leaning teams who want vendor-neutral instrumentation.
    **Tracing patterns:** propagate W3C Trace Context (`traceparent`) across services for end-to-end joins. Sample at the edge (10% of low-value, 100% of errors). Span tagging with K8s metadata (Pod name, namespace, node) makes spans correlatable with metrics.

## 4. Control-plane diagnostic settings, Network Observability, Cost Management

**Control-plane diagnostic settings** — enable apiserver, audit, audit-admin, controller-manager, scheduler, cluster-autoscaler, cloud-controller-manager log categories to flow to Log Analytics (or Event Hub / Storage). *Audit logs are essential for security forensics.* AKS Standard / Premium tier required for the long retention windows.
    **Network Observability** — AKS add-on (preview/GA) that captures Pod-to-Pod flow data (Hubble for Cilium clusters; eBPF on Azure CNI Powered by Cilium). Visualizes east-west traffic, NetworkPolicy drops, DNS lookups. Surfaces hard-to-debug "why is this connection refused?" at the L4/L7 layer.
    **Azure Cost Management** for AKS — enable *cost analysis with namespace-level granularity* (preview/GA depending on region). Surfaces per-namespace spend (split by compute, storage, network, log ingest). Without this you can see cluster total but not which team owns which slice — chargeback breaks.
    **Alerting:** AMP supports Prometheus alerting rules → Action Groups → PagerDuty / Teams / email. Log Analytics supports KQL-based alerts. App Insights supports smart-detection alerts. Combine in *Azure Monitor Action Groups* as a single notification channel set.

## Before / After

**Before.** Pre-managed AKS observability = Bring Your Own Prometheus + Bring Your Own Grafana + Bring Your Own log shipper (Fluent Bit / Filebeat) + ELK or Loki + custom alert routing. Operators ran 5+ Helm charts and a separate VMSS for the metrics+logs stack. AKS apiserver logs were essentially invisible without diagnostic-settings wiring. Tracing was unsupported in the basic stack — App Insights existed but was a separate sale.

**After.** Modern AKS gives you **Container Insights** (AKS-aware) + **AMP** (managed Prometheus) + **AMG** (managed Grafana) + **App Insights / managed OpenTelemetry** (traces) + **Log Analytics** (logs) + **Network Observability** + **Cost Management** at namespace granularity — all enabled with az CLI flags or AKS Automatic defaults. *One add-on each, one Grafana, one alert channel.*

*The DIY observability era is over. Five managed services replace a 12-component homemade stack at a fraction of operational cost.*

## Analogy — the K-Campus wing

The **Bell Tower** at K-Campus is where everything that happens on campus is heard. Three different bells ring for three different signals.
    The **Tempo Bell** (metrics) rings on a regular cadence — once a minute it bongs the campus heartbeat: "how full are the buildings? how many students are walking? how warm is the HVAC?" The Container Insights bell-ringer hears campus-aware patterns; the Managed Prometheus (AMP) bell-ringer follows industry-standard PromQL bell patterns.
    The **Story Bell** (logs) chimes whenever something narratable happens — "Professor Jones entered building C", "a student couldn't find a room", "the Auditorium HVAC threw an error." The bell echoes are recorded in the Log Analytics archive; you query the archive in **KQL** to find patterns ("how many 'door is jammed' chimes in the last hour?").
    The **Journey Bell** (traces) follows a single visitor end-to-end — "this visitor entered through the South Gate, walked to Building A, talked to Reception, was directed to Building C, met Professor Y, signed a form." The Application Insights bell-ringer sketches the path; the managed OpenTelemetry bell-ringer uses an open notation any visiting bell-ringer understands.
    All three bell-ringers also hand their notes to the **Bell Tower Curator** (Azure Managed Grafana) who composes one master dashboard everyone can read.

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| Tempo Bell | Metrics |
| Container Insights bell-ringer | Container Insights — AKS-aware metrics view |
| AMP bell-ringer | Azure Monitor managed Prometheus — PromQL |
| Story Bell | Logs |
| Story Bell archive | Log Analytics workspace |
| Story-archive query language | KQL (Kusto Query Language) |
| Journey Bell | Traces |
| Journey Bell .NET-savvy ringer | Application Insights |
| Journey Bell open-notation ringer | Azure Monitor managed OpenTelemetry |
| Bell Tower Curator | Azure Managed Grafana (AMG) |
| Apiserver-meeting transcripts | Control-plane diagnostic settings |
| "Who walked from A to C?" | Network Observability (Hubble / Cilium eBPF) |
| Per-department budget ledger | Azure Cost Management — per-namespace cost |

⚠️ *Analogy stops here:* A bell tower has three independent bells; in real Azure, signal types share a backend (Log Analytics underlies Container Insights and apiserver logs) — the metaphor over-separates them.

## ELI5 / ELI10

**ELI5.** A tower with three bells. One says how busy the campus is right now. One records every story so you can search it later. One follows one person through the day. They all also write to the same big poster everyone can read.

**ELI10.** AKS observability = three signal pipes joined in **AMG**. **Metrics:** Container Insights (AKS-aware) + AMP (managed Prometheus, PromQL). **Logs:** Log Analytics + KQL queries. **Traces:** Application Insights (zero-config for .NET) or managed OpenTelemetry (vendor-neutral OSS). Plus **control-plane diagnostic settings** (apiserver / audit / scheduler / etc. → Log Analytics), **Network Observability** (Hubble eBPF flows), **Cost Management** (per-namespace). All visible in AMG dashboards; alerts route via Action Groups.

## Real-world scenarios

- **SaaS — RED dashboard in AMG built from AMP + App Insights.** A SaaS team builds a per-service RED dashboard (Rate, Errors, Duration) in AMG. *Rate* + *Errors* from AMP via PromQL on Pod-emitted metrics; *Duration* from Application Insights percentile metrics. One dashboard joins both data sources; on-call sees red-line indicators per service in 30 seconds. *MTTR for a typical p99 spike: 11 minutes vs 35 before AMG.*
- **Bank — apiserver audit log to Sentinel for SOC.** A bank enables AKS apiserver + audit + audit-admin diagnostic settings to a dedicated Log Analytics workspace, mirrored to Sentinel. Sentinel rules detect: kubectl exec into Pods in prod namespaces, RoleBinding changes outside CI, secret reads outside expected SAs. *SOC owns the AKS audit story; platform team gets the alert routing.*
- **Cost — per-namespace chargeback rolled out across tenant clusters.** A multi-tenant SaaS platform team enables Cost Management with per-namespace granularity. Monthly export to a Storage Account; PowerBI report joins namespace → tenant mapping. *Tenants now see their actual cost; over-provisioned tenants get bills that prompt resource cleanup; finance has chargeback.*
- **Polyglot team — managed OpenTelemetry replaces a Jaeger DIY stack.** A 30-service team had been running self-hosted Jaeger for traces. Migration: instrument apps with OpenTelemetry SDKs; configure exporters to **Azure Monitor managed OpenTelemetry**. Traces appear in App Insights with the same data model. *Decommissioned Jaeger + Cassandra backend; -3 components to operate.*

## Common misconceptions

- **Myth:** "Container Insights and AMP do the same thing."
  **Truth:** Complementary. **Container Insights** = K8s-aware visualization built on Log Analytics; great for cluster overview, top-CPU containers, node health workbooks. **AMP** = open-format Prometheus metrics + PromQL + Prometheus alerting. AMP integrates with Grafana naturally; Container Insights answers "is my cluster healthy?" out of the box.
- **Myth:** "Tracing is only worth it for big distributed systems."
  **Truth:** Even a 3-service deployment benefits from traces — the moment a request crosses one service boundary, log-based debugging becomes a join problem. App Insights / managed OpenTelemetry auto-instrument enough for these gains in days, not weeks. The cost is small relative to the MTTR reduction on user-facing latency issues.
- **Myth:** "Log Analytics retention defaults are fine."
  **Truth:** Defaults are 30 days for most tables — too short for compliance (often 1 year) and too long for high-volume verbose logs (often days). Tune per-table retention. Use Basic Logs tier for high-volume infrequent-query data; Archive tier for compliance retention with infrequent reads. Without this discipline log ingest costs dominate AKS spend.

## Recap

Three pipes (metrics + logs + traces) joined in Managed Grafana; control-plane diagnostic settings + Network Observability + Cost Management close the loop. Cost-tune log ingest with filters + tiers + retention.

**Next — A8: AKS Add-ons and Platform Features.** Managed add-ons (KEDA, Dapr, Istio service mesh, Flux v2 GitOps, Workload Identity, Key Vault Secrets Provider, App Routing), Azure Arc-enabled K8s, AKS hybrid (Azure Local / Edge Essentials), Fleet Manager.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
