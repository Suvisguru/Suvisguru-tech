# K-EKS E3 — E3 · AWS Networking for EKS (VPC CNI, ALB/NLB, Gateway API, VPC Lattice)

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E3 · AWS Networking
> Companion preview: `/preview-kubernetes-eks-lesson-03.html`.

---

**🎯 If you remember nothing else:** AWS VPC CNI gives Pods real VPC IPs via secondary ENIs/IPs. **Enable prefix delegation** (16x more IPs per ENI) — this is non-negotiable for serious clusters. **AWS LB Controller** creates ALBs from Ingress/HTTPRoute, NLBs from Services. **VPC Lattice + AWS Gateway API Controller** for cross-VPC service-to-service. **ExternalDNS** for Route 53. **SG-for-pods** for per-Pod security groups. **Cilium / Calico / AWS Cilium dataplane** as alternatives.

## 1. VPC CNI — IP exhaustion is the default

AWS VPC CNI gives every Pod a real IP from your VPC subnet. No VXLAN, no overlay — Pods are first-class VPC citizens. Pod-to-Pod traffic stays in VPC routing; Pod-to-AWS-service traffic uses VPC endpoints; SG-for-pods works on real ENIs.
    The cost: every Pod consumes a real VPC IP. Each EC2 instance type supports a fixed number of **ENIs** + **IPs per ENI**. A `t3.medium` supports 3 ENIs × 6 IPs = 18 IPs. A `m5.large` = 3 × 10 = 30. *That's your Pod limit per node*.
    **Prefix delegation** (default-disabled, but you should enable it): the CNI gets `/28` prefixes (16 IPs each) per ENI instead of single IPs. Same 3 ENIs now hold 48 IPs. **Enable this on every cluster.**

## 2. VPC CNI variants + alternatives

- **AWS VPC CNI (default)** — Pods get VPC IPs. Enable prefix delegation. Use **custom networking** if your VPC is small + you need separate Pod subnets (often a /16 just for Pods).

      - **SG-for-pods** — assign SecurityGroups to specific Pods (not just nodes). Useful for fine-grained AWS-service ACLs (e.g., "only Pods with this SG can hit the RDS").

      - **IPv6 / dual-stack** — every Pod gets an IPv6 (unlimited), eliminating IP exhaustion entirely. Some workloads fully on IPv6.

      - **Cilium on EKS** — replace VPC CNI with Cilium. eBPF data plane, kube-proxy replacement, Hubble, FQDN policies. Trades VPC integration for Cilium features.

      - **Calico on EKS** — overlay or BGP. Mature; FIPS variants.

      - **AWS Cilium dataplane** — newer hybrid: AWS-supported Cilium with VPC CNI integration. Best of both.

## 3. AWS LB Controller + Gateway API + VPC Lattice

**AWS Load Balancer Controller** watches K8s objects + provisions AWS LBs:
    
      - **Ingress** with `kubernetes.io/ingress.class: alb` → ALB (L7 routing, TLS termination, WAF integration).

      - **Service type=LoadBalancer** with `service.beta.kubernetes.io/aws-load-balancer-type: external` → NLB (L4, low latency, static IP, EIP).

      - **Target type**: `ip` (LB sends to Pod IPs directly — modern default; needs VPC CNI or Cilium with VPC routing) or `instance` (LB sends to node, kube-proxy redirects — legacy).

      - Annotations control: scheme (internal/internet-facing), subnets, SSL cert, WAF, access logs, and ~50 more.

    
    **AWS Gateway API Controller for VPC Lattice** (released GA 2024): implements Gateway API for cross-VPC / cross-account service-to-service. Each VPC Lattice service group spans VPCs + accounts; service mesh-like without sidecars. New clusters in 2026 increasingly use this for multi-account architectures.
    **ExternalDNS**: K8s controller that watches Ingresses + Services + HTTPRoutes with hostname annotations + creates Route 53 records. Use private hosted zones for internal services.

## 4. PrivateLink, TGW, EFA

- **VPC Endpoints**: Pods reach AWS services (ECR, S3, KMS, STS) without going to the internet. Required for private clusters.

      - **PrivateLink**: expose your service via an interface VPC endpoint to other accounts. EKS itself uses PrivateLink for the private endpoint.

      - **Transit Gateway**: hub-and-spoke connectivity between many VPCs. Pod traffic between VPCs routes via TGW.

      - **EFA (Elastic Fabric Adapter)**: high-speed network for HPC/AI training. Pods running ML training across multiple nodes use EFA for low-latency, low-jitter all-to-all communication. Requires specific instance types (P4d/P5, etc.) + EFA device plugin.

    
    [ deep dive — skip if new ]EFA + Kubernetes is a niche but high-value combo: distributed PyTorch / NCCL training scales near-linearly to 100s of GPUs over EFA. Without EFA, the network becomes the bottleneck at ~16 GPUs.

## Before / After

**Before.** Default VPC CNI; IP exhaustion at 30 Pods/node. ALBs created by hand via console + DNS records typed into Route 53 by an SRE. Cross-VPC traffic via VPC peering + complex SGs. "Why is the LB stuck pending" answered with shrugs.

**After.** VPC CNI with prefix delegation; 4-5x more Pods per node. AWS LB Controller turns Ingress YAML into ALB. ExternalDNS handles Route 53. Cross-VPC via VPC Lattice + Gateway API. Cluster networking is YAML.

EKS networking is the place new shops trip on AWS-specific gotchas first. Prefix delegation + AWS LB Controller + ExternalDNS are the three you must get right at launch.

## Analogy — the K-Skyline floor

The Communication Tower stands tall above the K-Skyline. The building manager (AWS) operates the central exchange (VPC); the building's wiring (subnets) reaches every floor across three wings (AZs). Each tenant unit (Pod) has its own phone number on the building's public exchange (real VPC IPs via VPC CNI). The doorman (ALB / NLB) routes incoming visitors to the right unit. The address book (ExternalDNS → Route 53) keeps everything findable. And for tenants in different sister buildings (VPCs / accounts), the inter-building shuttle (VPC Lattice) lets them call each other directly.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Building's central exchange | VPC + subnets |
| Each unit's phone number from the building's book | Pod IP from VPC subnet (VPC CNI) |
| Limit on how many phones per floor | ENIs × IPs per instance type |
| Bulk-line phone bundle (more numbers per cable) | Prefix delegation (/28 per ENI) |
| Doorman accepting visitors | ALB / NLB via AWS LB Controller |
| Building address book | Route 53 via ExternalDNS |
| Inter-building shuttle | VPC Lattice + AWS Gateway API Controller |
| Per-unit call screening | SG-for-pods |
| Express line to the data centre across town | EFA for HPC/AI |

⚠️ *Analogy stops here:* The analogy stops here: VPC CNI is software running on each node, hooking into Linux networking namespaces. Real packet flow involves ENI attachments, ip-rule policies, and route table lookups — much more involved than "phone numbers."

## ELI5 / ELI10

**ELI5.** Every Pod gets a real address in the building. The doorman (ALB) sends visitors to the right Pod. The address book (Route 53) keeps everyone's number current.

**ELI10.** AWS VPC CNI gives Pods real VPC IPs (no overlay). Enable prefix delegation = 16x more IPs/ENI. AWS Load Balancer Controller turns Ingress → ALB, Service type=LB → NLB; target type IP for Pod-direct routing. AWS Gateway API Controller implements Gateway API via VPC Lattice for cross-VPC services. ExternalDNS syncs to Route 53. SG-for-pods for per-Pod SGs. Alternatives: Cilium on EKS, Calico, AWS Cilium dataplane.

## Real-world scenarios

- **A SaaS hitting IP exhaustion at scale.** Default VPC CNI; cluster grew from 50 to 500 Pods; nodes saturated at IP limits well before CPU/mem. Fix: enabled prefix delegation cluster-wide, no node replacement needed; per-node Pod density jumped 4x. Saved ~$8K/month on right-sizing nodes.
- **A bank using AWS LB Controller for ALB Ingress.** Single ALB serves 40 hostnames via host-based routing rules; cert-manager populates ACM certs; ExternalDNS creates internal Route 53 records. Adding a new service is a YAML PR. Cost: ~$25/month for the LB; ~$0 for cert + DNS.
- **A multi-account team using VPC Lattice.** 4 AWS accounts, 6 VPCs, dozens of services. Pre-Lattice: cross-account SG sprawl + custom service discovery + VPC peering complexity. Lattice: each service registered once; consumed by HTTPRoute from any account. Cross-account traffic just works.
- **An ML team running PyTorch on EFA.** 32 P5 nodes, EFA enabled, NCCL configured. PyTorch DDP scales 32 GPUs at 92% efficiency; without EFA, was 65%. The EFA setup is non-trivial (instance types + driver + plugin) but pays off massively for distributed training.

## Common misconceptions

- **Myth:** "Default VPC CNI is fine."
  **Truth:** Default = single secondary IPs per ENI = severe Pod density limits on most instance types. Enable prefix delegation on every cluster at launch. Or use Cilium / dual-stack / IPv6.
- **Myth:** "ALB target type instance is the safer default."
  **Truth:** Target type `ip` is the modern default — LB sends directly to Pod IPs (skipping kube-proxy + the per-node hop). Faster, more accurate health checks. `instance` is legacy.
- **Myth:** "VPC Lattice replaces a service mesh."
  **Truth:** Lattice is AWS's opinionated cross-VPC service-to-service. It overlaps with mesh features but doesn't replace mesh entirely (no sidecar mTLS within a single cluster, fewer L7 features). Often paired with Cilium / Linkerd inside the cluster + Lattice across.

## Recap

VPC CNI = real Pod IPs (enable prefix delegation). AWS LB Controller = ALB/NLB from K8s YAML. Gateway API + VPC Lattice = cross-VPC/account services. ExternalDNS for Route 53. SG-for-pods for fine-grained AWS ACLs.

**Next — E4: Identity and Access (EKS-Specific).** IAM access entries, IRSA, Pod Identity. The two-axis identity model (AWS IAM + K8s RBAC).

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
