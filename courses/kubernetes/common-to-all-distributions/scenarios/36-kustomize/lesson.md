# Lesson 36 — Kustomize · Overlay-Based Manifest Customisation

> Course: Kubernetes — Common to all distributions
> Module 16 · Application Delivery · Lesson 1 of 2
> Companion preview: `/preview-kubernetes-lesson-36.html`.

---

**🎯 If you remember nothing else:** **Kustomize** takes plain Kubernetes YAML files in a `base/` + `overlays/{env}/` structure and produces final manifests via **declarative patches**. Built into `kubectl` as `kubectl apply -k`. *No templates, no string interpolation*. The base is real YAML; overlays are real YAML; the result is real YAML.

## 1. The duplication problem and the overlay answer

Production K8s has *at least* three environments per service: dev, staging, prod. Each needs different replicas, image tags, configuration, namespaces, and so on. The naive solutions:
    
      - **Copy-paste files per environment** — every change is N edits; drift inevitable.

      - **String templating (Helm without overlays)** — fast to start, painful at scale; templating turns YAML into a custom DSL.

      - **Overlay model (Kustomize)** — base YAML stays plain; environment-specific YAML *patches* the base.

    
    Kustomize's big bet: most production differences between environments are small (`replicas: 1` → `replicas: 6`; `image: app:dev` → `image: app:v1.2`; namespace; a couple of env vars). Express those as patches; leave the bulk of the manifest unchanged in the base.

## 2. base/ + overlays/

The canonical layout:
    `app/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patches.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   └── patches.yaml
    └── prod/
        ├── kustomization.yaml
        ├── patches.yaml
        └── pdb.yaml`
    `base/kustomization.yaml` lists the resources in the base:
    `apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources: [deployment.yaml, service.yaml, configmap.yaml]
commonLabels:
  app: web`
    `overlays/prod/kustomization.yaml` includes the base + applies patches:
    `apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: prod
resources:
  - ../../base
  - pdb.yaml             # extra resource only in prod
patches:
  - target: {kind: Deployment, name: web}
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 6
images:
  - name: app
    newTag: v1.2.0`
    Run `kubectl apply -k overlays/prod/`; Kustomize expands the manifest in memory and applies. Or `kustomize build overlays/prod/` to print the result for review.

## 3. The features you actually use

- **Patches** — JSON 6902 (path-based) or strategic-merge (YAML-shape-based). Strategic-merge is more readable; JSON patch is more precise.

      - **Common labels / annotations** — apply to every resource. "`commonLabels: app: web, env: prod`" → every resource has those labels.

      - **Name prefix / suffix** — "`namePrefix: prod-`" → every Deployment/Service/etc. is renamed prod-X. Avoids name collisions in shared namespaces.

      - **Namespace** — set namespace on all resources at once.

      - **Image transformations** — "replace image:tag with image:v1.2 throughout."

      - **ConfigMap / Secret generators** — generate ConfigMap/Secret from files or literals; auto-suffix the name with content hash, so changes trigger Pod restart automatically ("the rolling-update bonus").

      - **Components** — reusable transformations across multiple overlays. "Add monitoring sidecar" as a Component; reference it from any overlay that wants it.

    
    What Kustomize won't do (and what people complain about):
    
      - **Conditionals** — "if env == prod then add this." Kustomize's answer: don't condition; have separate overlays. Forces clarity.

      - **Loops** — "for each item in list, generate a Deployment." No. Use a more powerful tool (Helm, jsonnet, CDK8s) if you need dynamic generation.

      - **Cross-resource references in transformations** — limited.

## 4. Different tools for different problems

Kustomize and Helm are not enemies. They solve different problems:
    
      - **Use Kustomize when:** you own the manifests; you have a few environments; you want plain YAML; you want zero templating cognitive load.

      - **Use Helm when:** you ship software to others (charts to the public); you need conditional logic / loops; you need versioned package distribution.

      - **Use both when:** Helm chart from a vendor (e.g., `nginx-ingress`) — but you want to patch its values per environment. Use Helm to render, Kustomize to overlay. Argo CD supports this combination.

    
    Most production teams in 2026 use Kustomize for their *own* apps and Helm for *vendor* charts. The split aligns with who owns the manifest — your code in Kustomize; their code in Helm.
    [ deep dive — skip if new ]The case *against* Kustomize is real for some teams: nested overlays + Components can become spaghetti. The remedy is discipline — keep overlays shallow (1-2 levels max), prefer flat structure over deep hierarchies, name patches descriptively. Done well, Kustomize repos are easy to navigate years later. Done poorly, they're worse than the YAML soup they replaced.

## Before / After

**Before.** Three copies of every manifest, one per environment. Every change = three PRs (or one giant PR with three sets of identical changes). Drift between environments inevitable; "works in staging, fails in prod" stories common.

**After.** One `base/` with the canonical manifest. `overlays/dev|staging|prod/` with small patches (replicas, image, env-specific config). One change to base = applies everywhere. Drift impossible by structure.

Kustomize's overlay model is the simplest valid answer to multi-environment K8s manifest management. Built into kubectl since 1.14; no extra tooling needed.

## Analogy — the K-Town district

The Print Shop has a master plate (the **base manifest**) — the canonical version of every poster the city prints. For each district that orders posters, the operator stacks transparency sheets (**overlays**) on top of the master plate before running the press. "For East District: replace the date and replicate three times." "For West District: change the colour scheme." The master plate never changes; each district's overlay is small and specific. The press (the `kustomize build` command) combines plate + overlay into a final printed poster ready to put up on the wall.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Master plate | `base/` |
| Transparency overlay sheet | `overlays/{env}/kustomization.yaml` + patches |
| "Change replica count" instruction | Strategic-merge or JSON patch |
| "Apply this label everywhere" stamp | `commonLabels` |
| "Rename to prod-X" stamp | `namePrefix` |
| "Use this image tag" rule | `images:` transformation |
| Reusable overlay across districts | `Component` |
| The press combining plate + overlay | `kubectl apply -k` / `kustomize build` |

⚠️ *Analogy stops here:* The analogy stops here: real K8s overlays apply via in-memory document merging — there's no physical layering. And ConfigMap/Secret content hashes change names automatically; that's a feature, not a metaphor.

## ELI5 / ELI10

**ELI5.** One main poster. Different stickers for different stores. The press puts the stickers on the poster automatically.

**ELI10.** Kustomize manages multi-environment K8s manifests via overlays. Plain YAML at base/, environment-specific patches at overlays/{env}/. Built into kubectl as `kubectl apply -k`. No string templating. Use it for your own apps; reach for Helm when you need loops/conditionals or are publishing charts.

## Real-world scenarios

- **A SaaS standardising on Kustomize for in-house apps.** One base/ per microservice, three overlays/ for dev/staging/prod. Argo CD watches the overlay paths; per-env apps automatic. Engineers contribute changes to base/; the overlay patches live forever as small env-specific docs.
- **A bank using Kustomize Components for compliance.** A `compliance/` Component adds: PSA-restricted label, NetworkPolicy default-deny, ResourceQuota, audit annotations. Every prod overlay references the Component. Compliance team owns the Component; app teams own their overlays. Single source of truth for compliance baseline.
- **A startup using Helm + Kustomize.** `helm template` renders the vendor chart (Ingress NGINX); the rendered output goes through Kustomize to add namespace + labels + monitoring sidecars. One Argo CD app per environment. Best of both worlds.
- **A team that fled from copy-paste YAML.** Started with 3 environments × 14 services = 42 nearly-identical YAML files. Migrated to Kustomize: 14 base/ directories + 3 overlay directories per service. Total YAML lines dropped 62%. Onboarding new env was a copy of an existing overlay.

## Common misconceptions

- **Myth:** Kustomize is just kubectl's built-in version of Helm.
  **Truth:** Different model. Helm = templating; Kustomize = overlays. Helm renders strings; Kustomize patches YAML. Both produce K8s manifests, but the development experience and use cases differ.
- **Myth:** You can do conditionals in Kustomize with Components.
  **Truth:** Components add transformations; they don't conditionally include resources based on a value. The Kustomize answer to "if condition then resource" is "have a separate overlay for that case."
- **Myth:** Kustomize can't handle complex apps.
  **Truth:** It can — but at scale you'll feel the limits (no loops/conditionals). Many large orgs use Kustomize successfully for hundreds of services. The discipline is keeping overlays shallow + flat.

## Recap

Kustomize manages multi-environment K8s manifests via overlays — plain YAML at base/, env-specific patches at overlays/. No templating. Built into kubectl. Use for your own apps; reach for Helm when you need loops/conditionals or are publishing charts.

**Next — Lesson 37: Helm 3.** The other major application-delivery tool. Charts, values, templates, OCI distribution, signing. Print Shop, vendor side.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
