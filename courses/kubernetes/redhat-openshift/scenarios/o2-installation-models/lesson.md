# K-OCP O2 — O2 · Installation Models

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O2 · Installation Models
> Companion preview: `/preview-kubernetes-ocp-lesson-02.html`.

---

**🎯 If you remember nothing else:** **Pick installer by environment: IPI for cloud + supported bare-metal; UPI when IPI doesn't fit; Assisted for guided bare-metal install with a SaaS UX; Agent-based for disconnected. SNO/3-node/2-node compact for edge. Disconnected = mirror registry + oc-mirror + OSUS.**

## 1. IPI vs UPI — automated vs DIY infrastructure

**IPI (Installer-Provisioned Infrastructure)** = `openshift-install` creates everything: VMs/instances, networks, load balancers, DNS records, then bootstraps the cluster. Cloud platforms (AWS, Azure, GCP, OpenStack) and supported bare-metal flavours. *Fastest path; least flexibility.*
    **UPI (User-Provisioned Infrastructure)** = you pre-create the infrastructure (compute, network, LB, DNS) per the install docs; `openshift-install` generates Ignition configs that you serve to nodes booting from RHCOS. *For bare-metal flavours not yet IPI-supported, custom networking, regulated environments where infra provisioning is owned by another team.*
    **Assisted Installer** (assisted-service / SaaS UI at `console.redhat.com/assisted-installer`) — guided wizard for bare-metal: download discovery ISO, boot nodes, the wizard finds them and walks you through cluster creation. Lower friction than UPI; more flexibility than IPI for bare-metal.
    **Agent-based Installer** = Assisted Installer's engine packaged for *disconnected / air-gapped* environments. `openshift-install agent create image` bakes a self-contained ISO with all artifacts; boot nodes from it; cluster comes up with no internet access required. *The path for regulated bare-metal / SCIF / classified environments.*

## 2. Cluster shapes — multi-node, SNO, 3-node, 2-node compact

Default: **3 control-plane (master) + ≥2 worker** nodes. Production minimum.
    **Single Node OpenShift (SNO)** — control plane + worker on one node. Edge sites; constrained environments. Lower availability (no zone redundancy) but full OCP API surface.
    **Compact 3-node cluster** — 3 master nodes that *also* run worker workloads (master taint removed). Use case: small clusters where 3+2 is overkill; pay for 3 nodes total instead of 5.
    **Two-node compact** — newer support shape: 2 nodes that share control plane + worker duties via a witness node for arbitration. Edge / cost-constrained scenarios.
    **Sizing guidance:** SNO for edge / dev / CRC-on-server; 3-node compact for small prod; multi-node default for general prod; 5+ control-plane only for very large clusters or specific HA requirements.

## 3. Platforms + install-config + Ignition + bootstrap

**Platforms IPI-supported**: bare metal (with Redfish for some hardware), vSphere, AWS, Azure, GCP, OpenStack, IBM Cloud. UPI works on more (any platform that boots RHCOS).
    **The install dance:**
    
      - `openshift-install create install-config` — interactive prompts → `install-config.yaml`. Pull secret from console.redhat.com.

      - `openshift-install create manifests` — generates K8s manifests. Customise here (network policies, MachineConfigs, etc.).

      - `openshift-install create ignition-configs` — generates `bootstrap.ign`, `master.ign`, `worker.ign` (Ignition is the RHCOS first-boot config format).

      - Boot the **bootstrap node** from RHCOS pointed at `bootstrap.ign`. It runs a temporary apiserver + etcd to bootstrap the real control plane.

      - Boot **3 master nodes** from RHCOS pointed at `master.ign`. They join the bootstrap apiserver, form the real etcd quorum, and the real apiserver takes over.

      - Bootstrap node is destroyed (`openshift-install wait-for bootstrap-complete`).

      - Worker nodes boot from `worker.ign`, join the cluster, become Ready.

      - `openshift-install wait-for install-complete` — cluster operators reconcile; cluster Available.

    
    **DNS requirements**: `api.<cluster>.<basedomain>` (apiserver), `api-int.<cluster>.<basedomain>` (internal apiserver from nodes), `*.apps.<cluster>.<basedomain>` (Routes wildcard). Get these wrong and you debug for hours.

## 4. Disconnected installs + oc-mirror + OSUS

**Disconnected (air-gapped) installs** are common in regulated industries (defence, banking, healthcare). The cluster has no internet access. Required:
    
      - **Mirror registry** — internal container registry (Quay, Harbor, or the small `mirror-registry` Quay flavour Red Hat ships) holding all OCP images + Operator catalog images.

      - **oc-mirror** — Red Hat tool to mirror OCP releases + selected Operators from public catalogs to your internal mirror. ImageSetConfiguration declaratively defines what to mirror.

      - **imageContentSourcePolicy / ImageDigestMirrorSet** — cluster-side resources that redirect `quay.io/openshift-release-dev/...` pulls to your mirror.

      - **Agent-based Installer** (above) — bakes everything into an ISO for cluster bootstrap without internet.

    
    **OpenShift Update Service (OSUS)** = the upgrade-graph service. Public (cloud-connected) clusters fetch the graph from `api.openshift.com/api/upgrades_info/v1/graph`. Disconnected clusters need their own OSUS instance (Red Hat ships an Operator) fed by mirrored upgrade-graph data.

## Before / After

**Before.** Pre-IPI installs were 2-3 weeks of pre-flight: VM + network + LB + DNS + storage prep, manual Ignition file generation, manual bootstrap dance. Disconnected installs were a research project. Bare-metal had no installer; you wrote bash. Mistakes at install time meant tear-down + restart.

**After.** Modern OCP: **IPI** in cloud or supported bare-metal — minutes from `openshift-install create cluster` to working cluster. **Assisted Installer** guides bare-metal via SaaS UI. **Agent-based** handles air-gapped. **oc-mirror** codifies disconnected mirroring. **SNO + compact 3-node + 2-node** shapes for cost-constrained / edge.

*Pick the installer that matches your environment and operating model. The four installers cover almost every reasonable shape.*

## Analogy — the K-Foundry bay

The **Construction Site** at K-Foundry is where you build a foundry from the ground up. Four contractor types are available.
    The **Turnkey Contractor (IPI)** shows up with everything: trucks, materials, foundation crew, framers, electricians. They build the foundry top-to-bottom; you sign one contract. Available in major metro areas (cloud platforms + supported bare-metal). **Assemble-Your-Own Contractor (UPI)** ships the materials but you bring the foundation crew, electricians, and zoning permits — you pre-build the lot, they hand you blueprints (Ignition configs). For unusual sites where the Turnkey contractor can't go.
    The **Guided Wizard (Assisted Installer)** is a Red Hat-hosted concierge that walks you through bare-metal step-by-step via a web wizard. Lower friction than UPI; more flexibility than IPI. The **Field Engineer (Agent-based)** packs every tool + material into a single shipping container that ships to your air-gapped site — no internet needed.
    Cluster shapes: full 3+2 production foundry; *single-node compact* (SNO) for a one-room edge foundry; *3-node compact* where the 3 masters also do worker duty; *2-node compact* with a witness node for arbitration.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| Turnkey Contractor | IPI (Installer-Provisioned Infrastructure) |
| Assemble-Your-Own Contractor | UPI (User-Provisioned Infrastructure) |
| Guided Wizard concierge | Assisted Installer (SaaS UI on console.redhat.com) |
| Field Engineer + sealed container | Agent-based Installer (air-gapped ISO) |
| Foundation pour blueprints | Ignition configs (bootstrap.ign, master.ign, worker.ign) |
| Temporary site office | Bootstrap node (temp apiserver + etcd) |
| Real foundry building | Permanent control plane (3 masters) |
| Day-1 worker shifts | Worker nodes joining |
| Single-room edge foundry | Single Node OpenShift (SNO) |
| 3-room compact (rooms double up) | Compact 3-node cluster (masters also workers) |
| 2-room + arbiter | Two-node compact + witness |
| Sealed warehouse of parts | Mirror registry |
| Parts-shipping manifest | oc-mirror + ImageSetConfiguration |
| Foundry repair-schedule oracle | OpenShift Update Service (OSUS) |

⚠️ *Analogy stops here:* A real construction site has fixed permits and zoning; OCP installs adapt to whatever environment you have, but DNS misconfiguration is the silent killer no metaphor captures.

## ELI5 / ELI10

**ELI5.** There are four ways to build the factory: turnkey (cloud — fastest), assemble-your-own (you do the prep), guided (web wizard for bare-metal), or field-engineer (sealed container for sites with no internet). Pick by where you're building.

**ELI10.** OCP install paths: IPI (installer creates infra; cloud + supported bare-metal), UPI (you pre-create infra; broader bare-metal), Assisted Installer (SaaS-guided wizard for bare-metal), Agent-based (air-gapped ISO). Cluster shapes: 3+2 default, SNO single-node, 3-node compact, 2-node + witness. Disconnected = mirror registry + oc-mirror + OSUS. Bootstrap dance: install-config → manifests → ignition-configs → bootstrap node temporary apiserver → masters join → bootstrap dies → workers join → cluster Available.

## Real-world scenarios

- **Bank — Agent-based on air-gapped bare metal.** Air-gapped data center, no internet. Agent-based Installer + internal Quay mirror + oc-mirror to populate the mirror with target OCP version + ~12 chosen Operators. Disconnected OSUS Operator for upgrade-graph access. Single ISO boots all 5 nodes; cluster Available in 90 minutes.
- **Telco — SNO at 800 cell sites via Assisted.** Each cell site needs OCP. Single-node OpenShift via Assisted Installer; bare-metal hardware fleet pre-provisioned. RHACM (covered later) registers the SNOs into a fleet for centralized policy + apps.
- **Bare-metal startup — IPI saves 2 weeks.** A startup adopts OCP on Dell servers with iDRAC (Redfish supported). IPI bare-metal: `openshift-install create cluster` handles BMC interaction, RHCOS provisioning, network setup. Cluster Ready in 90 minutes vs the 2 weeks UPI would have taken.
- **DNS bug — bootstrap stalled, fixed in 10 minutes.** Bootstrap stalled. Engineer checks DNS: `api-int.cluster.basedomain` resolves but to wrong IP (typo in DNS zone). Corrected; bootstrap completes within 10 minutes. *Postmortem: pre-flight DNS validation script before every install.*

## Common misconceptions

- **Myth:** "UPI is harder — always use IPI."
  **Truth:** UPI is the right call when: IPI doesn't support your platform/version combo; another team owns infra provisioning; you have specific networking / BMC requirements IPI can't express. UPI gives you control over every infra detail; IPI hides them. Both are valid; pick by need.
- **Myth:** "Disconnected install means no upgrades."
  **Truth:** Disconnected clusters DO upgrade — via mirrored OSUS data + mirrored release images. `oc-mirror` updates your mirror with new releases on a schedule (you sync from internet-connected staging or sneakernet). Cluster's ClusterVersion sees new versions in its disconnected OSUS feed and upgrades normally.
- **Myth:** "SNO is just OCP on a small VM."
  **Truth:** SNO is a specific cluster topology: control plane + worker on one node, etcd not quorum (single etcd; data resilience via storage backup). Different from "OCP on small VM" — uses a specific install profile that disables expectations of multi-master HA. Real edge cluster, not a dev shortcut.

## Recap

Four installers + four cluster shapes + bootstrap dance + disconnected mirror pattern. The Construction Site map is internalised.

**Next — O3: OpenShift Networking.** OVN-Kubernetes, cluster/service/machine networks, IngressController + Routes vs Ingress vs Gateway API, NetworkPolicy + EgressIP / Egress firewall, Multus + SR-IOV / DPDK, MetalLB Operator, Submariner, NetObserv.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
