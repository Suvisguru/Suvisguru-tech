"""K-OCP O1 — OpenShift Architecture (OCP vs upstream, ROSA/ARO/OSD/OKD, RHCOS, MCO, CVO, OLM, oc, HCP)."""
from _helpers import (
    LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario,
    PauseCheck, GlossaryItem,
)

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OpenShift architecture: opinionated K8s distribution + RHCOS + Operators + integrated CI/CD/registry/OAuth.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Welcome Hall — opinionated K8s + everything-built-in</text>
  <rect x="50" y="65" width="220" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="160" y="86" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">upstream Kubernetes</text>
  <text x="160" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">apiserver · etcd · kubelet</text>
  <text x="160" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">controllers · scheduler</text>
  <text x="160" y="138" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">+ what OCP adds:</text>
  <text x="160" y="155" text-anchor="middle" font-size="9" fill="#FFFFFF">Routes · BuildConfigs · ImageStreams</text>
  <text x="160" y="168" text-anchor="middle" font-size="9" fill="#FFFFFF">S2I · SCCs · Projects · OAuth</text>
  <text x="160" y="180" text-anchor="middle" font-size="9" fill="#FFFFFF">integrated registry · OperatorHub</text>
  <rect x="290" y="65" width="200" height="125" rx="10" fill="#3F4A5E" stroke="#FBF1D6"/>
  <text x="390" y="86" text-anchor="middle" font-size="12" font-weight="700" fill="#FBF1D6">RHCOS + MCO + CVO</text>
  <text x="390" y="105" text-anchor="middle" font-size="9" fill="#FBF1D6">RHCOS = immutable ostree OS</text>
  <text x="390" y="120" text-anchor="middle" font-size="9" fill="#FBF1D6">MCO = Machine Config Operator</text>
  <text x="390" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">CVO = Cluster Version Operator</text>
  <text x="390" y="155" text-anchor="middle" font-size="9" fill="#FBF1D6">OLM = Operator Lifecycle Manager</text>
  <text x="390" y="170" text-anchor="middle" font-size="9" fill="#FBF1D6">oc CLI vs kubectl</text>
  <text x="390" y="183" text-anchor="middle" font-size="9" fill="#FBF1D6">web console: Admin + Dev</text>
  <rect x="510" y="65" width="200" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="610" y="86" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">deployment shapes</text>
  <text x="610" y="105" text-anchor="middle" font-size="9" fill="#FFFFFF">OCP self-managed</text>
  <text x="610" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">OpenShift Dedicated (Red Hat-mgd)</text>
  <text x="610" y="131" text-anchor="middle" font-size="9" fill="#FFFFFF">ROSA (AWS) · ARO (Azure)</text>
  <text x="610" y="144" text-anchor="middle" font-size="9" fill="#FFFFFF">OpenShift on IBM / GCP</text>
  <text x="610" y="157" text-anchor="middle" font-size="9" fill="#FFFFFF">OKD (community)</text>
  <text x="610" y="172" text-anchor="middle" font-size="9" font-style="italic" fill="#FFFFFF">HyperShift · MicroShift · CRC</text>
</svg>"""


LESSON = LessonSpec(
    num="01",
    title_short="OCP architecture",
    title_full="O1 · OpenShift Architecture (what OCP adds + RHCOS + MCO + CVO + OLM + deployment shapes)",
    title_html="K-OCP O1 · OpenShift Architecture",
    module_eyebrow="Module O1 · the Welcome Hall — opinionated K8s + everything built-in",
    hero_sub_html='OpenShift Container Platform (OCP) = upstream Kubernetes <strong>plus</strong>: <strong>Routes</strong>, <strong>BuildConfigs</strong>, <strong>ImageStreams</strong>, <strong>S2I</strong>, <strong>Templates</strong>, <strong>SCCs</strong>, <strong>Projects</strong>, <strong>integrated OAuth</strong>, <strong>integrated registry</strong>, <strong>OperatorHub-everywhere</strong>. <strong>RHCOS</strong> = immutable ostree node OS managed by the <strong>Machine Config Operator (MCO)</strong>. <strong>Cluster Version Operator (CVO)</strong> orchestrates dozens of cluster operators. <strong>oc</strong> CLI extends kubectl. Deployment shapes: OCP self-managed / OpenShift Dedicated / ROSA / ARO / IBM Cloud / GCP / OKD / HyperShift / MicroShift / CRC.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. PagerDuty: <em>\"ClusterOperator authentication degraded; OAuth login failing for everyone.\"</em> You SSH for the apiserver — wait, you can\'t (RHCOS is immutable, no SSH by default). You start typing <code>kubectl get pods -n openshift-authentication</code> — but the cluster has its own <em>Project</em> isolation, its own <em>Operator</em> reconciliation loops, its own <em>OAuth server</em> separate from upstream K8s. <em>You inherited the cluster two days ago and don\'t even know which 30+ cluster operators must be healthy for it to be \"working.\"</em> Today\'s lesson: the OCP map.",
    stamp_html="<strong>OCP = upstream K8s + Red Hat\'s opinionated additions (Routes, SCCs, OperatorHub-everywhere, integrated OAuth/registry/console). RHCOS is immutable + MCO-managed. CVO orchestrates ~30 cluster operators. Pick the deployment shape that matches your operating model: OCP / OSD / ROSA / ARO / OKD / HyperShift / MicroShift / CRC.</strong>",
    district_pin="ko-bay01",
    district_label="Welcome Hall",
    sections=[
        Section(
            eyebrow="Section 1.1 · what OCP adds on top of K8s",
            h2="What OCP adds on top of upstream K8s",
            body_html="""    <p><strong>OpenShift Container Platform (OCP)</strong> is Red Hat\'s opinionated K8s distribution. It includes upstream K8s plus a curated set of additions and replacements:</p>
    <ul>
      <li><strong>Routes</strong> — Red Hat\'s ingress primitive (predates Ingress; handles TLS edge / passthrough / re-encrypt termination cleanly). Coexists with K8s <code>Ingress</code> + Gateway API; OpenShift Routes are still the workhorse.</li>
      <li><strong>BuildConfigs / Builds / ImageStreams / ImageStreamTags</strong> — built-in CI primitives. <strong>S2I (Source-to-Image)</strong> = build container images from source code without writing a Dockerfile.</li>
      <li><strong>Templates</strong> — pre-OperatorHub mechanism for app templates; still used.</li>
      <li><strong>Security Context Constraints (SCCs)</strong> — Red Hat\'s pre-PSA admission system. Default is <code>restricted-v2</code> (non-root, dropped capabilities, seccomp). Stricter than K8s\' historical PSP defaults.</li>
      <li><strong>Projects</strong> — OCP\'s namespace-with-extra-metadata. Every K8s namespace = a Project, with a <code>ProjectRequest</code>, default rolebinding policies, and self-provisioner support.</li>
      <li><strong>Integrated OAuth server</strong> — own OAuth provider built into the cluster; backs HTPasswd, LDAP, OIDC, GitHub, etc., providers.</li>
      <li><strong>Integrated container image registry</strong> — built-in registry (image-registry.openshift-image-registry.svc) for ImageStreams + builds.</li>
      <li><strong>OperatorHub-everywhere</strong> — every add-on (logging, monitoring, networking, storage, dev tools) ships as an Operator via OLM.</li>
    </ul>"""
        ),
        Section(
            eyebrow="Section 1.2 · deployment shapes",
            h2="Eight deployment shapes — pick the operating model",
            body_html="""    <p>OCP isn\'t one product — it\'s a family of deployments under the same software:</p>
    <ul>
      <li><strong>OpenShift Container Platform (OCP)</strong> — self-managed; you operate the cluster + control plane. Bare metal, vSphere, AWS, Azure, GCP, OpenStack.</li>
      <li><strong>OpenShift Dedicated (OSD)</strong> — Red Hat-managed OCP on AWS or GCP. Red Hat operates the control plane + nodes; you operate workloads.</li>
      <li><strong>ROSA (Red Hat OpenShift Service on AWS)</strong> — joint AWS + Red Hat managed. Native AWS billing + integration; Red Hat does the K8s lifting.</li>
      <li><strong>ARO (Azure Red Hat OpenShift)</strong> — joint Azure + Red Hat managed. Same idea on Azure.</li>
      <li><strong>OpenShift on IBM Cloud</strong> + <strong>OpenShift on Google Cloud</strong> — managed-OCP on those clouds.</li>
      <li><strong>OKD</strong> — community / upstream-development distribution of OCP. Same code, no Red Hat support.</li>
      <li><strong>Hosted Control Planes (HyperShift)</strong> — control planes run as Pods inside another OCP cluster. Density: many lightweight clusters share underlying compute.</li>
      <li><strong>MicroShift</strong> — single-node OCP for edge devices. <strong>OpenShift Local (CRC)</strong> — single-node OCP for laptops + dev environments.</li>
    </ul>
    <p><strong>Pick by operating-model intent:</strong> self-managed (OCP) for full control + bare-metal / hybrid; managed (ROSA / ARO / OSD / IBM / GCP) when Red Hat or your cloud provider should run the K8s lifting; HyperShift for cluster-fleet density; MicroShift / CRC for edge / dev.</p>"""
        ),
        Section(
            eyebrow="Section 1.3 · RHCOS + MCO + CVO + OLM",
            h2="RHCOS + MCO + CVO + OLM — the four operators that run OCP",
            body_html="""    <p><strong>RHCOS (Red Hat CoreOS)</strong> = OCP\'s node OS. <em>Immutable, ostree-based</em> — you don\'t apt/yum install on it; OS changes happen by redeploying a new ostree image. SSH disabled by default (use <code>oc debug node/...</code> instead). Includes CRI-O (container runtime), kubelet, NetworkManager, and a handful of system services.</p>
    <p><strong>Machine Config Operator (MCO)</strong> manages RHCOS. You declare changes via <strong>MachineConfig</strong> YAML resources (kernel args, systemd units, files, ignition snippets). MCO renders them into a final ostree-like config per <strong>MachineConfigPool</strong> (master, worker, custom pools), drains nodes, applies the new config, reboots, validates. <em>This is how you customize node OS without SSH or hand-editing.</em></p>
    <p><strong>Cluster Version Operator (CVO)</strong> orchestrates ~30 <strong>ClusterOperators</strong> — each manages one piece of OCP (authentication, console, dns, etcd, ingress, monitoring, network, storage, etc.). CVO ensures all CO\'s reconcile to the cluster\'s declared version. <em>Cluster health = all CO\'s Available + not Degraded + not Progressing (during steady state).</em></p>
    <p><strong>OLM (Operator Lifecycle Manager)</strong> = the operator that manages other operators. OperatorHub catalogs (CatalogSources) → Subscription → InstallPlan → ClusterServiceVersion (CSV) → operator running. <em>Almost every OCP add-on installs through OLM.</em></p>
    <p><strong>oc</strong> CLI = kubectl plus OCP-aware commands: <code>oc new-app</code>, <code>oc new-build</code>, <code>oc start-build</code>, <code>oc adm</code>, <code>oc debug</code>, <code>oc rsync</code>, <code>oc port-forward</code>. Works everywhere kubectl works; learn <em>both</em>.</p>"""
        ),
        Section(
            eyebrow="Section 1.4 · web console + edge variants",
            h2="Web console (Administrator + Developer) + edge variants",
            body_html="""    <p>The OCP <strong>web console</strong> ships two perspectives:</p>
    <ul>
      <li><strong>Administrator perspective</strong> — cluster-wide view: nodes, machines, operators, monitoring, storage, networking, RBAC. For platform engineers.</li>
      <li><strong>Developer perspective</strong> — project-scoped: topology view (pods/services/routes graph), build pipeline, dev catalog (templates, helm charts, S2I builders), monitoring of own workloads. For app developers.</li>
    </ul>
    <p>Both perspectives sit on the same RBAC; users see what their roles allow.</p>
    <p><strong>Edge variants:</strong>
    <ul>
      <li><strong>Single Node OpenShift (SNO)</strong> — full OCP on one node. Edge deployments at retail / branch / industrial.</li>
      <li><strong>MicroShift</strong> — even smaller (~1 GB RAM): minimal OCP for ultra-edge devices, IoT gateways, small footprint deployments.</li>
      <li><strong>OpenShift Local (CRC — CodeReady Containers)</strong> — single-node OCP on laptop. For dev + experimentation. Drives <code>crc start</code>; ~10 GB disk + ~10 GB RAM.</li>
    </ul>
    <p>All three variants register into a fleet via Red Hat Advanced Cluster Management (ACM) — covered in O10.</p>"""
        ),
    ],
    pause_check_after_section={
        2: PauseCheck(
            question="A cluster operator (CO) named <code>authentication</code> reports Degraded for 10 minutes. Which operator orchestrates resolution?",
            options=[
                ("kubelet on each node.", False),
                ("Cluster Version Operator (CVO) — it watches all CO statuses, reports cluster-level health, and ensures CO\'s converge to the declared version. Investigate the <code>authentication</code> CO\'s logs first.", True),
                ("OLM — it only manages add-on operators, not core CO\'s.", False),
            ],
            feedback="CVO is the meta-operator that orchestrates every cluster operator. Cluster Available = all CO\'s Available + not Degraded.",
        ),
    },
    before_after_before='<p>Pre-OCP K8s deployments were assembly-required: pick a CNI, install Helm charts for ingress + monitoring + logging + GitOps + dev tools + registry; integrate auth via custom OIDC plumbing; bake AMIs / images per cloud; write per-cluster scripts for upgrades. <em>Six weeks of platform engineering before the first developer Pod ran.</em> No vendor accountability if any one piece broke.</p>',
    before_after_after='<p>OCP ships an <strong>opinionated platform</strong>: Routes (ingress), integrated OAuth + registry + console + monitoring + logging, OperatorHub-everywhere (one place to install certified add-ons), CVO orchestrating cluster operators, RHCOS as the immutable node OS managed by MCO, oc CLI extending kubectl. <strong>Day-1 cluster is production-shaped</strong>; the trade-off is learning Red Hat\'s opinions (SCCs, Routes vs Ingress, Projects-as-namespaces, oc adm flow). One vendor accountable for the whole platform.</p>',
    before_after_caption='<p class="ba-caption"><em>OCP trades K8s flexibility for Red Hat opinionation + enterprise support. The cost is learning Red Hat\'s additions; the benefit is platform-team-in-a-box.</em></p>',
    analogy_intro_html='''<p>K-Foundry is the Red Hat enterprise factory. The <strong>Welcome Hall</strong> is where every visitor enters. On the wall is a giant floor plan showing the whole foundry: 13 bays, each handling a different production stage. The Foundry Master (you, the OCP platform admin) hands you a hard hat at the door.</p>
    <p>Unlike DIY K8s where you arrive with empty land, OCP\'s Welcome Hall has the building <em>already built</em>: the central forge (apiserver), the safety regulations posted (SCCs), the conveyor system installed (Routes + Service mesh), the safety inspector\'s booth ready (Compliance Operator), the operator hub stocked (OLM), the maintenance schedule on the wall (CVO + ClusterOperators). You add your products (workloads); the foundry comes equipped to make them.</p>
    <p>The Foundry has 8 deployment shapes — same blueprint, different operating models. Self-build the foundry (OCP), rent a turnkey foundry from Red Hat (OSD), rent one jointly with a hyperscaler (ROSA on AWS / ARO on Azure / IBM Cloud / GCP), use the community blueprint (OKD), pack many foundries into one (HyperShift), or run a tiny one at the edge (MicroShift / SNO / CRC).</p>
    <p>The <strong>Cluster Version Operator (CVO)</strong> is the Foundry Master\'s lieutenant — keeps every operator on the floor working. The <strong>Machine Config Operator (MCO)</strong> manages the floors themselves (RHCOS). The <strong>OLM</strong> manages all the specialty operators that visit the foundry.</p>''',
    translation_rows=[
        ("Welcome Hall floor plan", "OCP architecture overview"),
        ("Foundry Master", "OCP platform admin (you)"),
        ("Foundry Master\'s lieutenant", "Cluster Version Operator (CVO)"),
        ("Floor manager", "Machine Config Operator (MCO)"),
        ("Specialty-operator scheduler", "Operator Lifecycle Manager (OLM)"),
        ("Conveyor system", "Routes (TLS edge / passthrough / re-encrypt)"),
        ("Build mold + casting press", "S2I (Source-to-Image) + BuildConfig + ImageStream"),
        ("Safety regulations posted", "Security Context Constraints (SCCs)"),
        ("Project area on the floor", "OpenShift Project (= K8s namespace +)"),
        ("Front desk badge issuer", "Integrated OAuth server"),
        ("Internal parts warehouse", "Integrated container registry"),
        ("Hardened immutable floor surface", "RHCOS (immutable ostree node OS)"),
        ("Foundry Master\'s CLI", "oc CLI (kubectl + OCP-aware commands)"),
        ("Two views of the floor", "Web console — Administrator + Developer perspectives"),
        ("Foundry-network of branch foundries", "Hosted Control Planes (HyperShift) + ACM"),
    ],
    analogy_stops="A real foundry has fixed equipment; OCP\'s opinionated platform is software-defined and reshapes via Operators. Some workloads need bespoke configs that fight the opinionated defaults — that\'s when the foundry metaphor breaks.",
    eli5="Red Hat sells a Kubernetes that\'s already set up like a factory — the conveyor belts, safety officers, registry, login, dev tools all built in. You can build your own factory (DIY K8s) or buy this one with all the equipment included.",
    eli10="OpenShift = upstream K8s + Red Hat\'s opinionated additions (Routes, SCCs, BuildConfigs, S2I, Projects, OAuth, registry, OperatorHub-everywhere) + RHCOS immutable node OS + Machine Config Operator + Cluster Version Operator orchestrating ~30 ClusterOperators + Operator Lifecycle Manager for add-ons. Eight deployment shapes (OCP self-managed, OSD, ROSA, ARO, IBM, GCP, OKD, HyperShift, MicroShift / SNO / CRC). oc CLI extends kubectl. Web console has Admin + Dev perspectives.",
    scenarios=[
        Scenario(
            name="Bank — picks ROSA for managed OCP on AWS",
            body="A regulated bank standardising on OCP. They have an AWS-first cloud strategy. Pick <strong>ROSA</strong> — Red Hat operates the control plane + nodes via AWS native services; the bank operates workloads + identity. Native AWS billing; PrivateLink to existing AWS infra. <em>Compliance posture inherits from Red Hat\'s ROSA service controls.</em>",
        ),
        Scenario(
            name="Telco edge — SNO + MicroShift across 800 sites",
            body="A telco runs OCP at 800 cell sites. Each site has constrained compute. Edge sites get <strong>SNO</strong> (full OCP on one node) for the larger ones; remote IoT gateways get <strong>MicroShift</strong>. All registered in <strong>RHACM</strong> (covered in O10). One pane of glass for 800 mini-clusters.",
        ),
        Scenario(
            name="Migration — DIY K8s + 12 Helm-installed add-ons → OCP",
            body="A platform team running 6 self-managed K8s clusters with Argo CD, Prometheus, Loki, Linkerd, cert-manager, sealed-secrets, etc., all installed via Helm. Drift across charts; upgrade hell. Migration to OCP: each Helm chart maps to a Red Hat-supported Operator; OLM-installed; one supported version per Operator per OCP minor. <em>Reduced from 12 self-installed Helm charts to 12 OLM-managed Operators with vendor support.</em>",
        ),
        Scenario(
            name="Dev experience — CRC for laptop dev, OCP-bare-metal for prod",
            body="A 100-engineer team. Dev: <strong>OpenShift Local (CRC)</strong> on every developer laptop — same OCP APIs as prod; <code>oc new-app</code> + <code>oc new-build</code> work locally. Prod: OCP on bare metal in two on-prem data centres. <em>Same Routes, same SCCs, same OAuth — dev and prod feel identical from the developer\'s side.</em>",
        ),
    ],
    misconceptions=[
        Misconception(
            myth="\"OCP is just K8s with a wrapper.\"",
            truth="OCP includes meaningful additions: Routes (predate Ingress, handle TLS termination), SCCs (predate PSA, stricter defaults), Projects (namespace + metadata + self-provisioning), OAuth server, integrated registry, ImageStreams, BuildConfigs, S2I, OperatorHub-everywhere, CVO orchestrating CO\'s. <em>You can use kubectl for everything but you\'ll miss half the workflow without oc + OCP-aware concepts.</em>",
        ),
        Misconception(
            myth="\"RHCOS is just RHEL with K8s installed.\"",
            truth="RHCOS is <strong>immutable ostree-based</strong> — no apt / yum / package install at runtime. Changes happen by deploying new ostree images managed by the <strong>Machine Config Operator</strong>. SSH disabled by default. <em>You customise nodes via <code>MachineConfig</code> YAML, not by SSH-ing to nodes</em>. RHEL is the upstream; RHCOS is OCP\'s opinionated subset for cluster nodes only.",
        ),
        Misconception(
            myth="\"OLM is required for all my K8s operators.\"",
            truth="OLM manages OperatorHub-installed operators. You can <em>still</em> install bring-your-own operators directly via <code>kubectl apply -f operator.yaml</code> + RBAC + CRDs. OLM\'s value: lifecycle management (versions, upgrades, dependencies, channels) + a curated catalog. For Red Hat-supported workloads, OLM is the path. For custom internal operators, OLM is optional.",
        ),
    ],
    flashcards=[
        Flashcard(front="What does OCP add on top of upstream K8s?", back="<strong>Routes</strong>, <strong>BuildConfigs</strong>, <strong>ImageStreams</strong>, <strong>S2I</strong>, <strong>Templates</strong>, <strong>SCCs</strong>, <strong>Projects</strong>, <strong>integrated OAuth</strong>, <strong>integrated registry</strong>, <strong>OperatorHub-everywhere</strong>. Plus RHCOS, MCO, CVO, OLM, oc CLI, and a two-perspective web console."),
        Flashcard(front="Eight OCP deployment shapes?", back="<strong>OCP self-managed</strong>, <strong>OSD</strong> (Red Hat-managed on AWS/GCP), <strong>ROSA</strong> (joint AWS+RH), <strong>ARO</strong> (joint Azure+RH), <strong>IBM Cloud</strong>, <strong>GCP</strong>, <strong>OKD</strong> (community), <strong>HyperShift</strong> (hosted control planes), <strong>MicroShift</strong> (ultra-edge) / <strong>SNO</strong> (single-node) / <strong>CRC</strong> (laptop dev)."),
        Flashcard(front="What is RHCOS and how do you change it?", back="<strong>RHCOS</strong> = immutable ostree-based node OS. SSH disabled by default. Customisation via <strong>MachineConfig</strong> YAML reconciled by the <strong>Machine Config Operator (MCO)</strong> — applied per <strong>MachineConfigPool</strong> (master, worker, custom). MCO drains, applies, reboots, validates."),
        Flashcard(front="What does the CVO do?", back="<strong>Cluster Version Operator</strong> orchestrates ~30 <strong>ClusterOperators</strong> (authentication, console, dns, etcd, ingress, monitoring, network, storage, etc.). Cluster Available = all CO\'s Available + not Degraded. CVO drives upgrades to the declared version."),
        Flashcard(front="What is OLM and what does it manage?", back="<strong>Operator Lifecycle Manager</strong> manages add-on operators installed via OperatorHub. Pieces: <strong>CatalogSource</strong> → <strong>Subscription</strong> → <strong>InstallPlan</strong> → <strong>ClusterServiceVersion (CSV)</strong>. Channels (stable, fast, etc.). Manual vs automatic approval."),
        Flashcard(front="What\'s a Project in OCP?", back="A K8s <strong>namespace</strong> + extra metadata (display name, description, requestor) + default RoleBindings + self-provisioner support via the OCP <code>ProjectRequest</code> API. Every namespace is a Project; every Project is a namespace."),
        Flashcard(front="oc vs kubectl?", back="<strong>oc</strong> is kubectl + OCP-aware commands: <code>oc new-app</code>, <code>oc new-build</code>, <code>oc start-build</code>, <code>oc adm</code> (cluster admin), <code>oc debug</code> (privileged debug Pod on a node), <code>oc rsync</code>, <code>oc port-forward</code>, <code>oc login</code> (OAuth flow). All kubectl commands work via oc."),
        Flashcard(front="When pick HyperShift?", back="When you need to operate <strong>many lightweight clusters densely</strong>. HyperShift runs the control planes (apiserver + etcd + controllers + scheduler) as Pods inside another OCP cluster. Each tenant cluster\'s control plane is a Pod set; data planes are isolated. Reduces per-cluster overhead at fleet scale."),
    ],
    quizzes=[
        Quiz(
            prompt="A cluster admin runs <code>oc edit clusterversion</code> and changes the <code>desiredUpdate</code>. What happens next?",
            answer="The <strong>Cluster Version Operator (CVO)</strong> sees the desired version change, validates the upgrade graph (channel, conditional updates), then orchestrates the upgrade across all <strong>ClusterOperators</strong>: each CO upgrades its own piece (authentication, console, etcd, ingress, monitoring, network, etc.) in dependency order. CVO\'s ClusterVersion status reports progress. Upgrades typically take 30-60 min for the control plane; node pools follow via MachineConfigPool rollouts (covered in O8). <em>You don\'t kubectl-bump apiserver yourself; you set ClusterVersion.spec.desiredUpdate, CVO does the rest.</em>",
        ),
        Quiz(
            prompt="A team\'s Helm chart uses <code>hostPath: /var/log</code> in their Deployment. Pod fails to start in OCP. What\'s happening, and what\'s the fix?",
            answer="OCP\'s default SCC <code>restricted-v2</code> blocks hostPath, hostNetwork, hostPID, hostIPC, runAsRoot, and several capabilities. Pod is rejected at admission. Fix paths: (1) Rewrite the workload to not need hostPath (typically just need stdout logs in OCP — the cluster-logging operator collects them). (2) If genuinely needed (e.g. a privileged DaemonSet for node monitoring), grant the Pod\'s ServiceAccount an SCC that allows it (e.g. <code>privileged</code> SCC via <code>oc adm policy add-scc-to-user</code>). Recommended: assess whether the workload genuinely needs hostPath; in OCP, most don\'t.",
        ),
        Quiz(
            prompt="The CTO walks in: \"Why are we paying for OCP when we could run vanilla K8s for free?\" Defend the line item.",
            answer="\"<strong>Red Hat\'s OCP is K8s with five things built in that we\'d otherwise build + operate ourselves:</strong> (1) Ingress + TLS (Routes), (2) Image registry + builds (BuildConfigs + ImageStreams + S2I), (3) Identity + RBAC (integrated OAuth + SCCs), (4) Operator-Hub-everywhere (curated, supported add-ons via OLM with one Red Hat support contract), (5) Web console with Admin + Dev perspectives. Plus RHCOS as the immutable node OS managed by MCO — eliminates the per-cluster patching + drift problem. <em>The cost is the support contract; the saving is not staffing a 10-person platform team to assemble these from open-source pieces and own the support burden across them.</em> If we genuinely have the engineers to operate vanilla K8s + 12 self-installed add-ons + custom RHCOS-equivalent immutable image pipeline, vanilla K8s is fine. Otherwise OCP is the platform-team-in-a-box.\"",
            cyoa=True,
            cyoa_tag="how the platform engineer answered the CTO",
        ),
    ],
    glossary=[
        GlossaryItem(name="OCP", definition="OpenShift Container Platform. Red Hat\'s opinionated K8s distribution. Self-managed deployment shape."),
        GlossaryItem(name="ROSA / ARO", definition="Joint Red Hat + cloud-provider managed OCP. ROSA on AWS, ARO on Azure."),
        GlossaryItem(name="OSD", definition="OpenShift Dedicated — Red Hat-managed OCP on AWS or GCP."),
        GlossaryItem(name="OKD", definition="Community / upstream-development distribution of OCP. Same code; no Red Hat support."),
        GlossaryItem(name="HyperShift", definition="Hosted Control Planes — control planes run as Pods inside another OCP cluster. Density at fleet scale."),
        GlossaryItem(name="MicroShift / SNO / CRC", definition="Edge / single-node / laptop variants of OCP."),
        GlossaryItem(name="RHCOS", definition="Red Hat CoreOS — immutable ostree-based node OS for OCP. Customised via MachineConfig + MCO."),
        GlossaryItem(name="MCO", definition="Machine Config Operator — manages RHCOS via MachineConfig YAML per MachineConfigPool."),
        GlossaryItem(name="CVO", definition="Cluster Version Operator — orchestrates ~30 ClusterOperators; drives upgrades."),
        GlossaryItem(name="ClusterOperator (CO)", definition="An operator that manages one piece of OCP (authentication, console, dns, etcd, ingress, monitoring, network, storage, etc.). ~30 of them."),
        GlossaryItem(name="OLM", definition="Operator Lifecycle Manager — manages add-on operators via CatalogSource → Subscription → InstallPlan → CSV."),
        GlossaryItem(name="Route", definition="OCP ingress primitive — TLS edge / passthrough / re-encrypt termination. Predates K8s Ingress."),
        GlossaryItem(name="SCC (Security Context Constraint)", definition="OCP\'s Pod-security admission system. Default: restricted-v2 (non-root, dropped caps, seccomp)."),
        GlossaryItem(name="Project", definition="OCP namespace + metadata + default RoleBindings + ProjectRequest API for self-provisioning."),
    ],
    recap_lead='OpenShift = K8s + Red Hat opinionated additions + RHCOS + MCO + CVO + OLM + 8 deployment shapes. The Welcome Hall floor plan is internalised; choose the deployment shape + understand the four core operators (CVO, MCO, OLM, OAuth).',
    recap_next='<strong>Next — O2: Installation Models.</strong> IPI vs UPI; Assisted Installer; Agent-based Installer; SNO + compact 3-node + two-node; bare-metal + vSphere + AWS + Azure + GCP + OpenStack; disconnected installs + mirrored registries + oc-mirror; install-config + Ignition + bootstrap node + OSUS.',
)
