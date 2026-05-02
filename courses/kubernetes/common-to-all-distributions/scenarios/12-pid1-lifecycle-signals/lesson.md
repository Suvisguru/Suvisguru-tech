# Lesson 12 — PID 1 · Signals · Graceful Shutdown · Init Wrappers

> Course: Kubernetes — Common to all distributions
> Lesson 12 of 17 in K-COM. Module 2 · Lesson 5 of 5 (final container lesson).
> Companion preview: `/preview-kubernetes-lesson-12.html`.

---

## 1. Concept

When a pod terminates, the kubelet doesn't just yank the plug. It runs
a four-step shutdown protocol that depends on **whoever is running as
process 1 inside your container** doing the right thing. Most "my pod
takes 30 seconds to die" mysteries trace back to PID 1.

**Why PID 1 is special.** Linux gives PID 1 (the first process started
in a namespace) two responsibilities the kernel won't take care of for
anyone else: (1) **forward signals** to its descendants when it gets
them, and (2) **reap zombies** — call `waitpid()` on every child that
exits, so the kernel can free the process table entry. On a normal Linux
host, systemd does this. Inside a container, your ENTRYPOINT process is
PID 1 — and most apps don't know they're supposed to do those jobs.

**Signals K8s sends.** When a pod is deleted, the kubelet sends
**SIGTERM** to the container's PID 1. That's the polite "please wrap
up." If PID 1 doesn't exit within `terminationGracePeriodSeconds`
(default: 30s), the kubelet sends **SIGKILL** — the kernel-level "die
now," which can't be caught or ignored. SIGINT (Ctrl-C) is what your
shell sends locally; K8s does not use it.

**Graceful shutdown.** A well-behaved app catches SIGTERM, stops
accepting new work, finishes in-flight requests, flushes buffers,
closes connections, and exits 0. The kubelet waits up to the grace
period for this. The pod's status moves through `Running → Terminating
→ Terminated`.

**Zombies and orphans.** When a child process exits, it becomes a
*zombie* until its parent calls `waitpid()`. If the parent never does,
zombies accumulate until the process table fills up. If the parent dies
first, children get re-parented to PID 1 (orphans) — and PID 1 is
expected to reap them when they exit. A naive app as PID 1 doesn't, and
zombies pile up until the container OOMs or hits ulimits.

**Init wrappers.** **tini** and **dumb-init** are tiny binaries that
solve both problems. You set `ENTRYPOINT ["tini", "--", "your-app"]` in
the Dockerfile. tini becomes PID 1, your app is PID 2. tini forwards
every signal it gets to PID 2 and reaps any zombies that get
re-parented to it. Buys you graceful shutdown and zombie safety in one
line.

**preStop hook.** A pod-level escape hatch. When the kubelet decides
to terminate a pod, it runs `preStop` *before* sending SIGTERM. Common
use: `sleep 10` to let the load-balancer notice the pod is being
removed before it stops accepting connections. Critical for
zero-downtime rolling updates.

---

## 2. Before / After

**Before — naive container, no init.** Dockerfile:
`CMD ["bash", "/app/start.sh"]`. The bash script starts your Node app
in the background. SIGTERM arrives → bash receives it but doesn't
forward to Node → Node never gets the signal → 30 seconds elapse →
SIGKILL → Node dies mid-request, in-flight requests drop, no flush.
Logs show "Killed". Operators wonder why every deploy is "lossy."

**After — tini ENTRYPOINT, preStop drain.** Dockerfile:
`ENTRYPOINT ["/usr/bin/tini", "--"]` then `CMD ["node", "server.js"]`.
Pod spec adds `lifecycle.preStop.exec.command: ["sh", "-c", "sleep 5"]`
(let the LB drain) and `terminationGracePeriodSeconds: 60` (extra
runway). On SIGTERM: preStop runs, then tini forwards SIGTERM to Node,
Node gracefully closes Express server (drains in-flight requests),
exits 0. Pod cleanly terminates, zero requests dropped.

What didn't change: app code (well, Node already handles SIGTERM if
you wired it). What changed: PID 1 actually delivers the signal.

---

## 3. Analogy — the ship's captain

A container shutdown is a ship docking and disembarking. The **captain
is PID 1**. The crew (child processes) are at their stations: engine
room, cargo hold, navigation. Out at sea, the **lighthouse flashes a
signal** — that's SIGTERM from the kubelet — meaning "wrap up and head
to port."

A good captain hears the signal, picks up the megaphone, and **forwards
the order** to every crew member: "stop loading, wrap up the manifest,
prepare to disembark." A bad captain hears the lighthouse and just
stands there. The crew never gets the message and keeps loading cargo.

The captain also keeps a **roster log** — every crew member who
disembarks gets ticked off (zombie reaping). Crew members whose original
supervisor has already left get re-assigned to the captain (orphans),
and the captain ticks them off when they leave too.

After the lighthouse signals, the harbour gives the ship a **grace
period** (`terminationGracePeriodSeconds`, default 30s) to disembark
peacefully. If the ship is still moored after grace, the harbour pulls
the gangway and lights out (SIGKILL — can't be ignored). A captain
who doesn't act in time loses crew mid-disembarkation.

**The mapping:**

- Captain on the bridge = PID 1
- Crew at stations = child processes
- Lighthouse signal = SIGTERM from kubelet
- Captain's megaphone (forwarding) = signal propagation by PID 1
- Roster log (ticking off) = zombie reaping (waitpid)
- Re-assigned crew = orphan processes
- Grace period clock = terminationGracePeriodSeconds (default 30s)
- Gangway pulled / lights out = SIGKILL
- Pre-disembark announcement = preStop hook
- Hired professional captain = init wrapper (tini / dumb-init)
- Untrained captain = naive shell entrypoint that swallows signals

---

## 4. ELI5 / ELI10

**ELI5.** A captain on a ship. The lighthouse blinks "time to leave."
The captain picks up the megaphone and tells everyone. The crew packs
up. The captain checks every name on a list as they leave. Then lights
out. If the captain ignores the lighthouse, the harbour just turns out
the lights anyway and people get stuck.

**ELI10.** Inside a container, the first process you start is PID 1
and gets two special jobs Linux normally hands to systemd: forward
signals to descendants, and reap zombie children. When K8s wants to
delete a pod, it runs the optional `preStop` hook, then sends SIGTERM
to PID 1. PID 1 is supposed to forward that to every child and wait
for them to exit. If PID 1 doesn't exit within
`terminationGracePeriodSeconds` (default 30), K8s sends SIGKILL — an
uncatchable kill. If PID 1 is `bash` or any naive entrypoint, it
swallows SIGTERM and your app never learns the pod is shutting down,
so requests drop and shutdown is always lossy. Wrap your entrypoint in
**tini** or **dumb-init** (`ENTRYPOINT ["tini", "--", "node",
"server.js"]`) and it forwards signals + reaps zombies for you. Add a
`preStop: sleep 5` if you need the load-balancer to notice the pod is
draining before connections stop.

---

## 5. Real-world scenarios

**Bash-as-PID-1 dropped SIGTERM — pods always died with SIGKILL.**
A team's deploys consistently took the full 30 seconds and ended in
"Killed". Investigation: the Dockerfile used `CMD bash startup.sh` and
startup.sh ran `node server.js &` in the background. Bash was PID 1,
caught SIGTERM, didn't forward it. Node never knew. Fix: replace with
`ENTRYPOINT ["tini", "--"]` + `CMD ["node", "server.js"]`. Deploys
became instant and graceful.

**30-second grace was too short — DB shutdown got truncated.**
A team's PostgreSQL sidecar was getting SIGKILL'd mid-checkpoint
during pod shutdowns. Result: occasional WAL corruption requiring
recovery. Fix: set `terminationGracePeriodSeconds: 300` for that
pod, plus a preStop hook that runs `pg_ctl stop -m smart`. The DB
gets up to 5 minutes to flush cleanly. Corruption stopped.

**preStop sleep saved zero-downtime rolling updates.**
During rolling updates, a fraction of requests returned 502. Cause: pod
was shutting down before the Service's endpoint controller had updated
the load-balancer; the LB kept sending traffic to a closed port. Fix:
add `preStop: { exec: { command: ["sh", "-c", "sleep 10"] } }`. The pod
sits idle for 10s after being marked for deletion, giving the LB time
to remove it from the rotation. 502s dropped to zero.

**Zombie process accumulation crashed a Java app under sustained load.**
A Java app spawned subprocesses for thumbnail generation. Each finished
quickly, but the JVM didn't reap them. Zombies accumulated until the
process table filled, then `Resource temporarily unavailable` errors.
Pod restart cleared it temporarily. Real fix: add tini as PID 1
(`ENTRYPOINT ["tini", "--", "java", "-jar", "app.jar"]`). tini reaped
zombies as they appeared. Crashes stopped.

---

## 6. Animated illustration

Three modes:

1. **Graceful shutdown timeline** (4 steps). Clock ticks: t=0 kubelet
   marks pod for deletion → preStop hook fires (sleep 5) → kubelet
   sends SIGTERM to PID 1 → tini forwards to app → app drains and
   exits 0 → kubelet records pod Terminated. Clock shows total elapsed.
2. **Bad PID 1 vs good PID 1** (4 steps). Bash entrypoint receives
   SIGTERM at t=0 → bash absorbs it, doesn't forward → child process
   keeps running → grace period elapses at t=30 → kubelet SIGKILLs
   everything → connections dropped. Then with tini: same SIGTERM →
   tini forwards to PID 2 → app exits cleanly at t=2 → no SIGKILL.
3. **Zombie reaping** (4 steps). Parent forks child → child does work
   → child exits → kernel marks it zombie until parent calls
   waitpid() → with proper PID 1 (tini): zombie reaped immediately;
   without: zombie accumulates until process table is full.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
