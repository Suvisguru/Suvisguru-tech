# K-OCP O12 — O12 · OpenShift Troubleshooting

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O12 · OpenShift Troubleshooting
> Companion preview: `/preview-kubernetes-ocp-lesson-12.html`.

---

**🎯 If you remember nothing else:** **OCP triage playbook: ClusterOperator status first → CVO state → MachineConfigPool roll status → recent Activity. Diagnostic toolkit: must-gather (default + targeted) + oc adm inspect + oc debug node. Eight common failure pattern families with documented recovery paths.**

## 1. ClusterOperator + CVO + MachineConfigPool triage

**ClusterOperator (CO) degraded** — the most common starting symptom. `oc get co` shows all CO's + their Available / Progressing / Degraded conditions. For each Degraded CO:
    
      - `oc describe co/<name>` — status conditions + reason.

      - `oc logs -n openshift-<name> deployment/<operator>` — operator logs.

      - For some CO's: there's an OperatorHub-installed Operator behind it (e.g., authentication CO has multiple deployments).

    
    **CVO blocked** — Cluster Version Operator can't make progress. `oc describe clusterversion`:
    
      - Conditions: Progressing, Failing, Available.

      - Common: a CO's upgrade is failing → CVO pauses; resolve the CO failure first.

      - Or: ClusterOperator dependency loop; check upgrade graph + admission webhooks.

    
    **MachineConfigPool (MCP) degraded** — RHCOS roll failed.
    
      - `oc describe mcp/<pool>` — node status, drain reason.

      - Most common cause: PDB-blocked drain (node's workloads can't evict due to tight PDB).

      - `oc get nodes -o wide` — find the cordoned node; check why workloads can't drain.

      - Recovery: relax PDB temporarily; manually evict workloads; re-roll the pool.

    
    **Node NotReady** — kubelet not reporting ready.
    
      - `oc adm node-logs <node>` — system logs.

      - `oc debug node/<node>` — privileged debug Pod on the node.

      - Common: kubelet panic, container runtime (CRI-O) error, network partition.

## 2. SCC denial + Routes + cert + registry + OAuth failures

**SCC denial** ("unable to validate against any SCC"):
    
      - `oc describe pod <name>` — admission denial detail.

      - Identify SA + currently-granted SCCs: `oc adm policy who-can use scc/restricted-v2`.

      - Determine fix: rewrite Pod for restricted-v2 (preferred) OR grant the SA an appropriate SCC.

    
    **Route not working / cert issues**:
    
      - `oc describe route <name>` — admitted by IngressController? Cert valid?

      - `oc logs -n openshift-ingress deployment/router-default` — router runtime errors.

      - NetworkPolicy: is openshift-ingress allowed to reach the namespace?

      - For TLS: `openssl s_client -connect <host>:443 -servername <host>` — see what cert is served.

    
    **Internal registry failure**:
    
      - `oc get co/image-registry` — degraded? `oc describe` for reason.

      - Most common: storage backend (PVC zone-mismatch, S3 endpoint unreachable, NooBaa down).

      - Recovery: switch backend to S3 / NooBaa for zone-resilience; restart registry deployment.

    
    **OAuth failures**:
    
      - `oc get co/authentication` — degraded? `oc describe`.

      - Identity provider unreachable (LDAP / OIDC endpoint down)?

      - Cert chain issue (LDAP TLS cert expired)?

      - `oc logs -n openshift-authentication deployment/oauth-openshift`.

## 3. Build + CSV + CatalogSource + OVN-K + DNS Operator failures

**Build failure**:
    
      - `oc get builds -n <ns>` + `oc logs build/<name>`.

      - Common: S2I builder image incompatibility (recently updated builder broke build); pin builder version in BuildConfig.

      - Resource limits: builder Pod ran out of memory (typical for Java).

    
    **Operator CSV failed**:
    
      - `oc describe csv -n <ns> <name>` — failure reason.

      - Common: missing CRD permissions, RBAC, image pull failure, dependency conflict.

      - Recovery: delete Subscription + CSV; reinstall after fixing root cause.

    
    **CatalogSource failure / OLM Subscription stuck**:
    
      - `oc get catalogsource -n openshift-marketplace` + `oc describe`.

      - Common: CatalogSource registry pod failing (image pull from disconnected registry; pod crash loop).

      - Subscription stuck: check `oc describe sub <name>` — InstallPlan available? Approval mode? Channel issues?

    
    **OVN-Kubernetes issues**:
    
      - `oc get pods -n openshift-ovn-kubernetes` — ovnkube-master, ovnkube-node Pods healthy?

      - `oc adm must-gather --image=registry.redhat.io/openshift4/ose-must-gather:latest -- /usr/bin/gather_network_logs` — targeted network gather.

      - Symptoms: cross-Pod traffic broken, NetworkPolicy not enforced, EgressIP failover stuck.

    
    **DNS Operator failures**:
    
      - `oc get co/dns` — degraded?

      - `oc get pods -n openshift-dns` — coredns + node-resolver Pods.

      - `oc rsh <some-pod> nslookup kubernetes.default` — DNS resolution from a Pod.

## 4. etcd recovery + disconnected pull failures + the diagnostic toolkit

**etcd backup/restore** — disaster recovery procedure:
    
      - Backup: schedule `cluster-backup.sh` on a master node; ship snapshot off-cluster.

      - Restore: documented multi-step procedure — declare disaster, restore snapshot to a single master, validate, re-add other masters. **Practice this on a dev cluster before you need it.**

      - etcd quorum loss without backup = cluster rebuild.

    
    **Disconnected pull failures**:
    
      - `oc describe pod <name>` — ImagePullBackOff with auth or NXDOMAIN error.

      - Check `imageContentSourcePolicy` / `ImageDigestMirrorSet` CRs — are the public image refs being redirected to your mirror?

      - Mirror registry reachable? Pod running? Auth secret valid?

      - `oc adm release info <version>` — list all images in the release; check each is mirrored.

    
    **Diagnostic toolkit:**
    
      - **`oc adm must-gather`** — full diagnostic bundle. Targeted: `--image=registry.redhat.io/<operator>-must-gather` for per-operator gather.

      - **`oc adm inspect`** — focused gather on specific namespaces / resources. Lighter than must-gather.

      - **`oc debug node/<name>`** — privileged debug Pod on a specific node. `chroot /host` for full node OS access.

      - **`oc adm node-logs <node> -u <unit>`** — system journal logs from a node.

      - **Insights Advisor** (console.redhat.com) — known-issue checks against your cluster.

      - **Red Hat Knowledge Centered Service (KCS)** — searchable knowledge base of known issues + fixes.

    
    **The standard playbook:** (1) Insights Advisor for known issues; (2) `oc get co` for CO health; (3) `oc get clusterversion` for CVO state; (4) `oc get mcp` for node-roll state; (5) `oc adm must-gather` for support case + postmortem; (6) `oc debug node` for node-level investigation.

## Before / After

**Before.** Pre-OCP K8s troubleshooting was self-assembly: bring-your-own log search (kibana / loki / external), no consolidated diagnostic gather, no targeted Operator gathers. ClusterOperator + CVO concepts didn't exist (per-component upgrade trail). SCC was specific to OCP and engineers came from K8s without it. etcd backup was DIY scripts.

**After.** OCP ships **`oc adm must-gather`** as the canonical diagnostic gather; targeted variants per-operator. **ClusterOperator + CVO + MCP** as triage primitives. **Insights Advisor** as known-issue checker. Documented recovery procedures for etcd disaster recovery + disconnected pull failures + SCC denial + OVN-K + DNS + OAuth + Routes + etc. *Triage discipline + the right diagnostic surfaces.*

*Most OCP outages match a known pattern; the toolkit + playbook turn 4-hour wars into 15-minute recoveries.*

## Analogy — the K-Foundry bay

The **Diagnostic Lab** at K-Foundry is where you go when something's wrong. The triage nurse asks the same questions every time, in the same order.
    First: *"What does the master operator board (CVO) say?"* Second: *"Which specialty operators (CO's) are flashing red?"* Third: *"Are the floor crews (MCPs) stuck mid-roll?"* Fourth: *"What did Red Hat Insights flag yesterday?"*
    The wall has eight common diagnoses pinned: CO + CVO blockages, MCP + Node issues, SCC denials, Route/cert/registry failures, Build/CSV/Catalog issues, OVN-K + DNS Operator failures, OAuth issues, etcd recovery + disconnected pull failures. Each diagnosis has a one-page recovery procedure.
    The **diagnostic toolkit**: `must-gather` (full diagnostic bundle), `inspect` (focused), `debug node` (privileged on-node Pod), `adm node-logs` (system journal). Plus Insights + KCS (known-issue knowledge bases).

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| Master operator board | Cluster Version Operator (CVO) status |
| Specialty operators flashing | ClusterOperator degraded |
| Floor crew stuck mid-roll | MachineConfigPool (MCP) degraded |
| Operator stalled mid-shift | Node NotReady |
| Safety inspector denial | SCC denial — "unable to validate against any SCC" |
| Conveyor door not opening | Route admission failure / cert problem |
| Internal-parts warehouse failure | Internal registry CO degraded |
| Stamp-press jam | Build failure (S2I builder broke) |
| Specialty-machine install failed | CSV failed / Subscription stuck / CatalogSource down |
| Foundry rail network partition | OVN-K node-to-master partition |
| Floor address book down | DNS Operator failure |
| Badge-printer broken | OAuth failure |
| Inventory snapshot rebuild | etcd backup/restore |
| Sealed warehouse pull failure | Disconnected pull failure (mirror registry) |
| Foundry-master diagnostic kit | `oc adm must-gather` / `inspect` / `debug node` |
| Foundry-network knowledge base | Red Hat Insights Advisor + KCS |

⚠️ *Analogy stops here:* A real diagnostic lab can pause; OCP cascading failures can take down adjacent operators in minutes. The metaphor underplays the cascade-failure risk.

## ELI5 / ELI10

**ELI5.** When something hurts, you check the master board first, then look for which operators are flashing red, then ask if any floor crews are stuck. The wall has 8 common diagnoses; pick the matching one.

**ELI10.** OCP triage = (1) Insights Advisor for known issues, (2) `oc get co` for ClusterOperator health, (3) `oc get clusterversion` for CVO state, (4) `oc get mcp` for node-roll state, (5) `oc adm must-gather` for support case + postmortem, (6) `oc debug node` for node-level investigation. Eight failure pattern families: CO/CVO blocked, MCP/Node, SCC, Routes/cert/registry, Builds/CSV/Catalog, OLM Subscription, OVN-K/DNS/OAuth, etcd/disconnected.

## Real-world scenarios

- **Cascading failure — DNS Operator down → 4 CO's degraded.** DNS Operator goes degraded. Cascading: authentication CO can't reach LDAP, image-registry can't reach storage, build can't pull base images, console can't reach apiserver. **Triage**: identify root via Insights or `oc get co` + check timestamps; fix DNS (CoreDNS Pod CrashLoop, kubeconfig misconfig, NodeNetworkConfigurationPolicy regression); cascading CO's recover.
- **MCP stuck — PDB deadlock during upgrade.** MCP/worker stuck Updating for 90 min. `oc describe mcp/worker`: 1 node cordoned + drain blocked. `oc describe pod` on stuck workload: PDB `maxUnavailable: 0` + 3 replicas. Recovery: temporarily increase replicas to 4 (PDB allows 1 disruption when 4 exist); drain proceeds; restore replicas. Postmortem: document workload PDB requirements; pre-flight check before upgrades.
- **SCC denial — anyuid escalation reverted.** Helm chart fails admission: "unable to validate against any SCC." Pod runs as UID 0. Investigation: image was built without USER directive (default = root). Fix: rewrite Dockerfile to `USER 1001`; rebuild; redeploy under restricted-v2 SCC. Avoids granting anyuid SCC permanently.
- **etcd disaster recovery rehearsed quarterly.** A bank simulates etcd quorum loss on a dev cluster. Documented procedure: declare disaster, stop etcd Pods on remaining masters, restore latest snapshot to one master via `etcdctl snapshot restore`, restart cluster operators, validate + re-add other masters. *Procedure validated; runbook current; team trained.*

## Common misconceptions

- **Myth:** "must-gather is huge and slow — only run it for support cases."
  **Truth:** **must-gather is a 5-15 min routine collection**. Run it for any non-trivial incident, even if you don't open a Red Hat case. The bundle has ClusterOperator status, recent events, system logs, configs — all useful for postmortems. Targeted variants (per-operator) are smaller + faster.
- **Myth:** "Restart all Pods to fix it."
  **Truth:** *Almost never the right first step.* Pod restart is a last-resort symptom-treater. Always look at ClusterOperator status, CVO state, MCP roll status, Insights Advisor first. Pod restart hides root cause + may worsen cascading failures by retriggering scheduling pressure.
- **Myth:** "Insights is just nice-to-have telemetry."
  **Truth:** **Insights Advisor surfaces known-issue checks against YOUR cluster** — "this version of cluster-network-operator has a known issue X; here's the KCS article." Saves hours of debugging when the issue is already documented. Disabled by default in air-gapped clusters; manually-fed knowledge base is the fallback.

## Recap

Eight failure pattern families + diagnostic toolkit (must-gather + inspect + debug node + Insights + KCS). Triage discipline turns 4-hour wars into 15-minute recoveries.

**Next — O13: K-OCP Capstone.** Multi-tenant OCP platform (IPI on bare metal or AWS) with ODF + RHACS + OpenShift GitOps + Pipelines + Virtualization workload + RHACM federation; full SCC design + disconnected update + must-gather pack.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
