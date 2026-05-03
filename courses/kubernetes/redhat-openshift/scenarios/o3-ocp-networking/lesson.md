# K-OCP O3 — O3 · OpenShift Networking

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O3 · OpenShift Networking
> Companion preview: `/preview-kubernetes-ocp-lesson-03.html`.

---

**🎯 If you remember nothing else:** **OVN-Kubernetes is default; SDN is removed. Routes for TLS-aware ingress; Gateway API for modern multi-cluster. NetworkPolicy + EgressIP + Egress firewall for control. Multus + SR-IOV for telco. MetalLB for bare-metal LoadBalancer. NetObserv for flow visibility.**

## 1. OVN-Kubernetes + cluster/service/machine networks

**OVN-Kubernetes** is OCP's default CNI (default since OCP 4.12; OpenShift SDN was deprecated and is now removed). Built on Open Virtual Network (OVN) + Open vSwitch (OVS). Provides:
    
      - Pod networking (cluster network)

      - Service networking (kube-proxy replacement using OVN)

      - NetworkPolicy enforcement

      - EgressIP, Egress firewall, Egress router CRDs

      - Multi-network via Multus integration

      - IPv6 + dual-stack

    
    **Three network ranges** defined at install time:
    
      - **Cluster network** (Pod CIDR) — default `10.128.0.0/14`. Pods get IPs from here.

      - **Service network** (Service CIDR) — default `172.30.0.0/16`. ClusterIP Services from here.

      - **Machine network** (host network) — the actual VM/host subnet. Nodes have IPs here.

    
    Plan ranges generously at install — the cluster network is hard to expand later. Default `/14` = 256K Pod IPs which is plenty for most. Larger clusters need explicit planning.

## 2. Routes + Ingress + Gateway API — three ingress paths

**Route** = OpenShift's ingress primitive (predates K8s Ingress). Configured by the **IngressController** Operator + **Router pods** (HAProxy-based by default). Three TLS termination modes:
    
      - **Edge termination** — TLS terminates at the Router; Pod traffic is HTTP. Cert lives on the Route or Router default.

      - **Passthrough** — TLS passes through Router untouched. Pod terminates TLS itself (e.g. mTLS apps).

      - **Re-encrypt** — Router terminates the inbound TLS, then re-encrypts to Pod with a separate cert. For Pod-side TLS without sharing the public cert.

    
    **Ingress** (K8s standard) — also supported in OCP. The Ingress controller maps Ingress objects to Routes under the hood. Use Ingress for portability across clusters; Routes for OCP-specific TLS termination flexibility.
    **Gateway API** — OpenShift Service Mesh (Istio-based) + Gateway API support. Gateway / GatewayClass / HTTPRoute / TCPRoute. Modern path; for new ingress in OCP 4.13+ on Service Mesh.
    **IngressController CRD** — defines the public ingress(es). Default created at install. Add additional IngressControllers for sharded ingress (per-namespace, per-domain, internal-only LB on bare metal, etc.).

## 3. NetworkPolicy + EgressIP + Egress firewall + Egress router

**NetworkPolicy** (K8s standard) — namespace-scoped Pod-to-Pod allow/deny. Default is allow-all; apply default-deny per Project for zero-trust. Works on OVN-Kubernetes natively.
    **AdminNetworkPolicy + BaselineAdminNetworkPolicy** (newer K8s standard) — cluster-wide admission policies for network rules. Override per-namespace NetworkPolicies. Useful for enforcing org-wide deny-egress-to-internet baselines.
    **EgressIP** (CRD) — assign a deterministic source IP to traffic egressing from a Project. Useful when an external system whitelists by source IP. The egress IP attaches to a specific node; OCP fails it over to another node if the host fails.
    **Egress firewall** (CRD) — restrict which external IPs/domains a Project can talk to. CIDR-based or DNS-name-based rules. Blocks egress at the OVN-K layer.
    **Egress router** (CRD) — older mechanism: a dedicated Pod that source-NATs egress traffic to a fixed IP. EgressIP is preferred; Egress router still exists for niche cases.

## 4. Multus + SR-IOV / DPDK + MetalLB + NetObserv + Submariner

**Multus CNI** — attach Pods to *multiple networks*. The default cluster network plus 1+ additional networks defined as `NetworkAttachmentDefinition`. For Pods needing direct bridge to a VLAN, SR-IOV adapter, or secondary VPC.
    **SR-IOV + DPDK** — Single Root I/O Virtualization gives Pods direct hardware access to a NIC virtual function (VF). DPDK runs network stack in userspace. *For telco / NFV: 5G UPF, vRouter, low-latency packet processing.* SR-IOV Operator manages VFs.
    **NMState Operator** — declarative host-network configuration. `NodeNetworkConfigurationPolicy` (NNCP) defines bonding, VLANs, bridges, etc., applied per node group. Replaces hand-edited NetworkManager configs.
    **MetalLB Operator** — LoadBalancer Service support on bare-metal clusters (no cloud LB available). L2 mode (ARP/NDP) or BGP mode. Address pools allocate VIPs.
    **Submariner** — multi-cluster networking: Pod IPs and Services routable across registered clusters. For multi-cluster service mesh + DR.
    **NetObserv (Network Observability) Operator** — eBPF-based flow capture. Visualises east-west traffic, NetworkPolicy drops, DNS lookups in the OCP console. Storage backed by Loki (or external).

## Before / After

**Before.** Pre-OVN-K, OCP used OpenShift SDN (now removed). OCP-specific Egress features didn't exist; for fixed source IP you ran a sidecar SOCKS proxy. Bare-metal had no LoadBalancer; you used NodePort + external HAProxy. Multi-network was DIY. NetObserv was bring-your-own (Hubble or DIY tcpdump).

**After.** Modern OCP networking: **OVN-Kubernetes default** + cluster/service/machine networks; **Routes** (TLS edge/pass/re-enc) + **Ingress** + **Gateway API**; **NetworkPolicy** + **EgressIP** + **Egress firewall**; **Multus + SR-IOV + DPDK** for telco; **MetalLB Operator** for bare-metal LB; **Submariner** for multi-cluster; **NetObserv** for eBPF flow visibility.

*OCP networking is now coherent: one CNI (OVN-K), three ingress paths (Routes / Ingress / Gateway API), policy + egress + observability all first-class.*

## Analogy — the K-Foundry bay

The **Pipework & Conveyors** are the foundry's hidden infrastructure. The **OVN-Kubernetes Conveyor System** is the standardized rail network — every cart (Pod) gets an address (IP from cluster network); every workstation (Service) gets a virtual address (Service network); the foundry floor itself sits on the machine network.
    Visitors enter through one of three door types: the classic **Route Door** (Foundry-Master-built; TLS edge/passthrough/re-encrypt termination right at the door), the standard **Ingress Door** (K8s-portable but mapped to a Route under the hood), or the modern **Gateway Door** (Gateway API + Istio for service-mesh ingress).
    Inside, the Foundry has **traffic policies**: NetworkPolicy controls which carts can drive between which workstations; EgressIP gives a Project's outbound carts a fixed plate (source IP); Egress firewall whitelists which external addresses carts can reach.
    Specialty pipework: **Multus** (multi-track carts wired to multiple networks); **SR-IOV / DPDK** (direct-rail express trains for ultra-low-latency telco workloads); **MetalLB** (bare-metal LB-on-rails); **Submariner** (cross-foundry rail network); **NetObserv** (eBPF flow camera over every rail).

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| OVN-Kubernetes Conveyor System | OVN-K CNI (default; OCP 4.12+) |
| Cart address | Pod IP (from cluster network) |
| Workstation virtual address | Service IP (from service network) |
| Foundry floor address | Node IP (from machine network) |
| Route Door | OpenShift Route (TLS edge/pass/re-encrypt) |
| Ingress Door | K8s Ingress (mapped to Route under the hood) |
| Gateway Door | Gateway API + OpenShift Service Mesh (Istio) |
| Door operator | IngressController + Router pods (HAProxy) |
| Inter-station traffic policy | NetworkPolicy (K8s standard) |
| Cluster-wide policy override | AdminNetworkPolicy / BaselineAdminNetworkPolicy |
| Fixed plate for outbound carts | EgressIP (CRD) |
| Allowed external addresses list | Egress firewall (CRD) |
| Multi-track cart | Multus + NetworkAttachmentDefinition |
| Express telco rail | SR-IOV + DPDK |
| Bare-metal LB-on-rails | MetalLB Operator |
| Cross-foundry rail link | Submariner |
| Foundry flow camera | NetObserv (eBPF) Operator |

⚠️ *Analogy stops here:* A real foundry has fixed pipework; OVN-K is software-defined and reshapes per Pod. SDN-removal means existing OpenShift SDN clusters need migration — an operational lift the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** The factory has invisible rails (network) connecting workstations. Visitors come through doors — the Foundry-Master-built doors handle the TLS keys; standard doors are simpler but map to the same backend. Some carts wear special license plates so the outside world recognises them.

**ELI10.** OCP networking = OVN-K CNI (default; SDN removed) + three IP ranges (cluster/service/machine networks). Three ingress paths: Routes (TLS edge/pass/re-enc native), Ingress (K8s portable, maps to Route), Gateway API (Service Mesh modern). Policy + egress: NetworkPolicy / AdminNetworkPolicy / EgressIP / Egress firewall / Egress router. Specialty: Multus multi-net, SR-IOV/DPDK telco, MetalLB bare-metal LB, Submariner multi-cluster, NetObserv eBPF flow visibility, NMState declarative host networking.

## Real-world scenarios

- **Bank — EgressIP + Egress firewall for outbound API allowlist.** A bank's payment Project must call an external partner API that whitelists by source IP. EgressIP assigns a fixed IP to the Project; Egress firewall restricts the Project's egress to only the partner's API range. *Compliance-mandated allowlist enforced at the cluster network layer.*
- **Telco — SR-IOV + DPDK for 5G UPF.** Telco running 5G User Plane Function on OCP. Pods need wire-speed packet processing. SR-IOV Operator allocates NIC VFs to UPF Pods; DPDK userspace network stack inside the Pod. Sub-millisecond latency; line-rate throughput. *OCP carries telco workloads alongside enterprise workloads on the same platform.*
- **Bare metal — MetalLB BGP for LoadBalancer Services.** Bare-metal OCP cluster needs `type: LoadBalancer` Services. MetalLB Operator with BGP mode peers with the data-center spine routers; advertises VIPs from a configured pool. Failover handled at L3 routing layer. *Cloud-style LoadBalancer on bare metal.*
- **Multi-cluster failover — Submariner connects Routes across regions.** Active-active OCP deployment in two regions. Submariner extends Pod + Service networking across both clusters. ServiceExport in cluster A makes a Service reachable from cluster B. Failover routes traffic across regions transparently. *Multi-cluster service mesh without per-region DNS choreography.*

## Common misconceptions

- **Myth:** "OpenShift SDN still works; we can stay on it."
  **Truth:** OpenShift SDN is **removed** (no longer ships in modern OCP minors). Existing SDN clusters MUST migrate to OVN-Kubernetes via documented migration. *Plan + execute the migration on a defined schedule*; it's not optional.
- **Myth:** "Routes and Ingress do exactly the same thing."
  **Truth:** Routes have OCP-specific TLS termination flexibility (edge / passthrough / re-encrypt) and OCP-native annotations (haproxy timeouts, balance, etc.). Ingress is K8s-portable but maps to Routes via the IngressController under the hood. For OCP-specific TLS modes, use Route directly; for portable manifests, use Ingress.
- **Myth:** "NetworkPolicy is enough; I don't need Egress firewall."
  **Truth:** NetworkPolicy controls allow/deny at the cluster boundary by Pod selector. **Egress firewall** restricts a Project's egress to specific *external* CIDRs / DNS names — useful for compliance "only call these external APIs." They're complementary, not duplicates.

## Recap

OVN-K + Routes/Ingress/Gateway + NetworkPolicy/EgressIP/Egress firewall + Multus/SR-IOV/MetalLB + Submariner + NetObserv. The Pipework + Conveyors map is internalised.

**Next — O4: OpenShift Security.** OAuth providers + integrated OAuth server + LDAP/OIDC/HTPasswd; OCP RBAC + Security Context Constraints (SCCs) — restricted-v2 default; SCC vs PSA; Compliance Operator + File Integrity + Security Profiles; RHACS (StackRox); KMS + FIPS + sandboxed containers (Kata).

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
