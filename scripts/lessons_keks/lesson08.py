from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Observation deck: panes labeled CloudWatch Container Insights, AMP, AMG, ADOT, X-Ray, control-plane logs, Split Cost Allocation.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">OBSERVATION DECK · EKS OBSERVABILITY STACK</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <rect x="14" y="34" width="180" height="40" rx="3" fill="#3F4A5E"/><text x="104" y="50" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">CloudWatch Container Insights</text><text x="104" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">enhanced — Pods + nodes</text>
    <rect x="200" y="34" width="180" height="40" rx="3" fill="#A04832"/><text x="290" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">AMP (Managed Prometheus)</text><text x="290" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">scrape + remote-write</text>
    <rect x="386" y="34" width="200" height="40" rx="3" fill="#5A9F7A"/><text x="486" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">AMG (Managed Grafana)</text><text x="486" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">dashboards + IAM SSO</text>
    <rect x="14" y="80" width="180" height="40" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="104" y="96" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">ADOT (OTel)</text><text x="104" y="108" text-anchor="middle" font-size="7" fill="#5A4F45">collector → AMP / X-Ray</text>
    <rect x="200" y="80" width="180" height="40" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="290" y="96" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">Fluent Bit → CloudWatch Logs</text>
    <rect x="386" y="80" width="200" height="40" rx="3" fill="#E0EEF3" stroke="#4A8FA8"/><text x="486" y="96" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">X-Ray (traces)</text>
    <rect x="14" y="126" width="572" height="22" rx="3" fill="#3F4A5E"/><text x="300" y="140" text-anchor="middle" font-size="8" fill="#FBF1D6">Control-plane logs (api/audit/authenticator/cm/scheduler) → CloudWatch · Split Cost Allocation per namespace</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="08",
    title_short="observability",
    title_full="E8 · EKS Observability (Container Insights, AMP, AMG, ADOT, X-Ray, control-plane logs)",
    title_html="K-EKS E8 · EKS Observability",
    module_eyebrow="Module E8 · the observation deck",
    hero_sub_html='AWS-native observability stack for EKS: <strong>CloudWatch Container Insights</strong> for K8s metrics + logs; <strong>AMP / AMG</strong> for Prometheus + Grafana managed; <strong>ADOT</strong> (AWS Distro for OpenTelemetry) for ingestion; <strong>X-Ray</strong> for traces; <strong>control-plane logs</strong> to CloudWatch; <strong>Split Cost Allocation Data</strong> for per-namespace cost.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Outage at 2 AM. The on-call SRE opens the dashboards: blank. The team had <em>installed</em> Prometheus + Grafana six months ago, but it stopped scraping after a kubelet upgrade. Nobody noticed because nobody looked. Or: control-plane audit logs were never enabled — when AWS support asks for them to debug an apiserver issue, you have nothing. <em>EKS observability is opt-in, not on-by-default</em>. This module is the launch-time checklist.',
    stamp_html='AWS-native EKS observability: <strong>CloudWatch Container Insights (enhanced)</strong> for Pod/node metrics + logs; <strong>Amazon Managed Prometheus (AMP)</strong> for scaled metrics; <strong>Amazon Managed Grafana (AMG)</strong> for dashboards (IAM SSO); <strong>ADOT</strong> (AWS Distro for OpenTelemetry) collector → AMP / X-Ray; <strong>Fluent Bit → CloudWatch Logs</strong> for app logs; <strong>X-Ray</strong> for distributed traces; <strong>Control-plane logs</strong> (api / audit / authenticator / controllerManager / scheduler) → CloudWatch; <strong>AWS Split Cost Allocation Data</strong> for per-namespace cost.',
    district_pin="ks-floor08",
    district_label="Observation Deck",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Two paths: AWS-native vs OSS-on-AWS",
            body_html="""    <p>For EKS observability you can run either:</p>
    <ul>
      <li><strong>AWS-native</strong>: CloudWatch Container Insights + Logs + X-Ray. Pay-per-use; no infra to operate; tight IAM integration; comes pre-wired into many AWS services.</li>
      <li><strong>OSS-on-AWS</strong>: AMP (managed Prometheus) + AMG (managed Grafana) + ADOT (managed OTel collector). Same OSS APIs (PromQL, Grafana dashboards) but AWS handles the infra.</li>
    </ul>
    <p>Most teams in 2026 use a hybrid: <strong>CloudWatch for control-plane + node + container logs</strong> (free first-tier, deeply integrated); <strong>AMP + AMG for app metrics + dashboards</strong> (PromQL + open Grafana ecosystem); <strong>X-Ray or Tempo via OTel for traces</strong>; <strong>Fluent Bit</strong> ships logs to CloudWatch + optionally to a SIEM.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · CloudWatch Container Insights",
            h2="Pods + nodes + control-plane in one console",
            body_html="""    <p><strong>Container Insights enhanced</strong> (released 2023): Pod-level + node-level metrics + logs in CloudWatch with native EKS dashboards. Setup: enable observability via the EKS console or CLI; AWS deploys a managed CloudWatch agent + Fluent Bit DaemonSet.</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># Enable Container Insights via add-on
aws eks create-addon \\
  --cluster-name prod \\
  --addon-name amazon-cloudwatch-observability</code></pre>
    <p>Provides:</p>
    <ul>
      <li>Per-Pod CPU + memory + filesystem + network</li>
      <li>Per-node aggregated metrics</li>
      <li>Per-namespace cost (with Split Cost Allocation enabled)</li>
      <li>Container-level logs via Fluent Bit (managed) → CloudWatch Log Groups</li>
      <li>Pre-built dashboards covering cluster health + workload trends</li>
    </ul>
    <p><strong>Cost</strong>: GB-ingested for logs + per-metric for custom metrics. For a typical 50-Pod cluster: $50-200/month.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · AMP + AMG + ADOT",
            h2="Managed Prometheus + Grafana for EKS",
            body_html="""    <p><strong>Amazon Managed Service for Prometheus (AMP)</strong>: serverless Prometheus-compatible metrics store. Accepts <code>remote_write</code> from in-cluster collectors; serves PromQL queries. Pay per ingestion + storage. No Prometheus servers to operate.</p>
    <p><strong>Amazon Managed Grafana (AMG)</strong>: serverless Grafana. IAM Identity Center SSO; data sources include AMP, CloudWatch, X-Ray. Pay per active user.</p>
    <p><strong>AWS Distro for OpenTelemetry (ADOT)</strong>: AWS-supported OTel collector. Run as DaemonSet (collect node + Pod telemetry) + Deployment (gateway-style aggregation). Routes to AMP, X-Ray, CloudWatch, third-party.</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># ADOT collector config (snippet)
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
      exporters: [awscloudwatchlogs]</code></pre>""",
        ),
        Section(
            eyebrow="Section 1.9 · Control-plane logs + X-Ray + cost",
            h2="The other essentials",
            body_html="""    <ul>
      <li><strong>Control-plane logs</strong> (opt-in, <em>enable on every cluster</em>): five types — api, audit, authenticator, controllerManager, scheduler — to CloudWatch Log Groups. Required for compliance + debugging \"the apiserver did/didn\'t...\". Costs ~$5-50/month per cluster depending on volume.</li>
      <li><strong>X-Ray</strong>: AWS-native distributed tracing. ADOT collector sends spans; X-Ray UI shows service maps + per-trace timing. Alternative: Tempo / Jaeger backed by OSS Grafana stack.</li>
      <li><strong>AWS Split Cost Allocation Data for EKS</strong>: enable in Cost Explorer; AWS attributes EC2 + EBS costs to specific Pods + namespaces using Container Insights data. <em>The right way to answer \"what does team X cost?\"</em></li>
      <li><strong>Per-tool integration</strong>: Datadog, New Relic, Honeycomb, Grafana Cloud all integrate via ADOT or their own DaemonSets. Often paired with AWS-native at base layer.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For high-cardinality metrics + long retention, AMP scales to 100M active series (vs OSS Prometheus single-instance ceiling ~10M). Or use Mimir / Cortex / Thanos for full self-managed at scale; AMP for managed.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your EKS cluster has been running 2 months. AWS Support asks for the apiserver audit log for an investigation. You realise it was never enabled. What now?',
            options=[
                ('a) AWS has the logs anyway in their internal systems', False),
                ('b) Enable control-plane logs now; AWS only has logs from when you enabled it forward — the past 2 months are gone for that cluster', True),
                ('c) Reboot the cluster to recover them', False),
            ],
            feedback='<strong>Answer: b.</strong> Control-plane logs are opt-in per cluster. AWS doesn\'t store them retroactively. Enable on every cluster at create time. Document the launch-time checklist + audit quarterly.',
        ),
    },
    before_after_before='<p>OSS Prometheus + Grafana installed via Helm 6 months ago. Stopped scraping after a kubelet upgrade; nobody noticed. No control-plane logs. Per-team cost = wishful spreadsheet.</p>',
    before_after_after='<p>Container Insights for K8s metrics. AMP + AMG for app dashboards (PromQL + Grafana). ADOT for trace ingestion to X-Ray + Tempo. Fluent Bit ships logs. Control-plane logs always on. Split Cost Allocation breaks down per-namespace cost.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">EKS observability with managed services costs roughly the same as OSS but with zero ops + tighter IAM. The trade for hybrid: standardise on PromQL + Grafana for portability while AWS-managing the infra.</p>',
    analogy_intro_html='<p>The Observation Deck is the floor with the panoramic glass. Multiple instruments here. The <strong>cluster status panel</strong> (Container Insights) shows every Pod + node metric in one place. The <strong>star map</strong> (AMP + AMG) renders all the application telemetry into Grafana dashboards. The <strong>relay router</strong> (ADOT) sits in the data flow, sending metrics to AMP, traces to X-Ray, logs to CloudWatch. The <strong>activity ledger</strong> (control-plane logs) records every API request. And on a separate desk: the <strong>cost-allocation report</strong> showing what each tenant\'s slice of the building cost this month.</p>',
    translation_rows=[
        ('Cluster status panel', 'CloudWatch Container Insights enhanced'),
        ('Star map dashboards', 'AMG (Managed Grafana)'),
        ('Star data store', 'AMP (Managed Prometheus)'),
        ('Telemetry relay router', 'ADOT (AWS Distro for OTel) collector'),
        ('Activity ledger', 'Control-plane logs (api/audit/authn/cm/scheduler)'),
        ('Trail of every request through the building', 'X-Ray traces'),
        ('Building log archive', 'CloudWatch Logs (Fluent Bit DaemonSet)'),
        ('Per-tenant utility breakdown', 'AWS Split Cost Allocation Data for EKS'),
    ],
    analogy_stops="The analogy stops here: real EKS observability is N agents + collectors writing to N AWS services + IAM permissions + cost models. The deck metaphor undersells the integration work.",
    eli5='Lots of windows looking at the cluster. Some show numbers, some show pictures, some show what every visitor did. AWS provides the windows; you decide what to display.',
    eli10="Two-path observability: AWS-native (CloudWatch Container Insights + Logs + X-Ray) or OSS-on-AWS (AMP + AMG + ADOT). Most teams hybrid: Container Insights for cluster health + control-plane logs; AMP + AMG for app metrics; ADOT for ingestion to multiple destinations; X-Ray or Tempo for traces; Fluent Bit for log shipping; Split Cost Allocation for per-namespace cost.",
    scenarios=[
        Scenario(name='A SaaS using AWS-native end-to-end', body='Container Insights enhanced enabled at cluster create. ADOT collector ships PromQL metrics to AMP + traces to X-Ray + logs to CloudWatch. AMG dashboards via IAM Identity Center SSO. Total observability cost: ~$300/month for a 50-Pod cluster. Zero ops on observability infra.'),
        Scenario(name='A bank running hybrid: AMP + AMG + Datadog', body='AMP + AMG as the primary K8s metrics + dashboard. Datadog APM for app traces (existing licence). Both feed Container Insights + control-plane logs into a SIEM. Cost: managed AWS + Datadog licences ~$2K/month for 200-node cluster.'),
        Scenario(name='A startup using OSS Prometheus + Grafana on EKS for cost', body='kube-prometheus-stack via Helm. Self-hosted Grafana. Cheaper at small scale; SRE time invested. Migrate to AMP + AMG when scale or ops cost passes the threshold.'),
        Scenario(name='A team using Split Cost Allocation', body='Per-namespace cost report shared with each team monthly. Team A: $2400/month. Team B: $480. Team C: $5800 (turns out they were running an unused load-test cluster constantly). Visibility drove a 30% cluster spend reduction in 2 months.'),
    ],
    misconceptions=[
        Misconception(myth='\"AMP is just remote Prometheus.\"', truth='AMP exposes the same APIs (remote_write + PromQL) but it\'s a managed scaled service handling 100M+ active series. No Prometheus server you operate. Different operational shape.'),
        Misconception(myth='\"Control-plane logs are noise; skip them.\"', truth='Audit logs are required for compliance, breach forensics, and root-causing apiserver issues. Volume tunable via audit policy. Always enable from cluster create.'),
        Misconception(myth='\"Container Insights replaces application observability.\"', truth='Container Insights is K8s + node metrics. App-level metrics + traces + logs still need OTel SDKs in your apps. Container Insights complements; doesn\'t replace.'),
    ],
    flashcards=[
        Flashcard(front='What is CloudWatch Container Insights enhanced?', back='AWS-managed Pod + node + container metrics + logs DaemonSet for EKS. Pre-built dashboards. Enable as the <code>amazon-cloudwatch-observability</code> add-on.'),
        Flashcard(front='AMP vs OSS Prometheus?', back='Same APIs (remote_write + PromQL); AMP is serverless + scales to 100M+ active series + AWS handles ops. Cost = ingestion + storage + queries.'),
        Flashcard(front='AMG vs OSS Grafana?', back='Same UI; AMG handles infra; IAM Identity Center SSO; data sources include AMP, CloudWatch, X-Ray. Pay per active user.'),
        Flashcard(front='ADOT — what does it do?', back='AWS-supported OpenTelemetry collector. DaemonSet + Deployment. Receives Prometheus + OTLP; routes to AMP, X-Ray, CloudWatch, third-party.'),
        Flashcard(front='Five EKS control-plane log types?', back='api, audit, authenticator, controllerManager, scheduler. Each goes to CloudWatch Log Groups. Enable per-cluster.'),
        Flashcard(front='X-Ray for EKS?', back='AWS distributed tracing. ADOT sends spans; X-Ray UI shows service maps + trace flame graphs. Alternative: OTel → Tempo / Jaeger / Honeycomb.'),
        Flashcard(front='AWS Split Cost Allocation for EKS?', back='Cost Explorer feature attributing EC2 + EBS to Pods + namespaces using Container Insights data. The right way to answer per-team cost.'),
        Flashcard(front='Fluent Bit for EKS?', back='Lightweight log shipper. Container Insights observability add-on includes a managed Fluent Bit DaemonSet. Ships container logs to CloudWatch Log Groups.'),
    ],
    quizzes=[
        Quiz(prompt='Your team\'s AMP costs jumped 4x last month. Diagnose.', answer='<strong>Active series + ingestion.</strong> AMP cost = ingested samples ($0.30 per 10M) + active series stored ($0.10 per 1000 per month) + queries. <strong>Common cause: high cardinality.</strong> Someone added a metric label like <code>user_id</code> or <code>request_id</code>; series count exploded. <strong>Diagnose:</strong> AMP\'s <code>topk(10, count by (__name__) ({{__name__=~\".+\"}}))</code> shows per-metric series count. Find the offender. <strong>Fix:</strong> drop the high-cardinality label at the OTel collector or Prometheus relabel; or change the metric to use a low-cardinality bucket. <strong>Prevent:</strong> alert if any single metric exceeds 100K series. Cardinality budget per workload.'),
        Quiz(prompt='You enable Split Cost Allocation Data for EKS. The numbers don\'t match what your finance team has. Diagnose.', answer='<strong>Common reasons:</strong> (1) <em>Lag</em>: Cost Explorer data is 24-48 hours behind; finance might be looking at older data. (2) <em>Untagged resources</em>: EBS volumes without proper tags don\'t allocate cleanly. Add cluster + namespace tags to PV provisioning (StorageClass parameters or Kyverno mutation). (3) <em>Shared resources</em>: ALBs, NAT gateways, S3 buckets shared across namespaces. Split Cost Allocation handles EC2 + EBS Pod-allocated; other costs allocated separately by tag. (4) <em>System namespaces</em>: kube-system + amazon-cloudwatch + similar are typically not allocated to teams; they\'re platform overhead. Document this. <strong>Reconciliation:</strong> work with finance to define what \"team cost\" means: just direct EKS workload, or platform overhead share too?'),
        Quiz(prompt='You\'re building an observability stack for a new EKS cluster. <strong>Click for the launch playbook. ▼</strong>', cyoa=True, cyoa_tag='the launch playbook', answer='<strong>(1) At cluster create</strong>: enable all 5 control-plane log types. Don\'t skip — retroactive enabling doesn\'t backfill. <strong>(2) Container Insights add-on</strong>: <code>aws eks create-addon --addon-name amazon-cloudwatch-observability</code>. Pre-built dashboards in CloudWatch immediately. <strong>(3) AMP workspace</strong> + IAM role for ADOT: <code>aws amp create-workspace</code>. <strong>(4) ADOT collector</strong> as DaemonSet: scrape Prometheus annotations on Pods + node-exporter metrics + ServiceMonitor; remote_write to AMP. Plus OTLP receiver for app traces → X-Ray. <strong>(5) AMG workspace</strong>: AWS Console; add AMP + CloudWatch + X-Ray as data sources. Connect to IAM Identity Center for SSO. Import recommended Grafana dashboards (kube-state, node-exporter, etc.). <strong>(6) Fluent Bit</strong> (already part of the Container Insights add-on): tune to ship app logs to a separate CloudWatch Log Group per namespace. <strong>(7) Split Cost Allocation</strong>: enable in Cost Explorer + tag every workload with namespace + team. Wait 24h for first reports. <strong>(8) Alerts</strong>: AlertManager (in AMP) or CloudWatch Alarms for: control-plane errors, Pod CrashLoopBackOff, node NotReady, AMP cost spike, control-plane log spike. <strong>(9) Runbooks</strong> per alert. <strong>(10) Quarterly review</strong>: AMP cost trend, control-plane log volume, Container Insights alarm noise. <strong>Total launch time:</strong> 1 sprint. <strong>Result</strong>: production observability from day 1.'),
    ],
    glossary=[
        GlossaryItem(name='CloudWatch Container Insights', definition='AWS K8s metrics + logs DaemonSet. Enable as observability add-on. Pre-built dashboards.'),
        GlossaryItem(name='Amazon Managed Prometheus (AMP)', definition='Serverless Prometheus-compatible metrics store. Scales to 100M+ active series.'),
        GlossaryItem(name='Amazon Managed Grafana (AMG)', definition='Serverless Grafana. IAM Identity Center SSO. Data sources: AMP, CloudWatch, X-Ray.'),
        GlossaryItem(name='ADOT (AWS Distro for OpenTelemetry)', definition='AWS-supported OTel collector. DaemonSet + Deployment. Routes to AMP / X-Ray / CloudWatch.'),
        GlossaryItem(name='Control-plane logs', definition='Five types: api, audit, authenticator, controllerManager, scheduler. To CloudWatch. Per-cluster opt-in.'),
        GlossaryItem(name='X-Ray', definition='AWS distributed tracing. Service maps + trace flame graphs. Alternative: Tempo / Jaeger.'),
        GlossaryItem(name='Fluent Bit (managed)', definition='Lightweight log shipper. Part of CloudWatch observability add-on; ships container logs to CloudWatch Log Groups.'),
        GlossaryItem(name='AWS Split Cost Allocation Data', definition='Cost Explorer feature attributing EC2 + EBS to Pods + namespaces using Container Insights data.'),
        GlossaryItem(name='ServiceMonitor / PodMonitor', definition='Prometheus Operator CRDs for declarative scrape config. ADOT supports them.'),
        GlossaryItem(name='Active series (AMP)', definition='Distinct (metric_name, labels) combinations stored. Cardinality drives cost.'),
        GlossaryItem(name='remote_write (Prometheus)', definition='Protocol for shipping metrics from a collector to a remote store. AMP accepts via SigV4-signed remote_write.'),
        GlossaryItem(name='AWS observability hybrid pattern', definition='CloudWatch for cluster health + logs; AMP + AMG for app metrics; X-Ray or Tempo for traces. Most teams\' choice.'),
    ],
    recap_lead='Observability stack = CloudWatch Container Insights (cluster health) + AMP / AMG (app metrics + dashboards) + ADOT (ingestion) + X-Ray (traces) + Fluent Bit (logs) + control-plane logs to CloudWatch + Split Cost Allocation. Most enable at cluster create.',
    recap_next='<strong>Next — E9: EKS Upgrades and Operations.</strong> Standard support, extended support, version skew, control-plane + node + add-on upgrades, blue-green migration.',
)
