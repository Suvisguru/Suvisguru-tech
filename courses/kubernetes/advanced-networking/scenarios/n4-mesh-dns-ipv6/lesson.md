# K-ADV-NET N4 — N4 · Service Mesh + DNS + IPv6

> Course: K-ADV-NET (advanced specialization)
> Module N4 · Mesh + DNS + IPv6
> Companion preview: `/preview-kubernetes-adv-net-lesson-04.html`.

---

**🎯 If you remember nothing else:** **Pick mesh by needs (Istio rich; Linkerd simple-fast; Cilium eBPF-native). NodeLocal DNSCache + ndots:1 are non-optional at scale. IPv6 / dual-stack: enable per layer; legacy apps need readiness checks.**

## 1. Istio · Linkerd · Cilium Service Mesh · Kuma

**Istio**: most features (traffic shifting + canaries + AuthorizationPolicy + L7 metrics + multi-cluster); largest ecosystem; sidecar or ambient mode. Highest complexity; most operational tools needed.
    **Linkerd**: Rust micro-proxy; minimal overhead; SPIFFE-based identity; simple operational model; ambient-style by default. Recommended for teams wanting mTLS + retries + metrics without Istio's feature surface.
    **Cilium Service Mesh**: eBPF-native; integrates with Cilium NetPol + Hubble. Sidecar-less; can run with or without Envoy. Picks if cluster CNI is already Cilium.
    **Kuma**: built on Envoy; multi-cluster + multi-mesh patterns; vendor-supported by Kong. Niche compared to Istio / Linkerd / Cilium for K8s-only deployments.

## 2. CoreDNS + NodeLocal DNSCache + ndots tuning

**CoreDNS** is the cluster DNS server (replaced kube-dns long ago). At scale, CoreDNS Pods become the bottleneck — every Pod resolution hits them.
    **NodeLocal DNSCache**: a DaemonSet that runs a CoreDNS instance on every node + intercepts DNS queries via iptables / IPVS. *5× reduction in CoreDNS Pod load* + lower P99 latency (cache hit on local node = sub-millisecond).
    **ndots:1 + autoPath**: K8s default `ndots:5` means short names are tried with cluster.local + namespace + svc + cluster suffixes — many DNS queries per resolution. Setting `ndots:1` + autoPath collapses this to fewer queries; further reduces CoreDNS load.
    **Sizing**: CoreDNS replicas should scale with node count; HPA on CoreDNS Pods + NodeLocal DNSCache as DaemonSet is the production pattern.

## 3. cluster + CNI + Service + Pod IPv6 enablement

**Dual-stack**: cluster runs both IPv4 + IPv6. Enable across layers:
    
      - **kubelet**: `--cluster-dns` with both v4 + v6 IPs.

      - **kube-apiserver** + **kube-controller-manager**: `--service-cluster-ip-range=10.96.0.0/12,fd00::/108` (dual ranges).

      - **CNI**: Cilium / Calico / VPC CNI all support IPv6 + dual-stack — enable per CNI config.

      - **Service**: `ipFamilyPolicy: PreferDualStack` (or RequireDualStack); Services get both v4 + v6 IPs.

    
    **App readiness**: legacy apps may bind only to `0.0.0.0` (v4) — they don't accept v6 traffic. Audit + fix bind addresses to `[::]` or use dual binds. Tools: `netstat` / `ss` on running Pods.
    **Migration**: enable dual-stack first; verify v4 still works; gradually shift to v6-primary as apps support it; eventually drop v4 for closed environments.

## 4. how mesh + DNS + IPv6 interact

The three layers interact:
    
      - Mesh adds DNS load (sidecar resolves backends) — NodeLocal DNSCache critical.

      - Mesh + IPv6: ensure mesh control plane + sidecars support v6 explicitly. Istio + Linkerd both do; verify in deployment.

      - NodeLocal DNSCache must be configured for v6 query patterns when dual-stack.

    
    **Tuning playbook (for any cluster > 100 nodes)**:
    
      - Deploy NodeLocal DNSCache. Drop `ndots:1`. Verify CoreDNS load.

      - Pick + deploy mesh. Audit DNS query patterns post-mesh.

      - If IPv6 required: enable per layer; staged.

      - Hubble / Pixie / kube-burner profile cluster: latency, error rates, DNS hit ratio.

      - Iterate: tune CoreDNS replicas, mesh sidecar resources, IPv6 readiness.

## Before / After

**Before.** Pre-tuning: mesh adds latency, DNS bottlenecks, IPv6 deferred indefinitely. Cluster scale hits a wall around 200-300 nodes.

**After.** Tuned: mesh chosen by need (Linkerd simple, Istio for L7 features, Cilium for eBPF-native); NodeLocal DNSCache + ndots:1; dual-stack rolled per layer with app readiness audit. Cluster scales to 1000+ nodes cleanly.

*Three concerns; each has a known tuning answer; ignore at your scale-pain peril.*

## Analogy — the K-Highway junction

Express Lanes are the cluster's high-speed conveyors. Three concerns interlock. The **express-lane operator** (mesh) decides which lanes get TLS-sealed envelopes + retries + metrics. The **sign-system** (DNS) tells every vehicle where to exit; without local cached signs at every intersection, the central sign office is overwhelmed. The **address registry** (IPv6) lets the highway have many more lanes — staged across the system.
    Each concern has a known tuning. The Captain's job is to enable each at the right cluster scale.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Express-lane operator | Service mesh (Istio / Linkerd / Cilium / Kuma) |
| Sealed envelopes + retries | mTLS + automatic retries + observability |
| Sidecar courier next to vehicle | Sidecar mode (per-Pod proxy) |
| Per-floor courier | Ambient mode (per-node + per-namespace proxy) |
| Sign-system office (central) | CoreDNS Pods |
| Local cached signs | NodeLocal DNSCache (DaemonSet) |
| Ride-share routing tweaks | ndots:1 + autoPath |
| Wider address registry | IPv6 / dual-stack at every layer |

⚠️ *Analogy stops here:* A real express lane has visible pavement; mesh + DNS + IPv6 are policy + config + kernel state. Verify with synthetic queries + Hubble flow logs.

## ELI5 / ELI10

**ELI5.** Three things to tune for fast highways. Pick a courier service for sealed packages. Put a local sign-cache at every block so the central sign office isn't overwhelmed. Add longer license plates for more cars (IPv6).

**ELI10.** **Mesh**: Istio (rich, complex), Linkerd (simple, Rust, fast), Cilium SM (eBPF-native), Kuma (Envoy + multi-mesh). Sidecar or ambient. **DNS scale**: NodeLocal DNSCache (5× reduction) + ndots:1 + autoPath. **IPv6**: enable per layer (kubelet / apiserver / CNI / Service); audit app bind addresses; gradual migration.

## Real-world scenarios

- **Linkerd for simple mTLS.** A 30-engineer team needs mTLS + retries + metrics. Adopts Linkerd cluster-wide; ~5 MiB per Pod overhead; CLI annotates namespaces; no Rego-style complexity. mTLS automatic; per-Service metrics in Grafana.
- **NodeLocal DNSCache cut CoreDNS load 80%.** 500-node cluster; CoreDNS Pods at 90% CPU; queries 50K rps. Deployed NodeLocal DNSCache (DaemonSet) + dropped to ndots:1. Within 30 min: CoreDNS load 18%; P99 DNS latency 0.3ms; queries to CoreDNS Pods dropped to ~10K rps.
- **IPv6 readiness audit before migration.** A team auditing 200 services found 35 with hardcoded IPv4 binds. 3-month rolling fix; staged dual-stack rollout; gradual flip to v6-primary. Saved a major outage that would have hit during v4-deprecation deadline.
- **Istio ambient migration — sidecar overhead halved.** A 1000-Pod Istio sidecar deployment migrated to Istio ambient mode. Per-Pod overhead dropped from ~50 MiB to ~5 MiB; control plane simpler; same mTLS + AuthorizationPolicy. 6-week migration; namespace-by-namespace.

## Common misconceptions

- **Myth:** "Istio is the only mature mesh."
  **Truth:** Linkerd is CNCF Graduated + production-grade for years. Cilium Service Mesh is eBPF-native. Kuma is Envoy-based. Istio has the most features; not always the right tool.
- **Myth:** "NodeLocal DNSCache is optional."
  **Truth:** At any cluster > 100 nodes, it's a non-optional best practice. Without it, CoreDNS Pods saturate; DNS latency drives every cluster-internal call slower; cluster-wide cascades follow.
- **Myth:** "IPv6 isn't needed yet."
  **Truth:** Cloud providers + many enterprises have IPv6 mandates within 1-3 years. App readiness audits take months. Start dual-stack now; treat v6 as the foundation, not a deferred add-on.

## Recap

Three concerns: mesh (Istio / Linkerd / Cilium SM / Kuma; sidecar vs ambient); DNS at scale (NodeLocal DNSCache + ndots:1); IPv6 / dual-stack (per-layer enablement + app readiness). All three are non-optional past 100 nodes.

**Next — N5: NetworkPolicy at scale + egress + private + hybrid.** AdminNetworkPolicy + NetworkPolicy hierarchy; egress gateway; private clusters; hybrid (VPN + Direct Connect / ExpressRoute) connectivity.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
