# K-AKS A9 — A9 · AKS Upgrades and Operations

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A9 · Upgrades and Operations
> Companion preview: `/preview-kubernetes-aks-lesson-09.html`.

---

**🎯 If you remember nothing else:** **Five upgrade things: K8s minor (in place, blue-green for high stakes), node image (separate cycle), add-ons (mostly automatic), surge % to limit blast, PDBs to prevent deadlock. LTS gives you 2-year stability for designated versions. Use the Release Tracker; pre-flight with kube-no-trouble.**

## 1. Version policy + LTS — what AKS supports when

AKS supports **N (latest minor) + N-1 + N-2** as community-supported versions. Once a version drops below N-2, it enters **platform support** for one more minor (N-3) — security patches only, no feature support, time-limited. After N-3, the cluster cannot be upgraded directly to a supported version; it must be force-upgraded across multiple minors or rebuilt blue-green.
    **AKS Long-Term Support (LTS)** = designated minor versions get **2-year support** on the **Premium tier**. Available for select versions (e.g. v1.27 LTS). Use LTS when you cannot upgrade quarterly — regulated industries, ISV-bundled workloads, infrastructure with long change-control cycles. *LTS is a Premium-tier feature; budget for it.*
    **The AKS Release Tracker** (releases.aks.azure.com) shows which AKS minor versions are rolled out to which Azure regions. Plan upgrades around regional availability — your East US cluster might have v1.34 ready while West Europe is still on v1.33. Check before scheduling cross-region upgrade waves.

## 2. Auto-upgrade channels + planned maintenance windows

**Auto-upgrade channels** let AKS upgrade the cluster automatically:
    
      - `none` — manual upgrades only.

      - `patch` — auto-apply patch versions within the current minor (e.g. 1.34.5 → 1.34.7).

      - `stable` — auto-apply minor upgrades, lagging the bleeding edge by one (recommended for prod).

      - `rapid` — auto-apply the latest minor as soon as it's GA (for non-prod / canary).

      - `node-image` — separate channel for node OS image upgrades (independent of K8s minor).

    
    **Planned maintenance windows** — schedule the auto-upgrade and maintenance work to specific UTC time slots, e.g. "Sunday 02:00-06:00 UTC." Three sub-types: `aksManagedAutoUpgradeSchedule` (cluster K8s upgrades), `aksManagedNodeOSUpgradeSchedule` (node OS upgrades), `default` (legacy combined window). *Always set planned maintenance for prod*; otherwise upgrades fire at random.
    **Pre-flight:** before any upgrade, run **kube-no-trouble (kubent)** against the cluster to detect deprecated API usage in YAML / Helm charts. Surfaces issues that'll bite during the upgrade.

## 3. Upgrade techniques — surge, blue-green, in place

**Control-plane upgrade** = AKS-driven, in place, ~30 minutes, no downtime. Apiserver, etcd, scheduler, controller-manager all roll. Use `az aks upgrade --control-plane-only` first; nodes follow.
    **Node pool upgrade with surge** — surge % controls how many extra nodes are added during the rolling upgrade so Pods can drain to fresh nodes before old ones cordon. Defaults to 10% per pool. *For low-PDB-tolerance workloads, increase to 33% or 50%* — more parallelism, faster upgrade, more capacity needed during the window. `az aks nodepool update --max-surge 50%`.
    **PDB-aware drains:** the upgrade respects PodDisruptionBudgets. A workload with `maxUnavailable: 0` + min replicas + no surge headroom = *upgrade deadlock* (drain can't evict any Pod). The fix is realistic PDBs that allow at least 1 disruption when you have multiple replicas.
    **Blue-green node pool migration** — high-stakes upgrade pattern. Create a new node pool on the target version next to the old; cordon the old, drain workloads (PDB-aware) onto the new, delete the old. *Atomic rollback: if the new pool misbehaves, drain back to the old and delete the new.* Use this when you can't take any drain risk during in-place upgrade.
    **Cluster blue-green** = build a whole new cluster on the target version, route traffic via DNS or front-door, decommission the old. *Last-resort pattern* for major version jumps (cross-LTS), workloads that can't survive any in-place change, or when N-3 force-upgrade isn't safe.

## 4. API deprecations, add-on upgrades, certificate rotation

**API deprecations** are the silent killer. K8s removes APIs each minor (e.g. `networking.k8s.io/v1beta1 Ingress` removed in 1.22). Workloads that still reference deprecated APIs fail post-upgrade. Tools: **kube-no-trouble (kubent)** scans live cluster + git for deprecated API usage; **Pluto** scans Helm charts. Run before every minor upgrade.
    **Add-on upgrades** — managed add-ons (Defender, Container Insights, KEDA, Flux, etc.) are upgraded by Microsoft as part of the cluster upgrade or independently. Self-installed Helm-chart add-ons are *your responsibility* — easy to forget, and an old chart can break on the new K8s minor.
    **Certificate rotation:**
    
      - **Cluster certificates** (apiserver, etcd, kubelet) — rotated automatically by AKS. `az aks rotate-certs` can force a rotation if needed (e.g. compromise).

      - **Service Account tokens** — bound (BoundServiceAccountTokens) and short-lived in modern K8s; auto-rotated.

      - **Add-on certs** (cert-manager-issued, App Routing, etc.) — automatic via the cert-manager controller; verify rotation logs after major upgrades.

    
    **Upgrade order:** (1) pre-flight (kubent), (2) backup (Velero / etcd snapshot via AKS's managed backup if available), (3) upgrade non-prod, (4) bake non-prod a week, (5) upgrade prod control plane, (6) upgrade node pools with appropriate surge, (7) verify, (8) repeat for next minor (don't skip versions in one go).

## Before / After

**Before.** Pre-managed AKS upgrades = manual, scary. Operators ran `az aks upgrade` and watched logs in fear; rollback wasn't a single command. Node pools dragged because surge default was 1; PDBs deadlocked drains; LTS didn't exist; auto-upgrade channels were minimal. API deprecations bit teams who hadn't pre-flighted. Add-ons installed by Helm broke after every minor.

**After.** Modern AKS gives you **auto-upgrade channels** (patch / stable / rapid / node-image) + **planned maintenance windows** + **tunable surge %** + **LTS** (2 years on Premium tier) + **blue-green node pool** + **kubent / Pluto** for pre-flight. Managed add-ons upgrade with the cluster. Cert rotation is automatic. *Upgrades become routine; quarterly minor cycle without a war room.*

*The era of "upgrade Saturday" with the entire team on a bridge call is over for AKS — if you wire up channels, surge, PDBs, and pre-flight correctly.*

## Analogy — the K-Campus wing

The **Maintenance Yard** is the back-of-campus depot where rolling repairs happen. Three crews work different upgrade jobs.
    The **Roof Crew** (control plane) replaces the campus roof every quarter — no class disruption, residents don't see anything change. AKS does this in 30 minutes.
    The **Wing Renovation Crew** (node pool surge upgrade) renovates one wing at a time. They build a temporary annexe (surge nodes), move residents from the old wing to the annexe (drain), demolish + rebuild the old wing, move residents back. *Surge %* is how many extra annexe rooms they can build at once — bigger annexe = faster renovation but more parking strain. *PodDisruptionBudgets* are residents' safety contracts: "never have fewer than 2 of us in this wing at once."
    The **Build-New-Wing Crew** (blue-green node pool) doesn't renovate — they build a brand-new wing next to the old one. Residents migrate; old wing gets demolished. *Atomic rollback*: if the new wing leaks, residents move back to the old.
    The **Long-Term Lease Office** (LTS) runs a separate 2-year-stable wing for residents who absolutely cannot move every quarter. Costs more (Premium tier), guarantees no forced moves for 24 months.
    And there's a **Pre-Flight Inspector** (kube-no-trouble + Pluto) who walks every wing before any renovation and flags rooms with outdated wiring (deprecated API usage) — *fix before renovation, not during*.

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| Roof crew | Control-plane upgrade (in place, no downtime) |
| Wing renovation | Node pool upgrade with surge |
| Temporary annexe | Surge nodes (max-surge %) |
| Resident safety contract | PodDisruptionBudget (PDB) |
| Build-new-wing crew | Blue-green node pool migration |
| Atomic rollback | Drain back to old pool, delete new |
| Build-new-campus crew | Cluster blue-green (whole new AKS cluster) |
| Long-Term Lease Office | AKS LTS (2-year support, Premium tier) |
| Pre-Flight Inspector | kube-no-trouble + Pluto |
| Outdated wiring | Deprecated API usage |
| Daily auto-fix-it day | Auto-upgrade channels (patch / stable / rapid) |
| Approved work hours | Planned maintenance windows |
| Annual lockset rekey | Certificate rotation |

⚠️ *Analogy stops here:* A real renovation can pause; a K8s upgrade in flight can't easily pause mid-pool. The metaphor underplays the irreversibility of some upgrade steps (e.g., once etcd schema migrates).

## ELI5 / ELI10

**ELI5.** The maintenance crew has different jobs. One fixes the roof while everyone keeps working. Another renovates one wing at a time, putting up a temporary tent so people don't crowd. Sometimes they build a whole new wing instead. There's an inspector who walks the building first to find old wiring before they break the wall open.

**ELI10.** AKS upgrades = control plane (in place, ~30 min, no downtime) + node pool (surge % to control parallel, PDB-aware drain) + add-ons (managed = automatic; self-installed = your job). For high-stakes: blue-green node pool (atomic rollback). LTS gives 2-year stability on Premium tier for designated versions. Pre-flight with kube-no-trouble. Schedule with planned maintenance windows + auto-upgrade channels. API deprecations bite if you skip pre-flight; certificate rotation is automatic.

## Real-world scenarios

- **SaaS — quarterly minor cadence with stable channel + 33% surge.** A SaaS runs 30 AKS clusters on the `stable` auto-upgrade channel; planned maintenance Sundays 02:00-06:00 UTC; node-pool max-surge = 33%. Upgrades fire automatically; on-call gets a notification but doesn't need to be at keyboard. PDBs across all services tested for 33% surge tolerance. *Quarterly minor jumps without a war room.*
- **Bank — LTS on Premium tier for the regulated cluster.** A bank's payments cluster has 9-month change-control cycles. They cannot upgrade quarterly. Solution: AKS Premium tier + LTS on v1.27. Two years of supported updates without minor jumps. *$0.60/cluster-hour Premium tier vs $0.10 Standard — math works out for the regulated workload.*
- **Health-care — blue-green node pool for the SAP HANA workload.** A SAP HANA workload has zero PDB tolerance for unplanned drain. Upgrade strategy: build a new node pool on the target K8s + node OS version next to the existing pool; verify hardware (Ultra Disk attachment, ANF mounts); fence DB application traffic; drain with 60-min grace; delete old pool. *Atomic rollback ready until cutover commit.*
- **Pre-flight saved an outage — kubent caught Ingress v1beta1.** A team ran kubent before a 1.21 → 1.22 upgrade. Result: 14 Ingress objects still on `networking.k8s.io/v1beta1` (removed in 1.22). All in legacy Helm charts. Team migrated charts to `networking.k8s.io/v1` first; upgrade then went clean. *Without kubent, those 14 ingresses would have orphaned post-upgrade — silent partial outage.*

## Common misconceptions

- **Myth:** "AKS upgrades are zero-downtime by default."
  **Truth:** **Control-plane** upgrades are zero-downtime. **Node pool** upgrades cause Pod restarts during drain. With sane PDBs + surge + multiple replicas, the workload remains available — but individual Pods restart. Single-replica workloads with no PDB are exposed.
- **Myth:** "I can skip multiple minor versions in one upgrade."
  **Truth:** AKS supports **one minor at a time**. Going from 1.30 to 1.34 = four upgrades, not one. Each has its own pre-flight + window + add-on compatibility check. Trying to leap = AKS will refuse or, if you forced it, you're running an unsupported configuration.
- **Myth:** "LTS means I never have to upgrade."
  **Truth:** LTS = 2-year support for a designated version. After 2 years, the LTS version exits support and you must move to the next LTS or current N-2. *You're still upgrading; you're just doing it every 2 years instead of every quarter.* The trade-off is fewer upgrades, more change to absorb at each one.

## Recap

Five upgrade things mapped: K8s minor + node image + add-ons + surge + PDBs. LTS for stability; pre-flight with kubent; channels + windows for routine; blue-green for high-stakes.

**Next — A10: AKS Troubleshooting (Azure-specific).** Entra/kubelogin failures, Azure RBAC mismatch, VMSS quota issues, Azure CNI IP exhaustion, CoreDNS, SNAT, LB pending, private DNS, disk attach failures, Key Vault CSI failures, ACR pull failures, MI failures, upgrade blocked, kubectl-aks, AKS Diagnostic Settings, Resource Health.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
