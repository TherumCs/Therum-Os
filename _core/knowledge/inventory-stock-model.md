---
name: inventory-stock-model
description: "how storefront stock works — tracked vs in_stock, the \"Only N left\" nudge threshold, which products are a limited run vs POD-infinite"
metadata: 
  node_type: memory
  type: project
  originSessionId: e745e2aa-9578-48ef-9843-d125d121f24c
  modified: 2026-09-03T15:36:32.368Z
---

sidemoney stock lives in `src/counter/availability.ts`. `stockStatus` values: **tracked** (real count, `availableOf = inventory - reserved`, blocks oversell, decrements on paid), **in_stock** (POD / made-to-order → `UNLIMITED` = 1e9, never runs out), **out_of_stock** (0), **backorder**. `stockLabel` is the ONLY customer-facing stock text: "Sold out" at 0, **"Only N left" when tracked AND available ≤ 3** — Bam's low-stock nudge. Exact levels are NEVER shown otherwise (just "In stock"). Threshold is 3 (lowered from 5 so a 6-per-size run doesn't flash "Only 5 left" after one sale). Decrement path: `order.service.ts` reserves on order create (`reserved += qty`, refuses if `inventory - reserved < qty` for tracked) and on `markPaid` does `inventory -= qty` for tracked only.

Which is which: **Sixers jerseys** ('96/'01/'04/'25/'27 = ixers-season-jersey-{red,black,split-76,blue,white}) are **tracked, 6 per size** — a limited PREORDER run (meta.preorder, ships after Oct) with a 1-jersey-per-order cap (meta.limitGroup 'sixers-jersey'). **Bird Season practice jerseys** (bird-season-practice-jersey-{kelly-green,midnight-green,darkmode,snowflare}) are tracked with small hand-kept counts. Everything POD (tees, hoodie, mesh shorts, joggers, Proof of Purchase, money balls) stays **in_stock** (infinite). Bam reconciles physical stock by hand — e.g. "1 left = sold out" → set that variant to `inventory:0, stockStatus:'out_of_stock'`.

**Pre-order pill** (2026-09) is DATA-DRIVEN off `meta.preorder === true` + `meta.preorderShipAfter` (the 5 Sixers jerseys only; Bird jerseys are in-stock/ship-fast so they get nothing). Rendered three places, all keyed off that flag: product CARD (red pill top-right of the image — `card-badge--preorder`, `margin-left:auto`, built in the storefront gridProducts mapper as `preorderLabel`; text "PRE-ORDER · SHIPS OCT 10"); PDP (`pdp-preorder` pill under the title, "Pre-order now · Ships October 10th"); homepage MARQUEE (`injectMarqueePreorder` in site.ts post-processes the ported `.c-ip-running-line` — "Sixers Season jerseys — pre-order now, ships October 10th", AUTO-EXPIRES on 2026-10-10 via a date gate so it never goes stale). Date formatted once by `fmtPreorder()` in storefront.ts ({short:"Oct 10", long:"October 10th"}). Bam's rule: "ships Oct 10" not a bare date — say what the date MEANS. See [[live-store-real-money]] [[sidemoney-storefront-render]] [[sidemoney-blog-system]].
