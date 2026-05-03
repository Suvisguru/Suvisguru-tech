"""K-GKE G7 — GKE Observability (Cloud Logging + Monitoring + GMP + Grafana + Trace + Profiler + SLO)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GKE observability — Cloud Logging, Cloud Monitoring, GMP, managed Grafana, Cloud Trace, Profiler, SLO.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Watchtower — three signal pipes + SLO + cost</text>
  <rect x="40" y="70" width="160" height="120" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="120" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">metrics</text>
  <text x="120" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Cloud Monitoring (auto)</text>
  <text x="120" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Managed Prometheus (GMP)</text>
  <text x="120" y="135" text-anchor="middle" font-size="9" fill="#FFFFFF">Managed Grafana</text>
  <text x="120" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">control-plane metrics</text>
  <rect x="215" y="70" width="160" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="295" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">logs</text>
  <text x="295" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Cloud Logging (auto)</text>
  <text x="295" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Logs Explorer</text>
  <text x="295" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">structured logs</text>
  <text x="295" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">Error Reporting</text>
  <rect x="390" y="70" width="160" height="120" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="470" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">traces + perf</text>
  <text x="470" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">Cloud Trace</text>
  <text x="470" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">end-to-end spans</text>
  <text x="470" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">Cloud Profiler</text>
  <text x="470" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">CPU / heap profiles</text>
  <rect x="565" y="70" width="155" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="642" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">SLO + alerts + cost</text>
  <text x="642" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">Service Monitoring (SLO)</text>
  <text x="642" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">alerting policies</text>
  <text x="642" y="131" text-anchor="middle" font-size="9" fill="#FBF1D6">Pub/Sub → PagerDuty</text>
  <text x="642" y="145" text-anchor="middle" font-size="9" fill="#FBF1D6">BigQuery cost view</text>
  <text x="642" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">SLO-first alerting</text>
</svg>"""


LESSON = LessonSpec(
    num="07",
    title_short="GKE observability",
    title_full="G7 · GKE Observability (Cloud Logging + Monitoring + GMP + Grafana + Trace + Profiler + SLO)",
    title_html="K-GKE G7 · GKE Observability",
    module_eyebrow="Module G7 · the Watchtower",
    hero_sub_html='Three signal pipes + SLO + cost, mostly auto for GKE. <strong>Metrics</strong>: <strong>Cloud Monitoring</strong> (auto-enabled) + <strong>Managed Service for Prometheus (GMP)</strong> + <strong>managed Grafana</strong>. <strong>Logs</strong>: <strong>Cloud Logging</strong> (auto, Logs Explorer + structured logs + Error Reporting). <strong>Traces + perf</strong>: <strong>Cloud Trace</strong> (end-to-end spans) + <strong>Cloud Profiler</strong> (CPU + heap). <strong>SLO + alerts</strong>: <strong>Service Monitoring</strong> (define SLOs; burn-rate alerts). <strong>Cost</strong>: BigQuery cost view (covered in G6).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. CrashLoopBackOff alert: <em>\"checkout-service Pod restarting every 90 seconds.\"</em> You open the GCP console, click through Logs Explorer, copy a query into another tab for the upstream API trace in Cloud Trace, switch to Cloud Monitoring for the metric trend, switch to Cloud Profiler for the CPU profile. <em>Five tabs, no joined view.</em> Today\'s lesson: GKE\'s built-in observability stack and how to compose it on one Grafana dashboard.",
    stamp_html="<strong>Three pipes auto-enabled (Cloud Monitoring metrics + Cloud Logging logs + Cloud Trace spans). GMP for Prometheus + managed Grafana for the joined view. SLO-first alerting via Service Monitoring. BigQuery cost export ties everything to spend.</strong>",
    district_pin="kg-plot07",
    district_label="Watchtower",
    sections=[
        Section(
            eyebrow="Section 1.1 · Cloud Logging + Cloud Monitoring (auto for GKE)",
            h2="Cloud Logging + Cloud Monitoring — auto-enabled for GKE",
            body_html="""    <p><strong>Cloud Logging</strong> is auto-enabled for GKE clusters. Container stdout/stderr, kubelet, system, and (if enabled in diagnostic settings) control-plane logs all flow to a Log Analytics-equivalent <em>log bucket</em>. Query via <strong>Logs Explorer</strong> with the <em>Logs Query Language</em> (LQL — similar to grep+filter, simpler than KQL).</p>
    <p><em>Structured logs</em>: emit JSON to stdout from your app and Cloud Logging parses it. Fields searchable as labels. Standard Cloud Logging libraries for Go / Python / Java / Node make this idiomatic.</p>
    <p><strong>Cloud Monitoring</strong> auto-collects K8s metrics (CPU, memory, container restarts, scheduled vs running Pod counts, etc.) plus per-node + per-cluster GCE metrics. Pre-built <em>GKE dashboards</em> in the Cloud Monitoring console cover the standard panes. Workspace concept lets you join metrics across multiple projects.</p>
    <p><strong>Error Reporting</strong> auto-clusters similar exception traces from your app logs into <em>error groups</em>; tracks first-seen, last-seen, occurrence count. Replaces the manual log-grep-for-stack-traces workflow.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Managed Service for Prometheus (GMP) + managed Grafana",
            h2="Managed Service for Prometheus (GMP) + managed Grafana",
            body_html="""    <p><strong>Managed Service for Prometheus (GMP)</strong> = Google\'s managed Prometheus-as-a-service. Enable per cluster (<code>--enable-managed-prometheus</code>); the GMP collector scrapes Pod metrics annotated with the standard Prometheus annotations + ServiceMonitor / PodMonitor CRDs. Stores in a managed time-series backend; queries via PromQL through the GMP query frontend.</p>
    <p><em>Why GMP on top of Cloud Monitoring</em>: Cloud Monitoring covers GKE-native metrics; GMP covers <em>application metrics in standard Prometheus format</em> (counters, gauges, histograms emitted by libraries like prometheus_client, Micrometer). Use both in the same cluster.</p>
    <p><strong>Managed Grafana options</strong>:
    <ul>
      <li><strong>Self-hosted Grafana</strong> on GKE → GMP as Prometheus data source + Cloud Monitoring as Stackdriver data source.</li>
      <li><strong>Grafana Cloud</strong> integration via OAuth — managed by Grafana Labs.</li>
      <li><strong>Native Cloud Monitoring dashboards</strong> for cases where you don\'t need full Grafana flexibility.</li>
    </ul>
    <p>Grafana joins the three pipes (GMP for app metrics, Cloud Monitoring for infra metrics, Cloud Logging for logs via the Cloud Logging data source plugin). Cloud Trace spans visible inline. <em>One dashboard for the whole picture.</em></p>"""
        ),
        Section(
            eyebrow="Section 1.3 · Cloud Trace + Cloud Profiler",
            h2="Cloud Trace + Cloud Profiler",
            body_html="""    <p><strong>Cloud Trace</strong> = managed distributed tracing. Auto-collects traces from any app emitting <strong>OpenTelemetry</strong> spans or using the <strong>Cloud Trace SDK</strong> directly. Standard libraries auto-instrument HTTP, gRPC, SQL, gcloud SDK calls. Sampling configurable (10% of low-value, 100% of error / high-latency).</p>
    <p>Trace view shows <em>end-to-end timing</em> of a request across services: e.g., \"checkout request, 850ms total: 120ms in API gateway, 80ms in auth, 600ms in DB query, 50ms in payment provider call.\" Click a span for downstream child spans. Span tags propagate the K8s metadata (Pod name, namespace, node) for correlation with logs + metrics.</p>
    <p><strong>Cloud Profiler</strong> = continuous CPU + heap profiling. The Profiler agent (no app changes for some languages, library import for others) samples in production with low overhead. View flame graphs in the Cloud console. <em>Find the function that\'s burning 30% of your CPU but you didn\'t know it.</em></p>
    <p><strong>Pattern</strong>: spans give the request-level timing; logs give the per-step narrative; profiler gives the per-function cost. Together they answer \"why is this slow?\" + \"where is the CPU going?\"</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · control-plane metrics/logs + SLO + alerting + cost",
            h2="Control-plane metrics/logs + SLO Monitoring + alerting policies",
            body_html="""    <p><strong>Control-plane metrics + logs</strong>: enable apiserver, scheduler, and controller-manager <em>metric + log export</em> in the cluster\'s monitoring/logging config (<code>--monitoring=SYSTEM,WORKLOAD,APISERVER,CONTROLLER_MANAGER,SCHEDULER</code>). Apiserver request rate, latency, error rate land in Cloud Monitoring; audit logs in Cloud Logging.</p>
    <p><strong>Service Monitoring (SLO)</strong> = define SLOs declaratively: \"99.5% of HTTP requests to checkout return 200 with latency &lt; 300ms over a 28-day rolling window.\" Service Monitoring tracks attainment + burn rate. Alerting on <em>burn rate</em> rather than raw error rate gives you actionable signal: \"the service is burning error budget 14× faster than sustainable\" → page now; \"burning 1.5×\" → ticket. <em>Modern SRE alerting; replaces threshold-on-raw-metric noise.</em></p>
    <p><strong>Alerting policies</strong> (Cloud Monitoring) — define metric / log / SLO conditions; route to <em>Notification Channels</em> (Pub/Sub → Cloud Functions → PagerDuty / Teams / Slack / email; or direct PagerDuty integration). Use Pub/Sub for fan-out and audit (every alert is a Pub/Sub message you can replay).</p>
    <p><strong>BigQuery cost view</strong> (recap from G6): BQ billing export + GKE cost allocation = per-namespace cost dashboards in Looker Studio / Grafana. Join cost data with utilisation metrics from GMP / Cloud Monitoring to compute <em>cost per request</em> at the service level.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="The team uses prometheus_client in their app and wants centralised metrics without operating a Prometheus server. What\'s the path?",
            options=[
                ("Run Prometheus on GKE.", False),
                ("Enable <strong>Managed Service for Prometheus (GMP)</strong> on the cluster; annotate Pods or use ServiceMonitor / PodMonitor CRDs; metrics flow into GMP and are queryable via PromQL.", True),
                ("Push to Cloud Monitoring custom metrics manually.", False),
            ],
            feedback="GMP is the managed Prometheus service. App emits standard Prometheus metrics; GMP scrapes; PromQL works. No Prometheus server to operate.",
        ),
    },
    before_after_before='<p>Pre-managed GKE observability = Bring Your Own Prometheus + Bring Your Own Grafana + Bring Your Own log shipper + ELK or Loki + custom alert routing. Operators ran 5+ Helm charts and a separate VMSS for the metrics+logs stack. Apiserver logs were essentially invisible without diagnostic-settings wiring. Tracing was unsupported in the basic stack — Cloud Trace existed but was a separate sale.</p>',
    before_after_after='<p>Modern GKE auto-enables <strong>Cloud Logging</strong> + <strong>Cloud Monitoring</strong>; <strong>GMP</strong> + <strong>managed Grafana</strong> add Prometheus + flexible visualisation; <strong>Cloud Trace + Cloud Profiler</strong> are first-class for app perf; <strong>Service Monitoring</strong> turns SLOs into burn-rate alerts; <strong>BigQuery cost export</strong> ties spend to workload. <em>Five managed services replace a 12-component homemade stack.</em></p>',
    before_after_caption='<p class="ba-caption"><em>The DIY observability era is over for GKE. Wire up GMP + Grafana + SLO Monitoring; review the Cloud Logging cost monthly; the rest is mostly auto.</em></p>',
    analogy_intro_html='''<p>The <strong>Watchtower</strong> at K-Garden is staffed all hours by three observers + an SLO scribe.</p>
    <p>The <strong>Heartbeat Drummer</strong> (metrics) plays a regular cadence: \"how full are the plots? how warm is the climate? how fast is the irrigation?\" The Cloud Monitoring drummer tracks garden-aware patterns; the GMP drummer follows industry-standard Prometheus rhythms.</p>
    <p>The <strong>Story Scribe</strong> (logs) writes everything narratable: \"Gardener A opened greenhouse 3 at 14:32; the irrigation valve in plot 7 reported error.\" The Cloud Logging scribe\'s book is queryable via Logs Explorer.</p>
    <p>The <strong>Journey Tracker</strong> (traces) follows one visitor end-to-end: \"the visitor entered through Path A, picked up tickets at the Pavilion, walked to Plot 3, watered for 5 minutes, took a soil sample, left through the East Gate.\" Cloud Trace shows each segment\'s duration. <strong>Cloud Profiler</strong> is the time-and-motion observer who tells you which gardener spent most of the day on what motion.</p>
    <p>The <strong>SLO Scribe</strong> (Service Monitoring) keeps the contract: \"the irrigation service must successfully water plots within 300ms 99.5% of the time over 28 days.\" When the contract burn rate spikes (\"we\'re burning 14× the sustainable rate\"), the Watchtower bell rings (alerting policies → Pub/Sub → PagerDuty).</p>
    <p>The <strong>Garden Accountant</strong> from G6 (BigQuery cost) joins the Watchtower\'s data: \"this plot costs $X/day; it serves Y requests/day; cost per request = Z.\"</p>''',
    translation_rows=[
        ("Heartbeat Drummer", "Metrics — Cloud Monitoring (auto)"),
        ("GMP drummer", "Managed Service for Prometheus + PromQL"),
        ("Story Scribe", "Logs — Cloud Logging + Logs Explorer"),
        ("Auto-clustered exception groups", "Error Reporting"),
        ("Journey Tracker", "Cloud Trace — end-to-end distributed tracing"),
        ("Time-and-motion observer", "Cloud Profiler — CPU + heap profiles"),
        ("Apiserver / scheduler watchman", "Control-plane metrics + audit logs (--monitoring=APISERVER, etc.)"),
        ("SLO Scribe", "Service Monitoring — define SLOs, track burn rate"),
        ("Watchtower bell", "Alerting policies → Notification Channels (Pub/Sub → PagerDuty / Teams)"),
        ("\"Burning 14× sustainable\"", "Burn-rate-based alerting"),
        ("Joined Watchtower dashboard", "Managed Grafana with GMP + Cloud Monitoring + Cloud Logging data sources"),
        ("Garden Accountant\'s ledger", "BigQuery cost export + GKE cost allocation"),
    ],
    analogy_stops="A real Watchtower\'s observers see the same scene; in real systems the three pipes can be sampled / stored separately. Cloud Logging cost can be the dominant observability line item — without retention discipline it dwarfs everything else.",
    eli5="The Watchtower has three observers (a drummer for metrics, a scribe for stories, a tracker for visitor journeys) and a scribe who tracks the irrigation contract. They tell you when something\'s wrong before customers notice.",
    eli10="GKE observability auto-enables Cloud Logging + Cloud Monitoring. <strong>GMP</strong> adds managed Prometheus for app metrics; <strong>managed Grafana</strong> joins everything in one dashboard. <strong>Cloud Trace</strong> for end-to-end distributed traces; <strong>Cloud Profiler</strong> for CPU/heap profiling. <strong>Error Reporting</strong> auto-clusters exception traces. <strong>Service Monitoring</strong> defines SLOs + burn-rate alerts. <strong>Alerting policies</strong> route to Pub/Sub → PagerDuty / Teams. <strong>BigQuery cost view</strong> ties spend to workload. Enable apiserver / scheduler / controller-manager metrics + logs in monitoring/logging config.",
    scenarios=[
        Scenario(
            name="SaaS — RED dashboard in managed Grafana joining GMP + Cloud Monitoring",
            body="A SaaS team builds a per-service RED dashboard (Rate, Errors, Duration) in managed Grafana. Rate + Errors from GMP via PromQL on app-emitted prometheus_client counters. Duration from Cloud Trace span percentiles via the Cloud Trace data source. Cluster + node metrics from Cloud Monitoring. <em>One dashboard, three data sources, MTTR for p99 spikes drops to ~10 min.</em>",
        ),
        Scenario(
            name="Bank — apiserver audit log to Cloud Logging + Sentinel via Pub/Sub",
            body="Bank enables --monitoring=APISERVER + audit log routing. Sink ships audit logs to a Log Analytics-style log bucket; Pub/Sub fan-out forwards to Sentinel SOC. SOC rules detect kubectl exec into prod, RBAC changes outside CI, secret reads from unexpected SAs. <em>SOC owns the GKE security story; platform team owns alert wiring.</em>",
        ),
        Scenario(
            name="SLO-first alerting reduces pager noise",
            body="Team had threshold alerts: \"alert if 5xx rate > 1%.\" Result: 4-12 pages/day, 80% noise. Migration to <strong>burn-rate alerts</strong> via Service Monitoring: \"alert if 28-day burn rate > 14× over a 1-hour window.\" Now ~1 page/day, ~0 noise. <em>SLO-first alerting respects error budget; raw thresholds don\'t.</em>",
        ),
        Scenario(
            name="Profiler caught a 30% CPU regression no one noticed",
            body="Cloud Profiler flame graphs review: a recent code change introduced a regex compile in a hot loop, burning 30% of pod CPU. Refactored to compile once. <em>Cluster CPU dropped 25% across the affected service\'s namespace; cost saving paid for the Profiler license many times over.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Cloud Monitoring covers Prometheus metrics.\"",
            truth="Cloud Monitoring auto-collects <em>K8s + GCE infrastructure metrics</em>, not app-emitted Prometheus metrics. For app metrics in Prometheus format, enable <strong>GMP</strong>. Both can coexist in one cluster; both queryable from managed Grafana.",
        ),
        Misconception(
            myth="\"Threshold alerts are equivalent to SLO burn-rate alerts.\"",
            truth="Threshold alerts fire on raw metric values (\"error rate > 1%\"). They\'re noisy: any blip pages. Burn-rate alerts fire on <em>error-budget consumption rate</em> (\"burning 14× faster than sustainable over 1h\"). They wait for sustained breach + scale with severity — page when you\'re actually losing budget. SRE-grade alerting.",
        ),
        Misconception(
            myth="\"Cloud Logging retention defaults are fine.\"",
            truth="Defaults: 30 days for most logs in default log buckets. Often too short for compliance + too long for high-volume noisy logs. <em>Tune per log bucket</em>: shorter retention for chatty / dev; longer for audit. Plus consider routing to a custom log bucket with reduced cost; or to BigQuery for SQL-style analysis. Without discipline log ingest cost dominates GKE bills.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three signal pipes auto-enabled for GKE?", back="<strong>Cloud Logging</strong> (container stdout/stderr + kubelet + system + control-plane), <strong>Cloud Monitoring</strong> (K8s + GCE infra metrics + pre-built GKE dashboards), <strong>Cloud Trace</strong> (auto-collect from OpenTelemetry / Cloud Trace SDK)."),
        Flashcard(front="What does GMP add over Cloud Monitoring?", back="<strong>Managed Service for Prometheus</strong>: scrapes app-emitted Prometheus-format metrics (prometheus_client, Micrometer, etc.); PromQL queries; ServiceMonitor / PodMonitor CRDs. Cloud Monitoring covers infra; GMP covers app. Use both."),
        Flashcard(front="What does Cloud Profiler do?", back="Continuous CPU + heap profiling in production with low overhead. Flame graphs in the Cloud console. Find the function burning 30% of your CPU you didn\'t know about."),
        Flashcard(front="Service Monitoring + SLOs + burn-rate alerts — the pattern?", back="Define SLO (\"99.5% of requests &lt; 300ms over 28d\"). Service Monitoring tracks attainment + burn rate. Alert on <em>burn rate</em>: e.g., \"burning &gt; 14× sustainable for 1h\" = page; \"burning &gt; 1.5× for 6h\" = ticket. Replaces threshold-on-raw-metric noise."),
        Flashcard(front="What does Error Reporting do?", back="Auto-clusters similar exception stack traces from app logs into <em>error groups</em>. Tracks first-seen, last-seen, occurrence count. Replaces the manual log-grep-for-stack-traces workflow."),
        Flashcard(front="How do you enable apiserver / scheduler metrics + logs?", back="Cluster create / update with <code>--monitoring=SYSTEM,WORKLOAD,APISERVER,CONTROLLER_MANAGER,SCHEDULER</code> + <code>--logging=SYSTEM,WORKLOAD,API_SERVER,CONTROLLER_MANAGER,SCHEDULER</code>. Apiserver request rate / latency lands in Cloud Monitoring; audit logs in Cloud Logging."),
        Flashcard(front="Notification Channel patterns?", back="<strong>Direct integrations</strong>: PagerDuty, Slack, email, SMS. <strong>Pub/Sub</strong>: alert message goes to Pub/Sub topic → Cloud Functions / Workflows fans out + audits. Pub/Sub is the recommended pattern for fan-out + replayable alert audit trail."),
        Flashcard(front="Per-namespace cost — how does GKE expose it?", back="Enable BigQuery billing export at billing-account level + GKE cost allocation at cluster level. BQ rows include K8s metadata (cluster, namespace, workload). Build dashboards in Looker Studio / managed Grafana joining cost with namespace → tenant mapping."),
    ],
    quizzes=[
        Quiz(
            prompt="The team uses Logs Explorer to debug Pod CrashLoopBackOff incidents. What\'s a faster workflow that uses managed Grafana?",
            answer="Build a 4-panel Grafana dashboard scoped to namespace + service: (1) Cloud Monitoring panel: container_restart_count + Pod CPU / memory; (2) GMP panel: app-emitted RED metrics (rate / errors / duration); (3) Cloud Logging panel via Cloud Logging data source: tail of container logs filtered to the failing Pod; (4) Cloud Trace panel: latency p50/p99 + recent error traces. Pin the dashboard. On-call clicks one URL with template variables; sees four panes scoped to the alert. Time-to-diagnosis drops from 8-12 min (Logs Explorer + tab-switching) to under 2 min.",
        ),
        Quiz(
            prompt="The CFO sees the Cloud Logging bill: \"Why is observability $50K/month for a $120K GKE bill?\" The platform engineer investigates. What are the typical levers?",
            answer="Three usual suspects: (1) <strong>verbose stdout in production</strong> — single Deployment dumping debug-level JSON. Fix: log level + structured-log sampling. (2) <strong>Default 30-day retention on every log bucket</strong> — high-volume logs ingested + retained forever. Fix: per-bucket retention tuning; route low-value logs to a shorter-retention bucket. (3) <strong>Apiserver verbose audit logs at full fidelity</strong> when only audit-admin events needed for compliance. Fix: tune monitoring + logging config to include only the categories you actually use. Typical reduction: 40-70% with zero loss of operational signal.",
        ),
        Quiz(
            prompt="Black Friday eve. You want one alert chain for: p99 latency, error rate, traffic anomaly. You have Cloud Monitoring, GMP, Cloud Trace. Wire it in 30 minutes.",
            answer="Single <strong>Notification Channel</strong>: Pub/Sub topic → Cloud Function → PagerDuty webhook + Slack webhook + audit log to BigQuery. Three alerting sources: (a) Service Monitoring SLO with burn-rate alert (latency target via Cloud Trace data) → Notification Channel; (b) GMP <em>Prometheus alert rule</em> on RED metrics (5xx rate &gt; threshold for 5min) → same Channel; (c) Cloud Monitoring <em>anomaly detection</em> on traffic volume (configurable smart-detection) → same Channel. <em>One channel, three sources, no duplicate routing config.</em>",
            cyoa=True,
            cyoa_tag="how the holiday alerting got wired in 30 minutes",
        ),
    ],
    glossary=[
        GlossaryItem(name="Cloud Logging", definition="GKE-auto log destination. Logs Explorer + Logs Query Language. Container, kubelet, system, control-plane logs."),
        GlossaryItem(name="Cloud Monitoring", definition="GKE-auto metric destination. K8s + GCE infrastructure metrics. Pre-built GKE dashboards."),
        GlossaryItem(name="Managed Service for Prometheus (GMP)", definition="Managed Prometheus-as-a-service. Scrapes app-emitted Prometheus metrics; PromQL queries."),
        GlossaryItem(name="Managed Grafana (Grafana Cloud / self-hosted)", definition="Joins GMP + Cloud Monitoring + Cloud Logging + Cloud Trace data sources in one dashboard."),
        GlossaryItem(name="Cloud Trace", definition="Managed distributed tracing. OpenTelemetry / Cloud Trace SDK. End-to-end request span timing."),
        GlossaryItem(name="Cloud Profiler", definition="Continuous CPU + heap profiling in production. Flame graphs in Cloud console."),
        GlossaryItem(name="Error Reporting", definition="Auto-cluster exception stack traces into error groups. First/last seen + occurrence count."),
        GlossaryItem(name="Service Monitoring (SLO)", definition="Define SLOs declaratively + track attainment + burn rate. Foundation for burn-rate alerting."),
        GlossaryItem(name="Burn-rate alert", definition="Alert on error-budget consumption rate, not raw metric thresholds. SRE-grade alerting; reduces noise."),
        GlossaryItem(name="Alerting policy", definition="Cloud Monitoring construct combining condition + Notification Channels."),
        GlossaryItem(name="Notification Channel", definition="Direct integration (PagerDuty / Slack / email) or Pub/Sub fan-out target."),
        GlossaryItem(name="--monitoring / --logging flags", definition="Cluster create/update flags choosing which metric/log categories to ship: SYSTEM, WORKLOAD, APISERVER, CONTROLLER_MANAGER, SCHEDULER."),
    ],
    recap_lead='Three pipes auto-enabled (Logging + Monitoring + Trace); GMP + managed Grafana for the joined view; SLO-first alerting via Service Monitoring; BigQuery cost ties spend to workload.',
    recap_next='<strong>Next — G8: GKE Enterprise (Fleets) and AI/ML.</strong> Fleet management across GCP/AWS/Azure/on-prem; Config Sync; Policy Controller; Cloud Service Mesh across fleets; Connect Gateway; Multi-cluster Ingress / Gateway; GKE on AWS / Azure / VMware / bare metal; AI/ML on GKE (JobSet, Kueue, NVIDIA GPU Operator, MIG, TPU multi-host, Ray, GKE Inference Gateway, vLLM/NIM/Triton).',
)
