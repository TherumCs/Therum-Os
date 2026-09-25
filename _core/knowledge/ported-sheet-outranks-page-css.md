---
name: ported-sheet-outranks-page-css
description: "The ported stylesheet loads after page CSS and carries .th-page-<id> rules, so two-class overrides silently lose"
metadata: 
  node_type: memory
  type: project
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-05T17:37:13.185Z
---

On sidemoney.co the ported stylesheet (`/api/uploads/sidemoney-port-v2.css`,
~742KB) loads AFTER a page's inline `meta.css`. It carries rules like
`.th-page-165012 .th-el.th-el-479c7f3 { width:var(--container-widget-width,12%) }`
at specificity 0,3,0. A page rule written as `.th-el-parent .th-el-child` is
0,2,0 and loses; at an exact tie the later sheet wins on order alone. Overrides
need four classes, and the same trap already bit the contact form
(`.h-input` at 0,1,1 beating `.cf__f input`).

Two layout traps that come with those ported elements:
- Their widths are often PERCENTAGES. Add `min-width:0` to such an element as a
  grid item and the track collapses to zero — track 0 wide, percentage of 0 is
  0, track stays 0 — and the element vanishes while still present in the DOM.
- Their intrinsic sizes are large (one symbol wrapper was 500px), so an
  unconstrained `1fr` track blows past the viewport on mobile.

**Why:** every wrong verdict here looked like a working rule — the declaration
was present in the page CSS and simply never applied.

**How to apply:** don't reason about which rule wins. Read it with CDP
`CSS.getMatchedStylesForNode`, which lists matched rules in cascade order with
their media conditions and `!important` flags. See
[[verify-settings-by-rendered-geometry]] and [[headless-verify-harness]].
