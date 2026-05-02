#!/usr/bin/env python3
"""Produce per-lesson scenario folders for L16-L44.

For each lesson, writes the four canonical files (mirror of the L01-L15
pattern) under courses/kubernetes/common-to-all-distributions/scenarios/{nn-slug}/:

  - brief.yaml     intake brief (concise version — central metaphor,
                   prereqs, learning outcomes, structure, fact-check)
  - lesson.md      lesson markdown copy (sections + before/after +
                   analogy + ELI5/10 + scenarios + misconceptions +
                   recap)
  - flashcards.yaml  flashcards as data
  - quiz.yaml        quiz questions as data

Source of truth:
  - L19-L44: scripts/lessons/lessonNN.py LessonSpec
  - L16-L18: extracted from preview HTML by hand-mapped data below
    (L16/L17/L18 predate the lesson generator; their data is mirrored
    here from the committed HTML for completeness)

Idempotent — running twice overwrites files; doesn't lose existing
folders for lessons not in this batch.
"""

import importlib.util
import os
import re
import sys
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENARIOS = os.path.join(ROOT, "courses/kubernetes/common-to-all-distributions/scenarios")
LESSONS_DIR = os.path.join(ROOT, "scripts/lessons")
sys.path.insert(0, LESSONS_DIR)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from k8s_lesson_generator import LessonSpec  # noqa: E402

# Slug + module assignments per lesson
LESSON_META = {
    "16": ("16-workload-controllers", "Module 4 · Workloads · Lesson 1 of 5", "Workload Controllers · Deployment, StatefulSet, DaemonSet, Job, CronJob"),
    "17": ("17-services-and-networking", "Module 5 · Networking 101 · Lesson 1 of 1", "Services & Networking · ClusterIP, NodePort, LoadBalancer, Ingress, NetworkPolicy"),
    "18": ("18-storage-pt1-pv-pvc-storageclass", "Module 9 · Storage · Lesson 1 of 2", "Storage Part 1 · PV, PVC, StorageClass"),
    "19": ("19-storage-pt2-csi-snapshots", "Module 9 · Storage · Lesson 2 of 2", "Storage Part 2 · CSI, Snapshots, Cloning, VolumeAttributesClass"),
    "20": ("20-configuration-and-secrets", "Module 10 · Config & Identity · Lesson 1 of 2", "Configuration & Secrets · ConfigMap, Secret, KMS, External Secrets Operator"),
    "21": ("21-serviceaccounts-and-certificates", "Module 10 · Config & Identity · Lesson 2 of 2", "ServiceAccounts & Certificates · Tokens, Projected JWTs, cert-manager, Cluster PKI"),
    "22": ("22-scheduling-pt1-affinity-taints-spread", "Module 11 · Scheduling · Lesson 1 of 2", "Scheduling Part 1 · Affinity, Taints, Topology Spread"),
    "23": ("23-scheduling-pt2-priority-dra-numa", "Module 11 · Scheduling · Lesson 2 of 2", "Scheduling Part 2 · Priority, DRA, NUMA, Profiles"),
    "24": ("24-networking-foundations-cni", "Module 12 · Networking depth · Lesson 1 of 3", "Networking Foundations · Linux Primitives, CNI, MTU"),
    "25": ("25-gateway-api", "Module 12 · Networking depth · Lesson 2 of 3", "Gateway API · Roles, Listeners, Routes, and the Ingress Sunset"),
    "26": ("26-adminnetworkpolicy-fqdn", "Module 12 · Networking depth · Lesson 3 of 3", "AdminNetworkPolicy & FQDN-Based Egress"),
    "27": ("27-rbac-and-authentication", "Module 13 · Security · Lesson 1 of 5", "RBAC & Authentication · Roles, Bindings, OIDC, Structured Auth"),
    "28": ("28-admission-control", "Module 13 · Security · Lesson 2 of 5", "Admission Control · ValidatingAdmissionPolicy, PSA, Webhooks"),
    "29": ("29-policy-engines-kyverno-gatekeeper", "Module 13 · Security · Lesson 3 of 5", "Policy Engines · Kyverno and OPA Gatekeeper in Depth"),
    "30": ("30-supply-chain-security", "Module 13 · Security · Lesson 4 of 5", "Supply Chain Security · Cosign, Sigstore, SLSA, SBOM"),
    "31": ("31-multi-tenancy-and-hardening", "Module 13 · Security · Lesson 5 of 5", "Multi-Tenancy & Hardening · Quotas, Limits, kube-bench, Hierarchies"),
    "32": ("32-observability-pt1-logs-metrics", "Module 14 · Observability · Lesson 1 of 2", "Observability Part 1 · Logs and Metrics"),
    "33": ("33-observability-pt2-traces-ebpf-slo", "Module 14 · Observability · Lesson 2 of 2", "Observability Part 2 · Traces, eBPF, SLOs"),
    "34": ("34-autoscaling-hpa-vpa-keda-karpenter", "Module 15 · Capacity & Resilience · Lesson 1 of 2", "Autoscaling · HPA, VPA, KEDA, Cluster Autoscaler, Karpenter"),
    "35": ("35-reliability-ha-pdb-multi-zone-dr", "Module 15 · Capacity & Resilience · Lesson 2 of 2", "Reliability & HA · PDB, Multi-Zone, Regional DR"),
    "36": ("36-kustomize", "Module 16 · Application Delivery · Lesson 1 of 2", "Kustomize · Overlay-Based Manifest Customisation"),
    "37": ("37-helm-3", "Module 16 · Application Delivery · Lesson 2 of 2", "Helm 3 · Charts, Values, Hooks, OCI"),
    "38": ("38-gitops-argo-cd", "Module 17 · GitOps · Lesson 1 of 3", "GitOps with Argo CD · Application CRD, Sync, Drift Detection"),
    "39": ("39-gitops-flux-cd", "Module 17 · GitOps · Lesson 2 of 3", "GitOps with Flux CD · Multi-Controller Architecture"),
    "40": ("40-progressive-delivery-rollouts-flagger", "Module 17 · GitOps · Lesson 3 of 3", "Progressive Delivery · Argo Rollouts and Flagger"),
    "41": ("41-crds-deep-dive", "Module 18 · Extending K8s · Lesson 1 of 3", "CRDs Deep Dive · Schema, CEL, Conversion Webhooks"),
    "42": ("42-operators-kubebuilder", "Module 18 · Extending K8s · Lesson 2 of 3", "Operators with Kubebuilder · controller-runtime, OLM"),
    "43": ("43-service-mesh-istio-linkerd-cilium", "Module 18 · Extending K8s · Lesson 3 of 3", "Service Mesh · Istio Ambient, Linkerd, Cilium Mesh"),
    "44": ("44-troubleshooting-methodology", "Module 19 · Capstone · Lesson 1 of 1", "Troubleshooting Methodology + Drills (Capstone)"),
}


def load_spec(num: str) -> LessonSpec | None:
    """Load lessonNN.py if it exists; return None for L16-L18 (no spec)."""
    path = os.path.join(LESSONS_DIR, f"lesson{num}.py")
    if not os.path.exists(path):
        return None
    spec_spec = importlib.util.spec_from_file_location(f"lesson{num}", path)
    mod = importlib.util.module_from_spec(spec_spec)
    spec_spec.loader.exec_module(mod)
    return mod.LESSON


def yaml_escape(s: str) -> str:
    """Minimal YAML string escape — wrap in single quotes if needed."""
    return s.replace("'", "''")


def html_to_md(s: str) -> str:
    """Strip HTML tags + entities for markdown bodies. Keep <code> as backticks
    and <strong>/<em> as ** / *."""
    s = re.sub(r'<code>(.*?)</code>', r'`\1`', s, flags=re.DOTALL)
    s = re.sub(r'<strong>(.*?)</strong>', r'**\1**', s, flags=re.DOTALL)
    s = re.sub(r'<em>(.*?)</em>', r'*\1*', s, flags=re.DOTALL)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', s, flags=re.DOTALL)
    s = re.sub(r'</?(ul|ol|p|h\d|div|span|table|thead|tbody|tr|th|td|a|pre)[^>]*>', '', s, flags=re.IGNORECASE)
    s = re.sub(r'<[^>]+>', '', s)  # any other tags
    # entities
    s = (s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
           .replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' '))
    return s.strip()


def block_quote(s: str, prefix: str = "  ") -> str:
    """Indent each line for YAML block scalars."""
    return "\n".join(prefix + line for line in s.splitlines())


# ---------------------------------------------------------------------------
# Hand-mapped data for L16, L17, L18 (no Python spec exists; they predate
# the generator). Each entry holds the bits we need for brief + lesson +
# flashcards + quiz. Sourced from the committed preview HTML, condensed.
# ---------------------------------------------------------------------------

L16_DATA = {
    "central_metaphor": "K-Town Dispatch Office — workforce dispatch service. Deployments are rotating shifts (interchangeable workers, last-out-first-in roll); StatefulSets are assigned-seat employees (Anna at desk-0, Brian at desk-1, identity persists); DaemonSets are the one-per-building watchman; Jobs are one-time work orders; CronJobs are the scheduled maintenance round.",
    "outcomes": [
        "Pick the right controller for a given workload (Deployment vs StatefulSet vs DaemonSet vs Job vs CronJob).",
        "Read a Deployment YAML and explain the rolling-update strategy.",
        "Understand why StatefulSet Pods get stable identities + ordered startup.",
        "Know when DaemonSet beats Deployment+nodeAffinity.",
        "Convert a one-shot script to a Job; a recurring script to a CronJob.",
    ],
    "stamp": "Five workload controllers, each for a specific shape of work — match shape to controller, the rest is mostly tuning.",
    "flashcards": [
        ("Five workload controllers?", "Deployment (stateless rolling updates), StatefulSet (stable identity per replica), DaemonSet (one Pod per node), Job (run-to-completion), CronJob (scheduled Job)."),
        ("Deployment vs StatefulSet?", "Deployment: interchangeable Pods; can swap names; rolling update by ReplicaSet. StatefulSet: stable Pod names (web-0, web-1), stable storage per Pod (volumeClaimTemplates), ordered startup/shutdown."),
        ("DaemonSet use cases?", "Per-node infrastructure: log collectors (Fluent Bit), monitoring agents (node-exporter), CNI plugins, storage drivers, security tools (Falco). Anywhere you need exactly one Pod per node."),
        ("Job vs CronJob?", "Job: run a Pod to successful completion (a one-shot batch task). CronJob: a Job on a schedule (cron expression). CronJob creates Job objects on schedule; Job creates Pods."),
        ("ReplicaSet — when do you use it directly?", "Almost never. You use Deployment, which manages ReplicaSets for you. Direct ReplicaSet use is for very specific cases (custom controllers managing their own rollouts)."),
        ("StatefulSet ordered startup?", "Pods come up one at a time, in numeric order: web-0 starts and becomes Ready before web-1 starts. Ordered scale-down too: web-N deleted before web-(N-1). Use podManagementPolicy: Parallel to disable."),
        ("Where does volumeClaimTemplates live?", "On the StatefulSet spec. Each replica gets its own PVC named after the Pod (data-web-0, data-web-1). PVCs are NOT deleted when the StatefulSet is — intentional, so you can recreate without data loss."),
        ("HPA + Deployment vs HPA + StatefulSet?", "Both work. HPA targets either via scaleTargetRef. StatefulSet HPA scales 0→N: the Nth Pod waits for (N-1) to be Ready first. Plan startup time for stateful workloads accordingly."),
    ],
    "quiz": [
        ("A team's nightly report-generator runs as a Deployment with `replicas: 1`. The Pod runs 4 hours, exits, then K8s restarts it because Deployment expects it Running. What's the right fix?",
         "Convert to a CronJob (or a Job if it's truly one-time). Deployment is wrong here because it's designed for long-running services that should always be Running. Job is designed exactly for run-to-completion semantics: the Pod runs, exits 0, the Job records success, K8s doesn't restart. CronJob wraps Job in a schedule. Spec example:\n\n```yaml\napiVersion: batch/v1\nkind: CronJob\nmetadata:\n  name: nightly-report\nspec:\n  schedule: '0 2 * * *'\n  jobTemplate:\n    spec:\n      template:\n        spec:\n          restartPolicy: OnFailure\n          containers:\n          - name: report\n            image: report:v1\n```"),
        ("A Postgres team uses Deployment instead of StatefulSet. Each Pod has a PVC mounted. They scale 1 → 3 replicas. What goes wrong?",
         "Multiple problems: (1) all 3 replicas try to mount the same PVC (RWO conflict). (2) Pods get random names, so client config can't reference a specific replica. (3) No ordered startup — the followers might come up before the primary is ready. (4) On Pod replacement, the new Pod gets a new name and may not match the existing data layout. The fix is StatefulSet with volumeClaimTemplates: each replica gets its own PVC, stable Pod names (postgres-0, postgres-1), ordered startup, predictable identity."),
        ("Your team uses a DaemonSet for a logging agent. They want to roll out a new version with zero downtime. What's the strategy?",
         "DaemonSet supports `updateStrategy: RollingUpdate` with `maxUnavailable` controlling how many node-Pods can be down simultaneously. Default is 1 (one node at a time — slow but safe). For a 1000-node cluster you might bump to 10% to roll faster. Combined with PodDisruptionBudget you can also limit the total fleet downtime. Each node's Pod is independent, so rolling-update means 'update Pod on node-A, wait for Ready, move to node-B'. Skip OnDelete strategy unless you need manual control."),
    ],
    "stops": "Real K8s controllers don't 'dispatch workers' — they reconcile observed state with desired state in a control loop. The dispatch metaphor undersells the level-triggered, idempotent reconciliation that's the secret to K8s's robustness.",
    "scenarios": [
        ("A SaaS using Deployment + HPA for stateless web", "Deployment with replicas tied to HPA. Rolling updates happen automatically on image bumps (via Argo CD or kubectl set image). Service in front routes to the current ReplicaSet. Cookie-cutter K8s pattern that works at any scale."),
        ("A bank running PostgreSQL on StatefulSet", "Three replicas (postgres-0 primary, postgres-1/2 replicas). Each has its own PVC via volumeClaimTemplates. Headless Service for clients to address specific Pods (postgres-0.postgres.namespace.svc). StatefulSet handles rolling restarts in reverse-ordinal order during upgrades."),
        ("A team running Falco as a DaemonSet for runtime security", "One Falco Pod per node. Watches kernel syscalls via eBPF. Cluster-wide visibility without per-Pod overhead. Tolerations on master nodes too — security applies everywhere."),
        ("A startup's image-resize Job", "Customer uploads → SQS message → CronJob (every 1 min) checks queue. If items present, spawns Job to drain them. Job creates Pods that process N images then exit. Failed Pods retry up to backoffLimit; after that, Job marked Failed and alerted."),
    ],
    "misconceptions": [
        ("Deployments and ReplicaSets are interchangeable.", "Deployment is the higher-level abstraction; it manages ReplicaSets to do rolling updates. You write Deployment; you read ReplicaSet history. Direct ReplicaSet usage is rare."),
        ("StatefulSet is required for any Pod with state.", "StatefulSet is required for stable identity + per-replica storage. A single-replica stateful app can run as a Deployment with a PVC. The bar is: do you need stable, predictable Pod names + ordered startup? If yes, StatefulSet."),
        ("CronJob's schedule is reliable.", "It's best-effort. If the cluster is busy or the previous Job is still running, the next schedule may be skipped (per concurrencyPolicy). For mission-critical scheduling, layer on top: monitoring + alerting on missed runs."),
    ],
    "before": "Manage workloads as raw Pods + scripts. Restart by hand. Scale by editing YAML. No standardised rollout. Configuration drift between environments is common.",
    "after": "Five workload controllers cover ~95% of needs. Deployment for stateless, StatefulSet for stable identity, DaemonSet for per-node, Job/CronJob for batch. Rolling updates declarative. Scale via HPA. Drift impossible because git is source of truth.",
    "before_after_caption": "K8s's workload controllers are the most-used surface of the API. Get the pattern matching right and most operational complexity disappears.",
    "analogy_intro": "K-Town's Dispatch Office handles every kind of work assignment. **Rotating shifts** (Deployments) — anyone can take any slot, last shift's worker rolls off as the next rolls on. **Assigned-seat workers** (StatefulSets) — Anna always at desk-0, Brian at desk-1, even after a break. **Per-building watchmen** (DaemonSets) — exactly one per building. **One-time work orders** (Jobs) — do this and report back. **Scheduled rounds** (CronJobs) — every Tuesday at 2 AM, do that.",
    "translation_rows": [
        ("Rotating shifts (interchangeable workers)", "Deployment + ReplicaSet"),
        ("Assigned-seat employees (Anna at desk-0)", "StatefulSet"),
        ("Per-building watchman", "DaemonSet"),
        ("One-time work order", "Job"),
        ("Scheduled maintenance round", "CronJob"),
        ("\"Cover the shift no matter who\"", "Rolling update strategy"),
        ("\"Anna's badge stays Anna's badge\"", "Stable Pod identity in StatefulSet"),
    ],
    "eli5": "Five kinds of jobs at the dispatch office. Some workers can swap places (Deployment). Some always sit at the same desk (StatefulSet). Some are stationed at every building (DaemonSet). Some come in once for one task (Job). Some come in every Tuesday (CronJob).",
    "eli10": "Five workload controllers for five shapes of work: Deployment (stateless, rolling updates), StatefulSet (stable Pod names + per-replica PVCs + ordered startup), DaemonSet (one Pod per node — agents, log shippers), Job (run-to-completion — backoffLimit + completions + parallelism), CronJob (Job on a schedule). Pick by shape; don't fight the model.",
    "recap_lead": "Five workload controllers cover almost every shape of work in K8s. Match the shape to the controller; the rest is tuning replicas, probes, and resource requests.",
    "recap_next": "Next — Lesson 17: Services & Networking. The other half of the workload story: how Pods reach each other and how the world reaches in.",
    "fact_check_anchors": [
        "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/",
        "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/",
        "https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/",
        "https://kubernetes.io/docs/concepts/workloads/controllers/job/",
        "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/",
    ],
}

L17_DATA = {
    "central_metaphor": "K-Town Switchboard — the city's telephone exchange and street-routing system. Pods are buildings; Pod IPs are house numbers (change every renovation). Services are stable phone lines that always reach the right building. ClusterIP = internal directory; NodePort = phone booth on every block; LoadBalancer = dispatch operator with a public number; ExternalName = phone-book alias; Ingress = the city's main-entrance turnstile (host/path routing for HTTP); NetworkPolicy = the traffic rules deciding who-may-call-whom.",
    "outcomes": [
        "Explain why Pod IPs aren't the right abstraction to depend on.",
        "Pick the right Service type for a given exposure scenario.",
        "Write a Service spec selecting Pods by label.",
        "Choose between Ingress and Gateway API for HTTP exposure.",
        "Author a default-deny NetworkPolicy and one explicit allow.",
    ],
    "stamp": "Pods come and go; Services give them stable names. Four flavours of Service plus Ingress for HTTP plus NetworkPolicy for who-can-talk-to-whom.",
    "flashcards": [
        ("Why don't Pods have stable IPs?", "Pod IPs are assigned from the cluster network at scheduling time. When a Pod restarts, dies, or is rescheduled, it gets a fresh IP. Hardcoding a Pod IP is hardcoding tomorrow's outage."),
        ("Four Service types?", "ClusterIP (internal), NodePort (each node's high port), LoadBalancer (cloud LB), ExternalName (DNS alias to external host)."),
        ("When use ClusterIP?", "For Pod-to-Pod traffic inside the cluster. The default. The most common type — every internal microservice gets one."),
        ("When use LoadBalancer?", "On a cloud cluster, exposing a non-HTTP service (or a single HTTP service) to the public internet. The cloud-controller-manager provisions an external LB."),
        ("Ingress vs Service?", "A Service exposes a group of Pods at L4 (TCP/UDP). An Ingress is an L7 (HTTP/HTTPS) router in front of Services — host-based and path-based routing, TLS termination, shared LB."),
        ("Headless Service?", "A Service with `clusterIP: None`. DNS returns the IPs of all backing Pods directly (multiple A records) instead of a single virtual IP. Used for StatefulSets where callers need each Pod's identity."),
        ("NetworkPolicy default behaviour?", "Default-allow. Every Pod can reach every other Pod, and the public internet, until a NetworkPolicy selects it. Then it becomes default-deny — only the rules you wrote allow traffic."),
        ("Gateway API?", "The next-gen replacement for Ingress. Same job, more expressive, role-separated APIs (Gateway = cluster-operator-owned; HTTPRoute / TCPRoute = app-team-owned). New clusters often ship both."),
    ],
    "quiz": [
        ("A team has 30 microservices behind one Ingress controller. They want to add a new service available at `api.acme.com/inventory`. Walk through what they create.",
         "Three things. (1) A Deployment running the inventory service Pods (with labels `app=inventory`). (2) A ClusterIP Service named `inventory` that selects those Pods on the right port. (3) An Ingress rule (either appended to the existing Ingress resource or a new one) saying 'traffic to `api.acme.com/inventory` goes to the `inventory` Service.' The shared Ingress controller already terminates TLS at `api.acme.com`; this is just one more route. No new cloud LB; same external IP serves the new endpoint."),
        ("A team's `kubectl get pods` shows three replicas of the front-end with three different IPs. They want to load-balance traffic across all three. They write the front-end's URL into the back-end's config as `http://10.0.4.7:80`. Why is this wrong, and what's the right fix?",
         "Two problems. (1) `10.0.4.7` is one specific Pod's IP. The other two Pods get no traffic; if that Pod dies, the back-end breaks. (2) That IP changes on every restart. Fix: create a ClusterIP Service named `frontend` that selects all three Pods by label. Reference it as `http://frontend` (or `frontend.default.svc.cluster.local`) from the back-end. The Service load-balances across all matching Pods, and survives Pod churn. This is the Service abstraction's whole point."),
        ("Your front-end Pod hardcodes the database connection string to a Pod IP it discovered with `kubectl describe pod`. `DATABASE_URL=postgres://10.0.5.7:5432/app`. What happens at the next database restart?",
         "The database Pod restarts (a routine event — node maintenance, image update, eviction under memory pressure). Comes back up with a fresh IP, `10.0.6.2`. The front-end keeps trying `10.0.5.7`. Every API request returns a connection-refused error. The error message in the logs is generic; the underlying cause (the IP changed) is invisible without manual investigation. **Fix:** never use Pod IPs directly. Create a ClusterIP Service for Postgres; reference it by DNS name (`postgres.default.svc.cluster.local`, or just `postgres` in the same namespace). The Service tracks healthy backing Pods and routes accordingly. Pod IPs become an implementation detail you never see."),
    ],
    "stops": "Real Service IPs are virtual — kube-proxy or eBPF translates them to backend Pod IPs at the kernel level. The 'phone line' metaphor undersells how many translations happen per packet, and where they happen (every node, in iptables/IPVS/eBPF).",
    "scenarios": [
        ("A SaaS exposing one HTTPS service per customer", "Each customer gets a unique Ingress with their domain (acme-corp.app.example.com). All Ingresses share one cloud LB; nginx-ingress terminates TLS using cert-manager-issued certs. Adding a customer = one Ingress YAML + DNS record. Zero per-customer infrastructure cost."),
        ("A trading firm running internal-only services", "Every internal service is ClusterIP. NetworkPolicy enforces default-deny on every namespace. Specific allow rules let trading apps reach Postgres + Redis on specific ports; everything else is blocked, including the public internet. A compromised app can't even DNS-lookup an external host."),
        ("A logging platform on a DaemonSet", "Fluent Bit runs as a DaemonSet — one Pod per node. App Pods write logs to `localhost:24224`; the local Fluent Bit batches and ships them to a central log store. No Service needed for that internal communication — the agent is on the same node, reachable via `hostNetwork`. Cuts cross-node traffic for logs to zero."),
        ("A multi-tenant cluster with namespace isolation", "Each tenant gets a namespace. NetworkPolicy uses namespace selectors to enforce: tenant Pods can talk inside their own namespace + to `kube-system` (DNS) + to `monitoring` (Prometheus scraping) — and that's it. Cross-tenant traffic is blocked at the network layer."),
    ],
    "misconceptions": [
        ("Services have IPs, so the IP is the right thing to use in app config.", "Use the Service *name* (DNS), not the Service IP. The Service IP is stable but coupling to it ties you to one cluster's CIDR. Names work everywhere."),
        ("A LoadBalancer Service is the only way to expose HTTP traffic.", "For HTTP, an Ingress controller (or Gateway API) is more flexible — host and path routing, TLS termination, one cloud LB shared across many services. LoadBalancer is for non-HTTP or single-service setups."),
        ("NetworkPolicy is on by default; my Pods are isolated.", "By default every Pod can talk to every other Pod in the cluster. NetworkPolicy is opt-in — you write rules to restrict, otherwise everything is open. Default-deny is a posture you have to *configure*."),
    ],
    "before": "App-to-app via hardcoded Pod IPs. Restart breaks everything. No traffic policy. External access via SSH tunnels and prayer. Adding a new exposed service means an LB ticket to the cloud team.",
    "after": "Services give every workload a stable name. ClusterIP for internal, Ingress for HTTP, LoadBalancer for L4 public. NetworkPolicy enforces who-talks-to-whom. New endpoints are PRs, not tickets.",
    "before_after_caption": "Service / Ingress / NetworkPolicy is the trinity of K8s networking. Get the abstractions right and the network mostly disappears as a concern.",
    "analogy_intro": "The K-Town Switchboard is the city's telephone exchange. Buildings (Pods) move and renumber constantly; the Switchboard maintains stable phone lines (Services) that always reach the right building today. Internal calls go through the directory (ClusterIP); external calls reach a public number (LoadBalancer) or the city's main turnstile (Ingress). Traffic rules (NetworkPolicy) decide who's allowed to call whom.",
    "translation_rows": [
        ("Phone line that always reaches the building", "Service (any type)"),
        ("Internal directory", "ClusterIP"),
        ("Phone booth on every block", "NodePort"),
        ("Dispatch operator with a public number", "LoadBalancer"),
        ("Phone-book alias to an outside line", "ExternalName"),
        ("City's main entrance turnstile (HTTP routing)", "Ingress / Gateway API"),
        ("Traffic rules: who may call whom", "NetworkPolicy"),
        ("DNS lookup to find the line", "kube-dns / CoreDNS resolving service-name.namespace.svc"),
    ],
    "eli5": "Buildings move all the time. The phone numbers stay the same because the Switchboard knows which building has which phone today. Inside calls use a directory; outside calls use the main number.",
    "eli10": "Pods get fresh IPs on every restart. Services give a group of Pods a stable name + virtual IP. Four types: ClusterIP (internal), NodePort (every node port), LoadBalancer (cloud LB), ExternalName (DNS alias). Ingress / Gateway API adds L7 routing (host + path). NetworkPolicy is the firewall — default-allow until a Pod is selected by any policy, then default-deny except for explicit allows.",
    "recap_lead": "Pods are ephemeral; Services give them stable names. Ingress lets the world reach them. NetworkPolicy controls who can talk to whom.",
    "recap_next": "That's the Module 1-5 close — the foundations are set. Next up: Module 9 onward — storage, config, scheduling, and beyond.",
    "fact_check_anchors": [
        "https://kubernetes.io/docs/concepts/services-networking/service/",
        "https://kubernetes.io/docs/concepts/services-networking/ingress/",
        "https://kubernetes.io/docs/concepts/services-networking/network-policies/",
        "https://gateway-api.sigs.k8s.io/",
    ],
}

L18_DATA = {
    "central_metaphor": "Customs Warehouse — locker rental front desk. The PVC is the rental form (your request). The PV is the assigned locker (the actual disk). The StorageClass is the warehouse policy book (how new lockers are made + what happens at checkout). The clerk reading the form is the provisioner / CSI driver.",
    "outcomes": [
        "Explain why Pod storage is ephemeral by default.",
        "Write a PVC referencing a StorageClass; bind it to a PV.",
        "Pick the right access mode for a workload (RWO / ROX / RWX / RWOP).",
        "Pick the right reclaim policy (Delete vs Retain).",
        "Use WaitForFirstConsumer in any multi-zone cluster.",
    ],
    "stamp": "Pod storage is ephemeral. To survive a Pod restart, declare a PVC (the request). A StorageClass (the recipe) tells K8s how to provision a PV (the actual disk). The PV binds to the PVC and the Pod mounts it.",
    "flashcards": [
        ("PV vs PVC?", "PVC = Persistent Volume Claim, the request (namespace-scoped, written by app teams). PV = Persistent Volume, the actual disk (cluster-scoped, created by provisioner or admin). They bind 1:1."),
        ("What is StorageClass for?", "A 'recipe' telling K8s how to provision PVs on demand. Names the CSI provisioner, sets parameters (disk type, IOPS, encryption), reclaim policy, volume binding mode."),
        ("Four access modes?", "RWO ReadWriteOnce — one node, read-write. ROX ReadOnlyMany — many nodes, read-only. RWX ReadWriteMany — many nodes, read-write (needs network FS). RWOP ReadWriteOncePod — one Pod, read-write (1.27+)."),
        ("Reclaim policies?", "Delete (default for dynamic) — PV and underlying disk deleted with the PVC. Retain — PV stays in Released state; human reclaims. Recycle — deprecated; don't use."),
        ("Volume binding modes?", "Immediate — provision PV when PVC created (problematic in multi-zone). WaitForFirstConsumer — provision PV when first Pod scheduled (correct for multi-zone — disk lands in the right zone)."),
        ("Static vs dynamic provisioning?", "Static — admin pre-creates PVs by hand; PVCs match against existing PVs. Dynamic — StorageClass + provisioner creates PVs on demand. Dynamic is the modern default."),
        ("When does data actually get cleaned?", "Container filesystem: at every container restart. emptyDir: at Pod removal. PVC-backed volumes: per the PV's reclaim policy when the PVC is deleted (Delete = now; Retain = manual)."),
        ("Why doesn't RWX work on EBS?", "EBS (and most cloud block storage) attaches to one node at a time. RWX requires multiple nodes mounting concurrently — only network filesystems (EFS, Filestore, Azure Files, Ceph, Longhorn) support it."),
    ],
    "quiz": [
        ("A team writes `storageClassName: ''` (empty string) on their PVC. What does this mean?",
         "It explicitly opts out of dynamic provisioning. The PVC will only bind to a *pre-existing* PV that also has empty `storageClassName`. Different from omitting the field, which uses the cluster's default StorageClass. Used when you've manually created a PV and want this PVC to claim it specifically."),
        ("You delete a PVC with `kubectl delete pvc my-data`. The underlying disk should be preserved. What's the right setup?",
         "Use a StorageClass with `reclaimPolicy: Retain` (or set the PV's reclaim policy to Retain after the fact with `kubectl patch pv ... --type=json -p='[{\"op\":\"replace\",\"path\":\"/spec/persistentVolumeReclaimPolicy\",\"value\":\"Retain\"}]'`). On PVC deletion the PV moves to `Released` state with the data intact. A human verifies before deleting it manually."),
        ("Your team uses a StorageClass with `volumeBindingMode: Immediate` (the historical default). The cluster spans three availability zones. A new PVC is created. What happens at the next Pod restart?",
         "The PV was provisioned the moment the PVC was created — before any Pod existed to consume it. The provisioner picked a zone at random: `us-east-1b`. Two days later the workload's Pod gets scheduled — to `us-east-1c`. The Pod tries to mount the PVC. Cloud block storage can't attach across zones. The Pod is stuck Pending forever, with a cryptic `FailedAttachVolume` event. **Fix:** set `volumeBindingMode: WaitForFirstConsumer` on every StorageClass in any multi-zone cluster. The scheduler picks the node first; the disk gets provisioned in the right zone."),
    ],
    "stops": "Real lockers don't move. K8s persistent volumes can be detached from one node and re-attached to another (within the same zone for cloud block storage), so a Pod can reschedule and keep its disk.",
    "scenarios": [
        ("A SaaS startup running PostgreSQL", "Single primary, two read replicas, all on EKS. Storage class: gp3 with 4000 IOPS, WaitForFirstConsumer, Retain reclaim. Each Pod gets a 200 GiB PVC via StatefulSet's volumeClaimTemplates. Pod restarts re-attach the same disk. When they decommission a replica, the PV stays in Released state — a human verifies and deletes manually. Zero data loss in 18 months."),
        ("A bank running shared log aggregation", "Five Fluentd Pods need to write into the same staging directory before forwarding to a SIEM. ReadWriteMany on Azure Files (SMB-based). Slower than local SSD but everyone can write concurrently. The team accepted the latency hit for the pipeline simplicity."),
        ("A media company training ML models", "Training Pods need read access to a 4 TB dataset of pre-processed images. Their CSI driver supports ReadOnlyMany from object storage (S3-via-CSI). Each new training run mounts the same PVC; no copying, no duplication."),
        ("A retail platform migrating from local disk", "Legacy app wrote to /var/lib/myapp/sessions on the host. New PVC mounted at the same path via subPath. Code unchanged. The PVC handles the persistence; the app code stayed identical. Migration was a YAML change, not a refactor."),
    ],
    "misconceptions": [
        ("A PVC *is* the disk.", "The PVC is the *request*. The PV is the disk. They're separate objects that bind 1:1. You can delete a PVC without deleting the PV (with Retain reclaim policy)."),
        ("WaitForFirstConsumer is just an optimisation.", "It's a correctness fix in any multi-zone cluster. With Immediate binding the disk gets provisioned in some random zone *before* the Pod is scheduled — and cloud block storage can't cross zones. The Pod ends up Pending forever."),
        ("Deleting a PVC deletes the data instantly.", "Depends on the PV's reclaim policy. Delete (default for dynamic) → yes, the disk is gone. Retain → the PV moves to Released; data still there until a human decides. For production data, prefer Retain."),
    ],
    "before": "Manual disk wrangling: SSH to a VM, attach an EBS volume, mkfs, mount, edit /etc/fstab, document in a wiki nobody reads. Multiply by 50 services × 3 environments — permanent backlog.",
    "after": "PVC manifest declaring 10Gi of fast-ssd. kubectl apply. K8s provisions an EBS volume, formats it, attaches to the node, mounts into the Pod. Pod moves → disk follows. No scripts; the cluster handles it.",
    "before_after_caption": "Declarative storage is just declarative scheduling, applied to disks. The cluster does the wrangling.",
    "analogy_intro": "You arrive at K-Town's Customs Warehouse with goods you need to store. You don't pick a locker yourself — you fill out a rental form describing what you need. The clerk reads your form, checks the locker manifest, and either *assigns* you an unused locker that fits or *orders a new one* built to spec. The clerk hands you a key. The warehouse policy book defines what kinds of lockers exist, how to build new ones, and what happens when a renter leaves.",
    "translation_rows": [
        ("The rental form you fill out", "PersistentVolumeClaim (PVC)"),
        ("The locker assigned to you", "PersistentVolume (PV)"),
        ("The warehouse policy book", "StorageClass"),
        ("The clerk reading your form", "The provisioner (CSI driver)"),
        ("\"Just me / many of us / read-only\"", "Access modes (RWO / RWX / ROX / RWOP)"),
        ("Whether the locker is wiped or saved at checkout", "Reclaim policy (Delete vs Retain)"),
        ("\"Assign now\" vs \"wait until you arrive\"", "Volume binding mode (Immediate vs WaitForFirstConsumer)"),
    ],
    "eli5": "Your Pod is like a kid at school. The desk gets cleared at the end of every day. To keep their drawings, they need a *cubby*. They ask the teacher for a cubby. Drawings live in the cubby. The kid can move desks; the cubby stays theirs.",
    "eli10": "Pod container filesystem is wiped on restart. To keep data, declare a PVC referencing a StorageClass. The cluster's provisioner creates a PV matching the PVC, binds them, mounts the volume into the Pod. Pod restarts re-attach the same PV. Pick access mode by how many Pods need it; pick reclaim policy by whether deleting the PVC should delete the data; pick WaitForFirstConsumer in any multi-zone cluster.",
    "recap_lead": "Three roles: PVC requests storage, StorageClass tells K8s how to make it, PV is the actual disk. Pod restarts → same PV re-attached. Data survives.",
    "recap_next": "Next — Lesson 19: Storage Part 2. CSI drivers under the hood, snapshots and cloning, the new VolumeAttributesClass for live performance changes (GA in 1.34), stateful patterns, multi-attach errors.",
    "fact_check_anchors": [
        "https://kubernetes.io/docs/concepts/storage/persistent-volumes/",
        "https://kubernetes.io/docs/concepts/storage/storage-classes/",
        "https://kubernetes.io/docs/concepts/storage/volume-attributes-classes/",
    ],
}

LEGACY_DATA = {"16": L16_DATA, "17": L17_DATA, "18": L18_DATA}


# ---------------------------------------------------------------------------
# YAML/Markdown emitters
# ---------------------------------------------------------------------------

def emit_brief(num: str, slug: str, module: str, title: str, spec: LessonSpec | None) -> str:
    """Produce brief.yaml content."""
    if spec is not None:
        # Pull from LessonSpec
        outcomes = []
        for sec in spec.sections[:3]:
            line = html_to_md(sec.h2)
            outcomes.append(f"Learner can explain {line[0].lower()}{line[1:]}.")
        # Stamp text
        stamp = html_to_md(spec.stamp_html)
        # Misconception summaries → first sentence of truth
        # Scenarios → first sentence of body
        scenario_lines = [html_to_md(s.body).split('.')[0] + '.' for s in spec.scenarios[:4]]
        flashcard_count = len(spec.flashcards)
        quiz_count = len(spec.quizzes)
        anchors = []  # spec doesn't carry them; keep empty + a generic doc anchor
        anchors.append("https://kubernetes.io/docs/")
        analogy_short = html_to_md(spec.analogy_intro_html)[:240]
        sections_titles = [html_to_md(s.h2) for s in spec.sections]
    else:
        d = LEGACY_DATA[num]
        outcomes = d["outcomes"]
        stamp = d["stamp"]
        scenario_lines = [s[1].split('.')[0] + '.' for s in d["scenarios"][:4]]
        flashcard_count = len(d["flashcards"])
        quiz_count = len(d["quiz"])
        anchors = d["fact_check_anchors"]
        analogy_short = d["central_metaphor"][:240]
        sections_titles = []

    metaphor = LEGACY_DATA.get(num, {}).get("central_metaphor")
    if metaphor is None and spec is not None:
        # Use district label + first analogy paragraph
        metaphor = f"{spec.district_label} — {analogy_short}"

    prereqs_line = f"Lessons 1-{int(num) - 1 if num.isdigit() else 17} of K-COM (cumulative)."
    parts = []
    parts.append(f"# Intake brief — Lesson {num}, K-COM")
    parts.append(f"# Topic: {title}")
    parts.append(f"# {module}")
    parts.append("")
    parts.append("lesson:")
    parts.append(f"  title: '{yaml_escape(title)}'")
    parts.append(f"  slug: '{slug}'")
    parts.append("  domain: 'kubernetes'")
    parts.append("  course_slug: 'common-to-all-distributions'")
    parts.append(f"  position: {num}")
    parts.append("  granularity: 'concept'")
    parts.append("  brief_drafted_on: '2026-05-03'")
    parts.append(f"  central_metaphor: '{yaml_escape(metaphor)}'")
    parts.append(f"  module: '{yaml_escape(module)}'")
    parts.append("")
    parts.append("learner_profile:")
    parts.append("  prerequisites:")
    parts.append(f"    - '{yaml_escape(prereqs_line)}'")
    parts.append("  assumed_zero_knowledge_of: []")
    parts.append("")
    parts.append("learning_outcomes:")
    for o in outcomes:
        parts.append(f"  - '{yaml_escape(o)}'")
    parts.append("")
    parts.append("sections:")
    if sections_titles:
        for t in sections_titles:
            parts.append(f"  - '{yaml_escape(t)}'")
    else:
        parts.append("  - 'See lesson.md for full section list.'")
    parts.append("")
    parts.append("section_5_real_world:")
    parts.append("  count: 4")
    parts.append("  examples:")
    for s in scenario_lines:
        parts.append(f"    - '{yaml_escape(s)}'")
    parts.append("")
    parts.append("section_6_animated_svg:")
    parts.append("  modes_count: 3")
    parts.append(f"  description: 'See preview-kubernetes-lesson-{num}.html Section 6 for the live animation.'")
    parts.append("")
    parts.append("section_7_flashcards_quiz:")
    parts.append(f"  flashcards: {flashcard_count}")
    parts.append(f"  quiz_questions: {quiz_count}")
    parts.append("")
    parts.append("shared_artifacts:")
    parts.append(f"  preview_page: {{ file: '/preview-kubernetes-lesson-{num}.html' }}")
    parts.append("  lesson_md: { file: 'lesson.md' }")
    parts.append(f"  flashcards: {{ file: 'flashcards.yaml', count: {flashcard_count} }}")
    parts.append(f"  quiz: {{ file: 'quiz.yaml', count: {quiz_count} }}")
    parts.append("")
    parts.append("bar:")
    parts.append(f"  - '{yaml_escape(stamp)}'")
    parts.append("")
    parts.append("fact_check_anchors:")
    for a in anchors:
        parts.append(f"  - '{yaml_escape(a)}'")
    return "\n".join(parts) + "\n"


def emit_lesson_md(num: str, title: str, module: str, spec: LessonSpec | None) -> str:
    """Produce lesson.md content from spec or legacy data."""
    out = []
    out.append(f"# Lesson {num} — {title}")
    out.append("")
    out.append(f"> Course: Kubernetes — Common to all distributions")
    out.append(f"> {module}")
    out.append(f"> Companion preview: `/preview-kubernetes-lesson-{num}.html`.")
    out.append("")
    out.append("---")
    out.append("")

    if spec is not None:
        # Stamp
        out.append(f"**🎯 If you remember nothing else:** {html_to_md(spec.stamp_html)}")
        out.append("")
        # Sections
        for i, sec in enumerate(spec.sections, start=1):
            out.append(f"## {i}. {html_to_md(sec.h2)}")
            out.append("")
            out.append(html_to_md(sec.body_html))
            out.append("")
        # Before / After
        out.append("## Before / After")
        out.append("")
        out.append(f"**Before.** {html_to_md(spec.before_after_before)}")
        out.append("")
        out.append(f"**After.** {html_to_md(spec.before_after_after)}")
        out.append("")
        out.append(html_to_md(spec.before_after_caption))
        out.append("")
        # Analogy
        out.append("## Analogy — the K-Town district")
        out.append("")
        out.append(html_to_md(spec.analogy_intro_html))
        out.append("")
        out.append("**Translation legend.**")
        out.append("")
        out.append("| In the story… | …in Kubernetes |")
        out.append("|---|---|")
        for story, k8s in spec.translation_rows:
            out.append(f"| {html_to_md(story)} | {html_to_md(k8s)} |")
        out.append("")
        out.append(f"⚠️ *Analogy stops here:* {html_to_md(spec.analogy_stops)}")
        out.append("")
        # ELI
        out.append("## ELI5 / ELI10")
        out.append("")
        out.append(f"**ELI5.** {html_to_md(spec.eli5)}")
        out.append("")
        out.append(f"**ELI10.** {html_to_md(spec.eli10)}")
        out.append("")
        # Real-world
        out.append("## Real-world scenarios")
        out.append("")
        for s in spec.scenarios:
            out.append(f"- **{s.name}.** {html_to_md(s.body)}")
        out.append("")
        # Misconceptions
        out.append("## Common misconceptions")
        out.append("")
        for m in spec.misconceptions:
            out.append(f"- **Myth:** {html_to_md(m.myth)}")
            out.append(f"  **Truth:** {html_to_md(m.truth)}")
        out.append("")
        # Recap
        out.append("## Recap")
        out.append("")
        out.append(html_to_md(spec.recap_lead))
        out.append("")
        out.append(html_to_md(spec.recap_next))
        out.append("")
        # Flashcards + quiz pointer
        out.append("## Flashcards and quiz")
        out.append("")
        out.append(f"See `flashcards.yaml` ({len(spec.flashcards)} cards) and `quiz.yaml` ({len(spec.quizzes)} questions).")
    else:
        d = LEGACY_DATA[num]
        out.append(f"**🎯 If you remember nothing else:** {d['stamp']}")
        out.append("")
        out.append("## Before / After")
        out.append("")
        out.append(f"**Before.** {d['before']}")
        out.append("")
        out.append(f"**After.** {d['after']}")
        out.append("")
        out.append(d['before_after_caption'])
        out.append("")
        out.append("## Analogy — the K-Town district")
        out.append("")
        out.append(d['analogy_intro'])
        out.append("")
        out.append("**Translation legend.**")
        out.append("")
        out.append("| In the story… | …in Kubernetes |")
        out.append("|---|---|")
        for story, k8s in d['translation_rows']:
            out.append(f"| {story} | {k8s} |")
        out.append("")
        out.append(f"⚠️ *Analogy stops here:* {d['stops']}")
        out.append("")
        out.append("## ELI5 / ELI10")
        out.append("")
        out.append(f"**ELI5.** {d['eli5']}")
        out.append("")
        out.append(f"**ELI10.** {d['eli10']}")
        out.append("")
        out.append("## Real-world scenarios")
        out.append("")
        for name, body in d['scenarios']:
            out.append(f"- **{name}.** {body}")
        out.append("")
        out.append("## Common misconceptions")
        out.append("")
        for myth, truth in d['misconceptions']:
            out.append(f"- **Myth:** {myth}")
            out.append(f"  **Truth:** {truth}")
        out.append("")
        out.append("## Recap")
        out.append("")
        out.append(d['recap_lead'])
        out.append("")
        out.append(d['recap_next'])
        out.append("")
        out.append("## Flashcards and quiz")
        out.append("")
        out.append(f"See `flashcards.yaml` ({len(d['flashcards'])} cards) and `quiz.yaml` ({len(d['quiz'])} questions).")

    return "\n".join(out) + "\n"


def emit_flashcards(num: str, spec: LessonSpec | None) -> str:
    if spec is not None:
        cards = [(html_to_md(f.front), html_to_md(f.back)) for f in spec.flashcards]
    else:
        cards = LEGACY_DATA[num]['flashcards']
    out = [f"# Flashcards — Lesson {num}", f"# Total: {len(cards)} cards.", "", "cards:"]
    for i, (front, back) in enumerate(cards, start=1):
        out.append(f"  - id: {i}")
        out.append(f"    front: |")
        out.extend(f"      {line}" for line in front.splitlines())
        out.append(f"    back: |")
        out.extend(f"      {line}" for line in back.splitlines())
        out.append("")
    return "\n".join(out)


def emit_quiz(num: str, spec: LessonSpec | None) -> str:
    if spec is not None:
        quizzes = [(html_to_md(q.prompt), html_to_md(q.answer), q.cyoa) for q in spec.quizzes]
    else:
        quizzes = [(p, a, False) for p, a in LEGACY_DATA[num]['quiz']]
    out = [f"# Quiz — Lesson {num}", f"# Total: {len(quizzes)} questions.", "", "questions:"]
    for i, (prompt, answer, cyoa) in enumerate(quizzes, start=1):
        out.append(f"  - id: {i}")
        if cyoa:
            out.append(f"    type: 'cyoa'")
        out.append(f"    prompt: |")
        out.extend(f"      {line}" for line in prompt.splitlines())
        out.append(f"    answer: |")
        out.extend(f"      {line}" for line in answer.splitlines())
        out.append("")
    return "\n".join(out)


def main() -> None:
    for num, (slug, module, title) in LESSON_META.items():
        spec = load_spec(num)
        folder = os.path.join(SCENARIOS, slug)
        os.makedirs(folder, exist_ok=True)
        files = {
            "brief.yaml": emit_brief(num, slug, module, title, spec),
            "lesson.md": emit_lesson_md(num, title, module, spec),
            "flashcards.yaml": emit_flashcards(num, spec),
            "quiz.yaml": emit_quiz(num, spec),
        }
        for fname, content in files.items():
            path = os.path.join(folder, fname)
            with open(path, "w") as f:
                f.write(content)
        print(f"  L{num}: wrote {folder}")
    print(f"\nDone. {len(LESSON_META)} folders.")


if __name__ == "__main__":
    main()
