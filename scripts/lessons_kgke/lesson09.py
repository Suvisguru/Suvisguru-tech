"""K-GKE G9 — GKE Troubleshooting (GCP-Specific failure patterns + diagnostic surfaces)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GKE GCP-specific failure patterns + diagnostic toolkit.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Plant Doctor's Hut — GCP-specific triage</text>
  <rect x="40" y="70" width="320" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="200" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">six failure patterns</text>
  <text x="200" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">1. IAM / RBAC + WIF token issues</text>
  <text x="200" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">2. Autopilot admission rejection</text>
  <text x="200" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">3. Node pool / MIG failure · IP exhaustion</text>
  <text x="200" y="144" text-anchor="middle" font-size="9" fill="#FFFFFF">4. NEG health · Ingress · firewall · NAT/SNAT · DNS</text>
  <text x="200" y="157" text-anchor="middle" font-size="9" fill="#FFFFFF">5. Storage attach failures</text>
  <text x="200" y="170" text-anchor="middle" font-size="9" fill="#FFFFFF">6. Release-channel / maintenance-exclusion issues</text>
  <rect x="375" y="70" width="345" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="547" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">diagnostic surfaces</text>
  <text x="547" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">gcpdiag (GCP-aware preflight + RCA)</text>
  <text x="547" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">GKE Recommender</text>
  <text x="547" y="131" text-anchor="middle" font-size="9" fill="#FBF1D6">Logs Explorer + Cloud Trace</text>
  <text x="547" y="144" text-anchor="middle" font-size="9" fill="#FBF1D6">Cloud Status Dashboard (GCP-side)</text>
  <text x="547" y="157" text-anchor="middle" font-size="9" fill="#FBF1D6">Audit Logs + Activity</text>
  <text x="547" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">always check Cloud Status first</text>
</svg>"""


LESSON = LessonSpec(
    num="09",
    title_short="GKE troubleshooting",
    title_full="G9 · GKE Troubleshooting (GCP-Specific)",
    title_html="K-GKE G9 · GKE Troubleshooting",
    module_eyebrow="Module G9 · the Plant Doctor's Hut — GCP-specific triage",
    hero_sub_html='Six GCP-specific GKE failure patterns. <strong>Identity:</strong> IAM/RBAC mismatch + Workload Identity Federation token issues. <strong>Autopilot:</strong> admission rejections + resource-mutation surprises. <strong>Compute:</strong> node-pool / MIG failures + IP exhaustion. <strong>Network:</strong> NEG health-check failures + Ingress provisioning + firewall blocks + Cloud NAT/SNAT + DNS. <strong>Storage:</strong> attach failures. <strong>Lifecycle:</strong> release-channel / maintenance-exclusion issues. <strong>Toolkit:</strong> <code>gcpdiag</code>, <strong>GKE Recommender</strong>, <strong>Logs Explorer</strong>, <strong>Cloud Status Dashboard</strong>, Audit Logs.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Multiple alerts firing: nodes won\'t scale up, a Pod throws WIF 401, NEG backends report unhealthy, Ingress provisioning stuck. You start digging into kubectl logs but auth fails — your IAM role was rotated last week and the new role doesn\'t have <em>Kubernetes Engine Cluster Viewer</em>. <em>You can\'t even reach the cluster to diagnose.</em> Today\'s lesson: an ordered playbook for GCP-specific GKE failures + the diagnostic surfaces that surface root cause fast.",
    stamp_html="<strong>Six GCP-specific patterns: IAM/WIF, Autopilot admission, node pool / IP exhaustion, NEG / firewall / NAT / DNS, storage attach, release-channel. Always check Cloud Status first; then gcpdiag; then Audit Logs + Logs Explorer; then GKE Recommender for next-step suggestions.</strong>",
    district_pin="kg-plot09",
    district_label="Plant Doctor's Hut",
    sections=[
        Section(
            eyebrow="Section 1.1 · identity + Autopilot",
            h2="Identity + Autopilot failure patterns",
            body_html="""    <p><strong>1. IAM / RBAC mismatch</strong>: kubectl returns <em>403 Forbidden</em> after auth succeeds. Causes: user has no Kubernetes Engine role at cluster scope; user has KE role but no in-cluster RoleBinding (with Azure-style RBAC active); group propagation delayed; IAM Conditions excluding the request context. <strong>Diagnose:</strong> <code>gcloud auth print-identity-token</code> + <code>kubectl auth can-i</code> + check IAM bindings on the cluster + the user\'s group memberships.</p>
    <p><strong>Workload Identity Federation token issues:</strong> Pod gets 401/403 calling GCP APIs. Causes:
    <ul>
      <li>K8s SA annotation has wrong G-SA email.</li>
      <li>WIF Pool doesn\'t have a federated credential matching the cluster\'s OIDC issuer + SA subject.</li>
      <li>G-SA missing IAM role on target resource (Storage / BigQuery / Pub/Sub).</li>
      <li>Cluster recreated → new OIDC issuer URL → federated credential trust mismatch.</li>
    </ul>
    Diagnose: gcpdiag + check WIF Pool federated credentials + check Pod\'s SA annotation + check G-SA IAM grants.</p>
    <p><strong>2. Autopilot admission rejection</strong>: Pod fails to schedule with admission error. Autopilot blocks: privileged / hostNetwork / hostPath / hostIPC / hostPID / not-Compute-Class-compatible Pods. <em>Resource mutation surprises</em>: Autopilot may adjust requests upward to its minimum (e.g., request 50m CPU → mutated to 250m) — surprising for cost calculations. Fix: check Autopilot admission webhook events; either rewrite the workload to comply, OR use Autopilot workload class on Standard for that specific workload.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · compute + network",
            h2="Compute + network failure patterns",
            body_html="""    <p><strong>3. Node pool / MIG provisioning failures</strong>: cluster create or scale-up fails with <em>OperationFailure: ZONE_RESOURCE_POOL_EXHAUSTED</em> (specific SKU temporarily unavailable in zone), <em>quota exceeded</em>, or <em>SKU not available</em>. Fix paths: switch zones; switch SKU (use <code>gcloud compute machine-types list</code>); request quota increase via Cloud Console; consider NAP for SKU flexibility (Compute Class with multiple SKU options + Spot fallback).</p>
    <p><strong>IP exhaustion</strong> (covered in G3): VPC-native cluster\'s Pod secondary range exhausted. Pods stuck Pending with no IPs even on free-CPU nodes. Fix: cannot resize range in place — create new node pool with larger Pod CIDR; drain old pool. Pre-empt: <code>gcpdiag lint --type=cluster</code> warns on undersized ranges.</p>
    <p><strong>4. NEG health-check failures</strong>: Ingress backends 100% unhealthy. Almost always: <em>firewall rule allowing GFE health-check ranges <code>35.191.0.0/16</code> + <code>130.211.0.0/22</code> was removed</em>. Diagnose: <code>gcloud compute firewall-rules list</code> + check NEG backend health in Cloud Console. Fix: restore the firewall rule.</p>
    <p><strong>Ingress provisioning</strong>: Ingress / Gateway stays in <em>Pending</em>. Causes: missing or wrong GatewayClass; missing managed cert; missing backend Service annotation for NEG; backend service quota; project not authorised for the global LB SKU. Diagnose: <code>kubectl describe ingress</code> + <code>kubectl describe gateway</code> + Audit Logs for LB API errors.</p>
    <p><strong>Firewall blocks</strong>: blanket-deny defaults plus an unrelated firewall change can break Pod-to-Pod or Pod-to-API traffic. Use VPC Flow Logs + Connectivity Tests to verify.</p>
    <p><strong>Cloud NAT / SNAT issues</strong>: outbound from private cluster fails. Cloud NAT scales NAT ports per attached IP automatically — but per-VM SNAT port quota can run out under burst. Increase NAT port allocation; add Cloud NAT IPs.</p>
    <p><strong>DNS issues</strong>: intermittent name-resolution failures. Use <strong>Cloud DNS for GKE</strong> (<code>--cluster-dns=clouddns</code>) + <strong>NodeLocal DNSCache</strong> for scale + latency. CoreDNS in default mode for compatibility. Diagnose: <code>kubectl exec -- nslookup</code> + Cloud DNS query logs.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · storage + lifecycle",
            h2="Storage attach failures + release-channel / maintenance issues",
            body_html="""    <p><strong>5. Storage attach failures</strong>: PVC bound but Pod stuck mounting. Most common: zone mismatch (single-zone PD; Pod scheduled in different zone) — see G5 WaitForFirstConsumer. Other causes: PD already attached to a different node (split-brain after node failure), CMEK key disabled, snapshot in different region, Filestore quota.</p>
    <p><strong>6. Release-channel / maintenance-exclusion issues</strong>:
    <ul>
      <li>Auto-upgrade fired during traffic peak — exclusion missing or scoped wrong (e.g., \"no minor upgrades\" still allowed patches).</li>
      <li>Maintenance exclusion expires before team noticed — surprise upgrade after the freeze.</li>
      <li>Cluster stuck on EOS version — failed pre-flight (deprecated APIs in workloads); GKE auto-upgraded anyway, breaking workloads.</li>
      <li>Channel mismatch between projects — production on Stable, staging on Rapid; staging breaks features prod doesn\'t see for weeks.</li>
    </ul>
    Diagnose: GKE Release Notes + <code>gcloud container operations list</code> + Pub/Sub upgrade notifications history.</p>
    <p><strong>Quota troubleshooting</strong>: cluster CPU / memory / Persistent Disk capacity / IP / Cloud NAT / Cloud LB quotas all bite. Cloud Console → IAM &amp; Admin → Quotas. Alert on quota approaching limit (Cloud Monitoring quota dashboards).</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · diagnostic toolkit",
            h2="Diagnostic toolkit — gcpdiag, GKE Recommender, Logs Explorer, Cloud Status",
            body_html="""    <p><strong><code>gcpdiag</code></strong> — Google\'s open-source diagnostic CLI for GCP. Run <code>gcpdiag lint --project=PROJECT --type=cluster</code> against a GKE project; it executes ~100 checks (IAM, networking, quota, version policy, security baseline, common misconfigurations) and reports findings with recommended actions. <em>The single most useful tool for ad-hoc GKE diagnosis.</em></p>
    <p><strong>GKE Recommender</strong> — built into the GCP Recommender API. Surfaces actionable recommendations on a cluster: \"upgrade to channel X,\" \"Pod Y\'s requests over-provisioned by N%,\" \"node pool Z has unused capacity.\" Available in Cloud Console → GKE → Recommendations. Useful for ongoing optimisation, not incident triage.</p>
    <p><strong>Logs Explorer</strong> — Cloud Logging\'s query UI. Standard playbook for an incident:
    <ul>
      <li>Filter to the cluster + namespace + time window.</li>
      <li>Look at <em>kube-events</em> and <em>kube-apiserver</em> logs first.</li>
      <li>For Workload Identity Federation issues: filter to <code>iam.googleapis.com/Audit</code>.</li>
      <li>For Ingress / NEG: filter to LB + Compute Engine logs.</li>
    </ul>
    Save queries you find useful as Logs Explorer Saved Queries.</p>
    <p><strong>Cloud Status Dashboard</strong> (status.cloud.google.com) — <em>always check first</em>: rules out GCP-side incidents instantly. \"GKE in us-east1 degraded — partial connectivity issues\" is the kind of message that saves hours of theorising.</p>
    <p><strong>Audit Logs + Activity</strong> — every GCP API call against the cluster + nodes lands in <em>Cloud Audit Logs</em>. Find recent changes by humans / automation (\"who deleted that firewall rule yesterday?\"). Filter by principal, resource, method.</p>
    <p><strong>The standard playbook</strong>: (1) Cloud Status (rule out GCP-side); (2) Audit Logs (recent changes); (3) gcpdiag (run a comprehensive lint); (4) Logs Explorer with saved query (per-incident-type); (5) GKE Recommender (longer-term cleanup, not triage). <em>Most incidents resolve in steps 1-3 if the discipline is wired.</em></p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="Pods stuck Pending across the cluster. Where do you look first to rule out GCP-side trouble?",
            options=[
                ("kubectl logs of every Pod.", False),
                ("Cloud Status Dashboard for GKE + Compute Engine in your region — surfaces region-wide incidents instantly.", True),
                ("Restart the apiserver.", False),
            ],
            feedback="Cloud Status saves hours. If GCP says GKE is degraded in your region, you wait + page Google, not chase Pod-level red herrings.",
        ),
    },
    before_after_before='<p>Pre-gcpdiag, GKE troubleshooting was guess-and-grep — gcloud commands one-by-one, custom Bash scripts to verify common misconfigurations, no consolidated lint. Workload Identity errors looked like generic 401s. NEG-health-check firewall regressions surfaced only as 503s with no obvious cause. Quota issues bit during scale-out events. Cloud Status was a forum reflex, not a runbook step.</p>',
    before_after_after='<p>Modern GKE: <strong>gcpdiag</strong> as a comprehensive GCP-aware lint (~100 checks); <strong>GKE Recommender</strong> for ongoing optimisation; <strong>Logs Explorer + Cloud Trace + Audit Logs</strong> for incident root-cause; <strong>Cloud Status Dashboard</strong> for ruling out GCP-side. Plus the canonical playbook for the six failure patterns. <em>MTTR drops from hours to minutes for known patterns.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Triage discipline + the right diagnostic surfaces are the difference between a 15-minute incident and a 4-hour war room.</em></p>',
    analogy_intro_html='''<p>The <strong>Plant Doctor\'s Hut</strong> at K-Garden is where you go when something\'s wrong. The triage nurse asks the same questions every time, in the same order.</p>
    <p>First: <em>\"Is anyone else in any garden reporting this?\"</em> (Cloud Status Dashboard.) If half the gardens worldwide have the same complaint, it\'s the head-gardener network having a bad day, not your plot.</p>
    <p>Second: <em>\"Did anything change recently?\"</em> (Cloud Audit Logs + Activity.) Someone removed the visitor-pass for the Inspector last night — that\'s why the NEG plant inspection failed today.</p>
    <p>Third: <em>\"Run the standard checkup.\"</em> (gcpdiag.) The standard checkup is a 100-question form — IAM grants, network ranges, quota, version policy, common misconfigurations — and lights up exactly which questions failed.</p>
    <p>Fourth: <em>\"What does the building manager log say?\"</em> (Logs Explorer with saved queries.) The garden\'s building manager records every door entry; saved queries scope to the right cluster + namespace + window.</p>
    <p>The wall has six common diagnoses: identity + Autopilot rejection + node pool / IP exhaustion + NEG / firewall / NAT / DNS + storage attach + release-channel issues — each with a one-page treatment.</p>''',
    translation_rows=[
        ("Triage nurse first question", "Cloud Status Dashboard — GCP-side incident?"),
        ("\"Did anything change recently?\"", "Cloud Audit Logs + Activity"),
        ("Standard 100-question checkup", "gcpdiag (lint --type=cluster)"),
        ("Building manager journal", "Logs Explorer (Cloud Logging)"),
        ("Wall of common diagnoses", "Six GCP-specific failure patterns"),
        ("Sealed-envelope rejection", "Workload Identity Federation token issue"),
        ("Robot Caretaker refused the seedling", "Autopilot admission rejection"),
        ("Greenhouse SKU sold out", "Node pool / MIG provisioning failure"),
        ("Plant address book exhausted", "Pod IP secondary range exhaustion"),
        ("\"Inspector pass removed\"", "GFE health-check firewall regression"),
        ("Locker in another zone", "PD attach failure (zone mismatch)"),
        ("\"Surprise pruning\"", "Auto-upgrade outside expected window"),
        ("Optimisation recommendations", "GKE Recommender"),
    ],
    analogy_stops="A clinic patient describes symptoms; GKE clusters emit machine-readable signals you must instrument first. Without diagnostic-settings + Logs Explorer saved queries, you\'re blind.",
    eli5="When something hurts in the garden, you go to the doctor\'s hut. The doctor asks the same questions in order: is anyone else hurting? did anything change yesterday? let me run the standard checkup. The wall has six common diagnoses — yours is probably one of them.",
    eli10="GKE troubleshooting = identify pattern + run the right diagnostic. Six GCP-specific patterns: IAM/RBAC + WIF token, Autopilot admission, node pool / MIG / IP exhaustion, NEG / firewall / NAT / DNS, storage attach, release-channel / maintenance-exclusion. Toolkit: gcpdiag (comprehensive lint), GKE Recommender (ongoing optimisation), Logs Explorer (Cloud Logging UI), Cloud Status Dashboard (GCP-side incidents), Audit Logs (recent changes). Standard playbook: Cloud Status → Audit Logs → gcpdiag → Logs Explorer → GKE Recommender.",
    scenarios=[
        Scenario(
            name="Region-wide GKE degradation — Cloud Status saved hours",
            body="At 14:30 the SaaS\'s on-call sees ImagePullBackOff across 6 clusters. First instinct: bug, our images, our pipeline. Engineer checks Cloud Status: <em>GCR/Artifact Registry incident in us-east1 — increased latency on image pulls.</em> <em>Confirms GCP-side; team waits 22 min for Google to mitigate; no code change needed.</em> Without Cloud Status: hours of debugging private images.",
        ),
        Scenario(
            name="WIF 401 → cluster-recreated OIDC issuer mismatch",
            body="A Pod that worked yesterday returns 401 from BigQuery. Federated credential and IAM grants untouched. Engineer checks: cluster was recreated overnight by IaC pipeline (Audit Logs). New cluster has new OIDC issuer URL; WIF Pool federated credential trusts old. <em>Update fed cred issuer; auth restored in 2 minutes.</em>",
        ),
        Scenario(
            name="NEG health 503s root-caused by missing firewall rule (G3 recap)",
            body="An ingress backend started returning 503s. NEG marked all Pod IPs unhealthy. Root cause: Terraform refactor removed the firewall rule allowing 35.191.0.0/16 + 130.211.0.0/22 (GFE health-check IPs). Restored rule; NEG marked Pods healthy in 30 seconds. <em>Postmortem: pin the GFE-allow rule with a Terraform comment so future refactors don\'t remove it.</em>",
        ),
        Scenario(
            name="gcpdiag flagged the issue before the incident",
            body="Platform team ran <code>gcpdiag lint --type=cluster --project=prod</code> as part of a quarterly hygiene sweep. gcpdiag flagged: \"Pod secondary range projected to exhaust at 850 nodes; cluster currently at 780.\" Team created a new node pool with larger Pod CIDR + drain-and-replace plan; executed during next maintenance window. <em>The incident never happened.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"If kubectl works, the cluster is fine.\"",
            truth="kubectl is one signal — apiserver responds. Plenty can break around it: WIF, NEG, Cloud NAT, storage, identity, networking, IP exhaustion. Modern GKE troubleshooting goes beyond kubectl: Cloud Status, Audit Logs, gcpdiag, Logs Explorer.",
        ),
        Misconception(
            myth="\"<code>kubectl exec</code> is the right way to debug node-level issues.\"",
            truth="kubectl exec puts you inside a container, not on the node. Modern GKE doesn\'t expose node SSH on Autopilot; even on Standard, SSH is discouraged for debug. <strong>Use <code>gcpdiag</code></strong> for cluster + node-level diagnosis. For per-node syscall / packet inspection, deploy a debug Pod with the right SecurityContext (Standard) — Autopilot blocks privileged debug.",
        ),
        Misconception(
            myth="\"Cloud Status is for GCP outages; my cluster issues won\'t be there.\"",
            truth="Cloud Status surfaces partial-region incidents that affect specific GKE features (e.g., \"GKE control-plane upgrades degraded in us-east1\"). Many \"my cluster is broken\" incidents start as Cloud Status entries that the team just didn\'t check. Always check Cloud Status first.",
        ),
    ],
    flashcards=[
        Flashcard(front="Six GCP-specific GKE failure patterns?", back="(1) IAM/RBAC + WIF token issues, (2) Autopilot admission rejection + resource mutation, (3) node pool / MIG provisioning + IP exhaustion, (4) NEG health + Ingress + firewall + Cloud NAT/SNAT + DNS, (5) storage attach failures, (6) release-channel / maintenance-exclusion issues."),
        Flashcard(front="What does <code>gcpdiag</code> do?", back="Google\'s open-source GCP-aware diagnostic CLI. Run <code>gcpdiag lint --project=P --type=cluster</code> for ~100 GKE checks (IAM, networking, quota, version, security baseline, common misconfigs). Reports findings + recommended actions. The single most useful ad-hoc GKE diagnostic tool."),
        Flashcard(front="What is GKE Recommender?", back="Surfaces actionable recommendations on a cluster: upgrade channel, over-provisioned Pod requests, unused node pool capacity, security findings. Cloud Console → GKE → Recommendations. For ongoing optimisation, not incident triage."),
        Flashcard(front="What\'s the standard GKE triage playbook?", back="(1) Cloud Status Dashboard (rule out GCP-side). (2) Cloud Audit Logs + Activity (recent changes). (3) gcpdiag (comprehensive lint). (4) Logs Explorer with saved query (per-incident-type). (5) GKE Recommender (longer-term cleanup)."),
        Flashcard(front="WIF token 401 — most common cause?", back="<strong>Cluster\'s OIDC issuer URL changed</strong> (cluster recreated; pinned issuer in WIF Pool federated credential is now stale). Diagnose: <code>gcloud container clusters describe ... --format='value(workloadIdentityConfig.workloadPool, identityServiceConfig)'</code>; compare against WIF Pool federated credential issuer."),
        Flashcard(front="Pod stuck Pending — \"InsufficientPodCapacity\" — what\'s likely?", back="Pod secondary range exhaustion. Cluster grew past planned-for max-nodes × max-pods-per-node. Cannot resize range in place — create new node pool with larger Pod CIDR; drain old pool. Pre-empt with gcpdiag."),
        Flashcard(front="Auto-upgrade fires during traffic peak — what config prevents this?", back="<strong>Maintenance exclusion</strong> for the date range, scope <em>no upgrades</em> (or <em>no minor</em> if patches still wanted). Maximum exclusion length depends on scope. Set both maintenance window (when upgrades may fire) AND exclusions (when they may not)."),
        Flashcard(front="Why is checking Cloud Status the first triage step?", back="Most likely path to ruling out GCP-side incidents in 30 seconds. Saves hours of theorising on user-side root cause when the issue is Google\'s — \"GKE control plane degraded in us-east1\" stops the wild-goose chase immediately."),
    ],
    quizzes=[
        Quiz(
            prompt="kubectl returns <code>403 Forbidden</code> for a user. They authenticated cleanly via gcloud (no auth error). What\'s the diagnostic ladder?",
            answer="(1) Confirm auth: <code>gcloud auth list</code> + <code>kubectl auth whoami</code> (with a recent kubectl). (2) Check IAM: does the user have <em>Kubernetes Engine Cluster Viewer / Developer / Admin</em> at cluster or project scope? <code>gcloud projects get-iam-policy</code>. (3) Check K8s RBAC: any RoleBinding referencing the user / group? <code>kubectl get rolebindings,clusterrolebindings -A | grep USER</code>. (4) Check IAM Conditions: does the user\'s grant exclude their request context (network, time)? (5) Group propagation: if added to a group recently, can take 10-30 min to surface. (6) Specific resource: they have Reader at project but the resource is in a namespace they\'re not bound to.",
        ),
        Quiz(
            prompt="A Pod can\'t fetch a secret from Secret Manager via Secret Manager CSI. Pod events: <em>\"failed to get secret: not authorized.\"</em> Walk through diagnosis.",
            answer="(1) Identify the Pod\'s SA + the SA\'s annotation <code>iam.gke.io/gcp-service-account</code>. (2) Find the G-SA with that email; check its IAM role on the specific Secret Manager secret (Secret Manager Secret Accessor). (3) Verify Workload Identity Federation Pool federated credential matches the cluster\'s OIDC issuer + the SA subject. Common gotcha: cluster recreated → OIDC issuer changed; fed cred trust still points at old issuer. (4) Verify Secret Manager firewall (if VPC SC enabled). (5) Check Secret Manager CSI driver logs (<code>kubectl logs -n kube-system -l app=secrets-store-csi-driver</code>) for the precise auth error. (6) Run <code>gcpdiag lint --type=cluster</code> — often surfaces the WIF mismatch automatically.",
        ),
        Quiz(
            prompt="Saturday, 03:00. Cluster auto-upgrade fired and is now stuck. PagerDuty pages on-call. They open kubectl — auth fails. What\'s the right move?",
            answer="<strong>(1) Check Cloud Status Dashboard first</strong> — is GKE degraded? IAM degraded? Cloud Logging degraded? If yes: wait, page Google, communicate GCP-side cause. <strong>(2) If GCP-side healthy</strong>, pivot to alternate access: break-glass IAM grant via PIM (just-in-time elevation), MFA on a phone, gcloud from a fresh VM with a service account. <strong>(3) Once kubectl works</strong>: <code>gcloud container operations list</code> for upgrade state, <code>kubectl get events --sort-by=.lastTimestamp</code>, Logs Explorer filtered to apiserver / scheduler / cluster-autoscaler logs. Most likely: PDB violation (G6/A9 — fix surge or PDB), or deprecated API blocking (gcpdiag would have caught this in pre-flight; today fix the API in workloads, resume).",
            cyoa=True,
            cyoa_tag="how the on-call worked through it",
        ),
    ],
    glossary=[
        GlossaryItem(name="Cloud Status Dashboard", definition="status.cloud.google.com — per-product / per-region GCP incident view. First triage step."),
        GlossaryItem(name="Cloud Audit Logs", definition="Every GCP API call against your project. Used to find recent changes by humans / automation."),
        GlossaryItem(name="gcpdiag", definition="Google\'s open-source GCP diagnostic CLI. ~100 checks for GKE clusters covering IAM, networking, quota, version, security."),
        GlossaryItem(name="GKE Recommender", definition="Cloud Recommender API surface for GKE — actionable recommendations on a cluster. For ongoing optimisation."),
        GlossaryItem(name="Logs Explorer", definition="Cloud Logging\'s query UI. Standard filters by cluster, namespace, log name, severity. Saved queries."),
        GlossaryItem(name="ZONE_RESOURCE_POOL_EXHAUSTED", definition="Specific SKU temporarily unavailable in zone. Fix: switch zone or SKU; consider NAP."),
        GlossaryItem(name="Pod IP exhaustion", definition="VPC-native cluster\'s Pod secondary range exhausted. Cannot resize in place — create new pool."),
        GlossaryItem(name="GFE health-check firewall", definition="Allow 35.191.0.0/16 + 130.211.0.0/22 to Pod range — required for NEG-backed LB health checks."),
        GlossaryItem(name="Cloud NAT SNAT exhaustion", definition="Per-VM SNAT port quota under burst. Increase NAT port allocation; add Cloud NAT IPs."),
        GlossaryItem(name="Maintenance exclusion expiry", definition="Exclusion auto-expires; surprise upgrade after the freeze. Renew before expiry; alert on expiry approaching."),
        GlossaryItem(name="Autopilot admission webhook", definition="Built-in Autopilot webhook that blocks privileged / hostNetwork / hostPath / etc. Cannot be disabled."),
        GlossaryItem(name="Cloud Trace", definition="Used in troubleshooting to find slow downstream dependencies; see G7."),
    ],
    recap_lead='Six GCP-specific patterns + diagnostic toolkit (Cloud Status → Audit Logs → gcpdiag → Logs Explorer → GKE Recommender). MTTR shrinks when triage discipline + telemetry are wired.',
    recap_next='<strong>Next — G10: K-GKE Capstone.</strong> Regional Autopilot with Gateway API (multi-cluster) + Workload Identity Federation + Binary Authorization + GMP + Backup for GKE + Config Sync from Git + AI inference workload with Inference Gateway.',
)
