# K-VAN V3 — V3 · kubeadm Cluster Bootstrap End-to-End

> Course: Vanilla Kubernetes (K-VAN, prereq: K-COM)
> Module V3 · kubeadm Cluster Bootstrap
> Companion preview: `/preview-kubernetes-vanilla-lesson-03.html`.

---

**🎯 If you remember nothing else:** `kubeadm init` runs **10 phases** in order: preflight, certs, kubeconfig, control-plane (static pods), etcd, mark-cp, bootstrap-token, kubelet, addon (CoreDNS + kube-proxy), upload-certs. `kubeadm join` uses a bootstrap token + CA hash (or certificate key for control-plane join). For HA: **API server LB** (kube-vip / HAProxy / external) + 3+ CP nodes. Alternatives: kubespray, RKE2, k3s, Talos, Cluster API.

## 1. kubeadm's mental model

kubeadm is a *cluster bootstrapper*, not a cluster lifecycle manager. It does one thing exceptionally well: take a prepared host (V2) and turn it into a working K8s control plane or worker. After that, the cluster is yours to manage — kubeadm doesn't install Argo CD, doesn't handle backup, doesn't do upgrades automatically (it does help with kubelet/control-plane upgrade — see V8).
    The kubeadm workflow:
    
      - `kubeadm init` on the first control-plane node (with HA: configure API LB + use `--upload-certs`).

      - `kubeadm join --control-plane` on additional control-plane nodes (with the cert key from step 1).

      - `kubeadm join` on each worker node (with the bootstrap token + CA hash).

      - Install a CNI (Lesson V4) — until then, nodes show `NotReady`.

      - Install add-ons (Lesson V5) — usually via Argo CD pointed at git.

    
    The whole bootstrap is YAML-configurable via `kubeadm config` objects.

## 2. Four configuration objects

Instead of `kubeadm init --apiserver-advertise-address=...` with 30 flags, write a YAML file:
    `# kubeadm-config.yaml
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
mode: ipvs                                       # or empty if Cilium replaces kube-proxy`
    Then: `kubeadm init --config kubeadm-config.yaml --upload-certs`. The `--upload-certs` flag stores control-plane certs in a Secret keyed by a generated *certificate key* — additional CP nodes use that key to fetch certs without manual file copy.

## 3. Three CP nodes behind a virtual IP

Single-control-plane is fine for labs. Production needs ≥ 3 CP nodes behind a load balancer. The LB is the `controlPlaneEndpoint` in the kubeadm config. Three popular options:
    
      - **kube-vip** — runs as a static Pod on each CP node; one CP holds the VIP via ARP/BGP. Self-contained, no extra infra. The 2026 default for kubeadm HA.

      - **HAProxy + keepalived** — classic. HAProxy load-balances; keepalived provides the VIP failover. More moving parts but battle-tested.

      - **External LB** — a hardware LB (F5, Citrix), MetalLB, or cloud LB. Outside the cluster; predictable.

    
    The LB must point at `:6443` on every CP node. Health check on `/livez` or TCP 6443. The LB IP/name goes into the API server's certificate SANs (otherwise clients hitting the LB get cert-name-mismatch errors).
    HA bootstrap order:
    
      - Start the LB pointing at cp-1 only (or all three with cp-1 as the only healthy backend).

      - `kubeadm init --config ... --upload-certs` on cp-1. Output includes both a *worker join command* and a *control-plane join command* with a certificate key.

      - `kubeadm join <LB>:6443 --token X --discovery-token-ca-cert-hash sha256:Y --control-plane --certificate-key Z` on cp-2, cp-3.

      - Workers: `kubeadm join <LB>:6443 --token X --discovery-token-ca-cert-hash sha256:Y`.

## 4. kubespray, RKE2, k3s, Talos, Cluster API

- **kubespray** — Ansible playbooks installing kubeadm under the hood. Good for hybrid teams already in Ansible. Complex but flexible.

      - **kOps** — declarative cluster lifecycle on cloud (mostly AWS). State in S3; kubeadm-like under the hood. Mature.

      - **RKE2** — Rancher's production K8s distribution. Single binary, FIPS-certified, focuses on regulated environments. CIS-hardened defaults.

      - **k3s** — Rancher's lightweight distribution. Single binary, < 100 MB, ideal for edge / IoT / small clusters. Production-grade for its niche.

      - **Talos Linux** — immutable OS designed for K8s. No SSH; machine-config API. `talosctl apply-config` instead of `kubeadm init`. Modern + opinionated.

      - **Cluster API (CAPI)** — declarative K8s-on-K8s. A management cluster runs CAPI controllers; workload clusters are `Cluster` + `Machine` CRDs. Provider plugins: CAPV (vSphere), CAPA (AWS), CAPZ (Azure), CAPG (GCP), CAPD (Docker — for testing). The right answer when you operate many clusters.

    
    **"Kubernetes the Hard Way"** (Kelsey Hightower) is the educational walkthrough — install K8s without any bootstrapper, by hand, on raw VMs. Don't do this for production; do it once to understand what kubeadm hides.
    [ deep dive — skip if new ]For 2026 production self-managed clusters: kubeadm is the most common path; Talos has gained massive ground for new clusters; CAPI is the standard for fleet management. RKE2 is the safe pick in regulated industries. k3s for edge.

## Before / After

**Before.** Manual install: SSH each node, generate certs by hand, distribute kubeconfigs, write systemd units, configure each component. Hours per node, drift-prone, no clear procedure to recover from a failed bootstrap.

**After.** One YAML file (`kubeadm-config.yaml`) committed to git. `kubeadm init` on cp-1, two `kubeadm join --control-plane` on cp-2/3, three `kubeadm join` on workers. CNI installed, cluster `Ready`. Reproducible from the same YAML; documented bootstrap.

kubeadm is the lingua franca of vanilla K8s. Even kubespray, kOps, and most distros use kubeadm under the hood. Master it.

## Analogy — the K-Frontier site

Frame Raising is the third site. The blueprint is drawn (V1), the soil is prepped (V2). Now you raise the frame: corner posts (control-plane nodes) first, anchored deep into the foundation (etcd). The first corner post is the hardest — it requires the survey lines to be exactly right. Once it stands, the next two come up quickly using the same templates and ties (cert key, bootstrap token). Workers are the rafters that span between the posts; they connect via standard joints (`kubeadm join`).

**Translation legend.**

| In the story… | …in vanilla Kubernetes |
|---|---|
| First corner post (hardest) | `kubeadm init` on cp-1 |
| Posts 2 and 3 | `kubeadm join --control-plane` on cp-2/3 |
| Foundation depth | etcd (stacked or external) |
| Plumb line + survey markers | API LB IP + cert SANs |
| Ties between posts | Certificate key + bootstrap token |
| Rafters spanning the frame | Worker nodes (`kubeadm join`) |
| Pre-cut framing kit (no on-site measuring) | kubeadm config YAML |
| Alternative builders | kubespray / RKE2 / k3s / Talos / Cluster API |

⚠️ *Analogy stops here:* The analogy stops here: real cluster bootstrap involves cryptographic key exchange, x509 cert issuance, and gRPC handshakes — not lumber and hammers. The framing metaphor undersells the precision needed at the cert + token layer.

## ELI5 / ELI10

**ELI5.** You build a treehouse. First you put up one corner post very carefully. Then you put up the other corner posts using the same plans. Then you nail in the platform.

**ELI10.** kubeadm bootstraps K8s in 10 phases. `kubeadm init` on the first CP node generates certs + starts static-pod control plane + etcd. Additional CP nodes join via certificate key (`--upload-certs`). Workers join via bootstrap token + CA hash. HA needs an API server LB pointing at all CP nodes. Configure via YAML (kubeadm-config), not flags. Alternatives: kubespray (Ansible), kOps (cloud), RKE2 (Rancher), k3s (edge), Talos (immutable), Cluster API (declarative fleet).

## Real-world scenarios

- **A startup using kube-vip + kubeadm for HA.** 3 control-plane bare-metal nodes. kube-vip static pod on each holds a shared VIP via ARP. `controlPlaneEndpoint: api.k8s.corp:6443` resolves to the VIP. `kubeadm init --config ... --upload-certs` on cp-1; cp-2/3 join with the printed cert key. Workers join over the next hour. Total bootstrap time: ~45 minutes from prepped nodes.
- **A bank using external HAProxy + keepalived.** Dedicated LB pair. HAProxy front-ends 6443 → 3 CP backends. keepalived holds the VIP. Compliance team likes the explicit LB tier they can monitor + audit. Bootstrap is the same kubeadm pattern; just `controlPlaneEndpoint` points at the HAProxy VIP.
- **A platform team using Cluster API + Talos.** Management cluster runs CAPI + Cluster Provider Talos. Workload clusters declared as YAML: `kind: Cluster` + `kind: TalosControlPlane` + `kind: MachineDeployment`. New cluster = git PR + CAPI provisions VMs (vSphere) + applies Talos config + cluster comes up. Fleet of 12 clusters managed declaratively.
- **An edge team using k3s on 200 retail stores.** Each store has a single-node k3s install (everything in one binary, ~80MB RAM at idle). Argo CD syncs from the central git repo. Per-store config differences via Kustomize overlays. Reboot recovery is 30 seconds. Vanilla K8s primitives, micro footprint.

## Common misconceptions

- **Myth:** "kubeadm installs everything I need."
  **Truth:** kubeadm bootstraps the control plane + helps workers join. It does NOT install a CNI (cluster is NotReady until you do), an ingress controller, cert-manager, or any other add-ons. V4 + V5 cover those.
- **Myth:** "`kubeadm reset` cleans everything."
  **Truth:** kubeadm reset removes most cluster state but leaves: the CNI plugin's data (`/etc/cni/net.d/*`), iptables rules from kube-proxy, etcd data on dedicated mounts. After reset, also: `iptables -F + -t nat -F`, `ipvsadm --clear`, remove CNI configs, remove etcd dir. Otherwise the next init re-uses stale state.
- **Myth:** "Cluster API is for huge orgs only."
  **Truth:** Even small teams benefit if they'll operate ≥ 3 clusters (dev/staging/prod, or per-tenant). The declarative model + provider plugins make per-cluster YAML changes way faster than running kubeadm 3 times.

## Recap

`kubeadm init` + `kubeadm join` bootstraps vanilla K8s in 10 phases. HA = API LB + 3 CP nodes + cert key + bootstrap token. Configure via YAML, not flags. Alternatives (kubespray / RKE2 / k3s / Talos / CAPI) for specific needs.

**Next — V4: CNI Installation and Networking.** The cluster is NotReady until a CNI plugin is installed. Cilium, Calico, MTU tuning, kube-proxy replacement, the modern data planes.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
