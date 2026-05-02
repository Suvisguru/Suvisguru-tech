# Lesson 11 — Container Security · Rootless · Read-Only · Registries

> Course: Kubernetes — Common to all distributions
> Lesson 11 of 17 in K-COM. Module 2 · Lesson 4 of 5.
> Companion preview: `/preview-kubernetes-lesson-11.html`.

---

## 1. Concept

A container image alone is not secure. The runtime configuration around it
decides whether a single bug becomes a breached cluster or a contained
ticket. Two halves: **how the container runs** (security context) and
**where the image came from** (registries, pulls, signatures).

**Rootless / non-root user.** By default, the process inside a container
runs as root (UID 0). Combined with a kernel bug or a misconfigured
mount, that's a path to host-root. Set `runAsNonRoot: true` and
`runAsUser: 1000` in the pod's `securityContext`. The image must be built
to support a non-root user (your Dockerfile needs `USER 1000`).

**Read-only root filesystem.** `readOnlyRootFilesystem: true` makes the
container's filesystem immutable. An attacker who breaks in cannot drop
malware on disk, can't tamper with binaries, can't write a webshell.
If your app needs to write (logs, /tmp), mount a `emptyDir` at that path.

**Capabilities and seccomp.** Linux capabilities slice root power into
~40 pieces (CAP_NET_BIND_SERVICE, CAP_SYS_ADMIN, etc.). Best practice:
`drop: ["ALL"]`, then add only what's needed. Apply a seccomp profile
(`RuntimeDefault` is enough for most apps) to filter dangerous syscalls.

**Registry auth.** Public images on Docker Hub are pulled anonymously.
Private images need credentials. Create a `docker-registry` secret with
your registry username + password, reference it from the pod via
`imagePullSecrets`. Without this, the kubelet gets `ImagePullBackOff`.

**Pull policies.** Three options: `Always` (kubelet checks the registry
every time the pod starts; right for `:latest` and other mutable tags),
`IfNotPresent` (use the local copy if present; default for tagged
images; right for pinned versions), `Never` (require the image already
on the node; useful for air-gapped clusters and local development).

**Pod Security Standards.** Three levels Kubernetes ships out of the
box: **Privileged** (no restrictions), **Baseline** (block known-bad
patterns), **Restricted** (production-grade — non-root, drop caps,
read-only). Apply per namespace via labels.

---

## 2. Before / After

**Before — naive pod.** `image: my-app:latest`, no securityContext.
Container runs as root inside, with all 40 capabilities, with a writable
root filesystem, pulling a public image with a moving tag. An attacker
who finds an SSRF in the app gets a full root shell with write access.
Pull policy defaults to `Always` for `:latest` — every restart hits the
registry, sometimes pulling a different binary because someone re-pushed
the tag.

**After — hardened pod.** `image: registry.company.com/my-app@sha256:abc…`
(pinned digest, private registry). `securityContext: { runAsNonRoot: true,
runAsUser: 1000, allowPrivilegeEscalation: false, readOnlyRootFilesystem:
true, capabilities: { drop: [ALL] }, seccompProfile: RuntimeDefault }`.
`imagePullSecrets: [{ name: registry-creds }]`. `imagePullPolicy:
IfNotPresent`. Same SSRF now lands in a process that can't write to
disk, can't execute new privileged operations, and can't escalate.

What didn't change: the app still works. Hardening is operational, not
functional. The cost: a few lines of YAML, and image must be built
non-root-friendly (USER directive in Dockerfile).

---

## 3. Analogy — the fortified bank

A container registry is like a **bank vault**. Images are the safety
deposit boxes; the vault door (registry auth) decides who gets to take
one out. The **teller window** is the kubelet asking the registry "I'm
node-3, here are my credentials, give me image X." Without credentials,
the teller turns you away.

Once the box is out, the visitor doesn't get to roam the bank. They go
to a **glass inspection booth** — that's the container runtime. The
booth has rules: non-root visitor (`runAsNonRoot`), no tools allowed
(`drop: [ALL]` capabilities), display case is glass (`readOnlyRootFilesystem`),
and a security camera overhead recording every move (seccomp).

**The mapping:**

- Vault = container registry (Docker Hub, GHCR, ECR, GCR, ACR, Harbor)
- Vault door = registry auth
- Teller window = kubelet pulling on behalf of the pod
- Customer credentials = imagePullSecrets
- Inspection booth = the container's runtime sandbox
- Visitor wristband = non-root user (UID 1000)
- "No tools allowed" sign = drop ALL capabilities, allowPrivilegeEscalation: false
- Glass display case = readOnlyRootFilesystem: true
- Security camera = seccomp profile (RuntimeDefault)
- Bank security manager = Pod Security Standards (Privileged / Baseline / Restricted)
- Vendor seal on the box = image signing (cosign — covered in Lesson 10)

---

## 4. ELI5 / ELI10

**ELI5.** Imagine a bank. The vault holds boxes — those are the images.
You can't just walk in. The teller checks your card. Once you have a
box, you go to a glass room with a camera. You can't bring tools, can't
break the glass, and can't be the manager. The bank decides what's
allowed.

**ELI10.** Container security is two layers. First, where did the image
come from? You set imagePullSecrets so the kubelet can authenticate to
your private registry, and you set imagePullPolicy so the kubelet knows
when to re-fetch (Always for mutable tags like :latest, IfNotPresent
for pinned versions). Second, how does it run? The pod's securityContext
decides: runAsNonRoot prevents root, runAsUser pins a UID, capabilities
drop ALL strips Linux superpowers, readOnlyRootFilesystem locks the
disk, seccompProfile RuntimeDefault filters dangerous syscalls. All
together, this is the production-grade Pod Security Standards
"Restricted" profile. A single bug in your app can no longer become a
host-level compromise.

---

## 5. Real-world scenarios

**Container escape blocked by readOnlyRootFilesystem + non-root.**
A SaaS company's web app had an SSRF leading to RCE. The attacker
landed inside the container as UID 1000 (non-root) with a read-only
filesystem and ALL capabilities dropped. They couldn't write a malicious
binary, couldn't escalate to root, couldn't pivot to the host. The pod
was deleted; the deploy was hot-fixed by lunch. Same bug in 2018 took
out their staging cluster for a week.

**Private registry pull failed silently — fixed with imagePullSecret.**
A team migrated images from Docker Hub to their company's private
Harbor registry. Pods went into `ImagePullBackOff`. The kubelet logs
said "401 Unauthorized." Fix: create a `kubernetes.io/dockerconfigjson`
secret with Harbor credentials, add `imagePullSecrets: [name: harbor-creds]`
to the pod spec (or attach to a ServiceAccount used by all pods in the
namespace). Pods rolled out cleanly.

**Pull policy bug caused old code to keep running after a tag re-push.**
A team used `image: my-app:v2` and `imagePullPolicy: IfNotPresent`. They
re-pushed `v2` with a hotfix instead of cutting `v2.1`. Most nodes still
had the old `v2` cached and never pulled the new one — pods kept running
the old binary. Lesson: never re-push a tag. If you must push fresh
content under an existing tag, set `imagePullPolicy: Always`. Better:
pin to digest (`@sha256:abc…`) so the tag question goes away.

**Pod Security Standards "Restricted" caught a privileged pod attempt.**
A new dev tried to deploy a pod with `securityContext: { privileged:
true }` for "easier debugging." The namespace was labeled
`pod-security.kubernetes.io/enforce: restricted`. The API server
rejected the pod at admission: "violates PodSecurity 'restricted:latest'
- privileged is not allowed." Conversation moved from "let's just
allow it" to "let's fix the actual debugging tooling." Defaults won.

---

## 6. Animated illustration

Three modes:

1. **Pod admission with securityContext checks** (4 steps). A pod
   manifest with hardened securityContext arrives at the API server →
   admission controller checks each field (runAsNonRoot ✓, drop ALL ✓,
   readOnly ✓) → admitted. Then a privileged pod arrives → rejected.
2. **Image pull from private registry** (4 steps). Kubelet sees image
   ref `private.registry/my-app:v2` → looks up pod's imagePullSecret →
   auths to registry → pulls layers → starts container.
3. **Pull policy comparison** (4 steps). Same image deployed to three
   pods with different pullPolicy: `Always` (always hits registry),
   `IfNotPresent` (cache hit, no pull), `Never` (works only if cached,
   else fails). Watch network calls happen or not.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
