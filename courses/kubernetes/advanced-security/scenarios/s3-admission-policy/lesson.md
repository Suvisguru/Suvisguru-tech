# K-ADV-SEC S3 — S3 · Admission Policy Architecture

> Course: K-ADV-SEC (advanced specialization)
> Module S3 · Admission Policy
> Companion preview: `/preview-kubernetes-adv-sec-lesson-03.html`.

---

**🎯 If you remember nothing else:** **Hybrid: Kyverno for K8s-native YAML rules; Gatekeeper for OPA/Rego complex logic; ValidatingAdmissionPolicy + CEL inline for hot-path validation. Always roll out policies audit → warn → enforce. PolicyReport unifies feeds.**

## 1. audit → warn → enforce — never ship enforce on day one

K8s admission webhooks operate in three modes per policy: **audit** (record violations; don't block), **warn** (return warnings to `kubectl` output; don't block), **enforce** (block the request). Roll every new policy through the lifecycle:
    
      - **Audit (1-2 weeks)**: deploy in audit mode; collect violations from PolicyReport / metrics; review false positives + edge cases.

      - **Warn (1-2 weeks)**: enable warn; teams see the rule in their `kubectl apply` output; complaints surface before they become incidents.

      - **Enforce**: block. Document the policy + waiver path before flipping.

    
    Skip steps and you ship outages. Slow rollouts catch the policy that's right in theory and wrong in practice.

## 2. K8s-native YAML rules; mutating / validating / generating

**Kyverno** is policy-as-K8s-CRDs. You write `ClusterPolicy` / `Policy` objects with `match` selectors + `rules` using JMESPath expressions over the resource. Rule kinds:
    
      - **mutate**: patch the object (set defaults, add labels, inject sidecars). E.g., "every Pod gets `resources.requests.cpu: 100m` if missing."

      - **validate**: pass/fail check (return failed message). E.g., "every Pod must have `imagePullPolicy: Always`."

      - **generate**: create downstream resources triggered by parent (e.g., new Namespace → auto-create default NetworkPolicy + ResourceQuota).

      - **verifyImages**: image-signature check via Cosign / Sigstore (covered in S5).

    
    Kyverno wins for: K8s-shop teams; rules that are mostly K8s-resource-shaped; teams not wanting to learn Rego. Performance: webhook latency typically <50ms per request.

## 3. ConstraintTemplate + Constraint; formal logic in Rego

**Gatekeeper** is OPA (Open Policy Agent) wrapped as a K8s admission controller. You author:
    
      - **ConstraintTemplate**: a CRD definition + Rego policy logic (e.g., template "K8sRequiredLabels" with Rego logic).

      - **Constraint**: an instance of the template with parameters (e.g., "K8sRequiredLabels: required labels = [team, cost-center]; match Pods").

    
    Rego shines on **cross-resource logic**: "this Service can only target Pods labelled X if those Pods exist in this list of allowed namespaces — and the source Pod's SA must be in that list." Rego is a real query language; Kyverno's JMESPath is more limited. Gatekeeper wins for: complex correlations, formal-logic-heavy compliance, teams already invested in OPA.
    Trade-off: Rego is a learning curve. For a typical K8s team, 80% of policies are K8s-shape and Kyverno is faster to author; the 20% that are complex go to Gatekeeper.

## 4. Inline policy without a webhook + unified reporting

**ValidatingAdmissionPolicy** (K8s 1.30+ stable) lets you write validation rules in **CEL (Common Expression Language)** directly in K8s objects — *no webhook*. The apiserver evaluates them inline. *Major win*: zero webhook latency, no extra component to operate, no webhook outage risk. Use for hot-path rules where every millisecond counts (admission to a high-throughput cluster).
    Limits: CEL is simpler than Rego or JMESPath — no calls to external data, no cross-resource lookups within one rule. For complex needs, stick with Kyverno / Gatekeeper.
    **PolicyReport CRD** (Kyverno + Gatekeeper both write to it): one cluster-wide unified report of policy results per resource. Compliance dashboards query PolicyReports; engineers see violations in one place; SIEM ingestion is uniform.
    **Hybrid pattern**: 70% policies in Kyverno (ergonomic + K8s-native), 20% in Gatekeeper (complex logic), 10% in ValidatingAdmissionPolicy (hot-path latency-sensitive). Each engine reports to PolicyReport. Compliance + ops see one view.

## Before / After

**Before.** Pre-policy clusters had documentation "please add resource limits" + occasional code review. Drift was constant. Compliance evidence was "trust us" + a sample of YAML files. Bad images, missing labels, privileged Pods all slipped through.

**After.** Modern admission applies policy at apiserver: every request mutated + validated; PolicyReport tracks every decision; compliance evidence is automatic + queryable; engineers see violations in `kubectl apply` output. Hybrid Kyverno + Gatekeeper + CEL covers the spectrum from K8s-shape to complex to hot-path.

*Pick the engine to fit the rule, not the other way around. And always audit before enforcing.*

## Analogy — the K-Citadel bastion

The Checkpoint Gates are three desks at the second wall. The first desk (**mutating**) hands every visitor a standard-issue helmet + name tag (defaults + labels) before they pass through. The second desk (**validating**) checks the visitor's papers against the rule book — pass or fail. A third desk (**generating**) emits side-effect paperwork (auto-create NetworkPolicy when a new Namespace appears).
    Two rule-book authors share the work. One writes in plain K8s ergonomic syntax (Kyverno YAML + JMESPath). The other writes in formal-logic ledger (Gatekeeper / Rego) for the complex rules. Both append to a single archive (**PolicyReport CRD**) so compliance can audit one shelf.
    A new rule is never enforced overnight — it goes through three phases: **audit** (shadow log), **warn** (visitors see a yellow note), **enforce** (visitor turned away at gate).

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Standard-issue helmet + name tag | Kyverno mutate (defaults + labels) |
| Rule-book check (pass/fail) | Kyverno / Gatekeeper validate |
| Side-effect paperwork | Kyverno generate (auto-create resources) |
| K8s-ergonomic rule book | Kyverno YAML + JMESPath |
| Formal-logic ledger | Gatekeeper OPA / Rego |
| Inline gate-check (no helper desk) | ValidatingAdmissionPolicy + CEL |
| Single audit shelf | PolicyReport CRD |
| Shadow log | audit mode |
| Yellow warning slip | warn mode |
| Gate-turn-away | enforce mode |

⚠️ *Analogy stops here:* A real gate-keeper checks one document; admission webhooks evaluate every rule on every API call (potentially thousands per minute). Webhook latency adds up — keep policies tight or move to ValidatingAdmissionPolicy + CEL.

## ELI5 / ELI10

**ELI5.** Three desks at the gate. The first hands you a helmet so you're always equipped. The second checks your papers against the rule book. The third writes paperwork for what your visit triggers. Different rule books exist for K8s-shape rules vs complex logic vs latency-sensitive rules. Your cluster does the same.

**ELI10.** **Three engines**: Kyverno (K8s-native YAML + JMESPath; mutate/validate/generate/verifyImages), Gatekeeper (OPA + Rego; complex logic), ValidatingAdmissionPolicy + CEL (inline, no webhook, hot-path). **PolicyReport CRD** unifies results. **Lifecycle**: audit → warn → enforce, weeks each. **Hybrid pattern**: 70/20/10 Kyverno/Gatekeeper/CEL.

## Real-world scenarios

- **Kyverno default — every Pod gets resource requests.** A platform team ships a Kyverno mutate rule: every Pod with no `resources.requests.cpu` gets `100m`; no `requests.memory` gets `128Mi`. *Audit → warn → enforce* over 4 weeks. PolicyReport tracked. Cluster baseline now sane; capacity planning works.
- **Gatekeeper formal logic — Service-to-Namespace correlation.** A regulated cluster requires "a Service's selector may only target Pods in a namespace listed in the Service's allowed-targets annotation." Cross-resource correlation; Kyverno's JMESPath struggles; Gatekeeper Rego handles it cleanly. ConstraintTemplate ships once; per-Service Constraint declares the allowed-targets list.
- **ValidatingAdmissionPolicy + CEL hot-path.** A 1000-rps internal cluster API needs every PUT to validate one field. Webhook latency would add ~30ms per request — 30 seconds of cumulative latency per second. ValidatingAdmissionPolicy + CEL evaluates inline, ~0ms. Teams adopt for the latency-sensitive policies.
- **Outage — enforced on day one.** A team enabled "every Pod requires team label" enforce immediately. Existing CI tooling didn't set the label; deploys broke cluster-wide. 90-min outage. Postmortem: every new policy walks audit → warn → enforce; the team's runbook now requires evidence of audit-period violation count before enforcing.

## Common misconceptions

- **Myth:** "Pick one engine — Kyverno OR Gatekeeper, not both."
  **Truth:** **Hybrid is the standard pattern.** Kyverno for ergonomic K8s rules, Gatekeeper for complex logic, ValidatingAdmissionPolicy + CEL for hot-path. PolicyReport unifies the feeds. Forcing one engine for everything = either dumbed-down policies (Kyverno-only for complex needs) or pain (Gatekeeper for trivial rules).
- **Myth:** "ValidatingAdmissionPolicy + CEL is just a stripped-down Kyverno."
  **Truth:** It's *inline in the apiserver* — no webhook, no extra latency, no extra component to operate. For hot-path or simple rules, it's the right tool. CEL is more limited than JMESPath/Rego; for complex needs, Kyverno or Gatekeeper still win.
- **Myth:** "Audit mode is for the audit team; engineers don't need it."
  **Truth:** Audit mode is for *every team rolling out a policy*. It's the calibration phase — find false positives, edge cases, missing exemptions. Skip it and the policy that's right in theory ships incidents in practice.

## Recap

Three admission engines, three roles. Kyverno for K8s-native ergonomics; Gatekeeper for formal-logic complex correlation; ValidatingAdmissionPolicy + CEL for hot-path inline. PolicyReport unifies. Audit → warn → enforce. The hybrid pattern is the answer.

**Next — S4: PSA Restricted + runtime detection.** Pod Security Admission migration playbook (privileged → baseline → restricted); Falco / Tetragon eBPF-based runtime detection at scale; alert pipelines.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
