# Lesson 37 — Helm 3 · Charts, Values, Hooks, OCI

> Course: Kubernetes — Common to all distributions
> Module 16 · Application Delivery · Lesson 2 of 2
> Companion preview: `/preview-kubernetes-lesson-37.html`.

---

**🎯 If you remember nothing else:** A Helm **chart** = templates + values schema + Chart.yaml. `helm install` renders the templates with values, applies to the cluster, records a **release** in a Secret. `helm upgrade` applies a new chart version + values diff. Charts are distributed via **OCI registries** (same as images). Sign + verify charts with **cosign**. The dominant pattern: Kustomize for your own apps; Helm for vendor software.

## 1. Why a package manager

The Linux world has APT/YUM/DNF. The container world has registries. The K8s app world has **Helm**. The need is the same: bundle related files, version them, publish them, install with one command, upgrade safely.
    A K8s app is N manifests. Some are CRDs that must apply before others. Some have inter-references (Service references Deployment selector labels). Some need cluster-wide RBAC; some need namespace-scoped RBAC. Hand-managing this for vendor software (Postgres-Operator, cert-manager, Argo CD, etc.) was the original ops pain Helm solved.
    Helm 3 (released 2019) removed the controversial Tiller server component from Helm 2. Today, Helm runs entirely client-side: rendering templates locally, calling the K8s API directly. *Releases* are tracked in K8s Secrets in the install namespace.

## 2. What's in a chart

`my-app/
├── Chart.yaml          # name, version, dependencies
├── values.yaml         # default values
├── values.schema.json  # JSON-schema for values
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl    # template helpers
│   └── NOTES.txt       # post-install message
├── charts/             # vendored sub-charts
└── crds/               # CRDs (installed first, never templated)`
    Templates use Go templating with Helm helpers:
    `apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
      - name: web
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: {{ .Values.service.port }}`
    The `{{ }}` markers are Go templates; `.Values` is the user-provided values; `.Chart` is metadata; `include` calls a named template from `_helpers.tpl`. `helm install -f my-values.yaml` overrides the default `values.yaml`.

## 3. Operations on a release

Each chart installation is a **release**. Releases are namespaced; the same chart can be installed multiple times in different namespaces. Operations:
    
      - `helm install <name> <chart>` — render templates, apply, record release in a Secret.

      - `helm upgrade <name> <chart> --values new.yaml` — render with new values, diff, apply changes.

      - `helm rollback <name> <revision>` — re-apply a previous revision's manifests.

      - `helm uninstall <name>` — delete all resources from the release.

      - `helm list`, `helm status`, `helm history` — inspect releases.

    
    **Hooks** let charts run lifecycle scripts:
    
      - `pre-install` / `post-install` — run before/after the install. Common: database migration jobs.

      - `pre-upgrade` / `post-upgrade` — run on upgrade.

      - `pre-delete` / `post-delete` — run on uninstall.

      - `pre-rollback` / `post-rollback` — run on rollback.

    
    Hooks are regular K8s resources (usually Jobs) annotated with `helm.sh/hook`. The chart includes them; Helm runs them at the right phase.

## 4. The 2026 distribution model

Pre-2022, Helm charts were distributed via **chart repositories** — HTTP servers serving an `index.yaml`. It worked but was a parallel infrastructure to container registries.
    Helm 3.8+ supports **OCI registries** as first-class chart sources. `helm push my-chart:1.2 oci://registry.corp/charts`. Charts live alongside container images. Same auth, same vulnerability scanning, same retention policies. Almost every vendor in 2026 ships charts via OCI.
    **Chart signing** via cosign:
    
      - `cosign sign <chart-oci-ref>` — sign a chart in an OCI registry.

      - `helm install --verify ...` with `cosign-policy` — verify before install.

    
    Combined with Sigstore + admission verification (Lesson 30), the chain is: vendor signs chart in OCI; consumer's Helm verifies signature on install; the rendered manifests are themselves run only if the cluster's admission policies pass. Three layers of trust.
    [ deep dive — skip if new ]The K8s ecosystem largely standardised on Helm + OCI by 2024. Argo CD's `helm-charts` source type, Flux's `HelmChart` CRD, and most CI tools support it natively. New vendors publishing K8s software in 2026 default to OCI-distributed Helm charts; the index.yaml-based distribution is legacy.

## Before / After

**Before.** Hand-deploy 30 manifests for vendor software, hope you got every CRD right, lose track of versions, fight on every upgrade. Custom hooks for migrations done as ad-hoc Jobs you remember to apply. "Where's the latest install procedure?" lives in tribal memory or out-of-date Confluence.

**After.** One `helm install`; release tracked in a Secret; `helm upgrade` handles version-to-version migration; hooks orchestrate DB migrations; charts are signed; OCI registry distributes them; CI can auto-verify signatures before install. The vendor's install procedure is the chart.

Helm 3 + OCI is the K8s software distribution standard. Every major vendor ships charts via OCI in 2026; index.yaml repositories are legacy.

## Analogy — the K-Town district

Next door to the Kustomize press is the Helm chart counter. Vendors arrive with **sealed envelopes** (charts) — each containing a complete poster set ready to print, plus a parameter sheet (values.yaml) the customer fills in. The press operator runs the envelope through the press once (`helm install`), customising for the specific district's parameter sheet. The shop logs the install in a ledger (the release Secret) so they can roll back if needed. Vendors keep their envelopes in a sealed-envelope warehouse (OCI registry) with notarised stamps (cosign) the press can verify before opening.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Sealed envelope from a vendor | Helm chart |
| Parameter sheet customer fills in | `values.yaml` |
| Run envelope through press once | `helm install` |
| Run again with different parameters | `helm upgrade` |
| Press log entry per run | Release Secret |
| "Roll back to last entry" | `helm rollback` |
| Pre-print prep stage | `pre-install` hook |
| Sealed-envelope warehouse | OCI registry |
| Notarised stamp on envelope | Cosign chart signature |

⚠️ *Analogy stops here:* The analogy stops here: real Helm renders Go templates with values, including conditional branches and loops. Charts can have sub-charts (dependencies). It's much more programmable than "poster + parameter sheet."

## ELI5 / ELI10

**ELI5.** Vendors give you a recipe with blanks (chart). You fill in the blanks (values). The chef makes your dish (helm install).

**ELI10.** A Helm **chart** = Go-templated K8s manifests + values schema + Chart.yaml + lifecycle hooks. `helm install` renders the templates with user-provided values, applies the result, records a **release** as a Secret. `helm upgrade` diffs and applies new versions; `helm rollback` reverts. Charts are distributed via OCI registries (alongside images), signed via cosign. Use Helm for vendor software; Kustomize for your own apps.

## Real-world scenarios

- **A SaaS using Helm + Helmfile for vendor software.** Argo CD installs internal apps via Kustomize. Vendor software (cert-manager, Argo CD itself, Prometheus, Grafana) installed via Helm. Helmfile orchestrates multiple chart installs declaratively. Pinning chart versions in git; OCI registry hosts internal mirror of public charts.
- **A bank running cosign-verified Helm installs.** Internal Helm OCI registry. Charts signed by CI via cosign keyless. Cluster admission policy: chart pulls only allowed from internal registry. Verified install ensures supply-chain integrity end-to-end.
- **A vendor publishing their software as a chart.** Maintain Chart.yaml with semver. CI runs `helm lint` + tests on every commit. `helm package` + `helm push` to OCI on tag. Documentation references chart version. Customers `helm install vendor/their-app --version X.Y.Z` and they have the latest tested release.
- **A team using hooks for safe schema migrations.** Chart includes a `pre-upgrade` Job that runs database migration. `post-upgrade` Job warms the cache. Failing migration aborts the upgrade; broken state is recoverable via `helm rollback`. The hooks bind release lifecycle to actual application state.

## Common misconceptions

- **Myth:** Helm 3 still uses Tiller.
  **Truth:** Tiller was removed in Helm 3. Modern Helm is purely client-side; release state is in Secrets in your namespace.
- **Myth:** A Helm chart is just YAML with templates.
  **Truth:** It's also a versioned package, with a defined values schema (values.schema.json), lifecycle hooks, optional sub-charts, and a release-tracking model. Closer to a Linux package than a templated YAML.
- **Myth:** Helm and Kustomize are competing solutions you must pick between.
  **Truth:** They solve different problems. Use Helm for distributed/vendor packages; Kustomize for in-house environment differentiation. Most teams use both — Helm for cert-manager, Kustomize for their own services.

## Recap

A chart = templated manifests + values + hooks + Chart.yaml. helm install / upgrade / rollback are the operations. Releases are Secrets. OCI distribution is the modern default. Sign with cosign. Use Helm for vendor; Kustomize for in-house.

**Next — Lesson 38: GitOps with Argo CD.** Module 17 begins — the GitOps half of application delivery. Argo CD makes "git is the source of truth" mechanical: it watches your repo and reconciles the cluster.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
