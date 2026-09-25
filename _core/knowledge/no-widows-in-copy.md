---
name: no-widows-in-copy
description: Never leave a widow in copy — bind the last words of every line so none wraps alone
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f4504c37-caac-4f64-affa-6039105bec50
  modified: 2026-08-18T18:22:35.885Z
---

Bam's rule (2026-08-18), stated flatly: **"never no widows in copy."** A widow = a single word left alone on the last line of a paragraph or heading. Applies to ALL copy I produce for him — emails, pages, artifacts, product text.

**Why:** he is exacting about typography; a dangling last word reads as unpolished and cheapens the whole piece.

**How to apply:** bind the last two words of each line with a real non-breaking space (U+00A0) so a single word can never wrap alone — the email-safe technique (email clients ignore CSS `text-wrap:pretty`). The email kit (`scratchpad/email-kit.cjs`, to be ported into `therum-cms-2/src/services/emailTemplate.ts`) has a helper: `nw(html)` splits on `<br>` and replaces each segment's final space with an nbsp; it wraps every heading/eyebrow/paragraph. For web/artifacts, `text-wrap: balance` on headings + the nbsp guard on critical lines. See [[bam-working-style]] — he catches small visual flaws and calls them out.
