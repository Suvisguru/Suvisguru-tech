# Lesson 40 — Progressive Delivery · Argo Rollouts and Flagger

> Course: Kubernetes — Common to all distributions
> Module 17 · GitOps · Lesson 3 of 3
> Companion preview: `/preview-kubernetes-lesson-40.html`.

---

**🎯 If you remember nothing else:** **Argo Rollouts** + **Flagger** are the two main K8s progressive-delivery controllers. They replace Deployment with a CRD that knows how to *shift traffic gradually* (10% → 25% → 100%) using a service mesh, Ingress, or Gateway API. They run *automated analysis* (Prometheus metrics, custom queries) at each step; promote on success, abort + rollback on failure. **Argo Rollouts** is K8s-native + integrates with Argo CD; **Flagger** is mesh-native + integrates with Flux + many meshes.

## 1. Beyond rolling updates

Standard K8s rolling update is two-axis: `maxSurge` (extra replicas during rollout) + `maxUnavailable` (allowed-down during rollout). It's a binary deploy: old version replaced by new. No traffic shaping (every Pod gets equal traffic from the Service). No metric-driven validation (deploy proceeds regardless of error rate).
    Progressive delivery splits the deploy into **phases**:
    
      - **Canary** phase 1: 5% of traffic to new version, 95% to old. Wait. Measure.

      - **Canary** phase 2: if metrics look good, ramp to 25%. Wait. Measure.

      - Continue ramping. **Promote** to 100% only after final analysis pass.

      - If any phase's metrics fail, **abort**: drop traffic back to 0%, scale canary down, alert.

    
    This is what actual production teams want — but isn't in core K8s. Argo Rollouts and Flagger fill the gap.

## 2. The K8s-native option

**Argo Rollouts** ships a `Rollout` CRD that replaces `Deployment`. Same shape (PodSpec, replicas, selectors), plus a strategy section:
    `apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: {name: web}
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 5
      - pause: {duration: 5m}
      - setWeight: 25
      - pause: {duration: 5m}
      - setWeight: 50
      - analysis:
          templates:
          - templateName: success-rate
      - setWeight: 100
      trafficRouting:
        nginx:
          stableIngress: web-stable
  template: { ... PodSpec ... }`
    The `analysis` step runs an `AnalysisTemplate` — typically a Prometheus query. "Is the canary's success rate ≥ 99%?" Yes → continue. No → abort + rollback.
    Traffic routing options (depending on your ingress / mesh):
    
      - Ingress NGINX (legacy)

      - Gateway API (modern)

      - Istio, Linkerd, Cilium meshes

      - AWS Load Balancer Controller (TargetGroup weights)

      - Manual replica-count weights (no traffic mesh; less precise)

    
    Argo Rollouts UI shows the Rollout state in real time: which step, what % of traffic, what the analysis is seeing. Plays nicely with Argo CD's Application UI.

## 3. The other major option

**Flagger** is Flux's sister project for progressive delivery. Different model: rather than replacing Deployment, Flagger *watches* a Deployment and orchestrates a parallel canary Deployment + traffic shifts via the service mesh.
    Same canary semantics: weighted traffic, automated analysis, promotion / rollback. Flagger has first-class support for:
    
      - Istio, Linkerd, Cilium, NGINX, Contour, Gloo Edge

      - AWS App Mesh

      - Kuma

    
    Flagger's strength: deeper mesh integration. Linkerd-based progressive delivery often uses Flagger because of the tight Linkerd integration. Argo Rollouts' strength: tight integration with Argo CD's ecosystem.
    Both support similar canary strategies + blue/green + experiments (compare two versions side by side without traffic shift).

## 4. What "good metrics" means in canary

The analysis step is the heart of progressive delivery. Common AnalysisTemplate metrics:
    
      - **Success rate**: `sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))` — must be ≥ 99%.

      - **Latency**: `histogram_quantile(0.99, http_request_duration_seconds_bucket{...}[5m])` — must be ≤ baseline + 10ms.

      - **Error rate**: `sum(rate(http_requests_total{status=~"5.."}[5m]))` — must be ≤ N per minute.

      - **Custom business metrics**: cart_abandonment_rate, signup_completions, etc. — must be in expected range.

    
    Compare canary metrics to *stable* metrics, not absolute thresholds. "Canary success rate is within 1% of stable" is more robust than "canary success rate is > 99%." Real traffic varies; relative metrics catch regressions.
    Failure budgets: define how many failed analyses tolerated before abort. Default 1; higher for noisy services.
    [ deep dive — skip if new ]The most common progressive-delivery mistake: starting too aggressive. Five percent to canary, immediately 100%, no pause. The point of canary is to *see something happen* at 5% before 100%. Industry guidance: minimum 5 minutes per step; more for low-volume services where 5 minutes doesn't give enough samples for stable metrics. Set your AnalysisTemplate's `interval` + `count` based on your real traffic volume.

## Before / After

**Before.** Standard rolling update. Bug ships in v1.3, replicas roll over 5 minutes, customer impact for 5 minutes before someone notices, manual rollback another 5 minutes. Total: 10+ minutes degraded. "How do we ship safely?" answered with feature flags + lots of testing — but production traffic is its own surprise.

**After.** Argo Rollouts canary. Bug ships in v1.3, hits 5% canary first, AnalysisTemplate detects elevated 5xx within 30 seconds, automatic rollback in 10 seconds. Total customer impact: ~30 seconds of degraded performance for 5% of traffic. "How do we ship safely?" answered by the controller.

Progressive delivery is the difference between "hope" and "verified." Once you have it, you don't go back.

## Analogy — the K-Town district

The Print Shop's progressive release floor doesn't print every poster all at once. The first 5% of customers get the new version (canary); the other 95% get the established run (stable). A quality-control inspector watches what comes back: complaints, reprints, returns. If the new version is fine, they ramp to 25%, 50%, then full. If complaints spike, they abort and pull the new version off the press immediately. The inspector's rules are written down explicitly (analysis templates) so the decision is automatic, not based on vibes.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Established run | Stable Deployment / version |
| New canary run | Canary Deployment / Rollout step |
| "5% of customers get the new version" | `setWeight: 5` |
| Quality-control inspector's rules | `AnalysisTemplate` (Prometheus queries) |
| "Inspect for 5 minutes" | `pause: { duration: 5m }` |
| "Promote to full run" | `setWeight: 100` |
| "Abort and revert" | Auto-rollback on AnalysisTemplate failure |

⚠️ *Analogy stops here:* The analogy stops here: real progressive delivery shifts traffic via L7 routing (Ingress / Gateway API / mesh), not by selecting which customers get which version. And canary Pods are real Pods running real code — not a separate run on the same machine.

## ELI5 / ELI10

**ELI5.** Try the new cookies on a small group of testers first. If they like it, give to everyone. If they don't, throw it out.

**ELI10.** Argo Rollouts (CRD-based, K8s-native) and Flagger (mesh-native, Flux companion) replace standard rolling updates with weighted-traffic canary deploys + automated analysis. Define steps (5% → 25% → 50% → 100%) with pause durations. Each pause runs Prometheus queries (AnalysisTemplate) to validate. Promote on success; auto-rollback on failure. Pair with mesh / Ingress / Gateway API for traffic shaping.

## Real-world scenarios

- **A SaaS using Argo Rollouts on every prod service.** Every Deployment migrated to Rollout CRD. Standard canary: 5% → 25% → 50% → 100% with 10-min pauses. AnalysisTemplate checks success rate + P99 latency + custom business metric. ~3 ship-aborts per quarter; without canary they would have been customer-visible. Cumulative incidents avoided: significant.
- **A bank using Flagger with Linkerd mTLS canary.** Linkerd handles mTLS + traffic shifting. Flagger configures TrafficSplit. Per-service AnalysisTemplate based on golden signals. Compliance team appreciates: every release is a controlled experiment, every rollback is a documented event.
- **A startup using Argo Rollouts blue/green.** Not all services need canary; some prefer blue/green for atomic switches. Rollout supports blue/green strategy: deploy new version, run smoke tests, flip Service selector. Same CRD, different strategy. Used for stateful services where partial traffic split is awkward.
- **A team that learned analysis matters.** Initially had Argo Rollouts with no AnalysisTemplate — just timed canary. A regression slipped through anyway. Added AnalysisTemplate with success-rate + latency. Two months later, AnalysisTemplate caught a regression that timed-only would have promoted. Lesson: pause + analysis, not just pause.

## Common misconceptions

- **Myth:** Progressive delivery is only for huge services.
  **Truth:** It's for any service where regressions are expensive. A small auth service that breaks logins is more impactful than a big background job. Risk = probability × impact; not always proportional to size.
- **Myth:** Canary requires a service mesh.
  **Truth:** Service mesh gives precise weighted traffic shaping. Without one, you can do *replica-based* weights — 1 canary Pod alongside 19 stable = ~5% traffic. Less precise but works. Most ingresses (Ingress NGINX, Gateway API controllers) support weighted backends natively.
- **Myth:** If canary metrics are flat, the deploy is fine.
  **Truth:** Flat success rate doesn't mean no regression. Latency spike, queue backup, downstream pressure can all be regressions. Multi-metric analysis (success + latency + custom signals) catches more.

## Recap

Argo Rollouts and Flagger turn Deployments into phased releases with automated analysis. Define canary steps + AnalysisTemplate; promote on success, abort on failure. Cost: minutes of extra deploy time. Benefit: regressions caught at 5% traffic, not after they've hit 100%.

**Next — Lesson 41: CRDs Deep Dive.** Module 18 begins. The K8s extension story — schemas with CEL validation, conversion webhooks, the full custom-resource lifecycle. Permit Office, advanced wing.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
