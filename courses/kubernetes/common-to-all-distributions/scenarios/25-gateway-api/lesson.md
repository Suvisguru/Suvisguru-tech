# Lesson 25 — Gateway API · Roles, Listeners, Routes, and the Ingress Sunset

> Course: Kubernetes — Common to all distributions
> Module 12 · Networking depth · Lesson 2 of 3
> Companion preview: `/preview-kubernetes-lesson-25.html`.

---

**🎯 If you remember nothing else:** Gateway API splits Ingress into three roles: **GatewayClass** (cluster recipe — infra team), **Gateway** (listener bank — platform team), **HTTPRoute / GRPCRoute / TCPRoute / TLSRoute** (traffic clips — app teams). The same logical setup as Ingress, but with cleaner ownership boundaries and far more expressiveness. Ingress NGINX is sunsetting in 2026 — start the migration now.

## 1. Why Ingress wasn't enough

The Ingress API (in beta from 2015, finally stable in 2020) gave us "expose HTTP routes from outside the cluster." It worked. It also accumulated every limitation of a v1 API: no traffic splitting, no header manipulation, no separate concerns for infra vs apps, no good story for non-HTTP traffic, vendor-specific behavior locked behind *annotations*. Annotations on an Ingress object became the de-facto extension mechanism — and they're untyped strings that vary per controller.
    The **Gateway API** (Kubernetes SIG-Network, work started in 2019) is the redesign. Not just "Ingress v2" — a structurally different model with three explicit roles and CRDs for each:
    
      - **Infrastructure provider** — defines a `GatewayClass`: "this controller (Envoy Gateway, Cilium Gateway, NGINX Gateway Fabric, Istio gateways) handles Gateways of this class."

      - **Cluster operator** — creates `Gateway` objects: "give me a listener on :443 with these TLS certs, accepting routes from these namespaces."

      - **Application developer** — creates `HTTPRoute` / `GRPCRoute` / `TCPRoute` / `TLSRoute` objects: "this hostname/path → my Service."

    
    The big change for app teams: you don't describe the listener anymore. The platform team owns the Gateway; you just attach a Route to it. The old "every team writes their own Ingress with annotations" pattern is gone.

## 2. GatewayClass, Gateway, Route

🏛️
        GatewayClass
        recipe · cluster-scoped
        Cluster-scoped: "controller X handles Gateways of class Y." Ships with the Gateway controller; cluster operators reference it. Like StorageClass.
        Owned by: infrastructure team / Gateway controller install
      
      
        🚪
        Gateway
        listener bank · namespace-scoped
        A specific gateway with one or more listeners. Each listener is (port, protocol, optionally hostname, TLS config). Specifies which namespaces' Routes can attach via `allowedRoutes`.
        Owned by: platform team
      
      
        🛣️
        HTTPRoute (and friends)
        traffic clip · namespace-scoped
        "Match these hostnames + paths/headers, route to these backends with these weights." Far richer than Ingress: header matching, traffic splitting, request rewriting, retries, timeouts. GRPCRoute, TCPRoute, TLSRoute, UDPRoute exist for non-HTTP.
        Owned by: app teams
      
    
    A Route attaches to a Gateway via `parentRefs`. The Gateway's `allowedRoutes` field gates which namespaces / Route kinds can attach. This is the explicit cross-tenancy model Ingress never had.

## 3. Out of annotations, into a typed schema

Most Ingress controllers had de-facto annotations for traffic splitting (canary), header rewriting, retries. Each controller's syntax differed; cross-controller migration was painful. Gateway API moves all of this into the typed Route schema:
    
      - **Traffic splitting:** a single Route can backendRef two Services with weights (90/10 for canary).

      - **Header / path rewriting:** filters on a route can rewrite request URLs and headers in-flight.

      - **Request mirroring:** send a copy of every request to a debug Service while the real one is unaffected.

      - **Retries / timeouts:** declarative per-route, no controller-specific annotations.

      - **Method matching:** match by HTTP method (GET/POST), not just path/host.

      - **RBAC-friendly:** apps can have full control of their Routes without ops worrying about port conflicts or TLS.

    
    Gateway API also has a formal **conformance test suite**. Controllers advertise which features they support. Switching from Envoy Gateway to NGINX Gateway Fabric means re-running conformance and fixing any unsupported features — not rewriting hundreds of annotations.

## 4. What's actually happening in 2026

The community-maintained `kubernetes/ingress-nginx` project (the de-facto Ingress controller for years) announced in March 2025 it would stop accepting new features and would EOL security patches by end of 2026. Reasons cited: limited contributor capacity, fundamental architectural debt (NGINX as a templated config), and the existence of a clearer successor (NGINX Gateway Fabric, F5's officially-supported Gateway-API-conformant controller).
    The migration story:
    
      - **Tool: `InGate`** — Ingress NGINX's own translator that converts existing Ingress YAML to Gateway API objects. Not perfect but covers ~80% of typical setups.

      - **Strategy:** install a Gateway-API-conformant controller alongside Ingress NGINX (Envoy Gateway, NGINX Gateway Fabric, Cilium Gateway, Istio); migrate Routes incrementally with DNS cut-over per app; decommission Ingress NGINX last.

      - **Don't panic deadline:** Ingress objects still work in K8s — just unmaintained Ingress controllers won't receive CVEs. You have through 2026 to migrate at sane pace.

    
    [ deep dive — skip if new ]The political subtext: Ingress NGINX was always community-maintained without F5's direct backing. NGINX Gateway Fabric is F5-supported and Gateway-API-native — it's the supported successor. Other vendors saw the gap and moved their Gateway implementations earlier (Envoy Gateway, Cilium Gateway, Istio Gateway). The Gateway API itself is vendor-neutral; the choice of controller is yours. Most new clusters in 2026 are choosing Envoy Gateway or Cilium Gateway.

## Before / After

**Before.** Old way: every team writes an `Ingress` with the controller's annotations (`nginx.ingress.kubernetes.io/...`) for canary splits, rewrites, retries. Cross-controller migration = rewrite every Ingress. Tenancy via namespace + RBAC luck. Listener config baked into Ingress objects so app teams accidentally control TLS.

**After.** Gateway API: platform team owns Gateway (listeners, TLS, allowedRoutes). App teams own HTTPRoutes with first-class fields for splits/rewrites/retries. Switching controllers = rerun conformance. Tenancy explicit via `allowedRoutes`. Same listener serves many apps without a single shared annotation soup.

Gateway API was the most-discussed K8s API of 2024-25 for good reason. It's the cleanest single API redesign in the ecosystem's history.

## Analogy — the K-Town district

Switchboard, customer counter side. The old setup had every business carrying a single big poster with their phone number, address, who could call them, what hours they answered, and the rules for caller ID — all stuck on one wall, written by anyone, contradicting each other. *Ingress, with its annotations, on a wall.*The new layout has three separate workstations. The infra office hangs **operating-license posters** (GatewayClass): "the city contracts so-and-so for this kind of switchboard." The platform team operates the **main switchboard machine** (Gateway): a bank of physical jacks at specific addresses (listeners), each jack with its own line and posted rules about who can plug in. App teams clip their own **route slips** (HTTPRoute) onto a board: "calls to this number, from this exchange, route to my building, here are the rules for split-percentage and retry." Three roles, three artefacts, no overlap.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Operating-license poster | `GatewayClass` |
| The switchboard machine and its bank of jacks | `Gateway` with listeners (port, protocol, hostname, TLS) |
| Posted rules for which exchanges may plug into a jack | `allowedRoutes` on a listener |
| Clipped route slip on the board | `HTTPRoute` (and GRPCRoute, TCPRoute, TLSRoute, UDPRoute) |
| Split-percentage rules on a slip | Backend weights for canary / blue-green |
| In-flight call edits (rewrite extension) | Filters: URLRewrite, HeaderModifier |
| The annotation soup on the old single poster | Ingress + controller-specific annotations |
| "This switchboard contractor is shutting down" notice | Ingress NGINX EOL end of 2026 |

⚠️ *Analogy stops here:* The analogy stops here: real Gateway implementations are programs (Envoy Gateway, Cilium Gateway), not switchboards. And the "three roles" are an organisational ideal — small teams may collapse them, and that's fine; the API just makes the boundaries possible.

## ELI5 / ELI10

**ELI5.** Old way: one big sign for each store, with everything on it, half of it in code only the sign-maker understood. New way: a city sign for the road type, a building manager for the front-desk hours, and each store keeps a small slip on a shared board for "if someone asks for me, send them in."

**ELI10.** The Gateway API replaces the Ingress API. Three CRDs split the concerns: GatewayClass (cluster-level recipe; infra team), Gateway (listener bank; platform team), HTTPRoute / GRPCRoute / TCPRoute / TLSRoute (traffic rules; app teams). Routes attach to Gateways via `parentRefs`; Gateways gate cross-namespace attachment via `allowedRoutes`. First-class support for traffic splitting, header rewriting, mirroring, retries, timeouts — all the things that used to be controller-specific annotations on Ingress. Ingress NGINX is EOL end of 2026; the upgrade path is Gateway API + Envoy Gateway / Cilium Gateway / NGINX Gateway Fabric.

## Real-world scenarios

- **A SaaS replacing 47 Ingress objects with Gateway API.** One Gateway per cluster (managed by platform team), Routes per app team. Started with the InGate translator for the bulk migration; hand-fixed the 12 with custom annotations. Total migration: 6 weeks, including testing. End state: app teams own their HTTPRoutes, no platform-team approval needed for new routes.
- **A bank using Cilium Gateway.** Cilium provides both CNI and Gateway in the same DaemonSet. Single eBPF-based data plane for cluster-internal traffic and ingress. Hubble shows per-flow visibility from external request through Routes to backend Pods. Operations team has one fewer thing to deploy.
- **A startup running Envoy Gateway for richer traffic shaping.** Used HTTPRoute weighted backends for canary deploys: 90% to `v1`, 10% to `v2`. Increment to 50/50, then 0/100 over a week. Pushed via GitOps; no controller annotations. Same flow gets metrics/tracing in Envoy admin endpoint.
- **A team that mirrors prod traffic to staging.** HTTPRoute filter `RequestMirror` sends a copy of every prod request to the staging Service. Staging gets real prod traffic shape without affecting prod responses. Used to validate the next release before promoting it.

## Common misconceptions

- **Myth:** Gateway API is just Ingress with new YAML.
  **Truth:** It's a structural redesign with explicit role separation, first-class non-HTTP routes, conformance testing, and typed traffic-shaping fields. Migrating means reorganising who owns what, not just rewriting Ingress.
- **Myth:** You have to migrate to Gateway API before end of 2026.
  **Truth:** Ingress objects still work — what's EOL is the *kubernetes/ingress-nginx* controller specifically. Other Ingress controllers (NGINX Inc, Traefik, HAProxy, etc.) keep working. But the entire ecosystem is moving to Gateway API; do the migration on your terms before it becomes urgent.
- **Myth:** Gateway API can't do everything Ingress NGINX did.
  **Truth:** Conformance varies by controller. Most popular Gateway controllers cover the standard feature set; vendor-specific extensions (Lua scripts, ModSecurity rules) need vendor-specific extensions. Check your specific Gateway controller's feature matrix.

## Recap

Three roles, three CRDs: GatewayClass (cluster recipe), Gateway (listener bank), HTTPRoute/etc (app-team traffic clips). Cleaner ownership, first-class traffic shaping, conformance testing, non-HTTP support. Ingress NGINX EOL'd end of 2026 — start the migration.

**Next — Lesson 26: AdminNetworkPolicy & FQDN policies.** NetworkPolicy v1 was app-team-controlled and additive-only — there was no "admin override." The new `AdminNetworkPolicy` + `BaselineAdminNetworkPolicy` APIs give cluster admins enforceable network rules, plus FQDN-based policies for egress to external services. Switchboard, security wing.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
