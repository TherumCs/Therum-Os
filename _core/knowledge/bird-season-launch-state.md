---
name: bird-season-launch-state
description: sidemoney.co launch facts that still matter — what runs where, the 25MB animated-webp lesson, how the homepage is stored, and the 2.0-production roadmap Bam set
metadata: 
  node_type: memory
  type: project
  originSessionId: f4504c37-caac-4f64-affa-6039105bec50
  modified: 2026-08-15T00:20:16.877Z
---

sidemoney.co launched **2026-08-14** with the Bird Season (Eagles) capsule. Version **2.0.0-beta.9** (API + admin); CHANGELOG.md has the full launch entry. Bam's verdict: "this shit is good to go." Next up (later, separate): a Therum OS **2.0 production** cut from beta.9, and a fresh **Ethereum** site.

**Money path proven** with the first real order on launch day (Aug 2026). Everything else in the orders table is a test (`test@`/`shoptest@`/`audit@`/`bamleon` emails, $0.50 amounts) or an abandoned checkout (no email). Payments connected: Stripe + PayPal + Square. Order emails send (SMTP via smtp.gmail.com — `mailTransport()` reports ready). Contrado fulfillment connection is in `error` state but HARMLESS — nothing routes to it (vendors: inhouse/PODpartner/PodPluser/Tapstitch/Printify).

**SSL is hands-off.** Let's Encrypt cert valid to Oct 30 2026 AND `certbot.timer` is active on the VPS (auto-renews twice-daily, inside 30 days). Full chain (ISRG X2/X1), `Verify return code: 0`. HSTS 1yr, CSP `default-src 'self'`, X-Frame SAMEORIGIN, nosniff, no-referrer all live. Admin gated at `/tos-admin`. Don't panic about the Oct expiry — it renews itself.

**Performance — the 25MB trap.** The homepage was **25MB** because the four category tiles (mens/womens-category/playmoney/home-category.webp in `/var/www/sidemoney-static/wp-content/uploads/2026/03/`, owned by www-data, NOT therum-writable) were **120-frame animated webp** (10/8/4.5/2.5MB). Fix that worked: **sharp reads animated-webp frames** (`sharp(f,{page:i})`; ffmpeg's own webp decoder canNOT read animated webp), **ffmpeg encodes the PNG sequence → h264 mp4** (h264 needs even dims — add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`), upload via mediaService, swap the body `<img>`→`<video autoplay muted loop playsinline preload="none" poster=static>`. Result: 25MB → ~200KB initial paint, 494KB of lazy mp4, motion kept. **A static ffmpeg lives at `~/bin/ffmpeg` on the box** (I installed it; no system ffmpeg). Frame-extract of ~120 frames × N images is slow — run it backgrounded with `nohup`/detached, not inline (times out at 2min).

**Homepage is content (`db.content` slug `sidemoney-home`), body at `body.props.content`; per-element CSS/background-images in `body.meta.css`.** The two-column video band (guy-blue left, girl-black right) sits above Reserve Notes; season jersey panels (`#brxe-tscbrd1` Eagles / `#brxe-tscbrd2` Sixers) are meta.css backgrounds. Still open, non-blocking: Apple Pay in-sheet shipping (held — untestable without a device, current form-then-pay works), 7 test orders to clear, woo74 Corduroy Dad Hat swatches (Bam's).

**Roadmap (Bam's plan, 2026-08-14 wrap):** do NOT cut a Therum OS **2.0 production** tag yet — beta.9 is live and good, but first needs a **deep MANUAL audit**: walk every backend user-flow and settings screen by hand and confirm each setting actually links to behavior. Bam's point (correct): code/DB/browser audits miss flow-level gaps that only surface by physically stepping through. Sequence: manual audit → 2.0 production → future features on a **milestone schedule**. Separate to-do (not urgent): the **Therum OS core-update mechanism is janky** — updating core files by hand-uploading a ZIP through GitHub; wants a real release/update process instead. Next new project after this: a fresh **Ethereum site**.

See [[storefront-merchandising]], [[live-store-real-money]], [[fulfillment-routing]].
