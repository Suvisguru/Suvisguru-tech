# K-ADV-PE P2 — P2 · Backstage Deep Dive

> Course: K-ADV-PE (advanced specialization)
> Module P2 · Backstage
> Companion preview: `/preview-kubernetes-adv-pe-lesson-02.html`.

---

**🎯 If you remember nothing else:** **Backstage four pillars: Catalog, TechDocs, Scaffolder, Plugins. Catalog is the source of truth (every service registered with owner + tier). TechDocs surfaces every README; Scaffolder ships golden paths; Plugins integrate everything.**

## 1. Every Component / Service / API / Resource / System registered

**Catalog**: every entity registered via `catalog-info.yaml` in the repo (or auto-discovered). Entity kinds: *Component* (a service), *API* (REST/gRPC contract), *Resource* (DB / queue / SaaS), *System* (collection), *Domain* (collection of Systems), *User / Group*.
    Owners + lifecycle (production / experimental / deprecated) + tags + dependencies. "Who owns service-X?" answered in < 5 seconds.
    Auto-discovery: GitHub / GitLab integration scans org repos for `catalog-info.yaml` on cadence; new repos appear automatically.

## 2. Per-repo MkDocs rendered centrally

**TechDocs**: MkDocs (or AsciiDoc) lives in each repo at `docs/`; Backstage builds + serves centrally. *Documentation as code*: lives next to the code; PR-reviewed; versioned.
    Search across all repos' docs from one Backstage search. Replaces wiki silos.
    Build patterns: per-PR build (TechDocs in CI generates static site → S3 / GCS); Backstage TechDocs Backend serves from object storage. Recommended for scale.

## 3. Template engine generating repos + manifests

**Scaffolder**: templates declare parameters + steps. Steps include: `fetch:template` (skeleton render), `publish:github` (create repo), `catalog:register` (add to catalog), custom action (open PR for cluster onboarding). Parameters via Backstage form.
    Templates live in Git; PR-reviewed; versioned. Per-language / per-pattern: "new Go service," "new Postgres database," "new tenant namespace."
    Custom actions extend Scaffolder for org-specific patterns (e.g., "create AWS S3 bucket via Crossplane Claim PR").

## 4. Integrations + extensibility

**Plugins** integrate Backstage with everything: Argo CD (deployment status per service), Kubernetes (cluster + Pod view), PagerDuty (on-call + incidents), GitHub / GitLab (issues + PRs), Datadog / Grafana / Honeycomb (dashboards + traces), AWS / Azure / GCP (cloud resources), security tools (Snyk, Trivy).
    Each plugin is a React component + backend module; cluster admin installs; users see in service page.
    **Software Catalog API**: REST + GraphQL; programs query the catalog. CI pipelines + downstream tools consume catalog data — "who owns this commit?" "what tier is this?" — drives gates / alerts / routing.

## Before / After

**Before.** Pre-Backstage: ownership in spreadsheets / Slack / nobody-knows. Docs in scattered wikis. New service = manual setup ticket. Plugins absent or per-tool dashboards.

**After.** Backstage: Catalog is source of truth. TechDocs from repos. Scaffolder ships golden paths. Plugins surface every tool in one place. Service page is the developer's home.

*One portal; auto-discovered; doc-as-code; templated.*

## Analogy — the K-Workshop bench

The Catalog Drawer in K-Workshop holds index cards for every tool, every blueprint, every artifact. The card lists who built it, who owns it, what it does, where its docs live (TechDocs cabinet), how to make a new one (Scaffolder template), and which tools integrate (plugins).
    Apprentices flip through the drawer; Master Craftspeople keep it current.

**Translation legend.**

| In the story… | …in Kubernetes |
|---|---|
| Catalog Drawer | Backstage Catalog |
| Index card | catalog-info.yaml |
| Tool / blueprint / artifact | Component / API / Resource / System / Domain |
| Docs cabinet | TechDocs (per-repo MkDocs) |
| Make-new template | Scaffolder template |
| Tool integrations | Plugins (Argo CD / K8s / PagerDuty / etc.) |
| Programmatic queries | Software Catalog API |

⚠️ *Analogy stops here:* Index cards are physical; Backstage entities live in a database fed from Git. Stale catalog entries point to vanished services unless cleanup is automated.

## ELI5 / ELI10

**ELI5.** A drawer of index cards for everything in the workshop. The cards say who owns it, where the docs are, how to make a new one. Anyone can open the drawer and find what they need.

**ELI10.** **Catalog**: every Component / API / Resource / System / Domain registered via catalog-info.yaml. **TechDocs**: per-repo MkDocs auto-built + served centrally. **Scaffolder**: template engine generating new repos + manifests + catalog registration. **Plugins**: 100+ integrations (Argo CD / K8s / Datadog / PagerDuty / cloud / etc.). **Software Catalog API**: REST + GraphQL for programmatic queries.

## Real-world scenarios

- **3-AM ownership lookup.** On-call sees a failing Service; Backstage Catalog → owner + Slack channel + on-call rotation in 10 seconds. Pre-Backstage: 30-min Slack hunt. Time-to-mitigate cut materially.
- **Auto-discovery from GitHub org.** 200-repo org enables Backstage GitHub integration; existing repos with catalog-info.yaml appear automatically; new repos appear within 30 min. Catalog is current without manual maintenance.
- **Scaffolder template — new microservice.** "New Go service" template ships repo + Helm + CI + observability + Argo CD app. Developer answers 5 form questions; first deploy in 10 min; 100 services use the same template — uniformity from day 1.
- **Stale catalog entries.** Migration deleted services; catalog still listed them. Postmortem: nightly job verifies repo + Service exist; auto-flag stale entries; PR to delete. Catalog hygiene now automated.

## Common misconceptions

- **Myth:** "Backstage is just a service catalog."
  **Truth:** Catalog is one of four pillars. TechDocs + Scaffolder + Plugins make it an IDP storefront, not just a registry.
- **Myth:** "Backstage requires a dedicated team to operate."
  **Truth:** A small platform team (1-3 engineers) can operate Backstage at 100+ services. Hosted Backstage (Spotify Portal, Roadie) trades cost for setup time.
- **Myth:** "Plugins are optional."
  **Truth:** Without plugins, Backstage is mostly catalog. Argo CD + Kubernetes + PagerDuty plugins turn the service page into the developer's home — that's where adoption happens.

## Recap

Backstage = Catalog (source of truth) + TechDocs (doc-as-code) + Scaffolder (golden paths) + Plugins (every tool integrated). The IDP's storefront.

**Next — P3: Crossplane v2.** Providers + Compositions + XRDs + Functions + Configuration packages. Platform-as-API.

## Flashcards and quiz

See `flashcards.yaml` (8 cards) and `quiz.yaml` (3 questions).
