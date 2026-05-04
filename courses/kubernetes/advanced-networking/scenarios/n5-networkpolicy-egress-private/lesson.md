# K-ADV-NET N5 — N5 · NetworkPolicy + Egress + Private + Hybrid

> Course: K-ADV-NET (advanced specialization)
> Module N5 · NetworkPolicy + Egress + Private
> Companion preview: `/preview-kubernetes-adv-net-lesson-05.html`.

---

**🎯 If you remember nothing else:** **Default-deny ingress + egress at namespace; AdminNetworkPolicy for org-wide rules; egress gateway for audit trail; private cluster for apiserver isolation; hybrid VPN/DX for on-prem.**

## 1. AdminNetworkPolicy + NetworkPolicy + Baseline

K8s 1.30+ ships **AdminNetworkPolicy (ANP)** + **BaselineAdminNetworkPolicy (BANP)** as cluster-scoped CRDs alongside namespaced **NetworkPolicy (NP)**:
    
      - **AdminNetworkPolicy**: org-wide rules with explicit Pass / Allow / Deny + numeric priority. Set by platform team. Examples: "deny all egress to RFC-1918 from prod namespace," "allow all from observability namespace."

      - **NetworkPolicy**: namespaced; team-owned; default-deny + explicit allow. Cannot override AdminNetworkPolicy Deny rules.

      - **BaselineAdminNetworkPolicy**: cluster-scoped default rules below NP. Examples: "by default allow DNS to kube-system" so app teams don't need to declare it.

    
    Precedence: ANP > NP > BANP. The hierarchy lets platform enforce non-negotiable rules; teams refine within bounds.

## 2. The cluster's posture is no traffic by default

**Default-deny**: in every namespace, ship a base NetworkPolicy denying all ingress + egress. Then add explicit allow per consumer / per destination. Patterns:
    
      - **Ingress allow**: `podSelector: {app: api}; ingress: [{from: [{namespaceSelector: {team: web}}]}]` — only web team's namespace may call api Pods.

      - **Egress allow**: `egress: [{to: [{namespaceSelector: {kube-system: true}}], ports: [{port: 53}]}]` — DNS only.

      - **FQDN egress** (Cilium / Calico extensions): `toFQDNs: ["api.stripe.com"]` — egress to specific external services without IP enumeration.

    
    At scale, default-deny is unmaintainable as bespoke per-team work — generate from service catalog metadata or use mesh AuthorizationPolicy as L7 complement.

## 3. All cluster egress through one path; auditable

**Egress gateway**: a node group + Pods designated to handle *all* outbound cluster traffic. Patterns:
    
      - **Cilium egress gateway**: per-namespace / per-Pod-selector route to a designated gateway node; outbound traffic SNAT'd through that node's IP.

      - **Istio egress gateway**: mesh routes outbound through an egress proxy; L7 inspection + TLS origination.

      - **Cloud-native**: NAT gateway + IP allowlist per workload (rate limit / log).

    
    Wins: *fixed source IP* for partner allowlisting; *full audit log* of egress destinations; *L7 inspection* if mesh-based; *blocklist for known-bad CIDRs*; *compliance evidence*.
    Gotcha: gateway becomes single point of egress congestion; deploy redundant + autoscale.

## 4. apiserver isolation + on-prem connectivity

**Private clusters** (cloud terms vary):
    
      - *EKS*: `endpointPrivateAccess: true` + `endpointPublicAccess: false`. Access via VPN / DX / SSM / bastion.

      - *GKE*: private cluster + master authorized networks; Private Service Connect for apiserver.

      - *AKS*: private cluster + Private Endpoint for apiserver; Azure Bastion access.

    
    **Hybrid connectivity**:
    
      - **AWS**: Direct Connect (DX) + DX Gateway + Transit Gateway. Bandwidth dedicated; predictable latency.

      - **Azure**: ExpressRoute + ER Gateway + vWAN. Similar shape.

      - **GCP**: Cloud Interconnect + Cloud Router. Per-region attachments.

      - **VPN**: site-to-site IPsec for lower-bandwidth or backup paths.

    
    Combine with private cluster + AdminNetworkPolicy: cluster apiserver only reachable via the corporate network; cluster egress goes through DX / ER + corporate firewalls.

## Before / After

**Before.** Pre-policy clusters had open egress + flat ingress. Compromised Pod → free outbound to anywhere; lateral movement across all Pods.

**After.** Modern: AdminNetworkPolicy (org-wide) > NetworkPolicy (team) + default-deny + egress gateway + private cluster + hybrid VPN/DX. Compromise stops at the namespace boundary; egress to known destinations only.

*Default-deny everywhere; explicit allow at scale via service catalog + AdminNetworkPolicy hierarchy.*

## Analogy — the K-Highway junction

The Customs + Tollbooth marks the cluster's borders. A **federal customs office** (AdminNetworkPolicy) sets non-negotiable rules — no traffic to RFC-1918 from prod, no traffic from sandbox to prod ever. Each **team's tollbooth** (NetworkPolicy) refines within those rules — "my namespace accepts ingress from web; egress to api.stripe.com."
    Outbound traffic from the city flows through one **customs gate** (egress gateway) — every export logged + checked against the export ledger. The city's diplomatic gate (apiserver) is private — only reachable from the corporate diplomatic network (DX / ExpressRoute / VPN).

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Federal customs office | AdminNetworkPolicy (cluster-scoped) |
| Team tollbooth | NetworkPolicy (namespaced) |
| Standing default rules | BaselineAdminNetworkPolicy |
| Customs gate (export logged) | Egress gateway (Cilium / Istio / cloud NAT) |
| Allow-list of partner ports | FQDN egress / partner allowlist |
| Diplomatic gate | Private apiserver (PSC / Private Endpoint) |
| Diplomatic network connection | Direct Connect / ExpressRoute / Cloud Interconnect |
| Backup diplomatic line | Site-to-site VPN |

⚠️ *Analogy stops here:* A real customs office has paper records; cluster egress logs flow through SIEM; verify with synthetic egress probes.

## ELI5 / ELI10

**ELI5.** Three layers of border control. Federal rules nobody overrides. Team rules within those. One gate where all exports go through with logging. The leadership office is private — only reachable from headquarters.

**ELI10.** **AdminNetworkPolicy** > **NetworkPolicy** > **BaselineAdminNetworkPolicy** precedence. Default-deny + explicit allow. **Egress gateway** (Cilium / Istio / cloud-NAT) for fixed source IP + audit. **Private cluster** apiserver (EKS endpointPrivateAccess / GKE PSC / AKS Private Endpoint). **Hybrid** via DX / ExpressRoute / Cloud Interconnect / VPN.

## Real-world scenarios

- **Org-wide ANP with team NP refinement.** A 200-engineer org sets cluster-wide ANP: "deny ingress from sandbox-* to prod-*; deny egress to RFC-1918 from prod-*." Team NPs refine within this; sandbox can't accidentally reach prod even with permissive team NP.
- **Cilium egress gateway for partner allowlist.** Stripe required allowlisting source IPs. Cilium egress gateway routed all `app=billing` Pod egress through gateway nodes with elastic IPs. Stripe allowlist receives single IP set; rotation handled at gateway.
- **Private GKE + Cloud Interconnect.** A regulated team's GKE cluster has private apiserver + private nodes. Cloud Interconnect between corporate DC + GCP VPC; cluster reachable only from corporate network. Public Internet egress via egress gateway with allowlisted destinations.
- **Outage — egress gateway single point.** Egress gateway with single Pod replicas; OOM during traffic spike; cluster lost outbound for 4 minutes. Postmortem: HPA on gateway + minimum 3 replicas + node anti-affinity. Updated runbook.

## Common misconceptions

- **Myth:** "Default-deny is too restrictive for development."
  **Truth:** Dev clusters benefit too — finds missing allow rules early before production. Train developer instinct via dev-cluster default-deny; prod is the same shape.
- **Myth:** "AdminNetworkPolicy replaces NetworkPolicy."
  **Truth:** They're complementary. ANP for org-wide non-negotiable rules; NP for team-scoped allow rules within ANP bounds; BANP for defaults below NP. Three-tier hierarchy.
- **Myth:** "Private cluster eliminates need for NetworkPolicy."
  **Truth:** Private apiserver protects the control plane; NetworkPolicy protects Pod-to-Pod. Both required; private apiserver doesn't prevent lateral movement inside the cluster.

## Recap

Three-tier NetPol hierarchy (ANP > NP > BANP) + default-deny + egress gateway + private cluster + hybrid connectivity. Lateral movement contained at namespace; egress audited; apiserver isolated; on-prem connected.

**Next — N6: Packet tracing + performance tuning.** Hubble + Pixie + Tetragon + tcpdump + kubectl-trace + kube-burner. Common findings: MTU mismatch, conntrack saturation, kernel scheduling.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
