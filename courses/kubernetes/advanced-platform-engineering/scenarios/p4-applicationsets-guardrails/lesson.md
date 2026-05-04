# K-ADV-PE P4 — P4 · Argo CD ApplicationSets + OPA / Kyverno Guardrails

> Course: K-ADV-PE (advanced specialization)
> Module P4 · ApplicationSets + Guardrails
> Companion preview: `/preview-kubernetes-adv-pe-lesson-04.html`.

---

**🎯 If you remember nothing else:** **ApplicationSet generates per-cluster Apps from one template; OPA + Kyverno gate at PR + admission + sync. Fleet velocity + fleet safety.**

## 1. Five generator kinds for fleet patterns

**List generator**: explicit list of items; one App per item.
    **Cluster generator**: iterates over Argo CD-registered clusters; one App per cluster (auto-discovered).
    **Git generator**: scans a Git repo directory or files; one App per directory/file.
    **Matrix generator**: composes two generators (e.g., clusters × git directories).
    **Merge generator**: combines generators with overlay precedence.
    Cluster + git generators are the fleet-GitOps default — "every cluster gets every app declared in this directory."

## 2. Cluster labels feed template parameters

Cluster generator surfaces cluster labels as template variables: `{{name}}`, `{{server}}`, `{{metadata.labels.region}}`. Template uses these to differentiate per-cluster (region-specific endpoints, cluster-specific replicas, env-specific values).
    Pattern: cluster label `tier=prod` → ApplicationSet template renders `replicas: 5`; `tier=dev` → `replicas: 1`. One ApplicationSet handles both.

## 3. PR-time + admission + sync

**PR-time**: `kyverno-cli` / `conftest` in CI. Block bad YAML before merge. Fast feedback for developers.
    **Admission**: Kyverno / Gatekeeper webhook. Block at apiserver if PR-time gate was bypassed or new policy added.
    **Sync**: Argo CD PreSync hook runs policy checks against rendered manifests; blocks deploy if violation. Catches pre-render issues + drift.
    Three layers because: PR-time catches early; admission catches anything that slips; sync catches policy drift at deploy time.

## 4. staged rollouts + sync waves + ProgressiveSync

**Sync waves**: annotation `argocd.argoproj.io/sync-wave: "-1"` orders resource sync (CRDs first, then operators, then Apps).
    **ProgressiveSync** (alpha → beta): per-cluster rollout with health gates. Apply to dev cluster first; if healthy, apply to next; abort on first unhealthy. Replaces big-bang ApplicationSet deploy.
    **Per-environment App tier**: ApplicationSet generates Apps in waves: dev → staging → prod. Combined with ProgressiveSync = safe fleet rollouts.
    **RBAC**: ApplicationSet ownership separate from App. Platform team owns ApplicationSets; tenants own per-app values via Git PRs.

## Before / After

**Before.** Pre-ApplicationSet: per-cluster Argo CD Application files manually maintained. Drift across clusters; new cluster = manual file copy. Policy enforced ad-hoc.

**After.** ApplicationSet generates per-cluster Apps from one template; OPA + Kyverno gates at PR + admission + sync. Fleet GitOps with uniform policy.

*One template, many clusters; three policy layers; staged rollouts.*

## Analogy — the K-Workshop bench

The Batch-Crafting Jig in the workshop fixtures one master template + many empty wagon frames; the master pours per-frame variations from a labels list. Three quality inspectors review at three checkpoints: at-PR, at-assembly, at-shipping.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Master template | ApplicationSet template |
| Empty wagon frames | Per-cluster Argo CD Apps generated |
| Per-frame label | Cluster label (tier / region / etc.) |
| PR inspector | kyverno-cli / conftest in CI |
| Assembly inspector | Admission webhook (Kyverno / Gatekeeper) |
| Shipping inspector | Argo CD PreSync hook |
| Staged rollout | ProgressiveSync (dev → staging → prod) |

⚠️ *Analogy stops here:* Wagon frames are physical; per-cluster Apps are CRDs. Drift detection via ProgressiveSync + Argo CD health checks.

## ELI5 / ELI10

**ELI5.** One master template churns out many wagons sized per cluster. Three quality checks: at the design table, at assembly, at the loading dock.

**ELI10.** **ApplicationSet**: 5 generators (List / Cluster / Git / Matrix / Merge); generates per-cluster Apps. **Templates** use cluster labels for per-cluster values. **Policy gates**: PR-time (kyverno-cli / conftest), admission (Kyverno / Gatekeeper), sync (PreSync hook). **ProgressiveSync**: staged dev → prod with health gates.

## Real-world scenarios

- **One ApplicationSet → 30 clusters.** Platform team's ApplicationSet uses Cluster generator + values from cluster labels (tier/region/env). 30 clusters auto-onboard; new cluster registration = new App appears.
- **Three-layer policy catches misconfig.** A tenant PR'd a privileged Pod. PR-time kyverno-cli flagged; PR blocked. Admission also configured; sync hook also runs. Misconfig never reaches prod.
- **ProgressiveSync — bad release auto-aborted.** ProgressiveSync waved to dev → staging; staging health failed; rollout aborted before prod. Postmortem on dev change; fix; re-deploy. Saved a fleet outage.
- **Outage — image registry not allowlisted.** ApplicationSet deployed; Pods image-pull-error fleet-wide. Postmortem: PR-time gate didn't check registry allowlist; added rule; re-test.

## Common misconceptions

- **Myth:** "ApplicationSet is just a Helm chart of Apps."
  **Truth:** ApplicationSet has structured generators (Clusters / Git / Matrix); auto-extends as inputs change. Helm-of-Apps is static; ApplicationSet is dynamic.
- **Myth:** "Admission policy alone is enough."
  **Truth:** Admission catches at apiserver; PR-time gives faster feedback to developers + sync hook catches render-time issues. Three layers each catch different classes.
- **Myth:** "ProgressiveSync slows deploys unacceptably."
  **Truth:** ProgressiveSync adds 10-30 min per wave but prevents fleet-wide outages. Cost worth paying for prod tier; dev tier can be big-bang.

## Recap

ApplicationSet for fleet GitOps; OPA + Kyverno gates at PR + admission + sync; ProgressiveSync for staged rollouts. Fleet velocity with fleet safety.

**Next — P5: Tenant onboarding + resource templates + cost controls + service catalogs.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
