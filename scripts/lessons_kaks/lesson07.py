"""K-AKS A7 — AKS Observability (Container Insights, AMP, AMG, ADOT, KQL, Network Observability)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AKS observability stack — Container Insights, Managed Prometheus, Managed Grafana, ADOT, App Insights, KQL.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Bell Tower — three signal pipes, one Grafana</text>
  <rect x="50" y="60" width="140" height="130" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="120" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">metrics</text>
  <text x="120" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Container Insights</text>
  <text x="120" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">Managed Prometheus (AMP)</text>
  <text x="120" y="135" text-anchor="middle" font-size="9" fill="#FFFFFF">→ AMG (Grafana)</text>
  <rect x="205" y="60" width="140" height="130" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="275" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">logs</text>
  <text x="275" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Log Analytics</text>
  <text x="275" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">workspace</text>
  <text x="275" y="135" text-anchor="middle" font-size="9" fill="#FFFFFF">KQL queries</text>
  <text x="275" y="150" text-anchor="middle" font-size="9" fill="#FFFFFF">→ alerts</text>
  <rect x="360" y="60" width="140" height="130" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="430" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">traces</text>
  <text x="430" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6">Application Insights</text>
  <text x="430" y="115" text-anchor="middle" font-size="9" fill="#FBF1D6">→ end-to-end</text>
  <text x="430" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">OR Azure Monitor</text>
  <text x="430" y="150" text-anchor="middle" font-size="9" fill="#FBF1D6">managed OpenTelemetry</text>
  <rect x="515" y="60" width="195" height="130" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="613" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">control + cost + network</text>
  <text x="613" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6">apiserver / audit log</text>
  <text x="613" y="113" text-anchor="middle" font-size="9" fill="#FBF1D6">Diagnostic Settings → LA</text>
  <text x="613" y="130" text-anchor="middle" font-size="9" fill="#FBF1D6">Network Observability</text>
  <text x="613" y="145" text-anchor="middle" font-size="9" fill="#FBF1D6">Azure Cost Management</text>
  <text x="613" y="170" text-anchor="middle" font-size="8" font-style="italic" fill="#FBF1D6">all visible in AMG</text>
</svg>"""


LESSON = LessonSpec(
    num="07",
    title_short="AKS observability",
    title_full="A7 · AKS Observability (Container Insights, AMP, AMG, ADOT, App Insights)",
    title_html="K-AKS A7 · AKS Observability",
    module_eyebrow="Module A7 · the Bell Tower — three signal pipes, one Grafana",
    hero_sub_html='Three signal pipes joined in <strong>Managed Grafana (AMG)</strong>. <strong>Metrics</strong> via Container Insights + <strong>Azure Monitor managed Prometheus (AMP)</strong>. <strong>Logs</strong> via Log Analytics workspace + <strong>KQL</strong>. <strong>Traces</strong> via Application Insights or <strong>Azure Monitor managed OpenTelemetry</strong>. Plus control-plane diagnostic settings, <strong>Network Observability</strong>, and <strong>Azure Cost Management</strong> for per-namespace spend visibility.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. CrashLoopBackOff alert: <em>\"checkout-service Pod restarting every 90 seconds.\"</em> You start clicking through the AKS portal: Container Insights shows the metric spike but no logs; you switch to Log Analytics in another tab and start typing KQL but don\'t remember the schema; you switch to Application Insights for the upstream API trace; the spans don\'t show the Pod names. <em>Three tools, three browser tabs, no joined view.</em> Today\'s lesson: AKS observability stitched together — and how AMG joins all three on one dashboard.",
    stamp_html="<strong>Three pipes (metrics → AMP, logs → Log Analytics, traces → App Insights / managed OTel) joined in Managed Grafana. Container Insights for K8s-aware visualisation; KQL for log search; control-plane diagnostic settings to capture audit + apiserver logs.</strong>",
    district_pin="kc-wing07",
    district_label="Bell Tower",
    sections=[
        Section(
            eyebrow="Section 1.1 · Container Insights + Managed Prometheus",
            h2="Container Insights + Managed Prometheus (AMP)",
            body_html="""    <p><strong>Container Insights</strong> = AKS-aware metrics + log dashboard, built on Log Analytics. Enable the <code>monitoring</code> add-on; an OMS agent DaemonSet ships node + Pod + container metrics + container stdout/stderr logs to a Log Analytics workspace. <em>Pre-built workbooks</em>: cluster overview, node health, Pod distribution, top-CPU containers.</p>
    <p><strong>Azure Monitor managed Prometheus (AMP)</strong> = Microsoft\'s managed Prometheus-as-a-service. AKS add-on installs the metrics collector (Prometheus Receiver / Azure Monitor Metrics Add-on); cluster + Pod metrics are scraped and stored in AMP. <em>Compatible with PromQL</em> + Prometheus alerting. Use AMP for <em>red-line metrics</em> (RED: rate, errors, duration; USE: utilization, saturation, errors).</p>
    <p><strong>Container Insights vs AMP</strong>: complementary, not competing. <em>Container Insights</em> = AKS-aware visualization + log integration. <em>AMP</em> = open-format Prometheus metrics with PromQL + alerting + Grafana compatibility. Most production AKS clusters enable both.</p>
    <p><strong>Azure Managed Grafana (AMG)</strong> consumes AMP, Application Insights, Log Analytics, and Azure Monitor as data sources — <em>one dashboard for all signal types</em>. Enterprise tier adds RBAC integration with Entra. Pre-built dashboards for AKS ship in the AMG gallery.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · Log Analytics + KQL",
            h2="Log Analytics + KQL — log search",
            body_html="""    <p><strong>Log Analytics workspace</strong> is Azure\'s log store. Container Insights writes container logs (<code>ContainerLogV2</code> table), kubelet events, and node syslog. Apiserver / audit logs land here too via diagnostic settings. <em>Standard for AKS deployments — central log destination.</em></p>
    <p><strong>KQL (Kusto Query Language)</strong> is the query language. SQL-like but pipe-based. Example: find all CrashLoopBackOff events in the last hour grouped by Pod:</p>
    <pre><code>KubeEvents
| where TimeGenerated &gt; ago(1h)
| where Reason == "BackOff"
| summarize Count = count() by PodName, Namespace
| order by Count desc</code></pre>
    <p>Standard tables: <code>ContainerLogV2</code>, <code>KubeEvents</code>, <code>KubeNodeInventory</code>, <code>KubePodInventory</code>, <code>InsightsMetrics</code>. <em>Saved KQL queries</em> can power alerts (\"alert if X CrashLoopBackOff in 5 min\") and Grafana panels.</p>
    <p><strong>Cost levers:</strong> log ingest is the typical AKS observability cost driver. <em>Sample container logs</em> in Container Insights config (e.g. drop verbose stdout in dev); <em>basic logs</em> tier for high-volume low-query data; <em>retention period</em> per table; <em>Data Collection Rules (DCRs)</em> route subsets to cheaper destinations.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · App Insights + ADOT / managed OpenTelemetry",
            h2="App Insights + Azure Monitor managed OpenTelemetry",
            body_html="""    <p><strong>Application Insights</strong> is Azure\'s app-performance monitoring product. Auto-instruments .NET / Node / Python / Java apps with traces, exceptions, dependency maps, transaction details. <em>End-to-end transaction traces</em> across services + Azure Functions + SQL DB.</p>
    <p><strong>Azure Monitor managed OpenTelemetry</strong> = Microsoft\'s managed OTel-compatible ingestion endpoint (also called the <em>Azure Monitor OpenTelemetry Distro</em>). For polyglot teams or open-standard purists. Same backend as App Insights but the collector is OTel-native — your code emits OTel spans/metrics/logs; ADOT-compatible collectors export to Azure Monitor.</p>
    <p><strong>Pick:</strong> App Insights for .NET-heavy / Microsoft-stack teams who want zero-config auto-instrumentation. Managed OpenTelemetry for polyglot / OSS-leaning teams who want vendor-neutral instrumentation.</p>
    <p><strong>Tracing patterns:</strong> propagate W3C Trace Context (<code>traceparent</code>) across services for end-to-end joins. Sample at the edge (10% of low-value, 100% of errors). Span tagging with K8s metadata (Pod name, namespace, node) makes spans correlatable with metrics.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · control-plane logs, network, cost",
            h2="Control-plane diagnostic settings, Network Observability, Cost Management",
            body_html="""    <p><strong>Control-plane diagnostic settings</strong> — enable apiserver, audit, audit-admin, controller-manager, scheduler, cluster-autoscaler, cloud-controller-manager log categories to flow to Log Analytics (or Event Hub / Storage). <em>Audit logs are essential for security forensics.</em> AKS Standard / Premium tier required for the long retention windows.</p>
    <p><strong>Network Observability</strong> — AKS add-on (preview/GA) that captures Pod-to-Pod flow data (Hubble for Cilium clusters; eBPF on Azure CNI Powered by Cilium). Visualizes east-west traffic, NetworkPolicy drops, DNS lookups. Surfaces hard-to-debug \"why is this connection refused?\" at the L4/L7 layer.</p>
    <p><strong>Azure Cost Management</strong> for AKS — enable <em>cost analysis with namespace-level granularity</em> (preview/GA depending on region). Surfaces per-namespace spend (split by compute, storage, network, log ingest). Without this you can see cluster total but not which team owns which slice — chargeback breaks.</p>
    <p><strong>Alerting:</strong> AMP supports Prometheus alerting rules → Action Groups → PagerDuty / Teams / email. Log Analytics supports KQL-based alerts. App Insights supports smart-detection alerts. Combine in <em>Azure Monitor Action Groups</em> as a single notification channel set.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="The team\'s log ingest cost has tripled in three months. The cluster has Container Insights enabled. What\'s the typical lever?",
            options=[
                ("Disable Container Insights entirely.", False),
                ("Use Container Insights\' container-log filtering to drop low-value namespaces (dev, system) and high-volume verbose logs; switch high-volume tables to Basic Logs tier; tune retention per table.", True),
                ("Buy more Log Analytics capacity.", False),
            ],
            feedback="Cost-tune via filters + Basic Logs + retention; don\'t turn off observability. Most AKS log ingest cost comes from a small set of chatty services.",
        ),
    },
    before_after_before='<p>Pre-managed AKS observability = Bring Your Own Prometheus + Bring Your Own Grafana + Bring Your Own log shipper (Fluent Bit / Filebeat) + ELK or Loki + custom alert routing. Operators ran 5+ Helm charts and a separate VMSS for the metrics+logs stack. AKS apiserver logs were essentially invisible without diagnostic-settings wiring. Tracing was unsupported in the basic stack — App Insights existed but was a separate sale.</p>',
    before_after_after='<p>Modern AKS gives you <strong>Container Insights</strong> (AKS-aware) + <strong>AMP</strong> (managed Prometheus) + <strong>AMG</strong> (managed Grafana) + <strong>App Insights / managed OpenTelemetry</strong> (traces) + <strong>Log Analytics</strong> (logs) + <strong>Network Observability</strong> + <strong>Cost Management</strong> at namespace granularity — all enabled with az CLI flags or AKS Automatic defaults. <em>One add-on each, one Grafana, one alert channel.</em></p>',
    before_after_caption='<p class="ba-caption"><em>The DIY observability era is over. Five managed services replace a 12-component homemade stack at a fraction of operational cost.</em></p>',
    analogy_intro_html='''<p>The <strong>Bell Tower</strong> at K-Campus is where everything that happens on campus is heard. Three different bells ring for three different signals.</p>
    <p>The <strong>Tempo Bell</strong> (metrics) rings on a regular cadence — once a minute it bongs the campus heartbeat: \"how full are the buildings? how many students are walking? how warm is the HVAC?\" The Container Insights bell-ringer hears campus-aware patterns; the Managed Prometheus (AMP) bell-ringer follows industry-standard PromQL bell patterns.</p>
    <p>The <strong>Story Bell</strong> (logs) chimes whenever something narratable happens — \"Professor Jones entered building C\", \"a student couldn\'t find a room\", \"the Auditorium HVAC threw an error.\" The bell echoes are recorded in the Log Analytics archive; you query the archive in <strong>KQL</strong> to find patterns (\"how many \'door is jammed\' chimes in the last hour?\").</p>
    <p>The <strong>Journey Bell</strong> (traces) follows a single visitor end-to-end — \"this visitor entered through the South Gate, walked to Building A, talked to Reception, was directed to Building C, met Professor Y, signed a form.\" The Application Insights bell-ringer sketches the path; the managed OpenTelemetry bell-ringer uses an open notation any visiting bell-ringer understands.</p>
    <p>All three bell-ringers also hand their notes to the <strong>Bell Tower Curator</strong> (Azure Managed Grafana) who composes one master dashboard everyone can read.</p>''',
    translation_rows=[
        ("Tempo Bell", "Metrics"),
        ("Container Insights bell-ringer", "Container Insights — AKS-aware metrics view"),
        ("AMP bell-ringer", "Azure Monitor managed Prometheus — PromQL"),
        ("Story Bell", "Logs"),
        ("Story Bell archive", "Log Analytics workspace"),
        ("Story-archive query language", "KQL (Kusto Query Language)"),
        ("Journey Bell", "Traces"),
        ("Journey Bell .NET-savvy ringer", "Application Insights"),
        ("Journey Bell open-notation ringer", "Azure Monitor managed OpenTelemetry"),
        ("Bell Tower Curator", "Azure Managed Grafana (AMG)"),
        ("Apiserver-meeting transcripts", "Control-plane diagnostic settings"),
        ("\"Who walked from A to C?\"", "Network Observability (Hubble / Cilium eBPF)"),
        ("Per-department budget ledger", "Azure Cost Management — per-namespace cost"),
    ],
    analogy_stops="A bell tower has three independent bells; in real Azure, signal types share a backend (Log Analytics underlies Container Insights and apiserver logs) — the metaphor over-separates them.",
    eli5="A tower with three bells. One says how busy the campus is right now. One records every story so you can search it later. One follows one person through the day. They all also write to the same big poster everyone can read.",
    eli10="AKS observability = three signal pipes joined in <strong>AMG</strong>. <strong>Metrics:</strong> Container Insights (AKS-aware) + AMP (managed Prometheus, PromQL). <strong>Logs:</strong> Log Analytics + KQL queries. <strong>Traces:</strong> Application Insights (zero-config for .NET) or managed OpenTelemetry (vendor-neutral OSS). Plus <strong>control-plane diagnostic settings</strong> (apiserver / audit / scheduler / etc. → Log Analytics), <strong>Network Observability</strong> (Hubble eBPF flows), <strong>Cost Management</strong> (per-namespace). All visible in AMG dashboards; alerts route via Action Groups.",
    scenarios=[
        Scenario(
            name="SaaS — RED dashboard in AMG built from AMP + App Insights",
            body="A SaaS team builds a per-service RED dashboard (Rate, Errors, Duration) in AMG. <em>Rate</em> + <em>Errors</em> from AMP via PromQL on Pod-emitted metrics; <em>Duration</em> from Application Insights percentile metrics. One dashboard joins both data sources; on-call sees red-line indicators per service in 30 seconds. <em>MTTR for a typical p99 spike: 11 minutes vs 35 before AMG.</em>",
        ),
        Scenario(
            name="Bank — apiserver audit log to Sentinel for SOC",
            body="A bank enables AKS apiserver + audit + audit-admin diagnostic settings to a dedicated Log Analytics workspace, mirrored to Sentinel. Sentinel rules detect: kubectl exec into Pods in prod namespaces, RoleBinding changes outside CI, secret reads outside expected SAs. <em>SOC owns the AKS audit story; platform team gets the alert routing.</em>",
        ),
        Scenario(
            name="Cost — per-namespace chargeback rolled out across tenant clusters",
            body="A multi-tenant SaaS platform team enables Cost Management with per-namespace granularity. Monthly export to a Storage Account; PowerBI report joins namespace → tenant mapping. <em>Tenants now see their actual cost; over-provisioned tenants get bills that prompt resource cleanup; finance has chargeback.</em>",
        ),
        Scenario(
            name="Polyglot team — managed OpenTelemetry replaces a Jaeger DIY stack",
            body="A 30-service team had been running self-hosted Jaeger for traces. Migration: instrument apps with OpenTelemetry SDKs; configure exporters to <strong>Azure Monitor managed OpenTelemetry</strong>. Traces appear in App Insights with the same data model. <em>Decommissioned Jaeger + Cassandra backend; -3 components to operate.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Container Insights and AMP do the same thing.\"",
            truth="Complementary. <strong>Container Insights</strong> = K8s-aware visualization built on Log Analytics; great for cluster overview, top-CPU containers, node health workbooks. <strong>AMP</strong> = open-format Prometheus metrics + PromQL + Prometheus alerting. AMP integrates with Grafana naturally; Container Insights answers \"is my cluster healthy?\" out of the box.",
        ),
        Misconception(
            myth="\"Tracing is only worth it for big distributed systems.\"",
            truth="Even a 3-service deployment benefits from traces — the moment a request crosses one service boundary, log-based debugging becomes a join problem. App Insights / managed OpenTelemetry auto-instrument enough for these gains in days, not weeks. The cost is small relative to the MTTR reduction on user-facing latency issues.",
        ),
        Misconception(
            myth="\"Log Analytics retention defaults are fine.\"",
            truth="Defaults are 30 days for most tables — too short for compliance (often 1 year) and too long for high-volume verbose logs (often days). Tune per-table retention. Use Basic Logs tier for high-volume infrequent-query data; Archive tier for compliance retention with infrequent reads. Without this discipline log ingest costs dominate AKS spend.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three observability signal types in AKS — what backs each?", back="<strong>Metrics:</strong> Container Insights (AKS-aware, on Log Analytics) + AMP (managed Prometheus). <strong>Logs:</strong> Log Analytics workspace + KQL. <strong>Traces:</strong> Application Insights or Azure Monitor managed OpenTelemetry."),
        Flashcard(front="What is AMG and what does it consume?", back="<strong>Azure Managed Grafana</strong> — managed Grafana service. Consumes AMP, App Insights, Log Analytics, Azure Monitor as native data sources. Enterprise tier integrates with Entra RBAC. Pre-built AKS dashboards in the gallery."),
        Flashcard(front="What is KQL?", back="<strong>Kusto Query Language</strong> — Azure\'s SQL-like pipe-based query language for Log Analytics. Standard tables for AKS: <code>ContainerLogV2</code>, <code>KubeEvents</code>, <code>KubeNodeInventory</code>, <code>KubePodInventory</code>, <code>InsightsMetrics</code>."),
        Flashcard(front="When pick App Insights vs managed OpenTelemetry?", back="<strong>App Insights</strong>: .NET / Microsoft-stack, want zero-config auto-instrumentation. <strong>Managed OpenTelemetry</strong>: polyglot / OSS-leaning, want vendor-neutral instrumentation. Same backend; different SDK + collector."),
        Flashcard(front="Control-plane diagnostic settings — what categories matter?", back="<code>kube-apiserver</code> (api requests), <code>kube-audit</code> (security forensics), <code>kube-audit-admin</code>, <code>kube-controller-manager</code>, <code>kube-scheduler</code>, <code>cluster-autoscaler</code>, <code>cloud-controller-manager</code>. Route to Log Analytics for KQL search; or to Event Hub for SIEM ingest."),
        Flashcard(front="What does Network Observability do?", back="Captures Pod-to-Pod flow data (Hubble eBPF on Cilium clusters). Visualises east-west traffic, NetworkPolicy drops, DNS lookups. Useful for \"why is this connection refused?\" at L4/L7."),
        Flashcard(front="Per-namespace cost — how surfaced?", back="<strong>Azure Cost Management</strong> with cost analysis at namespace-level granularity. Splits compute / storage / network / log ingest per namespace. Foundation of internal chargeback and tenant billing."),
        Flashcard(front="Three knobs to tune Log Analytics cost?", back="(1) Filter at the source — Container Insights config drops low-value namespaces and verbose logs. (2) Tier per table — Basic Logs for high-volume low-query, Archive for compliance retention. (3) Retention per table — short for noisy data, long for audit logs. DCRs route subsets cleanly."),
    ],
    quizzes=[
        Quiz(
            prompt="The team has Container Insights enabled but the on-call uses kubectl to check Pod logs because \"the portal is too slow.\" What\'s the workflow upgrade?",
            answer="Build a 4-panel KQL dashboard in AMG: (1) <code>KubeEvents</code> filtered to the namespace + last 15 min; (2) <code>ContainerLogV2</code> tail for the alerting Pod; (3) AMP RED metrics for the service; (4) App Insights trace for the failing request. Pin the dashboard in AMG; bookmark in browser. On-call clicks one URL, has all 4 panes scoped to the alert. Time-to-diagnosis drops from 8-12 min (multiple kubectl + portal switches) to under 2 min.",
        ),
        Quiz(
            prompt="The CFO asks: \"Why is observability spend $40K/month for a $90K cluster?\" The platform engineer investigates. What\'s typically going on?",
            answer="Three usual suspects: (1) <strong>verbose stdout logs</strong> from a chatty service — single Deployment dumping debug-level JSON in production. Fix: log level + sample. (2) <strong>Default retention 30+ days on every table</strong> — high-volume tables like <code>ContainerLogV2</code> ingested forever. Fix: tier-down to Basic Logs or 7-day retention. (3) <strong>Apiserver verbose audit logs at full fidelity</strong> when only audit-admin events are needed for compliance. Fix: per-category category-filter in diagnostic settings. Typical reduction: 40-70% with zero loss of operational signal.",
        ),
        Quiz(
            prompt="Black Friday eve. The team wants p99 latency, error rate, and traffic in one alert chain to one channel. They have AMP, Application Insights, and Log Analytics. How do they wire this in 30 minutes?",
            answer="Single <strong>Action Group</strong> in Azure Monitor as the notification target (PagerDuty webhook + Teams + email). Three alert sources: (a) AMP <em>Prometheus alert rule</em>: <code>histogram_quantile(0.99, ...) &gt; 500ms</code> → Action Group; (b) App Insights <em>availability test</em> + <em>smart detection</em> on response time → same Action Group; (c) Log Analytics <em>scheduled query rule</em>: KQL counting 5xx in <code>ContainerLogV2</code> → same Action Group. <em>One channel, three sources, no duplicate routing config.</em>",
            cyoa=True,
            cyoa_tag="how the holiday alerting got wired in 30 minutes",
        ),
    ],
    glossary=[
        GlossaryItem(name="Container Insights", definition="AKS-aware monitoring add-on built on Log Analytics. Pre-built workbooks for cluster, node, Pod, container."),
        GlossaryItem(name="Azure Monitor managed Prometheus (AMP)", definition="Microsoft\'s managed Prometheus-as-a-service. PromQL-compatible. Add-on installs metrics scraper."),
        GlossaryItem(name="Azure Managed Grafana (AMG)", definition="Managed Grafana service. Native data sources: AMP, App Insights, Log Analytics, Azure Monitor."),
        GlossaryItem(name="Log Analytics workspace", definition="Azure\'s log store. Container Insights + apiserver diagnostic settings target it. Queried via KQL."),
        GlossaryItem(name="KQL", definition="Kusto Query Language — Azure\'s pipe-based SQL-like query language for Log Analytics."),
        GlossaryItem(name="Application Insights", definition="Azure\'s APM product. Auto-instruments .NET / Node / Python / Java; provides end-to-end transaction traces."),
        GlossaryItem(name="Azure Monitor managed OpenTelemetry", definition="Microsoft\'s OTel-compatible ingestion endpoint. Vendor-neutral instrumentation; same backend as App Insights."),
        GlossaryItem(name="Diagnostic Settings", definition="Per-resource config that ships logs/metrics to Log Analytics, Event Hub, or Storage. Critical for AKS apiserver / audit logs."),
        GlossaryItem(name="Network Observability", definition="AKS add-on capturing Pod-to-Pod flow data via Hubble (Cilium eBPF). Visualises east-west, NetworkPolicy drops, DNS."),
        GlossaryItem(name="Azure Cost Management", definition="Cost analysis tool. AKS namespace-level granularity surfaces per-tenant spend for chargeback."),
        GlossaryItem(name="Action Group", definition="Azure Monitor notification target — PagerDuty webhook, Teams, email. Single channel for AMP / Log Analytics / App Insights alerts."),
        GlossaryItem(name="Basic Logs / Archive", definition="Lower-cost Log Analytics tiers for high-volume low-query (Basic) and compliance retention with infrequent reads (Archive)."),
    ],
    recap_lead='Three pipes (metrics + logs + traces) joined in Managed Grafana; control-plane diagnostic settings + Network Observability + Cost Management close the loop. Cost-tune log ingest with filters + tiers + retention.',
    recap_next='<strong>Next — A8: AKS Add-ons and Platform Features.</strong> Managed add-ons (KEDA, Dapr, Istio service mesh, Flux v2 GitOps, Workload Identity, Key Vault Secrets Provider, App Routing), Azure Arc-enabled K8s, AKS hybrid (Azure Local / Edge Essentials), Fleet Manager.',
)
