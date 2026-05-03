from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Tower complete: a finished K-Skyline tower with floor labels - lobby, concierge, comm tower, security desk, vault, power, vault mezzanine, observation, maintenance, emergency, capstone roof.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">TOWER COMPLETE · K-EKS CAPSTONE</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">REFERENCE STACK · multi-AZ EKS Auto Mode</text>
    <rect x="14" y="34" width="115" height="34" rx="3" fill="#3F4A5E"/><text x="71" y="50" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">EKS Auto Mode</text><text x="71" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">Karpenter built-in</text>
    <rect x="135" y="34" width="115" height="34" rx="3" fill="#A04832"/><text x="192" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">multi-AZ VPC</text><text x="192" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">prefix delegation</text>
    <rect x="256" y="34" width="115" height="34" rx="3" fill="#5A9F7A"/><text x="313" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">Pod Identity</text><text x="313" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">no IRSA</text>
    <rect x="377" y="34" width="115" height="34" rx="3" fill="#E8B547"/><text x="434" y="50" text-anchor="middle" font-size="9" fill="#5A4F45" font-weight="700">KMS CMK</text><text x="434" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">secrets+EBS+EFS</text>
    <rect x="498" y="34" width="88" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="542" y="50" text-anchor="middle" font-size="8" font-weight="700" fill="#A04832">VPC Lattice</text><text x="542" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">Gateway API</text>
    <rect x="14" y="76" width="115" height="34" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="71" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">AMP + AMG</text>
    <rect x="135" y="76" width="115" height="34" rx="3" fill="#E0EEF3" stroke="#4A8FA8"/><text x="192" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">GuardDuty + Inspector</text>
    <rect x="256" y="76" width="115" height="34" rx="3" fill="#3F4A5E"/><text x="313" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">Argo CD GitOps</text>
    <rect x="377" y="76" width="115" height="34" rx="3" fill="#5A9F7A"/><text x="434" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">Velero + S3</text>
    <rect x="498" y="76" width="88" height="34" rx="3" fill="#A04832"/><text x="542" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">runbooks</text>
    <rect x="14" y="118" width="572" height="34" rx="3" fill="#5A9F7A"/><text x="300" y="138" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">deliverables: working cluster + git repo (EKS Blueprints) + 8 runbooks + DR + blue-green upgrade plan</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="11",
    title_short="capstone tower",
    title_full="E11 · Capstone — Multi-AZ EKS Auto Mode Tower with Everything",
    title_html="K-EKS E11 · Capstone Tower",
    module_eyebrow="Module E11 · the tower complete",
    hero_sub_html='<strong>Tie everything together.</strong> Multi-AZ EKS Auto Mode cluster with the reference stack: Karpenter (built-in), AWS LB Controller, Pod Identity, KMS-encrypted secrets / EBS / EFS, Gateway API via VPC Lattice, AMP + AMG observability, Argo CD GitOps, blue-green upgrade runbook, DR plan. Defend it.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Two weeks before launch, the team realises: nobody has built the full reference EKS stack end-to-end. They\'ve installed pieces. The capstone is the safeguard — finishing K-EKS means you\'ve done it, with the receipts (working cluster, git repo via EKS Blueprints, runbooks, blue-green upgrade plan, DR runbook).',
    stamp_html='<strong>Capstone deliverables</strong>: (1) Working multi-AZ EKS Auto Mode cluster (3 AZs). (2) EKS Blueprints / Terraform repo reproducing the cluster from scratch. (3) Pod Identity + access entries (no IRSA / aws-auth). (4) KMS CMK encryption everywhere. (5) Gateway API + VPC Lattice for cross-VPC. (6) AMP + AMG + ADOT + control-plane logs. (7) Argo CD App-of-Apps for workloads + add-ons. (8) Eight runbooks for the eight EKS failure patterns. (9) Documented blue-green upgrade rehearsal. (10) DR plan covering AZ failure + region failure. <strong>K-EKS-complete</strong> when a peer reproduces from your artifacts + recovers a chaos-injected disaster.',
    district_pin="ks-floor11",
    district_label="Tower Complete",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What \"capstone\" means here",
            body_html="""    <p>K-EKS is 10 modules of how. The capstone is one module of <em>do</em>: a single end-to-end project exercising every prior module in sequence. You come out with a working production-grade EKS cluster + IaC + runbooks + the muscle memory to do it again.</p>
    <p>The reference stack is opinionated to keep the project tractable: <strong>EKS Auto Mode</strong> (Karpenter built-in + add-ons bundled), <strong>AWS LB Controller</strong> (built into Auto Mode), <strong>Pod Identity</strong> (modern auth), <strong>KMS CMK</strong> everywhere, <strong>Gateway API + VPC Lattice</strong>, <strong>AMP + AMG + ADOT</strong>, <strong>Argo CD</strong>, <strong>EKS Blueprints (Terraform)</strong>. You can sub equivalents (Calico for Cilium, Datadog for AMG) but the modules apply.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Phase A — Architecture + Cluster",
            h2="E1-E3 in sequence",
            body_html="""    <p><strong>A.1 Architecture document</strong> (E1). One page: 3 AZs in <code>us-east-1</code>, EKS Auto Mode, Pod CIDR <code>192.168.224.0/20</code> (non-overlapping with corp VPN), Service CIDR <code>10.96.0.0/12</code>, private cluster endpoint, KMS CMK, Pod Identity for auth. Commit to git as <code>docs/architecture.md</code>.</p>
    <p><strong>A.2 EKS Blueprints (Terraform)</strong>. Module deploys: VPC (3 public + 3 private subnets, prefix-delegation-friendly), EKS cluster with Auto Mode enabled, KMS CMK for Secrets encryption, IAM roles (cluster role, Auto Mode node role), control-plane logs (all 5 types), Pod Identity Agent add-on, Container Insights add-on. <code>terraform apply</code>; ~20-30 min.</p>
    <p><strong>A.3 Validate</strong>: <code>kubectl get nodes</code> shows nodes from Auto Mode (Bottlerocket); CoreDNS Pods Running; Container Insights dashboard populated.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Phase B — Identity + Storage + Observability",
            h2="E4-E5-E8 in sequence",
            body_html="""    <p><strong>B.1 Pod Identity</strong> (E4). Define IAM roles per workload class (e.g., <code>app-prod-pods</code>, <code>logging-pods</code>, <code>backup-pods</code>) — each scoped least-privilege. Pod Identity associations per (namespace, SA) → role. No IRSA. No aws-auth.</p>
    <p><strong>B.2 Access entries</strong> (E4). Map IAM Identity Center permission sets to K8s groups via access entries. Per-team groups bound to namespace-scoped Roles. Cluster-creator IAM role documented as the break-glass admin.</p>
    <p><strong>B.3 Storage</strong> (E5). EBS CSI add-on (Auto Mode bundles). Custom StorageClass <code>gp3-encrypted</code> with KMS CMK + WaitForFirstConsumer. snapshot-controller (Auto Mode bundles). Optional: EFS CSI for any RWX workloads.</p>
    <p><strong>B.4 Observability</strong> (E8). AMP workspace + IAM role for ADOT. AMG workspace via Identity Center SSO. ADOT collector DaemonSet (deployed via Helm) scrapes Pod metrics + ships to AMP, traces to X-Ray, logs to CloudWatch. Container Insights enhanced (already from A.2). Split Cost Allocation enabled.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Phase C — Security, GitOps, DR, Upgrade",
            h2="E6-E7-E9-E10 + capstone deliverables",
            body_html="""    <p><strong>C.1 Security</strong> (E7). GuardDuty EKS Protection + Runtime Monitoring on. Inspector enhanced scanning on every ECR repo. Cosign signing in CI; Kyverno verifyImages in admission. PSA Restricted on every prod namespace. AdminNetworkPolicy default-deny + selective allows.</p>
    <p><strong>C.2 GitOps</strong> (Argo CD). Bootstrap script: helm install Argo CD; root App-of-Apps points at <code>k8s-platform/apps/</code>. Argo CD reconciles: cert-manager, ExternalDNS, Kyverno, Falco (or rely on GuardDuty Runtime Monitoring), Velero, AMP+AMG configurations, application Deployments.</p>
    <p><strong>C.3 Backup + DR</strong>. Velero schedule (nightly); EBS snapshot via CSI snapshot-controller (every 30 min for stateful workloads); cross-region replication of critical data (S3 versioning + cross-region replication for backups). DR plan: <strong>AZ failure</strong> = topology spread + multi-AZ EBS = automatic recovery; <strong>region failure</strong> = secondary cluster in another region (or blue-green migration to one).</p>
    <p><strong>C.4 Upgrade rehearsal</strong> (E9). Build a staging clone via EKS Blueprints. Walk a minor-version upgrade (control plane → Auto Mode handles add-ons + nodes). Document gotchas. Output: <code>docs/runbooks/eks-upgrade-vX-to-vY.md</code>.</p>
    <p><strong>C.5 Eight runbooks</strong> (E10). One file per failure pattern. Each tested on the staging cluster.</p>
    <p><strong>C.6 Final review</strong>: a colleague reproduces the cluster from the EKS Blueprints repo + recovers one chaos-injected disaster using your runbook. <strong>K-EKS-complete</strong>.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>If you have time + budget: build a multi-region active-active EKS pair. Aurora Global Database for stateful tier; Route 53 weighted health-checked records; Argo CD per cluster reconciling the same git path. Multi-region adds ~3 weeks beyond the standard capstone.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='You finish Phase A; cluster is up. Phase B step 1: you create Pod Identity associations. The first Pod fails to assume the role. What\'s the most common cause?',
            options=[
                ('a) Pod Identity is broken for everyone', False),
                ('b) The IAM role\'s trust policy doesn\'t include <code>pods.eks.amazonaws.com</code> as principal. Update the trust policy + retry.', True),
                ('c) Restart the cluster', False),
            ],
            feedback='<strong>Answer: b.</strong> Pod Identity requires the role\'s trust policy to allow <code>pods.eks.amazonaws.com</code> as principal (different from IRSA\'s OIDC-federated principal). Easy to miss when migrating from IRSA. Update + retry; Pod Identity Agent picks up associations live.',
        ),
    },
    before_after_before='<p>You\'ve finished K-COM and read all 10 K-EKS modules. You haven\'t built end-to-end. The gap between knowing and doing only shows up when something breaks in production.</p>',
    before_after_after='<p>You\'ve built the reference EKS Auto Mode cluster. You\'ve broken it on purpose and recovered. Your EKS Blueprints repo + runbooks let a colleague reproduce in a day. You can defend any choice in an interview. <strong>K-EKS-complete</strong>.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">The capstone exists so the gap between knowing and doing is closed deliberately, not by surprise in production.</p>',
    analogy_intro_html='<p>Tower Complete is the K-Skyline\'s eleventh and final floor — the one that takes in the view of every other floor below. The Drafting Hut\'s blueprint, the Concierge service running quietly, the Communication Tower\'s LBs humming, the Security Desk\'s identity flow, the Storage Vault\'s encrypted volumes, the Power Floor\'s right-sized compute, the Vault Mezzanine\'s detection, the Observation Deck\'s dashboards, the Maintenance Wing\'s upgrade calendar, the Emergency Plaza\'s drilled runbooks. You stand on the roof with the deed in one hand, the keys in the other, the runbook library in your pocket. <strong>K-EKS-complete</strong>.</p>',
    translation_rows=[
        ('Tower deed', 'Architecture document in git'),
        ('Plaque on the lobby', 'EKS Blueprints / Terraform module'),
        ('Concierge\'s daily report', 'Auto Mode + Container Insights dashboards'),
        ('Master keychain in the vault', 'KMS CMK encrypting Secrets / EBS / EFS / ECR'),
        ('Inter-building shuttle service', 'VPC Lattice + Gateway API'),
        ('Observation Deck instruments', 'AMP + AMG + ADOT + X-Ray + control-plane logs'),
        ('Resident registry', 'Argo CD App-of-Apps in git'),
        ('Insurance policy + drill log', 'Velero + DR plan + tested runbooks'),
        ('Renovation calendar', 'Quarterly EKS upgrade cadence'),
        ('Emergency-drill scoreboard', 'Eight runbooks + chaos drills'),
    ],
    analogy_stops="The analogy stops here: the tower is one snapshot. Real EKS clusters evolve continuously — new K8s minors, new add-ons, new workloads. K-EKS-complete means \"can build + operate + defend\" — not \"done forever.\"",
    eli5='You\'ve learned how to live in the AWS tower. Now build one yourself, lock it down, set up the alarms, write down what to do in a fire — and prove someone else could do it from your notes.',
    eli10="Capstone: build a multi-AZ EKS Auto Mode cluster end-to-end. EKS Blueprints (Terraform) for the cluster + VPC + KMS. Pod Identity + access entries for auth. KMS CMK for Secrets / EBS / EFS / ECR. Gateway API + VPC Lattice. AMP + AMG + ADOT. Argo CD GitOps for workloads + add-ons. GuardDuty + Inspector + Cosign. Velero + DR plan. Eight runbooks for E10\'s failure patterns. Blue-green upgrade rehearsal. Peer review + chaos-drill recovery = K-EKS-complete.",
    scenarios=[
        Scenario(name='A team finishing K-EKS as their pre-prod milestone', body='4 weeks of dedicated time. EKS Blueprints + Argo CD + observability + security stack + 8 runbooks. Final demo: chaos day on the lab cluster, recovering 3 of E10\'s scenarios in front of the team. Clear \"production-ready\" signal.'),
        Scenario(name='A bank using K-EKS graduates as the AWS Platform team', body='Anyone running prod EKS clusters has finished K-EKS. New hires onboarded by working through K-EKS with a buddy. Hand-off quality is hire-time + ongoing.'),
        Scenario(name='A startup choosing K-EKS over an AWS cert', body='K-EKS validates building. Cert validates trivia. Engineering manager: SRE candidates pair on EKS Blueprints + Pod Identity migration + Karpenter consolidation. Artifact (git repo + runbooks) is the portfolio.'),
        Scenario(name='An open-source contributor giving back', body='Used K-EKS to build their first managed cluster. Wrote a blog comparing EKS Auto Mode vs DIY Karpenter; PR\'d a typo fix in the K-EKS module; published their EKS Blueprints fork. Cycle complete.'),
    ],
    misconceptions=[
        Misconception(myth='\"The capstone is optional / nice-to-have.\"', truth='K-EKS-complete means built end-to-end. Reading the modules without doing the capstone is K-EKS-read. Different skill level.'),
        Misconception(myth='\"You need a real production cluster to do K-EKS.\"', truth='An AWS account + a small lab cluster are enough. Cost: ~$50-200 for the capstone duration. AWS\'s Free Tier covers some pieces; for full Auto Mode + AMP + observability + a few hours per day for 4 weeks, plan ~$200-400 total.'),
        Misconception(myth='\"You can skip the runbooks if everything works.\"', truth='Runbooks are the deliverable. Working cluster without runbooks = can\'t hand off + can\'t recover under pressure. Write them as you go.'),
    ],
    flashcards=[
        Flashcard(front='K-EKS deliverables (10)?', back='Architecture doc, EKS Blueprints repo, working multi-AZ Auto Mode cluster, Pod Identity + access entries, KMS CMK encryption everywhere, Gateway + VPC Lattice, AMP + AMG + ADOT + control-plane logs, Argo CD GitOps, 8 EKS-specific runbooks, blue-green upgrade rehearsal + DR plan.'),
        Flashcard(front='Reference K-EKS stack?', back='EKS Auto Mode (Karpenter + add-ons), AWS LB Controller (built-in), Pod Identity, KMS CMK, Gateway API + VPC Lattice, AMP + AMG + ADOT + X-Ray, Argo CD, Velero, GuardDuty + Inspector + Cosign + Kyverno verifyImages.'),
        Flashcard(front='Phase A?', back='Architecture doc + EKS Blueprints provisioning multi-AZ cluster with Auto Mode + KMS + control-plane logs + Container Insights. Cluster nodes Ready.'),
        Flashcard(front='Phase B?', back='Pod Identity per (ns, SA), access entries for human IAM, KMS-encrypted StorageClass, EBS / EFS CSI configs, AMP + AMG + ADOT observability stack.'),
        Flashcard(front='Phase C?', back='Security (GuardDuty / Inspector / Cosign / PSA / AdminNetworkPolicy), Argo CD GitOps for workloads + add-ons, Velero + DR plan, blue-green upgrade rehearsal, 8 runbooks.'),
        Flashcard(front='How to know K-EKS-complete?', back='Peer reproduces the cluster from EKS Blueprints + recovers a chaos-injected disaster using your runbook. Score = pass.'),
        Flashcard(front='Substitute components?', back='Calico for Cilium (FIPS); Datadog for AMP/AMG (existing licence); HashiCorp Vault for Secrets Manager. Same modules apply; substitute components.'),
        Flashcard(front='K-EKS time investment?', back='3-5 weeks of focused work for one engineer + reviewer pair. Less if your org has K-EKS graduates to mentor. AWS cost ~$200-400 for the lab.'),
    ],
    quizzes=[
        Quiz(prompt='You\'ve finished Phase A + B. Phase C\'s upgrade rehearsal: <code>aws eks update-cluster-version --kubernetes-version 1.36</code>. After 30 min, kubectl returns errors. Diagnose.', answer='<strong>Likely cause: VPC CNI / kube-proxy add-on incompatibility post-upgrade.</strong> Check: (1) <code>aws eks describe-update --cluster-name X --update-id Y</code> shows the upgrade status. (2) <code>kubectl describe pod -n kube-system aws-node-XXX</code> for CNI errors. <strong>Fix:</strong> upgrade managed add-ons in lockstep — <code>aws eks update-addon --addon-name vpc-cni --addon-version &lt;compatible&gt;</code>. Repeat for kube-proxy, CoreDNS, EBS CSI. <strong>Recovery if hung:</strong> AWS Support for control plane stuck issues; otherwise wait it out (control-plane upgrades are eventually consistent + AWS retries internally). <strong>Document:</strong> the add-on upgrade order + version compatibility in <code>docs/runbooks/eks-upgrade-vX-to-vY.md</code>.'),
        Quiz(prompt='Phase C\'s DR drill: simulate AZ failure on the lab cluster. Workloads survive but Karpenter logs show \"insufficient capacity\" trying to provision replacement nodes. Diagnose.', answer='<strong>Auto Mode (Karpenter) wants to replace nodes lost to the failed AZ.</strong> The remaining 2 AZs may not have spot capacity for the requested instance types. <strong>Fix in real-time:</strong> NodeClass requirements broaden across instance families + capacity-type In [spot, on-demand]. Verify via <code>kubectl get nodeclaims -A</code>; failed claims have reasons. <strong>Validate workloads still serve:</strong> 2/3 of replicas alive; HPA scales remaining; Pod-Disruption-Budgets honored. <strong>Document:</strong> the NodePool needs to span enough AZs / instance types that AZ failure doesn\'t break provisioning. Add to architecture doc + runbook.'),
        Quiz(prompt='You\'re the senior engineer reviewing a colleague\'s K-EKS capstone. <strong>Click for the rubric. ▼</strong>', cyoa=True, cyoa_tag='the rubric', answer='<strong>(1) Architecture doc clarity</strong>: one page; sizing, network plan (CIDRs non-overlapping with corp), endpoint mode, OS choice, IAM strategy, KMS strategy, observability plan, upgrade cadence, DR plan. Decisions justified. <strong>(2) Working cluster</strong>: multi-AZ; control plane HA-tested (kill cp-1 — irrelevant for EKS, but kill all worker nodes in one AZ); Container Insights showing Pod metrics; AMG dashboards rendering. <strong>(3) EKS Blueprints repo</strong>: <code>terraform apply</code> from scratch in a fresh AWS account reproduces the cluster identically. <strong>(4) Pod Identity</strong>: per-namespace IAM roles with least privilege; no IRSA; no aws-auth. <strong>(5) KMS CMK</strong>: Secrets, EBS, EFS, ECR all encrypted with team-controlled CMK. <strong>(6) GitOps</strong>: Argo CD App-of-Apps reconciles add-ons + workloads. Drift detection working. <strong>(7) Backups</strong>: Velero restore tested on staging cluster + worked. <strong>(8) Eight runbooks</strong>: each tested; each reproducible. <strong>(9) Upgrade rehearsal</strong>: documented + executed on staging at least once. <strong>(10) DR plan</strong>: AZ failure tested; region failure plan documented. <strong>(11) Defense</strong>: walk me through any decision; reasoning solid. <strong>(12) Live demo</strong>: introduce an E10 chaos failure on the lab cluster; colleague recovers in &lt; 30 min using their runbook. <strong>If all 12 pass: K-EKS-complete.</strong> Common failure modes: \"works but undocumented\", \"documented but unreproducible\", \"reproducible but no DR drilled.\"'),
    ],
    glossary=[
        GlossaryItem(name='Capstone (K-EKS)', definition='Final K-EKS module. End-to-end project building the reference EKS stack from scratch.'),
        GlossaryItem(name='Reference K-EKS stack', definition='EKS Auto Mode + AWS LB Controller + Pod Identity + KMS CMK + Gateway API + VPC Lattice + AMP + AMG + ADOT + Argo CD + Velero + GuardDuty + Inspector + Cosign.'),
        GlossaryItem(name='K-EKS deliverables', definition='Architecture doc, EKS Blueprints repo, working cluster, Pod Identity + access entries, KMS encryption, observability stack, GitOps, 8 runbooks, blue-green upgrade rehearsal, DR plan.'),
        GlossaryItem(name='Phase A', definition='Architecture + cluster (E1-E3). EKS Blueprints provisions multi-AZ cluster with Auto Mode + KMS + control-plane logs.'),
        GlossaryItem(name='Phase B', definition='Identity + Storage + Observability (E4-E5-E8). Pod Identity, access entries, KMS-encrypted StorageClass, AMP + AMG + ADOT.'),
        GlossaryItem(name='Phase C', definition='Security + GitOps + DR + Upgrade (E6-E7-E9-E10). GuardDuty + Cosign + Argo CD + Velero + 8 runbooks + blue-green rehearsal.'),
        GlossaryItem(name='K-EKS-complete', definition='You can build + operate + harden + back up + upgrade + recover an EKS cluster — and a peer can reproduce from your artifacts + chaos-recover.'),
        GlossaryItem(name='EKS Blueprints (Terraform)', definition='AWS reference Terraform modules for production EKS. Opinionated; batteries-included. Recommended IaC for K-EKS capstone.'),
        GlossaryItem(name='AWS Free Tier (EKS context)', definition='Limited free usage of some AWS services. EKS itself isn\'t in Free Tier ($0.10/h cluster fee); some related services are.'),
        GlossaryItem(name='Pair review', definition='Final K-EKS gate: peer reviews artifacts + watches chaos drill. Pass / iterate.'),
        GlossaryItem(name='Substitute K-EKS stack', definition='Calico instead of Cilium dataplane (FIPS); Datadog instead of AMG (licence); Vault instead of Secrets Manager. Same modules apply.'),
        GlossaryItem(name='Multi-region active-active EKS', definition='Optional advanced extension. Aurora Global DB + Route 53 weighted health-checked + Argo CD per cluster + same git path. ~3 weeks beyond standard capstone.'),
    ],
    recap_lead='K-EKS capstone = build the reference EKS stack end-to-end + harden + back up + upgrade + DR-drill + 8 runbooks. Working cluster + EKS Blueprints repo + runbooks + defended decisions + reproduced by a peer = K-EKS-complete.',
    recap_next='<strong>Done.</strong> You\'ve walked the K-Skyline tower from lobby to roof. K-EKS ends here; what comes next is operating real EKS clusters with the muscle memory you built.',
)
