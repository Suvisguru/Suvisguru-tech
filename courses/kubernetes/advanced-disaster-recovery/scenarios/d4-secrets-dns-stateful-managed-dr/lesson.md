# K-ADV-DR D4 — D4 · Secret + DNS + Stateful + Managed-Service DR

> Course: K-ADV-DR (advanced specialization)
> Module D4 · Secrets + DNS + Stateful + Managed DR
> Companion preview: `/preview-kubernetes-adv-dr-lesson-04.html`.

---

**🎯 If you remember nothing else:** **Each subsystem has DR: secrets via Vault + KMS; DNS via Route 53; stateful via DB replication; managed services have built-in DR with limits. Understand each; coordinate timeline.**

## 1. Vault + KMS + ESO chain

**External Vault**: HA across multiple regions; raft replication for snapshot; quarterly snapshot to immutable storage. **KMS keys**: cross-region replicas (AWS / Azure / GCP all support); root-of-trust survives single-region loss.
    Recovery: rebuild Vault in DR region from snapshot; rotate seal keys; KMS keys auto-replicated; **External Secrets Operator (ESO)** in new cluster re-syncs from Vault; K8s Secrets re-materialise.
    Without external Vault: K8s Secrets can be Velero-backed but tightly coupled to cluster; less flexible.

## 2. Route 53 / Azure DNS + TTL + health checks

DNS-based failover: **Route 53** health-check on primary endpoint; on failure, swap A record to DR LB. **Azure DNS** + Traffic Manager equivalent. **GCP Cloud DNS** + Global LB.
    TTL tuning: lower TTL (30-60s) on critical records for faster failover; trade DNS query load for fast failover. Pre-stage low TTL before known maintenance windows.
    External-DNS K8s controller automates DNS records from Service / Ingress; per-cluster setup syncs to managed DNS.

## 3. DB replication + restore + consistency

Self-managed DBs (PostgreSQL / MySQL operators):
    
      - Multi-AZ replication (primary + 2 standbys via streaming).

      - Cross-region streaming replica.

      - Backup to S3 / Blob via cron-job (pg_basebackup / wal-g / pgbackrest / Percona XtraBackup).

      - Restore-tested quarterly; consistency model (eventual / strong) understood.

    
    K8s operators (CloudNativePG / Zalando postgres-operator / Strimzi for Kafka): handle replication lifecycle. PVC + CSI snapshot for periodic capture.

## 4. RDS / Cosmos / Spanner — built-in but limited

**AWS RDS / Aurora**: multi-AZ standby (synchronous; in-region); cross-region read replica (async; promote on disaster); **Aurora Global Database** (async cross-region; minute RPO; global LB). RTO: minutes for promote.
    **Azure Cosmos DB**: multi-region built-in; configurable consistency (Strong / Bounded Staleness / Session / Eventual / Consistent Prefix); auto-failover.
    **GCP Spanner**: regional (1 region) or multi-region (5+ regions strong consistency); built-in; expensive.
    **Limits**: cross-region promotion has data-loss window (RPO > 0); restore-from-snapshot can be slow (TB-scale = hours); test for your data size.

## Before / After

**Before.** Pre-coordinated specialty DR: secrets vanish on cluster loss; DNS swap manual; DB DR vague; managed-service DR assumed-but-untested.

**After.** External Vault + KMS replication for secrets; Route 53 health-check failover for DNS; DB replication with restore-tested for stateful; managed-service DR understood + tested.

*Each subsystem has its own DR pattern; coordinate the timeline.*

## Analogy — the K-Lifeboat cell

Cargo Recovery Office handles per-cargo-type recovery. Secrets cargo: separate vault in another region (Vault) + key copies (KMS). Routing cargo: signal flag tower (DNS + health check). Stateful cargo: replicated cargo holds (DB replication). Specialty cargo from vendors: each vendor has own recovery procedure (managed services).

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Separate vault in another region | External Vault HA + KMS replicas |
| Vault → ship handoff | External Secrets Operator re-sync |
| Signal flag tower failover | Route 53 / Azure DNS / Cloud DNS health check |
| Per-record signal speed | DNS TTL tuning |
| Replicated cargo holds | DB streaming replication + cross-region replica |
| Cargo manifest backup | DB backups to S3 / Blob |
| Vendor cargo recovery | Managed services (RDS / Cosmos / Spanner) |
| Vendor SLA limits | Cross-region promotion RPO + RTO |

⚠️ *Analogy stops here:* A real vendor cargo procedure is well-documented; managed-service DR has gotchas (region-availability, restore-time-at-scale). Test before you need it.

## ELI5 / ELI10

**ELI5.** Different cargo needs different recovery. Secrets in a vault elsewhere. Routing through a flag tower. Stateful cargo replicated. Vendor cargo per vendor procedure.

**ELI10.** **Secrets**: external Vault HA + KMS replication + ESO re-sync. **DNS**: Route 53 / Azure DNS / Cloud DNS health-check failover; tune TTL. **Stateful**: DB replication + cross-region replica + backups + restore-tested. **Managed services**: RDS / Aurora Global / Cosmos DB / Spanner — built-in DR; understand RPO + RTO + restore time.

## Real-world scenarios

- **External Vault saved DR.** Cluster lost in us-east-1; Vault HA in us-east-1 + us-west-2; rebuild cluster in us-west-2; ESO re-syncs from Vault us-west-2; secrets immediately available.
- **Route 53 failover automated DNS.** Primary cluster ALB unhealthy; Route 53 health check fires; A record swaps to DR ALB within 60s. Tenants notice brief blip.
- **Aurora Global Database for tier-1.** Fintech runs Aurora Global across us-east-1 + us-west-2; RPO < 1s; on disaster, promote DR to primary; RTO < 1 min. Cost premium accepted for tier-1.
- **Outage — assumed RDS DR worked.** Pre-test: assumed RDS multi-AZ = enough. Real disaster: cross-region promotion took 2h. Postmortem: Aurora Global Database; cross-region promotion drilled.

## Common misconceptions

- **Myth:** "K8s Secrets are sufficient."
  **Truth:** Cluster loss = K8s Secrets gone. External Vault is the foundation; K8s Secrets are derived (via ESO) + ephemeral.
- **Myth:** "DNS TTL of 24h is OK."
  **Truth:** High TTL = slow DNS failover. Critical records: TTL 30-60s + accept higher DNS query cost.
- **Myth:** "Managed-service DR is automatic."
  **Truth:** Managed services offer DR features but require deliberate config + tested promotion. Aurora multi-AZ ≠ Aurora Global Database; understand the difference.

## Recap

Specialty DR per subsystem: external Vault + KMS for secrets; Route 53 / Azure DNS health-check for DNS failover; DB replication for stateful; managed services have built-in DR with limits. Coordinate timeline + drill.

**Next — D5: Capstone — destroy + rebuild a complete production cluster.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
