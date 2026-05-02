from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Permit Office: a clerk hands out non-secret rate cards (ConfigMaps), seals confidential envelopes (Secrets), and behind a vault door an external broker (KMS / ESO) signs in to bring fresh credentials.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">PERMIT OFFICE · CONFIG &amp; CREDENTIALS WINDOW</text>
  <!-- Counter clerk -->
  <g transform="translate(40,55)">
    <rect x="0" y="80" width="120" height="20" rx="4" fill="#A06B45" stroke="#5A4F45" stroke-width="1"/>
    <circle cx="60" cy="20" r="14" fill="#FBF1D6" stroke="#2A2520" stroke-width="1.4"/>
    <circle cx="56" cy="18" r="1.4" fill="#2A2520"/><circle cx="64" cy="18" r="1.4" fill="#2A2520"/>
    <path d="M 54 24 Q 60 28 66 24" stroke="#2A2520" stroke-width="1.2" fill="none" stroke-linecap="round"/>
    <path d="M 48 34 Q 48 80 54 80 L 66 80 Q 72 80 72 34 Z" fill="#3F4A5E"/>
    <text x="60" y="120" text-anchor="middle" font-size="9" font-weight="700" fill="#3F4A5E">clerk</text>
    <text x="60" y="133" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">issues paperwork</text>
  </g>
  <!-- ConfigMap (rate card) -->
  <g transform="translate(180,55)">
    <rect width="100" height="80" rx="6" fill="#FFFFFF" stroke="#3F4A5E" stroke-width="1.4"/>
    <text x="50" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="#3F4A5E">RATE CARD</text>
    <line x1="14" y1="32" x2="86" y2="32" stroke="#9D9389" stroke-width="0.6"/>
    <text x="14" y="44" font-size="8" fill="#6B6058">log_level: info</text>
    <text x="14" y="56" font-size="8" fill="#6B6058">timeout: 30s</text>
    <text x="14" y="68" font-size="8" fill="#6B6058">region: us-east-1</text>
    <text x="50" y="100" text-anchor="middle" font-size="10" font-weight="700" fill="#3F4A5E">ConfigMap</text>
    <text x="50" y="113" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">non-secret config</text>
  </g>
  <!-- Secret (sealed envelope) -->
  <g transform="translate(310,55)">
    <rect width="100" height="80" rx="6" fill="#FBE8DC" stroke="#A04832" stroke-width="1.5"/>
    <path d="M 0 0 L 50 36 L 100 0" fill="none" stroke="#A04832" stroke-width="1.5"/>
    <circle cx="50" cy="50" r="12" fill="#A04832"/>
    <text x="50" y="54" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">🔒</text>
    <text x="50" y="100" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">Secret</text>
    <text x="50" y="113" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">base64 (NOT encrypted)</text>
  </g>
  <!-- KMS vault -->
  <g transform="translate(440,40)">
    <rect width="100" height="110" rx="8" fill="#3F4A5E" stroke="#1B1814" stroke-width="2"/>
    <circle cx="50" cy="40" r="20" fill="#5A4F45" stroke="#FBF7F0" stroke-width="1.5"/>
    <line x1="50" y1="20" x2="50" y2="40" stroke="#FBF7F0" stroke-width="2"/>
    <line x1="33" y1="35" x2="50" y2="40" stroke="#FBF7F0" stroke-width="2"/>
    <circle cx="50" cy="40" r="3" fill="#FBF7F0"/>
    <text x="50" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF7F0">KMS vault</text>
    <text x="50" y="93" text-anchor="middle" font-size="7" fill="#FBF7F0" font-style="italic">encrypts secrets</text>
    <text x="50" y="103" text-anchor="middle" font-size="7" fill="#FBF7F0" font-style="italic">at rest in etcd</text>
  </g>
  <!-- External Secrets Operator (broker) -->
  <g transform="translate(560,55)">
    <rect width="90" height="80" rx="6" fill="#E0EFE6" stroke="#5A9F7A" stroke-width="1.4"/>
    <text x="45" y="18" text-anchor="middle" font-size="8" font-weight="700" fill="#3D7857">EXTERNAL</text>
    <text x="45" y="29" text-anchor="middle" font-size="8" font-weight="700" fill="#3D7857">BROKER</text>
    <circle cx="20" cy="50" r="6" fill="#5A9F7A"/>
    <text x="20" y="53" text-anchor="middle" font-size="8" fill="#FFFFFF" font-weight="700">V</text>
    <text x="32" y="52" font-size="7" fill="#3D7857">Vault</text>
    <circle cx="20" cy="65" r="6" fill="#3F4A5E"/>
    <text x="20" y="68" text-anchor="middle" font-size="7" fill="#FFFFFF" font-weight="700">A</text>
    <text x="32" y="67" font-size="7" fill="#3F4A5E">AWS SM</text>
    <text x="45" y="100" text-anchor="middle" font-size="9" font-weight="700" fill="#3D7857">ESO</text>
    <text x="45" y="113" text-anchor="middle" font-size="8" fill="#6B6058" font-style="italic">syncs to Secrets</text>
  </g>
  <text x="340" y="200" text-anchor="middle" font-size="11" fill="#3F4A5E" font-style="italic">Rate cards travel openly. Confidential envelopes need an actual lock — not just a label.</text>
</svg>"""

LESSON = LessonSpec(
    num="20",
    title_short="config &amp; secrets",
    title_full="Configuration & Secrets · ConfigMap, Secret, KMS, External Secrets Operator",
    title_html="Lesson 20 — Configuration & Secrets · K-COM",
    module_eyebrow="Module 10 · Lesson 20 · separating code from config",
    hero_sub_html='Twelve-factor said it: <strong>configuration belongs out of the image</strong>. K8s gives you two boxes for that — <code>ConfigMap</code> for non-secret values, <code>Secret</code> for credentials. Then a third question: how do you make <code>Secret</code> actually secret?',
    hero_illu_svg=HERO_SVG,
    nightmare_html="A junior engineer ships a config change. The Pod restarts and crashes — turns out a <code>DATABASE_URL</code> Secret was missing. Easy fix, says the senior. They paste the connection string into Slack to share with the on-call engineer. Three hours later: a contractor's GitHub bot scrapes the channel, finds the credential, opens a connection. Half a million customer rows leak before anyone notices. Two lessons here. <em>One:</em> Secrets must never live in chat or git. <em>Two:</em> a K8s <code>Secret</code> stored in <code>etcd</code> with no KMS provider is just <em>base64-encoded plaintext</em> — it's not actually encrypted. This lesson is how to do this right.",
    stamp_html="<code>ConfigMap</code> for non-sensitive values; <code>Secret</code> for credentials. By default Secrets are stored in <strong>etcd as plaintext</strong> (base64 ≠ encryption) — wire up a <strong>KMS provider</strong> for encryption-at-rest. For credentials managed outside the cluster (Vault, AWS SM, GCP SM), use the <strong>External Secrets Operator</strong> to sync them in.",
    district_pin="kt-pin14",
    district_label="Permit Office — Configuration Window",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why config and secrets are separate from your image",
            body_html="""    <p>The 12-factor app rule: <em>config that varies between deployments belongs in the environment, not the image</em>. The same image runs in dev, staging, and production — only the config differs. K8s implements this with two API objects: <code>ConfigMap</code> and <code>Secret</code>.</p>
    <p>Both are <strong>namespace-scoped</strong> key/value stores. Both can be projected into a Pod two ways: as <strong>environment variables</strong> (read once at Pod start) or as a <strong>mounted volume</strong> (file-per-key, can hot-reload). The split between ConfigMap and Secret is purely <em>convention plus a few ergonomic differences</em> — they're not technically very different objects. The big difference is that you should treat Secrets with extra care, and the cluster should be configured to encrypt them at rest.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · ConfigMap vs Secret",
            h2="Two objects, similar shape, different intent",
            body_html="""    <table class="data-table">
      <thead>
        <tr><th></th><th>ConfigMap</th><th>Secret</th></tr>
      </thead>
      <tbody>
        <tr><td>Intent</td><td>Non-sensitive values</td><td>Credentials, tokens, certs</td></tr>
        <tr><td>Stored as</td><td>Plain UTF-8 in etcd</td><td>Base64-encoded in etcd (<em>not encrypted unless KMS is on</em>)</td></tr>
        <tr><td>Size limit</td><td>1 MiB</td><td>1 MiB</td></tr>
        <tr><td>Mount</td><td>env vars or files</td><td>env vars or files (RAM-backed <code>tmpfs</code>)</td></tr>
        <tr><td>RBAC</td><td>Standard verbs</td><td>Same verbs, but admins typically restrict <code>get/list</code> to fewer Roles</td></tr>
        <tr><td>Audit</td><td>Often unrestricted</td><td>Should be audited (<code>Audit-Policy</code>)</td></tr>
        <tr><td>Special types</td><td>None</td><td><code>kubernetes.io/dockerconfigjson</code>, <code>kubernetes.io/tls</code>, <code>kubernetes.io/service-account-token</code></td></tr>
      </tbody>
    </table>
    <p style="margin-top:18px"><strong>Critical:</strong> by default, Secrets are stored in etcd in <em>base64</em>, not encrypted. Anyone with etcd read access (admins, backup processes, a compromised etcd backup) sees plaintext after a one-step decode. Always enable <strong>encryption-at-rest</strong> with a KMS provider in production.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Encryption-at-rest with a KMS provider",
            h2="Making Secrets actually secret",
            body_html="""    <p>K8s ships an <code>EncryptionConfiguration</code> mechanism for the API server. You point it at a key source — and from then on, the API server encrypts Secrets (and any other resources you list) before writing to etcd, and decrypts on read.</p>
    <p>Two flavours:</p>
    <ul>
      <li><strong>Static AES key</strong> in a file on the API server's disk. Better than nothing, but the key sits next to the data; not great if the API server host is compromised.</li>
      <li><strong>KMS provider</strong> — the API server delegates the actual encryption operation to an external KMS (AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault, an on-prem HSM). The DEK (data encryption key) lives encrypted in etcd; the KEK (key-encryption key) lives only in the KMS. Compromising etcd alone is not enough.</li>
    </ul>
    <p>K8s 1.31 GA'd <strong>KMS v2</strong>, which adds key rotation, batched operations, and a new health-check API. Always use v2 in new clusters.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>The actual encryption is envelope encryption: the API server generates a per-Secret DEK (data encryption key), encrypts the Secret payload with the DEK, then asks the KMS to encrypt the DEK with the KEK (key-encryption key). The encrypted DEK + ciphertext both go to etcd. Reads pull the encrypted DEK, ask the KMS to decrypt it (one fast call), then decrypt the Secret locally. Cost: one KMS call per Secret read. KMS v2 batches these for performance.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · External Secrets Operator (ESO)",
            h2="When the source of truth lives outside K8s",
            body_html="""    <p>Most large orgs already have a credential store: HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, 1Password, Doppler. They don't want a copy of every credential pasted into K8s manifests. They want K8s to <em>fetch</em> from the source of truth and refresh on rotation.</p>
    <p>The <strong>External Secrets Operator</strong> (ESO) is a CRD-driven controller that does exactly this. You write an <code>ExternalSecret</code> YAML pointing at a remote path; ESO syncs it into a K8s <code>Secret</code> on a refresh interval (default 1 hour). Rotation in Vault → propagated to K8s → ConfigMap-style refresh in your Pod (or Pod restart, depending on how you mount).</p>
    <p>Three CRD objects:</p>
    <ul>
      <li><code>SecretStore</code> / <code>ClusterSecretStore</code> — points at the backend (Vault address, AWS account, etc.) and how to authenticate.</li>
      <li><code>ExternalSecret</code> — the request: "here's the remote key, here's the K8s Secret name, here's the refresh interval."</li>
      <li><code>PushSecret</code> (newer) — the reverse direction. Push a K8s-managed Secret to the external store.</li>
    </ul>
    <p>ESO is the de-facto standard. If you're running EKS/GKE/AKS in 2026 and have Vault or cloud SM, install ESO. Trying to manage everything by raw <code>Secret</code> YAML in production gets painful fast.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A teammate opens a Secret YAML and sees the password decoded as <code>cGFzc3dvcmQ=</code>. They say \"oh, it's already encrypted, we're fine.\" What's the issue?",
            options=[
                ("a) That's not the right encryption — should be SHA-256", False),
                ("b) <code>cGFzc3dvcmQ=</code> is just base64 of <code>password</code> — it's encoded, not encrypted. Anyone with read access decodes it instantly.", True),
                ("c) Nothing — base64 is the K8s standard for secrets", False),
            ],
            feedback="<strong>Answer: b.</strong> Base64 is an encoding, not encryption. <code>echo cGFzc3dvcmQ= | base64 -d</code> gives <code>password</code>. The protection mechanism is encryption-at-rest in etcd via KMS, not the base64 wrapping.",
        ),
    },
    before_after_before='<p>Configuration baked into the image: <code>FROM nginx</code> + a custom config file. New environment = new image build = re-tag + redeploy. Secrets in env vars in YAML in git. Rotation means a code change. <em>One pasted Slack message away from a credential leak.</em></p>',
    before_after_after='<p>Configuration in <code>ConfigMap</code>, mounted as files or env vars. Same image runs in every environment. Secrets in <code>Secret</code> objects, encrypted at rest in etcd via KMS, sourced from Vault via ExternalSecretsOperator. Rotation in Vault → automatic resync → app restart (or hot reload). <em>The image never knew the credential.</em></p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">12-factor: code that varies between environments belongs in the environment. K8s makes this not just possible but ergonomic.</p>',
    analogy_intro_html='<p>The Permit Office in K-Town is where every business in the city goes for paperwork. Two windows, side by side. The <strong>rate card window</strong> hands out today\'s prices, hours, posted policies — anyone can see them, the clerk reads them off a printout. The <strong>credential window</strong> hands out keys to vaults and signing rights — those are slipped across the counter in <em>sealed envelopes</em>, the clerk\'s name is logged, the keys themselves are minted in a back room nobody else enters.</p><p>The mistake every new business owner makes: they treat the two windows the same way. They photograph their vault key and pin it to the office bulletin board "for convenience." That\'s a Secret in plain etcd. The fix is to insist on <strong>actual encryption at rest</strong> (a KMS provider) and to source long-lived credentials from a dedicated vault outside K-Town (Vault / AWS SM / etc., synced via ESO).</p>',
    translation_rows=[
        ("The rate card window", "<code>ConfigMap</code>"),
        ("The credential window", "<code>Secret</code>"),
        ("Photographing the vault key for the bulletin board", "Secret stored in etcd as base64 (no KMS provider)"),
        ("The back-room key minter", "KMS provider doing envelope encryption"),
        ("A bonded courier from a dedicated vault company", "External Secrets Operator (ESO)"),
        ("The vault company's address book", "<code>SecretStore</code> / <code>ClusterSecretStore</code>"),
        ("A request slip filled out by an app team", "<code>ExternalSecret</code>"),
    ],
    analogy_stops="The analogy stops here: real K8s Secrets aren't envelopes — they're records in a database. The protection is cryptographic, not physical, and it depends entirely on whether your cluster operator wired up a KMS provider.",
    eli5="There are two boxes on the desk. One is full of stickers — anyone can grab one (that's <strong>ConfigMap</strong>: regular settings). The other is full of house keys — only specific people get those, and they're locked in a real safe, not just a wooden box (that's <strong>Secret</strong> + <strong>KMS</strong>).",
    eli10="<strong>ConfigMap</strong> = key/value store for non-sensitive config (log levels, feature flags, region names). <strong>Secret</strong> = same shape but for credentials. By default Secrets are <em>base64 in etcd</em>, not encrypted — wire up a KMS provider via <code>EncryptionConfiguration</code> for real at-rest encryption. For long-lived credentials managed by Vault or cloud SM, use the External Secrets Operator (ESO) to sync them into K8s automatically. Mount as env vars (read-once) or files (auto-refresh).",
    scenarios=[
        Scenario(name="A SaaS using GitOps + Sealed Secrets", body="They commit YAML to git but never plain Secrets. Every Secret is sealed via Bitnami's Sealed Secrets controller — encrypted with a per-cluster public key, only the cluster's controller can decrypt. Git history is safe to share. Workflow stays declarative."),
        Scenario(name="A bank running Vault + ESO", body="Vault is the source of truth. Every K8s Secret is created from an <code>ExternalSecret</code> manifest. Rotation in Vault propagates within 1 hour. Audit log shows who synced what when. App teams never touch raw secrets — they just reference a SecretStore path."),
        Scenario(name="A startup hot-reloading config without restart", body="Their app watches <code>/etc/config/log_level</code> with inotify. ConfigMap mounted as a volume; K8s auto-syncs the file when the ConfigMap changes (~60s). They flip log level from <code>info</code> to <code>debug</code> in production with a <code>kubectl edit configmap</code>, no Pod restart, no rollout."),
        Scenario(name="A team that learned the hard way", body="Pre-2024 cluster, no KMS. Routine etcd backup landed on a misconfigured S3 bucket. A penetration test found the bucket; auditor decoded every Secret in 30 seconds. They had a long week. New cluster has KMS v2 + audit policy + access reviews. The mantra: \"if you write a Secret, assume it leaks unless KMS says otherwise.\""),
    ],
    misconceptions=[
        Misconception(myth="K8s Secrets are encrypted by default.", truth="They are <em>base64-encoded</em> by default. Encryption-at-rest only kicks in when you configure an <code>EncryptionConfiguration</code> with a provider (KMS or static key). Without that, an etcd dump = plaintext after one base64 decode."),
        Misconception(myth="Mounting a Secret as a file is more secure than env vars.", truth="Both have tradeoffs. Env vars: visible to <code>/proc/&lt;pid&gt;/environ</code> for any process the Pod runs as; one-shot at start (no refresh). File mount: visible only to the process inside the Pod's mount namespace; hot-refreshes when the Secret changes. File mount is the better default, but neither is secret <em>from a privileged attacker on the node</em>."),
        Misconception(myth="ConfigMap and Secret can be 10 MB if you compress.", truth="Both have a 1 MiB hard limit (etcd's default value-size cap). For larger config (e.g., model weights, large certs), use a PVC or pull from object storage at runtime. Keep ConfigMap/Secret for small key/value pairs."),
    ],
    flashcards=[
        Flashcard(front="ConfigMap vs Secret — are they technically different?", back="Mostly the same shape (key/value, namespace-scoped, env-var or file mount). Real difference is <em>intent</em> + <em>ergonomic guardrails</em>: Secrets get RBAC scrutiny, are stored on tmpfs (RAM) when mounted, and benefit from KMS encryption-at-rest. ConfigMaps usually don't."),
        Flashcard(front="Are K8s Secrets encrypted at rest?", back="Only if you configure encryption. By default they're base64 in etcd. Wire up an <code>EncryptionConfiguration</code> with a KMS provider (v2 in K8s 1.31+) for real encryption."),
        Flashcard(front="Two ways to project a ConfigMap into a Pod?", back="(1) <code>envFrom: configMapRef</code> or per-key <code>env: valueFrom: configMapKeyRef</code> — read once at Pod start. (2) <code>volumes: configMap</code> with a <code>volumeMounts</code> entry — file per key; ~60s auto-sync when ConfigMap changes."),
        Flashcard(front="What's KMS v2?", back="K8s 1.31 GA. Replaces KMS v1: adds key rotation without API server restart, batched encrypt/decrypt for performance, and a health-check API. Always use v2 in new clusters."),
        Flashcard(front="What is the External Secrets Operator?", back="A CRD-driven controller that syncs credentials from external sources (Vault, AWS SM, GCP SM, Azure KV, 1Password) into K8s Secrets on a refresh interval. De-facto standard since ~2023. Three core CRDs: SecretStore, ExternalSecret, PushSecret."),
        Flashcard(front="Sealed Secrets vs ESO?", back="Sealed Secrets: encrypts a Secret with a cluster-public-key so the encrypted form can be committed to git; cluster controller decrypts on apply. ESO: pulls from an external secret store at runtime; nothing in git. Different threat models — both common in GitOps shops."),
        Flashcard(front="What's <code>kubernetes.io/tls</code>?", back="A Secret type carrying <code>tls.crt</code> and <code>tls.key</code>. Used by Ingresses, Gateways, and webhook configurations. cert-manager creates these automatically from issued certificates."),
        Flashcard(front="Hot-reload of mounted Secret/ConfigMap?", back="Mounted as a volume → kubelet rewrites the file when the Secret changes (delay ~60s by default; controlled by sync period). Mounted as env var → no refresh; needs Pod restart. App must watch the file (inotify) to pick up the change."),
    ],
    quizzes=[
        Quiz(prompt="A team mounts a <code>Secret</code> as both an env var <em>and</em> a volume. They rotate the underlying credential in the Secret. What happens?", answer="The volume-mounted file gets the new value within ~60 seconds (the kubelet sync period). The env var <strong>does not change</strong> — env vars are populated once at Pod start. Result: the same Pod has two versions of the credential at the same time. Fix: pick one method (file mount is generally preferred for rotation) and have the app re-read the file on a watch."),
        Quiz(prompt="Your security team asks: \"is it safe for an engineer to <code>kubectl describe secret/db-creds</code> in prod?\" What's the answer?", answer="Mostly safe — <code>describe</code> shows metadata and key names but not values. <code>kubectl get secret -o yaml</code> <em>does</em> show base64-encoded values, which is plaintext after one decode. Lock down <code>get</code> verb on Secrets to a small set of subjects via RBAC; allow <code>list</code> + <code>describe</code> for ops users. Add an audit policy entry that logs all Secret reads at <code>RequestResponse</code> level."),
        Quiz(prompt="Production etcd backup ends up on an exposed S3 bucket. Cluster has no KMS configured. Storage class admin asks: \"how exposed are we?\" <strong>Click for the assessment. ▼</strong>", cyoa=True, cyoa_tag="the post-incident assessment", answer="Catastrophically. With no <code>EncryptionConfiguration</code>, every Secret in etcd is base64-encoded plaintext. <code>etcdctl get --prefix /registry/secrets/ --print-value-only | base64 -d</code> reveals every credential the cluster has — DB passwords, API tokens, TLS keys, service account tokens, image-pull credentials. The blast radius is the union of every Secret across every namespace. <strong>Action items:</strong> (1) treat every Secret as compromised — rotate all of them. (2) Enable KMS v2 on the new cluster before re-creating Secrets. (3) Audit etcd backup access policies. (4) Add a runtime detection rule: alert if any process other than kube-apiserver reads etcd. KMS doesn't make backups invincible (the KMS could be compromised too) but it raises the bar from \"one S3 leak compromises everything\" to \"attacker needs both the etcd dump <em>and</em> KMS access.\""),
    ],
    glossary=[
        GlossaryItem(name="ConfigMap", definition="Namespace-scoped key/value object for non-sensitive configuration. Mounted as env vars or files."),
        GlossaryItem(name="Secret", definition="Namespace-scoped key/value object for credentials. Base64 in etcd by default; encrypted-at-rest only with KMS."),
        GlossaryItem(name="EncryptionConfiguration", definition="API-server-level config that enables encryption-at-rest. Lists which resources to encrypt and which provider (identity, aescbc, secretbox, kms)."),
        GlossaryItem(name="KMS provider", definition="External key management service that holds the KEK. K8s API server calls it to encrypt/decrypt DEKs. Examples: AWS KMS, GCP KMS, Azure KV, Vault Transit."),
        GlossaryItem(name="KMS v2", definition="K8s 1.31 GA. Modern KMS protocol with rotation, batching, health checks. Use this for new clusters."),
        GlossaryItem(name="External Secrets Operator (ESO)", definition="CRD-driven controller syncing external secrets into K8s. De-facto standard for Vault / cloud SM integration."),
        GlossaryItem(name="SecretStore / ClusterSecretStore", definition="ESO CRD pointing at a backend (Vault address, AWS account) plus auth method."),
        GlossaryItem(name="ExternalSecret", definition="ESO CRD: \"sync remote path X to K8s Secret Y, refresh every Z minutes.\""),
        GlossaryItem(name="Sealed Secrets", definition="Bitnami project: encrypts a Secret with a cluster public key so the encrypted form can live in git. Distinct from ESO."),
        GlossaryItem(name="kubernetes.io/tls", definition="Secret type carrying <code>tls.crt</code> + <code>tls.key</code>. Used by Ingress, Gateway, webhooks."),
        GlossaryItem(name="Envelope encryption", definition="DEK encrypts data, KEK encrypts DEK, only the encrypted DEK + ciphertext go to storage. Compromising etcd ≠ compromising data."),
        GlossaryItem(name="tmpfs mount", definition="When a Secret is mounted as a volume, the kubelet uses tmpfs (RAM-backed) so it never hits the node's disk."),
    ],
    recap_lead="Two boxes: ConfigMap for plain config, Secret for credentials. \"Secret\" only means \"secret\" if you wire up KMS encryption-at-rest. For long-lived credentials managed elsewhere, sync them in with the External Secrets Operator.",
    recap_next="<strong>Next — Lesson 21: ServiceAccounts & Certificates.</strong> The other half of the credential story — what tokens K8s itself hands out, projected service account tokens (the modern way), cert-manager, and how the cluster's own PKI works.",
)
