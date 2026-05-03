# K-GKE G1 — G1 · GKE Architecture and Modes (Standard, Autopilot, Enterprise)

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G1 · GKE Architecture and Modes
> Companion preview: `/preview-kubernetes-gke-lesson-01.html`.

---

**🎯 If you remember nothing else:** **Three modes (Standard / Autopilot / Enterprise) × two control-plane scopes (regional / zonal). Regional control plane + Autopilot is the safe default; pick Standard for full knobs; layer Enterprise for fleets + multi-cloud governance.**

## 1. Three modes — Standard, Autopilot, Enterprise

**GKE Standard**: you create the cluster, you create node pools (System / User / GPU / Spot), you choose VM SKUs, you wire add-ons. Most flexibility. Highest ops surface. *Pick when you need precise control over node shape, custom DaemonSets, niche kernel features, or non-standard CNI.*
    **GKE Autopilot**: *Google manages all node operations*. You declare workloads with resource requests; Google provisions, scales, secures, upgrades, and bills **per Pod** (not per node). Built-in node-level security baseline (no privileged Pods unless you opt in; no SSH; managed registries; admission webhooks for safety). *Pod-level SLA* (vs Standard's control-plane SLA). Pick when you want minimal ops surface and your workloads fit Autopilot's admission constraints. **Autopilot workloads can also run inside Standard clusters** via the Autopilot workload class — gives you per-workload Pod-level billing without committing the whole cluster.
    **GKE Enterprise** (formerly Anthos) is a *tier on top of* Standard or Autopilot, not a third cluster shape. Adds *fleet management across GCP / AWS / Azure / on-prem*, *Config Sync* (GitOps), *Policy Controller* (managed Gatekeeper), *Cloud Service Mesh* (managed Istio), *Connect Gateway* (kubectl across registered clusters), *multi-cluster Ingress / Gateway*. Pick when you have ≥10 GKE clusters or hybrid / multi-cloud K8s under one governance plane.

## 2. Regional vs zonal control plane; multi-zonal node pools

**Zonal cluster**: control plane (apiserver + etcd) lives in *one zone*. Cheaper. **Single zone outage = control plane down.** Workloads keep running but you can't deploy or modify until the zone recovers. *Avoid for production.*
    **Regional cluster**: control plane runs in **three zones** within the region (apiserver replicated, etcd quorum across zones). Survives a single-zone outage. Recommended default for prod. *Roughly 3× the control-plane cost; trivial vs the cost of a workday-long unable-to-deploy outage.*
    **Multi-zonal node pools**: per node pool, you specify `--node-locations zone-a,zone-b,zone-c`. Pool autoscaler spreads nodes across zones. Workloads with topology-spread constraints stay balanced. Combine with regional control plane for true multi-zone resilience.
    **Quick rule:** *regional control plane + multi-zonal node pools* = the safe default. Pick zonal only for ephemeral / dev clusters where the cost saving matters and the outage risk is acceptable.

## 3. Private clusters + master authorized networks

By default GKE's apiserver has a public endpoint. Three increasingly-locked-down options:
    
      - **Master authorized networks** — public endpoint stays; firewall allows only specific CIDRs (your office VPN, your CI runners). Cheapest hardening.

      - **Private cluster, public endpoint** — nodes have only private IPs (egress via Cloud NAT); apiserver still has a public endpoint with authorized networks restricting access. Common production shape.

      - **Fully private cluster** — nodes private; apiserver private (Private Service Connect). Access via Cloud Interconnect / Cloud VPN / Connect Gateway. Most secure; requires private DNS + service connectivity design.

    
    **Cluster identity**: GKE clusters use a *service account* that the nodes run as. Defaults to the Compute Engine default SA (over-broad; rotate to a least-privilege SA per cluster). Workloads use **Workload Identity Federation for GKE** (covered in G4) — Pods authenticate to GCP services without baked secrets.

## 4. Four provisioning paths — gcloud, Terraform, Config Connector, Pulumi

Pick one tool and stick with it across the cluster lifecycle. Mixing tools = drift. Four common paths:
    
      - **gcloud CLI** (`gcloud container clusters create`) — interactive scripting, ad-hoc clusters, runbooks. The Cloud Console generates equivalent gcloud commands you can copy.

      - **Terraform Google provider** — most popular cross-platform IaC. Mature modules, strong community. State management is your responsibility (use GCS bucket backend with state locking).

      - **Config Connector** — GCP-native operator that manages GCP resources as Kubernetes Custom Resources. Reconciled by a control-plane GKE cluster. Useful when GitOps is the source of truth and Argo CD / Flux already runs your platform — GCP resources slot into the same workflow.

      - **Pulumi** — IaC in real programming languages (TypeScript, Python, Go). Same GCP resources as Terraform; expressive for complex composition logic.

    
    **Production rule:** GKE clusters live in Git via Terraform / Config Connector / Pulumi. Cloud Console + gcloud for exploration only.

## Before / After

**Before.** Pre-Autopilot, every GKE cluster was Standard — operators sized node pools, picked machine types, managed Cluster Autoscaler tuning, installed every add-on. New developers needed a week to understand the cluster shape. Autoscaling pools to zero was awkward. Cost surprises were common — over-provisioned pools idle most of the day. Multi-cloud K8s governance was bring-your-own; security baseline was bring-your-own.

**After.** Modern GKE has three intent shapes: **Standard** for full control, **Autopilot** for opinionated managed defaults with per-Pod billing and a Pod-level SLA, **Enterprise** as an add-on tier for fleets + multi-cloud governance + GitOps + service mesh. Regional control planes survive zone outages by default. Workload Identity Federation removes the keys-in-cluster problem. Provisioning is declarative via Terraform / Config Connector / Pulumi. *The day-1-cluster-to-day-N-cluster journey is shorter.*

*Pick the mode that matches your operational appetite. Autopilot for "I want managed defaults"; Standard for "I need every knob"; Enterprise on top when fleets + multi-cloud demand uniform governance.*

## Analogy — the K-Garden plot

K-Garden is the Google-managed botanical garden / orchard. The **Visitors' Pavilion** is where every visitor enters: at the door, the Head Gardener (Google) hands you a map and a choice — which kind of plot are you here to plant?
    The map shows three plot styles. **Standard plots**: you choose your own soil mix, your own irrigation schedule, your own seedlings. The Head Gardener supplies the climate-controlled greenhouse but you do the rest. **Autopilot plots**: you arrive with seedlings; the Garden's robot caretakers (Google) plant, water, prune, and harvest on a smart schedule; you pay per seedling-day, not per plot. **Enterprise membership**: a top-tier subscription that lets your gardening collective coordinate plots across *multiple gardens* in different climates (multi-cloud) — same care manuals, same security guards, same seasonal schedule, everywhere.
    The Pavilion also has a wall map showing two layout choices. *Single-greenhouse layout*: cheaper, but if that greenhouse loses heat overnight your plot is unrecoverable. *Three-greenhouse layout*: your plants live in three glass houses simultaneously; if one loses heat, the others keep going. **Pick the three-greenhouse layout for anything that has to survive bad weather.**

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| Visitors' Pavilion | GKE entry — pick mode + cluster shape |
| Head Gardener | Google's GKE management plane |
| Standard plot | GKE Standard — you manage node pools, scaling, ops |
| Autopilot plot | GKE Autopilot — managed nodes, per-Pod billing, Pod-level SLA |
| Robot caretakers | Autopilot's preconfigured platform (security baseline + auto-scaling + admission webhooks) |
| Enterprise membership | GKE Enterprise (formerly Anthos) — fleets + multi-cloud + Config Sync + Policy Controller + CSM |
| Single-greenhouse layout | Zonal control plane (single-zone apiserver/etcd) |
| Three-greenhouse layout | Regional control plane (3-zone apiserver/etcd quorum) |
| Multi-bed planting | Multi-zonal node pools |
| Locked garden gate + visitor pass | Private cluster + master authorized networks |
| Smart-seed planting tools | gcloud / Terraform / Config Connector / Pulumi |
| Garden's house keys (Pod auth) | Workload Identity Federation for GKE |

⚠️ *Analogy stops here:* A garden plot is fixed to the season; GKE clusters are software-defined and reshape constantly. Real Autopilot has admission webhooks that quietly mutate or reject Pod specs — a robot caretaker that occasionally refuses to plant your seed.

## ELI5 / ELI10

**ELI5.** Google has a giant garden. You can rent a plot and do everything yourself, or you can rent a plot where Google's robots plant, water, and harvest for you. There's a fancier subscription that also lets you have plots in other gardens around the world all coordinated. And — pick the three-greenhouse layout, not one greenhouse, so a frost in one doesn't kill everything.

**ELI10.** GKE has three modes. **Standard**: you manage node pools + scaling + ops. **Autopilot**: Google manages nodes + scaling + security baseline; per-Pod billing; Pod-level SLA; Autopilot workloads also run inside Standard clusters. **Enterprise** (formerly Anthos): tier-on-top for fleets + multi-cloud + Config Sync + Policy Controller + Cloud Service Mesh + Connect Gateway + multi-cluster Gateway. Plus regional vs zonal control planes (regional = 3-zone HA), multi-zonal node pools, private clusters + master authorized networks, four provisioning paths (gcloud, Terraform, Config Connector, Pulumi).

## Real-world scenarios

- **SaaS — first GKE cluster picks Autopilot.** A 40-engineer SaaS migrating from Cloud Run to K8s. They pick **regional Autopilot**. *Zero node management*: they declare Pods with resource requests; Google handles the rest. Per-Pod billing aligns the cluster bill to actual usage; off-hours cost approaches zero. *The platform team they didn't hire is the cost saving.*
- **ML team — GKE Standard with GPU node pools.** A 200-engineer ML team needs precise GPU scheduling: A3 H100 nodes for training, A4 H200 for inference, custom NVIDIA driver tuning. **GKE Standard** with three GPU node pools (autoscaling) + custom Compute Classes. Autopilot's admission constraints would block their custom DaemonSet for distributed training. *Trade-off accepted; they staff a small platform team.*
- **Enterprise IT — fleet of 30 clusters across GCP + AWS + on-prem.** A bank acquired three subsidiaries each with their own K8s footprint. They register all clusters into a **GKE Enterprise fleet**. Config Sync deploys uniform NetworkPolicies / Pod-security baselines from one git repo to all clusters. Policy Controller blocks non-compliant deploys at admission. Cloud Service Mesh handles cross-cluster mTLS. *One governance model across heterogeneous K8s.*
- **Outage — zonal cluster, zonal control-plane outage, half-day blackout.** A startup picked zonal GKE for cost. A GCP zone had a control-plane disruption at 09:00. Workloads kept running but the team couldn't deploy a critical feature flag flip. *5 hours of inability to deploy*. Postmortem: migrate all prod clusters to **regional control plane** + multi-zonal node pools. Cost premium per cluster: small. Outage cost: large.

## Common misconceptions

- **Myth:** "Autopilot is just Standard with autoscaling enabled."
  **Truth:** Autopilot is a different cluster shape. Google manages nodes (you don't see them; can't SSH; can't pick SKU directly except via Compute Classes). Per-Pod billing instead of per-node. Built-in admission webhooks block privileged / hostNetwork / hostPath / non-conforming Pods. *Pod-level SLA* instead of control-plane SLA. Different operational model, not a flag.
- **Myth:** "GKE Enterprise is a separate cluster type."
  **Truth:** GKE Enterprise is an add-on tier *on top of* Standard or Autopilot clusters. You enable it on a project / fleet to get fleets + Config Sync + Policy Controller + Cloud Service Mesh + multi-cluster Ingress + Connect Gateway. The cluster underneath is still Standard or Autopilot.
- **Myth:** "Regional control plane just means workloads run across zones."
  **Truth:** **Regional control plane** = apiserver + etcd are replicated across three zones in the region. **Multi-zonal node pools** = workloads distributed across zones. They're independent settings — you can have a regional control plane + a single-zone node pool (apiserver survives, but workloads don't). For full multi-zone resilience, both must be set.

## Recap

Three GKE modes (Standard / Autopilot / Enterprise) × control-plane scope (regional vs zonal) × node-pool topology (zonal / multi-zonal) × apiserver exposure (public / authorized / private). Pick mindfully; Autopilot regional is the safe default.

**Next — G2: GKE Versioning and Release Channels.** Rapid / Regular / Stable / Extended channels; auto-upgrades; maintenance windows + exclusions; version availability + EOS + SLA + upgrade notifications.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
