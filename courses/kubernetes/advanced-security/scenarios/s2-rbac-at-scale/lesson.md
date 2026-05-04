# K-ADV-SEC S2 — S2 · RBAC Design at Scale

> Course: K-ADV-SEC (advanced specialization)
> Module S2 · RBAC at Scale
> Companion preview: `/preview-kubernetes-adv-sec-lesson-02.html`.

---

**🎯 If you remember nothing else:** **RBAC = subject + role + binding. Use ClusterRole-aggregation for composability. Map OIDC groups to Roles, never to cluster-admin. Run audit-driven narrowing (audit2rbac) quarterly. Default-deny is the cluster's posture; cluster-admin is reserved for break-glass.**

## 1. Subject, Role / ClusterRole, RoleBinding / ClusterRoleBinding

**Subject** is who is asking — User (typically OIDC-authenticated humans), Group (an OIDC claim), or ServiceAccount (Pod identity). The apiserver resolves the subject from the request's authentication.
    **Role** (namespaced) and **ClusterRole** (cluster-scoped) declare *verbs on resources* — e.g., `get/list/watch on pods`. Verbs: get, list, watch, create, update, patch, delete, deletecollection, plus subresource verbs (`pods/exec`, `pods/log`). Resources can be wildcarded (`*`) but rarely should be.
    **RoleBinding** ties a subject to a Role *within one namespace*. **ClusterRoleBinding** ties a subject to a ClusterRole *across the whole cluster*. A ClusterRole can also be referenced by a RoleBinding to grant the ClusterRole's verbs *in just that namespace* — composable.

## 2. Built-in admin / edit / view + custom aggregation

K8s ships four **built-in ClusterRoles**: `cluster-admin` (god mode — all verbs all resources), `admin` (all verbs all resources within a namespace), `edit` (read+write most resources, no RBAC), `view` (read-only most resources). For most teams: bind `edit` or `view`, never `cluster-admin`.
    **Aggregation**: ClusterRoles can declare `aggregationRule.clusterRoleSelectors` matching label selectors; the apiserver merges all matching ClusterRoles' rules. Pattern: ship a CRD with a small ClusterRole carrying the CRD's verbs + label `rbac.authorization.k8s.io/aggregate-to-edit: true` — automatically rolled into `edit`. Operators do this; you can too.
    **Custom aggregation**: build platform-specific roles (`platform-developer`, `platform-readonly`) by aggregating finer-grained ClusterRoles. Bind groups (e.g., OIDC group `devs`) to these aggregated roles instead of bespoke RoleBindings per Service.

## 3. Humans via OIDC, workloads via SA — different patterns

**OIDC for humans**: configure apiserver flags to trust an OIDC issuer (Okta / Auth0 / Keycloak / Google / Azure AD). Tokens carry `sub` (user) + `groups` (claim mapped to K8s groups). RoleBindings reference groups (e.g., `oidc-group:platform-engineers`) — *never bind to individuals*; group membership is the abstraction.
    **ServiceAccount tokens**: every Pod has one (default = `default` SA in its namespace). *Disable auto-mount* on the default SA (`automountServiceAccountToken: false`) and create per-workload SAs with explicit RoleBindings. **Projected SA tokens** (audience-scoped, short-lived, auto-rotating) are the modern pattern; replace static SA tokens.
    **Service-to-API patterns**: an app calling the K8s API uses its Pod's SA. Scope the SA to *only the verbs on the resources the app actually calls*. Common over-grant: an app reads ConfigMaps but its SA has `configmap:*` (write too) — narrow to `get,list`.

## 4. audit2rbac, rakkess, kubectl-who-can, periodic narrowing

At 30+ services, RBAC drift is inevitable without tooling.
    
      - **rakkess** (`kubectl access-matrix`): show what every SA / user can do across resources. Find over-broad bindings.

      - **kubectl-who-can**: "who can  ?" — quickly find dangerous bindings.

      - **audit2rbac**: from audit logs, generate the *minimum* RBAC rules a workload actually used. Run during a representative period; replace the SA's broad RoleBinding with the generated narrow one.

      - **krew rbac-tool**: visualise binding graphs; find unused; lookup permissions per subject.

    
    **Quarterly narrowing playbook**: (1) Pull audit logs for past 90 days. (2) Per Service / SA, run audit2rbac to compute used permissions. (3) Diff against current binding — flag delta as candidate to remove. (4) Apply in dev / staging; observe one week; promote to prod. (5) Document the cut in change log. *Bind permissions you need; remove what you don't.*

## Before / After

**Before.** Pre-disciplined-RBAC, teams bound `cluster-admin` to every developer, every CI runner, every operator. SAs auto-mounted at default. Tokens were long-lived. Bindings drifted as new things were added; nothing was ever removed. Audit findings: dozens of unjustified cluster-admin bindings; no clear who-can-do-what story.

**After.** Modern RBAC: OIDC groups bound to aggregated platform roles; per-workload SAs with audit2rbac-narrowed bindings; auto-mount disabled on default SA; projected short-lived tokens; periodic narrowing reviews. *Audit can answer "who can call DELETE on Secrets" in 60 seconds.*

*Bind groups, not people. Bind narrow Roles, not cluster-admin. Run audit2rbac every quarter.*

## Analogy — the K-Citadel bastion

The Authorization Desk is the second wall of the Citadel. Every visitor presents a citizenship paper (subject), the gate-keeper consults a ledger of **verbs** (Role) — "may enter the courtyard, may read the registry, may not approach the vault" — and a **binding scroll** (RoleBinding) names which gate this verb-list applies at.
    Three desks share the load. The **citizenship desk** identifies (OIDC + SA tokens + mTLS). The **verb desk** records what each role may do (Roles + ClusterRoles). The **binding desk** assigns ledger pages to gate-keepers (RoleBindings). Aggregation lets one verb-list inherit pieces of another (admin/edit/view + custom aggregations) — saves rewriting.
    The Captain of the Watch reviews the ledgers quarterly with **audit2rbac**: the audit archive shows which verbs each citizen actually used; the ledgers get narrowed to match. Bindings that were never exercised are removed.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Citizenship paper | Subject (User / Group / ServiceAccount) |
| OIDC papers from a foreign embassy | OIDC token + groups claim |
| Pod's in-cluster ID badge | ServiceAccount token |
| Short-lived stamped pass | Projected ServiceAccount token (audience + expiry) |
| Verb ledger | Role / ClusterRole |
| Built-in role tiers (admin/edit/view) | Built-in ClusterRoles (admin / edit / view / cluster-admin) |
| Inheritance chains | ClusterRole aggregation via aggregationRule |
| Binding scroll (this namespace only) | RoleBinding |
| Cluster-wide binding scroll | ClusterRoleBinding |
| Quarterly ledger review | audit2rbac + rakkess + kubectl-who-can review |

⚠️ *Analogy stops here:* A real ledger is paper; K8s RBAC is policy evaluated by the apiserver per request — fast, deterministic, but invisible until tested. Test with `kubectl auth can-i`.

## ELI5 / ELI10

**ELI5.** Imagine three desks at the gate. One checks who you are. Another reads which doors that kind of person may open. A third writes down where the rules apply. Your cluster has three K8s objects doing the same thing: subject, role, binding.

**ELI10.** Three building blocks: **Subject** (User / Group / ServiceAccount; humans via OIDC, workloads via SA tokens — projected, short-lived). **Role / ClusterRole** (verbs on resources; built-ins admin/edit/view; aggregation via labels). **RoleBinding / ClusterRoleBinding** (binds subject to role; namespace-scoped or cluster-scoped). At scale: bind groups (not individuals); use built-in `edit` + per-namespace RoleBinding; disable default SA auto-mount; run audit2rbac quarterly to narrow.

## Real-world scenarios

- **Platform team — OIDC group → aggregated Role.** A 200-engineer org uses Okta. Group `k8s-developers` is bound (ClusterRoleBinding) to a custom aggregated `platform-developer` ClusterRole that combines the built-in `edit` + custom verbs (`get/list` on Backstage CRDs, `create/delete` on PRs to GitOps). New devs join group → access lands in 30 seconds; nothing per-developer.
- **Per-workload SA narrowed by audit2rbac.** An app reads ConfigMaps + lists Pods. Initial RoleBinding gave `edit`. Quarterly review: audit2rbac shows actual usage = `get/list configmap` + `list pod`. Narrowed RoleBinding reflects that. *Cut from "can write everything" to "can read two things"* with no app changes.
- **Break-glass cluster-admin via JIT.** Cluster-admin removed for all standing bindings. On-call invokes a JIT process (Vault SSH-style or a workflow approval) that issues a 1-hour cluster-admin kubeconfig + alarms in Slack. *Standing privilege replaced by audited just-in-time elevation.*
- **Audit finding — 17/20 SAs with cluster-admin.** An auditor sampled SAs in a regulated cluster; 17/20 had cluster-admin. Postmortem: SAs were broadly bound during the platform build phase; nothing narrowed after. Action: audit2rbac campaign over 60 days; quarterly narrowing now standard. Compliance gap closed.

## Common misconceptions

- **Myth:** "`cluster-admin` is for cluster admins; that's OK."
  **Truth:** **cluster-admin = god mode** — every verb on every resource including RBAC (can create/modify any binding). Use ONLY for break-glass elevation, never for standing access. Even cluster operators usually need only `admin`-equivalent ClusterRoles scoped to platform namespaces.
- **Myth:** "Every Pod needs the default ServiceAccount."
  **Truth:** The default SA gets auto-mounted unless explicitly disabled (`automountServiceAccountToken: false`). Most Pods don't need to call the K8s API at all — auto-mount + default SA = an attacker's gift if the Pod is compromised. Disable auto-mount; create per-workload SAs only when needed.
- **Myth:** "Aggregation is just for built-in roles like edit."
  **Truth:** **You can build your own aggregated ClusterRoles** for platform abstractions. Aggregation lets a CRD's small ClusterRole automatically merge into `edit` via a label — your platform can compose `platform-developer` from many small pieces. This is how operators integrate cleanly without modifying built-in roles.

## Recap

RBAC = subject + role + binding. Aggregation patterns compose. OIDC groups bind to aggregated roles. Per-workload SAs are narrow. Quarterly audit2rbac narrows further. Cluster-admin is break-glass; default-deny is the cluster's posture.

**Next — S3: Admission Policy Architecture.** Kyverno + Gatekeeper hybrid; mutating vs validating; ValidatingAdmissionPolicy + CEL inline; PolicyReport CRD; policy-as-code in CI.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
