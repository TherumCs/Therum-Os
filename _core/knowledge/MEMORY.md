## How to work with Bam (read these first)
- [Anticapitalist script](anticapitalist-script.md) — BAM'S STANDING LAW, hook-loaded every turn: 200≠working, no single-shot audits, verify end-to-end, use the setup, own failures
- [Quote before acting](quote-before-acting.md) — loop step 3: quote the instruction in Bam's words or the action is not authorised
- [Bam's working style](bam-working-style.md) — do the whole thing without asking; when he says it's wrong it's wrong; consolidate memory every turn; treat what he states as fact
- [Catch the gaps yourself](catch-the-gaps-yourself.md) — his #1 complaint: stop shipping half-working things; walk the WHOLE flow before claiming done
- [Get evidence before theorising](get-evidence-before-theorising.md) — assert only from the system of record, never from a stale note
- [Compare against the reference site](compare-against-the-reference-site.md) — :10025 is the visual bar; measure, never present a screenshot as proof
- [No widows in copy](no-widows-in-copy.md) — bind the last words of a line with a non-breaking space (email kit `nw()`)

## What sidemoney.co is
- [Live store, real money](live-store-real-money.md) — Stripe/PayPal/WooPayments live since 2026-08-14; never test-charge; order emails fire from markPaid
- [Bird Season launch state](bird-season-launch-state.md) — what runs where on the VPS, the 25MB animated-webp lesson, homepage = db.content, Bam's 2.0-production roadmap
- [THE PORT LAW](the-port-law.md) — :10025 is truth, nothing invented, Elementor banned — with a 2026-09-19 banner: what shipped is Therum OS 2.0, NOT Bricks
- [Product vs instance](product-vs-instance.md) — HARD RULE: the Therum-OS-2.0 repo carries no store; Sidemoney lives in TSC-BETA `addons/tsc/site-pack/` + DB settings + env
- [GitHub access](github-access.md) — SSH deploy key works; no gh login; beta.10 tag = store-neutral `480fd70`; the box must equal origin/main
- [Local sites and DBs](local-sites-and-dbs.md) — every Local DB is named "local"; :10025 socket zff81gb8N; verify socket before any mysql write
- [Deploy env reload trap](deploy-env-reload-trap.md) — `pm2 reload <name>` keeps stale env; after any .env change reload from ecosystem.config.cjs

## Commerce
- [Payments audit 2026-09](payments-audit-2026-09.md) — every checkout method's REAL rail; PayPal capture fix unverified live; Cash App not activated; admin "NOT CONNECTED" card is false
- [WooPayments engine](woopayments-engine.md) — headless WP at /var/www/pay under sidemoney.co (no subdomain); Jetpack-identity transplant; bridge to TOS
- [Coupon system](coupon-system.md) — cart-scope only; `meta.noMemberDiscount` exempts all 9 jerseys; GIVEAWAY15; WELCOME10 chain verified end to end 2026-09-18
- [Inventory / stock model](inventory-stock-model.md) — tracked vs in_stock; "Only N left" only when tracked & ≤3; jerseys preorder 6/size; POD infinite
- [Fulfillment routing](fulfillment-routing.md) — printful 8 / printify 22 / tapstitch 11; Printful card expired + Tapstitch unconnected are Bam's
- [Vendor order-sync mechanics](vendor-order-sync-mechanics.md) — PodPluser builds from the webhook body ONLY and keys on ITS OWN pushed ids (twin-id rewrite deployed 2026-09-16); push is ASYNC
- [Store attribution and feed](store-attribution-and-feed.md) — th_src first-touch → order.meta.source; Meta feed at /feed/facebook.xml; marginFloor guard
- [WP customer migration](wp-customer-migration.md) — 55 WP customers + 53 orders imported; DON'T email migrated customers until Bam says who gets what

## Storefront
- [Storefront merchandising](storefront-merchandising.md) — cluster primary defaults to earliest-created (woo44 trap); swatch binding; sortSizes; ONE GRID RULE
- [Storefront render gotchas](sidemoney-storefront-render.md) — descriptions render RAW HTML; Meta feed images must be local; PDP 'apple' style + lightbox
- [Site fonts](site-fonts.md) — Roboto Condensed/Montserrat were never loaded (fixed 2026-09-15); headings → Manrope via the ported CSS var + Redis settings flush
- [Blog + À Pas Dorés system](sidemoney-blog-system.md) — posts = Content type=post; À Pas Dorés = umbrella category over Sixers/Bird; pending art Bam owes
- [Sidemoney signage](sidemoney-signage.md) — the two print signs + PDP QR set; transparent-QR-fails-scan lesson
- [Pull images from :10025 MySQL](pull-images-from-10025-mysql.md) — reference galleries live in the WP DB (prefix smxx), not the Store API
- [Ported sheet outranks page CSS](ported-sheet-outranks-page-css.md) — .th-page-<id> rules are 0,3,0 and load last; read matched styles
- [Ported chrome has two headers](ported-chrome-has-two-headers.md) — querySelector('.js-cart') grabs the hidden mobile one; use querySelectorAll
- [Elementor port contract](elementor-port-contract.md) — REJECTED approach; record of the Elementor coupling that must be ripped out

## Email + marketing (Flow)
- [Flow marketing module](flow-marketing-module.md) — architecture map, live state (popup ON, welcome ON, first campaign sent), the compiled-html gotcha, Bam's copy rules
- [Email delivery stack](email-delivery-stack.md) — Postmark on both streams (2026-09-18), inline cid images, the 300M worker ceiling that stalled a live send, one-send guarantees, DNS/Cloudflare state
- [Signal (Meta Pixel + CAPI)](signal-meta-pixel.md) — Studio app built 2026-09-22 for the Meta ads plan; deployed OFF, needs Pixel ID + CAPI token; turn on ~a week before October launch
- [Therum OS artifact links](therum-os-artifact-links.md) — published Artifact URLs Bam refers to (incl. the Friday newsletter page)

## Security + verification
- [Site security audit 2026-08](site-security-audit-2026-08.md) — 9 confirmed (4 critical incl. a live buy-for-pennies hole), all fixed 2026-08-23; patterns to keep watching; 2026-09-19 re-audit appended
- [Headless verify harness](headless-verify-harness.md) — drive real Chrome over CDP; four traps that each produced a confidently wrong verdict
- [Verify settings by rendered geometry](verify-settings-by-rendered-geometry.md) — measure the element, not its wrapper, and not mid-load
- [Fake test fixtures hide real bugs](fake-test-fixtures-hide-real-bugs.md) — two live auth holes behind a green suite
- [Suite state leaks between runs](suite-state-leaks-between-runs.md) — a 409/429/duplicate-slug failure is last run's residue
