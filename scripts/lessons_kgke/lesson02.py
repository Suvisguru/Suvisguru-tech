"""K-GKE G2 — GKE Versioning and Release Channels."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GKE release channels — Rapid → Regular → Stable → Extended; auto-upgrades; maintenance windows.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">The Almanac Hut — channels &amp; the planting calendar</text>
  <rect x="40" y="70" width="160" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="120" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Rapid</text>
  <text x="120" y="110" text-anchor="middle" font-size="9" fill="#FFFFFF">latest minors first</text>
  <text x="120" y="125" text-anchor="middle" font-size="9" fill="#FFFFFF">~weeks bleeding edge</text>
  <text x="120" y="143" text-anchor="middle" font-size="9" fill="#FFFFFF">canary &amp; preview</text>
  <text x="120" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FFFFFF">no SLA on minors</text>
  <rect x="220" y="70" width="160" height="120" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="300" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">Regular (default)</text>
  <text x="300" y="110" text-anchor="middle" font-size="9" fill="#FFFFFF">balanced cadence</text>
  <text x="300" y="125" text-anchor="middle" font-size="9" fill="#FFFFFF">most prod clusters</text>
  <text x="300" y="143" text-anchor="middle" font-size="9" fill="#FFFFFF">SLA on supported minors</text>
  <rect x="400" y="70" width="160" height="120" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="480" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF7F0">Stable</text>
  <text x="480" y="110" text-anchor="middle" font-size="9" fill="#FBF7F0">conservative</text>
  <text x="480" y="125" text-anchor="middle" font-size="9" fill="#FBF7F0">slowest minors</text>
  <text x="480" y="143" text-anchor="middle" font-size="9" fill="#FBF7F0">regulated workloads</text>
  <rect x="580" y="70" width="140" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="650" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Extended</text>
  <text x="650" y="110" text-anchor="middle" font-size="9" fill="#FBF1D6">long-term</text>
  <text x="650" y="125" text-anchor="middle" font-size="9" fill="#FBF1D6">support window</text>
  <text x="650" y="143" text-anchor="middle" font-size="9" fill="#FBF1D6">~2 yr per minor</text>
  <text x="650" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">premium tier</text>
</svg>"""


LESSON = LessonSpec(
    num="02",
    title_short="release channels",
    title_full="G2 · GKE Versioning and Release Channels",
    title_html="K-GKE G2 · Versioning and Release Channels",
    module_eyebrow="Module G2 · the Almanac Hut",
    hero_sub_html='Four release channels: <strong>Rapid → Regular → Stable → Extended</strong>. New minor versions land in Rapid first, promote to Regular, then Stable, and (for designated versions) Extended for ~2-year long-term support. Plus <strong>auto-upgrades</strong> (default for channel clusters), <strong>maintenance windows</strong> + <strong>maintenance exclusions</strong>, version + patch availability, EOS, SLA, and upgrade notifications. <em>The channel you pick is the upgrade-cadence × stability trade-off.</em>',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Your prod cluster auto-upgraded last night to a new patch version. A node-image kernel change broke a custom NVIDIA driver DaemonSet you forgot was there. <em>15% of GPU Pods now CrashLoopBackOff.</em> You realise you set the maintenance window for the right hours but never set a <em>maintenance exclusion</em> for your finals-week peak that started yesterday. Today\'s lesson: GKE channels, windows, and exclusions — how to control upgrades without disabling them.",
    stamp_html="<strong>Pick a channel (Regular = default for prod; Stable for risk-averse; Extended for 2-year LTS; Rapid for canary). Set maintenance windows for routine upgrades; set maintenance exclusions during peaks / freezes. Don\'t opt out of channels.</strong>",
    district_pin="kg-plot02",
    district_label="The Almanac Hut",
    sections=[
        Section(
            eyebrow="Section 1.1 · the four channels",
            h2="Four release channels — Rapid, Regular, Stable, Extended",
            body_html="""    <p>A <strong>release channel</strong> is GKE\'s commitment to which K8s minors a cluster receives, when, and for how long. Pick at cluster create; can be changed (forward-only is the safe path; rapid → regular is fine, regular → rapid moves you onto bleeding-edge faster).</p>
    <ul>
      <li><strong>Rapid</strong> — newest GKE minors land here first (often within weeks of upstream K8s release). Useful for canary clusters, preview-feature testing, internal platform-team validation. <em>No SLA on the latest minor; supported once it stabilizes.</em></li>
      <li><strong>Regular</strong> — balanced cadence. Most production clusters. Minors arrive after they\'ve baked in Rapid for some weeks. Auto-upgrades flow predictably.</li>
      <li><strong>Stable</strong> — conservative cadence. Minors arrive after Rapid + Regular have validated them. For risk-averse production: regulated workloads where any change has a long approval cycle.</li>
      <li><strong>Extended</strong> — long-term support window for designated minor versions (~2 years per minor). For workloads that cannot upgrade quarterly. <em>Premium tier; specific version line.</em></li>
    </ul>
    <p><strong>No-channel clusters</strong> = clusters not enrolled in any channel. Loses auto-upgrades for minors; you upgrade manually. <em>Strongly discouraged for production</em> — you become responsible for tracking GKE EOS dates and force-migrating off unsupported versions.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · auto-upgrades + maintenance windows",
            h2="Auto-upgrades + maintenance windows",
            body_html="""    <p>Channel clusters get <strong>auto-upgrades</strong> by default — Google upgrades the control plane and (separately) node pools as part of the channel cadence.</p>
    <ul>
      <li><strong>Maintenance windows</strong> — one or more weekly time windows when GKE may perform upgrades and node-pool maintenance. Set per cluster. <em>Pick low-traffic hours;</em> an empty window means GKE picks any time.</li>
      <li><strong>Maintenance exclusions</strong> — explicitly block all upgrades during specific date ranges. Three exclusion scopes: <em>no upgrades</em> (suppresses minor + patch + node), <em>no minor upgrades</em> (still applies patches + security), <em>no minor or node upgrades</em>. Use during freezes (Black Friday, end-of-quarter, regulated change-control windows). Maximum exclusion length depends on scope (~30-180 days).</li>
      <li><strong>Surge upgrade</strong> on node pools — extra nodes added during the rolling upgrade so workloads drain to fresh nodes before old ones cordon. Tunable per pool. PDBs respected.</li>
      <li><strong>Blue-green node pool upgrade strategy</strong> — instead of in-place rolling, GKE creates a parallel new pool, drains workloads to it, then deletes the old. Atomic rollback before the old is deleted.</li>
    </ul>
    <p><strong>Key rule:</strong> <em>set the window AND the exclusions</em>. Window without exclusions = upgrades during your peak. Exclusion without window = ad-hoc upgrades when the exclusion expires.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · version availability + EOS + SLA",
            h2="Version availability, EOS, SLA, upgrade notifications",
            body_html="""    <p><strong>Version availability per channel</strong> evolves continuously. Use the <strong>GKE Release Notes</strong> + <strong><code>gcloud container get-server-config</code></strong> to see which minors + patches are currently available in each channel for your region.</p>
    <p><strong>End-of-support (EOS):</strong> each minor has a documented EOS date per channel. After EOS, the cluster is auto-upgraded by GKE to the next supported minor (you\'re not stranded; you may be force-upgraded sooner than you wanted). Channels publish their version-skew + EOS commitment so you can plan.</p>
    <p><strong>SLA:</strong> regional clusters have a 99.95% SLA on the control plane (Standard tier) when on a supported channel + version. Zonal clusters have no SLA (best-effort). Out-of-channel or EOS-version clusters lose SLA.</p>
    <p><strong>Upgrade notifications:</strong> enable Pub/Sub upgrade notifications — GKE publishes a message before maintenance fires. Subscribe with Cloud Functions / Workflows / Slack webhook to get a heads-up before each upgrade. <em>Operators love this</em>: \"upgrading prod-eu in 6 hours to v1.32.5\" lands in #ops-channel.</p>
    <p><strong>Pre-flight</strong> (before any minor upgrade): scan workloads for deprecated APIs (<code>gcpdiag</code>, <code>kube-no-trouble</code>, <code>Pluto</code>); validate Helm charts; review GKE Release Notes for breaking changes in the target minor.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · upgrade sequencing + safety",
            h2="Upgrade sequencing + safety patterns",
            body_html="""    <p><strong>Sequencing inside an auto-upgrade:</strong> control plane first, then node pools. Control plane upgrade is in place, ~minutes, no workload disruption. Node-pool upgrades roll one node at a time (with surge headroom and PDB-aware drain).</p>
    <p><strong>Manual override</strong> via <code>gcloud container clusters upgrade</code> — useful for accelerating a CVE patch or rolling back a node-pool change. <em>Manual control plane upgrades only move forward</em>; Google does not support rolling back the control plane to a prior minor.</p>
    <p><strong>Patch versions</strong> within a minor: GKE auto-applies these per channel cadence. They include security fixes + bug fixes; usually safe. Maintenance windows + exclusions still apply.</p>
    <p><strong>If something breaks during auto-upgrade</strong>: GKE automatically pauses if control-plane health checks fail; node-pool upgrades roll back the affected pool if upgrades fail health-checks. Combined with PDB-aware drain, the typical worst case is \"some Pods restart, the cluster ends up healthy.\" The atypical worst case (custom DaemonSet incompatible with new node image, etc.) is your responsibility — pre-flight + maintenance exclusions + canary on Rapid avoid most surprises.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="It\'s Black Friday week. The team needs no auto-upgrades for 7 days. What\'s the right knob?",
            options=[
                ("Disable the cluster\'s release channel.", False),
                ("Add a <strong>maintenance exclusion</strong> for the date range, scope <em>no upgrades</em>. Upgrades resume after the exclusion expires.", True),
                ("Delete the maintenance window.", False),
            ],
            feedback="Maintenance exclusions are the explicit \"don\'t upgrade now\" mechanism — preserves the channel + windows for normal operation; suspends them only for the freeze.",
        ),
    },
    before_after_before='<p>Pre-channel GKE meant operators picked a specific patch version at create and never moved. Versions went EOS silently; security patches required manual upgrade dance. Maintenance \"windows\" were a forum convention. No SLA differentiation by version. Auto-upgrades were either off (you forget) or on (surprises). The kube-no-trouble pre-flight discipline was bring-your-own. Operators tracked CVEs via mailing lists.</p>',
    before_after_after='<p>Modern GKE has <strong>release channels</strong> (Rapid / Regular / Stable / Extended) that codify the upgrade cadence + supported version window. Auto-upgrades flow within maintenance windows; exclusions block during peaks. Pub/Sub upgrade notifications give heads-up. SLA on supported channel + version. Documented EOS per minor per channel. <em>Upgrade discipline is built into the platform; you opt into a cadence and the platform delivers.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Pick the channel that matches your risk appetite and your change-control cadence. Add windows + exclusions. Don\'t opt out.</em></p>',
    analogy_intro_html='''<p>The <strong>Almanac Hut</strong> is the small wooden building at the back of the Visitors\' Pavilion. The Head Gardener (Google) keeps a calendar there showing when each new variety of seed becomes available, when the old varieties stop being supported, and when the planting and pruning happen.</p>
    <p>Visitors pick one of four planting calendars at sign-up:</p>
    <ul>
      <li><strong>Rapid Almanac</strong> — gets the brand-new variety right when the Gardener releases it. Bleeding edge. Useful for early-tester plots; not promised the variety will perform predictably.</li>
      <li><strong>Regular Almanac</strong> — gets the variety after a few weeks of testing in Rapid. The Gardener offers a yield guarantee (SLA). Most plots use this.</li>
      <li><strong>Stable Almanac</strong> — slow and conservative. Variety has been baked in Rapid + Regular before it lands here. For plots whose owners hate surprises.</li>
      <li><strong>Extended Almanac</strong> — picks one designated variety and supports it for two years. For plots whose owners cannot replant every quarter.</li>
    </ul>
    <p>Inside each calendar there are two important annotations: the weekly <em>Garden Maintenance Window</em> (when the Gardener will prune and replant, e.g. \"Tuesdays 2-6 AM\") and any <em>Maintenance Exclusions</em> the visitor has requested (\"please don\'t prune anything between Nov 25 and Dec 5 — that\'s our harvest week\"). The Gardener also sends a <em>Pub/Sub postcard</em> a few hours before any pruning so the visitor isn\'t surprised.</p>''',
    translation_rows=[
        ("The Almanac Hut", "GKE versioning + release-channel surface"),
        ("Rapid Almanac", "Rapid release channel"),
        ("Regular Almanac", "Regular release channel (default)"),
        ("Stable Almanac", "Stable release channel"),
        ("Extended Almanac", "Extended release channel (~2 yr LTS)"),
        ("No almanac at all", "No-channel cluster (manual upgrades; no auto-upgrades)"),
        ("Garden Maintenance Window", "Maintenance window (weekly time slot)"),
        ("Maintenance Exclusion", "Maintenance exclusion (block upgrades for date range)"),
        ("Pub/Sub postcard", "Upgrade notifications via Pub/Sub"),
        ("\"Variety performance guarantee\"", "SLA — 99.95% on supported channel + version"),
        ("Replant the whole bed at once", "Blue-green node pool upgrade"),
        ("Roll the new variety bed by bed", "Surge upgrade with PDB-aware drain"),
        ("Variety pulled from the catalog", "EOS — auto-upgrade to next supported minor"),
    ],
    analogy_stops="A real almanac is paper; channels are dynamic — versions stop being available without warning if you let your cluster drift past EOS without an exclusion. The Gardener auto-replants you onto a supported variety; you don\'t get to stay on yesterday\'s seed.",
    eli5="Google has a calendar for when new seed varieties come out and when old ones stop being supported. You pick one of four calendars: brand-new, steady, slow-and-careful, or super-long-term. You also tell Google when not to come prune (your harvest week). Google sends you a postcard before they prune.",
    eli10="GKE release channels = Rapid (bleeding edge, no SLA on latest minor) → Regular (default, balanced, SLA) → Stable (conservative) → Extended (~2-year LTS for designated minors, premium tier). Channel determines auto-upgrade cadence + supported version window + EOS dates. Maintenance windows schedule routine upgrades; maintenance exclusions block them during freezes. Pub/Sub upgrade notifications give heads-up. Pre-flight with gcpdiag / kubent / Pluto before minor upgrades. Don\'t run no-channel clusters in prod.",
    scenarios=[
        Scenario(
            name="SaaS — Regular channel + Tuesday 02-06 UTC + Nov-exclusion for Black Friday",
            body="A SaaS prod cluster: Regular channel, maintenance window Tuesdays 02-06 UTC, exclusion <em>no minor upgrades</em> Nov 20 - Dec 1 (security patches still apply). Pub/Sub upgrade notifications fire to a Slack channel. <em>Quarterly minor cycles run themselves; team intervenes only for the rare incompatibility.</em>",
        ),
        Scenario(
            name="Regulated bank — Stable channel + 6-week exclusions for change-control",
            body="A bank\'s payment cluster: Stable channel for slow predictable cadence, plus 6-week exclusion windows aligned with their change-control cycle. Pre-flight with gcpdiag before each upgrade window opens; CAB review mandatory. <em>~3 minor upgrades per year; predictable; auditable.</em>",
        ),
        Scenario(
            name="Hyperscale ISV — Extended channel for the regulated workload, Rapid for the inference platform",
            body="An ISV runs two GKE clusters per region. <em>Compliance cluster</em>: Extended channel, locked to a designated minor for 2 years. <em>Inference platform cluster</em>: Rapid channel — they want the latest GPU device-plugin features and TPU support as soon as Google ships them. Two channels, one team; the platform engineer documents the trade-off.",
        ),
        Scenario(
            name="Bug averted by Pub/Sub upgrade notification",
            body="A team\'s Pub/Sub upgrade notification fired with target version v1.30.6. A platform engineer on-call read the GKE Release Notes for that version and saw a known issue with their CSI driver version. They added a <em>2-week maintenance exclusion</em>; bumped the CSI driver in the meantime. <em>Auto-upgrade fired safely 3 weeks later.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Stable channel never auto-upgrades.\"",
            truth="Stable still auto-upgrades — just on a slower cadence. Minors arrive in Stable after they\'ve baked in Rapid + Regular; patches still flow continuously. Stable is \"conservative\", not \"manual.\" If you genuinely need no auto-upgrades, that\'s either Extended (still upgrades within the 2-year LTS minor) or no-channel (discouraged).",
        ),
        Misconception(
            myth="\"Maintenance window suppresses upgrades that haven\'t fired yet.\"",
            truth="Maintenance window <em>schedules when</em> upgrades may fire (the time-of-week slot). It does not stop GKE from queuing an upgrade. To suppress queued upgrades, use <strong>maintenance exclusions</strong> with appropriate scope. Window + exclusion together = controlled upgrade flow.",
        ),
        Misconception(
            myth="\"I can downgrade the control plane if an upgrade misbehaves.\"",
            truth="GKE control plane upgrades are <em>forward-only</em>. There is no supported rollback. If a control-plane upgrade introduces a problem, the path forward is: report the issue, wait for Google\'s patch, apply the patch (which moves you to a new patch version, not back to the old). Plan upgrades + exclusions to avoid this; the auto-pause on health-check failure prevents most disasters.",
        ),
    ],
    flashcards=[
        Flashcard(front="Four GKE release channels?", back="<strong>Rapid</strong> (newest minors first; canary; no SLA on latest minor), <strong>Regular</strong> (default; balanced; SLA), <strong>Stable</strong> (conservative for risk-averse prod), <strong>Extended</strong> (~2-year LTS for designated minors; premium tier)."),
        Flashcard(front="What\'s the difference between maintenance window and maintenance exclusion?", back="<strong>Maintenance window</strong> schedules <em>when</em> upgrades may fire (time-of-week slots). <strong>Maintenance exclusion</strong> blocks upgrades for a date range (with scope: no upgrades / no minor / no minor + node). Use both: window for routine; exclusion for freezes."),
        Flashcard(front="Three maintenance-exclusion scopes?", back="<strong>no upgrades</strong> (block everything: minor + patch + node-image), <strong>no minor upgrades</strong> (still apply patches + security), <strong>no minor or node upgrades</strong> (block everything except control-plane patches). Max length depends on scope (30-180 days)."),
        Flashcard(front="Do GKE control planes support rollback?", back="<strong>No.</strong> Control-plane upgrades are forward-only. Roll-forward via patch is the path. GKE auto-pauses upgrades on health-check failure and node-pool upgrades roll back the affected pool — but the control plane itself moves only forward."),
        Flashcard(front="What\'s the purpose of Pub/Sub upgrade notifications?", back="GKE publishes a Pub/Sub message before maintenance fires. Subscribe with Cloud Functions / Workflows / Slack webhook to get a heads-up — typically hours-to-days notice. Lets the on-call team verify the target version is safe before it lands."),
        Flashcard(front="When should you use Extended channel?", back="When the workload cannot upgrade quarterly: regulated industries, ISV-bundled workloads, infrastructure with long change-control cycles. Extended pins the cluster to a designated minor for ~2 years. Premium-tier feature."),
        Flashcard(front="What\'s a no-channel cluster, and why avoid it?", back="A cluster not enrolled in Rapid / Regular / Stable / Extended. Auto-upgrades disabled; you must manually upgrade and track EOS. Discouraged for prod — you become responsible for security patches, EOS dates, and force-migrating off unsupported versions."),
        Flashcard(front="Pre-flight tools before a minor upgrade?", back="<strong>gcpdiag</strong> (GCP-aware pre-flight), <strong>kube-no-trouble (kubent)</strong> (deprecated API scan against live cluster), <strong>Pluto</strong> (Helm chart manifest scan). Plus reading the GKE Release Notes for the target version."),
    ],
    quizzes=[
        Quiz(
            prompt="Your prod cluster is on Regular channel with maintenance window Tuesdays 02-06 UTC. The team is launching a new feature on Tuesday 5pm; rollout window is Tue-Thu. What configuration prevents an auto-upgrade during the launch?",
            answer="Set a <strong>maintenance exclusion</strong> for the date range Tue 12:00 UTC → Fri 12:00 UTC (or longer to give buffer), scope <strong>no upgrades</strong> (or <em>no minor upgrades</em> if you still want security patches). Pub/Sub upgrade notifications also let you confirm Google didn\'t pre-queue something; if it did, the exclusion suppresses it. After the launch validates, remove the exclusion (or let it auto-expire).",
        ),
        Quiz(
            prompt="You\'re running a v1.29 cluster on Regular channel. EOS is approaching. What\'s the upgrade plan?",
            answer="(1) Check the GKE Release Notes for v1.30 / v1.31 in Regular — pick the target. (2) Run gcpdiag + kubent against the cluster to find deprecated API usage. (3) Schedule the upgrade in the maintenance window; consider a maintenance exclusion right after to prevent piggyback patches. (4) Subscribe to Pub/Sub upgrade notifications. (5) If gcpdiag finds blockers, fix workloads first. (6) When the upgrade fires, Google upgrades the control plane in place; node pools roll with surge headroom. (7) If you don\'t take action, GKE auto-upgrades you to the next supported minor before EOS — you\'re not stranded; you may just upgrade later than convenient.",
        ),
        Quiz(
            prompt="The CTO walks in: \"Why are we on Regular channel? Latest features are in Rapid; let\'s switch.\" Defend or pivot.",
            answer="\"<strong>Rapid is for canary clusters and platform-team validation, not for prod we run customer workloads on.</strong> The reason: Rapid gets new minors within weeks of upstream K8s release; some of those minors have known issues that the GKE team patches in subsequent weeks before promoting to Regular. We\'d be running with the latest minors *and* their teething problems. The pattern that gets us the latest features safely: keep prod on Regular; spin up a small canary cluster on Rapid for the platform team to test new features + APIs. When something interesting lands in Rapid, we exercise it on canary, build the migration plan, then prod gets it 2-6 weeks later when it\'s in Regular and stable. <em>Regular gets the same features as Rapid, just slightly later, with better SLA and fewer surprises.</em>\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CTO",
        ),
    ],
    glossary=[
        GlossaryItem(name="Release channel", definition="GKE\'s commitment to which K8s minors a cluster receives + when + EOS dates. Four options: Rapid / Regular / Stable / Extended."),
        GlossaryItem(name="Rapid channel", definition="Newest GKE minors land first. For canary / preview-feature testing. No SLA on latest minor."),
        GlossaryItem(name="Regular channel", definition="Default. Balanced cadence; SLA on supported versions. Most production clusters."),
        GlossaryItem(name="Stable channel", definition="Conservative cadence. Minors arrive after Rapid + Regular have validated them. For risk-averse prod."),
        GlossaryItem(name="Extended channel", definition="Long-term support window for designated minors (~2 years). Premium tier. For workloads that cannot upgrade quarterly."),
        GlossaryItem(name="No-channel cluster", definition="Cluster not enrolled in any channel. No auto-upgrades. Operator must track EOS. Discouraged for prod."),
        GlossaryItem(name="Maintenance window", definition="Weekly time slot when GKE may perform upgrades + node maintenance."),
        GlossaryItem(name="Maintenance exclusion", definition="Date range that blocks upgrades. Three scopes: no upgrades / no minor / no minor + node. Max ~30-180 days depending on scope."),
        GlossaryItem(name="Pub/Sub upgrade notifications", definition="Pre-upgrade messages published to Pub/Sub. Subscribe via Cloud Functions / Workflows / Slack for heads-up notification."),
        GlossaryItem(name="Surge upgrade", definition="Per node pool — extra nodes added during rolling upgrade so workloads drain to fresh nodes before old ones cordon."),
        GlossaryItem(name="Blue-green node pool upgrade", definition="GKE creates a new pool, drains workloads, deletes old. Atomic rollback before old pool deletion."),
        GlossaryItem(name="EOS (end of support)", definition="Each GKE minor has a documented EOS per channel. After EOS, GKE auto-upgrades the cluster forward."),
    ],
    recap_lead='Four channels mapped to upgrade-cadence × stability trade-offs; window + exclusion are the routine + freeze controls; Pub/Sub gives heads-up; pre-flight with gcpdiag / kubent.',
    recap_next='<strong>Next — G3: GKE Networking.</strong> VPC-native (alias IPs), pod/service secondary ranges, IP exhaustion mitigation, GKE Dataplane V2 (Cilium-based eBPF), GKE Ingress + Gateway controller, NEG + container-native LB, Multi-Cluster Ingress / Multi-Cluster Services, Cloud Service Mesh, Network Connectivity Center, Shared VPC, firewall, DNS troubleshooting.',
)
