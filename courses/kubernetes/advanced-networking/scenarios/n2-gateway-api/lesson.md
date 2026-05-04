# K-ADV-NET N2 — N2 · Gateway API at Fleet Scale

> Course: K-ADV-NET (advanced specialization)
> Module N2 · Gateway API
> Companion preview: `/preview-kubernetes-adv-net-lesson-02.html`.

---

**🎯 If you remember nothing else:** **Gateway API: GatewayClass (infra) + Gateway (shared listener bank) + HTTPRoute (per-team). ReferenceGrant for cross-namespace; BackendTLSPolicy for re-encrypt. Replaces Ingress + per-controller annotations.**

## 1. GatewayClass · Gateway · HTTPRoute

**GatewayClass**: cluster-scoped CRD naming the controller (e.g., `envoy-gateway`) + parameters. Set up by infra team once. Defines who is implementing Gateways in this cluster.
    **Gateway**: namespaced; lists listeners (port + protocol + hostname + TLS cert + allowed routes); references a GatewayClass. Typically owned by infra / platform team and shared across multiple app teams.
    **HTTPRoute / GRPCRoute / TCPRoute / TLSRoute / UDPRoute**: namespaced; attaches to one or more Gateways via `parentRefs`; declares match (host + path + headers + method) + filters (header rewrite, redirect, mirror) + backendRefs (Service / Pod). Owned by app teams.
    Role separation is the win: infra controls cert + hostname + TLS termination once; app teams ship routes without touching infra.

## 2. Routes in one namespace pointing at backends in another

By default, an HTTPRoute can only reference backendRefs in the *same namespace*. To route across namespaces: **ReferenceGrant** in the *backend's* namespace explicitly grants the source namespace permission to reference the backend.
    Pattern: Gateway lives in `infra` namespace; HTTPRoutes in `team-X` namespaces; backends often in `team-X` namespace too (no grant needed). Cross-team backends (e.g., a shared identity Service) require ReferenceGrant in the backend namespace.
    This prevents an attacker who controls one namespace from creating routes that hijack traffic to another namespace's backends — without explicit cross-namespace consent, the route fails to attach.

## 3. re-encrypt to backend + header/URL rewrites

**BackendTLSPolicy** (alpha → beta in newer K8s): tells Gateway to re-encrypt traffic to backends. Default is plain HTTP from Gateway to backend; BackendTLSPolicy switches to HTTPS with caBundle reference. Useful for Pods running TLS terminators or for compliance-required end-to-end encryption.
    **HTTPRouteFilter** kinds: *RequestHeaderModifier* (add/set/remove header); *ResponseHeaderModifier*; *RequestRedirect* (HTTP → HTTPS, /old → /new); *URLRewrite* (path strip / replace); *RequestMirror* (mirror to another Service for shadow testing); *ExtensionRef* (controller-specific filters).
    Compared to Ingress's annotation-soup, filters are typed CRDs — versioned, schema-validated, controller-portable.

## 4. fleet-wide ingress + the path from Ingress

**Multi-cluster Gateway**: Gateway-api-extensions handle multi-cluster patterns. Cilium ClusterMesh + Gateway, Istio multi-cluster Gateway, GKE Multi-cluster Gateway. Single hostname routes to backends in multiple clusters per region; failover automatic.
    **Ingress migration**: per controller, migrate gradually. (1) Pick GatewayClass (often the same controller behind a different CRD). (2) Create Gateway with the same listeners as the existing Ingress. (3) Per Ingress, create equivalent HTTPRoute; switch traffic. (4) Decommission Ingress. Tools: **ingress2gateway** CLI converts manifests automatically.
    **Controller choice**: *Envoy Gateway* (cleanest implementation, CNCF), *Istio* (full mesh + Gateway), *Cilium Gateway* (eBPF-native, integrates with Cilium NetPol), *NGINX Gateway Fabric* (familiar to NGINX teams), *cloud-native* (GKE Gateway Controller, AKS Application Gateway Controller, AWS Gateway API Controller). All implement the same spec.

## Before / After

**Before.** Pre-Gateway API: Ingress + per-controller annotations (NGINX-style, ALB-style, GCE-style). Annotation soup; portability gaps; one controller bug affected every team's routes; cross-namespace Service reference impossible.

**After.** Gateway API: typed CRDs; role separation; ReferenceGrant explicit cross-namespace; BackendTLSPolicy + HTTPRouteFilter as schema-validated objects; portable across controllers (Envoy Gateway, Istio, Cilium, NGINX, cloud-native). Annotation chaos replaced by typed config.

*Three roles, three CRDs, one routing chain. Replaces a decade of Ingress annotation drift.*

## Analogy — the K-Highway junction

The Main Intersection in K-Highway has three layers of authority. The **city operator** (GatewayClass) builds + maintains the intersection itself; chooses asphalt + signals + traffic-engineering vendor. The **traffic-control engineer** (Gateway) decides which lanes are open at this intersection — the cert, the hostname, the protocol. Each **destination dispatcher** (HTTPRoute) says "vehicles for my building, take exit 4 + reroute via path X."
    The three roles never overlap. The city operator doesn't care about your destination. The destination dispatcher doesn't change the asphalt. When you need to send vehicles across district lines (cross-namespace), the destination district issues a permit slip (ReferenceGrant) saying "yes, deliveries from your district may end here."

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| City operator | GatewayClass (controller infrastructure) |
| Traffic-control engineer | Gateway (listener bank, cert, hostname) |
| Destination dispatcher | HTTPRoute / GRPCRoute / TLSRoute / TCPRoute |
| Cross-district permit slip | ReferenceGrant (cross-namespace consent) |
| Vehicle armoring at exit | BackendTLSPolicy (re-encrypt to backend) |
| Lane filters | HTTPRouteFilter (header / URL rewrite / redirect / mirror) |
| Fleet of intersections | Multi-cluster Gateway |
| Old single-board annotations | Ingress + per-controller annotations (legacy) |

⚠️ *Analogy stops here:* A real intersection has fixed pavement; Gateway API is virtual — controllers can have bugs, conformance gaps, version skew. Always test with the conformance suite.

## ELI5 / ELI10

**ELI5.** Three different people manage one intersection. The city builder makes the road. The traffic engineer decides which lights are on. Each store puts up its own "go this way for my deliveries" sign. Each does their job; nobody steps on the others.

**ELI10.** **GatewayClass** = controller (Envoy Gateway / Istio / Cilium / NGINX / cloud-native). **Gateway** = cluster/team listener bank (port + protocol + cert + hostnames + allowed routes). **HTTPRoute** (and GRPCRoute / TCPRoute / TLSRoute / UDPRoute) = per-team match + filter + backend ref. **ReferenceGrant** = cross-namespace consent. **BackendTLSPolicy** = re-encrypt to backend. **HTTPRouteFilter** = typed header / URL / redirect / mirror.

## Real-world scenarios

- **Multi-team cluster — single Gateway, many HTTPRoutes.** A 60-engineer org deploys one Gateway in `infra` namespace handling api.example.com. Each app team's namespace has HTTPRoutes attaching to that Gateway with their hostname / path. Infra owns cert; teams ship routes. Zero coordination required for route changes.
- **ingress2gateway migration.** A team had 80 Ingress objects across 30 namespaces. Used `ingress2gateway` CLI to convert; reviewed deltas; deployed Gateway + HTTPRoutes alongside Ingress; switched DNS / traffic; decommissioned Ingress over 4 weeks. Migration low-drama.
- **Multi-cluster Gateway via Cilium ClusterMesh.** A team needs api.example.com to fail over from us-east-1 cluster to eu-west-1 cluster automatically. Cilium ClusterMesh + Gateway API: HTTPRoute backendRef points at a multi-cluster Service; Cilium routes per-region with health-aware failover. Same DNS; transparent failover.
- **Outage — annotation typo took down 3 teams.** On the legacy Ingress, a single typo in an NGINX annotation broke routing cluster-wide. Postmortem: schema-typed CRDs (Gateway API) prevent silent annotation typos. Migration to Gateway API now scheduled.

## Common misconceptions

- **Myth:** "Gateway API is just a renamed Ingress."
  **Truth:** Gateway API has role separation (Gateway + Route owners differ), typed CRDs (no annotations), explicit cross-namespace consent (ReferenceGrant), portable controllers, and broader L4 protocol support (TCPRoute / TLSRoute / UDPRoute). Functionally + architecturally distinct.
- **Myth:** "You need to migrate everything before using Gateway API."
  **Truth:** Gateway API + Ingress coexist on the same cluster + same controller. Migrate per-route or per-team gradually; the controller serves both during the transition.
- **Myth:** "Gateway API is too complex for small teams."
  **Truth:** The three CRDs are simpler than Ingress + 30 controller-specific annotations once you have more than one route + one cert. For a single-route demo, Ingress is shorter; for production, Gateway API is clearer.

## Recap

Gateway API: three roles, three CRDs, typed config. ReferenceGrant for cross-namespace; BackendTLSPolicy for re-encrypt; HTTPRouteFilters for rewrites. Migration from Ingress is per-route + gradual.

**Next — N3: Multi-cluster networking.** Submariner, Skupper, Cilium ClusterMesh, Istio multi-cluster — pick by trust + perf needs; cross-cloud + on-prem patterns.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
