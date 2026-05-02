from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Observatory tower: a trace timeline showing nested spans across services, an eBPF kernel-instrumentation panel showing kernel-level signals, and an SLO dial with error budget remaining.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">OBSERVATORY · TRACES, eBPF, SLOs</text>
  <!-- Trace timeline -->
  <g transform="translate(40,55)">
    <text x="140" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">DISTRIBUTED TRACE</text>
    <rect x="0" y="22" width="280" height="12" rx="2" fill="#3F4A5E"/>
    <text x="6" y="32" font-size="8" fill="#FBF1D6" font-weight="700">gateway</text>
    <rect x="20" y="38" width="240" height="10" rx="2" fill="#5A9F7A"/>
    <text x="26" y="46" font-size="7" fill="#FFFFFF" font-weight="700">checkout-service</text>
    <rect x="50" y="52" width="160" height="10" rx="2" fill="#4A8FA8"/>
    <text x="56" y="60" font-size="7" fill="#FFFFFF" font-weight="700">auth-service</text>
    <rect x="70" y="66" width="100" height="10" rx="2" fill="#A04832"/>
    <text x="76" y="74" font-size="7" fill="#FFFFFF" font-weight="700">db query 60ms</text>
    <rect x="180" y="66" width="40" height="10" rx="2" fill="#E8B547"/>
    <text x="184" y="74" font-size="7" fill="#5A4F45" font-weight="700">cache</text>
    <text x="0" y="90" font-size="7" fill="#5A4F45">0ms</text>
    <text x="280" y="90" text-anchor="end" font-size="7" fill="#5A4F45">320ms total</text>
  </g>
  <!-- eBPF -->
  <g transform="translate(340,55)">
    <rect width="150" height="80" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <text x="75" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">eBPF</text>
    <text x="75" y="34" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">kernel-level instrumentation</text>
    <rect x="10" y="42" width="130" height="14" rx="2" fill="#5A9F7A"/>
    <text x="15" y="52" font-size="7" fill="#FFFFFF" font-weight="700">syscalls · network · trace</text>
    <rect x="10" y="58" width="130" height="14" rx="2" fill="#A04832"/>
    <text x="15" y="68" font-size="7" fill="#FFFFFF" font-weight="700">no app changes needed</text>
  </g>
  <!-- SLO dial -->
  <g transform="translate(510,55)">
    <text x="65" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">SLO · error budget</text>
    <circle cx="65" cy="65" r="40" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <path d="M 65 25 A 40 40 0 1 1 35 100" fill="none" stroke="#5A9F7A" stroke-width="8" stroke-linecap="round"/>
    <path d="M 35 100 A 40 40 0 0 1 25 65" fill="none" stroke="#A04832" stroke-width="8" stroke-linecap="round"/>
    <text x="65" y="62" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E">73%</text>
    <text x="65" y="76" text-anchor="middle" font-size="7" fill="#5A4F45">budget left</text>
    <text x="65" y="120" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">99.9% target</text>
  </g>
  <text x="340" y="200" text-anchor="middle" font-size="0" fill="#3F4A5E"></text>
</svg>"""

LESSON = LessonSpec(
    num="33",
    title_short="obs Pt 2 traces/eBPF",
    title_full="Observability Part 2 · Traces, eBPF, SLOs",
    title_html="Lesson 33 — Observability Part 2 · K-COM",
    module_eyebrow="Module 14 · Lesson 33 · the third pillar plus eBPF and SLOs",
    hero_sub_html='Traces show <em>where requests spend time</em> across services. eBPF-based tools (Hubble, Pixie, Cilium Tetragon) show <em>what the kernel saw</em> without app changes. <strong>SLOs</strong> turn observability data into honest reliability targets — and into the alerts that page you.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='\"Checkout is slow.\" Hours spent grepping logs across 8 services. Each team says \"we\'re fast.\" Eventually you find the problem: service A blocks for 200ms waiting on service B, which blocks for 150ms waiting on service C\'s cache miss, which is misconfigured. With <em>distributed tracing</em>, this would have taken 2 minutes — open the slow trace, see exactly where time went. Without traces, you\'re reconstructing the request flow from log timestamps, which is harder than it sounds.',
    stamp_html='<strong>Traces</strong> answer \"where did time go in this request?\" Implement with OTel SDKs; store in <strong>Tempo / Jaeger</strong>. <strong>eBPF</strong> tools (Hubble, Pixie, Tetragon) get kernel-level visibility without app changes. <strong>SLOs</strong> are explicit reliability targets (e.g., \"99.9% of requests under 200ms over 30 days\"); the gap between target and reality is your <em>error budget</em>. Alerts page when the budget burns fast.',
    district_pin="kt-pin32",
    district_label="Observatory — Tracing & Reliability Wing",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What a trace is",
            body_html="""    <p>A <strong>trace</strong> is the record of a single request as it flows through a distributed system. Each unit of work is a <strong>span</strong>: \"service X processed step Y in Z ms.\" Spans are nested: when service A calls service B, A\'s span contains B\'s span as a child. Spans share a <strong>trace ID</strong> (so you can find them all) and have <strong>span IDs</strong> + <strong>parent span IDs</strong> (so you can rebuild the tree).</p>
    <p>The OTel model is one trace ID per request, propagated through the call chain via the <code>traceparent</code> HTTP header (W3C Trace Context standard). Every service in the chain sees the trace ID, creates its own spans, and ships them to a tracing backend.</p>
    <p>What you get in return: a <strong>flame graph</strong> of one request across N services, showing exactly which span was slow. The single best debugging tool for distributed systems.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Tracing in practice",
            h2="Auto-instrumentation, sampling, backends",
            body_html="""    <p><strong>Auto-instrumentation</strong>: OTel ships SDKs for every major language. The Java agent and Python's auto-instrumentor add tracing to many libraries (HTTP clients, gRPC, databases) without code changes. Java: <code>java -javaagent:opentelemetry-javaagent.jar -jar app.jar</code>. Python: <code>opentelemetry-instrument</code> wraps your entry point. Most apps get traced for free.</p>
    <p><strong>Sampling</strong>: at scale, tracing 100% of requests is too expensive. Three patterns:</p>
    <ul>
      <li><strong>Head sampling</strong> — decide at the entry point (gateway): \"trace 1% of all requests.\" Simple, predictable cost. Loses interesting tails.</li>
      <li><strong>Tail sampling</strong> — collect everything per request, decide after seeing the result: \"trace this if it errored or took &gt;1s.\" Better signal, harder ops.</li>
      <li><strong>Adaptive sampling</strong> — modern approach: combine head + tail. OTel Collector\'s tail-sampling processor implements this.</li>
    </ul>
    <p><strong>Backends</strong>: <strong>Tempo</strong> (Grafana, object-storage backed, cheap), <strong>Jaeger</strong> (CNCF, mature), vendor SaaS (Honeycomb, Datadog, Lightstep). All consume OTLP.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · eBPF observability",
            h2="The view from the kernel",
            body_html="""    <p>OTel SDKs require code changes (or auto-instrumentation injection). <strong>eBPF</strong>-based tools observe from the kernel — no app changes, no SDK, no language support needed. The cost: kernel-level metrics, not application semantics.</p>
    <p>Three popular eBPF tools:</p>
    <ul>
      <li><strong>Hubble</strong> (Cilium) — per-flow network observability. \"Service X talked to Y on port 443; 12ms latency; HTTP 200.\" Built on Cilium\'s eBPF data plane (Lesson 24).</li>
      <li><strong>Pixie</strong> (New Relic, formerly Pixie Labs) — installs as a DaemonSet, instruments syscalls + HTTP/gRPC traffic at the kernel. PXL queries (Python-like) over the in-cluster data. Free for small clusters.</li>
      <li><strong>Cilium Tetragon</strong> — security-focused eBPF: detect process exec, file opens, network connects. Generates events for any of these and routes to your SIEM. Powerful for runtime detection.</li>
    </ul>
    <p>eBPF is also the backbone of:</p>
    <ul>
      <li>Continuous profiling — <strong>Parca</strong> / <strong>Pyroscope</strong> profile every process in production with low overhead.</li>
      <li><strong>Falco</strong> — runtime security: alert on suspicious syscall patterns. Lesson 31.</li>
      <li>Network performance monitoring — <strong>cilium hubble observe</strong>.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>eBPF\'s sweet spot: getting visibility into already-deployed apps that you can\'t modify. Vendor SaaS, legacy services, third-party Pods. The OTel SDK route gives semantically richer signals (\"this is the user-checkout flow, this part is auth\"). For new code, instrument with OTel; for old/opaque code, layer eBPF on top.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · SLOs — turning data into reliability commitments",
            h2="Error budgets and burn-rate alerts",
            body_html="""    <p>An <strong>SLO</strong> (Service Level Objective) is a target for a service\'s reliability over a window. Format: \"99.9% of HTTP requests succeed within 200ms, measured over 30 rolling days.\" Three components:</p>
    <ul>
      <li><strong>SLI</strong> (indicator) — what you measure. \"Successful requests / total requests.\"</li>
      <li><strong>SLO</strong> (objective) — the target. \"99.9%.\"</li>
      <li><strong>Error budget</strong> — the allowed failure. 100% - 99.9% = 0.1%. With 1M requests/month, you can fail 1000 and still hit your SLO.</li>
    </ul>
    <p>SLOs drive everything else. Alerts fire on <strong>burn rate</strong> — \"if you keep failing at this rate, you\'ll exceed your error budget in 1 hour\" — not on raw error counts. Alerts that page humans correspond to budget at risk; alerts that don\'t are noise.</p>
    <p>Tools that turn SLO definitions into Prometheus alerts:</p>
    <ul>
      <li><strong>Sloth</strong> (Slok.dev) — YAML SLO → Prometheus rules. Multi-window-multi-burn-rate alerts (Google SRE method) baked in.</li>
      <li><strong>Pyrra</strong> — K8s-native; SLO CRD; UI for budget tracking.</li>
      <li><strong>OpenSLO</strong> — emerging vendor-neutral spec.</li>
    </ul>
    <p>The reliability-cost trade: chasing 99.99% costs 10× more than 99.9%. SLOs are how the org agrees on which trade to make. Engineers don\'t commit to 99.99% \"because reliability is good\" — they commit to it because product / users actually need it.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team has \"99.9% over 30 days\" as their SLO. Their service has been at 99.85% for the last 5 days. The error budget for the month allows 0.1% failures. What does \"burn rate\" tell them?",
            options=[
                ("a) They have already exceeded their SLO; mark as failed", False),
                ("b) Their current 5-day burn rate is high — they\'ll exceed the 30-day budget by ~day 18 if it continues. Time to investigate before paging is needed", True),
                ("c) The SLO is too strict — relax it", False),
            ],
            feedback="<strong>Answer: b.</strong> Burn-rate alerts (multi-window-multi-burn-rate, Google SRE method) catch fast burns early — \"at this rate you\'ll exhaust budget in X hours\" — letting teams investigate before the SLO actually breaks. Far better than waiting for a hard-line 99.9% threshold to trip.",
        ),
    },
    before_after_before='<p>Pre-tracing era: \"the request is slow\" → grep logs across 8 services by timestamp, hope clocks are synced, reconstruct the call chain by hand. SLOs were aspirational notes in a wiki. eBPF was a research curiosity. Each app needed its own custom instrumentation.</p>',
    before_after_after='<p>OTel-instrumented services emit traces; one click in Grafana shows the flame graph. Hubble shows per-flow network signals without app changes. Pyrra shows real-time error budget remaining. Alerts fire on burn rate, not raw thresholds. MTTR drops from hours to minutes; on-call sleeps better.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Tracing + eBPF + SLOs is what \"observability\" actually means in 2026. The Three Pillars era is behind us; the future is unified semantic + kernel signals tied to explicit reliability targets.</p>',
    analogy_intro_html='<p>Two more rooms in the Observatory. The <strong>tracing room</strong> has a flight-data recorder for every request: when it entered the city, which buildings it visited, how long it spent in each, who else it talked to. Open one flight record and you see the whole journey as a flame chart. The <strong>eBPF wing</strong> has kernel-level sensors at every building entrance — they don\'t care what the building does, only what flows in and out at the OS level. Together, the two views answer different questions: tracing gives you semantics (\"this is the auth step, this is the cache lookup\"), eBPF gives you ground truth (\"the kernel saw 7 syscalls and a network read\").</p><p>Off to one side: the <strong>SLO board</strong>. Every service has a reliability target posted publicly. A meter shows error budget remaining. The on-call gets paged when the meter is burning fast — not on every blip, only when reliability is actually at risk.</p>',
    translation_rows=[
        ("Flight-data recorder per request", "Distributed trace"),
        ("Each leg of the journey on the recorder", "Span"),
        ("Recorder ID printed on the boarding pass", "Trace ID + W3C traceparent header"),
        ("Flame graph of the whole journey", "Trace visualisation (Tempo / Jaeger UI)"),
        ("Kernel-level sensors", "eBPF programs"),
        ("Per-flow network sensor", "Hubble"),
        ("\"What\'s every process doing right now\" sensor", "Pixie / Cilium Tetragon"),
        ("Public reliability target", "SLO"),
        ("Allowable failure budget", "Error budget"),
        ("\"Burning too fast\" alarm", "Burn-rate alert"),
    ],
    analogy_stops="The analogy stops here: real traces aren\'t pre-recorded — they\'re sampled subsets reconstructed from spans shipped post hoc, and they\'re only as good as your propagation discipline. \"Flight-data recorder for every request\" is sampling-dependent.",
    eli5='Imagine your toy went on an adventure through 5 rooms. The trace is a map showing how long it spent in each room. The eBPF is the doorbell at every room saying \"toy went in, toy came out, took 3 minutes.\" The SLO is your promise: \"toy will finish 99 of 100 adventures in time for dinner.\"',
    eli10="Traces show where time goes across services — instrument with OTel SDKs; ship spans to Tempo/Jaeger via OTLP. eBPF tools (Hubble, Pixie, Tetragon) observe at the kernel — no app changes. SLOs explicitly state reliability targets (e.g., \"99.9% under 200ms over 30 days\"); error budget = allowed failures. Burn-rate alerts catch fast burns before SLO is broken. Sloth / Pyrra generate alert rules from SLO YAML.",
    scenarios=[
        Scenario(name="A SaaS using OTel + Tempo for tracing", body="Every Go service has the OTel SDK; auto-instrumentation for HTTP, gRPC, Postgres clients. Tempo backend on S3 for cheap long-term retention. Tail sampling at 100% for errors + slow traces, 1% for normal. Storage cost ~$0.10 per million traces. MTTR for cross-service issues halved."),
        Scenario(name="A bank using Cilium Hubble for flow visibility", body="Pre-existing apps; instrumentation requires legal review per service. Hubble is install-once and gives per-flow signals immediately: \"<code>auth-service</code> connected to <code>user-db</code>, port 5432, latency 8ms.\" Found a misrouted flow within first day of install. Compliance pleased: no app changes."),
        Scenario(name="A startup using Pixie for live debugging", body="Pixie DaemonSet on every node. Engineers run PXL queries in production: \"show me all HTTP 500s in the last 5 minutes from service X.\" Like running tcpdump and Wireshark with structured queries. Especially useful for langs/frameworks where OTel SDKs don\'t work well."),
        Scenario(name="A team using Pyrra for SLO management", body="Each service ships an SLO YAML alongside its manifests. Pyrra generates Prometheus burn-rate alerts. Engineers see error-budget remaining on a Grafana panel; product sees SLA status in their dashboards. \"Should we deploy this risky change?\" answered by checking remaining budget — not gut feel."),
    ],
    misconceptions=[
        Misconception(myth="Tracing replaces logs.", truth="Traces show <em>where time went</em> in a request; logs show <em>what happened</em> within each step. They\'re complementary. A span\'s log statements + the surrounding trace context is more useful than either alone."),
        Misconception(myth="eBPF observability replaces OTel.", truth="They answer different questions. OTel sees app semantics (\"this is a user_login\"); eBPF sees the kernel (\"this is a connect+sendto+recv\"). Combined: powerful. Either alone misses half the picture."),
        Misconception(myth="A 99.99% SLO is more impressive than 99.9%.", truth="It\'s also 10× more expensive. \"More 9s\" isn\'t a virtue. The right SLO is the one your users actually need; over-targeting wastes engineering capacity."),
    ],
    flashcards=[
        Flashcard(front="What is a trace?", back="A record of one request flowing through services. Composed of nested spans sharing a trace ID. Spans have parent IDs forming a tree."),
        Flashcard(front="W3C Trace Context?", back="Standard for trace propagation. Header <code>traceparent: 00-{trace-id}-{span-id}-{flags}</code>. Every modern HTTP library propagates it."),
        Flashcard(front="Head sampling vs tail sampling?", back="Head: decide whether to trace at the entry point (fast, predictable, loses tails). Tail: collect everything, decide after seeing result (better signal, more ops). Adaptive: combine."),
        Flashcard(front="What is Tempo?", back="Grafana\'s tracing backend. Object-storage-based; cheap. Consumes OTLP. Pairs with Loki + Mimir + Grafana."),
        Flashcard(front="Hubble?", back="Cilium\'s per-flow network observability. eBPF-based. Shows source/dest/protocol/policy decision per flow."),
        Flashcard(front="Pixie?", back="eBPF-based DaemonSet for in-cluster observability. Auto-instruments HTTP/gRPC at the kernel. Free for small clusters."),
        Flashcard(front="What is an SLO?", back="Service Level Objective. \"99.X% of requests succeed in &lt;Yms over Z days.\" Drives alerting + reliability investment."),
        Flashcard(front="Error budget?", back="The complement of an SLO. 99.9% SLO = 0.1% budget = 1000 fails per million. Used as \"reliability currency\" — burn it on risky deploys, save it for stable periods."),
        Flashcard(front="Burn rate alert?", back="Alert based on \"how fast you\'re consuming the error budget.\" Multi-window-multi-burn-rate (Google SRE) is the standard pattern. Pages on fast burns, not on every error."),
        Flashcard(front="Sloth vs Pyrra?", back="Sloth: YAML SLO → Prometheus rules; older + popular. Pyrra: K8s-native CRD; UI; newer. Both implement burn-rate alerts."),
    ],
    quizzes=[
        Quiz(prompt="A team\'s P99 latency dashboard shows a spike. They want to find the slow requests. What\'s the workflow with traces?", answer="<strong>(1) Click the spike on the dashboard</strong> — Grafana panel for P99 should be linked to the trace backend with a time-window filter. <strong>(2) Tempo / Jaeger UI</strong> shows traces in that window, sorted by duration descending. <strong>(3) Open the slowest trace</strong> — flame graph shows where time went across services. <strong>(4) Identify the slow span</strong> — usually one service or one DB call dominates. <strong>(5) Drill into that service\'s logs</strong> via the trace ID; correlated logs explain the slow path. <strong>Pre-tracing</strong>, the same workflow took an hour of cross-service log grep. With traces, 2 minutes."),
        Quiz(prompt="A team adopts SLOs. They write \"99.99% over 30 days\" for their internal user-mgmt service. Their ops budget can\'t support that. What\'s the conversation?", answer="<strong>SLOs aren\'t aspirational; they\'re commitments.</strong> The ops budget tells you what\'s achievable. <strong>Discussion:</strong> (1) What\'s the actual user need? Does the user-mgmt service have to be 99.99%? Often \"login during business hours\" is the real constraint. (2) What\'s the current performance? Measure it for a month before committing. (3) What\'s the cost of the next 9? 99.9 → 99.99 = ~10× the engineering effort. (4) Is the upstream dependency reliable enough? You can\'t be more reliable than your dependencies. <strong>Outcome:</strong> usually the SLO drops to 99.9% or even 99.5%, with explicit acknowledgement of the trade-off. Honest SLOs build trust; aspirational SLOs cause permanent paging."),
        Quiz(prompt="Production has been on fire for 3 hours. The team is firefighting reactively. <strong>Click for what they should do tomorrow. ▼</strong>", cyoa=True, cyoa_tag="the post-incident playbook", answer="<strong>(1) Document the incident.</strong> Timeline (when alerts fired, who responded, what was done), root cause, contributing factors. Blameless. <strong>(2) Computed observability gap.</strong> What did you wish you had? Traces? eBPF? Better logs? Specific SLOs? Each \"I wish I had X\" is the highest-priority observability investment. <strong>(3) Update SLOs.</strong> Did the incident burn unbudgeted error budget? Recalibrate the SLO if reality is different from assumption. <strong>(4) Add the missing alert.</strong> Whatever caught the issue (probably a customer ticket) should have been an alert. Add it as a burn-rate alert if it relates to an SLO. <strong>(5) Update the runbook.</strong> The runbook for the alert should describe what the team did to remediate. Next on-call doesn\'t have to learn what you learned. <strong>(6) Schedule an observability sprint.</strong> The post-mortem identifies gaps; turn each into a ticket; close them within a quarter. <strong>The lesson:</strong> the cheapest observability is the kind you set up before you need it. Don\'t skip the sprint."),
    ],
    glossary=[
        GlossaryItem(name="Trace", definition="Record of one request across services. Composed of nested spans."),
        GlossaryItem(name="Span", definition="One unit of work in a trace. Has start/end time, parent span ID, attributes."),
        GlossaryItem(name="Trace ID", definition="Unique identifier shared by all spans of one request."),
        GlossaryItem(name="W3C Trace Context", definition="Standard for trace propagation. <code>traceparent</code> HTTP header."),
        GlossaryItem(name="Head / tail sampling", definition="Decide to trace at the entry vs after the request completes."),
        GlossaryItem(name="Tempo / Jaeger", definition="Tracing backends. Tempo is Grafana\'s; Jaeger is CNCF."),
        GlossaryItem(name="eBPF", definition="In-kernel programmable hooks. Used for observability, networking, security."),
        GlossaryItem(name="Hubble", definition="Cilium\'s per-flow network observability built on eBPF."),
        GlossaryItem(name="Pixie", definition="eBPF-based observability DaemonSet. Auto-instruments at the kernel."),
        GlossaryItem(name="SLI / SLO / SLA", definition="Indicator (what to measure) / Objective (target) / Agreement (with consequences)."),
        GlossaryItem(name="Error budget", definition="Complement of SLO. \"Allowable failure\" you can spend on risk."),
        GlossaryItem(name="Burn-rate alert", definition="Pages when error budget is being consumed too fast. Multi-window-multi-burn-rate pattern is standard."),
        GlossaryItem(name="Sloth / Pyrra", definition="SLO management tools. Generate Prometheus rules from SLO YAML."),
    ],
    recap_lead="Traces answer where time went across services; eBPF tools observe at the kernel without app changes; SLOs turn observability into reliability commitments. Burn-rate alerts page on actual risk, not raw thresholds.",
    recap_next="<strong>Next — Lesson 34: Autoscaling.</strong> HPA, VPA, KEDA, Cluster Autoscaler, Karpenter — how the cluster matches capacity to demand. New K-Town district: Power Station.",
)
