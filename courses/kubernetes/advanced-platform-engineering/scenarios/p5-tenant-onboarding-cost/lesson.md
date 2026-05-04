# K-ADV-PE P5 — P5 · Tenant Onboarding + Resource Templates + Cost Controls

> Course: K-ADV-PE (advanced specialization)
> Module P5 · Tenant Onboarding + Cost
> Companion preview: `/preview-kubernetes-adv-pe-lesson-05.html`.

---

**🎯 If you remember nothing else:** **Tenant onboarding via templated Crossplane Claim. Tiers + Quotas + cost labels + budget alerts baked in. Service catalog of pre-approved resources via XRDs. Day-1 economic governance.**

## 1. Form → Claim → PR → namespace

Step 1: **Backstage Scaffolder form** — tenant name, owner, tier (gold/silver/bronze), cost-center, expected workload class.
    Step 2: **Crossplane Claim** renders Namespace + RoleBinding (per OIDC group) + NetworkPolicy default-deny + ResourceQuota + LimitRange + cost label + Backstage Catalog entry.
    Step 3: **GitOps PR** auto-opened against fleet repo; policy gates run; auto-merge for trusted; human-approved for novel patterns.
    Step 4: **Argo CD ApplicationSet** picks up the new namespace claim; reconciles; namespace materializes within minutes.

## 2. Gold / silver / bronze defaults

Tiers encode per-tenant resource defaults:
    
      - **Gold**: ResourceQuota 50 vCPU + 100 GiB; PriorityClass guaranteed; multi-AZ NodeAffinity; HPA + PDB defaults; 99.95% SLO.

      - **Silver**: 20 vCPU + 40 GiB; standard PriorityClass; single-AZ tolerated; 99.9% SLO.

      - **Bronze**: 5 vCPU + 10 GiB; low PriorityClass; preemptible nodes OK; 99% SLO.

    
    Tiers map to cost: gold = ~5×bronze. Tenant chooses + accepts the budget at intake.

## 3. Labels + OpenCost / Kubecost + budget alerts

**Cost label**: every Pod / Service / PVC carries `cost-center` + `tenant` labels (mutating webhook injects if missing).
    **OpenCost / Kubecost**: aggregate cloud bill + per-Pod utilization; report cost per cost-center / tenant / namespace. Backstage plugin surfaces in service page.
    **Budget alerts**: per-tenant monthly budget; OpenCost emits Slack/email at 50% / 75% / 95% / 100% of budget.
    **Hard caps**: ResourceQuota enforces; tenant's requests cannot exceed. Hard cap + budget alert = no cost surprises.

## 4. XRDs as the menu of pre-approved resources

**Service catalog**: Backstage shows XRDs (XPostgresInstance, XBucket, XQueue, XCert) as service-template entries. Tenants browse; click "Provision"; Backstage form → Crossplane Claim → resource ships.
    Catalog entries include: schema (what to fill in), tier defaults, cost estimate per tier, owning team, runbook link.
    Pattern: every recurring infra request becomes a catalog entry; tenant self-service replaces the platform-team ticket.

## Before / After

**Before.** Pre-templated tenancy: each new tenant 2-week setup; bespoke YAML; no cost labels; surprise bills.

**After.** Tenant onboarding form → Claim → PR → namespace in < 1 day. Tiers encode quota + cost defaults. OpenCost surfaces per-tenant cost; budget alerts; service catalog of pre-approved resources.

*Day-1 governance + economics + service catalog. New tenant in < 1 day.*

## Analogy — the K-Workshop bench

Apprentice Intake is the workshop's door. New apprentices fill out the intake form (Backstage); the form picks a tier (gold / silver / bronze) which determines the workspace size + tools issued + budget. The intake clerk (Crossplane Claim) materialises the workspace. The accountant (OpenCost) tracks every apprentice's consumed materials; alarms when budget approaches. A menu (service catalog) lets apprentices order pre-approved tools without back-and-forth.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Apprentice Intake form | Backstage Scaffolder form |
| Tier (gold/silver/bronze) | Resource tier (Quota + NetPol + PriorityClass) |
| Intake clerk | Crossplane Claim |
| Workspace materialisation | Namespace + RBAC + NetPol + Quota + LimitRange |
| Accountant's ledger | OpenCost / Kubecost |
| Budget alarm | Slack/email at 75% / 95% / 100% of budget |
| Pre-approved tool menu | Service catalog of XRDs |

⚠️ *Analogy stops here:* A real apprentice intake is one-time; tenant tiers can be promoted (silver → gold) via PR — graceful upgrade path matters.

## ELI5 / ELI10

**ELI5.** Fill out the form. Pick a tier. The workspace + tools + budget materialize. The accountant warns you before you blow the budget.

**ELI10.** **Onboarding**: Backstage form → Crossplane Claim → GitOps PR → Argo CD. **Tiers**: gold/silver/bronze with Quota + PriorityClass + NetPol defaults. **Cost**: cost-center label + OpenCost / Kubecost + budget alerts. **Service catalog**: XRDs as menu items in Backstage.

## Real-world scenarios

- **New tenant in 30 minutes.** A team needs a new namespace; form → Claim → PR → Argo CD reconciles in 25 min. Day-1 quota + cost label + NetPol + RBAC; team starts deploying immediately.
- **Budget alert caught runaway dev workload.** A dev image had a memory leak; namespace approached 100% of monthly budget by mid-month. OpenCost alarm at 75%; team paged; fixed; budget recovered.
- **Tier promotion via PR.** A silver tenant's prod workload outgrew tier; team PRs the Claim with tier=gold; quota + observability defaults upgrade overnight.
- **Outage — no quota; surprise $40k bill.** Pre-controls, one tenant ran 200 unconstrained Pods; cloud bill spiked. Postmortem: ResourceQuota + cost label mandatory; budget alerts wired; never again.

## Common misconceptions

- **Myth:** "Cost labels don't need to be enforced."
  **Truth:** Without a mutating webhook adding cost-center labels, tenants forget. OpenCost / Kubecost can't allocate; cost surprises follow.
- **Myth:** "Service catalog is fancy YAML."
  **Truth:** Service catalog = XRDs + Backstage Scaffolder integration. Tenants browse + click; Crossplane provisions. Replaces ticket queue + per-resource bespoke.
- **Myth:** "Tiers are restrictive."
  **Truth:** Tiers are *defaults*; tenants pick at intake; promote via PR. Tiers eliminate per-tenant Quota math; PR for the 20% that need different shapes.

## Recap

Tenant onboarding via Backstage + Crossplane + GitOps. Tiers encode defaults. OpenCost / Kubecost surface cost per tenant. Service catalog of pre-approved resources. Day-1 governance + economics.

**Next — P6: Workload abstractions (Score, OAM, Radius, Humanitec).**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
