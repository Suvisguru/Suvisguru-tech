# K-ADV-PE P8 — P8 · Capstone — Self-Service IDP

> Course: K-ADV-PE (advanced specialization)
> Module P8 · Capstone IDP
> Companion preview: `/preview-kubernetes-adv-pe-lesson-08.html`.

---

**🎯 If you remember nothing else:** **Equipped IDP: Backstage + Crossplane + Argo CD + OPA + Score / OAM + OpenCost + SLOs + tenant onboarding + game-day rhythm. Self-service end-to-end; day-1 governance day-0; new tenant in < 1 day; new service in < 30 min.**

## 1. Storefront + API + GitOps + governance

**Storefront**: Backstage portal with Catalog (every service registered), TechDocs (per-repo docs), Scaffolder (golden paths), Plugins (Argo CD / K8s / PagerDuty / Datadog / OpenCost / Crossplane / Kubernetes).
    **API**: Crossplane XRDs (XPostgresInstance / XBucket / XQueue / XTenantNamespace / XCert) — tenants consume; platform team owns Compositions + Functions + Providers.
    **Fleet GitOps**: Argo CD ApplicationSets across all clusters; per-cluster values from labels; ProgressiveSync dev → staging → prod.
    **Governance**: OPA + Kyverno gates at PR + admission + sync; PSA Restricted; per-namespace Quota + LimitRange + NetPol; OPA conftest in CI.

## 2. Onboard a tenant; ship a service

**Onboard a tenant**: Backstage form (name + tier + cost-center) → Crossplane XTenantNamespace Claim → GitOps PR auto-merged → Argo CD reconciles → namespace + RBAC + NetPol + Quota + cost label ready in 5 min.
    **Ship a new service**: Backstage Scaffolder ("new Go service") → repo + Helm + CI + Argo CD App + observability + Score spec generated → first deploy in 10 min.
    **Provision infra**: Backstage service catalog → pick XRD (XPostgres) → fill form → Crossplane Claim → GitOps PR → resource ships in minutes.

## 3. Score / OAM + OpenCost + dashboards in Backstage

**Score spec** in every repo: 30-line workload definition; score-helm renders to chart at build; portable to dev/staging/prod targets.
    **Observability bundled**: Prometheus + Grafana + Loki + Tempo / X-Ray pre-wired per template; Datadog plugin in Backstage; OpenTelemetry for tracing.
    **Cost labels**: Kyverno mutating webhook injects on every Pod / Service / PVC; OpenCost / Kubecost dashboards in Backstage service page; budget alerts via Slack.

## 4. Game days + cost reviews + SLO retros

**Quarterly game days**: simulate platform failure (Argo CD down, Crossplane provider stuck, GitOps PR storm) + measure response.
    **Monthly cost review**: top spenders, optimisation playbook adoption, chargeback / showback adjustments.
    **Quarterly SLO retro**: any SLO breach? Postmortem. Roadmap items. Stakeholder review.
    **Continuous developer NPS**: quarterly survey + open-text feedback drives platform roadmap.
    **The architecture is the easy part; the operational rhythm is the discipline that keeps the workshop equipped.**

## Before / After

**Before.** Pre-IDP: per-team platform pieces; manual tickets; bespoke tenancy; cost surprises; SLOs aspirational; no game days; reactive ops.

**After.** Equipped IDP: every K-ADV-PE concept woven. Self-service end-to-end; day-1 governance; cost transparency; SLOs as contract; game days exercise; developer NPS as metric.

*The architecture is widely-known; the operational rhythm is the differentiator.*

## Analogy — the K-Workshop bench

The Equipped Workshop has every blueprint, every tool, every standard part stocked. Apprentices walk in, self-serve. The Master Craftsperson reviews monthly cost reports + quarterly SLO retros + game-day exercises. New apprentice in 30 min from form to ship.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Storefront | Backstage portal |
| Platform API | Crossplane XRDs |
| Fleet GitOps | Argo CD ApplicationSets |
| Quality inspectors | OPA + Kyverno gates (PR + admission + sync) |
| Standard tool kits | Score / OAM workload abstractions |
| Workshop accounting | OpenCost / Kubecost |
| Workshop commitments | Platform SLOs |
| Apprentice intake | Tenant onboarding (XTenantNamespace) |
| Quarterly drills | Game days |
| Master Craftsperson reviews | Quarterly SLO retros + monthly cost review |

⚠️ *Analogy stops here:* A real workshop has fixed assets; an IDP evolves continuously — new XRDs, new templates, new policies. The capstone is a snapshot; tomorrow it grows.

## ELI5 / ELI10

**ELI5.** The complete workshop. Apprentices walk in, fill out a form, ship their wagon. The master keeps the workshop equipped + organized.

**ELI10.** **Storefront**: Backstage. **API**: Crossplane XRDs. **GitOps**: Argo CD ApplicationSets + ProgressiveSync. **Governance**: OPA + Kyverno + PSA + Quota. **Workload**: Score / OAM. **Cost**: OpenCost + Kubecost + showback / chargeback. **Contract**: Platform SLOs. **Onboarding**: templated; day-1 governance. **Operational rhythm**: game days + cost reviews + SLO retros + developer NPS.

## Real-world scenarios

- **New developer onboarded in 60 minutes.** Day 1: Backstage account; pick "new Go service"; deploy in 10 min; day-1 observability + cost + SLO. Within an hour: producing user-visible feature.
- **New tenant in 30 minutes.** Form → Claim → PR → Argo CD reconciles. Namespace + RBAC + NetPol + Quota + cost label + Backstage entry ready.
- **Quarterly cost review drove behavior.** Showback dashboards highlighted top spenders; teams adopted Spot + scale-to-zero; aggregate cost dropped 25% over a quarter without platform-team push.
- **Game day caught Crossplane provider stuck.** Simulated provider-aws Pod restart loop; Crossplane stuck; tenant Claims pending. Runbook: provider-aws restart; ProviderConfig auth verify; eventual reconcile. Time-to-recover < 15 min; runbook updated.

## Common misconceptions

- **Myth:** "This architecture is over-engineered for < 100-engineer teams."
  **Truth:** Marginal cost of building from day-1 is moderate; cost of retrofitting after the team grows is enormous. Service Catalog template + golden paths from day-1 = engineers grow into the discipline.
- **Myth:** "Once built, the IDP runs itself."
  **Truth:** IDP is a product; needs continuous roadmap + customer feedback. Without operational rhythm + dev NPS, the IDP rots.
- **Myth:** "Backstage alone is the IDP."
  **Truth:** Backstage is the storefront; Crossplane is the API; Argo CD is the runtime; OPA + Kyverno are the gates; OpenCost is the accounting; SLOs are the contract. Together they form the IDP.

## Recap

Equipped IDP: Backstage + Crossplane + Argo CD + OPA + Score / OAM + OpenCost + SLOs + tenant onboarding + operational rhythm. Self-service end-to-end; day-1 governance; new tenant in < 1 day; new service in < 30 min.

**K-ADV-PE complete.** 8 modules. From IDP foundations (P1) to capstone (P8). Next K-ADV course: *K-ADV-AI* (K-Observatory) or per founder direction.

## Flashcards and quiz

See `flashcards.yaml` (5 cards) and `quiz.yaml` (3 questions).
