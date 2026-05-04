# K-ADV-NET N1 — N1 · CNI Internals, eBPF, BGP at Scale

> Course: K-ADV-NET (advanced specialization)
> Module N1 · CNI + eBPF + BGP
> Companion preview: `/preview-kubernetes-adv-net-lesson-01.html`.

---

**🎯 If you remember nothing else:** **CNI = Pod's network. eBPF = in-kernel programmable datapath; replaces iptables for modern CNIs. BGP = native routing across the fabric; eliminates encap tax. Pick CNI by features (NetPol, mesh integration, eBPF maturity) + scale.**

## 1. What CNI does, who provides it

**CNI (Container Network Interface)** is a thin spec — a binary that takes a JSON config + a network namespace, attaches an interface, returns the IP. K8s calls CNI per Pod create/delete; CNI plugin handles the network. Plugins fall into families:
    
      - **Cilium**: eBPF-native; rich features (NetworkPolicy, ClusterMesh, Service mesh, observability via Hubble, mTLS); modern default for non-cloud-managed clusters.

      - **Calico**: BGP + iptables/eBPF; NetworkPolicy heritage; widely deployed in regulated workloads.

      - **Cloud-managed**: AWS VPC CNI (ENI per Pod), Azure CNI, GKE Dataplane V2 (Cilium-based) — tightly cloud-integrated; managed for you.

      - **Flannel**: simple overlay; lightweight; legacy or learning use.

    
    Pick by needs: features (NetPol, mesh, observability), scale (per-node Pod density), control (your own fabric vs cloud).

## 2. Kernel-attached programs replace iptables

**eBPF** (extended Berkeley Packet Filter) lets you attach small programs to kernel hooks — at TC ingress/egress, XDP, socket, syscall. CNIs like Cilium attach programs that do load-balancing, NetworkPolicy enforcement, encapsulation, observability — all in-kernel, no userspace round-trip.
    Why this matters at scale: **iptables** rules grow linearly with Service count; cluster with 10K Services has chains so long that connection setup costs ms. **eBPF maps** are O(1) hash lookups + O(N) for some policy paths but with much better constants. Cilium reports up to 5× lower P99 latency vs iptables-based stacks at 10K-Service scale.
    Other eBPF wins: **Hubble** gives per-flow visibility without packet capture; **Tetragon** does runtime security at kernel level; **XDP** for DDoS protection at line rate. The same eBPF infrastructure powers networking + security + observability.

## 3. Native Pod-CIDR routing across the fabric

By default, Pod CIDRs are local to the cluster — a node's Pods can't be reached natively from other nodes. CNIs solve this with **encapsulation** (VXLAN / Geneve) — wrap the Pod packet in a node-to-node tunnel — or **native routing** via BGP.
    With **BGP**, each node peers with the top-of-rack (ToR) switch and advertises its Pod CIDR. The ToR routes Pod-IP packets directly to the right node. *No encap tax*; line-rate forwarding; latency drops; MTU isn't reduced.
    Operationally: BGP requires fabric cooperation. Cloud clusters often can't (AWS VPC won't accept your BGP peer); they fall back to encap or use VPC-route-injection patterns. Bare-metal + on-prem clusters with their own fabric → BGP shines. **MetalLB**, **Cilium BGP Control Plane**, **Calico BGP** are the implementations.

## 4. IP address management + density limits

**IPAM**: who hands out Pod IPs. Three patterns:
    
      - **CIDR-per-node**: each node gets a /24 (or larger) from a cluster CIDR; CNI hands out Pod IPs from the node's slice. Simple; wastes IPs at low Pod density.

      - **Cluster-pool dynamic**: CNI requests a sub-CIDR per node on demand; better packing at the cost of CNI-control-plane chatter (Cilium's ipam=cluster-pool).

      - **Cloud ENI per Pod**: AWS VPC CNI; each Pod gets its own ENI in the VPC; ENI count caps Pod density. Trunk ENI / IPv4 prefix delegation lifts the cap.

    
    **Scale gotchas**: conntrack saturation at high CPS (especially short-lived connections) — tune `nf_conntrack_max`; switch to eBPF where conntrack isn't used. MTU mismatch causes silent drops on encap paths — set Pod MTU to (host MTU − encap overhead) explicitly. NodeLocal DNSCache reduces CoreDNS load 5×.

## Before / After

**Before.** Pre-eBPF / pre-BGP, K8s networking ran on overlay (VXLAN / IP-in-IP) + iptables. At 10K-Service scale, iptables walks added latency. Encap reduced MTU + added CPU. Observability required tcpdump + ad-hoc tools.

**After.** Modern: eBPF datapath (Cilium / GKE Dataplane V2 / Calico eBPF) gives O(1) Service lookups; BGP native routing eliminates encap; Hubble / Pixie give built-in observability. Same hardware, 5× better latency tail.

*The kernel + the fabric matter. Pick CNI + routing model to match cluster scale + control.*

## Analogy — the K-Highway junction

K-Highway is the cluster's interstate. Every Pod is a vehicle entering the highway. The **on-ramp** (veth pair) connects the Pod's driveway to the host's lane. The **highway controller** (CNI plugin) decides which lane the vehicle takes, applies tolls (NetworkPolicy), and routes onward.
    Underneath the asphalt is a layer of **kernel-level traffic management** (eBPF) — tiny programmable rules that route, filter, and observe packets without ever leaving the kernel. Old highways used a long checklist (iptables) that every vehicle waited at; modern highways use a hash-keyed kiosk (eBPF map) — pull a slip, walk through.
    Beyond the cluster, the highway connects to the **regional fabric** via BGP. Each toll-booth (node) advertises its lane numbers (Pod CIDR) to the regional dispatch (ToR). Vehicles from another region can route directly to the right lane — no detour through tunnels.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| On-ramp | veth pair (Pod ↔ host netns) |
| Highway controller | CNI plugin (Cilium / Calico / VPC CNI / Flannel) |
| Kernel toll kiosks | eBPF programs (TC ingress/egress, XDP, socket) |
| Old long checklist at toll | iptables chains (linear, slow at scale) |
| Hash-keyed kiosk | eBPF maps (O(1) lookups) |
| Regional dispatch | BGP peer (ToR / fabric) |
| Lane numbers advertised | Pod CIDRs advertised via BGP |
| IP plate dispenser per region | IPAM (CIDR-per-node / cluster-pool / ENI-per-Pod) |
| Tunnel detour | VXLAN / Geneve encapsulation |
| Dashcam observability | Hubble (Cilium eBPF flow log) |

⚠️ *Analogy stops here:* A highway's lanes are physical; CNI lanes are eBPF maps + iptables. Misconfiguration is invisible until a probe runs (tcpdump, hubble, kubectl trace).

## ELI5 / ELI10

**ELI5.** Every Pod is a car entering the highway. A controller decides which lane it takes. The road has tiny smart sensors (eBPF) that route + observe in real time. The highway connects to the city via a regional dispatch (BGP) so cars don't need to take detours.

**ELI10.** **CNI** = plugin model that gives a Pod a network. Cilium (eBPF), Calico (BGP / eBPF), VPC CNI (cloud), Flannel (overlay). **eBPF** = kernel-attached programs handling routing + LB + policy + observability in-kernel; replaces iptables for scale. **BGP** = native fabric routing of Pod CIDRs; eliminates encap tax; needs fabric cooperation. **IPAM**: CIDR-per-node, cluster-pool, or ENI-per-Pod. **Scale gotchas**: conntrack saturation, MTU mismatch, DNS load.

## Real-world scenarios

- **Cilium eBPF migration — 5× latency tail improvement.** A 200-engineer SaaS migrated from kube-proxy iptables to Cilium kube-proxy-replacement (eBPF). At 8K Services, P99 connection-setup latency dropped from 30ms to 6ms. Same hardware, same workloads.
- **Bare-metal BGP — encap tax eliminated.** A bare-metal cluster ran VXLAN encap; MTU reduced; CPU on encap rose 8% per node. Adopted Calico BGP peering with ToR switches; advertised Pod CIDRs; encap dropped; throughput rose 30%; CPU dropped.
- **AWS VPC CNI ENI density crisis.** A team ran AWS VPC CNI; m5.large nodes hit ENI limits; Pods stuck PENDING. Enabled **prefix delegation** (each ENI gets a /28); per-node Pod density rose 16×. Same instance type; same VPC.
- **Outage — MTU mismatch.** A team adopted a new CNI without updating Pod MTU. Encap packets exceeded host MTU; large requests silently dropped (small worked). 6-hour debug. Postmortem: explicit MTU calculation in CNI config; CI test for jumbo-payload paths.

## Common misconceptions

- **Myth:** "All CNIs are equivalent — pick the one that's defaulted."
  **Truth:** Major differences: NetPol support (Calico, Cilium yes; Flannel no), eBPF (Cilium, Calico yes; VPC CNI partial), ClusterMesh / multi-cluster (Cilium yes), observability (Cilium's Hubble vs nothing). Pick by feature needs, not default.
- **Myth:** "eBPF replaces iptables completely."
  **Truth:** In modern CNIs (Cilium, Calico-eBPF), eBPF replaces kube-proxy iptables for Service load balancing + NetPol. iptables/nftables remain for some host firewall + edge cases. Cilium has "kube-proxy-replacement" mode that fully eliminates kube-proxy.
- **Myth:** "BGP is too complex; just use overlay."
  **Truth:** For non-cloud clusters (bare-metal, on-prem), BGP is the standard. Calico's BIRD or Cilium's BGP Control Plane both handle the BGP-to-ToR peering with minimal config. The complexity vs encap tax trade favors BGP for scale.

## Recap

Three layers: CNI (Pod's network), eBPF (in-kernel datapath replacing iptables), BGP (native fabric routing eliminating encap tax). Pick by features, scale, control. Tune MTU + conntrack + DNS at scale.

**Next — N2: Gateway API at fleet scale.** GatewayClass + Gateway + HTTPRoute / GRPCRoute / TCPRoute; cross-namespace routing via ReferenceGrant; BackendTLSPolicy; Ingress migration; controller choice (Envoy Gateway, Istio, Cilium, NGINX).

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
