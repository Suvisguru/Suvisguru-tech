# Lesson 26 — AdminNetworkPolicy & FQDN-Based Egress

> Course: Kubernetes — Common to all distributions
> Module 12 · Networking depth · Lesson 3 of 3
> Companion preview: `/preview-kubernetes-lesson-26.html`.

---

**🎯 If you remember nothing else:** Three policy tiers: **AdminNetworkPolicy** (admin, high priority, evaluated first), **NetworkPolicy** (team, namespace-scoped, additive), **BaselineAdminNetworkPolicy** (admin default, evaluated last). For egress to external services, **FQDN-based policies** (CNI extension; not yet core API) match by hostname not CIDR. `github.com` instead of "some IP block on the internet."

## 1. Why NetworkPolicy v1 wasn't enough

The original `NetworkPolicy` (covered in Lesson 17) is namespace-scoped and additive: each policy is an allow rule for the Pods it selects. If *any* NetworkPolicy applies to a Pod, the Pod is firewalled (default-deny, only the listed allows pass). Two important properties this *doesn't* have:
    
      - **No admin override.** A cluster admin can't write a policy that takes precedence over team policies. Every NetworkPolicy in a namespace has equal weight; they're all evaluated together.

      - **No deny rules.** Only allow. You can't say "block all egress to `1.2.3.4`" — you can only say "allow specific things." If a team forgets to write a policy, the namespace is wide open.

    
    The Gateway API style of layered ownership came to NetworkPolicy in K8s 1.30-1.32 with two new APIs: **AdminNetworkPolicy** (ANP, cluster-scoped, admin-owned, priority-ordered, supports allow/deny/pass) and **BaselineAdminNetworkPolicy** (BANP, cluster-scoped, admin-owned, exactly one per cluster, evaluated *last* as the default).

## 2. ANP → NetworkPolicy → BANP

For every packet, the CNI evaluates rules in this order:
    
      - **AdminNetworkPolicy** (highest priority numeric value first, sort within each ANP). Each rule has an action: `Allow`, `Deny`, or `Pass`. *Pass* is special — it means "stop evaluating ANP for this packet; let NetworkPolicy decide." Allow/Deny terminate evaluation.

      - **NetworkPolicy** (the original, namespace-scoped). Standard semantics: if a Pod is selected by any policy, default-deny applies; explicit allows let traffic through.

      - **BaselineAdminNetworkPolicy** (the cluster's default; one per cluster). Allow / Deny only (no Pass). Catches anything not handled above.

    
    The pattern this enables:
    
      - **ANP**: "no namespace can talk to the `kube-system` namespace except via the API server" (admin override; teams can't bypass).

      - **ANP Pass**: "for namespace X, defer to whatever the team's NetworkPolicy says" (admin opt-out for trusted teams).

      - **BANP**: "default deny all egress except to in-cluster Services" (cluster default; teams override per-namespace via NetworkPolicy or by passing through ANP).

## 3. When CIDR isn't expressive enough

NetworkPolicy v1 lets you allow egress to a CIDR (`10.0.0.0/8`) or a Service. It can't say "allow egress to `api.openai.com`." Why this matters:
    
      - External SaaS (OpenAI, Anthropic API, Stripe, GitHub) own large, dynamic IP ranges. Listing CIDRs is fragile.

      - Compliance often demands "list of allowed external destinations" by hostname, not by IP.

      - Egress filtering as exfiltration prevention needs FQDN matching (block `pastebin.com` regardless of IP).

    
    **FQDN-based policies** aren't yet in the core NetworkPolicy / ANP spec — but every modern CNI (Cilium, Calico Cloud, Tigera, NSX-T) exposes them via vendor extensions. Cilium's `CiliumNetworkPolicy` has `egress.toFQDNs`. Calico's `GlobalNetworkPolicy` has equivalent.
    How it works under the hood: the CNI hooks the Pod's DNS resolution (typically by intercepting DNS responses), records the IP it resolved a name to, and installs a short-lived per-IP allow rule. When the IP TTL expires, the rule expires too. Combined with eBPF-based enforcement, it's fast and accurate.
    [ deep dive — skip if new ]FQDN policies are intentionally vendor-specific because the implementation is non-trivial — DNS interception, IP cache management, and TTL handling. The K8s Network SIG has a working group on standardising it for ANP/BANP, expected to land in 1.36 or later. Until then, FQDN policies are CNI-specific YAML — your migration cost from one CNI to another includes rewriting these.

## 4. What a real cluster's policy stack looks like

A typical 2026 production cluster ships:
    
      - **One BANP**: "default deny all ingress and egress except DNS to kube-dns and traffic to kube-apiserver." Catches everything not explicitly allowed.

      - **A small ANP set**: protect `kube-system` (deny ingress except from controllers); deny egress to RFC1918 from internet-facing namespaces (defence in depth); allow Pods in `monitoring` namespace to scrape any Pod.

      - **Per-namespace NetworkPolicy**: app teams own their own ingress/egress allows. Most namespaces have a default-deny + one or two explicit allows.

      - **FQDN egress policies** (CNI-specific): allow-list of approved external SaaS endpoints per namespace. Updated as new external integrations are approved.

    
    This stack means: a developer can't accidentally bypass cluster policies by forgetting a NetworkPolicy. The BANP catches them. They also can't override admin-set deny rules — those are in ANP at high priority. They *can* add fine-grained allows within their namespace via standard NetworkPolicy.

## Before / After

**Before.** Pre-ANP: admin compliance rules baked into wiki pages. Teams forget a NetworkPolicy → namespace is wide open. No way to say "kube-system is admin-only" enforceably. Egress to external services controlled by IP allow lists that go stale weekly. Pastebin? Open by default until someone notices.

**After.** BANP at the bottom: default deny everywhere. ANP at the top: admin's non-negotiable rules. NetworkPolicy in the middle: app teams own their allows. FQDN policies: external services by name, not by ever-changing IP. Auditor asks "what stops X?" — show them the ANP. Done.

ANP + BANP closes the longest-standing gap in K8s policy. The single-tier model lasted nearly a decade; the layered model is what production teams have always wanted.

## Analogy — the K-Town district

The Switchboard's policy wing has three desks, in order of authority. The **City Council desk** (AdminNetworkPolicy) issues binding ordinances — "no calls to City Hall except from registered businesses" — which override anything else and are enforced at the city gate. The **building manager desks** (NetworkPolicy) handle individual building rules — "callers from the press must use the lobby line." The **default city ordinance shelf** (BaselineAdminNetworkPolicy) sits at the bottom: "no calls to the city without a business reason." Building managers' rules can override the default ordinance for their tenants; the city council's ordinances cannot be overridden by anyone.Off to the side: a separate **destination registry** (FQDN policies) listing every approved out-of-city number by name — `github.com`, `api.openai.com` — so phone-by-name works even when the actual phone numbers (IP addresses) change. The registry is owned by the city; building managers request additions; council approves.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| City Council ordinance | `AdminNetworkPolicy` |
| Building manager rule | `NetworkPolicy` (v1) |
| Default city ordinance shelf | `BaselineAdminNetworkPolicy` |
| "Pass — defer to building manager" | ANP `Pass` action |
| "Forbidden by city, no exceptions" | ANP `Deny` at high priority |
| Destination registry by name | FQDN egress policies (CNI extension) |
| Out-of-city numbers that change weekly | External SaaS IP ranges |

⚠️ *Analogy stops here:* The analogy stops here: real ANP/BANP enforcement happens in the kernel via eBPF or iptables, not at "the city gate." And FQDN policies depend on intercepting DNS, which works well 95% of the time but can be evaded by Pods that hard-code IPs.

## ELI5 / ELI10

**ELI5.** Three sets of rules. The grown-up's rules go first (admin). The kid's rules go in the middle (team). The house's default rule ("don't talk to strangers") goes last. Plus a separate list of friends' names you're allowed to call (FQDN).

**ELI10.** **AdminNetworkPolicy (ANP)**: cluster-scoped, admin-owned, priority-ordered, with Allow/Deny/Pass actions. Evaluated first. **NetworkPolicy (v1)**: namespace-scoped, app-team-owned, additive allows. Evaluated next. **BaselineAdminNetworkPolicy (BANP)**: one per cluster, admin-owned default. Evaluated last. **FQDN-based policies**: CNI-vendor extensions (Cilium, Calico, etc.) for matching egress by hostname. Combined: layered policy with admin override, team self-service, and hostname-aware egress.

## Real-world scenarios

- **A bank with strict compliance requirements.** ANP: "no namespace except `infra` can egress to RFC1918." "All ingress to `finance` namespace must come from `app-frontend` or be denied." BANP: default deny ingress + egress. Per-namespace NP: app-team allows. FQDN policies: 14 approved external SaaS, allowed only from specific namespaces. Auditor calls these "the cleanest policy stack we've seen."
- **A SaaS protecting against accidental data exfiltration.** BANP default-denies egress everywhere except DNS, kube-apiserver, kube-dns. Each namespace owns an FQDN allow list (Cilium FQDN policies). New external service = a YAML PR. Pastebin / Discord / random-IP egress impossible. Catches a contractor's misbehaving build script before it can phone home.
- **A platform team running multi-tenant clusters.** Each tenant gets a namespace with admin-installed ANP "this namespace can't talk to other tenants' namespaces." Tenants own their NP for intra-namespace allows. ANP `Pass` for known infra namespaces (monitoring, logging) so tenant policies don't accidentally block scraping.
- **A team using ANP <code>Pass</code> for delegated trust.** Their `security-staging` namespace runs experimental Pods. ANP at priority 50 says "`Pass` for security-staging" — meaning: don't apply admin rules; let the team's own NetworkPolicy decide. Other namespaces get admin-enforced denies. Used for security testing without disabling protection cluster-wide.

## Common misconceptions

- **Myth:** ANP replaces NetworkPolicy.
  **Truth:** ANP supplements NetworkPolicy. The three-tier model is intentional: admins set hard rules at the top, teams own additive allows in the middle, defaults catch the rest. Most clusters use all three.
- **Myth:** FQDN policies are part of NetworkPolicy v1.
  **Truth:** They're not. NP v1 only knows CIDR + Service references. FQDN matching is a CNI vendor extension (Cilium's `CiliumNetworkPolicy.egress.toFQDNs`; Calico's equivalent). The K8s Network SIG is working on standardising it for ANP.
- **Myth:** ANP `Pass` is the same as `Allow`.
  **Truth:** Different. `Allow` ends evaluation — packet flows. `Pass` means "skip ANP for this packet, let NetworkPolicy decide." Useful for delegating to teams selectively without admin denies blocking everything.

## Recap

ANP (admin, top priority) → NetworkPolicy (team, additive) → BANP (admin default, bottom). Three tiers, layered ownership. FQDN policies (CNI extensions) match egress by hostname. The ten-year gap in K8s network policy is closed.

**Next — Lesson 27: RBAC & Authentication.** Module 13 begins. RBAC, structured auth config, OIDC integration. The new K-Town district: Watchtower.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
