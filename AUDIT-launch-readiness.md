# Launch readiness — where we are, what's next

Run 2026-07-31 against the live local stack. Everything below was measured, not
recalled: pages fetched, database queried, scan run. Where an earlier note in
`_core/memory.md` turned out to be stale, the correction is recorded rather
than quietly dropped.

> **Updated 2026-07-31, end of day — verdict changed. Read this, not the
> original verdict below.** All four blockers are closed or reclassified:
> 3 was built, 4 is deferred by decision (products sync on the domain), and
> 1 and 2 are **not local blockers at all** — Bam's call, and the right one:
> payment and email connect through Nexus on the box, against the real domain.
> A Square key pasted into a laptop cannot be verified anyway; a webhook needs
> a public URL. The original findings are kept below rather than rewritten, so
> the record shows what changed.
>
> **Current verdict: get the VPS.** Everything that can be proven off a real
> host is proven — 331 tests, two runs back to back, both sides typechecking,
> tree clean, pushed at `1e0cef2`. What is left needs a host to exist, and
> `VPS-CHECKLIST.md` is the order to do it in.

## Verdict

> Superseded — see the update above. Kept for the record.

**Not ready for a domain yet — four blockers, none of them deep.**

The platform is in good shape. What is missing is not engineering depth, it is
four pieces of commerce plumbing that no amount of code quality substitutes
for: you cannot take money, cannot email a customer, cannot ask where to ship,
and the main nav leads to empty pages.

None of these are hard. They are mostly configuration plus one real feature
(the shipping step). But shipping to a domain without them means a store that
looks finished and cannot complete a single sale.

## Blockers — must fix before a domain

| # | What | Evidence | Why it blocks |
|---|---|---|---|
| 1 | **No payment provider** | `GET /api/counter/providers/payments` → `[]` | No way to charge. Checkout renders a method list with nothing in it. |
| 2 | **No SMTP** | `settings/notifications`: `smtpHost`, `smtpUser`, `smtpFrom`, `adminEmail` all `""` | No order confirmation, no password reset, no admin alerts. A customer pays and hears nothing. |
| 3 | ~~**Checkout has no shipping address**~~ **FIXED** (`8806e11`) | Was: `/checkout` collected only coupon, payment method, email | Now collects name / line1 / line2 / city / region / postal / country, and the value was traced through to `order_shipments` — fulfillment can see it. |
| 4 | ~~**Nav categories are empty**~~ **DEFERRED** by decision | `mens`, `womens`, `kids-playmoney`, `home-house-money`, `accessories` hold 0 products; only `apparel` has 2 | Bam: products sync on the domain. Worth re-checking the day of the sync — until then those links land on empty pages. |

Blockers 1, 2 and 4 are configuration and data. Blocker 3 is the only one that
needs building.

## Verified working

- **Code**: 318 tests pass, both sides typecheck, working tree clean, pushed to
  `origin/main` at `023aa89`. 28 commits.
- **Storefront**: `/`, `/shop`, `/faq`, `/cart`, `/checkout`, `/product/starter-tee`,
  `/c/apparel` all 200.
- **Category routing**: `/c/mens/`, `/c/womens/`, `/c/kids-playmoney/`,
  `/c/home-house-money/` and the nested `/c/mens/accessories/` all 200.
  **Correction:** `_core/memory.md` flagged these as 404. The routes were fixed;
  what is missing now is products, not routes.
- **Footer shortcode**: gone. The literal `[contact-form-7 …]` no longer appears
  on any page. Another stale flag, now closed.
- **Database**: 43 tables, 35 migrations applied, none pending, none failed or
  rolled back. (`prisma migrate status` reports "0 applied" when run without
  `--env-file` — that reading was mine, and wrong.)
- **Admin**: one user, `Bam`. Sessions renew past halfway.
- **Backups**: enabled, daily, destination `local`.
- **Connections**: `anthropic` (ai) and `printful` (fulfillment) connected.
- **Host advisor**: 0 critical, 1 high, 3 medium, 1 low. Details below.
- **Studio assistant**: real run verified against the live API — called
  `host_scan`, returned an accurate finding. No write tool is offered to the
  model (asserted in tests).
- **Scoped editing**: propose → review → apply verified over the MCP protocol,
  including refusal of traversal and refusal of a replayed proposal.

## Fix at launch, not blocking

| Item | Detail |
|---|---|
| ~~`.env` is mode 644~~ **FIXED** | Now 600. `admin/.env` does not exist — the admin reads the root file. |
| ~~Version string stale~~ **FIXED** | `2.0.0-beta.4` in both package.json files. |
| Redis has no `maxmemory` | Unlimited with `noeviction`. On a 16 GB VPS this is how the OOM killer takes Postgres instead. |
| Postgres `shared_buffers` 128 MB | The default. Set to ~25% of the VPS's RAM after provisioning. |
| ~~7 foreign keys without an index~~ **FIXED** | Migration `20260731161424_fk_indexes`. Postgres does not index FKs automatically, so each was a sequential scan on join and cascading delete. |
| Contact topics | Four topics still fall back to `info@`, and there is no admin UI for `counter.contactTopics` — it is edit-by-API. |
| Theme presets | The one 1.9.44 Appearance feature never ported. Needs a preset registry, not just a field. |
| `estimatedDelivery` | Never populated — no shipping integration writes it, so the ETA line never renders. |
| Wishlist | Per-browser `localStorage` only. An account-backed one needs a table. |

## Never exercised — the real deployment risk

These are not bugs. They are things that have no evidence either way, and every
one of them first runs on the day you go live:

- **The advisor's 12 deployed-only rules have never fired.** Firewall, SSH,
  TLS expiry, pending updates, exposed ports, HSTS, `NODE_ENV`. They are
  unit-tested against synthetic payloads; no Linux host has ever been scanned.
  First real scan on the VPS is where they get proven.
- **`deploy/nginx.conf` has never served a real domain.** It exists and gzip is
  configured correctly (including `gzip_proxied any`, the line that was missing
  once already), but it has never been loaded by a running nginx.
- **The BullMQ worker is not in the PM2 config.** `src/worker.ts` exists;
  `DEPLOY.md` declares this gap honestly. Large imports queue and nothing
  drains them.
- **Extension sandbox is not real.** Third-party extension JS runs in-process.
  Fine while every extension is ours; not fine if that ever changes.
- **No VPS exists yet.** Hostinger KVM 4 is the plan, not a purchase.

## Order of work

1. **Connect a payment provider** in Nexus, and confirm a test order end to end.
2. **Configure SMTP** and send one real confirmation to yourself.
3. **Build the shipping-address step** in checkout — the only code in this list.
4. **Assign products to the four nav categories**, or remove them from the nav
   until they have stock. An empty category is worse than a missing one.
5. Then provision the VPS, run the advisor against it, and work its findings —
   that is when the 12 deployed-only rules finally earn their keep.
6. `chmod 600` the env files, bump the version, set Redis `maxmemory` and
   Postgres `shared_buffers` to the box you actually bought.

Steps 1–4 are what "ready for a domain" means. Step 5 is what "ready for
traffic" means.


## What only Bam can do — ON THE BOX, not before

I will not enter credentials — not a payment key, not an SMTP password. Both
are five-minute jobs for you, and both belong on the VPS rather than here:
Square needs the live domain for its webhook and its hosted card fields, and an
SMTP or API sender is only worth testing from the address customers will see.
Doing them locally proves nothing and has to be redone.

### 1. Connect a payment provider

`GET /api/checkout/gateways` returns `[]` today, which is why checkout shows
"Setup required" under Card. The Nexus catalog already supports ten:

    stripe · paypal · square · braintree · adyen
    klarna · coinbase-commerce · authorizenet · mollie · razorpay

Admin → **Connections (Nexus)** → pick one → paste its key. Nexus encrypts it at
rest, shows only a masked preview, and writes an audit row. Then place one real
test order end to end and refund it.

### 2. Configure SMTP

Settings → Notifications is entirely blank: `smtpHost`, `smtpUser`, `smtpFrom`
and `adminEmail` are all `""`. Until those are set, a customer pays and hears
nothing, and password reset cannot work.

Nexus has SendGrid, Postmark and Resend in the catalog if you would rather use
an API provider than raw SMTP. Whichever you pick, set `adminEmail` too — that
is where order and error notifications go.

### 3. Then

Provision the VPS and run Settings → Advisor against it. Its twelve
deployed-only rules — firewall, SSH, TLS expiry, pending patches, exposed
ports, HSTS, `NODE_ENV` — have never once fired, because no Linux host has
existed to scan. That first scan is the real hardening pass, and it is also the
first proof those rules work at all.
