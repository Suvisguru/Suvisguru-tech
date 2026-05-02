from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Switchboard security wing: a hierarchy of policy panels — AdminNetworkPolicy (admin-tier hard rules), NetworkPolicy (team-tier additive), BaselineAdminNetworkPolicy (admin defaults), and a separate FQDN block listing api.openai.com, github.com, with one blocked.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">SWITCHBOARD · POLICY WING (ADMIN VS TEAM)</text>
  <!-- ANP layer -->
  <g transform="translate(40,55)">
    <rect width="280" height="50" rx="6" fill="#A04832" stroke="#1B1814" stroke-width="2"/>
    <text x="140" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">ADMIN NETWORK POLICY</text>
    <text x="140" y="36" text-anchor="middle" font-size="8" fill="#FBE8DC">priority 100 · DENY everything to namespace X</text>
    <text x="140" y="46" text-anchor="middle" font-size="7" fill="#FBE8DC" font-style="italic">admin can override · evaluated FIRST</text>
  </g>
  <!-- NP layer -->
  <g transform="translate(40,115)">
    <rect width="280" height="40" rx="6" fill="#5A9F7A" stroke="#3D7857" stroke-width="1.5"/>
    <text x="140" y="18" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">NetworkPolicy (NPv1)</text>
    <text x="140" y="32" text-anchor="middle" font-size="8" fill="#FFFFFF">team allow: from frontend → backend</text>
  </g>
  <!-- BANP -->
  <g transform="translate(40,165)">
    <rect width="280" height="35" rx="6" fill="#3F4A5E" stroke="#1B1814" stroke-width="1.5" stroke-dasharray="3,2"/>
    <text x="140" y="18" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">BaselineAdminNetworkPolicy</text>
    <text x="140" y="30" text-anchor="middle" font-size="7" fill="#FBF1D6" font-style="italic">cluster default · evaluated LAST · team can override</text>
  </g>
  <!-- FQDN block -->
  <g transform="translate(360,55)">
    <rect width="280" height="145" rx="6" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="140" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#5A4F45">EGRESS · FQDN ALLOW LIST</text>
    <rect x="14" y="22" width="252" height="22" rx="2" fill="#E0EFE6" stroke="#3D7857" stroke-width="1"/>
    <text x="20" y="36" font-size="8" font-weight="700" fill="#3D7857">✓ api.openai.com</text>
    <text x="260" y="36" text-anchor="end" font-size="7" fill="#5A4F45">443</text>
    <rect x="14" y="48" width="252" height="22" rx="2" fill="#E0EFE6" stroke="#3D7857" stroke-width="1"/>
    <text x="20" y="62" font-size="8" font-weight="700" fill="#3D7857">✓ github.com</text>
    <text x="260" y="62" text-anchor="end" font-size="7" fill="#5A4F45">443</text>
    <rect x="14" y="74" width="252" height="22" rx="2" fill="#E0EFE6" stroke="#3D7857" stroke-width="1"/>
    <text x="20" y="88" font-size="8" font-weight="700" fill="#3D7857">✓ *.amazonaws.com</text>
    <text x="260" y="88" text-anchor="end" font-size="7" fill="#5A4F45">443</text>
    <rect x="14" y="100" width="252" height="22" rx="2" fill="#FBE8DC" stroke="#A04832" stroke-width="1.2"/>
    <text x="20" y="114" font-size="8" font-weight="700" fill="#A04832">✗ pastebin.com</text>
    <text x="260" y="114" text-anchor="end" font-size="7" fill="#A04832">DENY</text>
    <text x="140" y="138" text-anchor="middle" font-size="7" fill="#5A4F45" font-style="italic">CIDR rules can't express this — FQDN can</text>
  </g>
  <text x="340" y="217" text-anchor="middle" font-size="0" fill="#3F4A5E"></text>
</svg>"""

LESSON = LessonSpec(
    num="26",
    title_short="AdminNetworkPolicy",
    title_full="AdminNetworkPolicy & FQDN-Based Egress",
    title_html="Lesson 26 — AdminNetworkPolicy & FQDN Policies · K-COM",
    module_eyebrow="Module 12 · Lesson 26 · the policy hierarchy NetworkPolicy never had",
    hero_sub_html='<code>NetworkPolicy</code> (covered in Lesson 17) is app-team-owned, additive-only, no priority. There\'s no way for an admin to say "absolutely no egress from this namespace." That gap is now filled by <strong>AdminNetworkPolicy</strong> (ANP) and <strong>BaselineAdminNetworkPolicy</strong> (BANP) — both reaching GA in K8s 1.32+. Plus, modern CNIs add <strong>FQDN-based policies</strong> for egress to external services.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='Compliance audit. Auditor asks: "what stops a developer from running <code>kubectl exec</code> into a Pod and curling out to <code>pastebin.com</code> with customer data?" The team\'s answer: "we have NetworkPolicy on every namespace." The auditor follows up: "do you have a default-deny policy that the team can\'t accidentally remove?" Silence. <em>NetworkPolicy v1 is namespace-scoped; nothing in the spec lets a cluster admin say "this rule trumps team rules."</em> Six months later K8s 1.32 GA\'d <code>AdminNetworkPolicy</code> with explicit priority and admin-only ownership. Today\'s lesson: how to layer admin / team policies + FQDN-based egress so the auditor goes home happy.',
    stamp_html='Three policy tiers: <strong>AdminNetworkPolicy</strong> (admin, high priority, evaluated first), <strong>NetworkPolicy</strong> (team, namespace-scoped, additive), <strong>BaselineAdminNetworkPolicy</strong> (admin default, evaluated last). For egress to external services, <strong>FQDN-based policies</strong> (CNI extension; not yet core API) match by hostname not CIDR. <code>github.com</code> instead of \"some IP block on the internet.\"',
    district_pin="kt-pin17",
    district_label="Switchboard — Policy Wing",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why NetworkPolicy v1 wasn't enough",
            body_html="""    <p>The original <code>NetworkPolicy</code> (covered in Lesson 17) is namespace-scoped and additive: each policy is an allow rule for the Pods it selects. If <em>any</em> NetworkPolicy applies to a Pod, the Pod is firewalled (default-deny, only the listed allows pass). Two important properties this <em>doesn\'t</em> have:</p>
    <ul>
      <li><strong>No admin override.</strong> A cluster admin can\'t write a policy that takes precedence over team policies. Every NetworkPolicy in a namespace has equal weight; they\'re all evaluated together.</li>
      <li><strong>No deny rules.</strong> Only allow. You can\'t say "block all egress to <code>1.2.3.4</code>" — you can only say "allow specific things." If a team forgets to write a policy, the namespace is wide open.</li>
    </ul>
    <p>The Gateway API style of layered ownership came to NetworkPolicy in K8s 1.30-1.32 with two new APIs: <strong>AdminNetworkPolicy</strong> (ANP, cluster-scoped, admin-owned, priority-ordered, supports allow/deny/pass) and <strong>BaselineAdminNetworkPolicy</strong> (BANP, cluster-scoped, admin-owned, exactly one per cluster, evaluated <em>last</em> as the default).</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The three-tier evaluation order",
            h2="ANP → NetworkPolicy → BANP",
            body_html="""    <p>For every packet, the CNI evaluates rules in this order:</p>
    <ol>
      <li><strong>AdminNetworkPolicy</strong> (highest priority numeric value first, sort within each ANP). Each rule has an action: <code>Allow</code>, <code>Deny</code>, or <code>Pass</code>. <em>Pass</em> is special — it means "stop evaluating ANP for this packet; let NetworkPolicy decide." Allow/Deny terminate evaluation.</li>
      <li><strong>NetworkPolicy</strong> (the original, namespace-scoped). Standard semantics: if a Pod is selected by any policy, default-deny applies; explicit allows let traffic through.</li>
      <li><strong>BaselineAdminNetworkPolicy</strong> (the cluster\'s default; one per cluster). Allow / Deny only (no Pass). Catches anything not handled above.</li>
    </ol>
    <p>The pattern this enables:</p>
    <ul>
      <li><strong>ANP</strong>: "no namespace can talk to the <code>kube-system</code> namespace except via the API server" (admin override; teams can\'t bypass).</li>
      <li><strong>ANP Pass</strong>: "for namespace X, defer to whatever the team\'s NetworkPolicy says" (admin opt-out for trusted teams).</li>
      <li><strong>BANP</strong>: "default deny all egress except to in-cluster Services" (cluster default; teams override per-namespace via NetworkPolicy or by passing through ANP).</li>
    </ul>""",
        ),
        Section(
            eyebrow="Section 1.7 · FQDN-based policies",
            h2="When CIDR isn't expressive enough",
            body_html="""    <p>NetworkPolicy v1 lets you allow egress to a CIDR (<code>10.0.0.0/8</code>) or a Service. It can\'t say "allow egress to <code>api.openai.com</code>." Why this matters:</p>
    <ul>
      <li>External SaaS (OpenAI, Anthropic API, Stripe, GitHub) own large, dynamic IP ranges. Listing CIDRs is fragile.</li>
      <li>Compliance often demands "list of allowed external destinations" by hostname, not by IP.</li>
      <li>Egress filtering as exfiltration prevention needs FQDN matching (block <code>pastebin.com</code> regardless of IP).</li>
    </ul>
    <p><strong>FQDN-based policies</strong> aren\'t yet in the core NetworkPolicy / ANP spec — but every modern CNI (Cilium, Calico Cloud, Tigera, NSX-T) exposes them via vendor extensions. Cilium\'s <code>CiliumNetworkPolicy</code> has <code>egress.toFQDNs</code>. Calico\'s <code>GlobalNetworkPolicy</code> has equivalent.</p>
    <p>How it works under the hood: the CNI hooks the Pod\'s DNS resolution (typically by intercepting DNS responses), records the IP it resolved a name to, and installs a short-lived per-IP allow rule. When the IP TTL expires, the rule expires too. Combined with eBPF-based enforcement, it\'s fast and accurate.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>FQDN policies are intentionally vendor-specific because the implementation is non-trivial — DNS interception, IP cache management, and TTL handling. The K8s Network SIG has a working group on standardising it for ANP/BANP, expected to land in 1.36 or later. Until then, FQDN policies are CNI-specific YAML — your migration cost from one CNI to another includes rewriting these.</p>""",
        ),
        Section(
            eyebrow="Section 1.9 · A practical layered design",
            h2="What a real cluster's policy stack looks like",
            body_html="""    <p>A typical 2026 production cluster ships:</p>
    <ul>
      <li><strong>One BANP</strong>: \"default deny all ingress and egress except DNS to kube-dns and traffic to kube-apiserver.\" Catches everything not explicitly allowed.</li>
      <li><strong>A small ANP set</strong>: protect <code>kube-system</code> (deny ingress except from controllers); deny egress to RFC1918 from internet-facing namespaces (defence in depth); allow Pods in <code>monitoring</code> namespace to scrape any Pod.</li>
      <li><strong>Per-namespace NetworkPolicy</strong>: app teams own their own ingress/egress allows. Most namespaces have a default-deny + one or two explicit allows.</li>
      <li><strong>FQDN egress policies</strong> (CNI-specific): allow-list of approved external SaaS endpoints per namespace. Updated as new external integrations are approved.</li>
    </ul>
    <p>This stack means: a developer can\'t accidentally bypass cluster policies by forgetting a NetworkPolicy. The BANP catches them. They also can\'t override admin-set deny rules — those are in ANP at high priority. They <em>can</em> add fine-grained allows within their namespace via standard NetworkPolicy.</p>""",
        ),
    ],
    pause_check_after_section={
        1: PauseCheck(
            question="A team-managed NetworkPolicy says \"allow egress to anywhere on port 443.\" An admin AdminNetworkPolicy at priority 100 says \"deny egress to <code>1.2.3.4/32</code>.\" A Pod tries to send to <code>1.2.3.4:443</code>. What happens?",
            options=[
                ("a) Allowed — team policy says 443 anywhere", False),
                ("b) Denied — ANP is evaluated first, and its <code>Deny</code> rule terminates evaluation", True),
                ("c) Indeterminate — depends on CNI", False),
            ],
            feedback="<strong>Answer: b.</strong> ANP is evaluated before NetworkPolicy. A <code>Deny</code> rule in ANP terminates evaluation immediately. Team policies can\'t override admin denies — exactly the property NetworkPolicy v1 lacked.",
        ),
    },
    before_after_before='<p>Pre-ANP: admin compliance rules baked into wiki pages. Teams forget a NetworkPolicy → namespace is wide open. No way to say "kube-system is admin-only" enforceably. Egress to external services controlled by IP allow lists that go stale weekly. Pastebin? Open by default until someone notices.</p>',
    before_after_after='<p>BANP at the bottom: default deny everywhere. ANP at the top: admin\'s non-negotiable rules. NetworkPolicy in the middle: app teams own their allows. FQDN policies: external services by name, not by ever-changing IP. Auditor asks "what stops X?" — show them the ANP. Done.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">ANP + BANP closes the longest-standing gap in K8s policy. The single-tier model lasted nearly a decade; the layered model is what production teams have always wanted.</p>',
    analogy_intro_html='<p>The Switchboard\'s policy wing has three desks, in order of authority. The <strong>City Council desk</strong> (AdminNetworkPolicy) issues binding ordinances — "no calls to City Hall except from registered businesses" — which override anything else and are enforced at the city gate. The <strong>building manager desks</strong> (NetworkPolicy) handle individual building rules — "callers from the press must use the lobby line." The <strong>default city ordinance shelf</strong> (BaselineAdminNetworkPolicy) sits at the bottom: "no calls to the city without a business reason." Building managers\' rules can override the default ordinance for their tenants; the city council\'s ordinances cannot be overridden by anyone.</p><p>Off to the side: a separate <strong>destination registry</strong> (FQDN policies) listing every approved out-of-city number by name — <code>github.com</code>, <code>api.openai.com</code> — so phone-by-name works even when the actual phone numbers (IP addresses) change. The registry is owned by the city; building managers request additions; council approves.</p>',
    translation_rows=[
        ("City Council ordinance", "<code>AdminNetworkPolicy</code>"),
        ("Building manager rule", "<code>NetworkPolicy</code> (v1)"),
        ("Default city ordinance shelf", "<code>BaselineAdminNetworkPolicy</code>"),
        ("\"Pass — defer to building manager\"", "ANP <code>Pass</code> action"),
        ("\"Forbidden by city, no exceptions\"", "ANP <code>Deny</code> at high priority"),
        ("Destination registry by name", "FQDN egress policies (CNI extension)"),
        ("Out-of-city numbers that change weekly", "External SaaS IP ranges"),
    ],
    analogy_stops="The analogy stops here: real ANP/BANP enforcement happens in the kernel via eBPF or iptables, not at \"the city gate.\" And FQDN policies depend on intercepting DNS, which works well 95% of the time but can be evaded by Pods that hard-code IPs.",
    eli5='Three sets of rules. The grown-up\'s rules go first (admin). The kid\'s rules go in the middle (team). The house\'s default rule (\"don\'t talk to strangers\") goes last. Plus a separate list of friends\' names you\'re allowed to call (FQDN).',
    eli10="<strong>AdminNetworkPolicy (ANP)</strong>: cluster-scoped, admin-owned, priority-ordered, with Allow/Deny/Pass actions. Evaluated first. <strong>NetworkPolicy (v1)</strong>: namespace-scoped, app-team-owned, additive allows. Evaluated next. <strong>BaselineAdminNetworkPolicy (BANP)</strong>: one per cluster, admin-owned default. Evaluated last. <strong>FQDN-based policies</strong>: CNI-vendor extensions (Cilium, Calico, etc.) for matching egress by hostname. Combined: layered policy with admin override, team self-service, and hostname-aware egress.",
    scenarios=[
        Scenario(name="A bank with strict compliance requirements", body="ANP: \"no namespace except <code>infra</code> can egress to RFC1918.\" \"All ingress to <code>finance</code> namespace must come from <code>app-frontend</code> or be denied.\" BANP: default deny ingress + egress. Per-namespace NP: app-team allows. FQDN policies: 14 approved external SaaS, allowed only from specific namespaces. Auditor calls these \"the cleanest policy stack we\'ve seen.\""),
        Scenario(name="A SaaS protecting against accidental data exfiltration", body="BANP default-denies egress everywhere except DNS, kube-apiserver, kube-dns. Each namespace owns an FQDN allow list (Cilium FQDN policies). New external service = a YAML PR. Pastebin / Discord / random-IP egress impossible. Catches a contractor\'s misbehaving build script before it can phone home."),
        Scenario(name="A platform team running multi-tenant clusters", body="Each tenant gets a namespace with admin-installed ANP \"this namespace can\'t talk to other tenants\' namespaces.\" Tenants own their NP for intra-namespace allows. ANP <code>Pass</code> for known infra namespaces (monitoring, logging) so tenant policies don\'t accidentally block scraping."),
        Scenario(name="A team using ANP <code>Pass</code> for delegated trust", body="Their <code>security-staging</code> namespace runs experimental Pods. ANP at priority 50 says \"<code>Pass</code> for security-staging\" — meaning: don\'t apply admin rules; let the team\'s own NetworkPolicy decide. Other namespaces get admin-enforced denies. Used for security testing without disabling protection cluster-wide."),
    ],
    misconceptions=[
        Misconception(myth="ANP replaces NetworkPolicy.", truth="ANP supplements NetworkPolicy. The three-tier model is intentional: admins set hard rules at the top, teams own additive allows in the middle, defaults catch the rest. Most clusters use all three."),
        Misconception(myth="FQDN policies are part of NetworkPolicy v1.", truth="They\'re not. NP v1 only knows CIDR + Service references. FQDN matching is a CNI vendor extension (Cilium\'s <code>CiliumNetworkPolicy.egress.toFQDNs</code>; Calico\'s equivalent). The K8s Network SIG is working on standardising it for ANP."),
        Misconception(myth="ANP <code>Pass</code> is the same as <code>Allow</code>.", truth="Different. <code>Allow</code> ends evaluation — packet flows. <code>Pass</code> means \"skip ANP for this packet, let NetworkPolicy decide.\" Useful for delegating to teams selectively without admin denies blocking everything."),
    ],
    flashcards=[
        Flashcard(front="Three tiers of K8s network policy (2026)?", back="AdminNetworkPolicy (cluster-scoped, admin-owned, priority-ordered, evaluated first). NetworkPolicy v1 (namespace-scoped, team-owned, additive allows). BaselineAdminNetworkPolicy (cluster-scoped, one per cluster, admin default, evaluated last)."),
        Flashcard(front="Three ANP actions?", back="<code>Allow</code> (terminate, packet flows), <code>Deny</code> (terminate, packet dropped), <code>Pass</code> (skip ANP for this packet, defer to NetworkPolicy). Pass enables admin-delegated trust to specific namespaces."),
        Flashcard(front="Why does ANP have priority?", back="To express \"this admin rule trumps that admin rule.\" Higher priority value wins. NetworkPolicy v1 had no priority — every rule was equal."),
        Flashcard(front="What does BANP solve?", back="The \"team forgot to write a NetworkPolicy\" problem. BANP is the cluster-wide default. Teams override per-namespace; cluster default applies otherwise."),
        Flashcard(front="What is an FQDN policy?", back="An egress policy matching by DNS hostname (<code>github.com</code>) instead of IP CIDR. CNI-vendor extension — Cilium <code>CiliumNetworkPolicy</code>, Calico <code>GlobalNetworkPolicy</code>, etc."),
        Flashcard(front="How do FQDN policies work under the hood?", back="CNI intercepts DNS responses, caches IP→name mappings, installs short-lived per-IP allow rules with TTLs matching DNS TTL. Pod-by-Pod, kept fresh as DNS records change."),
        Flashcard(front="Limit of FQDN policies?", back="Pods that hard-code IPs (skipping DNS entirely) bypass FQDN matching. Mitigation: combine FQDN policies with CIDR denies (block direct internet IPs except whitelisted ranges)."),
        Flashcard(front="When does ANP/BANP go GA?", back="ANP: GA in K8s 1.32. BANP: GA in 1.32. Cilium and Calico support both natively. CIS K8s benchmarks now reference them."),
    ],
    quizzes=[
        Quiz(prompt="A platform team writes an ANP at priority 100: <code>action: Deny, ports: [22]</code> for all namespaces. A team writes a NetworkPolicy allowing port 22 from a specific Pod to a specific node-management Pod. The team\'s policy is being ignored. Why?", answer="ANP runs first. The Deny rule at priority 100 is hit before NetworkPolicy gets evaluated, and Deny terminates evaluation. <strong>Fix options:</strong> (1) Use <code>Pass</code> instead of <code>Deny</code> for the specific Pod — let NetworkPolicy decide. (2) Use a higher-priority ANP <code>Pass</code> rule for that namespace + port combination. (3) Restructure: deny egress to <em>most</em> things at admin level, but allow this specific flow via a more specific ANP allow rule. The right answer depends on whether the admin policy is meant to be absolute (option 3) or delegable (options 1-2)."),
        Quiz(prompt="Compliance asks: \"prove no Pod in the production cluster can egress to <code>pastebin.com</code>.\" The cluster runs Cilium. What\'s the design + the evidence?", answer="<strong>Design:</strong> a CiliumNetworkPolicy at the cluster level (or as a namespaced policy in every namespace via a Kyverno policy) with egress.toFQDNs allow-list excluding pastebin.com. Even better: a BANP <code>Deny all egress except DNS</code>, combined with CiliumNetworkPolicy allows for approved FQDNs only. <strong>Evidence:</strong> (1) Hubble flows showing pastebin.com queries blocked at the policy layer. (2) Kyverno policy report enforcing the FQDN-allow-list as a CRD. (3) <code>cilium policy get</code> output showing no rule allows pastebin.com. <strong>Caveat:</strong> a Pod that hard-codes pastebin\'s IPs bypasses FQDN matching. Pair with egress IP allow-listing or run an explicit egress proxy."),
        Quiz(prompt="A new namespace is created. The team forgets to write a NetworkPolicy. With BANP installed, what happens to traffic? <strong>Click for the walk-through. ▼</strong>", cyoa=True, cyoa_tag="the walk-through", answer="The cluster has BANP <code>default deny ingress and egress</code>. (1) A Pod in the new namespace tries to call kube-apiserver — ANP at priority 5000 has <code>Allow</code> for kube-apiserver from all namespaces. Allowed. (2) Pod tries to call kube-dns — same, ANP allows. (3) Pod tries to call <code>github.com</code> — no ANP rule covers it; falls through NP (none exist); falls through to BANP \"default deny egress.\" Dropped. (4) Pod tries to receive ingress from another namespace — same path, BANP denies. <strong>Effect:</strong> the namespace is locked down by default. The team must explicitly write NetworkPolicy to allow what they need. Worst case: their service doesn\'t work until they fix it. <strong>Compare with no BANP:</strong> the namespace would be wide open until someone wrote a NP. BANP turns \"forgot to write a policy\" into a noisy failure (service broken) instead of a silent compromise (everything allowed)."),
    ],
    glossary=[
        GlossaryItem(name="AdminNetworkPolicy (ANP)", definition="Cluster-scoped, admin-owned policy. Priority-ordered. Allow/Deny/Pass actions. Evaluated before NetworkPolicy. GA in K8s 1.32."),
        GlossaryItem(name="BaselineAdminNetworkPolicy (BANP)", definition="One per cluster. Admin-owned default. Allow/Deny only. Evaluated last."),
        GlossaryItem(name="ANP Pass action", definition="\"Skip ANP for this packet; let NetworkPolicy decide.\" Used to delegate trust to specific namespaces."),
        GlossaryItem(name="Priority (ANP)", definition="Integer; higher value = evaluated first. Within a tier, sort by priority."),
        GlossaryItem(name="FQDN policy", definition="Egress policy matching by DNS hostname. CNI-vendor extension. Cilium <code>toFQDNs</code>, Calico <code>GlobalNetworkPolicy</code>."),
        GlossaryItem(name="DNS interception", definition="CNI mechanism for FQDN policies: watch DNS responses, cache name→IP, install short-lived allow rules."),
        GlossaryItem(name="Egress filtering", definition="Restricting outbound traffic from Pods. Used for compliance, exfiltration prevention, cost control."),
        GlossaryItem(name="default-deny", definition="Pattern: a NetworkPolicy/BANP that selects everything but allows nothing — blocks all traffic that isn\'t explicitly allowed elsewhere."),
        GlossaryItem(name="Egress proxy", definition="Hardware or software proxy through which all egress flows. Provides URL-based filtering at L7. Sometimes paired with FQDN policies for defence in depth."),
        GlossaryItem(name="CiliumNetworkPolicy", definition="Cilium\'s extended CRD with FQDN matching, L7 rules, identity-aware policy. Superset of standard NetworkPolicy."),
        GlossaryItem(name="Network Identity (Cilium)", definition="Per-Pod label-derived identity used for policy decisions in Cilium. Faster than IP-based matching."),
        GlossaryItem(name="Kyverno policy reports", definition="Auditing reports from Kyverno about which NetworkPolicies/ANPs/BANPs are present. Useful for compliance evidence."),
    ],
    recap_lead="ANP (admin, top priority) → NetworkPolicy (team, additive) → BANP (admin default, bottom). Three tiers, layered ownership. FQDN policies (CNI extensions) match egress by hostname. The ten-year gap in K8s network policy is closed.",
    recap_next="<strong>Next — Lesson 27: RBAC & Authentication.</strong> Module 13 begins. RBAC, structured auth config, OIDC integration. The new K-Town district: Watchtower.",
)
