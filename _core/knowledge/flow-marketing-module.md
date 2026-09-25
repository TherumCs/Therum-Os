---
name: flow-marketing-module
description: "Flow = Therum OS 2.0 email/SMS engine (built 2026-09-15) — architecture, live state on sidemoney.co, hard-won gotchas; delivery mechanics live in email-delivery-stack"
metadata: 
  node_type: memory
  type: project
  originSessionId: e745e2aa-9578-48ef-9843-d125d121f24c
  modified: 2026-09-19T12:39:52.479Z
---

**Flow** is the Flowdesk-style marketing module Bam asked for ("we might as well do the whole thing", then "build all bro. stop asking me"). Built in 7 slices on 2026-09-15, all deployed and verified live. Own sidebar section "Flow"; route stays `/tos-admin/marketing?tab=…`. How mail physically leaves the box (Postmark streams, inline images, worker limits, one-send guarantees) is in [[email-delivery-stack]] — do not duplicate it here.

**Architecture (files are the truth; this is the map)**
- Schema: `Subscriber`, `MarketingList`, `ListMembership`, `Segment`, `Campaign`, `Automation`, `CampaignSend` (unique `token` + unique `[campaignId,email]`), `CampaignEvent`, `SignupForm` — one migration `20260915100000_marketing_module`. After migrating on the box run `npx prisma generate` there too or dist crashes on unknown models.
- `src/services/marketing.service.ts` — subscribers/lists, `subscribe()` idempotent (`resubscribe:true` only for an explicit form act), `unsubscribe()` + `mirrorOptOutToCustomer()`, `syncCustomers()` (engaged customers → "Customers" list), `parseCsv()`, `mailableIn()`, `campaignService` (CRUD/duplicate/render/preview/sendTest/products), `personalise()` merge tags.
- `src/services/emailBlocks.ts` — Block union (eyebrow/heading/text/image/button/divider/spacer/product/html), each with optional `custom` HTML override; `renderEmail` goes through the shared `shell()` from emailTemplate.ts (`logoWidth` 210 for Flow, 150 for receipts).
- `src/services/campaignSend.service.ts` — `resolveAudience` (lists ∩ segments, `subscribed` only), `schedule` freezes CampaignSend rows + BullMQ delayed job (minute tick is the backstop), `run` drains in batches, `instrument()` rewrites hrefs to `/api/m/c/<token>?u=` and appends the `/api/m/o/<token>.gif` pixel, `report`.
- `src/services/segment.service.ts` — RuleSet evaluator (source/tag/list/bought_product/bought_category/orders_count/spent/last_order_days/subscribed_days/has_phone/engaged).
- `src/services/automation.service.ts` — 4 seeded rows (welcome / abandoned_cart / post_purchase / winback); `fire()` → CampaignSend + job on the **separate** `marketing-automation` queue; `deliver()` re-checks consent. Welcome uses ONE shared code when `trigger.coupon.code` is set (Bam: "just make the code welcome10"), else mints `<PREFIX>-XXXXXX` per person.
- `src/services/signupForm.service.ts` + `src/site/popupRuntime.ts` — one live popup at a time; per-BROWSER rules (Bam: "not super intrusive"): `th_sub` (subscribed, ever) / `th_pop` (dismissed, 30d) / `th_customer` / once per session / never on cart-checkout-account-unsubscribe; crawler UA gate (Meta's `meta-externalagent` once fired 10k "seen" beacons a day). Module settings: weekly slot (default Mon 10:00 ET), timezone, `capPerWeek` 2, `smsFrom`.
- `src/services/sms.service.ts` — Twilio via Nexus; STOP/START inbound at `/api/shop/sms/inbound` (403 without a valid signature). **Never verified live — no Twilio connected.**
- Admin: `admin/app/(app)/marketing/*` tabs + `campaigns/[id]` editor (drag blocks, per-block HTML toggle, live iframe preview, SendPanel) + `automations/[id]` (TriggerPanel). Proxy: catch-all `admin/app/api/marketing/[...path]/route.ts`.

**Live state on sidemoney.co (2026-09-19)**
- ~294 mailable subscribers: 57 mirrored customers + Bam's 297-row Flodesk export imported 2026-09-16 (statuses preserved, consent dates kept, old segments → tags) minus 8 hard bounces from the first send. Lists: Newsletter, Customers.
- Popup ON (logo, "10% off your first order", 6s delay) — 150+ views, **0 organic signups** as of 2026-09-19. Plumbing proven end to end (signup → welcome in ~1s → `WELCOME10` → $70 cart became $63); the zero is a conversion problem, not a bug.
- Welcome automation ON. Copy is deliberately five things and nothing else (Bam: "simple my nigga"): eyebrow, "Welcome to The Sidemoney Company.", "Thanks for signing up. You are on the list. Here is your code.", a bordered code panel, "Shop the store". Subject "Welcome to The Sidemoney Company. Here is your 10% code."
- First campaign sent Fri 2026-09-18 10:00 ET: 299 delivered / 0 failed, 238 unique opens (inflated by Apple Mail's proxy — `17.166.x` fetches the pixel), 15 clickers, 7 unsubscribes. Cart / review / win-back automations OFF. SMS unconnected.

**Gotchas that cost real time**
- **Editing `blocks` in the DB does not change what is sent.** `automation.html`/`campaign.html` are the compiled output; regenerate with `renderEmail` (or PATCH the blocks through the API) or the old body keeps going out. Bit me on the welcome rewrite 2026-09-18.
- **Prisma `NOT { meta: { path: [...], equals } }` is SQL NULL for rows missing the key** — everyone vanishes. Filter meta in JS. This had `dropBroadcast` mailing nobody for weeks.
- `{{first_name}}` falls back to "there"; the popup does not ask for a name, so never put the tag in a subject line.
- Bam's copy rules for Flow mail: **no em dashes anywhere**, no sales taglines ("for the ones who claim it" was "retarded"), name the capsules, plain sentences. He reads previews on his phone: a "preview" that is not the delivered message proves nothing (see [[email-delivery-stack]]).
- `/api/subscribe` sends a welcome email per call — treat it as an outbound-mail trigger when thinking about abuse.
- Test sends: ONE, to `commoncents@sidemoney.co`, then verify by reading the delivered message over IMAP (never print the password), then delete the test subscriber rows and reset the popup's `submits` counter. Bam: "I only need one test email."

**Open / not built:** per-campaign From name; social posting is calendar-only; automations are email-only; frequency cap never exercised in anger; SMS never sent. Bam owes: Gather Food Hall follow-up dates, pop-up list page.

See [[coupon-system]] [[email-delivery-stack]] [[wp-customer-migration]] [[live-store-real-money]].

**The first newsletter, as actually sent** (campaign `cmu4hot8z000028kzjovpjnau`, Fri 2026-09-18 10:00 ET, subject *"Sixers Season, Bird Season, and the Gather Food Hall pop-up"*, preheader *"Jersey pre-orders, Bird Season restocks, and where we pop up next."*). Block order and the copy Bam settled on after ~8 rounds — reuse this as the house structure:
1. logo · eyebrow "The Sidemoney Company" · **"Two seasons. One label."**
2. *"À Pas Dorés means with golden steps. It is our sports label, made for the teams and the eras that raised us, in the language of money. Two capsules are live right now. Bird Season for the Eagles and Sixers Season for the Sixers."* — he asked twice for the capsules to be NAMED, and for the Gather sentence to come out of the intro (it has its own section).
3. À Pas Dorés cover image → **Sixers Season / "Trust the process."** → '96 Series $120 product block → "Shop Sixers Season". Copy ends on facts; he killed the sales tag *"A limited run, for the ones who claim it"* ("such a fucking retarded line").
4. stadium hero → **Bird Season / "The city's colors, worn loud."** → Kelly Green practice jersey $75 → "Shop Bird Season". Colour vote is **DM @sidemoneyco**, not reply.
5. **Around the shop / "Money you can carry."** → Money Wash Wallet $70, Snakeskin Pin $4 → "Shop everything".
6. **Gather Food Hall / "Thank you for pulling up."** — Sunday Sept 13, Eagles opener, kickoff 4:25, thanks. Then the sentence he explicitly kept: *"We will be back at Gather, and at a few other spots around Philly, from now until December. An official list is coming with every pop-up and every date, and this list gets it first. Want us in your city? DM @sidemoneyco and say where."*
7. **"Read more stories from our blog"** → /blog (he renamed it from "Read the stories" once he learned where it pointed — label must say where it goes).
8. footer line: *"You are getting this because you signed up with The Sidemoney Company. Codes, drops and pop-up dates land here first."*

**Reply is never a CTA.** Mail goes from commoncents@sidemoney.co and bounces/auto-replies land on Bam; he does not want an inbox to work. Every "tell us" ask is **DM @sidemoneyco** (link styled `color:#070707;font-weight:700;text-decoration:underline`). `replyTo` is still set to commoncents so a reply is not lost.
