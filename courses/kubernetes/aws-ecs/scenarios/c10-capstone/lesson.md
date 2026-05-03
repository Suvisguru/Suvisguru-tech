# K-ECS C10 — C10 · Capstone — The Reference Multi-Service Fargate Harbor

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C10 · Capstone
> Companion preview: `/preview-kubernetes-ecs-lesson-10.html`.

---

**🎯 If you remember nothing else:** **The reference K-Harbor: Service Connect + ALB blue/green + EFS + Secrets/KMS + Container Insights + FireLens + ADOT/X-Ray + Service Auto Scaling + Fargate/Spot mix + circuit breaker + runbook. Every concept in C1-C9 has a place; the runbook closes the loop.**

## 1. Two Services, one ALB, Service Connect, EFS, Secrets

**Cluster**: `prod` with Container Insights enabled + Service Connect namespace `prod.local`.
    **Service A — api**: HTTPS API. Fargate launch type. `desiredCount: 6`. Task Definition: 1 vCPU + 2 GiB; awsvpc; `ephemeralStorage: 30 GiB`; one container *app* + one Firelens sidecar *log_router*. `capacityProviderStrategy: [{FARGATE, weight:1, base:6}]`. Two ALB target groups (blue + green) registered via `deploymentController: CODE_DEPLOY`. Service Connect `publishes: api`.
    **Service B — worker**: SQS consumer. Fargate launch type with Spot. `desiredCount: 2 (base) + auto-scaled by queue depth`. Task Definition: 0.5 vCPU + 1 GiB; awsvpc; *app* + *log_router* + *adot* sidecars. `capacityProviderStrategy: [{FARGATE, weight:1, base:2}, {FARGATE_SPOT, weight:4, base:0}]`. Service Connect `discovers: api` (worker calls API for callbacks).
    **EFS**: filesystem with two access points — `/uploads` (shared by api + worker), `/archive` (worker write-only). IAM-auth + transit-encryption ON. Mount targets in all three AZs.
    **Secrets**: Secrets Manager `prod/db`, `prod/api-key`, `prod/external-svc`; all encrypted with the `prod-app-secrets` customer KMS key. Execution role allows GetSecretValue + KMS Decrypt.

## 2. Three roles per Service; least-privilege by default

**Per-Service execution role**: ECR pull on the specific repo + GetSecretValue on the specific Secret ARNs + KMS Decrypt on the specific KMS key + CloudWatch Logs CreateLogStream/PutLogEvents on the specific log group + (api only) Firelens sidecar permissions.
    **Per-Service task role**:
    *api*: `dynamodb:GetItem/PutItem` on `arn:...table/orders`; `s3:GetObject/PutObject` on `arn:...bucket/uploads/*`; `sqs:SendMessage` on the worker queue. Plus ssmmessages:* for ECS Exec.
    *worker*: `sqs:ReceiveMessage/DeleteMessage` on the queue; `s3:GetObject` on uploads; `elasticfilesystem:ClientMount/ClientWrite` on the EFS access points; xray:PutTraceSegments + cloudwatch:PutMetricData. Plus ssmmessages.
    **CI/CD deploy role**: `ecs:RegisterTaskDefinition`, `ecs:UpdateService`, `codedeploy:CreateDeployment`, `iam:PassRole` on the execution + task role ARNs only. *No* direct AWS access overlapping with what the running Tasks have. Three-role separation: deploy creds, launch creds, runtime creds — three different scopes.

## 3. Blue/green + circuit breaker + autoscaling + telemetry

**Blue/green deploy via CodeDeploy**: *linear 10% per 5 min* with CloudWatch alarms — 5xxRate > 1% over 1 min OR P95Latency > 800ms over 5 min triggers auto-rollback. BeforeAllowTraffic Lambda smoke-tests the green TG. AfterAllowTraffic Lambda updates SLO dashboards.
    **Deployment circuit breaker** on the worker (rolling deploys for non-blue/green): `{ enable: true, rollback: true }`. Catches bad worker images without touching ALB-traffic-weight machinery.
    **Service Auto Scaling**:
    *api*: target tracking on `ALBRequestCountPerTarget = 200`; min 6, max 50.
    *worker*: target tracking on `SQSApproximateNumberOfMessagesVisible = 100`; min 2, max 30.
    **Capacity providers**: api on Fargate base (steady traffic; Spot interruption unacceptable for live API). Worker on Fargate base + Fargate Spot weighted 4:1 (queue tolerates interruption; ECS reschedules interrupted Tasks).
    **Observability**: Container Insights on; FireLens routes all logs to *CloudWatch live (14d)* + *S3 archive (Glacier after 30d)*; ADOT sidecar on every Service exports OTel traces to X-Ray + metrics to AMP. Service Connect emits per-service rps/latency/5xx automatically.

## 4. Every cause class → a 5-minute fix

The runbook. Pinned to the team's wiki + linked from oncall pages.
    **Symptom: Service A degraded (5xx spike + ALB unhealthy targets).**
    Step 1: `describe-services` events — circuit breaker / CodeDeploy alarm fired? If yes, rollback in flight; wait 5 min for stabilisation.
    Step 2: `describe-tasks --desired-status STOPPED` on recently stopped Tasks; read stoppedReason. If *OutOfMemoryError* → bump TD memory + redeploy. If *CannotPullContainerError* → check ECR perms / KMS / network.
    Step 3: ECS Exec into a RUNNING Task (any Task in the Service); curl localhost; check downstream connectivity to dependencies.
    Step 4: If symptoms remain after fix: `UpdateService --force-new-deployment` — replaces all Tasks.
    **Symptom: deploy stuck at 50% blue/green.**
    Step 1: CodeDeploy console — which Lambda hook is failing? Read its log group.
    Step 2: Manual decision: continue to 100% (if symptoms are noise) or auto-rollback. Default = auto-rollback after 10 min if not progressing.
    Step 3: Postmortem the bad-revision Tasks (still queryable in Stopped status).
    **Symptom: worker queue depth not draining.**
    Step 1: Check Service Auto Scaling — is it scaling out? `describe-scalable-target` + `describe-scaling-activities`.
    Step 2: Spot interruption rate up? Check capacity-provider strategy; consider temporarily shifting weight toward base Fargate.
    Step 3: Worker Task crashlooping? `describe-tasks STOPPED` in Service B; same chain.
    **Symptom: EFS-mounted Tasks stuck PROVISIONING.**
    Step 1: Mount target SG allows NFS (2049) from Task SG?
    Step 2: Subnet IPs available?
    Step 3: EFS access point still exists + IAM auth allowed?
    **The runbook lives because someone walks through it during low-stress dev / staging incidents** — at least monthly. *Game days* simulate failures; the runbook gets refined.

## Before / After

**Before.** Pre-this-design, AWS-shop teams running multi-service apps stitched together: a single big EC2 + Docker Compose, manual ALB target registration, host-baked secrets, ad-hoc log shipping, no traces, no autoscaling, no rollback path. Production incidents were day-long investigations.

**After.** The reference K-Harbor wires every C1-C9 concept into one defendable architecture. Service Connect for east-west; ALB blue/green for safe deploys; EFS for shared state; Secrets Manager + KMS for credentials; Container Insights + FireLens + ADOT/X-Ray for observability; Service Auto Scaling + Spot mix for cost + bursty load; circuit breaker + runbook for the rollback path. *Production incidents are 5-minute investigations.*

*The capstone is not a new concept — it's the disciplined assembly of everything before it. If your real architecture matches this, you have a defendable ECS deployment.*

## Analogy — the K-Harbor pier

The harbor master arrives at the **Grand Voyage** ceremony. Every pier is wired correctly. The signal flag tower (ALB) routes incoming traffic; the smart relay station (Service Connect) handles east-west. The cargo holds (EFS) hold shared state. The customs vault (Secrets + KMS) is double-locked. The lighthouse (Container Insights + FireLens + ADOT/X-Ray) sees every signal. The loading crew yard (Service Auto Scaling + capacity providers) sizes itself for the day's load. The salvage office (the runbook) has every failure family already mapped to a clear response. Two ships sail today — the API and the worker — each on the right kind of capacity. **The harbor is ready for the season.**
    The Grand Voyage is not a new concept; it's every previous district woven into one defendable harbor. C1's ECS shapes; C2's Task Definitions; C3's networking; C4's IAM + KMS; C5's storage; C6's deploy + scaling; C7's observability; C8's hybrid (kept simple here — pure cloud). Every K-Harbor lesson has a place on the map.
    The runbook is the discipline that keeps the harbor running when storms come. Each cause class — radio mast (ENI), warehouse handoff (image pull), customs vault (IAM/KMS), cargo too heavy (memory), lost crew letter (Essential exited), unhealthy ship (target health) — has a 5-minute response with a clear command. The harbor master practices the runbook on calm days so it's muscle memory by midnight.

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Grand Voyage ceremony | Capstone reference architecture |
| Two ships sailing today | Service A (api) + Service B (worker) |
| Signal flag tower | ALB with blue/green target groups + CodeDeploy |
| Smart relay station | Service Connect east-west |
| Shared cargo hold | EFS + access points (uploads + archive) |
| Customs vault, double-locked | Secrets Manager + customer KMS keys |
| Three letters per captain (deploy / launch / voyage) | CI/CD role + execution role + task role |
| Lighthouse with four observers | Container Insights + FireLens + ADOT + X-Ray |
| Load-aware crew yard | Service Auto Scaling target tracking + capacity providers |
| Steady ships on chartered berth | Fargate base capacity |
| Bursting ships on rented dock | Fargate Spot weighted strategy |
| Storm runbook on the wall | 5-minute failure-recovery runbook |

⚠️ *Analogy stops here:* A real harbor has years of accumulated muscle memory; the runbook only works if you exercise it during calm seas. Game days are the harbor's storm drills.

## ELI5 / ELI10

**ELI5.** The Grand Voyage is the day everything we've built ships at once. Every pier is wired right. The harbor master can route ships and the Salvage Office knows how to handle every kind of trouble in five minutes. The runbook is the harbor's storm playbook — practice it on calm days.

**ELI10.** Two Services on Fargate (api with blue/green via CodeDeploy + Service Auto Scaling target-tracking on ALBRequestCountPerTarget; worker on Fargate base + Fargate Spot weighted strategy with target-tracking on SQS depth), Service Connect east-west, ALB north-south, EFS shared state with access points + IAM auth, Secrets Manager + customer KMS keys, three IAM roles (CI/CD + execution + task), Container Insights + FireLens (CW + S3 archive) + ADOT + X-Ray, deployment circuit breaker on every Service, runbook mapping every cause class to a 5-minute fix.

## Real-world scenarios

- **Ship-it-Friday — first prod deploy on this architecture.** A 30-engineer SaaS replaces their single-EC2 + Compose stack with this reference. Day-1 deploy: blue/green via CodeDeploy with linear 10%-per-5min shift; CloudWatch alarms gate. *Five minutes from "go" to "100% on green"*; existing stack drained; team watches dashboards. Container Insights + traces show normal traffic. *Not a heroic deploy — a scripted one.*
- **Black Friday — autoscaling held.** Tax-deadline traffic 8× normal. `ALBRequestCountPerTarget` climbed; api Service scaled out from 6 to 28 over 12 minutes via target tracking. Worker queue depth spiked; Spot Tasks scaled out cheaply (some interruptions; SQS retries handled them). Latency P95 stayed under 300ms. *The runbook never opened.*
- **Bad deploy → blue/green rollback → 5-min postmortem.** A Friday deploy raised P95 latency above the 800ms alarm threshold during the 10% canary phase. CodeDeploy auto-rolled-back; listener flipped to blue; users saw a brief 30-second tail elevation. Postmortem chain (describe-tasks STOPPED on green Tasks → CloudWatch logs → root cause = stale cache stampede on cold-start) took 5 minutes; fixed in next revision; on-call closed the page. *The system caught itself.*
- **Game day — runbook proven on staging.** The team ran a quarterly game day on staging. Killed a Fargate Spot Task → autoscale replaced. Nuked the EFS mount target SG → Tasks PROVISIONING; runbook chain found the cause in 3 minutes. Tampered a Secret's KMS key policy → ResourceInitializationError; runbook chain found it in 4 minutes. *Confidence in the runbook is built before the storm, not during it.*

## Common misconceptions

- **Myth:** "This is over-engineered for a startup."
  **Truth:** Every layer here exists because something *doesn't* exist without it: blue/green for safe deploys, circuit breaker for runaway rollouts, observability for unknown unknowns, runbook for incident response. **The marginal cost** of including all of it on day 1 is small (Service Catalog templates do the heavy lift); the marginal cost of *adding it after the first incident* is much larger.
- **Myth:** "Blue/green is always better than rolling."
  **Truth:** Blue/green excels for *internet-facing* services where listener-flip-rollback is faster than launch-new-Task-rollback. For internal-only Services, rolling deploy + circuit breaker is simpler + cheaper (no two-target-group machinery) and almost as safe. The reference uses blue/green on api (internet-facing) and rolling on worker (internal queue consumer).
- **Myth:** "The runbook is documentation; we don't need to practice it."
  **Truth:** **Untested runbooks rot.** The cause-class commands change as AWS APIs evolve; the team's muscle memory fades; new failure modes emerge. Quarterly game days on staging keep both the runbook and the team current.

## Recap

The reference K-Harbor: two Fargate Services, ALB blue/green via CodeDeploy, Service Connect east-west, EFS + Secrets Manager + KMS, Container Insights + FireLens + ADOT/X-Ray, Service Auto Scaling, Fargate base + Spot mix, circuit breaker, three-role IAM separation, and a runbook kept current by game days. Every K-ECS concept woven into one defendable architecture.

**K-ECS complete.** 10 modules. 30+ hours of content. From C1's five-shape selection guide to C10's reference architecture. The K-Harbor map is fully populated. *Next courses in the K-* family* — possibly K-Lambda (event-driven AWS), K-AppRunner (single-service PaaS), or a return to the K8s family with K-K3s (k3s/k0s/MicroK8s). Decisions per founder direction.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
