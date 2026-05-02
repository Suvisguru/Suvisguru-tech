# Lesson 27 — RBAC & Authentication · Roles, Bindings, OIDC, Structured Auth

> Course: Kubernetes — Common to all distributions
> Module 13 · Security · Lesson 1 of 5
> Companion preview: `/preview-kubernetes-lesson-27.html`.

---

**🎯 If you remember nothing else:** Two checks: **authentication** (who are you?) and **authorisation** (RBAC: verb on resource for subject). Authentication is plug-in: OIDC for humans, ServiceAccount tokens for Pods, certs/webhooks for special cases. RBAC has four objects: **Role** + **RoleBinding** (namespace-scoped), **ClusterRole** + **ClusterRoleBinding** (cluster-wide). First match wins; if no rule allows, the request is denied.

## 1. Every API request is a 4-tuple

Every request to the kube-apiserver gets reduced to four things: **subject** (who is asking), **verb** (what they want to do — get/list/watch/create/update/patch/delete), **resource** (what kind of thing — pods, secrets, deployments, etc.), **scope** (cluster-wide or specific namespace). The API server runs each request through two stages:
    
      - **Authentication** turns the request into a subject (user identity). "Who is asking?" Plug-in: OIDC, ServiceAccount tokens (TokenRequest API), client certs, static tokens (deprecated), bootstrap tokens, webhook authenticators.

      - **Authorisation** takes the subject + verb + resource + scope and asks: "is this allowed?" K8s ships with one primary authorizer: **RBAC** (others exist — Node, ABAC, Webhook — but RBAC is the bread and butter).

    
    If authorisation says yes, the request goes to **admission** (Lesson 28). If anywhere in this chain says no, the request is rejected with a clean 401/403.

## 2. Roles + Bindings, namespace and cluster

📋
        Role
        namespace-scoped permissions
        A list of rules: "`verbs: [get, list, watch]` on `resources: [pods, services]`." Lives in a namespace; rules apply only to that namespace's resources.
        Use for: per-team or per-app permissions inside a namespace.
      
      
        🔗
        RoleBinding
        grants a Role to subjects
        Maps subjects (User, Group, ServiceAccount) to a Role. The binding lives in the same namespace as the Role; subjects can be from any namespace.
        Use for: "this team's SA gets these permissions in their namespace."
      
      
        🏛️
        ClusterRole
        cluster-wide permissions
        Same shape as Role, cluster-scoped. Can list cluster-scoped resources (nodes, persistentvolumes, namespaces themselves) *and* can be referenced by RoleBindings to grant rights inside one namespace without redefining rules.
        Use for: cluster-admin roles, reusable role definitions, scraping-style permissions (read all Pods cluster-wide).
      
      
        🌐
        ClusterRoleBinding
        grants a ClusterRole cluster-wide
        Maps subjects to a ClusterRole at cluster scope. Subject can do whatever the ClusterRole says, in every namespace + cluster-wide resources.
        Use for: cluster-admin grants, infra controllers, monitoring agents.
      
    
    **Key principle:** RBAC is purely additive. There are no Deny rules. If no Role grants the verb on the resource, the request is denied. If you want to revoke, you remove the binding (or restrict the Role's verbs).

## 3. From flag soup to structured auth config

K8s historically configured auth via API-server flags: `--oidc-issuer-url`, `--oidc-client-id`, `--oidc-username-claim`, … one OIDC issuer per cluster, no easy way to add a second, no way to express "if username matches X then claim Y means Z." The **Structured Authentication Configuration** (alpha 1.29, beta 1.30, GA 1.32) replaces all that with a YAML file.
    What it gets you:
    
      - **Multiple JWT issuers** in one cluster — corp OIDC + GitHub OIDC + Google Workspace, each with its own claim mapping.

      - **CEL expressions** for username and group derivation. "username = email if domain matches corp.com else email + ':external'".

      - **Audience-bound** issuer validation — protect against token confusion attacks.

      - **Hot reload** — change the config, API server picks it up without restart.

    
    Authentication mechanisms in 2026 (in priority of usage):
    
      - **OIDC** (humans) — corp SSO, GitHub, Google Workspace. Every CI tool integrates.

      - **ServiceAccount tokens** (Pods) — projected, bound, short-lived. See Lesson 21.

      - **X.509 client certs** — cluster admins, kubeadm bootstrap. CN = username; O = group.

      - **Webhook authenticator** — defer to an external service. Useful for IAM-style integration.

      - **Static tokens** — DEPRECATED. Don't use in new clusters.

## 4. What good cluster RBAC looks like

Three rules every team should follow:
    
      - **Least privilege.** A Pod that reads ConfigMaps doesn't need `list, watch, create, update, patch, delete`. It needs `get`. Audit your SA bindings; tighten them.

      - **One ServiceAccount per workload.** Don't let unrelated workloads share the same SA — a bug in one becomes a permission inheritance issue for the other. The `default` SA in every namespace should be permissionless (no RoleBindings).

      - **Avoid `*` verbs.** `verbs: ["*"]` means every verb K8s adds in the future automatically applies. Spell out the verbs you want.

    
    Common mis-grants to watch for:
    
      - `cluster-admin` grants — review every ClusterRoleBinding to `cluster-admin`. Each one is the keys to the kingdom.

      - `secrets` read access in unexpected places. Auditors love finding controllers that have read access to all Secrets when they only need a few.

      - `pods/exec` grants — anyone who can `exec` can effectively do whatever a Pod can do. Tight scope these.

      - Wildcard resource grants — `resources: ["*"]` grants access to every K8s resource, including future CRDs.

    
    [ deep dive — skip if new ]Run `kubectl auth can-i --list --as=system:serviceaccount:foo:bar` to enumerate everything an SA can do. `rakkess` and `rbac-tool` are popular utilities for visualising the full RBAC graph. Most production clusters benefit from running these as part of CI on every RBAC change — the diff catches accidentally-overpermissioned bindings before they merge.

## Before / After

**Before.** Pre-OIDC, pre-bound-tokens era: `kubectl create clusterrolebinding` with hand-crafted ServiceAccount tokens, kubeconfigs distributed via Slack, the same cluster-admin token shared across the team. Auth flags hard-coded into kube-apiserver; one OIDC provider only. "Quick tests" granted permanent cluster-admin to default SAs. *The default attacker objective: find an over-permissioned default SA.*

**After.** OIDC for humans (corp SSO + audit), bound tokens for Pods, structured auth config for cleaner setup, RBAC reviewed in CI via `rakkess` and policy reports. Default SA in every namespace: permissionless. Pen-test finds nothing interesting on the default SA path.

RBAC is the API server's most under-appreciated feature: by being purely additive (no deny rules), it's simple to reason about. The complexity is in your bindings, not in the model.

## Analogy — the K-Town district

Watchtower stands at the edge of K-Town: the city's identity-and-permissions bureau. Two checkpoints, in order. The **identity desk** verifies who you are — corp employee badge (OIDC), Pod license plate (ServiceAccount token), notarised letter of introduction (client cert), or a third-party endorsement (webhook authenticator). The **permissions desk** consults a binder of *roles* — each role lists "verbs you can perform on resources you can touch" — and a binder of *bindings* mapping people and Pods to roles.Two scopes. The **district binder** (Role + RoleBinding) covers permissions inside one neighbourhood. The **city binder** (ClusterRole + ClusterRoleBinding) covers the whole city plus the city-wide registries. Permissions are *additive*: no role binder ever has a "no" rule. If your role doesn't grant the verb, the answer is no by default. If you want to revoke, the desk tears your binding out of the binder.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The identity desk | Authentication (OIDC, SA tokens, certs, webhooks) |
| Corp employee badge | OIDC token from corp SSO |
| Pod license plate | ServiceAccount projected JWT |
| The district binder | `Role` + `RoleBinding` |
| The city-wide binder | `ClusterRole` + `ClusterRoleBinding` |
| "Verbs on resources" rule | RBAC rule: `verbs: [...]` on `resources: [...]` |
| "No" rules don't exist; revoke = tear out binding | Additive-only RBAC; no Deny rules |
| "Quick test" cluster-admin grant from 3 years ago | Stale ClusterRoleBinding to cluster-admin |
| New, cleaned-up identity desk software | Structured Authentication Configuration (GA 1.32) |

⚠️ *Analogy stops here:* The analogy stops here: real RBAC is a programmatic match against verbs/resources/names — there's no human reading a binder. And authentication isn't "checking a badge"; it's cryptographic verification of a signed token, with all the implications about key rotation and replay.

## ELI5 / ELI10

**ELI5.** Two doors. The first asks: who are you? Show your badge. The second asks: are you allowed to do this thing here? Look at the binder. If your name and the thing aren't both in the binder, sorry — you can't.

**ELI10.** Every API request: authenticate (who?) → authorise (allowed?). Authentication is plug-in: OIDC, SA tokens (modern bound JWTs), client certs, webhooks. Authorisation is mostly RBAC: `Role` + `RoleBinding` (namespace) and `ClusterRole` + `ClusterRoleBinding` (cluster). Rules are *additive* — no Deny. First match wins. Structured Auth Config (GA 1.32) lets you configure multiple OIDC issuers and CEL-based claim mapping in one YAML file. Modern best practice: OIDC for humans, bound SA tokens for Pods, default SAs permissionless, one SA per workload, audit RBAC graphs in CI.

## Real-world scenarios

- **A SaaS using corp SSO via OIDC.** Structured Auth Config maps email → user, Okta groups → K8s groups. Cluster admins are in the `k8s-cluster-admins` Okta group. Adding/removing admins is an Okta change, not a kubeconfig redistribution. Audit logs show every API call by corp username. SOC2 happy.
- **A bank running zero shared kubeconfigs.** Every developer authenticates via OIDC. `kubectl` uses the OIDC client plugin; tokens last 1 hour, refreshed silently. No shared static tokens exist anywhere. When a developer leaves the org, they're removed from Okta; their cluster access ends within minutes.
- **A startup that audits RBAC in CI.** Every PR touching a `RoleBinding` or `ClusterRoleBinding` runs `rbac-tool` + `kubectl auth can-i --list` diff. PR description requires explaining permission additions. The platform team has caught two cluster-admin grants that would have bypassed every other security control.
- **A team using webhook authn for AWS IAM identity.** Webhook authenticator integrates with AWS IAM; `eks-iam-authenticator` validates an AWS-signed token and returns an identity. K8s RBAC sees "`arn:aws:iam::123:role/PlatformEng`" as a username; bindings reference it. AWS-side IAM changes propagate to K8s instantly.

## Common misconceptions

- **Myth:** RBAC has Deny rules.
  **Truth:** It doesn't. RBAC is purely additive. Anything not explicitly allowed is denied by default. To "deny" something, you remove the binding that grants it. If you need true deny semantics (block specific operations even if other rules allow), use admission control (ValidatingAdmissionPolicy / Kyverno / OPA) — covered in Lesson 28.
- **Myth:** The `default` ServiceAccount in every namespace is harmless.
  **Truth:** It's harmless only if no RoleBindings reference it. By default, K8s ships `default` with no permissions. Many teams accidentally add bindings for "convenience" — these become privilege-escalation footholds. Pod Security Admission can enforce "must specify a non-default SA."
- **Myth:** `cluster-admin` is a normal role.
  **Truth:** It's the highest-privilege role: `verbs: ["*"]` on `resources: ["*"]` on all `apiGroups: ["*"]`. Anyone bound to it can do anything in the cluster. Treat every `ClusterRoleBinding` to `cluster-admin` as critical infrastructure; review them quarterly.

## Recap

Authentication answers "who?"; RBAC answers "can you do this?". Four objects: Role / RoleBinding (namespace) and ClusterRole / ClusterRoleBinding (cluster). Additive only. OIDC for humans, bound SA tokens for Pods, default SAs permissionless, one SA per workload.

**Next — Lesson 28: Admission Control.** When RBAC says yes, the request goes through admission. ValidatingAdmissionPolicy (in-cluster CEL), Pod Security Admission (PSA), webhook admission, mutation. The Watchtower interior.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
