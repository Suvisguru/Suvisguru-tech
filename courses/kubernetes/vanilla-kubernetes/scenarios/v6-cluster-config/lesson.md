# K-VAN V6 — V6 · Cluster Configuration (apiserver, kubelet, scheduler, kube-proxy)

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V6 · Cluster Configuration
> Companion preview: `/preview-kubernetes-vanilla-lesson-06.html`.

---

**🎯 If you remember nothing else:** Tune four components: **kube-apiserver** (audit policy, EncryptionConfiguration, admission plugins, APF flow schemas), **kubelet** (cgroupDriver, systemReserved, kubeReserved, evictionHard, CPU/Memory/Topology Manager), **kube-scheduler** (profiles for bin-packing vs spreading; multiple schedulers like Volcano), **kube-proxy** (mode or replaced by Cilium). Plus **RuntimeClass** (Kata / gVisor) for sandboxing. All via kubeadm config, no flag soup.

## 1. Why post-install configuration exists

kubeadm gives you a working cluster with safe defaults. "Safe" is not the same as "production-tuned." Cloud distros pre-tune most of these knobs for you; vanilla self-managed clusters don't. The cost of leaving them as-is shows up as: surprise OOM evictions, audit gaps in compliance reports, secrets in plaintext in etcd backups, scheduler bin-packing that fights HPA decisions.
    Post-install configuration falls into four buckets:
    
      - **kube-apiserver**: how requests are observed, encrypted, prioritised, validated.

      - **kubelet**: how the node manages local resources + when it evicts.

      - **kube-scheduler / kube-proxy**: how Pods are placed + how Service traffic flows.

      - **RuntimeClass + image GC + log rotation**: the operational hygiene knobs.

## 2. Audit, encryption, admission, APF

Critical apiserver flags (set via kubeadm `ClusterConfiguration.apiServer.extraArgs`):
    
      - **Audit logging**: `audit-log-path`, `audit-policy-file`. Policy file decides what gets logged at what level (None / Metadata / Request / RequestResponse). Production: log all writes at RequestResponse to a forwarded log destination.

      - **EncryptionConfiguration**: `encryption-provider-config /etc/k8s/encryption.yaml`. Encrypts Secrets (and others) at rest in etcd. KMS v2 (K8s 1.31 GA) for production; static AES key for testing only.

      - **Admission plugins**: `enable-admission-plugins` = NodeRestriction, NamespaceLifecycle, ServiceAccount, PodSecurity, ValidatingAdmissionPolicy, MutatingAdmissionPolicy, ResourceQuota, LimitRanger, …

      - **APF (API Priority and Fairness)**: `FlowSchema` + `PriorityLevelConfiguration` CRDs. Prevents one noisy client from starving the API.

      - **Request limits**: `max-requests-inflight`, `max-mutating-requests-inflight`. APF supersedes these but they remain hard caps.

## 3. Reserved + eviction + topology

`# KubeletConfiguration (in kubeadm-config.yaml)
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
systemReserved:
  cpu: 500m
  memory: 1Gi
  ephemeral-storage: 1Gi
kubeReserved:
  cpu: 500m
  memory: 1Gi
  ephemeral-storage: 1Gi
evictionHard:
  memory.available: 200Mi
  nodefs.available: 10%
  imagefs.available: 5%
cpuManagerPolicy: static          # opt-in for guaranteed pods
memoryManagerPolicy: Static       # NUMA-pinned memory
topologyManagerPolicy: single-numa-node  # CPU + memory + device co-located
imageGCHighThresholdPercent: 80
imageGCLowThresholdPercent: 60
serverTLSBootstrap: true          # auto-rotate kubelet serving certs`
    **node allocatable** = node total − systemReserved − kubeReserved − evictionHard. This is what the scheduler sees as schedulable. Without setting these, the scheduler over-allocates.
    **kubelet serving cert rotation**: enable `serverTLSBootstrap: true` + approve CSRs (manually or via an auto-approver). Otherwise kubelets serve with a self-signed cert; metrics-server / kubectl logs / kubectl exec break.

## 4. The other knobs

**Scheduler profiles**: the kube-scheduler can run multiple named profiles in one process. Bin-packing for batch (`NodeResourcesFit: scoring=MostAllocated`); spreading for traffic-serving (default). Multiple schedulers (Volcano, Yunikorn) for ML / batch with gang scheduling.
    **kube-proxy mode**: `iptables` (default), `ipvs` (better at high Service count), `nftables` (1.31+ alpha → β; modern). Or replaced entirely by Cilium / Calico eBPF (V4).
    **RuntimeClass**: defines alternate runtimes (Kata Containers for VM-isolated Pods; gVisor for syscall-filter sandbox). Pod opts in via `spec.runtimeClassName: kata`. Useful for untrusted multi-tenant code.
    **image GC + log rotation**: kubelet manages container image pruning; configure thresholds. Container logs in `/var/log/containers/` rotated by kubelet (`containerLogMaxSize`, `containerLogMaxFiles`) — set to avoid disk full.
    [ deep dive — skip if new ]Feature gates: `--feature-gates=GracefulNodeShutdown=true` etc. Beta and GA features default on; alpha features default off. Track upcoming features and pre-enable in dev, never alpha in prod.

## Before / After

**Before.** kubeadm defaults everywhere. No audit log → compliance gap. No encryption-at-rest → secrets readable from etcd backup. No reserved resources → surprise OOM evictions. No log rotation → disk full. "Why is X happening?" answered with shrugs.

**After.** kubeadm config YAML in git captures every tuned flag. Audit + encryption on. Reserved resources set per node-class. Scheduler profiles match workload mix. RuntimeClass available for sensitive workloads. New cluster = same config; same posture.

Cluster configuration is post-install but pre-workload. Get it right before the first app team onboards.

## Analogy — the K-Frontier site

The Rules Board is a posted notice on the homestead's central beam. Everyone passing through reads it: how loud you can be after dark (audit), where to lock the safe (encryption), how much firewood is reserved for the household (system/kubeReserved), what to do during a fire (eviction). The rules aren't fancy — they're the agreements that keep the homestead from collapsing under weather.

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| Posted house rules | Cluster-wide configuration files |
| "Quiet hours: log everything after 10 PM" | audit-policy.yaml |
| "Safe locked, only the cook + sheriff have keys" | EncryptionConfiguration + KMS v2 |
| "This stack is reserved for the house" | systemReserved + kubeReserved |
| "Fire drill: residents evacuate first, livestock second" | evictionHard thresholds + Pod priorities |
| "Stovekeeper schedules duties differently for night shift" | Multiple scheduler profiles |
| "Visitors from the city use a different gate" | RuntimeClass for sandboxed Pods (Kata / gVisor) |
| "Trash burned weekly, ash hauled monthly" | image GC + log rotation |

⚠️ *Analogy stops here:* The analogy stops here: real configuration changes propagate via kubelet restart (rolling) or apiserver restart (brief outage). "Posting a rule" doesn't restart anything; real rule changes come with operational impact.

## ELI5 / ELI10

**ELI5.** Every house has rules: when to be quiet, where to lock things, how much food is reserved for the family. The cluster has the same kind of rules, written down in config files.

**ELI10.** kubeadm sets safe defaults; production tunes via ClusterConfiguration: apiserver (audit + EncryptionConfiguration + admission + APF), kubelet (systemReserved + kubeReserved + evictionHard + cgroupDriver + CPU/Memory/Topology Manager + serving cert rotation), scheduler (profiles for bin-pack vs spread, multiple schedulers), kube-proxy (mode or replaced). RuntimeClass for sandboxing. All in one YAML committed to git.

## Real-world scenarios

- **A SaaS with reserved resources tuned per node class.** Worker class A (general): systemReserved 500m/1Gi, kubeReserved 500m/1Gi. Worker class B (memory-intensive): kubeReserved 2Gi (Pods are memory-heavy; scheduler factors in). Documented in the kubeadm-config.yaml per node pool. Allocatable predictable; eviction rare.
- **A bank with audit + encryption baseline.** Audit policy logs every Secret read at RequestResponse + every write to RBAC, NetworkPolicy, ResourceQuota. Forwarded to SIEM. EncryptionConfiguration uses KMS v2 + Vault Transit; Secrets encrypted at rest. Auditor confirms compliance via `kubectl get secrets -o yaml | grep -i encrypt` on a sample.
- **A team using two scheduler profiles.** Default scheduler (spreading) for traffic-serving Deployments. Bin-packing scheduler for batch / ML training. Pods opt in via `spec.schedulerName: bin-pack`. Same kube-scheduler binary, two profiles in its config. Spot instances pack tightly; prod spreads across zones.
- **A team running Kata for tenant isolation.** Multi-tenant cluster running customer code. RuntimeClass `kata` defined; specific namespaces have a Kyverno policy mutating Pods to use it. Each Pod runs in a lightweight VM. Defense-in-depth against kernel exploits.

## Common misconceptions

- **Myth:** "systemReserved is optional."
  **Truth:** Without it, allocatable = node total. The scheduler over-allocates and the kubelet evicts under pressure. Always set, based on measured baseline OS + DaemonSet usage.
- **Myth:** "Audit logs are noise."
  **Truth:** Untuned audit policy is noise. A good policy logs writes at full detail and reads at metadata-only; total volume is manageable. Compliance, breach forensics, and quiet-time anomaly detection all need audit.
- **Myth:** "Encryption-at-rest with a static AES key is good enough."
  **Truth:** Better than nothing, but the key sits next to the data on the API server's disk. KMS v2 with an external KMS (Vault, cloud KMS) is the production answer.

## Recap

Tune apiserver (audit + encryption + APF), kubelet (reserved + eviction + topology + serving certs), scheduler (profiles), kube-proxy (mode), RuntimeClass. All via kubeadm config in git. Production-tuned ≠ defaults.

**Next — V7: etcd Production-Grade.** The well below the homestead. Raft, quorum, snapshots, defrag, disaster recovery.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
