from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Outbuildings around a homestead: shed labels CoreDNS, metrics-server, Gateway, cert-manager, CSI, monitoring, logging, ingress.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">OUTBUILDINGS · CORE ADD-ON STACK</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">DAY-1 ADD-ONS (installed via Argo CD)</text>
    <rect x="14" y="34" width="110" height="34" rx="3" fill="#5A9F7A"/><text x="69" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">CoreDNS</text><text x="69" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">in-cluster DNS</text>
    <rect x="130" y="34" width="110" height="34" rx="3" fill="#3F4A5E"/><text x="185" y="50" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">metrics-server</text><text x="185" y="62" text-anchor="middle" font-size="7" fill="#FBF1D6">HPA + kubectl top</text>
    <rect x="246" y="34" width="110" height="34" rx="3" fill="#A04832"/><text x="301" y="50" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">Gateway / Ingress</text><text x="301" y="62" text-anchor="middle" font-size="7" fill="#FBE8DC">Envoy / Cilium GW</text>
    <rect x="362" y="34" width="110" height="34" rx="3" fill="#E8B547"/><text x="417" y="50" text-anchor="middle" font-size="9" fill="#5A4F45" font-weight="700">cert-manager</text><text x="417" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">app TLS</text>
    <rect x="478" y="34" width="110" height="34" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="533" y="50" text-anchor="middle" font-size="9" fill="#A04832" font-weight="700">CSI driver</text><text x="533" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">storage</text>
    <rect x="14" y="76" width="110" height="34" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="69" y="92" text-anchor="middle" font-size="9" fill="#8B5A00" font-weight="700">ExternalDNS</text>
    <rect x="130" y="76" width="110" height="34" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="185" y="92" text-anchor="middle" font-size="9" fill="#8B5A00" font-weight="700">SOPS / Sealed</text>
    <rect x="246" y="76" width="110" height="34" rx="3" fill="#E0EEF3" stroke="#4A8FA8"/><text x="301" y="92" text-anchor="middle" font-size="9" fill="#3F4A5E" font-weight="700">monitoring</text><text x="301" y="104" text-anchor="middle" font-size="7" fill="#5A4F45">kube-prometheus</text>
    <rect x="362" y="76" width="110" height="34" rx="3" fill="#E0EEF3" stroke="#4A8FA8"/><text x="417" y="92" text-anchor="middle" font-size="9" fill="#3F4A5E" font-weight="700">logging</text><text x="417" y="104" text-anchor="middle" font-size="7" fill="#5A4F45">Loki / Vector</text>
    <rect x="478" y="76" width="110" height="34" rx="3" fill="#3F4A5E"/><text x="533" y="92" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">policy + Falco</text>
    <rect x="14" y="118" width="578" height="34" rx="3" fill="#5A9F7A"/><text x="303" y="134" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">Argo CD installs + reconciles all of the above from git</text><text x="303" y="146" text-anchor="middle" font-size="7" fill="#FBE8DC">App-of-Apps + ApplicationSet manage versions</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="05",
    title_short="core add-ons",
    title_full="V5 · Core Add-ons (CoreDNS, Gateway, cert-manager, CSI, observability, GitOps)",
    title_html="K-VAN V5 · Core Add-ons",
    module_eyebrow="Module V5 · the outbuildings",
    hero_sub_html='kubeadm + CNI = a working but bare cluster. Production needs ~10 add-ons before the first workload lands. Get them right (and version-controlled) once; use the same stack across every cluster.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='You hand the cluster to an app team. They say "it has no DNS for our ingress hostname, no certificates, no metrics, no log shipping, no policy enforcement, no backup." You spend the next two weeks installing add-ons one by one, each one a manual <code>kubectl apply</code>. Three months later there\'s no record of which versions are installed where, and rebuilding a cluster takes a week of remembering. <em>Add-ons are infrastructure. Treat them as code from day 1.</em>',
    stamp_html='Day-1 add-on stack: <strong>CoreDNS</strong> (kubeadm installs; customise for stub zones), <strong>metrics-server</strong> (HPA + kubectl top), <strong>Gateway controller</strong> (Envoy Gateway / Cilium Gateway / Contour — Ingress NGINX EOL 2026), <strong>cert-manager</strong>, <strong>CSI driver</strong> + <strong>snapshot-controller</strong>, <strong>ExternalDNS</strong>, <strong>SOPS or Sealed Secrets</strong>, <strong>kube-prometheus-stack</strong>, <strong>Loki or Vector + S3</strong>, <strong>Kyverno</strong>, <strong>Falco</strong>. Install via <strong>Argo CD App-of-Apps</strong> from git.',
    district_pin="kf-site05",
    district_label="Outbuildings",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why add-ons need their own discipline",
            body_html="""    <p>kubeadm gives you the apartment building. Add-ons are everything else humans expect to live there: water (DNS), power (metrics), mail (Gateway / Ingress), security (cert-manager + policy), the basement (storage CSI), the security camera system (Falco), the maintenance log (logging stack), the energy meter (monitoring). Without these, the building is structurally complete but uninhabitable.</p>
    <p>Critical principle: <strong>add-ons are infrastructure</strong>, not "things ops installs by hand." Treat them as code: pinned versions, declarative manifests, GitOps reconciliation. The cluster reconciles its own add-on stack from git the same way Deployments reconcile their Pods.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The day-1 stack",
            h2="What every cluster needs",
            body_html="""    <table class="data-table">
      <thead><tr><th>Add-on</th><th>What it does</th><th>Common choice</th></tr></thead>
      <tbody>
        <tr><td>CoreDNS</td><td>In-cluster DNS</td><td>kubeadm-installed; customise via ConfigMap</td></tr>
        <tr><td>metrics-server</td><td>Pod/node CPU+memory for HPA, kubectl top</td><td>kubernetes-sigs/metrics-server</td></tr>
        <tr><td>Gateway controller</td><td>L7 traffic ingress (host/path routing, TLS)</td><td>Envoy Gateway, Cilium Gateway, Contour</td></tr>
        <tr><td>cert-manager</td><td>App-layer X.509 issuance + rotation</td><td>cert-manager.io + Let\'s Encrypt or Vault PKI</td></tr>
        <tr><td>CSI driver</td><td>Persistent storage</td><td>Longhorn (on-prem block), Rook-Ceph, vSphere CSI</td></tr>
        <tr><td>snapshot-controller</td><td>VolumeSnapshot support</td><td>kubernetes-csi/external-snapshotter</td></tr>
        <tr><td>ExternalDNS</td><td>Sync K8s Services + Ingresses to DNS provider</td><td>kubernetes-sigs/external-dns</td></tr>
        <tr><td>Sealed Secrets / SOPS</td><td>Git-stored encrypted secrets</td><td>bitnami-labs/sealed-secrets, getsops/sops</td></tr>
        <tr><td>kube-prometheus-stack</td><td>Prometheus + Grafana + AlertManager</td><td>prometheus-community/kube-prometheus-stack</td></tr>
        <tr><td>Logging</td><td>Cluster log collection</td><td>Loki + Vector + S3, or ELK, or vendor</td></tr>
        <tr><td>Policy engine</td><td>Admission policies</td><td>Kyverno (or OPA Gatekeeper)</td></tr>
        <tr><td>Runtime security</td><td>Syscall-level threat detection</td><td>Falco</td></tr>
        <tr><td>Argo CD</td><td>GitOps for everything above</td><td>argoproj/argo-cd</td></tr>
      </tbody>
    </table>""",
        ),
        Section(
            eyebrow="Section 1.7 · The bootstrap-Argo-CD problem",
            h2="Chicken and egg: who installs Argo CD?",
            body_html="""    <p>Argo CD will reconcile every other add-on from git — but Argo CD itself has to be installed somehow. Three patterns:</p>
    <ul>
      <li><strong>Bootstrap script</strong>: a small shell + Helm one-liner that installs Argo CD, then applies a single \"root\" Application that points at the rest of git. After that initial bootstrap, Argo CD manages itself.</li>
      <li><strong>Cluster API + ClusterResourceSet</strong>: in CAPI environments, a ClusterResourceSet attaches Argo CD to every new workload cluster automatically.</li>
      <li><strong>Talos extension</strong>: bake the Argo CD manifests into the Talos machine-config so they apply at first boot.</li>
    </ul>
    <p>The standard repo layout:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>k8s-platform/
├── bootstrap/argocd-install.sh
├── apps/
│   ├── root.yaml                 # App-of-Apps pointing at apps/*
│   ├── coredns/
│   ├── metrics-server/
│   ├── gateway-envoy/
│   ├── cert-manager/
│   ├── csi-longhorn/
│   ├── kube-prometheus-stack/
│   └── ...
└── overlays/{prod,staging,dev}/</code></pre>""",
        ),
        Section(
            eyebrow="Section 1.9 · Versioning + lifecycle",
            h2="Pinning, upgrading, retiring",
            body_html="""    <p>Each add-on is a separate project with its own release cadence. Treat them like dependencies in a programming language:</p>
    <ul>
      <li><strong>Pin versions</strong> in Helm chart references. Never use \"latest\" on production.</li>
      <li><strong>Update intentionally</strong>: PR to bump version, Argo CD detects diff, reviewer approves the resulting object diff before sync.</li>
      <li><strong>Test on staging cluster first.</strong> Same Helm version + same K8s version.</li>
      <li><strong>Retire EOL add-ons.</strong> Ingress NGINX is EOL end of 2026 — migrate to a Gateway-API-conformant controller.</li>
    </ul>
    <p>Special-case: <strong>dashboard</strong>. The Kubernetes Dashboard is included in many install guides but rarely justified for production — Grafana + Hubble + ArgoCD UI cover the use cases more securely. If you do install it, lock it down (auth, RBAC, no NodePort/LoadBalancer expose).</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For air-gapped: every add-on\'s images need to live in your internal registry. Helm charts often default to images on Docker Hub / Quay; override with <code>--set image.registry=harbor.corp</code>. Rebuild the bootstrap with these overrides.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='Your team installs add-ons via <code>kubectl apply</code> by hand on each cluster. Six months in, dev/staging/prod versions have drifted. What\'s the cure?',
            options=[
                ('a) Document everything in a wiki', False),
                ('b) Move every add-on into a git repo with Helm charts + pinned versions; install via Argo CD; let drift be impossible by structure', True),
                ('c) Ban kubectl apply', False),
            ],
            feedback='<strong>Answer: b.</strong> Documentation is no substitute for declarative reconciliation. With Argo CD + git, the cluster pulls its add-on stack from a single source of truth. Drift = git diff. Adding a new cluster = pointing Argo CD at the same git path. The wiki becomes the README in the same repo.',
        ),
    },
    before_after_before='<p>Add-ons installed by hand, one per ticket. No record of versions. \"Why does staging have 1.14 and prod has 1.11?\" answered with \"someone upgraded staging.\" Add-on outage requires log archeology to know what should be running.</p>',
    before_after_after='<p>One git repo. Argo CD reconciles every add-on. <code>kubectl get applications -n argocd</code> shows current state. Versions pinned. Adding a cluster = pointing Argo CD at the same path. Outages = git revert + sync.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Add-on stack as code is the difference between operating one cluster and operating a fleet.</p>',
    analogy_intro_html='<p>Outbuildings is the fifth site. The main house is up; the wiring is in. Now the property needs the supporting buildings: well house (DNS), shed (metrics), garage (Gateway), workshop (cert-manager), root cellar (storage CSI), watchtower (Falco), library (logging), barn (monitoring). Each outbuilding has its own purpose, but they all need to be planned together: where the path runs, where the power feeds in, who maintains them. The general contractor (Argo CD) coordinates: pulls all the building plans from git, reconciles them onto the property, keeps them updated.</p>',
    translation_rows=[
        ('Well house (always-on water)', 'CoreDNS'),
        ('Shed with the meter readings', 'metrics-server'),
        ('Garage facing the road', 'Gateway controller (Envoy / Cilium / Contour)'),
        ('Notary workshop with stamping press', 'cert-manager'),
        ('Root cellar', 'CSI driver + snapshot-controller'),
        ('Address-book sign at the gate', 'ExternalDNS'),
        ('Locked safe with vault keys', 'Sealed Secrets / SOPS'),
        ('Library + observatory', 'Logging + monitoring stacks'),
        ('Watchman + alarm panel', 'Kyverno + Falco'),
        ('General contractor coordinating it all', 'Argo CD App-of-Apps'),
    ],
    analogy_stops="The analogy stops here: real add-ons aren\'t separate buildings — they\'re Pods running on the same nodes as workloads, sharing the cluster\'s resources. Capacity planning has to account for the add-on stack\'s baseline load (~10-15% of cluster CPU/memory).",
    eli5='The house is built and wired. Now you build the well, the shed, the garage, the watchman\'s post — all the small buildings that make a homestead actually work.',
    eli10="kubeadm + CNI = bare cluster. Day-1 add-ons (~10): CoreDNS, metrics-server, Gateway controller, cert-manager, CSI + snapshot-controller, ExternalDNS, Sealed Secrets / SOPS, kube-prometheus-stack, Loki / Vector for logs, Kyverno, Falco. Install via Argo CD from a git repo (App-of-Apps pattern). Pin versions. Test on staging first. Treat the whole stack as code.",
    scenarios=[
        Scenario(name='A SaaS shipping the same add-on stack to 8 clusters', body='Single git repo. Argo CD on each cluster points at the same path with cluster-specific Kustomize overlays. New cluster create = bootstrap script installs Argo CD + applies the root App. 90 minutes from kubeadm done to fully populated cluster.'),
        Scenario(name='A bank with FIPS + air-gap requirements', body='Internal Harbor mirror with all add-on images. Argo CD bootstrap script overrides image registries. Custom cert-manager Issuer pointing at internal Vault PKI. ExternalDNS uses internal CoreDNS (not Route53). Same Argo CD pattern; different registry + DNS configs.'),
        Scenario(name='A startup graduating from "kubectl apply" to GitOps', body='First cluster: 18 manual installs. Migration: clone stack into a git repo, install Argo CD, import existing resources via <code>argocd app create --upsert</code>. Two weeks of validation. Then turn off manual access. Drift impossible.'),
        Scenario(name='A team retiring Ingress NGINX before EOL', body='Plan: install Envoy Gateway alongside Ingress NGINX. Migrate one Ingress at a time to HTTPRoute. Validate. Decommission Ingress NGINX. Deadline: end of 2026 (when ingress-nginx EOLs). Started Q2; finished Q4.'),
    ],
    misconceptions=[
        Misconception(myth='\"Argo CD is overkill for a single cluster.\"', truth='Even one cluster benefits from declarative reconciliation: drift detection, audit log via git, easy disaster recovery (cluster gone → new kubeadm + bootstrap Argo CD + git reconciles everything). The overhead of Argo CD itself is ~50 MB.'),
        Misconception(myth='\"Helm + a Makefile is good enough.\"', truth='Works until two clusters diverge or someone hand-patches a resource and forgets to update the Makefile. Argo CD detects drift; <code>helm install</code> doesn\'t.'),
        Misconception(myth='\"Add-ons are install-and-forget.\"', truth='Each add-on has its own release cadence + CVE history + breaking-change pattern. Treat them like any other dependency: review changelogs before bumping, test on staging, monitor deprecations.'),
    ],
    flashcards=[
        Flashcard(front='Why install Argo CD first?', back='Bootstraps the GitOps loop. Once installed, Argo CD installs every other add-on from git. Eliminates "kubectl apply by hand" drift across clusters.'),
        Flashcard(front='What\'s App-of-Apps?', back='Argo CD pattern: a single \"root\" Application points at a git path containing other Application manifests. Argo CD syncs the root, which creates/updates all the children. One sync = full add-on stack.'),
        Flashcard(front='kube-prometheus-stack — what\'s in it?', back='Helm chart bundling Prometheus + Grafana + AlertManager + node-exporter + kube-state-metrics + ServiceMonitor + PrometheusRule CRDs. The de-facto vanilla monitoring stack.'),
        Flashcard(front='Sealed Secrets vs SOPS?', back='Sealed Secrets: cluster controller decrypts on apply; secret encrypted with cluster public key (per-cluster). SOPS: encrypts at file layer with PGP/age/KMS; decrypts in CI. Either lets you commit secrets to git.'),
        Flashcard(front='Why no Kubernetes Dashboard in production?', back='Auth + RBAC are easy to misconfigure. Grafana + Hubble + Argo CD UI cover most use cases more safely. If you do install Dashboard, lock it down behind SSO + RBAC + no NodePort/LB expose.'),
        Flashcard(front='Snapshot-controller — what\'s it for?', back='K8s SIG-Storage component that turns VolumeSnapshot API objects into CSI snapshot calls. Required for any CSI driver supporting snapshots. Separate from the CSI driver itself; install once cluster-wide.'),
        Flashcard(front='ExternalDNS — what does it do?', back='Watches K8s Services + Ingresses + Gateways with hostname annotations; syncs corresponding records in your DNS provider (Route53, Cloud DNS, RFC2136 internal). Eliminates the \"someone forgot to add the DNS record\" failure mode.'),
        Flashcard(front='Argo CD on every cluster vs central?', back='Each cluster runs its own Argo CD pulling from git is the most resilient pattern (cluster fully self-managing). Central Argo CD pushing to many clusters is simpler but a SPOF. Most fleets land on per-cluster.'),
    ],
    quizzes=[
        Quiz(prompt='You\'re about to bootstrap a fresh cluster. What order do you install the add-ons?', answer='<strong>(1) CNI (V4)</strong> — until done, every node NotReady. <strong>(2) CoreDNS</strong> (kubeadm installs by default; customise after). <strong>(3) Argo CD</strong> (the meta-installer for everything else). <strong>(4) Argo CD installs the rest</strong> from git: metrics-server (so HPAs work), CSI + snapshot-controller (so PVs work), Gateway controller + cert-manager (so external access works), ExternalDNS (so DNS works), Sealed Secrets / SOPS (so secrets can come from git), kube-prometheus-stack (so you can see anything), logging stack (so you can debug), Kyverno + Falco (so policy enforcement is on). Order matters because some add-ons depend on others (cert-manager needs CRDs from snapshot-controller? no — just sequential). Use Argo CD sync waves (annotations) for explicit ordering of dependent apps.'),
        Quiz(prompt='Your <code>helm install kube-prometheus-stack</code> succeeds but Prometheus Pods crash-loop with <code>permission denied: /prometheus</code>. Diagnosis?', answer='Storage ownership / fsGroup mismatch. Prometheus runs as a non-root UID; the PV mounted at <code>/prometheus</code> is owned by root. <strong>Fix:</strong> set <code>prometheus.prometheusSpec.securityContext.fsGroup: 65534</code> in values.yaml. The kubelet (with most CSI drivers) <code>chown</code>s the PV to fsGroup at mount. <strong>Verify:</strong> exec into the Pod, <code>ls -la /prometheus</code> should show 65534. If still failing: PV provisioner doesn\'t support fsGroup; use an init container to chown, or pick a different StorageClass. <strong>This is the most common Helm chart deployment pain point</strong> — the chart values often need cluster-specific tuning.'),
        Quiz(prompt='You\'re asked to migrate a 30-Ingress cluster off Ingress NGINX before EOL. <strong>Click for the playbook. ▼</strong>', cyoa=True, cyoa_tag='the playbook', answer='<strong>(1) Pick replacement Gateway controller.</strong> Envoy Gateway (modern default), Cilium Gateway (if Cilium is your CNI), Contour (CNCF mature). Install alongside Ingress NGINX in the cluster. <strong>(2) Convert Ingress YAML to HTTPRoute.</strong> Use <code>InGate</code> tool (kubernetes/ingress-nginx provides it) for bulk translation. Manually fix the ones with vendor annotations. <strong>(3) Per-host migration.</strong> Each Ingress has a hostname. For one host: deploy the new HTTPRoute pointing at the same Service; keep Ingress NGINX serving the same host until you swap DNS. <strong>(4) Smoke test the host on the new Gateway</strong> by editing <code>/etc/hosts</code> on a test machine to point at the Gateway\'s LB IP. Once happy, flip ExternalDNS / DNS to the new Gateway. <strong>(5) Repeat per host.</strong> 30 hosts × ~30 min each = 1-2 sprints if anyone else is on the project. <strong>(6) Decommission Ingress NGINX</strong> when zero hosts remain. <code>helm uninstall ingress-nginx</code>. <strong>Result:</strong> all traffic on Gateway API, no EOL panic, no big-bang switch.'),
    ],
    glossary=[
        GlossaryItem(name='CoreDNS', definition='Default in-cluster DNS server. kubeadm installs it. Customise via the <code>coredns</code> ConfigMap in <code>kube-system</code>.'),
        GlossaryItem(name='metrics-server', definition='Aggregates Pod/node CPU+memory metrics from kubelets. Required for HPA + <code>kubectl top</code>.'),
        GlossaryItem(name='Gateway controller', definition='Implements Gateway API CRDs. Envoy Gateway (modern), Cilium Gateway, Contour. Replaces Ingress NGINX.'),
        GlossaryItem(name='cert-manager', definition='K8s-native X.509 issuance + rotation. Issuers: Let\'s Encrypt, Vault, internal CA.'),
        GlossaryItem(name='CSI driver + snapshot-controller', definition='Storage interface + the controller that processes VolumeSnapshot API objects.'),
        GlossaryItem(name='ExternalDNS', definition='Syncs K8s Services / Ingresses / Gateways with hostnames into your DNS provider.'),
        GlossaryItem(name='Sealed Secrets', definition='Bitnami project: encrypts a Secret with a cluster-public-key so the encrypted form lives in git. Cluster controller decrypts.'),
        GlossaryItem(name='SOPS', definition='Mozilla project: file-level encryption with PGP/age/KMS. Decryption usually in CI.'),
        GlossaryItem(name='kube-prometheus-stack', definition='Helm chart bundling Prometheus + Grafana + AlertManager + node-exporter + kube-state-metrics + Operator CRDs.'),
        GlossaryItem(name='Loki / Vector', definition='Lightweight log aggregation (Loki) + log shipping (Vector). Common pairing with S3-compatible storage.'),
        GlossaryItem(name='Kyverno', definition='K8s-native policy engine. YAML policies for validate/mutate/generate/cleanup/verifyImages.'),
        GlossaryItem(name='Falco', definition='CNCF runtime security tool. eBPF-based syscall monitoring with rule engine.'),
        GlossaryItem(name='Argo CD App-of-Apps', definition='Pattern: one parent App in Argo CD points at a git path containing many child App manifests. Bootstrap many add-ons in one sync.'),
    ],
    recap_lead='~10 day-1 add-ons installed via Argo CD App-of-Apps from git. Pin versions. Test on staging. Same stack across every cluster.',
    recap_next='<strong>Next — V6: Cluster Configuration.</strong> The knobs you tune after install: API server flags, audit, encryption, kubelet eviction, scheduler profiles, RuntimeClass.',
)
