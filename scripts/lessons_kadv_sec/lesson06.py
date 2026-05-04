"""K-ADV-SEC S6 — Secrets at scale + mTLS + service mesh."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Secrets + mTLS — External Secrets, Vault, mesh, SPIFFE.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Armored Vault · K-Citadel — secrets at rest, identity in flight</text>
  <rect x="40" y="70" width="160" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="120" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">External vault</text>
  <text x="120" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">HashiCorp Vault</text>
  <text x="120" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">/ AWS Secrets / Azure KV</text>
  <rect x="220" y="70" width="160" height="100" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="300" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">External Secrets Op</text>
  <text x="300" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">syncs vault → K8s Secret</text>
  <text x="300" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">+ KMS-encrypted at rest</text>
  <rect x="400" y="70" width="160" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="480" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Service mesh</text>
  <text x="480" y="108" text-anchor="middle" font-size="9" fill="#1F2433">Istio / Linkerd</text>
  <text x="480" y="124" text-anchor="middle" font-size="9" fill="#1F2433">automatic mTLS</text>
  <rect x="580" y="70" width="140" height="100" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="650" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">SPIFFE / SPIRE</text>
  <text x="650" y="108" text-anchor="middle" font-size="9" fill="#1F2433">workload identity</text>
  <text x="650" y="124" text-anchor="middle" font-size="9" fill="#1F2433">+ cert-manager</text>
</svg>"""


LESSON = LessonSpec(
    num="06",
    title_short="secrets + mTLS + mesh",
    title_full="S6 · Secrets at Scale + mTLS + Service Mesh Security",
    title_html="K-ADV-SEC S6 · Secrets + mTLS + Mesh",
    module_eyebrow="Module S6 · the Armored Vault — secrets at rest, identity in flight",
    hero_sub_html='Two coupled disciplines. <strong>Secrets at scale</strong>: store in an external vault (HashiCorp Vault / AWS Secrets Manager / Azure Key Vault); sync to cluster via External Secrets Operator (ESO); KMS-encrypt the K8s Secret at rest; rotate automatically. <strong>mTLS via service mesh</strong>: Istio / Linkerd / Cilium Mesh inject sidecars (or run as ambient mode); every Pod-to-Pod call is signed + encrypted using SPIFFE/SPIRE-issued workload identity; cert-manager + automated rotation back the cluster\'s PKI. The two together close the secret-leak + lateral-movement attack surfaces.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A repo audit found a database password committed in a Helm values.yaml from 2023. The password is still active. The team rotates it; <em>but they realise the same password was rotated by hand into 14 deployments — none of them have a runbook</em>. Today\'s lesson: design secrets as flowing artifacts (vault → ESO → K8s Secret → Pod) so rotation is one operation, not 14.",
    stamp_html="<strong>Secrets in external vault, synced via ESO, KMS-encrypted at rest. mTLS via mesh + SPIFFE/SPIRE workload identity. cert-manager + automated rotation. No long-lived static credentials anywhere.</strong>",
    district_pin="ksec-bastion06",
    district_label="Armored Vault",
    sections=[
        Section(
            eyebrow="Section 1.1 · external vault + ESO sync",
            h2="Vault / Secrets Manager / Key Vault as source of truth",
            body_html="""    <p>Pick one external vault. <strong>HashiCorp Vault</strong> for cloud-agnostic / hybrid; <strong>AWS Secrets Manager</strong> for AWS-only; <strong>Azure Key Vault</strong> / <strong>GCP Secret Manager</strong> similar. The vault holds the source-of-truth secrets + handles rotation (Lambda-style or built-in for DBs).</p>
    <p><strong>External Secrets Operator (ESO)</strong>: K8s controller that watches a <code>SecretStore</code> CR (vault auth config) + <code>ExternalSecret</code> CR (which secrets to sync where). ESO polls vault; creates/updates K8s Secrets; KMS-encrypts at rest via <code>--encryption-provider-config</code>.</p>
    <p>Pattern: per-namespace SecretStore using IRSA / Workload Identity / Pod Identity (no shared cluster-wide vault token). ESO\'s ServiceAccount in each namespace federates to the vault role for that namespace only — tenant isolation.</p>
    <p>Rotation: vault rotates → ESO detects on next poll → updates K8s Secret → Pods restart on Secret change (via reloader or in-app SDK). End-to-end rotation is a vault-API call.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · mesh-mTLS",
            h2="Istio / Linkerd / Cilium — sidecar vs ambient",
            body_html="""    <p><strong>Service mesh</strong> wraps every Pod-to-Pod call in mTLS automatically. Three popular meshes:</p>
    <ul>
      <li><strong>Istio</strong>: most features (traffic mgmt + policy + telemetry); sidecar mode (Envoy per Pod) or <em>ambient mode</em> (per-node ztunnel + per-namespace waypoint proxy — lower overhead).</li>
      <li><strong>Linkerd</strong>: simpler + faster than Istio; Rust micro-proxy; SPIFFE-based identity; ambient-style architecture.</li>
      <li><strong>Cilium Service Mesh</strong>: eBPF-based; integrates with Cilium NetworkPolicy + Hubble observability.</li>
    </ul>
    <p>All three: every workload gets a SPIFFE ID; mTLS certs are issued per workload; certs auto-rotate hourly; mesh enforces \"only signed traffic accepted\" per workload. Lateral movement after compromise is blocked at the mesh.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · SPIFFE / SPIRE + cert-manager",
            h2="workload identity standard",
            body_html="""    <p><strong>SPIFFE</strong> (Secure Production Identity Framework For Everyone) is the standard for workload identity. SPIFFE IDs look like <code>spiffe://cluster.local/ns/api/sa/orders</code>. <strong>SPIRE</strong> is the reference implementation: agents on each node issue short-lived X.509-SVIDs (or JWT-SVIDs) to workloads based on attestation rules.</p>
    <p>Mesh integration: Istio + Linkerd both issue SPIFFE-format certs to Pods. The mesh\'s control plane calls SPIRE (or its own CA) to issue per-Pod certs.</p>
    <p><strong>cert-manager</strong>: K8s CRD-based PKI for Ingress / API server / generic certs. Issuer types: ACME (Let\'s Encrypt), Vault, Venafi, custom CA, self-signed. CertificateRequest + Certificate CRDs auto-rotate via <code>renewBefore</code>. Pair with mesh for end-to-end PKI hygiene.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · zero-secrets pattern + audit",
            h2="No static credentials in images, env, or git",
            body_html="""    <p>The mature pattern is <strong>zero static credentials</strong> in container images, environment variables (committed to git), or Helm values. Sources of secrets:</p>
    <ul>
      <li><strong>Workload identity</strong> (IRSA / Workload Identity / Pod Identity): cloud auth via federation — Pod\'s SA token traded for cloud creds at runtime.</li>
      <li><strong>External Secrets via ESO</strong>: app secrets (DB passwords, API keys) fetched from vault.</li>
      <li><strong>SPIFFE workload identity</strong>: workload-to-workload mTLS identity.</li>
      <li><strong>cert-manager</strong>: in-cluster certs (Ingress, internal services).</li>
    </ul>
    <p><strong>Audit</strong>: scan images for hardcoded secrets (gitleaks, trufflehog); scan repos pre-commit (pre-commit hooks + git secrets); SIEM alert on Kubernetes Secret reads (audit.k8s.io). Quarterly review: any namespace with a Secret not managed by ESO or cert-manager → flag + remediate.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="Why use ESO with per-namespace SecretStore + IRSA / Workload Identity instead of one cluster-wide ESO?",
            options=[
                ("Performance.", False),
                ("Tenant isolation — each namespace gets only its own vault role / scope.", True),
                ("ESO requires it.", False),
            ],
            feedback="Per-namespace SecretStore + namespace-scoped vault role = tenant isolation at the secrets layer. A compromised namespace can\'t fetch another namespace\'s secrets via ESO.",
        ),
        3: PauseCheck(
            question="What does SPIFFE provide?",
            options=[
                ("A Kubernetes Secret type.", False),
                ("Workload identity standard (URI-style IDs + short-lived X.509/JWT).", True),
                ("A network plugin.", False),
            ],
            feedback="SPIFFE = Secure Production Identity Framework. SVIDs (X.509 or JWT) issued per workload via SPIRE; meshes use SPIFFE-format certs for mTLS.",
        ),
    },
    before_after_before='<p>Pre-vault clusters had secrets in env vars committed to git, ConfigMaps, or hand-rotated K8s Secrets. Rotation was manual + per-deployment — \"rotate password 14 times\" failure mode. Pod-to-Pod calls were unencrypted in the cluster network. Lateral movement after compromise was free.</p>',
    before_after_after='<p>Modern: secrets in external vault, synced via ESO, KMS-encrypted at rest. Pod-to-Pod over mesh-mTLS with SPIFFE workload identity. cert-manager + automated rotation. Workload identity (IRSA / Workload Identity / Pod Identity) for cloud auth. <em>Zero static credentials anywhere in source.</em></p>',
    before_after_caption='<p class="ba-caption"><em>Secrets flow; identity is short-lived; mTLS is automatic. Manual rotation is an anti-pattern.</em></p>',
    analogy_intro_html='''<p>The deepest stronghold in the citadel is the <strong>Armored Vault</strong>. Originally, secrets were copied by hand to every workshop in the citadel — when a key changed, every workshop had to be visited individually. Things broke when copies drifted; rotation was a multi-day job.</p>
    <p>The modern vault has three improvements. (1) A single <strong>master vault</strong> holds the source-of-truth (Vault / Secrets Manager / Key Vault). (2) <strong>Bonded couriers</strong> (External Secrets Operator) deliver secrets to each workshop on demand — automatically updated when the master changes. (3) Every courier presents their <strong>workshop-specific permit</strong> (per-namespace SecretStore + workload identity) — couriers can\'t cross-deliver.</p>
    <p>For workshop-to-workshop conversation, every worker now wears a <strong>numbered identity badge</strong> (SPIFFE ID) issued by the citadel\'s identity bureau (SPIRE), and every conversation is sealed in a tamper-evident envelope (mTLS). The mail-carrier (mesh sidecar) seals + checks every envelope automatically.</p>''',
    translation_rows=[
        ("Master vault", "External vault (HashiCorp / AWS Secrets / Azure KV / GCP SM)"),
        ("Bonded couriers", "External Secrets Operator (ESO)"),
        ("Workshop-specific permit", "Per-namespace SecretStore + IRSA / Workload Identity"),
        ("Sealed K8s storage chest", "K8s Secret with KMS encryption-at-rest"),
        ("Numbered identity badge", "SPIFFE workload ID"),
        ("Identity bureau", "SPIRE (or mesh CA issuing SPIFFE certs)"),
        ("Tamper-evident envelopes", "mTLS via service mesh (Istio / Linkerd / Cilium)"),
        ("Mail-carrier with sealing kit", "mesh sidecar (Envoy / Linkerd-proxy / ambient ztunnel)"),
        ("Citadel-wide PKI", "cert-manager (Ingress / API / generic certs)"),
    ],
    analogy_stops="A real vault holds physical objects; K8s Secrets are policy + bytes. KMS-encryption-at-rest is a config switch (encryption provider config) — easy to forget; verify with <code>etcdctl get</code> output.",
    eli5="The castle has one giant vault holding all the keys. Couriers bring keys to each workshop on schedule; couriers don\'t share routes. Every worker wears a numbered badge issued by the security office. Every message between workers is sealed in a tamper-proof envelope by the mail-carrier. No keys are left lying around.",
    eli10="<strong>External vault</strong> holds source-of-truth secrets. <strong>External Secrets Operator (ESO)</strong> syncs vault → K8s Secret per namespace; per-namespace SecretStore with workload identity. <strong>KMS encryption-at-rest</strong> via apiserver config. <strong>Service mesh</strong> (Istio / Linkerd / Cilium) injects sidecars or ambient proxies; auto mTLS for Pod-to-Pod with <strong>SPIFFE</strong>-format certs from <strong>SPIRE</strong>. <strong>cert-manager</strong> for cluster certs. <strong>Workload identity</strong> for cloud auth (IRSA / Workload Identity / Pod Identity). <strong>Zero static creds</strong> in images, env, or git.",
    scenarios=[
        Scenario(
            name="Greenfield with Vault + ESO + Linkerd",
            body="A 50-engineer SaaS deploys: HashiCorp Vault as cluster-external secret store; ESO with per-namespace SecretStore + IRSA; Linkerd auto-mTLS cluster-wide. From day one: zero static creds; mesh-mTLS for everything; rotation = vault API call.",
        ),
        Scenario(
            name="Brownfield audit + ESO migration",
            body="A team audits 200 namespaces; finds 80 K8s Secrets created manually + ~12 with credentials in git (oops). 6-month migration: vault setup, ESO ExternalSecret per Secret, gradual cutover. Each Secret\'s replacement validated; old Secret deleted from git history (BFG).",
        ),
        Scenario(
            name="Istio ambient — lower overhead than sidecars",
            body="A 1000-Pod cluster previously ran sidecar Istio with ~50 MiB memory overhead per Pod. Migration to Istio ambient: per-node ztunnel + per-namespace waypoint proxies; per-Pod overhead drops to ~5 MiB. mTLS still automatic; same SPIFFE identity model.",
        ),
        Scenario(
            name="Outage — vault unreachable; cluster kept running",
            body="An ESO-backed cluster lost vault connectivity for 90 minutes. Existing K8s Secrets stayed in cluster; Pods kept running with last-fetched values. Pod restarts that needed fresh secrets failed PROVISIONING; queued. Vault returned; ESO reconciled in 2 minutes; queued Pods drained. <em>Local cache + ESO\'s reconciliation kept blast radius small.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"K8s Secrets are encrypted by default.\"",
            truth="K8s Secrets are <em>base64-encoded by default</em>, NOT encrypted. To encrypt at rest, configure <code>--encryption-provider-config</code> on the apiserver pointing to KMS. Without that, etcd stores plain (base64) values. Verify with <code>etcdctl get</code>.",
        ),
        Misconception(
            myth="\"Service mesh is overkill for small clusters.\"",
            truth="The mTLS + workload identity benefits apply at any size. Linkerd has the lightest footprint; Istio ambient mode is now competitive. The right question is \"do we need Pod-to-Pod mTLS?\" — for any cluster handling sensitive data, the answer is yes.",
        ),
        Misconception(
            myth="\"SPIFFE / SPIRE adds complexity we don\'t need.\"",
            truth="If using a service mesh, you\'re using SPIFFE under the hood whether you know it or not. SPIRE explicit deployment matters when (a) you want workload identity for non-mesh workloads (databases, cloud APIs); (b) you need cross-cluster identity federation. For most teams, mesh-managed SPIFFE is enough.",
        ),
    ],
    flashcards=[
        Flashcard(front="What does ESO do?", back="Watches SecretStore + ExternalSecret CRs; polls external vault; creates/updates K8s Secrets in cluster. Per-namespace SecretStore + IRSA / Workload Identity = tenant-scoped sync."),
        Flashcard(front="Are K8s Secrets encrypted at rest by default?", back="<strong>No.</strong> Base64-encoded only. Enable encryption-at-rest via <code>--encryption-provider-config</code> on apiserver pointing to KMS. Without it, etcd holds plain values."),
        Flashcard(front="What does SPIFFE provide?", back="Workload identity standard. SPIFFE IDs (URIs like <code>spiffe://cluster/ns/X/sa/Y</code>) + short-lived X.509-SVID or JWT-SVID per workload. SPIRE is the reference implementation."),
        Flashcard(front="Sidecar vs ambient mode in service mesh?", back="<strong>Sidecar</strong>: Envoy proxy per Pod (~50 MiB memory each); per-Pod policy. <strong>Ambient</strong> (Istio / Linkerd new model): per-node ztunnel + per-namespace waypoint proxy; lower per-Pod overhead; same mTLS guarantees."),
        Flashcard(front="cert-manager — what does it do?", back="Automates X.509 cert issuance + rotation. Issuers (ACME / Vault / Venafi / CA / self-signed); Certificate + CertificateRequest CRDs; <code>renewBefore</code> auto-rotates."),
        Flashcard(front="Workload identity (IRSA / Workload Identity / Pod Identity) — what does it replace?", back="Long-lived AWS / GCP / Azure access keys baked into images / env vars. Replaced by federation: K8s SA token traded at cloud IAM for short-lived creds scoped per Pod."),
        Flashcard(front="Why per-namespace SecretStore in ESO?", back="Tenant isolation. A compromised namespace can\'t request other namespaces\' vault paths. Each SecretStore uses a workload identity scoped to one namespace + one vault path / role."),
        Flashcard(front="When is auto-mTLS via mesh insufficient?", back="When (a) workloads need cross-cluster mTLS (need cross-cluster mesh or SPIFFE federation); (b) workloads include non-K8s components (DBs, VM workloads — need explicit SPIRE agents); (c) regulated environments require key escrow or HSM-backed CA."),
    ],
    quizzes=[
        Quiz(
            prompt="Migrate a Helm chart with hardcoded DB password (in values.yaml committed to git) to ESO. Walk steps.",
            answer="(1) <strong>Inventory</strong>: list every place the password lives — values.yaml, deployment env, Pod spec. (2) <strong>Move to vault</strong>: write secret in HashiCorp Vault at <code>secret/myapp/db</code>. (3) <strong>Set up ESO</strong>: SecretStore CR in the namespace using IRSA / Workload Identity that has <code>read</code> on <code>secret/myapp/*</code>; ExternalSecret CR mapping <code>secret/myapp/db</code> → K8s Secret <code>myapp-db</code>. (4) <strong>Update Helm chart</strong>: replace hardcoded value with <code>secretKeyRef: {name: myapp-db, key: password}</code>; remove the value from values.yaml. (5) <strong>Validate</strong>: deploy in dev; ESO creates Secret; Pod consumes it. (6) <strong>Rotate</strong>: change password in vault; ESO updates Secret; reloader (or app SDK) restarts Pods. (7) <strong>Clean git history</strong>: BFG or git-filter-repo to remove the leaked password from past commits; revoke the leaked password forever in DB.",
        ),
        Quiz(
            prompt="A team objects to enabling mesh-mTLS — \"too much overhead.\" What\'s the modern Istio path that addresses this?",
            answer="<strong>Istio ambient mode</strong> removes the per-Pod sidecar overhead. Architecture: per-node <code>ztunnel</code> handles L4 mTLS for all Pods on the node; per-namespace <code>waypoint proxy</code> handles L7 if needed. <em>Per-Pod overhead</em> drops from ~50 MiB to ~5 MiB. <em>mTLS guarantees</em> stay (every Pod-to-Pod call signed). <em>Migration path</em>: deploy ambient alongside sidecars; flip workloads namespace-by-namespace; same Istio control plane. <em>Linkerd</em> uses similar architecture with even lower overhead. <em>Cilium Service Mesh</em> uses eBPF for the ambient role. <em>The performance argument no longer justifies skipping mesh-mTLS.</em>",
        ),
        Quiz(
            prompt="A vendor demands a static AWS credential in a K8s Secret for their integration. Defend pushing back to workload identity.",
            answer="\"<strong>A static AWS credential is exactly the failure mode workload identity removes.</strong> Three counter-points to argue for IRSA / Pod Identity: (1) <strong>Rotation</strong>: static credentials require rotation runbook + downtime risk. IRSA / Pod Identity rotate per-call automatically. (2) <strong>Blast radius</strong>: if the static credential leaks (image scan, log accident), it\'s usable from anywhere on the Internet. Workload-identity creds are scoped to the K8s cluster + the specific Pod\'s SA token + short TTL — usable only by that workload. (3) <strong>Compliance</strong>: PCI / HIPAA / SOC2 specifically call out long-lived credentials as a finding. <strong>Migration path for the vendor</strong>: ask their integration to support assume-role-with-web-identity (the standard for IRSA); if they can\'t today, set a 90-day deadline. <em>If absolutely required short-term</em>: store the credential in Vault, sync via ESO with rotation policy enforced by Vault\'s AWS-IAM secret engine. Even then, the credential is short-lived (vault rotates daily). <strong>Static creds are never the right answer in 2026.</strong>\"",
            cyoa=True,
            cyoa_tag="how the security architect rejected static creds",
        ),
    ],
    glossary=[
        GlossaryItem(name="External Secrets Operator (ESO)", definition="K8s controller that syncs secrets from external vault to K8s Secrets via SecretStore + ExternalSecret CRs."),
        GlossaryItem(name="SecretStore CR", definition="Per-namespace ESO config naming the vault + auth method. IRSA / Workload Identity preferred."),
        GlossaryItem(name="ExternalSecret CR", definition="ESO CR mapping vault keys to K8s Secret keys; refreshInterval controls poll frequency."),
        GlossaryItem(name="encryption-provider-config", definition="apiserver flag enabling encryption-at-rest for Secrets in etcd via KMS / aescbc / aesgcm."),
        GlossaryItem(name="SPIFFE / SPIRE", definition="Workload identity standard (SPIFFE) + reference implementation (SPIRE). SVIDs (X.509 or JWT) issued per workload."),
        GlossaryItem(name="Service mesh sidecar", definition="Envoy / Linkerd-proxy injected per Pod to handle mTLS + traffic management. Per-Pod memory overhead."),
        GlossaryItem(name="Service mesh ambient mode", definition="Per-node ztunnel + per-namespace waypoint proxy; lower per-Pod overhead than sidecars; same mTLS."),
        GlossaryItem(name="cert-manager", definition="K8s PKI operator. Issuer / Certificate / CertificateRequest CRDs; auto-rotation; ACME / Vault / CA / self-signed."),
        GlossaryItem(name="Workload identity", definition="Short-lived cloud creds via OIDC federation between K8s SA + cloud IAM. IRSA (AWS), Workload Identity (GCP), Pod Identity (Azure)."),
        GlossaryItem(name="Sealed Secrets / SOPS", definition="Alternative patterns — Sealed Secrets encrypts in git; SOPS encrypts files. Lighter than Vault but less powerful for rotation."),
    ],
    recap_lead="Secrets in external vault, synced via ESO with per-namespace tenant isolation, KMS-encrypted at rest. mTLS via mesh + SPIFFE identity. cert-manager for cluster PKI. Workload identity for cloud auth. Zero static credentials in source.",
    recap_next='<strong>Next — S7: Audit log analytics + compliance evidence + IR.</strong> audit.k8s.io webhook → SIEM; PCI / HIPAA / FedRAMP / SOC2 / NIST 800-190 control mapping; break-glass IAM; incident response playbooks.',
)
