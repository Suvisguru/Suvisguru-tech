# K-ADV-NET N6 — N6 · Packet Tracing + Performance Tuning

> Course: K-ADV-NET (advanced specialization)
> Module N6 · Packet Tracing + Perf
> Companion preview: `/preview-kubernetes-adv-net-lesson-06.html`.

---

**🎯 If you remember nothing else:** **Hubble for L4+L7 flows; Pixie / Tetragon for in-app calls without instrumentation; tcpdump for kernel-level when nothing else helps; kube-burner for proactive perf testing. Wire them all in dev so muscle memory exists during incidents.**

## 1. L4 + L7 verdicts without packet capture

**Hubble** (Cilium's observability layer) shows per-flow events: source / destination Pod, IP, port, verdict (Allowed / Dropped + reason — NetPol rule, RST, etc.), L7 metadata (HTTP method + path + status, DNS name + result, Kafka topic).
    Hubble UI / CLI / Grafana: "show all denied flows from namespace X past 5 min" — answer in seconds. Compare to without: tcpdump on every node + manually correlate.
    Hubble flow logs power: NetworkPolicy debugging ("why is this dropped?"), security forensics ("who connected to crypto-pool IPs?"), latency analysis ("P99 of HTTP / on this Service").

## 2. L7 + syscall trace with no app changes

**Pixie** (CNCF, NewRelic-acquired): eBPF probes for HTTP / gRPC / MySQL / Postgres / Redis / DNS — captures requests + responses (with redaction); script-able with PxL queries. Per-Service traffic + per-endpoint latency without OTel SDKs.
    **Tetragon** (Cilium): syscall-level + process-level trace + enforcement. Sees fork / exec / open / connect; emits events to SIEM; can also block at runtime.
    Both use eBPF; both bypass app instrumentation. Pixie shines on "what is this Service actually doing?"; Tetragon on security + runtime behavior.

## 3. When you need to see the actual packets

When higher-level tools don't answer:
    
      - **tcpdump** on a node: `kubectl debug node/X -- tcpdump -i any -nn -e`. Captures raw frames; great for MTU + checksum + encap problems.

      - **kubectl-trace**: bpftrace-style scripts run cluster-wide. `kubectl trace run node/X -e "..."` for kernel-level tracing.

      - **kubeshark**: cluster-wide sniffer with per-Pod filters; UI shows L7 streams (HTTP / gRPC / Kafka). Lower-overhead than tcpdump for ongoing inspection.

      - **retina** (Microsoft): cluster-wide network observability with eBPF + Prometheus metrics.

    
    Use these when: encap path debugging, MTU mismatch suspicion, kernel-level perf, custom protocol troubleshooting.

## 4. proactive testing + tuning playbook

**kube-burner**: synthetic load generator. Spin up N Pods + N Services + N CRDs + measure cluster behavior under load. Foundation of perf-test-as-code; CI gates on cluster-perf regressions.
    **Common findings + fixes**:
    
      - **MTU mismatch**: encap pushes packet over host MTU; large requests fragment / drop. *Set Pod MTU = host MTU − encap overhead*.

      - **conntrack saturation**: high CPS overflows nf_conntrack_max. *Tune nf_conntrack_max + hashsize; use eBPF to bypass conntrack*.

      - **CoreDNS bottleneck**: 80%+ CPU at scale. *NodeLocal DNSCache + ndots:1* (covered N4).

      - **Noisy neighbour**: shared host CPU / network. *QoS class Guaranteed + node anti-affinity*.

      - **Kernel scheduling**: high context-switch on overloaded nodes. *Right-size; use cpu-manager-policy=static for latency-sensitive*.

      - **Encap overhead**: 15-25% CPU on VXLAN/Geneve. *BGP native routing where fabric supports*.

## Before / After

**Before.** Pre-eBPF tracing, network debugging was tcpdump + manual correlation + intuition. Hours per incident. App-internal calls invisible without instrumentation.

**After.** Hubble + Pixie + Tetragon give per-flow + per-syscall + per-app-call visibility via eBPF; tcpdump + kubectl-trace are last-resort. kube-burner verifies perf in CI; common findings have known tunings.

*See the network. Don't guess. Profile in dev so muscle memory exists during incidents.*

## Analogy — the K-Highway junction

The Traffic Helicopter circles K-Highway 24/7. Four cameras + sensors give different views. **Wide-angle camera** (Hubble) sees every vehicle route — license + destination + verdict (allowed / blocked). **In-vehicle dashcam** (Pixie + Tetragon) sees what each driver was doing — calls made, syscalls executed. **Per-lane probe** (tcpdump / kubectl-trace) drops a sensor in one lane for kernel-level depth. **Stress-test convoy** (kube-burner) drives synthetic load + measures.
    The Captain reads the four together. Most issues surface in the wide-angle; some need dashcam; rare ones need probes; perf changes get convoy-tested.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Wide-angle camera | Hubble (Cilium eBPF flow log) |
| In-vehicle dashcam | Pixie + Tetragon (eBPF syscall + L7) |
| Per-lane probe | tcpdump / kubectl-trace / kubeshark / retina |
| Stress-test convoy | kube-burner (synthetic load) |
| Wrong-tire-pressure (MTU mismatch) | Pod MTU != host MTU − encap overhead |
| Toll booth overflow | conntrack saturation |
| Tunnel CPU tax | VXLAN / Geneve encap overhead |
| Single-driver lane delay | Noisy neighbour / shared CPU |

⚠️ *Analogy stops here:* A real helicopter sees vehicles physically; cluster traffic is bytes + policy. Tracing tools have observability cost — sample at scale; deploy fully in dev.

## ELI5 / ELI10

**ELI5.** Four kinds of camera over the highway. Wide angle for routes. Dashcam for what drivers do. Per-lane probe for kernel-level depth. Stress-test convoy for proactive testing. Read all four when the highway slows.

**ELI10.** **Hubble**: eBPF flow logs (L4+L7 verdicts). **Pixie**: eBPF L7 trace (HTTP/gRPC/MySQL/Postgres/Redis/DNS) without app changes. **Tetragon**: syscall + process trace + enforcement. **tcpdump / kubectl-trace / kubeshark / retina**: low-level packet + kernel tracing. **kube-burner**: synthetic load + cluster perf. **Common fixes**: MTU = host − encap; conntrack tuning; NodeLocal DNS; QoS Guaranteed; cpu-manager-policy.

## Real-world scenarios

- **Hubble caught a drop nobody had seen.** A team's API was occasionally returning 502s; app logs blank. Hubble flow log: drop on egress to backend; reason = NetworkPolicy. Bad NP rule was added by mistake; reverted; problem cleared in 5 minutes.
- **Pixie revealed slow downstream call.** P99 latency drift over weeks. Pixie L7 trace per Service showed HTTP P99 to one upstream API growing — that upstream service was slow; team alerted upstream owner; tail latency clipped.
- **MTU mismatch found via tcpdump.** Large requests silently dropped. tcpdump on host showed fragmentation + ICMP "Frag needed" being filtered. Pod MTU set to 1500 but host VXLAN-tunnel MTU was 1400. Set Pod MTU 1400; problem cleared.
- **kube-burner CI gate caught conntrack regression.** kube-burner CI test showed P99 latency rising 2× after a CNI version bump. Profile: conntrack table near limit. Tuning + version pinning kept change reversible. Caught before prod.

## Common misconceptions

- **Myth:** "tcpdump is the right first tool."
  **Truth:** tcpdump is high-overhead + low-context. Hubble + Pixie + Tetragon read kernel-level eBPF events with structure + verdicts. Use tcpdump only when higher-level tools can't see what you need (raw bytes, kernel encap).
- **Myth:** "Pixie requires changing the app."
  **Truth:** Pixie's eBPF probes attach at kernel level + decode L7 protocols (HTTP / gRPC / MySQL / Postgres / Redis / DNS) without any app changes. Add the Pixie agent; it sees existing traffic.
- **Myth:** "kube-burner is for cluster admins only."
  **Truth:** App teams can use it for capacity-test-as-code: "my Service can sustain 1000 rps with N replicas". Run in CI before deployment; perf regressions caught at PR time.

## Recap

Hubble for flows; Pixie + Tetragon for in-app L7 + syscalls; tcpdump / kubectl-trace last-resort; kube-burner for proactive perf testing. Common fixes: MTU, conntrack, DNS scaling, QoS, cpu-manager-policy.

**Next — N7: Capstone — multi-cluster network across EKS + AKS + GKE + on-prem.** Bridge selection per region; AdminNetworkPolicy fleet-wide; Hubble across clusters; runbook.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
