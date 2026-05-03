# K-ECS C1 — C1 · ECS Architecture — Cluster, Service, Task, Task Definition, Launch Types

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C1 · ECS Architecture
> Companion preview: `/preview-kubernetes-ecs-lesson-01.html`.

---

**🎯 If you remember nothing else:** **ECS = AWS-native orchestrator (Cluster / Service / Task / Task Definition); EKS = managed K8s; Fargate = serverless capacity (a launch type, not a product); App Runner = opinionated PaaS for single-service HTTPS apps; Lambda = functions, 15-min cap. Pick by operational appetite + workload shape, not popularity.**

## 1. ECS vs EKS vs Fargate vs App Runner vs Lambda

**ECS** (Elastic Container Service): AWS's own orchestrator. You declare a Cluster, then Tasks (groups of containers) and Services (long-running Tasks with ALB/NLB integration + auto scaling + rolling deploys). *No K8s APIs* — no `kubectl`, no Pods, no YAML manifests. Tight integration with IAM, CloudWatch, ALB, ECR, Secrets Manager. *Pick when* you're AWS-only and want the least YAML possible.
    **EKS** (Elastic Kubernetes Service): managed K8s. You get a real K8s API server, real Pods, real Deployments, real CRDs. Portable to GKE / AKS / on-prem. Huge ecosystem (Helm, operators, service mesh). *Pick when* you need K8s portability or your team already knows K8s. Covered in K-EKS.
    **Fargate**: serverless capacity for ECS *or* EKS. Not a product on its own — it's a *launch type*. AWS provisions and bills you per Task (or per Pod, on EKS). No EC2 to patch. *Pick when* you want zero node management; tolerate the per-Task pricing premium vs raw EC2.
    **App Runner**: opinionated PaaS for a single HTTPS service from a Git repo or container image. AWS does build, deploy, scale, TLS, custom domain. *120-second request timeout. No sidecars. No background workers. No multi-service.* Pick when you want a single web service with zero ops surface. Don't pick for batch jobs, long requests, or multi-container apps.
    **Lambda**: function-as-a-service. Up to *15-minute* execution per invocation. Container-image-based or zip-based. Event-driven (S3 / SQS / API Gateway / EventBridge). *Pick when* the workload is event-driven + short-running + bursty. Not for long-running services (use ECS or EKS).

## 2. Cluster, Service, Task, Task Definition

**Cluster**: a logical grouping of compute capacity. Empty until you give it Tasks. Can have *EC2 capacity*, *Fargate capacity*, *external instances* (ECS Anywhere), or any mix.
    **Task Definition**: a JSON spec describing what one Task should look like — list of containers, CPU + memory, network mode, volumes, IAM roles, log config, environment variables + secrets. *Versioned* — every change creates a new revision (e.g., `my-app:42`). The cargo manifest in the analogy.
    **Task**: one running instance of a Task Definition. A group of one or more containers scheduled and stopped *together* (similar to a K8s Pod, but ECS-specific). Has a state (PROVISIONING → PENDING → RUNNING → STOPPED) and stop reason on exit. Can be one-off (run once and stop) or part of a Service.
    **Service**: an ECS object that keeps N Tasks running long-term. Manages rolling deployments, integrates with ALB/NLB target groups, supports Service Auto Scaling, and emits service discovery records via Cloud Map or Service Connect. *Closest analog to a K8s Deployment + Service combined*, but it's its own object and cannot be confused with a K8s Service object.

## 3. EC2, Fargate, External (ECS Anywhere), ECS Managed Instances

**EC2 launch type**: you create EC2 Auto Scaling groups; ECS agents (running on each EC2) report capacity; ECS schedules Tasks onto your EC2s. You own patching + AMI updates + scaling. *Cheapest for steady-state workloads* with predictable utilisation; supports Spot, Graviton, GPU, large memory ratios.
    **Fargate launch type**: AWS owns the underlying capacity. You request a Task with CPU + memory; Fargate provisions a microVM, runs your containers, bills you by Task-second. *No EC2*. Pricier per vCPU-hour than raw EC2, but the price-of-not-managing-nodes wins for many workloads.
    **External instances (ECS Anywhere)**: register your-own-hardware (on-prem servers, edge devices, even VMs in another cloud) into an ECS cluster via the SSM agent + ECS agent. ECS schedules Tasks onto external capacity. *Bridge use cases*: regulated workloads on-prem, edge processing, gradual cloud migration.
    **ECS Managed Instances** [ deep dive — skip if new ]: AWS-managed EC2 with ECS-optimised AMI lifecycle. AWS patches and rotates the underlying instances on your behalf, but unlike Fargate you still get EC2-style features (full Bottlerocket / AL2023, custom AMIs, Spot, GPU pools). *Middle ground* between raw EC2 and Fargate.

## 4. ECS agent, control plane, scheduler, deployment controller, placement, lifecycle

**ECS agent**: a small Go binary (open-source) running on every container host (EC2, external instance, or Fargate microVM). Talks to the ECS control plane over outbound HTTPS, reports capacity, pulls Task assignments, manages container lifecycle (image pull, start, stop), and ships logs.
    **ECS control plane**: AWS-managed regional service. Holds Cluster + Service + Task Definition + Task state. Receives API calls (RunTask, CreateService, UpdateService, …) and emits Task assignments to ECS agents.
    **Service scheduler**: keeps the actual Task count matching the desired count for each Service. Replaces failed Tasks. Drives rolling deployments (start new revision, drain old, watch ALB target health).
    **Deployment controller**: orchestrates how a Service moves from one Task Definition revision to the next. Three options: *ECS* (built-in rolling — default), *CODE_DEPLOY* (blue/green via CodeDeploy), *EXTERNAL* (you drive deploys via the ECS API directly).
    **Task placement**: when a Task is launched, the placement engine picks compute to run it on, using *placement strategies* (binpack / spread / random) and *placement constraints* (instance type, AZ, attribute filters). Fargate ignores most of this — Fargate places one Task per microVM.
    **Task lifecycle**: PROVISIONING (capacity being prepared) → PENDING (waiting for ENI / volumes / image pull) → RUNNING (containers up, healthChecks reporting) → STOPPED (stopped reason: USER_INITIATED / OutOfMemoryError / Essential container exited / etc.). Service discovery + load balancing wire up only when state = RUNNING.

## Before / After

**Before.** Pre-ECS, AWS-shop teams running containers had to roll their own. *EC2 Auto Scaling group + custom AMI with Docker baked in + a homemade scheduler in Lambda + an ALB target group registered by hand*. Deploying a new version meant SSHing to each instance and running `docker pull`. Failures were silent. Logs went to disk and rotated. Multi-AZ took weeks of infra work. *Each team built their own orchestrator badly.*

**After.** Modern ECS gives you the orchestrator out of the box: a Cluster, a Service, a Task Definition, an ALB-integrated rolling deploy, CloudWatch logs by default, IAM-per-Task, multi-AZ from `--availability-zones`. Add Fargate and the EC2 fleet disappears too. Add Service Connect and east-west service discovery + traffic management land without an extra mesh. *The orchestrator is the platform; you ship Task Definitions.*

*If you're AWS-only and don't need K8s portability, ECS removes a lot of platform-team work. The trade is: you can't lift-and-shift to GKE.*

## Analogy — the K-Harbor pier

K-Harbor is a working AWS-managed harbor. Cargo ships arrive; piers receive them; tugboats nudge each one into its slip. The **Harbor Office** is the first building you see — every captain (operator) checks in there to get a berth assignment.
    On the wall is a chart of five different ways to ship cargo. **ECS**: a full harbor — piers, tugboats, harbor master, you walk in with a cargo manifest and ask for berth. **EKS**: a different harbor across the bay, run to international K8s standard so you can sail your cargo to GCP's harbor or Azure's harbor without repackaging. **Fargate**: the harbor master arranges *self-assembling pop-up piers* on demand — no permanent dock workers — and bills you per ship-day. **App Runner**: a curbside drop-off — you hand over a single small package and AWS delivers it; no piers, no manifests, no negotiation. **Lambda**: a pneumatic-tube system for tiny envelopes — fast, but anything over 15 minutes gets stuck in the tube.
    You're here for ECS. Inside the harbor: the **Harbor Master** (the ECS control plane) keeps the chart of every pier and ship. Each **pier** (Service) has N ships always docked; if one sinks, the Harbor Master orders a replacement. Each **ship** (Task) carries a group of containers — the Task Definition is the cargo manifest spelling out what containers and how much CPU and memory. The **tugboat skipper** (ECS agent) lives on every dock and actually pushes ships into their slips, reporting back to the Harbor Master.

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Harbor Office | ECS Cluster — entry point, configuration |
| Pier (long-term berth with N ships) | ECS Service — keeps N Tasks running |
| Ship at the pier | ECS Task — one running instance |
| Cargo manifest | Task Definition — JSON spec, versioned by revision |
| Harbor Master | ECS control plane / scheduler / deployment controller |
| Tugboat Skipper | ECS agent (one per host: EC2, external, or Fargate microVM) |
| Permanent dock workers (you hire them) | EC2 launch type |
| Pop-up self-assembling piers (AWS arranges) | Fargate launch type |
| Your-own-warehouse pier across the bay | External launch type — ECS Anywhere |
| AWS-managed dock workers + swap-out cycle | ECS Managed Instances launch type |
| International-standard harbor across the bay | EKS — managed K8s |
| Curbside one-package drop-off | App Runner — single-service PaaS |
| Pneumatic envelope tubes (15-min cap) | Lambda — function-as-a-service |

⚠️ *Analogy stops here:* A real harbor has fixed piers and ships. ECS Tasks are software-defined and disappear in seconds when stopped — there's no "empty pier" to inspect later. The Harbor Office stays; everything else is ephemeral state in DynamoDB.

## ELI5 / ELI10

**ELI5.** AWS has five different ways to run containers. ECS is AWS's own way — like a harbor where you bring a list of what's in your ship and AWS finds you a pier. EKS is the same idea but built to international Kubernetes standards. Fargate is when AWS arranges pop-up piers so you don't hire dock workers. App Runner is a curbside drop-off for one package. Lambda is a pneumatic tube for tiny envelopes. Pick the one that matches what you're shipping.

**ELI10.** ECS has four shapes — **Cluster** (the harbor), **Service** (a pier that keeps N ships docked long-term), **Task** (one running ship of containers), **Task Definition** (versioned JSON manifest of what a Task should look like). Four launch types: *EC2* (you manage hosts), *Fargate* (AWS manages capacity, per-Task billing), *External / ECS Anywhere* (your hardware joins the cluster), *ECS Managed Instances* (AWS-managed EC2). The control plane is regional, the ECS agent runs on every host, the service scheduler keeps Task count = desired, and the deployment controller handles rolling or blue/green moves to new Task Definition revisions.

## Real-world scenarios

- **SaaS — first containerised service picks ECS on Fargate.** A 30-engineer SaaS shipping their first containerised API. They pick **ECS on Fargate**. *Zero EC2 to manage*: they declare a Service with desired-count = 3 and a Task Definition with one container. ALB integration via target-type IP, blue/green via CodeDeploy, CloudWatch logs by default. *The platform team they didn't hire is the cost saving.*
- **Batch ML inference — ECS on EC2 with Spot + GPU.** A 200-engineer ML team runs nightly inference on 100 GiB of new images. **ECS on EC2** with *g5.xlarge Spot* capacity providers; nightly RunTask launches 50 inference Tasks, each with a single GPU container. Cost is ~70% less than On-Demand. Fargate would have worked too but doesn't support GPU as broadly + costs more per vCPU-hour for steady batch.
- **Regulated workload — ECS Anywhere on-prem hardware.** A bank can't move customer-data processing to the cloud. They run **ECS Anywhere** on their on-prem rack: SSM agent + ECS agent register external instances; the same Task Definitions deploy on-prem and on Fargate-cloud. *Single control plane across regulated and unregulated workloads.*
- **Outage — App Runner picked for a workload that needed ECS.** A startup picked App Runner for their CSV-import API for the demo speed. Production usage included 2-minute uploads. App Runner's 120-second request timeout fired; users got 504s. *4-hour Sunday outage*. Postmortem: migrate to ECS on Fargate (no request timeout cap) with ALB long-running connection support. *App Runner was the wrong shape.*

## Common misconceptions

- **Myth:** "ECS Service is just like a K8s Service."
  **Truth:** No. A K8s Service is a virtual IP + DNS for selecting Pods. An ECS Service is closer to a K8s *Deployment* — a long-running controller that keeps N Tasks running, drives rolling deploys, and (separately) integrates with ALB/NLB or Service Connect for traffic. The two "Service" objects share a name but not a meaning.
- **Myth:** "Fargate is a separate AWS product from ECS."
  **Truth:** Fargate is a **launch type** — a way to provide capacity to ECS or EKS. The same ECS Cluster can have Fargate Tasks and EC2 Tasks side by side via capacity providers. You don't "choose Fargate"; you choose ECS-with-Fargate-capacity or EKS-with-Fargate-capacity.
- **Myth:** "App Runner is just simpler ECS."
  **Truth:** App Runner is a *different shape entirely* — opinionated PaaS for a single HTTPS service. It has a 120-second request timeout, no sidecars, no multi-container, no orchestration knobs. ECS lets you express any orchestrator pattern; App Runner lets you express "a web service". Picking App Runner expecting ECS-like flexibility is the most common AWS-container mistake.

## Recap

ECS is AWS's native container orchestrator. Four shapes (Cluster / Service / Task / Task Definition) × four launch types (EC2 / Fargate / External / Managed Instances) × three deployment controllers. Pick by operational appetite + workload shape — App Runner for single-HTTPS-service, Lambda for short event-driven, ECS for orchestration without K8s, EKS for K8s portability.

**Next — C2: Task Definitions and Containers.** The JSON shape — family + revision, network mode, CPU + memory, ephemeralStorage, runtimePlatform; container definitions (image + ports + env + secrets + dependsOn + healthCheck + logConfiguration + ulimits + linuxParameters); volumes (bind / Docker / EFS / FSx); sidecars + task-level shared volumes; task IAM role vs execution role.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
