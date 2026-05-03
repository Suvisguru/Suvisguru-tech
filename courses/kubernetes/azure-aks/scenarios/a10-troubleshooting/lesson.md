# K-AKS A10 — A10 · AKS Troubleshooting (Azure-Specific)

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A10 · AKS Troubleshooting
> Companion preview: `/preview-kubernetes-aks-lesson-10.html`.

---

**🎯 If you remember nothing else:** **Eight Azure-specific patterns: Entra/RBAC, VMSS/quota, CNI IPs/CoreDNS, SNAT/LB, disk/KV CSI, ACR/MI, upgrade blocked, node-image. Always check Azure Resource Health first; then kubectl-aks; then KQL on AKS Diagnostic Settings logs.**

## 1. Identity + compute failure patterns

**1. Entra / kubelogin failure**: *"failed to refresh token"*, *"AADSTS50158"*, etc. Causes: stale browser session, Conditional Access blocking from current network, tenant trust missing, kubelogin version too old. Fixes: `kubelogin clean-cache`, re-run `az login`, check Conditional Access in Entra portal, upgrade kubelogin via az CLI.
    **2. Azure RBAC vs K8s RBAC mismatch**: kubectl returns `403 Forbidden` after auth succeeds. Possible causes: user has neither Azure RBAC role (e.g. *Azure Kubernetes Service RBAC Reader*) nor in-cluster RoleBinding; cluster has Azure RBAC for K8s enabled but user only has K8s RBAC binding (or vice versa); group membership took time to propagate. Fix: assign the right Azure role at cluster scope OR add a RoleBinding referencing the user's Entra OID.
    **3. VMSS / quota / SKU not available**: cluster create / scale-out fails with *"OperationNotAllowed: quota exceeded"* or *"SkuNotAvailable"*. Fix paths: request quota increase via Azure portal (Subscriptions → Usage + quotas — can take hours); switch SKU to one available in the region (use `az vm list-skus --location ... --output table`); switch zones; consider NAP for SKU flexibility.

## 2. Network failure patterns

**4. Azure CNI IP exhaustion / CoreDNS autoscaling**: Pods stuck Pending with *"InsufficientFreeAddressesInSubnet"*, or DNS lookups intermittently fail. Causes: traditional Azure CNI burning IPs (migrate to Overlay); CoreDNS replicas insufficient (default = 2). Fixes: migrate to Azure CNI Overlay; tune CoreDNS HPA (autoscaler add-on or manual replica bump); shard DNS via NodeLocal DNSCache.
    **5. SNAT exhaustion / LB pending**: outbound calls fail with *"SNAT port allocation"*; or `Service: type=LoadBalancer` stays in `Pending`. Fixes: deploy NAT Gateway (covered in A3); investigate LB pending via `kubectl describe service` — often points to outbound IP quota, AGC reconcile delay, or NSG blocking AKS load-balancer health probes.
    **Private DNS issues**: private cluster + custom DNS resolver setup; cluster apiserver FQDN doesn't resolve from worker network. Verify Private DNS zone link to the worker VNet; check custom DNS forwarder if hub-spoke topology.

## 3. Storage + identity failure patterns

**6. Disk attach failure**: PVC bound to a Premium SSD in `eastus-1`; Pod scheduled in `eastus-2`; attach fails with *"AttachVolume.Attach failed"*. Cause: missing `WaitForFirstConsumer`. Fix: see A4 — use the default StorageClass or migrate to ZRS.
    **Key Vault CSI failure**: *"failed to get secret from Key Vault"*. Causes: Workload Identity federated credential mismatch (cluster recreated → OIDC issuer changed); Key Vault access policy missing the MI; Key Vault firewall blocking the cluster's VNet; Secret Rotation poller misconfigured. Diagnose: check the Secrets Store CSI driver logs; verify federated credential and Key Vault access policy; check NSG / Key Vault firewall.
    **7. ACR pull failure**: *"ImagePullBackOff: 401 Unauthorized"*. Causes: cluster not attached to the registry (`az aks update --attach-acr` not run); kubelet identity missing AcrPull role; registry private endpoint not in cluster's VNet; image actually doesn't exist at that tag. Diagnose: `kubectl describe pod` for the exact ImagePullBackOff message; verify with `az aks check-acr`.
    **Managed identity failures**: Pod uses Workload Identity → Storage call returns 403. Cause: MI not assigned the right Azure role on the resource; or MI scope is wrong (resource-group vs subscription); or the federated credential subject is wrong. Diagnose: check the Pod's SA annotation, federated credential, and MI role assignment.

## 4. Upgrade blocked, node-image failure, and the diagnostic toolkit

**8. Upgrade blocked**: *"upgrade failed: PodDisruptionBudget violation"* or add-on compatibility check failed. Fixes: tune PDB / surge (covered in A9); upgrade or remove the offending self-installed add-on; check `Activity Log` for the precise error message.
    **Node-image failure**: pool stuck after node-image upgrade. Possible: workload uses an unsupported kernel feature on the new image; AL2 → AL3 migration left a stale image SKU; underlying VMSS scale operation failed. Investigate: `kubectl describe nodes`, AKS Diagnostic Settings `cluster-autoscaler` log, Activity Log on the VMSS.
    **Diagnostic toolkit:**
    
      - **`kubectl-aks`** — Azure CLI extension that exposes AKS-specific diagnostics: live node BPF inspection, syscall traces, network captures, ifconfig — *without SSH-ing the node*.

      - **AKS Diagnostic Settings → Log Analytics** — apiserver / audit / scheduler / cluster-autoscaler logs queryable via KQL.

      - **Azure Resource Health** — *always check first* — surfaces Azure-side incidents affecting the cluster (e.g., regional storage degradation, Entra outage). Eliminates many "is it me or is it Azure?" theorising.

      - **Azure Activity Log** — every Azure API call against the cluster + node resource group. Find who deleted the Public IP that broke ingress.

      - **Defender for Containers alerts** — security incidents.

      - **Container Insights workbooks** — pre-built node / Pod / container health views.

    
    **The standard playbook**: (1) Resource Health → ruling out Azure-side; (2) Activity Log → recent changes by humans / automation; (3) AKS Diagnostic Settings logs → control-plane perspective; (4) `kubectl describe` + `kubectl-aks` → workload + node perspective; (5) Defender alerts → security angle. *Most outages resolve in steps 1-3 if the toolkit is wired in.*

## Before / After

**Before.** Pre-AKS-Diagnostic-Settings era: troubleshooting AKS meant *guessing*. Apiserver logs invisible. No `kubectl-aks` — node-level inspection meant SSH (which AKS doesn't allow) or disruptive debug-Pod schemes. Resource Health was buried; engineers theorised "is it me or is it Azure?" for hours. ACR pull failures had three possible causes and no clear surface. Workload Identity errors were opaque — federated credential trust mismatches looked like generic 401s.

**After.** Modern AKS exposes the diagnostic surface: **`kubectl-aks`** for node-level inspection without SSH; **AKS Diagnostic Settings** route apiserver / audit / scheduler / autoscaler logs to Log Analytics for KQL search; **Azure Resource Health** is a one-click ruling-out for Azure-side trouble; **Activity Log** shows every Azure-API change; **Defender alerts** surface security incidents. Plus the canonical playbooks for the eight failure patterns are documented. *MTTR drops from hours to minutes for known patterns.*

*Triage discipline + the right diagnostic surfaces are the difference between a 15-minute incident and a 4-hour war room.*

## Analogy — the K-Campus wing

The **Health Clinic** on K-Campus is where you go when something's wrong. The triage nurse asks the same questions every time, in the same order.
    First question: *"Is anyone else on campus reporting this?"* (Azure Resource Health.) If half the campus has the same complaint, it's probably the campus power grid (Azure-side incident), not your symptom. Wait + page the campus utility.
    Second question: *"Did anything change recently?"* (Activity Log.) Someone deleted the campus shuttle stop in front of your building yesterday — that's why your students can't get to class.
    Third question: *"What does the building manager log say?"* (AKS Diagnostic Settings → Log Analytics → KQL.) The manager's journal records every door entry; the syscall-level inspection (`kubectl-aks`) walks each room.
    The Clinic has eight common diagnoses pinned on the wall (the eight Azure-specific failure patterns). Each diagnosis has a one-page treatment protocol: the cause, the test that confirms, the fix.

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| Triage nurse first question | Azure Resource Health — Azure-side incident? |
| "Did anything change recently?" | Azure Activity Log — recent Azure-API changes |
| Building manager journal | AKS Diagnostic Settings → Log Analytics + KQL |
| Walk into rooms without breaking down doors | `kubectl-aks` — node-level inspection without SSH |
| Wall of common diagnoses | Eight Azure-specific failure patterns |
| "Wrong wing badge" | Azure RBAC vs K8s RBAC mismatch |
| "Sold-out shoe size" | VMSS quota / SKU unavailability |
| "Building street is closed" | SNAT exhaustion / LB pending |
| "Locker is in another zone" | Disk attach failure (cross-AZ) |
| "Vault key wouldn't turn" | Key Vault CSI failure |
| "Mailroom rejected the package" | ACR pull failure |
| Security ward alerts | Defender for Containers alerts |

⚠️ *Analogy stops here:* A clinic patient describes symptoms; AKS clusters emit machine-readable signals you must instrument first. The metaphor underplays observability prerequisites — without diagnostic settings + Container Insights, you're blind.

## ELI5 / ELI10

**ELI5.** When something hurts, you go to the clinic. The nurse asks the same questions every time: is everyone else hurting? did anything change yesterday? what does your watch say? Then she looks at the wall — your problem is probably one of eight common ones, and each has a one-page treatment.

**ELI10.** AKS troubleshooting = identify pattern + run the right diagnostic. Eight Azure-specific patterns: Entra/kubelogin auth, Azure-vs-K8s RBAC mismatch, VMSS / quota / SKU, CNI IP exhaustion + CoreDNS, SNAT + LB pending + private DNS, disk attach + Key Vault CSI, ACR pull + MI permission, upgrade blocked + node-image. Toolkit: `kubectl-aks` (node inspection without SSH), AKS Diagnostic Settings + KQL (apiserver / audit / scheduler / autoscaler logs), Azure Resource Health (rule out Azure-side first), Activity Log (recent changes), Defender alerts. Standard playbook: Resource Health → Activity Log → Diagnostic Settings KQL → kubectl describe + kubectl-aks → Defender.

## Real-world scenarios

- **Region-wide ACR throttling — Resource Health saved hours.** At 14:30 the SaaS's on-call sees ImagePullBackOff across 12 clusters. First instinct: bug, our images, our pipeline. Engineer checks Azure Resource Health: *ACR throttling event in eastus2*. *Confirms Azure-side; the team waits 18 minutes for Microsoft to mitigate; no code change needed.* Without Resource Health: 4 hours of debugging private images.
- **Workload Identity 401 → cluster-recreated OIDC issuer mismatch.** A Pod that worked yesterday returns 401 from Key Vault. Federated credential and access policy untouched. Engineer checks: cluster was recreated overnight (Activity Log). New cluster has new OIDC issuer URL; federated credential still trusts the old one. *Update fed cred subject; auth restored in 2 minutes.*
- **Bursty SaaS — SNAT exhaustion at peak hour.** Black Friday peak; outbound to Stripe API fails with *SNAT port allocation*. Cluster had default LB-shared SNAT. Emergency: provision NAT Gateway via UDR (since outbound type is immutable); fail over egress through it within 25 minutes. Postmortem: NAT Gateway part of cluster creation from now on.
- **kubectl-aks node inspection diagnoses kernel issue.** A node throws random Pod restarts; `kubectl describe` blames "runtime error." Engineer runs `kubectl-aks node-inspect-tcpdump` — captures network traffic; finds an unusual SYN flood from a misconfigured client. *No SSH, no debug Pod, root cause in 8 minutes.*

## Common misconceptions

- **Myth:** "If kubectl works, the cluster is fine."
  **Truth:** kubectl is one signal — apiserver responds. Plenty can break around it: ACR pull, Key Vault CSI, SNAT, identity, networking. Modern AKS troubleshooting goes beyond kubectl: Resource Health, Activity Log, Diagnostic Settings + KQL, kubectl-aks for node-level signals.
- **Myth:** "`kubectl exec` into a Pod is the right node-debugging tool."
  **Truth:** kubectl exec puts you inside a container, not on the node. AKS doesn't allow node SSH. Use **`kubectl-aks`** for node-level inspection — runs as a privileged Pod on the target node, exposes BPF inspection, ifconfig, syscall traces, packet captures. Built for AKS specifically; designed for triage.
- **Myth:** "Diagnostic Settings logs are nice-to-have."
  **Truth:** They're *foundational*. Without apiserver + audit logs in Log Analytics you can't answer "who did X?", "when did Y stop working?", "what changed?" — the most common questions in any incident. Wire diagnostic settings on every cluster from creation, not after the first outage.

## Recap

Eight Azure-specific patterns + the diagnostic toolkit (Resource Health → Activity Log → Diagnostic Settings KQL → kubectl describe + kubectl-aks → Defender). MTTR shrinks when triage discipline + telemetry are wired.

**Next — A11: Capstone.** Build a private AKS Automatic with Cilium dataplane + Workload Identity + AGC (Gateway API) + Defender for Containers + Managed Prometheus/Grafana + Flux v2 GitOps + LTS upgrade & DR runbooks.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
