# Lesson 14 — The K8s API &amp; YAML · Objects, apiVersion, kind, spec, status, CRDs

> Course: Kubernetes — Common to all distributions
> Lesson 14 of 17 in K-COM. Module 3 · Lesson 2 of 5.
> Companion preview: `/preview-kubernetes-lesson-14.html`.

---

## 1. Concept

Everything in Kubernetes is a typed object: a Pod, a Service, a
Deployment, a ConfigMap, your custom Foo. Every object — whether
built-in or custom — has the **same four-block structure** and lives in
the same etcd-backed object store. Once you've internalized the
structure, every "kubectl apply" feels familiar.

**The four blocks.** Every YAML file has exactly these:

```yaml
apiVersion: apps/v1          # 1. Which form template (group/version)
kind: Deployment             # 2. Which form
metadata:                    # 3. Identity (name, namespace, labels, annotations)
  name: my-app
  namespace: default
  labels: { app: my-app, env: prod }
spec:                        # 4. What you want (desired state)
  replicas: 3
  ...
# status:                    # 5. What's actually true (filled in by the system, not you)
```

`apiVersion` + `kind` = "which API endpoint, which schema." `metadata`
identifies the object. `spec` is what you declared. `status` is what
controllers later wrote back (don't put it in your YAML; you don't own
it).

**API groups.** The API is partitioned into groups so it can evolve.
A handful you'll see constantly:

- **core** (`v1`) — Pods, Services, ConfigMaps, Secrets, Namespaces,
  Nodes. Core resources have `apiVersion: v1` (no group prefix).
- **apps** (`apps/v1`) — Deployments, ReplicaSets, StatefulSets,
  DaemonSets.
- **batch** (`batch/v1`) — Jobs, CronJobs.
- **networking.k8s.io** (`networking.k8s.io/v1`) — Ingress,
  NetworkPolicy.
- **rbac.authorization.k8s.io** — Roles, RoleBindings, ClusterRoles.
- **autoscaling**, **policy**, **storage.k8s.io**, **coordination.k8s.io**…

Each group has its own version lifecycle (`v1alpha1` → `v1beta1` →
`v1` → eventual deprecation). New features start in alpha. **CRDs**
(below) get their own custom group.

**`kubectl explain` — the manual built into your cluster.**
`kubectl explain pod` prints the documented schema of a Pod object.
`kubectl explain pod.spec.containers` drills down. `kubectl explain
pod.spec.containers --recursive` shows everything. This is the source
of truth — it reflects exactly what your cluster's API server accepts
right now (including CRDs), not the docs site for some other version.

**Server-side validation.** When you submit a YAML, the API server
validates it against the OpenAPI schema. Typos like `replicaCount: 3`
(should be `replicas`) are rejected with a clear error before anything
is persisted. This is why you should always use `kubectl apply
--server-side` in CI — you get the cluster's actual schema validation,
not a client-side guess.

**Declarative vs imperative.** Kubernetes is fundamentally
declarative: you write a YAML describing what should exist; controllers
make it so. `kubectl apply -f file.yaml` is declarative. `kubectl
create deployment ...` and `kubectl run ...` are imperative — they're
fine for ad-hoc poking and learning, but never use them in production.
Imperative commands have no diff, no audit trail, no GitOps story
(Lesson 06).

**Labels vs annotations.** Both go in `metadata`. **Labels** are
indexed and used for selection (Services find Pods by labels;
Deployments manage Pods by labels). Keep them short and meaningful:
`app=my-app`, `tier=frontend`, `env=prod`. **Annotations** are free-form
metadata not used for selection: build SHA, deploy timestamp, on-call
team contact, ingress controller hints. Use annotations for everything
labels would be too rigid for.

**Custom Resource Definitions (CRDs).** The single most powerful K8s
feature. You can define your own object types. Write a YAML that
*describes* a new type (`Foo`, `Certificate`, `Cluster`), apply it,
and the API server immediately starts serving `kubectl get foo`,
`kubectl apply foo.yaml`, with the same RBAC, audit, validation, and
storage as built-in types. Combine with a controller (the "operator"
pattern) and you've extended K8s with first-class new abstractions.
cert-manager, Argo CD, Crossplane, Istio, and most production
add-ons ship as CRDs + controllers.

---

## 2. Before / After

**Before — every tool has its own config format.** Nginx has its own
config syntax. Apache has its own. systemd uses unit files. Terraform
uses HCL. Ansible uses YAML but with its own structure. Each tool's
configs are validated by that tool only, stored in different places,
managed by different RBAC, audited (or not) by different mechanisms.
"What runs in production?" requires inspecting five different systems.

**After — every config is the same form.** In Kubernetes, your nginx
config (Deployment + ConfigMap), your TLS certs (cert-manager
Certificate CRD), your network policies (NetworkPolicy), your secrets,
your batch jobs, your custom monitoring rules — *all* of them are the
same 4-block YAML structure, validated by one API server, stored in
one etcd, audited by one log, secured by one RBAC system. "What runs
in production?" = `kubectl get all,certificates,networkpolicies -A`.

What changed: a uniform object model. Every operational concern is now
"just another typed object you read/write through one API."

---

## 3. Analogy — the permit office

Kubernetes is a **permit office** for your software. Every change
requires a permit, and every permit is the same standard 4-section
form.

You walk in with a **filled form** (your YAML). The form has four
sections: at the top, the **type-of-permit declaration** (`apiVersion:
apps/v1`, `kind: Deployment` — which form template, which version).
Below that, the **identity section** (`metadata: name, namespace,
labels, annotations`). Then the **what-you-want section** (`spec` —
the only part you really write). The fourth section, **status**, is
left blank — that gets stamped in later by the **inspector** (a
controller) when they verify the work.

The **clerk at the counter** (the API server) looks up the form
template, checks every field is filled correctly (server-side
validation against the OpenAPI schema), and either accepts the form or
points to the typo. If accepted, the form goes into the **filing
cabinet** (etcd) and a watch event fires.

Different permit types are filed at **different counters** (API
groups). `core/v1` for Pods and Services, `apps/v1` for Deployments,
`batch/v1` for Jobs, etc. The **handbook on the desk** that lists every
field of every form is `kubectl explain`.

If the system doesn't have a form for what you need, you can **register
your own form template** (a CRD). Once registered, the office accepts
your custom permits with the same validation and storage as the
built-in ones. Pair it with your own inspector (controller / operator)
and you've extended the office without forking the codebase.

**The mapping:**

- Permit office = the Kubernetes API server
- Standard 4-section form = the structure of every K8s object
- Type declaration at top = `apiVersion` + `kind`
- Identity section = `metadata`
- What-you-want section = `spec`
- Inspector's stamp = `status`
- Different counters = API groups
- Clerk validating the form = server-side OpenAPI validation
- Filing cabinet = etcd
- Handbook on the desk = `kubectl explain`
- Custom permit template = CRD
- Custom inspector = your operator (Lesson 06's controller pattern)
- Bringing in a filled form = `kubectl apply`
- Asking the clerk to fill one out for you = `kubectl create` (imperative)
- Labels = the colored sticker on the form (used to file & find it)
- Annotations = sticky notes on the form (humans read, system ignores)

---

## 4. ELI5 / ELI10

**ELI5.** A permit office. Every form has the same four parts: what
kind of form, who's asking, what you want, and a blank space for the
inspector to stamp. The clerk checks your form for typos. If it's
good, it goes in the filing cabinet. If you need a kind of form they
don't have, you can invent one and they'll start accepting it.

**ELI10.** Every Kubernetes object is YAML with four blocks:
`apiVersion` (which API group/version), `kind` (which type),
`metadata` (name, namespace, labels, annotations), and `spec` (what
you want). A fifth block, `status`, is filled in by controllers — you
don't write it. Resources are partitioned into API groups (`core`,
`apps`, `batch`, `networking.k8s.io`, `rbac.authorization.k8s.io`...)
each with its own versions (`v1alpha1` / `v1beta1` / `v1`). The API
server validates every submission against an OpenAPI schema —
`kubectl explain pod.spec.containers` shows you that schema. Use
`kubectl apply -f` (declarative — diff'd against the cluster's current
state, GitOps-friendly) instead of `kubectl create` / `kubectl run`
(imperative — no audit trail). When you need a new object type that
K8s doesn't ship, write a **CRD** (Custom Resource Definition). The
API server immediately starts serving your new type with the same
RBAC, audit, and validation as built-ins. cert-manager's `Certificate`,
Argo CD's `Application`, every operator out there — all CRDs.

---

## 5. Real-world scenarios

**`kubectl explain` saved hours of guessing the field name.**
A team was integrating with cert-manager. They guessed
`spec.commonNames` (plural). Got "field not declared in schema."
Tried `spec.dnsName`. Same error. Finally ran `kubectl explain
certificate.spec --recursive`. Saw the field is `spec.dnsNames`
(plural, singular form `dnsName` is wrong). Five-second fix once they
knew. Lesson: the cluster's own schema is authoritative; don't guess
or copy-paste blog posts that may be from a different version.

**Imperative `kubectl create` disasters in production.**
An engineer ran `kubectl scale deployment api --replicas=10` to "fix"
a slow service. It worked. Three days later a CI deploy ran from the
git-tracked YAML which had `replicas: 3`. Service got scaled DOWN to
3 mid-traffic-spike. 5xx surge. Lesson: never use imperative commands
on production state — they don't show up in your git history. Use
`kubectl apply -f` (and ideally Argo CD / Flux) so the YAML in git is
always the truth.

**cert-manager CRDs let teams declare TLS as K8s objects.**
Before cert-manager, getting a Let's Encrypt cert involved running
certbot, copying PEM files into a Secret, scheduling renewals. With
cert-manager (which ships a `Certificate` CRD + controller), you
write 10 lines of YAML: "I want a cert for `app.example.com`, store
it in Secret `app-tls`." The CRD's controller talks to Let's Encrypt,
proves DNS, fetches the cert, writes the Secret, and renews 30 days
before expiry. Same `kubectl apply` workflow, same RBAC, same audit.

**OpenAPI server-side validation caught a typo before it shipped.**
A PR added `replicaCount: 5` to a Deployment YAML (the field is
`replicas`). Local `kubectl apply --dry-run=client` did NOT catch it
(client-side validation is shallow). CI used `kubectl apply
--server-side --dry-run=server`. The cluster's schema rejected it
with `unknown field "spec.replicaCount"`. Caught at PR review, never
hit prod. Lesson: always `--server-side --dry-run=server` in CI.

---

## 6. Animated illustration

Three modes:

1. **YAML object lifecycle** (5 steps). YAML submitted → API server
   schema-validates → admission webhooks run → object persisted to
   etcd → controllers reconcile and write back to `status`.
2. **`kubectl explain` walkthrough** (4 steps). Type `kubectl
   explain pod` (top-level fields). Drill: `kubectl explain pod.spec`
   (spec fields). Drill: `kubectl explain pod.spec.containers`. Add
   `--recursive` for the full tree. The whole schema is queryable.
3. **CRD registration and use** (4 steps). Apply CRD YAML
   (`kind: CustomResourceDefinition`) → API server learns new type and
   starts serving `/apis/example.com/v1/foos` → user runs `kubectl
   apply foo.yaml` → operator (controller) reconciles, writes status.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
