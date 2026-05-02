# Lesson 03 — Cloud-Native Principles

> Course: Kubernetes — Common to all distributions
> Lesson 03 of 17 in K-COM. The big idea behind everything else.
> Companion preview: `/preview-kubernetes-lesson-03.html`.

---

## 1. Concept

Cloud-native is a way of building software that assumes the world keeps
breaking and changing. Servers fail. Network blips happen. Traffic goes up
and down. Apps need to ship 50 times a day. Cloud-native software is
designed for that — not in spite of it.

Seven principles describe it, but they all stem from one idea: the
**reconciliation loop**. A small program (called a **controller**) reads
what you said you wanted, looks at what's actually running, and takes the
smallest action to close the gap. Then it does it again. Forever.

The seven principles:

1. **Declarative config** — say what, not how.
2. **Reconciliation loops** — controllers always watching.
3. **Desired vs actual state** — the spec vs reality.
4. **Immutable infrastructure** — replace, don't patch.
5. **Pets vs cattle** — replaceable, not unique.
6. **Horizontal scaling** — more copies, not bigger ones.
7. **Failure as normal** — designed-in resilience.

That's the whole game. Everything else in Kubernetes is a specialization
of these.

---

## 2. Before / After

**Before — imperative scripts.** You write the exact steps. SSH into
machines. Run commands in order. Hope nothing changes mid-deploy. If step 4
fails, you don't know if you're in state 3 or state 5. Servers are "pets":
hand-tuned, named, irreplaceable.

**After — declarative config.** You write the goal in a YAML file. The
controller figures out the steps. If something fails halfway, the controller
picks up where it left off. State is always either "matches the spec" or
"actively being reconciled." Servers are "cattle": identical and
replaceable.

What didn't change: you still need a correct spec. If the YAML says "I want
3 copies of a broken app," you'll get 3 copies of a broken app —
restarted forever.

---

## 3. Analogy — the thermostat in your house

The clearest example of cloud-native thinking is something you've used a
thousand times: the thermostat on your wall. Notice what it does and
doesn't do.

You don't tell the thermostat *how* to heat the room. You don't say "first
turn on the gas valve, then ignite the burner, then run the fan for 12
minutes." You set a number — 22°C — and walk away. The thermostat reads
the room temperature, compares it to your dial, and makes whatever
adjustments are needed. When the room gets cold again, it acts again. It
never stops watching.

Kubernetes works exactly the same way. Your YAML file is the dial. The
cluster is the room. The controllers are the thermostat brain. Every
Kubernetes object has its own controller watching it. That's it.

**Mapping:**

- The thermostat dial = your YAML file (desired state)
- The room = your live cluster (actual state)
- The thermostat brain = a controller
- The thermometer = the cluster reporting what's running
- The heater firing = the controller taking action
- "Never stops watching" = the reconciliation loop

---

## 4. ELI5 / ELI10

**ELI5.** You know how a thermostat in your house works? You set the dial
to a temperature you want. The thermostat checks the room. If it's too
cold, the heater turns on. When the room is warm enough, the heater stops.
It never gets tired. Kubernetes works the exact same way, but with computer
apps instead of room temperature.

**ELI10.** Cloud-native software is built to live in a world where things
break — servers crash, networks blip, traffic spikes. So instead of
writing scripts that say "do step 1, then 2, then 3," you write a
*declarative spec* that says "I want 3 copies of my app running." A small
program called a *controller* reads your spec, looks at what's actually
running, and takes action to close the gap. This loop runs forever. That's
why Kubernetes is so good at recovering from failures. Everything else —
auto-scaling, self-healing, rolling updates, GitOps — is a specialized
version of this same loop.

---

## 5. Real-world scenarios

**Black Friday at an e-commerce site.** Traffic jumps from 100 requests
per second to 8,000 in under an hour. The team set up a "horizontal pod
autoscaler" that watches CPU usage and scales pod copies up automatically.
By 11 AM there are 40 copies running (up from 3 normally). By 11 PM, traffic
falls and count drops back to 3. Nobody manually scaled anything.

**A cloud machine fails at 3 AM.** AWS rotates out a server. The 12 pods
running on it die instantly. Controllers notice within seconds and
reschedule them onto healthy servers. By the time anyone wakes up, the
dashboard is green and Slack shows "self-healed at 03:14 — no action
needed."

**A bad deployment is rolling out.** An engineer pushes a new version. The
new pods crash on startup (bug in the new code). The Deployment controller
sees the failed pods, stops the rollout, and keeps the old version running.
One-command rollback. Production never went down.

**Someone manually edits a config file in production.** An engineer SSHes
into the cluster and changes a ConfigMap by hand. The GitOps controller
notices the cluster has drifted from Git. Within seconds, it reverts the
change. The engineer goes put their fix in Git like everyone else.

---

## 6. Animated illustration

Three modes in the preview animation:

1. **Thermostat fires heater.** Desired = 22°, actual = 19°. Controller
   compares, fires the heater, room warms to 22°, heater stops. Loop
   continues forever.
2. **Pod self-heals.** Desired = 3 pods, actual = 3. One pod dies. Controller
   notices, schedules a replacement. Back to 3.
3. **Scale up to 5.** You change replicas from 2 to 5. Controller sees the
   gap, starts 3 new pods. Returns to steady state.

---

## 7. Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
