# K-ECS C8 — C8 · ECS Anywhere and Hybrid — On-Prem and Edge Capacity

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C8 · ECS Anywhere and Hybrid
> Companion preview: `/preview-kubernetes-ecs-lesson-08.html`.

---

**🎯 If you remember nothing else:** **ECS Anywhere = control plane in AWS, capacity on your hardware. SSM + ECS agents register external instances. Networking is bridge/host (no awsvpc on external; no ALB). Pick for regulated, edge, hybrid bridge use cases — not for general-purpose workloads.**

## 1. Control plane in AWS, capacity on your hardware

**ECS Anywhere** extends the standard ECS control plane to capacity outside AWS. Your servers — on-prem racks, edge devices in retail / industrial sites, VMs in another cloud — register as *external instances*. ECS schedules Tasks onto them as if they were EC2 capacity, with constraints filtering "external-only" workloads.
    **Communications path**: external instance → outbound HTTPS to SSM Messages + ECS regional endpoints. *No inbound port* — the agents make the connection out. Behind a corporate firewall, only outbound 443 is needed (plus ICMP-based AWS health probes if Network Reachability is configured).
    **Cluster shape**: one ECS Cluster can have a mix of EC2, Fargate, and external capacity providers. Services declare which capacity they want via `capacityProviderStrategy`; Tasks marked `requiresAttributes` for `ecs.os-type=linux` and the EXTERNAL filter land on external instances.

## 2. SSM activation + agent installation

**Step 1 — SSM activation**: `aws ssm create-activation` generates a one-time activation code + ID. Activations have a default-instance-name + IAM role + region.
    **Step 2 — install agents on the server**: AWS provides a single shell script that installs the SSM agent + ECS agent + activates with the SSM code. Run as root.
    `curl --proto "https" -o "/tmp/ecs-anywhere-install.sh" \
  "https://amazon-ecs-agent.s3.amazonaws.com/ecs-anywhere-install-latest.sh"

sudo bash /tmp/ecs-anywhere-install.sh \
  --region us-east-1 \
  --cluster my-cluster \
  --activation-id $ACTIVATION_ID \
  --activation-code $ACTIVATION_CODE`
    **Step 3 — verification**: `aws ssm describe-instance-information` shows the registered server (Instance ID like `mi-XXXX`); `aws ecs list-container-instances` shows it in the ECS Cluster. Status: ACTIVE means it's ready for Tasks.
    **De-registration**: `aws ecs deregister-container-instance` + `aws ssm deregister-managed-instance`; uninstall the agents from the server.

## 3. bridge/host network only; no ALB; storage on host

**Networking limits**: external instances *do NOT support awsvpc* (no VPC ENIs on your hardware). Tasks use *bridge* or *host* network mode. Inbound traffic goes to the host's IP + container port; firewall + DNS are your responsibility.
    **ALB integration is unsupported** on external instances — ALB target type IP requires awsvpc; target type instance requires the instance to be in the VPC. For ingress to external instance Tasks, options are: (a) on-prem load balancer in front, (b) DNS round-robin, (c) Tasks publishing to a queue / event bus.
    **Service Connect is not supported** on external — east-west service discovery for external Tasks rolls over to Cloud Map (DNS) only.
    **Storage**: bind mounts to host paths work fine. EFS / FSx are AWS-cloud-only; not directly mountable on external. For shared state across cloud + on-prem, use S3 + S3 Gateway endpoint at the cloud side and S3 SDK calls from on-prem (or design for asynchronous handoff).
    **Operational**: external instances don't auto-heal — if the SSM agent dies or connectivity is lost, the instance disappears from the Cluster but ECS doesn't replace it (you're running it, not AWS). Capacity providers + managed scaling don't apply to external. *Treat external instances as carefully provisioned long-lived workers.*

## 4. When ECS Anywhere fits — and when it doesn't

**Strong fit**:
    
      - *Regulated workloads on-prem* — data residency rules forbid cloud; ECS control plane orchestrates locally-running containers under one Cluster you can also run cloud workloads in.

      - *Edge processing* — retail stores, factory floors, oilfield sensors; one ECS Cluster orchestrates per-site capacity for local data processing; periodic results upload to cloud.

      - *Gradual cloud migration* — register existing on-prem servers into a new Cluster; deploy on both old + new gradually; decommission on-prem capacity as cloud takes over.

      - *Hybrid burst* — steady on-prem + cloud burst; same Task Definitions deploy both places; capacity-provider strategy allocates per workload.

    
    **Weak fit (don't pick)**:
    
      - General-purpose web services — ALB + awsvpc + Service Connect missing kills the modern operational model.

      - Workloads needing EFS / FSx / RWX cross-Task storage — those are cloud-side only.

      - High-churn workloads — external instance churn is your operational burden; managed cloud capacity is more efficient.

    
    **Bottom line**: ECS Anywhere is a *bridge*. Pick when you have specific reasons to keep capacity outside AWS; don't pick because it sounds easier than managing standalone Docker hosts.

## Before / After

**Before.** Pre-ECS-Anywhere, hybrid workloads ran two separate orchestrators: ECS in the cloud, plain Docker / Compose / Swarm on-prem. Two operational models, two deploy pipelines, two monitoring stacks. Drift was constant. Migrating workload between environments meant rewriting the orchestration layer.

**After.** Modern ECS Anywhere keeps the control plane unified — one Cluster, one set of Task Definitions, one deployment workflow, one monitoring story. Capacity providers split the difference: cloud + on-prem capacity in one strategy. *The orchestrator stops being a per-environment burden.* Limits remain (networking surface narrower on external) but the bridge use case is well-served.

*ECS Anywhere is a real product, not a sales-deck checkbox. Use it for the bridge cases it's designed for; don't default to it for everything.*

## Analogy — the K-Harbor pier

The harbor isn't the only place ships dock. Some captains have private wharves at remote islands or up in the river estuary. The **Outport Station** is how those private wharves get registered into the K-Harbor system.
    The harbor master sends a *signed activation slip* (SSM activation code) to the wharf owner; the wharf owner installs two pieces of harbor equipment on their dock — a **radio reporter** (SSM agent) and a **cargo handler** (ECS agent) — and uses the slip to introduce the wharf to the harbor master. From then on, the wharf appears on the harbor map; the harbor master can route ships to it just like any harbor pier.
    But: it's still a private wharf, not a harbor pier. **The harbor's shared comms tower (awsvpc + Service Connect)** doesn't reach the wharf — local communications are by megaphone (bridge mode) or shouting from the deck (host network). **The harbor's entrance flag tower (ALB)** can't see ships at the wharf — incoming traffic from the open sea has to be handled by the wharf owner's own signal system. **The shared warehouse (EFS)** is on the harbor side; cargo at the wharf can't directly access it.
    The wharf is great when the cargo has to stay off-harbor for legal reasons (data residency), or when the wharf is closer to the source (edge processing), or when the wharf is being phased into the harbor over time (gradual migration). For everyday cargo work, it's simpler to dock at the harbor proper.

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Outport Station | ECS Anywhere registration layer |
| Private wharf at a remote island | external instance (on-prem / edge / other cloud) |
| Signed activation slip | SSM activation code + ID |
| Radio reporter on the wharf | SSM agent on external instance |
| Cargo handler on the wharf | ECS agent on external instance |
| Wharf appears on harbor map | external instance ACTIVE in Cluster |
| Harbor's shared comms tower (out of reach) | awsvpc network mode (unsupported on external) |
| Harbor's flag tower (out of reach) | ALB integration (unsupported on external) |
| Megaphone / shouting from deck | bridge / host network mode |
| Wharf-side cargo (cloud warehouse out of reach) | EFS / FSx (cloud-only; not on external) |
| Mixed flotilla — harbor + wharf assignments | capacity provider strategy with EXTERNAL + Fargate / EC2 |

⚠️ *Analogy stops here:* A real wharf is permanent capacity; ECS external instances disconnect when the agent stops or connectivity is lost — they vanish from the Cluster. There's no "empty wharf" — the wharf disappears from the harbor map.

## ELI5 / ELI10

**ELI5.** Some captains have private docks far from the harbor. The harbor master can still send them ships if they install harbor radios. But the private docks don't get the harbor's loudspeakers, the harbor's flag tower, or the harbor's shared warehouse. They're great for cargo that has to stay near the private dock, but harder for general-purpose work.

**ELI10.** **ECS Anywhere**: external instances (on-prem / edge / other cloud) join an ECS Cluster via `SSM agent + ECS agent` + an SSM activation code. **Limits**: no awsvpc, no ALB, no Service Connect, no Fargate, no EFS / FSx. **Network modes**: bridge / host / none. **Storage**: host filesystem only. **Use cases**: data-residency, edge, gradual migration, hybrid burst. **Don't use for**: general web services where the missing surface kills the operational model.

## Real-world scenarios

- **Edge — retail store inventory processor.** A retailer has 800 stores. Each store's back-office runs a small server processing point-of-sale data; results upload to cloud nightly. **ECS Anywhere**: each store is an external instance in a regional ECS Cluster; same Task Definitions deploy to all 800. *One Cluster + one CI pipeline; no per-store orchestration tooling.*
- **Compliance — healthcare analytics on-prem.** A health system can't move PHI to cloud. They run analytics Tasks on-prem racks; results aggregated to cloud (de-identified). ECS Anywhere keeps the orchestration unified — same TDs, same deploy story, same observability stack — while keeping data on regulated hardware. *Compliance + operational sanity.*
- **Migration bridge — gradual cloud move over 18 months.** A team migrating 40 services from on-prem to cloud. Phase 1: register on-prem servers as external; deploy ECS Tasks side-by-side with the legacy systemd-managed processes. Phase 2: spin up Fargate capacity in the same Cluster; capacity-provider strategy weights cloud-first, external-fallback. Phase 3: drain external; deregister. *The Cluster shape never changed; capacity moved underneath.*
- **Bad fit — "replace Docker Compose with ECS Anywhere" for a web app.** A team running a 5-service web app on a single on-prem server in Compose tried ECS Anywhere as a "pro upgrade." Lost ALB integration, lost service mesh, lost shared volumes across services (no EFS-equivalent). Operational complexity rose without orchestration value. *Postmortem*: stay on Compose for this case; pick ECS in the cloud or EKS if you want a real orchestrator.

## Common misconceptions

- **Myth:** "ECS Anywhere lets me run Fargate on-prem."
  **Truth:** No. **Fargate is AWS-managed cloud capacity**; it doesn't exist outside AWS. ECS Anywhere lets you register your own hardware as *external* capacity in an ECS Cluster. The Tasks running on external instances run on your hardware; the Cluster's control plane stays in AWS.
- **Myth:** "External instances support all ECS features."
  **Truth:** Significant limits: **no awsvpc, no ALB, no Service Connect, no EFS / FSx, no managed scaling**. Plan workload selection accordingly; ECS Anywhere is a bridge for specific use cases, not a drop-in equivalent of cloud-side ECS.
- **Myth:** "External instances self-heal like EC2 ASG."
  **Truth:** External instances are **your operational responsibility**. If the agent dies, the host crashes, or connectivity drops, ECS removes the instance from capacity but doesn't replace it. You run it; you fix it. (Capacity providers + managed scaling don't apply to external.)

## Recap

ECS Anywhere extends the ECS control plane to your hardware via SSM + ECS agents. Strong fit for regulated on-prem, edge, gradual migration, hybrid burst. Limits (no awsvpc, no ALB, no Service Connect) mean general-purpose web services should stay on cloud-side ECS or EKS.

**Next — C9: ECS Troubleshooting.** Tasks stuck PROVISIONING / PENDING (ENI, image pull, IAM); stoppedReason taxonomy (CannotPullContainerError, ResourceInitializationError, OutOfMemoryError); deployment circuit breaker firings; Service Connect endpoint issues; ALB target health failures.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
