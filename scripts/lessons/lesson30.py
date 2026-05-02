from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Bank vault interior: a chain of artefacts (source → SLSA build → signed image + SBOM + attestation) with a Sigstore notary stamping each step.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">BANK VAULT QUARTER · SUPPLY-CHAIN LEDGER</text>
  <!-- Source -->
  <g transform="translate(40,80)"><rect width="80" height="60" rx="6" fill="#5A9F7A"/><text x="40" y="28" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">source</text><text x="40" y="42" text-anchor="middle" font-size="7" fill="#FFFFFF">git commit</text><text x="40" y="52" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">signed</text></g>
  <line x1="125" y1="110" x2="155" y2="110" stroke="#A04832" stroke-width="2" marker-end="url(#a4)"/>
  <defs><marker id="a4" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#A04832"/></marker></defs>
  <!-- Build -->
  <g transform="translate(160,70)"><rect width="120" height="80" rx="6" fill="#3F4A5E"/><text x="60" y="20" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">SLSA build</text><text x="60" y="38" text-anchor="middle" font-size="7" fill="#FBF1D6">hermetic · reproducible</text><text x="60" y="52" text-anchor="middle" font-size="7" fill="#FBF1D6">level 3 isolated runner</text><text x="60" y="68" text-anchor="middle" font-size="7" fill="#E8B547" font-style="italic">provenance attestation</text></g>
  <line x1="285" y1="110" x2="315" y2="110" stroke="#A04832" stroke-width="2" marker-end="url(#a4)"/>
  <!-- Image + SBOM + Attestation -->
  <g transform="translate(320,55)"><rect width="180" height="110" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/><text x="90" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">REGISTRY</text>
    <rect x="14" y="22" width="152" height="22" rx="2" fill="#FBF1D6" stroke="#8B5A00" stroke-width="1"/>
    <text x="20" y="37" font-size="8" fill="#8B5A00" font-weight="700">image · sha256:abc...</text>
    <rect x="14" y="48" width="152" height="22" rx="2" fill="#E0EFE6" stroke="#3D7857" stroke-width="1"/>
    <text x="20" y="63" font-size="8" fill="#3D7857" font-weight="700">SBOM · SPDX / CycloneDX</text>
    <rect x="14" y="74" width="152" height="22" rx="2" fill="#FBE8DC" stroke="#A04832" stroke-width="1"/>
    <text x="20" y="89" font-size="8" fill="#A04832" font-weight="700">cosign signature</text>
  </g>
  <line x1="505" y1="110" x2="535" y2="110" stroke="#A04832" stroke-width="2" marker-end="url(#a4)"/>
  <!-- K8s -->
  <g transform="translate(540,80)"><rect width="100" height="60" rx="6" fill="#A04832"/><text x="50" y="28" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">K8s admit</text><text x="50" y="42" text-anchor="middle" font-size="7" fill="#FFFFFF">verifyImages</text><text x="50" y="52" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">policy reject</text></g>
  <text x="340" y="200" text-anchor="middle" font-size="11" fill="#3F4A5E" font-style="italic">From git commit to running Pod, every step leaves a verifiable receipt. The cluster\'s admission gate refuses unsigned receipts.</text>
</svg>"""

LESSON = LessonSpec(
    num="30",
    title_short="supply chain",
    title_full="Supply Chain Security · Cosign, Sigstore, SLSA, SBOM",
    title_html="Lesson 30 — Supply Chain Security · K-COM",
    module_eyebrow="Module 13 · Lesson 30 · what an image actually is, and how to trust it",
    hero_sub_html='\"Container image\" feels like a single thing. It\'s actually a <strong>chain of artefacts</strong> — source code, build provenance, the image itself, an SBOM, signatures. Each link can be tampered with. Modern supply-chain security signs each link and verifies the whole chain at admission. The toolkit: <strong>Sigstore + Cosign</strong> (signing), <strong>SLSA</strong> (build provenance), <strong>SBOMs</strong> (component inventory).',
    hero_illu_svg=HERO_SVG,
    nightmare_html='2024 — XZ Utils backdoor. A maintainer added obfuscated malicious code to a fundamental Linux library, hiding it through years of trusted contributions. Caught by accident days before stable Linux distros would have shipped it. The lesson the industry took: <em>code provenance is necessary but not sufficient — every artefact in the chain needs to be signed, scanned, and verified at admission</em>. K8s clusters that did supply-chain right caught the issue before it ran. Clusters that did \"pin tags + trust upstream\" were vulnerable. This lesson is the toolkit that gets you to the first column.',
    stamp_html='Three artefacts plus signing: <strong>SBOM</strong> (Software Bill of Materials — what\'s in the image), <strong>SLSA provenance</strong> (how the image was built, attested), <strong>Cosign signature</strong> (the artefact is authentic). All stored alongside the image in the OCI registry. Admission verifies the chain via <code>cosign verify</code> or Kyverno <code>verifyImages</code>.',
    district_pin="kt-pin11",
    district_label="Bank Vault Quarter — Trust Ledger",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="What\'s in an image, and what can go wrong",
            body_html="""    <p>A container image (Lesson 9-11) is a stack of layers + manifest. The chain that produced it has many places to inject something malicious:</p>
    <ul>
      <li><strong>Source</strong> — git commits. A compromised maintainer commits malicious code.</li>
      <li><strong>Build environment</strong> — the runner. Someone with access to the CI runner can swap in a different binary.</li>
      <li><strong>Dependencies</strong> — npm/pip/Maven packages pulled at build time. A typosquatted package replaces a legitimate one.</li>
      <li><strong>Image registry</strong> — push/pull. Tag mutability means \"<code>nginx:1.21</code>\" today can mean a different image tomorrow.</li>
      <li><strong>Pull at runtime</strong> — registry → kubelet. MITM, registry compromise.</li>
    </ul>
    <p>Each link in this chain needs a verifiable receipt. The modern toolkit signs each artefact (image, SBOM, attestations) with a key the cluster trusts, and admission policies verify before running.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Sigstore + Cosign",
            h2="Signing made boring",
            body_html="""    <p><strong>Sigstore</strong> is a CNCF project that made signing artefacts simple. Three pieces:</p>
    <ul>
      <li><strong>Cosign</strong> — CLI for signing/verifying container images, blobs, attestations.</li>
      <li><strong>Fulcio</strong> — short-lived certificate authority that issues x.509 certs tied to OIDC identities (your GitHub Actions OIDC token, corp SSO token, etc.). \"Keyless signing\" — no key file to manage.</li>
      <li><strong>Rekor</strong> — public tamper-evident log of every signing event. Auditable. Append-only.</li>
    </ul>
    <p>The keyless flow:</p>
    <ol>
      <li>CI obtains an OIDC token (e.g., from GitHub Actions).</li>
      <li>Fulcio exchanges it for a short-lived cert tied to the workflow identity.</li>
      <li>Cosign signs the image; signature + cert + transparency log entry stored in the OCI registry alongside the image.</li>
      <li>K8s admission verifies the cert chain + the workflow identity matches expectations.</li>
    </ol>
    <p>No long-lived signing keys to rotate. No HSM to manage. The OIDC identity (\"this image was signed by GitHub Actions on behalf of org/repo, branch main, workflow X\") is the trust root.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · SLSA — provenance levels",
            h2="A grading system for build supply chains",
            body_html="""    <p><strong>SLSA</strong> (Supply-chain Levels for Software Artifacts; pronounced \"salsa\") is a graded standard from OpenSSF. It defines build-process maturity from level 0 (\"we don\'t know how this was built\") to level 4 (\"hermetic, reproducible, two-person reviewed\"). The output of a SLSA-compliant build is an attestation describing:</p>
    <ul>
      <li>The exact source repo + commit.</li>
      <li>The exact build steps + environment.</li>
      <li>The exact dependencies pulled.</li>
      <li>Who triggered the build (identity).</li>
    </ul>
    <p>The attestation is itself a signed artefact in the OCI registry. SLSA Level 3 (the realistic target for most orgs) requires:</p>
    <ul>
      <li>Build runs on an isolated, ephemeral environment (typical CI runner).</li>
      <li>Provenance is generated by the build platform (not user code).</li>
      <li>Provenance is signed.</li>
      <li>Source platform is trusted (GitHub, GitLab, etc.).</li>
    </ul>
    <p>GitHub Actions gained native SLSA L3 provenance generation in 2023. Buildah and BuildKit support it. The major cloud build services (Cloud Build, AWS CodeBuild) support attestation export.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · SBOMs and admission verification",
            h2="What\'s actually in the image",
            body_html="""    <p>An <strong>SBOM</strong> (Software Bill of Materials) lists every package + version inside an image. Two main formats: <strong>SPDX</strong> (Linux Foundation) and <strong>CycloneDX</strong> (OWASP). Both are JSON; both are widely tooled.</p>
    <p>Generated at build time by tools like <strong>Syft</strong> (Anchore) or <strong>Trivy</strong>. Stored as an attestation in the registry. Used downstream by:</p>
    <ul>
      <li><strong>Vulnerability scanners</strong> — Trivy, Grype consume SBOMs to flag known CVEs without re-scanning the image.</li>
      <li><strong>License compliance</strong> — \"does any package have a license we can\'t use?\"</li>
      <li><strong>Forensics</strong> — \"after the log4j CVE, which images contain a vulnerable version?\" SBOM lookup, not code reading.</li>
    </ul>
    <p>The complete admission policy looks like:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># Kyverno verifyImages (simplified)
- imageReferences: [\"prod-registry.corp/*\"]
  attestations:
  - type: https://slsa.dev/provenance/v1
    attestors: [{keys: {publicKeys: \"...\"}}]
    conditions: [{key: \"buildType\", operator: Equals, value: \"github-actions-slsa3\"}]
  - type: https://cyclonedx.org/bom
    attestors: [{keys: {publicKeys: \"...\"}}]
  attestors:
  - entries: [{keyless: {issuer: \"https://token.actions.githubusercontent.com\", subject: \"https://github.com/myorg/.*\"}}]</code></pre>
    <p>This says: image must be from prod-registry, must have a SLSA L3 attestation from our CI, must have a CycloneDX SBOM, and the image must be signed by a Fulcio cert from our GitHub org. Every link in the chain verified at admission.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A team uses Cosign keyless signing in GitHub Actions. The signature in the registry has a Fulcio-issued cert. What\'s the trust root?",
            options=[
                ("a) A static signing key managed by the team", False),
                ("b) The OIDC identity asserted at signing time (e.g., the GitHub Actions workflow), validated against the cert", True),
                ("c) Sigstore\'s Rekor log alone", False),
            ],
            feedback="<strong>Answer: b.</strong> Keyless signing\'s trust root is the OIDC identity. The Fulcio cert binds the signature to the identity (\"this signature was created during the GitHub Actions run for repo X, branch Y\"). Verification at admission checks that identity matches expectations. Rekor adds tamper-evidence on top.",
        ),
    },
    before_after_before='<p>Old practice: pin <code>nginx:1.21</code>, hope upstream is honest, scan with Trivy nightly, react when CVE drops. \"Trust\" was a mix of a registry password + a tag string. SBOMs were a wishful spreadsheet. Build provenance was the assumption that GitHub\'s CI ran what was committed.</p>',
    before_after_after='<p>Modern: pin by digest (<code>sha256:abc...</code>), verify a Fulcio-signed cert tying the image to a specific OIDC identity, verify a SLSA L3 provenance attestation describing the build, verify an SBOM attestation, all at admission. Tag mutability is irrelevant. Compromise of a registry doesn\'t bypass admission. Compromise of a maintainer triggers a verification mismatch.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">XZ Utils 2024 was the wake-up call. The industry is moving from \"trust the registry\" to \"verify each artefact in the chain.\" Sigstore + SLSA is the toolkit; admission policies are the enforcement.</p>',
    analogy_intro_html='<p>Bank Vault Quarter holds K-Town\'s ledgers. Every package coming into the city has a paper trail. A signed <strong>declaration of origin</strong> (Cosign signature) — \"this came from this CI workflow on this date.\" A <strong>build manifest</strong> (SLSA provenance attestation) — \"these are the steps used to produce it; here\'s the runner identity that signed off.\" A <strong>contents inventory</strong> (SBOM) — \"the package contains these specific component versions.\" All stamped by a <strong>notary</strong> (Sigstore / Fulcio) whose stamps are themselves logged in a public ledger (Rekor) that nobody can edit retroactively. At the city gate (K8s admission), an inspector checks every package\'s paper trail against the city\'s allow-list. No paper trail = denied entry.</p>',
    translation_rows=[
        ("Declaration of origin", "Cosign signature"),
        ("The notary stamping declarations", "Sigstore / Fulcio"),
        ("The public ledger of stamps", "Rekor transparency log"),
        ("Build manifest", "SLSA provenance attestation"),
        ("\"Built by this runner identity\"", "OIDC subject in the keyless cert"),
        ("Contents inventory", "SBOM (SPDX or CycloneDX)"),
        ("Inspector at the city gate", "Admission policy (Kyverno verifyImages)"),
        ("Pinning by package weight, not name", "Pinning by digest, not tag"),
    ],
    analogy_stops="The analogy stops here: Sigstore notarisation is cryptographic, not paper. The trust root is OIDC + Rekor\'s tamper-evidence; if either is compromised, signatures can\'t be trusted. Pin to a known Rekor log entry for full assurance.",
    eli5='Every box that comes to the door needs three notes: who packed it, what\'s in it, and a stamp from the city. The doorman won\'t let in a box with missing notes.',
    eli10="Three artefacts per image: <strong>signature</strong> (Cosign — image is authentic, signed by a known identity), <strong>SLSA provenance attestation</strong> (build process is trusted), <strong>SBOM</strong> (what\'s in the image — packages, versions). Sigstore makes signing keyless via short-lived OIDC-derived certs. Rekor logs every signing event in a tamper-evident ledger. At admission, Kyverno (or similar) verifies the whole chain. Pin by digest, not tag.",
    scenarios=[
        Scenario(name="A SaaS shipping production with full chain", body="GitHub Actions builds + signs images via Cosign keyless. SLSA L3 provenance generated by the GitHub-provided action. Syft generates CycloneDX SBOM and uploads as OCI attestation. Kyverno verifyImages policy checks signature + provenance + SBOM presence. Attempt to deploy a hand-built image fails admission. Verifies the workflow that signed it."),
        Scenario(name="A bank doing forensic SBOM lookups", body="When CVE drops, query <code>cosign download attestation --predicate-type cyclonedx ...</code> for every running image. JSON parse against the SBOM, find affected ones in seconds. Pre-SBOM equivalent: re-scan every image with Trivy, hours of work. Reduces incident MTTR for known CVEs from hours to minutes."),
        Scenario(name="A startup using Chainguard Images", body="Migrated to <code>cgr.dev/chainguard/...</code> images for distroless minimal-CVE base layers. All Chainguard images come pre-signed + with SLSA L3 provenance + SBOMs. Their Kyverno policy reuses Chainguard\'s public key. Switching from a custom base image saved months of supply-chain plumbing."),
        Scenario(name="A team that caught XZ-style supply chain", body="Routine SBOM diff on a base-image update flagged a new package not in the previous SBOM. Investigation revealed the package was an obfuscated payload from a transitively-included Go module. Caught at PR review, never deployed. The SBOM made the diff visible; without it, the new file would have been invisible."),
    ],
    misconceptions=[
        Misconception(myth="Pinning images by tag is good enough.", truth="Tags are mutable. <code>nginx:1.21</code> can be republished with different content tomorrow. Pin by digest (<code>sha256:abc...</code>) for immutability. Or pin by tag + verify signature at admission so a stealth republish fails verification."),
        Misconception(myth="Sigstore keyless signing is less secure than key-based.", truth="It\'s often more secure: short-lived certs (10 min TTL) tied to OIDC identities can\'t be exfiltrated and reused; the trust root is a federated identity (GitHub, corp SSO) that\'s typically better managed than a key file in CI. Long-lived signing keys are notoriously leaky."),
        Misconception(myth="An SBOM proves the image is safe.", truth="An SBOM is an inventory, not a verdict. It tells you <em>what\'s</em> in the image. Combine with a vulnerability database to know <em>which CVEs apply</em>. SBOMs are evidence, not protection."),
    ],
    flashcards=[
        Flashcard(front="Three artefacts in modern supply-chain security?", back="Image (the thing). SBOM (what\'s in it). Provenance attestation (how it was built). All three signed and stored as OCI attestations alongside the image."),
        Flashcard(front="What is Cosign?", back="Sigstore CLI for signing/verifying container images and blobs. Supports both keyed and keyless signing."),
        Flashcard(front="What is keyless signing?", back="Sign with a short-lived (10 min) cert from Fulcio tied to an OIDC identity. No key file to rotate. Trust root is the OIDC identity."),
        Flashcard(front="What is Rekor?", back="Sigstore\'s tamper-evident transparency log. Every signing event recorded; append-only. Provides cryptographic proof a signature existed at a given time."),
        Flashcard(front="What does SLSA stand for?", back="Supply-chain Levels for Software Artifacts. OpenSSF standard. Levels 0-4 grade the maturity of the build process."),
        Flashcard(front="SLSA L3 requirements?", back="Build runs on isolated, ephemeral runner. Provenance generated by the build platform (not user code). Provenance is signed. Source platform is trusted."),
        Flashcard(front="SPDX vs CycloneDX?", back="Two SBOM formats. SPDX = Linux Foundation; widely used in license compliance. CycloneDX = OWASP; more common for security. Both are JSON; tools (Syft, Trivy) support both."),
        Flashcard(front="What is Syft?", back="Anchore\'s SBOM generator. Inspects images and produces SPDX or CycloneDX SBOMs. Often paired with Grype for vulnerability scanning."),
    ],
    quizzes=[
        Quiz(prompt="A vendor publishes a new image: <code>vendor/app:2.5</code>. Your cluster pulls it via Kyverno verifyImages. The vendor signed it with their key, which you\'ve added to your policy. Should you trust the image now?", answer="The signature proves the image came from the vendor — but it doesn\'t tell you if the vendor is honest, or compromised, or shipping malicious code. Cosign verification = authenticity, not safety. <strong>Defense in depth:</strong> (1) verify the SBOM has expected components (no surprise binaries). (2) Verify SLSA provenance (was built by the vendor\'s standard CI, not a one-off run). (3) Run vulnerability scans on the SBOM. (4) Track Rekor entries for unusual patterns (signing surge after a quiet period?). Signing solves \"is this from who they say it\'s from\"; supply-chain assurance needs all four signals."),
        Quiz(prompt="Your CI signs images with Cosign keyless. The Kyverno policy verifies <code>issuer: token.actions.githubusercontent.com</code> + <code>subject: github.com/myorg/.*</code>. An attacker steals a developer\'s GitHub credentials and pushes a malicious change. What still saves you?", answer="The malicious image gets built + signed by a legitimate workflow on the legitimate org. Verification passes. <strong>Cosign keyless doesn\'t protect against authenticated insider threats — it protects against unauthenticated attackers and registry compromise.</strong> What saves you: (1) PR review on the source code change. (2) Branch protection on main (no direct push). (3) Required code-owner approval. (4) PR-time SLSA provenance check (was the signing workflow run on main, or a fork?). (5) SBOM diff review — new dependencies flagged at PR. (6) Runtime detection (Falco rules, EDR). Supply-chain hardening is necessary; it\'s not sufficient against compromise of the source identity itself."),
        Quiz(prompt="The CISO mandates: \"every running image in production must have a signed SBOM available.\" Build the playbook. <strong>Click for the rollout. ▼</strong>", cyoa=True, cyoa_tag="the rollout playbook", answer="<strong>Phase 1 — produce SBOMs in CI.</strong> Add Syft (or Trivy) to every build pipeline. Output CycloneDX. Push as OCI attestation alongside the image: <code>cosign attest --predicate sbom.json --type cyclonedx ...</code>. <strong>Phase 2 — Kyverno policy in audit mode.</strong> Require SBOM attestation on all images in <code>prod</code> namespaces. Audit-mode = log violations, not block. Run for 2-4 weeks. <strong>Phase 3 — clean up.</strong> Audit reports list every image without an SBOM. Most are vendor / legacy images. For each: rebuild with SBOM, switch to a Chainguard-equivalent that ships SBOMs, or accept as a documented exception via <code>PolicyException</code>. <strong>Phase 4 — switch to Enforce mode.</strong> No more violations possible. <strong>Phase 5 — wire SBOMs into vulnerability response.</strong> Daily job pulls SBOMs from registry, runs against vulnerability DB, alerts on new CVEs affecting deployed images. <strong>Total time:</strong> ~6 weeks for a mature org with mature CI; longer if CI needs uplift first. <strong>Payoff:</strong> when the next log4j drops, you know which Pods are affected in minutes, not days."),
    ],
    glossary=[
        GlossaryItem(name="Cosign", definition="Sigstore CLI for signing/verifying images. Supports keyed and keyless modes."),
        GlossaryItem(name="Sigstore", definition="CNCF project for signing software artefacts. Includes Cosign, Fulcio, Rekor."),
        GlossaryItem(name="Fulcio", definition="Short-lived certificate authority. Issues certs tied to OIDC identities."),
        GlossaryItem(name="Rekor", definition="Tamper-evident transparency log for signing events."),
        GlossaryItem(name="Keyless signing", definition="Sigstore flow using OIDC + Fulcio to sign without long-lived keys."),
        GlossaryItem(name="SLSA", definition="Supply-chain Levels for Software Artifacts. Graded build-process standard. Pronounced \"salsa\"."),
        GlossaryItem(name="Provenance attestation", definition="Signed declaration of how an artefact was built. SLSA defines the schema."),
        GlossaryItem(name="SBOM", definition="Software Bill of Materials. Inventory of components + versions in an image."),
        GlossaryItem(name="SPDX / CycloneDX", definition="Two main SBOM formats. SPDX = Linux Foundation; CycloneDX = OWASP."),
        GlossaryItem(name="Syft", definition="Anchore\'s SBOM generator. Reads images, outputs SPDX or CycloneDX."),
        GlossaryItem(name="Trivy", definition="Aqua\'s scanner. Generates SBOMs and runs vulnerability checks against them."),
        GlossaryItem(name="OCI attestation", definition="A signed artefact stored alongside an image in an OCI registry. Conformant to OCI 1.1 reference types."),
    ],
    recap_lead="Three artefacts per image — signature (Cosign), provenance (SLSA), SBOM. All signed via Sigstore (keyless OIDC), logged in Rekor, verified at admission via Kyverno verifyImages. The chain from git to running Pod becomes auditable end-to-end.",
    recap_next="<strong>Next — Lesson 31: Multi-Tenancy & Hardening.</strong> The last security lesson — namespaces as boundaries (and where they fall short), ResourceQuota / LimitRange, kube-bench / cluster CIS scoring, the multi-tenant hierarchy NamespaceLabelSelector + HierarchicalNamespaces.",
)
