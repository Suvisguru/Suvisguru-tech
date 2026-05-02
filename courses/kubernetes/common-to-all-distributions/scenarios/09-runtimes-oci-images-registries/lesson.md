# Lesson 09 — Container Runtimes & the OCI Standard

> Course: Kubernetes — Common to all distributions
> Lesson 09 of 17 in K-COM. Module 2 · Lesson 2 of 5.
> Companion preview: `/preview-kubernetes-lesson-09.html`.

---

## 1. Concept

In 2015, the container ecosystem was at risk of fragmenting. Docker had
its own format. CoreOS had rkt with a different format. Cloud vendors
were building incompatible variations. The industry agreed to a common
standard hosted by the Linux Foundation: **OCI** (Open Container
Initiative). Today, every serious container tool implements OCI specs.

OCI defines three specifications:

- **image spec** — what's in a container image (layers, manifest, config)
- **runtime spec** — how to start a container from an unpacked filesystem
- **distribution spec** — how registries serve images via HTTP

Together they form a complete contract: build with one tool, store in
any registry, run with any runtime.

**Container runtimes** split into two layers:

- **High-level runtime** (containerd, CRI-O) — handles image pulling,
  container lifecycle, the Kubernetes CRI protocol.
- **Low-level runtime** (runc, crun, youki) — does the actual kernel
  work: `clone()` with namespace flags, cgroups setup, capability drop,
  seccomp profile.

runc is the original Go reference implementation. crun is a faster C
rewrite. youki is a Rust rewrite for memory safety. All OCI-compliant
drop-in replacements.

**Image structure:** an image is a stack of read-only **layers**
(each a tarball with its own SHA256 digest), a **manifest** (JSON
listing the layers and config), and a **config** (how to run: command,
env, ports, user). When the runtime "runs an image," it stacks those
layers into a unified filesystem and starts the container.

**Tags vs digests:** tags like `nginx:1.27` are mutable friendly names —
the publisher can move them. Digests like `sha256:abc...` are
cryptographic hashes — same content always = same digest. For
reproducibility, **pin to digests in production**.

**Registries** are HTTP services storing images, all speaking the OCI
distribution spec. Public: Docker Hub, GitHub Container Registry (GHCR).
Cloud: AWS ECR, Google Artifact Registry (GCR/AR), Azure ACR. Self-host:
Harbor, Quay, JFrog.

---

## The runtime landscape

| Tool | Layer | Notes |
|------|-------|-------|
| containerd | High-level | CNCF graduated. Default in most Kubernetes. |
| CRI-O | High-level | Kubernetes-only. Common on OpenShift. |
| runc | Low-level | Original Go reference. Default. |
| crun | Low-level | C rewrite by Red Hat. Faster, smaller. |
| youki | Low-level | Rust rewrite. Memory-safe. Newer. |
| gVisor / Kata | Sandboxed | Heavier isolation. Untrusted multi-tenancy. |

Most clusters run containerd + runc by default. Don't think about
runtime choice unless you have specific isolation or performance needs.

---

## 2. Before / After

**Before — pre-OCI (2015).** Docker images only worked with Docker.
CoreOS rkt had its own format. Cloud vendors built proprietary variants.
Switching tools meant rebuilding everything — different image format,
registry protocol, runtime API.

**After — OCI standard.** One image format works with any runtime
(containerd, CRI-O, Podman). One registry protocol means any image hosts
on any registry (Docker Hub, GHCR, ECR, GCR, Harbor). The image you
build today still works in 5 years on a runtime that doesn't exist yet —
as long as it's OCI-compliant.

What didn't change: there's still operational complexity around image
signing, supply-chain security (SBOMs, provenance), and registry
credential management. OCI standardized the format, not the policy.

---

## 3. Analogy — standardized warehouses and forklifts

Imagine the global shipping industry. There's one standard for shipping
containers (ISO sizes, lifting points, manifest format). Any container
fits on any truck, ship, or train. Any warehouse can store any
container. Any forklift can pick one up. The standard makes the network
work.

OCI is that standard for software containers. Different forklifts (runc,
crun, youki) all work with the same boxes. Different warehouses (Docker
Hub, GHCR, ECR) all store the same boxes.

Inside each box, smaller boxes stacked together = the layers. The
manifest is the packing list. The tag is the friendly label ("v1.27")
and the digest is the unique tracking number.

**Mapping:**

- Standard shipping container = OCI image format
- Layers stacked inside = image layers
- Packing list = manifest
- Friendly label = tag (mutable)
- Unique tracking number = digest (immutable)
- Warehouses = registries
- Forklifts = container runtimes

---

## 4. ELI5 / ELI10

**ELI5.** There are giant warehouses full of boxes. Every box is the
same shape, with a label on the outside and a packing list inside.
Forklifts can pick up any box from any warehouse, because all the boxes
are the same shape. Some boxes have stickers like "v1.27" — those
stickers can be moved. Some have a special bar code that nobody can
change.

**ELI10.** OCI (Open Container Initiative) is a Linux Foundation
standard with three specs: image format, runtime spec, distribution
spec. Container runtimes split into **high-level** (containerd, CRI-O —
pull images, manage lifecycle, talk to Kubernetes via CRI) and
**low-level** (runc, crun, youki — make the kernel `clone()` + cgroups
+ capabilities calls). Images are stacks of read-only layers + a
manifest. **Tags** like `nginx:1.27` are mutable labels; **digests**
like `sha256:abc...` are immutable hashes. For production
reproducibility, pin to digests.

---

## 5. Real-world scenarios

**:latest broke production.** A team ran `image: my-app:latest` in
their Kubernetes Deployments. Friday at 6 PM, someone published a new
"latest" with a bad migration. Pods restarting through the night picked
up the new image. By Saturday morning, half the pods had bad images.
Fix: pin to digests in production. Renovate auto-updates digests via PR.

**Multi-arch image build.** A team needs ARM (Graviton EC2) and AMD64
support. They use `docker buildx build --platform linux/amd64,linux/arm64`.
The result: one tag containing two manifests. Each node pulls the right
manifest for its architecture.

**Switched runc to crun for performance.** A high-density platform
(200+ containers per host) switched to crun. Smaller memory footprint,
faster startup → ~30% pod startup latency reduction, ~5% host memory
savings. Same OCI image; just a different forklift.

**ImagePullBackOff (private registry auth).** Pod stuck in ErrImagePull
→ ImagePullBackOff. Cause: kubelet didn't have credentials for private
GHCR. Fix: create a `kubernetes.io/dockerconfigjson` Secret with the
GHCR token, reference via `imagePullSecrets` in pod spec.

---

## 6. Animated illustration

Three modes in the preview animation:

1. **Pull & run image.** 4 steps: fetch manifest → fetch layers in
   parallel → stack into unified filesystem → low-level runtime starts
   container.
2. **Tag mutation.** Same `nginx:1.27` tag pointing at 3 different
   digests over 60 days (publisher rebuilt twice). Solution: pin to
   digest.
3. **Runtime stack.** 4-layer architecture: kubelet (top) → containerd
   (CRI) → runc (kernel calls) → Linux kernel (foundation).

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
