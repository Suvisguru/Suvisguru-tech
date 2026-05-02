from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Print shop progressive printing run: a stable run flowing to 90% of customers, a canary run going to 10%, a metrics dial deciding promote/abort, and a phased ramp 10→50→100.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">PRINT SHOP · PROGRESSIVE RELEASE FLOOR</text>
  <g transform="translate(40,55)"><rect width="160" height="120" rx="6" fill="#5A9F7A"/><text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">STABLE · v1.2</text><rect x="14" y="34" width="132" height="14" rx="2" fill="#FBF7F0"/><text x="80" y="44" text-anchor="middle" font-size="8" fill="#3D7857" font-weight="700">90% traffic</text><rect x="14" y="52" width="132" height="60" rx="3" fill="#FBE8DC" opacity="0.4"/><text x="80" y="84" text-anchor="middle" font-size="9" fill="#3F4A5E" font-style="italic">9 of 10 Pods</text></g>
  <g transform="translate(220,55)"><rect width="160" height="120" rx="6" fill="#E8B547"/><text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">CANARY · v1.3</text><rect x="14" y="34" width="132" height="14" rx="2" fill="#FBF7F0"/><text x="80" y="44" text-anchor="middle" font-size="8" fill="#8B5A00" font-weight="700">10% traffic</text><rect x="14" y="52" width="132" height="60" rx="3" fill="#FBF7F0" opacity="0.4"/><text x="80" y="84" text-anchor="middle" font-size="9" fill="#3F4A5E" font-style="italic">1 of 10 Pods</text></g>
  <g transform="translate(400,55)"><rect width="160" height="120" rx="6" fill="#3F4A5E"/><text x="80" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">ANALYSIS</text><rect x="14" y="34" width="132" height="20" rx="2" fill="#FBE8DC"/><text x="20" y="48" font-size="8" fill="#A04832" font-weight="700">errors &gt; baseline?</text><rect x="14" y="58" width="132" height="20" rx="2" fill="#E0EFE6"/><text x="20" y="72" font-size="8" fill="#3D7857" font-weight="700">P99 &lt; baseline+10%?</text><text x="80" y="98" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">decide: promote/abort</text></g>
  <g transform="translate(580,55)"><text x="30" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">RAMP</text><rect x="0" y="30" width="60" height="12" rx="2" fill="#5A9F7A"/><text x="30" y="40" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">10%</text><rect x="0" y="46" width="60" height="12" rx="2" fill="#5A9F7A" opacity="0.7"/><text x="30" y="56" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">25%</text><rect x="0" y="62" width="60" height="12" rx="2" fill="#5A9F7A" opacity="0.5"/><text x="30" y="72" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">50%</text><rect x="0" y="78" width="60" height="12" rx="2" fill="#5A9F7A" opacity="0.3"/><text x="30" y="88" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">100%</text></g>
</svg>"""

LESSON = LessonSpec(
    num="40",
    title_short="progressive delivery",
    title_full="Progressive Delivery · Argo Rollouts and Flagger",
    title_html="Lesson 40 — Progressive Delivery · K-COM",
    module_eyebrow="Module 17 · Lesson 40 · safer rollouts via canary + analysis",
    hero_sub_html='Standard Deployments do <strong>rolling updates</strong>: replace Pods one at a time. Fine for small risks; dangerous for big ones. <strong>Progressive delivery</strong> adds <em>traffic shaping</em> + <em>automated analysis</em>: send a small slice of traffic to the new version, measure metrics, promote or abort automatically. Two main tools: <strong>Argo Rollouts</strong> and <strong>Flagger</strong>.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='You ship v1.3 with confidence. The default rolling update replaces 25% of replicas at a time. The 25% turns out to have a regression — but by the time the team notices (5-10 minutes), 100% of replicas have rolled. <em>Recovering means rolling back the same way you rolled out</em>: another 5-10 minutes. Total: 20 minutes of degraded service. With <strong>Argo Rollouts</strong>: ship v1.3 to 5% first, automated analysis catches the regression in 30 seconds, rollback is instant, no user impact. Worth the setup.',
    stamp_html='<strong>Argo Rollouts</strong> + <strong>Flagger</strong> are the two main K8s progressive-delivery controllers. They replace Deployment with a CRD that knows how to <em>shift traffic gradually</em> (10% → 25% → 100%) using a service mesh, Ingress, or Gateway API. They run <em>automated analysis</em> (Prometheus metrics, custom queries) at each step; promote on success, abort + rollback on failure. <strong>Argo Rollouts</strong> is K8s-native + integrates with Argo CD; <strong>Flagger</strong> is mesh-native + integrates with Flux + many meshes.',
    district_pin="kt-pin36",
    district_label="Print Shop — Progressive Release Floor",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Beyond rolling updates",
            body_html="""    <p>Standard K8s rolling update is two-axis: <code>maxSurge</code> (extra replicas during rollout) + <code>maxUnavailable</code> (allowed-down during rollout). It\'s a binary deploy: old version replaced by new. No traffic shaping (every Pod gets equal traffic from the Service). No metric-driven validation (deploy proceeds regardless of error rate).</p>
    <p>Progressive delivery splits the deploy into <strong>phases</strong>:</p>
    <ul>
      <li><strong>Canary</strong> phase 1: 5% of traffic to new version, 95% to old. Wait. Measure.</li>
      <li><strong>Canary</strong> phase 2: if metrics look good, ramp to 25%. Wait. Measure.</li>
      <li>Continue ramping. <strong>Promote</strong> to 100% only after final analysis pass.</li>
      <li>If any phase\'s metrics fail, <strong>abort</strong>: drop traffic back to 0%, scale canary down, alert.</li>
    </ul>
    <p>This is what actual production teams want — but isn\'t in core K8s. Argo Rollouts and Flagger fill the gap.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Argo Rollouts — Deployment replacement",
            h2="The K8s-native option",
            body_html="""    <p><strong>Argo Rollouts</strong> ships a <code>Rollout</code> CRD that replaces <code>Deployment</code>. Same shape (PodSpec, replicas, selectors), plus a strategy section:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: {name: web}
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 5
      - pause: {duration: 5m}
      - setWeight: 25
      - pause: {duration: 5m}
      - setWeight: 50
      - analysis:
          templates:
          - templateName: success-rate
      - setWeight: 100
      trafficRouting:
        nginx:
          stableIngress: web-stable
  template: { ... PodSpec ... }</code></pre>
    <p>The <code>analysis</code> step runs an <code>AnalysisTemplate</code> — typically a Prometheus query. \"Is the canary\'s success rate ≥ 99%?\" Yes → continue. No → abort + rollback.</p>
    <p>Traffic routing options (depending on your ingress / mesh):</p>
    <ul>
      <li>Ingress NGINX (legacy)</li>
      <li>Gateway API (modern)</li>
      <li>Istio, Linkerd, Cilium meshes</li>
      <li>AWS Load Balancer Controller (TargetGroup weights)</li>
      <li>Manual replica-count weights (no traffic mesh; less precise)</li>
    </ul>
    <p>Argo Rollouts UI shows the Rollout state in real time: which step, what % of traffic, what the analysis is seeing. Plays nicely with Argo CD\'s Application UI.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Flagger — service-mesh-native",
            h2="The other major option",
            body_html="""    <p><strong>Flagger</strong> is Flux\'s sister project for progressive delivery. Different model: rather than replacing Deployment, Flagger <em>watches</em> a Deployment and orchestrates a parallel canary Deployment + traffic shifts via the service mesh.</p>
    <p>Same canary semantics: weighted traffic, automated analysis, promotion / rollback. Flagger has first-class support for:</p>
    <ul>
      <li>Istio, Linkerd, Cilium, NGINX, Contour, Gloo Edge</li>
      <li>AWS App Mesh</li>
      <li>Kuma</li>
    </ul>
    <p>Flagger\'s strength: deeper mesh integration. Linkerd-based progressive delivery often uses Flagger because of the tight Linkerd integration. Argo Rollouts\' strength: tight integration with Argo CD\'s ecosystem.</p>
    <p>Both support similar canary strategies + blue/green + experiments (compare two versions side by side without traffic shift).</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Analysis templates and abort criteria",
            h2="What \"good metrics\" means in canary",
            body_html="""    <p>The analysis step is the heart of progressive delivery. Common AnalysisTemplate metrics:</p>
    <ul>
      <li><strong>Success rate</strong>: <code>sum(rate(http_requests_total{status!~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))</code> — must be ≥ 99%.</li>
      <li><strong>Latency</strong>: <code>histogram_quantile(0.99, http_request_duration_seconds_bucket{...}[5m])</code> — must be ≤ baseline + 10ms.</li>
      <li><strong>Error rate</strong>: <code>sum(rate(http_requests_total{status=~\"5..\"}[5m]))</code> — must be ≤ N per minute.</li>
      <li><strong>Custom business metrics</strong>: cart_abandonment_rate, signup_completions, etc. — must be in expected range.</li>
    </ul>
    <p>Compare canary metrics to <em>stable</em> metrics, not absolute thresholds. \"Canary success rate is within 1% of stable\" is more robust than \"canary success rate is &gt; 99%.\" Real traffic varies; relative metrics catch regressions.</p>
    <p>Failure budgets: define how many failed analyses tolerated before abort. Default 1; higher for noisy services.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The most common progressive-delivery mistake: starting too aggressive. Five percent to canary, immediately 100%, no pause. The point of canary is to <em>see something happen</em> at 5% before 100%. Industry guidance: minimum 5 minutes per step; more for low-volume services where 5 minutes doesn\'t give enough samples for stable metrics. Set your AnalysisTemplate\'s <code>interval</code> + <code>count</code> based on your real traffic volume.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team configures Argo Rollouts with 5% → 25% → 50% → 100% canary phases. Each phase is 1 minute. Their service does ~50 requests per second. Why might the canary analysis be unreliable?",
            options=[
                ("a) 1 minute is too long; canaries should be 30 seconds", False),
                ("b) 1 minute × 50 RPS = 3000 requests; at 5% canary that\'s 150 requests. The metric (e.g., 99% success rate) is computed from too small a sample to be statistically meaningful — noise dominates", True),
                ("c) The pauses should be 10 seconds", False),
            ],
            feedback="<strong>Answer: b.</strong> Statistics matter. 150 requests at 99% success rate = ±0.8% noise. A real 0.5% regression looks like noise. <strong>Fix:</strong> longer pauses (5+ min) or higher canary weights, especially for low-volume services. Compare canary vs stable rates rather than absolute thresholds.",
        ),
    },
    before_after_before='<p>Standard rolling update. Bug ships in v1.3, replicas roll over 5 minutes, customer impact for 5 minutes before someone notices, manual rollback another 5 minutes. Total: 10+ minutes degraded. \"How do we ship safely?\" answered with feature flags + lots of testing — but production traffic is its own surprise.</p>',
    before_after_after='<p>Argo Rollouts canary. Bug ships in v1.3, hits 5% canary first, AnalysisTemplate detects elevated 5xx within 30 seconds, automatic rollback in 10 seconds. Total customer impact: ~30 seconds of degraded performance for 5% of traffic. \"How do we ship safely?\" answered by the controller.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Progressive delivery is the difference between \"hope\" and \"verified.\" Once you have it, you don\'t go back.</p>',
    analogy_intro_html='<p>The Print Shop\'s progressive release floor doesn\'t print every poster all at once. The first 5% of customers get the new version (canary); the other 95% get the established run (stable). A quality-control inspector watches what comes back: complaints, reprints, returns. If the new version is fine, they ramp to 25%, 50%, then full. If complaints spike, they abort and pull the new version off the press immediately. The inspector\'s rules are written down explicitly (analysis templates) so the decision is automatic, not based on vibes.</p>',
    translation_rows=[
        ("Established run", "Stable Deployment / version"),
        ("New canary run", "Canary Deployment / Rollout step"),
        ("\"5% of customers get the new version\"", "<code>setWeight: 5</code>"),
        ("Quality-control inspector\'s rules", "<code>AnalysisTemplate</code> (Prometheus queries)"),
        ("\"Inspect for 5 minutes\"", "<code>pause: { duration: 5m }</code>"),
        ("\"Promote to full run\"", "<code>setWeight: 100</code>"),
        ("\"Abort and revert\"", "Auto-rollback on AnalysisTemplate failure"),
    ],
    analogy_stops="The analogy stops here: real progressive delivery shifts traffic via L7 routing (Ingress / Gateway API / mesh), not by selecting which customers get which version. And canary Pods are real Pods running real code — not a separate run on the same machine.",
    eli5='Try the new cookies on a small group of testers first. If they like it, give to everyone. If they don\'t, throw it out.',
    eli10="Argo Rollouts (CRD-based, K8s-native) and Flagger (mesh-native, Flux companion) replace standard rolling updates with weighted-traffic canary deploys + automated analysis. Define steps (5% → 25% → 50% → 100%) with pause durations. Each pause runs Prometheus queries (AnalysisTemplate) to validate. Promote on success; auto-rollback on failure. Pair with mesh / Ingress / Gateway API for traffic shaping.",
    scenarios=[
        Scenario(name="A SaaS using Argo Rollouts on every prod service", body="Every Deployment migrated to Rollout CRD. Standard canary: 5% → 25% → 50% → 100% with 10-min pauses. AnalysisTemplate checks success rate + P99 latency + custom business metric. ~3 ship-aborts per quarter; without canary they would have been customer-visible. Cumulative incidents avoided: significant."),
        Scenario(name="A bank using Flagger with Linkerd mTLS canary", body="Linkerd handles mTLS + traffic shifting. Flagger configures TrafficSplit. Per-service AnalysisTemplate based on golden signals. Compliance team appreciates: every release is a controlled experiment, every rollback is a documented event."),
        Scenario(name="A startup using Argo Rollouts blue/green", body="Not all services need canary; some prefer blue/green for atomic switches. Rollout supports blue/green strategy: deploy new version, run smoke tests, flip Service selector. Same CRD, different strategy. Used for stateful services where partial traffic split is awkward."),
        Scenario(name="A team that learned analysis matters", body="Initially had Argo Rollouts with no AnalysisTemplate — just timed canary. A regression slipped through anyway. Added AnalysisTemplate with success-rate + latency. Two months later, AnalysisTemplate caught a regression that timed-only would have promoted. Lesson: pause + analysis, not just pause."),
    ],
    misconceptions=[
        Misconception(myth="Progressive delivery is only for huge services.", truth="It\'s for any service where regressions are expensive. A small auth service that breaks logins is more impactful than a big background job. Risk = probability × impact; not always proportional to size."),
        Misconception(myth="Canary requires a service mesh.", truth="Service mesh gives precise weighted traffic shaping. Without one, you can do <em>replica-based</em> weights — 1 canary Pod alongside 19 stable = ~5% traffic. Less precise but works. Most ingresses (Ingress NGINX, Gateway API controllers) support weighted backends natively."),
        Misconception(myth="If canary metrics are flat, the deploy is fine.", truth="Flat success rate doesn\'t mean no regression. Latency spike, queue backup, downstream pressure can all be regressions. Multi-metric analysis (success + latency + custom signals) catches more."),
    ],
    flashcards=[
        Flashcard(front="Argo Rollouts vs Flagger?", back="Argo Rollouts: replaces Deployment with Rollout CRD; integrates with Argo CD. Flagger: watches Deployment + creates parallel canary; integrates with Flux + meshes. Both do the same canary thing differently."),
        Flashcard(front="Canary phases?", back="Sequence of <code>setWeight</code> + <code>pause</code> + (optional) <code>analysis</code> steps. \"5% pause 5m, 25% pause 5m, analysis, 100%\" is typical."),
        Flashcard(front="AnalysisTemplate?", back="CRD defining metrics queries + success criteria. Argo Rollouts runs it as part of canary phases. Returns success / failure / inconclusive."),
        Flashcard(front="Traffic routing options for Argo Rollouts?", back="Ingress NGINX, Gateway API, Istio, Linkerd, Cilium, AWS LB Controller, manual replica-count weights."),
        Flashcard(front="Blue/green strategy?", back="Deploy new version alongside old. Run tests. Flip Service selector to new. Old kept around for rollback. Atomic switch; no traffic split."),
        Flashcard(front="Experiments?", back="Argo Rollouts feature: deploy two versions side by side without flipping traffic. Compare metrics; decide which to promote. Used for A/B tests with controlled exposure."),
        Flashcard(front="Flagger TrafficSplit?", back="Flagger\'s native CRD for service-mesh-aware splits. With Linkerd, it generates SMI TrafficSplit. With Istio, VirtualService."),
        Flashcard(front="Analysis at the right cadence?", back="Pause should give enough samples for statistically valid metrics. Low-volume services need longer pauses or higher canary weights."),
    ],
    quizzes=[
        Quiz(prompt="A team\'s Rollout aborts during analysis because P99 latency exceeded threshold by 5%. Investigation shows: the canary Pod was scheduled on a slower node. What\'s the fix?", answer="<strong>Two paths:</strong> (1) <em>Make analysis more robust</em>. Use a comparison query: <code>p99(canary) - p99(stable) &lt; 10ms</code> instead of absolute threshold. Comparing canary to stable handles cluster-wide variability. (2) <em>Schedule canary like stable</em>. Use the same nodeSelector / affinity for canary Pods. If stable runs on x86, so should canary. <strong>Anti-pattern:</strong> tightening AnalysisTemplate thresholds to ignore the issue — masks real regressions. <strong>Better:</strong> understand why the canary differs from stable; eliminate that difference. Progressive delivery exposes infrastructure variance; sometimes that\'s the bug."),
        Quiz(prompt="A team adopts Argo Rollouts. They notice the rollout takes 20 minutes for what was a 5-minute deploy. Justified?", answer="<strong>Yes — and no.</strong> The 20-minute total reflects: (1) Multiple canary phases (5% → 25% → 50%, 5 min each). (2) Final analysis. (3) Promotion. <strong>What you\'re trading:</strong> 15 extra minutes of deploy time for ~30 seconds of customer impact during regression vs ~10 minutes of full-blast impact. <strong>Tunables:</strong> shorten pauses if your traffic volume gives statistical confidence faster. Skip canary for trivial config-only changes (<code>spec.template.metadata.annotations</code> bumps). Some teams have two strategies: \"safe path\" (full canary) for risky changes, \"fast path\" (rolling update) for trivial. Pick by classifying the diff. <strong>The 20-minute total is the cost of safety</strong>; a regression that escapes canary is far more expensive."),
        Quiz(prompt="The team is rolling out Argo Rollouts cluster-wide. <strong>Click for the migration playbook. ▼</strong>", cyoa=True, cyoa_tag="the migration playbook", answer="<strong>(1) Pilot.</strong> Pick one non-critical service; convert Deployment → Rollout CRD with simple canary (5% → 100%, 2-min pause, no analysis). Validate the rollout works without breaking deploys. <strong>(2) Add AnalysisTemplate.</strong> Define one for success rate. Validate it triggers correctly by introducing a synthetic 5xx. <strong>(3) Roll to one team.</strong> Migrate 5-10 services. Engineers see the UI; Slack alerts on aborts. Iterate on AnalysisTemplate accuracy. <strong>(4) Define team-wide patterns.</strong> Standard AnalysisTemplate library: success-rate, latency-comparison, custom-metric-comparison. Standard step pattern: 5% → 25% → 50% → 100% with 5-min pauses. <strong>(5) Roll cluster-wide.</strong> One service team at a time. Two-quarter migration; track abort rate as KPI. <strong>(6) Stretch goal — automated promotion gate.</strong> No service can deploy to prod without a Rollout + AnalysisTemplate. Enforce via Kyverno or VAP. <strong>Lessons learned:</strong> the social side is harder than the technical: getting engineers to trust the controller takes a quarter of \"yes, we\'re aware of the changes; the controller is doing the right thing.\" Once trust is established, ship velocity goes up because confidence is higher."),
    ],
    glossary=[
        GlossaryItem(name="Progressive delivery", definition="Pattern of deploying new versions in phases with traffic shifts + automated analysis."),
        GlossaryItem(name="Argo Rollouts", definition="K8s controller replacing Deployment with Rollout CRD. Canary, blue/green, experiments."),
        GlossaryItem(name="Flagger", definition="Service-mesh-native progressive delivery controller. Companion to Flux."),
        GlossaryItem(name="Canary", definition="Small fraction of traffic routed to new version for validation."),
        GlossaryItem(name="setWeight", definition="Argo Rollouts step: \"send X% of traffic to canary.\""),
        GlossaryItem(name="AnalysisTemplate / AnalysisRun", definition="Argo Rollouts CRDs. Templates define metric queries + criteria; Runs execute them during a Rollout."),
        GlossaryItem(name="Blue/green", definition="Deploy strategy: new version alongside old; switch atomically. No traffic split."),
        GlossaryItem(name="Experiment", definition="Run two versions side-by-side without traffic shift. Compare metrics."),
        GlossaryItem(name="Traffic routing (Argo Rollouts)", definition="Mechanism to shift traffic — Gateway API, Ingress NGINX, mesh, AWS LB."),
        GlossaryItem(name="TrafficSplit (SMI)", definition="Standard CRD for service-mesh weighted splits. Used by Flagger with Linkerd."),
        GlossaryItem(name="Failure budget (analysis)", definition="Number of failed AnalysisRuns tolerated before abort."),
        GlossaryItem(name="Abort", definition="Auto-rollback when canary fails analysis. Drops traffic to 0%, scales canary down."),
    ],
    recap_lead="Argo Rollouts and Flagger turn Deployments into phased releases with automated analysis. Define canary steps + AnalysisTemplate; promote on success, abort on failure. Cost: minutes of extra deploy time. Benefit: regressions caught at 5% traffic, not after they\'ve hit 100%.",
    recap_next="<strong>Next — Lesson 41: CRDs Deep Dive.</strong> Module 18 begins. The K8s extension story — schemas with CEL validation, conversion webhooks, the full custom-resource lifecycle. Permit Office, advanced wing.",
)
