# K-ADV-NET N7 — N7 · Capstone — Multi-Cluster Network

> Course: K-ADV-NET (advanced specialization)
> Module N7 · Capstone
> Companion preview: `/preview-kubernetes-adv-net-lesson-07.html`.

---

**🎯 If you remember nothing else:** **Multi-cloud network = ClusterMesh + Submariner + Skupper + Gateway API + ANP fleet-wide + Hubble everywhere + runbooks. Pick bridges per peer trust + perf; private + hybrid clusters; global LB / DNS for failover.**

## 1. 5 clusters, 4 clouds, 4 bridges

**Clusters**: EKS us-east-1 (primary); EKS eu-west-1 (DR); AKS eastus (regulated workloads); GKE europe-west1 (data residency); OCP on-prem (legacy + regulated). All Cilium where cloud allows; OCP runs OVN-K with bridge to Cilium pattern.
    **Bridges**: ClusterMesh between EKS pair (same CNI, same cloud); Submariner between cloud peers + OCP; Skupper to partner clusters. Routing via Gateway API per cluster + global LB (Route 53 / Azure Traffic Manager / GCP Global LB) for failover.
    **Connectivity**: AWS DX + Azure ExpressRoute + GCP Cloud Interconnect to corporate DC. Private clusters; apiserver via PSC / Private Endpoint. Egress gateways per cluster route outbound through audited paths.

## 2. ANP fleet-wide; per-cluster NP; mesh L7 policy

**AdminNetworkPolicy fleet-wide**: GitOps-deployed via Argo CD ApplicationSets. Org rules: "deny ingress from sandbox-* to prod-*; deny egress to RFC-1918 from prod-*; require mTLS for east-west."
    **NetworkPolicy per team**: default-deny + explicit allow. Generated from service catalog + Hubble flow observation in dev + curated in Git.
    **Mesh L7 (Linkerd ambient)**: AuthorizationPolicy per Service — "only orders SA may call payments SA on POST /charge." Mesh traffic shifting + canary.

## 3. Hubble + Pixie + Tetragon everywhere; multi-cluster

**Hubble** in every cluster + Hubble Relay aggregating across clusters. Per-flow + L7 verdicts cluster-wide. Hubble UI shows multi-cluster service map.
    **Pixie** on every cluster: per-Service L7 trace; per-endpoint latency. CI pulls Pixie data + alarms on regressions.
    **Tetragon**: kernel-level event log per cluster; SIEM aggregates; rules detect novel patterns.
    **kube-burner**: CI gates on cluster perf regressions; runs against staging clusters before any CNI / mesh upgrade.

## 4. region failover + per-bridge runbooks

**Region failover**: global LB health checks per cluster's ingress; failed cluster removed from rotation in < 60s; traffic shifts to healthy clusters. Stateful workloads either active-active (replicated state) or active-passive (controlled failover with promote / demote).
    **Per-bridge runbooks**: ClusterMesh apiserver down (rebuild from etcd); Submariner gateway dead (failover to redundant gateway); Skupper VAN router stuck (re-establish TLS); Gateway controller crashloop (rollback CRD). Each runbook tested via game days.
    **Disaster scenarios**: region outage drill quarterly; cross-cloud failover drill semi-annually; partner-cluster integration regression annually. Time-to-detect / time-to-recover measured + improved.
    **The architecture is not the work; the discipline of operating it is.**

## Before / After

**Before.** Single-cloud / single-cluster + ad-hoc multi-cluster patterns. Region outage = product outage. Cross-cluster traffic via VPN. Observability fragmented. Runbooks aspirational.

**After.** Multi-cloud reference: bridges per peer pattern; ANP fleet-wide; Hubble + Pixie everywhere; private + hybrid; global LB failover. Region failure = 5-minute failover; partner integration = day-of standup.

*Pick bridges by peer pattern; ANP fleet-wide; observe everything; drill the runbook quarterly.*

## Analogy — the K-Highway junction

The capstone Highway Captain administers five cities across four nations. Each city pair is connected by the right bridge — twin-city expressways where the cities share planners, border-tunnels for different planners, diplomatic-pouches for foreign neighbours. Federal customs sets non-negotiable rules; each city refines within. Traffic helicopters circle every city; reports stream to the central command. The Captain runs region-failover drills every quarter — vehicles destined for the offline city redirect to the next-closest city in < 1 minute.
    The capstone is the sum of N1-N6: bridges (N3), Gateway API (N2), CNI + eBPF + BGP (N1), mesh + DNS (N4), policy + private + hybrid (N5), tracing + perf (N6). Plus operational rhythm.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Five cities, four nations | 5 clusters across AWS + Azure + GCP + on-prem |
| Twin-city expressway | Cilium ClusterMesh (same-CNI peers) |
| Border-tunnel | Submariner (cross-CNI peer) |
| Diplomatic-pouch | Skupper (partner / cross-org) |
| City entrance signs | Gateway API per cluster |
| Federal customs rules | AdminNetworkPolicy fleet-wide |
| Helicopters everywhere | Hubble / Pixie / Tetragon multi-cluster |
| Region-failover drill | Global LB failover + cross-cluster state |
| Diplomatic embassy line | Private apiserver + DX/ER/CI hybrid |

⚠️ *Analogy stops here:* A real city has fixed roads; cluster bridges + policy are software. Region failover scenarios must be exercised; they don't self-verify.

## ELI5 / ELI10

**ELI5.** Five cities; four bridges; central air-traffic control; quarterly disaster drills. The capstone is everything connected, observed, and exercised.

**ELI10.** **Clusters**: EKS x2 + AKS + GKE + OCP-on-prem. **Bridges**: ClusterMesh + Submariner + Skupper. **Edge**: Gateway API + global LB / DNS. **Policy**: AdminNetworkPolicy + NP + mesh AuthorizationPolicy. **Observability**: Hubble + Pixie + Tetragon multi-cluster. **Connectivity**: private clusters + DX/ER/CI hybrid + egress gateways. **Operational rhythm**: kube-burner CI + quarterly failover drills + per-bridge runbooks.

## Real-world scenarios

- **Real region failover — 90-second recovery.** A real AWS us-east-1 brownout: global LB health checks marked the EKS us-east cluster unhealthy at T+45s; Route 53 shifted traffic to EKS eu-west-1; user impact < 90s. Stateful Services already replicated. *The drill the team ran 3 weeks before paid off.*
- **Partner integration via Skupper — 1-day standup.** A new partner Service needed integration. Skupper VAN: partner side router peered with our router via TLS; Service exposed only via the VAN; no VPN, no firewall changes. Standup: 1 day; weeks shorter than VPN setup.
- **ANP caught a misconfigured tenant.** A new tenant team's NetworkPolicy allowed egress to RFC-1918. AdminNetworkPolicy denied; tenant's deploy logged the override at admission. Tenant updated their NetworkPolicy; deploy went through; no compromise reached prod.
- **Outage — Submariner gateway across clouds.** Submariner gateway between EKS + on-prem OCP failed in middle of replication. Failover to redundant gateway in 6 seconds. Postmortem: validated the redundant-gateway path quarterly; ensure ARP convergence + BGP withdrawal happens cleanly.

## Common misconceptions

- **Myth:** "Multi-cloud is over-engineered for most teams."
  **Truth:** Region failover (multi-region single-cloud) is a baseline for any product with paying customers. Multi-cloud (cross-cloud failover) earns its complexity for regulated / global / partner-heavy workloads. Match the architecture to the risk + customer expectations.
- **Myth:** "One bridge for all clusters is simpler."
  **Truth:** Forcing one bridge means accepting it's suboptimal for some peer patterns. The right answer is: pick the right bridge per peer; the bridges coexist; runbooks document each. Simplicity isn't "one tool"; it's "fewest right tools."
- **Myth:** "GitOps + Argo CD ApplicationSets fleet-deploy everything; no per-cluster work needed."
  **Truth:** ApplicationSets handle per-cluster deployment, but per-cluster differences (e.g., cloud-specific Storage / LB / IAM annotations) need the App template to handle. Fleet GitOps is foundation; per-cluster engineering still applies.

## Recap

Multi-cloud network = bridges per peer + ANP fleet-wide + Hubble everywhere + private hybrid + Gateway API + global LB + runbooks tested via game days. Architecture is the assembly; operational rhythm is the discipline.

**K-ADV-NET complete.** 7 modules. From CNI internals (N1) to multi-cloud capstone (N7). Next K-ADV course: *K-ADV-PE* (Platform Engineering — K-Workshop) or per founder direction.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
