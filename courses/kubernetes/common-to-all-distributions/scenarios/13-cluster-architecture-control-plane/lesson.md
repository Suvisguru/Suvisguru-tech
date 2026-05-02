# Lesson 13 — Cluster Architecture · Control Plane &amp; Nodes

> Course: Kubernetes — Common to all distributions
> Lesson 13 of 17 in K-COM. Module 3 · Lesson 1 of 5.
> Companion preview: `/preview-kubernetes-lesson-13.html`.

---

## 1. Concept

A Kubernetes cluster is two distinct halves: a **control plane** (the
brain — decides what should run) and one or more **worker nodes** (the
muscle — actually runs the containers). They are different machines
with different jobs, talking over a network.

**The control plane.** Five processes, usually running on dedicated
"control plane nodes" (and never running your app workloads):

- **API server** (`kube-apiserver`) — the only door into the cluster.
  Every read, write, watch, and authentication request goes through here.
  Stateless, horizontally scalable.
- **etcd** — the strongly-consistent key-value store that holds the
  entire cluster state. Every object you've ever created lives here.
  Source of truth.
- **Controller manager** (`kube-controller-manager`) — runs dozens of
  reconcile loops (Deployment controller, ReplicaSet controller, Node
  controller, Endpoints controller, etc.). Each loop watches the API
  server for desired state, compares to actual state, takes action.
- **Scheduler** (`kube-scheduler`) — picks which node should run each
  newly-created pod, based on resource requests, affinity, taints,
  topology, and other constraints.
- **Cloud controller manager** (`cloud-controller-manager`) — bridges
  K8s to the cloud provider (load balancers, persistent disks, node
  lifecycle). Optional on bare metal.

**The worker nodes.** Every node — control plane or worker — runs
three things:

- **kubelet** — the node agent. Watches the API server for pods
  assigned to its node and tells the container runtime to start/stop
  them. Reports node status (CPU, memory, disk, conditions) back.
- **kube-proxy** — manages the local network rules (iptables, IPVS,
  or eBPF) that implement Kubernetes Services on each node.
- **Container runtime** — containerd, CRI-O, or runc-based — actually
  starts and stops the containers (covered in Lesson 09).

**The data flow.** When you run `kubectl apply -f pod.yaml`:
(1) kubectl sends the YAML to the **API server**.
(2) API server validates and writes to **etcd**.
(3) **Scheduler** sees an unscheduled pod, picks node-3, writes the
    binding back to API server → etcd.
(4) **kubelet** on node-3 watches the API server, sees the pod is
    bound to it, asks the container runtime to start it.
(5) Pod is Running. kubelet reports status back to API server.

Notice: nothing talks directly to etcd. Nothing talks directly between
controllers. **All communication goes through the API server.** That's
the architectural constraint that makes everything else possible.

**HA control plane.** In production: 3 (or 5) API servers behind a
load-balancer, 3 (or 5) etcd members in quorum, controller manager
and scheduler running with **leader election** (only one is active at
a time, others stand by). Lose one node → cluster keeps running.

**Managed vs self-managed.** EKS / GKE / AKS run the control plane for
you (you pay them, you manage worker nodes). Self-managed (kubeadm,
kops, k3s, RKE) means you run all of it. Most teams under 50 engineers
use managed.

---

## 2. Before / After

**Before — single binary, no separation.** Imagine one Linux process
running your app + a "scheduler" + a "config store" all together. If
that process dies, everything dies. Adding a second machine? Now those
two processes need to coordinate state, and you've invented half of
Kubernetes badly. Scaling, failover, and rolling updates are all you,
manually, on each machine.

**After — control plane + nodes.** The control plane is one logical
unit (HA-replicated under the hood). It owns the cluster state and
makes decisions. Worker nodes are interchangeable cattle — add or
remove them and the control plane reschedules workloads. The pod you
deployed yesterday survives a node failure tonight, because the
control plane noticed and re-created it elsewhere.

What changed: separation of concerns. The control plane decides; the
nodes do. Every Kubernetes feature builds on top of this split.

---

## 3. Analogy — air traffic control + airport terminals

A Kubernetes cluster is an **airport** with one **control tower** and
several **terminal buildings**. The tower (the control plane) is where
all the decisions happen. The terminals (worker nodes) is where
aircraft (your pods) actually park, board, and fly.

Inside the **tower**, five rooms:

- **Radio dispatch** at the top window (API server) — every plane,
  every request, every change announcement passes through this radio.
  Nobody else has authority to broadcast.
- **Flight plan archive** in the basement (etcd) — every plane that
  has ever existed, every assignment, every route, written down and
  duplicated for safety.
- **Specialist controllers** in offices (controller manager) — the
  "always-3-planes-on-this-route" controller, the "this-plane-needs-a-gate"
  controller, the "node-just-went-dark-replace-it" controller. Each
  watches its slice of the archive and acts.
- **Runway assignment desk** (scheduler) — when a new plane is
  declared, this desk decides which terminal/runway it goes to based
  on size, fuel, crew, weather.
- **Cloud liaison** (cloud controller manager) — the radio link to the
  outside world: getting power hookups, cargo trucks, and external
  navigation aids.

Inside each **terminal** (worker node), three roles:

- **Gate manager** (kubelet) — receives assignments from the tower
  ("park 737 at gate 4"), executes them, reports back ("plane parked,
  doors open, all systems green").
- **Ground crew router** (kube-proxy) — directs taxiing planes to the
  right gate using the local taxiway map (iptables/IPVS/eBPF rules).
- **Tug operator** (container runtime) — actually moves the planes;
  the runtime that starts and stops containers.

The tower never directly grabs a plane. It writes the assignment to
the archive; the gate manager picks it up. The gate manager never
calls another terminal directly; it goes through the tower's radio.
That single-door discipline is what makes the airport scale to
hundreds of terminals.

---

## 4. ELI5 / ELI10

**ELI5.** A control tower talks to terminals. Terminals park planes.
The tower decides where each plane goes, the terminal makes it happen.
If a plane crashes, the tower puts up a new one somewhere else.

**ELI10.** A K8s cluster has a brain (control plane) and muscles
(worker nodes). The brain has 5 parts: an `API server` (the only door
in), `etcd` (where state is stored), a `controller manager` (lots of
small loops keeping desired state matching reality), a `scheduler`
(picks which node runs which pod), and a `cloud-controller-manager`
(bridges to AWS/GCP/Azure). Each worker node runs `kubelet` (the agent
that runs your pods), `kube-proxy` (network rules for Services), and
a `container runtime` (containerd or CRI-O). When you `kubectl apply`,
your YAML goes to the API server, which writes it to etcd; the
scheduler picks a node and writes that back; the kubelet on that node
reads its assignment and tells the runtime to start the container.
**Everything talks through the API server, nothing talks directly.**

---

## 5. Real-world scenarios

**etcd lost quorum during a network partition — cluster went read-only.**
A 3-member etcd cluster across three AZs hit a network partition that
isolated 2 of the 3 nodes from each other. Quorum (majority) couldn't
be achieved → etcd switched to read-only → API server could serve gets
but not writes → no new pods scheduled, no failover, no Deployments
updated. Lesson: 5-member etcd survives 2 failures; 3-member only
survives 1. Across-AZ etcd needs careful quorum-zone planning.

**API server overloaded by too-aggressive controller — rate-limit fix.**
A custom controller was watching all pods and re-listing every second
("LIST pods every 1s"). At 8000 pods, that hammered the API server
with 480 MB/s of JSON. API server fell behind on write requests, kubectl
timed out cluster-wide. Fix: use proper informers (LIST once + WATCH
for diffs) and respect the API server's rate limits. Standard
controller-runtime libraries do this for you.

**Managed control plane (GKE) saved a startup from etcd backup nightmares.**
A 12-engineer startup ran self-managed K8s on EC2 with kubeadm. They
spent 30+ hours/month on etcd backups, version upgrades, and CP
patching. They migrated to GKE. Engineering time on cluster ops dropped
to zero. They paid $73/month per cluster for GKE; they paid one
engineer $14k/month before. Math is what it is.

**kube-scheduler bug pinned all pods to one node.**
A scheduler bug in a specific minor version caused all newly-created
pods to be assigned to the same node, ignoring resource constraints.
That node OOM'd and got cordoned. Subsequent pods went to the next
node, also OOM'd. Cascading failure. Workaround: deploy a second
scheduler (multi-scheduler is supported via `schedulerName` on the pod
spec) until the upstream fix landed. Real fix: upgrade.

---

## 6. Animated illustration

Three modes:

1. **Pod creation request flow** (5 steps). kubectl → API server →
   etcd → scheduler picks node → API server (binding) → kubelet on
   chosen node → container runtime → Pod Running.
2. **Reconcile loop in action** (4 steps). Deployment controller
   watches Deployment object (desired: replicas=3). Sees actual=2 (one
   pod just crashed). Creates a new ReplicaSet entry. ReplicaSet
   controller creates a Pod. Kubelet picks it up, starts container.
   Desired = actual.
3. **HA control plane: API + etcd quorum** (4 steps). 3 API servers
   behind a load-balancer (any can serve). 3 etcd members vote on
   every write (need 2/3 majority). Controller manager and scheduler
   run on all 3 but only the leader is active (lease in etcd). One
   node fails: quorum survives, leader re-elected, no downtime.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
