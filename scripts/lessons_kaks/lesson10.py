"""K-AKS A10 — AKS Troubleshooting (Azure-Specific failure patterns + diagnostic surfaces)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AKS Azure-specific failure patterns + the diagnostic toolkit.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Health Clinic — Azure-specific failure triage</text>
  <rect x="50" y="60" width="320" height="130" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="210" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">eight failure patterns</text>
  <text x="210" y="98" text-anchor="middle" font-size="9" fill="#FFFFFF">1. Entra / kubelogin auth failure</text>
  <text x="210" y="111" text-anchor="middle" font-size="9" fill="#FFFFFF">2. Azure RBAC vs K8s RBAC mismatch</text>
  <text x="210" y="124" text-anchor="middle" font-size="9" fill="#FFFFFF">3. VMSS / quota / SKU not available</text>
  <text x="210" y="137" text-anchor="middle" font-size="9" fill="#FFFFFF">4. Azure CNI IP exhaustion / CoreDNS</text>
  <text x="210" y="150" text-anchor="middle" font-size="9" fill="#FFFFFF">5. SNAT exhaustion / LB pending</text>
  <text x="210" y="163" text-anchor="middle" font-size="9" fill="#FFFFFF">6. Disk attach / Key Vault CSI fail</text>
  <text x="210" y="176" text-anchor="middle" font-size="9" fill="#FFFFFF">7. ACR pull / MI permission fail</text>
  <rect x="385" y="60" width="325" height="130" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="547" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">diagnostic surfaces</text>
  <text x="547" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6">kubectl-aks (extension)</text>
  <text x="547" y="115" text-anchor="middle" font-size="9" fill="#FBF1D6">AKS Diagnostic Settings → Log Analytics</text>
  <text x="547" y="130" text-anchor="middle" font-size="9" fill="#FBF1D6">Azure Resource Health</text>
  <text x="547" y="145" text-anchor="middle" font-size="9" fill="#FBF1D6">Activity Log + Defender alerts</text>
  <text x="547" y="160" text-anchor="middle" font-size="9" fill="#FBF1D6">Container Insights workbooks</text>
  <text x="547" y="175" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">always check Resource Health first</text>
</svg>"""


LESSON = LessonSpec(
    num="10",
    title_short="AKS troubleshooting",
    title_full="A10 · AKS Troubleshooting (Azure-Specific)",
    title_html="K-AKS A10 · AKS Troubleshooting",
    module_eyebrow="Module A10 · the Health Clinic — Azure-specific triage",
    hero_sub_html='Eight Azure-specific AKS failure patterns and how to diagnose them. <strong>Identity:</strong> Entra/kubelogin auth, Azure RBAC mismatch. <strong>Compute:</strong> VMSS / quota / SKU. <strong>Network:</strong> Azure CNI IP exhaustion, CoreDNS, SNAT, LB pending, private DNS. <strong>Storage:</strong> disk attach, Key Vault CSI, ACR pull, MI permission. <strong>Lifecycle:</strong> upgrade blocked, node-image failure. <strong>Diagnostic toolkit:</strong> <code>kubectl-aks</code> CLI extension, AKS Diagnostic Settings → Log Analytics + KQL, Azure Resource Health, Activity Log, Container Insights workbooks. <em>Always check Resource Health first.</em>',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Multiple alerts firing: nodes not joining, ACR pulls failing, Key Vault CSI mounts timing out. You start digging into kubectl logs — but kubelogin throws <em>\"failed to refresh token\"</em>. Now you can\'t even reach the cluster. <em>Is the apiserver down? Is Entra down? Is your token expired?</em> You don\'t know which layer to start at. Today\'s lesson: an ordered playbook for Azure-specific AKS failures + the diagnostic surfaces that surface root cause fast.",
    stamp_html="<strong>Eight Azure-specific patterns: Entra/RBAC, VMSS/quota, CNI IPs/CoreDNS, SNAT/LB, disk/KV CSI, ACR/MI, upgrade blocked, node-image. Always check Azure Resource Health first; then kubectl-aks; then KQL on AKS Diagnostic Settings logs.</strong>",
    district_pin="kc-wing10",
    district_label="Health Clinic",
    sections=[
        Section(
            eyebrow="Section 1.1 · identity + compute patterns",
            h2="Identity + compute failure patterns",
            body_html="""    <p><strong>1. Entra / kubelogin failure</strong>: <em>\"failed to refresh token\"</em>, <em>\"AADSTS50158\"</em>, etc. Causes: stale browser session, Conditional Access blocking from current network, tenant trust missing, kubelogin version too old. Fixes: <code>kubelogin clean-cache</code>, re-run <code>az login</code>, check Conditional Access in Entra portal, upgrade kubelogin via az CLI.</p>
    <p><strong>2. Azure RBAC vs K8s RBAC mismatch</strong>: kubectl returns <code>403 Forbidden</code> after auth succeeds. Possible causes: user has neither Azure RBAC role (e.g. <em>Azure Kubernetes Service RBAC Reader</em>) nor in-cluster RoleBinding; cluster has Azure RBAC for K8s enabled but user only has K8s RBAC binding (or vice versa); group membership took time to propagate. Fix: assign the right Azure role at cluster scope OR add a RoleBinding referencing the user\'s Entra OID.</p>
    <p><strong>3. VMSS / quota / SKU not available</strong>: cluster create / scale-out fails with <em>\"OperationNotAllowed: quota exceeded\"</em> or <em>\"SkuNotAvailable\"</em>. Fix paths: request quota increase via Azure portal (Subscriptions → Usage + quotas — can take hours); switch SKU to one available in the region (use <code>az vm list-skus --location ... --output table</code>); switch zones; consider NAP for SKU flexibility.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · network patterns",
            h2="Network failure patterns",
            body_html="""    <p><strong>4. Azure CNI IP exhaustion / CoreDNS autoscaling</strong>: Pods stuck Pending with <em>\"InsufficientFreeAddressesInSubnet\"</em>, or DNS lookups intermittently fail. Causes: traditional Azure CNI burning IPs (migrate to Overlay); CoreDNS replicas insufficient (default = 2). Fixes: migrate to Azure CNI Overlay; tune CoreDNS HPA (autoscaler add-on or manual replica bump); shard DNS via NodeLocal DNSCache.</p>
    <p><strong>5. SNAT exhaustion / LB pending</strong>: outbound calls fail with <em>\"SNAT port allocation\"</em>; or <code>Service: type=LoadBalancer</code> stays in <code>Pending</code>. Fixes: deploy NAT Gateway (covered in A3); investigate LB pending via <code>kubectl describe service</code> — often points to outbound IP quota, AGC reconcile delay, or NSG blocking AKS load-balancer health probes.</p>
    <p><strong>Private DNS issues</strong>: private cluster + custom DNS resolver setup; cluster apiserver FQDN doesn\'t resolve from worker network. Verify Private DNS zone link to the worker VNet; check custom DNS forwarder if hub-spoke topology.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · storage + identity patterns",
            h2="Storage + identity failure patterns",
            body_html="""    <p><strong>6. Disk attach failure</strong>: PVC bound to a Premium SSD in <code>eastus-1</code>; Pod scheduled in <code>eastus-2</code>; attach fails with <em>\"AttachVolume.Attach failed\"</em>. Cause: missing <code>WaitForFirstConsumer</code>. Fix: see A4 — use the default StorageClass or migrate to ZRS.</p>
    <p><strong>Key Vault CSI failure</strong>: <em>\"failed to get secret from Key Vault\"</em>. Causes: Workload Identity federated credential mismatch (cluster recreated → OIDC issuer changed); Key Vault access policy missing the MI; Key Vault firewall blocking the cluster\'s VNet; Secret Rotation poller misconfigured. Diagnose: check the Secrets Store CSI driver logs; verify federated credential and Key Vault access policy; check NSG / Key Vault firewall.</p>
    <p><strong>7. ACR pull failure</strong>: <em>\"ImagePullBackOff: 401 Unauthorized\"</em>. Causes: cluster not attached to the registry (<code>az aks update --attach-acr</code> not run); kubelet identity missing AcrPull role; registry private endpoint not in cluster\'s VNet; image actually doesn\'t exist at that tag. Diagnose: <code>kubectl describe pod</code> for the exact ImagePullBackOff message; verify with <code>az aks check-acr</code>.</p>
    <p><strong>Managed identity failures</strong>: Pod uses Workload Identity → Storage call returns 403. Cause: MI not assigned the right Azure role on the resource; or MI scope is wrong (resource-group vs subscription); or the federated credential subject is wrong. Diagnose: check the Pod\'s SA annotation, federated credential, and MI role assignment.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · lifecycle + diagnostic surfaces",
            h2="Upgrade blocked, node-image failure, and the diagnostic toolkit",
            body_html="""    <p><strong>8. Upgrade blocked</strong>: <em>\"upgrade failed: PodDisruptionBudget violation\"</em> or add-on compatibility check failed. Fixes: tune PDB / surge (covered in A9); upgrade or remove the offending self-installed add-on; check <code>Activity Log</code> for the precise error message.</p>
    <p><strong>Node-image failure</strong>: pool stuck after node-image upgrade. Possible: workload uses an unsupported kernel feature on the new image; AL2 → AL3 migration left a stale image SKU; underlying VMSS scale operation failed. Investigate: <code>kubectl describe nodes</code>, AKS Diagnostic Settings <code>cluster-autoscaler</code> log, Activity Log on the VMSS.</p>
    <p><strong>Diagnostic toolkit:</strong>
    <ul>
      <li><strong><code>kubectl-aks</code></strong> — Azure CLI extension that exposes AKS-specific diagnostics: live node BPF inspection, syscall traces, network captures, ifconfig — <em>without SSH-ing the node</em>.</li>
      <li><strong>AKS Diagnostic Settings → Log Analytics</strong> — apiserver / audit / scheduler / cluster-autoscaler logs queryable via KQL.</li>
      <li><strong>Azure Resource Health</strong> — <em>always check first</em> — surfaces Azure-side incidents affecting the cluster (e.g., regional storage degradation, Entra outage). Eliminates many \"is it me or is it Azure?\" theorising.</li>
      <li><strong>Azure Activity Log</strong> — every Azure API call against the cluster + node resource group. Find who deleted the Public IP that broke ingress.</li>
      <li><strong>Defender for Containers alerts</strong> — security incidents.</li>
      <li><strong>Container Insights workbooks</strong> — pre-built node / Pod / container health views.</li>
    </ul>
    <p><strong>The standard playbook</strong>: (1) Resource Health → ruling out Azure-side; (2) Activity Log → recent changes by humans / automation; (3) AKS Diagnostic Settings logs → control-plane perspective; (4) <code>kubectl describe</code> + <code>kubectl-aks</code> → workload + node perspective; (5) Defender alerts → security angle. <em>Most outages resolve in steps 1-3 if the toolkit is wired in.</em></p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="Pods stuck Pending across the cluster. Where do you look first to rule out Azure-side trouble?",
            options=[
                ("kubectl logs of every Pod.", False),
                ("Azure Resource Health for the cluster + node-pool VMSS — surfaces region-wide AKS, Compute, or VMSS incidents instantly.", True),
                ("Restart the apiserver.", False),
            ],
            feedback="Resource Health saves hours of theorising. If Azure says the region\'s AKS service is degraded, you wait + page Microsoft, not chase Pod-level red herrings.",
        ),
    },
    before_after_before='<p>Pre-AKS-Diagnostic-Settings era: troubleshooting AKS meant <em>guessing</em>. Apiserver logs invisible. No <code>kubectl-aks</code> — node-level inspection meant SSH (which AKS doesn\'t allow) or disruptive debug-Pod schemes. Resource Health was buried; engineers theorised \"is it me or is it Azure?\" for hours. ACR pull failures had three possible causes and no clear surface. Workload Identity errors were opaque — federated credential trust mismatches looked like generic 401s.</p>',
    before_after_after='<p>Modern AKS exposes the diagnostic surface: <strong><code>kubectl-aks</code></strong> for node-level inspection without SSH; <strong>AKS Diagnostic Settings</strong> route apiserver / audit / scheduler / autoscaler logs to Log Analytics for KQL search; <strong>Azure Resource Health</strong> is a one-click ruling-out for Azure-side trouble; <strong>Activity Log</strong> shows every Azure-API change; <strong>Defender alerts</strong> surface security incidents. Plus the canonical playbooks for the eight failure patterns are documented. <em>MTTR drops from hours to minutes for known patterns.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Triage discipline + the right diagnostic surfaces are the difference between a 15-minute incident and a 4-hour war room.</em></p>',
    analogy_intro_html='''<p>The <strong>Health Clinic</strong> on K-Campus is where you go when something\'s wrong. The triage nurse asks the same questions every time, in the same order.</p>
    <p>First question: <em>\"Is anyone else on campus reporting this?\"</em> (Azure Resource Health.) If half the campus has the same complaint, it\'s probably the campus power grid (Azure-side incident), not your symptom. Wait + page the campus utility.</p>
    <p>Second question: <em>\"Did anything change recently?\"</em> (Activity Log.) Someone deleted the campus shuttle stop in front of your building yesterday — that\'s why your students can\'t get to class.</p>
    <p>Third question: <em>\"What does the building manager log say?\"</em> (AKS Diagnostic Settings → Log Analytics → KQL.) The manager\'s journal records every door entry; the syscall-level inspection (<code>kubectl-aks</code>) walks each room.</p>
    <p>The Clinic has eight common diagnoses pinned on the wall (the eight Azure-specific failure patterns). Each diagnosis has a one-page treatment protocol: the cause, the test that confirms, the fix.</p>''',
    translation_rows=[
        ("Triage nurse first question", "Azure Resource Health — Azure-side incident?"),
        ("\"Did anything change recently?\"", "Azure Activity Log — recent Azure-API changes"),
        ("Building manager journal", "AKS Diagnostic Settings → Log Analytics + KQL"),
        ("Walk into rooms without breaking down doors", "<code>kubectl-aks</code> — node-level inspection without SSH"),
        ("Wall of common diagnoses", "Eight Azure-specific failure patterns"),
        ("\"Wrong wing badge\"", "Azure RBAC vs K8s RBAC mismatch"),
        ("\"Sold-out shoe size\"", "VMSS quota / SKU unavailability"),
        ("\"Building street is closed\"", "SNAT exhaustion / LB pending"),
        ("\"Locker is in another zone\"", "Disk attach failure (cross-AZ)"),
        ("\"Vault key wouldn\'t turn\"", "Key Vault CSI failure"),
        ("\"Mailroom rejected the package\"", "ACR pull failure"),
        ("Security ward alerts", "Defender for Containers alerts"),
    ],
    analogy_stops="A clinic patient describes symptoms; AKS clusters emit machine-readable signals you must instrument first. The metaphor underplays observability prerequisites — without diagnostic settings + Container Insights, you\'re blind.",
    eli5="When something hurts, you go to the clinic. The nurse asks the same questions every time: is everyone else hurting? did anything change yesterday? what does your watch say? Then she looks at the wall — your problem is probably one of eight common ones, and each has a one-page treatment.",
    eli10="AKS troubleshooting = identify pattern + run the right diagnostic. Eight Azure-specific patterns: Entra/kubelogin auth, Azure-vs-K8s RBAC mismatch, VMSS / quota / SKU, CNI IP exhaustion + CoreDNS, SNAT + LB pending + private DNS, disk attach + Key Vault CSI, ACR pull + MI permission, upgrade blocked + node-image. Toolkit: <code>kubectl-aks</code> (node inspection without SSH), AKS Diagnostic Settings + KQL (apiserver / audit / scheduler / autoscaler logs), Azure Resource Health (rule out Azure-side first), Activity Log (recent changes), Defender alerts. Standard playbook: Resource Health → Activity Log → Diagnostic Settings KQL → kubectl describe + kubectl-aks → Defender.",
    scenarios=[
        Scenario(
            name="Region-wide ACR throttling — Resource Health saved hours",
            body="At 14:30 the SaaS\'s on-call sees ImagePullBackOff across 12 clusters. First instinct: bug, our images, our pipeline. Engineer checks Azure Resource Health: <em>ACR throttling event in eastus2</em>. <em>Confirms Azure-side; the team waits 18 minutes for Microsoft to mitigate; no code change needed.</em> Without Resource Health: 4 hours of debugging private images.",
        ),
        Scenario(
            name="Workload Identity 401 → cluster-recreated OIDC issuer mismatch",
            body="A Pod that worked yesterday returns 401 from Key Vault. Federated credential and access policy untouched. Engineer checks: cluster was recreated overnight (Activity Log). New cluster has new OIDC issuer URL; federated credential still trusts the old one. <em>Update fed cred subject; auth restored in 2 minutes.</em>",
        ),
        Scenario(
            name="Bursty SaaS — SNAT exhaustion at peak hour",
            body="Black Friday peak; outbound to Stripe API fails with <em>SNAT port allocation</em>. Cluster had default LB-shared SNAT. Emergency: provision NAT Gateway via UDR (since outbound type is immutable); fail over egress through it within 25 minutes. Postmortem: NAT Gateway part of cluster creation from now on.",
        ),
        Scenario(
            name="kubectl-aks node inspection diagnoses kernel issue",
            body="A node throws random Pod restarts; <code>kubectl describe</code> blames \"runtime error.\" Engineer runs <code>kubectl-aks node-inspect-tcpdump</code> — captures network traffic; finds an unusual SYN flood from a misconfigured client. <em>No SSH, no debug Pod, root cause in 8 minutes.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"If kubectl works, the cluster is fine.\"",
            truth="kubectl is one signal — apiserver responds. Plenty can break around it: ACR pull, Key Vault CSI, SNAT, identity, networking. Modern AKS troubleshooting goes beyond kubectl: Resource Health, Activity Log, Diagnostic Settings + KQL, kubectl-aks for node-level signals.",
        ),
        Misconception(
            myth="\"<code>kubectl exec</code> into a Pod is the right node-debugging tool.\"",
            truth="kubectl exec puts you inside a container, not on the node. AKS doesn\'t allow node SSH. Use <strong><code>kubectl-aks</code></strong> for node-level inspection — runs as a privileged Pod on the target node, exposes BPF inspection, ifconfig, syscall traces, packet captures. Built for AKS specifically; designed for triage."),
        Misconception(
            myth="\"Diagnostic Settings logs are nice-to-have.\"",
            truth="They\'re <em>foundational</em>. Without apiserver + audit logs in Log Analytics you can\'t answer \"who did X?\", \"when did Y stop working?\", \"what changed?\" — the most common questions in any incident. Wire diagnostic settings on every cluster from creation, not after the first outage.",
        ),
    ],
    flashcards=[
        Flashcard(front="Eight Azure-specific AKS failure patterns?", back="(1) Entra/kubelogin auth, (2) Azure RBAC vs K8s RBAC mismatch, (3) VMSS / quota / SKU, (4) Azure CNI IP exhaustion + CoreDNS, (5) SNAT exhaustion + LB pending + private DNS, (6) disk attach + Key Vault CSI, (7) ACR pull + MI permission, (8) upgrade blocked + node-image failure."),
        Flashcard(front="What does <code>kubectl-aks</code> do?", back="Azure CLI extension that runs node-level diagnostics on AKS nodes <em>without SSH</em> — BPF inspection, syscall traces, packet captures, ifconfig, network probes. Replaces the SSH-into-the-node workflow that AKS doesn\'t allow."),
        Flashcard(front="What does AKS Diagnostic Settings expose?", back="Apiserver, audit, audit-admin, kube-controller-manager, kube-scheduler, cluster-autoscaler, cloud-controller-manager log categories. Route to Log Analytics (KQL search), Event Hub (SIEM), or Storage (long-term archive)."),
        Flashcard(front="When do you check Azure Resource Health?", back="<strong>First</strong>, on every incident. Tells you whether Azure itself is degraded for your cluster, region, or service. Saves hours of theorising on user-side root cause when the issue is Azure-side."),
        Flashcard(front="Common cause of Workload Identity 401?", back="Federated credential mismatch — wrong OIDC issuer (e.g. cluster recreated; new issuer URL), wrong subject (typo in SA name), missing role assignment on the MI for the target resource."),
        Flashcard(front="ACR pull diagnostic command?", back="<code>az aks check-acr --name &lt;cluster&gt; --resource-group &lt;rg&gt; --acr &lt;registry&gt;.azurecr.io</code> — runs a self-test from the cluster against the registry; surfaces RBAC, networking, and DNS issues end-to-end."),
        Flashcard(front="Why does CoreDNS need autoscaling on big AKS clusters?", back="Default 2 CoreDNS replicas. Large clusters = millions of DNS queries/sec; replicas saturate. Symptoms: intermittent DNS lookup failures, increased Pod start latency. Fix: tune the CoreDNS autoscaler add-on or NodeLocal DNSCache."),
        Flashcard(front="What\'s the standard AKS triage playbook?", back="(1) Azure Resource Health (rule out Azure-side). (2) Activity Log (recent changes by humans/automation). (3) AKS Diagnostic Settings logs via KQL (control-plane perspective). (4) kubectl describe + kubectl-aks (workload + node). (5) Defender alerts (security)."),
    ],
    quizzes=[
        Quiz(
            prompt="kubectl returns <code>403 Forbidden</code> for a user. They authenticated cleanly via kubelogin (no auth error). What\'s the diagnostic ladder?",
            answer="(1) Confirm authentication actually worked: <code>kubectl auth whoami</code> — should show their Entra OID. (2) Check Azure RBAC if cluster has Azure RBAC for K8s enabled: do they have one of <em>Azure Kubernetes Service RBAC Reader/Writer/Admin/Cluster Admin</em> at cluster or namespace scope? (3) Check K8s RBAC: any RoleBinding referencing the user\'s OID or group? (4) Group propagation: if added to a group recently, can take 1-15 min to surface. (5) The specific resource being accessed — e.g., they have Reader cluster-wide but the resource is in a namespace they\'re not bound to.",
        ),
        Quiz(
            prompt="A Pod can\'t mount a Key Vault secret via Secrets Store CSI. The error in the Pod events is <em>\"failed to get secret from Key Vault: not authorized.\"</em> Walk through diagnosis.",
            answer="(1) Identify the Pod\'s SA + the SA\'s annotation <code>azure.workload.identity/client-id</code>. (2) Find the Entra app or MI with that client-id; check its <strong>federated credential</strong> — does subject match <code>{cluster-OIDC}/serviceaccount/{ns}/{sa}</code>? Common gotcha: cluster recreated → OIDC issuer changed; federated credential still points at old issuer. (3) Verify Key Vault <strong>access policy</strong> (or RBAC if KV is on RBAC mode) grants the MI <em>Get Secret</em> on the specific secret. (4) Verify Key Vault <strong>firewall</strong> allows the cluster\'s VNet (or that Private Endpoint is wired). (5) Inspect Secrets Store CSI driver logs (<code>kubectl logs -n kube-system -l app=secrets-store-csi-driver</code>) for the precise auth error.",
        ),
        Quiz(
            prompt="Saturday, 03:00. Cluster upgrade auto-fired and is now stuck. PagerDuty pages on-call. They open kubectl — kubelogin throws an error. What\'s the right move?",
            answer="<strong>(1) Check Azure Resource Health first</strong> — is Entra ID degraded? AKS service degraded in this region? If yes: wait, page Microsoft, communicate Azure-side cause. <strong>(2) If Azure-side is healthy</strong>, pivot to alternate access: the break-glass Entra group (PIM-elevated for 30 min), MFA on a phone, kubelogin from a fresh laptop. <strong>(3) Once kubectl works</strong>: <code>az aks show</code> for upgrade state, <code>kubectl get events --sort-by=.lastTimestamp</code>, KQL on AKS Diagnostic Settings <code>kube-controller-manager</code> log to find the precise stall. Most likely: PDB violation (covered in A9 — fix surge or PDB), or add-on compatibility check failed (the upgrade pauses; fix the add-on, resume).",
            cyoa=True,
            cyoa_tag="how the on-call worked through it",
        ),
    ],
    glossary=[
        GlossaryItem(name="Azure Resource Health", definition="Per-resource Azure incident view. Tells you whether Azure itself is degraded for your cluster / region / service."),
        GlossaryItem(name="Azure Activity Log", definition="Audit log of every Azure API call against your subscription. Used to find recent changes by humans / automation."),
        GlossaryItem(name="AKS Diagnostic Settings", definition="Configuration that ships AKS control-plane logs (apiserver, audit, scheduler, autoscaler, etc.) to Log Analytics / Event Hub / Storage."),
        GlossaryItem(name="kubectl-aks", definition="Azure CLI / kubectl extension for AKS-specific node-level diagnostics without SSH (BPF, syscalls, packet captures)."),
        GlossaryItem(name="az aks check-acr", definition="Self-test command that verifies the cluster can authenticate + pull from a specific ACR end-to-end."),
        GlossaryItem(name="SNAT exhaustion", definition="Egress failure when shared LB SNAT ports run out. Fixed by NAT Gateway."),
        GlossaryItem(name="LB pending", definition="A Service: type=LoadBalancer stays in <code>Pending</code>. Causes: outbound IP quota, AGC reconcile delay, NSG blocking health probes."),
        GlossaryItem(name="ImagePullBackOff", definition="Pod stuck because the kubelet can\'t pull the image. Causes: ACR not attached, registry firewall, MI permission, image tag missing."),
        GlossaryItem(name="Pod Security Admission violation", definition="Pod rejected at admission because PSA enforce level is restricted and the Pod requests forbidden options (root, hostPath, etc.)."),
        GlossaryItem(name="VMSS quota", definition="Azure subscription limit on VM cores / SKU per region. Hit during cluster create / scale-out. Increase via portal."),
        GlossaryItem(name="CoreDNS autoscaling", definition="DaemonSet/Deployment that scales CoreDNS replicas. Default 2; large clusters need autoscaler or NodeLocal DNSCache."),
        GlossaryItem(name="Defender for Containers alerts", definition="Security incident notifications from Defender. Often the first surface for Pod-level threats (suspicious shell, miner, lateral movement)."),
    ],
    recap_lead='Eight Azure-specific patterns + the diagnostic toolkit (Resource Health → Activity Log → Diagnostic Settings KQL → kubectl describe + kubectl-aks → Defender). MTTR shrinks when triage discipline + telemetry are wired.',
    recap_next='<strong>Next — A11: Capstone.</strong> Build a private AKS Automatic with Cilium dataplane + Workload Identity + AGC (Gateway API) + Defender for Containers + Managed Prometheus/Grafana + Flux v2 GitOps + LTS upgrade & DR runbooks.',
)
