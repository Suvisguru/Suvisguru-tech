# K-ECS C6 — C6 · ECS Deployment and Scaling

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C6 · Deployment and Scaling
> Companion preview: `/preview-kubernetes-ecs-lesson-06.html`.

---

**🎯 If you remember nothing else:** **Rolling is the default; blue/green is for richer rollback (CodeDeploy). Always enable the deployment circuit breaker. Service Auto Scaling for Task count; capacity providers + managed scaling for cluster nodes. Placement strategies (binpack / spread / random) + constraints set Task→host affinity.**

## 1. deploymentConfiguration, minimumHealthyPercent, maximumPercent, circuit breaker

Default `deploymentController: { type: ECS }`. Rolling deploy: ECS starts new Tasks, registers them with the ALB target group, waits for health, drains old Tasks, deregisters and stops them.
    **deploymentConfiguration.minimumHealthyPercent**: minimum % of desired-count that must remain RUNNING + healthy during a deploy. Default 100 (no over-provision needed but slower). 50 lets ECS stop half the old Tasks before launching new ones (faster on small Services, riskier capacity dip).
    **deploymentConfiguration.maximumPercent**: max % of desired-count Tasks running simultaneously (old + new combined). Default 200 (lets ECS double-deploy). Set to 100 for tight resource scenarios where you can't afford extra capacity briefly.
    **deploymentCircuitBreaker**: `{ enable: true, rollback: true }`. ECS watches new Task health during the rollout; if a configurable failure threshold is crossed (Tasks failing or new Tasks failing health checks), it stops the rollout and rolls back to the previous Task Definition revision. **Enable on every Service.** Default is off (legacy).
    **healthCheckGracePeriodSeconds**: time after a Task starts before ALB / container health checks count against the deploy decision. Set generously (60-120s) for apps with slow startup.

## 2. Two target groups, listener swap, canary + traffic shift

`deploymentController: { type: CODE_DEPLOY }` hands deploys to AWS CodeDeploy. Two ALB target groups (blue + green); CodeDeploy launches new Tasks into the green TG; runs *BeforeAllowTraffic* Lambda hooks (smoke tests); shifts traffic via the ALB listener; runs *AfterAllowTraffic* Lambda hooks; drains old Tasks.
    **Traffic shift modes**: *AllAtOnce* (full cutover; fast); *Linear* (10% per N minutes — gradual); *Canary* (10% then wait then 100%). Combine with **CloudWatch alarms** in the Deployment Group: alarm trips → CodeDeploy auto-rollback.
    **When pick blue/green over rolling?** When you want a separate test surface before traffic shifts (the green TG is private to CodeDeploy until cutover); when you need *fast rollback* (blue stays warm — listener flip back is seconds, not new-Task-launch); when alarm-driven rollback matters (your CloudWatch metric is the rollback trigger).
    **EXTERNAL deployment controller** [ deep dive — skip if new ]: you drive the deploy via ECS API directly (CreateTaskSet / UpdateServicePrimaryTaskSet / DeleteTaskSet). For custom deploy strategies (Argo Rollouts / Spinnaker-style controllers external to AWS).

## 3. Task count + node count

**Service Auto Scaling** uses Application Auto Scaling: register the ECS Service as a scalable target; attach scaling policies. Three policy types:
    
      - **Target tracking** (recommended): pick a metric (ECSServiceAverageCPUUtilization, ECSServiceAverageMemoryUtilization, ALBRequestCountPerTarget) + target value (e.g., 60% CPU). Auto Scaling computes the policy.

      - **Step scaling**: define alarm bands → adjust desired count by N. Older / more manual.

      - **Scheduled**: cron-style adjustments — "scale to 50 at 09:00 weekdays".

    
    **Cluster Auto Scaling** (EC2-launch only): **capacity providers** bind a Cluster to an EC2 Auto Scaling group with managed scaling — ECS computes how many instances are needed to host pending Tasks and scales the ASG. Avoids the older pattern of separate ECS desired-count + Cluster ASG that didn't coordinate.
    **Capacity provider strategies**: a Service's `capacityProviderStrategy` mixes capacity providers — e.g., 80% Fargate Spot, 20% Fargate base; ECS launches Tasks across the strategy. Use for Spot blending, multi-AZ EC2 + Fargate fallback, etc.

## 4. Where Tasks land on capacity

**placementConstraints** filter *which* hosts a Task can run on (EC2 launch only — Fargate ignores). Two kinds:
    
      - `distinctInstance` — at most one Task per host (HA pattern).

      - `memberOf` with cluster-query expression — "only on instances with attribute X" (instance type, AZ, custom attribute).

    
    **placementStrategies** control *preference order* for hosts that satisfy the constraints. Three:
    
      - **binpack** — pack onto fewest hosts possible (cost optimisation; reduces idle host count).

      - **spread** — evenly distribute by attribute (e.g., AZ for HA).

      - **random** — random selection.

    
    **Common combos**: *spread by AZ + binpack by memory* (HA across AZs while packing memory tight); *distinctInstance + spread by AZ* (one Task per host across all AZs for control-plane workloads).
    **Fargate placement**: AWS picks the underlying microVM placement; you can't influence it directly. AZ-spread comes from listing multiple subnets in `networkConfiguration` (one subnet per AZ).

## Before / After

**Before.** Pre-circuit-breaker, bad ECS deploys ran to completion or hung at partial-healthy state requiring manual UpdateService rollback. Pre-capacity-providers, autoscaling at the Cluster level (EC2 ASG) and Service level (desired count) were uncoordinated — pending Tasks waited for ASG to scale; ASG scaled based on CPU not pending Tasks. Manual sync.

**After.** Modern ECS deploys watch themselves (circuit breaker auto-rollback), capacity providers coordinate Cluster + Service scaling automatically (managed scaling drives ASG to fit pending Tasks), Service Auto Scaling target-tracks any CloudWatch metric, blue/green via CodeDeploy adds rich rollback semantics, and placement strategies + constraints encode operational intent declaratively.

*Get the deploy controller right + circuit breaker on + capacity providers in place; the rest is mostly tuning.*

## Analogy — the K-Harbor pier

The **Loading Crew Yard** is where new ships get prepared before being moved to active piers. Two crew rotation styles work in this yard.
    **Rolling rotation**: the harbor master starts new ships at adjacent slips, lets them warm up + pass medical inspection (ALB target health), then drains the old ships from active piers and decommissions them. The yard stays mostly busy throughout. A *safety inspector* (the deployment circuit breaker) watches; if too many new ships fail inspection in a window, the inspector calls a halt and reverts to the prior crew. *Always enable the safety inspector.*
    **Blue/green rotation** (CodeDeploy): two parallel pier groups (blue + green). Old crew at blue; new crew warms up at green privately. Inspector runs sea-trials at green (CloudWatch alarms during canary). When green passes, the harbor master flips the harbor entrance signal to route incoming shipments to green. Blue stays warm in case a flip-back is needed. Richer; takes a bit more orchestration.
    For sustained traffic, **Service Auto Scaling** watches the active piers' load (CPU / memory / request count) and adds or drains ships automatically — target tracking is the recommended dial. For the *yard's capacity itself* (how many crew bays exist), **capacity providers** let the harbor master compute "we need 5 more bays for pending ships" and scale the rental yard up — instead of the old pattern of separate yard-sizing and crew-sizing decisions.
    Where ships dock is governed by **placement**: constraints filter the eligible piers (only piers with a certain crane type, only certain AZs); strategies pick among eligibles (pack everything onto the fewest piers for cost, spread evenly across AZs for resilience, distinctInstance for "one per pier").

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Loading Crew Yard | ECS deployment + scaling layer |
| Rolling rotation | deploymentController: ECS (rolling) |
| Safety inspector calls halt | deploymentCircuitBreaker (auto-rollback) |
| Min healthy + max double-up rules | minimumHealthyPercent + maximumPercent |
| Sea-trial waiting period | healthCheckGracePeriodSeconds |
| Two pier groups + entrance flip | blue/green via CodeDeploy (two target groups) |
| Trial run with canary alarm | CloudWatch alarm in CodeDeploy Deployment Group |
| Watch the active piers | Service Auto Scaling (target tracking) |
| Yard rental sizing | capacity providers + managed scaling |
| Pier eligibility filter | placementConstraints (distinctInstance / memberOf) |
| Pier preference order | placementStrategies (binpack / spread / random) |

⚠️ *Analogy stops here:* A real harbor crew is hours of work; ECS Tasks rotate in seconds. The "warm up + drain" sequence is real but the timescales make some patterns from physical-yard logistics not transfer directly.

## ELI5 / ELI10

**ELI5.** When you change something in your ship, the harbor swaps in new ships gradually so passengers don't notice. A safety inspector watches; if too many new ships fail their checks, she calls a halt and brings back the old ones. There's also a fancier swap-out that uses two pier groups — flip a switch when the new group is ready. The yard adds and removes crews automatically based on how busy the piers are.

**ELI10.** **Rolling deploys**: minimumHealthyPercent + maximumPercent control the over/under-provision; **deploymentCircuitBreaker** auto-rolls-back. **Blue/green via CodeDeploy**: two target groups + listener swap; canary / linear / all-at-once traffic shift; CloudWatch alarms drive auto-rollback. **Service Auto Scaling**: target tracking (CPU / memory / ALB request count), step, scheduled. **Cluster Auto Scaling**: capacity providers with managed scaling drive EC2 ASGs based on pending Tasks. **Placement**: constraints (distinctInstance, memberOf) + strategies (binpack / spread / random).

## Real-world scenarios

- **Standard SaaS — rolling + circuit breaker.** A 50-engineer SaaS with 10 ECS Services on Fargate. Every Service has `deploymentCircuitBreaker: { enable: true, rollback: true }`, minimumHealthyPercent=100, maximumPercent=200. Standard rolling deploys; circuit breaker has caught two bad images this quarter. *Default + circuit breaker is the right baseline for almost everything.*
- **Regulated workload — blue/green with CloudWatch alarm gate.** A health-tech runs a PHI-handling API. **blue/green via CodeDeploy**: linear 10%-per-5min traffic shift. CodeDeploy Deployment Group has a CloudWatch alarm on `5xx-rate > 1%`. Bad deploy → alarm trips → CodeDeploy auto-rollback (listener flips back to blue, green Tasks drained). *Compliance gets a documented gradual-rollout + rollback story.*
- **Cost optimisation — Fargate + Fargate Spot blend.** A 25-engineer team runs background workers tolerant to interruption. Capacity provider strategy: *2 Tasks Fargate base + 80% Fargate Spot weight*. Steady 2 Tasks always; bursts go to Spot at ~70% discount. **Service Auto Scaling target-tracks** SQS queue depth → scales out when backlog grows. *Saved ~60% on the worker fleet.*
- **Outage — bad deploy without circuit breaker.** A team rolled a Task Definition revision with a memory leak. Tasks restarted every 8 minutes. Service stayed at 70% healthy churning forever. Latency tail climbed; oncall paged. **30-minute manual rollback** via UpdateService to prior revision. *Postmortem*: enable deploymentCircuitBreaker on every Service; ship a runbook for prod-rollback under 5 minutes.

## Common misconceptions

- **Myth:** "The deployment circuit breaker is on by default."
  **Truth:** It is **off by default** for legacy compatibility. You must explicitly set `deploymentCircuitBreaker: { enable: true, rollback: true }`. Enable on every Service — the cost is zero; the catch-rate on bad deploys is huge.
- **Myth:** "Service Auto Scaling and ASG autoscaling are the same."
  **Truth:** **Service Auto Scaling** changes the ECS Service's *desired Task count*. **EC2 ASG autoscaling** changes the *EC2 instance count*. Two different layers. **Capacity providers + managed scaling** bridge them — managed scaling adjusts the ASG based on pending Task capacity needs.
- **Myth:** "binpack always saves money."
  **Truth:** **binpack maximises host utilisation** — but if the workload has spiky memory and Tasks land on already-loaded hosts, OOM kills surface. *spread by AZ + binpack by memory* gets HA + density. Pure binpack on bursty workloads is a famous footgun.

## Recap

Three deployment controllers; rolling default + circuit breaker is the safe baseline. Blue/green for richer rollback. Service Auto Scaling for Task count; capacity providers for cluster sizing. Placement strategies + constraints encode operational intent.

**Next — C7: ECS Observability.** CloudWatch Container Insights for ECS; ECS Exec for interactive shell; FireLens (Fluent Bit / Fluentd) for log routing; ADOT for metrics + traces; AWS X-Ray.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
