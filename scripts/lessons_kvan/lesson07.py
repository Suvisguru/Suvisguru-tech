from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The Well: 3 ringed wellheads (etcd members), Raft arrows showing leader and followers, snapshot bucket on the side, defrag tool, alarm bell.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">THE WELL · etcd PRODUCTION</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">etcd CLUSTER · 3 MEMBERS · STACKED</text>
    <circle cx="120" cy="88" r="34" fill="#A04832" stroke="#5A4F45" stroke-width="2"/><text x="120" y="86" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">etcd-1</text><text x="120" y="98" text-anchor="middle" font-size="7" fill="#FBE8DC">leader</text>
    <circle cx="240" cy="88" r="30" fill="#5A9F7A" stroke="#3D7857" stroke-width="2"/><text x="240" y="86" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">etcd-2</text><text x="240" y="98" text-anchor="middle" font-size="7" fill="#FBE8DC">follower</text>
    <circle cx="360" cy="88" r="30" fill="#5A9F7A" stroke="#3D7857" stroke-width="2"/><text x="360" y="86" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">etcd-3</text><text x="360" y="98" text-anchor="middle" font-size="7" fill="#FBE8DC">follower</text>
    <line x1="154" y1="88" x2="210" y2="88" stroke="#3F4A5E" stroke-width="2" stroke-dasharray="3,2"/>
    <line x1="270" y1="88" x2="330" y2="88" stroke="#3F4A5E" stroke-width="2" stroke-dasharray="3,2"/>
    <text x="240" y="74" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">Raft heartbeat + log replication</text>
    <rect x="430" y="40" width="160" height="40" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="510" y="56" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">snapshot bucket</text><text x="510" y="68" text-anchor="middle" font-size="7" fill="#5A4F45">etcdctl snapshot save</text>
    <rect x="430" y="86" width="160" height="40" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="510" y="102" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">alarm: NOSPACE / CORRUPT</text><text x="510" y="114" text-anchor="middle" font-size="7" fill="#5A4F45">defrag + alarm disarm</text>
    <rect x="14" y="134" width="572" height="22" rx="3" fill="#3F4A5E"/><text x="300" y="148" text-anchor="middle" font-size="8" fill="#FBF1D6">disk: NVMe · &lt; 10ms p99 fsync · dedicated mount · network: low-latency between members</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="07",
    title_short="etcd production",
    title_full="V7 · etcd Production-Grade (Raft, Snapshots, Defrag, DR)",
    title_html="K-VAN V7 · etcd Production",
    module_eyebrow="Module V7 · the well below the homestead",
    hero_sub_html='<strong>etcd is the cluster\'s source of truth.</strong> Slow etcd = slow cluster. Lost etcd = lost cluster. Master Raft, snapshots, defragmentation, member replacement, and disaster recovery — or pick a managed K8s instead.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Cluster goes mysteriously slow. <code>kubectl get pod</code> takes 8 seconds. Investigation: etcd writes are at 800ms p99 because the etcd disk is shared with kubelet container images and the page cache is thrashing. Or: cluster locked up entirely because etcd alarm <code>NOSPACE</code> fired and reads stopped. Or: backup script ran for 6 months but nobody ever tested restore — the snapshots are corrupt. <em>etcd is the part of the cluster that punishes inattention</em>.',
    stamp_html='etcd uses <strong>Raft consensus</strong> across 3+ members for HA (need majority for quorum). Disk: <strong>dedicated NVMe SSD</strong>, &lt; 10ms p99 fsync, separate from kubelet. Routine ops: <strong>snapshots</strong> (every 30 min, off-site), <strong>defragmentation</strong> (weekly, rolling), <strong>compaction</strong> (auto via kube-apiserver). DR: <strong>practice restore quarterly</strong> — backups you don\'t test are fiction. Failed member: detach + add as learner + promote.',
    district_pin="kf-site07",
    district_label="The Well",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why etcd is special",
            body_html="""    <p>etcd holds every K8s object — every Pod spec, every Secret, every Deployment, every CRD instance. It\'s a strongly-consistent distributed key-value store using the <strong>Raft</strong> consensus protocol. The cluster reads + writes through the kube-apiserver, which writes to etcd. <em>If etcd is slow, the apiserver is slow, the cluster is slow.</em> If etcd loses data, the cluster loses state.</p>
    <p>What this means in practice: etcd needs better hardware than most components, careful operational hygiene, and disaster-recovery rehearsal. It\'s the only K8s component where 99% confidence isn\'t enough — you want 100%.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Raft + quorum + members",
            h2="The math behind HA",
            body_html="""    <ul>
      <li><strong>Members:</strong> the etcd processes (typically 3 or 5 — odd numbers for symmetric quorum).</li>
      <li><strong>Quorum:</strong> majority. 3 members → quorum is 2. 5 → quorum is 3. Lose more than (N-1)/2 and the cluster loses quorum + becomes read-only.</li>
      <li><strong>Leader:</strong> one member at a time accepts writes; followers replicate. Re-elected on heartbeat timeout (default 1s).</li>
      <li><strong>Learner members:</strong> non-voting members that catch up before being promoted. Use when adding a 4th member to an existing 3-member cluster (avoids temporary even-count + split-brain risk).</li>
    </ul>
    <p>Member sizes that make sense:</p>
    <ul>
      <li>3 members: HA, 1-fault-tolerant. Default + production minimum.</li>
      <li>5 members: 2-fault-tolerant. Use for larger clusters or when faults must overlap with maintenance windows.</li>
      <li>7+: rare; write throughput drops as more members must ack. Most clusters cap at 5.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.7 · Operational hygiene — snapshots, defrag, compaction",
            h2="The chores",
            body_html="""    <p><strong>Snapshots</strong> (manual or scheduled):</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># From any etcd member host
ETCDCTL_API=3 etcdctl \\
  --endpoints=https://127.0.0.1:2379 \\
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \\
  --cert=/etc/kubernetes/pki/etcd/server.crt \\
  --key=/etc/kubernetes/pki/etcd/server.key \\
  snapshot save /backup/etcd-$(date +%F-%H%M).db</code></pre>
    <p>Schedule via systemd timer (every 30 min for production), then ship off-cluster (S3, NFS, separate datacenter).</p>
    <p><strong>Compaction</strong> (auto): kube-apiserver runs <code>--etcd-compaction-interval</code> (default 5 min). Compaction discards old key revisions; freed space is in-database but not returned to disk.</p>
    <p><strong>Defragmentation</strong> (manual, rolling): defrag returns the freed space to disk. Run on one member at a time; the member is unavailable during defrag (~5-30s typically).</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>ETCDCTL_API=3 etcdctl --endpoints=https://etcd-3:2379 defrag</code></pre>
    <p><strong>Alarms:</strong> etcd raises <code>NOSPACE</code> when DB exceeds <code>quota-backend-bytes</code> (default 2 GiB; bump to 8 GiB for production). When NOSPACE is active, etcd accepts no writes. Check + clear: <code>etcdctl alarm list</code> + <code>etcdctl alarm disarm</code>.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Member replacement + DR",
            h2="When a member fails",
            body_html="""    <p><strong>Single member failure</strong> (cluster keeps working with 2 of 3 in quorum):</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># 1. Remove the failed member from the cluster
etcdctl member list
etcdctl member remove &lt;member-id&gt;

# 2. On the new node: prep the etcd dir (empty), get certs.
# 3. Add as learner first (won't vote until caught up)
etcdctl member add etcd-new --peer-urls=https://10.0.0.4:2380 --learner

# 4. Start etcd on the new node with --initial-cluster-state=existing
# 5. Promote learner to voting member once caught up
etcdctl member promote &lt;learner-id&gt;</code></pre>
    <p><strong>Quorum loss</strong> (e.g., 2 of 3 dead at once): the cluster is read-only. <strong>Recovery via snapshot restore:</strong></p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># On each surviving + replacement node, restore from a recent snapshot
ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd.db \\
  --name etcd-1 \\
  --initial-cluster etcd-1=https://10.0.0.1:2380,etcd-2=https://10.0.0.2:2380,etcd-3=https://10.0.0.3:2380 \\
  --initial-cluster-token new-cluster \\
  --initial-advertise-peer-urls https://10.0.0.1:2380 \\
  --data-dir /var/lib/etcd-restore

# Replace the etcd data dir; restart etcd on each node simultaneously</code></pre>
    <p><strong>Backup-restore drill cadence:</strong> quarterly minimum. Run a real restore on a non-prod cluster + verify the cluster comes up + sample objects look right. Untested backups are not backups.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>External etcd: separate the etcd nodes from the apiserver tier. Bigger ops surface but lets you scale + tune them independently. Use when cluster is &gt; 500 nodes or you have heavy watch load.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='You have 3 etcd members. Two go down at the same time (rack PSU failure). What state is the cluster in?',
            options=[
                ('a) Fully working — etcd handles 2-of-3 outage', False),
                ('b) Read-only — quorum lost (need 2 of 3, only 1 is up); apiserver will return errors on writes', True),
                ('c) Dead — no quorum, no reads', False),
            ],
            feedback='<strong>Answer: b.</strong> Quorum requires majority. 3 members → need 2 alive. With 1 alive, no leader can be elected; writes fail; reads from the single alive member are still served (depending on consistency level). Recovery: snapshot-restore to bring up a fresh 3-member cluster; or 5-member cluster from day 1 if 2-fault tolerance matters.',
        ),
    },
    before_after_before='<p>etcd shares a disk with kubelet image cache. Slow fsync. Backup script untested. \"It\'ll be fine\" until the day a member dies, defrag wasn\'t routine, NOSPACE fires, and the team learns about Raft quorum from a Stack Overflow tab open during the outage.</p>',
    before_after_after='<p>etcd on dedicated NVMe. Snapshot every 30 min to S3. Defrag weekly via cron. Quarterly restore drill on staging. Dashboards showing disk-fsync latency + member health. Member replacement runbook tested. Sleep through routine etcd ops.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">etcd is the part of K8s where you\'re punished hardest for shortcuts. Hardware + hygiene + drills.</p>',
    analogy_intro_html='<p>The Well is the deepest, oldest part of the homestead — the one that everything else depends on. The Well must be kept clean (defrag), the bucket has to come up cleanly (fsync &lt; 10ms), the water level has to be checked daily (alarms), and there has to be a backup well drilled in case this one fouls (snapshots + restore drills). If the Well runs dry or gets polluted, the whole homestead reverts to surviving on whatever\'s in the cistern (read-only mode, then nothing). Three caretakers tend the well together (3 etcd members + Raft); one is the well-keeper that day (leader); the others mirror everything she does.</p>',
    translation_rows=[
        ('The well-keeper today', 'etcd Raft leader'),
        ('Other caretakers mirroring her', 'Followers (Raft log replication)'),
        ('"Need at least 2 of 3 to draw water"', 'Quorum (majority of members)'),
        ('Daily water-level check', 'etcd alarms (NOSPACE / CORRUPT)'),
        ('Cleaning the well', 'Defragmentation'),
        ('Filling the cistern as backup', 'Snapshots → off-site'),
        ('Drilling a parallel well', 'Snapshot restore to a new 3-member cluster'),
        ('Replacing a sick caretaker', 'Member remove + add learner + promote'),
        ('Always-fresh water test', 'Quarterly restore drill on staging'),
    ],
    analogy_stops="The analogy stops here: real etcd has cryptographic authentication between members, TLS for client/peer traffic, and gRPC streaming for watches. The well metaphor undersells the network + crypto plumbing.",
    eli5='Imagine the homestead has one well that everyone drinks from. Three people share the work of pumping it. They all have to agree on what\'s in the bucket. If two of three are away, no water. Practice the backup well drill — don\'t learn it during a drought.',
    eli10="etcd: distributed key/value store using Raft. K8s object source of truth. 3 (or 5) members for HA; quorum = majority. Stacked (on CP nodes) or external. Disk: dedicated NVMe, &lt; 10ms p99 fsync. Routine: snapshot every 30 min off-site, weekly defrag, monitor alarms. Failure: single member → remove + add as learner + promote. Quorum loss → snapshot restore a fresh cluster. Drill the restore quarterly.",
    scenarios=[
        Scenario(name='A SaaS with stacked etcd + 30-min snapshots', body='3 stacked etcd on CP nodes, dedicated NVMe partition for /var/lib/etcd. systemd timer: <code>etcdctl snapshot save</code> every 30 min, <code>aws s3 cp</code> to a backup bucket. Lifecycle policy: 30-day retention. Quarterly restore drill on a staging cluster. ~10 min RTO from a full cluster loss.'),
        Scenario(name='A bank with external 5-member etcd', body='Dedicated etcd VMs (5 members in 3 racks for 2-fault tolerance). Tuned: <code>quota-backend-bytes=8589934592</code>, <code>auto-compaction-mode=periodic</code>, <code>auto-compaction-retention=1h</code>. Snapshots every 5 min, restore drilled monthly. NetworkPolicy isolates etcd to apiserver-only.'),
        Scenario(name='A team that learned from defrag inattention', body='etcd DB grew to 6 GiB over a year. Hit <code>quota-backend-bytes=2147483648</code> default; NOSPACE alarm; cluster read-only. Recovery: bumped quota to 8 GiB, ran defrag on each member. New runbook: weekly defrag via cron, dashboard alert on DB size > 60% of quota.'),
        Scenario(name='A team rehearsing snapshot-restore', body='Quarterly: clone production, simulate \"all 3 etcd nodes lost\". Restore from latest S3 snapshot. New 3-member cluster comes up; apply the kubeadm certs; start kube-apiserver. Verify a sampled set of Pods is recreated by their controllers. Total time end-to-end: ~25 min. Documented in the DR runbook.'),
    ],
    misconceptions=[
        Misconception(myth='\"3 members means 3-fault tolerance.\"', truth='3 members tolerates 1 failure (quorum is 2). For 2 faults need 5 members. The math is (N-1)/2 faults tolerated.'),
        Misconception(myth='\"Compaction frees disk space.\"', truth='Compaction frees in-database space but doesn\'t shrink the file. Defragmentation does — and it requires brief member unavailability per defrag. Roll member-by-member.'),
        Misconception(myth='\"Snapshots are reliable backups.\"', truth='Untested snapshots are theoretical backups. Routinely restore them on a non-prod cluster + verify the resulting cluster works. Quarterly minimum.'),
    ],
    flashcards=[
        Flashcard(front='What is Raft?', back='Distributed consensus protocol. Leader elected by heartbeat; followers replicate the log. Used by etcd, Consul, others.'),
        Flashcard(front='Quorum formula?', back='Majority of members. 3 → 2. 5 → 3. 7 → 4. Below quorum = read-only / unavailable.'),
        Flashcard(front='Why odd-number members?', back='Even numbers add cost without adding fault tolerance. 3 → tolerate 1 fail (need 2); 4 → still tolerate 1 (need 3, more fragile); 5 → tolerate 2.'),
        Flashcard(front='What is a learner member?', back='Non-voting member catching up to the cluster. Used when adding a member: avoids temporary disruption + split-brain risk during catch-up.'),
        Flashcard(front='etcd disk requirements?', back='Dedicated SSD (preferably NVMe) with &lt; 10ms p99 fsync. <em>Don\'t</em> share with container image cache or kubelet logs.'),
        Flashcard(front='Snapshot vs compaction vs defrag?', back='Snapshot = full point-in-time copy (for backup). Compaction = discard old key revisions (frees in-DB space). Defrag = return freed space to disk (member briefly unavailable).'),
        Flashcard(front='etcd alarms — NOSPACE?', back='DB hit <code>quota-backend-bytes</code>. Cluster read-only. Fix: bump quota, defrag, then <code>etcdctl alarm disarm</code>.'),
        Flashcard(front='Snapshot restore disaster recovery flow?', back='On every member node: <code>etcdctl snapshot restore</code> to a new data dir + same <code>--initial-cluster</code> flags. Replace the data dir + restart etcd. Apiserver will recover; controllers re-create derived state.'),
    ],
    quizzes=[
        Quiz(prompt='Your monitoring shows etcd p99 fsync latency climbing to 80ms. The cluster feels slow. First diagnostic step?', answer='Check the disk. <strong>(1)</strong> <code>iostat -x 1</code> on the etcd hosts during the latency spike. await + util%. (2) Is the etcd data dir on dedicated NVMe? Or shared with container image storage / logs / kubelet state? (3) Is there a noisy neighbour? (kubelet log rotation, container image GC, page-cache contention). <strong>Fix paths:</strong> move etcd to dedicated NVMe (rebuild member); set io scheduler to <code>none</code>; isolate via <code>systemd</code> resource limits. <strong>Long-term:</strong> alert on fsync p99 &gt; 25ms — long before users notice. Etcd is forgiving until it isn\'t.'),
        Quiz(prompt='Two of three etcd members went down at the same time (a hypervisor crash took out two CP VMs). The cluster is unresponsive. Walk the recovery.', answer='<strong>Quorum lost.</strong> Recovery requires snapshot-restore to a fresh cluster — you can\'t simply restart the dead members because they\'re missing committed log entries. <strong>Step 1:</strong> stop etcd on the surviving member to prevent it from being a stale source. <strong>Step 2:</strong> on each of three replacement nodes, restore from the latest snapshot to a new <code>--data-dir</code> + the same <code>--initial-cluster</code> set, using a fresh <code>--initial-cluster-token</code>. <strong>Step 3:</strong> start all three etcd processes simultaneously. <strong>Step 4:</strong> the K8s apiservers (which restart the static-pod automatically) reconnect; deployments + StatefulSets reconcile their derived state. <strong>Step 5:</strong> verify with <code>etcdctl endpoint status</code> + <code>etcdctl endpoint health</code>. Pods that were running keep running; new Pod scheduling resumes once the apiserver is healthy. <strong>Lesson:</strong> if recoveries like this terrify you, run a 5-member etcd (tolerates 2 simultaneous faults).'),
        Quiz(prompt='Your team has \"snapshots\" but has never restored them. <strong>Click for the etcd DR drill playbook. ▼</strong>', cyoa=True, cyoa_tag='the DR drill', answer='<strong>(1) Pick a non-prod cluster.</strong> Treat it as expendable. <strong>(2) Schedule a 1-hour drill window.</strong> Notify the team. <strong>(3) Take a fresh snapshot</strong> from production etcd: <code>etcdctl snapshot save</code> + <code>aws s3 cp</code>. Note the file path. <strong>(4) Stop kubelet + etcd on the non-prod cluster.</strong> Move the existing <code>/var/lib/etcd</code> aside. <strong>(5) Restore on each member node:</strong> <code>etcdctl snapshot restore $SNAP --data-dir /var/lib/etcd --initial-cluster ... --initial-cluster-token drill --initial-advertise-peer-urls ...</code>. <strong>(6) Start etcd on all three simultaneously.</strong> Watch logs for leader election + log replication. <strong>(7) Restart kube-apiserver static-pods</strong> (touch the manifest file). <strong>(8) Verify:</strong> <code>kubectl get nodes</code>, <code>kubectl get pods -A</code>. Sample 5 random Deployments — do their replicas match the production snapshot point-in-time? <strong>(9) Document timing</strong>: snapshot age (RPO), restore-to-cluster-ready elapsed (RTO). <strong>(10) File issues</strong> for any rough edges; iterate on the runbook. <strong>Cadence:</strong> quarterly, ideally rotating who runs the drill — knowledge spread is part of the goal.'),
    ],
    glossary=[
        GlossaryItem(name='etcd', definition='Distributed key-value store. K8s object source of truth. Uses Raft consensus.'),
        GlossaryItem(name='Raft', definition='Consensus protocol. Leader-based; replicated log. Tolerates (N-1)/2 faults with N members.'),
        GlossaryItem(name='Quorum', definition='Majority of members reachable. 3 → 2. 5 → 3. Below quorum = read-only / unavailable.'),
        GlossaryItem(name='Leader / follower', definition='Raft roles. Leader accepts writes; followers replicate. Re-elected on heartbeat timeout.'),
        GlossaryItem(name='Learner member', definition='Non-voting etcd member catching up. Used when adding a member without disrupting quorum.'),
        GlossaryItem(name='Snapshot', definition='Full point-in-time copy of etcd state. <code>etcdctl snapshot save</code>. Backup / restore primitive.'),
        GlossaryItem(name='Compaction', definition='Discards old key revisions. Frees in-DB space. Run automatically by kube-apiserver (<code>--etcd-compaction-interval</code>).'),
        GlossaryItem(name='Defragmentation', definition='Returns freed space to disk. Member briefly unavailable during defrag. Run rolling.'),
        GlossaryItem(name='Alarms (etcd)', definition='NOSPACE (DB exceeded quota), CORRUPT (data inconsistency). Check + clear with <code>etcdctl alarm</code>.'),
        GlossaryItem(name='quota-backend-bytes', definition='etcd flag: max DB size before NOSPACE. Default 2 GiB; bump to 8 GiB for production.'),
        GlossaryItem(name='Stacked etcd', definition='etcd runs on the same nodes as kube-apiserver. Default kubeadm topology.'),
        GlossaryItem(name='External etcd', definition='etcd on dedicated nodes. Used for &gt; 500-node clusters or heavy watch load.'),
    ],
    recap_lead='etcd uses Raft + quorum. 3 (or 5) members. Dedicated NVMe with &lt; 10ms p99 fsync. Snapshot every 30 min, defrag weekly, quarterly DR drill. Failed member: remove + add learner + promote. Quorum loss: snapshot restore.',
    recap_next='<strong>Next — V8: Upgrades and Patching.</strong> Cluster doesn\'t stay still. Version skew rules, kubeadm upgrade, control-plane → kubelet → workers → CNI/CSI order, surge nodes, rollback.',
)
