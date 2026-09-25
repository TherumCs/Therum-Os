---
name: the-port-law
description: "THE LAW for sidemoney.co — :10025 is truth, the target platform is Bricks on Therum OS, nothing is invented, and Elementor is banned"
metadata: 
  node_type: memory
  type: project
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-03T20:17:30.092Z
---

> **STATUS 2026-09-19 — read this first.** What SHIPPED on 2026-08-14 is a custom Therum OS 2.0 app (Fastify + Prisma, PM2 on the VPS) serving ported `c-ip-*` markup — **not Bricks**. Bricks was the original plan and `tsc-beta` (:10020) is its leftover design surface. The part of this law that still binds: :10025 remains the visual reference and nothing is invented. The part that does not: "target is Bricks". Verified from the box (`_core/memory.md` ⭐ section).

**sidemoney.co is a NEW PLATFORM (Therum OS). `http://localhost:10025` is the
existing site and it is TRUTH.** Everything — theme, layout, CSS, visuals, down
to the pixel — is being PORTED onto the new platform. Not redesigned, not
approximated, not reinterpreted.

## The four rules, in Bam's words

1. **"Nothing to invent or assume or make up."** If it is not on :10025 or in
   the folder, it does not get created. No invented class names, widget types,
   file paths, or designs. Can't verify it? Say so.
2. **"NOTHING ELEMENTOR."** The target platform is **Bricks**. Everything must
   be Bricks or Bricks elements.
3. **"Rewrite the CSS for Bricks so it's styled exactly like :10025."** The
   reference is the VISUAL spec, not the class vocabulary. Match how it looks
   using Bricks classes — do not import Elementor's stylesheet or its class
   contract.
4. **Templated once.** Header, footer and pages are designed and styled once and
   reused. Counter needs default templates the way Woo ships them
   (shop / PDP / cart / checkout / account).

And: **continued fixes must not break layouts, pages, or CSS.** A rule with no
check behind it is a wish — see `test/rendered-markup.test.mjs`.

## What I did wrong, so it is never repeated

Told "Bricks" throughout, I ported ELEMENTOR instead: extracted 904KB of the
reference's Elementor stylesheet, generated a 546-entry element-id → Elementor
class map (`src/site/portedElementClasses.ts`), and made the renderer emit
`e-con` / `elementor-widget-*` so that stylesheet would match. It got pixels
close and made the site depend on Elementor's class contract — the opposite of
the instruction, and the reason every visual fix had a wide blast radius.

That work has to be undone: the Elementor stylesheet, the class map, and the
`elementor-*` emission in `src/lib/render.ts` and `src/site/siteHtml.ts`.

## How to work here

- Reference every fact to :10025 or the folder. Pull it live, cite it.
- Verify by MEASUREMENT (`tools/visual-compare.mjs`, `tools/element-audit.mjs`)
  at 1440 / 768 / 390. Never by looking at a screenshot.
- **Confirm the full list every response**: what is done, what is not, and
  whether it is actually fixed. Bam requires this explicitly.
- One ask = one change. Log other issues, do not fix them unasked.

Related: [[compare-against-the-reference-site]], [[bam-working-style]],
[[elementor-port-contract]] (that file documents the WRONG approach — kept only
as the record of what to rip out), [[headless-verify-harness]].
