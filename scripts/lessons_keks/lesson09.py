from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Maintenance wing: timeline showing standard support, extended support, deprecation; sequence boxes - control plane, NG, Fargate, add-ons, CNI, EBS CSI; blue-green path on the side.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">MAINTENANCE WING · UPGRADES</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <rect x="14" y="34" width="572" height="22" rx="3" fill="#5A9F7A"/><text x="300" y="48" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">14 months standard support</text>
    <rect x="14" y="58" width="572" height="22" rx="3" fill="#E8B547"/><text x="300" y="72" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">+ 12 months extended support · $0.60/h premium</text>
    <rect x="14" y="84" width="100" height="34" rx="3" fill="#3F4A5E"/><text x="64" y="100" text-anchor="middle" font-size="8" fill="#FBF1D6" font-weight="700">control plane</text>
    <rect x="120" y="84" width="100" height="34" rx="3" fill="#A04832"/><text x="170" y="100" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">managed NG</text>
    <rect x="226" y="84" width="100" height="34" rx="3" fill="#A04832"/><text x="276" y="100" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">self-managed</text>
    <rect x="332" y="84" width="100" height="34" rx="3" fill="#A04832"/><text x="382" y="100" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">Fargate refresh</text>
    <rect x="438" y="84" width="148" height="34" rx="3" fill="#5A9F7A"/><text x="512" y="100" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">add-ons (CNI/CoreDNS/EBS)</text>
    <rect x="14" y="124" width="380" height="28" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="204" y="140" text-anchor="middle" font-size="8" font-weight="700" fill="#A04832">deprecated API scan: kubectl convert · Pluto</text>
    <rect x="400" y="124" width="186" height="28" rx="3" fill="#3F4A5E"/><text x="493" y="140" text-anchor="middle" font-size="8" fill="#FBF1D6" font-weight="700">blue-green cluster (high stakes)</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="09",
    title_short="upgrades &amp; ops",
    title_full="E9 · EKS Upgrades and Operations",
    title_html="K-EKS E9 · EKS Upgrades and Operations",
    module_eyebrow="Module E9 · the renovation wing",
    hero_sub_html='EKS gives you the standard K8s upgrade rules + AWS\'s 14-month standard / 12-month extended support window + a managed control-plane upgrade + lifecycle for Managed NG / Fargate / add-ons. Plus the option to do <strong>blue-green cluster migrations</strong> for high-stakes upgrades.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Cluster on K8s 1.31. AWS standard support ends in 2 weeks; extended kicks in at $0.60/hr (~$5K/year extra). Team\'s never upgraded. Blocked by: a custom Helm chart using <code>networking.k8s.io/v1beta1</code> (removed in 1.22), an operator pinned to 1.30, no upgrade rehearsal cluster. Recovery: budget extended support for now, schedule prep work, plan upgrade for next quarter. <em>Avoid this with quarterly upgrades</em>. This module is the discipline.',
    stamp_html='EKS upgrades: <strong>14 months standard support + 12 months extended support</strong> per minor. Order: <strong>(1) backup + scan</strong> (etcd snapshot equivalent doesn\'t exist; AWS handles control plane state — but Velero your workloads + scan with Pluto for deprecated APIs); <strong>(2) control plane</strong> (<code>aws eks update-cluster-version</code>; ~30-60 min, AWS handles); <strong>(3) Managed Node Groups</strong> (rolling drain via AWS); <strong>(4) Self-managed nodes</strong>; <strong>(5) Fargate Pod refresh</strong> (recreate Pods); <strong>(6) Add-ons</strong> (CNI, CoreDNS, kube-proxy, EBS / EFS CSI); <strong>(7) Verify</strong>. Blue-green cluster for high-stakes upgrades.',
    district_pin="ks-floor09",
    district_label="Maintenance Wing",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="EKS upgrade differences from vanilla K8s",
            body_html="""    <p>Vanilla K8s upgrades (K-VAN V8): you upgrade etcd snapshot → control plane → kubelets → workers → add-ons. Pure manual orchestration via kubeadm.</p>
    <p>EKS:</p>
    <ul>
      <li><strong>Control-plane upgrade</strong>: one API call (<code>aws eks update-cluster-version</code>); AWS rolls + manages. Takes 30-60 min; cluster API stays available throughout.</li>
      <li><strong>Managed Node Group upgrade</strong>: one API call per NG (<code>aws eks update-nodegroup-version</code>); AWS does rolling drain via the same lifecycle controller.</li>
      <li><strong>Fargate</strong>: no node version per se; new Pods get new platform version automatically. Existing Pods stay until naturally restarted; force-refresh by triggering rolling deploy.</li>
      <li><strong>Add-ons</strong> (VPC CNI, CoreDNS, kube-proxy, EBS / EFS CSI): managed-add-on versions tied to K8s versions. AWS Console / CLI to upgrade.</li>
      <li><strong>Self-managed nodes</strong>: same as K-VAN V8. You orchestrate the drain + rolling update.</li>
      <li><strong>EKS Auto Mode</strong>: AWS handles add-ons + nodes lifecycle. You don\'t touch them.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.5 · Version policy",
            h2="14 months standard + 12 months extended",
            body_html="""    <p>Per K8s minor: AWS provides <strong>14 months standard support</strong> at the regular $0.10/hour cluster fee. After that: <strong>12 months extended support</strong> at +$0.60/hour per cluster (~$5K/year extra). After extended ends: AWS forcibly upgrades your cluster (yes, really) — you don\'t want to be there.</p>
    <p>K8s minors release every ~4 months upstream; AWS lags by 1-2 months. So the standard support window covers ~3 minor versions out — plenty of time if you upgrade quarterly.</p>
    <p><strong>Track the lifecycle</strong>: <code>aws eks describe-cluster-versions --include-all</code> lists every version + dates. Set a calendar alert 60-90 days before standard support ends.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · The upgrade order",
            h2="Step-by-step",
            body_html="""    <ol>
      <li><strong>Pre-flight</strong>: scan manifests for deprecated APIs (<code>kubectl convert</code>, Pluto, kube-no-trouble). Check operator + Helm chart compatibility. Validate against staging cluster on the new version.</li>
      <li><strong>Backup</strong>: Velero backs up workloads + PVCs. AWS handles etcd internally; you don\'t snapshot it directly.</li>
      <li><strong>Control plane</strong>: <code>aws eks update-cluster-version --name prod --kubernetes-version 1.36</code>. AWS rolls in-place; ~30-60 min; API available.</li>
      <li><strong>Managed Node Groups</strong>: <code>aws eks update-nodegroup-version --cluster-name prod --nodegroup-name X</code>. AWS does rolling drain respecting PDBs. Repeat per NG.</li>
      <li><strong>Self-managed nodes</strong>: standard kubeadm-style drain + replace.</li>
      <li><strong>Fargate</strong>: trigger rolling deployment to recreate Pods on new platform version.</li>
      <li><strong>Add-ons</strong>: <code>aws eks update-addon --cluster-name prod --addon-name vpc-cni</code> per add-on. Order: kube-proxy → CoreDNS → VPC CNI → CSI drivers. (Consult docs for each version\'s required add-on combination.)</li>
      <li><strong>Verify</strong>: smoke tests, dashboards, Pod health.</li>
    </ol>""",
        ),
        Section(
            eyebrow="Section 1.9 · Blue-green cluster migration",
            h2="When in-place isn't safe",
            body_html="""    <p>For high-stakes upgrades (multi-version jumps, regulated workloads, distrust of in-place):</p>
    <ol>
      <li><strong>Build new cluster</strong> at the target version (Terraform / Blueprints).</li>
      <li><strong>Migrate workloads via GitOps</strong>: Argo CD points new cluster at the same git path. Workloads come up.</li>
      <li><strong>Migrate stateful</strong>: snapshot EBS / EFS volumes + restore in new cluster. Or: Velero backup-restore. Or: replicate data continuously (e.g., Postgres replication) + flip primary.</li>
      <li><strong>DNS cut-over</strong>: Route 53 weighted records gradually shift traffic from old to new.</li>
      <li><strong>Decommission old cluster</strong> after validation.</li>
    </ol>
    <p>Twice the infrastructure cost during cutover. Safest upgrade pattern. Used for the most-critical clusters.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For air-gapped or regulated environments: extended support gives you breathing room when an upgrade requires more validation than the standard window permits. Don\'t rely on extended support — but it\'s there if you need it.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your cluster is on 1.32. AWS support ends in 30 days. You want to skip to 1.36 to catch up. Can EKS do a multi-version jump in one update?',
            options=[
                ('a) Yes, AWS handles all the intermediate steps', False),
                ('b) No — like vanilla K8s, EKS allows only +1 minor at a time. You must go 1.32 → 1.33 → 1.34 → 1.35 → 1.36 in sequence.', True),
                ('c) Yes if you delete and recreate', False),
            ],
            feedback='<strong>Answer: b.</strong> EKS enforces +1 minor per upgrade. For a 4-version jump, plan 4 successive upgrades over 4-8 weeks. Or: blue-green to a new cluster directly at 1.36 (any version supported), migrate workloads, decommission old.',
        ),
    },
    before_after_before='<p>Cluster on K8s 1.30; standard support ended 6 months ago; paying $0.60/hr extended. Operators stopped supporting that version. Risky upgrade, no rehearsal cluster. Pluto scan never run.</p>',
    before_after_after='<p>Quarterly upgrade calendar. Pluto scans in CI on every PR. Staging cluster mirrors prod; upgrades rehearsed there first. <code>aws eks update-cluster-version</code> + add-on updates take an afternoon. Standard support always.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">EKS upgrades are easier than vanilla — AWS handles the control plane. The discipline (quarterly cadence, rehearsal, Pluto in CI) is the same.</p>',
    analogy_intro_html='<p>The Maintenance Wing handles all the building\'s renovation work. The contractor (AWS) handles the major renovations on AWS-managed parts (control plane, Managed NG lifecycle, add-on bumps); the tenant (you) handles the workload-side preparation (deprecated-API scans, Velero backups, smoke tests). The renovation calendar (version-support timeline) hangs on the wall: 14-month \"warranty period\" + 12-month extended-support window. Beyond that, the contractor forcibly renovates.</p>',
    translation_rows=[
        ('Renovation calendar', '14 months standard + 12 months extended support'),
        ('Contractor handles structural work', 'AWS handles control-plane + Managed NG lifecycle'),
        ('Tenant prepares the unit', 'Pluto scan, Velero backup, Helm + operator compat checks'),
        ('One renovation per cycle', 'One minor at a time'),
        ('Build a parallel unit + move tenants', 'Blue-green cluster migration'),
        ('Extended-support fee', '$0.60/h premium per cluster'),
        ('Forcible renovation at end of extended', 'AWS auto-upgrades after extended support ends'),
    ],
    analogy_stops="The analogy stops here: AWS\'s upgrade is mostly transparent because the control plane is in their account; the workloads still execute the K8s upgrade machinery (kubelet versions, API deprecations, etc.).",
    eli5='Every few months the building gets a renovation. AWS does the heavy lifting; you just clean your room first. If you don\'t renovate for too long, the building manager forcibly renovates anyway — you want to be ahead of that.',
    eli10="EKS upgrades: 14 months standard + 12 extended per minor. Order: pre-flight scan (Pluto / kubectl convert) → control plane (AWS handles) → Managed NG (AWS rolling drain) → self-managed → Fargate refresh → add-ons (CNI / CoreDNS / kube-proxy / EBS CSI) → verify. Only +1 minor per update; multi-version jumps via blue-green cluster. Quarterly cadence is the discipline.",
    scenarios=[
        Scenario(name='A SaaS doing quarterly EKS upgrades', body='Calendar: week 1 = staging upgrade. Week 2 = production control plane. Week 3 = nodes + add-ons. Repeat. Pluto in CI catches deprecated APIs. ~4 hours of SRE time per cluster per quarter.'),
        Scenario(name='A bank using blue-green cluster migration', body='Build new EKS cluster at target version. Argo CD migrates workloads. RDS Multi-AZ + Aurora handles state replication. Route 53 weighted records do gradual traffic shift. Old cluster decommissioned after 30 days. Twice the cost during cutover; zero in-place risk.'),
        Scenario(name='A team that hit extended support and learned', body='Cluster on 1.28; standard ended; bill jumped $5K/year. Couldn\'t upgrade quickly due to a CRD compatibility issue. Bought extended support; planned blue-green migration; completed in 2 sprints. Lesson: Pluto in CI from now on.'),
        Scenario(name='An EKS Auto Mode user with simplified upgrades', body='Auto Mode handles add-ons + node lifecycle. K8s minor upgrade = one API call to update control plane; Auto Mode handles the rest. No add-on update orchestration. Total upgrade time: 1 hour per cluster.'),
    ],
    misconceptions=[
        Misconception(myth='\"AWS upgrades my add-ons automatically.\"', truth='Only with EKS Auto Mode (E2). For self-managed add-ons or add-ons installed via Helm: you upgrade. For managed add-ons (e.g., VPC CNI managed): you trigger the upgrade via API, AWS performs.'),
        Misconception(myth='\"Extended support is fine; I\'ll stay there.\"', truth='Extended support is a runway, not a destination. AWS will eventually fully deprecate the version even on extended support. And you\'re paying $5K/year per cluster premium.'),
        Misconception(myth='\"EKS doesn\'t need pre-upgrade deprecated-API scans.\"', truth='Same K8s underneath; same API removals. Pluto / kubectl convert in CI on every PR; alert on deprecated API references.'),
    ],
    flashcards=[
        Flashcard(front='EKS standard support window?', back='14 months per K8s minor. After that, extended support kicks in at $0.60/hour cluster fee.'),
        Flashcard(front='Extended support window?', back='12 months at +$0.60/h. Buys time to upgrade. AWS forcibly upgrades after extended ends.'),
        Flashcard(front='EKS upgrade order?', back='Pre-flight scan + Velero → control plane (AWS handles) → Managed NG (rolling drain) → self-managed nodes → Fargate Pod refresh → add-ons (CNI / CoreDNS / kube-proxy / EBS CSI) → verify.'),
        Flashcard(front='Can EKS skip minor versions?', back='No. +1 minor per update. Multi-version jumps require sequential updates or blue-green cluster.'),
        Flashcard(front='How long does control-plane upgrade take?', back='~30-60 min. AWS rolls the apiserver instances behind the LB; cluster API stays available.'),
        Flashcard(front='Managed Node Group upgrade flow?', back='<code>aws eks update-nodegroup-version</code>. AWS uses the same lifecycle controller to drain + replace nodes one at a time. Respects PDBs.'),
        Flashcard(front='Fargate Pod refresh on upgrade?', back='New Pods get the new platform version automatically. Existing Pods stay until natural restart. Force-refresh = trigger rolling deploy.'),
        Flashcard(front='When use blue-green cluster?', back='High-stakes upgrades, multi-version jumps, regulated workloads, distrust of in-place. Twice the infra cost during cutover; zero in-place risk.'),
    ],
    quizzes=[
        Quiz(prompt='Pre-upgrade scan finds 12 Deployments using <code>autoscaling/v2beta2</code> (removed in 1.26). Walk the remediation.', answer='<strong>Same as vanilla (K-VAN V8).</strong> (1) Map deployments → owning teams. (2) Per-Deployment fix: <code>kubectl convert -f hpa.yaml --output-version autoscaling/v2</code>. Edit + re-apply. (3) PR + Argo CD diff review. (4) Apply on staging first; validate HPA still scales. (5) Apply on production. (6) Re-run Pluto to confirm clean. (7) Add CI check that fails PRs introducing deprecated APIs. <strong>EKS-specific note</strong>: if these are on Helm charts from upstream operators, you may need to bump operator version + chart version together. Verify operator compatibility with new K8s minor.'),
        Quiz(prompt='Your team needs to upgrade a 6-cluster fleet from 1.32 → 1.36 in 3 months. Plan?', answer='<strong>4 minor jumps × 6 clusters = 24 cluster upgrades.</strong> <strong>(1) Lab cluster</strong> first: walk all 4 jumps end-to-end; document gotchas; build runbooks. <strong>(2) Staging clusters</strong> next: 2 weeks per jump; soak time after each. <strong>(3) Production</strong>: 1 cluster at a time, 1 jump per week per cluster. Order clusters by criticality (lowest stakes first). <strong>Total timeline</strong>: 4 weeks lab + 8 weeks staging + 4 weeks production rolling = 16 weeks. <strong>Speed it up</strong> if PluTo + operator compat is clean: parallel staging clusters; 2-week production cadence per cluster. <strong>Alternative</strong>: blue-green for production: new clusters at 1.36 from scratch; migrate workloads via Argo CD; decommission old. ~8 weeks total but doubled infra cost during overlap.'),
        Quiz(prompt='Your cluster\'s control-plane upgrade succeeded. After upgrade, VPC CNI Pods crashloop. <strong>Click for the diagnostic. ▼</strong>', cyoa=True, cyoa_tag='the diagnostic', answer='<strong>Common cause: VPC CNI version incompatible with new K8s minor.</strong> Each EKS K8s version has a recommended add-on version compatibility matrix. <strong>Diagnose:</strong> (1) <code>kubectl describe pod -n kube-system aws-node-XXX</code> — look at the failure reason. (2) <code>aws eks describe-addon-versions --kubernetes-version 1.36 --addon-name vpc-cni</code> — see compatible CNI versions. (3) <strong>Fix:</strong> <code>aws eks update-addon --cluster-name prod --addon-name vpc-cni --addon-version v1.x.y-eksbuild.z</code>. AWS rolls the DaemonSet. <strong>Other common post-upgrade issues</strong>: CoreDNS missing required RBAC (auto-fixed by add-on update); kube-proxy ipvs binding errors (rare); EBS CSI driver schema mismatch (update CSI add-on). <strong>Prevention:</strong> in pre-upgrade staging, upgrade add-ons in lockstep with control plane; capture the recommended version pairs in your runbook.'),
    ],
    glossary=[
        GlossaryItem(name='Standard support (EKS)', definition='14 months of regular pricing per K8s minor. After: extended support.'),
        GlossaryItem(name='Extended support (EKS)', definition='12 additional months at +$0.60/hour cluster fee. Buys upgrade time.'),
        GlossaryItem(name='aws eks update-cluster-version', definition='API to upgrade EKS control plane. ~30-60 min; AWS handles rolling.'),
        GlossaryItem(name='aws eks update-nodegroup-version', definition='Per-Managed-NG upgrade. AWS does rolling drain.'),
        GlossaryItem(name='aws eks update-addon', definition='Per-managed-add-on upgrade. CNI, CoreDNS, kube-proxy, EBS CSI, etc.'),
        GlossaryItem(name='Fargate platform version refresh', definition='Recreate Pods on new platform version via rolling deploy.'),
        GlossaryItem(name='Pluto', definition='FairwindsOps tool scanning manifests for deprecated K8s APIs. Run in CI.'),
        GlossaryItem(name='kubectl convert', definition='Subcommand for migrating manifests between API versions.'),
        GlossaryItem(name='Blue-green cluster migration', definition='Build new cluster at target version; migrate workloads; decommission old. Twice infra cost; zero in-place risk.'),
        GlossaryItem(name='Add-on compatibility matrix', definition='AWS-published table of which add-on versions work with which K8s minor.'),
        GlossaryItem(name='aws eks describe-cluster-versions', definition='CLI listing every supported K8s version + standard / extended support dates.'),
        GlossaryItem(name='Velero (in EKS context)', definition='K8s backup tool. Backs up workloads + PVCs (with EBS / EFS snapshot plugins) to S3.'),
    ],
    recap_lead='EKS = 14 months standard + 12 extended per minor. AWS handles control plane + Managed NG + add-on upgrades; you handle pre-flight scans + Velero + verification. +1 minor at a time. Blue-green for high stakes.',
    recap_next='<strong>Next — E10: EKS Troubleshooting (AWS-specific).</strong> IAM/RBAC failures, IP exhaustion, ALB / NLB stuck, Karpenter issues, Auto Mode disruption, IRSA / Pod Identity failures.',
)
