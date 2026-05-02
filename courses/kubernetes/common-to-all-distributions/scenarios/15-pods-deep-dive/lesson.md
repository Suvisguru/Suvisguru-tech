# Lesson 15 — Pods Deep Dive · Init · Sidecars · Ephemeral · QoS

> Course: Kubernetes — Common to all distributions
> Lesson 15 of 17 in K-COM. Module 3 · Lesson 3 of 5.
> Companion preview: `/preview-kubernetes-lesson-15.html`.

---

## 1. Concept

A **Pod** is the atomic unit of scheduling in Kubernetes. Not a
container — a *Pod*. The container is the unit of packaging; the Pod
is the unit Kubernetes actually places on a node and reasons about.
90% of pods have exactly one container, but the architectural rule
that says "one or more containers, scheduled together, sharing some
namespaces" is what enables the rest of Kubernetes.

**What's shared inside a Pod.** All containers in a pod share:

- **Network namespace** — same Pod IP, same port space. Containers
  can talk to each other on `localhost:port`.
- **IPC namespace** — POSIX shared memory, semaphores.
- **(Optional) PID namespace** — `shareProcessNamespace: true` lets
  containers see each other's processes.
- **Volumes** — any volume mounted at the pod level can be mounted by
  any container.

**What's NOT shared by default.** Each container has its own
**filesystem (mount) namespace** and its own **PID namespace**. Each
container is also independently restartable.

**The pause container.** Under the hood, every pod has an invisible
`pause` container that's always PID 1 in the pod's network/IPC
namespaces. Its only job: hold those namespaces open so individual app
containers can come and go without losing the pod's IP. You'll see it
on a node with `crictl ps`, but you don't write YAML for it.

**Init containers.** Run-to-completion containers that execute
*sequentially before* any main containers start. Common uses: wait for
a database to be reachable, copy config files into a shared volume,
run a schema migration. If an init container fails, the kubelet keeps
retrying it until it succeeds (or the pod's `restartPolicy` says
otherwise). Main containers don't start until all inits exit 0.

**Sidecar containers.** A second container in the pod that supports
the main one — log shipping, metrics scraping, service mesh proxy
(Envoy/Linkerd), TLS termination. The classic pattern for ~10 years.
**K8s 1.28+ adds native sidecar support**: declare a container in
`initContainers` with `restartPolicy: Always` — it starts before the
main containers, stays running, and is properly handled at shutdown
(main containers exit first, then sidecars). This solves the long-
standing "sidecar dies during shutdown and breaks the main container's
last requests" problem.

**Multi-container patterns** (Brendan Burns's classic taxonomy):
- **Sidecar** — augments the main container (log shipper, mesh proxy)
- **Ambassador** — proxies an external service for the main container
  (e.g., a connection-pooling proxy in front of a remote DB)
- **Adapter** — exposes the main container's data in a different
  format (e.g., translates app metrics into Prometheus format)

**Ephemeral containers.** Added at runtime via
`kubectl debug -it <pod> --image=busybox --target=<container>`.
Doesn't restart the pod. Critical for debugging **distroless**
containers (Lesson 10) that have no shell. The ephemeral container
can share the target container's PID namespace and inspect its
processes/files.

**Resource requests and limits.**
- **request** — the floor; the scheduler reserves this much capacity
  on the node and won't pack the node past 100% of requests.
- **limit** — the ceiling; CPU usage above limit is throttled, memory
  usage above limit triggers an OOM kill.

**QoS classes** (computed automatically from requests/limits):
- **Guaranteed** — every container has CPU and memory `request == limit`.
  Highest priority, last to be evicted.
- **Burstable** — at least one container has a request, but request &lt;
  limit (or limit unset). Most production pods.
- **BestEffort** — no requests or limits anywhere. First to be evicted
  under pressure. Don't use for production workloads.

**Restart policy** (pod-level, applies to all containers):
- **Always** (default) — restart any exited container. Used by
  Deployments, StatefulSets, DaemonSets.
- **OnFailure** — restart only on non-zero exit. Used by Jobs.
- **Never** — don't restart. Used by Jobs that should fail loudly.

---

## 2. Before / After

**Before — naive multi-process container.** A team wants their app +
log shipper in the same package. They build a single Docker image with
a shell script that starts both processes (`./app & ./fluent-bit`).
Problems: the shell becomes PID 1 (Lesson 12), signals don't forward,
neither process is independently restartable, the `:latest` tag
couples their lifecycles, scaling one means scaling the other.

**After — Pod with sidecar.** Same workload, two separate container
images in one Pod. Main container is just the app. Sidecar container
is the log shipper. They share a volume (or use the shared network
to talk). Each restarts independently. Each has its own image lifecycle.
Each has its own resource requests and limits. The kubelet handles
PID 1, signal forwarding, and zombies for each container separately.

What didn't change: the app and the log shipper still cooperate. What
changed: they're cleanly separated, independently versioned, and
properly lifecycle-managed.

---

## 3. Analogy — the shared studio apartment

A Pod is a **shared studio apartment**. The containers are
**roommates**. They share the **kitchen** (network namespace — they
can chat from across the room via `localhost`) and the **bathroom**
(IPC), but each has their own **bedroom** (separate filesystem, often
separate PID namespace). The apartment has one **doorbell** (the Pod
IP) that any roommate can answer.

Before anyone moves in, the **handyman** (init container) shows up,
finishes the wifi setup, hangs the curtains, and leaves. Only then do
the roommates move in.

The **main roommate** does the actual work — let's say writes code.
The **sidecar housemate** does laundry quietly in the background, or
answers the door for the main roommate (ambassador), or translates
when guests speak a different language (adapter). Sidecars are part of
the household, not visitors.

When something breaks and the main roommate doesn't have a screwdriver
(distroless image, no shell), a **plumber** can drop in temporarily
(ephemeral debug container) — they don't move in, they just visit,
fix the problem, and leave. The apartment doesn't get evicted to bring
the plumber in.

The apartment building's superintendent (the kubelet) decides whether
to give your apartment **guaranteed rent control** (QoS Guaranteed,
last to evict in a crunch), **flexible rent** (Burstable), or **first
to be asked to leave** (BestEffort) based on how much electricity and
water you reserved.

**The mapping:**

- Apartment = Pod (atomic unit, shares an address)
- Roommates = containers in the pod
- Shared kitchen = network namespace (talk via localhost)
- Shared bathroom = IPC namespace
- Separate bedrooms = filesystem &amp; PID namespaces (per container)
- Doorbell at the front = Pod IP
- Handyman who came first = init container
- Helpful housemate = sidecar
- Doorman = ambassador container
- Translator = adapter container
- Visiting plumber = ephemeral debug container
- Building superintendent = kubelet
- Reserved utilities = resource requests
- Maximum utilities allowed = resource limits
- Rent-control class = QoS class (Guaranteed / Burstable / BestEffort)

---

## 4. ELI5 / ELI10

**ELI5.** A pod is an apartment. The containers inside are roommates
who share the kitchen and bathroom. A handyman comes first to fix
things up; then the roommates move in. One roommate works; the others
help. If something breaks and you don't have tools, a plumber visits
just to fix it. The building manager decides who has to leave first if
the building gets crowded.

**ELI10.** A Pod is the atomic unit of scheduling in K8s — not a
container. Containers in a pod share network and IPC namespaces (they
can talk via `localhost`) but have separate filesystems and PIDs by
default. Init containers run sequentially to completion before main
containers start. **Sidecars** support the main container (log
shipping, mesh proxy); since K8s 1.28, native sidecars are init
containers with `restartPolicy: Always`. **Ephemeral containers** are
added at runtime via `kubectl debug` — critical for distroless
containers with no shell. Each container has resource `requests`
(scheduler-reserved floor) and `limits` (kill ceiling); the combination
determines the pod's **QoS class** (Guaranteed / Burstable /
BestEffort). The pause container holds the pod's network namespace open
so app containers can come and go without losing the IP.

---

## 5. Real-world scenarios

**Init container blocked startup until the database was reachable.**
A web app needed PostgreSQL ready before starting. Engineers added
sleeps in the entrypoint, sometimes hit races. Fix: `initContainers:
[{ name: wait-db, image: busybox, command: ["sh","-c","until nc -z db
5432; do sleep 1; done"] }]`. Pod doesn't transition to Running until
the init exits 0 — guaranteed db-ready. No more flaky cold starts.

**Log-shipping sidecar replaced 12 different agents on each VM.**
Pre-K8s, every team installed their own log agent on each VM (different
versions, different configs). Audit nightmare. After K8s: one
standardized fluent-bit sidecar in every pod template (or, better, a
DaemonSet — Lesson 16). Logs flow to one collector. Each app pod still
has its own logging behavior but it's all one ship-mechanism.

**`kubectl debug` saved an outage when the main container had no shell.**
Production app started returning 500s. Image was `gcr.io/distroless/python3`
— no `/bin/sh` to exec into. `kubectl exec -it ... bash` failed with
"executable file not found." Engineer ran `kubectl debug -it broken-pod
--image=busybox --target=app -- sh`. Got a shell in a sibling container
sharing the broken container's PID namespace. Found the broken file
descriptor in seconds. Distroless safety + ephemeral debug = best of
both.

**QoS confusion: Guaranteed pods kept getting OOM-killed.**
A team set `requests.memory: 1Gi`, `limits.memory: 1Gi` (Guaranteed
class). Their app legitimately spiked to 1.2Gi during traffic bursts.
OOM-kills every burst. They didn't realize Guaranteed means
"hard-cap at limit" — exceeding limit = kill, regardless of class.
Fix: either raise limit (now Burstable if request stays at 1Gi) or
size the app so peak fits under limit. QoS doesn't grant extra
memory; it determines eviction priority when the *node* is under
pressure.

---

## 6. Animated illustration

Three modes:

1. **Pod startup with init containers** (4 steps). pause starts →
   init-1 runs and exits 0 → init-2 runs and exits 0 → main + sidecar
   start in parallel.
2. **Sidecar in action: log shipping** (4 steps). main writes
   `/var/log/app.log` to a shared `emptyDir` volume → sidecar
   `fluent-bit` tails it from the same volume → forwards to a
   remote log backend → ack received.
3. **`kubectl debug` adds an ephemeral container** (4 steps). Pod is
   broken (distroless main, no shell). User runs `kubectl debug -it
   broken --image=busybox --target=app`. Ephemeral busybox container
   joins the pod, sharing PID namespace with main. User inspects;
   finds the issue.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
