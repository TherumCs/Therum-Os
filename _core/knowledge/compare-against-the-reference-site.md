---
name: compare-against-the-reference-site
description: "localhost:10025 is the visual spec for sidemoney.co — if it does not look like :10025 it is wrong, and Bam saying it is wrong settles it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-03T17:45:12.025Z
---

`http://localhost:10025` is the original Elementor-built TSC site and is the
**visual bar** for sidemoney.co. Bam's rule, verbatim: *"If it don't look like
:10025, it's wrong."* And: *"If I tell you it's wrong, it's wrong. Don't fight me
on it. Don't go back on it."*

**How to apply:**
- Never answer "it's wrong" with "let me compare" or "you're right, let me look
  again." It is wrong. Go fix it.
- Never present a screenshot as evidence of done. Measure. `tools/visual-compare.mjs`
  loads our page and the reference in the same browser at the same viewport and
  reports overflow, collapsed containers, per-section height deltas and total page
  height. Run it at 1440 / 768 / 390.
- Match sections by **Elementor element id**, not by DOM position — position
  matching turns one ordering difference into a cascade of fake "wrong height"
  findings.
- Pick the comparison root carefully: the reference wraps its footer in
  `.elementor-505` too, so `querySelector('.elementor')` grabs the footer on any
  page without its own Elementor design, and you end up diffing our page body
  against their footer.
- Total page height must be its own pass criterion. A page whose sections happen
  to match can still be missing most of its content — the blog read "pass" at
  1133px against a 3141px reference.

**Why it kept going wrong:** nothing in the repo checked layout, so every "done"
rested on me looking at a screenshot, and the screenshot method was itself broken
(see [[headless-verify-harness]]). Bam's eyes were the only detector, and he
caught the same class of miss over and over. Related: [[elementor-port-contract]],
[[bam-working-style]].
