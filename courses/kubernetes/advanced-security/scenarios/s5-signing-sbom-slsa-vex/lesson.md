# K-ADV-SEC S5 — S5 · Image Signing, SBOM, SLSA, in-toto, VEX

> Course: K-ADV-SEC (advanced specialization)
> Module S5 · Signing + SBOM + SLSA + VEX
> Companion preview: `/preview-kubernetes-adv-sec-lesson-05.html`.

---

**🎯 If you remember nothing else:** **Five seals: Cosign signature, SBOM, SLSA L3+ provenance, in-toto attestations, VEX. CI signs and attests; cluster admission verifies. Sigstore + Rekor make signatures tamper-evident. VEX cuts vuln-scanner noise from 4000s to dozens.**

## 1. keyless signing, Rekor transparency log

**Cosign** signs OCI artifacts (images, SBOMs, provenance) and stores signatures as OCI referrers next to the image. *Keyless mode* (recommended): identity from OIDC (CI runner's token) rather than long-lived keys; no secrets to rotate. Sigstore's **Fulcio** issues short-lived certs from OIDC; **Rekor** logs every signature in a public transparency log so tampering is visible.
    **CI flow**: build → push → `cosign sign --identity-token=$CI_OIDC_TOKEN ghcr.io/org/app:abc123`. Signature is logged in Rekor; verifiable by anyone.
    **Cluster verification**: Kyverno `verifyImages` rule with `identities[].issuer + subject` + `cosignKey` or `keyless` spec. Admission rejects images without a matching signature + identity.
    **Why keyless?** No keys to leak; rotation is automatic (each CI run has a new short-lived cert); identity is auditable (subject = the CI runner that built it).

## 2. every package + version, attached to the image

**SBOM (Software Bill of Materials)**: a list of every package + version inside an image. Two main formats: **CycloneDX** (OWASP) — broad ecosystem support; **SPDX** (Linux Foundation) — older + ISO-standard.
    Generation: **Syft** (Anchore) is the de-facto generator ("`syft packages alpine:3 -o cyclonedx-json`"). Run in CI; attach SBOM to image as OCI referrer (`cosign attest --predicate sbom.json`).
    Cluster-side use: SBOMs are read by vuln scanners (**Trivy**, **Grype**) which compare package versions against CVE databases. Without SBOM, scanners re-scan binaries; with SBOM, scanners just check the inventory — much faster + more accurate.
    **Compliance evidence**: "every image we deploy has an SBOM attached" answers a chunk of NIST SSDF + EU CRA + US Executive Order 14028 requirements automatically.

## 3. how it was built, step-by-step

**SLSA** (Supply-chain Levels for Software Artifacts) is Google's framework. Levels 1-4 with increasing rigor:
    
      - **L1**: provenance exists.

      - **L2**: provenance authenticated by signing.

      - **L3**: build runs in isolated, hardened CI (no human can tamper with the build during execution); provenance is non-falsifiable.

      - **L4**: every input is verified + reviewed; full reproducibility.

    
    L3+ is the standard target. Achievable on GitHub Actions (with reusable workflows + ephemeral runners) or GitLab CI (with managed runners + isolated jobs). The provenance attestation states: builder ID, source repo + commit, builder image digest, recipe (e.g., Dockerfile path), result digest. Signed via Cosign; readable by anyone.
    **in-toto** is the broader supply-chain framework SLSA builds on. *step-by-step layout* defines required steps + signers; runtime evidence verifies each step happened. SLSA provenance is one in-toto attestation; you can attach more (vuln scan, license check, code review).

## 4. affected / not affected / fixed / under-investigation

Vulnerability scanners flood teams with CVEs that *look* bad but don't apply — "libssl 1.1.1k has CVE-X" but the affected code path isn't in the image's runtime. Without VEX, teams re-triage every CVE every day.
    **VEX (Vulnerability Exploitability eXchange)** is a structured statement: *this image, this CVE, status = not_affected; reason = vulnerable_code_not_present*. Two formats: **OpenVEX** (CISA) + **CSAF VEX** (OASIS). Both supported by major scanners.
    **Workflow**: vuln scanner finds CVE → security engineer triages → if not exploitable in this image, write VEX statement ("not_affected" + reason); attach to image as OCI referrer via Cosign. Next scanner pass reads VEX; suppresses the CVE; team sees only the genuinely-affecting CVEs.
    **Compliance angle**: VEX statements are *auditable* — auditors see exactly which CVEs you assessed and why you concluded not_affected. Replaces "trust us" with explicit, reviewable disposition.

## Before / After

**Before.** Pre-supply-chain-rigor, images shipped without signatures; SBOMs were sometimes generated then lost; vuln scanners produced 1000-CVE noise nobody could triage; "is this image really from CI?" was answered with *git log* + hope. Compliance audits asked "prove your build chain is secure" and the team wrote PowerPoints.

**After.** Modern pipelines sign every image (Cosign keyless), attach SBOMs (CycloneDX), produce SLSA L3+ provenance, file VEX statements for non-affecting CVEs. Cluster admission (Kyverno verifyImages) blocks unsigned + unverified images. Compliance evidence is automatic + queryable.

*Five seals on every image. Tooling does the work; engineers see only real findings; auditors see verifiable artifacts.*

## Analogy — the K-Citadel bastion

The **Seal Workshop** sits beside every printer (CI). Every batch of pamphlets coming off the press gets **five seals**: a signed wax seal from the printer (Cosign signature, logged in the Rekor public ledger), an attached **contents inventory** (SBOM listing every page), a **provenance card** stating which press, which paper, which steps (SLSA L3+), a **step-by-step audit trail** from the printer's production line (in-toto attestations), and an **exemption register** noting which generic warnings don't apply to this print run (VEX).
    At the citadel's gate, the gate-keeper checks every batch for the five seals. Missing the printer's wax seal? Refused. Missing the inventory? Refused. The exemption register tells the gate-keeper which generic concerns to ignore for this batch — "yes the warehouse logged a smoke alarm, but this batch was printed before the alarm and isn't affected."

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Wax seal from the printer | Cosign signature (image signed in CI) |
| Public ledger of every seal | Rekor transparency log |
| Short-lived stamp from authority | Sigstore Fulcio short-lived cert (keyless) |
| Contents inventory | SBOM (CycloneDX / SPDX) |
| Provenance card | SLSA L3+ provenance attestation |
| Step-by-step audit trail | in-toto attestations |
| Exemption register | VEX (OpenVEX / CSAF VEX) |
| Gate-keeper checking five seals | Kyverno verifyImages admission |

⚠️ *Analogy stops here:* A real wax seal can be melted + reapplied; Cosign signatures are cryptographic + logged in Rekor — tampering is detectable. The trade is operational, not visual.

## ELI5 / ELI10

**ELI5.** Every batch of pamphlets gets five labels before it leaves the print shop. A wax seal showing who printed it. A list of what's in it. A card describing how it was made. A step-by-step trail. And a list of "generic warnings that don't apply to this batch." The castle gate checks all five before letting the batch in.

**ELI10.** Five seals: **Cosign signature** (Sigstore keyless via OIDC + Fulcio + Rekor), **SBOM** (CycloneDX or SPDX from Syft), **SLSA L3+ provenance** (built in isolated CI; non-falsifiable attestation), **in-toto attestations** (step-by-step supply-chain framework), **VEX** (vuln disposition: affected / not_affected / fixed / under_investigation). All attached to the image as OCI referrers. Kyverno `verifyImages` validates at admission.

## Real-world scenarios

- **Greenfield CI — five seals on day one.** A new platform team integrates Cosign keyless + Syft SBOM + SLSA L3+ via reusable GitHub Actions; Kyverno verifyImages on the cluster. Every image PR triggers full chain; cluster admission blocks anything unsigned. *Day-1 supply chain meets EU CRA + US EO 14028 requirements.*
- **VEX cuts noise — 4,200 → 80 CVEs.** A regulated cluster scanned 200 images; 4,200 CRITICAL CVEs reported. Security team triaged; 80% were package CVEs in non-runtime code paths. Wrote OpenVEX statements + attached. Next scan: 80 CVEs remained — the genuinely-affecting ones. Triage went from "impossible" to "this week".
- **SLSA L3+ via reusable GHA.** A team migrated from inline GitHub Actions builds to **SLSA-Github-Generator** reusable workflow. Builder image is GitHub-hosted + isolated; provenance attestation is non-falsifiable; signed via the workflow's identity. Compliance evidence auto-generated; engineers see no extra burden.
- **Outage — admission blocked unsigned legacy image.** Kyverno verifyImages enforced cluster-wide. A team's 3-year-old service still ran an unsigned image; rolling deploy of a config change recreated Pods; admission rejected. Five-min outage. Postmortem: audit-mode for one week + warn-mode for one week before enforce; rebuild legacy image with Cosign signing.

## Common misconceptions

- **Myth:** "Image signing replaces vuln scanning."
  **Truth:** Signing proves *who* built the image; it doesn't say *what's* in it or whether anything is vulnerable. SBOM + vuln scanning are complementary — sign for trust, scan for vulns. Both are required.
- **Myth:** "SBOMs are too big / too noisy to be useful."
  **Truth:** SBOMs are the *input* to vuln scanners + license checkers; you don't read them by hand. Tools like Trivy, Grype, FOSSA consume SBOMs and produce actionable reports. SBOM size is irrelevant — toolchain handles it.
- **Myth:** "SLSA L3+ is too hard for our team."
  **Truth:** GitHub Actions has SLSA-L3 reusable workflows. GitLab CI does too. *The hard part is one PR to switch builder; the ongoing burden is zero*. Most teams who think "too hard" haven't looked at the reusable workflows.

## Recap

Five seals on every image: Cosign signature, SBOM, SLSA L3+ provenance, in-toto attestations, VEX. Sigstore + Rekor make the chain tamper-evident + auditable. Cluster admission verifies. VEX cuts vuln-scanner noise; SLSA blocks insider-threat tampering; SBOMs power compliance evidence.

**Next — S6: Secrets at Scale + mTLS + Service Mesh.** External Secrets Operator + Vault / Cloud KMS; mesh-mTLS via Istio / Linkerd; SPIFFE / SPIRE workload identity; cert-manager for cluster certs.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
