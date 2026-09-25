---
name: site-security-audit-2026-08
description: "The 8h multi-agent audit of the Therum OS engine (sidemoney.co) — 9 confirmed findings, all fixed 2026-08-23; patterns to keep watching"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4504c37-caac-4f64-affa-6039105bec50
  modified: 2026-08-23T11:45:32.756Z
---

Ran a 12-dimension adversarial audit of the live engine (2026-08-23). 9 confirmed (adversarially verified), 15 refuted, 40 unverified-minor. ALL 9 fixed + deployed + storefront smoke-verified. **Why:** proves the store's real risk surface; several were my own last-48h regressions. **How to apply:** these classes recur — re-check them whenever touching those files.

CRITICALS (all fixed):
1. Public unauth `POST /api/orders` trusted client `discountOverride`/`shippingTotal`/`taxTotal` → buy full basket for ~$0.50 then pay with the returned accessToken. FIX: gated behind admin+storefront-manager bundle. Storefront checks out ONLY via `/cart/checkout` (server recomputes). PATTERN: never expose orderService.create's trusted schema to an unauth route.
2. Store API + wc/v3 catalogue leaked draft/private/restricted/TRASHED products (crewneck leak, reopened). FIX: `PUBLIC_PRODUCT_GATE {status:'active',visibility:'public',deletedAt:null}` on every public/partner product read in wooCompat.ts. PATTERN: any new product read needs this gate.
3. Cross-partner webhook enum/tamper/delete — any store key touched ANY vendor's webhooks. FIX: `ownerScope(credentialId=req.storeAuth.id)` on all /wc/v3/webhooks routes.
4. Auth resolvers matched UNVERIFIED email identities → account capture by pre-seeding victim@email. FIX: upsertCustomer verifiedOnly:true; verifyCode requires verified identity + voids unverified conflicting claims.
5. `/api/mcp` accepted the `pending2fa` challenge token as full write (2FA bypass). FIX: requireMcpAuth rejects role not in {admin,custom} after jwtVerify.

HIGHS (all fixed): markPaid non-atomic (captured payment stranded if inventory-confirm threw → now forces processing + meta.inventoryReconcile flag); password reset unthrottled (email-bomb/OTP-brute → per-IP+per-dest throttle); review-request sweep emailed 53 migrated WP customers (recent updatedAt at import → `sourceId:null` excludes imports — respects the no-email-migrated-customers rule).

Refuted 15 (documented paranoias that are actually safe). 40 unverified-minor still queued (JPY/PayPal .toFixed, misc). Full detail: _core/BETA-10-UNRELEASED.md. Audit workflow script reusable at .../workflows/scripts/full-site-audit-*.js. See [[live-store-real-money]] [[fulfillment-routing]] [[deploy-env-reload-trap]].

## Re-audit 2026-09-19 (Bam: "hows site security") — three parallel adversarial reviewers + live probes

**All 9 August findings still hold**, each guard re-read in current code (orders route auth, PUBLIC_PRODUCT_GATE, ownerScope on partner webhooks, verifiedOnly identity resolution, MCP pending2fa rejection, atomic markPaid, reset throttles, sweep `sourceId: null`, wc/v3 gate).

**New, all fixed and re-verified live the same day:**
- **HIGH — open redirect** `GET /api/m/c/:token?u=` 302'd to any http(s) URL for ANY token (confirmed live: `notarealtoken?u=https://example.com/phish` → 302 phish). Now: token must resolve to a real send; `u` must carry the HMAC `instrument()` mints (`src/lib/clickSign.ts`, `&h=`) or be same-origin (legacy links from the 2026-09-18 send). Verified all five cases.
- **HIGH — cross-partner order PII via webhook brand label** (`webhookDelivery.ts`): the "transition fallback" widened ownership by hook NAME / delivery host, both partner-typed, so any partner key could register a hook called "PodPluser" and receive that vendor's customer addresses. I wrote that fallback in the PodPluser fix. Now credential-less hooks only; the one legacy hook (PODpartner) backfilled with its vendor's credentialId → **0 active hooks without a credential**.
- **MED — SSRF chain**: `emailInline` followed redirects and buffered unbounded bodies; through the open redirect an admin-authored `<img>` could make the worker GET loopback / the WooPayments engine. Now `redirect:'error'`, post-fetch origin check, uploads-paths only, 12MB streamed cap.
- **MED — deleted subscriber still mailed**: `if (s.subscriber && …)` let a null relation (onDelete SetNull) skip the consent gate. Now null = skipped.
- **MED — stranger could re-subscribe an opted-out address** with one form post. Now an opted-out address gets ONE email with a signed link (`/api/shop/resubscribe`, `resubscribeToken`), only the click restores consent; verified bad token ✗ / good token ✓.
- **MED — MCP token scope ignored role**: a custom-role user could mint a `write` token and bypass bundle checks. Token scope is now a ceiling; live access resolved like the session path.
- **HIGH→fixed — phone overwrite**: public signup could swap any existing subscriber's phone and mark it SMS-consented, and undo a STOP. Now a signup may add a phone, never replace one; `smsStatus: unsubscribed` is final. Verified.
- **LOW fixes**: `firstName` restricted to name characters + HTML-escaped in `personalise()` (replacer functions, `$&`-safe); test-send accepts exactly one address; admin proxy rejects `.`/`..` segments; uploads static `dotfiles:'ignore', index:false` (verified 404/403); page CSP gained `form-action 'self' https://www.paypal.com`.
- **Infra found the same day**: Cloudflare proxy came on with `trustProxy` loopback-only and no real-ip config, so every rate limit keyed on ~a dozen Cloudflare edge IPs (proved: `ratelimit:cart-new:162.158.63.181`). Fixed with `/etc/nginx/conf.d/cloudflare-realip.conf` (CF ranges + `real_ip_header CF-Connecting-IP`, copy in `addons/tsc/site-pack/deploy/`) — proved the key became my real IPv6. Then ufw restricted 80/443 to Cloudflare ranges only (`ufw-cloudflare-only.sh`); direct-to-origin now times out, site + checkout + cart POST all 200 through the edge, SSH untouched.

**Still open (accepted / Bam's call):** double opt-in for NEW signups (deliberately not added — it would cost popup conversions; revive-only confirm was the consent-critical half); customer session token readable by JS (design-accepted, no reflection found; `productGrid.ts`/`checkoutFlow.ts` not exhaustively read); MCP skips the mandatory-2FA policy (no 2FA-enrolment gap exists today); CSV import has no row cap (admin self-DoS only); tracking-event inserts per valid token are unbounded (low); `GET /api/shop/unsubscribe` mutates on GET (link scanners can opt people out — the POST one-click exists; change GET to a confirm button when convenient); DMARC still `p=none`.

**Method that worked:** three reviewers with disjoint scopes (Flow public surface / admin + mail path / August re-verification + money paths), each told to try to break it and to cite file:line, then I re-derived the top findings live before fixing, deployed in two gated batches, and re-probed every fix against production — 429 on my own probes was itself the proof the limiter now sees real IPs.
