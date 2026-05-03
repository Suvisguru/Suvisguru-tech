#!/usr/bin/env python3
"""K-COM lesson generator (L18+).

Takes a structured lesson spec and produces a self-contained
preview-kubernetes-lesson-NN.html. The CSS, K-Town map, concept rail,
topbar, and script tag are pre-baked from L18; each lesson supplies
the body content (hero, sections, scenarios, quiz, recap, etc.).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Optional
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# All 24 districts in the K-Town atlas as of L18 — extended below as
# new lessons add Watchtower, Observatory, etc. Each entry is the SVG
# group inserted into the K-Town map (transform + label + pin number).
KTOWN_PINS = [
    # (slug, num_label, x, y, label_text, sub, special)
    ("kt-pin03", "03", 130, 75, "Climate Tower", None, None),
    ("kt-pin07", "07", 380, 55, "Rail Yard", None, None),
    ("kt-pin13", "13", 660, 65, "Airport", None, None),
    ("kt-pin02", "02", 90, 150, "Residential", None, None),
    ("kt-pin05", "05", 220, 200, "Industrial Kitchen", None, None),
    ("kt-pin06", "06", 530, 145, "Public Library", None, None),
    ("kt-pin11", "11", 700, 145, "Bank Vault", None, None),
    ("kt-pin08", "08", 610, 200, "Office Tower", None, None),
    ("kt-pin01", "01", 400, 200, "Mayor's Office", "city anchor", "anchor"),
    ("kt-pin15", "15", 170, 255, "Co-Living", None, None),
    ("kt-pin14", "14", 470, 255, "Permit Office", None, None),
    ("kt-pin09", "09", 660, 265, "Customs Warehouse", None, None),
    ("kt-pin10", "10", 350, 290, "Bakery District", None, None),
    ("kt-pin7-5", "7·5", 90, 335, "Foundation Tour", "primer", "primer"),
    ("kt-pin04", "04", 290, 340, "Port + Restaurants", None, None),
    ("kt-pin12", "12", 570, 340, "Harbour", None, None),
    ("kt-pin16", "16", 295, 255, "Dispatch Office", None, None),
    ("kt-pin17", "17", 530, 290, "Switchboard", None, None),
    # New districts added at Phase 3+ (see DECISIONS.md upon addition)
    ("kt-pin27", "27", 740, 105, "Watchtower", "security", None),
    ("kt-pin32", "32", 230, 105, "Observatory", "observability", None),
    ("kt-pin34", "34", 230, 295, "Power Station", "scale & resilience", None),
    ("kt-pin36", "36", 410, 295, "Print Shop", "delivery", None),
    ("kt-pin42", "42", 700, 305, "Workshop", "operators", None),
    ("kt-pin44", "44", 770, 245, "Detective's Office", "troubleshooting", None),
]

# Default district for each lesson (lesson_num -> kt-pin* id)
LESSON_DISTRICT = {
    "18": "kt-pin09",  # Customs Warehouse
    "19": "kt-pin09",
    "20": "kt-pin14",  # Permit Office
    "21": "kt-pin14",
    "22": "kt-pin16",  # Dispatch Office
    "23": "kt-pin16",
    "24": "kt-pin17",  # Switchboard
    "25": "kt-pin17",
    "26": "kt-pin17",
    "27": "kt-pin27",  # Watchtower (NEW)
    "28": "kt-pin27",
    "29": "kt-pin27",
    "30": "kt-pin11",  # Bank Vault Quarter
    "31": "kt-pin27",
    "32": "kt-pin32",  # Observatory (NEW)
    "33": "kt-pin32",
    "34": "kt-pin34",  # Power Station (NEW)
    "35": "kt-pin34",
    "36": "kt-pin36",  # Print Shop (NEW)
    "37": "kt-pin36",
    "38": "kt-pin06",  # Public Library
    "39": "kt-pin06",
    "40": "kt-pin36",
    "41": "kt-pin14",
    "42": "kt-pin42",  # Workshop (NEW)
    "43": "kt-pin17",
    "44": "kt-pin44",  # Detective's Office (NEW)
}

# Concept-rail items: ordered list of (lesson_num, label). Lessons
# already shipped (L01-L17, L7.5) come first; subsequent lessons added
# in curriculum order. The current lesson's row is marked as `current`;
# rows preceding it are `done`; rows after are upcoming.
CONCEPT_RAIL = [
    ("01", "L01 What is Kubernetes"),
    ("02", "L02 containers vs VMs"),
    ("03", "L03 reconciliation loop"),
    ("04", "L04 12-factor + monoliths"),
    ("05", "L05 K8s fit / overkill"),
    ("06", "L06 GitOps + SRE"),
    ("07", "L07 history + KEPs"),
    ("7-5", "L7.5 Linux primer", "primer"),
    ("08", "L08 namespaces &amp; cgroups"),
    ("09", "L09 runtimes &amp; OCI"),
    ("10", "L10 image building"),
    ("11", "L11 container security"),
    ("12", "L12 PID 1 &amp; lifecycle"),
    ("13", "L13 cluster architecture"),
    ("14", "L14 K8s API &amp; YAML"),
    ("15", "L15 Pods deep dive"),
    ("16", "L16 workload controllers"),
    ("17", "L17 services &amp; networking"),
    ("18", "L18 storage Pt 1 — PV/PVC/SC"),
    ("19", "L19 storage Pt 2 — CSI"),
    ("20", "L20 config &amp; secrets"),
    ("21", "L21 service accounts &amp; certs"),
    ("22", "L22 scheduling Pt 1"),
    ("23", "L23 scheduling Pt 2"),
    ("24", "L24 net foundations &amp; CNI"),
    ("25", "L25 Gateway API"),
    ("26", "L26 AdminNetworkPolicy"),
    ("27", "L27 RBAC &amp; Auth"),
    ("28", "L28 admission control"),
    ("29", "L29 policy engines"),
    ("30", "L30 supply chain"),
    ("31", "L31 multi-tenancy"),
    ("32", "L32 obs Pt 1 — logs/metrics"),
    ("33", "L33 obs Pt 2 — traces/eBPF"),
    ("34", "L34 autoscaling"),
    ("35", "L35 reliability &amp; HA"),
    ("36", "L36 Kustomize"),
    ("37", "L37 Helm 3"),
    ("38", "L38 Argo CD"),
    ("39", "L39 Flux CD"),
    ("40", "L40 progressive delivery"),
    ("41", "L41 CRDs deep dive"),
    ("42", "L42 Operators"),
    ("43", "L43 service mesh"),
    ("44", "L44 troubleshooting"),
]


# ---------------------------------------------------------------------------
# CSS — copy of the L18 style block. Per-lesson custom CSS is appended at the
# end of <style> via spec.extra_css.
# ---------------------------------------------------------------------------

BASE_CSS = """
  :root {
    --bg: #FBF7F0; --bg-card: #FFFFFF; --bg-soft: #F5EFE3;
    --ink: #2A2520; --ink-soft: #6B6058; --ink-faint: #9D9389;
    --line: #E8DDC8; --accent: #3F4A5E; --accent-soft: #ECEFF5;
    --warm: #D97757; --warm-soft: #FBE8DC; --warm-deep: #A04832;
    --cool: #4A8FA8; --cool-soft: #E0EEF3;
    --good: #5A9F7A; --good-soft: #E0EFE6;
    --gold: #E8B547; --gold-soft: #FBF1D6;
    --r-pill: 999px; --r-card: 16px; --r-soft: 10px;
    --shadow-sm: 0 2px 8px rgba(42,37,32,0.06);
    --shadow-md: 0 8px 24px rgba(42,37,32,0.08);
    --ease: cubic-bezier(0.4,0,0.2,1);
  }
  [data-theme="dark"] {
    --bg: #1B1814; --bg-card: #25201B; --bg-soft: #2D2722;
    --ink: #F5EFE3; --ink-soft: #B8AC9D; --ink-faint: #8A7E70;
    --line: #3A332C; --accent: #A4B4D0; --accent-soft: #2D3340;
    --warm: #E89070; --warm-soft: #3A2820;
    --cool: #7AB3CC; --cool-soft: #1F2E36;
    --good: #7DBE9C; --good-soft: #1F3328;
    --gold: #F0C268; --gold-soft: #382C18;
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth;scroll-padding-top:80px}
  body{margin:0;font-family:'ui-rounded','SF Pro Rounded',-apple-system,BlinkMacSystemFont,'Inter','Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--ink);line-height:1.65;font-size:18px;transition:background .25s var(--ease),color .25s var(--ease)}
  .topbar{position:sticky;top:0;background:rgba(251,247,240,.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);z-index:100}
  [data-theme="dark"] .topbar{background:rgba(27,24,20,.9)}
  .topbar-inner{max-width:820px;margin:0 auto;display:flex;align-items:center;gap:16px;padding:12px 24px}
  .brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:14px;color:var(--ink);text-decoration:none}
  .brand-mark{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,var(--warm),var(--gold));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:12px;box-shadow:var(--shadow-sm)}
  .brand .course{color:var(--ink-soft);font-weight:400;font-size:13px}
  .progress-pill{margin-left:auto;font-size:12px;color:var(--ink-soft);background:var(--bg-card);border:1px solid var(--line);padding:4px 10px;border-radius:var(--r-pill)}
  .theme-toggle{background:var(--bg-card);border:1px solid var(--line);color:var(--ink);padding:6px 12px;border-radius:var(--r-pill);cursor:pointer;font-size:12px;font-family:inherit}
  .theme-toggle:hover{background:var(--accent-soft)}
  main{max-width:820px;margin:0 auto;padding:48px 24px 96px}
  .hero{margin-bottom:48px;text-align:center}
  .eyebrow{display:inline-block;font-size:13px;font-weight:600;color:var(--warm);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px}
  h1{font-size:38px;font-weight:700;line-height:1.18;letter-spacing:-0.6px;margin:0 0 18px;color:var(--ink)}
  @media (max-width:600px){h1{font-size:28px}}
  .hero-sub{font-size:20px;color:var(--ink-soft);max-width:640px;margin:0 auto 28px;line-height:1.5}
  .hero-illu{margin:0 auto 16px;max-width:680px}
  .hero-illu svg{display:block;width:100%;height:auto}
  section.s{margin:64px 0;background:var(--bg-card);border:1px solid var(--line);border-radius:var(--r-card);padding:36px;box-shadow:var(--shadow-sm)}
  @media (max-width:600px){section.s{padding:24px}}
  .s-eyebrow{display:inline-block;font-size:11px;font-weight:700;color:var(--warm-deep);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;background:var(--warm-soft);padding:4px 10px;border-radius:var(--r-pill)}
  [data-theme="dark"] .s-eyebrow{color:var(--warm)}
  .s h2{font-size:26px;font-weight:700;line-height:1.25;letter-spacing:-0.4px;margin:8px 0 18px;color:var(--ink)}
  .s p{font-size:17px;line-height:1.65;margin:0 0 14px;color:var(--ink)}
  .s p:last-child{margin-bottom:0}
  .s strong{color:var(--ink);font-weight:600}
  .s em{color:var(--warm-deep);font-style:normal;font-weight:600}
  [data-theme="dark"] .s em{color:var(--warm)}
  .s code{font-family:'ui-monospace',monospace;font-size:14.5px;background:var(--accent-soft);padding:1px 6px;border-radius:4px;color:var(--accent)}
  .s ul, .s ol{font-size:16px;line-height:1.7;color:var(--ink);padding-left:22px;margin:8px 0 14px}
  .s ul li, .s ol li{margin-bottom:6px}
  .s ul code, .s ol code{font-family:'ui-monospace',monospace;font-size:14px;background:var(--accent-soft);padding:1px 5px;border-radius:3px;color:var(--accent)}
  .ba-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}
  @media (max-width:600px){.ba-grid{grid-template-columns:1fr}}
  .ba{padding:20px;border-radius:var(--r-soft);border:2px solid}
  .ba.before{background:var(--warm-soft);border-color:var(--warm)}
  .ba.after{background:var(--good-soft);border-color:var(--good)}
  .ba-label{display:inline-block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;padding:3px 10px;border-radius:var(--r-pill);margin-bottom:10px;color:#fff}
  .ba.before .ba-label{background:var(--warm)}
  .ba.after .ba-label{background:var(--good)}
  .ba p{font-size:15px;margin:0 0 8px;color:var(--ink)}
  .ba p:last-child{margin-bottom:0}
  .ba code{font-family:'ui-monospace',monospace;font-size:13px;background:rgba(255,255,255,0.55);padding:1px 5px;border-radius:3px;color:var(--ink)}
  [data-theme="dark"] .ba code{background:rgba(0,0,0,0.25)}
  .eli{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}
  @media (max-width:600px){.eli{grid-template-columns:1fr}}
  .eli-card{padding:22px;border-radius:var(--r-soft);background:var(--bg-soft);border:1px solid var(--line)}
  .eli-tag{display:inline-block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;padding:3px 10px;border-radius:var(--r-pill);margin-bottom:10px}
  .eli-tag.five{background:#FBF1D6;color:#8B5A00}
  .eli-tag.ten{background:#D6E4F8;color:#1F4F8B}
  .eli p{font-size:15px;margin:0;line-height:1.6}
  .eli code{font-family:'ui-monospace',monospace;font-size:12.5px;background:var(--bg-card);padding:1px 5px;border-radius:3px;color:var(--accent)}
  .scenarios{display:grid;gap:14px;margin-top:18px}
  .scenario{background:var(--bg-soft);border-left:4px solid var(--accent);border-radius:0 var(--r-soft) var(--r-soft) 0;padding:16px 20px}
  .scenario-name{font-weight:700;font-size:15px;color:var(--accent);margin:0 0 6px}
  .scenario p{font-size:14.5px;line-height:1.6;margin:0;color:var(--ink)}
  .scenario code{font-family:'ui-monospace',monospace;font-size:13px;background:var(--accent-soft);padding:1px 5px;border-radius:3px;color:var(--accent)}
  .flashcard-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-top:18px}
  .flashcard{perspective:1000px;height:180px;cursor:pointer}
  .flashcard-inner{position:relative;width:100%;height:100%;transition:transform .5s var(--ease);transform-style:preserve-3d}
  .flashcard.flipped .flashcard-inner{transform:rotateY(180deg)}
  .flashcard-face{position:absolute;width:100%;height:100%;backface-visibility:hidden;border-radius:var(--r-soft);padding:18px;display:flex;align-items:center;justify-content:center;text-align:center;font-size:13.5px;line-height:1.5}
  .flashcard-front{background:var(--bg-soft);border:1.5px solid var(--accent);color:var(--ink);font-weight:600}
  .flashcard-back{background:var(--accent);color:#fff;transform:rotateY(180deg);padding:14px;font-size:12.5px}
  [data-theme="dark"] .flashcard-back{background:var(--accent-soft);color:var(--ink)}
  .flashcard-hint{position:absolute;bottom:6px;right:8px;font-size:9px;color:var(--ink-faint);opacity:.7}
  .quiz-grid{display:flex;flex-direction:column;gap:12px;margin-top:18px}
  .quiz-card{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--r-soft);padding:18px}
  .quiz-prompt{font-weight:600;font-size:15px;margin:0 0 12px;color:var(--ink);line-height:1.55}
  .quiz-prompt code{font-family:'ui-monospace',monospace;font-size:13px;background:var(--bg-card);padding:1px 5px;border-radius:3px;color:var(--accent)}
  .quiz-reveal{background:var(--accent);color:#fff;border:0;padding:8px 16px;border-radius:var(--r-pill);font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;animation:btn-bob 2.4s ease-in-out infinite}
  [data-theme="dark"] .quiz-reveal{color:var(--bg)}
  .quiz-reveal:hover{filter:brightness(1.1);animation:none}
  .quiz-answer{display:none;margin-top:12px;padding:14px 16px;background:var(--good-soft);border-left:3px solid var(--good);border-radius:0 var(--r-soft) var(--r-soft) 0;font-size:14.5px;line-height:1.6}
  .quiz-answer.show{display:block}
  .quiz-answer code{font-family:'ui-monospace',monospace;font-size:13px;background:var(--bg-card);padding:1px 5px;border-radius:3px;color:var(--accent)}
  .quiz-answer-tag{display:block;font-size:11px;font-weight:700;color:var(--good);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:6px}
  @keyframes btn-bob{0%,100%{transform:translateY(0);box-shadow:0 0 0 0 rgba(63,74,94,0)}50%{transform:translateY(-2px);box-shadow:0 0 0 5px rgba(63,74,94,0.06)}}
  .glossary{margin-top:32px;background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--r-card);padding:20px 24px}
  .glossary summary{cursor:pointer;font-weight:600;font-size:15px;color:var(--ink);list-style:none;display:flex;align-items:center;gap:10px;user-select:none}
  .glossary summary::before{content:'\\1F4DA';font-size:18px}
  .glossary summary::after{content:'\\203A';margin-left:auto;font-size:22px;color:var(--ink-soft);transition:transform .2s var(--ease)}
  .glossary[open] summary::after{transform:rotate(90deg)}
  .glossary-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:18px}
  .gloss-item{background:var(--bg-card);border:1px solid var(--line);border-radius:var(--r-soft);padding:12px 14px}
  .gloss-name{font-weight:600;color:var(--accent);font-size:14px;margin-bottom:4px}
  .gloss-def{font-size:13px;color:var(--ink-soft);line-height:1.5}
  .gloss-def code{font-family:'ui-monospace',monospace;font-size:12px;background:var(--accent-soft);padding:1px 4px;border-radius:3px;color:var(--accent)}
  .recap{margin:48px 0 0;text-align:center;padding:32px 24px;background:linear-gradient(135deg,var(--good-soft) 0%,var(--bg-card) 100%);border:1px solid var(--good);border-radius:var(--r-card);box-shadow:var(--shadow-md)}
  .recap-badge{display:inline-block;background:var(--good);color:#fff;padding:6px 14px;border-radius:var(--r-pill);font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:14px}
  .recap p{font-size:19px;font-weight:600;line-height:1.4;color:var(--ink);margin:0 0 10px;max-width:560px;margin-left:auto;margin-right:auto}
  .recap-next{font-size:14.5px;color:var(--ink-soft);font-weight:400;margin-top:14px}
  .recap-next strong{color:var(--ink)}
  footer{text-align:center;padding:28px 24px;color:var(--ink-faint);font-size:12px;margin-top:36px}
  .role-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:24px}
  .role{background:var(--bg-card);border:1.5px solid var(--line);border-radius:var(--r-card);padding:18px;display:flex;flex-direction:column;gap:8px;box-shadow:var(--shadow-sm);border-top:5px solid var(--accent)}
  .role.r1{border-top-color:#3F4A5E}
  .role.r2{border-top-color:#5A9F7A}
  .role.r3{border-top-color:#D97757}
  .role.r4{border-top-color:#E8B547}
  .role-icon{font-size:30px;line-height:1}
  .role-name{font-weight:700;font-size:15px;margin:0;line-height:1.3}
  .role.r1 .role-name{color:#3F4A5E}[data-theme="dark"] .role.r1 .role-name{color:var(--accent)}
  .role.r2 .role-name{color:#3D7857}[data-theme="dark"] .role.r2 .role-name{color:var(--good)}
  .role.r3 .role-name{color:#A04832}[data-theme="dark"] .role.r3 .role-name{color:var(--warm)}
  .role.r4 .role-name{color:#8B5A00}[data-theme="dark"] .role.r4 .role-name{color:var(--gold)}
  .role-tag{font-size:13px;color:var(--ink-soft);font-style:italic;margin:0;line-height:1.3}
  .role-desc{font-size:13.5px;color:var(--ink);line-height:1.55;margin:0}
  .role-desc code{font-family:'ui-monospace',monospace;font-size:12.5px;background:var(--accent-soft);padding:1px 4px;border-radius:3px;color:var(--accent)}
  .role-who{font-size:12.5px;color:var(--ink-soft);margin-top:6px;font-style:italic}
  .am-table, .data-table{width:100%;border-collapse:collapse;margin-top:18px;font-size:14px;border:1px solid var(--line);border-radius:var(--r-soft);overflow:hidden}
  .am-table th, .data-table th{background:var(--bg-soft);text-align:left;padding:10px 14px;font-size:11px;font-weight:700;color:var(--ink-soft);text-transform:uppercase;letter-spacing:1.2px;border-bottom:1px solid var(--line)}
  .am-table td, .data-table td{padding:10px 14px;border-bottom:1px solid var(--line);color:var(--ink);vertical-align:top}
  .am-table tr:last-child td, .data-table tr:last-child td{border-bottom:0}
  .am-table code, .data-table code{font-family:'ui-monospace',monospace;font-size:12.5px;background:var(--accent-soft);padding:1px 4px;border-radius:3px;color:var(--accent)}
  .visually-hidden{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
  .district-line{max-width:820px;margin:0 auto;padding:14px 24px 0;font-size:14.5px;color:var(--ink-soft)}
  .district-line strong{color:var(--accent);font-weight:600}
  .ktown-map-wrap{max-width:820px;margin:0 auto 8px;padding:8px 24px}
  .ktown-map{display:block;width:100%;height:auto;max-width:760px;margin:0 auto}
  .ktown-map .pin .pin-circle{transition:fill .25s var(--ease);fill:var(--ink-faint)}
  .ktown-map .pin .pin-num{fill:var(--bg)}
  .ktown-map .pin .pin-label,.ktown-map .pin .pin-sub{fill:var(--ink-soft)}
  .ktown-map .pin-anchor:not(.active) .pin-circle{fill:var(--accent)}
  .ktown-map .pin-anchor:not(.active) .pin-label{fill:var(--accent);font-weight:700}
  .ktown-map .pin.active .pin-circle{fill:var(--warm)}
  .ktown-map .pin.active .pin-label{fill:var(--ink);font-weight:700}
  .ktown-map .pin.active .pin-halo{fill:var(--warm);opacity:.18}
  [data-theme="dark"] .ktown-map .pin .pin-num{fill:var(--bg-card)}
  .ktown-strip{list-style:none;padding:0;margin:0}
  .ktown-strip,.ktown-strip-label{display:none}
  @media (max-width:720px){
    .ktown-map{display:none}
    .ktown-strip{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin:0;padding:0}
    .ktown-strip-pin{width:10px;height:10px;border-radius:50%;background:var(--ink-faint);opacity:.55;transition:transform .15s var(--ease)}
    .ktown-strip-pin.ktown-strip-anchor{background:var(--accent);opacity:1;width:13px;height:13px;align-self:center}
    .ktown-strip-pin.active{background:var(--warm);opacity:1;box-shadow:0 0 0 3px rgba(217,119,87,.22);transform:scale(1.15)}
    .ktown-strip-label{display:block;margin:10px 0 0;text-align:center;font-size:13px;color:var(--ink-soft)}
    .ktown-strip-label strong{color:var(--ink);font-weight:600}
    .ktown-strip-label span{color:var(--ink-faint)}
  }
  .nightmare{margin:0 0 16px}
  .nightmare-box{background:var(--warm-soft);border:1px solid var(--warm);border-radius:var(--r-card);padding:18px 22px;color:var(--ink);text-align:left}
  .nightmare-tag{display:block;font-size:13px;font-weight:600;color:var(--warm-deep);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px}
  [data-theme="dark"] .nightmare-tag{color:var(--warm)}
  .nightmare-box p{margin:0;font-size:16px;line-height:1.6}
  .stamp{margin:16px 0}
  .stamp-box{background:var(--accent-soft);border:1.5px solid var(--accent);border-radius:var(--r-card);padding:18px 26px;text-align:center;font-size:18px;font-weight:600;line-height:1.45;color:var(--ink);margin:0}
  .stamp-box strong{font-weight:700;color:var(--accent)}
  [data-theme="dark"] .stamp-box,[data-theme="dark"] .stamp-box strong{color:var(--ink)}
  .translation-legend{margin:20px 0 0;border:1px solid var(--line);border-radius:var(--r-soft);overflow:hidden}
  .translation-legend table{width:100%;border-collapse:collapse;font-size:15px}
  .translation-legend th{text-align:left;padding:12px 16px;background:var(--bg-soft);font-size:11px;font-weight:700;color:var(--ink-soft);text-transform:uppercase;letter-spacing:1.2px;border-bottom:1px solid var(--line)}
  .translation-legend th:first-child{border-right:1px solid var(--line)}
  .translation-legend td{padding:11px 16px;line-height:1.55;border-bottom:1px solid var(--line);color:var(--ink);vertical-align:top}
  .translation-legend td:first-child{border-right:1px solid var(--line);width:48%;color:var(--ink-soft)}
  .translation-legend tr:last-child td{border-bottom:0}
  .translation-legend code{font-family:'ui-monospace',monospace;font-size:13px;background:var(--accent-soft);padding:1px 5px;border-radius:3px;color:var(--accent)}
  @media (max-width:600px){
    .translation-legend table,.translation-legend tbody,.translation-legend tr{display:block}
    .translation-legend td{display:block;border-right:0!important;width:100%}
    .translation-legend td:first-child{padding-bottom:4px;background:var(--bg-soft)}
    .translation-legend td:first-child::before{content:'In the story \\B7 ';font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:var(--ink-faint);display:block;margin-bottom:2px}
    .translation-legend td:last-child::before{content:'\\2026in Kubernetes \\B7 ';font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:var(--ink-faint);display:block;margin-bottom:2px}
    .translation-legend th{display:none}
  }
  .pause-check{margin:24px 0}
  .pause-check-box{background:var(--gold-soft);border:1px dashed var(--gold);border-radius:var(--r-soft);padding:16px 20px}
  .pause-check-tag{display:inline-block;font-size:11px;font-weight:700;color:var(--warm-deep);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px}
  [data-theme="dark"] .pause-check-tag{color:var(--gold)}
  .pause-check-q{margin:0 0 12px;font-size:15.5px;font-weight:600;color:var(--ink);line-height:1.55}
  .pause-check-q code{font-family:'ui-monospace',monospace;font-size:14px;background:var(--bg-card);padding:1px 5px;border-radius:3px;color:var(--accent)}
  .pause-check-opts{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:6px}
  .pause-check-opt{display:block;width:100%;text-align:left;background:var(--bg-card);border:1px solid var(--line);border-radius:var(--r-soft);padding:9px 12px;font-size:14.5px;font-family:inherit;color:var(--ink);cursor:pointer;transition:background .15s var(--ease),border-color .15s var(--ease)}
  .pause-check-opt:hover:not(.correct):not(.wrong){background:var(--bg-soft);border-color:var(--accent)}
  .pause-check-opt.correct{background:var(--good-soft);border-color:var(--good);color:var(--ink)}
  .pause-check-opt.wrong{background:var(--warm-soft);border-color:var(--warm-deep);color:var(--ink)}
  .pause-check-feedback{display:none;margin-top:10px;padding:10px 12px;background:var(--bg-card);border-left:3px solid var(--good);border-radius:0 var(--r-soft) var(--r-soft) 0;font-size:13.5px;line-height:1.55;color:var(--ink-soft)}
  .pause-check-feedback.show{display:block}
  .pause-check-feedback strong{color:var(--ink);font-weight:600}
  .misconceptions{margin:0 0 24px}
  .misconceptions h3{font-size:18px;font-weight:700;margin:0 0 12px;color:var(--ink);letter-spacing:-0.2px}
  .misconceptions-grid{display:grid;gap:10px}
  .misc-card{border:1px solid var(--line);border-radius:var(--r-soft);overflow:hidden}
  .misc-row{padding:11px 14px;font-size:14.5px;line-height:1.55}
  .misc-myth{background:var(--warm-soft);color:var(--ink);border-bottom:1px solid var(--line)}
  .misc-myth strong{color:var(--warm-deep);margin-right:6px}
  [data-theme="dark"] .misc-myth strong{color:var(--warm)}
  .misc-truth{background:var(--good-soft);color:var(--ink)}
  .misc-truth strong{color:var(--good);margin-right:6px}
  .misc-row code{font-family:'ui-monospace',monospace;font-size:13px;background:var(--bg-card);padding:1px 5px;border-radius:3px;color:var(--accent)}
  .analogy-stops{margin:18px 0 0;padding:11px 14px;background:var(--gold-soft);border-left:3px solid var(--gold);border-radius:0 var(--r-soft) var(--r-soft) 0;font-size:14px;font-style:italic;color:var(--ink);line-height:1.55}
  .skip-pill{display:inline-block;background:var(--bg-soft);color:var(--ink-faint);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;padding:2px 9px;border-radius:var(--r-pill);margin-right:8px;border:1px solid var(--line);vertical-align:1px}
  .skip-block{opacity:.85}
  .concept-rail{display:none;font-size:13px;line-height:1.55;color:var(--ink-soft)}
  .concept-rail-title{font-size:11px;font-weight:700;color:var(--ink-faint);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;display:block}
  .concept-rail-item{display:flex;align-items:flex-start;gap:8px;padding:3px 0}
  .concept-rail-icon{flex:0 0 auto;width:14px;text-align:center;font-weight:700;color:var(--ink-faint)}
  .concept-rail-item.done .concept-rail-icon{color:var(--good)}
  .concept-rail-item.current .concept-rail-icon{color:var(--accent)}
  .concept-rail-item.current{font-weight:600;color:var(--ink)}
  .concept-rail-here{margin-left:6px;color:var(--warm);font-style:italic;font-size:11.5px}
  .concept-rail-item.primer{font-style:italic;color:var(--ink-faint)}
  @media (min-width:1240px){.concept-rail{display:block;position:fixed;top:96px;left:max(16px,calc(50vw - 600px));width:170px;z-index:50;max-height:calc(100vh - 110px);overflow-y:auto;padding-right:8px}}
  .quiz-card.cyoa-quiz{background:linear-gradient(135deg,var(--gold-soft) 0%,var(--bg-soft) 100%);border-color:var(--gold)}
  .cyoa-tag{display:inline-block;background:var(--bg-card);color:var(--accent);padding:3px 10px;border-radius:var(--r-pill);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:10px;border:1px solid var(--line)}
  .cyoa-quiz .quiz-prompt{font-style:italic}
  .cyoa-quiz .quiz-answer{background:var(--bg-card);border-left-color:var(--accent)}
  .cyoa-quiz .quiz-answer-tag{color:var(--accent)}
  /* Animation */
  .anim-wrap{margin-top:18px;background:var(--bg-soft);border-radius:var(--r-soft);padding:16px}
  .anim-wrap svg{display:block;width:100%;height:auto;max-width:760px;margin:0 auto}
  .anim-controls{display:flex;gap:10px;align-items:center;justify-content:center;margin-top:14px;flex-wrap:wrap}
  .anim-btn{background:var(--bg-card);border:1.5px solid var(--line);color:var(--ink);padding:7px 14px;border-radius:var(--r-pill);font-size:13px;font-weight:600;cursor:pointer;font-family:inherit}
  .anim-btn:hover{background:var(--accent-soft);border-color:var(--accent)}
  .anim-btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
  [data-theme="dark"] .anim-btn.active{color:var(--bg)}
  .anim-readout{margin-top:12px;padding:10px 14px;background:var(--bg-card);border:1px solid var(--line);border-radius:var(--r-soft);font-size:14px;color:var(--ink-soft);text-align:center;min-height:40px;display:flex;align-items:center;justify-content:center}
  .anim-readout strong{color:var(--ink);margin-right:6px}
  .anim-readout code{font-family:'ui-monospace',monospace;font-size:13px;background:var(--accent-soft);padding:1px 5px;border-radius:3px;color:var(--accent)}
"""

SCRIPT_BLOCK = """
<script>
  // Each setup block is isolated so a failure in one (e.g. localStorage
  // blocked on file:// origins in Safari) does not kill the others —
  // notably the animation IIFE that the generator appends below.
  function safeStorageGet(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function safeStorageSet(key, val) { try { localStorage.setItem(key, val); } catch (e) {} }

  try {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
      const stored = safeStorageGet('lesson-theme');
      if (stored) {
        document.body.setAttribute('data-theme', stored);
        themeToggle.textContent = stored === 'dark' ? '\\u2600 Light' : '\\ud83c\\udf19 Dark';
      }
      themeToggle.addEventListener('click', () => {
        const cur = document.body.getAttribute('data-theme');
        const next = cur === 'light' ? 'dark' : 'light';
        document.body.setAttribute('data-theme', next);
        themeToggle.textContent = next === 'dark' ? '\\u2600 Light' : '\\ud83c\\udf19 Dark';
        safeStorageSet('lesson-theme', next);
      });
    }
  } catch (e) { console.warn('theme toggle setup failed', e); }

  try {
    document.querySelectorAll('.flashcard').forEach(card => card.addEventListener('click', () => card.classList.toggle('flipped')));
  } catch (e) { console.warn('flashcard setup failed', e); }

  try {
    document.querySelectorAll('.quiz-reveal').forEach(btn => {
      const showText = btn.textContent;
      const hideText = showText.replace(/^Show/, 'Hide');
      btn.addEventListener('click', () => {
        const ans = btn.parentElement.querySelector('.quiz-answer');
        const open = ans.classList.toggle('show');
        btn.textContent = open ? hideText : showText;
      });
    });
  } catch (e) { console.warn('quiz reveal setup failed', e); }

  try {
    document.querySelectorAll('.pause-check-box').forEach(box => {
      const opts = box.querySelectorAll('.pause-check-opt');
      const fb = box.querySelector('.pause-check-feedback');
      opts.forEach(opt => opt.addEventListener('click', () => {
        opts.forEach(o => o.classList.remove('correct','wrong'));
        opt.classList.add(opt.dataset.correct === 'true' ? 'correct' : 'wrong');
        fb.classList.add('show');
      }));
    });
  } catch (e) { console.warn('pause-check setup failed', e); }
</script>
"""


# ---------------------------------------------------------------------------
# Spec dataclass
# ---------------------------------------------------------------------------

@dataclass
class Section:
    eyebrow: str
    h2: str
    body_html: str  # raw HTML inside the <section class="s">


@dataclass
class Flashcard:
    front: str
    back: str


@dataclass
class Quiz:
    prompt: str
    answer: str
    cyoa: bool = False
    cyoa_tag: str = "at the next restart"


@dataclass
class Misconception:
    myth: str
    truth: str


@dataclass
class Scenario:
    name: str
    body: str


@dataclass
class PauseCheck:
    question: str
    options: list  # list of (text, is_correct)
    feedback: str


@dataclass
class GlossaryItem:
    name: str
    definition: str


@dataclass
class AnimationPhase:
    """One step in a mode timeline.

    `readout` is HTML for the narration line (e.g. "<strong>Step 1.</strong> ...").
    `move_to` is an (x, y) destination for the moving packet, or None to skip motion.
    `duration_ms` is the motion duration; `pause_after_ms` is the post-motion wait.
    `set_text` is a list of (element_id, new_text) to set at phase start.
    `set_attr` is a list of (element_id, attr_name, attr_value) tuples.
    """
    readout: str
    move_to: tuple = None
    duration_ms: int = 1100
    pause_after_ms: int = 1500
    set_text: list = None
    set_attr: list = None


@dataclass
class AnimationScene:
    """A mode (button) with its sequence of phases. Loops indefinitely."""
    mode_id: str
    button_label: str  # "▶ ClusterIP (internal)"
    mode_label: str    # text for #anim-mode-label
    initial_set_text: list = None  # element label swaps applied when mode starts
    phases: list = None


@dataclass
class Animation:
    """Section 6 animation. svg_body must include element id="anim-mode-label" + a moving packet g id="anim-pkg" (opacity:0 at start)."""
    h2: str
    intro: str
    svg_viewbox: str  # e.g. "0 0 760 320"
    svg_body: str      # static SVG body inside <svg>...</svg>
    initial_packet_xy: tuple   # (x, y) starting transform of #anim-pkg
    initial_readout: str       # default readout HTML
    scenes: list = None        # list of AnimationScene


@dataclass
class LessonSpec:
    num: str
    title_short: str  # e.g. "storage Pt 1" — used in pill, footer
    title_full: str   # full <h1>
    title_html: str   # <title> in head
    module_eyebrow: str  # e.g. "Module 9 · Lesson 18 · stateful workloads start here"
    hero_sub_html: str  # the hero subtitle
    hero_illu_svg: str  # raw <svg>...</svg> for hero illustration
    nightmare_html: str  # paragraph contents inside .nightmare-box
    stamp_html: str     # the one-sentence stamp paragraph (used at top + bottom)
    district_pin: str   # which kt-pin id is active
    district_label: str  # label for district-line and ktown-strip
    sections: list      # list of Section in order
    pause_check_after_section: dict  # dict[int -> PauseCheck] — insert after section index
    before_after_before: str
    before_after_after: str
    before_after_caption: str  # italic tail under before/after
    analogy_intro_html: str  # paragraphs before the translation-legend
    translation_rows: list  # list of (story, k8s) tuples
    analogy_stops: str
    eli5: str
    eli10: str
    scenarios: list  # list of Scenario
    misconceptions: list  # list of Misconception
    flashcards: list  # list of Flashcard
    quizzes: list  # list of Quiz (last one can be cyoa=True)
    glossary: list  # list of GlossaryItem
    recap_lead: str
    recap_next: str
    extra_css: str = ""
    animation: Optional['Animation'] = None


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------

def _render_pin(pin: tuple, active_id: str) -> str:
    slug, num, x, y, label, sub, special = pin
    is_active = slug == active_id
    classes = ["pin"]
    if special == "anchor":
        classes.append("pin-anchor")
    if special == "primer":
        classes.append("pin-primer")
    if is_active:
        classes.append("active")
    cls = " ".join(classes)
    halo_r = 22 if special == "anchor" else 18
    circle_r = 14 if special == "anchor" else 10
    circle_fill = "#3F4A5E" if special == "anchor" else "#9D9389"
    stroke_extra = ' stroke-dasharray="2,1.5"' if special == "primer" else ""
    num_fontsize = 11 if special == "anchor" else (8 if num == "7·5" else 9)
    num_y = 4 if special == "anchor" else 3
    label_y = 34 if special == "anchor" else 26
    label_fontsize = 11 if special == "anchor" else 10
    label_fontweight = ' font-weight="700"' if special == "anchor" else ""
    label_color = "#3F4A5E" if special == "anchor" else "#6B6058"
    sub_html = ""
    if sub:
        sub_y = 46 if special == "anchor" else 38
        sub_color = "#9D9389"
        sub_html = f'<text class="pin-sub" y="{sub_y}" text-anchor="middle" font-family="sans-serif" font-size="9" font-style="italic" fill="{sub_color}">{sub}</text>'
    return (
        f'<g class="{cls}" id="{slug}" transform="translate({x},{y})">'
        f'<circle class="pin-halo" r="{halo_r}" fill="#D97757" opacity="0"/>'
        f'<circle class="pin-circle" r="{circle_r}" fill="{circle_fill}" stroke="#FBF7F0" stroke-width="{2.5 if special=="anchor" else 2}"{stroke_extra}/>'
        f'<text class="pin-num" y="{num_y}" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="{num_fontsize}" font-weight="700" fill="#FBF7F0">{num}</text>'
        f'<text class="pin-label" y="{label_y}" text-anchor="middle" font-family="sans-serif" font-size="{label_fontsize}" fill="{label_color}"{label_fontweight}>{label}</text>'
        f'{sub_html}'
        f'</g>'
    )


TOTAL_LESSONS_IN_CURRICULUM = 45  # L01-L17 + L7.5 + L18-L44

# Map lesson_num → strip dot index (anchor at L01 = 0; L7.5 inserted between L07 and L08).
def _strip_index_for(lesson_num: str) -> int | None:
    if lesson_num == "7-5":
        return 7
    try:
        n = int(lesson_num)
    except ValueError:
        return None
    if n <= 7:
        return n - 1  # L01 = 0 (anchor), L02 = 1, ..., L07 = 6
    return n  # L08 = 8 (skip 7 = L7.5), ..., L44 = 44


def _render_ktown_map(active_pin: str, lesson_num: str, district_label: str) -> str:
    pins_svg = "\n    ".join(_render_pin(p, active_pin) for p in KTOWN_PINS)
    # Build 45 dots: index 0 is the anchor (L01); active dot matches current lesson
    active_idx = _strip_index_for(lesson_num)
    strip_parts = []
    for i in range(TOTAL_LESSONS_IN_CURRICULUM):
        cls = "ktown-strip-pin"
        if i == 0:
            cls += " ktown-strip-anchor"
        if i == active_idx:
            cls += " active"
        strip_parts.append(f'<li class="{cls}"></li>')
    strip_html = "\n    ".join(strip_parts)

    aria_label = f"Lesson {lesson_num}, {district_label}."
    return f"""<div class="ktown-map-wrap">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" class="ktown-map" role="img" aria-label="K-Town district map: lesson {lesson_num}">
    <title>K-Town district map · lesson {lesson_num}</title>
    <desc>Stylised map of K-Town. {district_label} highlighted.</desc>
    <defs>
      <linearGradient id="kt-water" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7AB3CC" stop-opacity="0.18"/><stop offset="100%" stop-color="#4A8FA8" stop-opacity="0.32"/></linearGradient>
      <linearGradient id="kt-base" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FBF7F0" stop-opacity="0.6"/><stop offset="100%" stop-color="#F5EFE3" stop-opacity="0.6"/></linearGradient>
    </defs>
    <rect x="20" y="20" width="760" height="380" rx="14" fill="url(#kt-base)" stroke="#E8DDC8" stroke-width="1"/>
    <text x="400" y="38" text-anchor="middle" font-family="ui-rounded,sans-serif" font-size="10" font-weight="700" letter-spacing="3" fill="#9D9389">K · TOWN</text>
    <path d="M 20 365 Q 200 358 400 363 T 780 365 L 780 400 L 20 400 Z" fill="url(#kt-water)"/>
    <path d="M 20 365 Q 200 358 400 363 T 780 365" stroke="#7AB3CC" stroke-width="0.9" fill="none" opacity="0.5"/>
    <text x="745" y="392" text-anchor="end" font-family="sans-serif" font-size="8" font-style="italic" fill="#4A8FA8" opacity="0.7">— bay —</text>
    <rect x="615" y="76" width="140" height="9" rx="1" fill="#C9BFAE" opacity="0.5"/>
    <line x1="625" y1="80.5" x2="750" y2="80.5" stroke="#FBF7F0" stroke-width="0.7" stroke-dasharray="6,4" opacity="0.7"/>
    <line x1="320" y1="35" x2="450" y2="35" stroke="#5F5E5A" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.45"/>
    {pins_svg}
  </svg>
  <ol class="ktown-strip" aria-hidden="true">
    {strip_html}
  </ol>
  <p class="ktown-strip-label">\U0001F4CD <strong>{district_label}</strong> <span>· lesson {lesson_num} of {TOTAL_LESSONS_IN_CURRICULUM}</span><span class="visually-hidden">{aria_label}</span></p>
</div>"""


def _render_concept_rail(current_num: str) -> str:
    items = []
    found_current = False
    for entry in CONCEPT_RAIL:
        num = entry[0]
        label = entry[1]
        cls_extra = entry[2] if len(entry) > 2 else None
        if num == current_num:
            cls = "concept-rail-item current"
            if cls_extra == "primer":
                cls += " primer"
            icon = "▶"  # ▶
            here = '<span class="concept-rail-here">← here</span>'
            found_current = True
        elif not found_current:
            cls = "concept-rail-item done"
            if cls_extra == "primer":
                cls += " primer"
            icon = "✓"  # ✓
            here = ""
        else:
            cls = "concept-rail-item"
            if cls_extra == "primer":
                cls += " primer"
            icon = "○"  # ○
            here = ""
        items.append(
            f'  <div class="{cls}"><span class="concept-rail-icon">{icon}</span><span>{label}</span>{here}</div>'
        )
    items_html = "\n".join(items)
    return f"""<aside class="concept-rail" aria-label="Concept journey through the K-COM course">
  <span class="concept-rail-title">Concept journey</span>
{items_html}
</aside>"""


def _render_pause_check(pc: 'PauseCheck') -> str:
    opts = "\n        ".join(
        f'<li><button type="button" class="pause-check-opt" data-correct="{str(c).lower()}">{t}</button></li>'
        for t, c in pc.options
    )
    return f"""  <div class="pause-check">
    <div class="pause-check-box">
      <span class="pause-check-tag">⏸ Pause and check</span>
      <p class="pause-check-q">{pc.question}</p>
      <ul class="pause-check-opts">
        {opts}
      </ul>
      <p class="pause-check-feedback">{pc.feedback}</p>
    </div>
  </div>"""


def _render_section(idx: int, sec: 'Section') -> str:
    return f"""  <section class="s">
    <span class="s-eyebrow">{sec.eyebrow}</span>
    <h2>{sec.h2}</h2>
{sec.body_html}
  </section>"""


def _render_animation(anim: 'Animation') -> tuple:
    """Returns (section_html, script_js). section_html slots in between
    Section 5 (scenarios) and Section 7 (misconceptions/quiz). script_js
    is appended to the page's bottom <script> block."""
    if anim is None:
        return "", ""

    buttons = []
    for i, scene in enumerate(anim.scenes):
        cls = "anim-btn active" if i == 0 else "anim-btn"
        buttons.append(f'<button class="{cls}" type="button" data-mode="{scene.mode_id}">{scene.button_label}</button>')
    buttons_html = "\n        ".join(buttons)

    section_html = f"""  <section class="s">
    <span class="s-eyebrow">Section 6 · Animation</span>
    <h2>{anim.h2}</h2>
    <p>{anim.intro}</p>
    <div class="anim-wrap">
      <svg viewBox="{anim.svg_viewbox}" xmlns="http://www.w3.org/2000/svg" id="lesson-anim" role="img">
{anim.svg_body}
        <g id="anim-pkg" opacity="0" transform="translate({anim.initial_packet_xy[0]},{anim.initial_packet_xy[1]})">
          <circle r="9" fill="#D97757"/>
          <text y="3" text-anchor="middle" font-size="9" fill="#FFF" font-weight="700">📦</text>
        </g>
      </svg>
      <div class="anim-controls">
        {buttons_html}
      </div>
      <div class="anim-readout" id="anim-readout">{anim.initial_readout}</div>
    </div>
  </section>"""

    # Build a JS data structure describing every scene + phase
    scenes_data = []
    for scene in anim.scenes:
        phases_data = []
        for ph in scene.phases:
            phase = {
                "readout": ph.readout,
                "move_to": list(ph.move_to) if ph.move_to else None,
                "duration_ms": ph.duration_ms,
                "pause_after_ms": ph.pause_after_ms,
                "set_text": list(ph.set_text) if ph.set_text else None,
                "set_attr": list(ph.set_attr) if ph.set_attr else None,
            }
            phases_data.append(phase)
        scenes_data.append({
            "mode_id": scene.mode_id,
            "mode_label": scene.mode_label,
            "initial_set_text": list(scene.initial_set_text) if scene.initial_set_text else None,
            "phases": phases_data,
        })
    initial_xy = list(anim.initial_packet_xy)
    scenes_json = json.dumps(scenes_data)
    initial_xy_json = json.dumps(initial_xy)

    script_js = """
  // -------- Animation --------
  // _scope: in individual lesson HTML, no course-section ancestor exists -
  // _scope falls back to document. In combined-course HTML, document.currentScript
  // is inside a per-lesson section.course-section element - _scope is that section.
  // This keeps each combined-view lesson animation isolated to its own DOM subtree.
  try {{ (function() {{
    const _scope = (document.currentScript && document.currentScript.closest && document.currentScript.closest('section.course-section')) || document;
    // _byId: use attribute selector ([id="..."]) instead of #id selector to
    // force tree-walking of _scope. The #id selector goes via the document
    // id-element-map and would return null if the first matching element
    // in the document isn't a descendant of _scope (which happens in
    // combined-course view where every lesson section has its own
    // anim-pkg / anim-readout / anim-mode-label with the same id).
    const _byId = id => _scope.querySelector('[id="' + id + '"]');
    const SCENES = {scenes_json};
    const INITIAL_XY = {initial_xy_json};
    const animModeLabel = _byId('anim-mode-label');
    const animReadout = _byId('anim-readout');
    const animPkg = _byId('anim-pkg');
    const modeBtns = _scope.querySelectorAll('.anim-btn[data-mode]');
    if (!animPkg) return;

    let timer = null;
    let currentXY = INITIAL_XY.slice();

    function clearTimer() {{ if (timer) {{ clearTimeout(timer); timer = null; }} }}

    function setText(pairs) {{
      if (!pairs) return;
      pairs.forEach(p => {{
        const el = _byId(p[0]);
        if (el) el.textContent = p[1];
      }});
    }}
    function setAttr(triples) {{
      if (!triples) return;
      triples.forEach(t => {{
        const el = _byId(t[0]);
        if (el) el.setAttribute(t[1], t[2]);
      }});
    }}

    function moveTo(end, duration, done) {{
      const start = currentXY.slice();
      animPkg.setAttribute('opacity', '1');
      const t0 = performance.now();
      function frame(t) {{
        const k = Math.min((t - t0) / duration, 1);
        const e = k < 0.5 ? 2*k*k : 1 - Math.pow(-2*k+2, 2)/2;
        const x = start[0] + (end[0] - start[0]) * e;
        const y = start[1] + (end[1] - start[1]) * e;
        animPkg.setAttribute('transform', 'translate(' + x + ',' + y + ')');
        if (k < 1) requestAnimationFrame(frame);
        else {{ currentXY = [end[0], end[1]]; if (done) done(); }}
      }}
      requestAnimationFrame(frame);
    }}

    function runScene(modeId) {{
      clearTimer();
      const scene = SCENES.find(s => s.mode_id === modeId);
      if (!scene) return;
      if (animModeLabel) animModeLabel.textContent = scene.mode_label;
      setText(scene.initial_set_text);
      // Reset packet to start
      currentXY = INITIAL_XY.slice();
      animPkg.setAttribute('transform', 'translate(' + INITIAL_XY[0] + ',' + INITIAL_XY[1] + ')');
      animPkg.setAttribute('opacity', '0');

      let i = 0;
      function nextPhase() {{
        if (i >= scene.phases.length) {{ i = 0; currentXY = INITIAL_XY.slice(); animPkg.setAttribute('opacity', '0'); animPkg.setAttribute('transform', 'translate(' + INITIAL_XY[0] + ',' + INITIAL_XY[1] + ')'); timer = setTimeout(nextPhase, 800); return; }}
        const p = scene.phases[i++];
        animReadout.innerHTML = p.readout;
        setText(p.set_text);
        setAttr(p.set_attr);
        if (p.move_to) {{
          moveTo(p.move_to, p.duration_ms, () => {{ timer = setTimeout(nextPhase, p.pause_after_ms); }});
        }} else {{
          timer = setTimeout(nextPhase, p.pause_after_ms);
        }}
      }}
      nextPhase();
    }}

    modeBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        modeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        runScene(btn.dataset.mode);
      }});
    }});
    // Auto-start first scene
    if (SCENES.length) runScene(SCENES[0].mode_id);
  }})(); }} catch (e) {{ console.warn('animation setup failed', e); }}
""".format(scenes_json=scenes_json, initial_xy_json=initial_xy_json)

    return section_html, script_js


def render_lesson(spec: LessonSpec) -> str:
    css = BASE_CSS + (spec.extra_css or "")
    map_html = _render_ktown_map(spec.district_pin, spec.num, spec.district_label)
    rail_html = _render_concept_rail(spec.num)

    sections_html = []
    for i, sec in enumerate(spec.sections):
        sections_html.append(_render_section(i, sec))
        if i in spec.pause_check_after_section:
            sections_html.append(_render_pause_check(spec.pause_check_after_section[i]))
    sections_block = "\n\n".join(sections_html)

    # before / after
    ba_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 2 · Before &amp; After</span>
    <h2>What changes when you adopt this</h2>
    <div class="ba-grid">
      <div class="ba before"><span class="ba-label">Before</span>{spec.before_after_before}</div>
      <div class="ba after"><span class="ba-label">After</span>{spec.before_after_after}</div>
    </div>
    {spec.before_after_caption}
  </section>"""

    # analogy
    legend_rows = "\n".join(
        f'          <tr><td>{story}</td><td>{k8s}</td></tr>'
        for story, k8s in spec.translation_rows
    )
    analogy_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 3 · Analogy</span>
    <h2>The story for this district</h2>
{spec.analogy_intro_html}
    <div class="translation-legend">
      <table>
        <thead><tr><th>In the story…</th><th>…in Kubernetes</th></tr></thead>
        <tbody>
{legend_rows}
        </tbody>
      </table>
    </div>
    <p class="analogy-stops">⚠️ <em>{spec.analogy_stops}</em></p>
  </section>"""

    eli_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 4 · Two-level explanation</span>
    <h2>Two ways to hear it</h2>
    <div class="eli">
      <div class="eli-card">
        <span class="eli-tag five">ELI5 · explain like I'm 5</span>
        <p>{spec.eli5}</p>
      </div>
      <div class="eli-card">
        <span class="eli-tag ten">ELI10 · explain like I'm 10</span>
        <p>{spec.eli10}</p>
      </div>
    </div>
  </section>"""

    scenarios_html = "\n".join(
        f'      <div class="scenario"><p class="scenario-name">{s.name}</p><p>{s.body}</p></div>'
        for s in spec.scenarios
    )
    scenarios_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 5 · Real-world scenarios</span>
    <h2>How real teams use this</h2>
    <div class="scenarios">
{scenarios_html}
    </div>
  </section>"""

    miscs_html = "\n".join(
        f'        <div class="misc-card">'
        f'<div class="misc-row misc-myth"><strong>Myth:</strong> {m.myth}</div>'
        f'<div class="misc-row misc-truth"><strong>Truth:</strong> {m.truth}</div>'
        f'</div>'
        for m in spec.misconceptions
    )
    flashcards_html = "\n".join(
        f'      <div class="flashcard"><div class="flashcard-inner">'
        f'<div class="flashcard-face flashcard-front">{f.front}<div class="flashcard-hint">tap to flip</div></div>'
        f'<div class="flashcard-face flashcard-back">{f.back}</div>'
        f'</div></div>'
        for f in spec.flashcards
    )

    quiz_cards_html = []
    for q in spec.quizzes:
        if q.cyoa:
            quiz_cards_html.append(
                f'      <div class="quiz-card cyoa-quiz">'
                f'<span class="cyoa-tag">\U0001F3AC Choose Your Own Adventure</span>'
                f'<p class="quiz-prompt">{q.prompt}</p>'
                f'<button class="quiz-reveal" type="button">Show what happened</button>'
                f'<div class="quiz-answer"><span class="quiz-answer-tag">{q.cyoa_tag}</span>{q.answer}</div>'
                f'</div>'
            )
        else:
            quiz_cards_html.append(
                f'      <div class="quiz-card">'
                f'<p class="quiz-prompt">{q.prompt}</p>'
                f'<button class="quiz-reveal" type="button">Show answer</button>'
                f'<div class="quiz-answer"><span class="quiz-answer-tag">answer</span>{q.answer}</div>'
                f'</div>'
            )
    quizzes_html = "\n".join(quiz_cards_html)

    anim_section, anim_script = _render_animation(spec.animation)

    # Combine the static script block with any per-lesson animation script.
    # SCRIPT_BLOCK ends with `</script>`. Insert the animation script just before that.
    if anim_script:
        combined_script = SCRIPT_BLOCK.rstrip().rstrip("</script>").rstrip() + "\n" + anim_script + "\n</script>\n"
    else:
        combined_script = SCRIPT_BLOCK

    misc_quiz_block = f"""  <section class="s">
    <span class="s-eyebrow">Section 7 · Misconceptions, flashcards &amp; quiz</span>
    <h2>Lock it in</h2>
    <p>A few common misconceptions to clear up first, then the flashcards and quiz.</p>
    <div class="misconceptions">
      <h3>Common Misconceptions</h3>
      <div class="misconceptions-grid">
{miscs_html}
      </div>
    </div>
    <div class="flashcard-grid">
{flashcards_html}
    </div>
    <div class="quiz-grid" style="margin-top:24px">
{quizzes_html}
    </div>
  </section>"""

    glossary_html = "\n".join(
        f'      <div class="gloss-item"><div class="gloss-name">{g.name}</div><div class="gloss-def">{g.definition}</div></div>'
        for g in spec.glossary
    )
    glossary_block = f"""  <details class="glossary">
    <summary>Words from this lesson · open if you want a quick reference</summary>
    <div class="glossary-grid">
{glossary_html}
    </div>
  </details>"""

    recap_block = f"""  <section class="recap">
    <span class="recap-badge">✓ Lesson {spec.num} complete</span>
    <p>{spec.recap_lead}</p>
    <p class="recap-next">{spec.recap_next}</p>
  </section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{spec.title_html}</title>
<style>{css}</style>
</head>
<body data-theme="light">

{rail_html}

<header class="topbar">
  <div class="topbar-inner">
    <a href="#" class="brand"><span class="brand-mark">SG</span><span>Suvis Guru</span><span class="course"> · K-COM · Lesson {spec.num}</span></a>
    <span class="progress-pill">{spec.num} · {spec.title_short}</span>
    <button class="theme-toggle" id="theme-toggle" type="button">\U0001F319 Dark</button>
  </div>
</header>

<p class="district-line">\U0001F4CD Today's stop in K-Town: <strong>{spec.district_label}</strong>.</p>

{map_html}

<main>

  <section class="hero">
    <span class="eyebrow">{spec.module_eyebrow}</span>
    <h1>{spec.title_full}</h1>
    <p class="hero-sub">{spec.hero_sub_html}</p>
    <div class="hero-illu">
{spec.hero_illu_svg}
    </div>
  </section>

  <div class="nightmare">
    <div class="nightmare-box">
      <span class="nightmare-tag">\U0001F6A8 The 3 AM Nightmare</span>
      <p>{spec.nightmare_html}</p>
    </div>
  </div>

  <div class="stamp">
    <p class="stamp-box">\U0001F3AF <strong>If you remember nothing else:</strong> {spec.stamp_html}</p>
  </div>

{sections_block}

{ba_block}

{analogy_block}

{eli_block}

{scenarios_block}

{anim_section}

{misc_quiz_block}

{glossary_block}

  <div class="stamp">
    <p class="stamp-box">\U0001F3AF <strong>If you remember nothing else:</strong> {spec.stamp_html}</p>
  </div>

{recap_block}

</main>

<footer>Suvis Guru · K-COM · Lesson {spec.num} of {TOTAL_LESSONS_IN_CURRICULUM} · grounded in kubernetes.io</footer>

{combined_script}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def load_spec_module(path: str):
    abs_path = os.path.abspath(path)
    spec_dir = os.path.dirname(abs_path)
    if spec_dir not in sys.path:
        sys.path.insert(0, spec_dir)
    spec_name = os.path.splitext(os.path.basename(abs_path))[0]
    spec_spec = importlib.util.spec_from_file_location(spec_name, abs_path)
    mod = importlib.util.module_from_spec(spec_spec)
    spec_spec.loader.exec_module(mod)
    return mod


def _maybe_attach_animation(spec: LessonSpec, spec_path: str) -> None:
    """If a sibling animations.py exists exporting ANIMATIONS dict keyed by
    lesson num, attach the matching animation to the spec."""
    spec_dir = os.path.dirname(os.path.abspath(spec_path))
    anim_path = os.path.join(spec_dir, "animations.py")
    if not os.path.exists(anim_path):
        return
    if spec_dir not in sys.path:
        sys.path.insert(0, spec_dir)
    spec_spec = importlib.util.spec_from_file_location("animations", anim_path)
    mod = importlib.util.module_from_spec(spec_spec)
    spec_spec.loader.exec_module(mod)
    animations = getattr(mod, "ANIMATIONS", {})
    if spec.num in animations and spec.animation is None:
        spec.animation = animations[spec.num]


def _run_audits() -> int:
    """Auto-run both audits at the end of generation. Returns total issue count.

    Per CLAUDE.md "Audit runs immediately after generation": this is mandatory.
    """
    import subprocess
    failures = 0
    for script in ("audit_lessons.py", "audit_lessons_v2.py"):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script)
        result = subprocess.run([sys.executable, path], capture_output=True, text=True)
        if result.returncode != 0:
            failures += 1
            print(f"\n>>> {script} FAILED <<<")
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        else:
            # Print concise success line
            first_line = (result.stdout.splitlines() or [""])[0]
            print(f"audit: {script} ✓ ({first_line})")
    return failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("specs", nargs="+", help="Python files defining LESSON = LessonSpec(...)")
    parser.add_argument("--out", default=ROOT, help="Output directory (default: repo root)")
    parser.add_argument("--no-audit", action="store_true", help="Skip post-generation audits (NOT recommended; see CLAUDE.md).")
    args = parser.parse_args()

    for spec_path in args.specs:
        mod = load_spec_module(spec_path)
        if not hasattr(mod, "LESSON"):
            sys.exit(f"{spec_path}: missing top-level LESSON = LessonSpec(...)")
        spec: LessonSpec = mod.LESSON
        _maybe_attach_animation(spec, spec_path)
        html = render_lesson(spec)
        out_path = os.path.join(args.out, f"preview-kubernetes-lesson-{spec.num}.html")
        with open(out_path, "w") as f:
            f.write(html)
        print(f"wrote {out_path}")

    if args.no_audit:
        print("\n[--no-audit] skipped post-generation audits.")
        return
    print()
    failures = _run_audits()
    if failures:
        print(f"\n{failures} audit(s) reported issues — fix before committing.")
        sys.exit(2)


if __name__ == "__main__":
    main()
