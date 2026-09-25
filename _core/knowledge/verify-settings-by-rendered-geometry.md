---
name: verify-settings-by-rendered-geometry
description: "Prove a setting works by diffing the rendered page, not by reading the token or attribute it writes"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-05T20:11:23.268Z
---

A setting is only "working" if flipping it changes the **rendered page**. Checking
that the token or `data-` attribute changed proves nothing — Bam has caught this
twice ("these setting are doing nothing" while every attribute was landing
correctly).

**Why:** in the Therum admin, several settings wrote a correct attribute onto
`#th-shell` and still did nothing, for reasons no token check can see:
- the CSS targeted a class no component renders (`.th-grid`, `.th-save-hint`,
  `.th-sb-fold`, `.th-code`, `.th-grip`)
- two settings declared the same property at equal specificity, so the one later
  in the file always won (`bgImage` vs `background`; `cardGridGap` vs `bentoGap`)
- an inline style beat the stylesheet entirely (`cardImage` vs ContentCard's
  inline gradient)
- a **self-referential custom property** (`--th-accent: color-mix(..., var(--th-accent) ...)`)
  made the property invalid-at-computed-value-time, i.e. empty, silently killing
  every `color-mix()` built on it

**How to apply:** drive real Chrome over CDP, snapshot a wide computed-style +
geometry fingerprint of every element under the shell, flip the value, diff.
Empty diff = dead. Five traps that produce false verdicts:
- probing one page — cards, code fields and grids live on different routes
- injecting `transition:none` to stabilise measurement, which hides every motion
  setting
- headless has no window focus, so `:focus` never matches and `.focus()` looks
  broken; use `Emulation.setFocusEmulationEnabled`, and dispatch a real
  `Input.dispatchMouseEvent` when the rule is about mouse focus vs `:focus-visible`
- **measuring the wrapper instead of the element that renders.** Verifying the
  sidemoney.co hero mark I measured the flex wrapper, got `centre=696` against a
  container centre of 696, and reported the logo centred — while the `<img>`
  inside was 8px wide (from 78px, crushed by a `max-width:100%` chain) and sat
  near one edge. Measure the `<img>`, the text node, the button.
- **sampling mid-load.** The ported sheet is ~742KB and lands well after `load`;
  three consecutive readings were each internally consistent and all three wrong.
  Poll until the rect repeats before trusting it.

Finish with a click-through of the actual control that reloads the page between
states, which also proves it persisted — and by LOOKING at a screenshot cropped
to the element's own rect, not a guessed y offset. See [[headless-verify-harness]]
and [[bam-working-style]].
