# K-OCP O1 — O1 · OpenShift Architecture

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O1 · OpenShift Architecture
> Companion preview: `/preview-kubernetes-ocp-lesson-01.html`.

---

**🎯 If you remember nothing else:** **OCP = upstream K8s + Red Hat's opinionated additions (Routes, SCCs, OperatorHub-everywhere, integrated OAuth/registry/console). RHCOS is immutable + MCO-managed. CVO orchestrates ~30 cluster operators. Pick the deployment shape that matches your operating model: OCP / OSD / ROSA / ARO / OKD / HyperShift / MicroShift / CRC.**

## 1. What OCP adds on top of upstream K8s

**OpenShift Container Platform (OCP)** is Red Hat's opinionated K8s distribution. It includes upstream K8s plus a curated set of additions and replacements:
    
      - **Routes** — Red Hat's ingress primitive (predates Ingress; handles TLS edge / passthrough / re-encrypt termination cleanly). Coexists with K8s `Ingress` + Gateway API; OpenShift Routes are still the workhorse.

      - **BuildConfigs / Builds / ImageStreams / ImageStreamTags** — built-in CI primitives. **S2I (Source-to-Image)** = build container images from source code without writing a Dockerfile.

      - **Templates** — pre-OperatorHub mechanism for app templates; still used.

      - **Security Context Constraints (SCCs)** — Red Hat's pre-PSA admission system. Default is `restricted-v2` (non-root, dropped capabilities, seccomp). Stricter than K8s' historical PSP defaults.

      - **Projects** — OCP's namespace-with-extra-metadata. Every K8s namespace = a Project, with a `ProjectRequest`, default rolebinding policies, and self-provisioner support.

      - **Integrated OAuth server** — own OAuth provider built into the cluster; backs HTPasswd, LDAP, OIDC, GitHub, etc., providers.

      - **Integrated container image registry** — built-in registry (image-registry.openshift-image-registry.svc) for ImageStreams + builds.

      - **OperatorHub-everywhere** — every add-on (logging, monitoring, networking, storage, dev tools) ships as an Operator via OLM.

## 2. Eight deployment shapes — pick the operating model

OCP isn't one product — it's a family of deployments under the same software:
    
      - **OpenShift Container Platform (OCP)** — self-managed; you operate the cluster + control plane. Bare metal, vSphere, AWS, Azure, GCP, OpenStack.

      - **OpenShift Dedicated (OSD)** — Red Hat-managed OCP on AWS or GCP. Red Hat operates the control plane + nodes; you operate workloads.

      - **ROSA (Red Hat OpenShift Service on AWS)** — joint AWS + Red Hat managed. Native AWS billing + integration; Red Hat does the K8s lifting.

      - **ARO (Azure Red Hat OpenShift)** — joint Azure + Red Hat managed. Same idea on Azure.

      - **OpenShift on IBM Cloud** + **OpenShift on Google Cloud** — managed-OCP on those clouds.

      - **OKD** — community / upstream-development distribution of OCP. Same code, no Red Hat support.

      - **Hosted Control Planes (HyperShift)** — control planes run as Pods inside another OCP cluster. Density: many lightweight clusters share underlying compute.

      - **MicroShift** — single-node OCP for edge devices. **OpenShift Local (CRC)** — single-node OCP for laptops + dev environments.

    
    **Pick by operating-model intent:** self-managed (OCP) for full control + bare-metal / hybrid; managed (ROSA / ARO / OSD / IBM / GCP) when Red Hat or your cloud provider should run the K8s lifting; HyperShift for cluster-fleet density; MicroShift / CRC for edge / dev.

## 3. RHCOS + MCO + CVO + OLM — the four operators that run OCP

**RHCOS (Red Hat CoreOS)** = OCP's node OS. *Immutable, ostree-based* — you don't apt/yum install on it; OS changes happen by redeploying a new ostree image. SSH disabled by default (use `oc debug node/...` instead). Includes CRI-O (container runtime), kubelet, NetworkManager, and a handful of system services.
    **Machine Config Operator (MCO)** manages RHCOS. You declare changes via **MachineConfig** YAML resources (kernel args, systemd units, files, ignition snippets). MCO renders them into a final ostree-like config per **MachineConfigPool** (master, worker, custom pools), drains nodes, applies the new config, reboots, validates. *This is how you customize node OS without SSH or hand-editing.*
    **Cluster Version Operator (CVO)** orchestrates ~30 **ClusterOperators** — each manages one piece of OCP (authentication, console, dns, etcd, ingress, monitoring, network, storage, etc.). CVO ensures all CO's reconcile to the cluster's declared version. *Cluster health = all CO's Available + not Degraded + not Progressing (during steady state).*
    **OLM (Operator Lifecycle Manager)** = the operator that manages other operators. OperatorHub catalogs (CatalogSources) → Subscription → InstallPlan → ClusterServiceVersion (CSV) → operator running. *Almost every OCP add-on installs through OLM.*
    **oc** CLI = kubectl plus OCP-aware commands: `oc new-app`, `oc new-build`, `oc start-build`, `oc adm`, `oc debug`, `oc rsync`, `oc port-forward`. Works everywhere kubectl works; learn *both*.

## 4. Web console (Administrator + Developer) + edge variants

The OCP **web console** ships two perspectives:
    
      - **Administrator perspective** — cluster-wide view: nodes, machines, operators, monitoring, storage, networking, RBAC. For platform engineers.

      - **Developer perspective** — project-scoped: topology view (pods/services/routes graph), build pipeline, dev catalog (templates, helm charts, S2I builders), monitoring of own workloads. For app developers.

    
    Both perspectives sit on the same RBAC; users see what their roles allow.
    **Edge variants:**
    
      - **Single Node OpenShift (SNO)** — full OCP on one node. Edge deployments at retail / branch / industrial.

      - **MicroShift** — even smaller (~1 GB RAM): minimal OCP for ultra-edge devices, IoT gateways, small footprint deployments.

      - **OpenShift Local (CRC — CodeReady Containers)** — single-node OCP on laptop. For dev + experimentation. Drives `crc start`; ~10 GB disk + ~10 GB RAM.

    
    All three variants register into a fleet via Red Hat Advanced Cluster Management (ACM) — covered in O10.

## Before / After

**Before.** Pre-OCP K8s deployments were assembly-required: pick a CNI, install Helm charts for ingress + monitoring + logging + GitOps + dev tools + registry; integrate auth via custom OIDC plumbing; bake AMIs / images per cloud; write per-cluster scripts for upgrades. *Six weeks of platform engineering before the first developer Pod ran.* No vendor accountability if any one piece broke.

**After.** OCP ships an **opinionated platform**: Routes (ingress), integrated OAuth + registry + console + monitoring + logging, OperatorHub-everywhere (one place to install certified add-ons), CVO orchestrating cluster operators, RHCOS as the immutable node OS managed by MCO, oc CLI extending kubectl. **Day-1 cluster is production-shaped**; the trade-off is learning Red Hat's opinions (SCCs, Routes vs Ingress, Projects-as-namespaces, oc adm flow). One vendor accountable for the whole platform.

*OCP trades K8s flexibility for Red Hat opinionation + enterprise support. The cost is learning Red Hat's additions; the benefit is platform-team-in-a-box.*

## Analogy — the K-Foundry bay

K-Foundry is the Red Hat enterprise factory. The **Welcome Hall** is where every visitor enters. On the wall is a giant floor plan showing the whole foundry: 13 bays, each handling a different production stage. The Foundry Master (you, the OCP platform admin) hands you a hard hat at the door.
    Unlike DIY K8s where you arrive with empty land, OCP's Welcome Hall has the building *already built*: the central forge (apiserver), the safety regulations posted (SCCs), the conveyor system installed (Routes + Service mesh), the safety inspector's booth ready (Compliance Operator), the operator hub stocked (OLM), the maintenance schedule on the wall (CVO + ClusterOperators). You add your products (workloads); the foundry comes equipped to make them.
    The Foundry has 8 deployment shapes — same blueprint, different operating models. Self-build the foundry (OCP), rent a turnkey foundry from Red Hat (OSD), rent one jointly with a hyperscaler (ROSA on AWS / ARO on Azure / IBM Cloud / GCP), use the community blueprint (OKD), pack many foundries into one (HyperShift), or run a tiny one at the edge (MicroShift / SNO / CRC).
    The **Cluster Version Operator (CVO)** is the Foundry Master's lieutenant — keeps every operator on the floor working. The **Machine Config Operator (MCO)** manages the floors themselves (RHCOS). The **OLM** manages all the specialty operators that visit the foundry.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| Welcome Hall floor plan | OCP architecture overview |
| Foundry Master | OCP platform admin (you) |
| Foundry Master's lieutenant | Cluster Version Operator (CVO) |
| Floor manager | Machine Config Operator (MCO) |
| Specialty-operator scheduler | Operator Lifecycle Manager (OLM) |
| Conveyor system | Routes (TLS edge / passthrough / re-encrypt) |
| Build mold + casting press | S2I (Source-to-Image) + BuildConfig + ImageStream |
| Safety regulations posted | Security Context Constraints (SCCs) |
| Project area on the floor | OpenShift Project (= K8s namespace +) |
| Front desk badge issuer | Integrated OAuth server |
| Internal parts warehouse | Integrated container registry |
| Hardened immutable floor surface | RHCOS (immutable ostree node OS) |
| Foundry Master's CLI | oc CLI (kubectl + OCP-aware commands) |
| Two views of the floor | Web console — Administrator + Developer perspectives |
| Foundry-network of branch foundries | Hosted Control Planes (HyperShift) + ACM |

⚠️ *Analogy stops here:* A real foundry has fixed equipment; OCP's opinionated platform is software-defined and reshapes via Operators. Some workloads need bespoke configs that fight the opinionated defaults — that's when the foundry metaphor breaks.

## ELI5 / ELI10

**ELI5.** Red Hat sells a Kubernetes that's already set up like a factory — the conveyor belts, safety officers, registry, login, dev tools all built in. You can build your own factory (DIY K8s) or buy this one with all the equipment included.

**ELI10.** OpenShift = upstream K8s + Red Hat's opinionated additions (Routes, SCCs, BuildConfigs, S2I, Projects, OAuth, registry, OperatorHub-everywhere) + RHCOS immutable node OS + Machine Config Operator + Cluster Version Operator orchestrating ~30 ClusterOperators + Operator Lifecycle Manager for add-ons. Eight deployment shapes (OCP self-managed, OSD, ROSA, ARO, IBM, GCP, OKD, HyperShift, MicroShift / SNO / CRC). oc CLI extends kubectl. Web console has Admin + Dev perspectives.

## Real-world scenarios

- **Bank — picks ROSA for managed OCP on AWS.** A regulated bank standardising on OCP. They have an AWS-first cloud strategy. Pick **ROSA** — Red Hat operates the control plane + nodes via AWS native services; the bank operates workloads + identity. Native AWS billing; PrivateLink to existing AWS infra. *Compliance posture inherits from Red Hat's ROSA service controls.*
- **Telco edge — SNO + MicroShift across 800 sites.** A telco runs OCP at 800 cell sites. Each site has constrained compute. Edge sites get **SNO** (full OCP on one node) for the larger ones; remote IoT gateways get **MicroShift**. All registered in **RHACM** (covered in O10). One pane of glass for 800 mini-clusters.
- **Migration — DIY K8s + 12 Helm-installed add-ons → OCP.** A platform team running 6 self-managed K8s clusters with Argo CD, Prometheus, Loki, Linkerd, cert-manager, sealed-secrets, etc., all installed via Helm. Drift across charts; upgrade hell. Migration to OCP: each Helm chart maps to a Red Hat-supported Operator; OLM-installed; one supported version per Operator per OCP minor. *Reduced from 12 self-installed Helm charts to 12 OLM-managed Operators with vendor support.*
- **Dev experience — CRC for laptop dev, OCP-bare-metal for prod.** A 100-engineer team. Dev: **OpenShift Local (CRC)** on every developer laptop — same OCP APIs as prod; `oc new-app` + `oc new-build` work locally. Prod: OCP on bare metal in two on-prem data centres. *Same Routes, same SCCs, same OAuth — dev and prod feel identical from the developer's side.*

## Common misconceptions

- **Myth:** "OCP is just K8s with a wrapper."
  **Truth:** OCP includes meaningful additions: Routes (predate Ingress, handle TLS termination), SCCs (predate PSA, stricter defaults), Projects (namespace + metadata + self-provisioning), OAuth server, integrated registry, ImageStreams, BuildConfigs, S2I, OperatorHub-everywhere, CVO orchestrating CO's. *You can use kubectl for everything but you'll miss half the workflow without oc + OCP-aware concepts.*
- **Myth:** "RHCOS is just RHEL with K8s installed."
  **Truth:** RHCOS is **immutable ostree-based** — no apt / yum / package install at runtime. Changes happen by deploying new ostree images managed by the **Machine Config Operator**. SSH disabled by default. *You customise nodes via `MachineConfig` YAML, not by SSH-ing to nodes*. RHEL is the upstream; RHCOS is OCP's opinionated subset for cluster nodes only.
- **Myth:** "OLM is required for all my K8s operators."
  **Truth:** OLM manages OperatorHub-installed operators. You can *still* install bring-your-own operators directly via `kubectl apply -f operator.yaml` + RBAC + CRDs. OLM's value: lifecycle management (versions, upgrades, dependencies, channels) + a curated catalog. For Red Hat-supported workloads, OLM is the path. For custom internal operators, OLM is optional.

## Recap

OpenShift = K8s + Red Hat opinionated additions + RHCOS + MCO + CVO + OLM + 8 deployment shapes. The Welcome Hall floor plan is internalised; choose the deployment shape + understand the four core operators (CVO, MCO, OLM, OAuth).

**Next — O2: Installation Models.** IPI vs UPI; Assisted Installer; Agent-based Installer; SNO + compact 3-node + two-node; bare-metal + vSphere + AWS + Azure + GCP + OpenStack; disconnected installs + mirrored registries + oc-mirror; install-config + Ignition + bootstrap node + OSUS.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
