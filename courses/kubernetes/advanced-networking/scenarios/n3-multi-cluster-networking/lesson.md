# K-ADV-NET N3 — N3 · Multi-Cluster Networking

> Course: K-ADV-NET (advanced specialization)
> Module N3 · Multi-Cluster Networking
> Companion preview: `/preview-kubernetes-adv-net-lesson-03.html`.

---

**🎯 If you remember nothing else:** **Cilium ClusterMesh: low-latency same-CNI; Submariner: CNI-agnostic L4 IPsec; Skupper: L7 app-layer no-IP-route; Istio multi-cluster: mesh extends with shared identity. Pick by trust + perf, not features alone.**

## 1. eBPF-native, same-CNI peering

**Cilium ClusterMesh**: clusters running Cilium peer with each other via cluster-mesh-apiserver; etcd-replicated state; Pod-to-Pod traffic routes natively across cluster boundaries via eBPF. *Same identity model*: SPIFFE IDs unified across clusters; NetworkPolicy rules naturally apply across the mesh.
    Best fit: *same operator owns all clusters*; bandwidth + latency matter; eBPF observability (Hubble) extends across clusters. Common shape: 3-5 prod clusters in different cloud regions, all Cilium, ClusterMesh + global Services + multi-cluster Hubble.
    Constraints: requires Cilium on all clusters; Pod CIDRs must not overlap (tooling helps allocate); BGP / native routing across cloud region boundaries depends on cloud support (Cilium handles encap fallback).

## 2. CNI-agnostic L4 IPsec across heterogeneous clusters

**Submariner**: opens IPsec tunnels between clusters via per-cluster gateways; routes traffic at L4 (Service IP / endpoint slice). Works regardless of CNI — Cilium + Calico + cloud CNI all peer.
    Best fit: *heterogeneous cluster fleet* (different CNIs, different clouds, including on-prem); L4 routing is enough (no L7 mesh required); operational simplicity.
    Constraints: tunnel encap reduces effective MTU + adds CPU; gateway-per-cluster is single point of failure (deploy redundant gateways). Service Discovery via Lighthouse (DNS) — services across clusters resolved via `service.namespace.svc.clusterset.local`.

## 3. Application-layer Virtual Application Network

**Skupper**: deploys per-namespace router; routers connect via TLS (egress only); Services exposed across the VAN. *No IP routing requirement* — clusters can be in completely different network zones (your VPC + partner VPC + on-prem firewalled DC) without VPN / peering / opening firewall ports.
    Best fit: *cross-organization integration*; partner Services exposed without giving network access; security-domain-segmented architectures.
    Constraints: L7 only; per-Service overhead (router Pod); not suitable for high-bandwidth east-west; latency higher than ClusterMesh / Submariner. Good for control-plane integrations + occasional service calls; not for replication-heavy workloads.

## 4. mesh-spanning + how to choose

**Istio multi-cluster**: extends the mesh across clusters with shared / replicated control plane. Two patterns: *primary-remote* (one control plane manages others) + *multi-primary* (per-cluster control plane, replicated state). Workload identity unified via SPIFFE federation; AuthorizationPolicy + VirtualService work cluster-spanning.
    Best fit: *mesh-heavy deployments* already using Istio; rich L7 features required (canary + traffic shifting + mesh observability across clusters); ambitious complexity tolerance.
    **Selection grid**: Same operator, all Cilium, low-latency → ClusterMesh. Heterogeneous CNIs, L4 enough → Submariner. Cross-org / firewall-segmented → Skupper. Already on Istio mesh → Istio multi-cluster. Some teams run two (e.g., ClusterMesh internal + Skupper for partners).

## Before / After

**Before.** Pre-multi-cluster bridges, cross-cluster integration was VPN + manual Service registration + DNS hacks. Each new cluster pair was bespoke; observability fragmented; security model fragile.

**After.** Modern: ClusterMesh / Submariner / Skupper / Istio multi-cluster handle the bridge per architecture. Native Service discovery, unified identity, per-bridge policy. Pick by trust model + perf needs.

*Bridge choice is architectural, not feature-checklist. Match to trust + latency + CNI.*

## Analogy — the K-Highway junction

K-Highway connects to other K-cities via four kinds of **bridge**. The **twin-city expressway** (Cilium ClusterMesh) — both cities share the same urban planner; lanes connect natively; vehicles drive across without slowing. The **border-tunnel** (Submariner) — works between any two cities regardless of urban-planning style; encrypted; some toll. The **diplomatic-pouch service** (Skupper) — one city sends sealed couriers via TLS; no road crossing required; great for foreign-city partners. The **shared-rail-network** (Istio multi-cluster) — mesh-style passenger trains run across both cities under shared identity.
    The Captain doesn't pick by feature; she picks by **who runs the cities** (one operator vs many) + **how fast traffic must flow** + **whether neighbours allow open lanes**.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Twin-city expressway | Cilium ClusterMesh (same-CNI eBPF native) |
| Border-tunnel | Submariner (L4 IPsec tunnel; CNI-agnostic) |
| Diplomatic-pouch courier | Skupper (L7 application-layer VAN) |
| Shared-rail mesh | Istio multi-cluster (mesh extends with shared identity) |
| Twin-city map | Cilium ClusterMesh global Services + multi-cluster Hubble |
| Border-tunnel discovery | Submariner Lighthouse DNS |
| Sealed courier registry | Skupper VAN Service exposure |
| Mesh-wide identity | SPIFFE federation across clusters |

⚠️ *Analogy stops here:* A real bridge can be physically inspected; cluster bridges are policy + encryption + routing — invisible. Synthetic test traffic between clusters is the only reliable verification.

## ELI5 / ELI10

**ELI5.** Four kinds of bridges. Same-style cities use a smooth expressway. Different-style cities use a tunnel. Foreign neighbours use a sealed courier. Cities running shared trains use shared rails. Pick by who you're connecting + how often traffic flows.

**ELI10.** **ClusterMesh**: same-CNI Cilium clusters; eBPF native; lowest latency; unified identity. **Submariner**: CNI-agnostic L4 IPsec gateway pattern; tunnels; Lighthouse DNS. **Skupper**: L7 application VAN; egress-only TLS; no IP-routing required; partner-org pattern. **Istio multi-cluster**: primary-remote or multi-primary; SPIFFE federation; mesh L7 features extend.

## Real-world scenarios

- **Same-org 5-cluster Cilium ClusterMesh.** A 100-engineer org runs 5 Cilium-on-EKS clusters across 3 regions. ClusterMesh peers them; global Services route to nearest cluster; Hubble shows cross-cluster flows. *One identity model, native routing, eBPF observability.*
- **Bank — Submariner across heterogeneous CNIs.** Bank has Cilium-on-EKS + Calico-on-bare-metal + Azure CNI on AKS. Submariner peers all three at L4; gateway redundancy in each; tunnels IPsec-encrypted. CNI heterogeneity preserved; cross-cluster Service discovery via Lighthouse.
- **Skupper for partner SaaS integration.** A retailer's SaaS partner needs to call one billing-Service in our cluster + nothing else. Skupper VAN: partner-side router peers with our router via TLS over public Internet; Service exposed only via the VAN; no VPN, no firewall changes, partner sees nothing else.
- **Outage — Submariner gateway single point of failure.** A team deployed Submariner with one gateway per cluster. The gateway Pod restarted; cross-cluster traffic dropped for 90 seconds. Postmortem: deploy 2+ gateways per cluster + globalnet HA mode; failover is sub-second. Updated runbook + IaC.

## Common misconceptions

- **Myth:** "Pick whichever bridge works first."
  **Truth:** Bridge choice is architectural. Switching bridges later means re-running every cross-cluster Service through new connection paths. Pick deliberately based on trust model + perf + heterogeneity.
- **Myth:** "Multi-cluster mesh requires Istio."
  **Truth:** ClusterMesh / Submariner / Skupper all do multi-cluster Service discovery + connectivity without Istio. Istio mesh is required only when you need full L7 mesh features (canary by header, traffic mirroring, complex AuthorizationPolicy) *across clusters*.
- **Myth:** "Skupper is too slow for production."
  **Truth:** Skupper is L7 app-layer; latency higher than IP-level bridges. *Right tool for partner integrations + control-plane calls*; not for high-bandwidth east-west replication. Used for the right pattern, it's production-grade.

## Recap

Four bridges, four trade-offs. ClusterMesh for same-CNI low-latency. Submariner for heterogeneous L4. Skupper for partner-org L7. Istio multi-cluster for mesh-heavy. Pick by trust + perf + heterogeneity.

**Next — N4: Service mesh + DNS scaling + IPv6.** Mesh selection + operation; CoreDNS + NodeLocal DNSCache scaling; IPv6 + dual-stack at scale.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
