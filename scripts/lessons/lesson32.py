from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Observatory dome: a telescope (logs collector), a star chart (metrics dashboard), and an OpenTelemetry router connecting source Pods to sinks (Loki, Prometheus, Grafana, S3).">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">OBSERVATORY · LOGS &amp; METRICS</text>
  <!-- Pods -->
  <g transform="translate(40,80)">
    <text x="50" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">SOURCES</text>
    <rect x="0" y="22" width="100" height="20" rx="2" fill="#5A9F7A"/><text x="50" y="36" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">Pod logs (stdout)</text>
    <rect x="0" y="48" width="100" height="20" rx="2" fill="#4A8FA8"/><text x="50" y="62" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">/metrics endpoint</text>
    <rect x="0" y="74" width="100" height="20" rx="2" fill="#A04832"/><text x="50" y="88" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">kube-state-metrics</text>
  </g>
  <line x1="145" y1="120" x2="180" y2="120" stroke="#A04832" stroke-width="2" marker-end="url(#a5)"/>
  <defs><marker id="a5" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#A04832"/></marker></defs>
  <!-- OTel collector -->
  <g transform="translate(180,55)">
    <rect width="180" height="130" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="90" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">OPENTELEMETRY</text>
    <text x="90" y="34" text-anchor="middle" font-size="8" fill="#FBF1D6" font-style="italic">Collector · DaemonSet</text>
    <rect x="14" y="44" width="152" height="22" rx="2" fill="#5A9F7A"/><text x="20" y="58" font-size="7" fill="#FFFFFF" font-weight="700">receivers · OTLP, Prom</text>
    <rect x="14" y="70" width="152" height="22" rx="2" fill="#E8B547"/><text x="20" y="84" font-size="7" fill="#5A4F45" font-weight="700">processors · batch, filter</text>
    <rect x="14" y="96" width="152" height="22" rx="2" fill="#A04832"/><text x="20" y="110" font-size="7" fill="#FFFFFF" font-weight="700">exporters · loki, prom, otlp</text>
  </g>
  <line x1="370" y1="120" x2="405" y2="120" stroke="#A04832" stroke-width="2" marker-end="url(#a5)"/>
  <!-- Sinks -->
  <g transform="translate(410,55)">
    <text x="115" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">SINKS</text>
    <rect x="0" y="22" width="110" height="40" rx="4" fill="#FBE8DC" stroke="#A04832" stroke-width="1.2"/>
    <text x="55" y="38" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">Loki</text>
    <text x="55" y="52" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">log store</text>
    <rect x="120" y="22" width="110" height="40" rx="4" fill="#E0EEF3" stroke="#4A8FA8" stroke-width="1.2"/>
    <text x="175" y="38" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">Prometheus</text>
    <text x="175" y="52" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">metrics TSDB</text>
    <rect x="0" y="72" width="230" height="40" rx="4" fill="#FBF1D6" stroke="#8B5A00" stroke-width="1.2"/>
    <text x="115" y="88" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">Grafana</text>
    <text x="115" y="102" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">dashboards · alerts</text>
  </g>
  <text x="340" y="200" text-anchor="middle" font-size="0" fill="#3F4A5E"></text>
</svg>"""

LESSON = LessonSpec(
    num="32",
    title_short="obs Pt 1 logs/metrics",
    title_full="Observability Part 1 · Logs and Metrics",
    title_html="Lesson 32 — Observability Part 1: Logs & Metrics · K-COM",
    module_eyebrow="Module 14 · Lesson 32 · the first two of three pillars",
    hero_sub_html='\"You can\'t fix what you can\'t see.\" K8s observability is now standardised on three pillars — <strong>logs, metrics, traces</strong> — fed through <strong>OpenTelemetry</strong> to whatever backends you pick. This lesson covers the first two pillars, the modern standard collectors (Vector, Fluent Bit, OTel Collector), and what \"good observability\" looks like in 2026.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='3 AM page. Service is degraded but you don\'t know which one. Pod logs are scattered: some in CloudWatch (legacy), some in Loki, some only on the node\'s disk. Prometheus retention is 7 days but the bug started 10 days ago. Tracing exists but only in <code>checkout-service</code>; the failing service is <code>auth</code>, no traces. You spend 90 minutes searching for the signal, 5 minutes fixing the bug. <em>The MTTR was the observability gap, not the bug</em>. Today\'s lesson: how to close it.',
    stamp_html='Three pillars: <strong>logs</strong> (events), <strong>metrics</strong> (numbers), <strong>traces</strong> (request flow — Lesson 33). Modern stack: instrument with <strong>OpenTelemetry SDKs</strong>, ship via <strong>OpenTelemetry Collector</strong>, store in vendor-neutral backends (<strong>Loki</strong> for logs, <strong>Prometheus</strong>/<strong>Mimir</strong>/<strong>VictoriaMetrics</strong> for metrics). The single biggest mistake teams make: not deploying observability infrastructure before they need it.',
    district_pin="kt-pin32",
    district_label="Observatory — Logs & Metrics Telescope",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Three pillars, one collector",
            body_html="""    <p>Production debugging answers three questions: <strong>What happened?</strong> (logs — discrete events), <strong>How fast / how much?</strong> (metrics — numeric time series), <strong>Where did time go?</strong> (traces — distributed request flow). Most outages need at least two of three to diagnose.</p>
    <p>Until 2020, each pillar had its own ecosystem: Fluentd / Logstash for logs, Prometheus client libs for metrics, Jaeger / Zipkin / OpenTracing for traces. Each app had three integrations. Then <strong>OpenTelemetry</strong> happened — a CNCF project unifying the SDKs and collector across all three pillars. By 2026, OTel is the de-facto standard. Apps emit signals; the OTel Collector receives them; you choose backends.</p>
    <p>The K8s-specific layer adds:</p>
    <ul>
      <li><strong>kube-state-metrics</strong> — exposes K8s API state (Pod count, Deployment ready replicas, etc.) as Prometheus metrics.</li>
      <li><strong>node-exporter</strong> — exposes node-level metrics (CPU, memory, disk, network) per node.</li>
      <li><strong>cAdvisor</strong> (in kubelet) — exposes per-container resource metrics.</li>
      <li><strong>OTel Operator</strong> — manages OTel Collector instances + auto-instrumentation injection for common languages.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.5 · Logs — collection patterns",
            h2="From stdout to indexed",
            body_html="""    <p>K8s convention: containers write logs to <strong>stdout/stderr</strong>, the kubelet captures them, the container runtime writes them to <code>/var/log/containers/&lt;pod&gt;_&lt;namespace&gt;_&lt;container&gt;.log</code>. Anything else (writing to a file inside the container, syslog, custom socket) is non-standard and works against you.</p>
    <p>Three collection patterns:</p>
    <ul>
      <li><strong>Node-level DaemonSet</strong> (most common) — Vector / Fluent Bit / OTel Collector on every node, reading <code>/var/log/containers/*.log</code>, parsing, shipping. Scales linearly with nodes; minimal Pod-level overhead.</li>
      <li><strong>Sidecar</strong> — a logging container next to each app container. Use for apps that can\'t emit to stdout (legacy app writing to a file). Ad-hoc, more Pods, more cost.</li>
      <li><strong>Direct from app</strong> — app uses an OTel SDK to ship logs. Works but adds latency to the app process; mostly used in modern apps that already use OTel for metrics + traces.</li>
    </ul>
    <p>Backends in 2026:</p>
    <ul>
      <li><strong>Loki</strong> (Grafana Labs) — popular open-source choice. Indexes labels only, full-text search via parsing at query time. Cheap to run.</li>
      <li><strong>Elasticsearch / OpenSearch</strong> — full-text indexing. More powerful queries, more expensive ops.</li>
      <li><strong>Cloud-native</strong> — CloudWatch (AWS), Cloud Logging (GCP), Azure Log Analytics. Closed but easy.</li>
      <li><strong>Vector + S3</strong> — durable, cheap, query later via Athena / Trino.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.7 · Metrics — Prometheus and the modern alternatives",
            h2="From scraping to remote write",
            body_html="""    <p>Prometheus model: pull-based. A Prometheus server periodically scrapes <code>/metrics</code> endpoints exposed by Pods (using the OpenMetrics format), stores time series in its TSDB, exposes them via PromQL.</p>
    <p>The architecture is famously simple, but at scale it shows seams. Single Prometheus instance hits limits at ~10M active series. Three modern options:</p>
    <ul>
      <li><strong>Prometheus + Thanos / Cortex / Mimir</strong> — Prometheus shards write to a central deduplication/storage layer. Long-term storage on object storage. Mimir (Grafana) is the most popular in 2026.</li>
      <li><strong>VictoriaMetrics</strong> — drop-in Prometheus replacement, faster + lower memory at scale. Single-binary cluster mode.</li>
      <li><strong>OpenTelemetry-native</strong> — OTel Collector receives metrics, ships via OTLP to any OTLP-compatible backend (Mimir, VictoriaMetrics, vendor SaaS).</li>
    </ul>
    <p>What to scrape (the standard K8s metric stack):</p>
    <ul>
      <li>Apps\' own <code>/metrics</code> via OpenMetrics + ServiceMonitor (Prometheus Operator) or PodMonitor.</li>
      <li>kube-state-metrics for K8s object state.</li>
      <li>node-exporter for node-level resources.</li>
      <li>kubelet/cAdvisor for per-container resources.</li>
      <li>cluster autoscaler, controller-manager, scheduler — control-plane metrics.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The cardinality problem: every unique combination of metric labels is a separate time series. A metric with a <code>user_id</code> label and 1M users = 1M series. Prometheus doesn\'t care about the metric values; it cares about the series count. The single most common observability bug: shipping a metric with a high-cardinality label (request_id, user_id, full URL path with IDs). Catch it early; cardinality killers run servers out of memory faster than anything else.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Dashboards, alerts, and runbooks",
            h2="What good observability looks like",
            body_html="""    <p>Three artefacts every production service should have:</p>
    <ul>
      <li><strong>Dashboard</strong> — Grafana panel showing the four golden signals: latency, traffic, errors, saturation. One dashboard per service. Linkable from the runbook.</li>
      <li><strong>Alerts</strong> — Prometheus AlertManager rules with PromQL, paging on SLO violations. Alerts have runbooks linked in their annotations.</li>
      <li><strong>Runbook</strong> — markdown in git: \"if alert X fires, run these queries, look for these patterns, escalate at this signal.\"</li>
    </ul>
    <p>Modern teams also generate this from <strong>SLOs</strong> (Service Level Objectives — covered in Lesson 33). Tools like <strong>Sloth</strong> or <strong>Pyrra</strong> read your SLO definitions and generate the alerts + dashboards automatically. The team writes the SLO; the tools write the boilerplate.</p>
    <p>Common anti-patterns:</p>
    <ul>
      <li>\"Page on every 5xx\" — death by alert. Page on SLO violation, not transient errors.</li>
      <li>Alerts without runbooks — pager wakes someone who doesn\'t know what to do.</li>
      <li>Vanity dashboards — 40 panels per service nobody reads. Pick the four golden signals; everything else on a secondary dashboard.</li>
      <li>Logs at INFO level for routine flows — log volume balloons; signal-to-noise drops; cost spikes. Log at WARN or ERROR for routine; INFO only for state changes that might matter in a future incident.</li>
    </ul>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team adds a Prometheus metric: <code>http_request_duration_seconds{user_id, request_id}</code>. The Prometheus server\'s memory usage triples within an hour. What\'s wrong?",
            options=[
                ("a) Prometheus is buggy", False),
                ("b) The metric labels are high-cardinality — every unique user_id × request_id is a separate time series, exploding the series count", True),
                ("c) The scrape interval is too short", False),
            ],
            feedback="<strong>Answer: b.</strong> Classic cardinality bomb. <code>user_id</code> alone might be 1M unique values; <code>request_id</code> is unbounded. Each unique combination = a separate time series. <strong>Fix:</strong> never put unbounded-cardinality fields in metric labels. Use logs or traces for per-request data. Metrics are aggregations.",
        ),
    },
    before_after_before='<p>Pre-OTel era: Fluentd for logs, Prometheus for metrics, Jaeger for traces — three SDKs, three exporters per app, three on-call dashboards. \"Where did the request go?\" required correlating across three siloed systems by hand. Cardinality bombs took down Prometheus monthly. Logs at INFO everywhere because nobody had time to tune.</p>',
    before_after_after='<p>OpenTelemetry SDKs in every app, OTel Collector as a single ingress, vendor-neutral backends (Loki + Mimir + Tempo). Trace IDs propagated end-to-end. Cardinality monitored as a first-class concern. SLO-driven alerts with linked runbooks. MTTR drops from hours to minutes.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">OpenTelemetry adoption was the most consequential observability shift in a decade. By 2026 it\'s the default; new K8s deployments instrument with OTel from day 1.</p>',
    analogy_intro_html='<p>The Observatory sits high above K-Town with three instruments. The <strong>logbook telescope</strong> (logs collector) reads what every building wrote down today — typed messages, errors, traces of activity. The <strong>star chart</strong> (metrics dashboard) shows numerical time series for every quantity worth measuring — temperature, foot traffic, queue depth — refreshed continually. The <strong>OpenTelemetry router</strong> in the dome (OTel Collector) receives signals from every building in a standardised format and forwards them to specialist offices: log archive (Loki), metrics archive (Prometheus / Mimir), and the live alarm board (Grafana). When something goes wrong, the city\'s on-call walks into the Observatory, glances at the star chart, asks the logbook a question, and is back to bed in minutes.</p>',
    translation_rows=[
        ("The logbook telescope", "Logs collector (Vector / Fluent Bit / OTel Collector)"),
        ("The star chart", "Metrics dashboard (Grafana on Prometheus)"),
        ("The OpenTelemetry router", "OTel Collector"),
        ("Standardised signal format", "OTLP (OpenTelemetry Protocol)"),
        ("Log archive", "Loki / Elasticsearch / S3"),
        ("Metrics archive", "Prometheus / Mimir / VictoriaMetrics"),
        ("Live alarm board", "Grafana + AlertManager"),
        ("Star\'s position drifting suspiciously", "Cardinality bomb"),
    ],
    analogy_stops="The analogy stops here: real observability backends ingest gigabytes per second and need careful capacity planning; \"a telescope\" doesn\'t. And the OTel Collector isn\'t a router in the network sense — it\'s a stream-processing pipeline with receivers, processors, and exporters.",
    eli5='Two notebooks for every building. One says what happened (logs). One has all the numbers (metrics). A friendly robot collects both and puts them in the right drawer so you can find them later.',
    eli10="Three observability pillars: logs (events), metrics (numbers over time), traces (request flow). OpenTelemetry standardises SDKs + the collector across all three. K8s-specific: pods write to stdout, kubelet captures, a DaemonSet (Vector / Fluent Bit / OTel Collector) ships logs to Loki/Elastic; Prometheus scrapes <code>/metrics</code> endpoints (or apps push via OTLP). Avoid high-cardinality metric labels. Pair every alert with a runbook; pair every service with a four-golden-signals dashboard.",
    scenarios=[
        Scenario(name="A SaaS running OTel + Loki + Mimir", body="Every service uses OTel SDKs. OTel Collector DaemonSet receives via OTLP, splits to Loki (logs), Mimir (metrics), Tempo (traces — Lesson 33). Backends are Grafana stack, all open source. Cost: ~10× cheaper than a vendor SaaS, requires more ops effort."),
        Scenario(name="A bank running Prometheus + Thanos + ELK", body="Prometheus shards per cluster, write through Thanos to S3 for long-term. ELK for logs (full-text search required for compliance). 18-month log retention; PromQL across years via Thanos. Total observability spend: 5% of cluster cost — appropriate for a regulated industry."),
        Scenario(name="A startup using a vendor SaaS", body="Datadog (or Honeycomb / New Relic). OTel-compatible. One-line agent install. No backend ops. Cost: $$$ at scale. Tradeoff: speed-to-running vs eventual cost. Most startups land here, migrate to self-hosted at $1M+/yr observability spend."),
        Scenario(name="A team that fixed an MTTR problem with traces", body="Adopted OTel tracing across 14 services. New incident: \"checkout slow.\" Trace shows 4 services contributing to latency; bottleneck is an N+1 query in the inventory service. Pre-tracing, would have meant 2 hours of log-grepping. Post-tracing: 5 minutes."),
    ],
    misconceptions=[
        Misconception(myth="Logs replace metrics.", truth="They\'re complementary. Logs are great for \"what happened in this specific request.\" Metrics are great for \"how does the system behave over time?\" Querying logs at scale to compute aggregates is slow + expensive — that\'s what metrics are for."),
        Misconception(myth="Prometheus is the only metrics solution.", truth="Prometheus + Mimir / VictoriaMetrics / Thanos / Cortex are the main self-hosted options. Vendor SaaS (Datadog, Honeycomb, etc.) all support OpenMetrics + OTLP. Prometheus is most common; not the only path."),
        Misconception(myth="More logs = better observability.", truth="More logs = more cost + more noise. Useful logs are sparse: state changes, errors, edge-case branches. Routine info-level on every request is mostly waste. Use metrics for what happens often; logs for what\'s exceptional."),
    ],
    flashcards=[
        Flashcard(front="Three observability pillars?", back="Logs (discrete events), Metrics (numeric time series), Traces (distributed request flow). Modern stacks unify the three under OpenTelemetry."),
        Flashcard(front="What is OpenTelemetry (OTel)?", back="CNCF project unifying SDKs + collector across logs, metrics, traces. By 2026 the de-facto standard. Replaces older OpenTracing + OpenCensus."),
        Flashcard(front="Three log-collection patterns?", back="Node DaemonSet (most common), Sidecar (per-Pod), Direct-from-app via OTel SDK. DaemonSet scales best, sidecar handles legacy."),
        Flashcard(front="kube-state-metrics vs node-exporter?", back="kube-state-metrics: K8s API state (Pod counts, deployment ready replicas) as Prometheus metrics. node-exporter: node-level resources (CPU, memory, disk). Different domains, both common."),
        Flashcard(front="What\'s a cardinality bomb?", back="A metric label with high or unbounded uniqueness (user_id, request_id, full URL with IDs). Every unique combination = a new time series. Crashes Prometheus servers."),
        Flashcard(front="Loki vs Elasticsearch?", back="Loki: indexes labels only; full-text via grep at query time. Cheap, fast. Elasticsearch: full-text indexes. More powerful queries, more expensive."),
        Flashcard(front="Four golden signals?", back="Latency, Traffic, Errors, Saturation. Google SRE\'s framework. Every service\'s primary dashboard should show these four."),
        Flashcard(front="Vector?", back="Datadog\'s Rust-based logs/metrics shipping agent. Increasingly common alternative to Fluent Bit + Fluentd. Same role: collect on nodes, ship to backends."),
    ],
    quizzes=[
        Quiz(prompt="A service emits 50,000 log lines per minute at INFO. Cost spikes; on-call complains the logs are noise. What\'s the playbook?", answer="<strong>(1) Audit the noise.</strong> Sample 100 lines; categorise (\"request received,\" \"DB query,\" \"cache hit,\" etc.). 80% are routine flow. <strong>(2) Demote routine flow.</strong> Move \"request received,\" cache hits, etc. from INFO to DEBUG. Default to WARN or ERROR for production. <strong>(3) Use metrics for the routine.</strong> If you cared about \"how many requests received per minute,\" use a counter metric, not a log per request. <strong>(4) Add structured logging.</strong> Switch from text to JSON. Searches become 10× faster; can index specific fields. <strong>(5) Set log retention.</strong> 30 days hot, 90 days cold S3, 1 year archive. Most ops never read logs older than 14 days. <strong>Result:</strong> 80% volume reduction, faster searches, lower cost, better signal-to-noise."),
        Quiz(prompt="An on-call engineer pages: \"latency alert fired for service X, but I checked and latency is fine.\" What might be wrong?", answer="Several common diagnoses: <strong>(1) Alert tuning.</strong> Was the threshold set on absolute milliseconds or a percentile? P50 spike vs P99 spike are different beasts; \"latency increased 10ms\" might be normal noise. <strong>(2) The alert query is wrong.</strong> Maybe it\'s averaging across all requests including cached ones, masking the spike in the slow path. <strong>(3) Missing labels.</strong> The alert fires per-route but the engineer is looking at the overall dashboard. <strong>(4) Stale alert.</strong> Alert fires when one of N pods is slow; rolling restart resolved it; alert state didn\'t reset. <strong>(5) Lack of runbook.</strong> Alert annotation should explain: \"check P99 on this dashboard, not the average.\" <strong>Fix:</strong> alerts must include a query the engineer can copy/paste; runbook should link to the exact dashboard panel; tune thresholds to actually-paging conditions, not noise."),
        Quiz(prompt="The team ships an OTel-instrumented service. They want to verify traces are flowing end-to-end. <strong>Click for the diagnostic checklist. ▼</strong>", cyoa=True, cyoa_tag="the diagnostic checklist", answer="<strong>(1) App-side: are spans being created?</strong> Add an OTel debug exporter to log spans locally. Make a request; check the log. If empty, the SDK isn\'t initialised correctly (check service-name env var, OTLP endpoint). <strong>(2) App → Collector: is the connection succeeding?</strong> <code>kubectl logs deploy/otel-collector</code>; look for incoming OTLP receivers logging spans. If silent, check Service / DNS / TLS. <strong>(3) Collector → backend (Tempo / Jaeger / vendor): is the export working?</strong> Collector logs would show export failures (auth errors, network errors, schema mismatches). <strong>(4) Backend ingestion: do the spans appear?</strong> Query the backend; a known trace ID should resolve. <strong>(5) Cross-service propagation: do downstream services see the parent trace?</strong> Use the OTel test harness or an explicit X-trace test. <strong>(6) Sampling.</strong> If you sample at 1%, your test request might be one of the 99% dropped. Set sampling to 100% during validation. <strong>Tools:</strong> the otel-collector telemetrygen tool generates synthetic spans/metrics; use to validate the pipeline without the app."),
    ],
    glossary=[
        GlossaryItem(name="OpenTelemetry (OTel)", definition="CNCF project. Unified SDKs + collector for logs, metrics, traces. De-facto standard."),
        GlossaryItem(name="OTLP", definition="OpenTelemetry Protocol. The wire format / gRPC API for shipping telemetry. Every modern backend supports it."),
        GlossaryItem(name="OTel Collector", definition="Standalone agent. Receivers (in), processors (transform), exporters (out). Run as DaemonSet (per-node) or Deployment (gateway)."),
        GlossaryItem(name="Prometheus", definition="Pull-based metrics TSDB. The reference K8s metrics solution. PromQL query language."),
        GlossaryItem(name="Mimir / Cortex / Thanos", definition="Horizontally-scalable Prometheus extensions. Backend on object storage."),
        GlossaryItem(name="VictoriaMetrics", definition="Drop-in Prometheus replacement. Faster + lower memory at scale."),
        GlossaryItem(name="Loki", definition="Grafana\'s log store. Indexes labels; full-text via parsing at query."),
        GlossaryItem(name="Vector", definition="Datadog\'s Rust-based logs/metrics agent. Common DaemonSet for log collection."),
        GlossaryItem(name="Fluent Bit", definition="Lightweight log shipper. Long-time K8s default."),
        GlossaryItem(name="kube-state-metrics", definition="Exposes K8s API state as Prometheus metrics."),
        GlossaryItem(name="node-exporter", definition="Per-node OS-level metrics (CPU, memory, disk, network)."),
        GlossaryItem(name="ServiceMonitor / PodMonitor", definition="Prometheus Operator CRDs for declaratively configuring scrape targets."),
    ],
    recap_lead="Logs + metrics + (Lesson 33) traces. OTel standardises the SDKs + collector. K8s adds kube-state-metrics + node-exporter + cAdvisor. Avoid cardinality bombs. Pair alerts with runbooks; SLOs drive alerts.",
    recap_next="<strong>Next — Lesson 33: Observability Part 2.</strong> Tracing, eBPF-based observability (Hubble, Pixie, Cilium Tetragon), SLOs and the math behind them. Where requests actually spend their time.",
)
