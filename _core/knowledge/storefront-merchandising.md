---
name: storefront-merchandising
description: "sidemoney.co storefront internals — cluster primary trap, variant-image swatch binding, size order, front-end pager gating"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1eb82035-25c8-45fb-83e3-63b52d3072eb
  modified: 2026-08-12T23:45:05.173Z
---

therum-cms-2 storefront (`src/api/routes/storefront.ts`, `src/site/productGrid.ts`, `src/site/categoryTemplates.ts`) merchandising behaviors that are NOT obvious from a quick read and each cost real time on 2026-08-12:

**Clusters (`cluster.service.ts`).** A cluster shows as ONE card (the primary) carrying every member's colorways as swatches; non-primary members DROP from the grid. Primary resolution = explicit `clusterGroup.primaryProductId` override if still a member, ELSE **earliest-created member**. Trap that broke the Bird Season hats: with no explicit override the primary defaulted to woo44 — an older *draft* Printify hat not in the category — so the primary never rendered and all members vanished. ALWAYS `clusterService.setPrimary(gid, realProductId)`. Build via `clusterService.create({name, productIds})` then `setPrimary`. Two same-color members (both "Black") collapse to one swatch — give each a distinct color name + `variant.colorCodes` (2 hex = 135° hard-split swatch, e.g. `Black/White`=[#111111,#ffffff]). A color name with "/" also auto-splits via colourToHex.

**Variant color images.** `ProductVariant.image` is NULL by default; the PDP/card swatch swap reads `v.image` (storefront lines ~615/1031/1397). Tapstitch AND Printful push a product gallery but NOT per-variant images, so swatches show nothing until bound. Images arrive as operator zips of sequential `-mockups-N.png` (no color in the name): first block = 1400×1400 square flats (front/back pairs per color), later block = 2048×2731 lifestyle (skip via `sharp().metadata()`, `w!==h`). Bind by building a labeled contact sheet (sharp montage of the front-of-each-pair), READ it to name each color, map color→`urls[2*pairIndex]`, then a proof montage of the bound files labeled by DB color. Uploads live at `~/therum/therum/uploads` on the box.

**Size order.** `sortSizes()` / `sizeRank()` exported from `productGrid.ts` (S,M,L,XL,2XL… then numeric, One Size last). Applied to the card sizes, PDP sizes, and toolbar size facet in storefront.ts. Plain `.sort()` gave L,M,S,XL — that was the bug.

**Front-end pager.** Numbered `‹ 1 2 ›` pager exists; only renders when `pageCount > 1`, i.e. `collapsed.length > toolbarPageSize`. It was invisible because `counter.toolbarPageSize` (setting key `counter`, JSON blob) was 48 while the catalog was 38 → one page. Set to 24. Collection (T2) template pages had NO pager code at all until added to the `isCollection` branch of `bodyMarkup`.

See [[fulfillment-routing]], [[pull-images-from-10025-mysql]], [[live-store-real-money]].

**Restricted (invite-only) product drop — recipe, 2026-09-20 (Bird Season Kelly Green Limited Edition Snapback).** Bam: "hidden from all, sent only to my test account + Fresco." Visibility `restricted` + `ProductAccess` rows for named customers (`bam@beta.sidemoney.co` is his test account) = absent from /shop, search, sitemap and the Meta feed; PDP 404s; `POST /api/cart/items` refuses the variant — verified from outside. A Printful/Printify product arrives from the hourly `:00` sync as `active public`, so lock it at creation: an on-box poller (`/tmp/autolock.mjs`, 3s loop) flipped it 16ms after it appeared. The sync never writes `visibility`, so later syncs cannot un-hide it. `restrict.mjs` (scratchpad `restrict/`, staged at `/tmp/restrict.mjs` on the box) does grants + one email per account; per-person copy lives in its `NOTES` map. Bam's wording for these: "the kelly green limited is now available in your account. sign in to purchase." Open: Printful billing card expired (memory) — a purchase will not fulfil until fixed.
