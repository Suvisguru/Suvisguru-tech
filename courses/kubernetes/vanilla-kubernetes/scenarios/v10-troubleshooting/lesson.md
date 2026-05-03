# K-VAN V10 — V10 · Advanced Vanilla Troubleshooting (full disaster scenarios)

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V10 · Advanced Troubleshooting
> Companion preview: `/preview-kubernetes-vanilla-lesson-10.html`.

---

**🎯 If you remember nothing else:** Drill seven disasters: **(1) expired CP certs** (`kubeadm certs renew all`); **(2) broken CNI** (delete + reinstall DaemonSet, restart Pods); **(3) broken CoreDNS** (fix Corefile, restart); **(4) apiserver down** (fix static-pod manifest); **(5) etcd quorum loss** (snapshot restore — V7); **(6) webhook blocking apiserver** (edit static-pod manifest to disable admission temporarily); **(7) accidentally deleted namespace** (Velero restore). Run as tournament; document each recovery in a runbook.

## 1. Why drill disasters

Production troubleshooting is two skills layered: *diagnosis* (figuring out what's wrong) and *execution* (running the recovery commands without hesitation). Diagnosis is mostly experience; execution is muscle memory. Drilling builds both.
    The seven scenarios in this module are the most common high-impact failures in vanilla K8s — the ones where a confident, prepared operator restores service in 15 minutes and an unprepared one takes 3 hours + makes things worse. The discipline difference is the drill.

## 2. Certs, CNI, CoreDNS

**1. Expired control-plane certs.** Default kubeadm cert TTL: 1 year. Symptoms: kubectl fails with x509-expired; kubelet logs show same. Recovery:
    `sudo kubeadm certs check-expiration         # see what's expired
sudo kubeadm certs renew all                # re-issue all certs
# Restart control-plane static pods (kubelet detects file change):
sudo systemctl restart kubelet
# On every CP node. Repeat for kubelet client cert if needed.`
    **Prevention:** automate cert renewal: a Jan/Feb maintenance window every year (or run `kubeadm certs renew all` as a CronJob nightly). Or use Talos / cert-manager-managed cluster certs.
    **2. Broken CNI** (e.g., bad Helm upgrade). Symptoms: new Pods stuck in `ContainerCreating`, network connectivity broken. Recovery:
    `# Diagnose: check CNI Pod logs (on each node)
kubectl -n kube-system logs ds/cilium

# If borked: roll back Helm release
helm history cilium -n kube-system
helm rollback cilium <previous-revision> -n kube-system

# Force-restart CNI Pods
kubectl -n kube-system rollout restart ds/cilium`
    **3. Broken CoreDNS**. Symptoms: in-cluster DNS lookups fail; `nslookup kubernetes.default` from a Pod times out. Recovery: check Corefile (ConfigMap `coredns`), check CoreDNS Pod logs, restart Deployment.

## 3. apiserver, etcd, webhook lockout

**4. API server down.** Symptoms: `kubectl get nodes` hangs / refuses connection. Recovery: SSH to a CP node, `journalctl -u kubelet` for the static-pod state, `crictl ps -a | grep kube-apiserver` for container state. Common causes: bad `--encryption-provider-config` path, bad audit policy YAML, etcd unreachable. Edit `/etc/kubernetes/manifests/kube-apiserver.yaml` to fix; kubelet auto-restarts the static pod within ~20s.
    **5. etcd quorum loss.** Covered in V7. Snapshot restore is the recovery.
    **6. Webhook blocks apiserver.** Self-inflicted disaster: a ValidatingAdmissionWebhook with `failurePolicy: Fail` targets `*` resources; the webhook Pod itself can't be created (it depends on apiserver, which calls the webhook for everything). Cluster wedged. Recovery:
    `# SSH to a CP node, edit the kube-apiserver static-pod manifest:
sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml
# Add to args:
#   - --disable-admission-plugins=ValidatingAdmissionWebhook,MutatingAdmissionWebhook
# kubelet auto-restarts apiserver within ~20s
# kubectl works again; delete the bad webhook config; remove the disable flag`
    **Prevention:** webhooks should always exclude themselves + `kube-system` in their `namespaceSelector`; set `failurePolicy: Fail` only after careful testing on staging.

## 4. Velero restore + how to run a chaos drill

**7. Accidentally deleted namespace via Velero.** Someone runs `kubectl delete ns prod`. Cascading delete removes every Pod, Service, ConfigMap, Secret, PVC in that namespace. Apps go down hard. Recovery (assuming Velero backup exists):
    `velero backup get                        # find recent backup
velero restore create --from-backup nightly-20260503 \
  --include-namespaces prod \
  --restore-volumes=true`
    PVCs restore from snapshots if Velero was configured with the snapshot plugin. Pods recreate themselves; Services + ConfigMaps + Secrets come back. Total time: ~5-15 min depending on data size.
    **Tournament protocol** (run quarterly):
    
      - Build a non-prod cluster identical to production.

      - Two-person team: one is the chaos engineer (introduces a failure from the seven), one is the on-call (recovers blind).

      - Score: time-to-mitigation, completeness, blast radius caused by the recovery itself.

      - Rotate roles. Each engineer recovers each scenario at least once a year.

      - Update runbooks based on what surprised people.

    
    [ deep dive — skip if new ]Tools to make drills cheap: **Chaos Mesh**, **LitmusChaos** for scripted chaos. **k6** for load while injecting faults. Schedule a quarterly half-day; track score over time.

## Before / After

**Before.** Each disaster discovered live, in production, at 3 AM. Documentation is whatever the on-call typed in Slack while sweating. Recovery time wildly variable; depends on who's on call. Half-resolved fixes cause secondary outages. "We need to write a runbook" said monthly, never done.

**After.** Quarterly tournament. Each engineer has recovered each disaster at least once. Runbooks are version-controlled, tested, recently used. New on-call onboarded by walking through the runbooks. P0 recovery time: predictable + bounded.

The cluster you've drilled is the cluster you can fix. The cluster you haven't drilled is the one you're afraid of.

## Analogy — the K-Frontier site

The Drill Square is where the homestead practises emergencies. Not real emergencies — controlled ones, in a designated area, with a trainer. The well goes dry (etcd quorum loss) — practise the parallel-well drilling. The watchtower locks up (apiserver down) — practise the static-manifest restart. The fence falls (webhook lockout) — practise the disable-and-rebuild. Each drill ends with a debrief: what was hard, what was missing from the runbook, who needs more practice. The square is muddy from use — that's how you know the homestead is ready.

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| Drill square | Disaster recovery rehearsal cluster |
| Trainer with the scenario card | Chaos engineer in the drill |
| On-call recruit recovering blind | Engineer being trained on the runbook |
| Stopwatch | Time-to-mitigation metric |
| Debrief around the bonfire | Post-drill review + runbook updates |
| Spare bucket of sand for the well | Velero snapshots for namespace restore |
| Posted gate-unlock procedure | Static-pod manifest edit for apiserver lockout |
| Annual readiness inspection | Quarterly tournament protocol |

⚠️ *Analogy stops here:* The analogy stops here: real K8s disasters cascade in ways the drill square can't fully simulate. A real CNI outage during a real production peak is qualitatively different from a planned drill. Drill builds the muscle memory; production tests it.

## ELI5 / ELI10

**ELI5.** Practise the fire drill before the fire. Then it doesn't feel scary when it really happens. The homestead has seven kinds of fire drill; everyone takes a turn at each one.

**ELI10.** Seven recurring vanilla-K8s disasters: expired CP certs (kubeadm certs renew all), broken CNI (helm rollback or restart DaemonSet), broken CoreDNS (fix Corefile + restart), apiserver down (edit static-pod manifest), etcd quorum loss (snapshot restore), webhook blocking apiserver (disable admission via static-pod arg), deleted namespace (Velero restore). Drill quarterly: chaos engineer + on-call recover blind; runbooks updated based on what surprised people.

## Real-world scenarios

- **A SaaS running quarterly chaos days.** Off-peak Friday afternoon. Two-person teams; chaos engineer + on-call. Each scenario from V10 ran once. Score: time-to-mitigation. Track over 4 quarters: from 90 min average → 25 min average. Runbooks rewritten three times based on drill findings.
- **A team that automated cert renewal.** Annual cert expiration was a recurring P0. Now: a CronJob runs `kubeadm certs renew all` 30 days before expiry; alerts if it fails. Plus a Prometheus alert at 60-day cert expiry. No more cert-expiry incidents in the last 18 months.
- **A team recovering a deleted prod namespace.** Engineer copy-pasted a delete command from a wiki. `kubectl delete ns prod` ran. Team realised within 90 seconds. Velero restore from 6-hour-old backup; PVCs restored from snapshots; Pods reconciled by their controllers. Total downtime: ~12 min. Post-mortem: added Kyverno policy preventing namespace delete in production via RBAC + audit.
- **A team that hit the webhook lockout.** Bad Kyverno upgrade introduced a CRD that referenced itself (chicken/egg). Apiserver wedged. Recovery: edit kube-apiserver static-pod manifest to disable webhooks; cluster came back; uninstall Kyverno; reinstall correctly. Total downtime: 30 min. Runbook now includes "webhook lockout" with exact yaml edit.

## Common misconceptions

- **Myth:** "We don't need disaster drills; we've never had a disaster."
  **Truth:** You will. Vanilla K8s has known failure modes that hit every cluster eventually. Drill before; recover faster when. The first time you do `kubeadm certs renew all` shouldn't be in production at 3 AM.
- **Myth:** "Velero is enough for namespace restore — no need to test it."
  **Truth:** Untested Velero is fiction. Restore drills find: missing snapshot config, expired credentials, schema mismatches between Velero versions, missing Custom Resources, workloads that don't reconcile cleanly post-restore. Test quarterly.
- **Myth:** "Apiserver wedged → reboot the node."
  **Truth:** If kube-apiserver static pod is failing, rebooting just makes it fail again. Diagnose by reading the static-pod manifest + kubelet logs + the apiserver container logs. Fix the manifest; kubelet will restart the static pod automatically.

## Recap

Seven disasters every self-managed K8s operator should drill: cert expiry, broken CNI, broken CoreDNS, apiserver down, etcd quorum loss, webhook lockout, namespace delete + Velero restore. Quarterly tournament; runbooks updated each cycle.

**Next — V11: Capstone.** Build, harden, back up, upgrade, and recover an HA on-prem cluster on Talos with Cilium + Gateway API + cert-manager + Velero + kube-prometheus-stack + Argo CD. End-to-end project tying every module together.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
