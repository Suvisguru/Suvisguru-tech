# K-ADV-DR D5 — D5 · Capstone — Destroy + Rebuild Production Cluster

> Course: K-ADV-DR (advanced specialization)
> Module D5 · Capstone Total-Loss Drill
> Companion preview: `/preview-kubernetes-adv-dr-lesson-05.html`.

---

**🎯 If you remember nothing else:** **Total-loss drill: rebuild from Git + backups + OCI registry + Vault + DNS within RTO. Quarterly drill non-optional. The architecture isn't the work; the disciplined exercise is.**

## 1. Git + Velero + OCI + Vault + DNS

Total cluster loss recovery requires five sources outside the dead cluster:
    
      - **Git**: cluster IaC + GitOps source-of-truth for apps + ApplicationSets.

      - **Backups**: Velero (PVCs + Secrets + ConfigMaps) + DB snapshots (cross-region replicated).

      - **OCI registry**: container images + Cosign signatures + SBOMs + model artifacts.

      - **Secrets**: external Vault HA snapshot + KMS replicated keys.

      - **DNS**: Route 53 / managed DNS records + health-check failover.

    
    Each source is independent + survives cluster loss. Coordinate the timeline.

## 2. Numbered runbook; measured per phase

End-to-end runbook:
    
      - **Trigger**: cluster confirmed lost (or drill announced); on-call paged.

      - **Cluster IaC**: Terraform / Crossplane provisions new cluster; Argo CD installed (~10-15 min).

      - **GitOps sync**: Argo CD ApplicationSet picks up new cluster; CRDs (sync-wave -2) → operators (-1) → apps (0+) (~10 min).

      - **Vault snapshot restore**: rebuild Vault HA in new region (or DR region already running); ESO re-syncs secrets to new cluster (~5 min).

      - **Velero restore**: PVCs + Secrets + ConfigMaps from cross-region backup (~5 min).

      - **DB restore**: managed-DB cross-region promote + custom-DB restore from snapshot (~10 min).

      - **Validate**: SLO metrics return; tenant smoke tests pass (~5 min).

      - **DNS swap**: Route 53 record points at new ALB / global LB shifts traffic.

      - **Tenant communication**: status page update.

    
    **Total RTO target**: 30-60 min for managed K8s + warm DR pattern; longer for cold DR.

## 3. Quarterly + monthly + tabletop

Drill regimen:
    
      - **Quarterly full drill**: total cluster destruction in non-prod; full rebuild; measure end-to-end RTO.

      - **Monthly per-namespace test**: smaller-scope; catches drift between full drills.

      - **Semi-annual tabletop**: paper-walk through scenarios ("region down + DR partially degraded"); identify decision points.

      - **Per-incident postmortem**: real incidents drive runbook + automation improvements.

    
    Continuous improvement: every drill produces a runbook delta; every delta improves RTO; over years, RTO trends down.

## 4. DR engineering team + roles + budget

**DR engineering team**: 1-2 engineers focused on backup + restore tooling + drill orchestration. Reports to platform team.
    **Roles per drill**: *Drill Master* (designs scenario + coordinates), *On-call* (executes runbook), *Observer* (measures + records), *Tenant rep* (validates from tenant POV).
    **Budget**: drill cluster (non-prod) + cross-region storage + Vault HA + DNS health-check. Single biggest cost: cross-region data transfer.
    **Reporting**: per-quarter drill report to leadership: RTO measured + improvements made + outstanding gaps. **The architecture is the easy part; the disciplined exercise is the work.**

## Before / After

**Before.** Pre-disciplined-DR: total cluster loss = days of recovery; runbook in someone's head; first incident reveals gaps.

**After.** Disciplined DR: 5 sources + runbook + quarterly drill + measured RTO. Total cluster loss = 30-60 min recovery; SLA preserved.

*Discipline beats hope. Quarterly drill is non-optional.*

## Analogy — the K-Lifeboat cell

Total-Loss Drill: simulate (or live through) the loss of an entire ship + its harbor. The Drill Master shows the rebuild from five outside sources: blueprints (Git), cargo backups (Velero + DB), warehouse (OCI registry), vault (Vault + KMS), routing tower (DNS). The Captain runs the drill quarterly. Real loss = drill in production with adrenaline.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Five outside sources | Git + Velero + OCI registry + Vault + DNS |
| Drill Master | DR architect / lead engineer |
| On-call executor | On-call engineer following runbook |
| Observer / scribe | Records timing + gaps |
| Tenant rep | Validates from tenant POV |
| Quarterly full drill | Total cluster destroy + rebuild |
| Tabletop drill | Paper-walk scenarios |
| RTO measured + improved | End-to-end recovery time per quarter |

⚠️ *Analogy stops here:* A real fleet exercise has fixed assets; cluster + cloud + region setup change. Re-validate runbook after major architecture shifts.

## ELI5 / ELI10

**ELI5.** Practice losing the whole castle quarterly so you're ready when it happens for real. Five things outside the castle are needed: blueprints, cargo backups, warehouse, vault, signal tower.

**ELI10.** **Five sources**: Git + Velero + OCI registry + Vault + DNS. **Runbook**: cluster IaC → GitOps sync (sync waves) → Vault restore → Velero restore → DB restore → validate → DNS swap. **Drill cadence**: quarterly full + monthly per-namespace + semi-annual tabletop. **Roles**: Drill Master + on-call + observer + tenant rep. **Operational rhythm**: continuous improvement.

## Real-world scenarios

- **Quarterly drill — 28-min RTO.** Q3 drill: simulated us-east-1 cluster loss; rebuild followed runbook; measured 28-min end-to-end (vs 30-min target). One gap: Velero parallel restore tuning. Fixed before Q4 drill.
- **Real incident — runbook saved the day.** Bad upgrade corrupted prod cluster; on-call followed Q3-drilled runbook; rebuild in 32 min; tenants notified via status page; SLA preserved.
- **Tabletop caught decision-point gap.** Tabletop scenario: "primary region down + DR region partially degraded" — runbook didn't cover. Postmortem: added decision tree (route to which DR region); next drill clean.
- **Outage — drill skipped for a quarter.** Skipped Q2 drill due to launches. Q3 real incident; runbook had drift; recovery took 4h instead of 1h. Postmortem: drills are non-optional; protected calendar.

## Common misconceptions

- **Myth:** "Backups + GitOps means we don't need drills."
  **Truth:** Untested = unverified. Drills find gaps that backup-success metrics don't — schema drift, secret rotation, DNS TTL, runbook ambiguity.
- **Myth:** "Quarterly is too frequent."
  **Truth:** Less than quarterly = drift accumulates invisibly. Real loss reveals it; drill finds it on a calm day.
- **Myth:** "DR is for very large orgs."
  **Truth:** Even small orgs lose clusters (cloud incident; bad upgrade; human error). RTO commitment varies by org but every cluster benefits from tested DR.

## Recap

Total-loss drill: rebuild from Git + Velero + OCI + Vault + DNS within RTO. Quarterly + monthly + tabletop. Measured per-phase. Continuous improvement. The disciplined exercise is the work.

**K-ADV-DR complete.** 5 modules. From etcd backup (D1) to total-loss drill (D5). **K-ADV family complete**: K-ADV-SEC + K-ADV-NET + K-ADV-PE + K-ADV-AI + K-ADV-DR — 36 advanced modules across 5 specializations.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
