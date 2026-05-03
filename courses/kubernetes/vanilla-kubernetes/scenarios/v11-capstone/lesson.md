# K-VAN V11 — V11 · Capstone — Build, Harden, Back Up, Upgrade, Recover an HA Cluster

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V11 · Capstone
> Companion preview: `/preview-kubernetes-vanilla-lesson-11.html`.

---

**🎯 If you remember nothing else:** **Capstone deliverables**: (1) Working 6-node HA cluster on Talos with the reference stack. (2) Git repo (Argo CD App-of-Apps) reproducing the cluster from scratch. (3) etcd snapshot + Velero backup tested. (4) Documented upgrade rehearsal runbook. (5) Documented DR runbook covering all 7 disasters from V10. (6) kube-bench score > 95%. **You're K-VAN-complete when you can teach someone else to do it.**

## 1. What "capstone" means here

K-VAN is 10 modules of how. The capstone is one module of *do*: a single end-to-end project that exercises every prior module in sequence. You'll come out the other side with a working cluster you can defend in an interview, a runbook library, and the muscle memory to do it again on another network.
    The reference stack is opinionated to keep the project tractable: Talos (immutable OS, no SSH, fast bootstrap), Cilium (modern CNI), Gateway API (the future of ingress), cert-manager (TLS), Velero (backup), kube-prometheus-stack (monitoring), Argo CD (GitOps). You can sub equivalents if your environment demands it (RKE2 instead of Talos, Calico instead of Cilium) — the modules will still apply.

## 2. V1-V4 in sequence

**A.1 Architecture document** (V1). One page covering: 6 nodes (3 CP + 3 worker), Talos OS, Cilium CNI, stacked etcd, Pod CIDR `192.168.224.0/20`, Service CIDR `10.96.0.0/12`, kube-vip for API LB at 192.168.1.100, Longhorn CSI, Velero backup to S3, Argo CD GitOps, kube-bench scoring target ≥ 95%. Commit to git as `docs/architecture.md`.
    **A.2 Provision 6 VMs** with Talos image + machine-config (V2 collapses to applying the config). Each node's machine-config sets kernel modules, sysctl, runtime, swap-off — all baked into the OS image. `talosctl apply-config` on each.
    **A.3 Bootstrap the cluster** (V3 via Talos, not kubeadm): `talosctl bootstrap --nodes <cp-1-ip>` on the first CP node; the others auto-join via the machine-config. kube-vip runs as a Talos extension or a static pod. Cluster comes up in 2-3 minutes.
    **A.4 Install Cilium** (V4): Helm install with `kubeProxyReplacement=true`, native routing, Hubble enabled, MTU verified. `cilium connectivity test` passes.
    Verify: `kubectl get nodes` all 6 Ready.

## 3. V5, V6, V9 in sequence

**B.1 Bootstrap Argo CD**: helm install argocd; create the App-of-Apps root pointing at `k8s-platform/apps/` in the git repo. Argo CD installs:
    
      - cert-manager + ClusterIssuer (Let's Encrypt staging for the lab)

      - Cilium Gateway controller (already part of Cilium, register Gateway API CRDs)

      - Longhorn CSI + snapshot-controller

      - Velero with the Longhorn snapshot plugin + S3 (or MinIO) target

      - kube-prometheus-stack with Grafana exposed via Gateway

      - Loki + Vector for logs

      - Kyverno (policies) + Falco (runtime)

      - kube-bench as a daily CronJob, output to PolicyReport

    
    **B.2 Cluster config** (V6): apply your kubeadm/Talos cluster config additions: audit log on, KMS v2 encryption with Vault Transit (or static AES for the lab), systemReserved + kubeReserved on every node, scheduler bin-pack profile available, RuntimeClass for kata.
    **B.3 Hardening** (V9): label every namespace with `pod-security.kubernetes.io/enforce: restricted` (or baseline). Apply default-deny BANP. Apply Kyverno verifyImages policy in audit mode (move to enforce after a soak). Run kube-bench; investigate FAILs; aim for ≥ 95% Level 1 PASS.

## 4. V7, V8, V10 in sequence + writeup

**C.1 etcd snapshots** (V7): Talos has a built-in etcd-snapshot path; configure machine-config to snapshot every 30 min and ship to S3. Verify with `talosctl etcd snapshot save`.
    **C.2 Velero backup**: schedule `nightly` at 02:00; include all namespaces; include PV snapshots; retain 30 days.
    **C.3 Upgrade rehearsal** (V8): plan an upgrade from current Talos / K8s minor → next. On the staging clone (or a Vagrant lab): apply the upgrade. Document what broke + what to do differently. Output: `docs/runbooks/upgrade-vX-to-vY.md`.
    **C.4 DR drills** (V10): run all seven scenarios from V10 on the staging cluster. Document each recovery in a separate runbook file. Output: `docs/runbooks/dr-{cert-expiry,cni-broken,coredns,apiserver-down,etcd-quorum,webhook-lockout,namespace-restore}.md`.
    **C.5 Final review**: walk a colleague through the architecture doc, the git repo, the runbooks, kube-bench score. They should be able to reproduce the cluster from scratch using your artifacts. **That's the K-VAN bar**.
    [ deep dive — skip if new ]If you have time + capacity: build the cluster on real hardware (3 NUCs + 3 mini-PCs, ~$3K total). Operating physical infra adds the rack, power, network, BMC, console-server experience that VMs hide. Worth doing once for the muscle memory.

## Before / After

**Before.** You finished K-COM and read all 10 K-VAN modules. You haven't built end-to-end. There's a gap between knowing and doing — and you only find it when something breaks under pressure.

**After.** You've built the reference cluster. You've broken it on purpose and recovered each disaster. Your git repo + runbooks let a colleague reproduce the work in a day. You can defend any choice in an interview. **K-VAN-complete**.

The capstone exists so the gap between knowing and doing is closed deliberately, not by surprise in production.

## Analogy — the K-Frontier site

The Complete Homestead is the eleventh and final site on the K-Frontier map. The Drafting Hut produced the blueprint; the Land Clearing prepared the ground; the Frame went up; the Wiring went in; the Outbuildings clustered around the main house; the Rules Board was posted; the Well was drilled deep; the Renovation routine was practiced; the Watchtower was staffed; the Drill Square saw quarterly fires controlled. Now you stand in front of the gate, the deed in one hand, the keys in the other. The plaque on the post lists the stack. Inside the house: the runbook library, the architecture doc, the kube-bench scorecard. You can defend it to the inspector. You can leave it to the next homesteader. **That's K-VAN complete**.

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| The full deed of the homestead | Architecture document in git |
| The keys to every outbuilding | kubeconfig + RBAC bindings |
| Plaque on the post | Cluster bill of materials (versions, components) |
| Library of runbooks | docs/runbooks/ in git |
| Drill scoreboard on the wall | kube-bench Grafana dashboard |
| Backup well drilled + tested | etcd snapshots + Velero + DR drill |
| Renovation calendar pinned to the door | Quarterly upgrade cadence |
| Sealed envelope: emergency keys | Break-glass admin procedure |
| Property survey + inspector approval | kube-bench score + audit log review |

⚠️ *Analogy stops here:* The analogy stops here: the homestead is a one-time build; clusters are continuously evolving. K-VAN-complete means "you can build + operate + defend" — not "you're done forever." The next K8s minor is always coming.

## ELI5 / ELI10

**ELI5.** You've been learning to build a house the hard way. Now you build the whole house, lock it down, set up the alarms, write down what to do in a fire — and prove someone else could do it from your notes.

**ELI10.** Capstone: build a working 6-node HA cluster end-to-end on Talos + Cilium + Gateway API + cert-manager + Velero + kube-prometheus-stack + Argo CD, hardened to kube-bench > 95%. Phase A: architecture doc + Talos bootstrap + Cilium. Phase B: Argo CD App-of-Apps for all add-ons + cluster config + PSA + Kyverno + Falco. Phase C: etcd snapshots + Velero + upgrade rehearsal + 7 DR runbooks. Final review: a colleague can reproduce from your artifacts. K-VAN-complete.

## Real-world scenarios

- **A team finishing K-VAN as their pre-prod milestone.** 6 weeks of dedicated time. Vagrant + libvirt for local dev cluster; bare-metal NUCs for a real cluster. Final demo: chaos-day on the lab cluster recovering all 7 V10 scenarios in front of the team. Clear "we can do this in production" signal.
- **A bank using K-VAN graduates as the SRE pool.** Anyone running the production K8s clusters has finished K-VAN. Demonstrates: built the reference cluster, scored kube-bench > 95%, written the DR runbooks, walked a peer through. New hires onboarded by working through K-VAN with a buddy. Operational quality is hire-time + ongoing.
- **A startup choosing K-VAN over an EKS cert.** Engineering manager: certifications validate trivia; K-VAN validates the work. New SRE candidates pair on the Talos build + Cilium install + Velero restore drill. The artifact (git repo + runbooks) is the interview portfolio.
- **An open-source contributor giving back.** Used K-VAN to build their first self-managed cluster. Wrote a blog post documenting deviations (Calico instead of Cilium for FIPS reasons). PR'd a typo fix in the K-VAN module. Cycle complete.

## Common misconceptions

- **Myth:** "The capstone is optional / nice-to-have."
  **Truth:** K-VAN-complete means built end-to-end. Reading the modules without doing the capstone is K-VAN-read, not K-VAN-done. Different skill level.
- **Myth:** "You need real hardware to do K-VAN properly."
  **Truth:** VMs work fine for the curriculum. Real hardware adds depth (BMC, network, console) but isn't required. If you have access to a few NUCs or rack space, take it; otherwise VMs.
- **Myth:** "You can skip the runbooks if everything works."
  **Truth:** The runbooks ARE the deliverable. Working cluster without runbooks = you can't hand it off + you can't recover under pressure. Write them as you go, not after.

## Recap

Capstone = build the reference stack end-to-end + harden + back up + upgrade + DR-drill all 7 scenarios + produce runbooks. Working cluster + git repo + runbooks + defended decisions + reproduced by a peer = K-VAN-complete.

**Done.** You've walked the K-Frontier homestead from raw land to defendable property. K-VAN ends here; what comes next is operating real clusters with the muscle memory you built. The Drafting Hut on the next site is yours to design.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
