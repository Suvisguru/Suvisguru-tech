from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Detective's Office: a corkboard with a triage flowchart, evidence kit (kubectl describe, get events, logs, top), and a series of suspects (Pod, Node, CNI, Storage, RBAC, Admission).">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">DETECTIVE\'S OFFICE · TROUBLESHOOTING METHODOLOGY</text>
  <g transform="translate(40,55)"><rect width="200" height="140" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/><text x="100" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">TRIAGE FLOW</text>
    <rect x="14" y="32" width="172" height="22" rx="2" fill="#FBE8DC"/><text x="20" y="46" font-size="8" fill="#A04832" font-weight="700">1. Reproduce</text>
    <rect x="14" y="58" width="172" height="22" rx="2" fill="#FBF1D6"/><text x="20" y="72" font-size="8" fill="#8B5A00" font-weight="700">2. Observe + measure</text>
    <rect x="14" y="84" width="172" height="22" rx="2" fill="#E0EEF3"/><text x="20" y="98" font-size="8" fill="#3F4A5E" font-weight="700">3. Hypothesise</text>
    <rect x="14" y="110" width="172" height="22" rx="2" fill="#E0EFE6"/><text x="20" y="124" font-size="8" fill="#3D7857" font-weight="700">4. Test + verify</text></g>
  <g transform="translate(260,55)"><rect width="180" height="140" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/><text x="90" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">EVIDENCE KIT</text>
    <rect x="14" y="32" width="152" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="46" font-size="8" fill="#5A4F45" font-weight="700">describe + get events</text>
    <rect x="14" y="56" width="152" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="70" font-size="8" fill="#5A4F45" font-weight="700">logs --previous</text>
    <rect x="14" y="80" width="152" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="94" font-size="8" fill="#5A4F45" font-weight="700">top + cAdvisor</text>
    <rect x="14" y="104" width="152" height="20" rx="2" fill="#FBF1D6"/><text x="20" y="118" font-size="8" fill="#5A4F45" font-weight="700">debug ephemeral cont</text></g>
  <g transform="translate(460,55)"><rect width="180" height="140" rx="6" fill="#FBE8DC" stroke="#A04832" stroke-width="1.5"/><text x="90" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">USUAL SUSPECTS</text>
    <text x="20" y="40" font-size="8" fill="#5A4F45">• Image pull / signing</text>
    <text x="20" y="55" font-size="8" fill="#5A4F45">• Resource limits / OOM</text>
    <text x="20" y="70" font-size="8" fill="#5A4F45">• PVC / storage class</text>
    <text x="20" y="85" font-size="8" fill="#5A4F45">• NetworkPolicy / ANP</text>
    <text x="20" y="100" font-size="8" fill="#5A4F45">• PSA / admission</text>
    <text x="20" y="115" font-size="8" fill="#5A4F45">• MTU / DNS / certs</text>
    <text x="20" y="130" font-size="8" fill="#5A4F45">• Affinity / taints</text></g>
</svg>"""

LESSON = LessonSpec(
    num="44",
    title_short="troubleshooting",
    title_full="Troubleshooting Methodology + Drills (Capstone)",
    title_html="Lesson 44 — Troubleshooting Methodology · K-COM",
    module_eyebrow="Module 19 · Lesson 44 · the capstone — investigating under pressure",
    hero_sub_html='You\'ve learned every K8s primitive in 43 lessons. Now: <strong>how to debug when the system fails</strong>. Methodical investigation beats panic; structured triage beats wild guessing. This capstone covers the <strong>methodology</strong>, the <strong>evidence-gathering toolkit</strong>, and a tour of the <strong>most common failure patterns</strong> across the topics you\'ve studied.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='3 AM. Production is degraded. You\'re paged. Logs are noisy; metrics are spiking; everyone\'s in the war room asking \"what changed?\" The temptation is to start <code>kubectl edit</code>ing things. The discipline is the <strong>triage flow</strong>: reproduce, observe, hypothesise, test, verify. The detective\'s office runs by methodology, not vibes. After 43 lessons of how K8s works, this lesson is how to fix it when it doesn\'t.',
    stamp_html='Four-step triage: <strong>(1) Reproduce</strong> the issue. <strong>(2) Observe + measure</strong> with logs / events / metrics / traces. <strong>(3) Hypothesise</strong> a cause. <strong>(4) Test + verify</strong> the fix. The K8s evidence kit: <code>kubectl describe</code> (events!), <code>kubectl get events</code>, <code>kubectl logs --previous</code>, <code>kubectl debug</code>, <code>kubectl top</code>, the observability stack from L32-L33. Common failure patterns cluster around: image pulls, resource limits, storage, networking, admission policy, certificates.',
    district_pin="kt-pin44",
    district_label="Detective\'s Office — Investigation HQ",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Methodology before tooling",
            body_html="""    <p>The fundamental troubleshooting flow:</p>
    <ol>
      <li><strong>Reproduce.</strong> Can you trigger the issue at will? If yes, debugging is bounded. If no, you\'re in \"flaky\" territory — gather more telemetry, wait for next occurrence.</li>
      <li><strong>Observe + measure.</strong> Don\'t guess. Use <code>kubectl describe</code>, <code>get events</code>, logs, metrics, traces. Note timestamps. Look for patterns: which Pods, which times, which traffic, which dependencies.</li>
      <li><strong>Hypothesise.</strong> Form a specific theory. \"The ConfigMap content changed at 14:32; that\'s when error rate jumped.\" Hypotheses are testable.</li>
      <li><strong>Test + verify.</strong> Make a change. See if the issue resolves. If yes, you\'ve confirmed the cause. If no, hypothesis is wrong; back to step 2.</li>
    </ol>
    <p>The most common anti-pattern: skipping straight from \"problem reported\" to \"let me try a fix.\" This is debugging by random walk — sometimes you stumble onto the answer; usually you make things worse. Discipline beats brilliance under pressure.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The K8s evidence kit",
            h2="What kubectl gives you for free",
            body_html="""    <ul>
      <li><strong><code>kubectl describe pod &lt;pod&gt;</code></strong> — the most useful command. Shows events at the bottom: image pull errors, scheduling failures, probe failures, OOM kills. Almost every \"why won\'t my Pod start\" question is answered here.</li>
      <li><strong><code>kubectl get events --sort-by=.metadata.creationTimestamp</code></strong> — namespace-wide events. Catches things <code>describe</code> on one Pod misses.</li>
      <li><strong><code>kubectl logs &lt;pod&gt; --previous</code></strong> — logs from the previous container instance. Crucial after a crash; the current logs are post-restart and tell you nothing.</li>
      <li><strong><code>kubectl top pod / node</code></strong> — current CPU / memory. Pair with metrics-server.</li>
      <li><strong><code>kubectl debug</code></strong> — modern way to add an ephemeral debug container into an existing Pod or copy a Pod with a different image (e.g., debug a distroless container by adding a <code>busybox</code> ephemeral container).</li>
      <li><strong><code>kubectl auth can-i --as=&lt;sa&gt; &lt;verb&gt; &lt;resource&gt;</code></strong> — RBAC inspection. \"Can this SA do X?\" answered without trial and error.</li>
      <li><strong><code>kubectl explain &lt;resource&gt;.&lt;field&gt;</code></strong> — field-level documentation from the running cluster\'s API. Always reflects the cluster version, not the docs.</li>
    </ul>
    <p>Beyond kubectl: the observability stack (L32-L33) — Prometheus / Grafana for metrics, Loki / Elastic for logs, Tempo / Jaeger for traces. Hubble + Pixie for network and kernel-level signals. The right tool depends on which layer you\'re investigating.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · The usual suspects (a tour)",
            h2="Common failure patterns from L1-L43",
            body_html="""    <p>A quick tour of the failure patterns you\'ve learned about across the curriculum:</p>
    <ul>
      <li><strong>Image pull failures</strong> — <code>ImagePullBackOff</code>. Causes: typo in image name, missing imagePullSecret, registry unreachable, signed-image policy rejecting unsigned images. <em>Lesson 11 + 30.</em></li>
      <li><strong>Resource starvation</strong> — Pods OOMKilled, evicted. Causes: missing requests/limits, ResourceQuota exceeded, LimitRange violation. <em>Lesson 31 + 22.</em></li>
      <li><strong>Storage</strong> — PVC stuck Pending, Pod can\'t mount. Causes: zone mismatch (Immediate binding mode vs multi-zone scheduler), CSI driver missing capability, storage class typo. <em>Lessons 18-19.</em></li>
      <li><strong>Networking</strong> — Service unreachable, cross-zone slow. Causes: NetworkPolicy denying, kube-proxy stale, CNI MTU mismatch, DNS resolver pointing wrong. <em>Lessons 17 + 24-26.</em></li>
      <li><strong>Admission rejection</strong> — apply fails with a policy error. Causes: PSA mismatch, ValidatingAdmissionPolicy violation, Kyverno rule. <em>Lessons 27-29.</em></li>
      <li><strong>Certificates</strong> — TLS errors, mTLS handshake failure. Causes: cert expired (cert-manager not renewing), wrong CA, time skew. <em>Lessons 21 + 43.</em></li>
      <li><strong>Scheduling</strong> — Pod stays Pending. Causes: no node fits, taints not tolerated, affinity unsatisfiable, topology spread blocked. <em>Lessons 22-23.</em></li>
      <li><strong>Operator / controller errors</strong> — CR stays in OutOfSync / Pending. Causes: missing RBAC, finalizer stuck, conversion webhook down, dependency CRD not yet applied. <em>Lessons 38-42.</em></li>
    </ul>
    <p>For each pattern, the diagnostic is similar: read the events, check the most recent change, follow the dependency chain, narrow to the failing component. <em>Most production incidents are not novel — they\'re known patterns hitting your specific cluster.</em>""",
        ),
        Section(
            eyebrow="Section 1.9 · Drills, runbooks, post-mortems",
            h2="The discipline that produces calm engineers",
            body_html="""    <p>Three practices distinguish teams that survive incidents:</p>
    <ul>
      <li><strong>Game days.</strong> Quarterly chaos engineering: kill a zone, kill 50% of Pods, simulate a CSI driver hang. The team practises the response. Tools: Chaos Mesh, LitmusChaos. <em>Lesson 35.</em></li>
      <li><strong>Runbooks per alert.</strong> Every paging alert has an annotation linking to a markdown runbook: \"if this fires, run these queries, look for these patterns, escalate at this signal.\" Runbooks evolve from post-mortems. <em>Lesson 32.</em></li>
      <li><strong>Blameless post-mortems.</strong> After every incident: timeline, contributing factors, what worked, what didn\'t, action items. No individual blame; system-level fixes. The discipline is reading them as a team.</li>
    </ul>
    <p>The single biggest determinant of MTTR isn\'t individual skill — it\'s organisational practice. Teams that drill, write runbooks, and learn from incidents have low MTTR. Teams that don\'t, don\'t.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The hardest lesson is restraint. When something\'s broken at 3 AM, the temptation is to fix it now. The right move is often: <strong>narrow the impact, gather evidence, get the right person on the call, then fix</strong>. Random changes during incidents create new problems and erase evidence. Best practice: capture state (<code>kubectl get all -A -o yaml</code>, descriptions, logs) before any mutation. You can\'t debug what you can\'t reproduce.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A Pod shows <code>ImagePullBackOff</code>. <code>kubectl describe pod</code> shows the event \"failed to pull image: not authorized.\" What\'s the next step?",
            options=[
                ("a) Restart the kubelet on every node", False),
                ("b) Check the namespace\'s imagePullSecrets configuration; verify the credentials are present and valid; verify the SA has the secret attached", True),
                ("c) Re-tag the image and try again", False),
            ],
            feedback="<strong>Answer: b.</strong> The error is specific. Read it; act on the actual cause. <code>kubectl get secret -n &lt;ns&gt;</code> + <code>kubectl get sa &lt;sa&gt; -o yaml</code> reveals whether the imagePullSecret is correctly configured. Then verify the registry credentials work via a manual <code>docker pull</code> on a node, if needed.",
        ),
    },
    before_after_before='<p>Before discipline: 3 AM page. Engineer panic-edits resources hoping to fix. Sometimes works; usually makes things worse. No clear timeline. Post-mortem becomes \"who did what when?\" finger-pointing. Same incidents recur monthly because nobody learned.</p>',
    before_after_after='<p>After discipline: 3 AM page. Engineer follows the runbook. Captures state. Walks the triage. Identifies cause within minutes. Fixes precisely. Post-mortem is structured + blameless. Same incident never recurs — the runbook + alert tuning + system fix prevent it.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">After 43 lessons of how K8s works, this lesson is the most important: how to think when it doesn\'t.</p>',
    analogy_intro_html='<p>The Detective\'s Office is the last district on the K-Town map — the one that handles every other district\'s problems. Every wall has a corkboard with a flowchart: <em>reproduce → observe → hypothesise → test → verify</em>. Detectives carry an evidence kit (kubectl, observability tools, fingerprint reagents) and a list of usual suspects (image pulls, RBAC, MTU, certs, admission). They don\'t panic. They don\'t guess. They follow the procedure, document their findings, write up the case for the next detective. After every case: a debriefing where everyone learns. The Office\'s reputation isn\'t built on solving novel mysteries — it\'s built on solving routine ones <em>fast</em>, calmly, with evidence.</p>',
    translation_rows=[
        ("The corkboard flowchart", "Triage methodology"),
        ("Evidence kit", "<code>kubectl describe</code>, events, logs, top, debug"),
        ("Usual suspects", "Common failure patterns (image, resource, storage, network, admission, cert)"),
        ("Detective\'s drill", "Chaos engineering / game day"),
        ("Case file template", "Runbook"),
        ("Post-case debrief", "Blameless post-mortem"),
        ("\"Don\'t touch the crime scene\"", "Capture state before mutating during an incident"),
        ("\"Look for the pattern, not just this case\"", "Pattern-recognising recurring failure modes"),
    ],
    analogy_stops="The analogy stops here: real K8s incidents don\'t involve fingerprints — they involve correlated logs across distributed systems, with timestamps that may or may not be synced. The detective abstraction undersells the digital nature of the work.",
    eli5='When something\'s broken, don\'t panic. Look at the clues (events, logs). Guess what might be wrong. Test the guess. If it\'s right, fix it. If not, look more carefully.',
    eli10="Troubleshooting K8s is methodology before tooling. Four steps: reproduce, observe + measure, hypothesise, test + verify. The kubectl evidence kit (describe, events, logs --previous, top, debug, auth can-i) handles 80% of cases. Common failure patterns recur: image pulls, resource limits, storage zone mismatch, NetworkPolicy denial, admission rejection, expired certs. Run game days quarterly; pair every alert with a runbook; do blameless post-mortems. The discipline beats individual brilliance.",
    scenarios=[
        Scenario(name="A SaaS that drilled the right things", body="Quarterly game days for 18 months. Each game day produced 3-4 runbook updates + 1-2 system improvements (alert tuning, redundancy, SLO refinement). MTTR for production incidents dropped from 90 minutes (year 1) to 12 minutes (year 2). The drill discipline did it."),
        Scenario(name="A bank with comprehensive runbook coverage", body="Every alert has a runbook. Every runbook has been validated by an on-call engineer in the last quarter. Engineers rotate through on-call; new engineers ramp up by reading the runbook library. Net effect: anyone in the team can handle 90% of alerts in their first month."),
        Scenario(name="A startup that learned mid-incident triage", body="Their first major incident: 4 hours of chaotic firefighting. Their second (a year later, after instituting drills + runbooks): 15 minutes from page to mitigation. Same kind of issue. The difference was process, not knowledge."),
        Scenario(name="A team that captured state pre-mutation", body="Convention: any incident response action that would change state is preceded by <code>kubectl get all -A -o yaml &gt; incident-pre.yaml</code>. After the incident, post-mortem can compare pre/post. Caught a self-inflicted mistake (wrong namespace edit) within minutes. Saved hours of confusion."),
    ],
    misconceptions=[
        Misconception(myth="Senior engineers don\'t need runbooks.", truth="Senior engineers <em>write</em> the runbooks so junior engineers can act with confidence. Senior engineers also forget specifics under stress; runbooks are insurance for everyone."),
        Misconception(myth="Faster fixes are better.", truth="Faster <em>verified</em> fixes are better. A fast wrong fix creates a second incident on top of the first. Slow down to read events; the speed-up comes from acting on real evidence."),
        Misconception(myth="The most critical kubectl command is <code>kubectl edit</code>.", truth="The most critical command is <code>kubectl describe</code>. Read events first, edit later — and prefer applying YAML changes via PR after the incident, not <code>kubectl edit</code> live."),
    ],
    flashcards=[
        Flashcard(front="Four-step triage flow?", back="Reproduce, Observe + measure, Hypothesise, Test + verify. The discipline that beats panic."),
        Flashcard(front="kubectl describe vs get?", back="<code>describe</code> shows the resource\'s status + events at the bottom. <code>get</code> shows just the spec/status. <code>describe</code> is the diagnostic; <code>get</code> is the inspection."),
        Flashcard(front="kubectl logs --previous?", back="Logs from the <em>previous</em> container instance (post-crash). Critical: current logs are post-restart and don\'t include the crash."),
        Flashcard(front="kubectl debug ephemeral container?", back="<code>kubectl debug -it pod-x --image=busybox --target=container-y</code>. Adds a debug container into a running Pod sharing namespaces. Useful for distroless containers without shells."),
        Flashcard(front="The 8 usual suspects?", back="Image pulls, Resource limits, Storage (zone/CSI/SC), Networking (NP/MTU/DNS), Admission (PSA/policy), Certificates, Scheduling (taints/affinity), Operator/controller (RBAC/finalizers/webhook)."),
        Flashcard(front="What is a game day?", back="Scheduled chaos engineering exercise. Inject failure (kill a zone, kill Pods, slow a dependency) and have the team practise response. Quarterly cadence; produces runbook + system improvements."),
        Flashcard(front="Why blameless post-mortems?", back="Individual blame discourages reporting; system-level fixes prevent recurrence. Focus on contributing factors, what worked, what didn\'t, action items."),
        Flashcard(front="Most important pre-mutation step during incident?", back="Capture state. <code>kubectl get all -A -o yaml &gt; incident-pre.yaml</code>; describe affected resources; preserve logs. You can\'t debug what you can\'t reproduce."),
    ],
    quizzes=[
        Quiz(prompt="A Pod is stuck in Pending. <code>kubectl describe</code> shows event: \"0/3 nodes available: 3 Insufficient memory.\" What\'s the diagnostic + remediation path?", answer="<strong>Diagnosis:</strong> the Pod\'s memory request exceeds available memory on every node. <strong>(1) Check the Pod\'s request:</strong> <code>kubectl get pod -o jsonpath=\'{.spec.containers[*].resources.requests.memory}\'</code>. (2) Check node capacity: <code>kubectl describe nodes</code> — Allocatable + Allocated. (3) Decide: is the request realistic? Apps often request more than they use. Set requests to actual P95 + headroom. (4) Or: scale up nodes. Cluster Autoscaler / Karpenter (Lesson 34) should add a node automatically; if not, autoscaler logs reveal why. (5) Or: tighter Pod scheduling. Topology spread, anti-affinity may be unnecessarily restricting nodes. <strong>Anti-pattern:</strong> dropping requests to 0 to make Pod schedule. Then you have no QoS guarantee + nothing for HPA to compute on."),
        Quiz(prompt="Application is intermittently failing with TLS errors. App logs say \"x509: certificate expired.\" What\'s the investigation?", answer="<strong>(1) Identify which cert.</strong> Is it the cluster\'s API server cert? Service-to-service mTLS (mesh)? Application-level TLS (Ingress)? Each has a different rotation mechanism. <strong>(2) <code>kubectl get certificate -A</code></strong> — cert-manager managed certs. Check status. Status conditions reveal renewal failure. <strong>(3) <code>kubectl describe issuer / clusterissuer</code></strong> — is the issuer healthy? Let\'s Encrypt rate-limited? DNS provider misconfigured? <strong>(4) Mesh certs:</strong> mesh control plane handles rotation; check control-plane logs. <strong>(5) API server cert:</strong> kubeadm or cloud control plane handles. Check the cluster\'s health. <strong>(6) Time skew:</strong> if the node\'s clock is wrong, every cert appears expired. <code>chronyc tracking</code> on nodes. <strong>(7) Long-term:</strong> alert on certificate expiry &gt;14 days out. Don\'t learn this on Friday at 5 PM."),
        Quiz(prompt="The team\'s on-call engineer pages everyone: \"production is broken!\" The CTO asks how to handle. <strong>Click for the playbook. ▼</strong>", cyoa=True, cyoa_tag="the playbook", answer="<strong>(1) Acknowledge + impact assessment.</strong> Is it user-facing? How many users? Severity. SLO budget burning fast? <strong>(2) Form an incident channel.</strong> Slack channel #incident-2026-05-03-prod. Pin the goal: \"restore service.\" Anyone with relevant context joins. <strong>(3) Roles.</strong> Incident Commander (decision-maker, communicates externally), Subject-Matter Expert (technical lead), Scribe (documents timeline), Comms (updates customers/leadership). Roles can collapse to one person at small scale. <strong>(4) Capture pre-mutation state.</strong> <code>kubectl get all -A -o yaml &gt; incident-pre.yaml</code>. Describe affected resources. <strong>(5) Triage with methodology.</strong> Reproduce → observe → hypothesise → test. Don\'t skip steps. <strong>(6) Comms cadence.</strong> Status update every 15-30 minutes (\"investigating,\" \"identified cause,\" \"deploying fix,\" \"monitoring\"). External users get bare facts; internal team gets richer. <strong>(7) Mitigate first; root-cause later.</strong> Roll back the change, scale up capacity, route around the failure — restore service first, even with a duct-tape fix. Root cause investigation can be in a calm post-mortem. <strong>(8) Post-mortem within 48h.</strong> Timeline, contributing factors, action items, who owns each. Blameless. <strong>(9) Action items in tickets.</strong> Track closure. Half the value of post-mortems is the prevention work; the other half is the muscle memory for the next incident."),
    ],
    glossary=[
        GlossaryItem(name="Triage", definition="Initial assessment + classification of an incident. Define impact + assign priority."),
        GlossaryItem(name="kubectl describe", definition="Show resource status + events. The single most useful diagnostic command."),
        GlossaryItem(name="kubectl logs --previous", definition="Logs from the previous container instance (post-crash). Crucial after a crash."),
        GlossaryItem(name="kubectl debug", definition="Add an ephemeral container to a Pod or copy a Pod with different image. For distroless containers, side-loading debug tools, etc."),
        GlossaryItem(name="kubectl auth can-i", definition="Check RBAC permissions. With <code>--as</code> impersonate; with <code>--list</code> enumerate."),
        GlossaryItem(name="kubectl explain", definition="Field-level documentation from the running cluster. Always reflects the actual API version."),
        GlossaryItem(name="Game day", definition="Scheduled chaos engineering exercise. Inject failure; team practices response."),
        GlossaryItem(name="Runbook", definition="Markdown document linked to an alert: how to diagnose + remediate. Evolves from post-mortems."),
        GlossaryItem(name="Blameless post-mortem", definition="Incident retrospective focusing on system-level fixes, not individual blame."),
        GlossaryItem(name="Incident Commander", definition="Single decision-maker during an incident. Coordinates response; communicates externally."),
        GlossaryItem(name="Pre-mutation state capture", definition="Save cluster state before making changes during an incident. Enables debugging + retrospective."),
        GlossaryItem(name="MTTR", definition="Mean Time To Recovery. Measured per incident; tracked as a team metric."),
    ],
    recap_lead="Methodology before tooling. Reproduce → observe → hypothesise → test → verify. The kubectl evidence kit + observability stack handles most cases. Common failure patterns recur — pattern-recognition + runbooks accelerate response. The discipline (game days, blameless post-mortems) makes the difference.",
    recap_next="<strong>That\'s the full K-COM curriculum.</strong> 44 lessons + the L7.5 primer. From \"what is Kubernetes?\" to \"how to debug it under fire.\" Every K-Town district mapped, every primitive covered. The detective\'s office closes the loop — when you know how the system works, you know how to fix it when it doesn\'t. <strong>The course is complete.</strong>",
)
