from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="House rules board: posted rules for apiserver, kubelet, kube-proxy, scheduler. Highlights: audit log on, encryption on, system-reserved set, scheduler profile bin-pack.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">RULES BOARD · CLUSTER CONFIG</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">POSTED CONFIGURATION (API server / kubelet / scheduler)</text>
    <rect x="14" y="34" width="186" height="100" rx="4" fill="#3F4A5E"/><text x="107" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">API SERVER</text>
      <text x="22" y="68" font-size="8" fill="#FBE8DC">audit-log-path /var/log/audit.log</text>
      <text x="22" y="80" font-size="8" fill="#FBE8DC">audit-policy-file /etc/k8s/audit.yaml</text>
      <text x="22" y="92" font-size="8" fill="#FBE8DC">encryption-provider-config enc.yaml</text>
      <text x="22" y="104" font-size="8" fill="#FBE8DC">enable-admission-plugins ABAC,…</text>
      <text x="22" y="118" font-size="8" fill="#FBE8DC">apf flow-schemas + priority-levels</text>
    <rect x="206" y="34" width="186" height="100" rx="4" fill="#5A9F7A"/><text x="299" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">KUBELET</text>
      <text x="214" y="68" font-size="8" fill="#FBE8DC">cgroupDriver: systemd</text>
      <text x="214" y="80" font-size="8" fill="#FBE8DC">systemReserved {{cpu, mem, ephemeral}}</text>
      <text x="214" y="92" font-size="8" fill="#FBE8DC">kubeReserved {{cpu, mem}}</text>
      <text x="214" y="104" font-size="8" fill="#FBE8DC">evictionHard {{memory.available 200Mi}}</text>
      <text x="214" y="118" font-size="8" fill="#FBE8DC">topologyManagerPolicy single-numa</text>
    <rect x="398" y="34" width="186" height="100" rx="4" fill="#A04832"/><text x="491" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">SCHEDULER + kube-proxy</text>
      <text x="406" y="68" font-size="8" fill="#FBE8DC">profiles default + bin-pack</text>
      <text x="406" y="80" font-size="8" fill="#FBE8DC">multiple schedulers (Volcano)</text>
      <text x="406" y="92" font-size="8" fill="#FBE8DC">kube-proxy: ipvs OR replaced</text>
      <text x="406" y="104" font-size="8" fill="#FBE8DC">RuntimeClass kata / gvisor</text>
      <text x="406" y="118" font-size="8" fill="#FBE8DC">image-gc + log rotation</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="06",
    title_short="cluster config",
    title_full="V6 · Cluster Configuration (apiserver, kubelet, scheduler, kube-proxy)",
    title_html="K-VAN V6 · Cluster Configuration",
    module_eyebrow="Module V6 · the house rules",
    hero_sub_html='kubeadm sets sane defaults. Production needs intentional tuning: API server flags (audit + encryption + APF), kubelet (eviction + reserved resources + topology manager), scheduler profiles, RuntimeClass, image GC. <strong>Each tuning category has a default — and a production default that beats it.</strong>',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Kubelets start evicting workloads at random. Investigation: <code>--system-reserved</code> wasn\'t set, so the kubelet thinks it has 32 GiB of memory available; the OS + DaemonSets actually use 6 GiB; under load, the kubelet schedules past safe limits, hits OOM-killer, evicts the wrong Pods. Or: API server fills the disk with audit logs because no rotation. Or: encryption-at-rest never enabled because someone forgot the flag. Each is a one-flag fix; finding it from a production fire takes hours.',
    stamp_html='Tune four components: <strong>kube-apiserver</strong> (audit policy, EncryptionConfiguration, admission plugins, APF flow schemas), <strong>kubelet</strong> (cgroupDriver, systemReserved, kubeReserved, evictionHard, CPU/Memory/Topology Manager), <strong>kube-scheduler</strong> (profiles for bin-packing vs spreading; multiple schedulers like Volcano), <strong>kube-proxy</strong> (mode or replaced by Cilium). Plus <strong>RuntimeClass</strong> (Kata / gVisor) for sandboxing. All via kubeadm config, no flag soup.',
    district_pin="kf-site06",
    district_label="Rules Board",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why post-install configuration exists",
            body_html="""    <p>kubeadm gives you a working cluster with safe defaults. \"Safe\" is not the same as \"production-tuned.\" Cloud distros pre-tune most of these knobs for you; vanilla self-managed clusters don\'t. The cost of leaving them as-is shows up as: surprise OOM evictions, audit gaps in compliance reports, secrets in plaintext in etcd backups, scheduler bin-packing that fights HPA decisions.</p>
    <p>Post-install configuration falls into four buckets:</p>
    <ul>
      <li><strong>kube-apiserver</strong>: how requests are observed, encrypted, prioritised, validated.</li>
      <li><strong>kubelet</strong>: how the node manages local resources + when it evicts.</li>
      <li><strong>kube-scheduler / kube-proxy</strong>: how Pods are placed + how Service traffic flows.</li>
      <li><strong>RuntimeClass + image GC + log rotation</strong>: the operational hygiene knobs.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.5 · API server tuning",
            h2="Audit, encryption, admission, APF",
            body_html="""    <p>Critical apiserver flags (set via kubeadm <code>ClusterConfiguration.apiServer.extraArgs</code>):</p>
    <ul>
      <li><strong>Audit logging</strong>: <code>audit-log-path</code>, <code>audit-policy-file</code>. Policy file decides what gets logged at what level (None / Metadata / Request / RequestResponse). Production: log all writes at RequestResponse to a forwarded log destination.</li>
      <li><strong>EncryptionConfiguration</strong>: <code>encryption-provider-config /etc/k8s/encryption.yaml</code>. Encrypts Secrets (and others) at rest in etcd. KMS v2 (K8s 1.31 GA) for production; static AES key for testing only.</li>
      <li><strong>Admission plugins</strong>: <code>enable-admission-plugins</code> = NodeRestriction, NamespaceLifecycle, ServiceAccount, PodSecurity, ValidatingAdmissionPolicy, MutatingAdmissionPolicy, ResourceQuota, LimitRanger, …</li>
      <li><strong>APF (API Priority and Fairness)</strong>: <code>FlowSchema</code> + <code>PriorityLevelConfiguration</code> CRDs. Prevents one noisy client from starving the API.</li>
      <li><strong>Request limits</strong>: <code>max-requests-inflight</code>, <code>max-mutating-requests-inflight</code>. APF supersedes these but they remain hard caps.</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.7 · Kubelet — the most-tuned component",
            h2="Reserved + eviction + topology",
            body_html="""    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># KubeletConfiguration (in kubeadm-config.yaml)
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
serverTLSBootstrap: true          # auto-rotate kubelet serving certs</code></pre>
    <p><strong>node allocatable</strong> = node total − systemReserved − kubeReserved − evictionHard. This is what the scheduler sees as schedulable. Without setting these, the scheduler over-allocates.</p>
    <p><strong>kubelet serving cert rotation</strong>: enable <code>serverTLSBootstrap: true</code> + approve CSRs (manually or via an auto-approver). Otherwise kubelets serve with a self-signed cert; metrics-server / kubectl logs / kubectl exec break.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Scheduler profiles, kube-proxy mode, RuntimeClass",
            h2="The other knobs",
            body_html="""    <p><strong>Scheduler profiles</strong>: the kube-scheduler can run multiple named profiles in one process. Bin-packing for batch (<code>NodeResourcesFit: scoring=MostAllocated</code>); spreading for traffic-serving (default). Multiple schedulers (Volcano, Yunikorn) for ML / batch with gang scheduling.</p>
    <p><strong>kube-proxy mode</strong>: <code>iptables</code> (default), <code>ipvs</code> (better at high Service count), <code>nftables</code> (1.31+ alpha → β; modern). Or replaced entirely by Cilium / Calico eBPF (V4).</p>
    <p><strong>RuntimeClass</strong>: defines alternate runtimes (Kata Containers for VM-isolated Pods; gVisor for syscall-filter sandbox). Pod opts in via <code>spec.runtimeClassName: kata</code>. Useful for untrusted multi-tenant code.</p>
    <p><strong>image GC + log rotation</strong>: kubelet manages container image pruning; configure thresholds. Container logs in <code>/var/log/containers/</code> rotated by kubelet (<code>containerLogMaxSize</code>, <code>containerLogMaxFiles</code>) — set to avoid disk full.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>Feature gates: <code>--feature-gates=GracefulNodeShutdown=true</code> etc. Beta and GA features default on; alpha features default off. Track upcoming features and pre-enable in dev, never alpha in prod.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your nodes\' kubelets start evicting Pods under modest load. <code>kubectl describe node</code> shows allocatable = total. What\'s the diagnosis?',
            options=[
                ('a) The cluster is too small', False),
                ('b) <code>systemReserved</code> + <code>kubeReserved</code> are unset, so allocatable equals total memory; the OS/kubelet/runtime usage isn\'t accounted for and pushes nodes to OOM eviction', True),
                ('c) HPA is misconfigured', False),
            ],
            feedback='<strong>Answer: b.</strong> Without reserved resources, the scheduler sees the full node memory as available for Pods, then the kernel OOM-kills under pressure (since the OS + kubelet + containerd + DaemonSets need their share). Set <code>systemReserved</code> and <code>kubeReserved</code> based on measured baseline; rebuild nodes (kubeadm join with new config) or roll the kubelet config.',
        ),
    },
    before_after_before='<p>kubeadm defaults everywhere. No audit log → compliance gap. No encryption-at-rest → secrets readable from etcd backup. No reserved resources → surprise OOM evictions. No log rotation → disk full. \"Why is X happening?\" answered with shrugs.</p>',
    before_after_after='<p>kubeadm config YAML in git captures every tuned flag. Audit + encryption on. Reserved resources set per node-class. Scheduler profiles match workload mix. RuntimeClass available for sensitive workloads. New cluster = same config; same posture.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Cluster configuration is post-install but pre-workload. Get it right before the first app team onboards.</p>',
    analogy_intro_html='<p>The Rules Board is a posted notice on the homestead\'s central beam. Everyone passing through reads it: how loud you can be after dark (audit), where to lock the safe (encryption), how much firewood is reserved for the household (system/kubeReserved), what to do during a fire (eviction). The rules aren\'t fancy — they\'re the agreements that keep the homestead from collapsing under weather.</p>',
    translation_rows=[
        ('Posted house rules', 'Cluster-wide configuration files'),
        ('"Quiet hours: log everything after 10 PM"', 'audit-policy.yaml'),
        ('"Safe locked, only the cook + sheriff have keys"', 'EncryptionConfiguration + KMS v2'),
        ('"This stack is reserved for the house"', 'systemReserved + kubeReserved'),
        ('"Fire drill: residents evacuate first, livestock second"', 'evictionHard thresholds + Pod priorities'),
        ('"Stovekeeper schedules duties differently for night shift"', 'Multiple scheduler profiles'),
        ('"Visitors from the city use a different gate"', 'RuntimeClass for sandboxed Pods (Kata / gVisor)'),
        ('"Trash burned weekly, ash hauled monthly"', 'image GC + log rotation'),
    ],
    analogy_stops="The analogy stops here: real configuration changes propagate via kubelet restart (rolling) or apiserver restart (brief outage). \"Posting a rule\" doesn\'t restart anything; real rule changes come with operational impact.",
    eli5='Every house has rules: when to be quiet, where to lock things, how much food is reserved for the family. The cluster has the same kind of rules, written down in config files.',
    eli10="kubeadm sets safe defaults; production tunes via ClusterConfiguration: apiserver (audit + EncryptionConfiguration + admission + APF), kubelet (systemReserved + kubeReserved + evictionHard + cgroupDriver + CPU/Memory/Topology Manager + serving cert rotation), scheduler (profiles for bin-pack vs spread, multiple schedulers), kube-proxy (mode or replaced). RuntimeClass for sandboxing. All in one YAML committed to git.",
    scenarios=[
        Scenario(name='A SaaS with reserved resources tuned per node class', body='Worker class A (general): systemReserved 500m/1Gi, kubeReserved 500m/1Gi. Worker class B (memory-intensive): kubeReserved 2Gi (Pods are memory-heavy; scheduler factors in). Documented in the kubeadm-config.yaml per node pool. Allocatable predictable; eviction rare.'),
        Scenario(name='A bank with audit + encryption baseline', body='Audit policy logs every Secret read at RequestResponse + every write to RBAC, NetworkPolicy, ResourceQuota. Forwarded to SIEM. EncryptionConfiguration uses KMS v2 + Vault Transit; Secrets encrypted at rest. Auditor confirms compliance via <code>kubectl get secrets -o yaml | grep -i encrypt</code> on a sample.'),
        Scenario(name='A team using two scheduler profiles', body='Default scheduler (spreading) for traffic-serving Deployments. Bin-packing scheduler for batch / ML training. Pods opt in via <code>spec.schedulerName: bin-pack</code>. Same kube-scheduler binary, two profiles in its config. Spot instances pack tightly; prod spreads across zones.'),
        Scenario(name='A team running Kata for tenant isolation', body='Multi-tenant cluster running customer code. RuntimeClass <code>kata</code> defined; specific namespaces have a Kyverno policy mutating Pods to use it. Each Pod runs in a lightweight VM. Defense-in-depth against kernel exploits.'),
    ],
    misconceptions=[
        Misconception(myth='\"systemReserved is optional.\"', truth='Without it, allocatable = node total. The scheduler over-allocates and the kubelet evicts under pressure. Always set, based on measured baseline OS + DaemonSet usage.'),
        Misconception(myth='\"Audit logs are noise.\"', truth='Untuned audit policy is noise. A good policy logs writes at full detail and reads at metadata-only; total volume is manageable. Compliance, breach forensics, and quiet-time anomaly detection all need audit.'),
        Misconception(myth='\"Encryption-at-rest with a static AES key is good enough.\"', truth='Better than nothing, but the key sits next to the data on the API server\'s disk. KMS v2 with an external KMS (Vault, cloud KMS) is the production answer.'),
    ],
    flashcards=[
        Flashcard(front='node allocatable formula?', back='node total − systemReserved − kubeReserved − evictionHard reservations. This is what the scheduler sees as schedulable.'),
        Flashcard(front='Why <code>cgroupDriver: systemd</code> in kubelet?', back='Must match container runtime (containerd <code>SystemdCgroup = true</code>). Mismatch = kubelet refuses to start with cryptic cgroup errors. Both default to systemd in modern setups.'),
        Flashcard(front='evictionHard thresholds?', back='Memory and disk thresholds at which kubelet starts evicting BestEffort + Burstable Pods. Default soft eviction is too lenient for many workloads; tune <code>memory.available</code>, <code>nodefs.available</code>, <code>imagefs.available</code>.'),
        Flashcard(front='APF — what does it solve?', back='API Priority and Fairness. Prevents one noisy client (a runaway controller, a misbehaving Pod) from starving the API server. FlowSchemas categorise requests; PriorityLevels allocate concurrency.'),
        Flashcard(front='EncryptionConfiguration providers?', back='<code>identity</code> (no encryption), <code>aescbc</code> / <code>secretbox</code> (static AES key), <code>kms</code> (v1 deprecated; v2 GA in 1.31). Production: KMS v2 with an external KMS.'),
        Flashcard(front='Multiple scheduler profiles?', back='kube-scheduler runs N named profiles in one process. Pods opt in via <code>spec.schedulerName</code>. Use bin-pack profile for batch, default (spread) for traffic.'),
        Flashcard(front='What is RuntimeClass?', back='K8s API for selecting alternate container runtimes per Pod. Examples: <code>kata</code> (lightweight VMs), <code>gvisor</code> (syscall sandbox). Defense-in-depth for untrusted workloads.'),
        Flashcard(front='Kubelet serving cert rotation?', back='<code>serverTLSBootstrap: true</code> + a CSR auto-approver (rancher-csr or custom). Without it, kubelets use self-signed certs; metrics-server, kubectl exec/logs all break.'),
    ],
    quizzes=[
        Quiz(prompt='Your apiserver writes audit logs to <code>/var/log/audit.log</code>. Disk fills nightly. What\'s the right pattern?', answer='<strong>Don\'t write audit to local disk for production.</strong> Set <code>audit-log-path</code> + <code>audit-log-maxsize</code> + <code>audit-log-maxbackup</code> + <code>audit-log-maxage</code> for local rotation as a fallback, but configure a <strong>webhook</strong> backend (<code>audit-webhook-config-file</code>) to forward audit events to your SIEM / log lake in real time. Local disk is for debug only. <strong>Tune the audit policy</strong> to log writes at RequestResponse and reads at Metadata; otherwise even a healthy cluster generates GB/day. <strong>Volume sanity check</strong>: ~30K-100K events/day in a typical cluster; if you see millions, the policy is over-broad.'),
        Quiz(prompt='You enable <code>topologyManagerPolicy: single-numa-node</code>. After the kubelet restart, some previously-running Pods are now Pending forever. Why?', answer='Topology Manager <code>single-numa-node</code> policy requires every Pod\'s CPU + memory + (optionally) devices to fit on one NUMA node. If the Pod requests 16 CPU but each NUMA node has only 8 CPU, the Pod can never be admitted. <strong>Diagnose:</strong> <code>kubectl describe pod</code> shows the rejection reason. <strong>Fix:</strong> either reduce the Pod\'s request to fit one NUMA node, or relax to <code>policy: restricted</code> (warn but allow), or to <code>best-effort</code> (try, allow regardless). <strong>Lesson:</strong> <code>single-numa-node</code> is a correctness setting for latency-critical workloads; for general workloads it can cause Pending. Enable per-node-class via per-pool kubelet config, not cluster-wide.'),
        Quiz(prompt='You\'re asked to add audit + encryption-at-rest + APF to an existing cluster without downtime. <strong>Click for the playbook. ▼</strong>', cyoa=True, cyoa_tag='the playbook', answer='<strong>(1) Audit:</strong> write an <code>audit-policy.yaml</code> covering writes-at-RequestResponse + reads-at-Metadata for sensitive resources (secrets, RBAC, NP). <strong>(2) Encryption:</strong> create an <code>encryption-config.yaml</code> with KMS v2 provider pointing at Vault Transit (or static AES if no KMS). <strong>(3) Stage:</strong> push both files to <code>/etc/kubernetes/</code> on every CP node. <strong>(4) Edit static-pod manifest</strong> for kube-apiserver: <code>/etc/kubernetes/manifests/kube-apiserver.yaml</code>. Add <code>--audit-log-path</code>, <code>--audit-policy-file</code>, <code>--encryption-provider-config</code>. The kubelet auto-restarts the static pod on file change. <strong>(5) APF:</strong> verify FlowSchemas and PriorityLevelConfigurations are present (kubeadm 1.20+ ships defaults). Customise via custom CRDs if you have known noisy clients. <strong>(6) Encrypt existing Secrets:</strong> <code>kubectl get secrets -A -o json | kubectl replace -f -</code> rewrites them and triggers re-encryption. <strong>(7) Verify:</strong> grep an etcd dump for a Secret value — should be ciphertext. Audit log shows recent operations. APF metrics on Prometheus dashboard. <strong>Total downtime:</strong> ~30s per CP node as the static pod restarts. Roll one CP at a time; HA absorbs.'),
    ],
    glossary=[
        GlossaryItem(name='ClusterConfiguration', definition='kubeadm config kind for cluster-wide settings (apiserver flags, etcd, networking).'),
        GlossaryItem(name='KubeletConfiguration', definition='kubeadm config kind for kubelet settings (cgroupDriver, eviction, reserved, topology).'),
        GlossaryItem(name='Audit policy', definition='YAML defining what apiserver requests are logged at what level. Levels: None, Metadata, Request, RequestResponse.'),
        GlossaryItem(name='EncryptionConfiguration', definition='File pointed at by <code>encryption-provider-config</code>. Lists providers (KMS v2 / aescbc / identity) per resource.'),
        GlossaryItem(name='APF', definition='API Priority and Fairness. Prevents request starvation. CRDs: FlowSchema, PriorityLevelConfiguration.'),
        GlossaryItem(name='node allocatable', definition='Schedulable resources after subtracting systemReserved + kubeReserved + evictionHard from node total.'),
        GlossaryItem(name='evictionHard', definition='Thresholds at which kubelet evicts Pods to recover resources. <code>memory.available</code>, <code>nodefs.available</code>, etc.'),
        GlossaryItem(name='Topology Manager', definition='Kubelet coordinator for CPU + memory + device locality. Policies: best-effort, restricted, single-numa-node.'),
        GlossaryItem(name='Scheduler profile', definition='Named plugin/scoring config in kube-scheduler. Multiple per process. Pods opt in via <code>schedulerName</code>.'),
        GlossaryItem(name='RuntimeClass', definition='K8s API selecting alternate container runtime per Pod. Kata, gVisor, default.'),
        GlossaryItem(name='Image GC thresholds', definition='Kubelet settings (<code>imageGCHigh/LowThresholdPercent</code>) controlling when to prune unused container images.'),
        GlossaryItem(name='Container log rotation', definition='Kubelet settings (<code>containerLogMaxSize</code>, <code>containerLogMaxFiles</code>) controlling rotation of <code>/var/log/containers/*</code>.'),
    ],
    recap_lead='Tune apiserver (audit + encryption + APF), kubelet (reserved + eviction + topology + serving certs), scheduler (profiles), kube-proxy (mode), RuntimeClass. All via kubeadm config in git. Production-tuned ≠ defaults.',
    recap_next='<strong>Next — V7: etcd Production-Grade.</strong> The well below the homestead. Raft, quorum, snapshots, defrag, disaster recovery.',
)
