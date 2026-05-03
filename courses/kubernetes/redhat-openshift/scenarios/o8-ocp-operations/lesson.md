# K-OCP O8 — O8 · OpenShift Operations

> Course: Red Hat OpenShift (K-OCP, prereq: K-COM, ref OCP 4.21+)
> Module O8 · OpenShift Operations
> Companion preview: `/preview-kubernetes-ocp-lesson-08.html`.

---

**🎯 If you remember nothing else:** **CVO orchestrates ClusterOperators on a channel; pick stable for prod, fast for canary, EUS for regulated. MCO + MachineConfigPools roll node configs sequentially with PDB-aware drain. Always wire etcd backup + mirror registry + must-gather before you need them.**

## 1. ClusterVersion + update channels + EUS

**ClusterVersion** CR holds the cluster's declared + observed version. Edit `spec.desiredUpdate` or `spec.channel` to trigger upgrades; CVO orchestrates the rollout across all ClusterOperators.
    **Update channels:**
    
      - **stable-X.Y** (e.g., `stable-4.18`) — production. Bug + security fixes within minor X.Y; minor upgrades via channel switch.

      - **fast-X.Y** — earlier access to newer GA minors. Slightly less baked than stable.

      - **candidate-X.Y** — release candidates. Pre-production validation only.

      - **eus-X.Y** — **EUS (Extended Update Support)** channels: ~24-month support windows for designated minor versions. EUS-to-EUS upgrade path (e.g., 4.16 EUS → 4.18 EUS skipping 4.17). For workloads that cannot upgrade quarterly.

    
    **OCP version support:** Red Hat supports at least 4 minors concurrently with phased lifecycles (Full Support → Maintenance Support → Extended Update Support — EUS). Plan upgrades against the support matrix; track EOS dates per minor.
    **OpenShift Update Service (OSUS)** serves the upgrade graph. Public clusters fetch from api.openshift.com; disconnected clusters need their own OSUS instance fed by mirrored upgrade-graph data.

## 2. MachineConfig + MachineConfigPools + MachineSets + MachineHealthChecks

**MachineConfig** = declarative RHCOS node config (kernel args, systemd units, files, ignition snippets). Multiple MachineConfig YAMLs are *merged* per-pool by the MCO into a final rendered config.
    **MachineConfigPool (MCP)** = group of nodes sharing a MachineConfig roll. Defaults: `master` + `worker` pools. Custom pools via labels for shape-specific configs (e.g., GPU nodes, FIPS nodes, infra nodes).
    When a MachineConfig changes, the MCO renders the new config + rolls the pool: cordon → drain (PDB-aware) → apply config → reboot → uncordon → next node. MCP status: `Updated` (steady) / `Updating` (in flight) / `Degraded` (failed).
    **MachineSets** = analogous to ReplicaSets but for the cluster's VMs/instances. Cluster Autoscaler scales MachineSets up/down based on Pending Pods. Per-MachineSet: provider config (instance type, AZ, IAM, disk), Machine template.
    **MachineHealthChecks (MHC)** = automatic remediation for unhealthy Machines. Define conditions (NotReady > 5min, etc.); MHC deletes + recreates the Machine via the MachineSet.
    **Node tuning + performance profiles:** **Node Tuning Operator** + **PerformanceProfile** CR = CPU pinning, hugepages, RT kernel, NUMA-aware tuning. For telco / latency-sensitive workloads.

## 3. etcd backup + must-gather + Insights telemetry + support cases

**etcd backup** = single point of cluster-state truth. Regular backup is mandatory:
    
      - Run `oc debug node/<master>` + invoke `cluster-backup.sh` on a master node — produces snapshot + static-pod manifests.

      - Schedule via CronJob hosted on infra nodes; ship snapshots off-cluster (S3 / NFS / NetApp).

      - Hourly + daily + weekly retention typical.

    
    **oc adm must-gather** = collects diagnostic bundle (logs, configs, ClusterOperator status, events) for a cluster issue. Plus targeted gathers per Operator (e.g., `oc adm must-gather --image=registry.redhat.io/openshift-logging/cluster-logging-rhel9-operator-must-gather`). Bundle = tarball you attach to support cases.
    **oc adm inspect** = focused gather on specific namespaces/resources. Lighter than must-gather.
    **Insights telemetry** = OCP's phone-home (opt-out): cluster identifies itself to Red Hat Insights, sends anonymised health + version + ClusterOperator status. Red Hat Insights surfaces recommendations + known-issue alerts in console.redhat.com. *For air-gapped clusters: opt-out + manage manually.*
    **Support cases:** Red Hat Customer Portal. Include must-gather + ClusterVersion + relevant Operator logs. SLA per support tier.

## 4. Disconnected updates + upgrade risk assessment

**Disconnected (air-gapped) updates:**
    
      - On internet-connected staging: `oc-mirror --config imageset-config.yaml` pulls new release + Operator updates.

      - Sneakernet (or one-way data diode) to air-gapped facility.

      - Internal mirror registry: `oc-mirror --from tarball.tar --to docker://mirror.example.com`.

      - Disconnected OSUS Operator updates the upgrade graph.

      - ClusterVersion shows new versions; admin upgrades via `oc adm upgrade`.

    
    **Upgrade risk assessment:**
    
      - **Conditional upgrades**: OCP's upgrade graph flags certain upgrade paths as conditionally risky based on cluster characteristics (e.g., specific Operator versions, custom MachineConfigs). CVO surfaces them in `oc adm upgrade`.

      - **Insights Advisor**: known-issue checks against your cluster.

      - **RHACM Cluster Lifecycle** (covered in O10): fleet-wide upgrade orchestration.

      - **kube-no-trouble + Pluto** for deprecated K8s API usage in workloads.

    
    **Upgrade order:** control plane (CVO) → ClusterOperators → worker MCPs (one MCP at a time, PDB-aware). Master MCP rolls in parallel with CVO; worker MCPs roll after CO's converge. EUS-to-EUS skips the intermediate minor.

## Before / After

**Before.** Pre-CVO + MCO, K8s upgrades meant per-component upgrade scripts + node OS reboots done by hand or with config management. No coherent ClusterVersion concept. EUS didn't exist; you upgraded every minor or fell off support. Disconnected updates were research projects.

**After.** OCP's lifecycle: **ClusterVersion + CVO** orchestrate ClusterOperator upgrades; **MCO + MachineConfigPools** roll RHCOS configs node-by-node with PDB-aware drain; **MachineSets + MachineHealthChecks** manage VM lifecycle + auto-remediation. **EUS** for ~24-month support windows. **etcd backup** + **must-gather** + **Insights** are first-class. **Disconnected** via mirror registry + oc-mirror.

*OCP upgrades are repeatable + auditable; pick channel by risk appetite + change-control cadence.*

## Analogy — the K-Foundry bay

The **Maintenance Bay** is where the foundry stays running. Three crews operate.
    The **Version Crew** (CVO + ClusterOperators) tracks the foundry's declared version + ensures all 30+ specialty operators are at that version. Channels: stable, fast, candidate, EUS. EUS is the long-term-lease shop where designated versions get 24-month support.
    The **Floor Crew** (MCO + MachineConfigPools + MachineSets + MachineHealthChecks) maintains the foundry floors (RHCOS): rolls floor-config changes pool-by-pool, drains nodes with PDB safety, replaces failed machines automatically.
    The **Records Crew** (etcd backup + must-gather + Insights + support cases) keeps backups, runs diagnostic gathers when something breaks, and phones home to Red Hat Insights for known-issue alerts.
    For disconnected foundries: oc-mirror brings updates in via sneakernet; disconnected OSUS feeds the local upgrade graph.

**Translation legend.**

| In the story… | …in OpenShift / Red Hat |
|---|---|
| Foundry version master record | ClusterVersion CR |
| Version Crew foreman | Cluster Version Operator (CVO) |
| Specialty operators on the floor | ClusterOperators (~30 of them) |
| Long-term lease shop | EUS — Extended Update Support (~24 mo) |
| Floor Crew foreman | Machine Config Operator (MCO) |
| Floor configuration recipe | MachineConfig CR |
| Floor crew zone | MachineConfigPool (MCP) — master / worker / custom |
| VM scale set | MachineSet |
| Auto-replace bad machine | MachineHealthCheck (MHC) |
| Workload-tuned node profile | PerformanceProfile + Node Tuning Operator |
| Foundry inventory backup | etcd backup (cluster-backup.sh) |
| Diagnostic kit | `oc adm must-gather` / `oc adm inspect` |
| Phone-home telemetry | Insights — anonymised health to Red Hat |
| Sneakernet update package | oc-mirror tarball |
| Local upgrade-graph feed | Disconnected OSUS Operator |
| Conditional upgrade warning | Upgrade risk assessment in `oc adm upgrade` |

⚠️ *Analogy stops here:* A real maintenance crew can pause; OCP upgrades in flight need careful PDB planning to avoid mid-roll deadlock the metaphor doesn't capture.

## ELI5 / ELI10

**ELI5.** Three maintenance crews keep the foundry running: one tracks software versions, one maintains the floors, one keeps records and backups. Long-term-lease customers get a special slow-cadence shop (EUS).

**ELI10.** OCP ops = CVO orchestrating ClusterOperators on a channel (stable / fast / candidate / EUS); MCO + MachineConfigPools rolling RHCOS configs node-by-node PDB-aware; MachineSets + MHC manage VM lifecycle; etcd backup mandatory; oc adm must-gather + Insights for diagnosis + recommendations; disconnected via mirror registry + oc-mirror + disconnected OSUS; EUS for ~24-mo support windows + EUS-to-EUS skip-minor upgrades.

## Real-world scenarios

- **Bank — EUS channel for the regulated payments cluster.** A regulated bank's payments cluster runs OCP on the EUS channel. They hold on a designated EUS minor for ~24 months; EUS-to-EUS upgrade every 2 years. Avoids the per-minor change-control overhead. Premium support tier; stable Operators.
- **Telco — performance profile + node tuning for 5G UPF.** Telco running 5G UPF needs CPU pinning + hugepages + RT kernel. PerformanceProfile CR + Node Tuning Operator. Custom MachineConfigPool for these nodes. Latency targets under 100µs.
- **Disconnected upgrade — sneakernet OCP minor update.** Air-gapped SCIF facility. Internet-connected staging runs `oc-mirror` for the new OCP minor + selected Operators; tarball ships via sneakernet. Internal mirror registry updated; disconnected OSUS feeds the upgrade graph; ClusterVersion shows new minor available; admin upgrades during maintenance window.
- **DR drill — etcd snapshot restored cluster in 50 minutes.** A bank tests etcd disaster recovery quarterly. Backup taken; cluster simulated catastrophic etcd loss; restore from backup using the documented disaster-recovery procedure on a sibling cluster. *50 minutes total restore time; auditor satisfied with RTO.*

## Common misconceptions

- **Myth:** "EUS means I never have to upgrade."
  **Truth:** EUS = ~24-month support window; you still upgrade — just every 2 years instead of every quarter. After EUS support ends for your version, you must move to the next EUS or current minor. Plan the EUS-to-EUS upgrade well in advance.
- **Myth:** "etcd is auto-backed-up by OCP."
  **Truth:** **etcd backup is your responsibility.** OCP doesn't auto-backup etcd by default. Schedule a CronJob or cron-on-master invoking `cluster-backup.sh`; ship snapshots off-cluster. Without etcd backup, a quorum-loss event = cluster rebuild from scratch.
- **Myth:** "must-gather is only for Red Hat support cases."
  **Truth:** must-gather is your *own* diagnostic tool too. Run it on incidents; bundles include ClusterOperator status, recent events, system logs, configs — useful for postmortem regardless of opening a Red Hat case. Plus targeted gathers per Operator give component-specific deep diagnostic data.

## Recap

Three crews: Version (CVO + channels + EUS), Floor (MCO + MCPs + MachineSets + MHCs), Records (etcd + must-gather + Insights). Disconnected via oc-mirror + OSUS.

**Next — O9: OpenShift Virtualization, AI, and Edge.** OpenShift Virtualization (KubeVirt) for VMs as first-class workloads; OpenShift AI (formerly RHODS) for notebooks + KServe + Kubeflow + RHEL AI; SNO + MicroShift + Local Zones for edge.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
