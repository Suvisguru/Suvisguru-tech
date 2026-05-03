from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Frame raising: kubeadm phases shown as numbered framing steps; control-plane stones being placed; workers joining via tokens.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">FRAME RAISING · kubeadm BOOTSTRAP</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">kubeadm INIT PHASES (in order)</text>
    <rect x="14" y="34" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="60" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">1 preflight</text><text x="60" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">checks env</text>
    <rect x="112" y="34" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="158" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">2 certs</text><text x="158" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">PKI generated</text>
    <rect x="210" y="34" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="256" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">3 kubeconfig</text><text x="256" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">admin/sched</text>
    <rect x="308" y="34" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="354" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">4 control-plane</text><text x="354" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">static pods</text>
    <rect x="406" y="34" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="452" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">5 etcd</text><text x="452" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">stacked</text>
    <rect x="504" y="34" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="550" y="50" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">6 mark-cp</text><text x="550" y="62" text-anchor="middle" font-size="7" fill="#5A4F45">taint + label</text>
    <rect x="14" y="76" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="60" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">7 bootstrap-token</text>
    <rect x="112" y="76" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="158" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">8 kubelet</text><text x="158" y="104" text-anchor="middle" font-size="7" fill="#5A4F45">starts</text>
    <rect x="210" y="76" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="256" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">9 addon</text><text x="256" y="104" text-anchor="middle" font-size="7" fill="#5A4F45">CoreDNS, kube-proxy</text>
    <rect x="308" y="76" width="92" height="34" rx="3" fill="#FBF1D6"/><text x="354" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#8B5A00">10 upload-certs</text>
    <rect x="406" y="76" width="190" height="34" rx="3" fill="#5A9F7A"/><text x="501" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">control-plane joined!</text><text x="501" y="104" text-anchor="middle" font-size="7" fill="#FBE8DC">cp-2 + cp-3 join via certKey</text>
    <rect x="14" y="118" width="282" height="34" rx="3" fill="#3F4A5E"/><text x="155" y="134" text-anchor="middle" font-size="9" font-weight="700" fill="#FBF1D6">workers join via bootstrap token</text><text x="155" y="146" text-anchor="middle" font-size="7" fill="#FBF1D6">kubeadm join &lt;LB&gt;:6443 --token X --discovery-token-ca-cert-hash Y</text>
    <rect x="306" y="118" width="290" height="34" rx="3" fill="#A04832"/><text x="451" y="134" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">kubectl get nodes  →  STATUS=Ready</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="03",
    title_short="kubeadm bootstrap",
    title_full="V3 · kubeadm Cluster Bootstrap End-to-End",
    title_html="K-VAN V3 · kubeadm Cluster Bootstrap",
    module_eyebrow="Module V3 · raising the frame",
    hero_sub_html='<code>kubeadm</code> is the standard tool for vanilla K8s. It generates certs, places static pods for the control plane, joins workers via tokens. <strong>Master kubeadm and you can install K8s anywhere.</strong> Plus the alternatives — kubespray, RKE2, k3s, Talos, Cluster API.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='<code>kubeadm init</code> hangs at \"Waiting for the kubelet to boot up the control plane.\" The default error is one line; the cause could be 12 different things — wrong API server LB IP, missing CA SAN, port blocked, time skew, certificate already exists from a previous attempt, image pull failed silently, kubelet config mismatched cgroup driver. Without a mental model of what <em>phase</em> is failing, you\'re guessing. This module is the model.',
    stamp_html='<code>kubeadm init</code> runs <strong>10 phases</strong> in order: preflight, certs, kubeconfig, control-plane (static pods), etcd, mark-cp, bootstrap-token, kubelet, addon (CoreDNS + kube-proxy), upload-certs. <code>kubeadm join</code> uses a bootstrap token + CA hash (or certificate key for control-plane join). For HA: <strong>API server LB</strong> (kube-vip / HAProxy / external) + 3+ CP nodes. Alternatives: kubespray, RKE2, k3s, Talos, Cluster API.',
    district_pin="kf-site03",
    district_label="Frame Raising",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="kubeadm's mental model",
            body_html="""    <p>kubeadm is a <em>cluster bootstrapper</em>, not a cluster lifecycle manager. It does one thing exceptionally well: take a prepared host (V2) and turn it into a working K8s control plane or worker. After that, the cluster is yours to manage — kubeadm doesn\'t install Argo CD, doesn\'t handle backup, doesn\'t do upgrades automatically (it does help with kubelet/control-plane upgrade — see V8).</p>
    <p>The kubeadm workflow:</p>
    <ol>
      <li><code>kubeadm init</code> on the first control-plane node (with HA: configure API LB + use <code>--upload-certs</code>).</li>
      <li><code>kubeadm join --control-plane</code> on additional control-plane nodes (with the cert key from step 1).</li>
      <li><code>kubeadm join</code> on each worker node (with the bootstrap token + CA hash).</li>
      <li>Install a CNI (Lesson V4) — until then, nodes show <code>NotReady</code>.</li>
      <li>Install add-ons (Lesson V5) — usually via Argo CD pointed at git.</li>
    </ol>
    <p>The whole bootstrap is YAML-configurable via <code>kubeadm config</code> objects.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · The kubeadm config API",
            h2="Four configuration objects",
            body_html="""    <p>Instead of <code>kubeadm init --apiserver-advertise-address=...</code> with 30 flags, write a YAML file:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># kubeadm-config.yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 192.168.1.10
nodeRegistration:
  criSocket: unix:///run/containerd/containerd.sock
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: v1.36.0
controlPlaneEndpoint: api.cluster.corp:6443       # the LB
networking:
  podSubnet: 192.168.224.0/20
  serviceSubnet: 10.96.0.0/12
apiServer:
  certSANs: [api.cluster.corp, 192.168.1.100]    # the LB IP/name
  extraArgs:
    audit-log-path: /var/log/audit.log
    encryption-provider-config: /etc/kubernetes/enc/encryption.yaml
etcd:
  local: { dataDir: /var/lib/etcd, extraArgs: { quota-backend-bytes: '8589934592' } }
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
systemReserved: { cpu: '500m', memory: '1Gi' }
kubeReserved:   { cpu: '500m', memory: '1Gi' }
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: ipvs                                       # or empty if Cilium replaces kube-proxy</code></pre>
    <p>Then: <code>kubeadm init --config kubeadm-config.yaml --upload-certs</code>. The <code>--upload-certs</code> flag stores control-plane certs in a Secret keyed by a generated <em>certificate key</em> — additional CP nodes use that key to fetch certs without manual file copy.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · HA control plane + LB",
            h2="Three CP nodes behind a virtual IP",
            body_html="""    <p>Single-control-plane is fine for labs. Production needs ≥ 3 CP nodes behind a load balancer. The LB is the <code>controlPlaneEndpoint</code> in the kubeadm config. Three popular options:</p>
    <ul>
      <li><strong>kube-vip</strong> — runs as a static Pod on each CP node; one CP holds the VIP via ARP/BGP. Self-contained, no extra infra. The 2026 default for kubeadm HA.</li>
      <li><strong>HAProxy + keepalived</strong> — classic. HAProxy load-balances; keepalived provides the VIP failover. More moving parts but battle-tested.</li>
      <li><strong>External LB</strong> — a hardware LB (F5, Citrix), MetalLB, or cloud LB. Outside the cluster; predictable.</li>
    </ul>
    <p>The LB must point at <code>:6443</code> on every CP node. Health check on <code>/livez</code> or TCP 6443. The LB IP/name goes into the API server's certificate SANs (otherwise clients hitting the LB get cert-name-mismatch errors).</p>
    <p>HA bootstrap order:</p>
    <ol>
      <li>Start the LB pointing at cp-1 only (or all three with cp-1 as the only healthy backend).</li>
      <li><code>kubeadm init --config ... --upload-certs</code> on cp-1. Output includes both a <em>worker join command</em> and a <em>control-plane join command</em> with a certificate key.</li>
      <li><code>kubeadm join &lt;LB&gt;:6443 --token X --discovery-token-ca-cert-hash sha256:Y --control-plane --certificate-key Z</code> on cp-2, cp-3.</li>
      <li>Workers: <code>kubeadm join &lt;LB&gt;:6443 --token X --discovery-token-ca-cert-hash sha256:Y</code>.</li>
    </ol>""",
        ),
        Section(
            eyebrow="Section 1.9 · Alternatives + when to use them",
            h2="kubespray, RKE2, k3s, Talos, Cluster API",
            body_html="""    <ul>
      <li><strong>kubespray</strong> — Ansible playbooks installing kubeadm under the hood. Good for hybrid teams already in Ansible. Complex but flexible.</li>
      <li><strong>kOps</strong> — declarative cluster lifecycle on cloud (mostly AWS). State in S3; kubeadm-like under the hood. Mature.</li>
      <li><strong>RKE2</strong> — Rancher\'s production K8s distribution. Single binary, FIPS-certified, focuses on regulated environments. CIS-hardened defaults.</li>
      <li><strong>k3s</strong> — Rancher\'s lightweight distribution. Single binary, &lt; 100 MB, ideal for edge / IoT / small clusters. Production-grade for its niche.</li>
      <li><strong>Talos Linux</strong> — immutable OS designed for K8s. No SSH; machine-config API. <code>talosctl apply-config</code> instead of <code>kubeadm init</code>. Modern + opinionated.</li>
      <li><strong>Cluster API (CAPI)</strong> — declarative K8s-on-K8s. A management cluster runs CAPI controllers; workload clusters are <code>Cluster</code> + <code>Machine</code> CRDs. Provider plugins: CAPV (vSphere), CAPA (AWS), CAPZ (Azure), CAPG (GCP), CAPD (Docker — for testing). The right answer when you operate many clusters.</li>
    </ul>
    <p><strong>"Kubernetes the Hard Way"</strong> (Kelsey Hightower) is the educational walkthrough — install K8s without any bootstrapper, by hand, on raw VMs. Don\'t do this for production; do it once to understand what kubeadm hides.</p>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For 2026 production self-managed clusters: kubeadm is the most common path; Talos has gained massive ground for new clusters; CAPI is the standard for fleet management. RKE2 is the safe pick in regulated industries. k3s for edge.</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question='You\'re bootstrapping HA. The first <code>kubeadm init</code> succeeded but the join command for cp-2 fails with <code>error retrieving certificates from upload-certs Secret</code>. Diagnosis?',
            options=[
                ('a) cp-2 has the wrong CA', False),
                ('b) The certificate key has expired (default 2-hour TTL after <code>--upload-certs</code>)', True),
                ('c) Network is broken', False),
            ],
            feedback='<strong>Answer: b.</strong> The cert-key Secret created by <code>--upload-certs</code> is auto-deleted after 2 hours. Either re-run <code>kubeadm init phase upload-certs --upload-certs</code> on cp-1 to regenerate, or use <code>kubeadm certs certificate-key</code> + <code>kubeadm init phase upload-certs --upload-certs --certificate-key &lt;key&gt;</code>. <em>Common gotcha — bootstrap CP nodes promptly after init.</em>',
        ),
    },
    before_after_before='<p>Manual install: SSH each node, generate certs by hand, distribute kubeconfigs, write systemd units, configure each component. Hours per node, drift-prone, no clear procedure to recover from a failed bootstrap.</p>',
    before_after_after='<p>One YAML file (<code>kubeadm-config.yaml</code>) committed to git. <code>kubeadm init</code> on cp-1, two <code>kubeadm join --control-plane</code> on cp-2/3, three <code>kubeadm join</code> on workers. CNI installed, cluster <code>Ready</code>. Reproducible from the same YAML; documented bootstrap.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">kubeadm is the lingua franca of vanilla K8s. Even kubespray, kOps, and most distros use kubeadm under the hood. Master it.</p>',
    analogy_intro_html='<p>Frame Raising is the third site. The blueprint is drawn (V1), the soil is prepped (V2). Now you raise the frame: corner posts (control-plane nodes) first, anchored deep into the foundation (etcd). The first corner post is the hardest — it requires the survey lines to be exactly right. Once it stands, the next two come up quickly using the same templates and ties (cert key, bootstrap token). Workers are the rafters that span between the posts; they connect via standard joints (<code>kubeadm join</code>).</p>',
    translation_rows=[
        ('First corner post (hardest)', '<code>kubeadm init</code> on cp-1'),
        ('Posts 2 and 3', '<code>kubeadm join --control-plane</code> on cp-2/3'),
        ('Foundation depth', 'etcd (stacked or external)'),
        ('Plumb line + survey markers', 'API LB IP + cert SANs'),
        ('Ties between posts', 'Certificate key + bootstrap token'),
        ('Rafters spanning the frame', 'Worker nodes (<code>kubeadm join</code>)'),
        ('Pre-cut framing kit (no on-site measuring)', 'kubeadm config YAML'),
        ('Alternative builders', 'kubespray / RKE2 / k3s / Talos / Cluster API'),
    ],
    analogy_stops="The analogy stops here: real cluster bootstrap involves cryptographic key exchange, x509 cert issuance, and gRPC handshakes — not lumber and hammers. The framing metaphor undersells the precision needed at the cert + token layer.",
    eli5='You build a treehouse. First you put up one corner post very carefully. Then you put up the other corner posts using the same plans. Then you nail in the platform.',
    eli10="kubeadm bootstraps K8s in 10 phases. <code>kubeadm init</code> on the first CP node generates certs + starts static-pod control plane + etcd. Additional CP nodes join via certificate key (<code>--upload-certs</code>). Workers join via bootstrap token + CA hash. HA needs an API server LB pointing at all CP nodes. Configure via YAML (kubeadm-config), not flags. Alternatives: kubespray (Ansible), kOps (cloud), RKE2 (Rancher), k3s (edge), Talos (immutable), Cluster API (declarative fleet).",
    scenarios=[
        Scenario(name='A startup using kube-vip + kubeadm for HA', body='3 control-plane bare-metal nodes. kube-vip static pod on each holds a shared VIP via ARP. <code>controlPlaneEndpoint: api.k8s.corp:6443</code> resolves to the VIP. <code>kubeadm init --config ... --upload-certs</code> on cp-1; cp-2/3 join with the printed cert key. Workers join over the next hour. Total bootstrap time: ~45 minutes from prepped nodes.'),
        Scenario(name='A bank using external HAProxy + keepalived', body='Dedicated LB pair. HAProxy front-ends 6443 → 3 CP backends. keepalived holds the VIP. Compliance team likes the explicit LB tier they can monitor + audit. Bootstrap is the same kubeadm pattern; just <code>controlPlaneEndpoint</code> points at the HAProxy VIP.'),
        Scenario(name='A platform team using Cluster API + Talos', body='Management cluster runs CAPI + Cluster Provider Talos. Workload clusters declared as YAML: <code>kind: Cluster</code> + <code>kind: TalosControlPlane</code> + <code>kind: MachineDeployment</code>. New cluster = git PR + CAPI provisions VMs (vSphere) + applies Talos config + cluster comes up. Fleet of 12 clusters managed declaratively.'),
        Scenario(name='An edge team using k3s on 200 retail stores', body='Each store has a single-node k3s install (everything in one binary, ~80MB RAM at idle). Argo CD syncs from the central git repo. Per-store config differences via Kustomize overlays. Reboot recovery is 30 seconds. Vanilla K8s primitives, micro footprint.'),
    ],
    misconceptions=[
        Misconception(myth='\"kubeadm installs everything I need.\"', truth='kubeadm bootstraps the control plane + helps workers join. It does NOT install a CNI (cluster is NotReady until you do), an ingress controller, cert-manager, or any other add-ons. V4 + V5 cover those.'),
        Misconception(myth='\"<code>kubeadm reset</code> cleans everything.\"', truth='kubeadm reset removes most cluster state but leaves: the CNI plugin\'s data (<code>/etc/cni/net.d/*</code>), iptables rules from kube-proxy, etcd data on dedicated mounts. After reset, also: <code>iptables -F + -t nat -F</code>, <code>ipvsadm --clear</code>, remove CNI configs, remove etcd dir. Otherwise the next init re-uses stale state.'),
        Misconception(myth='\"Cluster API is for huge orgs only.\"', truth='Even small teams benefit if they\'ll operate ≥ 3 clusters (dev/staging/prod, or per-tenant). The declarative model + provider plugins make per-cluster YAML changes way faster than running kubeadm 3 times.'),
    ],
    flashcards=[
        Flashcard(front='Four kubeadm config kinds?', back='InitConfiguration (per-host init), ClusterConfiguration (cluster-wide), KubeletConfiguration (per-node kubelet), KubeProxyConfiguration (kube-proxy mode + settings).'),
        Flashcard(front='What does <code>--upload-certs</code> do?', back='Stores the control-plane CA + signing keys in a Secret keyed by a generated certificate key. Additional CP nodes use that key in <code>kubeadm join --control-plane --certificate-key X</code> to fetch certs without manual file copy. 2-hour TTL.'),
        Flashcard(front='kubeadm join — two flavours?', back='Worker: <code>kubeadm join &lt;LB&gt;:6443 --token X --discovery-token-ca-cert-hash sha256:Y</code>. Control plane: same plus <code>--control-plane --certificate-key Z</code>.'),
        Flashcard(front='controlPlaneEndpoint?', back='The LB address (FQDN preferred) clients hit. Embedded into kubeconfigs + cert SANs. Required for HA; for single-CP, can be omitted (defaults to apiserver address).'),
        Flashcard(front='kube-vip vs HAProxy + keepalived?', back='kube-vip = single static pod, self-contained. HAProxy + keepalived = two-tier classic LB pair. kube-vip is the modern kubeadm HA default; HAProxy still common in regulated environments.'),
        Flashcard(front='Talos\'s answer to kubeadm?', back='<code>talosctl apply-config</code> with a machine-config YAML. The OS itself is the kubeadm equivalent — bootstrapping is just applying config to immutable nodes.'),
        Flashcard(front='What is Cluster API (CAPI)?', back='Declarative cluster lifecycle. A management cluster runs CAPI; workload clusters are CRDs (<code>Cluster</code>, <code>Machine</code>, <code>MachineDeployment</code>, <code>ControlPlane</code>). Provider plugins handle the underlying infra: CAPV (vSphere), CAPA, CAPZ, CAPG, CAPD.'),
        Flashcard(front='\"Kubernetes the Hard Way\" — for what?', back='Educational walkthrough: install K8s without any bootstrapper, on raw VMs, by hand. Reveals what kubeadm/Talos automate. Production: never. Once for understanding: highly recommended.'),
    ],
    quizzes=[
        Quiz(prompt='Your <code>kubeadm init</code> succeeds, but <code>kubectl get nodes</code> shows the CP node as <code>NotReady</code>. What\'s the next step?', answer='<strong>Install a CNI.</strong> The kubelet needs a CNI plugin to set up Pod networking; without one, every node stays NotReady. Standard procedure: <code>kubectl apply -f &lt;cni-manifest.yaml&gt;</code> (Cilium / Calico / etc., with the right Pod CIDR matching your kubeadm config). Wait 30-60s; node transitions to Ready. <strong>If still NotReady after CNI install:</strong> check the CNI Pods (<code>kubectl -n kube-system get pods | grep -i cni</code>), check kubelet logs, check the node\'s <code>/etc/cni/net.d/</code> for the CNI config file. Lesson V4 covers CNI selection + install in detail.'),
        Quiz(prompt='You\'re bootstrapping a fresh cluster and notice cp-1 has been up for 6 hours but cp-2 is still failing to join. The error says \"unable to fetch the kubeadm-certs Secret.\" Diagnosis?', answer='The certificate key Secret created by <code>--upload-certs</code> has a default 2-hour TTL — long expired. <strong>Two fixes:</strong> (1) Regenerate from cp-1: <code>sudo kubeadm init phase upload-certs --upload-certs</code> — outputs a new cert key. Use it in cp-2\'s join command. (2) Print a fresh full join command: <code>sudo kubeadm token create --print-join-command --certificate-key $(sudo kubeadm certs certificate-key)</code>. <strong>Process improvement:</strong> bootstrap all CP nodes within the first hour after init. If you can\'t, document the regenerate-cert-key step in your runbook.'),
        Quiz(prompt='You\'re asked to design a fleet management approach for 12 K8s clusters across 3 regions. <strong>Click for the Cluster API playbook. ▼</strong>', cyoa=True, cyoa_tag='the CAPI playbook', answer='<strong>(1) Build a management cluster.</strong> Single small kubeadm cluster (3 CP, 1-2 workers). This runs CAPI and the provider controllers. Backed up obsessively (it\'s your fleet\'s source of truth). <strong>(2) Pick providers.</strong> CAPV for vSphere, CAPA for AWS, CAPZ for Azure, CAPG for GCP, CAPD for Docker (testing). Install via Helm or Operator. <strong>(3) Define a cluster template.</strong> A YAML manifest (<code>Cluster</code> + <code>KubeadmControlPlane</code> + <code>MachineDeployment</code>) parameterised by region/size/version. Store in git. <strong>(4) Apply per workload cluster.</strong> Helm install with values; CAPI provisions infra (VMs / nodes), bootstraps K8s, and registers the new cluster in your management. <strong>(5) Continuous reconciliation.</strong> CAPI keeps each workload cluster in line with its declared spec. Node failure → CAPI replaces. Version bump in spec → rolling upgrade. <strong>(6) Backup + DR.</strong> Velero on the management cluster snapshots the CAPI state. Recovery means restoring management → CAPI re-discovers workload clusters via their kubeconfigs. <strong>Result:</strong> 12 clusters declared in 12 git PRs. Adding a 13th cluster is a YAML change, not a manual install. Worth the management-cluster overhead at ~5+ workload clusters.'),
    ],
    glossary=[
        GlossaryItem(name='kubeadm', definition='Standard Kubernetes cluster bootstrapper. Init + join commands; YAML config API.'),
        GlossaryItem(name='InitConfiguration', definition='kubeadm config kind for per-host init settings (advertise IP, CRI socket).'),
        GlossaryItem(name='ClusterConfiguration', definition='kubeadm config kind for cluster-wide settings (version, networking, apiserver flags, etcd).'),
        GlossaryItem(name='KubeletConfiguration', definition='kubeadm config kind for kubelet settings (cgroup driver, eviction, reserved resources).'),
        GlossaryItem(name='KubeProxyConfiguration', definition='kubeadm config kind for kube-proxy mode (iptables / ipvs / nftables) + settings.'),
        GlossaryItem(name='Bootstrap token', definition='Short-lived token for new nodes to authenticate to the cluster during join. <code>kubeadm token create</code>.'),
        GlossaryItem(name='Certificate key', definition='Short-lived (2h default) key encrypting the upload-certs Secret. Required for HA control-plane joins.'),
        GlossaryItem(name='controlPlaneEndpoint', definition='Cluster-wide LB address for the API server. Embedded in kubeconfigs + cert SANs.'),
        GlossaryItem(name='kube-vip', definition='Self-contained LB for kubeadm HA. Static pod holds a shared VIP via ARP/BGP.'),
        GlossaryItem(name='RKE2', definition='Rancher\'s production K8s distribution. Single binary, FIPS-capable, CIS-hardened defaults.'),
        GlossaryItem(name='k3s', definition='Rancher\'s lightweight K8s. Single binary, ~50MB RAM at idle. Edge / IoT / small clusters.'),
        GlossaryItem(name='Talos Linux', definition='Immutable OS for K8s. No SSH; <code>talosctl apply-config</code> instead of kubeadm.'),
        GlossaryItem(name='Cluster API (CAPI)', definition='Declarative K8s-on-K8s. Management cluster operates workload clusters via CRDs + provider plugins.'),
        GlossaryItem(name='Kubernetes the Hard Way', definition='Educational walkthrough: install K8s without bootstrappers. Useful for understanding what kubeadm hides.'),
    ],
    recap_lead='<code>kubeadm init</code> + <code>kubeadm join</code> bootstraps vanilla K8s in 10 phases. HA = API LB + 3 CP nodes + cert key + bootstrap token. Configure via YAML, not flags. Alternatives (kubespray / RKE2 / k3s / Talos / CAPI) for specific needs.',
    recap_next='<strong>Next — V4: CNI Installation and Networking.</strong> The cluster is NotReady until a CNI plugin is installed. Cilium, Calico, MTU tuning, kube-proxy replacement, the modern data planes.',
)
