from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Complete homestead: a finished property with main house, well, fence, watchtower, outbuildings, and a posted plaque listing the K-VAN stack.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">COMPLETE HOMESTEAD · CAPSTONE</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">REFERENCE STACK · TALOS + CILIUM + ARGO CD</text>
    <rect x="14" y="34" width="110" height="34" rx="3" fill="#3F4A5E"/><text x="69" y="50" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">Talos Linux</text><text x="69" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">immutable hosts</text>
    <rect x="130" y="34" width="110" height="34" rx="3" fill="#A04832"/><text x="185" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">3 CP + 3 worker</text><text x="185" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">stacked etcd</text>
    <rect x="246" y="34" width="110" height="34" rx="3" fill="#5A9F7A"/><text x="301" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">Cilium</text><text x="301" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">eBPF + Hubble</text>
    <rect x="362" y="34" width="110" height="34" rx="3" fill="#E8B547"/><text x="417" y="50" text-anchor="middle" font-size="9" fill="#5A4F45" font-weight="700">Gateway API</text><text x="417" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">Cilium Gateway</text>
    <rect x="478" y="34" width="110" height="34" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="533" y="50" text-anchor="middle" font-size="9" fill="#8B5A00" font-weight="700">cert-manager</text>
    <rect x="14" y="76" width="110" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="69" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">Velero</text><text x="69" y="104" text-anchor="middle" font-size="7" fill="#5A4F45">backup S3</text>
    <rect x="130" y="76" width="110" height="34" rx="3" fill="#E0EEF3" stroke="#4A8FA8"/><text x="185" y="92" text-anchor="middle" font-size="9" fill="#3F4A5E" font-weight="700">Prometheus</text><text x="185" y="104" text-anchor="middle" font-size="7" fill="#5A4F45">+ Grafana + AM</text>
    <rect x="246" y="76" width="110" height="34" rx="3" fill="#3F4A5E"/><text x="301" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">Argo CD</text><text x="301" y="104" text-anchor="middle" font-size="7" fill="#FBF1D6">App-of-Apps</text>
    <rect x="362" y="76" width="110" height="34" rx="3" fill="#5A9F7A"/><text x="417" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">Falco + Kyverno</text>
    <rect x="478" y="76" width="110" height="34" rx="3" fill="#A04832"/><text x="533" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">runbooks</text><text x="533" y="104" text-anchor="middle" font-size="7" fill="#FBE8DC">DR + upgrade</text>
    <rect x="14" y="118" width="572" height="34" rx="3" fill="#5A9F7A"/><text x="300" y="138" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">capstone deliverables: working cluster + git repo + DR runbook + upgrade runbook</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="11",
    title_short="capstone homestead",
    title_full="V11 · Capstone — Build, Harden, Back Up, Upgrade, Recover an HA Cluster",
    title_html="K-VAN V11 · Capstone Homestead",
    module_eyebrow="Module V11 · the complete homestead",
    hero_sub_html='<strong>Tie everything together.</strong> Build an HA on-prem cluster from scratch using the reference stack: Talos + Cilium + Gateway API + cert-manager + Velero + kube-prometheus-stack + Argo CD. Harden, back up, upgrade, recover. Produce runbooks. Defend it.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Two weeks before launch, your team realises: nobody has end-to-end built this stack. They\'ve installed pieces. They haven\'t been through V1 → V10 in sequence with a working cluster at the end. The capstone is the safeguard — finishing K-VAN means you\'ve <em>actually done it</em>, with the receipts (a working cluster, the git repo, the runbooks).',
    stamp_html='<strong>Capstone deliverables</strong>: (1) Working 6-node HA cluster on Talos with the reference stack. (2) Git repo (Argo CD App-of-Apps) reproducing the cluster from scratch. (3) etcd snapshot + Velero backup tested. (4) Documented upgrade rehearsal runbook. (5) Documented DR runbook covering all 7 disasters from V10. (6) kube-bench score &gt; 95%. <strong>You\'re K-VAN-complete when you can teach someone else to do it.</strong>',
    district_pin="kf-site11",
    district_label="Complete Homestead",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What \"capstone\" means here",
            body_html="""    <p>K-VAN is 10 modules of how. The capstone is one module of <em>do</em>: a single end-to-end project that exercises every prior module in sequence. You\'ll come out the other side with a working cluster you can defend in an interview, a runbook library, and the muscle memory to do it again on another network.</p>
    <p>The reference stack is opinionated to keep the project tractable: Talos (immutable OS, no SSH, fast bootstrap), Cilium (modern CNI), Gateway API (the future of ingress), cert-manager (TLS), Velero (backup), kube-prometheus-stack (monitoring), Argo CD (GitOps). You can sub equivalents if your environment demands it (RKE2 instead of Talos, Calico instead of Cilium) — the modules will still apply.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Phase A — Architecture + Build",
            h2="V1-V4 in sequence",
            body_html="""    <p><strong>A.1 Architecture document</strong> (V1). One page covering: 6 nodes (3 CP + 3 worker), Talos OS, Cilium CNI, stacked etcd, Pod CIDR <code>192.168.224.0/20</code>, Service CIDR <code>10.96.0.0/12</code>, kube-vip for API LB at 192.168.1.100, Longhorn CSI, Velero backup to S3, Argo CD GitOps, kube-bench scoring target ≥ 95%. Commit to git as <code>docs/architecture.md</code>.</p>
    <p><strong>A.2 Provision 6 VMs</strong> with Talos image + machine-config (V2 collapses to applying the config). Each node\'s machine-config sets kernel modules, sysctl, runtime, swap-off — all baked into the OS image. <code>talosctl apply-config</code> on each.</p>
    <p><strong>A.3 Bootstrap the cluster</strong> (V3 via Talos, not kubeadm): <code>talosctl bootstrap --nodes &lt;cp-1-ip&gt;</code> on the first CP node; the others auto-join via the machine-config. kube-vip runs as a Talos extension or a static pod. Cluster comes up in 2-3 minutes.</p>
    <p><strong>A.4 Install Cilium</strong> (V4): Helm install with <code>kubeProxyReplacement=true</code>, native routing, Hubble enabled, MTU verified. <code>cilium connectivity test</code> passes.</p>
    <p>Verify: <code>kubectl get nodes</code> all 6 Ready.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Phase B — Add-ons + Hardening",
            h2="V5, V6, V9 in sequence",
            body_html="""    <p><strong>B.1 Bootstrap Argo CD</strong>: helm install argocd; create the App-of-Apps root pointing at <code>k8s-platform/apps/</code> in the git repo. Argo CD installs:</p>
    <ul>
      <li>cert-manager + ClusterIssuer (Let\'s Encrypt staging for the lab)</li>
      <li>Cilium Gateway controller (already part of Cilium, register Gateway API CRDs)</li>
      <li>Longhorn CSI + snapshot-controller</li>
      <li>Velero with the Longhorn snapshot plugin + S3 (or MinIO) target</li>
      <li>kube-prometheus-stack with Grafana exposed via Gateway</li>
      <li>Loki + Vector for logs</li>
      <li>Kyverno (policies) + Falco (runtime)</li>
      <li>kube-bench as a daily CronJob, output to PolicyReport</li>
    </ul>
    <p><strong>B.2 Cluster config</strong> (V6): apply your kubeadm/Talos cluster config additions: audit log on, KMS v2 encryption with Vault Transit (or static AES for the lab), systemReserved + kubeReserved on every node, scheduler bin-pack profile available, RuntimeClass for kata.</p>
    <p><strong>B.3 Hardening</strong> (V9): label every namespace with <code>pod-security.kubernetes.io/enforce: restricted</code> (or baseline). Apply default-deny BANP. Apply Kyverno verifyImages policy in audit mode (move to enforce after a soak). Run kube-bench; investigate FAILs; aim for ≥ 95% Level 1 PASS.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Phase C — Backup, Upgrade, DR Runbooks",
            h2="V7, V8, V10 in sequence + writeup",
            body_html="""    <p><strong>C.1 etcd snapshots</strong> (V7): Talos has a built-in etcd-snapshot path; configure machine-config to snapshot every 30 min and ship to S3. Verify with <code>talosctl etcd snapshot save</code>.</p>
    <p><strong>C.2 Velero backup</strong>: schedule <code>nightly</code> at 02:00; include all namespaces; include PV snapshots; retain 30 days.</p>
    <p><strong>C.3 Upgrade rehearsal</strong> (V8): plan an upgrade from current Talos / K8s minor → next. On the staging clone (or a Vagrant lab): apply the upgrade. Document what broke + what to do differently. Output: <code>docs/runbooks/upgrade-vX-to-vY.md</code>.</p>
    <p><strong>C.4 DR drills</strong> (V10): run all seven scenarios from V10 on the staging cluster. Document each recovery in a separate runbook file. Output: <code>docs/runbooks/dr-{cert-expiry,cni-broken,coredns,apiserver-down,etcd-quorum,webhook-lockout,namespace-restore}.md</code>.</p>
    <p><strong>C.5 Final review</strong>: walk a colleague through the architecture doc, the git repo, the runbooks, kube-bench score. They should be able to reproduce the cluster from scratch using your artifacts. <strong>That\'s the K-VAN bar</strong>.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>If you have time + capacity: build the cluster on real hardware (3 NUCs + 3 mini-PCs, ~$3K total). Operating physical infra adds the rack, power, network, BMC, console-server experience that VMs hide. Worth doing once for the muscle memory.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='You finish Phase A but Argo CD won\'t install — Helm fails because "no available CSI driver." Diagnosis?',
            options=[
                ('a) Argo CD has a known bug', False),
                ('b) Argo CD\'s redis component requests a PVC; no StorageClass exists yet because the CSI driver hasn\'t been installed. Order matters: install Longhorn CSI before Argo CD, or use Argo CD with emptyDir instead of PVC for the bootstrap', True),
                ('c) The cluster needs more memory', False),
            ],
            feedback='<strong>Answer: b.</strong> Add-on dependencies form an order: CNI → CoreDNS → CSI → cert-manager → ingress → Argo CD → everything else (which Argo CD then installs). Or use Argo CD\'s in-memory Redis bootstrap, then have it reconfigure to PV after CSI is up. Either is valid; document which approach in the runbook.',
        ),
    },
    before_after_before='<p>You finished K-COM and read all 10 K-VAN modules. You haven\'t built end-to-end. There\'s a gap between knowing and doing — and you only find it when something breaks under pressure.</p>',
    before_after_after='<p>You\'ve built the reference cluster. You\'ve broken it on purpose and recovered each disaster. Your git repo + runbooks let a colleague reproduce the work in a day. You can defend any choice in an interview. <strong>K-VAN-complete</strong>.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">The capstone exists so the gap between knowing and doing is closed deliberately, not by surprise in production.</p>',
    analogy_intro_html='<p>The Complete Homestead is the eleventh and final site on the K-Frontier map. The Drafting Hut produced the blueprint; the Land Clearing prepared the ground; the Frame went up; the Wiring went in; the Outbuildings clustered around the main house; the Rules Board was posted; the Well was drilled deep; the Renovation routine was practiced; the Watchtower was staffed; the Drill Square saw quarterly fires controlled. Now you stand in front of the gate, the deed in one hand, the keys in the other. The plaque on the post lists the stack. Inside the house: the runbook library, the architecture doc, the kube-bench scorecard. You can defend it to the inspector. You can leave it to the next homesteader. <strong>That\'s K-VAN complete</strong>.</p>',
    translation_rows=[
        ('The full deed of the homestead', 'Architecture document in git'),
        ('The keys to every outbuilding', 'kubeconfig + RBAC bindings'),
        ('Plaque on the post', 'Cluster bill of materials (versions, components)'),
        ('Library of runbooks', 'docs/runbooks/ in git'),
        ('Drill scoreboard on the wall', 'kube-bench Grafana dashboard'),
        ('Backup well drilled + tested', 'etcd snapshots + Velero + DR drill'),
        ('Renovation calendar pinned to the door', 'Quarterly upgrade cadence'),
        ('Sealed envelope: emergency keys', 'Break-glass admin procedure'),
        ('Property survey + inspector approval', 'kube-bench score + audit log review'),
    ],
    analogy_stops="The analogy stops here: the homestead is a one-time build; clusters are continuously evolving. K-VAN-complete means \"you can build + operate + defend\" — not \"you\'re done forever.\" The next K8s minor is always coming.",
    eli5='You\'ve been learning to build a house the hard way. Now you build the whole house, lock it down, set up the alarms, write down what to do in a fire — and prove someone else could do it from your notes.',
    eli10="Capstone: build a working 6-node HA cluster end-to-end on Talos + Cilium + Gateway API + cert-manager + Velero + kube-prometheus-stack + Argo CD, hardened to kube-bench &gt; 95%. Phase A: architecture doc + Talos bootstrap + Cilium. Phase B: Argo CD App-of-Apps for all add-ons + cluster config + PSA + Kyverno + Falco. Phase C: etcd snapshots + Velero + upgrade rehearsal + 7 DR runbooks. Final review: a colleague can reproduce from your artifacts. K-VAN-complete.",
    scenarios=[
        Scenario(name='A team finishing K-VAN as their pre-prod milestone', body='6 weeks of dedicated time. Vagrant + libvirt for local dev cluster; bare-metal NUCs for a real cluster. Final demo: chaos-day on the lab cluster recovering all 7 V10 scenarios in front of the team. Clear "we can do this in production" signal.'),
        Scenario(name='A bank using K-VAN graduates as the SRE pool', body='Anyone running the production K8s clusters has finished K-VAN. Demonstrates: built the reference cluster, scored kube-bench &gt; 95%, written the DR runbooks, walked a peer through. New hires onboarded by working through K-VAN with a buddy. Operational quality is hire-time + ongoing.'),
        Scenario(name='A startup choosing K-VAN over an EKS cert', body='Engineering manager: certifications validate trivia; K-VAN validates the work. New SRE candidates pair on the Talos build + Cilium install + Velero restore drill. The artifact (git repo + runbooks) is the interview portfolio.'),
        Scenario(name='An open-source contributor giving back', body='Used K-VAN to build their first self-managed cluster. Wrote a blog post documenting deviations (Calico instead of Cilium for FIPS reasons). PR\'d a typo fix in the K-VAN module. Cycle complete.'),
    ],
    misconceptions=[
        Misconception(myth='\"The capstone is optional / nice-to-have.\"', truth='K-VAN-complete means built end-to-end. Reading the modules without doing the capstone is K-VAN-read, not K-VAN-done. Different skill level.'),
        Misconception(myth='\"You need real hardware to do K-VAN properly.\"', truth='VMs work fine for the curriculum. Real hardware adds depth (BMC, network, console) but isn\'t required. If you have access to a few NUCs or rack space, take it; otherwise VMs.'),
        Misconception(myth='\"You can skip the runbooks if everything works.\"', truth='The runbooks ARE the deliverable. Working cluster without runbooks = you can\'t hand it off + you can\'t recover under pressure. Write them as you go, not after.'),
    ],
    flashcards=[
        Flashcard(front='Six K-VAN deliverables?', back='Architecture doc, working 6-node HA cluster, git repo (Argo CD App-of-Apps), etcd + Velero backups (tested), upgrade rehearsal runbook, 7 DR runbooks. Plus kube-bench score &gt; 95%.'),
        Flashcard(front='Reference stack components?', back='Talos Linux, 3 CP + 3 worker, stacked etcd, Cilium CNI + Gateway, cert-manager, Longhorn CSI, Velero, kube-prometheus-stack, Loki + Vector, Kyverno + Falco, Argo CD.'),
        Flashcard(front='Phase A milestones?', back='Architecture doc complete; 6 VMs provisioned with Talos + machine-config; cluster bootstrapped with kube-vip + stacked etcd; Cilium installed with kube-proxy replacement + Hubble; <code>kubectl get nodes</code> shows 6 Ready.'),
        Flashcard(front='Phase B milestones?', back='Argo CD installed + App-of-Apps reconciling all add-ons; cluster config tuned (audit + encryption + reserved); PSA + Kyverno + Falco enforcing; kube-bench &gt; 95%.'),
        Flashcard(front='Phase C milestones?', back='etcd snapshots scheduled + tested; Velero scheduled + restore tested; upgrade rehearsal documented; all 7 DR scenarios recovered + documented.'),
        Flashcard(front='How to know you\'re K-VAN-complete?', back='A colleague reproduces the cluster from your artifacts (git + runbooks + architecture doc) without help. They recover at least one disaster using your runbook only. Score = pass.'),
        Flashcard(front='Reference stack alternatives?', back='RKE2 instead of Talos (regulated). Calico instead of Cilium (BGP / FIPS). HAProxy + keepalived instead of kube-vip (large org). Same modules apply; substitute components.'),
        Flashcard(front='Time investment?', back='4-6 weeks of focused work for a single engineer + reviewer pair. Less if your org has previous K-VAN graduates to mentor. More if doing in spare time alongside other duties.'),
    ],
    quizzes=[
        Quiz(prompt='You\'ve finished Phase A and B. The cluster works; kube-bench is at 96%. You start Phase C\'s upgrade rehearsal: <code>talosctl upgrade --image talos:v1.x</code> on cp-1. After 5 min, cp-1 is unreachable. The other CP nodes still serve the API. What now?', answer='<strong>Diagnose first; don\'t reboot.</strong> <strong>(1)</strong> <code>talosctl --nodes cp-1 dmesg</code> + <code>service-control logs</code>. Talos surfaces config errors here. <strong>(2)</strong> Common: machine-config drift (the new image expects different sysctls or kernel modules). Fix the machine-config; <code>talosctl apply-config --insecure</code> while the node is still bootloader-stage. <strong>(3)</strong> If physically wedged: <code>talosctl reset</code> (factory reset) and re-bootstrap. The cluster\'s remaining 2 CPs hold quorum + serve traffic. <strong>(4) Document.</strong> What broke? What was missing from the upgrade procedure? Update <code>docs/runbooks/upgrade-vX-to-vY.md</code> with the finding. <strong>This is the value of a rehearsal:</strong> finding the gap when only one CP is at risk + you have 2 healthy ones. Never first-time-in-production.'),
        Quiz(prompt='Your Phase C\'s DR drill of "namespace deleted" finds: Velero restore brings everything back, but two Pods crash-loop on startup with config errors. Diagnosis?', answer='<strong>Restore-time race condition.</strong> Pods came up before their dependent ConfigMaps / Secrets were fully restored. Solution patterns: (1) <strong>Restore order</strong>: Velero supports restore hooks; configure to apply ConfigMaps + Secrets first, then Deployments. (2) <strong>Pod restart loops resolve themselves</strong> as kubelet retries; if the dependent resources eventually exist, the Pods recover. Often this resolves within 1-2 retry cycles (~60s). (3) <strong>If they never recover</strong>: check the Pod manifest for <code>configMapKeyRef</code> / <code>secretKeyRef</code> pointing at keys that don\'t match the restored ConfigMap (e.g., key renamed since backup). Rare; happens with old backups. <strong>Lesson:</strong> the DR drill exposes ordering bugs that production never showed. Document the restore procedure including the wait + observe step. Don\'t Velero-restore + leave; Velero-restore + verify each app\'s readiness.'),
        Quiz(prompt='You\'re the senior engineer reviewing a colleague\'s K-VAN capstone submission. <strong>Click for the rubric. ▼</strong>', cyoa=True, cyoa_tag='the rubric', answer='<strong>(1) Architecture doc clarity.</strong> One page; covers sizing, network plan, OS, runtime, CNI, CSI, HA topology, backup, upgrade, security baseline. Decisions justified, not just listed. <strong>(2) Working cluster.</strong> 6 nodes Ready; control plane HA-tested (kill cp-1, verify cluster keeps working); Cilium connectivity test passes; Hubble shows flows. <strong>(3) Git repo.</strong> Argo CD App-of-Apps reconciles every add-on; pinned versions; per-environment overlays. Reproducibility test: deploy to a fresh K8s cluster from the repo; should come up identically. <strong>(4) Backups tested.</strong> Velero restore on a fresh namespace works; etcd snapshot restore on a fresh cluster works; both timed end-to-end. <strong>(5) Upgrade rehearsal documented.</strong> Walked a minor-version upgrade end-to-end; surprises captured; runbook updated. <strong>(6) DR runbooks.</strong> Seven scenarios from V10; each tested; each runbook is reproducible by another engineer. <strong>(7) kube-bench score &gt; 95%.</strong> Documented exceptions for the remaining FAILs. <strong>(8) Defense.</strong> The colleague walks me through any decision I question; reasoning is solid. <strong>(9) Demo.</strong> Live: I introduce a chaos failure on the lab cluster; they recover blind, without help, in &lt; 30 min, using their runbook. <strong>If all 9 pass:</strong> K-VAN-complete. <strong>Common failure modes:</strong> "works but undocumented", "documented but unreproducible", "reproducible but no DR drilled". Each is the thin slice between knowing + doing.'),
    ],
    glossary=[
        GlossaryItem(name='Capstone', definition='Final K-VAN module. End-to-end project tying every prior module to a working artifact.'),
        GlossaryItem(name='Reference stack', definition='Opinionated K-VAN bill of materials: Talos + Cilium + Gateway + cert-manager + Velero + kube-prometheus-stack + Argo CD.'),
        GlossaryItem(name='K-VAN deliverables', definition='Architecture doc, working cluster, git repo, tested backups, upgrade runbook, 7 DR runbooks, kube-bench score &gt; 95%.'),
        GlossaryItem(name='Phase A (Build)', definition='V1-V4: architecture, OS, bootstrap, CNI. Cluster goes from blueprint to Ready.'),
        GlossaryItem(name='Phase B (Stack + Hardening)', definition='V5, V6, V9: Argo CD + add-ons, cluster config, hardening to baseline.'),
        GlossaryItem(name='Phase C (Resilience)', definition='V7, V8, V10: backups, upgrade rehearsal, 7 DR runbooks documented + tested.'),
        GlossaryItem(name='K-VAN-complete', definition='You can build, operate, harden, back up, upgrade, recover an HA cluster — and someone else can reproduce from your artifacts.'),
        GlossaryItem(name='Bare-metal capstone', definition='Optional: do the capstone on real hardware (NUCs / rack) for BMC + network + console depth.'),
        GlossaryItem(name='Pair review', definition='Final K-VAN gate: a peer reviews artifacts + watches a chaos drill. Score = pass / iterate.'),
        GlossaryItem(name='Substitute stack', definition='RKE2 instead of Talos; Calico instead of Cilium; same K-VAN modules apply with different components.'),
        GlossaryItem(name='Reproducibility test', definition='Deploy from your git repo to a fresh K8s cluster; should come up identically. Litmus test for "infra as code".'),
        GlossaryItem(name='Defense (interview-style)', definition='Walking through every decision; explaining tradeoffs; defending against alternatives. The K-VAN graduate test.'),
    ],
    recap_lead='Capstone = build the reference stack end-to-end + harden + back up + upgrade + DR-drill all 7 scenarios + produce runbooks. Working cluster + git repo + runbooks + defended decisions + reproduced by a peer = K-VAN-complete.',
    recap_next='<strong>Done.</strong> You\'ve walked the K-Frontier homestead from raw land to defendable property. K-VAN ends here; what comes next is operating real clusters with the muscle memory you built. The Drafting Hut on the next site is yours to design.',
)
