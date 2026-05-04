# K-ADV-PE P7 — P7 · Platform SLOs + Chargeback / Showback

> Course: K-ADV-PE (advanced specialization)
> Module P7 · SLOs + Chargeback
> Companion preview: `/preview-kubernetes-adv-pe-lesson-07.html`.

---

**🎯 If you remember nothing else:** **Platform SLOs are the contract; OpenCost / Kubecost surfaces cost per team. Chargeback (real bill) drives optimisation; showback (visible cost) is the gentle nudge. Both pay for themselves in tenant-driven cost reduction.**

## 1. Publish the contract; review quarterly

Platform team publishes SLOs:
    
      - **Cluster availability**: per tier; 99.9 / 99.95 / 99.99%.

      - **Deploy latency**: P95 git push → running < 5 min.

      - **Capacity headroom**: ≥ 20% free; auto-scale before saturation.

      - **Onboarding latency**: P95 new tenant < 1 day; new service < 30 min.

      - **Incident response**: P95 detect < 5 min; respond < 15 min; resolve per severity.

    
    Visible in Backstage; quarterly stakeholder review; failures → postmortem + roadmap items.

## 2. Cost allocation foundations + commercial extension

**OpenCost** (CNCF Incubating): open-source. Aggregates cloud-provider bill + per-Pod CPU / memory / storage / network utilization → per-Pod cost. Foundational. Free.
    **Kubecost** (commercial; built on OpenCost): adds richer dashboards + chargeback automation + recommendations + multi-cluster aggregation. Commercial tiers for budget alerts / forecasting / governance.
    Most teams: start with OpenCost; upgrade to Kubecost when chargeback automation needed. Both compatible.

## 3. Real bill vs visible cost

**Showback**: every team sees their cost in dashboards. No actual bill exchange; visibility drives behavior. Easier to roll out; lower friction.
    **Chargeback**: monthly bill from platform team to consuming team; finance allocates real $$. Stronger behavior change; more political.
    Most orgs run showback first; mature to chargeback when teams accustomed + finance ready. Kubecost automates chargeback; OpenCost foundations + custom integration for showback dashboards.

## 4. What teams do once they see cost

Once tenants see cost, common optimisations:
    
      - **Right-size requests**: many Pods request 2× what they use. VPA recommendations + manual review.

      - **Spot / Preemptible** for tolerable workloads — 60-90% discount.

      - **Scale-to-zero** for off-hours (Knative / KEDA scale-to-zero).

      - **ARM64 / Graviton** — 20-30% cheaper for compatible workloads.

      - **Reserved Instances / Savings Plans / CUDs** for steady baseline.

      - **Storage tiering**: log archive to S3 IA / Glacier; hot data on EBS gp3.

    
    Platform team publishes the playbook; tenants self-tune. Visible cost = behavior change.

## Before / After

**Before.** Pre-cost-transparency, platform team paid the cloud bill; tenants had no incentive to optimise. Bills surprised; allocation was "trust us"; teams optimised only when paged.

**After.** Platform SLOs published; OpenCost / Kubecost surface per-team cost; chargeback or showback drives behavior. Right-sizing + Spot + scale-to-zero adopted by tenants without platform-team push.

*SLOs = the contract. Cost transparency = the incentive. Together = a healthy platform business.*

## Analogy — the K-Workshop bench

Workshop Accounting is the master's ledger room. The walls show the workshop's commitments to apprentices (SLOs). The ledgers track every apprentice's consumed materials (OpenCost). Monthly bills go out (chargeback) or visible reports (showback) — apprentices see their consumption + adjust.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Workshop commitments wall | Platform SLOs (uptime + latency + headroom + onboarding + IR) |
| Apprentice material ledger | OpenCost / Kubecost |
| Monthly bill | Chargeback (real cost allocation) |
| Visible report | Showback (visible without billing) |
| Cost-center stamp | cost-center label on every Pod |
| Optimisation playbook | right-size + Spot + scale-to-zero + ARM64 + RIs |
| VPA recommendations | Vertical Pod Autoscaler advisory mode |

⚠️ *Analogy stops here:* Workshop ledgers are paper; cost data is API + dashboards. Per-Pod cost is a function of cloud bill + utilisation snapshots; not always penny-precise.

## ELI5 / ELI10

**ELI5.** Two things on the wall: what the workshop promises (SLOs) + what each apprentice spends (cost). Apprentices see their costs and learn to spend less.

**ELI10.** **Platform SLOs**: published per tier; cluster availability + deploy latency + capacity headroom + onboarding + IR. **OpenCost** (CNCF) + **Kubecost** (commercial extension): per-Pod / per-namespace / per-tenant cost from cloud bill + utilization. **Chargeback** (real bill) vs **showback** (visible). **Optimisation playbook**: right-size + Spot + scale-to-zero + ARM64 + RIs / SP / CUDs.

## Real-world scenarios

- **Showback drove tenant behavior.** 6 months after Kubecost rolled out: per-tenant cost reports in Slack weekly. Top spenders right-sized; one team adopted Spot for batch; aggregate cluster cost dropped 22% without platform-team intervention.
- **SLO breach drove roadmap.** Onboarding-latency SLO P95 < 1 day broke at 6 days. Postmortem: Crossplane reconciliation lag from missing CRDs. Roadmap item: pre-install required CRDs in cluster bootstrap. SLO recovered next quarter.
- **Chargeback rollout — finance + engineering aligned.** After 6 months of showback, org rolled chargeback. Each team's cloud cost in their P&L. CFO supports platform team's capacity expansion proposals because cost mapping is clear.
- **Outage — surprise $40k from one tenant.** Pre-controls, one tenant's Quota limit was high; Pods consumed; cost spiked. OpenCost + budget alerts + tighter Quota added. Same shape no longer possible.

## Common misconceptions

- **Myth:** "Platform SLOs are aspirational; nobody enforces."
  **Truth:** If unenforced, tenants don't plan around them. Quarterly stakeholder review + postmortem on misses + roadmap items make SLOs real.
- **Myth:** "OpenCost is precise."
  **Truth:** OpenCost is best-effort allocation: cloud-bill aggregates + per-Pod utilization snapshots. ~5-10% precision; good enough for chargeback at the team level.
- **Myth:** "Chargeback is too political; just use showback."
  **Truth:** Showback is fine for some orgs; chargeback aligns engineering with finance. Mature orgs run chargeback; the political work is one-time setup.

## Recap

Platform SLOs published as contract; OpenCost / Kubecost surface per-team cost; showback or chargeback drives behavior. Cost optimisation playbook + tenant self-tune.

**Next — P8: Capstone — self-service IDP with namespace provisioning, RBAC, quotas, NetworkPolicy, GitOps, app templates, observability, cost labels, policy guardrails.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
