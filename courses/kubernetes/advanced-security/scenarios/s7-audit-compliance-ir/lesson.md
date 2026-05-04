# K-ADV-SEC S7 — S7 · Audit Log Analytics + Compliance Evidence + IR

> Course: K-ADV-SEC (advanced specialization)
> Module S7 · Audit + Compliance + IR
> Companion preview: `/preview-kubernetes-adv-sec-lesson-07.html`.

---

**🎯 If you remember nothing else:** **audit.k8s.io → SIEM pipeline. Map every compliance control to a queryable log surface. Break-glass replaces standing privilege. IR runbook tested via game days. Evidence + readiness are the two outputs.**

## 1. three log levels, webhook backend, retention policy

**audit.k8s.io** is the K8s audit subsystem. Configured via `--audit-policy-file` (what to log) + `--audit-webhook-config-file` (where to send) on the apiserver. Three levels per rule:
    
      - **Metadata**: who, what, when, source IP. No request body. Smallest volume.

      - **Request**: + request body (e.g., the YAML being created). Medium volume.

      - **RequestResponse**: + response body. Largest. Use selectively for high-value resources (Secrets, RBAC, Bindings).

    
    **Policy**: typical pattern — Metadata for everything; Request for write verbs; RequestResponse for Secret + RBAC reads/writes; omit noisy probes (kubelet self-checks). YAML lives in Git; rolled via apiserver static-Pod manifest update.
    **Backend**: webhook (preferred — async to SIEM); log file (fallback for sampling). Webhook latency must be tight or apiserver throttles.
    **Retention**: per compliance regime — PCI 12 months, HIPAA 6 years, SOC2 1 year. Tiered storage: SIEM hot (90 days) + S3 archive (long-term) + Glacier (final).

## 2. aggregate, correlate, alert

Audit alone is data; SIEM is signal. Pipeline:
    
      - **Ingest**: webhook → Loki / Splunk / OpenSearch / Datadog / Sentinel. Tagged with cluster + namespace + tenant.

      - **Index**: structured fields (verb, resource, user, response code, namespace).

      - **Correlate**: cross-source (audit + Falco + cloud audit + WAF) join on user / Pod / time. Multi-signal incidents surface.

      - **Alert**: tiered rules (immediate-page / Slack / log-only). Common rules: *secret-read by unexpected SA*, *RoleBinding to cluster-admin*, *privileged Pod created in non-system namespace*, *API impersonation used*, *auth failures spike*.

      - **Dashboards**: per compliance regime. PCI dashboard, HIPAA dashboard, SOC2 dashboard.

    
    Mature pipelines have **detection-as-code**: SIEM rules in Git; PR reviewed; tested with replay. New rules added when threat models evolve.

## 3. PCI · HIPAA · FedRAMP · SOC2 · NIST 800-190

Compliance regimes ask "how do you do X?" Map each control to a specific K8s mechanism + audit query:
    
      - **PCI DSS**: 7.1 (least privilege) → RBAC reviews; 8.2 (rotation) → ESO + cert-manager rotation logs; 10.x (audit) → audit.k8s.io retention + SIEM alerts.

      - **HIPAA**: §164.308(a)(4) (access management) → RoleBinding change logs; §164.312(b) (audit controls) → audit.k8s.io + immutable storage.

      - **SOC2**: CC6.1 (logical access) → OIDC + RBAC + JIT; CC7.2 (anomaly detection) → Falco + SIEM rules.

      - **FedRAMP** (Moderate / High): controls AC, AU, CM, IA, SC — map each to specific K8s + cloud config.

      - **NIST 800-190** (container security): every section maps directly — image trust (S5), runtime (S4), orchestrator (S2/S3), network (S6 mTLS).

    
    Pattern: **compliance-as-code** — control → SIEM query → expected result. CI runs the mapping nightly; failures surface before audit.

## 4. JIT elevation + tested incident response

**Break-glass**: standing cluster-admin removed for everyone. Elevation requires a JIT process — Vault one-time credential, ChatOps approval bot, or AWS SSO emergency role. Every JIT use alarms in Slack + email; expires in 1 hour; logged in audit.k8s.io.
    **IR runbook** follows NIST 800-61 / SP 800-184: *Containment* (cordon node, scale to zero, isolate namespace via NetPol drop-all); *Eradication* (remove backdoor, rotate compromised secrets, replace from clean image); *Recovery* (restore from clean state via GitOps; canary + verify); *Postmortem* (timeline + cause + control gaps + remediation actions).
    **Game days** exercise the runbook on calm days. Quarterly: red team injects a known-pattern compromise (curl-bash from a Pod, RoleBinding change, suspicious DNS); on-call follows the runbook; time-to-detect + time-to-contain measured + improved.
    Mature programs have an IR *library*: scenarios → runbooks → game-day frequency. Each major service has an entry. New CVEs of class X get a runbook + a game day within 30 days.

## Before / After

**Before.** Pre-mature security ops: audit logs to disk; rotated; nobody read them. Compliance evidence was point-in-time PowerPoints + sample YAMLs. Standing cluster-admin to operators. IR was "call the founder". Game days didn't exist; every incident was a first-time scramble.

**After.** Modern: audit.k8s.io → SIEM with retention per regime; compliance-as-code maps controls to queries; break-glass replaces standing privilege; IR runbook tested via game days; metrics on time-to-detect + time-to-contain. *Audits are routine; incidents are exercises that matter.*

*Build evidence + readiness on calm days. Both outputs are needed; both decay without exercise.*

## Analogy — the K-Citadel bastion

The deepest part of the citadel has two adjoining rooms. The **Audit Archives** hold copies of every gate-keeper's decisions, every transaction at the vault, every shift change. The archive is searchable; auditors visit annually and ask "show me every time someone signed for a vault key in 2025" — the archivist runs a query.
    The **War Room** next door has wall-mounted maps of every threat scenario the citadel has prepared for. Each scenario has a numbered binder: containment steps, eradication steps, recovery steps, postmortem template. Standing privilege has been removed; the captain elevates only via the alarmed key (break-glass). Quarterly drills test the binders; the captain who can run "Scenario 17: ransomware on the tenant compound" by 09:30 doesn't need to invent at 03:00.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Audit Archives | audit.k8s.io webhook → SIEM |
| Three archive depths | audit levels: Metadata / Request / RequestResponse |
| Archivist with a query | SIEM queries / Loki LogQL / Splunk SPL |
| Cross-source ledgers | Audit + Falco + cloud audit correlation |
| Compliance review register | Compliance-as-code (control → query) |
| War Room scenario binders | IR runbooks (NIST 800-61) |
| Quarterly drills | Game days |
| Alarmed elevation key | Break-glass JIT IAM |
| Postmortem ledger | Incident postmortem template |

⚠️ *Analogy stops here:* A real archive has paper copies; K8s audit is webhook delivery + SIEM storage — if the webhook misses or SIEM drops, the record is gone. Test the pipeline with synthetic events monthly.

## ELI5 / ELI10

**ELI5.** Two rooms. One holds copies of every decision in the castle, organised so anyone can search them. The other has labelled binders for every emergency: what to do first, second, third. The castle's leaders practice with the binders monthly so they know them by heart.

**ELI10.** **audit.k8s.io** logs every API request via webhook → SIEM (Loki / Splunk). Three levels (Metadata / Request / RequestResponse). Retention per regime (PCI 12mo / HIPAA 6yr / SOC2 1yr). **Correlation**: SIEM rules join audit + Falco + cloud audit. **Compliance mapping**: each control → SIEM query; CI verifies nightly. **Break-glass**: standing cluster-admin removed; JIT elevation alarmed. **IR runbook**: NIST 800-61 phases (containment → eradication → recovery → postmortem); game days quarterly.

## Real-world scenarios

- **Compliance-as-code dashboards.** A 200-engineer org runs nightly Loki queries mapping every PCI / SOC2 / HIPAA control to log evidence. Failures surface in Slack 14 hours before audits. Auditors review the mapping rather than sample artefacts; audit time drops from 6 weeks to 2 weeks.
- **Break-glass JIT replaces standing admin.** Standing cluster-admin removed across 5 clusters. JIT process: on-call invokes `kubectl-jit grant cluster-admin --reason "page-12345" --duration 1h`; approval bot in Slack; alarmed; logged. Quarterly review: how often, by whom, why. "Always-on admin" replaced by "earned-once-per-incident."
- **Game day caught a runbook gap.** Quarterly red team simulated a curl-bash compromise on a Pod. On-call followed runbook. Issue: runbook said "cordon node" but didn't name how to evict the compromised Pod cleanly without losing forensic data. Runbook updated; one-line fix; next game day clean.
- **Outage — audit pipeline went down quietly.** audit.k8s.io webhook timed out for 6 hours; apiserver buffered + dropped audit events. Nobody noticed; no synthetic-event canary. Postmortem: synthetic event every minute; SIEM alerts if absent > 10 minutes; redundant local-file backend as fallback.

## Common misconceptions

- **Myth:** "audit.k8s.io is on by default."
  **Truth:** **It's opt-in.** Without `--audit-policy-file` on apiserver, no audit records are produced. Configure the policy + webhook on day-1 of cluster bring-up, before any production traffic.
- **Myth:** "Compliance is a once-a-year thing."
  **Truth:** Compliance-as-code makes it nightly. Each control has a query; CI runs queries; failures alert in real-time. Annual audit becomes a review of the mapping, not a forensic reconstruction.
- **Myth:** "Game days are theatre; the runbook works."
  **Truth:** Untested runbooks rot. APIs change; tools deprecate; team turnover loses tribal knowledge. Quarterly game days catch decay early; first one always finds gaps.

## Recap

audit.k8s.io → SIEM is the foundation; compliance-as-code is the evidence; break-glass + IR runbook + game days are the readiness. All three on calm days; the war room is exercised, not invented.

**Next — S8: Capstone — defendable regulated platform.** Every K-ADV-SEC concept woven into one architecture for finance / healthcare. Threat model + zero-trust + RBAC + admission + PSA + signed images + secrets + mTLS + audit + compliance + IR.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
