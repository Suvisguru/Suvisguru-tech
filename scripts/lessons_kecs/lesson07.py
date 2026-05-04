"""K-ECS C7 — Observability."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS observability — Container Insights, ECS Exec, FireLens, ADOT, X-Ray.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Lighthouse · K-Harbor — four signals, four observers</text>
  <rect x="40" y="70" width="170" height="120" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="125" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Container Insights</text>
  <text x="125" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">CPU / mem / net / I/O</text>
  <text x="125" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">preconfigured dashboards</text>
  <text x="125" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">cluster + service + task</text>
  <text x="125" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">enable per cluster</text>
  <rect x="225" y="70" width="170" height="120" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="310" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">ECS Exec</text>
  <text x="310" y="108" text-anchor="middle" font-size="9" fill="#1F2433">interactive shell</text>
  <text x="310" y="124" text-anchor="middle" font-size="9" fill="#1F2433">SSM-backed</text>
  <text x="310" y="144" text-anchor="middle" font-size="9" fill="#1F2433">no SSH; no inbound</text>
  <text x="310" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">audited via CloudTrail</text>
  <rect x="410" y="70" width="170" height="120" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="495" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">FireLens</text>
  <text x="495" y="108" text-anchor="middle" font-size="9" fill="#1F2433">Fluent Bit / Fluentd</text>
  <text x="495" y="124" text-anchor="middle" font-size="9" fill="#1F2433">logs → anywhere</text>
  <text x="495" y="144" text-anchor="middle" font-size="9" fill="#1F2433">CW / S3 / Kinesis / OS</text>
  <text x="495" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#1F2433">sidecar pattern</text>
  <rect x="595" y="70" width="125" height="120" rx="10" fill="#5E4A8E" stroke="#1F2433"/>
  <text x="657" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">ADOT + X-Ray</text>
  <text x="657" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">metrics + traces</text>
  <text x="657" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">OpenTelemetry</text>
  <text x="657" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">distributed tracing</text>
  <text x="657" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">collector sidecar</text>
</svg>"""


LESSON = LessonSpec(
    num="07",
    title_short="ECS observability",
    title_full="C7 · ECS Observability — Container Insights, ECS Exec, FireLens, ADOT, X-Ray",
    title_html="K-ECS C7 · ECS Observability",
    module_eyebrow="Module C7 · Lighthouse — four signals, four observers",
    hero_sub_html='<strong>CloudWatch Container Insights for ECS</strong>: preconfigured cluster + service + task metrics + dashboards. Enable per Cluster (account setting or per-cluster <em>containerInsights = enabled</em>). <strong>ECS Exec</strong>: interactive shell into a running Task via SSM (no SSH, no inbound port; CloudTrail-audited). <strong>FireLens</strong>: Fluent Bit / Fluentd sidecar for log routing — ship to CloudWatch / S3 / Kinesis / OpenSearch / Splunk / anywhere. <strong>ADOT (AWS Distro for OpenTelemetry)</strong>: metrics + traces collector; OTel-compatible; ships to CloudWatch, AMP, X-Ray. <strong>AWS X-Ray</strong>: distributed tracing; segment-and-subsegment model; integrates with ADOT.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A Service is silently failing every 5th request. CloudWatch logs are noisy. There\'s no tracing. The on-call engineer SSHes... <em>except there\'s no SSH on Fargate</em>. They restart the Service, hoping it clears. It doesn\'t. The bug is a downstream timeout that they can\'t see without traces. Today\'s lesson: wire ECS observability before you need it — Container Insights + ECS Exec + FireLens + ADOT/X-Ray.",
    stamp_html="<strong>Container Insights for cluster/service/task metrics. ECS Exec for live debug (no SSH). FireLens for log routing flexibility. ADOT + X-Ray for distributed tracing. Wire these before the incident, not during.</strong>",
    district_pin="kh-pier07",
    district_label="Lighthouse",
    sections=[
        Section(
            eyebrow="Section 1.1 · CloudWatch Container Insights",
            h2="Cluster + Service + Task metrics + dashboards",
            body_html="""    <p><strong>Container Insights</strong> auto-collects per-Cluster, per-Service, per-Task metrics: CPU + memory + network + storage I/O. Preconfigured CloudWatch dashboards aggregate per Cluster and Service. <em>Per-Task</em> metrics surface in CloudWatch Logs Insights via the <code>/aws/ecs/containerinsights/&lt;cluster&gt;/performance</code> log group.</p>
    <p><strong>Enabling</strong>: account setting <code>aws ecs put-account-setting --name containerInsights --value enabled</code> (default for new clusters thereafter), or per-cluster <code>aws ecs update-cluster-settings --cluster X --settings name=containerInsights,value=enabled</code>.</p>
    <p><strong>Cost note</strong>: Container Insights ingests metrics + Logs Insights performance log → metered as CloudWatch metrics + log ingest. For very-large fleets, the bill is real; budget accordingly. The trade-off (visibility vs cost) is usually overwhelmingly worth it but worth knowing.</p>
    <p><strong>Service-level dashboards</strong>: aggregate <code>CPUUtilization</code>, <code>MemoryUtilization</code>, <code>RunningTaskCount</code>, <code>DesiredTaskCount</code>, <code>PendingTaskCount</code>. The PendingTaskCount > 0 metric is gold for catching capacity starvation early — wire an alarm.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · ECS Exec",
            h2="Interactive shell via SSM, no SSH, CloudTrail-audited",
            body_html="""    <p><strong>ECS Exec</strong> opens a shell into a running container via the SSM Session Manager protocol. No inbound network port; no SSH key; no bastion. Use <code>aws ecs execute-command --cluster X --task ID --container Y --command "/bin/sh" --interactive</code>.</p>
    <p><strong>Prerequisites</strong>:</p>
    <ul>
      <li>Task Definition: <code>enableExecuteCommand: true</code> on the Service (or via RunTask).</li>
      <li>Task role policy: <code>ssmmessages:CreateControlChannel</code>, <code>ssmmessages:CreateDataChannel</code>, <code>ssmmessages:OpenControlChannel</code>, <code>ssmmessages:OpenDataChannel</code>.</li>
      <li>VPC connectivity: outbound to SSM Messages endpoint (or VPC endpoint <code>com.amazonaws.region.ssmmessages</code> for private-only VPCs).</li>
      <li>Container has <code>/bin/sh</code> or another shell.</li>
    </ul>
    <p><strong>Audit</strong>: every Exec session is logged to CloudTrail (<code>ecs:ExecuteCommand</code> + SSM <code>StartSession</code>). Optional CloudWatch Logs streaming of the session itself via the SSM logging configuration.</p>
    <p><strong>Why ECS Exec, not SSH?</strong> SSH requires open ports + key management + bastion + per-host config. ECS Exec needs none of that. Works identically on Fargate (where you can\'t SSH at all) and EC2.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · FireLens for log routing",
            h2="Fluent Bit / Fluentd sidecar; logs to anywhere",
            body_html="""    <p><strong>FireLens</strong> is a logConfiguration option (<code>logDriver: awsfirelens</code>) that routes container logs through a sidecar (Fluent Bit or Fluentd) which ships them anywhere. The sidecar runs in the same Task; consumes the app container\'s stdout/stderr; emits per its own routing config (Fluent Bit configmap or external file).</p>
    <p><strong>Why FireLens?</strong> The default <code>awslogs</code> driver only ships to CloudWatch. FireLens unlocks <em>any destination</em>: CloudWatch (multiple log groups), S3 (cheaper archive), Kinesis Data Firehose / Streams (downstream pipelines), OpenSearch, Splunk, Datadog, Elasticsearch, custom HTTP. Combine routes — same log to CloudWatch (live ops) + S3 (long-term archive) + OpenSearch (search).</p>
    <p><strong>Sidecar pattern</strong>: Task Definition has two containers — <em>app</em> (logConfiguration: awsfirelens) + <em>log_router</em> (Firelens-aware Fluent Bit image, essential: true). App stdout streams to the sidecar over Fluentd protocol; sidecar applies filters + routes per config.</p>
    <p><strong>Bottlerocket FireLens</strong> <span class="skip-tag">[ deep dive — skip if new ]</span>: on Bottlerocket-based EC2 hosts, a FireLens-as-host-daemon pattern is also possible — one log router per host, not per Task. Lower per-Task overhead at cost of less per-Task isolation.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · ADOT + X-Ray",
            h2="OpenTelemetry collector + distributed tracing",
            body_html="""    <p><strong>ADOT (AWS Distro for OpenTelemetry)</strong>: an AWS-supported distribution of the OTel collector. Ship as a sidecar in your Task Definition; receive metrics + traces from your app via OTLP; export to CloudWatch (metrics), AWS Managed Prometheus (AMP), X-Ray (traces), or any OTel-compatible backend.</p>
    <p><strong>AWS X-Ray</strong>: native distributed tracing service. Model: <em>segments</em> (top-level work unit, e.g., one HTTP request) + <em>subsegments</em> (downstream calls). SDKs for Java, Python, Node, Go, .NET, Ruby. ADOT exports OTel traces in X-Ray format.</p>
    <p><strong>Practical pattern</strong>:</p>
    <ul>
      <li>App instrumented with OTel SDK; emits OTLP to <code>localhost:4317</code> (gRPC) or <code>:4318</code> (HTTP).</li>
      <li>ADOT sidecar receives OTLP; exports traces → X-Ray; metrics → CloudWatch + AMP.</li>
      <li>ADOT task role allows <code>xray:PutTraceSegments</code>, CloudWatch <code>cloudwatch:PutMetricData</code>, AMP RemoteWrite if used.</li>
    </ul>
    <p><strong>Service Connect bonus</strong>: if you\'re using Service Connect, the proxy already emits per-service metrics (rps, latency, 5xx) into Container Insights — adds layer-7 observability without instrumenting the app. Pair with ADOT for app-level traces and you have a complete picture.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="A Cluster doesn\'t show CPU/memory dashboards in CloudWatch. What\'s the most likely cause?",
            options=[
                ("Tasks aren\'t emitting metrics — add an ADOT sidecar.", False),
                ("Container Insights isn\'t enabled on the Cluster.", True),
                ("FireLens needs to be configured first.", False),
            ],
            feedback="Container Insights is opt-in per Cluster (or via account-default setting). Once enabled, dashboards populate within minutes; no app changes needed.",
        ),
        3: PauseCheck(
            question="An app is instrumented with OTel SDK and exporting traces to localhost:4317. What does the Task need?",
            options=[
                ("FireLens sidecar to handle traces.", False),
                ("ADOT sidecar that receives OTLP and exports to X-Ray.", True),
                ("Direct HTTP calls from app to X-Ray.", False),
            ],
            feedback="ADOT is the OTel collector; it bridges OTLP-to-X-Ray (and OTel metrics to CloudWatch / AMP). FireLens routes logs, not traces.",
        ),
    },
    before_after_before='<p>Pre-Container-Insights, ECS observability meant manually wiring CloudWatch alarms on individual ECS metrics + writing custom log shippers + SSHing to EC2 hosts to debug Tasks (or rebooting Tasks blindly on Fargate). Pre-ECS-Exec, Fargate Tasks were opaque — no shell access. Pre-FireLens, all logs went to CloudWatch via the awslogs driver — no S3 archive, no OpenSearch search, no Splunk integration without separate agents on each host.</p>',
    before_after_after='<p>Modern ECS observability is four well-defined layers: <strong>Container Insights</strong> (metrics + dashboards), <strong>ECS Exec</strong> (live debug shell, no SSH), <strong>FireLens</strong> (log routing flexibility), <strong>ADOT + X-Ray</strong> (metrics + traces). All wireable in Task Definitions or per-Cluster config. Audit-friendly (CloudTrail logs every Exec session). Works identically on Fargate and EC2.</p>',
    before_after_caption='<p class="ba-caption"><em>Wire all four before the incident. The marginal cost is small; the marginal value when something breaks is enormous.</em></p>',
    analogy_intro_html='''<p>The harbor\'s <strong>Lighthouse</strong> is the highest point. Four observers work shifts there.</p>
    <p>The <strong>weather observer</strong> (Container Insights) keeps charts of every pier and ship — wind speed (CPU), tide level (memory), traffic count (network), warehouse activity (storage I/O). Daily dashboards show patterns across the whole harbor. When the pending-ship count starts climbing, an alarm fires before the harbor master notices.</p>
    <p>The <strong>boarding inspector</strong> (ECS Exec) can step onto any active ship and inspect it directly. No need to dock first; no boarding plank or ladder; the lighthouse keeper opens an authenticated channel to the ship\'s hold via the harbor\'s control system. Every visit is logged in the harbor\'s audit book.</p>
    <p>The <strong>signal officer</strong> (FireLens) reads every ship\'s logbook entries and routes them — the harbor\'s archive (CloudWatch), the long-term storage shed (S3), the foreign embassy office (OpenSearch / Splunk / Datadog), or the data pipeline (Kinesis). Same logbook entry can go to all four if needed.</p>
    <p>The <strong>navigator</strong> (ADOT + X-Ray) follows individual cargo journeys end-to-end — when a customer\'s shipment crosses three ships at three piers, the navigator pieces together the whole route and shows you where each leg took how long. Distributed traces.</p>''',
    translation_rows=[
        ("Lighthouse top", "ECS observability layer"),
        ("Weather observer", "Container Insights — cluster/service/task metrics + dashboards"),
        ("Boarding inspector", "ECS Exec — interactive shell via SSM"),
        ("Inspector\'s logged visits", "CloudTrail audit of ecs:ExecuteCommand + SSM StartSession"),
        ("Signal officer", "FireLens — Fluent Bit / Fluentd sidecar"),
        ("Foreign embassy office", "OpenSearch / Splunk / Datadog destinations"),
        ("Long-term storage shed", "S3 log archive"),
        ("Navigator", "ADOT + X-Ray distributed tracing"),
        ("End-to-end cargo journey", "trace = segments + subsegments"),
        ("Per-language journey log", "OTel SDKs (Java / Python / Node / Go / .NET / Ruby)"),
    ],
    analogy_stops="A real lighthouse uses light + sound; ECS observability is API calls + log streams. The four layers map cleanly to the analogy but the costs (storage, ingest, indexing) are very different from a physical harbor\'s observation cost.",
    eli5="Up at the lighthouse, four people watch the harbor. One reads the weather and writes daily reports. One can teleport onto any ship to look around. One reads everyone\'s logbooks and copies them to the right places. One follows individual packages from ship to ship to see how long each leg took. Together they show what\'s happening in the whole harbor.",
    eli10="<strong>Container Insights</strong>: per-Cluster opt-in; preconfigured CPU/memory/network/I/O metrics + dashboards. <strong>ECS Exec</strong>: <code>execute-command</code> via SSM; needs <code>enableExecuteCommand</code> on Service + ssmmessages perms in task role; CloudTrail-audited. <strong>FireLens</strong>: <code>logDriver: awsfirelens</code> + sidecar Fluent Bit/Fluentd; routes to anywhere. <strong>ADOT + X-Ray</strong>: OTel collector sidecar; receives OTLP from app; exports to X-Ray (traces) + CloudWatch / AMP (metrics).",
    scenarios=[
        Scenario(
            name="Production wire-up — all four enabled by default",
            body="A 100-engineer org has a Service Catalog template that every new ECS Service uses. Template includes: Container Insights enabled at Cluster level, Task role with ssmmessages perms (ECS Exec), FireLens sidecar routing logs to CloudWatch + S3 + OpenSearch, ADOT sidecar exporting OTel metrics to CloudWatch + traces to X-Ray. <em>Every new Service has full observability on day 1.</em>",
        ),
        Scenario(
            name="3 AM debug — ECS Exec saved the night",
            body="On-call engineer pages on a Fargate Service with intermittent 5xx. SSH not available; she runs <code>aws ecs execute-command --interactive --command \"/bin/sh\"</code> into a single Task; runs <code>netstat</code> + <code>nslookup</code> + reads in-memory state. Finds a stale DNS cache from a downstream service rotation. Restarts the Task; problem clears. Long-term fix: shorter DNS TTL. <em>Without ECS Exec, this would have been hours of trial-and-error restarts.</em>",
        ),
        Scenario(
            name="Compliance — every log to S3 archive + CloudWatch live",
            body="A regulated workload requires 7-year log retention. FireLens config routes <em>all</em> container logs to <strong>two</strong> destinations: CloudWatch (14-day live retention for ops) + S3 (Glacier-archive after 30 days for the 7-year requirement). Same log entry; two destinations. CloudWatch costs stay bounded; S3 archive cost is pennies/GB-year.",
        ),
        Scenario(
            name="Outage — no traces meant no answer",
            body="A team had Container Insights + FireLens but no ADOT/X-Ray. A Service had P95 latency tail 3× normal but only on one specific endpoint. CloudWatch metrics showed the spike; logs showed nothing useful (the slow path didn\'t crash). Without distributed traces, root cause stayed hidden for 2 days until a new engineer reproduced the call manually and found the slow downstream. <em>Postmortem</em>: ADOT + X-Ray on every Service.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Container Insights is on by default for new Clusters.\"",
            truth="<strong>Off by default unless</strong> the account-level setting <code>containerInsights = enabled</code> is set first (then new Clusters inherit it). Existing Clusters need explicit per-cluster enable. Audit your Clusters; you\'ll likely find some without it.",
        ),
        Misconception(
            myth="\"ECS Exec is just SSH for ECS.\"",
            truth="ECS Exec uses <strong>SSM Session Manager</strong> — no inbound network, no SSH keys, no bastion. The auth path is IAM (your principal needs <code>ecs:ExecuteCommand</code>); the Task needs SSM Messages perms in its task role. Different machinery; auditable via CloudTrail; works on Fargate where SSH doesn\'t exist.",
        ),
        Misconception(
            myth="\"FireLens replaces awslogs everywhere.\"",
            truth="FireLens is more flexible but adds a sidecar Task overhead (Fluent Bit container ~30MB memory). For simple workloads where CloudWatch is the only log destination, plain <code>awslogs</code> driver is fine — less ops surface. Pick FireLens when you need multi-destination routing or filtering.",
        ),
    ],
    flashcards=[
        Flashcard(front="What does Container Insights for ECS provide?", back="Preconfigured cluster + service + task metrics (CPU / memory / network / I/O) + dashboards in CloudWatch. Per-Task perf in <code>/aws/ecs/containerinsights/&lt;cluster&gt;/performance</code> log group."),
        Flashcard(front="Three things needed to use ECS Exec?", back="(1) <code>enableExecuteCommand: true</code> on Service, (2) Task role with <code>ssmmessages</code> perms, (3) VPC outbound to SSM Messages endpoint (or VPC endpoint for private). Container needs a shell."),
        Flashcard(front="ECS Exec audit trail?", back="CloudTrail logs <code>ecs:ExecuteCommand</code> and the underlying SSM <code>StartSession</code>. Optional CloudWatch Logs streaming of session content via SSM logging config."),
        Flashcard(front="What does FireLens route?", back="Container logs (stdout + stderr) through a sidecar Fluent Bit / Fluentd to any destination — CloudWatch, S3, Kinesis, OpenSearch, Splunk, Datadog, custom HTTP. Multi-destination routing in one sidecar."),
        Flashcard(front="ADOT vs X-Ray — what\'s the relationship?", back="<strong>ADOT</strong> = AWS Distro for OpenTelemetry — collector that receives OTLP from apps + exports to multiple backends. <strong>X-Ray</strong> = AWS\'s distributed tracing service. ADOT exports OTel traces in X-Ray format."),
        Flashcard(front="Where does an OTel-instrumented app emit traces?", back="To <code>localhost:4317</code> (gRPC) or <code>localhost:4318</code> (HTTP) on the same Task — picked up by an ADOT sidecar in the same Task that exports onward."),
        Flashcard(front="Service Connect observability bonus?", back="The Service Connect Envoy proxy emits per-service rps + latency + 5xx automatically — into Container Insights without app instrumentation. Layer-7 observability for free; pair with ADOT for app-internal traces."),
        Flashcard(front="When NOT use FireLens?", back="When CloudWatch is the only log destination + you don\'t need filtering — plain <code>awslogs</code> driver is simpler, no sidecar overhead. The trade gets favorable for FireLens when multi-destination or filtering matters."),
    ],
    quizzes=[
        Quiz(
            prompt="A Service\'s Tasks crash within 5 seconds of startup with no logs. ECS Exec into a Task during the brief startup window? Or another approach?",
            answer="ECS Exec needs the Task to reach RUNNING + healthy enough for the SSM agent path to be established — usually too slow if the container crashes in 5 seconds. Better approach: (1) Add a <strong>sleep + tail at the entrypoint</strong> for one debug Task — <code>command: [\"/bin/sh\", \"-c\", \"sleep 600\"]</code> — Exec in once it\'s up, run the real binary by hand, watch it fail. (2) Or use <strong>Run Task</strong> (one-off) with the suspect Task Definition + sleep override; debug at leisure. (3) Read <strong>stoppedReason + container exit code</strong> from <code>describe-tasks</code> — often names the cause (Essential container exited; OutOfMemoryError; CannotPullContainerError). (4) Make sure logConfiguration captures <em>everything</em> — stderr, not just stdout — so any startup error has a chance of being recorded.",
        ),
        Quiz(
            prompt="A team has Container Insights enabled but not ADOT/X-Ray. They\'re seeing P99 latency drift up over weeks with no obvious metric tipping. What\'s the next investment?",
            answer="<strong>Distributed tracing via ADOT + X-Ray.</strong> Container Insights gives per-Service and per-Task aggregates; it can\'t answer \"which downstream call is the slow one?\" or \"which user request paths take longest?\" Add OTel SDK to the app; deploy ADOT sidecar; export traces to X-Ray. Within hours, X-Ray service map shows: which downstream services are in the path, where time is spent, which paths have anomalous tails. Slow drift over weeks usually traces to a downstream that\'s gradually slowing (DB index degraded, cache hit rate dropping). Distributed tracing makes that visible in one chart.",
        ),
        Quiz(
            prompt="The CFO sees a $1,200/month CloudWatch bill from Container Insights + FireLens-to-CloudWatch on a 200-Task cluster. \"Cut it in half.\" Defend the value or propose tradeoffs.",
            answer="\"<strong>Container Insights and CloudWatch logging are the things we\'d miss most in an outage.</strong> $1,200/month works out to ~$6 per Task per month. Two ways to trim without losing the value: (1) <strong>Reduce CloudWatch log retention</strong> from default to 14 days (compliance work-around: keep S3 archive via FireLens for the long retention; CloudWatch is just live operational). Cuts ingestion of old logs from re-indexing during search. (2) <strong>Filter at FireLens</strong> — drop DEBUG logs from CloudWatch (route them to S3 only); keep INFO/WARN/ERROR in CloudWatch. Often 60-80% of log volume is DEBUG. <strong>Combined: usually halves the bill while preserving every signal we actually use during incidents.</strong> Cutting Container Insights itself would save more, but next outage we\'d be debugging blind.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CFO",
        ),
    ],
    glossary=[
        GlossaryItem(name="Container Insights for ECS", definition="Preconfigured CloudWatch dashboards + metrics for cluster + service + task. Per-Cluster enable."),
        GlossaryItem(name="ECS Exec", definition="Interactive shell into a running Task via SSM; no SSH; CloudTrail-audited."),
        GlossaryItem(name="enableExecuteCommand", definition="Service property enabling ECS Exec on Tasks within the Service."),
        GlossaryItem(name="FireLens", definition="logDriver awsfirelens routing logs through a Fluent Bit / Fluentd sidecar to any destination."),
        GlossaryItem(name="Fluent Bit", definition="Lightweight log shipper used as the FireLens sidecar default. C-based, low memory footprint."),
        GlossaryItem(name="ADOT", definition="AWS Distro for OpenTelemetry — supported OTel collector for ECS / EKS / Lambda."),
        GlossaryItem(name="OTLP", definition="OpenTelemetry Protocol — gRPC (4317) or HTTP (4318); how apps emit OTel signals to a collector."),
        GlossaryItem(name="X-Ray", definition="AWS distributed tracing service; segments + subsegments model; ADOT exports traces in X-Ray format."),
        GlossaryItem(name="CloudWatch performance log group", definition="<code>/aws/ecs/containerinsights/&lt;cluster&gt;/performance</code> — Container Insights per-Task data plane."),
        GlossaryItem(name="ssmmessages permissions", definition="IAM actions ECS Exec needs in the task role: CreateControlChannel, CreateDataChannel, OpenControlChannel, OpenDataChannel."),
    ],
    recap_lead="Four observability layers — Container Insights, ECS Exec, FireLens, ADOT + X-Ray. Wire them before incidents. Container Insights for at-a-glance health. ECS Exec for live debug. FireLens for log destination flexibility. ADOT + X-Ray for distributed tracing.",
    recap_next='<strong>Next — C8: ECS Anywhere and Hybrid.</strong> ECS control plane managing on-prem / edge servers; SSM agent + ECS agent registration; networking + storage limits on external instances; use cases (regulated, edge processing, gradual cloud migration).',
    architecture_svg='''<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ECS observability: Container Insights, ECS Exec, FireLens, ADOT, X-Ray.">
  <rect x="10" y="10" width="740" height="220" rx="12" fill="#FBF7F0" stroke="#3F4A5E"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">ECS OBSERVABILITY · METRICS · LOGS · TRACES · LIVE DEBUG</text>
  <rect x="20" y="50" width="170" height="60" rx="6" fill="#5DCAA5"/>
  <text x="105" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">ECS Task</text>
  <text x="105" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">app + sidecars</text>
  <text x="105" y="100" text-anchor="middle" font-size="8" fill="#1F2433">stdout · /metrics · OTel</text>
  <line x1="190" y1="80" x2="220" y2="80" stroke="#5A4F45" stroke-width="2" marker-end="url(#aC7)"/>
  <defs><marker id="aC7" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><polygon points="0 0, 10 5, 0 10" fill="#5A4F45"/></marker></defs>
  <rect x="220" y="50" width="170" height="60" rx="6" fill="#FF9900"/>
  <text x="305" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">FireLens sidecar</text>
  <text x="305" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">Fluent Bit / Fluentd</text>
  <text x="305" y="100" text-anchor="middle" font-size="8" fill="#1F2433">routes anywhere</text>
  <line x1="390" y1="80" x2="420" y2="80" stroke="#5A4F45" stroke-width="2" marker-end="url(#aC7)"/>
  <rect x="420" y="50" width="320" height="60" rx="6" fill="#3F4A5E"/>
  <text x="580" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">CloudWatch · S3 · Kinesis · OpenSearch · Splunk · Datadog</text>
  <text x="580" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">multi-destination logs</text>
  <text x="580" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">CloudWatch live · S3 archive</text>
  <rect x="20" y="125" width="170" height="55" rx="6" fill="#A04832"/>
  <text x="105" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Container Insights</text>
  <text x="105" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">CPU / mem / net / I/O</text>
  <text x="105" y="174" text-anchor="middle" font-size="8" fill="#FBE8DC">cluster + service + task</text>
  <rect x="200" y="125" width="170" height="55" rx="6" fill="#5E4A8E"/>
  <text x="285" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">ECS Exec</text>
  <text x="285" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">SSM-backed shell</text>
  <text x="285" y="174" text-anchor="middle" font-size="8" fill="#FBE8DC">no SSH; CloudTrail-audited</text>
  <rect x="380" y="125" width="170" height="55" rx="6" fill="#5A6B81"/>
  <text x="465" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">ADOT collector</text>
  <text x="465" y="161" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">OpenTelemetry</text>
  <text x="465" y="174" text-anchor="middle" font-size="8" fill="#FBE8DC">metrics + traces</text>
  <rect x="560" y="125" width="180" height="55" rx="6" fill="#FAC775"/>
  <text x="650" y="145" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">AWS X-Ray</text>
  <text x="650" y="161" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">distributed tracing</text>
  <text x="650" y="174" text-anchor="middle" font-size="8" fill="#5A4F45">segments + subsegments</text>
  <rect x="20" y="195" width="720" height="30" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="215" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">Wire all four before incidents · Service Connect emits per-service rps + latency + 5xx automatically</text>
</svg>''',
    architecture_caption='Four ECS observability layers: Container Insights for cluster/service/task metrics; ECS Exec for live debug shell (SSM-backed; no SSH); FireLens routes logs anywhere; ADOT + X-Ray for OTel metrics + traces. Wire all four before incidents.',
)
