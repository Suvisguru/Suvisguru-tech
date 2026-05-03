# K-GKE G9 — G9 · GKE Troubleshooting (GCP-Specific)

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G9 · GKE Troubleshooting
> Companion preview: `/preview-kubernetes-gke-lesson-09.html`.

---

**🎯 If you remember nothing else:** **Six GCP-specific patterns: IAM/WIF, Autopilot admission, node pool / IP exhaustion, NEG / firewall / NAT / DNS, storage attach, release-channel. Always check Cloud Status first; then gcpdiag; then Audit Logs + Logs Explorer; then GKE Recommender for next-step suggestions.**

## 1. Identity + Autopilot failure patterns

**1. IAM / RBAC mismatch**: kubectl returns *403 Forbidden* after auth succeeds. Causes: user has no Kubernetes Engine role at cluster scope; user has KE role but no in-cluster RoleBinding (with Azure-style RBAC active); group propagation delayed; IAM Conditions excluding the request context. **Diagnose:** `gcloud auth print-identity-token` + `kubectl auth can-i` + check IAM bindings on the cluster + the user's group memberships.
    **Workload Identity Federation token issues:** Pod gets 401/403 calling GCP APIs. Causes:
    
      - K8s SA annotation has wrong G-SA email.

      - WIF Pool doesn't have a federated credential matching the cluster's OIDC issuer + SA subject.

      - G-SA missing IAM role on target resource (Storage / BigQuery / Pub/Sub).

      - Cluster recreated → new OIDC issuer URL → federated credential trust mismatch.

    
    Diagnose: gcpdiag + check WIF Pool federated credentials + check Pod's SA annotation + check G-SA IAM grants.
    **2. Autopilot admission rejection**: Pod fails to schedule with admission error. Autopilot blocks: privileged / hostNetwork / hostPath / hostIPC / hostPID / not-Compute-Class-compatible Pods. *Resource mutation surprises*: Autopilot may adjust requests upward to its minimum (e.g., request 50m CPU → mutated to 250m) — surprising for cost calculations. Fix: check Autopilot admission webhook events; either rewrite the workload to comply, OR use Autopilot workload class on Standard for that specific workload.

## 2. Compute + network failure patterns

**3. Node pool / MIG provisioning failures**: cluster create or scale-up fails with *OperationFailure: ZONE_RESOURCE_POOL_EXHAUSTED* (specific SKU temporarily unavailable in zone), *quota exceeded*, or *SKU not available*. Fix paths: switch zones; switch SKU (use `gcloud compute machine-types list`); request quota increase via Cloud Console; consider NAP for SKU flexibility (Compute Class with multiple SKU options + Spot fallback).
    **IP exhaustion** (covered in G3): VPC-native cluster's Pod secondary range exhausted. Pods stuck Pending with no IPs even on free-CPU nodes. Fix: cannot resize range in place — create new node pool with larger Pod CIDR; drain old pool. Pre-empt: `gcpdiag lint --type=cluster` warns on undersized ranges.
    **4. NEG health-check failures**: Ingress backends 100% unhealthy. Almost always: *firewall rule allowing GFE health-check ranges `35.191.0.0/16` + `130.211.0.0/22` was removed*. Diagnose: `gcloud compute firewall-rules list` + check NEG backend health in Cloud Console. Fix: restore the firewall rule.
    **Ingress provisioning**: Ingress / Gateway stays in *Pending*. Causes: missing or wrong GatewayClass; missing managed cert; missing backend Service annotation for NEG; backend service quota; project not authorised for the global LB SKU. Diagnose: `kubectl describe ingress` + `kubectl describe gateway` + Audit Logs for LB API errors.
    **Firewall blocks**: blanket-deny defaults plus an unrelated firewall change can break Pod-to-Pod or Pod-to-API traffic. Use VPC Flow Logs + Connectivity Tests to verify.
    **Cloud NAT / SNAT issues**: outbound from private cluster fails. Cloud NAT scales NAT ports per attached IP automatically — but per-VM SNAT port quota can run out under burst. Increase NAT port allocation; add Cloud NAT IPs.
    **DNS issues**: intermittent name-resolution failures. Use **Cloud DNS for GKE** (`--cluster-dns=clouddns`) + **NodeLocal DNSCache** for scale + latency. CoreDNS in default mode for compatibility. Diagnose: `kubectl exec -- nslookup` + Cloud DNS query logs.

## 3. Storage attach failures + release-channel / maintenance issues

**5. Storage attach failures**: PVC bound but Pod stuck mounting. Most common: zone mismatch (single-zone PD; Pod scheduled in different zone) — see G5 WaitForFirstConsumer. Other causes: PD already attached to a different node (split-brain after node failure), CMEK key disabled, snapshot in different region, Filestore quota.
    **6. Release-channel / maintenance-exclusion issues**:
    
      - Auto-upgrade fired during traffic peak — exclusion missing or scoped wrong (e.g., "no minor upgrades" still allowed patches).

      - Maintenance exclusion expires before team noticed — surprise upgrade after the freeze.

      - Cluster stuck on EOS version — failed pre-flight (deprecated APIs in workloads); GKE auto-upgraded anyway, breaking workloads.

      - Channel mismatch between projects — production on Stable, staging on Rapid; staging breaks features prod doesn't see for weeks.

    
    Diagnose: GKE Release Notes + `gcloud container operations list` + Pub/Sub upgrade notifications history.
    **Quota troubleshooting**: cluster CPU / memory / Persistent Disk capacity / IP / Cloud NAT / Cloud LB quotas all bite. Cloud Console → IAM & Admin → Quotas. Alert on quota approaching limit (Cloud Monitoring quota dashboards).

## 4. Diagnostic toolkit — gcpdiag, GKE Recommender, Logs Explorer, Cloud Status

**`gcpdiag`** — Google's open-source diagnostic CLI for GCP. Run `gcpdiag lint --project=PROJECT --type=cluster` against a GKE project; it executes ~100 checks (IAM, networking, quota, version policy, security baseline, common misconfigurations) and reports findings with recommended actions. *The single most useful tool for ad-hoc GKE diagnosis.*
    **GKE Recommender** — built into the GCP Recommender API. Surfaces actionable recommendations on a cluster: "upgrade to channel X," "Pod Y's requests over-provisioned by N%," "node pool Z has unused capacity." Available in Cloud Console → GKE → Recommendations. Useful for ongoing optimisation, not incident triage.
    **Logs Explorer** — Cloud Logging's query UI. Standard playbook for an incident:
    
      - Filter to the cluster + namespace + time window.

      - Look at *kube-events* and *kube-apiserver* logs first.

      - For Workload Identity Federation issues: filter to `iam.googleapis.com/Audit`.

      - For Ingress / NEG: filter to LB + Compute Engine logs.

    
    Save queries you find useful as Logs Explorer Saved Queries.
    **Cloud Status Dashboard** (status.cloud.google.com) — *always check first*: rules out GCP-side incidents instantly. "GKE in us-east1 degraded — partial connectivity issues" is the kind of message that saves hours of theorising.
    **Audit Logs + Activity** — every GCP API call against the cluster + nodes lands in *Cloud Audit Logs*. Find recent changes by humans / automation ("who deleted that firewall rule yesterday?"). Filter by principal, resource, method.
    **The standard playbook**: (1) Cloud Status (rule out GCP-side); (2) Audit Logs (recent changes); (3) gcpdiag (run a comprehensive lint); (4) Logs Explorer with saved query (per-incident-type); (5) GKE Recommender (longer-term cleanup, not triage). *Most incidents resolve in steps 1-3 if the discipline is wired.*

## Before / After

**Before.** Pre-gcpdiag, GKE troubleshooting was guess-and-grep — gcloud commands one-by-one, custom Bash scripts to verify common misconfigurations, no consolidated lint. Workload Identity errors looked like generic 401s. NEG-health-check firewall regressions surfaced only as 503s with no obvious cause. Quota issues bit during scale-out events. Cloud Status was a forum reflex, not a runbook step.

**After.** Modern GKE: **gcpdiag** as a comprehensive GCP-aware lint (~100 checks); **GKE Recommender** for ongoing optimisation; **Logs Explorer + Cloud Trace + Audit Logs** for incident root-cause; **Cloud Status Dashboard** for ruling out GCP-side. Plus the canonical playbook for the six failure patterns. *MTTR drops from hours to minutes for known patterns.*

*Triage discipline + the right diagnostic surfaces are the difference between a 15-minute incident and a 4-hour war room.*

## Analogy — the K-Garden plot

The **Plant Doctor's Hut** at K-Garden is where you go when something's wrong. The triage nurse asks the same questions every time, in the same order.
    First: *"Is anyone else in any garden reporting this?"* (Cloud Status Dashboard.) If half the gardens worldwide have the same complaint, it's the head-gardener network having a bad day, not your plot.
    Second: *"Did anything change recently?"* (Cloud Audit Logs + Activity.) Someone removed the visitor-pass for the Inspector last night — that's why the NEG plant inspection failed today.
    Third: *"Run the standard checkup."* (gcpdiag.) The standard checkup is a 100-question form — IAM grants, network ranges, quota, version policy, common misconfigurations — and lights up exactly which questions failed.
    Fourth: *"What does the building manager log say?"* (Logs Explorer with saved queries.) The garden's building manager records every door entry; saved queries scope to the right cluster + namespace + window.
    The wall has six common diagnoses: identity + Autopilot rejection + node pool / IP exhaustion + NEG / firewall / NAT / DNS + storage attach + release-channel issues — each with a one-page treatment.

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| Triage nurse first question | Cloud Status Dashboard — GCP-side incident? |
| "Did anything change recently?" | Cloud Audit Logs + Activity |
| Standard 100-question checkup | gcpdiag (lint --type=cluster) |
| Building manager journal | Logs Explorer (Cloud Logging) |
| Wall of common diagnoses | Six GCP-specific failure patterns |
| Sealed-envelope rejection | Workload Identity Federation token issue |
| Robot Caretaker refused the seedling | Autopilot admission rejection |
| Greenhouse SKU sold out | Node pool / MIG provisioning failure |
| Plant address book exhausted | Pod IP secondary range exhaustion |
| "Inspector pass removed" | GFE health-check firewall regression |
| Locker in another zone | PD attach failure (zone mismatch) |
| "Surprise pruning" | Auto-upgrade outside expected window |
| Optimisation recommendations | GKE Recommender |

⚠️ *Analogy stops here:* A clinic patient describes symptoms; GKE clusters emit machine-readable signals you must instrument first. Without diagnostic-settings + Logs Explorer saved queries, you're blind.

## ELI5 / ELI10

**ELI5.** When something hurts in the garden, you go to the doctor's hut. The doctor asks the same questions in order: is anyone else hurting? did anything change yesterday? let me run the standard checkup. The wall has six common diagnoses — yours is probably one of them.

**ELI10.** GKE troubleshooting = identify pattern + run the right diagnostic. Six GCP-specific patterns: IAM/RBAC + WIF token, Autopilot admission, node pool / MIG / IP exhaustion, NEG / firewall / NAT / DNS, storage attach, release-channel / maintenance-exclusion. Toolkit: gcpdiag (comprehensive lint), GKE Recommender (ongoing optimisation), Logs Explorer (Cloud Logging UI), Cloud Status Dashboard (GCP-side incidents), Audit Logs (recent changes). Standard playbook: Cloud Status → Audit Logs → gcpdiag → Logs Explorer → GKE Recommender.

## Real-world scenarios

- **Region-wide GKE degradation — Cloud Status saved hours.** At 14:30 the SaaS's on-call sees ImagePullBackOff across 6 clusters. First instinct: bug, our images, our pipeline. Engineer checks Cloud Status: *GCR/Artifact Registry incident in us-east1 — increased latency on image pulls.* *Confirms GCP-side; team waits 22 min for Google to mitigate; no code change needed.* Without Cloud Status: hours of debugging private images.
- **WIF 401 → cluster-recreated OIDC issuer mismatch.** A Pod that worked yesterday returns 401 from BigQuery. Federated credential and IAM grants untouched. Engineer checks: cluster was recreated overnight by IaC pipeline (Audit Logs). New cluster has new OIDC issuer URL; WIF Pool federated credential trusts old. *Update fed cred issuer; auth restored in 2 minutes.*
- **NEG health 503s root-caused by missing firewall rule (G3 recap).** An ingress backend started returning 503s. NEG marked all Pod IPs unhealthy. Root cause: Terraform refactor removed the firewall rule allowing 35.191.0.0/16 + 130.211.0.0/22 (GFE health-check IPs). Restored rule; NEG marked Pods healthy in 30 seconds. *Postmortem: pin the GFE-allow rule with a Terraform comment so future refactors don't remove it.*
- **gcpdiag flagged the issue before the incident.** Platform team ran `gcpdiag lint --type=cluster --project=prod` as part of a quarterly hygiene sweep. gcpdiag flagged: "Pod secondary range projected to exhaust at 850 nodes; cluster currently at 780." Team created a new node pool with larger Pod CIDR + drain-and-replace plan; executed during next maintenance window. *The incident never happened.*

## Common misconceptions

- **Myth:** "If kubectl works, the cluster is fine."
  **Truth:** kubectl is one signal — apiserver responds. Plenty can break around it: WIF, NEG, Cloud NAT, storage, identity, networking, IP exhaustion. Modern GKE troubleshooting goes beyond kubectl: Cloud Status, Audit Logs, gcpdiag, Logs Explorer.
- **Myth:** "`kubectl exec` is the right way to debug node-level issues."
  **Truth:** kubectl exec puts you inside a container, not on the node. Modern GKE doesn't expose node SSH on Autopilot; even on Standard, SSH is discouraged for debug. **Use `gcpdiag`** for cluster + node-level diagnosis. For per-node syscall / packet inspection, deploy a debug Pod with the right SecurityContext (Standard) — Autopilot blocks privileged debug.
- **Myth:** "Cloud Status is for GCP outages; my cluster issues won't be there."
  **Truth:** Cloud Status surfaces partial-region incidents that affect specific GKE features (e.g., "GKE control-plane upgrades degraded in us-east1"). Many "my cluster is broken" incidents start as Cloud Status entries that the team just didn't check. Always check Cloud Status first.

## Recap

Six GCP-specific patterns + diagnostic toolkit (Cloud Status → Audit Logs → gcpdiag → Logs Explorer → GKE Recommender). MTTR shrinks when triage discipline + telemetry are wired.

**Next — G10: K-GKE Capstone.** Regional Autopilot with Gateway API (multi-cluster) + Workload Identity Federation + Binary Authorization + GMP + Backup for GKE + Config Sync from Git + AI inference workload with Inference Gateway.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
