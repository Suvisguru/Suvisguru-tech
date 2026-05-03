# K-AKS A3 — A3 · AKS Networking (Azure CNI, AGC, NetworkPolicy, private clusters)

> Course: Azure AKS (K-AKS, prereq: K-COM + Azure basics)
> Module A3 · AKS Networking
> Companion preview: `/preview-kubernetes-aks-lesson-03.html`.

---

**🎯 If you remember nothing else:** **Three surfaces: CNI (default Overlay; Cilium for performance), ingress (AGC + Gateway API > AGIC), control (private cluster + API VNet Integration). Always plan IP space and outbound (NAT Gateway, not LB SNAT).**

## 1. CNI choice — five options, default is Overlay

Pods need IPs and routing. AKS gives you five CNI options:
    
      - **Azure CNI** (legacy default, traditional) — every Pod gets a real IP from the node's subnet. *Fast, no overlay, but burns IPs* (one VNet IP per Pod). Fine for small clusters; doesn't scale to large ones.

      - **Azure CNI Overlay** (current default) — Pods get IPs from a separate *overlay* CIDR (not in the VNet). Node IPs stay in the VNet; Pod-to-Pod traffic is encapsulated inside VXLAN-like overlay. *Solves the IP-exhaustion problem.* Some Azure-native integrations (e.g. App Gateway v1 backend pools) need extra hops; AGC handles overlay correctly.

      - **Azure CNI Powered by Cilium** — Azure CNI for IPAM (real VNet IPs OR overlay), Cilium for the dataplane (eBPF, no kube-proxy needed, NetworkPolicy + observability). *Performance + visibility*; AKS Automatic uses this by default.

      - **BYO CNI** — install your own (Calico, Cilium upstream, etc.). Advanced; you own all IPAM + lifecycle. Rare in production.

      - **Kubenet** — legacy, NAT-on-node model. *Deprecated 2024*; do not use for new clusters.

    
    **IP planning:** overlay decouples Pod IPs from VNet — you can fit a 10K-node cluster in a /24 VNet. But if you use traditional Azure CNI, do the math: `nodes × pods-per-node ≤ subnet capacity`. **Pod subnet** (separate from node subnet) is supported with Azure CNI for finer-grained segmentation.

## 2. Four ingress paths — pick AGC for new

How does outside traffic reach your Pods? Four paths in increasing modernity:
    
      - **Standard Load Balancer** (L4) — every `Service: type=LoadBalancer` provisions one. Public or internal. Backend = Pod IPs (with Azure CNI / Overlay). The cluster's outbound SNAT also runs through this LB unless you set the outbound type to NAT Gateway.

      - **NAT Gateway** (outbound, recommended) — separate Azure resource for egress. Each NAT Gateway provides up to 64K SNAT ports per attached IP, scaling far beyond the LB-shared default. *Avoids the SNAT-exhaustion outage class.*

      - **AGIC — Application Gateway Ingress Controller** (legacy path) — AKS controller that programs an Application Gateway v1 to route Ingress objects. Works, but slated for end-of-life as Application Gateway for Containers takes over.

      - **Application Gateway for Containers (AGC)** + Gateway API (modern path) — purpose-built L7 LB for K8s. Configured via **Gateway API** (HTTPRoute, TCPRoute) — the K8s-blessed successor to Ingress. Faster reconcile, native Azure integration.

      - **Web Application Routing add-on** — managed NGINX inside the cluster + cert-manager + Azure DNS integration. Useful for self-hosted ingress without third-party Helm charts.

    
    **Decision rule:** new clusters → AGC + Gateway API for L7. Existing AGIC clusters → migration plan. Internal-only services → internal LB or AGC private mode.

## 3. Private clusters + API VNet Integration

By default the AKS apiserver has a public endpoint (FQDN like `mycluster-xxxxxx.hcp.eastus.azmk8s.io`). Two ways to lock that down:
    
      - **Authorized IP ranges** — public endpoint stays, firewall allows only specific CIDRs (your office VPN, your CI runners). Cheapest; no Private Link cost.

      - **Private cluster** — apiserver exposed via **Private Link** with a Private DNS zone. The FQDN resolves to a private IP inside your VNet (or a peered VNet). Public endpoint disabled entirely. Most secure; needs Private DNS hub-spoke design.

      - **API Server VNet Integration** (recommended modern path) — apiserver is injected into a delegated subnet of *your* VNet. No Private Link, no peering hub-spoke. Direct VNet routing. Use this for new clusters that need API isolation.

    
    **Outbound types:** `loadBalancer` (default, shared SNAT — risk of exhaustion), `natGateway` (recommended), `userDefinedRouting` (you provide a route table — for hub-spoke with central NVA), `userAssignedNATGateway`, `none` (private + cluster does no internet — for fully airgapped).

## 4. NetworkPolicy + Web App Routing add-on

**NetworkPolicy** options (you pick at cluster create; can't change in place):
    
      - **Azure NetworkPolicy** — Azure-native implementation. Standard NetworkPolicy semantics. Works with Azure CNI + Overlay.

      - **Calico** — third-party, proven, supports advanced features (egress policy, GlobalNetworkPolicy via Calico CRDs). Free tier.

      - **Cilium** — eBPF-based; standard NetworkPolicy + Cilium NetworkPolicy CRD (DNS-based, L7 awareness). Default with AKS Automatic + Azure CNI Powered by Cilium.

    
    **Web Application Routing add-on:** turns on a managed NGINX ingress controller + cert-manager + Azure DNS integration. Replaces the older HTTP Application Routing add-on (deprecated). For teams that want self-hosted ingress without operating Helm charts.
    **Other plumbing:** dual-stack (IPv4+IPv6) supported with Azure CNI Overlay. Windows networking has its own constraints (no eBPF, NetworkPolicy via Azure or Calico). Private DNS hub-spoke is the typical enterprise topology — central Private DNS zones + cross-VNet links.

## Before / After

**Before.** Pre-Overlay AKS clusters used **traditional Azure CNI**: every Pod consumed a real VNet IP. A 100-node cluster with 30 Pods/node burned 3,000 IPs from your subnet. Plus pre-AGC, ingress meant **AGIC** (programmed Application Gateway v1) — slow reconciles, complex backend pools, awkward overlay handling. Plus default outbound was **LB-shared SNAT** — burst traffic from one service exhausted the pool and broke *everything*.

**After.** Modern AKS uses **Azure CNI Overlay** (default) — Pod IPs come from an overlay CIDR; node IPs stay in VNet; one /24 VNet supports a 10K-node cluster. Ingress uses **Application Gateway for Containers** (AGC) configured via **Gateway API** — purpose-built L7, fast reconciles, native overlay support. Egress uses **NAT Gateway** — 64K SNAT ports per IP, no shared exhaustion. *The networking stack finally stops being the bottleneck.*

*Kubenet is deprecated; AGIC is fading; LB-shared SNAT is dangerous. Use Overlay + AGC + NAT Gateway as the modern default.*

## Analogy — the K-Campus wing

The **Pathways & Quad** are how everything moves around K-Campus. Faculty offices need addresses (IPs); students walk between buildings (Pod-to-Pod traffic); visitors arrive from off-campus and need directions to the right building (ingress); deliveries leave campus to the post office (egress).
    The **address scheme** on campus has options. Traditional: every dorm room has a unique street address from the city block (Azure CNI — every Pod = real VNet IP). Modern: each building has its own internal numbering, the city sees only the building (Azure CNI Overlay — default). High-performance: same as modern, but the building is staffed by Cilium runners who deliver mail with a stopwatch (CNI Powered by Cilium).
    The **front gates** (ingress) — visitors used to be greeted by a slow gatekeeper named AGIC who had to look up a paper map every time. The modern campus has a Concierge Desk (AGC) with the visitor manifest preloaded; visitors get walking directions instantly via Gateway API.
    The **delivery dock** (egress) — for years, all outgoing mail piled into one shared shipping room (LB-shared SNAT) and during finals week the room ran out of shipping labels (SNAT exhaustion). Modern campus added a dedicated post office (NAT Gateway) — virtually unlimited capacity, and one busy professor can't starve another.

**Translation legend.**

| In the story… | …in AKS / Azure |
|---|---|
| Campus address scheme | CNI (Azure CNI / Overlay / Cilium / BYO) |
| Modern building-internal numbering | Azure CNI Overlay — Pods on overlay CIDR |
| Cilium runners with stopwatches | Azure CNI Powered by Cilium (eBPF dataplane) |
| Slow paper-map gatekeeper | AGIC — Application Gateway Ingress Controller (legacy) |
| Concierge Desk with preloaded manifest | AGC + Gateway API |
| In-house mailroom (NGINX inside building) | Web Application Routing add-on |
| Shared shipping room | LB-shared SNAT (default outbound) |
| Dedicated post office | NAT Gateway |
| Locked-gate campus | Private cluster via Private Link |
| Apiserver in your own building basement | API Server VNet Integration |
| "Only these visitor IDs allowed" list | Authorized IP ranges |
| Inter-office delivery rules | NetworkPolicy (Azure / Calico / Cilium) |

⚠️ *Analogy stops here:* A campus has fixed buildings; a cluster's topology is software-defined and reconfigurable. The metaphor doesn't capture overlay encapsulation overhead or BGP route propagation across peered VNets.

## ELI5 / ELI10

**ELI5.** Every worker on campus needs a desk address. There are different ways to give out addresses — some use real city addresses, some use building-internal numbers. Visitors come in through a front gate and a friendly desk tells them where to go. Deliveries leave through a back gate that has to be big enough that everyone's mail fits at once.

**ELI10.** AKS networking has three surfaces. **CNI**: Azure CNI Overlay (default) decouples Pod IPs from VNet — solves IP exhaustion. CNI Powered by Cilium adds eBPF dataplane + DNS-aware NetworkPolicy. Kubenet is deprecated. **Ingress**: AGC + Gateway API for new (purpose-built L7); AGIC is legacy. Standard LB for L4; NAT Gateway for egress to avoid shared SNAT exhaustion. **Control**: API VNet Integration injects the apiserver into your VNet (modern); private cluster via Private Link; or authorized IP ranges. NetworkPolicy via Azure / Calico / Cilium — pick at create time.

## Real-world scenarios

- **Bank — private cluster + API VNet Integration + AGC private mode.** A bank requires no public endpoints. They create the AKS cluster with **API Server VNet Integration** (apiserver IP inside their hub VNet) + Azure CNI Overlay + AGC in private mode (private IP, attached to a private DNS zone). All ingress hits AGC privately; control plane never appears on the public internet. *Pen-test report: zero public-IP attack surface.*
- **SaaS — burst traffic broke SNAT, fixed with NAT Gateway.** A SaaS hit a sudden viral moment — 10× outbound API calls. Within minutes Pods started failing with `SNAT port allocation` errors. Root cause: default LB-shared SNAT. Emergency fix: `az aks update --outbound-type managedNATGateway` with two static IPs. New SNAT capacity = ~128K ports. *Outage resolved in 20 minutes; runbook now mandates NAT Gateway from cluster creation.*
- **Migration — AGIC → AGC across two sprints.** An older cluster runs 40 Ingresses on AGIC + Application Gateway v1. Migration plan: spin up AGC alongside, port Ingresses to `HTTPRoute` (Gateway API), test in parallel, swap DNS, keep AGIC as fallback for 30 days. Sprint 1 = porting + parallel testing; Sprint 2 = cutover + decommission. *No downtime; AGC reconcile times improved 30s → 2s.*
- **Microservices — Cilium NetworkPolicy + L7 awareness.** A 200-service cluster needs strict zero-trust policies. They enable AKS Automatic (Cilium dataplane). Use standard NetworkPolicy for Pod-to-Pod allow lists; use **Cilium NetworkPolicy CRD** for L7 rules ("frontend can call /api/v1/users on backend, nothing else"). Cilium's Hubble UI shows live flow graphs. *Network team and dev team share one mental model.*

## Common misconceptions

- **Myth:** "Kubenet is fine for small clusters."
  **Truth:** Kubenet is deprecated; new AKS clusters cannot use it. Even existing clusters should migrate (Azure has migration tools). The maintained options are Azure CNI, Azure CNI Overlay, Azure CNI Powered by Cilium, and BYO CNI.
- **Myth:** "AGIC and AGC are the same thing."
  **Truth:** **AGIC** = legacy AKS controller programming Application Gateway v1 via Ingress objects. **AGC** = purpose-built L7 LB programmed via Gateway API (HTTPRoute, TCPRoute). Different Azure SKU, different controller, different K8s API. AGC is the modern path; AGIC is end-of-life-bound.
- **Myth:** "My cluster doesn't need a NAT Gateway because it's small."
  **Truth:** Default LB-shared SNAT gives a cluster ~64 ports per node by default — and bursty workloads can exhaust them. Even a 5-node cluster can SNAT-exhaust if a single Pod opens hundreds of outbound connections. NAT Gateway is the safe-by-default choice from cluster creation; the cost of one NAT Gateway is small relative to the cost of an outage.

## Recap

Three networking surfaces understood: CNI (Overlay default, Cilium for performance), ingress (AGC + Gateway API for new), control (API VNet Integration + private endpoints). NAT Gateway is the egress safety net.

**Next — A4: AKS Storage.** Azure Disks CSI (Premium SSD v2, Ultra, VolumeAttributesClass), Azure Files CSI (RWX SMB/NFS), Blob CSI (BlobFuse2), Azure NetApp Files, Azure Container Storage, Secrets Store CSI with Key Vault, snapshots, ZRS, topology-aware scheduling.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
