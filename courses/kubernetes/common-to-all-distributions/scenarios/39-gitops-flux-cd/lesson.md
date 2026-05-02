# Lesson 39 — GitOps with Flux CD · Multi-Controller Architecture

> Course: Kubernetes — Common to all distributions
> Module 17 · GitOps · Lesson 2 of 3
> Companion preview: `/preview-kubernetes-lesson-39.html`.

---

**🎯 If you remember nothing else:** Flux uses **specialised controllers per concern**: `GitRepository` / `HelmRepository` / `OCIRepository` for sources; `Kustomization` for Kustomize-based deploys; `HelmRelease` for Helm; `Alert` + `Provider` for notifications. CLI is `flux`. CRD-only — no built-in UI. Best for: GitOps-native shops that prefer kubectl as the interface.

## 1. Same goal, different architecture

Flux and Argo CD share the GitOps goal but diverge architecturally. Where Argo CD ships one big controller binary + a UI, Flux ships **five specialised controllers**:
    
      - **source-controller** — fetches from sources. CRDs: `GitRepository`, `HelmRepository`, `HelmChart`, `OCIRepository`, `Bucket`.

      - **kustomize-controller** — renders Kustomize + applies. CRD: `Kustomization` (note: distinct from Kustomize's own `kustomization.yaml`).

      - **helm-controller** — installs Helm releases declaratively. CRD: `HelmRelease`.

      - **notification-controller** — sends alerts on events. CRDs: `Alert`, `Provider`, `Receiver`.

      - **image-automation-controller** + **image-reflector-controller** — automated image-tag updates in git from OCI registry events.

    
    Each controller is installed via the Flux Helm chart or `flux install`. They're independent — install only what you need. Each scales horizontally on its own.

## 2. "Flux bootstrapping its own GitOps"

The classic install: `flux bootstrap github --owner=myorg --repository=fleet-infra --branch=main --path=clusters/prod`. This:
    
      - Adds Flux's controller manifests to the git repo at the specified path.

      - Installs Flux on the cluster.

      - Sets up a `GitRepository` + `Kustomization` pointing at the same path.

      - From then on, Flux manages itself: edit the manifests in git, Flux applies the change.

    
    This "GitOps for GitOps" pattern is part of Flux's ergonomic; you don't hand-manage Flux upgrades — they're a `flux bootstrap` rerun or a manifest tweak.

## 3. GitRepository, Kustomization, HelmRelease

`# Source: where to fetch from
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata: {name: web-app, namespace: flux-system}
spec:
  interval: 1m
  url: https://github.com/myorg/web-app
  ref: {branch: main}
---
# Kustomization: render + apply from a source
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata: {name: web-prod, namespace: flux-system}
spec:
  interval: 5m
  path: ./overlays/prod
  prune: true
  sourceRef: {kind: GitRepository, name: web-app}
  targetNamespace: web-prod
  healthChecks:
  - {kind: Deployment, name: web, namespace: web-prod}
---
# HelmRelease: install a chart
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata: {name: cert-manager, namespace: cert-manager}
spec:
  interval: 5m
  chart:
    spec:
      chart: cert-manager
      version: 1.14.x
      sourceRef: {kind: HelmRepository, name: jetstack, namespace: flux-system}
  values: {installCRDs: true}`
    Common pattern: use Flux's `Kustomization` CRD to render Kustomize-style overlays from a git path; use `HelmRelease` for vendor charts. Each CRD has its own status, events, and reconcile loop.

## 4. The pieces beyond sync

**notification-controller** turns Flux events into outbound alerts. Provider points at Slack/Discord/Teams/PagerDuty/generic webhook; Alert filters which events to send. "Notify Slack on every `Kustomization` reconcile failure in production namespaces."
    **image-automation-controller + image-reflector-controller**: automate image-tag bumps. The reflector watches an OCI registry; when a new tag matches a policy, image-automation-controller commits the tag bump back to git. Closes the loop: build → push → flux auto-bumps → flux applies. CI pushes; Flux deploys.
    Compared to Argo CD Image Updater, Flux's image automation is more flexible (commits to git, so you have a record + PR review possible) but requires more setup. Most Flux shops use it for non-critical paths and let humans bump prod via PR.
    [ deep dive — skip if new ]The Flux vs Argo CD choice is mostly cultural. **Argo CD shines**: rich UI, easier ramp-up, Application abstraction, ApplicationSet PR generator (preview envs!). **Flux shines**: composable, kubectl-only, more flexible source types (Bucket, OCI, generic), tighter K8s feel. The CNCF graduation paths converged in 2024 — both are stable, both are widely adopted. Pick by your team's preference; both work.

## Before / After

**Before.** Pre-GitOps. CI ran kubectl apply. Same problems as Argo CD's before — drift, lost changes, unclear truth. Bonus problem if you wanted CRD-only ops: Argo CD's UI was central to its value but you couldn't fully manage it via kubectl.

**After.** Flux: every concern is a CRD. `kubectl get gitrepositories,kustomizations,helmreleases -A` shows the whole picture. CI/CD purists love it. UIs (Weave GitOps, Capacitor) exist as add-ons but aren't required.

Argo CD vs Flux is a matter of taste. Both deliver the GitOps experience. Flux for kubectl-first shops; Argo CD for UI-first shops.

## Analogy — the K-Town district

The Public Library has a Flux wing alongside the Argo CD reading room. Same goal — keep shelves matching the catalogue — but different staffing model. Instead of one librarian doing everything, Flux has **specialised desks**: a fetching desk (source-controller), a Kustomize-shelving desk, a Helm-shelving desk, a notifications desk. Each desk handles its concern; they coordinate by handing off to each other. The visitor (operator) interacts with each desk via paper forms (CRDs) — there's no central counter — but every desk's status is on a public bulletin board for inspection.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Fetching desk | `source-controller` + `GitRepository`/`HelmRepository`/`OCIRepository` |
| Kustomize-shelving desk | `kustomize-controller` + `Kustomization` CRD |
| Helm-shelving desk | `helm-controller` + `HelmRelease` |
| Notifications desk | `notification-controller` + `Alert`/`Provider` |
| Image-bump assistant | `image-automation-controller` |
| Public bulletin board (status) | CRD `.status` fields + events |
| "Self-installs from a git checkout" | `flux bootstrap` |

⚠️ *Analogy stops here:* The analogy stops here: Flux controllers are independent processes scheduled by K8s, not desks. They communicate via Kubernetes API objects, not paperwork.

## ELI5 / ELI10

**ELI5.** Like Argo CD, but each job has a different worker. One fetches the books. One organises the shelves. One sends notes. They share the same plan.

**ELI10.** Flux is GitOps via specialised controllers. `source-controller` handles GitRepository / HelmRepository / OCIRepository. `kustomize-controller` applies Kustomization CRDs. `helm-controller` applies HelmRelease CRDs. `notification-controller` alerts. `image-automation-controller` auto-bumps tags. CRD-only by default; UIs available as add-ons (Weave GitOps, Capacitor). Flux bootstrap installs Flux into a cluster managing itself via git.

## Real-world scenarios

- **A SaaS using Flux with image-automation.** CI builds + pushes signed images. image-reflector-controller watches OCI; image-automation-controller bumps tags in git on new releases. Kustomize-controller applies the bump. End-to-end: push image → 60-second reconcile → live in cluster. No manual step from build to deploy.
- **A bank running multi-tenant Flux.** Each tenant gets a namespace + a Flux Kustomization scoped to their git path. Tenant-RBAC limits which paths Flux can touch. Cluster admin owns the top-level Flux install + GitRepository CRDs; tenants own Kustomizations within their namespace. Clean tenant boundary.
- **A startup using Flux for vendor charts.** cert-manager, Argo Rollouts, Prometheus, etc., all installed via HelmRelease CRDs. `helm-controller` manages upgrades by updating the version field in git; rollback is a git revert. Less hand-tooling than Helm CLI. Reproducible across clusters.
- **A team that picked Flux over Argo CD for kubectl-first culture.** Engineering team mostly senior with deep K8s knowledge. They wanted kubectl as the only interface; UI as optional. Flux's CRD-first model fit. "What's the state?" answered by `kubectl get -A`. Slack alerts via notification-controller. Total UI: zero by design.

## Common misconceptions

- **Myth:** Flux is older and less feature-rich than Argo CD.
  **Truth:** Flux v1 was older; Flux v2 (current) is a complete rewrite with the multi-controller architecture. Both are CNCF graduated; both have rich feature sets; pick by preference.
- **Myth:** Flux has no UI.
  **Truth:** Flux's built-in UI is minimal. **Weave GitOps** + **Capacitor** are popular dashboards layered on top. The default experience is kubectl + flux CLI.
- **Myth:** You can't use Helm with Flux.
  **Truth:** Flux's `HelmRelease` CRD is one of its core features. Many shops use Flux specifically for Helm management.

## Recap

Flux is GitOps via specialised controllers. Source-controller fetches, kustomize-controller applies Kustomize, helm-controller manages Helm, notification-controller alerts. CRD-first; no built-in UI. Same goal as Argo CD; different aesthetic.

**Next — Lesson 40: Progressive Delivery.** The next layer above GitOps — controlled rollouts, automated canary analysis, automated rollback. Argo Rollouts and Flagger.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
