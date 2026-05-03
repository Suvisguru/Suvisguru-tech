from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drill square: scenarios pinned to a corkboard - expired certs, broken CNI, broken CoreDNS, apiserver down, etcd down, webhook-blocked apiserver, accidentally deleted namespace.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">DRILL SQUARE · DISASTER SCENARIOS</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">SEVEN DISASTERS · DRILL EACH ONE</text>
    <rect x="14" y="34" width="180" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="104" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">1 expired control-plane certs</text><text x="104" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">kubeadm certs renew all</text>
    <rect x="200" y="34" width="180" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="290" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">2 broken CNI</text><text x="290" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">restore conf + restart pods</text>
    <rect x="386" y="34" width="200" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="486" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">3 broken CoreDNS</text><text x="486" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">fix Corefile · resolvconf trace</text>
    <rect x="14" y="76" width="180" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="104" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">4 API server down</text><text x="104" y="104" text-anchor="middle" font-size="7" fill="#5A4F45">static-pod manifest + kubelet</text>
    <rect x="200" y="76" width="180" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="290" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">5 etcd quorum loss</text><text x="290" y="104" text-anchor="middle" font-size="7" fill="#5A4F45">snapshot restore (V7)</text>
    <rect x="386" y="76" width="200" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="486" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">6 webhook blocks apiserver</text><text x="486" y="104" text-anchor="middle" font-size="7" fill="#5A4F45">edit static-pod --disable-admission</text>
    <rect x="14" y="118" width="572" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="300" y="134" text-anchor="middle" font-size="9" font-weight="700" fill="#A04832">7 accidentally deleted namespace</text><text x="300" y="146" text-anchor="middle" font-size="7" fill="#5A4F45">Velero restore namespace ns-name --include-namespaces</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="10",
    title_short="troubleshooting",
    title_full="V10 · Advanced Vanilla Troubleshooting (full disaster scenarios)",
    title_html="K-VAN V10 · Advanced Vanilla Troubleshooting",
    module_eyebrow="Module V10 · the drill square",
    hero_sub_html='Self-managed K8s breaks in ways managed clusters never do — because there\'s nobody else to call. <strong>Drill the disasters before they happen.</strong> Seven scenarios, each with a documented recovery path. Run them as a tournament.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Routine apiserver restart fails. <code>journalctl -u kubelet</code> shows <code>x509: certificate has expired</code>. Diagnosis: control-plane certs expired (default 1-year TTL); kubeadm renew never ran. The cluster\'s API is down; <code>kubectl</code> doesn\'t work; you can\'t even SSH-fix from kubectl. Recovery: SSH to a CP node, <code>kubeadm certs renew all</code>, restart static-pod manifests. <em>You learned about kubeadm cert renewal in production at 3 AM</em>. Today\'s lesson is the seven disasters every self-managed operator should drill in advance.',
    stamp_html='Drill seven disasters: <strong>(1) expired CP certs</strong> (<code>kubeadm certs renew all</code>); <strong>(2) broken CNI</strong> (delete + reinstall DaemonSet, restart Pods); <strong>(3) broken CoreDNS</strong> (fix Corefile, restart); <strong>(4) apiserver down</strong> (fix static-pod manifest); <strong>(5) etcd quorum loss</strong> (snapshot restore — V7); <strong>(6) webhook blocking apiserver</strong> (edit static-pod manifest to disable admission temporarily); <strong>(7) accidentally deleted namespace</strong> (Velero restore). Run as tournament; document each recovery in a runbook.',
    district_pin="kf-site10",
    district_label="Drill Square",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why drill disasters",
            body_html="""    <p>Production troubleshooting is two skills layered: <em>diagnosis</em> (figuring out what\'s wrong) and <em>execution</em> (running the recovery commands without hesitation). Diagnosis is mostly experience; execution is muscle memory. Drilling builds both.</p>
    <p>The seven scenarios in this module are the most common high-impact failures in vanilla K8s — the ones where a confident, prepared operator restores service in 15 minutes and an unprepared one takes 3 hours + makes things worse. The discipline difference is the drill.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Scenarios 1-3 (apiserver-side state)",
            h2="Certs, CNI, CoreDNS",
            body_html="""    <p><strong>1. Expired control-plane certs.</strong> Default kubeadm cert TTL: 1 year. Symptoms: kubectl fails with x509-expired; kubelet logs show same. Recovery:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>sudo kubeadm certs check-expiration         # see what's expired
sudo kubeadm certs renew all                # re-issue all certs
# Restart control-plane static pods (kubelet detects file change):
sudo systemctl restart kubelet
# On every CP node. Repeat for kubelet client cert if needed.</code></pre>
    <p><strong>Prevention:</strong> automate cert renewal: a Jan/Feb maintenance window every year (or run <code>kubeadm certs renew all</code> as a CronJob nightly). Or use Talos / cert-manager-managed cluster certs.</p>
    <p><strong>2. Broken CNI</strong> (e.g., bad Helm upgrade). Symptoms: new Pods stuck in <code>ContainerCreating</code>, network connectivity broken. Recovery:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># Diagnose: check CNI Pod logs (on each node)
kubectl -n kube-system logs ds/cilium

# If borked: roll back Helm release
helm history cilium -n kube-system
helm rollback cilium &lt;previous-revision&gt; -n kube-system

# Force-restart CNI Pods
kubectl -n kube-system rollout restart ds/cilium</code></pre>
    <p><strong>3. Broken CoreDNS</strong>. Symptoms: in-cluster DNS lookups fail; <code>nslookup kubernetes.default</code> from a Pod times out. Recovery: check Corefile (ConfigMap <code>coredns</code>), check CoreDNS Pod logs, restart Deployment.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Scenarios 4-6 (control-plane-state)",
            h2="apiserver, etcd, webhook lockout",
            body_html="""    <p><strong>4. API server down.</strong> Symptoms: <code>kubectl get nodes</code> hangs / refuses connection. Recovery: SSH to a CP node, <code>journalctl -u kubelet</code> for the static-pod state, <code>crictl ps -a | grep kube-apiserver</code> for container state. Common causes: bad <code>--encryption-provider-config</code> path, bad audit policy YAML, etcd unreachable. Edit <code>/etc/kubernetes/manifests/kube-apiserver.yaml</code> to fix; kubelet auto-restarts the static pod within ~20s.</p>
    <p><strong>5. etcd quorum loss.</strong> Covered in V7. Snapshot restore is the recovery.</p>
    <p><strong>6. Webhook blocks apiserver.</strong> Self-inflicted disaster: a ValidatingAdmissionWebhook with <code>failurePolicy: Fail</code> targets <code>*</code> resources; the webhook Pod itself can\'t be created (it depends on apiserver, which calls the webhook for everything). Cluster wedged. Recovery:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># SSH to a CP node, edit the kube-apiserver static-pod manifest:
sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml
# Add to args:
#   - --disable-admission-plugins=ValidatingAdmissionWebhook,MutatingAdmissionWebhook
# kubelet auto-restarts apiserver within ~20s
# kubectl works again; delete the bad webhook config; remove the disable flag</code></pre>
    <p><strong>Prevention:</strong> webhooks should always exclude themselves + <code>kube-system</code> in their <code>namespaceSelector</code>; set <code>failurePolicy: Fail</code> only after careful testing on staging.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · Scenarios 7 + tournament protocol",
            h2="Velero restore + how to run a chaos drill",
            body_html="""    <p><strong>7. Accidentally deleted namespace via Velero.</strong> Someone runs <code>kubectl delete ns prod</code>. Cascading delete removes every Pod, Service, ConfigMap, Secret, PVC in that namespace. Apps go down hard. Recovery (assuming Velero backup exists):</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>velero backup get                        # find recent backup
velero restore create --from-backup nightly-20260503 \\
  --include-namespaces prod \\
  --restore-volumes=true</code></pre>
    <p>PVCs restore from snapshots if Velero was configured with the snapshot plugin. Pods recreate themselves; Services + ConfigMaps + Secrets come back. Total time: ~5-15 min depending on data size.</p>
    <p><strong>Tournament protocol</strong> (run quarterly):</p>
    <ol>
      <li>Build a non-prod cluster identical to production.</li>
      <li>Two-person team: one is the chaos engineer (introduces a failure from the seven), one is the on-call (recovers blind).</li>
      <li>Score: time-to-mitigation, completeness, blast radius caused by the recovery itself.</li>
      <li>Rotate roles. Each engineer recovers each scenario at least once a year.</li>
      <li>Update runbooks based on what surprised people.</li>
    </ol>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>Tools to make drills cheap: <strong>Chaos Mesh</strong>, <strong>LitmusChaos</strong> for scripted chaos. <strong>k6</strong> for load while injecting faults. Schedule a quarterly half-day; track score over time.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your apiserver is down because someone deployed a webhook with <code>failurePolicy: Fail</code> targeting <code>*/*</code>. <code>kubectl</code> doesn\'t work. What\'s the recovery sequence?',
            options=[
                ('a) Wait — the webhook controller will fix itself', False),
                ('b) SSH to a CP node, edit /etc/kubernetes/manifests/kube-apiserver.yaml to add --disable-admission-plugins=ValidatingAdmissionWebhook,MutatingAdmissionWebhook, kubelet auto-restarts apiserver, then kubectl delete the bad webhook config, then remove the disable flag', True),
                ('c) Restore etcd from snapshot', False),
            ],
            feedback='<strong>Answer: b.</strong> Static pod manifests bypass admission. Adding the disable flag breaks the webhook chain temporarily, lets the apiserver come up, you fix the webhook config, then restore admission. <strong>Prevention</strong>: webhook configs should exclude their own namespace + kube-system.',
        ),
    },
    before_after_before='<p>Each disaster discovered live, in production, at 3 AM. Documentation is whatever the on-call typed in Slack while sweating. Recovery time wildly variable; depends on who\'s on call. Half-resolved fixes cause secondary outages. \"We need to write a runbook\" said monthly, never done.</p>',
    before_after_after='<p>Quarterly tournament. Each engineer has recovered each disaster at least once. Runbooks are version-controlled, tested, recently used. New on-call onboarded by walking through the runbooks. P0 recovery time: predictable + bounded.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">The cluster you\'ve drilled is the cluster you can fix. The cluster you haven\'t drilled is the one you\'re afraid of.</p>',
    analogy_intro_html='<p>The Drill Square is where the homestead practises emergencies. Not real emergencies — controlled ones, in a designated area, with a trainer. The well goes dry (etcd quorum loss) — practise the parallel-well drilling. The watchtower locks up (apiserver down) — practise the static-manifest restart. The fence falls (webhook lockout) — practise the disable-and-rebuild. Each drill ends with a debrief: what was hard, what was missing from the runbook, who needs more practice. The square is muddy from use — that\'s how you know the homestead is ready.</p>',
    translation_rows=[
        ('Drill square', 'Disaster recovery rehearsal cluster'),
        ('Trainer with the scenario card', 'Chaos engineer in the drill'),
        ('On-call recruit recovering blind', 'Engineer being trained on the runbook'),
        ('Stopwatch', 'Time-to-mitigation metric'),
        ('Debrief around the bonfire', 'Post-drill review + runbook updates'),
        ('Spare bucket of sand for the well', 'Velero snapshots for namespace restore'),
        ('Posted gate-unlock procedure', 'Static-pod manifest edit for apiserver lockout'),
        ('Annual readiness inspection', 'Quarterly tournament protocol'),
    ],
    analogy_stops="The analogy stops here: real K8s disasters cascade in ways the drill square can't fully simulate. A real CNI outage during a real production peak is qualitatively different from a planned drill. Drill builds the muscle memory; production tests it.",
    eli5='Practise the fire drill before the fire. Then it doesn\'t feel scary when it really happens. The homestead has seven kinds of fire drill; everyone takes a turn at each one.',
    eli10="Seven recurring vanilla-K8s disasters: expired CP certs (kubeadm certs renew all), broken CNI (helm rollback or restart DaemonSet), broken CoreDNS (fix Corefile + restart), apiserver down (edit static-pod manifest), etcd quorum loss (snapshot restore), webhook blocking apiserver (disable admission via static-pod arg), deleted namespace (Velero restore). Drill quarterly: chaos engineer + on-call recover blind; runbooks updated based on what surprised people.",
    scenarios=[
        Scenario(name='A SaaS running quarterly chaos days', body='Off-peak Friday afternoon. Two-person teams; chaos engineer + on-call. Each scenario from V10 ran once. Score: time-to-mitigation. Track over 4 quarters: from 90 min average → 25 min average. Runbooks rewritten three times based on drill findings.'),
        Scenario(name='A team that automated cert renewal', body='Annual cert expiration was a recurring P0. Now: a CronJob runs <code>kubeadm certs renew all</code> 30 days before expiry; alerts if it fails. Plus a Prometheus alert at 60-day cert expiry. No more cert-expiry incidents in the last 18 months.'),
        Scenario(name='A team recovering a deleted prod namespace', body='Engineer copy-pasted a delete command from a wiki. <code>kubectl delete ns prod</code> ran. Team realised within 90 seconds. Velero restore from 6-hour-old backup; PVCs restored from snapshots; Pods reconciled by their controllers. Total downtime: ~12 min. Post-mortem: added Kyverno policy preventing namespace delete in production via RBAC + audit.'),
        Scenario(name='A team that hit the webhook lockout', body='Bad Kyverno upgrade introduced a CRD that referenced itself (chicken/egg). Apiserver wedged. Recovery: edit kube-apiserver static-pod manifest to disable webhooks; cluster came back; uninstall Kyverno; reinstall correctly. Total downtime: 30 min. Runbook now includes \"webhook lockout\" with exact yaml edit.'),
    ],
    misconceptions=[
        Misconception(myth='\"We don\'t need disaster drills; we\'ve never had a disaster.\"', truth='You will. Vanilla K8s has known failure modes that hit every cluster eventually. Drill before; recover faster when. The first time you do <code>kubeadm certs renew all</code> shouldn\'t be in production at 3 AM.'),
        Misconception(myth='\"Velero is enough for namespace restore — no need to test it.\"', truth='Untested Velero is fiction. Restore drills find: missing snapshot config, expired credentials, schema mismatches between Velero versions, missing Custom Resources, workloads that don\'t reconcile cleanly post-restore. Test quarterly.'),
        Misconception(myth='\"Apiserver wedged → reboot the node.\"', truth='If kube-apiserver static pod is failing, rebooting just makes it fail again. Diagnose by reading the static-pod manifest + kubelet logs + the apiserver container logs. Fix the manifest; kubelet will restart the static pod automatically.'),
    ],
    flashcards=[
        Flashcard(front='kubeadm cert TTL?', back='1 year by default. Renew with <code>kubeadm certs renew all</code> + restart static pods (kubelet auto-restarts on file change).'),
        Flashcard(front='Recovery for a broken CNI Helm upgrade?', back='<code>helm history</code> + <code>helm rollback</code> to last good revision; <code>kubectl rollout restart ds/&lt;cni&gt;</code> in kube-system. Verify <code>cilium status</code> or equivalent.'),
        Flashcard(front='CoreDNS not resolving in-cluster?', back='Check Corefile (<code>kubectl -n kube-system get cm coredns -o yaml</code>); CoreDNS Pod logs for parse errors; restart Deployment after fixing.'),
        Flashcard(front='Apiserver down — first diagnostic step?', back='SSH to a CP node, <code>journalctl -u kubelet</code> + <code>crictl ps -a | grep kube-apiserver</code> + <code>crictl logs &lt;container-id&gt;</code>. Static-pod manifest is the source of truth for apiserver config.'),
        Flashcard(front='etcd quorum lost — what?', back='Snapshot restore (V7). Bring up fresh 3-member etcd from the snapshot; restart kube-apiserver static pods.'),
        Flashcard(front='Webhook blocking apiserver — the trick?', back='Static-pod manifests bypass admission. Edit kube-apiserver.yaml: add <code>--disable-admission-plugins=ValidatingAdmissionWebhook,MutatingAdmissionWebhook</code>. Kubelet auto-restarts. Fix the bad webhook; remove the flag.'),
        Flashcard(front='Velero restore single namespace?', back='<code>velero restore create --from-backup &lt;name&gt; --include-namespaces &lt;ns&gt; --restore-volumes=true</code>. Requires PVC snapshot plugin if you want PVs back.'),
        Flashcard(front='Quarterly tournament protocol?', back='Build a non-prod cluster. Pair: chaos engineer + on-call. Each scenario drilled once per quarter. Track time-to-mitigation. Update runbooks. Rotate roles so everyone has recovered each disaster.'),
    ],
    quizzes=[
        Quiz(prompt='Your apiserver static pod is in CrashLoopBackOff. <code>crictl logs</code> on the most recent container shows: <code>error reading encryption-config-file: stat /etc/kubernetes/enc/encryption.yaml: no such file or directory</code>. Walk recovery.', answer='<strong>Diagnosis is in the log.</strong> Apiserver was reconfigured to use an encryption config file; the file is missing on this node. <strong>Fix:</strong> SSH to the CP node. Either: (a) place the missing encryption.yaml at the expected path (the same one that lives on other CP nodes; <code>scp</code> from a healthy peer); or (b) edit the static-pod manifest to remove the <code>--encryption-provider-config</code> arg temporarily. After (a) the kubelet detects the manifest unchanged and the apiserver starts. After (b) you can <code>kubectl apply</code> a Secret with the file content + redeploy properly. <strong>Prevention:</strong> the encryption.yaml should be deployed to every CP node atomically (Ansible / Talos machine-config / kubeadm config). Hand-deployment to one node + missing on another is the classic V6 hardening shortcut that bites V10 later.'),
        Quiz(prompt='Your CoreDNS Pods have been stable for months. After upgrading the cluster, all in-cluster DNS lookups fail with NXDOMAIN. The CoreDNS Pods themselves are Running. Diagnose.', answer='<strong>Common cause: Corefile schema mismatch.</strong> CoreDNS plugin syntax changes occasionally between versions; an older Corefile may reference a removed or renamed plugin. <strong>Diagnose:</strong> <code>kubectl -n kube-system logs deploy/coredns</code> often shows parse warnings. <code>kubectl -n kube-system get cm coredns -o yaml</code> + compare to the upstream default for the new version. <strong>Fix:</strong> update Corefile; restart Deployment (<code>kubectl rollout restart deploy/coredns -n kube-system</code>). <strong>Other possibilities:</strong> CoreDNS Pod\'s <code>readinessProbe</code> failing for a different reason (memory limit too tight, DNS upstream unreachable). <code>kubectl describe pod</code> shows the readiness state. <strong>Prevention:</strong> include CoreDNS upgrade in the pre-K8s-upgrade staging rehearsal; bump CoreDNS chart in same change as K8s minor.'),
        Quiz(prompt='Your team is running its first quarterly chaos tournament. <strong>Click for the protocol. ▼</strong>', cyoa=True, cyoa_tag='the protocol', answer='<strong>(1) Build the drill cluster.</strong> Same K8s version + add-on stack as production, on a separate VM pool. Velero backups taken pre-drill (so you can reset between scenarios). <strong>(2) Pair up.</strong> Two-person teams: A is chaos engineer (introduces failure, observes), B is on-call (recovers blind). <strong>(3) Round 1: certs.</strong> A: SSH to a CP node, <code>find /etc/kubernetes/pki -name "*.crt" -exec openssl x509 -in {} -dates -noout \\;</code> finds the expiry; A uses <code>faketime -1 year</code> to advance system clock OR manually rotates a cert with a 1-day TTL. B sees alerts; B walks recovery procedure. Stopwatch from \"alert fires\" to \"<code>kubectl get nodes</code> works\". <strong>(4) Reset cluster</strong> (Velero restore). <strong>(5) Round 2: CNI.</strong> A: <code>kubectl -n kube-system delete ds cilium</code>. B: notices new Pods stuck ContainerCreating; <code>helm install</code> Cilium back. <strong>(6) Repeat for scenarios 3-7.</strong> <strong>(7) Debrief.</strong> What was hard? What was missing from the runbook? Update runbooks. <strong>(8) Score keep + circulate.</strong> Visible to leadership; resourcing decisions follow. <strong>(9) Schedule next quarter.</strong> Same cluster reused. Cumulative knowledge after 4 quarters: every engineer has recovered every scenario.'),
    ],
    glossary=[
        GlossaryItem(name='kubeadm certs renew', definition='Subcommand: regenerates control-plane certificates using the cluster CA. Restart kubelet to pick up.'),
        GlossaryItem(name='Static pod manifest', definition='Pod spec YAML in <code>/etc/kubernetes/manifests/</code>. Kubelet runs these before apiserver is up; auto-restarts on file change. Source of truth for control-plane config.'),
        GlossaryItem(name='disable-admission-plugins flag', definition='kube-apiserver flag to disable specific admission plugins. Used as recovery for webhook lockout.'),
        GlossaryItem(name='Velero', definition='K8s backup tool. Backs up resources + PVCs (with snapshot plugin) to S3-compatible storage.'),
        GlossaryItem(name='Velero restore --include-namespaces', definition='Restore a single namespace from a backup. Survives accidental namespace deletion.'),
        GlossaryItem(name='Chaos Mesh', definition='CNCF chaos engineering framework. Inject Pod kills, network partitions, IO faults via CRDs.'),
        GlossaryItem(name='LitmusChaos', definition='CNCF chaos engineering platform. Workflow-based experiments + steady-state hypotheses.'),
        GlossaryItem(name='Tournament protocol', definition='Pair-based disaster drill. Chaos engineer introduces failure; on-call recovers blind. Track time-to-mitigation.'),
        GlossaryItem(name='Webhook lockout', definition='Self-inflicted: webhook config blocks the very requests it needs (e.g., webhook Pod\'s creation). Recovery via static-pod admission disable.'),
        GlossaryItem(name='Time-to-mitigation', definition='Wall-clock time from incident detection to service restored. Tracked across drills + real incidents.'),
        GlossaryItem(name='Runbook', definition='Documented recovery procedure for a specific failure mode. Tested + maintained via drills.'),
        GlossaryItem(name='Post-drill debrief', definition='Review after each chaos drill. What was hard? What was missing? Update runbook + tooling.'),
    ],
    recap_lead='Seven disasters every self-managed K8s operator should drill: cert expiry, broken CNI, broken CoreDNS, apiserver down, etcd quorum loss, webhook lockout, namespace delete + Velero restore. Quarterly tournament; runbooks updated each cycle.',
    recap_next='<strong>Next — V11: Capstone.</strong> Build, harden, back up, upgrade, and recover an HA on-prem cluster on Talos with Cilium + Gateway API + cert-manager + Velero + kube-prometheus-stack + Argo CD. End-to-end project tying every module together.',
)
