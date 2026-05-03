# K-ECS C3 — C3 · ECS Networking — Network Modes, Service Connect, ALB/NLB, VPC Lattice

> Course: AWS ECS (K-ECS, **non-Kubernetes companion course**; prereq: AWS basics + container fundamentals)
> Module C3 · ECS Networking
> Companion preview: `/preview-kubernetes-ecs-lesson-03.html`.

---

**🎯 If you remember nothing else:** **awsvpc network mode is the recommended default — ENI per Task, SG per Task, required for Fargate. Service Connect is the modern east-west pattern (replaces App Mesh). ALB target type = IP for awsvpc Tasks. VPC Lattice for cross-VPC / cross-account application networking.**

## 1. bridge, host, awsvpc (recommended), none

**awsvpc** (recommended): every Task gets its own *elastic network interface (ENI)* inside one of your VPC subnets. Each Task has its own private IP, its own Security Group(s), and behaves like a tiny EC2 instance from the network's perspective. *Required for Fargate.* Subnet-aware — the Service's `networkConfiguration` lists which subnets and SGs Tasks land in.
    **bridge** (EC2 launch only; legacy): the default Docker bridge. Containers share the host's ENI; ports are mapped (containerPort → ephemeral hostPort). *Hostport collision* if two Tasks bind the same port on one host. ALB target type = instance (port range). *Avoid for new workloads.*
    **host** (EC2 launch only): containers use the host's network namespace directly; `hostPort` = `containerPort`. *Even more collision-prone* — a single Task per port per host. Used historically for sidecar agents that must see the host's network.
    **none**: no network. Only for batch Tasks that don't need network (e.g., they read from S3 via VPC endpoint accessed by the agent's host network). Rare.

## 2. ENI per Task, SG per Task, ENI limits, awsvpc trunking

In awsvpc, the ECS agent provisions an ENI for the Task before the container starts (Task state PROVISIONING). The ENI is attached to the host (EC2 or Fargate microVM); the Task's containers see only that ENI; outbound traffic flows through the VPC route tables.
    **SG per Task** is the win — different Tasks on the same host can have completely different ingress/egress rules. The SG is set in the Service's `networkConfiguration.awsvpcConfiguration.securityGroups`. *Pre-awsvpc, the SG was a host-level shared concern; now it scopes to the workload.*
    **ENI limits** (EC2 launch only): each EC2 instance has a max ENI count tied to its instance type (e.g., m5.large = 3 ENIs incl. the host's primary). Each Task takes one ENI. Trunking — the **awsvpc trunking** feature — lets supported instance types attach a "trunk" ENI that multiplexes many sub-ENIs, raising effective Task density per host. *Enable in ECS account settings; opt-in.*
    **Fargate** doesn't expose ENI limits to you — each Fargate Task is one microVM with one ENI; there's no host-density constraint. The Fargate platform handles VPC routing, ENI lifecycle, and egress IP assignment.

## 3. Modern east-west and the legacy DNS path

**Service Connect** (the recommended modern path) wires up east-west service-to-service traffic with a sidecar Envoy proxy. Configure on a per-Service basis: `serviceConnectConfiguration` declares a namespace and the names this Service publishes / consumes. Tasks call `http://service-b.cluster:8080`; the Service Connect proxy resolves it to a healthy Task ENI, load-balances, applies timeouts + retries, and emits app-level metrics (rps / latency / 5xx) into CloudWatch + Container Insights. *Replaces App Mesh patterns; no separate mesh control plane to run.*
    **Service Discovery via Cloud Map** (legacy but still supported): each Service registers Task ENIs as A records in a Cloud Map private DNS namespace (e.g., `service-b.local`). Other Tasks resolve the name and connect directly. *No L7 features* — just DNS. Fine for very simple east-west; missing retries, observability, traffic shaping. Service Connect is the upgrade.
    **When to use which**: Service Connect for any Service that does east-west calls. Cloud Map for simple cross-Service DNS without L7 needs. Both can coexist on the same Cluster.

## 4. north-south traffic; cross-VPC application networking

**ALB integration**: Service's `loadBalancers` array points each Task at a target group. Two target types matter:
    
      - **IP** (use with awsvpc): ALB registers Task ENI IPs directly. Stable, fast deregistration, plays well with rolling deploys + CodeDeploy blue/green.

      - **instance** (use with bridge / host): ALB registers EC2 instance + dynamic port. ENI doesn't exist per Task. Older shape; still works.

    
    Health checks: ALB-level (HTTP probe by ALB) *and* container healthCheck command in Task Definition. Both report into the rolling-deploy decision logic.
    **NLB**: same target-type story (IP for awsvpc); used for TCP/UDP / ultra-low-latency / static IP / TLS passthrough cases. ALB is the right default for HTTP/HTTPS.
    **VPC Lattice for ECS**: a managed service-to-service application-networking layer that spans VPCs and accounts *without VPC peering*. Configure a Lattice Service Network; register ECS Services as Lattice Targets. Lattice handles auth (IAM-based), encryption, observability, and routing across VPC boundaries. *Picks the share-services-across-accounts use case* that east-west Service Connect can't reach (it's scoped to one VPC + Cluster).

## Before / After

**Before.** Pre-awsvpc, ECS Tasks shared a host's ENI in bridge or host mode. Tasks colliding on hostPort. Security Groups host-level — every workload on a host had the same network policy. East-west service discovery was rolled by hand: scripts registering each Task in DNS via the agent metadata API. Cross-VPC traffic went through expensive peering or NLB endpoints. *Networking was an obstacle to scaling.*

**After.** Modern ECS networking uses awsvpc by default (and Fargate forces it). ENI per Task; SG per Task. Service Connect handles east-west with a sidecar Envoy + L7 features + observability. ALB target type IP integrates cleanly. VPC Lattice extends application networking across VPCs and accounts. *Networking is just configuration.*

*Almost every ECS networking question collapses to: "are you on awsvpc?" If yes, the rest follows. If no, you're on a legacy path and should plan migration.*

## Analogy — the K-Harbor pier

The **Lookout & Comms Tower** overlooks every pier in K-Harbor. The harbor master uses it to wire each ship's communications and route signal traffic between ships and to the outside world.
    In **awsvpc** mode, every ship at every pier gets its own radio mast (ENI) and its own access list (Security Group). Two ships at the same pier can have completely different radio rules. Compared to the *old shared-mast* approach (bridge / host modes — every ship on a dock used the dock's mast and had to negotiate which channel was free), awsvpc is decisively cleaner.
    For ship-to-ship traffic, **Service Connect** is a small relay station beside each ship (sidecar Envoy proxy). The relay knows which ships speak which language (which Service publishes which protocol on which port), routes the call over the radio network, retries when a ship is offline, applies timeouts, and reports back to the harbor's observatory (CloudWatch / Container Insights). Compared to the older Cloud Map approach (just a phone book — "this is service-B's number, dial it directly"), Service Connect gives you the smart switchboard.
    For ship-to-shore traffic (the public Internet calling in), there's a **signal flag tower** (ALB / NLB) at the harbor entrance. Ships register their IPs (target type IP) with the tower; the tower routes incoming calls. For talking to *other harbors entirely* — partner companies, sister offices in other regions — there's **VPC Lattice**: a managed inter-harbor switchboard that lets ships in different harbors talk to each other without needing a shared bridge.

**Translation legend.**

| In the story… | …in ECS / AWS |
|---|---|
| Lookout & Comms Tower | ECS networking layer |
| Each ship gets its own radio mast | awsvpc ENI per Task |
| Each ship's radio access list | Security Group per Task |
| Old shared-mast at the dock | bridge / host network mode (legacy) |
| Smart relay station beside each ship | Service Connect sidecar Envoy proxy |
| Phone book at the harbor office | Cloud Map service discovery (DNS only) |
| Signal flag tower at the harbor entrance | ALB / NLB |
| Ships registered by IP at the tower | ALB target type = IP |
| Ships registered by dock + slot | ALB target type = instance (bridge / host) |
| Inter-harbor switchboard | VPC Lattice (cross-VPC + cross-account) |
| Trunked masts (advanced docks) | awsvpc trunking — multiplexed ENIs per host |

⚠️ *Analogy stops here:* A real harbor has fixed radios; ECS ENIs are software ENIs that AWS provisions and tears down per Task. There's no "left-behind mast" — when a Task stops, its ENI is gone in seconds.

## ELI5 / ELI10

**ELI5.** Every ship gets its own radio. Two ships at the same dock can have totally different radio rules. When ships need to talk to each other there's a smart relay that knows everyone's phone numbers and reconnects calls if a ship is busy. When the outside world calls in, there's a flag tower at the harbor mouth that routes the call to the right ship.

**ELI10.** **awsvpc** = ENI + SG per Task; required for Fargate; recommended for EC2 launch. **Service Connect** = managed sidecar Envoy + namespace-scoped service discovery + L7 LB + retries + timeouts + app-level metrics; replaces App Mesh. **Cloud Map** = legacy DNS-only service discovery; coexists. **ALB target type IP** = recommended for awsvpc; ALB registers Task ENI IPs directly. **VPC Lattice for ECS** = managed cross-VPC + cross-account application networking without peering.

## Real-world scenarios

- **Polyglot fleet — Service Connect across 12 services.** A 100-engineer org has 12 ECS Services on Fargate. They enable Service Connect cluster-wide; each Service publishes its name (e.g., `orders.cluster:8080`); other Services consume by name. *App-level metrics* appear automatically in Container Insights; retries handle transient deploy turbulence. Migrating from App Mesh: configure once, App Mesh sidecars retired.
- **Compliance — SG per Task gates blast radius.** A regulated workload has Tasks A (PII handler) and Tasks B (public web) on the same Cluster + same hosts. Old bridge-mode deployment had one host SG — both got the same rules. Migrating to awsvpc: Task A gets a tight SG (egress only to specific RDS + KMS endpoints), Task B gets a wide-open egress. *Compliance audit shifts from "trust the host config" to "trust the per-Task SG."*
- **Cross-account integration — VPC Lattice replaces peering.** A platform team owns Service A in Account-1; partner team owns Service B in Account-2. Without Lattice, options were Transit Gateway + cross-account peering (3 weeks of networking work + ongoing NAT cost). With **VPC Lattice**: define a Lattice Service Network; register Service A as a target; share the network with Account-2; Service B in Account-2 calls A by Lattice DNS name with IAM auth. Stand-up: 1 day.
- **Outage — bridge-mode hostPort collision blocked deploys.** A team running 50 Tasks on bridge-mode EC2 hit hostPort 8080 collision when adding a new Service. Scheduler's desired count of 10 stalled at 8 (only 8 hosts had a free 8080). Latency on the failing Service climbed because the desired count was permanent under-provision. *Postmortem*: migrate to awsvpc. Each Task ENI eliminates the collision class entirely.

## Common misconceptions

- **Myth:** "Service Connect is just App Mesh with a different name."
  **Truth:** Service Connect is a different design — managed by ECS with cluster-wide namespace + simpler config + tighter ECS integration; no separate App Mesh control plane. App Mesh is general-purpose multi-cluster mesh; Service Connect is purpose-built for ECS east-west and emits ECS-aware metrics.
- **Myth:** "awsvpc is only for Fargate."
  **Truth:** awsvpc is *required for Fargate* and *recommended for EC2 launch*. EC2 launch can also use awsvpc — get the same ENI-per-Task + SG-per-Task benefits on EC2 you get on Fargate. The trade is ENI density per host (mitigated by awsvpc trunking).
- **Myth:** "VPC Lattice is the same as VPC peering for ECS."
  **Truth:** VPC peering wires VPCs at the network layer (route tables + CIDRs). VPC Lattice is application-layer service networking — registers ECS Services as targets, handles auth (IAM), encryption, retries, observability. Lattice is for service-to-service across boundaries; peering is for raw IP routing.

## Recap

ECS networking pivots on awsvpc — ENI + SG per Task. Service Connect for east-west. ALB target type IP for north-south. VPC Lattice for cross-VPC + cross-account. Bridge / host modes are EC2-launch legacy; migrate when possible.

**Next — C4: IAM and Security.** Task execution role vs task role; Secrets Manager / SSM Parameter Store injection; KMS; ECR auth; private registry auth; SGs; Fargate platform versions and patching; VPC endpoints; compliance (PCI, HIPAA, FedRAMP).

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
