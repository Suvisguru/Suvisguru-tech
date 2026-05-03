# K-VAN V7 — V7 · etcd Production-Grade (Raft, Snapshots, Defrag, DR)

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V7 · etcd Production
> Companion preview: `/preview-kubernetes-vanilla-lesson-07.html`.

---

**🎯 If you remember nothing else:** etcd uses **Raft consensus** across 3+ members for HA (need majority for quorum). Disk: **dedicated NVMe SSD**, < 10ms p99 fsync, separate from kubelet. Routine ops: **snapshots** (every 30 min, off-site), **defragmentation** (weekly, rolling), **compaction** (auto via kube-apiserver). DR: **practice restore quarterly** — backups you don't test are fiction. Failed member: detach + add as learner + promote.

## 1. Why etcd is special

etcd holds every K8s object — every Pod spec, every Secret, every Deployment, every CRD instance. It's a strongly-consistent distributed key-value store using the **Raft** consensus protocol. The cluster reads + writes through the kube-apiserver, which writes to etcd. *If etcd is slow, the apiserver is slow, the cluster is slow.* If etcd loses data, the cluster loses state.
    What this means in practice: etcd needs better hardware than most components, careful operational hygiene, and disaster-recovery rehearsal. It's the only K8s component where 99% confidence isn't enough — you want 100%.

## 2. The math behind HA

- **Members:** the etcd processes (typically 3 or 5 — odd numbers for symmetric quorum).

      - **Quorum:** majority. 3 members → quorum is 2. 5 → quorum is 3. Lose more than (N-1)/2 and the cluster loses quorum + becomes read-only.

      - **Leader:** one member at a time accepts writes; followers replicate. Re-elected on heartbeat timeout (default 1s).

      - **Learner members:** non-voting members that catch up before being promoted. Use when adding a 4th member to an existing 3-member cluster (avoids temporary even-count + split-brain risk).

    
    Member sizes that make sense:
    
      - 3 members: HA, 1-fault-tolerant. Default + production minimum.

      - 5 members: 2-fault-tolerant. Use for larger clusters or when faults must overlap with maintenance windows.

      - 7+: rare; write throughput drops as more members must ack. Most clusters cap at 5.

## 3. The chores

**Snapshots** (manual or scheduled):
    `# From any etcd member host
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /backup/etcd-$(date +%F-%H%M).db`
    Schedule via systemd timer (every 30 min for production), then ship off-cluster (S3, NFS, separate datacenter).
    **Compaction** (auto): kube-apiserver runs `--etcd-compaction-interval` (default 5 min). Compaction discards old key revisions; freed space is in-database but not returned to disk.
    **Defragmentation** (manual, rolling): defrag returns the freed space to disk. Run on one member at a time; the member is unavailable during defrag (~5-30s typically).
    `ETCDCTL_API=3 etcdctl --endpoints=https://etcd-3:2379 defrag`
    **Alarms:** etcd raises `NOSPACE` when DB exceeds `quota-backend-bytes` (default 2 GiB; bump to 8 GiB for production). When NOSPACE is active, etcd accepts no writes. Check + clear: `etcdctl alarm list` + `etcdctl alarm disarm`.

## 4. When a member fails

**Single member failure** (cluster keeps working with 2 of 3 in quorum):
    `# 1. Remove the failed member from the cluster
etcdctl member list
etcdctl member remove <member-id>

# 2. On the new node: prep the etcd dir (empty), get certs.
# 3. Add as learner first (won't vote until caught up)
etcdctl member add etcd-new --peer-urls=https://10.0.0.4:2380 --learner

# 4. Start etcd on the new node with --initial-cluster-state=existing
# 5. Promote learner to voting member once caught up
etcdctl member promote <learner-id>`
    **Quorum loss** (e.g., 2 of 3 dead at once): the cluster is read-only. **Recovery via snapshot restore:**
    `# On each surviving + replacement node, restore from a recent snapshot
ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd.db \
  --name etcd-1 \
  --initial-cluster etcd-1=https://10.0.0.1:2380,etcd-2=https://10.0.0.2:2380,etcd-3=https://10.0.0.3:2380 \
  --initial-cluster-token new-cluster \
  --initial-advertise-peer-urls https://10.0.0.1:2380 \
  --data-dir /var/lib/etcd-restore

# Replace the etcd data dir; restart etcd on each node simultaneously`
    **Backup-restore drill cadence:** quarterly minimum. Run a real restore on a non-prod cluster + verify the cluster comes up + sample objects look right. Untested backups are not backups.
    [ deep dive — skip if new ]External etcd: separate the etcd nodes from the apiserver tier. Bigger ops surface but lets you scale + tune them independently. Use when cluster is > 500 nodes or you have heavy watch load.

## Before / After

**Before.** etcd shares a disk with kubelet image cache. Slow fsync. Backup script untested. "It'll be fine" until the day a member dies, defrag wasn't routine, NOSPACE fires, and the team learns about Raft quorum from a Stack Overflow tab open during the outage.

**After.** etcd on dedicated NVMe. Snapshot every 30 min to S3. Defrag weekly via cron. Quarterly restore drill on staging. Dashboards showing disk-fsync latency + member health. Member replacement runbook tested. Sleep through routine etcd ops.

etcd is the part of K8s where you're punished hardest for shortcuts. Hardware + hygiene + drills.

## Analogy — the K-Frontier site

The Well is the deepest, oldest part of the homestead — the one that everything else depends on. The Well must be kept clean (defrag), the bucket has to come up cleanly (fsync < 10ms), the water level has to be checked daily (alarms), and there has to be a backup well drilled in case this one fouls (snapshots + restore drills). If the Well runs dry or gets polluted, the whole homestead reverts to surviving on whatever's in the cistern (read-only mode, then nothing). Three caretakers tend the well together (3 etcd members + Raft); one is the well-keeper that day (leader); the others mirror everything she does.

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| The well-keeper today | etcd Raft leader |
| Other caretakers mirroring her | Followers (Raft log replication) |
| "Need at least 2 of 3 to draw water" | Quorum (majority of members) |
| Daily water-level check | etcd alarms (NOSPACE / CORRUPT) |
| Cleaning the well | Defragmentation |
| Filling the cistern as backup | Snapshots → off-site |
| Drilling a parallel well | Snapshot restore to a new 3-member cluster |
| Replacing a sick caretaker | Member remove + add learner + promote |
| Always-fresh water test | Quarterly restore drill on staging |

⚠️ *Analogy stops here:* The analogy stops here: real etcd has cryptographic authentication between members, TLS for client/peer traffic, and gRPC streaming for watches. The well metaphor undersells the network + crypto plumbing.

## ELI5 / ELI10

**ELI5.** Imagine the homestead has one well that everyone drinks from. Three people share the work of pumping it. They all have to agree on what's in the bucket. If two of three are away, no water. Practice the backup well drill — don't learn it during a drought.

**ELI10.** etcd: distributed key/value store using Raft. K8s object source of truth. 3 (or 5) members for HA; quorum = majority. Stacked (on CP nodes) or external. Disk: dedicated NVMe, < 10ms p99 fsync. Routine: snapshot every 30 min off-site, weekly defrag, monitor alarms. Failure: single member → remove + add as learner + promote. Quorum loss → snapshot restore a fresh cluster. Drill the restore quarterly.

## Real-world scenarios

- **A SaaS with stacked etcd + 30-min snapshots.** 3 stacked etcd on CP nodes, dedicated NVMe partition for /var/lib/etcd. systemd timer: `etcdctl snapshot save` every 30 min, `aws s3 cp` to a backup bucket. Lifecycle policy: 30-day retention. Quarterly restore drill on a staging cluster. ~10 min RTO from a full cluster loss.
- **A bank with external 5-member etcd.** Dedicated etcd VMs (5 members in 3 racks for 2-fault tolerance). Tuned: `quota-backend-bytes=8589934592`, `auto-compaction-mode=periodic`, `auto-compaction-retention=1h`. Snapshots every 5 min, restore drilled monthly. NetworkPolicy isolates etcd to apiserver-only.
- **A team that learned from defrag inattention.** etcd DB grew to 6 GiB over a year. Hit `quota-backend-bytes=2147483648` default; NOSPACE alarm; cluster read-only. Recovery: bumped quota to 8 GiB, ran defrag on each member. New runbook: weekly defrag via cron, dashboard alert on DB size > 60% of quota.
- **A team rehearsing snapshot-restore.** Quarterly: clone production, simulate "all 3 etcd nodes lost". Restore from latest S3 snapshot. New 3-member cluster comes up; apply the kubeadm certs; start kube-apiserver. Verify a sampled set of Pods is recreated by their controllers. Total time end-to-end: ~25 min. Documented in the DR runbook.

## Common misconceptions

- **Myth:** "3 members means 3-fault tolerance."
  **Truth:** 3 members tolerates 1 failure (quorum is 2). For 2 faults need 5 members. The math is (N-1)/2 faults tolerated.
- **Myth:** "Compaction frees disk space."
  **Truth:** Compaction frees in-database space but doesn't shrink the file. Defragmentation does — and it requires brief member unavailability per defrag. Roll member-by-member.
- **Myth:** "Snapshots are reliable backups."
  **Truth:** Untested snapshots are theoretical backups. Routinely restore them on a non-prod cluster + verify the resulting cluster works. Quarterly minimum.

## Recap

etcd uses Raft + quorum. 3 (or 5) members. Dedicated NVMe with < 10ms p99 fsync. Snapshot every 30 min, defrag weekly, quarterly DR drill. Failed member: remove + add learner + promote. Quorum loss: snapshot restore.

**Next — V8: Upgrades and Patching.** Cluster doesn't stay still. Version skew rules, kubeadm upgrade, control-plane → kubelet → workers → CNI/CSI order, surge nodes, rollback.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
