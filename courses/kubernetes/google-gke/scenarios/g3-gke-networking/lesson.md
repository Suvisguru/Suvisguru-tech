# K-GKE G3 — G3 · GKE Networking (VPC-native, Dataplane V2, Gateway, multi-cluster, CSM)

> Course: Google GKE (K-GKE, prereq: K-COM + GCP basics)
> Module G3 · GKE Networking
> Companion preview: `/preview-kubernetes-gke-lesson-03.html`.

---

**🎯 If you remember nothing else:** **VPC-native + Dataplane V2 + Gateway API + NEG container-native LB is the modern default. Plan IP space (Pod + Service secondary ranges) generously; firewall the GFE health-check ranges open; use Cloud NAT for egress; Cloud Service Mesh for mTLS + traffic management.**

## 1. VPC-native (alias IP) + IP planning

**VPC-native** clusters give every Pod and Service a real VPC IP via *alias IP ranges* on the node. Pods communicate directly via VPC routing — no NAT, no overlay encap. *The default for new GKE clusters; routes-based legacy is deprecated.*
    VPC-native clusters need three IP ranges:
    
      - **Node range (primary subnet)** — IPs for nodes themselves. Plan: max-nodes you'll ever scale to.

      - **Pod secondary range** — IPs allocated to Pods. Per-node alias range carved from this. Plan: `(max-nodes × default-max-pods-per-node × 2 buffer)`. *Default 110 Pods per node × 1024 nodes = ~225K IPs needed*; underspecify and you stop scheduling Pods even with empty CPU.

      - **Service secondary range** — IPs for ClusterIP Services. Smaller; default sufficient for most clusters.

    
    **IP exhaustion mitigation:** use larger Pod secondary ranges from the start (you can't resize a Pod range in place — need new node pool with different range). Tune `--max-pods-per-node` (default 110; can be lowered to reduce per-node alias usage). Use Discontiguous Multi-Pod CIDR for very large clusters. *Plan IP space at cluster creation; this bites later otherwise.*

## 2. Dataplane V2 + NetworkPolicy + Cloud NAT

**GKE Dataplane V2** = Cilium-based eBPF dataplane. Default for new clusters. Replaces kube-proxy (iptables / IPVS). Faster service routing, better observability (Hubble flow visibility), L4 + L7 NetworkPolicy.
    **NetworkPolicy**: standard K8s NetworkPolicy works on Dataplane V2. Plus *FQDN NetworkPolicy* (block egress to specific DNS names — useful for data-exfiltration prevention). Plus Cilium NetworkPolicy CRD for L7 rules ("allow GET /api on this service, deny POST"). *Default-deny per namespace + explicit allow lists* is the standard zero-trust posture.
    **Cloud NAT** for egress: Pods on private clusters have no public IPs. Outbound to internet (Stripe, package registries, third-party APIs) goes through Cloud NAT — managed NAT, scales NAT ports per attached IP. Avoids the SNAT-exhaustion class of outage that LB-shared SNAT causes on other clouds.
    **Master authorized networks** + **private cluster** from G1 apply at the network layer — control-plane access restricted to specific CIDRs, nodes private with Cloud NAT for egress.

## 3. Ingress, Gateway, NEG, container-native load balancing

**GKE Ingress** (legacy path) — controller programs a Google Cloud Load Balancer (HTTP(S) LB) from `Ingress` objects. Backend = NEG (Network Endpoint Group) of Pod IPs (container-native LB). Annotations on the Ingress configure the LB (TLS cert, backend config, Cloud Armor policy, IAP).
    **GKE Gateway controller** (modern) — first-class **Gateway API** support. Resources: `GatewayClass` (e.g. `gke-l7-global-external-managed`), `Gateway`, `HTTPRoute`, `TLSRoute`, `TCPRoute`. Cleaner separation of platform-team (Gateway) and app-team (HTTPRoute) responsibilities. Supports *multi-cluster Gateway* across clusters in a fleet.
    **NEG (Network Endpoint Group)** = the GCP LB primitive that holds Pod IPs (container-native LB) instead of node IPs (instance-group LB). Faster failure detection (LB sees Pod IP go away immediately instead of via kube-proxy NAT chain), lower latency. *Required for Ingress / Gateway in modern GKE.*
    **Multi Cluster Ingress (MCI) + Multi Cluster Services (MCS)** = single Ingress / Service that fronts Pods across multiple GKE clusters in a fleet (different regions). MCI gives you a global anycast IP with traffic routed to the nearest healthy cluster. MCS lets a Service in cluster A address Pods in cluster B. *Foundation for multi-region active-active.*

## 4. Cloud Service Mesh, Shared VPC, NCC, firewall + DNS

**Cloud Service Mesh (CSM)** = managed Istio for GKE. Sidecars on Pods for mTLS / traffic management / observability; Google operates the control plane. Works fleet-wide via GKE Enterprise — *cross-cluster mTLS without DIY mesh-of-meshes*.
    **Shared VPC** — host project owns the VPC + subnets; service projects (multiple GKE clusters across teams) attach. Centralised network ops; team-level cluster autonomy. Common enterprise pattern.
    **Network Connectivity Center (NCC)** = hub-spoke connectivity orchestrator: cross-region VPC peering, on-prem hybrid (Cloud Interconnect / Cloud VPN spokes), inter-cloud connectivity. For multi-cluster + hybrid topologies.
    **Firewall rules** — *critical:* firewall must allow GFE health-check IP ranges (`35.191.0.0/16`, `130.211.0.0/22`) to reach NEG-backed Pods, or LBs report all backends unhealthy. Plus standard Pod-to-Pod permits (Cilium NetworkPolicy is layered on top).
    **DNS troubleshooting**: **Cloud DNS for GKE** (managed kube-dns alternative, scales better; use `--cluster-dns=clouddns`). NodeLocal DNSCache to reduce DNS latency + load on cluster DNS. CoreDNS in default mode for compatibility. *DNS issues are the #2 cause of intermittent failures after IP exhaustion.*

## Before / After

**Before.** Pre-Dataplane-V2 GKE used kube-proxy (iptables/IPVS) for service routing. Pre-Gateway-controller, ingress meant the legacy Ingress object + Cloud LB. Multi-cluster anything = bring-your-own. Network Policy was bring-your-own (Calico). Mesh was bring-your-own (self-installed Istio). Routes-based clusters were the default — slow VPC-route lookups capped at low scale. IP planning was an afterthought.

**After.** Modern GKE ships **VPC-native + Dataplane V2 + Gateway API + NEG container-native LB** as defaults. Multi Cluster Ingress + Multi Cluster Services let one Service span clusters. **Cloud Service Mesh** is managed Istio. **Cloud DNS for GKE** + NodeLocal DNSCache solve scale-related DNS issues. *Operations + workloads share a coherent network model.*

*Plan IP space generously at creation; everything else is reasonable defaults.*

## Analogy — the K-Garden plot

The **Pathways & Trellises** are the hidden infrastructure of the K-Garden — paths visitors walk, irrigation pipes that connect plots, trellises that direct climbing plants where to grow. Six surfaces.
    The **address scheme**: every plant has a real garden address (VPC-native alias IP), not just a tag. The garden has three address books: one for the plot beds (Node range), one for the plants (Pod secondary range), and one for the watering taps (Service secondary range). *Underspecify the plant address book and you can't plant new flowers even in empty beds.*
    The **path engineer** is the *Cilium runner* (Dataplane V2) who delivers messages between plants via eBPF lanes — much faster than the old hand-delivered (kube-proxy) routes. The Cilium runner also enforces "who can talk to whom" rules (NetworkPolicy).
    The **front gates** — visitors used to enter through the slow gatekeeper (legacy Ingress controller programming Cloud LB). The modern garden has a Concierge (Gateway controller) who works the same Cloud LB but speaks Gateway API natively and can run a single concierge desk across multiple gardens at once (multi-cluster Gateway).
    The **plant directory** (NEG) lists each plant's exact address; the front-gate Concierge sends visitors directly to the plant, not via a generic plot lookup.
    The **delivery dock** (Cloud NAT) handles all packages leaving the garden — managed by Google, scales to plenty.
    And the **plant-to-plant courier service** (Cloud Service Mesh) is a managed Istio offering: every plant gets a personal courier (sidecar) for mTLS-encrypted notes between plants — and you can extend the courier service across multiple gardens worldwide.

**Translation legend.**

| In the story… | …in GKE / GCP |
|---|---|
| Garden address scheme | VPC-native (alias IP) |
| Plot bed address book | Node range (primary subnet) |
| Plant address book | Pod secondary range (alias IP per node) |
| Watering-tap address book | Service secondary range (ClusterIP) |
| Cilium runner with eBPF lanes | Dataplane V2 |
| "Who can talk to whom" rules | NetworkPolicy (incl. FQDN, L7 via Cilium) |
| Slow gatekeeper | GKE Ingress (legacy controller path) |
| Modern Concierge | GKE Gateway controller (Gateway API) |
| Concierge across gardens | Multi-cluster Gateway / MCI |
| Plant directory | NEG (Network Endpoint Group, container-native LB) |
| Delivery dock | Cloud NAT (egress for private clusters) |
| Plant-to-plant courier | Cloud Service Mesh (managed Istio) |
| Shared garden plumbing | Shared VPC (host + service projects) |
| Inter-garden tunnel network | Network Connectivity Center |
| Health inspector visit lane | Firewall rule allowing 35.191.0.0/16 + 130.211.0.0/22 (GFE health checks) |

⚠️ *Analogy stops here:* A garden's path layout is fixed; GKE's VPC-native is software-defined and reshapes per node-pool config — but Pod CIDRs cannot be resized in place, so the metaphor under-states this constraint.

## ELI5 / ELI10

**ELI5.** Plants in the garden have real addresses (not nicknames) so they can talk to each other directly. A fast runner delivers messages and enforces the rules of who-can-talk-to-whom. The front gate has a modern Concierge who handles visitors. Letters out of the garden go through a delivery dock. And there's a courier service for private notes between plants.

**ELI10.** GKE networking = VPC-native (alias IP, real Pod IPs) with three IP ranges (node + Pod secondary + Service secondary — plan generously). Dataplane V2 (Cilium-based eBPF, default) replaces kube-proxy + adds NetworkPolicy + L7 + Hubble. GKE Gateway controller (Gateway API) is the modern ingress; legacy Ingress works but Gateway is preferred. NEG = container-native LB (Pod IPs in the LB backend, not node IPs). MCI/MCS for multi-cluster. Cloud Service Mesh = managed Istio. Cloud NAT for egress. Firewall must allow GFE health-check ranges 35.191.0.0/16 + 130.211.0.0/22.

## Real-world scenarios

- **SaaS — multi-region active-active via Multi Cluster Ingress.** A SaaS runs three regional GKE clusters (us, eu, asia). Single Multi Cluster Ingress provides one global anycast IP; traffic routed to the nearest healthy cluster. Failover automatic if a region degrades. *One DNS name, one cert, three clusters.*
- **Bank — Shared VPC + Cloud Service Mesh fleet-wide mTLS.** A bank's host project owns the VPC; six service projects each run team-owned GKE clusters. Cloud Service Mesh (managed Istio) registered in the fleet provides mTLS between Pods across clusters + projects. Network team owns the VPC + firewall; team clusters consume it. *Centralised compliance, distributed app teams.*
- **IP exhaustion outage — Pod range too small.** A cluster created with default Pod secondary range (/14 ≈ 256K IPs sounded plenty). Six months later, autoscaling hits 800 nodes × 110 Pods × per-node alias overhead = exhausted. New Pods stuck Pending with no IPs. Fix: create new node pool with much larger Pod range; drain old workloads; delete old pool. *Cannot resize in place.*
- **NEG health-check 503s root-caused by missing firewall rule.** An ingress backend started returning 503s. NEG marked all Pod IPs unhealthy. Root cause: Terraform refactor removed the firewall rule allowing `35.191.0.0/16` + `130.211.0.0/22` (GFE health-check IPs) into the Pod range. Restored rule; NEG marked Pods healthy in 30 seconds. *Postmortem: pin the GFE-allow rule with a documented Terraform comment so future refactors don't remove it.*

## Common misconceptions

- **Myth:** "Routes-based clusters still work fine."
  **Truth:** Routes-based GKE clusters are *legacy* and deprecated. They use VPC routes for Pod traffic, hitting per-VPC route quota at low scale (a few hundred routes total). All new clusters should be VPC-native (alias IP); existing routes-based clusters need migration via blue-green to a new VPC-native cluster.
- **Myth:** "NEG and Instance Group LB backends are interchangeable."
  **Truth:** **NEG (container-native LB)** = LB sends traffic directly to Pod IPs (via VPC-native alias IPs). Faster failure detection, lower latency, kube-proxy not in the data path. **Instance Group LB** = LB sends traffic to node external IPs; kube-proxy NATs to Pods. Slower failure detection, kube-proxy hop. *NEG is required for modern Ingress / Gateway and for Cloud Service Mesh.*
- **Myth:** "Dataplane V2 only matters for NetworkPolicy."
  **Truth:** Dataplane V2 also: replaces kube-proxy (faster service routing, fewer iptables rules), enables Hubble flow observability, supports FQDN NetworkPolicy and L7 policies via Cilium, accelerates Service ClusterIP performance at scale. NetworkPolicy is one feature; the dataplane upgrade affects everything.

## Recap

Six surfaces: VPC-native + Dataplane V2 + Gateway/Ingress + NEG + MCI/MCS + CSM. Plan IP space at creation; firewall the GFE ranges; Cloud NAT for egress.

**Next — G4: GKE Identity and Security.** IAM + RBAC + IAM Conditions; Workload Identity Federation for GKE; Binary Authorization; Security Posture; Container Threat Detection (SCC); Confidential GKE Nodes (AMD SEV / Intel TDX); Shielded GKE Nodes; Secret Manager CSI; Artifact Registry; Policy Controller + Config Sync; GKE Sandbox (gVisor); CMEK.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
