"""K-OCP O2 — Installation Models (IPI/UPI/Assisted/Agent, SNO/3-node/2-node, disconnected, oc-mirror, OSUS)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OCP installation models — IPI/UPI/Assisted/Agent + cluster shapes + disconnected.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Construction Site — four installers + cluster shapes + disconnected</text>
  <rect x="40" y="65" width="170" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="125" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">four installers</text>
  <text x="125" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">IPI (installer-provisioned)</text>
  <text x="125" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">UPI (user-provisioned)</text>
  <text x="125" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">Assisted (guided)</text>
  <text x="125" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">Agent-based (disconnected)</text>
  <rect x="225" y="65" width="160" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="305" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">cluster shapes</text>
  <text x="305" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">multi-node prod</text>
  <text x="305" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">SNO (single node)</text>
  <text x="305" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">compact 3-node</text>
  <text x="305" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">two-node compact</text>
  <rect x="400" y="65" width="160" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="480" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">platforms</text>
  <text x="480" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">bare metal</text>
  <text x="480" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">vSphere</text>
  <text x="480" y="133" text-anchor="middle" font-size="9" fill="#FBF1D6">AWS · Azure · GCP</text>
  <text x="480" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">OpenStack</text>
  <rect x="575" y="65" width="145" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="647" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">disconnected</text>
  <text x="647" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">mirror registry</text>
  <text x="647" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">oc-mirror</text>
  <text x="647" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">OSUS</text>
  <text x="647" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">(Update Service)</text>
</svg>"""


LESSON = LessonSpec(
    num="02", title_short="installation",
    title_full="O2 · Installation Models (IPI / UPI / Assisted / Agent + cluster shapes + disconnected)",
    title_html="K-OCP O2 · Installation Models",
    module_eyebrow="Module O2 · the Construction Site",
    hero_sub_html='Four installers: <strong>IPI</strong> (installer-provisioned, fully automated), <strong>UPI</strong> (user-provisioned, you pre-create infra), <strong>Assisted Installer</strong> (guided web UI for bare metal), <strong>Agent-based Installer</strong> (disconnected / air-gapped). Cluster shapes: multi-node, <strong>Single Node OpenShift (SNO)</strong>, compact 3-node, two-node compact. Platforms: bare metal, vSphere, AWS, Azure, GCP, OpenStack. <strong>Disconnected installs</strong> via mirror registries + <strong>oc-mirror</strong>. <strong>Ignition</strong> + bootstrap node + OpenShift Update Service (OSUS).',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"Bare-metal install hangs at bootstrap. Console says \'waiting for ignition\'.\"</em> You ran <code>openshift-install create cluster</code> 4 hours ago. The bootstrap node booted from RHCOS but never reaches the bootstrap apiserver. You have no idea whether it\'s a DNS issue (api / api-int / *.apps records), a DHCP issue, ignition file delivery (HTTP server on bootstrap), or the ignition signature being wrong. You don\'t know how to inspect the bootstrap node\'s state. <em>The clock keeps ticking against your downtime window.</em> Today\'s lesson: pick the right installer + understand the bootstrap dance + master disconnected.",
    stamp_html="<strong>Pick installer by environment: IPI for cloud + supported bare-metal; UPI when IPI doesn\'t fit; Assisted for guided bare-metal install with a SaaS UX; Agent-based for disconnected. SNO/3-node/2-node compact for edge. Disconnected = mirror registry + oc-mirror + OSUS.</strong>",
    district_pin="ko-bay02", district_label="Construction Site",
    sections=[
        Section(eyebrow="Section 1.1 · IPI vs UPI", h2="IPI vs UPI — automated vs DIY infrastructure",
            body_html="""    <p><strong>IPI (Installer-Provisioned Infrastructure)</strong> = <code>openshift-install</code> creates everything: VMs/instances, networks, load balancers, DNS records, then bootstraps the cluster. Cloud platforms (AWS, Azure, GCP, OpenStack) and supported bare-metal flavours. <em>Fastest path; least flexibility.</em></p>
    <p><strong>UPI (User-Provisioned Infrastructure)</strong> = you pre-create the infrastructure (compute, network, LB, DNS) per the install docs; <code>openshift-install</code> generates Ignition configs that you serve to nodes booting from RHCOS. <em>For bare-metal flavours not yet IPI-supported, custom networking, regulated environments where infra provisioning is owned by another team.</em></p>
    <p><strong>Assisted Installer</strong> (assisted-service / SaaS UI at <code>console.redhat.com/assisted-installer</code>) — guided wizard for bare-metal: download discovery ISO, boot nodes, the wizard finds them and walks you through cluster creation. Lower friction than UPI; more flexibility than IPI for bare-metal.</p>
    <p><strong>Agent-based Installer</strong> = Assisted Installer\'s engine packaged for <em>disconnected / air-gapped</em> environments. <code>openshift-install agent create image</code> bakes a self-contained ISO with all artifacts; boot nodes from it; cluster comes up with no internet access required. <em>The path for regulated bare-metal / SCIF / classified environments.</em></p>"""),
        Section(eyebrow="Section 1.2 · cluster shapes", h2="Cluster shapes — multi-node, SNO, 3-node, 2-node compact",
            body_html="""    <p>Default: <strong>3 control-plane (master) + ≥2 worker</strong> nodes. Production minimum.</p>
    <p><strong>Single Node OpenShift (SNO)</strong> — control plane + worker on one node. Edge sites; constrained environments. Lower availability (no zone redundancy) but full OCP API surface.</p>
    <p><strong>Compact 3-node cluster</strong> — 3 master nodes that <em>also</em> run worker workloads (master taint removed). Use case: small clusters where 3+2 is overkill; pay for 3 nodes total instead of 5.</p>
    <p><strong>Two-node compact</strong> — newer support shape: 2 nodes that share control plane + worker duties via a witness node for arbitration. Edge / cost-constrained scenarios.</p>
    <p><strong>Sizing guidance:</strong> SNO for edge / dev / CRC-on-server; 3-node compact for small prod; multi-node default for general prod; 5+ control-plane only for very large clusters or specific HA requirements.</p>"""),
        Section(eyebrow="Section 1.3 · platforms + install-config + Ignition", h2="Platforms + install-config + Ignition + bootstrap",
            body_html="""    <p><strong>Platforms IPI-supported</strong>: bare metal (with Redfish for some hardware), vSphere, AWS, Azure, GCP, OpenStack, IBM Cloud. UPI works on more (any platform that boots RHCOS).</p>
    <p><strong>The install dance:</strong>
    <ol>
      <li><code>openshift-install create install-config</code> — interactive prompts → <code>install-config.yaml</code>. Pull secret from console.redhat.com.</li>
      <li><code>openshift-install create manifests</code> — generates K8s manifests. Customise here (network policies, MachineConfigs, etc.).</li>
      <li><code>openshift-install create ignition-configs</code> — generates <code>bootstrap.ign</code>, <code>master.ign</code>, <code>worker.ign</code> (Ignition is the RHCOS first-boot config format).</li>
      <li>Boot the <strong>bootstrap node</strong> from RHCOS pointed at <code>bootstrap.ign</code>. It runs a temporary apiserver + etcd to bootstrap the real control plane.</li>
      <li>Boot <strong>3 master nodes</strong> from RHCOS pointed at <code>master.ign</code>. They join the bootstrap apiserver, form the real etcd quorum, and the real apiserver takes over.</li>
      <li>Bootstrap node is destroyed (<code>openshift-install wait-for bootstrap-complete</code>).</li>
      <li>Worker nodes boot from <code>worker.ign</code>, join the cluster, become Ready.</li>
      <li><code>openshift-install wait-for install-complete</code> — cluster operators reconcile; cluster Available.</li>
    </ol>
    <p><strong>DNS requirements</strong>: <code>api.&lt;cluster&gt;.&lt;basedomain&gt;</code> (apiserver), <code>api-int.&lt;cluster&gt;.&lt;basedomain&gt;</code> (internal apiserver from nodes), <code>*.apps.&lt;cluster&gt;.&lt;basedomain&gt;</code> (Routes wildcard). Get these wrong and you debug for hours.</p>"""),
        Section(eyebrow="Section 1.4 · disconnected + oc-mirror + OSUS", h2="Disconnected installs + oc-mirror + OSUS",
            body_html="""    <p><strong>Disconnected (air-gapped) installs</strong> are common in regulated industries (defence, banking, healthcare). The cluster has no internet access. Required:</p>
    <ul>
      <li><strong>Mirror registry</strong> — internal container registry (Quay, Harbor, or the small <code>mirror-registry</code> Quay flavour Red Hat ships) holding all OCP images + Operator catalog images.</li>
      <li><strong>oc-mirror</strong> — Red Hat tool to mirror OCP releases + selected Operators from public catalogs to your internal mirror. ImageSetConfiguration declaratively defines what to mirror.</li>
      <li><strong>imageContentSourcePolicy / ImageDigestMirrorSet</strong> — cluster-side resources that redirect <code>quay.io/openshift-release-dev/...</code> pulls to your mirror.</li>
      <li><strong>Agent-based Installer</strong> (above) — bakes everything into an ISO for cluster bootstrap without internet.</li>
    </ul>
    <p><strong>OpenShift Update Service (OSUS)</strong> = the upgrade-graph service. Public (cloud-connected) clusters fetch the graph from <code>api.openshift.com/api/upgrades_info/v1/graph</code>. Disconnected clusters need their own OSUS instance (Red Hat ships an Operator) fed by mirrored upgrade-graph data.</p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A bank installs OCP in an air-gapped data center with no internet. Which installer + which path?",
        options=[
            ("IPI on bare metal — fastest.", False),
            ("Agent-based Installer + mirror registry + oc-mirror — bakes a self-contained ISO; no internet required.", True),
            ("Assisted Installer via console.redhat.com.", False),
        ],
        feedback="Agent-based + mirror registry + oc-mirror is the disconnected path. Assisted Installer needs internet (uses console.redhat.com SaaS); IPI bare-metal needs internet for image pulls.",
    )},
    before_after_before='<p>Pre-IPI installs were 2-3 weeks of pre-flight: VM + network + LB + DNS + storage prep, manual Ignition file generation, manual bootstrap dance. Disconnected installs were a research project. Bare-metal had no installer; you wrote bash. Mistakes at install time meant tear-down + restart.</p>',
    before_after_after='<p>Modern OCP: <strong>IPI</strong> in cloud or supported bare-metal — minutes from <code>openshift-install create cluster</code> to working cluster. <strong>Assisted Installer</strong> guides bare-metal via SaaS UI. <strong>Agent-based</strong> handles air-gapped. <strong>oc-mirror</strong> codifies disconnected mirroring. <strong>SNO + compact 3-node + 2-node</strong> shapes for cost-constrained / edge.</p>',
    before_after_caption='<p class="ba-caption"><em>Pick the installer that matches your environment and operating model. The four installers cover almost every reasonable shape.</em></p>',
    analogy_intro_html='''<p>The <strong>Construction Site</strong> at K-Foundry is where you build a foundry from the ground up. Four contractor types are available.</p>
    <p>The <strong>Turnkey Contractor (IPI)</strong> shows up with everything: trucks, materials, foundation crew, framers, electricians. They build the foundry top-to-bottom; you sign one contract. Available in major metro areas (cloud platforms + supported bare-metal). <strong>Assemble-Your-Own Contractor (UPI)</strong> ships the materials but you bring the foundation crew, electricians, and zoning permits — you pre-build the lot, they hand you blueprints (Ignition configs). For unusual sites where the Turnkey contractor can\'t go.</p>
    <p>The <strong>Guided Wizard (Assisted Installer)</strong> is a Red Hat-hosted concierge that walks you through bare-metal step-by-step via a web wizard. Lower friction than UPI; more flexibility than IPI. The <strong>Field Engineer (Agent-based)</strong> packs every tool + material into a single shipping container that ships to your air-gapped site — no internet needed.</p>
    <p>Cluster shapes: full 3+2 production foundry; <em>single-node compact</em> (SNO) for a one-room edge foundry; <em>3-node compact</em> where the 3 masters also do worker duty; <em>2-node compact</em> with a witness node for arbitration.</p>''',
    translation_rows=[
        ("Turnkey Contractor", "IPI (Installer-Provisioned Infrastructure)"),
        ("Assemble-Your-Own Contractor", "UPI (User-Provisioned Infrastructure)"),
        ("Guided Wizard concierge", "Assisted Installer (SaaS UI on console.redhat.com)"),
        ("Field Engineer + sealed container", "Agent-based Installer (air-gapped ISO)"),
        ("Foundation pour blueprints", "Ignition configs (bootstrap.ign, master.ign, worker.ign)"),
        ("Temporary site office", "Bootstrap node (temp apiserver + etcd)"),
        ("Real foundry building", "Permanent control plane (3 masters)"),
        ("Day-1 worker shifts", "Worker nodes joining"),
        ("Single-room edge foundry", "Single Node OpenShift (SNO)"),
        ("3-room compact (rooms double up)", "Compact 3-node cluster (masters also workers)"),
        ("2-room + arbiter", "Two-node compact + witness"),
        ("Sealed warehouse of parts", "Mirror registry"),
        ("Parts-shipping manifest", "oc-mirror + ImageSetConfiguration"),
        ("Foundry repair-schedule oracle", "OpenShift Update Service (OSUS)"),
    ],
    analogy_stops="A real construction site has fixed permits and zoning; OCP installs adapt to whatever environment you have, but DNS misconfiguration is the silent killer no metaphor captures.",
    eli5="There are four ways to build the factory: turnkey (cloud — fastest), assemble-your-own (you do the prep), guided (web wizard for bare-metal), or field-engineer (sealed container for sites with no internet). Pick by where you\'re building.",
    eli10="OCP install paths: IPI (installer creates infra; cloud + supported bare-metal), UPI (you pre-create infra; broader bare-metal), Assisted Installer (SaaS-guided wizard for bare-metal), Agent-based (air-gapped ISO). Cluster shapes: 3+2 default, SNO single-node, 3-node compact, 2-node + witness. Disconnected = mirror registry + oc-mirror + OSUS. Bootstrap dance: install-config → manifests → ignition-configs → bootstrap node temporary apiserver → masters join → bootstrap dies → workers join → cluster Available.",
    scenarios=[
        Scenario(name="Bank — Agent-based on air-gapped bare metal",
            body="Air-gapped data center, no internet. Agent-based Installer + internal Quay mirror + oc-mirror to populate the mirror with target OCP version + ~12 chosen Operators. Disconnected OSUS Operator for upgrade-graph access. Single ISO boots all 5 nodes; cluster Available in 90 minutes."),
        Scenario(name="Telco — SNO at 800 cell sites via Assisted",
            body="Each cell site needs OCP. Single-node OpenShift via Assisted Installer; bare-metal hardware fleet pre-provisioned. RHACM (covered later) registers the SNOs into a fleet for centralized policy + apps."),
        Scenario(name="Bare-metal startup — IPI saves 2 weeks",
            body="A startup adopts OCP on Dell servers with iDRAC (Redfish supported). IPI bare-metal: <code>openshift-install create cluster</code> handles BMC interaction, RHCOS provisioning, network setup. Cluster Ready in 90 minutes vs the 2 weeks UPI would have taken."),
        Scenario(name="DNS bug — bootstrap stalled, fixed in 10 minutes",
            body="Bootstrap stalled. Engineer checks DNS: <code>api-int.cluster.basedomain</code> resolves but to wrong IP (typo in DNS zone). Corrected; bootstrap completes within 10 minutes. <em>Postmortem: pre-flight DNS validation script before every install.</em>"),
    ],
    misconceptions=[
        Misconception(myth="\"UPI is harder — always use IPI.\"",
            truth="UPI is the right call when: IPI doesn\'t support your platform/version combo; another team owns infra provisioning; you have specific networking / BMC requirements IPI can\'t express. UPI gives you control over every infra detail; IPI hides them. Both are valid; pick by need."),
        Misconception(myth="\"Disconnected install means no upgrades.\"",
            truth="Disconnected clusters DO upgrade — via mirrored OSUS data + mirrored release images. <code>oc-mirror</code> updates your mirror with new releases on a schedule (you sync from internet-connected staging or sneakernet). Cluster\'s ClusterVersion sees new versions in its disconnected OSUS feed and upgrades normally."),
        Misconception(myth="\"SNO is just OCP on a small VM.\"",
            truth="SNO is a specific cluster topology: control plane + worker on one node, etcd not quorum (single etcd; data resilience via storage backup). Different from \"OCP on small VM\" — uses a specific install profile that disables expectations of multi-master HA. Real edge cluster, not a dev shortcut."),
    ],
    flashcards=[
        Flashcard(front="IPI vs UPI?", back="<strong>IPI</strong>: <code>openshift-install</code> creates all infra (VMs, network, LB, DNS); fastest. <strong>UPI</strong>: you pre-create infra; installer generates Ignition configs you serve. UPI for unsupported bare-metal flavors / custom networking / split-team ownership."),
        Flashcard(front="Assisted Installer vs Agent-based Installer?", back="<strong>Assisted</strong>: SaaS-hosted wizard on console.redhat.com; needs internet from your install host. <strong>Agent-based</strong>: same engine packaged into a self-contained ISO; for air-gapped / disconnected installs. Both target bare metal with guided UX."),
        Flashcard(front="Three OCP cluster shapes besides default 3+2?", back="<strong>SNO</strong> (single node = control plane + worker), <strong>compact 3-node</strong> (3 masters also schedule workers), <strong>two-node compact</strong> (2 nodes + witness for arbitration). Edge / cost-constrained scenarios."),
        Flashcard(front="What does the bootstrap node do?", back="Boots from RHCOS + bootstrap.ign. Runs a temporary apiserver + etcd. Real master nodes join the bootstrap apiserver, form real etcd quorum, real apiserver takes over. Bootstrap node is destroyed once <code>wait-for bootstrap-complete</code> succeeds."),
        Flashcard(front="What three DNS records do you need for OCP?", back="<code>api.&lt;cluster&gt;.&lt;base&gt;</code> (external apiserver), <code>api-int.&lt;cluster&gt;.&lt;base&gt;</code> (internal apiserver from nodes), <code>*.apps.&lt;cluster&gt;.&lt;base&gt;</code> (wildcard for Routes). Wrong DNS = bootstrap fails silently."),
        Flashcard(front="What is oc-mirror?", back="Red Hat tool to mirror OCP releases + Operator catalogs from public sources to an internal mirror registry. ImageSetConfiguration declaratively defines what to mirror (releases, operators, channels, additional images). Path-of-record for disconnected installs + ongoing updates."),
        Flashcard(front="What is OSUS?", back="<strong>OpenShift Update Service</strong> — the upgrade-graph service. Public clusters fetch from api.openshift.com; disconnected clusters need their own OSUS instance (Red Hat ships an Operator) fed by mirrored upgrade-graph data."),
        Flashcard(front="What is Ignition?", back="RHCOS first-boot config format. <code>openshift-install create ignition-configs</code> emits bootstrap.ign / master.ign / worker.ign. Each node boots RHCOS with a pointer to its Ignition file (kernel arg or HTTP). Ignition runs once at first boot; configures hostname, networking, k8s-cluster-id, kubelet, etc."),
    ],
    quizzes=[
        Quiz(prompt="Bootstrap node is up but masters never reach Ready. What\'s your diagnostic ladder?",
            answer="(1) DNS: from each master, can <code>api.&lt;cluster&gt;.&lt;base&gt;</code> + <code>api-int</code> resolve correctly? Wrong DNS = silent stall. (2) From each master to bootstrap apiserver: can the master reach the bootstrap on TCP 6443? Firewall rules. (3) Ignition: did each master fetch its master.ign successfully? Check IPMI/BMC console for Ignition errors at first boot. (4) NTP: time skew > a few seconds breaks etcd Raft. (5) Pull secret: each master pulls control-plane container images on first boot — bad pull secret means kubelet can\'t start. (6) <code>openshift-install gather bootstrap</code> bundles bootstrap-side logs."),
        Quiz(prompt="A bank wants OCP on existing vSphere with custom networking the IPI installer doesn\'t handle. UPI or IPI?",
            answer="<strong>UPI vSphere</strong>. They pre-create the VMs (or VM templates), the LB (typically MetalLB or external F5), the DNS records, the load-balancer health checks, and the DHCP. <code>openshift-install</code> generates Ignition configs they serve via an HTTP server. More work upfront; fits their existing vSphere networking constraints. IPI vSphere works for standard topologies but doesn\'t cover their custom path."),
        Quiz(prompt="Saturday at the regulated SCIF site. Air-gapped install. Engineer plugs in the Agent-based ISO. Cluster comes up. Six weeks later, security feed publishes a CVE. How do they patch?",
            answer="(1) On internet-connected staging: run <code>oc-mirror --config imageset-config.yaml</code> targeting their stash repository — pulls the new patch release + Operator updates into a tarball. (2) Sneakernet (or one-way data diode) the tarball to the air-gapped facility. (3) On the air-gapped mirror server: <code>oc-mirror --from tarball.tar --to docker://mirror.example.com</code> populates the internal registry. (4) Disconnected OSUS Operator picks up the new upgrade-graph data. (5) ClusterVersion sees the new patch as available; admin upgrades via <code>oc adm upgrade --to-image=...</code>. <em>Disconnected isn\'t patch-free — it\'s patches-via-sneakernet on a defined cadence.</em>",
            cyoa=True, cyoa_tag="how the disconnected patch landed at the SCIF"),
    ],
    glossary=[
        GlossaryItem(name="IPI", definition="Installer-Provisioned Infrastructure. openshift-install creates all infra. Cloud + supported bare-metal."),
        GlossaryItem(name="UPI", definition="User-Provisioned Infrastructure. You pre-create infra; installer generates Ignition. For unusual platforms or split-team ownership."),
        GlossaryItem(name="Assisted Installer", definition="SaaS wizard at console.redhat.com/assisted-installer. Guided bare-metal install; needs internet."),
        GlossaryItem(name="Agent-based Installer", definition="Self-contained ISO for disconnected / air-gapped installs. Same engine as Assisted, packaged offline."),
        GlossaryItem(name="SNO", definition="Single Node OpenShift. Control plane + worker on one node. For edge."),
        GlossaryItem(name="Compact 3-node cluster", definition="3 masters that also schedule workloads. Smaller / cheaper than 3+2."),
        GlossaryItem(name="Two-node compact", definition="2 nodes + witness for arbitration. Newer support shape for cost-constrained edge."),
        GlossaryItem(name="Ignition", definition="RHCOS first-boot config format. openshift-install emits bootstrap.ign / master.ign / worker.ign."),
        GlossaryItem(name="Bootstrap node", definition="Temporary node running apiserver + etcd to bootstrap the real control plane. Destroyed after masters join."),
        GlossaryItem(name="install-config.yaml", definition="The high-level install configuration. Cluster name, base domain, platform, network ranges, pull secret, SSH key."),
        GlossaryItem(name="oc-mirror", definition="Red Hat tool to mirror OCP releases + Operator catalogs to an internal registry. Defines what to mirror via ImageSetConfiguration."),
        GlossaryItem(name="OSUS", definition="OpenShift Update Service — upgrade-graph service. Public + disconnected variants."),
    ],
    recap_lead='Four installers + four cluster shapes + bootstrap dance + disconnected mirror pattern. The Construction Site map is internalised.',
    recap_next='<strong>Next — O3: OpenShift Networking.</strong> OVN-Kubernetes, cluster/service/machine networks, IngressController + Routes vs Ingress vs Gateway API, NetworkPolicy + EgressIP / Egress firewall, Multus + SR-IOV / DPDK, MetalLB Operator, Submariner, NetObserv.',
)
