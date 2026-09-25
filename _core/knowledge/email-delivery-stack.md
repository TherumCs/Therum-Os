---
name: email-delivery-stack
description: How sidemoney.co actually sends mail — Postmark streams, inline images, the worker memory ceiling, and the DNS state
metadata:
  type: project
---

How mail leaves sidemoney.co as of **2026-09-18**, after the Friday newsletter (302 people) exposed several holes.

**Transport: Postmark (Nexus), added 2026-09-18.** Server "The Sidemoney Company" (id 21004160), three streams: `outbound` (Transactional), `broadcast` (Broadcasts), `inbound`. Credential stored in Nexus under provider `postmark`; an optional second credential `postmark-broadcast` is used for marketing mail when present. Gmail SMTP (commoncents@sidemoney.co) remains the fallback, so **always verify which transport a send actually used** — `via` in the result is the transport that was TRIED, not the one that succeeded. The system of record is Postmark's own activity API (`/messages/outbound`, then `/details` for events + attachment count).

Two bugs found the moment it was switched on, both of which would have read as "working":
- **`Reply-To` is a named Postmark field, not a header.** Passing it in `Headers` gets the whole message rejected 422 / ErrorCode 300 — and the send then falls through to Gmail while still reporting Postmark. `viaPostmark` now lifts reply-to out and drops every other reserved header.
- **Mail WITH attachments used to skip every Nexus sender.** Since campaigns embed their images, every newsletter would have silently stayed on Gmail SMTP. `ATTACHMENT_CAPABLE_SENDERS = [viaPostmark]` fixes it.

**Images travel inside the message** (`src/services/emailInline.ts`): fetched once per campaign, re-encoded through sharp (max 1200px, JPEG q78, PNG kept when the source has alpha), attached as `cid:` parts. The open-tracking pixel is deliberately excluded — it only works because it is fetched. Campaigns and automations both use it.

**The worker memory ceiling.** That image work pushed the worker past `max_memory_restart: '300M'`, PM2 killed it mid-send, BullMQ marked the job stalled ("job stalled more than allowable limit"), and the Friday send died at 20 of 302. Ceiling is now **900M** in ecosystem.config.cjs, and emailInline sets `sharp.cache(false)` + `sharp.concurrency(1)`. After the fix the same send ran ~3s/message with zero failures. **Check the ceiling before adding memory-hungry work to the worker.**

**One send per person** (Bam's explicit requirement): `@@unique([campaignId, email])`, marketing worker concurrency 1, each row CLAIMED (`queued`→`sending`) before the transport call so a crash cannot re-send, and no retry when the failure came at SMTP `DATA` (the server may already have queued it).

**Automations have their own queue** (`marketing-automation`, own Worker, concurrency 2). Before this, a popup signup during a 300-person campaign waited the entire send for the 10%-off code it was promised "in your inbox".

**Bounce handling.** Gmail forces the envelope sender to the authenticating account, so bounces and out-of-office replies landed on commoncents no matter what Reply-To said — Postmark is the actual fix. The first send produced 8 hard bounces, all marked `status: 'bounced'` (list went 302 → 294 mailable).

**DNS (Cloudflare) — cleaned and un-paused 2026-09-18.** The zone had been PAUSED (every record showed "Proxied" but answered with the origin `2.25.93.243`, and the site returned `Server: nginx` with no `cf-ray`). Bam deleted the dead records and un-paused it the same afternoon. Final zone, 9 records: root A + `www` CNAME (both proxied, now answering 104.21.32.210 / 172.67.155.36), `pm-bounces` CNAME DNS-only, ONE MX (`smtp.google.com`), Postmark DKIM `20260918141948pm._domainkey`, `google._domainkey`, SPF, DMARC. Deleted: `alpha` / `beta` / `ftp` / `pay` / `staging` A records (nginx serves ONLY `sidemoney.co` and `www`, so all five were dead weight publishing the origin IP), the Titan MX pair, the Flodesk pair (`fde._domainkey`, `fdesp`), and 13 malformed double-encoded CAA records.

Verified THROUGH the Cloudflare edge after un-pausing, not just in DNS: homepage / shop / PDP / **checkout** all 200, `cf-cache-status: DYNAMIC` on `/api/*` (so the API is not being cached), and a real **cart POST returned 201**. Origin IP no longer resolves anywhere.

Left over, low priority: certbot still holds a renewal config for `pay.sidemoney.co`, a hostname nothing serves and that no longer resolves — its renewal will start failing around Oct 2026 and should be removed with `sudo certbot delete --cert-name pay.sidemoney.co` (needs Bam's password). The real cert (`sidemoney.co`, valid to 2026-10-30) renews fine and `certbot.timer` is active. DMARC is still `p=none` — tighten to `p=quarantine` once Postmark has a sending history.

**Account pages on a subdomain: asked and answered 2026-09-18 (no).** Bam asked whether `account.sidemoney.co` would just be a DNS record. It would not: the customer session token lives in localStorage AND a host-only `th_customer` cookie (set in `src/site/accountPage.ts` with `path=/` and no domain), and the cart token, `th_src` and `th_sub` are host-only too — so a subdomain logs everyone out, loses carts across the boundary, and turns every API call cross-origin. Verdict: `sidemoney.co/account` is the right shape; revisit only if the portal genuinely splits out.

See [[live-store-real-money]] [[marketing-module-groundwork]] [[bird-season-launch-state]] [[deploy-env-reload-trap]].

**2026-09-20 — STILL PENDING APPROVAL. Do not trust a blackhole test.** At 18:42 ET a send to `test@blackhole.postmarkapp.com` returned ErrorCode 0 and I declared Postmark approved; at 19:00 ET a real off-domain send (fresco.pbm@gmail.com) got 412 again. Postmark's own domains are exempt from the pending-approval restriction, so the blackhole proves nothing about approval. **The only valid approval test is a real off-domain recipient** (or the dashboard). Bam said "Postmark is setup" — that meant configured, not approved. Until approval, off-domain mail rides the 412 fallback to Gmail; watch `POSTMARK PENDING APPROVAL` in the api/worker logs.

**2026-09-19 — Postmark was PENDING APPROVAL (ErrorCode 412).** Until Postmark approves the account it can only deliver to `@sidemoney.co` recipients; every customer-facing send was being refused and silently falling back to Gmail SMTP. My own tests passed only because they went to `commoncents@`. Bam's decision: **"Everything should be through postmark"** → `sendEmailTo` is Postmark-only when a credential is connected; a refusal is a failed send (recorded on the row), EXCEPT 412 pending-approval which falls back to Gmail with an error-level log line `POSTMARK PENDING APPROVAL` so receipts are never lost. Invalid/inactive recipient (300/406) is final, never falls back. **Bam must click "Request approval" in the Postmark dashboard**; once approved the fallback stops firing on its own. Verify approval landed by grepping the worker log for that error line going quiet, then by a real customer send showing in Postmark activity.
- Per-signup "New newsletter signup" email to the merchant REMOVED (Bam: "stop fucking emailing me"; the audit also flagged it as an abuse vector). Flow › Subscribers is the record.
- **Never probe `/api/subscribe` on production.** It sends mail. My 8 audit probes (`probe*@example.invalid`, `verify*@`) produced 8 merchant notices + 8 bounces + rolling Gmail "Delay" DSNs in Bam's inbox the morning after I promised no more test emails. Probe the service layer on the box, or a route that does not send.

**Rendering an email to show Bam** (the method that finally worked, after several previews he couldn't see): render the campaign server-side, inline the images, then `chrome --headless=old --disable-gpu --hide-scrollbars --window-size=760,14000 --screenshot`. Then crop in Python **against the page's own background colour sampled at `px[5, h-5]`** — the email ground is `250,250,250`, so cropping against pure white finds no edge and you keep 14000px of blank. Slice at ≤1700px for chat, or build a single PDF (`PIL … save_all=True`) which he can scroll on a phone. The desktop preview panel does NOT load remote images, and a ~1.7MB base64-inlined page silently truncates — both read to him as "the images are broken". For anything that claims to be the real email, render the DELIVERED message pulled back over IMAP, not the composer preview.
