# Lesson 44 — Troubleshooting Methodology + Drills (Capstone)

> Course: Kubernetes — Common to all distributions
> Module 19 · Capstone · Lesson 1 of 1
> Companion preview: `/preview-kubernetes-lesson-44.html`.

---

**🎯 If you remember nothing else:** Four-step triage: **(1) Reproduce** the issue. **(2) Observe + measure** with logs / events / metrics / traces. **(3) Hypothesise** a cause. **(4) Test + verify** the fix. The K8s evidence kit: `kubectl describe` (events!), `kubectl get events`, `kubectl logs --previous`, `kubectl debug`, `kubectl top`, the observability stack from L32-L33. Common failure patterns cluster around: image pulls, resource limits, storage, networking, admission policy, certificates.

## 1. Methodology before tooling

The fundamental troubleshooting flow:
    
      - **Reproduce.** Can you trigger the issue at will? If yes, debugging is bounded. If no, you're in "flaky" territory — gather more telemetry, wait for next occurrence.

      - **Observe + measure.** Don't guess. Use `kubectl describe`, `get events`, logs, metrics, traces. Note timestamps. Look for patterns: which Pods, which times, which traffic, which dependencies.

      - **Hypothesise.** Form a specific theory. "The ConfigMap content changed at 14:32; that's when error rate jumped." Hypotheses are testable.

      - **Test + verify.** Make a change. See if the issue resolves. If yes, you've confirmed the cause. If no, hypothesis is wrong; back to step 2.

    
    The most common anti-pattern: skipping straight from "problem reported" to "let me try a fix." This is debugging by random walk — sometimes you stumble onto the answer; usually you make things worse. Discipline beats brilliance under pressure.

## 2. What kubectl gives you for free

- **`kubectl describe pod <pod>`** — the most useful command. Shows events at the bottom: image pull errors, scheduling failures, probe failures, OOM kills. Almost every "why won't my Pod start" question is answered here.

      - **`kubectl get events --sort-by=.metadata.creationTimestamp`** — namespace-wide events. Catches things `describe` on one Pod misses.

      - **`kubectl logs <pod> --previous`** — logs from the previous container instance. Crucial after a crash; the current logs are post-restart and tell you nothing.

      - **`kubectl top pod / node`** — current CPU / memory. Pair with metrics-server.

      - **`kubectl debug`** — modern way to add an ephemeral debug container into an existing Pod or copy a Pod with a different image (e.g., debug a distroless container by adding a `busybox` ephemeral container).

      - **`kubectl auth can-i --as=<sa> <verb> <resource>`** — RBAC inspection. "Can this SA do X?" answered without trial and error.

      - **`kubectl explain <resource>.<field>`** — field-level documentation from the running cluster's API. Always reflects the cluster version, not the docs.

    
    Beyond kubectl: the observability stack (L32-L33) — Prometheus / Grafana for metrics, Loki / Elastic for logs, Tempo / Jaeger for traces. Hubble + Pixie for network and kernel-level signals. The right tool depends on which layer you're investigating.

## 3. Common failure patterns from L1-L43

A quick tour of the failure patterns you've learned about across the curriculum:
    
      - **Image pull failures** — `ImagePullBackOff`. Causes: typo in image name, missing imagePullSecret, registry unreachable, signed-image policy rejecting unsigned images. *Lesson 11 + 30.*

      - **Resource starvation** — Pods OOMKilled, evicted. Causes: missing requests/limits, ResourceQuota exceeded, LimitRange violation. *Lesson 31 + 22.*

      - **Storage** — PVC stuck Pending, Pod can't mount. Causes: zone mismatch (Immediate binding mode vs multi-zone scheduler), CSI driver missing capability, storage class typo. *Lessons 18-19.*

      - **Networking** — Service unreachable, cross-zone slow. Causes: NetworkPolicy denying, kube-proxy stale, CNI MTU mismatch, DNS resolver pointing wrong. *Lessons 17 + 24-26.*

      - **Admission rejection** — apply fails with a policy error. Causes: PSA mismatch, ValidatingAdmissionPolicy violation, Kyverno rule. *Lessons 27-29.*

      - **Certificates** — TLS errors, mTLS handshake failure. Causes: cert expired (cert-manager not renewing), wrong CA, time skew. *Lessons 21 + 43.*

      - **Scheduling** — Pod stays Pending. Causes: no node fits, taints not tolerated, affinity unsatisfiable, topology spread blocked. *Lessons 22-23.*

      - **Operator / controller errors** — CR stays in OutOfSync / Pending. Causes: missing RBAC, finalizer stuck, conversion webhook down, dependency CRD not yet applied. *Lessons 38-42.*

    
    For each pattern, the diagnostic is similar: read the events, check the most recent change, follow the dependency chain, narrow to the failing component. *Most production incidents are not novel — they're known patterns hitting your specific cluster.*

## 4. The discipline that produces calm engineers

Three practices distinguish teams that survive incidents:
    
      - **Game days.** Quarterly chaos engineering: kill a zone, kill 50% of Pods, simulate a CSI driver hang. The team practises the response. Tools: Chaos Mesh, LitmusChaos. *Lesson 35.*

      - **Runbooks per alert.** Every paging alert has an annotation linking to a markdown runbook: "if this fires, run these queries, look for these patterns, escalate at this signal." Runbooks evolve from post-mortems. *Lesson 32.*

      - **Blameless post-mortems.** After every incident: timeline, contributing factors, what worked, what didn't, action items. No individual blame; system-level fixes. The discipline is reading them as a team.

    
    The single biggest determinant of MTTR isn't individual skill — it's organisational practice. Teams that drill, write runbooks, and learn from incidents have low MTTR. Teams that don't, don't.
    [ deep dive — skip if new ]The hardest lesson is restraint. When something's broken at 3 AM, the temptation is to fix it now. The right move is often: **narrow the impact, gather evidence, get the right person on the call, then fix**. Random changes during incidents create new problems and erase evidence. Best practice: capture state (`kubectl get all -A -o yaml`, descriptions, logs) before any mutation. You can't debug what you can't reproduce.

## Before / After

**Before.** Before discipline: 3 AM page. Engineer panic-edits resources hoping to fix. Sometimes works; usually makes things worse. No clear timeline. Post-mortem becomes "who did what when?" finger-pointing. Same incidents recur monthly because nobody learned.

**After.** After discipline: 3 AM page. Engineer follows the runbook. Captures state. Walks the triage. Identifies cause within minutes. Fixes precisely. Post-mortem is structured + blameless. Same incident never recurs — the runbook + alert tuning + system fix prevent it.

After 43 lessons of how K8s works, this lesson is the most important: how to think when it doesn't.

## Analogy — the K-Town district

The Detective's Office is the last district on the K-Town map — the one that handles every other district's problems. Every wall has a corkboard with a flowchart: *reproduce → observe → hypothesise → test → verify*. Detectives carry an evidence kit (kubectl, observability tools, fingerprint reagents) and a list of usual suspects (image pulls, RBAC, MTU, certs, admission). They don't panic. They don't guess. They follow the procedure, document their findings, write up the case for the next detective. After every case: a debriefing where everyone learns. The Office's reputation isn't built on solving novel mysteries — it's built on solving routine ones *fast*, calmly, with evidence.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| The corkboard flowchart | Triage methodology |
| Evidence kit | `kubectl describe`, events, logs, top, debug |
| Usual suspects | Common failure patterns (image, resource, storage, network, admission, cert) |
| Detective's drill | Chaos engineering / game day |
| Case file template | Runbook |
| Post-case debrief | Blameless post-mortem |
| "Don't touch the crime scene" | Capture state before mutating during an incident |
| "Look for the pattern, not just this case" | Pattern-recognising recurring failure modes |

⚠️ *Analogy stops here:* The analogy stops here: real K8s incidents don't involve fingerprints — they involve correlated logs across distributed systems, with timestamps that may or may not be synced. The detective abstraction undersells the digital nature of the work.

## ELI5 / ELI10

**ELI5.** When something's broken, don't panic. Look at the clues (events, logs). Guess what might be wrong. Test the guess. If it's right, fix it. If not, look more carefully.

**ELI10.** Troubleshooting K8s is methodology before tooling. Four steps: reproduce, observe + measure, hypothesise, test + verify. The kubectl evidence kit (describe, events, logs --previous, top, debug, auth can-i) handles 80% of cases. Common failure patterns recur: image pulls, resource limits, storage zone mismatch, NetworkPolicy denial, admission rejection, expired certs. Run game days quarterly; pair every alert with a runbook; do blameless post-mortems. The discipline beats individual brilliance.

## Real-world scenarios

- **A SaaS that drilled the right things.** Quarterly game days for 18 months. Each game day produced 3-4 runbook updates + 1-2 system improvements (alert tuning, redundancy, SLO refinement). MTTR for production incidents dropped from 90 minutes (year 1) to 12 minutes (year 2). The drill discipline did it.
- **A bank with comprehensive runbook coverage.** Every alert has a runbook. Every runbook has been validated by an on-call engineer in the last quarter. Engineers rotate through on-call; new engineers ramp up by reading the runbook library. Net effect: anyone in the team can handle 90% of alerts in their first month.
- **A startup that learned mid-incident triage.** Their first major incident: 4 hours of chaotic firefighting. Their second (a year later, after instituting drills + runbooks): 15 minutes from page to mitigation. Same kind of issue. The difference was process, not knowledge.
- **A team that captured state pre-mutation.** Convention: any incident response action that would change state is preceded by `kubectl get all -A -o yaml > incident-pre.yaml`. After the incident, post-mortem can compare pre/post. Caught a self-inflicted mistake (wrong namespace edit) within minutes. Saved hours of confusion.

## Common misconceptions

- **Myth:** Senior engineers don't need runbooks.
  **Truth:** Senior engineers *write* the runbooks so junior engineers can act with confidence. Senior engineers also forget specifics under stress; runbooks are insurance for everyone.
- **Myth:** Faster fixes are better.
  **Truth:** Faster *verified* fixes are better. A fast wrong fix creates a second incident on top of the first. Slow down to read events; the speed-up comes from acting on real evidence.
- **Myth:** The most critical kubectl command is `kubectl edit`.
  **Truth:** The most critical command is `kubectl describe`. Read events first, edit later — and prefer applying YAML changes via PR after the incident, not `kubectl edit` live.

## Recap

Methodology before tooling. Reproduce → observe → hypothesise → test → verify. The kubectl evidence kit + observability stack handles most cases. Common failure patterns recur — pattern-recognition + runbooks accelerate response. The discipline (game days, blameless post-mortems) makes the difference.

**That's the full K-COM curriculum.** 44 lessons + the L7.5 primer. From "what is Kubernetes?" to "how to debug it under fire." Every K-Town district mapped, every primitive covered. The detective's office closes the loop — when you know how the system works, you know how to fix it when it doesn't. **The course is complete.**

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
