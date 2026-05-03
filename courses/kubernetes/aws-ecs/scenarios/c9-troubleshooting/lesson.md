# K-ECS C9 — C9 · ECS Troubleshooting — Stuck Tasks, Stopped Reasons, Deploy Failures

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C9 · ECS Troubleshooting
> Companion preview: `/preview-kubernetes-ecs-lesson-09.html`.

---

**🎯 If you remember nothing else:** **Read top-down: describe-tasks → stoppedReason → service events → CloudWatch logs → ECS Exec. Each step narrows the cause class. Stop reading the moment the cause is identified — most ECS failures are in the first three categories: ENI / image pull / IAM-KMS.**

## 1. ENI, image pull, IAM, KMS — the launch-time failure quartet

A Task in PROVISIONING / PENDING for >2 minutes is unhappy. Four likely causes:
    
      - **ENI provisioning stalled** (awsvpc) — subnet has no free IPs (`VPC.IPAddressLimitExceeded`); VPC ENI limit hit per Region; SG references missing. Check: `describe-tasks` stoppedReason / lastStatus + VPC subnet free IP count + AWS Health Dashboard.

      - **Image pull stalled / failed** — execution role missing ECR perms; ECR repo policy denies; KMS key for ECR-encrypted repo missing Decrypt; private registry creds wrong (`repositoryCredentials`); registry network unreachable (no VPC endpoint or NAT). *stoppedReason: CannotPullContainerError* on the Task.

      - **Execution role + KMS missed** — execution role missing `secretsmanager:GetSecretValue` or `kms:Decrypt` on the secret's key. *stoppedReason: ResourceInitializationError: unable to retrieve secret value*.

      - **Capacity unavailable** — Service desired count exceeds available capacity in the chosen capacity provider (Fargate quota, EC2 ASG full, external instance count low). Service event: "unable to place a task because no container instance met all requirements".

    
    **First-look commands**: `aws ecs describe-tasks --cluster X --tasks ID --query "tasks[].lastStatus,stoppedReason"` + `aws ecs describe-services --query "services[].events[:5]"`.

## 2. Read the reason; take the matching action

**Common stoppedReason values + their cause classes**:
    
      - **CannotPullContainerError**: ECR / private registry pull failed. Look at the message tail: *"no basic auth credentials"* = repositoryCredentials wrong; *"manifest unknown"* = image tag/digest doesn't exist; *"AccessDenied"* = ECR repo policy or execution role IAM.

      - **ResourceInitializationError**: launch-time AWS resource fetch failed — Secrets Manager, SSM, KMS, log group create. The message tail names the failed resource.

      - **OutOfMemoryError**: container hit its memory hard limit. *Increase the Task or container `memory`*, or fix the leak.

      - **Essential container in task exited**: an essential container exited with non-zero code; whole Task stopped. Check the container's *exit code + last log lines*.

      - **Health check failed**: container healthCheck reported unhealthy past the configured retries. Tighten or loosen the healthCheck spec; verify the command works against the container's actual entrypoint.

      - **USER_INITIATED**: someone (or a deploy / scale) explicitly stopped the Task. Not a failure.

    
    **Exit codes**: container `exitCode` in `describe-tasks` shows the precise integer. 137 = SIGKILL (often OOM); 139 = SIGSEGV; 143 = SIGTERM (graceful stop). Map to your app's known exit-code conventions.

## 3. A deploy halted itself — read why

If the deployment **circuit breaker** fires, the Service rolls back to the previous Task Definition revision automatically. The `describe-services` events tab shows: "deployment circuit breaker — service has been rolled back". The root cause is upstream of that — *the new revision's Tasks failed health*. Look at the Tasks of the new (now-rolled-back) revision via `list-tasks --desired-status STOPPED` + read their stoppedReasons.
    **CodeDeploy blue/green rollback**: AWS CodeDeploy console shows a Failed deployment with the alarm that tripped (e.g., "5xxRate Alarm in ALARM state"). Linear / canary deploys give you the partial-traffic snapshot before rollback — useful for understanding the failure mode. Hooks (BeforeAllowTraffic / AfterAllowTraffic Lambdas) emit logs in their own log groups; failed hook = failed deploy.
    **Common deployment failure patterns**: (a) *app crashes on start* with new env / secret value (revert; verify config). (b) *health check fails* because new revision changed startup time (raise healthCheckGracePeriodSeconds). (c) *resource limits too tight* (revision changed CPU/memory; OOM at start; raise the limit). (d) *downstream dependency degraded* (new revision's integration test fails; not really a deploy failure but symptom shows there).

## 4. Tasks RUNNING but not serving traffic

Task is RUNNING (container started, healthCheck passing) but **ALB target health** is unhealthy. Six causes in increasing rarity:
    
      - **SG mismatch** — Task SG doesn't allow inbound from ALB SG on the container port. (Most common.)

      - **Wrong port** — ALB target group port doesn't match the Task's containerPort.

      - **Wrong path** — ALB health check path returns non-200 (e.g., `/healthz` not implemented; redirects to `/`).

      - **Slow startup** — app takes > ALB unhealthy threshold × interval to become ready; raise `healthCheckGracePeriodSeconds` on the Service.

      - **App crashes on first health probe** — check container logs.

      - **Network ACLs / route table** — uncommon; subnet config blocking ALB-to-Task path.

    
    **Service Connect endpoint failures**: A Service can't reach `service-b.namespace`. (a) Service Connect not enabled on the consumer Service's Service-level config. (b) Consumer doesn't have the right namespace ARN in its serviceConnectConfiguration. (c) The Cloud Map namespace SG blocks. (d) The producer Service's Tasks are unhealthy and not registered in Service Connect.
    **ECS Exec for live debug**: when the issue manifests inside the container (DNS resolution, downstream timeout, in-memory state), Exec into one of the running Tasks: `aws ecs execute-command --cluster X --task ID --container Y --command "/bin/sh" --interactive`. Run `nslookup` / `curl` / `netstat` / read in-memory state. Faster than restart-and-pray.

## Before / After

**Before.** Pre-circuit-breaker, pre-stoppedReason richness, ECS troubleshooting was: notice a Service is unhealthy → guess → restart → guess again. Logs went to CloudWatch but you had to know which log group; events on the Service tab were generic; ECS Exec didn't exist. Bad deploys ran to completion or hung at partial-healthy; manual rollback was a 30-minute investigation.

**After.** Modern ECS troubleshooting follows a chain: describe-tasks gives stoppedReason + exit code; describe-services events show capacity / scheduling failures; CloudWatch + Container Insights show the surrounding metrics; ECS Exec opens a live shell. Most issues are localised to one of four families (ENI, image pull, IAM/KMS, capacity) and surface in the first three commands. The deployment circuit breaker auto-rolls-back; CodeDeploy alarms drive blue/green rollback. *Diagnoses that took an hour now take five minutes.*

*Read the chain top-down. Don't debug-by-restart. Most ECS failures live in the first three categories — ENI, image pull, IAM-KMS — and the first three commands surface them.*

## Analogy — the K-Harbor pier

The harbor's **Salvage Office** is where things that went wrong come for forensic review. The salvager (you) reads a chain of evidence top-down.
    First the **boarding log** (describe-tasks) — what state is the ship in? Stuck at boarding (PROVISIONING / PENDING) usually means: the customs official couldn't set up the radio mast (ENI provisioning), the warehouse couldn't hand over the cargo (ECR pull), or the boarding letter was missing the right stamps (IAM / KMS).
    Next the **stop-reason slip** (stoppedReason) — if the ship stopped in the harbor: "could not pull container" (warehouse problem), "resource init error" (vault / KMS problem), "out of memory" (cargo too heavy for the deck), "essential container exited" (the captain abandoned ship; check exit code), "health check failed" (the medic flunked the ship).
    Then the **harbor events log** (service events) — capacity issues like "no berth available with the right wiring" surface here. The **signal officer's archive** (CloudWatch logs) holds detailed context. Finally, the salvager can **climb aboard** a still-running but troubled ship (ECS Exec) to inspect the engine room directly — no SSH ladders, no boarding planks, the lighthouse opens an authenticated channel straight in.
    The technique is to read top-down and stop the moment the cause is identified. Most failures live in the first three categories — radio mast, warehouse, boarding letter.

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Salvage Office | ECS troubleshooting layer |
| Boarding log | describe-tasks (lastStatus + stoppedReason) |
| Stuck at radio-mast setup | ENI provisioning stalled (subnet IPs / SG) |
| Stuck at warehouse handover | image pull (CannotPullContainerError) |
| Stuck at boarding-letter check | IAM / KMS (ResourceInitializationError) |
| Stop-reason slip | stoppedReason field |
| Cargo too heavy for the deck | OutOfMemoryError (memory limit) |
| Captain abandoned ship | Essential container in task exited (exit code) |
| Medic flunked the ship | Health check failed (container healthCheck) |
| Harbor events log | Service describe-services events |
| Auto-cancel + revert | deployment circuit breaker rollback |
| Climb aboard the ship | ECS Exec for live container debug |

⚠️ *Analogy stops here:* A real ship can have many simultaneous problems; ECS Tasks have one stoppedReason per stop event. The reason names the most-recent + most-specific cause; deeper context is in CloudWatch logs.

## ELI5 / ELI10

**ELI5.** When a ship gets in trouble, the salvager reads four pieces of paper in order: the boarding log (where did it stop?), the stop-reason slip (why did it stop?), the harbor events (what was happening around it?), and the signal officer's archive (what was it saying?). Then if the ship is still floating, the salvager can climb aboard and look around inside.

**ELI10.** Read top-down: **describe-tasks** → lastStatus + stoppedReason; **describe-services** → events for capacity / scheduling; **CloudWatch logs** → app + agent context; **ECS Exec** → live shell into a running container. Common stoppedReasons: *CannotPullContainerError* (image / IAM / KMS), *ResourceInitializationError* (Secrets / KMS / log group create), *OutOfMemoryError* (memory), *Essential container exited* (app crash; read exit code). Deploy failures: circuit breaker fires + auto-rollback; CodeDeploy alarm rollback. ALB target-health failures most often = SG mismatch.

## Real-world scenarios

- **Image pull fail — KMS Decrypt missing on execution role.** A Service's Tasks all stop with *CannotPullContainerError: failed to decrypt image manifest with KMS key arn:...*. Execution role had ecr:* on the repo but missed kms:Decrypt on the customer-managed KMS key the ECR repo was encrypted with. *Fix in 4 minutes* after reading the stoppedReason; would have been an hour of guesswork without it.
- **OOM after Task Definition revision change.** New revision raised the workload's baseline memory; container memory was unchanged; OOM at startup. stoppedReason: *OutOfMemoryError: Container killed due to memory usage*. Bumped Task Definition memory from 512 to 1024 MiB; new revision; ran clean. Postmortem ticket: add memory-utilisation alarm at 80% as early warning before OOM events.
- **Stuck PROVISIONING — subnet ran out of IPs.** During an autoscale-out spike, Tasks stuck PROVISIONING with *VPC.IPAddressLimitExceeded*. The Service's subnet (a /27 with 27 usable IPs) was full. Fix: added two more subnets to the Service's networkConfiguration; ECS spread Tasks across all three; subnet IP exhaustion no longer a single-subnet issue.
- **Outage — circuit breaker disabled, bad image churned all night.** A team's Service had circuit breaker disabled. A bad image rolled out at 22:00; Tasks crashlooped; rollout never completed. By 03:00 the Service was at 30% healthy. Postmortem: enabled circuit breaker + automated runbook to UpdateService rollback under 5 minutes. *The circuit breaker would have caught this in 90 seconds.*

## Common misconceptions

- **Myth:** "If a Task is RUNNING, the Service is healthy."
  **Truth:** **RUNNING means container started + container healthCheck passing**. ALB target health is separate (HTTP probe by ALB). A Task can be RUNNING but ALB-Unhealthy because of SG, port, or path mismatch — and the Service won't serve traffic to it. Always check both layers.
- **Myth:** "OutOfMemoryError means the host is out of memory."
  **Truth:** No. **OOM here is per-container hard limit** — the container hit its `memory` hard limit and got SIGKILL. Other containers on the host (and the host itself) are unaffected. The fix is per-container memory + per-Task memory in the Task Definition, not host sizing.
- **Myth:** "Restart the Service usually fixes ECS issues."
  **Truth:** **Restart-and-pray is the slowest debug technique.** ECS surfaces the failure cause in stoppedReason within seconds of the failure. Restart loses that context (the original Task is gone). Read the chain first; restart only when the chain has named the cause and you've fixed the underlying issue.

## Recap

Read the chain top-down. describe-tasks → stoppedReason → events → CloudWatch logs → ECS Exec. Most failures cluster in four families: ENI / image pull / IAM-KMS / capacity. Stop reading the moment the cause is identified.

**Next — C10 capstone: Multi-Service Fargate App.** Service Connect + ALB + EFS + Secrets Manager + CodeDeploy blue/green + Container Insights + autoscaling + failure-recovery runbook. The reference K-Harbor.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
