# Lesson 20 — Configuration & Secrets · ConfigMap, Secret, KMS, External Secrets Operator

> Course: Kubernetes — Common to all distributions
> Module 10 · Config & Identity · Lesson 1 of 2
> Companion preview: `/preview-kubernetes-lesson-20.html`.

---

**🎯 If you remember nothing else:** `ConfigMap` for non-sensitive values; `Secret` for credentials. By default Secrets are stored in **etcd as plaintext** (base64 ≠ encryption) — wire up a **KMS provider** for encryption-at-rest. For credentials managed outside the cluster (Vault, AWS SM, GCP SM), use the **External Secrets Operator** to sync them in.

## 1. Why config and secrets are separate from your image

The 12-factor app rule: *config that varies between deployments belongs in the environment, not the image*. The same image runs in dev, staging, and production — only the config differs. K8s implements this with two API objects: `ConfigMap` and `Secret`.
    Both are **namespace-scoped** key/value stores. Both can be projected into a Pod two ways: as **environment variables** (read once at Pod start) or as a **mounted volume** (file-per-key, can hot-reload). The split between ConfigMap and Secret is purely *convention plus a few ergonomic differences* — they're not technically very different objects. The big difference is that you should treat Secrets with extra care, and the cluster should be configured to encrypt them at rest.

## 2. Two objects, similar shape, different intent

ConfigMapSecret
      
      
        IntentNon-sensitive valuesCredentials, tokens, certs
        Stored asPlain UTF-8 in etcdBase64-encoded in etcd (*not encrypted unless KMS is on*)
        Size limit1 MiB1 MiB
        Mountenv vars or filesenv vars or files (RAM-backed `tmpfs`)
        RBACStandard verbsSame verbs, but admins typically restrict `get/list` to fewer Roles
        AuditOften unrestrictedShould be audited (`Audit-Policy`)
        Special typesNone`kubernetes.io/dockerconfigjson`, `kubernetes.io/tls`, `kubernetes.io/service-account-token`
      
    
    **Critical:** by default, Secrets are stored in etcd in *base64*, not encrypted. Anyone with etcd read access (admins, backup processes, a compromised etcd backup) sees plaintext after a one-step decode. Always enable **encryption-at-rest** with a KMS provider in production.

## 3. Making Secrets actually secret

K8s ships an `EncryptionConfiguration` mechanism for the API server. You point it at a key source — and from then on, the API server encrypts Secrets (and any other resources you list) before writing to etcd, and decrypts on read.
    Two flavours:
    
      - **Static AES key** in a file on the API server's disk. Better than nothing, but the key sits next to the data; not great if the API server host is compromised.

      - **KMS provider** — the API server delegates the actual encryption operation to an external KMS (AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault, an on-prem HSM). The DEK (data encryption key) lives encrypted in etcd; the KEK (key-encryption key) lives only in the KMS. Compromising etcd alone is not enough.

    
    K8s 1.31 GA'd **KMS v2**, which adds key rotation, batched operations, and a new health-check API. Always use v2 in new clusters.
    [ deep dive — skip if new ]The actual encryption is envelope encryption: the API server generates a per-Secret DEK (data encryption key), encrypts the Secret payload with the DEK, then asks the KMS to encrypt the DEK with the KEK (key-encryption key). The encrypted DEK + ciphertext both go to etcd. Reads pull the encrypted DEK, ask the KMS to decrypt it (one fast call), then decrypt the Secret locally. Cost: one KMS call per Secret read. KMS v2 batches these for performance.

## 4. When the source of truth lives outside K8s

Most large orgs already have a credential store: HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, 1Password, Doppler. They don't want a copy of every credential pasted into K8s manifests. They want K8s to *fetch* from the source of truth and refresh on rotation.
    The **External Secrets Operator** (ESO) is a CRD-driven controller that does exactly this. You write an `ExternalSecret` YAML pointing at a remote path; ESO syncs it into a K8s `Secret` on a refresh interval (default 1 hour). Rotation in Vault → propagated to K8s → ConfigMap-style refresh in your Pod (or Pod restart, depending on how you mount).
    Three CRD objects:
    
      - `SecretStore` / `ClusterSecretStore` — points at the backend (Vault address, AWS account, etc.) and how to authenticate.

      - `ExternalSecret` — the request: "here's the remote key, here's the K8s Secret name, here's the refresh interval."

      - `PushSecret` (newer) — the reverse direction. Push a K8s-managed Secret to the external store.

    
    ESO is the de-facto standard. If you're running EKS/GKE/AKS in 2026 and have Vault or cloud SM, install ESO. Trying to manage everything by raw `Secret` YAML in production gets painful fast.

## Before / After

**Before.** Configuration baked into the image: `FROM nginx` + a custom config file. New environment = new image build = re-tag + redeploy. Secrets in env vars in YAML in git. Rotation means a code change. *One pasted Slack message away from a credential leak.*

**After.** Configuration in `ConfigMap`, mounted as files or env vars. Same image runs in every environment. Secrets in `Secret` objects, encrypted at rest in etcd via KMS, sourced from Vault via ExternalSecretsOperator. Rotation in Vault → automatic resync → app restart (or hot reload). *The image never knew the credential.*

12-factor: code that varies between environments belongs in the environment. K8s makes this not just possible but ergonomic.

## Analogy — the K-Town district

The Permit Office in K-Town is where every business in the city goes for paperwork. Two windows, side by side. The **rate card window** hands out today's prices, hours, posted policies — anyone can see them, the clerk reads them off a printout. The **credential window** hands out keys to vaults and signing rights — those are slipped across the counter in *sealed envelopes*, the clerk's name is logged, the keys themselves are minted in a back room nobody else enters.The mistake every new business owner makes: they treat the two windows the same way. They photograph their vault key and pin it to the office bulletin board "for convenience." That's a Secret in plain etcd. The fix is to insist on **actual encryption at rest** (a KMS provider) and to source long-lived credentials from a dedicated vault outside K-Town (Vault / AWS SM / etc., synced via ESO).

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The rate card window | `ConfigMap` |
| The credential window | `Secret` |
| Photographing the vault key for the bulletin board | Secret stored in etcd as base64 (no KMS provider) |
| The back-room key minter | KMS provider doing envelope encryption |
| A bonded courier from a dedicated vault company | External Secrets Operator (ESO) |
| The vault company's address book | `SecretStore` / `ClusterSecretStore` |
| A request slip filled out by an app team | `ExternalSecret` |

⚠️ *Analogy stops here:* The analogy stops here: real K8s Secrets aren't envelopes — they're records in a database. The protection is cryptographic, not physical, and it depends entirely on whether your cluster operator wired up a KMS provider.

## ELI5 / ELI10

**ELI5.** There are two boxes on the desk. One is full of stickers — anyone can grab one (that's **ConfigMap**: regular settings). The other is full of house keys — only specific people get those, and they're locked in a real safe, not just a wooden box (that's **Secret** + **KMS**).

**ELI10.** **ConfigMap** = key/value store for non-sensitive config (log levels, feature flags, region names). **Secret** = same shape but for credentials. By default Secrets are *base64 in etcd*, not encrypted — wire up a KMS provider via `EncryptionConfiguration` for real at-rest encryption. For long-lived credentials managed by Vault or cloud SM, use the External Secrets Operator (ESO) to sync them into K8s automatically. Mount as env vars (read-once) or files (auto-refresh).

## Real-world scenarios

- **A SaaS using GitOps + Sealed Secrets.** They commit YAML to git but never plain Secrets. Every Secret is sealed via Bitnami's Sealed Secrets controller — encrypted with a per-cluster public key, only the cluster's controller can decrypt. Git history is safe to share. Workflow stays declarative.
- **A bank running Vault + ESO.** Vault is the source of truth. Every K8s Secret is created from an `ExternalSecret` manifest. Rotation in Vault propagates within 1 hour. Audit log shows who synced what when. App teams never touch raw secrets — they just reference a SecretStore path.
- **A startup hot-reloading config without restart.** Their app watches `/etc/config/log_level` with inotify. ConfigMap mounted as a volume; K8s auto-syncs the file when the ConfigMap changes (~60s). They flip log level from `info` to `debug` in production with a `kubectl edit configmap`, no Pod restart, no rollout.
- **A team that learned the hard way.** Pre-2024 cluster, no KMS. Routine etcd backup landed on a misconfigured S3 bucket. A penetration test found the bucket; auditor decoded every Secret in 30 seconds. They had a long week. New cluster has KMS v2 + audit policy + access reviews. The mantra: "if you write a Secret, assume it leaks unless KMS says otherwise."

## Common misconceptions

- **Myth:** K8s Secrets are encrypted by default.
  **Truth:** They are *base64-encoded* by default. Encryption-at-rest only kicks in when you configure an `EncryptionConfiguration` with a provider (KMS or static key). Without that, an etcd dump = plaintext after one base64 decode.
- **Myth:** Mounting a Secret as a file is more secure than env vars.
  **Truth:** Both have tradeoffs. Env vars: visible to `/proc/<pid>/environ` for any process the Pod runs as; one-shot at start (no refresh). File mount: visible only to the process inside the Pod's mount namespace; hot-refreshes when the Secret changes. File mount is the better default, but neither is secret *from a privileged attacker on the node*.
- **Myth:** ConfigMap and Secret can be 10 MB if you compress.
  **Truth:** Both have a 1 MiB hard limit (etcd's default value-size cap). For larger config (e.g., model weights, large certs), use a PVC or pull from object storage at runtime. Keep ConfigMap/Secret for small key/value pairs.

## Recap

Two boxes: ConfigMap for plain config, Secret for credentials. "Secret" only means "secret" if you wire up KMS encryption-at-rest. For long-lived credentials managed elsewhere, sync them in with the External Secrets Operator.

**Next — Lesson 21: ServiceAccounts & Certificates.** The other half of the credential story — what tokens K8s itself hands out, projected service account tokens (the modern way), cert-manager, and how the cluster's own PKI works.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
