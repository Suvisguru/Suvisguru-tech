# K-OCP O6 — O6 · Workloads and Developer Experience

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O6 · Workloads and Developer Experience
> Companion preview: `/preview-kubernetes-ocp-lesson-06.html`.

---

**🎯 If you remember nothing else:** **S2I + BuildConfig + ImageStream is the OCP-native build pipeline; works alongside (not replacing) external CI. Pipelines (Tekton) and GitOps (Argo CD) ship as managed Operators. Serverless / Service Mesh / Dev Spaces are productized Knative / Istio / Che. Use Deployment over DeploymentConfig for new workloads.**

## 1. S2I + BuildConfig + ImageStream + internal registry

**Source-to-Image (S2I)** = build container images from source code *without* writing a Dockerfile. S2I builder images encode the build logic for a language/framework (Java, Node, Python, Ruby, etc.). You provide source repo URL; S2I clones, builds, packages, outputs an image to the internal registry.
    **BuildConfig** declares: source (Git URL + branch + context-dir), strategy (S2I vs Docker vs Custom), output (target ImageStreamTag), triggers (webhook / image-change / manual). One BuildConfig → many **Build** CRs (each Build is one execution).
    **ImageStream** = abstraction over container image tags. `my-app:latest` as an ImageStreamTag points to a specific image SHA in the internal registry. Decouples consumers (Deployments) from concrete image versions; updates flow via image triggers.
    **Internal container registry** (`image-registry.openshift-image-registry.svc:5000`) — built-in registry hosting BuildConfig outputs + ImageStream-tracked images. Project-scoped namespaces; RBAC via OCP roles.
    **oc new-app** + **oc new-build** — quick-start commands: `oc new-app https://github.com/my/repo` autodetects language → creates BuildConfig + ImageStream + Service + DeploymentConfig + Route in one command. Great for dev-stage spin-up.

## 2. DeploymentConfig (legacy) vs Deployment + Templates

**DeploymentConfig (DC)** = OCP's pre-Deployment workload primitive. Predates K8s' Deployment + ReplicaSet. Has unique features: image triggers (auto-deploy on ImageStream tag change), config-change triggers, lifecycle hooks (pre / mid / post deploy), automatic rollback on failed deploy.
    **Deployment** (K8s standard) = the recommended workload primitive. ReplicaSet-based; rolling updates; rollback via kubectl rollout undo. *For new workloads, use Deployment*; DeploymentConfig is legacy + still supported but no longer the default.
    **When DC over Deployment?** When you genuinely need OCP-specific image-triggered redeploys without external CI. Otherwise Deployment + image-trigger via Pipelines / GitOps / external CI is the modern path.
    **Templates** = pre-OperatorHub mechanism for app templates. Parameterised YAML (image, replicas, resources, etc.) instantiated via `oc process <template> -p PARAM=value | oc apply -f -`. Still used in Developer Catalog. Largely superseded by Helm + Operators for new platforms but still common.

## 3. OpenShift Pipelines (Tekton) + GitOps (Argo CD) + Serverless (Knative) + Service Mesh (Istio)

**OpenShift Pipelines** = managed **Tekton**. Pipeline + Task + PipelineRun + TaskRun CRs. Container-native CI/CD; Pods run each task. Tekton Hub catalog of reusable Tasks. *Replaces Jenkins on OCP.*
    **OpenShift GitOps** = managed **Argo CD**. Application + ApplicationSet + AppProject CRs. Continuous reconciliation from Git into clusters. Replaces self-installed Argo CD or Flux. Sync wave / hooks support. Multi-cluster via ApplicationSet.
    **OpenShift Serverless** = managed **Knative**. Knative Serving (autoscale to zero, request-based scaling, traffic splitting) + Knative Eventing (event-driven workflows). For request-driven workloads with idle cost concerns; for event consumers (Kafka / CloudEvents).
    **OpenShift Service Mesh** = managed **Istio**. Sidecars on Pods for mTLS, traffic management, observability. Multi-cluster mesh + Gateway API support. Managed by the Service Mesh Operator; cluster-scoped Istio control plane.

## 4. Dev Spaces (Eclipse Che) + Helm + Developer Catalog + web console workflows

**OpenShift Dev Spaces** = managed **Eclipse Che**. Cloud-hosted dev environments (Pods running editor + tools) for browser-based development. Devfiles define the workspace stack. *For onboarding, demo environments, or laptop-less dev.*
    **Helm in OCP** — fully supported. Helm charts visible in the **Developer Catalog** alongside Templates and Operator-installable apps. Add custom Helm chart repos via `HelmChartRepository` CR. Tiller-less (Helm 3+); RBAC via the user's OCP credentials.
    **Developer Catalog** = Developer perspective view of installable apps: Templates + Helm charts + S2I builders + Operator-backed services. Click-to-deploy with parameterised forms.
    **Web console workflows:**
    
      - **Topology view** — visualises Project: Deployments, Services, Routes, Pods + their connections. Click an icon for actions (scale, edit, view logs, port-forward, debug).

      - **Pipelines view** — Tekton Pipeline runs + logs + success/failure timeline.

      - **Builds view** — BuildConfig + Build status + logs.

      - **Add+ menu** — quick-start: From Git, From Container image, From Catalog (Templates + Helm), Container Image, Database, etc.

## Before / After

**Before.** Pre-Operator-managed CI/CD on K8s = self-installed Argo CD + Tekton + Knative + Istio + cert-manager + 5 more Helm charts. Each chart has its own upgrade cycle; chart drift was constant. Dev environments meant per-developer laptop setup with widely-varying tool versions. No built-in build path — devs wrote Dockerfiles or external CI configs.

**After.** OCP ships **S2I + BuildConfig + ImageStream + internal registry** as built-in build path. Managed Operators: **Pipelines (Tekton)**, **GitOps (Argo CD)**, **Serverless (Knative)**, **Service Mesh (Istio)**, **Dev Spaces (Eclipse Che)**. **Developer Catalog** + topology view in web console. *End-to-end developer experience without assembly.*

*Red Hat productizes the major K8s dev tools as supported Operators. Less assembly; one vendor accountable for the whole DX stack.*

## Analogy — the K-Foundry bay

The **Mold Shop** at K-Foundry is where raw material (source code) becomes finished products (running workloads). The Foundry-Master-built tools sit on the workbench:
    The **S2I press** takes source code + a builder image (one for Java, one for Python, etc.) and stamps out a finished container image. No Dockerfile required — the builder image's knowledge handles the language-specific packaging. The **BuildConfig recipe card** declares what to build; each **Build job ticket** is one execution. The **ImageStream conveyor** tracks finished images by tag; downstream consumers (Deployments) listen for new tags and roll forward.
    For more complex CI/CD, the **Pipelines (Tekton) workshop** chains Tasks into Pipelines. The **GitOps (Argo CD) reconciler** continuously syncs from Git to cluster — git push = production rollout.
    For specialty runtimes: **Serverless (Knative)** for scale-to-zero request workloads; **Service Mesh (Istio)** for sidecar-managed mTLS + routing; **Dev Spaces (Eclipse Che)** for browser-based dev environments.
    The **Developer Catalog** is the parts catalog visible to app devs: Templates + Helm charts + S2I builders + Operator-backed services. The **topology view** in the web console shows the running Project as a graph.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| S2I press | Source-to-Image (S2I) build strategy |
| Builder image (per-language) | S2I builder image (java / python / nodejs / etc.) |
| Recipe card | BuildConfig |
| Build job ticket | Build CR (one execution) |
| ImageStream conveyor | ImageStream + ImageStreamTag (decouples consumers from image SHAs) |
| Internal-parts warehouse | Internal container registry (image-registry.openshift-image-registry.svc:5000) |
| Quick-start order command | `oc new-app` + `oc new-build` |
| Foundry workshop chain | OpenShift Pipelines (Tekton) — Pipeline + Task + PipelineRun |
| Continuous-sync reconciler | OpenShift GitOps (Argo CD) — Application + ApplicationSet |
| Scale-to-zero turbine | OpenShift Serverless (Knative) |
| Sidecar-mediated traffic shop | OpenShift Service Mesh (Istio) |
| Cloud-hosted dev workshop | OpenShift Dev Spaces (Eclipse Che) |
| Pre-built Mold Shop catalog | Developer Catalog (Templates + Helm + S2I + Operators) |
| Foundry overview map | Web console Topology view |
| Pre-Deployment workload primitive | DeploymentConfig (DC) — legacy, still supported |
| Modern workload primitive | Deployment (K8s standard) |

⚠️ *Analogy stops here:* A real mold shop has fixed press lines; OCP's build/CI/runtime stack is software-defined. Helm chart drift across teams is a real failure mode the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** The Mold Shop turns code into running apps. The S2I press handles the basic stamp-out for common languages; the Pipelines workshop handles fancier CI; the GitOps reconciler keeps the cluster matching what's in git. Plus specialty runtimes for scale-to-zero, mesh routing, and browser dev environments.

**ELI10.** OCP DX = built-in S2I + BuildConfig + ImageStream + internal registry; managed Operators for OpenShift Pipelines (Tekton), OpenShift GitOps (Argo CD), OpenShift Serverless (Knative), OpenShift Service Mesh (Istio), OpenShift Dev Spaces (Eclipse Che); Helm in Developer Catalog; `oc new-app` for quick-start. Use Deployment (not DeploymentConfig) for new workloads. Topology view + Developer perspective in web console.

## Real-world scenarios

- **SaaS — GitOps + Pipelines for git-push-to-prod.** A SaaS uses OpenShift GitOps + Pipelines: developer pushes to feature branch → Pipeline runs unit tests + builds container via S2I to ImageStream → on merge to main, Pipeline tags image → Argo CD detects change → reconciles to staging → automated promotion job to prod after smoke tests. *Git push to prod takes 12 minutes.*
- **Legacy migration — Java apps S2I-built without Dockerfiles.** A bank migrates 40 legacy Java apps to OCP. They use the Java S2I builder; no Dockerfiles to write. `oc new-app` per app generates BuildConfig + Deployment + Service + Route. Builder image upgrades flow automatically via image triggers. *40 apps containerised + deployed in 2 weeks; no Dockerfile expertise required.*
- **Event-driven — OpenShift Serverless scales to zero between events.** A retail platform processes order events from Kafka. Each consumer is a Knative Service; idle = zero replicas; events arrive → Knative scales pods up; processed → scale back to zero. *Off-hours infra cost approaches zero; no over-provisioning required.*
- **Onboarding — Dev Spaces saved 3 days per new hire.** A 200-engineer team uses Dev Spaces for new-hire onboarding. Day 1: log into console, click "Open in Dev Spaces" on the project repo, get a fully-configured workspace (Java 17 + Maven + IDE + dependencies pre-loaded). *3 days of laptop setup compressed to 5 minutes.*

## Common misconceptions

- **Myth:** "Use DeploymentConfig because it's OCP-native."
  **Truth:** **Deployment** is the modern recommendation for new workloads. DeploymentConfig is legacy + still supported but not preferred. Use Deployment + image triggers via Pipelines / GitOps / external CI for the modern path. DC only when you specifically need its OCP-only image-trigger feature without external CI.
- **Myth:** "S2I is a black box; I have no control over the build."
  **Truth:** S2I builder images are open and customisable. Add scripts via `.s2i/bin/` in your repo (assemble, run, save-artifacts hooks). Customise base images to add packages. Or use **Docker strategy** BuildConfig for full Dockerfile control. S2I covers 80% case; Docker covers the rest.
- **Myth:** "OpenShift Pipelines is just rebranded Jenkins."
  **Truth:** **Pipelines = Tekton**, container-native CI/CD where each Task runs as a Pod. No Jenkins server, no plugin sprawl, no JVM tuning. Tekton has its own Hub of reusable Tasks. Different paradigm from Jenkins; better-suited to K8s-native workflows.

## Recap

Built-in: S2I + BuildConfig + ImageStream + registry. Managed Operators: Pipelines + GitOps + Serverless + Service Mesh + Dev Spaces. Use Deployment for new workloads.

**Next — O7: OpenShift Storage.** ODF (Ceph + NooBaa + Rook) for block/file/object; Local + LVM Storage Operators (single-node/edge); CSI per-cloud (vSphere, EBS, Disk/File, GCE PD); RWX storage; snapshots; OADP (Velero-based); registry storage; monitoring storage.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
