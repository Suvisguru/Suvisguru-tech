#!/usr/bin/env python3
"""K-Town revision — Phase 5 generalised batch transformer.

Applies the layman-first scaffolding component family from the L01
reference (preview-kubernetes-lesson-01.html) to any lesson in the
LESSONS dict whose key appears in ENABLED. Idempotent: a second run on
the same lesson aborts with an anchor-not-found error because the
first run consumed the original anchor strings.

Successor to scripts/apply_phase5_batch1.py. The transform structure
is identical; this version accumulates per-lesson data dicts as the
revision works through subsequent batches and uses ENABLED to gate
which lessons get rewritten.

Usage:
    python3 scripts/apply_phase5_batch.py
    # rewrites every lesson whose key is in ENABLED at the bottom.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------- helpers ----------

def replace_once(content: str, old: str, new: str, label: str) -> str:
    if old not in content:
        sys.exit(f"[{label}] anchor not found.\n--- expected (first 300 chars) ---\n{old[:300]}\n----------------")
    if content.count(old) > 1:
        sys.exit(f"[{label}] anchor matched {content.count(old)} times — not unique.")
    return content.replace(old, new, 1)


# ---------- extract reusable blocks from L01 ----------

L01_PATH = os.path.join(ROOT, "preview-kubernetes-lesson-01.html")
L01 = open(L01_PATH).read()

css_start = L01.index("  /* ============ LAYMAN-FIRST")
css_end = L01.index("</style>", css_start)
CSS_BLOCK = L01[css_start:css_end]

svg_start = L01.index('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" class="ktown-map"')
svg_end = L01.index("</svg>", svg_start) + len("</svg>")
KTOWN_SVG = L01[svg_start:svg_end]


def map_with_active(active_pin_id: str) -> str:
    """Return the K-Town SVG with `active` class moved to active_pin_id.

    Mayor's Office (kt-pin01) keeps the pin-anchor class but loses `active`
    unless active_pin_id == 'kt-pin01'.
    """
    svg = KTOWN_SVG
    svg = svg.replace(
        '<g class="pin pin-anchor active" id="kt-pin01"',
        '<g class="pin pin-anchor" id="kt-pin01"',
    )
    if active_pin_id == "kt-pin01":
        return svg.replace(
            '<g class="pin pin-anchor" id="kt-pin01"',
            '<g class="pin pin-anchor active" id="kt-pin01"',
        )
    if active_pin_id == "kt-pin7-5":
        return svg.replace(
            '<g class="pin pin-primer" id="kt-pin7-5"',
            '<g class="pin pin-primer active" id="kt-pin7-5"',
        )
    pattern = f'<g class="pin" id="{active_pin_id}"'
    repl = f'<g class="pin active" id="{active_pin_id}"'
    if pattern not in svg:
        sys.exit(f"map_with_active: pin {active_pin_id} not found")
    return svg.replace(pattern, repl, 1)


# ---------- shared layout data ----------

CONCEPT_RAIL_ITEMS = [
    ("L01", "what Kubernetes is", False),
    ("L02", "containers vs VMs", False),
    ("L03", "the reconciliation loop", False),
    ("L04", "how apps should be designed", False),
    ("L05", "when K8s makes sense", False),
    ("L06", "how mature teams operate it", False),
    ("L07", "how the project evolves", False),
    ("L7-5", "Linux foundations <small>(primer)</small>", True),
    ("L08", "how containers actually work", False),
    ("L09", "runtimes &amp; the OCI standard", False),
    ("L10", "how images are built", False),
    ("L11", "container security", False),
    ("L12", "how containers shut down", False),
    ("L13", "cluster architecture", False),
    ("L14", "K8s API &amp; YAML", False),
    ("L15", "Pods deep dive", False),
    ("L16", "workload controllers", False),
    ("L17", "services &amp; networking", False),
]

STRIP_ORDER = [
    "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L7-5",
    "L08", "L09", "L10", "L11", "L12", "L13", "L14", "L15",
]


def concept_rail_html(current: str) -> str:
    cur_idx = next(i for i, (k, _, _) in enumerate(CONCEPT_RAIL_ITEMS) if k == current)
    out = ['<aside class="concept-rail" aria-label="Concept journey through the Kubernetes course">',
           '  <span class="concept-rail-title">Concept journey</span>']
    for i, (key, label, primer) in enumerate(CONCEPT_RAIL_ITEMS):
        primer_cls = " primer" if primer else ""
        if i < cur_idx:
            out.append(f'  <div class="concept-rail-item done{primer_cls}"><span class="concept-rail-icon">✓</span><span>{label}</span></div>')
        elif i == cur_idx:
            out.append(f'  <div class="concept-rail-item current{primer_cls}"><span class="concept-rail-icon">▶</span><span>{label}</span><span class="concept-rail-here">← you are here</span></div>')
        else:
            out.append(f'  <div class="concept-rail-item{primer_cls}"><span class="concept-rail-icon">○</span><span>{label}</span></div>')
    out.append('</aside>')
    return "\n".join(out)


def strip_html(active_key: str) -> str:
    lines = ['  <ol class="ktown-strip" aria-hidden="true">']
    for i, key in enumerate(STRIP_ORDER, start=1):
        classes = ["ktown-strip-pin"]
        if i == 1:
            classes.append("ktown-strip-anchor")
        if key == active_key:
            classes.append("active")
        lines.append(f'    <li class="{" ".join(classes)}"></li>')
    lines.append('  </ol>')
    return "\n".join(lines)


# ---------- per-lesson data ----------

LESSONS: dict = {}

# Batch 1 entries (L02, L03, L04) preserved for completeness — gated by ENABLED
LESSONS["L02"] = dict(
    file="preview-kubernetes-lesson-02.html",
    rail_key="L02", active_pin="kt-pin02", strip_key="L02",
    district_name="Residential District",
    strip_label_district="Residential District",
    strip_label_pos="lesson 2 of 16",
    a11y_phrase="Lesson 2 of 16, Residential District.",
    aria_label_today="K-Town district map: today we are at Residential District, Lesson 02",
    map_title_today="K-Town district map · today: Residential District",
    nightmare_text="Your team needs to ship 60 microservices. Each one runs in its own virtual machine. Each VM carries a full operating system — that's 60 copies of Linux, hogging RAM and disk. Booting one takes minutes. Cold starts during traffic spikes are the difference between a sale and a lost customer. This lesson is about the lighter alternative — and why Kubernetes was built on top of it.",
    stamp_takeaway="VMs are houses (own everything, heavy). Containers are apartments (shared building, light).",
    pc1_q="A VM image is typically 5–20 GB. A container image is typically 10–500 MB. Why the gap?",
    pc1_opts=[("a) Containers compress better", False), ("b) A VM ships a whole operating system inside; a container ships only the app", True), ("c) Containers store fewer files", False)],
    pc1_feedback="<strong>Answer: b.</strong> The OS-shaped chunk is what's missing.",
    pc2_q="A bank wants to run apps for three competing customers on the same hardware. The customers don't trust each other. VMs or containers?",
    pc2_opts=[("a) Containers — they're faster", False), ("b) VMs (or sandboxed runtimes like gVisor) — separate kernels per customer", True), ("c) Either is fine", False)],
    pc2_feedback="<strong>Answer: b.</strong> Plain containers share the host kernel. A kernel exploit in one customer's container could reach others. VMs give each customer their own kernel — much stronger isolation.",
    tl_rows=[("Each house", "One virtual machine (VM)"), ("Each apartment", "One container"), ("The building's shared infrastructure (foundation, heating, plumbing)", "The host operating system's kernel"), ("The land underneath", "The physical hardware"), ("The walls between apartments", "Linux namespaces and cgroups")],
    analogy_stops_text="The analogy stops here: unlike apartments, you can run thousands of containers on one computer. The plumbing doesn't get clogged.",
    misconceptions=[("A container has its own operating system.", "It shares the host's kernel. The \"OS-like\" feel is a private view, not a real second OS."), ("Containers replaced VMs.", "They're complementary. Most cloud Kubernetes runs containers <em>inside</em> VMs the cloud provides."), ("Containers are unsafe because they share a kernel.", "They're safe enough for trusting tenants. For hostile multi-tenancy, use VMs or sandboxed runtimes (gVisor, Kata).")],
    cyoa_setup="You're running a CI system. Every commit triggers 50,000 test jobs per day. You build it on VMs, because \"VMs are isolated and safe.\" <strong>Click to see what happens to your bill. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="months later",
    cyoa_reveal="Each VM takes 90 seconds to boot. Each test takes 30 seconds. So 75% of your CI time and budget is spent waiting for VMs to boot. Containers boot in milliseconds. Switching cuts your CI bill by ~70% and triples throughput. <strong>Lesson:</strong> pick the lighter unit when the workload churns.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Each house</strong> = one VM</li>
      <li><strong>Each apartment</strong> = one container</li>
      <li><strong>Building's shared infrastructure</strong> (foundation, heating, plumbing, electrical) = the host operating system kernel</li>
      <li><strong>The land underneath</strong> = the physical hardware</li>
      <li><strong>Apartment walls between units</strong> = Linux namespaces and cgroups (the things that keep one container's view of the world separate from another's)</li>
    </ul>
  </section>''',
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">Why is the apartment-vs-house analogy a good fit for VMs vs containers?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Because it captures the real trade-off: a house duplicates everything (own roof, own furnace, own plumbing) and is fully self-contained but takes more space and resources. An apartment shares the building's infrastructure, which makes it lighter and denser, but the shared parts become a single point of failure or attack. VMs vs containers have exactly the same trade-off, just with operating systems instead of furnaces.</div>
      </div>
    </div>
  </section>''',
)

LESSONS["L03"] = dict(
    file="preview-kubernetes-lesson-03.html",
    rail_key="L03", active_pin="kt-pin03", strip_key="L03",
    district_name="Climate Control Tower",
    strip_label_district="Climate Control Tower",
    strip_label_pos="lesson 3 of 16",
    a11y_phrase="Lesson 3 of 16, Climate Control Tower.",
    aria_label_today="K-Town district map: today we are at Climate Control Tower, Lesson 03",
    map_title_today="K-Town district map · today: Climate Control Tower",
    nightmare_text="Your deploy script has 200 lines of bash. Step 4 runs <code>ssh</code> to 30 servers. Tonight, on server 17, step 4 fails — and you have no idea what state servers 1–16 are in, or 18–30. Are they on the new version? The old? Half each? You can't tell without looking. The script can't recover; it just stopped. This lesson is about the model that makes that whole class of problem go away.",
    stamp_takeaway="Kubernetes is a thermostat. You set what you want; controllers watch forever; gaps close automatically. Everything else in the course is a variation of this loop.",
    pc1_q="Your YAML says <code>replicas: 3</code>. A Pod crashes. Now 2 are running. What does the controller do?",
    pc1_opts=[("a) Sends an email", False), ("b) Notices the gap (3 ≠ 2) and starts a 3rd Pod on a healthy node", True), ("c) Updates the YAML to say <code>replicas: 2</code>", False)],
    pc1_feedback="<strong>Answer: b.</strong> The controller is constantly comparing desired (3) to actual (2). When they differ, it acts. Forever. That's the loop.",
    pc2_q="Imperative vs declarative — which one is Kubernetes?",
    pc2_opts=[("a) Imperative: \"do step 1, then step 2, then step 3\"", False), ("b) Declarative: \"I want this end state; figure it out\"", True), ("c) Both", False)],
    pc2_feedback="<strong>Answer: b.</strong> You write the goal; controllers figure out the steps. That's why K8s recovers from failures — it doesn't have a \"step 4 failed\" problem because there's no fixed step 4.",
    tl_rows=[("The thermostat dial", "Your YAML manifest <em>(desired state)</em>"), ("The room", "Your live cluster <em>(actual state)</em>"), ("The thermostat brain", "A controller"), ("The thermometer", "The cluster reporting actual state"), ("The heater firing", "The controller acting (start a Pod, scale up, restart)"), ("\"Never stops watching\"", "The reconciliation loop")],
    analogy_stops_text="The analogy stops here: a real thermostat watches one thing — temperature. Kubernetes runs many \"thermostats\" at once, one per resource type, all in parallel.",
    misconceptions=[("The reconciliation loop runs once and stops when everything matches.", "It never stops. When the gap is zero it idles, but it keeps watching. The moment something drifts (a crash, a manual edit), the loop fires again."), ("Declarative means \"I never write any logic.\"", "You still write a correct spec. If the YAML says \"3 copies of a broken app,\" you'll get 3 copies of a broken app — restarted forever."), ("There's one big controller in Kubernetes.", "There are dozens, each watching one type of resource (Deployments, Services, Jobs…), all running the same loop pattern in parallel.")],
    cyoa_setup="You SSH into a production node and \"quickly\" hand-edit a config to fix an issue. Your cluster is GitOps-managed by Argo CD. You log off feeling smart. <strong>Click to see what happens in 30 seconds. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="30 seconds later",
    cyoa_reveal="Argo CD reads your hand-edit (drift), reads what Git says (the source of truth), notices they differ, reverts your change. Slack pings the team channel: <code>drift detected, reconciled to git/main</code>. Your \"fix\" is gone. <strong>Lesson:</strong> in a GitOps world, Git is the truth. Out-of-band edits get politely undone — by design.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>The thermostat dial</strong> = your YAML file (desired state)</li>
      <li><strong>The room</strong> = your live cluster (actual state)</li>
      <li><strong>The thermostat brain</strong> = a controller (the small program watching forever)</li>
      <li><strong>The thermometer</strong> = the cluster reporting what's running</li>
      <li><strong>The heater firing</strong> = the controller taking action (start a pod, scale up, restart)</li>
      <li><strong>"Never stops watching"</strong> = the reconciliation loop (the heart of Kubernetes)</li>
    </ul>
  </section>''',
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">Why is "treat servers as cattle" a reliability strategy, not just a fashion statement?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Because if every server is hand-tuned (a "pet"), losing one means losing knowledge. Documentation is always incomplete. Recovery means a human reverse-engineering what made that server special. If servers are interchangeable cattle described declaratively, losing one is a non-event — the controller starts another from the same spec. Reliability scales because nothing depends on a specific machine surviving.</div>
      </div>
    </div>
  </section>''',
)

LESSONS["L04"] = dict(
    file="preview-kubernetes-lesson-04.html",
    rail_key="L04", active_pin="kt-pin04", strip_key="L04",
    district_name="Port + Restaurant Row",
    strip_label_district="Port + Restaurant Row",
    strip_label_pos="lesson 4 of 16",
    a11y_phrase="Lesson 4 of 16, Port and Restaurant Row.",
    aria_label_today="K-Town district map: today we are at Port + Restaurant Row, Lesson 04",
    map_title_today="K-Town district map · today: Port + Restaurant Row",
    nightmare_text="You're moving an app to Kubernetes. The app reads its database password from a file at <code>/etc/myapp/db.conf</code>, written by a Chef recipe at server-provisioning time. You bring it up in a Kubernetes Pod. The file isn't there. The app crashes on startup. Pods are temporary; Pod filesystems disappear. Your weekend is gone. This lesson is about the 12 rules that prevent you from ever fighting the platform like this again.",
    stamp_takeaway="A 12-factor app is a standard shipping container — drops cleanly into any platform. Microservices vs monoliths is about size, not virtue. Most teams should start with a modular monolith.",
    pc1_q="Where should an app's database password live?",
    pc1_opts=[("a) Hardcoded in source code", False), ("b) In a file under <code>/etc/</code> written by a Chef recipe", False), ("c) In an environment variable, injected by the platform", True)],
    pc1_feedback="<strong>Answer: c.</strong> Factor 3 (Config) — env vars, never code, never baked-in files. Same image, different config per environment.",
    pc2_q="A 6-engineer startup is debating \"should we start with microservices or a monolith?\"",
    pc2_opts=[("a) Microservices — that's how Netflix did it", False), ("b) Modular monolith — clear boundaries, simple ops", True), ("c) Doesn't matter", False)],
    pc2_feedback="<strong>Answer: b.</strong> Microservices push complexity from the codebase to the network: tracing, retries, timeouts, separate dashboards, separate on-call. A 6-engineer team rarely has the operational maturity for that. Start with a modular monolith; split a service out only when scale or team boundaries clearly demand it.",
    tl_rows=[("A standard ISO shipping container", "A 12-factor app"), ("A custom crate (barrels, bales)", "A pre-12-factor app needing custom platform handling"), ("A single restaurant", "A monolith"), ("A restaurant with specialty stations", "A modular monolith"), ("A food court of stalls", "Microservices")],
    analogy_stops_text="The analogy stops here: standard shipping containers are 20 or 40 feet long. Software containers are whatever size you make them — the \"standard\" is the interface, not the dimensions.",
    misconceptions=[("Microservices are always better than monoliths.", "They're an answer to <em>organisational scale</em>, not a starting architecture. Shopify runs hundreds of engineers on one Rails monolith — and ships daily."), ("12-factor is just a coding style.", "It's the contract between your app and any modern platform. Violating it doesn't fail tests — it fails Tuesday afternoons in production."), ("Stateless means \"the app doesn't store anything.\"", "Stateless means <em>the process</em> doesn't hold important state in memory. State lives in attached backing services — Postgres, Redis, S3 — that survive restarts.")],
    cyoa_setup="Your team writes logs to <code>/var/log/myapp.log</code>, rotated by a cron job. You move to Kubernetes \"as is.\" <strong>Click to see what happens to your logs. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="3 AM the next outage",
    cyoa_reveal="The Pod restarts. The Pod's filesystem disappears. Your logs disappear with it. Cron isn't running. Log rotation never happened. You're trying to investigate a 3 AM outage with nothing to look at. <strong>Fix:</strong> Factor 11 — write logs to stdout. Kubernetes captures them, ships them to your aggregator, retains them as policy. The platform owns log lifecycle; your app stays generic.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Standard container</strong> = 12-factor app (drops into any platform)</li>
      <li><strong>Custom crate</strong> = pre-12-factor app (needs custom handling everywhere)</li>
      <li><strong>Single restaurant</strong> = monolith (simple, coordinated, but coupled)</li>
      <li><strong>Restaurant with stations</strong> = modular monolith (boundaries inside, simple ops)</li>
      <li><strong>Food court</strong> = microservices (independent, but coordination overhead)</li>
    </ul>
  </section>''',
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">Why is "log to stdout" (Factor 11) a 12-factor rule rather than just a personal preference?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Because writing logs to a file on the pod's local disk fights the platform — that disk disappears when the pod restarts, log rotation needs separate cron jobs, and you've coupled your app to filesystem-specific assumptions. Writing to stdout lets the platform (Kubernetes, Heroku, whatever) capture logs uniformly, ship them to centralized aggregation, and rotate/retain them as policy demands. Your app stays generic; the platform handles log lifecycle.</div>
      </div>
    </div>
  </section>''',
)

# Batch 2 — L05, L06, L07
LESSONS["L05"] = dict(
    file="preview-kubernetes-lesson-05.html",
    rail_key="L05", active_pin="kt-pin05", strip_key="L05",
    district_name="Industrial Kitchen Block",
    strip_label_district="Industrial Kitchen Block",
    strip_label_pos="lesson 5 of 16",
    a11y_phrase="Lesson 5 of 16, Industrial Kitchen Block.",
    aria_label_today="K-Town district map: today we are at Industrial Kitchen Block, Lesson 05",
    map_title_today="K-Town district map · today: Industrial Kitchen Block",
    nightmare_text="You adopted Kubernetes \"because it's the modern way.\" A year in, two of your four engineers are full-time on cluster ops: upgrades, observability, security patches, certificate rotation, on-call. You're shipping fewer features than you would have on Heroku. Your investors are asking why. This lesson is about reading the situation honestly <em>before</em> adoption — not after.",
    stamp_takeaway="Kubernetes pays back at operational scale (many services, many teams). For a single small app, it's an industrial kitchen for your morning toast.",
    pc1_q="Three engineers, one Django app, one Postgres, deploying twice a week. Does Kubernetes fit?",
    pc1_opts=[("a) Yes — it's the standard", False), ("b) No — managed app platform (Render, Fly, Heroku) is a better fit at this size", True), ("c) Only if they're remote", False)],
    pc1_feedback="<strong>Answer: b.</strong> Kubernetes pays back when many services and many teams are the bottleneck. With one app and three engineers, the cluster itself becomes the bottleneck.",
    pc2_q="A high-frequency trading firm has a trading engine that needs sub-100µs latency. K8s networking adds 50–200µs per Pod hop. Should the trading engine run on Kubernetes?",
    pc2_opts=[("a) Yes — it's the modern way", False), ("b) No — bare metal with kernel-bypass networking", True), ("c) Only the dashboards", False)],
    pc2_feedback="<strong>Answer: b</strong> (and also c). The trading engine goes on bare metal. The dashboards (normal HTTP latency) can happily sit on K8s. Different workloads, different platforms.",
    tl_rows=[("An industrial kitchen", "Kubernetes"), ("Many cooks", "Many engineering teams sharing one platform"), ("Many ovens", "Many services running concurrently"), ("Service standards and the expediter", "Consistency, observability, automation"), ("A toaster on the counter", "A managed app platform (Render, Fly, Heroku, App Runner)"), ("Building a kitchen for toast", "Adopting Kubernetes for a single small app")],
    analogy_stops_text="The analogy stops here: a kitchen and a toaster cost different amounts. Kubernetes can be free if you self-manage — the cost is engineering time, which is harder to see on a cloud bill.",
    misconceptions=[("Kubernetes makes one app simpler.", "It never does. It pays off when the <em>count</em> of things you're operating becomes the bottleneck."), ("Managed Kubernetes is the same operational burden as self-managed.", "Managed (EKS / AKS / GKE) takes the control plane off your plate — that's most of the ongoing pain."), ("If we don't pick Kubernetes now, we'll regret it later.", "Most teams are better off starting on a managed app platform and migrating <em>if</em> they outgrow it. Migrations are real but cheaper than two engineers full-time on cluster ops at year one.")],
    cyoa_setup="Your CEO read a Hacker News post and announces \"we're moving to Kubernetes by Q3.\" Your team is 4 engineers, 1 app, 100 daily users. <strong>Click to see how this goes. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="end of Q4",
    cyoa_reveal="You've shipped half the planned features. One engineer quit because \"I joined to build a product, not babysit YAML.\" The CEO eventually asks \"what would have happened on Render?\" The answer is: same product, twice the velocity, no cluster on-call. <strong>Lesson:</strong> \"the modern way\" without \"the modern need\" is just the modern bill.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Industrial kitchen</strong> = Kubernetes (powerful platform with rich tooling)</li>
      <li><strong>Many cooks</strong> = many teams sharing infrastructure</li>
      <li><strong>Many ovens</strong> = many services running concurrently</li>
      <li><strong>Service standards &amp; expediter</strong> = consistency, observability, automation</li>
      <li><strong>Toaster</strong> = a managed app platform (Render, Fly, Heroku, App Runner)</li>
      <li><strong>"Wrong tool"</strong> = building a kitchen for toast (or running K8s for one app)</li>
    </ul>
  </section>''',
    # L05 third quiz: HFT firm dashboards/bare-metal scenario — replaced with CYOA
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">A high-frequency trading firm has 3 services. Two are dashboards (HTTP, normal latency). One is the trading engine (sub-100µs end-to-end). What's the right architecture?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Mixed. Run the dashboards on Kubernetes (managed, cheap, normal HTTP latency is fine). Run the trading engine on bare metal with kernel-bypass networking (DPDK). K8s adds 50-200µs per network hop via CNI/kube-proxy — negligible for HTTP, lethal for HFT. The trick: don't force one tool to handle every workload. Different workloads, different platforms.</div>
      </div>
    </div>
  </section>''',
)

LESSONS["L06"] = dict(
    file="preview-kubernetes-lesson-06.html",
    rail_key="L06", active_pin="kt-pin06", strip_key="L06",
    district_name="Public Library",
    strip_label_district="Public Library",
    strip_label_pos="lesson 6 of 16",
    a11y_phrase="Lesson 6 of 16, Public Library.",
    aria_label_today="K-Town district map: today we are at Public Library, Lesson 06",
    map_title_today="K-Town district map · today: Public Library",
    nightmare_text="Your one ops engineer is the bottleneck for every deploy across 6 product teams. Every change is a ticket. Tickets pile up. Deploys take days. The ops engineer is on call for everything they didn't write. They're burning out and the company can't ship. This lesson is about the org shape that fixes this — and why it's not just a tooling change.",
    stamp_takeaway="Five practices that compound — GitOps + platform engineering + SRE + service ownership + multi-tenancy. None is a Kubernetes feature; all are practices Kubernetes enables.",
    pc1_q="GitOps puts the source of truth in:",
    pc1_opts=[("a) The cluster", False), ("b) An ops engineer's head", False), ("c) A Git repository", True)],
    pc1_feedback="<strong>Answer: c.</strong> An agent in the cluster watches Git and reconciles. Same loop pattern as a Kubernetes controller, just one level up.",
    pc2_q="\"You build it, you run it\" means:",
    pc2_opts=[("a) Developers do everything; no ops team", False), ("b) The team that built the service is on its on-call rotation", True), ("c) Only senior engineers go on call", False)],
    pc2_feedback="<strong>Answer: b.</strong> The team that wrote the code is paged when it breaks. Reliability emerges from incentive — they fix the things that wake them up.",
    tl_rows=[("The card catalog", "Git (the source of truth for every change)"), ("The librarian", "The GitOps controller (Argo CD / Flux)"), ("The library building and reading rooms", "The platform (cluster + tooling) the platform team builds"), ("The section-owning staff", "Product teams owning their services and on-call"), ("The head librarian", "SRE practice (SLIs / SLOs / error budgets)"), ("Schools, scholars, public sharing the building", "Multi-tenancy (many teams sharing one cluster)")],
    analogy_stops_text="The analogy stops here: the GitOps controller doesn't argue with you. If the catalog says \"shelve it under N\", it shelves it under N — even if a human walked by and put the book somewhere \"more sensible.\"",
    misconceptions=[("GitOps is just \"use Git for your YAML.\"", "It's an <em>agent in the cluster</em> continuously reconciling state to match Git. Manual edits get reverted. That's the part that makes it powerful."), ("SRE = \"ops, but renamed.\"", "SRE adds explicit reliability targets (SLOs) and an <em>error budget</em> — when you've spent the budget on outages, you slow down feature work and fix things. It's an operating model, not a job title."), ("Multi-tenancy means one cluster per team.", "Soft tenancy = one cluster, isolated by namespaces + RBAC + quotas (for trusted tenants). Hard tenancy (separate clusters or vCluster) is for <em>untrusted</em> tenants only.")],
    cyoa_setup="Your platform team runs an \"ops ticket queue\" for 6 product teams. Tickets average 2 days to close. <strong>Click to see the year-end review. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="year-end review",
    cyoa_reveal="Two engineers quit (burnout). The remaining ops engineer is on call for 6 teams' code they didn't write. Deploys average 2 days from PR to live. Product velocity is half of what it could be. The fix isn't more tooling — it's restructuring: platform team owns the road; product teams own their services and their pages. Reliability follows incentive.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>The card catalog</strong> = Git (source of truth for every change)</li>
      <li><strong>The librarian</strong> = the GitOps controller (Argo CD / Flux) reading the catalog and shelving books</li>
      <li><strong>The library building &amp; reading rooms</strong> = the platform (cluster + tooling) the platform team builds</li>
      <li><strong>The section-owning staff</strong> = product teams owning their services and on-call rotations</li>
      <li><strong>The head librarian</strong> = SRE practice (measuring reliability with SLIs/SLOs/error budgets)</li>
      <li><strong>Schools, scholars, public sharing the building</strong> = multi-tenancy (many teams sharing one cluster)</li>
    </ul>
  </section>''',
    # L06 third quiz: research-platform multi-tenancy — replaced with CYOA
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">A research computing platform serves 12 labs. Some labs are trusted; others run code from external collaborators (untrusted). What's the right multi-tenancy strategy?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Mixed. Use soft tenancy (namespaces + RBAC + ResourceQuotas + NetworkPolicies) for trusted labs — cheap, easy, perfectly fine when teams trust each other. Use hard tenancy (vCluster or separate clusters) for untrusted labs — each lab gets its own API server, isolated control plane, no risk of breaking out. Both share the same physical nodes underneath, so you don't pay 12× cluster costs.</div>
      </div>
    </div>
  </section>''',
)

LESSONS["L07"] = dict(
    file="preview-kubernetes-lesson-07.html",
    rail_key="L07", active_pin="kt-pin07", strip_key="L07",
    district_name="K-Town Rail Yard",
    strip_label_district="K-Town Rail Yard",
    strip_label_pos="lesson 7 of 16",
    a11y_phrase="Lesson 7 of 16, K-Town Rail Yard.",
    aria_label_today="K-Town district map: today we are at K-Town Rail Yard, Lesson 07",
    map_title_today="K-Town district map · today: K-Town Rail Yard",
    nightmare_text="You enabled a Kubernetes alpha feature in production \"to get ahead.\" Six months later you upgrade the cluster. The feature was renamed. Your manifests don't apply. Your deploys are broken. You spend two on-call weeks rebuilding workloads. This lesson is about the lifecycle every Kubernetes feature graduates through — and why \"GA only in prod\" is the rule that keeps you out of this hole.",
    stamp_takeaway="Every Kubernetes feature graduates alpha → beta → GA, like train signals tested on a quiet branch line first. Production runs on GA.",
    pc1_q="What does \"GA\" mean in Kubernetes?",
    pc1_opts=[("a) \"Good Available\"", False), ("b) \"General Availability\" — stable, on by default, backward-compatibility guaranteed", True), ("c) \"Google Approved\"", False)],
    pc1_feedback="<strong>Answer: b.</strong> GA carries the strongest compatibility guarantee K8s offers.",
    pc2_q="Your team is debating whether to enable a new beta feature in production.",
    pc2_opts=[("a) Yes — beta is mostly stable", False), ("b) Read the KEP, vet case-by-case, decide based on risk", True), ("c) Never use anything until it's GA", False)],
    pc2_feedback="<strong>Answer: b.</strong> Beta APIs <em>can</em> still change shape. The right move is vetting per feature, per cluster, per risk profile — not a blanket yes or no.",
    tl_rows=[("Quiet branch line", "Alpha (off by default, may break, dev / test only)"), ("Moderately busy line", "Beta (mostly works, may still tweak — vet for prod case by case)"), ("Main intercity line", "GA / Stable (boring, predictable, default for production)"), ("The railroad's signal-testing process", "Kubernetes Enhancement Proposals (KEPs)"), ("The signal designers", "SIGs (Special Interest Groups)"), ("The railroad's operating standards body", "The CNCF and the Kubernetes project itself")],
    analogy_stops_text="The analogy stops here: trains test new signals once per signal. Kubernetes tests every feature, separately, every release. There's no shared \"main line approval.\"",
    misconceptions=[("Alpha = \"almost done.\"", "Alpha = \"off by default, may break, may vanish without deprecation.\" Production-hostile by design."), ("Kubernetes belongs to Google.", "It came out of Google in 2014, but it's been governed by the CNCF (a Linux Foundation project) since 2015. Hundreds of contributors at hundreds of companies."), ("\"Kubernetes-compatible\" and \"Certified Kubernetes\" mean the same thing.", "Certified Kubernetes is a CNCF program with a specific test suite. \"Compatible\" is marketing.")],
    cyoa_setup="You read about a shiny new alpha feature and enable it cluster-wide. Your prod runs on it. <strong>Click to see what happens at the next minor upgrade. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="next minor upgrade",
    cyoa_reveal="The alpha API was renamed without deprecation (legal under alpha rules). Your manifests don't apply. Pods stuck. You spend two weeks rewriting workloads. <strong>Lesson:</strong> alpha is the quiet branch line where breakage is expected. Production is the main intercity. Don't run intercity trains on branch-line tracks.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Quiet branch line</strong> = alpha (off by default, may break, dev/test clusters only)</li>
      <li><strong>Moderately busy line</strong> = beta (mostly works, may still tweak, vet for prod case by case)</li>
      <li><strong>Main intercity line</strong> = GA / Stable (boring, predictable, default for production)</li>
      <li><strong>The railroad's signal-testing process</strong> = Kubernetes Enhancement Proposals (KEPs)</li>
      <li><strong>The signal designers</strong> = SIGs (Special Interest Groups) reviewing changes</li>
      <li><strong>The railroad's operating standards body</strong> = the CNCF and the Kubernetes project itself</li>
    </ul>
  </section>''',
    # L07 third quiz: alpha → beta → GA reasoning — replaced with CYOA
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">Why does Kubernetes ship features through alpha → beta → GA instead of just shipping them as "stable" right away?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Same reason railways test new signals on quiet branch lines first. Once a feature is GA, its API is locked — you can't change it without a multi-release deprecation cycle. So Kubernetes wants the API design to be tested in real workloads BEFORE it commits to backward compatibility forever. Alpha gives a small group of brave users a chance to try it and report problems. Beta opens it to a wider audience for shape refinement. By the time it goes GA, the API has had real usage feedback baked in.</div>
      </div>
    </div>
  </section>''',
)


# ----------- HTML builders -----------

def build_district_line(name: str) -> str:
    return f'<p class="district-line">📍 Today\'s stop in K-Town: <strong>{name}</strong>.</p>'


def build_map_block(L: dict) -> str:
    svg = map_with_active(L["active_pin"])
    svg = svg.replace(
        'aria-label="K-Town district map: today we are at Mayor\'s Office, Lesson 01"',
        f'aria-label="{L["aria_label_today"]}"',
    )
    svg = svg.replace(
        '<title>K-Town district map · today: Mayor\'s Office</title>',
        f'<title>{L["map_title_today"]}</title>',
    )
    strip = strip_html(L["strip_key"])
    return f'''<div class="ktown-map-wrap">
  {svg}

{strip}
  <p class="ktown-strip-label">📍 <strong>{L["strip_label_district"]}</strong> <span>· {L["strip_label_pos"]}</span><span class="visually-hidden">{L["a11y_phrase"]}</span></p>
</div>'''


def build_nightmare(text: str) -> str:
    return f'''  <!-- 3 AM Nightmare opener -->
  <div class="nightmare">
    <div class="nightmare-box">
      <span class="nightmare-tag">🚨 The 3 AM Nightmare</span>
      <p>{text}</p>
    </div>
  </div>'''


def build_stamp(takeaway: str, placement_comment: str) -> str:
    return f'''  <!-- One-sentence stamp · {placement_comment} -->
  <div class="stamp">
    <p class="stamp-box">🎯 <strong>If you remember nothing else:</strong> {takeaway}</p>
  </div>'''


def build_pause_check(label: str, q: str, opts: list, feedback: str) -> str:
    opt_html = "\n".join(
        f'        <li><button type="button" class="pause-check-opt" data-correct="{"true" if c else "false"}">{txt}</button></li>'
        for (txt, c) in opts
    )
    return f'''  <!-- {label} -->
  <div class="pause-check">
    <div class="pause-check-box">
      <span class="pause-check-tag">⏸ Pause and check</span>
      <p class="pause-check-q">{q}</p>
      <ul class="pause-check-opts">
{opt_html}
      </ul>
      <p class="pause-check-feedback">{feedback}</p>
    </div>
  </div>'''


def build_translation_legend(rows: list, analogy_stops: str) -> str:
    row_html = "\n".join(
        f'          <tr><td>{l}</td><td>{r}</td></tr>'
        for (l, r) in rows
    )
    return f'''    <div class="translation-legend">
      <table>
        <thead>
          <tr><th>In the story…</th><th>…in Kubernetes</th></tr>
        </thead>
        <tbody>
{row_html}
        </tbody>
      </table>
    </div>

    <p class="analogy-stops">⚠️ <em>{analogy_stops}</em></p>
  </section>'''


def build_misconceptions(items: list) -> str:
    cards = "\n".join(
        f'''        <div class="misc-card">
          <div class="misc-row misc-myth"><strong>Myth:</strong> {m}</div>
          <div class="misc-row misc-truth"><strong>Truth:</strong> {t}</div>
        </div>'''
        for (m, t) in items
    )
    return f'''    <!-- Common Misconceptions panel -->
    <div class="misconceptions">
      <h3>Common Misconceptions</h3>
      <div class="misconceptions-grid">
{cards}
      </div>
    </div>

    <div class="flashcard-grid">'''


def build_cyoa(L: dict) -> str:
    return f'''      <div class="quiz-card cyoa-quiz">
        <span class="cyoa-tag">🎬 Choose Your Own Adventure</span>
        <p class="quiz-prompt">{L["cyoa_setup"]}</p>
        <button class="quiz-reveal" type="button">{L["cyoa_button"]}</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">{L["cyoa_tag_text"]}</span>{L["cyoa_reveal"]}</div>
      </div>
    </div>
  </section>'''


JS_OLD = '''  // quiz reveals
  document.querySelectorAll('.quiz-reveal').forEach(btn => {
    btn.addEventListener('click', () => {
      const ans = btn.parentElement.querySelector('.quiz-answer');
      const open = ans.classList.toggle('show');
      btn.textContent = open ? 'Hide answer' : 'Show answer';
    });
  });'''

JS_NEW = '''  // quiz reveals (handles both "Show answer" and CYOA "Show what happened")
  document.querySelectorAll('.quiz-reveal').forEach(btn => {
    const showText = btn.textContent;
    const hideText = showText.replace(/^Show/, 'Hide');
    btn.addEventListener('click', () => {
      const ans = btn.parentElement.querySelector('.quiz-answer');
      const open = ans.classList.toggle('show');
      btn.textContent = open ? hideText : showText;
    });
  });

  // pause-and-check
  document.querySelectorAll('.pause-check-box').forEach(box => {
    const opts = box.querySelectorAll('.pause-check-opt');
    const fb = box.querySelector('.pause-check-feedback');
    opts.forEach(opt => {
      opt.addEventListener('click', () => {
        opts.forEach(o => o.classList.remove('correct','wrong'));
        opt.classList.add(opt.dataset.correct === 'true' ? 'correct' : 'wrong');
        fb.classList.add('show');
      });
    });
  });'''


SECTION7_INTRO_PATTERN = re.compile(
    r'  <section class="s">\n'
    r'    <span class="s-eyebrow">Section 7 · Flashcards &amp; quiz</span>\n'
    r'    <h2>([^<]+)</h2>\n'
    r'(?:    <p>([^<]+)</p>\n)?'
    r'\n'
    r'    <div class="flashcard-grid">'
)


def transform(L: dict) -> None:
    path = os.path.join(ROOT, L["file"])
    content = open(path).read()

    if "LAYMAN-FIRST SCAFFOLDING" in content:
        sys.exit(f"{L['file']}: already has scaffolding block. Aborting (idempotency).")

    content = replace_once(content, "</style>", CSS_BLOCK + "</style>", f"{L['file']} CSS")

    rail = concept_rail_html(L["rail_key"])
    content = replace_once(
        content,
        '<body data-theme="light">\n\n<header class="topbar">',
        f'<body data-theme="light">\n\n{rail}\n\n<header class="topbar">',
        f"{L['file']} concept rail",
    )

    district = build_district_line(L["district_name"])
    map_block = build_map_block(L)
    content = replace_once(
        content,
        "</header>\n\n<main>",
        f"</header>\n\n{district}\n\n{map_block}\n\n<main>",
        f"{L['file']} district + map",
    )

    nightmare = build_nightmare(L["nightmare_text"])
    stamp_top = build_stamp(L["stamp_takeaway"], "top placement")
    content = replace_once(
        content,
        '  </section>\n\n  <!-- ============================== SECTION 1 — CONCEPT ============================== -->',
        f'  </section>\n\n{nightmare}\n\n{stamp_top}\n\n  <!-- ============================== SECTION 1 — CONCEPT ============================== -->',
        f"{L['file']} Nightmare + top stamp",
    )

    pc1 = build_pause_check("Pause-and-check #1 · after Section 1", L["pc1_q"], L["pc1_opts"], L["pc1_feedback"])
    content = replace_once(
        content,
        '  </section>\n\n  <!-- ============================== SECTION 2 — BEFORE / AFTER ============================== -->',
        f'  </section>\n\n{pc1}\n\n  <!-- ============================== SECTION 2 — BEFORE / AFTER ============================== -->',
        f"{L['file']} pause-check #1",
    )

    legend = build_translation_legend(L["tl_rows"], L["analogy_stops_text"])
    content = replace_once(content, L["old_mapping_block"], legend, f"{L['file']} translation legend")

    pc2 = build_pause_check("Pause-and-check #2 · after Section 4", L["pc2_q"], L["pc2_opts"], L["pc2_feedback"])
    content = replace_once(
        content,
        '  </section>\n\n  <!-- ============================== SECTION 5 — REAL-WORLD ============================== -->',
        f'  </section>\n\n{pc2}\n\n  <!-- ============================== SECTION 5 — REAL-WORLD ============================== -->',
        f"{L['file']} pause-check #2",
    )

    m = SECTION7_INTRO_PATTERN.search(content)
    if not m:
        sys.exit(f"{L['file']}: Section 7 intro pattern not found.")
    h2_text = m.group(1)
    misconceptions_block = build_misconceptions(L["misconceptions"])
    new_section7 = (
        '  <section class="s">\n'
        f'    <span class="s-eyebrow">Section 7 · Misconceptions, flashcards &amp; quiz</span>\n'
        f'    <h2>{h2_text}</h2>\n'
        f'    <p>Three common misconceptions to clear up first, then the flashcards and quiz.</p>\n'
        f'\n'
        f'{misconceptions_block}'
    )
    content = replace_once(content, m.group(0), new_section7, f"{L['file']} Section 7 update")

    cyoa = build_cyoa(L)
    content = replace_once(content, L["old_third_quiz"], cyoa, f"{L['file']} CYOA")

    stamp_bottom = build_stamp(L["stamp_takeaway"], "bottom placement (identical to top)")
    content = replace_once(
        content,
        '  </details>\n\n  <!-- ============================== RECAP + COMPLETION ============================== -->',
        f'  </details>\n\n{stamp_bottom}\n\n  <!-- ============================== RECAP + COMPLETION ============================== -->',
        f"{L['file']} bottom stamp",
    )

    content = replace_once(content, JS_OLD, JS_NEW, f"{L['file']} JS")

    open(path, "w").write(content)
    print(f"  {L['file']}: rewritten ({len(content):,} bytes)")


LESSONS["L08"] = dict(
    file="preview-kubernetes-lesson-08.html",
    rail_key="L08", active_pin="kt-pin08", strip_key="L08",
    district_name="Office Tower with Utility Meters",
    strip_label_district="Office Tower",
    strip_label_pos="lesson 8 of 16",
    a11y_phrase="Lesson 8 of 16, Office Tower with Utility Meters.",
    aria_label_today="K-Town district map: today we are at Office Tower with Utility Meters, Lesson 08",
    map_title_today="K-Town district map · today: Office Tower with Utility Meters",
    nightmare_text="Your container keeps getting killed. The logs say <code>OOMKilled</code>. You set the memory limit to 256Mi. The app reports it only uses 200MB. Why is it dying? Because the kernel — the <em>real</em> boss of the whole machine — is enforcing limits you didn't fully understand. This lesson is about the five Linux features that decide what your container can and can't do. No magic. Just plumbing.",
    stamp_takeaway="A container is a Linux process with walls (namespaces), meters (cgroups), and rules about what it can do (capabilities, seccomp, LSM). Five kernel features, no magic.",
    pc1_q="What stops one container from seeing another container's processes?",
    pc1_opts=[("a) The container runtime", False), ("b) Linux namespaces — specifically the PID namespace", True), ("c) Encryption", False)],
    pc1_feedback="<strong>Answer: b.</strong> Each container gets a private view of process IDs. Without that namespace, <code>ps</code> would show every process on the host.",
    pc2_q="A container hits 257MB of memory; its <code>limits.memory</code> is 256Mi. What happens?",
    pc2_opts=[("a) The container slows down", False), ("b) The kernel kills the container's PID 1 (OOM)", True), ("c) The container gets more memory automatically", False)],
    pc2_feedback="<strong>Answer: b.</strong> cgroup memory limits aren't suggestions. The kernel enforces them with <code>OOMKilled</code>.",
    tl_rows=[("The office building", "The host machine + Linux kernel"), ("Each office", "A container (a process or process group)"), ("Office walls and a private door", "Linux namespaces (PID, NET, MNT, UTS, IPC, USER, cgroup, time)"), ("Utility meters per office", "cgroups (CPU, memory, I/O budgets)"), ("The doorman / security guard", "capabilities + seccomp + AppArmor / SELinux"), ("Shared building utilities", "The host kernel everyone shares")],
    analogy_stops_text="The analogy stops here: an office building has one electrical panel that one tenant can overload. The kernel can be DoS'd by a noisy container too — but cgroups make this much harder than the real-world equivalent.",
    misconceptions=[("\"Container\" is a Linux feature.", "Containers are made by <em>combining</em> five kernel features (namespaces + cgroups + capabilities + seccomp + LSM). The runtime (Docker, containerd) bundles them. The kernel does the work."), ("Each container has its own kernel.", "All containers on a host share the host's kernel. That's the whole point — and the whole risk. A kernel exploit can break out of any container."), ("<code>limits</code> and <code>requests</code> are the same thing.", "<code>requests</code> is what the scheduler reserves (the floor). <code>limits</code> is the hard ceiling (CPU throttled, memory OOM-killed above).")],
    cyoa_setup="A teammate adds <code>hostNetwork: true</code> to a Pod spec \"just to test something.\" <strong>Click to see what they just did. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="what they just did",
    cyoa_reveal="The container now shares the host's network stack — same IPs, same interfaces, same firewall rules. It can bind to any host port (and conflict with anything else on the host). It can sniff traffic on host interfaces. K8s Service discovery often breaks because the Pod has the host's IP, not a Pod IP. <strong>Lesson:</strong> every <code>host*</code> field (<code>hostNetwork</code>, <code>hostPID</code>, <code>hostIPC</code>) drops a namespace and gives the container access to host resources. Powerful for specific cases (CNI plugins). Footgun for normal apps.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>The office building</strong> = the host machine + Linux kernel</li>
      <li><strong>Each office</strong> = a container (a process or group of processes)</li>
      <li><strong>Office walls + private door</strong> = namespaces (PID, NET, MNT, UTS, IPC, USER, cgroup, time)</li>
      <li><strong>Utility meters per office</strong> = cgroups (CPU, memory, I/O budgets)</li>
      <li><strong>Doorman / security guard</strong> = capabilities + seccomp + AppArmor/SELinux</li>
      <li><strong>Shared building utilities</strong> = the kernel everyone shares</li>
    </ul>
  </section>''',
    # L08 third quiz: hostNetwork — replaced with the CYOA which covers same ground in story form
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">A DevOps engineer wants to "just test something" in a container and adds <code>hostNetwork: true</code> to the pod spec. What did they just give up?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>The NET namespace. The container now shares the host's network stack — same IP addresses, same interfaces, same firewall rules. It can bind to any host port (and conflict with anything else on the host using that port). It can sniff traffic on host interfaces. Service discovery via Kubernetes Services often breaks because the pod has the host's IP, not a pod IP. Powerful for specific use cases (CNI plugins, host-level monitoring) — but a security and operational footgun for normal apps. Audit hostNetwork usage regularly.</div>
      </div>
    </div>
  </section>''',
)


LESSONS["L09"] = dict(
    file="preview-kubernetes-lesson-09.html",
    rail_key="L09", active_pin="kt-pin09", strip_key="L09",
    district_name="Customs Warehouse",
    strip_label_district="Customs Warehouse",
    strip_label_pos="lesson 9 of 16",
    a11y_phrase="Lesson 9 of 16, Customs Warehouse.",
    aria_label_today="K-Town district map: today we are at Customs Warehouse, Lesson 09",
    map_title_today="K-Town district map · today: Customs Warehouse",
    nightmare_text="Your team built an app on an ARM Mac (M-series). You deploy to AMD64 nodes in EKS. The Pod crashes immediately: <code>exec format error</code>. You can't tell from the message that the binary is the wrong architecture. You stare at logs for an hour. This lesson is about the format that makes containers portable — and the standard that lets one image work on every CPU and every cloud.",
    stamp_takeaway="OCI is the standard. Runtimes are forklifts. Layers stack. Tags move; digests don't. Pin to digests in production.",
    pc1_q="What does \"OCI\" stand for?",
    pc1_opts=[("a) Open Container Image", False), ("b) Open Container Initiative — Linux Foundation standards body since 2015", True), ("c) Operating Container Index", False)],
    pc1_feedback="<strong>Answer: b.</strong> Three specs (image, runtime, distribution). The contract that lets any runtime work with any registry.",
    pc2_q="You see <code>nginx:1.27</code> and <code>nginx@sha256:abc…</code>. Which is safe to use in production?",
    pc2_opts=[("a) The tag — it's friendlier", False), ("b) The digest — it's immutable", True), ("c) Either, doesn't matter", False)],
    pc2_feedback="<strong>Answer: b.</strong> Tags can be moved by the publisher. Digests are SHA-256 of the manifest — same content always = same digest. Pin to digests for reproducibility.",
    tl_rows=[("A standard ISO shipping container", "An OCI image (the format)"), ("Layers stacked inside the container", "Image layers (each a tarball with its own SHA-256)"), ("The packing list on the door", "The image manifest (JSON describing the layers)"), ("A friendly label on the outside", "A tag (mutable — can be moved by the publisher)"), ("The unique tracking number", "The digest (immutable SHA-256 hash of the manifest)"), ("The warehouse", "A container registry (Docker Hub, GHCR, ECR, GCR, ACR, Harbor, Quay)"), ("The forklifts that move boxes", "Container runtimes (containerd / CRI-O at high level; runc / crun / youki at low level)")],
    analogy_stops_text="The analogy stops here: a real shipping container has fixed dimensions. A software image is whatever size the layers add up to. The \"standard\" is the format, not the size.",
    misconceptions=[("Docker is the only container runtime.", "Modern Kubernetes runs <code>containerd</code> or <code>CRI-O</code> by default. Docker is a higher-level platform that uses <code>containerd</code> underneath."), ("<code>:latest</code> is fine for production.", "<code>:latest</code> is the worst tag offender. It's mutable. Two Pods with the same <code>:latest</code> tag can run different code on different nodes after a re-push. Pin to a digest."), ("An image works on any CPU.", "Only if it was built multi-arch (<code>docker buildx --platform linux/amd64,linux/arm64</code>). Otherwise an ARM build will not run on AMD64 nodes.")],
    cyoa_setup="Your team uses <code>image: my-app:latest</code> in production \"so we always get the newest version.\" <strong>Click to see what happens on Friday at 6 PM. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="by Saturday morning",
    cyoa_reveal="Someone pushes a new <code>latest</code> with a bad migration. Pods restarting through the night pick up the new image. Half the Pods are on the bad image and half on the old — depending on when each Pod last restarted. You can't even reproduce the issue locally because <code>latest</code> is whatever it is right now. <strong>Fix:</strong> pin to a digest. Use Renovate to bump digests via PR with tests. Reproducibility AND staying current.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Standard shipping container</strong> = OCI image format</li>
      <li><strong>Layers stacked inside</strong> = image layers (each a tarball with its own SHA256)</li>
      <li><strong>Packing list</strong> = manifest (JSON describing the layers)</li>
      <li><strong>Friendly label</strong> = tag (mutable, can be moved)</li>
      <li><strong>Unique tracking number</strong> = digest (immutable SHA256 hash)</li>
      <li><strong>Warehouses</strong> = registries (Docker Hub, GHCR, ECR, GCR, ACR, Harbor, Quay)</li>
      <li><strong>Forklifts</strong> = container runtimes (containerd / CRI-O at high level; runc / crun / youki at low level)</li>
    </ul>
  </section>''',
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">A team builds their image on an ARM Mac (M-series). When they deploy to AMD64 nodes in EKS, the pod crashes with "exec format error". What happened?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>The image was built only for the host's architecture (linux/arm64). The AMD64 nodes can't run an ARM binary. Fix: build a multi-arch image with <code>docker buildx build --platform linux/amd64,linux/arm64 -t my-app:v1 --push .</code> The result is a single tag containing manifests for both architectures. EKS nodes will pick the right one automatically.</div>
      </div>
    </div>
  </section>''',
)

LESSONS["L10"] = dict(
    file="preview-kubernetes-lesson-10.html",
    rail_key="L10", active_pin="kt-pin10", strip_key="L10",
    district_name="Bakery District",
    strip_label_district="Bakery District",
    strip_label_pos="lesson 10 of 16",
    a11y_phrase="Lesson 10 of 16, Bakery District.",
    aria_label_today="K-Town district map: today we are at Bakery District, Lesson 10",
    map_title_today="K-Town district map · today: Bakery District",
    nightmare_text="Your Node.js image is 1.2 GB. CVE scans flag 124 vulnerabilities, mostly in libraries you don't even use. Production pulls take 90 seconds — that's 90 seconds of extra outage every time something restarts. Your security team is asking pointed questions. This lesson is about the changes that take that image from 1.2 GB to 80 MB and from 124 CVEs to 8 — without touching your app code.",
    stamp_takeaway="Build small (multi-stage), ship smaller (distroless), sign your work, generate an SBOM, scan for CVEs. That's a production-grade image.",
    pc1_q="A multi-stage Dockerfile has:",
    pc1_opts=[("a) Multiple Dockerfiles in one repo", False), ("b) Multiple <code>FROM</code> statements — a \"build\" stage with full toolchain, a \"runtime\" stage with only the artifact", True), ("c) Multiple containers running in parallel", False)],
    pc1_feedback="<strong>Answer: b.</strong> Final image is 10–100× smaller because the runtime stage doesn't carry compilers, source code, or dev dependencies.",
    pc2_q="What's an SBOM?",
    pc2_opts=[("a) \"Service Bound Object Metadata\"", False), ("b) Software Bill of Materials — machine-readable list of every component in your image", True), ("c) A type of container", False)],
    pc2_feedback="<strong>Answer: b.</strong> When the next Log4Shell drops, an SBOM database lets you grep for the vulnerable library across hundreds of services in seconds. Without one, days.",
    tl_rows=[("The recipe", "The Dockerfile (or Buildpacks descriptor, ko config, etc.)"), ("The oven", "The image builder (BuildKit, Buildah, Kaniko, ko, Buildpacks)"), ("Multi-stage baking", "A multi-stage Dockerfile (build stage + runtime stage)"), ("The cake base", "The base image (full distro vs alpine vs distroless vs scratch)"), ("Ingredient list on the side", "The SBOM (SPDX or CycloneDX)"), ("The baker's signature seal", "Image signing (cosign / sigstore)"), ("Food safety inspection", "Vulnerability scanning (Trivy, Grype, Snyk)")],
    analogy_stops_text="The analogy stops here: a real cake gets baked once and eaten. A container image gets pulled millions of times. Optimisation matters here in a way it doesn't for cakes.",
    misconceptions=[("Distroless means \"no Linux.\"", "Distroless images include just enough Linux to run your app — and nothing else (no shell, no package manager, no debugger). The runtime is still Linux underneath."), ("Smaller image = always better.", "Distroless and <code>scratch</code> are harder to debug. The right answer is \"smallest base that runs your app <em>and</em> lets you investigate when needed\" — sometimes that's a slim variant, not scratch."), ("Image signing prevents bugs.", "Signing prevents <em>tampering</em>. It tells you the image was built by your pipeline and hasn't been swapped. It says nothing about whether the code is correct.")],
    cyoa_setup="An attacker compromises your CI credentials and pushes a malicious image to your registry under a legitimate tag. Your prod has a Kyverno admission policy requiring images to be signed by your team's Cosign key. <strong>Click to see what happens. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="at admission",
    cyoa_reveal="The malicious image isn't signed — the attacker had registry creds but not the Cosign key. Kubernetes refuses to admit the Pod. The incident is contained at the admission boundary, before any malicious code ran. Your incident retrospective is about why the CI creds were compromised, not about a breached cluster. <strong>Lesson:</strong> image signing turns a tag-swap from a breach into a denied admission.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Recipe</strong> = Dockerfile (or Buildpacks descriptor, ko config, etc.)</li>
      <li><strong>Oven</strong> = builder (BuildKit, Buildah, Kaniko, ko, Buildpacks)</li>
      <li><strong>Multi-stage process</strong> = builder stage + runtime stage</li>
      <li><strong>Cake base</strong> = base image (full distro vs alpine vs distroless vs scratch)</li>
      <li><strong>Ingredient list on the side</strong> = SBOM (SPDX, CycloneDX)</li>
      <li><strong>Baker's signature seal</strong> = image signing (cosign / sigstore)</li>
      <li><strong>Food safety inspection</strong> = vulnerability scanning (Trivy, Grype, Snyk)</li>
    </ul>
  </section>''',
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">An engineer wants to use <code>FROM ubuntu:latest</code> as the base for a Go app. Why is that wrong, and what should they use instead?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Two issues. (1) <code>:latest</code> is a moving tag — pin to a specific tag (<code>ubuntu:24.04</code>) or digest. (2) ubuntu (300 MB) is overkill for a Go app. Go binaries are statically linked — they need nothing from the OS. Use <code>FROM scratch</code> or <code>FROM gcr.io/distroless/static</code> in the runtime stage. Final image = just the Go binary. ~5-15 MB instead of 300+. Faster, safer, fewer CVEs.</div>
      </div>
    </div>
  </section>''',
)

LESSONS["L11"] = dict(
    file="preview-kubernetes-lesson-11.html",
    rail_key="L11", active_pin="kt-pin11", strip_key="L11",
    district_name="K-Town Bank Vault Quarter",
    strip_label_district="Bank Vault Quarter",
    strip_label_pos="lesson 11 of 16",
    a11y_phrase="Lesson 11 of 16, Bank Vault Quarter.",
    aria_label_today="K-Town district map: today we are at Bank Vault Quarter, Lesson 11",
    map_title_today="K-Town district map · today: K-Town Bank Vault Quarter",
    nightmare_text="Your web app gets compromised through an unsanitised input. The attacker gets a shell <em>as root</em> inside the container. They write a webshell to disk, escalate via a kernel CVE, pivot to the host, then to other Pods. By morning, your cluster is gone. The same bug, on a hardened Pod, is a Tuesday afternoon ticket. This lesson is the 12 lines of YAML that change which one happens.",
    stamp_takeaway="Where the image came from (auth + pull policy) plus how it runs (non-root, read-only, drop caps, seccomp) shrinks blast radius 10×.",
    pc1_q="Your image is in a private registry. Your Pod can't pull it (<code>ImagePullBackOff</code>). What's missing?",
    pc1_opts=[("a) The cluster doesn't have internet", False), ("b) An <code>imagePullSecret</code> with the registry credentials", True), ("c) The image doesn't exist", False)],
    pc1_feedback="<strong>Answer: b.</strong> The kubelet needs credentials to pull from private registries. Create a <code>kubernetes.io/dockerconfigjson</code> secret and reference it in the Pod spec via <code>imagePullSecrets</code>.",
    pc2_q="Pick the safest of these settings for a production Pod:",
    pc2_opts=[("a) Run as root, all capabilities, writable filesystem", False), ("b) Run as non-root (UID 1000), drop ALL caps, read-only filesystem, seccomp RuntimeDefault", True), ("c) Run as root, drop ALL caps", False)],
    pc2_feedback="<strong>Answer: b.</strong> Each of those settings shrinks the blast radius of a bug. Together they match the Pod Security Standards \"Restricted\" profile.",
    tl_rows=[("The bank vault", "The container registry (Docker Hub, GHCR, ECR, GCR, ACR, Harbor)"), ("The vault door", "Registry authentication"), ("The teller window", "The kubelet pulling on behalf of the Pod"), ("The customer's credentials", "<code>imagePullSecrets</code>"), ("The glass inspection booth", "The container runtime sandbox"), ("The visitor wristband", "Non-root user (<code>runAsUser: 1000</code>)"), ("The \"no tools allowed\" sign", "<code>capabilities.drop: [ALL]</code> + <code>allowPrivilegeEscalation: false</code>"), ("The sealed glass display case", "<code>readOnlyRootFilesystem: true</code>"), ("The security camera", "The seccomp profile (<code>RuntimeDefault</code>)"), ("The bank's security manager", "Pod Security Standards (Privileged / Baseline / Restricted)")],
    analogy_stops_text="The analogy stops here: a bank vault has one combination. A container has dozens of independent locks (each <code>securityContext</code> field). Skipping any one is leaving a door cracked.",
    misconceptions=[("Running as root inside a container is safe because the container is isolated.", "Container root + a kernel exploit = host root. Run as a non-root UID by default."), ("<code>imagePullPolicy: Always</code> is overkill.", "For mutable tags it's the only safe policy. For digest-pinned images, the question is moot — same digest, same content, every time."), ("Pod Security Standards are something you have to install.", "They're built into the Kubernetes API server (since 1.25). Apply via namespace labels — no third-party admission needed.")],
    cyoa_setup="A new dev tries to deploy a Pod with <code>securityContext: { privileged: true }</code> \"for easier debugging.\" Your namespace is labeled <code>pod-security.kubernetes.io/enforce: restricted</code>. <strong>Click to see what happens. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="at admission",
    cyoa_reveal="The API server rejects the Pod at admission with a clear message: <code>violates PodSecurity 'restricted:latest' — privileged is not allowed</code>. The conversation moves from \"let's just allow it\" to \"let's fix the actual debugging tooling.\" Defaults won. <strong>Lesson:</strong> opt-in security is opt-out reality. Set the namespace policy and let the API server hold the line.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Vault</strong> = container registry (Docker Hub, GHCR, ECR, GCR, ACR, Harbor)</li>
      <li><strong>Vault door</strong> = registry authentication</li>
      <li><strong>Teller window</strong> = kubelet pulling on behalf of the pod</li>
      <li><strong>Customer credentials</strong> = imagePullSecrets</li>
      <li><strong>Inspection booth</strong> = container runtime sandbox</li>
      <li><strong>Visitor wristband</strong> = non-root user (UID 1000)</li>
      <li><strong>"No tools allowed" sign</strong> = drop ALL capabilities, allowPrivilegeEscalation: false</li>
      <li><strong>Glass display case</strong> = readOnlyRootFilesystem: true</li>
      <li><strong>Security camera</strong> = seccomp profile (RuntimeDefault)</li>
      <li><strong>Bank security manager</strong> = Pod Security Standards (Privileged / Baseline / Restricted)</li>
      <li><strong>Vendor seal on the box</strong> = image signing (cosign — Lesson 10)</li>
    </ul>
  </section>''',
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">A team uses <code>image: my-app:v2</code> with <code>imagePullPolicy: IfNotPresent</code>. They re-push <code>v2</code> with a hotfix. Most pods keep running the OLD image. Why? What's the right fix going forward?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span><code>IfNotPresent</code> means "if the node already has an image with this tag locally cached, use it — don't re-pull." Most nodes had <code>v2</code> cached from earlier deploys, so they kept the old binary; only brand-new nodes pulled the hotfix. Two fixes: (1) Never re-push tags. Cut a fresh tag (<code>v2.1</code>) per change. (2) Pin to digest: <code>image: my-app@sha256:abc...</code> — digests are immutable. If you absolutely must mutate a tag, set <code>imagePullPolicy: Always</code> so every pod start re-validates against the registry.</div>
      </div>
    </div>
  </section>''',
)


LESSONS["L12"] = dict(
    file="preview-kubernetes-lesson-12.html",
    rail_key="L12", active_pin="kt-pin12", strip_key="L12",
    district_name="K-Town Harbour",
    strip_label_district="K-Town Harbour",
    strip_label_pos="lesson 12 of 16",
    a11y_phrase="Lesson 12 of 16, K-Town Harbour.",
    aria_label_today="K-Town district map: today we are at K-Town Harbour, Lesson 12",
    map_title_today="K-Town district map · today: K-Town Harbour",
    nightmare_text="It's 3 AM. Your deploy went out clean. But somehow 4% of customer orders vanished mid-checkout, and your logs just say <code>Killed</code>. By morning you have 47 angry support tickets and no idea which Pods got hit. This lesson is about why that happens — and the one line of YAML (<code>ENTRYPOINT [\"tini\", \"--\", ...]</code>) that prevents it.",
    stamp_takeaway="PID 1 inside your container has two jobs Linux normally hands to systemd — forward signals and reap zombies. Wrap your entrypoint in <code>tini</code>. Handle SIGTERM. Add a <code>preStop</code> sleep. Tune the grace period.",
    pc1_q="Your container's Dockerfile has <code>CMD [\"bash\", \"start.sh\"]</code> and <code>start.sh</code> runs <code>node server.js &amp;</code>. K8s sends SIGTERM. What happens?",
    pc1_opts=[("a) Node receives SIGTERM and shuts down gracefully", False), ("b) Bash (PID 1) receives it but doesn't forward it; Node never knows", True), ("c) Both processes get the signal", False)],
    pc1_feedback="<strong>Answer: b.</strong> Bash is PID 1 and doesn't forward signals to background children. Node never learns the Pod is shutting down. After 30s grace, SIGKILL. In-flight requests dropped.",
    pc2_q="During rolling updates, a small fraction of requests return 502 for a few seconds. Pods are healthy. The app handles SIGTERM correctly. What's the cause?",
    pc2_opts=[("a) The app is broken", False), ("b) Race condition: load balancer is still sending traffic to a Pod whose port has already closed", True), ("c) The cluster is overloaded", False)],
    pc2_feedback="<strong>Answer: b.</strong> The endpoints update is slower than the app's shutdown. Fix: add a <code>preStop</code> hook that sleeps 10s before SIGTERM is sent — gives the LB time to drain the Pod from rotation.",
    tl_rows=[("The captain on the bridge", "PID 1 (your <code>ENTRYPOINT</code> process)"), ("The crew at stations", "Child processes"), ("The lighthouse signal", "SIGTERM (the polite shutdown signal)"), ("The captain's megaphone", "Signal forwarding (PID 1 re-shouting SIGTERM to children)"), ("The roster log", "Zombie reaping (<code>waitpid</code> on each finished child)"), ("Crew re-assigned to PID 1", "Orphan processes adopted by PID 1"), ("The grace-period clock", "<code>terminationGracePeriodSeconds</code>"), ("Lights out", "SIGKILL (uncatchable, kernel-level)"), ("The pre-disembark announcement", "The <code>preStop</code> hook"), ("Hiring a professional captain", "Wrapping the entrypoint in <code>tini</code> / <code>dumb-init</code>")],
    analogy_stops_text="The analogy stops here: a real captain can refuse to leave port. PID 1 cannot refuse SIGKILL — it's uncatchable. The only way to leave on your own terms is to leave during the grace period.",
    misconceptions=[("SIGKILL is \"just a stronger SIGTERM.\"", "SIGKILL is uncatchable, kernel-level. Your app <em>cannot</em> clean up under SIGKILL — it just dies. That's why graceful shutdown matters."), ("<code>terminationGracePeriodSeconds</code> is a hint.", "It's a hard wall-clock timer. SIGKILL fires at the end. Tune it (60s, 300s) for slow shutdowns — databases, queue workers, big flushes."), ("Zombies are theoretical.", "A Java app spawning subprocesses without <code>waitpid()</code> will fill the PID table over hours. Real outage. <code>tini</code> solves it for free.")],
    cyoa_setup="You hire a rookie captain (<code>bash</code>) for your container ship. The lighthouse blinks SIGTERM. The captain… does nothing. He didn't think it applied to him. <strong>Click to see what happens to the crew. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="30 seconds later",
    cyoa_reveal="<pre>  harbour clock:  0s ───────────── 30s ───── 💀\n  crew status:    [loading]    [still loading]   [SIGKILL]\n  passengers:     ████████████████████ 47% lost</pre>The harbour waited the full 30-second grace, then pulled the gangway with SIGKILL. The crew never got the message and were still loading cargo when the lights went out. <strong>Fix:</strong> hire <code>tini</code> as your captain — he forwards every signal he receives, on time, every time. <code>ENTRYPOINT [\"tini\", \"--\", \"node\", \"server.js\"]</code>. One line.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Captain on the bridge</strong> = PID 1 (your ENTRYPOINT process)</li>
      <li><strong>Crew at stations</strong> = child processes</li>
      <li><strong>Lighthouse signal</strong> = SIGTERM from kubelet</li>
      <li><strong>Captain's megaphone</strong> = signal forwarding</li>
      <li><strong>Roster log</strong> = zombie reaping (waitpid)</li>
      <li><strong>Re-assigned crew</strong> = orphan processes adopted by PID 1</li>
      <li><strong>Grace period clock</strong> = terminationGracePeriodSeconds</li>
      <li><strong>Lights out</strong> = SIGKILL</li>
      <li><strong>Pre-disembark announcement</strong> = preStop hook</li>
      <li><strong>Hired professional captain</strong> = tini / dumb-init</li>
      <li><strong>Untrained captain</strong> = naive shell entrypoint that swallows signals</li>
    </ul>
  </section>''',
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">A Java app spawns subprocesses for thumbnail generation. Under sustained load, after ~2 hours, the pod returns "Resource temporarily unavailable" errors. Restarting clears it. What's happening and what's the permanent fix?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Zombie process accumulation. The Java app forks a subprocess for each thumbnail. Each subprocess exits quickly, but the JVM does not call <code>waitpid()</code> to collect them. Each becomes a zombie — a defunct process consuming a PID slot. After thousands of thumbnails, the process table is full and the kernel can't fork new processes → "Resource temporarily unavailable." Pod restart clears the table temporarily but the leak resumes. Real fix: use tini as PID 1. <code>ENTRYPOINT ["tini", "--", "java", "-jar", "app.jar"]</code>. tini reaps any zombie re-parented to it, including the JVM's abandoned children. Bonus: tini also gives you proper signal forwarding for graceful shutdown.</div>
      </div>
    </div>
  </section>''',
)

LESSONS["L13"] = dict(
    file="preview-kubernetes-lesson-13.html",
    rail_key="L13", active_pin="kt-pin13", strip_key="L13",
    district_name="K-Town International Airport",
    strip_label_district="K-Town International Airport",
    strip_label_pos="lesson 13 of 16",
    a11y_phrase="Lesson 13 of 16, K-Town International Airport.",
    aria_label_today="K-Town district map: today we are at K-Town International Airport, Lesson 13",
    map_title_today="K-Town district map · today: K-Town International Airport",
    nightmare_text="A network partition isolates 2 of your 3 etcd nodes from each other. Quorum is lost. The cluster goes read-only — no new Pods scheduled, no failover, no Deployments updated. Anything currently running keeps running, but the cluster is frozen in amber. You can't even apply the fix. This lesson is about the brain–muscle split that makes Kubernetes work, and where it breaks if you're not careful.",
    stamp_takeaway="Control plane decides; nodes execute. Five control-plane components, three node components, one API door between them. Memorise the 6-hop Pod-creation flow.",
    pc1_q="Which component is the <em>only door</em> into a Kubernetes cluster?",
    pc1_opts=[("a) etcd", False), ("b) The API server", True), ("c) The kubelet", False)],
    pc1_feedback="<strong>Answer: b.</strong> Every read, every write, every watch goes through the API server. Nothing talks to etcd directly. That's the design.",
    pc2_q="Your 3-member etcd cluster loses 2 nodes. What happens?",
    pc2_opts=[("a) The cluster keeps running normally", False), ("b) The cluster goes read-only — quorum lost", True), ("c) Kubernetes schedules new etcd Pods automatically", False)],
    pc2_feedback="<strong>Answer: b.</strong> 3 members tolerate 1 failure. Lose 2, you're below quorum. 5-member etcd tolerates 2 failures.",
    tl_rows=[("The control tower", "The control plane (the brain)"), ("Radio dispatch", "The API server (the only door)"), ("The flight-plan archive", "etcd (source of truth)"), ("The specialist controllers", "<code>kube-controller-manager</code> (reconciliation loops)"), ("The runway-assignment desk", "<code>kube-scheduler</code>"), ("The cloud liaison", "<code>cloud-controller-manager</code>"), ("A terminal building", "A worker node"), ("The gate manager", "The kubelet"), ("The ground-crew router", "<code>kube-proxy</code>"), ("The aircraft at the gate", "A Pod")],
    analogy_stops_text="The analogy stops here: an airport tower has one radio operator. The Kubernetes API server is replicated 3+ ways behind a load balancer — multiple operators, all serving the same view, any can fail.",
    misconceptions=[("The control plane runs your apps.", "Control plane decides; worker nodes run. In production they're usually different machines, often with taints to keep workloads off the CP."), ("Components talk directly to each other.", "Everything goes through the API server. The scheduler doesn't tell the kubelet anything — it writes a Binding; the kubelet's watch picks it up."), ("Self-managed Kubernetes is \"more flexible.\"", "For most teams under 50 engineers, managed (EKS / GKE / AKS) is a no-brainer. Self-managed wins for specific cases: bare metal, regulated environments, or 100+ clusters.")],
    cyoa_setup="You run <code>kubectl apply -f pod.yaml</code>. <strong>Click to trace exactly what happens. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="trace",
    cyoa_reveal="<pre>  1. kubectl  → API server     (POST /api/v1/.../pods)\n  2. API srvr → etcd           (validate, persist)\n  3. scheduler watches API     (picks node-3, POSTs Binding)\n  4. kubelet on node-3 watches (sees its Pod)\n  5. kubelet  → runtime        (pull image, start)\n  6. kubelet  → API server     (PATCH status: Running)</pre>Notice every hop routes through the API server. The scheduler never tells the kubelet anything directly. <strong>That single-door discipline is the architectural constraint that makes K8s scale.</strong>",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Control tower</strong> = control plane (the brain)</li>
      <li><strong>Radio dispatch</strong> = API server (the only door)</li>
      <li><strong>Flight plan archive</strong> = etcd (source of truth)</li>
      <li><strong>Specialist controllers</strong> = controller manager (reconcile loops)</li>
      <li><strong>Runway assignment desk</strong> = scheduler</li>
      <li><strong>Cloud liaison</strong> = cloud-controller-manager</li>
      <li><strong>Terminal building</strong> = worker node</li>
      <li><strong>Gate manager</strong> = kubelet</li>
      <li><strong>Ground crew router</strong> = kube-proxy</li>
      <li><strong>Tug operator</strong> = container runtime</li>
      <li><strong>Aircraft at the gate</strong> = pod</li>
    </ul>
  </section>''',
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">A 12-engineer startup is debating between keeping their kubeadm-managed K8s on EC2 or migrating to GKE. They spend ~30 hours/month on cluster ops. Make the case.</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Managed (GKE/EKS/AKS) wins almost every time at this scale. Cost math: 30 eng-hours/month × ~$87/hr fully-loaded = $2,610/month in eng time on cluster ops. GKE control plane is ~$73/cluster/month. Net savings: ~$2,500/month, plus better security patching, faster CP version upgrades, and etcd backups handled by SREs who do this all day. Self-managed wins when: you need a CP version not yet supported by the managed offering, you need physical control of etcd (regulatory), you're on bare metal where no managed option exists, you have hundreds of clusters and per-cluster cost adds up, or cluster ops is genuinely a core competency. For 12 engineers shipping product, managed is a no-brainer.</div>
      </div>
    </div>
  </section>''',
)

LESSONS["L14"] = dict(
    file="preview-kubernetes-lesson-14.html",
    rail_key="L14", active_pin="kt-pin14", strip_key="L14",
    district_name="City Hall — Permit Office",
    strip_label_district="Permit Office",
    strip_label_pos="lesson 14 of 16",
    a11y_phrase="Lesson 14 of 16, City Hall Permit Office.",
    aria_label_today="K-Town district map: today we are at City Hall — Permit Office, Lesson 14",
    map_title_today="K-Town district map · today: City Hall — Permit Office",
    nightmare_text="An engineer ran <code>kubectl scale deployment api --replicas=10</code> to handle a slow service. It worked. Three days later, a CI deploy from the git-tracked YAML (which still says <code>replicas: 3</code>) ran. <code>apply</code> diffed, scaled DOWN to 3 mid-traffic-spike. 5xx surge. This lesson is about why imperative kubectl is dangerous, and why every K8s object has the same 4-section permit form.",
    stamp_takeaway="Every K8s object is the same 4-block form (<code>apiVersion + kind + metadata + spec</code>). <code>kubectl explain</code> is the manual. Never use imperative kubectl in production. CRDs make custom types first-class.",
    pc1_q="Which of these is <em>not</em> a mandatory block in every Kubernetes YAML?",
    pc1_opts=[("a) <code>apiVersion</code>", False), ("b) <code>status</code>", True), ("c) <code>metadata</code>", False)],
    pc1_feedback="<strong>Answer: b.</strong> <code>status</code> is filled in by controllers, not by you. The four mandatory blocks are <code>apiVersion</code>, <code>kind</code>, <code>metadata</code>, <code>spec</code>.",
    pc2_q="You don't know if <code>replicaCount</code> or <code>replicas</code> is the right field name. What's the fastest way to find out?",
    pc2_opts=[("a) Google it", False), ("b) <code>kubectl explain deployment.spec</code> — the cluster's own schema", True), ("c) Read the source code", False)],
    pc2_feedback="<strong>Answer: b.</strong> Your cluster ships with the manual built in. Reflects the <em>exact</em> version you're running, including any CRDs.",
    tl_rows=[("The permit office", "The Kubernetes API server"), ("The standard 4-section permit form", "Every K8s object's structure"), ("The type declaration at the top", "<code>apiVersion</code> + <code>kind</code>"), ("The identity section", "<code>metadata</code>"), ("The \"what-you-want\" section", "<code>spec</code>"), ("The inspector's stamp", "<code>status</code> (filled in by controllers, not by you)"), ("The handbook on the desk", "<code>kubectl explain</code>"), ("The filing cabinet", "etcd"), ("Bringing in a filled-out form", "<code>kubectl apply -f</code>"), ("A custom permit template plus its own inspector", "A CRD plus a controller (the operator pattern)")],
    analogy_stops_text="The analogy stops here: a permit office has business hours. The Kubernetes API server is always open and serves thousands of requests per second.",
    misconceptions=[("CRDs are second-class objects.", "Once registered, they get the same RBAC, audit, validation, and storage as built-ins. cert-manager's <code>Certificate</code> and a Pod are equivalent in the API server's eyes."), ("<code>kubectl run</code> and <code>kubectl create</code> are the right way to deploy.", "Those are imperative — direct mutations with no audit trail. Production should always use <code>kubectl apply -f</code> (and ideally GitOps on top)."), ("Labels and annotations are interchangeable.", "Labels are <em>indexed</em> and used for selection (<code>-l app=foo</code>). Annotations are free-form metadata, not selectable. If you'd ever filter by it, it's a label.")],
    cyoa_setup="Your YAML has <code>replicaCount: 3</code> (the right field is <code>replicas</code>). You run <code>kubectl apply --dry-run=client</code>. It passes. You commit. <strong>Click to see what happens at deploy. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="at deploy",
    cyoa_reveal="<code>--dry-run=client</code> only does shallow client-side validation — it doesn't know your cluster's actual schema. The deploy goes to prod. The API server rejects: <code>unknown field \"spec.replicaCount\"</code>. CI fails. Incident. <strong>Fix:</strong> always use <code>kubectl apply --server-side --dry-run=server</code> in CI. That talks to the actual API server and catches typos like this — including CRD-specific fields client-side validation misses.",
    old_mapping_block='''    <p style="margin-top:18px"><strong>The mapping:</strong></p>
    <ul style="font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 0">
      <li><strong>Permit office</strong> = the Kubernetes API server</li>
      <li><strong>Standard 4-section form</strong> = the structure of every K8s object</li>
      <li><strong>Type declaration at top</strong> = <code>apiVersion</code> + <code>kind</code></li>
      <li><strong>Identity section</strong> = <code>metadata</code></li>
      <li><strong>What-you-want section</strong> = <code>spec</code></li>
      <li><strong>Inspector's stamp</strong> = <code>status</code></li>
      <li><strong>Different counters</strong> = API groups</li>
      <li><strong>Clerk validating</strong> = server-side OpenAPI validation</li>
      <li><strong>Filing cabinet</strong> = etcd</li>
      <li><strong>Handbook on the desk</strong> = <code>kubectl explain</code></li>
      <li><strong>Custom permit template</strong> = CRD</li>
      <li><strong>Custom inspector</strong> = your operator</li>
      <li><strong>Bringing in a filled form</strong> = <code>kubectl apply</code></li>
      <li><strong>Asking the clerk to fill it for you</strong> = <code>kubectl create</code> (imperative)</li>
      <li><strong>Colored sticker on the form</strong> = labels (used to file &amp; find)</li>
      <li><strong>Sticky notes</strong> = annotations (humans read, system ignores for selection)</li>
    </ul>
  </section>''',
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">Your team uses cert-manager. You can run <code>kubectl apply -f certificate.yaml</code>, <code>kubectl get certificates</code>, even <code>kubectl describe certificate my-cert</code>. But Certificate isn't a built-in K8s type. How does this work?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>cert-manager ships two things. (1) A <strong>CRD</strong> registers <code>Certificate</code> as a new type with your cluster's API server. The CRD YAML defines the schema (fields, types, validation rules). Once applied, the API server starts serving <code>/apis/cert-manager.io/v1/certificates</code> with full RBAC, audit, kubectl support — identical to built-in types. (2) A <strong>controller</strong> (the cert-manager pod) watches Certificate objects and reconciles: talks to Let's Encrypt, completes ACME challenges, fetches certs, writes a Secret, schedules renewals. CRD + controller = the operator pattern. Argo CD (Application), Crossplane, Istio (VirtualService), Prometheus Operator — all the same shape. Roll your own with kubebuilder or operator-sdk.</div>
      </div>
    </div>
  </section>''',
)


# ----------- which lessons to process this run -----------

ENABLED = ["L12", "L13", "L14"]


def main() -> None:
    for key in ENABLED:
        L = LESSONS[key]
        print(f"=== {key} ({L['file']}) ===")
        transform(L)
    print("Done.")


if __name__ == "__main__":
    main()
