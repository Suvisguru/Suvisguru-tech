# Lesson 24 — Networking Foundations · Linux Primitives, CNI, MTU

> Course: Kubernetes — Common to all distributions
> Module 12 · Networking depth · Lesson 1 of 3
> Companion preview: `/preview-kubernetes-lesson-24.html`.

---

**🎯 If you remember nothing else:** Every Pod gets a Linux `veth` pair pulled into a node bridge. The **CNI plugin** creates the veth, assigns the IP, and connects nodes (encapsulation or native routing). Modern CNIs (**Cilium**) use **eBPF** instead of iptables — much faster and more observable. The most common production bug: **MTU mismatch**.

## 1. The Linux primitives behind every Pod

K8s networking is not new infrastructure — it's *Linux networking applied at scale*. Each node is a regular Linux box with extra namespaces. Each Pod has its own `net` namespace (covered in Lesson 8) — its own loopback, its own routing table, its own iptables/nftables. The Pod sees a single network interface (`eth0`); the host sees its other end as a `veth` pair.
    The four primitives you need:
    
      - **`veth` pair** — a virtual cable. One end is in the Pod's net namespace as `eth0`; the other is on the host. Whatever's sent into one end pops out the other.

      - **Bridge** (e.g., `cni0`, `cilium_host`) — a virtual L2 switch on the host. Every Pod's host-side veth plugs into it. Pods on the same node can talk to each other across the bridge with no further help.

      - **Routing table** — for cross-node traffic, the host's routing table must know "Pod 10.1.2.4 is on node-B." That entry is installed by the CNI plugin (or by BGP if the CNI uses native routing).

      - **iptables / nftables / eBPF** — packet rules: NAT for outbound traffic, Service load balancing (kube-proxy), NetworkPolicy enforcement.

    
    Run `ip link show`, `ip route show`, `iptables -t nat -L -n` on any K8s node and you see exactly this. K8s doesn't add anything new at the data-plane layer — it choreographs a thousand standard Linux pieces.

## 2. One spec, many implementations

The **Container Network Interface (CNI)** is a CNCF spec. Two roles: a *runtime* (the kubelet, in K8s) calls *plugins* (binaries on the node) at three lifecycle moments — ADD (set up Pod networking), DEL (tear down), CHECK (verify). The plugin's job: create the Pod's veth, assign an IP, set up routing. The runtime feeds back to K8s.
    The major CNI plugins:
    
      PluginStyleNotes
      
        CiliumeBPF, native routing or VXLANFastest, best observability, supersedes kube-proxy. De-facto modern choice.
        CalicoBGP routing, optional VXLAN, eBPF data planeMature, widely deployed in regulated environments. Strong policy support.
        FlannelVXLAN encapsulationSimple, common in lab clusters. Limited policy support.
        AWS VPC CNIPod gets a real ENI IPEKS default. No encapsulation; Pods are first-class VPC citizens.
        Azure CNI / GKE Dataplane V2Cloud-nativeGKE Dataplane V2 = Cilium-based by default in 2026.
      
    
    Two big architectural choices: **encapsulation vs native routing** (does each cross-node packet get wrapped in a VXLAN header, or do nodes route directly?), and **iptables vs eBPF** for Service load balancing (eBPF is dramatically faster at scale — kube-proxy with iptables hits perf cliffs at ~5000 Services).

## 3. The thing that kills latency you can't explain

The **Maximum Transmission Unit (MTU)** is the largest packet your interface can send without fragmentation. Standard Ethernet: 1500 bytes. VXLAN encapsulation adds 50 bytes of header. So your Pod's effective MTU on a VXLAN-overlay cluster is 1450, not 1500. *If the CNI hasn't told the Pod's eth0 about this*, the Pod thinks it can send 1500-byte packets, the host wraps them in VXLAN making 1550, the underlay rejects them, fragmentation/retransmits ensue.
    Symptoms: cross-node traffic mysteriously slow, sometimes specific HTTP requests time out (the ones with bodies large enough to hit MTU), TCP throughput plateaus way below line rate. The diagnostic command:
    `# From inside a Pod
ping -M do -s 1472 <another-pod-ip>   # 1472 + 28 (ICMP+IP) = 1500
# If this fails with "Frag needed", you have an MTU mismatch.`
    Modern CNIs (Cilium, Calico) auto-detect underlay MTU and configure Pod MTU accordingly. Older or hand-rolled setups: read the CNI's docs, set MTU explicitly. AWS EKS clusters: jumbo frames (MTU 9001) on most instance types — your CNI should pick this up.
    [ deep dive — skip if new ]The classic MTU bug: a cluster runs fine for months. Someone migrates from VXLAN to native routing (no encap header). They forget to bump the Pod MTU back up to 1500. Now Pods send 1450-byte packets when 1500-byte underlay is available — 3% throughput loss for no reason. Or vice versa. The fix: pin Pod MTU to `$UNDERLAY_MTU - $ENCAP_OVERHEAD` in the CNI config and forget it.

## 4. Where Service IPs come from

Lesson 17 covered ClusterIP from the user's view: "Service has a virtual IP that load-balances to the Pods." The implementation was **kube-proxy**: a per-node DaemonSet writing iptables rules. Each Service got a chain with one rule per backend Pod, randomised. It worked, it scaled to a few thousand Services, and then it didn't.
    Modern alternative: **eBPF-based Service routing** (Cilium kube-proxy replacement, Calico eBPF data plane, GKE Dataplane V2). The kernel's eBPF programs do Service load balancing in the network stack at the socket level — no iptables chains, no per-rule overhead. At 50,000 Services Cilium beats iptables-mode kube-proxy by orders of magnitude on throughput and connection establishment time.
    Beyond performance: eBPF gives you observability the iptables model couldn't. Cilium Hubble exposes per-flow visibility (which Pod is talking to which Service, what's getting denied by NetworkPolicy, where latency is). Tools like `tcpdump -i any` on a node now have a structured equivalent.

## Before / After

**Before.** Pre-CNI / pre-eBPF era: docker0 bridge per node, iptables for everything, kube-proxy generating thousands of rules per Service. Cross-node debugging meant `tcpdump -i eth0` on every hop. NetworkPolicy was best-effort. Service performance ceiling somewhere around 5000 Services.

**After.** Modern era: standardised CNI plugins, eBPF data plane (Cilium / Calico eBPF), per-flow observability via Hubble, NetworkPolicy enforced in kernel programs, Service performance scales linearly to 50K+ Services. The IP layer feels boring — exactly the goal.

Cilium's 2024-25 dominance pushed the rest of the industry toward eBPF. By 2026 nearly every new cluster is eBPF-based; iptables-mode kube-proxy is legacy.

## Analogy — the K-Town district

The Switchboard is K-Town's telephone exchange (Lesson 17 was the customer-facing front desk). Today we go behind the wall. Every apartment (Pod) has a phone (eth0) connected to a wire (one end of a **veth pair**) running to the building's switchboard (the node bridge). The switchboard connects every apartment in the building. To reach an apartment in *another* building, the call goes out through the building's trunk line, across town, into the other building's switchboard.The **CNI plugin** is the contractor who runs all this wiring. Different contractors use different methods: Cilium uses eBPF (think: programmable junctions in the wire), Calico uses BGP (the buildings know each other's routing maps directly), Flannel uses VXLAN (every cross-building call gets wrapped in an extra envelope). All of them deliver the call. They differ on speed, observability, and how they handle policy.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The phone in the apartment | Pod's `eth0` interface |
| The wire from phone to switchboard | `veth` pair (Pod side + host side) |
| The building's switchboard | Node bridge (`cni0`, `cilium_host`) |
| The contractor who ran the wiring | CNI plugin |
| The trunk line between buildings | Inter-node tunnel (VXLAN) or direct route |
| The wrapped envelope on cross-building calls | VXLAN encapsulation header (50 bytes) |
| Wires too thin for fat envelopes | MTU mismatch (encap overhead exceeds Pod MTU) |
| Pre-eBPF: kube-proxy iptables — old-school operator boards | iptables-mode kube-proxy |
| eBPF: programmable junctions in the wire itself | Cilium / GKE Dataplane V2 / Calico eBPF |

⚠️ *Analogy stops here:* The analogy stops here: real packets aren't "calls" — they're datagrams that can be lost, reordered, or split mid-flight. The CNI's job is harder than wiring; it has to handle live re-IPing, Pod churn, and policy enforcement in microseconds.

## ELI5 / ELI10

**ELI5.** Every toy phone has a wire. The wire goes to a big board in the room (the bridge). The room's board connects to the room next door's board. The contractor who put in the wires is the CNI.

**ELI10.** Each Pod has a Linux network namespace with its own `eth0`. `eth0` is one end of a `veth` pair; the other end is on the host plugged into a bridge. Cross-node traffic goes through inter-node routing or VXLAN encap. The CNI plugin is the per-node binary the kubelet calls (ADD/DEL/CHECK) on Pod lifecycle to set this up. The biggest production bug is MTU mismatch when encap overhead exceeds underlay capacity. Modern CNIs use eBPF instead of iptables for Service load balancing — much faster at scale and dramatically more observable.

## Real-world scenarios

- **A SaaS migrating from kube-proxy to Cilium.** Replaced kube-proxy with Cilium's kube-proxy replacement. Service-establishment latency dropped from 50µs to 8µs. NetworkPolicy moved from iptables to eBPF; no perf cliff at high rule count. Hubble lit up with per-flow visibility — they found three policy violations they didn't know existed.
- **A bank running Calico with BGP peering.** No encap. Every node BGP-peers with the top-of-rack switch. Pod IPs routable across the data center directly. No VXLAN overhead, no MTU surprises. Tradeoff: requires network team coordination and infrastructure that supports BGP.
- **An EKS cluster using AWS VPC CNI.** Pods get real VPC ENI IPs. Pod-to-Pod traffic goes through the VPC, no overlay, no encap. MTU = 9001 (jumbo frames). Tradeoff: ENI count limits how many Pods per node; needs careful node-type selection.
- **A team debugging a 200ms latency that wasn't supposed to be there.** Symptoms: only large HTTP responses slow. `ping -M do -s 1472` failed cross-node. MTU mismatch confirmed. CNI ConfigMap MTU bumped from 1500 to 1450 to account for VXLAN overhead. Latency normalised. Total fix time: 4 hours of mystery + 2 minutes of fix.

## Common misconceptions

- **Myth:** K8s networking is its own special thing.
  **Truth:** K8s networking is Linux networking applied with namespaces and a CNI plugin. Every primitive (`veth`, bridges, routing tables, iptables) is bog-standard Linux. The novelty is automation, not the data plane.
- **Myth:** Encapsulation is a performance disaster.
  **Truth:** VXLAN encap costs ~5-10% throughput on most workloads. Native routing is faster but requires infrastructure cooperation (BGP-capable switches, or cloud VPC integration). For most clusters, encap is fine; chase native routing only when measured throughput matters.
- **Myth:** kube-proxy is required for K8s networking to work.
  **Truth:** kube-proxy implements *Services* (ClusterIP/NodePort), not Pod-to-Pod connectivity. CNIs like Cilium replace kube-proxy entirely. Pod-to-Pod just needs the CNI.

## Recap

Pods get veth pairs into a node bridge; CNI plugin handles routing across nodes (encap or native). Modern CNIs (Cilium) use eBPF for both data plane and Service routing — much faster than iptables-mode kube-proxy. The single most common production bug is MTU mismatch.

**Next — Lesson 25: Gateway API.** The Ingress API is being retired in favour of the Gateway API across the entire ecosystem. Roles, listeners, routes, the Ingress NGINX migration story, and what changes for app teams. Switchboard, customer side.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
