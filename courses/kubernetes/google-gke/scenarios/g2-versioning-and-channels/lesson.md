# K-GKE G2 — G2 · GKE Versioning and Release Channels

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G2 · Versioning and Release Channels
> Companion preview: `/preview-kubernetes-gke-lesson-02.html`.

---

**🎯 If you remember nothing else:** **Pick a channel (Regular = default for prod; Stable for risk-averse; Extended for 2-year LTS; Rapid for canary). Set maintenance windows for routine upgrades; set maintenance exclusions during peaks / freezes. Don't opt out of channels.**

## 1. Four release channels — Rapid, Regular, Stable, Extended

A **release channel** is GKE's commitment to which K8s minors a cluster receives, when, and for how long. Pick at cluster create; can be changed (forward-only is the safe path; rapid → regular is fine, regular → rapid moves you onto bleeding-edge faster).
    
      - **Rapid** — newest GKE minors land here first (often within weeks of upstream K8s release). Useful for canary clusters, preview-feature testing, internal platform-team validation. *No SLA on the latest minor; supported once it stabilizes.*

      - **Regular** — balanced cadence. Most production clusters. Minors arrive after they've baked in Rapid for some weeks. Auto-upgrades flow predictably.

      - **Stable** — conservative cadence. Minors arrive after Rapid + Regular have validated them. For risk-averse production: regulated workloads where any change has a long approval cycle.

      - **Extended** — long-term support window for designated minor versions (~2 years per minor). For workloads that cannot upgrade quarterly. *Premium tier; specific version line.*

    
    **No-channel clusters** = clusters not enrolled in any channel. Loses auto-upgrades for minors; you upgrade manually. *Strongly discouraged for production* — you become responsible for tracking GKE EOS dates and force-migrating off unsupported versions.

## 2. Auto-upgrades + maintenance windows

Channel clusters get **auto-upgrades** by default — Google upgrades the control plane and (separately) node pools as part of the channel cadence.
    
      - **Maintenance windows** — one or more weekly time windows when GKE may perform upgrades and node-pool maintenance. Set per cluster. *Pick low-traffic hours;* an empty window means GKE picks any time.

      - **Maintenance exclusions** — explicitly block all upgrades during specific date ranges. Three exclusion scopes: *no upgrades* (suppresses minor + patch + node), *no minor upgrades* (still applies patches + security), *no minor or node upgrades*. Use during freezes (Black Friday, end-of-quarter, regulated change-control windows). Maximum exclusion length depends on scope (~30-180 days).

      - **Surge upgrade** on node pools — extra nodes added during the rolling upgrade so workloads drain to fresh nodes before old ones cordon. Tunable per pool. PDBs respected.

      - **Blue-green node pool upgrade strategy** — instead of in-place rolling, GKE creates a parallel new pool, drains workloads to it, then deletes the old. Atomic rollback before the old is deleted.

    
    **Key rule:** *set the window AND the exclusions*. Window without exclusions = upgrades during your peak. Exclusion without window = ad-hoc upgrades when the exclusion expires.

## 3. Version availability, EOS, SLA, upgrade notifications

**Version availability per channel** evolves continuously. Use the **GKE Release Notes** + **`gcloud container get-server-config`** to see which minors + patches are currently available in each channel for your region.
    **End-of-support (EOS):** each minor has a documented EOS date per channel. After EOS, the cluster is auto-upgraded by GKE to the next supported minor (you're not stranded; you may be force-upgraded sooner than you wanted). Channels publish their version-skew + EOS commitment so you can plan.
    **SLA:** regional clusters have a 99.95% SLA on the control plane (Standard tier) when on a supported channel + version. Zonal clusters have no SLA (best-effort). Out-of-channel or EOS-version clusters lose SLA.
    **Upgrade notifications:** enable Pub/Sub upgrade notifications — GKE publishes a message before maintenance fires. Subscribe with Cloud Functions / Workflows / Slack webhook to get a heads-up before each upgrade. *Operators love this*: "upgrading prod-eu in 6 hours to v1.32.5" lands in #ops-channel.
    **Pre-flight** (before any minor upgrade): scan workloads for deprecated APIs (`gcpdiag`, `kube-no-trouble`, `Pluto`); validate Helm charts; review GKE Release Notes for breaking changes in the target minor.

## 4. Upgrade sequencing + safety patterns

**Sequencing inside an auto-upgrade:** control plane first, then node pools. Control plane upgrade is in place, ~minutes, no workload disruption. Node-pool upgrades roll one node at a time (with surge headroom and PDB-aware drain).
    **Manual override** via `gcloud container clusters upgrade` — useful for accelerating a CVE patch or rolling back a node-pool change. *Manual control plane upgrades only move forward*; Google does not support rolling back the control plane to a prior minor.
    **Patch versions** within a minor: GKE auto-applies these per channel cadence. They include security fixes + bug fixes; usually safe. Maintenance windows + exclusions still apply.
    **If something breaks during auto-upgrade**: GKE automatically pauses if control-plane health checks fail; node-pool upgrades roll back the affected pool if upgrades fail health-checks. Combined with PDB-aware drain, the typical worst case is "some Pods restart, the cluster ends up healthy." The atypical worst case (custom DaemonSet incompatible with new node image, etc.) is your responsibility — pre-flight + maintenance exclusions + canary on Rapid avoid most surprises.

## Before / After

**Before.** Pre-channel GKE meant operators picked a specific patch version at create and never moved. Versions went EOS silently; security patches required manual upgrade dance. Maintenance "windows" were a forum convention. No SLA differentiation by version. Auto-upgrades were either off (you forget) or on (surprises). The kube-no-trouble pre-flight discipline was bring-your-own. Operators tracked CVEs via mailing lists.

**After.** Modern GKE has **release channels** (Rapid / Regular / Stable / Extended) that codify the upgrade cadence + supported version window. Auto-upgrades flow within maintenance windows; exclusions block during peaks. Pub/Sub upgrade notifications give heads-up. SLA on supported channel + version. Documented EOS per minor per channel. *Upgrade discipline is built into the platform; you opt into a cadence and the platform delivers.*

*Pick the channel that matches your risk appetite and your change-control cadence. Add windows + exclusions. Don't opt out.*

## Analogy — the K-Garden plot

The **Almanac Hut** is the small wooden building at the back of the Visitors' Pavilion. The Head Gardener (Google) keeps a calendar there showing when each new variety of seed becomes available, when the old varieties stop being supported, and when the planting and pruning happen.
    Visitors pick one of four planting calendars at sign-up:
    
      - **Rapid Almanac** — gets the brand-new variety right when the Gardener releases it. Bleeding edge. Useful for early-tester plots; not promised the variety will perform predictably.

      - **Regular Almanac** — gets the variety after a few weeks of testing in Rapid. The Gardener offers a yield guarantee (SLA). Most plots use this.

      - **Stable Almanac** — slow and conservative. Variety has been baked in Rapid + Regular before it lands here. For plots whose owners hate surprises.

      - **Extended Almanac** — picks one designated variety and supports it for two years. For plots whose owners cannot replant every quarter.

    
    Inside each calendar there are two important annotations: the weekly *Garden Maintenance Window* (when the Gardener will prune and replant, e.g. "Tuesdays 2-6 AM") and any *Maintenance Exclusions* the visitor has requested ("please don't prune anything between Nov 25 and Dec 5 — that's our harvest week"). The Gardener also sends a *Pub/Sub postcard* a few hours before any pruning so the visitor isn't surprised.

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| The Almanac Hut | GKE versioning + release-channel surface |
| Rapid Almanac | Rapid release channel |
| Regular Almanac | Regular release channel (default) |
| Stable Almanac | Stable release channel |
| Extended Almanac | Extended release channel (~2 yr LTS) |
| No almanac at all | No-channel cluster (manual upgrades; no auto-upgrades) |
| Garden Maintenance Window | Maintenance window (weekly time slot) |
| Maintenance Exclusion | Maintenance exclusion (block upgrades for date range) |
| Pub/Sub postcard | Upgrade notifications via Pub/Sub |
| "Variety performance guarantee" | SLA — 99.95% on supported channel + version |
| Replant the whole bed at once | Blue-green node pool upgrade |
| Roll the new variety bed by bed | Surge upgrade with PDB-aware drain |
| Variety pulled from the catalog | EOS — auto-upgrade to next supported minor |

⚠️ *Analogy stops here:* A real almanac is paper; channels are dynamic — versions stop being available without warning if you let your cluster drift past EOS without an exclusion. The Gardener auto-replants you onto a supported variety; you don't get to stay on yesterday's seed.

## ELI5 / ELI10

**ELI5.** Google has a calendar for when new seed varieties come out and when old ones stop being supported. You pick one of four calendars: brand-new, steady, slow-and-careful, or super-long-term. You also tell Google when not to come prune (your harvest week). Google sends you a postcard before they prune.

**ELI10.** GKE release channels = Rapid (bleeding edge, no SLA on latest minor) → Regular (default, balanced, SLA) → Stable (conservative) → Extended (~2-year LTS for designated minors, premium tier). Channel determines auto-upgrade cadence + supported version window + EOS dates. Maintenance windows schedule routine upgrades; maintenance exclusions block them during freezes. Pub/Sub upgrade notifications give heads-up. Pre-flight with gcpdiag / kubent / Pluto before minor upgrades. Don't run no-channel clusters in prod.

## Real-world scenarios

- **SaaS — Regular channel + Tuesday 02-06 UTC + Nov-exclusion for Black Friday.** A SaaS prod cluster: Regular channel, maintenance window Tuesdays 02-06 UTC, exclusion *no minor upgrades* Nov 20 - Dec 1 (security patches still apply). Pub/Sub upgrade notifications fire to a Slack channel. *Quarterly minor cycles run themselves; team intervenes only for the rare incompatibility.*
- **Regulated bank — Stable channel + 6-week exclusions for change-control.** A bank's payment cluster: Stable channel for slow predictable cadence, plus 6-week exclusion windows aligned with their change-control cycle. Pre-flight with gcpdiag before each upgrade window opens; CAB review mandatory. *~3 minor upgrades per year; predictable; auditable.*
- **Hyperscale ISV — Extended channel for the regulated workload, Rapid for the inference platform.** An ISV runs two GKE clusters per region. *Compliance cluster*: Extended channel, locked to a designated minor for 2 years. *Inference platform cluster*: Rapid channel — they want the latest GPU device-plugin features and TPU support as soon as Google ships them. Two channels, one team; the platform engineer documents the trade-off.
- **Bug averted by Pub/Sub upgrade notification.** A team's Pub/Sub upgrade notification fired with target version v1.30.6. A platform engineer on-call read the GKE Release Notes for that version and saw a known issue with their CSI driver version. They added a *2-week maintenance exclusion*; bumped the CSI driver in the meantime. *Auto-upgrade fired safely 3 weeks later.*

## Common misconceptions

- **Myth:** "Stable channel never auto-upgrades."
  **Truth:** Stable still auto-upgrades — just on a slower cadence. Minors arrive in Stable after they've baked in Rapid + Regular; patches still flow continuously. Stable is "conservative", not "manual." If you genuinely need no auto-upgrades, that's either Extended (still upgrades within the 2-year LTS minor) or no-channel (discouraged).
- **Myth:** "Maintenance window suppresses upgrades that haven't fired yet."
  **Truth:** Maintenance window *schedules when* upgrades may fire (the time-of-week slot). It does not stop GKE from queuing an upgrade. To suppress queued upgrades, use **maintenance exclusions** with appropriate scope. Window + exclusion together = controlled upgrade flow.
- **Myth:** "I can downgrade the control plane if an upgrade misbehaves."
  **Truth:** GKE control plane upgrades are *forward-only*. There is no supported rollback. If a control-plane upgrade introduces a problem, the path forward is: report the issue, wait for Google's patch, apply the patch (which moves you to a new patch version, not back to the old). Plan upgrades + exclusions to avoid this; the auto-pause on health-check failure prevents most disasters.

## Recap

Four channels mapped to upgrade-cadence × stability trade-offs; window + exclusion are the routine + freeze controls; Pub/Sub gives heads-up; pre-flight with gcpdiag / kubent.

**Next — G3: GKE Networking.** VPC-native (alias IPs), pod/service secondary ranges, IP exhaustion mitigation, GKE Dataplane V2 (Cilium-based eBPF), GKE Ingress + Gateway controller, NEG + container-native LB, Multi-Cluster Ingress / Multi-Cluster Services, Cloud Service Mesh, Network Connectivity Center, Shared VPC, firewall, DNS troubleshooting.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
