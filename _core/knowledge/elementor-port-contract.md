---
name: elementor-port-contract
description: "An Elementor-ported page needs three things in its markup or its whole stylesheet matches nothing — scope wrapper, full element name, and the e-con class"
metadata: 
  node_type: memory
  type: project
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-03T17:44:59.247Z
---
> **REJECTED APPROACH.** Bam's instruction was Bricks throughout and NO
> Elementor. This file documents the Elementor port that was built against
> that instruction; it is kept only as the record of what has to be removed.
> The governing rule is [[the-port-law]].

TSC's pages came from Elementor. Elementor's generated CSS only applies when
**all three** of these are true in the markup. Miss any one and every rule for
that page silently matches nothing, and the page falls through to whatever
generic container defaults exist — which reads as "narrow and unstyled," not as
"missing CSS."

```
.elementor-165012 .elementor-element.elementor-element-a7707ab { --min-height: 80vh }
^ 1. scope wrapper              ^ 2. full element name          ^ 3. only a custom property
```

1. **Scope wrapper** — `<div class="elementor elementor-<wp post id>">` around the
   page body. Stored per page in `content.meta.elementorScope`, applied in
   `sitePage()`, re-validated against `/^elementor-\d+$/` at both ends because it
   lands in a class attribute.
2. **Full element name** — our WP import shortened `elementor-element-<id>` to
   `el-<id>`. `expandElementorIds()` in `src/lib/render.ts` re-emits both.
3. **`e-con` on containers / `elementor-widget-<type>` on widgets** — the
   per-element rules set only CUSTOM PROPERTIES, and `.e-con { display:
   var(--display); min-height: var(--min-height) }` is the only thing that reads
   them. Without it a section declaring `--min-height:100vh` renders at content
   height (242px instead of 900px).

**The trap in step 3:** `--display` is defined only by a page's own generated
stylesheet. A var that resolves to nothing computes as `unset`, and **an unset div
is inline** — adding `e-con` to pages without a stylesheet turned 226 About-page
containers inline. Declare the default at zero specificity,
`:where(.e-con){--display:block}`, so a page that HAS its rules still wins and a
page without renders as before. Not scoped to `#brx-content`: the ported header
and footer carry these containers too.

Also: `.elementor-505` is the shared FOOTER scope, present on every reference
page — do not mistake it for the page's own scope. Related:
[[compare-against-the-reference-site]], [[headless-verify-harness]].
