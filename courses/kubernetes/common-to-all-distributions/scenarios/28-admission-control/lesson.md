# Lesson 28 — Admission Control · ValidatingAdmissionPolicy, PSA, Webhooks

> Course: Kubernetes — Common to all distributions
> Module 13 · Security · Lesson 2 of 5
> Companion preview: `/preview-kubernetes-lesson-28.html`.

---

**🎯 If you remember nothing else:** Admission runs *after* auth/RBAC, *before* persistence. **Mutating** admission can rewrite the object (add defaults, inject sidecars). **Validating** admission can accept or reject. Three modern tools: **Pod Security Admission (PSA)** for the standard Pod-security profiles, **ValidatingAdmissionPolicy (VAP)** for CEL-based rules in-cluster (no webhook needed, GA 1.30), and **policy webhooks** (Kyverno, OPA Gatekeeper) for richer logic.

## 1. Where admission sits in the request flow

Walk a write request through the API server:
    
      - **Authentication** establishes the user.

      - **Authorisation (RBAC)** checks if the verb on the resource is allowed.

      - **Mutating admission** — controllers can rewrite the object before it's validated.

      - **Schema validation** — does the object match its CRD/built-in schema?

      - **Validating admission** — final accept/reject by validators.

      - **Persistence** — write to etcd. Done.

    
    Mutating runs first; validating runs last. The order matters: mutators can add fields that validators check. A common pattern: mutating admission injects a default `resources.requests` if the Pod didn't set one; validating admission then enforces "all containers must have requests."
    Built-in admission controllers ship with kube-apiserver: `NamespaceLifecycle`, `ResourceQuota`, `LimitRange`, `PodSecurity` (PSA), `ServiceAccount` (auto-injects the SA token mount), and ~20 others. They run automatically and don't need external infrastructure.

## 2. The successor to PodSecurityPolicy

K8s 1.25 removed **PodSecurityPolicy** (PSP) — the original Pod-level security policy CRD that nobody loved. Replaced by **Pod Security Admission** (PSA): a built-in admission controller, namespace-scoped, configured via labels.
    Three security profiles, ordered by strictness:
    
      - **`privileged`** — "do whatever you want" (= no restrictions).

      - **`baseline`** — disallow known-dangerous things: privileged containers, hostPath, hostNetwork, hostPID. Permits most of what apps actually need.

      - **`restricted`** — strong hardening: must run as non-root, drop ALL capabilities (or all but a small allow-list), seccomp/AppArmor required, read-only root filesystem encouraged. The 80% of workloads that don't need elevation should run here.

    
    For each namespace, set labels:
    `pod-security.kubernetes.io/enforce: restricted
pod-security.kubernetes.io/enforce-version: latest
pod-security.kubernetes.io/audit: restricted
pod-security.kubernetes.io/warn: restricted`
    `enforce` rejects violations. `audit` logs them. `warn` shows them to the user. Most teams ship namespaces with `enforce: baseline` + `warn: restricted` as a transition pattern.

## 3. Custom rules in-cluster, no webhook needed

Pre-VAP, custom admission rules required a **webhook**: a separate Pod the API server calls on every admission. Webhooks add latency, fail-open vs fail-closed tradeoffs, and a chicken-and-egg problem ("the webhook is down, can I deploy a fix?").
    **ValidatingAdmissionPolicy** (alpha 1.26, beta 1.28, GA 1.30) lets you write admission rules in **CEL** (Common Expression Language) and run them *inside the API server*. No webhook, no Pod, no latency. Two CRDs:
    
      - **`ValidatingAdmissionPolicy`** — defines the rule. Selects which resources to apply to. CEL expression returns true (allow) or false (deny).

      - **`ValidatingAdmissionPolicyBinding`** — binds the policy to specific namespaces or label selectors. Same shape as RoleBinding.

    
    Example CEL: "every Deployment must have a `team` label." CEL: `has(object.metadata.labels.team)`. Selector: `resources: ["deployments"]`. Binding: every namespace except `kube-system`. Done — five-line YAML, in-cluster enforcement, zero infrastructure.
    K8s 1.32 added **MutatingAdmissionPolicy** for in-cluster mutation via JSONPatch / CEL — replacing many simple Kyverno mutate policies. By 2026, most teams have migrated their simple validation/mutation rules to VAP/MAP and reserve webhooks (Kyverno, OPA) for cross-cutting policies that need richer logic or external state.
    [ deep dive — skip if new ]The big architectural win of VAP: admission rules are *inspectable*. Operators can `kubectl get validatingadmissionpolicies` and read the CEL. With webhooks, you have to know which Pod implements which rule and read its source. VAP is also the basis for K8s's emerging "policy as data" story — you ship policies as YAML alongside your manifests.

## 4. When CEL isn't enough

VAP/MAP cover most of what teams used to need webhooks for. The remaining cases (richer logic, external lookups, complex state, generation/cleanup, image scanning integration) still call for webhook-based policy engines:
    
      - **Kyverno** — K8s-native; policies as YAML (no DSL). Mutate, validate, generate, cleanup. Most popular in 2026 by deployments.

      - **OPA Gatekeeper** — uses Rego. More flexible, much steeper learning curve. Strong in regulated environments.

      - **Custom webhooks** — write your own. Use only when off-the-shelf tools genuinely can't express your rule.

    
    Webhook gotchas:
    
      - **Fail policy.** If the webhook is unreachable, do you allow the request (`failurePolicy: Ignore`) or block it (`Fail`)? Wrong choice = either security gap or cluster-wide outage.

      - **Latency.** Every admission request waits for the webhook. A slow webhook degrades every `kubectl apply`. Cap timeouts (`timeoutSeconds: 5`).

      - **Self-bootstrapping.** If your webhook validates itself, you can't deploy the webhook. Most policy engines exclude their own namespace; check yours does.

    
    By 2026, the practical pattern: PSA at the security baseline, VAP/MAP for simple custom rules, Kyverno or Gatekeeper for cross-cutting governance. Lesson 29 covers the policy engines in depth.

## Before / After

**Before.** Pre-VAP era: every custom rule was a webhook. Each webhook = a Pod, a Service, certificate management, fail-policy decisions, latency on every admission. Most clusters had 5-10 different webhooks; debugging "why was my Pod rejected" meant chasing logs across pods. PodSecurityPolicy (PSP) was the only built-in security primitive, and it was being removed.

**After.** 2026 stack: PSA at the namespace-label level (no infra). VAP/MAP for custom CEL rules in-cluster (no infra). Kyverno or Gatekeeper for the truly complex stuff. Webhook count goes from 10 to 1-2. Admission decisions are inspectable: `kubectl get vap` shows the rules.

VAP's GA in K8s 1.30 was the most important admission-layer change since admission webhooks were introduced. By 2027, simple webhook-based policy will look anachronistic.

## Analogy — the K-Town district

The Watchtower's admission hallway runs after the identity desk. Three stations along the way. The **stamping desk** (mutating admission) adds default stamps to incoming envelopes — "please add return address, signature, today's date." The envelope keeps moving. The **standards bench** (Pod Security Admission) checks every envelope against three pre-printed standards (privileged / baseline / restricted) — namespaces post their preferred standard at their door. The **custom rules counter** (ValidatingAdmissionPolicy) reads CEL expressions written by the cluster's policy team — "every envelope must have a `team` label" — and stamps yes or no. Past all three, the envelope reaches the filing room (etcd).Two extra rooms behind the counter: a **policy engine office** (Kyverno / OPA Gatekeeper) for rules richer than CEL can handle, and a **webhook switchboard** for the few legacy custom rules. Every desk can stop the envelope; only stamps from the standards bench and custom-rules counter actually *say no*.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The stamping desk | Mutating admission (built-in + webhooks + MutatingAdmissionPolicy) |
| The standards bench | Pod Security Admission (privileged / baseline / restricted) |
| Pre-printed standards on namespace doors | PSA labels: `pod-security.kubernetes.io/enforce` |
| Custom rules counter with CEL slips | `ValidatingAdmissionPolicy` + Binding |
| Policy engine office | Kyverno / OPA Gatekeeper webhooks |
| Filing room | etcd |
| "Stop the envelope" stamp | Validating admission denial |
| "Add stamp before forwarding" | Mutating admission injection |

⚠️ *Analogy stops here:* The analogy stops here: real admission decisions happen in microseconds at the API server. Webhook-based ones add network round-trips; in-cluster (VAP/PSA) ones are virtually free. Pick admission patterns with this perf in mind.

## ELI5 / ELI10

**ELI5.** Before your drawing goes on the fridge, three checks. First: someone adds your name (mutate). Second: it must follow house rules (PSA). Third: it must follow Mom's extra rules (VAP). If any check says no, no fridge.

**ELI10.** Admission runs after RBAC, before etcd. Two phases: **mutating** (rewrite the object — defaults, sidecars, labels) and **validating** (accept/reject). Built-in: PSA (Pod Security Admission, replacing PSP) with three profiles (privileged/baseline/restricted) configured via namespace labels. Custom rules: **ValidatingAdmissionPolicy** (GA 1.30) and **MutatingAdmissionPolicy** (1.32+) using CEL — in-cluster, no webhook. Beyond CEL: Kyverno and OPA Gatekeeper webhooks for cross-cutting governance. Modern stack: PSA + VAP + Kyverno or Gatekeeper covers nearly all needs.

## Real-world scenarios

- **A SaaS enforcing labels via VAP.** VAP requires every Deployment to have `team`, `cost-center`, `environment` labels. CEL: `has(object.metadata.labels.team) && has(object.metadata.labels["cost-center"])`. Bound to every namespace except kube-system. Cost reporting works because every workload has a cost-center label.
- **A bank running PSA at restricted.** Production namespaces have `enforce: restricted`. Workloads must run as non-root, drop ALL capabilities, use seccomp profile `RuntimeDefault`. Pen-test fails repeatedly because nothing privileged can run. Auditor signs off: "the cluster enforces hardening at the API."
- **A startup using Kyverno for image policies.** Kyverno policy: every container image must be from `internal-registry.corp/` or `cgr.dev/chainguard/`. `quay.io/some-random/image` rejected. Combined with VAP for label requirements + PSA for security. Single Kyverno install replaces what used to be five custom webhooks.
- **A team migrating from webhooks to VAP.** Had a webhook enforcing "every Pod must have liveness probe." Migration: rewrote as 4-line VAP CEL. Webhook deleted. `kubectl apply` latency dropped 18ms. Mean Time To Investigate "why was my Pod rejected" dropped to seconds: `kubectl get validatingadmissionpolicies` + read.

## Common misconceptions

- **Myth:** Mutating and validating admission run together.
  **Truth:** They run in two distinct phases. Mutating runs first, validators run after schema check. The two-phase split is intentional: it lets mutators add fields that validators can rely on. *All* mutators run before any validator.
- **Myth:** VAP can't do everything Kyverno does.
  **Truth:** Correct — VAP is intentionally simpler. CEL handles validation and (in MAP) basic JSONPatch mutation. Kyverno adds object generation, cleanup, image verification, complex pattern-matching. Use the right tool: VAP for simple per-object rules; Kyverno/Gatekeeper for cross-cutting flows.
- **Myth:** `failurePolicy: Fail` is always the safer choice for webhooks.
  **Truth:** It's safer for security but riskier for cluster availability. If the webhook Pod crashes during a kube-apiserver restart, no Pod can be created until the webhook recovers — *including the webhook's own Pod*. Most clusters use `Fail` with careful exclusions (kube-system, the webhook's own namespace) and tight Pod redundancy.

## Recap

Admission runs after RBAC, before etcd. Mutating adds defaults; validating accepts/rejects. PSA covers Pod-security baselines via namespace labels. VAP/MAP handle custom CEL rules in-cluster. Kyverno + Gatekeeper handle the rest. Modern admission stacks have far fewer webhooks and far more inspectable policies than 2022.

**Next — Lesson 29: Policy Engines.** Kyverno and OPA Gatekeeper in depth. When to choose which, common policy patterns, the policy-as-code workflow.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
