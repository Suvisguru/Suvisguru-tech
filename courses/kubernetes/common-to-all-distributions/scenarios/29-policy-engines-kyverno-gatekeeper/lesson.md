# Lesson 29 — Policy Engines · Kyverno and OPA Gatekeeper in Depth

> Course: Kubernetes — Common to all distributions
> Module 13 · Security · Lesson 3 of 5
> Companion preview: `/preview-kubernetes-lesson-29.html`.

---

**🎯 If you remember nothing else:** **Kyverno** uses K8s-native YAML for policies (validate / mutate / generate / cleanup / verifyImages). **OPA Gatekeeper** uses Rego (more powerful, harder to learn) via `ConstraintTemplate` + `Constraint`. Both produce **PolicyReport** CRDs (a CNCF standard). Pick Kyverno for K8s-only governance; pick Gatekeeper if you already run OPA for non-K8s policy.

## 1. What a policy engine actually does

A policy engine plugs into K8s admission as a webhook (validating + mutating). On every request, it consults its policy library and replies allow / deny / mutate. That replaces hand-rolled webhooks with a **declarative, auditable** policy library managed in git.
    Five common policy capabilities (Kyverno + Gatekeeper both cover most of them):
    
      - **Validate** — accept / reject based on object content. "Pods must have liveness probes."

      - **Mutate** — rewrite objects. "Inject default topology-spread constraints."

      - **Generate** — create related objects on triggers. "When a new namespace is created, create a NetworkPolicy in it."

      - **Cleanup** — delete stale objects. "Delete completed Jobs older than 7 days."

      - **Verify images** — check image signatures (cosign / Sigstore) and SBOM presence.

    
    Both engines write reports as **PolicyReport** CRDs (a CNCF Policy WG standard) — every namespace gets a list of pass/fail/warn results. This is your audit evidence: `kubectl get policyreport -A`.

## 2. YAML policies, no DSL to learn

Kyverno was designed K8s-first: policies look like K8s manifests. No new language to learn. The four policy CRDs:
    
      - `ClusterPolicy` / `Policy` — the rule definitions. Cluster or namespace scope.

      - `PolicyException` — explicit exclusions for specific namespaces / workloads. Auditable.

      - `ClusterCleanupPolicy` / `CleanupPolicy` — scheduled deletion rules.

      - `VerifyImages` — cosign / Sigstore image verification.

    
    A typical Kyverno rule:
    `apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: require-team-label}
spec:
  validationFailureAction: Enforce
  rules:
  - name: require-team
    match: {any: [{resources: {kinds: [Deployment]}}]}
    validate:
      message: "Deployment must have a 'team' label"
      pattern:
        metadata:
          labels:
            team: "?*"`
    Patterns use simple wildcards: `?*` = required + non-empty, `?*` = required, etc. For richer logic, Kyverno supports JMESPath and (from v1.11) CEL expressions. The K8s-native feel is its biggest strength: ops engineers can write policies the day they install it.

## 3. Maximum flexibility, steep learning curve

Open Policy Agent (OPA) is a general-purpose policy engine — not K8s-specific. **Gatekeeper** is OPA's K8s integration. Policies are written in **Rego**, a declarative logic language. Two CRDs:
    
      - **`ConstraintTemplate`** — defines a policy *type* with parameters and Rego logic. "This template enforces that images come from certain repos; the repos are a parameter."

      - **`Constraint`** — instances of a template with specific parameters. "For namespace A, images must come from `internal/` or `cgr.dev/`."

    
    Rego excerpt for the same image-repo policy:
    `package k8sallowedrepos
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not any_match(container.image)
  msg := sprintf("image %v from disallowed repo", [container.image])
}
any_match(image) {
  startswith(image, input.parameters.repos[_])
}`
    Rego is more powerful than CEL or JMESPath — it can do unification, recursion, complex query logic. The downside: most ops engineers don't know it, and debugging Rego is harder. Gatekeeper shines in regulated environments that already use OPA for non-K8s policy (Terraform, IAM, microservice authz).

## 4. When you should pick which

The 2026 guidance:
    
      - **Use Kyverno when:** K8s is your only policy domain; ops engineers (not platform engineers) own the policies; you want to ship policies the same week you install the engine.

      - **Use OPA Gatekeeper when:** You already run OPA for non-K8s things (Terraform validation, microservice authz); you have engineers who know Rego; you need policy logic CEL/JMESPath can't express.

      - **Use both when:** You're a large org with separate domains. Most don't need this.

    
    The policy-as-code workflow (works for both):
    
      - **Policies in git.** One repo, with PR review for every change. Policies as YAML files; CI runs `kyverno test` or Gatekeeper's test framework against fixture inputs.

      - **GitOps deploy.** Argo CD or Flux applies policies. Same workflow as any other K8s manifest.

      - **Audit reports.** `kubectl get policyreport -A -o jsonpath` dumps the current state. Pipe to your dashboard / SIEM.

      - **Exemption process.** When a workload genuinely needs an exception, file a `PolicyException` (Kyverno) or scope a Constraint differently (Gatekeeper). Exceptions are first-class objects, not exceptions in code.

    
    [ deep dive — skip if new ]The CNCF Policy Working Group standardised PolicyReport in 2023; both Kyverno and Gatekeeper emit them. This means downstream tooling (Falco for runtime alerts, custom dashboards, Grafana panels) can consume policy results from *any* engine without engine-specific code. Even custom webhook policies can produce PolicyReport CRDs to participate in this ecosystem.

## Before / After

**Before.** Pre-policy-engine era: every policy was a hand-rolled webhook (Go service + cert management + Pod redundancy + ad-hoc tests). Each policy = a project. Auditors ask "show me your enforced rules" → you point at a Confluence page. Exceptions live in YAML comments and tribal memory.

**After.** Modern: one Kyverno or Gatekeeper install. Policies as YAML in git, deployed via GitOps. `kubectl get policyreport` shows current state. Exceptions are `PolicyException` objects with PR review history. Auditors get a dashboard, not a wiki.

Policy engines + GitOps + PolicyReport is the cleanest compliance story K8s has ever had. The bar of evidence is now "show me the YAML and the report," not "explain your process."

## Analogy — the K-Town district

Watchtower expanded its admission hallway from Lesson 28 with a full **policy library**. Two cabinets stand side by side. The **Kyverno cabinet** holds rules in plain K-Town vernacular: "Deployment must have a team label." Anyone who can read a Permit Office form can read a Kyverno rule. The **OPA Gatekeeper cabinet** holds rules in a more powerful — but harder to read — formal logic language (Rego), in two parts: a *template* describing the rule's shape, and *instances* with the specific values for this cluster. Both cabinets produce identical filing reports (PolicyReport CRDs), which makes the auditor's job easy: same form regardless of which cabinet wrote the rule.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Plain-K-Town-vernacular cabinet | Kyverno |
| Formal-logic cabinet (Rego) | OPA Gatekeeper |
| Rule template + instances split | `ConstraintTemplate` + `Constraint` |
| Standard filing report | `PolicyReport` CRD |
| Mutation: "add this stamp before forwarding" | Kyverno mutate / generate |
| Image-signature checking machine | `verifyImages` with cosign |
| "Excluded by special permit" | `PolicyException` object |
| Cabinet contents in git, deployed by GitOps | Policy-as-code workflow |

⚠️ *Analogy stops here:* The analogy stops here: real policy engines are admission webhooks performing decisions in milliseconds. Their evaluation is bounded — Rego with deeply nested logic can be slow; Kyverno patterns can't express recursion at all. Pick complexity to match what you actually need.

## ELI5 / ELI10

**ELI5.** Two big rule-books for what's allowed in the building. One is in plain English. One is in lawyer language. Both produce the same report when an inspector visits.

**ELI10.** Policy engines plug into K8s admission and centralise rules. **Kyverno**: K8s-native YAML, no DSL, validate/mutate/generate/cleanup/verifyImages. **OPA Gatekeeper**: Rego-based, more powerful, harder to learn, two-CRD model (ConstraintTemplate + Constraint). Both emit standard PolicyReport CRDs for audit. Picked by org context: Kyverno for K8s-only with ops-team ownership; Gatekeeper for orgs with existing Rego/OPA. Workflow: policies in git → GitOps → PolicyReport audit → PolicyExceptions for the rare opt-out.

## Real-world scenarios

- **A SaaS using Kyverno for governance.** 20 ClusterPolicies covering: required labels, NetworkPolicy generation per namespace, image-repo allow-list, cosign image verification, Job cleanup after 7 days, sidecar injection. Total YAML: ~600 lines in git. Auditor reads the policies directly; spends 30 minutes confirming, calls it a day.
- **A bank running Gatekeeper for cross-domain policy.** Gatekeeper enforces K8s admission. Same Rego library used by their Terraform-pipeline-Conftest setup for IaC validation. One source of truth for policy logic across IaC + cluster admission. Compliance team trained once, applies everywhere.
- **A startup migrating from custom webhooks.** Six hand-rolled validating webhooks, total 3000 LoC of Go. Replaced by 12 Kyverno policies (~250 lines YAML). Engineering hours saved per month: 8. Number of admission outages: dropped to zero (the webhooks used to crash occasionally during deploys; Kyverno is robust).
- **A team using Kyverno verifyImages with cosign.** ClusterPolicy verifies every image is signed by the org's cosign public key. Build pipeline signs on push. Unsigned images = rejected at admission. Catches: leaked image-pull credentials being used to run an attacker image. Real incident found in audit logs after policy was installed.

## Common misconceptions

- **Myth:** Kyverno is just for simple cases; Gatekeeper is for serious work.
  **Truth:** Kyverno covers ~90% of typical policies, including image verification + signature checks. "Serious" depends on what you mean — for K8s-only, both are equally serious. Gatekeeper's edge is multi-domain orgs already using OPA.
- **Myth:** VAP replaces Kyverno / Gatekeeper.
  **Truth:** VAP/MAP cover simple per-object rules. For generation, image verification, cleanup, cross-object validation, you still need a policy engine. The 2026 stack is VAP/MAP + Kyverno/Gatekeeper, not one or the other.
- **Myth:** Policies in git = policies that work.
  **Truth:** Policies must be tested. Both Kyverno (`kyverno test`) and Gatekeeper (`gator`) ship test frameworks. Without tests, a renamed field in K8s upstream silently breaks your policies — and you discover it during incidents.

## Recap

Policy engines centralise admission rules as code. Kyverno (YAML) for K8s-only governance; Gatekeeper (Rego) for OPA-heavy orgs. Both emit PolicyReports for audit. Workflow: policies in git → GitOps → reports → exceptions as objects.

**Next — Lesson 30: Supply Chain Security.** The other half of trust: are the images you're running what you think they are? Cosign, Sigstore, SLSA, SBOMs, attestations. Bank Vault Quarter — the trust ledger.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
