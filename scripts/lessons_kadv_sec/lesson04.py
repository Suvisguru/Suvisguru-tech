"""K-ADV-SEC S4 — PSA Restricted migration + runtime detection (Falco / Tetragon)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="PSA + runtime — three PSA profiles, plus Falco/Tetragon runtime probes.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Mandatory-Helmet Zones · K-Citadel — admission stops misconfig; runtime stops escape</text>
  <rect x="40" y="70" width="160" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="120" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">PSA: privileged</text>
  <text x="120" y="108" text-anchor="middle" font-size="9" fill="#1F2433">no restrictions</text>
  <text x="120" y="124" text-anchor="middle" font-size="9" fill="#1F2433">legacy / system</text>
  <rect x="220" y="70" width="160" height="100" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="300" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">PSA: baseline</text>
  <text x="300" y="108" text-anchor="middle" font-size="9" fill="#1F2433">no privileged Pods</text>
  <text x="300" y="124" text-anchor="middle" font-size="9" fill="#1F2433">+ no hostPath, hostNet, etc.</text>
  <rect x="400" y="70" width="160" height="100" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="480" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">PSA: restricted</text>
  <text x="480" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">drop ALL caps, runAsNonRoot</text>
  <text x="480" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">seccompProfile required</text>
  <rect x="580" y="70" width="140" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="650" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">Falco / Tetragon</text>
  <text x="650" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">eBPF syscall watch</text>
  <text x="650" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">runtime escape detection</text>
</svg>"""


LESSON = LessonSpec(
    num="04",
    title_short="PSA + runtime",
    title_full="S4 · PSA Restricted Migration + Runtime Detection (Falco / Tetragon)",
    title_html="K-ADV-SEC S4 · PSA + Runtime",
    module_eyebrow="Module S4 · the Mandatory-Helmet Zones — admission stops misconfig; runtime stops escape",
    hero_sub_html='Two complementary security layers. <strong>Pod Security Admission (PSA)</strong>: namespace-level enforcement of Pod-spec safety profiles — <em>privileged</em> (no restriction; legacy + system), <em>baseline</em> (no privileged, no hostPath, no hostNet, no privilege-escalation), <em>restricted</em> (drop ALL capabilities, runAsNonRoot, readOnlyRootFilesystem encouraged, seccompProfile required, allowPrivilegeEscalation false). <strong>Runtime detection</strong>: Falco / Tetragon attach eBPF probes to Linux syscalls; alert on suspicious behaviour (shell spawn from app container, mount() inside container, network connection to unexpected destination, write to /etc). Admission catches misconfig at submit time; runtime catches what slips past or emerges later.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A web app on the cluster ran a base image with an old <code>libxml</code>; an attacker leveraged a known CVE to gain shell. The Pod\'s SA was over-broad. The container had <code>privileged: true</code> for legacy reasons (the deploy was migrated from a VM). The attacker\'s shell ran <code>nsenter</code> + escaped to the host; pivoted to the kubelet credential. <em>Admission would have blocked the privileged Pod; runtime would have caught the nsenter call.</em> Today\'s lesson: defence-in-depth at the container layer.",
    stamp_html="<strong>PSA migration: privileged → baseline → restricted, namespace by namespace, audit → warn → enforce. Falco / Tetragon eBPF for runtime detection at scale. Admission stops misconfig; runtime stops escape attempts. Both layers are required for production-grade clusters.</strong>",
    district_pin="ksec-bastion04",
    district_label="Mandatory-Helmet Zones",
    sections=[
        Section(
            eyebrow="Section 1.1 · the three PSA profiles",
            h2="privileged, baseline, restricted",
            body_html="""    <p><strong>privileged</strong>: no restrictions. Use only for system namespaces (<code>kube-system</code>, monitoring agents needing host access). Default for legacy clusters.</p>
    <p><strong>baseline</strong>: no <code>privileged</code> containers, no <code>hostPath</code>, no <code>hostNetwork</code> / <code>hostPID</code> / <code>hostIPC</code>, no <code>allowPrivilegeEscalation: true</code>, no <code>NET_RAW</code> capability. Stops the most common cluster-escape vectors. Should be the cluster\'s minimum bar.</p>
    <p><strong>restricted</strong> (the strictest): everything from baseline + drop ALL capabilities (no <code>capabilities.add</code>), <code>runAsNonRoot: true</code>, <code>seccompProfile</code> required, <code>allowPrivilegeEscalation: false</code> explicitly. Recommended for all workloads that don\'t have a documented reason to be different.</p>
    <p>Each profile has three modes per namespace: <strong>enforce</strong> (block on violation), <strong>audit</strong> (record), <strong>warn</strong> (kubectl warning). Set via namespace labels: <code>pod-security.kubernetes.io/enforce: restricted</code>, <code>pod-security.kubernetes.io/warn: restricted</code>, etc.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · the migration playbook",
            h2="privileged → baseline → restricted, namespace by namespace",
            body_html="""    <p>Most existing clusters start at privileged for everything. The path:</p>
    <ol>
      <li><strong>Audit cluster-wide</strong>: <code>kube-no-trouble</code> / <code>kubescape</code> / <code>kyverno-pss-audit</code> finds Pods that would fail baseline + restricted.</li>
      <li><strong>Pick canary namespaces</strong>: dev / non-prod first; one namespace at a time; label with <code>warn: baseline</code> first.</li>
      <li><strong>Fix offenders</strong>: most are leftover from migration — privileged for no real reason, hostPath for ad-hoc debug. Remove the dependency or move to a privileged-allowed namespace.</li>
      <li><strong>Promote enforce: baseline</strong> per namespace.</li>
      <li><strong>Repeat for restricted</strong>: warn → enforce. Restricted often blocks workloads that ran as root; <code>runAsNonRoot</code> + image rebuilds with non-root user fix them.</li>
      <li><strong>Cluster default</strong>: once 80%+ of namespaces are restricted, set the cluster admission policy default to enforce-restricted; exempt the few legitimate privileged namespaces.</li>
    </ol>
    <p>Tools: <strong>Kyverno PSS pack</strong> (pre-built ClusterPolicies for each PSA profile + reporting); <strong>Gatekeeper PSS</strong> (Constraint templates); <strong>kyverno-pss-audit</strong> for migration prep.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · runtime detection — Falco vs Tetragon",
            h2="eBPF syscall watch + alert pipeline",
            body_html="""    <p><strong>Falco</strong> (CNCF Graduated): rules engine over Linux syscalls + K8s audit + container events. Default rules detect shell-in-container, write-to-etc, sensitive-mount, network-anomaly. Emit alerts via gRPC / Webhook / Kafka / Slack. Battle-tested; large rule library; works on most kernels.</p>
    <p><strong>Tetragon</strong> (Cilium project): eBPF-native, kernel-level. Lower overhead than Falco for high-cardinality monitoring. Can <em>also enforce</em> at runtime — kill processes, block syscalls — not just observe. More powerful + newer; learning curve is the trade-off.</p>
    <p>Pick: Falco for breadth + ecosystem + rule library; Tetragon for kernel-level performance + enforcement use cases. Many clusters run both — Falco for general detection, Tetragon for high-rps namespaces.</p>
    <p><strong>Common rules to enable</strong>: shell spawned in container; mount() inside container; write to /etc, /bin, /sbin; outbound network connection to unexpected CIDR; ptrace inside container; capability NET_RAW used; suspicious process tree (e.g., crypto-miner names).</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · alert pipeline + tuning",
            h2="From eBPF event to on-call action",
            body_html="""    <p>Runtime detection without a tuned pipeline is noise. Build the pipeline:</p>
    <ul>
      <li><strong>Aggregate</strong>: Falco / Tetragon emit events; route to Falcosidekick / Fluent Bit / Vector → SIEM (Loki, Splunk, OpenSearch).</li>
      <li><strong>Suppress noise</strong>: tune rules to your environment. \"Shell in container\" fires for legitimate <code>kubectl exec</code> debug; suppress when source = on-call group + window.</li>
      <li><strong>Correlate</strong>: an alert on a Pod gets joined with the Pod\'s namespace + service + recent admission events. SIEM correlation rules surface multi-signal incidents.</li>
      <li><strong>Tier severity</strong>: critical (immediate page) — escape-style rules. Warning (Slack) — informational rules. Info (log only) — audit-trail rules.</li>
      <li><strong>Auto-response</strong> (Tetragon enforce mode): kill process / block syscall on critical rules. Reserve for well-tested rules; over-aggressive auto-kill = self-DoS.</li>
    </ul>
    <p>The mature pattern: alert tier 1-3 + named runbooks; quarterly red-team exercise to verify alerts fire + on-call responds in budget.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="Which PSA profile drops ALL Linux capabilities + requires runAsNonRoot + seccompProfile?",
            options=[
                ("baseline", False),
                ("restricted", True),
                ("privileged", False),
            ],
            feedback="restricted is the strictest profile. baseline only blocks the worst (no privileged, no hostPath, etc.). restricted goes further: no capabilities at all, no root, seccomp required.",
        ),
        3: PauseCheck(
            question="A Pod is admitted (passed PSA Restricted) but a process inside calls <code>mount()</code>. What\'s the second layer?",
            options=[
                ("Re-run admission.", False),
                ("Falco or Tetragon eBPF rule alerts on mount() in container.", True),
                ("RBAC blocks the syscall.", False),
            ],
            feedback="Admission only validates Pod spec at submit time; runtime detection (Falco / Tetragon eBPF) is the layer that catches in-container behaviour like mount(), nsenter(), shell spawn. Two layers, two timeframes.",
        ),
    },
    before_after_before='<p>Pre-PSA / pre-runtime, clusters ran with no Pod-security gates and no syscall observability. Privileged Pods slipped in unnoticed; container escapes were undetectable; compromised workloads moved laterally without alerting. Compliance evidence relied on YAML inspection samples.</p>',
    before_after_after='<p>Modern clusters enforce PSA Restricted on every workload-namespace by default; runtime detection (Falco / Tetragon) attaches eBPF probes for escape attempts; alerts route through SIEM with severity tiers + runbooks. Two layers, complementary failure modes; compliance evidence is automatic + queryable.</p>',
    before_after_caption='<p class="ba-caption"><em>Admission stops 90% of misconfig at submit; runtime catches the rest + the live attacks. Skip either layer and the cluster has a blind spot.</em></p>',
    analogy_intro_html='''<p>The Mandatory-Helmet Zones mark every quarter of the citadel where standard kit must be worn. The <strong>privileged area</strong> is the staff-only zone (kube-system) where workers carry tools that would be dangerous outside it. The <strong>baseline area</strong> requires basic helmets — no spiked clubs, no climbing the walls, no reaching outside the citadel for tools. The <strong>restricted area</strong> requires full kit — gloves, lockable boots, sealed gauntlets — drop ALL extra capabilities, run as a non-elevated visitor.</p>
    <p>Beyond the helmet check, the citadel\'s walls have <strong>silent observers</strong> (Falco / Tetragon eBPF probes) watching every gesture inside. They alert on motions that pass the gate but are suspicious in the room — opening a sealed crate (mount), shouting outside the building (unexpected network), wandering toward the keep (privilege escalation).</p>
    <p>The migration is gradual: walk every quarter, find which workers don\'t fit the new kit, fix or exempt them, then enforce. Quarter by quarter the entire citadel goes restricted.</p>''',
    translation_rows=[
        ("Staff-only zone (tools allowed)", "PSA privileged profile (kube-system, system agents)"),
        ("Basic helmet zone", "PSA baseline (no privileged / hostPath / hostNet)"),
        ("Full kit zone", "PSA restricted (drop ALL caps + runAsNonRoot + seccomp)"),
        ("Helmet inspector at every door", "Pod Security Admission webhook"),
        ("Three inspection modes", "audit / warn / enforce per profile per namespace"),
        ("Silent observers in every room", "Falco / Tetragon eBPF probes"),
        ("Suspicious motion alarm", "Falco rule (shell-in-container, mount, write-to-etc)"),
        ("Real-time alarm-and-block", "Tetragon enforcement mode (kill / block syscall)"),
        ("Gradual quarter-by-quarter sweep", "Namespace-by-namespace PSA migration"),
    ],
    analogy_stops="A real helmet-zone is visible; PSA + runtime are policy + kernel-level — invisible until tested. Game-day exercises (deliberately deploy a privileged Pod or run a shell inside) are how you verify the controls fire.",
    eli5="Two safety officers at every quarter of the castle. The first checks at the door — no spikes, no climbing gear, no shouting outside. The second watches you inside — if you try to open a sealed crate or wander somewhere you shouldn\'t, an alarm rings. Your cluster has these two officers: PSA at admission, Falco / Tetragon at runtime.",
    eli10="<strong>PSA</strong>: namespace-level enforcement via labels (<code>pod-security.kubernetes.io/enforce: restricted</code>). Three profiles (privileged / baseline / restricted) × three modes (audit / warn / enforce). <strong>Migration</strong>: privileged → baseline → restricted, namespace by namespace, audit then warn then enforce. <strong>Falco</strong>: eBPF syscall watch + rules engine; CNCF Graduated; large rule library. <strong>Tetragon</strong>: Cilium-native eBPF; lower overhead + can enforce (kill / block) not just observe. <strong>Pipeline</strong>: events → SIEM → tiered alerts → on-call runbooks.",
    scenarios=[
        Scenario(
            name="Greenfield cluster — restricted from day one",
            body="A new cluster ships with cluster-wide default <code>enforce: restricted</code>; <code>kube-system</code> + monitoring exempt to <code>privileged</code>. Workload teams write Pods that pass restricted from day one. Falco runs as DaemonSet; alerts route to Slack + PagerDuty. Day-1 security baseline is the cluster\'s baseline.",
        ),
        Scenario(
            name="Brownfield migration — 90 namespaces, 18 months",
            body="A 100-engineer org with 90 prod namespaces. Phase 1 (3 months): audit every namespace; build inventory of privileged Pods. Phase 2 (6 months): warn baseline cluster-wide; teams migrate offenders. Phase 3 (3 months): enforce baseline. Phase 4 (6 months): warn + enforce restricted. <em>18 months but every cluster ends restricted.</em>",
        ),
        Scenario(
            name="Runtime catch — crypto-miner",
            body="A compromised dev image silently launched a crypto-miner. Falco rule \"unexpected outbound network to mining-pool CIDRs\" fired within 5 minutes; on-call killed the Pod via runbook; root caused a vulnerable transitive dep. <em>PSA didn\'t catch it (the Pod spec was clean); runtime did.</em>",
        ),
        Scenario(
            name="Outage — restricted enforced without runAsNonRoot fixes",
            body="A team flipped enforce: restricted on a namespace whose images ran as root. Every Pod failed admission; Service down. Postmortem: should have run audit + warn for 4 weeks first; image rebuilds for non-root user; ship in waves. Runbook updated.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"PSA Restricted is enough; we don\'t need runtime detection.\"",
            truth="Admission validates the <em>spec</em> at submit time. A Pod that\'s spec-clean but exploits a kernel CVE for container escape passes admission and breaks out at runtime. PSA + runtime are complementary; neither alone catches the full failure surface.",
        ),
        Misconception(
            myth="\"Falco is too noisy; we tried it once and disabled it.\"",
            truth="Default Falco rules need tuning for any environment. <em>Suppression rules + severity tiers + named runbooks</em> turn Falco from noise into signal. Skip tuning and yes, it\'s noisy. Spend two weeks tuning and it\'s the lighthouse you\'ve always wanted.",
        ),
        Misconception(
            myth="\"Tetragon replaces Falco.\"",
            truth="They overlap but solve subtly different things. <strong>Falco</strong> = mature, broad rule library, ecosystem of integrations. <strong>Tetragon</strong> = kernel-level eBPF, lower overhead, can enforce. Many clusters run both: Falco general-purpose, Tetragon for specific high-rps workloads or enforcement.",
        ),
    ],
    flashcards=[
        Flashcard(front="Three PSA profiles?", back="<strong>privileged</strong> (no restriction; legacy / system), <strong>baseline</strong> (no privileged / hostPath / hostNet / privilege-escalation), <strong>restricted</strong> (drop ALL caps, runAsNonRoot, seccompProfile required)."),
        Flashcard(front="How is PSA configured per namespace?", back="Namespace labels: <code>pod-security.kubernetes.io/enforce: restricted</code>, <code>...warn: restricted</code>, <code>...audit: restricted</code>. Three modes orthogonal."),
        Flashcard(front="Migration order from privileged → restricted?", back="<strong>Audit</strong> cluster (find offenders) → <strong>warn baseline</strong> per namespace → fix → <strong>enforce baseline</strong> → <strong>warn restricted</strong> → fix non-root issues → <strong>enforce restricted</strong>. Cluster default last."),
        Flashcard(front="What does Falco watch?", back="Linux syscalls (via eBPF or kernel module) + K8s audit events + container events. Rules engine matches against built-in + custom rules; emits alerts."),
        Flashcard(front="Tetragon advantage over Falco?", back="(1) Pure eBPF — lower kernel overhead at high syscall volumes. (2) Can <em>enforce</em> — kill process, block syscall — not just observe. (3) Cilium-native — integrates with Cilium NetworkPolicy + Hubble. Trade: newer, smaller rule library."),
        Flashcard(front="Common Falco rules to enable?", back="Shell spawned in container; mount() inside container; write to /etc /bin /sbin; ptrace inside container; capability NET_RAW used; outbound to unexpected CIDR; suspicious process names (miners, scanners)."),
        Flashcard(front="Why audit + warn + enforce phases for PSA?", back="Audit finds workloads that would fail without breaking them. Warn surfaces failures to teams via kubectl output for self-service fix. Enforce blocks. Skip phases = production outages from policy that\'s right in theory + wrong in practice."),
        Flashcard(front="Falcosidekick — what is it?", back="Event router for Falco. Receives Falco events; routes to 50+ destinations (Slack / Teams / PagerDuty / Loki / Splunk / Kafka / S3 / etc.). Glue between detection + alert pipelines."),
    ],
    quizzes=[
        Quiz(
            prompt="A new namespace is added for a third-party software vendor that requires hostPath mounts. The cluster default is restricted. How do you handle this cleanly?",
            answer="(1) <strong>Confirm the requirement</strong>: hostPath is rare; verify the vendor genuinely needs it (often requested out of habit; alternatives like CSI volumes, projected volumes, EmptyDir suffice). (2) <strong>Quarantine namespace</strong>: label the new namespace with <code>pod-security.kubernetes.io/enforce: privileged</code> + <code>warn: privileged</code> — vendor workload runs; rest of cluster stays restricted. (3) <strong>Compensating controls</strong>: tighter NetworkPolicy on the namespace; runtime detection rules tuned for the vendor\'s expected behaviour; audit log monitoring for unexpected actions. (4) <strong>Document</strong>: a per-namespace exception register tracked in Git; re-review quarterly. (5) <strong>Push back</strong>: if the vendor adds capabilities later, can it migrate to baseline or restricted? Most vendors can with image rebuilds.",
        ),
        Quiz(
            prompt="A Falco alert fires: \"shell spawned in container.\" On-call investigates. Walk through diagnostic steps.",
            answer="(1) <strong>Read the alert detail</strong>: pod, namespace, parent process, command. (2) <strong>Source check</strong>: was this an authorised <code>kubectl exec</code> by an SRE? Falco includes the K8s context — if exec by an authenticated SRE during business hours, suppress; consider scoping the rule to exclude exec by named groups. (3) <strong>If unexpected</strong>: <code>kubectl describe pod</code> + check recent deploys; was a new image pushed? Pull the audit log for the namespace. (4) <strong>Isolate</strong>: cordon the node? <code>kubectl exec</code> into the Pod with the runbook\'s investigative kit (or use ECS Exec equivalent in cluster) — check process list, network connections, file changes. (5) <strong>Containment</strong>: if compromise confirmed, scale Service to zero, snapshot the Pod\'s state for forensics, replace from clean image. (6) <strong>Postmortem</strong>: how did the attacker get shell? Image vuln? Exposed credential? Update controls.",
        ),
        Quiz(
            prompt="Leadership asks: \"PSA Restricted blocks too many workloads — let\'s set the default to baseline cluster-wide and call it done.\" Defend pushing through to restricted.",
            answer="\"<strong>Baseline catches the worst — privileged, hostPath, hostNet — but leaves real attack surface open.</strong> Three reasons restricted is worth the migration cost: (1) <strong>Capabilities</strong>: baseline still allows containers to add capabilities like NET_RAW or SYS_ADMIN that enable attacks. Restricted drops all by default; teams add specific ones with justification. (2) <strong>Run-as-root</strong>: baseline doesn\'t require runAsNonRoot. Many container CVEs need root inside the container to exploit; running as non-root substantially reduces blast radius. (3) <strong>seccompProfile</strong>: restricted requires explicit seccomp; many syscalls are filtered out by default — closes another exploit class. <strong>The migration cost</strong>: image rebuilds for non-root user, capability narrowing, seccomp profile picking. Real work, but: (a) it\'s one-time, (b) baseline has accumulated tech debt anyway, (c) every restricted-passing image is a clean image. <strong>The right framing: baseline is the price of entry to operating a K8s cluster; restricted is the operational standard for workloads. We aim for restricted by quarter\'s end.</strong>\"",
            cyoa=True,
            cyoa_tag="how the security architect pushed through to restricted",
        ),
    ],
    glossary=[
        GlossaryItem(name="Pod Security Admission (PSA)", definition="K8s built-in admission controller enforcing Pod-spec safety profiles via namespace labels."),
        GlossaryItem(name="PSA privileged profile", definition="No restriction. For system namespaces (kube-system, agents). Default for legacy clusters."),
        GlossaryItem(name="PSA baseline profile", definition="No privileged / hostPath / hostNet / privilege-escalation / NET_RAW. Cluster minimum bar."),
        GlossaryItem(name="PSA restricted profile", definition="Strictest: drop ALL capabilities, runAsNonRoot, seccompProfile required, allowPrivilegeEscalation false."),
        GlossaryItem(name="Falco", definition="CNCF Graduated runtime detection — eBPF or kernel-module syscall watch with rules engine + alerts."),
        GlossaryItem(name="Tetragon", definition="Cilium project; pure-eBPF runtime detection + enforcement (kill / block). Lower overhead at high syscall volumes."),
        GlossaryItem(name="seccompProfile", definition="Linux syscall filter for a container; PSA restricted requires either RuntimeDefault or Localhost."),
        GlossaryItem(name="Falcosidekick", definition="Event router for Falco — sends events to 50+ destinations (Slack, PagerDuty, Loki, S3, etc.)."),
        GlossaryItem(name="kube-no-trouble / kubescape", definition="Audit tools — find Pods that would fail PSA baseline / restricted; useful for migration prep."),
        GlossaryItem(name="Kyverno PSS pack", definition="Pre-built Kyverno ClusterPolicies implementing PSA-equivalent enforcement + reporting."),
    ],
    recap_lead="Two complementary layers: PSA at admission, Falco / Tetragon at runtime. PSA migration is privileged → baseline → restricted, namespace by namespace, audit → warn → enforce. Runtime detection requires tuning + a real alert pipeline; without that it\'s noise.",
    recap_next='<strong>Next — S5: Image Signing + SBOM + SLSA + in-toto + VEX.</strong> Cosign signing in CI; SLSA L3+ provenance attestation; SBOM (CycloneDX / SPDX); VEX vulnerability disposition; cluster-side admission verification.',
)
