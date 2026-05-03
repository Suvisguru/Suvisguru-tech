# K-ECS C7 — C7 · ECS Observability — Container Insights, ECS Exec, FireLens, ADOT, X-Ray

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C7 · ECS Observability
> Companion preview: `/preview-kubernetes-ecs-lesson-07.html`.

---

**🎯 If you remember nothing else:** **Container Insights for cluster/service/task metrics. ECS Exec for live debug (no SSH). FireLens for log routing flexibility. ADOT + X-Ray for distributed tracing. Wire these before the incident, not during.**

## 1. Cluster + Service + Task metrics + dashboards

**Container Insights** auto-collects per-Cluster, per-Service, per-Task metrics: CPU + memory + network + storage I/O. Preconfigured CloudWatch dashboards aggregate per Cluster and Service. *Per-Task* metrics surface in CloudWatch Logs Insights via the `/aws/ecs/containerinsights/<cluster>/performance` log group.
    **Enabling**: account setting `aws ecs put-account-setting --name containerInsights --value enabled` (default for new clusters thereafter), or per-cluster `aws ecs update-cluster-settings --cluster X --settings name=containerInsights,value=enabled`.
    **Cost note**: Container Insights ingests metrics + Logs Insights performance log → metered as CloudWatch metrics + log ingest. For very-large fleets, the bill is real; budget accordingly. The trade-off (visibility vs cost) is usually overwhelmingly worth it but worth knowing.
    **Service-level dashboards**: aggregate `CPUUtilization`, `MemoryUtilization`, `RunningTaskCount`, `DesiredTaskCount`, `PendingTaskCount`. The PendingTaskCount > 0 metric is gold for catching capacity starvation early — wire an alarm.

## 2. Interactive shell via SSM, no SSH, CloudTrail-audited

**ECS Exec** opens a shell into a running container via the SSM Session Manager protocol. No inbound network port; no SSH key; no bastion. Use `aws ecs execute-command --cluster X --task ID --container Y --command "/bin/sh" --interactive`.
    **Prerequisites**:
    
      - Task Definition: `enableExecuteCommand: true` on the Service (or via RunTask).

      - Task role policy: `ssmmessages:CreateControlChannel`, `ssmmessages:CreateDataChannel`, `ssmmessages:OpenControlChannel`, `ssmmessages:OpenDataChannel`.

      - VPC connectivity: outbound to SSM Messages endpoint (or VPC endpoint `com.amazonaws.region.ssmmessages` for private-only VPCs).

      - Container has `/bin/sh` or another shell.

    
    **Audit**: every Exec session is logged to CloudTrail (`ecs:ExecuteCommand` + SSM `StartSession`). Optional CloudWatch Logs streaming of the session itself via the SSM logging configuration.
    **Why ECS Exec, not SSH?** SSH requires open ports + key management + bastion + per-host config. ECS Exec needs none of that. Works identically on Fargate (where you can't SSH at all) and EC2.

## 3. Fluent Bit / Fluentd sidecar; logs to anywhere

**FireLens** is a logConfiguration option (`logDriver: awsfirelens`) that routes container logs through a sidecar (Fluent Bit or Fluentd) which ships them anywhere. The sidecar runs in the same Task; consumes the app container's stdout/stderr; emits per its own routing config (Fluent Bit configmap or external file).
    **Why FireLens?** The default `awslogs` driver only ships to CloudWatch. FireLens unlocks *any destination*: CloudWatch (multiple log groups), S3 (cheaper archive), Kinesis Data Firehose / Streams (downstream pipelines), OpenSearch, Splunk, Datadog, Elasticsearch, custom HTTP. Combine routes — same log to CloudWatch (live ops) + S3 (long-term archive) + OpenSearch (search).
    **Sidecar pattern**: Task Definition has two containers — *app* (logConfiguration: awsfirelens) + *log_router* (Firelens-aware Fluent Bit image, essential: true). App stdout streams to the sidecar over Fluentd protocol; sidecar applies filters + routes per config.
    **Bottlerocket FireLens** [ deep dive — skip if new ]: on Bottlerocket-based EC2 hosts, a FireLens-as-host-daemon pattern is also possible — one log router per host, not per Task. Lower per-Task overhead at cost of less per-Task isolation.

## 4. OpenTelemetry collector + distributed tracing

**ADOT (AWS Distro for OpenTelemetry)**: an AWS-supported distribution of the OTel collector. Ship as a sidecar in your Task Definition; receive metrics + traces from your app via OTLP; export to CloudWatch (metrics), AWS Managed Prometheus (AMP), X-Ray (traces), or any OTel-compatible backend.
    **AWS X-Ray**: native distributed tracing service. Model: *segments* (top-level work unit, e.g., one HTTP request) + *subsegments* (downstream calls). SDKs for Java, Python, Node, Go, .NET, Ruby. ADOT exports OTel traces in X-Ray format.
    **Practical pattern**:
    
      - App instrumented with OTel SDK; emits OTLP to `localhost:4317` (gRPC) or `:4318` (HTTP).

      - ADOT sidecar receives OTLP; exports traces → X-Ray; metrics → CloudWatch + AMP.

      - ADOT task role allows `xray:PutTraceSegments`, CloudWatch `cloudwatch:PutMetricData`, AMP RemoteWrite if used.

    
    **Service Connect bonus**: if you're using Service Connect, the proxy already emits per-service metrics (rps, latency, 5xx) into Container Insights — adds layer-7 observability without instrumenting the app. Pair with ADOT for app-level traces and you have a complete picture.

## Before / After

**Before.** Pre-Container-Insights, ECS observability meant manually wiring CloudWatch alarms on individual ECS metrics + writing custom log shippers + SSHing to EC2 hosts to debug Tasks (or rebooting Tasks blindly on Fargate). Pre-ECS-Exec, Fargate Tasks were opaque — no shell access. Pre-FireLens, all logs went to CloudWatch via the awslogs driver — no S3 archive, no OpenSearch search, no Splunk integration without separate agents on each host.

**After.** Modern ECS observability is four well-defined layers: **Container Insights** (metrics + dashboards), **ECS Exec** (live debug shell, no SSH), **FireLens** (log routing flexibility), **ADOT + X-Ray** (metrics + traces). All wireable in Task Definitions or per-Cluster config. Audit-friendly (CloudTrail logs every Exec session). Works identically on Fargate and EC2.

*Wire all four before the incident. The marginal cost is small; the marginal value when something breaks is enormous.*

## Analogy — the K-Harbor pier

The harbor's **Lighthouse** is the highest point. Four observers work shifts there.
    The **weather observer** (Container Insights) keeps charts of every pier and ship — wind speed (CPU), tide level (memory), traffic count (network), warehouse activity (storage I/O). Daily dashboards show patterns across the whole harbor. When the pending-ship count starts climbing, an alarm fires before the harbor master notices.
    The **boarding inspector** (ECS Exec) can step onto any active ship and inspect it directly. No need to dock first; no boarding plank or ladder; the lighthouse keeper opens an authenticated channel to the ship's hold via the harbor's control system. Every visit is logged in the harbor's audit book.
    The **signal officer** (FireLens) reads every ship's logbook entries and routes them — the harbor's archive (CloudWatch), the long-term storage shed (S3), the foreign embassy office (OpenSearch / Splunk / Datadog), or the data pipeline (Kinesis). Same logbook entry can go to all four if needed.
    The **navigator** (ADOT + X-Ray) follows individual cargo journeys end-to-end — when a customer's shipment crosses three ships at three piers, the navigator pieces together the whole route and shows you where each leg took how long. Distributed traces.

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Lighthouse top | ECS observability layer |
| Weather observer | Container Insights — cluster/service/task metrics + dashboards |
| Boarding inspector | ECS Exec — interactive shell via SSM |
| Inspector's logged visits | CloudTrail audit of ecs:ExecuteCommand + SSM StartSession |
| Signal officer | FireLens — Fluent Bit / Fluentd sidecar |
| Foreign embassy office | OpenSearch / Splunk / Datadog destinations |
| Long-term storage shed | S3 log archive |
| Navigator | ADOT + X-Ray distributed tracing |
| End-to-end cargo journey | trace = segments + subsegments |
| Per-language journey log | OTel SDKs (Java / Python / Node / Go / .NET / Ruby) |

⚠️ *Analogy stops here:* A real lighthouse uses light + sound; ECS observability is API calls + log streams. The four layers map cleanly to the analogy but the costs (storage, ingest, indexing) are very different from a physical harbor's observation cost.

## ELI5 / ELI10

**ELI5.** Up at the lighthouse, four people watch the harbor. One reads the weather and writes daily reports. One can teleport onto any ship to look around. One reads everyone's logbooks and copies them to the right places. One follows individual packages from ship to ship to see how long each leg took. Together they show what's happening in the whole harbor.

**ELI10.** **Container Insights**: per-Cluster opt-in; preconfigured CPU/memory/network/I/O metrics + dashboards. **ECS Exec**: `execute-command` via SSM; needs `enableExecuteCommand` on Service + ssmmessages perms in task role; CloudTrail-audited. **FireLens**: `logDriver: awsfirelens` + sidecar Fluent Bit/Fluentd; routes to anywhere. **ADOT + X-Ray**: OTel collector sidecar; receives OTLP from app; exports to X-Ray (traces) + CloudWatch / AMP (metrics).

## Real-world scenarios

- **Production wire-up — all four enabled by default.** A 100-engineer org has a Service Catalog template that every new ECS Service uses. Template includes: Container Insights enabled at Cluster level, Task role with ssmmessages perms (ECS Exec), FireLens sidecar routing logs to CloudWatch + S3 + OpenSearch, ADOT sidecar exporting OTel metrics to CloudWatch + traces to X-Ray. *Every new Service has full observability on day 1.*
- **3 AM debug — ECS Exec saved the night.** On-call engineer pages on a Fargate Service with intermittent 5xx. SSH not available; she runs `aws ecs execute-command --interactive --command "/bin/sh"` into a single Task; runs `netstat` + `nslookup` + reads in-memory state. Finds a stale DNS cache from a downstream service rotation. Restarts the Task; problem clears. Long-term fix: shorter DNS TTL. *Without ECS Exec, this would have been hours of trial-and-error restarts.*
- **Compliance — every log to S3 archive + CloudWatch live.** A regulated workload requires 7-year log retention. FireLens config routes *all* container logs to **two** destinations: CloudWatch (14-day live retention for ops) + S3 (Glacier-archive after 30 days for the 7-year requirement). Same log entry; two destinations. CloudWatch costs stay bounded; S3 archive cost is pennies/GB-year.
- **Outage — no traces meant no answer.** A team had Container Insights + FireLens but no ADOT/X-Ray. A Service had P95 latency tail 3× normal but only on one specific endpoint. CloudWatch metrics showed the spike; logs showed nothing useful (the slow path didn't crash). Without distributed traces, root cause stayed hidden for 2 days until a new engineer reproduced the call manually and found the slow downstream. *Postmortem*: ADOT + X-Ray on every Service.

## Common misconceptions

- **Myth:** "Container Insights is on by default for new Clusters."
  **Truth:** **Off by default unless** the account-level setting `containerInsights = enabled` is set first (then new Clusters inherit it). Existing Clusters need explicit per-cluster enable. Audit your Clusters; you'll likely find some without it.
- **Myth:** "ECS Exec is just SSH for ECS."
  **Truth:** ECS Exec uses **SSM Session Manager** — no inbound network, no SSH keys, no bastion. The auth path is IAM (your principal needs `ecs:ExecuteCommand`); the Task needs SSM Messages perms in its task role. Different machinery; auditable via CloudTrail; works on Fargate where SSH doesn't exist.
- **Myth:** "FireLens replaces awslogs everywhere."
  **Truth:** FireLens is more flexible but adds a sidecar Task overhead (Fluent Bit container ~30MB memory). For simple workloads where CloudWatch is the only log destination, plain `awslogs` driver is fine — less ops surface. Pick FireLens when you need multi-destination routing or filtering.

## Recap

Four observability layers — Container Insights, ECS Exec, FireLens, ADOT + X-Ray. Wire them before incidents. Container Insights for at-a-glance health. ECS Exec for live debug. FireLens for log destination flexibility. ADOT + X-Ray for distributed tracing.

**Next — C8: ECS Anywhere and Hybrid.** ECS control plane managing on-prem / edge servers; SSM agent + ECS agent registration; networking + storage limits on external instances; use cases (regulated, edge processing, gradual cloud migration).

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
