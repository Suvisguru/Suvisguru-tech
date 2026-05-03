"""K-GKE G4 — GKE Identity and Security (IAM, WIF for GKE, Binary Auth, Posture, Confidential, Sandbox)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GKE identity + security stack — IAM/RBAC, WIF for GKE, Binary Auth, Posture, Confidential, Sandbox.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Gatekeeper's Lodge — defence in depth</text>
  <rect x="40" y="70" width="170" height="120" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="125" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">identity</text>
  <text x="125" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">IAM + RBAC + Conditions</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">Workload Identity Federation</text>
  <text x="125" y="131" text-anchor="middle" font-size="9" fill="#FBF1D6">G-SA ↔ K8s SA bindings</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">Connect Gateway</text>
  <rect x="225" y="70" width="170" height="120" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="310" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">supply chain + admission</text>
  <text x="310" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Binary Authorization</text>
  <text x="310" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Artifact Registry scan</text>
  <text x="310" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">Policy Controller (Gatekeeper)</text>
  <text x="310" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">Config Sync (GitOps)</text>
  <rect x="410" y="70" width="170" height="120" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="495" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">runtime + posture</text>
  <text x="495" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">Security Posture</text>
  <text x="495" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">Container Threat Detection</text>
  <text x="495" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">(Security Command Center)</text>
  <text x="495" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">Secret Manager CSI</text>
  <rect x="595" y="70" width="125" height="120" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="657" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">node + hardware</text>
  <text x="657" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">Shielded nodes</text>
  <text x="657" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">Confidential GKE</text>
  <text x="657" y="130" text-anchor="middle" font-size="9" fill="#FBF1D6">(AMD SEV · Intel TDX)</text>
  <text x="657" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">GKE Sandbox (gVisor)</text>
  <text x="657" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">CMEK · disks/secrets/images</text>
</svg>"""


LESSON = LessonSpec(
    num="04",
    title_short="identity + security",
    title_full="G4 · GKE Identity and Security",
    title_html="K-GKE G4 · Identity and Security",
    module_eyebrow="Module G4 · the Gatekeeper's Lodge — defence in depth",
    hero_sub_html='<strong>Identity:</strong> GCP IAM + K8s RBAC + IAM Conditions; <strong>Workload Identity Federation for GKE</strong> (replacement for older Workload Identity GKE Pool); G-SA ↔ K8s SA bindings; Connect Gateway. <strong>Supply chain + admission:</strong> <strong>Binary Authorization</strong> (signature/attestation enforcement at deploy); Artifact Registry scanning + remote/virtual repos; Policy Controller (managed Gatekeeper) + Config Sync. <strong>Runtime + posture:</strong> GKE Security Posture; Container Threat Detection (SCC); Secret Manager CSI. <strong>Node + hardware:</strong> Shielded nodes; Confidential GKE Nodes (AMD SEV / Intel TDX); GKE Sandbox (gVisor); CMEK across disks / secrets / images.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. Container Threat Detection alert: a Pod with Workload Identity bound to a G-SA holding Storage Admin on production data is making outbound calls to a known crypto-miner pool. The image was scanned at build, but a CVE was published last week. Binary Authorization wasn\'t enforcing signatures. <em>Blast radius is everything.</em> Today\'s lesson: layered GKE security — identity, supply chain, posture, runtime, hardware.",
    stamp_html="<strong>Layered defence: Workload Identity Federation (no secrets in Pods); Binary Authorization (deploy-time signature/attestation); Policy Controller (admission); Security Posture + CTD (runtime); Confidential / Shielded / Sandbox nodes; CMEK end-to-end. Each layer matters.</strong>",
    district_pin="kg-plot04",
    district_label="Gatekeeper's Lodge",
    sections=[
        Section(
            eyebrow="Section 1.1 · IAM + RBAC + Workload Identity Federation",
            h2="IAM + RBAC + Workload Identity Federation for GKE",
            body_html="""    <p>GKE has two identity surfaces.</p>
    <ul>
      <li><strong>Human → cluster:</strong> GCP IAM authenticates; either GCP IAM (with the <em>Kubernetes Engine Developer/Admin/Viewer</em> roles) <em>or</em> K8s RBAC authorises (or both — additive). <strong>IAM Conditions</strong> let you scope grants ("allow read of cluster X only if request comes from the corp VPN range"). For audit + just-in-time access, use <strong>IAM PAM</strong> or short-lived role grants.</li>
      <li><strong>Pod → GCP service:</strong> <strong>Workload Identity Federation for GKE</strong> — the modern replacement for the older Workload Identity GKE Pool model. The cluster\'s OIDC issuer + a federated identity pool let K8s ServiceAccounts impersonate or directly authenticate as Google Service Accounts (or directly as principals via WIF principal binding). <em>Pods get short-lived GCP access tokens with no secret in cluster.</em></li>
    </ul>
    <p><strong>Pattern:</strong> annotate K8s SA → bind to G-SA → grant G-SA the IAM roles on target resources (Storage / BigQuery / Pub/Sub / Secret Manager). Pod uses the K8s SA; gcloud SDK in the Pod calls Workload Identity metadata server; gets short-lived G-SA token; calls GCP API normally.</p>
    <p><strong>Connect Gateway</strong> (covered in G8) lets a human run kubectl against any registered fleet cluster via the GCP control plane — no need to expose individual cluster apiserver IPs to humans; auth flows through IAM.</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · supply chain — Binary Authorization + Artifact Registry + Policy Controller",
            h2="Binary Authorization + Artifact Registry + Policy Controller + Config Sync",
            body_html="""    <p><strong>Artifact Registry</strong> = GCP\'s container + package registry. Features: <em>vulnerability scanning</em> (continuous CVE scan), <em>remote repos</em> (proxy upstream Docker Hub / GitHub Container Registry — protects against upstream blips), <em>virtual repos</em> (combine multiple sources behind one URL), <em>attestations</em> (signed metadata about images: \"this image passed scan,\" \"this image was built by trusted CI\").</p>
    <p><strong>Binary Authorization</strong> (BinAuth) = deploy-time signature / attestation enforcement. Configure a policy: \"Pods in namespace X may only run images that have an attestation from Attestor Y.\" Pods that don\'t meet the policy are <em>rejected at admission</em>. Attestors are typically Google KMS-signed pipelines: \"image passed Artifact Registry scan = sign attestation; image was built by trusted CI = sign attestation.\" <em>BinAuth + Artifact Registry scanning = supply-chain trust at deploy</em>.</p>
    <p><strong>Policy Controller</strong> (managed OPA Gatekeeper) — fleet-wide admission policies. Built-in <em>Constraint templates</em> for common policies (require labels, restrict registries, block hostPath, etc.); custom policies via Rego or CEL. Effect: <em>Audit</em> (log) or <em>Enforce</em> (deny). Ships as part of GKE Enterprise.</p>
    <p><strong>Config Sync</strong> — fleet-wide GitOps. <code>RootSync</code> + <code>RepoSync</code> reconcile manifests from Git into clusters. Use to deploy NetworkPolicies, RBAC, ConfigMaps, applications uniformly across the fleet. Drift detection on; manual overrides reverted.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · runtime — Security Posture + CTD + Secret Manager CSI",
            h2="Security Posture + Container Threat Detection + Secret Manager CSI",
            body_html="""    <p><strong>GKE Security Posture dashboard</strong> — continuously evaluates cluster + workloads against the GKE security baseline + CIS K8s Benchmark. Findings: \"PSA not enforced in namespace X,\" \"NetworkPolicy missing in namespace Y,\" \"image with critical CVE running in production.\" Actionable; integrates with Security Command Center.</p>
    <p><strong>Container Threat Detection (CTD)</strong> — part of <strong>Security Command Center (SCC)</strong>. Runtime threat detection on GKE nodes — watches for known malicious behaviours (suspicious shell-in-container, crypto-miner, lateral movement, K8s-specific TTPs). Alerts ship to SCC + Cloud Logging.</p>
    <p><strong>Secret Manager CSI driver</strong> — mounts <strong>Secret Manager</strong> secrets as files in Pods. Authenticates via Workload Identity Federation; auto-rotation supported. <em>Cleaner than env-var Secrets</em>: file-based, watched by app for changes, no Secret-in-K8s with the rotation gap.</p>
    <p><strong>Pod Security Admission (PSA)</strong> — same K8s-native PSA standard. Enforce <em>Restricted</em> per namespace as the production default. Combines with Policy Controller for custom rules beyond the PSA baseline.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · node + hardware — Shielded, Confidential, Sandbox, CMEK",
            h2="Shielded nodes + Confidential GKE + GKE Sandbox + CMEK",
            body_html="""    <p><strong>Shielded GKE Nodes</strong> — Secure Boot + virtual TPM attestation. Default for new clusters. Catches rootkit injection at boot.</p>
    <p><strong>Confidential GKE Nodes</strong> — memory encryption with attestation at the silicon level: <strong>AMD SEV / SEV-SNP</strong> (Confidential VMs on N2D / C2D) and <strong>Intel TDX</strong>. Per-Pod memory encrypted; even Google operators cannot read it. For regulated workloads (PII, financial, health, ML on sensitive data).</p>
    <p><strong>GKE Sandbox (gVisor)</strong> — runs untrusted Pods inside a user-space kernel that intercepts syscalls. Stronger isolation than the default container runtime; performance trade-off (~5-15% on syscall-heavy workloads). For multi-tenant clusters running untrusted workloads (CI runners, customer-submitted code).</p>
    <p><strong>CMEK (Customer-Managed Encryption Keys)</strong> — encrypt at rest with keys you control via Cloud KMS:
    <ul>
      <li><strong>Persistent Disks</strong> — node OS disks + PVC disks encrypted with CMEK.</li>
      <li><strong>etcd Secrets</strong> — Application-layer Secrets encryption: K8s Secrets in etcd encrypted with CMEK before write.</li>
      <li><strong>Artifact Registry images</strong> — image storage encrypted with CMEK.</li>
    </ul>
    Combine with <strong>VPC Service Controls</strong> for data-exfiltration boundaries.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A new image is pushed to Artifact Registry. Pipeline scans it; result is clean. The team wants \"only attested clean images deploy.\" Which feature?",
            options=[
                ("Policy Controller alone.", False),
                ("<strong>Binary Authorization</strong> with an attestor that requires an attestation generated by the scan-and-sign pipeline. Unattested or attestation-missing images rejected at admission.", True),
                ("Shielded nodes.", False),
            ],
            feedback="Binary Authorization is the deploy-time signature/attestation enforcement primitive. Policy Controller handles admission rules; BinAuth handles supply-chain trust.",
        ),
    },
    before_after_before='<p>Pre-Workload-Identity-Federation, Pods used either node-SA tokens (over-broad) or downloaded G-SA JSON keys (long-lived, leak-prone). Binary Authorization existed but admission-only; no scan-then-attest pipeline integration. Container threat detection was bring-your-own. Confidential VMs existed but pre-K8s-aware. PSA was bring-your-own. Multi-cluster policy was scripts looping kubectl across contexts.</p>',
    before_after_after='<p>Modern GKE: <strong>Workload Identity Federation</strong> for keyless Pod auth. <strong>Binary Authorization</strong> + <strong>Artifact Registry attestations</strong> = scan-then-attest-then-deploy. <strong>Security Posture</strong> + <strong>Container Threat Detection</strong> in SCC = unified runtime security. <strong>Confidential GKE Nodes</strong> + <strong>Shielded</strong> + <strong>Sandbox</strong> + <strong>CMEK</strong> stack hardware-level guarantees. <strong>Policy Controller + Config Sync</strong> = fleet-wide policy + GitOps admission.</p>',
    before_after_caption='<p class="ba-caption"><em>Each layer is independently meaningful; together they\'re a coherent defendable security story.</em></p>',
    analogy_intro_html='''<p>The <strong>Gatekeeper\'s Lodge</strong> sits at the entrance to the K-Garden, with four shifts working different jobs.</p>
    <p>The <strong>Identity Window</strong> (IAM + WIF for GKE) checks every visitor and every robot worker. Visitors show their photo ID (IAM); robots present a sealed envelope (WIF for GKE federated credential) tied to their work-permit (G-SA). No worker carries a long-lived key — they fetch a fresh one for each task.</p>
    <p>The <strong>Inspection Bench</strong> (Binary Auth + Artifact Registry) inspects every package arriving at the loading dock. Each package must carry an attestation: \"this package was scanned by the Inspector and was clean,\" \"this package was built by the trusted Carpenter.\" Unattested packages are refused at the gate.</p>
    <p>The <strong>Watchtower</strong> (Security Posture + Container Threat Detection) is staffed all hours. The watchman has a checklist (Posture) of \"are all gates locked, are NetworkPolicies set, are CVEs cleared?\" and a binoculars (CTD) for \"that worker is doing something suspicious — they\'re digging up someone else\'s plot.\"</p>
    <p>The <strong>Building Crew</strong> (Shielded / Confidential / Sandbox / CMEK) reinforces the buildings themselves. Some sheds are reinforced concrete (Shielded), some are vault-grade with silicon-level memory encryption (Confidential GKE — AMD SEV / Intel TDX), some are isolation cells for visiting workers whose intentions you don\'t fully trust (Sandbox / gVisor). Every storage room is locked with a key you control (CMEK).</p>''',
    translation_rows=[
        ("Identity Window", "GCP IAM + K8s RBAC + IAM Conditions"),
        ("Worker sealed envelope", "Workload Identity Federation for GKE"),
        ("Worker work-permit (G-SA)", "Google Service Account bound to K8s SA"),
        ("Visitor photo ID", "Human IAM principal"),
        ("\"Only allow ID checks from the corp VPN\"", "IAM Condition (request.attribute scope)"),
        ("Inspection Bench", "Binary Authorization"),
        ("Package attestation", "Artifact Registry attestation (KMS-signed)"),
        ("\"Where packages come from\"", "Artifact Registry remote / virtual repo"),
        ("Door rules", "Policy Controller (managed Gatekeeper)"),
        ("Garden-wide rule book in Git", "Config Sync (GitOps fleet-wide)"),
        ("Watchman\'s checklist", "GKE Security Posture dashboard"),
        ("Watchman\'s binoculars", "Container Threat Detection (in SCC)"),
        ("Vault-grade memory-encrypted shed", "Confidential GKE Node (AMD SEV / Intel TDX)"),
        ("Reinforced shed", "Shielded GKE Node (Secure Boot + vTPM)"),
        ("Untrusted-worker isolation cell", "GKE Sandbox (gVisor)"),
        ("Storage room with your padlock", "CMEK on disks / secrets / images"),
        ("File-based key fetch from the locker", "Secret Manager CSI driver"),
    ],
    analogy_stops="A real Gatekeeper inspects everything; in production, rate-limited inspection + sampling apply. Confidential GKE + Sandbox have measurable performance trade-offs (~5-15% syscall overhead on Sandbox; CPU + boot time on Confidential).",
    eli5="The garden gate has four shifts. One checks IDs. One checks every package coming in. One has binoculars to spot bad behaviour. One reinforces the buildings themselves. Together they protect the garden.",
    eli10="GKE security = four layers. <strong>Identity:</strong> IAM + RBAC + IAM Conditions for humans; Workload Identity Federation for GKE for Pods (no keys). <strong>Supply chain + admission:</strong> Binary Authorization for deploy-time signature/attestation; Artifact Registry scan + remote/virtual; Policy Controller (managed Gatekeeper); Config Sync for fleet-wide GitOps. <strong>Runtime + posture:</strong> Security Posture dashboard; Container Threat Detection (SCC); Secret Manager CSI; PSA Restricted. <strong>Node + hardware:</strong> Shielded nodes (default, Secure Boot + vTPM); Confidential GKE (AMD SEV / Intel TDX); GKE Sandbox (gVisor); CMEK on disks / secrets / images.",
    scenarios=[
        Scenario(
            name="SaaS — WIF + Secret Manager CSI = no secrets in cluster",
            body="A SaaS migrates from baked G-SA JSON keys to Workload Identity Federation. K8s SAs annotated; G-SAs scoped narrowly per workload; Secret Manager secrets mounted via Secret Manager CSI driver with WIF auth. <em>Zero long-lived secrets in cluster; zero key rotations to manage; per-Pod blast radius bounded by G-SA scope.</em>",
        ),
        Scenario(
            name="Bank — Binary Authorization with attest-after-scan pipeline",
            body="Bank pipeline: build → push to Artifact Registry → AR scan → if clean: KMS-signed attestation written → deploy. BinAuth policy: \"only images with attestation from Attestor X may run.\" Unsigned + unattested images rejected at admission. <em>Compliance-clean supply chain; auditable from build to deploy.</em>",
        ),
        Scenario(
            name="Healthcare — Confidential GKE Nodes for PHI training",
            body="ML team trains models on patient data. Confidential GKE node pool (N2D AMD SEV-SNP) for PHI workloads. Memory encrypted at silicon level; Google operators cannot read RAM. External attestation report given to compliance auditor. <em>HIPAA-style requirements met without on-prem.</em>",
        ),
        Scenario(
            name="CI runners — GKE Sandbox prevents CI escape",
            body="A CI platform runs customer-submitted build jobs on GKE. Risk: malicious build escapes container, attacks node. Solution: dedicated node pool with GKE Sandbox (gVisor) — every CI Pod runs in user-space kernel; syscalls mediated. Even a privileged escape stays contained. <em>Performance ~10% slower on syscall-heavy builds; acceptable cost for the isolation.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Binary Authorization is admission control. So is PSA. Same thing.\"",
            truth="Different concerns. <strong>PSA</strong> = K8s-native pod-security baseline (no root, no privilege escalation, no hostPath). <strong>Binary Authorization</strong> = deploy-time enforcement of <em>which images may run</em> (signature / attestation). Combine: PSA enforces what the Pod can do; BinAuth enforces what image is allowed in the first place. Plus Policy Controller for arbitrary admission policies on top.",
        ),
        Misconception(
            myth="\"Workload Identity GKE Pool is the new way to do Pod-to-GCP auth.\"",
            truth="<strong>Workload Identity Federation for GKE</strong> is the current modern path (the federation-based model). The older <em>Workload Identity GKE Pool</em> approach still works in many clusters but the recommended pattern for new clusters is WIF for GKE — uses GCP\'s Workload Identity Federation infrastructure, supports more flexible binding patterns (direct principal, impersonation), aligns with the broader GCP WIF story.",
        ),
        Misconception(
            myth="\"Shielded nodes and Confidential GKE Nodes are the same.\"",
            truth="<strong>Shielded</strong> = Secure Boot + virtual TPM attestation (boot-time integrity). <em>Default for new clusters; no perf cost.</em> <strong>Confidential GKE Nodes</strong> = AMD SEV / Intel TDX silicon memory encryption (data-in-use). <em>Specific SKUs (N2D / C2D etc.); has CPU and boot-time cost.</em> Different threat models; complementary.",
        ),
    ],
    flashcards=[
        Flashcard(front="Two GKE identity surfaces?", back="<strong>Human → cluster:</strong> GCP IAM (with KE Developer/Admin/Viewer) + K8s RBAC (additive) + IAM Conditions for context-aware grants. <strong>Pod → GCP service:</strong> Workload Identity Federation for GKE — K8s SA bound to G-SA; Pod gets short-lived GCP token via metadata server; no secret in cluster."),
        Flashcard(front="What is Binary Authorization (BinAuth)?", back="Deploy-time signature/attestation enforcement. Policy: \"Pods may run only images with an attestation from Attestor X.\" Attestors are KMS-signed pipelines (e.g., scan-then-sign). Unattested images rejected at admission. Foundation of supply-chain security."),
        Flashcard(front="What does Artifact Registry give you beyond \"hold images\"?", back="Continuous vulnerability scanning, remote repos (proxy upstream Docker Hub / GitHub CR), virtual repos (combine sources behind one URL), KMS-signed attestations metadata. Plus CMEK at rest."),
        Flashcard(front="Policy Controller vs Binary Authorization?", back="<strong>Policy Controller</strong> = managed OPA Gatekeeper for arbitrary admission policies (require labels, restrict registries, etc.) — fleet-wide via GKE Enterprise. <strong>BinAuth</strong> = deploy-time enforcement of image trust (signature / attestation). Complementary; use both."),
        Flashcard(front="What is GKE Security Posture dashboard?", back="Continuous evaluation of cluster + workloads against GKE security baseline + CIS K8s Benchmark. Findings: PSA missing, NetworkPolicy missing, CVEs in running images. Integrates with Security Command Center."),
        Flashcard(front="Container Threat Detection (CTD) — what is it part of?", back="Part of <strong>Security Command Center (SCC)</strong>. Runtime threat detection on GKE: suspicious shell-in-container, crypto-miner, lateral movement, K8s TTPs. Alerts ship to SCC + Cloud Logging."),
        Flashcard(front="When use Confidential GKE Nodes?", back="When the workload requires <em>memory encryption with attestation at silicon level</em> — AMD SEV / SEV-SNP or Intel TDX. PHI / financial / regulated workloads where Google operators must not be able to read RAM. Specific SKUs (N2D / C2D); CPU + boot cost."),
        Flashcard(front="What is GKE Sandbox?", back="gVisor user-space kernel runtime for Pods. Stronger isolation than default container runtime; intercepts syscalls. Use for multi-tenant clusters running untrusted workloads (CI runners, customer code). Performance ~5-15% syscall overhead."),
    ],
    quizzes=[
        Quiz(
            prompt="A Pod uses WIF for GKE bound to a G-SA with Storage Object Viewer. Pod returns 403 trying to write a Storage object. The team \"just adds Storage Admin\" to the G-SA. Why is this dangerous, and what\'s the right fix?",
            answer="Storage Admin lets the G-SA delete buckets, change ACLs, etc. — overscoped for one workload that needs to write objects. <strong>Right fix:</strong> grant <em>Storage Object Creator</em> (write) and <em>Storage Object Viewer</em> (read) on the specific bucket only — minimum needed. Use IAM Conditions if you need contextual scoping (e.g., only from this cluster\'s WIF principal). Add Security Posture and CTD alerts on G-SA scope creep so the next over-grant gets flagged.",
        ),
        Quiz(
            prompt="The team enables BinAuth in <em>enforce</em> mode. Suddenly half the deploys fail. What\'s likely going on, and how do you debug?",
            answer="Existing images don\'t have attestations from the configured Attestor. BinAuth rejects them at admission. <strong>Debug:</strong> (1) Check BinAuth audit logs (<code>logName=\"projects/PROJECT/logs/cloudaudit.googleapis.com%2Fdata_access\"</code>) for the rejection reasons. (2) Identify which images need attestations. (3) Either backfill attestations (have your scan-pipeline emit one for each existing-clean image) or temporarily switch BinAuth to <em>dry-run</em> mode (still logs rejections without blocking) while fixing pipelines. <strong>Roll-out pattern:</strong> always enable BinAuth in dry-run first; observe rejections; fix; then enforce. Big-bang enforce = your nightmare.",
        ),
        Quiz(
            prompt="Container Threat Detection alert: a Pod is making outbound calls to a known crypto-miner pool. The Pod\'s WIF-bound G-SA has Storage Object Admin on production data. How do you respond in the next 30 minutes?",
            answer="(1) <strong>Immediate isolation</strong>: kubectl cordon the node + delete the Pod (or scale Deployment to 0). (2) <strong>Revoke trust</strong>: remove the K8s SA <em>annotation</em> that binds it to the G-SA, OR detach the federated credential at the Workload Identity Pool level — no new tokens. (3) <strong>Audit what was accessed</strong>: Storage audit logs filtered to the G-SA; identify object reads/writes during the window. (4) <strong>Rotate any keys/credentials the Pod might have touched</strong>. (5) <strong>Postmortem</strong>: how did the malicious image get past Binary Authorization? Was BinAuth in audit mode? Was the image signed but compromised? Tighten image-scan + attestation pipeline. (6) Re-enable WIF binding only after image is rebuilt + scanned + attested clean.",
            cyoa=True,
            cyoa_tag="how on-call responded in the first 30 minutes",
        ),
    ],
    glossary=[
        GlossaryItem(name="Workload Identity Federation for GKE", definition="Modern Pod-to-GCP auth: K8s SA federated with G-SA via cluster OIDC + WIF Pool. Short-lived tokens; no secrets in cluster."),
        GlossaryItem(name="IAM Conditions", definition="Context-aware IAM grants — scope a role binding by request attribute (network, time, resource tag)."),
        GlossaryItem(name="Binary Authorization", definition="Deploy-time signature/attestation enforcement. Policy gates which images may run via attestor signatures."),
        GlossaryItem(name="Artifact Registry", definition="GCP image + package registry. Scanning, remote / virtual repos, KMS-signed attestations, CMEK."),
        GlossaryItem(name="Policy Controller", definition="Managed OPA Gatekeeper (GKE Enterprise). Fleet-wide admission policies via Constraint templates / Rego / CEL."),
        GlossaryItem(name="Config Sync", definition="Fleet-wide GitOps. RootSync + RepoSync reconcile Git manifests into clusters."),
        GlossaryItem(name="GKE Security Posture", definition="Continuous evaluation against GKE security baseline + CIS K8s Benchmark. Findings actionable in Security Command Center."),
        GlossaryItem(name="Container Threat Detection (CTD)", definition="Runtime threat detection in Security Command Center. Alerts on suspicious behaviour: shell-in-container, crypto-miner, lateral movement."),
        GlossaryItem(name="Secret Manager CSI driver", definition="Mount Secret Manager secrets as files in Pods. WIF-authenticated. Auto-rotation."),
        GlossaryItem(name="Shielded GKE Nodes", definition="Secure Boot + virtual TPM attestation. Default for new clusters. Catches rootkit injection at boot."),
        GlossaryItem(name="Confidential GKE Nodes", definition="AMD SEV / SEV-SNP or Intel TDX silicon memory encryption + attestation. For regulated workloads."),
        GlossaryItem(name="GKE Sandbox", definition="gVisor user-space kernel runtime. Stronger isolation; ~5-15% syscall overhead. For untrusted workloads."),
        GlossaryItem(name="CMEK", definition="Customer-Managed Encryption Keys via Cloud KMS. Encrypt PDs, etcd Secrets, Artifact Registry images at rest."),
    ],
    recap_lead='Four security shifts: identity (IAM + RBAC + WIF for GKE), supply chain + admission (BinAuth + AR + Policy Controller + Config Sync), runtime + posture (Posture + CTD + Secret Manager CSI), node + hardware (Shielded + Confidential + Sandbox + CMEK).',
    recap_next='<strong>Next — G5: GKE Storage.</strong> Persistent Disk CSI (pd-balanced, pd-ssd, Hyperdisk + Storage Pools), Filestore CSI (RWX), GCS FUSE CSI, Parallelstore CSI (HPC/AI), Backup for GKE, snapshots, expansion, VolumeAttributesClass with Hyperdisk.',
)
