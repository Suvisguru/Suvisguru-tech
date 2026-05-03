# K-EKS E8 — E8 · EKS Observability (Container Insights, AMP, AMG, ADOT, X-Ray, control-plane logs)

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E8 · EKS Observability
> Companion preview: `/preview-kubernetes-eks-lesson-08.html`.

---

**🎯 If you remember nothing else:** AWS-native EKS observability: **CloudWatch Container Insights (enhanced)** for Pod/node metrics + logs; **Amazon Managed Prometheus (AMP)** for scaled metrics; **Amazon Managed Grafana (AMG)** for dashboards (IAM SSO); **ADOT** (AWS Distro for OpenTelemetry) collector → AMP / X-Ray; **Fluent Bit → CloudWatch Logs** for app logs; **X-Ray** for distributed traces; **Control-plane logs** (api / audit / authenticator / controllerManager / scheduler) → CloudWatch; **AWS Split Cost Allocation Data** for per-namespace cost.

## 1. Two paths: AWS-native vs OSS-on-AWS

For EKS observability you can run either:
    
      - **AWS-native**: CloudWatch Container Insights + Logs + X-Ray. Pay-per-use; no infra to operate; tight IAM integration; comes pre-wired into many AWS services.

      - **OSS-on-AWS**: AMP (managed Prometheus) + AMG (managed Grafana) + ADOT (managed OTel collector). Same OSS APIs (PromQL, Grafana dashboards) but AWS handles the infra.

    
    Most teams in 2026 use a hybrid: **CloudWatch for control-plane + node + container logs** (free first-tier, deeply integrated); **AMP + AMG for app metrics + dashboards** (PromQL + open Grafana ecosystem); **X-Ray or Tempo via OTel for traces**; **Fluent Bit** ships logs to CloudWatch + optionally to a SIEM.

## 2. Pods + nodes + control-plane in one console

**Container Insights enhanced** (released 2023): Pod-level + node-level metrics + logs in CloudWatch with native EKS dashboards. Setup: enable observability via the EKS console or CLI; AWS deploys a managed CloudWatch agent + Fluent Bit DaemonSet.
    `# Enable Container Insights via add-on
aws eks create-addon \
  --cluster-name prod \
  --addon-name amazon-cloudwatch-observability`
    Provides:
    
      - Per-Pod CPU + memory + filesystem + network

      - Per-node aggregated metrics

      - Per-namespace cost (with Split Cost Allocation enabled)

      - Container-level logs via Fluent Bit (managed) → CloudWatch Log Groups

      - Pre-built dashboards covering cluster health + workload trends

    
    **Cost**: GB-ingested for logs + per-metric for custom metrics. For a typical 50-Pod cluster: $50-200/month.

## 3. Managed Prometheus + Grafana for EKS

**Amazon Managed Service for Prometheus (AMP)**: serverless Prometheus-compatible metrics store. Accepts `remote_write` from in-cluster collectors; serves PromQL queries. Pay per ingestion + storage. No Prometheus servers to operate.
    **Amazon Managed Grafana (AMG)**: serverless Grafana. IAM Identity Center SSO; data sources include AMP, CloudWatch, X-Ray. Pay per active user.
    **AWS Distro for OpenTelemetry (ADOT)**: AWS-supported OTel collector. Run as DaemonSet (collect node + Pod telemetry) + Deployment (gateway-style aggregation). Routes to AMP, X-Ray, CloudWatch, third-party.
    `# ADOT collector config (snippet)
exporters:
  awsxray: {}
  prometheusremotewrite:
    endpoint: https://aps-workspaces.us-east-1.amazonaws.com/.../api/v1/remote_write
    auth:
      authenticator: sigv4auth
  awscloudwatchlogs:
    log_group_name: /aws/eks/prod/app-logs

service:
  pipelines:
    metrics:
      receivers: [prometheus]
      exporters: [prometheusremotewrite]
    traces:
      receivers: [otlp]
      exporters: [awsxray]
    logs:
      receivers: [otlp]
      exporters: [awscloudwatchlogs]`

## 4. The other essentials

- **Control-plane logs** (opt-in, *enable on every cluster*): five types — api, audit, authenticator, controllerManager, scheduler — to CloudWatch Log Groups. Required for compliance + debugging "the apiserver did/didn't...". Costs ~$5-50/month per cluster depending on volume.

      - **X-Ray**: AWS-native distributed tracing. ADOT collector sends spans; X-Ray UI shows service maps + per-trace timing. Alternative: Tempo / Jaeger backed by OSS Grafana stack.

      - **AWS Split Cost Allocation Data for EKS**: enable in Cost Explorer; AWS attributes EC2 + EBS costs to specific Pods + namespaces using Container Insights data. *The right way to answer "what does team X cost?"*

      - **Per-tool integration**: Datadog, New Relic, Honeycomb, Grafana Cloud all integrate via ADOT or their own DaemonSets. Often paired with AWS-native at base layer.

    
    [ deep dive — skip if new ]For high-cardinality metrics + long retention, AMP scales to 100M active series (vs OSS Prometheus single-instance ceiling ~10M). Or use Mimir / Cortex / Thanos for full self-managed at scale; AMP for managed.

## Before / After

**Before.** OSS Prometheus + Grafana installed via Helm 6 months ago. Stopped scraping after a kubelet upgrade; nobody noticed. No control-plane logs. Per-team cost = wishful spreadsheet.

**After.** Container Insights for K8s metrics. AMP + AMG for app dashboards (PromQL + Grafana). ADOT for trace ingestion to X-Ray + Tempo. Fluent Bit ships logs. Control-plane logs always on. Split Cost Allocation breaks down per-namespace cost.

EKS observability with managed services costs roughly the same as OSS but with zero ops + tighter IAM. The trade for hybrid: standardise on PromQL + Grafana for portability while AWS-managing the infra.

## Analogy — the K-Skyline floor

The Observation Deck is the floor with the panoramic glass. Multiple instruments here. The **cluster status panel** (Container Insights) shows every Pod + node metric in one place. The **star map** (AMP + AMG) renders all the application telemetry into Grafana dashboards. The **relay router** (ADOT) sits in the data flow, sending metrics to AMP, traces to X-Ray, logs to CloudWatch. The **activity ledger** (control-plane logs) records every API request. And on a separate desk: the **cost-allocation report** showing what each tenant's slice of the building cost this month.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Cluster status panel | CloudWatch Container Insights enhanced |
| Star map dashboards | AMG (Managed Grafana) |
| Star data store | AMP (Managed Prometheus) |
| Telemetry relay router | ADOT (AWS Distro for OTel) collector |
| Activity ledger | Control-plane logs (api/audit/authn/cm/scheduler) |
| Trail of every request through the building | X-Ray traces |
| Building log archive | CloudWatch Logs (Fluent Bit DaemonSet) |
| Per-tenant utility breakdown | AWS Split Cost Allocation Data for EKS |

⚠️ *Analogy stops here:* The analogy stops here: real EKS observability is N agents + collectors writing to N AWS services + IAM permissions + cost models. The deck metaphor undersells the integration work.

## ELI5 / ELI10

**ELI5.** Lots of windows looking at the cluster. Some show numbers, some show pictures, some show what every visitor did. AWS provides the windows; you decide what to display.

**ELI10.** Two-path observability: AWS-native (CloudWatch Container Insights + Logs + X-Ray) or OSS-on-AWS (AMP + AMG + ADOT). Most teams hybrid: Container Insights for cluster health + control-plane logs; AMP + AMG for app metrics; ADOT for ingestion to multiple destinations; X-Ray or Tempo for traces; Fluent Bit for log shipping; Split Cost Allocation for per-namespace cost.

## Real-world scenarios

- **A SaaS using AWS-native end-to-end.** Container Insights enhanced enabled at cluster create. ADOT collector ships PromQL metrics to AMP + traces to X-Ray + logs to CloudWatch. AMG dashboards via IAM Identity Center SSO. Total observability cost: ~$300/month for a 50-Pod cluster. Zero ops on observability infra.
- **A bank running hybrid: AMP + AMG + Datadog.** AMP + AMG as the primary K8s metrics + dashboard. Datadog APM for app traces (existing licence). Both feed Container Insights + control-plane logs into a SIEM. Cost: managed AWS + Datadog licences ~$2K/month for 200-node cluster.
- **A startup using OSS Prometheus + Grafana on EKS for cost.** kube-prometheus-stack via Helm. Self-hosted Grafana. Cheaper at small scale; SRE time invested. Migrate to AMP + AMG when scale or ops cost passes the threshold.
- **A team using Split Cost Allocation.** Per-namespace cost report shared with each team monthly. Team A: $2400/month. Team B: $480. Team C: $5800 (turns out they were running an unused load-test cluster constantly). Visibility drove a 30% cluster spend reduction in 2 months.

## Common misconceptions

- **Myth:** "AMP is just remote Prometheus."
  **Truth:** AMP exposes the same APIs (remote_write + PromQL) but it's a managed scaled service handling 100M+ active series. No Prometheus server you operate. Different operational shape.
- **Myth:** "Control-plane logs are noise; skip them."
  **Truth:** Audit logs are required for compliance, breach forensics, and root-causing apiserver issues. Volume tunable via audit policy. Always enable from cluster create.
- **Myth:** "Container Insights replaces application observability."
  **Truth:** Container Insights is K8s + node metrics. App-level metrics + traces + logs still need OTel SDKs in your apps. Container Insights complements; doesn't replace.

## Recap

Observability stack = CloudWatch Container Insights (cluster health) + AMP / AMG (app metrics + dashboards) + ADOT (ingestion) + X-Ray (traces) + Fluent Bit (logs) + control-plane logs to CloudWatch + Split Cost Allocation. Most enable at cluster create.

**Next — E9: EKS Upgrades and Operations.** Standard support, extended support, version skew, control-plane + node + add-on upgrades, blue-green migration.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
