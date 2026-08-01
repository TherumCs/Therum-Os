# Prod-readiness audit — Therum OS 2.0.0-beta.3

> **STATUS: all findings below are CLOSED.** Fixes and their verification are
> recorded in `AUDIT-beta.3-CLOSED.md`. This file is kept as the record of what
> was found.

Run 2026-07-29, against the tagged `v2.0.0-beta.3` tree, on localhost:10009.
Every finding below was reproduced, not inferred. Where a first reading turned
out to be wrong, the correction is noted rather than quietly dropped.

## Gates (all green)

| Gate | Result |
|---|---|
| Server typecheck | clean |
| Admin typecheck | clean |
| Server build | clean |
| Admin production build | clean, all routes compiled |
| Test suite | 260 pass, 0 fail |
| System health preflight | db, redis, JWT secret, credential key, CORS, webhook secret all OK; only warn is "development mode" |

## What is already right

Worth stating, because it narrows what still needs doing.

- **Env is parse-or-die.** `src/lib/env.ts` validates with zod and calls
  `process.exit(1)` on a bad environment. `JWT_SECRET` min 32, `CREDENTIAL_KEY`
  separate from it so signing keys stay cheap to rotate.
- **Admin session cookie is correct**: `httpOnly`, `secure` in production,
  `sameSite: lax`, 12h expiry.
- **Webhooks reject unsigned requests** — `POST /webhooks/psp/:provider` and
  `POST /webhooks/:provider` both 401 without a signature.
- **Uploads are served by `@fastify/static`**, so path traversal is handled by
  the library rather than hand-rolled string work.
- **The public catalog does not leak.** `GET /products` returns active products
  only, with no cost, margin, or supplier fields.
- **Customer auth is properly throttled** — and this corrects my own first
  reading. The limits live in `src/counter/customerAuth.ts`, not in the route
  files: `customer-login:{email}` 10/15min, `customer-code:{destination}`
  5/15min, and `MAX_CODE_ATTEMPTS = 5` on code verification.
- **No mobile overflow.** Nine key pages at 390px: `scrollWidth == clientWidth`
  on every one.
- **No console or network errors** on `/`, `/shop`, `/product/:slug`,
  `/order-tracking` after the font fixes in this release.

## Back end findings

### H-1 · `POST /customers` takes an unauthenticated write

`src/api/routes/customers.ts:20`. `GET /customers` and `GET /customers/:id` in
the same file both carry `{ preHandler: app.authenticate }`. `POST` carries
nothing, and the file-level hook is only `requireCapability('commerce')`, which
gates the feature, not the caller.

Reproduced: `POST /api/customers` with no token and `{"email":"..."}` returned
**201** and created a row. (Row deleted after the test.)

Anyone on the internet can write to the customers table: unbounded row
creation, and it sidesteps the verified-email rule the storefront signup path
enforces. Nothing on the front end needs this route public — the storefront
registers through `POST /shop/account/register`, which is separately throttled.

**Fix:** add `{ preHandler: app.authenticate }`.

### H-2 · `GET /media` and `GET /media/:id` are unauthenticated

`src/api/routes/media.ts:14,18`. Every mutation in that file is authenticated;
these two reads are not, and the file-level hook is only
`requireCapability('content')`.

Reproduced: `GET /api/media?limit=2` with no token returned **200** with each
item's upload URL, original filename, dimensions, byte size and upload date.

On a live domain the entire asset library becomes enumerable by anyone,
including files uploaded but not yet used on a published page.

**Fix:** add `{ preHandler: app.authenticate }` to both.

### M-1 · Four public writes have no rate limit

The complete limit map is six keys: `contact` 5/15min, `track` 12/10min,
`cart-new` 30/hr, `cart-coupon` 20/10min, `customer-login` 10/15min,
`customer-code` 5/15min. Not covered:

| Route | Exposure |
|---|---|
| `POST /orders` | Public by design ("protected by idempotency + the inventory guard, not auth"). Unlimited order creation. |
| `POST /shop/products/:productId/reviews` | No auth, no limit, **and no proof of purchase**. Review spam. |
| `POST /public/register/:regSlug` | Unlimited Milieu registrations. |
| `POST /shop/account/register` | Account-creation spam (login and code paths are limited; register is not). |

### M-2 · Customer login is throttled per email, not per IP

`customer-login:${email}` is the right key for defending one account, but one
IP can spray thousands of different addresses without ever hitting a limit. Add
an IP-keyed limiter alongside the email one.

### M-3 · The admin knock cookie has no `Secure` flag

`src/api/adminProxy.ts:117` sets
`HttpOnly; SameSite=Lax; Max-Age=31536000` with no `Secure`. On a real domain it
will ride a plaintext request. It is a year-long cookie that suppresses the
stealth 404, so it is worth protecting.

### M-4 · There is no way to delete a customer

No `DELETE /customers/:id` route exists — verified, it 404s. Data-deletion
requests currently have no path through the API.

### L-1 · Deployment config will silently misfire off localhost

- `admin/app/api/auth/login/route.ts:4` — `API_URL` defaults to
  `http://localhost:4100`. If unset in production, admin login returns 502.
- `src/lib/env.ts` — `PORT` defaults to 4100 while the server actually runs on
  10009, and `.env.example` still ships `PORT=4100`.
- `CORS_ORIGINS` defaults to three localhost origins. The preflight only
  *warns* when production has localhost-only origins; nothing fails.
- `CREDENTIAL_KEY` is optional, falling back to a JWT_SECRET derivation. Fine
  today (it is set), but in production it should be required, so that rotating
  the signing key can never orphan stored payment credentials.

## Front end findings

Thirty pages crawled from `/`, following internal links.

### H-3 · Fourteen broken internal links

**Your main navigation is four dead links:**
`/c/mens`, `/c/womens`, `/c/kids-playmoney`, `/c/home-house-money`
— plus `/c/mens/accessories`. The `/c/:slug` route works; the categories do not
exist (only `apparel` and `basics` do).

**Stale links carried over from the WP port:**
`/shop/sevn-fold-snapback`, `/shop/soul-sold-out-tee-2`,
`/the-city-series-exclusively-at-footlocker`, `/category/news`, `/147857-2`,
`/welcome-back`, `/collections_post`, `/about-us`, `/product`

### H-4 · Raw shortcodes render as visible text

| Shortcode | Where |
|---|---|
| `[contact-form-7 id="970" title="Subscribe"]` | Footer — so, ~14 pages |
| `[vc_column width="1/1"…]` | Homepage |
| `[insert contact email or address]` | Cookie policy |

The last one is a legal page instructing the visitor to insert an email address.

### M-5 · Commerce pages have no meta description, canonical, or `og:` tags

`/shop`, `/cart`, `/checkout`, `/wishlist`, `/order-tracking`,
`/product/starter-tee`, `/product/starter-pant`.

Product pages with no `og:` tags share as a bare URL with no image or price,
which for a store is money. The ported document pages *do* have these — the gap
is specifically the pages this project generates.

### M-6 · Heading structure

- **Zero `h1`** on `/`, `/faq`, `/accessibility-statement`, `/cookie-policy`,
  `/privacy-statement`, `/terms-and-conditions`, `/refund_returns`.
- **Two `h1`** on `/order-tracking` — mine. The intro title and the result
  headline are both `h1`; only one is ever visible, but both are in the DOM.

## Suggested order

1. **H-1, H-2** — two `preHandler` additions. Minutes, and they are the only
   findings that expose data or writes to the internet.
2. **H-3, H-4** — the dead nav links and the visible shortcodes are what a
   visitor sees first.
3. **M-1, M-2** — rate limits before the domain goes live.
4. **M-5, M-6** — SEO and headings.
5. **M-3, M-4, L-1** — cookie flag, deletion route, deploy config.
