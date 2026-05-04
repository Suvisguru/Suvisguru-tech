"""Per-module Section 6 animations for K-ADV-SEC S1-S8."""

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


# S1 — Threat surface + zero-trust + tenant isolation
SCENE_S1 = f'''        {_mode_label()}
        {_box(40, 70, 150, 100, "Outer perimeter", "untrusted internet", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(220, 70, 150, 100, "Identity check", "AuthN at every gate", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(400, 70, 150, 100, "Tenant zone", "namespace + RBAC + NetPol", fill="#5DCAA5", label_color="#1F2433")}
        {_box(580, 70, 140, 100, "Vault + audit", "secrets + log signed", fill="#A04832", label_color="#FBF1D6")}'''

ANIM_S1 = Animation(
    h2="A request walks the citadel — perimeter → identity → tenant → vault",
    intro="Zero-trust = no implicit trust at any boundary. Every step authenticates and authorises.",
    svg_viewbox="0 0 760 220",
    svg_body=SCENE_S1,
    initial_packet_xy=(115, 120),
    initial_readout='<strong>Watching:</strong> a request walks the citadel.',
    scenes=[
        AnimationScene(
            mode_id="zerotrust",
            button_label="▶ zero-trust path",
            mode_label="Mode: zero-trust — every gate checks identity + authorisation",
            phases=[
                P(readout='<strong>Step 1.</strong> Request arrives at the outer perimeter. Untrusted by default.', move_to=(115, 120), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Identity check (OIDC / mTLS / ServiceAccount) — proves who it is.', move_to=(295, 120), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Tenant zone — namespace boundary + RBAC + NetworkPolicy gate access to data.', move_to=(475, 120), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Vault + audit — secrets fetched signed, every action logged.', move_to=(650, 120), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# S2 — RBAC at scale
SCENE_S2 = f'''        {_mode_label()}
        {_box(40, 70, 150, 60, "User / SA", "subject", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(220, 70, 200, 60, "Role / ClusterRole", "verbs on resources", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(450, 70, 270, 60, "RoleBinding / ClusterRoleBinding", "binds subject to role in namespace / cluster", fill="#5DCAA5", label_color="#1F2433")}
        {_box(40, 150, 680, 60, "audit.k8s.io — every authz decision is logged + sampled centrally", "scale via aggregation patterns + tooling (rakkess, kubectl-who-can)", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_S2 = Animation(
    h2="RBAC binding chain — subject + role + binding",
    intro="RBAC at scale = composition + aggregation + audit.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_S2,
    initial_packet_xy=(115, 100),
    initial_readout='<strong>Watching:</strong> RBAC binding chain.',
    scenes=[
        AnimationScene(
            mode_id="rbac",
            button_label="▶ subject → role → binding",
            mode_label="Mode: RBAC binding chain at scale",
            phases=[
                P(readout='<strong>Step 1.</strong> Subject = user / group / ServiceAccount.', move_to=(115, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Role / ClusterRole declares verbs on resources (get/list/create on Pods, etc.).', move_to=(320, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> RoleBinding (namespaced) or ClusterRoleBinding ties subject to role.', move_to=(580, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> audit.k8s.io logs every decision; sampling + pipelines surface anomalies.', move_to=(380, 180), duration_ms=900, pause_after_ms=2200),
            ],
        ),
    ],
)


# S3 — Admission policy hybrid
SCENE_S3 = f'''        {_mode_label()}
        {_box(40, 70, 130, 60, "API request", "kubectl / CI", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(190, 70, 130, 60, "kube-apiserver", "auth + admission", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(340, 70, 200, 60, "Mutating webhook (Kyverno)", "patch / set defaults", fill="#FF9900", label_color="#1F2433")}
        {_box(560, 70, 160, 60, "Validating (Gatekeeper)", "OPA / Rego", fill="#5DCAA5", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "PolicyReport CRD = unified report (Kyverno + Gatekeeper); ValidatingAdmissionPolicy + CEL inline (no webhook)", "modern hybrid pattern", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_S3 = Animation(
    h2="Admission walks the gate — Kyverno mutating + Gatekeeper validating",
    intro="Hybrid: Kyverno for K8s-native rules; Gatekeeper for formal-logic rules; both report to PolicyReport.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_S3,
    initial_packet_xy=(95, 100),
    initial_readout='<strong>Watching:</strong> a request through admission.',
    scenes=[
        AnimationScene(
            mode_id="hybrid",
            button_label="▶ admission hybrid path",
            mode_label="Mode: API request → mutate → validate → store",
            phases=[
                P(readout='<strong>Step 1.</strong> kubectl / CI calls API.', move_to=(95, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> kube-apiserver authn + authz (RBAC) → admission chain.', move_to=(240, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Mutating: Kyverno patches defaults (e.g., adds resource limits).', move_to=(420, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Validating: Gatekeeper enforces formal rules via OPA / Rego.', move_to=(620, 100), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Both write PolicyReport CRDs; failures surface in one feed.', move_to=(380, 185), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# S4 — PSA Restricted + runtime detection
SCENE_S4 = f'''        {_mode_label()}
        {_box(40, 70, 200, 60, "Pod Security Admission", "restricted: no privileged, no hostPath, drop capabilities, runAsNonRoot", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(280, 70, 200, 60, "Falco / Tetragon", "runtime syscall watch", fill="#A04832", label_color="#FBF1D6")}
        {_box(520, 70, 200, 60, "alert pipeline", "EventBridge / SIEM / pager", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "warn → audit → enforce migration; runtime catches what admission can\'t (e.g., escape attempts, exec into Pod)", "two-layer defence", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_S4 = Animation(
    h2="PSA Restricted + runtime detection — admission stops misconfig; runtime stops escape",
    intro="PSA = static config; Falco / Tetragon = live syscalls. They catch different failure modes.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_S4,
    initial_packet_xy=(140, 100),
    initial_readout='<strong>Watching:</strong> the two security layers in action.',
    scenes=[
        AnimationScene(
            mode_id="layers",
            button_label="▶ admission + runtime layers",
            mode_label="Mode: PSA Restricted + Falco / Tetragon",
            phases=[
                P(readout='<strong>Step 1.</strong> Pod manifest hits PSA Restricted: rejects privileged / hostPath / writable rootfs.', move_to=(140, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Allowed Pod runs; Falco / Tetragon attach eBPF probes to syscalls.', move_to=(380, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Suspicious syscall (e.g., shell spawned from app, mount() in container) → alert.', move_to=(620, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Alert flows to EventBridge / SIEM / pager; on-call investigates + isolates.', move_to=(380, 185), duration_ms=900, pause_after_ms=2200),
            ],
        ),
    ],
)


# S5 — Image signing + SBOM + SLSA
SCENE_S5 = f'''        {_mode_label()}
        {_box(40, 70, 130, 60, "build", "CI: provenance attestation", fill="#5DCAA5", label_color="#1F2433")}
        {_box(190, 70, 130, 60, "Cosign sign", "signature + SBOM", fill="#FF9900", label_color="#1F2433")}
        {_box(340, 70, 130, 60, "registry (OCI)", "image + sigs + SBOM + VEX", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(490, 70, 130, 60, "policy gate", "Kyverno verifyImages", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(640, 70, 80, 60, "deploy", "approved", fill="#A04832", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "SLSA L3+ provenance + in-toto attestations + VEX (vulnerability disposition) — signed, verifiable supply chain", "supply-chain integrity", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_S5 = Animation(
    h2="An image\'s journey — sign, attest, store, verify, deploy",
    intro="Cosign sign → SBOM + provenance attached → cluster verifies before admit.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_S5,
    initial_packet_xy=(95, 100),
    initial_readout='<strong>Watching:</strong> an image traverse the supply chain.',
    scenes=[
        AnimationScene(
            mode_id="supplychain",
            button_label="▶ build → verify → deploy",
            mode_label="Mode: signed supply chain",
            phases=[
                P(readout='<strong>Step 1.</strong> CI builds image; emits SLSA provenance attestation.', move_to=(105, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Cosign signs image; attaches SBOM + provenance + VEX.', move_to=(255, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Push to OCI registry (image + sigs + SBOM + VEX as referrers).', move_to=(405, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Cluster admission (Kyverno verifyImages) checks signature + identity + provenance.', move_to=(555, 100), duration_ms=900),
                P(readout='<strong>Step 5.</strong> Approved → deploy. Unsigned / unverified → rejected.', move_to=(680, 100), duration_ms=900, pause_after_ms=2000),
            ],
        ),
    ],
)


# S6 — Secrets at scale + mTLS + service mesh
SCENE_S6 = f'''        {_mode_label()}
        {_box(40, 70, 180, 60, "External Secrets Operator", "Vault / Secrets Manager", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(240, 70, 180, 60, "Sealed K8s Secret", "in cluster, KMS-wrapped", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(440, 70, 280, 60, "mTLS via service mesh (Istio / Linkerd)", "every Pod-to-Pod call signed + encrypted", fill="#5DCAA5", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "cert-manager + SPIFFE / SPIRE = workload identity foundation; rotation automated", "identity for every workload", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_S6 = Animation(
    h2="Secret + mTLS path — fetched from external store; mesh enforces in transit",
    intro="External Secrets fetches; mesh signs in transit. Workload identity is the foundation.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_S6,
    initial_packet_xy=(125, 100),
    initial_readout='<strong>Watching:</strong> secrets + mTLS at scale.',
    scenes=[
        AnimationScene(
            mode_id="vault",
            button_label="▶ secret + mTLS path",
            mode_label="Mode: External Secrets → Sealed K8s Secret → mTLS",
            phases=[
                P(readout='<strong>Step 1.</strong> External Secrets Operator polls Vault / Secrets Manager.', move_to=(125, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Creates / updates K8s Secret (KMS-encrypted at rest).', move_to=(330, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Workload mounts; mesh sidecar wraps Pod-to-Pod calls in mTLS.', move_to=(580, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> SPIFFE / SPIRE issues workload identity; cert-manager rotates everything.', move_to=(380, 185), duration_ms=900, pause_after_ms=2200),
            ],
        ),
    ],
)


# S7 — Audit + compliance + IR
SCENE_S7 = f'''        {_mode_label()}
        {_box(40, 70, 200, 60, "audit.k8s.io webhook", "every authz decision + request body", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(280, 70, 220, 60, "SIEM / Loki / Splunk", "search + alert + retention", fill="#5DCAA5", label_color="#1F2433")}
        {_box(540, 70, 180, 60, "compliance evidence", "PCI / HIPAA / SOC2", fill="#FF9900", label_color="#1F2433")}
        {_box(40, 160, 680, 50, "break-glass IAM (high-privilege role time-boxed + alerting); IR runbook (containment → eradication → recovery)", "incident response", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_S7 = Animation(
    h2="From audit log to compliance evidence — and back to IR",
    intro="Every decision logged → SIEM → searchable → compliance evidence + IR triggers.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_S7,
    initial_packet_xy=(140, 100),
    initial_readout='<strong>Watching:</strong> audit + compliance + IR loop.',
    scenes=[
        AnimationScene(
            mode_id="audit",
            button_label="▶ audit → SIEM → evidence + IR",
            mode_label="Mode: audit pipeline",
            phases=[
                P(readout='<strong>Step 1.</strong> kube-apiserver writes audit events (Metadata / Request / RequestResponse).', move_to=(140, 100), duration_ms=900),
                P(readout='<strong>Step 2.</strong> Webhook → SIEM / Loki / Splunk; tagged + retained per policy.', move_to=(390, 100), duration_ms=900),
                P(readout='<strong>Step 3.</strong> Compliance dashboards aggregate: PCI / HIPAA / SOC2 / NIST 800-190 controls evidenced.', move_to=(630, 100), duration_ms=900),
                P(readout='<strong>Step 4.</strong> Anomaly → IR runbook: containment + eradication + recovery + postmortem.', move_to=(380, 185), duration_ms=900, pause_after_ms=2200),
            ],
        ),
    ],
)


# S8 — Capstone defendable citadel
SCENE_S8 = f'''        {_mode_label()}
        {_box(40, 70, 130, 60, "perimeter", "zero-trust", fill="#3F4A5E", label_color="#FBF1D6")}
        {_box(190, 70, 130, 60, "RBAC + admission", "Kyverno + Gatekeeper", fill="#5A6B81", label_color="#FBF1D6")}
        {_box(340, 70, 130, 60, "PSA Restricted", "+ Falco runtime", fill="#5DCAA5", label_color="#1F2433")}
        {_box(490, 70, 130, 60, "signed images", "Cosign + SBOM + VEX", fill="#FF9900", label_color="#1F2433")}
        {_box(640, 70, 80, 60, "vault + mesh", "mTLS", fill="#A04832", label_color="#FBF1D6")}
        {_box(40, 160, 680, 50, "audit → SIEM → compliance evidence; break-glass + IR runbook on the wall", "operational fabric", fill="#FBE8DC", stroke="#A04832", label_color="#A04832")}'''

ANIM_S8 = Animation(
    h2="The full citadel — every K-ADV-SEC concept in one architecture",
    intro="Perimeter → RBAC → admission → PSA + runtime → signed images → vault + mesh → audit + IR.",
    svg_viewbox="0 0 760 230",
    svg_body=SCENE_S8,
    initial_packet_xy=(105, 100),
    initial_readout='<strong>Watching:</strong> the full defendable citadel.',
    scenes=[
        AnimationScene(
            mode_id="capstone",
            button_label="▶ end-to-end citadel walk",
            mode_label="Mode: full reference K-Citadel",
            phases=[
                P(readout='<strong>Phase A.</strong> Perimeter: zero-trust; every gate authenticates.', move_to=(105, 100), duration_ms=900),
                P(readout='<strong>Phase B.</strong> RBAC + admission: Kyverno + Gatekeeper hybrid.', move_to=(255, 100), duration_ms=900),
                P(readout='<strong>Phase C.</strong> Pod Security Admission Restricted + Falco runtime detection.', move_to=(405, 100), duration_ms=900),
                P(readout='<strong>Phase D.</strong> Image signed (Cosign) + SBOM + VEX; verified at admission.', move_to=(555, 100), duration_ms=900),
                P(readout='<strong>Phase E.</strong> Secrets via External Secrets; mesh-mTLS for all Pod-to-Pod.', move_to=(680, 100), duration_ms=900),
                P(readout='<strong>Phase F.</strong> Audit pipeline → SIEM → compliance evidence; IR runbook closes the loop.', move_to=(380, 185), duration_ms=900, pause_after_ms=2400),
            ],
        ),
    ],
)


ANIMATIONS = {
    "01": ANIM_S1,
    "02": ANIM_S2,
    "03": ANIM_S3,
    "04": ANIM_S4,
    "05": ANIM_S5,
    "06": ANIM_S6,
    "07": ANIM_S7,
    "08": ANIM_S8,
}
