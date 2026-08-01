# Audit closure — Therum OS 2.0.0-beta.3

Every finding from `AUDIT-beta.3.md`, what was changed, and how it was proven.
Nothing here is "should work" — each line was re-run against the server.

## Back end

| Finding | Fix | Proof |
|---|---|---|
| **H-1** `POST /customers` unauthenticated | Added `{ preHandler: app.authenticate }` | 401 without a token; 201 with one. Regression test added. |
| **H-2** `GET /media`, `GET /media/:id` unauthenticated | Same | Both 401 anonymously, 200 authenticated. The FILES under `/api/uploads` stay public — storefront images need them. |
| **M-1** four public writes unthrottled | `order-create` 10/10min, `review-submit` 5/hr, `milieu-register` 10/15min, `customer-register` 5/15min | Limit map went from 6 keys to 11. |
| **M-2** login throttled per email only | Added `customer-login-ip` 30/15min beside it | One host can no longer spray one password across thousands of addresses without ever tripping a limit. |
| **M-3** knock cookie had no `Secure` | `Secure` when `NODE_ENV=production` | Off in dev because localhost is http. |
| **M-4** no way to delete a customer | `DELETE /customers/:id` → `customerService.erase` | ERASE, not delete: addresses, social identities, sessions and pushed offers go; email becomes a unique tombstone; **orders stay**, because those rows are accounting. |
| **L-1** deploy config could silently misfire | Production gate in `src/lib/env.ts` | Verified both ways: with dev placeholders it prints the three problems and exits 1; with real values it boots. Development untouched. |

## Front end

| Finding | Fix | Proof |
|---|---|---|
| **H-3** 4 dead nav links + 10 stale | Created the real categories (Mens, Womens, Kids / Playmoney, Home / House Money, and Accessories under Mens); added a **nested** `/c/:parent/:slug` route; retargeted 24 ported links | Crawl of 22 pages: **zero broken links**. `/c/womens/accessories` correctly 404s — the parent is verified, so two URLs cannot serve the same page. |
| **H-4** raw shortcodes on ~14 pages | Footer CF7 node dropped; the homepage's Visual Composer tags **unwrapped, keeping the copy**; cookie-policy placeholder replaced with a real mailto | Zero shortcodes site-wide. Homepage copy intact ("The City Series, Exclusively at Footlocker."). |
| **M-5** no description / canonical / og: on commerce pages | `SeoMeta` added to the storefront layout and threaded per page; listing head added for `/blog` and `/work` | Every indexable page now has all three. `og:url` and `og:image` absolute; PDPs carry `og:type=product` and `product:price`. |
| **M-6** heading structure | Visually-hidden `h1` where a ported layout genuinely has none; order-tracking's result headline demoted to `h2` | Every page has **exactly one** h1. The hidden one measures 1×1, clipped, and adds no horizontal scroll. |

## Found during the closing pass, not in the original audit

- **A test fixture was live on the shop.** "carttest Tee" by "carttest Vendor"
  was `active` in the catalog, with 4 duplicate vendor rows and one $25 pending
  order. Cause was mine: `cart.test.mjs` cleans up in `after()`, and I had
  killed two test runs mid-flight so `after()` never ran. Product, vendors,
  milieu and the fixture order removed; catalog is back to the two real products.
- **A test artifact was publicly reachable.** `/sidemoney-bricks-import-e2e`
  returned 200. It holds real case-study content, so it is set to `draft`
  rather than deleted — **publish it under a proper slug if you want it live.**
- **Leftover chatbot text on a legal page.** The cookie policy ended with
  "Want me to adjust the tone, add/remove any sections, or prep this for
  dropping into WordPress?" — removed. A sweep of all 16 content records for
  chatter, placeholders, lorem ipsum and TODO markers now comes back clean.
  (One hit remains and is deliberately left: "feel free to reach out to our
  Customer Service team" in the terms is real policy prose.)

## Verified clean

- Crawl, 22 pages: no broken links, no shortcodes, no chatter, one h1 each,
  SEO complete on every indexable page.
- Console + network across 8 pages: zero errors, zero failed requests.
- Images: 0 broken out of 23 on the homepage, 0 broken across 15 pages.
- Mobile at 390px: no horizontal overflow on 12 pages.
- `noindex` where it belongs: `/cart`, `/checkout`, `/wishlist`, `/my-account`,
  receipts, and themed 404s.

## Still open, deliberately

- **The four new categories have no products.** They resolve and render, but
  show "No products". Assigning products is yours to do — the two existing ones
  are both Apparel.
- Four contact topics (Modelling, Press, Partnerships, Careers) still fall back
  to `info@`.
- ~~`admin/app/globals.css` has 45 more `}` than `{`.~~ **CORRECTION: this was
  wrong.** The file is balanced — 697 `{` and 697 `}`, including at the line I
  cited. I repeated the claim from earlier context without checking it. The save
  bar was still made independent of the stylesheet, which stands on its own
  merits, but the real reason its `.th-savebar` rules never applied is still
  unidentified.
- `estimatedDelivery` is never populated — needs a shipping provider.
- "Read The Manifesto" on the About page now points at the About page itself.
  If a real Manifesto page is written, that is the one link to repoint.
