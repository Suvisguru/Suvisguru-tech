from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Watchtower and fence: a tower with a watchman, a fence with locked gates, signs for CIS / NSA-CISA / image signing / runtime security.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">WATCHTOWER &amp; FENCE · HARDENING</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">CIS-STYLE BASELINE (subset)</text>
    <rect x="14" y="34" width="186" height="40" rx="3" fill="#3F4A5E"/><text x="107" y="50" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">apiserver hardening</text><text x="107" y="64" text-anchor="middle" font-size="7" fill="#FBE8DC">--anonymous-auth=false · audit · enc-at-rest</text>
    <rect x="206" y="34" width="186" height="40" rx="3" fill="#5A9F7A"/><text x="299" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">RBAC least privilege</text><text x="299" y="64" text-anchor="middle" font-size="7" fill="#FBE8DC">no default-SA grants; review CRBs</text>
    <rect x="398" y="34" width="186" height="40" rx="3" fill="#A04832"/><text x="491" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">PSA + admission</text><text x="491" y="64" text-anchor="middle" font-size="7" fill="#FBE8DC">restricted profile · Kyverno/VAP</text>
    <rect x="14" y="80" width="186" height="40" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="107" y="96" text-anchor="middle" font-size="9" fill="#A04832" font-weight="700">supply chain</text><text x="107" y="110" text-anchor="middle" font-size="7" fill="#5A4F45">cosign verify · SBOM · SLSA L3</text>
    <rect x="206" y="80" width="186" height="40" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="299" y="96" text-anchor="middle" font-size="9" fill="#8B5A00" font-weight="700">runtime security</text><text x="299" y="110" text-anchor="middle" font-size="7" fill="#5A4F45">Falco · Tetragon · NetworkPolicy</text>
    <rect x="398" y="80" width="186" height="40" rx="3" fill="#E0EEF3" stroke="#4A8FA8"/><text x="491" y="96" text-anchor="middle" font-size="9" fill="#3F4A5E" font-weight="700">node OS hardening</text><text x="491" y="110" text-anchor="middle" font-size="7" fill="#5A4F45">CIS-Ubuntu · SELinux · auditd</text>
    <rect x="14" y="126" width="572" height="22" rx="3" fill="#3F4A5E"/><text x="300" y="140" text-anchor="middle" font-size="8" fill="#FBF1D6">break-glass admin: time-bounded · audited · separate auth path</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="09",
    title_short="security hardening",
    title_full="V9 · Security Hardening (CIS, RBAC, PSA, supply-chain, runtime)",
    title_html="K-VAN V9 · Security Hardening",
    module_eyebrow="Module V9 · the watchtower and fence",
    hero_sub_html='Self-managed K8s gives you all the security knobs the cloud usually pre-tunes. <strong>The CIS Kubernetes Benchmark</strong> + NSA/CISA hardening guide are the playbook. Add: RBAC least-privilege, PSA enforcement, supply-chain verification, runtime detection, certificate hygiene, break-glass.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Pen-test report lands on Friday. Findings: anonymous-auth still enabled on the apiserver. <code>cluster-admin</code> bound to four SAs nobody remembers. Etcd snapshots in S3 unencrypted. PSA at <code>privileged</code> on every namespace. No image signature verification. \"How did we get here?\" answered with \"we never set the baseline.\" This module is the baseline.',
    stamp_html='Hardening posture: <strong>CIS Kubernetes Benchmark</strong> (kube-bench scores), <strong>NSA/CISA K8s hardening guide</strong>. Tactical layers: <strong>API server</strong> (anonymous-auth=false, audit, encryption-at-rest, admission), <strong>RBAC least privilege</strong> (no default-SA grants), <strong>PSA</strong> (restricted profile baseline), <strong>NetworkPolicy</strong> (default-deny), <strong>supply chain</strong> (cosign + SBOM + verifyImages), <strong>runtime</strong> (Falco / Tetragon), <strong>certificate rotation</strong> (cert-manager + auto-renewal), <strong>break-glass admin</strong> (time-bounded + audited).',
    district_pin="kf-site09",
    district_label="Watchtower",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why hardening is its own module",
            body_html="""    <p>kubeadm + V6 cluster config get you to \"working with sensible defaults.\" Hardening pushes you to \"defensible against a determined attacker.\" The two are not the same. Self-managed clusters need explicit posture work because nothing else is doing it for you.</p>
    <p>Hardening for K8s has a clear playbook: the <strong>CIS Kubernetes Benchmark</strong> (community-curated checklist with kube-bench tooling), supplemented by the <strong>NSA/CISA Kubernetes Hardening Guidance</strong> (more recent, prescriptive). Together they cover ~120 controls across API server, etcd, kubelet, node OS, network, RBAC, audit, supply chain.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The seven hardening layers",
            h2="What to harden, in priority order",
            body_html="""    <ol>
      <li><strong>API server</strong>: <code>--anonymous-auth=false</code>, audit policy enabled (V6), encryption-at-rest with KMS v2 (V6), admission plugins enabled (NodeRestriction, PodSecurity, ResourceQuota, LimitRanger), private API endpoint where possible, certificate rotation.</li>
      <li><strong>etcd</strong>: client + peer cert auth, encryption-at-rest (cluster-wide), no anonymous client access, dedicated network segment.</li>
      <li><strong>kubelet</strong>: anonymous auth off, authorization mode <code>Webhook</code>, serving cert rotation enabled (V6), no <code>--read-only-port</code>.</li>
      <li><strong>Node OS</strong>: CIS-style baseline (Ubuntu CIS, RHEL CIS), SELinux/AppArmor enforcing, auditd shipping logs, SSH keys-only + bastion, no root login, automatic security patches scheduled.</li>
      <li><strong>RBAC</strong>: least privilege, no default-SA grants, audit ClusterRoleBindings to <code>cluster-admin</code> quarterly, OIDC for humans (no shared kubeconfigs).</li>
      <li><strong>Workload security</strong>: PSA <code>restricted</code> on production namespaces (V6 + L31 of K-COM), NetworkPolicy default-deny (L17/L26 of K-COM), AdminNetworkPolicy for cluster-wide rules.</li>
      <li><strong>Supply chain + runtime</strong>: cosign image signing + verifyImages admission policy (L30 of K-COM), SBOMs available, Falco/Tetragon for runtime detection.</li>
    </ol>""",
        ),
        Section(
            eyebrow="Section 1.7 · Run the benchmark",
            h2="kube-bench + reporting",
            body_html="""    <p><code>kube-bench</code> (Aqua) runs CIS Benchmark checks against a cluster. Run as a Job:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs -l job-name=kube-bench

# Output: per-control PASS / FAIL / WARN with remediation guidance
# Example: 1.2.6 Ensure that the --kubelet-https argument is set to true (PASS)
# Example: 5.7.3 Apply Security Context to Your Pods and Containers (FAIL)</code></pre>
    <p>Run weekly via CronJob; ship report to a SIEM or PolicyReport CRD. Track score over time as a metric. Investigate every regression.</p>
    <p>For managed K8s components (EKS / GKE / AKS), kube-bench has provider-specific profiles — pick the right one to avoid false alarms on cloud-managed components. For vanilla self-managed: standard profile applies.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Break-glass + ongoing posture",
            h2="When the regular path won't do",
            body_html="""    <p><strong>Break-glass admin</strong>: occasionally you need cluster-admin to debug a P0. Best practice:</p>
    <ul>
      <li>A separate auth path: not the daily SSO; a hardware key + emergency-only credentials.</li>
      <li>Time-bounded: short TTL on the credential. Auto-expire.</li>
      <li>Audited: every break-glass use logs to an out-of-band channel that on-call sees + reviews next day.</li>
      <li>Documented: when to use, who can authorise, what to do after.</li>
    </ul>
    <p><strong>Ongoing posture</strong>: hardening is a daily practice, not a one-time event.</p>
    <ul>
      <li>kube-bench weekly + dashboard.</li>
      <li>Vulnerability scanning (Trivy / Grype on container images, weekly + on every build).</li>
      <li>Patch management (V8 cadence + monthly OS patches).</li>
      <li>Backup encryption + off-site replication (Velero with KMS).</li>
      <li>Compliance evidence: PolicyReports, audit log retention, change-control records — quarterly review with security team.</li>
    </ul>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For FIPS / FedRAMP / regulated environments: RKE2 ships FIPS-validated binaries; Talos has a FIPS edition; OpenShift and other commercial distros have their own paths. Vanilla kubeadm does not provide a FIPS posture out of the box; pick a distro that does if compliance demands it.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='kube-bench reports control 5.1.5 (\"Ensure that the namespace-default service account is not actively used\") as FAIL. What does this mean?',
            options=[
                ('a) The default ServiceAccount has been deleted', False),
                ('b) Some Pods in some namespaces are using the default SA — and that SA may have RBAC bindings, escalating any compromised Pod\'s blast radius', True),
                ('c) The default namespace is in use', False),
            ],
            feedback='<strong>Answer: b.</strong> The default SA in every namespace gets a token mounted into every Pod that doesn\'t specify a custom SA. If anyone bound a Role to <code>default:default</code>, every Pod in that namespace inherits it. Fix: ensure no RoleBindings reference <code>default</code>; require Pods to specify a non-default SA via Kyverno mutation or PSA.',
        ),
    },
    before_after_before='<p>Anonymous auth on. Default SA grants. PSA at <code>privileged</code>. No image verification. No runtime detection. Compliance reports are wiki entries. Audit findings dozens deep.</p>',
    before_after_after='<p>kube-bench in CI; score &gt; 95%. RBAC reviewed quarterly via <code>rakkess</code>. PSA <code>restricted</code> baseline. Cosign verifies images at admission. Falco shipping events to SIEM. Break-glass tested + auditable. Compliance evidence is queries against PolicyReports.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Hardening is layered + ongoing. Each layer alone is partial; the stack makes the cluster defensible.</p>',
    analogy_intro_html='<p>The Watchtower stands at the perimeter of the homestead. The fence (NetworkPolicy + admission) keeps casual intruders out. The watchman in the tower (Falco / Tetragon) sees what\'s actually happening inside. The night patrol (kube-bench, weekly) checks that locks are still in place. The deed-of-trust drawer (audit logs) records who entered + what they did. And tucked in a sealed envelope at the back of the tower: the break-glass key, time-stamped, used only when the regular gates are locked + something\'s on fire.</p>',
    translation_rows=[
        ('Fence around the homestead', 'NetworkPolicy + AdminNetworkPolicy default-deny'),
        ('Locked gates with posted rules', 'API server + admission policies (PSA, VAP, Kyverno)'),
        ('Watchman in the tower', 'Falco / Tetragon runtime monitoring'),
        ('Night patrol checking locks', 'kube-bench weekly CIS scan'),
        ('Deed-of-trust drawer', 'Audit log + EncryptionConfiguration'),
        ('Notarised package receipts', 'Cosign signature + SBOM verification'),
        ('Sealed break-glass envelope', 'Time-bounded admin credential; audited'),
        ('Yearly fence inspection', 'Quarterly RBAC + posture review'),
    ],
    analogy_stops="The analogy stops here: real security is layered defense, not a single fence. A single misconfigured RBAC binding bypasses every other control. The watchman + the fence + the locks + the audits all matter; one alone is fiction.",
    eli5='Build a fence, post a watchman, lock the doors, write down who comes in. Once a week the patrol checks the locks. Always have a backup key for emergencies — but only one person knows where it is, and using it sets off an alarm.',
    eli10="Hardening = posture work after install. Run kube-bench weekly (CIS Benchmark); track score. Layers: apiserver (audit + encryption + admission), etcd (cert auth, no anonymous), kubelet (no anonymous, no read-only port, serving cert rotation), node OS (CIS baseline, SELinux/AppArmor, auditd), RBAC (least privilege; no default-SA grants), workload (PSA restricted + NetworkPolicy default-deny), supply chain (cosign + SBOM + verifyImages), runtime (Falco/Tetragon). Break-glass admin: separate path, time-bounded, audited.",
    scenarios=[
        Scenario(name='A SaaS with kube-bench in CI', body='Daily kube-bench job; output to PolicyReport CRD; Grafana dashboard on score over time. Alert if any Level 1 FAIL appears. Runbook for each control. Score consistently &gt; 96%; remaining 4% are documented exceptions.'),
        Scenario(name='A bank running RKE2 for FIPS posture', body='RKE2 with FIPS-validated binaries. CIS Level 2 baseline. Harvester for Talos-based hosts. CIS scan + SBOM scanning + Falco rules + cosign verifyImages. Auditor: \"this is the cleanest cluster we\'ve seen.\"'),
        Scenario(name='A team that audited 200 ClusterRoleBindings', body='Year-end review used <code>rakkess</code> to enumerate every subject + permission. Found: 14 cluster-admin bindings nobody remembered, 8 SAs with secrets read access cluster-wide, 3 group bindings for old projects. Cleanup PR removed 18 of them. Annual cadence now built into compliance reviews.'),
        Scenario(name='A startup with break-glass tested quarterly', body='1Password vault holds emergency credential. SSO break-glass procedure documented. Quarterly test: someone uses break-glass for a planned operation (e.g., bumping etcd quota); on-call gets the alert; team reviews after. Avoids \"we have it but never used it\" failure mode.'),
    ],
    misconceptions=[
        Misconception(myth='\"PSA Restricted is too strict for production.\"', truth='Restricted is the right baseline for nearly all application Pods. Specific workloads (CSI drivers, Falco, kube-proxy) need privileged; those go in their own namespaces with explicit privileged label. Most app namespaces should be restricted.'),
        Misconception(myth='\"kube-bench is only for compliance teams.\"', truth='It\'s a continuous quality signal for engineering. New misconfiguration introduced by a change shows up as a new FAIL. Treat the score the way you treat unit-test coverage — own it.'),
        Misconception(myth='\"Cosign verifyImages slows down deploys.\"', truth='&lt; 100ms per Pod admission once cached. Negligible. The supply-chain assurance benefit is enormous; the latency cost isn\'t.'),
    ],
    flashcards=[
        Flashcard(front='What is the CIS Kubernetes Benchmark?', back='Community-curated set of ~120 hardening controls across master, etcd, control plane, worker, policies. Run via kube-bench (Aqua). Track score over time.'),
        Flashcard(front='Three apiserver hardening flags?', back='<code>--anonymous-auth=false</code>, audit policy enabled, EncryptionConfiguration with KMS v2. NodeRestriction admission. Disable insecure-port if still around (deprecated).'),
        Flashcard(front='RBAC least-privilege checklist?', back='No bindings to <code>system:authenticated</code> beyond <code>system:public-info-viewer</code>. No default-SA RoleBindings. Quarterly cluster-admin review. OIDC for humans (no shared kubeconfigs).'),
        Flashcard(front='PSA restricted requirements?', back='runAsNonRoot, drop ALL capabilities, seccompProfile RuntimeDefault, AppArmor profile, no privileged, no hostPath, no hostNetwork, no hostPID. K8s baseline for app Pods.'),
        Flashcard(front='Image signing verification flow?', back='cosign sign image in CI (keyless via Fulcio + OIDC). Kyverno verifyImages policy at admission verifies signature against expected identity. Reject unsigned or wrong-key.'),
        Flashcard(front='Falco vs Tetragon?', back='Both are eBPF runtime security. Falco: longer-established, rule-based, CNCF graduated. Tetragon (Cilium): newer, integrates with Cilium policy, broader process tracking. Either is fine; pick one.'),
        Flashcard(front='Break-glass best practices?', back='Separate auth path (not daily SSO). Time-bounded credential. Audited (out-of-band alert on use). Documented when/why/how. Tested quarterly.'),
        Flashcard(front='Where do FIPS-validated binaries come from?', back='RKE2 ships FIPS builds. Talos has a FIPS edition. OpenShift + commercial distros provide their own. Vanilla kubeadm does not provide FIPS out of the box.'),
    ],
    quizzes=[
        Quiz(prompt='kube-bench reports 5.2.4 (\"Minimize the admission of containers wishing to share the host network namespace\") as FAIL. Walk the remediation.', answer='<strong>(1) Find the offending Pods.</strong> <code>kubectl get pods -A -o jsonpath=\'{range .items[?(@.spec.hostNetwork==true)]}{.metadata.namespace}/{.metadata.name}{"\\n"}{end}\'</code>. Some are legitimate (CNI agents, monitoring DaemonSets); others are accidental. <strong>(2) Categorise.</strong> Legitimate hostNetwork goes in a namespace labelled <code>pod-security.kubernetes.io/enforce: privileged</code> (an explicit exception). Accidental hostNetwork in app Pods gets fixed: remove the field. <strong>(3) Enforce.</strong> PSA <code>baseline</code> profile blocks hostNetwork; ensure your app namespaces have <code>baseline</code> or stricter. <strong>(4) Re-run kube-bench</strong>; control 5.2.4 should pass. <strong>Lesson:</strong> CIS controls have remediation pointers; the work is finding which Pods + which namespaces are in scope.'),
        Quiz(prompt='Your audit shows <code>cluster-admin</code> bound to a ServiceAccount in the <code>jenkins</code> namespace. The Jenkins job needs to apply manifests across many namespaces. How do you tighten?', answer='<strong>(1) Replace <code>cluster-admin</code> with a least-privilege ClusterRole.</strong> Identify the actual verbs Jenkins needs: <code>create</code>, <code>update</code>, <code>patch</code>, <code>delete</code>, <code>get</code>, <code>list</code> on specific resources (Deployments, Services, ConfigMaps). Probably NOT cluster-scoped objects (CRDs, Nodes, ClusterRoles themselves) unless explicitly. <strong>(2) Scope by namespace.</strong> If Jenkins manages 20 specific namespaces, create a RoleBinding in each. If it manages \"any namespace where label X=Y\", use a CRB but with the tight ClusterRole. <strong>(3) Validate.</strong> <code>kubectl auth can-i --as=system:serviceaccount:jenkins:jenkins-deployer &lt;verb&gt; &lt;resource&gt; -n &lt;ns&gt;</code> for representative actions. <strong>(4) Soft-rollout.</strong> Run Jenkins jobs in CI mode (dry-run) against the new SA; verify nothing breaks. Then switch the SA. <strong>(5) Remove the cluster-admin binding.</strong> <strong>(6) Add to compliance evidence:</strong> document the new permissions + reason. Pen-tester next quarter sees the thoughtful boundary instead of a cluster-admin keystone.'),
        Quiz(prompt='You\'re tasked with bringing a vanilla kubeadm cluster to a CIS-style 95+ score in a sprint. <strong>Click for the playbook. ▼</strong>', cyoa=True, cyoa_tag='the playbook', answer='<strong>Day 1: baseline measure.</strong> Install kube-bench Job + capture report. Categorise FAILs by impact + ease. <strong>Day 2-3: API server hardening.</strong> Edit the static-pod manifest: <code>--anonymous-auth=false</code>, <code>--audit-log-*</code>, <code>--encryption-provider-config</code>. KMS v2 backed by Vault Transit. Roll one CP at a time. <strong>Day 4: kubelet hardening.</strong> KubeletConfiguration: <code>authentication.anonymous.enabled: false</code>, <code>authorization.mode: Webhook</code>, <code>readOnlyPort: 0</code>, <code>serverTLSBootstrap: true</code> + auto-CSR-approver. Roll node-by-node. <strong>Day 5-6: PSA + NetworkPolicy default-deny.</strong> Label every namespace with <code>pod-security.kubernetes.io/enforce: baseline</code> (or restricted where workloads tolerate). Apply BANP for cluster-wide default-deny egress. Smoke test. <strong>Day 7-8: RBAC review.</strong> <code>rakkess</code> output → spreadsheet. Find + fix obvious over-grants. Quarterly re-review baked into runbook. <strong>Day 9: image verification.</strong> Install cosign + Kyverno verifyImages policy in audit mode (log only). Cataloguing weeks 2-3. Switch to enforce after. <strong>Day 10: runtime + scan loop.</strong> Falco + Trivy as DaemonSets / CronJobs. Re-run kube-bench. <strong>Result:</strong> ~95+ score, documented exceptions, ongoing weekly scan + alerting. Sprint complete; baseline locked in.'),
    ],
    glossary=[
        GlossaryItem(name='CIS Kubernetes Benchmark', definition='Community-curated hardening checklist (~120 controls). De-facto standard for K8s security posture.'),
        GlossaryItem(name='kube-bench', definition='Aqua tool that runs the CIS Kubernetes Benchmark and reports per-control results.'),
        GlossaryItem(name='NSA/CISA Hardening Guidance', definition='US-government K8s hardening guide. Complements CIS with prescriptive recommendations.'),
        GlossaryItem(name='Pod Security Admission (PSA)', definition='Built-in admission controller. Three profiles (privileged, baseline, restricted) per namespace via labels.'),
        GlossaryItem(name='Anonymous auth (apiserver)', definition='When true, requests without credentials are treated as user <code>system:anonymous</code>. Disable in production.'),
        GlossaryItem(name='RBAC least privilege', definition='Practice of granting only the verbs + resources actually needed; no <code>cluster-admin</code> casually; no default-SA grants.'),
        GlossaryItem(name='Cosign verifyImages (Kyverno)', definition='Admission policy verifying image signatures + identity at admission time. Rejects unsigned / wrong-key images.'),
        GlossaryItem(name='Falco', definition='CNCF runtime security. eBPF-based syscall monitoring with rule engine + alerting.'),
        GlossaryItem(name='Tetragon', definition='Cilium\'s eBPF security tool. Process tracking + policy enforcement at the kernel.'),
        GlossaryItem(name='Break-glass admin', definition='Emergency cluster-admin credential. Separate auth path; time-bounded; audited.'),
        GlossaryItem(name='FIPS-validated K8s', definition='K8s binaries built with FIPS-certified crypto. RKE2, Talos FIPS edition, commercial distros.'),
        GlossaryItem(name='rakkess', definition='Community CLI for visualising RBAC permissions across subjects + resources.'),
    ],
    recap_lead='Hardening is layered: apiserver / etcd / kubelet / node OS / RBAC / workload (PSA + NetworkPolicy) / supply chain / runtime. CIS Benchmark via kube-bench tracks the posture. Break-glass for emergencies. Quarterly review.',
    recap_next='<strong>Next — V10: Advanced Vanilla Troubleshooting.</strong> When everything goes wrong: expired certs, broken CNI, broken CoreDNS, apiserver failure, etcd failure, webhook-blocked apiserver. Drill the disasters before they happen.',
)
