# Lesson 17 — Services & Networking · ClusterIP, NodePort, LoadBalancer, Ingress, NetworkPolicy

> Course: Kubernetes — Common to all distributions
> Module 5 · Networking 101 · Lesson 1 of 1
> Companion preview: `/preview-kubernetes-lesson-17.html`.

---

**🎯 If you remember nothing else:** Pods come and go; Services give them stable names. Four flavours of Service plus Ingress for HTTP plus NetworkPolicy for who-can-talk-to-whom.

## Before / After

**Before.** App-to-app via hardcoded Pod IPs. Restart breaks everything. No traffic policy. External access via SSH tunnels and prayer. Adding a new exposed service means an LB ticket to the cloud team.

**After.** Services give every workload a stable name. ClusterIP for internal, Ingress for HTTP, LoadBalancer for L4 public. NetworkPolicy enforces who-talks-to-whom. New endpoints are PRs, not tickets.

Service / Ingress / NetworkPolicy is the trinity of K8s networking. Get the abstractions right and the network mostly disappears as a concern.

## Analogy — the K-Town district

The K-Town Switchboard is the city's telephone exchange. Buildings (Pods) move and renumber constantly; the Switchboard maintains stable phone lines (Services) that always reach the right building today. Internal calls go through the directory (ClusterIP); external calls reach a public number (LoadBalancer) or the city's main turnstile (Ingress). Traffic rules (NetworkPolicy) decide who's allowed to call whom.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Phone line that always reaches the building | Service (any type) |
| Internal directory | ClusterIP |
| Phone booth on every block | NodePort |
| Dispatch operator with a public number | LoadBalancer |
| Phone-book alias to an outside line | ExternalName |
| City's main entrance turnstile (HTTP routing) | Ingress / Gateway API |
| Traffic rules: who may call whom | NetworkPolicy |
| DNS lookup to find the line | kube-dns / CoreDNS resolving service-name.namespace.svc |

⚠️ *Analogy stops here:* Real Service IPs are virtual — kube-proxy or eBPF translates them to backend Pod IPs at the kernel level. The 'phone line' metaphor undersells how many translations happen per packet, and where they happen (every node, in iptables/IPVS/eBPF).

## ELI5 / ELI10

**ELI5.** Buildings move all the time. The phone numbers stay the same because the Switchboard knows which building has which phone today. Inside calls use a directory; outside calls use the main number.

**ELI10.** Pods get fresh IPs on every restart. Services give a group of Pods a stable name + virtual IP. Four types: ClusterIP (internal), NodePort (every node port), LoadBalancer (cloud LB), ExternalName (DNS alias). Ingress / Gateway API adds L7 routing (host + path). NetworkPolicy is the firewall — default-allow until a Pod is selected by any policy, then default-deny except for explicit allows.

## Real-world scenarios

- **A SaaS exposing one HTTPS service per customer.** Each customer gets a unique Ingress with their domain (acme-corp.app.example.com). All Ingresses share one cloud LB; nginx-ingress terminates TLS using cert-manager-issued certs. Adding a customer = one Ingress YAML + DNS record. Zero per-customer infrastructure cost.
- **A trading firm running internal-only services.** Every internal service is ClusterIP. NetworkPolicy enforces default-deny on every namespace. Specific allow rules let trading apps reach Postgres + Redis on specific ports; everything else is blocked, including the public internet. A compromised app can't even DNS-lookup an external host.
- **A logging platform on a DaemonSet.** Fluent Bit runs as a DaemonSet — one Pod per node. App Pods write logs to `localhost:24224`; the local Fluent Bit batches and ships them to a central log store. No Service needed for that internal communication — the agent is on the same node, reachable via `hostNetwork`. Cuts cross-node traffic for logs to zero.
- **A multi-tenant cluster with namespace isolation.** Each tenant gets a namespace. NetworkPolicy uses namespace selectors to enforce: tenant Pods can talk inside their own namespace + to `kube-system` (DNS) + to `monitoring` (Prometheus scraping) — and that's it. Cross-tenant traffic is blocked at the network layer.

## Common misconceptions

- **Myth:** Services have IPs, so the IP is the right thing to use in app config.
  **Truth:** Use the Service *name* (DNS), not the Service IP. The Service IP is stable but coupling to it ties you to one cluster's CIDR. Names work everywhere.
- **Myth:** A LoadBalancer Service is the only way to expose HTTP traffic.
  **Truth:** For HTTP, an Ingress controller (or Gateway API) is more flexible — host and path routing, TLS termination, one cloud LB shared across many services. LoadBalancer is for non-HTTP or single-service setups.
- **Myth:** NetworkPolicy is on by default; my Pods are isolated.
  **Truth:** By default every Pod can talk to every other Pod in the cluster. NetworkPolicy is opt-in — you write rules to restrict, otherwise everything is open. Default-deny is a posture you have to *configure*.

## Recap

Pods are ephemeral; Services give them stable names. Ingress lets the world reach them. NetworkPolicy controls who can talk to whom.

That's the Module 1-5 close — the foundations are set. Next up: Module 9 onward — storage, config, scheduling, and beyond.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
