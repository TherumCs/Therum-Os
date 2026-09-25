---
name: live-store-real-money
description: sidemoney.co runs LIVE Stripe + PayPal — never test-charge; order emails fire from markPaid
metadata: 
  node_type: memory
  type: project
  originSessionId: 1eb82035-25c8-45fb-83e3-63b52d3072eb
  modified: 2026-08-12T13:04:48.022Z
---

sidemoney.co is a **LIVE** storefront: Stripe key is `sk_live`, the PayPal
credential is `:live` (4 parts, webhookId set). Real cards, real money. NEVER
complete a checkout to "test" payments — a Stripe/PayPal charge is real. Verify
payment/email flows by **server evidence** (the `order` + `paymentEvent` tables,
an SMTP self-test via `sendEmailTo`) and by driving the browser only up to the
payment handoff — not by paying. See [[get-evidence-before-theorising]].

Order emails (customer receipt + admin notify to `commoncents@sidemoney.co`) fire
from `orderService.markPaid` at the pending→paid edge — the one chokepoint every
settlement path funnels through (in-page Stripe `payWithToken`, PayPal
`/checkout/return`, and the PSP webhook `_apply`). They used to live ONLY in the
webhook handler, so in-page Stripe orders (no webhook is even configured —
`webhookSecret=none` for every provider) settled silently: no receipt, no owner
alert. Mail goes out via Gmail SMTP (`smtp.gmail.com`, `commoncents@sidemoney.co`
app password) and is confirmed working.

PayPal is a redirect gateway: approval only authorises; the money captures when
the buyer returns to `/checkout/return`. `createIntent` now sets `return_url` for
every funding source (it used to only for Venmo), and the access token rides as
`t` because PayPal appends its own `token` on return.

**Checkout methods (verified 2026-08-12, all end-to-end through the deployed
checkout):** card + Apple/Google/Link settle in-page via `pay-token`; PayPal /
Venmo / PayPal Credit redirect via PayPal; **Klarna / Affirm / Afterpay / Cash
App now work** — `stripeGateway.createIntent` confirms server-side with a
`return_url` and returns Stripe's redirect (Cash App uses the
`cashapp_handle_redirect_or_display_qr_code` next_action, others use
`redirect_to_url`); `redirect-start` accepts `provider: stripe`; `/checkout/return`
→ `finalizeReturn` marks paid. Before this they were OFFERED but had no
settlement path — an unpaid order shown as "success". Venmo lives in the P2P
method group, PayPal Credit in "Pay later". Redirect methods REQUIRE a complete
US address (Stripe 400s on missing `postal_code`) — checkout now requires ZIP +
state for US. Any gateway rejection is caught in `paymentGatewayService.createIntent`
and returned as a clean `ValidationError` (422 "choose another method"), never a
raw 500. `finalizeReturn` polls Stripe `intentStatus` up to ~4×1.5s so orders
settle without a webhook.

**Fulfillment (Printful) — 2026-08-12:** paid orders auto-submit to Printful from
`orderService.markPaid` → `confirmPrintfulOrder` (drafts at checkout via
`routeOrder`, confirmed to production on payment). In-page Stripe used to bypass
markPaid so orders never routed (same bug as emails) — now fixed. TWO real
issues found: (1) the Printful connection credential is `token|storeId` and the
storeId was WRONG (`1536603`, a dead store → every order failed "Store not found
or not accessible by this user"). Correct store is **`18591060` "The Sidemoney
Company"** (the token via GET api.printful.com/stores also sees `14110753`
"Personal orders" — do NOT use that). Fixed in `db.connection` (provider
'printful', credentialEncrypted via `encryptSecret`). (2) After that, orders
reach Printful but fail with **error "Expired Card"** — the Printful ACCOUNT's
billing card is expired (Bam must update it in Printful → Billing; not a code
fix). Felix's order = Printful order 171185470 (external SMNY-20260812-0de393548d),
re-confirm once the card is updated.

**STILL OPEN — no PSP webhook (webhookSecret none for every provider).** Needed
for: **ACH** (`bank_ach`, us_bank_account — async over days, needs Financial
Connections bank-link + the webhook; currently graceful-unavailable with a clean
422, NOT a 500) and belt-and-suspenders reconciliation. Fix: add endpoint
`https://sidemoney.co/webhooks/psp/stripe` (event `payment_intent.succeeded`) in
the Stripe dashboard, store the `whsec` via Nexus so `connectionService.webhookSecretFor('stripe')`
returns it. Bam's dashboard action — cannot be done from code.
