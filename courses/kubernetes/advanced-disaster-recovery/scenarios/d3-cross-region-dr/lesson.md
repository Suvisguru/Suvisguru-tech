# K-ADV-DR D3 — D3 · Cross-Region DR + RPO / RTO + Restore Testing

> Course: K-ADV-DR (advanced specialization)
> Module D3 · Cross-Region DR
> Companion preview: `/preview-kubernetes-adv-dr-lesson-03.html`.

---

**🎯 If you remember nothing else:** **Pick DR shape: active-active / active-passive / warm-standby. Per-tier RPO + RTO. Quarterly restore-test mandatory. Untested backup is hope, not plan.**

## 1. active-passive · active-active · warm-standby

**Active-passive**: primary serves; DR cluster cold (cluster doesn't exist or scaled-to-zero). Cheapest. RTO 30-60 min (cluster IaC + GitOps + restore). Use for cost-sensitive non-critical workloads.
    **Active-active**: both regions serve via global LB; cross-region replication of state. RTO < 60s; RPO seconds-minutes. Most expensive. Use for tier-1 critical.
    **Warm standby**: DR cluster runs; minimal capacity; scale on disaster. RTO 5-10 min. Middle ground. Use for tier-2 important.

## 2. Define + publish + measure

Define per-tier RPO + RTO commitments:
    
      - **Tier-1 (gold)**: RPO < 5 min; RTO < 5 min. Active-active.

      - **Tier-2 (silver)**: RPO < 1h; RTO < 30 min. Warm standby.

      - **Tier-3 (bronze)**: RPO < 24h; RTO < 4h. Active-passive.

    
    Publish to tenants; tenants choose tier; cost varies. Quarterly drill measures actual; gap drives engineering.

## 3. "Backup completed" ≠ "restorable"

**Backup validation** beyond "job succeeded":
    
      - **Bit-rot check**: re-read backup; verify checksums. Detect storage corruption.

      - **Test-restore**: scheduled restore to non-prod cluster; validate apps come up.

      - **Synthetic transactions**: post-restore, run synthetic queries; compare to pre-backup state.

      - **Time-bounded**: restore must complete within RTO; alarm if exceeded.

    
    Tools: Velero schedules + cron-job test-restore + Datadog / Prometheus monitoring of restore-time.

## 4. Quarterly minimum; drive RTO improvement

**Quarterly restore-test**: per critical cluster, full rebuild to non-prod. Measure: time per phase (cluster + GitOps + Velero + DNS); identify bottlenecks; engineer fixes.
    **Per-namespace test**: monthly; faster + smaller-scope; catches per-namespace drift.
    **Tabletop drill**: paper-walk through scenarios ("region X down + DR region Y partially degraded"); identify gaps in runbook before real exercise.
    **Cadence**: quarterly full + monthly per-namespace + semi-annual tabletop. Continuous improvement.

## Before / After

**Before.** Pre-tested-DR: backups configured; nobody restored; RPO + RTO unmeasured; assumed "it'll work." Real outage = chaos.

**After.** Tested DR: per-tier RPO + RTO; quarterly drill measures; engineering fixes gaps. Real outage = bounded recovery.

*Untested backup = hope. Quarterly drill = plan.*

## Analogy — the K-Lifeboat cell

Mirror-Ship Harbor: a sister harbor in another region, mirroring the primary. Three operating shapes: **both harbors active** (active-active; ships dock either); **cold mirror** (active-passive; mirror dormant); **warm mirror** (warm-standby; mirror has minimal crew). Drill Master tests the failover quarterly + measures RTO.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Both harbors active | active-active (global LB + cross-region replication) |
| Cold mirror | active-passive (DR cluster off; rebuild on disaster) |
| Warm mirror | warm standby (DR cluster runs; minimal capacity) |
| Per-tier mirror commitments | RPO + RTO per tier |
| Backup-rehydration drill | Restore-test |
| Tabletop drill | Paper-walk through scenarios |

⚠️ *Analogy stops here:* A real harbor is fixed; cluster regions are virtual. Cross-region replication has cloud-specific gotchas (data egress cost; latency).

## ELI5 / ELI10

**ELI5.** Sister harbor across the bay. Sometimes both work; sometimes the sister is dormant. Practice the failover every quarter so it's fast when needed.

**ELI10.** **DR shapes**: active-active / warm-standby / active-passive. **RPO** = data loss window; **RTO** = recovery time. Per-tier commitments published. **Backup validation**: bit-rot + test-restore + synthetic transactions. **Restore-testing**: quarterly full + monthly per-namespace + semi-annual tabletop.

## Real-world scenarios

- **Active-active for tier-1 fintech.** Fintech runs payment processing across us-east-1 + us-west-2 active-active; cross-region DB replication (Aurora Global / Spanner); global LB routes; failover < 60s on region degradation. RTO requirement met.
- **Warm-standby for tier-2 SaaS.** SaaS runs primary in us-east-1; DR cluster in us-west-2 minimal-capacity; on disaster, scale + activate. RTO 8 min; cost ~30% premium over single-region. Acceptable for tier-2.
- **Quarterly drill caught Velero version skew.** Drill: backup taken on Velero v1.10; new cluster ran v1.13; restore failed schema mismatch. Postmortem: pin Velero version + auto-upgrade in IaC; runbook updated.
- **Outage — untested DR.** Pre-drill, DR plan was paper. Real outage: 12-hour recovery (vs target 4h). Postmortem: quarterly drills mandated; staffed.

## Common misconceptions

- **Myth:** "Active-active is always best."
  **Truth:** Cost premium is high (~2× capacity + cross-region traffic). Use only for tier-1 critical. Most workloads suit warm-standby or active-passive.
- **Myth:** "Backup success metric is enough."
  **Truth:** Backup that completes ≠ backup that restores. Test-restore quarterly to verify.
- **Myth:** "Cross-region DR works automatically with managed K8s."
  **Truth:** EKS / GKE / AKS = managed control plane; you still own cross-region cluster + state replication strategy. Not automatic; deliberate engineering required.

## Recap

Cross-region DR shapes: active-active / warm-standby / active-passive. Per-tier RPO + RTO. Backup validation. Quarterly restore-test mandatory.

**Next — D4: Secret recovery + DNS failover + stateful workload DR + managed-service DR limits.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
