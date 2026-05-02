#!/usr/bin/env python3
"""K-Town revision — Phase 5 batch 1 (L02, L03, L04).

Applies the layman-first scaffolding component family to L02, L03, L04
in one pass. Reads the canonical CSS block and K-Town map body from
L01 (preview-kubernetes-lesson-01.html) and rewrites each target lesson
with: scaffolding CSS, concept rail, district line, K-Town map (with
correct active pin), Nightmare opener, top stamp, two pause-and-checks,
Translation Legend (replaces the existing 'The mapping:' list), the
analogy-stops-here callout, Misconceptions panel inside Section 7, a
CYOA quiz card replacing the existing third scenario question, the
bottom stamp, and the smarter quiz-reveal + pause-check JS handlers.

This script is idempotent in the sense that running it twice will fail
on the second run (the second pass will fail to find anchors that the
first pass replaced), which is the safe behavior we want.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------- helpers ----------

def replace_once(content: str, old: str, new: str, label: str) -> str:
    if old not in content:
        sys.exit(f"[{label}] anchor not found.\n--- expected ---\n{old[:300]}\n----------------")
    if content.count(old) > 1:
        sys.exit(f"[{label}] anchor matched {content.count(old)} times — not unique.")
    return content.replace(old, new, 1)


# ---------- extract reusable blocks from L01 ----------

L01_PATH = os.path.join(ROOT, "preview-kubernetes-lesson-01.html")
L01 = open(L01_PATH).read()

# CSS scaffolding block: from the LAYMAN-FIRST comment to (but not including) </style>
css_start = L01.index("  /* ============ LAYMAN-FIRST")
css_end = L01.index("</style>", css_start)
CSS_BLOCK = L01[css_start:css_end]

# K-Town map SVG body: from <svg ... class="ktown-map" ... up to and including </svg>
svg_start = L01.index('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" class="ktown-map"')
svg_end = L01.index("</svg>", svg_start) + len("</svg>")
KTOWN_SVG = L01[svg_start:svg_end]


def map_with_active(active_pin_id: str) -> str:
    """Return the K-Town SVG with `active` class moved to active_pin_id.

    Mayor's Office (kt-pin01) keeps the pin-anchor class but loses `active`
    unless active_pin_id == 'kt-pin01'.
    """
    svg = KTOWN_SVG
    # Reset L01: drop the `active` from the anchor pin
    svg = svg.replace(
        '<g class="pin pin-anchor active" id="kt-pin01"',
        '<g class="pin pin-anchor" id="kt-pin01"',
    )
    if active_pin_id == "kt-pin01":
        # restore active on the anchor
        return svg.replace(
            '<g class="pin pin-anchor" id="kt-pin01"',
            '<g class="pin pin-anchor active" id="kt-pin01"',
        )
    if active_pin_id == "kt-pin7-5":
        return svg.replace(
            '<g class="pin pin-primer" id="kt-pin7-5"',
            '<g class="pin pin-primer active" id="kt-pin7-5"',
        )
    # Standard pin
    pattern = f'<g class="pin" id="{active_pin_id}"'
    repl = f'<g class="pin active" id="{active_pin_id}"'
    if pattern not in svg:
        sys.exit(f"map_with_active: pin {active_pin_id} not found")
    return svg.replace(pattern, repl, 1)


# ---------- per-lesson data ----------

# Concept rail items in lesson order. Each is (icon-default, label, primer?)
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

# Lesson curriculum order in the dot-strip (matches the K-Town map's pin order
# but in lesson sequence). 1-indexed.
STRIP_ORDER = [
    "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L7-5",
    "L08", "L09", "L10", "L11", "L12", "L13", "L14", "L15",
]


def concept_rail_html(current: str) -> str:
    """Build the concept rail with `current` marked active and earlier items done."""
    cur_idx = next(i for i, (k, _, _) in enumerate(CONCEPT_RAIL_ITEMS) if k == current)
    out = ['<aside class="concept-rail" aria-label="Concept journey through the Kubernetes course">',
           '  <span class="concept-rail-title">Concept journey</span>']
    for i, (key, label, primer) in enumerate(CONCEPT_RAIL_ITEMS):
        primer_cls = " primer" if primer else ""
        if i < cur_idx:
            icon = "✓"
            cls = " done"
            out.append(f'  <div class="concept-rail-item{cls}{primer_cls}"><span class="concept-rail-icon">{icon}</span><span>{label}</span></div>')
        elif i == cur_idx:
            icon = "▶"
            cls = " current"
            out.append(f'  <div class="concept-rail-item{cls}{primer_cls}"><span class="concept-rail-icon">{icon}</span><span>{label}</span><span class="concept-rail-here">← you are here</span></div>')
        else:
            icon = "○"
            cls = ""
            out.append(f'  <div class="concept-rail-item{cls}{primer_cls}"><span class="concept-rail-icon">{icon}</span><span>{label}</span></div>')
    out.append('</aside>')
    return "\n".join(out)


def strip_html(active_key: str) -> str:
    """Build the dot-strip <ol> with anchor at position 1 and active at active_key's position."""
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


# ----------- per-lesson content -----------

LESSONS = {}

LESSONS["L02"] = dict(
    file="preview-kubernetes-lesson-02.html",
    rail_key="L02",
    active_pin="kt-pin02",
    strip_key="L02",
    district_name="Residential District",
    strip_label_district="Residential District",
    strip_label_pos="lesson 2 of 16",
    a11y_phrase="Lesson 2 of 16, Residential District.",
    aria_label_today="K-Town district map: today we are at Residential District, Lesson 02",
    map_title_today="K-Town district map · today: Residential District",
    nightmare_text="Your team needs to ship 60 microservices. Each one runs in its own virtual machine. Each VM carries a full operating system — that's 60 copies of Linux, hogging RAM and disk. Booting one takes minutes. Cold starts during traffic spikes are the difference between a sale and a lost customer. This lesson is about the lighter alternative — and why Kubernetes was built on top of it.",
    stamp_takeaway="VMs are houses (own everything, heavy). Containers are apartments (shared building, light).",
    pc1_q="A VM image is typically 5–20 GB. A container image is typically 10–500 MB. Why the gap?",
    pc1_opts=[
        ("a) Containers compress better", False),
        ("b) A VM ships a whole operating system inside; a container ships only the app", True),
        ("c) Containers store fewer files", False),
    ],
    pc1_feedback="<strong>Answer: b.</strong> The OS-shaped chunk is what's missing.",
    pc2_q="A bank wants to run apps for three competing customers on the same hardware. The customers don't trust each other. VMs or containers?",
    pc2_opts=[
        ("a) Containers — they're faster", False),
        ("b) VMs (or sandboxed runtimes like gVisor) — separate kernels per customer", True),
        ("c) Either is fine", False),
    ],
    pc2_feedback="<strong>Answer: b.</strong> Plain containers share the host kernel. A kernel exploit in one customer's container could reach others. VMs give each customer their own kernel — much stronger isolation.",
    tl_rows=[
        ("Each house", "One virtual machine (VM)"),
        ("Each apartment", "One container"),
        ("The building's shared infrastructure (foundation, heating, plumbing)", "The host operating system's kernel"),
        ("The land underneath", "The physical hardware"),
        ("The walls between apartments", "Linux namespaces and cgroups"),
    ],
    analogy_stops_text="The analogy stops here: unlike apartments, you can run thousands of containers on one computer. The plumbing doesn't get clogged.",
    misconceptions=[
        ("A container has its own operating system.", "It shares the host's kernel. The \"OS-like\" feel is a private view, not a real second OS."),
        ("Containers replaced VMs.", "They're complementary. Most cloud Kubernetes runs containers <em>inside</em> VMs the cloud provides."),
        ("Containers are unsafe because they share a kernel.", "They're safe enough for trusting tenants. For hostile multi-tenancy, use VMs or sandboxed runtimes (gVisor, Kata)."),
    ],
    cyoa_setup="You're running a CI system. Every commit triggers 50,000 test jobs per day. You build it on VMs, because \"VMs are isolated and safe.\" <strong>Click to see what happens to your bill. ▼</strong>",
    cyoa_button="Show what happened",
    cyoa_tag_text="months later",
    cyoa_reveal="Each VM takes 90 seconds to boot. Each test takes 30 seconds. So 75% of your CI time and budget is spent waiting for VMs to boot. Containers boot in milliseconds. Switching cuts your CI bill by ~70% and triples throughput. <strong>Lesson:</strong> pick the lighter unit when the workload churns.",
    # The exact existing text we need to replace
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
    old_section7_intro='''  <section class="s">
    <span class="s-eyebrow">Section 7 · Flashcards &amp; quiz</span>
    <h2>Lock it in</h2>
    <p>Eight flashcards on the key terms, then three quick questions.</p>

    <div class="flashcard-grid">''',
)

LESSONS["L03"] = dict(
    file="preview-kubernetes-lesson-03.html",
    rail_key="L03",
    active_pin="kt-pin03",
    strip_key="L03",
    district_name="Climate Control Tower",
    strip_label_district="Climate Control Tower",
    strip_label_pos="lesson 3 of 16",
    a11y_phrase="Lesson 3 of 16, Climate Control Tower.",
    aria_label_today="K-Town district map: today we are at Climate Control Tower, Lesson 03",
    map_title_today="K-Town district map · today: Climate Control Tower",
    nightmare_text="Your deploy script has 200 lines of bash. Step 4 runs <code>ssh</code> to 30 servers. Tonight, on server 17, step 4 fails — and you have no idea what state servers 1–16 are in, or 18–30. Are they on the new version? The old? Half each? You can't tell without looking. The script can't recover; it just stopped. This lesson is about the model that makes that whole class of problem go away.",
    stamp_takeaway="Kubernetes is a thermostat. You set what you want; controllers watch forever; gaps close automatically. Everything else in the course is a variation of this loop.",
    pc1_q="Your YAML says <code>replicas: 3</code>. A Pod crashes. Now 2 are running. What does the controller do?",
    pc1_opts=[
        ("a) Sends an email", False),
        ("b) Notices the gap (3 ≠ 2) and starts a 3rd Pod on a healthy node", True),
        ("c) Updates the YAML to say <code>replicas: 2</code>", False),
    ],
    pc1_feedback="<strong>Answer: b.</strong> The controller is constantly comparing desired (3) to actual (2). When they differ, it acts. Forever. That's the loop.",
    pc2_q="Imperative vs declarative — which one is Kubernetes?",
    pc2_opts=[
        ("a) Imperative: \"do step 1, then step 2, then step 3\"", False),
        ("b) Declarative: \"I want this end state; figure it out\"", True),
        ("c) Both", False),
    ],
    pc2_feedback="<strong>Answer: b.</strong> You write the goal; controllers figure out the steps. That's why K8s recovers from failures — it doesn't have a \"step 4 failed\" problem because there's no fixed step 4.",
    tl_rows=[
        ("The thermostat dial", "Your YAML manifest <em>(desired state)</em>"),
        ("The room", "Your live cluster <em>(actual state)</em>"),
        ("The thermostat brain", "A controller"),
        ("The thermometer", "The cluster reporting actual state"),
        ("The heater firing", "The controller acting (start a Pod, scale up, restart)"),
        ("\"Never stops watching\"", "The reconciliation loop"),
    ],
    analogy_stops_text="The analogy stops here: a real thermostat watches one thing — temperature. Kubernetes runs many \"thermostats\" at once, one per resource type, all in parallel.",
    misconceptions=[
        ("The reconciliation loop runs once and stops when everything matches.", "It never stops. When the gap is zero it idles, but it keeps watching. The moment something drifts (a crash, a manual edit), the loop fires again."),
        ("Declarative means \"I never write any logic.\"", "You still write a correct spec. If the YAML says \"3 copies of a broken app,\" you'll get 3 copies of a broken app — restarted forever."),
        ("There's one big controller in Kubernetes.", "There are dozens, each watching one type of resource (Deployments, Services, Jobs…), all running the same loop pattern in parallel."),
    ],
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
    # L03's third quiz card is the "treat servers as cattle" one — replace with CYOA
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">Why is "treat servers as cattle" a reliability strategy, not just a fashion statement?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Because if every server is hand-tuned (a "pet"), losing one means losing knowledge. Documentation is always incomplete. Recovery means a human reverse-engineering what made that server special. If servers are interchangeable cattle described declaratively, losing one is a non-event — the controller starts another from the same spec. Reliability scales because nothing depends on a specific machine surviving.</div>
      </div>
    </div>
  </section>''',
    old_section7_intro=None,  # will be discovered
)

LESSONS["L04"] = dict(
    file="preview-kubernetes-lesson-04.html",
    rail_key="L04",
    active_pin="kt-pin04",
    strip_key="L04",
    district_name="Port + Restaurant Row",
    strip_label_district="Port + Restaurant Row",
    strip_label_pos="lesson 4 of 16",
    a11y_phrase="Lesson 4 of 16, Port and Restaurant Row.",
    aria_label_today="K-Town district map: today we are at Port + Restaurant Row, Lesson 04",
    map_title_today="K-Town district map · today: Port + Restaurant Row",
    nightmare_text="You're moving an app to Kubernetes. The app reads its database password from a file at <code>/etc/myapp/db.conf</code>, written by a Chef recipe at server-provisioning time. You bring it up in a Kubernetes Pod. The file isn't there. The app crashes on startup. Pods are temporary; Pod filesystems disappear. Your weekend is gone. This lesson is about the 12 rules that prevent you from ever fighting the platform like this again.",
    stamp_takeaway="A 12-factor app is a standard shipping container — drops cleanly into any platform. Microservices vs monoliths is about size, not virtue. Most teams should start with a modular monolith.",
    pc1_q="Where should an app's database password live?",
    pc1_opts=[
        ("a) Hardcoded in source code", False),
        ("b) In a file under <code>/etc/</code> written by a Chef recipe", False),
        ("c) In an environment variable, injected by the platform", True),
    ],
    pc1_feedback="<strong>Answer: c.</strong> Factor 3 (Config) — env vars, never code, never baked-in files. Same image, different config per environment.",
    pc2_q="A 6-engineer startup is debating \"should we start with microservices or a monolith?\"",
    pc2_opts=[
        ("a) Microservices — that's how Netflix did it", False),
        ("b) Modular monolith — clear boundaries, simple ops", True),
        ("c) Doesn't matter", False),
    ],
    pc2_feedback="<strong>Answer: b.</strong> Microservices push complexity from the codebase to the network: tracing, retries, timeouts, separate dashboards, separate on-call. A 6-engineer team rarely has the operational maturity for that. Start with a modular monolith; split a service out only when scale or team boundaries clearly demand it.",
    tl_rows=[
        ("A standard ISO shipping container", "A 12-factor app"),
        ("A custom crate (barrels, bales)", "A pre-12-factor app needing custom platform handling"),
        ("A single restaurant", "A monolith"),
        ("A restaurant with specialty stations", "A modular monolith"),
        ("A food court of stalls", "Microservices"),
    ],
    analogy_stops_text="The analogy stops here: standard shipping containers are 20 or 40 feet long. Software containers are whatever size you make them — the \"standard\" is the interface, not the dimensions.",
    misconceptions=[
        ("Microservices are always better than monoliths.", "They're an answer to <em>organisational scale</em>, not a starting architecture. Shopify runs hundreds of engineers on one Rails monolith — and ships daily."),
        ("12-factor is just a coding style.", "It's the contract between your app and any modern platform. Violating it doesn't fail tests — it fails Tuesday afternoons in production."),
        ("Stateless means \"the app doesn't store anything.\"", "Stateless means <em>the process</em> doesn't hold important state in memory. State lives in attached backing services — Postgres, Redis, S3 — that survive restarts."),
    ],
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
    # L04's third quiz card is "log to stdout (Factor 11)" — replace with CYOA
    old_third_quiz='''      <div class="quiz-card">
        <p class="quiz-prompt">Why is "log to stdout" (Factor 11) a 12-factor rule rather than just a personal preference?</p>
        <button class="quiz-reveal" type="button">Show answer</button>
        <div class="quiz-answer"><span class="quiz-answer-tag">answer</span>Because writing logs to a file on the pod's local disk fights the platform — that disk disappears when the pod restarts, log rotation needs separate cron jobs, and you've coupled your app to filesystem-specific assumptions. Writing to stdout lets the platform (Kubernetes, Heroku, whatever) capture logs uniformly, ship them to centralized aggregation, and rotate/retain them as policy demands. Your app stays generic; the platform handles log lifecycle.</div>
      </div>
    </div>
  </section>''',
    old_section7_intro=None,
)


# ----------- HTML builders -----------

def build_district_line(name: str) -> str:
    return f'<p class="district-line">📍 Today\'s stop in K-Town: <strong>{name}</strong>.</p>'


def build_map_block(L: dict) -> str:
    svg = map_with_active(L["active_pin"])
    # Update the inline title and aria-label on the SVG root for this lesson
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


# ----------- discover Section 7 intro per lesson -----------

# All three lessons follow a similar pattern but the intro paragraph wording varies.
# Find the actual existing block in each file at runtime.
SECTION7_INTRO_PATTERN = re.compile(
    r'  <section class="s">\n'
    r'    <span class="s-eyebrow">Section 7 · Flashcards &amp; quiz</span>\n'
    r'    <h2>([^<]+)</h2>\n'
    r'    <p>([^<]+)</p>\n'
    r'\n'
    r'    <div class="flashcard-grid">'
)


# ----------- transform a lesson -----------

def transform(L: dict) -> None:
    path = os.path.join(ROOT, L["file"])
    content = open(path).read()

    if "LAYMAN-FIRST SCAFFOLDING" in content:
        sys.exit(f"{L['file']}: already has scaffolding block. Aborting (idempotency).")

    # 1. Insert CSS block before </style>
    content = replace_once(
        content,
        "</style>",
        CSS_BLOCK + "</style>",
        f"{L['file']} CSS",
    )

    # 2. Insert concept rail before <header class="topbar">
    rail = concept_rail_html(L["rail_key"])
    content = replace_once(
        content,
        '<body data-theme="light">\n\n<header class="topbar">',
        f'<body data-theme="light">\n\n{rail}\n\n<header class="topbar">',
        f"{L['file']} concept rail",
    )

    # 3. Insert district line + K-Town map between </header> and <main>
    district = build_district_line(L["district_name"])
    map_block = build_map_block(L)
    content = replace_once(
        content,
        "</header>\n\n<main>",
        f"</header>\n\n{district}\n\n{map_block}\n\n<main>",
        f"{L['file']} district + map",
    )

    # 4. Insert Nightmare + top stamp between hero close and Section 1
    nightmare = build_nightmare(L["nightmare_text"])
    stamp_top = build_stamp(L["stamp_takeaway"], "top placement")
    content = replace_once(
        content,
        '  </section>\n\n  <!-- ============================== SECTION 1 — CONCEPT ============================== -->',
        f'  </section>\n\n{nightmare}\n\n{stamp_top}\n\n  <!-- ============================== SECTION 1 — CONCEPT ============================== -->',
        f"{L['file']} Nightmare + top stamp",
    )

    # 5. Insert pause-and-check #1 between Section 1 close and Section 2 marker
    pc1 = build_pause_check("Pause-and-check #1 · after Section 1", L["pc1_q"], L["pc1_opts"], L["pc1_feedback"])
    content = replace_once(
        content,
        '  </section>\n\n  <!-- ============================== SECTION 2 — BEFORE / AFTER ============================== -->',
        f'  </section>\n\n{pc1}\n\n  <!-- ============================== SECTION 2 — BEFORE / AFTER ============================== -->',
        f"{L['file']} pause-check #1",
    )

    # 6. Replace the "The mapping:" block with Translation Legend + analogy-stops
    legend = build_translation_legend(L["tl_rows"], L["analogy_stops_text"])
    content = replace_once(
        content,
        L["old_mapping_block"],
        legend,
        f"{L['file']} translation legend",
    )

    # 7. Insert pause-and-check #2 between Section 4 close and Section 5 marker
    pc2 = build_pause_check("Pause-and-check #2 · after Section 4", L["pc2_q"], L["pc2_opts"], L["pc2_feedback"])
    content = replace_once(
        content,
        '  </section>\n\n  <!-- ============================== SECTION 5 — REAL-WORLD ============================== -->',
        f'  </section>\n\n{pc2}\n\n  <!-- ============================== SECTION 5 — REAL-WORLD ============================== -->',
        f"{L['file']} pause-check #2",
    )

    # 8. Update Section 7 eyebrow + intro + insert misconceptions panel
    m = SECTION7_INTRO_PATTERN.search(content)
    if not m:
        sys.exit(f"{L['file']}: Section 7 intro pattern not found.")
    h2_text = m.group(1)
    intro_text = m.group(2)
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

    # 9. Replace third quiz card with CYOA
    cyoa = build_cyoa(L)
    content = replace_once(content, L["old_third_quiz"], cyoa, f"{L['file']} CYOA")

    # 10. Insert bottom stamp between glossary close and recap section
    stamp_bottom = build_stamp(L["stamp_takeaway"], "bottom placement (identical to top)")
    content = replace_once(
        content,
        '  </details>\n\n  <!-- ============================== RECAP + COMPLETION ============================== -->',
        f'  </details>\n\n{stamp_bottom}\n\n  <!-- ============================== RECAP + COMPLETION ============================== -->',
        f"{L['file']} bottom stamp",
    )

    # 11. Update JS handler
    content = replace_once(content, JS_OLD, JS_NEW, f"{L['file']} JS")

    open(path, "w").write(content)
    print(f"  {L['file']}: rewritten ({len(content):,} bytes)")


def main():
    for key in ("L02", "L03", "L04"):
        L = LESSONS[key]
        print(f"=== {key} ({L['file']}) ===")
        transform(L)
    print("Done.")


if __name__ == "__main__":
    main()
