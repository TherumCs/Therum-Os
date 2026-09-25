---
name: store-attribution-and-feed
description: "New commerce surfaces on the live store — attribution capture, dashboard activity panel, and the Meta/Instagram product feed URL"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4504c37-caac-4f64-affa-6039105bec50
  modified: 2026-08-18T23:29:30.675Z
---

Built 2026-08-18 in therum-cms-2 (the live store), all deployed + verified on sidemoney.co.

**Attribution (first-touch):** the base layout stamps a `th_src` cookie on landing from `utm_source`/`ref`, else the external referrer host (30-day, first-touch, never overwritten). `cart.ts sourceFrom()` reads it server-side at `/cart/items` → `cartService.addItem(...,source)` stores it first-touch on the cart → checkout passes it to `order.create` → written to `order.meta.source`. To confirm Instagram traffic works, land with `?utm_source=instagram`.

**Dashboard "Store activity" card** (admin `(app)/page.tsx`) reads `GET /api/counter/activity` (`dashboardService.activity()`): orders by status, revenue 30d, attempted-but-unfinished (pending+failed), live abandoned carts (count + priced value from Redis), launch-list count (EmailSignup), and top order sources. This is the read side for cart/signup data that was previously written and never surfaced.

**Meta/Instagram product feed = `https://sidemoney.co/feed/facebook.xml`** (also `/feed/products.xml`) — RSS 2.0 + g: namespace, one `<item>` per sellable VARIANT grouped by `g:item_group_id`. Point Meta Commerce Manager / Google Merchant here (Bam's stated next step: Instagram shopping, the "CTX Feed"). Fixed the variant-sync bugs he hit: real per-variant availability (was hardcoded "in stock"), `public`-visibility only (private/restricted like the bespoke no longer leak), per-variant `additional_image_link`, and `g:mpn`=SKU.

Margin-floor discount enforcement now shared between cart display and `order.create` via [[live-store-real-money]] `src/counter/marginFloor.ts` — the order charges exactly the clamped figure the cart showed (was display-only, undercharged below floor).

**2026-09-20 — Instagram product tagging errored; cause was the feed.** The 5 Foot Locker exclusives (`meta.externalUrl`, PDP 302s to footlocker.com since 2026-09-16) were still in `/feed/facebook.xml`; Meta follows each `g:link`, lands off-domain, rejects the item, and a rejected item cannot be tagged. Fixed in `feedHandler` (storefront.ts): products with `externalUrl` are excluded → 795 items / 70 products, every link 200 on-domain. Meta fetches the feed daily at 04:00 UTC (nginx shows 200s on the 18th/19th/20th); Bam can force it via Commerce Manager › Catalog › Data Sources › Request update. Not a size problem: the 67KB→47KB drop on the 19th was gzip→brotli once Cloudflare came on. Also verified as Meta's crawler: images 200, `facebook-domain-verification` tag present, og tags on PDPs. **Lesson: when a product's PDP starts redirecting off-site, walk every surface that publishes its URL — feed, sitemap, emails — not just the page.** The Sixers pin duplicates carry `copy-of-copy-of-…` slugs in the feed; left alone per "leave the dups, I'll handle it".
