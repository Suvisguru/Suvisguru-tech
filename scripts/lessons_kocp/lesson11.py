"""K-OCP O11 — OpenShift Observability (Cluster Monitoring + Loki Logging + Tempo Tracing + NetObserv)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OCP observability — Cluster Monitoring (Prometheus + Thanos + Alertmanager) + Loki Logging + Tempo Tracing + NetObserv.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Control Tower — three pipes + network flows + COO</text>
  <rect x="40" y="65" width="170" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="125" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">metrics</text>
  <text x="125" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">Cluster Monitoring</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Prometheus + Thanos</text>
  <text x="125" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">Alertmanager</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">User Workload Monitoring</text>
  <rect x="225" y="65" width="170" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="310" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">logs</text>
  <text x="310" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">OpenShift Logging</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Loki + Vector</text>
  <text x="310" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">Fluentd deprecated</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">LogQL queries</text>
  <rect x="410" y="65" width="170" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="495" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">traces</text>
  <text x="495" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">Distributed Tracing</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">Tempo + OpenTelemetry</text>
  <text x="495" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">replaces Jaeger</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">TraceQL queries</text>
  <rect x="595" y="65" width="125" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="657" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">network + COO</text>
  <text x="657" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">NetObserv (eBPF)</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">flow visibility</text>
  <text x="657" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">Cluster Observability</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">Operator (COO)</text>
</svg>"""


LESSON = LessonSpec(
    num="11", title_short="OCP observability",
    title_full="O11 · OpenShift Observability (Cluster Monitoring + Loki Logging + Tempo Tracing + NetObserv)",
    title_html="K-OCP O11 · OpenShift Observability",
    module_eyebrow="Module O11 · the Control Tower",
    hero_sub_html='<strong>Built-in Cluster Monitoring</strong> (Prometheus + Thanos Querier + Alertmanager); <strong>User Workload Monitoring</strong> for app metrics. <strong>OpenShift Logging</strong> = Loki + Vector (Fluentd deprecated). <strong>OpenShift Distributed Tracing</strong> = Tempo + OpenTelemetry (replaces Jaeger). <strong>Network Observability (NetObserv)</strong> with eBPF for east-west flow visibility. <strong>Cluster Observability Operator (COO)</strong> for unified config + multi-stack management.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"Alertmanager firing 200 ContainerCpuUsageHigh alerts; on-call drowning in noise.\"</em> The team has Cluster Monitoring + User Workload Monitoring + OpenShift Logging + Tempo + NetObserv all installed. Each emits its own dashboards + alerts. None are routed to a single notification channel; alert fatigue is real. <em>You don\'t know which alerts are SLO-driving and which are noise.</em> Today\'s lesson: OCP\'s observability stack + how to compose it with SLO-first alerting.",
    stamp_html="<strong>Built-in Cluster Monitoring (Prom + Thanos + Alertmanager) + User Workload Monitoring is the metrics foundation. OpenShift Logging (Loki + Vector) for logs. Distributed Tracing (Tempo + OTel) for traces. NetObserv (eBPF) for network flow. SLO-first alerting reduces noise; COO unifies config.</strong>",
    district_pin="ko-bay11", district_label="Control Tower",
    sections=[
        Section(eyebrow="Section 1.1 · Cluster Monitoring + User Workload Monitoring",
            h2="Cluster Monitoring (Prometheus + Thanos + Alertmanager) + User Workload Monitoring",
            body_html="""    <p><strong>Built-in Cluster Monitoring</strong> ships enabled in every OCP cluster (no opt-in needed). Components managed by the <strong>Cluster Monitoring Operator (CMO)</strong>:</p>
    <ul>
      <li><strong>Prometheus</strong> — scrapes platform metrics (kubelet, apiserver, controller-manager, scheduler, etcd, ClusterOperators, OperatorHub-installed operators).</li>
      <li><strong>Thanos Querier</strong> — multi-Prometheus query layer; supports federation + long-term storage when wired.</li>
      <li><strong>Alertmanager</strong> — alert routing + grouping; receivers (PagerDuty, Slack, email, webhook).</li>
      <li><strong>kube-state-metrics + node-exporter</strong> — standard exporters.</li>
      <li><strong>Telemeter Client</strong> — anonymised cluster health telemetry to Red Hat Insights.</li>
    </ul>
    <p><strong>User Workload Monitoring (UWM)</strong> — opt-in (set <code>enableUserWorkload: true</code> in <code>cluster-monitoring-config</code> ConfigMap). Lets app teams expose Prometheus metrics from their workloads via <strong>ServiceMonitor / PodMonitor</strong> CRs. Separate Prometheus instance scopes app metrics; Alertmanager handles user alerts.</p>
    <p><strong>Long-term metrics storage:</strong> wire Thanos Storer + S3-compatible bucket (NooBaa / AWS S3 / Azure Blob); Thanos Querier federates short-term Prometheus + long-term Thanos blocks. Default retention: 15 days per Prometheus.</p>"""),
        Section(eyebrow="Section 1.2 · OpenShift Logging (Loki + Vector)", h2="OpenShift Logging — Loki + Vector (Fluentd deprecated)",
            body_html="""    <p><strong>OpenShift Logging</strong> = managed Operator. Components:</p>
    <ul>
      <li><strong>Vector</strong> — log collector DaemonSet (replaced Fluentd; Fluentd is deprecated). Faster + lighter; Rust-based.</li>
      <li><strong>Loki</strong> — log storage (replaces Elasticsearch; Elasticsearch backend deprecated). Loki uses S3-compatible object storage for log indices + chunks.</li>
      <li><strong>LokiStack</strong> CR — declarative LokiOperator config: storage, retention, replication.</li>
    </ul>
    <p><strong>Three log streams:</strong>
    <ul>
      <li><strong>Application logs</strong> — container stdout/stderr from user namespaces.</li>
      <li><strong>Infrastructure logs</strong> — kubelet, kube-apiserver, OCP system namespaces.</li>
      <li><strong>Audit logs</strong> — apiserver audit + OAuth audit. Routed separately for compliance.</li>
    </ul>
    <p><strong>ClusterLogForwarder</strong> CR routes logs to one or more outputs: Loki (default), external Splunk / Elasticsearch / Kafka / S3 / syslog. Different streams to different destinations.</p>
    <p><strong>LogQL</strong> = Loki\'s query language (Prometheus-PromQL-flavored). Query logs in OCP console <em>Observe → Logs</em>; supports both manual + saved queries.</p>"""),
        Section(eyebrow="Section 1.3 · Distributed Tracing (Tempo + OTel)",
            h2="OpenShift Distributed Tracing — Tempo + OpenTelemetry",
            body_html="""    <p><strong>OpenShift Distributed Tracing</strong> = managed Operator. <strong>Tempo</strong> (replaces Jaeger as the storage backend; Jaeger Operator deprecated). Tempo uses S3-compatible object storage; cheaper than Jaeger\'s Cassandra/Elasticsearch backends.</p>
    <p><strong>OpenTelemetry (OTel) Operator</strong> — manages OTel Collector deployments. Apps emit OTLP traces; Collector forwards to Tempo. Auto-instrumentation injection for supported languages (Java, Python, Node, .NET) via OTel Operator\'s instrumentation CR.</p>
    <p><strong>TempoStack</strong> CR — declarative Tempo configuration: storage backend, retention, replication.</p>
    <p><strong>TraceQL</strong> = Tempo\'s query language. Find traces by service, span attributes, latency thresholds. View span timelines in the OCP console.</p>
    <p>Pattern: app emits OTel spans → OTel Collector aggregates → Tempo stores → console + Grafana visualises. Cross-service request tracing across microservice + serverless boundaries.</p>"""),
        Section(eyebrow="Section 1.4 · NetObserv + Cluster Observability Operator",
            h2="NetObserv (eBPF) + Cluster Observability Operator (COO)",
            body_html="""    <p><strong>Network Observability (NetObserv) Operator</strong> — eBPF-based flow capture. DaemonSet on each node hooks into kernel; captures Pod-to-Pod, Pod-to-external, DNS lookups. Stores flow data in Loki (or external).</p>
    <p>OCP console: <em>Observe → Network Traffic</em> shows flow graph + tabular flows. Filter by namespace, port, label, NetworkPolicy decision (allow/drop). For debugging \"why is this connection refused?\" + auditing east-west traffic.</p>
    <p>Use cases: NetworkPolicy validation (drops visible), microservice dependency mapping, DNS issue diagnosis, performance bottleneck identification.</p>
    <p><strong>Cluster Observability Operator (COO)</strong> — unified config + multi-stack observability. Manages multiple Prometheus instances, Tempo, Loki across multiple Projects. Useful for multi-tenant OCP where each Project gets dedicated observability with shared backbone.</p>
    <p>Integration: SLO definitions in Prometheus rules; burn-rate alerts; cross-Operator dashboards in OCP console + external Grafana via Cluster Monitoring data sources.</p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A team\'s app emits prometheus_client metrics. They want them visible in OCP\'s Cluster Monitoring stack. What do they enable?",
        options=[("Install a separate Prometheus.", False),
            ("Enable User Workload Monitoring (set <code>enableUserWorkload: true</code> in cluster-monitoring-config ConfigMap); create a ServiceMonitor or PodMonitor CR pointing at the app\'s metrics endpoint.", True),
            ("Push metrics manually.", False)],
        feedback="UWM is the OCP-native path for app metrics. ServiceMonitor / PodMonitor are the standard scrape-config CRs.",
    )},
    before_after_before='<p>Pre-OCP-managed observability = self-installed Prometheus + Grafana + Loki + Jaeger + Hubble + 8 more Helm charts. Each chart\'s upgrade cycle independent; chart drift everywhere. No native fleet view. Apiserver / audit logs invisible without diagnostic-settings wiring. Tracing was bring-your-own.</p>',
    before_after_after='<p>OCP ships <strong>Cluster Monitoring auto-enabled</strong> (Prom + Thanos + Alertmanager); <strong>User Workload Monitoring</strong> for app metrics; <strong>Logging Operator</strong> (Loki + Vector); <strong>Distributed Tracing Operator</strong> (Tempo + OTel); <strong>NetObserv Operator</strong> (eBPF flow); <strong>Cluster Observability Operator</strong> for unified config. SLO-first alerting via Prometheus rules + Alertmanager.</p>',
    before_after_caption='<p class="ba-caption"><em>Each piece is a managed Operator with one Red Hat support contract; assemble vs DIY-Helm tradeoff is firmly in favour of managed.</em></p>',
    analogy_intro_html='''<p>The <strong>Control Tower</strong> at K-Foundry watches all production. Three signal pipes + a network camera + a unified config console.</p>
    <p>The <strong>Heartbeat Drum</strong> (Cluster Monitoring) plays the foundry\'s vital signs — Prometheus collects platform metrics; Thanos Querier federates queries; Alertmanager routes alarms. The User Workload Drum (UWM) plays each Project\'s app-specific metrics.</p>
    <p>The <strong>Story Scribe</strong> (OpenShift Logging — Loki + Vector) writes everything narratable: app logs, infra logs, audit logs. LogQL queries the archive.</p>
    <p>The <strong>Journey Tracker</strong> (Distributed Tracing — Tempo + OTel) follows one request end-to-end across services. TraceQL queries the trace archive.</p>
    <p>The <strong>NetObserv camera</strong> records every Pod-to-Pod packet (eBPF). The <strong>Cluster Observability Operator</strong> conducts the whole orchestra — unified config across the four signal types + multi-stack support for multi-tenant Projects.</p>''',
    translation_rows=[("Heartbeat Drum (platform vitals)", "Cluster Monitoring — Prometheus + Thanos Querier + Alertmanager"),
        ("Per-Project workload drum", "User Workload Monitoring (UWM)"),
        ("Story Scribe", "OpenShift Logging — Loki + Vector"),
        ("Three log streams", "Application + Infrastructure + Audit log streams"),
        ("Log archive query language", "LogQL"),
        ("Log-routing tablet", "ClusterLogForwarder CR"),
        ("Journey Tracker", "OpenShift Distributed Tracing — Tempo + OpenTelemetry"),
        ("Auto-instrumentation injector", "OpenTelemetry Operator + Instrumentation CR"),
        ("Trace query language", "TraceQL"),
        ("Network packet camera", "Network Observability (NetObserv) Operator (eBPF)"),
        ("Pod-to-Pod flow graph", "OCP Console → Observe → Network Traffic"),
        ("Cross-stack conductor", "Cluster Observability Operator (COO)"),
        ("Multi-tenant observability backbone", "COO managed Prometheus + Tempo + Loki per Project"),
        ("Phone-home health", "Telemeter Client → Red Hat Insights")],
    analogy_stops="A real control tower has fixed vantage points; OCP\'s observability surfaces are software-defined and grow per Operator install. Cardinality explosions in Prometheus are a real failure mode the metaphor doesn\'t capture.",
    eli5="The Control Tower watches the whole foundry: heartbeat drums for vital signs, scribes writing every story, trackers following each visitor, cameras on every walkway. Plus a conductor making sure they all play together.",
    eli10="OCP observability = built-in Cluster Monitoring (Prometheus + Thanos + Alertmanager) + UWM for app metrics; OpenShift Logging Operator (Loki + Vector — Fluentd deprecated, Elasticsearch deprecated); OpenShift Distributed Tracing Operator (Tempo + OpenTelemetry — Jaeger deprecated); NetObserv Operator (eBPF flow capture); Cluster Observability Operator (COO) for unified config + multi-tenant. SLO-first alerting via Prometheus rules + burn-rate.",
    scenarios=[
        Scenario(name="SaaS — UWM + Tempo + Loki RED dashboard in console",
            body="A SaaS team enables UWM + Logging + Tracing Operators. App emits prometheus_client + OTel spans. ServiceMonitor scrapes; OTel Collector forwards to Tempo. RED dashboard in console: Rate (Prom rate()), Errors (Prom counter), Duration (Tempo p95). Logs from same Pod available via console <em>Observe → Logs</em> in same view. <em>One console; minutes to dashboard; no external Grafana needed for basics.</em>"),
        Scenario(name="Bank — audit log forwarded to Splunk for SOC",
            body="A bank requires apiserver audit logs in their SOC Splunk. ClusterLogForwarder CR routes audit stream to Splunk; application + infrastructure streams stay in Loki. Splunk consumers consume the Splunk-side; OCP team handles Loki-side ops. <em>Audit log isolation for compliance.</em>"),
        Scenario(name="Telco — NetObserv finds NetworkPolicy drops in 2 min",
            body="Telco team enables NetObserv. Microservice A can\'t reach B; status: timeout. Open <em>Observe → Network Traffic</em>; filter by source-namespace=A, destination-namespace=B; see <em>NetworkPolicy drops</em> in flow data. NetworkPolicy in B\'s namespace was missing the allow-rule. Fixed in 2 minutes vs 30+ min of trial-and-error tcpdump."),
        Scenario(name="Multi-tenant Project — COO carves dedicated observability",
            body="An ISV runs multi-tenant OCP. Each tenant Project has its own observability requirements (different retention, different Slack channels for alerts, different Grafana orgs). COO manages per-Project Prometheus + Tempo + Loki configs from a central CR set. <em>Tenant isolation in observability without per-tenant Operator installs.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"Fluentd is still the OCP log collector.\"",
            truth="<strong>Fluentd is deprecated</strong> in OpenShift Logging; <strong>Vector</strong> is the current collector. Likewise Elasticsearch backend is deprecated; <strong>Loki</strong> is the current store. Migration: install Logging Operator at current minor; LokiStack CR; ClusterLogForwarder. <em>Existing Fluentd + Elasticsearch installs need migration; don\'t deploy fresh on deprecated stack.</em>"),
        Misconception(myth="\"Cluster Monitoring covers app metrics.\"",
            truth="<strong>Cluster Monitoring covers platform metrics</strong> (kubelet, apiserver, ClusterOperators, OperatorHub operators). For app metrics, enable <strong>User Workload Monitoring</strong> separately and create ServiceMonitor / PodMonitor CRs in your namespace."),
        Misconception(myth="\"Default retention is enough.\"",
            truth="Default Prometheus retention = 15 days; default Loki retention varies. <strong>For compliance + post-incident analysis, plan long-term storage</strong> (Thanos to S3 for metrics; Loki S3-backend for long-term logs; Tempo S3-backend for long-term traces). Without retention discipline, observability bills + storage explode + investigations stall on missing data."),
    ],
    flashcards=[
        Flashcard(front="What is OCP\'s built-in Cluster Monitoring stack?", back="Prometheus + Thanos Querier + Alertmanager + kube-state-metrics + node-exporter + Telemeter Client. Auto-enabled. Managed by the Cluster Monitoring Operator (CMO)."),
        Flashcard(front="What\'s the difference between Cluster Monitoring and User Workload Monitoring?", back="<strong>Cluster Monitoring</strong> covers platform metrics (kubelet, apiserver, ClusterOperators, etc.). <strong>User Workload Monitoring (UWM)</strong> = opt-in second Prometheus for app metrics via ServiceMonitor / PodMonitor in user namespaces."),
        Flashcard(front="OpenShift Logging stack — what replaced what?", back="<strong>Vector</strong> replaced Fluentd (collector). <strong>Loki</strong> replaced Elasticsearch (storage). LokiStack CR + ClusterLogForwarder for routing to Loki + external (Splunk / ES / Kafka / S3 / syslog)."),
        Flashcard(front="Three OCP log streams?", back="<strong>Application</strong> (user namespaces), <strong>Infrastructure</strong> (kubelet + system namespaces), <strong>Audit</strong> (apiserver + OAuth — separate for compliance routing)."),
        Flashcard(front="OpenShift Distributed Tracing — what replaced what?", back="<strong>Tempo</strong> replaced Jaeger (storage). <strong>OpenTelemetry (OTel) Operator</strong> manages collectors + auto-instrumentation. TempoStack CR + Instrumentation CR. TraceQL queries."),
        Flashcard(front="What is NetObserv?", back="Network Observability Operator — eBPF-based flow capture. DaemonSet on each node; stores flows in Loki. Console <em>Observe → Network Traffic</em> for flow graph + tabular view. NetworkPolicy decisions visible."),
        Flashcard(front="What is COO?", back="<strong>Cluster Observability Operator</strong> — unified config + multi-stack management for Prometheus + Tempo + Loki across Projects. Useful for multi-tenant OCP."),
        Flashcard(front="ClusterLogForwarder vs LokiStack?", back="<strong>LokiStack</strong> = the Loki cluster install (storage backend, retention, replication). <strong>ClusterLogForwarder</strong> = log routing — which streams go to which outputs (Loki / Splunk / ES / Kafka / S3 / syslog)."),
    ],
    quizzes=[
        Quiz(prompt="Alertmanager fires 200 alerts in an hour during a non-incident. Walk through reducing the noise.",
            answer="(1) Audit current alert rules: <code>oc get prometheusrule -A</code>. (2) Categorise by SLO impact: which alerts indicate genuine SLO burn vs threshold blips? (3) Replace threshold-on-raw-metric alerts with <strong>burn-rate alerts</strong>: e.g., \"alert if 28-day burn rate > 14× over 1h\" instead of \"alert if 5xx rate > 1%.\" (4) Adjust severity: most threshold alerts → ticket-level (low priority); only burn-rate alerts → page (high priority). (5) Use Alertmanager <em>inhibition rules</em> to suppress derived alerts when their root cause is firing. (6) Group alerts: per-namespace, per-service. (7) Re-route: low-severity to Slack channel; high-severity to PagerDuty. <em>Result: ~5-10 paged alerts per day, signal-rich; lots of tickets-in-Slack for tracking but not waking anyone.</em>"),
        Quiz(prompt="Migration plan: cluster currently runs OpenShift Logging with Fluentd + Elasticsearch (both deprecated). Walk through the migration to Vector + Loki.",
            answer="(1) Install LokiStack: install Loki Operator from OperatorHub; create LokiStack CR pointing to S3 / NooBaa storage. (2) Install + configure Logging Operator at current minor. (3) Update ClusterLogForwarder to route streams to LokiStack output (in addition to existing Fluentd → Elasticsearch). Run in parallel for a sprint to validate. (4) Validate Loki + Vector work end-to-end: log ingestion, console <em>Observe → Logs</em> queries, retention. (5) Cut over: remove Elasticsearch + Fluentd outputs; remove Elasticsearch operator + cluster. (6) Decommission Elasticsearch. (7) Postmortem any data-format / index differences. <em>Plan a 2-3 sprint migration; expect query semantics to change (LogQL vs Lucene).</em>"),
        Quiz(prompt="The CTO Slacks: \"Why are we paying for OCP\'s observability when we already have Datadog?\" Defend or pivot.",
            answer="\"<strong>Built-in Cluster Monitoring is free + auto-enabled</strong> — Prometheus + Thanos + Alertmanager for platform metrics. We can\'t turn it off; it\'s part of OCP. Datadog can coexist for app-side observability; we use Datadog for distributed tracing + APM, OCP\'s built-in for platform health. <strong>The OCP-managed Operators (Logging, Tracing, NetObserv, COO) are optional</strong>; install only if we want self-hosted alternatives or SOC integration that needs in-cluster control. <em>Honest cost-benefit:</em> Datadog excels for SaaS-hosted observability with rich integrations; OCP-managed Operators excel for self-hosted/sovereign data + integration with Red Hat\'s support contract. Most shops pick one for primary + use the other selectively. We don\'t pay extra for OCP\'s built-in Cluster Monitoring; the optional Operators are part of our existing OCP subscription.\"",
            cyoa=True, cyoa_tag="how the platform engineer answered the CTO"),
    ],
    glossary=[
        GlossaryItem(name="Cluster Monitoring", definition="Built-in OCP monitoring stack: Prometheus + Thanos Querier + Alertmanager + kube-state-metrics + node-exporter."),
        GlossaryItem(name="Cluster Monitoring Operator (CMO)", definition="Manages the built-in Cluster Monitoring stack."),
        GlossaryItem(name="User Workload Monitoring (UWM)", definition="Opt-in second Prometheus instance for app metrics. Enable via cluster-monitoring-config ConfigMap."),
        GlossaryItem(name="ServiceMonitor / PodMonitor", definition="Prometheus scrape config CRs for app metrics under UWM."),
        GlossaryItem(name="OpenShift Logging Operator", definition="Managed Operator for Vector log collection + Loki storage. Fluentd + Elasticsearch deprecated."),
        GlossaryItem(name="LokiStack CR", definition="Declarative LokiOperator config: storage backend (S3/NooBaa), retention, replication."),
        GlossaryItem(name="ClusterLogForwarder CR", definition="Routes log streams (application/infrastructure/audit) to outputs: Loki / Splunk / ES / Kafka / S3 / syslog."),
        GlossaryItem(name="LogQL", definition="Loki\'s query language. Prometheus-PromQL-flavored."),
        GlossaryItem(name="OpenShift Distributed Tracing Operator", definition="Managed Operator for Tempo storage + OpenTelemetry. Jaeger deprecated."),
        GlossaryItem(name="TempoStack CR", definition="Declarative Tempo config: storage backend, retention, replication."),
        GlossaryItem(name="OpenTelemetry (OTel) Operator", definition="Manages OTel Collector deployments + Instrumentation CR for auto-injection."),
        GlossaryItem(name="TraceQL", definition="Tempo\'s query language. Find traces by service, span attributes, latency."),
        GlossaryItem(name="Network Observability (NetObserv) Operator", definition="eBPF flow capture. Console Observe → Network Traffic flow graph."),
        GlossaryItem(name="Cluster Observability Operator (COO)", definition="Unified config + multi-stack mgmt across Prometheus + Tempo + Loki for multi-tenant Projects."),
    ],
    recap_lead='Built-in Cluster Monitoring + UWM for metrics; Logging Operator (Loki + Vector) for logs; Distributed Tracing Operator (Tempo + OTel) for traces; NetObserv for network flows; COO for unified config.',
    recap_next='<strong>Next — O12: OpenShift Troubleshooting.</strong> oc adm must-gather; oc adm inspect; ClusterOperator degraded; CVO blocked; MCP degraded; Node NotReady; SCC denial; Route + cert issues; internal registry failure; Build failure; Operator CSV failed; CatalogSource failure; OLM Subscription issues; OVN-K + DNS; OAuth failures; etcd backup/restore; disconnected pull failures.',
)
