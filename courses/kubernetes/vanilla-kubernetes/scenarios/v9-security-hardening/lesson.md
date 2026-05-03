# K-VAN V9 — V9 · Security Hardening (CIS, RBAC, PSA, supply-chain, runtime)

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V9 · Security Hardening
> Companion preview: `/preview-kubernetes-vanilla-lesson-09.html`.

---

**🎯 If you remember nothing else:** Hardening posture: **CIS Kubernetes Benchmark** (kube-bench scores), **NSA/CISA K8s hardening guide**. Tactical layers: **API server** (anonymous-auth=false, audit, encryption-at-rest, admission), **RBAC least privilege** (no default-SA grants), **PSA** (restricted profile baseline), **NetworkPolicy** (default-deny), **supply chain** (cosign + SBOM + verifyImages), **runtime** (Falco / Tetragon), **certificate rotation** (cert-manager + auto-renewal), **break-glass admin** (time-bounded + audited).

## 1. Why hardening is its own module

kubeadm + V6 cluster config get you to "working with sensible defaults." Hardening pushes you to "defensible against a determined attacker." The two are not the same. Self-managed clusters need explicit posture work because nothing else is doing it for you.
    Hardening for K8s has a clear playbook: the **CIS Kubernetes Benchmark** (community-curated checklist with kube-bench tooling), supplemented by the **NSA/CISA Kubernetes Hardening Guidance** (more recent, prescriptive). Together they cover ~120 controls across API server, etcd, kubelet, node OS, network, RBAC, audit, supply chain.

## 2. What to harden, in priority order

- **API server**: `--anonymous-auth=false`, audit policy enabled (V6), encryption-at-rest with KMS v2 (V6), admission plugins enabled (NodeRestriction, PodSecurity, ResourceQuota, LimitRanger), private API endpoint where possible, certificate rotation.

      - **etcd**: client + peer cert auth, encryption-at-rest (cluster-wide), no anonymous client access, dedicated network segment.

      - **kubelet**: anonymous auth off, authorization mode `Webhook`, serving cert rotation enabled (V6), no `--read-only-port`.

      - **Node OS**: CIS-style baseline (Ubuntu CIS, RHEL CIS), SELinux/AppArmor enforcing, auditd shipping logs, SSH keys-only + bastion, no root login, automatic security patches scheduled.

      - **RBAC**: least privilege, no default-SA grants, audit ClusterRoleBindings to `cluster-admin` quarterly, OIDC for humans (no shared kubeconfigs).

      - **Workload security**: PSA `restricted` on production namespaces (V6 + L31 of K-COM), NetworkPolicy default-deny (L17/L26 of K-COM), AdminNetworkPolicy for cluster-wide rules.

      - **Supply chain + runtime**: cosign image signing + verifyImages admission policy (L30 of K-COM), SBOMs available, Falco/Tetragon for runtime detection.

## 3. kube-bench + reporting

`kube-bench` (Aqua) runs CIS Benchmark checks against a cluster. Run as a Job:
    `kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs -l job-name=kube-bench

# Output: per-control PASS / FAIL / WARN with remediation guidance
# Example: 1.2.6 Ensure that the --kubelet-https argument is set to true (PASS)
# Example: 5.7.3 Apply Security Context to Your Pods and Containers (FAIL)`
    Run weekly via CronJob; ship report to a SIEM or PolicyReport CRD. Track score over time as a metric. Investigate every regression.
    For managed K8s components (EKS / GKE / AKS), kube-bench has provider-specific profiles — pick the right one to avoid false alarms on cloud-managed components. For vanilla self-managed: standard profile applies.

## 4. When the regular path won't do

**Break-glass admin**: occasionally you need cluster-admin to debug a P0. Best practice:
    
      - A separate auth path: not the daily SSO; a hardware key + emergency-only credentials.

      - Time-bounded: short TTL on the credential. Auto-expire.

      - Audited: every break-glass use logs to an out-of-band channel that on-call sees + reviews next day.

      - Documented: when to use, who can authorise, what to do after.

    
    **Ongoing posture**: hardening is a daily practice, not a one-time event.
    
      - kube-bench weekly + dashboard.

      - Vulnerability scanning (Trivy / Grype on container images, weekly + on every build).

      - Patch management (V8 cadence + monthly OS patches).

      - Backup encryption + off-site replication (Velero with KMS).

      - Compliance evidence: PolicyReports, audit log retention, change-control records — quarterly review with security team.

    
    [ deep dive — skip if new ]For FIPS / FedRAMP / regulated environments: RKE2 ships FIPS-validated binaries; Talos has a FIPS edition; OpenShift and other commercial distros have their own paths. Vanilla kubeadm does not provide a FIPS posture out of the box; pick a distro that does if compliance demands it.

## Before / After

**Before.** Anonymous auth on. Default SA grants. PSA at `privileged`. No image verification. No runtime detection. Compliance reports are wiki entries. Audit findings dozens deep.

**After.** kube-bench in CI; score > 95%. RBAC reviewed quarterly via `rakkess`. PSA `restricted` baseline. Cosign verifies images at admission. Falco shipping events to SIEM. Break-glass tested + auditable. Compliance evidence is queries against PolicyReports.

Hardening is layered + ongoing. Each layer alone is partial; the stack makes the cluster defensible.

## Analogy — the K-Frontier site

The Watchtower stands at the perimeter of the homestead. The fence (NetworkPolicy + admission) keeps casual intruders out. The watchman in the tower (Falco / Tetragon) sees what's actually happening inside. The night patrol (kube-bench, weekly) checks that locks are still in place. The deed-of-trust drawer (audit logs) records who entered + what they did. And tucked in a sealed envelope at the back of the tower: the break-glass key, time-stamped, used only when the regular gates are locked + something's on fire.

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| Fence around the homestead | NetworkPolicy + AdminNetworkPolicy default-deny |
| Locked gates with posted rules | API server + admission policies (PSA, VAP, Kyverno) |
| Watchman in the tower | Falco / Tetragon runtime monitoring |
| Night patrol checking locks | kube-bench weekly CIS scan |
| Deed-of-trust drawer | Audit log + EncryptionConfiguration |
| Notarised package receipts | Cosign signature + SBOM verification |
| Sealed break-glass envelope | Time-bounded admin credential; audited |
| Yearly fence inspection | Quarterly RBAC + posture review |

⚠️ *Analogy stops here:* The analogy stops here: real security is layered defense, not a single fence. A single misconfigured RBAC binding bypasses every other control. The watchman + the fence + the locks + the audits all matter; one alone is fiction.

## ELI5 / ELI10

**ELI5.** Build a fence, post a watchman, lock the doors, write down who comes in. Once a week the patrol checks the locks. Always have a backup key for emergencies — but only one person knows where it is, and using it sets off an alarm.

**ELI10.** Hardening = posture work after install. Run kube-bench weekly (CIS Benchmark); track score. Layers: apiserver (audit + encryption + admission), etcd (cert auth, no anonymous), kubelet (no anonymous, no read-only port, serving cert rotation), node OS (CIS baseline, SELinux/AppArmor, auditd), RBAC (least privilege; no default-SA grants), workload (PSA restricted + NetworkPolicy default-deny), supply chain (cosign + SBOM + verifyImages), runtime (Falco/Tetragon). Break-glass admin: separate path, time-bounded, audited.

## Real-world scenarios

- **A SaaS with kube-bench in CI.** Daily kube-bench job; output to PolicyReport CRD; Grafana dashboard on score over time. Alert if any Level 1 FAIL appears. Runbook for each control. Score consistently > 96%; remaining 4% are documented exceptions.
- **A bank running RKE2 for FIPS posture.** RKE2 with FIPS-validated binaries. CIS Level 2 baseline. Harvester for Talos-based hosts. CIS scan + SBOM scanning + Falco rules + cosign verifyImages. Auditor: "this is the cleanest cluster we've seen."
- **A team that audited 200 ClusterRoleBindings.** Year-end review used `rakkess` to enumerate every subject + permission. Found: 14 cluster-admin bindings nobody remembered, 8 SAs with secrets read access cluster-wide, 3 group bindings for old projects. Cleanup PR removed 18 of them. Annual cadence now built into compliance reviews.
- **A startup with break-glass tested quarterly.** 1Password vault holds emergency credential. SSO break-glass procedure documented. Quarterly test: someone uses break-glass for a planned operation (e.g., bumping etcd quota); on-call gets the alert; team reviews after. Avoids "we have it but never used it" failure mode.

## Common misconceptions

- **Myth:** "PSA Restricted is too strict for production."
  **Truth:** Restricted is the right baseline for nearly all application Pods. Specific workloads (CSI drivers, Falco, kube-proxy) need privileged; those go in their own namespaces with explicit privileged label. Most app namespaces should be restricted.
- **Myth:** "kube-bench is only for compliance teams."
  **Truth:** It's a continuous quality signal for engineering. New misconfiguration introduced by a change shows up as a new FAIL. Treat the score the way you treat unit-test coverage — own it.
- **Myth:** "Cosign verifyImages slows down deploys."
  **Truth:** < 100ms per Pod admission once cached. Negligible. The supply-chain assurance benefit is enormous; the latency cost isn't.

## Recap

Hardening is layered: apiserver / etcd / kubelet / node OS / RBAC / workload (PSA + NetworkPolicy) / supply chain / runtime. CIS Benchmark via kube-bench tracks the posture. Break-glass for emergencies. Quarterly review.

**Next — V10: Advanced Vanilla Troubleshooting.** When everything goes wrong: expired certs, broken CNI, broken CoreDNS, apiserver failure, etcd failure, webhook-blocked apiserver. Drill the disasters before they happen.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
