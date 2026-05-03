# K-VAN V1 — V1 · Production Architecture Design for Self-Managed K8s

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V1 · Production Architecture
> Companion preview: `/preview-kubernetes-vanilla-lesson-01.html`.

---

**🎯 If you remember nothing else:** Production self-managed K8s starts as a **blueprint**: control-plane sizing, worker sizing, etcd sizing, API LB, Pod/Service CIDR, CNI, CSI, OS choice, runtime, HA topology (stacked vs external etcd), backup, upgrade, security baseline. Get the blueprint right; everything downstream is mechanical.

## 1. Why the architecture phase exists

Managed K8s (EKS / GKE / AKS) hides 80% of the architecture decisions behind a console — the cloud picks the topology, the networking, the upgrade strategy. Self-managed K8s gives you all of those decisions. *You are the cloud now*. That power is liberating until day 90, when a wrong choice in week 1 forces a cluster rebuild.
    Architecture is the document that turns "we want a Kubernetes cluster" into *this many CPUs, on these subnets, with these CIDRs, this CNI, this etcd topology, with these backup intervals*. It also says what you are *not* trying to optimise (cost? availability? latency?). Without that explicit list, every later argument is unresolvable.

## 2. Three sizing axes

ComponentDrives sizingFloor for production
      
        Control planeNumber of nodes, Pods, Services, watch load3 nodes (HA quorum) · 4 vCPU / 8 GiB each for ≤ 250 nodes; 8/16 for ≤ 500
        WorkerWorkloads + room to evictMix of sizes; reserve 20% headroom for spikes + rolling updates
        etcdObject count, write rate, snapshot size3 members minimum · NVMe SSD · 8 GiB+ RAM · 4 vCPU+ · < 10ms p99 fsync
      
    
    **Stacked vs external etcd.** Stacked = etcd runs on the same nodes as kube-apiserver. Simpler bootstrap; one less tier to operate. External = etcd on its own nodes. More resilient (apiserver crash doesn't affect etcd), more flexible scaling, more ops surface. *For a small org, stacked is fine. For 500+ node clusters, external.*

## 3. CIDRs, DNS, and the LB

You pick five things, and once they're in production they're hard to change without a cluster rebuild:
    
      - **Pod CIDR** — the IP space Pods come from. Default `10.244.0.0/16`. Must NOT overlap with any network reachable from the cluster (corporate VPN, peered VPCs, on-prem subnets). 65K IPs, divided per node.

      - **Service CIDR** — virtual IPs for Services. Default `10.96.0.0/12`. ~1M IPs. Must NOT overlap with Pod CIDR or any reachable network.

      - **Cluster DNS** — IP within the Service CIDR (typically `10.96.0.10`) where CoreDNS lives. Hard-coded into `/etc/resolv.conf` for every Pod.

      - **Dual-stack / IPv6** — opt-in at install time. Once on, you can't un-stack without rebuild. If you're running out of IPv4 (cluster of clusters, IP scarcity), plan for v6 or dual-stack from day 1.

      - **API server LB** — clients always hit `https://<LB>:6443`. Options: kube-vip (built into your kubeadm bootstrap), HAProxy + keepalived (classic), MetalLB (for L2/BGP), an external hardware LB. The LB IP is part of the API server's certificate SANs.

## 4. OS, runtime, CNI, CSI, ingress, backup

- **OS** — Ubuntu LTS (most-tested), Debian, Rocky/Alma (RHEL-compatible), Flatcar (immutable), **Talos Linux** (no SSH, API-driven, immutable; modern choice for 2026).

      - **Runtime** — **containerd 2.x** (the default). CRI-O is the alternative. Docker shim is dead.

      - **CNI** — Cilium (eBPF, modern default), Calico (BGP, mature), Antrea, Flannel (simple labs), kube-router, OVN-Kubernetes. *Lesson V4.*

      - **CSI** — Longhorn (cloud-native block, on-prem), Rook-Ceph, OpenEBS, vSphere CSI, your storage vendor. Snapshot controller required for VolumeSnapshot.

      - **Ingress / Gateway** — Envoy Gateway, Cilium Gateway, Contour (Gateway API). Ingress NGINX is EOL end of 2026.

      - **Backup** — Velero (the standard), restic for file-level, etcd snapshots for control-plane state.

    
    [ deep dive — skip if new ]For air-gapped or compliance-heavy environments, additional choices: image mirror (Harbor + signing), private cert authority, audit log forwarding, SOPS/Sealed Secrets for git-stored secrets, FIPS-mode kernel + crypto. These rarely change once decided; document them in the architecture doc.

## Before / After

**Before.** "We installed kubeadm and it worked." Six months later: Pod CIDR overlaps the new VPC peering, etcd disk pressure causes random slowdowns, no documented backup procedure, manual operations only one person knows, no upgrade plan. Migration off this cluster takes a quarter.

**After.** One-page architecture doc lives in git. CIDRs documented + non-overlapping. etcd on dedicated NVMe. CNI/CSI choices recorded with rationale. Backup interval + restore tested. Upgrade rehearsal scheduled quarterly. The same doc onboards new engineers in an afternoon.

Time spent on the blueprint is the highest-leverage hour you'll ever spend on a self-managed cluster.

## Analogy — the K-Frontier site

The Drafting Hut is the first stop on the K-Frontier homestead. Before a single tool comes out, you sit at the survey table and draw what you're building: where the well goes, where the main house sits, where the watchtower commands the property, how the road approaches the front gate. The drawing names the materials (OS, runtime), the dimensions (CIDR sizes), the foundations (etcd disks), the perimeter (LB, network), and the contingencies (backup chest). You'll deviate from it later — but only consciously, with a pencil note.

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| Survey table with the cluster blueprint | Production architecture document |
| Where the well goes | etcd topology + sizing |
| Main house location | Control-plane node placement + sizing |
| Property road + front gate | API server LB + network ingress |
| Plot lines (don't dig past these) | Pod CIDR + Service CIDR + node subnets |
| Materials list | OS, runtime, CNI, CSI, ingress controller choices |
| Backup chest | Velero + etcd snapshot strategy |
| Watchtower position | Hardening posture + bastion access |

⚠️ *Analogy stops here:* The analogy stops here: a real cluster has many feedback loops the homestead drawing doesn't capture — autoscaling, controller reconciliation, certificate rotation. The drawing is initial conditions, not the running system.

## ELI5 / ELI10

**ELI5.** Before you build a house, you draw it on paper. Where the kitchen goes, where the lights are, where the water comes in. Same with a Kubernetes cluster: you draw it before you start pouring concrete.

**ELI10.** Self-managed K8s = you make every architectural choice the cloud usually hides. Sizing (CP / worker / etcd), HA topology (stacked vs external etcd), network plan (Pod CIDR / Service CIDR / DNS / LB / dual-stack), OS, runtime, CNI, CSI, ingress, backup. Document these in a one-page architecture spec before kubeadm runs. Wrong CIDRs and undersized etcd are unfixable without a rebuild.

## Real-world scenarios

- **A startup picking stacked etcd + Cilium + Talos.** 3 control-plane + 5 worker bare-metal cluster. Stacked etcd (simpler ops). Talos Linux (immutable, API-driven, no SSH). Cilium CNI with kube-proxy replacement. Pod CIDR `192.168.224.0/20` (deliberately picked to avoid the corporate `10.0.0.0/8`). The whole architecture doc fits on two pages.
- **A bank with external etcd + air-gapped + Calico.** 5 dedicated etcd nodes (NVMe, isolated subnet) + 5 control-plane + 30 worker nodes across 3 racks. Calico with BGP peering to top-of-rack switches (no VXLAN; full underlay routing). Air-gapped install via internal Harbor mirror. RHEL 9 hardened to CIS Level 2. Architecture doc is 18 pages with explicit compliance evidence pointers.
- **A team that re-architected after pain.** First cluster: 2 CP nodes (no quorum), shared etcd disks with kubelet, Pod CIDR `10.0.0.0/24` exhausted at 250 Pods. Rebuilt 18 months in: 3 CP nodes, dedicated etcd disks, Pod CIDR bumped to `/16`, CNI swapped Flannel → Cilium. The rebuild was 3 weeks of pain that 1 day of architecture would have prevented.
- **A team using Cluster API (CAPI) for declarative lifecycle.** Management cluster runs Cluster API. Workload clusters declared as YAML — desired-state managed like any other K8s resource. CAPV (vSphere), CAPA (AWS), CAPZ (Azure), CAPG (GCP) providers handle the underlying infra. Architecture-as-code; new clusters are PRs.

## Common misconceptions

- **Myth:** "We can change the Pod CIDR later if we need to."
  **Truth:** Pod CIDR is set in stone at cluster creation. Changing it is a rebuild. Pick a non-overlapping range, big enough for projected node count × max Pods per node × 2x growth, on day 1.
- **Myth:** "Two control-plane nodes is half-redundant."
  **Truth:** Two etcd members can't form quorum after one fails — you need ≥ 3 (or technically odd numbers ≥ 3 — 3, 5, 7). Two CP nodes is worse than one because losing either takes down the cluster. Always odd, always ≥ 3 for HA.
- **Myth:** "Talos and Flatcar are exotic; just use Ubuntu."
  **Truth:** Talos in particular has gained massive adoption in 2024-26 for production self-managed clusters. No SSH, immutable, API-managed. Smaller attack surface, simpler upgrades. Worth evaluating against Ubuntu — the right choice is org-specific, not always the obvious one.

## Recap

Architecture-first. Sizing, network plan, OS/runtime/CNI/CSI choices, HA topology, backup, upgrade strategy. One page in git, referenced by every subsequent module.

**Next — V2: OS and Node Preparation.** Now that you have the blueprint, prepare the soil: kernel modules, sysctl, swap, time sync, runtime install, image pre-pulling. The land has to be cleared before the frame goes up.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
