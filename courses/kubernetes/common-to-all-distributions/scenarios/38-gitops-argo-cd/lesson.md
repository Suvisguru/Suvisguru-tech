# Lesson 38 — GitOps with Argo CD · Application CRD, Sync, Drift Detection

> Course: Kubernetes — Common to all distributions
> Module 17 · GitOps · Lesson 1 of 3
> Companion preview: `/preview-kubernetes-lesson-38.html`.

---

**🎯 If you remember nothing else:** Argo CD is a controller that watches a git repo + reconciles the cluster to match. Define an **Application** CRD pointing at a git path; Argo CD syncs (auto or manual). Drift detection is built in — if someone `kubectl edit`s a managed resource, Argo CD shows it as *OutOfSync*. Pair with **Argo CD Image Updater** for image-bump automation; **App-of-Apps** for managing many Apps at scale.

## 1. Why GitOps

Pre-GitOps deployment models: *imperative push*. Engineer (or CI) runs `kubectl apply`; cluster state changes; nothing tracks the change. Many failure modes:
    
      - Drift — someone `kubectl edit`s, cluster ≠ git.

      - Lost changes — git is updated; nobody applied; cluster still old.

      - No audit — what's in production right now? Hope your last apply was the truth.

      - Hard to roll back — `git revert` doesn't reach the cluster automatically.

    
    GitOps inverts the model: *git is the source of truth; the cluster pulls*. A controller (Argo CD) watches git; whenever git changes, the controller applies. Whenever the cluster drifts, the controller notices + alerts (and optionally re-applies).
    The four GitOps principles (OpenGitOps spec): **declarative**, **versioned + immutable**, **pulled automatically**, **continuously reconciled**. Argo CD implements all four.

## 2. Argo CD's primary unit

An **Application** is one tracked deployment unit. Define it once; Argo CD reconciles forever.
    `apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/web-app
    targetRevision: main
    path: overlays/prod
    # OR for Helm:
    # chart: web-app
    # repoURL: oci://registry.corp/charts
    # targetRevision: 1.2.0
    # helm: { values: |- ... }
  destination:
    server: https://kubernetes.default.svc
    namespace: web-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions: [CreateNamespace=true, ServerSideApply=true]`
    Source can be plain manifests, Kustomize, Helm chart, Helm chart from OCI, or even a custom plugin. Destination is a cluster + namespace. `syncPolicy.automated`: auto-sync on git change, auto-prune deleted resources, auto-heal drift.

## 3. What Argo CD actually does

Three states an Application can be in:
    
      - **Synced** — cluster matches git.

      - **OutOfSync** — cluster differs from git (because git updated, or someone hand-edited).

      - **Unknown** — Argo CD can't reach git or the cluster.

    
    Two health states layered on top:
    
      - **Healthy** — resources are running as expected (Pods ready, etc.).

      - **Degraded** — applied but something's wrong (CrashLoopBackOff, etc.).

    
    The Argo CD UI shows a colour-coded tree of resources: green Synced+Healthy, yellow Synced+Progressing, red Degraded. One glance per env.
    **Self-healing**: if `selfHeal: true`, Argo CD re-applies whenever drift is detected. Engineer who `kubectl edit`s gets reverted within seconds. Hard discipline; common in mature shops.
    **Sync waves** + **hooks**: order resource application via `argocd.argoproj.io/sync-wave: 0/1/2` annotations; run pre-sync / post-sync Jobs as hooks. Used for: install CRDs first, then operator, then operator instances.

## 4. Managing many Applications at scale

One Application per microservice × per environment = 50 Applications quickly. Two patterns to manage at scale:
    
      - **App-of-Apps** — one parent Application points at a git path containing many child Application YAMLs. Argo CD syncs the parent; the parent's sync creates/updates the children. Bootstrap in one apply.

      - **ApplicationSet** — modern alternative. A CRD that generates Applications from a template + a set of inputs. Inputs can be: a list, a set of git directories matching a glob, a set of clusters in Argo CD, even external sources. "For every directory under `apps/`, generate an Application targeting that directory." Eliminates boilerplate Application YAML.

    
    ApplicationSet generators in production:
    
      - `list` — explicit list of values.

      - `git` — one Application per matching git path.

      - `cluster` — one Application per registered cluster (multi-cluster GitOps).

      - `matrix` — combinatorial: every Service × every cluster.

      - `pull-request` — generate Application per open PR (preview environments!).

    
    [ deep dive — skip if new ]The PR-based ApplicationSet generator is one of the underrated GitOps wins. Open a PR; Argo CD spins up an isolated namespace with the PR's manifests; QA tests; merge → namespace destroyed. Preview environments without bespoke tooling. Combined with Karpenter, the cost is just per-PR Pod time.

## Before / After

**Before.** CI runs `kubectl apply` from the build pipeline. Sometimes someone `kubectl edit`s. Drift accumulates. Engineers go to the cluster console to verify what's deployed; sometimes they're wrong. Rollbacks involve replaying old git commits through CI. "What's in production?" is a question, not an answer.

**After.** Argo CD watches git, syncs continuously. UI shows every cluster's state at a glance. Drift is impossible (selfHeal reverts it). Rollback = `git revert` + auto-sync. Audit log is the git log. "What's in production?" = "the latest commit on the prod branch."

GitOps via Argo CD turned K8s deployment from "a script you ran somewhere" into "a continuous reconciliation loop." The pre-GitOps days look medieval.

## Analogy — the K-Town district

The Public Library has a special **Argo CD reading room**. Every cluster is represented by a shelf. Each shelf has a librarian (Argo CD controller) who consults a master catalogue (the git repo) and ensures the shelf matches the catalogue exactly. If a visitor sneaks in and rearranges the books (`kubectl edit`), the librarian notices instantly and either flags it (notification) or restores order (selfHeal). The catalogue is the truth; the shelf reflects the catalogue. To change the shelf, you change the catalogue (commit to git); the librarian propagates within seconds.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Master catalogue | Git repository |
| Library shelf | Cluster state |
| Librarian | Argo CD controller |
| "This shelf must match this section of the catalogue" | `Application` CRD |
| "Match exactly, no extra books" | `prune: true` |
| "Restore order if disturbed" | `selfHeal: true` |
| "Build a card for every section automatically" | `ApplicationSet` |
| "Open a temporary shelf for every new chapter draft" | PR-based ApplicationSet generator |
| "Every shelf in every branch" | Multi-cluster GitOps via cluster generator |

⚠️ *Analogy stops here:* The analogy stops here: Argo CD also handles complex resource ordering (sync waves, hooks), partial drift (some resources OutOfSync, some Synced), and multi-source apps. The librarian metaphor undersells the precision.

## ELI5 / ELI10

**ELI5.** Robot librarian. The plan is in a notebook (git). Every minute, the robot checks the shelf. If wrong, it puts the right books back. If you write in the notebook, the robot updates the shelf.

**ELI10.** Argo CD is a GitOps controller. Define an `Application` CRD pointing at a git path; Argo CD reconciles the cluster to match. Three sync states (Synced/OutOfSync/Unknown) + two health states (Healthy/Degraded). selfHeal reverts manual drift. App-of-Apps + ApplicationSet patterns scale to many apps. PR-based ApplicationSet enables free preview environments.

## Real-world scenarios

- **A SaaS using Argo CD as the only deployment path.** CI builds + signs images, pushes to OCI. Engineers update Helm values or Kustomize overlays in git via PR. Argo CD auto-syncs on merge. Zero `kubectl apply` in CI; zero `kubectl edit` in production. Engineering culture: "if it's not in git, it doesn't exist."
- **A bank with multi-cluster GitOps.** 40 production clusters across regions. ApplicationSet with cluster generator: one Application per cluster, all from the same git path. Update once in git → all 40 clusters update on next sync. RBAC in Argo CD ensures team A can only sync apps in their projects.
- **A startup with PR-based preview environments.** ApplicationSet PR generator. Open PR → temporary namespace + Application created. `preview-pr-1234.dev.example.com` works. QA tests, designer reviews. Merge → namespace destroyed. Cost: $0.05/PR. Replaces a manual provisioning process that took 30 minutes per request.
- **A team using selfHeal as a discipline tool.** Initial pushback: "can I still kubectl edit during incidents?" Resolution: dedicated `incident` branch with hotfix manifests; ops engineers commit there during P0s; Argo CD syncs the hotfix branch immediately. After incident, hotfix gets cherry-picked to main. selfHeal stays on; cultural shift to "cluster state lives in git."

## Common misconceptions

- **Myth:** GitOps slows down deployment.
  **Truth:** It changes the deployment path, not the speed. Argo CD syncs on git push within seconds (or use `argocd app sync` for instant). The slowness people complain about is *discipline* (everything via PR), not technology.
- **Myth:** Argo CD replaces CI.
  **Truth:** No. CI builds + tests + pushes images. Argo CD deploys. The boundary: CI ends with a manifest update PR; Argo CD picks up from there. Some shops pair Argo CD Image Updater (auto-bumps tags in git) with CI; that automates the handoff.
- **Myth:** You need ApplicationSet for every multi-app setup.
  **Truth:** App-of-Apps is sufficient for most cases. ApplicationSet shines when generators (cluster, PR, matrix, git) replace boilerplate. Start with App-of-Apps; switch when boilerplate becomes painful.

## Recap

Argo CD is a GitOps controller: declare Applications pointing at git, the controller reconciles continuously. selfHeal + prune make git the only mutator. App-of-Apps + ApplicationSet scale to many apps + clusters. PR-based ApplicationSet gives free preview environments.

**Next — Lesson 39: GitOps with Flux CD.** The other major GitOps tool. Same goal, different design — controllers + CRDs per concern (sources, kustomizations, helm releases). Public Library, Flux wing.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
