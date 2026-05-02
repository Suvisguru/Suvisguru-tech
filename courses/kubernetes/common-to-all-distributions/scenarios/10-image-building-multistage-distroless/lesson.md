# Lesson 10 — Image Building · Multi-Stage · Distroless · SBOM &amp; Signing

> Course: Kubernetes — Common to all distributions
> Lesson 10 of 17 in K-COM. Module 2 · Lesson 3 of 5.
> Companion preview: `/preview-kubernetes-lesson-10.html`.

---

## 1. Concept

An image is not magic. You write a **Dockerfile** (or equivalent)
describing the build steps, hand it to a **builder**, and out comes an
OCI image. Each build instruction (FROM, COPY, RUN) becomes a layer.
The builder hashes everything, deduplicates, and pushes to a registry.

**Build tools beyond Docker.** Docker's BuildKit is the dominant builder,
but several alternatives exist: Buildah (Red Hat, daemonless), Kaniko
(Google, in-cluster builds), ko (Go-only, no Dockerfile), Cloud Native
Buildpacks (auto-detect language). Bazel and Nix offer reproducible
bytewise-identical builds.

**Multi-stage builds** are the most important Dockerfile pattern. One
stage builds your app (compiler, dev dependencies, full toolchain).
Another copies *only the artifacts* into a tiny final image. The
builder is huge; the runtime is small.

**Base image strategies.** Four trade-offs: full distros like `ubuntu`
(~300 MB, easy to debug), slim variants like `node:22-alpine` (5–80
MB), **distroless** (10–50 MB, no shell, no package manager), **scratch**
(literally empty — only for static binaries like Go and Rust). Each
strip-down reduces image size and attack surface.

**Multi-arch with buildx.** `docker buildx build --platform
linux/amd64,linux/arm64` produces a single tag containing manifests for
both architectures. Each node pulls the right one.

**Supply chain.** Three concerns. **CVEs** — known vulnerabilities;
scan with Trivy, Grype, Snyk. **SBOM** — Software Bill of Materials,
a machine-readable list of every component (formats: SPDX, CycloneDX);
generate with syft. **Image signing** — cryptographically prove the
image came from your build pipeline (cosign, Sigstore). Together they
form your supply-chain story.

---

## 2. Before / After

**Before — naive single-stage build.** One-stage Dockerfile starting
`FROM ubuntu`. apt install build tools. Copy source. npm install + build.
Final image: 1.4 GB containing full ubuntu + gcc + make + source code +
npm cache + build artifacts + your app. Slow pulls, ~120 CVEs, attacker
gets full shell.

**After — multi-stage + distroless.** Two-stage Dockerfile. Stage 1:
node:22 with all dev deps, builds /app/dist. Stage 2: distroless/nodejs22,
copies only /app/dist from stage 1. Final image: 80 MB. 17× smaller,
pulls in seconds, ~5 CVEs, attacker has nothing (no shell to exec).

What didn't change: app behavior. Multi-stage + distroless is purely
operational improvement — no code change. The cost: harder to debug
running containers (no shell). Build "debug variants" with shell when
needed.

---

## 3. Analogy — the bakery

Building a container image is like running a bakery. Recipe (Dockerfile)
+ oven (BuildKit / Buildah / Kaniko) + ingredients (base + layers) =
finished cake (OCI image). The pros use a multi-stage process (messy
prep kitchen + clean finishing kitchen), the smallest cake base
(distroless or scratch), and ship a complete ingredient list (SBOM)
plus a baker's signature seal (cosign).

**Mapping:**

- Recipe = Dockerfile
- Oven = builder (BuildKit, Buildah, Kaniko, ko, Buildpacks)
- Multi-stage process = builder stage + runtime stage
- Cake base = base image (full / alpine / distroless / scratch)
- Ingredient list = SBOM (SPDX, CycloneDX)
- Baker's signature = image signing (cosign / Sigstore)
- Food safety inspection = vulnerability scanning (Trivy, Grype)

---

## 4. ELI5 / ELI10

**ELI5.** A bakery. The recipe is a list of steps. The oven is the
machine that bakes. You can use a small base (just a cookie) or a big
base (a whole cake). Pros use the smallest base that works because
nobody wants to eat the box. They also write down what's in the cake so
you know what you're eating, and they sign their work so you know it
came from them.

**ELI10.** An OCI image is built by feeding instructions (a Dockerfile)
to a builder (BuildKit, Buildah, Kaniko, ko, or Buildpacks). Each
instruction becomes a layer. The most important pattern is
**multi-stage**: one stage with all the build tools and dev dependencies,
a final stage that copies just the compiled artifact into a tiny base
image. Common bases: full distro (300MB), alpine (~5MB), distroless
(~10-50MB, no shell), scratch (literally empty, only for static
binaries). Then you scan for CVEs (Trivy/Grype), generate an SBOM
(SPDX or CycloneDX), and sign the image (cosign). Those three give you
a defensible supply-chain story.

---

## 5. Real-world scenarios

**Multi-stage cut image from 1.2 GB to 80 MB.** A team's Node.js app
shipped as 1.2 GB. Pulls took 90s. Refactored to multi-stage with
distroless runtime. Result: 80 MB. Pulls take 6s. CVEs dropped from 124
to 8. Same app, 15× faster deploys.

**Distroless prevented attacker shell access.** Web app got compromised
through an unsanitized input. Attacker tried `exec("/bin/sh")` to
escalate. Image used `gcr.io/distroless/python3` — no shell. Exec
failed. Team fixed the input bug calmly during business hours. Distroless
turned a 3am incident into a Tuesday afternoon ticket.

**SBOM sped up the Log4j response.** When Log4Shell landed (Dec 2021),
teams scrambled to find which images included vulnerable Log4j. Teams
generating SBOMs (SPDX/CycloneDX) had a one-line answer: grep their SBOM
database for "log4j-core". Teams without SBOMs spent days inspecting
Dockerfiles.

**Image signing caught a supply-chain attack.** An attacker compromised
CI credentials and pushed a malicious image under a legitimate tag.
Production had a Kyverno admission policy requiring images to be signed
by the team's Cosign key. The malicious image wasn't signed. Kubernetes
refused to admit the pod. Incident contained at the admission boundary.

---

## 6. Animated illustration

Three modes:

1. **Multi-stage build** (4 steps). Stage 1 builder: FROM node:22 →
   npm ci → npm build (1.25 GB). Stage 2 runtime: FROM distroless +
   COPY --from=0 /app/dist → 80 MB final. Builder discarded.
2. **Base image sizes** (4 options). Same Node.js app on ubuntu (350
   MB) vs alpine (90 MB) vs distroless (80 MB) vs scratch (10 MB,
   Go/Rust only).
3. **Scan + SBOM + sign pipeline** (4 steps). Trivy CVE scan → syft
   SBOM (SPDX) → cosign sign → push → admission verifies signature.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
