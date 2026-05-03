# K-ECS C2 — C2 · Task Definitions and Containers

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C2 · Task Definitions and Containers
> Companion preview: `/preview-kubernetes-ecs-lesson-02.html`.

---

**🎯 If you remember nothing else:** **Task Definitions are immutable; every change is a new revision. Two IAM roles: execution (image pull + secrets + logs) vs task (your app's AWS calls). awsvpc is the recommended network mode for almost every Task. Sidecars share the Task's network namespace + task-level volumes via mountPoints.**

## 1. family, revision, network mode, CPU + memory, ephemeralStorage, runtimePlatform

**family + revision**: each Task Definition has a `family` name (e.g., `my-app`) and a monotonic `revision` number per family (1, 2, 3, …). Reference as `my-app:42`. Revisions are *immutable* — you never edit; you register a new revision. Old revisions remain queryable + usable for rollback (until DEREGISTER + the cleanup grace period).
    **networkMode**: `awsvpc` (recommended; ENI per Task; SG per Task), `bridge` (Docker bridge — EC2-launch only; legacy), `host` (Task uses host network — EC2-launch; collisions if multiple Tasks bind the same port), `none` (no network). Fargate *requires* awsvpc.
    **cpu + memory**: declared at *task level* (the sum across all containers) and optionally per-container. Fargate has a fixed CPU/memory matrix (256/0.5GB up to 16384/120GB); EC2 launch lets you specify any combination that fits the host. Per-container `memoryReservation` is a soft limit; `memory` is the hard limit. Per-container `cpu` is a relative weight (units), not a hard cap unless paired with cgroup limits.
    **ephemeralStorage**: Fargate Tasks get *20 GiB default* ephemeral storage; bumpable up to 200 GiB via `ephemeralStorage.sizeInGiB`. EC2 launch: ephemeral storage is the host disk path (no per-Task quota by default).
    **runtimePlatform**: `operatingSystemFamily` (LINUX, WINDOWS_SERVER_2019_FULL/CORE, WINDOWS_SERVER_2022_FULL/CORE) + `cpuArchitecture` (X86_64, ARM64). ARM64 + Graviton is materially cheaper for compatible workloads — pick early.

## 2. image, ports, env, secrets, dependsOn, healthCheck, logConfiguration, ulimits, linuxParameters

**image**: `account.dkr.ecr.region.amazonaws.com/repo:tag` (or public registry). Pinned digests (`@sha256:…`) preferred over mutable tags for production.
    **portMappings**: array of `{containerPort, hostPort, protocol}`. With awsvpc network mode `hostPort` must equal `containerPort`. ALB target groups bind to `containerPort` via target type IP.
    **environment + secrets**: plain `environment` for non-sensitive values; `secrets` array for values fetched from **Secrets Manager** or **SSM Parameter Store** at Task launch (the execution role policy must allow the fetch). Secrets are injected as env vars in the running container — never logged + KMS-encrypted in transit.
    **dependsOn**: lists other containers in the same Task that must reach a state (`START`, `COMPLETE`, `SUCCESS`, `HEALTHY`) before this one starts. Use for sidecar boot order (e.g., the app waits for the log-router to be HEALTHY).
    **healthCheck**: command + interval + timeout + retries + startPeriod. Reports container health to ECS; ALB target health is separate (HTTP probe by ALB).
    **logConfiguration**: *awslogs* (CloudWatch — default), *awsfirelens* (route via Firelens sidecar to anywhere), *splunk*, *fluentd*, *journald*. Production default = awsfirelens for routing flexibility; awslogs for simplicity.
    **ulimits + linuxParameters** [ deep dive — skip if new ]: ulimits set RLIMIT_NOFILE etc.; linuxParameters configures capabilities, devices, sharedMemorySize, swappiness, init process. Touch only when a workload demands it.

## 3. bind mounts, Docker volumes, EFS, FSx for Windows / ONTAP

**volumes** are declared at the Task Definition top level and *mounted* by containers via `mountPoints` (`{containerPath, sourceVolume, readOnly}`). Five flavours:
    
      - **Bind mount** — host path on the EC2 instance (EC2 launch only). Cheap, fast, host-coupled. Lost when Task moves hosts.

      - **Docker volume** — Docker plugin volume on EC2 host (e.g., REX-Ray, EBS-bound via plugin). EC2 launch only.

      - **EFS** — managed NFSv4 filesystem; **RWX-equivalent** across many Tasks and AZs; supports IAM-based authorization + EFS access points (path + UID/GID + permission isolation per Task). The shared-state answer for ECS.

      - **FSx for Windows File Server** — for Windows Tasks needing SMB share. Configure in Task Definition with `fsxWindowsFileServerVolumeConfiguration`.

      - **FSx for NetApp ONTAP** — NFS-attach for higher-tier file storage (multi-protocol, snapshots, replication). Configure via `fsxWindowsFileServerVolumeConfiguration`-style block (FSx ONTAP is treated similarly).

    
    **Sharing volumes between containers**: declare the volume once at Task level; multiple containers list the same `sourceVolume` in their `mountPoints`. Classic use: app container writes to `/var/log/app`; Firelens sidecar reads from the same mount and ships off-host.

## 4. Sidecars share the Task; execution role vs task role

**Sidecars**: a Task can have multiple containers — one app + one or more sidecars (log router, proxy, observability collector, init helper). Sidecars share the Task's *network namespace* (in awsvpc mode they share the same ENI), Task-level volumes, lifecycle (one container stop → whole Task stops if `essential: true`), and IAM via the task role.
    **essential**: container-level boolean; if `true` (default for the app) and that container exits, the whole Task is stopped (with `stoppedReason` = "Essential container in task exited"). Sidecars that should crash without taking the Task down get `essential: false` — but log routers usually stay `essential: true` so log loss surfaces fast.
    **Execution role**: assumed by the *ECS agent / Fargate* at Task launch to do *infrastructure* things — pull image from ECR, fetch Secrets Manager / SSM values, send container logs to CloudWatch. `AmazonECSTaskExecutionRolePolicy` is the AWS-managed baseline. Add KMS Decrypt for the Secrets KMS key. *The execution role is launch-time scaffolding; the running app does NOT use it.*
    **Task role**: assumed by the *application code* at runtime via the ECS metadata endpoint. Grants the app permission to call AWS APIs (e.g., S3 Put, DynamoDB UpdateItem). **Always least-privilege**: scope to the specific resources + actions the app actually performs. Default to denying everything else.
    *Different roles, different policies, different lifecycles.* Forgetting which is which is the most common ECS-IAM bug.

## Before / After

**Before.** Pre-immutable Task Definitions, teams edited live container configs by SSHing into hosts. Drift was constant. Rolling back meant remembering what the previous shape was. Sidecars that should have run alongside the app were skipped or run as separate ECS Tasks (no shared volumes; no shared lifecycle). Secrets were baked into images or stuffed into env vars committed to source. The execution-role / task-role distinction wasn't in the pattern; teams gave the app every permission the agent had.

**After.** Modern Task Definitions are immutable JSON, versioned per change. Sidecars are first-class — share network and volumes; the app + log-router + envoy / agent run as one Task. Secrets are fetched at launch from Secrets Manager / SSM; KMS-encrypted; not in source. The execution role / task role split keeps launch-time AWS access separate from runtime app access. Rolling back is "UpdateService to revision N-1." *The cargo manifest is the source of truth; everything else is derived.*

*The Task Definition is the only thing you really write for a workload. Get its shape right and most of the rest follows.*

## Analogy — the K-Harbor pier

Down at the harbor, every ship's captain checks in at **Cargo Manifests**. The manifest is a stamped numbered form: family name (*"my-app"*), revision number (*42*), the type of ship (LINUX or WINDOWS, X86_64 or ARM64), how much cargo (CPU + memory), how much spare deck (ephemeralStorage), and what kind of berth wiring (network mode).
    Inside the manifest is the **cargo list** — every container you're putting on the ship. For each container: which warehouse to fetch it from (image), what doors open out (portMappings), what crew badges go inside (environment + secrets), what shipboard rituals must finish first (dependsOn), how the medic reports its health (healthCheck), and where its logs are funnelled (logConfiguration).
    The captain hands the form to the harbor master with two signed letters of authority. The first is for *boarding day only* — it's how the dock crew unlock the ECR warehouse and the secrets vault to load the ship before sailing (**execution role**). The second is what the captain carries on the voyage and uses to call ahead to ports along the way (**task role**). Different letters, different scopes. The dock crew never use the captain's voyage letter; the captain never uses the boarding-day letter.

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Stamped numbered form | Task Definition (immutable revision) |
| Family name + form number | family + revision (e.g., my-app:42) |
| Ship type (Linux/Windows × arch) | runtimePlatform (operatingSystemFamily, cpuArchitecture) |
| How much cargo + spare deck | CPU + memory + ephemeralStorage |
| Berth wiring | networkMode (awsvpc / bridge / host / none) |
| Cargo list (per container) | containerDefinitions array |
| Warehouse address | image (e.g., ECR URI) |
| Crew badges, sealed | environment + secrets (Secrets Manager / SSM) |
| Shipboard rituals before sailing | dependsOn (container startup ordering) |
| Medic's health checks | healthCheck command |
| Log funnel | logConfiguration (awslogs / awsfirelens / etc.) |
| Boarding-day letter (dock crew) | task execution role — image pull + secrets + logs |
| Voyage letter (captain carries) | task role — app's AWS calls at runtime |
| Shared deck space | Task-level volumes + container mountPoints |

⚠️ *Analogy stops here:* A real cargo ship's manifest is paper and changes during the voyage if needed. ECS Task Definition revisions are *completely* immutable — you never edit; you register a new revision. Even a typo means revision N+1.

## ELI5 / ELI10

**ELI5.** Every running ship in the harbor is a copy of a stamped form called a Task Definition. The form has the ship's family name, a number, what cargo to load, what cargo doors open, who can fetch the cargo from the warehouse, and what the cargo can do once it's sailing. You can't edit a stamped form. If something's wrong, you stamp a new one.

**ELI10.** A Task Definition is JSON: `family` + `revision` (immutable per change), `networkMode` (awsvpc recommended), `cpu` + `memory` at task level, `ephemeralStorage`, `runtimePlatform`, an array of `containerDefinitions` (image, ports, env + secrets, dependsOn, healthCheck, logConfiguration, ulimits, linuxParameters), an array of `volumes` (bind / Docker / EFS / FSx), and two IAM roles — **execution role** (launch-time: pull ECR + fetch Secrets + write logs) and **task role** (runtime: the app's AWS calls). Sidecars share the Task's ENI + volumes + lifecycle; `essential` per container controls whether one container exit stops the whole Task.

## Real-world scenarios

- **API + Firelens sidecar — log routing without an agent on every host.** A 60-engineer SaaS runs a Node.js API. Task Definition has two containers: **app** (essential: true, logConfiguration: awsfirelens) + **log-router** (Fluent Bit, essential: true, logConfiguration: awslogs). App stdout flows to the sidecar; sidecar routes to OpenSearch + S3 archive. *No daemonset, no host agents — Task carries its own logging.*
- **ARM64 cost win — Graviton retrofit.** A 25-engineer team flipped `cpuArchitecture` from `X86_64` to `ARM64` + rebuilt their Node + Java images for arm64. Fargate Graviton pricing is ~20% lower per vCPU-hour; image sizes are similar; perf is competitive on most non-AVX workloads. *One config flip + a multi-arch image build saved ~$2k/month.*
- **Stateful migration — adding EFS to a Task.** A team migrating a legacy uploader to ECS. The app expects local `/var/uploads` — but they need state to persist across Task restarts and to be shared with a periodic-cleanup Task. Task Definition gets a `volumes` entry pointing to an EFS access point; both Task Definitions mount it via `mountPoints`. *RWX shared state without redesigning the app.*
- **IAM bug — execution role given S3 access; app couldn't Put.** An on-call engineer added `s3:PutObject` to the execution role (intending to grant runtime access). Task launched fine but app calls returned AccessDenied. The fix: move the policy to the *task role*. *Execution role does launch-time AWS work; task role is what the running container assumes.*

## Common misconceptions

- **Myth:** "You can edit a Task Definition revision after it's registered."
  **Truth:** No. Revisions are **immutable**. Each change registers a new revision (e.g., 42 → 43). Old revisions stay queryable and usable for rollback until DEREGISTER. This is intentional — it's what makes rollbacks deterministic.
- **Myth:** "Execution role and task role are the same; ECS just renamed it."
  **Truth:** Different roles, different lifecycles. **Execution role** is assumed by the agent / Fargate *at launch time* to pull images, fetch secrets, write logs. **Task role** is assumed by the *running container code* via the ECS metadata endpoint, granting the app its AWS API permissions. The split exists so the app never sees the launch-time credentials.
- **Myth:** "Sidecar containers run as separate Tasks."
  **Truth:** No. Sidecars are additional containers *inside the same Task* — they share the Task's ENI (in awsvpc), Task-level volumes, lifecycle, and the same task role. ECS schedules and stops them together. Putting a sidecar in a separate Task loses all of that.

## Recap

Task Definitions are immutable JSON manifests. Get the network mode right (awsvpc), CPU + memory + ephemeralStorage sized, the right runtimePlatform (Graviton if compatible), the containerDefinitions correct (especially dependsOn + healthCheck + logConfiguration), the volumes wired to mountPoints across containers, and the two IAM roles separated cleanly — execution for launch, task for runtime.

**Next — C3: ECS Networking.** Network modes (bridge, host, awsvpc — recommended, none); awsvpc ENI per Task + SG per Task; Service Connect (modern east-west); Service Discovery via Cloud Map; ALB + NLB integration with target type IP; VPC Lattice for ECS.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
