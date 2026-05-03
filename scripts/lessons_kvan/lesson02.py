from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Land clearing site: a cleared patch with foundation stones marked, tools (kernel modules, sysctl values), a containerd toolbox, and a sign showing 'swap OFF'.">
  <rect width="680" height="220" rx="12" fill="#F5EFE3"/>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#3F4A5E" letter-spacing="1.5">LAND CLEARING · NODE PREP</text>
  <g transform="translate(40,50)">
    <rect width="600" height="160" rx="8" fill="#FFFFFF" stroke="#5A4F45" stroke-width="1.5"/>
    <text x="300" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="#5A4F45">PER-NODE PREP CHECKLIST</text>
    <rect x="14" y="34" width="140" height="40" rx="3" fill="#FBF1D6" stroke="#8B5A00"/><text x="84" y="50" text-anchor="middle" font-size="9" fill="#8B5A00" font-weight="700">kernel modules</text><text x="84" y="64" text-anchor="middle" font-size="7" fill="#5A4F45">overlay · br_netfilter</text>
    <rect x="160" y="34" width="140" height="40" rx="3" fill="#E0EEF3" stroke="#4A8FA8"/><text x="230" y="50" text-anchor="middle" font-size="9" fill="#3F4A5E" font-weight="700">sysctl</text><text x="230" y="64" text-anchor="middle" font-size="7" fill="#5A4F45">ip_forward · bridge-nf</text>
    <rect x="306" y="34" width="140" height="40" rx="3" fill="#FBE8DC" stroke="#A04832"/><text x="376" y="50" text-anchor="middle" font-size="9" fill="#A04832" font-weight="700">swap OFF</text><text x="376" y="64" text-anchor="middle" font-size="7" fill="#5A4F45">/etc/fstab + swapoff -a</text>
    <rect x="452" y="34" width="140" height="40" rx="3" fill="#E0EFE6" stroke="#3D7857"/><text x="522" y="50" text-anchor="middle" font-size="9" fill="#3D7857" font-weight="700">time sync</text><text x="522" y="64" text-anchor="middle" font-size="7" fill="#5A4F45">chrony / systemd-timesyncd</text>
    <rect x="14" y="84" width="140" height="40" rx="3" fill="#3F4A5E"/><text x="84" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">containerd 2.x</text><text x="84" y="114" text-anchor="middle" font-size="7" fill="#FBF1D6">SystemdCgroup=true</text>
    <rect x="160" y="84" width="140" height="40" rx="3" fill="#3F4A5E"/><text x="230" y="100" text-anchor="middle" font-size="9" fill="#FBF1D6" font-weight="700">CRI socket</text><text x="230" y="114" text-anchor="middle" font-size="7" fill="#FBF1D6">/run/containerd/containerd.sock</text>
    <rect x="306" y="84" width="140" height="40" rx="3" fill="#5A9F7A"/><text x="376" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">image pre-pull</text><text x="376" y="114" text-anchor="middle" font-size="7" fill="#FBE8DC">crictl pull or air-gap load</text>
    <rect x="452" y="84" width="140" height="40" rx="3" fill="#A04832"/><text x="522" y="100" text-anchor="middle" font-size="9" fill="#FFFFFF" font-weight="700">hardening</text><text x="522" y="114" text-anchor="middle" font-size="7" fill="#FBE8DC">SSH · auditd · firewall</text>
    <rect x="14" y="134" width="578" height="22" rx="3" fill="#FBF7F0" stroke="#9D9389"/><text x="303" y="148" text-anchor="middle" font-size="8" fill="#5A4F45" font-style="italic">order of operations: kernel modules → sysctl → runtime → swap-off → reboot test → kubeadm</text>
  </g>
</svg>"""

LESSON = LessonSpec(
    num="02",
    title_short="OS &amp; node prep",
    title_full="V2 · OS and Node Preparation for kubeadm",
    title_html="K-VAN V2 · OS and Node Preparation",
    module_eyebrow="Module V2 · the soil before the frame",
    hero_sub_html='Every <strong>self-managed</strong> K8s install fails the same way: the team skips a kernel module, leaves swap on, or misconfigures the cgroup driver. This module is the per-node checklist that makes <code>kubeadm init</code> work the first time.',
    hero_illu_svg=HERO_SVG,
    nightmare_html='You\'ve built three control-plane nodes and three workers. <code>kubeadm init</code> starts and then hangs. Hours later you find: the kernel\'s <code>br_netfilter</code> module wasn\'t loaded, so iptables can\'t see bridged traffic. Or swap was on and kubelet refused to start. Or containerd uses cgroupfs while kubelet expects systemd. <em>Each is a one-line fix; finding it from a hung install takes hours.</em> Today\'s lesson is the checklist.',
    stamp_html='Per-node prep, in order: <strong>kernel modules</strong> (<code>overlay</code>, <code>br_netfilter</code>), <strong>sysctl</strong> (<code>net.ipv4.ip_forward=1</code>, <code>net.bridge.bridge-nf-call-iptables=1</code>), <strong>swap OFF</strong>, <strong>time sync</strong>, <strong>container runtime</strong> (<code>containerd 2.x</code> with <code>SystemdCgroup=true</code>), <strong>image pre-pulling</strong> for air-gap. Reboot, sanity-check, then run kubeadm.',
    district_pin="kf-site02",
    district_label="Land Clearing",
    sections=[
        Section(
            eyebrow="Section 1 · Concept",
            h2="Why per-node prep exists",
            body_html="""    <p>Linux is configurable to a fault. K8s assumes a specific configuration: certain kernel modules loaded, certain sysctl values, no swap, a CRI-compatible runtime, the right cgroup driver. The kubelet and CNI plugins fail in confusing ways when these aren't right. The one good thing: the checklist is short and the same on every node.</p>
    <p>Your goal in V2 is a node that, when handed to <code>kubeadm</code>, joins the cluster cleanly. That means the same six categories on every node: kernel, network sysctl, swap, time, runtime, hardening.</p>""",
        ),
        Section(
            eyebrow="Section 1.5 · Kernel modules + sysctl",
            h2="What the cluster expects from the host",
            body_html="""    <p><strong>Modules to load at boot</strong> (write to <code>/etc/modules-load.d/k8s.conf</code>):</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>overlay
br_netfilter</code></pre>
    <p>Then <code>modprobe overlay</code> and <code>modprobe br_netfilter</code> for the running kernel.</p>
    <p><strong>sysctl values</strong> (<code>/etc/sysctl.d/k8s.conf</code>):</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1</code></pre>
    <p>Then <code>sysctl --system</code>. <code>br_netfilter</code> must be loaded before sysctl applies — order matters.</p>""",
        ),
        Section(
            eyebrow="Section 1.7 · Swap, time, runtime",
            h2="The other three categories",
            body_html="""    <p><strong>Swap.</strong> Kubelet refuses to start with swap enabled by default (you can enable swap support explicitly via <code>KubeletConfiguration</code> in K8s 1.28+, but most production clusters keep it off). Disable now and persist:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code>swapoff -a
sed -i '/ swap / s/^/#/' /etc/fstab</code></pre>
    <p><strong>Time sync.</strong> Certificates, etcd, and audit logs all assume monotonic time. Run <code>chrony</code> or <code>systemd-timesyncd</code>; verify with <code>chronyc tracking</code> (offset &lt; 100ms).</p>
    <p><strong>Container runtime.</strong> Install <code>containerd 2.x</code>:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># Generate default config
containerd config default | sudo tee /etc/containerd/config.toml

# CRITICAL: enable systemd cgroup driver to match kubelet
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# Optional: configure registry mirror for air-gap or ratelimit avoidance
# [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
#   endpoint = ["https://harbor.corp/v2/dockerhub-proxy"]

systemctl restart containerd
crictl info | grep -i cgroup  # verify systemd</code></pre>""",
        ),
        Section(
            eyebrow="Section 1.9 · Hardening + image pre-pull",
            h2="Beyond minimum-viable",
            body_html="""    <p><strong>Node hardening</strong> (cover at minimum):</p>
    <ul>
      <li>SSH: key-only auth (<code>PasswordAuthentication no</code>); root login disabled; SSH on standard port behind a bastion.</li>
      <li>auditd: enable at boot; ship logs to a central collector.</li>
      <li>Firewall: <code>ufw</code> / <code>firewalld</code> allowing only required ports (6443 to CP, 10250 kubelet, etcd 2379-2380 between CP, CNI overlay UDP if applicable).</li>
      <li>SELinux/AppArmor: keep enabled (<code>setenforce 1</code> on RHEL family). K8s components have AppArmor profiles; PSA <code>restricted</code> requires AppArmor.</li>
      <li>Log rotation: <code>logrotate</code> for <code>/var/log/containers/*</code> and <code>/var/log/pods/*</code> if not handled by container runtime.</li>
      <li>Package management: pin <code>kubeadm</code>, <code>kubelet</code>, <code>kubectl</code>, <code>containerd</code> to a known version; <code>apt-mark hold</code> / <code>dnf versionlock</code> to prevent surprise upgrades.</li>
    </ul>
    <p><strong>Air-gapped image pre-pull.</strong> If the cluster has no internet, you must seed the kubeadm + add-on images on every node:</p>
    <pre style="background:var(--bg-soft);padding:8px 12px;border-radius:6px;font-size:12px;overflow:auto"><code># Online: list and pull
kubeadm config images list --kubernetes-version v1.36
kubeadm config images pull --kubernetes-version v1.36

# Air-gap: ctr -n k8s.io images import &lt;tar&gt; on every node
# Or push to internal registry mirror + configure containerd</code></pre>
    <p class="skip-block"><span class="skip-pill">[ deep dive — skip if new ]</span>For Talos Linux: most of this is the machine-config YAML you write at install time — no manual <code>modprobe</code>, no per-node tweaking. The OS image bakes in the right kernel modules and cgroup driver. That's the appeal of immutable infra: V2 collapses to \"apply machine-config.\"</p>""",
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="<code>kubeadm init</code> hangs at \"Waiting for the kubelet to boot up the control plane.\" You check kubelet logs and see <code>failed to find cgroup mountpoint</code>. The most likely cause?",
            options=[
                ("a) etcd isn't running yet", False),
                ("b) containerd is using cgroupfs while kubelet expects systemd (or vice versa)", True),
                ("c) The node is out of memory", False),
            ],
            feedback="<strong>Answer: b.</strong> The cgroup-driver mismatch is the #1 kubeadm bootstrap bug. Both must agree. Edit <code>/etc/containerd/config.toml</code> → <code>SystemdCgroup = true</code>; restart containerd. Modern kubelet defaults to systemd. Verify with <code>crictl info | grep -i cgroup</code>.",
        ),
    },
    before_after_before='<p>SSH into 6 nodes. <code>vim</code> some files. Forget one. Run kubeadm. Hang. Diagnose. Fix. Re-run. Hang differently. Repeat for hours. Different team members do it differently; nodes drift; \"works on my node\" stories abound.</p>',
    before_after_after='<p>Per-node prep is one Ansible playbook (or one Talos machine-config YAML). Idempotent, repeatable, version-controlled. New node = run playbook + reboot + verify with a sanity script. kubeadm runs first time. Drift impossible.</p>',
    before_after_caption='<p style="margin-top:18px;color:var(--ink-soft);font-size:15px;font-style:italic">Per-node prep is the most automatable layer of self-managed K8s. Manual SSH-and-edit is the wrong unit of work even for one cluster.</p>',
    analogy_intro_html='<p>Land Clearing is the second site. Trees don\'t fall and stones don\'t arrange themselves. Before any frame goes up, the surveyor walks the plot, removes the stumps (legacy services that conflict), checks the soil pH (kernel modules + sysctl), tests the well water (time sync), and stockpiles the materials at the build site (image pre-pull). The work is repetitive but each step prevents a class of later disaster. Skip the soil test, your foundation cracks. Skip the kernel modules, your CNI never starts.</p>',
    translation_rows=[
        ("Soil pH test", "Kernel modules + sysctl"),
        ("Removing stumps + brush", "Disabling swap + conflicting services"),
        ("Calibrating tools", "Time sync (chrony / timesyncd)"),
        ("The contractor's toolbox", "Container runtime (containerd / CRI-O)"),
        ("Cgroup-driver toolbox lock", "<code>SystemdCgroup = true</code> alignment"),
        ("Stockpiling materials at the site", "Image pre-pull for air-gap installs"),
        ("Posted construction rules", "Hardening: SSH, audit, firewall, SELinux"),
    ],
    analogy_stops="The analogy stops here: kernel modules + sysctl aren't physical preparation — they're knobs in /proc and /sys that only matter at runtime. Setting them and rebooting is more like \"flipping breakers\" than \"clearing land.\"",
    eli5='Before you build a treehouse, you check that the tree is healthy and bring all your tools to the spot. Same for a Kubernetes node: check the kernel, turn off swap, install containerd, gather images.',
    eli10="Per-node prep checklist for kubeadm to work: load kernel modules (<code>overlay</code>, <code>br_netfilter</code>), set sysctls (<code>ip_forward</code>, <code>bridge-nf-call-iptables</code>), disable swap, sync time, install + configure containerd 2.x with <code>SystemdCgroup = true</code>, harden the host, optionally pre-pull images for air-gap. Order matters: modules before sysctl. Automate via Ansible or use Talos Linux which bakes it in.",
    scenarios=[
        Scenario(name="A bank using Ansible playbook for 50 nodes", body="One playbook. Idempotent. Tests with <code>--check</code>. Runs in CI on every change. New rack of 10 nodes onboarded by a junior engineer in an afternoon. Drift detected automatically by a daily Ansible-pull cron."),
        Scenario(name="A startup picking Talos to skip V2 entirely", body="No SSH, no per-node prep. Machine-config YAML defines the kernel + sysctl + runtime in one place. Boot the Talos image; nodes register themselves. The whole V2 module collapses to writing the machine-config. Trade-off: less flexibility for non-K8s workloads on the host."),
        Scenario(name="A team that learned about the cgroup-driver bug", body="First install: containerd cgroupfs, kubelet systemd. <code>kubeadm init</code> hangs. Three hours of debugging. Now: every node sanity-script checks <code>crictl info</code> output before kubeadm runs. Pre-flight assumption — fail loudly, fix instantly."),
        Scenario(name="An air-gapped install at a defence contractor", body="No internet. <code>kubeadm config images pull</code> + <code>ctr images export</code> on a connected build host. Tarballs to physical media. <code>ctr -n k8s.io images import</code> on every disconnected node. Plus internal Harbor mirror with the rest of the add-on images. Air-gap process documented + automated."),
    ],
    misconceptions=[
        Misconception(myth='\"Disabling swap is optional in modern K8s.\"', truth='K8s 1.28+ supports swap behind a feature gate, but most production clusters still disable it. Memory eviction logic and QoS classes assume no swap; enabling adds complexity. Default to off unless you have a specific reason.'),
        Misconception(myth='\"The cgroup driver doesn\'t really matter as long as both ends agree.\"', truth='True — but the failure mode when they disagree is opaque. Always systemd in 2026 (it\'s the default for all major distros + containerd). \"Both agree on systemd\" is the rule.'),
        Misconception(myth='\"You can skip <code>br_netfilter</code> if your CNI handles its own networking.\"', truth='Even Cilium with eBPF prefers <code>br_netfilter</code> loaded for compatibility paths. The cost of loading it is essentially zero; load it anyway.'),
    ],
    flashcards=[
        Flashcard(front='Two kernel modules to load?', back='<code>overlay</code> (overlay filesystem for container layers) and <code>br_netfilter</code> (bridge traffic visible to iptables/nftables). Both go in <code>/etc/modules-load.d/k8s.conf</code>.'),
        Flashcard(front='Three sysctl values?', back='<code>net.bridge.bridge-nf-call-iptables=1</code>, <code>net.bridge.bridge-nf-call-ip6tables=1</code>, <code>net.ipv4.ip_forward=1</code>. Apply via <code>/etc/sysctl.d/k8s.conf</code> + <code>sysctl --system</code>.'),
        Flashcard(front='Cgroup driver alignment?', back='containerd <code>SystemdCgroup = true</code> + kubelet defaults to systemd in modern K8s = aligned. Mismatch = kubelet refuses to start with cryptic cgroup errors.'),
        Flashcard(front='Time sync — why?', back='Certificates, etcd Raft, audit logs all assume monotonic time within ms tolerance. <code>chrony</code> or <code>systemd-timesyncd</code> on every node.'),
        Flashcard(front='Image pre-pulling for air-gap?', back='<code>kubeadm config images list</code> for the version. <code>ctr -n k8s.io images import &lt;tar&gt;</code> on every node, or pull from an internal registry mirror configured in containerd.'),
        Flashcard(front='Why disable swap?', back='Kubelet eviction + QoS logic assumes no swap. K8s 1.28+ supports it behind a flag, but production default is off.'),
        Flashcard(front='Pin package versions?', back='<code>apt-mark hold kubeadm kubelet kubectl containerd</code> on Debian/Ubuntu. <code>dnf versionlock</code> on RHEL family. Prevents surprise minor-version drift between unattended-upgrades runs.'),
        Flashcard(front='Talos Linux\'s answer to V2?', back='Bakes everything in: machine-config YAML covers kernel, sysctl, runtime, swap, time. No SSH, no per-node tweaking. Re-image to upgrade.'),
    ],
    quizzes=[
        Quiz(prompt='You SSH to a freshly-prepped node. <code>kubeadm join</code> fails with <code>node "x" not found</code> after a few minutes. The kubelet logs show <code>x509: certificate signed by unknown authority</code>. Diagnosis?', answer='Two common causes: (1) <strong>Time skew.</strong> The node\'s clock is wrong — JWT and certs fail validation. <code>chronyc tracking</code> shows offset &gt; 5 minutes. Sync time, retry. (2) <strong>Wrong CA</strong>. The kubeadm join command\'s discovery token + CA hash don\'t match the cluster\'s actual CA (typo? old token?). Re-run <code>kubeadm token create --print-join-command</code> on the control plane and use the fresh output. <strong>Pre-flight rule:</strong> verify <code>chronyc tracking</code> output before any kubeadm command — saves hours of mystery.'),
        Quiz(prompt='You\'re asked to onboard 30 new bare-metal nodes for an existing cluster. What\'s the right unit of work?', answer='Not SSH. <strong>(1) Ansible playbook</strong> covering the V2 checklist, idempotent. <strong>(2) PXE boot + cloud-init</strong> for fully unattended provisioning. <strong>(3) Talos Linux</strong> if you can pick the OS — the machine-config IS the playbook. <strong>(4) For each new node</strong>: PXE boots, cloud-init applies playbook, node reboots, sanity script verifies (crictl info / sysctl values / chronyc tracking), then <code>kubeadm join</code>. Scripted end-to-end. <strong>Manual SSH for 30 nodes is a process smell</strong> — automate now, not later.'),
        Quiz(prompt='Air-gapped customer needs the kubeadm v1.36 install bundle for a fresh cluster. <strong>Click for the air-gap procedure. ▼</strong>', cyoa=True, cyoa_tag='the air-gap procedure', answer='<strong>(1) On a connected build host</strong>: <code>kubeadm config images list --kubernetes-version v1.36</code> → captures the list (kube-apiserver, kube-controller-manager, kube-scheduler, kube-proxy, etcd, coredns, pause). <code>kubeadm config images pull --kubernetes-version v1.36</code> → caches them in containerd. <code>ctr -n k8s.io images export kubeadm-v1.36.tar &lt;each-image&gt;</code>. <strong>(2) Add-on images</strong>: pull and export Cilium / cert-manager / Velero / kube-prometheus-stack / Argo CD images the same way (or push to internal registry). <strong>(3) Distribution media</strong>: USB / encrypted tarball / internal artifact server reachable from the air-gapped network. <strong>(4) On every disconnected node</strong>: <code>ctr -n k8s.io images import kubeadm-v1.36.tar</code>. Verify with <code>crictl images</code>. <strong>(5) Configure containerd registry mirror</strong> pointing at the internal Harbor (or local cache) so subsequent pulls work transparently. <strong>(6) Install kubeadm/kubelet/kubectl Debian/RPM packages</strong> from the internal package mirror. <strong>(7) Run kubeadm init</strong> — the images are already local; no internet needed.'),
    ],
    glossary=[
        GlossaryItem(name='containerd 2.x', definition='Default container runtime for Kubernetes. CRI-compatible. Configure via <code>/etc/containerd/config.toml</code>.'),
        GlossaryItem(name='CRI', definition='Container Runtime Interface — gRPC API kubelet uses to talk to runtime.'),
        GlossaryItem(name='Cgroup driver', definition='Mechanism for organising cgroups. <code>systemd</code> (modern default) or <code>cgroupfs</code> (legacy). Container runtime + kubelet must agree.'),
        GlossaryItem(name='br_netfilter', definition='Kernel module enabling iptables/nftables to see bridged traffic. Required for kube-proxy iptables mode and many CNIs.'),
        GlossaryItem(name='overlay', definition='Overlay filesystem kernel module — used for container image layering.'),
        GlossaryItem(name='ip_forward sysctl', definition='Enables the kernel to forward packets between interfaces. Required for cross-node Pod traffic.'),
        GlossaryItem(name='Swap', definition='Disk space used as virtual memory. K8s default is to refuse to start kubelet if swap is on. 1.28+ has opt-in.'),
        GlossaryItem(name='chrony / systemd-timesyncd', definition='NTP clients for time synchronisation. One per node, monitored.'),
        GlossaryItem(name='crictl', definition='CRI-compatible CLI for runtime debugging (analog to docker CLI). <code>crictl ps</code>, <code>crictl images</code>, <code>crictl info</code>.'),
        GlossaryItem(name='nerdctl', definition='containerd-native CLI with docker-compatible UX. Useful for image management on nodes.'),
        GlossaryItem(name='Image pre-pulling', definition='Caching container images in the runtime ahead of Pod creation. Required for air-gap; useful for big images on slow networks.'),
        GlossaryItem(name='Talos machine-config', definition='YAML defining the entire OS state of a Talos node — kernel modules, sysctls, runtime, networking. Replaces V2 manual prep.'),
    ],
    recap_lead='Six categories of node prep — kernel, sysctl, swap, time, runtime, hardening — repeated identically on every node. Automate via Ansible or skip with Talos.',
    recap_next='<strong>Next — V3: kubeadm Cluster Bootstrap.</strong> Now that the soil is prepared, raise the frame: kubeadm phases, configuration files, HA control plane, worker join, the alternative bootstrappers (kubespray / kOps / Talos / Cluster API).',
)
