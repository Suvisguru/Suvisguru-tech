# K-Town scaffolding component templates

> **Working note**, not the source of truth. The canonical implementation is
> `preview-kubernetes-lesson-01.html`. Phase 5 lessons (L02–L15 + L7.5) copy
> CSS and HTML from L01 directly. This file lists the component blocks and
> per-lesson slots so a future agent can locate and copy each one without
> re-deriving the structure.
>
> **Built in:** K-Town revision Phase 2 (commit references the phase).
> **Applied in:** L01 (live reference), then propagated lesson-by-lesson in Phase 5.

---

## CSS block

All scaffolding CSS lives in a single block at the bottom of L01's `<style>`,
just before `</style>`. It is fenced with the comment line:

```css
/* ============ LAYMAN-FIRST SCAFFOLDING (K-Town revision Phase 2) ============ */
```

Copy the entire block from that comment to `</style>` into each lesson's
`<style>`. Tokens (`--accent`, `--warm`, `--good`, `--ink-faint`, etc.) are
already defined in every lesson's `:root` block, so no token additions are
needed downstream.

The block also includes:
- `.s code` rule for inline `<code>` parity (already present in L13; needed everywhere else).
- `.visually-hidden` utility for screen-reader-only text in the K-Town strip label.
- `prefers-reduced-motion` overrides for the new transitions.

---

## HTML components — slot-by-slot, top to bottom

Use this order so each lesson reads consistently. The exact slot before/after
which each block sits is given in the L01 reference.

### 1. Concept rail (`<aside class="concept-rail">`) — outside `<main>`

Sits between `<body data-theme="light">` and `<header class="topbar">`.
Position: fixed, top:96px, left:max(16px, calc(50vw - 600px)), width:170px,
visible only at viewport ≥1240px (hidden otherwise — the K-Town dot strip
covers mobile).

For each lesson, change exactly one item from `class="concept-rail-item"` to
`class="concept-rail-item current"` and append `<span class="concept-rail-here">← you are here</span>`.
Earlier items get `class="concept-rail-item done"` plus icon `✓`. Later items
stay `class="concept-rail-item"` with icon `○`.

The 18-item list (one per lesson plus the L7.5 primer) is hard-coded per
lesson; see L01 for the full inventory.

### 2. District line (`<p class="district-line">`) — between `</header>` and `<main>`

```html
<p class="district-line">📍 Today's stop in K-Town: <strong>{District Name}</strong>.</p>
```

District names come from STYLE.md "Unified analogical universe — Kubernetes (K-Town)" and the K-Town plan §7.2.

### 3. K-Town map (`<div class="ktown-map-wrap">`) — between district line and `<main>`

Inline SVG copied verbatim from `library/primitives/kubernetes/k-town-map.svg`
(the symbol body — see L01). To activate the lesson's pin:

- For Lesson 01 (anchor): keep the existing `<g class="pin pin-anchor active" id="kt-pin01" …>`.
- For all other lessons: add the `active` class to that lesson's pin
  (e.g. `<g class="pin active" id="kt-pin02" …>` for Lesson 02). Mayor's
  Office's pin keeps `class="pin pin-anchor"` (no `active`) — it stays slate
  as the persistent city anchor. The Lesson 7.5 primer pin uses
  `class="pin pin-primer active"` when L7.5 itself is the current lesson.

The dot-strip mobile fallback (`<ol class="ktown-strip">` plus
`<p class="ktown-strip-label">`) sits inside the same `.ktown-map-wrap`.
For each lesson, the `active` class moves to that lesson's pin in the strip
(in lesson order: 01, 02, 03, 04, 05, 06, 07, 7.5, 08, 09, 10, 11, 12, 13,
14, 15 — matches the K-Town map's pin order). The visible label and the
`<span class="visually-hidden">…</span>` accessibility line both update with
the lesson's district name and "lesson N of 16" position.

### 4. Nightmare opener (`<div class="nightmare">`) — after hero `</section>`, before Section 1

```html
<div class="nightmare">
  <div class="nightmare-box">
    <span class="nightmare-tag">🚨 The 3 AM Nightmare</span>
    <p>{Nightmare scenario from K-Town plan §8.NN, 2–3 sentences ending with the lesson's one-line promise.}</p>
  </div>
</div>
```

Per-lesson Nightmare scripts: K-Town plan §8.1 through §8.15, plus L7.5 (see plan §5.9 — primer may omit Nightmare per DECISIONS).

### 5. One-sentence stamp · top placement — immediately after the Nightmare

```html
<div class="stamp">
  <p class="stamp-box">🎯 <strong>If you remember nothing else:</strong> {takeaway}.</p>
</div>
```

Per-lesson stamps: K-Town plan §8.NN. Stamp must be **identical** at top and
bottom — same wording, same emphasis. Repetition is the point.

### 6. Pause-and-check #1 — between Section 1 `</section>` and Section 2 `<section class="s">`

```html
<div class="pause-check">
  <div class="pause-check-box">
    <span class="pause-check-tag">⏸ Pause and check</span>
    <p class="pause-check-q">{Question}</p>
    <ul class="pause-check-opts">
      <li><button type="button" class="pause-check-opt" data-correct="false">a) {wrong}</button></li>
      <li><button type="button" class="pause-check-opt" data-correct="true">b) {correct}</button></li>
      <li><button type="button" class="pause-check-opt" data-correct="false">c) {wrong}</button></li>
    </ul>
    <p class="pause-check-feedback"><strong>Answer: b.</strong> {one-sentence "why" that surfaces the mental model}</p>
  </div>
</div>
```

Per-lesson questions: K-Town plan §8.NN.

### 7. Translation Legend — replaces the existing "The mapping:" block in Section 3

Replace the existing `<p>The mapping:</p>` + `<ul>…</ul>` (or whatever per-lesson
mapping list exists) with:

```html
<div class="translation-legend">
  <table>
    <thead>
      <tr><th>In the story…</th><th>…in Kubernetes</th></tr>
    </thead>
    <tbody>
      <tr><td>{jargon-free story element}</td><td>{canonical technical term per STYLE.md vocab canon}</td></tr>
      …5–10 rows total…
    </tbody>
  </table>
</div>
```

**Vocabulary canonicalization (Phase 3 fold-in):** when reformatting the
existing mapping list as a Translation Legend, make the right-column entries
canonical per STYLE.md "Vocabulary canonicalization" (e.g. "desired state"
not "the spec", "controller" not "the loop", "Pod" capitalised, "the kubelet"
not "the agent"). Preserve every existing mapping; sharpen the phrasing where
the original drifted.

### 8. Analogy-stops-here callout — inside Section 3, after the Translation Legend

```html
<p class="analogy-stops">⚠️ <em>The analogy stops here: {one-sentence cliff}.</em></p>
```

Per-lesson cliff lines: K-Town plan §8.NN. Most lessons have one; skip when
the analogy has no known cliff.

### 9. Pause-and-check #2 — between Section 4 `</section>` and Section 5 `<section class="s">`

Same shape as Pause-and-check #1.

### 10. Common Misconceptions panel — start of Section 7, before the flashcard grid

```html
<div class="misconceptions">
  <h3>Common Misconceptions</h3>
  <div class="misconceptions-grid">
    <div class="misc-card">
      <div class="misc-row misc-myth"><strong>Myth:</strong> {one-sentence myth a beginner actually believes}</div>
      <div class="misc-row misc-truth"><strong>Truth:</strong> {one-sentence dislodging truth}</div>
    </div>
    <div class="misc-card">…</div>
    <div class="misc-card">…</div>
  </div>
</div>
```

Exactly three `.misc-card` blocks per lesson. Per-lesson myths/truths: K-Town
plan §8.NN.

### 11. Section 7 intro update

Update the existing intro paragraph from "Eight flashcards…" to acknowledge
the misconceptions panel. L01 example:

```html
<p>Three common misconceptions to clear up first, eight flashcards to lock in the key terms, then three quick check questions.</p>
```

Update the eyebrow from "Section 7 · Flashcards & quiz" to
"Section 7 · Misconceptions, flashcards & quiz" for parity.

### 12. CYOA quiz item — replaces ONE of the three existing quiz cards in Section 7

Pick one of the existing scenario `quiz-card` blocks (the K-Town plan §8.NN
specifies which one to replace per lesson — usually the third). Replace with:

```html
<div class="quiz-card cyoa-quiz">
  <span class="cyoa-tag">🎬 Choose Your Own Adventure</span>
  <p class="quiz-prompt">{Story setup, 1–2 sentences}. <strong>Click to see what happens. ▼</strong></p>
  <button class="quiz-reveal" type="button">Show what happened</button>
  <div class="quiz-answer"><span class="quiz-answer-tag">{period · e.g. "six months later" / "by morning"}</span>{Reveal narrative}. <strong>Lesson:</strong> {one-sentence takeaway}.</div>
</div>
```

For lessons with an ASCII text graphic in the reveal (L12, L13 specifically),
wrap the graphic in `<pre>…</pre>` inside the `quiz-answer` block.

### 13. One-sentence stamp · bottom placement — between glossary `</details>` and recap `<section class="recap">`

Identical content to the top stamp. Repetition is the point.

```html
<div class="stamp">
  <p class="stamp-box">🎯 <strong>If you remember nothing else:</strong> {takeaway}.</p>
</div>
```

---

## JavaScript additions

Two changes inside the existing `<script>` block:

1. **Replace the existing quiz-reveal handler** with the smarter version that
   handles both "Show answer" and "Show what happened" labels via prefix
   substitution (`/^Show/` → `Hide`).

2. **Add the pause-and-check handler** below quiz-reveals. It selects all
   `.pause-check-opt` buttons, marks the clicked one `correct` or `wrong`
   based on `data-correct`, and shows the feedback paragraph.

Both blocks are visible in L01's script; copy verbatim.

---

## Per-lesson checklist (Phase 5)

For each of L02–L15 + L7.5:

1. Copy the entire scaffolding CSS block from L01 into the lesson's `<style>` (before `</style>`).
2. Add the concept rail `<aside>` after `<body>`. Update icons: `✓` for items before this lesson, `▶ + here` for this lesson, `○` for later items.
3. Add the district line `<p>` after `</header>`.
4. Inline the K-Town map SVG. Add `active` to this lesson's pin `<g>`. Update the dot-strip's `active` class and the strip label.
5. Insert the Nightmare opener after the hero `</section>`.
6. Insert the top stamp immediately below the Nightmare.
7. Insert pause-and-check #1 between Section 1 and Section 2.
8. Replace the analogy-section "The mapping:" block with the Translation Legend table. Apply vocabulary canon.
9. Insert the analogy-stops-here callout in Section 3 (skip if the lesson has no known cliff).
10. Insert pause-and-check #2 between Section 4 and Section 5.
11. Update Section 7 eyebrow + intro to acknowledge misconceptions.
12. Insert the Common Misconceptions panel before the flashcard grid.
13. Replace the third (per plan) quiz card with the CYOA item.
14. Insert the bottom stamp between glossary and recap.
15. Update the script block: replace quiz-reveal handler, add pause-check handler.
16. Sweep the full lesson for "Avoid" terms per STYLE.md vocab canon (Phase 3 fold-in).

Verify in a browser (light + dark, desktop + 360px width) before moving to the next lesson.
