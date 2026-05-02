# Lesson 42 — Operators with Kubebuilder · controller-runtime, OLM

> Course: Kubernetes — Common to all distributions
> Module 18 · Extending K8s · Lesson 2 of 3
> Companion preview: `/preview-kubernetes-lesson-42.html`.

---

**🎯 If you remember nothing else:** An **operator** = CRD + controller. Use **Kubebuilder** to scaffold a Go project (or **Operator SDK** for Helm/Ansible-based operators). The controller logic lives in a **Reconciler**: "given the CR's desired state, make the cluster match." controller-runtime handles watches, caching, queueing, leader election. Distribute via Helm chart or OLM (OperatorHub).

## 1. What an operator is

The Operator Pattern: package operational knowledge as code. The CRD is the user-facing API; the controller is the operations runbook expressed in Go. The user writes "`kind: PostgresCluster, replicas: 3, storage: 100Gi`"; the operator does everything to make that real.
    The reconcile loop:
    
      - User creates / updates a CR.

      - The kube-apiserver writes it to etcd.

      - The operator (running as a Pod in the cluster) is watching that CR kind. Receives an event.

      - Reconciler reads the current CR + cluster state, computes the diff, applies changes.

      - Updates the CR's `status` with what happened.

      - Repeats indefinitely ("reconcile loop" — runs every change + periodically).

    
    This is exactly how K8s's built-in controllers work (Deployment controller, ReplicaSet controller, etc.). Operators extend the pattern to your custom kinds.

## 2. The Go-based standard

**controller-runtime** is the Go library underneath Kubebuilder. It abstracts: API client, informer cache, work queue, leader election, manager (lifecycle of all reconcilers). You write a Reconciler struct with a `Reconcile(ctx, req)` method; the framework handles everything else.
    **Kubebuilder** is the project scaffolder + code generator. `kubebuilder init` creates the project; `kubebuilder create api --group example.com --version v1 --kind PostgresCluster` creates the CRD types + controller skeleton. From there you implement the Reconciler.
    A typical Reconciler:
    `func (r *PostgresClusterReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. Fetch the CR
    var cluster examplev1.PostgresCluster
    if err := r.Get(ctx, req.NamespacedName, &cluster); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    // 2. Reconcile owned resources
    if err := r.reconcileStatefulSet(ctx, &cluster); err != nil {
        return ctrl.Result{}, err
    }
    if err := r.reconcileService(ctx, &cluster); err != nil {
        return ctrl.Result{}, err
    }
    // 3. Update status
    cluster.Status.ReadyReplicas = ...
    if err := r.Status().Update(ctx, &cluster); err != nil {
        return ctrl.Result{}, err
    }
    return ctrl.Result{}, nil
}`
    Use `ctrl.SetControllerReference` to set owner refs on owned objects (so they're garbage-collected when the CR is deleted). Use `SetupWithManager` to register watches: "reconcile when the CR changes; reconcile when an owned StatefulSet changes."

## 3. Idempotent, level-triggered, observable

Three properties every Reconciler should have:
    
      - **Idempotent** — running it twice with the same input produces the same result. No "create if not exists"; use `CreateOrUpdate` or `Patch` with server-side apply.

      - **Level-triggered, not edge-triggered** — react to current state, not to a specific event. Multiple events for the same CR get coalesced; the Reconciler reads the latest state and acts.

      - **Observable** — every reconcile updates `status` with what happened. Conditions, ready replicas, last reconcile time. Users debug via `kubectl describe`.

    
    Common patterns:
    
      - **Finalizers** — for resources that need cleanup before deletion (e.g., releasing external cloud resources). Add a finalizer; the operator clears it once cleanup is done; only then is the CR actually deleted.

      - **Conditions** — standardised status fields: `type, status, reason, message, lastTransitionTime`. Common types: Ready, Progressing, Degraded.

      - **Events** — operators emit K8s Events on the CR for visibility. `kubectl describe` shows them; useful for debugging.

      - **Requeue** — return `RequeueAfter: 30 * time.Second` to schedule a re-reconcile (poll external API, etc.).

## 4. How users install your operator

Two main distribution paths:
    
      - **Helm chart** — the K8s-standard package format (Lesson 37). Works for any operator: chart contains CRDs + RBAC + Deployment for the operator. Users `helm install`. Mainstream, widely supported.

      - **OLM (Operator Lifecycle Manager)** — Red Hat's framework for operator distribution + lifecycle. Originally OpenShift-only; now mainstream. Users browse **OperatorHub.io**, install via `Subscription` CRD; OLM handles dependencies, upgrades, channels (stable / fast / dev), conflicts.

    
    OLM's value: automatic upgrade management. Users subscribe to a channel; OLM applies new versions when they're published, runs migration scripts, handles upgrade graphs. Helm requires manual `helm upgrade`.
    OLM's cost: an extra layer to learn + extra CRDs in your cluster. Many teams stick with Helm for simplicity.
    [ deep dive — skip if new ]The 2026 default for new operators: **Helm chart** for general distribution; **OLM** if your target audience is OpenShift-heavy. The CNCF Operator Hub (operatorhub.io) accepts both. Cluster API's control plane providers, cert-manager, Argo CD all distribute via Helm. OpenShift-aligned vendors (Red Hat OpenShift Service Mesh, OpenShift Pipelines) use OLM.

## Before / After

**Before.** Pre-Kubebuilder: write your own informer setup, queue, leader election, RBAC, code generation. Hundreds of lines of boilerplate before you write any business logic. Each operator's code looked different; quality varied wildly. Distribution: ad-hoc YAML or hand-rolled Helm charts.

**After.** Kubebuilder scaffolds the project. controller-runtime handles the framework. Idiomatic Reconciler. Generated CRD YAMLs, RBAC, Dockerfile, Makefile. Distribute via standard Helm chart or OLM. Operators across the ecosystem look similar; ramp-up time for a new operator project: hours, not weeks.

Kubebuilder + controller-runtime is the closest thing K8s has to Rails — opinionated scaffolding that makes the right thing easy. Most production operators built since 2021 use it.

## Analogy — the K-Town district

Workshop is the K-Town district where master craftspeople build custom assistants — robots that watch over a specific kind of permit (CRD) and take action when one is filed. The Workshop has a **standard workbench** (Kubebuilder) where new craftsperson sets up a project in an afternoon: standard tools, standard layout, standard code-gen. The **engine** (controller-runtime) handles all the boring infrastructure — listening for events, queueing work, surviving restarts. The craftsperson focuses on the business logic: what does this assistant *do* when a permit changes? Once built, the assistant is packaged for distribution: either a sealed envelope (Helm chart) or a registered subscription (OLM).

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Standard workbench | Kubebuilder scaffold |
| Workbench engine | controller-runtime |
| Custom assistant for a permit kind | Operator (controller for a CRD) |
| Assistant's reaction logic | Reconciler |
| "React to current state, not what just happened" | Level-triggered reconciliation |
| "Same input, same result" | Idempotent reconciler |
| Cleanup before assistant lets the permit go | Finalizer |
| Status board the assistant updates | `status.conditions` |
| Sealed envelope distribution | Helm chart |
| Subscription registry distribution | OLM / OperatorHub |

⚠️ *Analogy stops here:* The analogy stops here: real operators are Pods running real Go binaries. The "engine" of controller-runtime is leader election, informer caches, work queues — not actual machinery.

## ELI5 / ELI10

**ELI5.** You build a robot that watches your custom forms. When you fill in a form, the robot does the work. Same form = same work; the robot doesn't panic.

**ELI10.** An operator is a controller for a CRD. Use Kubebuilder (CLI scaffolder) + controller-runtime (Go SDK) to write one. Reconciler reads the CR + current state, makes them match, updates status. Patterns: idempotent, level-triggered, finalizers for cleanup, conditions for status. Distribute via Helm chart (most common) or OLM (Red Hat ecosystem).

## Real-world scenarios

- **A SaaS operator managing internal databases.** `InternalDatabase` CRD; user specifies size, type, backup policy. Operator creates StatefulSet + Service + Secret + CronJob (backup) + ServiceMonitor. Built with Kubebuilder; ~3000 lines of Go. Distributed via Helm internally; deployed via Argo CD.
- **A bank using cert-manager (an operator).** `Issuer` + `Certificate` CRDs. cert-manager operator handles ACME flows, key rotation, secret updates. Distributed via Helm. Reliable, widely deployed; the canonical example of operator value.
- **An ML platform using a model-serving operator.** `InferenceService` CRD (KServe / Seldon). Operator creates a Knative Service or Deployment + autoscaling + canary. Routes inference traffic. Built on controller-runtime; mature project, widely used in ML platforms.
- **A team migrating from custom controller to Kubebuilder.** Old controller: ~5000 lines hand-written, used informer-only patterns, no leader election. Migrated to Kubebuilder: ~2200 lines, generated boilerplate, supports HA via leader election, easier to reason about. Migration paid for itself in 6 months of fewer ops issues.

## Common misconceptions

- **Myth:** Operators must be written in Go.
  **Truth:** Most are, because controller-runtime is Go. But Operator SDK supports Helm-based and Ansible-based operators where you write no code. Pure-Helm operators are surprisingly capable: chart + dependency mgmt = an "operator."
- **Myth:** Reconciliation is the same as a webhook.
  **Truth:** Reconciliation is async + level-triggered ("current state vs desired state"). Webhooks are sync + edge-triggered ("this specific request, accept or reject"). Operators usually have both: webhook for admission validation, reconciler for state convergence.
- **Myth:** An operator means OperatorHub + OLM.
  **Truth:** OperatorHub is a marketplace; OLM is the lifecycle manager. Both are optional. Most operators in production are installed via plain Helm; OperatorHub is for discovery + Red Hat ecosystem alignment.

## Recap

Kubebuilder + controller-runtime is the canonical operator stack. Reconciler is the loop; idempotent + level-triggered + observable; finalizers + conditions + events for production polish. Distribute via Helm (most common) or OLM (Red Hat ecosystem).

**Next — Lesson 43: Service Mesh.** The data-plane layer that adds mTLS, observability, traffic shaping to existing services without code changes. Istio ambient, Linkerd, Cilium Service Mesh.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
