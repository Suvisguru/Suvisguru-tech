# K-ADV-PE P1 — P1 · IDP Foundations + Golden Paths + Self-Service Namespaces

> Course: K-ADV-PE (advanced specialization)
> Module P1 · IDP Foundations
> Companion preview: `/preview-kubernetes-adv-pe-lesson-01.html`.

---

**🎯 If you remember nothing else:** **IDP = platform-as-product. Golden paths cover the 80% common cases (new service, new tenant, new namespace). Self-service via Backstage + Crossplane. Platform SLOs published. Platform team measures customer (developer) NPS.**

## 1. Developer is the customer; platform team owns the experience

**IDP shift**: platform team is no longer "infra ops" or "K8s admins" — they're building a product whose users are developers. Three implications:
    
      - **Customer feedback loop**: developer NPS, time-to-first-deploy, time-to-incident-resolution measured. Quarterly developer surveys.

      - **Roadmap discipline**: features prioritised by customer pain, not infrastructure preferences.

      - **Documentation as deliverable**: TechDocs / Backstage portal as good as any vendor's docs.

    
    Outcome: developers don't "file tickets with infra" — they consume self-service. Platform team scales beyond head-count by templating common cases.

## 2. Opinionated templates — the 80% case automated

**Golden path**: a pre-built, opinionated way to do a common thing. "New microservice in Go" → repo with directory layout + Dockerfile + Helm chart + CI workflow + observability + GitOps onboarding all wired. Developer fills in business logic.
    Implemented via **Backstage Scaffolder**: template + parameters + steps; generates repo + commits initial files + opens PR for cluster onboarding. Developer answers 5 questions; first deploy in 10 minutes.
    Common golden paths: new service (per language), new tenant namespace, new database (Postgres / MySQL / DynamoDB), new ingress / API endpoint, new observability dashboard. **The platform team owns templates**; updates propagate to new services automatically.

## 3. Templated tenant onboarding with governance baked in

Manual namespace creation is the platform-team bottleneck. **Self-service**:
    
      - **Backstage form** or CLI command: tenant name, owner, tier (gold / silver / bronze), cost-center.

      - **Crossplane Claim** renders Namespace + RoleBinding (per OIDC group) + NetworkPolicy default-deny + ResourceQuota + LimitRange + service catalog entry.

      - **GitOps PR**: human-approved (or automated for trusted requesters); merge → namespace materializes within minutes.

    
    **Day-1 governance is day-0**: the new namespace has every guardrail from the moment it exists. No "we'll add NetworkPolicy later."

## 4. Publish the platform's contract like a vendor

Platform team publishes **SLOs**:
    
      - **Cluster availability**: 99.9% / 99.95% / 99.99% — different per tier.

      - **Deploy latency**: P95 deploy < 5 min from git push to running.

      - **Capacity headroom**: never < 20% free; auto-scale before saturation.

      - **Onboarding latency**: P95 new service < 30 min; new tenant < 1 day.

      - **Incident response**: P95 detect < 5 min; respond < 15 min; resolve per severity.

    
    Visible in Backstage; quarterly review with stakeholders; failures trigger postmortem + roadmap items. *The platform is held to a contract; tenants know what to expect.*

## Before / After

**Before.** Pre-IDP, every team built their own platform pieces. Platform team filed tickets. Onboarding took weeks. Bespoke YAML across teams. Platform team scaled with head-count, not leverage.

**After.** IDP: platform-as-product; golden paths cover 80%; self-service via Backstage + Crossplane; SLOs published. Onboarding in 1 day; platform team scales beyond head-count.

*Treat developers as customers; ship platform features as a product.*

## Analogy — the K-Workshop bench

K-Workshop's Master Blueprint Library shelves hundreds of pre-drafted blueprints. Apprentices (developers) walk in with a request — "I need a wagon" — and pick the closest blueprint from the shelf. The shop's standard tools, materials, and finishes are pre-stocked. The apprentice fills in the wagon's specific cargo carrying capacity; the wagon ships in hours, not weeks.
    The Master Craftsperson (platform team) maintains the blueprints + the standard tools. New blueprints are added by customer demand. Each blueprint comes with a sealed contract (SLO) — "this wagon meets payload X over Y miles before service."

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Master Blueprint Library | Internal Developer Platform (IDP) |
| Pre-drafted blueprint | Golden path / Backstage Scaffolder template |
| Apprentice (customer) | Developer |
| Master Craftsperson | Platform engineer |
| Pre-stocked tools + materials | Standard CI + manifests + observability |
| Sealed contract (SLO) | Platform SLO (uptime + latency + headroom) |
| Blueprint shelf catalog | Backstage catalog |
| New blueprint by request | New golden path / template via PR |

⚠️ *Analogy stops here:* A real blueprint is paper; golden-path templates evolve as the platform evolves. Old templates produce old shapes; refresh templates as standards drift.

## ELI5 / ELI10

**ELI5.** A workshop with shelves of pre-drafted blueprints. You walk in, pick the right blueprint, fill in the small bits, your wagon ships. The workshop's manager keeps the blueprints fresh.

**ELI10.** **IDP** = platform-as-product; developer is the customer. **Golden paths** = opinionated Backstage Scaffolder templates (repo + CI + manifests + observability). **Self-service NS** = Backstage form → Crossplane Claim → GitOps PR → namespace with RBAC + NetPol + Quota. **Platform SLOs**: cluster availability + deploy latency + capacity headroom + onboarding latency + IR.

## Real-world scenarios

- **Backstage golden path — new service in 10 minutes.** A 200-engineer org adopts Backstage. "New Go service" template generates repo + Helm chart + GitHub Actions + observability + Argo CD onboarding. Developer answers 5 questions; first deploy in 10 minutes; quality bar = day-1 production-ready.
- **Self-service namespace via Crossplane Claim.** A team needs a new namespace. Backstage form: name + owner + tier + cost-center. Crossplane Claim renders Namespace + RoleBinding + NetPol + Quota + service catalog entry. GitOps PR auto-merged after policy gates. Namespace ready in 5 minutes.
- **Platform SLO drove a roadmap item.** P95 deploy latency degraded over 6 months — Argo CD sync time grew. Platform SLO breach surfaced in quarterly review; Argo CD + cluster-mesh-apiserver upgrade prioritised; SLO recovered next quarter.
- **Onboarding bottleneck before IDP.** Pre-IDP, each new tenant was 2-week setup; platform team booked solid. Adopted golden paths + Crossplane self-service; new tenant Day-1 to production. Platform team headcount stayed flat as tenant count tripled.

## Common misconceptions

- **Myth:** "IDP is just Backstage."
  **Truth:** Backstage is the storefront; IDP is the operating model. Backstage + Crossplane + Argo CD + OPA + golden paths + tenant catalog + SLOs together form the IDP. Backstage alone without the back-end automation is a portal that doesn't self-serve.
- **Myth:** "Self-service means no platform-team review."
  **Truth:** Self-service automates the 80% common case + leaves human-approved PR for the 20% novel cases. Templates have policy gates; deviations escalate to platform team review. Self-service is templated + governed, not unmanaged.
- **Myth:** "Platform SLOs are vanity metrics."
  **Truth:** SLOs are the platform team's product contract. Without them, tenants don't know what to expect; platform team has no measurable goal. SLOs drive roadmap + postmortems; vanity vs operational is a question of follow-through.

## Recap

IDP = platform-as-product. Golden paths cover 80%. Self-service via Backstage + Crossplane. Platform SLOs are the contract. Developer NPS is the success metric.

**Next — P2: Backstage deep dive.** Catalog, TechDocs, Scaffolder, plugins. The IDP storefront.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
