from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Vault mezzanine: KMS keychain, GuardDuty radar, Inspector scanner, Bottlerocket badge, signed-image stamps, CloudTrail audit ledger.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">VAULT MEZZANINE · EKS SECURITY</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <rect x="14" y="34" width="140" height="40" rx="3" fill="#3F4A5E"/><text x="84" y="50" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">KMS envelope</text><text x="84" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">secrets · EBS · EFS</text>
    <rect x="160" y="34" width="140" height="40" rx="3" fill="#A04832"/><text x="230" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">GuardDuty EKS</text><text x="230" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">audit + runtime threat</text>
    <rect x="306" y="34" width="140" height="40" rx="3" fill="#5A9F7A"/><text x="376" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">Inspector / ECR scan</text><text x="376" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">CVE + Snyk-powered</text>
    <rect x="452" y="34" width="140" height="40" rx="3" fill="#E8B547"/><text x="522" y="50" text-anchor="middle" font-size="9" fill="#5A4F45" font-weight="700">Cosign + AWS Signer</text><text x="522" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">image signing</text>
    <rect x="14" y="80" width="140" height="40" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="84" y="96" text-anchor="middle" font-size="9" fill="#A04832" font-weight="700">Bottlerocket</text><text x="84" y="108" text-anchor="middle" font-size="7" fill="#5A4F45">immutable nodes</text>
    <rect x="160" y="80" width="140" height="40" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="230" y="96" text-anchor="middle" font-size="9" fill="#8B5A00" font-weight="700">PSA + SG-for-pods</text>
    <rect x="306" y="80" width="140" height="40" rx="3" fill="#E0EEF3" stroke="#4A8FA8"/><text x="376" y="96" text-anchor="middle" font-size="9" fill="#3F4A5E" font-weight="700">CloudTrail audit</text><text x="376" y="108" text-anchor="middle" font-size="7" fill="#5A4F45">EKS API logs</text>
    <rect x="452" y="80" width="140" height="40" rx="3" fill="#3F4A5E"/><text x="522" y="96" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">private endpoint</text><text x="522" y="108" text-anchor="middle" font-size="7" fill="#FBE8DC">no public API</text>
    <rect x="14" y="128" width="572" height="22" rx="3" fill="#5A9F7A"/><text x="300" y="142" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">Pod Identity / IRSA = least-privilege Pod-to-AWS — security baseline rests on E4</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="07",
    title_short="EKS security",
    title_full="E7 · EKS Security (KMS, GuardDuty, ECR signing, Bottlerocket, audit)",
    title_html="K-EKS E7 · EKS Security",
    module_eyebrow="Module E7 · the vault mezzanine",
    hero_sub_html='Layer the AWS security stack on top of K8s baselines: <strong>KMS envelope encryption</strong> for secrets / EBS / EFS, <strong>GuardDuty EKS Protection + Runtime Monitoring</strong>, <strong>Inspector / ECR enhanced scanning</strong>, <strong>Cosign + AWS Signer</strong> for image signing, <strong>Bottlerocket</strong> immutable nodes, <strong>PSA + SG-for-pods</strong>, <strong>private cluster endpoint</strong>, <strong>CloudTrail audit</strong>.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Penetration test finds: secrets stored unencrypted at rest in etcd (no KMS provider), all images pulled unsigned from public ECR, GuardDuty EKS Runtime Monitoring disabled, public cluster endpoint open to the internet (only protected by IAM), one IAM role with cluster-admin attached to 23 EC2 instances. <em>Each finding is a one-flag fix you should have made at launch</em>. This module is the launch-time checklist.',
    stamp_html='EKS security baseline: <strong>KMS envelope encryption</strong> for K8s Secrets + EBS + EFS (CMK, not default key); <strong>GuardDuty EKS Protection</strong> (audit) + <strong>Runtime Monitoring</strong> (eBPF threat detection); <strong>Inspector + ECR enhanced scanning</strong> (Snyk-powered CVE); <strong>Cosign + AWS Signer</strong> for image signing + verifyImages admission; <strong>ECR replication + pull-through cache</strong>; <strong>Bottlerocket</strong> immutable nodes; <strong>PSA Restricted</strong>; <strong>private cluster endpoint</strong>; <strong>CloudTrail audit</strong>; <strong>IAM Access Analyzer</strong>; <strong>FIPS</strong> for regulated.',
    district_pin="ks-floor07",
    district_label="Vault Mezzanine",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Layer AWS on top of K8s security",
            body_html="""    <p>K8s security baselines (PSA, NetworkPolicy, RBAC, audit log, encryption-at-rest) — covered in K-COM L27-L31 + K-VAN V9. EKS adds AWS-native primitives that complement them. The full posture stack:</p>
    <ul>
      <li><strong>K8s baselines</strong>: RBAC + access entries, PSA, NetworkPolicy, audit, encryption-at-rest.</li>
      <li><strong>AWS layer</strong>: KMS for encryption, GuardDuty for threat detection, Inspector for image scanning, AWS Signer / ECR signing, Bottlerocket nodes, CloudTrail.</li>
      <li><strong>Identity</strong>: Pod Identity / IRSA (E4) for least-privilege Pod-to-AWS.</li>
      <li><strong>Network</strong>: SG-for-pods (E3), private cluster endpoint, VPC endpoints.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.5 · Encryption — KMS everywhere",
            h2="Secrets, EBS, EFS, ECR",
            body_html="""    <ul>
      <li><strong>Secrets at rest in etcd</strong>: enable EKS secrets encryption with a KMS Customer Managed Key (CMK) at cluster create. Pre-existing clusters: enable via <code>aws eks update-cluster-config</code>; existing Secrets need re-write to be encrypted (<code>kubectl get secrets -A -o json | kubectl replace -f -</code>).</li>
      <li><strong>EBS volumes</strong>: every StorageClass should have <code>encrypted: true + kmsKeyId</code> (E5). Default to a CMK; the AWS-managed default key has fewer controls.</li>
      <li><strong>EFS / FSx</strong>: encryption-at-rest with KMS CMK. Encryption-in-transit via TLS to the EFS mount.</li>
      <li><strong>ECR images</strong>: ECR encrypts at rest by default (KMS); use a CMK for compliance.</li>
      <li><strong>CloudWatch Logs / S3 buckets</strong>: KMS-encrypted; same CMK or per-purpose CMKs.</li>
    </ul>
    <p><strong>Key management strategy</strong>: one CMK per environment (dev / staging / prod) per region. Rotate annually (KMS supports automatic). Audit access via CloudTrail.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Threat detection + image security",
            h2="GuardDuty EKS + Inspector + signing",
            body_html="""    <p><strong>Amazon GuardDuty EKS Protection</strong> (released 2022): analyses Kubernetes audit logs for suspicious patterns (privilege escalation, anonymous API access, etc.). <em>Enable on every cluster — free first 30 days, modest cost after</em>.</p>
    <p><strong>GuardDuty EKS Runtime Monitoring</strong> (2023): eBPF-based agent (DaemonSet, AWS-managed) detects runtime threats — process anomalies, network anomalies, file-system anomalies — without requiring you to operate Falco.</p>
    <p><strong>Amazon Inspector + ECR Enhanced Scanning</strong> (Snyk-powered): scan ECR images for CVEs continuously. Findings in Security Hub. ECR Enhanced Scanning is opt-in per-repo.</p>
    <p><strong>Image signing</strong>: <strong>Cosign</strong> (Sigstore, OSS) is the de-facto standard. <strong>AWS Signer</strong> (managed signing service) integrates with ECR + Cosign. Pipeline: build → sign with Cosign keyless or AWS Signer → push to ECR → admission controller (Kyverno verifyImages) verifies before admission.</p>
    <p><strong>ECR features</strong>: <em>replication</em> (cross-region or cross-account), <em>pull-through cache</em> (proxy public registries through your private ECR), <em>repository policies</em> (IAM controlling pulls/pushes per repo).</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Node + cluster + audit hardening",
            h2="Bottlerocket, PSA, private endpoint, CloudTrail, FIPS",
            body_html="""    <ul>
      <li><strong>Bottlerocket</strong>: AWS\'s immutable, container-optimised OS. Read-only root FS, dm-verity, automatic updates via update operator. Smaller attack surface vs Amazon Linux 2; default for EKS Auto Mode.</li>
      <li><strong>Pod Security Standards</strong>: label every namespace <code>pod-security.kubernetes.io/enforce: restricted</code>. Workloads requiring privileged escape get exception namespaces (CSI drivers, monitoring agents).</li>
      <li><strong>SG-for-pods</strong> (E3): per-Pod SecurityGroups for fine-grained AWS-service ACLs. The right path to \"only Pod X can reach RDS Y.\"</li>
      <li><strong>Private cluster endpoint</strong>: <code>endpointPrivateAccess: true, endpointPublicAccess: false</code>. <code>kubectl</code> reachable only from within the VPC (or via VPN / Direct Connect / PrivateLink).</li>
      <li><strong>CloudTrail audit</strong>: every EKS API call logged. Plus K8s control-plane logs (E8) cover in-cluster auth + API requests.</li>
      <li><strong>IAM Access Analyzer</strong>: detects unintended cross-account access in IAM policies + S3 / KMS resource policies.</li>
      <li><strong>FIPS</strong>: required for regulated environments (FedRAMP, FedRAMP-Mod). EKS supports FIPS endpoints; node OS choice (Bottlerocket FIPS, RHEL FIPS) for FIPS-validated crypto.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For PCI / HIPAA-regulated workloads: above + dedicated tenancy, dedicated KMS keys per workload class, per-namespace audit log destinations, segregated IAM admin. Add ~3-6 months of compliance implementation per regulation.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='You enable EKS Secrets encryption with KMS CMK on a cluster that already has 200 Secrets. After the change, are old Secrets encrypted?',
            options=[
                ('a) Yes, AWS auto-encrypts everything', False),
                ('b) No, only new Secrets are encrypted; existing ones stay plaintext until rewritten. Run <code>kubectl get secrets -A -o json | kubectl replace -f -</code> to re-encrypt.', True),
                ('c) Yes after a cluster restart', False),
            ],
            feedback='<strong>Answer: b.</strong> Encryption-at-rest only kicks in on writes. Existing Secrets in etcd are unencrypted until something rewrites them. The replace-all-Secrets command rewrites every Secret + triggers re-encryption. Verify with an etcd dump (if you have access) or by trusting the post-rewrite state.',
        ),
    },
    before_after_before='<p>Public cluster endpoint, IAM-only protection. Secrets unencrypted in etcd. EBS encrypted with default key. No image scanning. No runtime threat detection. CloudTrail enabled but nobody reads it. \"Compliance evidence\" is a wiki page.</p>',
    before_after_after='<p>Private endpoint, only-via-VPN access. KMS CMK encrypts secrets / EBS / EFS / ECR. GuardDuty EKS Runtime Monitoring on. Inspector continuous CVE scan. Kyverno verifyImages enforces Cosign signatures. CloudTrail forwards to SIEM. PSA Restricted everywhere except documented exceptions.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">EKS security is layering AWS-native services on top of K8s baselines. Each layer adds defense without requiring you to operate the security tooling.</p>',
    analogy_intro_html='<p>The Vault Mezzanine sits one floor above the lobby — visible from below, but glass-walled and key-locked. Inside: the master keychain (KMS), the radar dish scanning for intruders (GuardDuty), the conveyor-belt scanner reading every package on entry (Inspector + ECR Enhanced Scanning), the notary stamping authentic packages (AWS Signer + Cosign), the immutable-floor-tile certification (Bottlerocket), the elevator restriction (private cluster endpoint), the building-wide audit ledger (CloudTrail). The vault staff are the AWS security services; you tell them what to watch + they handle the rest.</p>',
    translation_rows=[
        ('Master keychain', 'KMS Customer Managed Keys'),
        ('Radar scanning patrons', 'GuardDuty EKS Protection (audit)'),
        ('Doorman watching for actual misbehaviour', 'GuardDuty EKS Runtime Monitoring (eBPF)'),
        ('Conveyor scanner at entry', 'Amazon Inspector + ECR Enhanced Scanning'),
        ('Notary stamping authentic packages', 'AWS Signer + Cosign + Kyverno verifyImages'),
        ('Immutable-floor certification', 'Bottlerocket OS'),
        ('Elevator restricted to keycard holders', 'Private cluster endpoint'),
        ('Building audit ledger', 'CloudTrail (EKS API + AWS resource changes)'),
        ('Cross-account loan oversight', 'IAM Access Analyzer'),
    ],
    analogy_stops="The analogy stops here: real AWS security services run as separate AWS-side compute (GuardDuty + Inspector are out-of-cluster; Runtime Monitoring is an in-cluster DaemonSet). The vault metaphor undersells the IAM + audit plumbing.",
    eli5='Locks on every door (KMS), cameras watching the building (GuardDuty), inspector at the front desk checking IDs (Inspector + ECR), and a logbook of every visitor (CloudTrail). All run by the building staff (AWS).',
    eli10="EKS security baseline: KMS CMK for Secrets + EBS + EFS + ECR. GuardDuty EKS Protection + Runtime Monitoring (eBPF). Inspector + ECR Enhanced Scanning for CVEs. Cosign + AWS Signer + Kyverno verifyImages. Bottlerocket immutable nodes. PSA Restricted + SG-for-pods. Private cluster endpoint. CloudTrail audit. IAM Access Analyzer for unintended cross-account. FIPS for regulated workloads.",
    scenarios=[
        Scenario(name='A SaaS with full GuardDuty + Inspector + ECR signing', body='GuardDuty EKS Audit + Runtime Monitoring on. Findings forwarded to PagerDuty for P0 (e.g., privilege escalation). ECR Enhanced Scanning for every push; severity Critical = block deploy via Kyverno + verifyImages. Pipeline signs every image with Cosign keyless via GitHub OIDC; cluster admission verifies. Compliance: SOC2 + ISO27001 evidence largely automated.'),
        Scenario(name='A bank with private endpoint + FIPS Bottlerocket + dedicated KMS per workload', body='EKS endpoint private only. Direct Connect from corporate. Bottlerocket FIPS variant on all nodes. KMS CMK per workload class (payments / accounts / analytics) with separate IAM. CloudTrail forwarded to SIEM. Annual external audit; minor findings only.'),
        Scenario(name='A team that learned about default KMS', body='Enabled secrets encryption at cluster create with the AWS-managed default key. Compliance auditor flagged: \"can\'t prove you control the key.\" Migration: created CMK; updated EKS encryption config; rewrote all Secrets to re-encrypt with new key. Lesson: always CMK from the start.'),
        Scenario(name='A startup using ECR pull-through cache', body='Heavy use of public images (postgres, redis, busybox). Set up ECR pull-through cache for Docker Hub + Quay. Now: image pulls go to private ECR, which fetches from public on cache miss. Resilient to Docker Hub rate limits + outages; supply-chain visibility for every image.'),
    ],
    misconceptions=[
        Misconception(myth='\"AWS-managed KMS key is fine for production secrets.\"', truth='Functionally encrypted, but you don\'t control rotation, can\'t restrict access cross-account, can\'t prove key control to an auditor. Always CMK for production. Cost is negligible ($1/month per key).'),
        Misconception(myth='\"GuardDuty Runtime Monitoring is just Falco.\"', truth='Same data plane (eBPF), but AWS-managed: no DaemonSet to operate, integrated with Security Hub / EventBridge, AWS handles updates. Falco is more flexible (custom rules); GuardDuty is operationally simpler.'),
        Misconception(myth='\"Private endpoint means I can\'t kubectl from anywhere.\"', truth='Private endpoint = reachable from within the VPC. Engineers reach it via: VPN, AWS Client VPN, Direct Connect, jump host in the VPC, or AWS SSM Session Manager + port-forwarding. Modern shops use SSM tunneling for kubectl.'),
    ],
    flashcards=[
        Flashcard(front='What does EKS Secrets encryption do?', back='AWS adds a KMS-based envelope encryption layer on top of etcd Secrets storage. Each Secret value encrypted with KMS-derived data key. Set at cluster create or update.'),
        Flashcard(front='GuardDuty EKS Protection vs Runtime Monitoring?', back='Protection: analyses K8s audit logs for suspicious API patterns. Runtime Monitoring: eBPF agent (DaemonSet) detects in-cluster threats (process / network / file). Both managed by AWS.'),
        Flashcard(front='Amazon Inspector for ECR?', back='Continuous CVE scanning of ECR images. Snyk-powered. Findings in Security Hub. Severity-based reporting + alerting.'),
        Flashcard(front='Cosign vs AWS Signer?', back='Cosign = OSS Sigstore CLI. AWS Signer = managed signing service. Both integrate with ECR. Cosign keyless via GitHub OIDC (modern); AWS Signer for fully managed.'),
        Flashcard(front='ECR pull-through cache?', back='Proxy public registries (Docker Hub, Quay, GitHub Container Registry) through private ECR. First pull fetches + caches; subsequent pulls hit ECR. Resilient to public-registry outages + rate limits.'),
        Flashcard(front='Bottlerocket OS?', back='AWS\'s minimal, immutable, container-optimised Linux. Read-only root + dm-verity. Auto-updates via update operator. Default for EKS Auto Mode.'),
        Flashcard(front='Private cluster endpoint?', back='<code>endpointPrivateAccess: true, endpointPublicAccess: false</code>. kubectl reachable only from VPC (or VPN / Direct Connect / SSM tunneling).'),
        Flashcard(front='IAM Access Analyzer for EKS?', back='Detects IAM / S3 / KMS / SQS / etc resource policies allowing unintended cross-account access. Continuous; findings in Security Hub.'),
    ],
    quizzes=[
        Quiz(prompt='You enable GuardDuty EKS Runtime Monitoring. After 24 hours, dashboards show 1500 \"impossible-travel\" findings. Diagnose.', answer='<strong>False positives from CI / build automation.</strong> GuardDuty\'s impossible-travel detector flags an IAM principal authenticating from geographically distant locations within a short window. CI/CD systems (GitHub Actions runners, AWS CodeBuild) span regions; legitimate but flagged. <strong>Fix:</strong> (1) Add suppression rules for known CI principals + their regions. (2) Review actual findings — manual triage. (3) Tune severity thresholds. <strong>For Runtime Monitoring specifically</strong> (eBPF threats): expect noisy first 1-2 weeks as the model baselines your workloads. Tune by suppressing well-known patterns (kubelet probes, node-local DNS). <strong>Long-term:</strong> threat triage as a weekly ritual; runbooks per finding type.'),
        Quiz(prompt='Your team needs to verify image signatures at admission. Cosign keyless signing in CI; you want EKS to verify. Walk the setup.', answer='<strong>(1) Build pipeline</strong>: cosign sign keyless via GitHub OIDC: <code>cosign sign $IMAGE</code>; signature stored as OCI attestation in ECR. <strong>(2) Install Kyverno</strong> in the cluster (Helm). <strong>(3) Define ClusterPolicy</strong>: <pre style=\'background:#F5EFE3;padding:6px;font-size:11px\'>apiVersion: kyverno.io/v2beta1\nkind: ClusterPolicy\nmetadata: {name: verify-images}\nspec:\n  validationFailureAction: Enforce\n  rules:\n  - name: check-signature\n    match:\n      resources:\n        kinds: [Pod]\n        namespaces: [prod]\n    verifyImages:\n    - imageReferences: [\"123.dkr.ecr.us-east-1.amazonaws.com/*\"]\n      attestors:\n      - entries:\n        - keyless:\n            issuer: \"https://token.actions.githubusercontent.com\"\n            subject: \"https://github.com/myorg/.*\"</pre> <strong>(4) Test</strong>: deploy a signed image (succeeds) + an unsigned image (rejected). <strong>(5) Pod Identity</strong> for Kyverno: cosign needs network access to Sigstore + OCI; ensure egress works. <strong>(6) Soak in Audit mode first</strong> (<code>validationFailureAction: Audit</code>) for 1-2 weeks; review PolicyReports; then switch to Enforce. <strong>(7) Add to CI</strong>: PR check that fails if any deployed image isn\'t signed.'),
        Quiz(prompt='Your team is starting from a blank EKS cluster. <strong>Click for the security launch checklist. ▼</strong>', cyoa=True, cyoa_tag='the security launch checklist', answer='<strong>(1) Cluster create</strong>: <code>endpointPrivateAccess: true, endpointPublicAccess: false</code> (or hybrid with allowlist). KMS CMK for Secrets encryption. <strong>(2) Access entries</strong> (E4): map IAM roles → K8s groups; no aws-auth dependence. <strong>(3) Pod Identity Agent</strong> as managed add-on. Per-namespace IAM roles for Pod-to-AWS via Pod Identity associations. <strong>(4) PSA labels</strong>: every namespace gets <code>pod-security.kubernetes.io/enforce: restricted</code> (or baseline for legacy). Exception namespaces (kube-system, csi-) labeled privileged. <strong>(5) GuardDuty</strong>: enable EKS Protection + Runtime Monitoring. Forward findings to SIEM / PagerDuty. <strong>(6) Inspector</strong> + ECR Enhanced Scanning on every repo. <strong>(7) Cosign + Kyverno verifyImages</strong>: every prod image must be signed. <strong>(8) Bottlerocket</strong> nodes (default with Auto Mode; for managed NG, set AMI). <strong>(9) StorageClasses</strong> all KMS-encrypted with the CMK. <strong>(10) NetworkPolicy default-deny</strong> per namespace; AdminNetworkPolicy for cluster-wide rules. <strong>(11) CloudTrail</strong>: control-plane logs to CloudWatch (E8); EKS API logs to S3 + SIEM. <strong>(12) IAM Access Analyzer</strong> on the AWS account. <strong>(13) Backup</strong>: Velero with KMS encryption. <strong>(14) Document break-glass admin</strong>: a separate IAM principal with cluster-admin via access entry; usage alerts to Slack. <strong>(15) kube-bench in CronJob</strong>: weekly score, alert on regression. <strong>Total time</strong>: ~1 sprint for an experienced team. <strong>Result</strong>: production-grade security posture from day 1.'),
    ],
    glossary=[
        GlossaryItem(name='KMS Customer Managed Key (CMK)', definition='AWS KMS key you create + control. Rotation, access, audit all yours. Required for production encryption.'),
        GlossaryItem(name='EKS Secrets encryption', definition='AWS-managed envelope encryption on Secrets in etcd. Set with --encryption-config + KMS CMK at cluster create or update.'),
        GlossaryItem(name='GuardDuty EKS Protection', definition='AWS service. Analyses K8s audit logs for suspicious API patterns. No agent; fully managed.'),
        GlossaryItem(name='GuardDuty EKS Runtime Monitoring', definition='eBPF-based agent (managed DaemonSet) detecting runtime threats. Process / network / file.'),
        GlossaryItem(name='Amazon Inspector', definition='AWS continuous vulnerability scanning. ECR Enhanced Scanning is Snyk-powered; findings in Security Hub.'),
        GlossaryItem(name='AWS Signer', definition='Managed signing service. Integrates with ECR + Cosign. Alternative to Cosign keyless for fully managed signing.'),
        GlossaryItem(name='ECR replication', definition='Cross-region or cross-account ECR image replication. For DR + multi-region deployments.'),
        GlossaryItem(name='ECR pull-through cache', definition='Proxy public registries through private ECR. Resilient to outages + rate limits; supply-chain visibility.'),
        GlossaryItem(name='Bottlerocket', definition='AWS\'s minimal, immutable, container-optimised OS. Read-only root, dm-verity, auto-update operator.'),
        GlossaryItem(name='Private cluster endpoint', definition='endpointPrivateAccess true + endpointPublicAccess false. kubectl via VPC only.'),
        GlossaryItem(name='IAM Access Analyzer', definition='Detects unintended cross-account access in IAM / S3 / KMS / SQS resource policies.'),
        GlossaryItem(name='FIPS-validated K8s on EKS', definition='Bottlerocket FIPS variant + FIPS endpoint API. For FedRAMP / FedRAMP-Mod regulated environments.'),
    ],
    recap_lead='EKS security = AWS layer (KMS + GuardDuty + Inspector + Signer) on top of K8s baselines (PSA + RBAC + NetworkPolicy + audit). Pod Identity (E4) for least-privilege Pod-to-AWS. Bottlerocket nodes. Private endpoint. CloudTrail audit.',
    recap_next='<strong>Next — E8: EKS Observability.</strong> CloudWatch Container Insights, AMP, AMG, ADOT, X-Ray, control-plane logs, AWS Split Cost Allocation.',
)
