from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Renovation site: scaffolding around the homestead, sequence arrows showing CP -> kubelet -> kube-proxy -> workers -> add-ons -> CNI/CSI; rollback flag in case.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">RENOVATION · UPGRADES &amp; PATCHING</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">UPGRADE ORDER · v1.35 → v1.36</text>
    <rect x="14" y="34" width="110" height="34" rx="3" fill="#3F4A5E"/><text x="69" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">1 backup etcd</text><text x="69" y="62" text-anchor="middle" font-size="7" fill="#FBF1D6">snapshot save</text>
    <rect x="130" y="34" width="110" height="34" rx="3" fill="#A04832"/><text x="185" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">2 cp-1 (kubeadm)</text><text x="185" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">apiserver/scheduler/cm</text>
    <rect x="246" y="34" width="110" height="34" rx="3" fill="#A04832"/><text x="301" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">3 cp-2/3</text>
    <rect x="362" y="34" width="110" height="34" rx="3" fill="#5A9F7A"/><text x="417" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">4 kubelet (CP)</text>
    <rect x="478" y="34" width="110" height="34" rx="3" fill="#5A9F7A"/><text x="533" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">5 workers</text><text x="533" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">drain → kubeadm</text>
    <rect x="14" y="76" width="110" height="34" rx="3" fill="#E8B547"/><text x="69" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">6 add-ons</text>
    <rect x="130" y="76" width="110" height="34" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="185" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">7 CNI / CSI</text>
    <rect x="246" y="76" width="110" height="34" rx="3" fill="#E0EFE6" stroke="#3D7857"/><text x="301" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#3D7857">verify smoke</text>
    <rect x="362" y="76" width="226" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="475" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">rollback: kubeadm-config + etcd snapshot</text>
    <rect x="14" y="118" width="572" height="34" rx="3" fill="#3F4A5E"/><text x="300" y="134" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">version skew rule: kubelet may be at most 3 minor versions behind apiserver</text><text x="300" y="146" text-anchor="middle" font-size="7" fill="#FBE8DC">k8s release cadence: minor every 4 months · patch monthly · 14 months support</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="08",
    title_short="upgrades &amp; patching",
    title_full="V8 · Upgrades and Patching (kubeadm, version skew, rollback)",
    title_html="K-VAN V8 · Upgrades and Patching",
    module_eyebrow="Module V8 · the renovation site",
    hero_sub_html='K8s ships a new minor version every ~4 months and patches monthly. <strong>Skipping minors is dangerous</strong>; staying current is operational discipline. kubeadm has good upgrade tooling — but the order matters and rollback is limited.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='You upgrade the cluster and 30% of workloads break. Investigation: a CRD you depend on used <code>apiextensions.k8s.io/v1beta1</code> which was removed in v1.22; the operator hadn\'t been updated. Or: PodSecurityPolicy was removed in v1.25 + your namespaces still reference it. Or: your CSI driver requires a feature gate that flipped default. <em>Upgrades only feel routine when the prep work is done</em>. This module is the prep work.',
    stamp_html='K8s release cadence: <strong>minor every ~4 months</strong>, patches monthly, ~14 months support per minor. Version skew: <strong>kubelet ≤ apiserver, max 3 minors behind</strong>; never skip a minor on upgrade. Order: <strong>etcd snapshot → cp-1 (kubeadm upgrade apply) → cp-2/3 → kubelet on CP → workers (drain → upgrade → uncordon) → add-ons → CNI/CSI</strong>. Pre-upgrade: scan for deprecated APIs (kubectl convert, Pluto). Rollback: limited — backup-restore is the safety net.',
    district_pin="kf-site08",
    district_label="Renovation",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why upgrades scare people",
            body_html="""    <p>Three things make K8s upgrades different from other software:</p>
    <ul>
      <li><strong>Frequent minors.</strong> Three or four minor releases a year. Skipping is unsafe (can\'t go 1.32 → 1.36 in one shot — must be 1.32 → 1.33 → 1.34 → 1.35 → 1.36).</li>
      <li><strong>Multi-component coordination.</strong> Upgrade apiserver + controller-manager + scheduler + etcd + kubelets + kube-proxy + CNI + CSI + add-ons + CRDs. Each must work together and has its own version skew rules.</li>
      <li><strong>Limited rollback.</strong> kubeadm doesn\'t auto-rollback. The safety net is etcd snapshot + backup → cluster restore. Plan for upgrade-fail by having a tested restore.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.5 · Version skew",
            h2="Who can be how far ahead/behind whom",
            body_html="""    <ul>
      <li><strong>kube-apiserver</strong>: highest version. New minor first.</li>
      <li><strong>controller-manager / scheduler</strong>: ≤ apiserver. Same minor or one behind during transition.</li>
      <li><strong>kubelet</strong>: ≤ apiserver, may be up to 3 minors behind. Practical: don\'t leave kubelets behind by &gt; 1 minor.</li>
      <li><strong>kube-proxy</strong>: same minor as kubelet on its node.</li>
      <li><strong>kubectl</strong>: ±1 minor from apiserver.</li>
    </ul>
    <p>The skew rules let you upgrade the control plane first, then workers — without a hard cutover. A worker on v1.35 can keep talking to a v1.36 apiserver during the transition.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · The kubeadm upgrade flow",
            h2="One node at a time, control plane first",
            body_html="""    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># 0. Backup etcd snapshot (V7) — verify it's recent + tested
# 1. Plan
sudo kubeadm upgrade plan v1.36.0

# 2. On cp-1 — apply
sudo apt-get install -y kubeadm=1.36.0-1.1
sudo kubeadm upgrade apply v1.36.0

# 3. On cp-1 — kubelet + kubectl
sudo kubectl drain cp-1 --ignore-daemonsets --delete-emptydir-data
sudo apt-get install -y kubelet=1.36.0-1.1 kubectl=1.36.0-1.1
sudo systemctl daemon-reload && sudo systemctl restart kubelet
sudo kubectl uncordon cp-1

# 4. Repeat steps 2-3 on cp-2, cp-3 (with `kubeadm upgrade node`, not `apply`)
sudo apt-get install -y kubeadm=1.36.0-1.1
sudo kubeadm upgrade node
# ... drain + kubelet + uncordon

# 5. Workers — same drain → kubeadm upgrade node → kubelet → uncordon, one at a time
# 6. Add-ons — Argo CD detects new versions if you've bumped Helm chart values

# 7. CNI / CSI — typically on a different cadence; bump after K8s upgrade settles</code></pre>
    <p>Surge nodes (extra worker added before upgrade, removed after) make worker upgrades safer for capacity-sensitive clusters.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Pre-upgrade hygiene + rollback",
            h2="Detect breakage early; have a path back",
            body_html="""    <p><strong>Pre-upgrade:</strong></p>
    <ul>
      <li><strong>Scan for deprecated APIs</strong> in your manifests + git: <code>pluto detect-files -d &lt;dir&gt;</code> or <code>kubectl convert</code>. Removes are listed in each release\'s notes.</li>
      <li><strong>Check CRD compatibility:</strong> third-party operators often pin to a K8s version range. Check their docs.</li>
      <li><strong>Run upgrade on staging first.</strong> Same K8s minor, same add-on versions, same workloads. If it breaks there, fix before prod.</li>
      <li><strong>PodDisruptionBudgets</strong> on production workloads to prevent drain from taking too many replicas at once.</li>
      <li><strong>Backup-before-upgrade:</strong> fresh etcd snapshot, fresh Velero backup of all namespaces.</li>
    </ul>
    <p><strong>Rollback options</strong> (in increasing pain):</p>
    <ol>
      <li><strong>Per-component:</strong> downgrade kubelet/kubeadm packages on a node, restart. Limited (apiserver downgrade is more disruptive).</li>
      <li><strong>etcd restore:</strong> bring the cluster back to its pre-upgrade snapshot. All workloads come back to that state. Lose any post-upgrade work.</li>
      <li><strong>Blue-green clusters:</strong> the safest. Build the new cluster fresh at the new version, migrate workloads via GitOps, decommission the old. Twice the cost during cutover.</li>
    </ol>
    <p>For most teams: <strong>etcd restore is the rollback plan</strong>. Make sure you have a tested one.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For Talos: upgrades are a single <code>talosctl upgrade --image talos:v1.x</code> per node — the OS image is replaced + rebooted. Cluster API: declarative version bump in the Cluster manifest; CAPI rolls nodes. Different operational shape but same skew rules apply.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your cluster is on v1.32. You want to go to v1.36. Can you do it in one <code>kubeadm upgrade apply</code>?',
            options=[
                ('a) Yes — kubeadm handles multi-version jumps', False),
                ('b) No — must upgrade one minor at a time: 1.32 → 1.33 → 1.34 → 1.35 → 1.36 (each verified before the next)', True),
                ('c) Yes if you skip kubelet upgrade in between', False),
            ],
            feedback='<strong>Answer: b.</strong> kubeadm enforces +1 minor at most. Skipping risks API removals + storage migrations + skew violations. Plan a 1-minor-per-week cadence (or faster if your team has the muscle), with each step verified on staging first.',
        ),
    },
    before_after_before='<p>\"We\'ll upgrade later.\" 18 months pass. Cluster is now 4 minors behind. CVEs accumulate. Operators stop supporting the version. Upgrade requires going through 4 minors with all their breaking changes at once. Migration ends up being a cluster rebuild.</p>',
    before_after_after='<p>Quarterly upgrade cadence. Each upgrade rehearsed on staging the prior week. Pluto + kubectl convert in CI on every PR catches deprecated APIs before they ship. etcd snapshot + Velero backup before every upgrade. Rollback playbook drilled. Upgrades feel like routine maintenance.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">The cluster that doesn\'t upgrade routinely is the cluster that has to be rebuilt.</p>',
    analogy_intro_html='<p>The Renovation site sits next to the main house. Every season, the homesteader rolls in a new floor, replaces a worn beam, swaps the old roof for a better one. The work follows a strict order — you can\'t replace the roof before the rafters are stable. The contractor knows: <strong>foundation first</strong> (etcd snapshot), <strong>frame next</strong> (control plane), <strong>then floors</strong> (kubelets), <strong>then siding</strong> (workers), <strong>then fixtures</strong> (add-ons + CNI/CSI). And before any of it: <strong>backup the family heirlooms</strong> (etcd + Velero) in case the contractor falls through the floor.</p>',
    translation_rows=[
        ('Renovation calendar', 'K8s release cadence (~4 months/minor)'),
        ('"Foundation first"', 'etcd snapshot before upgrade'),
        ('Frame replacement', 'kubeadm upgrade apply on cp-1'),
        ('Mirror the new frame on the other corners', '<code>kubeadm upgrade node</code> on cp-2/3'),
        ('New floors over the same frame', 'kubelet upgrade on each node'),
        ('Siding (one wall at a time)', 'Worker drain → upgrade → uncordon'),
        ('Light fixtures + plumbing fittings', 'Add-ons + CNI / CSI'),
        ('Family heirlooms in storage', 'etcd snapshot + Velero backup before start'),
        ('Contractor\'s rollback van', 'Restore from snapshot if upgrade fails'),
    ],
    analogy_stops="The analogy stops here: real upgrades don't have nailguns. They have API deprecations, controller restarts, version skew rules, and YAML CRD migrations. The renovation feel undersells the precision needed.",
    eli5='Every few months, the house gets a renovation. Don\'t skip three years of renovations and try them all at once — do one per season. Save the family photos before the contractor starts, just in case.',
    eli10="K8s minors every ~4 months; patches monthly. Skew rule: kubelet may be ≤ 3 minors behind apiserver but never ahead. Upgrade order: etcd snapshot → cp-1 (kubeadm upgrade apply) → cp-2/3 → kubelet on CP → workers (drain + upgrade + uncordon) → add-ons → CNI/CSI. Pre-upgrade: scan for deprecated APIs (Pluto, kubectl convert), test on staging, take etcd snapshot + Velero backup. Rollback: per-component downgrade, etcd restore, or blue-green cluster.",
    scenarios=[
        Scenario(name='A SaaS doing quarterly upgrades', body='Calendar: week 1 = staging upgrade + soak. Week 2 = production CP. Week 3 = production workers. Week 4 = add-on bumps. Repeat next quarter. Upgrades feel boring. Pre-upgrade: Pluto runs in CI on every PR; deprecated APIs caught months before they bite.'),
        Scenario(name='A bank doing blue-green cluster upgrades', body='Build new cluster at v1.36. Migrate workloads via GitOps (Argo CD points at new cluster). Validate. Cut DNS + load balancer. Decommission old cluster. Twice the infra cost during cutover; zero in-place upgrade risk. Used for the most-critical clusters only.'),
        Scenario(name='A team that hit a 4-minor-behind upgrade', body='Cluster on v1.28 in early 2026 (now v1.36 era). Plan: skip n+1 strategy is unsafe, but they can\'t schedule 4 sequential upgrades. Adopted blue-green: built fresh v1.36 cluster, migrated workloads over 3 weeks via Argo CD, decommissioned old. Total project: 6 weeks; would have been 4-12 months of in-place upgrades + risk.'),
        Scenario(name='A team using kube-proxy mode change as an upgrade', body='K8s 1.31 added nftables mode for kube-proxy (β). Plan: upgrade cluster to 1.32 first; then on a soak weekend, change KubeProxyConfiguration mode iptables → nftables; restart kube-proxy; verify Service traffic still flows. Different from a K8s minor upgrade but follows the same staging-first pattern.'),
    ],
    misconceptions=[
        Misconception(myth='\"kubeadm rolls back automatically on failure.\"', truth='No. kubeadm does its best to be atomic per-node, but cluster-wide rollback is on you (snapshot restore or per-component downgrade). Plan for it.'),
        Misconception(myth='\"You can skip a minor if nothing in your workloads uses removed APIs.\"', truth='kubeadm itself enforces +1 minor max. The CRD + admission webhook compat + storage migration + scheduler / kubelet skew rules also assume incremental. Doing it in one shot has been seen to corrupt clusters.'),
        Misconception(myth='\"Patch versions are safe to skip.\"', truth='Mostly true, with exceptions: some patches fix CVEs you should not be running unpatched against. Stay current on patches; skip them only with eyes open.'),
    ],
    flashcards=[
        Flashcard(front='K8s release cadence?', back='Minor every ~4 months. Patches monthly. ~14 months of patch support per minor.'),
        Flashcard(front='Skew rules?', back='kubelet ≤ apiserver, max 3 minors behind. controller-manager/scheduler same minor as apiserver. kubectl ±1 minor.'),
        Flashcard(front='kubeadm upgrade order?', back='etcd snapshot → cp-1 (<code>kubeadm upgrade apply</code>) → cp-2/3 (<code>kubeadm upgrade node</code>) → kubelet on CP → workers (drain + upgrade + uncordon) → add-ons → CNI/CSI.'),
        Flashcard(front='Why drain a node before kubelet upgrade?', back='Kubelet restart kills its Pods briefly. Drain reschedules them onto other nodes first, respecting PodDisruptionBudgets. Without drain, you take random Pod outages.'),
        Flashcard(front='What is Pluto?', back='Tool from FairwindsOps that scans manifests for deprecated/removed K8s APIs. Run in CI to catch API regressions before upgrade.'),
        Flashcard(front='kubectl convert?', back='Subcommand of kubectl that converts manifests between API versions. Useful for migrating off deprecated APIs ahead of upgrade.'),
        Flashcard(front='Three rollback paths?', back='Per-component package downgrade (limited), etcd snapshot restore (cluster-wide), blue-green cluster (safest, costliest).'),
        Flashcard(front='Talos / CAPI upgrade differences?', back='Talos: <code>talosctl upgrade --image</code> per node — image-replacement, no kubeadm. CAPI: bump version in Cluster manifest; CAPI rolls Machines. Same skew rules; different mechanics.'),
    ],
    quizzes=[
        Quiz(prompt='Pre-upgrade scan flags 4 Deployments using <code>autoscaling/v2beta2</code> (removed in v1.26). Walk the remediation.', answer='<strong>(1) Identify owners.</strong> Each Deployment lives in a namespace; map to team. <strong>(2) Per-Deployment fix.</strong> Edit the HPA YAML: change <code>apiVersion: autoscaling/v2beta2</code> to <code>autoscaling/v2</code>. The schema is mostly compatible; sometimes field names changed (e.g., <code>targetCPUUtilizationPercentage</code> → <code>metrics</code>). Use <code>kubectl convert</code>: <code>kubectl convert -f hpa.yaml --output-version autoscaling/v2</code>. <strong>(3) PR + Argo CD diff review</strong> shows the exact change. <strong>(4) Apply on staging first.</strong> Validate HPA still scales. <strong>(5) Apply on production.</strong> <strong>(6) Re-run Pluto</strong> to confirm no remaining v2beta2 references. <strong>(7) Add a CI check</strong> that blocks PRs introducing deprecated APIs going forward. <strong>Total time:</strong> 1-2 sprints depending on team count + workload count. <strong>Lesson:</strong> deprecation scans should be running quarterly, not on the day of upgrade.'),
        Quiz(prompt='Your prod cluster upgrade hangs at \"upgrading kubelet on cp-1\" — 30 minutes in, no progress. Diagnose.', answer='<strong>Common causes:</strong> (1) <em>Image pull stuck</em>. The new kubelet/kube-apiserver/etc images aren\'t in the local containerd cache + the registry is unreachable. <code>crictl images</code> on cp-1 — empty? <code>journalctl -u containerd</code> for pull errors. (2) <em>etcd unhealthy</em>. The kubeadm upgrade waits for etcd; if etcd is degraded (slow disk, alarm), the upgrade hangs. <code>etcdctl endpoint health + status</code>. (3) <em>API server health-check failing</em>. The new apiserver static pod is up but failing readiness. <code>journalctl -u kubelet</code>; <code>kubectl logs -n kube-system kube-apiserver-cp-1</code>. <strong>Recovery:</strong> if you can identify + fix in &lt; 30 min, do. Otherwise, restore etcd snapshot + downgrade kubelet + kubeadm packages on cp-1 + restart kubelet to roll back to pre-upgrade state. Then debug on staging. <strong>Documentation:</strong> add the diagnosis path to the upgrade runbook.'),
        Quiz(prompt='You\'re asked to upgrade a 30-node cluster from v1.34 to v1.36. <strong>Click for the playbook. ▼</strong>', cyoa=True, cyoa_tag='the upgrade playbook', answer='<strong>Two minor versions = two upgrade cycles, each verified.</strong> <strong>Cycle A: 1.34 → 1.35.</strong> <strong>(A.1) Pre-flight</strong> — Pluto scan for v1.35 removals; staging upgrade succeeds; etcd snapshot + Velero backup taken. <strong>(A.2) Control plane</strong> — kubeadm upgrade apply on cp-1 (10 min); kubeadm upgrade node on cp-2, cp-3 (10 min each). <strong>(A.3) Kubelets on CP</strong> — drain + upgrade + uncordon on each (15 min each). <strong>(A.4) Workers</strong> — drain + kubeadm upgrade node + kubelet + uncordon on each, with PodDisruptionBudgets respected. 30 nodes × 10 min = 5 hrs. Run rolling, 3 in parallel where capacity allows. <strong>(A.5) Verify</strong> — <code>kubectl get nodes</code> all v1.35; smoke tests pass. <strong>Cycle B: 1.35 → 1.36.</strong> Repeat A.1-A.5. <strong>Add-ons + CNI + CSI</strong> bumped after both cycles complete; per their compat matrices. <strong>Total time:</strong> ~2 weekends if scheduled outside production load. <strong>Risk mitigation:</strong> if anything breaks at A.1-A.3, you have an etcd snapshot + a tested restore. If a worker upgrade fails, that node is cordoned + reportable; cluster is degraded by 1/30 nodes max. Beats one 4-minor leap by months.'),
    ],
    glossary=[
        GlossaryItem(name='K8s release cadence', definition='Minor versions every ~4 months. Patches monthly. ~14 months of support per minor.'),
        GlossaryItem(name='Version skew', definition='How far apart components can be. kubelet ≤ apiserver, max 3 minors behind. Practical: keep within 1 minor.'),
        GlossaryItem(name='kubeadm upgrade plan', definition='Subcommand: shows the available upgrade target + version skew check.'),
        GlossaryItem(name='kubeadm upgrade apply', definition='On the first CP node: upgrades cluster control plane to the target version.'),
        GlossaryItem(name='kubeadm upgrade node', definition='On subsequent CP nodes + workers: upgrades kubeadm-managed components on this node.'),
        GlossaryItem(name='Deprecated API', definition='K8s API marked for removal in a future version. Often replaced by a stable equivalent.'),
        GlossaryItem(name='Pluto', definition='FairwindsOps tool scanning manifests for deprecated/removed K8s APIs.'),
        GlossaryItem(name='kubectl convert', definition='Converts manifests between API versions. Useful for ahead-of-upgrade migration.'),
        GlossaryItem(name='Surge node', definition='Extra worker node added before drains to maintain capacity during upgrade.'),
        GlossaryItem(name='Blue-green cluster', definition='Build new cluster at new version; migrate workloads; decommission old. Safest upgrade pattern; costliest.'),
        GlossaryItem(name='PodDisruptionBudget', definition='Cap on simultaneous voluntary disruptions. Critical during drain/upgrade.'),
        GlossaryItem(name='Backup-before-upgrade', definition='Standard practice: fresh etcd snapshot + Velero backup before any upgrade work.'),
    ],
    recap_lead='Quarterly upgrades, one minor at a time. Order: etcd snapshot → cp-1 → cp-2/3 → CP kubelets → workers → add-ons → CNI/CSI. Pre-upgrade: deprecated-API scan + staging rehearsal. Rollback: snapshot restore.',
    recap_next='<strong>Next — V9: Security Hardening.</strong> CIS benchmark, RBAC least privilege, secret encryption, admission policy, image signing, runtime security, certificate rotation.',
)
