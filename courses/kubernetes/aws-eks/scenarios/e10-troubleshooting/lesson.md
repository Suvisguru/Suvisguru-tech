# K-EKS E10 — E10 · EKS Troubleshooting (AWS-Specific)

> Course: Amazon EKS (K-EKS, prereq: K-COM + AWS basics)
> Module E10 · EKS Troubleshooting
> Companion preview: `/preview-kubernetes-eks-lesson-10.html`.

---

**🎯 If you remember nothing else:** EKS-specific failure modes need EKS-specific debugging. Top eight: **(1) IAM/RBAC unauth** (access entries vs aws-auth precedence); **(2) node NotReady / NG launch fail** (IAM, AMI, subnet capacity); **(3) VPC CNI IP exhaustion** (enable prefix delegation); **(4) LB pending** (subnet tags, IAM); **(5) EBS multi-AZ attach** (WaitForFirstConsumer); **(6) IRSA / Pod Identity** (trust policy, OIDC, association); **(7) Karpenter / Auto Mode stuck** (instance availability, IAM, NodeClass); **(8) API throttling** (CloudWatch + CloudTrail RCA, request limits). **CloudTrail + CloudWatch + Container Insights** are the diagnostic surfaces.

## 1. Why EKS-specific troubleshooting deserves its own module

Vanilla K8s troubleshooting (K-VAN V10) covers the cluster-internal failures: cert expiry, broken CNI, broken CoreDNS, etc. EKS adds a layer of *AWS-specific* failures that don't exist on vanilla:
    
      - IAM / RBAC mismatch (because EKS bridges two identity systems).

      - VPC CNI IP exhaustion (because Pods consume real VPC IPs).

      - LB provisioning failures (because AWS LB Controller talks to ELB API).

      - EBS multi-AZ attach (because EBS is single-AZ).

      - IRSA / Pod Identity broken (because Pod-to-AWS auth has its own machinery).

      - Karpenter / Auto Mode quirks (because they call EC2 / spot APIs).

      - API throttling (because AWS rate-limits everything).

    
    Diagnosis follows a similar methodology (V44 in K-COM): reproduce → observe → hypothesise → test. The *tools* are AWS-specific: CloudTrail, CloudWatch, Container Insights, ALB access logs, EC2 Console.

## 2. The recurring incidents

**1. IAM / RBAC unauth**: "You must be logged in to the server (Unauthorized)." Common cause: no access entry / aws-auth mapping. Diagnose: `aws eks list-access-entries --cluster-name X`; `kubectl auth can-i --as=user`. Fix: add access entry. *Migrate to access entries; aws-auth lockouts are still recoverable via cluster-creator IAM principal.*
    **2. Node NotReady / Managed NG launch failure**: NG creation hangs; nodes don't register. Common causes: (a) IAM role missing required policies (AmazonEKSWorkerNodePolicy, AmazonEC2ContainerRegistryReadOnly, AmazonEKS_CNI_Policy); (b) subnet IP exhaustion; (c) wrong AMI for the K8s version; (d) launch template SG blocks 443 to control plane. Diagnose: NG events in EKS Console; CloudTrail for the EC2 RunInstances call.
    **3. VPC CNI IP exhaustion**: "0/N nodes available: N had no Pod IPs available." Fix: enable prefix delegation. `kubectl set env -n kube-system ds/aws-node ENABLE_PREFIX_DELEGATION=true`; restart aws-node; new Pods provision IPs.
    **4. LoadBalancer / ALB pending**: Service stuck without an external IP, or Ingress without an ALB. Common causes: subnets missing required tags (`kubernetes.io/role/elb` for internet, `internal-elb` for internal); IAM permissions on the LB controller; wrong target type. Diagnose: `kubectl describe svc / ingress` for events; `kubectl logs -n kube-system deploy/aws-load-balancer-controller`.

## 3. The other four

**5. EBS multi-AZ attach failure**: "FailedAttachVolume — volume is in different AZ." Cause: Pod scheduled in AZ that doesn't have the volume. Fix: StorageClass `volumeBindingMode: WaitForFirstConsumer`; recreate PVC. *Always WaitForFirstConsumer on multi-AZ EBS.*
    **6. IRSA / Pod Identity broken**: AWS SDK calls return AccessDenied or NoCredentialsProvider. Diagnose IRSA: (a) OIDC provider exists in IAM (`aws iam list-open-id-connect-providers`); (b) trust policy on the role allows the cluster's OIDC + the SA path; (c) SA annotated with role ARN; (d) Pod's projected JWT contains correct audience. Diagnose Pod Identity: (a) Pod Identity Agent installed (managed add-on); (b) association exists for the (cluster, namespace, SA); (c) IAM role trust policy allows `pods.eks.amazonaws.com`; (d) Pod restarted after association.
    **7. Karpenter / Auto Mode stuck**: Pending Pods not getting nodes. Common causes: (a) NodePool requirements too restrictive (no instance type can satisfy); (b) IAM role lacks `ec2:RunInstances`; (c) NodeClass subnet/SG selectors match nothing; (d) instance type unavailable in target AZ; (e) spot interruption rate exceeds NodePool limits. Diagnose: `kubectl get nodeclaims -A`; `kubectl logs -n karpenter deploy/karpenter`; CloudTrail for failed RunInstances calls.
    **8. API throttling**: AWS API calls fail with `Throttling: Rate exceeded`. Cause: too many EC2 / EKS / IAM calls in a short window (often Karpenter scaling fast or controllers polling aggressively). Mitigate: tune controller poll intervals, request quota increase, batch requests, exponential backoff (most controllers do this automatically).

## 4. CloudTrail, CloudWatch, kubectl

- **CloudTrail**: every AWS API call (EC2, EKS, IAM, KMS, ELB) — the source of truth for "what AWS API was called when by whom." Searchable via Athena. Default 90-day retention; configure trails for longer.

      - **CloudWatch Logs**: control-plane logs (E8) + container logs (Fluent Bit) + ALB access logs + Karpenter logs.

      - **CloudWatch Container Insights**: cluster-wide metrics + per-Pod resource trends.

      - **kubectl describe**: events on resources are still the first stop. Most EKS-specific failures show useful events here.

      - **EKS Console**: cluster + nodegroup + add-on status; node group launch failures shown here.

      - **EC2 Console**: instance state, system log, instance status checks. For NotReady nodes: check the EC2 instance for hardware / OS issues.

      - **VPC Reachability Analyzer**: simulates network paths. Useful for "why can't Pod reach RDS" problems.

    
    [ deep dive — skip if new ]For very subtle issues: AWS Support case + screen-share with TAM. EKS standard support tier is included; enterprise support is faster + has solution architects available.

## Before / After

**Before.** Outages diagnosed by SSH-then-guess. No CloudTrail integration with on-call. Same incidents recur because runbooks aren't written. Six EKS-specific patterns each take 2 hours to diagnose first time + 30 min next time.

**After.** Eight runbooks per EKS-specific failure. CloudTrail integrated with PagerDuty / Slack on suspicious patterns. Quarterly chaos drills covering each scenario. New on-call recovers most incidents in < 30 min using the runbook.

EKS-specific incidents recur. Drilled team + runbook library makes them routine; un-drilled team makes them emergencies.

## Analogy — the K-Skyline floor

The Emergency Plaza is the K-Skyline's practice ground for unusual incidents. Pinned on the wall: eight scenario cards, each with a runbook. The dispatcher (CloudTrail) records every API call to the building. The control room (CloudWatch + Container Insights) shows live metrics. New on-call walks the plaza, takes a card, runs the drill blind, debriefs. Goal: every responder has handled every scenario at least once before the real call comes.

**Translation legend.**

| In the story… | …in EKS / AWS |
|---|---|
| Practice ground for unusual incidents | EKS-specific failure drills |
| Eight scenario cards on the wall | Eight failure patterns + runbooks |
| Building API call recorder | CloudTrail |
| Live metrics control room | CloudWatch + Container Insights |
| On-call walks the drill blind | Chaos drills (similar to K-VAN V10) |
| Debrief after each scenario | Runbook updates from drill findings |
| Specialist tools at the desk | EKS Console, EC2 Console, VPC Reachability Analyzer |

⚠️ *Analogy stops here:* The analogy stops here: real EKS incidents are diagnosed via API calls, log queries, eBPF traces, AWS Support tickets — not paper cards on a plaza wall.

## ELI5 / ELI10

**ELI5.** Eight kinds of fire drill specific to the AWS tower. Practice each one before the real fire so it's muscle memory.

**ELI10.** Eight EKS-specific failure patterns: IAM/RBAC unauth, node NotReady / NG launch, VPC CNI IP exhaustion, LB pending, EBS multi-AZ, IRSA / Pod Identity, Karpenter / Auto Mode stuck, API throttling. Diagnostic tools: CloudTrail (every API call), CloudWatch Container Insights, kubectl describe (still useful), EKS / EC2 Console, VPC Reachability Analyzer. Build runbooks; drill quarterly.

## Real-world scenarios

- **A SaaS with quarterly EKS chaos days.** Practice each of the eight scenarios on a non-prod cluster. Score: time-to-mitigation. Track over 6 quarters: from 90 min average → 22 min average. Five new runbook updates from drill findings.
- **A bank that automated IRSA migration.** Old IRSA roles still in use; pre-migration audit found 47 unique trust policies, several with subtle SA path bugs. Migration to Pod Identity removed all 47 trust-policy YAMLs; replaced with associations. Cleaner; auditable; tested.
- **A team hit by Karpenter API throttling.** Cluster scaled 50 → 500 nodes during a marketing event. Karpenter exhausted EC2 RunInstances quota; Pods Pending for 10 min; some workloads couldn't start. Mitigation: requested quota increase + tuned Karpenter to batch RunInstances calls. Lesson: pre-emptive quota increases for events you know about.
- **A team using VPC Reachability Analyzer.** Pod can't reach RDS. Old debugging: SSH everywhere, tcpdump, etc. New: VPC Reachability Analyzer simulates the path; immediately shows the SG rule blocking traffic. RCA in 5 minutes vs hours.

## Common misconceptions

- **Myth:** "AWS Support is faster than my own runbook."
  **Truth:** AWS Support is great for genuinely novel issues + AWS-side bugs. For recurring patterns: your runbook is faster + builds team skills. Use Support for the 5%; runbooks for the 95%.
- **Myth:** "CloudTrail is too noisy for incident response."
  **Truth:** Default CloudTrail across many AWS APIs IS noisy. Filter aggressively: Athena queries by time + service + IAM principal. Or: ship to a SIEM with smart parsing. Don't skip it; just operate it.
- **Myth:** "Karpenter / Auto Mode rarely fails."
  **Truth:** They're reliable for steady state but have specific failure modes (NodeClass mis-config, instance unavailability, IAM gaps). Build runbooks for these; they happen.

## Recap

Eight EKS-specific failure patterns. Diagnostic surfaces: CloudTrail, CloudWatch Container Insights, kubectl describe, EKS / EC2 Console, VPC Reachability Analyzer. Build runbooks per pattern; drill quarterly.

**Next — E11: K-EKS Capstone.** Multi-AZ EKS Auto Mode cluster with everything wired together: Karpenter, AWS LB Controller, Pod Identity, KMS, Gateway API via VPC Lattice, AMP + AMG, Argo CD GitOps, blue-green upgrade runbook, DR plan.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
