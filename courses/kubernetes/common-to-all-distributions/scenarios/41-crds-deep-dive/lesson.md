# Lesson 41 — CRDs Deep Dive · Schema, CEL, Conversion Webhooks

> Course: Kubernetes — Common to all distributions
> Module 18 · Extending K8s · Lesson 1 of 3
> Companion preview: `/preview-kubernetes-lesson-41.html`.

---

**🎯 If you remember nothing else:** A CRD has a name, group, versions, scope, and (per version) an OpenAPI v3 schema. Add **CEL validation** via `x-kubernetes-validations`. To evolve schemas safely, define multiple `versions` with one as `storage` + a **conversion webhook** that translates between them on read/write. **Status subresource** separates user spec from controller writes; **scale subresource** enables HPA on custom kinds.

## 1. CRD anatomy

A CustomResourceDefinition has these top-level fields:
    
      - `group`, `names`, `scope` — namespace identity. `group: cert-manager.io`, `kind: Certificate`, `listKind: CertificateList`, `singular: certificate`, `plural: certificates`, `scope: Namespaced` or `Cluster`.

      - `versions` — list of versions. Each has `name` (v1alpha1, v1beta1, v1), `served` (visible to clients), `storage` (exactly one), and a `schema`.

      - `conversion` — strategy for converting between versions. `None` (versions identical) or `Webhook` (call out to your conversion webhook).

    
    The schema is OpenAPI v3 — same as standard K8s schemas. Add `x-kubernetes-validations` for CEL rules; `x-kubernetes-list-type: map` + `map-keys` for proper merge semantics; `x-kubernetes-int-or-string` for fields that accept either.

## 2. In-CRD validation rules

Pre-CEL, validating CRD fields beyond schema constraints required a *validating admission webhook* — a Pod the API server called for every CR write. Latency, fail-policy decisions, deploy ordering pain.
    CEL validation in CRD schema (GA in K8s 1.29) lets you add rules in the CRD itself:
    `spec:
  versions:
  - name: v1
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              replicas: {type: integer, minimum: 1}
              maxReplicas: {type: integer}
            x-kubernetes-validations:
            - rule: "self.maxReplicas >= self.replicas"
              message: "maxReplicas must be ≥ replicas"
            - rule: "self.maxReplicas <= 100"
              message: "maxReplicas cannot exceed 100"`
    CEL has access to `self` (the field being validated), `oldSelf` (previous value, for transition rules), and built-in functions for working with maps, lists, durations, etc. The big win: validation logic ships with the CRD; no webhook needed.

## 3. Schema evolution without breaking users

You can't change a CRD schema in place — existing stored CRs would become invalid. Instead: **add a new version** alongside the old, and a **conversion webhook** that translates between them.
    The flow:
    
      - CRD has `v1alpha1` served + storage. CRs are stored as v1alpha1 in etcd.

      - You add `v1` with the new shape. Set `conversion` to `Webhook` pointing at your conversion service.

      - Now CRD has v1alpha1 + v1, both served, v1alpha1 still storage.

      - Conversion webhook converts v1alpha1 → v1 on read (when client requests v1), v1 → v1alpha1 on write (storage version).

      - Bump `storage: true` to v1. Now writes are v1; existing v1alpha1-stored CRs are converted on read.

      - Run `kubectl get` on every CR to force a rewrite (or use `storage migration` mechanism). All CRs now stored as v1.

      - Drop v1alpha1 from served. (Or remove via deprecated marker first.)

    
    The conversion webhook is a small HTTPS service (Pod + Service) responding to `POST /convert` with the converted object. Most operator frameworks (Kubebuilder, Operator SDK) generate the webhook scaffolding for you.

## 4. Polish that matters in practice

Three CRD features that polish the user experience:
    
      - **`status` subresource** — separates the spec (user-managed) from the status (controller-managed). With it enabled, `kubectl edit` can't change status; `kubectl patch --subresource=status` can. Required for healthy reconciliation patterns.

      - **`scale` subresource** — exposes a `/scale` endpoint compatible with HPA. With it enabled, `kubectl scale myresource --replicas=5` works. HPA can target your CRD.

      - **Additional printer columns** — `kubectl get mykind` defaults to NAME + AGE. Add columns: `READY`, `VERSION`, `STATUS`. JSONPath into the spec/status. Massive UX improvement.

    
    Lifecycle markers:
    
      - **deprecated** — mark a version `deprecated: true` with a `deprecationWarning`. K8s logs warnings on every API call to that version.

      - **removal** — drop the version from `versions`; K8s 410 Gones any client request for it. Make sure no stored CRs are at this version first (run a storage migration).

    
    [ deep dive — skip if new ]The K8s API conventions for versions: `v1alpha1` = experimental, may break, never default. `v1beta1` = closer to stable, may still break. `v1` = stable, won't break. Most operators ship many alpha versions before they stabilise. Don't depend on alpha CRDs in production unless you control the codebase. Storage version skew (clients on v1, storage on v1alpha2) is a real source of subtle bugs; pin client + cluster + CRD versions deliberately.

## Before / After

**Before.** Schema evolution = pain. "Just edit the CRD" silently broke existing CRs. Validation logic lived in webhooks (extra Pods, latency, fail-policy decisions). status subresource not enabled — controllers and users fought over the same fields. `kubectl get mykind` showed only NAME + AGE; you parsed JSON to see anything useful.

**After.** CEL validation in the CRD itself — no webhook. Multiple versions + conversion webhook for schema evolution. status subresource separates spec from status. Printer columns make `kubectl get` useful. Operator framework (Kubebuilder, Operator SDK) generates most of this for you.

CEL's GA in 1.29 was the most consequential CRD change in years. Most validating webhooks for CRDs can now be deleted.

## Analogy — the K-Town district

Back at the Permit Office, the advanced wing handles custom permit forms (CRDs). New form designs need an **OpenAPI schema** describing every field. Validation rules can be inline (**CEL** annotations on the form) or run by a third-party clerk (validating webhook). When the form design changes, the office keeps both versions for a while — old applications stay in their original shape; a **conversion clerk** (webhook) translates between versions on the fly. Eventually old versions are deprecated and removed once nobody uses them.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| New permit form design | `CustomResourceDefinition` |
| Form fields with required types | `openAPIV3Schema` |
| Inline validation rules | `x-kubernetes-validations` CEL |
| Existing applications kept on old form | Stored CRs at older version |
| Conversion clerk translating between forms | Conversion webhook |
| "Form v1 is the storage version" | `storage: true` on a CRD version |
| Status fields the office writes | `status` subresource |
| "Scale up by amount" stamp | `scale` subresource |
| Printed columns on the office board | `additionalPrinterColumns` |
| "This form is being phased out" | `deprecated: true` on a version |

⚠️ *Analogy stops here:* The analogy stops here: real conversion webhooks are HTTP/JSON services with retry semantics + TLS auth. The "clerk" abstraction undersells the operational care needed.

## ELI5 / ELI10

**ELI5.** You write down what your custom form looks like. Rules say what fields are allowed. When you change the form, you keep the old version too and translate between them.

**ELI10.** A CRD has versions, schemas, and optional conversion webhooks. CEL validation (GA 1.29) puts validation rules in the CRD itself, replacing many webhooks. Schema evolution: add new version, set up conversion webhook, migrate storage version, drop old version. Subresources (status, scale) and printer columns polish the user experience. Operator frameworks (Kubebuilder, Operator SDK) generate most of the boilerplate.

## Real-world scenarios

- **A SaaS migrating an Operator from v1alpha1 to v1.** Used Kubebuilder to scaffold v1 alongside v1alpha1. Conversion webhook generated. Tested in dev; ran storage migration via `kubectl get crd-name -o json | kubectl apply -f -` on every CR (forces rewrite at storage version). Marked v1alpha1 deprecated for two minor versions; removed in the third. Zero user-visible breakage.
- **A bank using CEL for cross-field validation.** Custom `SecurityPolicy` CRD. CEL rule: "if scope=Cluster, then issuer must be present." Pre-CEL, this needed a webhook. With CEL, it's 4 lines in the CRD. One less Pod to operate; one less point of failure.
- **A team using subresource scale with HPA.** `WorkerPool` custom resource has `spec.replicas` + `status.readyReplicas`. Scale subresource enabled. HPA points at the WorkerPool with `scaleTargetRef`. Standard K8s autoscaling on a custom kind.
- **A startup with rich printer columns.** `kubectl get certificates` shows NAME, READY, SECRET, EXPIRES, AGE. Configured via `additionalPrinterColumns` on the cert-manager CRD. Saves engineers from `kubectl describe` for routine status checks.

## Common misconceptions

- **Myth:** CEL replaces all admission webhooks.
  **Truth:** CEL replaces simple per-object validation. Cross-resource validation ("this CR refers to that ConfigMap; check it exists") still needs webhook or K8s's `x-kubernetes-validations` with `variables` referencing other resources (limited). Complex generation/mutation needs Kyverno or webhooks.
- **Myth:** A CRD can have multiple storage versions.
  **Truth:** Exactly one version is `storage: true`. The rest are served versions converted on read/write. Switching storage version requires a migration step (rewrite all CRs) before dropping the old version.
- **Myth:** Conversion webhooks only run during schema migrations.
  **Truth:** They run on *every* read or write of a non-storage version. If a controller still uses v1alpha1 but storage is v1, every reconcile triggers conversion. Latency-sensitive; design webhooks accordingly.

## Recap

A CRD has schema (OpenAPI v3 + CEL validation), versions (one storage + others served), conversion webhook for evolution, status/scale subresources, and printer columns. CEL replaces most validating webhooks. Operator frameworks generate the scaffolding.

**Next — Lesson 42: Operators with Kubebuilder.** The CRD is the data; the operator is the brain. Controller-runtime, Kubebuilder, OLM. NEW: Workshop district.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
