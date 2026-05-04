# K-ADV-DR D2 — D2 · GitOps-Driven Recovery + Cluster Rebuild

> Course: K-ADV-DR (advanced specialization)
> Module D2 · GitOps Recovery
> Companion preview: `/preview-kubernetes-adv-dr-lesson-02.html`.

---

**🎯 If you remember nothing else:** **Recovery order: cluster IaC → CRDs → operators → apps (GitOps) → Velero restore. Tested via quarterly drill. RTO < 30 min for well-built systems.**

## 1. Terraform / Crossplane / Pulumi

Cluster itself is rebuildable from IaC. Terraform / Crossplane / Pulumi declares: control plane (managed K8s service) + node pools + IAM + networking + DNS.
    Rebuild time: 5-15 min on managed K8s; 30-60 min on self-managed (etcd restore + control-plane bootstrap). Cluster name + cloud account + region preserved (or new region for disaster).
    Pre-prep: IaC tested + drill-rebuilt quarterly to non-prod; runbook updated.

## 2. Argo CD / Flux re-creates everything

Once cluster is up: install **Argo CD** / **Flux** (one Helm chart). Argo CD reads Git; reconciles all Apps. Within 5-10 min, all workloads spawn.
    **Sync waves** matter: CRDs first (sync wave -2), operators (sync wave -1), apps (sync wave 0+). Without ordering, apps fail because their CRDs don't exist yet.
    ApplicationSet generators replicate fleet-wide; new cluster picks up automatically.

## 3. PVCs + Secrets + ConfigMaps

**Velero restore** per backup. Restore order: per-namespace; high-priority first (databases / auth services); low-priority later. `velero restore create --from-backup <name>`.
    **Mapping**: `--namespace-mappings` if restoring to a different namespace; `--include-resources` to limit scope.
    External services (RDS / Vault) restore separately via their own DR procedures. Coordinate the timeline.

## 4. Tested quarterly; RTO measured

**Runbook**: numbered steps; per cluster shape; tested. Common skeleton:
    
      - Provision cluster via Terraform / Crossplane (~5-15 min).

      - Install Argo CD / Flux (~2 min).

      - Argo CD syncs CRDs + operators (sync wave) (~5 min).

      - Argo CD syncs apps (~5 min).

      - Velero restore PVCs + Secrets + ConfigMaps (~5 min).

      - Validate: SLO metrics return.

      - DNS swap to new cluster (Route 53 / Azure DNS).

      - Tenant communications.

    
    **Quarterly drill**: full rebuild to non-prod; measure RTO; update runbook. Find issues before real loss.

## Before / After

**Before.** Pre-GitOps recovery: total cluster loss = days of manual rebuild from notes + memory + Slack scrollback. RTO measured in days.

**After.** GitOps + IaC + Velero: cluster IaC + GitOps sync + Velero restore. RTO < 30 min for well-built systems. Runbook + drill mandatory.

*Cluster as cattle, not pet. Rebuildable in minutes from Git + backups.*

## Analogy — the K-Lifeboat cell

Ship Rebuild Yard: when a ship is lost, the yard rebuilds from blueprints (IaC) + cargo manifests (Git) + cargo backups (Velero). The Drill Master practices quarterly so the rebuild flows in < 30 min.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Ship blueprints | Terraform / Crossplane / Pulumi |
| Cargo manifests | Git source-of-truth (apps + config) |
| Cargo backup vaults | Velero backup of PVCs + Secrets |
| Yard rebuild order | cluster → CRDs → operators → apps → data restore |
| Sync wave priority | argocd.argoproj.io/sync-wave annotation |
| Drill Master | DR engineer / on-call |

⚠️ *Analogy stops here:* A real ship is physical; cluster is config + state. Backups + IaC = rebuildable; verify quarterly.

## ELI5 / ELI10

**ELI5.** When a ship is lost, the yard rebuilds from blueprints + cargo lists + cargo backups. Practice every quarter so the rebuild is fast.

**ELI10.** **Cluster IaC** (Terraform / Crossplane / Pulumi) → **GitOps sync** (Argo CD / Flux with sync waves: CRDs → operators → apps) → **Velero restore** (PVCs + Secrets + ConfigMaps). RTO < 30 min. Quarterly drill mandatory.

## Real-world scenarios

- **Quarterly drill — 22-min rebuild.** Quarterly disaster drill: destroy non-prod cluster; rebuild from Terraform + Argo CD + Velero. Measured: 22 min from start to SLO-passing. Runbook validated.
- **Real cluster loss — 28 min recovery.** Bad upgrade corrupted prod cluster; rebuild via runbook in 28 min; tenants noticed brief degradation; full recovery within RTO.
- **Sync wave caught CRD-first ordering.** Initial recovery attempt failed; apps referenced CRDs not yet created. Postmortem: sync waves -2 / -1 / 0+ for CRDs / operators / apps. Subsequent drill clean.
- **Outage — Velero backup not tested.** Backup existed but restore failed (StorageClass mismatch new cluster vs old). 6-hour outage. Postmortem: quarterly restore drill to find these gaps.

## Common misconceptions

- **Myth:** "Velero alone is enough."
  **Truth:** Velero handles K8s objects + PVCs; cluster itself needs IaC; secrets often need separate ESO + Vault recovery; DNS + external services need own DR. Coordinate.
- **Myth:** "Argo CD will figure out the order."
  **Truth:** Without sync waves, Argo CD applies in graph order — apps before CRDs may fail. Annotate sync-wave for deterministic ordering.
- **Myth:** "GitOps recovery is too complex; just snapshot the cluster."
  **Truth:** Snapshot-based recovery has limits (state drift, can't cross-region, large size). GitOps + IaC + Velero is more flexible + recoverable to any cluster shape.

## Recap

GitOps recovery: cluster IaC → CRDs (sync wave) → operators → apps → Velero restore PVCs / Secrets → DNS swap → validate. Quarterly drill measures + improves RTO.

**Next — D3: Cross-region DR + RPO/RTO + restore testing.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
