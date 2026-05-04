# K-ADV-PE P3 — P3 · Crossplane v2

> Course: K-ADV-PE (advanced specialization)
> Module P3 · Crossplane v2
> Companion preview: `/preview-kubernetes-adv-pe-lesson-03.html`.

---

**🎯 If you remember nothing else:** **Crossplane v2: XRD = user-facing CRD; Composition + Functions = render logic; Providers = AWS / Azure / GCP / SaaS controllers; ConfigurationPackage = shareable bundle. Platform-as-API; one consistent shape for every tenant.**

## 1. K8s control plane for cloud resources

Crossplane runs in your cluster as a CRD-driven control plane for external resources. Apply a CR; Crossplane reconciles in the cloud. *kubectl is the API for everything* — cloud + SaaS + on-prem.
    Compared to Terraform: Crossplane is *continuous reconciliation* (drift auto-corrected), runs *in-cluster* (no separate state file), uses *K8s primitives* (RBAC, audit, GitOps). Trade: K8s as the runtime; learning curve for non-K8s shops.

## 2. Define the user API + render logic

**XRD (CompositeResourceDefinition)**: declares a user-facing CRD (e.g., `XPostgresInstance`) with schema + claim type (namespaced version). Tenants create Claims; XR controller reconciles.
    **Composition**: per XRD, declares how to render to Provider resources. e.g., XPostgresInstance Composition renders: AWS RDSInstance + DBSubnetGroup + IAMRole + KMS Key + Backup config. Tenants see one CR; platform composes the stack.
    **Multiple Compositions per XRD**: "AWS-RDS Postgres" + "Azure-Database-Postgres" + "on-prem-CloudNativePG" — same user-facing XRD; cloud-specific render logic. Selector at Claim picks Composition.

## 3. Pluggable composition logic — KCL / Pkl / Go / patch-and-transform

**Functions** (Crossplane v1.14+) replace legacy patch-and-transform with a pluggable pipeline. Each Function is a container; Composition declares a list of Function calls; each transforms the desired state.
    Common Functions: **function-go-templating** (Go templates), **function-kcl** (KCL — typed config language), **function-pkl** (Pkl — Apple's config language), **function-patch-and-transform** (legacy YAML patches), **function-cel** (CEL expressions).
    Pick by team's ergonomics. KCL + Pkl typed; Go templating familiar; CEL expression-style. Functions are versioned + tested independently.

## 4. Provider ecosystem + shareable bundles

**Providers**: per-platform controllers. *provider-upjet-aws* + *provider-upjet-azure* + *provider-upjet-gcp* ship Terraform-resource-equivalent CRDs. *provider-kubernetes* + *provider-helm* for in-cluster. *provider-github*, *provider-vault*, *provider-cloudflare*, etc. for SaaS.
    Provider auth via ProviderConfig: cloud creds (IRSA / Workload Identity for least-privilege) or static creds.
    **ConfigurationPackages**: bundle XRDs + Compositions + Function references + Provider references in one OCI artifact. `crossplane xpkg push registry.example.com/my-platform:v1.0`. Install on any cluster: same platform shape everywhere. *Shareable platforms across teams + companies*.

## Before / After

**Before.** Pre-Crossplane: Terraform per team or manual cloud console. Drift constant. Tenant onboarding bespoke. State files everywhere.

**After.** Crossplane v2: XRDs are the API; Compositions + Functions render to Providers; ConfigurationPackages distribute the platform. Tenants `kubectl apply` a Claim; consistent infra ships.

*Platform-as-API. Tenants consume; platform team owns the API contract.*

## Analogy — the K-Workshop bench

The Composition Workbench is where the Master Craftsperson designs reusable assemblies. The blueprint (XRD) declares what the customer asks for. The assembly instructions (Composition + Functions) explain how to combine standard parts (Providers) to fulfill the order. The whole assembly ships as a sealed package (ConfigurationPackage) to other workshops; install once, build the same assembly anywhere.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Customer order form | XRD (CompositeResourceDefinition) |
| Customer order | Claim |
| Assembly instructions | Composition |
| Pluggable assembly steps | Functions (KCL / Pkl / Go / patch-and-transform / CEL) |
| Standard parts catalog | Providers (provider-upjet-aws / azure / gcp / SaaS) |
| Sealed package | ConfigurationPackage (OCI artifact) |
| Workshop installation | crossplane xpkg install |

⚠️ *Analogy stops here:* A real assembly is one-time; Crossplane reconciles continuously — drift is auto-corrected (sometimes surprising if a human edited the resource directly).

## ELI5 / ELI10

**ELI5.** A workbench where the master writes assembly instructions for the most-asked customer orders. Customer says "I want this kind of thing"; the workbench reads the order; combines standard parts; ships the result. The whole workbench can be sealed + sent to another shop.

**ELI10.** **XRD**: user-facing CRD + Claim type. **Composition**: render logic per XRD; selectable per Claim. **Functions**: pluggable pipeline (KCL / Pkl / Go templates / patch-and-transform / CEL). **Providers**: cloud + SaaS controllers (Upjet-generated for AWS/Azure/GCP). **ConfigurationPackage**: OCI-distributed bundle.

## Real-world scenarios

- **XPostgresInstance — one CRD, three clouds.** Platform ships XPostgresInstance XRD + 3 Compositions (AWS RDS / Azure Database / GCP CloudSQL). Tenant Claims pick cloud via label; consistent backup + IAM + monitoring across all three.
- **XTenantNamespace — onboarding.** XTenantNamespace XRD ships namespace + RBAC + NetPol + Quota + service-catalog entry. Tenant Claim form-fillable; new tenant ready in 5 minutes.
- **ConfigurationPackage distributed across business units.** Platform team ships one ConfigurationPackage (XPostgres + XTenantNamespace + XBucket); 8 BU clusters install; same shape everywhere.
- **Outage — drift auto-corrected.** A human edited an RDS instance via console; Crossplane saw drift; reconciled back to spec. Postmortem: enable manual-edit detection alerts; train teams that Crossplane is source of truth.

## Common misconceptions

- **Myth:** "Crossplane replaces Terraform."
  **Truth:** Different model. Crossplane = continuous reconciliation in-cluster; Terraform = one-shot apply. Many teams use both: Crossplane for runtime cloud + SaaS resources; Terraform for one-shot bootstrap (VPC / cluster itself).
- **Myth:** "Functions are too new."
  **Truth:** Crossplane v1.14+ Functions are GA + recommended. Legacy patch-and-transform still supported but Functions are more pluggable + better tested.
- **Myth:** "Providers + Compositions are too low-level for tenants."
  **Truth:** That's the point. Tenants don't see Providers or Compositions; they see XRDs (high-level API). Platform team owns the low-level mapping.

## Recap

Crossplane v2: XRDs are the platform API; Compositions + Functions render; Providers reconcile cloud/SaaS; ConfigurationPackages distribute. Continuous reconciliation; tenant self-service via Claims.

**Next — P4: Argo CD ApplicationSets + OPA / Kyverno guardrails.** Fleet GitOps + policy gates.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
