# K-VAN V5 — V5 · Core Add-ons (CoreDNS, Gateway, cert-manager, CSI, observability, GitOps)

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V5 · Core Add-ons
> Companion preview: `/preview-kubernetes-vanilla-lesson-05.html`.

---

**🎯 If you remember nothing else:** Day-1 add-on stack: **CoreDNS** (kubeadm installs; customise for stub zones), **metrics-server** (HPA + kubectl top), **Gateway controller** (Envoy Gateway / Cilium Gateway / Contour — Ingress NGINX EOL 2026), **cert-manager**, **CSI driver** + **snapshot-controller**, **ExternalDNS**, **SOPS or Sealed Secrets**, **kube-prometheus-stack**, **Loki or Vector + S3**, **Kyverno**, **Falco**. Install via **Argo CD App-of-Apps** from git.

## 1. Why add-ons need their own discipline

kubeadm gives you the apartment building. Add-ons are everything else humans expect to live there: water (DNS), power (metrics), mail (Gateway / Ingress), security (cert-manager + policy), the basement (storage CSI), the security camera system (Falco), the maintenance log (logging stack), the energy meter (monitoring). Without these, the building is structurally complete but uninhabitable.
    Critical principle: **add-ons are infrastructure**, not "things ops installs by hand." Treat them as code: pinned versions, declarative manifests, GitOps reconciliation. The cluster reconciles its own add-on stack from git the same way Deployments reconcile their Pods.

## 2. What every cluster needs

Add-onWhat it doesCommon choice
      
        CoreDNSIn-cluster DNSkubeadm-installed; customise via ConfigMap
        metrics-serverPod/node CPU+memory for HPA, kubectl topkubernetes-sigs/metrics-server
        Gateway controllerL7 traffic ingress (host/path routing, TLS)Envoy Gateway, Cilium Gateway, Contour
        cert-managerApp-layer X.509 issuance + rotationcert-manager.io + Let's Encrypt or Vault PKI
        CSI driverPersistent storageLonghorn (on-prem block), Rook-Ceph, vSphere CSI
        snapshot-controllerVolumeSnapshot supportkubernetes-csi/external-snapshotter
        ExternalDNSSync K8s Services + Ingresses to DNS providerkubernetes-sigs/external-dns
        Sealed Secrets / SOPSGit-stored encrypted secretsbitnami-labs/sealed-secrets, getsops/sops
        kube-prometheus-stackPrometheus + Grafana + AlertManagerprometheus-community/kube-prometheus-stack
        LoggingCluster log collectionLoki + Vector + S3, or ELK, or vendor
        Policy engineAdmission policiesKyverno (or OPA Gatekeeper)
        Runtime securitySyscall-level threat detectionFalco
        Argo CDGitOps for everything aboveargoproj/argo-cd

## 3. Chicken and egg: who installs Argo CD?

Argo CD will reconcile every other add-on from git — but Argo CD itself has to be installed somehow. Three patterns:
    
      - **Bootstrap script**: a small shell + Helm one-liner that installs Argo CD, then applies a single "root" Application that points at the rest of git. After that initial bootstrap, Argo CD manages itself.

      - **Cluster API + ClusterResourceSet**: in CAPI environments, a ClusterResourceSet attaches Argo CD to every new workload cluster automatically.

      - **Talos extension**: bake the Argo CD manifests into the Talos machine-config so they apply at first boot.

    
    The standard repo layout:
    `k8s-platform/
├── bootstrap/argocd-install.sh
├── apps/
│   ├── root.yaml                 # App-of-Apps pointing at apps/*
│   ├── coredns/
│   ├── metrics-server/
│   ├── gateway-envoy/
│   ├── cert-manager/
│   ├── csi-longhorn/
│   ├── kube-prometheus-stack/
│   └── ...
└── overlays/{prod,staging,dev}/`

## 4. Pinning, upgrading, retiring

Each add-on is a separate project with its own release cadence. Treat them like dependencies in a programming language:
    
      - **Pin versions** in Helm chart references. Never use "latest" on production.

      - **Update intentionally**: PR to bump version, Argo CD detects diff, reviewer approves the resulting object diff before sync.

      - **Test on staging cluster first.** Same Helm version + same K8s version.

      - **Retire EOL add-ons.** Ingress NGINX is EOL end of 2026 — migrate to a Gateway-API-conformant controller.

    
    Special-case: **dashboard**. The Kubernetes Dashboard is included in many install guides but rarely justified for production — Grafana + Hubble + ArgoCD UI cover the use cases more securely. If you do install it, lock it down (auth, RBAC, no NodePort/LoadBalancer expose).
    [ deep dive — skip if new ]For air-gapped: every add-on's images need to live in your internal registry. Helm charts often default to images on Docker Hub / Quay; override with `--set image.registry=harbor.corp`. Rebuild the bootstrap with these overrides.

## Before / After

**Before.** Add-ons installed by hand, one per ticket. No record of versions. "Why does staging have 1.14 and prod has 1.11?" answered with "someone upgraded staging." Add-on outage requires log archeology to know what should be running.

**After.** One git repo. Argo CD reconciles every add-on. `kubectl get applications -n argocd` shows current state. Versions pinned. Adding a cluster = pointing Argo CD at the same path. Outages = git revert + sync.

Add-on stack as code is the difference between operating one cluster and operating a fleet.

## Analogy — the K-Frontier site

Outbuildings is the fifth site. The main house is up; the wiring is in. Now the property needs the supporting buildings: well house (DNS), shed (metrics), garage (Gateway), workshop (cert-manager), root cellar (storage CSI), watchtower (Falco), library (logging), barn (monitoring). Each outbuilding has its own purpose, but they all need to be planned together: where the path runs, where the power feeds in, who maintains them. The general contractor (Argo CD) coordinates: pulls all the building plans from git, reconciles them onto the property, keeps them updated.

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| Well house (always-on water) | CoreDNS |
| Shed with the meter readings | metrics-server |
| Garage facing the road | Gateway controller (Envoy / Cilium / Contour) |
| Notary workshop with stamping press | cert-manager |
| Root cellar | CSI driver + snapshot-controller |
| Address-book sign at the gate | ExternalDNS |
| Locked safe with vault keys | Sealed Secrets / SOPS |
| Library + observatory | Logging + monitoring stacks |
| Watchman + alarm panel | Kyverno + Falco |
| General contractor coordinating it all | Argo CD App-of-Apps |

⚠️ *Analogy stops here:* The analogy stops here: real add-ons aren't separate buildings — they're Pods running on the same nodes as workloads, sharing the cluster's resources. Capacity planning has to account for the add-on stack's baseline load (~10-15% of cluster CPU/memory).

## ELI5 / ELI10

**ELI5.** The house is built and wired. Now you build the well, the shed, the garage, the watchman's post — all the small buildings that make a homestead actually work.

**ELI10.** kubeadm + CNI = bare cluster. Day-1 add-ons (~10): CoreDNS, metrics-server, Gateway controller, cert-manager, CSI + snapshot-controller, ExternalDNS, Sealed Secrets / SOPS, kube-prometheus-stack, Loki / Vector for logs, Kyverno, Falco. Install via Argo CD from a git repo (App-of-Apps pattern). Pin versions. Test on staging first. Treat the whole stack as code.

## Real-world scenarios

- **A SaaS shipping the same add-on stack to 8 clusters.** Single git repo. Argo CD on each cluster points at the same path with cluster-specific Kustomize overlays. New cluster create = bootstrap script installs Argo CD + applies the root App. 90 minutes from kubeadm done to fully populated cluster.
- **A bank with FIPS + air-gap requirements.** Internal Harbor mirror with all add-on images. Argo CD bootstrap script overrides image registries. Custom cert-manager Issuer pointing at internal Vault PKI. ExternalDNS uses internal CoreDNS (not Route53). Same Argo CD pattern; different registry + DNS configs.
- **A startup graduating from "kubectl apply" to GitOps.** First cluster: 18 manual installs. Migration: clone stack into a git repo, install Argo CD, import existing resources via `argocd app create --upsert`. Two weeks of validation. Then turn off manual access. Drift impossible.
- **A team retiring Ingress NGINX before EOL.** Plan: install Envoy Gateway alongside Ingress NGINX. Migrate one Ingress at a time to HTTPRoute. Validate. Decommission Ingress NGINX. Deadline: end of 2026 (when ingress-nginx EOLs). Started Q2; finished Q4.

## Common misconceptions

- **Myth:** "Argo CD is overkill for a single cluster."
  **Truth:** Even one cluster benefits from declarative reconciliation: drift detection, audit log via git, easy disaster recovery (cluster gone → new kubeadm + bootstrap Argo CD + git reconciles everything). The overhead of Argo CD itself is ~50 MB.
- **Myth:** "Helm + a Makefile is good enough."
  **Truth:** Works until two clusters diverge or someone hand-patches a resource and forgets to update the Makefile. Argo CD detects drift; `helm install` doesn't.
- **Myth:** "Add-ons are install-and-forget."
  **Truth:** Each add-on has its own release cadence + CVE history + breaking-change pattern. Treat them like any other dependency: review changelogs before bumping, test on staging, monitor deprecations.

## Recap

~10 day-1 add-ons installed via Argo CD App-of-Apps from git. Pin versions. Test on staging. Same stack across every cluster.

**Next — V6: Cluster Configuration.** The knobs you tune after install: API server flags, audit, encryption, kubelet eviction, scheduler profiles, RuntimeClass.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
