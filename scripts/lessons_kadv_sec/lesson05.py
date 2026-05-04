"""K-ADV-SEC S5 — Image signing + SBOM + SLSA + in-toto + VEX in CI/CD."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Image signing + SBOM + SLSA + VEX — supply-chain integrity.">
  <rect x="20" y="20" width="720" height="160" rx="16" fill="#FBF7F0" stroke="#C8C2B6" stroke-width="1"/>
  <text x="380" y="44" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="14" font-weight="700" fill="#3F4A5E">Seal Workshop · K-Citadel — five seals: signature · SBOM · provenance · in-toto · VEX</text>
  <rect x="40" y="70" width="130" height="100" rx="10" fill="#FF9900" stroke="#1F2433"/>
  <text x="105" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">Signature</text>
  <text x="105" y="108" text-anchor="middle" font-size="9" fill="#1F2433">Cosign / Sigstore</text>
  <text x="105" y="124" text-anchor="middle" font-size="9" fill="#1F2433">+ Rekor log</text>
  <rect x="180" y="70" width="130" height="100" rx="10" fill="#5DCAA5" stroke="#1F2433"/>
  <text x="245" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#1F2433">SBOM</text>
  <text x="245" y="108" text-anchor="middle" font-size="9" fill="#1F2433">CycloneDX / SPDX</text>
  <text x="245" y="124" text-anchor="middle" font-size="9" fill="#1F2433">contents inventory</text>
  <rect x="320" y="70" width="130" height="100" rx="10" fill="#3F4A5E" stroke="#1F2433"/>
  <text x="385" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">SLSA L3+</text>
  <text x="385" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">build provenance</text>
  <text x="385" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">attestation</text>
  <rect x="460" y="70" width="130" height="100" rx="10" fill="#5A6B81" stroke="#1F2433"/>
  <text x="525" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">in-toto</text>
  <text x="525" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">step-by-step trail</text>
  <text x="525" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">supply-chain framework</text>
  <rect x="600" y="70" width="130" height="100" rx="10" fill="#A04832" stroke="#1F2433"/>
  <text x="665" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">VEX</text>
  <text x="665" y="108" text-anchor="middle" font-size="9" fill="#FBF1D6">vuln disposition</text>
  <text x="665" y="124" text-anchor="middle" font-size="9" fill="#FBF1D6">affected / not affected</text>
</svg>"""


LESSON = LessonSpec(
    num="05",
    title_short="signing + SBOM + SLSA + VEX",
    title_full="S5 · Image Signing, SBOM, SLSA L3+, in-toto, VEX in CI/CD",
    title_html="K-ADV-SEC S5 · Signing + SBOM + SLSA + VEX",
    module_eyebrow="Module S5 · the Seal Workshop — five seals on every image",
    hero_sub_html='Five supply-chain seals every production image carries. <strong>Cosign signature</strong> (Sigstore) — proves who built it; logged in Rekor. <strong>SBOM</strong> (CycloneDX or SPDX) — inventory of every package + version inside. <strong>SLSA L3+ provenance</strong> — attestation about how it was built (builder, source, isolation level). <strong>in-toto attestations</strong> — step-by-step trail of supply-chain operations. <strong>VEX</strong> — explicit \"this CVE doesn\'t affect this image because X\" so vuln scanners don\'t flood you with false positives. Cluster admission (Kyverno verifyImages) checks signatures + provenance before allowing the Pod to start.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. A vuln scanner reports 4,200 CRITICAL CVEs across the image fleet — the team paged is told they have to remediate everything in 24 hours. <em>Most of those CVEs aren\'t exploitable in the way the scanner assumed</em>; the team has no way to mark them VEX-not-affected. Workflow grinds. Today\'s lesson: build the supply chain so vuln scanners give signal, not noise.",
    stamp_html="<strong>Five seals: Cosign signature, SBOM, SLSA L3+ provenance, in-toto attestations, VEX. CI signs and attests; cluster admission verifies. Sigstore + Rekor make signatures tamper-evident. VEX cuts vuln-scanner noise from 4000s to dozens.</strong>",
    district_pin="ksec-bastion05",
    district_label="Seal Workshop",
    sections=[
        Section(
            eyebrow="Section 1.1 · Cosign + Sigstore",
            h2="keyless signing, Rekor transparency log",
            body_html="""    <p><strong>Cosign</strong> signs OCI artifacts (images, SBOMs, provenance) and stores signatures as OCI referrers next to the image. <em>Keyless mode</em> (recommended): identity from OIDC (CI runner\'s token) rather than long-lived keys; no secrets to rotate. Sigstore\'s <strong>Fulcio</strong> issues short-lived certs from OIDC; <strong>Rekor</strong> logs every signature in a public transparency log so tampering is visible.</p>
    <p><strong>CI flow</strong>: build → push → <code>cosign sign --identity-token=$CI_OIDC_TOKEN ghcr.io/org/app:abc123</code>. Signature is logged in Rekor; verifiable by anyone.</p>
    <p><strong>Cluster verification</strong>: Kyverno <code>verifyImages</code> rule with <code>identities[].issuer + subject</code> + <code>cosignKey</code> or <code>keyless</code> spec. Admission rejects images without a matching signature + identity.</p>
    <p><strong>Why keyless?</strong> No keys to leak; rotation is automatic (each CI run has a new short-lived cert); identity is auditable (subject = the CI runner that built it).</p>"""
        ),
        Section(
            eyebrow="Section 1.2 · SBOM (CycloneDX / SPDX)",
            h2="every package + version, attached to the image",
            body_html="""    <p><strong>SBOM (Software Bill of Materials)</strong>: a list of every package + version inside an image. Two main formats: <strong>CycloneDX</strong> (OWASP) — broad ecosystem support; <strong>SPDX</strong> (Linux Foundation) — older + ISO-standard.</p>
    <p>Generation: <strong>Syft</strong> (Anchore) is the de-facto generator (\"<code>syft packages alpine:3 -o cyclonedx-json</code>\"). Run in CI; attach SBOM to image as OCI referrer (<code>cosign attest --predicate sbom.json</code>).</p>
    <p>Cluster-side use: SBOMs are read by vuln scanners (<strong>Trivy</strong>, <strong>Grype</strong>) which compare package versions against CVE databases. Without SBOM, scanners re-scan binaries; with SBOM, scanners just check the inventory — much faster + more accurate.</p>
    <p><strong>Compliance evidence</strong>: \"every image we deploy has an SBOM attached\" answers a chunk of NIST SSDF + EU CRA + US Executive Order 14028 requirements automatically.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · SLSA L3+ provenance + in-toto",
            h2="how it was built, step-by-step",
            body_html="""    <p><strong>SLSA</strong> (Supply-chain Levels for Software Artifacts) is Google\'s framework. Levels 1-4 with increasing rigor:</p>
    <ul>
      <li><strong>L1</strong>: provenance exists.</li>
      <li><strong>L2</strong>: provenance authenticated by signing.</li>
      <li><strong>L3</strong>: build runs in isolated, hardened CI (no human can tamper with the build during execution); provenance is non-falsifiable.</li>
      <li><strong>L4</strong>: every input is verified + reviewed; full reproducibility.</li>
    </ul>
    <p>L3+ is the standard target. Achievable on GitHub Actions (with reusable workflows + ephemeral runners) or GitLab CI (with managed runners + isolated jobs). The provenance attestation states: builder ID, source repo + commit, builder image digest, recipe (e.g., Dockerfile path), result digest. Signed via Cosign; readable by anyone.</p>
    <p><strong>in-toto</strong> is the broader supply-chain framework SLSA builds on. <em>step-by-step layout</em> defines required steps + signers; runtime evidence verifies each step happened. SLSA provenance is one in-toto attestation; you can attach more (vuln scan, license check, code review).</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · VEX — vulnerability disposition",
            h2="affected / not affected / fixed / under-investigation",
            body_html="""    <p>Vulnerability scanners flood teams with CVEs that <em>look</em> bad but don\'t apply — \"libssl 1.1.1k has CVE-X\" but the affected code path isn\'t in the image\'s runtime. Without VEX, teams re-triage every CVE every day.</p>
    <p><strong>VEX (Vulnerability Exploitability eXchange)</strong> is a structured statement: <em>this image, this CVE, status = not_affected; reason = vulnerable_code_not_present</em>. Two formats: <strong>OpenVEX</strong> (CISA) + <strong>CSAF VEX</strong> (OASIS). Both supported by major scanners.</p>
    <p><strong>Workflow</strong>: vuln scanner finds CVE → security engineer triages → if not exploitable in this image, write VEX statement (\"not_affected\" + reason); attach to image as OCI referrer via Cosign. Next scanner pass reads VEX; suppresses the CVE; team sees only the genuinely-affecting CVEs.</p>
    <p><strong>Compliance angle</strong>: VEX statements are <em>auditable</em> — auditors see exactly which CVEs you assessed and why you concluded not_affected. Replaces \"trust us\" with explicit, reviewable disposition.</p>"""
        ),
    ],
    pause_check_after_section={
        0: PauseCheck(
            question="What does Cosign keyless signing replace?",
            options=[
                ("Image registry authentication.", False),
                ("Long-lived signing keys with rotation burden.", True),
                ("SBOM generation.", False),
            ],
            feedback="Keyless uses OIDC identity (CI runner\'s short-lived token) → Fulcio issues a short-lived cert → Cosign signs with it. No long-lived keys to leak or rotate.",
        ),
        3: PauseCheck(
            question="A scanner reports 1,000 CVEs in your image fleet. 80% aren\'t actually exploitable. How do you cut the noise?",
            options=[
                ("Use a different scanner.", False),
                ("Triage + write VEX statements (not_affected + reason); attach to images.", True),
                ("Disable the scanner.", False),
            ],
            feedback="VEX is the standard answer. Triage once; statement attached to image; scanners read VEX on subsequent runs and suppress not-affected CVEs. Compliance still sees the disposition; the team sees only signal.",
        ),
    },
    before_after_before='<p>Pre-supply-chain-rigor, images shipped without signatures; SBOMs were sometimes generated then lost; vuln scanners produced 1000-CVE noise nobody could triage; \"is this image really from CI?\" was answered with <em>git log</em> + hope. Compliance audits asked \"prove your build chain is secure\" and the team wrote PowerPoints.</p>',
    before_after_after='<p>Modern pipelines sign every image (Cosign keyless), attach SBOMs (CycloneDX), produce SLSA L3+ provenance, file VEX statements for non-affecting CVEs. Cluster admission (Kyverno verifyImages) blocks unsigned + unverified images. Compliance evidence is automatic + queryable.</p>',
    before_after_caption='<p class="ba-caption"><em>Five seals on every image. Tooling does the work; engineers see only real findings; auditors see verifiable artifacts.</em></p>',
    analogy_intro_html='''<p>The <strong>Seal Workshop</strong> sits beside every printer (CI). Every batch of pamphlets coming off the press gets <strong>five seals</strong>: a signed wax seal from the printer (Cosign signature, logged in the Rekor public ledger), an attached <strong>contents inventory</strong> (SBOM listing every page), a <strong>provenance card</strong> stating which press, which paper, which steps (SLSA L3+), a <strong>step-by-step audit trail</strong> from the printer\'s production line (in-toto attestations), and an <strong>exemption register</strong> noting which generic warnings don\'t apply to this print run (VEX).</p>
    <p>At the citadel\'s gate, the gate-keeper checks every batch for the five seals. Missing the printer\'s wax seal? Refused. Missing the inventory? Refused. The exemption register tells the gate-keeper which generic concerns to ignore for this batch — \"yes the warehouse logged a smoke alarm, but this batch was printed before the alarm and isn\'t affected.\"</p>''',
    translation_rows=[
        ("Wax seal from the printer", "Cosign signature (image signed in CI)"),
        ("Public ledger of every seal", "Rekor transparency log"),
        ("Short-lived stamp from authority", "Sigstore Fulcio short-lived cert (keyless)"),
        ("Contents inventory", "SBOM (CycloneDX / SPDX)"),
        ("Provenance card", "SLSA L3+ provenance attestation"),
        ("Step-by-step audit trail", "in-toto attestations"),
        ("Exemption register", "VEX (OpenVEX / CSAF VEX)"),
        ("Gate-keeper checking five seals", "Kyverno verifyImages admission"),
    ],
    analogy_stops="A real wax seal can be melted + reapplied; Cosign signatures are cryptographic + logged in Rekor — tampering is detectable. The trade is operational, not visual.",
    eli5="Every batch of pamphlets gets five labels before it leaves the print shop. A wax seal showing who printed it. A list of what\'s in it. A card describing how it was made. A step-by-step trail. And a list of \"generic warnings that don\'t apply to this batch.\" The castle gate checks all five before letting the batch in.",
    eli10="Five seals: <strong>Cosign signature</strong> (Sigstore keyless via OIDC + Fulcio + Rekor), <strong>SBOM</strong> (CycloneDX or SPDX from Syft), <strong>SLSA L3+ provenance</strong> (built in isolated CI; non-falsifiable attestation), <strong>in-toto attestations</strong> (step-by-step supply-chain framework), <strong>VEX</strong> (vuln disposition: affected / not_affected / fixed / under_investigation). All attached to the image as OCI referrers. Kyverno <code>verifyImages</code> validates at admission.",
    scenarios=[
        Scenario(
            name="Greenfield CI — five seals on day one",
            body="A new platform team integrates Cosign keyless + Syft SBOM + SLSA L3+ via reusable GitHub Actions; Kyverno verifyImages on the cluster. Every image PR triggers full chain; cluster admission blocks anything unsigned. <em>Day-1 supply chain meets EU CRA + US EO 14028 requirements.</em>",
        ),
        Scenario(
            name="VEX cuts noise — 4,200 → 80 CVEs",
            body="A regulated cluster scanned 200 images; 4,200 CRITICAL CVEs reported. Security team triaged; 80% were package CVEs in non-runtime code paths. Wrote OpenVEX statements + attached. Next scan: 80 CVEs remained — the genuinely-affecting ones. Triage went from \"impossible\" to \"this week\".",
        ),
        Scenario(
            name="SLSA L3+ via reusable GHA",
            body="A team migrated from inline GitHub Actions builds to <strong>SLSA-Github-Generator</strong> reusable workflow. Builder image is GitHub-hosted + isolated; provenance attestation is non-falsifiable; signed via the workflow\'s identity. Compliance evidence auto-generated; engineers see no extra burden.",
        ),
        Scenario(
            name="Outage — admission blocked unsigned legacy image",
            body="Kyverno verifyImages enforced cluster-wide. A team\'s 3-year-old service still ran an unsigned image; rolling deploy of a config change recreated Pods; admission rejected. Five-min outage. Postmortem: audit-mode for one week + warn-mode for one week before enforce; rebuild legacy image with Cosign signing.",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"Image signing replaces vuln scanning.\"",
            truth="Signing proves <em>who</em> built the image; it doesn\'t say <em>what\'s</em> in it or whether anything is vulnerable. SBOM + vuln scanning are complementary — sign for trust, scan for vulns. Both are required.",
        ),
        Misconception(
            myth="\"SBOMs are too big / too noisy to be useful.\"",
            truth="SBOMs are the <em>input</em> to vuln scanners + license checkers; you don\'t read them by hand. Tools like Trivy, Grype, FOSSA consume SBOMs and produce actionable reports. SBOM size is irrelevant — toolchain handles it.",
        ),
        Misconception(
            myth="\"SLSA L3+ is too hard for our team.\"",
            truth="GitHub Actions has SLSA-L3 reusable workflows. GitLab CI does too. <em>The hard part is one PR to switch builder; the ongoing burden is zero</em>. Most teams who think \"too hard\" haven\'t looked at the reusable workflows.",
        ),
    ],
    flashcards=[
        Flashcard(front="What does Cosign keyless replace?", back="Long-lived signing keys. Identity comes from OIDC (CI runner\'s token); Sigstore Fulcio issues a short-lived cert; signature logged in Rekor public transparency log. No keys to rotate or leak."),
        Flashcard(front="Two main SBOM formats?", back="<strong>CycloneDX</strong> (OWASP — broader ecosystem support) and <strong>SPDX</strong> (Linux Foundation — older + ISO-standard). Most tools support both."),
        Flashcard(front="What does SLSA L3 require?", back="(1) Provenance is generated. (2) Build runs in isolated, hardened CI (no human tampering during build). (3) Provenance is non-falsifiable (signed + logged). Practical: GitHub Actions reusable workflow + ephemeral runners hits L3."),
        Flashcard(front="What is in-toto?", back="Supply-chain integrity framework. Defines step-by-step layouts (required steps + signers); runtime evidence verifies each step happened. SLSA provenance is one in-toto attestation type."),
        Flashcard(front="Four VEX statuses?", back="<strong>not_affected</strong> (with reason), <strong>affected</strong>, <strong>fixed</strong>, <strong>under_investigation</strong>. OpenVEX (CISA) + CSAF VEX (OASIS) are the two formats."),
        Flashcard(front="How does cluster admission verify signatures?", back="Kyverno <code>verifyImages</code> rule references the expected <code>identities[].issuer</code> + <code>subject</code> (keyless) or <code>publicKey</code> (keyed). Admission rejects images without matching attestation."),
        Flashcard(front="Where do attestations live?", back="As <strong>OCI referrers</strong> in the same registry, alongside the image. Cosign attaches them via <code>cosign attest</code> + <code>cosign sign</code>. Tools query the registry for referrers."),
        Flashcard(front="Why is Rekor public?", back="Public transparency log = signatures are immutable + auditable by anyone. If a signature is forged or backdated, Rekor\'s history shows the discrepancy. Replaces trust-the-CA with trust-the-log."),
    ],
    quizzes=[
        Quiz(
            prompt="Walk through enabling Cosign keyless + SLSA L3+ + admission verification for a Go service in GitHub Actions, end to end.",
            answer="(1) <strong>CI workflow</strong>: use the SLSA-3 reusable workflow <code>slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml</code> — builds image, pushes, generates + signs SLSA L3+ provenance attestation. (2) <strong>SBOM</strong>: separate step runs Syft → emits CycloneDX → <code>cosign attest --type cyclonedx --predicate sbom.json &lt;image&gt;</code>. (3) <strong>Cosign keyless signature</strong>: SLSA workflow already signs; OIDC identity = the workflow\'s token; verifiable. (4) <strong>Cluster admission</strong>: Kyverno ClusterPolicy with <code>verifyImages</code> rule: <code>identities: [{issuer: \"https://token.actions.githubusercontent.com\", subjectRegExp: \"^https://github.com/your-org/.*\"}]</code> + <code>verifyAttestations: [{predicateType: \"https://slsa.dev/provenance/v1\"}]</code>. (5) <strong>Audit + warn + enforce rollout</strong>: 4 weeks total. (6) <strong>VEX</strong>: integrate VEX-Hub or vexctl for triaging false positives.",
        ),
        Quiz(
            prompt="A vuln scanner shows 200 CVEs across 50 images. The team can\'t triage manually. What\'s the operational pattern that scales?",
            answer="(1) <strong>Sort by exploitability</strong>: Trivy + Grype both support EPSS (Exploit Prediction Scoring System) scoring + KEV (CISA Known Exploited Vulnerabilities) tagging. Filter the 200 to the ~20 with EPSS &gt; 0.1 or KEV-listed. (2) <strong>Triage the 20</strong>: per CVE, check whether the image\'s runtime actually exercises the vulnerable code path. Many CVEs are in libraries the image carries but doesn\'t use. (3) <strong>Write OpenVEX statements</strong> for not_affected + reason; attach to images via Cosign. (4) <strong>For affected CVEs</strong>: schedule remediation per severity (KEV → 24h; high EPSS → 1 week; medium → 30d). (5) <strong>Automate</strong>: VEX statements in Git; CI workflow re-attaches on image rebuild. (6) <strong>Measure</strong>: \"open CVEs &gt; 30 days\" trends down; team\'s actual workload trends down.",
        ),
        Quiz(
            prompt="A new exec asks: \"why are we doing all this supply-chain work? CVEs aren\'t trending up.\" Defend the investment.",
            answer="\"<strong>Supply-chain attacks are the highest-leverage attacks because they hit thousands of consumers per breach.</strong> Three reasons the seals are non-optional: (1) <strong>Real attacks at scale</strong>: SolarWinds (2020), Codecov (2021), Log4Shell amplification through downstream packages, dozens of NPM/PyPI typosquats per quarter. We\'re not preparing for hypothetical risk; we\'re preparing for documented attack patterns. (2) <strong>Regulatory inevitability</strong>: US EO 14028, EU CRA, NIST SSDF, FedRAMP — all require signed builds + SBOMs. Costs of catching up at audit are massively higher than building it now. (3) <strong>Operational quality</strong>: SBOMs + VEX make vuln triage 10× faster. SLSA-isolated builds remove insider-threat surface. Sigstore replaces key rotation pain. <strong>The seals make the day-job easier, not harder, after the initial setup.</strong> The investment pays in operational dividend within a quarter; the security upside is on top.\"",
            cyoa=True,
            cyoa_tag="how the security architect defended the supply chain investment",
        ),
    ],
    glossary=[
        GlossaryItem(name="Cosign", definition="Tool for signing OCI artifacts (images, SBOMs, attestations). Sigstore project."),
        GlossaryItem(name="Sigstore", definition="OpenSSF project — Cosign + Fulcio + Rekor. Keyless signing infrastructure with public transparency log."),
        GlossaryItem(name="Fulcio", definition="Sigstore certificate authority — issues short-lived X.509 certs based on OIDC identity claims."),
        GlossaryItem(name="Rekor", definition="Sigstore public transparency log — immutable record of every signature + attestation. Tamper-evident."),
        GlossaryItem(name="SBOM (CycloneDX / SPDX)", definition="Software Bill of Materials. Inventory of every package + version inside an image. Two formats."),
        GlossaryItem(name="SLSA", definition="Supply-chain Levels for Software Artifacts. Levels 1-4; L3+ is the practical target (isolated CI + non-falsifiable provenance)."),
        GlossaryItem(name="in-toto", definition="Supply-chain integrity framework. Defines layouts + attestations for each step. SLSA builds on it."),
        GlossaryItem(name="VEX", definition="Vulnerability Exploitability eXchange. Statements: not_affected / affected / fixed / under_investigation. OpenVEX or CSAF VEX."),
        GlossaryItem(name="OCI referrer", definition="Companion artifact attached to an image in a registry — signature, SBOM, attestation, VEX. Discoverable via OCI 1.1 referrers API."),
        GlossaryItem(name="Kyverno verifyImages", definition="Kyverno rule kind validating image signatures + attestations at admission."),
    ],
    recap_lead="Five seals on every image: Cosign signature, SBOM, SLSA L3+ provenance, in-toto attestations, VEX. Sigstore + Rekor make the chain tamper-evident + auditable. Cluster admission verifies. VEX cuts vuln-scanner noise; SLSA blocks insider-threat tampering; SBOMs power compliance evidence.",
    recap_next='<strong>Next — S6: Secrets at Scale + mTLS + Service Mesh.</strong> External Secrets Operator + Vault / Cloud KMS; mesh-mTLS via Istio / Linkerd; SPIFFE / SPIRE workload identity; cert-manager for cluster certs.',
    architecture_svg='''<svg viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Supply chain pipeline: build → SBOM + SLSA → Cosign sign → Rekor log → registry → Kyverno verify → admission → deploy.">
  <rect x="10" y="10" width="740" height="220" rx="12" fill="#FBF7F0" stroke="#FF9900"/>
  <text x="380" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1">SUPPLY-CHAIN PIPELINE · 5 SEALS ON EVERY IMAGE</text>
  <rect x="20" y="50" width="100" height="65" rx="6" fill="#5DCAA5"/>
  <text x="70" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">CI build</text>
  <text x="70" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">isolated</text>
  <text x="70" y="100" text-anchor="middle" font-size="8" fill="#1F2433">SLSA L3+</text>
  <line x1="120" y1="82" x2="145" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aS5)"/>
  <defs><marker id="aS5" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><polygon points="0 0, 10 5, 0 10" fill="#5A4F45"/></marker></defs>
  <rect x="145" y="50" width="100" height="65" rx="6" fill="#FF9900"/>
  <text x="195" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#1F2433">Syft SBOM</text>
  <text x="195" y="86" text-anchor="middle" font-size="8" fill="#1F2433" font-style="italic">CycloneDX</text>
  <text x="195" y="100" text-anchor="middle" font-size="8" fill="#1F2433">/ SPDX</text>
  <line x1="245" y1="82" x2="270" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aS5)"/>
  <rect x="270" y="50" width="100" height="65" rx="6" fill="#3F4A5E"/>
  <text x="320" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Cosign sign</text>
  <text x="320" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">keyless OIDC</text>
  <text x="320" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">via Fulcio</text>
  <line x1="370" y1="82" x2="395" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aS5)"/>
  <rect x="395" y="50" width="100" height="65" rx="6" fill="#5E4A8E"/>
  <text x="445" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Rekor log</text>
  <text x="445" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">public</text>
  <text x="445" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">transparency</text>
  <line x1="495" y1="82" x2="520" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aS5)"/>
  <rect x="520" y="50" width="100" height="65" rx="6" fill="#5A6B81"/>
  <text x="570" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">OCI registry</text>
  <text x="570" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">image + sigs</text>
  <text x="570" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">+ SBOM + VEX</text>
  <line x1="620" y1="82" x2="645" y2="82" stroke="#5A4F45" stroke-width="2" marker-end="url(#aS5)"/>
  <rect x="645" y="50" width="95" height="65" rx="6" fill="#A04832"/>
  <text x="692" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">Kyverno</text>
  <text x="692" y="86" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">verifyImages</text>
  <text x="692" y="100" text-anchor="middle" font-size="8" fill="#FBE8DC">at admission</text>
  <rect x="20" y="130" width="350" height="55" rx="6" fill="#FAC775"/>
  <text x="195" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">VEX (vuln disposition)</text>
  <text x="195" y="166" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">OpenVEX / CSAF VEX — not_affected reasons</text>
  <text x="195" y="178" text-anchor="middle" font-size="8" fill="#5A4F45">cuts scanner noise from 4000s to dozens</text>
  <rect x="380" y="130" width="360" height="55" rx="6" fill="#1F8A60"/>
  <text x="560" y="150" text-anchor="middle" font-size="10" font-weight="700" fill="#FBF1D6">in-toto attestations</text>
  <text x="560" y="166" text-anchor="middle" font-size="8" fill="#FBE8DC" font-style="italic">step-by-step supply chain framework</text>
  <text x="560" y="178" text-anchor="middle" font-size="8" fill="#FBE8DC">SLSA provenance is one in-toto attestation type</text>
  <rect x="20" y="195" width="720" height="30" rx="6" fill="#FBE8DC" stroke="#A04832"/>
  <text x="380" y="215" text-anchor="middle" font-size="10" font-weight="700" fill="#A04832">5 seals: signature · SBOM · SLSA · in-toto · VEX — all attached as OCI referrers next to the image</text>
</svg>''',
    architecture_caption='Supply chain pipeline: CI build (SLSA L3+) → Syft SBOM → Cosign keyless sign → Rekor public log → OCI registry holds image + sigs + SBOM + VEX → Kyverno verifyImages at admission. VEX cuts scanner noise; in-toto wraps the framework.',
)
