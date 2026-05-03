# K-OCP O5 — O5 · Operators and OLM

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O5 · Operators and OLM
> Companion preview: `/preview-kubernetes-ocp-lesson-05.html`.

---

**🎯 If you remember nothing else:** **OLM lifecycle: CatalogSource → Subscription (channel + approval) → InstallPlan (deps + RBAC) → CSV (deploys operator). OperatorGroup defines scope. Pick channel by stability tolerance; pick approval mode by upgrade discipline; resolve dependency conflicts before installing.**

## 1. Operator Hub + CatalogSources

**OperatorHub** is the OCP web console's view of installable operators. Sourced from **CatalogSources**:
    
      - **Red Hat Operators** — supported by Red Hat. Production-ready.

      - **Certified Operators** — third-party (IBM, NetApp, Crunchy, etc.) with Red Hat certification.

      - **Community Operators** — community-maintained. Best-effort.

      - **Red Hat Marketplace** — purchasable operators with billing integration.

      - **Custom CatalogSource** — your internal catalog (hosted in your private registry; supports air-gapped + curated installs).

    
    Each CatalogSource is a Pod running a registry that exposes a gRPC API; OLM queries it to list operators + manifests + dependencies.
    For air-gapped clusters: mirror the catalog images via `oc-mirror`; deploy a private CatalogSource pointing at the internal mirror.

## 2. Subscription + InstallPlan + CSV — the install pipeline

**Subscription** CR — declares: which operator (package name), from which CatalogSource, on which channel, with what approval mode (Automatic / Manual). One Subscription per operator per Project.
    **OLM workflow:**
    
      - You create a Subscription.

      - OLM reads the channel's current head + dependencies; creates an **InstallPlan**.

      - If `installPlanApproval: Automatic`, InstallPlan is auto-approved + executed. If Manual: human runs `oc patch installplan ... --type merge -p '{"spec":{"approved":true}}'`.

      - InstallPlan creates the **ClusterServiceVersion (CSV)** + dependencies + CRDs + RBAC.

      - CSV phases: *Pending → InstallReady → Installing → Succeeded* (or Failed). Operator Pod runs.

      - For upgrades: when CatalogSource publishes a new CSV in the channel, OLM creates a new InstallPlan; same approval flow applies.

    
    **Channel choice:** *stable* (production), *fast* (latest GA, faster cadence), *preview* (pre-release / candidate), version-pinned channels (e.g. `4.14`). Operator authors define the channels.
    **Approval mode:**
    
      - **Automatic** — OLM applies new versions when they appear in the channel. Use for non-prod or operators with great backward compatibility.

      - **Manual** — OLM creates the InstallPlan but pauses; human approves. Use for prod / regulated.

## 3. OperatorGroup + scope (AllNamespaces / SingleNamespace / OwnNamespace)

**OperatorGroup** defines the namespaces the operator watches + manages. Required: every Project that hosts an OLM-installed operator must have an OperatorGroup.
    **Scope modes:**
    
      - **AllNamespaces** — operator watches every namespace cluster-wide. Default for openshift-operators namespace. For platform-wide operators (e.g. cert-manager Operator).

      - **OwnNamespace** — operator watches only the namespace it's installed in. For Project-scoped operators (e.g. one Postgres Operator per tenant).

      - **SingleNamespace** — operator installed in one namespace, watches another. Less common.

      - **MultiNamespace** — operator watches multiple specific namespaces. Less common.

    
    Operator authors declare which scopes their operator supports (`installModes` in CSV). If your OperatorGroup mode doesn't match a supported installMode, the install fails. *Check the operator's docs before creating the OperatorGroup.*
    **openshift-operators** is the well-known AllNamespaces OperatorGroup namespace; many cluster-wide operators install there.

## 4. Dependencies + broken-operator recovery + custom / certified operators

**Operator dependencies:** when Operator A requires Operator B, OLM's InstallPlan installs B first. If B is unavailable in any catalog, A's install fails. *The most common cause of "my operator won't install" is unmet dependencies.*
    Use `oc describe installplan` to see required + resolved deps. `oc get packagemanifest -A` lists all available operators across catalogs.
    **Broken-operator recovery:**
    
      - CSV in *Failed* state: `oc describe csv <name>` for failure reason; common causes are missing CRD, RBAC denial, image pull failure, dependency conflict.

      - Stuck Subscription: delete + recreate; OLM rebuilds InstallPlan.

      - CSV upgrade stuck mid-flight: `oc delete csv <old-csv>`; OLM's next reconcile installs new CSV cleanly.

      - Last resort: uninstall (delete Subscription + CSV) then reinstall fresh.

    
    **Custom operators:** internal teams build operators with Operator SDK (Go, Ansible, or Helm-based). Publish to your custom CatalogSource. Same OLM lifecycle as Red Hat Operators.
    **Certified Operators** are vendor-supported (IBM Cloud Pak, Crunchy Postgres, NetApp Trident, Confluent, etc.). **Community Operators** are best-effort. *For prod, prefer Red Hat or Certified.*

## Before / After

**Before.** Pre-OLM K8s operator install was Helm + custom RBAC + manual CRD apply per operator. No dependency resolution. No upgrade gates. No cluster-wide visibility into installed operators. Each team's operator drift was their own problem; cluster admins had no inventory.

**After.** OLM standardises operator lifecycle: **CatalogSources** + **Subscriptions** + **InstallPlans** + **CSVs** + **OperatorGroups**. **Channels** for upgrade cadence; **approval mode** for upgrade discipline; **dependency resolution** built in; **cluster-wide inventory** via `oc get csv -A`; **certified + community + custom** CatalogSources.

*OLM is the operator-of-operators. Once you understand its CR pipeline, every OperatorHub install becomes predictable.*

## Analogy — the K-Foundry bay

The **Operator Hub** at K-Foundry is where you order specialty machinery. Four catalogs sit on the counter: Red Hat's officially-supported parts, Certified third-party parts (IBM, NetApp, etc.), Community parts (best-effort), and the Marketplace (purchasable parts).
    You fill out a **Subscription order form**: which part, from which catalog, what version channel, do I want auto-shipping or hand-approval. The Hub creates an **InstallPlan invoice** listing dependencies + RBAC + CRDs that must be installed first. With auto-approval, the invoice processes immediately; with manual approval, you sign off before any work begins.
    Once approved, the **ClusterServiceVersion (CSV) work-order** deploys the operator. The CSV walks through phases: Pending → InstallReady → Installing → Succeeded. Pod is running; operator is reconciling.
    The **OperatorGroup** is the operator's territory permit: AllNamespaces (it patrols the whole foundry) or OwnNamespace (it patrols only one bay). Match the operator's declared installModes; the wrong territory permit causes silent install failures.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| Catalog counter | CatalogSource (Red Hat / Certified / Community / Marketplace / custom) |
| Subscription order form | Subscription CR |
| Channel selection | stable / fast / preview / version-pinned |
| Auto-shipping vs hand-approval | installPlanApproval: Automatic vs Manual |
| InstallPlan invoice | InstallPlan CR (lists deps + RBAC + CRDs) |
| Hand-approval signature | `oc patch installplan ... approved:true` |
| Work order | ClusterServiceVersion (CSV) |
| CSV phases | Pending → InstallReady → Installing → Succeeded (or Failed) |
| Territory permit | OperatorGroup |
| Cluster-wide patrol | AllNamespaces scope |
| Single-bay patrol | OwnNamespace scope |
| Foundry parts inventory | `oc get csv -A` |
| Internal-parts catalog | Custom CatalogSource (private registry) |
| Specialty supported parts | Certified Operators |
| Best-effort parts | Community Operators |

⚠️ *Analogy stops here:* A real catalog has fixed inventory; OperatorHub is a live gRPC service with rolling updates. Operator dependency conflicts are a real failure mode the catalog metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** The Operator Hub is a parts catalog. You fill an order form (Subscription), the office creates an invoice (InstallPlan) listing what else has to be ordered first, you approve it, then the work order (CSV) installs the part.

**ELI10.** OLM = OperatorHub-everywhere lifecycle: CatalogSource (Red Hat/Certified/Community/Marketplace/custom) → Subscription (channel + approval) → InstallPlan (dependencies + RBAC + CRDs) → CSV (deploys operator). OperatorGroup defines scope (AllNamespaces / OwnNamespace / SingleNamespace / MultiNamespace) and must match the operator's declared installModes. CSV phases: Pending → InstallReady → Installing → Succeeded. Manual approval mode pauses at InstallReady for human sign-off; Automatic auto-applies. Use Red Hat or Certified for prod; Community for non-prod.

## Real-world scenarios

- **Bank — manual approval + custom CatalogSource.** A regulated bank uses only operators from their internal CatalogSource (mirrored from Red Hat + curated by the platform team). Every Subscription has `installPlanApproval: Manual`. Operator upgrades require change-control approval; platform engineer runs `oc patch installplan` after approval. *Compliance-clean upgrade trail.*
- **Multi-tenant SaaS — OwnNamespace per-tenant Postgres Operator.** A SaaS where each tenant gets their own Postgres database. Crunchy Data Postgres Operator installed per-tenant Project with OwnNamespace OperatorGroup. Tenant isolation: each tenant's operator only manages their own Postgres CRs. *Operator-per-tenant pattern.*
- **Dependency hell — cert-manager required Compliance Operator first.** Team installs cert-manager Operator. InstallPlan fails: depends on Compliance Operator v1.2+ (for CRD compatibility), and the channel pinned to v1.1 in the cluster. Fix: change Compliance Operator Subscription channel to `stable` (which has v1.2+); cert-manager InstallPlan succeeds on next reconcile. *OLM dependency resolution surfaces these conflicts; `oc describe installplan` tells you.*
- **Stuck CSV — recovered by deleting + reinstalling Subscription.** An operator CSV stuck in Failed for 3 days due to CRD-conflict drama. Recovery: `oc delete subscription <name>` + `oc delete csv <name>` + manually clean orphaned CRDs (rare). Reinstall Subscription; clean CSV install succeeds. *Postmortem: documented recovery runbook.*

## Common misconceptions

- **Myth:** "All Operators install the same way."
  **Truth:** Operators have **different supported installModes**: AllNamespaces, SingleNamespace, OwnNamespace, MultiNamespace. The OperatorGroup must match. Some operators don't support every mode. Read the operator's docs / packagemanifest to know which modes work.
- **Myth:** "Manual approval = no auto-upgrades = safer always."
  **Truth:** Manual approval gives you control over *when* to upgrade — but you must actually approve, otherwise InstallPlans pile up and the operator drifts behind security patches. *Manual is safer only if you have a process to approve regularly.* If unmanned, automatic with a known channel (stable) may be safer in practice.
- **Myth:** "Community Operators are fine for production."
  **Truth:** Community Operators are **best-effort** — no Red Hat support contract, no SLA on bug fixes, may have abandoned upstreams. For prod, prefer **Red Hat Operators** or **Certified Operators**. Use Community for evaluation / non-prod or when the only available option.

## Recap

OLM lifecycle: CatalogSource → Subscription → InstallPlan → CSV. OperatorGroup defines scope. Channels + approval mode are the upgrade-discipline knobs.

**Next — O6: Workloads and Developer Experience.** Source-to-Image (S2I) + BuildConfig + ImageStream + Build; DeploymentConfig (legacy) vs Deployment; Templates; OpenShift Pipelines (Tekton); OpenShift GitOps (Argo CD); Serverless (Knative); Service Mesh (Istio); Dev Spaces (Eclipse Che); internal registry; Helm in OCP; web console workflows.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
