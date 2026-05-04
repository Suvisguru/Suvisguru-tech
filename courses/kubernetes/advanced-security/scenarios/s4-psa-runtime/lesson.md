# K-ADV-SEC S4 — S4 · PSA Restricted + Runtime Detection

> Course: K-ADV-SEC (advanced specialization)
> Module S4 · PSA + Runtime
> Companion preview: `/preview-kubernetes-adv-sec-lesson-04.html`.

---

**🎯 If you remember nothing else:** **PSA migration: privileged → baseline → restricted, namespace by namespace, audit → warn → enforce. Falco / Tetragon eBPF for runtime detection at scale. Admission stops misconfig; runtime stops escape attempts. Both layers are required for production-grade clusters.**

## 1. privileged, baseline, restricted

**privileged**: no restrictions. Use only for system namespaces (`kube-system`, monitoring agents needing host access). Default for legacy clusters.
    **baseline**: no `privileged` containers, no `hostPath`, no `hostNetwork` / `hostPID` / `hostIPC`, no `allowPrivilegeEscalation: true`, no `NET_RAW` capability. Stops the most common cluster-escape vectors. Should be the cluster's minimum bar.
    **restricted** (the strictest): everything from baseline + drop ALL capabilities (no `capabilities.add`), `runAsNonRoot: true`, `seccompProfile` required, `allowPrivilegeEscalation: false` explicitly. Recommended for all workloads that don't have a documented reason to be different.
    Each profile has three modes per namespace: **enforce** (block on violation), **audit** (record), **warn** (kubectl warning). Set via namespace labels: `pod-security.kubernetes.io/enforce: restricted`, `pod-security.kubernetes.io/warn: restricted`, etc.

## 2. privileged → baseline → restricted, namespace by namespace

Most existing clusters start at privileged for everything. The path:
    
      - **Audit cluster-wide**: `kube-no-trouble` / `kubescape` / `kyverno-pss-audit` finds Pods that would fail baseline + restricted.

      - **Pick canary namespaces**: dev / non-prod first; one namespace at a time; label with `warn: baseline` first.

      - **Fix offenders**: most are leftover from migration — privileged for no real reason, hostPath for ad-hoc debug. Remove the dependency or move to a privileged-allowed namespace.

      - **Promote enforce: baseline** per namespace.

      - **Repeat for restricted**: warn → enforce. Restricted often blocks workloads that ran as root; `runAsNonRoot` + image rebuilds with non-root user fix them.

      - **Cluster default**: once 80%+ of namespaces are restricted, set the cluster admission policy default to enforce-restricted; exempt the few legitimate privileged namespaces.

    
    Tools: **Kyverno PSS pack** (pre-built ClusterPolicies for each PSA profile + reporting); **Gatekeeper PSS** (Constraint templates); **kyverno-pss-audit** for migration prep.

## 3. eBPF syscall watch + alert pipeline

**Falco** (CNCF Graduated): rules engine over Linux syscalls + K8s audit + container events. Default rules detect shell-in-container, write-to-etc, sensitive-mount, network-anomaly. Emit alerts via gRPC / Webhook / Kafka / Slack. Battle-tested; large rule library; works on most kernels.
    **Tetragon** (Cilium project): eBPF-native, kernel-level. Lower overhead than Falco for high-cardinality monitoring. Can *also enforce* at runtime — kill processes, block syscalls — not just observe. More powerful + newer; learning curve is the trade-off.
    Pick: Falco for breadth + ecosystem + rule library; Tetragon for kernel-level performance + enforcement use cases. Many clusters run both — Falco for general detection, Tetragon for high-rps namespaces.
    **Common rules to enable**: shell spawned in container; mount() inside container; write to /etc, /bin, /sbin; outbound network connection to unexpected CIDR; ptrace inside container; capability NET_RAW used; suspicious process tree (e.g., crypto-miner names).

## 4. From eBPF event to on-call action

Runtime detection without a tuned pipeline is noise. Build the pipeline:
    
      - **Aggregate**: Falco / Tetragon emit events; route to Falcosidekick / Fluent Bit / Vector → SIEM (Loki, Splunk, OpenSearch).

      - **Suppress noise**: tune rules to your environment. "Shell in container" fires for legitimate `kubectl exec` debug; suppress when source = on-call group + window.

      - **Correlate**: an alert on a Pod gets joined with the Pod's namespace + service + recent admission events. SIEM correlation rules surface multi-signal incidents.

      - **Tier severity**: critical (immediate page) — escape-style rules. Warning (Slack) — informational rules. Info (log only) — audit-trail rules.

      - **Auto-response** (Tetragon enforce mode): kill process / block syscall on critical rules. Reserve for well-tested rules; over-aggressive auto-kill = self-DoS.

    
    The mature pattern: alert tier 1-3 + named runbooks; quarterly red-team exercise to verify alerts fire + on-call responds in budget.

## Before / After

**Before.** Pre-PSA / pre-runtime, clusters ran with no Pod-security gates and no syscall observability. Privileged Pods slipped in unnoticed; container escapes were undetectable; compromised workloads moved laterally without alerting. Compliance evidence relied on YAML inspection samples.

**After.** Modern clusters enforce PSA Restricted on every workload-namespace by default; runtime detection (Falco / Tetragon) attaches eBPF probes for escape attempts; alerts route through SIEM with severity tiers + runbooks. Two layers, complementary failure modes; compliance evidence is automatic + queryable.

*Admission stops 90% of misconfig at submit; runtime catches the rest + the live attacks. Skip either layer and the cluster has a blind spot.*

## Analogy — the K-Citadel bastion

The Mandatory-Helmet Zones mark every quarter of the citadel where standard kit must be worn. The **privileged area** is the staff-only zone (kube-system) where workers carry tools that would be dangerous outside it. The **baseline area** requires basic helmets — no spiked clubs, no climbing the walls, no reaching outside the citadel for tools. The **restricted area** requires full kit — gloves, lockable boots, sealed gauntlets — drop ALL extra capabilities, run as a non-elevated visitor.
    Beyond the helmet check, the citadel's walls have **silent observers** (Falco / Tetragon eBPF probes) watching every gesture inside. They alert on motions that pass the gate but are suspicious in the room — opening a sealed crate (mount), shouting outside the building (unexpected network), wandering toward the keep (privilege escalation).
    The migration is gradual: walk every quarter, find which workers don't fit the new kit, fix or exempt them, then enforce. Quarter by quarter the entire citadel goes restricted.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Staff-only zone (tools allowed) | PSA privileged profile (kube-system, system agents) |
| Basic helmet zone | PSA baseline (no privileged / hostPath / hostNet) |
| Full kit zone | PSA restricted (drop ALL caps + runAsNonRoot + seccomp) |
| Helmet inspector at every door | Pod Security Admission webhook |
| Three inspection modes | audit / warn / enforce per profile per namespace |
| Silent observers in every room | Falco / Tetragon eBPF probes |
| Suspicious motion alarm | Falco rule (shell-in-container, mount, write-to-etc) |
| Real-time alarm-and-block | Tetragon enforcement mode (kill / block syscall) |
| Gradual quarter-by-quarter sweep | Namespace-by-namespace PSA migration |

⚠️ *Analogy stops here:* A real helmet-zone is visible; PSA + runtime are policy + kernel-level — invisible until tested. Game-day exercises (deliberately deploy a privileged Pod or run a shell inside) are how you verify the controls fire.

## ELI5 / ELI10

**ELI5.** Two safety officers at every quarter of the castle. The first checks at the door — no spikes, no climbing gear, no shouting outside. The second watches you inside — if you try to open a sealed crate or wander somewhere you shouldn't, an alarm rings. Your cluster has these two officers: PSA at admission, Falco / Tetragon at runtime.

**ELI10.** **PSA**: namespace-level enforcement via labels (`pod-security.kubernetes.io/enforce: restricted`). Three profiles (privileged / baseline / restricted) × three modes (audit / warn / enforce). **Migration**: privileged → baseline → restricted, namespace by namespace, audit then warn then enforce. **Falco**: eBPF syscall watch + rules engine; CNCF Graduated; large rule library. **Tetragon**: Cilium-native eBPF; lower overhead + can enforce (kill / block) not just observe. **Pipeline**: events → SIEM → tiered alerts → on-call runbooks.

## Real-world scenarios

- **Greenfield cluster — restricted from day one.** A new cluster ships with cluster-wide default `enforce: restricted`; `kube-system` + monitoring exempt to `privileged`. Workload teams write Pods that pass restricted from day one. Falco runs as DaemonSet; alerts route to Slack + PagerDuty. Day-1 security baseline is the cluster's baseline.
- **Brownfield migration — 90 namespaces, 18 months.** A 100-engineer org with 90 prod namespaces. Phase 1 (3 months): audit every namespace; build inventory of privileged Pods. Phase 2 (6 months): warn baseline cluster-wide; teams migrate offenders. Phase 3 (3 months): enforce baseline. Phase 4 (6 months): warn + enforce restricted. *18 months but every cluster ends restricted.*
- **Runtime catch — crypto-miner.** A compromised dev image silently launched a crypto-miner. Falco rule "unexpected outbound network to mining-pool CIDRs" fired within 5 minutes; on-call killed the Pod via runbook; root caused a vulnerable transitive dep. *PSA didn't catch it (the Pod spec was clean); runtime did.*
- **Outage — restricted enforced without runAsNonRoot fixes.** A team flipped enforce: restricted on a namespace whose images ran as root. Every Pod failed admission; Service down. Postmortem: should have run audit + warn for 4 weeks first; image rebuilds for non-root user; ship in waves. Runbook updated.

## Common misconceptions

- **Myth:** "PSA Restricted is enough; we don't need runtime detection."
  **Truth:** Admission validates the *spec* at submit time. A Pod that's spec-clean but exploits a kernel CVE for container escape passes admission and breaks out at runtime. PSA + runtime are complementary; neither alone catches the full failure surface.
- **Myth:** "Falco is too noisy; we tried it once and disabled it."
  **Truth:** Default Falco rules need tuning for any environment. *Suppression rules + severity tiers + named runbooks* turn Falco from noise into signal. Skip tuning and yes, it's noisy. Spend two weeks tuning and it's the lighthouse you've always wanted.
- **Myth:** "Tetragon replaces Falco."
  **Truth:** They overlap but solve subtly different things. **Falco** = mature, broad rule library, ecosystem of integrations. **Tetragon** = kernel-level eBPF, lower overhead, can enforce. Many clusters run both: Falco general-purpose, Tetragon for specific high-rps workloads or enforcement.

## Recap

Two complementary layers: PSA at admission, Falco / Tetragon at runtime. PSA migration is privileged → baseline → restricted, namespace by namespace, audit → warn → enforce. Runtime detection requires tuning + a real alert pipeline; without that it's noise.

**Next — S5: Image Signing + SBOM + SLSA + in-toto + VEX.** Cosign signing in CI; SLSA L3+ provenance attestation; SBOM (CycloneDX / SPDX); VEX vulnerability disposition; cluster-side admission verification.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
