# memory.md — Working Memory
TSC-BETA · volatile state across loop iterations.
Read at START every loop. Update at END every loop. Keep lean.
Scope: UNIVERSAL mechanism · per-project content. Durable user/project facts go context.md.

> **Consolidated 2026-09-12.** The full dated decision log (83 entries, Aug 2026 and
> earlier — POD/vendor connect fixes, email/SMTP, category templates, WooPayments
> build, all resolved and baked into code) is archived in `memory.backup-20260912.md`.
> This file is the LEAN current state. Deep topic knowledge lives in the `/memory/*.md`
> files (indexed in the auto-memory `MEMORY.md`) — point to them, do not duplicate.

## ⭐ WHAT SIDEMONEY.CO IS — VERIFIED live 2026-09-12 (not Bricks — read this)
- **sidemoney.co = a custom Therum OS 2.0 app** (Fastify/Node + Prisma/Postgres), LIVE since
  2026-08-14, under PM2 on the VPS (`therum@2.25.93.243`). Deployed tree
  `/Users/bam/Local Sites/therum-os/therum-cms-2`. THE live store — real money. [[live-store-real-money]]
- **It is NOT Bricks and NOT a WordPress front end.** Verified from the box: nginx
  `location / { proxy_pass http://therum_api }` where `therum_api = 127.0.0.1:10009` = the
  Fastify app (PM2 `therum-cms-api`). Every page (/, /careers, /shop) is served by it. The
  live HTML uses Therum's OWN classes (`th-*`) + ported `c-ip-*` components (from :10025's
  look) — ZERO `brxe-`/Bricks/Elementor framework in the output. Bricks was the ORIGINAL PLAN
  (context.md / [[the-port-law]] say "target is Bricks") but that is NOT what shipped.
- **WordPress exists only as an internal headless WooPayments engine** (`therum_pay :8088`,
  `/var/www/pay`) — nginx routes ONLY `/wp-json/wc/v3/payments`, `/wp-json/jetpack`,
  `/wp-content/plugins/woocommerce` to it. Admin = Next.js (`therum-cms-admin :3100`) at
  `/tos-admin`. Static assets from `/var/www/sidemoney-static` (that's the only `wp-content`
  in page HTML — image URLs, not WP serving pages). [[woopayments-engine]]
- **Pages render from `db.content`** (Content model): homepage slug `sidemoney-home`,
  `/careers`, blog posts, category pages — each a Content row with an HTML body rendered by
  the app. Editing a page = editing its Content row (script pattern in [[sidemoney-blog-system]]).
  **Header/footer chrome = db.content rows too, rendered site-wide as chromeHeader/chromeFooter:
  the FOOTER is slug `site-footer` (id `cms2kmjd80037sxlpy70m43l7`).** GOTCHA that cost hours
  2026-09-12: the ported `c-footer` and its wrappers are TRANSPARENT — the black only comes from the
  bottom-bar container `.th-el-5c9433d` (bg `#070707`), a 3-col flex (payment slot | © | social).
  The OLD payment strip was the IMAGE `ricky-2152262473.png` (alt="Ricky") — a PNG of the badges
  INCL Shop Pay, sitting in the left slot (the image widget `.th-el-51199c4`). To replace it: put
  the new strip INSIDE that `51199c4` widget (left slot). Putting it anywhere ELSE (e.g. a "full-width
  row" between containers) lands it in a transparent gap → shows the white page = a white bar. The
  accepted-payments strip `.c-pay-strip` now lives there: 10 inline-SVG badges (aaronfagan full-color
  Visa/MC/Amex/Discover/PayPal + simple-icons Apple(logo)/Google Pay/Klarna/Afterpay + affirm
  wordmark), 30×19, `justify-content:flex-start`, one line (the slot is ~383px at desktop; keep badges
  small or it wraps), NO Shop Pay / Cash App. Rebuilt via scratchpad `buildstrip.mjs` (fetches real
  SVGs) → `inject.mjs`. (The buy-box express wallet row in productGrid.ts still has an inert `shop_pay`
  label — never renders for us.)
- **tsc-beta** (Local `:10020`, theme `bricks`) = the Bricks design surface from the (unshipped)
  Bricks plan. **:10025** (`the-sidemoney-company`, old WP/Elementor, socket `zff81gb8N`) =
  READ-ONLY visual reference; never edit unless Bam names that path; keep shut down (shares the
  Jetpack token with the payments engine). [[local-sites-and-dbs]] [[the-port-law]]
- **Payments:** headless WooPayments engine on the VPS (`/var/www/pay`, internal only) carries
  card / Apple / Google / Link / Klarna / Affirm / Afterpay; the PayPal rail carries
  PayPal / Venmo / Credit / Pay-in-4. [[woopayments-engine]] [[payments-audit-2026-09]]
- Prod DB access: `DBURL=$(pm2 jlist | node -e '…pm2_env.DATABASE_URL')`; strip `?schema=` via
  `${DBURL%%\?*}` for psql. Table `content` (snake_case cols). Deploy: scp src → box, gated
  `if npm run build EXIT 0; then pm2 reload`; reload from ecosystem after any `.env` change
  or it keeps stale env [[deploy-env-reload-trap]].

## LIVE OPEN THREADS (2026-09)
- **Payments [[payments-audit-2026-09]]:** PayPal was 100% broken (approve-then-never-capture);
  capture-on-approval fix DEPLOYED 2026-09-03 + verified against the real failed event, but NOT
  proven with a live capture yet (needs one real OR sandbox approval). Bam's PayPal **sandbox app
  keys** exist + work (found in the f39b8ece transcript, verified on sandbox) — no sandbox BUYER
  account yet, so a full autonomous sandbox capture is still blocked on the approval click.
  **Cash App** is offered at checkout but NOT activated on the WCPay account (createIntent 500s).
  The admin "WooPayments NOT CONNECTED / $0" card is a FALSE readout (rail is connected + depositing).
- **Careers page — DONE + verified live 2026-09-12.** Added 6 roles to the `/careers` Content row
  (id `cms6fyqrj00002clp0cfxf20z`), matching the existing `.cr` markup: Content Creator/Editor →
  Brand & Creative; Social/Community Mgr → Marketing; Partnerships & Collab Mgr → Partnerships;
  Bookkeeper/Finance (fractional) → Finance & Operations; + NEW dept "Operations & Fulfillment"
  (Ops/Fulfillment Mgr + Production/Vendor Coordinator). Header now "20 open across 8 departments".
  Existing listings untouched. Verified: 200, all 6 titles + counts live. **Apply links: the careers
  system is CODE-DRIVEN — `src/site/careers.ts` `ROLES[]` powers real per-role apply PAGES (a form →
  careers@) at route `/careers/:slug` (storefront.ts). The `/careers` INDEX is the db.content row; its
  Apply hrefs are `/careers/<slug>` (NOT auto-rewritten — kept in sync by hand).** First pass I linked
  the 6 new roles to mailto; Bam then wanted them to work like the rest, so I ADDED all 6 to `ROLES`
  (deployed) and repointed the index links to `/careers/<slug>`. Verified live: all 6 apply pages 200 +
  form, index has 0 mailto / 20 apply-page links, existing intact. **Adding a role = edit ROLES in
  careers.ts AND the db.content index listing (both).**
- **Careers APPLY form — FIXED + verified end-to-end 2026-09-12.** Real multipart submissions were
  500'ing (`nodemailer EENVELOPE "No recipients defined"`): `CAREERS_INBOX` was read only from
  `process.env`, and the live pm2 env snapshot lacked it — the var was added to `.env` after the last
  full `pm2 start`, and deploys reload by NAME so kept the stale snapshot ([[deploy-env-reload-trap]]).
  Contact form was unaffected (its recipient is DB-sourced). Fix: `CAREERS_INBOX = process.env.CAREERS_INBOX
  || 'careers@sidemoney.co'` fallback (careers.ts) + build/reload. Verified: real `-F` POST w/ PDF CV →
  200 `{sent:true}`, transport accepted, no error. NOTE: env-drift means MAIL_FROM/SMTP_HOST are also
  absent from live env (mail works because transport is DB-sourced) — see FLAGGED.
- **Marquee running-line bullets — FIXED + verified 2026-09-12** (home + about, mobile + desktop). The
  SVG-circle bullets hugged words at the copy SEAM ("…Afterpay•", 0px) because my earlier white-band
  fix had set `.c-ip-running-line__content{margin:0}`, killing the trailing gap the theme's scroll
  keyframe assumes (`translateX(calc(100% + var(--gap)))`, `--gap:15px`); plus some home titles had a
  stray leading space. Fix: restored `margin:0 var(--gap,15px) 0 0` in BANNER_STYLES (bannerRuntime.ts)
  + trimmed title whitespace in the db.content rows. Now bullet→text and copy-seam all a uniform 15px,
  loop still seamless.
- **Coupon GIVEAWAY15** live: 15% off, one use per customer, all jerseys exempt [[coupon-system]].
- **Pending art Bam owes:** À Pas Dorés hero background photo; Gather Food Hall flyer (draft ready)
  [[sidemoney-blog-system]].

## STANDING CONSTRAINTS (hard — open the file for each)
- [[anticapitalist-script]] — 200≠working; verify end-to-end; no single-shot audits; don't
  overcomplicate/waste tokens; USE the setup (MD + memory + skills); own failures flatly.
- [[quote-before-acting]] · [[bam-working-style]] · [[catch-the-gaps-yourself]] · [[get-evidence-before-theorising]].
- **ONE GRID RULE** + category T1/T2 templates — do not re-derive: `src/site/categoryTemplates.ts`, [[storefront-merchandising]].
- Vendor-draft purge keeps ONLY manual drafts (sourceId=null); PULL partners checked via the
  StoreCredential row, never `credentialFor()` [[fulfillment-routing]] [[vendor-order-sync-mechanics]].
- Do NOT email migrated WP customers until Bam says who gets what [[wp-customer-migration]].
- Bam standing "leave the dups, I'll handle it" — do NOT cluster/delete the Bird Season Snapback /
  Sweat Shorts duplicate-name products.

## FLAGGED (noticed, not fixed)
- **Live pm2 env is a stale snapshot of `.env`.** `ecosystem.config.cjs` reads `.env` only at
  `pm2 start`; `CAREERS_INBOX`, `MAIL_FROM`, `SMTP_HOST` are in `.env` on the box but ABSENT from the
  running `therum-cms-api` env (added after the last full start; deploys reload by name). Mail still
  works (transport DB-sourced), and careers now has a code fallback — so nothing is broken today. To
  actually sync env, do a full `pm2 reload ecosystem.config.cjs --update-env` (NOT reload-by-name) —
  but that would also inject whatever `SMTP_HOST`/`MAIL_FROM` are in `.env` into a process whose mail
  currently works via DB; check those values won't override the working DB transport BEFORE doing it.
- **ROTATE the Gmail SMTP app password** — Bam pasted it in chat once (exposed). Carried from the
  Aug state; confirm whether already rotated.
- Printful billing card expired / Printify billing confirm — Bam's to handle [[fulfillment-routing]].
- Nav: the 5 T2 collections are orphaned from `site.menu` (Bam said "hold for now").
- `_core/memory.md` was 407KB append-only until this 2026-09-12 consolidation.

---
Completion status of last loop: NEEDS_CONTEXT — careers edit paused on Bam's "page should be bricks"
(is the careers page meant to stay a 2.0 Content page, or be authored in Bricks?). Payments PayPal fix
awaits a live/sandbox capture to certify.

## 2026-09-15 — Flow shipped; wallets/pins/fonts/Foot Locker fixes (status: DONE_WITH_CONCERNS)
- Built + deployed **Flow** (Therum OS email/SMS engine, own sidebar section): subscribers/lists, block composer w/ per-block HTML, campaigns + schedule + worker send + open/click/opt-out tracking, segments, automations (welcome w/ shared `WELCOME10` once-per-person, cart, review, win-back), popup (logo, 10% off, once-per-browser rules), calendar, weekly slot Mon 10:00 ET, frequency cap 2/wk, SMS via Twilio (built, unverified — no Twilio connected). Live+ON: popup + welcome. Details: memory `marketing-module-groundwork.md`.
- Fixed pre-existing: unsubscribe link 404 + one-click 415; product images blocked in mail (CORP header); Roboto Condensed/Montserrat never loaded; headings → Manrope to match :10025; Printify wallet publish errors (vendor_id NULL on legacy rows); Foot Locker exclusives buyable via PDP/cart (closed; 0 orders affected); City Series blog post had no links.
- Concerns: 4 pins still unlinked on Printify (re-publish clobbers curation); `settings.site.tagline`="AuditTag" leftover; frequency cap + SMS not exercised live; per-campaign From name not built.
- Failures logged: _core/FAILURES.md (uploads 504 ~2min from an ungated deploy; Foot Locker PDP miss).

## 2026-09-16 — PodPluser order 100074 finally on their side (status: DONE_WITH_CONCERNS)
- Root cause (evidence in memory `vendor-order-sync-mechanics.md`): PodPluser creates from the webhook body only (never pulls); it resolves `product_id/variation_id` against the ids of ITS OWN pushed copy (155/1782), not our branded product (131/1234). The one push with their ids was the only one their server processed (500 = handled). Secondary: shopper-typed state "Pa" + we sent no phone.
- Fixes deployed: (1) webhook lines now carry the partner-owned twin's ids (`partnerTwinIds` in scopeOrderDelivery; blast radius = hoodie 131↔155 only); (2) `ShipAddressInput` uppercases 2-letter regions/country at checkout (verified on a throwaway cart, removed); (3) payload sends phone.
- Concern: which of the three their handler keys on is only provable on the next real PodPluser order. Bam to confirm exactly one 100074 on their side (7 pushes today) with Dark Green / M.
