---
name: signal-meta-pixel
description: Signal = Therum OS Studio app for Meta Pixel + Conversions API (built 2026-09-22) — how it's wired, what's left to turn it on, and the ad plan it serves
metadata:
  type: project
---

**Why it exists.** Bam shared a Meta ads plan (2026-09-22): Advantage+ broad targeting where "creative is the targeting", 10–15 distinct vertical concepts, $20–30/day sales + $10/day follower campaign, judge by store revenue ÷ ad spend, launch early October ahead of the Sixers drop and Gather vending **Oct 31**. The plan's step 1 assumed WooCommerce's Meta plugin — **sidemoney.co had no Pixel and no Conversions API at all**, so ads would have optimised blind. Bam: "ok lets do it" → Signal.

**How it works** (commit `d784d89`, product repo, brand-clean):
- `src/site/signalRuntime.ts` in both shells: fetches `/api/shop/signal`; if a pixel ID is live, loads fbq → PageView; ViewContent on `/product/*` using `data-product-id` (= feed `g:item_group_id`), content_type product_group; AddToCart by wrapping `fetch` for POST `/api/cart/items` (uses `totals.lines[].unitPrice`); InitiateCheckout on `/checkout`; Purchase on order-received from a hidden `[data-signal-order]` element rendered **only for paid orders**, eventID `purchase-<number>`.
- `src/services/signal.service.ts`: settings in Setting key `signal` {enabled, pixelId, testEventCode}; token = Nexus provider **`meta-capi`**. Server Purchase from `hookBus` `onOrderPaid` (registered in server.ts AND worker.ts, fire-and-forget), same event_id → Meta dedupes. user_data SHA-256 hashed (em, ph, fn, ln, ct, st, zp, country, external_id) + fbp/fbc/IP/UA captured at `/cart/checkout` onto `order.meta.signal`. Success = `events_received >= 1` (not HTTP 200). Last 25 results kept in memory per process for the admin table.
- Admin: Studio app **Signal** at `/tos-admin/signal` (enable under "From the Studio"); proxy `admin/app/api/signal`.
- CSP: `connect.facebook.net` in script-src, `www.facebook.com` + `connect.facebook.net` in connect-src.

**State 2026-09-22: deployed, OFF.** Verified: `/api/shop/signal` → `{pixelId:null}`, runtime present on /, /shop, PDP; cart add 201 + checkout 200 unaffected; `/api/signal` 401 without auth.

**To turn on (needs Bam):** Pixel ID + Conversions API access token from Events Manager. Then: save pixel in Signal, token in Nexus › Meta Conversions API, set a Test Events code, press "Send a test event" and see it in Events Manager › Test events, browse the site and see browser events there too, **then clear the test code** (otherwise real sales report as tests). Meta wants ~a week of real traffic before campaigns launch → turn on by ~Sept 24–26 for an early-October launch.

**Planned part 2 (not built):** scoreboard — Marketing API spend per ad vs real orders → true ROAS per creative, creative board for the 10–15 concepts with "kill the bottom third at two weeks", cost per follower. Deliberately NOT building campaign creation (Ads Manager does it).

See [[store-attribution-and-feed]] [[live-store-real-money]] [[product-vs-instance]].
