"""K-AKS A6 — AKS Security (Defender, Azure Policy, Image Cleaner, FIPS, Confidential Containers, AL2→AL3)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AKS security stack — Defender for Containers, Azure Policy, Image Cleaner, ACR scanning, Workload Identity, FIPS / Confidential Computing.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Campus Police — defence in depth</text>
  <rect x="50" y="60" width="160" height="130" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="130" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">image / supply chain</text>
  <text x="130" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">ACR scanning (Defender)</text>
  <text x="130" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">geo-replication</text>
  <text x="130" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">content trust / signing</text>
  <text x="130" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">Image Cleaner (vulnerable)</text>
  <text x="130" y="170" text-anchor="middle" font-size="8" font-style="italic" fill="#FFFFFF">private ACR + Private Link</text>
  <rect x="225" y="60" width="160" height="130" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="305" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">admission / posture</text>
  <text x="305" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6">Azure Policy (Gatekeeper)</text>
  <text x="305" y="115" text-anchor="middle" font-size="9" fill="#FBF1D6">PSA Restricted</text>
  <text x="305" y="130" text-anchor="middle" font-size="9" fill="#FBF1D6">NetworkPolicy default-deny</text>
  <text x="305" y="145" text-anchor="middle" font-size="9" fill="#FBF1D6">Defender posture findings</text>
  <text x="305" y="170" text-anchor="middle" font-size="8" font-style="italic" fill="#FBF1D6">block before deploy, not after</text>
  <rect x="400" y="60" width="160" height="130" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="480" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">runtime</text>
  <text x="480" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF">Defender runtime watch</text>
  <text x="480" y="115" text-anchor="middle" font-size="9" fill="#FFFFFF">Azure Firewall egress</text>
  <text x="480" y="130" text-anchor="middle" font-size="9" fill="#FFFFFF">Workload Identity (no secrets)</text>
  <text x="480" y="145" text-anchor="middle" font-size="9" fill="#FFFFFF">CloudTrail-equivalent</text>
  <text x="480" y="170" text-anchor="middle" font-size="8" font-style="italic" fill="#FFFFFF">audit + alert</text>
  <rect x="575" y="60" width="135" height="130" rx="10" fill="#E8B547" stroke="#3F4A5E"/>
  <text x="643" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="#5A4F45">node OS / hardware</text>
  <text x="643" y="100" text-anchor="middle" font-size="9" fill="#5A4F45">FIPS pool</text>
  <text x="643" y="115" text-anchor="middle" font-size="9" fill="#5A4F45">host encryption</text>
  <text x="643" y="130" text-anchor="middle" font-size="9" fill="#5A4F45">Trusted Launch</text>
  <text x="643" y="145" text-anchor="middle" font-size="9" fill="#5A4F45">Confidential Containers</text>
  <text x="643" y="158" text-anchor="middle" font-size="9" fill="#5A4F45">(Kata + SEV-SNP)</text>
  <text x="643" y="178" text-anchor="middle" font-size="8" font-style="italic" fill="#5A4F45">AL2 EOL · migrate AL3 / Ubuntu 24</text>
</svg>"""


LESSON = LessonSpec(
    num="06",
    title_short="AKS security",
    title_full="A6 · AKS Security (Defender, Policy, Image Cleaner, FIPS, Confidential Containers)",
    title_html="K-AKS A6 · AKS Security",
    module_eyebrow="Module A6 · Campus Police — defence in depth",
    hero_sub_html='Layered Azure security on top of K8s baselines. <strong>Microsoft Defender for Containers</strong> (image scan + posture + runtime). <strong>Azure Policy for AKS</strong> (Gatekeeper-based admission). <strong>Image Cleaner</strong> for AKS (removes vulnerable images from nodes). <strong>ACR scanning, geo-replication, content trust</strong>. <strong>Workload Identity</strong> + <strong>PSA Restricted</strong> + <strong>NetworkPolicy</strong> + <strong>Azure Firewall</strong>. Hardware-level: <strong>FIPS pools, host encryption, Trusted Launch, Confidential Containers (Kata + AMD SEV-SNP)</strong>. Plus the <strong>Azure Linux 2 → 3 / Ubuntu 24</strong> node OS migration (AL2 EOL 2025-11-30).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"Defender for Containers alert: container running with a CVE-2024-XXXX exploitable vulnerability is making outbound network calls to a known malware C2.\"</em> You realise the image was pulled from a public registry six months ago, hasn\'t been scanned since, and PSA wasn\'t enforced. The Pod has Workload Identity bound to a managed identity with Storage Blob Data Contributor on production data. <em>The blast radius is everything.</em> Today\'s lesson: layered AKS security — image, admission, runtime, OS, hardware.",
    stamp_html="<strong>Defence in depth: Defender (image scan + posture + runtime) + Azure Policy (Gatekeeper admission) + PSA Restricted + NetworkPolicy default-deny + Workload Identity (no secrets) + Azure Firewall egress. Move from Azure Linux 2 to AL3 or Ubuntu 24 before March 2026.</strong>",
    district_pin="kc-wing06",
    district_label="Campus Police",
    sections=[
        Section(
            eyebrow="Section 1.1 · Defender for Containers + ACR",
            h2="Defender for Containers + ACR scanning",
            body_html="""    <p><strong>Microsoft Defender for Containers</strong> is Azure\'s K8s security plan with three pillars:</p>
    <ul>
      <li><strong>Image scanning</strong> — every push to ACR triggers a CVE scan; findings appear in Defender + the ACR portal. <em>Continuous re-scan</em> as new CVEs are published — an image \"clean\" yesterday can be \"vulnerable\" today.</li>
      <li><strong>Posture management</strong> — Defender continuously evaluates the cluster against the CIS Kubernetes Benchmark + Azure security baseline. Findings: \"PSA not enforced in namespace X\", \"NetworkPolicy missing in namespace Y\", \"insecure runtime config Z\". Actionable recommendations in the Defender portal.</li>
      <li><strong>Runtime threat detection</strong> — Defender agents on each node watch for known malicious behaviours (suspicious shell-in-container, crypto-miner, lateral movement, Kubernetes-specific TTPs). Alerts ship to Sentinel.</li>
    </ul>
    <p><strong>ACR (Azure Container Registry):</strong>
    <ul>
      <li><strong>Geo-replication</strong> — replicate the registry across regions; Pods pull from the nearest replica.</li>
      <li><strong>Content trust / image signing</strong> — sign images with Notation or Cosign; verify signatures via admission policy (e.g. Azure Policy + Notation Verifier or Kyverno).</li>
      <li><strong>Private ACR</strong> — disable public endpoint, expose via Private Link, attach Private DNS.</li>
    </ul>"""
        ),
        Section(
            eyebrow="Section 1.2 · Azure Policy + PSA + Image Cleaner",
            h2="Azure Policy + PSA + Image Cleaner — admission and posture",
            body_html="""    <p><strong>Azure Policy for AKS</strong> = Microsoft\'s implementation of <strong>OPA Gatekeeper</strong> packaged as an AKS add-on. Built-in initiative <em>\"Kubernetes cluster pod security baseline / restricted standards\"</em> ships hundreds of admission policies. <em>Effect choice</em>: Audit (log only) or Deny (block at admission). Custom Constraints / ConstraintTemplates supported.</p>
    <p><strong>Pod Security Admission (PSA)</strong> — K8s\'s built-in replacement for PodSecurityPolicy. Three levels: <em>Privileged / Baseline / Restricted</em>. Apply via namespace labels: <code>pod-security.kubernetes.io/enforce: restricted</code>. Restricted is production default — runs as non-root, no privileged escalation, drops all capabilities, seccomp RuntimeDefault.</p>
    <p><strong>Image Cleaner for AKS</strong> — DaemonSet that scans node disks for unused or vulnerable images and removes them. <em>Reduces lateral movement risk</em> (an attacker landing on a node can\'t use a stale vulnerable image to pivot). Configure scan schedule + CVE severity threshold.</p>
    <p><strong>NetworkPolicy default-deny</strong> per namespace + explicit allow lists per service is the standard hardening posture (covered in A3).</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · runtime + identity + egress",
            h2="Runtime + Workload Identity + Azure Firewall",
            body_html="""    <p><strong>Workload Identity</strong> (covered in A2) is the security baseline for Pod auth — <em>no long-lived secrets in cluster</em>. Combined with managed identities scoped narrowly (least privilege per workload), the blast radius of a compromised Pod is bounded by what its MI can do.</p>
    <p><strong>Azure Firewall</strong> (or <strong>Azure Firewall Premium</strong> for IDPS + TLS inspection) sits between the cluster\'s VNet and the internet. <em>Egress filtering</em>: an FQDN allow-list of permitted destinations (Microsoft Graph, ACR, Key Vault, your own APIs); everything else denied. Catches data exfiltration attempts at the network layer. Pair with NetworkPolicy for in-cluster east-west.</p>
    <p><strong>CloudTrail equivalent</strong>: <strong>Azure Activity Log</strong> + <strong>Defender alerts</strong> + <strong>Diagnostic Settings → Log Analytics</strong>. Every <code>az aks ...</code> change is in Activity Log; every kubectl-as-Entra-principal call is in apiserver audit logs (turn on diagnostic settings to forward to Log Analytics).</p>
    <p><strong>Private cluster + private ACR + private Key Vault</strong> = no public endpoints across the cluster\'s adjacent surface. Combined with Conditional Access on the management plane, this is the modern \"locked-down enterprise AKS\" topology.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · node OS + hardware",
            h2="Node OS + hardware — FIPS, Confidential, Trusted Launch, AL2→AL3",
            body_html="""    <p><strong>FIPS node pools</strong> — node OS configured for FIPS 140-2 cryptography (SHA-256+, AES-256, etc.). Required for some US federal compliance contexts. Per-pool flag at create time.</p>
    <p><strong>Host encryption</strong> — encrypts node OS + temp disks with platform-managed or customer-managed (CMK via Key Vault HSM) keys. On by default for new clusters; verify on existing.</p>
    <p><strong>Trusted Launch VMs</strong> — secure boot + virtual TPM (vTPM) attestation. Default for new node pools on supported SKUs. Catches rootkit injection at boot.</p>
    <p><strong>Confidential Containers</strong> — Kata Containers runtime + AMD SEV-SNP. Each Pod runs in a hardware-encrypted utility VM with attestation. <em>Memory encrypted at the silicon level — even Azure host operators can\'t read it.</em> For regulated workloads (PII / financial / health).</p>
    <p><strong>Node OS migration — Azure Linux 2 → AL3 / Ubuntu 24:</strong> <em>Azure Linux 2.0 reached end of support 2025-11-30; node images are removed from 2026-03-31.</em> Every AKS node currently on AL2 must migrate. Pick path: <strong>Azure Linux 3</strong> (Microsoft\'s newer optimised distro; same family) or <strong>Ubuntu 24</strong> (broader ecosystem, broader 3rd-party agent support). Migration = create new pool with target OS SKU, drain workloads from old pool, delete old pool. Cannot change OS SKU in place.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="Defender for Containers flags an image with a critical CVE running in production. Image was pushed three months ago and not re-scanned since then. What\'s the modern AKS pattern that prevents this?",
            options=[
                ("Manually scan with trivy weekly.", False),
                ("Enable Defender for Containers with continuous re-scan + Image Cleaner add-on + admission policy that blocks images above a CVE severity threshold.", True),
                ("Block all image pulls.", False),
            ],
            feedback="Defender re-scans continuously as new CVEs publish; Image Cleaner removes vulnerable images from node disks; admission policy blocks new deploys above the threshold. Defence in depth, not a single scanner.",
        ),
    },
    before_after_before='<p>Pre-Defender AKS = patchwork. CVE scans by self-installed Trivy or Anchore. PodSecurityPolicy was the admission tool — deprecated 2021. Image Cleaner didn\'t exist; nodes accumulated vulnerable images for months. NetworkPolicy installation was bring-your-own. Egress filtering = open. <em>Three different scanners, two different audit log destinations, zero correlation.</em> Plus Azure Linux didn\'t exist; Ubuntu 18 was reaching EOL with no managed migration story.</p>',
    before_after_after='<p>Modern AKS ships <strong>Defender for Containers</strong> (image + posture + runtime, single pane), <strong>Azure Policy for AKS</strong> (Gatekeeper admission with built-in baseline), <strong>Image Cleaner</strong>, <strong>PSA Restricted</strong> as the production default, <strong>Workload Identity</strong> (no cluster secrets), <strong>Azure Firewall</strong> for egress, <strong>FIPS / Confidential Containers / Trusted Launch</strong> for hardware-level guarantees. Plus <strong>Azure Linux 3</strong> as the optimised, well-maintained node OS path forward.</p>',
    before_after_caption='<p class="ba-caption"><em>Security in AKS is now coherent — one console (Defender), one admission framework (Azure Policy), one identity model (Workload Identity), one egress controller (Azure Firewall).</em></p>',
    analogy_intro_html='''<p><strong>Campus Police</strong> on K-Campus runs four shifts.</p>
    <p>The <strong>Mailroom Shift</strong> (image / supply chain) inspects every box arriving at the loading dock — scans for contraband CVEs, refuses unsigned packages, replicates the safe ones to satellite mailrooms (geo-replication). The mailroom keeps a continuously updated list of \"recalled items\" (new CVEs) and pulls them off shelves automatically (Image Cleaner).</p>
    <p>The <strong>Door Shift</strong> (admission / posture) checks every guest at every building door — Azure Policy / Gatekeeper says \"this guest is wearing the wrong badge, denied,\" or \"this guest needs PSA Restricted clearance.\" Posture inspectors walk the buildings continuously checking that locks are engaged, fire doors closed, NetworkPolicy default-deny present.</p>
    <p>The <strong>Patrol Shift</strong> (runtime + identity + egress) watches what happens inside. Defender runtime agents look for unusual behaviour. Workload Identity means no master keys are stashed in offices — every worker gets a fresh permit. Azure Firewall guards the only road off campus — only addresses on the allow-list get out.</p>
    <p>The <strong>Building Shift</strong> (node OS + hardware) maintains the buildings themselves. Some buildings are reinforced concrete (FIPS pools), some are vault-grade (Confidential Containers — silicon-encrypted memory), all have tamper-evident seals (Trusted Launch). Plus there\'s a notice on every Azure Linux 2 building: <em>\"this building closes 2026-03-31; move to Azure Linux 3 or Ubuntu 24.\"</em></p>''',
    translation_rows=[
        ("Mailroom inspectors", "ACR + Defender image scanning"),
        ("Recalled-items list", "Continuous CVE re-scan"),
        ("Mailroom shelf-purge", "Image Cleaner add-on"),
        ("Sealed package signature check", "Cosign / Notation + admission verifier"),
        ("Mailroom satellites", "ACR geo-replication"),
        ("Door checker", "Azure Policy for AKS (Gatekeeper)"),
        ("Restricted-clearance guests", "PSA Restricted standard"),
        ("Posture inspector walks", "Defender posture management"),
        ("Patrol agents", "Defender runtime threat detection"),
        ("No master keys in offices", "Workload Identity (no long-lived secrets)"),
        ("Single road off campus + allow-list", "Azure Firewall egress filtering"),
        ("Reinforced-concrete buildings", "FIPS node pools"),
        ("Vault-grade memory-encrypted offices", "Confidential Containers (Kata + AMD SEV-SNP)"),
        ("Tamper-evident door seals", "Trusted Launch (secure boot + vTPM)"),
        ("\"Building closes 2026-03-31\" notice", "Azure Linux 2 EOL migration"),
    ],
    analogy_stops="A real Campus Police force can\'t look inside encrypted memory; Confidential Containers can be inspected by their own attestation reports but not by external observers — the metaphor of \"vault-grade\" is closer to literal in this case.",
    eli5="Police on campus do four jobs: check what arrives in the mail (boxes), check who comes through doors (guests), watch what happens in buildings (cameras), and keep the buildings strong (locks, walls). Same with AKS — image scans, admission rules, runtime watching, hardware security.",
    eli10="AKS security is layered. <strong>Image:</strong> Defender + ACR scanning + content trust + Image Cleaner; private ACR for isolation. <strong>Admission/posture:</strong> Azure Policy (Gatekeeper) + PSA Restricted + NetworkPolicy default-deny + Defender posture findings. <strong>Runtime:</strong> Defender runtime detection + Workload Identity (no secrets) + Azure Firewall egress + apiserver audit to Log Analytics. <strong>Node OS / hardware:</strong> FIPS pools, host encryption, Trusted Launch (secure boot + vTPM), Confidential Containers (Kata + AMD SEV-SNP). Migrate Azure Linux 2 → AL3 or Ubuntu 24 by 2026-03-31 (AL2 node images removed).",
    scenarios=[
        Scenario(
            name="Bank — Defender + private ACR + signed images",
            body="A bank requires every production image to be signed (Cosign) and scanned (Defender). Pipeline: Build → push to private ACR → Defender scans → if 0 critical CVEs, Cosign signs → admission verifier (Azure Policy with custom Constraint) blocks unsigned or vulnerable images at deploy. Bank also enables continuous re-scan; Image Cleaner removes anything that becomes vulnerable post-deploy. <em>Compliance audit: zero exception in 6 months.</em>",
        ),
        Scenario(
            name="SaaS — PSA Restricted across all namespaces in one quarter",
            body="A SaaS has 200 microservices that historically ran as root with privileged: true. Q1 plan: enable PSA Audit on all namespaces (no breakage; just findings); per service, fix root + capability + seccomp violations; flip to PSA Warn (informs developers); finally PSA Enforce. <em>Q1 end: every namespace at PSA Restricted; zero deployment-time surprises in Q2.</em>",
        ),
        Scenario(
            name="Healthcare — Confidential Containers for PHI workloads",
            body="A healthcare ML team trains models on patient data. Compliance requires in-use memory encryption. They add a Confidential Containers node pool (DCasv5, AMD SEV-SNP). PHI-handling Pods are scheduled to that pool via toleration + nodeSelector. Each Pod runs in a Kata utility VM with hardware-encrypted RAM and attestation. <em>External attestation report given to compliance auditor; audit clears on first review.</em>",
        ),
        Scenario(
            name="Migration — Azure Linux 2 to Ubuntu 24 across 12 clusters",
            body="A platform team has 12 clusters with mixed AL2 / Ubuntu 22 pools. Azure Linux 2 EOL 2025-11-30; node images removed 2026-03-31. Plan: per cluster, create new Ubuntu 24 pool alongside AL2 pool; drain workloads with PDB safety; delete AL2 pool. Two-week sprint per cluster; finished by Feb 2026 with one-month buffer. <em>No outages; one cluster needed an Ubuntu 24 driver fix for an obscure GPU SKU; otherwise smooth.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"PSA replaces Azure Policy / Gatekeeper.\"",
            truth="They\'re complementary. <strong>PSA</strong> = K8s-native, baseline Pod-security checks (root, capabilities, hostPath, etc.) at three levels. <strong>Azure Policy / Gatekeeper</strong> = arbitrary admission policies (image registry allowlist, label requirements, NetworkPolicy presence, etc.). PSA covers Pod-security baseline; Azure Policy covers everything else.",
        ),
        Misconception(
            myth="\"My image was scanned at build time, so it\'s safe.\"",
            truth="A new CVE published yesterday makes yesterday\'s \"clean\" image vulnerable today. Defender for Containers does <strong>continuous re-scan</strong> as the CVE feed updates. Image Cleaner pulls vulnerable images off node disks. Build-time scan is necessary but not sufficient.",
        ),
        Misconception(
            myth="\"My Workload Identity-bound MI is small-scope; an attacker compromising a Pod can\'t do much.\"",
            truth="Verify the MI scope is actually small. Common drift: MI was created with one permission, expanded over time as new features were added, never re-pruned. Defender posture flags over-privileged identities; review quarterly. Combine WI scoping with PSA Restricted (limits what the Pod itself can do on the node) + NetworkPolicy default-deny (limits lateral movement) + Azure Firewall (limits egress to known endpoints).",
        ),
    ],
    flashcards=[
        Flashcard(front="Three pillars of Defender for Containers?", back="<strong>Image scanning</strong> (continuous CVE scan in ACR), <strong>Posture management</strong> (CIS K8s + Azure baseline findings), <strong>Runtime threat detection</strong> (suspicious behaviour alerts via node agents). All visible in one Defender pane; alerts ship to Sentinel."),
        Flashcard(front="What is Azure Policy for AKS?", back="Microsoft\'s packaging of OPA Gatekeeper as an AKS add-on. Built-in initiatives include <em>Kubernetes pod security baseline / restricted standards</em>. Effect = Audit (log) or Deny (block). Supports custom ConstraintTemplates."),
        Flashcard(front="Three PSA levels?", back="<strong>Privileged</strong> (no restrictions — pre-existing workloads), <strong>Baseline</strong> (no known privilege escalation paths), <strong>Restricted</strong> (production default — non-root, no privileged escalation, drop all capabilities, seccomp RuntimeDefault). Apply via namespace label <code>pod-security.kubernetes.io/enforce: restricted</code>."),
        Flashcard(front="What does Image Cleaner for AKS do?", back="DaemonSet that scans node disks for unused or vulnerable images, removes them. Reduces lateral movement (attacker on a node can\'t use a stale vulnerable image to pivot). Configure scan interval + CVE severity threshold."),
        Flashcard(front="When are FIPS node pools required?", back="When the workload must use FIPS 140-2 validated cryptography — typically US federal contracts. Per-pool flag at creation. Workloads that don\'t need FIPS run on regular pools to avoid the FIPS performance overhead."),
        Flashcard(front="Confidential Containers on AKS — what hardware + runtime?", back="<strong>Kata Containers</strong> runtime (Pod runs in a utility VM, not the host kernel) + <strong>AMD SEV-SNP</strong> (memory encryption + attestation). DCasv5 / ECasv5 SKUs. Each Pod\'s memory encrypted at silicon level — invisible to Azure operators."),
        Flashcard(front="What is the AL2 → AL3 / Ubuntu 24 deadline?", back="<strong>Azure Linux 2.0 reached end of support 2025-11-30; node images removed 2026-03-31.</strong> Every AKS node currently on AL2 must migrate to <strong>Azure Linux 3</strong> or <strong>Ubuntu 24</strong> via new pools (OS SKU is immutable on existing pools)."),
        Flashcard(front="Why use Azure Firewall for AKS egress?", back="FQDN-based allow-list of permitted destinations (Microsoft Graph, ACR, Key Vault, your APIs); everything else denied at L7. Catches data exfiltration at the network layer. Premium tier adds IDPS + TLS inspection. Pair with in-cluster NetworkPolicy."),
    ],
    quizzes=[
        Quiz(
            prompt="The team enables PSA Restricted on the prod namespace. Half the deployments fail to start. What went wrong, and what\'s the recovery path?",
            answer="Restricted bans: running as root, allowPrivilegeEscalation, dropping all capabilities, hostPath mounts, hostNetwork, etc. Existing workloads written without these constraints fail at admission. <strong>Recovery</strong>: temporarily move to <code>pod-security.kubernetes.io/enforce: privileged</code> (or <code>baseline</code>) to restore service; concurrently set <code>pod-security.kubernetes.io/audit: restricted</code> + <code>warn: restricted</code> to surface every violation; fix workloads one at a time (drop runAsRoot, drop hostPath, declare seccompProfile, etc.); flip back to enforce: restricted when all pass.",
        ),
        Quiz(
            prompt="You enabled Defender continuous re-scan. Three days later, an image deployed last month is suddenly flagged as having a critical CVE. The Pod is still running. What does Image Cleaner do, and what should the team do?",
            answer="<strong>Image Cleaner</strong> (if enabled with appropriate severity threshold) detects the now-vulnerable image on node disks and removes it. The <em>running Pod is not killed</em> — Image Cleaner doesn\'t evict; it just stops the image from being available for new Pod starts. Team action: identify the upstream image fix (vendor patch, base image rebuild), bump the image tag, redeploy. Until then, the running Pod is exposed — Defender alert + admission policy preventing new deploys of the bad tag is the bridge.",
        ),
        Quiz(
            prompt="It\'s February 2026. An on-call engineer is paged: <em>\"All AKS nodes in the cluster failed to start — node image not found.\"</em> What happened, and what\'s the immediate fix?",
            answer="<strong>Azure Linux 2 node images were removed on 2026-03-31</strong> — wait, the date matches. The team didn\'t migrate. Nodes that need to scale or replace are now stuck because AL2 image is gone. <strong>Immediate fix</strong>: create a new node pool with <code>--os-sku AzureLinux</code> (which now resolves to AL3) or <code>--os-sku Ubuntu</code> (24); drain workloads from the dead AL2 pool to the new pool; delete the AL2 pool. Long-term fix: same migration but planned, with PDB safety + a dry-run, not at 3 AM. The takeaway: deprecation deadlines are real outage events.",
            cyoa=True,
            cyoa_tag="why a deprecation date matters",
        ),
    ],
    glossary=[
        GlossaryItem(name="Microsoft Defender for Containers", definition="Azure security plan: image scanning + posture + runtime threat detection. Single pane in the Defender portal."),
        GlossaryItem(name="Azure Policy for AKS", definition="Microsoft\'s packaging of OPA Gatekeeper. Admission and posture policies. Built-in baseline / restricted initiatives."),
        GlossaryItem(name="Pod Security Admission (PSA)", definition="K8s-native replacement for PodSecurityPolicy. Three levels: privileged / baseline / restricted. Apply via namespace label."),
        GlossaryItem(name="Image Cleaner for AKS", definition="DaemonSet that removes unused / vulnerable images from node disks. Reduces lateral-movement risk."),
        GlossaryItem(name="ACR content trust", definition="Sign images on push (Cosign / Notation); verify signatures at admission via custom Azure Policy / Kyverno."),
        GlossaryItem(name="ACR geo-replication", definition="Replicate registry across regions. Pods pull from nearest replica."),
        GlossaryItem(name="Azure Firewall (Premium)", definition="L7 egress controller in front of the cluster VNet. FQDN allow-list; Premium adds IDPS + TLS inspection."),
        GlossaryItem(name="FIPS node pool", definition="Node OS configured for FIPS 140-2 cryptography. Required for some US federal compliance."),
        GlossaryItem(name="Trusted Launch", definition="Secure boot + virtual TPM (vTPM) attestation for AKS nodes. Catches rootkit injection at boot."),
        GlossaryItem(name="Confidential Containers", definition="Kata Containers + AMD SEV-SNP. Per-Pod hardware-encrypted memory + attestation. For regulated workloads."),
        GlossaryItem(name="Host encryption", definition="Encrypts node OS + temp disks at rest. Platform-managed or CMK via Key Vault HSM."),
        GlossaryItem(name="Azure Linux 3", definition="Microsoft\'s current optimised AKS node OS. Successor to Azure Linux 2 (EOL 2025-11-30)."),
    ],
    recap_lead='Four security shifts: image (Defender + ACR + Image Cleaner), admission/posture (Azure Policy + PSA), runtime (Defender + WI + Azure Firewall), node OS / hardware (FIPS + Confidential + Trusted Launch + AL3 migration).',
    recap_next='<strong>Next — A7: AKS Observability.</strong> Azure Monitor managed Prometheus + Managed Grafana, Container Insights with Log Analytics + KQL, Application Insights for app traces, Azure Monitor managed OpenTelemetry, control-plane diagnostic settings, Network Observability, Cost Management.',
)
