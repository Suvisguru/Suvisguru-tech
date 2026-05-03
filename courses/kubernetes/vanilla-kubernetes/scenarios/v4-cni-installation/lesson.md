# K-VAN V4 — V4 · CNI Installation and Cluster Networking

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V4 · CNI and Networking
> Companion preview: `/preview-kubernetes-vanilla-lesson-04.html`.

---

**🎯 If you remember nothing else:** Choose CNI by trade-off: **Cilium** (eBPF, fastest, observability via Hubble, kube-proxy replacement), **Calico** (BGP-native, mature, eBPF data plane optional), **Antrea / OVN-K** (OVS-based, SDN-friendly), **Flannel / kube-router** (simple, limited policy). The CNI's Pod CIDR config **must match** kubeadm's podSubnet. **MTU**: pod MTU = underlay MTU minus encap overhead.

## 1. Why CNI is its own decision

kubeadm doesn't install a CNI on purpose: K8s is intentionally network-plugin-agnostic. The CNI handles three things: assign Pod IPs from the cluster CIDR, route packets between Pods on different nodes, enforce NetworkPolicy. Different CNIs solve all three differently — and you can't change CNI on a running cluster without significant ceremony (drain + uninstall + reinstall + reschedule everything).
    For vanilla self-managed in 2026, the realistic choices are Cilium (eBPF), Calico (BGP), Antrea / OVN-Kubernetes (OVS), and Flannel / kube-router for the tiny / lab end. Each has a strong identity:

## 2. What each is good at

CNIData planeNetworkPolicyEncryptionObservabilityBest for
      
        **Cilium**eBPF in-kernelStandard + L7 + FQDN + cluster-meshWireGuard / IPsecHubble (per-flow)Modern default; production at scale
        **Calico**BGP routing or VXLAN; eBPF dp opt-inStandard + global + FQDNWireGuard / IPsecCalico Whisker (newer)Compliance, regulated, FIPS
        **Antrea**OVSStandard + multi-clusterIPsecTheia / Antrea UIVMware-aligned shops; SDN parity
        **OVN-Kubernetes**OVN/OVSStandardIPsecOVN traceOpenShift, large SDN setups
        **Flannel**VXLANLimited (no native enforcement)none built-innoneLabs, simplest possible
        **kube-router**BGPiptables-basednoneLimitedBGP-only, no VXLAN
      
    
    **For a fresh 2026 production cluster: Cilium is the modern default.** Calico is the regulated alternative. The other choices serve specific niches.

## 3. Cilium walkthrough (Helm)

Cilium ships a Helm chart. Critical alignment with your kubeadm config:
    `helm repo add cilium https://helm.cilium.io
helm install cilium cilium/cilium --version 1.16.0 \
  --namespace kube-system \
  --set ipam.operator.clusterPoolIPv4PodCIDRList="192.168.224.0/20" \
  --set kubeProxyReplacement=true \
  --set k8sServiceHost=api.cluster.corp \
  --set k8sServicePort=6443 \
  --set tunnel=disabled \
  --set ipv4NativeRoutingCIDR=192.168.224.0/20 \
  --set autoDirectNodeRoutes=true \
  --set hubble.enabled=true \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true`
    What this does: native routing (no VXLAN/Geneve overhead), Cilium replaces kube-proxy entirely (kube-proxy DaemonSet should be deleted: `kubectl -n kube-system delete ds kube-proxy`), Hubble enabled for per-flow observability.
    Verify after install:
    `cilium status --wait
cilium connectivity test    # ~5 min, exhaustive
hubble observe --since 1m   # see flows`

## 4. MTU, dual-stack, multi-network, switching CNIs

**MTU.** Pod MTU must be ≤ underlay MTU minus encapsulation overhead. VXLAN: 50-byte overhead. Geneve: 60-byte. WireGuard: 60-80. Native routing: 0. Cilium auto-detects but verify: `kubectl -n kube-system exec ds/cilium -- cilium status | grep MTU`.
    **Dual-stack.** If you set both IPv4 + IPv6 in kubeadm's `networking.podSubnet`, the CNI must support dual-stack (Cilium yes, Calico yes, Flannel limited). Once enabled at install, can't un-stack without rebuild.
    **Multi-network** via **Multus**. A meta-CNI that lets Pods have additional interfaces from secondary CNIs (SR-IOV, MACVLAN). Used in NFV, telecom, ML training with dedicated NICs. Adds operational complexity; only when you need it.
    **Switching CNIs on a running cluster.** Painful but doable. Steps: drain nodes, uninstall old CNI (delete DaemonSet, remove `/etc/cni/net.d/*`, reset iptables), install new CNI, uncordon. Test network policy semantics on a non-prod cluster first; the L4/L7 nuances differ between Cilium and Calico.
    [ deep dive — skip if new ]For air-gapped: pull all CNI images to your internal registry, configure containerd registry mirror so the CNI Helm chart's image references resolve. The CNI typically pulls 4-8 images; small relative to add-on stack.

## Before / After

**Before.** Cluster bootstrapped, every node NotReady. Trial-and-error CNI install. Wrong Pod CIDR alignment requires reset + reinstall. MTU mismatch causes intermittent failures days later. NetworkPolicy enforcement different from what was assumed.

**After.** CNI install via Helm + values committed to git. Pod CIDR matches V1 architecture decision. MTU verified at install. `cilium connectivity test` passes. Hubble shows live flows. NetworkPolicy enforced consistently.

CNI is "install once, change rarely" — get the choice right before the cluster has workloads.

## Analogy — the K-Frontier site

Wiring & Plumbing is the fourth site. The frame is up; now the contractor lays the trenches and runs the cables. Different contractors do this differently. **Cilium** uses programmable junctions (eBPF) right inside the wires; **Calico** uses big ring-main routing (BGP) tying the buildings together; **Flannel** wraps every cross-building call in an extra envelope (VXLAN). The wires must match the building's plug-spec (Pod CIDR matches kubeadm config); the cable thickness must accept the largest packets you'll send (MTU); and the contractor sets up the meters that show what's flowing (Hubble / Whisker).

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| The wiring contractor | CNI plugin |
| Programmable in-wire junctions | Cilium eBPF data plane |
| Ring-main BGP routing | Calico BGP |
| Wrapping every cross-building call | VXLAN encapsulation |
| Plug-spec matching | Pod CIDR alignment kubeadm ↔ CNI |
| Cable thickness limit | MTU (underlay − encap overhead) |
| Live flow meters | Hubble / Calico Whisker |
| Telecom-grade specialty wiring | Multus + secondary CNIs (SR-IOV) |

⚠️ *Analogy stops here:* The analogy stops here: networking isn't physical wires — every Pod IP is a virtual interface in a Linux namespace. The CNI's job is configuring tens of thousands of these abstractions per cluster, not laying cable.

## ELI5 / ELI10

**ELI5.** The frame is up but there's no electricity yet. The wiring crew picks how to wire it (Cilium / Calico / etc.), runs the wires through the walls, and turns it on.

**ELI10.** Until you install a CNI, every node is NotReady. Cilium (eBPF, modern default) or Calico (BGP, mature) for production. Pod CIDR must match between kubeadm config and CNI install. MTU = underlay - encap overhead. Cilium can also replace kube-proxy entirely. Hubble (Cilium) or Whisker (Calico) for per-flow observability. Switching CNIs on a running cluster is possible but painful.

## Real-world scenarios

- **A SaaS using Cilium with kube-proxy replacement.** Cilium installed via Helm. kube-proxy DaemonSet deleted. eBPF handles Service load balancing in-kernel. Hubble enabled for flow visibility. `cilium connectivity test` in CI on every cluster create. Network performance: cross-node latency 0.4ms; kube-proxy iptables would have been 1.5ms+ at the same scale.
- **A bank running Calico with BGP.** Calico configured for BGP peering with TOR (top-of-rack) switches. No VXLAN — Pod traffic is native routed across the underlay. Compliance team approves: predictable routing, no encap overhead, mature codebase. WireGuard enabled for cross-node mTLS at the data plane. eBPF data plane opt-in for performance.
- **An NFV team using Multus + SR-IOV.** Telco workload (5G User Plane Function) needs dedicated NICs with hardware offload. Multus as meta-CNI; primary CNI is Cilium (for control plane traffic), secondary is SR-IOV (for data plane). Pods get two interfaces. Operational complexity is real; the perf gain (line-rate forwarding) justifies it.
- **A team that switched Flannel → Cilium.** Started with Flannel for simplicity. Hit limitations: weak NetworkPolicy enforcement, no observability, kube-proxy bottleneck at 5K Services. Migration plan: install Cilium with chaining mode (Cilium on top of Flannel) for one week of validation, then drain + uninstall Flannel + reinstall Cilium native. Total downtime per node: ~5 minutes during drain.

## Common misconceptions

- **Myth:** "All CNIs implement NetworkPolicy the same way."
  **Truth:** Standard NetworkPolicy is a CRD spec — but L7 features, FQDN matching, AdminNetworkPolicy support, encryption all vary. Cilium has the richest feature set; Calico is close; Antrea has multi-cluster; Flannel doesn't enforce at all.
- **Myth:** "VXLAN is always slower than native routing."
  **Truth:** VXLAN adds ~5-10% throughput overhead; for most workloads it's invisible. Native routing requires BGP-capable infrastructure or cloud VPC integration. Pick by infra capability, not raw perf.
- **Myth:** "You can swap CNI without taking workloads down."
  **Truth:** Possible but messy. Easiest path: drain nodes one at a time, uninstall old CNI, install new CNI, uncordon. Cluster is degraded during the migration. Plan it like a major upgrade.

## Recap

CNI install is install-once, change-rarely. Cilium is the modern default; Calico for compliance. Pod CIDR alignment + MTU tuning are the two install-time gotchas. Hubble or Whisker for observability.

**Next — V5: Core Add-ons.** CoreDNS, metrics-server, ingress / Gateway, cert-manager, CSI, ExternalDNS, Sealed Secrets / SOPS, monitoring + logging stack. The outbuildings around the main house.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
