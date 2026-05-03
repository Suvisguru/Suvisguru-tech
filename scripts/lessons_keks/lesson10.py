from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Emergency plaza: scenario tiles - IAM/RBAC failure, IP exhaustion, ALB pending, IRSA broken, Pod Identity issue, Karpenter stuck, Auto Mode disruption, API throttle, with CloudTrail searchlight.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">EMERGENCY PLAZA · EKS-SPECIFIC RCA</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">EIGHT EKS-SPECIFIC FAILURE PATTERNS</text>
    <rect x="14" y="34" width="180" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="104" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">1 IAM/RBAC unauth</text><text x="104" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">access entry vs aws-auth</text>
    <rect x="200" y="34" width="180" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="290" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">2 node NotReady / NG launch</text>
    <rect x="386" y="34" width="200" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="486" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">3 VPC IP exhaustion</text>
    <rect x="14" y="76" width="180" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="104" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">4 LB / ALB pending</text>
    <rect x="200" y="76" width="180" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="290" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">5 EBS multi-AZ attach</text>
    <rect x="386" y="76" width="200" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="486" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">6 IRSA / Pod Identity</text>
    <rect x="14" y="118" width="180" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="104" y="134" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">7 Karpenter / Auto Mode</text>
    <rect x="200" y="118" width="180" height="36" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="290" y="134" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">8 API throttling</text>
    <rect x="386" y="118" width="200" height="36" rx="3" fill="#3F4A5E"/><text x="486" y="134" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">CloudTrail · CloudWatch RCA</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="10",
    title_short="troubleshooting",
    title_full="E10 · EKS Troubleshooting (AWS-Specific)",
    title_html="K-EKS E10 · EKS Troubleshooting",
    module_eyebrow="Module E10 · the emergency plaza",
    hero_sub_html='Eight EKS-specific failure patterns: IAM / RBAC mismatch, node NotReady / NG launch failure, VPC CNI IP exhaustion, LB pending, EBS multi-AZ attach, IRSA / Pod Identity broken, Karpenter / Auto Mode stuck, API throttling. <strong>CloudTrail + CloudWatch are the two primary RCA surfaces.</strong>',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Multiple alarms in 10 minutes. New Pods stuck Pending; existing services 503\'ing intermittently. Investigation: VPC CNI IP exhaustion (E3 prefix delegation never enabled); ALB target groups un-registering Pods (security group misconfigured); Karpenter throttled by AWS EC2 RunInstances API (cluster scaled too fast). <em>Three EKS-specific issues in one outage</em>. This module is the runbook library.',
    stamp_html='EKS-specific failure modes need EKS-specific debugging. Top eight: <strong>(1) IAM/RBAC unauth</strong> (access entries vs aws-auth precedence); <strong>(2) node NotReady / NG launch fail</strong> (IAM, AMI, subnet capacity); <strong>(3) VPC CNI IP exhaustion</strong> (enable prefix delegation); <strong>(4) LB pending</strong> (subnet tags, IAM); <strong>(5) EBS multi-AZ attach</strong> (WaitForFirstConsumer); <strong>(6) IRSA / Pod Identity</strong> (trust policy, OIDC, association); <strong>(7) Karpenter / Auto Mode stuck</strong> (instance availability, IAM, NodeClass); <strong>(8) API throttling</strong> (CloudWatch + CloudTrail RCA, request limits). <strong>CloudTrail + CloudWatch + Container Insights</strong> are the diagnostic surfaces.',
    district_pin="ks-floor10",
    district_label="Emergency Plaza",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why EKS-specific troubleshooting deserves its own module",
            body_html="""    <p>Vanilla K8s troubleshooting (K-VAN V10) covers the cluster-internal failures: cert expiry, broken CNI, broken CoreDNS, etc. EKS adds a layer of <em>AWS-specific</em> failures that don\'t exist on vanilla:</p>
    <ul>
      <li>IAM / RBAC mismatch (because EKS bridges two identity systems).</li>
      <li>VPC CNI IP exhaustion (because Pods consume real VPC IPs).</li>
      <li>LB provisioning failures (because AWS LB Controller talks to ELB API).</li>
      <li>EBS multi-AZ attach (because EBS is single-AZ).</li>
      <li>IRSA / Pod Identity broken (because Pod-to-AWS auth has its own machinery).</li>
      <li>Karpenter / Auto Mode quirks (because they call EC2 / spot APIs).</li>
      <li>API throttling (because AWS rate-limits everything).</li>
    </ul>
    <p>Diagnosis follows a similar methodology (V44 in K-COM): reproduce → observe → hypothesise → test. The <em>tools</em> are AWS-specific: CloudTrail, CloudWatch, Container Insights, ALB access logs, EC2 Console.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Top four (identity + nodes + IPs + LBs)",
            h2="The recurring incidents",
            body_html="""    <p><strong>1. IAM / RBAC unauth</strong>: \"You must be logged in to the server (Unauthorized).\" Common cause: no access entry / aws-auth mapping. Diagnose: <code>aws eks list-access-entries --cluster-name X</code>; <code>kubectl auth can-i --as=user</code>. Fix: add access entry. <em>Migrate to access entries; aws-auth lockouts are still recoverable via cluster-creator IAM principal.</em></p>
    <p><strong>2. Node NotReady / Managed NG launch failure</strong>: NG creation hangs; nodes don\'t register. Common causes: (a) IAM role missing required policies (AmazonEKSWorkerNodePolicy, AmazonEC2ContainerRegistryReadOnly, AmazonEKS_CNI_Policy); (b) subnet IP exhaustion; (c) wrong AMI for the K8s version; (d) launch template SG blocks 443 to control plane. Diagnose: NG events in EKS Console; CloudTrail for the EC2 RunInstances call.</p>
    <p><strong>3. VPC CNI IP exhaustion</strong>: \"0/N nodes available: N had no Pod IPs available.\" Fix: enable prefix delegation. <code>kubectl set env -n kube-system ds/aws-node ENABLE_PREFIX_DELEGATION=true</code>; restart aws-node; new Pods provision IPs.</p>
    <p><strong>4. LoadBalancer / ALB pending</strong>: Service stuck without an external IP, or Ingress without an ALB. Common causes: subnets missing required tags (<code>kubernetes.io/role/elb</code> for internet, <code>internal-elb</code> for internal); IAM permissions on the LB controller; wrong target type. Diagnose: <code>kubectl describe svc / ingress</code> for events; <code>kubectl logs -n kube-system deploy/aws-load-balancer-controller</code>.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Identity + Karpenter + API issues",
            h2="The other four",
            body_html="""    <p><strong>5. EBS multi-AZ attach failure</strong>: \"FailedAttachVolume — volume is in different AZ.\" Cause: Pod scheduled in AZ that doesn\'t have the volume. Fix: StorageClass <code>volumeBindingMode: WaitForFirstConsumer</code>; recreate PVC. <em>Always WaitForFirstConsumer on multi-AZ EBS.</em></p>
    <p><strong>6. IRSA / Pod Identity broken</strong>: AWS SDK calls return AccessDenied or NoCredentialsProvider. Diagnose IRSA: (a) OIDC provider exists in IAM (<code>aws iam list-open-id-connect-providers</code>); (b) trust policy on the role allows the cluster\'s OIDC + the SA path; (c) SA annotated with role ARN; (d) Pod\'s projected JWT contains correct audience. Diagnose Pod Identity: (a) Pod Identity Agent installed (managed add-on); (b) association exists for the (cluster, namespace, SA); (c) IAM role trust policy allows <code>pods.eks.amazonaws.com</code>; (d) Pod restarted after association.</p>
    <p><strong>7. Karpenter / Auto Mode stuck</strong>: Pending Pods not getting nodes. Common causes: (a) NodePool requirements too restrictive (no instance type can satisfy); (b) IAM role lacks <code>ec2:RunInstances</code>; (c) NodeClass subnet/SG selectors match nothing; (d) instance type unavailable in target AZ; (e) spot interruption rate exceeds NodePool limits. Diagnose: <code>kubectl get nodeclaims -A</code>; <code>kubectl logs -n karpenter deploy/karpenter</code>; CloudTrail for failed RunInstances calls.</p>
    <p><strong>8. API throttling</strong>: AWS API calls fail with <code>Throttling: Rate exceeded</code>. Cause: too many EC2 / EKS / IAM calls in a short window (often Karpenter scaling fast or controllers polling aggressively). Mitigate: tune controller poll intervals, request quota increase, batch requests, exponential backoff (most controllers do this automatically).</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Diagnostic tooling",
            h2="CloudTrail, CloudWatch, kubectl",
            body_html="""    <ul>
      <li><strong>CloudTrail</strong>: every AWS API call (EC2, EKS, IAM, KMS, ELB) — the source of truth for \"what AWS API was called when by whom.\" Searchable via Athena. Default 90-day retention; configure trails for longer.</li>
      <li><strong>CloudWatch Logs</strong>: control-plane logs (E8) + container logs (Fluent Bit) + ALB access logs + Karpenter logs.</li>
      <li><strong>CloudWatch Container Insights</strong>: cluster-wide metrics + per-Pod resource trends.</li>
      <li><strong>kubectl describe</strong>: events on resources are still the first stop. Most EKS-specific failures show useful events here.</li>
      <li><strong>EKS Console</strong>: cluster + nodegroup + add-on status; node group launch failures shown here.</li>
      <li><strong>EC2 Console</strong>: instance state, system log, instance status checks. For NotReady nodes: check the EC2 instance for hardware / OS issues.</li>
      <li><strong>VPC Reachability Analyzer</strong>: simulates network paths. Useful for \"why can\'t Pod reach RDS\" problems.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For very subtle issues: AWS Support case + screen-share with TAM. EKS standard support tier is included; enterprise support is faster + has solution architects available.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your Pod logs show <code>NoCredentialsProvided: Unable to locate credentials</code>. The Pod\'s SA is annotated with the IRSA role ARN. Diagnose.',
            options=[
                ('a) The IAM role doesn\'t exist', False),
                ('b) Verify the SA annotation, the IAM role\'s trust policy includes the cluster\'s OIDC provider + the correct SA path, the OIDC provider is registered in IAM, the Pod restarted after annotation. Most often: trust policy SA path mismatch.', True),
                ('c) Restart the cluster', False),
            ],
            feedback='<strong>Answer: b.</strong> IRSA setup has 4 moving parts: SA annotation, role trust policy, OIDC provider, Pod restart. The most common bug is the trust policy condition (<code>StringEquals</code> on the SA path) being slightly off (typo, wrong namespace, missing <code>system:serviceaccount:</code> prefix). <strong>Modern fix:</strong> migrate to Pod Identity (no trust-policy YAML to write) for new SAs.',
        ),
    },
    before_after_before='<p>Outages diagnosed by SSH-then-guess. No CloudTrail integration with on-call. Same incidents recur because runbooks aren\'t written. Six EKS-specific patterns each take 2 hours to diagnose first time + 30 min next time.</p>',
    before_after_after='<p>Eight runbooks per EKS-specific failure. CloudTrail integrated with PagerDuty / Slack on suspicious patterns. Quarterly chaos drills covering each scenario. New on-call recovers most incidents in &lt; 30 min using the runbook.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">EKS-specific incidents recur. Drilled team + runbook library makes them routine; un-drilled team makes them emergencies.</p>',
    analogy_intro_html='<p>The Emergency Plaza is the K-Skyline\'s practice ground for unusual incidents. Pinned on the wall: eight scenario cards, each with a runbook. The dispatcher (CloudTrail) records every API call to the building. The control room (CloudWatch + Container Insights) shows live metrics. New on-call walks the plaza, takes a card, runs the drill blind, debriefs. Goal: every responder has handled every scenario at least once before the real call comes.</p>',
    translation_rows=[
        ('Practice ground for unusual incidents', 'EKS-specific failure drills'),
        ('Eight scenario cards on the wall', 'Eight failure patterns + runbooks'),
        ('Building API call recorder', 'CloudTrail'),
        ('Live metrics control room', 'CloudWatch + Container Insights'),
        ('On-call walks the drill blind', 'Chaos drills (similar to K-VAN V10)'),
        ('Debrief after each scenario', 'Runbook updates from drill findings'),
        ('Specialist tools at the desk', 'EKS Console, EC2 Console, VPC Reachability Analyzer'),
    ],
    analogy_stops="The analogy stops here: real EKS incidents are diagnosed via API calls, log queries, eBPF traces, AWS Support tickets — not paper cards on a plaza wall.",
    eli5='Eight kinds of fire drill specific to the AWS tower. Practice each one before the real fire so it\'s muscle memory.',
    eli10="Eight EKS-specific failure patterns: IAM/RBAC unauth, node NotReady / NG launch, VPC CNI IP exhaustion, LB pending, EBS multi-AZ, IRSA / Pod Identity, Karpenter / Auto Mode stuck, API throttling. Diagnostic tools: CloudTrail (every API call), CloudWatch Container Insights, kubectl describe (still useful), EKS / EC2 Console, VPC Reachability Analyzer. Build runbooks; drill quarterly.",
    scenarios=[
        Scenario(name='A SaaS with quarterly EKS chaos days', body='Practice each of the eight scenarios on a non-prod cluster. Score: time-to-mitigation. Track over 6 quarters: from 90 min average → 22 min average. Five new runbook updates from drill findings.'),
        Scenario(name='A bank that automated IRSA migration', body='Old IRSA roles still in use; pre-migration audit found 47 unique trust policies, several with subtle SA path bugs. Migration to Pod Identity removed all 47 trust-policy YAMLs; replaced with associations. Cleaner; auditable; tested.'),
        Scenario(name='A team hit by Karpenter API throttling', body='Cluster scaled 50 → 500 nodes during a marketing event. Karpenter exhausted EC2 RunInstances quota; Pods Pending for 10 min; some workloads couldn\'t start. Mitigation: requested quota increase + tuned Karpenter to batch RunInstances calls. Lesson: pre-emptive quota increases for events you know about.'),
        Scenario(name='A team using VPC Reachability Analyzer', body='Pod can\'t reach RDS. Old debugging: SSH everywhere, tcpdump, etc. New: VPC Reachability Analyzer simulates the path; immediately shows the SG rule blocking traffic. RCA in 5 minutes vs hours.'),
    ],
    misconceptions=[
        Misconception(myth='\"AWS Support is faster than my own runbook.\"', truth='AWS Support is great for genuinely novel issues + AWS-side bugs. For recurring patterns: your runbook is faster + builds team skills. Use Support for the 5%; runbooks for the 95%.'),
        Misconception(myth='\"CloudTrail is too noisy for incident response.\"', truth='Default CloudTrail across many AWS APIs IS noisy. Filter aggressively: Athena queries by time + service + IAM principal. Or: ship to a SIEM with smart parsing. Don\'t skip it; just operate it.'),
        Misconception(myth='\"Karpenter / Auto Mode rarely fails.\"', truth='They\'re reliable for steady state but have specific failure modes (NodeClass mis-config, instance unavailability, IAM gaps). Build runbooks for these; they happen.'),
    ],
    flashcards=[
        Flashcard(front='\"Unable to locate credentials\" in a Pod — IRSA diagnosis?', back='Check: SA annotated with role ARN, IAM role trust policy includes the cluster\'s OIDC + correct SA path, OIDC provider registered, Pod restarted after annotation. Most common bug: trust policy SA path typo.'),
        Flashcard(front='Pod Identity \"Unable to locate credentials\" diagnosis?', back='Check: Pod Identity Agent installed, association exists for (cluster, namespace, SA), IAM role trust includes <code>pods.eks.amazonaws.com</code>, Pod restarted after association.'),
        Flashcard(front='\"You must be logged in to the server\" — diagnosis?', back='AWS IAM works (you got the kubeconfig) but no access entry / aws-auth mapping for your IAM principal. Add access entry mapping to a K8s group.'),
        Flashcard(front='ALB Ingress stays Pending — what to check?', back='Subnets must have <code>kubernetes.io/role/elb</code> tag (internet-facing) or <code>internal-elb</code> (internal). LB controller IAM. Logs: <code>kubectl logs -n kube-system deploy/aws-load-balancer-controller</code>.'),
        Flashcard(front='\"Pod has no IPs available\" — fix?', back='VPC CNI IP exhaustion. Enable prefix delegation: <code>kubectl set env -n kube-system ds/aws-node ENABLE_PREFIX_DELEGATION=true</code> + restart aws-node DaemonSet. Or: bigger instance types, or add Pod subnets via custom networking.'),
        Flashcard(front='\"FailedAttachVolume — volume in different AZ\"?', back='EBS is single-AZ; Pod scheduled in different AZ from volume. Fix: StorageClass <code>volumeBindingMode: WaitForFirstConsumer</code>; recreate PVC.'),
        Flashcard(front='Karpenter not provisioning nodes — common causes?', back='(1) NodePool requirements too restrictive. (2) IAM role lacks ec2:RunInstances. (3) NodeClass subnet/SG selectors match nothing. (4) Instance type unavailable in zone. (5) Spot interruption rate exceeds limits. Check <code>kubectl get nodeclaims</code> + Karpenter logs.'),
        Flashcard(front='AWS API throttling — mitigate?', back='Tune controller poll intervals; request quota increases; batch requests; exponential backoff. Karpenter and add-on controllers respect backoff by default.'),
    ],
    quizzes=[
        Quiz(prompt='Your Pod logs <code>403 Forbidden: User arn:aws:sts::123:assumed-role/PodRole/i-abc is not authorized to perform: s3:GetObject on resource ...</code>. Diagnose.', answer='<strong>The Pod is using the EC2 instance role, not its IRSA / Pod Identity role.</strong> The <code>i-abc</code> in the assumed-role ARN is the instance ID, not the SA name. <strong>Causes:</strong> (1) IRSA: SA not annotated, or annotation typo, or trust policy mismatch — Pod falls back to the node\'s instance profile. (2) Pod Identity: association doesn\'t exist for this (cluster, ns, SA), or Pod started before association was created — Pod Identity Agent gives no creds, AWS SDK falls back. <strong>Fix:</strong> verify SA annotation (IRSA) or association (Pod Identity); restart Pod. <strong>Verify after restart</strong>: <code>kubectl exec POD -- aws sts get-caller-identity</code> should show the role ARN, not the instance role.'),
        Quiz(prompt='Karpenter logs show <code>insufficient capacity: spot price exceeded</code> for 30 minutes. Diagnose.', answer='<strong>Spot capacity dynamics.</strong> AWS\'s spot market for the instance types in your NodePool isn\'t offering capacity at acceptable prices in target AZs. <strong>Mitigations:</strong> (1) <strong>Broaden instance types in NodePool</strong>: more diversity = more spot pools = better availability. Add multiple families (c6i, c7i, m6i, m7i, c6a) + multiple sizes. (2) <strong>Add on-demand fallback</strong>: NodePool capacity-type In [spot, on-demand]; Karpenter prefers spot, falls back. (3) <strong>Multi-AZ</strong>: ensure NodeClass subnet selectors hit all AZs. (4) <strong>Lower spot bid by accepting older generations</strong>: m5 / c5 often have better spot availability than m7i / c7i. (5) <strong>Quota</strong>: vCPU spot quota per region — request increase preemptively. <strong>Long-term:</strong> graph spot capacity rejection rate by instance type per region; build a NodePool that mostly succeeds.'),
        Quiz(prompt='You\'re building runbooks for the eight EKS failure patterns. <strong>Click for the structure. ▼</strong>', cyoa=True, cyoa_tag='the runbook structure', answer='<strong>Each runbook has 6 sections:</strong> <strong>(1) Symptom</strong>: exact error message + where it appears (kubectl, Pod logs, AWS Console). <strong>(2) Likely causes</strong>: ranked by frequency. <strong>(3) Diagnostic commands</strong>: copy-paste-ready. <code>aws eks describe-cluster</code>, <code>kubectl describe</code>, <code>aws cloudtrail lookup-events</code>, etc. <strong>(4) Recovery procedure</strong>: step-by-step fix. Conservative path first; nuclear option last. <strong>(5) Prevention</strong>: what to set up so this doesn\'t recur. <strong>(6) Drill scenario</strong>: how to reproduce on a non-prod cluster. <strong>Storage:</strong> in git alongside the platform repo. Linked from PagerDuty alert annotations. <strong>Maintenance:</strong> after each real incident, update the relevant runbook with what surprised people. <strong>Cadence:</strong> quarterly chaos day exercising 2-3 runbooks; new on-call runs through all 8 within 6 months. <strong>Result:</strong> mean time to mitigation drops from \"figure it out\" to \"execute the runbook.\" The runbook library is a force-multiplier for the team; treat it as a first-class artefact.'),
    ],
    glossary=[
        GlossaryItem(name='Access entry vs aws-auth precedence', definition='When both exist for the same principal, access entry wins. Migrate to access entries; aws-auth is legacy.'),
        GlossaryItem(name='Cluster-creator IAM principal', definition='Implicit cluster-admin path even when access entries / aws-auth are broken. Document who created each cluster.'),
        GlossaryItem(name='Managed NG launch failure causes', definition='IAM policy missing, AMI mismatch, subnet capacity, launch template SG blocking 443.'),
        GlossaryItem(name='Prefix delegation enable command', definition='<code>kubectl set env -n kube-system ds/aws-node ENABLE_PREFIX_DELEGATION=true</code> + restart aws-node.'),
        GlossaryItem(name='Subnet tags for AWS LB Controller', definition='<code>kubernetes.io/role/elb</code> (internet ALB), <code>internal-elb</code> (internal). At least 2 subnets in different AZs.'),
        GlossaryItem(name='WaitForFirstConsumer (multi-AZ EBS)', definition='StorageClass binding mode aligning EBS provisioning to Pod\'s zone. Required in multi-AZ clusters.'),
        GlossaryItem(name='IRSA trust policy structure', definition='Federated principal = OIDC provider; Action = AssumeRoleWithWebIdentity; Condition = StringEquals on SA path.'),
        GlossaryItem(name='Pod Identity association', definition='EKS API mapping (cluster, namespace, SA) → IAM role. Replaces IRSA trust-policy editing.'),
        GlossaryItem(name='Karpenter NodeClaim', definition='Internal CRD representing in-flight node provision. <code>kubectl get nodeclaims -A</code> reveals stuck provisions.'),
        GlossaryItem(name='AWS API throttling', definition='Rate-limit responses (Throttling: Rate exceeded). Mitigate via backoff, batching, quota increases.'),
        GlossaryItem(name='CloudTrail (for EKS RCA)', definition='Every AWS API call. Searchable via Athena. Default 90-day retention. Configure trails for longer.'),
        GlossaryItem(name='VPC Reachability Analyzer', definition='AWS service simulating network paths. Identifies SG / route table / NACL issues without manual debugging.'),
    ],
    recap_lead='Eight EKS-specific failure patterns. Diagnostic surfaces: CloudTrail, CloudWatch Container Insights, kubectl describe, EKS / EC2 Console, VPC Reachability Analyzer. Build runbooks per pattern; drill quarterly.',
    recap_next='<strong>Next — E11: K-EKS Capstone.</strong> Multi-AZ EKS Auto Mode cluster with everything wired together: Karpenter, AWS LB Controller, Pod Identity, KMS, Gateway API via VPC Lattice, AMP + AMG, Argo CD GitOps, blue-green upgrade runbook, DR plan.',
)
