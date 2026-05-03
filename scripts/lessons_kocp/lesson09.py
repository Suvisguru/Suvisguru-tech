"""K-OCP O9 — OpenShift Virtualization (KubeVirt), AI (RHODS), Edge (SNO + MicroShift)."""
from _helpers import LessonSpec, Section, Flashcard, Quiz, Misconception, Scenario, PauseCheck, GlossaryItem

HERO_SVG = """<svg viewBox="0 0 760 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OpenShift Virtualization + AI + Edge.">
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#FBF7F0" stroke="#C8C2B6"/>
  <text x="380" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#3F4A5E">Special Castings Wing — VMs + AI + Edge</text>
  <rect x="40" y="65" width="220" height="125" rx="10" fill="#A04832" stroke="#3F4A5E"/>
  <text x="150" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">OpenShift Virtualization</text>
  <text x="150" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">KubeVirt — VMs as first-class</text>
  <text x="150" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">DataVolumes</text>
  <text x="150" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">live migration · snapshots</text>
  <text x="150" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">hot-plug NICs / disks</text>
  <text x="150" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FFFFFF">VMs + containers in one platform</text>
  <rect x="275" y="65" width="220" height="125" rx="10" fill="#5A9F7A" stroke="#3F4A5E"/>
  <text x="385" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">OpenShift AI (RHODS)</text>
  <text x="385" y="103" text-anchor="middle" font-size="9" fill="#FFFFFF">notebooks (Jupyter)</text>
  <text x="385" y="118" text-anchor="middle" font-size="9" fill="#FFFFFF">KServe (model serving)</text>
  <text x="385" y="133" text-anchor="middle" font-size="9" fill="#FFFFFF">Kubeflow Pipelines</text>
  <text x="385" y="148" text-anchor="middle" font-size="9" fill="#FFFFFF">distributed training</text>
  <text x="385" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FFFFFF">RHEL AI integration</text>
  <rect x="510" y="65" width="210" height="125" rx="10" fill="#7AB3CC" stroke="#3F4A5E"/>
  <text x="615" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#FBF1D6">Edge</text>
  <text x="615" y="103" text-anchor="middle" font-size="9" fill="#FBF1D6">Single Node OpenShift (SNO)</text>
  <text x="615" y="118" text-anchor="middle" font-size="9" fill="#FBF1D6">MicroShift (ultra-edge)</text>
  <text x="615" y="135" text-anchor="middle" font-size="9" fill="#FBF1D6">Local Zones</text>
  <text x="615" y="148" text-anchor="middle" font-size="9" fill="#FBF1D6">RHACM-managed fleets</text>
  <text x="615" y="170" text-anchor="middle" font-size="9" font-style="italic" fill="#FBF1D6">retail / telco / IoT</text>
</svg>"""


LESSON = LessonSpec(
    num="09", title_short="Virt + AI + Edge",
    title_full="O9 · OpenShift Virtualization (KubeVirt), AI (RHODS), Edge (SNO + MicroShift)",
    title_html="K-OCP O9 · Virtualization + AI + Edge",
    module_eyebrow="Module O9 · the Special Castings Wing",
    hero_sub_html='<strong>OpenShift Virtualization</strong> (KubeVirt-based) — run VMs as first-class K8s workloads alongside containers. <strong>DataVolumes</strong>, <strong>live migration</strong>, <strong>snapshots</strong>, <strong>hot-plug</strong> NICs/disks. <strong>OpenShift AI (formerly RHODS)</strong> — Jupyter notebooks, <strong>KServe</strong> model serving, <strong>Kubeflow Pipelines</strong>, distributed training; <strong>RHEL AI</strong> integration. <strong>Edge</strong>: <strong>Single Node OpenShift (SNO)</strong> for cell sites + retail; <strong>MicroShift</strong> for ultra-edge IoT; <strong>Local Zones</strong> for hyperscaler edge presence.',
    hero_illu_svg=HERO_SVG,
    nightmare_html="It\'s 3 AM. <em>\"VirtualMachine instance migrating; live migration failed mid-flight; storage corruption suspected.\"</em> The team\'s VM (a legacy Windows app on KubeVirt) was live-migrating to drain a node for an upgrade. Migration started; aborted at 78%; VM now in unknown state. The DataVolume backing it is on ODF; storage report shows healthy. <em>You don\'t know whether to power-cycle the VM, restore from snapshot, or wait + retry the migration.</em> Today\'s lesson: KubeVirt VM lifecycle + AI workloads + edge variants.",
    stamp_html="<strong>OCP Virtualization runs VMs as first-class CRs alongside containers; same RBAC, same storage, same networking. OpenShift AI = the Red Hat AI/ML platform stack. SNO + MicroShift extend OCP to the edge; RHACM federates fleets.</strong>",
    district_pin="ko-bay09", district_label="Special Castings Wing",
    sections=[
        Section(eyebrow="Section 1.1 · OpenShift Virtualization (KubeVirt)", h2="OpenShift Virtualization — VMs as first-class K8s workloads",
            body_html="""    <p><strong>OpenShift Virtualization</strong> = productized <strong>KubeVirt</strong>. Lets you run VMs (Windows, RHEL, Ubuntu, etc.) as <strong>VirtualMachine</strong> CRs alongside containers in the same OCP cluster. Use cases:</p>
    <ul>
      <li>Migrate from VMware vSphere — modernize at your own pace, keep VMs you can\'t containerize yet.</li>
      <li>Legacy Windows apps that don\'t containerize cleanly.</li>
      <li>Mixed workloads (containers + VMs) sharing the same Networks / NetworkPolicy / Routes / RBAC.</li>
    </ul>
    <p><strong>Core CRs:</strong>
    <ul>
      <li><strong>VirtualMachine (VM)</strong> — declarative VM spec.</li>
      <li><strong>VirtualMachineInstance (VMI)</strong> — running VM (auto-created from VM by virt-controller).</li>
      <li><strong>DataVolume</strong> — VM disk storage abstraction (creates a PVC + populates from a source — HTTP image, registry, blank, etc.).</li>
      <li><strong>VirtualMachineSnapshot / VirtualMachineRestore</strong> — point-in-time snapshots of VMs.</li>
      <li><strong>VirtualMachineInstanceMigration</strong> — live migration to another node.</li>
    </ul>
    <p><strong>Live migration</strong> moves a running VM between nodes (for maintenance / draining) without VM downtime. Requires shared storage (RWX or pre-attached block). Hot-plug NICs and disks on running VMs.</p>
    <p>Networking: Multus Pod-secondary networks for VM-to-physical-network bridging; VM gets a real VLAN-routed IP. <strong>OpenShift Virtualization Operator</strong> installs CRDs + virt-controllers + virt-launcher + virt-handler.</p>"""),
        Section(eyebrow="Section 1.2 · OpenShift AI (formerly RHODS)", h2="OpenShift AI — Jupyter, KServe, Kubeflow, distributed training",
            body_html="""    <p><strong>OpenShift AI</strong> (rebranded from <em>Red Hat OpenShift Data Science (RHODS)</em>) = Red Hat\'s ML platform on OCP. Components:</p>
    <ul>
      <li><strong>Notebooks</strong> — Jupyter, JupyterLab, RStudio, Visual Studio Code on Pods. Per-user workspaces; image catalog with curated stacks (PyTorch, TensorFlow, XGBoost).</li>
      <li><strong>KServe</strong> — managed Knative-based model-serving. Handles transformer-class large-model inference; auto-scaling, GPU support.</li>
      <li><strong>Kubeflow Pipelines (DSP — Data Science Pipelines)</strong> — ML workflow orchestration; reproducible training runs.</li>
      <li><strong>Distributed training</strong> via Kubeflow training operator (PyTorchJob, TFJob, MPIJob, MXJob).</li>
      <li><strong>RHEL AI</strong> integration — Red Hat\'s base inference platform with InstructLab + IBM Granite models; can be hosted on OCP via OpenShift AI.</li>
    </ul>
    <p>GPU workloads: <strong>NVIDIA GPU Operator</strong> manages drivers, runtime, device plugin. Pods request <code>nvidia.com/gpu</code>. MIG (Multi-Instance GPU) supported on H100/H200.</p>
    <p>For distributed training across many GPU nodes: combine PyTorchJob + topology-aware scheduling + RDMA / InfiniBand networking via SR-IOV.</p>
    <p>Use cases: enterprise model training + serving on OCP; combining traditional analytics + LLM inference on one platform; air-gapped + on-prem AI deployments where SaaS isn\'t an option.</p>"""),
        Section(eyebrow="Section 1.3 · SNO + MicroShift + Local Zones", h2="SNO + MicroShift + Local Zones — edge variants",
            body_html="""    <p><strong>Single Node OpenShift (SNO)</strong> — full OCP on one node. Same APIs, same operators, same web console as multi-node OCP. Use cases:</p>
    <ul>
      <li>Edge sites: cell towers, retail stores, factory floors, branch offices.</li>
      <li>Compact deployments where the cost of 3+2 is unjustified.</li>
      <li>Constrained sites: limited rack space / power / cooling.</li>
    </ul>
    <p>Trade-off: no zone redundancy; etcd is single-node (data resilience via storage backup, not quorum).</p>
    <p><strong>MicroShift</strong> — even smaller (sub-1GB-RAM) variant of OCP for IoT gateways, ATMs, kiosks, embedded devices. Subset of OCP CRDs (Routes, OperatorHub not included; lighter API surface). Optimised for 100s-of-MB footprint + restart in seconds.</p>
    <p><strong>Local Zones</strong> — AWS/Azure-style hyperscaler edge presence. ROSA on Local Zones extends ROSA into edge AWS metro POPs (Los Angeles, Boston, etc.) for ultra-low-latency to local users. Same OCP APIs; less round-trip to nearest data center.</p>
    <p>All three federate into <strong>RHACM</strong> for fleet-wide management (covered in O10): one console manages 800 SNOs, 1000 MicroShifts, and the central + Local Zones clusters.</p>"""),
        Section(eyebrow="Section 1.4 · combining: AI on edge, VMs at edge",
            h2="Combining the three — AI inference at edge, VMs migrated to OCP",
            body_html="""    <p><strong>VMware migration to OCP Virtualization</strong>: <strong>Migration Toolkit for Virtualization (MTV)</strong> — Operator-based tool that ingests VMs from vSphere and converts them to KubeVirt VirtualMachines on OCP. Schedule batches; preserve IPs; minimal downtime. <em>Path-of-record for vSphere → OCP modernisation.</em></p>
    <p><strong>AI inference at edge</strong>: deploy KServe + small LLMs (e.g., Granite, Llama 3 8B) on SNO at the edge. Local inference reduces latency + privacy. RHACM pushes models to the fleet of SNOs.</p>
    <p><strong>RHEL AI on OCP</strong>: RHEL AI is Red Hat\'s curated inference platform with IBM Granite models + InstructLab for fine-tuning. Hosted on OCP via OpenShift AI; enterprise-supported AI stack.</p>
    <p><strong>Specialty hardware:</strong> SR-IOV + DPDK for network-intensive AI workloads; Confidential Computing (AMD SEV) for sensitive PHI training; CMEK for encryption at rest.</p>"""),
    ],
    pause_check_after_section={2: PauseCheck(
        question="A team has 50 legacy Windows VMs on VMware they need to keep running but want consolidated platform with their containers. Path?",
        options=[("Rewrite all 50 VMs as containers.", False),
            ("Install OpenShift Virtualization Operator on OCP; use Migration Toolkit for Virtualization (MTV) to ingest the VMs from vSphere as VirtualMachine CRs. VMs run alongside containers in same cluster; modernise at your own pace.", True),
            ("Keep VMware indefinitely.", False)],
        feedback="OCP Virtualization + MTV is the modernisation path: VMs and containers coexist; same RBAC, same storage, same networking, same console.",
    )},
    before_after_before='<p>Pre-OCP Virtualization, VMs and K8s lived in separate worlds. VMware for legacy + Windows; K8s for new microservices. Two control planes; two ops teams; two RBAC systems; two storage stacks. AI workloads needed bring-your-own Jupyter + KServe + GPU operator. Edge K8s was DIY — k3s/k0s/MicroK8s with no Red Hat support; or full OCP that didn\'t fit on small hardware.</p>',
    before_after_after='<p>OCP unifies: <strong>VMs (KubeVirt) + containers + AI workloads + edge sites</strong> on one platform. <strong>OpenShift Virtualization</strong> + <strong>MTV</strong> for VMware migration. <strong>OpenShift AI</strong> for ML platform (notebooks + KServe + Kubeflow + RHEL AI). <strong>SNO + MicroShift + Local Zones</strong> for edge variants. <strong>RHACM</strong> manages the fleet.</p>',
    before_after_caption='<p class="ba-caption"><em>One platform for VMs + containers + AI + edge. Modernise legacy VMs without big-bang rewrites; deploy AI inference where the data lives.</em></p>',
    analogy_intro_html='''<p>The <strong>Special Castings Wing</strong> at K-Foundry handles the unusual products. Three specialty production lines.</p>
    <p>The <strong>VM Casting Line</strong> (OpenShift Virtualization / KubeVirt) makes VM-shaped products alongside the container-shaped ones. Same molds, same conveyors, same paint shop — but the output is a Windows server or RHEL VM instead of a container. The Migration Toolkit (MTV) takes vSphere-shaped products from the old foundry next door and recasts them as KubeVirt VMs.</p>
    <p>The <strong>AI Lab Wing</strong> (OpenShift AI / RHODS) handles ML workloads: scientist notebooks (Jupyter), model serving (KServe), pipelines (Kubeflow). Specialty heavy machinery (NVIDIA GPU Operator) for training; MIG to slice big GPUs into small ones; RHEL AI integration for productised inference.</p>
    <p>The <strong>Branch Foundry Network</strong> (Edge) extends the foundry to remote sites. Single Node OpenShift (SNO) at retail stores + cell sites; MicroShift at IoT / ATM / kiosk; Local Zones at hyperscaler edge POPs. RHACM (next bay) coordinates them all.</p>''',
    translation_rows=[("VM Casting Line", "OpenShift Virtualization (KubeVirt)"),
        ("VM-shaped product", "VirtualMachine (VM) CR + VirtualMachineInstance (VMI)"),
        ("VM disk recipe", "DataVolume CR"),
        ("In-flight VM relocation", "Live migration (VirtualMachineInstanceMigration CR)"),
        ("Hot-attach a NIC / drive", "Hot-plug NICs / disks on running VM"),
        ("vSphere migration loader", "Migration Toolkit for Virtualization (MTV)"),
        ("AI Lab Wing", "OpenShift AI (formerly RHODS)"),
        ("Scientist notebook", "Jupyter / JupyterLab / RStudio / VS Code on Pods"),
        ("Model-serving turbine", "KServe (Knative-based model serving)"),
        ("ML workflow pipeline", "Kubeflow Data Science Pipelines (DSP)"),
        ("Distributed training rig", "Kubeflow PyTorchJob / TFJob / MPIJob"),
        ("Heavy-machinery manager", "NVIDIA GPU Operator + MIG slicing"),
        ("Productised inference platform", "RHEL AI (Granite models + InstructLab)"),
        ("Branch Foundry — full-OCP edge", "Single Node OpenShift (SNO)"),
        ("Branch Foundry — IoT/ATM", "MicroShift (sub-GB OCP)"),
        ("Hyperscaler edge POP", "Local Zones (ROSA / OCP on AWS/Azure edge regions)")],
    analogy_stops="A real foundry has fixed casting lines; OCP\'s VM-and-container coexistence is software-defined. KubeVirt VMs share Pod scheduling + networking + storage primitives — the metaphor underplays the integration depth.",
    eli5="The Special Wing makes three things alongside regular containers: VMs (with the same controls as containers), AI experiments (with notebooks + GPU + model serving), and edge sites (small foundries at remote locations). Same factory; specialty production lines.",
    eli10="OCP Virtualization (KubeVirt) runs VMs as first-class CRs (VirtualMachine, DataVolume, live migration, hot-plug). MTV ingests VMware VMs. OpenShift AI = Jupyter notebooks + KServe model serving + Kubeflow Pipelines + distributed training + RHEL AI integration; NVIDIA GPU Operator + MIG. Edge = SNO (full OCP single node), MicroShift (sub-GB ultra-edge), Local Zones (hyperscaler edge). RHACM federates fleets.",
    scenarios=[
        Scenario(name="Bank — VMware migration via MTV; 200 VMs in 6 months",
            body="A bank with 200 legacy VMs on vSphere installs OpenShift Virtualization + MTV. 6-month migration: batch ingestion of VMs as VirtualMachine CRs; same network IPs preserved; minimal user-visible downtime. <em>VMware contract not renewed.</em>"),
        Scenario(name="ML team — OpenShift AI for enterprise model training",
            body="An ML team needs on-prem training (PHI data; can\'t leave the data centre). OpenShift AI installed on a 4-node GPU cluster (H100). Notebooks for scientists; PyTorchJob for distributed training; KServe for inference. RHEL AI hosts production Granite-3 inference. <em>End-to-end ML platform without SaaS.</em>"),
        Scenario(name="Retail — SNO at 800 stores + RHACM",
            body="Grocery chain runs OCP at 800 stores. Each store: 1 SNO node hosting POS + inventory + local AI inference (vision-based shelf monitoring). RHACM federates the fleet; new app rollout via Argo CD ApplicationSet → 800 stores in 30 minutes."),
        Scenario(name="Telco — Local Zones for sub-10ms 5G core",
            body="Telco running 5G UPF on ROSA in AWS Local Zones (Los Angeles, NYC, Chicago metros). Sub-10ms latency to local subscribers. Same OCP APIs as core ROSA cluster; deployed via RHACM Cluster Lifecycle."),
    ],
    misconceptions=[
        Misconception(myth="\"VMs in OCP are second-class — containers are the real deal.\"",
            truth="VirtualMachine CRs use the same Pod scheduling + networking + storage + RBAC + monitoring as containers. <em>VMs are first-class K8s workloads in OCP Virtualization.</em> Same kubectl/oc; same console; same Operators. Mixed workloads in the same cluster work cleanly."),
        Misconception(myth="\"OpenShift AI is just rebranded RHODS.\"",
            truth="<strong>Yes</strong> — Red Hat OpenShift Data Science (RHODS) was renamed to OpenShift AI. Same product evolution; expanded scope to include broader AI use cases beyond data science (LLM serving, RHEL AI integration). The brand changed; the platform continues."),
        Misconception(myth="\"SNO is just OCP on a small VM for testing.\"",
            truth="SNO is a <strong>specific cluster topology</strong>: full OCP control plane + worker on one node. Production-ready for edge use cases. Single etcd (no quorum); data resilience via storage backup. <em>Different from \"OCP on small VM for testing\" — designed for real edge production.</em>"),
    ],
    flashcards=[
        Flashcard(front="What is OpenShift Virtualization?", back="Productized KubeVirt — VMs as first-class CRs in OCP. VirtualMachine + VirtualMachineInstance + DataVolume + live migration + snapshot + hot-plug. VMs and containers in same cluster."),
        Flashcard(front="Five core OCP Virtualization CRs?", back="<strong>VirtualMachine (VM)</strong> declarative spec, <strong>VirtualMachineInstance (VMI)</strong> running VM, <strong>DataVolume</strong> disk source, <strong>VirtualMachineSnapshot/Restore</strong> snapshots, <strong>VirtualMachineInstanceMigration</strong> live migration."),
        Flashcard(front="What is MTV?", back="<strong>Migration Toolkit for Virtualization</strong>. Operator-based tool ingesting VMs from vSphere → KubeVirt VirtualMachines on OCP. Batches; preserves IPs; minimal downtime."),
        Flashcard(front="What is OpenShift AI (formerly RHODS)?", back="Red Hat\'s ML platform on OCP. Notebooks (Jupyter), KServe model serving, Kubeflow Pipelines, distributed training (PyTorchJob/TFJob/MPIJob), RHEL AI integration."),
        Flashcard(front="What does the NVIDIA GPU Operator do?", back="Manages NVIDIA driver + container runtime + device plugin lifecycle on GPU pools. MIG (Multi-Instance GPU) for slicing H100/H200. Required for advanced GPU features."),
        Flashcard(front="What is RHEL AI?", back="Red Hat\'s curated inference platform: IBM Granite models + InstructLab for fine-tuning + RHEL base. Hosted on OCP via OpenShift AI. Enterprise-supported AI stack."),
        Flashcard(front="What is SNO?", back="Single Node OpenShift — full OCP control plane + worker on one node. Same APIs as multi-node. For edge sites (cell, retail, factory). Single etcd; storage-backed resilience."),
        Flashcard(front="What is MicroShift and how is it different from SNO?", back="<strong>MicroShift</strong> = sub-1GB-RAM variant for IoT / kiosks / embedded. Lighter API surface (Routes / OperatorHub absent). Restarts in seconds. <strong>SNO</strong> = full OCP on one node. MicroShift for ultra-edge; SNO for edge sites with more capacity."),
    ],
    quizzes=[
        Quiz(prompt="Live migration of a Windows VM in OCP Virtualization fails at 78%. What\'s the diagnostic + recovery?",
            answer="(1) <code>oc get vmim -A</code> — find the migration object; check status + reason. (2) <code>oc describe vmim &lt;name&gt;</code> — failure cause: storage incompatibility (source/target node has different storage access), network (Multus secondary network not on target), CPU model mismatch, or virt-launcher Pod scheduling issue. (3) Check the VMI: <code>oc get vmi &lt;name&gt; -o yaml</code> — phase + conditions. Often the VMI returns to original node intact (live-migration is intent-to-move; rollback on failure). (4) If VMI is in unknown state: stop + restart the VM; restore from latest snapshot if needed. (5) Postmortem: ensure storage is RWX-shared or pre-attached block; ensure target nodes have required Multus networks."),
        Quiz(prompt="A telco wants to deploy a small LLM (Granite-7B) for local inference at 200 cell sites. Walk through the architecture.",
            answer="(1) Each cell site = SNO with GPU node (e.g., L4 GPU sufficient for 7B inference). (2) Install OpenShift AI Operator + KServe on each SNO. (3) Use RHACM (covered next module) ApplicationSet to push KServe InferenceService manifests to all 200 SNOs. (4) Model artifacts hosted in central S3 bucket / NooBaa; KServe pulls on cold-start. (5) Local app routes inference traffic to local SNO (no round-trip to central). (6) NVIDIA GPU Operator on each SNO manages driver + device plugin. (7) Optional: RHEL AI for managed inference platform with InstructLab fine-tuning for site-specific tuning. <em>Sub-100ms inference latency to local users.</em>"),
        Quiz(prompt="The CTO Slacks: \"Why are we keeping VMware? Just rewrite the legacy Windows apps as containers.\" Defend the OCP Virtualization path.",
            answer="\"<strong>Containerising legacy Windows apps is a multi-year project for the apps that are even feasible to containerise.</strong> Many legacy Windows apps depend on Windows desktop services, COM, MSMQ, or other patterns that don\'t containerise cleanly — or the source code is lost / vendored. <strong>OpenShift Virtualization gives us a middle path:</strong> migrate VMs from VMware to OCP via MTV (preserves IPs, minimal downtime); VMs run alongside our containers under one platform with one control plane, one RBAC, one storage stack. <em>VMware contract savings + container-platform consolidation in 6 months</em> vs 3-year container-rewrite project. We can rewrite individual VMs to containers over time at our own pace. <strong>Both old and new workloads on one supported platform.</strong>\"",
            cyoa=True, cyoa_tag="how the platform engineer answered the CTO"),
    ],
    glossary=[
        GlossaryItem(name="OpenShift Virtualization", definition="Productized KubeVirt. VMs as first-class CRs in OCP."),
        GlossaryItem(name="VirtualMachine (VM) CR", definition="Declarative VM spec. Companion: VirtualMachineInstance (VMI) for running VM."),
        GlossaryItem(name="DataVolume", definition="VM disk storage abstraction. Creates PVC + populates from source (HTTP image, registry, blank, etc.)."),
        GlossaryItem(name="Live migration (VMIM)", definition="VirtualMachineInstanceMigration CR. Moves running VM between nodes without downtime. Requires shared storage."),
        GlossaryItem(name="MTV (Migration Toolkit for Virtualization)", definition="Operator ingesting VMs from vSphere → KubeVirt VirtualMachines on OCP."),
        GlossaryItem(name="OpenShift AI (formerly RHODS)", definition="Red Hat\'s ML platform: notebooks + KServe + Kubeflow + distributed training + RHEL AI integration."),
        GlossaryItem(name="KServe", definition="Knative-based model-serving for ML inference. Auto-scaling, GPU support, transformers-class models."),
        GlossaryItem(name="Kubeflow Pipelines (DSP)", definition="ML workflow orchestration. Reproducible training runs."),
        GlossaryItem(name="NVIDIA GPU Operator", definition="Manages NVIDIA driver + runtime + device plugin lifecycle. MIG slicing for H100/H200."),
        GlossaryItem(name="RHEL AI", definition="Red Hat\'s curated inference platform — IBM Granite models + InstructLab fine-tuning. Hosted on OCP via OpenShift AI."),
        GlossaryItem(name="Single Node OpenShift (SNO)", definition="Full OCP on one node. Same APIs as multi-node. For edge sites."),
        GlossaryItem(name="MicroShift", definition="Sub-1GB-RAM OCP variant. IoT / ATM / kiosk. Lighter API surface; restarts in seconds."),
        GlossaryItem(name="Local Zones", definition="ROSA / OCP on hyperscaler edge metro POPs (AWS Local Zones / Azure edge regions). Sub-10ms to local users."),
    ],
    recap_lead='Three specialty production lines: VM (KubeVirt) + AI (RHODS / OpenShift AI) + Edge (SNO / MicroShift / Local Zones). MTV brings vSphere VMs in; RHACM federates the edge fleet.',
    recap_next='<strong>Next — O10: Multi-Cluster with ACM.</strong> RHACM (Open Cluster Management) — ManagedClusters, Placement, ApplicationSets, Policy, ObservabilityAddon. Hosted Control Planes at scale; Submariner integration.',
)
