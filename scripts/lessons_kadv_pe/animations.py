"""Per-module Section 6 animations for K-ADV-PE P1-P8."""

from _helpers import Animation, AnimationScene, AnimationPhase as P


def _box(x, y, w, h, label, sub=None, fill="#FFFFFF", stroke="#3F4A5E", label_color="#3F4A5E"):
    sub_html = f'<text x="{x+w//2}" y="{y+38}" text-anchor="middle" font-size="9" fill="#6B6058">{sub}</text>' if sub else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        f'<text x="{x+w//2}" y="{y+22}" text-anchor="middle" font-size="11" font-weight="700" fill="{label_color}">{label}</text>'
        f'{sub_html}'
    )


def _mode_label(x=380, y=22):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="13" font-weight="600" fill="#3F4A5E" id="anim-mode-label">Mode</text>'


def _simple_anim(num, h2, intro, scene_body, button_label, mode_label, phases):
    return Animation(
        h2=h2, intro=intro,
        svg_viewbox="0 0 760 230", svg_body=scene_body,
        initial_packet_xy=(115, 110), initial_readout=f'<strong>Watching:</strong> {h2.lower()}.',
        scenes=[AnimationScene(mode_id=f"p{num}", button_label=button_label, mode_label=mode_label, phases=phases)],
    )


SCENE_P1 = f'''        {_mode_label()}
        {_box(40, 70, 180, 80, "developer", "I want a service", fill="#5DCAA5", label_color="#1F2433")}
        {_box(240, 70, 180, 80, "golden path", "Backstage Scaffolder", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(440, 70, 180, 80, "self-service NS", "RBAC + NetPol + Quota", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(640, 70, 80, 80, "ship", "K8s", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "IDP = the platform team\'s product; developer is the customer; golden path is the menu", "platform-as-product", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_P1 = _simple_anim(1, "Developer hits the golden path",
    "Developer asks for a service; golden path scaffolds; namespace + governance auto-provision; ship.",
    SCENE_P1, "▶ developer journey", "Mode: developer self-service via golden path",
    [P(readout='<strong>Step 1.</strong> Developer needs a new service. Opens Backstage portal.', move_to=(130, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> Picks golden path; Scaffolder generates repo + manifests + CI.', move_to=(330, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Namespace auto-provisioned with RBAC + NetPol + Quota.', move_to=(530, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> Ship to K8s. Day-1 governance was day-0.', move_to=(680, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_P2 = f'''        {_mode_label()}
        {_box(40, 70, 200, 80, "Backstage catalog", "every service + owner", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(260, 70, 180, 80, "TechDocs", "MkDocs from repos", fill="#5DCAA5", label_color="#1F2433")}
        {_box(460, 70, 180, 80, "Scaffolder", "generate from template", fill="#FF9900", label_color="#1F2433")}
        {_box(660, 70, 60, 80, "plugins", "100+", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "Backstage = single pane: catalog / docs / scaffolder / plugins; the IDP\'s storefront", "developer experience", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_P2 = _simple_anim(2, "Backstage as the IDP storefront",
    "Catalog + TechDocs + Scaffolder + plugins; one place for every developer-facing artifact.",
    SCENE_P2, "▶ Backstage tour", "Mode: Backstage four pillars",
    [P(readout='<strong>Step 1.</strong> Catalog: every service registered with owner + tier.', move_to=(140, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> TechDocs: MkDocs auto-rendered from each repo\'s mkdocs.yml.', move_to=(350, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Scaffolder: golden-path templates create repos + manifests + CI.', move_to=(550, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> Plugins: ArgoCD, Jenkins, PagerDuty, Datadog, K8s, custom.', move_to=(690, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_P3 = f'''        {_mode_label()}
        {_box(40, 70, 180, 80, "XRD", "schema + claim type", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(240, 70, 180, 80, "Composition + Functions", "compose Providers", fill="#5DCAA5", label_color="#1F2433")}
        {_box(440, 70, 180, 80, "Providers", "AWS / Azure / GCP / SaaS", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(640, 70, 80, 80, "Configuration package", "shareable", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "Crossplane v2 = Compose + Functions (KCL / Go templates / Pkl) + Configuration packages", "platform-as-API", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_P3 = _simple_anim(3, "Crossplane composes cloud + SaaS into one CRD",
    "XRD defines the user-facing claim; Composition + Functions resolve to Provider resources.",
    SCENE_P3, "▶ Crossplane v2 walk", "Mode: Crossplane v2 compose",
    [P(readout='<strong>Step 1.</strong> XRD declares user-facing API (e.g., XPostgresInstance).', move_to=(130, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> User creates a Claim; Composition + Functions render Provider resources.', move_to=(330, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Providers (AWS / Azure / GCP / SaaS) reconcile with the cloud.', move_to=(530, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> Whole stack ships as a Configuration package; install once across clusters.', move_to=(680, 110), duration_ms=900, pause_after_ms=2200)])


SCENE_P4 = f'''        {_mode_label()}
        {_box(40, 70, 200, 80, "ApplicationSet", "generators (clusters / git / list)", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(260, 70, 200, 80, "per-cluster App", "from one chart + values", fill="#5DCAA5", label_color="#1F2433")}
        {_box(480, 70, 240, 80, "OPA / Kyverno guardrails", "PR + admission + sync", fill="#A04832", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "fleet GitOps + policy gates: deploy + governance from one Git source", "GitOps at scale", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_P4 = _simple_anim(4, "ApplicationSet fans out + guardrails enforce",
    "One template; per-cluster Apps generated; OPA + Kyverno gate policy.",
    SCENE_P4, "▶ ApplicationSet walk", "Mode: ApplicationSet + guardrails",
    [P(readout='<strong>Step 1.</strong> ApplicationSet generator iterates over clusters / git dirs / list.', move_to=(140, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> Per-cluster App spawns from template with cluster-label values.', move_to=(360, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> OPA / Kyverno policies gate at PR + admission + sync.', move_to=(600, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_P5 = f'''        {_mode_label()}
        {_box(40, 70, 180, 80, "tenant request", "Backstage form", fill="#5DCAA5", label_color="#1F2433")}
        {_box(240, 70, 180, 80, "Crossplane Claim", "namespace + RBAC + NetPol + Quota", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(440, 70, 180, 80, "GitOps PR", "human-approved", fill="#FF9900", label_color="#1F2433")}
        {_box(640, 70, 80, 80, "ready", "K8s", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "tenant onboarding = templated; resource quotas, cost label, ownership baked in", "self-service tenancy", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_P5 = _simple_anim(5, "Tenant onboarding via Backstage + Crossplane",
    "Form → Claim → GitOps PR → namespace ready with governance.",
    SCENE_P5, "▶ tenant onboarding", "Mode: tenant self-service",
    [P(readout='<strong>Step 1.</strong> Tenant fills Backstage form (name, owner, tier).', move_to=(130, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> Crossplane Claim renders namespace + RBAC + NetPol + Quota.', move_to=(330, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> GitOps PR opens; human-approved; merge.', move_to=(530, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> Namespace ready; tenant\'s pipeline can deploy. ~10 minutes total.', move_to=(680, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_P6 = f'''        {_mode_label()}
        {_box(40, 70, 130, 80, "developer", "Score / OAM / Radius", fill="#5DCAA5", label_color="#1F2433")}
        {_box(190, 70, 130, 80, "Score abstract", "language-agnostic", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 70, 130, 80, "OAM / KubeVela", "CUE-based", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(490, 70, 130, 80, "Radius (Microsoft)", "app-graph", fill="#FF9900", label_color="#1F2433")}
        {_box(640, 70, 80, 80, "Humanitec", "PaaS-style", fill="#A04832", label_color="#FBF1D6")}'''
ANIM_P6 = _simple_anim(6, "Workload abstractions layer on top of K8s",
    "Score / OAM / Radius / Humanitec — pick by team + ergonomics.",
    SCENE_P6, "▶ workload abstraction tour", "Mode: abstractions",
    [P(readout='<strong>Step 1.</strong> Developer writes Score spec (language-agnostic; portable).', move_to=(140, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> OAM / KubeVela uses CUE for typed app definitions.', move_to=(290, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Radius models app-graph (resources + connections).', move_to=(440, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> Humanitec is opinionated PaaS-style on top.', move_to=(620, 110), duration_ms=900, pause_after_ms=2000)])


SCENE_P7 = f'''        {_mode_label()}
        {_box(40, 70, 200, 80, "OpenCost / Kubecost", "cost per Pod / namespace", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(260, 70, 200, 80, "platform SLO", "uptime + latency + capacity", fill="#5DCAA5", label_color="#1F2433")}
        {_box(480, 70, 240, 80, "chargeback / showback dashboards", "team / cost-center", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "platform team is a business unit; cost transparency = behavior change in tenants", "platform economics", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_P7 = _simple_anim(7, "Platform SLOs + chargeback shape behavior",
    "OpenCost / Kubecost surface per-namespace cost; SLOs are the platform\'s contract.",
    SCENE_P7, "▶ SLO + chargeback walk", "Mode: platform economics",
    [P(readout='<strong>Step 1.</strong> OpenCost / Kubecost compute per-Pod cost from cloud bill + utilization.', move_to=(140, 110), duration_ms=900),
     P(readout='<strong>Step 2.</strong> Platform SLOs (uptime, latency, capacity-headroom) published like a vendor SLA.', move_to=(360, 110), duration_ms=900),
     P(readout='<strong>Step 3.</strong> Chargeback (real bill) or showback (visible cost) per team.', move_to=(600, 110), duration_ms=900),
     P(readout='<strong>Step 4.</strong> Tenants self-tune: cheaper instance types, smaller requests, scale-to-zero.', move_to=(380, 185), duration_ms=900, pause_after_ms=2200)])


SCENE_P8 = f'''        {_mode_label()}
        {_box(40, 70, 130, 60, "Backstage", "+ catalog", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(190, 70, 130, 60, "Crossplane", "+ XRDs", fill="#5DCAA5", label_color="#1F2433")}
        {_box(340, 70, 130, 60, "Argo CD AS", "+ guardrails", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(490, 70, 130, 60, "OPA / Kyverno", "policy", fill="#A04832", label_color="#FBF1D6")}
        {_box(640, 70, 80, 60, "Score / OAM", "abstraction", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "OpenCost + SLO + tenant onboarding wired; the equipped workshop", "self-service IDP", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''
ANIM_P8 = _simple_anim(8, "The equipped workshop — every K-ADV-PE concept",
    "Backstage + Crossplane + Argo CD AS + OPA + Score + OpenCost + tenant onboarding.",
    SCENE_P8, "▶ equipped workshop", "Mode: full reference IDP",
    [P(readout='<strong>Phase A.</strong> Backstage = developer storefront.', move_to=(105, 100), duration_ms=900),
     P(readout='<strong>Phase B.</strong> Crossplane = platform-as-API.', move_to=(255, 100), duration_ms=900),
     P(readout='<strong>Phase C.</strong> Argo CD ApplicationSets = fleet GitOps.', move_to=(405, 100), duration_ms=900),
     P(readout='<strong>Phase D.</strong> OPA + Kyverno = policy gates.', move_to=(555, 100), duration_ms=900),
     P(readout='<strong>Phase E.</strong> Score / OAM = workload abstraction.', move_to=(680, 100), duration_ms=900),
     P(readout='<strong>Phase F.</strong> OpenCost + SLO + onboarding wired; new tenant in &lt; 1 day.', move_to=(380, 185), duration_ms=900, pause_after_ms=2400)])


ANIMATIONS = {"01": ANIM_P1, "02": ANIM_P2, "03": ANIM_P3, "04": ANIM_P4, "05": ANIM_P5, "06": ANIM_P6, "07": ANIM_P7, "08": ANIM_P8}
